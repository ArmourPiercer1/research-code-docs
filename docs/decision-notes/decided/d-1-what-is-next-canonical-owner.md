# D-1 — "What is next" canonical owner (DECIDED)

<!--
generated_by_skill: manual (Phase-2 vertical slice; records the final external-review ruling — the slice does NOT self-decide, P8)
skill_version: n/a
source_commit: 8a37387
source_documents:
  - docs/plans/active/research_code_docs_phase2_implementation_prompt.md §0/P1 (final external-review ruling, option A, 2026-09-10)
  - docs/plans/active/reconstruction/revised-phase2-vertical-slice.md §6 (note shape)
  - docs/plans/active/reconstruction/README.md (status table — the ruled owner)
status: DECIDED (note records a ruled decision; decision_state: decided)
last_verified: 2026-09-10
-->

```yaml
id: D-1
object_type: design_decision
epistemic_state: supported
decision_state: decided
evidence_level: E3
evidence_state: current
implementation_state: not_applicable
ruling: option A — docs/plans/active/reconstruction/README.md status table is the
  single canonical owner of "current execution status / what is next"
semantic_division: decision register = what has been decided / what remains open;
  system architecture = what the system currently is; status table = what is being
  worked on now and what comes next
problem: after creation-roadmap.md is archived, which document owns "what is next"?
evidence: at 3bb307f the roadmap is VOID (62ada30) yet still the de-facto next-pointer
  (D12 live class; File 3 row 4 split: 4b names the owner); 3 candidate homes exist.
alternatives:
  A: docs/plans/active/reconstruction/README.md status table (the single "what is next"
     owner — File 3 row 4b)
  B: the decision register's active rows (register = decisions, not scheduling)
  C: system-architecture.md (architecture map, not execution status — File 1 Q9)
why: A keeps exactly one "what is next" owner (I2); the status table already carries the
  per-round pointer and is updated in-round by the planning agent; B/C conflate decision
  state with execution status (the D5 class).
consequences: every former roadmap pointer (DQE SKILL.md:9 class) re-points to the status
  table; the roadmap's per-batch statuses are frozen history in the archive.
revisit_condition: if the status table grows beyond one screen of next-actions, or a
  second plan family appears under docs/plans/active/, revisit the single-owner rule.
```

**Implementation of this ruling in the same change (Phase-2 slice):** the VOID
`creation-roadmap.md` was archived to `docs/plans/archived/` (banner intact), its seven live
inbound references (5 files) were re-pointed or labeled (full classified census in the Phase-2
execution record §2), and the
status table row now states the Phase-2 result as "what is next". No generic `status:` field
is part of this note (prompt §2.3) — the six orthogonal fields above carry its state.
