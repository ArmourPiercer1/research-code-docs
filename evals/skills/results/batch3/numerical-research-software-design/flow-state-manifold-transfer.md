<!--
generated_by_skill: numerical-research-software-design
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/ (the Track-B evidence base this run consults), "the manifold-transfer design question"]
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
-->

# Flow-State — `numerical-research-software-design` run on the manifold-transfer design question

A worked v0 skeleton run for the design question *"base the equality-constrained solver core on a
manifold-optimization backbone, or reject/defer?"*. It **consults the real Batch-2.5 Track-B evidence base**
(which already exists on disk) as its evidence front, then demonstrates the honest stop: the numerical-**design**
core (problem-framing, architecture, algorithm spec, prototype, validation, roadmap) is Batch 4 and not built,
so `flow_status=BLOCKED`. The flow authored no design; every artifact below was produced by a delegated atomic
skill (or, for retrieval, the installed stack stand-in).

```yaml
flow_name: numerical-research-software-design
flow_version: 0.1.0
flow_status: BLOCKED
current_stage: uncertainty-and-decision-manager (evidence base assembled; decision registered as HYPOTHESIS)
completed_artifacts:
  - evals/skills/results/batch2_5/research-chain/literature-search-plan.md     # research-question-and-literature-planner
  - evals/skills/results/batch2_5/research-chain/lit-review-results.md         # lit-review (real retrieval, delegated)
  - evals/skills/results/batch2_5/research-chain/research-evidence-map.md      # research-evidence-synthesizer
  - evals/skills/results/batch2_5/research-chain/decision-register.md          # uncertainty-and-decision-manager
  - evals/skills/results/batch2_5/research-chain/quality-advisory.md           # DQE advisory (of the register)
open_decisions:
  - "H-1 backbone decision: HYPOTHESIS (E2 analogy), needs-experiment — NOT decided"
  - "O-A1 / O-A2: two enabling assumptions at E0 (submanifold under LICQ; constructible retraction)"
  - "O-G1 / O-G2: Face-D evidence gaps -> route back to research-question-and-literature-planner"
  - "O-G4: no in-project evidence -> needs an in-project prototype experiment"
blocked_by: "research-software-problem-framer + scientific-software-architect + algorithm-technical-spec-author + scientific-prototype-experiment + scientific-validation-and-benchmark-planner + research-software-roadmap-author (Batch 4 — NOT built)"
next_skill: "human decision (is the E2 evidence enough to commit to a prototype?), THEN the Batch-4 numerical-design core when it exists; in parallel, research-question-and-literature-planner to close G1/G2"
next_input: evals/skills/results/batch2_5/research-chain/decision-register.md
quality_advisory: "evals/skills/results/batch2_5/research-chain/quality-advisory.md (DQE: PASS(90)/ALLOW-advisory — advisory only; authorizes no design/build)"
source_commit: 7919bc4
```

## What ran (route trace — evidence front; each stage delegated, hand-off verified)
- research-question-and-literature-planner → `literature-search-plan.md` (scope + route; E2 cap; **no retrieval**)
- lit-review (installed-stack stand-in, real OpenAlex) → `lit-review-results.md` (5 real sources; Face D flagged un-covered)
- research-evidence-synthesizer → `research-evidence-map.md` (claim–evidence matrix; E2 cap; 2 E0 assumptions; gaps routed)
- uncertainty-and-decision-manager → `decision-register.md` (1 HYPOTHESIS / 5 OPEN / 1 DEFERRED / 0 DECIDED)
- documentation-quality-evaluator (advisory) → `quality-advisory.md` (advisory; authorized nothing)
- Each hand-off verified with `interface_check.py` (all PASS the frozen interface).
- *(A full design run also fronts with `project-state-reconstructor` → `goal-scope-and-workflow-elicitor`; this
  worked example reused the Track-B evidence sub-chain. The flow BLOCKs at the Batch-4 core either way.)*

## Why it stopped here
The next stage — actually **framing the problem, designing the architecture, and writing the algorithm spec**
(`research-software-problem-framer`, `scientific-software-architect`, `algorithm-technical-spec-author`, …) —
requires skills that are **Batch 4 and not built**. Compounding it, the backbone decision is only an **E2
HYPOTHESIS** with two **E0** enabling assumptions unresolved: even if the design atoms existed, an honest flow
would route the gaps (G1/G2) back to the planner and a prototype (G4) before committing. The v0 skeleton records
a named `BLOCKED` and hands the evidence base to a human. This is the correct capability boundary — and it is
why this flow is **third** in the Batch-3 build order (directive §9.3).

## Next handoff
1. A human judges whether the E2 evidence justifies a prototype (or first closes G1/G2 via more retrieval).
2. When the Batch-4 numerical-design core exists, it consumes `decision-register.md` + `research-evidence-map.md`
   to frame the problem and design the architecture/algorithm — with the E2 cap and the two E0 assumptions
   carried through, never laundered into a project fact. Until then: **BLOCKED, honestly.**
