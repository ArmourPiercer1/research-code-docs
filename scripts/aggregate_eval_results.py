#!/usr/bin/env python3
"""
aggregate_eval_results.py — compute the blind-matrix metrics + admission checklist from raw evaluator
verdicts, comparing each run to its case manifest (the expected labels the runner never saw).

Input: a raw-results JSON = list of runs, each:
  {arm?, case_id, run_kind, run_idx, run_key?,
   verdict: {quality_band, gate_decision, document_quality, factual_validity, reader_test, checker_status,
             blockers: [...], finding_codes: [...], evaluation_profile?, confidence, total_score?},
   checker?: {files_checked, target}}

`arm` is optional. With no arm field every run is one implicit arm (backward compatible with the
2026-07-31 blind matrix + the diag-2026-08-02 single-arm run). With arms present, the admission bar is
scored on the CANDIDATE arm (default "v0.4.1" or --candidate-arm) and a per-arm comparison is emitted.

Two-axis + v0.4.1 additions (DQE_D3决策与PhaseE安全准入计划 §3/§6):
  - terminal_green (derived, §3): GATE=ALLOW AND FACTUAL_VALIDITY!=UNVERIFIED AND CHECKER_STATUS=COMPLETE
    AND READER_TEST=PASS. An ALLOW is NOT automatically a green terminal gate.
  - terminal_contract_mismatch_count (§3.3): derived terminal_green vs manifest expected.terminal_green.
  - checker_execution_compliance (§6.1): every candidate run has CHECKER_STATUS=COMPLETE, files_checked>=1,
    and a checker target that matches the manifest document.

Output (to <out-dir>, default the raw file's dir): metrics.json + evaluation-summary.md.
Exit 0 iff the candidate arm meets the admission bar.

Usage: python scripts/aggregate_eval_results.py <raw-results.json> [--out <dir>] [--candidate-arm v0.4.1]
       [--skill-version 0.4.1] [--dataset-version 4] [--run-id <id>]
"""
from __future__ import annotations
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
HF = re.compile(r"(HF-\d+[a-e]?)", re.I)
POS = {"golden-positive", "boundary-pass"}
NEG = {"golden-negative", "boundary-fail"}
# two-axis (v0.4): gate falls back from document_quality when a run predates the gate axis (e.g. v0.3 arm)
GATE_FROM_DQ = {"PASS": "ALLOW", "FAIL": "BLOCK",
                "INCOMPLETE_EVALUATION": "INCOMPLETE", "INCOMPLETE": "INCOMPLETE"}


def gate_of(explicit, dq):
    return str(explicit).upper() if explicit else GATE_FROM_DQ.get(str(dq).upper(), str(dq).upper())


def terminal_green_of(gate, factual_validity, checker_status, reader_test) -> bool:
    """§3 terminal-green derivation. An ALLOW alone is not terminal-green."""
    fv = str(factual_validity or "UNVERIFIED").upper()
    return (str(gate).upper() == "ALLOW"
            and fv not in ("UNVERIFIED", "?", "NONE", "")
            and str(checker_status or "").upper() == "COMPLETE"
            and str(reader_test or "").upper() == "PASS")


def target_ok(checker_target, manifest_doc):
    """Did the run's checker actually target the manifest document? None = unknown (not recorded)."""
    if not checker_target or not manifest_doc:
        return None
    t = str(checker_target).replace("\\", "/").strip()
    d = str(manifest_doc).replace("\\", "/").strip()
    return t.endswith(d) or d.endswith(t)


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


def parse_runs(runs, man):
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
        gate_mismatch = (exp_gate in ("ALLOW", "BLOCK", "INCOMPLETE")) and (got_gate != exp_gate)
        req_find = [str(x).lower() for x in (exp.get("required_findings") or [])]
        got_find = {str(x).lower() for x in (v.get("finding_codes") or [])}
        req_find_codes = [x for x in req_find if re.match(r"^[a-z0-9]+(-[a-z0-9]+)+$", x)]
        find_rec = (len([x for x in req_find_codes if x in got_find]) / len(req_find_codes)) if req_find_codes else None
        # v0.4.1: terminal-green + terminal-contract + checker-execution
        checker_status = v.get("checker_status")
        tgreen = terminal_green_of(got_gate, v.get("factual_validity"), checker_status, v.get("reader_test"))
        exp_tgreen = exp.get("terminal_green")            # optional bool in manifest
        tcontract_mismatch = (exp_tgreen is not None) and (bool(tgreen) != bool(exp_tgreen))
        chk = r.get("checker", {}) or {}
        files_checked = chk.get("files_checked")
        tgt_ok = target_ok(chk.get("target"), m.get("document"))
        checker_ok = (str(checker_status or "").upper() == "COMPLETE"
                      and isinstance(files_checked, int) and files_checked >= 1
                      and tgt_ok is True)
        per_run.append({
            "arm": r.get("arm") or "(single)",
            "case_id": cid, "class": cls, "pair_id": m.get("pair_id"),
            "run_kind": r.get("run_kind"), "run_idx": r.get("run_idx"), "run_key": r.get("run_key"),
            "expected": exp.get("document_quality"), "got": dq,
            "exp_gate": exp_gate, "got_gate": got_gate, "gate_mismatch": gate_mismatch,
            "quality_band": str(v.get("quality_band", "")).upper() or None,
            "profile_echoed": bool(v.get("evaluation_profile") or v.get("profile_echoed")),
            "required": sorted(required), "forbidden": sorted(forbidden), "reported": sorted(reported),
            "recall": rec, "forbidden_violation": sorted(reported & forbidden),
            "req_find_codes": req_find_codes, "got_find": sorted(got_find), "finding_recall": find_rec,
            "total_score": v.get("total_score"),
            "factual_validity": v.get("factual_validity"), "reader_test": v.get("reader_test"),
            "checker_status": checker_status, "files_checked": files_checked,
            "terminal_green": tgreen, "exp_terminal_green": exp_tgreen,
            "tcontract_mismatch": tcontract_mismatch, "checker_ok": checker_ok, "checker_target_ok": tgt_ok,
        })
    return per_run


def score(rows):
    """Score ONE arm's per-run rows. Returns (bar, details). Identical formulas across arms."""
    cur = [x for x in rows if x["run_kind"] == "current"]
    gate_mismatches = [x for x in cur if x["gate_mismatch"]]
    neg_false_pass = [x for x in cur if x["class"] in NEG and x["got_gate"] == "ALLOW" and x["exp_gate"] != "ALLOW"]
    pos_false_fail = [x for x in cur if x["class"] in POS and x["got_gate"] != "ALLOW" and x["exp_gate"] == "ALLOW"]
    profile_compliance = (sum(1 for x in rows if x["profile_echoed"]) / len(rows)) if rows else 1.0

    fi = ft = 0
    for x in cur:
        if x["req_find_codes"]:
            fi += len([c for c in x["req_find_codes"] if c in set(x["got_find"])]); ft += len(x["req_find_codes"])
    finding_recall = (fi / ft) if ft else 1.0

    inter = tot = 0
    for x in cur:
        if x["class"] in NEG and x["required"]:
            inter += len(set(x["required"]) & set(x["reported"])); tot += len(x["required"])
    recall = (inter / tot) if tot else 1.0

    viol = [x for x in rows if x["forbidden_violation"]]
    viol_rate = len(viol) / len(rows) if rows else 0.0

    pairs = {}
    for x in cur:
        if x["pair_id"]:
            pairs.setdefault(x["pair_id"], {})[x["class"]] = x["got_gate"]
    pair_ok = {p: (d.get("boundary-pass") == "ALLOW" and d.get("boundary-fail") in ("BLOCK", "INCOMPLETE"))
               for p, d in pairs.items()}
    ordering = (sum(pair_ok.values()) / len(pair_ok)) if pair_ok else 1.0

    runs_by_case = defaultdict(list)
    for x in rows:
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
            stability[cid] = {"n": len(xs), "verdicts": verdicts, "consistent": len(set(verdicts)) == 1,
                              "blocker_jaccard": round(jac, 3),
                              "score_stddev": round(statistics.pstdev(scores), 2) if len(scores) > 1 else None}
    consistency = (sum(1 for s in stability.values() if s["consistent"]) / len(stability)) if stability else 1.0
    max_stddev = max((s["score_stddev"] for s in stability.values() if s["score_stddev"] is not None), default=0.0)

    tcontract = [x for x in rows if x["tcontract_mismatch"]]
    checker_ok_n = sum(1 for x in rows if x["checker_ok"])
    checker_compliance = (checker_ok_n / len(rows)) if rows else 1.0

    bar = {
        "gate_expectation_mismatch_count": len(gate_mismatches),           # == 0  (PRIMARY)
        "terminal_contract_mismatch_count": len(tcontract),                # == 0  (§3.3)
        "golden_negative_false_pass": len(neg_false_pass),                 # == 0
        "golden_positive_false_hard_fail": len(pos_false_fail),            # == 0
        "required_blocker_recall": round(recall, 3),                       # >= 0.90
        "required_finding_recall": round(finding_recall, 3),              # >= 0.90
        "forbidden_blocker_violation_rate": round(viol_rate, 3),          # == 0
        "boundary_pair_ordering_accuracy": round(ordering, 3),            # == 1.0
        "three_run_verdict_consistency": round(consistency, 3),           # == 1.0
        "max_score_stddev": max_stddev,                                    # <= 5
        "profile_echo_compliance": round(profile_compliance, 3),          # == 1.0
        "checker_execution_compliance": round(checker_compliance, 3),     # == 1.0 (§6.1)
    }
    details = {"gate_mismatches": gate_mismatches, "neg_false_pass": neg_false_pass,
               "pos_false_fail": pos_false_fail, "tcontract": tcontract, "viol": viol,
               "pair_ok": pair_ok, "stability": stability, "cur": cur,
               "checker_bad": [x for x in rows if not x["checker_ok"]]}
    return bar, details


def bar_passed(b) -> bool:
    return (b["gate_expectation_mismatch_count"] == 0 and b["terminal_contract_mismatch_count"] == 0
            and b["golden_negative_false_pass"] == 0 and b["golden_positive_false_hard_fail"] == 0
            and b["required_blocker_recall"] >= 0.90 and b["required_finding_recall"] >= 0.90
            and b["forbidden_blocker_violation_rate"] == 0.0
            and b["boundary_pair_ordering_accuracy"] == 1.0 and b["three_run_verdict_consistency"] == 1.0
            and b["max_score_stddev"] <= 5 and b["profile_echo_compliance"] == 1.0
            and b["checker_execution_compliance"] == 1.0)


CHECK_ROWS = [
    ("gate-expectation mismatch (PRIMARY)", "gate_expectation_mismatch_count", "== 0", lambda v: v == 0),
    ("terminal-contract mismatch", "terminal_contract_mismatch_count", "== 0", lambda v: v == 0),
    ("golden-negative false ALLOW", "golden_negative_false_pass", "== 0", lambda v: v == 0),
    ("golden-positive false non-ALLOW", "golden_positive_false_hard_fail", "== 0", lambda v: v == 0),
    ("required-blocker recall", "required_blocker_recall", ">= 0.90", lambda v: v >= 0.90),
    ("required-finding recall", "required_finding_recall", ">= 0.90", lambda v: v >= 0.90),
    ("forbidden-blocker violation rate", "forbidden_blocker_violation_rate", "== 0", lambda v: v == 0.0),
    ("boundary-pair ordering", "boundary_pair_ordering_accuracy", "== 1.0", lambda v: v == 1.0),
    ("3-run gate consistency", "three_run_verdict_consistency", "== 1.0", lambda v: v == 1.0),
    ("max score stddev", "max_score_stddev", "<= 5", lambda v: v <= 5),
    ("profile echo compliance", "profile_echo_compliance", "== 1.0", lambda v: v == 1.0),
    ("checker execution compliance", "checker_execution_compliance", "== 1.0", lambda v: v == 1.0),
]


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: aggregate_eval_results.py <raw-results.json> [--out <dir>] [--candidate-arm v0.4.1]", file=sys.stderr)
        return 2
    raw_path = Path(args[0])
    out_dir = (Path(argv[argv.index("--out") + 1]) if "--out" in argv else raw_path.parent).resolve()
    skill_version = argv[argv.index("--skill-version") + 1] if "--skill-version" in argv else "0.4.1"
    dataset_version = argv[argv.index("--dataset-version") + 1] if "--dataset-version" in argv else "4"
    run_id = argv[argv.index("--run-id") + 1] if "--run-id" in argv else raw_path.parent.name
    runs = json.loads(raw_path.read_text(encoding="utf-8"))
    man = load_manifests()
    per_run = parse_runs(runs, man)

    arms = list(dict.fromkeys(x["arm"] for x in per_run))
    if "--candidate-arm" in argv:
        candidate_arm = argv[argv.index("--candidate-arm") + 1]
    elif "v0.4.1" in arms:
        candidate_arm = "v0.4.1"
    else:
        candidate_arm = arms[0]

    cand_runs = [x for x in per_run if x["arm"] == candidate_arm]
    bar, det = score(cand_runs)
    passed = bar_passed(bar)
    arm_bars = {a: score([x for x in per_run if x["arm"] == a])[0] for a in arms}
    multi_arm = len(arms) > 1

    metrics = {"skill_version": skill_version, "dataset_version": dataset_version, "run_id": run_id,
               "candidate_arm": candidate_arm, "arms": arms,
               "n_runs": len(per_run), "n_candidate_runs": len(cand_runs), "n_current": len(det["cur"]),
               "bar": bar, "admission_bar_met": passed, "arm_comparison": arm_bars,
               "gate_mismatch_cases": [{"case": x["case_id"], "expected": x["exp_gate"], "got": x["got_gate"]} for x in det["gate_mismatches"]],
               "terminal_contract_mismatches": [{"case": x["case_id"], "expected_terminal_green": x["exp_terminal_green"], "got_terminal_green": x["terminal_green"], "gate": x["got_gate"], "reader": x["reader_test"], "factual": x["factual_validity"]} for x in det["tcontract"]],
               "checker_noncompliant": [{"case": x["case_id"], "run_key": x["run_key"], "checker_status": x["checker_status"], "files_checked": x["files_checked"], "target_ok": x["checker_target_ok"]} for x in det["checker_bad"]],
               "negative_false_pass_cases": [x["case_id"] for x in det["neg_false_pass"]],
               "positive_false_fail_cases": [x["case_id"] for x in det["pos_false_fail"]],
               "forbidden_violations": [{"case": x["case_id"], "arm": x["arm"], "fired": x["forbidden_violation"]} for x in det["viol"]],
               "boundary_pairs": det["pair_ok"], "stability": det["stability"], "per_run": per_run}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- evaluation-summary.md ----
    L = [f"# Blind-matrix evaluation summary — documentation-quality-evaluator v{skill_version}",
         "", f"Runs: {len(per_run)} across arms {arms}. Candidate arm: **{candidate_arm}** "
         f"({len(cand_runs)} runs, {len(det['cur'])} current). Corpus dataset_version {dataset_version}. run_id={run_id}.",
         "", "## Candidate admission bar", "", "| metric | value | bar | ok |", "|---|---|---|---|"]
    for name, key, thr, ok in CHECK_ROWS:
        L.append(f"| {name} | {bar[key]} | {thr} | {'✅' if ok(bar[key]) else '❌'} |")
    L += ["", f"**ADMISSION BAR ({candidate_arm}): {'MET ✅' if passed else 'NOT MET ❌'}**", ""]

    if multi_arm:
        L += ["## Arm comparison (§6.3)", "", "| metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
        comp_keys = [("gate mismatch", "gate_expectation_mismatch_count"),
                     ("terminal-contract mismatch", "terminal_contract_mismatch_count"),
                     ("required-finding recall", "required_finding_recall"),
                     ("required-blocker recall", "required_blocker_recall"),
                     ("forbidden rate", "forbidden_blocker_violation_rate"),
                     ("gate consistency", "three_run_verdict_consistency"),
                     ("profile echo", "profile_echo_compliance"),
                     ("checker compliance", "checker_execution_compliance")]
        for label, key in comp_keys:
            L.append(f"| {label} | " + " | ".join(str(arm_bars[a][key]) for a in arms) + " |")
        L += ["", "> Comparison arms do not gate the candidate pass/fail; they establish that the candidate "
              "improves over frozen-v0.3 and the no-skill baseline (§6.3).", ""]

    L += ["## Candidate per-case (current runs)", "",
          "| case | class | exp_gate | got_gate | ✓ | recall | find-rec | term-green | forbidden-fired |",
          "|---|---|---|---|---|---|---|---|---|"]
    for x in sorted(det["cur"], key=lambda r: (r["class"] or "", r["case_id"])):
        tg = ("green" if x["terminal_green"] else "—")
        if x["exp_terminal_green"] is not None:
            tg += "/exp:" + ("green" if x["exp_terminal_green"] else "non")
        L.append(f"| {x['case_id']} | {x['class']} | {x['exp_gate']} | {x['got_gate']} | "
                 f"{'❌' if x['gate_mismatch'] else '✅'} | "
                 f"{'' if x['recall'] is None else round(x['recall'],2)} | "
                 f"{'' if x['finding_recall'] is None else round(x['finding_recall'],2)} | "
                 f"{tg} | {','.join(x['forbidden_violation']) or '—'} |")
    if det["tcontract"]:
        L += ["", "## Terminal-contract mismatches", ""]
        for x in det["tcontract"]:
            L.append(f"- {x['case_id']}: expected terminal_green={x['exp_terminal_green']} but derived "
                     f"{x['terminal_green']} (gate={x['got_gate']}, reader={x['reader_test']}, factual={x['factual_validity']})")
    if det["checker_bad"]:
        L += ["", "## Checker-execution non-compliance", ""]
        for x in det["checker_bad"]:
            L.append(f"- {x['case_id']} [{x['run_key']}]: status={x['checker_status']} files_checked={x['files_checked']} target_ok={x['checker_target_ok']}")
    L += ["", "## Boundary-pair ordering (candidate)", ""]
    for p, ok in sorted(det["pair_ok"].items()):
        L.append(f"- {p}: {'✅ correct' if ok else '❌ WRONG'}")
    L += ["", "## Stability (candidate repeat cases)", ""]
    for cid, s in sorted(det["stability"].items()):
        L.append(f"- {cid}: verdicts {s['verdicts']} — {'consistent ✅' if s['consistent'] else 'INCONSISTENT ❌'}; "
                 f"blocker Jaccard {s['blocker_jaccard']}; score σ {s['score_stddev']}")
    (out_dir / "evaluation-summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"# aggregate -> {(out_dir/'metrics.json').as_posix()} + evaluation-summary.md")
    print(f"  candidate arm = {candidate_arm}; arms = {arms}")
    for name, key, thr, ok in CHECK_ROWS:
        print(f"  [{'ok ' if ok(bar[key]) else 'FAIL'}] {name}: {bar[key]} ({thr})")
    print(f"\n==> admission bar ({candidate_arm}): {'MET' if passed else 'NOT MET'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
