#!/usr/bin/env python3
"""
score_all.py — score a skill's combined trigger+conflict results in one report.

Loads evals/skills/trigger/<skill>.yaml AND evals/skills/conflict/<skill>.yaml, matches
against a results JSON (list of {id, decision, route_to}), and prints per-set accuracy plus
the deliverable-C gate (>=9/10 engage on should-trigger, >=9/10 decline/route on should-not,
all conflict cases route correctly).

Usage: python score_all.py <skill-name> <results.json>
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import defaultdict
import yaml

ROOT = Path(__file__).resolve().parents[3]


def load(kind: str, skill: str) -> dict:
    p = ROOT / "evals" / "skills" / kind / f"{skill}.yaml"
    if not p.exists():
        return {}
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    return {c["id"]: c for c in d.get("cases", [])}


def correct(case: dict, res: dict) -> tuple[bool, str]:
    s = case.get("set")
    d = (res.get("decision") or "").strip().lower()
    exp = case.get("expected", {}) or {}
    if s == "should-trigger":
        return (d == "engage"), d
    if s == "should-not":
        ok = d in {"decline", "route"}
        # if the case named a route target, prefer that route (soft: decline also acceptable)
        return ok, d
    if s == "short-ambiguous":
        want = (exp.get("decision") or "").strip().lower()
        if want == "engage":
            return (d == "engage"), d
        if want == "engage-with-clarify":
            return (d == "engage-with-clarify"), d
        if want in ("decline", "route"):
            return (d in {"decline", "route"}), d
        return (d in {"decline", "route", "engage-with-clarify"}), d
    if s == "conflict":
        if d not in {"decline", "route"}:
            return False, d
        want = exp.get("route_to")
        if want:
            got = (res.get("route_to") or "").strip()
            allowed = [str(w).strip() for w in (want if isinstance(want, list) else [want])]
            return (got in allowed), f"{d}->{res.get('route_to')}"
        return True, d
    return False, d


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: score_all.py <skill-name> <results.json>", file=sys.stderr)
        return 2
    skill = argv[1]
    cases = {**load("trigger", skill), **load("conflict", skill)}
    results = {r["id"]: r for r in json.loads(Path(argv[2]).read_text(encoding="utf-8"))}

    by_set: dict[str, list] = defaultdict(list)
    for cid, case in cases.items():
        r = results.get(cid)
        ok, got = (correct(case, r) if r else (False, "MISSING"))
        by_set[case.get("set", "?")].append((cid, ok, got))

    print(f"# score_all: {skill}")
    gate = True
    order = ["should-trigger", "should-not", "short-ambiguous", "conflict"]
    for s in order:
        items = by_set.get(s, [])
        if not items:
            continue
        n = len(items)
        c = sum(1 for _, ok, _ in items if ok)
        print(f"\n[{s}] {c}/{n}")
        for cid, ok, got in items:
            if not ok:
                print(f"    MISS {cid} (got {got})")
        if s in ("should-trigger", "should-not") and c < max(9, n - 1):
            gate = False
        if s == "conflict" and c < n:
            gate = False
    total = sum(len(v) for v in by_set.values())
    correct_n = sum(1 for v in by_set.values() for _, ok, _ in v if ok)
    print(f"\nTOTAL {correct_n}/{total}   GATE(trigger>=9,not>=9,conflict=all) = {'PASS' if gate else 'FAIL'}")
    return 0 if gate else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
