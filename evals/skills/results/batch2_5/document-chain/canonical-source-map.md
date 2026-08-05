<!--
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: 7919bc4
source_documents:
  - evals/skills/results/batch2_5/document-chain/document-artifact-map.md
  - evals/skills/results/batch2_5/document-chain/project-state-report.md
status: CANDIDATE (design plan; extracted from the document-artifact-map §2; homes borrowed from PSR are FACT, unresolved ones provisional/BLOCKED)
last_verified: 2026-08-05T15:00:00Z
-->

# Canonical Source Map — `docs/skill-development/` corpus

The **one-canonical-home-per-information-type** table (the HF-13 cure), extracted from
`document-artifact-map.md` §2 as a standalone lookup product. **This is a design plan, not an executed
migration** — no file was moved, rewritten, or deleted to produce it. FACT homes are **borrowed** from the PSR
state report (not re-verified here); provisional/BLOCKED homes depend on an unresolved fact or open decision
and must not be treated as settled.

## Legend

- **FACT** — canonical owner confirmed by `project-state-report.md`; borrowed as-is (CC-2). Firm design basis.
- **provisional** — home depends on a diff/currency check not yet done, or a lifecycle label not yet chosen.
- **BLOCKED** — no single owner can be assigned until an open decision is made (see `open-decisions.md`).
- **out of scope** — canonical file lives outside `docs/skill-development/**`; existence noted, currency UNKNOWN.

## Information-type → canonical home

| info type | canonical home | verdict | pointer/duplication note | ref |
|---|---|---|---|---|
| architecture · layers · call-chains · trigger ladder · norms · vocab · security | `system-architecture.md` §1–§12 | FACT | sole architecture doc | PSR `:89` |
| open questions OQ-1..OQ-5 | `system-architecture.md` §13 | FACT | registry + README copies stay **labeled mirrors** (O3) | PSR O3 |
| design rationale / DQE evaluation contract | `adr/ADR-DQE-001-…md` | FACT | Decisions 1–6 in force; forward "Phase E" framing STALE (C4, annotate) | PSR `:92` |
| phase roadmap · batches · DoD · exit criteria | `creation-roadmap.md` (**plan only**) | FACT | §0/§1 progress-tracker STALE (C2) → **pointer to status owner** | PSR `:91` |
| co-trigger / conflict / release-gate rules | `conflict-matrix.md` | FACT | single-role matrix | PSR |
| per-skill version / status / write-scope / evals | `skills-registry.yaml` (schema entries) | FACT | canonical version source (resolves C1); prose `meta:` narrative → pointer (C6) | PSR `:90` |
| skill audit / KEEP–REMOVE classification | `current-skills-audit.md` | FACT | single audit role | PSR |
| observability run log | `reports/runlog.md` | FACT | append-only; front-matter date STALE (C5) | PSR `:93` |
| QC policy + soft rubric + eval methodology | `quality-control-plan.md` | FACT | policy role canonical; catalog sub-type provisional (below) | PSR |
| DQE evaluation-output on the eoopt target | `reports/quality-report-…_v0.3-2026-07-31.md` | FACT | v0.3 authoritative; v0.2 → DEPRECATED pointer (C3/Or1, pending D-2) | PSR C3 |
| hard-fail catalog (as reusable data) | `evals/skills/harness/hard-fail.md` | provisional · out of scope | qc-plan §1.1 → summary+pointer once drift diffed (O1) | D-6 / U1 |
| DQE defect tracking (living register) | `reports/dqe-v0.4-defect-ledger.md` | provisional | confirm canonical vs `dqe-blind-matrix…` §4 dated snapshot (O2) | D-6 / U6 |
| upstream method attribution / license | `references/documentation-methodology/upstream-method-matrix.md` | provisional · out of scope | exists; currency UNKNOWN; cited canonical by 5+ docs | U2 |
| corpus index / navigation membership | `README.md` (index) | provisional | which reports/adr are canonical index children (Or2/Or3) | D-4 |
| **current project status · phase · batch progress (VOLATILE)** | **UNASSIGNED** — candidate: standing PSR **state report** / `status/`-dir (`system-architecture.md:198`) | **BLOCKED** | the HF-14b core; the **pointer target** every volatile split (S1–S3) needs | D-1 / IA-2 |

**Tally:** 10 FACT · 4 provisional · 1 BLOCKED.

## Volatile-state rule (the HF-14b cure, applied)

Volatile "current status / version roll-up / batch progress" is stored **once**, in its single owner (BLOCKED
on D-1), and referenced by **pointer** everywhere else. It must **never** be copied into a stable/living doc.
The three current copies — `README.md §0`, `creation-roadmap.md §0/§1`, `skills-registry.yaml meta:` — are
each scheduled to become a one-line pointer (splits S1–S3 in the artifact-map), **not** duplicated stores. The
highest-leverage instance is `creation-roadmap.md`'s "Batch 0 IN PROGRESS" tracker (C2), which misreports the
phase by ~2 batches; its cure is a pointer to the status owner / registry, not a copied count.
