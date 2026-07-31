<!--
generated_by_skill: scientific-software-architect
skill_version: 0.1.0
source_commit: meshkit@c7d8e9f
source_documents: [decision-register.md (ADR-1..6), status.md]
status: DECIDED
last_verified: 2026-07-24
-->

# Architecture — MeshKit adaptive mesh library

> **Primary responsibility:** the architecture of MeshKit (module boundaries + the extension seams).
> This is a single design document. Appendices A–B are **subordinate** to it (a risk log and a
> validation plan that exist only to support the architecture). **Update mechanism:** this doc changes
> only when an ADR changes the architecture; **live implementation status is NOT here — see `status.md`**;
> **test counts/CI are NOT here — see the CI dashboard.** Rationale for each decision lives in the ADR
> it cites; this doc does not restate it.

## 1. Module boundaries

```
io/         ← mesh readers/writers (format adapters)
  → core/   ← topology + geometry kernel (stable; ADR-1)
  → adapt/  ← refinement/coarsening strategies (pluggable; ADR-3)
  → quality/← element quality metrics (pluggable; ADR-4)
```

Dependency direction is one-way `io → core → {adapt, quality}`. The kernel depends on nothing above it.

## 2. Extension seams

- **Refinement strategy** (`adapt/base.py :: Strategy`): red-green, longest-edge, or custom. Chosen at
  runtime. Why a seam and not a switch: strategies are research-volatile (ADR-3, with the rejected
  "single hard-coded strategy" alternative and its consequences).
- **Quality metric** (`quality/base.py :: Metric`): scaled-Jacobian, aspect-ratio, or custom (ADR-4).

## 3. Data model

Half-edge topology in `core/topology.py`; geometry is a separable backend (ADR-2 records why geometry
is not baked into topology, the rejected "fat vertex" alternative, and the consequence for memory).

---

## Appendix A — Risk log (subordinate to §2)

| Risk | Mitigation | Owner doc |
|---|---|---|
| Strategy seam over-abstracts | keep 2 built-ins until a 3rd real need | ADR-3 |
| Geometry backend perf | benchmark before adding a 2nd backend | ADR-2 |

## Appendix B — Validation plan (subordinate to the architecture)

Each seam ships with a conformance test suite (the *plan*, not results — results live in CI):
- refinement: every `Strategy` preserves a valid half-edge mesh on the 5 conformance meshes.
- quality: every `Metric` returns values in its declared range on degenerate + regular elements.
