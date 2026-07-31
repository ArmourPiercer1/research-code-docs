<!--
generated_by_skill: (manual, v0.4 test-upgrade)
skill_version: n/a
source_documents:
  - tests/corpus/blind-runs/adjudication-v4/ (blind inputs + .secret mapping)
  - docs/testing/corpus-repair-report-v4.md
status: FINAL — 4 gold locked, 2 disputes queued for user
last_verified: 2026-07-31
-->

# Adjudication v4 — two-axis blind Reviewer A/B on the repaired fixtures

## Method

Six repaired/new documents were copied to neutral, shuffled filenames (`doc-01`…`doc-06`) with the
class-name directory and case-id stripped; the id↔case mapping was kept in a `.secret/` sidecar the
reviewers cannot see. Two **independent, isolated** reviewer sub-agents (fresh context, **no** DQE skill /
hard-fail / rubric / manifest access) each judged all six on the two axes from ADR-DQE-001:
`QUALITY_BAND ∈ {PASS, PARTIAL, FAIL}` (holistic quality) and `GATE_RECOMMENDATION ∈ {ALLOW, BLOCK,
INCOMPLETE}` (release/merge gate). Both reviewers' `FILES_READ` confirmed only the six inputs were opened.
Gold is **not** inherited from any v1 case.

## Results

| blind | case | Reviewer A (quality / gate / tags / conf) | Reviewer B | outcome |
|---|---|---|---|---|
| doc-01 | BP-005-pass | PASS / ALLOW / [] / HIGH | PASS / ALLOW / [] / HIGH | **gold PASS/ALLOW** |
| doc-02 | GN-PROP-001 | PASS / ALLOW / [] / HIGH | PASS / ALLOW / [] / HIGH | **disputed** (vs corpus FAIL) |
| doc-03 | GN-ROADMAP-001 | PARTIAL / BLOCK / [non-executable-milestone, not-actionable] / MEDIUM | PARTIAL / BLOCK / [non-executable-milestone] / HIGH | **gold FAIL/BLOCK** |
| doc-04 | GN-EVIDENCE-BARE-CLAIM-001 | FAIL / BLOCK / [unsupported-claim, not-reproducible] / HIGH | FAIL / BLOCK / [unsupported-claim] / HIGH | **gold FAIL/BLOCK** |
| doc-05 | BP-002-fail | PARTIAL / BLOCK / [volatile-in-stable] / MEDIUM | PARTIAL / ALLOW / [volatile-in-stable] / MEDIUM | **disputed** (gate split) |
| doc-06 | GN-EXP-REPRO-001 | PARTIAL / BLOCK / [not-reproducible, context-dependent] / MEDIUM | FAIL / BLOCK / [not-reproducible] / HIGH | **gold FAIL/BLOCK** (gate consensus) |

## Locked gold (4)

- **BP-005-pass → PASS/ALLOW (HIGH).** Confirms the D-09 repair: an honestly-labeled hypothesis under
  `document_lifecycle: ACCEPTED` is high-quality and allowed.
- **GN-ROADMAP-001 → FAIL/BLOCK.** Both reviewers independently isolate Phase-1 (`committed · next`) as
  having no executable pass/fail gate — exactly the intended HF-15 defect.
- **GN-EVIDENCE-BARE-CLAIM-001 → FAIL/BLOCK (HIGH).** Both fail the bare 74% claim as unsupported; with
  complete front-matter neither raised a controlled-profile provenance gap.
- **GN-EXP-REPRO-001 → FAIL/BLOCK** (gate consensus; quality-band split PARTIAL/FAIL). Both block on
  non-reproducibility; under the external profile neither penalized the missing local front-matter.

## Disputes queued for the user (2) — NOT force-resolved

### D6 — GN-PROP-001: reviewers say PASS, corpus intended FAIL
Both reviewers rated the mutated KEP **PASS/ALLOW**. Their reasoning (independently): the Design Details
(CRI protobuf changes, ID-mapping algorithm, worked idmap examples, PRR questionnaire, failure modes,
alternatives) are complete enough to implement from, so removing Test Plan / Graduation Criteria /
Feature-Enablement reads as non-blocking *process scaffolding*, not an executability blocker. This is the
same failure mode as the quarantined GN-EXP-001 (D-04): the base is too rich to break with one deletion.
The unchanged v0.3 evaluator FAILs it, but on HF-9 (external-profile gap, D-01) + a residual
mutation-induced contradiction (Implementation-History "GA" vs the unchecked (R) checklist boxes) — not on
the intended defect. → **user decides**: (a) quarantine + rebuild on a leaner proposal; (b) override to
FAIL as in v1 D-1; (c) reclassify the intended defect.

### D7 — BP-002-fail: gate split
Both reviewers see the volatile-in-stable defect (a bare "当前 69 项测试全部通过" in a doc that declares
itself the stable/BASELINE design) and rate quality PARTIAL, but split on the gate: **A = BLOCK** (a
baseline reference must not carry a live count), **B = ALLOW** (architecture comprehension is intact; one
line does not block). The unchanged v0.3 evaluator fires HF-14b (BLOCK), agreeing with A + corpus intent.
→ **user decides**: does a single volatile-in-stable line BLOCK a baseline architecture doc (keep gold
FAIL), or is it a MINOR (soften to PASS/ALLOW)?

## Provenance

Blind inputs, mapping, evaluator injections, and raw outputs live under
`tests/corpus/blind-runs/adjudication-v4/`. The reviewer contract used is the two-axis REVIEWER_CONTRACT in
`evals/skills/harness/make_grading_injection.py` (reviewer role never loads the skill).
