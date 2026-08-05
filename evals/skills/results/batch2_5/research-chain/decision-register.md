---
generated_by_skill: uncertainty-and-decision-manager
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/research-evidence-map.md, evals/skills/results/batch2_5/research-chain/literature-search-plan.md]
artifact_type: decision-register
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Single source of truth for the uncertain items behind ONE decision — whether to base the solver's equality-constrained ('implicit-constraint') core on a manifold-optimization backbone (retraction / vector transport / Riemannian CG), or reject/defer to standard NLP. Records uncertainty STATE only: it does NOT make the decision and does NOT convert the RES evidence map into a user decision (directive §3.2) — a human/gate decides. Excludes: retrieval, the in-project experiment itself, and any fact upgrade past the E2 cross-domain-analogy cap."
facts: "none (no E3+ in-project proof exists; all evidence in the RES map is cross-domain-analogy capped at E2 — D.8: paper/analogy is never a project-verified fact; no entry is FACT/VERIFIED/BASELINE/DECIDED)"
hypotheses: "1 HYPOTHESIS — see Register H-1 (the transfer/backbone claim; E2 cross-domain-analogy cap; disposition needs-experiment; NOT decided)"
open_questions: "6 OPEN/DEFERRED — see Register: O-A1, O-A2 (enabling assumptions, E0, needs-evidence) + O-G1, O-G2, O-G3 (OPEN gaps → research-question-and-literature-planner) + O-G4 (DEFERRED → in-project experiment). Never 'none' — the decision is unsettled."
evidence_level: "E0–E2 across entries. Paper/analogy carries the RES cross-domain cap ≤ E2: H-1 at E2 (channel cap). Enabling assumptions O-A1/O-A2 and gaps O-G1/O-G2/O-G4 at E0 (assumed/unevidenced); O-G3 at E1 (partial S5, ceiling ≤ E2). No entry reaches E3+: no direct in-project measurement exists, so none may be called verified/FACT."
next_handoff: documentation-quality-evaluator
handoff_requirements: "The advisory reviewer / decision gate needs, per entry: status + evidence E-level + a re-openable locator (evidence-map row id / DOI#context) + disposition. It MUST treat H-1 as a HYPOTHESIS (E2 analogy, not a decision), keep O-A1/O-A2 as OPEN (E0), and honor the gap routing: O-G1/O-G2/O-G3 back to research-question-and-literature-planner (re-scope retrieval — Face D / Face C), O-G4 to an in-project experiment (the only path off the E2 cap). No item may be read as DECIDED/VERIFIED; any future reversal must be by SUPERSEDE (append new + point back), never by edit. A human/gate — not this register — makes the base/reject/defer decision."
---

# Decision Register — Manifold-optimization backbone for a general equality-constrained ("implicit-constraint") solver core

The single source of truth for the uncertain items behind this one decision. It **records state; it does not
decide** — the base/reject/defer choice is made by a human/gate, not by this register (directive §3.2). Stable,
decided terms would graduate to the `domain-modeling` glossary; code facts live in the state report. Status +
evidence vocabulary follows the frozen interface; **only E3+ (a direct in-project measurement) may be called
"verified"** — and none exists here, so the whole register is capped at **E2** (cross-domain-analogy).

**Discipline held in this register (do not blur):**
- `HYPOTHESIS` (H-1), `OPEN` (O-A1, O-A2, O-G1–O-G3) and `DEFERRED` (O-G4) are kept **distinct**. There is **no
  `DECIDED`/`BASELINE`/`VERIFIED`/`FACT`/`CANDIDATE`** entry — no one has decided, and no candidate option has
  been adopted.
- Paper/analogy evidence is **never promoted past E2**; the RES map's E2 cap is carried through unchanged.
- The RES evidence map was **not auto-converted into a user decision** — the transfer claim is registered as an
  open HYPOTHESIS awaiting an experiment, not as a chosen backbone.
- Every `source` is a **re-openable locator** (evidence-map row id / `DOI#section`), never a bare author name.
- Reversal, if the decision is ever made and later changed, is **by SUPERSEDE** (append a new entry with
  `supersedes:` + mark the old `STALE`/`REJECTED` with a `reason`), never by editing a decided item.

## Register

```yaml
# One entry per tracked item. status ∈ {FACT,VERIFIED,DECIDED,BASELINE,HYPOTHESIS,
# CANDIDATE,OPEN,DEFERRED,REJECTED,STALE}; evidence ∈ {E0..E5}; source = a re-openable
# LOCATOR (file#anchor / row-id / DOI#section), never a bare name; disposition ∈
# {supported, needs-evidence, needs-experiment}. Only E3+ (direct in-project proof) may be
# VERIFIED/FACT — NONE qualifies here (paper/analogy capped at E2). Reversal is by SUPERSEDE,
# never by editing a decided item. No item below is DECIDED — a human/gate decides.

# ── THE transfer / backbone decision claim → HYPOTHESIS (recorded, NOT decided) ──
- id: H-1
  statement: "Base the solver's GENERAL equality-constrained / implicit-constraint core on a manifold-optimization backbone (retraction / vector transport / Riemannian gradient / CG)."
  status: HYPOTHESIS
  evidence: E2
  source: "research-evidence-map.md#CL-5 (THE transfer/decision claim) + Method-transfer card T-1; supported by-analogy only via S1–S5; sharpest caution S2 DOI:10.1137/110845768#retraction (cheap retraction exists BECAUSE of matrix structure the general case lacks); literature-search-plan.md#cross-domain-transfer-warning (genuine leap; E2 cap)"
  disposition: needs-experiment
  decided_by: null
  last_verified: "2026-08-05"
  notes: "NOT DECIDED — no human/gate has chosen; this records state only (directive §3.2). E2 is the CHANNEL cap (cross-domain-analogy; the direct and same-domain-indirect channels are EMPTY in the RES map). Load-bearing on O-A1 and O-A2 (both E0) → for the general/implicit case the claim is honestly unsupported beyond analogy until A1/A2 are evidenced AND an in-project measurement (O-G4) exists. Only a direct E3+ in-project result could lift this past E2; an analogy/published result may NEVER be called verified. In-domain support CL-1..CL-4 (S1–S5) is genuine but ONLY on structured matrix manifolds, so it transfers as analogy, not proof. No discharge attempted and none recorded → stays HYPOTHESIS, not promoted."

# ── The two enabling assumptions the transfer stands on → OPEN, E0 ──
- id: O-A1
  statement: "Assumption A1: for a general smooth h, the feasible set {x : h(x)=0} is a well-behaved embedded submanifold under a named constraint qualification (LICQ / regular-value / constant-rank) with smoothness h ∈ C^k — i.e. the manifold the machinery needs even EXISTS."
  status: OPEN
  evidence: E0
  source: "research-evidence-map.md#CL-6 (Assumption A1) + Method-transfer card T-1 row A1 — ASSUMED, no kept source (uncovered Face D)"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-08-05"
  notes: "E0 (assumed, unevidenced; project-inference channel). This is where the machinery is even DEFINED — the manifold must first exist. Closed by gap O-G1 (routed BACK to research-question-and-literature-planner). Not promoted: no evidence, no discharge, no decision."
- id: O-A2
  statement: "Assumption A2: a computable retraction (+ vector transport) is constructible WITHOUT a closed form, at acceptable cost (projection / feasibility-restoration / Newton-on-constraint), for that implicit manifold."
  status: OPEN
  evidence: E0
  source: "research-evidence-map.md#CL-7 (Assumption A2) + Method-transfer card T-1 row A2 — ASSUMED, no kept source (Face D); S2 DOI:10.1137/110845768#retraction warns cheap retraction came from matrix structure the general case lacks"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-08-05"
  notes: "E0 (assumed, unevidenced; project-inference). The RES map's sharpest E0 — the origin setting's whole advantage is the closed-form/cheap retraction from matrix structure, and S2 says so explicitly; strip that structure and the core operation may not be constructible or affordable. Closed by gap O-G2 (routed BACK to research-question-and-literature-planner)."

# ── The four unresolved gaps → OPEN / DEFERRED, each with its route ──
- id: O-G1
  statement: "Gap G1: no source establishes when {x : h(x)=0} is a smooth embedded submanifold under a named CQ for a general h, or where it fails (rank-deficient / near-singular Jacobian, non-smooth / algebraic constraints). Uncovered Face D — this gap closes assumption A1 (O-A1)."
  status: OPEN
  evidence: E0
  source: "research-evidence-map.md#Unresolved-gaps G1 (Face D; would be closed by the regular-value theorem / CQ ⇔ full-row-rank Jacobian ⇔ embedded-submanifold bridge)"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-08-05"
  notes: "Route: BACK to research-question-and-literature-planner (re-scope retrieval — Face D). Addresses assumption O-A1."
- id: O-G2
  statement: "Gap G2: no source CONSTRUCTS or ANALYZES a computable retraction (+ transport) for a general / implicitly-defined constraint manifold WITHOUT closed form, at acceptable cost. Uncovered Face D — this gap closes assumption A2 (O-A2)."
  status: OPEN
  evidence: E0
  source: "research-evidence-map.md#Unresolved-gaps G2 (Face D; would be closed by method papers on projection / feasibility-restoration / Newton-on-constraint retractions for implicit manifolds)"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-08-05"
  notes: "Route: BACK to research-question-and-literature-planner (re-scope retrieval — Face D). Addresses assumption O-A2."
- id: O-G3
  statement: "Gap G3: no head-to-head comparison of manifold-optimization vs standard NLP (SQP / augmented-Lagrangian / interior-point) for the SAME general equality-constrained problem (needed for Q3 — sound basis vs dominated-by / defer-to standard NLP). Face C only partial (S5)."
  status: OPEN
  evidence: E1
  source: "research-evidence-map.md#Unresolved-gaps G3 (Face C partial — S5 only, no head-to-head); nearest partial source S5 DOI:10.1007/s10589-021-00336-w"
  disposition: needs-evidence
  decided_by: null
  last_verified: "2026-08-05"
  notes: "E1 = single partial signal (S5); retrieval ceiling ≤ E2 (still cross-domain) — the RES map records E-now ≤E2. Route: BACK to research-question-and-literature-planner (preferred — such comparison studies exist) OR an in-project experiment as fallback."
- id: O-G4
  statement: "Gap G4: no DIRECT (in-project) evidence — even if A1/A2 are evidenced from the literature, transfer to OUR solver at acceptable cost/robustness (rank-deficient / near-singular Jacobian, feasibility-restoration breakdown) is UNMEASURED."
  status: DEFERRED
  evidence: E0
  source: "research-evidence-map.md#Unresolved-gaps G4 (no in-project trial run; the direct channel is EMPTY across the whole map)"
  disposition: needs-experiment
  decided_by: null
  reason: "Deferred to an in-project experiment phase — it CANNOT be closed by literature retrieval. A prototype retraction/CG on a representative implicit h on our problem class is the ONLY path off the E2 analogy cap toward a direct (E3+) level. Postponed, not rejected."
  last_verified: "2026-08-05"
  notes: "Route: IN-PROJECT EXPERIMENT (not retrieval). Closing G4 together with A1/A2 is the only way H-1 could ever exceed E2 and become a candidate for verification/decision."
```

## Reversal & decision boundary

- **This register does not close the decision.** H-1 is an open HYPOTHESIS; the base/reject/defer call is made
  by a **human/gate** after the OPEN/DEFERRED items are addressed. No entry is `DECIDED`/`BASELINE`/`VERIFIED`.
- **If the decision is later made and then changed,** reverse **by SUPERSEDE**: append a new entry with
  `supersedes: <old-id>`, mark the old entry `STALE`/`REJECTED` with `superseded_by:` + a `reason`. Decided
  entries are append-only; both rows survive a reversal.
- **Promotion gate.** H-1 → any decided status requires, per skill: one recorded adversarial disproof attempt
  (`discharge`) + `decided_by`, and its `needs-experiment` disposition discharged (O-G4 closed). None is present,
  so H-1 stays HYPOTHESIS.

## Change log

| date | id | change |
|---|---|---|
| 2026-08-05 | H-1 | registered the transfer/backbone claim as HYPOTHESIS (E2 analogy cap; needs-experiment; NOT decided) from research-evidence-map CL-5 / card T-1 |
| 2026-08-05 | O-A1 | registered enabling assumption A1 as OPEN (E0; needs-evidence) from CL-6 / card T-1 row A1 |
| 2026-08-05 | O-A2 | registered enabling assumption A2 as OPEN (E0; needs-evidence) from CL-7 / card T-1 row A2 |
| 2026-08-05 | O-G1 | registered gap G1 as OPEN → route BACK to research-question-and-literature-planner (Face D); addresses O-A1 |
| 2026-08-05 | O-G2 | registered gap G2 as OPEN → route BACK to research-question-and-literature-planner (Face D); addresses O-A2 |
| 2026-08-05 | O-G3 | registered gap G3 as OPEN → route BACK to research-question-and-literature-planner or experiment (Face C partial) |
| 2026-08-05 | O-G4 | registered gap G4 as DEFERRED → in-project experiment (only path off the E2 cap) |
