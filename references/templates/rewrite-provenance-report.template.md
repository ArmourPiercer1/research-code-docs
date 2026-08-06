<!--
generated_by_skill: technical-document-rewriter
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<migration-map.md>, <selected source docs>, <project-state-report.md>, <decision-register.md>]
artifact_type: rewrite-provenance-report
document_lifecycle: DRAFT
scope: <one line: candidate rewrite of which corpus; new files only — no source overwritten/moved/deleted>
facts: none (provenance, not a fact record; rewritten claims keep their PSR status)
hypotheses: <pointer+count to candidate content that stays HYPOTHESIS/OPEN>
open_questions: <pointer+count to the unresolved-content list; never 'none' if any source range is unplaced>
evidence_level: n/a (rewrite provenance; asserts no new evidence)
next_handoff: documentation-quality-evaluator
handoff_requirements: <what the reviewer/maintainer needs: candidate dir, candidate↔source map, unresolved-content, completion status>
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Rewrite Provenance Report — <corpus>

Candidate rewritten docs realizing the `migration-map` dispositions. **The source corpus is untouched** (each
source hash below is re-verified). Every candidate maps to its source range(s); unplaced content and standing
conflicts are listed, not dropped.

```yaml
rewrite_provenance:
  mode: candidate-output-only
  may_overwrite: false
  may_move: false
  may_delete: false
  candidate_dir: "<.../candidate-doc-set/>"
  completion: <PARTIAL | COMPLETE>   # COMPLETE only if unresolved_content is empty
  unresolved_content:
    - "<source range with no home / conflict left standing / DEFERRED disposition>"
  sources:
    - {path: "<path/to/source.md>", sha256: "<hash at read time — re-verified unchanged>"}
  provenance:
    - candidate: "<.../candidate-doc-set/doc.md>"   # MUST differ from every source path
      from_sources: ["<path/to/source.md#Lxx-yy>"]  # >=1 source range
      change: "<what changed; OPEN kept OPEN; no fact invented>"
```

## 1. Candidate ↔ source provenance
| candidate doc | from source range(s) | change summary | status kept |
|---|---|---|---|
| `<candidate>` | `<source#Lxx>` | <restructure; pointer left> | OPEN stays OPEN |

## 2. Unresolved-content list (nothing dropped silently)
| source content (locator) | why unresolved | routed to |
|---|---|---|
| `<source#Lxx>` | DEFERRED (blocked_by D-1) | open decision / human |

## 3. Source integrity
- Sources read: <n>. Each `sha256` recorded above; re-verify with `rewrite_provenance_check.py` — all unchanged.

## 4. Coverage note
- Completion is `PARTIAL` while §2 is non-empty. Candidate docs are drafts (`document_lifecycle: DRAFT`);
  nothing is published. Apply-mode (replacing live docs) needs explicit user approval.
