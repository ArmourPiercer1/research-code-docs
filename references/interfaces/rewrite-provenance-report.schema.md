<!--
generated_by_skill: (manual, Batch-5 additive interface extension per directive Batch3后续 §6.2)
skill_version: n/a
source_commit: 07b5306
source_documents: [references/interfaces/README.md, references/interfaces/migration-map.schema.md, .claude/skills/technical-document-rewriter/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1 — Batch-5 additive extension; adds a new handoff TYPE, re-means none of the seven)
last_verified: 2026-08-06
-->

# Interface schema — `rewrite-provenance-report` *(Batch-5 additive extension of `batch2.5-v1`)*

Produced by **`technical-document-rewriter`**. Consumed by **`documentation-quality-evaluator`** (advisory) and
**`living-design-maintainer`** (maintenance impact of accepting the candidates). See [README.md](README.md).

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `rewrite-provenance-report` |
| `facts` | **`none (...)`** — provenance, not a fact record. Rewritten claims carry the PSR status they came in with; none is upgraded. |
| `hypotheses` | pointer+count to candidate content that stays HYPOTHESIS/OPEN (never promoted to FACT). |
| `open_questions` | pointer+count to the **unresolved-content list** — never "none" if any source range is unplaced or any conflict stands. |
| `evidence_level` | `n/a (rewrite provenance; asserts no new evidence)`. |
| `next_handoff` | `documentation-quality-evaluator` (advisory) then `living-design-maintainer`. Apply-mode is `BLOCKED:explicit-write-approval-required`. |
| `handoff_requirements` | what the reviewer/maintainer needs: the candidate dir, the candidate↔source map, the unresolved-content list, and the completion status (PARTIAL until unresolved-content is empty). |

## The machine block (checked by `rewrite_provenance_check.py`)

A fenced ```yaml block with a top-level `rewrite_provenance:` mapping:

```yaml
rewrite_provenance:
  mode: candidate-output-only
  may_overwrite: false     # v0: MUST be false
  may_move: false
  may_delete: false
  candidate_dir: "evals/skills/results/.../candidate-doc-set/"
  completion: PARTIAL      # COMPLETE only if unresolved_content is empty
  unresolved_content:      # source ranges with no home, conflicts left standing, DEFERRED dispositions
    - "docs/.../creation-roadmap.md status tracker → DEFERRED (blocked_by D-1)"
  sources:
    - {path: "docs/skill-development/README.md", sha256: "<hash at read time>"}   # re-verified unchanged
  provenance:
    - candidate: "evals/skills/results/.../candidate-doc-set/README.md"   # candidate path != any source path
      from_sources: ["docs/skill-development/README.md#L16-25"]           # >=1 source range (completeness)
      change: "removed volatile status header; replaced with pointer; OPEN kept OPEN"
```

## Handoff rule

- **Candidate output, never overwrite.** Every `candidate` path differs from every `source` path; each recorded
  source `sha256` still matches the file on disk (the source was not touched). A report whose candidate equals a
  source, or whose source hash has changed, is a `SKILL_DEFECT`.
- **Provenance complete.** Every candidate maps to ≥1 source range; nothing is created from nothing and nothing
  is dropped silently (unplaced source content is in `unresolved_content`).
- **Honest completion.** `completion: COMPLETE` is illegal while `unresolved_content` is non-empty.
- **Traceability front-matter.** Each candidate doc file carries `generated_by_skill` + `source_documents` +
  `document_lifecycle: DRAFT`.
