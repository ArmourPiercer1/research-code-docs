<!--
generated_by_skill: research-evidence-synthesizer
skill_version: 0.1.0
source_commit: 975e930
source_documents: [evals/skills/task-quality/fixtures/res/evidence-bundle-manifold-transfer.md (SYNTHETIC eval fixture — 4 fictional sources)]
status: evidence map (CANDIDATE-level; no project-verified fact asserted; nothing retrieved here)
last_verified: 2026-08-05T09:09Z
eval_artifact: research-evidence-synthesizer v0.1.0 SHADOW RUN (Batch-2 light round) — a fresh sub-agent injected with the SKILL.md + template, organizing the SYNTHETIC evidence bundle. Read-only; no retrieval; analogy capped at E2, LICQ assumption flagged E0, weak direct trial isolated at E1; no project-fact upgrade (D.8). Eval evidence, not a governance doc.
-->

# Evidence Map — which optimization scheme to adopt for our general nonlinear implicit-constraint solver

Design-decision-facing. Every source→claim link carries an **E-level + channel**; paper / same-domain /
cross-domain-analogy evidence is **never** presented as a project-verified fact (constraint D.8). This organizes
the already-retrieved (synthetic) evidence bundle only — it does **not** retrieve, and it does **not** assign the
final DECIDED status (that is `uncertainty-and-decision-manager`).

> **Decision informed:** which optimization scheme to adopt for our *general nonlinear implicit-constraint solver*.
> **Bundle scope:** the four sources argue essentially one question — *does matrix-manifold optimization transfer
> to our problem?* Three of four sources are **cross-domain** to us; the single **same-domain** source is a
> **limiting** one; the single **direct** in-project source is **weak (E1)**.

### E-level scale used (working calibration)
Exact anchoring lives in `system-architecture.md §7`, **not re-read here** (constraint D.8). Levels are applied
conservatively, calibrated to the template (cross-domain-analogy caps at **E2**; project-inference / weak-direct
at **E1**) and to the bundle note that [S4] is "direct but E1 at most":

- **E0** — assumed / asserted with no evidence (or contradicted).
- **E1** — weak: a single unreplicated in-project trial (direct-but-weak), or a project-inference/extrapolation.
- **E2** — cross-domain analogy: theory/empirics from a different domain or problem family (**cap for analogy**).
- **E3** — same-domain-indirect: established survey/theory in *our* domain, but not measured on our solver.
- **E4** — direct in-project measurement, controlled/replicated.
- **E5** — direct in-project, rigorously verified / proven baseline.

## Source inventory (read-only; nothing searched-for here)
| handle | what it claims | setting/domain | channel to our problem |
|---|---|---|---|
| **[S1]** Rivest & Kan 2019 | RGD converges **linearly** to a local min **when** the feasible set is a smooth embedded manifold **and** the objective is geodesically L-smooth (convergence *proof*) | smooth matrix manifolds (Stiefel, Grassmann); theoretical | **cross-domain-analogy** |
| **[S2]** Okonkwo et al. 2021 | RGD needs **~30% fewer iterations** than projected gradient on their suite (empirical benchmark) | low-rank matrix completion (still matrix-manifold family) | **cross-domain-analogy** |
| **[S3]** Vasquez 2020 | manifold-assuming methods **break down when LICQ fails**; many *general* implicit-constraint sets violate LICQ at kinks/cusps (survey) | constraint qualifications in nonlinear programming (**our domain**) | **same-domain-indirect (LIMITING)** |
| **[S4]** Internal note 2026-07 | a manifold-style preconditioner on `case-7` dropped iterations **~20%** (single trial, no seed/tolerance, unrepeated) | our project / our solver | **direct (weak)** |

## Claim–evidence matrix
Channels kept separate: a cross-domain analogy is never listed in the same cell as the direct measurement. The
sole direct trial is isolated as **C4** so it cannot be laundered into the transfer rows.

| # | candidate claim (for *our* solver) | supports | contradicts / limits | E-level | channel |
|---|---|---|---|---|---|
| **C1** | Manifold optimization (RGD / manifold-style preconditioner) **transfers / is applicable** to our general nonlinear implicit-constraint solver | [S1], [S2] *(analogy)* | **[S3]** | **E2 (cap)** — and *undercut* by [S3]; effective confidence **< E2** until A1/A3 characterized in-project | cross-domain-analogy |
| **C2** | RGD **converges linearly** (fast local convergence) on our problem | [S1] | — *(its enabling assumption is questioned by [S3])* | **E2 (cap)** | cross-domain-analogy |
| **C3** | RGD needs **~30% fewer iterations** than projected gradient on our problem | [S2] | — | **E2 (cap)** | cross-domain-analogy |
| **C4** | A manifold-style **preconditioner reduces iterations** on our problem (~20% on `case-7`) | [S4] | — *(self-limited: n=1, no seed/tolerance, unrepeated)* | **E1** | **direct (weak)** |
| **C5** | *Enabling assumption:* our feasible set **is a smooth manifold where LICQ holds** | — *(none; assumed)* | **[S3]** | **E0** (assumed **and** contradicted) | project-inference (unsupported); contradicted by same-domain [S3] |

*Reading:* the favorable claims C1–C3 rest **only on cross-domain analogy** (E2 cap); the only **direct** signal
(C4) is **E1**; and the only **same-domain** source (C5←[S3]) argues **against** the enabling assumption.

## Method-transfer cards

### Card: Manifold optimization — RGD + manifold-style preconditioner (matrix-manifold origin → our general nonlinear implicit-constraint solver)
- **Origin setting:** smooth matrix manifolds — Stiefel/Grassmann [S1]; low-rank matrix completion [S2]. The
  feasible set is a smooth embedded manifold **by construction**.
- **Our setting:** a general nonlinear implicit-constraint solver — feasible set defined implicitly by general
  nonlinear constraints; may be **non-smooth (kinks/cusps)** and may **violate LICQ** at active points [S3].
- **Assumptions the transfer relies on:**
  - **A1 (smooth manifold):** the feasible set is a smooth embedded manifold.
  - **A2 (geodesic L-smoothness):** the objective is geodesically L-smooth.
  - **A3 (constraint qualification / LICQ):** active constraint gradients stay linearly independent, so the
    "manifold" picture holds where the solver operates.
  - **A4 (benchmark transfer):** the ~30% iteration advantage over projected gradient [S2] carries to our
    problem class.
- **Evidenced vs assumed:**
  - **A1** — evidenced **only** in the matrix-manifold domain [S1]; for our general nonlinear problem it is
    **ASSUMED**, and [S3] gives same-domain evidence it **FAILS in general** (kinks/cusps). → gap **G1**.
  - **A2** — evidenced in the matrix-manifold domain [S1]; **ASSUMED** for our objective/geometry.
  - **A3** — **NOT** evidenced for us; [S3] is same-domain-indirect evidence **AGAINST** it for general implicit
    constraints. → the critical gap **G1**.
  - **A4** — evidenced only by cross-domain benchmark [S2]; **ASSUMED** for us. One weak direct trial [S4]
    (**E1**; n=1, no seed/tolerance, unrepeated) is *consistent* but does **not** confirm. → gaps **G2/G3**.
- **E-level cap:** **E2.** The transfer rests on **cross-domain-analogy** ([S1],[S2]); by the weakest-assumption
  rule the honest cap is E2, and because A1/A3 (the enabling assumption) are **actively contradicted** by
  same-domain [S3] for the general case, real confidence sits **below a clean E2** until characterized in-project.
  The only direct evidence [S4] reaches **E1**. **This is NOT a direct / project-verified fact.**

*(No second adoption card: the bundle "considers" only manifold optimization. **Projected gradient** appears
merely as the matrix-manifold baseline in [S2]; there is no evidence about it — or any other scheme — for our
problem. Treated as coverage gap **G5**, not a card.)*

## Unresolved gaps (+ what would close each)
| # | gap | what would close it |
|---|---|---|
| **G1** | **Enabling assumption unverified & contradicted.** Is our feasible set a smooth manifold / does LICQ hold? [S3] says general implicit constraints violate LICQ at kinks/cusps; we have no in-project characterization (C5 = E0). | A **direct in-project characterization** of our feasible geometry (do our constraints produce kinks/cusps? is LICQ satisfied at active points?), **or** a same-domain source specific to our constraint class. |
| **G2** | **No replicated direct comparison.** [S4] is n=1, no seed/tolerance recorded, unrepeated, one case (`case-7`). | A **controlled in-project benchmark**: multiple representative cases, fixed seeds & tolerances, repeated runs, manifold-preconditioner/RGD vs the incumbent scheme. |
| **G3** | **Favorable results untested for us.** Linear convergence [S1] and ~30% fewer iterations [S2] are matrix-manifold-only. | **In-project experiments** on representative instances, **or** a same-domain (general NLP) result establishing rate/iteration behavior for our constraint class. |
| **G4** | **Behavior at non-smooth points unknown.** [S3] predicts breakdown where the manifold assumption locally fails; no evidence on robustness/fallback there. | **In-project stress tests** at/near kinks/cusps; **or** a method variant that tolerates LICQ failure (regularization / CQ-free scheme). |
| **G5** | **Alternatives uncharacterized for our problem.** The bundle argues only about manifold optimization; no direct evidence on projected gradient, augmented Lagrangian, SQP, etc., on our solver. | Route to `research-question-and-literature-planner` to **scope retrieval** on alternatives, plus in-project trials. |

## Coverage note
- **Sources used:** [S1],[S2] (cross-domain-analogy), [S3] (same-domain-indirect, **limiting**), [S4] (direct,
  **E1**). Four sources; all **synthetic** per the fixture; **none is a project-verified fact**.
- **Channel distribution:** 2× cross-domain-analogy (both *favorable*), 1× same-domain-indirect (the *only*
  in-domain source — and it is **LIMITING**), 1× direct (**weak, E1**). **Zero** same-domain-direct or
  replicated-direct evidence.
- **Evidenced vs assumed:** the favorable claims (linear convergence, ~30% iteration savings) are evidenced
  **only by analogy**; the enabling assumption (smooth manifold / LICQ) is **assumed and contradicted** by [S3];
  the sole direct signal is a **single unreplicated trial**. Evidentiary center of gravity = *analogy + one weak
  trial, against one same-domain caution.*
- **Honest reading for the decision:** adopting manifold optimization as the scheme would currently rest on
  **cross-domain analogy (E2 cap)** plus an **E1** in-project hint, while the **only same-domain evidence
  cautions against** the enabling assumption. Nothing here is upgraded to a project fact.
- **Discipline:** nothing retrieved or searched here; the four channels are kept separate; **no DECIDED status
  assigned**. Candidate claims C1–C5 with their E-levels/channels are routed to
  `uncertainty-and-decision-manager` (it assigns DECIDED/CANDIDATE/OPEN + records `proof_context`); gaps **G1–G5**
  route to `research-question-and-literature-planner` (scope follow-up retrieval) or to in-project experiments.
