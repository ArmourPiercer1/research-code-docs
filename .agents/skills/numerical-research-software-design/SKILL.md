---
name: numerical-research-software-design
description: "Orchestrate the DESIGN of a numerical / scientific-computing research-software effort — route through fact recovery → goal/scope → literature-scope → retrieval → evidence synthesis → decision register (the evidence base), then hand off to numerical problem-framing, architecture, algorithm spec, prototype/experiment, validation, and roadmap authoring. This is an L1 CONTROL FLOW: it ROUTES to existing atomic skills, persists artifacts, records a flow-state, verifies each hand-off, manages decision points, and STOPS HONESTLY (flow_status=BLOCKED) at any capability not built yet. It does NOT itself frame the problem, design the architecture, write the algorithm spec, or run experiments — those are delegated. Use when someone wants to design/scope a numerical research-software direction (a solver, a method, a scientific pipeline). NOT for a messy code workspace (scientific-workspace-reconstruction), a messy doc corpus (documentation-refactor), or a bare literature question (research-question-and-literature-planner)."
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/user-invoked-only until its control-flow conflict eval passes; v0 SKELETON)
generated_by_skill: manual authoring (Batch 3, control-flow #3; per 2026-08-05 directive §9.3/§10)
source_commit: 7919bc4
source_documents:
  - docs/skill-development/system-architecture.md §3.1 (the numerical-research-software-design chain)
  - docs/skill-development/conflict-matrix.md §1 (control-flow cluster) + §2 (research-adapter delegation)
  - references/interfaces/flow-state.schema.md (the §10.1 flow-state output this flow emits)
  - references/mattpocock-skills/skills/engineering/wayfinder/SKILL.md (MIT — orchestrator: route + persist, don't do the work; method-borrow)
  - references/documentation-methodology/upstream-method-matrix.md §3.3
  - evals/skills/results/batch2_5/research-chain/ (Track B — the validated evidence-front sub-chain this flow consults)
last_verified: 2026-08-05
-->

# Numerical Research-Software Design (L1 control flow · v0 skeleton)

> **Experimental · manual/user-invoked-only · v0 SKELETON.** This flow **orchestrates**; it does not do any
> stage's work itself. Its **evidence-front** sub-chain (state → goal/scope → literature-scope → retrieval →
> evidence synthesis → decision register) uses **built** skills (validated in Batch-2.5 Track B). Its
> **numerical-design core** — problem-framing, software architecture, algorithm spec, prototype/experiment,
> validation, roadmap — is **Batch 4 and not built**, so a real v0 run **stops at `flow_status=BLOCKED /
> blocked_by=research-software-problem-framer + … (Batch 4)`** once the evidence base is assembled. This flow is
> **third** in the build order precisely because its core atoms do not exist yet (directive §9.3).

## Purpose

Take a numerical / scientific-computing research idea (a solver, a method transfer, a simulation pipeline) and
drive its **design**: first assemble the honest evidence base (recovered facts + scoped literature + a
transfer-aware evidence map + a decision register), then (when those skills exist) frame the problem, design the
architecture, specify the algorithm, prototype + validate, and author the roadmap. The flow owns **routing,
persistence, hand-off verification, decision management, and flow-state**; every substantive step is delegated.

## The call chain (route; do not re-implement any stage)

```text
project-state-reconstructor         (what already exists / runs; FACT)  → project-state-report
→ goal-scope-and-workflow-elicitor  (design goal + non-goals + scope)   → goal-scope-note
→ research-question-and-literature-planner (scope+route; never retrieves)→ literature-search-plan
→ lit-review / wos-research / …     (INSTALLED retrieval — the flow delegates) → retrieval results
→ research-evidence-synthesizer     (claim–evidence matrix; E-levels; transfer caps) → research-evidence-map
→ uncertainty-and-decision-manager  (register: HYPOTHESIS/OPEN/DECIDED) → decision-register
── v0 SKELETON STOPS HERE (the numerical-DESIGN core below is Batch 4, NOT BUILT) ──
→ research-software-problem-framer            (problem statement + constraints)   [BLOCKED: not built]
→ scientific-software-architect                (software architecture)            [BLOCKED: not built]
→ algorithm-technical-spec-author              (algorithm math + spec)            [BLOCKED: not built]
→ scientific-prototype-experiment              (GO/MODIFY/STOP/NEED-MORE-EVIDENCE)[BLOCKED: not built]
→ scientific-validation-and-benchmark-planner                                     [BLOCKED: not built]
→ research-software-roadmap-author                                                [BLOCKED: not built]
→ documentation-quality-evaluator              (ADVISORY review)
```

Each hand-off is **verified** against the artifact's frozen interface (`interface_check.py`) before the next
call. The retrieval stage **delegates** to the installed research stack (`lit-review` etc.) — the flow never
retrieves itself (conflict-matrix §2).

## Trigger conditions

Engage when the user wants to **design / scope a numerical or scientific-computing research-software direction**
— a solver, a numerical method, a method transfer, a simulation/analysis pipeline — end-to-end (evidence →
design), not just one narrow step.

## Do-not-trigger conditions (route instead)

- A messy **code / experiment workspace** to recover → `scientific-workspace-reconstruction` (DENY co-run;
  reconstruction runs first, then hands recovered state here — conflict-matrix §1).
- A messy **document corpus** → `documentation-refactor`.
- A bare **literature question** (scope + route only, no design) → `research-question-and-literature-planner`.
- Consuming **already-retrieved evidence** only → `research-evidence-synthesizer`.
- **Never run two L1 flows at once** (conflict-matrix §1); route by dominant artifact after a read-only pass.

## Skeleton duties (directive §10)

Route to the next atomic skill · **delegate retrieval** to the installed stack · persist each artifact · verify
the hand-off (`interface_check.py`) · aggregate open decisions upward · record flow-state (§10.1) · **stop
honestly** at the first missing capability (`flow_status=BLOCKED` + named `blocked_by`) · output the next hand-off.

## Must NOT (directive §10 + §2 delegation)

- **Not** implement the Batch-4 numerical-design atoms (problem-framer / architect / spec-author / prototype /
  validation / roadmap) **inline** to "finish" the design.
- **Not** retrieve literature itself (delegate to `lit-review` / `wos-research` / `deep-research` /
  `paper-fetch-skill`); **not** re-implement synthesis or the register.
- **Not** upgrade paper/analogy evidence to a project fact (that discipline lives in RES/UDM; the flow must not
  launder it either).
- **Not** mark an un-run step completed; **not** move/delete/overwrite; **not** auto-run a second L1 flow;
  **not** treat a DQE `ALLOW` as authorization.

## Inputs / Outputs / Write-scope

- **Input:** the design question/idea + optional existing state/evidence artifacts to resume from.
- **Outputs:** the evidence-front artifacts (each conforming to its frozen interface) **+ one `flow-state`**.
- **Write-scope:** creates NEW files only; `read_only` w.r.t. any target repo; never moves/overwrites/deletes.

## v0 expected result

For a real design question today, the honest v0 result is **`flow_status=BLOCKED`,
`blocked_by=research-software-problem-framer + scientific-software-architect + … (Batch 4 — not built)`**, with
the evidence base (search-plan → evidence-map → decision-register) assembled and handed to a human. Worked
example: `evals/skills/results/batch3/numerical-research-software-design/flow-state-manifold-transfer.md` (it
consults the real Batch-2.5 Track-B evidence base and stops honestly at the missing Batch-4 core).

## References / Scripts

- `references/interfaces/flow-state.schema.md` + `docs/skill-development/system-architecture.md` §3.1 +
  `conflict-matrix.md` §1/§2.
- `interface_check.py` (verify each hand-off) · `flow_state_check.py` (honest BLOCKED) · `run_checks.py`.
