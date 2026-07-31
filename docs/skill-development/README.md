# Skill Development — Phase 1 Index

<!--
generated_by_skill: (manual, Phase-1)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents: [docs/prompt.md, docs/研究软件文档Skills系统_设计与创建指南.md]
status: DECIDED (Phase-1 complete; Batch-2 unlocked)
last_verified: 2026-07-30T09:47:06Z
-->

> Governance home for the research-software documentation **Skills system**. Everything here is
> **workspace-only** and isolated from the live Claude Code loader (versioned via GitHub). Nothing
> is installed or auto-triggered without explicit user approval.

## Phase-1 status: ✅ complete · Batch-2 gate: ⚠️ PROVISIONAL · DQE at **v0.3.0** (false-pass fixed)

`documentation-quality-evaluator` passed its basic evals (trigger 28/28 + discriminative e2e), which
per [prompt.md](../prompt.md) §E unlocked Batch 2. It was then upgraded to **0.2.0** (real vendored
references). **v0.3.0** fixes a **hybrid-roadmap false-pass** found in an independent audit: the evaluator
had FAIL-ed a broken hybrid roadmap on the trivial HF-9 only, called it "substantively high quality", and
predicted a re-eval PASS. v0.3 adds anti-erosion discipline + structural gates **HF-13/HF-14a/HF-14b/HF-15**,
a decomposed **HF-12A–E** (DOCUMENT_QUALITY vs FACTUAL_VALIDITY), non-compensatory scoring, a two-layer
reader, a structured verdict, and 5 SIGNAL checkers. The eoopt roadmap is now a **permanent golden-negative**
that FAILs correctly (recall 1.0, false_pass 0); a comprehensive report still PASSes (no over-fire);
trigger+conflict **28/28 no-regression**. **The Batch-2 gate is now PROVISIONAL** — DQE is not a terminal
gate until the v1.0 bar (full golden suite + ablation + recall≥90%) is met. Details:
[dqe-v0.3-upgrade-2026-07-30.md](reports/dqe-v0.3-upgrade-2026-07-30.md). All skills remain
`experimental` + manual-only. Per-method attribution + license:
[upstream-method-matrix.md](../../references/documentation-methodology/upstream-method-matrix.md).

## Deliverables (this phase)

| Doc | What it is |
|---|---|
| [current-skills-audit.md](current-skills-audit.md) | Phase A: audit of all installed + reference skills, classified KEEP/…/REMOVE |
| [system-architecture.md](system-architecture.md) | Phase B: the fine-tuned architecture (layers, call chains, trigger ladder, norms, write model, budgets, versioning) |
| [conflict-matrix.md](conflict-matrix.md) | pairwise co-trigger rules + release gates |
| [creation-roadmap.md](creation-roadmap.md) | batched creation plan (0→5) + what we deliberately don't build |
| [quality-control-plan.md](quality-control-plan.md) | hard-fail catalog, soft rubric, eval methodology, governance |
| [skills-registry.yaml](skills-registry.yaml) | machine-readable roster (schema, status, write-scope, evals) |
| [../../references/documentation-methodology/upstream-method-matrix.md](../../references/documentation-methodology/upstream-method-matrix.md) | per-rule source + license + adoption boundary |
| [reports/batch1-eval-run-2026-07-30.md](reports/batch1-eval-run-2026-07-30.md) | the eval run + gate decision |
| [reports/runlog.md](reports/runlog.md) | append-only observability log |

## The four Batch-1 skills (drafts)

Under [`.claude/skills/`](../../.claude/skills/) — all `disable-model-invocation: true`, now at **v0.2.0**:

1. `documentation-quality-evaluator` — grades every other skill (built first). **v0.3.0** · evals: anchor golden-negative FAILs correctly (recall 1.0, false_pass 0) + B1 over-strictness PASS + trigger 28/28. +HF-13/14a/14b/15, HF-12A–E, non-compensatory scoring, two-layer reader, structured verdict, 5 signal checkers.
2. `project-state-reconstructor` — recover facts → state report. +claimed-vs-verified ledger, pipeline-trace anchor, evidence-hygiene trust tiers, two-tier unknowns.
3. `goal-scope-and-workflow-elicitor` — interview for goals/scope/workflow. +hypothesis+confidence, sufficiency stop, correctable-brief, fixed-field restate.
4. `uncertainty-and-decision-manager` — status + evidence register. +ADR supersede-lifecycle, checkable-locator sources, `proof_context`, adversarial promotion gate, claim disposition.

## Eval harness

Under [`evals/skills/`](../../evals/skills/): deterministic checkers (`harness/checkers/`), rubric +
hard-fail catalog, injection/scoring scripts, and 134 case files (trigger/conflict/multi-turn/task-quality).
Runner uv-venv: `.venv/` (pyyaml). See [evals/skills/README.md](../../evals/skills/README.md).

## Open items carried forward (not hidden)

- **OQ-1** issue tracker? · **OQ-2** install `git-guardrails`? · **OQ-3** confirm research-stack license · **OQ-4** merge the two research adapters? · **OQ-5** final router scope. (See architecture §13.)
- **G3** narrow installed `research` so it won't fire on literature tasks — needs user approval to modify an installed skill.
- **Real-task gap** — ≥2 real historical project tasks per skill must be supplied by the user; current task-quality cases are environment-grounded, not verbatim (constraint D.8).
- **Not yet executed** — multi-turn runs; task-quality soft-scoring for PSR/GSWE/UDM; standalone reader-agent pass. (Batch-1→2 hardening.)

## Next (Batch 2, now unlocked)

`document-information-architect` · `research-question-and-literature-planner` (adapter over lit-review/wos-research/deep-research) · `research-evidence-synthesizer` (consumes retrieved evidence) · `workspace-forensics-and-inventory` (read-only). See [creation-roadmap.md](creation-roadmap.md) §2.
