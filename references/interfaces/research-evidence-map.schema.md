<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/evidence-map.template.md, .claude/skills/research-evidence-synthesizer/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `research-evidence-map`

Produced by **`research-evidence-synthesizer`** (RES) from **already-retrieved** evidence. Consumed by
**`uncertainty-and-decision-manager`**. See [README.md](README.md) for the common header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `research-evidence-map` |
| `facts` | **`none (...)`** — paper/analogy evidence is **never** a project-verified fact (constraint **D.8**). An in-project trial, if any, is isolated at its own low E-level, not laundered into the transfer rows. |
| `hypotheses` | pointer+count to the claim–evidence matrix rows (each with an E-level + channel). |
| `open_questions` | pointer+count to the *Unresolved gaps* (each with what would close it) — including any gap to hand **back** to RQLP for more retrieval. Never "none" if a gap exists. |
| `evidence_level` | the **max** E-level any claim carries, **capped** by channel: cross-domain-analogy ≤ `E2`; an unevidenced assumption is `E0`. Never above the weakest load-bearing assumption. |
| `next_handoff` | `uncertainty-and-decision-manager` (to register), and (if gaps) `research-question-and-literature-planner` (to re-scope retrieval). |
| `handoff_requirements` | what the register needs: the per-claim E-level + channel, the method-transfer card's assumptions + E-cap, and which gaps are unresolved. |

## Handoff rule

- **RES never retrieves** and **never upgrades analogy → project fact** (D.8). A map that starts a search, or
  that presents a cross-domain claim as a project-verified fact, is a `SKILL_DEFECT` (the exact failure this
  skill guards).
- Keep the **four channels separate**: direct / same-domain-indirect / cross-domain-analogy /
  project-inference. Collapsing them is an `INTERFACE_DEFECT` for the downstream register.
- Decisions are **routed to the register, not made here** — RES organizes evidence; `uncertainty-and-decision-manager`
  assigns the final DECIDED status.

## Conformant header example

```yaml
---
generated_by_skill: research-evidence-synthesizer
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/lit-review-results.md, "<the design decision it informs>"]
artifact_type: research-evidence-map
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Organizes the retrieved bundle into a claim–evidence matrix for one transfer decision; no retrieval; no fact upgrade."
facts: "none (paper/analogy capped ≤ E2; any in-project trial isolated at its own level — D.8)"
hypotheses: "6 claim rows — see 'Claim–evidence matrix' (E-level + channel each)"
open_questions: "4 gaps — see 'Unresolved gaps' (1 routed back to RQLP for more retrieval)"
evidence_level: "E2 (cap: cross-domain-analogy; one assumption sits at E0 — unevidenced)"
next_handoff: uncertainty-and-decision-manager
handoff_requirements: "The register needs per-claim E-level+channel, the transfer card's assumptions+E-cap, and the unresolved-gap list."
---
```
