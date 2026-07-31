#!/usr/bin/env python3
"""
_textutils.py — shared helpers for the v0.3 SIGNAL checkers.

The signal checkers extract numbers / keywords from Chinese-and-English markdown. Two hazards
this module defends against (both were real false-positive bugs in earlier checkers):

  1. Phantom numbers/keywords from NON-PROSE regions — fenced code, inline code spans, and the
     URL/target part of markdown links (`](src/eoopt/continuation/chart.py#L39)` would otherwise
     yield "39", `arXiv:2006.07746` -> "2006", `ADR-0011` -> "0011"). `mask_noise` blanks those
     regions to spaces while PRESERVING newlines, so line numbers computed on the masked text still
     match the original file.
  2. `\b` word-boundaries misbehave around CJK (CJK code points are "word" chars). The checkers use
     explicit context keywords / lookarounds instead of relying on \b next to Chinese text.

Nothing here sets a hard-fail; these are advisory signals for the model to adjudicate.
"""
from __future__ import annotations
import re
import sys

# The signal checkers emit CJK + emoji (✅/⚠) candidates. On a Windows GBK console, printing those
# raises UnicodeEncodeError. Reconfigure std streams to UTF-8 on import so every checker that imports
# this module (and run_checks, which aggregates them) is output-safe regardless of console codepage.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # py3.7+
    except Exception:
        pass


def _blank_keep_nl(m: re.Match) -> str:
    """Replace every non-newline char in the match with a space (preserve length + line count)."""
    return re.sub(r"[^\n]", " ", m.group(0))


def mask_noise(text: str) -> str:
    """Blank fenced code, inline code spans, and markdown-link targets. Line-count preserving."""
    text = re.sub(r"```.*?```", _blank_keep_nl, text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", _blank_keep_nl, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", _blank_keep_nl, text)          # inline `code`
    text = re.sub(r"\]\([^)\n]*\)", _blank_keep_nl, text)      # keep [label, blank ](target)
    return text


def line_of(text: str, pos: int) -> int:
    """1-based line number of char offset `pos` in `text`."""
    return text.count("\n", 0, pos) + 1


def context(text: str, pos: int, span: int = 36) -> str:
    """A compact one-line context window around `pos` (newlines/space collapsed)."""
    lo = max(0, pos - span)
    hi = min(len(text), pos + span)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+(\S.*)$")


def split_sections(text: str) -> list[dict]:
    """Split into sections at markdown headings. Each dict: {level, title, start_line, heading_line,
    body}. `body` excludes the heading line. Text before the first heading is a level-0 'preamble'."""
    matches = list(HEADING_RE.finditer(text))
    sections: list[dict] = []
    if not matches or matches[0].start() > 0:
        pre_end = matches[0].start() if matches else len(text)
        pre = text[:pre_end]
        if pre.strip():
            sections.append({"level": 0, "title": "(preamble)", "heading_line": 0,
                             "start_line": 1, "body": pre})
    for i, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append({
            "level": level, "title": title,
            "heading_line": line_of(text, m.start()),
            "start_line": line_of(text, body_start),
            "body": text[body_start:body_end],
        })
    return sections
