---
name: uncertainty-and-decision-manager
description: Maintain a decision register that tags every research/design item with a status (FACT/VERIFIED/DECIDED/BASELINE/HYPOTHESIS/CANDIDATE/OPEN/DEFERRED/REJECTED/STALE) and an evidence level (E0-E5), keeping candidates, hypotheses, and open questions strictly separate from decided facts and enforcing that only E3+ (in-project proof) may be called "verified". Use when a flow must record/track decisions and uncertainty, or facts and guesses are getting mixed. NOT for stable domain terminology (domain-modeling) or plain code facts.
disable-model-invocation: true
---

<!--
skill_version: 0.2.0
status: experimental (orchestrator/wayfinder-only; no auto-trigger until evals pass)
generated_by_skill: manual authoring; v0.2 upgraded from real references
source_commit: addyosmani/agent-skills@7829ffd (MIT); Master-cai/Research-Paper-Writing-Skills@77e7c2c (MIT); mattpocock/skills@snapshot(v1.2.0)
source_documents:
  - references/agent-skills/skills/documentation-and-adrs/SKILL.md (MIT)
  - references/agent-skills/skills/source-driven-development/SKILL.md (MIT)
  - references/agent-skills/skills/doubt-driven-development/SKILL.md (MIT)
  - references/research-paper-writing-skills/ (MIT — claim-evidence map)
  - docs/研究软件文档Skills系统_设计与创建指南.md §2.3
  - references/documentation-methodology/upstream-method-matrix.md §2.4
last_verified: 2026-07-30T09:47:06Z
-->

# Uncertainty & Decision Manager

> **Experimental · orchestrator/`wayfinder`-only.** The system's single source of truth for what is *uncertain*: hypotheses, candidates, open questions, and the evidence behind each decision.
> **v0.2** adopts the ADR supersede-lifecycle + rationale fields (documentation-and-adrs), a source-authority ladder + `UNVERIFIED` flag (source-driven-development), an adversarial promotion gate (doubt-driven-development), and the claim→evidence disposition (research-paper-writing) — all MIT, attributed in `upstream-method-matrix.md` §2.4.

## Purpose

Prevent the most damaging research-doc failure — **candidate/hypothesis written as decided fact**. Every item gets an explicit **status**, **evidence level**, and a **checkable source**; only capabilities proven **in this project (E3+)** may be written as "verified"; every reversal leaves an audit trail.

## Trigger conditions

Engage when:
- A control flow needs to **record or update decisions, hypotheses, candidates, or open questions**, **or**
- A produced artifact **mixes facts with guesses** and they must be separated and tagged, **or**
- `wayfinder` (if installed) needs its decision tickets backed by an inline register.

## Do-not-trigger conditions

- **Stable, decided domain terminology / relationships** → `domain-modeling` (owns the glossary + ADRs). An item moves here → there once it is `DECIDED`.
- **Plain code-behavior facts** → state report / tests, not the uncertainty register.
- A **simple, certain task** with nothing uncertain to track.
- The user wants a **decision made for them** — this skill records decisions; it does not make them.

## Inputs

- The goal/scope note + open-decision list (from `goal-scope-and-workflow-elicitor`).
- The evidence matrix (from `research-evidence-synthesizer`, later) and any prototype/experiment results.
- The existing `decision-register.md` (if any).

## Register entry fields

Each entry (a `## Register` fenced ```yaml list item): `id`, `statement`, `status`, `evidence` (E0–E5), `source`, `disposition`, `decided_by`, `last_verified`, and when applicable `proof_context`, `supersedes`/`superseded_by`, `reason`, `alternatives`, `notes`.

## Workflow

1. **Ingest items.** One-line statement each.
2. **Assign status + evidence level with a checkable source.** *(source-driven-development)* `source` must be a **locator you can re-open**, never a bare name: `file:line` / `test-id` / `experiment-run-id` / `bench-artifact-path` / `DOI#section`. Rank by authority → level:
   - in-project passing test / reproducible benchmark / stable+regression → **E3–E5**
   - official library/API doc or standard → **E2**
   - peer-reviewed paper / sibling-domain result (indirect) → **E1–E2 (capped at E2)**
   - preprint / blog / forum → **E1**
   - model memory / "I recall" → **E0, tagged `UNVERIFIED`**, never rendered as fact.
3. **Enforce the verified threshold.** Only `E3+` may be phrased "verified" downstream (HF-10). A published result is not in-project proof.
4. **Bind E3+ to its reproducibility conditions.** *(source-driven-development)* Any `E4/E5`/`VERIFIED` entry carries `proof_context`: commit SHA + env/seed + dataset/split + the metric value. If any element changes, the entry **auto-transitions to `STALE`** until re-proven; a STALE verified claim may not be cited downstream as verified.
5. **Promotion gate — never promote silently.** *(doubt-driven-development)* Before `CANDIDATE`/`HYPOTHESIS → DECIDED`/`BASELINE` for a **non-trivial** item (branching logic, boundary crossing, an unverifiable property, or irreversible blast radius), run **one adversarial disproof attempt** (a fresh-context skeptic, or a failing check) and record `discharge: {attempted, findings, disposition}`. Unresolved after up to 3 attempts → hold `OPEN`; do not force (HF-3). Record `decided_by` + date on promotion.
6. **Disposition every item.** *(research-paper-writing)* `disposition ∈ {supported, needs-evidence, needs-experiment}`. An item that loses its supporting evidence is **downgraded** (→ `HYPOTHESIS`/`OPEN`) or **removed** (→ `REJECTED`), never left `DECIDED`. Gate: no `DECIDED`/`BASELINE` carries `needs-evidence`.
7. **Reverse by supersede, not by edit.** *(documentation-and-adrs)* A `DECIDED`/`BASELINE`/`VERIFIED` item is never edited to a contradictory value. Append a **new** entry with `supersedes: <old-id>`; mark the old entry `STALE` (or `REJECTED`) with `superseded_by: <new-id>` and a **`reason`**. The register is append-only for decided items. Every `REJECTED`/`DEFERRED`/superseded entry **requires a `reason`**; `DECIDED` items may list `alternatives` (rejected candidate ids + one-line why).
8. **Respect the `domain-modeling` boundary.** Unstable items live here; when an item reaches `DECIDED` and is a stable term/relationship, hand it to `domain-modeling` for the glossary/ADR and mark it `→ glossary` here.
9. **Keep OPEN questions alive** (HF-7); if closed, record the resolution.

## Quality gates

- Every row has **status + evidence level + a checkable `source` locator + `disposition`**.
- No item at E≤2 described as "verified"; no paper cited as in-project fact (HF-10). `E0`/memory items tagged `UNVERIFIED`.
- No `CANDIDATE`/`HYPOTHESIS` rendered as `DECIDED`/`FACT` without a recorded `discharge` + `decided_by` (HF-3).
- Every `REJECTED`/`DEFERRED`/superseded entry has a `reason`; no decided item silently overwritten (both rows survive a reversal).
- No `OPEN` item dropped between versions (HF-7). No `DECIDED`/`BASELINE` structural commitment without an evidence locator (coverage gate).
- The `domain-modeling` boundary is respected in both directions.

## Anti-inflation red flags (challenge these before recording)

| Rationalization | Reality |
|---|---|
| "I'm confident about this result." | Confidence is not evidence — needs a locator + level. |
| "The paper proves it." | Sibling-domain paper is **E2**, not in-project proof. |
| "It passed once." | Without `proof_context` (commit/seed/data) it is not reproducible → not E4. |
| "We basically decided." | Until `discharge` + `decided_by` recorded, it stays CANDIDATE. |

## Outputs

- `decision-register.md` — front-matter + a `## Register` fenced ```yaml list (machine-checkable). Template: `references/templates/decision-register.template.md`.

## Handoff rules

- Feeds `research-software-roadmap-author` (phases reference register items + status).
- Feeds `scientific-software-architect` / `algorithm-technical-spec-author` (only `DECIDED`/`BASELINE` items become structural commitments).
- Decided stable terms → `domain-modeling`.

## Failure modes

- **Conflicting evidence** → keep `OPEN` with both sides recorded; do not force a decision.
- **Pressure to mark something done** → hold at the evidence level; escalate the gap as an `OPEN`/`needs-experiment` item.

## References to load

- `references/agent-skills/skills/documentation-and-adrs/SKILL.md` (MIT — supersede lifecycle, alternatives/consequences). Adapted onto the existing 10-status vocabulary (no new status added); see matrix §2.4.
- `references/agent-skills/skills/source-driven-development/SKILL.md` (MIT — source-authority ladder, `UNVERIFIED`, version pinning).
- `docs/skill-development/system-architecture.md` §7 (status + evidence definitions).

## Scripts to run

- `evals/skills/harness/checkers/register_check.py <decision-register>` — validates status/evidence legality, checkable source, `disposition`, `reason` on REJECTED/DEFERRED/superseded, and flags VERIFIED/FACT at E≤2.
- `evals/skills/harness/checkers/run_checks.py <decision-register>` — front-matter + status-vocabulary checks.
