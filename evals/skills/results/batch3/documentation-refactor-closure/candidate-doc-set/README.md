<!--
generated_by_skill: technical-document-rewriter
skill_version: 0.1.0
source_commit: 07b5306
source_documents: [docs/skill-development/README.md]
document_lifecycle: DRAFT
last_verified: 2026-08-06T00:00:00Z
-->

# Skill Development — Phase 1 Index

> Governance home for the research-software documentation **Skills system**. Everything here is
> **workspace-only** and isolated from the live Claude Code loader (versioned via GitHub). Nothing
> is installed or auto-triggered without explicit user approval.

<!-- CANDIDATE REWRITE — split S2 (migration-map disposition: DEFERRED, blocked_by D-1). The live
     phase/batch/version status header + version changelog that stood here (source README.md lines 16-43)
     is dynamic state, not stable index content; per the volatile-state -> pointer rule it is removed from
     this stable index and replaced by the single pointer below. The pointer TARGET is left UNRESOLVED on
     purpose: D-1 (which surface owns "current project status") is OPEN, and naming an owner here would
     decide D-1 — which this rewrite must not do. No figure is re-invented; a stale value becomes a
     pointer, not a fresh number. -->

**Current status / phase / batch progress ->** the canonical status owner (**PENDING decision D-1**).
This README is the stable **plan + index**, not the status tracker (the volatile-state -> pointer rule). The
former "Phase-1 done / DQE FROZEN / Batch-2 4·4 / Batch-3 skeletons" header and its collapsed version
changelog have been removed here rather than re-dated; the current phase is not restated in this document
while its canonical home is undecided.

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

Under [`.claude/skills/`](../../.claude/skills/) — all `disable-model-invocation: true`. **Per-skill current
version and eval-pass status ->** the canonical status owner (**PENDING decision D-1**); the machine roster of
record is [skills-registry.yaml](skills-registry.yaml). (The inline "v0.2.0 / v0.3.0" version figures and the
self-reported eval counts that stood here are **stale** per the state report — a stale value becomes a
pointer, never a freshly-invented number, so they are not re-stated in this index.)

1. `documentation-quality-evaluator` — grades every other skill (built first). +HF-13/14a/14b/15, HF-12A–E, non-compensatory scoring, two-layer reader, structured verdict, 5 signal checkers.
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

## Next

For the batched creation plan (Batch 0→5), the definitions of done, and what we deliberately don't build,
see [creation-roadmap.md](creation-roadmap.md).

**Current progress / next-step status ->** the canonical status owner (**PENDING decision D-1**). The former
"Next (Batch 3 v0 skeletons BUILT; Batch 4/5 atoms next)" narrative (source README.md lines 81-102) — the
Batch-2.5 integration sprint, the Track A/B chains, the interface freeze, and the Batch-3 skeleton write-up —
is batch-progress state and is not re-asserted in this stable index. The report cross-references it carried
are listed in the rewrite-provenance unresolved-content ledger; whether those reports join this index is
**PENDING decision D-4** (README index scope), which is not decided here.
