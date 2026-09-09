#!/usr/bin/env python3
"""
make_batch.py — emit ONE evaluation prompt for a skill covering all its trigger + conflict
cases at once, for a single sub-agent to answer. The sub-agent sees the injected SKILL.md
and a compact roster of OTHER skills (so route_to is grounded), but never the expected answers.

Usage: python make_batch.py <skill-name>
Reads evals/skills/trigger/<skill>.yaml and evals/skills/conflict/<skill>.yaml.
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]

ROSTER = """\
Other skills available for routing (name — one-line role):
- code-review — review a code diff (Standards + Spec).
- diagnosing-bugs — diagnose a specific broken/failing/slow behaviour.
- tdd — build a behaviour test-first.
- implement — build a stable, specified feature.
- to-spec — synthesize a finished discussion into a spec.
- to-tickets — split a spec into tickets.
- domain-modeling — define STABLE domain terms + ADRs (the glossary).
- paper-fetch-skill — read/summarize/verify a single KNOWN paper.
- lit-review — survey an open literature topic (retrieval).
- wos-research / deep-research — heavier literature/web retrieval.
- grilling — the user-invoked relentless manual interview primitive.
- improve-codebase-architecture — restructure code into deep modules (AFTER facts recovered).
- scientific-software-architect — overall scientific system architecture (planned).
- scientific-prototype-experiment — numerical prototype answering a convergence/noise question (planned).
- research-evidence-synthesizer — build an evidence matrix from retrieved papers (planned).
- research-software-roadmap-author — build roadmap phases with acceptance criteria (planned).
- technical-document-rewriter — rewrite a document (never overwrites originals) (planned).
- scientific-validity-review — math/units/stability/RNG review of code (planned).
- project-state-reconstructor — recover verifiable project facts into a state report.
- goal-scope-and-workflow-elicitor — interview for goals/scope/workflow (automatic, in-flow).
- uncertainty-and-decision-manager — tag items with status + evidence level; the decision register.
- documentation-quality-evaluator — grade a documentation artifact against gates + rubric.
"""

CONTRACT = """\
You are evaluating the TRIGGERING behaviour of ONE skill (defined below). For each CASE, decide
whether THIS skill should handle it, as if it sat among the many skills in the roster. Do NOT
perform any task. Use the skill's own Trigger / Do-not-trigger sections and the trigger-priority
ladder (safety/forensics > explicit invocation > router > control flows > specialized atoms >
existing domain skills > general help).

Return ONLY a JSON array, one object per case, in order:
[{"id": "...", "decision": "engage|decline|route|engage-with-clarify", "route_to": "<skill or null>",
  "justification": "<=30 words citing the skill's trigger/do-not-trigger"}]
Decisions:
- engage: trigger matches and nothing higher-priority pre-empts.
- decline: out of scope; no named skill needed (or a trivially-direct answer).
- route: out of scope for THIS skill; name the owner in route_to.
- engage-with-clarify: borderline/underspecified; you would ask exactly one routing question first.
"""


def load_cases(kind: str, skill: str):
    p = ROOT / "evals" / "skills" / kind / f"{skill}.yaml"
    if not p.exists():
        return []
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    return d.get("cases", [])


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: make_batch.py <skill-name>", file=sys.stderr)
        return 2
    skill = argv[1]
    skill_md = (ROOT / ".agents" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    cases = load_cases("trigger", skill) + load_cases("conflict", skill)

    out = [CONTRACT, "\n", ROSTER, "\n===== SKILL UNDER TEST (injected SKILL.md) =====\n", skill_md,
           "\n===== CASES =====\n"]
    for c in cases:
        line = f'- id: {c["id"]} | set: {c.get("set")} | input: {c.get("input","").strip()}'
        if c.get("context"):
            line += f' | context: {c["context"].strip()}'
        out.append(line + "\n")
    out.append(f"\nReturn the JSON array for all {len(cases)} cases now.")
    print("".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
