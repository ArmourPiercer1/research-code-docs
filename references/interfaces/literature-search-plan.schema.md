<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/search-plan.template.md, .claude/skills/research-question-and-literature-planner/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `literature-search-plan`

Produced by **`research-question-and-literature-planner`** (RQLP). Consumed by the **installed retrieval
stack** — `lit-review` (default) / `wos-research` / `deep-research` / `paper-fetch-skill`. See
[README.md](README.md) for the common header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `literature-search-plan` |
| `facts` | **`none (...)`** — a search plan is produced **before retrieval**; it contains no retrieved papers and no findings. Named seed anchors are labeled *"to confirm/expand — not asserted findings."* |
| `hypotheses` | pointer+count to the decision-tied questions the search will inform (framed as questions, not answers). |
| `open_questions` | pointer+count to the questions + the transfer-assumption warning that retrieval must resolve. Never "none". |
| `evidence_level` | the **target** evidence standard the question can support (e.g., cross-domain → capped indirect/analogy → `E2`), stated as an expectation for the synthesizer, not a claim held now. |
| `next_handoff` | the chosen retrieval skill (default `lit-review`), with a one-line justification vs the other four. |
| `handoff_requirements` | what retrieval needs: the seed query/seeds, the in/out scope, the inclusion/exclusion criteria, and the stop criterion. |

## Handoff rule

- **RQLP never retrieves.** A search plan that contains retrieved papers, summaries, or findings is an
  `INTERFACE_DEFECT` (planning conflated with doing) — directive §7 forbids RQLP executing retrieval. This is
  the boundary the no-skill baseline most often violated in Batch 2.
- The do-not-trigger set names **all five** research skills; the route is **one** chosen skill with a reason.
- The plan must carry a **stop criterion** and an **evidence standard mapped to E0–E5**, so the synthesizer
  downstream knows the ceiling (e.g., a cross-domain question cannot yield a direct/project fact).
- Emits the machine-readable route line: `` `ROUTE retrieval=<skill> because=<one line>` ``.

## Conformant header example

```yaml
---
generated_by_skill: research-question-and-literature-planner
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: ["<the open research question>", "<originating decision/goal if any>"]
artifact_type: literature-search-plan
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Scope + route for one cross-domain transfer question; excludes retrieval/summary/synthesis (delegated)."
facts: "none (no retrieval performed; seeds are labeled 'to confirm — not findings')"
hypotheses: "3 decision-tied questions — see 'Question(s) + the decision they inform'"
open_questions: "3 questions + 1 transfer warning — see 'Evidence / quality standard'"
evidence_level: "E2 target cap (cross-domain → analogy/indirect only; cannot support a direct/project fact)"
next_handoff: lit-review
handoff_requirements: "lit-review needs the seed query + in/out scope + inclusion/exclusion criteria + the stop criterion."
---
```
