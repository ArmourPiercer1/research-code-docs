# DQE v0.3 Upgrade — Hybrid-Roadmap False-Pass Fix

<!--
generated_by_skill: (manual, v0.3 upgrade run)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md (third-party audit / upgrade spec)
  - docs/skill-development/reports/quality-report-最终目标设计与开发路线图.md (the v0.2 false-pass)
  - evals/skills/results/documentation-quality-evaluator/e2e/quality-report-anchor-v0.3.md (v0.3 anchor re-eval)
  - evals/skills/results/documentation-quality-evaluator/trigger-v0.3-2026-07-30.json
status: DECIDED (run recorded)
last_verified: 2026-07-30
-->

> **What happened:** `documentation-quality-evaluator@0.2.0` was run on a real research-software
> roadmap (`tests/最终目标设计与开发路线图.md`) and **false-passed it in substance** — verdict FAIL but
> only on the trivial HF-9 (missing front-matter), while declaring the doc "文档实质质量高" and predicting
> a re-eval PASS. This upgrade to **0.3.0** fixes that. Skill stays `experimental` + manual-only; nothing
> installed or pushed.

## 1. Root cause (reproduced, not assumed)

Re-running `run_checks.py` on the target confirmed the checker JSON in the v0.2 report was genuine
(front-matter fail, 36 broken links, status/placeholders pass). The failure was in the **rule set +
methodology**, three compounding bugs:

1. **Hard-gate erosion.** The evaluator *found* most symptoms but reclassified them as compensable soft
   findings — the 59/69 test-count contradiction → "MAJOR M1"; undefined workflow labels → "M2"; a phase
   with no acceptance → "M3". Even the **existing HF-6** (roadmap phase without acceptance) was talked
   down to MAJOR ("不升为第二 BLOCKER"). New gates alone would be eroded the same way.
2. **Stop-at-first-gate + PASS-prediction.** It stopped at the trivial HF-9 and wrote "修好即可复评…
   大概率 PASS". *That prediction is the real false-pass.*
3. **Claim-support passed without source access.** HF-12 was marked "PASS (纪律很强)" though the report
   itself said "本区无参考库，逐条解析未做" — it graded "has a citation handle" as "supported".

Neither (a) mixed artifact responsibilities, (b) volatile-state contamination, nor (c) systemic
non-executable milestones had a gate at all — so the evaluator read "10 documents in one file" as a
*completeness strength* and *excused* "算例届时定" as "显式设计性延迟".

## 2. What changed (v0.3)

| Area | Change |
|---|---|
| **Anti-erosion discipline** | SKILL.md: evaluate EVERY applicable gate, collect ALL blockers, never stop at the first; a met gate may not be downgraded; **no PASS-prediction** while a structural gate or non-compensatory dim is failing/unassessed. |
| **New hard gates** | `hard-fail.md`: **HF-13** mixed artifact responsibilities (with appendix escape hatch), **HF-14a** state contradiction (all types) / **HF-14b** volatile contamination (stable-design types only), **HF-15** non-executable committed milestone (reconciled with HF-6 = presence; research-phase + deferred escapes). |
| **HF-12 → A–E** | A traceability + E evidence-status label are **doc-only** (→ DOCUMENT_QUALITY); B accessibility + C actual-support + D transfer-assumptions **need source access** (→ FACTUAL_VALIDITY). Zero sources opened ⇒ FACTUAL_VALIDITY=UNVERIFIED; may not report "HF-12 PASS". |
| **Scoring** | `rubric.md`: **non-compensatory** rule anchored to a *substantiated paired gate* (not a raw score) so breadth can't buy back a structural failure — and it can't false-FAIL on a mere low score. Added a **roadmap-specific rubric**. |
| **Reader test** | Two layers: comprehension+location, then execution+refutation (next+DoD / decided-vs-candidate / fallback / stale / off-goal sections). A contract-misread on a core question is ≥ MAJOR, never dismissed as "reader error". |
| **Structured verdict** | Machine-parseable `KEY=VALUE` block (DOCUMENT_QUALITY / FACTUAL_VALIDITY / READER_TEST / CHECKER_STATUS / SOURCE_COVERAGE / CONFIDENCE / BLOCKERS / FILES_READ) + `INCOMPLETE_EVALUATION` state + a terminal-gate formula for downstream skills. |
| **5 SIGNAL checkers** | `state_number_consistency`, `completion_open_conflict`, `roadmap_stage_fields`, `agent_session_residue`, `artifact_role_mixing` — all ADVISORY-class SIGNAL (never block/affect exit code); shared `_textutils.mask_noise` (fences + inline code + link URLs; CJK-safe). |
| **Isolation harness** | `make_grading_injection.py` (evaluator / reader / meta roles — reader deliberately gets neither rubric nor hard-fail) + `score_grading.py` (recall / false-pass / blocker-precision + `forbidden_report_patterns`). Closes the "evaluator ran in the main session" leak. |
| **Canonical-source map** | New always-loaded reference grounding HF-14b ("this belongs in CI/status, not the roadmap"). |

Per-method attribution + license in `references/documentation-methodology/upstream-method-matrix.md` §2.1.

## 3. Eval results

### 3.1 Anchor regression (the headline) — the eoopt roadmap, frozen as the permanent golden-negative

Isolated fresh sub-agent, v0.3 skill injected, **no project context**. Scored by `score_grading.py`
against the human annotation (`fixtures/dqe/negative/messy-hybrid-roadmap.annotations.md`):

```
DOCUMENT_QUALITY=FAIL   FACTUAL_VALIDITY=UNVERIFIED   READER_TEST=FAIL   SOURCE_COVERAGE=0/64
BLOCKERS=[HF-9, HF-13, HF-14a, HF-14b, HF-15]
severe_issue_recall = 1.00 (bar ≥ 0.90)   false_pass = 0 (bar = 0)   ==> evaluator PASS
```

The doc-only structural gates fired; claim-support was **not** reported verified (0 sources openable);
**no re-eval PASS was predicted**. The exact v0.2 failure is closed.

### 3.2 Over-strictness guard — B1 comprehensive architecture report (must NOT trip HF-13)

```
DOCUMENT_QUALITY=PASS   BLOCKERS=[]   (HF-13 correctly does NOT fire — appendix subordination +
single update mechanism + no drift; PASS is not a green *terminal* gate because FACTUAL_VALIDITY=UNVERIFIED)
```

The new gates do not over-fire on a legitimate broad document. Deterministic guards P1 (lightweight
roadmap), B2 (research roadmap w/ GO/STOP), B4 (prompt-injection), B5 (hollow template) behave correctly
at the checker layer (P1/B2 clean; B4/B5 flag vague/empty DoD).

### 3.3 No-regression — trigger + conflict (behavior changed → §14.11)

`score_all.py` on a fresh injected sub-agent: **should-trigger 10/10 · should-not 10/10 ·
short-ambiguous 3/3 · conflict 5/5 = 28/28, GATE PASS.** No routing regression (the SKILL `description`
was kept byte-identical).

### 3.4 Deterministic self-check

New checkers dogfooded: **clean on `good-state-report.md`** and on B1/B2/P1; surface exactly the eoopt
defects (59-vs-69, three vague committed DoDs, 6-pattern session residue, 8 section-level roles / 2
volatile). HARD-gate sweep over all authored output dirs = `hard_fail=False`. `validate_cases.py`:
142 cases OK.

## 4. Honest deferrals (v0.4 candidate)

Per the third-party's version ladder (v0.3 new gates → v0.4 full golden suite → v1.0 stable terminal
gate), this pass **defers**:

- The full **N1–N5 / P1–P4 / B1–B5** golden suite as *model-graded* cases (this pass model-graded the
  anchor + B1; the rest are deterministically checked + specified).
- The **5-way ablation matrix** (without_skill / v0.2 / v0.3 / no-reader / no-checkers) and the full
  numeric admission bar (blocker-precision, evidence-classification accuracy, 3-round regression).
- A second **real** historical task (constraint D.8 — the eoopt roadmap is now one real anchor; the user
  is to supply a second; not fabricated).

**Until the v1.0 admission bar is met, `documentation-quality-evaluator` remains `experimental`,
manual/orchestrator-only, and its PASS is NOT a terminal auto-approval for other skills** (registry
`batch2_gate` marked PROVISIONAL).

## 5. Reproduce

```bash
# anchor re-eval (assemble isolated prompt -> fresh sub-agent -> score)
.venv/Scripts/python.exe evals/skills/harness/make_grading_injection.py documentation-quality-evaluator \
  evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md --role evaluator
.venv/Scripts/python.exe evals/skills/harness/score_grading.py messy-hybrid-roadmap-001 \
  evals/skills/results/documentation-quality-evaluator/e2e/quality-report-anchor-v0.3.md

# checker signals on the anchor / a clean doc
.venv/Scripts/python.exe evals/skills/harness/checkers/run_checks.py \
  evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md

# trigger regression
.venv/Scripts/python.exe evals/skills/harness/score_all.py documentation-quality-evaluator \
  evals/skills/results/documentation-quality-evaluator/trigger-v0.3-2026-07-30.json
```
