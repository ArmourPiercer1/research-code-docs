#!/usr/bin/env python3
"""check_deliverables.py — Phase 0/1 deliverable verification for the reconstruction.

Usage: python check_deliverables.py
Checks (per deliverable): exists, non-trivial size, header block (generated_by,
date, status), citation density (file:line / commit-hash / path references),
section count. Prints a table; exit 0 = all present & sane, 1 = gaps found.

This is a working tool for the plan folder (docs/plans/ is git-ignored), not a
release artifact.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# docs/plans/active/reconstruction/intermediate/x.py -> repo root
ROOT = Path(__file__).resolve().parents[5]
PLAN = ROOT / "docs" / "plans" / "active" / "reconstruction"

DELIVERABLES = {
    "phase0/current-system-map.md": {"min_chars": 20000, "min_citations": 150},
    "phase0/existing-skill-classification.md": {"min_chars": 10000, "min_citations": 80},
    "phase0/current-information-ownership-map.md": {"min_chars": 12000, "min_citations": 100},
    "phase0/pain-point-evidence.md": {"min_chars": 10000, "min_citations": 80},
    "intermediate/dsh-current-state-findings.md": {"min_chars": 15000, "min_citations": 120},
    "intermediate/dsh-history-findings.md": {"min_chars": 12000, "min_citations": 100},
    "phase1/dsh-workflow-evidence-map.md": {"min_chars": 15000, "min_citations": 150},
    "phase1/dsh-transferability-crosswalk.md": {"min_chars": 8000, "min_citations": 60},
    "phase1/target-workflow-invariants.md": {"min_chars": 10000, "min_citations": 80},
    "phase1/target-capability-architecture.md": {"min_chars": 12000, "min_citations": 80},
    "phase1/canonical-information-model.md": {"min_chars": 8000, "min_citations": 60},
    "phase1/skill-change-matrix.md": {"min_chars": 12000, "min_citations": 80},
    "phase1/eval-plan.md": {"min_chars": 10000, "min_citations": 60},
}

CITATION = re.compile(
    r"[A-Za-z0-9_\-./\\]+\.(?:md|py|yaml|yml|json|txt|toml)(?::\d+)?"   # file paths (optionally :line)
    r"|\b[0-9a-f]{7,40}\b"                                                # commit hashes
    r"|\bgit (?:log|show|blame)\b"
    r"|\b[DMPCAGSH]\d{1,2}[a-z]?(?:-\d+)?"                                # ledger IDs: D1-D19, M1-M32, P1-P10, C1-C15, A1-A10, G1-G6, S1-S14, H1-H6
    r"|\bI(1[0-2]|[1-9])\b"                                              # invariant IDs I1-I12
    r"|\bQ(1[0-7]|[1-9])\b"                                              # charter §17 question IDs
    r"|charter §\d+",
)
HEADER_KEYS = ["generated_by", "date", "status"]


def main() -> int:
    ok = True
    rows = []
    for rel, req in DELIVERABLES.items():
        p = PLAN / rel
        if not p.exists():
            rows.append((rel, "MISSING", 0, 0, 0, 0))
            ok = False
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        head = text[:3000]
        header_ok = all(k in head for k in HEADER_KEYS)
        n_cite = len(CITATION.findall(text))
        n_sec = len(re.findall(r"^#{1,3} ", text, flags=re.M))
        size_ok = len(text) >= req["min_chars"]
        cite_ok = n_cite >= req["min_citations"]
        good = header_ok and size_ok and cite_ok
        ok = ok and good
        rows.append((rel, "OK" if good else "CHECK", len(text), n_cite, n_sec,
                     int(header_ok and size_ok and cite_ok)))
    w = max(len(r[0]) for r in rows)
    print(f"{'deliverable':<{w}}  status   chars     citations  sections  gate")
    for rel, status, size, cite, sec, gate in rows:
        print(f"{rel:<{w}}  {status:<8} {size:<9} {cite:<10} {sec:<10} {gate}")
    print()
    print("VERDICT:", "ALL PRESENT & SANE" if ok else "GAPS FOUND (see CHECK/MISSING rows)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
