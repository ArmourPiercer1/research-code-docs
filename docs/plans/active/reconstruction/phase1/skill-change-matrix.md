# Skill Change Matrix — Proposed Portfolio (Phase 1)

```text
generated_by: phase1-target-synthesis-subagent (S2)
scope:        charter §11 proposed portfolio — one entry per: all 14 current skills
              (S1–S14; the 3 L1 control flows ARE S12/S13/S14, counted once each),
              the eval harness components (H1–H6), the governance components (G1–G6),
              the phase0 ADDs (A1–A6), and the 8 charter §12 candidate changes
              (12.1–12.8, each EVALUATED, not assumed); plus 4 new ADDs this synthesis
              justifies (A7–A10, each tied to a §12 candidate)
schema:       the exact charter §11 YAML schema (all 21 fields per entry)
inputs:       ../phase0/existing-skill-classification.md (labels — proposed_action MUST
              match; disagreements stated with evidence); ../phase0/current-system-map.md
              (B/C/E/G); ../phase0/pain-point-evidence.md; both DSH intermediates;
              phase1/dsh-transferability-crosswalk.md (§7 labels, cited as "crosswalk: Mx");
              File 1 (Q-answers, invariants); File 2 (capability decisions); File 3 (owners)
date:         2026-09-09
status:       DRAFT-for-review (architecture proposal, pending human review per charter §15)
```

Label agreement (repair round, R8 — prior/posterior rule): the phase0 classification
label is the PRIOR (`phase0_label`); this matrix is the POSTERIOR (`phase1_label`). Any
delta (phase1_label != phase0_label) must carry a `delta_reason` + the new evidence in
the entry. Census at the 3bb307f re-verification: KEEP×15, REFINE×7, SPLIT×1 SWR,
MERGE×1 register_check→run_checks, REPLACE×1 runlog, REMOVE×1 creation-roadmap, ADD×6
A1–A6 — zero deltas (the header's old "KEEP×13" undercounted; §6 below explains the
15 = 9 skills + 6 harness mechanisms). Where this matrix disagrees with a naive reading,
the disagreement is stated in `why_this_must_be_a_skill` with evidence. Entries without a
convincing `why_this_must_be_a_skill` default to another mechanism (named) or removal —
per charter §11 and File 2 §6.

---

## 1. Current skills (S1–S14)

```yaml
name: documentation-quality-evaluator (DQE)
problem: decide, within an admitted evaluation profile, whether a document passes the
  quality standard (hard-fail catalog + rubric + scoring), advisory-scoped
current_owner: .agents/skills/documentation-quality-evaluator/SKILL.md (v0.4.1) +
  harness (rubric.md, hard-fail.md, golden-negative corpus, 5 SIGNAL checkers)
proposed_action: refine   # phase0 S1 = REFINE (agreed)
why_this_must_be_a_skill: repeated non-trivial judgment (grading within profile; the
  v0.2 false pass P2 proves uncalibrated judgment fails); REFINES: (1) grader envelope
  ~860 lines split so the injected context is bounded (classification S1.1; I9);
  (2) EVALUATOR_CONTRACT duplicated in make_grading_injection.py moves to the harness
  only (H3); (3) terminal-gate promotion stays DEFERRED behind A6 (canary P4; File 1 I7)
trigger: an admitted-profile document needs a pass/fail quality verdict (flow stage or
  manual); the eoopt golden-negative regression
non_trigger: judging a RESEARCH claim's evidence strength (→ UDM/RES); checking
  mechanical invariants (→ run_checks tiers); design/rewrite (→ DIA/TDR)
inputs: document + profile + rubric/hard-fail + corpus case
outputs: verdict JSON (per-claim audit, HF hits, score) + report; advisory — authorizes nothing
canonical_or_transient: transient (verdicts are records under results/; File 3 row 6)
reads: the graded document, rubric, hard-fail, case manifest
writes: results/<run>/ only
upstream: (flows: DR/SWR/NRSD doc stages) / direct
downstream: flow-state gate (advisory), human review
invariants: Rule 0 profile admission; no-fact-upgrade (D.8); non-compensatory scoring;
  golden-negative recall 1.0 / false_pass 0 (README:42-43)
mechanical_checks: 5 SIGNAL checkers (never auto-block, existing); state-number
  consistency planted-contradiction (smoke); planted-defect self-test
failure_modes: gate erosion (P2 history); LLM-signal instability across runs (P2/P4 —
  why it stays advisory); over-triggering on non-admitted profiles (Rule 0 guard)
evals: 23 trigger / 5 conflict / 10 task-quality (eval-coverage-baseline); blind matrix;
  golden-negative regression every run (existing)
dsh_basis: M17 DN (anti-golden doctrine does NOT transfer — goldens are the point here);
  M23 TAG (reliability doctrine: no masking, recorded rejections); crosswalk M17/M23
research_specific_delta: the "profile admission + honest INCOMPLETE" pattern is the
  research adaptation of DSH's honest self-skip (M24 TAG) — an unadmitted profile is a
  loud non-verdict, not a silent pass
```

```yaml
name: project-state-reconstructor (PSR)
problem: recover, read-only, what a repository ACTUALLY is (exists/runs/tested/validated),
  separating current fact from stale doc from historical intent
current_owner: .agents/skills/project-state-reconstructor/SKILL.md (v0.2.0)
proposed_action: keep   # phase0 S2 = KEEP (agreed)
why_this_must_be_a_skill: the system's load-bearing detector; fact recovery under a
  context budget with no-fabrication is repeated non-trivial judgment; every other
  capability reads its output (File 2 §1.3)
trigger: resuming/entering an unfamiliar or drifted repo; before any simplification or
  reconstruction (the Phase-2 slice entry point)
non_trigger: judging doc quality (DQE); designing IA (DIA); recovering a single
  known file (plain read)
inputs: repo tree (≤~2,000 focused lines; stop-and-summarize near 5,000)
outputs: state report (exists/tracked/clean/runs/tested/validated, each with locator)
canonical_or_transient: transient (report); its FACTS feed the canonical owners (File 3 rows 1–4)
reads: repo (read-only; verified by git porcelain)
writes: none (read_only — enforced by the shadow-run check)
upstream: (entry point)
downstream: WFI, GSWE, DIA, CCM, DR/SWR/NRSD flows, the Phase-2 slice
invariants: no-fabrication; "structured-to-run ≠ runs" (E2 cap); read-only (git
  porcelain clean); budget stop rule
mechanical_checks: read-only shadow run (existing, registry:198); reader test
  (OVERCLAIM_DETECTED=NO)
failure_modes: over-interpretation (the no-skill baseline's measured failure,
  registry:198); budget blowout on large repos
evals: 23 trigger / 5 conflict / 2 task-quality (eval-coverage-baseline); e2e no-
  fabrication case; task-quality runs to be RECORDED (D8 gap)
dsh_basis: M11 DT (incident→guardrail: PSR is the detector half of the loop); M1 DT
  (resume set, File 1 Q9)
research_specific_delta: research repos add the "notebook output = claim, not evidence"
  class (File 5 §c defect 7) — PSR's E-level vocabulary already carries it
```

```yaml
name: goal-scope-and-workflow-elicitor (GSWE)
problem: turn a fuzzy ask into a scoped goal + open-decision list, one question at a
  time, stopping when answerable
current_owner: .agents/skills/goal-scope-and-workflow-elicitor/SKILL.md (v0.2.0)
proposed_action: keep   # phase0 S3 = KEEP (agreed)
why_this_must_be_a_skill: adaptive elicitation with a stop rule is repeated non-trivial
  judgment; P8 (baseline "decided" D-1 by fiat) is the measured failure of its absence
trigger: a new task/project arrives under-scoped; a flow reaches the elicitation stage
non_trigger: grilling an existing decision (grilling skill); running a search (RQLP);
  a fully-specified mechanical change
inputs: the ask + repo state (PSR report)
outputs: goal-scope note (persistence: transient) + open-decisions list (feed to UDM)
canonical_or_transient: transient (File 1 Q6); the open-decisions ENTRIES become
  canonical in the register (File 3 row 7)
reads: ask, PSR state
writes: none (plan files only)
upstream: PSR
downstream: UDM, flow-state open_decisions (as POINTERS — I1), NRSD front
invariants: one question at a time; stop-when-answerable; never decide for the user
  (the P8 discipline); open decisions handed off, not silently closed
mechanical_checks: flow-state open_decisions pointer-check (new, I1); no-skill-baseline
  regression "D-1_LEFT_OPEN" (File 5 §c)
failure_modes: deciding open decisions by fiat (P8 — the baseline case); over-eliciting
  (stop-rule violation)
evals: 23 trigger / 5 conflict / 2 task-quality (eval-coverage-baseline); multi-turn
  cases exist, runs unrecorded (D8)
dsh_basis: M2 RSA (decision capture with mandatory handoff); M22 TAG (verify the
  artifact, not the report)
research_specific_delta: the "never decide for the user" rule is load-bearing for
  research routes (Q15) — a research repo cannot bank decisions the way a product repo can
```

```yaml
name: uncertainty-and-decision-manager (UDM)
problem: manage the decision register — state, evidence strength (E-levels), reversal
  conditions, honest BLOCKED — for ideas/hypotheses/candidates/decisions
current_owner: .agents/skills/uncertainty-and-decision-manager/SKILL.md (v0.2.0) +
  standalone register_check.py
proposed_action: keep   # phase0 S4 = KEEP (agreed; §12.6 refine applies to its SCHEMA,
  see entry 12.6 — the skill itself is kept, the register schema is refactored)
why_this_must_be_a_skill: epistemic state management is the system's core repeated
  judgment (strength calibration, promotion E3+ rule, reversal judgment); the standalone
  register_check is a runner-integration gap, not a skill defect (classification S4/H2)
trigger: any idea/hypothesis/candidate enters the register; a decision reverses; a flow
  hits an unresolvable open decision (honest BLOCKED)
non_trigger: evidence SYNTHESIS (RES); doc quality (DQE); routing (conflict-matrix)
inputs: claim/decision + evidence (RES maps) + register
outputs: register entries (canonical in docs/decision-register.md — File 3 row 7),
  BLOCKED flow-states, decision notes (durable rationale — File 3 row 8)
canonical_or_transient: canonical (register + notes) — the one skill that writes canonical stores
reads: register, evidence maps, flow-state
writes: docs/decision-register.md, docs/decision-notes/**
upstream: GSWE, RES, PSR, user rulings
downstream: every flow (decision gates), CCM (decision-triggered migrations), File 5 evals
invariants: E3+ before "verified" (SKILL.md:22-29); supersedes/superseded_by lineage
  (SKILL.md:51-53); honest BLOCKED with named blocked_by; orthogonal fields after 12.6
mechanical_checks: register_check → MERGED into run_checks.py HARD for register files
  (H2); supersession-lint; revisit-condition presence (File 1 I5)
failure_modes: dimension conflation (Q11.1 — fixed by 12.6 schema); register drift from
  the notes (supersession-lint); silent promotion (I3)
evals: 23 trigger / 5 conflict / 2 task-quality (eval-coverage-baseline); planted
  VERIFIED-at-E2 case (register_check must flag — existing self-test pattern)
dsh_basis: M2 RSA (decision notes with mandatory alternatives + richer research
  provenance); M16 DN (the enforced-vocabulary fix is our §12.6 orthogonalization, not
  a board)
research_specific_delta: routes (object_type: route) and experiments (object_type: experiment, R4) live in
  the SAME register (File 2 §3.3/§3.6) — the research delta vs DSH's software-only 6-class set
```

```yaml
name: workspace-forensics-and-inventory (WFI)
problem: bounded read-only inventory of what exists (tree, orphan candidates, high-
  signal files) under a context budget
current_owner: .agents/skills/workspace-forensics-and-inventory/SKILL.md (v0.1.0)
proposed_action: refine   # phase0 S5 = REFINE (agreed)
why_this_must_be_a_skill: sampling judgment under budget is repeated non-trivial; REFINES
  the loose PSR co-ownership on "candidate canonical source" (classification S5; §3.3
  prob-1): WFI INVENTORIES and PROPOSES candidate homes only as flagged candidates — DIA
  DECIDES, File 3 row 5.1 records (the 4-assigner collapse, File 1 I2). Disagreement note:
  phase0 left open consolidation vs boundary-prose (crosswalk M20: drift already caught
  by dogfood PSR audit) — this matrix chooses boundary-prose FIRST (cheaper; the
  consolidation question re-opens at Phase 4 if the boundary keeps leaking).
trigger: entering a repo for inventory; before DIA design; before simplification audit
non_trigger: state FACT recovery with locators (PSR); judging quality (DQE); moving
  anything (CCM)
inputs: repo tree (shallow + sampled high-signal)
outputs: inventory + orphan candidates + candidate canonical sources (flagged)
canonical_or_transient: transient (inventory report)
reads: repo (read-only)
writes: none
upstream: PSR (or direct on small repos)
downstream: DIA, CCM, simplification-audit (A8), DR/SWR flows
invariants: read-only; never a raw whole-tree dump (registry:190); "runs/passes"
  assertions forbidden (lane violation the reader-test guards)
mechanical_checks: read-only shadow run; reader test (OVERCLAIM_DETECTED=NO,
  registry:198)
failure_modes: over-interpretation (blurring inventory with interpretation — the
  baseline's measured failure, registry:198); boundary leak into PSR territory
evals: 6 trigger / 2 conflict (eval-coverage-baseline)
dsh_basis: M13 TAG (inventory derivation, never hand-maintained); M3 DT (trigger contract)
research_specific_delta: research inventories must distinguish result artifacts that are
  reproducible vs not (§12.2 target list) — the orphan-candidate class is wider than code
```

```yaml
name: document-information-architect (DIA)
problem: design the target information architecture for a hybrid doc/corpus: doc-roles,
  one canonical home per info-type, audience/frequency/lifecycle, split plan
current_owner: .agents/skills/document-information-architect/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S6 = KEEP (agreed)
why_this_must_be_a_skill: information-architecture design is repeated non-trivial judgment;
  strong evidence — the shadow run on the eoopt hybrid roadmap beat the no-skill baseline
  (11 roles, one canonical home per info-type; baseline "drifted into rewrite/execute +
  silent decisions", registry:229-231). It is the DESIGN counterpart to DQE's HF-13
  (SKILL.md:26-31) and the single canonical-home DECIDER in the target (File 2 §5.1).
trigger: one document carries multiple doc-roles; a corpus has overlapping/duplicated
  responsibilities needing a target architecture
non_trigger: judging a doc (DQE); rewriting (TDR); moving files (CCM); naming domain
  terms (domain-modeling)
inputs: target corpus + WFI inventory + PSR state + File 3 owner table
outputs: document-artifact-map + canonical-home assignments (frozen interface) + open
  decisions — a PLAN, not a rewritten doc
canonical_or_transient: transient plan; its canonical-home DECISIONS are recorded in
  File 3 row 5.1 (docs/canonical-source-map.md) — decision, not the plan file
reads: doc-set + inventory/state; no whole-repo scan
writes: plan files only (read_only scope, registry:220)
upstream: WFI, PSR
downstream: CCM, TDR, the Phase-2 slice (IA of the governance corpus)
invariants: one canonical home per info-type; facts marked provisional-needs-PSR
  (SKILL.md:145) — never self-verified; plan not execution
mechanical_checks: document-artifact-map.schema.md + interface_check (existing)
failure_modes: over-triggering on any writing task (creation-roadmap:75 — restrict to
  "corpus/mixed/needs type-split"); drifting into rewrite/execute (registry:229)
evals: 6 trigger / 2 conflict / 1 reader (eval-coverage-baseline); eoopt shadow run
dsh_basis: M12 DT (one-home-per-fact tier taxonomy — DIA is the judgment half; File 3
  is the record half; M12 crosswalk: "rebuilt around our fact types, not DSH's table")
research_specific_delta: research corpora mix evidence/decision/plan roles that software
  doc tiers don't have — the doc-role set is the research delta
```

```yaml
name: research-question-and-literature-planner (RQLP)
problem: turn an open/fuzzy research question into a reviewable literature-search-plan,
  then route execution to the installed retrieval stack
current_owner: .agents/skills/research-question-and-literature-planner/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S7 = KEEP (agreed; OQ-4 merge question answered by its
  own Track-B evidence: keep separate from RES)
why_this_must_be_a_skill: scoping a reviewable search plan under a stop criterion is
  repeated non-trivial judgment; the thin-adapter boundary ("never retrieves, never reads,
  never synthesizes") is what keeps it composable
trigger: an open research question needs scoping before search; the NRSD flow reaches
  the literature step
non_trigger: running the survey (lit-review); WoS iterative search (wos-research); a
  known single paper (paper-fetch-skill); organizing retrieved evidence (RES)
inputs: the question + decision context
outputs: literature-search-plan (persistence: transient)
canonical_or_transient: transient (File 1 Q6); its stop-criteria feed the register
reads: question + decision context; no retrieval
writes: plan only
upstream: GSWE (open question), NRSD front
downstream: L3 retrieval stack (wos-research / scansci-pdf / paper-fetch-skill /
  lit-review), RES (on retrieval)
invariants: never retrieves/reads/synthesizes; stop criteria mandatory; scope in/out
  explicit
mechanical_checks: plan schema completeness (interface-style check); L3 roster vs disk
  (preflight extension — closes D11: deep-research listed but absent)
failure_modes: routing to an uninstalled L3 (D11 class — preflight closes it); scope
  creep into execution
evals: 6 trigger / 2 conflict (eval-coverage-baseline)
dsh_basis: M3 DT (frontmatter trigger contract + non-trigger lists as the routing
  mechanism); M24 TAG (external-dependency honesty — listed-≠installed)
research_specific_delta: the whole skill IS the research delta (DSH has no retrieval-
  planning equivalent)
```

```yaml
name: research-evidence-synthesizer (RES)
problem: synthesize retrieved/project evidence into claims with E-levels and channel
  separation (literature / project / inference)
current_owner: .agents/skills/research-evidence-synthesizer/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S8 = KEEP (agreed; E-level duplication with UDM is by
  design — same vocabulary, classification S8 note)
why_this_must_be_a_skill: weighing evidence into calibrated claims (no fact-upgrade,
  analogy capped E2) is repeated non-trivial judgment; the shadow run verified the
  boundary (registry:280-288)
trigger: retrieved evidence needs organizing into claims; a route needs an evidence map
non_trigger: planning the search (RQLP); deciding (UDM); judging doc quality (DQE)
inputs: retrieved evidence (L3 outputs) + project results + register
outputs: evidence-synthesis output (claims + E-levels + channel tags) — merges into the
  persistent topic map (File 3 row 5)
canonical_or_transient: transient per run; MERGED claims are canonical in
  docs/evidence/<topic>-evidence-map.md (File 3 row 5)
reads: retrieval outputs, project results
writes: results/ per run + the topic evidence map (merge)
upstream: RQLP (plan) + L3 stack, experiment results (File 2 §3.7)
downstream: UDM (E-level updates), 12.5 discriminating-experiment, DQE (FACTUAL_VALIDITY context)
invariants: channel separation; no fact-upgrade (D.8); E3+ = verified floor (with UDM);
  provenance field per claim (source, fetched, license)
mechanical_checks: provenance-lint (new — required fields on claim entries);
  corpus non-mutation (existing)
failure_modes: literature-vs-project conflation (I3/Q16 — the lint + DQE catch it);
  synthesis drift into decision-making (boundary to UDM)
evals: 6 trigger / 2 conflict (eval-coverage-baseline); planted fact-upgrade case
dsh_basis: M2 RSA (richer research provenance than DSH's 6-class notes); M13 TAG
  (derive provenance, never hand-maintain it)
research_specific_delta: the whole skill is the research delta; the persistent topic map
  (File 3 row 5) is NEW — DSH has no evidence store
```

```yaml
name: content-canonicalization-and-migration (CCM)
problem: plan the canonical migration (move/delete/rewrite map) for a corpus; (target:
  apply an approved map) — dry-run planner today
current_owner: .agents/skills/content-canonicalization-and-migration/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S9 = KEEP (agreed) — planning skill kept; the missing
  APPLY half is ADD A1 (separate entry), so CCM itself takes no new label
why_this_must_be_a_skill: migration PLANNING (what moves where, which facts restate
  what) is repeated non-trivial judgment; the invariants themselves stay checker-
  enforceable (existing self-test catches planted violations)
trigger: a canonical-home decision (DIA) needs a migration plan; a corpus restructure
  is approved
non_trigger: deciding homes (DIA); applying (A1); judging (DQE)
inputs: canonical-source-map (File 3 row 5.1) + inventory + decisions
outputs: migration map (may_move / may_delete / may_overwrite=false; no target==source;
  no duplicate primary) — dry-run
canonical_or_transient: transient plan; applied state is canonical in the target owners
reads: corpus + inventory + decisions
writes: none (dry-run; plan files only)
upstream: DIA, UDM (decision), WFI
downstream: A1 (apply), TDR (rewrite stage), LDM (post-change impact)
invariants: may_move/delete/overwrite=false; no target==source; no duplicate primary;
  sha256 source unchanged; human write-approval boundary (HUMAN-APPROVAL)
mechanical_checks: existing CCM checker self-test (planted violations caught);
  interface_check
failure_modes: plan drift between planning and apply (A1 re-verifies invariants at
  apply time); silent overwrite (boundary + checker)
evals: 6 trigger / 2 conflict (eval-coverage-baseline)
dsh_basis: M18 TAG (relocation-never-edit archive semantics feed the may_delete rule);
  M13 TAG (derive the inventory)
research_specific_delta: research migrations move EVIDENCE and DECISION artifacts, which
  carry provenance fields that must survive the move (provenance-lint at apply)
```

```yaml
name: technical-document-rewriter (TDR)
problem: rewrite a document candidate within scope — candidate-only, no fact-upgrade,
  source preserved
current_owner: .agents/skills/technical-document-rewriter/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S10 = KEEP (agreed)
why_this_must_be_a_skill: candidate-quality rewriting under hard scope constraints is
  repeated non-trivial judgment; the checker self-test proves the mechanical half
  (planted hypothesis-as-fact caught) — the craft stays with the skill
trigger: an approved change needs the actual text rewrite (post-CCM plan or LDM
  same-change update)
non_trigger: judging (DQE); planning moves (CCM); deciding content (UDM/GSWE)
inputs: source doc + scope decision (what may change)
outputs: candidate doc + rewrite-provenance-report (sha256 source, candidate≠source,
  no fact-upgrade)
canonical_or_transient: transient candidate (until human approval promotes it);
  provenance report is a record
reads: source doc + scope
writes: candidate file only (never the source — enforced)
upstream: CCM plan, UDM/GSWE decisions, LDM impact list
downstream: human approval (HUMAN-APPROVAL), then the canonical owner; DQE (advisory re-check)
invariants: source sha256 unchanged; candidate≠source; no fact-upgrade (OPEN/HYPOTHESIS
  stay OPEN/HYPOTHESIS); no silent decision (P8)
mechanical_checks: existing TDR checker self-test; sha256 guard (existing); state-
  consistency-lint on the candidate (new)
failure_modes: fact-upgrade under rewrite pressure (P8 disease — checker + DQE catch);
  scope creep (boundary + scope field)
evals: 6 trigger / 2 conflict (eval-coverage-baseline); planted fact-upgrade case
  (existing, caught)
dsh_basis: M30 TAG (repo prose = current-state facts, not session transcript — TDR's
  no-fact-upgrade is the rewrite-side instance); M22 TAG (verify the artifact)
research_specific_delta: research rewrites must preserve channel tags and E-levels
  (the provenance pattern generalized from rewrite-provenance-report, File 1 I3)
```

```yaml
name: living-design-maintainer (LDM)
problem: after a change, find which current-state docs are invalidated (maintenance
  impact + stale-reference list) — proposal-only today
current_owner: .agents/skills/living-design-maintainer/SKILL.md (v0.1.0)
proposed_action: refine   # phase0 S11 = REFINE (agreed)
why_this_must_be_a_skill: judging WHICH docs a change invalidates and HOW to update them
  minimally is repeated non-trivial judgment (kept); REFINES per §12.8: the output becomes
  impact-set → SAME-CHANGE owner updates (the S11 defect was "proposal-parallel
  maintenance outputs that duplicate the same-change update path", classification S11);
  a standalone report survives only for explicit review value. The mechanical half
  (detecting stale impact) moves to canonical-impact-lint + dead-pointer check (R2).
trigger: after any change touching a canonical owner (or its declared scope); the
  Phase-2 slice stage 4
non_trigger: first-time design (DIA); rewriting for quality (TDR); judging (DQE)
inputs: the change (diff/summary) + File 3 owner table
outputs: impact set + same-change owner updates (or optional standalone report)
canonical_or_transient: transient (impact set); the OWNER UPDATES it produces are the
  canonical writes (via the write-approval boundary)
reads: change + owner table + current-state docs
writes: owner updates under HUMAN-APPROVAL (existing boundary)
upstream: any change (CCM apply, TDR, code), DQE flags
downstream: canonical owners (File 3 rows 2–4, 14); archive-lint (stale banners)
invariants: proposal-only → same-change (refine); approved:false until applied; no
  auto-publish (existing)
mechanical_checks: canonical-impact-lint (new — same-change impact discharge, R2); dead-pointer
  check (new — VOID/archived targets); existing LDM checker (approved:false)
failure_modes: parallel-artifact disease (S11 — the refine fixes it); missing owner
  (D-1 — DECIDED by the final ruling, option A; the slice's note records it, File 2 §7)
evals: 6 trigger / 2 conflict (eval-coverage-baseline); planted stale-claim case
  (new, File 5 §c defect 1)
dsh_basis: M30 TAG (dead references are a defect class — the checker half); M12 DT
  (current-state doc ownership + budgets); M18 TAG (archive as relocation-never-edit)
research_specific_delta: research docs rot via EVIDENCE supersession (a new result
  falsifies a claim) — the impact set must include evidence-map claims, not just doc text
  (crosswalk M19: extend supersession to evidence)
```

```yaml
name: documentation-refactor (DR) — L1 control flow
problem: the first closed loop: reconstruct → design → plan → rewrite → evaluate a doc
  corpus end-to-end (dry-run + candidate scope)
current_owner: .agents/skills/documentation-refactor/SKILL.md (v0.1.0, Sprint 6B closed
  the first real loop — registry:331-333)
proposed_action: refine   # phase0 S12 = REFINE (agreed)
why_this_must_be_a_skill: L1 orchestration = repeated non-trivial routing/orchestration
  judgment across 6+ atoms with honest-BLOCKED discipline; REFINES: SKILL.md:47 "v0
  SKELETON STOPS HERE… NOT BUILT" is one day stale vs Sprint 6B (D3) and conflict case
  docref-conf-03 is stale (expects BLOCKED, flow now COMPLETEs for dry-run+candidate —
  D4): the same-change update rule (File 1 I6) applies to the flow's own SKILL.md;
  the stale case gets re-baselined (dataset_version bump, D4's closure trigger).
trigger: a doc corpus needs end-to-end reconstruction/refactor (the Phase-2 slice)
non_trigger: single-doc fix (TDR directly); design only (DIA); evaluation only (DQE)
inputs: corpus + PSR state + decisions
outputs: flow-state (HONEST-BLOCKED or COMPLETE for dry-run+candidate scope) + the
  atoms' artifacts (plan, map, candidate, verdict)
canonical_or_transient: transient (flow-state → results/<run>/); core artifacts per
  File 1 Q14 (2–3 per run, rest transient/record)
reads: corpus, atoms' outputs
writes: flow-state + staging (atom writes under their own boundaries)
upstream: (entry: PSR stage)
downstream: WFI → GSWE → DIA → CCM → TDR → DQE → LDM (call chain, registry:331)
invariants: exactly-one-L1-at-a-time (conflict-matrix DENY); honest BLOCKED with named
  blocked_by; completion semantics = dry-run+candidate, NOT applied (manifest:71-73);
  0 source files changed in dry-run (sha256)
mechanical_checks: flow_state_check (existing); interface_check (existing); sha256
  0-footprint (existing); duplicate-fact-lint before/after (new — the slice's proof)
failure_modes: stale builtness claims (D3 class); artifact inflation (Q14 — the
  10-artifact/run class); silent decisions (P8)
evals: 6 trigger / 3 conflict (eval-coverage-baseline; docref-conf-03 re-baselined per
  D4); the Phase-2 slice IS scenario-A workflow eval (File 5 §b)
dsh_basis: M11 DT (postmortem→guardrail: the Sprint 6B closure is the loop's evidence);
  M21 DN (research alternatives are not PR stacks — the flow stays linear, correctly)
research_specific_delta: the corpus is GOVERNANCE + RESEARCH docs, not product docs —
  the loop's DQE stage is profile-scoped (Rule 0) because research docs are often
  non-admitted (honest INCOMPLETE, not forced verdicts)
```

```yaml
name: scientific-workspace-reconstruction (SWR) — L1 control flow
problem: reconstruct a scientific workspace end-to-end (recovery prefix + research-
  workspace tail)
current_owner: .agents/skills/scientific-workspace-reconstruction/SKILL.md (v0.1.0)
proposed_action: split   # phase0 S13 = SPLIT (agreed — the only SPLIT)
why_this_must_be_a_skill: the RECOVERY PREFIX stays an L1 skill (orchestration judgment,
  proven by the DR loop); the TAIL cannot complete its own scope (blocked at
  dev-test-experiment-workspace-architect + 4 atoms, SWR SKILL.md:49 class) and the
  structurally-identical recovery prefix is DUPLICATED across all three flows
  (classification S13; crosswalk B.5 base+patches pattern: two N%-identical trees →
  extract the shared part). SPLIT into: (a) the shared recovery prefix, extracted ONCE
  (a convention + the DR flow's stages — not a third skill: extracting it as a skill
  would create a 4th orchestration layer, violating charter §0); (b) the SWR tail,
  parked as a `proposed/`-style frozen scope (crosswalk M4 DT: freeze decisions, not
  formats; DSH frozen side-branch pattern B.6: keep archaeology, drop the claim) until
  the Batch-4 atoms exist.
trigger: a scientific workspace (code + data + experiments) needs reconstruction
non_trigger: doc-only corpus (DR); numerical design front (NRSD)
inputs: workspace + PSR state
outputs: flow-state (recovery prefix: COMPLETE-capable; tail: HONEST-BLOCKED with named
  blocked_by — the current honest state, kept)
canonical_or_transient: transient
reads: workspace, atoms' outputs
writes: flow-state + staging
upstream: (entry: PSR stage, shared prefix)
downstream: WFI → GSWE → (prefix ends at design; tail: research atoms)
invariants: honest BLOCKED (existing — the tail's boundary is the system's best honest
  claim, D14 shows even it goes stale → impact-set discharge, R2/I6); exactly-one-L1-at-a-time
mechanical_checks: flow_state_check; the tail's blocked_by must name EXISTING atoms
  (dependency-graph-lint — the D14 class becomes a lint: a "not built" claim must match
  the roster)
failure_modes: unbuildable tail claimed as scope (the SPLIT reason); prefix
  re-duplication (fixed by the shared extraction)
evals: 6 trigger / 3 conflict (eval-coverage-baseline)
dsh_basis: M4 DT (freeze, don't half-build); B.6 frozen side-branch (park with
  archaeology); M6 TAG (the shared prefix is the "one source" for the 3 flows)
research_specific_delta: the tail's blocked atoms are RESEARCH-workspace-specific (dev-
  test-experiment architecture) — the split is the research delta vs a generic DR
```

```yaml
name: numerical-research-software-design (NRSD) — L1 control flow
problem: the research-design front: question → literature → evidence → design candidates
  for numerical research software
current_owner: .agents/skills/numerical-research-software-design/SKILL.md (v0.1.0)
proposed_action: keep   # phase0 S14 = KEEP (agreed — "evidence-front is real and
  valuable; blocked tail is a known ADD, flow is honest")
why_this_must_be_a_skill: the research-design orchestration (route the question through
  RQLP → retrieval → RES → design candidates, holding honest BLOCKED at the Batch-4
  boundary) is repeated non-trivial judgment; the 10-upstream call chain (NRSD SKILL.md:
  40-60) is exactly the context-boundary stress I9 names — kept, with the executor-
  contract convention (File 2 §4.2) as the mitigation, not a redesign
trigger: a numerical research question needs end-to-end design support
non_trigger: single-paper questions (paper-fetch-skill); doc refactors (DR)
inputs: question + repo context
outputs: literature plan → evidence map → design candidates + flow-state (HONEST-
  BLOCKED at the 6 Batch-4 atoms — the known ADD, kept honest)
canonical_or_transient: transient per run; evidence maps merge to File 3 row 5
reads: question, PSR state, L3 stack
writes: flow-state + staging + evidence-map merge
upstream: (entry: GSWE/RQLP stage)
downstream: RQLP → L3 stack → RES → (Batch-4 atoms: BLOCKED)
invariants: honest BLOCKED at the Batch-4 boundary (existing); evidence front never
  skips to "the plan" (I3: candidates stay candidates)
mechanical_checks: flow_state_check; provenance-lint on the evidence map (new);
  blocked_by names existing/planned atoms (dependency-graph-lint)
failure_modes: silent promotion of a candidate to "the plan" (I3 — the Q15 discipline);
  tail claimed as built (D14 class → builtness-claim vs roster, R7)
evals: 6 trigger / 3 conflict (eval-coverage-baseline); the manifold-transfer e2e (real
  evidence base — File 5 §b scenario C input)
dsh_basis: M2 RSA (decision notes for the design candidates); M9 TAG (smallest
  discriminating experiment at the design fork — the 12.5 skill plugs in here)
research_specific_delta: the whole flow is the research delta; its blocked tail (6
  Batch-4 atoms) is the single largest honest-BLOCKED surface in the system
```

---

## 2. Eval harness components (H1–H6)

```yaml
name: run_checks.py (harness runner)
problem: run the deterministic checker tiers (HARD / ADVISORY / SIGNAL) over paths
current_owner: evals/skills/run_checks.py
proposed_action: keep   # phase0 H1 = KEEP (agreed — "tier model is sound; integration
  gap only")
why_this_must_be_a_skill: N/A — NOT a skill; it is the CHECKER mechanism (charter §10:
  deterministic checker, no skill restating it). Kept as the runner; REFINED by
  absorbing register_check (H2) + the 4 Phase-2 minimum lints (File 2 §6) into its tier
  lists now (the 6 deferred lints join at each build phase, R11).
  Disagreement note vs a naive "keep": the tier bookkeeping already drifts (D5: manifest
  lists markdown_links/placeholders under signal, runner classifies ADVISORY; register_
  check not registered at all) — the runner becomes the SINGLE source of the tier
  inventory (crosswalk M6 TAG: "single source of truth for the check inventory, tested,
  fail-fast") with a manifest-consistency self-test.
trigger: preflight / PR / manual invocation
non_trigger: model-level grading (DQE); flow-state checks (flow_state_check)
inputs: paths + tier selection
outputs: per-checker results + exit code (HARD blocks; ADVISORY/SIGNAL never auto-block)
canonical_or_transient: transient (results are records)
reads: repo
writes: none
upstream: preflight, CI (when added), the slice
downstream: release gate, the lints
invariants: tier semantics (HARD blocks, SIGNAL never auto-blocks — P2/P5 no-masking
  doctrine); inventory = single source (D5 fix)
mechanical_checks: self-test with planted defects (existing pattern, H5); manifest
  consistency check (new)
failure_modes: tier drift (D5 — the self-test closes it); orphan checkers (H2 — the
  merge closes it)
evals: planted-defect self-tests per checker (existing); the adversarial battery (File 5 §c)
dsh_basis: M6 TAG (gate runner as single source of inventory); M5 TAG (narrow local
  tier vs exhaustive outer)
research_specific_delta: the SIGNAL tier's "never auto-block" is the research adaptation
  of DSH's advisory doctrine — LLM-judged and statistical signals stay advisory (P2/P4)
```

```yaml
name: register_check.py (harness checker)
problem: flag illegal/insufficient decision-register states (e.g., VERIFIED at E≤2)
current_owner: evals/skills/register_check.py (STANDALONE — run directly by UDM)
proposed_action: merge   # phase0 H2 = MERGE into run_checks.py's tier system (agreed —
  the only MERGE in the portfolio)
why_this_must_be_a_skill: N/A — a CHECKER. Merger rationale: it is not registered in
  run_checks.py (classification H2; D5) — the E≤2 flag (the I3 mechanical half) is
  skippable today because it is not in the runner's path. Merged as HARD for
  decision-register files. No new behavior; only its ENFORCEMENT path changes.
trigger: any change touching decision-register files (via the runner)
non_trigger: n/a
inputs: register files
outputs: HARD flags (VERIFIED/FACT at E≤2; missing lineage fields)
canonical_or_transient: transient
reads: docs/decision-register.md + decision notes
writes: none
upstream: run_checks.py
downstream: release gate
invariants: E3+ before verified (UDM SKILL.md:22-29); supersession lineage present
mechanical_checks: its own planted-case self-test (existing pattern)
failure_modes: orphaning (the H2 defect — closed by the merge)
evals: planted VERIFIED-at-E2 case (existing); adversarial defect 5 (File 5 §c)
dsh_basis: M16 DN (the vocabulary enforcement is local: our fix is the runner merge +
  §12.6 fields, not a policy engine)
research_specific_delta: after 12.6, the checker validates ORTHOGONAL fields (role-
  mixing rule, File 1 I4) — the research status model is richer than DSH's
```

```yaml
name: make_grading_injection.py (harness builder)
problem: build injection prompts + grading envelopes for skill evals (trigger/conflict/
  task-quality/reader)
current_owner: evals/skills/make_grading_injection.py (+ make_injection.py, make_batch.py)
proposed_action: refine   # phase0 H3 = REFINE (agreed)
why_this_must_be_a_skill: N/A — harness tooling (CHECKER/TEST mechanism). REFINES:
  EVALUATOR_CONTRACT duplicates DQE's gate-derivation/profile logic already in SKILL.md
  (classification H3) — the contract lives in ONE place (the harness); the injection
  script consumes it. Also: the new eval dimensions (File 5 §a: write-scope, interface,
  fact/hypothesis separation, refuse-to-overclaim, checker compatibility, context
  boundedness) are added as case TYPES here, reusing make_injection/make_batch/make_
  grading_injection — no new builder machinery (ratchet: the builders are sufficient).
trigger: any eval run
non_trigger: n/a
inputs: case YAMLs + skill SKILL.md + contract files
outputs: injection prompts + required-read sets
canonical_or_transient: transient
reads: cases, skills, contracts
writes: injection artifacts (results/)
upstream: case YAMLs, the DQE contract
downstream: eval runs, score_trigger/score_all
invariants: no duplicated contract logic (H3 fix); case manifest validated before
  injection (existing)
mechanical_checks: case manifest validator (existing); injection self-test
failure_modes: contract drift between SKILL.md and injection (the H3 defect); case
  format drift (D2 class — evals README stale)
evals: the builders ARE the eval machinery; their own regression = the case suite passes
dsh_basis: M8 TAG (record-once/replay-forever: injection = the "record" step; replay
  frozen DQE bundles read-only)
research_specific_delta: the reader-test role (OVERCLAIM_DETECTED) is the research
  adaptation of DSH's "prove it FAILS on the unfixed code" trust-but-verify rule (M22 TAG)
```

```yaml
name: rubric.md / hard-fail.md / canonical-source-map.md (harness references)
problem: the stable scoring references: quality rubric, HF-1..HF-15 catalog, canonical-
  home table (10 rows)
current_owner: evals/skills/{rubric,hard-fail,canonical-source-map}.md
proposed_action: keep   # phase0 H4 = KEEP (agreed)
why_this_must_be_a_skill: N/A — DOC-FORMAT references (the stable part of the eval
  contract). KEPT as-is; canonical-source-map.md is the eval fixture that File 3 row 5.1
  (docs/canonical-source-map.md) SUPERSEDES as the repo-level declaration — the harness
  table then becomes a LINK to the repo doc (no duplicate fact, I2). Disagreement note:
  "keep" for the eval fixture, "superseded as declaration" for the canonical-home
  authority — both are true, stated here so the two uses don't collide.
trigger: grading (rubric/HF); canonical-home lookups in evals
non_trigger: repo-level ownership (File 3)
inputs: n/a (references)
outputs: scoring criteria; home table
canonical_or_transient: canonical (the eval contract's stable part)
reads: —
writes: —
upstream: DQE skill
downstream: grading, the slice
invariants: HF catalog versioned (HF-1..HF-15, hard-fail.md:1); rubric changes go
  through adjudication (existing protocol)
mechanical_checks: HF-catalog consistency (the D11 defect: quality-control-plan's HF
  table drifted pre-v0.4 — fixed by pointing at hard-fail.md, not re-listing)
failure_modes: catalog drift (D11 class — closed by single-source pointing)
evals: n/a (they ARE the eval references)
dsh_basis: M13 TAG (stable references as single source; no hand-maintained restatement)
research_specific_delta: the HF-13 (hybrid doc) / HF-14a/14b (status posture) family is
  the research-specific hard-fail set (added after P2)
```

```yaml
name: the other 13 checkers (interface_check, flow_state_check, status_vocab_check,
markdown_links_check, placeholders_check, CCM/TDR/LDM self-tests, corpus validators, …)
problem: the deterministic invariant tier (per-artifact invariants + corpus integrity)
current_owner: evals/skills/*.py (17 checker files on disk — current-system-map C, D2)
proposed_action: keep   # phase0 H5 = KEEP (agreed)
why_this_must_be_a_skill: N/A — CHECKERS (charter §10's canonical home for everything
  decidable). Kept; EXTENDED: markdown_links_check gains VOID/archived-banner awareness
  (I6), status_vocab_check gains the role-mixing rule (I4), the corpus validators gain
  the computed census (File 3 row 17). The 4 Phase-2 minimum lints (File 2 §6) are
  ADDED as new files in the same tier now — the 6 deferred lints join at each build
  phase (R11) — not replacements; the planted-defect self-test pattern
  applies to each (the existing bar, classification H5).
trigger: preflight / PR / manual
non_trigger: model-level judgment (DQE/UDM)
inputs: artifacts + corpus
outputs: tier results
canonical_or_transient: transient
reads: repo
writes: none
upstream: run_checks.py
downstream: release gate
invariants: per-artifact invariants (12 fields, migration map, rewrite provenance,
  flow-state semantics); corpus non-mutation (verified shadow)
mechanical_checks: planted-defect self-tests (existing — the Batch-5 checkers caught
  their planted defects, classification H5)
failure_modes: self-test gaps (a planted defect not caught = release blocker — the
  existing bar)
evals: the adversarial battery (File 5 §c) runs against this tier
dsh_basis: M23 TAG (reliability doctrine: no masking; rejection records); M14 DN
  (interface_check already solves the doc-drift problem DSH's type-fence solves — a
  second gate would be a duplicate ledger)
research_specific_delta: flow-state semantics (honest-BLOCKED, COMPLETE-scope) and the
  E-level register checks have no DSH counterpart — the research invariant tier
```

```yaml
name: corpus + blind-runs + adjudication + snapshots (eval fixtures)
problem: the test corpus (20-case seeds, 41 case YAMLs / 229 entries, golden-negatives),
  blind-run protocol, dual-reviewer adjudication, frozen DQE bundles
current_owner: tests/corpus/**, evals/skills/{adjudication,snapshots}/, docs/testing/
  {corpus-policy,adjudication-protocol,adjudication-v4}.md
proposed_action: keep   # phase0 H6 = KEEP (agreed)
why_this_must_be_a_skill: N/A — TEST fixtures + protocol (TEST mechanism). Kept as the
  system's strongest integrity asset (isolation strong / provenance weak — pain-points
  §4.4); REFINED only by TRACKING: frozen bundles + upstream pins + snapshots move into
  git (File 3 row 1/6 — D10/D19; crosswalk M8 TAG: "track the frozen bundles + upstream
  pins; replay frozen DQE bundles read-only in gates; review every fixture diff").
  The adjudication protocol stays human (P7 is the standing cost — kept honest, not
  mechanized: gold labels are judgment, and the dual-reviewer design is the calibration).
trigger: any skill's eval; any corpus mutation (postcondition-verified)
non_trigger: n/a
inputs: seeds, case YAMLs, blind suites
outputs: metrics, adjudicated gold labels, frozen bundles
canonical_or_transient: canonical fixtures (append-only); results transient/record
reads: seeds, cases
writes: corpus (postcondition-verified mutation only — P3 discipline)
upstream: seed selection (human), corpus-policy
downstream: all skill evals, the slice, scenario A
invariants: corpus non-mutation in skill runs (existing); mutation postconditions
  (validate_mutation_semantics.py — P3); blind .secret mappings comparator-only (I9/
  Q6); gold labels adjudicated, never solo-authored
mechanical_checks: validate_case_manifests; mutation postconditions; shadow run
  (git porcelain clean)
failure_modes: fixture defect measuring the wrong thing (P3 — the postcondition
  closes it); preservation claims drifting from disk (D19 — tracking closes it)
evals: the corpus IS the eval substrate; its own integrity = the manifest validators
dsh_basis: M8 TAG (record/replay + reviewed refresh); M17 DN (goldens KEPT — the
  filename ban would fight the design)
research_specific_delta: the blind-run .secret identity separation + dual-reviewer
  adjudication is the research adaptation of DSH's keyless snapshot discipline —
  stronger on identity, weaker on automation, by design
```

---

## 3. Governance components (G1–G6) — not skills; labels carried for completeness

```yaml
name: skills-registry.yaml
problem: the skill roster (names, versions, upstream/downstream, eval state, meta narrative)
current_owner: docs/skill-development/skills-registry.yaml
proposed_action: refine   # phase0 G1 = REFINE (agreed)
why_this_must_be_a_skill: N/A — the ROSTER document (DOC + CHECKER). REFINES to roster-
  only: delete the `meta:` batch narrative (it duplicates frozen plans — D6); derive
  name/path/version/eval-count fields from disk where derivable (crosswalk M13 TAG:
  "generate roster fields from SKILL.md + disk; freshness check"); verify L3
  "installed" claims against disk (D11: deep-research listed but absent). It stays the
  dependency-graph source of truth (File 3 row 10).
trigger: preflight (load-bearing reader — existing)
non_trigger: narrative history (git + incident ledger)
inputs: disk + SKILL.md front-matter
outputs: roster + graph fields
canonical_or_transient: canonical (roster)
reads: disk
writes: itself (roster fields)
upstream: skills, disk
downstream: preflight, dependency-graph-lint, the slice
invariants: roster = single source of "what exists" (I2); "listed installed" = on disk
mechanical_checks: preflight version/dependency consistency (existing); new: roster-
  vs-disk freshness (M13), L3 disk check (D11)
failure_modes: narrative drift (D6 — deletion closes it); phantom installs (D11)
evals: preflight (existing)
dsh_basis: M13 TAG (derive, never hand-edit, what is derivable); M3 DT (the frontmatter
  is the single trigger contract the roster derives from)
research_specific_delta: the L3 research stack (wos/scansci/paper-fetch/lit-review +
  the user-local deep-research, OQ-3 provenance UNKNOWN) is the research-specific roster
  surface
```

```yaml
name: creation-roadmap.md
problem: per-batch build roadmap (status per skill)
current_owner: docs/skill-development/creation-roadmap.md (marked VOID 2026-09-09)
proposed_action: remove   # phase0 G2 = REMOVE from active governance; archive (agreed)
why_this_must_be_a_skill: N/A — a plan doc that is already VOID (commit 62ada30) but
  still tracked and still referenced by DQE SKILL.md:9 (D12) and system-architecture
  (D12). REMOVED from active governance and moved to docs/plans/archived/ — this is the
  Phase-2 slice's remove-side ratchet event (File 2 §7 refinement 4). archive-lint makes
  the move mechanically required (banner ⇒ archived within one release).
trigger: n/a (VOID)
non_trigger: everything
inputs/outputs: n/a
canonical_or_transient: historical record (archived)
reads/writes: —
upstream/downstream: the inbound pointer (DQE SKILL.md:9) must be fixed in the same
  change (I6 same-change rule)
invariants: VOID docs live in archived/ (archive-lint)
mechanical_checks: archive-lint (new)
failure_modes: the VOID-but-referenced zombie (D12 — the live instance)
evals: n/a
dsh_basis: M18 TAG (archive = relocation, never edit; supersession at creation)
research_specific_delta: n/a — a pure process artifact
```

```yaml
name: runlog.md
problem: append-only "run log" narrative of what was done
current_owner: docs/skill-development/reports/runlog.md (58 lines, all of it)
proposed_action: replace   # phase0 G3 = REPLACE (agreed — the only REPLACE)
why_this_must_be_a_skill: N/A — chronology (GIT-ONLY, File 1 Q8 / File 3 row 13).
  REPLACED by git history + the incident ledger (File 3 row 12): P9 measured the disease
  — the "append-only" runlog is batch-logged RETROACTIVELY, its phantom "wrote=[… memory]"
  lines are untracked (pain-points P9; crosswalk M30 TAG: "retroactive runlog" is the
  named defect class), and its LARGEST incident (63M tokens) is absent. Git records the
  chronology better and cannot drift; the incident ledger carries the incidents git
  doesn't (the 63M event has no commit to hang on). Transition: a one-line pointer during
  the slice, then deleted.
trigger: n/a
non_trigger: everything
inputs/outputs: n/a
canonical_or_transient: replaced (git + incident ledger are canonical)
reads/writes: —
upstream/downstream: —
invariants: no document restates "what happened when" as current state (I2/I13-row-1)
mechanical_checks: state-consistency-lint (new — doc claims vs observed state)
failure_modes: retroactive batch-logging (P9); phantom writes (P9)
evals: n/a
dsh_basis: M30 TAG (repo prose = current-state facts, not session transcript); M11 DT
  (incidents get a home: the ledger)
research_specific_delta: the "wrote=[… memory]" phantom-write class is specific to
  agent-run logging — the research delta is the incident-ledger format (P1–P10 as seed)
```

```yaml
name: system-architecture.md
problem: the architecture doc (layers, call chains, gate rules, open questions)
current_owner: docs/skill-development/system-architecture.md
proposed_action: refine   # phase0 G4 = REFINE (agreed)
why_this_must_be_a_skill: N/A — the architecture DOC (DOC-FORMAT + CHECKER). REFINES:
  status line "DECIDED for Phase 1" (2026-08-05) gets a pointer to the active charter
  + optional informational `last_verified:` (R2: not a freshness gate; D12/G4); the OQ-1..OQ-5 table DELETED (moved to the decision
  register — the D9 collision, File 3 row 2); "advisory checkpoint" rule restatements
  collapse to the decision note + links (current §1.2: ≥5 copies). Kept as the ordered
  map (DSH tier: architecture.md is an ordered map, not a resume doc — File 1 Q9).
trigger: architecture questions
non_trigger: resume (Q9 set); status (status table)
inputs: decisions
outputs: the map
canonical_or_transient: canonical (architecture)
reads: decision notes
writes: itself (same-change as architecture decisions)
upstream: decision notes
downstream: flows (call-chain reference)
invariants: current-state prose (I6); no rule restatement (I2); open questions live in
  the register only
mechanical_checks: canonical-impact-lint (new, R2); dead-pointer check (new)
failure_modes: status drift (G4 — the live instance); ID collisions (D9)
evals: n/a
dsh_basis: M12 DT (tier taxonomy: architecture.md = ordered map); M1 TAG (budgeted
  standing orders)
research_specific_delta: the architecture is a SKILL-WORKFLOW architecture (L0/L1/L2/
  L3 layers) — the tier table is built around it (File 3 row 2)
```

```yaml
name: conflict-matrix / quality-control-plan / current-skills-audit / ADR-DQE-001
problem: routing rules (OK/SEQ/DENY/COND); eval pass targets + regression policy; the
  audit record; the one durable ADR
current_owner: docs/skill-development/{conflict-matrix,quality-control-plan,current-
  skills-audit,adr/ADR-DQE-001-…}.md
proposed_action: keep   # phase0 G5 = KEEP (agreed)
why_this_must_be_a_skill: N/A — CONVENTION + DOC-FORMAT + decision note. conflict-
  matrix: kept as the co-run semantics source (File 3 row 10 splits it from the
  dependency graph: CO-RUN is a different relation — no duplication); quality-control-
  plan: kept (its §10 pass targets govern File 5; the drifted HF table D11 fixed by
  pointing at hard-fail.md, not re-listing); current-skills-audit: kept as an append-
  only record (it is the audit, not a current claim); ADR-DQE-001: KEPT but MIGRATED
  into docs/decision-notes/decided/ (File 3 row 8, R3: decision lifecycle folder; its
  implementation_state = implemented — the freeze is operational) + ANNOTATED (the OQ-REPRO=A
  falsification, D12 — supersession-lint enforces the annotation).
trigger: routing decisions (conflict-matrix); eval runs (QC plan); audits
non_trigger: n/a
inputs/outputs: conventions
canonical_or_transient: canonical (conflict-matrix, QC plan); record (audit); canonical
  decision (ADR)
reads/writes: —
upstream/downstream: flows, preflight (release blocker rule)
invariants: DENY without resolution = release blocker (conflict-matrix:15); pass
  targets (QC plan §10); ADR annotation on falsified claims (D12)
mechanical_checks: conflict-matrix vs dependency-graph consistency (dependency-graph-
  lint); supersession-lint (ADR annotation)
failure_modes: co-run semantics drifting from the graph (the lint); un-annotated
  falsification (D12 — the live instance)
evals: n/a
dsh_basis: M16 DN (the closed-vocabulary idea transfers as §12.6 fields, not a board);
  M11 DT (the ADR annotation is the same-change guardrail pattern)
research_specific_delta: the QC plan's "regression policy + pass targets" is the
  research governance surface DSH has no equivalent for (DSH gates are code gates)
```

```yaml
name: release-manifest + preflight / install / smoke
problem: release state (source_commit, completion semantics, skill_count) + the
  23-check preflight + install + the clean-room smoke test
current_owner: release-manifest.yaml, scripts/preflight.py, INSTALL/UNINSTALL, docs/
  release/clean-room-smoke-test.md
proposed_action: keep   # phase0 G6 = KEEP (agreed)
why_this_must_be_a_skill: N/A — CHECKER + CI-GATE + GIT-PR-CONVENTION (the release
  machinery). Kept; EXTENDED: preflight gains (1) release-version-lint over the 11 doc
  headers (D1), (2) the installed-skills disk check writing results/preflight/<date>.yaml
  (A5 — D6), (3) the L3 roster disk check (D11), (4) roster-vs-disk freshness (M13).
  The smoke test's planted-contradiction + 0-footprint safety-negative is generalized
  into state-consistency-lint (File 1 I7) but the smoke test itself stays the release
  gate.
trigger: preflight (per change); smoke (per release)
non_trigger: n/a
inputs: repo, VERSION, manifest, disk
outputs: check results; smoke report
canonical_or_transient: manifest canonical; results records
reads: repo + disk
writes: results/preflight/ (new record)
upstream: every change
downstream: release gate
invariants: completion semantics pinned (manifest:71-73); 0-footprint (existing);
  "listed installed" = on disk (new)
mechanical_checks: preflight 23 checks (existing) + the 4 extensions; smoke (existing)
failure_modes: version drift (D1 — the lint); phantom isolation (D6 — the record)
evals: smoke report per release (existing practice, docs/release/)
dsh_basis: M10 DN (the full CI matrix does NOT transfer — no CI exists here; ratchet:
  add after a concrete failure); M24 TAG (honest external-dependency checks in preflight)
research_specific_delta: the clean-room smoke against the RELEASED package (not the dev
  tree) is the research-repo adaptation of DSH's fresh-clone discipline (A.2)
```

---

## 4. ADDs — capabilities that do not exist yet (A1–A10)

A1–A6 are the phase0 ADD list (labels ADD — agreed). A7–A10 are ADDs justified by this
synthesis, each tied to a §12 candidate (File 2 §6).

```yaml
name: A1 — apply-mode executor (migration apply)
problem: apply an APPROVED migration map under the CCM invariants, verify the post-state
current_owner: none (the missing half of CCM — classification A1)
proposed_action: add
why_this_must_be_a_skill: apply-time judgment (conflict handling when the map meets
  reality, verifying the post-state against invariants) is repeated non-trivial judgment;
  without it the closed loop stays dry-run forever (Q14: the slice's own owner updates
  are hand-applied because A1 is absent — the measured cost). It is a NEW MODE of CCM
  (not a mode of TDR, which rewrites TEXT; A1 moves/deletes STRUCTURE) — same skill, same
  invariant suite (File 2 §1 census counts A1 as a mode, not a new skill).
trigger: an approved migration map exists (CCM output + human write-approval)
non_trigger: planning the map (CCM); text rewrites (TDR); unapproved maps (never)
inputs: approved map + corpus
outputs: applied state + apply-provenance (per-file sha256 before/after, invariant
  verification result)
canonical_or_transient: the applied state is canonical (in the target owners);
  provenance is a record
reads: map, corpus
writes: the corpus (under the write-approval boundary — HUMAN-APPROVAL)
upstream: CCM (map), UDM (decision), human approval
downstream: LDM (post-change impact), DQE (advisory re-check), flow-state COMPLETE
invariants: the CCM invariant suite re-verified AT APPLY (may_overwrite=false, no
  target==source, no duplicate primary, provenance survives moves)
mechanical_checks: CCM checkers run before AND after apply (existing, reused);
  duplicate-fact-lint before/after (new)
failure_modes: apply drift from plan (re-verification closes it); partial apply
  (atomic-per-file + post-state check)
evals: planted map-conflict case (new); the slice's owner updates as the first real apply
  (hand-applied until A1 lands — Phase 3)
dsh_basis: M18 TAG (relocation-never-edit semantics at apply time); M22 TAG (verify the
  artifact, not the report)
research_specific_delta: research artifacts (evidence maps, decision notes) carry
  provenance that must survive moves — the apply invariant is wider than file moves
```

```yaml
name: A2 — Batch-4 research core (6 atoms)
problem: the six research atoms NRSD's tail is blocked at (the evidence-front to
  implementation bridge)
current_owner: none (named in NRSD SKILL.md:40-60; classification A2)
proposed_action: add
why_this_must_be_a_skill: each atom is a repeated non-trivial research judgment (the
  phase0 audit named them as the flow's honest blocked tail); they are the single largest
  unexercised surface of charter mission #4. Batched (not one-by-one) because the flow's
  call chain integrates them together — the ratchet allows a batch when the consumer
  (NRSD tail) demands the whole set at once (the DR Sprint-6B precedent: Batch-5 atoms
  landed as the flow's tail, registry:331).
trigger: the NRSD tail (each atom's own trigger per its future SKILL.md)
non_trigger: n/a (batch)
inputs/outputs: per-atom (frozen interfaces per the batch2.5-v1 pattern)
canonical_or_transient: per-atom (transient outputs, canonical merges where applicable)
reads/writes: per-atom
upstream: NRSD front (RES/UDM)
downstream: NRSD tail, the 12.5 discriminating-experiment
invariants: honest BLOCKED until built (the D14 discipline); frozen interface per atom
mechanical_checks: interface_check per atom (existing pattern); dependency-graph-lint
  (blocked_by names)
failure_modes: skeleton-first (the D3/D14 disease — SKILL.md claims builtness only when
  true; builtness matched to the graph, R7)
evals: 6 trigger / 2 conflict per atom (the Batch-5 pattern, the minimum bar)
dsh_basis: M2 RSA (research decision notes at each fork); M9 TAG (smallest evidence at
  each atom)
research_specific_delta: the entire batch is research-specific (DSH has no research core)
parked: PARKED CAPABILITY GAP (R12, repair round)
  gap: the evidence-front-to-implementation bridge (6 research atoms)
  evidence_of_need: NRSD tail HONEST-BLOCKED at exactly these atoms (SKILL.md:40-60);
    the 10-upstream call chain is the system's largest honest-BLOCKED surface
  current_blocked_consumer: NRSD (Batch-4 tail, live at 3bb307f)
  activation_condition: a real consumer request arrives (a design question the evidence
    front cannot answer without an atom) AND D-1 is ruled (route state has a home)
  not_planned_until: the first real consumer request (Phase 3+; no speculative build)
```

```yaml
name: A3 — Batch-5 tail atoms (4)
problem: the four remaining doc-execution atoms the flows list as not built (SWR
  SKILL.md:49 class; classification A3)
current_owner: none
proposed_action: add
why_this_must_be_a_skill: same reasoning as A2 — the atoms are the honest blocked tails
  of SWR/DR; each is a repeated non-trivial doc-execution judgment. NOTE: LDM was the
  5th Batch-5 atom and is BUILT (D14 shows the stale claim) — A3 is the remaining 4.
trigger: per-atom (future SKILL.md)
non_trigger: n/a
inputs/outputs: per-atom (frozen interfaces)
canonical_or_transient: per-atom
reads/writes: per-atom
upstream: the L1 flows' tails
downstream: flow-state completion
invariants: honest BLOCKED until built; frozen interface per atom
mechanical_checks: interface_check; dependency-graph-lint
failure_modes: the D14 stale-builtness claim (builtness-claim vs roster + lint, R7)
evals: 6 trigger / 2 conflict per atom (minimum bar)
dsh_basis: M28 TAG (canonical SKILL.md section sequence for the new atoms)
research_specific_delta: research-workspace-specific execution (data/experiment docs)
parked: PARKED CAPABILITY GAP (R12, repair round)
  gap: the 4 remaining doc-execution atoms (SWR/DR tails)
  evidence_of_need: SWR SKILL.md:49 names them not-built (D14's stale-claim class —
    builtness now graph-matched, R7)
  current_blocked_consumer: SWR + DR execution tails
  activation_condition: a real document-execution request reaches the tail AND the
    interface contracts are versioned (File 3 row 11)
  not_planned_until: the first real consumer request (Phase 3+)
```

```yaml
name: A4 — L0 router
problem: a single invocable entry point that routes any request to the right flow/skill
current_owner: none (conflict-matrix covers routing at DOC level; classification A4)
proposed_action: add   # phase0 A4 = ADD (agreed as a capability; mechanism decision
  below DISAGREES with the naive "single invocable entry point" reading — see why)
why_this_must_be_a_skill: DISAGREEMENT, with evidence: phase0 names A4 "a documented
  routing table … as a single invocable entry point." This matrix keeps the capability
  (ADD) but lands it as CONVENTION + CHECKER first, not a skill: routing is rule-based
  (the conflict-matrix table is already the decision procedure), so the §10 test
  (repeated non-trivial judgment) fails for a router skill at 3-flow scale. Mechanism:
  the routing table lives in root AGENTS.md (Q9 resume set) + `dependency-graph-lint`
  verifies table-vs-registry consistency. PROMOTION TRIGGER (explicit, ratchet): a
  standalone router skill is added only when flow count > 3 OR the table needs judgment
  beyond the OK/SEQ/DENY/COND vocabulary (evidence: the table has so far never needed
  it — 18 commits, no unresolved routing case in the incident record).
trigger: any new request (the table, not a skill)
non_trigger: in-flow routing (the flow owns it)
inputs: the request + roster
outputs: the route (table lookup)
canonical_or_transient: canonical (the table, in AGENTS.md)
reads: AGENTS.md table, roster
writes: none
upstream: (entry)
downstream: flows / skills
invariants: table = single source of routes (I2); consistency with the graph (lint)
mechanical_checks: dependency-graph-lint (table-vs-registry)
failure_modes: table drift (the lint); judgment-less misroute (review — no measured
  instance yet, which is WHY it is not a skill)
evals: routing table cases (a subset of the existing conflict cases, re-pointed)
dsh_basis: M3 DT (frontmatter non-triggers ARE the routing mechanism — the table is
  their repo-level complement); M1 TAG (AGENTS.md as standing-order home)
research_specific_delta: research requests split along EVIDENCE axes (literature vs
  project vs inference) that the table must encode — the research routing delta
parked: PARKED CAPABILITY GAP (R12, repair round) — the CONVENTION + CHECKER half
  (routing table in AGENTS.md + dependency-graph-lint) ships with the Phase-3
  convention batch; the SKILL promotion stays parked
  gap: single invocable router entry point
  evidence_of_need: none measured yet (18 commits, no unresolved routing case — the
    PROMOTION TRIGGER above is the evidence bar)
  current_blocked_consumer: none (the table covers routing at 3-flow scale)
  activation_condition: flow count > 3 OR routing needs judgment beyond
    OK/SEQ/DENY/COND
  not_planned_until: that trigger fires
```

```yaml
name: A5 — install/registration state record
problem: a machine-checkable record of what is actually installed where (mode A/B)
current_owner: none (the claim "workspace-only isolation" is untracked prose — D6)
proposed_action: add
why_this_must_be_a_skill: DISAGREEMENT (mechanism): NOT a skill and not a standalone
  document — a CHECKER (preflight extension) writing a result record
  (results/preflight/<date>.yaml). Rationale: the state is fully derivable from disk
  (ls the loader dir, diff against the roster) — §10: decidable ⇒ checker (crosswalk
  M13 TAG: derive, never hand-edit, what is derivable). The D6 failure (all 14 installed
  as user-level copies, untracked in runlog/manifest/KNOWN_LIMITATIONS) is a
  derivability gap, not a judgment gap.
trigger: every preflight run
non_trigger: n/a
inputs: loader dir, roster
outputs: results/preflight/<date>.yaml (installed set + mode + drift)
canonical_or_transient: record (append-only); the claim in KNOWN_LIMITATIONS becomes a
  pointer to the latest record
reads: disk
writes: results/preflight/
upstream: preflight
downstream: release checklist
invariants: "listed installed" = on disk (D11/D6 closed mechanically)
mechanical_checks: the check IS the mechanism
failure_modes: untracked installs (the D6 class — closed)
evals: preflight (existing harness)
dsh_basis: M13 TAG (derived roster); M24 TAG (honest external state in preflight)
research_specific_delta: the L3 research stack (user-local, OQ-3 provenance UNKNOWN) is
  the install surface the record must cover
```

```yaml
name: A6 — DQE terminal-gate promotion gate
problem: the readiness evidence + decision procedure for promoting DQE from advisory to
  a terminal gate (per profile)
current_owner: none as a mechanism (the readiness evidence exists: 3 frozen bundles —
  registry:26; the decision is DEFERRED — classification A6)
proposed_action: add
why_this_must_be_a_skill: DISAGREEMENT (mechanism): NOT a skill — a HUMAN-APPROVAL
  boundary + CHECKER (the 3-arm matrix runner, when it runs). The judgment (is the gate
  trustworthy enough for THIS profile) is a one-shot human decision per profile, made
  against machine evidence — not repeated non-trivial judgment. Mechanism: the Phase-E
  3-arm matrix (deferred by the canary, P4) produces the evidence; the promotion is a
  decision note (File 3 row 8) with the canary's revisit conditions as the
  revisit_condition field (File 2 §3.10). Stays DEFERRED for Phase 2 (File 1 Q13: the
  canary already deferred it — the ratchet says keep the deferral).
trigger: a profile's 3-arm matrix passes + human ruling
non_trigger: all evals until then (advisory, Rule 0)
inputs: matrix results, canary record
outputs: promotion decision note + manifest flag
canonical_or_transient: canonical (the decision note)
reads: results, canary
writes: decision note, manifest
upstream: the 3-arm matrix (Phase-E), human
downstream: the release gate (per profile)
invariants: Rule 0 (unadmitted profile = honest INCOMPLETE, never a forced verdict);
  evidence-before-promotion (the P2/P4 lesson)
mechanical_checks: the 3-arm matrix runner (deterministic); rule-0 admission check
  (existing)
failure_modes: premature promotion (the P2 disease — the gate's own history); LLM-
  signal instability (P2/P4 — why the evidence must be multi-arm, not single-run)
evals: the 3-arm matrix (File 5 §b scenario C uses its canary as input)
dsh_basis: M24 TAG (honest admission: missing capability = loud non-verdict); A.6
  perf-gate lesson (no quality gate without a calibrated deterministic harness + named
  budget)
research_specific_delta: the profile dimension (which document classes are admissible)
  is the research delta — DSH's gates are binary, DQE's are profile-scoped
parked: PARKED CAPABILITY GAP (R12, repair round) — stays DEFERRED by the canary (P4):
  the 3-arm matrix has not run, so promotion evidence does not exist yet
  gap: the evidence + procedure for DQE terminal-gate promotion
  evidence_of_need: P2's false pass (a single-run gate is untrustworthy); the Phase-E
    canary deferred the matrix itself
  current_blocked_consumer: none today — DQE advisory scope is sufficient (Rule 0);
    the release gate stays binary
  activation_condition: the 3-arm matrix runs and passes for a profile AND a human
    ruling promotes it (decision note, File 3 row 8)
  not_planned_until: the canary's revisit conditions are met (Phase-E evidence exists)
```

```yaml
name: A7 — repo-bootstrap (greenfield bootstrap skill)
problem: create a new research repo from zero with the MINIMUM sufficient structure
current_owner: none (this repo was never bootstrapped — P10; charter §12.1)
proposed_action: add   # new ADD (charter §12.1 candidate — evaluated in §5.1)
why_this_must_be_a_skill: "what is the minimum sufficient structure for THIS repo's
  nature" is a repeated per-target non-trivial judgment (every new research repo re-
  asks it); the ratchet rule (guardrail only after a concrete failure) is a judgment
  applied at bootstrap time. The mechanical half (the skeleton template: AGENTS.md, one
  HARD checker, decision-notes dir, incident ledger, README current-state rule) is a
  CONVENTION artifact the skill instantiates — §10: judgment in the skill, mechanics in
  the template. DSH evidence: the day-one gate suite (A.1) shows the minimal gate set
  must exist on day one; its 8,130-word AGENTS.md shows what NOT to do (M1: budgets).
trigger: a new repository is being created (this repo or a downstream research repo)
non_trigger: reconstructing an existing repo (PSR/SWR); simplifying (A8)
inputs: the repo's purpose (GSWE-elicited scope)
outputs: the minimal skeleton + first decision note + first (deliberately small) guardrail
canonical_or_transient: canonical (the skeleton IS the new repo's canonical set)
reads: the purpose
writes: the new repo
upstream: GSWE (scope)
downstream: everything in the new repo
invariants: no speculative governance tree (§12.1); every guardrail names its failure
  mode (charter §18); current-state docs carry owner front-matter (optional informational
  last_verified, R2) from day one (I6)
mechanical_checks: preflight from day one (the one HARD checker); AGENTS.md budget
  (M1 — a small ceiling on standing orders)
failure_modes: premature framework inflation (the anti-pattern §12.1 names); missing
  decision-note home (the D8 disease from day one)
evals: scenario B (File 5 §b) — greenfield bootstrap eval on an empty dir
dsh_basis: M1 TAG (standing orders + budgets); M12 DT (one-home-per-fact from day one);
  M4 DT (pre-release stance as deletion license)
research_specific_delta: the skeleton includes the RESEARCH surfaces (evidence dir,
  decision register with route/experiment object_types (R4)) that a software-repo bootstrap omits
```

```yaml
name: A8 — simplification-audit
problem: find high-value simplification candidates (consumer-classified, evidence-
  backed, few strong over many thin)
current_owner: none (charter §12.2; DSH dsh-find-simplifications is the seed, M31)
proposed_action: add   # new ADD (charter §12.2 candidate — evaluated in §5.2)
why_this_must_be_a_skill: consumer classification ("does anything consume it? is the
  consumer obsolete too?") is repeated non-trivial judgment — the cleanest §10 case in
  the new adds; the candidate GENERATION (git ls-files inventory, consumer graph) is a
  CHECKER feeding it (File 2 §1.4). DSH evidence: M31 = RESEARCH-SPECIFIC ADAPTATION
  REQUIRED (crosswalk) — the charter explicitly commissions the adaptation; the knip
  lesson (B.2.1: the exception inventory IS the debt) is the import guardrail — the
  skill must output candidates, not a detection regime with carve-outs.
trigger: a periodic simplification pass (Phase 4); after a release; when the corpus
  grows past a threshold (the longitudinal metric flags it)
non_trigger: one-off cleanup of a known orphan (direct edit); state recovery (PSR)
inputs: inventory (checker-generated) + consumer graph + the §12.2 research target list
outputs: a FEW evidence-backed candidates (each: what, consumer analysis, evidence,
  proposed action) — a proposal, never an applied diff
canonical_or_transient: transient (the candidate list); applied simplifications are
  normal changes (own their decision notes)
reads: repo (read-only)
writes: candidate report
upstream: the inventory checker, dependency-graph-lint output
downstream: human/agent decision, then normal changes
invariants: evidence-backed only (no shallow lists); protected seams declared
  (crosswalk M31: the research target list is ours, not DSH's); no exception inventories
  (the knip lesson)
mechanical_checks: inventory + consumer graph (checker — the mechanical half);
  each candidate must carry a consumer analysis (decision-note-lint style)
failure_modes: large shallow list (the named anti-pattern, §12.2); exception-inventory
  growth (knip — the B.2.1 warning); auditing the audit (one pass per trigger, not
  standing)
evals: scenario A (File 5 §b) includes a simplification stage; planted orphan + planted
  duplicate-abstraction cases (adversarial defects 4/12)
dsh_basis: M31 RSA (the commissioned adaptation); B.2.1 knip negative evidence; M7 DN
  ("uncovered = suspect" as audit heuristic, not a coverage bar)
research_specific_delta: the target list is research-specific (§12.2: orphan scripts,
  stale notebooks, duplicated pipelines, non-reproducible results, prototypes-as-
  dependencies, tests/docs as sole consumers)
```

```yaml
name: A9 — focused-verification (change-scope → smallest sufficient evidence)
problem: for a change, compute the scope and select the NARROWEST evidence sufficient
  to catch the regression
current_owner: none (run_checks.py runs everything — no diff-aware selection; §12.3)
proposed_action: add   # new ADD (charter §12.3 candidate — evaluated in §5.3)
why_this_must_be_a_skill: HYBRID by design (charter §12.3's three parts split across
  layers): the change-scope report is a CHECKER (deterministic: touched files → touched
  skills → relevant checker/case subset, from dependency-graph-lint); the SELECTION is
  the skill (judgment: "narrowest SUFFICIENT" is not decidable — sufficiency is the
  judgment). This is exactly DSH dsh-pre-push-checks' split (M9 = TRANSFERABLE AFTER
  GENERALIZATION, crosswalk: "smallest relevant evidence → smallest discriminating
  experiment"; "separate selection from standard"). The import guardrail: do NOT
  recreate the removed check:pre-push aggregate (A.1).
trigger: a change needs verification (the default path for any non-trivial change)
non_trigger: a release (full gate — preflight+smoke); a research experiment (12.5)
inputs: the change (diff) + dependency graph
outputs: scope report (checker) + selected evidence set + verification result
canonical_or_transient: transient (the selection is a record under results/)
reads: diff, graph, checkers' capabilities
writes: results/
upstream: any change
downstream: the selected checkers/cases, release gate (full)
invariants: never re-run a passing check (M9); scope = machine-computed, selection =
  judgment (the split); "narrowest sufficient" documented per selection (auditability)
mechanical_checks: the change-scope checker (new); the selected subset (existing
  checkers/cases)
failure_modes: under-selection (a regression escapes — the sufficiency judgment;
  mitigated by the release full-gate as backstop); over-selection (the P1/P3 disease —
  running everything before asking what is sufficient)
evals: planted regression in an unselected module (must NOT pass silently — the
  selection records WHY); scenario D integration stage
dsh_basis: M9 TAG (the commissioned generalization); A.1 (the aggregate removal — do
  not re-aggregate); M5 TAG (narrow local tier)
research_specific_delta: the research extension is "smallest discriminating EXPERIMENT"
  for research uncertainty (§8.8 second clause) — the selection vocabulary extends from
  tests to experiments (the 12.5 skill is the research half of the same capability)
```

```yaml
name: A10 — next-discriminating-experiment
problem: choose the smallest experiment most likely to change which route we pursue
current_owner: none (the system sequences "next tasks", never decision-value — §12.5)
proposed_action: add   # new ADD (charter §12.5 candidate — evaluated in §5.5)
why_this_must_be_a_skill: DECISION-VALUE-FIRST, cost-second optimization (R10.2:
  decision relevance + expected discrimination established BEFORE cost minimization)
  over competing routes is PURE repeated non-trivial judgment — nothing about it is checker-decidable
  (File 2 §3.6: "you cannot lint 'discriminating'"). The cost-bounding half (pre-
  counted, capped plans feeding validate_eval_plan.py's existing caps — the P1 fix)
  is CONVENTION + the existing validator. DSH evidence: M9 TAG (the same "smallest
  evidence" principle generalized to research) + A.6 (the canary is the one time this
  question was answered well — by hand, at 0.7M tokens; the skill exists to make that
  judgment repeatable, not to replace it).
trigger: ≥2 active routes with an unresolved ranking (register object_type: route, R4)
non_trigger: a single-route continuation (just the next task); an admitted-profile
  document question (DQE)
inputs: register state (route entries — the route table is their generated view, P7)
  + evidence maps
outputs: the experiment spec (decision_relevance, expected_discrimination, hypothesis
  tested, cost bound, what ranking change would mean what, stop criterion) as a register
  entry object_type: experiment (R4)
canonical_or_transient: the spec is a register entry (canonical); the result is a
  record (File 3 row 6) + evidence-map merge
reads: register, evidence maps
writes: register (experiment entry)
upstream: UDM (route state), RES (evidence gaps)
downstream: the experiment (external execution), result ingestion (File 2 §3.7), UDM
  (E-level/ranking update)
invariants: decision value first, cost second (R10.2 — a cheap NON-discriminating
  alternative must lose); cost bound mandatory (pre-countable — the P1 discipline);
  stop criterion mandatory; the output changes a RANKING, not a to-do list (§8.8)
mechanical_checks: register schema (experiment object_type: cost + stop fields required
  — register_check); validate_eval_plan.py (existing) on the execution
failure_modes: task-sequencing masquerade ("continue the next task" — the named anti-
  pattern, §12.5); unbounded experiments (P1 class — the cap); running the big
  experiment first (the P3 class — measure the smallest thing that discriminates)
evals: the canary as the golden case (File 5 §b scenario C — the 3-arm matrix is the
  discriminating experiment the skill must re-derive cheaper); planted near-duplicate
  routes case (must pick the cheaper discriminator)
dsh_basis: M9 TAG (smallest-evidence principle); A.6 (calibrated harness + named
  budget before a quality claim — the experiment's budget is its "named budget")
research_specific_delta: the entire skill is the research delta (DSH discriminates
  between IMPLEMENTATION options; this discriminates between RESEARCH routes)
```

---

## 5. Charter §12 candidate changes — each EVALUATED (not assumed)

Charter §12: "Do not assume these are final decisions, but explicitly evaluate them."
For each: verdict (ADOPT / ADOPT-LIGHT / DEFER / REJECT) + the proposed_action it
resolves to in this portfolio.

### 5.1 §12.1 Greenfield repository bootstrap — **ADOPT** → `add` (A7)
Rationale: charter mission #1 has no mechanism (this repo proves the cost: pre-git
unrecoverable era, P10); the ratchet model (bootstrap minimal, guardrail-after-failure)
is the import from DSH day-one (A.1) minus the day-one bloat (M1: budgets). A7 carries
it. Not deferred: a research org that cannot bootstrap a minimal repo re-pays P10 for
every project.

### 5.2 §12.2 Repository simplification audit — **ADOPT** → `add` (A8)
Rationale: the ratchet's remove side (I11) has no owner today; the VOID-but-referenced
roadmap (D12) is the live un-audited case; DSH's M31 (RSA — the commissioned
adaptation) supplies the method; the knip negative evidence (B.2.1) supplies the
import guardrail. A8 carries it.

### 5.3 §12.3 Focused change evidence selector — **ADOPT** (hybrid) → `add` (A9)
Rationale: P1/P3 are the paid-for proof (63M + 2.6M); DSH M9 (TAG — charter §7's own
calibration example) supplies the pattern; the hybrid split (checker scope report +
skill selection) respects §10. The import guardrail: no re-aggregation (A.1). A9 carries
it.

### 5.4 §12.4 Research route manager — **ADOPT-LIGHT** → `add` (capability, NOT yet a skill)
Rationale: the route OBJECT is needed (Q15: routes cannot be paused/rejected/revived
without falsifying history today), but the STANDALONE MANAGER SKILL fails the §10 test
at current scale — route bookkeeping is checker-able, and route-strategy judgment has
not been exercised at multi-route scale (this repo has run one route at a time).
Decision: route records = register entries `object_type: route` (R4 schema) = the
canonical mutable route state; the route table file (File 2 §3.3) is a GENERATED view
of those entries — non-authoritative, its checker verifies generation integrity (final
patch P7); promotion trigger: Phase 3 evidence of repeated
non-trivial route judgment (the charter's own caution: no big hierarchy "unless evidence
proves it is necessary"). This is the portfolio's largest deliberate NOT-a-skill call.

### 5.5 §12.5 Next discriminating experiment — **ADOPT** → `add` (A10)
Rationale: charter mission #4's last clause has no mechanism; the canary (P4) is the
proof-of-value (the question answered well, by hand, once); A.6 supplies the
calibration discipline (named budget); A10 carries it.

### 5.6 §12.6 Decision model refactor — **ADOPT** → `refine` (UDM + register schema; NOT a new skill)
Rationale: the conflation is verified (Q11.1; §3.3 prob-5); the charter's own
instruction was to TEST the schema against real examples BEFORE freezing (File 1 I4) —
DONE in the repair round (R4): the 13-entry state-space test (File 1 §I4.1, all real
entries) passed, with one material deviation: the charter's `kind` split into
`object_type` + `epistemic_state`, plus `not_applicable` on decision/implementation
states (per-entry justification in I4.1). The Phase-2 slice then exercises the revised
schema on new real entries (the D-1 note + register updates).
Mechanism: SCHEMA + `VOCAB.yaml` + role-mixing rule in status_vocab_check + register_check
(H2 merge) — no new skill (UDM keeps the judgment).

### 5.7 §12.7 Research Decision Notes — **ADOPT** → `add` (DOC-FORMAT + CHECKER; NOT a skill)
Rationale: the decision backlog has "no cheap durable home" (pain-points §4.3); the
ADR's un-annotated falsification (D12) is the live cost; DSH M2 (RSA) supplies the
format (Problem/Decision/Evidence/Alternatives/Why/Consequences/Revisit), the
lifecycle folders, and the supersession-on-creation rule (M19 DT — including the
evidence-supersession extension DSH's rule lacks); the "when is a decision note-worthy"
question stays a prose rule enforced in review (DSH tried a gate, rejected it —
b1b57a0ac5:37, crosswalk M19). Format + `decision-note-lint`, not a skill.

### 5.8 §12.8 Living design maintenance — **ADOPT** → `refine` (LDM = S11)
Rationale: the S11 defect (proposal-parallel artifacts duplicating the same-change path)
is exactly the disease §12.8 names; the refinement (impact set → same-change owner
updates, optional standalone report) is in the LDM entry above; the mechanical half
(freshness-lint → canonical-impact-lint (R2) + dead-pointer lints) is new; the DSH basis is M30 TAG + M12 DT + M18 TAG.

### 5.9 Evaluation summary (verdict → portfolio delta)

| §12 candidate | Verdict | Portfolio delta |
|---|---|---|
| 12.1 bootstrap | ADOPT | +A7 skill + template convention |
| 12.2 simplification audit | ADOPT | +A8 skill + inventory checker |
| 12.3 focused evidence selector | ADOPT (hybrid) | +A9 skill + change-scope checker |
| 12.4 route manager | ADOPT-LIGHT | +route schema/table + checker; skill PENDING Phase-3 evidence |
| 12.5 discriminating experiment | ADOPT | +A10 skill |
| 12.6 decision model refactor | ADOPT | UDM refine + §12.6 schema + VOCAB + role-mixing checker (no new skill) |
| 12.7 decision notes | ADOPT | +doc format + decision-note-lint (no new skill) |
| 12.8 living design maintenance | ADOPT | LDM refine + 2 lints (no new skill) |

Net: 4 new skills (A7–A10), 2 new non-skill capabilities (12.4-light, 12.7), 2 refines
(12.6→UDM, 12.8→LDM). The two biggest "not a skill" calls (12.4, 12.7) are the portfolio's
main anti-inflation moves — both fail the §10 test on CURRENT evidence and carry explicit
promotion triggers instead of premature skills.

---

## 6. Portfolio distribution

**Phase0-labeled items — proposed_action vs phase0 label: 32/32 AGREE** (26 items in
existing-skill-classification.md §1 + the 6 ADDs of its §3.4).
KEEP×15 (S2 S3 S4 S6 S7 S8 S9 S10 S14, H1 H4 H5 H6, G5 G6), REFINE×7 (S1 S5 S11 S12,
H3, G1 G4), SPLIT×1 (S13), MERGE×1 (H2), REPLACE×1 (G3), REMOVE×1 (G2), ADD×6 (A1–A6).
COUNT DISCREPANCY NOTE: the brief/execution-notes say "KEEP×13"; the phase0 table
itself (verified row-by-row) labels 15 items KEEP — the "13" counts the 9 skills +
4 harness items and omits G5 (conflict-matrix/QC-plan/audit/ADR) and G6 (release
machinery), both KEEP in the table. My entries agree with the TABLE row-by-row; the
brief's "13" is the undercount.
Disagreements: none on labels; four on MECHANISM within agreed labels (A4 add-as-
capability-landing-as-convention-not-skill; A5 add-as-checker-not-skill; A6 add-as-
human-boundary-not-skill; H1 keep-with-inventory-refine) — each stated in the entry with
evidence, per the brief's "where you disagree, say why" rule.

**Full proposed portfolio (44 entries): 14 skills + 6 harness + 6 governance + 10 ADDs
(A1–A10) = 36 labeled entries, + 8 §12 candidate evaluations (§5 — each resolves to an
existing portfolio item or a named non-skill capability; they add no new labels).**

Final proposed_action distribution across the 36 labeled entries (sums to 36):
- **keep**: 15 (S2 S3 S4 S6 S7 S8 S9 S10 S14, H1 H4 H5 H6, G5 G6)
- **refine**: 7 (S1, S5, S11, S12, H3, G1, G4) — plus the §12 resolutions 12.6→UDM and
  12.8→LDM, which ARE S4/S11 (no new labels)
- **split**: 1 (S13)
- **merge**: 1 (H2)
- **replace**: 1 (G3)
- **remove**: 1 (G2)
- **add**: 10 (A1–A10) — A1 = a new MODE of CCM (no new skill); A2/A3 = atom batches
  (10 skills when built, Phase 3+); A4/A5/A6 = non-skill capabilities (convention +
  checker / checker / human-boundary + checker); A7/A8/A9/A10 = 4 NEW skills

Skill portfolio after the change: **14 current → 13 active (S13 splits: shared prefix
folded into the DR flow's stages, tail parked — no new skill) + 4 new (A7–A10) = 17
invocable skills at steady state**, plus CCM's new apply mode (A1). The net DELTA is
+4 skills against a system that simultaneously DELETES 1 document (runlog), REMOVES 1
governance doc (roadmap), MERGES 1 checker, and converts 5 candidate mechanisms to
non-skill layers (A4, A5, A6, 12.4-light, 12.7) — the charter §0 "small number of
deep, composable capabilities" reading of the numbers.
