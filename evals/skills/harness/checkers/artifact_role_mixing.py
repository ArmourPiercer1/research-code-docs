#!/usr/bin/env python3
"""
artifact_role_mixing.py — SIGNAL (v0.3): which formal doc roles does one file carry?

Feeds HF-13 (mixed artifact responsibilities). It does NOT decide HF-13 — the model does, using the
role list + subordination markers + drift signals (from state_number_consistency / completion_open).
It reports, per role, whether the role is SECTION-LEVEL (owns a ## / ### heading) or only MENTION-LEVEL,
and whether the file uses appendix/link subordination (附 / appendix / 详见 / see [...]) — the escape
hatch that distinguishes a legitimate comprehensive report (roles subordinated in appendices) from a
hybrid file (divergent-lifecycle roles as body-level primary content).

check_file(path) -> (ok, problems). ok=True means "<=1 divergent section-level role" (not a candidate).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _textutils import mask_noise, split_sections  # noqa: E402

# role -> signature regex. Divergent-lifecycle roles are the ones whose canonical source / update
# frequency differ (a stable roadmap body should not also BE the live status + the session record).
ROLES = {
    "architecture": re.compile(r"架构|分层|模块|seam|接口设计|依赖方向", re.I),
    "roadmap": re.compile(r"路线图|里程碑|开发路线|分阶段|按难度", re.I),
    "status": re.compile(r"完成状态|当前进度|现状|已完成（20|state report|进度快照", re.I),
    "adr": re.compile(r"\bADR\b|架构决策|决策记录|adr-\d", re.I),
    "research_review": re.compile(r"文献|调研|综述|lit-review|对齐表|transfer|移植卡片", re.I),
    "validation": re.compile(r"验证策略|验证[:：]|测试算例|validation|回归测试", re.I),
    "open_questions": re.compile(r"开放问题|open question|待调研|留给后续", re.I),
    "handover_session": re.compile(r"HANDOVER|用户决定|本轮|会话|handoff|AskUserQuestion", re.I),
    "experiment_report": re.compile(r"实验结果|实验报告|基准结果|benchmark result|复现", re.I),
}
# roles that share a lifecycle with a design doc (not, by themselves, contamination)
STABLE_DESIGN_ROLES = {"architecture", "roadmap", "adr", "research_review", "validation", "open_questions"}
SUBORDINATION = re.compile(r"^#{1,6}\s*附|appendix|附录|详见|另见|see \[|参见", re.I)


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = mask_noise(path.read_text(encoding="utf-8", errors="replace"))
    sections = split_sections(text)
    section_level: dict[str, int] = {}   # role -> heading line where it owns a section
    mention_level: set[str] = set()
    for sec in sections:
        head = sec["title"]
        for role, rx in ROLES.items():
            if rx.search(head):
                section_level.setdefault(role, sec["heading_line"])
    # body-wide mention scan for roles not already section-level
    for role, rx in ROLES.items():
        if role not in section_level and rx.search(text):
            mention_level.add(role)
    subordinated = bool(SUBORDINATION.search(text))

    problems: list[str] = []
    roles_desc = []
    for role, ln in sorted(section_level.items(), key=lambda kv: kv[1]):
        roles_desc.append(f"{role}@L{ln}")
    if roles_desc:
        problems.append("section-level roles: " + ", ".join(roles_desc))
    if mention_level:
        problems.append("mention-level roles: " + ", ".join(sorted(mention_level)))
    # divergent = a volatile role (status / handover_session / experiment_report) co-resident with
    # stable-design roles at SECTION level -> the harmful kind of mixing
    volatile_present = {r for r in ("status", "handover_session", "experiment_report") if r in section_level}
    stable_present = {r for r in STABLE_DESIGN_ROLES if r in section_level}
    divergent = len(volatile_present) >= 1 and len(stable_present) >= 2
    if divergent:
        problems.append(
            f"HF-13 candidate: {len(stable_present)} stable-design + {len(volatile_present)} volatile "
            f"role(s) at section level; appendix/link subordination present={subordinated} "
            f"(if not subordinated + drift confirmed -> HF-13)")
    # ok=False only when a genuine divergent candidate exists
    return (not divergent), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: artifact_role_mixing.py <file.md> [...]", file=sys.stderr)
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
