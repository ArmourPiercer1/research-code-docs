<!--
generated_by_skill: (manual, Batch-2 light eval round per 2026-08-05 directive §8)
skill_version: Batch 2 — workspace-forensics-and-inventory 0.1.0 · document-information-architect 0.1.0 · research-question-and-literature-planner 0.1.0 · research-evidence-synthesizer 0.1.0
source_commit: 975e930 (workspace HEAD at eval time; internal report)
source_documents:
  - .claude/skills/{workspace-forensics-and-inventory,document-information-architect,research-question-and-literature-planner,research-evidence-synthesizer}/SKILL.md
  - evals/skills/{trigger,conflict,reader-tests}/<each-skill>.yaml
  - evals/skills/results/{workspace-forensics-and-inventory,document-information-architect,research-question-and-literature-planner,research-evidence-synthesizer}/shadow/*.md
  - docs/third-party-suggestions/Research-Code-Docs当前进展_阻塞项与下一阶段开发计划.md §7-§8 (build order + light test spec)
status: DECIDED (all four Batch-2 skills PASSED their light round; all stay experimental + manual-only)
last_verified: 2026-08-05
-->

# Batch 2 — Light Eval Round: Detailed Test Report (4 skills)

> **Headline.** All **four** Batch-2 skills were built and passed their light first round:
> **trigger 32/32** (8/8 each), **4 real read-only shadow runs** (targets verified untouched), **4 no-context
> reader tests** (each with its lane-specific discipline check green), and a **no-skill baseline** per skill
> showing a clear value-add. Every skill stays **experimental + `disable-model-invocation: true`**
> (manual/orchestrator-only) — the light round validates *advisory manual use*, not auto-trigger. Tested via
> injected-prompt sub-agents; **nothing installed or pushed**; no HF thresholds or the DQE skill were touched.

## 0. Scope & method

Per the 2026-08-05 scope-correction directive (§7 build order, §8 light test spec), Batch 2 is decoupled from
"DQE becomes a universal terminal gate" and each new skill gets a **deliberately light** first round — **not**
DQE's heavy corpus:

```
3 should-trigger · 3 should-not · 2 boundary/conflict · 1 real shadow run · 1 no-context reader test · 1 no-skill comparison
```

Eval posture = **DQE-advisory + an independent reviewer** (here: fresh injected-prompt sub-agents in isolated
contexts), not a large admission matrix. Regression cases are added only after a **real** failure appears.

**Isolation.** Every eval ran in a fresh `general-purpose` sub-agent injected with only the skill under test
(and, for shadow runs, its template + the target). Trigger/reader agents were told to read **only** the one
SKILL.md / artifact and no other governance file, so routing and reader judgments reflect the skill text alone.

**The four skills (build order — lowest-risk / most-reused first):**

| # | skill | class | what it produces | key discipline |
|---|---|---|---|---|
| 1 | `workspace-forensics-and-inventory` | audit (read-only) | inventory report | candidate+signal; **never claims anything runs** |
| 2 | `document-information-architect` | design | artifact map | a **plan** (no rewrite/move); one canonical home per type (HF-13/14b cure) |
| 3 | `research-question-and-literature-planner` | research-adapter | search plan | thin scope+route; **never retrieves** |
| 4 | `research-evidence-synthesizer` | research-adapter | evidence map | design-facing; **never upgrades analogy→project-fact** (D.8) |

## 1. Results at a glance

| skill | trigger | shadow (real target) | read-only proven | reader test | no-skill compare |
|---|---|---|---|---|---|
| forensics | **8/8** | `tests/corpus/` | ✅ git porcelain clean | READER_CAN_ACT=YES / OVERCLAIM=NO | ✅ adds hygiene+handoff |
| IA | **8/8** | eoopt hybrid roadmap | ✅ untouched | DESIGN_ACTIONABLE=YES / LANE_VIOLATION=NO / DUPLICATION=NO | ✅ (baseline drifts to execute) |
| RQLP | **8/8** | manifold-transfer question | ✅ (no retrieval) | SCOPE_ACTIONABLE=YES / OVERREACH=NO | ✅ (baseline overreached) |
| RES | **8/8** | SYNTHETIC evidence bundle | ✅ fixture untouched | SYNTHESIS_ACTIONABLE=YES / FACT_UPGRADE=NO | ✅ (baseline lacks structure) |

**Trigger total: 32/32.** All 4 reader-test discipline flags green. All 4 shadow targets verified untouched
by `git status --porcelain`.

## 2. Per-skill detail

### 2.1 `workspace-forensics-and-inventory` v0.1.0 (read-only inventory)
*(Built + reported first — full write-up in `reports/batch2-workspace-forensics-eval-2026-08-05.md`; summarized here.)*
- **Trigger 8/8** — 3 ENGAGE; routed code-review, diagnosing-bugs, document-information-architect (design-not-inventory), and the two identity boundaries **project-state-reconstructor** (what-runs) + **workspace-migration-planner** (move/delete).
- **Shadow** — inventoried `tests/corpus/` read-only; Project Map + coverage; GENERATED-labeled `blind-runs/`; **5 orphan candidates each with the cited search** (incl. a real plan/case coverage gap `GN-EVIDENCE-BARE-CLAIM-001`); PSR handoff; **no over-claim** that anything runs. `git status` proved the tree untouched.
- **Reader** — actionable inventory AND the reader could **not** conclude anything runs.
- **Value** — baseline narrated + asserted ("provenance is rigorous"); skill added candidate+signal tagging, GENERATED hygiene, orphan-with-search, trust tiers, coverage note, PSR handoff.

### 2.2 `document-information-architect` v0.1.0 (design the split — the HF-13 cure)
- **Trigger 8/8** — 3 ENGAGE (hybrid split / corpus canonical-owner / HF-13 structural fix); routed **documentation-quality-evaluator** (grade≠design), **technical-document-rewriter** (rewrite≠design), **content-canonicalization-and-migration** (move≠design), **domain-modeling** (terminology≠doc-structure), **project-state-reconstructor** (facts-first).
- **Shadow** (target: the real eoopt hybrid roadmap `tests/最终目标设计与开发路线图.md`, the canonical HF-13 case) — identified **11 doc-roles** with divergent update-frequencies, assigned **one canonical home per information-type**, a **complete split plan** (every section assigned or raised as an open decision), **7 open decisions** left for a human, and marked fact-dependent assignments **provisional (needs PSR)**. Volatile state (test counts, code snapshot, session residue) is **stripped to a pointer, never copied into a stable doc** — the HF-14b cure. It **did not rewrite prose or move files** — it stayed a plan handed to migration→rewriter→DQE.
- **Reader** — `DESIGN_ACTIONABLE=YES` (roles / target doc-set / per-type home all listable); `LANE_VIOLATION=NO` (a plan, not a rewrite/move); `DUPLICATION=NO` (the one spec-home ambiguity raised as **Open decision #2**, not silently duplicated).
- **Value vs no-skill** — the baseline was a competent narrative but **drifted out of lane**: it prescribed an "order of operations" that *creates/moves files* and *rewrites in present tense*, and it made **silent decisions** ("what to drop"). The skill's output is a structured design plan with `provisional (needs PSR)` flags and *open decisions* instead of silent choices — usable by migration/rewriter without smuggling in unverified interpretation.

### 2.3 `research-question-and-literature-planner` v0.1.0 (thin scope + route; never retrieves)
- **Trigger 8/8** — 3 ENGAGE (scope a transfer question / question→protocol+route / define scope+stop); routed **lit-review** (run the survey), **paper-fetch-skill** (known paper), **research** (software/API behavior≠literature), and the two boundaries **research-evidence-synthesizer** (already-retrieved evidence — the OQ-4 line) + **wos-research** (WoS iterative execution). The do-not-trigger names all five research skills (§50).
- **Shadow** (a cross-domain transfer question) — produced a **scope-and-route artifact only**: 3 decision-tied questions, in/out scope, a 6-row inclusion/exclusion table, a **saturation stop criterion + a source-budget backstop**, an evidence standard mapped to **E0–E5**, a prominent **cross-domain transfer warning** (HF-12D lens), and a **justified route to `lit-review`** (contrasted against the other four). Seed anchors are explicitly labeled *"to confirm/expand — not asserted findings."* **No retrieval, no summaries, no synthesis.**
- **Reader** — `SCOPE_ACTIONABLE=YES`; `OVERREACH=NO` (confirmed no retrieved findings; seeds are labeled candidates; transfer limit flagged).
- **Value vs no-skill — the batch's clearest demonstration.** The no-skill baseline **overreached badly**: it produced **named seed papers as findings** (Absil–Mahony–Sepulchre 2008, Boumal 2023, Rheinboldt 1996, …), a **"pre-registered hypothesis about what the literature will show,"** and offered to *"execute the first pass rather than just plan it."* That is exactly the thin-adapter boundary violated — planning conflated with doing (retrieval + synthesis). The skilled run stayed a plan and delegated retrieval. This is the sharpest evidence that the adapter earns its place over an unstructured model.

### 2.4 `research-evidence-synthesizer` v0.1.0 (design-facing evidence; never upgrades analogy→fact)
- **Trigger 8/8** — 3 ENGAGE (matrix+levels / transfer-cards+assumptions / channel separation for the register); routed **lit-review** (find papers), **review-writer** (write a narrative — the boundary vs the *installed* review-writing stack), **research-question-and-literature-planner** (scope-before-retrieval), and the two boundaries **evidence-extraction** (single-paper full-text→units) + **uncertainty-and-decision-manager** (record the decision/status). *(res-not-02 routed to `review-writer` rather than `literature-synthesis` — an even more precise target in the same review-writing lane; accepted.)*
- **Shadow** (a **SYNTHETIC** evidence bundle — 4 clearly-fictional sources, so no fabricated project history) — organized it into a claim–evidence matrix with **E-level + channel per link**, **kept the four channels separate**, and held constraint **D.8**: the cross-domain analogy claims are **capped at E2**, the enabling LICQ/manifold assumption is flagged **E0 (assumed *and* contradicted by the one same-domain source)**, and the single weak in-project trial is **isolated at E1** so it can't be laundered into the transfer rows. The method-transfer card states its assumptions + the E-cap; 5 numbered gaps each carry what would close them; decisions route to the register, gaps to the planner. **Nothing retrieved; nothing upgraded to a project fact.**
- **Reader** — `SYNTHESIS_ACTIONABLE=YES`; `FACT_UPGRADE=NO` (analogy capped, transfer bounded by weakest assumption, channels separate, no retrieval).
- **Value vs no-skill** — the baseline was disciplined *narratively* (it respected the synthetic label and framed the LICQ crux well) but produced **no E-level tags, no channel column, no transfer card with an E-cap, no numbered gaps, no register handoff**. The skill adds exactly the decision-register-facing structure + the E-level/channel discipline that lets `uncertainty-and-decision-manager` consume it without over-crediting analogy.

## 3. Cross-cutting observations

- **Each skill's discipline is the inverse of the failure it guards.** Forensics must *not* claim things run;
  IA must *not* rewrite/move; RQLP must *not* retrieve; RES must *not* upgrade analogy to fact. Every reader
  test checked exactly that inverse, and every one held.
- **The two research adapters stayed thin.** Both RQLP and RES *delegated* (RQLP→lit-review; RES→register +
  planner) rather than doing retrieval/decision themselves, and both routed correctly at the sharp boundaries
  against the **installed** stack (`lit-review`, `wos-research`, `paper-fetch-skill`, `evidence-extraction`,
  `literature-synthesis`/`review-writer`). This is the "thin adapter, not reimplementation" requirement met.
- **Baselines failed differently, and informatively.** IA's baseline over-*executed*; RQLP's over-*retrieved*;
  RES's under-*structured*. The value-add is not "the skill is smarter" but "the skill holds a boundary the
  unstructured model does not."

## 4. Honest scope & deferrals (not hidden)

- **Light round only.** Each skill has **one** shadow run in **one** mode. Not yet exercised:
  - forensics **document-corpus mode** (only workspace mode was shadow-run);
  - IA on a **multi-doc corpus** (only the single hybrid doc);
  - RQLP/RES **chained to a real retrieval** (RES ran on a *synthetic* bundle by design — no real lit-review
    output exists yet; a real end-to-end RQLP→lit-review→RES chain is the natural next validation);
  - a **second** real target per skill.
  Add these — and any regression case — when a real need or failure appears (directive §8), not preemptively.
- **OQ-4 stays open.** RQLP and RES are deliberately kept as two thin adapters with a sharp before/after-retrieval
  boundary; whether they should merge into one `research-evidence-adapter` is revisited after Batch 3 (per
  architecture §13 / conflict-matrix OQ-4). Nothing here forces the decision.
- **All four stay manual-only.** `disable-model-invocation: true` + `experimental`. Auto-trigger remains gated
  on each skill's own trigger/conflict evals + real shadow runs + human admission (directive §5.3).
- **Nothing installed or pushed.** DQE (v0.4.1 advisory freeze) and the four Batch-1 skills were untouched this
  round; snapshots + canary evidence remain preserved.

## 5. Verdict

Batch 2 is **built and light-validated**: four new skills, each triggering correctly, respecting its
read-only/scope/no-retrieval/no-fact-upgrade discipline, producing a usable artifact on a real target, and
beating a no-skill baseline on the dimension that matters (holding its boundary). The batch advances the
system from "1 evaluator + 3 fact/scope skills" to a working **inventory → architecture → literature-scope →
evidence-map** chain, all advisory and manual-only. Evidence under
`evals/skills/results/{forensics,document-information-architect,research-question-and-literature-planner,research-evidence-synthesizer}/`.
