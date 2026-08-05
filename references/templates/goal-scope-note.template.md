---
generated_by_skill: goal-scope-and-workflow-elicitor
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [state-report.md, user answers]
artifact_type: goal-scope-note
document_lifecycle: IN_REVIEW
scope: <one line: what goal/scope this settles; excludes doing the work>
facts: <pointer+count to Confirmed constraints (each sourced)>
hypotheses: <usually "none (settled or deferred; beliefs go to the register)">
open_questions: <pointer+count to Open decisions (classified + next action); never 'none' if unsettled>
evidence_level: <usually "n/a (goal/scope statement)"; a state-sourced constraint may carry its row's E-level>
next_handoff: <document-information-architect | research-question-and-literature-planner | uncertainty-and-decision-manager>
handoff_requirements: <what the consumer needs: goal + non-goals + in/out scope + classified open decisions>
status: DECIDED for settled items; OPEN items listed separately
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
---

# Goal / Scope / Workflow Note — <project>

Readable with no chat context. Settled here; unresolved items in the open-decision list.

## Goal
- <what success looks like, in one paragraph a fresh reader can act on>

## In scope
- <bullet> · <bullet>

## Non-goals (explicit)
- <what we are deliberately NOT doing>

## Intended workflow (dev–test–experiment)
- <how work will actually flow: where code lives, how it's tested, how experiments run/log>

## Confirmed constraints
| constraint | source |
|---|---|
| <e.g. must run on a single workstation, no cluster> | user @ <date> |

## Open decisions (→ decision register)
| id | question | classification | recommended next action |
|---|---|---|---|
| Q-1 | <question> | needs-literature \| needs-prototype \| user-preference \| repo-verifiable \| deferred | <action> |
