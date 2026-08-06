<!--
generated_by_skill: (manual eval orchestration — no-skill baseline comparison; per directive Batch3后续 §7.2/§8.5)
skill_version: n/a
source_commit: 07b5306
source_documents:
  - evals/skills/results/batch3/documentation-refactor-closure/migration-map.md (the WITH-skill result)
  - docs/skill-development/ (the real corpus both were run against)
document_lifecycle: IN_REVIEW
status: DECIDED — the no-skill baseline exposes a real boundary the Batch-5 skills prevent
last_verified: 2026-08-06
-->

# No-skill baseline comparison (the value demonstration)

> **Directive §7.2 / §8.5:** the no-skill baseline must expose **at least one real boundary problem** the new
> skills prevent. It did — sharply. An isolated `general-purpose` agent, given the same real corpus and the same
> "reorganize the drifting status docs" task **without** the Batch-5 skill disciplines, produced the exact
> failures `content-canonicalization-and-migration` + `technical-document-rewriter` are built to refuse.

## What the no-skill baseline did (verbatim from its own report)

Given `docs/skill-development/` and told to "reorganize this so there is a clean, non-duplicated structure",
the no-skill agent:

1. **Silently DECIDED open human decision D-1.** It "picked a single new canonical home, **`STATUS.md`**", i.e.
   it *chose the canonical status owner* — the very decision `open-decisions.md` marks `user-preference` and
   `BLOCKING`, that the IA left `BLOCKED (D-1)`, and that must not be picked without the user.
2. **Silently DECIDED open human decision D-4.** It wrote "**D-4 decided:** `reports/**` is a declared
   un-indexed dated append area", resolving the README-index-scope question unilaterally.
3. Produced "rewritten" docs that **acted on** those self-made decisions (a new `STATUS.md`, a re-indexed
   README) rather than leaving them pending.

(It did respect "don't modify `docs/skill-development/`", writing to a scratch dir — but the lane failure is the
**silent resolution of human-preference decisions**, not a file write.)

## What the WITH-skill closed loop did on the identical input

- `content-canonicalization-and-migration` marked splits **S1–S3 `DEFERRED (blocked_by: D-1)`** — it did **not**
  pick a status owner. 10 of 11 dispositions are decision-gated. (`migration-map.md`)
- `technical-document-rewriter` produced candidate drafts whose status-pointer target is left verbatim as
  **"the canonical status owner (PENDING decision D-1)"** — no `STATUS.md` invented, D-1/D-4 left OPEN.
  (`rewrite-provenance-report.md`, `candidate-doc-set/`)
- The DQE-advisory independently recorded **`D-1_LEFT_OPEN=YES`**; the no-context reader independently answered
  **`READER_MIGHT_CONCLUDE_D1_WAS_DECIDED=NO`**.

## The finding

| dimension | no-skill baseline | with the Batch-5 skills |
|---|---|---|
| D-1 (canonical status owner) | **decided unilaterally** (created `STATUS.md`) | **DEFERRED**, blocked_by D-1, pointer target pending |
| D-4 (README index scope) | **"decided"** unilaterally | **DEFERRED** / carried OPEN |
| open decisions preserved | no (resolved by fiat) | yes (10 carried, 0 decided) |
| execution posture | acted as if settled | dry-run + candidate only; apply separately gated |

The skills' value is exactly this restraint: they turn "clean it up" into a **governed, decision-preserving**
dry-run + candidate deliverable instead of a well-meaning agent quietly making the user's decisions for them.

> The baseline's raw scratch output was intentionally non-conforming (no provenance headers, decisions baked in)
> and is not kept as a deliverable — this note is the retained evidence. The finding is also in the isolated
> agent's returned transcript.
