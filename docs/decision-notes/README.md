# Decision Notes — lifecycle store

<!--
generated_by_skill: manual (Phase-2 vertical slice, per 2026-09-10 implementation prompt §6)
skill_version: n/a
source_commit: 8a37387
source_documents:
  - docs/plans/active/research_code_docs_phase2_implementation_prompt.md §6 (stores)
  - docs/plans/active/reconstruction/phase1/canonical-information-model.md row 8 (owner + lifecycle + format)
  - docs/canonical-source-map.md §A row 8 (live owner table)
status: DECIDED (store created; D-1 is the first note)
last_verified: 2026-09-10
-->

**Owner row:** canonical-source-map §A row 8 — durable decision rationale lives ONLY here;
`docs/decision-register.md` (row 7) tracks STATE and links here for rationale; the register never
carries rationale prose.

## Lifecycle (folders = decision lifecycle, NOT implementation lifecycle — R3)

| Folder | decision_state | Semantics |
|---|---|---|
| `proposed/` | `proposed` | proposal-oriented wording; open for amendment |
| `decided/` | `decided` | rewritten to present-tense ACCEPTED REALITY, without implying implementation completion |
| `rejected/` | `rejected` | FROZEN: reason + non-empty `rejection_basis` (R5) + revisit condition |
| `archived/` | `decided` / `rejected` / `deferred` / `superseded` | SEALED: relocation, never edit (M18); low-value decided notes move here at release boundaries |

`implementation_state` is a FIELD on the note (`none` / `not_applicable` / `planned` /
`in_progress` / `implemented` / `blocked`) — it is never inferred from the folder. A decision can
be `decided` with implementation `not_applicable` (e.g. D-1: a ruling with no implementation
concept).

## Note format (enforced by `decision_note_lint.py`, HARD tier)

Each note carries an `id:` + the six orthogonal state fields (R4 revised schema, I4.1) + the seven
required content sections:

```text
problem (or question) · decision · evidence_basis (or evidence) ·
alternatives (or alternatives_considered) · why · consequences · revisit_condition
```

Legal values: `object_type ∈ {claim, route, experiment, design_decision, requirement, artifact}`;
`epistemic_state ∈ {unknown, hypothesis, inferred, observed, supported, contradicted}`;
`decision_state ∈ {not_applicable, proposed, decided, rejected, deferred, superseded}`;
`evidence_level ∈ {E0..E5}`; `evidence_state ∈ {current, stale, contradicted}`;
`implementation_state ∈ {not_applicable, none, planned, in_progress, implemented, blocked}`.
A generic `status:` field is NOT part of the note format (prompt §2.3). Superseded notes carry a
dated `superseded_by` + annotation (supersession-lint).

## Seed and migration

- **D-1** (`decided/d-1-what-is-next-canonical-owner.md`) — first note; records the final
  external-review ruling (option A) — a RECORDING of a ruling, not a self-decided fiat (P8).
- **ADR-DQE-001** (`adr/ADR-DQE-001-*.md`) — MIGRATES in as `decided/` in Phase 3 (its
  implementation_state is `implemented`; that state is a field, not the folder name).
- `archived/` starts empty on purpose; `.gitkeep` files keep the four lifecycle folders tracked.
