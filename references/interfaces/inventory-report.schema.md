<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/inventory-report.template.md, .claude/skills/workspace-forensics-and-inventory/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `inventory-report`

Produced by **`workspace-forensics-and-inventory`** (workspace or document-corpus mode). Consumed by
**`project-state-reconstructor`**. Read the common header + field rules in
[README.md](README.md) first; this file only states the specializations.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `inventory-report` |
| `facts` | **`none (...)`** — an inventory asserts **candidates + structural signals only**; it never claims code/tests/experiments run. Verification is `project-state-reconstructor`'s job. |
| `hypotheses` | pointer+count to *candidate* classifications (entry-points, orphans, canonical-source guesses) — all tagged with the signal that makes them candidates. |
| `open_questions` | pointer+count to the **Handoff** unknowns + contradiction/overlap candidates raised for PSR. Never "none" if any orphan/contradiction candidate exists. |
| `evidence_level` | **`n/a (structural signals only; no evidence claims)`**. An inventory does not assign E-levels. |
| `next_handoff` | `project-state-reconstructor` |
| `handoff_requirements` | what PSR needs: the corpus/repo root, the list of candidates to verify, and the contradiction pairs to resolve. |

## Handoff rule

- The inventory is **read-only**: `source_documents` names the corpus/repo root, and the artifact asserts
  **nothing runs**. If a downstream reads a runtime fact out of this artifact, that is an **INTERFACE_DEFECT**
  (the inventory over-claimed) — an inventory→runtime-fact upgrade is forbidden (directive §7).
- Every orphan / canonical-source / contradiction entry must carry **the search that produced it** (scan
  boundary), so PSR can re-open it. A candidate without its cited signal is a `SKILL_DEFECT`.

## Conformant header example

```yaml
---
generated_by_skill: workspace-forensics-and-inventory   # ≡ produced_by_skill
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [docs/skill-development/]              # ≡ source_artifacts (the corpus root)
artifact_type: inventory-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Structural inventory of docs/skill-development/**; excludes code execution + fact verification (PSR's job)."
facts: "none (candidates + signals only; nothing here is claimed to run)"
hypotheses: "12 candidate doc-role classifications — see 'Doc-type table'"
open_questions: "6 items — see 'Contradiction candidates' (2) + 'Handoff' (4 for PSR)"
evidence_level: "n/a (structural signals only; no evidence claims)"
next_handoff: project-state-reconstructor
handoff_requirements: "PSR needs the corpus root + the candidate list to verify + the contradiction pairs to resolve."
---
```
