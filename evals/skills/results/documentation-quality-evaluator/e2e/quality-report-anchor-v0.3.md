<!--
generated_by_skill: documentation-quality-evaluator
skill_version: 0.3.0
source_commit: n/a (workspace is not a git repo; skill provenance = addyosmani/agent-skills@7829ffd, Master-cai/Research-Paper-Writing-Skills@77e7c2c, mattpocock/skills v1.2.0 snapshot)
source_documents:
  - evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md (TARGET under review)
  - evals/skills/harness/hard-fail.md
  - evals/skills/harness/rubric.md
  - evals/skills/harness/canonical-source-map.md
  - evals/skills/harness/checkers/run_checks.py (+ roadmap_stage_fields.py, artifact_role_mixing.py sources read)
status: FAIL (evaluation complete; DOCUMENT_QUALITY=FAIL, FACTUAL_VALIDITY=UNVERIFIED)
last_verified: 2026-07-30
-->

# Quality Report — eoopt 最终目标设计与开发路线图 (messy-hybrid-roadmap)

**Target:** `evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md`
**Artifact type:** roadmap (goal-design + development roadmap; self-declared at L11 "本文件是目标设计 + 路线图，不是实现计划") — evaluated as a **roadmap** with **hybrid contamination** (HF-13, see below).
**Mode:** terminal quality gate, fresh/no-project-context process, read-only w.r.t. the target.

---

## 0. Verdict block (machine-parseable — see bottom for the canonical copy)

`DOCUMENT_QUALITY=FAIL` · `FACTUAL_VALIDITY=UNVERIFIED` · `READER_TEST=FAIL` · `CHECKER_STATUS=COMPLETE` · `SOURCE_COVERAGE=0/64` · `BLOCKERS=[HF-9, HF-13, HF-14a, HF-14b, HF-15]`

This is a **structural FAIL from the document itself** (five doc-only hard gates substantiate). It is **not** an INCOMPLETE_EVALUATION: `FACTUAL_VALIDITY=UNVERIFIED` records that the cited sources could not be opened here, but per the skill's anti-erosion rule an unreadable-source state **cannot rescue a doc-only structural FAIL** and INCOMPLETE may not be emitted to dodge it.

---

## 1. Deterministic checker output (run, not eyeballed)

Command:
```
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe evals/skills/harness/checkers/run_checks.py \
  "evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md" --json
```
Process exit code **1** (expected: `hard_fail:true`). JSON (trimmed only in the `markdown_links` advisory list, which repeats one broken-link class ~40×):

```json
{
  "path": "evals\\skills\\task-quality\\fixtures\\dqe\\negative\\messy-hybrid-roadmap.md",
  "files_checked": 1,
  "hard_fail": true,
  "results": [{
    "hard": {
      "frontmatter": { "pass": false,
        "problems": ["no front-matter block found (need YAML '---' header or leading HTML comment)"] },
      "status_vocab": { "pass": true, "problems": [] }
    },
    "advisory": {
      "markdown_links": { "pass": false, "problems": ["broken link: (src/eoopt/physics/base.py) -> ...\\negative\\src\\eoopt\\physics\\base.py", "... ~40 more broken links, all resolving under the fixture's staging dir (../references/..., src/eoopt/..., adr/..., design/..., tests/...) rather than the eoopt home repo ..."] },
      "placeholders": { "pass": true, "problems": [] }
    },
    "signals": {
      "state_numbers": { "clear": false,
        "candidates": ["candidate test_count drift — distinct values: 59 (lines 5,131,133,269); 69 (lines 144)"] },
      "completion_open": { "clear": false, "candidates": [
        "line 124: section '阶段 1 ... ✅ 已完成（2026-07-28）' marked complete ('✅') but body carries open marker ('届时定')",
        "line 135: section '阶段 2 ... ✅ 已完成基础版（2026-07-29）' marked complete ('✅') but body carries open marker ('届时定')",
        "line 253: section '四、ADR 计划' marked complete ('✅') but body carries open marker ('待补充')"] },
      "roadmap_fields": { "clear": false, "candidates": [
        "stage 1 (line 124, committed): DoD present but VAGUE ('算例届时定') — HF-15 signal; has_metric=True, has_GO/STOP=False",
        "stage 1 (line 124, committed): missing fields ['decision_gate']",
        "stage 2 (line 135, committed): DoD present but VAGUE ('算例届时定') — HF-15 signal; has_metric=True, has_GO/STOP=False",
        "stage 2 (line 135, committed): missing fields ['risks', 'decision_gate']",
        "stage 3 (line 148, committed): DoD present but VAGUE ('待补充调研') — HF-15 signal; has_metric=True, has_GO/STOP=False",
        "stage 3 (line 148, committed): missing fields ['deliverables', 'decision_gate']",
        "stage 4 (line 187, unmarked): missing fields ['status', 'risks', 'decision_gate']",
        "stage 5 (line 195, unmarked): missing fields ['status', 'risks', 'decision_gate']",
        "stage 6 (line 204, unmarked): missing fields ['status', 'risks', 'decision_gate']",
        "stage 7 (line 212, deferred): missing fields ['status', 'decision_gate']",
        "stage 8 (line 230, unmarked): missing fields ['deliverables', 'status', 'risks', 'decision_gate']",
        "stage 9 (line 237, deferred): missing fields ['deliverables', 'decision_gate']"] },
      "session_residue": { "clear": false, "candidates": [
        "AskUserQuestion: lines 291", "HANDOVER: lines 45,142,190,278,285", "session-deixis: lines 182,291",
        "user-decision: lines 11,284,291,321", "authority-paren: lines 11,321", "agent-research: lines 328"] },
      "role_mixing": { "clear": false, "candidates": [
        "section-level roles: roadmap@L1, architecture@L15, research_review@L93, status@L124, adr@L148, open_questions@L212, validation@L267, handover_session@L291",
        "HF-13 candidate: 6 stable-design + 2 volatile role(s) at section level; appendix/link subordination present=True (if not subordinated + drift confirmed -> HF-13)"] }
    }
  }]
}
```

**Checker adjudication summary:**
- HARD **frontmatter → FAIL** = HF-9 (script-confirmed).
- HARD **status_vocab → pass** (HF-3 not fired).
- Advisory **markdown_links → fail**: every `src/…`, `../references/…`, `adr/…`, `design/…`, `tests/…` link is broken **because the fixture is staged out of its eoopt home repo**. This is the *source-inaccessibility* condition, not a content defect — it drives `FACTUAL_VALIDITY=UNVERIFIED`, and per the skill it does **not** by itself force INCOMPLETE.
- All five **SIGNAL** checkers returned `clear:false` → candidates adjudicated in §2 below.

`CHECKER_STATUS = COMPLETE` (hard + advisory + all five signals ran).

---

## 2. Hard-gate walk — EVERY applicable gate, ALL blockers collected

Anti-erosion discipline observed: a met gate is a **BLOCKER** and is **not** downgraded; the walk does not stop at the first (trivial) HF-9. DOCUMENT_QUALITY (doc-only) is separated from FACTUAL_VALIDITY (source-needing).

| HF | Applies? | Verdict | Cited instance / reason |
|---|---|---|---|
| HF-1 Fabricated code-state | yes (factual) | **UNVERIFIED** | Code-state claims ("PhysicsBackend…均已实现" L133; "69 测试全绿…均已实现" L144) need the eoopt repo, which is absent. Cannot confirm or clear — **not** reported as passed. |
| HF-2 Fabricated literature | yes (factual) | **UNVERIFIED** | ~39 external citations (absil2012, he2020, neustock2019, amstutz2017, arXiv:2006.07746, arXiv:2509.23357…) unresolved here. Not passed. |
| HF-3 CANDIDATE-as-DECIDED | yes | pass | `status_vocab` clean; candidates are labeled 备选/押注/待补充调研; ADR-0010 marked "提议中". No DECIDED/FACT misuse found. |
| HF-6 Phase lacks acceptance *section* | yes | not fired | Every committed phase carries a `验证：` line; `roadmap_fields` reported **no** "NO acceptance/DoD (HF-6 signal)". (MINOR: deferred 阶段9 has no explicit `验证：` line — acceptable for a 远期 phase.) |
| HF-7 Dropped a known OPEN question | yes | **UNASSESSABLE** | Requires the originating decision register / OPEN-question list, which was not provided. Cannot diff. Not a confirmed blocker; not cleared either. |
| HF-8 Needs unstated chat context | yes | see §4 | Session residue present (用户决定「本轮 AskUserQuestion」L291; "HANDOVER §7.2/§7.3" L142/L285; "用户明确" L11). Adjudicated with the reader test in §4. Feeds HF-13. |
| **HF-9 Missing traceability front-matter** | yes | **BLOCKER** | Doc opens at L1 with `# eoopt …` — no YAML `---` header, no leading HTML comment. Script-confirmed. |
| HF-10 ≤E2 evidence as E3+ | yes | not substantiated | The transfer table (L97–111) separates 外部成果 (literature) from 就绪度 (project readiness); external precedent is labeled 同域佐证/先例. No clear "indirect-as-project-verified" instance at doc level. Full check needs sources → factual half UNVERIFIED. |
| HF-12A Traceability (doc-only) | yes | pass | Load-bearing claims carry handles (ADR-000x, code paths, transfer cards) or explicit OPEN/assumption labels. No bare unsupported load-bearing claim found. |
| HF-12E Evidence-status labeling (doc-only) | yes | marginal (MINOR) | Readiness/uncertainty *are* labeled (★已实现 / ◐新建; "待补充调研"; "d=3 旧实测、高维未测" L179; the transfer-gap self-flag "把 ManES…落到…隐式流形…是方法学空白" L169 — **rewarded** per HF-12D asymmetry), but not tagged with the explicit direct/indirect/analogy/inference taxonomy. Not a blocker. |
| HF-12B/C/D Source access | yes (factual) | **UNVERIFIED** | 0 cited sources opened (see §3). May **not** be reported as "HF-12 verified/PASS". |
| **HF-13 Mixed artifact responsibilities** | yes | **BLOCKER** | See §2.1. |
| **HF-14a State contradiction** | yes | **BLOCKER** | See §2.2. |
| **HF-14b Volatile-state contamination** | yes | **BLOCKER** | See §2.3. |
| **HF-15 Non-executable committed milestone** | yes | **BLOCKER** | See §2.4. |
| HF-4/HF-5/HF-11 | no | n/a | Not a rewrite/migration output; not a skill-registry/auto-trigger question. |

### 2.1 HF-13 — Mixed artifact responsibilities → BLOCKER

All three firing conditions hold; the escape hatch does **not** apply.

1. **≥2 divergent-lifecycle roles as body-level primary content.** `artifact_role_mixing` finds 8 section-level roles: `roadmap@L1, architecture@L15, research_review@L93, status@L124, adr@L148, open_questions@L212, validation@L267, handover_session@L291` — 6 stable-design + **2 volatile**. The volatile ones are body-level primary content, not pointers:
   - **status** — live per-phase completion blocks embedded *inside* the plan: "完成状态（2026-07-28）… 59 测试全绿" (L133) and "完成状态（2026-07-29）… 69 测试全绿" (L144). Canonical home = `status`/CI, not a roadmap.
   - **handover_session** — "### 用户决定（本轮 AskUserQuestion，已固化）" (L291), a session/interview decision record. Per `canonical-source-map.md`, "a 用户决定(本轮) block inside a roadmap is residue (HF-13 + agent_session_residue)"; canonical home = decision register (ADR).
2. **Not subordinated.** The checker's `subordination present=True` only means *some* `附/详见` markers exist elsewhere (§附 fact-check, cross-phase "详见 §三阶段 7"). The **volatile roles themselves are not subordinated**: the status blocks sit inline in each phase, and the 用户决定 block is its own body `###` section — neither is placed under an appendix/`详见 <decision-register>` pointer with a single stated update mechanism.
3. **Observable harm.** Concrete realized drift (the 59-vs-69 split, §2.2), mislocated canonical state (a reader cannot name the single owning doc for "current test count"), and duplication of the transfer-card material across §一/§二/§三/§附.

Escape hatch (appendix/link subordination + one stated update mechanism + no observed drift) is **not** satisfied — subordination of the volatile roles is absent, no update mechanism is stated, and drift is already observed. **Hybridity is itself the finding**; the applicable HF set is not a "comfortable union" to be relaxed. Recommended split: roadmap plan (this file, plan-only) ▸ live completion/test-count → `status`/CI with an as-of pointer ▸ 用户决定 → decision register/ADR ▸ §附 code-state → `see src/…` pointers ▸ §二 research alignment → research-basis/evidence map.

### 2.2 HF-14a — State contradiction → BLOCKER

`state_number_consistency` candidate confirmed. The document simultaneously asserts two incompatible **current** test counts:
- **59** — L5 "当前 59 测试全绿" (Context, "当前"=now); L131 "现有 59 测试零回归"; L269 "（现有 59 测试全绿）" (§五 validation, "现有"=existing); L133 "59 测试全绿" (阶段1 完成 2026-07-28).
- **69** — L144 "**69 测试全绿**" (阶段2 完成 2026-07-29, the *most recent* completion).

The Context header and §五 ("当前"/"现有" = the present baseline) say 59, while the newest phase-completion says 69. A reader cannot tell whether the current suite is 59 or 69.

**Second doc-only instance (done vs unbuilt), independently surfaced by the no-context reader:** §附 "代码现状" (labeled "讨论前已对代码…核实", L303) describes the code as essentially *unbuilt* — "PhysicsModel 当前硬绑 EO…只有 transfer_matrix+spherical_aberration" (L308), "匹配方法只有 MatchingConstraint…**无 twiss/色品/C1-C3**" (L309), "branch_id 全程占位透传…**无分支枚举/比较/全局图**" (L312) — which directly contradicts §三's "PhysicsBackend…双后端…均已实现", "C1-C3 平衡…可用" (L128, L133) and 阶段2's implemented `branch_probe.py` clustering (L144). The appendix reads as a stale pre-阶段1 snapshot living beside post-阶段2 "已完成" claims. A reader cannot determine what actually exists.

This is the strongest doc-only gate (needs no sources) and near-binary — two independent contradiction sites. **BLOCKER.**

### 2.3 HF-14b — Volatile-state contamination → BLOCKER

Type gate satisfied: the file is a **stable-design roadmap** (self-declared L11), so HF-14b applies (it is *not* a state/experiment report that would legitimately own live counts). It embeds volatile facts as bare restated values with **no timestamped pointer to a single dynamic source** (`canonical-source-map.md`: "a bare '59 tests green' in a roadmap is HF-14b"):
- L5 "当前 59 测试全绿" and L269 "现有 59 测试全绿" — undated, no `as-of`/CI pointer.
- Live "✅ 已完成" completion state inlined per phase (L124, L135) instead of pointing to `status`.

Because two such restatements disagree (59 vs 69), the contamination has already realized as drift (→ HF-14a). **BLOCKER.**

### 2.4 HF-15 — Non-executable committed milestone → BLOCKER

`roadmap_fields` flags committed stages 1/2/3 with **vague** DoD and `has_GO/STOP=False`. Reconciled with HF-6 (acceptance section is *present*, so this is HF-15 not HF-6):
- **阶段 3** (L148, `🔨` committed / "首轮设计完成…待实现"): the committed deliverable's acceptance is "四族各与 PatternSearch/NM…对照（**算例届时定**）" (L184) — `算例届时定` is on the HF-15 vague-acceptance blocklist; non-measurable. No GO/MODIFY/STOP gate, no "if the gating experiment fails, route → …". The "前置地基小实验（gating）" (L179) states a question + metric + downstream weighting but **lacks explicit GO/MODIFY/STOP**, so the research-phase escape is **incomplete** and does not protect the committed implementation DoD.
- **阶段 1 & 2** (L124, L135, both `✅`): marked complete yet their acceptance still reads "各 spec 单元测试（**算例届时定**）" (L131) / "在已知多簇问题上跑通基础管线（**算例届时定**）" (L142) — a completed phase whose DoD is still deferred is an internal completion/open conflict (echoed by `completion_open`).

Committed phases with non-measurable acceptance and no decision gate ⇒ **BLOCKER.** (Deferred 远期 phases 7/9 correctly carry acknowledged-open DoDs → MINOR, not HF-15.)

**Confirmed BLOCKERS: HF-9, HF-13, HF-14a, HF-14b, HF-15.** → **DOCUMENT_QUALITY = FAIL.**

---

## 3. Factual validity / source coverage

`SOURCE_COVERAGE = 0 / 64` (0 load-bearing cited sources opened).

The target is staged in `evals/skills/task-quality/fixtures/dqe/negative/` — **out of its eoopt home repo**. Verified absent from this workspace: `references/lit-review-manifold-optimization/` (transfer-to-electron-optics.md, review.md, matrix.md), `references/algorithm/` (review/matrix/reading-list), all `src/eoopt/…` modules, the `adr/…` files, `tests/…`, and every external paper/arXiv target. The ~64 load-bearing cited handles break down roughly as: ~6 internal corpus docs + ~12 eoopt source modules + ~7 ADRs + ~39 external papers/arXiv IDs. **0 opened.**

Therefore HF-1, HF-2, HF-10 (factual half), and **HF-12B/C/D are UNVERIFIED — not passed.** `FACTUAL_VALIDITY = UNVERIFIED` (hard floor: 0 opened). This report makes **no** claim that the four-family survey ("45 included / 6 全文"), the transfer cards, or citations like [he2020]/[absil2012]/[neustock2019] actually support the specific conclusions drawn — that verification requires opening the eoopt corpus.

> Isolation note: a sibling `messy-hybrid-roadmap.annotations.md` exists next to the target. It was **deliberately not opened** — it would be an answer key and would violate the no-outside-knowledge contract this harness exists to enforce.

---

## 4. Two-layer no-context reader test

A fresh sub-agent was given **only** the target file (no chat, no author intent, no rubric, no hard-fail) and instructed to treat every link/reference as unavailable and to answer purely from the text.

**Result: `READER_TEST = FAIL`.** The reader parsed the goal (Layer-1 Q1) and the decided-vs-candidate split (Layer-2 Q7), but failed the state-source core question (Layer-1 Q3) and two Layer-2 core questions (Q6 next-step DoD, Q11 fallback).

**Layer 1:**
- Q1 goal — answered correctly (dual-formulation matching-manifold optimization platform, kernel + two peer physics backends; L9).
- Q2 primary responsibility — reader flagged the doc as **internally hybrid**: "the stated single job is actually two jobs bundled (目标设计 + 路线图)" and embeds implementation detail despite L11's "不是实现计划". **Target reader is not named.** → corroborates HF-13.
- Q3 current state + canonical source — **FAILED**: reader found "no single canonical current-state section", the 59-vs-69 contradiction, **and** the §附 code-inventory (L308/L309/L312) contradicting the "已完成" phases. "A first-time reader cannot tell what actually exists."
- Q4 term definitions / where ADRs live — reader: "**Key terms: not defined in this document.** There is no glossary… essentially all definitions, decision records, and evidence live outside this file, which itself carries **no reference list**." (whiten/κ≈20, two-level seam, retraction, IGO used undefined.)
- Q5 open questions — answered (the six §六 items enumerated).

**Layer 2:**
- Q6 next step + measurable DoD — **FAILED**: "the document does not provide one… every phase's verification defers cases with 算例届时定"; also ambiguous whether to run the gating experiment first or code the four optimizers. → substantiates HF-15 + Reader-actionability.
- Q7 decided vs candidate — answered (family ③ GA "蓝本待补充调研", gating outcomes, within-family menus all flagged candidate). ✓
- Q8 unsupported load-bearing claims — reader: completion/test counts (self-inconsistent), all algorithm blueprints cited by bare keys with no in-file bibliography, and the driving anisotropy numbers "κ≈20 / 31:1" admitted "d=3 旧实测、高维未测" (L179).
- Q9 fastest-stale facts — test counts, dated ✅ completion markers, §附 code snapshot, "45 included / 6 全文". → corroborates HF-14b.
- Q10 out-of-place sections — §附 code inventory, per-phase 完成状态 logs, 阶段3 code-class specs, the 用户决定 AskUserQuestion log "read as process artifacts rather than design/roadmap content". → corroborates HF-13.
- Q11 if the gating experiment fails, route change — **FAILED**: "no explicit if-fail contingency… outcomes are said to adjust family weights… but there is no stated branch for 'experiment fails → plan becomes X'." → decision-gate/fallback absent.

**RECONCILE.** Every failed answer is **actionable** (a real document defect), not reader error or noise. The state-source failure (Q3) is — per the v0.3 rule — a **MAJOR state-source defect** that must not be downgraded by claiming to know author intent; it concerns the canonical state-source and so **feeds the non-compensatory FAIL**. Q6/Q11 failures make **Reader-actionability** substantiate its paired Layer-2 gate → also feeds the non-compensatory rule. HF-8 is **not** a standalone blocker (the reader did recover goal, responsibility, decided-vs-candidate, and open questions from the text alone — the doc is not *solely* parseable via chat context), but the session residue it noted (用户决定/HANDOVER) is HF-13 input.

Reader's one-line verdict: "A no-context reader could NOT act on this document immediately and unambiguously"; single biggest blocker = "the contradiction about project state."

<!-- READER_SECTION_DONE -->

Reader agent's read-set: `evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md` (only).

---

## 5. Rubric scores (recorded to feed the non-compensatory rule + fix list; a roadmap is scored only after gates, which here FAIL)

**8-dimension base rubric** (0–5 × weight):

| Dim | Wt | Score | Note |
|---|--:|--:|---|
| Factual accuracy | 20 | 2.5 | Doc-level handles good, but 59-vs-69 contradiction (HF-14a) is a factual defect; deep support UNVERIFIED. |
| Information architecture | 15 | 2.0 | 8 roles in one file (HF-13); transfer material duplicated across §一/§二/§三/§附. "Many roles crammed in one file" band. |
| Actionability | 15 | 2.5 | Steps exist but committed DoDs are "算例届时定" (HF-15); no decision gates. |
| Evidence traceability | 15 | 3.0 | Dense citations + readiness labels; evidence *levels* (E0–E5) not systematic; support unverifiable here. |
| Uncertainty expression | 10 | 3.5 | Strong: candidates/gaps labeled; explicit transfer-gap self-flag (L169); "d=3 旧实测、高维未测". |
| Reader fit | 10 | 2.5 | Session residue + the state contradiction impede a no-context reader (see §4). |
| Maintainability | 10 | 2.0 | Volatile counts/completion copied into a stable roadmap → already drifted (HF-14b). |
| Concision | 5 | 3.0 | Thorough but repetitive (transfer cards restated 3–4×). |

raw = 2.5·20 + 2.0·15 + 2.5·15 + 3.0·15 + 3.5·10 + 2.5·10 + 2.0·10 + 3.0·5 = **257.5** → **total = 51.5 / 100**.
Below the 75 pass line; **two** dimensions (IA 2.0, Maintainability 2.0) are below the 2.5 floor. Fails on total, on the floor, and (below) on the non-compensatory rule — three independent ways, consistent with the hard-gate FAIL.

**Roadmap-specific [NC] dimensions:** Definition of Done ≈ 2.0 (< 3.5, substantiates **HF-15**), State consistency ≈ 1.5 (< 3.5, substantiates **HF-14a**), Canonical-source management ≈ 2.0 (< 3.5, substantiates **HF-14b**), Reader actionability ≈ 2.0 (< 3.5, substantiates **Reader Layer-2 failure** — §4 Q6/Q11). Stage-granularity is also uneven (阶段3 = 4 optimizer families + shared preconditioner + gating experiment, vs the thin 阶段5/6).

### Non-compensatory rule
**Four** critical dimensions score < 3.5 **and each substantiates its paired hard gate/failure with a cited instance** (DoD→HF-15 阶段3 L184; State→HF-14a 59-vs-69 + §附/body; Canonical-source→HF-14b L5/L269; Reader-actionability→Layer-2 Q6/Q11 §4). Under the v0.3 rule this is a **verdict-level FAIL regardless of total** — breadth (the "强" information architecture) may **not** buy back the structural failures. This is exactly the v0.2 false-pass pattern the rule exists to stop.

### Reverse-outline coherence
Thesis (L9 最终目标) is clear, but many sections map to *different* goals than "a plan" — §一 is an architecture spec, §二 a research-alignment review, the 完成状态 blocks a status report, §附 a fact-check register, §用户决定 a session record. Many-sections-to-different-goals is itself an **HF-13 signal**, not merely an IA cap.

---

## 6. Severity-ordered fix list (structural first, one lever before any nit)

1. `BLOCKER` **HF-13** — Split the file by lifecycle. Keep only the *plan* here; move live completion/test counts to `status`/CI (pointer + as-of), the 用户决定 block to a decision register/ADR, §附 code-state to `see src/…` pointers. (L124/L133/L144/L291)
2. `BLOCKER` **HF-14a** — Resolve 59 vs 69 to one current value with a single source; make Context (L5) and §五 (L269) agree with the newest completion (L144).
3. `BLOCKER` **HF-14b** — Replace every embedded count/completion with a timestamped pointer to the single dynamic source; a stable roadmap must not restate "59/69 tests green". (L5, L269, L124, L135)
4. `BLOCKER` **HF-15** — Give committed 阶段3 (and the still-"届时定" 阶段1/2 acceptance) a measurable DoD + explicit GO/MODIFY/STOP; or mark genuinely-research work deferred with an acknowledged-open DoD. (L184, L131, L142)
5. `BLOCKER` **HF-9** — Add traceability front-matter (skill/version/commit/time/status) to the target. (L1)
6. `MAJOR` — Reader-actionability / state-source clarity (see §4) and the uneven 阶段3 granularity.
7. `MINOR` — HF-12E: adopt an explicit evidence-level taxonomy (direct/indirect/analogy/inference/assumption-open) per claim. Deferred 阶段9 lacks a `验证：` line.
8. `FYI` — Broken `src/…`/`../references/…` links are a staging artifact (fixture out of home repo), not a target defect; they gate *factual verification*, not document quality.

Handoff: on FAIL, this severity-labeled list returns to the invoking flow / `technical-document-rewriter`. This gate does **not** edit the target.

---

## 7. Verdict block (canonical)

```
DOCUMENT_QUALITY=FAIL
FACTUAL_VALIDITY=UNVERIFIED
READER_TEST=FAIL
CHECKER_STATUS=COMPLETE
SOURCE_COVERAGE=0/64
CONFIDENCE=HIGH
BLOCKERS=[HF-9, HF-13, HF-14a, HF-14b, HF-15]
FILES_READ=[evals/skills/task-quality/fixtures/dqe/negative/messy-hybrid-roadmap.md, evals/skills/harness/hard-fail.md, evals/skills/harness/rubric.md, evals/skills/harness/canonical-source-map.md, evals/skills/harness/checkers/run_checks.py, evals/skills/harness/checkers/roadmap_stage_fields.py, evals/skills/harness/checkers/artifact_role_mixing.py]
```

VERDICT=FAIL total=51.5 blockers=[HF-9, HF-13, HF-14a, HF-14b, HF-15]

No re-eval PASS is predicted or implied: four structural gates (HF-13/14a/14b/15) and four non-compensatory dimensions are failing, READER_TEST=FAIL, and FACTUAL_VALIDITY is UNVERIFIED. A downstream skill may **not** proceed on this artifact (terminal-gate contract requires DOCUMENT_QUALITY=PASS AND FACTUAL_VALIDITY≠UNVERIFIED AND CHECKER_STATUS=COMPLETE AND READER_TEST=PASS — none of the first, second, or fourth hold).
