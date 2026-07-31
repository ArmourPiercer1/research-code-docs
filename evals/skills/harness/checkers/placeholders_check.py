#!/usr/bin/env python3
"""
placeholders_check.py — banned placeholders / unfilled stubs.

Flags leftover authoring placeholders that must never survive into a delivered
document: TODO/TBD/FIXME/XXX, 'lorem ipsum', bare 'PLACEHOLDER', unfilled angle-bracket
stubs like <fill this in>, and empty required sections (a heading immediately followed
by another heading or EOF).

Deliberately does NOT flag: '...' inside code/quotes, or angle-bracket tokens that are
clearly schema placeholders inside fenced code blocks (skills legitimately show
'<skill-name>' in code examples).

Usage: python placeholders_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

BANNED = [
    (re.compile(r"\bTODO\b"), "TODO"),
    (re.compile(r"\bTBD\b"), "TBD"),
    (re.compile(r"\bFIXME\b"), "FIXME"),
    (re.compile(r"\bXXX\b"), "XXX"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "lorem ipsum"),
    (re.compile(r"\bPLACEHOLDER\b"), "PLACEHOLDER"),
    (re.compile(r"\bWRITE ME\b", re.IGNORECASE), "write me"),
    (re.compile(r"<fill[^>]*>", re.IGNORECASE), "<fill...>"),
]


def mask_code_fences(text: str) -> str:
    """Replace fenced code blocks with a sentinel content line (preserving line count) so
    that (a) '#' comments inside code aren't parsed as headings, and (b) a section whose
    body is only a code block is NOT seen as empty."""
    def repl(m: re.Match) -> str:
        nl = m.group(0).count("\n")
        return "CODEBLOCK" + ("\n" * nl)
    return re.sub(r"```.*?```", repl, text, flags=re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so schema placeholders inside examples aren't flagged."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def find_empty_sections(text: str) -> list[str]:
    lines = text.splitlines()
    problems = []
    heading_idx = []
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+\S", ln)
        if m:
            heading_idx.append((i, len(m.group(1)), ln))
    for j, (i, level, ln) in enumerate(heading_idx):
        end = heading_idx[j + 1][0] if j + 1 < len(heading_idx) else len(lines)
        body = "\n".join(lines[i + 1:end]).strip()
        if body:
            continue
        # A parent heading immediately followed by a DEEPER subheading is not empty
        # (it introduces subsections). Only flag if the next heading is a peer/ancestor.
        if j + 1 < len(heading_idx):
            next_level = heading_idx[j + 1][1]
            if next_level > level:
                continue
        problems.append(f"empty section: {ln.strip()!r} (line {i+1})")
    return problems


def check_file(path: Path) -> tuple[bool, list[str]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_code_fences(raw)
    problems: list[str] = []
    for pat, label in BANNED:
        n = len(pat.findall(text))
        if n:
            problems.append(f"banned placeholder {label!r} x{n}")
    problems.extend(find_empty_sections(mask_code_fences(raw)))
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: placeholders_check.py <file.md> [...]", file=sys.stderr)
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
