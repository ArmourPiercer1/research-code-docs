# Architecture review disposition (repair round)

```yaml
date: 2026-09-10
role: disposition record for the 12-item repair contract (R1–R12) + guide §§13–21
inputs: research_code_docs_phase1_architecture_repair_guide.md (the contract);
  post-audit-reconciliation.md (R1 evidence); the five revised Phase-1 files;
  revised-phase2-vertical-slice.md
status: COMPLETE — all items resolved; D-1 finalized by the final external-review
  consistency patch (option A); Phase 2 GO
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ./README.md; 2026-09-10, final consistency patch)
```

Every review item below carries: **decision** (accept / partially_accept / reject),
**evidence** (file:line or commit on current main, 3bb307f + repair-round edits),
**change_made**, **residual_risk**.

---

## 1. Repair items R1–R12

### R1 — Reconcile Phase 0 audit findings with current main

- **decision:** accept (executed)
- **evidence:**
  - RESOLVED-BY-CURRENT-MAIN: D3/D4 (4e839b2 — docref-conf-03 re-baselined, DQE SKILL.md:9
    pointer fixed), D10 (098f2bb — 24 files tracked under references/).
  - PARTIALLY-RESOLVED: D6 (4df8f7f recorded the Mode-B test install in
    docs/skill-development/README.md; the registry `meta: isolation:` line still said
    "workspace-only" at 3bb307f — fixed this round in skills-registry.yaml:20),
    D12 (DQE pointer fixed by 4e839b2; unarchived VOID roadmap + system-architecture
    status line still live at 3bb307f).
  - STILL-LIVE: D1, D2, D5, D7, D8, D9, D11, D13, D14, D15–D19 (14 items; per-item
    current-main evidence in post-audit-reconciliation.md §1), P5 (shrunken instance
    list; §2).
  - No historical cost figure was rewritten (guide §2 rule 6).
- **change_made:** post-audit-reconciliation.md (new, §1 D-table, §2 P-table, §3 the 12
  statement corrections, §4 Phase-2 candidate pool); the 12 stale Phase-1 statements
  corrected in place (File 1 I2(b)/I5(b)/I6(b)/Q5/Q10, File 2 §5.2, File 3 rows 1/3/16,
  File 4 A2/A3/D14 refs, File 5 defects 1/6 + scenario A); skills-registry.yaml:20
  isolation line (the one live-repo edit of the round, YAML re-validated).
- **residual_risk:** the reconciliation is a point-in-time census; any commit after the
  slice-start commit re-opens it. Mitigation: the slice's before/after evidence table
  re-captures the live state at slice start.

### R2 — Replace timestamp-as-correctness with change-impact discharge

- **decision:** accept (executed)
- **evidence:** the audit's D14-class instances (registry:89/102/538, SWR SKILL.md:49)
  were stale-claim vs roster, not stale-vs-timestamp — a `last_verified` comparison
  would not have caught them; the guide's three fixture tests are the acceptance bar.
- **change_made:** `canonical-freshness-lint` → `canonical-impact-lint` in every file
  (File 1 I6(c)/Q7/Q10/Q13/Q17, File 2 §2.9/§5.2/§5.7/§6, File 3 rows 2/14/rules, File 4
  LDM + G4 + §5.8, File 5 §a.2/§b/§c/d.1/d.2); I6(c) fully rewritten: declared
  documentation impact set + same-change update OR explicit no-doc-impact; `last_verified`
  demoted to optional informational; the 3 fixture tests specified (unrelated commit
  passes; in-scope stale owner fails; timestamp-only does not clear).
- **residual_risk:** the impact set must be DECLARED per change — a change that omits its
  declaration is outside the lint's power. Mitigation: change-scope input (the slice
  carries the declared set; the lint validates against it) and the same-change review
  rule in the slice's two-axis spec axis.

### R3 — Decision lifecycle ≠ implementation lifecycle

- **decision:** accept (executed)
- **evidence:** DSH's own `implemented/` folder tracked code changes through shipment
  (its notes are code-change notes); this repo's decisions (e.g. ADR-DQE-001's advisory
  freeze) can be accepted with implementation none/not_applicable — the folder name
  "implemented/" forces the wrong conflation (charter §12.7 context; DSH crosswalk A.8).
- **change_made:** folders `proposed/ decided/ rejected/ archived/` in File 1 I5(c)(2)
  (+ DSH-adaptation rationale), File 2 §1.1 bootstrap skeleton, File 2 §5.4, File 3 row 8
  (full lifecycle rewrite; ADR-DQE-001 migrates to `decided/` with
  implementation_state: implemented), File 4 A4/G5 entries; two new eval cases in
  File 5 §a.2 (route DECIDED + implementation none; decision with implementation
  not_applicable) — both also rows 4/1 of the I4.1 state-space table.
- **residual_risk:** the existing DSH habit of `implemented/` as a label may leak back in
  prose. Mitigation: decision-note-lint + the register schema (implementation_state is a
  field; the folder name is lifecycle-only).

### R4 — Redesign the orthogonal state model so it is actually orthogonal

- **decision:** accept (executed — schema REVISED, then tested)
- **evidence:** charter:711-724 (`kind` candidate) mixes object types (route, claim) with
  an epistemic role (hypothesis) and a selection state (candidate) — one real object
  (a route that is a candidate, hypothesis-supported, proposed, implementation none)
  cannot be represented without a lossy choice; the charter's own instruction was to
  test before adopting.
- **change_made:** revised 6-field schema (object_type / epistemic_state /
  decision_state / evidence_level / evidence_state / implementation_state;
  not_applicable added to decision_state AND implementation_state) in File 1 I4(c); the
  TEST is done: File 1 §I4.1 = 13 real entries (no invented examples) covering all seven
  required representations (weakly supported active hypothesis; candidate route not yet
  decided; decided route not yet implemented; rejected route with strong historical
  evidence; claim with no decision/implementation concept; contradicted claim with
  temporarily-in-use implementation; experiment result with no decision state); one
  material deviation from the charter candidate (kind split) with per-entry
  justification; `kind` references purged (File 1 I2/Q15/Q11, File 2 §3.3, File 4 §5.4,
  File 5 scenario C, UDM entry row 174).
- **residual_risk:** 12 entries is a real but bounded sample; a future object type
  (e.g. a requirement with a compliance state) may expose a gap. Mitigation: the schema
  is frozen-pending-Phase-2-confirmation — the slice's D-1 note + register updates are
  the next real entries, and VOCAB.yaml + the role-mixing rule make any new value a
  declared addition, not a silent drift.

### R5 — Weak evidence is not rejection

- **decision:** accept (executed)
- **evidence:** the old adversarial defect 10 took "all E≤2 after the experiment" as
  rejection grounds — an epistemic error (insufficient evidence is not contradictory
  evidence); the canary data (P4) supplies the true rejection basis (direct
  contradiction of a load-bearing premise).
- **change_made:** I3(a) adds "uncertainty↔rejection" to the never-equate list; I3(c)(5)
  lists the 5 explicit rejection bases (direct contradictory evidence; constraint
  violation; domination under explicit criteria; human stop decision; invalidated
  load-bearing premise) + the symmetric "no silent demotion from uncertainty to
  rejection" rule + decision-note-lint enforcement (non-empty rejection_basis);
  File 3 rows 7/8 (rejected ⇒ basis); File 2 §5.4; File 5 defect 10 split into 10A
  (REJECTED with basis) / 10B (STAYS OPEN/DEFERRED/needs-experiment) and scenario C
  rewritten with the explicit basis.
- **residual_risk:** "dominated under explicit criteria" is judgment-adjacent; a
  reviewer could stretch it. Mitigation: the criteria must be explicit IN the note
  (linted field), and Case B's eval asserts the basis names the criterion.

### R6 — Canonical-source ownership granularity

- **decision:** accept (executed, with a citation correction — §8 below)
- **evidence:** File 3 row 4 named three authorities (charter + status table + route
  table) in one row — the charter is an operating contract, the status table is
  execution state, the route table is register state: three different fact types; row 6
  mixed raw results, corpus evolution, and release reproducibility.
- **change_made:** row 4 → 4a (operating contract = charter) / 4b (execution status =
  status table, the single "what is next" owner) / 4c (route state = register);
  row 6 → 6a (raw results) / 6b (corpus/dataset evolution) / 6c (release
  reproducibility); single manual canonical source map fixed: `docs/canonical-source-map.md`
  (Phase 2, tracked) is the ONE hand-maintained map; the existing harness table
  `evals/skills/harness/canonical-source-map.md` becomes a thin pointer / generated
  view (File 2 §5.1, File 3 §2).
- **residual_risk:** until Phase 2 creates `docs/canonical-source-map.md`, the live map
  is still the File-3 table + the harness table — a two-copy window. Mitigation: the
  slice's same-change step names the creation; the window is bounded to the slice.

### R7 — Do not solve duplication by synchronizing duplicate authorities

- **decision:** accept (executed)
- **evidence:** four unreconciled partial dependency views at audit (ownership 1.9;
  creation-roadmap:78-80 vs registry:25 vs system-architecture §3 vs flow SKILL.md
  tails); the old `dependency-graph-lint` spec cross-checked the graph against SKILL.md
  PROSE — a synchronization checker.
- **change_made:** the registry graph is the ONE machine authority for
  deps/shared-resources (File 1 I10(c) rewritten; File 3 row 10; File 2 §4.4):
  SKILL.md carries a one-line pointer to its graph entry; architecture/flow views are
  GENERATED from the graph; the lint redefined as graph INTEGRITY (roster existence,
  no cycles, shared_resources declared, routing-table consistency, builtness-claim vs
  roster — the D7/D14 class) with NO prose-syncing duty; the conflict-matrix is KEPT
  (genuinely different relation: co-run semantics OK/SEQ/DENY/COND).
- **residual_risk:** the graph fields do not exist yet (they ship with the Phase-3
  schema batch), so the lint is deferred until then — until then, builtness-claim
  checks run ad hoc. Mitigation: the slice's D14 owner update is the first
  graph-matched claim; the field batch is scheduled, not dropped.

### R8 — Phase-0 labels are prior, Phase-1 posterior

- **decision:** accept (executed)
- **evidence:** the matrix header's "Label agreement rule" mechanically bound
  `proposed_action` to the phase0 label; the header's own census (KEEP×13) also
  undercounted vs §6's verified row-by-row census (KEEP×15 — the "13" omits G5/G6).
- **change_made:** matrix header rewritten to the prior/posterior rule (phase0_label /
  phase1_label / delta_reason + new evidence required on any delta); header census
  corrected to KEEP×15 with the undercount explained; the §6 census (32/32 agree at
  3bb307f, zero deltas) re-verified as the current state.
- **residual_risk:** none material — the rule is a constraint on future deltas; the
  current census has zero deltas, so no entry needs retrofitting.

### R9 — Redesign the Phase-2 vertical slice

- **decision:** accept (executed)
- **evidence:** the original slice was a synthetic duplicate-census loop with WFI
  mandatory and the full 10-checker portfolio on first run — the guide's four R9
  counts are documented in revised-phase2-vertical-slice.md §1.
- **change_made:** File 2 §7 replaced with the R9 shape + pointer;
  revised-phase2-vertical-slice.md created (real messy repo → PSR → simplification-audit
  (WFI participates as the audit's mechanical half, documented) → ONE candidate:
  archive the VOID creation-roadmap → D-1 decision note (landed proposed/ at that
  time — FINAL RULING per the consistency patch P1: option A, decided) → host
  implements → focused-verification (A9 minimum subset) → two-axis review →
  same-change canonical-owner updates → before/after evidence table); File 5 scenario A
  rewritten to the same shape.
- **residual_risk:** RESOLVED — the final external-review consistency patch ruled D-1
  (option A); the note lands decided/ recording the ruling. See §7.

### R10 — Fix gameable eval criteria

- **decision:** accept (executed, all four sub-items)
- **evidence:** (a) "baseline detects ≤50%" made the baseline a required loser; (b)
  A10 optimized cost without first establishing the experiment changes the ranking;
  (c) "≥1 removal per 10 iterations" is a fixed deletion quota; (d) "≤3 skills", "≤2
  artifacts", "≤2 duplicates" as pass shapes rewarded counting, not responsibility.
- **change_made:** (a) File 5 a.3 + adversarial criteria: baseline = DELTA diagnostic,
  tie valid, triggers A8 simplification signal; (b) A10 entry (File 4) + scenario C:
  decision_relevance + expected_discrimination fields, cheap non-discriminating spec
  must LOSE; (c) metric 11 + d.4: planted obsolescence at iterations 12/24, healthy
  fixture may have zero removals; (d) metrics 1/9/10: indicators, fail on pathological
  growth (monotone growth without capability gain / duplicate types / one fact in
  multiple artifacts / new skill with no unique judgment).
- **residual_risk:** "pathological growth" is a looser gate than a number — a review
  could disagree on pathology. Mitigation: the four concrete predicates are named in
  every metric row; a disputed case is a two-axis review finding, not a silent pass.

### R11 — Re-trim the checker portfolio

- **decision:** accept (executed)
- **evidence:** the 10-checker portfolio was designed before R6 removed its first
  instances (the row splits) and before R7 redefined the graph lint; six checkers have
  no input artifact until a later phase.
- **change_made:** File 2 §6 CHECKER row + File 3 rules section + File 5 §a.2 checker
  row + revised slice §7: Phase-2 minimum set = {canonical-impact-lint (+change-scope
  input), archive-lint, supersession-lint, decision-note-lint}; DEFERRED with build
  phase = {duplicate-fact-lint (Phase 3), release-version-lint (Phase 3),
  dependency-graph-lint (with graph fields), state-consistency-lint (Phase 3),
  provenance-lint (Phase 3)}; change-scope ships as canonical-impact-lint's input,
  standalone only if it earns its own invocation.
- **residual_risk:** the deferred checkers' defects (e.g. D13's "134 case files") go
  unlinted until their phase — the same-change review rule covers them interim.

### R12 — Reclassify old roadmap capabilities as parked gaps

- **decision:** accept (executed)
- **evidence:** A2 (Batch-4 atoms), A3 (Batch-5 tail atoms), A4 (router skill), A6 (DQE
  promotion gate) were ADD entries that the still-live evidence shows no current
  consumer activates — A6's own deferral was the canary's (P4).
- **change_made:** PARKED CAPABILITY GAP blocks added to all four entries (File 4) with
  the five fields (gap / evidence_of_need / current_blocked_consumer /
  activation_condition / not_planned_until); A6 explicitly "stays deferred by the
  canary"; A4's convention+checker half still ships with the Phase-3 convention batch
  (only the SKILL promotion is parked); revised slice §8 lists them as out of scope.
- **residual_risk:** parking is a label, not a deletion — the activation conditions must
  be re-checked each phase review or the gaps ossify. Mitigation: each parked block
  names its consumer; the Phase-2 slice's audit (stage 2) re-surfaces the pool.

---

## 2. Guide §13 — the 10 preserved principles (verification, not changes)

| # | Principle | Where it survives the repair |
|---|---|---|
| 1 | mechanism-layer discipline | File 2 §6 census unchanged in shape (SKILL/CONVENTION/AGENTS/SCHEMA/CHECKER/CI/DOC-FORMAT/GIT-PR); only the CHECKER row's set changed (R11) |
| 2 | truth separation | I3 extended (R5), not weakened; E-level rules untouched |
| 3 | no silent promotion | I3 + R5 symmetric demotion rule (stronger than before) |
| 4 | supersession over silent rewrite | I5 + supersession-lint; the slice's archive event is the first practice instance |
| 5 | smallest useful evidence | A8/A10 + M9 TAG basis intact; R10.2 sharpens (decision value first) |
| 6 | context-bounded decomposition | I9 + PSR budget stop-rule untouched; the slice is itself one bounded task |
| 7 | explicit dependencies/shared resources | I10 + R7 (graph authority — the principle, minus the prose-sync defect) |
| 8 | complexity ratchet both directions | I11; the slice's archive move IS the remove-side event; R10.3 fixes the quota distortion |
| 9 | bounded active corpus | File 3 row 13 + metric 1 (indicator form) |
| 10 | DSH as evidence, not template | crosswalk labels (TAG/DT/RSA/MN) untouched; the R3 DSH-adaptation note is a citation, not a copy |

**decision:** all 10 accepted and verified preserved.

## 3. Guide §16 — revised Phase 1 consistency checks (12-point pass)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Every canonical information type has exactly one authority | PASS | File 3 rows 4a/4b/4c + 6a/6b/6c splits; §2 single-map rule; File 2 §5.1 |
| 2 | No target document contradicts another on decision-note lifecycle | PASS | File 1 I5(c)(2) = File 2 §5.4 = File 3 row 8 = File 4 A4/G5 (§5.4) = revised slice §6: all `proposed/decided/rejected/archived/` |
| 3 | No target document uses last_verified as semantic truth | PASS | every remaining occurrence is marked "optional informational, R2" (File 1 Q7, File 2 §5.2/§1.1, File 3 row 2, File 4 G4/repo-bootstrap, File 5 defect 12) |
| 4 | No schema value mixes object type with decision state | PASS | I4.1 13-entry test; `kind` purged from all five files (grep-verified; final patch P3 re-verified) |
| 5 | Weak evidence never implies rejection | PASS | I3(a)/(c)(5); File 5 defects 10A/10B; scenario C basis |
| 6 | Phase 0 labels not mechanically binding on Phase 1 | PASS | matrix header prior/posterior rule; zero current deltas |
| 7 | Phase 2 contains simplification-audit + focused-verification | PASS | revised slice stages 2 and 6 |
| 8 | No checker exists only to synchronize duplicate authorities | PASS | R7 graph-integrity lint (integrity ≠ prose sync); duplicate-fact-lint DETECTS duplicated facts (I2), deferred per R11, and no lint syncs two prose copies |
| 9 | Resolved Phase 0 defects are not called live | PASS | D3/D4/D10 marked resolved-by-commit everywhere (File 1 I6(b), File 3 rows 1/3/16, File 4 A2/A3, File 5 defects 1/6); D6/D12 marked partial with the residual named |
| 10 | Every new persistent artifact has owner/lifecycle/archive rules | PASS | File 3 rows 7/8/12/5 + the §2 new-store list (register, notes, ledger, map, evidence) each with lifecycle + archive + never-delete |
| 11 | Every new Skill has a unique repeated judgment | PASS | File 2 §6 (4 new skills, each with the why-this-must-be-a_skill field); A8 shared across both lifecycles by design (one judgment, one home) |
| 12 | Every eval metric is resistant to obvious gaming | PASS | R10 (a)–(d) applied across File 5 (a.3, adversarial, metrics 1/9/10/11, d.4) |

**12/12 PASS.**

## 4. Guide §19 — do-NOT list compliance (15 items)

| # | Do NOT | Status |
|---|---|---|
| 1 | implement the full target system | kept — doc round + 1 registry line |
| 2 | build all proposed new checkers | kept — none built; 4 specified for the slice, unbuilt |
| 3 | build A2/A3/A4/A6 | kept — all four PARKED (File 4) |
| 4 | rerun a large DSH historical study | kept — crosswalk reused as-is |
| 5 | regenerate Phase 0 from scratch | kept — reconciliation, not regeneration |
| 6 | create a second canonical source map | kept — one manual map (docs/) + thin harness pointer |
| 7 | create a new status super-enum | kept — orthogonal fields, no merged enum |
| 8 | add a route-manager Skill before proven insufficient | kept — ADOPT-LIGHT preserved; A4 skill promotion parked |
| 9 | use last_verified as a semantic freshness gate | kept — demoted to informational |
| 10 | preserve Phase 0 labels by rule | kept — prior/posterior rule |
| 11 | treat E≤2 as a rejection reason | kept — 5 explicit bases instead |
| 12 | impose fixed deletion frequency | kept — planted obsolescence |
| 13 | force the Skill to beat the no-skill baseline | kept — baseline diagnostic |
| 14 | use artifact/skill-count quotas as correctness | kept — indicators + pathology predicates |
| 15 | create permanent docs for git-owned chronology | kept — runlog still REPLACE; results/ still the record |

**15/15 complied.**

## 5. Guide §20 — final acceptance gate (Phase 2)

| # | Gate item | Status |
|---|---|---|
| 1 | post-audit reconciliation completed | DONE (post-audit-reconciliation.md) |
| 2 | current-main live defects re-ranked | DONE (reconciliation §1/§2; 14 still-live, 2 partial, 3 resolved) |
| 3 | decision lifecycle separated from implementation lifecycle | DONE (R3) |
| 4 | orthogonal state model tested against real entries | DONE (I4.1, 13 real entries; final patch P6 re-fit) |
| 5 | weak-evidence/rejection eval corrected | DONE (10A/10B + scenario C) |
| 6 | canonical information model has one owner per fact type | DONE (R6 row splits + single map) |
| 7 | dependency model no longer synchronizes duplicate prose | DONE (R7) |
| 8 | Phase 1 classifications may override Phase 0 | DONE (R8 rule; zero deltas at current census) |
| 9 | eval gaming criteria removed | DONE (R10 a–d) |
| 10 | checker portfolio re-trimmed | DONE (R11) |
| 11 | old roadmap gaps parked unless re-justified | DONE (R12) |
| 12 | revised Phase 2 includes simplification + implementation + focused verification + review | DONE (revised slice: all four + same-change + before/after) |
| 13 | cross-file consistency check passes | DONE (§3 above, 12/12) |
| 14 | architecture-review-disposition.md complete | DONE (this document) |

## 6. Guide citation corrections (evidence found, guide not amended)

1. **R6.2 canonical-source-map paths:** the guide cites `evals/skills/canonical-source-map.md`;
   the actual live path is `evals/skills/harness/canonical-source-map.md`. The guide also
   implies `docs/canonical-source-map.md` exists; it does not — it is the Phase-2
   creation (the single manual authority per the revised design).
2. **§3.1 post-audit commit list:** accurate as found (098f2bb, 4e839b2, 4df8f7f,
   3bb307f verified present).

## 7. Open items (explicit, per the guide's own instruction)

Per guide §20: "If any item remains unresolved, mark it explicitly and request human
review rather than silently choosing."

- **D-1 — canonical "what is next" owner: RESOLVED (final external-review consistency
  patch P1, 2026-09-10): option A accepted** — `docs/plans/active/reconstruction/README.md`
  status table is the single canonical owner of "current execution status / what is
  next"; the D-1 note carries decision_state: decided + implementation_state:
  not_applicable and lands in `docs/decision-notes/decided/` recording the ruling (the
  slice does not self-decide — P8). The D-1_LEFT_OPEN assertion class remains the
  standing guard for future decisions. No open items remain.

## 8. What this round did NOT do (scope record)

- No checker code written; no skill SKILL.md touched (except zero — the registry line is
  the sole live-repo edit, and it is a `meta:` record fix, D6 residual).
- No Phase-2 execution (the slice is specified, not run).
- No historical cost figures rewritten (guide §2 rule 6).
- `docs/plans/` was git-ignored during the repair round (its documents travel to the
  review mirror in `docs/reconstruction-external-review/` under the established
  sanitization rules); the final consistency patch P2 removed the blanket ignore
  (`docs/plans/active/**` + `docs/plans/archived/**` now trackable; the tracking
  transition itself is a Phase-2 slice step).

---

## 9. Final external-review consistency patch (2026-09-10)

The final external review returned **ACCEPTED WITH REQUIRED CONSISTENCY PATCH** (Phase 2:
CONDITIONAL GO) and carried one final ruling. Patch status after execution:

```text
P1 D-1 ruling (canonical status owner): ACCEPTED A — decided everywhere
P2 docs/plans tracking fix: FIXED
P3 deprecated kind field: FIXED (0 live usages in the target set)
P4 Phase-2 eval/checker scope alignment: FIXED
P5 artifact quota residue: FIXED (REPORT ONLY + semantic predicates)
P6 state-space evidence fitting: FIXED (honest coverage; no renamed filler)
P7 route-table authority: FIXED (register = authority; table = generated view)
P8 Phase-2 canonical-store creation: FIXED (slice §4.5 + register seed rule)
```

Focused consistency checks (guide §11), run against the target spec set
(`phase1/` + `revised-phase2-vertical-slice.md` + this file):

- 11.1 decision consistency: D-1 DECIDED in every target document; option A is the only
  selected alternative; implementation_state = not_applicable throughout — **PASS**
- 11.2 tracking consistency: the blanket `docs/plans/` ignore is removed;
  `docs/plans/active/**` and `docs/plans/archived/**` are trackable (verified via
  `git check-ignore`); `docs/plans/local/` + `docs/plans/scratch/` are the explicitly
  ignored ephemeral dirs; the revised slice Stage 5 carries the tracking transition —
  **PASS**
- 11.3 schema consistency: zero live `kind` schema usages in the target set (remaining
  occurrences are historical: the DSH crosswalk's `kind→template` description, the
  rejected-field discussion in R4/I4.1) — **PASS**
- 11.4 checker consistency: Phase-2 minimum set = canonical-impact-lint, archive-lint,
  supersession-lint, decision-note-lint; no Phase-2 gate requires a deferred checker
  (defect 4 + duplicate-count-decreased moved to the Phase-3 gate) — **PASS**
- 11.5 eval consistency: eval-plan's Phase-2 exit criteria now restate the revised
  slice's success criteria (the slice is the named authority for Phase-2 exit) — **PASS**
- 11.6 artifact metric consistency: persistent_artifact_count is REPORT ONLY (indicator
  + the five P5 predicates); no hard ≤2 artifact gate remains — **PASS**
- 11.7 route authority consistency: the decision register is the route authority; the
  route table is a generated/non-authoritative view in every file that mentions it —
  **PASS**
- 11.8 canonical path consistency: every canonical path the slice needs is either
  present or explicitly created in Phase 2 (slice §4.5: `docs/decision-notes/` +
  register + seed rule, `docs/canonical-source-map.md`, the tracked plans dirs) —
  **PASS**

Final status (all acceptance checks above pass):

```text
Phase 1 architecture: ACCEPTED
Phase 2 implementation: GO
```
