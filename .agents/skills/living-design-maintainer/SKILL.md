---
name: living-design-maintainer
description: "Given a change event (e.g. a set of accepted candidate documents) plus the canonical-source-map and decision register, work out the MAINTENANCE IMPACT — which canonical artifacts a change touches, what stable-design / dynamic-state / experiment-fact / session-context boundaries it crosses — and emit a maintenance-impact report, a set of PROPOSED canonical updates, a stale-reference list, and a verification checklist. v0 is read-only w.r.t. the canonical docs and creates new proposal files only: it never edits a canonical document, never auto-accepts a candidate as canonical, and never auto-publishes. NOT for grading a doc (documentation-quality-evaluator), designing architecture (document-information-architect), planning a migration (content-canonicalization-and-migration), or writing candidate prose (technical-document-rewriter)."
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only until its Batch-5 evals pass; v0 = read-only + proposal-only)
generated_by_skill: manual authoring (Batch 5, doc-refactor executor #3; per directive Batch3后续_首个闭环垂直切片与分层测试节奏计划.md §6.3)
source_commit: 07b5306
source_documents:
  - references/agent-skills/skills/documentation-and-adrs/SKILL.md (MIT — canonical home per role; supersede-don't-edit; method-borrow)
  - docs/研究软件文档Skills系统_设计与创建指南.md §17 (keep stable-design / dynamic-state / evidence / session separate — the maintenance principle)
  - references/interfaces/rewrite-provenance-report.schema.md + references/interfaces/maintenance-impact-report.schema.md
  - evals/skills/harness/canonical-source-map.md (info-type -> canonical source; the single-source-of-truth table)
  - docs/skill-development/system-architecture.md §3.3 (documentation-refactor chain, maintenance stage)
  - references/documentation-methodology/upstream-method-matrix.md §2.12
last_verified: 2026-08-06
-->

# Living Design Maintainer (v0 · proposal only)

> **Experimental · manual/orchestrator-only · v0 PROPOSAL-ONLY.** This skill decides *what a change implies for
> the canonical docs* and **proposes** updates; it does **not** edit any canonical document, accept a candidate,
> or publish (`read_only: true` w.r.t. canonical docs, `creates_new_files: true`, `may_overwrite = false`,
> `auto_accept_candidates = auto_publish = false`). Canonical-home + supersede-don't-edit discipline from
> `documentation-and-adrs` (MIT); the stable/dynamic/evidence/session separation principle from the design guide
> §17. Attributed in `upstream-method-matrix.md` §2.12.

## Purpose

Keep a living design coherent under change **without silently mutating it**. Given a **change event** (typically
a set of accepted candidate docs from a rewrite, or a decision/state change) + the `canonical-source-map` + the
`decision-register`, produce:

1. a **maintenance-impact report** — which canonical artifacts the change touches, and which
   stable-design / dynamic-state / experiment-fact / session-context boundaries it crosses;
2. **proposed canonical updates** — each pointing at a **known canonical home**, as a *proposal*, not an edit;
3. a **stale-reference list** — pointers/links that a change makes stale;
4. a **verification checklist** — what a human must confirm before any update is applied.

## Trigger conditions

Engage when a change has happened (or is proposed) and someone needs to know **what it means for the canonical
documentation** — usually the `documentation-refactor` control flow calling the maintenance stage after a
rewrite + DQE-advisory. Also engage on "a decision/experiment/state just changed — what docs go stale, and what
should be updated?"

## Do-not-trigger conditions (route instead)

- **Grade** a doc → `documentation-quality-evaluator`.
- **Design** the target architecture → `document-information-architect`.
- **Plan** the migration / **write** the candidate docs → `content-canonicalization-and-migration` /
  `technical-document-rewriter`.
- **Actually edit / publish** the canonical docs → NOT in v0; that needs explicit user apply-approval.

## Inputs (consume from disk; no chat dependence)

- The **change event** — e.g. the accepted `candidate-doc-set/` + its `rewrite-provenance-report`, or a
  decision/state change record.
- `canonical-source-map.md` (info-type → canonical home — the single-source-of-truth table).
- `decision-register.md` (which items are DECIDED vs OPEN — a proposal never treats OPEN as settled).

## Workflow

1. **Locate the canonical homes touched.** Map the change onto the `canonical-source-map`; list which canonical
   artifacts (architecture, roadmap, registry, ADR, runlog, status owner, …) the change implicates.
2. **Classify by lifecycle.** For each implicated home, mark whether the change carries **stable-design**,
   **dynamic-state**, **experiment-fact**, or **session-context** content — and enforce the boundary: volatile
   state is proposed as a pointer, **never** copied into a stable doc (the HF-14b rule).
3. **Propose updates.** For each home, propose the update as a *proposal* (info-type → canonical → action),
   never an edit. A candidate that is not yet **accepted** may not be proposed as canonical.
4. **Stale references.** List every pointer/link the change makes stale (so nothing points at a superseded home).
5. **Verification checklist.** State what a human must confirm before apply (which candidates are accepted, which
   open decisions must first be resolved, which pointers to re-point).
6. **Emit** the `maintenance-impact-report.md` (`artifact_type: maintenance-impact-report`, `maintenance_impact:`
   machine block).

## Core discipline (the gates that keep v0 safe — directive §6.3)

- **Proposal only.** `may_overwrite = false`, `auto_accept_candidates = false`, `auto_publish = false`. No
  canonical doc is edited; nothing is published.
- **Every proposed update points at a known canonical type/home** (from the canonical-source-map) — not at a
  candidate, a handoff artifact, or a transient session note.
- **Single source of truth.** No information-type is proposed into two canonical homes; volatile facts are never
  proposed into a stable doc.
- **Candidate ≠ canonical.** A candidate document is not treated as canonical until a human accepts it; the
  maintainer records `approved: false` and proposes acceptance, it does not perform it.
- **Handoff ≠ canonical source.** A session `handoff` / transient note is never treated as a source of truth.

## Must NOT

- **Not** edit / overwrite / publish any canonical document (v0 permissions).
- **Not** auto-accept a candidate as canonical; **not** auto-publish.
- **Not** propose copying volatile state into a stable doc; **not** create a second home for one info-type.
- **Not** treat a `handoff` / session note as canonical.

## Outputs / Write-scope

- **`maintenance-impact-report.md`** — a NEW proposal file, frozen handoff header
  (`artifact_type: maintenance-impact-report`) + `maintenance_impact:` machine block. Sections: Impacted
  canonical homes · Lifecycle classification · Proposed updates (proposal only) · Stale-reference list ·
  Verification checklist · Coverage note. Template: `references/templates/maintenance-impact-report.template.md`.
- **Write-scope:** `read_only: true` w.r.t. canonical docs; `creates_new_files: true`; `may_overwrite = false`.

## Handoff rules

- To a **human / orchestrator** for review + apply-approval. Applying the proposed updates (editing the canonical
  docs) is a **separate, explicit user apply-approval**; until then the report is a proposal only.

## Failure modes

- **A change touches an info-type with no canonical home yet** (e.g. status owner BLOCKED on D-1) → propose the
  home as blocked on that decision; do not invent one.
- **A candidate is not yet accepted** → propose acceptance + record `approved: false`; do not mark it canonical.
- **Volatile content wants to land in a stable doc** → propose a pointer instead; flag the boundary.

## References to load

- `references/interfaces/maintenance-impact-report.schema.md` + `evals/skills/harness/canonical-source-map.md`.
- `references/agent-skills/skills/documentation-and-adrs/SKILL.md` (MIT — canonical home; supersede). Matrix §2.12.

## Scripts to run

- `evals/skills/harness/checkers/maintenance_impact_check.py <report>` — every proposed update points at a known
  canonical type, no volatile-into-stable, single source of truth, no unapproved candidate marked canonical.
- `evals/skills/harness/checkers/interface_check.py <report>` + `run_checks.py <report>`.
