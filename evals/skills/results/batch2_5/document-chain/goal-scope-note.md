---
generated_by_skill: goal-scope-and-workflow-elicitor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/document-chain/project-state-report.md]
artifact_type: goal-scope-note
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T14:00:00Z
scope: "Goal + in/out scope + non-goals + workflow for restructuring the docs/skill-development governance corpus (24 files) to one canonical home per information-type with pointer-only volatile state and a resolution plan for the enumerated staleness/contradictions. EXCLUDES designing the canonical-home assignment itself (that is document-information-architect) and doing any edit/move/rewrite of the corpus."
facts: "7 confirmed constraints — see 'Confirmed constraints' (each sourced to a project-state-report FACT row with a locator)."
hypotheses: "none (a scope note settles or defers; unsettled beliefs stay in the state report / go to the decision register, not here)."
open_questions: "7 open decisions — see 'Open decisions' (each classified + recommended next action; 4 user-preference, 1 repo-verifiable, 2 deferred). Never 'none'."
evidence_level: "n/a (goal/scope statement, not an evidence claim); each Confirmed constraint cites the state-report row it rests on, whose ceiling is E2 (doc-only corpus, no runtime)."
next_handoff: document-information-architect
handoff_requirements: "The IA needs: the settled goal + non-goals + in/out scope below. The 7 open decisions are handed in parallel to uncertainty-and-decision-manager; of them D-1 (canonical current-status owner) and D-4 (README index scope) are BLOCKING and must be decided before canonical-home assignment. Batch-5 migration + rewriter are NOT built, so the effort ends at the document-artifact-map with an honest BLOCKED execution handoff."
status: DECIDED for settled items; the 7 OPEN items are listed separately (Open decisions)
---

# Goal / Scope / Workflow Note — `docs/skill-development/` documentation refactor

Readable with no chat context. This note frames the goal, scope, non-goals, and workflow of the documentation
refactor; it does **not** design the architecture and it changes no file. It was produced with **no human
available to interview** — nothing below was decided by a fabricated human answer; every item that needs human
preference is recorded, unresolved, in *Open decisions*.

## Goal

Give the `docs/skill-development/` governance corpus (24 files: 7 top-level governance docs, 16 `reports/**`,
1 `adr/`) a clean information architecture in which **every information-type has exactly one canonical home**,
**volatile "current status" content lives in a single owner and is referenced by pointer everywhere else**, and
the state report's enumerated staleness and contradictions have a stated cure. Concretely, success is a
target-architecture decision (produced *next*, by `document-information-architect`) that (a) confirms the
already-established canonical owners and assigns a home for the content that is currently mirrored, duplicated,
or orphaned; (b) reduces the mirrored current-status surfaces, the OQ-1..5 mirror, and the duplicated catalogs
to pointer-only against their single owner; and (c) records how each of the **5 STALE claims (C1-C5)**, **3
orphan/index gaps (Or1-Or3)**, and **3 overlap candidates (O1-O3)** will be resolved — all **without this
front-end step editing, moving, merging, or rewriting any file**. This note settles that goal and its
boundaries and hands the design work downstream; it does not perform the design.

## In scope (of the documentation-refactor this chain serves)

- One canonical home per information-type across `docs/skill-development/**` (24 files) — confirming the
  FACT-established owners (CC-2) and assigning homes for the currently mirrored / duplicated / orphaned content.
- Reducing volatile "current status" to a **single canonical owner + pointers elsewhere**, per the prescription
  in `system-architecture.md:198` (CC-3).
- A **resolution plan** (what becomes canonical, what becomes a pointer, what gets a dated supersede note) for
  the enumerated defects: 5 STALE claims (C1-C5), 3 orphan/index gaps (Or1-Or3), 3 overlap candidates (O1-O3)
  (CC-6) — delivered as the IA's `document-artifact-map`, not as edits here.
- Framing this effort (this note) and handing the target-architecture design to `document-information-architect`,
  with the *Open decisions* handed in parallel to the decision register.

## Non-goals (explicit — load-bearing, so downstream does not silently re-expand scope)

- **NOT moving, editing, merging, deleting, or rewriting any file.** The entire front-end (forensics → state →
  this note → IA) is **read-only**; the actual moves are `content-canonicalization-and-migration` and the prose
  edits are `technical-document-rewriter` — both **Batch 5, not built** (CC-5-adjacent; workflow below).
- **NOT deciding the human-preference items now** — canonical current-status owner, v0.2-report deprecation,
  ADR annotation, README index scope, and the OQ-1..5 lifecycle are *Open decisions* (D-1..D-5) for the user /
  decision register. This note records them; it does not resolve them.
- **NOT designing the target information architecture / canonical-home assignment in THIS note** — that is
  `document-information-architect`'s downstream job. This note only frames the goal/scope it will work to (the
  state report already scopes this out at `project-state-report.md:9`).
- **NOT verifying, re-deriving, or running anything.** No eval-result JSON verification, no `run_checks.py`
  execution, no full-read of the 3 large report bodies, no currency-audit of the out-of-scope canonical files
  (`upstream-method-matrix.md`, `hard-fail.md`, `rubric.md`, `canonical-source-map.md`). Those are PSR
  UNKNOWNs U2-U5 / HYPOTHESES H-a..H-c and are out of scope for a *structural* doc refactor. The corpus is
  doc-only (CC-1) — there is no runtime to validate.
- **NOT re-doing forensics or state reconstruction** — those upstream steps are complete (`inventory-report.md`
  + `project-state-report.md`).
- **NOT treating the honest forward/dangling refs** (ADR-DQE-002, HF-REPRO, `reproducibility_contract_check.py`,
  the 61-slot matrix) **as defects** — they are explicitly DEFERRED / not-built, not broken promises (CC-5).

> **Single most important non-goal:** *NOT mutating any file and NOT deciding the human-preference items now.*
> Both keep the `document-information-architect` from silently re-expanding a read-only planning step into
> execution or into deciding what only the user can decide.

## Intended workflow (dev–test–experiment)

This is a **doc-only corpus**: there is no code to run and no experiment to log. "Dev" = producing governance
artifacts; "test" = the harness checkers run over each artifact (`frontmatter_check` + `status_vocab_check` are
HARD, `interface_check` is ADVISORY, run with `--advisory-is-hard` for the Batch-2.5 chains); "experiment" =
n/a; verification is against doc content + filesystem existence, ceiling **E2** (CC-1).

Chain (build status marked so a fresh reader knows where execution stops):

1. `workspace-forensics-and-inventory` → `inventory-report.md` — **done (upstream).**
2. `project-state-reconstructor` → `project-state-report.md` — **done; this note's sole input.**
3. `goal-scope-and-workflow-elicitor` → **this** `goal-scope-note.md` — **current step.**
4. `document-information-architect` → `document-artifact-map` — **next.** Consumes this note + the state report;
   designs the canonical-home assignment and the per-defect resolution mapping. D-1 and D-4 must be decided first.
5. `content-canonicalization-and-migration` (file moves) + `technical-document-rewriter` (prose) —
   **Batch 5, NOT built → honest BLOCKED handoff.** The artifact-map is produced and parked here; no file is
   actually moved or rewritten until this capability exists or a manual migration is authorized (D-7).
6. `documentation-quality-evaluator` (v0.4.1, advisory/profile-scoped-frozen) → **advisory** final pass.

Open decisions are emitted in parallel to `uncertainty-and-decision-manager` (the decision register).

## Confirmed constraints

Each row is sourced to a FACT (or FACT-with-noted-staleness) row in the state report.

| id | constraint | source (project-state-report.md) |
|---|---|---|
| CC-1 | Doc-only corpus, **no executable target** — "validation" is against doc content + filesystem existence, not runtime; evidence ceiling **E2**. | "What runs (FACT)" (`:42-50`) + `evidence_level` (`:13`) |
| CC-2 | Canonical owners are already FACT-established: architecture = `system-architecture.md`; per-skill version/status = `skills-registry.yaml`; roadmap = `creation-roadmap.md`; ADR = `adr/ADR-DQE-001`; observability = `reports/runlog.md`. The IA **builds on these, does not reassign them.** | "Corpus facts (confirmed)" (`:87-96`) |
| CC-3 | The prescribed canonical home for "current dev status" is a `status/`-dir or a **standing PSR state report** (`system-architecture.md:198`) — no single such owner exists yet (feeds D-1). | C6 (`:78`) |
| CC-4 | OQ-1..OQ-5 are mirrored across 3 surfaces **intentionally + self-declaredly**; `system-architecture.md §13` is canonical. Mirror is a labeled convention, not a contradiction. | O3 (`:81`) |
| CC-5 | Forward refs (ADR-DQE-002 / HF-REPRO / `reproducibility_contract_check.py` / 61-slot matrix) are **explicitly NOT built / DEFERRED** — honest dangling refs, not defects to fix. | "Corpus facts" (`:96`) |
| CC-6 | The defect surface is **bounded and located**: 5 STALE claims (C1-C5), 3 orphan/index gaps (Or1-Or3), 3 overlap candidates (O1-O3) — each with a `file:line` locator. Scope of "resolve staleness" is these, not an open hunt. | ledger + STALE + orphan tables (`:71-83`, `:102-104`, `:108-116`) |
| CC-7 | Project phase is **settled FACT** (Batch 0+1 complete; Batch 2 = 4/4 built + light-passed; Phase E deferred). So the roadmap's STALE §0/§1 progress-tracker (C2) is a *fix target*; the phase itself is not in question. | "Real progress" (`:61`) + C2 (`:74`, `:112`) |

## Open decisions (→ `uncertainty-and-decision-manager` / decision register)

Carried forward from the state report's 5 ASK-HUMAN items + the load-bearing scope ambiguities. **None is
decided here.** Classifications: `user-preference` (only the user can choose), `repo-verifiable` (resolve by
looking at the repo — no human needed), `deferred` (frozen for now).

| id | question (PSR ref) | classification | recommended next action (not a decision) |
|---|---|---|---|
| **D-1** | **Which surface is the canonical "current project status" owner** — `README.md §0`, the `…freeze-and-batch2-entry…` doc, `skills-registry.yaml meta`, or a standing PSR state report? (C6 / ASK-HUMAN Q1) **BLOCKS IA.** | user-preference | Put to the user. Register the recommendation that the standing PSR state report be the owner (per `system-architecture.md:198`, CC-3), with the other surfaces reduced to pointers. Do **not** assign a canonical home until decided. |
| **D-2** | **Deprecate the v0.2 quality report** (`quality-report-…图.md`) now that v0.3 supersedes it? (C3 / ASK-HUMAN Q2) | user-preference | Put to the user with the evidence that it is superseded (C3) *and* an orphan (Or1); recommend `document_lifecycle: DEPRECATED` + pointer to v0.3. Do not re-label it here. |
| **D-3** | **Annotate `ADR-DQE-001` Status** with a dated "superseded-in-part by the 2026-08-05 advisory freeze" note? (C4 / ASK-HUMAN Q3) | user-preference | Put to the user; note that Decisions 1-6 stay in force (CC-2/C4) and only the forward provisional-gate framing is stale. Do not edit the ADR here. |
| **D-4** | **README index scope** — extend the Deliverables index to `adr/` + the `dqe-v0.4*` / `batch2-*` reports, or is `reports/` a deliberately un-indexed dated append area? (Or2/Or3 / ASK-HUMAN Q4) **BLOCKS IA.** | user-preference | Put to the user; this determines whether the ~15 un-indexed reports are "orphans to wire up" or "intentional append area". Required before canonical-home assignment. |
| **D-5** | **OQ-1..OQ-5 lifecycle** — keep OPEN/DEFERRED, owned by user/project? (ASK-HUMAN Q5) | deferred | Carry forward as OPEN/DEFERRED (arch §13 canonical, CC-4); do **not** silently close. Owner: user/project. |
| **D-6** | **Duplication drift** — has `quality-control-plan.md §1.1` drifted from `evals/skills/harness/hard-fail.md` (O1/U1), and is `dqe-blind-matrix §4` a true duplicate of the standalone defect-ledger or a historical snapshot (O2/U6)? | repo-verifiable | Resolve by **diff, no human needed**, before canonical-home assignment: if drifted, the canonical file wins and the copy becomes a pointer; if a dated snapshot, keep as-is and mark it a snapshot. Feeds the IA's dedup decisions for O1/O2. |
| **D-7** | **Execution boundary** — does this effort stop at the `document-artifact-map`, or proceed to actually move/rewrite files? (scope ambiguity; Batch-5 tooling not built, CC-5/workflow) | deferred | Effort ends at the artifact-map + an honest BLOCKED execution handoff, because `content-canonicalization-and-migration` + `technical-document-rewriter` are not built. Whether to bridge the gap by a user-authorized manual migration is deferred to the user / Batch-5 delivery. |
