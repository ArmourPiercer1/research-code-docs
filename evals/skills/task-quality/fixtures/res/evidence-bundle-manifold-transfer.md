<!--
generated_by_skill: (manual — SYNTHETIC eval fixture for research-evidence-synthesizer)
skill_version: n/a
source_commit: n/a (fixture)
source_documents: [n/a — SYNTHETIC; all four sources below are FICTIONAL, authored only for eval]
status: SYNTHETIC eval fixture — every claim is HYPOTHESIS-level and none is VERIFIED; do NOT cite as real.
last_verified: 2026-08-05
-->

# Retrieved evidence bundle (SYNTHETIC) — "do manifold-optimization methods transfer to our implicit-constraint solver?"

> ⚠️ **SYNTHETIC FIXTURE.** Every source below is invented for eval purposes. No claim here is real, and none
> is a project-verified fact. This simulates the *output of a retrieval step* (papers already fetched + notes),
> which `research-evidence-synthesizer` must ORGANIZE (it must not search for more, and must not upgrade any of
> this into a project fact). The design decision it informs: *which optimization scheme to adopt for our
> general nonlinear implicit-constraint solver.*

## [S1] Rivest & Kan, 2019 — "Riemannian gradient descent on smooth matrix manifolds" (method paper)
- **Setting:** optimization over smooth *matrix* manifolds (Stiefel, Grassmann).
- **Claim:** Riemannian gradient descent (RGD) converges linearly to a local minimum **when the feasible set
  is a smooth embedded manifold and the objective is geodesically L-smooth**.
- **Evidence type:** a convergence proof (theoretical), on matrix manifolds — NOT on general nonlinear
  implicit constraints.

## [S2] Okonkwo et al., 2021 — "Empirical comparison of manifold optimizers on low-rank problems" (benchmark)
- **Setting:** low-rank matrix completion (adjacent, still matrix-manifold).
- **Claim:** RGD needs ~30% fewer iterations than projected gradient on their benchmark suite.
- **Evidence type:** empirical benchmark; same broad family, different problem than ours.

## [S3] Vasquez, 2020 — "A survey of constraint qualifications in nonlinear programming" (survey)
- **Claim:** methods that assume the feasible set is a smooth manifold **break down when the constraint
  qualification (LICQ) fails** — e.g. at points where active constraint gradients are linearly dependent;
  many *general* implicit-constraint sets violate LICQ at kinks/cusps.
- **Evidence type:** survey; directly relevant *limiting* evidence — it says the manifold assumption is not
  free for general nonlinear constraints.

## [S4] Internal note (our project), 2026-07 — sprint scratchpad
- **Claim:** "we swapped in a manifold-style preconditioner on the `case-7` test and iterations dropped ~20%."
- **Evidence type:** a single in-project trial on one test case; no seed/tolerance recorded; not repeated.
