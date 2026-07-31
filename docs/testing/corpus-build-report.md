<!--
generated_by_skill: (manual, Phase-1 DQE corpus build, rounds A–F + reviewer G)
skill_version: n/a (corpus dataset_version 3)
source_commit: upstream seeds pinned in tests/corpus/upstream/UPSTREAM-COMMITS.tsv
source_documents:
  - docs/documentation-quality-evaluator_测试语料自动准备与评测流程.md (the spec this round executes)
  - docs/testing/{corpus-policy,adjudication-protocol,benchmark-changelog}.md
status: DELIVERED (rounds A–F + reviewer initial pass); blind eval matrix is the NEXT round
last_verified: 2026-07-31
-->

# DQE Test-Corpus Build Report — round 1 (2026-07-31)

Executes the "测试前的准备工作" (rounds **A–F** + reviewer initial pass **G**) of the eval-flow spec,
folded into the existing `evals/skills/` harness. Nothing was installed, pushed, or auto-triggered; no
upstream content was modified.

## 1. What was built (all green)

| Layer | Result |
|---|---|
| Provenance | `tests/corpus/upstream/UPSTREAM-COMMITS.tsv` — 12 repos, real commit SHAs |
| Seed register | `source-seeds/seed-register.yaml` — **14 seeds** (repo+commit+path+**SHA-256**+license) |
| Immutable snapshots | `source-seeds/original/` — 14 records, **14/14 SHA-256 verified**; quarantine bodyless |
| Normalized inputs | `source-seeds/normalized/` — 4 case inputs (CRLF→LF; PEP kept as `.rst`, tool=none) |
| Mutation layer | `mutations/mutation-catalog.yaml` + 5 plans + `generate_mutations.py` (diffs + invariants) |
| Cases | **20 manifests** = 5 golden-positive + 5 golden-negative + 5 boundary-pairs (10) |
| Manifests | each carries `required_blockers` **and** `forbidden_blockers` (anti-over-firing) + adjudication |
| Scripts | `scripts/`: snapshot / normalize / generate_mutations / validate / build_blind_suite / apply_adjudication (+ harness: `score_grading` extended, `make_grading_injection --role reviewer` added) |
| Governance | `docs/testing/`: corpus-policy · adjudication-protocol · benchmark-changelog · this report |

Deterministic gates: `snapshot_sources.py --check` = 14/14 OK · `validate_case_manifests.py` = **0 errors,
0 warnings**.

## 2. Seeds & licensing (real upstream, on-disk)

10 upstream repos (12 dirs; 2 are sparse stubs whose content lives under differently-named full clones —
KEP→`enhancements/`, PEP→`peps/`). Licenses: Apache-2.0 (backstage, k8s-enhancements, llm-d, open-design),
MIT/dual (yahoo, madr MIT∨CC0, rust Apache∨MIT), public-domain/CC0 (peps), BSD-style+ACM (artifact-eval).
**`mozilla-sre-adrs` has NO license → QUARANTINED**: registered for reference, **body never copied**
(verified: its `original/` dir holds only `SOURCE.yaml` + `LICENSE-REFERENCE.txt`).

## 3. Cases (5 + 5 + 5)

- **Positives** (candidate→gold after review): GP-ADR-001 (Backstage ADR-002), GP-PROP-001 (KEP-127),
  GP-PROP-002 (**PEP-2026, Status=Rejected**), GP-EXP-001 (Yahoo ResNet recipe), GP-ROADMAP-001 (re-homed
  `b2` research roadmap).
- **Negatives** (single-defect mutations, verified diff + forbidden-section invariants): GN-ADR-001
  (rationale removed), GN-ADR-002 (runbook/live-state appended → HF-13), GN-PROP-001 (test-plan/graduation
  removed), GN-EXP-001 (provenance redacted → HF-12A), GN-ROADMAP-001 (measurable DoD→"届时定" → HF-15).
- **Boundary pairs** (differ by one condition): BP-001 HF-13 escape · BP-002 HF-14b (frozen snapshot vs
  bare count) · BP-003 HF-15 research escape · BP-004 external-vs-controlled HF-9 (same bytes, two
  profiles) · BP-005 HF-12E (labeled hypothesis vs bare "VERIFIED").

The 6 pre-existing v0.3 fixtures were **re-homed by reference**, not moved (regression anchors intact).

## 4. Reviewer A/B adjudication (the informative part)

Two **isolated** sub-agents (no DQE skill / hard-fail / rubric) each reviewed all 20 blind inputs.
**Verdict agreement A vs B = 20/20; primary-defect-tag agreement = 20/20.** →

- **15 gold-consensus** (A=B=intended): all 5 positives, the 4 clean negatives, and **all 5 boundary-pair
  orderings correct**. Notably GP-PROP-002 passed *despite* Status=Rejected, and GP-ROADMAP-001 passed
  (HF-15 research-escape held).
- **5 queued for USER decision** — see `adjudication-2026-07-31.md`. Both reviewers rated each
  single-defect negative **PARTIAL** where the corpus intends **FAIL** (holistic severity vs the DQE's
  non-compensatory "a met gate is a non-downgradeable BLOCKER" contract). Plus one data-quality find:
  **GN-PROP-001's mutation left the KEP signoff checklist claiming the removed sections are "in place"**
  → refine or demote per policy §6.3.

## 5. Pipeline spot-verify (one gold case, real DQE)

`build_blind_suite → DQE evaluator (isolated sub-agent) → score_grading --manifest` on **BP-001-fail**:
evaluator returned `DOCUMENT_QUALITY=FAIL, BLOCKERS=[HF-13,HF-14a,HF-14b]`, **correctly did NOT fire the
forbidden HF-15**, ran the checkers, and stayed read-only/isolated. Scorer: **recall 1.00, forbidden
violation none, false_pass 0 → evaluator PASS for this case**. (Also surfaced a genuine 78-vs-69 count
contradiction inside the BP-001-fail fixture — a minor impurity to optionally clean, like GN-PROP-001.)

## 6. Decisions (resolved 2026-07-31) + remaining

Ruled by the user via [decisions-pending-2026-07-31.md](decisions-pending-2026-07-31.md):
- **D-1=A** — the 4 single-defect negatives keep gold **FAIL** (reviewer PARTIAL preserved in each
  manifest). **D-2=A** — `GN-PROP-001` mutation refined (signoff checklist unchecked to match removed
  sections; re-confirmed no contradiction). **D-3=A** — `BP-001-fail` count fixed (78/94), isolating
  HF-13. **D-5=A** — a `PARTIAL/CONDITIONAL_PASS` verdict tier is deferred to v0.4+.
- Result: **20/20 gold, 0 queued.**
- **Remaining — D-4 (your optional spot-check):** governance §9.4 asks you to sample ≥1 case per type +
  any public doc whose "is-this-a-positive" call you want to confirm. Document paths are in the decision
  brief's §3 D-4 and were provided in chat. Not a blocker for the next round.

## 7. Explicitly NOT done (next round = "the test")

The blind eval matrix (baseline-no-skill / v0.3 / v0.2 / repeat×3), `metrics.json`,
`evaluation-summary.md`, `regression-report.md`, and the `experimental → provisional-gate` promotion.
The corpus + harness are now ready to run it: `build_blind_suite.py` → per-case
`make_grading_injection.py --role evaluator` → `score_grading.py --manifest`.
