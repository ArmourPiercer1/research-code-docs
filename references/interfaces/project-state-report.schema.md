<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/state-report.template.md, .claude/skills/project-state-reconstructor/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `project-state-report`

Produced by **`project-state-reconstructor`**. Consumed by **`goal-scope-and-workflow-elicitor`** and
**`document-information-architect`**. See [README.md](README.md) for the common header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `project-state-report` |
| `facts` | **required, the payload** — pointer+count to the *What runs (FACT)* / *What is tested* rows, each with its evidence locator + E-level. Facts are **recovered, not inherited** from old docs. |
| `hypotheses` | pointer+count to claims that are believed but unverified (e.g., "phase-2 module imports but untested"). |
| `open_questions` | pointer+count to the *UNKNOWNs* table (+ how to resolve) and *Contradicted / STALE* rows. Never "none" if any UNKNOWN exists. |
| `evidence_level` | the **max** E-level actually substantiated (e.g., `E3` if a smoke test passes; `E1/E2` if only imports/claims). Do not inflate. |
| `next_handoff` | `goal-scope-and-workflow-elicitor` (Track A/B) — or `document-information-architect` directly for a doc-only corpus. |
| `handoff_requirements` | what the consumer needs: the FACT/UNKNOWN split, which claims were marked STALE, and which UNKNOWNs block a downstream decision. |

## Handoff rule

- A claim from an old doc stays a **claim** until this artifact gives it an evidence locator. Passing an
  inherited-but-unverified claim downstream as a FACT is a `SKILL_DEFECT`.
- `UNKNOWN` must be preserved as `UNKNOWN` — never defaulted to done/false/verified (directive §5.1).
- For a **document-only** corpus (Track A), "what runs" is mostly `n/a`/`UNKNOWN` (no executable target):
  the report's job there is the **claim-vs-reality / STALE** ledger across the docs, not runtime facts.

## Conformant header example

```yaml
---
generated_by_skill: project-state-reconstructor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/document-chain/inventory-report.md, docs/skill-development/]
artifact_type: project-state-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Recovered state of the docs/skill-development corpus; excludes design of a target structure (IA's job)."
facts: "8 FACT rows — see 'What is true of the corpus (FACT)'; max evidence E2 (doc-content, not execution)"
hypotheses: "3 — see 'Believed but unverified'"
open_questions: "5 UNKNOWN + 4 STALE — see 'UNKNOWNs' and 'Contradicted / STALE claims'"
evidence_level: "E2 (claims verified against doc content; no runtime target in a doc-only corpus)"
next_handoff: goal-scope-and-workflow-elicitor
handoff_requirements: "Consumer needs the FACT/UNKNOWN split + the STALE list; UNKNOWN-3 blocks the IA canonical-home choice."
---
```
