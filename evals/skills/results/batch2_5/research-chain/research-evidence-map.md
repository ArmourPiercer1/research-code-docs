---
generated_by_skill: research-evidence-synthesizer
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/lit-review-results.md, evals/skills/results/batch2_5/research-chain/literature-search-plan.md]
artifact_type: research-evidence-map
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Organizes the already-retrieved 5-source bundle (S1–S5) into a claim–evidence matrix + one method-transfer card for ONE decision — base the GENERAL equality-constrained/implicit-constraint solver core on a manifold-optimization backbone (retraction / vector transport / Riemannian CG), or reject/defer. Excludes: all retrieval/search (none performed), any fact upgrade (D.8), and the decision itself (routed to the register)."
facts: "none (paper/analogy evidence is never a project-verified fact — D.8; all 5 sources are cross-domain-analogy, capped ≤ E2; no in-project trial has been run, so nothing sits above E2)"
hypotheses: "7 claim rows — see 'Claim–evidence matrix' (E-level + channel each): CL-1..CL-5 are cross-domain-analogy at the E2 cap; CL-6 and CL-7 are the two uncovered enabling assumptions at E0 (assumed, unevidenced)"
open_questions: "4 gaps — see 'Unresolved gaps': G1,G2 route BACK to research-question-and-literature-planner (the uncovered Face D); G3 → RQLP-or-experiment (Face C comparison, only partial); G4 → in-project experiment (the only path off the E2 analogy cap)"
evidence_level: "E2 (cap — cross-domain-analogy; all 5 sources are matrix-manifold / given-manifold). Two load-bearing transfer assumptions (A1, A2) are E0 (unevidenced). No direct (in-project) or same-domain-indirect evidence exists → no claim exceeds E2, and the general/implicit-case transfer conclusion is unsupported beyond analogy."
next_handoff: "uncertainty-and-decision-manager (register the candidate claims); research-question-and-literature-planner (gaps G1–G3 → re-scope retrieval)"
handoff_requirements: "The register needs, per candidate claim: the E-level + channel (here EVERY support link is cross-domain-analogy at E2 — the `direct` and `same-domain-indirect` channels are empty); the method-transfer card's assumptions with their evidenced-vs-assumed split (A1=E0, A2=E0, A3=E2-analogy) and E-cap; and the 4 unresolved gaps with their route (RQLP vs in-project experiment). RES assigns NO DECIDED/BASELINE status — that is the register's."
status: evidence map (CANDIDATE-level; no project-verified fact asserted; nothing retrieved here)
---

# Evidence Map — Manifold-optimization backbone for a general equality-constrained ("implicit-constraint") solver core

Design-decision-facing. Every source→claim link carries an **E-level + channel**; paper/analogy evidence is
**never** presented as a project-verified fact (constraint **D.8**). This organizes the retrieved bundle; it does
**not** retrieve, and it does **not** assign the final DECIDED status (that is `uncertainty-and-decision-manager`).

**Decision this informs (verbatim from the RQLP plan):** whether to base our solver's equality-constrained
("implicit-constraint") optimization **core on a manifold-optimization backbone** (retraction / vector transport /
Riemannian gradient / CG), or **reject/defer** it in favor of standard NLP machinery (SQP / augmented-Lagrangian /
interior-point).

### E-level legend (as used in this map — per the frozen schema's cap rule, not a re-derivation of the canonical ladder)
- **E0** — assumed / unevidenced: no source in this bundle bears on it (an unevidenced transfer assumption).
- **E1** — weak: a single indirect signal, or a project-inference not measured.
- **E2** — the ceiling for a **cross-domain-analogy** (or same-domain-indirect) transfer claim. **This is the cap of the whole map.**
- **E3–E5** — reserved for **`direct`** (measured-in-this-project) evidence. **None present here** — the `direct` channel is empty.

### The four channels (kept strictly separate — collapsing them is an INTERFACE_DEFECT)
| channel | meaning (to *our* general implicit-constraint solver) | populated here? |
|---|---|---|
| `direct` | measured in THIS project | **EMPTY** — no in-project trial has been run |
| `same-domain-indirect` | evidence about a general implicit/equality-constraint solver, indirect | **EMPTY** — no source addresses the general/implicit case (this emptiness *is* the Face-D gap) |
| `cross-domain-analogy` | matrix-manifold / given-manifold results, transferred by analogy | **S1, S2, S3, S4, S5 (all 5)** — hence the E2 cap |
| `project-inference` | our own assumption/reasoning, no source | **A1, A2** (the two uncovered enabling assumptions) → E0 |

## Source inventory (read-only; nothing searched-for here)

| handle | what it claims (its OWN stated scope) | setting / domain | channel to our problem |
|---|---|---|---|
| [S1] Absil, Mahony, Sepulchre 2008 — *Optimization Algorithms on Matrix Manifolds* (book; cited ≈1749; OA no; DOI 10.1515/9781400830244) | Foundational machinery: retraction-based, vector-transport optimization on **structured matrix** manifolds (Stiefel, Grassmann, fixed-rank, SPD). | matrix manifolds (given, structured) | cross-domain-analogy |
| [S2] Vandereycken 2013 — *Low-Rank Matrix Completion by Riemannian Optimization* (SIAM J. Optim.; cited ≈523; OA yes; DOI 10.1137/110845768) | Retraction-based CG on **one specific structured** manifold (fixed rank); **closed-form/cheap retraction is available *because* of that structure**. | fixed-rank matrix manifold (given, structured) | cross-domain-analogy |
| [S3] Boumal, Absil, Cartis 2018 — *Global rates of convergence for nonconvex optimization on manifolds* (IMA J. Numer. Anal.; cited ≈288; OA yes; DOI 10.1093/imanum/drx080) | Convergence-rate theory (Riemannian GD / trust regions) — O(1/ε²) to an ε-Riemannian-gradient point, **given a manifold** + Lipschitz-type pullback assumptions. | Riemannian manifolds (given) | cross-domain-analogy |
| [S4] Hu, Liu, Wen, Yuan 2020 — *A Brief Introduction to Manifold Optimization* (J. Oper. Res. Soc. China; cited ≈197; OA yes; DOI 10.1007/s40305-020-00295-9) | Survey; frames "**constrained → unconstrained-on-manifold**"; worked structures are again the standard matrix manifolds. | survey / given matrix manifolds | cross-domain-analogy |
| [S5] Yamakawa, Sato 2022 — *Sequential optimality conditions … and a globally convergent augmented Lagrangian method* (Comput. Optim. Appl.; cited ≈12; OA yes; DOI 10.1007/s10589-021-00336-w) | **Additional** equality/inequality constraints *on top of* a Riemannian manifold, via augmented Lagrangian + global convergence. Closest to "constrained-on-manifold"; **still assumes the base manifold is given**. | constraints on a given Riemannian manifold | cross-domain-analogy |

**Retrieval coverage carried from upstream (a retrieval-coverage fact, NOT a transfer verdict):** Face A *(source machinery)* covered (S1,S2); Face B *(convergence theory)* covered (S3,S5); Face C *(constrained-on-manifold vs standard NLP)* **partial** (S5 only — no head-to-head comparison); Face D *(when is `{h(x)=0}` a well-behaved submanifold, and how is a retraction **constructed** without closed form)* **NOT covered by any kept source** → the two E0 assumptions below.

## Claim–evidence matrix

Each support link's channel is `cross-domain-analogy` unless stated; the `direct` and `same-domain-indirect`
columns are **empty for every row** (shown once, above, not repeated per row). "Contradicts" includes
contradiction *by implication* (a source whose stated scope warns against the general case).

| # | candidate design claim | supports (channel) | contradicts / cautions | E-level | channel |
|---|---|---|---|---|---|
| CL-1 | The retraction / vector-transport / Riemannian-CG machinery is well-defined and usable — **on structured matrix manifolds**. | S1, S2 | — | **E2 (cap)** | cross-domain-analogy |
| CL-2 | Riemannian first-/second-order methods carry convergence-rate & global-convergence guarantees — **given a manifold** + Lipschitz-type assumptions. | S3, S5 | — | **E2 (cap)** | cross-domain-analogy |
| CL-3 | A constrained problem can be viewed as **unconstrained-on-manifold** ("constrained → unconstrained"). | S4 (survey/viewpoint), S5 | — | **E2 (cap)** *(viewpoint-level; softer within analogy)* | cross-domain-analogy |
| CL-4 | **Additional** equality/inequality constraints *on top of a given manifold* can be handled by a globally convergent augmented-Lagrangian method. | S5 | — | **E2 (cap)** | cross-domain-analogy |
| CL-5 | **[THE transfer / decision claim]** This backbone is a sound basis for our **GENERAL equality-constrained / implicit-constraint** solver core. | (by analogy only) S1–S5 | S2 *(cheap retraction exists **because** of matrix structure the general case lacks)*; **Face D uncovered — no source addresses the general/implicit case** | **E2 (cap by channel) → E0 for the general/implicit case** (rests entirely on the two E0 assumptions A1, A2 in the card) | cross-domain-analogy |
| CL-6 | **[Assumption A1]** For a general smooth `h`, the feasible set `{x : h(x)=0}` is a well-behaved **embedded submanifold** under a named CQ (**LICQ / regular-value / constant-rank**) + smoothness `h ∈ Cᵏ`. | **none** (no kept source — Face D) | — | **E0 (assumed, unevidenced)** | project-inference |
| CL-7 | **[Assumption A2]** A **computable retraction** (and vector transport) is **constructible without a closed form**, at acceptable cost (projection / feasibility-restoration / Newton-on-constraint), for that implicit manifold. | **none** (no kept source — Face D) | S2 *(by implication: closed-form/cheap retraction came from structure the general case does not have)* | **E0 (assumed, unevidenced)** | project-inference |

**Reading of the matrix:** CL-1..CL-4 are genuinely supported — but **only in the matrix-manifold / given-manifold
domain**, so as evidence for *our* general solver they are cross-domain-analogy, capped at E2. CL-5 (the decision
claim itself) inherits that E2 channel cap **and** is load-bearing on CL-6/CL-7, which are **E0**. Therefore the
general/implicit-case transfer is, honestly, **unsupported beyond analogy** until A1/A2 are evidenced and an
in-project measurement exists.

## Method-transfer card

### Card T-1: matrix-manifold optimization machinery → our general implicit-constraint solver core
- **Origin setting:** Riemannian optimization on **smooth, structured MATRIX manifolds** (Stiefel, Grassmann,
  fixed-rank, SPD), where geodesics / retractions / projections have **closed-form or cheap** expressions
  (S1, S2); with convergence theory *given* the manifold (S3), a constrained-as-unconstrained viewpoint (S4),
  and augmented-Lagrangian handling of extra constraints *on a given* manifold (S5).
- **Our setting:** a **GENERAL equality-constrained ("implicit-constraint") solver core**, where the feasible set
  `{x : h(x)=0}` for an **arbitrary smooth `h`** is only **implicitly defined** and has **no** closed-form
  geodesic / retraction / projection.
- **Assumptions the transfer relies on** (the explicit form of the HF-12D leap):

  | id | assumption | evidenced or assumed | E-level | source / gap |
  |---|---|---|---|---|
  | **A1** | `{x : h(x)=0}` is a smooth **embedded submanifold** under LICQ / regular-value / constant-rank (+ `h ∈ Cᵏ`), where the machinery is even *defined*. | **ASSUMED** — no kept source (Face D) | **E0** | → gap **G1** (back to RQLP) |
  | **A2** | A **computable retraction** (+ transport) is **constructible without a closed form**, at acceptable cost, for that implicit manifold. | **ASSUMED** — no kept source; S2 warns cheap retraction came from *structure* the general case lacks | **E0** | → gap **G2** (back to RQLP) |
  | **A3** | *Once* a smooth manifold with a cheap retraction is **given**, the machinery + convergence theory apply. | **EVIDENCED — but only in-domain** (S1, S3, S5) | **E2 (analogy cap)** | S1, S3, S5 |
- **Evidenced vs assumed:** the transfer's **downstream half (A3)** is evidenced, but only by analogy (E2). Its
  **two upstream, load-bearing halves (A1 = the manifold even exists; A2 = the retraction is computable) are
  ASSUMED, E0.** A3 is worthless for the decision until A1 and A2 hold — a manifold you cannot build a retraction
  on carries no machinery.
- **E-level cap of the transfer claim:** **E2** by channel (cross-domain-analogy — no `direct`/`same-domain`
  evidence exists), **and** the conclusion cannot honestly exceed **E0** for the general/implicit case while A1
  and A2 are unevidenced. **NOT a direct / project-verified fact.** The E2 ceiling can only be approached — and
  only a `direct` in-project measurement could lift it past E2 — after A1/A2 are closed.
- **Weakest (E0) assumption:** **A2** — a computable retraction constructible *without a closed form* at
  acceptable cost. It is the sharpest E0 because the origin setting's whole advantage (S1, S2) is the
  **closed-form / cheap** retraction that comes *from* matrix structure, and S2 says so explicitly; strip that
  structure and the core operation the backbone depends on may not be constructible or affordable. (A1 is equally
  E0 — the manifold must first *exist* — but A2 is where the origin evidence most directly warns against transfer.)

## Unresolved gaps (+ what would close each, + route)

| # | gap | what closes it | E-now | route |
|---|---|---|---|---|
| **G1** | A1 untested: no source establishes when `{h=0}` is a smooth embedded submanifold under a named CQ (LICQ / regular-value / constant-rank) for a **general** `h`, or where it fails (rank-deficient / near-singular Jacobian, non-smooth / algebraic constraints). Uncovered **Face D**. | A retrieval pass for the **regular-value theorem / CQ ⇔ full-row-rank Jacobian ⇔ embedded submanifold** bridge (smooth-manifolds text + NLP CQ text). | E0 | **BACK to RQLP** (re-scope retrieval — Face D) |
| **G2** | A2 untested: no source **constructs or analyzes** a computable retraction (+ transport) for a **general / implicitly-defined** constraint manifold **without closed form**, at acceptable cost. Uncovered **Face D**. | A retrieval pass for **method papers on projection / feasibility-restoration / Newton-on-constraint retractions** for implicit manifolds. | E0 | **BACK to RQLP** (re-scope retrieval — Face D) |
| **G3** | No **head-to-head comparison**: manifold-optimization vs standard NLP (SQP / augmented-Lagrangian / interior-point) for the **same general equality-constrained** problem (needed for Q3: "sound basis vs dominated-by / defer-to standard NLP"). Face C only **partial** (S5). | Either a retrieval pass for **comparative method papers / numerical studies**, or a project benchmark. | ≤E2 | **BACK to RQLP** (preferred — such comparisons exist in the literature) **OR in-project experiment** |
| **G4** | No **direct (in-project)** evidence: even if A1/A2 are evidenced from literature, transfer to *our* solver at acceptable cost/robustness (rank-deficient / near-singular Jacobian, feasibility-restoration breakdown) is **unmeasured**. | An **in-project experiment** — a prototype retraction/CG on a representative implicit `h` on our problem class. This is the ONLY path from the E2 analogy cap toward a `direct` (E3+) level. | (would be `direct`) | **IN-PROJECT EXPERIMENT** (not retrieval) |

**Routing summary:** **G1 and G2 route BACK to `research-question-and-literature-planner`** (the un-covered Face D
— more retrieval). **G3** is a retrieval gap first (RQLP for comparison studies) with an experiment as fallback.
**G4 needs an in-project experiment**, not retrieval — it is the only gap whose closure could ever raise the map
above E2.

## Coverage note

- **Sources used:** S1–S5 (all real, from the upstream `lit-review-results.md`), each read only for its **own
  stated scope**. **No source was retrieved, searched for, or fetched by this skill.**
- **Evidenced vs assumed:** the machinery, convergence, viewpoint, and on-manifold-constraint claims (CL-1..CL-4,
  and the transfer card's A3) are **evidenced but only cross-domain (E2 cap)**. The two enabling assumptions the
  whole general-case transfer stands on (A1, A2 / CL-6, CL-7) are **assumed, E0** — the uncovered Face D.
- **Channels populated:** **only** `cross-domain-analogy` (S1–S5) and `project-inference` (A1, A2). The `direct`
  and `same-domain-indirect` channels are **empty** — no analogy has been laundered into a direct or
  same-domain claim, and no paper/analogy claim is presented as a **project-verified fact** (D.8).
- **Discipline check (the exact failure this skill guards):** cross-domain transfer **capped at E2**; the two
  un-covered enabling assumptions marked **E0 (assumed, unevidenced)**; **no** project-verified fact asserted;
  **no** retrieval performed.
- **Decisions routed to `uncertainty-and-decision-manager`** (it assigns DECIDED / CANDIDATE / OPEN and records
  `proof_context`) — **not decided here**. **Gaps G1–G3 routed to `research-question-and-literature-planner`**;
  **G4 routed to an in-project experiment.**
