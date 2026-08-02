# Blind-matrix evaluation summary — documentation-quality-evaluator v0.3

Runs: 39 (13 current + 26 repeat). Corpus dataset_version 3.

## §17 promotion bar

| metric | value | bar | ok |
|---|---|---|---|
| golden-negative false ALLOW | 1 | == 0 | ❌ |
| golden-positive false non-ALLOW | 0 | == 0 | ✅ |
| required-blocker recall | 1.0 | >= 0.90 | ✅ |
| forbidden-blocker violation rate | 0.0 | <= 0.05 | ✅ |
| boundary-pair ordering | 1.0 | == 1.0 | ✅ |
| 3-run gate consistency | 1.0 | == 1.0 | ✅ |
| max score stddev | 0.0 | <= 5 | ✅ |
| profile echo compliance | 1.0 | == 1.0 | ✅ |

**PROMOTION BAR: NOT MET ❌**

## Per-case (current runs)

| case | class | expected | got | recall | forbidden-fired |
|---|---|---|---|---|---|
| BP-002-fail | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-004-controlled | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-005-fail | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-002-audit | boundary-pass | PASS | PASS |  | — |
| BP-002-pass | boundary-pass | PASS | PASS |  | — |
| BP-004-external | boundary-pass | PASS | PASS |  | — |
| BP-005-pass | boundary-pass | PASS | PASS |  | — |
| GN-EVIDENCE-BARE-CLAIM-001 | golden-negative | FAIL | FAIL | 1.0 | — |
| GN-EXP-REPRO-001 | golden-negative | FAIL | PASS |  | — |
| GN-PROP-VALIDATION-001 | golden-negative | INCOMPLETE_EVALUATION | INCOMPLETE_EVALUATION |  | — |
| GN-ROADMAP-001 | golden-negative | FAIL | FAIL | 1.0 | — |
| GP-EXP-001 | golden-positive | PASS | PASS |  | — |
| GP-PROP-CONTROLLED-001 | golden-positive | PASS | PASS |  | — |

## Boundary-pair ordering

- BP-002: ✅ correct
- BP-004: ✅ correct
- BP-005: ✅ correct

## Stability (repeat cases)

- BP-002-audit: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-002-fail: verdicts ['BLOCK', 'BLOCK', 'BLOCK'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-002-pass: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-004-controlled: verdicts ['BLOCK', 'BLOCK', 'BLOCK'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-004-external: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-005-fail: verdicts ['BLOCK', 'BLOCK', 'BLOCK'] — consistent ✅; blocker Jaccard 1.0; score σ None
- BP-005-pass: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GN-EVIDENCE-BARE-CLAIM-001: verdicts ['BLOCK', 'BLOCK', 'BLOCK'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GN-EXP-REPRO-001: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GN-PROP-VALIDATION-001: verdicts ['INCOMPLETE', 'INCOMPLETE', 'INCOMPLETE'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GN-ROADMAP-001: verdicts ['BLOCK', 'BLOCK', 'BLOCK'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GP-EXP-001: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
- GP-PROP-CONTROLLED-001: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
