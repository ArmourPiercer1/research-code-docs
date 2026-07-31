<!--
generated_by_skill: (manual, v0.4 test-upgrade)
skill_version_under_test: documentation-quality-evaluator 0.3.0 (UNCHANGED — no skill file was modified)
corpus: dataset_version 4
source_documents:
  - docs/skill-development/reports/dqe-v0.4-defect-ledger.md
  - docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md
  - docs/third-party-suggestions/DQE_v0.4_测试修正与最小升级计划.md
  - tests/corpus/blind-runs/adjudication-v4/ (blind inputs, two-axis A/B, evaluator spot-check)
status: FINAL — corpus repaired + re-adjudicated; skill unchanged; 2 items queued for user
last_verified: 2026-07-31
-->

# DQE v0.4 corpus-repair report (test upgrade — skill untouched)

## 0. TL;DR

Per the third-party plan's principle — *a test must first prove it caught the target defect before it can
demand a skill change* — this round only touched the **test side**: quarantined the 5 contaminated cases,
repaired/split them into clean v2 fixtures, upgraded the mutation tooling with semantic post-conditions +
a new semantic validator, re-adjudicated with **two-axis** blind Reviewer A/B, and ran a **confirmatory
spot-check** with the **unchanged v0.3 evaluator**. No skill file was modified.

**The decisive result:** running the unchanged v0.3 skill on the *repaired* fixtures shows that **most of
the original "skill failures" were corpus defects.** Of the four skill fixes the earlier report proposed
(F1–F4), the evidence now justifies **only F1 (HF-9 profile-gating)**:

- **HF-15 recall** (F3) — *fine*. The v1 miss was a mutation that never removed the measurable gate; the
  clean v2 fires HF-15.
- **HF-12A recall** (F2) — *fine*. The v1 miss was a mutation that kept the hyperparameters; a clean bare
  claim fires HF-12A.
- **HF-13 / HF-14a over-firing** (F4) — *did not reproduce*. On the de-contaminated BP-002-fail v2 the
  evaluator fires only HF-14b; HF-13/HF-14a stay silent.
- **HF-9 not profile-aware** (F1) — *confirmed skill defect*. It still hard-fails the two external docs.

Two items are **queued for your decision** (§5): GN-PROP-001 (both reviewers say the mutated KEP is still
PASS-worthy → likely an invalid negative) and BP-002-fail's gate (reviewers split ALLOW/BLOCK).

## 1. What changed (all test-side)

- **Quarantined (immutable v1 snapshots)** under `tests/corpus/cases/quarantine/<id>-v1/` +
  `QUARANTINE.yaml`: GN-EXP-001, GN-ROADMAP-001, BP-002-fail, BP-005-pass, GN-PROP-001. Validators skip
  `**/quarantine/**`, so they never enter a live metric.
- **Repaired / split (v2):**
  - **GN-EXP-001 → split** into `GN-EVIDENCE-BARE-CLAIM-001` (pure HF-12A) + `GN-EXP-REPRO-001`
    (reproducibility). The v1 was too weak (kept the full `python train.py` command + hyperparameters).
  - **GN-ROADMAP-001 v2** — the whole Phase-1 GO/MODIFY/STOP gate + downstream route is now truly removed
    (v1's regex missed the dash-prefixed `- **GO:**`). Phase-2's gate is asserted to survive.
  - **GN-PROP-001 v2** — the removed sections' `<!-- toc -->` anchors are removed too (no dangling nav).
  - **BP-002-fail v2** — the incidental `status: DECIDED` + "core is done" vs "design review in progress"
    contradiction removed; the bare live count (the sole HF-14b) kept.
  - **BP-005-pass v2** — `status: DECIDED` → `document_lifecycle: ACCEPTED` + `status: OPEN` (an accepted
    note may record an unverified hypothesis).
- **Tooling:** `generate_mutations.py` gained `postconditions:{assert_absent, assert_present}` (aborts if
  the target defect did not land); new `scripts/validate_mutation_semantics.py` (dangling-TOC resolution,
  retired-`DECIDED`+unverified co-occurrence, mutation post-condition re-check, same-byte-different-profile
  SHA equality); `validate_case_manifests.py` learns `case_version` / two-axis fields / quarantine-skip;
  `make_grading_injection.py` REVIEWER_CONTRACT now emits two axes. **EVALUATOR_CONTRACT unchanged.**
- **Contract:** `ADR-DQE-001` (PROPOSED) defines evaluation_profile / provenance_policy /
  QUALITY_BAND vs GATE_DECISION / document_lifecycle vs claim-status / reproducibility findings — the
  corpus is aligned to it now; **skill implementation is deferred.**

## 2. Deterministic gates (all green)

```
generate_mutations.py GN-ROADMAP-001 GN-PROP-001 GN-EXP-REPRO-001   # 3/3, postconditions PASS
validate_mutation_semantics.py tests/corpus/cases                   # 0 errors (8 WARN = retired status: on out-of-scope fixtures)
validate_case_manifests.py    tests/corpus/cases                    # 0 errors; 21 live ids; 5 pairs; 5 quarantined skipped
```

The semantic validator's pre-repair run flagged exactly the two defects we then fixed (11 dangling TOC
anchors in GN-PROP-001; `DECIDED`+HYPOTHESIS in BP-005-pass) and cleared after repair — i.e. the tooling
catches the class of bug that shipped the v1 corpus (defect-ledger D-12).

## 3. Two-axis blind re-adjudication (Reviewer A/B, no DQE skill)

Two isolated reviewers judged the six repaired docs blind (neutral filenames, class/id stripped;
`FILES_READ` confirmed only the six inputs were opened). Both emit `QUALITY_BAND` + `GATE_RECOMMENDATION`.

| case | Rev A | Rev B | gold |
|---|---|---|---|
| BP-005-pass | PASS / ALLOW | PASS / ALLOW | **gold PASS** |
| GN-ROADMAP-001 | PARTIAL / BLOCK | PARTIAL / BLOCK | **gold FAIL** (both cite Phase-1 non-executable = HF-15) |
| GN-EVIDENCE-BARE-CLAIM-001 | FAIL / BLOCK | FAIL / BLOCK | **gold FAIL** |
| GN-EXP-REPRO-001 | PARTIAL / BLOCK | FAIL / BLOCK | **gold FAIL** (gate consensus; quality-band split) |
| GN-PROP-001 | PASS / ALLOW | PASS / ALLOW | **DISPUTED** — contradicts corpus FAIL → user |
| BP-002-fail | PARTIAL / BLOCK | PARTIAL / ALLOW | **DISPUTED** — gate split → user |

Gold is **not** inherited from v1 (each repaired case is `case_version` bumped / new). Disputes are queued,
not force-resolved.

## 4. Confirmatory spot-check — unchanged v0.3 evaluator on the repaired fixtures

Six isolated evaluators loaded the **frozen v0.3 skill** (via `make_grading_injection.py --role evaluator`),
ran `run_checks.py`, walked HF-1..15, and emitted the verdict. This answers, per case, *"was the original
failure the fixture or the skill?"*

| case | v0.3 verdict | v0.3 blockers | expected | attribution |
|---|---|---|---|---|
| **BP-005-pass v2** | PASS | `[]` | PASS | 🟢 **fixture-fix confirmed** — v1 false-FAILed [HF-3,HF-14a]; the honest hypothesis now passes. **D-09 was 100% fixture.** |
| **GN-ROADMAP-001 v2** | FAIL | `[HF-15]` | FAIL (HF-15) | 🟢 **fixture-fix confirmed** — the evaluator fires HF-15 and explicitly contrasts un-gated Phase 1 vs still-gated Phase 2. **HF-15 recall was never broken (F3 unneeded).** |
| **GN-EVIDENCE-BARE-CLAIM-001** | FAIL | `[HF-12A, HF-12E, HF-10]` | FAIL (HF-12A) | 🟢 **HF-12A recall works** on a clean bare claim; HF-12E/HF-10 are legitimate co-findings; **no forbidden violation. F2 unneeded.** |
| **BP-002-fail v2** | FAIL | `[HF-14b]` | FAIL (HF-14b; forbid HF-13/14a/15) | 🟢 **fixture-fix confirmed** — only HF-14b; **HF-13 and HF-14a NO LONGER fire** on the clean single-defect doc. **The v1 over-fire was fixture-amplified (F4 unneeded).** |
| **GN-EXP-REPRO-001** | FAIL | `[HF-9, HF-12A, HF-12E]` | FAIL (findings; forbid HF-13/14a/14b/15) | 🟢 reproducibility blocks; **no forbidden over-fire.** `HF-9` = 🔴 **D-01** (external doc, profile gap). |
| **GN-PROP-001 v2** | FAIL | `[HF-9, HF-14a, HF-12E]` | disputed | ⚠️ `HF-9` = 🔴 D-01; `HF-14a` = a **new residual contradiction** the mutation created ("1.36 GA" vs unchecked (R) Test-plan/Graduation boxes), not the old TOC misread. Reviewers say PASS → **invalid negative (D-13).** |

### 4.1 The one surviving skill defect — D-01 (HF-9 not profile-aware) 🔴
HF-9 fired as a blocker on **both** external documents (`GN-PROP-001`, `GN-EXP-REPRO-001`) that
legitimately carry no local traceability front-matter. Per ADR-DQE-001, `external ⇒ HF-9 is MINOR/NA`.
This is the single, cleanly-reproduced skill defect and the only justified skill change (F1). It stays
**deferred** to a separately-approved skill pass; this round produced its regression fixtures (BP-004 pair
already exists; the two external negatives here add witnesses).

### 4.2 What the spot-check retired
- **F2 (HF-12A recall)** and **F3 (HF-15 recall)** — the clean fixtures fire both gates. The v1 "misses"
  were mutations that never carried the defect. **No skill change.**
- **F4 (HF-13/HF-14a tightening)** — on the clean BP-002-fail v2, neither over-fires. The v1 violations
  were fixture contradictions. **No skill change justified by current evidence.**

## 5. Queued for your decision

- **D6 — GN-PROP-001 validity.** Both blind reviewers rate the mutated KEP PASS/ALLOW; its v0.3 FAIL comes
  from HF-9 (profile) + a residual mutation-induced contradiction, not the intended "no validation story".
  The KEP base is too implementation-complete to fail by one deletion (same failure mode as GN-EXP-001).
  **Options:** (a) quarantine + rebuild on a leaner proposal where removing the test plan truly breaks
  executability; (b) override to FAIL as in v1's D-1; (c) reclassify its intended defect.
- **D7 — BP-002-fail gate.** Reviewers agree the volatile-in-stable defect exists (PARTIAL quality) but
  split on the gate (A BLOCK / B ALLOW). v0.3 fires HF-14b (BLOCK). **Decide:** does a single
  volatile-in-stable line BLOCK a baseline architecture doc (keep gold FAIL), or is it a MINOR (soften)?

## 6. Corpus state after this round

- **Live cases: 21** — 5 golden-positive, 6 golden-negative (GN-ADR-001/002, GN-PROP-001[disputed],
  GN-ROADMAP-001, GN-EVIDENCE-BARE-CLAIM-001, GN-EXP-REPRO-001), 10 boundary (5 pairs).
- **Gold locked this round: 4** (BP-005-pass, GN-ROADMAP-001, GN-EVIDENCE-BARE-CLAIM-001, GN-EXP-REPRO-001).
- **Disputed (excluded from metrics until ruled): 2** (GN-PROP-001, BP-002-fail).
- **Quarantined (archived, immutable): 5 v1 snapshots.**
- **Skill: unchanged.** Nothing installed, pushed, or auto-triggered.

## 7. Next (after your D6/D7 ruling) — the v0.4 skill round, separately approved

1. Resolve D6/D7; if GN-PROP-001 is rebuilt, re-adjudicate it.
2. **Skill:** implement **only F1 (HF-9 profile-gating)** per ADR-DQE-001; reconcile the document_lifecycle
   vocab (D-14). Do **not** touch HF-12A/HF-15/HF-13/HF-14a — the evidence says they are fine.
3. Run the diagnostic matrix, then the full admission matrix + a baseline-no-skill arm; only then consider
   `experimental → provisional-gate`.
