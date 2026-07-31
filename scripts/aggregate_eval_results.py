#!/usr/bin/env python3
"""
aggregate_eval_results.py — compute the §11 blind-matrix metrics + §17 promotion checklist from raw
evaluator verdicts, comparing each run to its case manifest (the expected labels the runner never saw).

Input: a raw-results JSON = list of runs, each:
  {case_id, run_kind, run_idx, blind_id, verdict: {document_quality, factual_validity, reader_test,
                                                    checker_status, blockers: [...], confidence, total_score?}}

Output (to <out-dir>, default the raw file's dir): metrics.json + evaluation-summary.md.
Exit 0 iff the §17 promotion bar is met.

Usage: python scripts/aggregate_eval_results.py <raw-results.json> [--out <dir>]
"""
from __future__ import annotations
import json
import re
import statistics
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
HF = re.compile(r"(HF-\d+[a-e]?)", re.I)
POS = {"golden-positive", "boundary-pass"}
NEG = {"golden-negative", "boundary-fail"}


def norm(xs):
    out = set()
    for x in xs or []:
        m = HF.match(str(x).strip())
        if m:
            out.add(m.group(1).upper())
    return out


def load_manifests():
    by_id = {}
    for mp in CASES.glob("**/manifest.yaml"):
        if "quarantine" in mp.parts:      # archived v1 snapshots are excluded from all metrics
            continue
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        by_id[m["case_id"]] = m
    return by_id


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: aggregate_eval_results.py <raw-results.json> [--out <dir>]", file=sys.stderr)
        return 2
    raw_path = Path(args[0])
    out_dir = (Path(argv[argv.index("--out") + 1]) if "--out" in argv else raw_path.parent).resolve()
    runs = json.loads(raw_path.read_text(encoding="utf-8"))
    man = load_manifests()

    per_run = []
    for r in runs:
        cid = r["case_id"]; m = man.get(cid, {})
        exp = (m.get("expected", {}) or {})
        cls = m.get("class")
        v = r.get("verdict", {}) or {}
        dq = str(v.get("document_quality", "?")).upper()
        reported = norm(v.get("blockers"))
        required = norm(exp.get("required_blockers"))
        forbidden = norm(exp.get("forbidden_blockers"))
        rec = (len(required & reported) / len(required)) if required else None
        per_run.append({
            "case_id": cid, "class": cls, "pair_id": m.get("pair_id"),
            "run_kind": r.get("run_kind"), "run_idx": r.get("run_idx"),
            "expected": exp.get("document_quality"), "got": dq,
            "required": sorted(required), "forbidden": sorted(forbidden), "reported": sorted(reported),
            "recall": rec, "forbidden_violation": sorted(reported & forbidden),
            "total_score": v.get("total_score"),
            "factual_validity": v.get("factual_validity"), "reader_test": v.get("reader_test"),
        })

    cur = [x for x in per_run if x["run_kind"] == "current"]

    neg_false_pass = [x for x in cur if x["class"] in NEG and x["got"] == "PASS"]
    pos_false_fail = [x for x in cur if x["class"] in POS and x["got"] == "FAIL"]

    # pooled required-blocker recall over negative current runs that declare required blockers
    inter = tot = 0
    for x in cur:
        if x["class"] in NEG and x["required"]:
            inter += len(set(x["required"]) & set(x["reported"])); tot += len(x["required"])
    recall = (inter / tot) if tot else 1.0

    viol = [x for x in per_run if x["forbidden_violation"]]
    viol_rate = len(viol) / len(per_run) if per_run else 0.0

    # boundary pair ordering (current runs)
    pairs = {}
    for x in cur:
        if x["pair_id"]:
            pairs.setdefault(x["pair_id"], {})[x["class"]] = x["got"]
    pair_ok = {p: (d.get("boundary-pass") == "PASS" and d.get("boundary-fail") == "FAIL")
               for p, d in pairs.items()}
    ordering = (sum(pair_ok.values()) / len(pair_ok)) if pair_ok else 1.0

    # stability: cases with >1 run
    from collections import defaultdict
    runs_by_case = defaultdict(list)
    for x in per_run:
        runs_by_case[x["case_id"]].append(x)
    stability = {}
    for cid, xs in runs_by_case.items():
        if len(xs) > 1:
            verdicts = [x["got"] for x in xs]
            scores = [x["total_score"] for x in xs if isinstance(x["total_score"], (int, float))]
            blsets = [set(x["reported"]) for x in xs]
            jac = 1.0
            if len(blsets) > 1:
                u = set().union(*blsets); i = set(blsets[0]).intersection(*blsets[1:])
                jac = (len(i) / len(u)) if u else 1.0
            stability[cid] = {
                "n": len(xs), "verdicts": verdicts,
                "consistent": len(set(verdicts)) == 1,
                "blocker_jaccard": round(jac, 3),
                "score_stddev": round(statistics.pstdev(scores), 2) if len(scores) > 1 else None,
            }
    consistency = (sum(1 for s in stability.values() if s["consistent"]) / len(stability)) if stability else 1.0
    max_stddev = max((s["score_stddev"] for s in stability.values() if s["score_stddev"] is not None), default=0.0)

    bar = {
        "golden_negative_false_pass": len(neg_false_pass),                 # == 0
        "golden_positive_false_hard_fail": len(pos_false_fail),            # == 0
        "required_blocker_recall": round(recall, 3),                       # >= 0.90
        "forbidden_blocker_violation_rate": round(viol_rate, 3),          # <= 0.05
        "boundary_pair_ordering_accuracy": round(ordering, 3),            # == 1.0
        "three_run_verdict_consistency": round(consistency, 3),           # == 1.0
        "max_score_stddev": max_stddev,                                    # <= 5
    }
    passed = (bar["golden_negative_false_pass"] == 0 and bar["golden_positive_false_hard_fail"] == 0
              and bar["required_blocker_recall"] >= 0.90 and bar["forbidden_blocker_violation_rate"] <= 0.05
              and bar["boundary_pair_ordering_accuracy"] == 1.0 and bar["three_run_verdict_consistency"] == 1.0
              and bar["max_score_stddev"] <= 5)

    metrics = {"n_runs": len(per_run), "n_current": len(cur), "bar": bar, "promotion_bar_met": passed,
               "negative_false_pass_cases": [x["case_id"] for x in neg_false_pass],
               "positive_false_fail_cases": [x["case_id"] for x in pos_false_fail],
               "forbidden_violations": [{"case": x["case_id"], "fired": x["forbidden_violation"]} for x in viol],
               "boundary_pairs": pair_ok, "stability": stability, "per_run": per_run}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    # evaluation-summary.md
    L = ["# Blind-matrix evaluation summary — documentation-quality-evaluator v0.3",
         "", f"Runs: {len(per_run)} ({len(cur)} current + {len(per_run)-len(cur)} repeat). "
         f"Corpus dataset_version 3.", "",
         "## §17 promotion bar", "", "| metric | value | bar | ok |", "|---|---|---|---|"]
    checks = [("golden-negative false PASS", bar["golden_negative_false_pass"], "== 0", bar["golden_negative_false_pass"] == 0),
              ("golden-positive false hard FAIL", bar["golden_positive_false_hard_fail"], "== 0", bar["golden_positive_false_hard_fail"] == 0),
              ("required-blocker recall", bar["required_blocker_recall"], ">= 0.90", bar["required_blocker_recall"] >= 0.90),
              ("forbidden-blocker violation rate", bar["forbidden_blocker_violation_rate"], "<= 0.05", bar["forbidden_blocker_violation_rate"] <= 0.05),
              ("boundary-pair ordering", bar["boundary_pair_ordering_accuracy"], "== 1.0", bar["boundary_pair_ordering_accuracy"] == 1.0),
              ("3-run verdict consistency", bar["three_run_verdict_consistency"], "== 1.0", bar["three_run_verdict_consistency"] == 1.0),
              ("max score stddev", bar["max_score_stddev"], "<= 5", bar["max_score_stddev"] <= 5)]
    for name, val, thr, ok in checks:
        L.append(f"| {name} | {val} | {thr} | {'✅' if ok else '❌'} |")
    L += ["", f"**PROMOTION BAR: {'MET ✅' if passed else 'NOT MET ❌'}**", "",
          "## Per-case (current runs)", "", "| case | class | expected | got | recall | forbidden-fired |",
          "|---|---|---|---|---|---|"]
    for x in sorted(cur, key=lambda r: (r["class"], r["case_id"])):
        L.append(f"| {x['case_id']} | {x['class']} | {x['expected']} | {x['got']} | "
                 f"{'' if x['recall'] is None else round(x['recall'],2)} | "
                 f"{','.join(x['forbidden_violation']) or '—'} |")
    L += ["", "## Boundary-pair ordering", ""]
    for p, ok in sorted(pair_ok.items()):
        L.append(f"- {p}: {'✅ correct' if ok else '❌ WRONG'}")
    L += ["", "## Stability (repeat cases)", ""]
    for cid, s in sorted(stability.items()):
        L.append(f"- {cid}: verdicts {s['verdicts']} — {'consistent ✅' if s['consistent'] else 'INCONSISTENT ❌'}; "
                 f"blocker Jaccard {s['blocker_jaccard']}; score σ {s['score_stddev']}")
    (out_dir / "evaluation-summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"# aggregate -> {(out_dir/'metrics.json').as_posix()} + evaluation-summary.md")
    for name, val, thr, ok in checks:
        print(f"  [{'ok ' if ok else 'FAIL'}] {name}: {val} ({thr})")
    print(f"\n==> §17 promotion bar: {'MET' if passed else 'NOT MET'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
