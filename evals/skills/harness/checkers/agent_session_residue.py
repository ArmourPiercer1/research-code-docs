#!/usr/bin/env python3
"""
agent_session_residue.py — SIGNAL (v0.3): conversation/agent leftovers in a FORMAL document.

Feeds HF-13 (session-record role) and HF-8 (needs conversation context). A formal, long-lived doc
should not embed AskUserQuestion transcripts, HANDOVER pointers, "本轮/前文" deixis, or "(用户决定)"
authority parentheticals — those tie the doc to a specific chat.

CRITICAL false-positive guard (design review): do NOT match bare `用户` / `user`. This corpus
legitimately uses 用户自定义 / 用户指定 / 用户挑 / 用户驱动 / 用户给定 as product features. Only
high-precision multiword patterns match, and the authority parenthetical excludes the feature words.

check_file(path) -> (ok, problems). ok=True means "no residue found".
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _textutils import mask_noise, line_of  # noqa: E402

_FEATURE = r"(?!自定义|自行|指定|挑|驱动|给定|可)"   # negative lookahead: product-feature uses of 用户

PATTERNS = [
    ("AskUserQuestion", re.compile(r"AskUserQuestion")),
    ("HANDOVER", re.compile(r"\bHANDOVER\b")),
    ("session-deixis", re.compile(r"本轮|本次对话|前文|如前所述|按此前决定|上文|上一轮")),
    ("user-decision", re.compile(r"用户" + _FEATURE + r"(决定|明确|确认|拍板|要求)")),
    ("authority-paren", re.compile(r"（\s*用户" + _FEATURE + r"[^）\n]{0,10}）")),
    ("agent-research", re.compile(r"(DeepSeek|Explore|Claude|Agent)\s*[+＋]?\s*\w*\s*调研")),
    ("agent-directive", re.compile(r"本 ?Agent|sub-?agent|子代理据|SendMessage")),
]


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = mask_noise(path.read_text(encoding="utf-8", errors="replace"))
    hits: dict[str, list[int]] = {}
    for label, rx in PATTERNS:
        for m in rx.finditer(text):
            hits.setdefault(label, [])
            ln = line_of(text, m.start())
            if ln not in hits[label]:
                hits[label].append(ln)
    problems = [f"{label}: lines {','.join(map(str, sorted(lns)))}"
                for label, lns in hits.items()]
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: agent_session_residue.py <file.md> [...]", file=sys.stderr)
        return 2
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        print(f"[{'OK' if ok else 'SIGNAL'}] {p}")
        for pr in problems:
            print(f"    - {pr}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
