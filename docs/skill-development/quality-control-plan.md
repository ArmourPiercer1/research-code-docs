# Quality-Control Plan — Research-Software Documentation Skills System

<!--
generated_by_skill: (manual, Phase-1 governance authoring)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/研究软件文档Skills系统_设计与创建指南.md (§13-§15, quality control)
  - docs/prompt.md (constraints D, deliverable C)
status: DECIDED (v0.1 QC policy)
last_verified: 2026-07-30T09:47:06Z
-->

> Treats the Skills system as a **software product**: architecture, tests, versions, dependencies, run logs, deprecation (guide §17). This plan defines how any skill is judged, what blocks release, and how regressions are caught.

---

## 1. The two-tier gate: hard fails vs soft score

Every skill output passes through **hard gates first** (binary, mostly script-checked). Only if all hard gates pass is the **soft rubric** scored. A hard fail is a release blocker regardless of soft score (guide §14.10).

### 1.1 Hard failure conditions (binary, system-wide)

A skill output **fails** if it does any of:

| ID | Hard fail | Check type |
|---|---|---|
| HF-1 | Fabricates code state (claims behavior not in code/tests). | model + spot-checker (symbol existence) |
| HF-2 | Fabricates literature (citation with no resolvable source). | checker (citation resolvable) + model |
| HF-3 | Writes a CANDIDATE/HYPOTHESIS as DECIDED/FACT. | checker (status vocabulary) + model |
| HF-4 | Overwrites an original document a rewrite skill was told not to touch. | checker (no-overwrite diff guard) |
| HF-5 | Moves/deletes files without explicit approval. | checker (write-scope guard) |
| HF-6 | Roadmap phase with no acceptance criteria. | checker (roadmap schema) |
| HF-7 | Drops a known OPEN question silently. | model diff vs decision register |
| HF-8 | Output only makes sense with unstated conversation context. | no-context reader test |
| HF-9 | Missing traceability front-matter (skill/version/commit/time/status). | checker (front-matter completeness) |
| HF-10 | Treats paper/indirect evidence (≤E2) as project-verified (E3+). | checker (evidence-level tag) + model |
| HF-11 | A skill without passing evals auto-triggered. | registry guard (`auto_trigger` vs eval status) |
| HF-12A–E | A load-bearing claim is unsupported/mis-supported — A traceability + E evidence-status (doc-only); B accessibility + C actual-support + D transfer-assumptions (source-needing). | model + claim→evidence map |
| HF-13 | Mixed artifact responsibilities — one file carries divergent-lifecycle formal roles as body-level content, with drift. | model + `artifact_role_mixing`/`state_number_consistency` signals |
| HF-14a | State contradiction — mutually contradictory state values in the doc/corpus. | model + `state_number_consistency` |
| HF-14b | Volatile-state contamination — a stable-design doc embeds volatile state with no single dynamic source. | model (type-gated) + `completion_open_conflict` |
| HF-15 | Non-executable committed milestone — a committed roadmap phase's acceptance is vague/non-measurable. | model + `roadmap_stage_fields` |

Checkers for HF-3, HF-4, HF-5, HF-6, HF-9 are deterministic and live in `evals/skills/harness/checkers/` (constraint D.9).
The **v0.3** additions HF-13/14a/14b/15 + the HF-12 decomposition are backed by **SIGNAL** checkers
(`state_number_consistency`, `completion_open_conflict`, `roadmap_stage_fields`, `agent_session_residue`,
`artifact_role_mixing`) that surface *candidates* the grader adjudicates — they never auto-block. Full
catalog: `evals/skills/harness/hard-fail.md`. HF-13/14/15 were added after a **hybrid-roadmap false-pass**
(see `reports/dqe-v0.3-upgrade-2026-07-30.md`).

### 1.2 Soft rubric (0–100, weighted; guide §14.10)

| Dimension | Weight | What "good" means |
|---|---:|---|
| Factual accuracy | 20 | Claims trace to code/tests/experiments/authoritative source. |
| Information architecture | 15 | Right content in the right doc type; clean boundaries. |
| Actionability | 15 | Next steps + acceptance criteria are concrete. |
| Evidence traceability | 15 | Every non-trivial claim cites its source + evidence level. |
| Uncertainty expression | 10 | Unknowns/hypotheses/candidates explicitly labeled. |
| Reader fit | 10 | A no-context reader of the target role can act on it. |
| Maintainability | 10 | Canonical-source discipline; no duplication. |
| Concision | 5 | No filler; within context budget. |

**Pass line:** hard gates all pass **and** soft ≥ 75, with no single dimension < 50. `documentation-quality-evaluator` is the skill that computes this; its own rubric file is versioned in `evals/skills/harness/rubric.md`.

---

## 2. Per-skill eval suite (what deliverable C requires for each of the four)

Per the prompt, each Batch-1 skill gets, under `evals/skills/`:

- **10 should-trigger** — inputs where the skill (when invoked) should engage and do its job.
- **10 should-not-trigger** — inputs where it must **decline / defer / route elsewhere** (self-restraint; especially "this is a simple task").
- **5 conflict cases** — inputs where an adjacent skill competes; correct behavior = defer/hand-off per `conflict-matrix.md`.
- **3 multi-turn cases** — context builds over turns; the skill must not lose state or re-interview.
- **≥2 real historical project tasks** — drawn from the actual environment (e.g., a `gpt` particle-tracer study; a messy multi-script analysis workspace). Marked `real:true` in the case file.
- **Hard-fail conditions** — the subset of §1.1 that applies, listed per skill.
- **Soft-score rubric** — the §1.2 weights, with skill-specific "good/bad" anchors.

Because all four Batch-1 skills are **manual-only**, "should-trigger" is evaluated as *"when explicitly invoked on this input, does it engage correctly?"* and "should-not-trigger" as *"when invoked on an out-of-scope input, does it correctly decline or route away?"* — i.e., we test **self-restraint and routing**, not autonomous firing (which is disabled).

Case file schema: `evals/skills/README.md` §"Case schema".

---

## 3. Eval types & where they live

| Eval type | Dir | Question answered |
|---|---|---|
| Trigger | `evals/skills/trigger/` | Does it engage/decline on the right inputs? |
| Conflict | `evals/skills/conflict/` | Does it defer to the right neighbor? |
| Task-quality | `evals/skills/task-quality/` | Is the output better than no-skill / upstream / prior version? |
| Multi-turn | `evals/skills/multi-turn/` | Does it hold state across turns? |
| Reader-test | `evals/skills/reader-tests/` | Can a no-context reader act on the output? |
| Regression | `evals/skills/regression/` | Did a change re-break a previously-fixed case? |
| Results | `evals/skills/results/` | Timestamped run outputs + verdicts. |

---

## 4. How evals are run (isolation-respecting)

Per the working constraints, we do **not** install skills to test them. Instead:

1. A **sub-agent** is spawned with the skill's `SKILL.md` body **injected directly into its prompt**, plus the eval case input.
2. For **trigger** evals, the sub-agent is asked to decide *engage / decline / route-to-X* and justify — we score the routing decision, not a full run.
3. For **task-quality / reader-test** evals, the sub-agent runs the skill on a real input and produces the artifact; a separate grader sub-agent (running `documentation-quality-evaluator`) scores it.
4. Deterministic checkers run over produced artifacts as a pre-filter (hard gates) before any model grading.
5. Results are written to `evals/skills/results/<skill>/<date>.md` with the verdict, the skill version, and the run timestamp (constraint D.10).

This keeps everything inside the workspace and never touches the live loader.

---

## 5. Eval-dataset governance (guide §14.9)

The eval set must include, and be **versioned** to avoid overfitting to current failures:
- synthetic cases; real historical projects; edge cases; adversarial triggers; ultra-short ambiguous inputs; large messy workspaces; missing-file / fact-conflict cases; multilingual (zh/en) docs; **old docs containing wrong conclusions** (to test that the system recovers facts rather than inheriting them).

Each case file carries `dataset_version`. Adding a case to fix a specific failure requires also adding a **general** case covering the class, so the suite doesn't become a memorized answer key.

---

## 6. Regression policy (guide §14.11)

After **any** skill edit, re-run: its own trigger set; adjacent-skill conflict set; the relevant control-flow e2e; the real-project cases; previously-failed cases; and the **no-skill baseline** for contrast. A skill may not be re-promoted to `active` on a green partial run — the regression set must be green.

---

## 7. Observability / run log (guide §14.12)

Every skill run (in eval or in real use) logs to `docs/skill-development/reports/runlog.md` (append-only): which skill fired, why, which references loaded, which sub-skills called, files created/modified, which gate failed, what the user corrected, and whether the output was accepted. Without this, quality drift can't be attributed to rule / routing / context / model variance.

Log line schema:
```text
<ISO-time> | skill=<name>@<version> | trigger=<reason> | refs=[…] | calls=[…] | wrote=[…] | gate=<pass|fail:HF-x> | accepted=<y/n> | note=<…>
```

---

## 8. Traceability requirement (guide §14.6, constraint D.10)

Every generated document carries front-matter:
```yaml
generated_by_skill:
skill_version:
source_commit:
source_documents:
status:            # from the §7 vocabulary
last_verified:
```
The `front-matter-completeness` checker (HF-9) enforces presence; a missing field is a hard fail.

---

## 9. License & provenance governance (guide §14.7, constraint D.2)

- Every **adopted rule** records repo@commit + license + adoption type (copy / adapt / method-borrow) in `references/documentation-methodology/upstream-method-matrix.md`.
- Non-commercial-licensed content is not baked into any skill.
- Attribution is retained; upstream is re-checked periodically but never auto-overwrites local versions.
- **No simple concatenation of upstream `SKILL.md`** (constraint D.1) — each rule is re-derived and bounded.

---

## 10. Phase-1 concrete pass targets

| Skill | Minimum to be called "Batch-1 complete" |
|---|---|
| documentation-quality-evaluator | trigger ≥ 9/10 engage + ≥ 9/10 decline; discriminates a seeded good vs bad doc; reader-test protocol runs; beats no-skill on one A/B grading task. |
| project-state-reconstructor | trigger evals pass; state report cleanly separates FACT vs UNKNOWN; no fabricated status (HF-1). |
| goal-scope-and-workflow-elicitor | trigger evals pass; declines to interview on ≥ 9/10 simple-task should-not cases; no duplicate questions across a 3-turn case. |
| uncertainty-and-decision-manager | trigger evals pass; correctly assigns §7 status + evidence levels; respects the `domain-modeling` boundary in all 5 conflict cases. |

**Gate:** `documentation-quality-evaluator` had to clear its **basic** target (§10 row 1) before Batch 2 began — it did. **Scope-correction (2026-08-05):** Batch 2 is now DECOUPLED from DQE becoming a *universal automatic terminal gate*; DQE v0.4.1 is frozen as an **advisory / profile-scoped** evaluator and the heavier Phase-E promotion is deferred (see `skills-registry.yaml` meta `batch2_gate`/`phase_e`).
