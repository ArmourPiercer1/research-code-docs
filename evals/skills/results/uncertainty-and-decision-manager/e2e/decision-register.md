---
generated_by_skill: uncertainty-and-decision-manager
skill_version: 0.2.0
source_commit: "udm-e2e@scenario"
source_documents: [goal-scope-note.md, prototype-results.md, early-notes.md, Benzi-2002-review.bib]
status: DECIDED (register is the live source for uncertainty)
last_verified: 2026-07-30T09:47:06Z
---

# Decision Register — matrix-free numerical solver

The single source of truth for uncertain items in this solver project. Stable, decided
terms graduate to the `domain-modeling` glossary; plain code-behaviour facts live in the
state report. Status + evidence vocabulary follows system-architecture §7. Only E3+
(in-project proof) may be phrased "verified"; a peer-reviewed or sibling-domain result is
capped at E2 until reproduced here. Decided items are append-only — a reversal appends a
new entry and marks the old one STALE with a back-reference and a reason, never editing in
place.

## Register

```yaml
# One entry per tracked item. status in {FACT,VERIFIED,DECIDED,BASELINE,HYPOTHESIS,
# CANDIDATE,OPEN,DEFERRED,REJECTED,STALE}; evidence in {E0..E5}; source = a re-openable
# LOCATOR (file:line / test-id / experiment-run-id / bench-path / DOI#section), never a name;
# disposition in {supported, needs-evidence, needs-experiment}. Only E3+ may be VERIFIED/FACT.
# Reversal is by SUPERSEDE (append new + point back), never by editing a decided item.

- id: D-001
  statement: "Use a matrix-free CG solver as the linear-system baseline."
  status: BASELINE
  evidence: E3
  source: "prototype-results.md#cg-vs-direct  (in-project prototype run @ commit a1b2c3d, seed=0)"
  disposition: supported
  decided_by: "user @ 2026-07-30"
  proof_context: "commit a1b2c3d; seed=0; dataset=sample_A.npz; metric=iters=41 (converged)"
  supersedes: X-000
  discharge:
    attempted: "adversarial disproof — re-ran the large-N memory scaling that killed the LU baseline"
    findings: "matrix-free CG never forms the system matrix; memory stays O(N), no blow-up at N>1e5"
    disposition: "held — promoted CANDIDATE -> BASELINE"
  alternatives:
    - "X-000 direct LU solver — REJECTED: dense factor memory O(N^2), blew up at N>1e5"
    - "H-002 incomplete-Cholesky preconditioning — not yet tried in-project (stays HYPOTHESIS)"
  last_verified: "2026-07-30"
  notes: "Structural commitment. E3 in-project proof carries proof_context; if commit/seed/dataset change it auto-transitions to STALE until re-proven."

- id: H-002
  statement: "Incomplete-Cholesky preconditioning will cut CG iterations >2x."
  status: HYPOTHESIS
  evidence: E2
  source: "Benzi 2002 review, DOI:10.1006/jcph.2002.7176#sec3  (sibling-domain, peer-reviewed — NOT in-project)"
  disposition: needs-experiment
  decided_by: null
  last_verified: "2026-07-30"
  notes: "E2 cap: published but sibling-domain and never run here, so not 'verified'. An in-project prototype reproducing the >2x speedup (commit+seed+dataset) would raise it toward E3."

- id: Q-003
  statement: "What accuracy (tolerance) does the downstream step actually require?"
  status: OPEN
  evidence: E0
  source: "goal-scope-note.md#open-decisions  (user-preference; UNVERIFIED)"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-07-30"
  notes: "Open question — kept alive across versions. Blocks the CG stopping-tolerance choice; needs a downstream/user answer, not a guess (HF-7)."

- id: X-000
  statement: "(superseded) Use a direct LU solver as the linear-system baseline."
  status: STALE
  evidence: E3
  source: "early-notes.md#lu-baseline  (in-project, superseded)"
  disposition: supported
  superseded_by: D-001
  reason: "Reversed after a memory blow-up at large N — dense LU factor is O(N^2) and exceeded RAM for N>1e5. Kept for the audit trail, not deleted."
  proof_context: "held on small N only; invalid at N>1e5 (the failing condition that triggered the reversal)"
  last_verified: "2026-07-30"
  notes: "Not edited in place — this row survives the reversal alongside its replacement D-001 (append-only)."
```

## Change log

| date | id | change |
|---|---|---|
| 2026-07-24 | X-000 | created as BASELINE (direct LU solver) |
| 2026-07-29 | X-000 | marked STALE — memory blow-up at N>1e5; superseded_by D-001 (reason recorded) |
| 2026-07-30 | D-001 | created as BASELINE after matrix-free CG prototype (41 iters, seed=0); supersedes X-000 |
| 2026-07-30 | H-002 | recorded HYPOTHESIS at E2 (Benzi 2002, sibling-domain); disposition needs-experiment |
| 2026-07-30 | Q-003 | recorded OPEN — downstream accuracy requirement unknown; disposition needs-evidence |
