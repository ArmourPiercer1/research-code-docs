# Current Information Ownership Map (Phase 0)

```text
generated_by: phase-0-audit-subagent
scope:       D:\AI_Coworking\skill-build\research-code-docs (research-code-docs v0.1.0-alpha.1, 18 git commits, 536 tracked files)
method:      read-only audit; every duplication verified by reading the competing files; citations are file:line or commit hash;
             UNKNOWN where unverifiable. Companion file: pain-point-evidence.md (same scope).
date:        2026-09-09
status:      DRAFT-for-review
```

Measured against charter §8.1 (truth separation) and §8.2/§13 (one canonical owner per fact, artifact & canonical-source model).
This file documents the CURRENT state only; it proposes no target design.

---

## 1. Per-information-type ownership

Format per type: **owner** (verified) / **updated by, when** / **archive & supersession** / **verified duplications**.

### 1.1 Current repository state (what exists, what is tracked, what is clean)

- **Canonical owner:** git itself — `git status` / `git log` / `git diff` (repo has 19 commits, `279c0ce` 2026-07-31 → `f404d72` 2026-09-09; 536 tracked files).
- **Updated by, when:** human/agent commits; the governance layer only ever *claims* state ("git status: no … modified", "git porcelain clean") — e.g. `docs/skill-development/reports/batch2_5-integration-2026-08-05.md:119` ("git status: no .md changed, no new files"), `runlog.md:34` ("shadow read-only PROVEN (git porcelain clean)"), `docs/release/smoke-report-2026-08-06.md:82-84` ("zero footprint").
- **Archive/supersession:** none in docs; git history is the archive. Release tag `v0.1.0-alpha.1` is **local only, not pushed** (`docs/release/release-checklist.md:21,35`).
- **Duplication (verified):** the "nothing modified" fact is restated in ≥5 places per release (runlog.md:57; smoke-report:82-84; `final-flow-state.md:53-57` with `corpus_content_hash: 5fb5aa09…`; sprint6 report:20-21 "byte-identical to HEAD"). No doc is authoritative — git is. No mechanical cross-check between doc claims and git state exists.
- **Git-tracking gap (verified):** the repo is NOT a complete record of the system — `tests/corpus/upstream/` (12 pinned upstream clones + `UPSTREAM-COMMITS.tsv`), `references/` (entire tree incl. the frozen interfaces — `git ls-files references` = 0 files; untracked in `a4d780f`), `evals/skills/snapshots/` (untracked in `f39fbb2`), `docs/plans/` (never tracked; `.gitignore:19`) are all git-ignored. The pin file `UPSTREAM-COMMITS.tsv` is itself inside the ignored `upstream/` dir (`corpus-policy.md:38-39` pins commits "in" that file).

### 1.2 Project architecture

- **Canonical owner:** `docs/skill-development/system-architecture.md` (front-matter `status: DECIDED (architecture v0.1 for Phase 1)`, `last_verified: 2026-08-05`, lines 11-12; §8 gate rule revised in the Batch-2.5 sprint per `batch2_5-integration-2026-08-05.md:165-168`).
- **Updated by, when:** manual governance authoring; last substantive update 2026-08-05 (sprint bookkeeping, `runlog.md:43` "wrote=[… system-architecture (§8 gate rule advisory checkpoint)]").
- **Archive/supersession:** none; the doc self-declares DECIDED-for-Phase-1 (line 11). Not yet touched by the 2026-09-09 charter supersession (no banner).
- **Duplication (verified):**
  - The open-questions table `system-architecture.md:326-332` (OQ-1..OQ-5) is mirrored in `skills-registry.yaml:577-582` (`open_questions`) — two stores, no stated precedence, and the `OQ-` namespace **collides** with the different OQ-1/OQ-2/OQ-3 in `adr/ADR-DQE-001-…md:225-235` (OQ-1 there = reproducibility, RESOLVED 2026-08-02; OQ-1 in arch §13 = issue tracker, OPEN). Same ID string, three different meanings, no global registry.
  - The "advisory checkpoint, not terminal gate" architecture rule is restated in ≥5 docs: `creation-roadmap.md:22-23`, `quality-control-plan.md:174`, `docs/skill-development/README.md:25-31`, `batch2_5-integration-2026-08-05.md:165-168`, `CHANGELOG.md:58-65`. Currently consistent; none is mechanically checked against the others.

### 1.3 Current roadmap / active routes

- **Canonical owner (today):** the charter `docs/plans/active/research_software_agent_workflow_reconstruction_charter.md` — named "the governing development plan" by both supersession banners (`docs/skill-development/README.md:3-8`, `creation-roadmap.md:3-7`, both dated 2026-09-09). Live progress: `docs/plans/active/reconstruction/README.md:44-58` (status table, all 13 deliverables `pending`) + `execution-notes.md` ("parent-agent working file", line 5).
- **Updated by, when:** parent agent, ad hoc per round (execution-notes.md round structure); the charter itself is static so far.
- **Archive/supersession:** the old roadmap `creation-roadmap.md` carries a `⛔ VOID / SUPERSEDED (2026-09-09)` banner (lines 3-7) and meta `status: SUPERSEDED` (line 17); the 8 former per-sprint plans moved from `docs/third-party-suggestions/` to `docs/plans/archived/` in `f404d72` (sha256-verified, per commit body). `docs/plans/` is git-ignored (`.gitignore:19`) — the entire active plan is **local-only, outside version control**.
- **Duplication (verified):**
  - `docs/skill-development/README.md:116-118` still ends with "**Next (directive §10):** **Batch 4** — the numerical-design atoms …" while the banner 108 lines above says "do not start new Batch 4/5 work under the retired roadmap" (README:7-8) and `creation-roadmap.md:6-7` repeats the same instruction. The contradiction is *labeled* (the "Next" section heading, README:88, says "as recorded 2026-08-06 — SUPERSEDED by the reconstruction charter") but the content was not removed or moved.
  - `creation-roadmap.md:29` says "Current phase lives in `skills-registry.yaml` + `reports/runlog.md`, not here" — a stale pointer in two directions: the registry header stops at `last_verified: 2026-08-05` (registry:8) and governance moved to the charter on 2026-09-09.
  - Per-batch "Status:" lines in the voided roadmap (`creation-roadmap.md:65,89,115,151`) duplicate the registry `last_evaluated` dates and runlog entries; this exact drift class was caught once in the field (see 1.17 D-10).
  - The registry `meta` block carries its own roadmap-ish state: `batch2_gate` (registry:25), `phase_e` (registry:26), `v0_4_1_freeze` (registry:27), `batch2_5` (registry:28) — a fourth restatement of "where the project is".

### 1.4 Evidence (literature / research)

- **Canonical owner:** per-run, not standing. Track-B evidence lives in `evals/skills/results/batch2_5/research-chain/` (`lit-review-results.md`, `research-evidence-map.md`, `decision-register.md`); corpus seed provenance in `tests/corpus/source-seeds/seed-register.yaml` + `UPSTREAM-COMMITS.tsv` (`corpus-policy.md:33-39`).
- **Updated by, when:** the research-chain ran once (2026-08-05, `batch2_5-integration-2026-08-05.md:88-98`, real OpenAlex retrieval, 5 sources); seeds pinned at corpus build 2026-07-31 (`corpus-build-report.md:18-41`).
- **Archive/supersession:** none for research evidence; upstream seeds are immutable (`corpus-policy.md:26-29`), license-quarantined seeds kept clone-only (`corpus-policy.md:49-52`).
- **Duplication (verified):** none material — the 5 Track-B sources are cited in `batch2_5-integration-2026-08-05.md:97-98` and in the run's `lit-review-results.md` (run artifact). **No canonical owner:** there is no standing project-level evidence store; evidence exists only inside dated eval runs and will not be findable as "project evidence" without knowing the run path.

### 1.5 Experiment / eval results + provenance

- **Canonical owner:** raw runs — `evals/skills/results/**` (per-skill dated outputs; `git log --diff-filter=D -- 'evals/skills/results/*'` is empty: never deleted/moved), blind runs — `tests/corpus/blind-runs/<run>/` (inputs + params + `.secret/mapping.tsv` + raw-results.json), frozen skill bundles — `evals/skills/snapshots/`.
- **Updated by, when:** harness scripts + sub-agent runs; append-only in practice (each run = new dated dir/file).
- **Archive/supersession:** `release-manifest.yaml:162-170` excludes `tests/corpus/blind-runs/`, `evals/skills/snapshots/`, `tests/corpus/upstream/` from distribution; corpus quarantine (`tests/corpus/cases/quarantine/` + `QUARANTINE.yaml`, `defect-ledger.md:37`).
- **Duplication (verified):**
  - The same run's verdict facts are stored in ≥3 layers: raw `raw-results.json` / per-case result JSONs → `metrics.json` + `evaluation-summary.md` → the dated narrative report → a runlog line → the append-only `docs/testing/benchmark-changelog.md` entry. Example: the 2026-07-31 matrix's "0/7 §17 metrics" appears in `blind-matrix-2026-07-31/evaluation-summary.md:9-17`, `benchmark-changelog.md:34-39`, and the narrative `dqe-blind-matrix-investigation-2026-07-31.md:20-21`. No checker verifies layer consistency; the narrative layer is where corrections (§4X re-attribution) actually happen, so the raw+metrics layers are the pre-correction record.
  - **Stale provenance reference (verified):** `skills-registry.yaml:26` (meta `phase_e`) declares "Canary-failure evidence + frozen snapshots are PRESERVED: `tests/corpus/blind-runs/phase-e-2026-08-05/` and `evals/skills/snapshots/{dqe-v0.3.0,dqe-v0.4.0-pre-d16,dqe-v0.4.1-candidate}/`" — but `evals/skills/snapshots/` is currently an **empty directory** (0 files), and the bundles are not tracked in git (untracked `f39fbb2`). The registry claim and disk disagree today.

### 1.6 Open decisions

- **Canonical owner:** **none single** — decision items are owned per context:
  - corpus gold-label decisions: `docs/testing/decisions-pending-2026-07-31.md` (D-1..D-7, RESOLVED banner line 9: "RESOLVED 2026-07-31 (v3) … RESOLVED 2026-08-02 (v4)");
  - refactor-chain canonical-home decisions: `evals/skills/results/batch2_5/document-chain/open-decisions.md:9` (`status: OPEN (10 decisions; none decided here)`; D-1/D-4 still open per `final-flow-state.md:42-45`);
  - architecture questions: `system-architecture.md:326-332` (+ registry mirror 1.2);
  - DQE contract questions: `adr/ADR-DQE-001-…md:225-235` (OQ-REPRO RESOLVED, OQ-2 RESOLVED, OQ-3 open) + `dqe-v0.4.1-phase-e-canary-decision.md` (D-17);
  - per-run handoff decisions: `open_decisions` field of flow-state artifacts (`final-flow-state.md:42-45`, `flow-state-docs-skill-development.md:30-34`).
- **Updated by, when:** human rulings recorded by the orchestrator into the owning file (user_decision blocks, e.g. `decisions-pending-2026-07-31.md:19-21,218-224`); flow-states updated by the flows.
- **Archive/supersession:** `open-decisions.md` says "a plan raises, it does not pick" (line 18); there is no decision register that aggregates all namespaces — UDM's `decision-register` schema (`references/templates/decision-register.template.md`) is a per-run artifact format, and no standing register file exists in the repo.
- **Duplication (verified):**
  - **D-1/D-4 duplication across 7+ files:** `open-decisions.md:26-27` (definition), `flow-state-docs-skill-development.md:31-32`, `final-flow-state.md:42-45`, `migration-map.md` (10 of 11 dispositions `DEFERRED (blocked_by: D-1)` per `final-flow-state.md:35`), `no-skill-baseline-comparison.md:25-31`, `candidate-doc-set/README.md:24,47,75` ("PENDING decision D-1"), `candidate-doc-set/creation-roadmap.md:12-18,28`, `maintenance-impact-report.md:41-64`. Consistent, but the *decision state* is re-declared in every downstream artifact with no single status query point.
  - **ID namespace collision (verified):** `decisions-pending-2026-07-31.md` uses D-1 (gold label FAIL-vs-PARTIAL, line 31) and D-4 (user spot-check scope, line 34); `open-decisions.md` uses D-1 (canonical status owner, line 26) and D-4 (README index scope, line 27); the defect ledger uses D-01..D-17 (a third namespace, `dqe-v0.4-defect-ledger.md:47-352`). "D-1" and "D-4" each denote **two different decisions** in two live files; `no-skill-baseline-comparison.md:25-29` refers to the open-decisions.md meanings without disambiguating.
  - **OQ-1..OQ-5 collision** as in 1.2 (arch §13 vs ADR-DQE-001).

### 1.7 Durable decision rationale

- **Canonical owner:** `docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md` — the **only** ADR (ACCEPTED 2026-08-02, line 9). Secondary rationale stores: `decisions-pending-2026-07-31.md` (rulings + reasoning), `dqe-v0.4.1-phase-e-canary-decision.md` (D-17 + scope-out), `skills-registry.yaml:25-28` (meta notes: batch2_gate, phase_e, v0_4_1_freeze, batch2_5), `batch2_5-integration-2026-08-05.md` §5 (why RQLP+RES were NOT merged).
- **Updated by, when:** ADR is frozen after acceptance (lifecycle `ACCEPTED`); rationale for new decisions is appended to dated reports, not to a register.
- **Archive/supersession:** the ADR superseded a PROPOSED draft (line 15); no ADR index exists; no "superseded-in-part" annotation mechanism in use.
- **Duplication/drift (verified):**
  - ADR-DQE-001:227-230 records OQ-REPRO=RESOLVED (Option A) with the rationale "blocking (BLOCK via rubric+non-compensatory) under `controlled+release-gate`" — the 2026-08-05 canary **retroactively falsified** the skill-side of that claim (D-17: "retroactively falsifies the D.3 'BLOCK×3 / 8/8 / OQ-REPRO=A confirmed-by-skill' claim", `dqe-v0.4-defect-ledger.md:330-337`), but the ADR was never annotated. The suggested annotation is itself an open decision (`open-decisions.md:40`, D-3: "Annotate ADR-DQE-001 Status with a dated 'superseded-in-part' note" — OPEN).
  - The v0.4.1 scope-out rationale (why DQE is advisory/profile-scoped) is stated **four times**: `runlog.md:32`, `docs/skill-development/README.md:25-31`, `skills-registry.yaml:27`, `dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md`. Consistent today; the registry meta note is the most machine-readable copy.

### 1.8 Execution plans (per-sprint directives)

- **Canonical owner:** the 8 archived directive plans in `docs/plans/archived/` (moved from `docs/third-party-suggestions/` in `f404d72`; that directory now exists but is **empty**); going forward: the charter + `docs/plans/active/reconstruction/execution-notes.md`.
- **Updated by, when:** written by the orchestrator ("third-party suggestions" per the old naming) at the start of each sprint; frozen afterwards.
- **Archive/supersession:** per-sprint plans are additive archives (never edited post-hoc, by practice — each commit added exactly one plan doc: `c108695`, `14959a8`, `0585574`, `975e930`, `7919bc4`, `07b5306`, `9dc7f18`, `2c5ca1d`); supersession by the next sprint's plan (implicit) and by the charter (2026-09-09, explicit for the roadmap only).
- **Duplication (verified):** historical report headers still cite the **old paths** — e.g. `batch2_5-integration-2026-08-05.md:6` (`source_documents: docs/third-party-suggestions/Batch2_5集成冲刺…`), `sprint6…2026-08-06.md:8`, `references/interfaces/README.md:6`, `ADR-DQE-001…md:5-8`, `dqe-v0.4-defect-ledger.md:7`. These paths no longer exist on disk. The convention is declared: "Historical artifacts … keep the old paths — they are frozen-in-time records" (`CHANGELOG.md:16-17`), so this is a *labeled* broken-reference class, not drift — but nothing validates it.

### 1.9 Task dependency graph

- **Canonical owner:** **none.** Partial, mutually-overlapping views: per-skill `upstream_dependencies`/`downstream_outputs` fields in `skills-registry.yaml` (e.g. DQE entry, registry:57-58); the call-chain diagrams in `system-architecture.md` §3 (architecture-level); the per-batch build order in `creation-roadmap.md` §2 (e.g. lines 78-80) and registry:25 ("Recommended order: …"); the pairwise co-run rules in `conflict-matrix.md` (which is co-trigger, not dependency).
- **Updated by, when:** each at authoring time; never reconciled.
- **Archive/supersession:** n/a.
- **Duplication (verified):** the Batch-2 build order appears in `creation-roadmap.md:78-80` (table) and `skills-registry.yaml:25` (meta `batch2_gate` "Recommended order"); the Batch-4 slice order appears in `sprint6…2026-08-06.md:136-140` and the roadmap §4/§5. No single machine-readable graph; a reader must merge 4 documents.

### 1.10 Session handoff

- **Canonical owner (skill-chain handoffs):** the frozen 12-field handoff contract — `references/interfaces/README.md` (freeze `batch2.5-v1`, lines 15-20) + the 11 `references/interfaces/*.schema.md` + `references/templates/*.template.md` + `evals/skills/harness/checkers/interface_check.py` (checker, registered ADVISORY, `run_checks.py`). Run-level handoff state: flow-state artifacts (`references/interfaces/flow-state.schema.md`, `flow_state_check.py`).
- **Updated by, when:** frozen 2026-08-05 (`interfaces/README.md:1-13`); Batch-5 additive extension documented in-place (lines 40-56) without re-freezing; the rename `.claude`→`.agents` (62ada30) required path fixes in 7 scripts (`install_workspace.py` 26±, `smoke_test.py` 10±, …).
- **Archive/supersession:** versioned by name (`batch2.5-v1` → next is `batch2.5-v2`, `interfaces/README.md:120-124`); "Not frozen" list at lines 120-124.
- **Duplication (verified):**
  - The common 12-field header is stated in `interfaces/README.md` (common-header section), in **each** of the 11 schema files, and in **each** of the 11 templates — a deliberate frozen-contract replication; drift between them is only caught when `interface_check.py` is run with `--advisory-is-hard` (advisory by default, `interfaces/README.md:116-118`).
  - **No owner for governance-process session handoff:** the runlog claims writes to "memory" (`runlog.md:43,48,56`, `wrote=[… memory]`) but **no memory file exists anywhere in the repo** (verified by recursive search); the handoff of the governance work itself lived in the chat session and the runlog line only. Session-local, unarchived.

### 1.11 Incident / defect history

- **Canonical owner (DQE defects only):** `docs/skill-development/reports/dqe-v0.4-defect-ledger.md` (self-declared `status: LIVING (defect ledger; entries move OPEN -> IMPLEMENTED -> VERIFIED)`, lines 9, 41-43).
- **Canonical owner (harness/process incidents):** **none** — scattered across: `benchmark-changelog.md:129` (`63M-token runaway → HARNESS_ORCHESTRATION_FAILURE`), `dqe-v0.4.1-diagnostic-close.md:41-59`, `batch2_5-integration-2026-08-05.md:134-135` (P1/P2 harness nits), `batch1-eval-run-2026-07-30.md:33-35` (scorer bug), `runlog.md:17` ("3 precision bugs found+fixed"), `runlog.md:57` ("fixed 1 real preflight bug"), git commits (`1b28895` cc-switch parse fix, `2a82ca9` .pyc hygiene).
- **Updated by, when:** ledger entries at discovery + implementation; the rest, ad hoc in sprint reports.
- **Archive/supersession:** ledger entries move to VERIFIED in place; release-side defect intake *format* is defined (`KNOWN_LIMITATIONS.md:59-62`, "run-feedback record … a new regression is added only when a real run exposes a reproducible error") but **no ledger file implements it**.
- **Duplication (verified):** the 63M-token runaway is documented in `dqe-v0.4.1-diagnostic-close.md:41-48` and `benchmark-changelog.md:93-111` with matching numbers, but is **absent from `runlog.md`** entirely (the v0.4.x period is two retroactive lines, see 1.12) — so the project's own observability log lost its largest incident.

### 1.12 Implementation chronology

- **Canonical owner:** `docs/skill-development/reports/runlog.md` — self-declared "Append-only observability log (quality-control-plan §7). One line per skill/eval run" (lines 12-13), header `last_verified: 2026-08-06T01:45Z` (line 9).
- **Updated by, when:** *supposed* to be per-run; actually batch-written. `runlog.md:31` admits it: `trigger=logged-retroactively … note=history authority = reports/dqe-v0.4*.md (per-step timestamps not reconstructed here)` — the entire 2026-07-31→08-05 period (corpus v4, v0.4, D.3, canary) is two lines stamped `2026-08-05T09:09Z`.
- **Archive/supersession:** append-only by declaration; no mechanism enforces it.
- **Duplication (verified):** the chronology is stored three ways: runlog lines; git commit messages (`git log --oneline` — 19 commits, one-line Chinese messages like `7919bc4 执行了第二批四个skills的开发，完成了MVP Spring 3`); and per-report front-matter headers. The runlog is the only *structured* one, and it is the least accurate for the DQE era. Also: the pre-git era (all 2026-07-30 work: Phase 0/1, Batch 1, v0.2, v0.3) has **no granular history at all** — git starts at `279c0ce` (2026-07-31, 521 files in one commit); `defect-ledger.md:25` explains: "Baseline freeze (replaces a git tag — this workspace is not a git repo)".

### 1.13 Skill registry (roster, versions, statuses, eval state)

- **Canonical owner:** `docs/skill-development/skills-registry.yaml` (machine roster: 14 experimental + 12 planned `0.0.0` stubs + 23 `existing_installed` rows + open_questions + meta; header lines 1-15).
- **Updated by, when:** manual, at each sprint's bookkeeping step (`runlog.md` "wrote=[… registry]" lines, e.g. 33, 43, 52); last header `last_verified: 2026-08-05` (line 8).
- **Archive/supersession:** in-place edits (no versioning of the registry file itself; `schema_version: "0.1"` line 18, never bumped).
- **Duplication (verified):**
  - Per-skill **version** exists in 3 places: registry (e.g. `reg:39` `"0.4.1"`), `release-manifest.yaml` skills section, SKILL.md HTML comment `skill_version:` line (e.g. `.agents/skills/documentation-quality-evaluator/SKILL.md:8`). Mechanically cross-checked by `scripts/preflight.py:151-162` (manifest vs registry = blocking; manifest vs SKILL.md = warning) — a *controlled* duplication, currently green.
  - Per-skill **status** in registry (`reg:40` etc.) and SKILL.md comment (every `SKILL.md:9`); no mechanical check. Verified drift: `documentation-refactor/SKILL.md:27-28` still says "Its executor tail (migration → rewrite → living-maintainer) is **Batch 5 and not built**, so a real v0 run **stops at `flow_status=BLOCKED`**" while registry:333 says "Sprint 6B closed its FIRST REAL vertical slice: the Batch-5 executor tail … is now **BUILT**, so the flow **COMPLETEs** for the dry-run+candidate scope" — SKILL.md `last_verified: 2026-08-05` (SKILL.md:20) vs registry `last_evaluated: "2026-08-06"` (reg:332); the same 1-day lag on the other two Batch-3 flows (reg:364/reg:396 vs SKILL.md:19).
  - Stale pointer: `documentation-quality-evaluator/SKILL.md:9` status qualifier says "until the v0.4.1 admission matrix passes; see `docs/skill-development/creation-roadmap.md`" — a file that has been VOID since 2026-09-09.
  - **`status:` key overloaded across 3 vocabularies in one file** (verified): lifecycle values `experimental`/`planned` (reg:40, reg:399-404), open-question values `OPEN`/`DEFERRED` (reg:578-582), and the claim vocabulary `meta.status_vocabulary` (reg:21) contains `OPEN`/`DEFERRED` too; the header also declares unused lifecycle values `active|deprecated|replaced|retired|reference-only` (reg:11). Document-level comment statuses drift further: `README.md:15` `status: DECIDED (…)`, `creation-roadmap.md:17` `status: SUPERSEDED (2026-09-09)` — "SUPERSEDED" is in **neither** declared vocabulary.

### 1.14 Eval cases & results

- **Canonical owner:** case definitions — `evals/skills/{trigger,conflict,multi-turn,task-quality,reader-tests,regression}/*.yaml` (schema in `evals/skills/README.md:47-69`); results — `evals/skills/results/<skill>/<date>.*`. DQE corpus cases — `tests/corpus/cases/**` (`manifest.yaml` per case, `case_version` field).
- **Updated by, when:** case authors + repair scripts; `dataset_version` bumped per corpus change (`corpus-build-report.md:12-16`, `benchmark-changelog.md:12-13`).
- **Archive/supersession:** "A repaired case is a new `case_version`/new archive, never an edit of a baseline result" (`defect-ledger.md:27-29`); quarantine dir + `QUARANTINE.yaml` (`corpus-policy.md:49-52`); ≥3 hidden holdout cases (`corpus-policy.md:89-91`).
- **Duplication (verified):**
  - Expected labels are stored in **two places by design**: case `manifest.yaml` (`expected.*`, read only by the comparator) and the blind-run `.secret/mapping.tsv` (blind_id→case_id only — no verdicts, verified in `adj-2026-07-31/.secret/mapping.tsv`); plus user-override encoding in `evals/skills/adjudication/reviewer-results-2026-07-31.yaml` (`user_decision: FAIL, user_decision_ref: "D-1"` etc.). Isolation is deliberate (`corpus-policy.md:65-71`) but there is no checker that manifest ↔ results-yaml ↔ adjudication narrative agree.
  - Adjudication facts live in two parallel trees: `evals/skills/adjudication/*.md` (round 1: raw reviewer outputs + consensus mapping) and `docs/testing/adjudication-*.md` (v4/v4b: summaries). Same round, two homes, no stated precedence (raw vs summary).

### 1.15 Test corpus (DQE)

- **Canonical owner:** `tests/corpus/` — cases/ + source-seeds/ + upstream/ (immutable) + blind-runs/; policy `docs/testing/corpus-policy.md`; append-only changelog `docs/testing/benchmark-changelog.md`; build record `docs/testing/corpus-build-report.md`.
- **Updated by, when:** corpus repair scripts (`generate_mutations.py` with postconditions, `validate_mutation_semantics.py` — added `c108695`) + human rulings; upstream immutable, pinned (`corpus-policy.md:26-39`).
- **Archive/supersession:** quarantine (49-52); `dataset_version` bumping; "nothing here is pushed" (`corpus-policy.md:99`).
- **Duplication (verified):** dataset version + case census restated in: each case manifest (`dataset_version`), `benchmark-changelog.md` entries, `corpus-repair-report-v4.md` header, and as **defaults baked into code** (`scripts/aggregate_eval_results.py:248-249` `--skill-version` default `"0.4.1"`, `--dataset-version` default `"4"`). The code defaults can silently drift from the corpus if bumped in docs only.

### 1.16 Schemas / templates / interfaces

- **Canonical owner:** `references/interfaces/` (README freeze record + 11 schema files) + `references/templates/` (11 templates) + `evals/skills/harness/checkers/` (deterministic enforcement).
- **Updated by, when:** freeze 2026-08-05; Batch-5 additive extension 2026-08-06 documented in the freeze README itself (lines 40-56).
- **Archive/supersession:** interface versioning by suffix (`batch2.5-v2` rule, lines 120-124); superseded schema = new version file (none so far).
- **Duplication (verified):** see 1.10 (header replicated across README + 11 schemas + 11 templates). **Provenance gap (verified):** the entire `references/` tree is git-untracked (`.gitignore:13`, untracked `a4d780f`, 198 files removed from tracking) — the "frozen" contract has **no version-controlled copy**; its integrity rests on local files + the `SNAPSHOT-MANIFEST.yaml`-style sha256 practice, and the frozen DQE skill bundles that encode the same contract are in the empty `evals/skills/snapshots/` dir (1.5).

### 1.17 Release state (version / manifest / changelog)

- **Canonical owner:** `release-manifest.yaml` — self-declared "the **authoritative** description of WHAT this release contains and its SAFETY POSTURE" (lines 5-6), `version: 0.1.0-alpha.1` (line 22), `source_commit: 9dc7f18…` (line 32); machine version `VERSION` (line 1); `CHANGELOG.md` (loose Keep-a-Changelog, header lines 1-6).
- **Updated by, when:** the R0 packaging commit `2c5ca1d` (2026-08-07, 21 files, purely additive per commit body); `CHANGELOG.md` has an `[Unreleased]` section (lines 8-27) already recording the 2026-09-09 renames/voiding **after** the alpha tag.
- **Archive/supersession:** tag `v0.1.0-alpha.1` is local, "push gated on owner" (`release-checklist.md:21,35`); the manifest documents a two-commit semantics — baseline `9dc7f18` vs packaging commit (lines 25-32, "A file cannot embed its own commit SHA").
- **Duplication (verified):**
  - The release version string `0.1.0-alpha.1` is stored in **13+ files**: `VERSION:1`, `README.md:3`, `release-manifest.yaml:22`, `CHANGELOG.md:29,78`, `INSTALL.md:1`, `QUICKSTART.md:1`, `UNINSTALL.md:1`, `KNOWN_LIMITATIONS.md:1`, `SUPPORTED_ENVIRONMENTS.md:1`, `SUPPORT_MATRIX.md:1`, `THIRD_PARTY_LICENSES.md:1`, `docs/release/{smoke-report,release-checklist,clean-room-smoke-test}.md` (line 1 each; checklist also lines 10, 21, 35), `runlog.md:57`. The manifest's own header admits the manual regime: "Keep in sync with: VERSION, skills-registry.yaml, THIRD_PARTY_LICENSES.md, SUPPORT_MATRIX.md, KNOWN_LIMITATIONS.md" (manifest:16-17). Only per-skill versions are mechanically checked (`preflight.py:151-162`); the release version in the 11 doc headers is **not checked anywhere** — `preflight.py:270` only reads `VERSION` for display.
  - Safety posture restated in 5 consistent copies: `release-manifest.yaml:43-51` (posture block), `README.md:37-41` (safety posture block), `SUPPORT_MATRIX.md:28-34` (safety invariants block), `CHANGELOG.md:58-65` (Safety section), `KNOWN_LIMITATIONS.md` (11 caveats). Consistent today; no cross-check.
  - Stale per-skill version claims in `docs/skill-development/README.md:68-70`: header says the four Batch-1 skills are "now at **v0.2.0**" while line 70 describes DQE as "**v0.3.0**" — the registry says DQE is **0.4.1** (reg:39). A third, uncontrolled copy of per-skill versions (README prose) that has not moved since 2026-07-30.

---

## 2. Information types with NO canonical owner (owned nowhere / session-local)

| # | Information type | Where the fragments live (verified) | Consequence |
|---|---|---|---|
| 1 | **Why a route/option was rejected** | Scattered: ADR-DQE-001 (HF-REPRO NOT-ADOPTED rationale, :70-73, :102-104); defect-ledger verdicts (D-02 "REJECTED as a standalone skill defect", :240-244); `open-decisions.md` IA-1 "leave as-is for now" (:48); `batch2_5…md` §5 (RQLP+RES not merged); runlog notes | No rejected-options register; re-litigating a rejected route requires re-reading 4-5 documents; a new session cannot answer "what did we already reject and why" from one file |
| 2 | **Eval verdict history (DQE's own track record over time)** | Per-run dirs (`results/documentation-quality-evaluator/{e2e,blind-matrix-2026-07-31,diag-2026-08-02,…}`), narrative reports (batch1 → v0.3 → matrix → diag → canary), `benchmark-changelog.md` (corpus side only) | No consolidated "v0.1→v0.4.1 verdict history" ledger; the story is reconstructable only by reading ~10 documents in order |
| 3 | **Governance-session handoff ("memory")** | `runlog.md:43,48,56` claim `wrote=[… memory]`; no such file exists in the repo (verified recursively) | The between-session memory of the governance process is session-local (chat), not durable |
| 4 | **Interface freeze change-history (why each field/rule)** | Freeze README (current contract, `interfaces/README.md:15-124`) + archived directive plans (`docs/plans/archived/Batch2_5…md` §5) + sprint report `batch2_5…md:40-56` | The *what* is owned; the *why* (design rationale per field) lives in an archived plan that is itself a frozen snapshot; no ADR for the interface |
| 5 | **Harness/process incident ledger (non-DQE)** | 1.11 list (benchmark-changelog L129, diagnostic-close, batch2_5 P1/P2, batch1 §2, runlog notes, commits 1b28895/2a82ca9) | No single incident ledger; the release-side intake format exists (KNOWN_LIMITATIONS:59-62) but has no home file |
| 6 | **Task dependency graph (machine-readable)** | 1.9 (4 partial doc-level views) | No `dependencies:` graph a script can consume; integration ordering is argued in prose per sprint |
| 7 | **Corpus "current dataset state" (case counts, gold counts, quarantine list)** | `benchmark-changelog.md` entries, `corpus-repair-report-v4.md`, per-case manifests, code defaults (`aggregate_eval_results.py:248-249`) | No live `corpus-state.yaml`; the authoritative count of gold/quarantined cases must be recomputed from manifests |
| 8 | **Open-architecture-question lifecycle** | arch §13 table + registry mirror (1.2) — "tracked, not hidden" (arch:334) but with colliding OQ IDs (1.6) | Questions can be "resolved" in one place (ADR) while remaining OPEN in two others (arch §13, registry) |

---

## 3. Consolidated duplication ledger (verified)

| # | Fact duplicated | Competing locations (quotes) | Authoritative today | Checked mechanically? |
|---|---|---|---|---|
| D1 | Release version `0.1.0-alpha.1` | `VERSION:1` · `README.md:3` "**v0.1.0-alpha.1 — Internal Controlled Preview**" · `release-manifest.yaml:22` `version: 0.1.0-alpha.1` · `CHANGELOG.md:29` "## [0.1.0-alpha.1] — 2026-08-06" · 8 release-doc line-1 titles · `runlog.md:57` | `release-manifest.yaml` (self-declared) + `VERSION` | No (release version); per-skill versions yes (`preflight.py:151-162`) |
| D2 | Per-skill version | registry (reg:39 `"0.4.1"`) · manifest skills section · SKILL.md comment (SKILL.md:8) · **README prose** `README.md:68` "now at **v0.2.0**" / `:70` "**v0.3.0**" | registry+manifest | Partially (3 stores checked; README prose not) |
| D3 | Per-skill status + "can it COMPLETE or BLOCKED" | `documentation-refactor/SKILL.md:27-28` "executor tail … **not built** … stops at `flow_status=BLOCKED`" vs registry:333 "executor tail … is now **BUILT**, so the flow **COMPLETEs**" | registry (reg:332 date 2026-08-06 > SKILL.md:20 2026-08-05) | No |
| D4 | DQE status pointer | `DQE/SKILL.md:9` "…see `docs/skill-development/creation-roadmap.md`" (VOID since 2026-09-09, `creation-roadmap.md:3-7`) | banner in README/roadmap | No |
| D5 | "What is next" | `README.md:116-118` "**Next … Batch 4**" vs `README.md:7-8` "do not start new Batch 4/5 work under the retired roadmap" vs charter (governing, per both banners) | charter + `reconstruction/README.md` status table | No (contradiction labeled at README:88) |
| D6 | Current-phase pointer | `creation-roadmap.md:29` "Current phase lives in skills-registry.yaml + reports/runlog.md, not here" (registry header stops 2026-08-05, reg:8) | charter-era `reconstruction/` | No |
| D7 | D-17 decision state | `dqe-v0.4-defect-ledger.md:352` "status: **OPEN** — awaiting user decision (A/B/C)" vs `runlog.md:32` "D-17 resolved by **SCOPE-OUT**" vs `README.md:25-31` "is resolved by **scoping that profile out**" vs registry:27 "resolves the halted D-17 canary by SCOPING OUT" | scope-out resolution (runlog + freeze report + canary-decision RESOLVED banner per runlog:32) | No — LIVING ledger not updated |
| D8 | Open decisions D-1/D-4 (+D-6…) | defined in `open-decisions.md:26-27` (D-1=status owner, D-4=index scope) AND in `decisions-pending-2026-07-31.md:31,34` (D-1=FAIL-vs-PARTIAL, D-4=spot-check scope); re-declared in 7+ refactor artifacts (`final-flow-state.md:42-45`, `candidate-doc-set/README.md:24`, `maintenance-impact-report.md:41-64`, …) | per-namespace source files; no cross-namespace ID registry | No |
| D9 | OQ-1..OQ-5 IDs | `system-architecture.md:328` "OQ-1 Adopt an issue tracker? … OPEN" + registry:577-582 vs `ADR-DQE-001…md:227` "OQ-1 → **RESOLVED** (Option A)" (reproducibility) | none — same ID, two questions, opposite states | No |
| D10 | Per-batch build status | `creation-roadmap.md:65` "**Status: ALL FOUR BUILT + light-round PASSED (2026-08-05)**" etc. vs registry `last_evaluated` vs runlog lines; historical instance: `creation-roadmap.md:23` "Batch 0 — Status: IN PROGRESS" caught stale by the system's own agent (`batch2_5…md:76-78`, "Fixed in this sprint's bookkeeping") | registry + runlog | No |
| D11 | Hard-fail catalog (HF-1..15) | `quality-control-plan.md:26-43` (v0.1-era table; HF-9 row: "checker (front-matter completeness)", no profile severity) vs `evals/skills/harness/hard-fail.md:27-34,82-98` (v0.4: "Severity is profile-dependent (v0.4…)", §HF-9 profile table) | `hard-fail.md` (self-declared "Full catalog", `quality-control-plan.md:49`) | No — the drift check was an *open* repo-verifiable decision D-6 (`open-decisions.md:33`, never executed); **verified drifted today** |
| D12 | OQ-REPRO=A rationale | `ADR-DQE-001…md:227-230` (BLOCK under controlled+release-gate, "confirmed by the skill") vs canary `dqe-v0.4.1-phase-e-canary-decision.md:89-96` (stable ALLOW×3; run-2 QUALITY_BAND=FAIL+READER_TEST=FAIL still ALLOW) + `defect-ledger.md:330-337` "retroactively falsifies …" | canary evidence + scope-out (2026-08-05); ADR text stale | No — annotation is open decision D-3 (`open-decisions.md:40`) |
| D13 | Directive plan locations | reports cite `docs/third-party-suggestions/…` (`batch2_5…md:6`, `sprint6…md:8`, `interfaces/README.md:6`, ADR:5-8, ledger:7) vs actual `docs/plans/archived/…` (moved in `f404d72`) | `docs/plans/archived/` (current); old citations = frozen-in-time records per `CHANGELOG.md:16-17` | No |
| D14 | DQE advisory/frozen posture | `registry:25-27` (batch2_gate/phase_e/v0_4_1_freeze) · `creation-roadmap.md:23` · `quality-control-plan.md:174` · `README.md:25-31` · `CHANGELOG.md:58-65` · `KNOWN_LIMITATIONS.md:16-22` · DQE SKILL.md:9 | registry meta (most machine-readable) | No (7 restatements) |
| D15 | candidate-doc-set copies of repo docs | `candidate-doc-set/README.md:46` "Under [`.claude/skills/`]" + `:70-80` "## Next … see creation-roadmap.md" vs live `docs/skill-development/README.md:3-8` (2026-09-09 plan-change banner, absent in candidate) + `:88` "Next (…SUPERSEDED)"; candidate `creation-roadmap.md:10` (no VOID banner) vs live `creation-roadmap.md:3-7` (VOID) | live docs; candidates are DRAFT staging (`candidate-doc-set/README.md:6` `document_lifecycle: DRAFT`) | No — re-verification "at apply" only (`KNOWN_LIMITATIONS.md:11-14`) |
| D16 | "nothing was modified" claims | `runlog.md:57` · `smoke-report:82-84` · `final-flow-state.md:53-57` (corpus_content_hash) · sprint6:20-21 | git | No |
| D17 | Corpus dataset version + census | case manifests · `benchmark-changelog.md` entries · `corpus-repair-report-v4.md:3` · code defaults `aggregate_eval_results.py:248-249` (`"0.4.1"` / `"4"`) | manifests + changelog | No |
| D18 | Safety posture | manifest:43-51 · README:37-41 · SUPPORT_MATRIX:28-34 · CHANGELOG:58-65 | manifest (self-declared) | No |
| D19 | Frozen DQE snapshots "preserved" | `registry:26` "frozen snapshots are PRESERVED: evals/skills/snapshots/{…3 bundles}" vs **empty directory on disk** (verified; untracked in `f39fbb2`) | disk/git disagree → UNKNOWN what is preserved | No |

---

## 4. Structural observations for Phase 1 (facts, not proposals)

1. **Two "append-only" logs with different authority** (runlog vs per-report docs vs git) — the runlog's own line 31 delegates historical authority away from itself for the most event-dense period.
2. **The volatile-state→pointer rule exists (HF-14b) but has no target**: D-1 ("who owns current status") is OPEN, so every pointer the Batch-3 closure produced says "PENDING decision D-1" (`candidate-doc-set/README.md:24`) — the cure is in flight, the disease (D10/D14-class duplication) persists in the live docs.
3. **Freeze without version control**: the three "frozen" artifact families (interface schemas `references/`, DQE snapshots `evals/skills/snapshots/`, upstream pins `tests/corpus/upstream/`) are all git-untracked; freezes are enforced by prose + local sha256, and one (snapshots) is already inconsistent with its registry claim (D19).
4. **ID namespaces are local, not global**: D-* and OQ-* IDs collide across at least three decision contexts (D8/D9); "SUPERSEDED" is used as a document status that belongs to no declared vocabulary (1.13).
5. **The governance corpus is the system's test fixture and its own subject at once** — `docs/skill-development/` was the Track-A eval corpus (`batch2_5…md:60-81`) and the documentation-refactor target; defects found *about* it (stale status lines, version drift) are simultaneously eval results and the system's own debt (D10, D11, D15).
