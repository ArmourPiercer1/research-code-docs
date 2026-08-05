<!--
generated_by_skill: (manual, v0.4 Phase D)
skill_version_under_test: documentation-quality-evaluator 0.4.0 (== the frozen 0.4.0-pre-d16 bundle)
corpus: dataset_version 4
raw: tests/corpus/blind-runs/diag-2026-08-02/raw-results.json
metrics: evals/skills/results/documentation-quality-evaluator/diag-2026-08-02/metrics.json
status: 7/8 on 0.4.0-pre-d16 → RESOLVED: OQ-REPRO=A + D-16 fix → diagnostic 8/8 on candidate 0.4.1 (see reports/dqe-v0.4.1-diagnostic-close.md)
last_verified: 2026-08-05
-->

# DQE v0.4 diagnostic matrix (Phase D)

> **Version note (2026-08-05):** this matrix ran on **0.4.0-pre-d16** (now frozen at
> `evals/skills/snapshots/dqe-v0.4.0-pre-d16/`). Its 1 open item — OQ-REPRO / GN-EXP-REPRO-001 — resolved to
> **Option A** (no dedicated HF-REPRO gate), and the audit-gate instability it foreshadowed was fixed by
> **D-16** (deterministic 3-rule `GATE_DECISION`). On candidate **0.4.1** the diagnostic **closes 8/8**. This
> report is kept **immutable** as the historical 0.4.0 record; the close-out is in
> `reports/dqe-v0.4.1-diagnostic-close.md`.


**13 cases × 3 = 39 isolated v0.4 evaluators; 39/39 returned a verdict, 0 errors** (6 mid-run stalls
auto-retried; ~3.6M tokens, 15 min). Each evaluator loaded the v0.4 skill + hard-fail + rubric + the
caller-supplied profile + the target, ran the checker, walked the gates, and returned the two-axis verdict.

## Result vs the §D2 pass conditions

| §D2 condition | result | ok |
|---|---|---|
| BP-004 ordering (external ALLOW / controlled BLOCK) | external ALLOW×3, controlled BLOCK[HF-9]×3 | ✅ |
| external docs not HF-9-BLOCKed | GP-EXP-001 ALLOW×3, BP-004-external ALLOW×3 | ✅ |
| controlled missing frontmatter → HF-9 | BP-004-controlled BLOCK[HF-9]×3 | ✅ |
| BP-002 release case 3/3 BLOCK, only HF-14b | BLOCK[HF-14b]×3 | ✅ |
| BP-002 pass case 3/3 ALLOW | ALLOW×3 | ✅ |
| BP-002 audit case not HF-14b-BLOCKed | ALLOW×3 | ✅ |
| BP-005 pass case 3/3 ALLOW | ALLOW×3 | ✅ |
| HF-12A / HF-15 recall 3/3 | GN-EVIDENCE-BARE-CLAIM-001 BLOCK[HF-12A]×3; GN-ROADMAP-001 BLOCK[HF-15]×3 | ✅ |
| proposal positive 3/3 ALLOW | GP-PROP-CONTROLLED-001 ALLOW×3 | ✅ |
| proposal negative 3/3 non-ALLOW | GN-PROP-VALIDATION-001 INCOMPLETE×3 | ✅ |
| forbidden-blocker violations = 0 | **0** (HF-13/HF-14a never fired wrongly) | ✅ |
| profile echo / schema compliance | 39/39 echoed profile; 39/39 valid schema | ✅ |

## §17-style aggregate (two-axis)

| metric | value | bar | ok |
|---|---|---|---|
| golden-negative false ALLOW | **1** | == 0 | ❌ |
| golden-positive false non-ALLOW | 0 | == 0 | ✅ |
| required-blocker recall | **1.0** | ≥ 0.90 | ✅ |
| forbidden-blocker violation rate | **0.0** | ≤ 0.05 | ✅ |
| boundary-pair ordering | **1.0** | == 1.0 | ✅ |
| 3-run gate consistency | **1.0** | == 1.0 | ✅ |
| max score stddev | 0.0 | ≤ 5 | ✅ |
| profile echo compliance | **1.0** | == 1.0 | ✅ |

**7 of 8 pass, all perfectly stable (3/3).** This is a dramatic improvement over the v0.3 matrix (which
failed all 7). The v0.4 fixes are confirmed by clean, repeated evidence:

- **profile-aware HF-9 (D-01) works** — the BP-004 pair now orders correctly (external ALLOW, controlled
  BLOCK); GP-EXP-001 (external) no longer false-fails. This was the single confirmed v0.3 skill defect.
- **HF-14b profile severity (D-7) works** — the byte-identical BP-002 triad splits by profile
  (release-gate BLOCK / audit ALLOW / *external ALLOW seen in adjudication-v4b*).
- **HF-13 / HF-14a no longer over-fire** — forbidden-violation rate 0.0 (was 0.115 in v0.3); the clean
  fixtures confirm those v0.3 over-fires were fixture-induced.
- **HF-12A / HF-15 recall = 1.0** — the repaired fixtures fire their target gates stably (confirming the
  v0.3 "misses" were fixture defects, not skill gaps — HF-12A/HF-15 logic was left unchanged).
- **INCOMPLETE works** — the proposal negative (missing release sections) is correctly non-ALLOW via
  INCOMPLETE, stable 3/3.

## The one open item — GN-EXP-REPRO-001 false-ALLOW (= OQ-REPRO)

`GN-EXP-REPRO-001` (the Yahoo recipe stripped of every reproduction handle) was profiled **external +
audit** and got **QUALITY_BAND=PARTIAL / GATE_DECISION=ALLOW** stably (3/3). The evaluator **did** surface
the reproducibility gaps (missing hyperparameters/seed/versions, author-gated data, broken figure links)
as MAJOR quality findings → `QUALITY_BAND=PARTIAL`; but under **external + audit** (an advisory audit of an
upstream doc), with **no reproducibility hard gate** (HF-REPRO was deferred — ADR B2), it did not
gate-BLOCK → `GATE_DECISION=ALLOW`.

This is exactly the **OQ-REPRO** question ADR-DQE-001 deferred, now answered with data. It is **not a
regression or an over-fire** — it is a profile/expectation question:

- **Interpretation 1 (behavior is correct; expectation is wrong):** an external doc audited advisorily
  should NOT be release-BLOCKed for a quality gap — that is the very over-blocking D-01 fixed. The
  reproducibility defect *is* caught (PARTIAL). Under external+audit, ALLOW+PARTIAL is defensible; the
  case's "must not ALLOW" expectation baked in a release-gate assumption that its profile contradicts.
- **Interpretation 2 (a gate is missing):** reproducibility-failure should force non-ALLOW; since no hard
  gate exists and audit mode is advisory, it slipped through → design HF-REPRO. (Caveat: under *audit*
  mode HF-REPRO would be a MAJOR, not a BLOCK, so a gate alone would not change *this* case — the profile
  is the lever.)

The blind reviewers (adjudication-v4) rated it BLOCK, so the recorded gold and the v0.4 audit-mode ALLOW
genuinely conflict — a decision is required before the full admission matrix.

### Options (user decision)
- **(A) Re-profile to `controlled + release-gate` and re-run** (recommended first step): test the
  reproducibility defect under the profile where blocking is meaningful (a reproducibility doc WE gate for
  release). If v0.4 then BLOCKs via the rubric/non-compensatory rule → OQ-REPRO resolved, no new gate. If
  it still ALLOWs → escalate to (C).
- **(B) Accept & re-spec** GN-EXP-REPRO-001 as an external-audit case whose correct outcome is
  PARTIAL/ALLOW (it demonstrates v0.4 surfaces reproducibility without over-blocking external docs); add a
  separate controlled+release-gate reproducibility negative if a blocking test is wanted.
- **(C) Design HF-REPRO** — a dedicated reproducibility hard gate (blocker under controlled+release-gate;
  MAJOR under audit). Larger skill change; only if (A) shows the rubric alone cannot block it.

### Probe result (2026-08-02) — OQ-REPRO answered: no HF-REPRO needed
Ran GN-EXP-REPRO-001 under **`controlled + release-gate`** (2 isolated evaluators, `probe/`):
both returned **QUALITY_BAND=FAIL / GATE_DECISION=BLOCK** — and both explicitly noted that **even setting
HF-9 aside**, the stripped recipe collapses the rubric (total ≈ 39–44.5 < 75; Actionability ≈ 1.0,
Evidence-traceability ≈ 1.0–1.5) and **substantiates the non-compensatory rule** via HF-12A/E claim-support
+ a failed reader Layer-2 (cannot reproduce). **Conclusion:** the existing rubric + non-compensatory rule
already blocks a non-reproducible report under release-gate — **(C) HF-REPRO is NOT needed**. The
diagnostic's audit-mode ALLOW is the *correct* advisory outcome for an external doc; the only open item is
how to record the case (A vs B), which is a corpus-spec decision for the user.


## Not blocking, noted
- GP-EXP-001's checker ran on a stale path (`files_checked=0`) in the workflow (a hardcoded doc-path in the
  diag script; the injection embedded the correct doc, so the verdict ALLOW×3 is valid). Fix the path
  before the admission run.

## Gate
Phase E (full admission matrix + no-skill baseline + promotion) is **held** until the OQ-REPRO item is
resolved — 7/8 with one profiled negative in question is not yet a clean diagnostic pass.
