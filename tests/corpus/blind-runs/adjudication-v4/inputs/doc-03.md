<!--
generated_by_skill: research-software-roadmap-author
skill_version: 0.1.0
source_commit: flowsim@e4f5a6b
source_documents: [state-report.md, references/turbulence-closure-review.md]
status: DECIDED
last_verified: 2026-07-22
-->

# Research Roadmap — data-driven turbulence closure

> **Scope:** the closure-model research track. This is a **research roadmap**: several phases are
> investigations whose outcome is a decision, not a shipped feature. Each research phase states its
> question, minimal experiment, metric, and a GO / MODIFY / STOP gate. Current code state: `status.md`.
> **Non-goals:** the base solver, meshing, the CI pipeline.

## Phase 1 — feasibility probe (research) · committed · next

- **Research question:** does a small MLP closure reduce a-posteriori error vs the algebraic baseline
  on the periodic-hill case?
- **Minimal experiment:** train on 2 Reynolds numbers, test on a 3rd; compare to the baseline.
- **Metric:** time-averaged velocity-profile L2 error at 4 stations.
- **验收（committed · next）：** 与基线对照，效果达标即可，具体算例与阈值届时定。

## Phase 2 — architecture & generalization (research) · committed

- **Research question:** which inductive bias (tensor-basis vs plain MLP) generalizes across geometries?
- **Minimal experiment:** hill + duct + backward-step; leave-one-geometry-out.
- **Metric:** worst-case separation-point error across the 3 geometries.
- **GO / MODIFY / STOP:** GO if worst-case < 10%; MODIFY if 10–25%; STOP if > 25% (route to hybrid).
- **Depends on:** Phase-1 GO.

## Phase 3 — deployment hardening · deferred

Only meaningful after Phase-2 GO. Scope/DoD defined then; not committed now.

## Open questions

- **OQ-3:** train/test Reynolds split — is 2→1 enough signal? (resolve in Phase-1)
- **OQ-4:** realizability enforcement — soft penalty vs hard projection? (Phase-2)
