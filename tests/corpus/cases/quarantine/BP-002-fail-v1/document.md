<!--
skill_version: 0.1.0
generated_by_skill: scientific-software-architect
source_commit: meshkit@f7a1b20
source_documents: [status/current.md]
status: DECIDED
last_verified: 2026-07-31
-->

# Architecture — adaptive mesh refinement (AMR) core

> **Scope:** the stable design of the AMR core. This is a **design document**.

## Design

The AMR core is organized around an immutable `Forest` of octree roots and a `RefinementPolicy` that
marks cells for split/coarsen. The `Balancer` enforces the 2:1 constraint after each mark pass. The
design goal is that refinement is deterministic given `(Forest, Policy, seed)`.

## Module boundaries

- `forest` owns topology; no numerics.
- `policy` is pure: `mark(&Forest, &Field) -> MarkSet`; no mutation.
- `balancer` transforms a `MarkSet` into a 2:1-legal `MarkSet`.

## Maturity snapshot

当前 69 项测试全部通过，`forest`、`policy`、`balancer` 三个模块都已就绪。The core is done.

## Open questions

- **OQ-2:** should the balancer be incremental or full-rebuild per adapt step? (design review in progress)
