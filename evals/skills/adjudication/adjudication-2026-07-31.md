<!--
generated_by: Corpus Builder (this session), from isolated Reviewer A/B outputs
source: evals/skills/adjudication/reviewer-{A,B}-2026-07-31.md + reviewer-results-2026-07-31.yaml
blind_run: tests/corpus/blind-runs/adj-2026-07-31
last_verified: 2026-07-31
-->

# Adjudication — DQE corpus, round 1 (2026-07-31)

Reviewer A and Reviewer B ran as **independent isolated sub-agents** (general-purpose, no DQE skill /
hard-fail catalog / rubric), each reviewing the same 20 blind inputs (UUID-named, class-dir stripped,
no expected labels). Neither saw the other.

## Inter-reviewer reliability

- **Verdict agreement A vs B: 20 / 20** (they never split).
- **Primary defect tag agreement: 20 / 20** (they named the same principal defect on every case).

This high reliability means the corpus is discriminative and the reviewer rubric is unambiguous. It also
means the split below is **builder-intent vs reviewers**, not reviewer-vs-reviewer.

## Outcome: 15 gold-consensus, 5 queued

| case | A | B | intent | outcome |
|---|---|---|---|---|
| GP-ADR-001 | PASS | PASS | PASS | **GOLD** |
| GP-PROP-001 | PASS | PASS | PASS | **GOLD** |
| GP-PROP-002 (Rejected PEP) | PASS | PASS | PASS | **GOLD** ← rejected-decision ≠ low quality, confirmed |
| GP-EXP-001 | PASS | PASS | PASS | **GOLD** |
| GP-ROADMAP-001 | PASS | PASS | PASS | **GOLD** ← HF-15 research-escape held |
| GN-ADR-002 (HF-13) | FAIL | FAIL | FAIL | **GOLD** |
| BP-001-pass / -fail | PASS / FAIL | PASS / FAIL | PASS / FAIL | **GOLD** (ordering correct) |
| BP-002-pass / -fail | PASS / FAIL | PASS / FAIL | PASS / FAIL | **GOLD** (ordering correct) |
| BP-003-pass / -fail | PASS / FAIL | PASS / FAIL | PASS / FAIL | **GOLD** (ordering correct) |
| BP-004-external | PASS | PASS | PASS | **GOLD** ← external profile tolerates missing FM |
| BP-005-pass / -fail | PASS / FAIL | PASS / FAIL | PASS / FAIL | **GOLD** (ordering correct) |
| GN-ADR-001 | PARTIAL | PARTIAL | FAIL | **QUEUED** |
| GN-PROP-001 | PARTIAL | PARTIAL | FAIL | **QUEUED** (+ mutation defect, below) |
| GN-EXP-001 | PARTIAL | PARTIAL | FAIL | **QUEUED** |
| GN-ROADMAP-001 | PARTIAL | PARTIAL | FAIL | **QUEUED** |
| BP-004-controlled | PARTIAL | PARTIAL | FAIL | **QUEUED** |

## The user-decision queue (5 items)

All five queued cases share **one** root question. The reviewers, judging holistically **without** the
hard-fail catalog, rated each single-defect negative **PARTIAL** ("excellent doc, one real defect"). The
corpus labels them **FAIL** because the DQE's **v0.3 non-compensatory / anti-erosion contract** says a
*met hard gate is a non-downgradeable BLOCKER* → FAIL. Both framings are internally correct; they differ
on the FAIL-vs-PARTIAL boundary for a one-defect document.

**Q-1 (policy, affects GN-ADR-001, GN-EXP-001, GN-ROADMAP-001, BP-004-controlled).** Should a single
met hard gate (HF-9 / HF-12A / HF-15) or a single serious soft defect (missing-rationale) make the gold
label **FAIL** (aligning gold with the DQE's binary gate contract — recommended, since the whole v0.3
upgrade exists to stop gate-erosion) or **PARTIAL** (aligning gold with holistic severity)?
- **Recommendation:** keep gold = **FAIL** for the hard-gate cases (GN-EXP-001 HF-12A, GN-ROADMAP-001
  HF-15, BP-004-controlled HF-9). These are exactly the "one real blocker on an otherwise-good doc"
  shape the DQE must FAIL, and the reviewer PARTIAL is *evidence the defect is real but subtle* — a good
  discriminator. For GN-ADR-001 (soft, no hard gate) either FAIL-on-rationale-anchor or PARTIAL is
  defensible; lean FAIL to keep the ADR rationale anchor meaningful.

**Q-2 (data quality, GN-PROP-001 only).** Both reviewers caught an **unintended** secondary defect: the
provenance mutation removed the Test Plan / Graduation Criteria sections but **left the KEP signoff
checklist still asserting they are "in place"**, creating a checklist-vs-body contradiction. Per policy
§6.3 (a mutation that adds non-target defects → demote), this case should be **refined** (also blank the
checklist items so the sole defect is the missing sections) **or demoted to candidate**.
- **Recommendation:** refine the `GN-PROP-001` mutation plan to also clear the checklist markers, then
  re-run `generate_mutations.py` and re-review. Until then it stays `candidate`.

## What is locked now

The **15 gold-consensus** cases (5 positive, 4 clean negative, all 5 boundary-pair orderings) are ready
for the blind eval matrix. The **5 queued** cases remain `candidate` and are **not** used as gold until
the user rules on Q-1/Q-2. No case was promoted to gold by overriding the reviewers.
