---
generated_by_skill: project-state-reconstructor
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<repo tree>, <existing status docs treated as claims>]
artifact_type: project-state-report
document_lifecycle: IN_REVIEW
scope: <one line: what state is recovered; excludes designing a target structure (IA's job)>
facts: <pointer+count to 'What runs (FACT)' rows, each with a locator + E-level>
hypotheses: <pointer+count to believed-but-unverified claims>
open_questions: <pointer+count to UNKNOWNs + STALE rows; never 'none' if any UNKNOWN exists>
evidence_level: <max E-level actually substantiated; do not inflate>
next_handoff: goal-scope-and-workflow-elicitor
handoff_requirements: <what the consumer needs: FACT/UNKNOWN split + STALE list + blocking UNKNOWNs>
status: FACT/UNKNOWN separated below
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
---

# State Report — <project>

Facts are **recovered, not inherited**. Old docs are claims until verified.

## Inventory (read-only)
- Entry points: <files>
- Build/deps: <manifests, env>
- Tests: <dirs, count if run>
- Data / results / notebooks: <paths>

## What runs (FACT)
| capability | evidence (file:line / test / command) | evidence level |
|---|---|---|
| <e.g. `solver.run()` executes on the sample input> | `src/solver.py:120`; `tests/test_solver.py::test_smoke` passes | E3 |

## What is tested
| area | tests | status |
|---|---|---|
| <module> | <test files> | <pass/UNKNOWN(blocked: …)> |

## Real progress
- Written vs runs vs tested vs validated — one line each, no inflation.

## Contradicted / STALE claims
| doc | claim | reality (evidence) | marked |
|---|---|---|---|
| `ROADMAP.md` | "phase 2 complete" | phase-2 module imports but has no tests | STALE |

## UNKNOWNs (+ how to resolve)
| unknown | why it matters | how to resolve |
|---|---|---|
| <does experiment X reproduce?> | blocks E4 claim | run `<cmd>`; inspect `<artifact>` |

## Evidence index
- <symbol/claim> → <file:line / test / command output>
