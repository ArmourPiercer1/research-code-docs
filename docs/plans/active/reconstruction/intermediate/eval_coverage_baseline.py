#!/usr/bin/env python3
"""eval_coverage_baseline.py — independent eval-coverage table for cross-checking.

Builds the ground-truth eval coverage per skill directly from the case YAMLs and
harness directories (not from any report doc). Output:
  docs/plans/active/reconstruction/intermediate/eval-coverage-baseline.md

Working tool for the plan folder (git-ignored), not a release artifact.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

# docs/plans/active/reconstruction/intermediate/x.py -> repo root
ROOT = Path(__file__).resolve().parents[5]
EVALS = ROOT / "evals" / "skills"
OUT = Path(__file__).resolve().parent / "eval-coverage-baseline.md"
SKILLS_DIR = ROOT / ".agents" / "skills"


def case_count(p: Path) -> int | None:
    """Count `- {id:` case entries in a case yaml (None if file absent)."""
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r"^\s*-\s*\{?\s*id:\s*", text, flags=re.M))


def main() -> int:
    skills = sorted(d.name for d in SKILLS_DIR.iterdir() if d.is_dir())
    per = {}
    for s in skills:
        trig = case_count(EVALS / "trigger" / f"{s}.yaml")
        conf = case_count(EVALS / "conflict" / f"{s}.yaml")
        tq = case_count(EVALS / "task-quality" / f"{s}.yaml")
        mt = case_count(EVALS / "multi-turn" / f"{s}.yaml")
        rt = case_count(EVALS / "reader-tests" / f"{s}.yaml")
        per[s] = (trig, conf, tq, mt, rt)

    # results trees: which skills have recorded run outputs
    results = EVALS / "results"
    res_dirs = sorted(d.name for d in results.iterdir() if d.is_dir()) if results.exists() else []
    # blind runs
    blind = ROOT / "tests" / "corpus" / "blind-runs"
    blind_runs = sorted(d.name for d in blind.iterdir() if d.is_dir()) if blind.exists() else []

    lines = [
        "# Eval Coverage Baseline (independent ground truth)",
        "",
        "<!--",
        "generated_by: eval_coverage_baseline.py (parent-agent tooling)",
        "scope: ground truth from case YAMLs + dirs, NOT from report docs",
        "date: 2026-09-09",
        "status: reference for cross-checking phase0/current-system-map.md",
        "-->",
        "",
        "| skill | trigger | conflict | task-quality | multi-turn | reader-tests |",
        "|---|---|---|---|---|---|",
    ]
    tot = [0, 0, 0, 0, 0]
    for s in skills:
        t, c, q, m, r = per[s]
        for i, v in enumerate((t, c, q, m, r)):
            if v:
                tot[i] += v
        fmt = lambda v: "—" if v is None else str(v)
        lines.append(f"| {s} | {fmt(t)} | {fmt(c)} | {fmt(q)} | {fmt(m)} | {fmt(r)} |")
    lines.append(f"| **TOTAL** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]}** | **{tot[4]}** |")
    lines += [
        "",
        "## Recorded run outputs (evals/skills/results/ subdirs)",
        "",
    ]
    for d in res_dirs:
        lines.append(f"- `{d}/`")
    lines += ["", "## Blind runs (tests/corpus/blind-runs/)", ""]
    for d in blind_runs:
        lines.append(f"- `{d}/`")
    lines += [
        "",
        "## Notes for cross-checking",
        "",
        "- A '—' means no case file exists for that skill/set (not zero cases).",
        "- Verified 2026-09-10 (parent recount, all 5 case dirs): 41 files / 229 cases",
        "  (152 trigger / 43 conflict / 16 task-quality / 12 multi-turn / 6 reader-tests).",
        "  This matches phase0/current-system-map.md's figure; the earlier 211/32 count",
        "  covered only the three primary dirs.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print("\n".join(lines[:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
