#!/usr/bin/env python3
"""supersession_lint.py — Phase-2 (revised slice §5; invariants I5): supersession lineage.

Rules (prompt §5.3, 2026-09-10 Phase-2 implementation prompt):
  S1: every `supersedes:` / `superseded_by:` reference that names a PATH (contains '/',
      ends in .md, or is a bare file name) must resolve to an existing file
      (repo-root-relative, file-dir-relative, or — for a bare name — anywhere in the repo).
  S2: every `supersedes:` / `superseded_by:` reference that names an ID (e.g. D-001)
      must be defined in the same file as `id: <ID>`.
  S3: self-supersession (target resolves to the file itself) is a problem.
  S4: a file under docs/plans/archived/ that is pointed at by a supersession reference
      must still carry a VOID/SUPERSEDED banner (lineage must survive an archive move).
  S5: a `superseded_by:` reference requires a non-empty `reason:` within the next 12
      lines (a superseded/contradicted decision keeps its lineage annotation).

Applies to .md files only; a file without any supersedes/superseded_by key passes
vacuously.

Usage:
    python supersession_lint.py <file.md> [...]
    python supersession_lint.py --repo        # scan all .md under the repo root
Exit code 0 if all pass, 1 otherwise.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SUP_LINE = re.compile(r"^\s*(supersedes|superseded_by)\s*:\s*(.*?)\s*$")
ID_DEF = re.compile(r"^\s*-?\s*id\s*:\s*(\S+)\s*$")
ARCHIVED = ("docs", "plans", "archived")

# imported lazily to avoid a hard dependency when used per-file
def _has_void_banner(path: Path) -> bool:
    try:
        import archive_lint
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return bool(archive_lint.banner_line_indices(lines))
    except Exception:
        return False


def _strip_qualifier(target: str) -> str:
    """'target-capability-architecture.md §7' -> 'target-capability-architecture.md';
    'docs/x/y.md#anchor' -> 'docs/x/y.md'."""
    t = target.strip()
    t = re.split(r"\s+", t, maxsplit=1)[0]          # drop ' §7' style qualifiers
    t = t.split("#", 1)[0]                          # drop anchors
    return t


def _is_pathlike(tok: str) -> bool:
    return ("/" in tok) or tok.endswith(".md") or tok.endswith(".yaml") or tok.endswith(".yml")


def check_file(path: Path) -> tuple[bool, list[str]]:
    path = path.resolve()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    problems: list[str] = []
    own_ids = {m.group(1) for m in (ID_DEF.match(l) for l in lines) if m}
    try:
        own_parts = path.relative_to(ROOT).parts
    except ValueError:
        own_parts = tuple(path.parts)

    for i, line in enumerate(lines):
        m = SUP_LINE.match(line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2)
        if not raw or raw in ("null", "~", "-", '""', "''") or raw.startswith("#"):
            continue
        tok = _strip_qualifier(raw)
        if not tok:
            continue
        if _is_pathlike(tok):
            candidates = [ROOT / tok, path.parent / tok]
            resolved = next((c for c in candidates if c.exists()), None)
            if resolved is None and "/" not in tok:
                # bare file name: search the repo (bounded, ignore .venv/node_modules)
                hits = [p for p in ROOT.rglob(tok)
                        if ".venv" not in p.parts and "node_modules" not in p.parts and p.is_file()]
                resolved = hits[0] if hits else None
            if resolved is None:
                problems.append(f"supersession-lint S1: {key} target not found: {tok!r} (L{i+1})")
                continue
            rp = resolved.resolve()
            if rp == path:
                problems.append(f"supersession-lint S3: self-supersession via {tok!r} (L{i+1})")
            try:
                rparts = rp.relative_to(ROOT).parts
            except ValueError:
                rparts = tuple()
            if rparts[:3] == ARCHIVED and not _has_void_banner(rp):
                problems.append(f"supersession-lint S4: {key} target {tok!r} (L{i+1}) is in "
                                f"docs/plans/archived/ but carries no VOID/SUPERSEDED banner — lineage not preserved")
            if rparts[:3] != ARCHIVED and _has_void_banner(rp):
                problems.append(f"supersession-lint S4: {key} target {tok!r} (L{i+1}) is a VOID/SUPERSEDED doc "
                                f"outside docs/plans/archived/")
        else:
            # ID reference: must be defined in this file
            if tok not in own_ids:
                problems.append(f"supersession-lint S2: {key} ID {tok!r} (L{i+1}) is not defined as "
                                f"'id: {tok}' in this file")
        if key == "superseded_by":
            window = lines[i + 1:i + 13]
            if not any(re.match(r"^\s*reason\s*:\s*\S", l) for l in window):
                problems.append(f"supersession-lint S5: superseded_by at L{i+1} has no non-empty "
                                f"'reason:' within the next 12 lines")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if not argv[1:]:
        print("usage: supersession_lint.py <file.md> [...] | --repo", file=sys.stderr)
        return 2
    if argv[1] == "--repo":
        files = sorted(p for p in ROOT.rglob("*.md")
                       if ".venv" not in p.parts and "node_modules" not in p.parts)
        print(f"supersession_lint --repo {ROOT}: scanning {len(files)} .md files")
    else:
        files = [Path(a) for a in argv[1:]]
    ok_all = True
    for arg in files:
        ok, problems = check_file(arg)
        if not ok:
            print(f"[FAIL] {arg}")
            for p in problems:
                print(f"    - {p}")
            ok_all = False
    if argv[1:] == ["--repo"]:
        print(f"supersession_lint --repo: {'PASS' if ok_all else 'FAIL'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
