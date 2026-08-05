<!--
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: 7919bc4
source_documents:
  - evals/skills/results/batch2_5/document-chain/goal-scope-note.md
  - evals/skills/results/batch2_5/document-chain/project-state-report.md
  - evals/skills/results/batch2_5/document-chain/document-artifact-map.md
status: OPEN (10 decisions; none decided here — a plan raises, it does not pick)
last_verified: 2026-08-05T15:00:00Z
-->

# Open Decisions — `docs/skill-development/` information architecture

Consolidated list handed to `uncertainty-and-decision-manager` (decision register) and the user. **Nothing
below is decided here** — `document-information-architect` raises canonical-home ambiguities and human-preference
items; it does not pick them silently. **D-1..D-7** are carried from `goal-scope-note.md`; **IA-1..IA-3** are new
canonical-home ambiguities this IA surfaced while designing the artifact-map. Classifications:
`user-preference` (only the user can choose), `repo-verifiable` (resolve by diff/inspection, no human),
`deferred` (frozen for now).

## Blocking canonical-home assignment (must be decided before any migration)

| id | question | class | what it blocks | IA recommendation (NOT a decision) |
|---|---|---|---|---|
| **D-1** | Which surface is the canonical **"current project status"** owner — `README.md §0`, `…freeze-and-batch2-entry…md`, `skills-registry.yaml meta:`, or a standing PSR **state report** (`system-architecture.md:198`)? (C6 / PSR ASK-HUMAN Q1) | user-preference | the entire volatile-status home (artifact-map §2 BLOCKED row) + splits S1–S3 have **no pointer target** until this is set | make the standing state report the single owner; reduce the other three surfaces to pointers. Do not assign silently. |
| **D-4** | **README index scope** — extend the Deliverables index to `adr/` + the ~14 `dqe-*`/`batch2-*` reports, or is `reports/` a deliberately un-indexed dated append area? (Or2/Or3 / Q4) | user-preference | the index-membership canonical home (artifact-map §2) | put to user; determines whether ~15 reports are "orphans to wire up" or an intentional append area. |

## Gating two provisional homes (resolvable without a human)

| id | question | class | what it gates | next action |
|---|---|---|---|---|
| **D-6** | Has `quality-control-plan.md §1.1` drifted from `evals/skills/harness/hard-fail.md` (O1/U1)? Is `dqe-blind-matrix…md §4` a true duplicate of the standalone defect-ledger or a dated snapshot (O2/U6)? | repo-verifiable | splits **S4** (hard-fail catalog → pointer vs summary+pointer) + **S5** (defect-ledger canonical confirm) | run the two diffs; canonical file wins if drifted, keep-as-snapshot if dated. No human needed. |

## Carried human-preference / deferred items (affect the plan; decided by user / register)

| id | question | class | plan touchpoint | IA recommendation (NOT a decision) |
|---|---|---|---|---|
| **D-2** | Deprecate the **v0.2 quality report** (`quality-report-…图.md`) now that v0.3 supersedes it? (C3 / Q2) | user-preference | split **S6** | mark `document_lifecycle: DEPRECATED` + pointer to v0.3 (it is also an orphan, Or1). Do not relabel here. |
| **D-3** | Annotate **`ADR-DQE-001` Status** with a dated "superseded-in-part by the 2026-08-05 advisory freeze" note? (C4 / Q3) | user-preference | split **S7** | add the note; Decisions 1–6 stay in force. Do not edit the ADR here. |
| **D-5** | **OQ-1..OQ-5 lifecycle** — keep OPEN/DEFERRED, owned by user/project? (Q5) | deferred | role 3 / info-type OQ home | carry forward OPEN/DEFERRED; arch §13 stays canonical (CC-4). Do not silently close. |
| **D-7** | **Execution boundary** — stop at the `document-artifact-map`, or proceed to actually move/rewrite files? | deferred | `next_handoff` | effort ends at this map + an honest **BLOCKED** execution handoff (Batch-5 tooling not built). Manual migration is a separate user authorization. |

## New IA canonical-home ambiguities (surfaced designing the artifact-map)

| id | question | class | plan touchpoint | IA recommendation (NOT a decision) |
|---|---|---|---|---|
| **IA-1** | Split the **MIXED frozen dated reports** (`…独立检查失败复盘…md` 952L = post-mortem+spec+test-plan+task-list; `dqe-v0.4.1-diagnostic-close` = close-out+incident+contract-fix+decision; `dqe-v0.4.1-freeze-and-batch2-entry` = decision+changelog+state) into single-responsibility docs, or accept role-mixing in records that **don't drift**? | user-preference | split **S9** | leave as-is for now — frozen dated records don't drift, so the HF-13 cost is low; revisit only if one is promoted to a living doc. Raised, not forced. |
| **IA-2** | Create a **dedicated `docs/skill-development/status/state-report.md`** as the current-status owner, or let the **standing PSR-report family** itself serve that role? (refines D-1) | user-preference | target doc-set §3 (NEW row) + BLOCKED home | prefer a standing `status/` state report the PSR chain refreshes, so status has a stable path AND a verified-fact provenance. Contingent on D-1. |
| **IA-3** | Hard-fail catalog in `quality-control-plan.md §1.1` — **pointer-only** to `hard-fail.md`, or a short **summary + pointer**? (the residual design choice even after D-6's drift result) | user-preference | split **S4** | summary + pointer if D-6 shows no drift (readability without a second store); pointer-only if drifted. |

---

**Discipline check:** 10 open decisions raised; **zero decided**. D-1 and D-4 block canonical-home assignment;
D-6 gates two provisional homes; the rest are recorded with a recommendation but left to the user/register. No
file in the corpus was moved, edited, merged, or deleted to produce this list.
