<!--
generated_by_skill: (manual, v0.4.1 Phase D close-out + Phase E pre-flight)
skill_version: documentation-quality-evaluator 0.4.1 (candidate; D-16 gate-composition fix)
corpus: dataset_version 4
candidate_commit_base: 0585574 (HEAD) + uncommitted 0.4.1 version bump (working tree)
snapshots:
  - evals/skills/snapshots/dqe-v0.3.0/          (git 279c0ce)
  - evals/skills/snapshots/dqe-v0.4.0-pre-d16/  (git 14959a8)
  - evals/skills/snapshots/dqe-v0.4.1-candidate/ (working tree)
status: Phase D CLOSED 8/8; Phase E APPROVED_WITH_PRECONDITIONS (this doc is a precondition, §2.3)
last_verified: 2026-08-05
-->

# DQE v0.4.1 — diagnostic close-out (8/8) + the D.3 runaway incident

> **⚠️ SUPERSEDED IN PART by the Phase E canary (2026-08-05) — READ FIRST.** The "8/8 / BP-006-release
> BLOCK×3 / OQ-REPRO=A confirmed" claims below were based on the **single D.3 rerun sample**. The Phase E
> canary re-ran BP-006-release **3× on the frozen `dqe-v0.4.1-candidate` bundle and got ALLOW ×3 (stable)** —
> including one run at `QUALITY_BAND=FAIL` + `READER_TEST=FAIL`. The gate is **framing-dependent**, and under
> the D-16 rule its default resolves to a **false ALLOW**. This is the **D-16 × OQ-REPRO=A contract
> collision** (see `tests/corpus/blind-runs/phase-e-2026-08-05/canary-summary.md` and defect-ledger **D-17**).
> **Phase E is HALTED at the canary; §5's `PASS_8_OF_8` no longer holds for BP-006-release; a user decision is
> required before the matrix runs.** The runaway-incident (§1) and D-16-mechanics (§3) sections below remain
> accurate.


This is the canonical close of the Phase D diagnostic. It supersedes the "7/8, Phase E held" status in
`dqe-v0.4-diagnostic-matrix.md` (kept immutable as the historical 0.4.0-pre-d16 record). Authority:
`docs/third-party-suggestions/DQE_D3决策与PhaseE安全准入计划.md` (`D16_DECISION=ACCEPT`,
`CANDIDATE_VERSION=0.4.1`, `PHASE_D=PASS_8_OF_8`, `OQ_REPRO=RESOLVED_OPTION_A`).

## 1. The 63M-token runaway — HARNESS_ORCHESTRATION_FAILURE

```text
INCIDENT_CLASS=HARNESS_ORCHESTRATION_FAILURE
SEVERITY=HIGH_COST_NO_DATA_CORRUPTION
CORPUS_CLEANUP=NOT_REQUIRED
RESULT_CLEANUP=NOT_REQUIRED
```

The first D.3 rerun was launched as a background **Workflow**. Its `args` (intended as an array of cases)
arrived as a JSON **string**; the script iterated it **character by character** and spawned one agent per
character, hitting the 1000-agent cap after **~63M tokens / ~11 h** before failing (`WorkflowAgentCapError`).

- **Root cause:** parameter type drift (array → JSON string) + an unbounded `for … of` over that value.
- **Data impact:** none. Evaluators are read-only; aggregation never ran; no corpus / skill / results file
  was written by the runaway. Verified: the only artifacts from that period are the 7 direct-rerun outputs
  (below), not the workflow.
- **This was NOT:** a DQE quality failure, corpus contamination, an evaluator error, or a promotion result.

**Governance response (this round):**
1. Recorded in `docs/testing/benchmark-changelog.md` (dataset_version 4, Phase D.3 addendum + §incident).
2. The invalid run contributes to **no** metric (it produced no results file).
3. Structural fix — Phase E may **not** use a background Workflow (`BACKGROUND_WORKFLOW_FOR_ADMISSION=FORBIDDEN`):
   a **static, pre-counted, hash-verified plan** (`make_phase_e_plan.py` → `validate_eval_plan.py`) is the
   only launch path, with hard caps (`MAX_EVAL_RUNS=64`, `MAX_BATCH_SIZE=4`, `MAX_RUN_IDX=3`,
   `MAX_NESTING_DEPTH=1`, `MAX_RETRIES_PER_SLOT=1`). The validator **aborts before the first agent** if
   `runs` is a string, if any run_key repeats, or if the count exceeds the cap — i.e. the exact runaway
   signature is now a hard pre-flight failure (adversarially tested).

## 2. The 7 controlled direct reruns (no workflow, no loop)

Redone as **7 isolated direct Agent calls** on the D.3 targets:

| case | profile | result | notes |
|---|---|---|---|
| BP-006-release | controlled + release-gate | **BLOCK ×3** | via HF-12A/HF-12E; **HF-9 correctly silent** (frontmatter complete) |
| BP-006-audit | external + audit | first ran **3-way unstable** (BLOCK/ALLOW/INCOMPLETE) → after D-16: **ALLOW ×3** | the instability caught a real v0.4 text gap |
| GP-EXP-001 | external + audit | **ALLOW**, `files_checked=1` | the earlier `files_checked=0` stale-path bug is fixed |

## 3. D-16 — the gate-composition contract fix (the one real gap the rerun caught)

**Symptom:** BP-006-audit (external+audit, an unreproducible experiment report with complete external
frontmatter) resolved 3-way across identical runs.

**Root cause:** the v0.4.0 ALLOW preconditions (`total ≥ 75 AND FACTUAL_VALIDITY ≠ UNVERIFIED`) were
**release-gate semantics leaking onto `GATE_DECISION`**. A sub-75 / UNVERIFIED-but-unblocked audit doc had
no deterministic gate, so each run improvised differently.

**Fix (text-only; NO hard-gate threshold changed):** `GATE_DECISION` is now a **deterministic 3-rule
derivation**:

```text
(1) missing required section/input/profile, unclassifiable type, or checkers/reader not run → INCOMPLETE
(2) else any applicable hard gate MET at BLOCKER severity (after profile mapping)         → BLOCK
(3) else                                                                                    → ALLOW
```

The **rubric total and `FACTUAL_VALIDITY` gate `QUALITY_BAND` only** and never move `GATE_DECISION`;
`FACTUAL_VALIDITY=UNVERIFIED` bars the *green terminal gate* but does not change the gate value. Applied in
`SKILL.md` (§"How to derive each axis") + the harness `EVALUATOR_CONTRACT`. Re-ran BP-006-audit **×3 →
ALLOW ×3, stable**.

Because this is an **observable behavior change** (3-way → stable ALLOW) it is versioned **0.4.1**, not
0.4.0; the pre-fix build is frozen at `evals/skills/snapshots/dqe-v0.4.0-pre-d16/` so the instability stays
reproducible. See `dqe-v0.4-defect-ledger.md` D-16.

## 4. OQ-REPRO = A (confirmed; no HF-REPRO)

The BP-006 pair proves the profile carries the gate, with **no dedicated reproducibility hard gate**:

- `BP-006-release` (controlled + release-gate): a non-reproducible report **BLOCKs** via HF-12A/E + the
  non-compensatory rubric rule — `required_blockers: []`, so the BLOCK is not from a special HF-REPRO.
- `BP-006-audit` (external + audit, byte-identical body): correctly **ALLOWs** (advisory audit), while still
  surfacing the reproducibility findings (quality PARTIAL). It is **terminal_green=false** (reader FAIL +
  UNVERIFIED) — an ALLOW that is explicitly **not** a green terminal gate.

`HF_REPRO=NOT_ADOPTED`.

## 5. Diagnostic verdict

```text
PHASE_D = PASS_8_OF_8
```

The 8th condition (BP-006-audit gate stability) passed after D-16. The candidate advances to **0.4.1** and
Phase E is **APPROVED_WITH_PRECONDITIONS**. Preconditions completed in this round: version bump 0.4.1;
three hash-verified snapshots; this close-out; `validate_eval_plan.py` + hard caps; aggregator
`terminal_green` + `terminal_contract_mismatch_count` + `checker_execution_compliance`; the static
`phase-e-plan.json` (61 slots). Next: 2-slot canary, then the bounded 3-arm matrix.
