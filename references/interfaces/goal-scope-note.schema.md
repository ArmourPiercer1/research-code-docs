<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/goal-scope-note.template.md, .claude/skills/goal-scope-and-workflow-elicitor/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `goal-scope-note`

Produced by **`goal-scope-and-workflow-elicitor`**. Consumed by **`document-information-architect`** (Track A),
**`research-question-and-literature-planner`** (Track B), and **`uncertainty-and-decision-manager`**.
See [README.md](README.md) for the common header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `goal-scope-note` |
| `facts` | pointer+count to the *Confirmed constraints* (each with its source — user@date or state-report row). |
| `hypotheses` | usually `none` — a scope note settles or defers; unsettled beliefs belong in the register. If present, pointer+count. |
| `open_questions` | pointer+count to the *Open decisions* table (each classified: needs-literature / needs-prototype / user-preference / repo-verifiable / deferred). Never "none" if any decision is unsettled. |
| `evidence_level` | usually `n/a (scope/goal statement, not an evidence claim)`; a constraint sourced from a verified state-report row may carry that row's E-level. |
| `next_handoff` | the skill that acts on the settled scope: `document-information-architect` (doc corpus), `research-question-and-literature-planner` (a research question), or `uncertainty-and-decision-manager` (to register the open decisions). |
| `handoff_requirements` | what the consumer needs: the settled goal + non-goals, the in/out scope, and the classified open-decision list. |

## Handoff rule

- **Non-goals are load-bearing**: the note must state what is *deliberately not* being done, so a downstream
  skill does not silently re-expand scope. A missing non-goals section is a `SKILL_DEFECT`.
- Every unsettled item is an **Open decision with a classification + recommended next action** — it is not
  silently decided. Downstream (`uncertainty-and-decision-manager`) registers these; the elicitor does not
  decide them itself.
- Must be **readable with no chat context** (the note restates the goal a fresh reader can act on).

## Conformant header example

```yaml
---
generated_by_skill: goal-scope-and-workflow-elicitor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/document-chain/project-state-report.md]
artifact_type: goal-scope-note
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Goal + in/out scope for restructuring the docs/skill-development corpus; excludes doing the restructure."
facts: "4 confirmed constraints — see 'Confirmed constraints' (each sourced)"
hypotheses: "none (scope settled or deferred; beliefs go to the register)"
open_questions: "7 open decisions — see 'Open decisions' (classified + next action each)"
evidence_level: "n/a (goal/scope statement; constraints cite the state-report rows they rest on)"
next_handoff: document-information-architect
handoff_requirements: "IA needs the goal + non-goals + in/out scope; the 7 open decisions are handed to the decision register in parallel."
---
```
