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
# two-axis (v0.4): gate falls back from document_quality when a run predates the gate axis
GATE_FROM_DQ = {"PASS": "ALLOW", "FAIL": "BLOCK",
                "INCOMPLETE_EVALUATION": "INCOMPLETE", "INCOMPLETE": "INCOMPLETE"}


def gate_of(explicit, dq):
    g = str(explicit).upper() if explicit else GATE_FROM_DQ.get(str(dq).upper(), str(dq).upper())
    return g


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
    # §4.4: version metadata from CLI (not hardcoded); default to v0.4 / dataset 4 / run-id from the dir
    skill_version = argv[argv.index("--skill-version") + 1] if "--skill-version" in argv else "0.4.0"
    dataset_version = argv[argv.index("--dataset-version") + 1] if "--dataset-version" in argv else "4"
    run_id = argv[argv.index("--run-id") + 1] if "--run-id" in argv else raw_path.parent.name
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
        got_gate = gate_of(v.get("gate_decision"), dq)
        exp_gate = gate_of(exp.get("gate_decision"), exp.get("document_quality"))
        # §4.1 primary correctness: got gate matches the manifest's explicit expected gate
        gate_mismatch = (exp_gate in ("ALLOW", "BLOCK", "INCOMPLETE")) and (got_gate != exp_gate)
        # §4.2 required-finding recall (machine-scored findings)
        req_find = [str(x).lower() for x in (exp.get("required_findings") or [])]
        got_find = {str(x).lower() for x in (v.get("finding_codes") or [])}
        # only count findings that use the controlled code vocabulary (skip free-text required_findings)
        req_find_codes = [x for x in req_find if re.match(r"^[a-z0-9]+(-[a-z0-9]+)+$", x)]
        find_rec = (len([x for x in req_find_codes if x in got_find]) / len(req_find_codes)) if req_find_codes else None
        per_run.append({
            "case_id": cid, "class": cls, "pair_id": m.get("pair_id"),
            "run_kind": r.get("run_kind"), "run_idx": r.get("run_idx"),
            "expected": exp.get("document_quality"), "got": dq,
            "exp_gate": exp_gate, "got_gate": got_gate, "gate_mismatch": gate_mismatch,
            "quality_band": str(v.get("quality_band", "")).upper() or None,
            "profile_echoed": bool(v.get("evaluation_profile") or v.get("profile_echoed")),
            "required": sorted(required), "forbidden": sorted(forbidden), "reported": sorted(reported),
            "recall": rec, "forbidden_violation": sorted(reported & forbidden),
            "req_find_codes": req_find_codes, "got_find": sorted(got_find), "finding_recall": find_rec,
            "total_score": v.get("total_score"),
            "factual_validity": v.get("factual_validity"), "reader_test": v.get("reader_test"),
        })

    cur = [x for x in per_run if x["run_kind"] == "current"]

    # §4.1 PRIMARY correctness metric: gate matches the explicit expected gate (works for ALLOW negatives too)
    gate_mismatches = [x for x in cur if x["gate_mismatch"]]
    # class-based positive/negative kept as SECONDARY (advisory)
    neg_false_pass = [x for x in cur if x["class"] in NEG and x["got_gate"] == "ALLOW" and x["exp_gate"] != "ALLOW"]
    pos_false_fail = [x for x in cur if x["class"] in POS and x["got_gate"] != "ALLOW" and x["exp_gate"] == "ALLOW"]
    profile_compliance = (sum(1 for x in per_run if x["profile_echoed"]) / len(per_run)) if per_run else 1.0

    # §4.2 pooled required-finding recall over current runs that declare finding codes
    fi = ft = 0
    for x in cur:
        if x["req_find_codes"]:
            fi += len([c for c in x["req_find_codes"] if c in set(x["got_find"])]); ft += len(x["req_find_codes"])
    finding_recall = (fi / ft) if ft else 1.0

    # pooled required-blocker recall over negative current runs that declare required blockers
    inter = tot = 0
    for x in cur:
        if x["class"] in NEG and x["required"]:
            inter += len(set(x["required"]) & set(x["reported"])); tot += len(x["required"])
    recall = (inter / tot) if tot else 1.0

    viol = [x for x in per_run if x["forbidden_violation"]]
    viol_rate = len(viol) / len(per_run) if per_run else 0.0

    # boundary pair ordering (current runs) — gate axis: pass side ALLOW, fail side non-ALLOW
    pairs = {}
    for x in cur:
        if x["pair_id"]:
            pairs.setdefault(x["pair_id"], {})[x["class"]] = x["got_gate"]
    pair_ok = {p: (d.get("boundary-pass") == "ALLOW" and d.get("boundary-fail") in ("BLOCK", "INCOMPLETE"))
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
            verdicts = [x["got_gate"] for x in xs]
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
        "gate_expectation_mismatch_count": len(gate_mismatches),           # == 0  (PRIMARY, §4.1)
        "golden_negative_false_pass": len(neg_false_pass),                 # == 0  (secondary)
        "golden_positive_false_hard_fail": len(pos_false_fail),            # == 0  (secondary)
        "required_blocker_recall": round(recall, 3),                       # >= 0.90
        "required_finding_recall": round(finding_recall, 3),              # >= 0.90 (§4.2)
        "forbidden_blocker_violation_rate": round(viol_rate, 3),          # <= 0.05
        "boundary_pair_ordering_accuracy": round(ordering, 3),            # == 1.0
        "three_run_verdict_consistency": round(consistency, 3),           # == 1.0 (gate axis)
        "max_score_stddev": max_stddev,                                    # <= 5
        "profile_echo_compliance": round(profile_compliance, 3),          # == 1.0
    }
    passed = (bar["gate_expectation_mismatch_count"] == 0
              and bar["golden_negative_false_pass"] == 0 and bar["golden_positive_false_hard_fail"] == 0
              and bar["required_blocker_recall"] >= 0.90 and bar["required_finding_recall"] >= 0.90
              and bar["forbidden_blocker_violation_rate"] <= 0.05
              and bar["boundary_pair_ordering_accuracy"] == 1.0 and bar["three_run_verdict_consistency"] == 1.0
              and bar["max_score_stddev"] <= 5 and bar["profile_echo_compliance"] == 1.0)

    metrics = {"skill_version": skill_version, "dataset_version": dataset_version, "run_id": run_id,
               "n_runs": len(per_run), "n_current": len(cur), "bar": bar, "promotion_bar_met": passed,
               "gate_mismatch_cases": [{"case": x["case_id"], "expected": x["exp_gate"], "got": x["got_gate"]} for x in gate_mismatches],
               "negative_false_pass_cases": [x["case_id"] for x in neg_false_pass],
               "positive_false_fail_cases": [x["case_id"] for x in pos_false_fail],
               "forbidden_violations": [{"case": x["case_id"], "fired": x["forbidden_violation"]} for x in viol],
               "boundary_pairs": pair_ok, "stability": stability, "per_run": per_run}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    # evaluation-summary.md  (§4.4: version from CLI/metadata, not hardcoded)
    L = [f"# Blind-matrix evaluation summary — documentation-quality-evaluator v{skill_version}",
         "", f"Runs: {len(per_run)} ({len(cur)} current + {len(per_run)-len(cur)} repeat). "
         f"Corpus dataset_version {dataset_version}. run_id={run_id}.", "",
         "## Promotion bar (two-axis)", "", "| metric | value | bar | ok |", "|---|---|---|---|"]
    checks = [("gate-expectation mismatch (PRIMARY)", bar["gate_expectation_mismatch_count"], "== 0", bar["gate_expectation_mismatch_count"] == 0),
              ("golden-negative false ALLOW", bar["golden_negative_false_pass"], "== 0", bar["golden_negative_false_pass"] == 0),
              ("golden-positive false non-ALLOW", bar["golden_positive_false_hard_fail"], "== 0", bar["golden_positive_false_hard_fail"] == 0),
              ("required-blocker recall", bar["required_blocker_recall"], ">= 0.90", bar["required_blocker_recall"] >= 0.90),
              ("required-finding recall", bar["required_finding_recall"], ">= 0.90", bar["required_finding_recall"] >= 0.90),
              ("forbidden-blocker violation rate", bar["forbidden_blocker_violation_rate"], "<= 0.05", bar["forbidden_blocker_violation_rate"] <= 0.05),
              ("boundary-pair ordering", bar["boundary_pair_ordering_accuracy"], "== 1.0", bar["boundary_pair_ordering_accuracy"] == 1.0),
              ("3-run gate consistency", bar["three_run_verdict_consistency"], "== 1.0", bar["three_run_verdict_consistency"] == 1.0),
              ("max score stddev", bar["max_score_stddev"], "<= 5", bar["max_score_stddev"] <= 5),
              ("profile echo compliance", bar["profile_echo_compliance"], "== 1.0", bar["profile_echo_compliance"] == 1.0)]
    for name, val, thr, ok in checks:
        L.append(f"| {name} | {val} | {thr} | {'✅' if ok else '❌'} |")
    L += ["", f"**PROMOTION BAR: {'MET ✅' if passed else 'NOT MET ❌'}**", "",
          "## Per-case (current runs)", "", "| case | class | exp_gate | got_gate | ✓ | recall | find-rec | forbidden-fired |",
          "|---|---|---|---|---|---|---|---|"]
    for x in sorted(cur, key=lambda r: (r["class"] or "", r["case_id"])):
        L.append(f"| {x['case_id']} | {x['class']} | {x['exp_gate']} | {x['got_gate']} | "
                 f"{'❌' if x['gate_mismatch'] else '✅'} | "
                 f"{'' if x['recall'] is None else round(x['recall'],2)} | "
                 f"{'' if x['finding_recall'] is None else round(x['finding_recall'],2)} | "
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
