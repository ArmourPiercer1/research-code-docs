---
name: content-canonicalization-and-migration
description: Turn a document-information-architect's split/link plan into a DRY-RUN migration map — a canonicalization plan, a per-source disposition (migration) map, a supersession map for retired docs, a link-update plan, and a rollback plan — so a messy doc corpus CAN be restructured without any file being moved, deleted, or overwritten yet. This is a PLANNING skill: v0 is read-only w.r.t. the corpus and writes only NEW plan files. It never executes the move; every source section gets exactly one primary disposition (or an explicit DEFERRED), every retired doc gets a supersession (never a silent delete), and every unresolved decision from upstream is preserved, not decided. NOT for designing the target architecture (document-information-architect), rewriting prose (technical-document-rewriter), grading a doc (documentation-quality-evaluator), or recovering facts (project-state-reconstructor).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only until its Batch-5 evals pass; v0 = dry-run/new-files-only)
generated_by_skill: manual authoring (Batch 5, doc-refactor executor #1; per directive Batch3后续_首个闭环垂直切片与分层测试节奏计划.md §6.1)
source_commit: 07b5306
source_documents:
  - references/agent-skills/skills/documentation-and-adrs/SKILL.md (MIT — supersede-don't-delete lifecycle; canonical home; method-borrow)
  - references/agent-skills/skills/source-driven-development/SKILL.md (MIT — checkable locator: every source/target is a real path; method-borrow)
  - docs/skill-development/creation-roadmap.md §5 (Batch-5 workspace-migration-planner: dry-run first)
  - docs/skill-development/system-architecture.md §3.3 (documentation-refactor chain, executor tail)
  - references/interfaces/document-artifact-map.schema.md + references/interfaces/migration-map.schema.md
  - references/documentation-methodology/upstream-method-matrix.md §2.10
last_verified: 2026-08-06
-->

# Content Canonicalization & Migration (v0 · dry-run planner)

> **Experimental · manual/orchestrator-only · v0 DRY-RUN.** This skill produces a **migration map**; it does
> **not** execute the migration. In v0 it is `read_only: true` w.r.t. the corpus, `creates_new_files: true`,
> and `may_move / may_delete / may_overwrite = false`. It converts the `document-information-architect`'s
> split/link plan into an executable-later, approval-gated map. Supersede-don't-delete lifecycle adapted from
> `documentation-and-adrs` (MIT); checkable-locator discipline from `source-driven-development` (MIT); both
> attributed in `upstream-method-matrix.md` §2.10.

## Purpose

Take the design hand-off (`document-artifact-map` + `canonical-source-map` + `open-decisions` + the PSR
`project-state-report`) and turn its split/link plan into a concrete, **checkable, dry-run** migration plan:

1. **Canonicalization plan** — for each information-type, the single canonical home it will live in.
2. **Migration map** — for each existing source section, exactly **one primary disposition**
   (`move-to` / `split-and-pointer` / `keep-in-place` / `merge-into` / `annotate` / `DEFERRED`) with its target.
3. **Supersession map** — for each doc that is being retired/replaced, the replacing doc + a `supersedes` /
   `superseded_by` record — never a silent delete.
4. **Link-update plan** — every cross-link/pointer that must change so the fact is stored **once**.
5. **Rollback plan** — how to revert (in v0, since nothing executes, revert = discard the plan + candidate dir).

## Trigger conditions

Engage when: a `document-artifact-map` (a target IA + a split plan) exists and someone needs the **executable
migration plan** to realize it — typically the `documentation-refactor` control flow calling the executor tail
after IA. Also engage on "plan how to actually reorganize/move these docs into the new layout (but don't do it
yet)."

## Do-not-trigger conditions (route instead)

- **Design** the target architecture / decide canonical homes from scratch → `document-information-architect`
  (this skill consumes its output; it does not redo the design).
- **Rewrite** the prose / write the new doc bodies → `technical-document-rewriter`.
- **Grade** a doc → `documentation-quality-evaluator`.
- Recover **what is FACT vs STALE** → `project-state-reconstructor`.
- Actually **execute** moves/deletes on disk → NOT in v0. That requires a separate, explicit user
  apply-approval; without it the plan stays a dry-run and the flow reports `BLOCKED:explicit-write-approval-required`.

## Inputs (consume from disk; no chat dependence)

- `document-artifact-map.md` (the split/link plan §4 + target doc-set §3) — **primary input.**
- `canonical-source-map.md` (info-type → canonical home).
- `open-decisions.md` (the unresolved D-*/IA-* items — **carried, never decided here**).
- `project-state-report.md` (FACT/STALE — so a disposition never rests on a STALE claim).

## Workflow

1. **Load the design hand-off** and confirm every source section named in the artifact-map §4 split plan.
2. **Canonicalization plan** — restate the one-canonical-home-per-info-type table (borrowed from
   `canonical-source-map`; do not reassign a FACT home).
3. **Per-source disposition** — for each source section, assign exactly **one** primary disposition + target.
   A disposition whose target is a home BLOCKED on an open decision (e.g. every volatile-status split blocked on
   D-1's status owner) is marked **`DEFERRED (blocked_by: D-1)`** — never given a silently-picked target.
4. **Supersession map** — any doc slated for retirement gets a `superseded_by` pointer + reason; the old doc is
   marked `DEPRECATED` (a lifecycle annotation the rewriter/human applies later), **not** deleted.
5. **Link-update plan** — list every pointer that changes so each fact is stored once.
6. **Rollback plan** — record how to revert; in v0 this is "discard the candidate output + this map" (nothing
   was executed).
7. **Emit the machine block** (`migration_map:` fenced YAML, checked by `migration_map_check.py`) + the frozen
   handoff header (`artifact_type: migration-map`).

## Core discipline (the gates that keep v0 safe — directive §6.1)

- **Dry-run only.** `may_move = may_delete = may_overwrite = false`. The map is a plan; it executes nothing.
- **No silent attribution.** Every source section has exactly one primary disposition **or** an explicit
  `DEFERRED` with a `blocked_by`. Never invent a canonical home for a section whose home is unresolved.
- **Provisional stays provisional.** A provisional/BLOCKED home from IA is **not** upgraded to decided.
- **Unresolved decisions preserved.** Every open decision from `open-decisions.md` that gates a disposition is
  carried into `migration_map.unresolved_decisions` and referenced by the blocked dispositions — none dropped.
- **Supersede, never delete.** A retired doc gets a supersession record, not a disappearance.
- **No overwrite.** Every target path differs from its source path; the map creates new homes / candidate files.

## Must NOT

- **Not** move / rename / delete / overwrite any corpus file (v0 permissions above).
- **Not** decide an `open-decisions.md` item (D-1, D-4, D-6, …) — carry it, recommend at most, never pick.
- **Not** upgrade a provisional/STALE home to a settled one.
- **Not** claim the migration is done — the map's `next_handoff` is the rewriter (candidate output), and the
  execution itself remains `BLOCKED:explicit-write-approval-required` until a user authorizes apply-mode.

## Outputs / Write-scope

- **`migration-map.md`** — a NEW file (default under a results/status dir), carrying the frozen handoff header
  (`artifact_type: migration-map`) + the `migration_map:` machine block. Sections: Canonicalization plan ·
  Per-source disposition (migration) map · Supersession map · Link-update plan · Rollback plan · Carried open
  decisions · Coverage note. Template: `references/templates/migration-map.template.md`.
- **Write-scope:** `read_only: true` w.r.t. the corpus; `creates_new_files: true`; never moves/deletes/overwrites.

## Handoff rules

- To `technical-document-rewriter` (writes the candidate target docs from the disposition map, new files only) →
  `documentation-quality-evaluator` (advisory) → `living-design-maintainer`.
- Execution of the moves is a **separate, explicit user apply-approval**; until then the flow stops at
  `BLOCKED:explicit-write-approval-required` (directive §8.6).

## Failure modes

- **A source section has no clear home** → `DEFERRED (blocked_by: <decision>)`, raised, not guessed.
- **Two sources claim the same canonical home for one info-type** → one primary + the other becomes a
  pointer/supersession; if genuinely ambiguous, `DEFERRED` + open decision.
- **Upstream open decision unresolved (D-1 status owner)** → all dispositions that need that pointer target are
  `DEFERRED`; the map is still complete (nothing silently assigned).

## References to load

- `references/interfaces/migration-map.schema.md` + `references/interfaces/document-artifact-map.schema.md`.
- `evals/skills/harness/hard-fail.md` §HF-13/§HF-14b (the disease the migration realizes the cure for).
- `references/agent-skills/skills/documentation-and-adrs/SKILL.md` (MIT — supersede-don't-delete). Matrix §2.10.

## Scripts to run

- `evals/skills/harness/checkers/migration_map_check.py <migration-map>` — dry-run flags false, one primary
  disposition per source, target ≠ source, rollback present, unresolved decisions preserved.
- `evals/skills/harness/checkers/interface_check.py <migration-map>` — frozen handoff header.
- `evals/skills/harness/checkers/run_checks.py <run-dir>` — front-matter + status vocab.
