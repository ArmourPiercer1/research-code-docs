#!/usr/bin/env python3
"""
validate_eval_plan.py — the hard gate that runs BEFORE any Phase E agent starts
(DQE_D3决策与PhaseE安全准入计划 §4.3/§4.4). Any failure => ABORT_BEFORE_AGENT_CALL (exit 2).

This is the structural defense against the 63M-token runaway: it proves the task set is a finite, unique,
capped list of objects — NOT a string that something will iterate character-by-character, and NOT larger
than MAX_EVAL_RUNS. It also hash-verifies each frozen snapshot bundle so an arm cannot silently drift.

Checks:
  - the plan's `runs` is a JSON array (NOT a string); every element is an object (NOT a char/string)
  - run_key globally unique
  - arm is known; arm ↔ snapshot ↔ role are consistent with the frozen ARMS mapping
  - case_id is a LIVE GOLD case (present, not quarantine/disputed/candidate/queued)
  - snapshot dir exists and every file hash matches its SNAPSHOT-MANIFEST.yaml (evaluator arms);
    baseline arm must have snapshot=null
  - run_idx in 1..MAX_RUN_IDX; per (case,arm) count <= MAX_RUN_IDX
  - input_path exists and equals the case's manifest document
  - total runs <= MAX_EVAL_RUNS

Usage: python scripts/validate_eval_plan.py tests/corpus/blind-runs/<run-id>/phase-e-plan.json
"""
from __future__ import annotations
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
SNAP = ROOT / "evals" / "skills" / "snapshots"

# hard caps — MUST match make_phase_e_plan.py (§4.4)
MAX_EVAL_RUNS = 64
MAX_RUN_IDX = 3
ARMS = {
    "v0.4.1":  ("dqe-v0.4.1-candidate", "evaluator"),
    "v0.3.0":  ("dqe-v0.3.0",           "evaluator"),
    "no-skill": (None,                  "baseline"),
}
BAD_STATUS = {"quarantine", "disputed", "candidate", "queued"}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_live_manifests():
    by_id = {}
    for mp in CASES.glob("**/manifest.yaml"):
        if "quarantine" in mp.parts:
            continue
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        by_id[m["case_id"]] = m
    return by_id


def verify_snapshot(name: str) -> list[str]:
    """Re-hash every file in the snapshot against its SNAPSHOT-MANIFEST.yaml. Returns error strings."""
    errs = []
    sd = SNAP / name
    manp = sd / "SNAPSHOT-MANIFEST.yaml"
    if not manp.is_file():
        return [f"snapshot {name}: missing SNAPSHOT-MANIFEST.yaml"]
    man = yaml.safe_load(manp.read_text(encoding="utf-8"))
    for f in (man.get("files") or []):
        fp = sd / f["path"]
        if not fp.is_file():
            errs.append(f"snapshot {name}: file missing {f['path']}"); continue
        actual = sha256_file(fp)
        if actual != f["sha256"]:
            errs.append(f"snapshot {name}: HASH MISMATCH {f['path']} (bundle tampered)")
    return errs


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: validate_eval_plan.py <phase-e-plan.json>", file=sys.stderr)
        return 2
    plan_path = Path(args[0])
    if not plan_path.is_file():
        print(f"ABORT_BEFORE_AGENT_CALL: plan not found: {plan_path}", file=sys.stderr)
        return 2

    raw = plan_path.read_text(encoding="utf-8")
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ABORT_BEFORE_AGENT_CALL: plan is not valid JSON: {e}", file=sys.stderr)
        return 2

    errs: list[str] = []

    # ---- CRITICAL anti-runaway shape checks ----
    if isinstance(plan, str):
        print("ABORT_BEFORE_AGENT_CALL: plan is a JSON STRING, not an object/array "
              "(this is the 63M-token runaway signature).", file=sys.stderr)
        return 2
    runs = plan.get("runs") if isinstance(plan, dict) else plan
    if isinstance(runs, str):
        errs.append("`runs` is a STRING, not an array — a char-iterating runner would spawn one agent per "
                    "character. HARD ABORT.")
        runs = []
    elif not isinstance(runs, list):
        errs.append(f"`runs` must be a JSON array; got {type(runs).__name__}")
        runs = []
    for i, r in enumerate(runs):
        if not isinstance(r, dict):
            errs.append(f"runs[{i}] is {type(r).__name__}, not an object")

    runs = [r for r in runs if isinstance(r, dict)]
    live = load_live_manifests()

    # ---- total-count cap (§4.4) ----
    if len(runs) > MAX_EVAL_RUNS:
        errs.append(f"total runs {len(runs)} > MAX_EVAL_RUNS {MAX_EVAL_RUNS} — trim the plan; do NOT relax the cap")

    # ---- run_key uniqueness ----
    keys = [r.get("run_key") for r in runs]
    for k, c in Counter(keys).items():
        if c > 1:
            errs.append(f"duplicate run_key '{k}' ×{c}")
    if any(not k for k in keys):
        errs.append("some runs have no run_key")

    # ---- per-(case,arm) count cap ----
    ca = Counter((r.get("arm"), r.get("case_id")) for r in runs)
    for (arm, cid), c in ca.items():
        if c > MAX_RUN_IDX:
            errs.append(f"({arm},{cid}) appears {c}× > MAX_RUN_IDX {MAX_RUN_IDX}")

    # ---- verify snapshots once (each referenced snapshot) ----
    snaps_seen = {r.get("snapshot") for r in runs if r.get("snapshot")}
    for s in sorted(snaps_seen):
        errs += verify_snapshot(s)

    # ---- per-run checks ----
    for r in runs:
        rk = r.get("run_key", "?")
        arm = r.get("arm")
        if arm not in ARMS:
            errs.append(f"{rk}: unknown arm {arm!r}"); continue
        exp_snap, exp_role = ARMS[arm]
        if r.get("snapshot") != exp_snap:
            errs.append(f"{rk}: arm {arm} expects snapshot {exp_snap!r}, got {r.get('snapshot')!r}")
        if r.get("role") != exp_role:
            errs.append(f"{rk}: arm {arm} expects role {exp_role!r}, got {r.get('role')!r}")
        ri = r.get("run_idx")
        if not isinstance(ri, int) or not (1 <= ri <= MAX_RUN_IDX):
            errs.append(f"{rk}: run_idx {ri!r} out of 1..{MAX_RUN_IDX}")
        cid = r.get("case_id")
        m = live.get(cid)
        if not m:
            errs.append(f"{rk}: case_id {cid!r} is not a LIVE case (quarantine/unknown)"); continue
        status = ((m.get("adjudication") or {}).get("status") or "gold")
        if status in BAD_STATUS:
            errs.append(f"{rk}: case {cid} adjudication.status={status} (not gold)")
        ip = r.get("input_path")
        if not ip or not (ROOT / ip).is_file():
            errs.append(f"{rk}: input_path missing on disk: {ip!r}")
        elif ip != m.get("document"):
            errs.append(f"{rk}: input_path {ip!r} != manifest document {m.get('document')!r} "
                        "(checker-target metric would misfire)")

    if errs:
        print(f"ABORT_BEFORE_AGENT_CALL — {len(errs)} error(s):", file=sys.stderr)
        for e in errs:
            print(f"  ✗ {e}", file=sys.stderr)
        return 2

    arm_counts = Counter(r["arm"] for r in runs)
    print(f"# plan OK: {len(runs)} runs, {len(set(keys))} unique run_keys, cap {MAX_EVAL_RUNS}")
    for a in ARMS:
        print(f"  {a:9s}: {arm_counts.get(a,0)} runs  (snapshot={ARMS[a][0]}, role={ARMS[a][1]})")
    print(f"  snapshots hash-verified: {sorted(snaps_seen)}")
    print("  ✅ VALIDATED — safe to run bounded direct batches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
