#!/usr/bin/env python3
"""
roadmap_stage_fields.py — SIGNAL (v0.3): per-phase field completeness for roadmaps.

This is the deterministic backing the catalog always named for HF-6 ("roadmap phase without acceptance
criteria") and the new HF-15 ("committed phase with vague/non-measurable DoD"). It runs ONLY on files
with >=2 stage headings, so it never fires on non-roadmaps.

Per stage it reports: which of {goal, deps, deliverables, DoD, status, risks, decision-gate} are
present; whether the stage is COMMITTED or DEFERRED; and — the HF-15 signal — whether a DoD line exists
but is *vague* (matches the shared vague-acceptance blocklist that hard-fail.md HF-15 defines). It also
surfaces GO/STOP/metric markers so a legitimate research phase can be netted out by the model.

Gaps on COMMITTED stages are foregrounded (a deferred/远期 phase without a hard DoD is acceptable).

check_file(path) -> (ok, problems). ok=True means "no missing-DoD / vague-DoD candidate on a committed stage".
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _textutils import mask_noise  # noqa: E402

STAGE_HEADING = re.compile(r"(?m)^(#{2,4})\s*(阶段|Phase|Stage)\s*(\d+)\b(.*)$", re.I)

# vague-acceptance blocklist — MUST mirror hard-fail.md HF-15 (single source of truth for the phrases)
VAGUE_DOD = re.compile(
    r"算例届时定|届时定|跑通即可|效果足够好|三选一或组合|三选一|二选一|后续调研确定|后续决定"
    r"|待补充调研|效果好|明显提升|视情况|酌情")

FIELDS = {
    "goal": re.compile(r"目标|产出|为何排|为何在此|\bgoal\b|research question|objective", re.I),
    "deps": re.compile(r"依赖|前置|需阶段|为何排|depends on|prerequisite|\bdeps\b", re.I),
    "deliverables": re.compile(r"产出|交付|deliverable", re.I),
    "DoD": re.compile(r"验证[:：]|验收|完成条件|acceptance|Definition of Done|DoD", re.I),
    "status": re.compile(r"✅|🔨|已完成|进行中|完成状态|状态[:：]|待实现|committed|deferred|\bnext\b", re.I),
    "risks": re.compile(r"风险|未知|⚠|开放问题|\brisk|open question", re.I),
    "decision_gate": re.compile(r"\bGO\b|\bSTOP\b|\bMODIFY\b|决策门|decision gate|若.{0,8}失败", re.I),
}
COMMITTED = re.compile(r"✅|🔨|进行中|已完成|首轮|待实现|committed|\bnext\b", re.I)
DEFERRED = re.compile(r"远期|后移|待调研|未来|later|deferred", re.I)
METRIC = re.compile(r"\d+\s*%|降\s*\d|≤|≥|<|>|阈值|指标|收敛|误差|精度|\bL2\b|error|\biters?\b", re.I)


def _stage_bounds(text: str):
    heads = list(STAGE_HEADING.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        yield m, text[m.start():end]


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = mask_noise(path.read_text(encoding="utf-8", errors="replace"))
    heads = list(STAGE_HEADING.finditer(text))
    if len(heads) < 2:
        return True, []  # not a roadmap-with-stages -> nothing to say
    problems: list[str] = []
    for m, block in _stage_bounds(text):
        n = m.group(3)
        line = text.count("\n", 0, m.start()) + 1
        head_and_body = block
        deferred = bool(DEFERRED.search(m.group(4)) or DEFERRED.search(block[:400]))
        committed = bool(COMMITTED.search(m.group(4)) or COMMITTED.search(block[:400])) and not deferred
        present = {f: bool(rx.search(head_and_body)) for f, rx in FIELDS.items()}
        has_metric = bool(METRIC.search(head_and_body))
        # Acceptance is present if a literal DoD/验证 line exists OR the phase is research-style with a
        # GO/MODIFY/STOP gate AND a metric (this is the HF-15 research escape — protects a legit
        # research roadmap from a false HF-6/DoD-missing signal).
        dod_line = present["DoD"]
        has_dod = dod_line or (present["decision_gate"] and has_metric)
        vague = VAGUE_DOD.search(head_and_body) if dod_line else None
        tag = "committed" if committed else ("deferred" if deferred else "unmarked")
        # Only foreground DoD problems on committed/unmarked stages
        if tag != "deferred":
            if not has_dod:
                problems.append(f"stage {n} (line {line}, {tag}): NO acceptance/DoD field (HF-6 signal)")
            elif vague:
                problems.append(
                    f"stage {n} (line {line}, {tag}): DoD present but VAGUE "
                    f"({vague.group(0)!r}) — HF-15 signal; has_metric={has_metric}, "
                    f"has_GO/STOP={present['decision_gate']}")
        other_missing = [f for f, ok in present.items() if not ok and f != "DoD"]
        if other_missing:
            problems.append(f"stage {n} (line {line}, {tag}): missing fields {other_missing}")
    # ok=True only if no committed-stage DoD problem surfaced
    dod_problem = any("HF-6 signal" in p or "HF-15 signal" in p for p in problems)
    return (not dod_problem), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: roadmap_stage_fields.py <file.md> [...]", file=sys.stderr)
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
