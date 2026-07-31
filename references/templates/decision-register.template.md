---
generated_by_skill: uncertainty-and-decision-manager
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [goal-scope-note.md, evidence-matrix.md, prototype-results.md]
status: DECIDED (register is the live source for uncertainty)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
---

# Decision Register — <project>

The single source of truth for uncertain items. Stable, decided terms graduate to the
`domain-modeling` glossary; code facts live in the state report. Status + evidence
vocabulary: see system-architecture.md §7. Only E3+ may be called "verified".

## Register

```yaml
# One entry per tracked item. status ∈ {FACT,VERIFIED,DECIDED,BASELINE,HYPOTHESIS,
# CANDIDATE,OPEN,DEFERRED,REJECTED,STALE}; evidence ∈ {E0..E5}; source = a re-openable
# LOCATOR (file:line / test-id / experiment-run-id / bench-path / DOI#section), never a name;
# disposition ∈ {supported, needs-evidence, needs-experiment}. Only E3+ may be VERIFIED/FACT.
# Reversal is by SUPERSEDE (append new + point back), never by editing a decided item.
- id: D-001
  statement: "Use a matrix-free CG solver as the linear-system baseline."
  status: BASELINE
  evidence: E3
  source: "prototype-results.md#cg-vs-direct  (in-project prototype run 2026-07-30)"
  disposition: supported
  decided_by: "user @ 2026-07-30"
  proof_context: "commit a1b2c3d; seed=0; sample_A.npz; iters=41"
  alternatives: ["D-000 direct solver — REJECTED: memory O(N^2) for N>1e5"]
  last_verified: "2026-07-30"
  notes: "Discharge: adversarial check attempted (large-N memory) — held."

- id: H-002
  statement: "Incomplete-Cholesky preconditioning will cut iterations >2x."
  status: HYPOTHESIS
  evidence: E2
  source: "Benzi 2002 review, DOI:10.1006/jcph.2002.7176#sec3  (sibling-domain, NOT in-project)"
  disposition: needs-experiment
  decided_by: null
  last_verified: "2026-07-30"
  notes: "E2 cap: published, not in-project. Do NOT call verified until an in-project prototype (would raise to E3)."

- id: Q-003
  statement: "What accuracy does the downstream step actually require?"
  status: OPEN
  evidence: E0
  source: "goal-scope-note.md#open-decisions  (user-preference; UNVERIFIED)"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-07-30"
  notes: "Blocks tolerance selection; classified needs-user-preference."

- id: X-000
  statement: "(superseded) Use a direct LU solver as the baseline."
  status: STALE
  evidence: E3
  source: "early-notes.md#lu  (in-project, superseded)"
  disposition: supported
  superseded_by: D-001
  reason: "Replaced by matrix-free CG after the memory blow-up at N>1e5; kept for audit trail."
  last_verified: "2026-07-30"
```

## Change log

| date | id | change |
|---|---|---|
| <YYYY-MM-DD> | D-001 | created as BASELINE after CG prototype |
