---
name: simplification-audit
description: Read-only SIMPLIFICATION AUDIT of a proposed change — reconstruct the verified current state (PSR), take a mechanical inventory/doc-corpus map (WFI), run deterministic repo searches for inbound references, and classify every consumer five ways (CURRENT-AUTHORITY/POINTER, HISTORICAL-PROVENANCE, FROZEN-RESULT/FIXTURE, PLAIN-TEXT-HISTORY, DEAD/STALE) to derive the minimal sufficient change set (archive vs pointer-fix vs keep) and a draft impact declaration. It answers "what does this change actually have to touch, and what can it NOT touch". Use BEFORE executing a doc/governance refactor or archive move, when a plan names concrete target files and you must know its true blast radius. NOT for executing the change (host does), NOT for verifying a finished change (focused-verification), NOT for open-ended refactoring (no dependency-graph lint is built here — classification is search-based), NOT for inventorying an unknown workspace from scratch without a change target (workspace-forensics-and-inventory).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only; Phase-2 vertical slice, 2026-09-10)
generated_by_skill: manual authoring (Phase-2 vertical slice; per research_code_docs_phase2_implementation_prompt.md §2.1 A8)
source_commit: 1dc6b8694dac60ac355b8094e61ffebde322fba0
source_documents:
  - docs/plans/active/research_code_docs_phase2_implementation_prompt.md §2.1 (A8 spec)
  - docs/plans/active/reconstruction/revised-phase2-vertical-slice.md §3 (chain: PSR → A8 → candidate → D-1 → host → A9)
  - docs/plans/active/reconstruction/phase1/target-workflow-invariants.md (I11/I12 archive discipline)
  - .agents/skills/project-state-reconstructor/SKILL.md (state recovery consumed by A8)
  - .agents/skills/workspace-forensics-and-inventory/SKILL.md (inventory/doc-corpus map consumed by A8)
last_verified: 2026-09-10
-->

# Simplification Audit

> **Experimental · manual/orchestrator-only · READ-ONLY.** Given a *proposed* change (concrete target
> files + intent), this skill answers the question that makes the change cheap and safe: **what does it
> actually have to touch, and what can it not touch?** It is the mechanical half of "simplify before
> executing": verified state (PSR) + structural map (WFI) + deterministic reference searches + a
> **five-way consumer classification**, producing a **minimal sufficient change set** and a **draft
> impact declaration**. It executes nothing; the host executes the audited set.

## Purpose

Produce a **simplification-audit report**: for every artifact the proposed change names (or that its
intent could reach), the verified current state, the complete inbound-reference census, each reference
**classified into one of five consumer classes**, and the resulting minimal change set —
`archive | fix-pointer | keep | touch-noted` — plus a draft canonical-impact declaration
(`canonical_owners` with `impact: updated | no_impact` + justification). The audit's discipline is that
**classification comes from search evidence, not from memory of the repo** — an inbound reference is
"known" only when the grep/glob that found it is cited.

## Trigger conditions

Engage when:
- A **planned change names concrete target files** (an archive move, a canonical-owner rewrite, a
  pointer re-pointing) and its blast radius is not yet known — "audit what touching X actually breaks".
- The **Phase-2 vertical slice** (or any later refactor) needs the pre-change state recorded with
  evidence before the host implements the candidate change.
- A plan's claim about inbound references ("only one reference at Y:9") must be **recomputed** against
  the current repo state instead of trusted.

## Do-not-trigger conditions

- The change is **already implemented** and needs checking → `focused-verification` (A9). A8 is pre-change.
- The workspace is **unknown and there is no change target** → `workspace-forensics-and-inventory` first
  (A8 *consumes* its map; it does not replace a from-scratch inventory).
- The question is **open-ended** ("what could we delete?") with no named targets → this is a scoping
  discussion, not an audit; name the targets first.
- **Building a dependency-graph lint** is requested → explicitly out of scope for A8 (Phase-2 minimum
  checker set; see prompt §2.1). Classification here is search-based and cited per reference.

## Inputs

- `change_target` — the proposed change: named file(s) + one-line intent ("archive the VOID
  creation-roadmap and re-point inbound references").
- `root` — repo root (defaults to cwd).
- `base` — optional base commit for state recovery (defaults to HEAD).
- An existing WFI inventory report, if one exists (otherwise A8 runs the mechanical half itself).

## Context budget

Build the map **shallow-first**: the target file(s) in full, their directory, then search-driven reads
only. Keep working context under **~2,000 focused lines**; if approaching **~5,000**, stop and summarize.
`whole_repo_allowed: false` for *reading* — but **searches are repo-wide by design**: the census is the
point, and a census that skipped a subtree is a coverage gap to declare, not a silent success.

## Workflow

1. **State recovery (PSR half).** Establish the verified current state of the target artifact(s):
   tracked vs untracked, VOID/SUPERSEDED banners, the actual governing document, and the claims a
   README/status doc makes about it. Tag each fact FACT / CANDIDATE / **UNKNOWN** with its locator
   (file:line or command). PSR's verified facts only; no "should be" claims.
2. **Mechanical map (WFI half).** Take (or run) the WFI inventory / doc-corpus map for the affected
   subtree: where the artifact sits, what the directory's role is, which docs are frozen mirrors or
   fixtures vs live plans. The map is structural; it does not decide consumer class.
3. **Deterministic reference census.** Repo-wide, **ignoring nothing by default** (state the ignore
   list if any — e.g. `.venv/`, `node_modules/`):
   - `grep -rn "<artifact basename>"` and the artifact's distinctive title/anchor strings;
   - `git ls-files` to separate tracked from untracked hits (untracked planning state is classified,
     not deleted);
   - record **every** hit as `file:line → matched string`. The census table is the audit's evidence
     base; an uncited reference does not exist for this skill.
4. **Classify every reference (five-way).** Each census row gets exactly one class:
   - **CURRENT-AUTHORITY/POINTER** — live text that points at the artifact as a source of truth or
     current direction (a `source_documents:` entry, a "see §N" pointer, an index row). These are the
     rows the change must re-point or fix.
   - **HISTORICAL-PROVENANCE** — changelogs, reports, and freeze snapshots that *record that the
     artifact existed / was used then*. Keep; do not rewrite history for a move (annotate at most).
   - **FROZEN-RESULT/FIXTURE** — files under `evals/skills/results/**`, `tests/**`, frozen mirrors
     (`docs/reconstruction-external-review/**`), or any artifact with a recorded hash/sha256. Never
     edit; cite as frozen.
   - **PLAIN-TEXT HISTORY** — prose that mentions the artifact in passing (session notes, narrative
     paragraphs) without a link/anchor that would break. Keep; no action.
   - **DEAD/STALE** — a reference that is already wrong or points at superseded content; the change
     should note it (or fix it if it is cheap and in-scope), flagged with the defect class.
   A row that fits two classes: record the primary class + the competing one in the notes column; the
   host decides. **The old claim is not the census** — a plan may say "one inbound reference at Y:9";
   the census recomputes it and the audit records the delta.
5. **Derive the minimal sufficient change set.** From the classification:
   - CURRENT-AUTHORITY/POINTER rows → `fix-pointer` (each row = one planned edit, with the intended
     replacement text);
   - the target artifact itself → `archive` (move under `docs/plans/archived/` + keep banner) or
     `keep` (with why);
   - DEAD/STALE rows → `touch-noted` (recorded, not necessarily edited);
   - everything else → explicitly `not-touched` **with the class that justified leaving it**.
   The output set must be *minimal*: any row the host could skip without breaking a live reference is
   out of scope.
6. **Draft the impact declaration.** Emit `impact-declaration.yaml` (draft) in the change's working
   folder: `changed_paths` (the full minimal set), `canonical_owners` (each File-3 owner touched or
   claimed untouched, with `impact:` and `justification:` for every `no_impact`). This is the contract
   A9 later verifies.
7. **Assemble the report** with the census table, classification, minimal set, impact draft, and a
   **coverage note** (subtrees searched, ignores, UNKNOWNs — e.g. references in untracked planning
   docs that the change intentionally does not track yet).

## Classification discipline (the gates that keep this skill in its lane)

- **Search-evidence only.** Every classified reference cites the command + `file:line` that found it.
  No memory, no plan-text. The plan's reference count is an *input to recompute*, never a result.
- **Five-way, exactly one primary class per row.** Mixed roles go in a notes column, not a sixth class.
- **Frozen is frozen.** A FROZEN-RESULT/FIXTURE row is never in the change set, no matter how stale it
  looks — it is evidence, not a target (hash-recorded files are doubly frozen).
- **Untracked is classified, not deleted.** Planning-state files under untracked dirs (e.g.
  `docs/plans/`) are census rows; this skill never deletes, moves, or edits any file (read-only).
- **UNKNOWN is a result.** A reference whose class cannot be settled from search evidence is recorded
  UNKNOWN with the missing evidence, not guessed.
- **Minimal, not maximal.** The change set is what live references force; anything extra is scope
  creep for a later change to own.

## Quality gates (on this skill's own output)

- Every census row is cited (`file:line` + matched string); the report states its search commands and
  ignore list; a **coverage note** names what was NOT searched and why.
- Every reference has exactly one primary class (or an explicit UNKNOWN with the missing evidence).
- The plan's prior claim about references (if any) is explicitly recomputed and the delta recorded.
- The minimal change set contains **only** CURRENT-AUTHORITY/POINTER fixes, the target's own
  archive/keep decision, and noted DEAD/STALE rows — and names what it deliberately does NOT touch.
- The report carries traceability front-matter (or fails its own HF-9) and **modifies nothing** in the
  target tree (the report + impact draft are new files in the change's own working folder).

## Outputs

- `simplification-audit-report.md` — a **new** file in the change's working folder (e.g.
  `docs/plans/active/reconstruction/phase2/`). Sections: Target & intent · Verified state (PSR facts,
  tagged) · Structural map (WFI half) · Reference census (commands + every hit) · Five-way
  classification table (with the plan-claim delta) · Minimal sufficient change set (per-row action) ·
  Impact declaration draft (pointer to the yaml) · Coverage note + UNKNOWNs.
- `impact-declaration.yaml` (draft) — consumed by the host (implementation) and by
  `focused-verification` (A9) as the change contract.

## Handoff rules

- Hand the report + impact draft to the **host** (the executing agent) for implementation; the host's
  change set must equal the audited minimal set or explain each deviation.
- Hand the (now real) `impact-declaration.yaml` to `focused-verification` (A9) as the verification
  contract, together with the base commit.
- On a request to *execute* → stop; A8 executes nothing.

## Failure modes

- **Very large repo / many hits** → cite the search commands, page the census by file, keep the
  classification exhaustive (a skipped hit is a coverage gap, declared, not silent).
- **Artifact name is common** (e.g. `README.md`) → search by the distinctive title/anchor strings
  first, then basename with context filtering; record which pattern found which rows.
- **Untracked planning docs dominate the census** → classify them (they are rows), keep them
  untracked if the change says so, and say so in the coverage note.
- **A live reference turns out unfixable in-scope** (it lives in a frozen artifact) → record
  DEAD/STALE + frozen; the candidate change may still proceed, with the frozen conflict named in the
  report and the decision note.

## References to load

- `docs/plans/active/research_code_docs_phase2_implementation_prompt.md` §2.1 (the A8 spec this skill
  implements).
- `.agents/skills/project-state-reconstructor/SKILL.md` and
  `.agents/skills/workspace-forensics-and-inventory/SKILL.md` (the two consumed halves).
- `docs/plans/active/reconstruction/phase1/target-workflow-invariants.md` I11/I12 (archive discipline
  the audit's `archive` action must preserve: banner kept, metadata kept).
- `evals/skills/harness/canonical-source-map.md` (info-type → canonical owner, for the impact draft).

## Scripts to run

- `evals/skills/harness/checkers/run_checks.py <simplification-audit-report>` — verify front-matter +
  status vocabulary before handing off.
- `evals/skills/harness/checkers/archive_lint.py --repo` — pre-change baseline for the target's archive
  state (the audit records it; A9 re-runs it post-change).
