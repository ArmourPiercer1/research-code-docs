<!--
generated_by_skill: content-canonicalization-and-migration
skill_version: 0.1.0
source_commit: 07b5306
source_documents:
  - evals/skills/results/batch2_5/document-chain/document-artifact-map.md
  - evals/skills/results/batch2_5/document-chain/canonical-source-map.md
  - evals/skills/results/batch2_5/document-chain/open-decisions.md
  - evals/skills/results/batch2_5/document-chain/project-state-report.md
artifact_type: migration-map
document_lifecycle: IN_REVIEW
scope: "Dry-run migration plan for the docs/skill-development governance+reports+adr corpus: translates the artifact-map split plan S1-S9 into per-source dispositions. Plan only — nothing is moved, deleted, or overwritten; the corpus is read-only w.r.t. this run."
facts: "none (dry-run plan; FACT homes borrowed from PSR/IA canonical-source-map, not re-asserted here)"
hypotheses: "10 gated dispositions (8 DEFERRED + 2 annotate pending a user decision) — see §2 disposition table; every gated row names its blocked_by. Only S8 (keep-in-place) is unblocked."
open_questions: "Carried: 10 open decisions (D-1..D-7, IA-1..IA-3); 6 bear on this map and are listed in unresolved_decisions (D-1, D-2, D-3, D-4, D-6, IA-1). See §6. Never 'none' — 8 of 11 dispositions are DEFERRED."
evidence_level: "n/a (dry-run plan; makes no evidence claim)"
next_handoff: "technical-document-rewriter"
handoff_requirements: "The rewriter needs, per source: the primary disposition + target (§2), the canonicalization plan (§1), the link-update / pointer plan (§4), the supersession map (§3), and the explicit list of DEFERRED dispositions it must NOT rewrite yet (S1-S5 and S9 pending D-1/D-6/IA-1; S6/S7 annotations pending D-2/D-3). Execution of any move is a separate explicit-write-approval-required stop, not authorized by this map."
last_verified: "2026-08-06T00:00:00Z"
-->

# Migration Map (dry-run) — `docs/skill-development/` corpus

A **dry-run migration plan**: it translates the artifact-map's split plan (`document-artifact-map.md` §4, S1-S9)
into one primary disposition per source, with a target that differs from the source. **Nothing is executed** —
`may_move / may_delete / may_overwrite` are all `false`. Every FACT canonical home is **borrowed** from the
upstream `canonical-source-map.md` (not re-asserted); every disposition whose target home is blocked on an open
decision is a `DEFERRED` (or a decision-gated `annotate`) that **names its gating decision** — no target is
invented, no open decision is silently dropped. Retired docs are **superseded**, never deleted (§3).

**Mode:** dry-run. **Read-only w.r.t. the corpus:** this run wrote exactly one new file (this map, under
`evals/skills/results/batch3/…`); it moved, edited, merged, renamed, and deleted **nothing** in
`docs/skill-development/**`.

## Machine block

```yaml
migration_map:
  mode: dry-run
  may_move: false
  may_delete: false
  may_overwrite: false
  rollback: "v0: nothing executed — revert = discard the candidate dir (evals/skills/results/batch3/documentation-refactor-closure/) + this map. No corpus file was touched, so there is nothing to restore."
  unresolved_decisions: ["D-1", "D-2", "D-3", "D-4", "D-6", "IA-1"]
  dispositions:
    - split_id: S1
      source: "docs/skill-development/creation-roadmap.md"
      primary: DEFERRED
      target: "canonical status owner — pending D-1 (no home assigned)"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-1
      driver: "C2 (highest-leverage HF-14b cure: §0/§1 progress-tracker misreports phase)"
    - split_id: S2
      source: "docs/skill-development/README.md"
      primary: DEFERRED
      target: "canonical status owner — pending D-1 (no home assigned)"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-1
      driver: "C1 (README §0 live status/progress header + version changelog)"
    - split_id: S3
      source: "docs/skill-development/skills-registry.yaml"
      primary: DEFERRED
      target: "canonical status owner — pending D-1 (no home assigned)"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-1
      driver: "C6 (prose meta: status-narrative in the machine roster)"
    - split_id: S4
      source: "docs/skill-development/quality-control-plan.md"
      primary: DEFERRED
      target: "evals/skills/harness/hard-fail.md — disposition pending D-6 drift diff"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-6
      driver: "O1 (§1.1 inline hard-fail catalog vs canonical harness file)"
    - split_id: S5
      source: "docs/skill-development/reports/dqe-blind-matrix-investigation-2026-07-31.md"
      primary: DEFERRED
      target: "docs/skill-development/reports/dqe-v0.4-defect-ledger.md — pending D-6 (true duplicate vs dated snapshot)"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-6
      driver: "O2 (§4 embedded 缺陷账本 vs standalone living ledger)"
    - split_id: S6
      source: "docs/skill-development/reports/quality-report-最终目标设计与开发路线图.md"
      primary: annotate
      target: "docs/skill-development/reports/quality-report-最终目标设计与开发路线图_v0.3-2026-07-31.md"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-2
      driver: "C3 / Or1 (v0.2 superseded by v0.3; supersession annotation, relabel gated on D-2)"
    - split_id: S7
      source: "docs/skill-development/adr/ADR-DQE-001-evaluation-profile-and-verdict-axes.md"
      primary: annotate
      target: "docs/skill-development/reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md"
      move: false
      delete: false
      overwrite: false
      blocked_by: D-3
      driver: "C4 (forward 'Phase E' Status framing STALE; dated superseded-in-part note, gated on D-3)"
    - split_id: S8
      source: "docs/skill-development/system-architecture.md"
      primary: keep-in-place
      target: "no move — §13 stays canonical for OQ-1..5; skills-registry.yaml + README.md OQ copies remain labeled mirrors"
      move: false
      delete: false
      overwrite: false
      driver: "O3 (open-questions mirrored ×3; mirrors already self-labeled — confirm only)"
    - split_id: S9a
      source: "docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md"
      primary: DEFERRED
      target: "single-responsibility split — pending IA-1 (frozen record, low drift)"
      move: false
      delete: false
      overwrite: false
      blocked_by: IA-1
      driver: "IA-1 (MIXED frozen report: post-mortem+spec+test-plan+task-list)"
    - split_id: S9b
      source: "docs/skill-development/reports/dqe-v0.4.1-diagnostic-close.md"
      primary: DEFERRED
      target: "single-responsibility split — pending IA-1 (frozen record, low drift)"
      move: false
      delete: false
      overwrite: false
      blocked_by: IA-1
      driver: "IA-1 (MIXED frozen report: close-out+incident+contract-fix+decision)"
    - split_id: S9c
      source: "docs/skill-development/reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md"
      primary: DEFERRED
      target: "single-responsibility split — pending IA-1 (frozen record, low drift)"
      move: false
      delete: false
      overwrite: false
      blocked_by: IA-1
      driver: "IA-1 (MIXED frozen report: decision+changelog+state)"
```

---

## 1. Canonicalization plan

Canonicalization here = *decide, per information-type, the one home the content will live in once migrated* —
**borrowed** verbatim from `canonical-source-map.md` (10 FACT homes · 4 provisional · 1 BLOCKED). This map does
**not** re-verify or reassign those homes and rewrites **no prose**; it only routes each split's source content
toward its borrowed home (or records that the home is blocked).

| info-type being canonicalized | borrowed canonical home | this map's action | gate |
|---|---|---|---|
| current project status · phase · batch progress (VOLATILE) | **UNASSIGNED** — standing state-report / `status/` owner | route S1, S2, S3 here once a home exists | **BLOCKED D-1** |
| hard-fail catalog (reusable data) | `evals/skills/harness/hard-fail.md` | S4: qc-plan §1.1 → summary+pointer **iff** no drift | D-6 (+IA-3 style) |
| DQE defect register (living) | `reports/dqe-v0.4-defect-ledger.md` | S5: blind-matrix §4 → snapshot marker + pointer **iff** duplicate | D-6 |
| DQE eval-output on the eoopt target | `reports/quality-report-…_v0.3-2026-07-31.md` | S6: mark v0.2 DEPRECATED + supersession pointer | D-2 |
| DQE design rationale | `adr/ADR-DQE-001-…md` (Decisions 1-6 in force) | S7: annotate Status "superseded-in-part" | D-3 |
| open questions OQ-1..5 | `system-architecture.md` §13 | S8: keep canonical; mirrors stay labeled | none (confirm) |

No new prose, no merged bodies, no renames: canonicalization at this stage is **assignment + routing only**. The
volatile-status route (S1-S3) is the highest-leverage cure but cannot be canonicalized until D-1 names an owner.

## 2. Per-source disposition table

Exactly **one primary disposition per source**; every `target` differs from its `source`; every `DEFERRED`/gated
row names its `blocked_by`. "Post-decision intent" is the disposition this becomes **once the gate clears** — it is
**not** executed now.

| # | source (exists) | primary | target (dry-run) | blocked_by | post-decision intent |
|---|---|---|---|---|---|
| S1 | `creation-roadmap.md` §0/§1 tracker | `DEFERRED` | canonical status owner (pending D-1) | **D-1** | split-and-pointer → status owner |
| S2 | `README.md` §0 status header + changelog | `DEFERRED` | canonical status owner (pending D-1) | **D-1** | split-and-pointer → status owner |
| S3 | `skills-registry.yaml` `meta:` narrative | `DEFERRED` | canonical status owner (pending D-1) | **D-1** | reduce `meta:` to a pointer |
| S4 | `quality-control-plan.md` §1.1 catalog | `DEFERRED` | `evals/skills/harness/hard-fail.md` (pending D-6) | **D-6** | split-and-pointer (summary+pointer) |
| S5 | `dqe-blind-matrix-investigation-2026-07-31.md` §4 | `DEFERRED` | `reports/dqe-v0.4-defect-ledger.md` (pending D-6) | **D-6** | merge-into ledger + dated snapshot marker |
| S6 | `quality-report-…图.md` (v0.2) | `annotate` | `reports/quality-report-…_v0.3-2026-07-31.md` | **D-2** | annotate: `DEPRECATED` + `superseded_by` v0.3 |
| S7 | `adr/ADR-DQE-001-…md` Status | `annotate` | `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` | **D-3** | annotate: dated "superseded-in-part" note |
| S8 | `system-architecture.md` §13 (OQ register) | `keep-in-place` | no move; registry + README OQ copies stay labeled mirrors | — | confirm mirrors labeled; no action |
| S9a | `documentation-quality-evaluator_独立检查失败复盘与升级要求.md` | `DEFERRED` | single-responsibility split (pending IA-1) | **IA-1** | optional split (only if promoted to living) |
| S9b | `dqe-v0.4.1-diagnostic-close.md` | `DEFERRED` | single-responsibility split (pending IA-1) | **IA-1** | optional split (only if promoted to living) |
| S9c | `dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` | `DEFERRED` | single-responsibility split (pending IA-1) | **IA-1** | optional split (only if promoted to living) |

**Tally:** 11 dispositions → **8 DEFERRED** (S1-S5, S9a-c) · **2 annotate** (S6, S7 — decision-gated) · **1
keep-in-place** (S8). **10 of 11 are gated** on an open decision; only S8 is unblocked. **0 move / 0 delete / 0
overwrite** — dry-run.

> **Why so many DEFERRED, not `move-to`/`split-and-pointer` now:** the volatile-status splits S1-S3 have **no
> pointer target** until D-1 names the status owner; S4/S5 cannot choose pointer-only vs summary+pointer until the
> D-6 drift diff runs; S9 targets frozen records that do not drift (IA-1 = optional). Assigning a concrete target
> to any of these would be *inventing* a home the upstream explicitly left open — a NO_SILENT_ATTRIBUTION
> violation. `DEFERRED` with a named `blocked_by` is the honest disposition.

## 3. Supersession map (supersede — never delete)

No corpus file is deleted by this plan. The two retired/overtaken docs get a **supersession**, both **gated** so
the relabel is not applied until the owning decision clears:

| retired / overtaken doc | `superseded_by` | mark | executed? | gate |
|---|---|---|---|---|
| `reports/quality-report-…图.md` (v0.2 eval output) | `reports/quality-report-…_v0.3-2026-07-31.md` | `document_lifecycle: DEPRECATED` + one-line pointer to v0.3 | **no** (annotation planned, S6) | **D-2** |
| `adr/ADR-DQE-001-…md` Status (forward "Phase E" framing) | in part, `reports/dqe-v0.4.1-freeze-and-batch2-entry-2026-08-05.md` | dated "superseded-in-part 2026-08-05" note; **Decisions 1-6 stay in force** | **no** (annotation planned, S7) | **D-3** |

The v0.2→v0.3 supersession is a **borrowed FACT** (PSR C3 RESOLVED); what is gated on D-2 is only the act of
applying the `DEPRECATED` label. The ADR's Decisions 1-6 are **not** superseded — only the forward Status framing.

## 4. Link-update / pointer plan

"Leaves pointer" = after a (future, approved) move, the source keeps a **one-line cross-link** to the canonical
home so each fact is stored **once**. For every `DEFERRED` split the pointer **target is not yet resolvable** — it
becomes writable only when the gate clears.

| # | pointer left behind (planned) | pointer target | resolvable now? |
|---|---|---|---|
| S1 | roadmap keeps the plan; tracker → "current progress → \<status owner\>" | status owner | **no — D-1** |
| S2 | README keeps index; header → "current status → \<status owner\>" | status owner | **no — D-1** |
| S3 | registry keeps machine fields; `meta:` → pointer | status owner | **no — D-1** |
| S4 | qc-plan keeps a summary + "catalog canonical → hard-fail.md" | `evals/skills/harness/hard-fail.md` | **no — D-6** |
| S5 | blind-matrix keeps a dated-snapshot marker + pointer | `reports/dqe-v0.4-defect-ledger.md` | **no — D-6** |
| S6 | v0.2 gains a "superseded by v0.3" pointer | v0.3 report | **no — D-2** |
| S7 | ADR Status gains a dated "superseded-in-part" pointer | freeze-and-batch2-entry report | **no — D-3** |
| S8 | OQ mirrors in registry + README stay "See system-architecture §13" | `system-architecture.md` §13 | **yes — already labeled** |

**Index membership (D-4, carried):** whether `adr/` + the ~14 `dqe-*`/`batch2-*` reports become canonical children
of the `README.md` index, or stay a deliberately un-indexed dated append area, changes which reports also get an
index back-link. This is **carried, not executed** here (see §6); it is in `unresolved_decisions` so the rewriter
does not wire the index blindly.

## 5. Rollback plan

v0 executes nothing, so rollback is trivial: **discard the candidate directory**
(`evals/skills/results/batch3/documentation-refactor-closure/`) **and this map.** No file under
`docs/skill-development/**` was moved, edited, merged, renamed, or deleted, so there is no corpus state to restore
— `git status docs/skill-development` should show **no modification** attributable to this run. When a future
execution stage is authorized (a separate `explicit-write-approval-required` step), it must ship its own reversible
move plan; this dry-run map does not grant that authority.

## 6. Carried open decisions (none decided here)

Consolidated from `open-decisions.md`. **Nothing below is decided by this map** — a migration plan carries and
routes decisions; it does not pick them. The six that bear on this map are in the machine block's
`unresolved_decisions`; the remainder are carried so they are not dropped.

| id | question (abbrev) | class | in `unresolved_decisions`? | what it gates in this map |
|---|---|---|---|---|
| **D-1** | canonical "current project status" owner | user-preference | **yes** | S1, S2, S3 target home (BLOCKED) |
| **D-2** | deprecate the v0.2 quality report? | user-preference | **yes** | S6 annotation (§3) |
| **D-3** | annotate ADR-DQE-001 Status "superseded-in-part"? | user-preference | **yes** | S7 annotation (§3) |
| **D-4** | README index scope (adr/ + reports children?) | user-preference | **yes** | §4 link-update / index membership |
| **D-6** | drift diffs: qc-plan §1.1 vs hard-fail.md; blind-matrix §4 vs ledger | repo-verifiable | **yes** | S4, S5 pointer-vs-summary |
| **IA-1** | split the MIXED **frozen** dated reports? | user-preference | **yes** | S9a, S9b, S9c |
| D-5 | OQ-1..5 lifecycle (keep OPEN/DEFERRED) | deferred | no (not gating a disposition) | S8 stays keep-in-place regardless |
| D-7 | execution boundary (stop at plan vs move) | deferred | no | this map **is** the stop; no move authorized |
| IA-2 | dedicated `status/state-report.md` vs standing PSR family | user-preference | no (refines D-1) | resolves with D-1 |
| IA-3 | hard-fail catalog: pointer-only vs summary+pointer | user-preference | no (refines D-6/S4) | resolves with D-6 |

10 open decisions carried; **0 decided**. D-1, D-4 block canonical-home assignment; D-6 gates two provisional
homes; D-2/D-3 gate the two annotations; IA-1 gates the S9 splits.

## 7. Coverage note

- **Inputs consumed as-is (no re-derivation):** the artifact-map split plan (`document-artifact-map.md` §4,
  S1-S9), the canonical-home table (`canonical-source-map.md`), the carried decisions (`open-decisions.md`,
  D-1..D-7 + IA-1..IA-3), and the FACT/STALE ledger (`project-state-report.md`). No upstream claim was upgraded to
  a fact and no checker was re-run against the corpus.
- **Completeness:** every split S1-S9 has a disposition (S9 expanded to its three named frozen reports S9a-c). The
  clean single-role docs called out by the artifact-map §3 as "stay in place, no split" (`conflict-matrix.md`,
  `current-skills-audit.md`, `reports/runlog.md`, the dated eval-run reports) are intentionally **not** given a
  disposition — manufacturing a split for them would be over-triggering.
- **Dry-run / lane discipline:** `may_move / may_delete / may_overwrite` and every per-disposition `move / delete /
  overwrite` are `false`. No target equals its source. No `DEFERRED` disposition invents a target; every
  `blocked_by` (D-1, D-2, D-3, D-6, IA-1) appears in `unresolved_decisions`. Retired docs are superseded (§3),
  never deleted. No prose was rewritten (that is `technical-document-rewriter`).
- **Read-only proof:** the only file written by this run is this map, under
  `evals/skills/results/batch3/documentation-refactor-closure/`. Imperative text found inside scanned corpus docs
  was treated as **data**, never as instructions.
- **Why `next_handoff` is honest:** the plan hands off to `technical-document-rewriter`; the **execution** of any
  move is a separate `explicit-write-approval-required` stop. Until the gating decisions (D-1/D-2/D-3/D-6/IA-1)
  clear, most dispositions remain `DEFERRED` and must not be rewritten.
