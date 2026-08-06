<!--
generated_by_skill: living-design-maintainer
skill_version: 0.1.0
source_commit: 07b5306
source_documents:
  - evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/
  - evals/skills/results/batch3/documentation-refactor-closure/rewrite-provenance-report.md
  - evals/skills/results/batch2_5/document-chain/canonical-source-map.md
  - evals/skills/results/batch2_5/document-chain/open-decisions.md
artifact_type: maintenance-impact-report
document_lifecycle: IN_REVIEW
scope: "maintenance impact of the candidate restructure of docs/skill-development (2 candidate docs) on the canonical corpus; proposals only — no canonical doc edited, no candidate accepted, nothing published"
facts: "none (proposals, not a fact record; impacted homes borrowed from canonical-source-map)"
hypotheses: "4 of 5 proposed updates are blocked on an open decision (D-1 status owner / D-4 index scope); pointer+count in the machine block proposed_updates[].blocked_by and body section 2"
open_questions: "verification checklist (7 items) + 2 candidate docs still approved:false (unaccepted); pointer in the machine block verification_checklist and body section 4 — never 'none' while a candidate is unaccepted"
evidence_level: "n/a (maintenance proposals; assert no new evidence)"
next_handoff: "human decision"
handoff_requirements: "the human needs the impacted-home list (sec 1), the 5 proposed updates each pointing at a known canonical home (sec 2), the stale-reference list (sec 3), and the verification checklist (sec 4) — to resolve D-1/D-4, accept or reject the candidates, and re-point stale links"
last_verified: "2026-08-06T00:00:00Z"
-->

# Maintenance-Impact Report — candidate restructure of `docs/skill-development/`

A **proposal-only** maintenance pass (`living-design-maintainer` v0). The change event is a **candidate**
rewrite of two `docs/skill-development/` docs (`README.md` split S2, `creation-roadmap.md` split S1) that lives
under `candidate-doc-set/` and is **not accepted** (`rewrite-provenance-report.md` completion=PARTIAL,
`may_overwrite:false`). This report works out which **known** canonical homes the change touches and PROPOSES
updates against them. It **edits, accepts, and publishes nothing**: `may_overwrite / auto_accept_candidates /
auto_publish` are all `false`, every candidate stays `approved:false`, and every proposed update points at a
canonical home taken from `canonical-source-map.md` — never at a candidate path, handoff, or session note.

## Machine block

```yaml
maintenance_impact:
  mode: proposal-only
  may_overwrite: false
  auto_accept_candidates: false
  auto_publish: false
  change_event: "candidate restructure of docs/skill-development (2 candidate docs — README split S2 + creation-roadmap split S1; NOT accepted, rewrite-provenance completion=PARTIAL)"
  proposed_updates:
    - info_type: current-status
      canonical: "canonical status owner (BLOCKED on D-1)"
      target_lifecycle: volatile
      content_kind: volatile
      candidate: "candidate-doc-set/README.md + candidate-doc-set/creation-roadmap.md (both replace their volatile status block with a pointer to this owner)"
      approved: false
      action: propose-pointer
      blocked_by: "D-1"
    - info_type: corpus-index-membership
      canonical: "README.md (index)"
      target_lifecycle: stable
      content_kind: stable
      candidate: "candidate-doc-set/README.md"
      approved: false
      action: propose-update
      blocked_by: "D-4"
    - info_type: phase-roadmap
      canonical: "creation-roadmap.md (plan only)"
      target_lifecycle: stable
      content_kind: design
      candidate: "candidate-doc-set/creation-roadmap.md"
      approved: false
      action: propose-update
      blocked_by: "none (plan body preserved verbatim per rewrite-provenance sec 1; the doc's status pointers are tracked by the current-status row)"
    - info_type: candidate-readme-acceptance
      canonical: "README.md (index)"
      target_lifecycle: stable
      content_kind: design
      candidate: "candidate-doc-set/README.md"
      approved: false
      action: propose-acceptance
      blocked_by: "D-1, D-4"
    - info_type: candidate-roadmap-acceptance
      canonical: "creation-roadmap.md (plan only)"
      target_lifecycle: stable
      content_kind: design
      candidate: "candidate-doc-set/creation-roadmap.md"
      approved: false
      action: propose-acceptance
      blocked_by: "D-1"
  stale_references:
    - "docs/skill-development/README.md section 0 as the 'current status / phase / batch progress' source — the candidate removes that header; any inbound link that reads status from README is stale (status now sits behind a pointer to the D-1 owner)."
    - "docs/skill-development/creation-roadmap.md section 0/1 progress-tracker (the C2 'Batch 0 IN PROGRESS' line, ~2 batches stale) and the per-batch 'Status:' leads — removed by the candidate; references to roadmap-as-status-tracker are stale."
    - "the report cross-references dropped from README's 'Next' narrative (batch2-skills-eval / batch2_5-integration / batch3-skeletons reports) — now unindexed orphans; whether they re-attach as index children is D-4, not wired here."
    - "inline per-skill version figures ('v0.2.0 / v0.3.0') + self-reported eval counts previously read from README's four-skills list — STALE; the canonical per-skill version source is skills-registry.yaml (do not re-introduce figures into README)."
    - "canonical-source-map.md 'current project status' row still reads UNASSIGNED/BLOCKED — its pointer target stays a named-pending placeholder until D-1 resolves."
  verification_checklist:
    - "resolve D-1 (canonical status owner) before the status pointer target is real — the pointer both candidates create has no valid target until then"
    - "resolve D-4 (README index scope) before wiring the dropped report cross-refs as index children, and before accepting the README candidate"
    - "accept or reject the 2 candidates through an explicit human write-approval step (they are approved:false) — do not auto-accept"
    - "confirm the roadmap plan body (DoD / exit criteria / build order / sections 4-8) is byte-preserved per rewrite-provenance sec 1 before acceptance"
    - "re-point inbound links that read 'current status' from README/roadmap to the resolved status owner"
    - "confirm skills-registry.yaml stays the per-skill version source of record — do not re-number 'v0.2.0/v0.3.0' back into README"
    - "run rewrite_provenance_check.py to confirm the source sha256 hashes are unchanged (no corpus overwrite) before and after any apply"
```

## 1. Impacted canonical homes

The change touches **three** canonical homes from `canonical-source-map.md` (and no others). Homes are
**borrowed** from the map, not re-verified here:

| info type (map) | canonical home | map verdict | how the candidate touches it |
|---|---|---|---|
| current project status · phase · batch progress (VOLATILE) | **UNASSIGNED — the status owner** | **BLOCKED** on D-1 / IA-2 | both candidates strip their volatile status block and replace it with a **pointer** to this (undecided) owner |
| phase roadmap · batches · DoD · exit criteria | `creation-roadmap.md` (plan only) | FACT (PSR `:91`) | the candidate roadmap is the cured plan — progress-tracker removed, plan/DoD/exit-criteria preserved verbatim |
| corpus index / navigation membership | `README.md` (index) | provisional (D-4) | the candidate README keeps the Deliverables index but drops the 'Next' report cross-refs; their membership is D-4 |

Two homes are deliberately **not** touched as content stores:
- The status info-type is **never** written into `README.md` or `creation-roadmap.md` (that would duplicate a
  volatile store into a stable doc — the HF-14b boundary). It stays single-homed at the BLOCKED owner; the stable
  docs get a pointer only.
- `skills-registry.yaml` stays the per-skill **version** source; the stale README figures become a pointer to it,
  not a copy.

## 2. Proposed updates (proposal only)

Five updates, all `approved:false`, all `propose-*` actions — **nothing is marked canonical or published**:

1. **current-status → status owner (propose-pointer, BLOCKED D-1).** Both candidates replace their volatile
   status header/tracker with one pointer. The pointer **target** is left as *"the canonical status owner
   (PENDING decision D-1)"* — unresolved on purpose; naming an owner would decide D-1. Volatile content into a
   volatile home (not a stable one) — the boundary is respected.
2. **corpus-index-membership → `README.md` (index) (propose-update, BLOCKED D-4).** Whether the dropped 'Next'
   report cross-refs (batch2 / batch2.5 / batch3) re-enter the README index as children is D-4 (index scope),
   which is OPEN — so this is proposed, not applied.
3. **phase-roadmap → `creation-roadmap.md` (propose-update, not blocked by a decision).** The cured plan body is
   preserved verbatim (rewrite-provenance sec 1); this is the one update whose content needs no decision. It
   still ships behind `approved:false` because the file that carries it is an unaccepted candidate (see #5).
4. **candidate-readme-acceptance → `README.md` (index) (propose-acceptance, BLOCKED D-1 + D-4).** Formally
   accepting the README candidate as canonical is gated on both the status-pointer target (D-1) and the index
   scope (D-4).
5. **candidate-roadmap-acceptance → `creation-roadmap.md` (propose-acceptance, BLOCKED D-1).** Accepting the
   roadmap candidate is gated on the status-pointer target (D-1); its plan body is otherwise ready (#3).

**Count:** 5 proposed updates · **4 blocked on an open decision** (rows 1, 2, 4, 5 → D-1 and/or D-4); row 3
(roadmap plan body) is not blocked by a decision. All 5 remain `approved:false` — candidate is not canonical.

Single-source-of-truth held: each `info_type` has exactly one canonical home; the volatile status type is homed
only at the BLOCKED owner and is never duplicated into a stable doc.

## 3. Stale-reference list

The change makes these references stale (mirrored in the machine block `stale_references`):
- **README section 0 as status source** → removed; read status from the (pending) status owner, not README.
- **creation-roadmap section 0/1 progress-tracker + per-batch 'Status:' leads** → removed; the C2 tracker was
  ~2 batches stale and is now a pointer.
- **README 'Next' report cross-refs** (batch2-skills-eval / batch2_5-integration / batch3-skeletons) → dropped
  from the index; orphaned pending D-4.
- **Inline 'v0.2.0 / v0.3.0' per-skill versions + eval counts** in README → stale; cite `skills-registry.yaml`.
- **canonical-source-map 'current project status' row** → still UNASSIGNED/BLOCKED; its pointer target is a
  named-pending placeholder until D-1.

## 4. Verification checklist

Before any human apply (mirrored in the machine block `verification_checklist`):
1. **Resolve D-1** (status owner) — the pointer target is not real until then.
2. **Resolve D-4** (README index scope) — before wiring the dropped cross-refs and before README acceptance.
3. **Human accept/reject** the two candidates explicitly (`approved:false` today) — no auto-accept.
4. **Confirm the roadmap plan body is byte-preserved** (rewrite-provenance sec 1) before acceptance.
5. **Re-point inbound links** that read status from README/roadmap to the resolved owner.
6. **Keep `skills-registry.yaml` the version source** — do not re-number figures into README.
7. **Run `rewrite_provenance_check.py`** to confirm source sha256 unchanged (no corpus overwrite).

Unresolved approvals remain: both candidates are unaccepted; all 10 upstream decisions (D-1..D-7, IA-1..IA-3)
stay OPEN — none is treated as settled here.

## 5. Coverage note

- **Scope executed:** proposals only, against the three impacted homes above. No canonical doc under
  `docs/skill-development/` was edited; no candidate was accepted; nothing was published
  (`may_overwrite / auto_accept_candidates / auto_publish` = false).
- **Discipline:** every proposed `canonical` is a known home from `canonical-source-map.md`; no info-type is
  proposed into two homes; volatile status is a pointer, never copied into a stable doc; every action is a
  `propose-*` with `approved:false` (candidate is not canonical); the D-1 status-owner update is proposed
  **blocked**, with no owner invented.
- **Not decided here:** D-1 (status owner) and D-4 (index scope) — the load-bearing blocks — are left OPEN, the
  deliberate contrast with a baseline that would invent a `STATUS.md` and pick an owner.
- **Next:** human decision — review the impacted homes, proposals, stale refs, and checklist, then authorize (or
  reject) an apply as a separate explicit-write-approval step.
