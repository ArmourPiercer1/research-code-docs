# Phase-0 — Existing-Skill Classification (research-code-docs)

> generated_by: phase-0-audit-subagent
> scope: exactly one label per skill (14), per control flow (3, counted within the 14), per harness component, per governance component; ADD entries for missing capabilities; §3.3 structural-problem confirmation — per charter §3.2/§3.3 (docs/plans/active/research_software_agent_workflow_reconstruction_charter.md)
> method: same evidence base as phase0/current-system-map.md (all 14 SKILL.md, registry, conflict-matrix, QC plan, architecture, roadmap, audit, ADR, runlog, manifest, release/smoke docs, harness checkers/injection scripts, corpus policy/adjudication protocol, case YAMLs measured, git log/show, disk checks); file:line citations; UNKNOWN where not verifiable
> date: 2026-09-09
> status: DRAFT-for-review
> labels: KEEP / REFINE / MERGE / SPLIT / REPLACE / ADD / REMOVE (one per item; evidence inline)

Companion file: `current-system-map.md` (factual map + discrepancy log D1–D14 referenced below).

## 1. Label summary

| # | Item | Kind | Label | One-line rationale |
|---|---|---|---|---|
| S1 | documentation-quality-evaluator | L2 evaluator | **REFINE** | sound advisory instrument, but ~860-line grader envelope, contract duplicated in injection script, terminal gate deferred |
| S2 | project-state-reconstructor | L2 atomic | **KEEP** | clean single-purpose fact recovery; no known defect beyond stale registry note |
| S3 | goal-scope-and-workflow-elicitor | L2 atomic | **KEEP** | works as designed; boundary with grilling explicit |
| S4 | uncertainty-and-decision-manager | L2 atomic | **KEEP** | core epistemic discipline; register_check standalone is a runner-integration gap, not a skill defect |
| S5 | workspace-forensics-and-inventory | L2 atomic | **REFINE** | functional, but boundary/co-ownership with PSR on "candidate canonical source" is loose |
| S6 | document-information-architect | L2 atomic | **KEEP** | strong evidence (shadow run beat baseline); canonical-home tri-way ownership noted in §3.3 |
| S7 | research-question-and-literature-planner | L2 atomic | **KEEP** | thin adapter as intended; OQ-4 merge question answered by its own Track-B evidence ("keep separate") |
| S8 | research-evidence-synthesizer | L2 atomic | **KEEP** | thin adapter as intended; E-level duplication with UDM is by design (same vocab) |
| S9 | content-canonicalization-and-migration | L2 atomic | **KEEP** | dry-run planner complete + checked; its missing capability is an ADD, not a defect |
| S10 | technical-document-rewriter | L2 atomic | **KEEP** | candidate-only rewriter complete + checked |
| S11 | living-design-maintainer | L2 atomic | **REFINE** | functional, but its artifacts are proposal-parallel maintenance outputs that duplicate the same-change update path |
| S12 | documentation-refactor | L1 control | **REFINE** | first closed loop is real, but its SKILL.md + one conflict case are stale vs Sprint 6B (same-change updates not done) |
| S13 | scientific-workspace-reconstruction | L1 control | **SPLIT** | unbuildable tail + recovery prefix duplicated across all three flows; cannot complete its own scope |
| S14 | numerical-research-software-design | L1 control | **KEEP** | evidence-front is real and valuable; blocked tail is a known ADD, flow is honest |
| H1 | run_checks.py | harness runner | **KEEP** | tier model is sound; integration gap only |
| H2 | register_check.py | harness checker | **MERGE** | not registered in run_checks.py (orphan); merge into the runner's tier lists |
| H3 | make_grading_injection.py | harness builder | **REFINE** | EVALUATOR_CONTRACT duplicates DQE gate-derivation/profile logic already in SKILL.md |
| H4 | rubric.md / hard-fail.md / canonical-source-map.md | harness refs | **KEEP** | stable references the evaluator and checkers both consume |
| H5 | other 13 checkers (interface/flow_state/3× Batch-5/markdown/placeholders/5 signal/frontmatter/status_vocab) | harness checkers | **KEEP** | each maps to a documented HF or handoff rule; no orphan behavior found |
| H6 | corpus + blind-runs + adjudication protocol + snapshots | harness corpus | **KEEP** | policy is strong and consistently applied (32 cases, 11 runs, quarantine intact) |
| G1 | skills-registry.yaml | governance | **REFINE** | useful roster, but meta block duplicates current-state in 5+ other docs and has stale notes (D6/D7/D11) |
| G2 | creation-roadmap.md | governance | **REMOVE** (from active governance) | already VOID-badged 2026-09-09; still tracked and still referenced by DQE SKILL.md:9 — archive |
| G3 | runlog.md | governance | **REPLACE** | hand-narrated chronology duplicates git log + 18 dated reports; keep as thin pointer or fold into reports/ |
| G4 | system-architecture.md | governance | **REFINE** | accurate architecture doc but status line stale ("DECIDED for Phase 1", no charter pointer) |
| G5 | conflict-matrix.md / quality-control-plan.md / current-skills-audit.md / ADR-DQE-001 | governance | **KEEP** | each is the single home of a distinct concern; no duplication found |
| G6 | release-manifest.yaml + preflight/install/smoke | release | **KEEP** | internally consistent release engineering; one bookkeeping mismatch (D5) |

## 2. Per-item evidence

### S1 documentation-quality-evaluator — **REFINE**
- Evidence for: the only evaluator in the system; five documented defect-fix cycles (v0.3 false-pass fix, D-01, D-16, D-17 — reports/dqe-v0.3-upgrade-2026-07-30.md, dqe-blind-matrix-investigation-2026-07-31.md, dqe-v0.4.1-diagnostic-close.md, dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md) show a working improvement loop; 23+5+10+3+2 cases + 32-case blind corpus + 11 recorded runs (measured) — the most-evaluated skill in the repo.
- Evidence against (REFINE not KEEP): (1) the grader's full working envelope is ~860 lines (SKILL.md 241 + hard-fail.md 197 + rubric.md 148 + canonical-source-map.md 43 + EVALUATOR_CONTRACT ~56 lines in make_grading_injection.py:41-96) injected as ONE context — charter §0 cognitive-load principle; (2) the two-axis verdict + profile-admission + 3-rule gate contract is maintained in TWO places (SKILL.md:60-83 vs make_grading_injection.py:41-96) with no single-source extraction; (3) the terminal-gate promotion (Phase-E admission matrix, reproducibility contract, ADR-DQE-002, HF-REPRO) is DEFERRED and not built (registry:26, 56) — the skill's biggest consumer-facing capability is a stub.

### S2 project-state-reconstructor — **KEEP**
- Single responsibility (fact recovery), explicit non-trigger set (SKILL.md:36-41), 23+5+2+3 cases (measured), e2e evidence of no-fabrication discipline (runlog.md:23, registry:365 E2-cap note). Only defect is the registry's stale "(PLANNED; self-inventories until built)" upstream note (D7) — a registry issue, not a skill one.

### S3 goal-scope-and-workflow-elicitor — **KEEP**
- Works as specified: facts-looked-up-not-asked (SKILL.md:22-29), primary should-not "simple well-specified task" present in trigger set (23 cases); boundary vs grilling explicit (conflict-matrix G5; registry:120); 23+5+2+3 cases (measured). No defect found.

### S4 uncertainty-and-decision-manager — **KEEP**
- Owns the system's core epistemic discipline (10-state vocab + E0–E5 + supersession audit trail; SKILL.md:22-29); ADR-DQE-001's lifecycle/claim-status split exists to protect this artifact (ADR:62-70); 23+5+2+3 cases (measured). The one gap — register_check.py not in run_checks.py (H2, run_checks.py:46-58) — is a runner-integration item, classified on the checker, not the skill.

### S5 workspace-forensics-and-inventory — **REFINE**
- Evidence for: clean read-only inventory, boundary sentence explicit (WFI SKILL.md:23-26 "never asserts that anything runs — that verified judgement belongs to project-state-reconstructor"), shadow run beat no-skill baseline (registry:198-200).
- Evidence for REFINE: "CANDIDATE canonical source" proposals (WFI SKILL.md:31-40) overlap DIA's canonical-home assignment (DIA SKILL.md:26-42) AND the harness table canonical-source-map.md (10 rows) — three places propose/assign the same info type (charter §3.3 "multiple skills claiming the same info type"); the WFI↔PSR "what is here vs what is real" split is a judgment call a single merged audit skill could own more simply. Not broken — boundary needs tightening, hence REFINE not REMOVE/MERGE.

### S6 document-information-architect — **KEEP**
- Strongest measured evidence among design skills: shadow run on the eoopt hybrid roadmap — 11 roles, one canonical home per info-type, complete split plan, provisional(needs-PSR) flags, open decisions, vs baseline "drifted into rewrite/execute + silent decisions" (registry:229-231); 6+2+1 cases (measured). The tri-way canonical-home ownership is a system-level issue recorded in §3.3 (and partly assigned to S5).

### S7 research-question-and-literature-planner — **KEEP**
- Exactly the thin adapter its environment requires (A1 adaptation; system-architecture.md A1): plans + routes, never retrieves (SKILL.md:20-38); do-not-trigger names all five L3 skills (conflict-matrix §50); shadow run: baseline OVERREACHED — "clearest value demonstration of the batch" (registry:258). OQ-4 (merge with RES?) is answered by the same batch's evidence: "evidence says keep separate" (registry:28). 6+2+1 cases (measured).

### S8 research-evidence-synthesizer — **KEEP**
- Same adapter discipline (never retrieves; E2 cap on analogy; channels separated; SKILL.md:20-43); boundary vs evidence-extraction and literature-synthesis explicitly written (SKILL.md:26-31, 54-60); shadow evidence-map held D.8 no-fact-upgrade (registry:288); 6+2+1 cases (measured).

### S9 content-canonicalization-and-migration — **KEEP**
- Complete dry-run planner: 5-part output, single-primary-disposition rule, supersession-not-delete, rollback plan (SKILL.md:22-42); checker enforces all invariants (migration_map_check; self-test planted defects all caught, registry:447-451); shadow run on real Track-A corpus (11 dispositions, 10 decision-gated; corpus git-verified untouched). The missing apply-mode execution is ADD A1 below — a new capability, not a defect in this skill. 6+2 cases (measured).

### S10 technical-document-rewriter — **KEEP**
- Candidate-only rewriter with sha256 source guard, provenance mapping, unresolved-content carry (SKILL.md:22-43); checker self-test caught may_overwrite/hash-tamper/candidate==source/empty-provenance/COMPLETE-while-unresolved (registry:482); shadow on Track-A produced PARTIAL completion with D-1/D-4 left OPEN — exactly the intended honesty. 6+2 cases (measured).

### S11 living-design-maintainer — **REFINE**
- Evidence for: proposal-only maintenance impact analysis with boundary checking (stable-design/dynamic-state/experiment-fact/session-context; SKILL.md:22-41); checker self-test caught auto_publish/volatile-into-stable/unapproved-mark-canonical/dual-home (registry:517).
- Evidence for REFINE: its outputs (proposed canonical updates + stale-reference list) are PARALLEL artifacts to the "update the canonical doc in the same change" path — the maintenance impact report and the actual edit both have to be produced for any real change, so the skill's value is bounded by how often parallel proposals survive review; the artifact-role is also the one most likely to be absorbed into the doc being updated (charter §3.3 separate-maintenance-artifacts). Functional; shape to be re-decided in Phase 1.

### S12 documentation-refactor — **REFINE**
- Evidence for: FIRST REAL CLOSED LOOP in the system — Sprint 6B e2e forensics→…→maintainer→flow-state COMPLETE, corpus byte-for-byte untouched, all checkers green (registry:331-333; reports/sprint6-routing-and-first-closed-loop-2026-08-06.md); 27/27 Sprint-6A routing cases across the 3-flow cluster.
- Evidence for REFINE: SKILL.md:47 still says "v0 SKELETON STOPS HERE (executor tail … Batch 5, NOT BUILT)" with last_verified 2026-08-05 — one day STALE against Sprint 6B (D3); conflict case docref-conf-03 still expects BLOCKED-at-Batch-5 (D4); the same-change update discipline the system itself preaches (quality-control-plan §6 regression policy) was not applied to its own docs. The orchestration logic itself (route/persist/verify/honest-stop) is sound.

### S13 scientific-workspace-reconstruction — **SPLIT**
- Evidence: it cannot complete its own scope — blocked at dev-test-experiment-workspace-architect (SKILL.md:25-27, 93-98; KNOWN_LIMITATIONS.md:34-38) with FOUR further atoms missing after that; its SKILL.md even lists living-design-maintainer as "BLOCKED: not built" (SKILL.md:49) although LDM was built 2026-08-06 (D14). Structurally it is (a) a 3-stage recovery prefix — WFI→PSR→GSWE — DUPLICATED VERBATIM in purpose, duties, write-scope, and honest-stop semantics with S12/S14 (their "Skeleton duties / Must NOT / v0 expected result" sections are structurally identical), and (b) a code-workspace tail of 5 unbuilt atoms. The prefix is a shared capability that belongs to one place; the tail is a separate capability. SPLIT = extract the shared recovery prefix into one reusable unit + keep the workspace-tail as its own (still-blocked) flow. Its e2e evidence (prefix run on the harness workspace, BLOCKED correctly, registry:363) supports that the prefix part works.

### S14 numerical-research-software-design — **KEEP**
- Evidence: its evidence-front is the only place in the system where the research atoms (RQLP→L3→RES→UDM) are composed into a working chain, and the e2e consults the REAL Batch-2.5 Track-B evidence base before stopping honestly at the missing Batch-4 core (registry:395; flow-state-manifold-transfer.md); 27/27 routing cases (Sprint 6A); DENY co-run enforced (conflict-matrix §1). The 6 missing Batch-4 atoms are ADD A2, not a design defect — the flow's contract (routes, never retrieves, E2 cap, honest BLOCKED) is exactly what charter §0 wants for an unbuildable-tail flow.

### H1 run_checks.py — **KEEP**
- The HARD/ADVISORY/SIGNAL tier model is sound and consistently documented (run_checks.py:5-24); it is the single deterministic gate for every skill (quality-control-plan §1.1, D.9). Only gap: register_check.py not registered (H2).

### H2 register_check.py — **MERGE** (into run_checks.py's tier system)
- Evidence: a standalone checker that validates the decision-register (status/evidence legality, checkable sources, disposition, VERIFIED-at-E≤2 flag) but is NOT in run_checks.py's tier lists (run_checks.py:46-58 — grep: no import); UDM invokes it by hand (SKILL.md:111-114); release-manifest lists it as `signal` (D5). A checker that must be remembered to run is not mechanically enforced (charter §0: mechanical enforcement over prose) — merge into the runner (as HARD for `decision-register.md` files, mirroring how interface_check/flow_state_check are opt-in on artifact markers).

### H3 make_grading_injection.py — **REFINE**
- Evidence: the EVALUATOR_CONTRACT block (lines 41-96) restates the profile-admission rule, the 3-rule GATE_DECISION derivation, the severity mapping, and the full verdict-block schema — all ALREADY specified in SKILL.md:60-83 and ADR-DQE-001. Two maintenance sites for one contract (D3-class risk, same as S1 point 2). REFINE = single-source the contract (extract once, inject verbatim from SKILL.md/ADR) rather than maintain the duplication.

### H4 rubric.md / hard-fail.md / canonical-source-map.md — **KEEP**
- hard-fail.md (HF-1..HF-15) is the single home of hard gates (quality-control-plan §1.1 cites it as authoritative); rubric.md's non-compensatory rule + dimension weights are stable since v0.3; canonical-source-map.md is consumed by BOTH the DQE grader (EVALUATOR_CONTRACT) and the LDM checker — a genuinely shared reference, not a duplication.

### H5 other 13 checkers — **KEEP**
- interface_check.py enforces the frozen 12-field handoff + 11 artifact types + KNOWN_NON_FROZEN exclusion (interface_check.py:1-30); flow_state_check.py enforces the HONEST-BLOCKED rule (flow_state_check.py:1-12); the 3 Batch-5 checkers each enforce their skill's documented invariants (all self-tests caught planted defects — registry:447/482/517); markdown_links/placeholders/frontmatter/status_vocab/5 signal checkers map 1:1 to HF-8/9/3/10/13/14a/14b/15. No checker found to be dead, redundant, or contradicting its skill's SKILL.md.

### H6 corpus + blind-runs + adjudication + snapshots — **KEEP**
- Corpus policy (docs/testing/corpus-policy.md) has 9 concrete mechanisms, all verifiably in effect: 32 manifests with quarantine intact (measured), seed-register.yaml with URL/SHA/SHA-256/SPDX per seed, UPSTREAM-COMMITS.tsv pinning (tests/corpus/upstream/, git-ignored clone per policy §3), blind UUID suites with comparator-only .secret/mapping.tsv (build_blind_suite.py:3-13), two-reviewer adjudication with consensus-only promotion (adjudication-protocol.md:1-59), 11 recorded runs including the Phase-E canary (blind-runs/). This is the strongest subsystem in the repo relative to its size.

### G1 skills-registry.yaml — **REFINE**
- Evidence for: the only machine-readable roster; per-skill write_scope/context_budget/conflicts/evals fields are load-bearing for preflight (preflight.py reads it) and for the conflict-matrix.
- Evidence for REFINE: the meta block (lines 17-31 + per-batch narrative notes) duplicates current-state that ALSO lives in the skill-development README, system-architecture §13, creation-roadmap, runlog, conflict-matrix header, and CHANGELOG (charter §3.3 "current state duplicated across documents"); and it carries stale entries (D6 isolation claim vs user-level install on disk; D7 WFI "PLANNED"; D11 deep-research listed as installed) — i.e., the single-source candidate currently fails as one.

### G2 creation-roadmap.md — **REMOVE** (from active governance; archive)
- Evidence: already marked "⛔ VOID / SUPERSEDED (2026-09-09)" by its own header (creation-roadmap.md:3-7); the charter (docs/plans/active/…charter.md) supersedes it; commit 62ada30 voided it in-repo; yet it is still TRACKED in git and still referenced by DQE SKILL.md:9 (D12). Keep the file as history under docs/plans/archived/ or similar; remove it from the active docs tree and from the DQE pointer.

### G3 runlog.md — **REPLACE**
- Evidence: a ~55-line hand-narrated chronology (reports/runlog.md:1-57) whose content is almost entirely "commit X did Y" + pointers to the 18 dated reports in the same directory; git log/show already records the commit history (e.g. b0e62c4, 2c5ca1d) and the reports record the substance. It is a third copy of the same chronology (charter §3.3 "git state duplicated in hand-written docs"). REPLACE = keep at most a thin index of report files + the few non-commit events (e.g. user-level install, D6) that git cannot express; stop appending narrative.

### G4 system-architecture.md — **REFINE**
- Evidence: accurate, decision-grade architecture (A1/A2/A3 adaptations, layering, vocab, §13 OQ-1..OQ-5); but status line still "architecture v0.1, DECIDED for Phase 1" (line ~11, last_verified 2026-08-05) with no pointer to the now-active charter, and it post-dates nothing — it predates the charter that supersedes the roadmap (D12 partial).

### G5 conflict-matrix / quality-control-plan / current-skills-audit / ADR-DQE-001 — **KEEP**
- conflict-matrix.md: single home of co-run rules + G1–G5 governance gates; G2's "DENY without resolution = release blocker" is an actual mechanism (line 15). quality-control-plan.md: single home of the two-tier gate + regression policy + dataset governance. current-skills-audit.md: the Phase-A evidence the environment adaptations rest on. ADR-DQE-001: the contract all DQE behavior hangs on (ACCEPTED 2026-08-02). No duplication found between them.

### G6 release-manifest + preflight/install/smoke — **KEEP**
- Release engineering is internally consistent: manifest fixes source_commit 9dc7f18 (release-manifest:32); preflight is read-only exit-0/1/2 and checks the exact invariants (preflight.py:1-33); smoke_test.py is a genuine clean-room with planted state-contradiction + safety-negative (smoke_test.py:1-64); smoke-report-2026-08-06.md records an actual PASS run with 0 tracked files modified. One bookkeeping mismatch (D5: signal-tier list vs run_checks.py) — fix, don't restructure.

## 3. ADD — capabilities that do not exist yet

- **A1 — apply-mode migration executor (explicit write-approval).** Missing capability: executing an approved migration-map (move/split/link/annotate) under an explicit per-run write approval, with HF-4 no-overwrite diff guard + HF-5 write-scope + rollback execution. Evidence of absence: CCM is dry-run only (SKILL.md:22-29, "execution is a separate, un-granted write-approval"), KNOWN_LIMITATIONS.md:6-9 ("apply-mode execution not implemented in Alpha"), TDR/LDM both stop at candidate/proposal (S9/S10/S11 evidence), release-manifest completion_semantics ("COMPLETE = dry-run+candidate scope, NOT migration executed"). What would implement it: a new L2 skill (or CCM apply sub-mode) that consumes an approved migration-map + rewrite-provenance-report, performs guarded writes, re-verifies sha256 of untouched sources, and records source_files_changed in flow-state.
- **A2 — Batch-4 numerical-design core (six atoms).** research-software-problem-framer, scientific-software-architect, algorithm-technical-spec-author, scientific-prototype-experiment, scientific-validation-and-benchmark-planner, research-software-roadmap-author. Evidence of absence: NRSD SKILL.md:40-60 lists all six as "NOT BUILT (Batch 4)"; registry Batch-4 rows (planned, not built); KNOWN_LIMITATIONS.md:34-38; NRSD e2e stops at problem-framer (registry:395). Unblocks S14's design scope.
- **A3 — Batch-5 workspace-tail atoms (four).** dev-test-experiment-workspace-architect, experiment-provenance-and-reproducibility, workspace-migration-planner, scientific-validation-and-benchmark-planner. Evidence of absence: SWR SKILL.md:38-50 ("all NOT BUILT"); registry rows planned; KNOWN_LIMITATIONS.md:34-38; SWR e2e BLOCKED at the first (registry:363). Unblocks S13's tail (SPLIT candidate's second half).
- **A4 — L0 router (research-software-workflow-router).** The only UNBUILT layer in the whole system. Evidence of absence: registry L0 row (layer L0-router, planned; registry:~7-13 area, "planned router"); system-architecture layering lists L0 as not built; no .agents/skills/<router> exists on disk (14 skills measured, none is a router). What it would implement: the documented routing table (README.md:30-34; conflict-matrix §1) as one invocable entry point instead of three manual flow entries.
- **A5 — install/registration-state record.** Missing capability: a machine-checkable record of WHERE each skill is installed (workspace `.agents/skills` vs user-level `C:\Users\user\.claude\skills`), versioned with the repo. Evidence of absence: the isolation claim (registry:20) contradicts disk (all 14 installed user-level 2026-08-07 22:48, D6) with NO record anywhere (runlog/manifest/KNOWN_LIMITATIONS all silent); preflight.py checks the workspace tree only. What it would implement: a `installed-skills.yaml` (or preflight extension) listing each skill, its install location(s), copy-hash vs source, and install date — making "workspace-only" verifiable or falsifiable mechanically.
- **A6 — DQE promotion terminal gate (Phase-E package).** Missing capability: the 3-arm admission matrix (DQE v0.3.0 / v0.4.0-pre-d16 / v0.4.1-candidate as independent graders), the reproducibility contract (ADR-DQE-002, HF-REPRO, reproducibility checker, 12-slot canary), and the controlled+release-gate experiment-report profile. Evidence of absence: registry meta.phase_e DEFERRED (registry:26); the 3 frozen bundles + phase-e-2026-08-05 canary run are PRESERVED precisely for this (build_skill_snapshots.py:1-46; blind-runs/phase-e-2026-08-05); SKILL.md:29 scope guard. Deferred by decision, not forgotten — ADD keeps it explicit as a separate capability with a readiness gate, not a feature of S1.

## 4. Charter §3.3 — the 13 named structural problems: EXISTS / NOT PRESENT

(1) **Multiple skills claiming the same information type — EXISTS.** WFI proposes "candidate canonical source" (WFI SKILL.md:31-40), DIA assigns canonical homes (DIA SKILL.md:26-42), LDM enforces them (LDM SKILL.md:22-41), and the harness table canonical-source-map.md (10 rows) is the fourth place — four owners of one info type.

(2) **One skill with too many responsibilities — EXISTS.** DQE's grader envelope = SKILL.md 241 + hard-fail.md 197 + rubric.md 148 + canonical-source-map.md 43 + EVALUATOR_CONTRACT ~56 lines ≈ 860 lines of judgment contract injected per evaluation (S1 evidence); it is simultaneously policy (profile admission), taxonomy (HF-1..15), rubric, reader-test protocol, and verdict composer.

(3) **Control flows that cannot complete — EXISTS.** SWR blocked at 5 unbuilt atoms (SKILL.md:25-27, 38-50; KNOWN_LIMITATIONS.md:34-38); NRSD blocked at 6 unbuilt atoms (SKILL.md:28-30); release-manifest lists both as experimental with honest-BLOCKED expected (release-manifest:74-80).

(4) **Artifact proliferation — EXISTS.** One closed loop (documentation-refactor) produces ~10 distinct artifact types: inventory-report, project-state-report, goal-scope-note, decision-register, document-artifact-map, migration-map, candidate-doc-set, rewrite-provenance-report, maintenance-impact-report, flow-state (+ quality-report) — with 11 interface schemas + 12 templates under references/ (D10) for a system with 14 skills.

(5) **Status-vocabulary mixing — EXISTS.** The 10-value claim-status field (FACT VERIFIED DECIDED BASELINE HYPOTHESIS CANDIDATE OPEN DEFERRED REJECTED STALE) mixes epistemic states (FACT/HYPOTHESIS/CANDIDATE/STALE) with process states (DECIDED/OPEN/DEFERRED/REJECTED) in ONE field (registry:17-19; system-architecture §7); ADR-DQE-001 explicitly split ONLY document_lifecycle out of it, leaving the claim/process mix (ADR:62-70); three vocabularies (claim-status, document_lifecycle, flow_status) coexist with the cross-usage rules living in prose (SKILL.md files) rather than one checked contract (status_vocab_check validates legality, not role-mixing).

(6) **Canonical artifacts that are actually session-local — EXISTS.** flow-state (per-run, per-flow directory), goal-scope-note, literature-search-plan, and document-artifact-map are written as "artifacts" under the frozen-interface contract (references/interfaces/README.md — all 12-field, DECIDED) yet are session-local working outputs, not durable canonical docs — the interface does not distinguish "durable canonical" from "session scratch" (the 12 fields include no persistence/locus field; only document_lifecycle on some types).

(7) **Stale roadmap / plan documents — EXISTS.** creation-roadmap.md is VOID (2026-09-09) yet still tracked in git AND still referenced by DQE SKILL.md:9 (D12); docs/plans/archived/ holds 8 superseded batch plans under git-ignored docs/plans/ (f404d72) — i.e., both the active and the void plans are reachable from tracked SKILL.md text without a single current pointer.

(8) **Current state duplicated across documents — EXISTS.** The "what is built / what is passing / what is deferred" state is stated in ≥6 places: registry meta (registry:17-31 + per-batch notes), skill-development README:1-60, system-architecture §13, creation-roadmap §0/history, runlog.md (chronology), conflict-matrix header status, CHANGELOG — D1/D2/D3/D4/D6/D7/D11/D13 are all instances of two of these copies drifting out of sync.

(9) **Separate maintenance artifacts for the same change — EXISTS.** The v0.4.1 freeze alone touched: SKILL.md (version+scope+verdict), hard-fail.md (D-16 note), registry meta (v0_4_1_freeze + DQE row + phase_e), dqe-v0.4.1-* reports (3 new files), runlog line, skill-development README, CHANGELOG — and still MISSED DQE SKILL.md:9's roadmap pointer and SWR SKILL.md:49's LDM staleness (D3/D14) — maintenance is spread across parallel artifacts rather than one change record.

(10) **Git state duplicated in hand-written docs — EXISTS.** runlog.md retells the commit history (e.g. its 2026-08-05/06 lines mirror 9dc7f18/f39fbb2/1b28895/2c5ca1d, all in `git log`); SNAPSHOT-MANIFEST.yaml records sha256+source_commit for files whose commit is already in git (279c0ce/14959a8 are git refs, build_skill_snapshots.py:25-40); per-skill "last_verified" dates duplicate file mtimes/git history across 14 SKILL.md files.

(11) **High context-load skills — EXISTS.** S1 (≈860-line grader envelope, §problem 2); the three control flows each require the reader to hold conflict-matrix §1 + interfaces README + flow-state schema + 7+ downstream SKILL.md contracts to evaluate one routing decision; NRSD's call chain spans 10 upstream skills' contracts (SKILL.md:40-60).

(12) **Permanent documentation of transient state — EXISTS.** runlog.md (a chronicle written as if permanent), 18 dated reports in reports/ committed as living docs, CHANGELOG.md with per-sprint prose, SKILL.md HTML-comment headers (skill_version/source_commit/source_documents/last_verified) on all 14 files, registry meta narrative blocks — the system's running history is stored as many permanent text files instead of in git.

(13) **Orchestration mostly reproducing downstream logic — NOT PRESENT (as logic reproduction).** The three control flows do NOT inline their downstream skills' logic: every SKILL.md carries explicit "MUST NOT" lists (DR SKILL.md:79-83, SWR:77-81, NRSD:101-107), the routing is 27/27 across 14 conflict cases (registry:331), and e2e runs show artifacts PRODUced BY the atoms with produced_by_skill attribution (interface_check.py enforces the field). What exists is only chain-DESCRIPTION duplication — the three flows' "call chain" + "skeleton duties" prose is structurally identical text (see S13) — a documentation duplication (covered by problems 8/10 and the SPLIT label), not orchestration re-implementing downstream judgment.

## 5. Consistency notes

- Counts agree with current-system-map.md §B (per-skill eval coverage) and §C.7 (229 cases / 41 files); discrepancy IDs D1–D14 reference that file's §G.
- "14 skills" = 11 L2 atomic + 3 L1 control (release-manifest.yaml:99-116, skill_count 14 at :116; README's "2 flows" is discrepancy D1).
- No label in this file contradicts a KEEP elsewhere in the same file; S13 is the only SPLIT; H2 is the only MERGE; G2/G3 are the only REMOVE/REPLACE of non-skill items; 6 ADD entries (A1–A6).
- UNKNOWN items: provenance/license of the user-local L3 research stack (OQ-3, registry:529) — not verifiable from this workspace; deep-research's intended live status (listed installed, absent from loader, D11) — marked as discrepancy, not resolved by this audit.
