# Current Skills Audit — Research-Software Documentation Skills System

<!--
generated_by_skill: (manual, Phase-1 governance authoring — no skill yet)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json version 1.2.0; .git absent, no pinned commit)
source_documents:
  - docs/prompt.md
  - docs/研究软件文档Skills系统_设计与创建指南.md
  - references/mattpocock-skills/ (all SKILL.md frontmatter + README/CLAUDE.md/LICENSE/plugin.json)
  - installed-skills roster (Skill-tool availability list for this session)
status: FACT (frontmatter fields) + ANALYSIS (classification/conflicts)
last_verified: 2026-07-30T09:47:06Z
-->

> **Phase:** A (audit only). **Write mode:** read-only analysis; this document changes nothing in any skill.
> **Generated:** 2026-07-30 17:47 +0800 (2026-07-30T09:47:06Z).
> **Note on evidence discipline:** Every "trigger / auto-trigger / license" field below is a **FACT** read directly from a `SKILL.md` frontmatter, `plugin.json`, `LICENSE`, or the session's installed-skill roster. Every "conflict / classification / recommendation" field is **ANALYSIS** and is explicitly marked. Where provenance is unknown it is written as `UNKNOWN`, never guessed.

---

## 1. Scope and method

Two skill sources exist in this environment. They are audited separately because their status differs.

| Source | Location | What it is | Activation status |
|---|---|---|---|
| **Reference (vendored)** | `references/mattpocock-skills/` | Matt Pocock's skills repo, copied in. MIT, `plugin.json` version **1.2.0**. No `.git` → **no pinned commit**. | Inert files. Not loaded by the harness from here. |
| **Installed (live)** | The live Claude Code skill loader | The skills actually offered to the model this session (the Skill-tool roster). A curated **subset** of Matt's skills + a research/science stack + vendor meta-skills. | Model- or user-invocable **now**. |

**Method.** Read all reference `SKILL.md` frontmatter (name, description, `disable-model-invocation`), the repo `README.md` / `CLAUDE.md` / `LICENSE` / `plugin.json` / `package.json`; cross-referenced against the installed roster. Workflow bodies were read for the skills central to conflict analysis (`ask-matt`, `research`, `prototype`, `grilling`, `code-review`, `domain-modeling`, `codebase-design`, `wayfinder`); peripheral bodies were classified from frontmatter + the repo README's flow map.

**Provenance caveat (constraint D.10 / §14.7).** The vendored copy has no `.git`, so no exact upstream commit can be pinned. Recorded provenance is `mattpocock/skills @ vendored-snapshot (plugin.json v1.2.0)`. Before any of these methods is *adopted* into a new skill, the exact upstream commit must be re-pinned from https://github.com/mattpocock/skills. The installed research/science skills (`lit-review`, `wos-research`, …) are **user-local**; their upstream repo/commit/license are `UNKNOWN` from inside this workspace and are flagged for the user to confirm.

**Key environment finding (drives Phase B).** The third-party design guide assumes a generic environment and proposes building research atomic skills from scratch. In reality:
1. Matt's **issue-tracker flow** (`ask-matt`, `to-spec`, `to-tickets`, `triage`, `wayfinder`, `implement`, `improve-codebase-architecture`, `grill-with-docs`, `handoff`, `setup-matt-pocock-skills`) is **not installed** — it exists only as reference. So the guide's "replace/split these active skills" mostly collapses to "keep as reference."
2. A rich **research/literature stack is already installed** (`lit-review`, `wos-research`, `deep-research`, `paper-fetch-skill`, `literature-ingest`, `scansci-pdf`, `mineru-ocr`). This **already covers most of the guide's proposed research atomic skills**. New research skills must be thin adapters over these, not reimplementations.
3. Upstreams the guide names (Addy Osmani, GitHub docs skills, Academic Research Skills) are **not present** in this workspace and cannot be cited as methodology sources.

---

## 2. Classification legend

| Class | Meaning | Default action in this system |
|---|---|---|
| **KEEP** | Sound as-is; no conflict with the new flows. | Use unchanged. |
| **KEEP_WITH_LIMITS** | Useful but must be scoped (write-range or trigger narrowed) to avoid conflict. | Add do-not-trigger / write-scope limits in the registry + router. |
| **SPLIT** | Bundles two jobs that should be separable in the new system. | Keep upstream as reference; the split targets become new skills in later batches. |
| **REPLACE** | A new control/router skill supersedes its role. | New skill created later; upstream kept as reference until then. |
| **REFERENCE_ONLY** | Valuable as a method/vocabulary source; must not auto-activate here. | Keep in `references/`; never symlink into an active skills dir. |
| **REMOVE** | Deprecated upstream, or irrelevant to research-software work. | Do not install; exclude from the system. |

> Classification is **ANALYSIS**. "REPLACE / SPLIT" here never means "delete now" — it is a target state for later batches. Nothing is deleted or rewritten in Phase 1 (constraints D.4–D.6).

---

## 3. Installed research / science stack (user-local)

These are the highest-priority audit targets because they are **live** and they overlap the guide's proposed research skills. License/commit `UNKNOWN` (user-local) — flagged for user confirmation.

| Skill | Purpose (from installed description) | Trigger (installed) | Auto-trigger | Write scope (observed/declared) | Class | Conflict with new flows |
|---|---|---|---|---|---|---|
| **lit-review** | End-to-end literature-review **orchestration**: plan → grounded retrieval → citation snowball → concept matrix → reflect/iterate. Reuses retrieval/download/OCR/ingest skills. | "文献调研/综述/研究现状"; multi-paper survey. Routes single-paper→paper-fetch; heavy PRISMA→deep-research. | Yes (model-invocable) | Writes review corpus + structured survey (MD) | **KEEP_WITH_LIMITS** | Overlaps `research-question-and-literature-planner` + `research-evidence-synthesizer`. **This is already a control skill for the literature axis.** New research atoms must defer retrieval to it. |
| **wos-research** | Iterative **Web of Science** search with relevance-feedback query rewriting; BM25+SPECTER2 + LLM rerank; Rocchio PRF; quick/standard/deep tiers. | "WoS/Clarivate 检索, 迭代 query 优化, 检索质量评估, idea 查重". | Yes | Writes search results/scoring artifacts | **KEEP** | Complements the planner; new planner should **hand off** to it, not duplicate WoS logic. |
| **deep-research** | Deep multi-source web research harness: fan-out search, fetch, adversarially verify, synthesize cited report. | "deep research report" on a topic; asks clarifying Qs if underspecified. | Yes (skill) | Writes cited report (MD) | **KEEP** | Heavy. New `research-evidence-synthesizer` must **not** re-trigger on ordinary doc questions; deep-research owns the fan-out+verify pattern. |
| **paper-fetch-skill** | Known-paper reading/summary/full-text/verification from DOI/URL/arXiv/title/citation. | Known paper → read/summarize/compare/translate/verify/get full text. Not open-ended search. | Yes | Reads/caches papers; writes summaries | **KEEP** | Clean boundary (single known paper). Router sends single-paper here. |
| **literature-ingest** | Ingest local PDF (+OCR) into Zotero + linked Obsidian note; dedup; deterministic Zotero writes; idempotent. | `/literature-ingest` on a local paper, or lit-review archive handoff. | Manual/handoff | Writes Zotero + Obsidian note (idempotent, never overwrites human notes) | **KEEP** | Feeds `research-evidence-synthesizer` with an evidence store. No conflict. |
| **scansci-pdf** | Download papers (13+ sources, WebVPN/Tor/Sci-Hub), search, citations, batch, `.bib`. | "下载论文, DOI, 批量下载, 文献检索, citation export". | Yes | Downloads files to disk | **KEEP** | Pure acquisition. No conflict; used by lit-review. |
| **mineru-ocr** | MinerU cloud OCR of PDF/images → Markdown (tables, formulas). | OCR a PDF/image to Markdown. | Yes | Writes OCR markdown | **KEEP** | Utility. No conflict. |
| **gpt** | Drive GPT (General Particle Tracer) sims: author `.in` decks, run, analyze `.gdf`, scan/optimize. | Particle tracking / beam dynamics / `.gdf` / emittance. | Yes | Writes decks, runs sims, writes outputs | **KEEP** | A concrete scientific-computing domain skill — a realistic **eval sample** for the numerical-design flow. No conflict. |
| **dataviz** | Design system for any chart/plot/dashboard (palette, marks, a11y). | Before writing any chart code / choosing chart colors. | Yes | Advises; produces viz code | **KEEP** | Feeds validation/benchmark reporting. No conflict. |

**Analysis — the single most important adaptation:** the guide's `research-question-and-literature-planner` and `research-evidence-synthesizer` **cannot be built as standalone heavy skills** without colliding with `lit-review`, `wos-research`, and `deep-research`. They must be reframed (Phase B) as (a) a **scoping/stop-criteria front-end** that routes to the existing retrieval skills, and (b) a **design-facing synthesizer** that turns already-retrieved evidence into an evidence matrix + method-transfer cards + evidence-level tags. Their do-not-trigger lists must name all five existing research skills.

---

## 4. Installed Matt Pocock subset (live)

The live roster includes exactly these Matt skills: `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grilling`, `prototype`, `research`, `resolving-merge-conflicts`, `tdd`. (Frontmatter FACT from `references/mattpocock-skills/`; live-availability FACT from the session roster. License MIT, `mattpocock/skills @ snapshot v1.2.0`.)

| Skill | Purpose | Auto-trigger (from `disable-model-invocation`) | Write scope | Class | Limit / conflict (ANALYSIS) |
|---|---|---|---|---|---|
| **tdd** | Red→green test loop reference. | Yes (model-invocable) | Edits code + tests | **KEEP** | None. Downstream of implementation, orthogonal to design docs. |
| **diagnosing-bugs** | Diagnosis loop for hard bugs / perf regressions. | Yes | Edits code; adds regression test | **KEEP** | None. Reads `CONTEXT.md`/ADRs — compatible. |
| **resolving-merge-conflicts** | Resolve in-progress merge/rebase. | Yes | Edits conflicted files | **KEEP** | None. |
| **code-review** | Two-axis review (Standards + Spec) of a diff vs a fixed point, parallel sub-agents. | Yes | Read-only review output | **KEEP_WITH_LIMITS** | Add a **scientific-validity** dimension (math correctness, units/dimensions, numerical stability, boundary/convergence, RNG control, reference solutions, reproducibility) as a **separate** `scientific-validity-review` skill — do **not** bloat `code-review`. |
| **codebase-design** | Deep-module vocabulary (module/interface/seam/depth/adapter). | Yes | Advisory | **KEEP_WITH_LIMITS** | Internal code-shape lens **only**. Must not override external API docs, C4, scientific terminology, or established domain conventions. Overall system architecture belongs to `scientific-software-architect`. |
| **domain-modeling** | Actively build/sharpen domain model + ADRs + glossary. | Yes | Writes `CONTEXT.md`, ADRs, glossary | **KEEP_WITH_LIMITS** | Owns **stable** terms/objects/confirmed relations/decided concepts **only**. Must **not** hold unverified hypotheses, transient experiment observations, candidate algorithms, or current progress — those go to `uncertainty-and-decision-manager`. |
| **grilling** | Relentless one-at-a-time interview to a shared understanding. | Yes (model-invocable) | None (conversation) | **KEEP_WITH_LIMITS** | Change stop criterion to "the current **decidable** boundary," and require unresolved branches be classified (repo-verifiable / needs-literature / needs-prototype / user-preference / deferred). Automatic elicitation in the doc flows is owned by `goal-scope-and-workflow-elicitor`; `grilling` stays a manual primitive. |
| **prototype** | Throwaway code answering one design question. | Yes | Writes throwaway code | **SPLIT** | Split into `application-prototype` (app/UI logic) and `scientific-prototype-experiment` (convergence, effective dimension, noise, ill-conditioning, differentiability, benchmarks — must emit GO/MODIFY/STOP/NEED-MORE-EVIDENCE). Until the split ships, keep `prototype` but the router prefers the science variant for numerical questions. |
| **research** | Background agent → primary-source investigation → cited MD. | Yes | Writes a MD notes file | **SPLIT / KEEP_WITH_LIMITS** | Narrow auto-trigger so it does **not** fire on *academic literature* tasks (owned by `lit-review`/`wos-research`) — its lane is **technical primary sources** (official docs, standards, source, first-party APIs). Effectively the guide's `technical-primary-source-research`. |

---

## 5. Reference-only Matt skills (present in repo, NOT installed)

These are the guide's "replace/split" targets — but they are **already dormant** here. Action for Phase 1 is simply to keep them as reference and let the three new control flows fill their niche. (MIT, `mattpocock/skills @ snapshot v1.2.0`.)

| Skill | Purpose | Auto-trigger | Class | Rationale (ANALYSIS) |
|---|---|---|---|---|
| **ask-matt** | User-invoked router over Matt's skills; "main flow + on-ramps" map. | No (`disable-model-invocation`) | **REPLACE** (later) | Router scope is Matt's engineering flow. Superseded by a project `research-software-workflow-router` (later batch). Keep as the exemplar of a good router. |
| **wayfinder** | Plan an effort too big for one session as decision tickets on a tracker. | No | **KEEP_WITH_LIMITS** (if installed) | Valuable for "long-term decision fog." Requires an issue tracker (not configured here). If adopted, it sits **after** state-reconstruction, and shares the "decision, not deliverable" idea with `uncertainty-and-decision-manager`. Not installed now → REFERENCE_ONLY in practice. |
| **to-spec** | Synthesize conversation → spec on tracker. | No | **KEEP_WITH_LIMITS** (rename target `to-implementation-spec`) | Only for *stable* implementation needs; gated behind decided algorithm baseline + verified assumptions. Numerical algorithms first pass through `algorithm-technical-spec-author`. Not installed → reference. |
| **to-tickets** | Split plan/spec into tracer-bullet tickets with blocking edges. | No | **KEEP_WITH_LIMITS** | Extend task taxonomy (DECISION/RESEARCH/FACT_AUDIT/PROTOTYPE/EXPERIMENT/IMPLEMENTATION/VALIDATION/…) + status gates. Needs a tracker. Reference for now. |
| **triage** | Move externally-arriving issues/PRs through a role state machine. | No | **REFERENCE_ONLY** | Tracker-dependent; not central to doc system. |
| **implement** | Build from spec/tickets via TDD, close with code-review. | No | **KEEP** (if tracker adopted) | Distinguish software implementation from formal experiment runs (`run-scientific-experiment`, later). Reference for now. |
| **improve-codebase-architecture** | Scan for deepening opportunities → HTML report → grill. | No | **KEEP_WITH_LIMITS** | Only **after** workspace forensics + state reconstruction + goal/workflow elicitation. Ordering enforced by the workspace control flow. Reference for now. |
| **grill-with-docs** | `/grilling` + `/domain-modeling`, leaves ADR/glossary trail. | No | **REPLACE** (later) | Superseded by the three control flows (which own automatic elicitation + doc trail). Keep as reference; optionally a manual `domain-grill`, never auto. |
| **grill-me** | Stateless `/grilling`, no codebase. | No | **REFERENCE_ONLY** | Fine as a manual primitive; nothing to change. |
| **handoff** | Compact conversation → handoff MD in OS temp dir. | No | **KEEP** | Session-compression only; must **not** replace `current-status.md`, roadmap, ADR, experiment registry, architecture doc. Reference/optional-install. |
| **setup-matt-pocock-skills** | Scaffold tracker + triage labels + doc layout. | No | **REPLACE** (later) | Superseded by `setup-research-software-skills` (reuse its tracker/label ideas). Reference for now. |
| **writing-great-skills** | Reference for authoring skills well. | No | **REFERENCE_ONLY** (methodology) | Primary methodology source for our own skill authoring (with `skill-creator`). Cite per-rule in the upstream-method-matrix. |
| **teach** | Multi-session teaching workspace. | No | **REMOVE** (not relevant) | Out of scope for research-software docs. |

---

## 6. Reference-only Matt skills — misc / personal / in-progress / deprecated

Condensed; all MIT, `mattpocock/skills @ snapshot v1.2.0`, all **not installed**.

| Bucket | Skills | Class | Note (ANALYSIS) |
|---|---|---|---|
| misc | `git-guardrails-claude-code` | **KEEP** (recommend install) | Safety hooks blocking destructive git. Aligns with §14.8; recommend the user install it. |
| misc | `setup-pre-commit` | **KEEP_WITH_LIMITS** | Useful for the eventual repo; JS/TS-flavored (Husky/lint-staged/Prettier) — adapt for Python (`uv`, pre-commit, ruff) before use. |
| misc | `migrate-to-shoehorn`, `scaffold-exercises` | **REMOVE** | TS-course-specific; irrelevant. |
| personal | `obsidian-vault`, `edit-article` | **REFERENCE_ONLY** | `obsidian-vault` is tied to a foreign vault path; `literature-ingest` already owns our Obsidian writes. `edit-article` is prose editing — reference. |
| in-progress | `batch-grill-me`, `to-questionnaire`, `loop-me`, `writing-beats/-fragments/-shape` | **REFERENCE_ONLY** | Draft interview/writing primitives; harvest ideas (design tree, frontier rounds) into `goal-scope-and-workflow-elicitor`, cited. Do not install. |
| in-progress | `claude-handoff`, `wizard`, `setup-ts-deep-modules` | **REMOVE / REFERENCE_ONLY** | `claude-handoff` spawns background agents (harness-specific); `wizard`/`setup-ts-deep-modules` TS-specific. Not for this system. |
| deprecated | `design-an-interface`, `qa`, `request-refactor-plan`, `ubiquitous-language` | **REMOVE** | Upstream-deprecated (guide §7.4 agrees). `ubiquitous-language` superseded by `domain-modeling`. Do not install. |

---

## 7. Vendor / meta skills (installed)

| Skill | Purpose | License/provenance | Class | Note |
|---|---|---|---|---|
| **skill-creator** | Create/modify/measure skills; run evals. | Anthropic (installed) | **KEEP** (meta) | Primary tool for authoring the new skills + eval harness. |
| **doc-coauthoring** | Structured doc co-authoring workflow. | Anthropic (installed) | **KEEP** (meta) | Methodology source for `technical-document-rewriter` + the control flows' doc steps. |
| **mcp-builder** | Build MCP servers. | Anthropic (installed) | **KEEP** (utility) | Only if we wrap a checker as an MCP server. Not core. |
| **context7-mcp** | Fetch current library docs. | Installed | **KEEP** (utility) | Used by technical-primary-source research. Not a doc-flow skill. |
| **commit** | Conventional commits. | Installed | **KEEP** | Git hygiene. |
| harness built-ins | `verify`, `simplify`, `run`, `review`, `security-review`, `loop`, `init`, `update-config`, `keybindings-help`, `fewer-permission-prompts`, `claude-api` | Anthropic (built-in) | **out of scope** | Harness commands, not classifiable skills. Listed for completeness only. |

---

## 8. Classification roll-up

| Class | Installed | Reference-only | Total |
|---|---|---|---|
| KEEP | tdd, diagnosing-bugs, resolving-merge-conflicts, wos-research, deep-research, paper-fetch-skill, literature-ingest, scansci-pdf, mineru-ocr, gpt, dataviz, skill-creator, doc-coauthoring, mcp-builder, context7-mcp, commit | git-guardrails-claude-code, handoff | 18 |
| KEEP_WITH_LIMITS | code-review, codebase-design, domain-modeling, grilling, lit-review, research* | wayfinder, to-spec, to-tickets, improve-codebase-architecture, setup-pre-commit | 11 |
| SPLIT | prototype, research* | — | 2 |
| REPLACE (later) | — | ask-matt, grill-with-docs, setup-matt-pocock-skills | 3 |
| REFERENCE_ONLY | — | grill-me, writing-great-skills, triage, obsidian-vault, edit-article, in-progress interview/writing set | ~9 |
| REMOVE | — | teach, migrate-to-shoehorn, scaffold-exercises, claude-handoff, wizard, setup-ts-deep-modules, deprecated/* (4) | ~10 |

\* `research` appears twice: its **literature** lane is SPLIT-away (to `lit-review`/`wos-research`); its **technical-primary-source** lane is KEEP_WITH_LIMITS (narrowed trigger).

---

## 9. Conflict flags against the three new control flows

Detailed matrix is in [`conflict-matrix.md`](conflict-matrix.md); this is the audit-level summary of **which existing skills collide with which new flow**.

| New control flow | Colliding existing skills | Nature of collision | Resolution direction |
|---|---|---|---|
| **numerical-research-software-design** | `research` (matt), `lit-review`, `wos-research`, `deep-research`, `prototype`, `domain-modeling`, `codebase-design`, `grilling` | Overlapping triggers on "research/idea/design/prototype." Risk: multiple heavy flows fire on one fuzzy idea. | Router owns entry; research atoms are thin adapters; `prototype`→science variant; elicitation via `goal-scope-...`; `domain-modeling` write-scope limited. |
| **scientific-workspace-reconstruction** | `improve-codebase-architecture`, `diagnosing-bugs`, `code-review` | `improve-codebase-architecture` must run only after forensics + state reconstruction; risk of premature refactor. | Enforce ordering: `workspace-forensics-and-inventory` → `project-state-reconstructor` → `goal-scope-...` → architect → `improve-codebase-architecture`. Forensics is **read-only**. |
| **documentation-refactor** | `doc-coauthoring`, `domain-modeling`, `edit-article`, `research`, `technical-document-rewriter` (future) | Any writing task could over-trigger a full doc refactor; premature polish of unaudited facts. | Restrict trigger to "document corpus / mixed or contradictory docs." Rewrite happens only **after** fact audit + migration map; rewriter never overwrites originals. |

**Cross-cutting high-risk conflict (all three flows):** the **three control flows have adjacent triggers** ("messy files" vs "messy docs" vs "fuzzy algorithm idea"). This is the top conflict to resolve before any of them may auto-trigger — handled by the trigger-priority ladder + conflict matrix in Phase B, and gated by the conflict eval set (constraint D.3, acceptance §15.4).

---

## 10. Audit conclusions feeding Phase B

1. **Do not rebuild the research layer.** Reframe `research-question-and-literature-planner` and `research-evidence-synthesizer` as thin front-end/synthesizer adapters over `lit-review` / `wos-research` / `deep-research` / `paper-fetch-skill`, with do-not-trigger lists naming all five.
2. **The dormant Matt flow lowers Phase-1 risk.** `to-spec`/`to-tickets`/`triage`/`wayfinder`/`ask-matt` are not live, so Phase 1 need not "fight" them — only decide later whether to install adapted versions.
3. **Narrow `research` (matt) now** so it does not auto-fire on literature tasks — this is the one live SPLIT that matters immediately.
4. **Keep `domain-modeling`, `codebase-design`, `code-review`, `grilling` but bound their scope** in the registry; add a separate `scientific-validity-review` rather than expanding `code-review`.
5. **Recommend installing `git-guardrails-claude-code`** (safety) — pending user approval, per constraint (no install without notice).
6. **Confirm provenance** of the user-local research stack (repo/commit/license `UNKNOWN`) — user action item.
