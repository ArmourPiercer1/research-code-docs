# Research Software Agent Workflow Reconstruction Charter

> Purpose: use the full DeepSeek Harness (`deepseek-harness`, abbreviated **DSH**) repository and its Git history as a reference system, then audit, redesign, and incrementally rebuild this repository's own agent-driven research-software development workflow.
>
> This document is a **development charter + investigation contract + implementation-plan seed**. It is **not** permission to immediately rewrite every Skill. The first obligation is to reconstruct the current system, extract transferable evidence from DSH, define target invariants, and produce a reviewed architecture before broad implementation begins.

---

## 0. Operating principle

The objective is **not** to maximize the number of Skills, orchestration layers, documents, or workflow states.

The objective is to minimize:

- human cognitive load during long-running research/software projects;
- agent context load when resuming or delegating work;
- ambiguity between facts, hypotheses, decisions, plans, and implementation state;
- duplicated or stale canonical information;
- integration cost between parallel agent tasks;
- the probability that incorrect work silently enters the main development line;
- the long-term entropy of research repositories and their documentation.

Prefer a **small number of deep, composable capabilities** over a large catalog of overlapping roles.

Whenever a rule can be enforced mechanically, prefer a schema, checker, test, repository convention, or CI gate over prose-only guidance.

Whenever a new abstraction is proposed, ask whether deleting or simplifying an existing abstraction would solve the same problem more cleanly.

---

# 1. Mission

Build an agent-native development workflow suitable for long-running research software projects that must support all of the following:

1. **Greenfield repository bootstrap**
   - create a new repository from zero;
   - establish only the minimum useful structure, checks, documentation ownership, and development contracts;
   - avoid premature framework/governance inflation.

2. **Messy repository reconstruction and simplification**
   - recover what actually exists, runs, is tested, and is validated;
   - distinguish current fact from stale documentation and historical intent;
   - identify high-value simplification opportunities;
   - incrementally restructure the repository without assuming that a complete target architecture must be designed first.

3. **Multiple related development/research routes under one larger project**
   - manage several workstreams/routes that may share code, data, tools, and evidence;
   - distinguish implementation dependencies from research alternatives;
   - support parallel work without forcing every route into one linear roadmap or PR stack.

4. **Research uncertainty and evolving methods**
   - preserve ideas that are promising but under-specified;
   - represent several competing approaches without falsely promoting any to “the plan”;
   - track hypotheses, candidate methods, open questions, decisions, and evidence;
   - support method changes during implementation;
   - preserve why a route was rejected, deferred, superseded, or revived;
   - select experiments that most efficiently discriminate between competing routes.

5. **Long-task and multi-agent development**
   - decompose work by **context boundary**, not merely by software module or feature label;
   - use explicit contracts for planning, execution, review, and integration;
   - maximize safe parallelism while controlling integration cost.

6. **Long-term knowledge integrity**
   - give every important information type one canonical home;
   - keep current-state documentation current;
   - keep decision rationale separate from current-state reference documentation;
   - preserve evidence lineage without turning every intermediate thought into permanent documentation;
   - archive/supersede stale material rather than allowing the active corpus to grow without bound.

---

# 2. Existing systems that MUST be audited first

Before proposing the target system, inspect the current skills repositories and reconstruct the actual design.

At minimum inspect:

- `research-code-dev`
- `research-code-docs`

Locate their current paths automatically if this working repository vendors or mirrors them elsewhere.

Pay particular attention to the current implementations and interactions of:

- `project-state-reconstructor`
- `uncertainty-and-decision-manager`
- `research-evidence-synthesizer`
- `living-design-maintainer`
- `scientific-workspace-reconstruction`
- repository/workspace forensics skills
- documentation refactor skills
- goal/scope elicitation skills
- `wayfinder`
- `to-spec`
- `to-tickets`
- `implement`
- `tdd`
- `code-review`
- architecture/codebase-improvement skills
- handoff/context-management skills
- any existing ADR/decision-note machinery
- existing eval harnesses, schemas, checkers, flow-state files, registries, and release governance.

Do not trust README descriptions as sufficient evidence of behavior. Treat them as claims to verify against:

- Skill files;
- schemas;
- checkers;
- tests/evals;
- orchestrator code;
- example outputs;
- Git history.

---

# 3. Phase 0A — reconstruct the current system

Produce a factual map of the existing system before redesigning it.

## 3.1 Required analysis dimensions

For every existing Skill or workflow, record:

- name;
- purpose;
- trigger conditions;
- non-trigger conditions;
- inputs;
- outputs;
- read scope;
- write scope;
- whether it is atomic, orchestration/control-flow, policy/reference, or evaluator;
- whether outputs are canonical or transient;
- upstream/downstream dependencies;
- external dependencies;
- schemas/checkers that enforce its artifacts;
- actual eval coverage;
- known unsupported or BLOCKED downstream capabilities;
- overlap with other Skills;
- information types it owns;
- information types it duplicates;
- common failure modes;
- current maintenance burden.

## 3.2 Classification matrix

Every current Skill must be classified as one of:

- `KEEP`
- `REFINE`
- `MERGE`
- `SPLIT`
- `REPLACE`
- `ADD`
- `REMOVE`

Do not assign these labels from aesthetics. Each classification must cite concrete reasons from current repository evidence.

## 3.3 Explicitly identify structural problems

Search for:

- multiple Skills owning the same information type;
- one Skill carrying too many unrelated responsibilities;
- orchestration Skills that mostly reproduce downstream Skill logic;
- control flows that cannot complete because required capabilities do not exist;
- artifact proliferation;
- status vocabularies mixing unrelated dimensions;
- canonical artifacts that are really session-local planning outputs;
- stale-roadmap risk;
- duplicated “current state” descriptions;
- separate maintenance artifacts that could instead become same-change updates;
- places where Git/PR/test state is duplicated in custom documents;
- high-context Skills that require too much repository reading;
- permanent documents that mostly contain implementation chronology.

---

# 4. DSH reference system: what to study

The DSH repository is a **reference and evidence source**, not a template to copy verbatim.

Study both the current repository and the history that produced it.

At minimum inspect:

- root and subtree `AGENTS.md`;
- `.agents/skills/`;
- `.agents/notes/`;
- current Agent Note rules and lifecycle;
- `docs/AGENTS.md`;
- `docs/testing.md`;
- `docs/architecture.md`;
- package/subsystem documentation conventions;
- `docs/postmortem/`;
- CI workflows;
- repository scripts that mechanically enforce conventions;
- snapshot/replay infrastructure;
- pre-push/test-selection logic;
- code-review skills;
- simplification skills;
- Agent Note archival/supersession rules;
- stacked-PR/worktree integration practices;
- test-reliability guidance;
- commit and PR history for important workflow changes.

Important candidate Skills/mechanisms to inspect include, but are not limited to:

- `dsh-find-simplifications`
- `dsh-pre-push-checks`
- `dsh-code-review`
- `dsh-ci-test-reliability`
- `dsh-archive-agent-notes`
- `dsh-doc`
- `dsh-merging-stacked-prs`

Also inspect the historical evolution of:

- quality gates;
- fresh-clone CI failures;
- snapshot/replay testing;
- real-entry-path testing;
- flaky-test fixes;
- performance-gate design;
- documentation ownership;
- Agent Note format/lifecycle;
- removed packages/APIs;
- simplified or superseded abstractions.

---

# 5. DSH historical evidence protocol

Do not summarize DSH by reading only the latest files.

For every mechanism considered for adoption, build an evidence chain:

```text
Observed DSH mechanism
        ↓
Problem it was solving
        ↓
Historical evidence that the problem mattered
        ↓
How DSH encoded the solution
        ↓
How the solution evolved
        ↓
What later got removed or simplified
        ↓
Whether the same problem exists here
        ↓
What generic principle is transferable
        ↓
What must NOT be copied
```

## 5.1 Evidence sources

Prefer, in order:

1. current source and machine-enforced rules;
2. Agent Notes explaining the decision and alternatives;
3. commits/PRs that introduced or changed the mechanism;
4. postmortems and bug-fix history;
5. tests and CI workflows showing what is actually enforced;
6. README/prose summaries.

## 5.2 Historical questions to answer

For each important DSH mechanism:

- When was it introduced?
- What failure, scaling pressure, review problem, or maintenance burden motivated it?
- What was the first design?
- What changed afterward?
- Which parts were later deleted?
- Which parts remained stable?
- What did DSH move from prose to mechanical enforcement?
- What did DSH intentionally leave as human/agent judgment?
- Which mechanisms exist only because DSH is a pre-release TypeScript/Cordis product?
- Which mechanisms are generic enough to migrate?

## 5.3 Required DSH crosswalk artifact

Create a table with at least:

| DSH mechanism | Original problem | Historical evidence | Generic principle | Relevance here | Proposed adaptation | DSH-specific parts to reject |
|---|---|---|---|---|---|---|

Do not treat “DSH has this Skill” as sufficient justification for creating an equivalent Skill here.

---

# 6. Negative evidence and deleted designs

Study what DSH **removed**, not only what survived.

Search especially:

- simplification Agent Notes;
- archived implemented notes;
- rejected notes;
- removed APIs;
- removed packages;
- collapsed seams;
- duplicated representations;
- obsolete testing/process machinery;
- speculative functionality that was later deleted.

For each relevant deletion, ask:

- Why did the abstraction originally seem useful?
- What evidence later showed that it cost more than it bought?
- What replaced it?
- Could our current system contain the same pattern?

This section is mandatory because a workflow system can fail by becoming too elaborate even when each individual addition was locally reasonable.

---

# 7. Transferability rules

Every proposed import from DSH must be labeled as one of:

- `DIRECTLY TRANSFERABLE`
- `TRANSFERABLE AFTER GENERALIZATION`
- `RESEARCH-SPECIFIC ADAPTATION REQUIRED`
- `DSH-SPECIFIC — DO NOT COPY`

Examples of the expected reasoning:

- DSH PR stacks solve implementation dependency; research alternatives are not automatically PR stacks.
- DSH pre-push “smallest relevant evidence” can generalize to “smallest discriminating experiment”.
- DSH Agent Notes can inform research decision notes, but research evidence needs richer provenance than software architecture rationale.
- DSH current-state documentation ownership generalizes well.
- DSH exact TypeScript/Cordis gates do not.

---

# 8. Target system invariants

Define the target architecture from invariants first, not from Skill names.

The final system must satisfy at least the following.

## 8.1 Truth separation

These information classes must remain distinguishable:

- current repository reality;
- current product/software contracts;
- research evidence;
- hypothesis;
- candidate approach;
- open question;
- decision rationale;
- implementation state;
- future proposal;
- execution plan;
- session-local context;
- historical chronology.

Do not create a single artifact that tries to be authoritative for all of them.

## 8.2 One canonical owner per fact

Every durable information type has one canonical owner.

Other documents should link to that owner instead of repeating the same fact.

## 8.3 No silent promotion

The system must never silently equate:

- idea with hypothesis;
- hypothesis with candidate;
- candidate with decision;
- literature evidence with in-project verification;
- prototype with supported implementation;
- code existence with tested behavior;
- test existence with passing validation;
- agent self-report with external evidence.

## 8.4 Orthogonal state dimensions

Do not use one status enumeration to mix:

- decision lifecycle;
- evidence strength;
- freshness;
- implementation progress;
- object role.

Prefer orthogonal fields when these concepts can vary independently.

## 8.5 Decision reversal by supersession

A durable decision must not be silently rewritten into its opposite.

Reversal or material redesign must preserve decision lineage through supersession/cross-linking.

## 8.6 Current-state docs stay current

README, architecture, API/reference, and package docs describe current reality.

They do not become change logs.

## 8.7 Evidence-backed completion

A task can only be called complete when the relevant external evidence passes.

Prefer verification of the world over agent self-report.

## 8.8 Smallest useful evidence

For software changes:

- choose the narrowest evidence sufficient to catch the regression.

For research uncertainty:

- choose the smallest experiment likely to change the ranking between competing routes.

## 8.9 Context-bounded task decomposition

Decompose long tasks by the context required to execute them correctly.

Do not use software module/feature boundaries by default if they force each executor to load excessive unrelated context.

## 8.10 Parallelism with explicit dependencies

Represent:

- true blocking dependencies;
- optional dependencies;
- shared resources;
- independent routes.

Do not linearize independent work unnecessarily.

## 8.11 Complexity ratchet in both directions

Support both:

```text
repeated failure → add guardrail
```

and:

```text
obsolete abstraction/guardrail → remove or simplify
```

The workflow must have an explicit simplification path.

## 8.12 Bounded active corpus

Active decision/state artifacts must not grow without bound.

The system must define:

- archival conditions;
- supersession rules;
- deletion criteria;
- what should remain only in Git history.

---

# 9. Target capability model

Design capabilities by lifecycle/family first.

Only afterward decide which capabilities deserve standalone Skills.

## 9.1 Repository lifecycle

Potential capabilities:

- greenfield bootstrap;
- bounded inventory;
- project-state reconstruction;
- simplification audit;
- migration/restructure planning;
- repository health/contract verification.

## 9.2 Change lifecycle

Potential capabilities:

- problem clarification;
- proposal/decision capture;
- implementation planning;
- context-bounded task decomposition;
- implementation;
- focused verification;
- code review;
- integration;
- post-change canonical-doc maintenance.

## 9.3 Research lifecycle

Potential capabilities:

- idea capture;
- hypothesis management;
- candidate-route management;
- evidence synthesis;
- evidence provenance;
- next discriminating experiment;
- experiment result ingestion;
- decision promotion;
- rejection/defer/supersede;
- revisit conditions.

## 9.4 Multi-agent lifecycle

Potential capabilities:

- plan contract creation;
- executor context contract;
- worktree/branch isolation;
- dependency graph;
- safe parallel scheduling;
- integration ordering;
- handoff;
- review;
- failure recovery.

## 9.5 Knowledge lifecycle

Potential capabilities:

- canonical-source ownership;
- current-state documentation;
- research evidence store;
- decision notes;
- active decision register;
- archival/supersession;
- stale-reference detection;
- corpus simplification.

---

# 10. Decide the mechanism, not just the Skill

For every capability, explicitly decide whether it belongs primarily in:

- a Skill;
- repository convention;
- `AGENTS.md` instruction;
- schema;
- deterministic checker;
- test;
- CI gate;
- Git/PR convention;
- canonical document format;
- human approval boundary;
- existing external tool;
- no automation at all.

A new Skill is justified only if an agent must repeatedly apply non-trivial judgment or orchestration.

If a requirement can be enforced by a deterministic checker, do not create a Skill merely to restate it.

If Git already records the necessary history, do not create another permanent ledger unless there is a concrete retrieval/decision need Git does not satisfy.

---

# 11. Skill portfolio review

After Phase 0/1 analysis, produce a proposed Skill portfolio.

For every current or proposed Skill, use this schema:

```yaml
name:
problem:
current_owner:
proposed_action: keep | refine | merge | split | replace | add | remove

why_this_must_be_a_skill:

trigger:
non_trigger:

inputs:
outputs:

canonical_or_transient:

reads:
writes:

upstream:
downstream:

invariants:

mechanical_checks:

failure_modes:

evals:

dsh_basis:
research_specific_delta:
```

A proposal without a convincing `why_this_must_be_a_skill` should default to another mechanism or be removed.

---

# 12. Specific candidate changes to investigate

Do not assume these are final decisions, but explicitly evaluate them.

## 12.1 Greenfield repository bootstrap

Investigate creating a minimal `repo-bootstrap` capability with:

- minimal repository skeleton;
- project terminology/context entry point;
- minimum test/static/build feedback loop;
- decision-note location;
- current-state architecture/document ownership;
- optional CI;
- no speculative large governance tree.

Prefer a “ratchet” model:

1. bootstrap minimal;
2. add mechanical guardrails only after concrete need/failure appears.

## 12.2 Repository simplification audit

Investigate adapting DSH `dsh-find-simplifications` into a generic research/software cleanup Skill.

Potential research-specific targets include:

- orphan scripts;
- stale notebooks;
- duplicated pipelines;
- multiple implementations of one algorithm;
- result artifacts that cannot be reproduced;
- obsolete parameters/configuration paths;
- temporary prototypes becoming de facto production dependencies;
- abandoned experiment branches;
- speculative abstractions;
- tests/docs that are the only consumers of obsolete behavior.

The Skill should prefer a few evidence-backed candidates over a large shallow list.

## 12.3 Focused change evidence selector

Investigate adapting DSH `dsh-pre-push-checks` into a generic:

- change-scope analyzer;
- smallest-relevant-test selector;
- evidence-owner selector.

Do not run full local validation by default when a narrower sufficient check exists.

## 12.4 Research route manager

Investigate a lightweight route/workstream manager that distinguishes:

- implementation dependency routes;
- alternative research hypotheses;
- shared code/data/evidence;
- active/deferred/rejected routes.

A route should emphasize:

- goal;
- status;
- dependencies;
- active decisions;
- open questions;
- evidence;
- next discriminator;
- next action.

Avoid a giant Project→Topic→Workstream→Node hierarchy unless evidence proves it is necessary.

## 12.5 Next discriminating experiment

Investigate a Skill that asks:

> What is the smallest experiment that is most likely to change which route we should pursue?

It should optimize information gain/decision value rather than simply “continue the next task”.

## 12.6 Decision model refactor

Evaluate refactoring `uncertainty-and-decision-manager`.

Current concern: a single status vocabulary may mix:

- epistemic status;
- decision lifecycle;
- freshness;
- implementation progress;
- role.

Investigate orthogonal fields such as:

```yaml
kind: idea | hypothesis | claim | candidate | decision | route

decision_state:
  proposed | decided | rejected | deferred | superseded

evidence_level:
  E0 | E1 | E2 | E3 | E4 | E5

evidence_state:
  current | stale | contradicted

implementation_state:
  none | planned | in_progress | implemented | blocked
```

Do not adopt this exact schema without testing it against real examples.

## 12.7 Research Decision Notes

Investigate adding a durable decision-note layer inspired by DSH Agent Notes.

Potential structure:

```text
Problem / Question
Proposal or Decision
Evidence basis
Alternatives considered
Why this choice
Consequences
Revisit condition
```

Evidence should usually be linked, not duplicated.

Target distinction:

```text
Decision Register
= active, fine-grained, changing state

Decision Note
= compressed durable rationale worth future re-reading
```

## 12.8 Living design maintenance

Evaluate whether `living-design-maintainer` should evolve from:

- producing standalone maintenance proposal artifacts

toward:

- determining canonical owners impacted by a change;
- updating those owners in the same PR/change;
- using mechanical stale-link/ownership checks;
- reserving separate maintenance reports only when explicit review is useful.

---

# 13. Artifact and canonical-source model

Produce a canonical-source map for the target system.

At minimum decide owners for:

- current repository state;
- project architecture;
- package/module contracts;
- current roadmap/active routes;
- evidence;
- experiment results/provenance;
- open decisions;
- durable decision rationale;
- execution plans;
- task dependency graph;
- session handoff;
- incident history;
- implementation history.

For each information type specify:

```text
canonical owner
lifecycle
update trigger
archive/delete rule
allowed references
forbidden duplication
```

---

# 14. Evaluation strategy

The redesign is incomplete until it has evals.

## 14.1 Atomic Skill evals

Test:

- correct trigger;
- correct non-trigger;
- write-scope discipline;
- artifact interface;
- fact/hypothesis separation;
- refusal to overclaim;
- deterministic checker compatibility;
- context boundedness.

## 14.2 Workflow evals

Build end-to-end scenarios such as:

### Scenario A — messy repository

```text
messy repo
→ state reconstruction
→ simplification survey
→ decision/proposal
→ implementation
→ focused verification
→ review
```

### Scenario B — greenfield repository

```text
goal
→ minimal bootstrap
→ first feature
→ first decision
→ first mechanical guardrail
```

### Scenario C — competing research routes

```text
idea set
→ hypotheses/candidates
→ evidence synthesis
→ route state
→ discriminating experiment
→ result
→ decision update
```

### Scenario D — long multi-agent task

```text
problem
→ planning contract
→ context-bounded tasks
→ parallel execution
→ integration
→ review
```

## 14.3 Adversarial evals

Deliberately inject:

- stale roadmap;
- contradictory evidence;
- obsolete result artifacts;
- duplicate facts in several docs;
- unsupported “verified” claims;
- half-implemented feature;
- misleading saved notebook output;
- branch divergence;
- stale decision;
- route that should be rejected;
- agent claiming success without external evidence;
- duplicated or speculative abstractions.

The system should not silently accept them.

## 14.4 Longitudinal evals

Simulate many iterations.

Measure at least:

- active artifact count;
- duplicated canonical facts;
- stale-reference count;
- number of unresolved decisions;
- number of superseded artifacts still active;
- context required for cold-start resume;
- token/time cost to reconstruct current state;
- time to identify the next actionable task;
- number of Skills involved in a common workflow;
- number of artifacts generated per change;
- rate at which obsolete workflow machinery is removed.

The system should remain understandable after many changes, not only in a fresh demo.

---

# 15. Development process

Do not perform a repository-wide rewrite in one pass.

## Phase 0 — Audit only

Read-only.

Deliver:

- `current-system-map.md`
- `existing-skill-classification.md`
- `current-information-ownership-map.md`
- `pain-point-evidence.md`

No broad Skill implementation.

## Phase 1 — DSH investigation + architecture proposal

Deliver:

- `dsh-workflow-evidence-map.md`
- `dsh-transferability-crosswalk.md`
- `target-workflow-invariants.md`
- `target-capability-architecture.md`
- `canonical-information-model.md`
- `skill-change-matrix.md`
- `eval-plan.md`

Stop here for architecture review before broad implementation.

## Phase 2 — Minimal vertical slice

Implement only one closed loop first.

Preferred candidate:

```text
messy repository
→ project-state-reconstructor
→ repo-simplification-audit
→ Decision Note
→ implementation
→ focused verification
→ review
```

The slice must have evals.

## Phase 3 — Expand

After the vertical slice passes:

- greenfield bootstrap;
- multi-route management;
- research uncertainty/decision refactor;
- discriminating experiments;
- multi-agent execution/integration.

## Phase 4 — Simplification pass

Run a dedicated workflow simplification audit on the newly built system.

Ask:

- Which new Skills are redundant?
- Which schemas duplicate each other?
- Which artifacts can be removed?
- Which orchestration steps can be collapsed?
- Which rules should move from prose to mechanical checks?
- Which rules should be deleted entirely?

Do not skip this phase.

---

# 16. Long-task execution rules

For the work described by this charter:

1. A planning agent/subagent should first create durable contracts and artifacts.
2. Executor tasks should be split by **minimum necessary context**, not by arbitrary feature/module labels.
3. Build an explicit dependency graph before launching parallel work.
4. Run independent tasks in parallel when integration risk is low.
5. Keep dependent work serial or stacked.
6. Each executor must receive:
   - task goal;
   - relevant source files;
   - required invariants;
   - forbidden scope;
   - expected artifacts;
   - validation commands;
   - integration dependency.
7. Review agents should evaluate against both:
   - repository/workflow standards;
   - the originating task/decision contract.
8. Do not let executors rewrite planning/decision artifacts merely to make their implementation appear compliant.
9. After integration, re-evaluate the combined state rather than assuming individually passing branches compose correctly.

---

# 17. Questions that MUST be answered before broad coding

Before Phase 2 begins, answer all of the following:

1. What are the three most costly real failure modes in the current system?
2. Which existing Skills already solve them adequately?
3. Which DSH mechanisms solve DSH-specific rather than generic problems?
4. Which proposed rules belong in Skills versus mechanical gates?
5. Which artifacts must be canonical?
6. Which artifacts should be transient?
7. Which artifacts should automatically become stale, archived, or deleted?
8. Which information should exist only in Git history?
9. What is the minimum context a new agent needs to resume the project correctly?
10. Which current workflows are blocked because they were designed ahead of available capability?
11. Which current status models conflate orthogonal dimensions?
12. Which DSH mechanisms were later simplified or removed, and what warning does that provide?
13. If half of the proposed new mechanisms were deleted, which capabilities would actually be lost?
14. Can a common change be completed without generating unnecessary new permanent documents?
15. Can a research route be paused/rejected/revived without falsifying history?
16. Can the system distinguish “strong literature support” from “verified in this project”?
17. Can the system recover the current state after 20–50 changes without reading the entire repository?

---

# 18. Non-goals and guardrails

Do **not**:

- copy the DSH file tree mechanically;
- copy DSH TypeScript/Cordis-specific rules into generic Skills;
- create a Skill merely because DSH has one;
- create a universal mega-orchestrator;
- create a universal mega-status enum;
- create a permanent artifact for every intermediate thought;
- duplicate Git/PR/test state in custom ledgers without a clear need;
- assume every research route is a PR stack;
- treat literature as project verification;
- treat notebook saved output as current executable truth;
- design all future capabilities before proving one vertical slice;
- add governance without an explicit failure mode it addresses;
- preserve obsolete governance just because it once existed;
- declare a Skill successful without evals;
- declare a workflow complete when downstream capabilities are missing;
- silently rewrite previous durable decisions into their opposite;
- let current-state docs accumulate chronology;
- optimize for “looks comprehensive”.

---

# 19. Required deliverables

At the end of the full development program, the repository should contain:

## Investigation artifacts

- current-system map;
- DSH evidence map;
- DSH transferability crosswalk;
- gap analysis.

## Architecture artifacts

- target workflow architecture;
- canonical information model;
- decision/evidence/state model;
- Skill portfolio map;
- enforcement-layer map;
- long-task/multi-agent execution model.

## Implemented capabilities

Only those justified by evidence and validated by evals.

## Mechanical enforcement

Where appropriate:

- schemas;
- deterministic checkers;
- tests;
- CI;
- stale-reference checks;
- artifact/interface checks.

## Evals

- atomic;
- workflow;
- adversarial;
- longitudinal.

## Simplification report

A final pass documenting:

- what was removed;
- what was merged;
- what remained intentionally manual;
- what was deliberately not copied from DSH.

---

# 20. Acceptance criteria

The redesign is successful only if all of the following are true.

## Repository bootstrap

A new repository can reach a usable agent-development state without generating excessive governance machinery.

## Messy repository recovery

The system can reconstruct actual state, distinguish fact from stale intent, and identify a small number of high-value cleanup actions.

## Multi-route research

Several related routes can coexist without being flattened into one linear plan.

## Research uncertainty

Ideas, hypotheses, candidates, decisions, evidence strength, freshness, and implementation status remain distinguishable.

## Decision durability

Important decisions retain rationale, alternatives, evidence basis, and revisit conditions without turning the active corpus into a historical transcript.

## Multi-agent development

Long tasks can be split by context boundary, parallelized safely, and integrated with explicit dependency/evidence contracts.

## Verification

Completion claims are grounded in external evidence.

## Knowledge integrity

Each durable fact has one owner and stale duplication is detectable.

## Long-term maintainability

After many simulated changes, the active workflow corpus remains compact enough for a new agent to reconstruct state without reading everything.

## Simplicity

The final system contains no Skill, artifact type, schema, or orchestration layer that lacks a concrete responsibility and evidence-backed need.

---

# 21. Final instruction to the implementation agent

Treat this as a research-and-engineering problem, not a documentation-generation task.

First reconstruct reality.

Then study DSH historically.

Then extract transferable principles.

Then define invariants.

Then design the smallest coherent target architecture.

Then implement one vertical slice.

Then evaluate it.

Then expand.

Then simplify.

Do not optimize for completeness of the first design. Optimize for a workflow that can **learn from its own failures without becoming increasingly complicated every time it learns**.
