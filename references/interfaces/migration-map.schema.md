<!--
generated_by_skill: (manual, Batch-5 additive interface extension per directive Batch3后续 §6.1)
skill_version: n/a
source_commit: 07b5306
source_documents: [references/interfaces/README.md, references/interfaces/document-artifact-map.schema.md, .claude/skills/content-canonicalization-and-migration/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1 — Batch-5 additive extension; adds a new handoff TYPE, re-means none of the seven)
last_verified: 2026-08-06
-->

# Interface schema — `migration-map` *(Batch-5 additive extension of `batch2.5-v1`)*

Produced by **`content-canonicalization-and-migration`**. Consumed by **`technical-document-rewriter`** (writes
the candidate docs) and a human (apply-approval). See [README.md](README.md) for the common header + rules and
the [§ Batch-5 additive extension](README.md) note explaining why this is additive, not an interface re-freeze.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `migration-map` |
| `facts` | **`none (...)`** — a migration map is a **dry-run plan**, not a fact record. Dispositions that rest on a FACT home borrow it from the PSR/IA upstream, never re-assert it. |
| `hypotheses` | pointer+count to **provisional / DEFERRED** dispositions (targets blocked on an open decision). |
| `open_questions` | pointer+count to the **carried open decisions** (D-*/IA-*) — never "none" if any disposition is `DEFERRED`. |
| `evidence_level` | `n/a (dry-run plan; makes no evidence claim)`. |
| `next_handoff` | `technical-document-rewriter` — the map hands the disposition plan to the rewriter (candidate output). The **execution** of moves is a separate `BLOCKED:explicit-write-approval-required`. |
| `handoff_requirements` | what the rewriter needs: the per-source disposition + target, the canonicalization plan, the link-update plan, and which dispositions are `DEFERRED` (must not be rewritten yet). |

## The machine block (checked by `migration_map_check.py`)

A fenced ```yaml block with a top-level `migration_map:` mapping:

```yaml
migration_map:
  mode: dry-run
  may_move: false          # v0: MUST be false
  may_delete: false        # v0: MUST be false
  may_overwrite: false     # v0: MUST be false
  rollback: "<how to revert — v0: discard the candidate dir + this map; nothing was executed>"
  unresolved_decisions: [D-1, D-4, D-6]   # carried from open-decisions.md; every blocked_by below must appear here
  dispositions:
    - source: "docs/skill-development/creation-roadmap.md#L21-40"   # a real path (existence checked)
      primary: split-and-pointer         # EXACTLY ONE primary disposition per source
      target: "status-owner (DEFERRED)"  # target path/home; MUST differ from source
      move: false
      delete: false
      overwrite: false
      blocked_by: D-1                     # if DEFERRED, name the gating decision (must be in unresolved_decisions)
```

## Handoff rule

- **A dry-run plan, never an execution.** `may_move / may_delete / may_overwrite` are all `false`; a map that
  reports a file was moved/deleted/overwritten is a `SKILL_DEFECT` (lane violation) — the directive §6.1 forbids
  the executor executing in v0.
- **One primary disposition per source; target ≠ source.** A source with two primary dispositions, or a target
  equal to its own source path (an in-place overwrite), is a defect.
- **Supersede, never delete.** A retired doc is `superseded_by` a replacement + marked `DEPRECATED`, never
  dropped.
- **Unresolved decisions preserved.** Every `blocked_by` token appears in `unresolved_decisions`; a `DEFERRED`
  disposition never receives a silently-picked target.
