# Conflict Matrix — Research-Software Documentation Skills System

<!--
generated_by_skill: (manual, Phase-1 governance authoring)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/skill-development/current-skills-audit.md
  - docs/skill-development/system-architecture.md
  - docs/研究软件文档Skills系统_设计与创建指南.md (§14.3)
status: DECIDED for Phase-1 pairs; §1 control-flow cluster now LIVE (Batch-3 skeletons, manual-only); PROJECTED for not-yet-built pairs (marked)
last_verified: 2026-08-05
-->

> **Purpose.** For every pair of skills that could plausibly co-trigger, state whether they may run together, who dominates, and the hand-off rule. A pair marked **DENY** with no resolution is a *release blocker* (acceptance §15.4).
> **Legend — Co-run:** `OK` = may run together · `SEQ` = sequential only (one hands to the other) · `DENY` = must never both activate for the same request · `COND` = conditional (rule stated).
> **Status of a row:** `LIVE` = both skills exist now (installed/reference); `PROJECTED` = at least one is a not-yet-built new skill (rule is a design target, re-verified when built).

---

## 1. Highest-risk cluster: the three control flows vs each other

These share adjacent surfaces ("messy files" / "messy docs" / "fuzzy algorithm"). **This cluster is the top release gate.**

| A | B | Co-run | Dominant | Hand-off rule | Row |
|---|---|:---:|---|---|---|
| `numerical-research-software-design` | `scientific-workspace-reconstruction` | DENY | routing decision | If a numerical idea lives inside a messy workspace, **reconstruction runs first** (recover facts), then hands the recovered state to the design flow. Never both at once. | LIVE¹ |
| `numerical-research-software-design` | `documentation-refactor` | DENY | routing decision | If the idea is buried in messy docs, **refactor/curate first** only if docs block understanding; otherwise design flow proceeds and refactor is a later handoff. One at a time. | LIVE¹ |
| `scientific-workspace-reconstruction` | `documentation-refactor` | SEQ | reconstruction | Files-and-code mess → reconstruction; if the *residue* is a doc corpus, reconstruction hands off to refactor after state is known. Doc-only input → refactor directly. | LIVE¹ |

**¹ Built 2026-08-05 (Batch 3, v0 skeletons) — all three are `experimental` + `disable-model-invocation: true` + manual/user-invoked-only, so auto co-trigger is currently impossible by construction. These DENY/SEQ rules are the design target enforced *before* any of them flips to `auto_trigger` (creation-roadmap §3 gate). Each flow's own `conflict/*.yaml` encodes the cluster cases.**

**Disambiguator (from `system-architecture.md` §5):** route by the **dominant artifact type** after a read-only forensic/state pass. When ambiguous, `goal-scope-and-workflow-elicitor` asks exactly **one** routing question; no flow launches until it resolves.

---

## 2. New research atoms vs the existing (installed) research stack — **the critical LIVE conflict**

This is where the environment differs most from the guide (audit §3, arch [ADAPT] A1). The new atoms must **defer**, not compete.

| A (new) | B (existing L3) | Co-run | Dominant | Hand-off rule | Row |
|---|---|:---:|---|---|---|
| `research-question-and-literature-planner` | `lit-review` | SEQ | planner (scoping) → `lit-review` (execution) | Planner sets scope/inclusion/exclusion/stop-criteria, then **invokes `lit-review`** to run the survey. Planner never retrieves. | PROJECTED |
| `research-question-and-literature-planner` | `wos-research` | SEQ | planner → `wos-research` | For WoS-specific iterative search, planner hands the seed query + stop criteria to `wos-research`. | PROJECTED |
| `research-question-and-literature-planner` | `deep-research` | COND | planner → `deep-research` | Only when the question needs multi-source web fan-out + adversarial verification. Planner must justify the heavier flow; otherwise prefer `lit-review`. | PROJECTED |
| `research-evidence-synthesizer` | `lit-review` / `wos-research` / `deep-research` | SEQ | retrieval skills → synthesizer | Synthesizer consumes their **output** (papers/notes) and produces the evidence matrix; it must **not** launch new searches. | PROJECTED |
| `research-evidence-synthesizer` | `paper-fetch-skill` | OK | synthesizer | Synthesizer may call `paper-fetch-skill` to pull a specific known paper's full text while building a card. | PROJECTED |
| `research-evidence-synthesizer` | `literature-ingest` | OK | synthesizer | Reads the Zotero/Obsidian store `literature-ingest` populated. Read-only for the synthesizer. | PROJECTED |
| `technical-primary-source-research` | `research` (matt) | COND | same lane | These are the **same lane** (official docs/standards/source/APIs). Only one should be active; if Matt's `research` is installed, `technical-primary-source-research` is a *narrowing rename*, not a co-runner. | LIVE(ref) |
| `technical-primary-source-research` | `lit-review` / `deep-research` | DENY-parallel | by source type | Primary-source (docs/APIs) vs academic-literature are **different lanes**; route by whether the question is about *software behavior* (primary-source) or *published research* (literature). Never both auto. | PROJECTED |

**Rule of the layer:** any new research atom's `SKILL.md` do-not-trigger list must name **all five** existing research skills (`lit-review`, `wos-research`, `deep-research`, `paper-fetch-skill`, plus `research`), and its workflow must *delegate* retrieval.

---

## 3. Batch-1 skills vs each other and vs existing skills (LIVE — enforced now)

The four Phase-1 skills are all `experimental` + manual/orchestrator-only, so **auto co-trigger is impossible by construction**. Rows below define orchestration order + scope so they compose cleanly.

| A | B | Co-run | Dominant | Hand-off / scope rule | Row |
|---|---|:---:|---|---|---|
| `project-state-reconstructor` | `goal-scope-and-workflow-elicitor` | SEQ | reconstructor | Recover facts **before** eliciting goals, so the interview builds on real state, not assumptions. | LIVE |
| `goal-scope-and-workflow-elicitor` | `grilling` (L3) | DENY-parallel | elicitor (in flows) | Both interview. In the control flows, elicitor owns automatic questioning; `grilling` stays a **manual** primitive. Never auto-parallel. | LIVE |
| `goal-scope-and-workflow-elicitor` | `domain-modeling` (L3) | OK | elicitor | Elicitor surfaces terms; hands confirmed **stable** terms to `domain-modeling`. Unstable ones go to the decision register instead. | LIVE |
| `uncertainty-and-decision-manager` | `domain-modeling` (L3) | COND | split by stability | `domain-modeling` owns **stable/decided** terms & relations; `uncertainty-and-decision-manager` owns **hypotheses/candidates/open**. A term graduates from the register to the glossary when it reaches `DECIDED`. Boundary must be explicit or they overwrite each other. | LIVE |
| `uncertainty-and-decision-manager` | `wayfinder` (ref) | OK | wayfinder (if used) | Both track decisions; `wayfinder`'s decision tickets are the *tracker* form, the register is the *inline* form. If `wayfinder` is installed, the register feeds its tickets. | LIVE(ref) |
| `documentation-quality-evaluator` | every other skill | OK (as gate) | evaluator | Runs **read-only** at the end of any chain; produces a report, never edits. No conflict by design. | LIVE |
| `documentation-quality-evaluator` | `code-review` (L3) | OK | different objects | `code-review` judges **code diffs**; the evaluator judges **documents**. Complementary; may both run. | LIVE |
| `project-state-reconstructor` | `workspace-forensics-and-inventory` | SEQ | forensics → reconstructor | Forensics inventories raw artifacts (read-only); reconstructor interprets them into a state report. In Phase 1 (forensics not built), reconstructor does a bounded inventory itself. | PROJECTED |

---

## 4. Existing-skill scope conflicts carried from the audit (LIVE — enforced via registry limits)

| A | B | Co-run | Dominant | Rule | Row |
|---|---|:---:|---|---|---|
| `code-review` | `scientific-validity-review` (new) | OK | separate axes | Keep scientific checks (math/units/stability/convergence/RNG/reference-solutions/reproducibility) **out** of `code-review`; run as a distinct third axis. | PROJECTED |
| `codebase-design` | `scientific-software-architect` (new) | SEQ | architect | `codebase-design` is the **internal-shape** lens only; overall architecture (C4, external API, sci terminology) belongs to the architect, which may *pull in* codebase-design vocabulary. | PROJECTED |
| `prototype` | `scientific-prototype-experiment` (new, SPLIT) | COND | by question type | Numerical/convergence/noise/ill-conditioning question → science variant (emits GO/MODIFY/STOP/NEED-MORE-EVIDENCE). App/UI/state question → `prototype`. Router picks one. | PROJECTED |
| `research` (matt) | `lit-review` | DENY-parallel | by source type | Narrow `research` so it does **not** fire on academic-literature tasks (owned by `lit-review`/`wos-research`). This is the one **immediate live** narrowing action. | LIVE |
| `domain-modeling` | `uncertainty-and-decision-manager` (new) | COND | split by stability | (Duplicate of §3 for visibility) stable→glossary, unstable→register. | LIVE |
| `improve-codebase-architecture` (ref) | `scientific-workspace-reconstruction` (new) | SEQ | reconstruction | Refactor only **after** forensics+state+goals. Enforced by the workspace chain ordering. | PROJECTED |
| `handoff` (ref) | `living-design-maintainer` / status docs | DENY-substitution | canonical docs | `handoff` is transient session compression; it must **not** stand in for `current-status.md`/roadmap/ADR/experiment registry/architecture. | LIVE(ref) |

---

## 5. Release-gate summary

| Gate | Condition | Current state |
|---|---|---|
| G1 | No `DENY` control-flow pair may auto-trigger both flows. | **Met by construction** — all three L1 flows are `disable-model-invocation: true` until conflict evals pass. |
| G2 | Every new research atom defers retrieval to the L3 stack (do-not-trigger names all five). | Design rule set; enforced when those atoms are built (Batch 3). |
| G3 | `research` (matt) narrowed so it doesn't fire on literature tasks. | **Action item, LIVE** — pending user approval to modify the installed skill (constraint: no modify without notice). Tracked as OQ in architecture. |
| G4 | Batch-1 four skills cannot auto co-trigger. | **Met by construction** (all manual/orchestrator-only). |
| G5 | `domain-modeling` ↔ `uncertainty-and-decision-manager` boundary written into both. | To be encoded in the `uncertainty-and-decision-manager` SKILL.md (Batch 1) + noted for `domain-modeling` limits. |

**No unresolved high-risk conflict remains for Phase-1 activation**, because Phase-1 skills do not auto-trigger. The `PROJECTED` rows convert to `LIVE` gates as their skills are built and must pass the conflict eval set (`evals/skills/conflict/`) before any `auto_trigger: true` flip.
