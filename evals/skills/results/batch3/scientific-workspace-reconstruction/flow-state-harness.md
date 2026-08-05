<!--
generated_by_skill: scientific-workspace-reconstruction
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/harness/ (the workspace), evals/skills/results/batch3/scientific-workspace-reconstruction/ (the prefix artifacts this run orchestrates)]
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
-->

# Flow-State — `scientific-workspace-reconstruction` run on `evals/skills/harness/`

A worked v0 skeleton run on a **real code workspace** (our own eval harness). The recovery prefix
(inventory → state → goal/scope) ran **live** via the delegated atomic skills (forensics in **workspace mode**,
then PSR, then the elicitor); this flow authored/recovered **nothing** itself. The next stage — designing the
target workspace layout (`dev-test-experiment-workspace-architect`) — is **Batch 5 and not built**, so
`flow_status=BLOCKED`.

```yaml
flow_name: scientific-workspace-reconstruction
flow_version: 0.1.0
flow_status: BLOCKED
current_stage: goal-scope-and-workflow-elicitor (goal/scope settled; hand-off verified)
completed_artifacts:
  - evals/skills/results/batch3/scientific-workspace-reconstruction/inventory-report.md      # forensics (workspace mode)
  - evals/skills/results/batch3/scientific-workspace-reconstruction/project-state-report.md  # project-state-reconstructor
  - evals/skills/results/batch3/scientific-workspace-reconstruction/goal-scope-note.md        # goal-scope-and-workflow-elicitor
open_decisions:
  - "Q-1 make_injection ↔ make_batch canonicity (user-preference)"
  - "Q-2 score_trigger ↔ score_all retirement (user-preference)"
  - "Q-3 test strategy for a harness with zero unit tests (user-preference)"
  - "Q-4 run-green E2→E3 gap: does run_checks.py / register_check.py actually run? (repo-verifiable — run it)"
  - "Q-5 9 unread checker bodies + present-only scripts (repo-verifiable)"
blocked_by: "dev-test-experiment-workspace-architect (Batch 5 — NOT built); then experiment-provenance-and-reproducibility + workspace-migration-planner (Batch 5)"
next_skill: "human decision (resolve Q-1/Q-2/Q-3, run the Q-4 checks), THEN dev-test-experiment-workspace-architect when it exists"
next_input: evals/skills/results/batch3/scientific-workspace-reconstruction/goal-scope-note.md
quality_advisory: "not run (prefix-only skeleton run; DQE-advisory would review the eventual target-layout plan, not the recovery prefix)"
source_commit: 7919bc4
```

## What ran (route trace — live, each stage delegated, hand-off verified)
- forensics(**workspace mode**) → `inventory-report.md` (45 files; 20 entry-point candidates; orphan candidate `register_check.py`; candidates+signals only — nothing claimed to run)
- project-state-reconstructor → `project-state-report.md` (13 FACT rows @ **E2 static** — "structured to run ≠ runs", no execution; test-status UNKNOWN; orphan resolved to a real caller)
- goal-scope-and-workflow-elicitor → `goal-scope-note.md` (goal + 7 non-goals + 5 open decisions; no fabricated human answers)
- Each hand-off verified with `interface_check.py` (all three PASS the frozen interface).

## Why it stopped here
The next stage — **designing the target dev–test–experiment workspace layout** — is
`dev-test-experiment-workspace-architect`, a **Batch-5** skill that does not exist. The v0 skeleton refuses to
design a layout or move files inline (directive §9.2/§10); it records a named `BLOCKED` and hands the recovered
state to a human. Correct capability boundary, not a failure. Note also the state is capped at **E2** (static
structure) — an honest reconstruction would run the Q-4 checks to reach E3 before committing to a redesign.

## Next handoff
1. A human resolves Q-1/Q-2/Q-3 and runs the Q-4 "does it actually run green" checks (E2→E3).
2. When `dev-test-experiment-workspace-architect` exists, it consumes `goal-scope-note.md` +
   `project-state-report.md` to plan the target layout (a plan; migration executes later, dry-run first).
   Until then: **BLOCKED, honestly.**
