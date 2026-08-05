<!--
generated_by_skill: lit-review (STAND-IN — see provenance note; real metadata retrieval, not the installed skill)
skill_version: n/a (retrieval executed via OpenAlex + Semantic Scholar public metadata APIs)
source_commit: 7919bc4
source_documents:
  - evals/skills/results/batch2_5/research-chain/literature-search-plan.md (the RQLP plan this executes)
  - "OpenAlex works API (via scansci-pdf MCP): 3 queries, 2026-08-05"
document_lifecycle: IN_REVIEW
status: CANDIDATE retrieval output (real sources; metadata + abstracts only; NO synthesis, NO E-levels, NO channels — that is the synthesizer's job)
last_verified: 2026-08-05
-->

# Retrieval Results — manifold-optimization transfer to implicit-constraint solvers

> **Provenance / honesty note (read first).** This artifact is the **`lit-review` step of the Batch-2.5
> research chain**, produced as a **stand-in** for the *installed* `lit-review` skill: the retrieval is
> **real** (real papers, real DOIs, real citation counts, real abstracts, pulled 2026-08-05 from the
> **OpenAlex** works API via the `scansci-pdf` MCP, with a Semantic-Scholar attempt that was rate-limited).
> The installed `lit-review` skill was **not auto-invoked** (this system does not auto-trigger installed
> skills, and re-implementing a retriever is forbidden) — so the *wrapper* is a stand-in, but the *evidence
> is not synthetic*. This satisfies directive §3.2 ("lit-review must actually produce retrieval results").
>
> **Boundary kept:** this is **retrieval only** — sources + their own stated scope. It assigns **no**
> evidence channel, **no** E-level, and makes **no** transfer judgement. That is `research-evidence-synthesizer`'s
> job downstream. (Testing exactly this hand-off is the point of Track B.)

## Scope of this retrieval (executed per the search plan)

- **Round:** 1 (bounded). **Budget:** 5–8 sources. **Returned & kept:** 5 on-topic sources.
- **Queries run (OpenAlex):** (1) "Riemannian optimization on matrix manifolds retraction vector transport";
  (2) "augmented Lagrangian method Riemannian manifolds nonlinear constraints"; (3) "Absil Mahony Sepulchre
  optimization algorithms on matrix manifolds"; plus relevance probes for constraint-qualification-on-manifold.
- **Coverage of the plan's four faces** (retrieval-coverage fact, not a transfer verdict):
  - Face A — *source machinery anchor* (retraction / vector transport on matrix manifolds): **covered** (S1, S2).
  - Face B — *convergence / optimality theory on manifolds*: **covered** (S3, S5).
  - Face C — *constrained optimization ON manifolds vs standard NLP*: **partially covered** (S5).
  - Face D — *general/implicit constraint manifold: when is `{h(x)=0}` a smooth submanifold, and how is a
    retraction **constructed** for it (no closed form)*: **NOT covered** by any kept source — every source
    assumes an already-given, mostly **structured** matrix manifold. Recorded as an open retrieval gap.

## Sources (real metadata; each source's OWN stated scope only)

### [S1] Absil, Mahony, Sepulchre (2008) — *Optimization Algorithms on Matrix Manifolds*
- DOI: `10.1515/9781400830244` · book · cited-by ≈ 1749 · OA: no.
- Stated scope: the foundational text defining retraction-based, vector-transport optimization on **matrix**
  manifolds (Stiefel, Grassmann, fixed-rank, SPD). Establishes the machinery the transfer question is about.

### [S2] Vandereycken (2013) — *Low-Rank Matrix Completion by Riemannian Optimization*
- DOI: `10.1137/110845768` · SIAM J. Optim. · cited-by ≈ 523 · OA: yes.
- Abstract (excerpt): "…minimizes the least-square distance … over the Riemannian manifold of fixed-rank
  matrices … an adaptation of classical nonlinear conjugate gradients, developed within the framework of
  retraction-based optimization on manifolds…"
- Stated scope: a concrete instance — retraction-based CG on **one specific structured matrix manifold**
  (fixed rank). Closed-form/cheap retraction is available *because* of that structure.

### [S3] Boumal, Absil, Cartis (2018) — *Global rates of convergence for nonconvex optimization on manifolds*
- DOI: `10.1093/imanum/drx080` · IMA J. Numer. Anal. · cited-by ≈ 288 · OA: yes.
- Abstract (excerpt): "…Riemannian gradient descent and Riemannian trust regions … under Lipschitz-type
  assumptions on the pullbacks of f to the tangent spaces … produce points with Riemannian gradient smaller
  than ε in O(1/ε²) iterations…"
- Stated scope: convergence-rate theory for Riemannian first-/second-order methods, **given** a manifold and
  Lipschitz-type assumptions on pullbacks.

### [S4] Hu, Liu, Wen, Yuan (2020) — *A Brief Introduction to Manifold Optimization*
- DOI: `10.1007/s40305-020-00295-9` · J. Oper. Res. Soc. China · cited-by ≈ 197 · OA: yes.
- Abstract (excerpt): "…By utilizing the geometry of manifold, a large class of constrained optimization
  problems can be viewed as unconstrained optimization problems on manifold. From this perspective, intrinsic
  structures, optimality conditions and numerical algorithms…"
- Stated scope: a survey; explicitly frames "constrained → unconstrained-on-manifold." States the viewpoint;
  its worked structures are again the standard matrix manifolds.

### [S5] Yamakawa, Sato (2022) — *Sequential optimality conditions for nonlinear optimization on Riemannian manifolds and a globally convergent augmented Lagrangian method*
- DOI: `10.1007/s10589-021-00336-w` · Comput. Optim. Appl. · cited-by ≈ 12 · OA: yes.
- Stated scope: **additional** equality/inequality constraints *on top of* a Riemannian manifold, handled by
  an augmented-Lagrangian method with sequential optimality conditions + a global convergence result. Closest
  source to "constrained optimization on manifolds"; still assumes the base manifold is given.

## Retrieval coverage note (for the synthesizer)

- Strong, real evidence exists for the **machinery** (S1, S5) and its **convergence behaviour** (S3), and for
  the **"constrained-as-unconstrained-on-manifold"** viewpoint (S4), all in the **matrix-manifold / given-manifold**
  setting.
- **No kept source** addresses the **general implicit constraint** case our decision hinges on: (i) conditions
  under which `{x : h(x)=0}` for an arbitrary smooth `h` is a well-behaved submanifold (regular value / LICQ /
  constant-rank), or (ii) how to **construct a computable retraction** there without a closed form. These are
  left as **open retrieval gaps** for the synthesizer to flag (and possibly route back to RQLP), NOT resolved
  here.
- Nothing here is a project fact or a decided transfer; the synthesizer assigns channels + E-levels.
