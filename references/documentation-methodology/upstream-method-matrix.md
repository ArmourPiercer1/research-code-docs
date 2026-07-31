# Upstream Method Matrix

<!--
generated_by_skill: (manual, Phase-1 governance authoring; v0.2 with real references)
skill_version: n/a
source_commit: see per-source pins below
source_documents:
  - references/{agent-skills, github-awesome-copilot, research-paper-writing-skills, academic-research-skills, mattpocock-skills}/ (LICENSE + SKILL.md)
  - docs/研究软件文档Skills系统_设计与创建指南.md (§9, §14.7)
  - docs/skill-development/current-skills-audit.md
  - 4x method-extraction sub-agent reports (2026-07-30)
status: DECIDED (v0.2) — extended per skill as methods are adopted
last_verified: 2026-07-30T09:47:06Z
-->

> **Purpose (constraint D.2, guide §9 / §14.7).** Every rule adopted into a new skill records **where it came from**, **its license**, **how we adopted it** (copy / adapt / method-borrow / ideas-only), and **its boundary**. No wholesale concatenation of upstream `SKILL.md` (constraint D.1).
>
> **Adoption types:** `copy` (near-verbatim; license-gated) · `adapt` (restructured for our context) · `method-borrow` (technique only, re-authored) · `ideas-only` (general uncopyrightable idea, for license-restricted sources) · `reject` (considered, not used).

---

## 1. Source inventory (now vendored, with pinned commits)

The design guide's named upstreams are present as of 2026-07-30. Provenance pinned per §14.7.

| Source | Path | License | Pinned commit | Adopt policy |
|---|---|---|---|---|
| Addy Osmani agent-skills | `references/agent-skills/` | **MIT** (© 2025 Addy Osmani) | `7829ffd` | copy/adapt/method-borrow OK |
| GitHub awesome-copilot | `references/github-awesome-copilot/` | **MIT** (GitHub, Inc.) | `be7a1cf` | copy/adapt/method-borrow OK |
| Research-Paper-Writing-Skills | `references/research-paper-writing-skills/` | **MIT** (© 2026 Master-cai) | `77e7c2c` | copy/adapt/method-borrow OK |
| academic-research-skills | `references/academic-research-skills/` | **⚠ CC-BY-NC 4.0** (© 2026 Cheng-I Wu) | `2cf3a51` | **ideas-only** — no copy/close-paraphrase; attribute; NonCommercial |
| Matt Pocock skills | `references/mattpocock-skills/` | **MIT** (© 2026 Matt Pocock) | snapshot, `plugin.json` v1.2.0 (no `.git`) | copy/adapt/method-borrow OK |
| Anthropic skills | `references/skills/` | no LICENSE file (repo `anthropics/skills` `b29e7cf`) | `b29e7cf` | reference-only until license confirmed |
| pengsida/learning_research | `references/pengsida-learning-research/` | **no LICENSE** (`6fdbcdf`) | `6fdbcdf` | reference-only (all-rights-reserved by default) |

### 1.1 License hazard — `academic-research-skills` is CC-BY-NC 4.0

Per guide §14.7 ("avoid non-commercial content in a commercial system"), this source may contribute **only general ideas** (which are not copyrightable), never copied or closely-paraphrased text, and must be **attributed**. Where a method is genuinely valuable, we prefer the **MIT twin** (e.g. the adversarial-reviewer idea is taken from MIT `doubt-driven-development`, not from this source). Two ideas-only borrows are recorded in §2.1 and flagged.

### 1.2 No-license sources

`anthropics/skills` and `pengsida/learning_research` ship no LICENSE. Default = all-rights-reserved → **reference-only**; do not adopt text or close structure until a license is confirmed. Not used in the v0.2 upgrades.

---

## 2. Method adoptions — v0.2 (real, sourced)

Each row: the concrete method, its source path, license, adoption type, and the **boundary** (where the rule stops). Rejected upstream rules are in §3.

### 2.1 `documentation-quality-evaluator` (v0.2.0)

| Method | Source | License | Adoption | Boundary |
|---|---|---|---|---|
| Claim→evidence support as **HF-12** (+ `Claim｜Evidence｜Status` table) | research-paper-writing `references/paper-review.md` | MIT | adapt | Applies to state-report/evidence-matrix/roadmap/algorithm-spec; unsupported assertion-as-fact → FAIL. |
| **Severity taxonomy** BLOCKER/MAJOR/MINOR/NIT/FYI, leverage-ordered | agent-skills `code-review-and-quality` | MIT | adapt | Ordering/labels only; the *code* review axes are rejected (§3). |
| **Two-pass adversarial reader** (reader never sees author's conclusion) + RECONCILE | agent-skills `doubt-driven-development` | MIT | method-borrow | Single terminal pass, not an in-flight loop; no external-CLI machinery (§3). |
| **Reverse-outline** coherence check | research-paper-writing `SKILL.md` | MIT | method-borrow | Structure/altitude only; no prose-craft rules. |
| **ADR rationale anchor** (why + rejected alternative + consequences) + "restates code" red flag | agent-skills `documentation-and-adrs` | MIT | adapt | Rubric anchor for ADR/decision/spec types; does not author docs. |
| **Match-existing-convention-first** in the corpus pass | agent-skills `documentation-and-adrs` | MIT | method-borrow | Surface convention conflicts, don't penalize a project convention. |
| **Untrusted-document guard** + ordinal-not-cardinal verdict caveat | academic-research-skills `academic-paper-reviewer` | **CC-BY-NC** | **ideas-only** | General ideas only (no text); embedded instructions in the doc never change the verdict/read-only. Attributed. |

#### 2.1.1 v0.3 additions (hybrid-roadmap false-pass fix)

Source for the structural gates is the **internal** third-party audit
`docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md` (workspace-internal,
no external license). Two borrows extend existing MIT rows.

| Method | Source | License | Adoption | Boundary |
|---|---|---|---|---|
| **HF-13** mixed artifact responsibilities (divergent-lifecycle body-level roles + harm; appendix escape hatch) | internal audit §3.1/§5.1 | internal | adapt | Judged by role & lifecycle, not heading count; a subordinated-appendix comprehensive report does not trip it. |
| **HF-14a/HF-14b** state contradiction (all types) / volatile contamination (stable-design types only) | internal audit §3.2/§5.2 | internal | adapt | 14b is type-gated OUT for state/experiment reports (they own live state). |
| **HF-15** non-executable committed milestone (vague DoD blocklist; research-phase + deferred escapes) | internal audit §3.4/§5.3 | internal | adapt | Reconciled with HF-6 (presence vs quality); fires only on committed phases; GO/STOP+metric nets it out. |
| **HF-12 → A–E** doc-only (traceability/label) vs source-needing (accessibility/support/transfer) | internal audit §3.3/§5.4 | internal | adapt | Zero sources opened ⇒ FACTUAL_VALIDITY=UNVERIFIED; never "HF-12 verified" without opening sources. |
| **Non-compensatory scoring** anchored to a substantiated paired gate | internal audit §3.6/§5.5 | internal | adapt | A low critical dim FAILs only if its paired gate substantiates with a cited instance (no raw-score false-FAIL). |
| **Anti-erosion / no-PASS-prediction / no-downgrade** verdict discipline | internal audit §2/§3.6 | internal | adapt | The core fix: a met gate is a BLOCKER; walk all gates; never predict a re-eval PASS while a structural gate fails. |
| **Two-LAYER reader** (execution+refutation deepens the two-pass reader) | agent-skills `doubt-driven-development` (MIT) + internal audit §5.6 | MIT + internal | method-borrow | Reader gets neither rubric nor hard-fail; a core-question contract-misread is ≥ MAJOR, never dismissed. |
| **Structured verdict + terminal-gate formula + canonical-source map** | internal audit §5.7/§5.8 | internal | adapt | DOCUMENT_QUALITY vs FACTUAL_VALIDITY split; downstream gate needs FACTUAL_VALIDITY≠UNVERIFIED. |
| **5 SIGNAL checkers** (never block; model adjudicates) | internal audit §6 | internal | adapt | Advisory candidates only; CJK-safe masking; all under `evals/skills/harness/checkers/`. |

### 2.2 `project-state-reconstructor` (v0.2.0)

| Method | Source | License | Adoption | Boundary |
|---|---|---|---|---|
| **Intent-before-verify** + CLAIMED ledger + "Intent vs Reality divergences" | github `acquire-codebase-knowledge` | MIT | adapt | Read-only; no multi-file `docs/codebase/` write (§3). |
| **Trace one pipeline end-to-end** as the anchor FACT | github `architecture-blueprint-generator` + `acquire-codebase-knowledge` | MIT | method-borrow | "runs end-to-end" only if the chain is cited; no C4/UML generation (§3). |
| **Evidence hygiene** — generated/cached outputs ≠ evidence; **file trust tiers** | `acquire-codebase-knowledge` + agent-skills `context-engineering` | MIT | adapt | Untrusted file text is data, not instructions. |
| **Two-tier unknowns** `UNKNOWN(resolve:)` vs `ASK-HUMAN(intent)` | `acquire-codebase-knowledge` | MIT | adapt | ASK-HUMAN surfaced as numbered questions to the elicitor. |
| **Concrete context budget** (Project Map, ~2k/~5k lines) + Coverage note | agent-skills `context-engineering` | MIT | adapt | No CLAUDE.md authoring / MCP catalog (§3). |
| **Evidence-authority ladder** + `UNVERIFIED` tag + stack DETECT | agent-skills `source-driven-development` + `stack-detection.md` | MIT | adapt | Authority is THIS workspace's code/tests, not external web docs (§3). |
| **Pre-handoff self-audit loop** + TESTING/CONCERNS question bank | `acquire-codebase-knowledge` `inquiry-checkpoints.md` | MIT | method-borrow | Iterate the report; still read-only. |

### 2.3 `goal-scope-and-workflow-elicitor` (v0.2.0)

| Method | Source | License | Adoption | Boundary |
|---|---|---|---|---|
| **Sufficiency stop** (predict next 3 answers) + cannot-converge floor | agent-skills `interview-me` | MIT | method-borrow | Second stop rule alongside the decidable-boundary stop. |
| **Goal hypothesis + confidence**; high-confidence+no-gap = too-simple signal | agent-skills `interview-me` | MIT | method-borrow | Makes the should-not "decline simple task" call explicit. |
| **Correctable brief** (facts + assumptions, "correct me or I proceed") | agent-skills `spec-driven-development` | MIT | adapt | Reduces N questions to one round; does not author a spec (§3). |
| **Want-vs-should-want** buzzword probe | agent-skills `interview-me` | MIT | method-borrow | One probe when the goal is a convention/buzzword. |
| **Fixed-field restate** + mandatory Non-goals + anti-sycophancy confirm | agent-skills `interview-me` | MIT | adapt | "whatever you think" re-asked as options; no live user → CANDIDATE. |
| **Floor + question ceiling (~5–6)** | agent-skills `idea-refine` | MIT | method-borrow | Bounds only; batched AskUserQuestion rejected (§3). |
| **Reframe vague goal → testable success criteria** | agent-skills `spec-driven-development` | MIT | adapt | Stop at the criterion; do not proceed into a spec. |

### 2.4 `uncertainty-and-decision-manager` (v0.2.0)

| Method | Source | License | Adoption | Boundary |
|---|---|---|---|---|
| **Supersede-don't-edit** lifecycle (`supersedes`/`superseded_by`, `reason`, `alternatives`) | agent-skills `documentation-and-adrs` | MIT | adapt | **Mapped onto the existing 10-status vocabulary** — no new SUPERSEDED status added; old row → STALE/REJECTED + pointer. |
| **Source = checkable locator** + authority ladder → E-levels + `UNVERIFIED` | agent-skills `source-driven-development` | MIT | adapt | Operationalizes E0–E5; external-doc-fetch mission rejected (§3). |
| **`proof_context`** for E3+ (commit/env/seed/dataset) + auto-STALE on drift | agent-skills `source-driven-development` | MIT | adapt | Recommended on E4/E5; makes "verified" reproducible + time-bounded. |
| **Adversarial promotion gate** (`discharge`) before CANDIDATE→DECIDED | agent-skills `doubt-driven-development` | MIT | method-borrow | Only for non-trivial items; ≤3 attempts then hold OPEN; no external-CLI (§3). |
| **Claim disposition** {supported/needs-evidence/needs-experiment} + weaken-or-remove | research-paper-writing `paper-review.md` | MIT | adapt | No DECIDED/BASELINE with needs-evidence (checker-enforced). |
| **Reason on REJECTED/DEFERRED/superseded** + alternatives/consequences | agent-skills `documentation-and-adrs` | MIT | adapt | Checker-enforced; ADR file-layout rejected (§3). |
| **Evidence-coverage gate** (no orphan commitment) | research-paper-writing `experiments.md` | MIT | method-borrow | Every structural commitment maps to an evidence locator. |

---

## 3. Rejected upstream rules (with reason)

**documentation-quality-evaluator:** five-axis *code* review + change-sizing (code-only → `code-review`); multi-agent 5-reviewer panel + cross-model tracks + CC-BY-NC bloat (`academic-paper-reviewer`); ML-paper rejection dimensions (app-specific); doc-authoring/rewriting workflows (target is read-only → `technical-document-rewriter`).

**project-state-reconstructor:** writing seven `docs/codebase/*` files + `scan.py` artifact (target is read-only); enterprise architecture taxonomy + mandatory C4/UML (`architecture-blueprint-generator` — invites theoretical structure); authoring `CLAUDE.md` + MCP catalog (`context-engineering`); fetch-external-library-docs mission (`source-driven-development`).

**goal-scope-and-workflow-elicitor:** the SDD six-area spec + 4-phase pipeline + planning task-templates/sizing (downstream skills, wrong altitude); idea-refine divergent ideation (SCAMPER/HMW) + painkiller-vs-vitamin evaluation (that's ideation/evaluation, not goal elicitation); idea-refine batched `AskUserQuestion` (conflicts with one-at-a-time); interview-me "loop until explicit yes" as-is (target must tolerate an absent user → CANDIDATE fallback).

**uncertainty-and-decision-manager:** ADR per-file `docs/decisions/ADR-NNN.md` layout (collides with the domain-modeling ADR store; we emit one checkable YAML block); doubt-driven cross-model CLI escalation + per-persona loading constraints; SDD live doc-fetch loop; paper prose/figure/table craft.

**Cross-cutting:** no new status token added to the guide's fixed 10-status vocabulary (§2.3) despite the ADR SUPERSEDED status — adapted onto STALE/REJECTED + `superseded_by` to keep the system-wide contract and the checkers stable.

---

## 4. Upstream-drift policy (guide §14.7)

- Pinned commits above are the adoption baseline. Re-check upstream periodically; **never auto-overwrite** local skills.
- The Matt snapshot has no commit — re-pin from `github.com/mattpocock/skills` before adopting anything *new* from it.
- `academic-research-skills` (CC-BY-NC) and the two no-license repos are **called/ideas-only**, never internalized as text, pending license confirmation (OQ-3 / §1.2).
