# Canonical-Source Map

<!--
generated_by_skill: (manual, Phase-1 governance authoring; v0.3 addition)
skill_version: n/a
source_commit: n/a
source_documents:
  - docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md §5.7
  - docs/skill-development/system-architecture.md §6 (canonical homes)
status: DECIDED (v0.3 shared reference)
last_verified: 2026-07-30
-->

> Shared reference for `documentation-quality-evaluator`. It grounds **HF-14b (volatile-state
> contamination)** and the **canonical-source / maintainability** rubric dimensions: "this fact
> belongs in X, not copied into a stable doc" is decided against this table, not by feel. A stable
> design doc (roadmap / architecture / vision / ADR / algorithm-spec) that **embeds** a fact whose
> canonical home is dynamic (code/tests/CI/status) — without a **timestamped pointer** to that single
> source — is contaminating itself and will drift.

| Information type | Canonical source | If it appears in a stable doc |
|---|---|---|
| Current implementation behavior | code + tests | pointer only (`see src/…`), never a restated fact |
| Current progress / % done | `status` / issue tracker | pointer + timestamp, or omit |
| Test status / counts / "all green" | CI / test report | pointer + `as-of <date>`; a bare "59 tests green" in a roadmap is HF-14b |
| Architecture *rationale* (why) | ADR | the roadmap links the ADR; it does not re-argue it |
| Long-term goal / vision | vision / overview doc | one stable statement; not mixed with live status |
| Phase / milestone plan | roadmap | the roadmap owns this — but only the *plan*, not live completion state |
| Algorithm math / spec details | algorithm spec | roadmap links it; does not inline the derivation |
| Experiment results / metrics | experiment report / registry | pointer + run id; not a floating number |
| Literature-transfer basis | research basis / evidence map | pointer; transfer assumptions labeled (HF-12D/E) |
| Session / interview decisions | decision register (ADR) | a `用户决定 (本轮)` block inside a roadmap is residue (HF-13 + agent_session_residue) |

## How to use it (evaluator)

1. For each **volatile fact** in a stable-design doc, look up its canonical source here.
2. If the fact is **restated** (not a pointer) and carries **no `as-of <date>` / single-source
   reference** → candidate **HF-14b**. If two such restatements disagree → **HF-14a**.
3. A doc whose type **is** the canonical source for that fact (a state report owns live counts; an
   experiment report owns metrics) is exempt from HF-14b for those facts — check HF-14a (internal
   contradiction) instead.
4. Feed the maintainability + canonical-source rubric dimensions from the count of un-pointered
   restatements (drift risk already realized = low score).
