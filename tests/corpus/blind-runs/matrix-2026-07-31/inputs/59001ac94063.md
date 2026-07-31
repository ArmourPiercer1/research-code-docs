<!--
skill_version: 0.1.0
generated_by_skill: research-software-roadmap-author
source_commit: solverkit@a1b2c3d
source_documents: [architecture.md, status/current.md]
status: DECIDED
last_verified: 2026-07-28
-->

# Roadmap — implicit-solver preconditioner track

> **Scope:** the preconditioner research/build track for the implicit solver.
> **Architecture:** summarized below (≤20 lines); the full module decomposition, data structures, and
> APIs live in [architecture.md](architecture.md). **Current state:** [status/current.md](status/current.md).
> **Non-goals:** the time integrator, the mesh layer, CI.

## Architecture summary (see architecture.md for detail)

The preconditioner is one pluggable stage behind the linear-solve interface `LinearOp.apply()`. Three
families sit behind a common `Preconditioner` trait: block-Jacobi, ILU(k), and an algebraic-multigrid
adapter. Selection is by config, not compile-time. Full class/data-structure detail: architecture.md §2–§4.

## Phase 1 — block-Jacobi baseline · committed · next

- **Goal:** a working block-Jacobi preconditioner behind the trait.
- **DoD:** solves the 3 benchmark systems in `bench/` to 1e-8 in ≤ 200 iterations; wall-clock recorded.

## Phase 2 — ILU(k) · committed

- **Goal:** ILU(k) with configurable fill.
- **DoD:** ≥ 30% iteration-count reduction vs Phase-1 baseline on the same 3 systems, k∈{0,1,2} swept.

## Phase 3 — AMG adapter · deferred

Only meaningful after Phase-2 GO. Scope/DoD defined then; not committed now.

## Open questions

- **OQ-1:** does ILU(2) fill cost outweigh its iteration savings on the largest system? (resolve in Phase-2)
