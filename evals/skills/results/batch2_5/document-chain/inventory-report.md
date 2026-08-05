---
generated_by_skill: workspace-forensics-and-inventory
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [docs/skill-development/]
artifact_type: inventory-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Structural inventory of the docs/skill-development/** governance + reports + adr corpus (24 files). Classifies each doc by candidate doc-type + structural signal, flags role-mixing/overlap/contradiction/orphan CANDIDATES, and nominates CANDIDATE canonical sources. Excludes code/eval execution, running the checkers, and any fact verification — that is project-state-reconstructor's job. Read-only: nothing was moved, edited, or asserted to run."
facts: "none (candidates + structural signals only; nothing here is claimed to run, be tested, or be verified truth)"
hypotheses: "45 candidates — 24 doc-type classifications (see 'Doc-type table'), 9 role-mixed candidates (same table, mixed? col), 12 candidate canonical sources (see 'Candidate canonical sources')"
open_questions: "17 items — 9 contradiction/overlap candidates (see 'Contradiction / overlap candidates'), 3 orphan/index candidates (see 'Orphans & unreferenced'), 5 PSR handoff questions (see 'Handoff')"
evidence_level: "n/a (structural signals only; no evidence claims)"
next_handoff: project-state-reconstructor
handoff_requirements: "PSR needs: (1) the corpus root docs/skill-development/; (2) the candidate list below to verify (doc-types, canonical sources, role-mixing); (3) the contradiction/overlap pairs to resolve (each cites where both sides are); (4) access to the OUT-OF-SCOPE targets these docs reference (evals/skills/harness/**, references/documentation-methodology/upstream-method-matrix.md, tests/最终目标设计与开发路线图.md, .claude/skills/**) so it can confirm they exist and are current."
---

# Inventory — `docs/skill-development/` governance + reports corpus

**Mode:** document-corpus
Read-only. Every classification below is a **candidate tagged with its structural signal** — nothing here is a
claim that a doc is correct, current, canonical, or that any code/eval "runs" or "passed" (that verified
judgement is `project-state-reconstructor`'s). Imperative text found *inside* any scanned doc was treated as
inventory DATA, never as an instruction.

## Project Map (one line per directory)
| dir | purpose-guess (signal) | files | notable types | coverage |
|---|---|---|---|---|
| `docs/skill-development/` | governance home for a Skills-system (index + audit + architecture + conflict + roadmap + QC + machine roster) | 7 | 6×`.md` + 1×`.yaml` | fully-scanned (deep-read) |
| `docs/skill-development/reports/` | dated run/eval/decision/defect reports + 1 append-only run log | 16 | `.md` | front-matter + heading structure scanned; long bodies summarized-only |
| `docs/skill-development/adr/` | architecture decision records (1 present; `ADR-DQE-002` named but not built) | 1 | `.md` | fully-scanned (deep-read) |

## Coverage note
- **Fully deep-read (10):** `README.md`, `system-architecture.md`, `creation-roadmap.md`, `current-skills-audit.md`, `conflict-matrix.md`, `quality-control-plan.md`, `skills-registry.yaml`, `adr/ADR-DQE-001-…md`, `reports/runlog.md`, plus front-matter of all reports.
- **Summarized-only (14 reports):** front-matter (`status`/`document_lifecycle`/`generated_by_skill`/`last_verified`) + `#`/`##` heading structure + inbound/outbound reference grep were read; multi-hundred-line report bodies (e.g. `documentation-quality-evaluator_独立检查失败复盘与升级要求.md` 952L, `dqe-blind-matrix-investigation…` 464L, `dqe-v0.4-defect-ledger.md` 372L) were NOT full-read — flagged for PSR if a claim inside them is load-bearing.
- **Skipped:** none inside the corpus. Total corpus ≈ 5,140 lines; deep-read kept under budget by sampling report bodies via structure + grep.
- **Out of scan boundary (referenced but NOT inventoried):** `evals/skills/harness/**` (`hard-fail.md`, `rubric.md`, `canonical-source-map.md`, `checkers/**`), `references/documentation-methodology/upstream-method-matrix.md`, `tests/最终目标设计与开发路线图.md`, `src/eoopt/**`, `.claude/skills/**`. These are cited as canonical by corpus docs but live elsewhere — PSR must confirm existence/currency.

## Doc-type table — document-corpus mode (each row: candidate doc-type + signal; `mixed?` = role-mixing candidate)
| file | doc-type (CANDIDATE) | structural signal | role-mixed? |
|---|---|---|---|
| `README.md` | index / landing | "Phase-1 Index" title + Deliverables link table | **MIXED (high):** index + live progress/status header + collapsed version-history changelog + "Open items" + "Next" — a stable index carrying volatile state (drives contradiction C1) |
| `system-architecture.md` | architecture doc | §1 Layering…§12 security; "architecture v0.1, DECIDED" | no — one maturity snapshot + §13 OQ table is the ADR-DQE-001 HF-13 *escape* (not mixing) |
| `creation-roadmap.md` | roadmap | "Batch 0…5" phase headings + exit criteria + DoD | **MIXED (med):** roadmap + embedded per-phase completion checkboxes/progress-tracker (`[x]/[ ]`) → volatile state in a roadmap (drives contradiction C2) |
| `current-skills-audit.md` | audit report | KEEP/…/REMOVE classification legend + roll-up tables; "status: FACT + ANALYSIS" | no — single audit role (marks FACT vs ANALYSIS internally) |
| `conflict-matrix.md` | conflict/policy matrix | co-run legend (OK/SEQ/DENY/COND) + release-gate table | no — single role |
| `quality-control-plan.md` | QC policy / standard | hard-fail catalog §1.1 + soft rubric §1.2 + eval methodology | borderline — embeds a hard-fail catalog whose canonical home is stated to be `evals/skills/harness/hard-fail.md` (see overlap O1) |
| `skills-registry.yaml` | machine-readable roster | `schema_version`, per-entry `name/version/status/write_scope/evals` | **MIXED (med):** roster + a large prose `meta:` changelog/status-narrative (`batch2_gate`, `phase_e`, `v0_2/3/4_upgrade`) → machine roster carrying human status prose (a "current status" candidate, C6) |
| `adr/ADR-DQE-001-…md` | ADR (decision record) | "# ADR-…", Status/Deciders/Context, Decision 1–6, Consequences, Open questions | no — single ADR role (but currency questioned, C4) |
| `reports/runlog.md` | append-only run log | one-line `time \| skill@ver \| … \| gate=` schema; "status: DECIDED (append-only log)" | no — single role (but self-stale date C5) |
| `reports/batch1-eval-run-2026-07-30.md` | eval-run report | §1 trigger+conflict…§4 gate decision…§7 v0.2 regression | borderline — two eval runs (v0.1 + appended v0.2 regression) + gate decision in one file |
| `reports/quality-report-最终目标设计与开发路线图.md` | evaluation report (DQE **output artifact**) | `generated_by_skill: documentation-quality-evaluator`, `skill_version 0.2.0`; verdict FAIL (HF-9) | no — single eval-output role (but overlaps its v0.3 sibling, C3) |
| `reports/quality-report-最终目标设计与开发路线图_v0.3-2026-07-31.md` | evaluation report (DQE output, v0.3) | `skill_version 0.3.0`; §0 "why this verdict differs from the co-located v0.2 report" | no — single role, but **orphan + overlap** candidate (C3 / Or1) |
| `reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md` | failure retrospective / upgrade spec | 952L; §1 复盘…§5 升级方向…§6 checkers…§7 测试…§8 准入…§9 顺序…§11 任务清单…§12 验收 | **MIXED (high):** post-mortem + requirements-spec + new-checker spec + test-plan + acceptance-criteria + agent task-list; **also has NO front-matter block** (missing-traceability signal) |
| `reports/dqe-v0.3-upgrade-2026-07-30.md` | change/upgrade run report | §1 root cause…§2 what changed…§3 eval results…§5 reproduce | no — single upgrade-run role |
| `reports/dqe-blind-matrix-investigation-2026-07-31.md` | investigation report | 464L; §2 method…§3 results…§4 根因(缺陷账本)…§4X per-failure…§7 recs | **MIXED (high):** investigation + embedded defect-ledger (§4) + per-failure adjudication + recommendations (defect content overlaps O2) |
| `reports/dqe-v0.4-oq-repro-decision.md` | decision brief | "OQ-REPRO decision brief"; §5 the decision; status RESOLVED | no — single decision-brief role (ADR-adjacent; overlaps ADR-DQE-001 Decision 4) |
| `reports/dqe-v0.4-skill-change-summary.md` | change summary / review guide | "review guide"; Files changed / NOT changed; status "immutable — superseded by 0.4.1" | no — single role; self-marks superseded |
| `reports/dqe-v0.4-diagnostic-matrix.md` | diagnostic/eval report | "diagnostic matrix (Phase D)"; status "7/8 → 8/8" | no — single role (dated progression reconciled in-doc) |
| `reports/dqe-v0.4.1-diagnostic-close.md` | diagnostic close-out + incident report | §1 "63M-token runaway — HARNESS_ORCHESTRATION_FAILURE" + §3 D-16 contract fix + §4 OQ-REPRO + §5 verdict | **MIXED (med):** eval close-out + incident post-mortem + contract-fix + decision in one file |
| `reports/dqe-v0.4-defect-ledger.md` | defect ledger (living register) | 372L; "status: LIVING"; Baseline freeze + Ledger D-01… + Spot-check outcomes | borderline — ledger role + embedded baseline-freeze + a spot-check eval result |
| `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` | governance decision / state report | "Advisory Freeze + Batch-2 Entry"; §0 decision…§3 what changed…§6 Batch 2 entered…§7 Phase E preconditions | **MIXED (med):** decision-record + changelog + current-state + roadmap-precondition (a "current status" candidate, C6) |
| `reports/dqe-v0.4.1-phase-e-canary-decision.md` | decision-request brief (superseded) | "Canary 失败汇报与 D-17 决策请求"; §0 TL;DR asks user to pick A/B/C; status RESOLVED banner | borderline — decision-request whose asked-for choice is now moot (superseded content, C4-adjacent) |
| `reports/batch2-workspace-forensics-eval-2026-08-05.md` | eval-run report | "Light Eval Round"; §2 trigger 8/8…§3 shadow…§6 verdict | no — single eval-report role |
| `reports/batch2-skills-eval-2026-08-05.md` | eval-run report | "Light Eval Round (4 skills)"; §1 results…§5 verdict | no — single eval-report role |

**Role-mixed candidate count:** 6 higher-confidence (`README.md`, `creation-roadmap.md`, `skills-registry.yaml`, `…独立检查失败复盘…md`, `dqe-blind-matrix-investigation…md`, `dqe-v0.4.1-diagnostic-close.md`) + 3 borderline (`batch1-eval-run`, `dqe-v0.4-defect-ledger`, `dqe-v0.4.1-freeze-and-batch2-entry`) = **9 flagged**. All are CANDIDATES for `document-information-architect`'s split design + PSR's HF-13/HF-14b lens — flagged only, not resolved here.

## Candidate canonical sources (per information type — CANDIDATE; confirmed later by PSR / document-information-architect)
| info type | candidate source | signal |
|---|---|---|
| Architecture / layers / call chains / trigger ladder | `system-architecture.md` | only architecture doc; §1–§12 structure |
| Design rationale (DQE evaluation contract) | `adr/ADR-DQE-001-…md` | ADR format; Decision 1–6; "ACCEPTED 2026-08-02" |
| Roadmap / batches / phases | `creation-roadmap.md` | "Batch 0…5" headings + exit criteria |
| Machine roster: per-skill version/status/write-scope/evals | `skills-registry.yaml` | schema-per-entry; `status`/`version`/`evals` fields |
| Skill audit / KEEP-REMOVE classification | `current-skills-audit.md` | classification legend + §8 roll-up |
| Pairwise co-trigger / conflict rules / release gates | `conflict-matrix.md` | OK/SEQ/DENY/COND legend + §5 gates |
| QC policy / hard-fail + soft rubric / eval methodology | `quality-control-plan.md` | two-tier gate + rubric weights (but full HF catalog canonical = `evals/skills/harness/hard-fail.md`, OUT OF SCOPE) |
| Observability run log | `reports/runlog.md` | append-only one-line schema; "quality-control-plan §7" |
| DQE defect tracking | `reports/dqe-v0.4-defect-ledger.md` | "status: LIVING"; D-01…D-17 ledger |
| DQE quality-evaluation output (eoopt target) | `reports/quality-report-…图_v0.3…md` **appears to supersede** `…图.md` (v0.2) | v0.3 §0 explains divergence — but neither marks a lifecycle winner (see C3) |
| **Current project progress/status** | **AMBIGUOUS — 3 candidates:** `README.md` §0 header · `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` · `skills-registry.yaml` `meta:` | each carries a "current status" narrative; no single declared owner (see C6) — a PSR question, not resolved here |
| Upstream method attribution / license | `references/documentation-methodology/upstream-method-matrix.md` | cited as canonical by 5+ docs — **OUT OF SCOPE** (outside corpus); PSR to confirm |

## Orphans & unreferenced (candidates — cite the search)
| item | kind | signal (why candidate) | scan boundary |
|---|---|---|---|
| `reports/quality-report-最终目标设计与开发路线图_v0.3-2026-07-31.md` | orphan-candidate | grep for inbound refs across `docs/skill-development/**` found **no** file linking TO it; only the older v0.2 report is cited upstream (by `dqe-v0.3-upgrade` `source_documents` + runlog), and v0.3 only back-links to v0.2 | searched all corpus `.md`/`.yaml` for the filename stem + `quality-report-` |
| `adr/ADR-DQE-001-…md` + the `adr/` dir | index-orphan-candidate | referenced by sibling reports (skill-change-summary, oq-repro, defect-ledger, diagnostic-matrix, runlog) but **absent from the `README.md` "Deliverables" table** and unmentioned by the top-level index | searched `README.md`/registry for `adr/`, `ADR-DQE` |
| Most `reports/dqe-v0.4*` + `dqe-blind-matrix*` reports | index-completeness-candidate | reachable only via `skills-registry.yaml` `meta` prose + sibling cross-refs, **not** listed in `README.md` Deliverables (which names only batch1-eval + runlog) | searched `README.md` link table vs `reports/` glob |
| `ADR-DQE-002`, `HF-REPRO`, `reproducibility_contract_check.py`, 61-slot admission matrix | forward/dangling-reference (labeled not-built) | named in `registry.meta.phase_e` + `freeze…md` §4 + `phase-e-canary…md` as explicitly **NOT built / DEFERRED** | grep `ADR-DQE-002` — appears only as "not done" |

## Contradiction / overlap candidates (flag only — do NOT resolve; PSR / document-information-architect decide)
| # | statement A (loc) | statement B (loc) | note (signal) |
|---|---|---|---|
| C1 | `README.md:16` header "DQE **v0.4.1** FROZEN" | `README.md:63` body list "documentation-quality-evaluator … **v0.3.0**"; `README.md:61` "four Batch-1 skills … now at **v0.2.0**" vs `skills-registry.yaml:38` DQE **0.4.1** | intra-doc + doc-vs-registry version drift (state_number_consistency) |
| C2 | `creation-roadmap.md:23` "Batch 0 — **Status: IN PROGRESS (this commit)**" + `:33-34` unchecked `[ ]` Batch-1 drafts / run evals; `:40` "Batch 1 … (THIS deliverable)" | `README.md:16` "Phase-1 ✅"; `skills-registry.yaml:24` `batch1_eval: PASS`; roadmap **front-matter** `:11` "DECIDED for Batch 1" | roadmap body stale vs its own front-matter + README + registry (completion_open_conflict) |
| C3 | `reports/quality-report-…图.md` status "**DECIDED (verdict FAIL — HF-9 blocker)**" | `reports/quality-report-…图_v0.3…md` status "**DECIDED (verdict FAIL — 5 structural + traceability blockers)**" | two eval outputs, same target `tests/最终目标设计与开发路线图.md`, divergent blocker sets, **both DECIDED, neither DEPRECATED** (which is current?) |
| C4 | `adr/ADR-DQE-001:18-20` "promotion to `provisional-gate` is gated on the admission matrix (Phase E)"; ACCEPTED 2026-08-02 | `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` + `registry.meta.phase_e` "DQE frozen **advisory**; Phase E **DEFERRED**" | ADR's forward "provisional-gate/Phase E" framing overtaken by the 2026-08-05 freeze; ADR not marked superseded/updated (temporal drift) |
| C5 | `reports/runlog.md:9` front-matter `last_verified: 2026-08-05T09:09Z` | `reports/runlog.md:33-38` appended entries dated `09:20Z` / `10:05Z` | front-matter `last_verified` older than the file's own latest lines (stale-date) |
| C6 | "current status" narrated in `README.md` §0 | also in `reports/dqe-v0.4.1-freeze-and-batch2-entry…md` AND `skills-registry.yaml` `meta` | 3 co-existing "current status" surfaces, no single declared canonical owner (overlap / unclear ownership) |
| O1 | hard-fail catalog inline in `quality-control-plan.md` §1.1 (HF-1…HF-15) | canonical home declared as `evals/skills/harness/hard-fail.md` (`qc-plan:49`) | duplicated catalog; drift risk between the two (OUT-OF-SCOPE side unverified) |
| O2 | standalone `reports/dqe-v0.4-defect-ledger.md` (D-01…) | embedded "缺陷账本" in `reports/dqe-blind-matrix-investigation…md` §4 | defect content in two places — overlap/duplication candidate |
| O3 | OQ-1…OQ-5 list in `system-architecture.md` §13 | mirrored in `skills-registry.yaml` `open_questions` + `README.md` "Open items" | same open-questions set in 3 docs (registry `:373` even self-labels "mirror of system-architecture §13") — intentional mirror but a sync-drift surface |

## Handoff (unknowns + questions for `project-state-reconstructor`)
- **H1 (status ownership + version):** Determine the canonical "current project status" among `README.md` §0 / `freeze-and-batch2-entry…md` / `registry.meta` (C6), and reconcile the DQE version (README says v0.3.0/skills "v0.2.0" vs registry 0.4.1 — C1) and the Batch-0/Batch-1 completion state (roadmap body "IN PROGRESS/unchecked" vs registry "PASS" — C2). Forensics only flags; PSR verifies which is FACT.
- **H2 (eval-output lifecycle):** Confirm whether `quality-report-…图_v0.3…md` supersedes the v0.2 report (C3); neither carries a `document_lifecycle` marking a winner, and the v0.3 one is also an **orphan** (Or1). Decide if v0.2 should be DEPRECATED.
- **H3 (out-of-scope canonical sources):** Verify existence/currency of the heavily-cited targets outside the corpus: `evals/skills/harness/{hard-fail,rubric,canonical-source-map}.md` + `checkers/**`, `references/documentation-methodology/upstream-method-matrix.md`, `tests/最终目标设计与开发路线图.md`, `.claude/skills/**`. This inventory could not open them (scan boundary = `docs/skill-development/`).
- **H4 (ADR currency):** Adjudicate whether `ADR-DQE-001`'s "provisional-gate → Phase E" framing is now STALE given the 2026-08-05 advisory freeze + Phase-E DEFERRAL (C4), and whether the `adr/` dir + the `dqe-v0.4*` reports should be added to the `README.md` index (Or2/Or3).
- **H5 (load-bearing report bodies not full-read):** If any claim inside the summarized-only large reports is load-bearing (`…独立检查失败复盘…md` 952L [also missing front-matter], `dqe-blind-matrix-investigation…md` 464L, `dqe-v0.4-defect-ledger.md` 372L), PSR should full-read them; this inventory scanned only their front-matter + headings.

> Discipline check: everything above is a **candidate + structural signal**. No doc was asserted to be correct, current, canonical, tested, or "passing"; no contradiction was resolved; no file was moved, edited, or created except this one report.
