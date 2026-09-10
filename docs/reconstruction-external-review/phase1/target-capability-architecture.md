# Target Capability Architecture (Phase 1)

```text
generated_by: phase1-target-synthesis-subagent (S2)
scope:        charter §9 capability model (5 lifecycle families, all listed capabilities +
              phase0-identified additions), each with current-state mapping, gap, and the
              §10 mechanism-layer decision; then the Phase-2 vertical slice (charter §15)
inputs:       charter §9/§10/§12/§15/§16; ../phase0/current-system-map.md (B.1–B.14, C, E, G);
              ../phase0/existing-skill-classification.md (S1–S14, H1–H6, G1–G6, A1–A6, §3.3);
              ../phase0/current-information-ownership-map.md; ../phase0/pain-point-evidence.md;
              ../intermediate/dsh-current-state-findings.md (M1–M32);
              ../intermediate/dsh-history-findings.md (Parts A/B);
              ../intermediate/parent-preliminary-answers.md; File 1 (target-workflow-invariants.md)
method:       per capability: CURRENT (which existing skill/checker/doc covers it, cited) →
              GAP → DECISION (mechanism layer per §10) with one-line justification.
              §10 rules applied: checker-enforceable ⇒ no skill; Git-recorded history ⇒ no
              second ledger; new skill only for repeated non-trivial judgment/orchestration.
date:         2026-09-09
status:       DRAFT-for-review (architecture proposal, pending human review per charter §15)
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ../README.md; 2026-09-10, repair round)
```

Mechanism-layer vocabulary (§10): SKILL / CONVENTION / AGENTS.md / SCHEMA / CHECKER / TEST /
CI-GATE / GIT-PR-CONVENTION / DOC-FORMAT / HUMAN-APPROVAL / EXTERNAL-TOOL / NO-AUTOMATION.
A capability may combine layers; the FIRST listed is the primary owner.
DSH transferability labels: resolved from S1's `dsh-transferability-crosswalk.md`
(phase1/, on disk at sweep time) — labels cited as "crosswalk: Mx → <§7 label>";
mechanisms absent from the crosswalk's M1–M32 register are marked UNKNOWN-CROSSWALK.

---

## 1. §9.1 Repository lifecycle

### 1.1 Greenfield bootstrap (charter §12.1)

- **CURRENT:** nothing. This repo was never bootstrapped — it started pre-git (the pre-git
  era is unrecoverable, pain-points P10) with no skeleton, no AGENTS.md, no gate on day one.
  DSH contrast: the full gate suite + lefthook + CI landed day one (`9d20a36cc4`,
  `86955b96a4`, history A.1) with the explicit rationale "agents follow enforced gates far
  more reliably than prose conventions" (founding ADR).
- **GAP:** no bootstrap capability, no minimal skeleton, no "ratchet" rule (add guardrail
  only after concrete failure) is codified anywhere.
- **DECISION: SKILL** (`repo-bootstrap`, new — phase0 A-list addition, "A7") **plus
  CONVENTION** (a minimal skeleton template: root `AGENTS.md` layout map + standing orders,
  one HARD checker wired into preflight, `docs/decision-notes/{proposed,decided,rejected,archived}` (R3: decision lifecycle folders; implementation_state is a field, not a folder),
  `docs/decision-register.md`, `docs/incident-ledger.md`, `README` current-state rule,
  optional CI; NO speculative governance tree — charter §12.1) **plus AGENTS.md** (the
  ratchet rule: "add mechanical guardrail only after a concrete need/failure; name the
  failure mode in the decision note" — I11/charter §18).
  Justification: the non-trivial, repeated judgment is "what is the MINIMUM sufficient
  structure for THIS repo's nature" — a per-target judgment a template alone cannot make,
  and it recurs for every new research repo (charter mission #1). The template keeps the
  mechanical half out of the skill's head.

### 1.2 Bounded inventory

- **CURRENT:** `workspace-forensics-and-inventory` (WFI, v0.1.0): shallow tree + sampled
  high-signal files, orphan candidates, "runs/passes" assertions forbidden (reader test
  OVERCLAIM_DETECTED=NO, registry:190-198); evals 6 trigger / 2 conflict (eval-coverage-
  baseline).
- **GAP:** boundary with PSR on "candidate canonical source" is loose (S5 REFINE; the three-
  place canonical-home co-ownership, classification §3.3 problem 1); WFI proposes canonical
  homes that DIA then re-decides and the harness table re-states.
- **DECISION: SKILL** (existing WFI, REFINE per phase0) — boundary rule: WFI INVENTORIES
  (facts: what exists, what's tracked, orphan candidates) and PROPOSES candidate homes only
  as flagged candidates; DIA DECIDES canonical homes; the harness `canonical-source-map.md`
  is replaced by the File-3 `docs/canonical-source-map.md` (single owner, I2).
  Justification: inventory judgment (what to sample, what is "high-signal" under budget) is
  repeated non-trivial judgment; the canonical-home DECISION stays with DIA (one decider).

### 1.3 Project-state reconstruction

- **CURRENT:** `project-state-reconstructor` (PSR, v0.2.0): read-only fact recovery,
  "structured-to-run ≠ runs" (E2 cap), no-fabrication, ~2,000-line budget (PSR SKILL.md:49-
  51); evals 23 trigger / 5 conflict / 2 task-quality (eval-coverage-baseline) — the
  deepest-tested atom.
- **GAP:** none intrinsic (S2 KEEP); stale upstream note in registry (D7) is a doc bug, not
  a capability gap.
- **DECISION: SKILL** (existing PSR, KEEP). Justification: the core fact-recovery judgment
  (separate current fact from stale doc from historical intent, charter mission #2) is the
  system's load-bearing detector; every other capability in this file reads its output.

### 1.4 Simplification audit (charter §12.2)

- **CURRENT:** nothing. No capability can identify orphan scripts / duplicated pipelines /
  multiple implementations of one algorithm / prototype-becoming-dependency / obsolete
  config paths (charter §12.2 target list); the VOID roadmap's archive move was a human
  action with no audit trail (D12).
- **GAP:** the ratchet's remove side (I11) has no owner; DSH `dsh-find-simplifications` is
  the seed (M31) — its consumer-classification method (does anything consume it? is the
  consumer obsolete too?) is the transferable core; its knip-style exception-inventory
  trap is the part NOT to copy (Q12).
- **DECISION: SKILL** (`simplification-audit`, new — "A8") **plus CHECKER** (input:
  `git ls-files` inventory + consumer graph from `dependency-graph-lint` — machine
  candidates in, judgment out). Justification: consumer classification — "few evidence-
  backed candidates over a large shallow list" (charter §12.2) — is exactly the repeated
  non-trivial judgment §10 reserves for skills; the candidate GENERATION is mechanical and
  stays in the checker. crosswalk: M31 → RESEARCH-SPECIFIC ADAPTATION REQUIRED
  (the commissioned adaptation; the knip exception-inventory trap is the part NOT to copy).

### 1.5 Migration / restructure planning

- **CURRENT:** `content-canonicalization-and-migration` (CCM, v0.1.0): dry-run migration
  map, invariants may_move/delete/overwrite=false, no target==source, no duplicate primary;
  checker self-test catches planted violations; proposal-only (write approval boundary,
  registry:296-300).
- **GAP:** the APPLY half is missing (A1: no executor that applies an approved map under the
  same invariants) — this is what keeps the whole doc-refactor loop dry-run (Q14).
- **DECISION: SKILL** (existing CCM, KEEP per phase0 for planning) **+ SKILL-mode** for A1
  (apply-mode executor: consumes an APPROVED map, applies move/delete/rewrite, verifies
  sha256 + invariants after, emits provenance). Justification: planning judgment (what
  moves where) and apply judgment (conflict handling at apply time, verification of the
  post-state) are both repeated non-trivial; the invariants themselves stay CHECKER-
  enforceable (existing CCM checkers run before AND after apply).

### 1.6 Repository health / contract verification

- **CURRENT:** the eval harness as health instrument: `preflight.py` (23 checks, version/
  dependency/registry consistency), `run_checks.py` (HARD/ADVISORY/SIGNAL tiers),
  `smoke_test.py` (end-to-end, planted state contradiction, 0-footprint safety-negative),
  `interface_check.py`, `flow_state_check.py`, `status_vocab_check.py`, corpus manifest
  validators (current-system-map C, E; classification H1/H5 KEEP).
- **GAP:** no change-scope-aware selection (runs everything, §9.2.6); release-version
  consistency across the 11 doc headers unchecked (D1); install-state unrecorded (D6).
- **DECISION: CHECKER + CI-GATE** (existing scripts — keep; extend: `release-version-lint`
  in preflight; `installed-skills` check in preflight writing the record (A5); no new skill)
  Justification: all of this is decidable; a skill here would restate the checkers (§10).
  EXTERNAL-TOOL: none needed beyond git + python stdlib (keep — the repo already runs on
  stdlib; DSH's pnpm/lefthook stack rejected per crosswalk: M5 → TRANSFERABLE AFTER
  GENERALIZATION (the hook-split idea only, not lefthook or its hook content) and
  M10 → DSH-SPECIFIC — DO NOT COPY (no CI matrix before a concrete failure — ratchet)).

---

## 2. §9.2 Change lifecycle

### 2.1 Problem clarification

- **CURRENT:** `goal-scope-and-workflow-elicitor` (GSWE, v0.2.0): one question at a time,
  stop-when-answerable, explicit grilling boundary; evals 23/5/2 (eval-coverage-baseline) —
  tied-deepest with PSR/UDM.
- **GAP:** none intrinsic (S3 KEEP).
- **DECISION: SKILL** (existing GSWE, KEEP). Justification: adaptive elicitation with a
  stop rule is repeated non-trivial judgment; the P8 lesson (baseline "decided" D-1/D-4 by
  fiat) is exactly the failure this judgment prevents.

### 2.2 Proposal / decision capture

- **CURRENT:** `uncertainty-and-decision-manager` (UDM, v0.2.0): decision register with
  status/evidence/audit, E-levels, supersedes/superseded_by, honest BLOCKED; standalone
  `register_check.py`; evals 23/5/2.
- **GAP:** (1) the register is per-run — there is NO persistent decision register
  (ownership-map 1.6: open decisions are "session-local, not persisted"); (2) the 10-value
  status conflates dimensions (Q11.1); (3) `register_check` is not in the runner (H2);
  (4) no home for rejected-option rationale (ownership §2.1).
- **DECISION: SKILL** (existing UDM, KEEP with §12.6 REFINE) **+ SCHEMA** (orthogonal
  fields per File 1 I4, tested first on the real Batch-2.5 register + the 10 live D-rulings)
  **+ DOC-FORMAT** (decision notes, §9.5.4) **+ CHECKER** (`register_check` merged into
  `run_checks.py` HARD for register files — H2 MERGE).
  Justification: deciding what is a decision, its strength, its reversal conditions is the
  core epistemic judgment of the system (kept); the register schema and the check are
  mechanical (moved out); the persistent store is a document (File 3 row 7), not a skill.

### 2.3 Implementation planning

- **CURRENT:** nothing as a capability — per-sprint execution plans exist as frozen prose
  (the 8 archived per-sprint directives, ownership 1.8), and the reconstruction charter
  itself is the current planning artifact.
- **GAP:** no plan CONTRACT format (charter §16.1 "durable contracts" exist as a rule, not
  a checked artifact); the D4 class (stale expectations vs built state) is the measured
  failure of prose plans.
- **DECISION: AGENTS.md + SCHEMA** (plan-contract template: goal / scope in / scope out /
  dependency graph pointer / acceptance criteria / validation commands; frozen-on-accept,
  never edited — the existing 8-plan immutability practice codified). NO-AUTOMATION beyond
  a light `plan-contract-lint` (required fields present). Justification: planning CONTENT
  is judgment but it belongs to the planning agent already doing the research (NRSD front /
  UDM); the repeated, checkable artifact is the contract's fields — §10 sends that to
  schema + convention, not a new skill (a "planning skill" would be a role without a
  decision of its own — the charter §0 anti-inflation rule).

### 2.4 Context-bounded task decomposition

- **CURRENT:** none as a mechanism — decomposition is implicit in briefs (this
  reconstruction's own briefs are the de facto template: goal / sources / invariants /
  forbidden scope / expected artifacts / validation / integration dependency = charter
  §16.6).
- **GAP:** the template exists only in practice; no checked fields; the 63M runaway (P1) is
  the measured cost of an undeclared dependency graph at fan-out time.
- **DECISION: SCHEMA + AGENTS.md** (task artifact: `goal`, `context_budget`,
  `forbidden_scope`, `expected_artifacts`, `validation_commands`, `integration_dependency`,
  `depends_on` graph edge — §16.6 verbatim; enforced by `plan-contract-lint` /
  `dependency-graph-lint`). NO skill. Justification: decomposition QUALITY is planning
  judgment (already owned by §2.3's planning agent); the repeated artifact is a contract
  with decidable fields — §10: checker-enforceable things do not get a skill.

### 2.5 Implementation

- **CURRENT:** external — implementation is done by the host agent's general coding
  capability / user-installed `implement`+`tdd` skills (L3, interface-level only,
  current-system-map F).
- **GAP:** none to fill in THIS repo (the repo's product is the workflow, not a product
  codebase with its own implementation loop).
- **DECISION: EXTERNAL-TOOL / NO-AUTOMATION.** Justification: adding an implementation
  skill here would be a role with no repo-specific judgment; DSH's lesson (B.1, desktop
  shell) — a second interactive surface with no owner is dead weight.

### 2.6 Focused verification (charter §12.3)

- **CURRENT:** nothing change-scope-aware — `run_checks.py` runs every tier over a path;
  the only "smallest evidence" mechanism is DQE's corpus budget (a different axis).
- **GAP:** the P1/P3 cost record (File 1 I8); DSH `dsh-pre-push-checks` is the seed (M9):
  machine change-scope report → prose selection → "never repeat a passing check" → do NOT
  recreate the removed `check:pre-push` aggregate (A.1).
- **DECISION: SKILL** (`focused-verification`, new — "A9") **plus CHECKER** (a
  `change-scope` script producing the machine report: touched files → touched skills →
  relevant checker subset + relevant case files, from `dependency-graph-lint`).
  Justification: "choose the narrowest evidence SUFFICIENT to catch the regression"
  (charter §8.8) is the repeated non-trivial judgment §10 reserves for skills; the scope
  COMPUTATION is mechanical and stays in the checker (the DSH split, imported).

### 2.7 Code review

- **CURRENT:** none in-repo; user-installed `code-review` (L3, two-axis Standards+Spec)
  available at the interface level.
- **GAP:** no repo-standards axis yet — there is no documented "coding standard" for the
  workflow scripts beyond preflight conventions.
- **DECISION: EXTERNAL-TOOL** (existing `code-review` skill) **+ CONVENTION** (review must
  check against BOTH the task/decision contract and repo standards — charter §16.7, which
  the external skill's two-axis structure already matches). NO new skill. Justification:
  the judgment is generic (code review), not research-repo-specific; DSH `dsh-code-review`
  is not in the crosswalk's M1–M32 register (UNKNOWN-CROSSWALK); its repo-specific content is DSH's gate set
  (M13/M14) which we do not copy (Q3).

### 2.8 Integration

- **CURRENT:** none — single-agent, single-branch history (18 commits, one branch); the
  smoke test's 0-footprint check is the only integration guard.
- **GAP:** multi-agent integration ordering + "re-evaluate the combined state" (§16.9) has
  no mechanism; but NO multi-agent integration has happened in this repo yet — the need is
  projected, not observed.
- **DECISION: GIT-PR-CONVENTION** (branch + PR per change; §16.9 re-verification of the
  combined state after merge — the smoke test as the integration test) — NO new machinery.
  Justification: DSH's stacked-PR object (M21) solves ≥2-PR dependency chains on GitHub;
  this repo has not yet produced one dependent PR pair — the ratchet (I11/charter §12.1)
  says do not build the stack object before the first real dependent-PR pair appears;
  one worktree per branch (M22) is the CONVENTION to adopt now (zero cost).

### 2.9 Post-change canonical-doc maintenance (charter §12.8)

- **CURRENT:** `living-design-maintainer` (LDM, v0.1.0): maintenance-impact + stale-
  reference list, proposal-only, `approved:false` (registry:353-360).
- **GAP:** (S11 REFINE) its output is a PROPOSAL-PARALLEL artifact duplicating the same-
  change update path — the right fix is 12.8's direction: compute the impact set, then
  UPDATE THE OWNERS IN THE SAME CHANGE; a standalone report is optional, for review value.
- **DECISION: SKILL** (existing LDM, REFINE per phase0: impact set → same-change owner
  updates; standalone report only when explicit review is wanted) **+ CHECKER**
  (`canonical-impact-lint` + dead-pointer check, File 1 I6 — the mechanical half of
  "docs stay current"; R2: declared impact set + same-change discharge, not timestamp
  comparison). Justification: judging WHICH docs a change invalidates and HOW to
  update them minimally is repeated non-trivial judgment (kept as skill); detecting
  staleness is decidable (moved to checker); the "update in same change" rule is AGENTS.md
  convention.

### 2.10 (implicit) Change evidence recording

- **CURRENT:** per-run `results/` trees + `benchmark-changelog.md` (append-only corpus
  ledger) + git (ownership 1.5, 1.12).
- **GAP:** the runlog restates this (P9) — that is the defect, not a missing capability.
- **DECISION: NO-AUTOMATION** (git + append-only `results/` + the changelog ledger are the
  record; Q8). Justification: Git already records the necessary history — §10: no second
  permanent ledger.

---

## 3. §9.3 Research lifecycle

### 3.1 Idea capture

- **CURRENT:** UDM (status HYPOTHESIS/CANDIDATE entries) + GSWE (scope note carries the
  open questions); no dedicated capture surface.
- **GAP:** none functional — capture works; the gap is that captured ideas have no
  persistent home (register is per-run, ownership 1.6).
- **DECISION: SKILL** (existing UDM — capture is one of its operations) **+ DOC** (the
  persistent register, File 3 row 7). NO new capability. Justification: adding an "idea
  inbox" would be a second store for what the register already is (Q12 SQLite warning).

### 3.2 Hypothesis management

- **CURRENT:** UDM (hypothesis/claim lifecycle, E-levels, strength calibration).
- **GAP:** dimension conflation (Q11.1) — fix is the §12.6 schema (§2.2), not a new skill.
- **DECISION: SKILL** (existing UDM, REFINE via §12.6) + SCHEMA. Justification: same as
  §2.2 — epistemic state management is the system's core judgment.

### 3.3 Candidate-route management (charter §12.4)

- **CURRENT:** no route object (File 3 row 4; Q15). Routes are implied by call chains
  (NRSD) or by prose plans.
- **GAP:** active/deferred/rejected alternatives cannot be represented without falsifying
  history (Q15); no next-discriminator field anywhere.
- **DECISION: SCHEMA + CONVENTION first** (route record = decision-register entry
  `object_type: route` (R4 schema) + fields goal/status/dependencies/active decisions/open questions/evidence/
  next discriminator/next action — charter §12.4's own list) **+ CHECKER** (route table
  consistency: every route's status vocabulary legal, next-discriminator non-empty for
  active routes) — **SKILL PENDING Phase-3 evidence** (a standalone route-manager skill is
  added only if Phase 3 shows repeated non-trivial ROUTE judgment — the charter §12.4
  caution: avoid the big hierarchy "unless evidence proves it is necessary").
  Justification: today the repeated work is bookkeeping (checker-able); the judgment that
  might justify a skill (route strategy) has not been exercised at multi-route scale yet.
  DSH caution applied: research alternatives are NOT PR stacks (charter §7) — the route
  table is a register extension, not a branch model. crosswalk: M21 → DSH-SPECIFIC — DO
NOT COPY (atomic-landing principle only, re-enters if dependent PR chains appear);
M31 → RESEARCH-SPECIFIC ADAPTATION REQUIRED.

### 3.4 Evidence synthesis

- **CURRENT:** `research-evidence-synthesizer` (RES, v0.1.0): thin adapter over the
  installed retrieval stack; channel separation (literature/project/inference), E-level
  assignment with "no fact-upgrade," analogy capped E2; shadow run verified (registry:280-
  288).
- **GAP:** E-level-duplication with UDM is by design (same vocab, S8 note) — not a defect;
  synthesis output has no persistent home (ownership 1.4).
- **DECISION: SKILL** (existing RES, KEEP) **+ DOC** (persistent evidence map, File 3 row
  5 — per-run maps merge into the topic's evidence map). Justification: weighing evidence
  into claims with calibrated strength is the repeated non-trivial judgment; storage is a
  document rule.

### 3.5 Evidence provenance

- **CURRENT:** RES channel separation + E-levels; corpus-side: `seed-register.yaml` with
  sha256/commit/license + frozen `UPSTREAM-COMMITS.tsv` (but the pin file is inside a
  git-ignored dir, ownership 1.1).
- **GAP:** no provenance FIELD on claim-bearing artifacts (Q16 mechanics missing); the
  pin file's untracked location is a D10-class freeze gap.
- **DECISION: SCHEMA + CHECKER** (`evidence_level`/`evidence_state`/`source`/`fetched` on
  every claim-bearing artifact; `provenance-lint` = required fields + license present;
  pins tracked in git) — NO skill. Justification: provenance is fully decidable; DSH
  lesson (M13/M14, A.11): generated/checked provenance beats prose provenance.

### 3.6 Next discriminating experiment (charter §12.5)

- **CURRENT:** nothing — the system sequences "next tasks" (NRSD chain), never "smallest
  experiment most likely to change the route ranking."
- **GAP:** charter mission #4's last clause ("select experiments that most efficiently
  discriminate between competing routes") has no mechanism; the Phase-E canary (P4) is the
  one time this question was answered well, by hand, at 0.7M-token cost.
- **DECISION: SKILL** (`next-discriminating-experiment`, new — "A10") **plus CONVENTION**
  (its output is a decision-register entry of kind `experiment` with cost bound, so the
  plan is pre-countable — feeding `validate_eval_plan.py`'s existing caps).
  Justification: information-gain / decision-value optimization over competing routes is
  pure repeated non-trivial judgment — the cleanest §10 skill justification in this file;
  nothing about it is checker-decidable (you cannot lint "discriminating").

### 3.7 Experiment result ingestion

- **CURRENT:** nothing as a capability — results are written into dated reports (P9's
  retroactive-logging disease).
- **GAP:** no standard result record (hypothesis tested / outcome / E-level effect /
  provenance / which route ranking changed).
- **DECISION: SCHEMA + CONVENTION** (experiment-result record under `results/` or the
  evidence map; UDM consumes it to update E-levels) — NO skill. Justification: ingestion
  is mechanical transcription + one UDM judgment (E-level update) that UDM already owns;
  a dedicated ingestion skill would be a role without decisions.

### 3.8 Decision promotion

- **CURRENT:** UDM (status → DECIDED, E3+ rule, Rule 0 admission for the DQE gate).
- **GAP:** same as §2.2 (persistent register; runner integration).
- **DECISION: SKILL** (existing UDM) + CHECKER (`register_check` in runner, H2). No new
  capability. Justification: promotion IS UDM's core operation.

### 3.9 Rejection / defer / supersede

- **CURRENT:** UDM fields (supersedes/superseded_by) + VOID banners + `rejected/` does not
  exist (ownership §2.1: rejected options have no home).
- **GAP:** D12-class silent falsification; no mechanical lineage.
- **DECISION: SKILL** (UDM makes the call) **+ DOC-FORMAT** (rejected/ decision notes with
  reason + revisit condition — DSH rejected-triplet pattern, history A.8) **+ CHECKER**
  (`supersession-lint`, File 1 I5). Justification: the judgment (reject vs defer vs
  supersede) stays with UDM; the lineage is decidable.

### 3.10 Revisit conditions

- **CURRENT:** none — "when would this deferral be reconsidered" is nowhere recorded; the
  canary's deferral of Phase E is a case in point (P4: the revisit conditions are
  implicit in the canary report).
- **GAP:** small but real — deferred decisions (DEFERRED is a live register state) have no
  machine-visible re-trigger.
- **DECISION: SCHEMA + CHECKER** (every REJECTED/DEFERRED decision note and register entry
  carries non-empty `revisit_condition`; `supersession-lint` checks it) — NO skill.
  Justification: presence is decidable; content is written at decision time by the
  decision-maker (UDM/human) — no repeated judgment to encapsulate.

### 3.11 (phase0 addition) Literature-search planning & routing

- **CURRENT:** `research-question-and-literature-planner` (RQLP, v0.1.0): thin adapter —
  question → literature-search-plan → route to the installed retrieval stack
  (wos-research / scansci-pdf / paper-fetch-skill / lit-review); "never retrieves, never
  reads, never synthesizes."
- **GAP:** L3 overlap risk (D11: deep-research listed but absent) — boundary already
  handled by non-trigger lists; OQ-4 ("merge with RES?") answered by Track-B evidence:
  keep separate (S7 KEEP).
- **DECISION: SKILL** (existing RQLP, KEEP) + CONVENTION (L3 roster recorded in registry,
  verified by preflight — closes D11 mechanically: "listed installed" must match disk).
  Justification: scoping a reviewable search plan under a stop criterion is repeated
  non-trivial judgment; routing is convention.

---

## 4. §9.4 Multi-agent lifecycle

### 4.1 Plan contract creation

- **CURRENT:** none (prose plans, §2.3).
- **GAP/DECISION:** AGENTS.md + SCHEMA (plan-contract template, §2.3) — shared with §2.3;
  no separate capability. Justification: §10 — contract fields are checkable; content is
  planning judgment.

### 4.2 Executor context contract

- **CURRENT:** the seven-field brief practice (charter §16.6; this reconstruction's own
  briefs).
- **GAP/DECISION:** SCHEMA + AGENTS.md (task artifact fields, §2.4). Justification:
  decidable fields → schema; the decomposition judgment stays with the planner.

### 4.3 Worktree / branch isolation

- **CURRENT:** none (single branch).
- **GAP/DECISION:** GIT-PR-CONVENTION (one worktree per branch, DSH M22 — zero-cost
  convention; no pool management until parallel branches actually coexist — DSH runs the
  same minimalism: "worktrees are per-branch checkouts managed by the agent/human,"
  dsh-current-state §8.6). Justification: no automation is justified before two real
  parallel branches exist (I11 ratchet).

### 4.4 Dependency graph

- **CURRENT:** four unreconciled partial views (ownership 1.9).
- **GAP/DECISION:** SCHEMA + CHECKER (registry `upstream_dependencies`/`downstream_outputs`
  + new `shared_resources`/`optional_deps` fields as the single machine graph — R7: the
  registry graph OWNS all dependency / shared-resource relations; SKILL.md carries a
  one-line pointer to its graph entry; architecture/flow views are GENERATED from the
  graph (no prose copy is synced); `dependency-graph-lint` validates GRAPH INTEGRITY
  (roster existence, no cycles, shared_resources declared, routing table ↔ registry,
  builtness claim vs roster), not prose synchronization —
  the D7/D14 staleness class becomes a lint). Justification: fully decidable once the
  fields exist; DSH's `run-gates.ts` validated-graph idea is imported as the invariant
  ("one graph, one source of truth," M6), not the runner. crosswalk: M6 →
  TRANSFERABLE AFTER GENERALIZATION.

### 4.5 Safe parallel scheduling

- **CURRENT:** conflict-matrix OK/SEQ/DENY/COND co-run rules (doc-level; "DENY without
  resolution = release blocker").
- **GAP/DECISION:** CONVENTION (charter §16.3-5: graph before fan-out; independent
  parallel, dependent serial) + CHECKER (conflict detection: two tasks touching the same
  `shared_resources` entry without a declared SEQ/DENY ⇒ flag — extends
  `dependency-graph-lint`). NO scheduler skill. Justification: scheduling at this scale is
  a plan-contract judgment already made under §16; the 63M runaway (P1) was a graph
  absence, not a scheduler absence.

### 4.6 Integration ordering

- **CURRENT:** none needed yet (§2.8).
- **GAP/DECISION:** GIT-PR-CONVENTION (topological order from the graph; §16.9 re-
  verification). No new mechanism.

### 4.7 Handoff

- **CURRENT:** the 12-field frozen interface (batch2.5-v1, 11 schemas + 11 templates +
  README) + `flow-state` — the system's strongest contract; `interface_check` +
  no-placeholder checks enforce it (current-system-map C.2).
- **GAP:** D10 (the frozen contract is git-untracked); problem 6 (no persistence/locus
  field); drift caught only under `--advisory-is-hard` (README:136).
- **DECISION: SCHEMA + GIT-PR-CONVENTION** (track `references/` in git — the freeze gets a
  version history; additive-only extension rule from the freeze README; `persistence:`
  field per Q11.4) — NO skill. Justification: a contract with decidable completeness is
  a schema; its drift is lintable (`interface_check` already exists).

### 4.8 Review

- **CURRENT:** DQE advisory (docs) + external `code-review` (code, §2.7).
- **GAP/DECISION:** EXTERNAL-TOOL + CONVENTION (§16.7 two-axis review: repo standards AND
  originating contract). No new skill. Justification: both axes exist; the workflow adds
  no review judgment of its own.

### 4.9 Failure recovery

- **CURRENT:** HONEST-BLOCKED flow-state with named `blocked_by` + registry BLOCKED rows +
  the reconstruction's own fail-resume cycle (execution-notes: two round-1 subagents died
  and resumed — the mechanism worked).
- **GAP:** no recovery RUNBOOK (a resumed agent must re-derive "where am I" from flow-
  state + reports).
- **DECISION: CONVENTION + AGENTS.md** (recovery runbook: read flow-state → read named
  `blocked_by` → resume from the failed stage; the Q9 resume set is the cold-start path)
  — NO skill. Justification: recovery follows the contract's own fields (decidable);
  the fail-resume cycle already proves the pattern works without a skill.

---

## 5. §9.5 Knowledge lifecycle

### 5.1 Canonical-source ownership

- **CURRENT:** `evals/skills/canonical-source-map.md` (10-row harness table) + 4 places
  assigning canonical homes (§3.3 problem 1) + D-1 OPEN (no decided status owner).
- **GAP:** no repo-level owner doc; the harness table is the eval system's fixture, not the
  system's declaration.
- **DECISION: DOC-FORMAT + CHECKER** (`docs/canonical-source-map.md` = File 3's table,
  tracked, single source — R6: ONE hand-maintained map; the existing harness-side table
  `evals/skills/harness/canonical-source-map.md` becomes a thin pointer / generated view
  (no second manual copy); `duplicate-fact-lint` runs against it — every owner row declares
  the fact templates that may appear once; the 4 assigners collapse to 1 decider per
  information type: DIA decides, File-3 records, lint enforces). NO skill. Justification:
  ownership is a declaration with decidable consequences; the judgment (which home) is DIA's
  existing operation, not a new one.

### 5.2 Current-state documentation

- **CURRENT:** `system-architecture.md` (stale status line, G4) + README (version drift,
  D2) + per-skill SKILL.md (self-sufficient contracts).
- **GAP:** I6 violations (7 live at the pre-repair census; re-counted per post-audit-reconciliation §1); no change-impact mechanics (R2 replaces timestamp freshness with declared impact set + same-change discharge).
- **DECISION: CONVENTION + CHECKER** (current-state prose rule + `owner:` front-matter (optional informational `last_verified:`, R2) + `canonical-impact-lint` + DSH budgets
  pattern: relocate → condense → raise with justification, M12/A.7) — the maintenance
  JUDGMENT stays with LDM (§2.9). Justification: detecting staleness is decidable; writing
  the corrected current state is LDM's judgment.

### 5.3 Research evidence store

- **CURRENT:** none persistent (ownership 1.4: Track-B evidence lives in dated run dirs
  only; "the persistent owner is absent by design" — that design is now the gap).
- **GAP/DECISION:** CONVENTION + SCHEMA (`docs/evidence/<topic>-evidence-map.md` — topic-
  level persistent map; per-run RES outputs merge in with E-levels + provenance fields;
  archive when no active route cites it — File 3 row 5). NO skill. Justification: storage
  + merge is mechanical; synthesis is RES.

### 5.4 Decision notes (charter §12.7)

- **CURRENT:** exactly one ADR (`adr/ADR-DQE-001`), no index, no rejected-options home,
  no lifecycle folders.
- **GAP:** 10 open decisions with colliding IDs (Q11.5); the decision backlog has "no
  cheap durable home" (pain-points §4.3); ADR's falsified claim un-annotated (D12).
- **DECISION: DOC-FORMAT + CHECKER** (note format per charter §12.7: Problem / Decision /
  Evidence / Alternatives considered / Why / Consequences / Revisit condition; lifecycle
  folders `proposed/`→`decided/|rejected/`→`archived/` (R3: decision lifecycle, not implementation lifecycle — implementation_state is a field, R4); `decision-note-lint`: required
  sections, non-empty Alternatives for non-trivial notes, non-empty rejection_basis + revisit-condition on rejected/ (R5: rejection requires an explicit basis — direct contradiction, constraint violation, explicit domination, human stop decision, or invalidated load-bearing premise) — the DSH `verify-agent-note-format` pattern, history A.8/M2) — NO skill.
  Justification: the FORMAT is decidable; WHEN a decision is non-trivial enough to note is
  a review-enforced prose rule (DSH kept exactly this as prose after `b1b57a0ac5`,
  history A.8.5 — a mechanism that was tried, evaluated, and left as judgment).

### 5.5 Active decision register

- **CURRENT:** per-run registers only (UDM); no persistent store (ownership 1.6).
- **GAP:** Q5/Q7/Q15 all need one; the 10 live D-rulings are scattered in 7+ files (D8).
- **DECISION: DOC + SCHEMA + CHECKER** (`docs/decision-register.md`, UDM-owned; schema per
  §12.6, revised per R4 (I4.1); `register_check` HARD in runner; global unique IDs) — NO new skill (UDM is the
  skill). Justification: the store is a document; the state transitions are UDM's
  judgment; the legality is the checker.

### 5.6 Archival / supersession

- **CURRENT:** ad hoc (VOID banner + commit; frozen bundles exist for eval assets; the
  DSH-style sealed archive exists in DSH, not here).
- **GAP/DECISION:** CHECKER (`archive-lint`, File 1 I11/I12) + CONVENTION (lifecycle
  folders from §5.4; archive at release boundary; sealing = move + freeze, simplified
  from DSH M18 — no standalone archive skill at this scale; the archive DECISION for
  non-obvious cases rides on the §12.2 simplification-audit skill when it runs).
  Justification: archive conditions are decidable once declared (File 3); the occasional
  judgment (is this note still a guardrail?) needs no dedicated skill. crosswalk:
  M18 → TRANSFERABLE AFTER GENERALIZATION (frozen-archive semantics transfer; the
  SHA-256 seal does not).

### 5.7 Stale-reference detection

- **CURRENT:** `markdown_links_check` (link existence only).
- **GAP:** pointers to VOID/archived docs are not flagged (D12/D4 live); `last_verified`
  impact-set staleness not flagged (I6, R2).
- **DECISION: CHECKER** (extend `markdown_links_check` with banner-awareness + the
  `canonical-impact-lint` same-change-discharge signal) — NO skill. Justification: decidable.

### 5.8 Corpus simplification

- **CURRENT:** none (§1.4).
- **GAP/DECISION:** SKILL (the §12.2 `simplification-audit` — shared with repo lifecycle;
  its research-specific target list is charter §12.2's: orphan scripts, stale notebooks,
  duplicated pipelines, multiple implementations of one algorithm, non-reproducible result
  artifacts, obsolete config paths, prototypes-becoming-dependencies, abandoned experiment
  branches, speculative abstractions, tests/docs that are the only consumers of obsolete
  behavior). Justification: one audit skill serves both lifecycles with a target list —
  two skills would be a duplication of the same judgment (I2 applied to the skills
  themselves).

---

## 6. Capability census and mechanism distribution

33 capabilities considered (31 from charter §9.1–9.5 + 2 phase0 additions: §2.10 change-
evidence recording, §3.11 literature-search planning — the latter already existing as RQLP).

| Mechanism layer (primary assignment) | Capabilities | Count |
|---|---|---|
| SKILL | repo-bootstrap (new), WFI (refine), PSR (keep), simplification-audit (new), CCM (keep + A1 apply mode), GSWE (keep), UDM (keep, §12.6 refine), RQLP (keep), RES (keep), focused-verification (new), next-discriminating-experiment (new), LDM (refine) | 12 (8 existing, 4 new; A1 counted as a mode) |
| CONVENTION (primary) | route table (12.4 light), experiment-result records, worktree/branch, integration ordering, current-state doc writing, corpus-simplification targets, recovery practice | 7 |
| AGENTS.md (primary) | executor/task contracts, plan-contract template, ratchet rule, review two-axis rule, Git-only rule | 5 |
| SCHEMA (primary) | orthogonal decision fields (12.6, revised per R4 — I4.1), decision-note format, dependency-graph fields, provenance fields, persistence field, route record | 6 |
| CHECKER (primary) | duplicate-fact-lint, canonical-impact-lint (renamed, R2), supersession-lint, archive-lint, release-version-lint, dependency-graph-lint, state-consistency-lint, change-scope, provenance-lint, decision-note-lint (all 10 proposed; Phase-2 minimum set = canonical-impact-lint, archive-lint, supersession-lint, decision-note-lint, R11 — the other six defer with their build phase) + register_check-merge + existing tier kept | 12 (10 new, 2 existing-extended) |
| CI-GATE | preflight + run_checks on PR/commit (existing, extended) | 1 |
| DOC-FORMAT (primary) | canonical-source-map, decision notes, evidence maps | 3 |
| GIT-PR-CONVENTION (primary) | integration, interface-freeze versioning | 2 |
| EXTERNAL-TOOL (primary) | code-review, implementation host skills | 2 |
| NO-AUTOMATION (primary) | implementation, change-evidence recording, integration (pre-multi-agent) | 3 |

(Counts overlap by design — a capability names its PRIMARY layer first; secondary layers
are listed in its entry. **Net new SKILLS: 4** (`repo-bootstrap`, `simplification-audit`,
`focused-verification`, `next-discriminating-experiment`) **plus A1 as a mode of existing
CCM. Net new CHECKERS: 10 (8 lints + change-scope + provenance-lint), plus the H2 merge
of register_check into the runner. Net new persistent documents: 5**
(`docs/decision-register.md`, `docs/decision-notes/**`, `docs/incident-ledger.md`,
`docs/canonical-source-map.md`, `docs/evidence/**`). **Net DELETIONS/REPLACEMENTS carried
forward from phase0:** runlog (REPLACE), creation-roadmap (REMOVE), registry narrative
meta (roster-only refactor).)

## 7. Phase-2 vertical slice (charter §15 Phase 2; redesign R9)

**The full redesign lives in `revised-phase2-vertical-slice.md`** (created in the repair
round, repair guide R9). Summary of the shape the guide requires:

```text
this repo (real messy governance corpus; the still-live D-defects of
post-audit-reconciliation §1 — no synthetic fixture for the primary loop)
  → PSR (read-only fact recovery, within budget)
  → simplification-audit (A8: consumer classification over the still-live
  candidate pool; WFI document-corpus inventory participates as the audit's mechanical
  half, only because the audit needs the consumer graph — R9: WFI is a stage
  only when actually needed)
  → ONE selected evidence-backed candidate: "archive the VOID creation-roadmap"
  (decided in the repair round — I4.1 entry 4; the ratchet's remove-side event)
  → decision note ONLY for the durable judgment it forces: D-1 (which doc owns
  "what is next" after the roadmap leaves) — written to proposed/, the human
  ruling gates it (P8: the slice does NOT decide D-1 by fiat)
  → host agent IMPLEMENTS (archive move + banner, inbound pointer fixes
  D9/D12/G4-class, registry meta note cleanup — no more, no less)
  → focused-verification (A9: smallest relevant subset — preflight +
  markdown_links_check + the 4 Phase-2 minimum lints on touched paths; NOT a full
  tier run — I8)
  → two-axis review (standards vs spec; both axes recorded)
  → same-change canonical-owner update (status table 4b, SKILL.md builtness line
  (D14), README flow count (D1))
```

**Why this redesign over the original candidate (kept for the record):**
- R9: the slice starts from a REAL messy repo and closes ONE simplification end-to-end
  (candidate → decision if non-trivial → implementation → focused verification
  → two-axis review → same-change owner updates), not a synthetic duplicate-census
  loop. The original before/after duplicate-count proof is replaced by before/after lint
  counts + git diff + 0 unrelated files touched (success remains checker-verifiable
  without model judgment).
- R9: WFI is not a mandatory slice stage; it participates only because the
  simplification-audit needs its consumer graph (participation documented, not assumed).
- R9/R11: the slice uses the MINIMUM checker set (canonical-impact-lint,
  archive-lint, supersession-lint, decision-note-lint) instead of the full 10-checker
  portfolio; deferred checkers ride with their build phase.
- R10: the slice's own eval set (File 5 §b scenario A, rewritten in this round) reports
  baseline DELTAS, designs experiments decision-value-first, and plants obsolescence
  instead of quotaing deletions.

**Out of scope for the slice (explicit, ratchet discipline):** apply-mode A1 (Phase 3 —
the slice's owner updates are hand-applied under the existing write-approval boundary,
so the slice does not depend on A1); the A2/A3/A4/A6 parked capability gaps (R12);
multi-agent machinery beyond the two parallel synthesis subagents this plan already ran
(S1/S2) as the §4.5 evidence.
