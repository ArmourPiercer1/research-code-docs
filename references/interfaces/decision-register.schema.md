<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/decision-register.template.md, .claude/skills/uncertainty-and-decision-manager/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `decision-register`

Produced by **`uncertainty-and-decision-manager`** (UDM). Consumed by **`documentation-quality-evaluator`**
(advisory) and by a human/orchestrator at a decision point. See [README.md](README.md) for the common
header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `decision-register` |
| `facts` | pointer+count to entries at `FACT`/`VERIFIED`/`BASELINE`/`DECIDED` — each with a re-openable **locator** source (never a bare name) and E-level. Only `E3+` may be called verified. |
| `hypotheses` | pointer+count to `HYPOTHESIS`/`CANDIDATE` entries (with disposition `needs-evidence`/`needs-experiment`). |
| `open_questions` | pointer+count to `OPEN`/`DEFERRED` entries. Never "none" if any item is unsettled. |
| `evidence_level` | the E-level range across entries; paper/analogy entries carry the RES cap (≤ `E2`); project entries stand alone. |
| `next_handoff` | `documentation-quality-evaluator` (advisory review of the register) and/or `human decision` at the gate. |
| `handoff_requirements` | what the reviewer needs: the per-entry status + evidence + locator, the supersede chain for any reversed item, and the unresolved-gap list. |

## Handoff rule

- **Statuses do not blur.** `HYPOTHESIS`/`CANDIDATE`/`OPEN`/`DECIDED` stay distinct; a paper/analogy item may
  not be promoted past `E2`, and evidence-synthesis output is **not** auto-converted into a user decision
  (directive §3.2) — UDM records the state; the human/gate decides. Blurring these is a `SKILL_DEFECT`.
- **Reversal is by SUPERSEDE** (append a new entry + point back), never by editing a decided item — the audit
  trail is preserved.
- Every source is a **re-openable locator** (`file:line` / test-id / run-id / `DOI#section`), never a bare
  author name. A name-only source is an `INTERFACE_DEFECT` for any downstream that must re-verify.

## Conformant header example

```yaml
---
generated_by_skill: uncertainty-and-decision-manager
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/research-evidence-map.md, ".../goal-scope-note.md"]
artifact_type: decision-register
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Single source of truth for the transfer decision's uncertain items; records state, does not decide the gate."
facts: "1 BASELINE — see register (E3, in-project locator)"
hypotheses: "3 HYPOTHESIS/CANDIDATE — see register (E2 cap, needs-experiment)"
open_questions: "2 OPEN — see register (block the tolerance/route choice)"
evidence_level: "E0–E3 across entries; paper/analogy items capped at E2 (RES), project item at E3"
next_handoff: documentation-quality-evaluator
handoff_requirements: "Reviewer needs per-entry status+evidence+locator, the supersede chain, and the 2 OPEN gaps blocking the gate."
---
```
