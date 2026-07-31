#!/usr/bin/env python3
"""
completion_open_conflict.py — SIGNAL (v0.3): a section marked complete that still carries open items.

Feeds HF-14b (volatile-state contamination) and HF-15 (vague/deferred acceptance in a committed
phase). Per section, flags when the heading or its status line carries a COMPLETION marker AND the
body carries an OPEN marker. Sections that are *explicitly* open/deferred by their own heading
(开放问题 / Open Questions / 远期 / 后续阶段 …) are skipped — their open markers are legitimate.

On the eoopt roadmap this lights 阶段1 (✅ + AD open item), 阶段2 (✅基础版 + 算例届时定 + α扫另起一期),
阶段3 (首轮完成 + GA 蓝本待补充调研 + 算例届时定) — without firing on §六 开放问题.

check_file(path) -> (ok, problems). ok=True means "no conflict candidate".
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _textutils import mask_noise, split_sections  # noqa: E402

COMPLETE = re.compile(r"✅|已完成|已实现|已验证|已落定|已建|全绿|\bcomplete\b|\bverified\b|\bdone\b", re.I)
OPEN = re.compile(
    r"待定|待调研|待补充|待办|届时定|尚未|未实装|未测|三选一|二选一|后续决定|后续调研|留待|⚠|押注"
    r"|\bOPEN\b|\bTBD\b|\bTODO\b", re.I)
# sections whose whole purpose is deferral/open-tracking — their OPEN markers are legitimate
DEFERRED_SECTION = re.compile(r"开放问题|open\s*question|遗留|风险|未来工作|future\s*work|远期|后续阶段|待办事项", re.I)


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = mask_noise(path.read_text(encoding="utf-8", errors="replace"))
    problems: list[str] = []
    for sec in split_sections(text):
        title = sec["title"]
        if DEFERRED_SECTION.search(title):
            continue
        body = sec["body"]
        # "status line" = heading + first two non-empty body lines
        head_zone = title + "\n" + "\n".join(
            [ln for ln in body.splitlines() if ln.strip()][:2])
        c = COMPLETE.search(head_zone)
        if not c:
            continue
        o = OPEN.search(body)
        if not o:
            continue
        problems.append(
            f"line {sec['heading_line']}: section {title!r} marked complete "
            f"({c.group(0)!r}) but body carries open marker ({o.group(0)!r})")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: completion_open_conflict.py <file.md> [...]", file=sys.stderr)
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
