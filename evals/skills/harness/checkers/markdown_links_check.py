#!/usr/bin/env python3
"""
markdown_links_check.py — relative link / file-path validity.

Checks that relative markdown links [text](path) and reference-style paths point to
files that actually exist. Skips external (http/https/mailto), in-page anchors (#...),
and template placeholders (<...>). Anchors after a path ('file.md#section') are stripped
before the existence check.

Usage: python markdown_links_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "tel:", "data:")


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    base = path.parent
    problems: list[str] = []
    for m in LINK.finditer(text):
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
