<!--
generated_by_skill: (manual, governance wrap-up per 2026-08-05 scope-correction directive)
skill_version: documentation-quality-evaluator 0.4.1 (FROZEN — advisory / profile-scoped)
source_commit: 975e930 (workspace HEAD at authoring; internal governance doc — no upstream)
source_documents:
  - docs/third-party-suggestions/Research-Code-Docs当前进展_阻塞项与下一阶段开发计划.md (the directive)
  - docs/skill-development/reports/dqe-v0.4.1-phase-e-canary-decision.md (the halted D-17 canary)
  - tests/corpus/blind-runs/phase-e-2026-08-05/ (canary evidence, preserved)
  - evals/skills/snapshots/{dqe-v0.3.0,dqe-v0.4.0-pre-d16,dqe-v0.4.1-candidate}/ (frozen bundles, preserved)
status: DECIDED (Step 1 governance wrap-up complete; Batch 2 entered)
last_verified: 2026-08-05
-->

# DQE v0.4.1 — Advisory Freeze + Batch-2 Entry (scope correction)

> **One line.** Per the 2026-08-05 directive we **stopped expanding the DQE test system**, **froze DQE
> v0.4.1 as an advisory / profile-scoped evaluator**, **resolved the halted D-17 canary by scoping the
> failing profile OUT** (→ `INCOMPLETE / unsupported-evaluation-profile`, *not* by building HF-REPRO),
> **deferred Phase E**, and **decoupled Batch 2** from "DQE becomes a universal terminal gate." Nothing was
> installed or pushed; no HF-1..15 threshold was changed; all canary evidence + snapshots are preserved.

## 0. Decision applied (verbatim from the directive)

```text
DQE_CURRENT_ROLE=ADVISORY_EVALUATOR
DQE_VERSION=0.4.1
DQE_STATUS=EXPERIMENTAL
DQE_TERMINAL_GATE_AUTHORITY=PROFILE_SCOPED
PHASE_E=DEFERRED
BATCH_2=UNBLOCKED
AUTO_TRIGGER=DISABLED
```

The judgement behind it: **DQE is already good enough as a human-supervised advisory evaluator to support
downstream Skills development; it is not yet good enough to be a universal automatic terminal gate for every
document type and profile — and that second goal should no longer block Batch 2.**

## 1. Why (root cause recap — the halted canary)

Phase E's 2-slot canary FAILED: on `BP-006-release` (a non-reproducible ResNet-50 experiment report under
`controlled + release-gate`) the frozen candidate emitted `GATE_DECISION=ALLOW` **×3 stably** against a
`BLOCK` gold — once even with `QUALITY_BAND=FAIL` + `READER_TEST=FAIL`. Root cause = **D-17: the
D-16 × OQ-REPRO=A collision.** D-16 made `GATE_DECISION` depend *only* on a hard-gate BLOCKER (rubric/reader
can no longer move the gate); OQ-REPRO=A (`HF_REPRO = NOT_ADOPTED`) had relied on the rubric non-compensatory
path + reader Layer-2 to BLOCK. D-16 severed that path → default ALLOW. The canary also proved **every
LLM-judged signal is unstable** (reader_test PASS/FAIL/PASS; HF-12A fires or not across runs), so any fix
that routes the gate through those signals inherits the jitter.

## 2. The resolution: scope OUT, don't fix now (closes D-17)

The earlier canary-decision report offered A/B/C — all of which *build* reproducibility machinery. The
directive **supersedes** that with a stricter, lighter move: **declare the profile unsupported.**

- `artifact_type: experiment-report` **∧** `provenance_policy: controlled` **∧** `decision_mode: release-gate`
  is now an **unsupported evaluation profile**. DQE emits `GATE_DECISION=INCOMPLETE` with
  `GATE_REASON=unsupported-evaluation-profile` and states plainly *"this evaluator is not validated for this
  profile."* The canary's stable **false-ALLOW becomes a safe INCOMPLETE.**
- This is a **profile-admission guard (Rule 0)** that sits **above** the D-16 gate rules 1–3 — it changes
  **no** HF-1..15 threshold, no rubric weight, and no gate-derivation rule. It is a *scope declaration*, not
  a quality judgement of the target.
- It is **more conservative than option C**: C would still evaluate the report and return INCOMPLETE only
  when reproduction elements are missing (needing a deterministic reproducibility checker). Scoping the whole
  profile out needs **no new checker** and honours "**do not adopt HF-REPRO**."

The real reproducibility-release contract (ADR-DQE-002 / HF-REPRO / a reproducibility checker / the 12-slot
canary / the 61-slot Phase E matrix) is **deferred** — it belongs to the future
`experiment-provenance-and-reproducibility` capability, not to perfecting DQE before Batch 2.

## 3. What changed (Step 1 — small, governance + one scope guard)

| File | Change |
|---|---|
| `.claude/skills/documentation-quality-evaluator/SKILL.md` | Advisory-freeze banner; new **Supported scope & profile admission** section; GATE_DECISION **Rule 0** (profile admission); `GATE_REASON` added to the verdict block; advisory/profile-scoped terminal-gate contract. Version stays **0.4.1** (freeze). |
| `evals/skills/harness/make_grading_injection.py` | `EVALUATOR_CONTRACT` mirrors Rule 0 + the unsupported-profile list + `GATE_REASON`; opening line relabelled advisory (v0.4.1). |
| `docs/skill-development/skills-registry.yaml` | DQE `role: advisory-evaluator` + `terminal_gate_authority: profile-scoped` + `supported_profiles` / `unsupported_profiles`; meta `batch2_gate` → **DECOUPLED**, new `phase_e` (deferred) + `v0_4_1_freeze`. |
| `docs/skill-development/creation-roadmap.md` | Scope-correction note; Batch 2 **decoupled** + reordered to build order (forensics → IA → lit-planner → evidence-synth) + light per-skill round; Phase E deferred. |
| `docs/skill-development/quality-control-plan.md` | §10 gate line updated to advisory/decoupled. |
| `docs/skill-development/reports/dqe-v0.4.1-phase-e-canary-decision.md` | RESOLVED banner (D-17 closed by scope-out; Phase E deferred). |

## 4. What was explicitly NOT done (per directive §6.1 / §10)

- **No** `ADR-DQE-002`, **no** `HF-REPRO` hard gate, **no** `reproducibility_contract_check.py`, **no**
  experiment-report complete/incomplete/invalid triad.
- **No** 12-slot canary, **no** new 61-slot Phase E matrix run.
- **No** HF-1..15 threshold / rubric weight / gate-rule (1–3) change.
- **No** new DQE fixtures; **no** re-judgement of the BP-006 gold (kept as canary evidence).
- **Nothing installed, nothing pushed, no live loader change, no auto-trigger.** DQE stays
  `disable-model-invocation: true` + `experimental`.

## 5. Preserved evidence (not deleted)

- Snapshots: `evals/skills/snapshots/{dqe-v0.3.0, dqe-v0.4.0-pre-d16, dqe-v0.4.1-candidate}/` (+ SHA-256
  manifests). NOTE: `dqe-v0.4.1-candidate` is the **pre-scope-guard canary bytes**; the live SKILL.md now
  carries the advisory guard on top of those bytes — the divergence is intentional (the snapshot is frozen
  evidence, the live skill is the working advisory version).
- Canary: `tests/corpus/blind-runs/phase-e-2026-08-05/` (`canary-summary.md`, `canary-raw.json`,
  `canary-metrics/`, `results/*.json`, `injections/`, `phase-e-plan.json`).
- Defect ledger D-17 + `dqe-v0.4.1-diagnostic-close.md` correction banner remain in place.

## 6. Batch 2 — entered

Unblocked and decoupled. Build order (lowest-risk / most-reused first):

1. **`workspace-forensics-and-inventory`** (read-only; `project-state-reconstructor` already depends on it) — **started in this pass.**
2. `document-information-architect` (directly addresses the original hybrid-doc disease).
3. `research-question-and-literature-planner` (thin scoping adapter over the L3 research stack).
4. `research-evidence-synthesizer` (consumes retrieved evidence; no retrieval).

**Light per-skill round** (NOT DQE's heavy corpus): 3 should-trigger · 3 should-not · 2 boundary/conflict ·
1 real shadow run · 1 no-context reader test · 1 no-skill comparison. Regression cases are added only after a
**real** failure appears. Eval posture = **DQE advisory report + an independent reviewer** (not a large
admission matrix).

## 7. Phase E restart preconditions (future promotion gate)

Revisit Phase E only when: **≥2 Batch-2 skills done** + **5–10 real downstream Skill outputs collected** +
**a real output exposes a new DQE failure mode** + **intent to promote DQE from advisory to a terminal
gate.** At that point the corpus should be **real downstream outputs**, not synthetic mutations.
