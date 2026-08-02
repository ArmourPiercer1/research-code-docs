<!--
generated_by_skill: (manual, v0.4 Phase C — review aid)
skill_version: documentation-quality-evaluator 0.4.0
source_documents:
  - docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md (ACCEPTED)
  - docs/testing/DQE_v4_待决策项回复与下一阶段开发计划.md (Phase C scope)
status: for user review before the Phase E admission matrix
last_verified: 2026-08-02
-->

# DQE v0.4 skill-change summary (review guide)

Everything the v0.4 round changed in the **skill + harness**, file by file, with what to check. Scope was
deliberately **minimal** (ADR-DQE-001 + the plan's Phase C): profile-aware HF-9, two-axis verdict,
lifecycle vocabulary, HF-14b profile severity. **HF-12A and HF-15 logic are byte-unchanged; HF-13/HF-14a
keep their v0.3 thresholds** (only their contract *wording* was synced to the ADR). Validated by the
4-case sanity check + the 39-run diagnostic (7/8 metrics, stable 3/3; the 1 open item is a corpus-spec
question, not a skill bug — see `dqe-v0.4-oq-repro-decision.md`).

## Files changed

### 1. `.claude/skills/documentation-quality-evaluator/SKILL.md`  (skill definition)
- Version `0.3.0 → 0.4.0`; header note rewritten for v0.4.
- **Inputs:** new `evaluation_profile` (caller-supplied; `provenance_policy`/`decision_mode` **not**
  inferable; missing ⇒ `GATE_DECISION=INCOMPLETE`).
- **Workflow step 3:** profile-aware severity — HF-9 by `provenance_policy`, HF-14b by
  `provenance_policy + decision_mode`; INCOMPLETE for a missing required section; HF-12A/HF-15 explicitly
  unchanged.
- **Verdict block:** now two-axis — `QUALITY_BAND` + `GATE_DECISION` + `DOCUMENT_QUALITY` (compat map) +
  `EVALUATION_PROFILE` echo.
- **PASS condition + terminal-gate contract:** keyed to `GATE_DECISION=ALLOW` (was `DOCUMENT_QUALITY=PASS`).
- *Review:* confirm the two-axis + profile rules match ADR-DQE-001 §1/§3/Decision 6; confirm no HF-12A/15
  wording drift.

### 2. `evals/skills/harness/hard-fail.md`  (gate catalog)
- New v0.4 framing note (two axes; checker = raw finding, evaluator = profile-mapped severity).
- HF-9 row flagged profile-dependent + new **§HF-9 profile-aware severity** table
  (controlled BLOCKER / legacy MAJOR / external MINOR-NA; `document_lifecycle` satisfies the doc-level req).
- HF-14b row flagged + new **§HF-14b severity map** (Decision 6 / D-7): BLOCKER only under
  `controlled + release-gate` on a stable-canonical doc with a bare undated current fact + no pointer;
  full profile/mode table; regression triad noted.
- HF-14a: **"Does NOT fire on"** list synced (dangling TOC = link-integrity; lifecycle≠claim-status; etc.) —
  **no threshold change**.
- Applicability table: added a `technical-proposal` row (release-readiness → INCOMPLETE via rubric; no new
  hard gate).
- *Review:* confirm HF-13/HF-14a are **narrowed in wording only**, thresholds intact; confirm the HF-14b
  map matches the D-7 ruling.

### 3. `evals/skills/harness/checkers/frontmatter_check.py`  (HF-9 detector)
- The `status` requirement now also accepts `document_lifecycle` (a doc with `document_lifecycle: ACCEPTED`
  satisfies the doc-level requirement without a legacy `status:`). Detection stays a **raw finding**;
  severity is decided by the evaluator/profile, not the checker.
- *Review:* one-line change to the REQUIRED aliases; no other detection logic touched.

### 4. `evals/skills/harness/checkers/status_vocab_check.py`  (HF-3/HF-10 vocab)
- Added `DOC_LIFECYCLE = {DRAFT, IN_REVIEW, ACCEPTED, DEPRECATED}` and a check that a `document_lifecycle:`
  field carries a legal token. Claim-`STATUS` and skill-`LIFECYCLE` sets unchanged.
- *Review:* additive only; legacy `status:` values still validated exactly as before.

### 5. `evals/skills/harness/make_grading_injection.py`  (isolated-prompt builder — harness, not the skill)
- `EVALUATOR_CONTRACT` rewritten: profile-aware severity instructions + two-axis verdict keys +
  `EVALUATION_PROFILE` echo + INCOMPLETE-on-missing-profile.
- Evaluator branch now **injects the caller-supplied profile** (`--profile`, `--artifact-type`) into the
  prompt.
- `REVIEWER_CONTRACT` already two-axis (prior round).
- *Review:* confirm the evaluator now receives the profile; confirm the contract text mirrors SKILL.md.

### 6. `scripts/aggregate_eval_results.py`  (scorer — harness)
- Two-axis aware: gate falls back from `document_quality` when absent; negatives fail by being **ALLOWed**,
  positives by **not being ALLOWed**; boundary ordering + 3-run consistency on the **gate** axis; added
  **profile-echo compliance**. Backward-compatible with the old v0.3 raw-results.
- *Review:* the §17 bar now has 8 checks (added profile compliance).

### 7. `scripts/gen_eval_injections.py`  (NEW — runner support)
- Generates per-case evaluator injections with each case's profile (reads the manifest). Used to build the
  diagnostic matrix inputs.

## Corpus manifests touched for v0.4 (not skill behavior)
- Added `decision_mode` to the 9 diagnostic manifests that lacked it (external→audit, controlled→release-gate).
- Repaired fixtures already migrated to `document_lifecycle` in the earlier round.

## Explicitly NOT changed (byte-frozen)
- HF-12A and HF-15 model logic (SKILL.md + hard-fail.md wording untouched for these).
- HF-13 / HF-14a detection thresholds and the checkers' core detection logic.
- The v0.3 blind-matrix results and reports (immutable baseline).

## How to review quickly
1. Read the ADR (`ADR-DQE-001-…md`, ACCEPTED) — it is the spec these changes implement.
2. Skim SKILL.md §Inputs + §"Structured verdict block" + workflow step 3 (the behavioral core).
3. Skim hard-fail.md §HF-9 + §HF-14b severity map.
4. Spot-check the 4 sanity results (`tests/corpus/blind-runs/v04-sanity/`) and the diagnostic report
   (`dqe-v0.4-diagnostic-matrix.md`) — they show the changes producing correct, stable behavior.

Nothing here has been installed into the live loader or pushed anywhere; the skill remains
`disable-model-invocation: true`, `experimental`, manual-only.
