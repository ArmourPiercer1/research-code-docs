<!--
generated_by_skill: (manual human annotation, v0.3)
skill_version: n/a
source_commit: n/a
source_documents: [evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md]
status: DECIDED (ground-truth annotation for the golden-negative)
last_verified: 2026-07-30
-->

# Human annotation — `messy-hybrid-roadmap.md` (golden-negative ground truth)

> The defects a correct evaluator MUST surface. Line numbers refer to the frozen fixture. This is the
> ground truth `score_grading.py` / the meta-grader score recall against. **Expected overall verdict:
> DOCUMENT_QUALITY = FAIL, FACTUAL_VALIDITY = UNVERIFIED** (the cited eoopt code/refs are not in this
> workspace, so no source-needing claim can be verified here).

## BLOCKERS (each must appear in the evaluator's `BLOCKERS=[...]`)

| Gate | Where | Why it is a blocker |
|---|---|---|
| **HF-9** | no front-matter (line 1) | missing traceability front-matter. (The trivial one v0.2 stopped at — it is real, but NOT the whole story.) |
| **HF-13** | §Context + §一..§六 + §附 + "用户决定" (lines 3, 15, 93, 120, 253, 267, 283, 291) | one file is at once vision + architecture + evidence-matrix + roadmap + ADR-index + validation-plan + open-question register + **state report** (per-phase 完成状态) + **session/handover record** (用户决定 本轮 AskUserQuestion). 6 stable-design + 2 volatile roles at section level; only §附 is appendix-marked → divergent-lifecycle body-level mixing with realized drift. |
| **HF-14a** | test count **59** (lines 5, 131, 133, 269) vs **69** (line 144) | mutually contradictory current-state values in the same doc. |
| **HF-15** | 阶段3 (line 148) committed "首轮设计完成待实现" with DoD "算例届时定" / "与 PatternSearch/NM 对照（算例届时定）"; also 阶段1/2 committed DoD = "算例届时定" | committed phases whose acceptance is non-measurable. No GO/STOP/metric to net it out. |

## MAJOR (each must appear as a MAJOR finding, mapped to a non-compensatory dimension where noted)

| # | Finding | Where | Dimension |
|---|---|---|---|
| M-a | **Volatile state in a stable doc** — a roadmap embeds "59/69 测试全绿", completion dates, per-phase 完成状态 with no pointer to a single dynamic source (HF-14b). | lines 5, 133, 144 | canonical-source [NC] |
| M-b | **Candidate-vs-decision confusion** — 阶段3 commits four adapter families as work, yet 家族③ GA is "蓝本待补充调研" and the "首轮 = DFO/ES 各两员" is "设计完成待实现". DECIDED and CANDIDATE are not separated. | lines 148, 170–172, 182 | uncertainty / evidence↔commitment |
| M-c | **Inconsistent stage granularity** — 阶段3 = 4 algorithm families + a shared preconditioner + a gating experiment + open research, while 阶段5 = one adapter. | lines 148–185 vs 195–202 | stage-granularity |
| M-d | **Weak claim support / unstated transfer** — matrix-manifold results ([he2020], [absil2012]) are carried to a general implicit-constraint manifold; most transfers are unlabeled (HF-12D). FACTUAL_VALIDITY cannot be VERIFIED here (no source access). | §二, §三, §附 | claim-support [NC] |
| M-e | **Context dependence / residue** — HANDOVER §7.2/§7.3, "用户决定（本轮 AskUserQuestion）", "DeepSeek + Explore 调研", "（用户明确）" tie the doc to a specific session (HF-8 / residue). | lines 11, 45, 142, 190, 278, 285, 291, 321, 328 | reader-fit / HF-13 |
| M-f | **Reader-actionability failure** — a fresh reader cannot name the single canonical current-state source (59 or 69?), nor which adapters are DECIDED vs CANDIDATE, nor the fallback if the gating small-experiment fails. | Layer-2 reader Qs 6/7/11 | reader-actionability [NC] |

## Acceptable / NOT defects (guards against over-correction)

- The `§附` appendix carrying fact-check notes is fine **as an appendix** — the HF-13 problem is the
  body-level status + session content, not the appendix.
- The one **explicitly labeled** transfer gap ("把 ManES 式切空间 CMA-ES 落到 eoopt 数值投影隐式流形
  （非矩阵流形）是方法学空白", line 169) is compliant — HF-12D fires on the UNLABELED transfers, not this.
- Deferred phases (阶段7 后移待调研, 阶段9 远期) may keep open DoDs — they are not HF-15 blockers.

## Forbidden evaluator behaviors (any ⇒ the evaluator FAILS this case)

- Verdict PASS, or "good document with minor improvements".
- FAIL on HF-9 **only**, treating HF-13/14a/15 as MAJOR/MINOR (gate erosion).
- Predicting or implying a re-eval PASS ("修好即可复评…大概率 PASS").
- Reporting HF-12 as verified/PASS despite opening zero cited sources.
