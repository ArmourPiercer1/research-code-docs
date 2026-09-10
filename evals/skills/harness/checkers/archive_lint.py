#!/usr/bin/env python3
"""archive_lint.py — Phase-2 (revised slice §5; invariants I11/I12): archive discipline.

Rules (prompt §5.2, 2026-09-10 Phase-2 implementation prompt):
  R1: a doc that carries a VOID/SUPERSEDED banner must live under
      docs/plans/archived/ (or the banner + pointers removed). The frozen external
      review mirror (docs/reconstruction-external-review/) is exempt — it is a
      frozen snapshot, not a live plan.
  R2: a VOID/SUPERSEDED-bannned doc under docs/plans/archived/ must KEEP its
      supersession metadata: a dated banner AND a replacement pointer (a link or
      backticked path within 12 lines of the banner).
  R3 (repo mode only): every file under docs/plans/archived/ must be tracked in git
      (the archive is not version-controlled if git does not know it).

A "VOID banner" is either:
  * a blockquote line (starts with '>') matching VOID / SUPERSEDED (date), or
  * a comment/metadata line `status: SUPERSEDED` (the creation-roadmap meta style).

Usage:
    python archive_lint.py <file.md> [...]          # per-file (run_checks check_file)
    python archive_lint.py --repo [root]            # repo mode: scan + R3 git check
Exit code 0 if all pass, 1 otherwise.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ARCHIVED = ("docs", "plans", "archived")
MIRROR = ("docs", "reconstruction-external-review")

BANNER_BLOCKQUOTE = re.compile(r">.*VOID\s*/\s*SUPERSEDED\s*\(\d{4}-\d{2}-\d{2}\)")
BANNER_STATUS_LINE = re.compile(r"^\s*status\s*:\s*SUPERSEDED\b")
REPLACEMENT_REF = re.compile(r"\[[^\]]+\]\([^)]+\)|`[^`]+\.md`|`docs/[^`]+`")


def _rel_parts(path: Path) -> tuple[str, ...]:
    try:
        return path.resolve().relative_to(ROOT).parts
    except ValueError:
        return tuple(path.parts)


def banner_line_indices(lines: list[str]) -> list[int]:
    return [i for i, l in enumerate(lines) if BANNER_BLOCKQUOTE.search(l) or BANNER_STATUS_LINE.match(l)]


def check_file(path: Path) -> tuple[bool, list[str]]:
    """run_checks interface. Returns (ok, problems)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    idxs = banner_line_indices(lines)
    if not idxs:
        return True, []
    parts = _rel_parts(path)
    rel = Path(*parts).as_posix() if parts else str(path)
    problems: list[str] = []
    in_archived = parts[:3] == ARCHIVED
    in_mirror = parts[:2] == MIRROR
    for i in idxs:
        if in_archived:
            # R2: banner must keep date + a replacement pointer nearby.
            has_date = any(BANNER_BLOCKQUOTE.search(lines[j]) or re.search(r"\(\d{4}-\d{2}-\d{2}\)", lines[j])
                           for j in range(i, min(i + 4, len(lines))))
            if not has_date:
                problems.append(f"archive-lint R2: banner at L{i+1} lost its date (supersession metadata must be kept)")
            window = lines[i:min(i + 13, len(lines))]
            if not any(REPLACEMENT_REF.search(l) for l in window):
                problems.append(f"archive-lint R2: banner at L{i+1} has no replacement pointer "
                                "(link or backticked path within 12 lines)")
        elif in_mirror:
            continue  # frozen snapshot: exempt
        else:
            if not any("R1" in p and f"docs/plans/archived/" in p for p in problems):
                problems.append(f"archive-lint R1: VOID/SUPERSEDED doc {rel} lives outside "
                                f"docs/plans/archived/ (L{i+1}) — archive it (banner + move) or remove the banner")
    return (len(problems) == 0), problems


def _tracked(root: Path, p: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", p.as_posix()],
            capture_output=True, text=True, timeout=60)
        return bool(out.stdout.strip())
    except Exception:
        return False


def check_repo(root: Path = ROOT) -> tuple[bool, list[str]]:
    problems: list[str] = []
    for f in sorted(root.rglob("*.md")):
        if ".venv" in f.parts or "node_modules" in f.parts or "fixtures" in f.parts:
            continue
        ok, probs = check_file(f)
        problems.extend(probs)
    # R3: archive destination must be tracked
    arch = root / "docs" / "plans" / "archived"
    if arch.is_dir():
        for f in sorted(arch.rglob("*")):
            if f.is_file() and f.suffix in (".md", ".yaml", ".yml"):
                if not _tracked(root, f):
                    problems.append(f"archive-lint R3: {f.relative_to(root).as_posix()} is in "
                                    f"docs/plans/archived/ but NOT tracked in git (the archive must be version-controlled)")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--repo":
        root = Path(argv[2]) if len(argv) > 2 else ROOT
        ok, problems = check_repo(root)
        print(f"archive_lint --repo {root}: {'PASS' if ok else 'FAIL'}")
        for p in problems:
            print(f"    - {p}")
        return 0 if ok else 1
    if len(argv) < 2:
        print("usage: archive_lint.py <file.md> [...] | --repo [root]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        ok, problems = check_file(Path(arg))
        print(f"[{'PASS' if ok else 'FAIL'}] {arg}")
        for p in problems:
            print(f"    - {p}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
