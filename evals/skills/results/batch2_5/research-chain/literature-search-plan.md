---
generated_by_skill: research-question-and-literature-planner
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: ["Can Riemannian / manifold-optimization methods (retraction, vector transport, Riemannian gradient / CG) — developed for smooth matrix manifolds — be transferred to solve equality-constrained ('implicit-constraint') optimization problems in a general numerical solver, and under what assumptions (constraint qualification such as LICQ, smoothness of the constraint manifold) does that transfer hold?"]
artifact_type: literature-search-plan
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Scope + route for ONE cross-domain transfer question (matrix-manifold optimization machinery → general equality-constrained/implicit-constraint solver core); excludes all retrieval, reading, summary, and synthesis (delegated to lit-review)."
facts: "none (no retrieval performed; named seed anchors are labeled 'to confirm/expand — NOT asserted findings')"
hypotheses: "3 decision-tied questions (Q1 CQ→smooth-manifold theory; Q2 constructibility+cost of the core operations for a general/implicit manifold; Q3 backbone-vs-defer decision) — see 'Question(s) + the decision they inform'"
open_questions: "3 open questions + 1 prominent cross-domain transfer warning + the hinge-assumption conditionals (LICQ / regular value / constant rank + smoothness of h) retrieval must resolve — see 'Evidence / quality standard' and 'Expected evidence types'. Never 'none'."
evidence_level: "E2 target cap (cross-domain → analogy/indirect only; an in-domain matrix-manifold theorem cannot become a direct/project fact for a GENERAL implicit-constraint solver)"
next_handoff: lit-review
handoff_requirements: "lit-review needs: the seed query (below) + in/out scope + the inclusion/exclusion table + the stop criterion (5–8 source budget OR saturation). It executes retrieval; this plan does not."
status: search plan (scoping artifact; NO retrieval performed, NO papers read)
---

# Search Plan — Transfer of matrix-manifold optimization machinery to a general equality-constrained solver core

A **scoping artifact**, produced *before* retrieval. It contains **no retrieved papers and no summaries** — the
named retrieval skill (`lit-review`) executes it. All paper names below are **candidate anchors to
confirm/expand — NOT asserted findings**.

## Question(s) + the decision they inform

**Decision this feeds:** whether to base our solver's equality-constrained ("implicit-constraint") optimization
**core on a manifold-optimization backbone**, or **reject/defer** it in favor of standard NLP machinery.

Refined, answerable, decision-tied questions:

- **Q1 — Theory / hinge condition.** Under which constraint qualifications and smoothness assumptions on the
  constraint map `h` (LICQ / regular-value condition / constant-rank; `h ∈ C^k`) is the feasible set
  `{x : h(x)=0}` a smooth *embedded* submanifold on which the source machinery (retraction, vector transport,
  Riemannian gradient / CG) is well-defined? Where does that condition *fail* (rank-deficient Jacobian,
  non-smooth / algebraic constraints)?
- **Q2 — Constructibility & cost.** For a *general, implicitly-defined* constraint manifold (no closed-form
  geodesics/retractions, unlike Stiefel / Grassmann / SPD / fixed-rank), can the core operations be **constructed
  and computed at acceptable cost** (e.g. projection / feasibility-restoration retractions, Newton-on-constraint
  retractions, transport-by-projection) — and how does that compare with SQP / augmented-Lagrangian / interior-point
  baselines for the same equality-constrained problem?
- **Q3 — Backbone decision.** Given Q1–Q2, is a manifold-optimization backbone a **sound basis** for our general
  equality-constrained core, or is it dominated by / should defer to standard NLP methods — and for **which
  problem sub-classes** (structured orthogonality/low-rank vs. generic smooth `h`) does each win?

## Scope (in / out)

- **In:**
  - Riemannian optimization on **smooth matrix manifolds** — the *source* machinery: retraction, vector transport,
    Riemannian gradient / conjugate-gradient / trust-region.
  - **Optimization on manifolds defined by constraints** / equality-constrained NLP viewed through the manifold
    lens (regular value theorem; feasible-set-as-manifold; feasibility restoration as retraction).
  - **Constraint qualifications** (LICQ, constant-rank, MFCQ as contrast) and **smoothness** assumptions as the
    *transfer hinge*.
  - Method/theory papers, authoritative monographs/surveys, and toolbox/method papers (e.g. Manopt / Pymanopt /
    ROPTLIB) as **method-existence anchors**.
  - Time window: foundational (≈2008–) for the source machinery through **recent (last ~3–5 yr)** for the
    general/implicit-constraint transfer.
- **Out** (a scope of "everything" is a defect):
  - Application papers that merely **use** optimization on a fixed named manifold with no bearing on the
    *general-constraint* transfer.
  - Inequality-constrained / interior-point specifics **except** as a named comparison baseline.
  - Stochastic / deep-learning manifold optimization, unless it speaks to the general-constraint *construction*.
  - Non-smooth manifold optimization, except where it bears on the smoothness assumption.
  - Library benchmarking as an end in itself (implementation timing without method/theory content).

## Inclusion / exclusion criteria

| include if | exclude if |
|---|---|
| Establishes when `{h=0}` is a smooth (embedded) manifold under a **named CQ** (LICQ / regular value / constant rank). | Applies only a fixed **closed-form** manifold (pure Stiefel/Grassmann/SPD app) with no bearing on the general/implicit transfer. |
| **Constructs or analyzes** retraction / vector transport / Riemannian gradient/CG for a **general or implicitly-defined** constraint manifold. | No smoothness/CQ discussion **and** no solver-construction content (off the transfer hinge). |
| **Directly compares** manifold optimization vs SQP / augmented-Lagrangian / interior-point for equality-constrained problems. | Wrong domain (unconstrained-only; inequality-only interior point with no equality-manifold view). |
| Authoritative **text / survey** defining the source machinery or the regular-value ⇔ CQ bridge (method anchor). | Below quality floor (non-archival; no proof/derivation and no reproducible method). |

## Stop criteria (this run is deliberately small)

- **Source budget: 5–8 sources**, **OR** **saturation** — no new transfer mechanism or CQ/smoothness assumption
  appears across **2 consecutive** sources — **whichever comes first.**
- Budget must **cover the four faces** before stopping: (a) ≥1 authoritative *source-machinery* anchor;
  (b) ≥1 *regular-value / CQ → smooth-manifold* theory source; (c) ≥1 *general/implicit-constraint retraction
  construction* source; (d) ≥1 *manifold-optimization vs standard-NLP* comparison. If a face is uncovered at the
  budget ceiling, record it as an **open gap** rather than overspending.

## Evidence / quality standard (→ E0–E5)

- **Strong (for the *source* claims)** = theorem + proof establishing CQ ⇔ full-row-rank Jacobian ⇔ embedded
  submanifold, or a constructive retraction with cost/convergence analysis. High *internal* rigor.
- **Weak / indirect** = "it should carry over" assertions, single-manifold demonstrations, application analogies,
  toolbox capability claims with no general-constraint analysis.
- **⚠ CROSS-DOMAIN TRANSFER WARNING (prominent — this is the load-bearing caveat).** The machinery (retraction,
  vector transport, Riemannian gradient/CG) was developed for **smooth *matrix* manifolds** whose special
  structure gives **closed-form or cheap** geodesics/retractions and projections. Moving it to a **general
  equality-constrained solver**, where the feasible manifold is only **implicitly defined** and lacks those
  closed-form operations, is a **genuine leap**. Therefore evidence for the *transfer claim itself* is
  **analogy / indirect**: even a rigorous in-domain (Stiefel/Grassmann) theorem does **not** establish a
  **direct / project fact** for our general solver. **Evidence ceiling for the transfer conclusion = E2 (cap).**
  The whole transfer is **conditional** on the hinge assumption (**LICQ / regular value / constant rank +
  smoothness of `h`**); retrieval must surface **where that assumption fails** (rank-deficient/near-singular
  Jacobian, non-smooth or algebraic constraints, feasibility-restoration breakdown). This is the
  transfer-assumption input the downstream synthesizer's transfer lens will consume.

## Expected evidence types

- Authoritative **monographs / surveys** defining the source machinery — *to confirm/expand, NOT findings*.
- **Theorems + proofs**: regular value theorem; LICQ ⇔ full-row-rank Jacobian ⇔ embedded submanifold of dim `n−m`.
- **Method papers** constructing retraction / vector transport for constraint / implicit manifolds (projection,
  feasibility restoration, Newton-on-constraint).
- **Comparative method papers / numerical studies**: manifold optimization vs SQP / AL / interior-point on
  equality-constrained problems.
- **Toolbox / software papers** (Manopt / Pymanopt / ROPTLIB) as **method-existence anchors** — capabilities, not
  our-solver facts.

## Route (delegate retrieval — this skill stops here)

- **Chosen:** **`lit-review`** (default).
- **Why it — not the others:**
  - **`lit-review` (chosen):** the decision ("base the core on a manifold backbone, or reject/defer") is an
    **open, multi-paper *decision review*** needing scope → grounded retrieval → per-paper evidence ledger →
    strength-calibrated synthesis → independent audit. `lit-review` owns exactly that loop and fans out per-paper
    extraction, which is what a base/reject/defer choice over a small curated set requires. **Best fit.**
  - **`wos-research` (not routed):** best for **iterative WoS query optimization / relevance-driven query
    rewriting / "has this idea been implemented"** checks. Our need is decision-tied synthesis over a bounded,
    known-anchored set — not a WoS-Core relevance-coefficient iteration. Could optionally *pre-feed* candidate
    discovery, but is not the primary route.
  - **`deep-research` (not routed):** heavier **multi-source *web* fan-out + adversarial verification**; justified
    only for a broad web sweep. Overkill for a bounded **5–8 source** scholarly-method question rooted in known
    monographs + method papers.
  - **`paper-fetch-skill` (not routed as planner route):** for a **KNOWN single paper**. We hold *candidate
    anchors to confirm*, not one known target; once `lit-review` fixes specific seeds, `paper-fetch-skill` is the
    **downstream fetch primitive**, not this plan's route.
- **Seed query handed over:**
  `("Riemannian optimization" OR "manifold optimization" OR "optimization on manifolds") AND (retraction OR "vector transport" OR "Riemannian gradient" OR "Riemannian conjugate gradient") AND ("equality constraint" OR "constraint manifold" OR "implicitly defined manifold" OR "regular value" OR LICQ OR "constraint qualification" OR "feasibility restoration") AND (SQP OR "augmented Lagrangian" OR "interior point")`
- **Seed anchors — TO CONFIRM/EXPAND, *NOT* asserted findings** (labels only; unread, unverified):
  - Absil, Mahony & Sepulchre, *Optimization Algorithms on Matrix Manifolds* (2008) — source-machinery anchor *(to confirm)*.
  - Boumal, *An Introduction to Optimization on Smooth Manifolds* (2023) — source machinery + retraction/smoothness theory *(to confirm)*.
  - A standard NLP text for the CQ side (e.g. Nocedal & Wright, *Numerical Optimization*) + a smooth-manifolds text for the regular value theorem (e.g. Lee, *Introduction to Smooth Manifolds*) — the LICQ ⇔ embedded-submanifold bridge *(to confirm)*.
  - Method paper(s) on retraction / feasibility restoration for **implicitly-defined** constraint manifolds *(to confirm/expand)*.
  - Manopt / Pymanopt / ROPTLIB toolbox paper(s) — method-existence anchor *(to confirm)*.

`ROUTE retrieval=lit-review because=open base/reject/defer decision review over a bounded 5–8 source set needs scope→grounded evidence-ledger→calibrated audited synthesis, not WoS query-iteration, heavy web fan-out, or single-paper fetch`
