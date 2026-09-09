---
name: documentation-refactor
description: "Orchestrate the end-to-end restructuring of a MESSY or MIXED-RESPONSIBILITY DOCUMENT CORPUS — route through read-only inventory → state reconstruction → goal/scope → information-architecture DESIGN, then hand the design plan to migration + rewrite + a final quality review. This is an L1 CONTROL FLOW: it ROUTES to existing atomic skills, persists their artifacts, records a flow-state, verifies each hand-off, manages the human decision points, and STOPS HONESTLY (flow_status=BLOCKED) at any capability that is not built yet. It does NOT itself inventory, reconstruct, design, move, or rewrite — each stage is delegated. Use when a whole doc-set (not one file) is tangled/contradictory/duplicated and needs a governed refactor. NOT for grading one doc (documentation-quality-evaluator), designing one doc's split (document-information-architect), a messy code/workspace (scientific-workspace-reconstruction), or a numerical design question (numerical-research-software-design)."
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/user-invoked-only until its control-flow conflict eval passes; first real closed loop COMPLETE in Sprint 6B 2026-08-06, dry-run + candidate scope)
generated_by_skill: manual authoring (Batch 3, control-flow #1; per 2026-08-05 directive §9.1/§10; executor-tail claims corrected 2026-09-10 per Sprint 6B closure)
source_commit: 7919bc4
source_documents:
  - docs/skill-development/system-architecture.md §3.3 (the documentation-refactor chain)
  - docs/skill-development/conflict-matrix.md §1 (control-flow cluster; DENY/SEQ vs the other two flows)
  - references/interfaces/flow-state.schema.md (the §10.1 flow-state output this flow emits)
  - references/interfaces/README.md (the 7 handoff interfaces it routes between)
  - references/mattpocock-skills/skills/engineering/wayfinder/SKILL.md (MIT — orchestrator: route + persist decisions, don't do the work; method-borrow)
  - references/documentation-methodology/upstream-method-matrix.md §3.1
  - evals/skills/results/batch2_5/document-chain/ (Track A — the validated runnable prefix; this flow's integration fixture)
  - docs/skill-development/reports/sprint6-routing-and-first-closed-loop-2026-08-06.md (Sprint 6B — first closed loop COMPLETE)
  - evals/skills/results/batch3/documentation-refactor-closure/ (the closure's artifacts incl. the apply-gate BLOCKED negative)
last_verified: 2026-09-10
-->

# Documentation Refactor (L1 control flow · v0)

> **Experimental · manual/user-invoked-only.** This flow **orchestrates**; it does not do any
> stage's work itself. Its runnable prefix (inventory → state → goal/scope → information-architecture) is
> **validated** (Batch-2.5 Track A), and its executor tail (migration → rewrite → review → living-maintainer)
> was **built in Sprint 6B (2026-08-06)**: the first real closed loop is **COMPLETE for the dry-run +
> candidate scope** (zero source files changed; every open human decision left undecided). Apply-mode still
> requires an explicit write-approval: a request to move/overwrite/delete **without** that approval
> **stops at `flow_status=BLOCKED`, `blocked_by=explicit-write-approval-required`** — a truthful
> permission boundary, not a failure. Orchestration pattern (route + persist + record, never do the work)
> adapted from `wayfinder` (MIT), attributed in `upstream-method-matrix.md` §3.1.

## Purpose

Take a tangled **document corpus** (overlapping / contradictory / duplicated / mixed-responsibility docs) and
drive it through a governed refactor: recover the facts first, design the target information architecture, then
(when those skills exist) migrate + rewrite + re-review. The flow owns **routing, artifact persistence,
hand-off verification, decision-point management, and flow-state** — every substantive step is a **delegated
call to an existing atomic skill**.

## The call chain (route; do not re-implement any stage)

```text
workspace-forensics-and-inventory  (document-corpus mode, READ-ONLY)   → inventory-report
→ project-state-reconstructor      (verify claims; FACT/UNKNOWN/STALE) → project-state-report
→ goal-scope-and-workflow-elicitor (goal + non-goals + open decisions) → goal-scope-note
→ document-information-architect   (target IA; a PLAN, no move/rewrite)→ document-artifact-map (+ canonical-source-map, open-decisions)
── executor tail (built in Sprint 6B; dry-run/candidate scope by default) ──
→ content-canonicalization-and-migration  (dry-run move map first; may_move/delete/overwrite=false)
→ technical-document-rewriter              (new files only; never overwrite; candidate output)
→ documentation-quality-evaluator          (ADVISORY review of the result)
→ living-design-maintainer                  (proposal only; approved:false)
── apply-gate: explicit write-approval required to move/overwrite/delete ──
```

At every stage the flow **verifies the hand-off** (does the upstream artifact conform to its
`references/interfaces/<type>.schema.md`? — run `interface_check.py`) before invoking the next skill.

## Trigger conditions

Engage when **all** hold: (a) the input is a **doc corpus / multiple documents** (not a single file), (b) it is
**tangled** — mixed responsibilities, contradictions, duplication, or stale state across docs, and (c) the user
wants it **restructured / curated end-to-end**, not just one narrow action.

## Do-not-trigger conditions (route instead)

- **One document** to split/structure → `document-information-architect` directly (no flow needed).
- **Grade / judge** a doc → `documentation-quality-evaluator`.
- **Rewrite prose** of an otherwise-fine doc → `technical-document-rewriter`.
- **Just inventory** what exists → `workspace-forensics-and-inventory`.
- A messy **code / workspace** (not docs) → `scientific-workspace-reconstruction` (SEQ: if its residue is a doc
  corpus, it hands off to this flow after state is known — conflict-matrix §1).
- A **numerical / algorithm design** question → `numerical-research-software-design`.
- **Never run two L1 flows at once** (conflict-matrix §1: DENY/SEQ). If two could match, a read-only
  forensic/state pass + one routing question (`goal-scope-and-workflow-elicitor`) picks exactly one.

## Skeleton duties (directive §10) — what this flow DOES

1. **Route** to the next atomic skill in the chain (never do its work).
2. **Persist** each produced artifact to `evals/skills/results/<run>/…` (or the corpus's `docs/status/`).
3. **Verify the hand-off** — the upstream artifact conforms to its frozen interface (`interface_check.py`).
4. **Manage decision points** — aggregate every atomic skill's open decisions upward into the flow-state;
   pause for the human on any that block (e.g. IA's D-1 canonical-owner).
5. **Record flow-state** (§10.1) after each stage.
6. **Stop honestly** at the first missing capability: set `flow_status=BLOCKED` + a named `blocked_by`.
7. **Output the next hand-off** (next_skill + next_input), even when BLOCKED.

## Must NOT (directive §10)

- **Not** copy/re-implement any atomic skill's writing rules (no inventorying, fact-recovery, IA design,
  migration, or rewriting *inside* the flow — always delegate).
- **Not** implement a Batch-4/5 capability inline to "finish" the chain.
- **Not** mark an un-run step as completed (`completed_artifacts` = only artifacts that exist on disk).
- **Not** auto-move / delete / overwrite any file (the flow persists NEW artifacts only; migration is a later,
  dry-run-first, approval-gated skill).
- **Not** auto-run a second L1 flow.
- **Not** treat a DQE `ALLOW` as a release/authorization (it is advisory — architecture §gate-rule).

## Inputs / Outputs

- **Input:** the doc corpus path(s) + (optional) an existing forensics inventory / PSR state report to resume from.
- **Outputs:** the chain's artifacts (each conforming to its frozen interface) **+ one `flow-state` artifact**
  (`references/templates/flow-state.template.md`, contract `references/interfaces/flow-state.schema.md`).
- **Write-scope:** creates NEW files (artifacts + flow-state) only; `read_only` w.r.t. the corpus; never moves/
  overwrites/deletes; no isolated branch needed (it writes only under a results/status dir).

## v0 expected result

For a real corpus today, the honest v0 result is **`flow_status=COMPLETE` for
`requested_scope=dry-run-and-candidate-output`** — the full chain runs (design prefix + dry-run migration-map +
candidate rewrites + DQE-advisory + maintenance-impact plan) with **zero source files changed** and every open
human decision left undecided. If the request also asks to **apply** (move/overwrite/delete) **without an
explicit write-approval**, the honest result is **`flow_status=BLOCKED`,
`blocked_by=explicit-write-approval-required`** at the apply-gate — the flow does not relax permissions to
"finish". Worked examples: `evals/skills/results/batch3/documentation-refactor-closure/final-flow-state.md`
(COMPLETE closure) and `evals/skills/results/batch3/documentation-refactor-closure/flow-state-apply-without-approval-BLOCKED.md`
(the safety negative). The skeleton-era example
`evals/skills/results/batch3/documentation-refactor/flow-state-docs-skill-development.md` is historical
(pre-Sprint 6B, when the executors were not yet built).

## References to load

- `references/interfaces/flow-state.schema.md` (the output contract) + `references/interfaces/README.md`.
- `docs/skill-development/system-architecture.md` §3.3 + `docs/skill-development/conflict-matrix.md` §1.

## Scripts to run

- `evals/skills/harness/checkers/interface_check.py <artifact>` — verify each hand-off before the next call.
- `evals/skills/harness/checkers/flow_state_check.py <flow-state>` — verify the flow-state (honest COMPLETE/BLOCKED semantics).
- `evals/skills/harness/checkers/run_checks.py <run-dir>` — front-matter + status vocab on all outputs.
