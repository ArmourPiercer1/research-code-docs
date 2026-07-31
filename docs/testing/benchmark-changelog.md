<!--
generated_by_skill: (manual, Phase-1 test-corpus governance authoring)
skill_version: n/a
source_commit: upstream seeds pinned in tests/corpus/upstream/UPSTREAM-COMMITS.tsv
source_documents: [docs/testing/corpus-policy.md, docs/testing/adjudication-protocol.md]
status: LIVING (append-only changelog)
last_verified: 2026-07-31
-->

# Benchmark Changelog — DQE test corpus

Append-only. Each entry records what changed in the corpus, so a later regression can attribute a score
shift to a data change vs an evaluator change. `dataset_version` is bumped on every entry.

## dataset_version 3 — 2026-07-31 — first real-seed corpus build (rounds A–F)

- **Added seed layer** `tests/corpus/` from 12 manually-cloned upstream repos (SHAs pinned in
  `upstream/UPSTREAM-COMMITS.tsv`). Register: `source-seeds/seed-register.yaml`.
- **Quarantined** `mozilla-sre-adrs` (no license) → reference only, no body copied.
- **Cases targeted:** 5 golden-positive (GP-ADR-001, GP-PROP-001, GP-PROP-002, GP-EXP-001,
  GP-ROADMAP-001), 5 golden-negative (GN-ADR-001, GN-ADR-002, GN-PROP-001, GN-EXP-001, GN-ROADMAP-001),
  5 boundary-pairs (BP-001..BP-005). The 6 pre-existing v0.3 fixtures (`messy-hybrid-roadmap`,
  `p1-lightweight-roadmap`, `b2-research-roadmap`, `b1/b4/b5`) are **re-homed by reference**, not moved.
- **Manifests** gain `forbidden_blockers` (anti-over-firing) + `adjudication` blocks.
- **Scripts** added under `scripts/`; `evals/skills/harness/score_grading.py` extended with
  forbidden-blocker-violation + boundary-ordering; `make_grading_injection.py` gains `--role reviewer`.
- **Not yet done (next round):** the blind eval matrix (baseline / v0.3 / v0.2 / repeat×3) and the
  `experimental → provisional-gate` promotion.

> Predecessor: `evals/skills/task-quality/documentation-quality-evaluator.yaml` was `dataset_version: 2`
> (the v0.3 inline anchor + 6 fixtures). This corpus supersedes it as the authoritative gold source
> while keeping those fixtures byte-for-byte as regression anchors.

### Addendum — blind eval matrix run (2026-07-31)

- Ran the 26-run matrix (v0.3 × 20 + 3 stability × 2) via a background workflow (26/26 agents, 0 errors,
  ~2.6M tokens). Raw: `tests/corpus/blind-runs/matrix-2026-07-31/raw-results.json`; metrics + summary +
  regression report under `evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/`.
- **§17 promotion bar NOT MET (all 7 metrics).** DQE v0.3 stays `experimental`. The matrix surfaced:
  HF-9 not profile-aware (false-fails external docs — the top defect), HF-12A + HF-15 recall gaps (2
  golden-negatives false-PASSed), HF-13/HF-14a over-firing (forbidden violations), and instability
  (2/3 stability cases inconsistent). Plus 2 fixture ambiguities to clean (BP-005-pass / BP-002-fail
  both use a `status: DECIDED` over-claim). Full analysis + recommended v0.4 fixes in the regression
  report. No skill or fixture changed this round.

- Reviewer A/B (isolated, no DQE skill) agreed **20/20** on verdict and primary defect tag.
- User rulings: **D-1=A** (single-defect negatives keep gold **FAIL** — reviewer PARTIAL preserved in
  each manifest's adjudication block), **D-2=A** (`GN-PROP-001` mutation refined so the signoff checklist
  is unchecked to match the removed sections; re-confirmed `CONTRADICTION=NO`), **D-3=A** (`BP-001-fail`
  count fixed 69→**78** of 94, isolating HF-13), **D-5=A** (a `PARTIAL/CONDITIONAL_PASS` verdict tier is
  deferred to v0.4+).
- Result: **20/20 gold, 0 queued**; `validate_case_manifests.py` = 0 errors. Corpus ready for the blind
  eval matrix. New op `replace-text` added to `generate_mutations.py`; `apply_adjudication.py` gained a
  `user_decision` override path.

## dataset_version 4 — 2026-07-31 — v0.4 test upgrade (repair, not skill change)

Test-side upgrade driven by `docs/third-party-suggestions/DQE_v0.4_测试修正与最小升级计划.md` + the §4X
re-check. **No skill file was modified** (SKILL.md / hard-fail.md / rubric.md / checkers all byte-frozen).

- **Quarantined** 5 contaminated v1 cases → `tests/corpus/cases/quarantine/<id>-v1/` (immutable snapshots +
  `QUARANTINE.yaml`): GN-EXP-001, GN-ROADMAP-001, BP-002-fail, BP-005-pass, GN-PROP-001. Validators now
  skip `**/quarantine/**`, excluding them from every live metric.
- **Repaired / split (case_version 2 / new ids):**
  - GN-EXP-001 **split** → `GN-EVIDENCE-BARE-CLAIM-001` (pure HF-12A) + `GN-EXP-REPRO-001` (reproducibility).
  - `GN-ROADMAP-001 v2` — Phase-1 GO/MODIFY/STOP gate + downstream route truly removed (v1 regex missed the
    dash-prefixed `- **GO:**`); Phase-2 gate asserted intact.
  - `GN-PROP-001 v2` — removed sections' `<!-- toc -->` anchors removed (no dangling nav).
  - `BP-002-fail v2` — incidental `status: DECIDED`/"core is done" contradiction removed; bare HF-14b count
    kept.
  - `BP-005-pass v2` — `status: DECIDED` → `document_lifecycle: ACCEPTED` + `status: OPEN`.
- **Tooling:** `generate_mutations.py` +`postconditions` (assert_absent/present, aborts if the defect did
  not land); NEW `scripts/validate_mutation_semantics.py` (dangling-TOC, retired-DECIDED+unverified,
  post-condition re-check, profile-pair SHA); `validate_case_manifests.py` +case_version/two-axis/quarantine
  skip; `aggregate_eval_results.py` +quarantine skip; `make_grading_injection.py` REVIEWER_CONTRACT → two
  axes (EVALUATOR_CONTRACT unchanged).
- **Contract:** `ADR-DQE-001` (PROPOSED) — evaluation_profile / provenance_policy / QUALITY_BAND vs
  GATE_DECISION / document_lifecycle vs claim-status / reproducibility findings. Corpus aligned now; skill
  impl deferred. Manifests gain additive `expected.quality_band` / `expected.gate_decision`.
- **Deterministic gates:** generate 3/3 postconditions PASS; semantic-validator 0 errors; manifest-validator
  0 errors (21 live ids, 5 pairs, 5 quarantined skipped).
- **Re-adjudication (two-axis blind A/B):** 4 gold locked (BP-005-pass PASS; GN-ROADMAP-001,
  GN-EVIDENCE-BARE-CLAIM-001, GN-EXP-REPRO-001 FAIL); **2 disputed → user** (GN-PROP-001 both-PASS vs corpus
  FAIL; BP-002-fail gate split). Gold not inherited from v1.
- **Confirmatory spot-check (unchanged v0.3 evaluator on repaired fixtures):** BP-005-pass→PASS[];
  GN-ROADMAP-001→FAIL[HF-15]; GN-EVIDENCE-BARE-CLAIM-001→FAIL[HF-12A,HF-12E,HF-10]; BP-002-fail→FAIL[HF-14b];
  GN-EXP-REPRO-001→FAIL[HF-9,HF-12A,HF-12E]; GN-PROP-001→FAIL[HF-9,HF-14a,HF-12E]. **Conclusion: of the
  report's F1–F4 skill fixes, only F1 (HF-9 profile-gating) is justified** — HF-12A/HF-15 recall are fine
  (fixture defects), HF-13/HF-14a did not over-fire on the clean fixture. Full analysis:
  `docs/testing/corpus-repair-report-v4.md`, `docs/skill-development/reports/dqe-v0.4-defect-ledger.md`.
- Nothing installed, pushed, or auto-triggered.

