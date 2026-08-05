---
name: scientific-workspace-reconstruction
description: Orchestrate recovery of a MESSY dev–test–experiment CODE WORKSPACE into a known, trustworthy state — route through read-only inventory → state reconstruction (what actually runs / is tested, FACT vs UNKNOWN vs STALE) → goal/scope, then hand off to workspace-architecture + provenance + migration planning. This is an L1 CONTROL FLOW: it ROUTES to existing atomic skills, persists their artifacts, records a flow-state, verifies each hand-off, and STOPS HONESTLY (flow_status=BLOCKED) at any capability not built yet. It does NOT itself inventory, reconstruct facts, design a workspace layout, or move files — each stage is delegated. Use when a research code/experiment workspace is tangled (unclear what runs, untracked scripts, stale results) and needs a governed reconstruction. NOT for a messy DOCUMENT corpus (documentation-refactor), a numerical DESIGN question (numerical-research-software-design), or a single read-only inventory (workspace-forensics-and-inventory).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/user-invoked-only until its control-flow conflict eval passes; v0 SKELETON)
generated_by_skill: manual authoring (Batch 3, control-flow #2; per 2026-08-05 directive §9.2/§10)
source_commit: 7919bc4
source_documents:
  - docs/skill-development/system-architecture.md §3.2 (the scientific-workspace-reconstruction chain)
  - docs/skill-development/conflict-matrix.md §1 (control-flow cluster; SEQ/DENY vs the other two flows)
  - references/interfaces/flow-state.schema.md (the §10.1 flow-state output this flow emits)
  - references/mattpocock-skills/skills/engineering/wayfinder/SKILL.md (MIT — orchestrator: route + persist, don't do the work; method-borrow)
  - references/documentation-methodology/upstream-method-matrix.md §3.2
  - evals/skills/results/batch3/scientific-workspace-reconstruction/ (worked prefix e2e on a real code workspace)
last_verified: 2026-08-05
-->

# Scientific Workspace Reconstruction (L1 control flow · v0 skeleton)

> **Experimental · manual/user-invoked-only · v0 SKELETON.** This flow **orchestrates**; it does not do any
> stage's work itself. Its runnable prefix (inventory → state → goal/scope) uses **built** skills. Its next
> stage — designing the target workspace architecture — is `dev-test-experiment-workspace-architect`, which is
> **Batch 5 and not built**, so a real v0 run **stops at `flow_status=BLOCKED / blocked_by=dev-test-experiment-workspace-architect`** with the recovered state handed to a human. Truthful capability boundary, not a failure.

## Purpose

Take a tangled research **code/experiment workspace** (unclear what runs, untracked or orphan scripts, stale
results, no clean dev–test–experiment separation) and drive it to a **known, trustworthy state** before any
restructuring: inventory what exists (read-only), recover what is actually FACT vs UNKNOWN vs STALE, and settle
the goal/scope — then hand off to the (future) workspace-architecture, provenance, and migration skills. The
flow owns **routing, artifact persistence, hand-off verification, decision management, and flow-state**; each
substantive step is a **delegated call**.

## The call chain (route; do not re-implement any stage)

```text
workspace-forensics-and-inventory  (workspace mode, READ-ONLY)          → inventory-report
→ project-state-reconstructor      (what RUNS / is TESTED; FACT/UNKNOWN)→ project-state-report
→ goal-scope-and-workflow-elicitor (goal + intended dev–test–exp flow)  → goal-scope-note
── v0 SKELETON STOPS HERE (the stages below are Batch 4/5, NOT BUILT) ──
→ dev-test-experiment-workspace-architect   (target layout)             [BLOCKED: not built]
→ experiment-provenance-and-reproducibility (provenance/repro plan)      [BLOCKED: not built]
→ workspace-migration-planner                (dry-run move map first)    [BLOCKED: not built]
→ scientific-validation-and-benchmark-planner                           [BLOCKED: not built]
→ living-design-maintainer                                              [BLOCKED: not built]
```

Every hand-off is **verified** against the artifact's frozen interface (`interface_check.py`) before the next
call.

## Trigger conditions

Engage when: the input is a **code / experiment workspace** (not a doc corpus, not a single algorithm question),
it is **tangled** (unclear what runs, untracked scripts, stale/duplicated results, no clean dev–test–experiment
structure), and the user wants it **reconstructed into a known state / reorganized end-to-end**.

## Do-not-trigger conditions (route instead)

- The mess is a **document corpus** → `documentation-refactor` (SEQ: this flow hands off to it if the *residue*
  after state-recovery is docs — conflict-matrix §1).
- A **numerical / algorithm design** question → `numerical-research-software-design`.
- Just a read-only **inventory** → `workspace-forensics-and-inventory`.
- Just "**what actually runs / is tested**" (facts only) → `project-state-reconstructor`.
- **Never run two L1 flows at once** (conflict-matrix §1). Route by dominant artifact after a read-only pass; one
  routing question (`goal-scope-and-workflow-elicitor`) if ambiguous.

## Skeleton duties (directive §10)

Route to the next atomic skill · persist each artifact · verify the hand-off (`interface_check.py`) · aggregate
open decisions upward · record flow-state (§10.1) after each stage · **stop honestly** at the first missing
capability (`flow_status=BLOCKED` + named `blocked_by`) · output the next hand-off.

## Must NOT (directive §10)

- **Not** implement `dev-test-experiment-workspace-architect` / migration / provenance **inline** to "finish".
- **Not** re-implement forensics / state-recovery / elicitation inside the flow (delegate).
- **Not** mark an un-run step completed; `completed_artifacts` = only on-disk artifacts.
- **Not** move / delete / overwrite any file (migration is a later, dry-run-first, approval-gated skill).
- **Not** auto-run a second L1 flow; **not** treat a DQE `ALLOW` as authorization.

## Inputs / Outputs / Write-scope

- **Input:** the workspace path + optional existing inventory/state to resume from.
- **Outputs:** the prefix artifacts (each conforming to its frozen interface) **+ one `flow-state`** (template
  `references/templates/flow-state.template.md`).
- **Write-scope:** creates NEW files (artifacts + flow-state) only; `read_only` w.r.t. the workspace; never
  moves / overwrites / deletes.

## v0 expected result

For a real workspace today, the honest v0 result is **`flow_status=BLOCKED`,
`blocked_by=dev-test-experiment-workspace-architect (Batch 5 — not built)`**, with inventory + state + goal/scope
completed and handed to a human. Worked example:
`evals/skills/results/batch3/scientific-workspace-reconstruction/flow-state-harness.md`.

## References / Scripts

- `references/interfaces/flow-state.schema.md` + `docs/skill-development/system-architecture.md` §3.2 +
  `conflict-matrix.md` §1.
- `interface_check.py` (verify each hand-off) · `flow_state_check.py` (honest BLOCKED) · `run_checks.py`.
