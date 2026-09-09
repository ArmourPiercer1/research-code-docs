#!/usr/bin/env python3
"""
make_injection.py — build the sub-agent injection prompt for one eval case.

Because we never install a skill to test it, an eval runs by injecting the skill's
SKILL.md body into a fresh sub-agent together with the case input, and asking for a
structured routing decision. This script assembles that prompt text so the
orchestrator can hand it to an Explore/general sub-agent verbatim.

Usage:
    python make_injection.py <case.yaml> <case-id> [--skill-md <path>]
If --skill-md is omitted, it is inferred from the case file's `skill:` field as
    .agents/skills/<skill>/SKILL.md  (resolved from the repo root).
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]  # harness/ -> skills/ -> evals/ -> root

DECISION_CONTRACT = """\
You are being evaluated for TRIGGERING behavior only. Do NOT actually perform the task.
Read the SKILL definition below, then read the CASE. Decide, as if this skill were one of
many available, whether THIS skill should handle the case.

Respond with a single JSON object and nothing else:
{
  "decision": "engage" | "decline" | "route" | "engage-with-clarify",
  "route_to": "<other-skill-name or null>",
  "justification": "<= 40 words, cite the SKILL's trigger/do-not-trigger lines>"
}
- "engage": this skill's trigger matches and no higher-priority skill should pre-empt it.
- "decline": out of scope; another skill or none should handle it.
- "route": out of scope for this skill; name the skill it belongs to in route_to.
- "engage-with-clarify": borderline; you would ask exactly one routing question first.
"""


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print("usage: make_injection.py <case.yaml> <case-id> [--skill-md <path>]", file=sys.stderr)
        return 2
    case_path = Path(args[0])
    case_id = args[1]
    data = yaml.safe_load(case_path.read_text(encoding="utf-8"))
    skill = data["skill"]
    cases = {c["id"]: c for c in data.get("cases", [])}
    if case_id not in cases:
        print(f"case id {case_id!r} not found in {case_path}", file=sys.stderr)
        return 2
    case = cases[case_id]

    skill_md = None
    if "--skill-md" in argv:
        skill_md = Path(argv[argv.index("--skill-md") + 1])
    else:
        skill_md = REPO_ROOT / ".agents" / "skills" / skill / "SKILL.md"
    if not skill_md.exists():
        print(f"SKILL.md not found: {skill_md}", file=sys.stderr)
        return 2
    skill_body = skill_md.read_text(encoding="utf-8")

    parts = [
        DECISION_CONTRACT,
        "\n===== SKILL DEFINITION (injected) =====\n",
        skill_body,
        "\n===== CASE =====\n",
        f"case_id: {case_id}\nset: {case.get('set')}\n",
        "input:\n" + (case.get("input", "").rstrip()) + "\n",
    ]
    if case.get("context"):
        parts.append("context:\n" + case["context"].rstrip() + "\n")
    print("".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
