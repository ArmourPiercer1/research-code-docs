#!/usr/bin/env python3
"""
make_eval_plan.py — turn a blind-run directory into a flat list of evaluator RUNS for the blind matrix.

Reads <run-dir>/.secret/mapping.tsv (blind_id -> case_id) + <run-dir>/params/<blind_id>.yaml
(artifact_type + profile, label-free) and emits <run-dir>/eval-plan.json: one entry per run.

The plan carries case_id (used by the AGGREGATOR to look up expected labels) and the blind input_path +
artifact_type + provenance_policy (the ONLY things fed to the evaluator agent). The runner must NOT put
case_id into the agent prompt — case_id encodes pass/fail.

Run kinds:
  current : every case, run_idx 1 (the admission test)
  repeat  : the --stability cases, run_idx 2..N (stability / 3-run consistency)

Usage:
  python scripts/make_eval_plan.py tests/corpus/blind-runs/<run-id> \
      --stability GN-ROADMAP-001 BP-001-fail GP-PROP-002 --repeats 3
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: make_eval_plan.py <run-dir> [--stability C1 C2 ...] [--repeats N]", file=sys.stderr)
        return 2
    run_dir = (ROOT / args[0]).resolve()
    repeats = int(argv[argv.index("--repeats") + 1]) if "--repeats" in argv else 3
    stability = []
    if "--stability" in argv:
        i = argv.index("--stability") + 1
        while i < len(argv) and not argv[i].startswith("--"):
            stability.append(argv[i]); i += 1

    mapping = {}
    for line in (run_dir / ".secret" / "mapping.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        blind_id, case_id, manifest, pair_id = (line.split("\t") + ["", "", ""])[:4]
        mapping[blind_id] = {"case_id": case_id, "pair_id": pair_id}

    runs = []
    for pf in sorted((run_dir / "params").glob("*.yaml")):
        blind_id = pf.stem
        p = yaml.safe_load(pf.read_text(encoding="utf-8"))
        inp = next((run_dir / "inputs").glob(f"{blind_id}.*"))
        base = {
            "case_id": mapping[blind_id]["case_id"],
            "pair_id": mapping[blind_id]["pair_id"] or None,
            "blind_id": blind_id,
            "input_path": inp.relative_to(ROOT).as_posix(),
            "artifact_type": p.get("artifact_type"),
            "provenance_policy": (p.get("profile") or {}).get("provenance_policy"),
        }
        runs.append({**base, "run_kind": "current", "run_idx": 1})
        if base["case_id"] in stability:
            for k in range(2, repeats + 1):
                runs.append({**base, "run_kind": "repeat", "run_idx": k})

    out = run_dir / "eval-plan.json"
    out.write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")
    n_cur = sum(1 for r in runs if r["run_kind"] == "current")
    n_rep = sum(1 for r in runs if r["run_kind"] == "repeat")
    print(f"# eval-plan -> {out.relative_to(ROOT).as_posix()}")
    print(f"  {len(runs)} runs = {n_cur} current + {n_rep} repeat (stability: {stability}, repeats={repeats})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
