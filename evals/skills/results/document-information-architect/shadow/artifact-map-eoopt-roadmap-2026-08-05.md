<!--
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: 975e930
source_documents:
  - tests/最终目标设计与开发路线图.md  (the hybrid "eoopt 最终目标设计与开发路线图" — vision + architecture + algorithm review + roadmap + ADR index + status report + validation plan + open-question register + session/handover record; the canonical HF-13 target)
  - (no forensics inventory present)
  - (no PSR state report present)
status: CANDIDATE information architecture (a design plan; no file moved, no prose rewritten)
last_verified: 2026-08-05T09:09Z
eval_artifact: document-information-architect v0.1.0 SHADOW RUN (Batch-2 light round) — a fresh sub-agent injected with the SKILL.md + template, designing the target IA for the real eoopt hybrid roadmap (the canonical HF-13 case). Read-only; no file moved, no prose rewritten. Eval evidence, not a governance doc.
-->

# Artifact Map — eoopt 最终目标设计与开发路线图

A **design plan**: where each responsibility and information-type carried by the single `tests/最终目标设计与开发路线图.md` file should live. Nothing here is rewritten prose or an executed file move — the split plan is a hand-off to `content-canonicalization-and-migration` (dry-run first) and `technical-document-rewriter` (writes the target docs). Facts are **borrowed from the doc, not verified**; because no forensics inventory or PSR state report was supplied, canonical-source assignments that hinge on an unverified fact are marked **provisional (needs PSR)**.

This is not a manufactured split: the file genuinely carries **eleven** doc-roles with divergent update-frequencies (stable vision through continuous test-counts through one-time session residue in one file) — the exact HF-13 signal, plus HF-14b (test counts / completion state embedded in a stable design doc) and agent_session_residue (a `用户决定（本轮）` block).

## Role inventory (what this material is carrying)

| role / responsibility | serving sections (evidence) | audience | update-frequency |
|---|---|---|---|
| Long-term vision / project goal | Context intro; the `> 最终目标…` quote block; "本文件是目标设计+路线图，不是实现计划" (non-goal) | stakeholders | rare / on pivot (stable) |
| Target architecture design | §1.1 分层, §1.2 双后端, §1.3 MatchingSpec, §1.4 目标层, §1.5 优化器层 (adapter table), §1.6 多分支层; §二 "三处必须自造件" (contributions) | architects / implementers | on design change (stable) |
| Algorithm review / spec (four-family optimizers) | §1.5 deep notes; §三 阶段3 (两条设计不变量, 跨族预条件子, 四族备选 + citations); §附 "四族切向优化器蓝本台账" | algorithm implementers | on research / selection |
| Literature-transfer basis / evidence map | §二 alignment table (transfer 卡片 A–H); §附 "调研现状" | provenance reviewers | on new lit-review |
| Phase roadmap (the plan) | §三 intro (排序原则); §三 阶段1–9 *plan* portions (what · ordering · DoD · 为何排X); §四 phase tags | implementers / PM | per phase |
| **Live status / progress (VOLATILE)** | `✅ 已完成`/`🔨` markers; `完成状态（2026-07-28/-29）` blocks; "59/69 测试全绿", "内核零改动", "release/ 镜像已同步"; ADR status ("提议中/已建/已采纳") | team | **continuous (volatile) ← HF-14b** |
| ADR / decision rationale | §四 ADR 计划 (ADR-0009…0017); design-rationale inside 阶段 blocks (表示假设门, "为何排X" where it argues *why*) | future maintainers | append-on-decision |
| Validation plan | §五 验证策略 (items 1–10); per-阶段 "验证：…" lines | implementers / QA | per phase |
| Open-question register | §六 开放问题 (items 1–6) | researchers / deciders | on resolution |
| **Session / handover record** | §六 "用户决定（本轮 AskUserQuestion，已固化）" (1–7); the `HANDOVER §1/§7.2/§7.3` pointers | transient (none) | **one-time ← agent_session_residue** |
| **Code current-state snapshot (VOLATILE)** | §附 "代码现状" (11 bullets: "PhysicsModel 硬绑 EO", "只有盒式 bounds", seam counts, file/line pointers) | team | **continuous (volatile) ← current behavior** |

## Information-type → canonical home (one per type)

Per `evals/skills/harness/canonical-source-map.md`. This doc exhibits **every row** of that table — an unusually clean HF-13/HF-14b specimen.

| info type | canonical home (target doc) | note |
|---|---|---|
| Current implementation behavior | code + tests (`see src/eoopt/…`) | §附 代码现状 & inline "硬绑 EO / 只有盒式 bounds" — pointer only, never a restated fact in a stable doc; **provisional (needs PSR)** for the state-report home |
| Current progress / % done | `status` / issue tracker / PSR state report | "阶段X 已完成", `完成状态（date）` — pointer + timestamp, or omit; **provisional (needs PSR)** |
| Test status / counts / "all green" | CI / test report | "59 测试全绿", "69 测试全绿", "内核零回归/零改动" — pointer + `as-of <date>`; a bare "59 tests green" in this roadmap **is** HF-14b |
| Architecture rationale (why) | ADR (`docs/adr/NNNN-*.md`) | double-backend / 表示假设门 / whiten-by-deterministic-side rationale — roadmap & architecture *link* the ADR, do not re-argue it |
| Long-term goal / vision | vision / overview doc | the `最终目标` quote — one stable statement, not mixed with live "59 测试全绿" |
| Phase / milestone plan | roadmap | §三 owns the *plan* (阶段, ordering, DoD) only — **not** the live completion state |
| Algorithm math / spec details | algorithm spec (`docs/design/tangent-optimizers-phase3.md`; `references/algorithm/review.md`) | 四族 invariants / 备选 / citations / κ≈20 / whiten — roadmap links it, does not inline the derivation |
| Experiment results / metrics | experiment report / registry | 前置小实验, "31:1 是 d=3 旧实测", α 扫, "Bifurcation→3 簇" — pointer + run id, not a floating number; **provisional (needs PSR)** |
| Literature-transfer basis | research basis / evidence map (`references/lit-review-manifold-optimization/*`, `references/algorithm/*`) | §二 + §附 调研现状 — pointer; transfer assumptions (e.g., "Eldred = 目标非光滑流形，非匹配流形") stay labeled (HF-12D/E) |
| Session / interview decisions | decision register (ADR) | §六 "用户决定（本轮）" — a `用户决定（本轮）` block inside a roadmap is residue (HF-13 + agent_session_residue); relocate to the ADRs those decisions justify |

## Target doc-set (one responsibility each)

Designed **within the existing house convention** evidenced by the doc's own links: a `docs/` root with `docs/adr/NNNN-*.md` and `docs/design/*.md`, a `references/<topic>/` research corpus, and `src/eoopt/` + `tests/`. New canonical docs are placed to match it. Exact filenames and the existence of a status/vision/roadmap home are **provisional (needs forensics/PSR)**.

| target doc | purpose (1 line) | audience | lifecycle | owns info-types |
|---|---|---|---|---|
| `docs/vision.md` (or `overview.md`) **[provisional: may already exist]** | why eoopt exists + the 最终目标 statement + non-goals + "三处必须自造件" | stakeholders | living, rare | vision, non-goals, project contributions |
| `docs/architecture.md` **[provisional: may already exist]** | target layered architecture + seams (§1.1–§1.6, structure only) | architects / implementers | living, on design change | architecture (code-state referenced by pointer, never restated) |
| `docs/roadmap.md` **[provisional: this file may become it]** | phased plan, difficulty×importance ordering, DoD, ordering rationale (§三 *plan*) | implementers / PM | living per phase | phase plan (plan only, not completion state) |
| `docs/adr/ADR-NNNN-*.md` + `docs/adr/README.md` (index) | one decision each; index = §四 ADR 计划 | maintainers | append-on-decision | architecture rationale, decisions, relocated session decisions |
| `docs/design/tangent-optimizers-phase3.md` **(exists)** + `references/algorithm/review.md` **(exists)** | four-family algorithm spec / review | algorithm implementers | living, on research | algorithm math / spec details |
| `docs/status/state-report.md` **or** project PSR / issue tracker **[provisional (needs PSR)]** | the single verified current-state home | team | continuous | current behavior, progress, test status (CANONICAL for these) |
| `references/lit-review-manifold-optimization/*` + `references/algorithm/*` **(exist)** | literature & transfer evidence | provenance reviewers | on new lit-review | literature-transfer basis |
| `docs/validation-plan.md` (or a §roadmap section) | roadmap-level validation strategy (§五) | QA / implementers | per phase | validation plan (live counts via pointer) |
| `docs/open-questions.md` (or `uncertainty-and-decision-manager` register) | open research / decision questions (§六 1–6) | deciders | on resolution | open questions |

## Split & linking plan (existing section → target)

Every section is assigned; volatile facts are *stripped to a pointer*, never copied.

| existing section | → target doc | link left behind |
|---|---|---|
| Context intro + `> 最终目标` quote + "不是实现计划" non-goal | `docs/vision.md` | roadmap/architecture link vision; vision holds the single goal statement |
| Context "阶段1 已完成 / 59 测试全绿" | `docs/status/state-report.md` (pointer) | vision/roadmap say "current state → state report (as-of)"; **no count copied** (HF-14b strip) |
| §1.1–1.6 (architecture structure) | `docs/architecture.md` | architecture links ADRs (rationale) + algorithm spec (math) + roadmap (phasing) |
| §1.2/§1.3 inline "硬绑 EO / 只有盒式 bounds" (current behavior) | code + `state-report` (pointer `see src/eoopt/…`) | architecture references the pointer, does not restate as fact |
| §1.5 adapter table — *structure* | `docs/architecture.md` | — |
| §1.5 "来源: 已有 / 新增(阶段X)" status column | `roadmap` (planned) + `state-report` (done) | architecture table links the phase/status, not embeds it |
| §1.5 / §三阶段3 four-family invariants, 备选, citations | `docs/design/tangent-optimizers-phase3.md` + `references/algorithm/review.md` | roadmap §阶段3 links the spec; does not inline the algorithm math |
| §二 alignment table (transfer 卡片 A–H) | `references/lit-review-manifold-optimization/*` (canonical) | keep a thin *pointer index* in architecture; transfer assumptions stay labeled |
| §二 "三处必须自造件" (contributions) | `docs/vision.md` (or architecture) | — |
| §三 intro (排序原则) + 阶段1–9 *plan* + "为何排X" ordering rationale | `docs/roadmap.md` | roadmap links each ADR + validation plan |
| §三 per-阶段 `✅已完成 / 🔨 / 完成状态（date） / 测试全绿 / 零改动 / release镜像` | `docs/status/state-report.md` (pointer, as-of) | roadmap shows status as a pointer with timestamp — **HF-14b cure** |
| §三 阶段-level design decisions (表示假设门, ADR-0010/0011 rationale) | `docs/adr/ADR-NNNN-*.md` | roadmap/architecture link the ADR |
| §四 ADR 计划 (index of ADR-0009…0017) | `docs/adr/README.md` + individual ADRs | roadmap links the index |
| §四 ADR status markers ("提议中 / 已建 / 已采纳") | `docs/status/state-report.md` (pointer) | index shows decision status via pointer, not embedded |
| §五 验证策略 1–10 | `docs/validation-plan.md` (or roadmap §) | item 1 & "59 测试全绿" → pointer to CI/state (strip the count) |
| §六 开放问题 1–6 | `docs/open-questions.md` | roadmap/architecture link the open items |
| §六 "用户决定（本轮 AskUserQuestion）" 1–7 | `docs/adr/*` (decision register) | relocate as the decisions ADR-0009/0010/0011… encode; **drop the "（本轮）" transient framing** (residue) |
| §附 代码现状 (11 bullets) | code + `docs/status/state-report.md` (pointer) | architecture/roadmap keep only `see src/eoopt/…` pointers |
| §附 调研现状 | `references/lit-review-manifold-optimization/*` + `references/algorithm/*` | evidence-map index points here; assumptions stay labeled |

## Open decisions (for elicitor / decision-manager — do not pick silently)

1. **Session-residue disposition.** Fold §六 "用户决定（本轮）" (the 7 fixed decisions) into the ADRs they justify (ADR-0009/0010/0011…), or keep a standalone append-only session/handover log? The `（本轮）` framing is transient residue either way.
2. **Two canonical homes for algorithm spec.** `docs/design/tangent-optimizers-phase3.md` (design) *and* `references/algorithm/review.md` (review) both currently carry the four-family selection. Which owns the canonical selection statement, and which merely links it?
3. **State-report home identity.** Does a canonical volatile-state home already exist (a PSR doc, a `status/` doc, or an issue tracker), or must `docs/status/state-report.md` be created? **provisional (needs PSR/forensics)** — the whole HF-14b cure depends on this single home existing.
4. **Validation plan placement.** Own doc `docs/validation-plan.md`, or a section inside `docs/roadmap.md`? (§五 is roadmap-level strategy, so either is defensible.)
5. **This file's fate.** Does `tests/最终目标设计与开发路线图.md` *become* `docs/roadmap.md` (rename + strip), or is it retired to a pointer stub after its content is distributed? Note it currently lives under `tests/` while linking `docs/`-rooted paths — a location/convention mismatch to resolve.
6. **ADR filename convention.** The doc mixes `adr/0011-multibranch-detection.md` with prose `docs/adr/0010-…` and label `ADR-0011`. Pin one filename form (`docs/adr/NNNN-*.md` vs `ADR-NNNN-*.md`) before migration.
7. **Open-question register home.** Standalone `docs/open-questions.md`, or route §六 (1–6) into the `uncertainty-and-decision-manager` register?

## Coverage note

- **Inputs used:** the target doc (light structural read for roles only) + `evals/skills/harness/canonical-source-map.md` (always-loaded). **No forensics inventory and no PSR state report were available** — so this is a roles-only architecture; no fact was re-verified.
- **Assumptions marked provisional (needs PSR/forensics):** existence/identity of a canonical state-report/status source (Open decision 3); whether `docs/vision.md` / `docs/architecture.md` / `docs/roadmap.md` already exist vs must be created; which ADRs actually exist (0009 "已采纳", 0010 "提议中", 0011 referenced) vs are planned (0012–0017); all embedded volatile values ("59/69 测试全绿", completion dates, "内核零改动", "release/ 镜像已同步", "Bifurcation→3 簇", "κ≈20 / 31:1"). These are **borrowed, not verified**; their *type→home* mapping is firm, their *values* are not confirmed here.
- **Convention:** designed within the doc's own `docs/adr/NNNN-*` + `docs/design/*` + `references/<topic>/*` house style; genuine convention conflicts (ADR filename form, this file's `tests/` location) are surfaced as Open decisions 5–6 rather than silently normalized.
- **Completeness:** every existing section (Context, §1.1–1.6, §二, §三 阶段1–9, §四, §五, §六 + 用户决定, §附 代码/调研现状) is assigned above or raised as an open decision. Every information-type maps to exactly one canonical home; the three volatile roles (live status, code snapshot, session residue) point at a dynamic/decision source and are **never copied into a stable doc** — the HF-14b/agent_session_residue cure. Hand-off: `content-canonicalization-and-migration` (dry-run move map) → `technical-document-rewriter` (writes each target doc) → `documentation-quality-evaluator` (HF-13 should now pass); run `evals/skills/harness/checkers/run_checks.py` on this map's front-matter first.
