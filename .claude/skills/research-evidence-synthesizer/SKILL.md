---
name: research-evidence-synthesizer
description: Turn ALREADY-RETRIEVED evidence (papers/notes from the retrieval stack, extracted evidence units, or the literature-ingest store) into a DESIGN-DECISION-facing evidence structure — a claim–evidence matrix + method-transfer cards + E0–E5 evidence levels + explicit transfer assumptions + unresolved gaps, with direct / same-domain-indirect / cross-domain-analogy / project-inference channels kept separate. It never retrieves or searches, and it never upgrades paper/indirect evidence into a project-verified fact. Use to organize collected evidence to inform a research-software design decision. NOT for retrieving (lit-review / wos-research / deep-research / paper-fetch-skill), extracting evidence from one paper's full text (evidence-extraction), writing a literature-review narrative (literature-synthesis / review-writer), or recording the decision itself (uncertainty-and-decision-manager).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only until its Batch-2 evals pass)
generated_by_skill: manual authoring (Batch 2, skill #4; per 2026-08-05 scope-correction directive §7 Step 2.4)
source_commit: Master-cai/Research-Paper-Writing-Skills@77e7c2c (MIT); addyosmani/agent-skills@7829ffd (MIT)
source_documents:
  - references/research-paper-writing-skills/research-paper-writing/references/paper-review.md (MIT — claim|evidence|status, method-borrow)
  - references/agent-skills/skills/source-driven-development/SKILL.md (MIT — evidence-authority ladder -> E-levels)
  - docs/skill-development/system-architecture.md §3.1 (chain), §7 (E0-E5 + status vocab); conflict-matrix.md §44-46,§50
  - references/documentation-methodology/upstream-method-matrix.md §2.8
last_verified: 2026-08-05
-->

# Research Evidence Synthesizer

> **Experimental · manual/orchestrator-only · [ADAPT] thin, design-facing adapter.** It **consumes**
> already-retrieved evidence and re-projects it into the system's **decision vocabulary** (E0–E5 levels +
> transfer assumptions), then hands off to `uncertainty-and-decision-manager`. It **never retrieves/searches**
> and **never writes a literature-review narrative**.
> **Boundary vs the installed research-writing stack (important):** `literature-synthesis` / `review-writer`
> are **review-writing-facing** (claim ledger → argument map → review dossier → a written review). This skill
> is **design-decision-facing** (does method X *transfer* to our problem, and how strong is the evidence for
> the choice). If the goal is to write a review, route there. **OQ-4:** may later merge with
> `research-question-and-literature-planner`; keep the boundary sharp until decided (planner = before
> retrieval; synthesizer = after).
> **v0.1** adapts `claim|evidence|status` (paper-review, MIT) + the evidence-authority ladder →
> E0–E5 (source-driven-development, MIT); attributed in `upstream-method-matrix.md` §2.8.

## Purpose

Take collected evidence and produce a **design-facing evidence structure**: a **claim–evidence matrix**
(each candidate design claim ↔ its supporting/contradicting sources), **method-transfer cards** (can a method
established in domain/setting A be used for our problem B, and under what **assumptions**), each item tagged
with an **E0–E5 evidence level** and an **evidence channel** — **direct** (measured in *this* project),
**same-domain-indirect**, **cross-domain-analogy**, or **project-inference** — plus the **unresolved gaps**.
This is the "literature basis / evidence map" that feeds `uncertainty-and-decision-manager` and the architect
skills. It **organizes**, it does not retrieve and does not decide.

## Trigger conditions

Engage when:
- Someone has **already-retrieved evidence** (papers, extracted notes, a `literature-ingest` store) and needs
  it **organized to inform a design decision** — an evidence matrix, method-transfer cards, evidence levels,
  transfer assumptions, gaps — **or**
- a control flow (`numerical-research-software-design`) reaches the evidence step **after** the retrieval stack
  ran, and needs the evidence mapped for the decision register.

## Do-not-trigger conditions

**Rule of the research layer (conflict-matrix §50): never retrieve; delegate.**
- **Find / search for papers** → `lit-review` / `wos-research` / `deep-research` (or scope first via
  `research-question-and-literature-planner`). This skill consumes *retrieved* evidence only.
- **Fetch a specific known paper's full text** → `paper-fetch-skill` (this skill *may* call it to pull one
  known source while building a card, but "go get papers" is not its job).
- **Extract evidence from one paper's full text** into units → `evidence-extraction` (its upstream). This skill
  consumes those units; it does not read raw full texts to extract them.
- **Write a literature-review narrative / dossier** → `literature-synthesis` / `review-writer`. This skill
  produces a decision-facing matrix, not a review write-up.
- **Record the decision / assign DECIDED-CANDIDATE status** → `uncertainty-and-decision-manager`. This skill
  supplies the evidence; it does not own the decision.
- **Scope a search that hasn't run yet** → `research-question-and-literature-planner`.

## Inputs

- `evidence` — the retrieved material: extracted evidence units, paper notes, a `literature-ingest`
  Zotero/Obsidian store (read-only), or a bundle of sources. Nothing is searched for here.
- Optional: the **design decision / candidate methods** the evidence must inform (from the elicitor / decision
  register), the target problem's setting (so transfer can be judged).

## Workflow

1. **Normalize the evidence set.** List each source (handle + what it claims), read-only. If a specific known
   paper's full text is missing for a card, you may call `paper-fetch-skill` for *that* source — never a search.
2. **Claim–evidence matrix.** For each candidate design claim, gather the sources that **support** and
   **contradict** it. *(paper-review: `claim | evidence | status`.)* Empty support = a gap, not a pass.
3. **Assign evidence level + channel per link.** Map each source→claim link to **E0–E5**
   *(source-driven-development authority ladder)* and to a **channel**: `direct` (measured in this project) /
   `same-domain-indirect` / `cross-domain-analogy` / `project-inference`. Keep the channels **visually
   separate** — a cross-domain analogy must never sit in the same column as a direct measurement.
4. **Method-transfer cards.** For each method considered for adoption: origin setting → our setting; the
   **assumptions the transfer relies on** (what must hold for it to carry over); what is **evidenced** vs
   **assumed**; and the **E-level** the transfer claim can honestly reach. This is the explicit form of the
   leap DQE's HF-12D flags.
5. **Unresolved gaps.** Claims with no/weak support, contested claims, and transfer assumptions that are
   untested → a numbered gap list (each with what evidence would close it — a hand-off to the planner or an
   experiment).
6. **Assemble the evidence map** with a coverage note (sources used; what was assumed vs evidenced) and route
   the decisions to `uncertainty-and-decision-manager`.

## Evidence discipline (gates that keep this skill honest — constraint D.8)

- **Never upgrade evidence to project-fact.** Paper / same-domain / analogy evidence is **never** presented as
  a project-verified fact. Only `direct` (measured in this project) evidence can reach the higher E-levels; a
  transfer claim caps at the level its weakest assumption allows. This is the core rule.
- **Channels stay separate.** Direct vs indirect vs analogy vs inference are distinct columns/tags; a decision
  built on analogy must *look* like it is built on analogy.
- **Consume, never retrieve.** No searching. `paper-fetch-skill` for a single named source is the only fetch.
- **Assumptions are explicit.** Every method-transfer card names what must hold; an unstated transfer leap is a
  defect (the HF-12D failure).
- **Organize, don't decide.** Emit CANDIDATE-level evidence; the DECIDED/BASELINE status is the decision
  manager's, never asserted here.

## Quality gates (on this skill's own output)

- Every claim has a support/contradict row; every source→claim link has an **E-level + channel**.
- Every method-transfer card states its **assumptions** and the **E-level cap**; no cross-domain claim is
  presented as direct/fact.
- Unresolved gaps are listed with what would close each; nothing searched-for here.
- Front-matter traceability (HF-9); decisions handed to the register, not decided here.

## Outputs

- `evidence-map.md` — a **new** file (default `docs/research/evidence-map-<topic>-<date>.md`). Sections:
  Source inventory · Claim–evidence matrix (claim · support · contradict · E-level · channel) · Method-transfer
  cards (origin → our setting · assumptions · evidenced-vs-assumed · E-cap) · Unresolved gaps (+ what closes
  each) · Coverage note. Template: `references/templates/evidence-map.template.md`.

## Handoff rules

- To `uncertainty-and-decision-manager` (each candidate claim + its E-level/channel → the register; it assigns
  DECIDED/CANDIDATE/OPEN and records `proof_context`). Gaps → `research-question-and-literature-planner` (scope
  the follow-up search) or an experiment.
- Writing a review from this → `literature-synthesis` / `review-writer` (different lane).

## Failure modes

- **No retrieved evidence yet** → route to `research-question-and-literature-planner` (scope) → retrieval; do
  not search here.
- **Only cross-domain analogy exists** → say so; cap the E-level; make the transfer assumptions explicit — do
  not launder analogy into a direct claim.
- **Asked to also decide** → supply the evidence + levels, then route the decision to
  `uncertainty-and-decision-manager`.
- **Asked to write it up as a review** → route to `literature-synthesis` / `review-writer`.

## References to load

- `docs/skill-development/system-architecture.md` §7 (E0–E5 + status vocabulary), §3.1 (chain); `conflict-matrix.md` §44–46, §50.
- `references/research-paper-writing-skills/.../paper-review.md` + `references/agent-skills/skills/source-driven-development/SKILL.md` (MIT). See matrix §2.8.

## Scripts to run

- `evals/skills/harness/checkers/run_checks.py <evidence-map>` — front-matter + status vocabulary before handing off.
