<!--
generated_by_skill: (manual, Batch-3 skeletons per 2026-08-05 directive §10.1)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at authoring time)
source_documents:
  - docs/third-party-suggestions/Batch2_5集成冲刺与Batch3最小控制流开发计划.md (§10.1 unified flow-state output; §10 skeleton duties)
  - references/interfaces/README.md (the 7 handoff interfaces the flows route between)
document_lifecycle: ACCEPTED
status: DECIDED (flow-state contract v1 for the Batch-3 control-flow skeletons)
last_verified: 2026-08-05
-->

# Interface schema — `flow-state` (Batch-3 control-flow output)

Every Batch-3 control-flow skeleton (`documentation-refactor`, `scientific-workspace-reconstruction`,
`numerical-research-software-design`) emits **one `flow-state` artifact per run** — its own status output. This
is **not** one of the 7 frozen *handoff* interfaces (those pass data *between atomic skills*); it is the
**orchestrator's status record**. Checked by `evals/skills/harness/checkers/flow_state_check.py` (ADVISORY).

## The flow-state block (directive §10.1)

The artifact carries HF-9 provenance front-matter **and** a fenced ```yaml block with these **11 fields**:

```yaml
flow_name:            # REQUIRED. one of the three L1 flows.
flow_version:         # REQUIRED. e.g. 0.1.0.
flow_status:          # REQUIRED. RUNNING | BLOCKED | COMPLETE.
current_stage:        # REQUIRED. the stage reached (skill name / step label).
completed_artifacts:  # REQUIRED. list of produced artifacts (paths); [] if none yet.
open_decisions:       # REQUIRED. list of decisions awaiting a human; [] if none.
blocked_by:           # REQUIRED IF flow_status=BLOCKED — the missing capability / skill name.
                      #   (may be "none" only when NOT blocked.)
next_skill:           # REQUIRED. the next skill to run, "human decision", or "none (terminal)".
next_input:           # REQUIRED. what that next skill consumes (artifact path(s) / decision id).
quality_advisory:     # REQUIRED. DQE-advisory pointer/verdict, or "not run" — NEVER an auto-authorization.
source_commit:        # REQUIRED. repo@commit at run time.
```

## Rules (the honesty the checker enforces)

1. **`flow_status=BLOCKED` MUST name `blocked_by`** — a non-empty missing capability/skill. A BLOCKED flow with
   an empty `blocked_by` is a defect: "blocked" without saying by-what hides an un-built capability (directive
   §10: "把未执行步骤标为完成" is forbidden; the honest form is a named BLOCKED).
2. **A skeleton's most common honest result is `BLOCKED`** (directive §10.1) — its downstream atoms are Batch
   4/5 and not built. That is a **truthful capability boundary, not a failure**.
3. **`quality_advisory` is advisory only** — a DQE `ALLOW` in it authorizes **no** publish/move/delete/
   overwrite/install/auto-trigger (architecture §gate-rule). The flow never treats it as a release token.
4. **No step marked done that did not run.** `completed_artifacts` lists only artifacts that actually exist on
   disk; `current_stage` is the real last stage.
5. **`open_decisions` never silently drops** items surfaced by an atomic skill (they aggregate upward).

## Conformant example (a BLOCKED skeleton run — the common case)

```yaml
flow_name: documentation-refactor
flow_version: 0.1.0
flow_status: BLOCKED
current_stage: document-information-architect (design plan produced)
completed_artifacts:
  - evals/skills/results/batch2_5/document-chain/inventory-report.md
  - evals/skills/results/batch2_5/document-chain/project-state-report.md
  - evals/skills/results/batch2_5/document-chain/goal-scope-note.md
  - evals/skills/results/batch2_5/document-chain/document-artifact-map.md
open_decisions:
  - D-1 canonical current-status owner (user-preference; BLOCKS finalization)
  - D-4 README index scope (user-preference)
blocked_by: content-canonicalization-and-migration + technical-document-rewriter (Batch 5 — not built)
next_skill: "human decision (resolve D-1/D-4), then the Batch-5 migration/rewriter capability when it exists"
next_input: evals/skills/results/batch2_5/document-chain/document-artifact-map.md
quality_advisory: "evals/skills/results/batch2_5/document-chain/quality-advisory.md (PASS/INCOMPLETE — advisory; authorizes nothing)"
source_commit: 7919bc4
```
