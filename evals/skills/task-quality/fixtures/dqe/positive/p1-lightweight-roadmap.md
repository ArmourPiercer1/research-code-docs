<!--
generated_by_skill: research-software-roadmap-author
skill_version: 0.1.0
source_commit: solverproj@a1b2c3d
source_documents: [state-report.md, decision-register.md]
status: DECIDED
last_verified: 2026-07-20
-->

# Roadmap — SolverProj preconditioner track

> **Scope:** the preconditioner track only. Current implementation state lives in `status.md`
> (single source of truth); this roadmap owns the *plan*, not live progress.
> **Non-goals:** the CG core (done, frozen), the CLI, distributed execution.

## Phase 1 — block-Jacobi preconditioner  · committed · next

- **Goal:** cut CG iteration count on `sample_A` with a block-Jacobi preconditioner.
- **Depends on:** the CG core interface (frozen, `src/solver.py`).
- **Deliverables:** `src/precond/block_jacobi.py`; wired into `solve_cg(precond=...)`.
- **Definition of Done (measurable):** on `sample_A`, iteration count drops **≥ 30%** vs no
  preconditioner, wall-clock does not regress, and `tests/test_precond.py` (new) passes.
- **Risks:** block size selection may be problem-dependent (tracked as OQ-7).

## Phase 2 — ILU(0) preconditioner  · committed

- **Goal:** add an ILU(0) option for stiffer matrices.
- **Depends on:** Phase 1 (the `precond=` seam).
- **Deliverables:** `src/precond/ilu0.py`.
- **Definition of Done (measurable):** on `sample_B` (stiff), ILU(0) converges in **≤ 50 iters**
  where block-Jacobi needs > 200; both pass `tests/test_precond.py::test_ilu0`.
- **Risks:** fill-in memory cost.

## Phase 3 — adaptive selection  · deferred (待调研)

Choose the preconditioner automatically from a cheap matrix probe. Deferred: the selection heuristic
is an **open research question** (OQ-8) — needs the Phase-1/2 benchmarks first. DoD to be defined when
promoted; not committed here.

## Open questions

- **OQ-7:** block size — fixed, or scaled to bandwidth? (resolve with a Phase-1 sweep)
- **OQ-8:** adaptive selection metric. (resolve after Phase-1/2 data)
