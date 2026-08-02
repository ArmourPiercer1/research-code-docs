<!--
generated_by_skill: (manual, v0.4 Phase D — decision brief)
skill_version_under_test: documentation-quality-evaluator 0.4.0
corpus: dataset_version 4
source_documents:
  - docs/skill-development/reports/dqe-v0.4-diagnostic-matrix.md
  - tests/corpus/blind-runs/diag-2026-08-02/raw-results.json (39 diagnostic runs)
  - tests/corpus/blind-runs/diag-2026-08-02/probe/ (2 controlled+release-gate probes)
  - docs/skill-development/adr/ADR-DQE-001-...md (OQ-REPRO, Decision 4/B2)
status: OPEN — user decision needed (A / B / C) before the full admission matrix
last_verified: 2026-08-02
-->

# OQ-REPRO decision brief — GN-EXP-REPRO-001 (the diagnostic's one open item)

## 1. One-paragraph summary

The v0.4 diagnostic matrix passed **7 of 8** conditions, every case stable **3/3**. The single deviation is
`GN-EXP-REPRO-001` (a reproducibility negative) getting **PARTIAL / ALLOW** under its declared
`external + audit` profile, where the corpus expected a non-ALLOW. A follow-up probe under
`controlled + release-gate` returned **FAIL / BLOCK** twice. Together these show the v0.4 skill is behaving
**correctly on both profiles** — and that **no dedicated reproducibility hard gate (HF-REPRO) is needed**.
What remains is a small **corpus-spec** choice about how to record this one case. This brief lays out the
evidence and three options so you can decide.

## 2. What the case is

`GN-EXP-REPRO-001` is the Yahoo ResNet-50 recipe (an **external** upstream doc) after a clean mutation that
strips **every reproduction handle** — training command, all hyperparameters, LR schedule, code commits,
framework versions, hardware — while keeping the result numbers (74.0%, 11ms). Intended defect: "a report
you cannot reproduce." It carries **no local traceability front-matter** (it is upstream). I profiled it
`provenance_policy: external, decision_mode: audit`.

## 3. The evidence

### 3.1 Diagnostic (external + audit) — ALLOW ×3, stable
| run | QUALITY_BAND | GATE_DECISION | blockers |
|---|---|---|---|
| 1 / 2 / 3 | PARTIAL | ALLOW | [] |

The evaluators **did** surface the reproducibility gaps (missing hyperparameters/seed/versions, author-gated
HDFS data, broken figure/notebook links) as **MAJOR quality findings → QUALITY_BAND=PARTIAL**. But under
`external + audit` — an advisory audit of an upstream doc — with **no reproducibility hard gate** and
`audit` being non-blocking, the gate stayed **ALLOW**. HF-9 correctly did **not** fire (external ⇒ MINOR/NA).

### 3.2 Probe (controlled + release-gate) — BLOCK ×2
| probe | QUALITY_BAND | GATE_DECISION | blockers | independent-of-HF-9? |
|---|---|---|---|---|
| 1 | FAIL | BLOCK | [HF-9] | **yes** — total 44.5<75, Actionability 1.0, non-comp substantiates |
| 2 | FAIL | BLOCK | [HF-9, HF-12A/E] | **yes** — total 39<75, Evidence-trace 1.0, non-comp substantiates |

Both probes reached BLOCK **two independent ways**: (a) HF-9 (this doc has no front-matter, so under
`controlled` HF-9 is a blocker); and (b) — the load-bearing one — the stripped recipe **collapses the
rubric** (Actionability ≈ 1.0, Evidence-traceability ≈ 1.0–1.5, total < 75) and **substantiates the
non-compensatory rule** via HF-12A/E claim-support + a failed reader Layer-2 (cannot reproduce). Both
evaluators stated the non-ALLOW holds **even if HF-9 is set aside** — i.e. reproducibility alone blocks it.

## 4. What the evidence means

1. **v0.4 is correct on both profiles.** `external + audit → ALLOW + PARTIAL` (surface the defect, don't
   over-block an upstream doc — the very over-blocking D-01 fixed). `controlled + release-gate → BLOCK`
   (a reproducibility doc we gate for release cannot pass). This is the two-axis + profile contract working
   as designed.
2. **OQ-REPRO is answered: no HF-REPRO is needed.** The existing **rubric + non-compensatory rule** already
   forces non-ALLOW for a non-reproducible report under release-gate (probe, 2/2, independent of HF-9). ADR
   B2 said "design HF-REPRO only if the diagnostic shows this case wrongly ALLOWs" — it ALLOWed only under
   *audit*, where ALLOW is correct; a dedicated gate would not (and should not) change the audit outcome.
3. **The diagnostic "false-allow" is a profile/expectation mismatch, not a skill bug.** The case's
   `must-not-ALLOW` expectation encoded a release-gate assumption that its `external + audit` profile
   contradicts.

## 5. The decision — how to record this one case

### Option A — split into a profile pair (recommended)
- Keep `GN-EXP-REPRO-001` as `external + audit`; correct its gold to **PARTIAL / ALLOW** with
  `required_findings: [missing-code-version, …]` (the "negative" is the quality finding; the gate is
  correctly ALLOW under advisory audit). Reclassify it from `golden-negative` to a boundary/quality case.
- Add a NEW `GN-EXP-REPRO-GATE-001`: the **same stripped recipe but WITH traceability front-matter** (so
  HF-9 does not fire) under `controlled + release-gate`, expected **FAIL / BLOCK** via the rubric +
  non-compensatory rule — a *clean* reproducibility-blocking test with no HF-9 confound.
- Re-adjudicate both (isolated A/B), re-run the affected diagnostic slots.
- **Pros:** both paths (audit-surface, release-block) are adjudicated and regression-covered; matches the
  BP-002 / BP-004 profile-pair philosophy; isolates reproducibility→BLOCK cleanly. **Cons:** one new
  fixture + a small re-adjudication.

### Option B — simplest: correct the gold in place
- Keep `GN-EXP-REPRO-001` as `external + audit`, change its gold to **PARTIAL / ALLOW**; rely on the probe
  as the recorded release-gate evidence. No new case.
- **Pros:** diagnostic → 8/8 immediately; least work. **Cons:** the corpus then has no *adjudicated*
  reproducibility-BLOCK case (only the probe); the reproducibility-blocking path is evidenced but not a
  standing regression.

### Option C — add HF-REPRO anyway
- Implement a dedicated reproducibility hard gate (BLOCKER under `controlled + release-gate`; MAJOR under
  `audit`).
- **Pros:** an explicit, named reproducibility gate. **Cons:** the probe shows it is **unnecessary** (the
  rubric already blocks); it is a larger skill change that contradicts the "minimal v0.4" principle; under
  `audit` it would still be MAJOR (ALLOW), so it would not change the diagnostic case.

## 6. Recommendation

**Option A.** It is the most principled and leaves the corpus with clean, adjudicated coverage of both
profiles, at the cost of one small fixture + a short re-adjudication. If you want the fastest path to a
clean diagnostic and are comfortable relying on the probe as the release-gate evidence, **Option B** is
fine. **Option C is not recommended** — the evidence says the rubric already does the job.

## 7. What I need from you

1. Choose **A / B / C** for GN-EXP-REPRO-001 (this is the last item before the corpus is admission-ready).
2. You also asked to **review the v0.4 skill changes first** — see
   `docs/skill-development/reports/dqe-v0.4-skill-change-summary.md` for a file-by-file diff guide. I will
   **not** run the Phase E full-admission matrix until you have reviewed v0.4 and ruled on this item.
