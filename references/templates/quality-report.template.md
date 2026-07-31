---
generated_by_skill: documentation-quality-evaluator
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<target-doc under review>]
status: DECIDED (verdict recorded below)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
---

# Quality Report — <target-doc>

**VERDICT: <PASS|FAIL>**  ·  total=<n>/100  ·  blockers=[<HF-x, …>]

## 1. Deterministic checks (run_checks.py)
```json
<paste the --json summary here>
```

## 2. Hard gates (applicable subset)
| HF | applies? | pass? | evidence (line/section) |
|---|---|---|---|
| HF-1 fabricated code state | yes/no | pass/FAIL | <cite> |
| HF-8 needs chat context | yes | pass/FAIL | <cite> |
| HF-9 traceability front-matter | yes | pass/FAIL | <cite> |

> If any applicable hard gate FAILS → VERDICT is FAIL; do not score the rubric; list blockers.

## 3. Soft rubric (only if hard gates pass)
| dimension | score /5 | weight | justification (cite) |
|---|---:|---:|---|
| Factual accuracy | | 20 | |
| Information architecture | | 15 | |
| Actionability | | 15 | |
| Evidence traceability | | 15 | |
| Uncertainty expression | | 10 | |
| Reader fit | | 10 | |
| Maintainability | | 10 | |
| Concision | | 5 | |
| **total (normalized 0–100)** | | | |

## 4. No-context reader test
| question | answerable from doc alone? | note |
|---|---|---|
| goal/target | y/n | |
| current state (FACT vs UNKNOWN) | y/n | |
| next step + acceptance | y/n | |
| open questions | y/n | |
| evidence sources | y/n | |

## 5. Prioritized fixes (blockers first)
1. <blocker> — <what to change>
2. <major> — <…>
3. <minor> — <…>
