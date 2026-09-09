---
name: goal-scope-and-workflow-elicitor
description: Structured interview that pins down a user's real goals, scope boundaries, non-goals, and intended workflow before design work begins — asking only genuine decisions (looking up facts itself), one question at a time with a recommended answer, stopping at the current decidable boundary and classifying every unresolved branch. Use when a control flow needs goals/scope clarified or a request is ambiguous across multiple paths. NOT for simple well-specified tasks, and NOT the manual grilling primitive.
disable-model-invocation: true
---

<!--
skill_version: 0.2.0
status: experimental (orchestrator-only; no auto-trigger until evals pass)
generated_by_skill: manual authoring; v0.2 upgraded from real references
source_commit: mattpocock/skills@snapshot(v1.2.0); addyosmani/agent-skills@7829ffd (MIT)
source_documents:
  - references/agent-skills/skills/interview-me/SKILL.md (MIT)
  - references/agent-skills/skills/idea-refine/SKILL.md (MIT)
  - references/agent-skills/skills/spec-driven-development/SKILL.md (MIT)
  - references/mattpocock-skills/skills/productivity/grilling/SKILL.md (MIT)
  - docs/研究软件文档Skills系统_设计与创建指南.md §6.3
  - references/documentation-methodology/upstream-method-matrix.md §2.3 (per-method attribution)
last_verified: 2026-07-30T09:47:06Z
-->

# Goal, Scope & Workflow Elicitor

> **Experimental · orchestrator-only.** Owns *automatic* questioning inside the control flows. The manual, user-invoked interview is `grilling` — this skill must never auto-run in parallel with it.
> **v0.2** integrates real elicitation methods (interview-me, idea-refine, spec-driven-development — all MIT). Every adopted rule is attributed in `upstream-method-matrix.md` §2.3; the spec/task/ideation machinery of those skills is deliberately left downstream.

## Purpose

Convert a fuzzy or multi-path request into a **goal/scope note** and an **open-decision list**, by interviewing the user efficiently: look up every fact yourself, put only real **decisions** to the user, one at a time, each with a recommended answer — and **stop as soon as understanding is shared**, not after every question is closed.

## Trigger conditions

Engage when:
- A control flow needs goals/scope/non-goals/workflow clarified before it can proceed, **or**
- The request is **genuinely ambiguous** across multiple valid directions and the ambiguity blocks progress, **or**
- The user explicitly asks to "figure out what I actually want / scope this."

## Do-not-trigger conditions

- The task is **simple and well-specified** → just do it; interviewing would be noise. (Primary should-not; when invoked on such input, **decline and route** to the doer.) The confidence check in Workflow §2 makes this call explicit.
- The goal is **already clear** from the request + state report.
- The answer is a **fact that can be looked up** (filesystem, tests, docs) → look it up, don't ask.
- The user wants a **manual, relentless grilling** → that's `grilling` (a separate, user-invoked primitive).
- **Stable domain terminology** needs defining → `domain-modeling`.

## Inputs

- The user's initial ask.
- The **state report** from `project-state-reconstructor` (read this first — facts before questions).

## Workflow

1. **Read the state report first.** Never ask what the facts already answer.
2. **State a one-line goal hypothesis + confidence (0–100%).** Write your current best read of the goal in one sentence with an honest confidence. *(interview-me)* If confidence is already high and you can name no missing piece → this **is** the too-simple signal: decline/route per Do-not-trigger. If confidence < ~70%, append **what specifically is missing** (who / why-now / success / binding constraint); the gap list seeds the questions.
3. **Present a correctable brief before asking.** *(spec-driven-development)* List, as a "correct me or I proceed with these" bullet list: the facts you looked up **and** the assumptions you're riding on them. One bulk correction replaces a string of questions. Only decisions the user changes or can't rule on become questions.
4. **Ask the frontier, one question at a time**, each with a **recommended answer**; wait before the next. *(grilling)* Order questions by the design tree's frontier; never dump them all at once.
5. **Look up, don't ask, for facts.** Only genuine decisions go to the user. When an answer is a **buzzword or convention** ("modern", "scalable", "robust", "best practice") rather than a concrete outcome, probe once — *"if you didn't have to justify this to anyone, what would you actually want?"* — before recording it as the goal. *(interview-me)* When the goal or its success is vague ("faster", "cleaner"), propose 1–2 **concrete, checkable success conditions** and ask "are these the right targets?"; record the confirmed criteria. Stop at the criterion — do not draft a spec (that is `to-spec`/`algorithm-technical-spec-author`, downstream).
6. **Stop — two independent tests, whichever fires first:**
   - **(a) decidable-boundary** — remaining questions depend on research / experiments / facts not yet available; stop and classify them.
   - **(b) sufficiency** — before asking the next question, check: *can you already predict the user's answer to it and the next two?* If yes, understanding is shared → stop and restate. *(interview-me)*
7. **Classify every unresolved branch** as one of: `repo-verifiable` · `needs-literature` · `needs-prototype` · `user-preference` · `deferred`.
8. **Restate in fixed fields, in the user's own words**, and confirm: **Outcome / User / Why-now / Success / Constraint / Non-goals**. *(interview-me)* "Out of scope" is mandatory — half of misalignment is silent disagreement about what is *not* being built. Confirm by an **explicit yes**: "sounds good"/silence is not a yes, and "whatever you think" is a delegation → re-ask as two concrete options, don't record it as decided.
9. **Emit** the goal/scope note + open-decision list.

**Bounds.** *(idea-refine)* Floor: don't emit the note until who-it's-for, success, the binding constraint, and non-goals are each answered or classified. Ceiling: if the genuine-decision frontier exceeds ~5–6, you are over-decomposing — freeze the rest as `deferred`.

## Quality gates

- Opened with an explicit **goal hypothesis + confidence**; every < 70% confidence named the missing piece.
- Presented a **correctable brief** (looked-up facts + assumptions) before questioning.
- **No duplicate questions**; no question whose answer is a known/lookable fact.
- **Did not interview a simple task** — on out-of-scope simple input, it declined/routed.
- Every question carried a recommended answer; every unresolved branch is classified (§7).
- Restate has **explicit Non-goals** and was confirmed by an explicit yes (or, no live user, marked `CANDIDATE`).
- Goal/scope note is readable with **no chat context** — else HF-8.

## Outputs

- `goal-scope-note.md` — fixed fields (Outcome / User / Why-now / Success / Constraint / **Non-goals**) + intended dev–test–experiment workflow + confirmed constraints. Template: `references/templates/goal-scope-note.template.md`.
- `open-decision-list.md` — unresolved branches, each classified + recommended next action.

## Handoff rules

- Open decisions → `uncertainty-and-decision-manager` (it tags status + evidence).
- `needs-literature` branches → `research-question-and-literature-planner` (later) → `lit-review`/`wos-research`.
- `needs-prototype` branches → `scientific-prototype-experiment` (later) / `prototype`.
- Confirmed **stable** terms → `domain-modeling`; unstable ones stay in the open-decision list.

## Failure modes

- **User unavailable** → best-effort note marking every assumed answer as `CANDIDATE`, with the exact questions to confirm later. Never present assumptions as decided. (Overrides the explicit-yes gate — mark, don't block.)
- **Cannot converge** — after ~3 rounds without the goal getting sharper, stop and surface "something foundational is missing — want to step back?" rather than grinding. *(interview-me floor)*
- **Scope keeps expanding** → freeze the current frontier, record the rest as `deferred`.

## References to load

- `references/agent-skills/skills/interview-me/SKILL.md` (MIT — hypothesis+confidence, sufficiency stop, buzzword probe, fixed-field restate). Method-borrowed; see matrix §2.3.
- `references/mattpocock-skills/skills/productivity/grilling/SKILL.md` (MIT — one-at-a-time, recommend-an-answer, look-up-facts).
- `docs/skill-development/system-architecture.md` §7 (status vocabulary for the open-decision list).

## Scripts to run

- `evals/skills/harness/checkers/run_checks.py <goal-scope-note>` — front-matter + no-empty-section check before handoff.
