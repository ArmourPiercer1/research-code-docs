# Target Workflow Invariants (Phase 1)

```text
generated_by: phase1-target-synthesis-subagent (S2)
scope:        charter §8 (12 invariants) — current-system compliance verdicts for
              the project (an agent-skills repository for research-software documentation) + proposed mechanical enforcement; and charter §17
              (17 questions) answered as constraints on Files 2–5
inputs:       docs/plans/active/research_software_agent_workflow_reconstruction_charter.md (§8, §13, §17, §20);
              ../phase0/current-system-map.md; ../phase0/existing-skill-classification.md;
              ../phase0/current-information-ownership-map.md (duplication ledger D1–D19);
              ../phase0/pain-point-evidence.md (P1–P10);
              ../intermediate/dsh-current-state-findings.md (M1–M32 mechanism register);
              ../intermediate/dsh-history-findings.md (Part A evolution + Part B negative evidence);
              ../intermediate/parent-preliminary-answers.md (starting point, re-grounded here);
              ../intermediate/eval-coverage-baseline.md
method:       each invariant: (a) exact charter statement; (b) SATISFIED/PARTIAL/VIOLATED with
              phase0 file:line evidence; (c) proposed mechanical enforcement (named checker/
              schema/test/CI/convention, or explicit judgment-only); (d) charter §20 acceptance
              criterion that verifies it. §17 answers keep/correct the parent's preliminary
              answers with phase0 evidence. DSH transferability labels: S1's
              dsh-transferability-crosswalk.md (phase1/) arrived after the first drafts; all
              former PENDING-S1 markers were swept to the crosswalk's §7 labels (DT/TAG/RSA/DN
              abbreviations as defined in the crosswalk); mechanisms absent from the crosswalk's
              M1–M32 register are marked UNKNOWN-CROSSWALK.
date:         2026-09-09
status:       DRAFT-for-review (architecture proposal, pending human review per charter §15)
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ../README.md; 2026-09-10, final consistency patch)
```

Verdict scale: **SATISFIED** = mechanism exists and phase0 found no live violation; **PARTIAL** =
mechanism exists but live violations or missing mechanics found; **VIOLATED** = no adequate
mechanism and live violations measured.

---

## 1. The twelve §8 invariants

### I1 — §8.1 Truth separation

**(a) Statement.** The information classes current repository reality / product contracts /
research evidence / hypothesis / candidate approach / open question / decision rationale /
implementation state / future proposal / execution plan / session-local context / historical
chronology must remain distinguishable; no single artifact authoritative for all of them.

**(b) Verdict: PARTIAL.** The 12-field handoff contract + E0–E5 levels + claim-status vocab
partially distinguish classes (current-system-map B.1/B.4, `references/interfaces/README.md`).
Live violations: the 10-value claim-status field mixes epistemic states (FACT/HYPOTHESIS/
CANDIDATE/STALE) with process states (DECIDED/OPEN/DEFERRED/REJECTED) in ONE field
(existing-skill-classification §3.3 problem 5; skills-registry.yaml:17-19); `flow-state`
`open_decisions` re-carries GSWE/UDM items (triple-carry, current-system-map B.3, B.12);
session-local planning outputs (goal-scope-note, literature-search-plan, document-artifact-map)
are written as frozen-interface "artifacts" with no persistence/locus field (§3.3 problem 6);
the D-17 decision state is stored in 4 inconsistent files (ownership-map D7; ADR rationale
falsified un-annotated, ownership-map 1.7/D12).

**(c) Enforcement.** (1) Schema: orthogonal fields per §12.6, revised per R4 (I4.1:
object_type / epistemic_state / decision_state / evidence_level / evidence_state /
implementation_state) as one `VOCAB.yaml` consumed by schema files and
`status_vocab_check` (extend to forbid role-mixing, not just legality).
(2) Schema: add a `persistence: canonical|transient|record` field to the 12-field interface
(fixes §3.3 problem 6 mechanically). (3) Checker: new `duplicate-fact-lint` over the File-3
owner table. Judgment-only residue: classifying a claim's epistemic level (E-level assignment)
stays with UDM — no decidable predicate exists for "is this verified enough" below the E3
threshold (UDM SKILL.md:22-29).

**(d) §20 acceptance.** "Research uncertainty — ideas, hypotheses, candidates, decisions,
evidence strength, freshness, and implementation status remain distinguishable."

### I2 — §8.2 One canonical owner per fact

**(a) Statement.** Every durable information type has one canonical owner; other documents
link to it instead of repeating the fact.

**(b) Verdict: VIOLATED.** 19 verified duplications (ownership-map §3 ledger D1–D19):
release version in 13+ files (D1); per-skill status "BLOCKED vs COMPLETE" contradictory
(D14 LIVE — `scientific-workspace-reconstruction/SKILL.md:49` lists built LDM as "not
built"; D3, its twin in `documentation-refactor`, RESOLVED by 4e839b2 2026-09-10);
"what is next" contradictory
(D5, README:116-118 vs README:7-8); D-1/D-4 decision state re-declared in 7+ files (D8);
OQ-1..OQ-5 ID collision with opposite states (D9); HF catalog pre-v0.4 vs v0.4 drifted
(D11, the check was open decision D-6, never executed); safety posture in 5 copies (D18);
registry "PRESERVED" snapshot claim vs empty dir (D19). Four places assign canonical homes
for one info type (classification §3.3 problem 1: WFI SKILL.md:31-40, DIA SKILL.md:26-42,
LDM SKILL.md:22-41, harness `canonical-source-map.md`). DSH comparison: `docs/AGENTS.md`
"one home per fact" tier taxonomy + word budgets, machine-checked where decidable
(dsh-current-state-findings M12; history A.7: 8,130 words → 984 in one budget commit).

**(c) Enforcement.** (1) File-3 canonical-information-model as a tracked repo doc
(`docs/canonical-source-map.md`) replacing the 10-row harness table as the single owner.
(2) New checker `duplicate-fact-lint`: for each owner row, a declared fact template (version
string, status line, "what is next" pointer) may appear verbatim in at most one location;
restatements must be relative links. (3) Checker: `release-version-lint` extending
`preflight.py:151-162` from per-skill versions to the release version in the 11 doc headers
(D1 today unchecked). (4) Convention: DSH budgets pattern (relocate → condense → raise).

**(d) §20 acceptance.** "Knowledge integrity — each durable fact has one owner and stale
duplication is detectable."

### I3 — §8.3 No silent promotion

**(a) Statement.** Never silently equate: idea↔hypothesis, hypothesis↔candidate,
candidate↔decision, literature evidence↔in-project verification, prototype↔supported
implementation, code existence↔tested behavior, test existence↔passing validation, agent
self-report↔external evidence, **uncertainty (weak evidence)↔rejection** (revised per
repair guide R5 — the symmetric half: no silent promotion upward, no silent demotion from
uncertainty to rejection).

**(b) Verdict: PARTIAL.** Design is the system's strongest asset: only E3+ may be called
"verified" (UDM SKILL.md:22-29); `register_check.py` flags VERIFIED/FACT at E≤2 (standalone,
current-system-map C.2 — itself an enforcement gap, H2); TDR checker self-test caught
hypothesis-as-fact (classification S10); RES shadow held no-fact-upgrade, analogy capped E2
(registry:288); "DQE ALLOW authorizes nothing" (release-manifest:50); "structured-to-run ≠
runs" capped E2 (registry:365). Live violations: the no-skill baseline DECIDED open human
decision D-1 by fiat (pain-points P8, `no-skill-baseline-comparison.md:25-31`) — the disease
is real and only skill-discipline (not a checker) prevents it; ADR-DQE-001's OQ-REPRO=A
claim was retroactively falsified by the canary and never annotated (P4d; ownership-map D12)
— a silent reversal of rationale.

**(c) Enforcement.** (1) Mechanical: merge `register_check` into `run_checks.py` as HARD for
decision-register files (classification H2) so the E≤2 flag cannot be skipped.
(2) Mechanical: `supersession-lint` — any claim/decision marked superseded/refuted must carry
a dated `superseded_by`/annotation link (closes D12-class). (3) Convention: no-skill baseline
as a standing regression with preserved raw output (closes P8 "raw output discarded").
(4) Judgment-only: E-level assignment itself (UDM) — the ≥2/3-stable-reproduction bar before
promoting a claim (pain-points P4, defect-ledger:349-350) is a judgment rule, kept prose.
(5) Explicit rejection bases (R5): a route/claim may be REJECTED only when one or more of:
direct contradictory evidence; explicit constraint violation; clearly dominated alternative
under an explicit decision criterion; human/authorized decision to stop pursuing;
invalidated load-bearing premise. If evidence is merely insufficient, the state stays OPEN /
DEFERRED / needs-experiment — never REJECTED. Enforced by `decision-note-lint` (a rejected/
note requires a non-empty `rejection_basis`) + the register schema (rejected ⇒ basis field
present + linked evidence). E≤2 alone is NOT a rejection basis (eval-plan adversarial
defect 10 split into cases A/B accordingly).

**(d) §20 acceptance.** "Verification — completion claims are grounded in external evidence";
"Research uncertainty" (candidate vs decision distinguishable).

### I4 — §8.4 Orthogonal state dimensions

**(a) Statement.** Do not use one status enumeration to mix decision lifecycle, evidence
strength, freshness, implementation progress, object role; prefer orthogonal fields.

**(b) Verdict: VIOLATED.** (1) UDM's 10-value status mixes epistemic + process in one field
(classification §3.3 problem 5; ADR-DQE-001 split only `document_lifecycle` out, ADR:62-70).
(2) The registry `status:` key is overloaded across 3 vocabularies in one file (lifecycle
experimental/planned; open-question OPEN/DEFERRED; claim-vocabulary OPEN/DEFERRED), header
declares unused values active/deprecated/replaced/retired, and "SUPERSEDED" is used as a
document status in neither vocabulary (ownership-map 1.13). (3) `flow_status` COMPLETE
conflates "scope-complete" with "approved-to-continue" (defensible in Alpha only because
release-manifest:71-73 pins completion semantics; must split when apply-mode lands).
(4) Three vocabularies coexist with cross-usage rules in prose only; `status_vocab_check`
validates legality, not role-mixing (classification S4/H5).

**(c) Enforcement.** (1) Schema: orthogonal fields — the charter §12.6 candidate, REVIDED
per repair guide R4 and TESTED against 13 real entries (state-space table in §I4.1 below —
the charter's own warning, "do not adopt this exact schema without testing it against real
examples," satisfied). The charter's `kind` enumeration is not adopted as-is: its values
are not peers (route/claim = object types; hypothesis = an epistemic role; candidate = a
selection state; decision = a lifecycle role), and one real object can simultaneously be a
route that is a candidate, hypothesis-supported, decision=proposed, implementation=none —
a single `kind` forces a lossy choice. Revised schema (frozen after the 13-entry test fit
without forced semantic compromise):

```yaml
object_type:        claim | route | experiment | design_decision | requirement | artifact
epistemic_state:    unknown | hypothesis | inferred | observed | supported | contradicted
decision_state:     not_applicable | proposed | decided | rejected | deferred | superseded
evidence_level:     E0 | E1 | E2 | E3 | E4 | E5
evidence_state:     current | stale | contradicted
implementation_state: not_applicable | none | planned | in_progress | implemented | blocked
```

Deviations from the charter candidate, each with a real-entry justification: `kind` split
into `object_type` + `epistemic_state` (hypothesis is an epistemic role — entry 11 in the
table is an experiment whose epistemic role is `observed`, not a "hypothesis object");
"candidate" is not an object type — it is `decision_state: proposed` on any object_type
(entries 2, 3); `not_applicable` added to `decision_state` AND `implementation_state` (a
ruling like D-1 has no implementation concept at all — entry 1; an experiment result has
no decision state — entry 11). No other changes. (2) One machine-readable vocabulary file
`VOCAB.yaml` (single source for schema files + `status_vocab_check` + registry header —
kills the 3-vocab overload mechanically). (3) Checker: extend `status_vocab_check` with a
role-mixing rule (each field constrained to one dimension's value set).

**(d) §20 acceptance.** "Research uncertainty" (freshness and implementation status
distinguishable from epistemic state).

### I4.1 (repair round, R4) — state-space test: 13 real entries

Per R4's procedure: the schema is frozen only after real entries fit without forced
semantic compromise. All entries below are real objects from this repository (no invented
examples).

| # | Real object (source) | object_type | epistemic_state | decision_state | evidence_level | evidence_state | implementation_state | Represents |
|---|---|---|---|---|---|---|---|---|
| 1 | D-1 canonical status owner (final ruling: option A — the status table) | design_decision | supported | decided | E3 | current | not_applicable | an accepted decision with no implementation concept (R3 case B) |
| 2 | A1 apply-mode executor (portfolio candidate) | design_decision | hypothesis | proposed | E2 | current | planned | weakly supported active hypothesis |
| 3 | Batch-4 research atoms route (registry planned rows; parked per R12) | route | inferred | deferred | E1 | current | planned | candidate route not yet decided |
| 4 | "archive the VOID creation-roadmap" (selected Phase-2 candidate, decided this round) | design_decision | supported | decided | E3 | current | planned | decided change decision with implementation planned (the Phase-2 archive move) |
| 5 | "delegate retrieval to the installed research stack" (conflict-matrix SEQ row) | route | supported | decided | E3 | current | implemented | ordinary decided route, implemented |
| 6 | LU→CG route reversal (runlog supersession, parent Q13) | route | contradicted | rejected (superseded_by CG) | E3 | contradicted | not_applicable | rejected route with strong historical evidence |
| 7 | A6 DQE terminal-gate promotion (canary-deferred) | design_decision | hypothesis | deferred | E2 | current | none | deferred decision, implementation not started |
| 8 | OQ-3 research-stack provenance/license (registry:529,580) | claim | unknown | not_applicable | E1 | current | not_applicable | claim with no decision/implementation concept |
| 9 | "frozen snapshots are PRESERVED" (registry:26; D19) | claim | contradicted | not_applicable | E2 | contradicted | implemented (temporarily in use) | contradicted claim whose associated implementation remains in use temporarily |
| 10 | DQE v0.4.1 advisory scope-out (ADR-DQE-001; Phase-E deferred) | design_decision | supported | decided | E3 | current | implemented | decision + implementation both complete |
| 11 | DQE 39-run canary (P4 record) | experiment | observed | not_applicable | E3 | current | not_applicable | experiment result with no decision state |
| 12 | "workspace-only isolation" (registry meta; D6, after the R1 line fix) | claim | supported | not_applicable | E2 | current | not_applicable | evidence-state transition with no decision involved |
| 13 | the reconstruction program route (charter-approved; Phase 1 complete, Phase-2 conditional GO) | route | supported | decided | E3 | current | none | decided route NOT yet implemented (R3 case A) |

Coverage, reported honestly (final patch P6): real-state-space coverage 7/7 — every
required R4.5 representation maps to a semantically natural real entry: weakly supported
hypothesis (2), candidate route not yet decided (3), decided route not yet implemented
(13), rejected route with strong historical evidence (6), claim with no
decision/implementation concept (8), contradicted claim with temporarily-in-use
implementation (9), experiment result with no decision state (11); plus R3's required
cases: decided + implementation none (13) and decided + not_applicable (1, D-1 after the
final ruling). No object was renamed to fill coverage — "archive the VOID
creation-roadmap" (row 4) is a design_decision with implementation planned, NOT a route.
Synthetic/adversarial schema coverage: 7/7 — the eval-plan §a.2 fixtures assert every
state combination, including ones the live repo does not currently contain, so the
checker stays exercised between real instances.

### I5 — §8.5 Decision reversal by supersession

**(a) Statement.** A durable decision must not be silently rewritten into its opposite;
reversal or material redesign must preserve decision lineage through supersession/
cross-linking.

**(b) Verdict: PARTIAL.** Mechanisms exist: UDM register entries carry `supersedes` /
`superseded_by` + audit trail (UDM SKILL.md:51-53); runlog shows a real supersession (LU→CG,
parent-preliminary-answers Q13); `creation-roadmap.md` carries a proper VOID/SUPERSEDED banner
with dated supersedee (creation-roadmap.md:3-7, commit 62ada30). Live violations: the VOID
roadmap is still tracked and still referenced by a tracked file (DQE SKILL.md:9 — D12);
ADR-DQE-001:227-230 states OQ-REPRO=A as "confirmed by the skill" after the canary falsified
it, with the annotation still an OPEN decision (ownership-map 1.7, D12; `open-decisions.md:40`);
there is no home for rejected options at all — "why was route X rejected" requires re-reading
4–5 documents (ownership-map §2.1). (Reconciliation 2026-09-10: the DQE SKILL.md:9 inbound
pointer is FIXED by 4e839b2 — D12 now PARTIALLY resolved; the unarchived roadmap + the
system-architecture status line remain live. See post-audit-reconciliation.md §1.) DSH comparison: supersession check on every new note
(`.agents/notes/AGENTS.md:5`), consolidation rule (history A.8.9), sealed frozen archive
(M18 — crosswalk: M18 → TRANSFERABLE AFTER GENERALIZATION: frozen-archive semantics
transfer, SHA-256 seal does not).

**(c) Enforcement.** (1) Checker: `supersession-lint` — every `superseded_by`/`supersedes`
pair must resolve, be non-circular, and the superseded side must carry a dated annotation;
a VOID/SUPERSEDED-bannered doc must be moved to `docs/plans/archived/` or have its inbound
pointers removed (mechanical closure of D12/D4-class). (2) Convention: decision notes
(File 3 row 8) with `proposed/decided/rejected` lifecycle folders + `archived/` (revised
per repair guide R3 — decision lifecycle ≠ implementation lifecycle): `proposed/`
proposal-oriented wording; `decided/` rewritten to present-tense ACCEPTED REALITY without
implying implementation completion (DSH's `implemented/` tracked code changes through
shipment — correct there, wrong as a research-decision folder name: a research decision can
be accepted with implementation `none` or `not_applicable`); `rejected/` frozen with reason
+ revisit condition (DSH rejected-triplet pattern, history A.8; B.4 "kept only while it
prevents a tempting mistake"); `archived/` sealed (relocation, never edit — M18).
Implementation state is an ORTHOGONAL schema field (`implementation_state`, R4), never
encoded in the path. (3) Judgment-only: judging whether a reversal is "material" (new note
+ cross-link) vs an in-place fact update (decided-note rule) — DSH keeps this prose
(`implemented/AGENTS.md`: "facts only, no decision rewrite"; reversal requires new note +
cross-link).

**(d) §20 acceptance.** "Decision durability — important decisions retain rationale,
alternatives, evidence basis, and revisit conditions without turning the active corpus into
a historical transcript."

### I6 — §8.6 Current-state docs stay current

**(a) Statement.** README, architecture, API/reference, and package docs describe current
reality; they do not become change logs.

**(b) Verdict: VIOLATED (live, system-wide).** Phase0 verified 7 live instances (pain-points
P5): `documentation-refactor/SKILL.md:47` "v0 SKELETON STOPS HERE… NOT BUILT" one day stale
vs Sprint 6B (D3); SWR SKILL.md:49 lists built LDM as "not built" (D14); README:68/70
"now at v0.2.0"/"v0.3.0" vs registry 0.4.1 (D2); `quality-control-plan.md:26-43` HF table
pre-v0.4 vs `hard-fail.md:27-34,82-98` v0.4 (D11); README:116-118 "Next: Batch 4" contradicting
its own banner 108 lines above (D5); system-architecture "DECIDED for Phase 1" with no
charter pointer (G4); DQE SKILL.md:9 → VOID roadmap (D4).
**Post-audit reconciliation (2026-09-10, 3bb307f — see post-audit-reconciliation.md §1):**
D3 and D4 RESOLVED (4e839b2); D12 partially resolved (DQE:9 fixed); D10 RESOLVED
(098f2bb); D6 install state recorded (4df8f7f). Live instances now: D1, D2, D5, D7, D9,
D11, D13, D14, D15–D19 — the verdict stays VIOLATED. Root cause measured: the volatile
state→pointer rule (HF-14b) exists but its target (D-1, canonical status owner) was OPEN
at audit time — the final ruling (option A: the status table) now closes it, so the
produced pointers resolve to a named owner once Phase-2 lands the decision note
(ownership-map §4.2) — the cure is ruled; the disease persists until Phase-2 applies it. DSH comparison: "current-state prose, one physical line per
paragraph, relocate-condense-raise budgets, machine-checkable links only" (dsh-current-state
§4.1 M12; history A.7).

**(c) Enforcement.** (1) **Change-impact discharge** (revised per repair guide R2 —
replaces timestamp-as-correctness): a change that touches a canonical authority, source,
or contract carries a *declared documentation impact set*; for every impacted canonical
owner — update it in the SAME change, or record an explicit no-doc-impact. Carriers: the
change-scope report (touched files → impact set; the A9 mechanism), the review obligation,
and the same-change convention (§12.8). New checker `canonical-impact-lint` (renamed from
`canonical-freshness-lint`): flags an owner in the declared impact set that was NOT updated
in the same change. `last_verified` MAY remain as optional informational metadata, but it
is not a primary correctness gate: changing it alone must not satisfy freshness, and its
absence must not imply staleness. This kills both failure modes of the timestamp test —
unrelated commits making a still-correct doc "stale" (false positive) and a touched
timestamp on unchanged semantics (false negative). The judgment of "is it still true"
stays with the LDM refine of §12.8. (2) Same-change rule (§12.8): unchanged in substance —
it IS the discharge obligation, now with the impact set as its machine-readable carrier
(review + the stale-reference list LDM already produces, LDM SKILL.md:22-41; promoted from
parallel artifact to same-change obligation, classification S11). (3) Checker: dead-pointer
lint (links to VOID/archived docs, existing `markdown_links_check` extended with a banner
check) — unchanged. Fixture tests (R2 acceptance): an unrelated commit does NOT flag a
correct doc; an in-scope source/contract change that leaves its owner stale DOES flag; a
timestamp-only change does NOT clear the flag.

**(d) §20 acceptance.** "Long-term maintainability"; "Messy repository recovery"
(distinguish current fact from stale documentation).

### I7 — §8.7 Evidence-backed completion

**(a) Statement.** A task can only be called complete when the relevant external evidence
passes; prefer verification of the world over agent self-report.

**(b) Verdict: PARTIAL.** Strong design: `release-manifest` completion_semantics "COMPLETE =
dry-run+candidate scope, NOT migration executed" (manifest:71-73); HONEST-BLOCKED rule with
named `blocked_by` (`flow_state_check.py:1-12`, enforced); "DQE ALLOW authorizes nothing"
(README:40, manifest:50); smoke test plants a real state contradiction ("59 tests passing" vs
"69 tests green") + safety-negative overwrite request and verifies 0 source files changed
(smoke_test.py:37-64; smoke-report-2026-08-06 PASS). Live gaps: doc-level completion claims
are not mechanically verified — the registry's "frozen snapshots are PRESERVED" claim was
false at audit (D19; parent consistency-check note 1: bundles exist only after a build run);
every LLM-judged signal was found unstable across runs — "所有靠 LLM 判断的信号都不稳定"
(canary, P2/canary-decision:122-134); no deterministic reproducibility checker exists (P4
unresolved (a)).

**(c) Enforcement.** (1) Keep the existing HARD/ADVISORY/SIGNAL tier (`run_checks.py:46-58`)
— deterministic checkers are the only stable signals (P2); completion of anything checker-
enforceable requires the checker to pass (already the design, D.9 quality-control-plan §1.1).
(2) New checker: `state-consistency-lint` in the smoke test — doc claims of the form
"N tests passing / status X / version Y" must match the mechanically observed state
(generalizes the planted-contradiction from one fixture to a standing check).
(3) Judgment-only: DQE remains an ADVISORY profile-scoped evaluator (its own canary proved a
terminal LLM gate unreliable, P4) — terminal gating only where a deterministic path exists;
the DQE promotion gate (phase0 A6) stays DEFERRED with the 3 frozen bundles as readiness
evidence (registry:26).

**(d) §20 acceptance.** "Verification — completion claims are grounded in external evidence."

### I8 — §8.8 Smallest useful evidence

**(a) Statement.** Software changes: choose the narrowest evidence sufficient to catch the
regression. Research uncertainty: choose the smallest experiment likely to change the ranking
between competing routes.

**(b) Verdict: PARTIAL (software side), VIOLATED (research side).** The system has no
change-scope analyzer or smallest-test selector at all (no §12.3 capability; `run_checks.py`
runs every tier over a path, no diff-aware selection). The cost of the absence is measured:
the 63M-token / 11h / zero-data runaway happened in an orchestrated eval with no pre-counted,
capped plan (P1; `validate_eval_plan.py` + hard caps built only after), and the 2.6M-token
matrix mostly measured corpus defects, not skill behavior (P3) — i.e., evidence chosen before
the smallest-sufficient question was asked. Research side: "smallest experiment most likely
to change the ranking" is not a mechanism anywhere (§12.5 missing); the system today runs
"next task" sequences (NRSD call chain) with no decision-value criterion. DSH comparison:
`dsh-pre-push-checks` — machine-produced change-scope report + prose selection + "never
repeat a passing check" + "do not recreate the removed check:pre-push aggregate"
(dsh-current-state §2.1, M9; history A.1: the aggregate was removed 2026-07-22 — the
anti-inflation lesson to import WITH the pattern).

**(c) Enforcement.** (1) New capability §12.3 as a hybrid: deterministic `change-scope`
report (checker/script, DSH M9) + a skill for the selection judgment (File 2 §9.2.6).
(2) New skill §12.5 (next discriminating experiment) — judgment only: information-gain /
decision-value optimization has no decidable predicate (File 2 §9.3.6). (3) Convention:
pre-counted, hash-verified, capped eval plans for any orchestrated run (existing
`validate_eval_plan.py`, P1 — extended from admission runs to all runs).

**(d) §20 acceptance.** "Multi-route research" (experiments discriminate routes); "Simplicity"
(narrowest sufficient evidence keeps the evidence corpus bounded).

### I9 — §8.9 Context-bounded task decomposition

**(a) Statement.** Decompose long tasks by the context required to execute them correctly;
do not use module/feature boundaries by default if they force each executor to load excessive
unrelated context.

**(b) Verdict: PARTIAL.** Existing mechanics: per-skill `context_budget` fields in the
registry (load-bearing, preflight reads the registry; PSR budget ≈2,000 focused lines,
stop-and-summarize near 5,000 — PSR SKILL.md:49-51); WFI "shallow tree + sampled high-signal
files; never a raw whole-tree dump" (registry:190); DQE `whole_repo_allowed: false`
(registry:63). Live gaps: the DQE grader envelope is ≈860 lines of contract injected as ONE
context (classification S1 point 1; §3.3 problem 11); the three L1 flows require the reader
to hold conflict-matrix §1 + interfaces README + flow-state schema + 7+ downstream SKILL.md
contracts to evaluate one routing decision (problem 11); NRSD's call chain spans 10 upstream
skills' contracts (NRSD SKILL.md:40-60). There is no executor-contract template: charter
§16.6's seven fields (goal / sources / invariants / forbidden scope / expected artifacts /
validation commands / integration dependency) exist in this charter only.

**(c) Enforcement.** (1) Convention: AGENTS.md executor-contract template = §16.6's seven
fields, required for every delegated task (this reconstruction's own briefs are a worked
example of the format). (2) Schema: task artifacts carry `context_budget` + `forbidden_scope`
as checked fields (extending the registry's existing pattern to task level).
(3) Judgment-only: choosing the boundary itself — "minimum necessary context, not arbitrary
feature labels" (§16.2) is a planning judgment; the checker verifies the fields exist and the
budget was respected (FILES_READ audit, existing in DQE grading, make_grading_injection
required-read-set), not that the boundary was optimal.

**(d) §20 acceptance.** "Multi-agent development — long tasks can be split by context
boundary…".

### I10 — §8.10 Parallelism with explicit dependencies

**(a) Statement.** Represent true blocking dependencies, optional dependencies, shared
resources, and independent routes; do not linearize independent work unnecessarily.

**(b) Verdict: PARTIAL (design), VIOLATED (mechanics).** Design: conflict-matrix encodes
co-run semantics OK/SEQ/DENY/COND per pair, with "DENY without resolution = release blocker"
(conflict-matrix:15); exactly-one-L1-flow-at-a-time is correct linearization for flows, not a
violation. Mechanics: there is NO machine-readable task dependency graph — four partial,
mutually-overlapping doc-level views that "were never reconciled" (ownership-map 1.9:
registry upstream/downstream fields, system-architecture §3 call chains, creation-roadmap
build order, conflict-matrix co-run rules); the Batch-2 order appears in two places
(creation-roadmap.md:78-80 + registry:25). The 63M-token runaway (P1) is the measured cost of
parallel fan-out without an explicit graph (per-character agent fan-out hit the 1000-agent
cap). DSH comparison: `run-gates.ts` with validated dependency graphs as the single source of
gate inventory (M6; history A.1 `6fc7dd4c02` — the rewire caught a gate that had never been
wired), stacked-PR atomic landing (M21).

**(c) Enforcement.** (1) Schema: machine-readable dependency graph — the registry's existing
`upstream_dependencies`/`downstream_outputs` fields ARE the single machine authority for
implementation/optional dependencies + shared resources (revised per repair guide R7: one
authority per relation type — the graph is NOT a synchronization target for prose copies).
Add `shared_resources:` + `optional_deps:` fields. SKILL.md carries a one-line pointer to
its registry graph entry, not a prose restatement of dependencies; architecture/flow
visualizations are GENERATED from the graph. New checker `dependency-graph-lint` validates
GRAPH INTEGRITY (referenced skills exist in the roster; no cycles; shared_resources
declared wherever parallel work touches them; routing table ↔ registry; builtness claims ↔
roster — the D7/D14 staleness class): it does not check equality among several
hand-maintained prose copies. Co-run semantics (OK/SEQ/DENY/COND) stay in conflict-matrix
— a genuinely different relation, not a duplicated edge (File 3 row 10). (2) Convention: parallel work launches
only with a named dependency graph in the plan contract (§16.3); independent tasks parallel,
dependent serial (§16.4-5). (3) No new scheduler machinery at current scale — DSH's gate
runner is a TypeScript monorepo artifact (crosswalk: M6 → TRANSFERABLE AFTER
GENERALIZATION — the "one validated graph, one source of truth" invariant, not the
runner); the transferable
part is "one validated graph, one source of truth," not the runner.

**(d) §20 acceptance.** "Multi-agent development — parallelized safely, and integrated with
explicit dependency/evidence contracts."

### I11 — §8.11 Complexity ratchet in both directions

**(a) Statement.** Support both "repeated failure → add guardrail" and "obsolete
abstraction/guardrail → remove or simplify"; the workflow must have an explicit
simplification path.

**(b) Verdict: PARTIAL (add-side strong, remove-side weak).** Add-side measured: HF-13/14/15
after the v0.2 false pass (P2); mutation postconditions + `validate_mutation_semantics.py`
after P3; plan validator + hard caps after P1; profile-admission Rule 0 after the D-17 canary
(P4). Each guardrail traces to a documented failure — the ratchet works in the + direction.
Remove-side: `creation-roadmap.md` is VOID since 2026-09-09 yet still tracked and
unarchived (D12 — PARTIALLY resolved 2026-09-10: the DQE:9 inbound pointer fixed by
4e839b2; the archive move + the system-architecture status line remain) — no archive
mechanism enforced the move; there is no simplification-audit capability at all (§12.2 missing; DSH `dsh-find-simplifications` is the seed); runlog
chronology grows append-only with no deletion criterion (P9); DSH's deletion record (TUI,
knip, INDEX.md, `dsh-doc-standards` consolidation, 209 empty invariant companions — history
Part B) is the benchmark this system currently lacks.

**(c) Enforcement.** (1) New skill §12.2 (simplification audit) — consumer classification is
judgment (DSH M31; the knip lesson: a detector that needs a per-skill exception inventory is
already the debt — history B.2.1). (2) Checker: `archive-lint` — VOID/SUPERSEDED-bannered
tracked docs must live under `docs/plans/archived/` (or the banner + pointers removed);
measures the remove-side mechanically. (3) Process: charter §15 Phase 4 (dedicated
simplification pass) is mandatory, not optional; every new guardrail must name the failure
mode it addresses (charter §18 "add governance without an explicit failure mode it addresses"
is forbidden) — enforced by the decision-note format (File 3 row 8: `Revisit condition`
required).

**(d) §20 acceptance.** "Simplicity — no Skill, artifact type, schema, or orchestration layer
that lacks a concrete responsibility and evidence-backed need."

### I12 — §8.12 Bounded active corpus

**(a) Statement.** Active decision/state artifacts must not grow without bound; the system
must define archival conditions, supersession rules, deletion criteria, and what should
remain only in Git history.

**(b) Verdict: VIOLATED (no rules defined).** The four required definitions exist nowhere in
the current system: archival conditions — none (18 dated reports committed as living docs;
classification §3.3 problem 12); supersession rules — ad hoc (banner + commit, no
mechanism); deletion criteria — none (everything kept; even the VOID roadmap); Git-only
content — undeclared (runlog + report front-matter + SNAPSHOT-MANIFEST all duplicate git
state, ownership-map 1.12/D16/D17). The corpus IS git-ignored where it matters
(`docs/plans/` never tracked, `references/` untracked in a4d780f — ownership-map 1.3/1.16),
so even the "archive" is not version-controlled. DSH comparison: the `proposed/` tree as the
visible buffer between "tempting mechanism" and "paid-for mechanism" (history A.13), sealed
frozen archive (M18), "rejected notes kept only as guardrail, else deleted as full triplet"
(dsh-archive-agent-notes) — the exact four definitions, in working form.

**(c) Enforcement.** (1) File 3 defines, per information type: lifecycle, update trigger,
archive/delete rule — this file set IS the missing definition (charter §13).
(2) Checker: `archive-lint` (shared with I11) + "what stays in Git" rule made explicit in
AGENTS.md: chronology, superseded plan bodies, adjudication round records, per-run raw
results = append-only records (immutable, never "current"); they are retrievable, not
load-bearing. (3) Convention: decision notes lifecycle folders give the supersession/archive
operation a home (I5). No word-count budgets on decision notes (DSH uses them as triage aids
only — dsh-archive-agent-notes SKILL.md:8 "word count only a triage aid") — judgment-only
archival classification, mechanical sealing.

**(d) §20 acceptance.** "Long-term maintainability — after many simulated changes, the active
workflow corpus remains compact enough for a new agent to reconstruct state without reading
everything"; "Decision durability" (without turning the active corpus into a historical
transcript).

---

## 2. Charter §17 — the 17 questions, ANSWERED

Method: the parent's preliminary answers (`intermediate/parent-preliminary-answers.md`) are
the starting point; each is kept, corrected, or replaced below with phase0 evidence. Parent
answer numbering differs from charter numbering (parent Q5 merges charter Q5+Q6+Q7; parent
Q16/Q17 are artifact-side expansions) — the mapping is noted per answer.

### Q1. What are the three most costly real failure modes in the current system?

**Answer (corrects the parent's three-item list into a cost-ranked chain view):**

1. **The unvalidated quality gate (P2 chain, ~70M documented tokens).** DQE v0.2.0 false-
   PASSED a broken hybrid roadmap (FAILing only on trivial HF-9, still calling it
   "substantively high quality") — the parent's (a). That single false pass spawned the whole
   v0.3→v0.4.1 program: anti-erosion gates, a 20-case corpus, dual-reviewer adjudication, the
   26-run matrix, the D.3 re-runs, and the Phase-E canary — and ended with the gate STILL
   not promotable: the D-17 canary stable-false-ALLOW (the parent's (b)) and every LLM-judged
   signal unstable across runs (pain-points P2; canary-decision:122-134). The parent's (a) and
   (b) are the two ends of ONE failure mode: a gate that had no mechanism to prove itself.
2. **Unbounded orchestrated-eval cost (P1, 63M tokens / 11h / zero data).** A background
   workflow whose `args` arrived as a JSON string iterated per-character, spawning one agent
   per character until the 1000-agent cap; the same bug class had already killed a 0-cost
   launch on 2026-07-31 and was fixed ad hoc ("已修") instead of being promoted to a
   mechanical pre-launch check (P1 "Unresolved"). Single largest one-off burn in the repo.
3. **Stale + duplicated "current state" in the governance corpus (P5, live at audit).**
   Detected by the system's own atoms on 2026-08-05 (`creation-roadmap.md:23` "IN PROGRESS"
   stale by ~2 batches, batch2_5-integration:76-81) and still present 2026-09-09 with 7
   verified live instances (P5 "Unresolved"; ownership-map D2/D3/D5/D10/D11/D14). It is the
   only top-3 failure mode still active, and it is the one a vertical slice can attack
   end-to-end — which is why the Phase-2 slice (File 2 §6) targets it.

Near-misses (ranked below the top 3 by measured cost): P3 corpus fixture defects paying for
the 2.6M matrix twice; P4 the D-16×OQ-REPRO contract collision (≈0.7M + deferred 5.6M
matrix); P7 standing adjudication cost (58–66 reviewer runs, ≥4 blocking human rounds); P8
no-skill baseline deciding open decisions by fiat (1 slot, evidential cost). The parent's
separate item (c) "independent-check + blind-matrix failures" is subsumed: its harness bugs
are P6 (recurring, cheaper), its corpus defects are P3.

### Q2. Which existing Skills already solve them adequately?

**Answer (kept, with phase0 grounding):**

- Q1.1 (false pass): **DQE v0.4.1 + the golden-negative corpus solve it for SUPPORTED
  profiles** — the eoopt hybrid roadmap is a permanent golden-negative with recall 1.0 /
  false_pass 0 (README:42-43; runlog:29), and profile admission (Rule 0) converts "cannot
  judge yet" into an honest `INCOMPLETE/unsupported-evaluation-profile` instead of a silent
  ALLOW (SKILL.md:29; P4). That is adequate as **advisory + scoped gate**; it is NOT adequate
  as a universal terminal gate (canary, P2/P4) — adequacy is profile-scoped by design.
- Q1.2 (unbounded eval): **solved at the script layer, not the skill layer** —
  `validate_eval_plan.py` + hard caps (MAX_EVAL_RUNS=64) + `BACKGROUND_WORKFLOW_FOR_ADMISSION=
  FORBIDDEN` (P1 "Addressed by"). No skill owns it; the residual gap (fix lives in a
  validator, not the harness API) is a mechanism fix, not a skill gap.
- Q1.3 (stale current state): **NO existing skill solves it.** PSR recovers facts (the
  detector) and LDM proposes updates (proposal-only, S11), but no mechanism OWNS "the current
  doc is false again" — D-1 (canonical status owner) is now DECIDED (option A: the status
  table), so the pointer has a target from Phase-2 onward (ownership-map §4.2). This is
  the largest skill-level gap in the system and the Phase-2 slice's target.
- Cross-cutting: task-quality/multi-turn coverage for PSR/GSWE/UDM is cases-built-but-runs-
  not-recorded (D8; KNOWN_LIMITATIONS #5 — eval-coverage-baseline confirms 2 task-quality
  cases each, no results runs recorded); the three Batch-5 executors carry light sets (6+2);
  cross-project generalization is single-corpus (KNOWN_LIMITATIONS #9/#10).

### Q3. Which DSH mechanisms solve DSH-specific rather than generic problems?

**Answer (kept, confirmed against the M1–M32 register + history A.13):**

**DSH-specific (do NOT copy the implementation; at most the principle):**
- TypeScript/Cordis gate internals: Oxlint/jscpd configs, `type-equiv` fences, generated
  Cordis catalogs, `verify-cordis-*` (M13/M14; history A.11 rows 3, 13).
- Bilingual triplet + pairing gates + merge driver (M15) — an organizational requirement.
- Sandbox kernel-proof lanes (M25, Landlock/bwrap/Seatbelt product).
- `record-browser-gif` (M26) — GUI-product evidence; the *pattern* (evidence chain for a
  claim a reviewer cannot verify) is transferable, the GIF is not.
- Issue/PR policy engine (M16) + trusted-branch App token (M32) — GitHub-surface machinery.
- Vendored-Cordis-as-source policy, pre-release "remove at first tagged release" stance as a
  license for deletion volume (M4; A.13) — posture, not mechanism.
- 100% per-file coverage as a deletion prompt (M7) — semi-generic bar, pre-release-scale
  feasibility (A.13); do not import the bar, import the "uncovered line = deletion candidate"
  reading.
- Skill self-maintenance loop with private out-of-repo tooling (M20) — infra-specific.

**Generic (transferable — §7 labels resolved per crosswalk §1/§2; distribution
DT×5 [M3, M4, M11, M12, M19] / TAG×12 [M1, M5, M6, M8, M9, M13, M18, M22, M23, M24, M28,
M30] / RSA×2 [M2, M31] / DN×13):**
- AGENTS.md standing-order layering (M1 → TAG); Agent Note decision lifecycle: path-
  encodes-state, closed class set, mandatory alternatives, supersession-on-creation,
  sealed archive (M2 → RSA, M18 → TAG, M19 → DT — history A.8's maturation, each step
  added after a measured drift incident); fast-local-hooks vs exhaustive-CI split
  (M5 → TAG, M10 → DN — the split idea transfers, the hook content and the CI matrix do
  not); pre-push smallest-evidence selection with machine change-scope report (M9 → TAG
  — seed of §12.3, charter §7's own calibration example); gate runner as single source of
  truth (M6 → TAG, idea only); postmortem→guardrail loop (M11 → DT); doc tier taxonomy +
  one-home-per-fact + budgets (M12 → DT); record/replay snapshot tier (M8 → TAG — idea
  generic, profile composition DSH-specific); one worktree per PR branch (M22 → TAG — the
  two judgment rules transfer, the checkout topology does not); test-reliability doctrine
  + flake diagnosis taxonomy (M23 → TAG); simplification audit with consumer
  classification (M31 → RSA — seed of §12.2, the commissioned adaptation); the `proposed/`
  buffer for tempting mechanisms (A.13); the perf-gate lesson (A.6: quality/perf scores
  are interpreted signals unless a calibrated deterministic harness with a named budget
  exists — directly applicable to DQE).
- MOVED to DSH-specific per the crosswalk: stacked-PR native landing (M21 → DSH-SPECIFIC
  — DO NOT COPY: "charter §7's own example applies verbatim"; nothing to serve at 18
  commits / no PR workflow — the atomic-landing principle re-enters only if dependent PR
  chains appear, File 2 §2.8).

### Q4. Which proposed rules belong in Skills versus mechanical gates?

**Answer (kept; the split, re-grounded):**

**Mechanical (checker/schema/CI) — already checker-able today or should be:**
- front-matter + `disable-model-invocation` (existing checker); status vocabulary (existing
  `status_vocab_check`, extended for role-mixing per I4); 12-field interface completeness +
  no-placeholder (existing `interface_check`); flow-state semantics, honest-BLOCKED
  (existing `flow_state_check`); migration-map invariants (may_move/delete/overwrite=false,
  no target==source, no duplicate primary — existing CCM checkers); rewrite provenance
  (sha256 source unchanged, candidate≠source, no fact-upgrade — existing TDR checker);
  maintenance proposals (approved:false, no auto-publish — existing LDM checker); corpus
  non-mutation (existing, verified shadow run, registry:336).
- **New** mechanical: `duplicate-fact-lint` (I2), `canonical-impact-lint` (renamed from
  `canonical-freshness-lint`, R2) + dead-pointer banner check (I6), `supersession-lint` (I5), `archive-lint` (I11/I12), `release-version-
  lint` (D1), `dependency-graph-lint` (I10), `state-consistency-lint` in smoke (I7),
  `change-scope` report (I8), E-level field checks on claim-bearing artifacts (I3/I16).

**Skill (repeated non-trivial judgment or orchestration — charter §10 test):**
- quality grading within a profile (DQE); fact recovery (PSR); goal/scope elicitation with
  stop-when-answerable (GSWE); evidence synthesis with E-levels and channel separation (RES);
  decision-state policy incl. reversal judgment (UDM); information-architecture design (DIA);
  candidate-quality rewriting (TDR); migration planning (CCM); maintenance impact assessment
  (LDM); plus the new: simplification audit (12.2 — consumer classification), next
  discriminating experiment (12.5 — decision value), focused-verification selection (12.3 —
  "narrowest sufficient" judgment on a machine scope report).

**Convention / AGENTS.md (prose standing orders, DSH M1 pattern):** artifact placement;
executor contracts (the §16.6 seven fields); "update the owner in the same change" (12.8);
"no new persistent doc unless a decision requires one"; when to re-run PSR; what stays in
Git only (Q8).

**Schema (contract):** orthogonal decision fields (12.6, revised per R4 — see I4.1);
decision-note format (12.7, with mandatory Alternatives/Why/Revisit-condition +
rejection_basis for rejected notes, R5); experiment-result record; route record.

**Human approval boundary (keep exactly as designed):** write approval for move/delete/
overwrite (CCM mode boundary; smoke safety-negative); D-1/D-4-class decisions; rejected/
deferred decision notes; DQE terminal-gate promotion (A6, deferred).

### Q5. Which artifacts must be canonical?

**Answer (kept; the list, with one correction — see File 3 for the full owner table):**
SKILL.md files (per-skill contracts); `references/interfaces/` frozen handoff contracts —
**GIT-TRACKED since 098f2bb (D10 resolved 2026-09-10; 24 files now have history)**;
`references/templates/` (same); harness
checkers + rubric + hard-fail + `canonical-source-map.md` (the harness is the system's
testbed); `release-manifest.yaml` + `VERSION` (single release-state source, D1 fix);
`skills-registry.yaml` (roster only — narrative meta deleted, G1); corpus seeds + golden
cases + blind-run suites (test fixtures with mutation postconditions); the new persistent
stores: `docs/decision-register.md`, `docs/decision-notes/**`, `docs/incident-ledger.md`,
`docs/canonical-source-map.md`; `AGENTS.md` (new at repo root — currently absent, gap vs
DSH M1).

### Q6. Which artifacts should be transient?

**Answer (kept):** `flow-state` (per run, archived to `results/<run>/` at completion);
injection prompts and eval runs (records, not canonical — under `results/`);
candidate-doc-set (until applied or re-validated); goal-scope-note / literature-search-plan /
document-artifact-map (session planning outputs — §3.3 problem 6: they are frozen-interface
"artifacts" today but should carry `persistence: transient`); smoke clean rooms; blind-run
`.secret` identity mappings (comparator-only, never load-bearing — DSH M22 pattern);
no-skill baseline scratch outputs (exception: KEEP RAW THIS TIME — P8). DSH comparison: DSH
keeps session summaries mutable **only because its sole consumer is the tests**; the
analogue here (flow-state) already satisfies that — keep it mutable, archive it, never read
it as "current" (Q8).

### Q7. Which artifacts should automatically become stale, archived, or deleted?

**Answer (kept, made rule-explicit — the four missing definitions of I12):**
- **Stale (mechanical signal):** any canonical owner in a change's declared impact set that
  was not updated in that change ⇒ `canonical-impact-lint` flag (change-impact discharge,
  I6(c)(1)); any pointer to a VOID/SUPERSEDED doc ⇒ dead-pointer flag (D12/D4 class). A
  bare `last_verified` touch is NOT a staleness discharge.
- **Archived:** dated reports — superseded by the next accepted report on the same subject,
  then moved to `docs/plans/archived/` (or `reports/archive/`) at the next release boundary;
  VOID/SUPERSEDED plans — moved within one release (creation-roadmap is the live test case,
  2 commits old); completed flow-states → `results/<run>/`; candidate-doc-sets after apply or
  re-validation; superseded decision-register rows → collapse to pointer + note.
- **Deleted:** runlog narrative (REPLACED by git — G3); registry meta narrative (deleted,
  not archived — replaced by decision notes, G1); per-run injection prompts beyond
  `results/` (never promoted to living docs); rejected decision notes whose "prevents a
  tempting mistake" guardrail role has been mechanized (DSH rule: kept only as guardrail,
  else deleted as full triplet — history A.8).

### Q8. Which information should exist only in Git history?

**Answer (kept):** implementation chronology (the runlog's actual content — P9 showed the
append-only runlog is batch-logged retroactively and already missing its largest incident);
per-skill `last_verified` dates (git + file metadata is the record); the two-commit release
semantics (release-baseline `source_commit` 9dc7f18 vs packaging commit 2c5ca1d — git tells
this story, runlog.md:57 restates it); superseded plan bodies (the 8 archived per-sprint
directives are immutable records — their VOID status is a pointer, the bodies stay in
archive); adjudication raw reviewer outputs (frozen append-only round records, never
"current"); the full history of blind-run `raw-results.json` (corrections are new runs —
the existing `corrections: []` discipline, P7); commit-level rationale already in commit
messages (the 18-commit history is legible: rename b0e62c4, untrack a4d780f, archive
f404d72). Rule: **Git = the chronology owner; no document restates "what happened when" as
current state** (kills D16/D17-class duplication mechanically — `state-consistency-lint`).

### Q9. What is the minimum context a new agent needs to resume the project correctly?

**Answer (kept, made concrete — target ≤7 files, each ≤~500 lines):**
1. `README.md` (after the I6 repairs — current state: what this is + how to run + where
   status lives); 2. `KNOWN_LIMITATIONS.md` (honest boundary); 3. the active charter
   (operating contract); 4. `docs/plans/active/reconstruction/README.md` (status table —
   the live "what is next" pointer, the D5 fix); 5. `docs/decision-register.md` (active
   decisions + open rulings — NEW, single store); 6. root `AGENTS.md` (NEW — repo layout
   map + standing orders, DSH M1; today this repo has NO root AGENTS.md, a gap vs DSH whose
   layering landed day one); 7. the `SKILL.md` of whichever skill the agent is asked to use
   (each currently ≤~160 lines — the per-skill contract is self-sufficient by design).
Verification: a PSR re-run on this repo must reconstruct state within its ~2,000-line budget
(PSR SKILL.md:49-51) and agree with this set — the operational cold-start test (also the
longitudinal metric, File 5 §d). What must NOT be required: the 14-SKILL.md corpus, the 18
dated reports, the registry narrative meta, or `system-architecture.md` in full
(architecture doc stays for architecture questions; the resume set does not need it — DSH
tier: architecture.md is an ordered map, not a resume doc).

### Q10. Which current workflows are blocked because they were designed ahead of available capability?

**Answer (kept):** All four, honestly, via the HONEST-BLOCKED rule:
- **SWR** (`scientific-workspace-reconstruction`): tail blocked at
  `dev-test-experiment-workspace-architect` + 4 more atoms; its recovery prefix is
  duplicated across all three flows (classification S13 → SPLIT; the unbuildable tail is
  the SPLIT reason).
- **NRSD** (`numerical-research-software-design`): blocked at the 6 Batch-4 research atoms
  (NRSD SKILL.md:40-60 call chain); the evidence front is real and valuable (S14 KEEP).
- **DQE terminal gate**: blocked on the Phase-E 3-arm matrix (deferred by its own canary) +
  ADR-DQE-002 + HF-REPRO definition (registry:26; A6 DEFERRED).
- **Apply-mode** for CCM/TDR/LDM: the 3 Batch-5 executors are proposal/candidate-only,
  write-approval boundary intact; A1 (apply executor) missing.
- **L0 router** (A4): not built; conflict-matrix covers routing at doc level.
Root cause identified by phase0: skeleton-first cadence — flows written before their
executors, then going stale exactly where builtness was claimed (D14 live; D3 resolved by
4e839b2). Target rule (I6 + charter §16.8, revised per R2): a flow's SKILL.md may claim an
executor "built" only if the executor exists in the roster and the claim matches the
registry graph (builtness-claim ↔ roster); the stale-claim class becomes checker-visible
via `dependency-graph-lint` (R7), with `canonical-impact-lint` covering the same-change
discharge of any doc that names executor state.

### Q11. Which current status models conflate orthogonal dimensions?

**Answer (kept — five instances, each mapped to a fix):**
1. UDM's 10-value claim-status (epistemic ⊕ process in one field — §3.3 problem 5) → §12.6
   orthogonal fields, REVISED per R4 and TESTED on 13 real entries (I4.1 — the charter
   §12.6 "no exact-schema adoption without that test" instruction is satisfied; the charter
   candidate's `kind` split is the one material deviation, with per-entry justification).
2. Registry `status:` key, 3 vocabularies + "SUPERSEDED" out-of-vocabulary (ownership 1.13)
   → `VOCAB.yaml` single source + role-mixing rule in `status_vocab_check`.
3. `flow_status` COMPLETE ⊕ approval-to-continue (defensible now ONLY because
   manifest:71-73 pins the completion semantics) → split into `flow_status` + `gate_state`
   when apply-mode lands; do not split now (YAGNI — the pinned semantics already discharge
   §8.4 for the Alpha scope).
4. Artifact persistence/locus — absent entirely (problem 6: session planning outputs frozen
   as "interface artifacts") → `persistence: canonical|transient|record` field on the
   12-field interface.
5. Identity model: OQ-* / D-* ID namespaces collide across contexts (D8/D9: OQ-1 = "issue
   tracker (OPEN)" in architecture §13, "reproducibility (RESOLVED)" in ADR-DQE-001, plus
   the register's own OQ-1/OQ-2) → global IDs owned by the decision register; local IDs
   namespaced `<owner>-<n>`.

### Q12. Which DSH mechanisms were later simplified or removed, and what warning does that provide?

**Answer (kept — the warning register, each item with a named exposure of the project):**
- **knip** (removed after its exception inventory grew): a detector that needs per-skill
  carve-outs is already the debt (history B.2.1). Exposure: per-skill eval carve-outs in the
  registry + DQE per-profile exceptions; any new checker shipping with an exception list is
  a Phase-4 deletion candidate.
- **TUI package** (removed 2026-08-04, zero deployed consumers): a surface with no consumer
  is product-sized dead weight (B.1). Exposure: the L3 research-stack overlap —
  wos-research/scansci-pdf/paper-fetch-skill all cover the retrieval lane (conflict-matrix
  §41-43, §50) and deep-research is listed installed but absent (D11).
- **check:pre-push aggregate** (removed 2026-07-22, after the fast/local vs exhaustive/CI
  split): do not re-aggregate local and CI evidence (A.1). Exposure: `run_checks.py` runs
  everything in one invocation — the tier split is right; add no "run-all-plus" convenience.
- **INDEX.md** (deleted — central generated inventories are merge hotspots): do NOT add a
  generated skill-index doc (B.5). Exposure: the registry already plays that role; keep it
  the ONLY roster (G1) and let `git ls-files .agents/skills` be the truth check.
- **Mutable session summaries** (kept mutable because the only consumer is tests): keep
  flow-state mutable + archived, never "current" (Q6/Q8).
- **SQLite second store** (removed; single authoritative store): a second source of truth
  multiplies every durability obligation (B.5). Exposure: the registry as second store for
  what SKILL.md + flow-state + git already say (D2/D3) — roster-only refactor (G1).
- **Shared base-config overlays** (removed when two N%-identical trees existed → base +
  patches): the three L1 flows' structurally-identical skeleton sections are the same
  pattern (B.5; classification S13 "recovery prefix duplicated across all three flows") →
  extract the shared recovery prefix once (the SPLIT target).
- **`dsh-doc-standards` consolidation** (three skills → one + a doc standard): skill
  consolidation is a first-class simplification operation (A.11/B.7). Exposure: the
  WFI/PSR "candidate canonical source" co-ownership (S5 REFINE) may resolve by
  consolidation, not by boundary prose.
- **Frozen side-branch `legacy-agent-team`** (kept out of the first-parent tree, tree
  unchanged): a template for retiring a prototype while keeping archaeology (B.6) → the
  pattern for SWR's unbuildable tail if the split defers it.
- **Packed-fixture migration** (documented transition outlived its window; removed once no
  consumer): give every transitional artifact a mechanical end condition (B.6). Exposure:
  `dataset_version: 1` case files never re-baselined after Sprint 6B (D4) — transitions
  without closure triggers are the D4 class.
- **8,130 → 984-word condense in one commit** (A.7): current-state docs condense on
  supersession, not accumulate; budgets are the enforcement (M12).
One-line register: *every mechanism that needs an exception inventory to tolerate reality,
a second copy to be useful, or a central index to be findable is a deletion candidate —
transfer the principle, not the DSH instance.*

### Q13. If half of the proposed new mechanisms were deleted, which capabilities would actually be lost?

**Answer (kept — the portfolio's cheap half vs expensive half, made explicit):**
**Cheap half (deletable before the slice without losing a user-visible capability):**
standalone L0 router skill (A4 — routing table in AGENTS.md + `dependency-graph-lint`
suffices until flow count forces it); 12.4 route manager as a standalone skill (route state
folds into the decision register's `object_type: route` (R4) + a route table file (a GENERATED view of the register entries — non-authoritative, final patch P7) — revisit at Phase 3);
the DQE Phase-E 3-arm matrix as a pre-slice mechanism (already DEFERRED by its own canary —
A6); 12.7 as a separate doc type apart from an ADR-style directory (fold durable decision
notes into `docs/decision-notes/` with ADR-DQE-001 migrated in — one format, not two);
installed-skills record as a separate file (A5 — fold into a `preflight.py` extension that
records the check result).
**Expensive half (deleting it loses a real capability — Phase 2 must keep it):**
- `register_check` merged into the runner (H2) + E-level field checks — without them I3
  regresses: "VERIFIED at E2" becomes silent again (the P4 disease).
- `duplicate-fact-lint` + `canonical-impact-lint` (R2 rename) — without them I2/I6 regress:
  P5's disease (live instances per post-audit-reconciliation §1) recurs unmeasured; the
  slice's own success becomes unprovable.
- A1 apply-mode executor — without it the closed loop stays dry-run forever (Q14 fails;
  charter mission #2 unexercised end-to-end).
- §12.3 focused-verification — without it "smallest sufficient evidence" stays prose (P1/P3
  recur; the 63M-token class is unguarded).
- §12.2 simplification audit — without it the ratchet's remove side has no owner (I11 stays
  one-way; the VOID-roadmap class persists).
Deletion-test result: the proposal's defensible minimum is **5 new mechanisms** (H2 merge +
the two lints + A1 + 12.3); the full proposal is 11 (adding 12.5, 12.7, archive-lint,
supersession-lint, the persistent stores). Phase 4 re-runs this exact half-deletion test
against what actually shipped.

### Q14. Can a common change be completed without generating unnecessary new permanent documents?

**Answer (kept — currently NO for flow runs, YES for plain edits; target defined):**
Today: a plain code/doc edit needs no new permanent doc (commit only) — OK. A flow run
generates up to 10 persistent artifacts per run (§3.3 problem 4: flow-state + goal-scope +
search-plan + evidence-map + register + migration-map + rewrite-provenance + maintenance-
proposals + decisions + reports) — and 8 of the 10 are session-scoped by nature (Q6).
Target: a common change = the change itself + (only if non-trivial) ONE decision note +
same-change update of the affected canonical owners (12.8); flow runs keep `flow-state` +
the run's 2–3 core artifacts, with everything else transient (Q6) or an append-only record
under `results/` (Q8). Mechanisms: charter §16.8 (executors may not rewrite planning/
decision artifacts to appear compliant — keeps the document count honest); the artifact
budget is measured, not just declared — "number of artifacts generated per change" is a
tracked longitudinal metric (File 5 §d), so "unnecessary new permanent documents" becomes a
measured regression, not a review opinion.

### Q15. Can a research route be paused/rejected/revived without falsifying history?

**Answer (kept — decision level YES today, route level NO today; target YES by design):**
Decision level: YES today — UDM's supersession fields hold both lines and the runlog shows a
real LU→CG reversal with lineage (parent Q13; UDM SKILL.md:51-53). Route level: NO today —
there is no route object at all (File 3: "current roadmap/active routes" has no canonical
route store; NRSD's "routes" are call-chain steps, not managed alternatives). Target: §12.4
implemented as the LIGHTWEIGHT form — a route record is a decision-register entry
(`object_type: route`, R4 revised schema) = the canonical mutable route state, + a single
route table (goal / status / dependencies / active decisions / open questions / evidence /
next discriminator / next action, per charter §12.4's own field list) that is a GENERATED
/ rendered view of the register entries — explicitly NOT a second source of truth (final
patch P7) — and NOT a Project→Topic→Workstream→Node hierarchy (charter §12.4: avoid it
"unless evidence proves it is necessary"; no such evidence exists yet). Rejection = a
`rejected/` decision note with reason + revisit condition (DSH rejected-triplet pattern,
history A.8); revival = a NEW note cross-linking the rejected one (supersession lineage, I5)
— history is appended to, never rewritten; `supersession-lint` makes the lineage mechanical.
This is also the DSH §7 caution applied: DSH PR stacks solve IMPLEMENTATION dependency;
research alternatives are not PR stacks (charter §7 example 1) — route state is a register
entry, not a branch.

### Q16. Can the system distinguish "strong literature support" from "verified in this project"?

**Answer (kept — PARTIAL today, YES under target; the artifact-side restatement of the
parent's Q16, kept as the operational check of the same rule):**
Today: the SEMANTICS exist — E0–E5 with the E3 "verified" floor (UDM SKILL.md:22-29), RES's
literature/project/inference channel separation (RES SKILL.md:20-38), DQE's FACTUAL_VALIDITY
HF check — and the no-skill baseline's silent fact-upgrade (P8) proves the distinction is
load-bearing. But the MECHANICS are missing: a document citing literature reads as "verified"
to every checker (E-levels live only in UDM's register and RES's synthesis output; the
12-field interfaces carry no evidence field); `register_check` is standalone and not in the
runner (H2); and the ADR's un-annotated falsified claim (D12) shows prose-level evidence
claims can rot silently. Target: `evidence_level` + `evidence_state` become REQUIRED fields
on every claim-bearing artifact (schema, §12.6), `register_check` runs HARD for register
files (H2 merge), `duplicate-fact-lint` reports any "verified" claim lacking an E≥3 link,
and DQE's FACTUAL_VALIDITY keeps the model-level audit for claims the checkers cannot see.
Verdict: the distinction is then checker-visible in the register and schema-visible
everywhere claims are made; the residual judgment (assigning the level) stays UDM's.

### Q17. Can the system recover the current state after 20–50 changes without reading the entire repository?

**Answer (kept — verdict sharpened from the parent's "YES at the cost of ~15 docs"):**
Today: **DEGRADED** — after only 18 commits the audit already found 19 verified duplicate
families and 7 live stale instances (ownership-map §3; P5), the VOID roadmap is still
referenced (D12), and the README's "Next" contradicts its own banner (D5). The parent's
preliminary "YES for a reader who follows the governance chain, at the cost of ~15 docs" is
correct as to today's path but insufficient as a target, because the chain itself is
drifting (two of its 15 links are stale now). Target: **YES by construction** —
(1) File 3 bounds the active corpus (every information type has a lifecycle + archive rule;
append-only records are retrievable, not load-bearing); (2) the lints make drift
DETECTABLE before a human reads it (duplicate-fact-lint, canonical-impact-lint,
dead-pointer); (3) cold-start recovery is the Q9 set (≤7 files) and is MEASURED every
simulation iteration as "context required for cold-start resume" (File 5 §d). Operational
definition of "understandable after many changes" (File 5 §d): a fresh no-context agent
answers {what exists / what is current / what is decided / what is next / what is blocked}
from the Q9 set + `git log`, scoring ≥4/5 correct within a ≤3,000-line read budget, while
`duplicate-fact-lint` reports ≤2 active duplications (Phase-3+ — the checker rides with
its build phase, R11; not a Phase-2 gate). If that test passes after 25
simulated changes, §20 "Long-term maintainability" is satisfied by measurement, not
demonstration.

---

## 3. S1 crosswalk resolution (sweep complete)

S1's `dsh-transferability-crosswalk.md` (phase1/, 32 mechanisms labeled) arrived after
the first drafts of this file; every former PENDING-S1 marker has been swept to the
crosswalk's §7 label: I5 (M18 → TRANSFERABLE AFTER GENERALIZATION), I10 (M6 →
TRANSFERABLE AFTER GENERALIZATION), Q3 (per-mechanism labels inline + the M21 move to
DSH-SPECIFIC, per crosswalk §1). Mechanisms cited in S2's files that are NOT in the
crosswalk's M1–M32 register (e.g., `dsh-code-review` in File 2 §2.7) are marked
**UNKNOWN-CROSSWALK** rather than guessed. All other DSH claims cite the two
intermediates directly (mechanism ids M1–M32 from `dsh-current-state-findings.md`;
Part A/B + commits from `dsh-history-findings.md`). S2's other four files carry the same
resolution (swept in the same pass).
