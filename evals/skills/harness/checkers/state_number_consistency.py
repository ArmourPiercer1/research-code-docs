#!/usr/bin/env python3
"""
state_number_consistency.py — SIGNAL (v0.3): surface same-kind state values that may contradict.

Feeds HF-14a (state contradiction). This checker NEVER asserts a contradiction and does NO arithmetic
(e.g. it will not reason 59+10=69) — it only lists, per category, the distinct values it found with
their line numbers, so the model can adjudicate. It flags a *candidate* only for categories where two
distinct values almost always mean drift: **test counts** and **progress percentages**. Dates and
version numbers are listed as context but never trip the candidate flag on their own (a roadmap
legitimately carries many distinct dates/versions).

Must catch the eoopt roadmap's `59` (lines 5/131/133/269) vs `69` (line 144) test-count split.

check_file(path) -> (ok, problems). ok=True means "no contradiction candidate".
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _textutils import mask_noise, line_of  # noqa: E402

# Each category: list of regexes with ONE capturing group = the value. Chinese unit keywords make the
# match specific (no bare integers). Numbers inside code/links are already blanked by mask_noise.
CATEGORIES = {
    "test_count": [
        re.compile(r"(\d{1,4})\s*(?:个|项)?\s*测试"),          # "59 测试", "10 项测试"
        re.compile(r"测试\s*(?:数|数量|count)?\s*[:：=]?\s*(\d{1,4})"),  # "测试数 59"
        re.compile(r"(\d{1,4})\s+tests?\b", re.I),
        re.compile(r"\btests?\b[^\d\n]{0,6}(\d{1,4})", re.I),
    ],
    "progress_pct": [
        re.compile(r"(\d{1,3}(?:\.\d+)?)\s*%\s*(?:完成|done|complete)", re.I),
        re.compile(r"(?:完成|进度|done|complete)[^\d\n]{0,4}(\d{1,3}(?:\.\d+)?)\s*%", re.I),
    ],
    "date": [re.compile(r"(\d{4}-\d{2}-\d{2})")],
    "version": [re.compile(r"\bv(\d+\.\d+(?:\.\d+)?)\b")],
}

# categories where >=2 distinct values is a genuine drift candidate
CANDIDATE_CATS = {"test_count", "progress_pct"}


def _collect(text: str) -> dict[str, dict[str, list[int]]]:
    found: dict[str, dict[str, list[int]]] = {}
    for cat, regexes in CATEGORIES.items():
        val_lines: dict[str, list[int]] = {}
        for rx in regexes:
            for m in rx.finditer(text):
                val = m.group(1)
                ln = line_of(text, m.start(1))
                val_lines.setdefault(val, [])
                if ln not in val_lines[val]:
                    val_lines[val].append(ln)
        if val_lines:
            found[cat] = val_lines
    return found


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = mask_noise(path.read_text(encoding="utf-8", errors="replace"))
    found = _collect(text)
    problems: list[str] = []
    for cat in CANDIDATE_CATS:
        vals = found.get(cat, {})
        if len(vals) >= 2:
            rendered = "; ".join(
                f"{v} (lines {','.join(map(str, sorted(lns)))})" for v, lns in sorted(vals.items())
            )
            problems.append(f"candidate {cat} drift — distinct values: {rendered}")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: state_number_consistency.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        print(f"[{'OK' if ok else 'SIGNAL'}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0  # SIGNAL checkers never fail the process


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
