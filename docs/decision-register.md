---
generated_by_skill: manual (Phase-2 vertical slice, per 2026-09-10 implementation prompt §6 — store seeded with decided items only, no backfill)
skill_version: n/a
source_commit: 8a37387
source_documents: [docs/plans/active/research_code_docs_phase2_implementation_prompt.md §6, references/templates/decision-register.template.md, docs/canonical-source-map.md §A row 7]
artifact_type: decision-register
document_lifecycle: ACCEPTED
scope: Single source of truth for the decision STATE this repo tracks; records state, does not decide the gate. Seeded in the Phase-2 slice with exactly two entries (D-1 + the reconstruction program route) — no backfill of historical items.
facts: 2 DECIDED entries (D-1 E3; R-001 E3) — both E3 in-project, both verified against tracked docs
hypotheses: none seeded (the store is new; hypothesis entries enter when routes are proposed, R4 schema)
open_questions: none tracked in this register at seed time (open items enter as they arise; "none" is never used while an item is unsettled)
evidence_level: E3 across entries (paper/analogy would carry the RES cap ≤ E2)
next_handoff: documentation-quality-evaluator (advisory) + human decision at the gate
handoff_requirements: per-entry status + evidence + re-openable locator + supersede chain + unresolved gaps (none at seed)
status: DECIDED (register is the live source for decision state)
last_verified: 2026-09-10
---

# Decision Register — research-code-docs

The single source of truth for decision STATE (row 7 of `docs/canonical-source-map.md`). Durable
rationale lives in `docs/decision-notes/` (row 8) — this register records state and LINKS to the
note; it never carries rationale prose. Entries use the R4 revised schema (invariants I4.1):
`object_type / epistemic_state / decision_state / evidence_level / evidence_state /
implementation_state` — the R4 fields are the entry model; the `status:`/`evidence:` claim pair on
each entry is required by `register_check` (H2, HARD tier) for state validation and is orthogonal
to the R4 lifecycle fields — prompt §2.3 forbids a MIXED generic status, which this does not
recreate: claim status and decision_state coexist without ambiguity, and
`references/templates/decision-register.template.md` defines the same pair. Reversal is by
SUPERSEDE (append + point back), never by editing a decided entry. Status + evidence vocabulary:
`docs/skill-development/system-architecture.md` §7. Only E3+ may be called verified.

## Register

```yaml
# One entry per tracked decision. source = a re-openable LOCATOR (file:line / commit / run-id),
# never a bare name. Reversal is by SUPERSEDE (append new + point back), never by editing.
- id: D-1
  statement: "The status table in docs/plans/active/reconstruction/README.md is the single canonical owner of 'current execution status / what is next' (option A)."
  status: DECIDED
  evidence: E3
  source: "docs/plans/active/research_code_docs_phase2_implementation_prompt.md (final external-review ruling P1, 2026-09-10) + docs/plans/active/reconstruction/revised-phase2-vertical-slice.md §6"
  disposition: supported
  decided_by: "final external-review ruling @ 2026-09-10 (recorded by the Phase-2 slice — a recording of a ruling, not a self-decided fiat, P8)"
  object_type: design_decision
  epistemic_state: supported
  decision_state: decided
  evidence_level: E3
  evidence_state: current
  implementation_state: not_applicable
  proof_context: "rationale note: docs/decision-notes/decided/d-1-what-is-next-canonical-owner.md (alternatives B/C considered and rejected; semantic division of the three authorities)"
  last_verified: "2026-09-10"
  notes: "Ruling recorded in the same change that archived the VOID creation-roadmap.md; the note's implementation_state is not_applicable — a ruling has no implementation concept (R3 case B / I4.1 entry 1)."

- id: R-001
  statement: "The reconstruction program routes: charter -> Phase 1 (ACCEPTED) -> Phase 2 vertical slice (COMPLETE 2026-09-10) -> Phase 3 (stores complete, apply-mode A1 + deferred checkers) per the charter and its amendments."
  status: DECIDED
  evidence: E3
  source: "docs/plans/active/reconstruction/README.md status table (Phase-1 ACCEPTED; Phase-2 COMPLETE) + docs/plans/active/research_software_agent_workflow_reconstruction_charter.md"
  disposition: supported
  decided_by: "user-approved charter + Phase-1 acceptance (in-project, tracked docs)"
  object_type: route
  epistemic_state: supported
  decision_state: decided
  evidence_level: E3
  evidence_state: current
  implementation_state: none
  proof_context: "route state is the canonical mutable state for routes (row 4c); the status table is the execution-status view, not this entry's locator"
  last_verified: "2026-09-10"
  notes: "Program-level route seed (the register's first route object — Q15 'routes get a real object'). implementation_state: none per slice §4.5 (seed rule) — per-phase implementation progress lives in the status table, not in this seed. Phase-3 content: ADR-DQE-001 note migration, remaining git-tracking targets (D19 snapshots/corpus), deferred lints (R11 list)."
```

## Change log

| date | id | change |
|---|---|---|
| 2026-09-10 | D-1 | created as DECIDED — final external-review ruling (option A) recorded by the Phase-2 slice; note in `docs/decision-notes/decided/` |
| 2026-09-10 | R-001 | created as DECIDED route seed — reconstruction program route (Phase 3 pending); implementation_state none (slice §4.5 seed rule) |
