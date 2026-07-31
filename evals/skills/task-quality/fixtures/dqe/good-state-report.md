---
generated_by_skill: project-state-reconstructor
skill_version: 0.1.0
source_commit: solverproj@a1b2c3d
source_documents: [repo tree, tests/, ROADMAP.md (treated as claims)]
status: FACT/UNKNOWN separated below
last_verified: 2026-07-28T10:00:00Z
---

# State Report — SolverProj

## Inventory (read-only)
- Entry point: `src/solver.py` (`solve_cg()`), `src/cli.py`
- Build/deps: `pyproject.toml` (numpy, scipy); `.venv` present
- Tests: `tests/` — 12 tests
- Data: `data/sample_A.npz`

## What runs (FACT)
| capability | evidence | level |
|---|---|---|
| `solve_cg()` converges on `sample_A` | `tests/test_solver.py::test_cg_converges` passes | E3 |
| CLI runs end-to-end on the sample | `python -m src.cli data/sample_A.npz` exits 0 | E3 |

## What is tested
| area | tests | status |
|---|---|---|
| CG core | test_solver.py (8) | pass |
| preconditioner | test_precond.py (0) | UNKNOWN (no tests exist) |

## Real progress
- CG core: written, runs, tested (E3). Preconditioner: written, runs, NOT tested.

## Contradicted / STALE claims
| doc | claim | reality | marked |
|---|---|---|---|
| ROADMAP.md | "phase 2 (preconditioner) complete" | module imports but has no tests and no benchmark | STALE |

## UNKNOWNs (+ how to resolve)
| unknown | why it matters | how to resolve |
|---|---|---|
| Does the preconditioner reduce iterations? | blocks any "verified" claim | add `tests/test_precond.py`; benchmark vs no-precond on sample_A |

## Evidence index
- `solve_cg` → `src/solver.py:45`; `tests/test_solver.py::test_cg_converges`
