# Eval Coverage Baseline (independent ground truth)

<!--
generated_by: eval_coverage_baseline.py (parent-agent tooling)
scope: ground truth from case YAMLs + dirs, NOT from report docs
date: 2026-09-09
status: reference for cross-checking phase0/current-system-map.md
-->

| skill | trigger | conflict | task-quality | multi-turn | reader-tests |
|---|---|---|---|---|---|
| content-canonicalization-and-migration | 6 | 2 | — | — | — |
| document-information-architect | 6 | 2 | — | — | 1 |
| documentation-quality-evaluator | 23 | 5 | 10 | 3 | 2 |
| documentation-refactor | 6 | 3 | — | — | — |
| goal-scope-and-workflow-elicitor | 23 | 5 | 2 | 3 | — |
| living-design-maintainer | 6 | 2 | — | — | — |
| numerical-research-software-design | 6 | 3 | — | — | — |
| project-state-reconstructor | 23 | 5 | 2 | 3 | — |
| research-evidence-synthesizer | 6 | 2 | — | — | 1 |
| research-question-and-literature-planner | 6 | 2 | — | — | 1 |
| scientific-workspace-reconstruction | 6 | 3 | — | — | — |
| technical-document-rewriter | 6 | 2 | — | — | — |
| uncertainty-and-decision-manager | 23 | 5 | 2 | 3 | — |
| workspace-forensics-and-inventory | 6 | 2 | — | — | 1 |
| **TOTAL** | **152** | **43** | **16** | **12** | **6** |

## Recorded run outputs (evals/skills/results/ subdirs)

- `batch2_5/`
- `batch3/`
- `document-information-architect/`
- `documentation-quality-evaluator/`
- `goal-scope-and-workflow-elicitor/`
- `project-state-reconstructor/`
- `prompts/`
- `research-evidence-synthesizer/`
- `research-question-and-literature-planner/`
- `uncertainty-and-decision-manager/`
- `workspace-forensics-and-inventory/`

## Blind runs (tests/corpus/blind-runs/)

- `adj-2026-07-31/`
- `adjudication-v4/`
- `adjudication-v4b/`
- `adjudication-v4c/`
- `diag-2026-08-02/`
- `diag-d3-2026-08-02/`
- `diag-d3b-2026-08-04/`
- `matrix-2026-07-31/`
- `phase-e-2026-08-05/`
- `reconfirm-2026-07-31/`
- `v04-sanity/`

## Notes for cross-checking

- A '—' means no case file exists for that skill/set (not zero cases).
- Verified 2026-09-10 (parent recount, all 5 case dirs): 41 files / 229 cases
  (152 trigger / 43 conflict / 16 task-quality / 12 multi-turn / 6 reader-tests).
  This matches phase0/current-system-map.md's figure; the earlier 211/32 count
  covered only the three primary dirs.
