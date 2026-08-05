# Creation Roadmap — Research-Software Documentation Skills System

<!--
generated_by_skill: (manual, Phase-1 governance authoring)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/研究软件文档Skills系统_设计与创建指南.md (§10, §16)
  - docs/skill-development/system-architecture.md
  - docs/skill-development/current-skills-audit.md
status: DECIDED for Batch 1; Batch 2 IN PROGRESS (decoupled from DQE terminal-gate promotion, 2026-08-05); PLANNED for Batches 3-5
last_verified: 2026-08-05
-->

> **Principle (guide §17).** The quality bar is not "all files generated" but: recover facts before designing; write unknowns as unknown; turn research questions into surveys/experiments, not fake plans; keep stable design / dynamic state / paper evidence / session notes separate; recognize simple tasks; improve via evals, not vibes.
> **Gate rule (constraint D.3 / prompt E).** No new skill auto-triggers until it passes trigger+conflict evals. `documentation-quality-evaluator` had to pass its own **basic** evals before Batch 2 began — it grades everything after it. It did (trigger 28/28 + discriminative e2e).
> **Scope-correction (2026-08-05).** Batch 2 is now **DECOUPLED** from "DQE becomes a *universal automatic terminal gate*." DQE v0.4.1 is frozen as an **advisory / profile-scoped** evaluator — enough to assist Batch-2 development alongside an independent/human reviewer. The heavier promotion bar (full golden suite, Phase E 3-arm admission matrix, reproducibility contract) is **deferred**; it must not keep blocking functional-skill development. See `skills-registry.yaml` meta `batch2_gate` / `phase_e` and `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md`.

---

## 0. Batch 0 — governance & eval foundation (THIS deliverable)

**Status: IN PROGRESS (this commit).**

- [x] Directory isolation (`.claude/skills/`, `references/`, `evals/skills/`, `docs/skill-development/`).
- [x] Audit (`current-skills-audit.md`).
- [x] Architecture (`system-architecture.md`) — fine-tuned to the real environment.
- [x] Conflict matrix (`conflict-matrix.md`).
- [x] Quality-control plan (`quality-control-plan.md`).
- [x] Registry (`skills-registry.yaml`).
- [x] Upstream method matrix (`references/documentation-methodology/upstream-method-matrix.md`).
- [x] Eval harness + schema + deterministic checkers (`evals/skills/`).
- [ ] Batch-1 four skill **drafts** (experimental + manual-only) — created in this deliverable.
- [ ] Run trigger + conflict evals + one e2e case (this deliverable).

**Exit criterion for Batch 0:** the four drafts exist, the eval sets exist, and `documentation-quality-evaluator` passes its own trigger + basic self-consistency evals. Only then does Batch 2 unlock.

---

## 1. Batch 1 — quality & fact foundation (THIS deliverable)

Order is fixed by dependency (guide §10.2):

| # | Skill | Why first | Ships as | Eval bar to reach `active` |
|---|---|---|---|---|
| 1 | **documentation-quality-evaluator** | Grades every later skill; must exist before we can judge them. | `0.1.0` experimental, manual/orchestrator-only | trigger ≥ 9/10 + 9/10; self-run on a known-good and known-bad doc discriminates them; reader-test protocol executes. |
| 2 | **project-state-reconstructor** | Prevents later skills building on wrong facts. | `0.1.0` experimental, invocation limited to "recover project facts" | trigger evals; produces a state report with FACT/UNKNOWN separation. |
| 3 | **goal-scope-and-workflow-elicitor** | Controls question quality; owns automatic interviewing. | `0.1.0` experimental, orchestrator-only (no auto) | trigger evals + must not over-interview simple tasks (should-not set). |
| 4 | **uncertainty-and-decision-manager** | Unifies status/evidence language; prevents candidate↔fact bleed. | `0.1.0` experimental, orchestrator/`wayfinder`-only | trigger evals + boundary-with-`domain-modeling` conflict cases. |

**Invocation posture (all four):** `disable-model-invocation: true`. Reached only by explicit `/skill` or by a control flow. This satisfies constraints D.3 and the guide §12 "create-but-don't-install" list.

**Deterministic checkers to ship with Batch 1** (constraint D.9): markdown-link validity, file-path existence, status-value legality (against the §7 vocabulary), heading-depth, banned-placeholder scan, stale-date scan, front-matter traceability completeness. These live in `evals/skills/harness/checkers/` and are reused by every skill.

---

## 2. Batch 2 — document structure & research-evidence adapters

**Status: ALL FOUR BUILT + light-round PASSED (2026-08-05).** Decoupled from "DQE reaches `active`" (see the scope-correction note above).
DQE v0.4.1 (advisory) + an independent reviewer + a no-skill comparison was a sufficient eval posture for these.
All ship **experimental + `disable-model-invocation: true`** (manual/orchestrator-only) until their own auto-trigger evals pass.
Trigger 32/32 · 4 read-only shadow runs (targets verified untouched) · 4 reader discipline-checks green. Report: `reports/batch2-skills-eval-2026-08-05.md`.

**Recommended build order** (lowest-risk / most-reused first — not the guide's numbering):

| Build | # | Skill | Key adaptation | Special caution |
|---|---|---|---|---|
| 1st | 8 | `workspace-forensics-and-inventory` | Read-only inventory of a messy workspace / doc corpus. | **Never** move/delete/modify. `project-state-reconstructor` already depends on it; it also supplies real messy-workspace eval samples. |
| 2nd | 5 | `document-information-architect` | Detect mixed doc responsibilities → artifact map + canonical-source + split/link/lifecycle plan. | Easily over-triggers on any writing task → restrict to "document corpus / mixed / needs type-split." Directly addresses the original hybrid-roadmap disease. |
| 3rd | 6 | `research-question-and-literature-planner` | **[ADAPT]** thin scoping front-end (question→scope, inclusion/exclusion, stop criteria, evidence standard) that hands off to `lit-review`/`wos-research`/`deep-research`. | Do-not-trigger must name all existing research skills; must NOT itself run broad retrieval/synthesis. |
| 4th | 7 | `research-evidence-synthesizer` | **[ADAPT]** consumes already-retrieved evidence → matrix/cards/levels/transfer-assumptions; no retrieval. | Must not launch heavy paper flows on ordinary technical questions. |

**Per-skill first round (light — deliberately NOT DQE's heavy corpus):** 3 should-trigger · 3 should-not · 2 boundary/conflict · 1 real shadow run · 1 no-context reader test · 1 no-skill comparison. Only add a regression case after a **real** failure appears.

**Decision point after Batch 2 (OQ-4):** if 6+7 prove to be mostly glue over the L3 stack, merge them into a single `research-evidence-adapter`.

**Phase E (DQE promotion) is deferred**, not cancelled — revisit only after ≥2 Batch-2 skills exist and 5–10 real downstream Skill outputs are collected (then judge DQE on real outputs, not synthetic mutations). See `skills-registry.yaml` meta `phase_e`.

---

## 3. Batch 3 — three control-flow skeletons

| # | Skill | Scope of v0 |
|---|---|---|
| 9 | `numerical-research-software-design` | Orchestrates existing atoms only; carries routing + gates, minimal writing rules. |
| 10 | `scientific-workspace-reconstruction` | Orchestrates forensics→state→goals→architect→migration; enforces ordering. |
| 11 | `documentation-refactor` | Orchestrates forensics(doc)→state→IA→canonicalize→rewrite→evaluate. |

**Must pass the control-flow conflict eval** (`conflict-matrix.md` §1) before any of the three flips to `auto_trigger`. Until then, all three are user-invoked.

**After Batch 3**, optionally down-rank the dormant references (`grill-with-docs`, `ask-matt`, broad `research`/`prototype`) — but since they are not installed, this is a documentation action, not a live change.

---

## 4. Batch 4 — numerical writing & design skills

`research-software-problem-framer` · `scientific-software-architect` · `algorithm-technical-spec-author` · `scientific-prototype-experiment` (from `prototype` SPLIT) · `scientific-validation-and-benchmark-planner` · `research-software-roadmap-author`.

These shape development direction, so they build on the fact-recovery + evidence + evaluation base. `scientific-prototype-experiment` must emit a GO/MODIFY/STOP/NEED-MORE-EVIDENCE decision.

## 5. Batch 5 — workspace & refactor specialists + maintenance

`dev-test-experiment-workspace-architect` · `experiment-provenance-and-reproducibility` · `workspace-migration-planner` (dry-run first) · `content-canonicalization-and-migration` · `technical-document-rewriter` (never overwrite) · `living-design-maintainer`.

Plus the **[ADAPT]** cross-cutting additions when needed: `scientific-validity-review`, `technical-primary-source-research`, `research-software-workflow-router`, `setup-research-software-skills`.

---

## 6. Per-skill creation checklist (guide §13, applied to every skill)

1. **Responsibility boundary** — solves / does-not-solve / inputs / outputs / calls / must-not-co-trigger.
2. **Real cases** — ≥3 success, ≥3 edge, ≥3 should-not, ≥2 conflict, ≥1 insufficient-info.
3. **Intermediate artifacts** — not just the final doc (fact audit, assumption register, migration map, evidence matrix, decision gate, reader-test report).
4. **Compact `SKILL.md`** — the §13-step-4 structure; details pushed to `references/`.
5. **Deterministic scripts** — for everything checkable.
6. **Trigger evals** — 10 should / 10 should-not / 5 conflict / 5 short-ambiguous / 3 multi-turn.
7. **Task-quality evals** — vs no-skill, vs upstream ref, vs prior version.
8. **No-context reader test** — fresh agent answers fixed questions from the output alone.
9. **Shadow run** — manual / dry-run / suggest-only before any auto-trigger.
10. **Versioned release** — `0.x → 1.0 → 1.x → 2.0` with registry + changelog updates.

---

## 7. What we deliberately are **not** building (and why)

| Not building | Because (from audit) |
|---|---|
| A from-scratch literature retriever / paper downloader / OCR | `lit-review` + `wos-research` + `scansci-pdf` + `mineru-ocr` + `paper-fetch-skill` already own this. |
| A heavy `research-evidence-synthesizer` that also searches | Retrieval belongs to the L3 stack; the synthesizer only *consumes* + *maps*. |
| Replacements for `to-spec`/`to-tickets`/`triage`/`wayfinder` now | Not installed → no live conflict → defer to an optional tracker decision (OQ-1). |
| Expanding `code-review` with scientific checks | Keep `code-review` lean; add a separate `scientific-validity-review`. |
| Course/TS-specific skills (`teach`, `scaffold-exercises`, `migrate-to-shoehorn`, `setup-ts-deep-modules`) | Irrelevant to research-software docs. |

---

## 8. Milestone acceptance (maps to guide §15)

Batch 1 is "done" when:
- All four skills are registered, `experimental`, manual-only. ✔ by construction.
- Trigger should/should-not pass for each (auto-triggered set is empty, so this is about *self-restraint*: they must decline when invoked on out-of-scope inputs). 
- Conflict eval shows no auto co-trigger possible. ✔ by construction.
- Every writing skill declares write-scope + rollback. ✔ (all read-only / new-files-only).
- All research artifacts use the §7 status + evidence language. ✔ enforced by `uncertainty-and-decision-manager` + evaluator checker.
- ≥1 real end-to-end case run (this deliverable runs one).
- `documentation-quality-evaluator` beats no-skill baseline on a doc-grading task in an A/B check.
- A no-context reader can extract goal/state/next-step/acceptance/open-questions from the produced state report.

**Batch 2 entry (revised 2026-08-05):** Batch 2 began once `documentation-quality-evaluator` cleared its **basic** bar (§1 row 1) — which it did. It is **no longer** blocked on DQE reaching a universal terminal gate; that promotion (Phase E) is deferred. New Batch-2 skills still ship experimental + manual-only and are evaluated with the light per-skill round in §2.
