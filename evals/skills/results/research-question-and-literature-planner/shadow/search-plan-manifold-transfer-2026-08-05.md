<!--
generated_by_skill: research-question-and-literature-planner
skill_version: 0.1.0
source_commit: 975e930
source_documents: [the open research question]
status: search plan (scoping artifact; NO retrieval performed)
last_verified: 2026-08-05T09:09Z
eval_artifact: research-question-and-literature-planner v0.1.0 SHADOW RUN (Batch-2 light round) — a fresh sub-agent injected with the SKILL.md + template, scoping a cross-domain transfer question. NO retrieval/synthesis performed; seed anchors are labeled "to confirm, not asserted findings". Eval evidence, not a governance doc.
-->

# Search Plan — Transfer of matrix-manifold optimization methods to a general nonlinear implicit-constraint solver

A **scoping artifact**, produced *before* retrieval. It contains no retrieved papers and no
summaries — the named retrieval skill executes it. This is explicitly a **cross-domain transfer**
question (method domain A = *matrix manifolds* → problem B = *general nonlinear implicit-constraint
solver*); the transfer warning below governs how its evidence must be read.

## Question(s) + the decision they inform

**Decision it informs:** which optimization scheme to adopt for our general nonlinear
implicit-constraint solver (feasible set defined by `h(x) = 0` for general smooth nonlinear `h`).
Candidate scheme families the search must be able to discriminate between:
(a) **Riemannian / retraction-based** optimization generalized from matrix manifolds to the
constraint manifold; (b) **classical equality-constrained NLP** (SQP, reduced/projected-gradient,
feasible-direction); (c) **augmented-Lagrangian / hybrid** approaches (including Riemannian-ALM).

Refined, answerable questions (each tied to that decision):

- **Q1 — Component transferability.** Which components of the matrix-manifold toolkit —
  retraction, vector transport / parallel transport, Riemannian gradient & Hessian (Weingarten /
  second fundamental form), Riemannian trust-region (RTR), Riemannian CG, Riemannian
  (S)GD — have a *demonstrated or provable* generalization to feasible sets defined by general
  nonlinear equality constraints, and which are **specific to the closed-form algebraic structure**
  of matrix manifolds (Stiefel, Grassmann, SPD, fixed-rank, oblique)?
- **Q2 — Assumptions for transfer.** *Under what assumptions* does each transfer hold? Specifically:
  (i) regularity / constraint qualification (`h` a submersion, Jacobian full-rank / LICQ → embedded
  smooth submanifold); (ii) metric choice (induced/embedded vs. manifold-specific);
  (iii) availability and cost of a **retraction** when no closed-form geodesic exists (projection-like
  retractions, one-step feasibility restoration, ODE integration); (iv) cost of tangent-space
  projection (closed-form for matrix manifolds vs. solving Jacobian systems in general);
  (v) completeness / curvature bounds required by the convergence guarantees.
- **Q3 — Decision-facing comparison.** Given Q1–Q2, for a *general* nonlinear `h(x)=0`, which scheme
  family is the better fit, and **what does adopting it require us to implement** (a retraction, a
  tangent-space projector, a Riemannian Hessian, a feasibility-restoration step)? Where does the
  retraction-based view collapse into, or become dominated by, a classical SQP / augmented-Lagrangian
  step?

*(If, on review, the team concludes this is a design decision resolvable without literature — e.g.
we already know we want plain SQP — route back to the elicitor rather than run the search.)*

## Scope (in / out)

- **In:**
  - Riemannian / manifold optimization **methods** for matrix manifolds (Stiefel, Grassmann, SPD,
    fixed-rank, oblique) as the **source** domain — method & theory content only.
  - **Generalization** results to embedded submanifolds / feasible sets defined by general smooth
    `h(x)=0` (the bridge literature): retraction constructions for general constraints
    (projection-like, restoration-based, ODE/geodesic), constraint qualification & regularity,
    Riemannian methods on abstract/general manifolds.
  - **Target-family** references for the comparison in Q3: equality-constrained NLP — SQP,
    reduced/projected-gradient, augmented Lagrangian / Riemannian-ALM — *only* insofar as they
    connect to the manifold/constraint-surface view.
  - Foundational monographs & surveys; method/theory papers; convergence proofs; optimization
    **toolboxes** as evidence of *what is implemented for which manifolds* (e.g. Manopt / Pymanopt /
    Manifolds.jl).
  - Time window: foundational (≈2008 matrix-manifold monograph) → present, emphasis on
    generalization/transfer results.
- **Out:** (a scope of "everything" is a defect)
  - Application-only matrix-manifold papers with no transferable method content (a single task that
    merely *uses* a Stiefel constraint).
  - Inequality-constrained / interior-point NLP as a primary topic (our constraints are equality
    `h(x)=0`) — admitted only when a source directly bears on the manifold transfer.
  - DL/stochastic-specific Riemannian optimizers unless the method itself generalizes.
  - Convex optimization over simple fixed sets (simplex, ball) not framed as a manifold.
  - Non-smooth manifold optimization, except where it changes a transfer assumption.
  - PDE-/data-fitting problems where "constraint" means something other than `h(x)=0` feasibility.

## Inclusion / exclusion criteria

| include if | exclude if |
|---|---|
| Presents a **method** (retraction, transport, Riemannian grad/Hess, RTR/RCG, Riemannian-ALM) with its geometric construction | Uses a matrix manifold only as an application detail, no transferable method |
| States or proves **transfer to general `h(x)=0` / embedded submanifolds**, or gives the general-manifold form with conditions | Restricted to one closed-form manifold with no path to generalization |
| Makes **assumptions explicit** (constraint qualification / submersion, metric, retraction existence, curvature) | Asserts a method "works" with the constraint-qualification / regularity conditions left unstated |
| Provides a **convergence result, proof, or reproducible benchmark**, or is a canonical monograph/survey | Opinion / analogy only, or a claim with no derivation, proof, or measured evidence |
| Bridges Riemannian view ↔ classical SQP / augmented-Lagrangian (needed for Q3) | Pure inequality/interior-point NLP with no manifold bearing |
| Recency: foundational canon **or** post-canon generalization work | Superseded restatement adding no new transfer mechanism or assumption class |

## Stop criteria (pick one, make it explicit)

- **Primary — method/assumption saturation.** Stop when **2 consecutive included sources introduce
  no new transfer mechanism** (a distinct retraction construction, metric, tangent-space-projection
  strategy, or feasibility/restoration scheme) **and no new assumption class** (constraint
  qualification, curvature/completeness, cost condition) beyond those already logged for Q1/Q2.
- **Backstop guard (bounds effort, not the primary rule):** hard cap at ~25 screened sources or once
  the top venues/monographs for Riemannian optimization + constrained NLP are covered — whichever
  comes first. If the cap is hit before saturation, record the gap rather than over-claim closure.

## Evidence / quality standard (→ E0–E5)

Mapped to the system's E0–E5 evidence ladder (E5 strongest … E0 weakest), interpreted for *this*
transfer question:

- **Strongest (E5 / E4)** — a formal **theorem + proof** that a specific matrix-manifold method
  generalizes to general `h(x)=0` under explicitly stated assumptions (CQ/submersion, retraction
  existence, curvature/completeness); or a convergence guarantee stated for general embedded
  submanifolds; or a reproducible benchmark on a genuinely general (non-closed-form) constraint.
- **Established (E3)** — canonical **monograph / well-cited survey** presenting the general-manifold
  version with conditions (i.e. the field's settled treatment), directly applicable to our setting.
- **Indirect / weak (E2 / E1)** — empirical demonstration on *a* constraint case without a proof of
  general transfer; existence of a toolbox implementation; a result proven only for one closed-form
  matrix manifold that we must *extrapolate*.
- **Weakest (E1 / E0)** — **analogy-only** transfer ("Stiefel works, so it should work for general
  `h`"), or any claim whose constraint-qualification / regularity assumptions are unstated.

**Standard for the decision:** a scheme family should be adopted on the back of **E4–E5** support for
the *specific* transfer we rely on (retraction + projection + Hessian under our CQ), or **E3** canon
*with* an explicit assumption check. Anything resting on **E0–E2** must be logged as an
assumption/risk for the decision-manager, not asserted as fact.

- **Transfer warning (cross-domain — raise the HF-12D lens):** the source domain (matrix manifolds)
  supplies rich **closed-form** geometry (geodesics, retractions, transports) that our **general**
  `h(x)=0` setting generally does **not** have. Expect much of the "does it transfer?" evidence to be
  either (a) **general-manifold theory we must map back** to our solver, or (b) **analogy**. Direct
  evidence tested on an explicitly *general nonlinear implicit-constraint solver* will be **sparse**;
  every transferred claim must travel with its **assumption set** (CQ, retraction cost, curvature),
  and the strength of the transfer is bounded by whether those assumptions hold for our `h`. This is
  the synthesizer's transfer-assumption input — do not let an analogy be logged as a finding.

## Expected evidence types

- **Monographs / textbooks** — foundational matrix-manifold optimization; general smooth-manifold
  optimization; classical constrained NLP (for the Q3 comparison).
- **Method / theory papers** — retraction & vector-transport constructions, RTR/RCG convergence,
  Riemannian Hessian via the Weingarten map.
- **Bridge papers** — projection-like / restoration-based retractions for general constraints,
  Riemannian augmented-Lagrangian & constrained-manifold methods, DAE/constraint-surface views.
- **Surveys** of Riemannian optimization (coverage + settled conditions).
- **Software / toolbox docs** — evidence of *which* manifolds and retractions are actually
  implemented (implementation cost signal for the decision).
- **Proofs / convergence theorems** (strongest) and **benchmarks** on general constraints.
- Weighted per the **transfer warning**: analogy-grade material is admissible only as hypothesis, not
  as an E3+ finding.

## Route (delegate retrieval — this skill stops here)

- **Chosen:** `lit-review`
- **Why it (not the others):** this is an open, **decision-facing survey** of a well-bounded academic
  field (Riemannian/manifold optimization + equality-constrained NLP) that must end in a
  **strength-calibrated, audited synthesis comparing scheme families** — exactly `lit-review`'s
  end-to-end remit (plan → grounded retrieval → snowball → evidence ledger → argument ledger →
  audited review). Not `deep-research`: that is a heavier **web** multi-source fan-out with
  adversarial verification, mis-fit for peer-reviewed mathematical-optimization literature seeded by
  known monographs. Not `wos-research`: its value is iterative WoS query-quality feedback / novelty
  ("has this been done") — useful as a *secondary* completeness pass, but our need is synthesis of a
  known field into a decision, not query iteration. Not `paper-fetch-skill` as the top-level route:
  it fetches **known** seeds and will be invoked *inside* `lit-review` for the entry points below —
  it does not scope an open survey.
- **Seed query / seeds handed over** (entry points for the retrieval skill to verify — **not**
  asserted findings):
  - Seed queries: `retraction general equality constraints manifold optimization`;
    `Riemannian optimization embedded submanifold constraint qualification`;
    `projection-like retractions nonlinear constraints`;
    `Riemannian augmented Lagrangian optimization with constraints`;
    `manifold optimization vs SQP equality constrained comparison`;
    `feasibility restoration retraction general nonlinear constraint`.
  - Candidate seed anchors to confirm/expand: the foundational matrix-manifold optimization
    monograph (Absil–Mahony–Sepulchre, 2008); the general smooth-manifold optimization monograph
    (Boumal, 2023); projection-like-retractions work (Absil–Malick); Riemannian-constrained /
    Riemannian-ALM method papers; a standard equality-constrained NLP reference (Nocedal–Wright) for
    the Q3 target family. Hand over with **scope + inclusion/exclusion + the saturation stop
    criterion** above.

`ROUTE retrieval=lit-review because=open decision-facing survey of a bounded academic method field (matrix-manifold ↔ general-constraint optimization) needing a strength-calibrated, audited synthesis comparing scheme families — not web fan-out, WoS query-iteration, or single-paper fetch`
