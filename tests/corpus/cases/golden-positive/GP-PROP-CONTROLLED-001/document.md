<!--
generated_by_skill: research-software-proposal-author
skill_version: 0.1.0
source_commit: solverkit@9f2c1a7
source_documents: [adr/ADR-014-cache-keys.md, status/current.md]
document_lifecycle: ACCEPTED
status: DECIDED
last_verified: 2026-08-01
-->

# Technical Proposal — content-addressed result cache for the assembly pipeline

## Problem

The finite-element assembly re-runs the full element loop on every solve, even when the mesh, material
map, and quadrature rule are unchanged. On the `hill-3d` regression this wastes ~40% of wall-clock in
repeated identical assembly. We want to skip assembly when its inputs are unchanged.

## Scope and non-goals

- **In scope:** a content-addressed cache keyed by `(mesh_hash, material_hash, quadrature_id)` for the
  assembled stiffness matrix.
- **Non-goals:** caching the linear solve; distributed / multi-node caches; changing the assembly numerics.

## Proposed design

Introduce an `AssemblyCache` keyed by a 32-byte BLAKE3 digest of the canonicalized inputs. On `assemble()`:
compute the key; on a hit return the cached CSR matrix; on a miss assemble and insert. The cache is
process-local and bounded (LRU, default 8 entries) so memory stays predictable.

## Interface changes

- `assemble(mesh, materials, quad) -> CsrMatrix` gains an internal cache lookup; the public signature is
  unchanged.
- New config `assembly_cache.max_entries: int = 8` and `assembly_cache.enabled: bool` (shipped **false**,
  flipped to true after the rollout gate below).

## Validation plan

- Run benchmarks `hill-3d`, `duct-2d`, `step-2d` with `assembly_cache.enabled` set to false, then true,
  at a fixed seed and fixed config.
- Compare the assembled matrix (Frobenius norm of the difference) and total runtime against the
  `enabled=false` baseline on the same commit.

## Acceptance criteria

- **Correctness:** max ‖K_cached − K_baseline‖_F ≤ 1e-12 on all three benchmarks.
- **Speed:** wall-clock regression ≤ 0 on `hill-3d`; no benchmark slower by > 2%.
- **Memory:** peak RSS increase ≤ 1.1× baseline at `max_entries = 8`.

## Rollout plan

- Land behind `assembly_cache.enabled` defaulting to **false** for one release; enable it in CI on the
  three benchmarks; flip the default to **true** only after the acceptance criteria pass on `main` for
  7 consecutive days.

## Rollback conditions

- If any correctness invariant (‖·‖_F ≤ 1e-12) fails, or a solve diverges that converged without the
  cache, set `assembly_cache.enabled = false` (a single config flip, no code revert) and fall back to the
  direct assembly path, which is never removed.

## Risks and mitigations

- **Hash collision:** a BLAKE3 32-byte digest makes collision negligible; an on-miss recomputation is
  always correct regardless.
- **Stale cache after a numerics change:** the quadrature and material hashes are part of the key, so any
  numerics change changes the key; the cache is also process-local and never persisted.
