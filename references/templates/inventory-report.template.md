---
generated_by_skill: workspace-forensics-and-inventory
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<repo tree / corpus tree>, <existing status docs listed as claims, not verified>]
status: read-only inventory (candidates + signals; nothing verified as running)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
---

# Inventory — <workspace-or-corpus>

**Mode:** workspace | document-corpus
Read-only. Every classification is a **candidate tagged with its structural signal** — nothing here is a
claim that code runs, is tested, or is the canonical truth (that is `project-state-reconstructor`'s job).

## Project Map (one line per directory)
| dir | purpose-guess | files | notable types | coverage |
|---|---|---|---|---|
| `src/` | solver package (guess) | 24 | `.py` | fully-scanned |
| `results/` | produced outputs | 310 | `.csv`,`.png` | summarized-only (generated) |

## Coverage note
- Fully scanned: <dirs>. Summarized-only: <dirs>. Skipped (with reason): <dirs, e.g. `.venv/` deps>.

## Artifact buckets — workspace mode (each entry: `path → signal`)
- **Entry-point candidates:** `run.py` (signal: `__main__` guard); `Snakefile` (signal: workflow file).
- **Build / deps / config:** `pyproject.toml`, `environment.yml`.
- **Tests:** `tests/` (`test_*.py`, `conftest.py`).
- **Experiment / analysis scripts:** `experiments/sweep.py`, `analysis.ipynb`.
- **Results & produced artifacts:** `results/*.csv`, `figures/*.png` (GENERATED).
- **Caches & generated:** `__pycache__/`, `.ipynb_checkpoints/` (GENERATED — not source).
- **Data:** `data/*.h5`.
- **Docs:** `README.md`, `docs/`, `status/`.

## Doc-type table — document-corpus mode
| file | doc-type (candidate) | signal | mixed? |
|---|---|---|---|
| `ROADMAP.md` | roadmap | phase headings + DoD | mixed: also holds a status log |

## Orphans & unreferenced (candidates — cite the search)
| item | kind | signal (why candidate) | scan boundary |
|---|---|---|---|
| `old_plot.py` | orphan-candidate | no import/reference found in scanned set | searched `src/`,`experiments/` |
| `results/run17.csv` | unreferenced-artifact | no producing script found | searched `*.py` writers |

## Candidate canonical sources (per information type — CANDIDATE, confirmed later)
| info type | candidate source | signal |
|---|---|---|
| current behavior | `src/solver.py` | imported by entry point |
| progress | `status/README.md` | only status-like doc |

## Contradiction / overlap candidates (corpus mode — flag only, do not resolve)
| statement A (loc) | statement B (loc) | note |
|---|---|---|
| `ROADMAP.md`: "phase 2 done" | `status/README.md`: "phase 2 in progress" | contradiction candidate |

## Handoff (unknowns + questions for the next skill)
- To `project-state-reconstructor`: verify whether `run.py` actually executes end-to-end; confirm orphan
  candidates; resolve the phase-2 contradiction.
- To `document-information-architect` (corpus mode): `ROADMAP.md` mixes roadmap + status → split candidate.
