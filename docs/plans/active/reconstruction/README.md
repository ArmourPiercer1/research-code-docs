# Workflow Reconstruction — Phase 0/1 Working Area

<!--
generated_by: (parent agent, reconstruction kickoff)
scope: deliverables for the Research Software Agent Workflow Reconstruction Charter
status: Phase 0 + Phase 1 COMPLETE + REPAIR ROUND COMPLETE + FINAL CONSISTENCY PATCH
        APPLIED (2026-09-10) + PHASE-2 VERTICAL SLICE COMPLETE (2026-09-10):
        third-party architecture review (12-item contract R1–R12) verified against current main
        and executed; 5 Phase-1 files revised, 3 new docs
        (post-audit-reconciliation, revised-phase2-vertical-slice,
        architecture-review-disposition); ARCHITECTURE ACCEPTED (final external review,
        conditional on the consistency patch); D-1 DECIDED (option A — this README's
        status table is the single canonical "what is next" owner, per the final ruling);
        Phase-2 slice executed per the 2026-09-10 implementation prompt (two commits:
        mechanism + slice; evidence in phase2/execution-record.md); Phase 3 is what is next
date: 2026-09-09 → 2026-09-10 (completion + repair round + final consistency patch + Phase-2 slice)
-->

> Execution home for
> [research_software_agent_workflow_reconstruction_charter.md](../research_software_agent_workflow_reconstruction_charter.md).
> This folder was git-ignored until the final consistency patch P2 (now trackable —
> the tracking transition is a Phase-2 slice step). Phase 0 is **audit-only** (read-only on the
> audited repos); Phase 1 produces the investigation + architecture proposal. Per charter §15,
> broad implementation starts only after the architecture review at the end of Phase 1.

## Execution status / what is next (D-1 single owner)

> Per **D-1** (final external-review ruling, option A; recorded in
> `docs/decision-notes/decided/d-1-what-is-next-canonical-owner.md`), this table is the SINGLE
> canonical owner of "current execution status / what is next". Decision STATE lives in
> `docs/decision-register.md` (row 7); what the system currently IS lives in
> `docs/skill-development/system-architecture.md`. The VOID `creation-roadmap.md` is frozen history
> in `docs/plans/archived/` — its per-batch statuses are no longer live.

| Phase | Status | Evidence | What is next |
|---|---|---|---|
| Phase 0 (read-only audit) | **COMPLETE** 2026-09-09 | `phase0/` deliverables (status table below) | — |
| Phase 1 (investigation + architecture proposal) | **ACCEPTED** 2026-09-10 — architecture-review round done; final external review ACCEPTED conditional on the consistency patch; P1–P8 applied | `architecture-review-disposition.md` §9 (8/8 focused consistency checks PASS); deliverable status table below | — |
| Phase 2 (vertical slice: minimum checkers + A8/A9 + ONE candidate + canonical stores) | **COMPLETE** 2026-09-10 (awaiting external review) | two commits: `8a37387` (mechanism: 4 Phase-2 lints + register_check merge + A8/A9 + eval datasets + registry) + the slice commit (archive move of the VOID roadmap, 7 inbound refs re-pointed, stores created: decision-notes/ + decision-register.md + canonical-source-map.md, tracking transition of `docs/plans/active/**` + `archived/**`); full evidence: `phase2/execution-record.md` | external review of the slice (ACCEPT / patch) |
| Phase 3 (apply-mode A1 + deferred checkers + remaining tracking) | **PLANNED** — next after Phase-2 review | scope: charter + R11 deferred list (6 checkers) + R12 parked gaps (A2/A3/A4/A6) + D19 tracking (snapshots/corpus) + ADR-DQE-001 note migration + packaging of A8/A9 into the next release manifest | begin when the Phase-2 slice review is ACCEPTED |

## Layout

```text
reconstruction/
├── README.md                     (this file)
├── execution-notes.md            parent-agent orchestration state (subagent map, round plan)
├── post-audit-reconciliation.md  REPAIR ROUND (R1) — D1–D19/P1–P10 re-verified against current main
├── revised-phase2-vertical-slice.md  REPAIR ROUND (R9) — the current slice (supersedes File 2 §7 original)
├── architecture-review-disposition.md  REPAIR ROUND — per-item disposition of R1–R12 + guide §§13–21
├── phase0/
│   ├── current-system-map.md             Phase 0 deliverable — factual map of the existing system (§3.1)
│   ├── existing-skill-classification.md  Phase 0 deliverable — KEEP/REFINE/MERGE/SPLIT/REPLACE/ADD/REMOVE (§3.2)
│   ├── current-information-ownership-map.md  Phase 0 deliverable — canonical owners + duplications (§8.2, §13)
│   └── pain-point-evidence.md            Phase 0 deliverable — most expensive real failure modes (§3.3, §17)
├── phase1/
│   ├── dsh-workflow-evidence-map.md      Phase 1 deliverable — §5 evidence chains for DSH mechanisms
│   ├── dsh-transferability-crosswalk.md  Phase 1 deliverable — §5.3 crosswalk table + §7 labels
│   ├── target-workflow-invariants.md     Phase 1 deliverable — §8 invariants + current-state compliance
│   ├── target-capability-architecture.md Phase 1 deliverable — §9 capability model + §10 mechanism decisions
│   ├── canonical-information-model.md    Phase 1 deliverable — §13 canonical-source map for the target
│   ├── skill-change-matrix.md            Phase 1 deliverable — §11 proposed portfolio (YAML schema)
│   └── eval-plan.md                      Phase 1 deliverable — §14 evaluation strategy, concretized
├── phase2/
│   ├── execution-record.md               Phase-2 slice record — Stage-0 state, census, A8 report,
│   │                                     A9 verification record, before/after evidence, two-axis review
│   └── impact-declaration.yaml           the slice's change contract (canonical_impact_lint input)
└── intermediate/
    ├── dsh-current-state-findings.md     raw evidence — DSH current mechanisms (input to evidence map)
    ├── dsh-history-findings.md           raw evidence — DSH git history + negative evidence (§5, §6)
    ├── brief-s1.md                       synthesis prompt — DSH evidence map + crosswalk
    ├── brief-s2.md                       synthesis prompt — target architecture 5-file set
    ├── parent-preliminary-answers.md     parent's preliminary §17 answers (S2 input)
    ├── check_deliverables.py             verification tool — 13 deliverables, 5 gates
    ├── eval_coverage_baseline.py         ground-truth per-skill case-count builder
    └── eval-coverage-baseline.md         ground truth — eval coverage per skill
```

## Status (verified 2026-09-10 via intermediate/check_deliverables.py — ALL PRESENT & SANE)

| Deliverable | Status | Size / citations |
|---|---|---|
| phase0/current-system-map.md | ✅ DONE | 76.2KB / 413 |
| phase0/existing-skill-classification.md | ✅ DONE | 30.7KB / 297 (KEEP15 REFINE7 SPLIT1 MERGE1 REPLACE1 REMOVE1) |
| phase0/current-information-ownership-map.md | ✅ DONE | 39.5KB / 330 (17 types, 8 unowned, D1–D19) |
| phase0/pain-point-evidence.md | ✅ DONE | 32.3KB / 207 (P1–P10) |
| intermediate/dsh-current-state-findings.md | ✅ DONE | 73.5KB / 349 (M1–M32) |
| intermediate/dsh-history-findings.md | ✅ DONE | 86.9KB / 431 (46 negative-evidence items) |
| phase1/dsh-workflow-evidence-map.md | ✅ DONE | 83.7KB / 520 (32×9-link chains, C1–C15) |
| phase1/dsh-transferability-crosswalk.md | ✅ DONE | 32.7KB / 375 (32 rows; DT5/TAG12/RSA2/DN13) |
| phase1/target-workflow-invariants.md | ✅ DONE | 57.6KB / 416 (12 invariants: 0 SAT / 8 PARTIAL / 4 VIOLATED; §17 17/17 answered) |
| phase1/target-capability-architecture.md | ✅ DONE | 41.1KB / 211 (33 capabilities; slice = PSR→WFI→UDM→LDM→checkers) |
| phase1/canonical-information-model.md | ✅ DONE | 20.0KB / 112 (17 owner rows, explicit Δ) |
| phase1/skill-change-matrix.md | ✅ DONE | 84.6KB / 571 (36 entries, 32/32 agree with phase0) |
| phase1/eval-plan.md | ✅ DONE | 30.2KB / 144 (229 carried cases, 12 adversarial defects, N=25 longitudinal) |

Consistency checks (parent, Round 3): classification labels ↔ matrix proposed_action
36/36 match; I1–I12 referenced set = defined set (no orphans); M1–M32 evidence-map
coverage = crosswalk 32 rows; canonical-model deltas explicit (Δ column + §2 summary);
0 residual PENDING/TODO placeholders; 9-item parent discrepancy list resolved
(229/41 case count verified by independent recount; 18 commits; day-one CLAUDE.md
symlink; queue.md absent; D-17 split; registry path; snapshot wording).

## Repair round (2026-09-10, third-party architecture review)

Contract: `docs/plans/active/research_code_docs_phase1_architecture_repair_guide.md`
(R1–R12). Verified against current main (3bb307f, 23 commits) and executed in-place:

- All 12 repair items ACCEPTED (no rejections) — per-item disposition + evidence +
  change_made + residual_risk in `architecture-review-disposition.md`.
- Revised: the 5 Phase-1 deliverables above (invariants, canonical-information-model,
  eval-plan, target-capability-architecture, skill-change-matrix).
- New: `post-audit-reconciliation.md` (R1), `revised-phase2-vertical-slice.md` (R9),
  `architecture-review-disposition.md`.
- Key design changes: R2 canonical-impact-lint (change-impact discharge replaces
  timestamp-as-correctness); R3 decision folders `proposed/decided/rejected/archived/`
  + orthogonal `implementation_state`; R4 revised 6-field state schema, tested on 13
  REAL entries before freezing (File 1 §I4.1); R5 five explicit rejection bases;
  R6 one authority per fact type (row 4→4a/b/c, row 6→6a/b/c) + single manual
  canonical source map `docs/canonical-source-map.md`; R7 registry graph owns
  relations (lint = integrity only); R8 prior/posterior labels (KEEP×15 census fix);
  R9 slice redesigned (real repo, one candidate, minimum checkers, D-1 decision note);
  R10 eval anti-gaming (baseline diagnostic, decision-value-first, planted
  obsolescence, counts as indicators); R11 Phase-2 checker minimum set (4) + 6
  deferred; R12 A2/A3/A4/A6 parked capability gaps.
- One live-repo edit in the repair round: `skills-registry.yaml:20` `meta.isolation`
  (D6 residual, cites 4df8f7f). Everything else was docs under this folder (now
  trackable — final patch P2).
- Gate status (guide §20): 14/14 items done; D-1 is now **DECIDED** (final external-
  review ruling, option A — this README's status table; guide §20's "mark, don't
  silently choose" was honored: the ruling arrived as the final review's explicit
  decision, recorded in the D-1 note, not chosen by the slice).
- §16 consistency pass: 12/12; §19 do-NOT list: 15/15 complied; guide citation
  corrections recorded in the disposition doc.

## Final consistency patch (2026-09-10)

Final external review: **ACCEPTED WITH REQUIRED CONSISTENCY PATCH; Phase 2 GO**. The
patch (P1–P8) is applied in place; per-item status + the 8 focused consistency checks
(11.1–11.8, all PASS) are recorded in `architecture-review-disposition.md` §9:

- P1: D-1 ruled **option A** — this README's status table is the single canonical
  owner of "current execution status / what is next" (decision register = decided/
  open; architecture = what the system is; status table = what is worked on next).
- P2: blanket `docs/plans/` ignore removed — `docs/plans/active/**` +
  `docs/plans/archived/**` trackable; `local/` + `scratch/` the explicit ephemeral
  dirs; the tracking transition (git add) is a Phase-2 slice step (Stage 5).
- P3: zero live `kind` schema usages in the target set.
- P4: Phase-2 exit criteria = the revised slice's success criteria; no Phase-2 gate
  depends on a deferred checker.
- P5: `persistent_artifact_count` = REPORT ONLY + 5 semantic failure predicates (no
  ≤2 hard gate).
- P6: I4.1 coverage reported honestly (13 real entries; 7/7 real + 7/7 synthetic;
  the archive-roadmap entry is a design_decision, not a renamed route).
- P7: the route table is a generated/non-authoritative view of the register in every
  file that mentions it.
- P8: Phase-2 canonical stores named in the slice (§4.5: decision-notes/ + register
  seed rule, canonical-source-map.md, tracked plans dirs).

## Audit scope note (charter §2)

- `research-code-dev` = **former name of this repo** (commit `b0e62c4`); no second local repo exists.
- `D:\AI_Coworking\skill-build\research-skills` and `D:\AI_Coworking\skill-build\research-set`
  are the external L3 research stack (lit-review, wos-research, scansci-pdf, mineru-ocr,
  paper-fetch-skill) — audited at interface level only.
- DSH reference checkout: `D:\deepseek-harness\` (read-only).
