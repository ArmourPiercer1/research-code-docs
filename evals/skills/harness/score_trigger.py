#!/usr/bin/env python3
"""
score_trigger.py — score a filled trigger/conflict results file against expected labels.

Inputs:
  1. a case file (evals/skills/trigger/<skill>.yaml or conflict/<skill>.yaml)
  2. a results file (JSON): a list of {"id": <case-id>, "decision": "engage|decline|route",
     "route_to": <skill|null>, "justification": "..."}
     produced by the sub-agents that ran each case with the injected SKILL.md.

Scoring:
  * should-trigger  -> correct iff decision == "engage"
  * should-not      -> correct iff decision in {"decline","route"}
  * short-ambiguous -> correct iff decision in {"decline","route","engage-with-clarify"}
                       (ambiguous inputs may legitimately ask one routing question)
  * conflict        -> correct iff decision in {"decline","route"} AND route_to matches
                       expected.route_to (when the case specifies one)

Prints a per-set summary + pass/fail vs the targets in quality-control-plan §10
(>=9/10 engage on should-trigger, >=9/10 decline on should-not).

Usage: python score_trigger.py <case.yaml> <results.json>
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import yaml


def load_cases(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {c["id"]: c for c in data.get("cases", [])}


def correct(case: dict, res: dict) -> bool:
    s = case.get("set")
    d = (res.get("decision") or "").strip().lower()
    exp = case.get("expected", {}) or {}
    if s == "should-trigger":
        return d == "engage"
    if s == "should-not":
        return d in {"decline", "route"}
    if s == "short-ambiguous":
        return d in {"decline", "route", "engage-with-clarify"}
    if s == "conflict":
        if d not in {"decline", "route"}:
            return False
        want = exp.get("route_to")
        if want:
            return (res.get("route_to") or "").strip() == str(want).strip()
        return True
    # default: exact decision match if expected.decision given
    want = (exp.get("decision") or "").strip().lower()
    return (d == want) if want else False


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: score_trigger.py <case.yaml> <results.json>", file=sys.stderr)
        return 2
    cases = load_cases(Path(argv[1]))
    results = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in results}

    sets: dict[str, list[tuple[str, bool]]] = {}
    for cid, case in cases.items():
        r = by_id.get(cid)
        ok = correct(case, r) if r else False
        sets.setdefault(case.get("set", "?"), []).append((cid, ok))

    print(f"# trigger score: {argv[1]}")
    overall_ok = True
    for s, items in sorted(sets.items()):
        n = len(items)
        c = sum(1 for _, ok in items if ok)
        print(f"\n[{s}] {c}/{n} correct")
        for cid, ok in items:
            if not ok:
                print(f"    MISS {cid}")
        # gate for the two headline sets
        if s == "should-trigger" and c < max(9, n - 1):
            overall_ok = False
        if s == "should-not" and c < max(9, n - 1):
            overall_ok = False
    print(f"\n==> headline-sets pass = {overall_ok}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
