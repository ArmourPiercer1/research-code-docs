# Blind-matrix evaluation summary — documentation-quality-evaluator v0.4.1

Runs: 4 across arms ['v0.4.1']. Candidate arm: **v0.4.1** (4 runs, 2 current). Corpus dataset_version 4. run_id=phase-e-canary.

## Candidate admission bar

| metric | value | bar | ok |
|---|---|---|---|
| gate-expectation mismatch (PRIMARY) | 1 | == 0 | ❌ |
| terminal-contract mismatch | 0 | == 0 | ✅ |
| golden-negative false ALLOW | 1 | == 0 | ❌ |
| golden-positive false non-ALLOW | 0 | == 0 | ✅ |
| required-blocker recall | 1.0 | >= 0.90 | ✅ |
| required-finding recall | 0.0 | >= 0.90 | ❌ |
| forbidden-blocker violation rate | 0.0 | == 0 | ✅ |
| boundary-pair ordering | 0.0 | == 1.0 | ❌ |
| 3-run gate consistency | 1.0 | == 1.0 | ✅ |
| max score stddev | 0.0 | <= 5 | ✅ |
| profile echo compliance | 1.0 | == 1.0 | ✅ |
| checker execution compliance | 1.0 | == 1.0 | ✅ |

**ADMISSION BAR (v0.4.1): NOT MET ❌**

## Candidate per-case (current runs)

| case | class | exp_gate | got_gate | ✓ | recall | find-rec | term-green | forbidden-fired |
|---|---|---|---|---|---|---|---|---|
| BP-006-release | boundary-fail | BLOCK | ALLOW | ❌ |  | 0.0 | —/exp:non | — |
| BP-006-audit | boundary-pass | ALLOW | ALLOW | ✅ |  | 0.0 | —/exp:non | — |

## Boundary-pair ordering (candidate)

- BP-006: ❌ WRONG

## Stability (candidate repeat cases)

- BP-006-release: verdicts ['ALLOW', 'ALLOW', 'ALLOW'] — consistent ✅; blocker Jaccard 1.0; score σ None
