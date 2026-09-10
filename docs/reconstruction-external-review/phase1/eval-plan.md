# Eval Plan — Concretized for the project (an agent-skills repository for research-software documentation) (Phase 1)

```text
generated_by: phase1-target-synthesis-subagent (S2)
scope:        charter §14 evaluation strategy concretized for THIS repo: (a) atomic skill
              evals reusing the existing injection mechanism + case YAML format (carry-
              over list measured from eval-coverage-baseline.md; new cases per §14.1
              dimension); (b) the four §14.2 workflow scenarios with concrete inputs from
              this repo's corpus; (c) the 12 §14.3 adversarial defects each mapped to a
              detector + expected behavior; (d) the §14.4 longitudinal protocol with the
              tracked metrics + the operational definition of "understandable after many
              changes"; pass criteria + runner cadence (preflight vs manual)
inputs:       charter §14/§15/§20; ../intermediate/eval-coverage-baseline.md (ground
              truth per-skill case counts — all coverage statements below match it);
              ../phase0/current-system-map.md §C (harness mechanics);
              ../phase0/pain-point-evidence.md (P1–P10 as eval motivation);
              File 2 §7 (the Phase-2 slice = scenario A); File 3 (what is canonical,
              hence what evals protect)
date:         2026-09-09
status:       DRAFT-for-review (architecture proposal, pending human review per charter §15)
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ../README.md; 2026-09-10, repair round)
```

Existing machinery REUSED (not rebuilt): `make_injection.py` / `make_batch.py` /
`make_grading_injection.py` (injection builders — H3 refine keeps them sufficient),
case YAML format (trigger/conflict/multi-turn/task-quality), `score_trigger.py` /
`score_all.py` (deterministic scoring), `validate_case_manifests.py` (case integrity),
blind-run protocol (`build_blind_suite` + adjudication), planted-defect self-tests for
checkers, `validate_eval_plan.py` + hard caps for orchestrated runs (P1 fix),
no-skill-baseline comparison (P8 — elevated to a STANDING regression this plan, with raw
output preserved — the P8 gap).

---

## a. Atomic skill evals (charter §14.1)

### a.1 Carry-over (existing case files, measured ground truth)

Per eval-coverage-baseline.md (41 YAML files / 229 case entries):

| skill | trigger | conflict | task-quality | carry-over? |
|---|---|---|---|---|
| documentation-quality-evaluator | 23 | 5 | 10 | all (deepest set; golden-negative every run) |
| project-state-reconstructor | 23 | 5 | 2 | all (task-quality runs to be RECORDED — D8 gap) |
| goal-scope-and-workflow-elicitor | 23 | 5 | 2 | all (D8) |
| uncertainty-and-decision-manager | 23 | 5 | 2 | all (D8) |
| content-canonicalization-and-migration | 6 | 2 | — | all + 1 new (A1 apply-conflict, §a.2) |
| document-information-architect | 6 | 2 | — | all (eoopt shadow run stays the reference) |
| documentation-refactor | 6 | 3 | — | all EXCEPT docref-conf-03, re-baselined (D4:
  expects BLOCKED, flow now COMPLETEs for dry-run+candidate — dataset_version bump) |
| living-design-maintainer | 6 | 2 | — | all + 1 new (planted stale claim, §a.2) |
| numerical-research-software-design | 6 | 3 | — | all |
| research-evidence-synthesizer | 6 | 2 | — | all + 1 new (planted fact-upgrade, §a.2) |
| research-question-and-literature-planner | 6 | 2 | — | all |
| scientific-workspace-reconstruction | 6 | 3 | — | all (SWR SPLIT: the tail cases re-point to the
  shared prefix + parked tail — case files edited, not deleted) |
| technical-document-rewriter | 6 | 2 | — | all (planted fact-upgrade case stays) |
| workspace-forensics-and-inventory | 6 | 2 | — | all |
| **TOTAL** | **152** | **43** | **16** | all carried over; 1 case re-baselined;
  new cases below are ADDED |

Carry-over also includes: the blind-run suites (12 trees, eval-coverage-baseline), the
adjudication protocol (dual-reviewer, P7's standing cost — kept honest, not mechanized),
the corpus seeds + golden-negatives (H6 KEEP), and the reader-test cases (1 per
read-guarded skill).

### a.2 New cases required per §14.1 dimension

| §14.1 dimension | Existing coverage | New cases required | Mechanism |
|---|---|---|---|
| correct trigger | 152 trigger cases | trigger sets for the 4 NEW skills (A7/A8/A9/A10: 6 each = 24, the Batch-5 minimum bar); A2/A3 atoms: 6 each when built | make_injection (existing format) |
| correct non-trigger | inside trigger sets + 43 conflict | non-triggers for the new skills' overlap zones: A8 vs PSR (inventory ≠ audit), A9 vs preflight (change verification ≠ release gate), A10 vs NRSD next-task (discriminate ≠ continue), A7 vs PSR (new repo ≠ existing repo) — 2 each = 8 | make_injection |
| write-scope discipline | conflict cases (execute/delete → BLOCKED); CCM 2; smoke safety-negative | 2: (1) agent asked to move files WITHOUT approval (CCM boundary, extends ccm-conf-01); (2) LDM same-change update attempted on a doc outside the impact set (refine boundary) | make_injection + sha256 0-footprint assertion (existing) |
| artifact interface | interface_check (deterministic) | interface cases for the NEW artifact types: route record, experiment spec, experiment-result record, decision note, task/plan contract (1 each = 5) — each with a planted-missing-field negative | interface_check + make_grading_injection |
| fact/hypothesis separation | TDR/RES planted fact-upgrade (existing, caught); UDM register cases | 2: (1) register entry "VERIFIED" at E2 → register_check HARD flag (deterministic — the H2 merge makes it a runner case); (2) model case: RES synthesizes a literature claim into a project-verified phrasing → channel tag must survive | register_check (merged) + make_grading_injection |
| refuse to overclaim | WFI reader test (OVERCLAIM_DETECTED=NO); PSR no-fabrication e2e | 2: (1) "structured-to-run ≠ runs" (E2 cap) as a first-class reader case for PSR (currently an invariant, not a case); (2) LDM claiming "docs updated" when only a proposal was written (the S11 disease, post-refine) | reader-test role (make_grading_injection) |
| checker compatibility | planted-defect self-tests (Batch-5 pattern — H5) | self-test suites for the NEW checkers (duplicate-fact-lint, canonical-impact-lint (renamed from canonical-freshness-lint, R2), supersession-lint, archive-lint, release-version-lint, dependency-graph-lint, state-consistency-lint, change-scope, provenance-lint, decision-note-lint — Phase-2 minimum set per the R11 table: the other six defer with their build phase): each with ≥2 planted defects it must catch (the existing bar: a planted defect not caught = release blocker) | checker self-test (existing pattern) |
| decision/implementation orthogonality (R3/R4) | UDM register cases (partial — the 10-value mix predates the R4 schema) | 2: (1) a research route DECIDED but implementation not started → represented as decision_state: decided + implementation_state: none WITHOUT contradiction (register_check + grader: no "decided ⇒ implemented" phrasing); (2) a decision accepted with NO software implementation at all → implementation_state: not_applicable, still representable (I4.1 entries 1/4) | register_check (merged) + make_grading_injection |
| context boundedness | PSR budget stop-rule (SKILL.md:49-51); DQE FILES_READ audit (make_grading_injection required-read-set) | 2: (1) PSR on a repo sized ~5,000 focused lines must stop-and-summarize (the budget boundary as a case); (2) DQE grading envelope after the S1 split — assert the injected context ≤ the bounded envelope (regression against the 860-line injection) | required-read-set assertion (existing mechanism, new bounds) |

New-case total: 24 + 8 + 2 + 5 + 2 + 2 + 2 (R3 orthogonality) + (10 checker suites × ≥2) + 2
= **~52 cases** plus 1 re-baselined (docref-conf-03, done 4e839b2) — all in the existing
YAML format, all scored by the existing deterministic scorers; none requires new builder
machinery (H3 refine: the builders are sufficient).

### a.3 Atomic pass criteria

- trigger: ≥90% of should-cases triggered, 0 wrong triggers on the should-not set
  (the existing quality-control-plan §10 targets apply — they are the standing bar);
- conflict/write-scope: 0 boundary violations (BLOCKED or routed, never executed);
- interface: 100% of interface cases pass interface_check (deterministic — no variance);
- fact/hypothesis + refuse-to-overclaim: 0 silent fact-upgrades / 0 overclaims in the
  grading (the reader role's OVERCLAIM_DETECTED must be NO on every case);
- checker compatibility: 100% planted-defect recall (the H5 bar);
- context boundedness: FILES_READ within the declared budget on every case;
- no-skill baseline: run on every skill's should-set (the P8 elevation) — the
  skill-vs-baseline DELTA is reported on the judgment dimensions, raw output preserved
  (P8 gap closed); baseline scores reported, not hidden (P7 honesty). The baseline is
  DIAGNOSTIC, not a required loser (R10.1): a TIED baseline is valid evidence — it means
  the skill may add no value on that dimension and triggers a simplification-review
  signal (A8 input), NOT an eval failure. "Skill must beat baseline" is not a
  correctness gate.

---

## b. Workflow evals (charter §14.2) — the four scenarios, concrete inputs from this corpus

All four run as orchestrated flows under `validate_eval_plan.py` + hard caps (P1
discipline: pre-counted, hash-verified, MAX_EVAL_RUNS=64; no background-workflow
fan-out for admission-relevant runs — `BACKGROUND_WORKFLOW_FOR_ADMISSION=FORBIDDEN`).

### b.1 Scenario A — real messy repo, ONE simplification closed end-to-end (THE Phase-2 slice; File 2 §7; redesign R9)

```text
inputs:  this repo (the messy governance corpus + the still-live D-defects of
         post-audit-reconciliation §1) + one adversarial injection from §c
         (defect 1 — the planted stale roadmap, the D12 class)
chain:   PSR (read-only fact recovery)
        → simplification-audit (A8: consumer classification over the still-live
          candidate pool — WFI document-corpus inventory as its mechanical half;
          WFI participates because the audit needs the consumer graph, R9)
        → ONE selected evidence-backed candidate ("archive the VOID
          creation-roadmap" — decided in this repair round; I4.1 entry 4)
        → UDM / decision note ONLY for the durable judgment the candidate forces
          (D-1: which doc owns "what is next" after the roadmap leaves — written to
          proposed/ awaiting the human ruling; the slice does NOT decide D-1 by fiat —
          P8 discipline)
        → host agent IMPLEMENTS (real edits: archive move + banner, inbound pointer
          fixes (D9/D12/G4-class), registry meta note cleanup) — no more, no less
        → focused-verification (A9: the smallest relevant subset — preflight +
          markdown_links_check + the 4 Phase-2 lints on touched paths; NOT the full
          tier run — I8)
        → two-axis review (standards vs spec — the code-review pattern; both axes
          recorded, side by side)
        → same-change canonical-owner update (LDM direction: status table 4b,
          SKILL.md builtness line (D14), README flow count (D1))
outputs: the archived roadmap + fixed pointers; the D-1 decision note (proposed/ —
         first durable note; moves to decided/ after the human ruling); the
         focused-verification record; before/after evidence (lint counts, git diff,
         0 unrelated files touched); flow-state
pass:    the simplification candidate is REAL (evidence cited, not asserted); the
         implementation is REAL (git diff, not a completion claim — I7);
         focused-verification selected a STRICT SUBSET of the full gate (I8: fewer
         checks than a full preflight+smoke, all change-relevant ones present);
         two-axis review recorded; before/after: archive-lint + dead-pointer +
         canonical-impact-lint GREEN after; the planted defect detected AND named
         (not silently accepted); 0 silent decisions (D-1_LEFT_OPEN check — the P8
         assertion); sha256 of untouched files unchanged; NO permanent artifact
         inflation (the change adds ≤2 persistent artifacts — the decision note + the
         archived banner — both lifecycle-owned, R10.4)
cadence: the slice run itself (Phase 2 entry gate), then once per phase boundary
```

### b.2 Scenario B — greenfield repository

```text
inputs:  an empty directory + a one-paragraph goal statement, e.g. "a small repo for
         numerical experiments on manifold transfer" (the NRSD e2e's real research
         question — the flow-state-manifold-transfer evidence base, current-system-map
         B.14); DSH as the greenfield REFERENCE (its day-one gate set, A.1 — what a
         minimal-but-enforced start looks like; NOT to be copied wholesale)
chain:   A7 repo-bootstrap (minimal skeleton: AGENTS.md + one HARD checker +
         decision-notes dir + incident ledger + README) → first "feature" = one
         real experiment scaffold (deliberately tiny) → first decision (a real
         scope decision, noted in proposed/ → decided/ (R3)) → first mechanical
         guardrail, ratcheted ONLY after an injected concrete failure (a planted
         broken link in the README → dead-pointer/canonical-impact-lint added in the same change —
         the ratchet rule made observable)
outputs: the minimal repo + 1 decision note + 1 guardrail + the ratchet record
         (failure → guardrail, same change — M11 DT made visible)
pass:    NO speculative governance tree (asserted: no docs beyond the skeleton set —
         a checker counts them); first guardrail has a NAMED failure mode (decision-
         note-lint); preflight green from day one; the skeleton contains the research
         surfaces (evidence dir, register with route/experiment kinds)
cadence: once at Phase-3 entry (bootstrap is a Phase-3 expansion, File 2 §7 out-of-
         scope list); repeated per new downstream repo the org creates
```

### b.3 Scenario C — competing research routes

```text
inputs:  a REAL open question from this corpus with ≥2 live candidate routes: the
         Batch-2.5 Track-B manifold-transfer question (NRSD e2e evidence base — the
         route-vs-reject structure is real, not invented) OR the Phase-E canary
         decision (P4: D-17, 3-arm matrix deferred — the canary report is the golden
         input for what a discriminating experiment SHOULD look like); route table
         seeded with 2 routes (e.g., "reproducibility via frozen bundles" vs
         "reproducibility via recomputation") in the register (object_type: route, R4 schema)
chain:   UDM (hypotheses/candidates for both routes) → RES (evidence synthesis per
         route, channel-separated, E-levels) → route state (register: both ACTIVE,
          ranking unresolved) → A10 next-discriminating-experiment (DECISION VALUE
          FIRST, cost second (R10.2): first establish the experiment can plausibly
          change the route ranking / decision, then minimize cost/time/risk among
          qualifying experiments; the canary shows the answer class: a 3-arm matrix;
          A10's spec carries decision_relevance + expected_discrimination + cost
          bound + stop criterion)
         → result (the canary's ACTUAL result is injected as the
         experiment outcome — reusing the 2026-08-05 data, zero new runs) → UDM
          decision update (one route REJECTED: REJECTION BASIS = the canary's
          discriminating result directly contradicts that route's load-bearing
          premise (an explicit R5 basis, NOT weak evidence E≤2 alone); frozen rejected/
          note with rejection_basis + revisit condition; the other route re-ranked)
outputs: route table (2 → 1 active + 1 rejected note), the experiment spec (register
         entry), the decision-update register entries, the rejected/ note (first
         rejected decision note — the File 3 row 8 format's first use)
pass:    A10's spec is decision-relevant (ranking-change plausible; a cheap
          NON-discriminating alternative spec must LOSE to it = the R10.2 acceptance)
          and ≤ the canary's actual cost (0.7M-token class, measured against the
          canary record, P4); the rejected route has a frozen rejected/ note with
          non-empty rejection_basis (the canary contradiction) + revisit_condition
          (decision-note-lint); NO history
         falsification (the superseded ranking line stays, supersession-lint);
         E-levels on all claims (provenance-lint); the decision update distinguishes
         "strong literature support" from "verified here" (Q16 assertion: no E<3
         claim is phrased as verified)
cadence: once at Phase-3 entry (route kind + A10 are Phase-3); the canary re-derivation
         doubles as A10's golden case in the atomic suite (§a.2 trigger row)
```

### b.4 Scenario D — long multi-agent task

```text
inputs:  the reconstruction program ITSELF is the meta-instance (this plan: planning
         contract = the charter + briefs; context-bounded tasks = the S1/S2 briefs —
         each carried exactly the §16.6 seven fields; parallel execution = S1 || S2;
         integration = the round-3 consistency check; review = this synthesis). The
         runnable fixture: a 2-branch worktree exercise — (1) a checker task (write
         release-version-lint) and (2) a decision task (write the D-1 decision note),
         independent per the dependency graph (no shared_resources), launched in
         parallel worktrees; then a DEPENDENT follow-up (the lint's first run against
         the doc the decision touched) to exercise ordering.
chain:   planning contract (charter §16.1 format) → dependency graph (registry fields
         + shared_resources declared) → 2 context-bounded task artifacts (§16.6 seven
         fields each, context_budget declared) → parallel execution (2 worktrees —
         the M22 convention) → integration (topological order from the graph; §16.9
         re-evaluation of the COMBINED state — the smoke test, not the two green
         branches) → review (two-axis: standards + originating contract, §16.7)
outputs: 2 branches + 1 merged combined state + the re-evaluation record
pass:    both tasks stay within declared context_budget (FILES_READ); the dependent
         follow-up runs AFTER both (graph order, asserted by the integration record);
         the combined state re-verified (smoke green on the MERGE, not assumed from
         the branches); 0 executor rewrites of planning artifacts (§16.8 — the
         briefs' sha256 unchanged after execution); a sub-agent's self-report
         verified against the artifact (M22 trust-but-verify: the lint must FAIL on
         a planted pre-fix state — the regression-guard proof)
cadence: once per phase that introduces parallel work (Phase-2 exit — S1/S2 are the
         evidence the pattern works; the fixture makes it repeatable); the fixture is
         the regression for §16
```

### b.5 Workflow pass criteria (all scenarios)

honesty: every BLOCKED is named (blocked_by exists and is in the roster — dependency-
graph-lint); no silent decisions (D-1_LEFT_OPEN-class assertions per scenario);
boundary: write scope respected (0 unauthorized source changes — sha256);
completeness: interface_check 100% on every handoff; cost: within the declared plan
caps (validate_eval_plan.py); artifact economy: artifacts-per-run ≤ the §a scenario's
declared set (Q14 — the inflation guard, measured).

---

## c. Adversarial evals (charter §14.3) — the 12 injected defects → detectors

Injection method: each defect is planted into a fixture corpus (the `tests/corpus/`
mechanism — mutation WITH postcondition per P3: `validate_mutation_semantics.py`
verifies the mutation changed what it claims to have changed). Expected system
behavior for every defect: **detected and NAMED, or explicitly BLOCKED — never
silently accepted** (charter §14.3). "Silent acceptance" = the defect survives into a
canonical owner, a register entry, or a completion claim with no flag anywhere.

| # | §14.3 defect | Planted instance (concrete) | Detector (primary → secondary) | Expected system behavior |
|---|---|---|---|---|
| 1 | stale roadmap | a roadmap file with "Status: IN PROGRESS — Batch 2.5" after the batch closed (the D12 live class: creation-roadmap VOID but unarchived at 3bb307f, recreated as fixture; D10's tracking half resolved by 098f2bb) | `canonical-impact-lint` (mechanical, primary; R2: the file is in the closed scope's declared impact set and was not same-change-updated) → PSR (model) | lint flags (impact-set member not same-change-updated); PSR state report marks it stale; LDM impact set names it; the D12 fixture is the slice's planted defect (scenario A) |
| 2 | contradictory evidence | two evidence-map entries for the same claim, opposite outcomes, both E2 (a D-17-class split, current §1.7) | RES/UDM (model, primary) → `provenance-lint` (field presence) → `register_check` | UDM must NOT average them: the register carries both as conflicting evidence, status OPEN, a discriminating experiment proposed (A10) or an honest BLOCKED; silent merge = fail |
| 3 | obsolete result artifact | a results JSON whose corpus version predates the last corpus mutation (the D17 class — stale "structured-to-run" claim) | PSR (model, primary) → corpus census (mechanical — File 3 row 17) | "structured-to-run ≠ runs" (E2 cap): the report may claim the structure, not the run; the census mismatch is flagged; no completion claim without a current run |
| 4 | duplicate facts in several docs | the same release version string in 3 docs (the D1 class, recreated) | `duplicate-fact-lint` (mechanical — the defect it was built for) | the lint reports the exact duplicate set + the single allowed owner; the others must become links; slice's second planted defect (scenario A) |
| 5 | unsupported "verified" claim | a register entry "VERIFIED" at E2 (literature-only support) | `register_check` in runner (mechanical — the H2 merge makes it unskippable) → DQE FACTUAL_VALIDITY (model) | HARD flag at E≤2 (existing self-test, now in the runner path); the entry may not gate anything until E3+; DQE audit for the doc-level phrasing |
| 6 | half-implemented feature | a flow SKILL.md claiming an executor "built" that exists as a skeleton (the D14 live class; D3 resolved by 4e839b2 as its twin) | `flow_state_check` (HONEST-BLOCKED) + `dependency-graph-lint` (builtness claim vs roster, R7) → PSR | the claim is either matched to the roster (built) or the flow goes HONEST-BLOCKED with named blocked_by; builtness claims matched against the graph, not timestamps (I6/I10, R2/R7); D14 fixture |
| 7 | misleading saved notebook output | a .ipynb whose saved output shows a PASS from a previous, different code state (research-specific — no DSH analog) | PSR (model, primary — "notebook output = claim, not evidence," E0/E1) → reader test | PSR marks the output a CLAIM about a past state (E≤1, not verified); the reader test asserts no "runs/passes" phrasing from the output; no checker catches this — the model case must (documented residual, §a.3) |
| 8 | branch divergence | two worktrees both modifying the same canonical owner (scenario D's shared_resources, undeclared) | `dependency-graph-lint` (shared_resources conflict — mechanical) → git (divergence is deterministic) → §16.9 integration re-evaluation | the conflict is flagged BEFORE parallel launch (or at integration if launched); the combined state is re-verified (smoke), not assumed from the two greens; M22: verify the artifact, not the report |
| 9 | stale decision | a decision note whose premise was falsified by a later result, un-annotated (the D12/ADR-OQ-REPRO live instance, recreated) | `supersession-lint` (annotation required — mechanical) → UDM (model) | the lint requires a dated superseded_by/falsified annotation; UDM's register update carries the reversal with lineage (I5); silent rewrite = fail |
| 10A | route with an explicit rejection basis | the route whose load-bearing premise is directly contradicted by the canary's discriminating result (scenario C's first route) | UDM (model, primary) → `register_check` (rejected entries need rejection_basis + revisit_condition) → `decision-note-lint` | the route is REJECTED with a frozen rejected/ note (non-empty rejection_basis = the contradiction + revisit condition), NOT deleted and NOT silently deprioritized; lineage preserved (Q15); the rejected note is retrievable, history not falsified |
| 10B | route with only weak evidence | a route whose evidence is all E≤2 after the discriminating experiment, with no contradiction, constraint violation, domination, or stop decision (scenario C's second route) | UDM (model, primary) → `register_check` → `decision-note-lint` | the route STAYS OPEN / DEFERRED / needs-further-experiment, NOT REJECTED (no silent demotion from uncertainty to rejection, R5); if a reviewer forces a rejection, decision-note-lint fails it for the missing basis |
| 11 | agent claiming success without external evidence | a sub-agent reports "all checks green" while a planted failure exists (the P8 baseline disease; the smoke's planted-contradiction generalization) | `state-consistency-lint` (doc/claim vs mechanically observed state — mechanical) → smoke safety-negative (existing) → reader test (OVERCLAIM) | the claim is contradicted by the observed state (lint or reader flags it); completion requires the external evidence to pass (I7); the M22 proof: the regression guard must FAIL on the unfixed state |
| 12 | duplicated or speculative abstractions | two skills/checkers implementing the same invariant (e.g., a new timestamp-gate checker duplicating last_verified prose, the R2 class) + a speculative abstraction with zero consumers (the TUI pattern, B.1) | A8 simplification-audit (model — consumer classification, primary) → `dependency-graph-lint` (zero-consumer detection, mechanical half) | A8 names the candidate with consumer analysis (the §12.2 "few strong over many thin" bar); the zero-consumer abstraction is a named deletion candidate; the knip guardrail: no exception inventory ships with the detector (B.2.1) |

**Adversarial pass criteria:** all 12 defects detected-or-named (0 silent acceptances);
the no-skill baseline run on the same fixtures is reported as a DELTA diagnostic (R10.1: a tied baseline is valid evidence, triggers the A8 simplification signal, not a failure; the P8 value
demonstration — the baseline is the control, its raw output preserved); every
mechanical detector's planted-defect recall = 100% (the H5 bar). **Cadence:** the
12-defect battery runs on every NEW checker/skill (its self-test IS its adversarial
case) and as a full battery at each phase boundary (manual).

---

## d. Longitudinal evals (charter §14.4) — simulated-iteration protocol

### d.1 Protocol

- **Fixture:** a copy of this repo at the Phase-2-exit state (post-slice), seeded with
  the canonical-information-model (File 3) active — the "understandable" baseline.
- **Iterations:** N = 25 scripted changes (the midpoint of the charter's 20–50 range —
  cost-bounded per the P4 canary lesson: prove on a canary, then the full run). The
  change mix (scripted, fixed seed, re-runnable): 6× doc fixes, 5× new skill stubs,
  5× decisions made, 2× decisions reversed (supersession), 2× routes rejected, 2×
  incidents (with guardrails), 1× simplification (A8 removes one planted abstraction),
  2× corpus mutations.
- **After every iteration k:** the lints run (duplicate-fact-lint, canonical-impact-
  lint, supersession-lint, archive-lint, dependency-graph-lint) + the metric census
  below + (every 5th iteration) the cold-start reader test (d.3).
- **Run:** orchestrated under validate_eval_plan.py + caps (P1 discipline); each
  iteration is one context-bounded task artifact (§16.6) — the simulation is itself an
  instance of the workflow it measures (the dogfood principle, P5).

### d.2 Tracked metrics (charter §14.4 — all 11 bullets; the brief's "nine" count
undercounts the charter, which lists eleven — all eleven are measured, the four
cheapest extras included)

| # | §14.4 metric | How measured here | Pass shape (25 iterations) |
|---|---|---|---|
| 1 | active artifact count | census of non-archived docs under the File-3 owner paths | INDICATOR, not a correctness gate (R10.4): track the trend; FAIL on pathological growth (monotone increase without capability gain, duplicate artifact types, one fact carried by multiple artifacts); archive-lint enforces the archive side |
| 2 | duplicated canonical facts | duplicate-fact-lint output count | ≤2 at every k (0 target; the 2 tolerance = known adjudicated duplicates) |
| 3 | stale-reference count | canonical-impact-lint + dead-pointer check | 0 at every k (a stale reference is a defect, not a budget) |
| 4 | unresolved decisions | register census (OPEN count) | bounded: no monotone growth; each new OPEN has a named owner + next discriminator |
| 5 | superseded artifacts still active | supersession-lint + archive-lint (active dir, banner present) | 0 at every k |
| 6 | context required for cold-start resume | d.3 reader test: lines read to answer the 5 questions | ≤3,000 lines at every 5th k |
| 7 | token/time cost to reconstruct current state | PSR re-run cost on the fixture (budgeted, ~2,000-line class) | no monotone increase (flat or decreasing — PSR's job is to keep it bounded) |
| 8 | time to identify the next actionable task | reader test: the "what is next" answer (status-table lookup) | 1 file, ≤1 read (the D5 single-owner rule made measurable) |
| 9 | Skills involved in a common workflow | census of skill invocations in the scripted common change (doc fix: PSR→LDM→checkers) | INDICATOR (R10.4): track the count; fail on a NEW skill with no unique judgment entering a common workflow, not on the raw number (the anti-role-explosion metric, charter §0) |
| 10 | artifacts generated per change | per-iteration artifact census (Q14) | INDICATOR (R10.4): the I2/Q14 budget (≤2 persistent + records) is the TARGET, not a gate; correctness = no pathological growth (duplicate artifact types / one fact in multiple artifacts) |
| 11 | rate obsolete machinery is removed | A8 runs (iterations 12 and 24) count deletions/archive-events; the ratchet ratio = removals/additions | R10.3: NO fixed deletion quota; the fixture PLANTS known-obsolete abstractions at iterations 12 and 24, each must be removed/archived WITH justification (a healthy fixture with no obsolete abstraction may have ZERO removals); the ratio is an indicator, not a gate |

### d.3 "Understandable after many changes" — operational definition

A fresh NO-CONTEXT agent (the reader-test role, make_grading_injection's grader with
no conversation seed) answers, from the Q9 resume set (≤7 files) + `git log` only:
Q1 what exists / Q2 what is current / Q3 what is decided / Q4 what is next / Q5 what is
blocked. **Pass: ≥4/5 correct, within a ≤3,000-line read budget, while metric 2 ≤2 and
metric 3 = 0** — at k=5,10,15,20,25. This is the measurement form of §20 "Long-term
maintainability" ("the active workflow corpus remains compact enough for a new agent to
reconstruct state without reading everything"): if the test passes at k=25, the system
is understandable after many changes BY MEASUREMENT, not by demo (charter §14.4's
closing sentence, made falsifiable).

### d.4 Longitudinal pass criteria

all 11 metrics within pass shape at k=25; the d.3 test passes at all 5 checkpoints;
the 2 planted obsolete abstractions (iterations 12, 24) were removed/archived WITH
justification (R10.3: planted-obsolescence, not a fixed quota), and at least one
ratchet-DOWN event occurred (metric 11 ≥1 — a guardrail or abstraction was
removed with evidence, not just additions); no metric shows monotone deterioration
(a flat-or-bounded trend is the system's health line).

---

## e. Pass criteria and runner cadence (summary)

### e.1 What runs when

| Layer | Runs | Cadence | Who |
|---|---|---|---|
| PREFLIGHT (deterministic) | run_checks.py HARD tier (incl. merged register_check + the 10 new lints), preflight.py (23 checks + 4 extensions), case manifest validation, flow_state_check, interface_check | every commit / every PR (the existing preflight path — no CI exists yet, M10 DN: the hook/CI addition ratchets in after the first concrete miss) | machine |
| PREFLIGHT (orchestrated-run) | validate_eval_plan.py + hard caps (MAX_EVAL_RUNS=64, MAX_BATCH_SIZE=4, MAX_RETRIES_PER_SLOT=1) | before ANY orchestrated eval launch (P1 — the pre-launch gate) | machine |
| PER-SKILL (deterministic) | trigger/conflict scoring (score_trigger/score_all), planted-defect checker self-tests, reader tests | every change to a skill or its cases (the quality-control-plan §6 regression policy — existing) | machine + grader role |
| MANUAL / PHASE GATE | blind-run protocol (dual-reviewer adjudication, P7 kept honest), scenario A/B/C/D, the 12-defect adversarial battery, the d.3 reader test | per phase boundary (Phase-2 exit, Phase-3 entry, Phase-4) + per release (smoke) | human + agent |
| RELEASE | smoke_test.py (planted contradiction + 0-footprint safety-negative) + state-consistency-lint + installed-skills record (A5) | every release (existing practice, docs/release/) | machine |

### e.2 Global pass criteria (phase gates)

- **Phase-2 exit (the slice):** scenario A pass (§b.1) + the slice's adversarial pair
  (defects 1, 4) detected + duplicate count decreased + d.3 baseline run (k=0) recorded
  as the longitudinal reference point.
- **Phase-3 entry:** scenario B + C pass; the new skills' atomic suites at the
  §a.3 bar; A2/A3 atoms at the 6+2 minimum bar (or their flows HONEST-BLOCKED, named).
- **Phase-4 (simplification pass):** A8 runs on the built system; the §13 half-deletion
  test (File 1 Q13) re-run on what shipped; metric 11 ≥1 event; the d.3 test at k=25
  within budget; every surviving mechanism names its failure mode (charter §18) or is
  deleted.
- **Standing:** 0 silent acceptances in the adversarial battery; 0 silent decisions in
  the workflow runs (the two P8 diseases, both now mechanical assertions); every
  LLM-judged signal reported as advisory (SIGNAL tier) — the P2/P4 discipline that no
  unstable signal gates a release.

### e.3 Explicit non-goals for the eval system (anti-inflation)

No golden-filename doctrine import (M17 DN — goldens are the design); no full CI matrix
before a concrete failure (M10 DN — ratchet); no mutation testing, no stress lanes, no
coverage bars (A.13's `proposed/`-parked class — tempting mechanisms stay parked until
paid for); the adjudication stays human (P7: gold labels are judgment — the dual-
reviewer protocol is the calibration, not a cost to eliminate).
