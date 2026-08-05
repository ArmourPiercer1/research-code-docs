<!--
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: 7919bc4
source_documents:
  - evals/skills/results/batch2_5/document-chain/inventory-report.md
  - evals/skills/results/batch2_5/document-chain/project-state-report.md
  - evals/skills/results/batch2_5/document-chain/goal-scope-note.md
artifact_type: document-artifact-map
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T15:00:00Z
scope: "Target information architecture for the docs/skill-development/** governance+reports+adr corpus (24 files). A design plan only — no file is moved, rewritten, merged, or deleted. Assigns one canonical home per information-type (HF-13 cure), routes all volatile 'current status' to a single owner + pointers (HF-14b cure), and hands a split/linking map to the (Batch-5, not-built) migration+rewriter executors. EXCLUDES fact re-verification (that is PSR), re-inventory (that is forensics), prose rewriting (technical-document-rewriter), file moves (content-canonicalization-and-migration), and deciding the human-preference open questions."
facts: "none (a design plan asserts no new facts; FACT-confirmed canonical owners are BORROWED from the PSR state report, not re-verified here; every home that rests on an unresolved fact/decision is flagged provisional/BLOCKED in the 'Information-type -> canonical home' verdict column)."
hypotheses: "5 provisional/blocked home assignments — see 'Information-type -> canonical home' (verdict = provisional/BLOCKED rows) + 'Coverage note': (1) current-status owner BLOCKED on D-1; (2) hard-fail catalog home provisional on D-6/U1; (3) DQE defect-register canonical provisional on D-6/U6; (4) upstream-method-matrix currency provisional (U2, out of scope); (5) README index membership provisional on D-4."
open_questions: "10 open decisions — see 'Open decisions' + companion open-decisions.md. D-1..D-7 carried from goal-scope-note + IA-1..IA-3 new canonical-home ambiguities this IA cannot resolve. D-1 (canonical current-status owner) and D-4 (README index scope) BLOCK canonical-home assignment; D-6 (duplication drift) gates two provisional homes. Never 'none'."
evidence_level: "n/a (design plan; makes no evidence claim). The borrowed canonical owners rest on PSR rows whose ceiling is E2 (doc-only corpus, no runtime)."
next_handoff: "BLOCKED:content-canonicalization-and-migration, technical-document-rewriter (Batch 5 — not built)"
handoff_requirements: "A future migration skill (content-canonicalization-and-migration, dry-run map first) + rewriter (technical-document-rewriter, new files only) will need: (1) the target doc-set below; (2) the per-info-type canonical home table; (3) the split & linking plan (existing section -> target, pointer left behind); (4) the resolved open decisions — critically D-1 (status owner, the pointer target every volatile split needs) and D-4 (index scope) decided, and D-6 (drift diff) run — before any move/rewrite. Until that capability exists or a user authorizes a manual migration, this plan is parked for human / DQE-advisory review; nothing executes."
status: "CANDIDATE information architecture (a design plan; open decisions listed; no file moved, no prose rewritten, no file deleted)"
-->

# Artifact Map — `docs/skill-development/` governance + reports + adr corpus

A **design plan**: where each responsibility and information-type *should* live once the corpus is
restructured. Nothing here is rewritten prose or an executed file move. Every FACT-confirmed canonical owner
is **borrowed from the PSR state report** (not re-verified); every assignment that depends on an unresolved
fact or human choice is flagged **provisional** or **BLOCKED** and raised as an open decision — never picked
silently. The split plan is a hand-off to `content-canonicalization-and-migration` (dry-run first) and
`technical-document-rewriter` (writes the target docs) — **both Batch-5, not built → `next_handoff` is an
honest BLOCKED marker.**

**Mode:** document-corpus. **Read-only w.r.t. the target:** this run wrote only the three artifacts of this
chain step (this map + `canonical-source-map.md` + `open-decisions.md`); it moved, edited, merged, and
deleted **nothing** in `docs/skill-development/**`.

---

## 1. Role inventory (what this material is carrying)

Fifteen distinct doc-roles across 24 files. `MIXED` = the file that currently serves this role also serves a
role with a **divergent update-frequency** (the HF-13 signal, from forensics' 9 role-mixed candidates).
Volatile roles in stable files are the HF-14b disease.

| # | role / responsibility | serving file(s) / section (evidence) | audience | update-frequency | mixing signal |
|---|---|---|---|---|---|
| 1 | corpus index / navigation | `README.md` (index frame) | newcomers / navigators | rare (stable) | **MIXED** — carries live status header + version changelog (C1) |
| 2 | system architecture (layers, call-chains, norms, vocab, security) | `system-architecture.md` §1–§12 | implementers / maintainers | rare / on-pivot | clean |
| 3 | open-questions register (OQ-1..5) | `system-architecture.md` §13 (canonical) + registry + README (mirrors) | user / project | on-decision | labeled **mirror** ×3 (O3) — not a contradiction |
| 4 | design rationale / decision record | `adr/ADR-DQE-001-…md` | future maintainers | append-on-decision (frozen) | clean (forward "Phase E" framing STALE, C4) |
| 5 | phase roadmap (Batch 0–5 plan + DoD + exit criteria) | `creation-roadmap.md` (plan) | implementers | per-phase | **MIXED** — embeds per-phase completion checkboxes/progress-tracker (C2) |
| 6 | QC policy (hard-fail catalog + soft rubric + eval methodology) | `quality-control-plan.md` | skill authors / reviewers | on-policy-change | borderline — inlines the hard-fail catalog whose canonical home is the harness (O1) |
| 7 | co-run / conflict / release-gate policy | `conflict-matrix.md` | orchestrator / authors | on-policy-change | clean |
| 8 | machine roster (per-skill version/status/write-scope/evals) | `skills-registry.yaml` (schema entries) | tooling + humans | continuous | **MIXED** — large prose `meta:` status-narrative (C6) |
| 9 | **current project status / phase / batch progress (VOLATILE)** | `README.md` §0 + `dqe-v0.4.1-freeze-and-batch2-entry…md` + `skills-registry.yaml` `meta:` | team | continuous | **NO SINGLE OWNER (D-1)** — 3 co-equal surfaces; the HF-14b core |
| 10 | skill audit (KEEP/REMOVE classification) | `current-skills-audit.md` | maintainers | per-audit (dated) | clean |
| 11 | DQE defect register (living) | `reports/dqe-v0.4-defect-ledger.md` | developers | continuous (living) | clean; overlaps blind-matrix §4 embedded ledger (O2) |
| 12 | observability run log (append-only) | `reports/runlog.md` | team | append-only | clean (front-matter date STALE, C5) |
| 13 | eval-run / diagnostic reports (dated records) | `reports/batch1-eval-run…`, `batch2-*-eval…`, `dqe-v0.4-diagnostic-matrix`, `dqe-v0.4.1-diagnostic-close` | reviewers | one-time (frozen) | some **MIXED** (diagnostic-close = close-out + incident + contract-fix + decision) |
| 14 | evaluation-output artifacts (DQE outputs on the `tests/最终目标…` target) | `reports/quality-report-…图.md` (v0.2) + `…_v0.3…md` | eval consumers | frozen-on-generation | v0.2 superseded by v0.3 (C3); v0.3 is an orphan (Or1) |
| 15 | change/upgrade · investigation · retrospective · decision-brief · governance-decision records (dated) | `reports/dqe-v0.3-upgrade`, `dqe-v0.4-skill-change-summary`, `dqe-v0.4-oq-repro-decision`, `dqe-blind-matrix-investigation`, `…独立检查失败复盘…md`, `dqe-v0.4.1-freeze-and-batch2-entry`, `dqe-v0.4.1-phase-e-canary-decision` | developers / deciders | one-time (frozen) | several **MIXED** (retrospective = post-mortem+spec+test-plan+task-list; freeze-entry = decision+changelog+state) |

> **HF-13 reading.** The urgent mixing is where a **living/stable** doc (roles 1, 5, 8) has **volatile** role 9
> baked in — those drift (and already have: C1, C2, C6). The mixing inside **frozen dated reports** (roles 13,
> 15) does not drift and is a lower-priority split → raised as **IA-1**, not force-split here.

---

## 2. Information-type → canonical home (one per type — the HF-13 cure)

FACT-confirmed owners are **borrowed from PSR** (`project-state-report.md` "Corpus facts (confirmed)" + the
resolved contradiction ledger); this IA does **not** re-verify or reassign them (goal-scope CC-2). Rows whose
home depends on an unresolved fact or human choice are **provisional** / **BLOCKED**. Extracted as a standalone
product in the companion `canonical-source-map.md`.

| info type | canonical home (target) | verdict | basis / note |
|---|---|---|---|
| architecture · layers · call-chains · trigger ladder · norms · vocab · security | `system-architecture.md` §1–§12 | **FACT** | PSR: sole architecture doc (`…:89`) |
| open questions OQ-1..OQ-5 | `system-architecture.md` §13 | **FACT** | PSR O3 — canonical; registry/README are self-labeled mirrors |
| design rationale / DQE evaluation contract | `adr/ADR-DQE-001-…md` | **FACT** | PSR: sole ADR, Decisions 1–6 in force (`…:92`); forward framing STALE (C4) |
| phase roadmap · batches · DoD · exit criteria | `creation-roadmap.md` (**plan only**) | **FACT** | PSR: sole roadmap (`…:91`); §0/§1 progress-tracker STALE (C2) — must leave as pointer |
| co-trigger / conflict / release-gate rules | `conflict-matrix.md` | **FACT** | single-role policy matrix |
| per-skill version / status / write-scope / evals | `skills-registry.yaml` (schema entries) | **FACT** | PSR: canonical roster; the source that resolves version drift C1 (`…:90`) |
| skill audit / KEEP–REMOVE classification | `current-skills-audit.md` | **FACT** | single audit role |
| observability run log | `reports/runlog.md` | **FACT** | PSR: append-only log (`…:93`); date STALE (C5) |
| QC policy + soft rubric + eval methodology | `quality-control-plan.md` | **FACT** | policy role is canonical here; the *catalog* sub-type is provisional (next row) |
| DQE evaluation-output on the eoopt target | `reports/quality-report-…_v0.3-2026-07-31.md` (authoritative) | **FACT** | PSR C3 RESOLVED — v0.3 supersedes v0.2; v0.2 lifecycle label → D-2 |
| hard-fail catalog (as reusable data, not policy prose) | `evals/skills/harness/hard-fail.md` *(OUT OF SCOPE of this corpus)* | **provisional** | O1 — drift of `quality-control-plan.md` §1.1 vs the harness file not diffed (D-6/U1); §1.1 to become summary+pointer once confirmed |
| DQE defect tracking (living register) | `reports/dqe-v0.4-defect-ledger.md` | **provisional** | PSR O2 = CONSISTENT/CANDIDATE, not FACT — confirm standalone ledger is canonical vs `dqe-blind-matrix…` §4 snapshot (D-6/U6) |
| upstream method attribution / license | `references/documentation-methodology/upstream-method-matrix.md` *(OUT OF SCOPE)* | **provisional** | exists (PSR filesystem listing); currency UNKNOWN (U2); cited canonical by 5+ docs |
| **current project status · phase · batch progress (VOLATILE)** | **UNRESOLVED — no single owner assigned.** Candidate: a standing PSR **state report** / `status/`-dir per `system-architecture.md:198` | **BLOCKED (D-1)** | HF-14b core. This is the *pointer target* that the C1/C2/C6 volatile splits all require. Cannot be assigned until D-1 is decided (+ IA-2). |
| corpus index / navigation membership | `README.md` (index) — *membership set unresolved* | **provisional (D-4)** | which of `adr/` + the ~14 `dqe-*`/`batch2-*` reports are canonical index children vs a deliberately un-indexed dated append area (Or2/Or3) |

**Tally:** 15 info-types mapped → **10 FACT** homes (borrowed from PSR-confirmed owners) · **4 provisional**
(fact-/diff-/currency-dependent) · **1 BLOCKED** (current-status owner, D-1). Each forensics
contradiction/overlap candidate (C1–C6, O1–O3) is resolved to a canonical owner or explicitly routed to an
open decision — none left silently.

---

## 3. Target doc-set (one responsibility each)

Builds on the FACT-confirmed owners (CC-2 — IA does not reassign them); the only **new** proposed doc is the
single volatile-status owner, which is **provisional/BLOCKED** pending D-1/IA-2.

| target doc | purpose (1 line) | audience | lifecycle | owns info-types |
|---|---|---|---|---|
| `README.md` | corpus index / navigation only | newcomers | living, rare | index/navigation (status header removed → pointer) |
| `system-architecture.md` | architecture + open-questions register | maintainers | living, rare | architecture, norms, vocab, OQ-1..5 (§13 canonical) |
| `adr/ADR-DQE-001-…md` | one DQE design-rationale record | maintainers | append-only, frozen-on-accept | DQE evaluation contract (Decisions 1–6) |
| `creation-roadmap.md` | phased **plan** + DoD + exit criteria | implementers | living per-phase | phase plan (progress-tracker removed → pointer) |
| `quality-control-plan.md` | QC policy + rubric + methodology | authors / reviewers | living on-change | QC policy (hard-fail catalog → pointer to harness) |
| `conflict-matrix.md` | co-run / conflict / release-gate policy | orchestrator | living on-change | conflict + gate rules |
| `skills-registry.yaml` | machine roster of per-skill version/status/evals | tooling + humans | continuous | version/status/write-scope/evals (`meta:` narrative → pointer) |
| `current-skills-audit.md` | KEEP/REMOVE skill audit | maintainers | dated record | skill audit classification |
| `reports/runlog.md` | append-only observability log | team | append-only | run/eval/gate log lines |
| `reports/dqe-v0.4-defect-ledger.md` | living DQE defect register | developers | living | defect IDs D-01… *(canonical pending D-6)* |
| `reports/**` (dated) | frozen dated record area (eval-runs, diagnostics, decision briefs, investigations, governance decisions, change summaries, DQE outputs) | reviewers / deciders | frozen-on-generation | one per dated event *(index membership → D-4; internal split of MIXED reports → IA-1)* |
| **`status/state-report.md`** *(NEW — provisional)* | the single canonical "current project status / phase / batch progress" owner; everything else points here | team | continuous (volatile) | current-status narrative, phase/batch progress, live version roll-up **— BLOCKED on D-1 / IA-2; do not create until decided** |

Clean single-responsibility docs (architecture core, `conflict-matrix.md`, `current-skills-audit.md`,
`runlog.md`, the eval-run reports) **stay in place, no split** — manufacturing a split for them would be
over-triggering.

---

## 4. Split & linking plan (existing section → target, pointer left behind)

A **design map only** — a hand-off for `content-canonicalization-and-migration` to turn into a dry-run move
map and execute. **This IA moves nothing.** "Leaves pointer" = the source keeps a one-line cross-link to the
canonical home; the fact is stored **once**.

| # | existing content (locator) | → target doc | link left behind | driver |
|---|---|---|---|---|
| S1 | `creation-roadmap.md` §0/§1 per-phase completion checkboxes + "Batch 0 IN PROGRESS" tracker (`:21,:23,:33-34,:40`) | **status owner (D-1)** / `skills-registry.yaml` | roadmap keeps the **plan**, replaces the tracker with "current progress → \<status owner\>" | **C2 — the single highest-leverage HF-14b cure** |
| S2 | `README.md` §0 live status/progress header + collapsed version-history changelog (`:16-25`) | **status owner (D-1)** | README keeps index; header → "current status → \<status owner\>" | C1 |
| S3 | `skills-registry.yaml` prose `meta:` status-narrative (`batch2_gate`, `phase_e`, `v0_*_upgrade`) (`:17-30`) | **status owner (D-1)** | registry keeps machine fields; `meta:` reduced to a pointer | C6 |
| S4 | `quality-control-plan.md` §1.1 inline hard-fail catalog HF-1..HF-15 (`:26-50`) | `evals/skills/harness/hard-fail.md` (canonical, out of scope) | qc-plan keeps a summary + "catalog canonical → hard-fail.md" | O1 — **provisional pending D-6/U1 drift diff** |
| S5 | `dqe-blind-matrix-investigation…md` §4 embedded 缺陷账本 | `reports/dqe-v0.4-defect-ledger.md` | blind-matrix keeps a dated-**snapshot** marker + pointer to the living ledger | O2 — **provisional pending D-6/U6** |
| S6 | `reports/quality-report-…图.md` (v0.2) status label | *(no move)* mark `document_lifecycle: DEPRECATED` + pointer to v0.3 | v0.2 → "superseded by v0.3" | C3 / Or1 — **lifecycle annotation, pending D-2** |
| S7 | `adr/ADR-DQE-001-…md` Status forward "provisional-gate → Phase E" framing (`:18-20`) | *(no move)* dated "superseded-in-part by 2026-08-05 advisory freeze" note | Decisions 1–6 **stay in force** | C4 — **annotation, pending D-3** |
| S8 | OQ-1..5 copies in `skills-registry.yaml` + `README.md` | *(no move)* keep `system-architecture.md` §13 canonical | copies stay **labeled pointers/mirrors** | O3 — already labeled; confirm only |
| S9 | MIXED frozen reports (`…独立检查失败复盘…md` 952L; `dqe-v0.4.1-diagnostic-close`; `dqe-v0.4.1-freeze-and-batch2-entry`) | *(deferred)* optional split into single-responsibility docs | — | **IA-1** — frozen dated records don't drift; split is optional, raised not forced |

**Completeness:** every top-level governance file's volatile/duplicated content is assigned above; the clean
single-role docs (§3) stay put; the mixed frozen reports are routed to IA-1. No existing section is silently
dropped — anything not assigned to a canonical home is listed as an open decision.

---

## 5. Open decisions (for the elicitor / decision-manager — do NOT pick silently)

Consolidated in the companion `open-decisions.md`. Carried from `goal-scope-note.md` (D-1..D-7) + three new
canonical-home ambiguities this IA surfaced (IA-1..IA-3). **None is decided here.**

**Blocking canonical-home assignment:**
1. **D-1 — canonical "current project status" owner.** `README.md §0` vs `…freeze-and-batch2-entry…` vs
   `skills-registry.yaml meta` vs a standing PSR **state report** (`system-architecture.md:198`). Until decided,
   the entire volatile-status home (§2 BLOCKED row) and splits **S1–S3** have no pointer target. Recommendation
   on record (not a decision): the standing state report be the owner; do not assign silently.
2. **D-4 — README index scope.** Are `adr/` + the ~14 `dqe-*`/`batch2-*` reports canonical index children, or
   is `reports/` a deliberately un-indexed dated append area? Gates the index-membership home (§2) + Or2/Or3.

**Gating two provisional homes:**
3. **D-6 — duplication drift (repo-verifiable by diff, no human):** has `quality-control-plan.md` §1.1 drifted
   from `hard-fail.md` (O1/U1)? Is `dqe-blind-matrix §4` a true duplicate of the standalone ledger or a dated
   snapshot (O2/U6)? Result decides S4 + S5 (pointer-only vs summary+pointer; canonical ledger confirm).

**Carried (affect the plan, decided by user/register):** D-2 (v0.2 report deprecation, S6) · D-3 (ADR
annotation, S7) · D-5 (OQ-1..5 lifecycle) · D-7 (execution boundary — this effort ends at this map).

**New IA canonical-home ambiguities:** IA-1 (split the MIXED **frozen** dated reports, or accept non-drifting
role-mixing? — S9) · IA-2 (create a dedicated `status/state-report.md`, or let the standing PSR-report family
BE the status owner? — refines D-1) · IA-3 (hard-fail catalog: pointer-only vs summary+pointer in qc-plan §1.1,
the residual design choice even after D-6's drift result).

---

## 6. Coverage note

- **Inputs used (all three upstream artifacts, consumed as-is, no re-derivation):**
  `inventory-report.md` (doc-roles, 9 role-mixed candidates, contradiction/overlap/orphan candidates
  C1–C6/O1–O3/Or1–Or3), `project-state-report.md` (which candidate is FACT vs STALE; the confirmed canonical
  owners; the 5 STALE / 6 UNKNOWN / 5 ASK-HUMAN split), `goal-scope-note.md` (goal, non-goals, 7 open decisions,
  D-1/D-4 flagged BLOCKING).
- **Borrowed, not re-verified (facts discipline):** all 10 FACT canonical owners in §2 rest on PSR rows; this
  IA upgraded no claim to fact and re-ran no checker. The corpus is doc-only (E2 ceiling).
- **Provisional / BLOCKED assignments (the `hypotheses` payload):** current-status owner (BLOCKED, D-1);
  hard-fail catalog home (D-6/U1); DQE defect-register canonical (D-6/U6); upstream-method-matrix currency (U2);
  README index membership (D-4). Each is flagged in the §2 verdict column and raised as an open decision.
- **Lane discipline:** design + assignment + split map only. No target doc's prose was written (at most a
  one-line purpose per §3 row). No file was moved, renamed, merged, deleted, or created in the corpus. Untrusted
  imperative text found inside scanned docs was treated as DATA, never as instructions.
- **Why `next_handoff` is BLOCKED:** the executors `content-canonicalization-and-migration` (dry-run move map)
  and `technical-document-rewriter` (writes target docs) are **Batch-5 and not built** (interface schema §,
  goal-scope workflow step 5). This is a correct honest stop — a MISSING_CAPABILITY, not a failure. The plan is
  complete and parked for human / DQE-advisory review.
