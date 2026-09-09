---
name: research-question-and-literature-planner
description: A THIN scoping front-end for literature work — turn an open/fuzzy research question into a concrete, reviewable SEARCH PLAN (refined question(s), scope, inclusion/exclusion criteria, stop criteria, evidence/quality standard, expected evidence types), then ROUTE execution to the existing retrieval skills. It never retrieves, never reads papers, and never synthesizes findings. Use to plan/scope a literature search before running it. NOT for actually running a search or review (lit-review / wos-research / deep-research), fetching a known paper (paper-fetch-skill), looking up technical primary sources / software behavior (research), or organizing already-retrieved evidence (research-evidence-synthesizer).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only until its Batch-2 evals pass)
generated_by_skill: manual authoring (Batch 2, skill #3; per 2026-08-05 scope-correction directive §7 Step 2.3)
source_commit: addyosmani/agent-skills@7829ffd (MIT); mattpocock/skills@snapshot(v1.2.0)
source_documents:
  - references/agent-skills/skills/spec-driven-development/SKILL.md (MIT — testable-criteria + stop conditions, method-borrow)
  - references/agent-skills/skills/interview-me/SKILL.md (MIT — sufficiency/stop, method-borrow)
  - docs/skill-development/system-architecture.md §3.1 (chain), §4 research-lane rule; conflict-matrix.md §41-43,§50
  - references/documentation-methodology/upstream-method-matrix.md §2.7
last_verified: 2026-08-05
-->

# Research Question and Literature Planner

> **Experimental · manual/orchestrator-only · [ADAPT] thin adapter.** It produces a **search plan** and then
> **hands off** to the installed retrieval stack (`lit-review` / `wos-research` / `deep-research` /
> `paper-fetch-skill`). It **never retrieves, reads papers, or synthesizes** — those are owned skills.
> **v0.1**'s whole value is a *reviewable scoping artifact* (scope, inclusion/exclusion, stop criteria,
> evidence standard) produced **before** committing to retrieval, plus a justified route. Methods
> (testable-criteria, sufficiency-stop) adapted from `spec-driven-development` + `interview-me` (MIT),
> attributed in `upstream-method-matrix.md` §2.7.
> **Open question OQ-4:** this skill and `research-evidence-synthesizer` may later merge into one adapter —
> keep the boundary sharp until that is decided (planner = *before* retrieval; synthesizer = *after*).

## Purpose

Turn an open/fuzzy research question into a **literature search plan**: refined answerable question(s),
explicit **scope** (in/out), **inclusion/exclusion criteria**, **stop criteria** (when the search is "enough"),
an **evidence/quality standard** (what counts as strong vs weak evidence), and the **expected evidence types**
— then **route** to the right retrieval skill. The plan is a decision-quality artifact the team can review and
the downstream retrieval skill can execute against. This skill **delegates all retrieval**.

## Trigger conditions

Engage when:
- Someone has an **open research question** and needs to **scope / plan** a literature search *before* running
  it ("help me plan a review of X", "what's the scope and stop criteria for surveying Y", "turn this question
  into a search protocol"), **or**
- a control flow (`numerical-research-software-design`) reaches the literature step and needs the **scoping
  artifact + route** before invoking the L3 retrieval stack.

## Do-not-trigger conditions

**Rule of the research layer (conflict-matrix §50): delegate retrieval; name all five existing research skills.**
- **Actually run the survey / review** → `lit-review` (the review execution control).
- **Iterative Web-of-Science search + relevance feedback** → `wos-research`.
- **Multi-source web fan-out + adversarial verification** → `deep-research` (heavier; justify before routing here).
- **Fetch / summarize a KNOWN specific paper** → `paper-fetch-skill`.
- **Technical primary sources / software behavior / API/docs/standards** (not academic literature) → `research`.
- **Organize already-retrieved evidence** into a matrix/levels → `research-evidence-synthesizer` (downstream).
- **No research question yet** (a vague topic with no decision behind it) → `goal-scope-and-workflow-elicitor`.

## Inputs

- `question` — the open research question (or the decision it must inform).
- Optional: the originating goal/decision (from the elicitor / decision register), domain constraints, a time
  budget, known seed papers.

## Workflow

1. **Frame the question for decision.** Restate the open question as one or more **answerable** questions,
   tied to the **decision** they inform (why we are searching). *(spec-driven-development: testable criteria.)*
   If the question is really a design decision with no literature need, say so and route back to the elicitor.
2. **Scope.** State what is **in** and **out** (domains, sub-topics, time window, venues, languages). A scope
   that is "everything" is a defect — bound it.
3. **Inclusion / exclusion criteria.** Concrete, checkable rules for what counts (study type, relevance,
   recency, method match, quality floor).
4. **Stop criteria.** When is the search "enough"? *(interview-me: sufficiency-stop.)* e.g. saturation (no new
   methods in N sources), a fixed source budget, or coverage of the top venues — pick one and make it explicit.
5. **Evidence / quality standard.** What counts as **strong** vs **weak** evidence for *this* question, and
   which of the system's **E0–E5** levels a source can support. Flag up front where the question will only ever
   get **cross-domain / analogy** evidence (a transfer question) — this pre-warns the synthesizer's HF-12D lens.
6. **Route (delegate retrieval).** Pick the retrieval skill and justify it: default `lit-review`; `wos-research`
   for WoS iterative; `deep-research` only for multi-source web fan-out (justify the heavier flow);
   `paper-fetch-skill` for known seeds. Hand over the seed query + scope + stop criteria. **You stop here — you
   do not run the search.**

## Adapter discipline (gates that keep this skill thin)

- **Plan, never retrieve.** No searching, no reading papers, no summarizing sources, no synthesizing findings.
  The output is a plan + a route; the retrieval skill does the work.
- **Name the route.** Every plan ends with a specific downstream skill + why it (not the others) fits.
- **Bounded, checkable scope.** Inclusion/exclusion and stop criteria must be concrete enough for someone else
  to execute and know when to stop.
- **No project-fact upgrade.** The plan describes what *might* be found; it never asserts a finding as fact
  (that is the synthesizer's + decision-manager's job, under E-levels).

## Quality gates (on this skill's own output)

- The plan has: refined question(s) tied to a decision, in/out scope, inclusion/exclusion, an explicit stop
  criterion, an evidence standard mapped to E0–E5, and a **named downstream retrieval skill** with justification.
- Contains **no retrieved results** (no paper list, no summaries) — if it does, the skill overstepped.
- Front-matter traceability present (HF-9); the transfer/analogy warning is raised when the question is cross-domain.

## Outputs

- `search-plan.md` — a **new** file (default `docs/research/search-plan-<topic>-<date>.md`). Sections:
  Question(s) + decision · Scope (in/out) · Inclusion/exclusion · Stop criteria · Evidence standard (→ E0–E5) ·
  Expected evidence types + transfer warning · **Route** (chosen skill + why). Template:
  `references/templates/search-plan.template.md`.
- A one-line route for the caller: `ROUTE retrieval=<lit-review|wos-research|deep-research|paper-fetch-skill> because=<…>`.

## Handoff rules

- Hand the plan + seed query to the chosen retrieval skill (`lit-review` by default). Its output (papers/notes)
  then goes to `research-evidence-synthesizer`, not back here.
- Decision context / open questions → `uncertainty-and-decision-manager`.

## Failure modes

- **Vague topic, no decision** → route to `goal-scope-and-workflow-elicitor`; don't manufacture a search plan.
- **User actually wants the results now** → produce the plan, then route to the retrieval skill; do not run it here.
- **Transfer question** (method from domain A → problem B) → mark that only cross-domain/analogy evidence exists;
  set the evidence standard accordingly (this becomes the synthesizer's transfer-assumption input).

## References to load

- `docs/skill-development/system-architecture.md` §3.1 (chain) + §4 (research-lane priority); `conflict-matrix.md` §41–43, §50.
- `references/agent-skills/skills/spec-driven-development/SKILL.md` + `interview-me/SKILL.md` (MIT). See matrix §2.7.

## Scripts to run

- `evals/skills/harness/checkers/run_checks.py <search-plan>` — front-matter + status vocabulary before handing off.
