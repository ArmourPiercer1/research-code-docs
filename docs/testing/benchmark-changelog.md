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

### Addendum — Phase D.3 diagnostic close + one v0.4 text fix (2026-08-04)

- **Runaway averted, then re-run controlled.** The first D.3 attempt was a background Workflow that received
  `args` as a JSON **string** (not the array), iterated it character-by-character, and hit the 1000-agent cap
  after ~63M tokens / ~11h before failing. **No corpus/skill/result file was written by it** (evaluators are
  read-only; aggregation never ran). The D.3 reruns were then done as **7 controlled direct Agent calls** — no
  workflow, no loop, no runaway surface.
- **BP-006 pair + GP-EXP-001 results (v0.4):** `BP-006-release` → **BLOCK ×3** via HF-12A/HF-12E (HF-9
  correctly silent, frontmatter complete); `GP-EXP-001` → **ALLOW, files_checked=1** (the earlier
  `files_checked=0` stale-path bug is fixed). `BP-006-audit` first ran **3-way unstable** (BLOCK/ALLOW/
  INCOMPLETE) → root-caused to an **audit-mode gate-composition gap** (release-gate ALLOW preconditions
  leaking onto GATE_DECISION; see ledger **D-16**).
- **Fix (text-only, no threshold change):** made GATE_DECISION a deterministic 3-rule derivation in `SKILL.md`
  + EVALUATOR_CONTRACT; rubric total now gates QUALITY_BAND only; UNVERIFIED bars the green terminal gate but
  never moves the gate. Re-ran `BP-006-audit ×3` → **ALLOW ×3 / PARTIAL ×3**, stable. **Diagnostic closes at
  8/8.** Skill stays **0.4.0** (pre-admission hardening; disclosed, not auto-installed).
- **OQ-REPRO = A confirmed** by both blind A/B and the skill: no dedicated HF-REPRO gate is needed — a
  non-reproducible controlled release-gate doc BLOCKs on existing HF-12A/E, and its external+audit twin ALLOWs.
- Nothing installed, pushed, or auto-triggered this round.

### Addendum — candidate 0.4.1 + Phase E safety pre-flight (2026-08-05)

Driven by `docs/third-party-suggestions/DQE_D3决策与PhaseE安全准入计划.md` (`D16_DECISION=ACCEPT`,
`CANDIDATE_VERSION=0.4.1`, `PHASE_E=APPROVED_WITH_PRECONDITIONS`, `BACKGROUND_WORKFLOW_FOR_ADMISSION=FORBIDDEN`).
**No hard-gate threshold changed.** This entry is corpus/harness/governance only; the skill's *judging* logic
is byte-identical to the D-16 build (only the declared version string moved 0.4.0→0.4.1).

- **Candidate versioned 0.4.1** (D-16 is an observable behavior change, so it does not share 0.4.0's number).
  Synced: `SKILL.md`, `skills-registry.yaml` (was stale at 0.3.0 → 0.4.1, still `experimental`),
  `dqe-v0.4-skill-change-summary.md` + `dqe-v0.4-diagnostic-matrix.md` (immutable historical bodies + forward
  banners), `last_verified: 2026-08-05`.
- **Three hash-verified frozen bundles** under `evals/skills/snapshots/` (`scripts/build_skill_snapshots.py`):
  `dqe-v0.3.0` (git 279c0ce, single-axis), `dqe-v0.4.0-pre-d16` (git 14959a8, two-axis, no D-16),
  `dqe-v0.4.1-candidate` (working tree, D-16). v0.3 is extracted from **git history**, not rebuilt from memory.
  Each carries a `SNAPSHOT-MANIFEST.yaml` with per-file SHA-256; the checker layer is **held constant** across
  arms (recorded, not varied).
- **63M-token runaway → `HARNESS_ORCHESTRATION_FAILURE`** (see `reports/dqe-v0.4.1-diagnostic-close.md` §1).
  No corpus/skill/results were written by it. Structural fix: Phase E launches **only** from a static,
  pre-counted, hash-verified plan; a background Workflow is forbidden for admission.
- **New/updated tooling:** `scripts/build_skill_snapshots.py`, `scripts/make_phase_e_plan.py` (static plan),
  `scripts/validate_eval_plan.py` (aborts before the first agent on string-`runs`, dup run_key, >`MAX_EVAL_RUNS=64`,
  snapshot hash mismatch, non-gold case — adversarially tested); `aggregate_eval_results.py` gains
  `terminal_green` derivation (§3), `terminal_contract_mismatch_count`, `checker_execution_compliance`, and
  arm-aware scoring + comparison (backward-compatible single-arm mode); `make_grading_injection.py` gains an
  additive `--snapshot` read-path (frozen bundle injection) + `--role baseline` (no-skill arm). Live evaluator
  behavior with no `--snapshot` is unchanged.
- **Manifests:** BP-006-audit / BP-006-release gain `expected.terminal_green: false` (the unambiguous cases —
  reader FAIL / BLOCK). Manifest validator: 25 live, 0 errors.
- **Static Phase E plan** `tests/corpus/blind-runs/phase-e-2026-08-05/phase-e-plan.json`: **61 slots**
  (Arm A v0.4.1 = 25 live ×1 + 5 stability ×2 = 35; Arm B frozen-v0.3 = 13-case diagnostic subset ×1;
  Arm C no-skill = same 13 ×1). Expected ≈ 5.6M tokens; hard ceiling 7.0M. Validated 0 errors.
- Nothing installed, pushed, or auto-triggered. Skill stays `disable-model-invocation: true`, `experimental`;
  promotion to `provisional-gate` remains GATED on the Phase E admission bar (not yet run at time of writing).

### Addendum — Phase-2 routing eval datasets for A8/A9 (2026-09-10; DQE gold corpus UNCHANGED)

- **Added 4 routing-eval case files** (NOT DQE gold cases; the DQE test corpus is byte-unchanged — no
  `dataset_version` bump): `evals/skills/trigger/simplification-audit.yaml` + `evals/skills/conflict/
  simplification-audit.yaml` (A8) and `evals/skills/trigger/focused-verification.yaml` + `evals/skills/
  conflict/focused-verification.yaml` (A9) — 20 trigger + 5 conflict cases each, `dataset_version: 1`,
  `real: false` (authored datasets, not yet scored by a routing run — the skills stay
  `experimental` + `disable-model-invocation` until that run passes).
- Mutation history of these routing files = git (row 13: git is the chronology owner); this addendum
  exists for later regression attribution (score shifts → this data addition vs a skill change).


