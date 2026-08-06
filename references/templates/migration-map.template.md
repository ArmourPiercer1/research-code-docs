<!--
generated_by_skill: content-canonicalization-and-migration
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<document-artifact-map.md>, <canonical-source-map.md>, <open-decisions.md>, <project-state-report.md>]
artifact_type: migration-map
document_lifecycle: DRAFT
scope: <one line: dry-run migration plan for which corpus; a plan only — nothing moved/deleted/overwritten>
facts: none (a dry-run plan; FACT homes borrowed from PSR/IA, not re-asserted)
hypotheses: <pointer+count to provisional/DEFERRED dispositions>
open_questions: <pointer+count to carried open decisions; never 'none' if any disposition is DEFERRED>
evidence_level: n/a (dry-run plan; no evidence claim)
next_handoff: technical-document-rewriter
handoff_requirements: <what the rewriter needs: per-source disposition+target, canonicalization plan, link-update plan, which dispositions are DEFERRED>
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Migration Map (dry-run) — <corpus>

A **dry-run plan** realizing the `document-artifact-map` split plan. **Nothing is moved, deleted, or
overwritten.** Every source section gets one primary disposition or an explicit `DEFERRED`; retired docs are
superseded, not deleted; unresolved decisions are carried, not decided.

```yaml
migration_map:
  mode: dry-run
  may_move: false
  may_delete: false
  may_overwrite: false
  rollback: "v0: nothing was executed — revert = discard the candidate dir + this map"
  unresolved_decisions: [<D-1>, <D-4>, <D-6>]
  dispositions:
    - source: "<path/to/source.md#Lxx-yy>"
      primary: <move-to | split-and-pointer | keep-in-place | merge-into | annotate | DEFERRED>
      target: "<target home/path — MUST differ from source>"
      move: false
      delete: false
      overwrite: false
      blocked_by: <decision-id if DEFERRED, else omit>
```

## 1. Canonicalization plan (info-type → single canonical home)
| info type | canonical home | verdict (FACT/provisional/BLOCKED) | basis |
|---|---|---|---|
| <architecture> | `<home>` | FACT (borrowed from PSR) | <ref> |

## 2. Per-source disposition (migration) map
| # | source (locator) | primary disposition | target | move/del/ovw | blocked_by |
|---|---|---|---|---|---|
| M1 | `<source#Lxx>` | split-and-pointer | `<target>` | false/false/false | <D-x or —> |

## 3. Supersession map (retired doc → replacement; never a delete)
| retired doc | superseded_by | reason | lifecycle action |
|---|---|---|---|
| `<old.md>` | `<new.md>` | <why> | mark DEPRECATED + pointer (not deleted) |

## 4. Link-update plan (so each fact is stored once)
| pointer/link | in | change to |
|---|---|---|
| <status header> | `<doc>` | "current status → <owner>" |

## 5. Rollback plan
- v0: nothing executed → revert = discard the candidate dir + this map. (Apply-mode rollback plan added only
  when a user authorizes execution.)

## 6. Carried open decisions (NOT decided here)
- <D-1 … carried from open-decisions.md; each gates the DEFERRED dispositions above.>

## 7. Coverage note
- Inputs used: <artifact-map, canonical-source-map, open-decisions, state-report>. Every source section in the
  artifact-map split plan is assigned a disposition or DEFERRED above. Nothing moved/deleted/overwritten.
