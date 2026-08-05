---
generated_by_skill: project-state-reconstructor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/document-chain/inventory-report.md, docs/skill-development/]
artifact_type: project-state-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T13:30:00Z
scope: "Recovered state of the docs/skill-development/** governance+reports+adr corpus (24 files), consumed via the upstream forensics inventory. Resolves the inventory's contradiction candidates (C1-C6, O1-O3) and confirms/denies its orphan + canonical-source candidates into a FACT/UNKNOWN/STALE/CANDIDATE claim-vs-reality ledger. Doc-only corpus: there is no executable target, so 'what runs' is n/a/UNKNOWN. EXCLUDES designing a target information architecture / canonical-home assignment (that is document-information-architect's job) and running the harness checkers or eval-result verification."
facts: "17 FACT rows with file:line locators — see 'Claim-vs-reality ledger (FACT side)' + 'Corpus facts (confirmed)'; max evidence E2 (verified against doc content + filesystem existence, no runtime target)."
hypotheses: "3 — see 'Believed but unverified (HYPOTHESIS)' (self-reported eval PASS counts, large-report body claims, checker pass-behavior — none independently re-derived)."
open_questions: "16 items — 5 STALE claims ('Contradicted / STALE claims'), 6 file-resolvable UNKNOWNs ('UNKNOWNs (+ how to resolve)'), 5 ASK-HUMAN questions ('ASK-HUMAN — seeds the elicitor'). Never 'none'."
evidence_level: "E2 (claims verified against actual doc content + filesystem existence listing; no runtime/executable target exists in a doc-only corpus, so E3+ is structurally unreachable; checkers + eval-result JSONs were not run/opened, so no execution-level fact is claimed)."
next_handoff: goal-scope-and-workflow-elicitor
handoff_requirements: "Consumer gets: (1) the FACT/UNKNOWN/STALE/CANDIDATE split below; (2) the 5 STALE claims to fix (C2 is the highest-leverage — the roadmap misreports project phase by ~2 batches); (3) the 5 ASK-HUMAN decisions that a repo cannot answer (status ownership C6, v0.2-report deprecation C3/H2, ADR annotation C4/H4, README-index extension Or2/Or3, OQ-1..5). Blocking for the downstream information-architect: C6 (no single canonical current-status owner) and Or1/Or2/Or3 (index gaps) must be decided before canonical-home assignment."
status: FACT/UNKNOWN separated below
---

# State Report — `docs/skill-development/` Skills-system documentation corpus

Facts are **recovered, not inherited** (system-architecture.md:209). Every candidate the inventory raised was
re-checked by opening the actual doc; a doc's self-claim stays a **claim** until this report gives it a
`file:line` locator. Because this is a **document-only** corpus there is no executable target, so *what runs*
is mostly `n/a`/`UNKNOWN` and the real payload is the **claim-vs-reality ledger** below.

**Mode:** document-corpus (Track A). **Read-only:** this run wrote exactly one file (this report); it moved,
edited, or deleted nothing in the corpus.

---

## Inventory (read-only)
- **Entry points / executable target:** none. This is governance + reports + ADR prose. `n/a`.
- **Deterministic assets referenced by the corpus (exist, not run here):** `evals/skills/harness/hard-fail.md`,
  `rubric.md`, `canonical-source-map.md`, `checkers/run_checks.py` + `frontmatter_check.py` +
  `status_vocab_check.py` + `interface_check.py` + 5 signal checkers (`state_number_consistency`,
  `completion_open_conflict`, `roadmap_stage_fields`, `agent_session_residue`, `artifact_role_mixing`) — **all
  present** (filesystem listing).
- **Corpus:** 24 files — 7 top-level governance (`README.md`, `system-architecture.md`, `creation-roadmap.md`,
  `current-skills-audit.md`, `conflict-matrix.md`, `quality-control-plan.md`, `skills-registry.yaml`),
  16 `reports/**`, 1 `adr/ADR-DQE-001-…md`.

## What runs (FACT)
| capability | evidence (file:line / listing) | evidence level |
|---|---|---|
| No executable target in the corpus | doc-only corpus; no manifest/entry-point | n/a |
| The harness checkers the docs cite **exist on disk** | directory listing of `evals/skills/harness/**` (23 `.py`/`.md`, incl. `run_checks.py`, `frontmatter_check.py`, `status_vocab_check.py`, `interface_check.py`, 5 signal checkers) | E2 (exists) |
| The 8 skills the corpus describes **exist as SKILL.md** | `.claude/skills/{documentation-quality-evaluator,project-state-reconstructor,goal-scope-and-workflow-elicitor,uncertainty-and-decision-manager,workspace-forensics-and-inventory,document-information-architect,research-question-and-literature-planner,research-evidence-synthesizer}/SKILL.md` present | E2 (exists) |

> Note: *exists* ≠ *runs/passes*. Whether `run_checks.py` passes on these docs, and whether the eval-result
> JSONs substantiate the claimed PASS counts, is **UNKNOWN** (not run/opened here) — see UNKNOWNs.

## What is tested
| area | evidence | status |
|---|---|---|
| Eval PASS claims (trigger 28/28 ×4; batch-2 32/32; light-round PASS) | self-reported in `skills-registry.yaml:24,197`, `runlog.md:22-24,33-38` | UNKNOWN(resolve: open `evals/skills/results/**`) — corroborated across 3 docs but **not** independently verified against result files |

## Real progress (written vs runs vs tested vs validated)
- **Written:** governance corpus is complete and internally cross-referenced (Batch-0/1 deliverables + Batch-2 build reports all present).
- **Runs:** `n/a` (no runtime target).
- **Tested:** eval PASS counts are self-reported, not re-derived here (E2 ceiling; see above).
- **Validated:** the project's phase state is **FACT**: Batch 0 + Batch 1 complete; Batch 2 = all four skills built + light-round passed (locators in C2 below). Phase E is **deferred** (FACT, C4).

---

## Claim-vs-reality ledger (FACT side) — contradiction candidates resolved

Each inventory contradiction candidate was opened on both sides. Verdicts: **RESOLVED** = one side is current
(FACT, locator) and the other STALE; **CONSISTENT/CANDIDATE** = the sides agree, residual issue is
overlap/ownership; **PARTIAL** = one side FACT, residue UNKNOWN.

| # | verdict | CURRENT side = FACT (locator) | resolving action |
|---|---|---|---|
| **C1** DQE version drift | RESOLVED | DQE current version = **0.4.1**, advisory/profile-scoped-frozen. `skills-registry.yaml:38` (`version: "0.4.1"`) + `.claude/skills/documentation-quality-evaluator/SKILL.md:8` (`skill_version: 0.4.1`) + `:29` (advisory-freeze banner) + `README.md:16` (header). Corroborated `runlog.md:32`. | Update README body version lines (see STALE C1) to 0.4.1, or point them at the registry as the single version source. |
| **C2** Batch-0/1 completion & phase | RESOLVED | **Batch 1 complete; Batch 2 = 4/4 built + light-passed.** `skills-registry.yaml:24` (`batch1_eval: "PASS …"`) + registry Batch-2 entries at `0.1.0` (`:169-289`) + `runlog.md:22-24` (batch-1 gate=pass) + `runlog.md:33-38` (batch-2 build + light-eval gate=pass) + `creation-roadmap.md:11` front-matter ("DECIDED for Batch 1; Batch 2 IN PROGRESS") + same doc `:59` (§2 "ALL FOUR BUILT + light-round PASSED"). | Fix the STALE §0/§1 progress-tracker (see STALE C2). **Highest-leverage fix in the corpus.** |
| **C3** two eval reports, same target | RESOLVED | The **v0.3 report is the authoritative** evaluation of `tests/最终目标设计与开发路线图.md`; blockers = HF-13/14a/14b/15/9. `quality-report-…_v0.3-2026-07-31.md:12,25` + `:35-37` (§0 anti-erosion note explicitly correcting v0.2) + `:3` (skill 0.3.0, newer) + `:11` (reads v0.2). Corroborated `README.md:32-39`, `skills-registry.yaml:29`, `runlog.md:28`. | DEPRECATE the v0.2 report (see STALE C3 / ASK-HUMAN Q2). Both agree target = FAIL; only the blocker set + the (false) PASS-prediction differ. |
| **C4** ADR currency | PARTIAL (FACT + STALE) | ADR-DQE-001 **Decisions 1-6 remain the current DQE contract** (`ADR-DQE-001:28-232`); DQE `SKILL.md:30-31` implements them and the freeze `…freeze-and-batch2-entry…md:82-86` (§4) explicitly changed **none** of them. | The forward "provisional-gate → Phase E" framing is STALE (see STALE C4); annotate the ADR Status, decisions stay in force. |
| **C5** runlog self-stale date | RESOLVED | Log's newest content = **2026-08-05T10:05Z** (`runlog.md:35-38`). | The front-matter `last_verified` is older (STALE C5) — bump it. |
| **C6** current-status ownership | CONSISTENT / CANDIDATE | The 3 "current status" surfaces are **mutually consistent** on substance (DQE 0.4.1 advisory-frozen · Batch 2 decoupled+entered · Phase E deferred): `README.md:16-25`, `…freeze-and-batch2-entry…md` (whole doc), `skills-registry.yaml:17-30` (`meta`). | **No factual contradiction.** Residue = ownership: no single canonical owner; `system-architecture.md:198` says the canonical home for "current dev status" is a `status/`-dir / PSR state report (which did not exist until this one). → ASK-HUMAN Q1 + IA. |
| **O1** hard-fail catalog duplication | PARTIAL (FACT + UNKNOWN) | The catalog appears **inline** in `quality-control-plan.md:26-50` (§1.1, HF-1..HF-15) **and** the same doc declares canonical home `evals/skills/harness/hard-fail.md` at `:49`; that file **exists** (listing). | Whether §1.1 has **drifted** from `hard-fail.md` is UNKNOWN (not diffed; §1.1 is framed as a summary + pointer). See UNKNOWN U1. |
| **O2** defect-ledger overlap | CONSISTENT / CANDIDATE | Living register = standalone `reports/dqe-v0.4-defect-ledger.md` (densest defect-ID content, 41 hits; self-labeled "LIVING" per inventory). Overlapping embedded defect content in `dqe-blind-matrix-investigation-2026-07-31.md` §4 (the investigation that spawned it). | Confirm standalone ledger as canonical DQE-defect register; blind-matrix §4 = dated investigation snapshot → IA. CANDIDATE. |
| **O3** open-questions mirrored ×3 | CONSISTENT / CANDIDATE | OQ-1..OQ-5 are **in sync** across `system-architecture.md:317-321` (§13, canonical), `skills-registry.yaml:369-374`, `README.md:76`; mirror is **intentional + self-declared** (`skills-registry.yaml:367` "mirror of system-architecture §13"; `README.md:76` "See architecture §13"). | Keep arch §13 canonical; the two copies are already labeled mirrors. Drift-risk CANDIDATE (hand-synced) → maintainer/IA. |

**Tally:** 9 candidates → **5 RESOLVED to a clear FACT-current-vs-STALE split (C1, C2, C3, C4, C5)** · **3 CONSISTENT/overlap CANDIDATE with a declared or nominated canonical owner (C6, O2, O3)** · **1 PARTIAL, duplication-FACT with drift UNKNOWN (O1)**. None left wholly unresolved.

## Corpus facts (confirmed) — canonical sources + existence

| fact | verdict | locator |
|---|---|---|
| `system-architecture.md` is the sole architecture doc (canonical for layers/call-chains/norms/vocab) | FACT | `system-architecture.md:1-323` (§1-§13; §6 norm table `:195-207`; §7 vocab `:217-221`) |
| `skills-registry.yaml` is the canonical per-skill version/status roster (the source that resolves C1) | FACT | `skills-registry.yaml:35-374` |
| `creation-roadmap.md` is the sole roadmap (Batch 0-5) | FACT (body §0/§1 STALE — C2) | `creation-roadmap.md:21-105` |
| `adr/ADR-DQE-001` is the sole ADR (canonical DQE design rationale) | FACT (currency-gap — C4) | `adr/ADR-DQE-001-…md:13-232` |
| `reports/runlog.md` is the append-only observability log | FACT (date STALE — C5) | `runlog.md:15-39` |
| `references/documentation-methodology/upstream-method-matrix.md` (cited canonical by 5+ docs) **exists** | FACT (exists); currency UNKNOWN | filesystem listing |
| `tests/最终目标设计与开发路线图.md` (the eval target of C3) **exists** | FACT (exists) | filesystem listing |
| Forward refs `ADR-DQE-002` / `HF-REPRO` / `reproducibility_contract_check.py` / 61-slot matrix are **explicitly NOT built / DEFERRED** (honest dangling refs, not broken promises) | FACT | `skills-registry.yaml:26` ("…are NOT built now"); `…freeze-and-batch2-entry…md:82-84` (§4 "explicitly NOT done") |

## Orphan + index candidates (confirm/deny)

| item | verdict | evidence |
|---|---|---|
| **Or1** `quality-report-…_v0.3-2026-07-31.md` is an orphan | **FACT (orphan)** | grep for the `_v0.3` filename stem across `docs/skill-development/**` = **0 inbound references**. Reachable from no corpus file; only the older v0.2 report is cited upstream. |
| **Or2** `adr/ADR-DQE-001` absent from the README index | **FACT** | `README.md:47-57` Deliverables table lists neither `adr/` nor `ADR-DQE-001`; the ADR is referenced only by sibling reports. |
| **Or3** `dqe-v0.4*` / `dqe-blind-matrix*` / `batch2-*` reports absent from the README index | **FACT** | `README.md:47-57` names only `batch1-eval-run` + `runlog`; the other ~14 reports are reachable only via `skills-registry.yaml` `meta` prose + sibling cross-refs. |

---

## Contradicted / STALE claims (5)

| # | doc (locator) | claim | reality (evidence) | marked |
|---|---|---|---|---|
| **C2** | `creation-roadmap.md:23` (§0) + `:33-34` (unchecked `[ ]`) + "(THIS deliverable)" `:21,:40` | "Batch 0 — **Status: IN PROGRESS (this commit)**"; Batch-1 drafts + eval-runs unchecked | Batch 1 complete + Batch 2 4/4 built: `skills-registry.yaml:24` + `runlog.md:33-38` + roadmap's **own** front-matter `:11` + **own** §2 `:59` | **STALE** — highest-leverage: misreports project phase by ~2 batches |
| **C1** | `README.md:63` ("v0.3.0") + `:61` ("now at v0.2.0" for all four Batch-1 skills) | DQE is v0.3.0 / the four are at v0.2.0 | DQE = **0.4.1** (`skills-registry.yaml:38` + `SKILL.md:8`); README's own header `:16` already says 0.4.1. (v0.2.0 is correct only for PSR/GSWE/UDM, `registry:77,106,136`) | **STALE** (intra-README drift) |
| **C3** | `quality-report-…图.md:16,18,185` (status `DECIDED`, `:10`) | "唯一硬 BLOCKER = HF-9 … 修一处即可复评 … 复评走向大概率 PASS" | The exact false-pass v0.3 was hardened against; superseded by `…_v0.3…md:35-37` | **STALE / superseded** (still labeled `DECIDED`, not `DEPRECATED`) |
| **C4** | `adr/ADR-DQE-001:18-20` (Status, ACCEPTED 2026-08-02) | "promotion to `provisional-gate` is gated on the admission matrix (Phase E)" | Overtaken by the 2026-08-05 advisory freeze + Phase-E deferral (`…freeze-and-batch2-entry…md:30`; `skills-registry.yaml:26`); ADR carries no supersede note | **STALE framing** (decisions themselves stay FACT) |
| **C5** | `runlog.md:9` (`last_verified: 2026-08-05T09:09Z`) | log verified as of 09:09Z | file's own newest entries are `10:05Z` (`runlog.md:35-38`) | **STALE date** |

**Single most important STALE claim:** **C2** — `creation-roadmap.md:23` "Batch 0 — Status: IN PROGRESS (this commit)" with the Batch-1 drafts/eval boxes still unchecked (`:33-34`). A fresh reader landing on the roadmap would conclude the project is still authoring Batch 0, when Batch 1 is finished and all four Batch-2 skills are built and light-passed. It contradicts the roadmap's **own** front-matter (`:11`) and **own** §2 (`:59`), plus the registry (`:24`) and runlog (`:33-38`). It is the volatile-progress-tracker-in-a-roadmap pattern (an HF-14b design smell) whose cure is a pointer to the registry/state report.

## Believed but unverified (HYPOTHESIS)

| # | claim believed | why not a FACT | resolve |
|---|---|---|---|
| H-a | Eval PASS counts (trigger 28/28 ×4, batch-2 32/32, light-round PASS) | self-reported in registry + runlog; I did not open `evals/skills/results/**` to re-derive | read the result JSONs |
| H-b | The large report bodies' load-bearing claims ("diagnostic 8/8", "recall 1.0 false_pass 0", "63M-token runaway") | the 952L/464L/372L bodies were **not** full-read here (roles taken from inventory + targeted greps) | full-read `…独立检查失败复盘…md` (952L), `dqe-blind-matrix-investigation…md` (464L), `dqe-v0.4-defect-ledger.md` (372L) |
| H-c | `run_checks.py` passes on these corpus docs | checkers exist but were **not run** here | run `evals/skills/harness/checkers/run_checks.py` over the corpus |

## UNKNOWNs (+ how to resolve)

| # | unknown | why it matters | how to resolve |
|---|---|---|---|
| U1 | Has `quality-control-plan.md` §1.1 drifted from `evals/skills/harness/hard-fail.md`? (O1) | duplication → drift risk in the canonical hard-gate catalog | diff §1.1 (`:26-50`) against `hard-fail.md` |
| U2 | Currency of the out-of-scope canonical files (`upstream-method-matrix.md`, `hard-fail.md`, `rubric.md`, `canonical-source-map.md`) | 5+ docs cite them as canonical | open each; check `last_verified` / content vs the citing claims |
| U3 | Do the eval-result JSONs substantiate the PASS claims? (H-a) | the corpus's "tested" status rests on them | read `evals/skills/results/**` |
| U4 | Load-bearing content of the 3 un-full-read large reports (H-b) | may contain load-bearing facts | full-read them |
| U5 | Does `run_checks.py` actually pass on the corpus? (H-c) | the docs assert front-matter/status-vocab cleanliness | run the checker |
| U6 | Is the `dqe-blind-matrix §4` defect content a true duplicate of the standalone ledger or a historical snapshot? (O2) | canonical-home assignment for defect tracking | diff §4 against `dqe-v0.4-defect-ledger.md` |

## ASK-HUMAN — seeds the elicitor (intent-dependent; a repo cannot answer)

1. **Status ownership (C6/H1).** Which surface is the *canonical* "current project status" — `README.md` §0, `…freeze-and-batch2-entry…md`, `skills-registry.yaml` `meta`, or a standing PSR state report as `system-architecture.md:198` prescribes? (blocks the IA's canonical-home assignment)
2. **v0.2 report lifecycle (C3/H2).** Deprecate `quality-report-…图.md` (mark `document_lifecycle: DEPRECATED` + pointer to v0.3) now that v0.3 supersedes it?
3. **ADR annotation (C4/H4).** Add a dated "superseded-in-part by the 2026-08-05 advisory freeze" note to `ADR-DQE-001` Status (decisions stay in force)?
4. **Index scope (Or2/Or3).** Extend the `README.md` Deliverables index to cover `adr/` + the `dqe-v0.4*`/`batch2-*` reports, or is `reports/` a deliberately un-indexed dated append area?
5. **OQ-1..OQ-5** remain OPEN/DEFERRED, owned by user/project (`system-architecture.md:317-321`) — carried forward, not silently closed.

## Evidence index
- DQE version = 0.4.1 → `skills-registry.yaml:38`; `.claude/skills/documentation-quality-evaluator/SKILL.md:8,29`; `README.md:16`
- Batch 1 done / Batch 2 built → `skills-registry.yaml:24,169-289`; `runlog.md:22-24,33-38`; `creation-roadmap.md:11,59`
- Roadmap §0 stale → `creation-roadmap.md:23,33-34`
- v0.3 report supersedes v0.2 → `quality-report-…_v0.3-2026-07-31.md:35-37,12,25`; v0.2 conclusion → `quality-report-…图.md:16,18,185`
- ADR decisions vs framing → `adr/ADR-DQE-001-…md:28-232` vs `:18-20`; freeze `…freeze-and-batch2-entry…md:30,82-86`
- Runlog date → `runlog.md:9` vs `:35-38`
- Current-status consistency → `README.md:16-25`; `skills-registry.yaml:17-30`; `…freeze-and-batch2-entry…md`
- Hard-fail duplication → `quality-control-plan.md:26-50,49`
- Open-questions mirror → `system-architecture.md:317-321`; `skills-registry.yaml:367-374`; `README.md:76`
- v0.3 orphan → grep `_v0.3` stem = 0 inbound; README index → `README.md:47-57`
- Norm source "facts recovered not inherited" / current-dev-status canonical → `system-architecture.md:209,198`
- Out-of-scope canonical files + 8 SKILL.md + harness checkers **exist** → filesystem listing

## Coverage note
- **Deep-read (opened in full):** `README.md`, `system-architecture.md`, `creation-roadmap.md`, `quality-control-plan.md`, `skills-registry.yaml`, `runlog.md`, `adr/ADR-DQE-001-…md`, `reports/quality-report-…图.md` (v0.2), `reports/quality-report-…_v0.3…md`, `reports/dqe-v0.4.1-freeze-and-batch2-entry…md`; head of `.claude/skills/documentation-quality-evaluator/SKILL.md`. Targeted greps for Or1 (orphan) + O2 (defect IDs).
- **Existence-only (listed, not read):** `current-skills-audit.md`, `conflict-matrix.md`, the other 12 `reports/**` (incl. the 3 large bodies in H-b), `evals/skills/harness/**`, `references/…/upstream-method-matrix.md`, `tests/最终目标设计与开发路线图.md`, 7 of 8 `.claude/skills/*/SKILL.md`.
- **Budget:** ~11 files deep-read + 6 targeted greps/listings; well under the ~2,000-line focus budget. `whole_repo_allowed: false` respected.
- **Discipline:** every FACT carries a `file:line` (or explicit "filesystem listing") locator; no doc self-claim was promoted to FACT without one; UNKNOWNs/HYPOTHESES kept separate and each carries a resolve-path; imperative text inside scanned docs was treated as DATA, never as instructions.
