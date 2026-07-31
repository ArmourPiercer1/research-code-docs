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
> **Non-goals:** the time integrator, the mesh layer, CI.

## Full architecture (inlined here so it is all in one place)

The preconditioner is one pluggable stage behind `LinearOp.apply()`. Three families sit behind a common
`Preconditioner` trait.

### Module decomposition
- `precond/core.rs` — the `Preconditioner` trait: `setup(&Matrix)`, `apply(&Vec) -> Vec`, `teardown()`.
- `precond/block_jacobi.rs` — block extraction, dense inverse per block, block size from config.
- `precond/ilu.rs` — symbolic factorization, level-of-fill `k`, numeric factorization, triangular solves.
- `precond/amg.rs` — coarsening, interpolation, V-cycle; wraps the external `hypre` adapter.

### Data structures
`BlockMap { starts: Vec<usize>, size: usize }`; `IluFactors { l: CsrMatrix, u: CsrMatrix, perm: Vec<usize> }`;
`AmgHierarchy { levels: Vec<Level>, smoother: SmootherCfg }`. See the class diagram in the appendix.

### API surface
`build_preconditioner(cfg: &PrecondCfg, a: &Matrix) -> Box<dyn Preconditioner>` … (18 more signatures) …

## Current status (live)

| Phase | 完成状态 | tests |
|---|---|---|
| Phase 1 block-Jacobi | ✅ 完成 (2026-07-25) | 47/47 green |
| Phase 2 ILU(k) | 🔨 进行中 | 31/47 green today |
| Phase 3 AMG | 未开始 | — |

Right now **78 of 94** total preconditioner tests pass on `main`.

## Phase 1 — block-Jacobi baseline · committed · next

- **DoD:** solves the 3 benchmark systems in `bench/` to 1e-8 in ≤ 200 iterations.

## Phase 2 — ILU(k) · committed

- **DoD:** ≥ 30% iteration-count reduction vs Phase-1 baseline, k∈{0,1,2} swept.

## Phase 3 — AMG adapter · deferred

Scope/DoD defined after Phase-2 GO.

## Session note (本轮 AskUserQuestion)

用户决定：本轮先把 ILU(2) 的 fill 上限设为 12；AMG 家族的 hypre 版本蓝本待补充调研；block 大小默认取 8。
These decisions were made in today's working session and are recorded here for continuity.

## Open questions

- **OQ-1:** does ILU(2) fill cost outweigh its iteration savings on the largest system?
