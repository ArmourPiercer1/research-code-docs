<!--
generated_by_skill: (manual, Batch-5 additive interface extension per directive Batch3后续 §6.3)
skill_version: n/a
source_commit: 07b5306
source_documents: [references/interfaces/README.md, references/interfaces/rewrite-provenance-report.schema.md, .claude/skills/living-design-maintainer/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1 — Batch-5 additive extension; adds a new handoff TYPE, re-means none of the seven)
last_verified: 2026-08-06
-->

# Interface schema — `maintenance-impact-report` *(Batch-5 additive extension of `batch2.5-v1`)*

Produced by **`living-design-maintainer`**. Consumed by a **human / orchestrator** for review + apply-approval.
See [README.md](README.md).

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `maintenance-impact-report` |
| `facts` | **`none (...)`** — proposals, not a fact record. Impacted-home assignments borrow the canonical-source-map; none is re-asserted. |
| `hypotheses` | pointer+count to proposed updates that are blocked on an open decision (e.g. status owner on D-1). |
| `open_questions` | pointer+count to the verification checklist / unresolved approvals — never "none" if any candidate is unaccepted. |
| `evidence_level` | `n/a (maintenance proposals; assert no new evidence)`. |
| `next_handoff` | `human decision` — a human reviews the proposals + verification checklist and authorizes apply. Applying is `BLOCKED:explicit-write-approval-required`. |
| `handoff_requirements` | what the human needs: the impacted-home list, the proposed updates (each pointing at a known canonical home), the stale-reference list, and the verification checklist. |

## The machine block (checked by `maintenance_impact_check.py`)

A fenced ```yaml block with a top-level `maintenance_impact:` mapping:

```yaml
maintenance_impact:
  mode: proposal-only
  may_overwrite: false            # v0: MUST be false
  auto_accept_candidates: false   # v0: MUST be false
  auto_publish: false             # v0: MUST be false
  change_event: "<what changed — e.g. accepted candidate-doc-set from the rewrite>"
  proposed_updates:
    - info_type: current-status
      canonical: "status-owner (BLOCKED on D-1)"   # a KNOWN canonical home, never a candidate/handoff
      target_lifecycle: volatile   # the home's lifecycle
      content_kind: volatile       # volatile content may NOT be proposed into a stable home
      candidate: "<.../candidate-doc-set/README.md>"
      approved: false              # a candidate is not canonical until a human accepts it
      action: propose-pointer      # never 'mark-canonical'/'publish' while approved:false
  stale_references:
    - "<pointer that a change makes stale>"
  verification_checklist:
    - "<what a human must confirm before apply>"
```

## Handoff rule

- **Proposal only.** `may_overwrite / auto_accept_candidates / auto_publish` are all `false`; a report that
  edits a canonical doc, accepts a candidate, or publishes is a `SKILL_DEFECT`.
- **Known canonical homes.** Every `proposed_update.canonical` names a home from the canonical-source-map — not a
  candidate path, a handoff artifact, or a session note.
- **Single source of truth.** No `info_type` is proposed into two different canonical homes; a `content_kind:
  volatile` update targeting a `target_lifecycle: stable` home is a boundary violation (the HF-14b rule).
- **Candidate ≠ canonical.** A `proposed_update` with `approved: false` may not carry a `mark-canonical` /
  `publish` / `accept` action.
