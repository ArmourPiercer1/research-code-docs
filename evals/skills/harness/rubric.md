# Soft Rubric — 8 dimensions (0–100 weighted) + artifact-specific rubrics

<!--
generated_by_skill: (manual, Phase-1 governance authoring; v0.3 adds non-compensatory gating, roadmap rubric, two-layer reader)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/skill-development/quality-control-plan.md §1.2, docs/研究软件文档Skills系统_设计与创建指南.md §14.10
  - docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md §5.5/§5.6 (v0.3)
status: DECIDED (v0.3 rubric)
last_verified: 2026-07-30
-->


Scored **only after** all applicable hard gates pass (`hard-fail.md`).
Each dimension is scored 0–5, multiplied by its weight, summed, normalized to 100.
**Pass line:** total ≥ 75 **and** no single dimension < 2.5/5 **and** the non-compensatory rule (below) holds.

| Dim | Weight | 0–1 (bad) | 3 (ok) | 5 (excellent) |
|---|---:|---|---|---|
| **Factual accuracy** | 20 | Claims untraceable or contradicted by code/tests. | Most claims trace; a few unverified but labeled. | Every non-trivial claim traces to code/tests/experiment/authoritative source. |
| **Information architecture** | 15 | Content in the wrong doc type; boundaries blurred; **many roles crammed in one file**. | Mostly right home; minor bleed. | Each fact in its canonical doc (arch §6); clean boundaries; no duplication. |
| **Actionability** | 15 | No next step, or steps not doable. | Next steps present, some vague. | Concrete next steps **with measurable acceptance criteria**. |
| **Evidence traceability** | 15 | Claims with no source or level. | Sources for key claims; levels partial. | Every claim cites source **and** evidence level (E0–E5) **and** a support/transfer label. |
| **Uncertainty expression** | 10 | Guesses stated as facts. | Some unknowns flagged. | Unknowns/hypotheses/candidates explicitly labeled; DECIDED vs CANDIDATE kept separate. |
| **Reader fit** | 10 | Needs the chat history to parse. | A careful reader can follow. | A no-context reader of the target role can act immediately. |
| **Maintainability** | 10 | Fact duplicated across docs; volatile state copied into stable docs; will drift. | Mostly single-source. | Strict canonical-source discipline (`canonical-source-map.md`); change-in-one-place. |
| **Concision** | 5 | Padding, repetition, off-budget. | Reasonable length. | Tight; nothing removable without loss; within context budget. |

## Scoring formula

```
raw   = Σ (score_dim × weight_dim)          # max = 5 × 100 = 500
total = raw / 5                             # normalized to 0–100
pass  = (all applicable hard gates pass)
        AND (total ≥ 75)
        AND (min dimension score ≥ 2.5/5)
        AND (non-compensatory rule holds)   # v0.3, see below
```

## Non-compensatory rule (v0.3) — breadth may not buy back a structural failure

Certain dimensions are **critical**: a high total must not rescue them. But to avoid over-firing on
"I felt it was a 3", the non-compensatory FAIL is **anchored to a substantiated paired hard gate**, not
to the raw score alone:

> If a **critical dimension scores < 3.5/5**, the evaluator must **re-examine its paired hard gate with
> a cited instance**. It is a **verdict-level FAIL** only if that paired gate **substantiates** (a
> concrete line/section is cited). A low critical dimension with no substantiating instance is a MAJOR,
> not a FAIL.

| Critical dimension | Paired hard gate (must substantiate to FAIL) | Base-dim it maps to (non-roadmap types) |
|---|---|---|
| Definition-of-Done clarity | HF-15 (vague committed DoD) | Actionability |
| State consistency | HF-14a (contradiction) | Factual accuracy |
| Canonical-source discipline | HF-14b (volatile contamination) | Maintainability |
| Claim support | HF-12A/E (untraceable / unlabeled) | Evidence traceability |
| Reader actionability | Reader Layer-2 failure (below) | Reader fit |

This is the fix for the v0.2 false-pass: the eoopt roadmap's Information-architecture was rated "强"
(strong) and its breadth read as completeness, masking that DoD, state-consistency, and canonical-source
were all failing. Under this rule, those three each substantiate their paired gate (HF-15 on 阶段3,
HF-14a on 59-vs-69, HF-14b on the embedded counts) → verdict FAIL regardless of total.

---

## Roadmap-specific rubric (applied when artifact_type = roadmap)

The 8-dim base rubric is the shared floor; a roadmap is additionally scored on these. Dimensions marked
**[NC]** are the critical/non-compensatory ones for roadmaps.

| # | Roadmap dimension | What "good" means |
|---|---|---|
| 1 | Goals & non-goals | Both stated; scope boundary explicit. |
| 2 | Stage-granularity consistency | Phases are comparably sized; one phase isn't 5 algorithm families + shared components + open research. |
| 3 | Dependencies & order | Each phase names prerequisites; ordering justified. |
| 4 | Deliverable clarity | Concrete artifacts per phase. |
| 5 | **Definition of Done [NC]** | Each *committed* phase has a **measurable** DoD (not "算例届时定"). |
| 6 | Research-uncertainty expression | Research phases state question + minimal experiment + metric + GO/MODIFY/STOP. |
| 7 | Decision-gate & fallback | "If the gating experiment fails, the route changes to …" is present. |
| 8 | **State consistency [NC]** | No contradictory counts/status across sections. |
| 9 | **Canonical-source management [NC]** | Volatile state is pointed-to, not copied into the roadmap. |
| 10 | Maintainability | Single-source discipline; low drift risk. |
| 11 | **Reader actionability [NC]** | A fresh reader can name the next executable step + its DoD + decided-vs-candidate. |
| 12 | Evidence ↔ commitment match | A phase committed as work has evidence proportional to the commitment (candidate methods are labeled candidate, not written as committed). |

---

## Reader-test protocol (feeds "Reader fit" + HF-8) — **two layers** (v0.3)

Give a fresh sub-agent **only** the produced artifact — **no chat history, no author intent, and (for
the reader role) not even this rubric or hard-fail.md** (handing it the grading criteria or the
conclusion biases it toward agreement). See `make_grading_injection.py --role reader`.

**Layer 1 — comprehension + location.** From the artifact alone:
1. What is the goal / target of this work?
2. What is the single **primary responsibility** of this document? Who is the target reader?
3. What is the current state (FACT vs UNKNOWN), and **where is the canonical source** of that state?
4. Where are the key terms defined? Where do related ADR / spec / experiment reports live?
5. What are the open questions?

**Layer 2 — execution + refutation** *(doubt-driven-development, MIT; deepened per audit §5.6)*:
6. What is the **next immediately-executable** piece of work, and **how will we know it's done** (DoD)?
7. Which methods/algorithms are **DECIDED** vs merely **CANDIDATE**?
8. Which load-bearing claims **lack support** (no handle, or a topically-related-only source)?
9. Which facts will go **stale** fastest?
10. Which sections **do not serve** the document's stated goal?
11. If the gating/precondition experiment **fails**, how does the route change?

If the reader cannot answer Layer-1 Q1–Q4 → **HF-8 fail**. If it cannot answer the Layer-2 **core**
questions (6 next-step+DoD, 7 decided-vs-candidate, 11 fallback) → **Reader-actionability fails** →
feeds the non-compensatory rule.

**RECONCILE — contract-misread maps to *doc-defect severity*, never "reader error, dismiss."** Sort each
returned finding into **contract-misread** / **actionable** / **valid trade-off** / **noise**. Rule
(sharpened, v0.3): a `contract-misread` on any **core** Layer-1/Layer-2 question is **at minimum MAJOR**;
if it concerns the **canonical state-source or a DoD**, it feeds the **non-compensatory FAIL**. The
evaluator must **not** downgrade a misread by claiming it "knows the author's intent" — if the misread
stems from the doc being unclear, that is the defect. (In v0.2 the reader correctly caught that the
Context section reported only phase-1 done while the body was at phase-3; that was wrongly demoted to a
MINOR "contract-misread". Under this rule it is a MAJOR state-source defect.)

## Reverse-outline coherence check (feeds Information architecture) *(research-paper-writing, MIT)*

Extract the doc's thesis/goal, then each section's topic sentence + supporting points; map every section
to the stated goal and every supporting point to its section. An **orphan section** (no mapping) or a
**buried/missing thesis** caps the Information-architecture dimension and is reported as a MINOR/MAJOR
finding. When many sections map to *different* goals (not the stated one), that is an **HF-13** signal,
not just an IA cap.

## ADR / decision / algorithm-spec rationale anchor *(documentation-and-adrs, MIT)*

For ADR, decision-register, and algorithm-spec artifact types: the doc must record **why** (context +
constraints + trade-offs), **≥1 rejected alternative with its reason**, and **consequences** — not just
the *what*. A decision stated without why/alternatives, or a doc that **restates code/behavior instead of
explaining intent**, caps the relevant dimension at ≤ 2/5.

## Finding severity taxonomy (for the emitted fix list) *(code-review-and-quality, MIT)*

Label and order every finding by leverage — one structural issue is surfaced before any nits:

| Label | Meaning |
|---|---|
| `BLOCKER` | an applicable hard-gate failed (verdict is FAIL) — **may not be downgraded** (hard-fail.md anti-erosion rule) |
| `MAJOR` | a rubric dimension < 2.5/5, a failed reader **core** question, or a contract-misread on a core question |
| `MINOR` | a real but non-blocking quality issue |
| `NIT` | cosmetic / style |
| `FYI` | context, no action required |
