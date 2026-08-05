<!--
generated_by_skill: (manual, v0.4 test-upgrade authoring)
skill_version_under_test: documentation-quality-evaluator 0.3.0 (UNCHANGED this round)
corpus: dataset_version 3 -> 4 (test-upgrade in progress)
source_documents:
  - docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md (§4, §4X)
  - docs/third-party-suggestions/DQE_v0.4_测试修正与最小升级计划.md (§3, §4.2)
  - evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/{metrics.json,regression-report.md}
status: LIVING (defect ledger; entries move OPEN -> IMPLEMENTED -> VERIFIED)
last_verified: 2026-07-31
-->

# DQE v0.4 Defect Ledger

Every defect the 2026-07-31 blind matrix surfaced, categorized so a later change can be attributed to a
**data** fix vs a **skill** fix vs a **contract** decision vs a **harness** fix. This replaces the
un-actionable "test-vs-skill is 50/50" framing with a per-defect classification.

**Scope of THIS round (test upgrade):** implement every `FIXTURE`, `CONTRACT`, and `HARNESS` entry.
**Do NOT** touch the skill — every `SKILL` entry stays `OPEN (deferred to v0.4 skill round)` and is only
implemented after the user approves a separate skill pass. A `SKILL` entry may not be implemented until
its corrected fixture is validated and the unchanged v0.3 evaluator *still* mis-judges it (see the
confirmatory spot-check in `docs/testing/corpus-repair-report-v4.md`).

## Baseline freeze (replaces a git tag — this workspace is not a git repo)

The following v0.3 artifacts are the **immutable baseline** for this upgrade. They are read-only; nothing
in this round overwrites them. A repaired case is a new `case_version`/new archive, never an edit of a
baseline result.

| Frozen artifact | Path |
|---|---|
| Blind-matrix raw verdicts (26 runs) | `tests/corpus/blind-runs/matrix-2026-07-31/raw-results.json` |
| Metrics + summary + regression report | `evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/` |
| Investigation report (method + §4X) | `docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md` |
| Skill under test (byte-frozen this round) | `.claude/skills/documentation-quality-evaluator/SKILL.md`, `evals/skills/harness/{hard-fail,rubric,canonical-source-map}.md`, `evals/skills/harness/checkers/**` |
| v1 fixtures being replaced | archived to `tests/corpus/cases/quarantine/<id>-v1/` (immutable copies) |

## Ledger

Legend — **category**: `SKILL` (evaluator logic) · `FIXTURE` (corpus content/mutation) · `CONTRACT`
(undefined evaluator input/output semantics) · `HARNESS` (test tooling). **status**: `OPEN` /
`IMPLEMENTED` / `VERIFIED` / `REJECTED` / `DEFERRED`.

---

### D-01 — HF-9 not profile-aware
- **category:** SKILL
- **evidence:** `BP-004-external`→FAIL[HF-9] though byte-identical to `BP-004-controlled` (only profile
  differs); `GP-EXP-001`→FAIL[HF-9]; `GP-PROP-002` repeat-2→FAIL[HF-9] (sole stability break). The
  BP-004 controlled/external pair is a same-byte control that isolates this cleanly.
- **affected_cases:** BP-004-external, GP-EXP-001, GP-PROP-002
- **decision:** Real skill capability gap (design required profile-awareness; v0.3 never implemented it).
  It is a **feature add**, not a regression. Highest-leverage fix (F1).
- **planned_change:** `frontmatter_check.py` emits a raw finding; final severity decided by
  `provenance_policy` (external⇒MINOR/NA, legacy⇒MAJOR, controlled⇒BLOCKER). Contract defined in
  ADR-DQE-001; **skill code change deferred**.
- **regression_cases:** BP-004-external (must PASS), BP-004-controlled (must FAIL[HF-9]), GP-EXP-001,
  GP-PROP-002 ×3.
- **status:** OPEN (deferred to v0.4 skill round)

### D-02 — HF-13 over-fires on a single architecture doc
- **category:** SKILL
- **evidence:** `BP-002-fail`→fired HF-13 (a forbidden blocker): a single architecture doc carrying one
  maturity snapshot is not a ≥2-role mixed-responsibility document.
- **affected_cases:** BP-002-fail
- **decision:** Real skill over-classification (F4, HF-13 half). Note this is *partly* entangled with the
  contaminated BP-002-fail fixture (see D-07); the confirmatory spot-check on **BP-002-fail v2** (clean
  single-defect) determines whether HF-13 still over-fires. If it does → confirmed SKILL.
- **planned_change:** HF-13 requires ≥2 body-level roles with distinct canonical sources + update
  frequencies + observable harm (per ADR-DQE-001 §HF-13 tightening). **Skill change deferred**; this
  round only produces the clean regression fixture that proves/【dis】proves it.
- **regression_cases:** BP-002-fail v2 (HF-13 must NOT fire)
- **status:** OPEN (deferred to v0.4 skill round; awaiting v2 spot-check evidence)

### D-03 — HF-14a misclassifies a dangling TOC / metadata gap as a state contradiction
- **category:** SKILL (entangled with FIXTURE D-08)
- **evidence:** `GN-PROP-001`→fired HF-14a (forbidden): after sections were removed the TOC still listed
  their anchors; the evaluator read the dangling nav as a contradiction. `BP-002-fail`→HF-14a also fired
  but there the fixture had a *real* contradiction (D-07), so that instance is fixture-caused.
- **affected_cases:** GN-PROP-001 (skill-side), BP-002-fail (fixture-side)
- **decision:** HF-14a must be limited to two incompatible assertions about the **same state variable /
  same scope / same time**. A dangling TOC entry is link/nav integrity, not a state contradiction. Skill
  half of F4.
- **planned_change:** Per ADR-DQE-001 §HF-14a tightening. **Skill change deferred**; this round removes
  the dangling TOC from GN-PROP-001 v2 so the case no longer *invites* the misfire, and the spot-check
  reveals whether HF-14a still fires on the clean v2 (→ confirmed SKILL) or not (→ was fixture-induced).
- **regression_cases:** GN-PROP-001 v2 (HF-14a must NOT fire)
- **status:** OPEN (deferred to v0.4 skill round; awaiting v2 spot-check evidence)

### D-04 — HF-12A recall unproven (golden-negative false-PASSed, but mutation too weak)
- **category:** FIXTURE (may escalate to SKILL only after repair)
- **evidence:** `GN-EXP-001`→PASS (missed HF-12A). But §4X re-check: the mutation deleted commits/versions
  yet **kept** the full `python train.py` command + all hyperparameters + LR schedule, so the method is
  still largely followable. The "74% with no commit" claim is a far weaker HF-12A than intended — the
  PASS is defensible. The fixture did not cleanly carry the target defect.
- **affected_cases:** GN-EXP-001
- **decision:** Do NOT change HF-12A yet. Repair the corpus first: split into (a) a pure bare-claim case
  and (b) a reproducibility case. Only if v0.3 still misses HF-12A on the **clean** bare-claim fixture
  does this escalate to a SKILL entry.
- **planned_change:** New `GN-EVIDENCE-BARE-CLAIM-001` (pure HF-12A) + `GN-EXP-REPRO-001` (reproducibility
  findings). Archive GN-EXP-001. Spot-check both.
- **regression_cases:** GN-EVIDENCE-BARE-CLAIM-001 (HF-12A must fire), GN-EXP-REPRO-001 (repro findings)
- **status:** OPEN (this round — FIXTURE repair)

### D-05 — HF-15 recall unproven (golden-negative false-PASSed, but mutation failed)
- **category:** FIXTURE (may escalate to SKILL only after repair)
- **evidence:** `GN-ROADMAP-001`→PASS/PASS/FAIL (missed HF-15, unstable). §4X: the mutation's regex
  `^\s*\*\*(GO|MODIFY|STOP):\*\*` did NOT match the dash-prefixed `- **GO:** ≥ 20% error reduction…`
  line, so Phase-1 **kept a measurable GO gate**. The phase was therefore still measurable → HF-15 not
  firing is defensible. The mutation did not land.
- **affected_cases:** GN-ROADMAP-001
- **decision:** Do NOT change HF-15 yet. Redo the mutation so Phase-1 has NO measurable gate at all, add
  semantic post-conditions, re-adjudicate. Escalate to SKILL only if v0.3 still misses HF-15 on the clean
  v2.
- **planned_change:** GN-ROADMAP-001 v2 with `assert_absent: ["- **GO:**","20% error reduction",
  "proceed to Phase 2"]`, `assert_present: ["届时定"]`.
- **regression_cases:** GN-ROADMAP-001 v2 (HF-15 must fire, ×3 stable)
- **status:** OPEN (this round — FIXTURE repair)

### D-06 — Evaluation profile is not an explicit evaluator input
- **category:** CONTRACT
- **evidence:** profile (`provenance_policy`) reaches the evaluator only via a prompt field; there is no
  stable contract for how a caller supplies it, and behavior on `external` docs is unstable (D-01).
- **decision:** Define `evaluation_profile` (artifact_type / provenance_policy controlled|legacy|external
  / decision_mode / evidence_requirement / reader_profile / output_mode) as the DQE input contract.
- **planned_change:** ADR-DQE-001 §5.1. Corpus manifests already carry `profile`; ADR makes it the
  authoritative contract. **Skill plumbing deferred.**
- **regression_cases:** BP-004 pair
- **status:** OPEN (this round — CONTRACT/ADR)

### D-07 — BP-002-fail fixture carries an incidental state contradiction
- **category:** FIXTURE
- **evidence:** frontmatter `status: DECIDED` + "The core is done" co-exist with `OQ-2 … (design review
  in progress)` — a genuine "done vs in-progress" contradiction. HF-14a fired *legitimately*, so listing
  it in `forbidden_blockers` was wrong. The intended sole defect was HF-14b (a bare live count with no
  dynamic-source pointer).
- **affected_cases:** BP-002-fail
- **decision:** Clean the over-claim so HF-14b is the lone defect; keep the bare live count with no
  pointer.
- **planned_change:** BP-002-fail v2: drop `status: DECIDED`→`document_lifecycle: ACCEPTED`, remove "The
  core is done", remove the OQ-2 contradiction; retain "当前 69 项测试全部通过" with no pointer.
- **regression_cases:** BP-002-fail v2 (required [HF-14b]; forbidden [HF-13, HF-14a, HF-15])
- **status:** OPEN (this round — FIXTURE repair)

### D-08 — GN-PROP-001 mutation left dangling TOC anchors (secondary defect)
- **category:** FIXTURE
- **evidence:** removing Test Plan / Graduation Criteria / Feature-Enablement sections left their
  `<!-- toc -->` entries pointing at now-missing anchors — a second, unintended defect on top of the
  intended "no validation story" one.
- **affected_cases:** GN-PROP-001
- **decision:** Remove the corresponding TOC entries in the same mutation; assert no dangling TOC.
- **planned_change:** GN-PROP-001 v2 mutation adds TOC-line removal + `assert_no_dangling_toc`.
- **regression_cases:** GN-PROP-001 v2 (forbidden [HF-13, HF-14a, HF-14b, HF-15])
- **status:** OPEN (this round — FIXTURE repair)

### D-09 — BP-005-pass fixture uses `status: DECIDED` over an unverified hypothesis
- **category:** FIXTURE (+ CONTRACT via D-11)
- **evidence:** frontmatter `status: DECIDED` while the body is an explicitly-labeled `HYPOTHESIS
  (尚未验证)`. This mixed signal invited HF-3 (candidate-as-decided) + HF-14a → false-FAIL of a case
  meant to PASS.
- **affected_cases:** BP-005-pass
- **decision:** Use `document_lifecycle: ACCEPTED` (an accepted note may record a hypothesis) and drop the
  claim-status word from the doc-level header, isolating the honest-hypothesis signal.
- **planned_change:** BP-005-pass v2; `forbidden_blockers` gains HF-3 + HF-14a (must not fire on the
  honest label).
- **regression_cases:** BP-005-pass v2 (PASS/ALLOW; forbidden [HF-3, HF-10, HF-12E, HF-14a])
- **status:** OPEN (this round — FIXTURE repair)

### D-10 — Quality vs gate decision share one binary verdict
- **category:** CONTRACT
- **evidence:** the single-defect negatives were rated PARTIAL by reviewers but the gate contract forced
  FAIL — because "holistic document quality" and "may this be released" are collapsed into one
  DOCUMENT_QUALITY flag.
- **decision:** Introduce two axes: `QUALITY_BAND` (PASS/PARTIAL/FAIL) and `GATE_DECISION`
  (ALLOW/BLOCK/INCOMPLETE); keep `DOCUMENT_QUALITY` as the backward-compatible mapping of GATE_DECISION.
- **planned_change:** ADR-DQE-001 §5.3. Corpus manifests add `expected.quality_band`/`expected.gate_decision`
  (additive; existing scorers keep using `document_quality`). Reviewers emit both axes.
  **Skill two-axis output deferred.**
- **regression_cases:** all repaired cases carry both axes
- **status:** OPEN (this round — CONTRACT/ADR + manifest/reviewer)

### D-11 — Document lifecycle vs claim status conflated in `status:` header
- **category:** CONTRACT
- **evidence:** the same `status: DECIDED` string is used both for "the document is decided/accepted" and
  as a claim-level knowledge state, colliding with body claim labels (HYPOTHESIS, in-progress).
- **decision:** Split `document_lifecycle` (DRAFT/IN_REVIEW/ACCEPTED/DEPRECATED) from the claim-status
  vocabulary (FACT/VERIFIED/DECIDED/HYPOTHESIS/CANDIDATE/OPEN/…).
- **planned_change:** ADR-DQE-001 §5.2. Repaired fixtures (BP-002-fail v2, BP-005-pass v2) adopt
  `document_lifecycle`. **Skill change deferred.**
- **regression_cases:** BP-002-fail v2, BP-005-pass v2
- **status:** OPEN (this round — CONTRACT/ADR + fixtures)

### D-12 — Mutations were only validated as "script ran", not "target defect present"
- **category:** HARNESS
- **evidence:** D-05/D-08 shipped because `generate_mutations.py` asserted only "text changed + forbidden
  sections intact", never "the intended defect is actually present and no secondary defect was
  introduced". The stale GO gate and dangling TOC passed generation.
- **decision:** Add semantic post-conditions to mutation generation + a standalone semantic validator.
- **planned_change:** `generate_mutations.py` gains `postconditions:{assert_absent,assert_present}`; new
  `scripts/validate_mutation_semantics.py` (string presence/absence, TOC-anchor resolution, no
  DECIDED+unverified co-occurrence, same-byte-different-profile SHA equality). Semantic failure ⇒ auto
  quarantine.
- **regression_cases:** all mutated cases
- **status:** OPEN (this round — HARNESS)

## Roll-up

| category | ids | this round? |
|---|---|---|
| SKILL | D-01, D-02, D-03 | **No — deferred to v0.4 skill round** (only regression fixtures produced now) |
| FIXTURE | D-04, D-05, D-07, D-08, D-09 | Yes — repaired |
| CONTRACT | D-06, D-10, D-11 | Yes — ADR-DQE-001 (PROPOSED) + additive manifest/reviewer fields |
| HARNESS | D-12 | Yes — postconditions + semantic validator |

The **only** cleanly-isolated skill defect is **D-01 (HF-9 profile)**; D-02/D-03 are skill-suspected but
must be confirmed on the repaired v2 fixtures before any skill change. D-04/D-05 are **not** yet skill
recall gaps — their fixtures did not carry the defect. This is the ledger form of the report's conclusion:
*corpus defects > skill defects; fix the corpus first, then re-test.*

## Spot-check outcomes (2026-07-31) — unchanged v0.3 evaluator on the repaired fixtures

Six isolated v0.3 evaluators (skill byte-frozen) were run on the repaired/new fixtures. Verdicts (full
evidence in `docs/testing/corpus-repair-report-v4.md`):

| case | v0.3 verdict | v0.3 blockers | reading |
|---|---|---|---|
| BP-005-pass v2 | PASS | [] | D-09 fixture-fix **confirmed** (v1 false-FAILed on HF-3/HF-14a) |
| GN-ROADMAP-001 v2 | FAIL | [HF-15] | D-05 fixture-fix **confirmed** — **HF-15 recall was never broken** |
| GN-EVIDENCE-BARE-CLAIM-001 | FAIL | [HF-12A, HF-12E, HF-10] | **HF-12A recall works** on a clean bare claim (no forbidden violation) |
| BP-002-fail v2 | FAIL | [HF-14b] | D-07 fixture-fix **confirmed** — **HF-13 & HF-14a no longer fire** on the clean doc |
| GN-EXP-REPRO-001 | FAIL | [HF-9, HF-12A, HF-12E] | reproducibility blocks; **no forbidden over-fire**; HF-9 = D-01 (external) |
| GN-PROP-001 v2 | FAIL | [HF-9, HF-14a, HF-12E] | still not a clean negative (HF-9=D-01; HF-14a = NEW residual contradiction) |

### Verdicts on the ledger entries (post-evidence)

- **D-01 (HF-9 profile) — CONFIRMED skill defect, still OPEN (deferred).** HF-9 fired on BOTH external
  docs (GN-PROP-001, GN-EXP-REPRO-001) that legitimately have no local front-matter. This is the **one**
  skill change (F1) the evidence justifies.
- **D-02 (HF-13 over-fire) — NOT reproduced on the clean fixture → REJECTED as a standalone skill defect.**
  BP-002-fail v2 (contradiction removed) did **not** fire HF-13; the evaluator applied the
  comprehensive-single-design-report protection correctly. The v1 HF-13 over-fire was
  **fixture-amplified**, not a standalone skill bug. No HF-13 skill change is justified by current
  evidence.
- **D-03 (HF-14a misclassification) — the dangling-TOC half was FIXTURE (fixed, D-08).** On the clean
  BP-002-fail v2, HF-14a did not fire. HF-14a in GN-PROP-001 v2 is a *different, legitimate* contradiction
  (see D-13), not the TOC misread. No HF-14a skill change is justified by current evidence.
- **D-04 (HF-12A recall) — RESOLVED as fixture.** The clean bare-claim `GN-EVIDENCE-BARE-CLAIM-001` fires
  HF-12A. The v1 GN-EXP-001 "miss" was mutation weakness (kept hyperparameters). **HF-12A recall is fine.**
- **D-05 (HF-15 recall) — RESOLVED as fixture.** GN-ROADMAP-001 v2 fires HF-15, with the evaluator
  explicitly contrasting the un-gated Phase 1 vs the still-gated Phase 2. **HF-15 recall is fine.**
- **D-07 / D-08 / D-09 — IMPLEMENTED + VERIFIED.** Fixture repairs confirmed by the spot-check (single
  clean blocker / dangling TOC gone / honest hypothesis now PASSes).
- **D-06 / D-10 / D-11 — IMPLEMENTED (contract).** ADR-DQE-001 + additive manifest/reviewer two-axis.
- **D-12 — IMPLEMENTED.** Postconditions + `validate_mutation_semantics.py`; both green.

### New entries surfaced this round

### D-13 — GN-PROP-001 is not a reliable single-defect negative
- **category:** FIXTURE (corpus validity)
- **evidence:** Both blind reviewers rated the mutated KEP **PASS/ALLOW** (its Design Details are complete
  enough to implement from). The unchanged v0.3 evaluator FAILs it, but on HF-9 (D-01, external) + a NEW
  residual contradiction (Implementation History "1.36 GA" vs the unchecked (R) Test-plan / Graduation
  boxes the mutation itself left) + HF-12E — not on the intended "missing validation story".
- **decision:** UNRESOLVED → user (decisions-pending D6): quarantine + rebuild on a leaner base proposal
  where removing the test plan genuinely breaks executability, OR accept a different intended defect. The
  KEP base is too implementation-complete to fail by one deletion (same failure mode as GN-EXP-001, D-04).
- **status:** RESOLVED 2026-08-02 (D-6=A). GN-PROP-001 v2 → `cases/quarantine/GN-PROP-001-v2/` (not
  overridden to FAIL). Rebuilt lean controlled pair `GP-PROP-CONTROLLED-001` (gold PASS/ALLOW) +
  `GN-PROP-VALIDATION-001` (gold PARTIAL/**INCOMPLETE** — both reviewers: missing required release
  sections → non-ALLOW; a refinement of the expected BLOCK). See adjudication-v4b.md.

### D-14 — retired-status vocab: `ACCEPTED` is not a legal skill status token
- **category:** CONTRACT + FIXTURE
- **evidence:** The bare-claim fixture used `status: ACCEPTED`; the v0.3 `status_vocab` checker rejected it
  (legal set = FACT/VERIFIED/DECIDED/BASELINE/HYPOTHESIS/CANDIDATE/OPEN/DEFERRED/REJECTED/STALE +
  lifecycle experimental/active/planned/deprecated/replaced/retired/reference-only/in-progress), firing a
  spurious HF-3. ADR-DQE-001's `document_lifecycle` vocab (DRAFT/IN_REVIEW/ACCEPTED/DEPRECATED) therefore
  does **not** match the skill's existing lifecycle vocab.
- **decision:** FIXTURE fixed now (bare-claim uses `status: BASELINE`; the checker only validates the
  `status:` field, so `document_lifecycle: ACCEPTED` elsewhere is inert under v0.3). CONTRACT: reconcile
  ADR document_lifecycle vocab with the skill lifecycle vocab in the v0.4 skill round.
- **status:** FIXTURE part IMPLEMENTED; CONTRACT part OPEN (v0.4)

### D-15 — HF-14b applicability must be profile-qualified (D-7 resolution)
- **category:** CONTRACT (+ corpus)
- **evidence:** BP-002-fail's gate split in adjudication-v4 (A BLOCK / B ALLOW). User ruled D-7=A_QUALIFIED:
  keep FAIL/BLOCK, but only under `controlled + release-gate + stable-canonical-doc + bare-current-volatile-
  fact + no-pointer`. Three byte-identical BP-002 variants (adjudication-v4b) confirm the gate flips with
  profile alone: release-gate→BLOCK, controlled+audit→ALLOW, external+audit→ALLOW.
- **decision:** HF-14b severity is profile-mapped (controlled+release-gate ⇒ BLOCKER; controlled+audit ⇒
  MAJOR; legacy/external/audit ⇒ MINOR/MAJOR, never a lone BLOCK; status/experiment reports ⇒ N/A; dated
  snapshot + pointer ⇒ escape). This is a **narrowing** of HF-14b, not an expansion.
- **planned_change:** ADR-DQE-001 §HF-14b severity map (Phase B); skill implements the mapping (Phase C5,
  C-round). Corpus: BP-002-fail (BLOCK) + BP-002-audit/external (ALLOW) added as regressions.
- **status:** CONTRACT + corpus IMPLEMENTED (this round); skill mapping = Phase C.

### D-16 — audit-mode gate under-specified (found by the D.3 diagnostic on BP-006-audit)
- **category:** CONTRACT (skill text) — surfaced 2026-08-04
- **evidence:** first D.3 rerun of `BP-006-audit` (external + audit) was **3-way unstable**: run-1 BLOCK,
  run-2 ALLOW, run-3 INCOMPLETE — while all three agreed QUALITY_BAND=PARTIAL and surfaced the same
  reproducibility findings. Root cause in the evaluators' own reasoning: with **no hard gate MET** but rubric
  total < 75 and `FACTUAL_VALIDITY=UNVERIFIED`, the v0.4 ALLOW preconditions (`total ≥ 75 AND
  FACTUAL_VALIDITY≠UNVERIFIED`) were **release-gate semantics leaking onto the GATE_DECISION axis**, so each
  run resolved the gate differently. BP-006-release (BLOCK×3) and GP-EXP-001 (ALLOW) were unaffected — the
  ambiguity only bites when no blocker fires and the score is sub-threshold.
- **decision:** clarify (not re-scope) the two axes: **GATE_DECISION is derived deterministically** —
  (1) missing required section/input/profile or checkers/reader not run ⇒ INCOMPLETE; (2) else any BLOCKER-
  severity hard gate ⇒ BLOCK; (3) else ALLOW. Rubric total gates **QUALITY_BAND only**; UNVERIFIED is a
  factual-validity floor that bars the *green terminal* gate but never moves GATE_DECISION. Added the worked
  case (external+audit, no blocker, total 74, UNVERIFIED ⇒ ALLOW/PARTIAL) to SKILL.md + the EVALUATOR_CONTRACT.
- **change:** `SKILL.md` (derivation rule + amended forbidden-ALLOW list + amended PASS condition) and
  `make_grading_injection.py` EVALUATOR_CONTRACT (deterministic derivation). **No discrimination threshold
  changed** (HF-9/12A/13/14a/14b/15 untouched); this is a verdict-composition clarification only. Skill stays
  0.4.0 (pre-admission text hardening, disclosed here).
- **verify:** re-ran `BP-006-audit ×3` (diag-d3b) → **ALLOW ×3**, PARTIAL ×3, blockers=[] — stable. Diagnostic
  closes at 8/8.
- **status:** IMPLEMENTED + verified (2026-08-04).

## Bottom line (evidence-based)

**Of the report's proposed skill fixes F1–F4, only F1 (HF-9 profile-gating) survives the evidence.**
F2 (HF-12A) and F3 (HF-15) were fixture defects — the clean v2 fixtures fire those gates correctly.
F4 (HF-13/HF-14a tightening) did not reproduce on the clean fixture. This round therefore **prevents an
over-modification of the skill**: the next (separately-approved) skill pass should implement HF-9
profile-gating and re-run, not a broad F1–F4 sweep.

**D.3 addendum (2026-08-04):** the diagnostic also caught one genuine v0.4 text gap (**D-16**, audit-mode
gate composition) which is now fixed and re-verified stable. The OQ-REPRO=A decision (BP-006 pair) is
confirmed by blind A/B **and** by the skill: a non-reproducible controlled release-gate doc BLOCKs via
HF-12A/E **without** any dedicated HF-REPRO, and the audit twin ALLOWs — the two-axis model holds.

