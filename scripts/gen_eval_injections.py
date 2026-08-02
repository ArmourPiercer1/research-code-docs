#!/usr/bin/env python3
"""
gen_eval_injections.py — generate v0.4 evaluator injection prompts for a set of live cases.

For each case_id it locates the manifest under tests/corpus/cases/**, reads artifact_type + profile
(provenance_policy / decision_mode), and shells out to make_grading_injection.py --role evaluator with
that profile, writing <out-dir>/<case_id>.txt. The evaluator therefore receives the caller-supplied
profile (ADR-DQE-001 B1) — no silent inference.

Usage:
  python scripts/gen_eval_injections.py <out-dir> <case_id> [<case_id> ...]
  python scripts/gen_eval_injections.py <out-dir> --all-live          # every non-quarantine live case
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
MGI = ROOT / "evals" / "skills" / "harness" / "make_grading_injection.py"
PY = sys.executable


def manifests():
    return {yaml.safe_load(mp.read_text(encoding="utf-8"))["case_id"]: mp
            for mp in CASES.glob("**/manifest.yaml") if "quarantine" not in mp.parts}


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    if len(argv) < 3:
        print(__doc__); return 2
    out = ROOT / argv[1]; out.mkdir(parents=True, exist_ok=True)
    by_id = manifests()
    picks = sorted(by_id) if "--all-live" in argv[2:] else argv[2:]
    n = 0
    for cid in picks:
        mp = by_id.get(cid)
        if not mp:
            print(f"  [skip] {cid}: no live manifest"); continue
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        prof = m.get("profile", {}) or {}
        at = prof.get("artifact_type") or m.get("artifact_type") or ""
        pp, dm = prof.get("provenance_policy", ""), prof.get("decision_mode", "")
        doc = ROOT / m["document"]
        profile_str = f"provenance_policy: {pp}, decision_mode: {dm}"
        cmd = [PY, str(MGI), "documentation-quality-evaluator", str(doc),
               "--role", "evaluator", "--artifact-type", at, "--profile", profile_str]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            print(f"  [FAIL] {cid}: {res.stderr[:200]}"); continue
        (out / f"{cid}.txt").write_text(res.stdout, encoding="utf-8")
        n += 1
        print(f"  {cid}: profile=({pp}/{dm}) type={at} -> {out.name}/{cid}.txt")
    print(f"\n==> generated {n} evaluator injection(s) under {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
