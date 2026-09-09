---
name: technical-document-rewriter
description: Write the CANDIDATE rewritten documents that a migration-map calls for — new, restructured doc bodies produced into an ISOLATED candidate output directory, never overwriting the originals — plus a rewrite-provenance report (each candidate mapped to its source ranges) and an unresolved-content list. This is the executor that turns a dry-run migration plan into concrete draft documents WITHOUT touching the source corpus. v0 creates new files only (may_overwrite/move/delete = false). It never upgrades OPEN/HYPOTHESIS to FACT, never silently drops source content, and preserves conflicts rather than adjudicating them. NOT for designing the architecture (document-information-architect), planning the migration (content-canonicalization-and-migration), grading the result (documentation-quality-evaluator), or recovering facts (project-state-reconstructor).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only until its Batch-5 evals pass; v0 = candidate-output/new-files-only)
generated_by_skill: manual authoring (Batch 5, doc-refactor executor #2; per directive Batch3后续_首个闭环垂直切片与分层测试节奏计划.md §6.2)
source_commit: 07b5306
source_documents:
  - references/agent-skills/skills/source-driven-development/SKILL.md (MIT — checkable locator; never upgrade an unverified claim; method-borrow)
  - references/research-paper-writing-skills/references/paper-review.md (MIT — claim disposition: weaken-or-remove, never invent support; method-borrow)
  - references/agent-skills/skills/doubt-driven-development/SKILL.md (MIT — preserve the doubt/conflict, do not adjudicate; method-borrow)
  - references/interfaces/migration-map.schema.md + references/interfaces/rewrite-provenance-report.schema.md
  - docs/skill-development/system-architecture.md §3.3 (documentation-refactor chain, rewrite stage)
  - references/documentation-methodology/upstream-method-matrix.md §2.11
last_verified: 2026-08-06
-->

# Technical Document Rewriter (v0 · candidate output only)

> **Experimental · manual/orchestrator-only · v0 CANDIDATE-OUTPUT.** This skill writes **new draft documents
> into an isolated candidate directory**; it does **not** overwrite, move, or delete the source corpus
> (`creates_new_files: true`, `may_overwrite/move/delete = false`). It realizes a `migration-map`'s dispositions
> as concrete prose. Checkable-locator + no-unverified-upgrade discipline from `source-driven-development` (MIT);
> weaken-or-remove-don't-invent from `paper-review` (MIT); preserve-the-conflict from `doubt-driven-development`
> (MIT). Attributed in `upstream-method-matrix.md` §2.11.

## Purpose

Turn a `migration-map` (per-source dispositions) + the selected source documents + the PSR `project-state-report`
+ the `decision-register` into **candidate rewritten documents** — the actual restructured doc bodies — written
to a **separate candidate output directory**, together with:

1. a **rewrite-provenance report** mapping every candidate doc (and every significant delete/merge/rewrite) back
   to its **source range(s)**, and
2. an **unresolved-content list** — source content that could not be placed, conflicts left standing, and any
   claim whose evidence does not support a stronger wording.

The originals are never touched; the result is a set of drafts a human (and DQE-advisory) can review before any
apply-mode migration is authorized.

## Trigger conditions

Engage when a `migration-map` exists and someone needs the **candidate new documents** written from it — usually
the `documentation-refactor` control flow calling the rewrite stage after canonicalization/migration. Also
engage on "write the restructured version of these docs into new files (don't overwrite the originals)."

## Do-not-trigger conditions (route instead)

- **Design** the target doc-set / canonical homes → `document-information-architect`.
- **Plan** which section goes where (the migration map) → `content-canonicalization-and-migration`.
- **Grade** the result → `documentation-quality-evaluator` (this skill writes; it does not judge).
- Recover **what is FACT vs claim** → `project-state-reconstructor` (the rewriter consumes it; never re-verifies).
- **Overwrite / replace the live documents** → NOT in v0; requires explicit user apply-approval.

## Inputs (consume from disk; no chat dependence)

- `migration-map.md` (the disposition plan — **which source range → which target**) — primary input.
- The **selected source documents** it names (read-only).
- `project-state-report.md` (FACT/UNKNOWN/STALE — so no claim is strengthened past its evidence).
- `decision-register.md` (DECIDED/HYPOTHESIS/OPEN — so OPEN stays OPEN in the rewrite).

## Workflow

1. **Hash the sources.** Record each source file's `sha256` at read time (the tamper baseline — a candidate run
   never changes a source, and `rewrite_provenance_check.py` re-verifies the hash).
2. **Honor the dispositions.** For each `migration-map` disposition that is **not** `DEFERRED`, write the target
   content into the candidate directory. A `DEFERRED` disposition is **not** rewritten (its target is blocked on
   an open decision) — it is listed in unresolved-content instead.
3. **Rewrite faithfully.** Restructure for the target doc's single responsibility; **carry facts at their PSR
   status** (a claim marked UNKNOWN stays hedged; an OPEN decision stays OPEN; a STALE value is replaced by a
   pointer, not a freshly-invented number).
4. **Trace every change.** Every candidate doc, and every significant delete/merge/reword, maps to a source
   range in the provenance report. Nothing from a source is dropped silently — if it has no home, it goes to
   unresolved-content.
5. **Preserve conflicts.** Where two sources disagree, the candidate surfaces the conflict (both, labeled); the
   rewriter does **not** pick a winner (that is a decision for the register / human).
6. **Emit** the candidate docs (each with traceability front-matter) + the `rewrite-provenance-report.md`
   (`artifact_type: rewrite-provenance-report`, `rewrite_provenance:` machine block).

## Core discipline (the gates that keep v0 safe — directive §6.2)

- **Candidate output only.** Write to an isolated candidate directory; `may_overwrite/move/delete = false`.
  Every candidate path differs from its source path; source files are byte-for-byte unchanged (hash-verified).
- **No fact upgrade.** Never turn OPEN / HYPOTHESIS / UNKNOWN into FACT; never invent a citation or a number to
  support a stronger claim (weaken-or-remove instead).
- **No silent loss.** Every source range is either placed in a candidate doc or listed in unresolved-content.
- **Preserve conflicts.** Surface disagreements; do not adjudicate them.
- **Not COMPLETE while unresolved.** If the unresolved-content list is non-empty, the report's `completion` is
  `PARTIAL`, never `COMPLETE`.

## Must NOT

- **Not** overwrite / move / delete any source file (v0 permissions).
- **Not** fabricate facts, citations, or resolved decisions to make a doc read as "finished".
- **Not** silently delete source content; **not** mark the rewrite COMPLETE while content is unresolved.
- **Not** execute the migration or claim the docs are published — that needs explicit user apply-approval.

## Outputs / Write-scope

- **`candidate-doc-set/`** — a NEW directory of rewritten draft docs, each with traceability front-matter
  (`generated_by_skill`, `skill_version`, `source_commit`, `source_documents`, `document_lifecycle: DRAFT`).
- **`rewrite-provenance-report.md`** — frozen handoff header (`artifact_type: rewrite-provenance-report`) +
  `rewrite_provenance:` machine block (candidate↔source map, source hashes, completion, unresolved-content).
  Template: `references/templates/rewrite-provenance-report.template.md`.
- **Write-scope:** `creates_new_files: true` under the candidate dir; `may_overwrite/move/delete = false`;
  source corpus `read_only`.

## Handoff rules

- To `documentation-quality-evaluator` (advisory review of the candidate set) → `living-design-maintainer`
  (maintenance-impact of accepting them). Apply-mode (replacing the live docs) is a **separate user
  apply-approval**; until then the flow reports `BLOCKED:explicit-write-approval-required`.

## Failure modes

- **A source range has no target** → unresolved-content (never dropped); `completion: PARTIAL`.
- **A claim's evidence is weaker than the source's wording** → weaken it; do not invent support.
- **Two sources conflict** → surface both, labeled; route the choice to the decision-register.
- **A disposition is DEFERRED** → do not rewrite it; list it as blocked in unresolved-content.

## References to load

- `references/interfaces/rewrite-provenance-report.schema.md` + `references/interfaces/migration-map.schema.md`.
- `references/agent-skills/skills/source-driven-development/SKILL.md` (MIT — no unverified upgrade). Matrix §2.11.

## Scripts to run

- `evals/skills/harness/checkers/rewrite_provenance_check.py <report>` — candidate≠source, source hashes
  unchanged, provenance complete, not-COMPLETE-while-unresolved, candidate docs carry traceability front-matter.
- `evals/skills/harness/checkers/interface_check.py <report>` + `run_checks.py <candidate-dir>`.
