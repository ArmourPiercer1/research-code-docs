# Blind-matrix evaluation summary — documentation-quality-evaluator v0.3

Runs: 26 (20 current + 6 repeat). Corpus dataset_version 3.

## §17 promotion bar

| metric | value | bar | ok |
|---|---|---|---|
| golden-negative false PASS | 2 | == 0 | ❌ |
| golden-positive false hard FAIL | 3 | == 0 | ❌ |
| required-blocker recall | 0.75 | >= 0.90 | ❌ |
| forbidden-blocker violation rate | 0.115 | <= 0.05 | ❌ |
| boundary-pair ordering | 0.6 | == 1.0 | ❌ |
| 3-run verdict consistency | 0.333 | == 1.0 | ❌ |
| max score stddev | 6.18 | <= 5 | ❌ |

**PROMOTION BAR: NOT MET ❌**

## Per-case (current runs)

| case | class | expected | got | recall | forbidden-fired |
|---|---|---|---|---|---|
| BP-001-fail | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-002-fail | boundary-fail | FAIL | FAIL | 1.0 | HF-13,HF-14A |
| BP-003-fail | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-004-controlled | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-005-fail | boundary-fail | FAIL | FAIL | 1.0 | — |
| BP-001-pass | boundary-pass | PASS | PASS |  | — |
| BP-002-pass | boundary-pass | PASS | PASS |  | — |
| BP-003-pass | boundary-pass | PASS | PASS |  | — |
| BP-004-external | boundary-pass | PASS | FAIL |  | HF-9 |
| BP-005-pass | boundary-pass | PASS | FAIL |  | — |
| GN-ADR-001 | golden-negative | FAIL | FAIL |  | — |
| GN-ADR-002 | golden-negative | FAIL | FAIL | 1.0 | — |
| GN-EXP-001 | golden-negative | FAIL | PASS | 0.0 | — |
| GN-PROP-001 | golden-negative | FAIL | FAIL |  | HF-14A |
| GN-ROADMAP-001 | golden-negative | FAIL | PASS | 0.0 | — |
| GP-ADR-001 | golden-positive | PASS | PASS |  | — |
| GP-EXP-001 | golden-positive | PASS | FAIL |  | — |
| GP-PROP-001 | golden-positive | PASS | PASS |  | — |
| GP-PROP-002 | golden-positive | PASS | PASS |  | — |
| GP-ROADMAP-001 | golden-positive | PASS | PASS |  | — |

## Boundary-pair ordering

- BP-001: ✅ correct
- BP-002: ✅ correct
- BP-003: ✅ correct
- BP-004: ❌ WRONG
- BP-005: ❌ WRONG

## Stability (repeat cases)

- BP-001-fail: verdicts ['FAIL', 'FAIL', 'FAIL'] — consistent ✅; blocker Jaccard 1.0; score σ 2.62
- GN-ROADMAP-001: verdicts ['PASS', 'PASS', 'FAIL'] — INCONSISTENT ❌; blocker Jaccard 1.0; score σ 6.18
- GP-PROP-002: verdicts ['PASS', 'FAIL', 'PASS'] — INCONSISTENT ❌; blocker Jaccard 0.0; score σ 4.84
