#!/usr/bin/env python3
"""
make_phase_e_plan.py — emit the STATIC Phase E admission plan (DQE_D3决策与PhaseE安全准入计划 §4.2/§5).

This produces ONE flat, fully-enumerated, capped list of evaluator runs BEFORE any agent starts. It never
iterates agent output, never expands dynamically, and never emits more than MAX_EVAL_RUNS. That is the
structural fix for the 63M-token runaway: the task set is fixed and counted here, validated by
validate_eval_plan.py, then executed as bounded direct Agent batches.

Arms (§5):
  A  v0.4.1     (snapshot dqe-v0.4.1-candidate, role evaluator) — ALL live gold ×1 + 5 stability cases ×2
  B  v0.3.0     (snapshot dqe-v0.3.0,          role evaluator) — the 13-case diagnostic subset ×1
  C  no-skill   (snapshot none,                role baseline)  — the SAME 13-case subset ×1

Runs are DIRECT on the manifest `document` (not blinded): §6.1 requires the checker target to match the
manifest document, and each evaluator prompt carries a path-neutrality instruction (the filename is not
evidence). total slots = N + 36 (with N live gold cases).

Output: tests/corpus/blind-runs/<run-id>/phase-e-plan.json = {"meta": {...}, "runs": [ {entry}, ... ]}.

Usage: python scripts/make_phase_e_plan.py [--run-id phase-e-2026-08-05] [--date 2026-08-05]
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"

# hard caps — MUST match validate_eval_plan.py (§4.4)
MAX_EVAL_RUNS = 64
MAX_RUN_IDX = 3

# arm -> (slug, snapshot, role). "no-skill" has no snapshot bundle (baseline prompt).
ARMS = {
    "v0.4.1":  ("v041",   "dqe-v0.4.1-candidate", "evaluator"),
    "v0.3.0":  ("v03",    "dqe-v0.3.0",           "evaluator"),
    "no-skill": ("noskill", None,                 "baseline"),
}

# §5.1 stability cases (candidate arm runs each of these 3×: covers profile-aware HF-9, D-16 audit ALLOW,
# controlled reproducibility BLOCK, HF-15, a clean controlled positive).
STABILITY = ["BP-004-external", "BP-006-audit", "BP-006-release", "GN-ROADMAP-001", "GP-PROP-CONTROLLED-001"]

# §5.2/5.3 the fixed 13-case diagnostic subset. This is the 2026-08-02 diagnostic set with the now-quarantined
# GN-EXP-REPRO-001 replaced by its OQ-REPRO=A successor BP-006-audit (external+audit reproducibility).
DIAG_SUBSET = [
    "BP-002-audit", "BP-002-fail", "BP-002-pass", "BP-004-controlled", "BP-004-external",
    "BP-005-fail", "BP-005-pass", "GN-EVIDENCE-BARE-CLAIM-001", "GN-PROP-VALIDATION-001",
    "GN-ROADMAP-001", "GP-EXP-001", "GP-PROP-CONTROLLED-001", "BP-006-audit",
]


def load_live():
    by_id = {}
    for mp in CASES.glob("**/manifest.yaml"):
        if "quarantine" in mp.parts:
            continue
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        by_id[m["case_id"]] = (m, mp)
    return by_id


def entry(arm, case_id, run_idx, m):
    slug, snapshot, role = ARMS[arm]
    prof = (m.get("profile", {}) or {})
    return {
        "run_key": f"{slug}__{case_id}__{run_idx}",
        "arm": arm,
        "case_id": case_id,
        "run_idx": run_idx,
        "snapshot": snapshot,
        "role": role,
        "input_path": m["document"],
        "artifact_type": prof.get("artifact_type") or m.get("artifact_type") or "",
        "provenance_policy": prof.get("provenance_policy", ""),
        "decision_mode": prof.get("decision_mode", ""),
        "max_turns": 24,
    }


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    run_id = argv[argv.index("--run-id") + 1] if "--run-id" in argv else "phase-e-2026-08-05"
    created_at = argv[argv.index("--date") + 1] if "--date" in argv else "2026-08-05"
    live = load_live()
    all_cases = sorted(live)
    N = len(all_cases)

    # sanity: subset + stability cases must all be live
    missing = [c for c in DIAG_SUBSET + STABILITY if c not in live]
    if missing:
        print(f"ERROR: subset/stability cases not live: {missing}", file=sys.stderr)
        return 2

    runs = []
    # Arm A — candidate: every live gold ×1, plus stability cases ×2 more (run_idx 2,3)
    for c in all_cases:
        runs.append(entry("v0.4.1", c, 1, live[c][0]))
    for c in STABILITY:
        for idx in (2, 3):
            runs.append(entry("v0.4.1", c, idx, live[c][0]))
    # Arm B — frozen v0.3 on the 13-case subset ×1
    for c in DIAG_SUBSET:
        runs.append(entry("v0.3.0", c, 1, live[c][0]))
    # Arm C — no-skill baseline on the same subset ×1
    for c in DIAG_SUBSET:
        runs.append(entry("no-skill", c, 1, live[c][0]))

    arm_counts = {a: sum(1 for r in runs if r["arm"] == a) for a in ARMS}
    total = len(runs)

    meta = {
        "run_id": run_id, "created_at": created_at,
        "candidate_arm": "v0.4.1",
        "N_live_gold": N,
        "arm_counts": arm_counts,
        "total_slots": total,
        "diag_subset": DIAG_SUBSET, "stability_cases": STABILITY,
        "caps": {"MAX_EVAL_RUNS": MAX_EVAL_RUNS, "MAX_CONCURRENCY": 2, "MAX_BATCH_SIZE": 4,
                 "MAX_RUN_IDX": MAX_RUN_IDX, "MAX_NESTING_DEPTH": 1, "MAX_RETRIES_PER_SLOT": 1,
                 "MAX_TURNS_PER_EVALUATOR": 24},
        "token_budget": {"per_slot_est": 92000, "expected_total": total * 92000,
                         "hard_ceiling": 7000000, "stop_at_fraction": 0.8},
        "execution": "bounded direct Agent batches of MAX_BATCH_SIZE; NO background Workflow; NO dynamic expansion",
    }

    out_dir = ROOT / "tests" / "corpus" / "blind-runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = out_dir / "phase-e-plan.json"
    plan_path.write_text(json.dumps({"meta": meta, "runs": runs}, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- print the exact scale (must be human-confirmed before launch, §5.4) ----
    print(f"# Phase E static plan -> {plan_path.relative_to(ROOT).as_posix()}")
    print(f"  N (live gold cases)      = {N}")
    print(f"  Arm A  v0.4.1 candidate  = {arm_counts['v0.4.1']}  ({N} live ×1 + {len(STABILITY)} stability ×2)")
    print(f"  Arm B  frozen v0.3.0     = {arm_counts['v0.3.0']}  (13-case diagnostic subset ×1)")
    print(f"  Arm C  no-skill baseline = {arm_counts['no-skill']}  (same 13-case subset ×1)")
    print(f"  TOTAL SLOTS              = {total}   (cap MAX_EVAL_RUNS={MAX_EVAL_RUNS})")
    exp_m = meta["token_budget"]["expected_total"] / 1e6
    print(f"  token budget: expected ≈ {exp_m:.1f}M  (per-slot ~92k)  |  hard ceiling = 7.0M  |  stop at 80%")
    if total > MAX_EVAL_RUNS:
        print(f"  ❌ total {total} EXCEEDS MAX_EVAL_RUNS {MAX_EVAL_RUNS} — trim the plan (do NOT relax the cap).")
        return 1
    print(f"  ✅ within cap. Next: validate_eval_plan.py then 2-slot canary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
