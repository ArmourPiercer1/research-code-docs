<!--
skill_version: 0.1.0
generated_by_skill: research-software-roadmap-author
source_commit: eoopt@c3d4e5f
source_documents: [status/current.md]
status: DECIDED
last_verified: 2026-07-30
-->

# Research roadmap — Bayesian-optimization (BO) feasibility

> **Scope:** decide whether BO is worth adopting for the surrogate-search stage. This is a **research
> roadmap**: the phase's outcome is a decision, not a shipped feature. Current state: status/current.md.

## Phase 1 — effective-dimension probe · research · committed · next

- **Research question:** after whitening, is the effective dimension of the search space ≤ 8?
- **Minimal experiment:** 3 benchmark problems × 10 random seeds; estimate effective dimension per run.
- **Metric:** median effective dimension across the 30 runs.
- **GO:** median ≤ 8 → adopt BO for the surrogate stage.
  **MODIFY:** 8 < median ≤ 15 → add a dimension-reduction step, then re-evaluate.
  **STOP:** median > 15 → abandon the BO route, stay on CMA-ES; record why in the decision register.
- **Downstream impact:** GO unlocks Phase 2 (kernel selection); STOP closes the BO track.

## Open questions

- **OQ-1:** is whitening by the sample covariance stable enough at n=30? (resolve in Phase 1)
