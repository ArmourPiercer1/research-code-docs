# Reconstruction Execution Notes (parent-agent working file)

<!--
generated_by: parent agent
scope: orchestration state for Phase 0/1 execution — NOT a charter deliverable
status: IN PROGRESS
date: 2026-09-09
-->

## Round 1 — parallel investigation (4 background subagents)

| id | label | outputs |
|---|---|---|
| 7b372257-487c-49ed-8c70-ea218132cae8 | Phase 0 系统地图+技能分类 | **DONE** (1 fail-resume cycle) — `phase0/current-system-map.md` (76.2KB, 384 cites; 14 skills, harness, DQE, governance, L3 interface, discrepancy log D1–D14), `phase0/existing-skill-classification.md` (30.7KB, 163 cites; KEEP×13 REFINE×7 SPLIT×1 MERGE×1 REPLACE×1 REMOVE×1 ADD×6) |
| 9e5798bc-a1ac-4bfc-9492-d8d1283ecd46 | Phase 0 信息所有权+痛点证据 | **DONE** — `phase0/current-information-ownership-map.md` (39.5KB, 298 cites; 17 info types, 8 unowned, duplication ledger D1–D19), `phase0/pain-point-evidence.md` (32.2KB, 156 cites; P1–P10, top cost = 63M-token workflow runaway) |
| 8afbdd82-e392-4670-8231-9dab6cb3b6cc | DSH 现状机制调研 | **DONE** (1 fail-resume cycle) — `intermediate/dsh-current-state-findings.md` (73.5KB, 279 cites, 37 sections; 32 mechanisms M1–M32; 14 machine / 10 mixed / 8 prose-only) |
| 59b9ac4f-e50b-4c6c-9941-1e7b43931c6d | DSH 历史证据+负证据调研 | running (steered to start writing progressively) |

DSH sanity check (2026-09-09): repo OK — 14,882 commits, HEAD `a66e470204`
(release dsh 0.1.2-rc.1), `.agents/skills/` = 11 skills, `.agents/notes/` present,
root `AGENTS.md` present, both `.github/` workflows and `.gitlab-ci.yml`, `snapshots/`
at repo root, `.claude/` also present alongside `.agents/` (DSH itself keeps both —
noted for the evidence map).

## Round 2 — synthesis (LAUNCHED 2026-09-10 once all 6 round-1 files passed gates)

Round-1 totals: 6 files, 338.9KB, 1,711 citations — all 5-gate PASS.

| id | role | outputs |
|---|---|---|
| 45295ffb-5549-48ee-b33e-e759c093fbb4 | S1 DSH synthesis | **DONE** — `phase1/dsh-workflow-evidence-map.md` (83.7KB, 255 cites, 32/32 mechanisms, 15-row negative-evidence table C1–C15), `phase1/dsh-transferability-crosswalk.md` (32.7KB, 107 cites; labels 5/12/2/13) |
| 54c2e83b-8a19-491c-88be-4527c9e3c8e0 | S2 target architecture | running — invariants DONE (56.4KB, 108 cites), capability-architecture in progress, 3 files remaining. Steering sent: final step = sweep ~10 PENDING-S1 markers in the two already-written files against S1's crosswalk (leave UNKNOWN-CROSSWALK if unresolvable). |

(Original round-2 plan below.)

Two parallel synthesis subagents:

- **S1 (DSH synthesis)** — inputs: `intermediate/dsh-current-state-findings.md` +
  `intermediate/dsh-history-findings.md` + charter §5/§6/§7 + phase0
  classification/pain-points (for "relevance here"). Outputs:
  `phase1/dsh-workflow-evidence-map.md` (one full 9-link chain per mechanism:
  observed mechanism → problem → historical evidence it mattered → encoding →
  evolution → later removals → does same problem exist here → generic principle →
  what NOT to copy) + `phase1/dsh-transferability-crosswalk.md` (§5.3 table with
  the 7 required columns + §7 label per row: DIRECTLY TRANSFERABLE /
  TRANSFERABLE AFTER GENERALIZATION / RESEARCH-SPECIFIC ADAPTATION REQUIRED /
  DSH-SPECIFIC — DO NOT COPY).

- **S2 (target architecture synthesis)** — inputs: all 4 phase0 files + both DSH
  intermediates + charter §8–§14, §17–§20. Outputs:
  `phase1/target-workflow-invariants.md` (§8 invariants, each with: statement,
  current-system compliance verdict + evidence, proposed mechanical enforcement)
  + `phase1/target-capability-architecture.md` (§9 capability model organized by
  lifecycle family, each capability mapped to existing/absent mechanism + §10
  mechanism-layer decision with justification) +
  `phase1/canonical-information-model.md` (§13: for each information type —
  owner, lifecycle, update trigger, archive/delete rule, allowed references,
  forbidden duplications) + `phase1/skill-change-matrix.md` (§11 YAML schema per
  skill: all 14 current skills + 3 flows + harness + the §12 candidate changes,
  each with proposed_action and `why_this_must_be_a_skill` — entries failing that
  test default to another mechanism or removal) + `phase1/eval-plan.md` (§14:
  atomic/workflow/adversarial/longitudinal, concretized with real scenarios from
  this repo's corpus and DSH-informed cases).

## Review-gate decisions (user, 2026-09-10) — Phase-0 findings adjudicated

1. **D6 (user-level .claude install)** → EXPECTED behavior (deliberate Mode B test install,
   2026-08-07, byte-identical); docs were just not updated. → COMMITTED `4df8f7f`
   (docs/skill-development/README.md "Recorded install state" + evals/skills/README.md pointer).
2. **D10 (frozen contracts unversioned)** → user: "move them to the right place". →
   COMMITTED `098f2bb`: `references/interfaces/` + `references/templates/` now git-tracked
   (.gitignore `references/*` + negations; 9 vendored corpora stay ignored).
3. **D3/D4 (documentation-refactor stale vs Sprint 6B)** → user: fix it. → COMMITTED
   `4e839b2`: SKILL.md skeleton claims → post-6B state (first closed loop COMPLETE
   dry-run+candidate; apply-gate BLOCKED on explicit write-approval); docref-conf-03
   re-baselined (dataset_version 2); registry purpose synced; DQE SKILL.md:9 VOID-roadmap
   pointer → ADR-DQE-001 (D12). Preflight + YAML parses pass.

Still pending from the review gate: architecture review (invariants / mechanism layers /
portfolio / Phase-2 slice) + the D-1 human ruling (canonical status owner) — the slice
cannot close without it. External ChatGPT review in flight: sanitized copy being written
to docs/reconstruction-external-review/ (tracked) by subagent f18f6c54.

## Review gate (charter §15 — user decides before any implementation)

When Phase 0/1 are complete, the user review should decide, in order:
1. Do the Phase-0 findings (system map, classification, duplications, pain points)
   match the user's experience of the system? (factual correction round)
2. Target invariants: accept / amend the §8 set + proposed mechanical enforcement.
3. Mechanism decisions: accept / amend the §10 layer assignments (which capabilities
   get skills vs checkers vs conventions vs no automation).
4. Skill portfolio: accept / amend the §11 matrix (keep/refine/merge/split/replace/
   add/remove actions).
5. Phase-2 vertical slice: accept the proposed closed loop (or substitute).
Only after these does Phase 2 (minimal vertical slice) begin.

## Consistency-check items (parent findings, verify in Round 3)

1. **Snapshot preservation nuance**: B states `evals/skills/snapshots/` "is empty on
   disk"; parent's 2026-09-09 22:37 verification run of `build_skill_snapshots.py`
   populated it with 3 bundles (dqe-v0.3.0 / dqe-v0.4.0-pre-d16 / dqe-v0.4.1-candidate,
   all git-ignored). Substantive finding stands — the registry's "PRESERVED" claim
   overstates persistence (bundles exist only after a build run; fresh clone = empty
   dir) — but the final report must reword "empty on disk" → "empty in a fresh clone /
   not git-tracked".
2. **Adjudication file layout**: protocol + v4 + v4b live in `docs/testing/`; dated
   round file(s) in `evals/skills/adjudication/` (1 file: 2026-07-31) +
   `tests/corpus/blind-runs/adjudication-v4{,b,c}/`. Verify B's "5 dated round files"
   count; `queue.md` (referenced by adjudication-protocol.md) confirmed absent.
3. **DSH dual-platform stub**: C found DSH's `.claude/skills` empty/unresolved —
   crosswalk observation must say ".claude exists as a stub, not a parallel copy"
   (verify before quoting).
4. **D-17 status split** (B): OPEN in the defect ledger vs scope-out in 3 other files —
   a live current-state inconsistency; feed into target-workflow-invariants
   (single-source-of-truth for decision state).
5. **DSH in-place-update gap** (C): `2026-06-11-quality-gates.md` still lists TUI in
   CI smokes after TUI removal — prose rules rot in DSH too; use as crosswalk
   negative evidence.
6. **Registry path**: skills-registry.yaml lives at
   `docs/skill-development/skills-registry.yaml` (not repo root).
7. **Case-count discrepancy**: A reports 229 case entries / 41 YAML files;
   parent's direct count (regex `^\s*-\s*\{?\s*id:\s*` over evals/skills
   trigger|conflict|task-quality) = 211 / 32. A may have counted all case YAMLs
   incl. harness/flow files or a different case syntax. Resolve in Round 3 by
   re-counting with A's stated method (read A's system-map §C methodology) and
   quoting both with method.
8. **Commit count**: verified 18 total (root 279c0ce; rev-list root..HEAD = 17).
   B's "19 commits" headers corrected by parent (both files); A's 18 stands.
9. **DSH day-one dual-platform**: first commit b67e81ac97 ships CLAUDE.md as a
   symlink — the .claude coexistence is a day-one design, not a later addition
   (updates crosswalk item 3).

## Round 3 — parent consistency check (EXECUTED 2026-09-10) — ALL PASS

| Check | Result |
|---|---|
| A. classification labels ↔ matrix proposed_action | 36/36 exact (phase0 census KEEP15/REFINE7/SPLIT1/MERGE1/REPLACE1/REMOVE1 = matrix keep15/add10/refine7/split1/merge1/replace1/remove1) |
| B. I-refs in phase1 ⊆ defined I1–I12 | no orphans (referenced set = full I1–I12) |
| C. M1–M32 evidence-map coverage = crosswalk rows | 32 = 32 |
| D. canonical-model vs phase0 ownership | Δ explicit on all 17 rows + §2 summary (5 new stores / 4 git-tracking / 3 deletions / 4 collapses / 9 lints) |
| E. residual PENDING-S1 / TODO-SECTION / PENDING-PHASE0 | 0 (3 grep hits = prose references to the sweep) |
| F. check_deliverables.py (ID-aware citation count) | VERDICT: ALL PRESENT & SANE (13/13) |

Discrepancy list resolution: #1 snapshot wording (reword in report: "empty in fresh
clone", D19 tracked in canonical model row 6); #2 adjudication layout verified
(queue.md absent — stands); #3 day-one CLAUDE.md symlink verified; #4 D-17 split →
canonical rows 7-8; #5 TUI rot in C's file + crosswalk negative evidence; #6 registry
path noted; #7 case count RESOLVED: 229/41 correct (independent recount: 152/43/16/12/6),
baseline file updated to 5 dirs; #8 commits RESOLVED: 18, B's headers corrected;
#9 day-one dual-platform RESOLVED.
S2 flag resolved: "KEEP×13" (inherited from A's summary) was an undercount; phase0
table row-by-row census = KEEP 15 (A's own parenthetical list even enumerated more
than 13 incl. the REFINEd S5). S2's 15 stands; matrix matches.

## Round 3 — parent consistency check + report (original plan)

1. Verify all 11 deliverables exist and are non-trivial (read each header + spot sections).
2. Cross-check consistency: classification labels (phase0) must match
   skill-change-matrix proposed_action; invariants cited in capability architecture
   must exist in target-workflow-invariants.md; evidence-map mechanisms must appear
   in crosswalk; canonical-information-model owners must not contradict
   phase0/current-information-ownership-map.md (target vs current: differences must
   be explicit deltas, not silent).
3. Update this README's status table; report to user with a one-page summary.

## Candidate Phase-2 vertical slice (parent's preliminary, for S2 to evaluate)

> SUPERSEDED (repair round, R9): the candidate below became File 2 §7, and the third-
> party repair guide's R9 counts (synthetic loop / WFI mandatory / full checker set /
> quota proof) led to its redesign. Current slice: `revised-phase2-vertical-slice.md`
> (real messy repo → PSR → simplification-audit → ONE candidate → decision note →
> implement → focused-verification → two-axis review → same-change updates). Kept here
> as the record of the preliminary.

Hypothesis (from the pain-point pre-read): the highest-value slice attacks the two
most costly recurring failures — stale current-state docs and duplicated "current
state" descriptions — using machinery that ALMOST exists:

    rerun PSR on this repo (fresh, post-rename)
      → find stale/duplicated current-state claims (vs canonical owners)
      → produce a same-change canonical-update proposal (12.8 living-design-maintainer
        direction: update the owner in the same change, not a standalone report)
      → mechanical duplicate-fact check verifies before/after
      → flow-state + eval record the run

Why this candidate: end-to-end on the real corpus (this repo), exercises the new
mechanical checks, reuses 3 existing skills, produces a verifiable artifact, and its
success is checkable without model judgment (sha256 + checker output). S2 must test
this against the alternatives (e.g. the 12.3 smallest-evidence selector slice, or the
12.6 decision-model refactor slice) and pick with justification — this note is a
candidate, not a decision.

## Round 4 — repair round (third-party architecture review, 2026-09-10)

Input: `docs/plans/active/research_code_docs_phase1_architecture_repair_guide.md`
(1496-line revision contract, R1–R12 + guide §§13–21).

Scope: verify every repair item against the real repo (3bb307f, 23 commits), then
execute the 12-item contract. Parent did all design + precise edits directly (no
synthesis subagents this round — the edits were small, dense, and codepoint-sensitive:
EN/EM dash mix + 2/3-space indents broke naive string edits; PS codepoint-anchored
patches used for the two big rewrites).

Outputs (all under this folder unless noted):
- `post-audit-reconciliation.md` (NEW) — R1: D1–D19 re-verified (3 RESOLVED by
  098f2bb/4e839b2, 2 PARTIAL D6/D12, 14 STILL-LIVE with current evidence), P1–P10
  re-ranked, 12 stale Phase-1 statements corrected, Phase-2 candidate pool (selected:
  archive VOID creation-roadmap + D-1 decision note).
- `phase1/target-workflow-invariants.md` (REVISED) — I3 uncertainty↔rejection + 5
  rejection bases; I4(c) R4 revised 6-field schema + NEW §I4.1 (12 REAL entries,
  all 7 required representations + R3 cases); I6(c) R2 rewrite (impact-set +
  same-change discharge; last_verified → optional informational; 3 fixture tests);
  I10(c) R7 graph-integrity.
- `phase1/canonical-information-model.md` (REVISED) — row 4→4a/4b/4c, row 6→6a/6b/6c
  (R6); row 8 decision folders proposed/decided/rejected/archived (R3, ADR-DQE-001→
  decided/); row 10 R7; row 16 D6 partial (4df8f7f); single manual canonical source
  map = `docs/canonical-source-map.md` (Phase 2), harness copy → thin pointer;
  R11 deferral list; D3/D4/D10 marked resolved by commit.
- `phase1/eval-plan.md` (REVISED) — R5 defect 10→10A/10B (basis vs weak-evidence);
  scenario A rewritten to R9 shape (real repo → PSR → audit → ONE candidate →
  decision note → implement → focused-verification → two-axis → same-change →
  before/after); scenario C decision-value-first (R10.2); baseline = delta diagnostic
  (R10.1); planted obsolescence not quotas (R10.3); counts as indicators (R10.4);
  checker row = Phase-2 minimum set (R11).
- `phase1/target-capability-architecture.md` (REVISED) — §2.9 canonical-impact-lint;
  §4.4 R7 (graph OWNS relations; SKILL.md one-line pointer; views generated); §5.x
  R2/R3/R4/R5/R6/R11 updates; §7 fully rewritten (R9 shape + pointer to the revised
  slice; A2/A3/A4/A6 parked per R12).
- `phase1/skill-change-matrix.md` (REVISED) — header R8 prior/posterior rule +
  KEEP×15 census fix; LDM/G4/§5.8 canonical-impact-lint; G5 ADR → decided/; A2/A3/A4/A6
  PARKED CAPABILITY GAP blocks (5 fields each); A10 R10.2 (decision value first);
  §5.6 schema test DONE (I4.1); D14 builtness wording → graph-match (R7).
- `revised-phase2-vertical-slice.md` (NEW) — R9: the slice = real messy repo → PSR →
  simplification-audit (WFI as mechanical half, documented) → ONE candidate (archive
  VOID creation-roadmap, D12 live instance) → D-1 decision note (proposed/; HUMAN
  RULING GATES IT) → host implements → focused-verification (A9 minimum) → two-axis
  review → same-change owner updates → before/after evidence. Minimum checkers (R11):
  canonical-impact-lint(+change-scope), archive-lint, supersession-lint,
  decision-note-lint; 6 deferred with build phase.
- `architecture-review-disposition.md` (NEW) — every R-item: decision + evidence +
  change_made + residual_risk; §13 10 principles preserved (verified); §16 12/12 PASS;
  §19 do-NOT 15/15 complied; §20 14/14 gate items done (the one open item, D-1, was
  then resolved by the final ruling — see Round 5); guide citation corrections
  recorded (canonical-source-map actual path; docs/ map not yet created).
- LIVE-REPO edit (the one and only): `docs/skill-development/skills-registry.yaml:20`
  `meta.isolation` — recorded the Mode-B test install (4df8f7f) instead of the bare
  "workspace-only" claim (D6 residual; YAML re-validated with .venv python).

## Round 5 — final external-review consistency patch (2026-09-10)

- Final review verdict: **ACCEPTED WITH REQUIRED CONSISTENCY PATCH; Phase 2 GO**;
  D-1 ruled **option A** (this README's status table = single canonical "what is next"
  owner). D-1 is now DECIDED — the slice note lands `decided/` with the full 6-field
  block (implementation_state: not_applicable).
- Patch items applied in place (P1–P8): see `architecture-review-disposition.md` §9
  (per-item FIXED + §11 checks 11.1–11.8 PASS) and `reconstruction/README.md` final
  consistency patch section.
- Scope: 5 phase1/ files + revised-phase2-vertical-slice.md + disposition (target
  spec set); README/execution-notes lightly synced; `.gitignore` P2 (blanket
  `docs/plans/` ignore → explicit `local/` + `scratch/` only); the git-add tracking
  transition stays Phase-2 slice Stage 5 scope (NOT staged in this patch).
- Mirror: `docs/reconstruction-external-review/` re-synced (7 changed docs + README),
  zero-leak re-verified.
- No new live-repo edits (registry line unchanged since b67ba43).

Still open: none. Next: Phase-2 vertical slice per the revised spec.

## Constraints

- Phase 0/1 are documentation-only: no changes to `.agents/skills/`, scripts, or
  tracked repo files during this phase (charter §15).
- All deliverables live under `docs/plans/active/reconstruction/` (was git-ignored;
  now trackable after P2, tracking transition pending Phase-2 Stage 5).
- Evidence bar: file:line or commit-hash citations; UNKNOWN where unverifiable;
  no invented facts.
