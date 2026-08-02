<!--
generated_by_skill: (manual, v0.4 Phase A)
skill_version: n/a
source_documents:
  - tests/corpus/blind-runs/adjudication-v4b/ (blind inputs + .secret mapping)
  - docs/third-party-suggestions/DQE_v4_待决策项回复与下一阶段开发计划.md (D-6=A, D-7=A_QUALIFIED)
status: FINAL — 4 gold locked, 0 disputes
last_verified: 2026-08-02
-->

# Adjudication v4b — new proposal pair + HF-14b profile-boundary cases

Two isolated two-axis reviewers judged four blind docs (neutral shuffled names; `FILES_READ` confirmed
only the four inputs). Two of the four (BP-002-external, BP-002-audit) are byte-identical with different
declared profiles — an intentional test of profile-sensitivity.

| blind | case | Rev A (quality/gate) | Rev B (quality/gate) | gold |
|---|---|---|---|---|
| doc-c | GP-PROP-CONTROLLED-001 | PASS / ALLOW | PASS / ALLOW | **gold PASS / ALLOW** |
| doc-a | GN-PROP-VALIDATION-001 | PARTIAL / INCOMPLETE | PARTIAL / INCOMPLETE | **gold PARTIAL / INCOMPLETE** (non-ALLOW) |
| doc-d | BP-002-audit (controlled+audit) | PARTIAL / ALLOW | PASS / ALLOW | **gold ALLOW** |
| doc-b | BP-002-external (external+audit) | PARTIAL / ALLOW | PASS / ALLOW | **gold ALLOW** |

## Two results that matter

### 1. The D-6=A proposal rebuild is a valid pair
- **Positive (GP-PROP-CONTROLLED-001): PASS/ALLOW** from both — a complete controlled proposal with
  load-bearing validation/acceptance/rollout/rollback. (Reviewer A caught a minor `enabled: bool = true`
  vs "rollout defaults to false" inconsistency in the draft; fixed before locking, so the positive is
  clean.)
- **Negative (GN-PROP-VALIDATION-001): INCOMPLETE/INCOMPLETE** from both, HIGH. Removing the
  validation/acceptance/rollout/rollback sections from a *lean* base genuinely leaves a proposal a release
  gate cannot approve. Both reviewers chose **INCOMPLETE** (not BLOCK, not ALLOW): "missing required
  sections → can't approve yet", not "wrong". This is a **refinement of the plan's BLOCK expectation** —
  the two-axis contract maps missing-required-sections to INCOMPLETE. The negative's core purpose (a
  not-release-ready proposal must NOT be ALLOWed) is satisfied. **Gold not overridden to BLOCK** —
  reviewers are authoritative. Diagnostic pass condition for this case = **non-ALLOW**.

### 2. The D-7 HF-14b profile-severity map is empirically confirmed
Three byte-identical documents, gate flips with the profile alone:

| case | profile | gate | set by |
|---|---|---|---|
| BP-002-fail | controlled + release-gate | **BLOCK** | user ruling D-7 (Rev A agreed) |
| BP-002-audit | controlled + audit | **ALLOW** | Rev A/B |
| BP-002-external | external + audit | **ALLOW** | Rev A/B |

This proves the HF-14b BLOCK is the **controlled release-gate contract**, not a mechanical penalty on one
volatile line — exactly the D-7=A_QUALIFIED requirement.

## Corpus effect
- 4 gold locked; **0 disputes**. GN-PROP-001 v2 quarantined (D-6=A). BP-002-fail locked FAIL/BLOCK (D-7).
- Provenance: `tests/corpus/blind-runs/adjudication-v4b/`.
