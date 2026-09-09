<!--
generated_by_skill: living-design-maintainer
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<change event / accepted candidate-doc-set + rewrite-provenance-report>, <canonical-source-map.md>, <decision-register.md>]
artifact_type: maintenance-impact-report
document_lifecycle: DRAFT
scope: <one line: maintenance impact of which change on which canonical corpus; proposals only — no canonical doc edited/published>
facts: none (proposals, not a fact record; impacted homes borrowed from canonical-source-map)
hypotheses: <pointer+count to proposed updates blocked on an open decision>
open_questions: <pointer+count to the verification checklist / unresolved approvals; never 'none' if any candidate is unaccepted>
evidence_level: n/a (maintenance proposals; assert no new evidence)
next_handoff: human decision
handoff_requirements: <what the human needs: impacted-home list, proposed updates, stale-reference list, verification checklist>
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Maintenance-Impact Report — <change event> on <corpus>

What a change implies for the canonical documentation — **proposals only**. No canonical document is edited, no
candidate is accepted, nothing is published. Volatile state is proposed as a pointer, never copied into a stable
doc; a candidate is proposed for acceptance, not marked canonical.

```yaml
maintenance_impact:
  mode: proposal-only
  may_overwrite: false
  auto_accept_candidates: false
  auto_publish: false
  change_event: "<what changed>"
  proposed_updates:
    - info_type: <info-type>
      canonical: "<known canonical home from canonical-source-map>"
      target_lifecycle: <stable | volatile | append-only | frozen>
      content_kind: <stable | volatile | experiment-fact | session-context>
      candidate: "<.../candidate-doc-set/doc.md or —>"
      approved: false
      action: <propose-pointer | propose-update | propose-acceptance>   # not mark-canonical/publish while approved:false
  stale_references:
    - "<pointer a change makes stale>"
  verification_checklist:
    - "<what a human must confirm before apply>"
```

## 1. Impacted canonical homes
| info type | canonical home | touched how | lifecycle |
|---|---|---|---|
| <current-status> | `<home>` | <candidate proposes a pointer> | volatile |

## 2. Proposed updates (proposal only — not applied)
| info type | → canonical home | action | approved? | blocked_by |
|---|---|---|---|---|
| <current-status> | `<home>` | propose-pointer | no | <D-1 or —> |

## 3. Stale-reference list
- <pointer/link a change makes stale → where it should point>

## 4. Verification checklist (human confirms before apply)
- [ ] <which candidates are accepted>
- [ ] <which open decisions must first be resolved (D-1 …)>
- [ ] <which pointers to re-point>

## 5. Coverage note
- Change event: <…>. Every impacted home is from the canonical-source-map. Nothing edited/accepted/published;
  applying needs explicit user approval.
