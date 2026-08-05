<!--
generated_by_skill: (manual, Batch-3 minimal control-flow skeletons per 2026-08-05 directive §9-§10, §13)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at sprint time)
source_documents:
  - docs/third-party-suggestions/Batch2_5集成冲刺与Batch3最小控制流开发计划.md (§9 build order, §10 skeleton duties + §10.1 flow-state, §13 Sprint-5 spec)
  - .claude/skills/{documentation-refactor,scientific-workspace-reconstruction,numerical-research-software-design}/SKILL.md
  - references/interfaces/flow-state.schema.md + evals/skills/harness/checkers/flow_state_check.py
  - evals/skills/results/batch3/**/flow-state-*.md (three worked BLOCKED flow-states)
document_lifecycle: ACCEPTED
status: DECIDED (all three Batch-3 v0 skeletons built + light-validated; all stay experimental + manual-only)
last_verified: 2026-08-05
-->

# Batch 3 — Minimal Control-Flow Skeletons: Report (3 flows)

> **Headline.** The three L1 control-flow skeletons are built as **v0 orchestrators** that **route to existing
> atoms, persist their artifacts, record a `flow-state`, verify each hand-off, and STOP HONESTLY (`flow_status=
> BLOCKED`) at the first missing Batch-4/5 capability** — no faked closed loops. Build order per §9:
> **`documentation-refactor` → `scientific-workspace-reconstruction` → `numerical-research-software-design`**.
> Each has a worked BLOCKED flow-state (two reuse the real Batch-2.5 chains; one ran a **live** prefix on a real
> code workspace), all pass `flow_state_check` (honest-BLOCKED enforced), and all pass a no-context reader test.
> All three ship **`experimental` + `disable-model-invocation: true` + manual/user-invoked-only**; auto
> co-trigger is impossible by construction. Nothing installed or pushed.

## 0. What a v0 skeleton is (directive §10)

Each flow does **only**: route to the next atomic skill · persist each produced artifact · verify the hand-off
(`interface_check.py`) · aggregate open decisions upward · record flow-state (§10.1) · **stop honestly** at the
first missing capability (`flow_status=BLOCKED` + a **named** `blocked_by`) · output the next hand-off. It must
**not**: copy an atom's writing rules, implement a Batch-4/5 capability inline, mark an un-run step done,
auto-move/delete/overwrite, auto-run a second L1 flow, or treat a DQE `ALLOW` as authorization. **"The common,
correct result of a v0 run is BLOCKED"** (§10.1) — a truthful capability boundary, not a failure.

## 1. The flow-state contract + checker

- `references/interfaces/flow-state.schema.md` — the §10.1 11-field flow-state (`flow_name`, `flow_version`,
  `flow_status ∈ {RUNNING,BLOCKED,COMPLETE}`, `current_stage`, `completed_artifacts`, `open_decisions`,
  `blocked_by`, `next_skill`, `next_input`, `quality_advisory`, `source_commit`).
- `evals/skills/harness/checkers/flow_state_check.py` (ADVISORY in `run_checks.py`; `--advisory-is-hard`
  enforces). **Load-bearing rule: a `BLOCKED` flow MUST name a non-empty `blocked_by`** — a blocked flow that
  hides *what* it is blocked by is a defect. Self-tested (GOOD-BLOCKED passes; empty-`blocked_by` fails).
- `references/templates/flow-state.template.md` — the authoring shape.

## 2. The three skeletons

| flow | runnable prefix (built atoms) | honest BLOCKED at (not built) | e2e |
|---|---|---|---|
| `documentation-refactor` | forensics(doc-corpus) → PSR → goals → IA | `content-canonicalization-and-migration` + `technical-document-rewriter` + `living-design-maintainer` (Batch 5) | **reuses real Track-A** artifacts |
| `scientific-workspace-reconstruction` | forensics(workspace) → PSR → goals | `dev-test-experiment-workspace-architect` (Batch 5) | **LIVE prefix** on `evals/skills/harness/` |
| `numerical-research-software-design` | (state → goals →) RQLP → lit-review → RES → UDM | `research-software-problem-framer` + `scientific-software-architect` + `algorithm-technical-spec-author` + prototype/validation/roadmap (Batch 4) | **reuses real Track-B** evidence base |

### 2.1 `documentation-refactor` (v0 · control flow #1)
The most complete runnable prefix — its whole prefix was **validated in Batch-2.5 Track A**, so its worked
flow-state orchestrates those real artifacts and stops BLOCKED at the Batch-5 executor tail. Reader:
`HONEST_BLOCKED=YES · NO_FAKED_COMPLETION=YES · NO_AUTO_AUTHORIZATION=YES · READER_CAN_ACT=YES`. The DQE advisory
inside the flow-state is explicitly "advisory; authorizes no move/rewrite/publish."

### 2.2 `scientific-workspace-reconstruction` (v0 · control flow #2)
Its prefix had **not** been exercised, so this sprint ran it **live** (three isolated sub-agents) on a real code
workspace, `evals/skills/harness/` — which also delivered **forensics WORKSPACE-mode coverage** (complementing
Track A's document-corpus mode). Results: forensics found 45 files + 20 entry-point candidates + a genuine
orphan (`register_check.py` unwired by the aggregator); PSR held **"structured-to-run ≠ runs"** (13 FACTs capped
at **E2 static**, no execution, no `.pyc` regenerated); goals produced 7 non-goals + 5 open decisions with no
fabricated answers. The flow then BLOCKs at `dev-test-experiment-workspace-architect`. All three prefix
artifacts PASS the frozen interface; the harness's inventoried files are **untouched** (only my own checker
files changed under `harness/`). Reader: all four discipline checks green.

### 2.3 `numerical-research-software-design` (v0 · control flow #3)
**Third by design** (§9.3): its numerical-**design** core atoms are Batch 4 and absent. Its evidence front
(RQLP → lit-review → RES → UDM) was **validated in Batch-2.5 Track B**, so its worked flow-state consults those
real artifacts, carries the **E2 cap + two E0 assumptions** forward, and BLOCKs at the six missing Batch-4
design skills. Reader adds `NO_FACT_UPGRADE=YES` (the backbone is an E2 HYPOTHESIS, never claimed proven).

## 3. Results at a glance

| flow | flow_state_check | interface_check (prefix artifacts) | reader test | MUST-NOT compliance |
|---|---|---|---|---|
| documentation-refactor | ✅ honest BLOCKED | ✅ (Track-A artifacts) | ✅ 4/4 | no move/rewrite; no faked completion; DQE=advice |
| scientific-workspace-reconstruction | ✅ honest BLOCKED | ✅ (3 live prefix artifacts) | ✅ 4/4 | no layout/move inline; E2 not inflated to "runs" |
| numerical-research-software-design | ✅ honest BLOCKED | ✅ (Track-B artifacts) | ✅ 5/5 | no design authored; no fact-upgrade; delegates retrieval |

`run_checks.py evals/skills/results/batch3 --advisory-is-hard` → `hard_fail = False`. All three SKILL.md
HARD-green. conflict-matrix §1 (the top release gate) updated **PROJECTED → LIVE** (manual-only; auto
co-trigger impossible by construction). Registry: 3 stale `planned` one-liners replaced with 3 full
`experimental` entries; `upstream-method-matrix.md` §2.9 added (wayfinder orchestration method-borrow, MIT).

## 4. Honest scope & deferrals (not hidden)

- **Skeletons, not closed loops** (directive §13: "不要求完整闭环"). Every flow legitimately ends BLOCKED because
  its executor/design atoms are Batch 4/5 and not built. That is the point — the skeletons exist to route +
  record + stop honestly, and to be ready when those atoms land.
- **Trigger/conflict cases are AUTHORED, not yet sub-agent-run.** Batch 1/2 got an 8/8 sub-agent trigger run;
  the §13 light skeleton round authors the routing/conflict cases + runs the e2e + reader instead. A full
  trigger/conflict sub-agent run (the gate before any `auto_trigger`) is the natural next step.
- **One e2e per flow, one mode.** `documentation-refactor` + `numerical` reuse the Batch-2.5 chains (real, but
  not a fresh multi-target run); only `scientific-workspace-reconstruction` ran a fresh live prefix this sprint.
- **All three stay `experimental` + manual-only.** They do **not** flip to `auto_trigger` until they pass the
  control-flow conflict eval (creation-roadmap §3 gate). The reconstruction↔refactor SEQ and the DENY pairs are
  encoded but enforced by manual-only for now.
- **Batch 4/5 still gates the full loops.** `documentation-refactor` needs migration+rewriter+maintainer;
  `scientific-workspace-reconstruction` needs the workspace-architect+provenance+migration; `numerical` needs
  the six numerical-design atoms. None is built; each flow names exactly what it waits on.

## 5. Verdict

Batch 3 delivers **three honest v0 control-flow skeletons**: each routes real Batch-1/2 atoms, records a
verifiable flow-state, and **stops at a named capability boundary rather than faking a result**. The
orchestration layer now exists and is correct about what it cannot yet do — which is exactly what a skeleton
built on top of an incomplete atom set should be. Nothing installed or pushed; all skills (the 3 new flows + the
8 atoms) remain experimental/manual-only; DQE + the Batch-1/2 atoms are untouched. Evidence:
`evals/skills/results/batch3/**` + `references/interfaces/flow-state.schema.md`.
