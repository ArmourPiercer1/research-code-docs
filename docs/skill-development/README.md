# Skill Development — Phase 1 Index

<!--
generated_by_skill: (manual, Phase-1)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents: [docs/prompt.md, docs/研究软件文档Skills系统_设计与创建指南.md]
status: DECIDED (Phase-1 complete; DQE v0.4.1 advisory freeze; Batch 2 built + light-passed; Batch 2.5 integration DONE; Batch 3 v0 skeletons BUILT)
last_verified: 2026-08-05
-->

> Governance home for the research-software documentation **Skills system**. Everything here is
> **workspace-only** and isolated from the live Claude Code loader (versioned via GitHub). Nothing
> is installed or auto-triggered without explicit user approval.

## Phase-1 ✅ · DQE **v0.4.1 FROZEN (advisory / profile-scoped)** · Batch 2 **4/4 built + light-passed** · Batch 2.5 **integration DONE** · Batch 3 **3 v0 skeletons BUILT**

> **Scope correction (2026-08-05).** DQE reached a reliable **advisory** state (v0.4.1). Rather than keep
> expanding its test system toward a *universal automatic terminal gate*, we **froze it as advisory /
> profile-scoped**, **decoupled Batch 2** from that promotion, and **entered Batch 2**. The halted Phase-E
> D-17 canary (a `controlled + release-gate` experiment report stably false-ALLOWs) is resolved by **scoping
> that profile out** → `GATE_DECISION=INCOMPLETE / GATE_REASON=unsupported-evaluation-profile` (no HF-REPRO,
> no HF-threshold change). **Phase E is deferred** to a future promotion gate. Details:
> [dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md](reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md).
> All skills remain `experimental` + manual-only; nothing installed or pushed.

<details><summary>Earlier: Phase-1 complete · v0.2 real refs · v0.3 false-pass fix · v0.4 profile-aware</summary>

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

</details>

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

## Next (Batch 3 v0 skeletons BUILT; Batch 4/5 atoms are next)

The four Batch-2 skills passed their light round, and **Batch 2.5** then proved they **compose through explicit,
deterministically-checked artifact interfaces with no chat dependence** — two real chains, one run each:
**Track A** `forensics(document-corpus) → PSR → goals → IA → DQE-advisory → reader` (over the real
`docs/skill-development/` corpus) and **Track B** `RQLP → lit-review(real, 5 sources) → RES → UDM → DQE-advisory
→ reader`. A minimal 12-field handoff interface is frozen ([`references/interfaces/`](../../references/interfaces/)
+ `interface_check.py`); all §7 exit conditions met; **0 SKILL_DEFECT / 0 INTERFACE_DEFECT**; sources unchanged;
`.pyc` hygiene done; architecture §8 gate-rule corrected to *advisory checkpoint*. All four Batch-2 skills stay
`experimental` + manual-only. Report:
[batch2_5-integration-2026-08-05.md](reports/batch2_5-integration-2026-08-05.md) (earlier:
[batch2-skills-eval](reports/batch2-skills-eval-2026-08-05.md) +
[batch2-workspace-forensics-eval](reports/batch2-workspace-forensics-eval-2026-08-05.md)).
**Batch 3 then built the three L1 control-flow skeletons** — `documentation-refactor`,
`scientific-workspace-reconstruction`, `numerical-research-software-design` — as v0 orchestrators that route the
atoms, record a `flow-state`, and **stop honestly (`BLOCKED`) at their missing Batch-4/5 capabilities** (two
reuse the Batch-2.5 chains; one ran a live prefix on the eval harness). All `flow_state_check`-green +
reader-green; all `experimental` + manual-only. Report:
[batch3-skeletons-2026-08-05.md](reports/batch3-skeletons-2026-08-05.md). **Next options:** a full
trigger/conflict sub-agent run on the 3 flows (the gate before any `auto_trigger`), or start **Batch 4** (the
numerical-design atoms) / **Batch 5** (the doc/workspace executor atoms) that unblock the flows. See
[creation-roadmap.md](creation-roadmap.md) §3–§5.
