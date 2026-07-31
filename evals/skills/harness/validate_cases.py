#!/usr/bin/env python3
"""
validate_cases.py — parse every evals/skills/**/*.yaml case file, check schema basics,
and print per-file counts. Verifies each trigger file meets the deliverable-C minimums
(>=10 should-trigger, >=10 should-not) and each conflict/multi-turn/task file its minimums.

Usage: python validate_cases.py [<evals/skills dir>]
"""
from __future__ import annotations
import sys
from collections import Counter
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]  # evals/skills/


def main(argv: list[str]) -> int:
    base = Path(argv[1]) if len(argv) > 1 else ROOT
    problems: list[str] = []
    total = 0
    for f in sorted(base.rglob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or "cases" not in d:
            problems.append(f"{f}: not a case file (no 'cases')")
            continue
        cases = d["cases"]
        total += len(cases)
        kind = f.parent.name
        ids = [c.get("id") for c in cases]
        if len(ids) != len(set(ids)):
            problems.append(f"{f}: duplicate case ids")
        if kind == "trigger":
            c = Counter(x.get("set") for x in cases)
            print(f"[trigger ] {f.stem:38s} should-trigger={c.get('should-trigger',0)} "
                  f"should-not={c.get('should-not',0)} short-ambiguous={c.get('short-ambiguous',0)}")
            if c.get("should-trigger", 0) < 10:
                problems.append(f"{f}: <10 should-trigger")
            if c.get("should-not", 0) < 10:
                problems.append(f"{f}: <10 should-not")
        else:
            print(f"[{kind:8s}] {f.stem:38s} cases={len(cases)}")
            mins = {"conflict": 5, "multi-turn": 3, "task-quality": 2}
            if kind in mins and len(cases) < mins[kind]:
                problems.append(f"{f}: <{mins[kind]} cases for {kind}")
    print(f"\nTOTAL cases: {total}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("all case files OK (schema + deliverable-C minimums)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
