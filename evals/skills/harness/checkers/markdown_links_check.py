#!/usr/bin/env python3
"""
markdown_links_check.py — relative link / file-path validity.

Checks that relative markdown links [text](path) and reference-style paths point to
files that actually exist. Skips external (http/https/mailto), in-page anchors (#...),
and template placeholders (<...>). Anchors after a path ('file.md#section') are stripped
before the existence check.

Banner-aware extension (Phase-2 slice, prompt §9 "required banner-aware extension" +
§5.2 rule 4 "active status pointers must not keep treating the archived plan as current
authority"): a link from a LIVE document to a file under docs/plans/archived/ (or to a
file carrying a VOID/SUPERSEDED banner) must be labeled on its own line as
historical/frozen/archived/superseded. Frozen sources (docs/plans/archived/, the
external-review mirror, evals/skills/results/, tests/corpus/, references/) are exempt —
their links are historical evidence, not live pointers.

Usage: python markdown_links_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "tel:", "data:")
ARCHIVED = ("docs", "plans", "archived")
# frozen source areas: links from these are historical evidence, not live pointers
FROZEN_SOURCE_PREFIXES = (
    ("docs", "plans", "archived"),
    ("docs", "reconstruction-external-review"),
    ("evals", "skills", "results"),
    ("tests", "corpus"),
    ("references",),
)
HIST_LABEL = re.compile(r"(frozen|historical|void|archived|superseded)", re.IGNORECASE)
ROOT = Path(__file__).resolve().parents[4]


def _repo_rel(path: Path):
    try:
        return path.resolve().relative_to(ROOT).parts
    except ValueError:
        return None


def _has_void_banner(path: Path) -> bool:
    try:
        import archive_lint
        return bool(archive_lint.banner_line_indices(path.read_text(encoding="utf-8", errors="replace").splitlines()))
    except Exception:
        return False


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    base = path.parent
    problems: list[str] = []
    src_parts = _repo_rel(path)
    frozen_source = any(src_parts and src_parts[:len(pfx)] == pfx for pfx in FROZEN_SOURCE_PREFIXES)
    for line in text.splitlines():
        for m in LINK.finditer(line):
            target = m.group(1).strip()
            if not target or target.startswith(SKIP_PREFIX):
                continue
            if target.startswith("<") and target.endswith(">"):
                continue  # template placeholder
            # strip anchor and query
            clean = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            if clean.startswith("/"):
                # workspace-absolute: resolve from the repo root (two levels up from harness use is unknown;
                # treat leading '/' as relative to the file's drive is unreliable) -> just skip with a note
                candidate = Path(clean)
            else:
                candidate = (base / clean)
            try:
                exists = candidate.exists()
            except OSError:
                exists = False
            if not exists:
                problems.append(f"broken link: ({target}) -> {candidate}")
                continue
            # banner-aware rule (Phase-2 §9): live doc → archived/VOID target must be labeled
            if not frozen_source:
                tparts = _repo_rel(candidate)
                archived_target = bool(tparts and (tparts[:3] == ARCHIVED or _has_void_banner(candidate)))
                if archived_target:
                    # label must appear OUTSIDE the link target itself (the path may say 'archived')
                    line_wo_target = line.replace(m.group(1), "")
                    if not HIST_LABEL.search(line_wo_target):
                        problems.append(f"archive-pointer: link to archived/VOID doc ({target}) from a live "
                                        f"document must be labeled historical/frozen/archived on its line "
                                        f"(banner-aware rule)")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: markdown_links_check.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        print(f"[{'PASS' if ok else 'FAIL'}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
