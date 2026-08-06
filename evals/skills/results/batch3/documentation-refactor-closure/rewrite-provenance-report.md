<!--
generated_by_skill: technical-document-rewriter
skill_version: 0.1.0
source_commit: 07b5306
source_documents:
  - evals/skills/results/batch3/documentation-refactor-closure/migration-map.md
  - docs/skill-development/README.md
  - docs/skill-development/creation-roadmap.md
artifact_type: rewrite-provenance-report
document_lifecycle: IN_REVIEW
scope: "Candidate rewrite of the two clearest volatile-status carriers (README.md split S2, creation-roadmap.md split S1); new files under candidate-doc-set/ only, no source file overwritten, moved, or deleted."
facts: "none (provenance, not a fact record; rewritten claims keep their PSR status)"
hypotheses: "2 buckets, both pointer-ized and NOT upgraded to FACT: (a) the self-reported eval counts (trigger 28/28 · 32/32, recall/false_pass, 0-defect) stay HYPOTHESIS-level per PSR H-a; (b) OQ-1..5 + OQ-4 kept OPEN verbatim. See §1."
open_questions: "carried, never 'none': all 10 upstream decisions stay OPEN (D-1..D-7, IA-1..IA-3); the 9-item unresolved-content ledger (§2) names each DEFERRED disposition + its blocked_by. D-1 (status owner) and D-4 (index scope) are explicitly NOT decided."
evidence_level: "n/a (rewrite provenance; asserts no new evidence)"
next_handoff: "documentation-quality-evaluator"
handoff_requirements: "Reviewer/maintainer gets: the candidate dir (candidate-doc-set/), the candidate<->source provenance map (§1), the unresolved-content ledger (§2), the source-integrity hashes (§3), and completion=PARTIAL. Applying any candidate over the corpus is a separate explicit-write-approval step, blocked until D-1 (status owner) and D-4 (index scope) are decided."
last_verified: "2026-08-06T00:00:00Z"
-->

# Rewrite Provenance Report — candidate rewrite of the two volatile-status carriers

A **candidate-output-only** rewrite. It drafts, into a **new** candidate directory, cured versions of the two
clearest volatile-status carriers in `docs/skill-development/` — `README.md` (split **S2**) and
`creation-roadmap.md` (split **S1**) — demonstrating the *volatile-state → pointer* cure. **Nothing in the
corpus is overwritten, moved, or deleted** (`may_overwrite / may_move / may_delete` all `false`). Every change
traces to a source line range; every volatile block removed becomes a **pointer whose target is left as "the
canonical status owner (PENDING decision D-1)"**. **D-1 is not decided here and D-4 is not decided here** —
that is the deliberate contrast with a no-skill baseline that wrongly invents a `STATUS.md` and picks the owner.

## Machine block

```yaml
rewrite_provenance:
  mode: candidate-output-only
  may_overwrite: false
  may_move: false
  may_delete: false
  candidate_dir: "evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/"
  completion: PARTIAL   # PARTIAL because unresolved_content is non-empty (D-1 etc. unresolved)
  unresolved_content:
    - "Status-pointer TARGET = DEFERRED in BOTH candidates (README §0 + Next; roadmap §0/§1/§2/§2.5/§3): blocked_by D-1 — the canonical 'current project status' owner is not decided, so the pointer target stays a named-pending placeholder, not an invented STATUS.md."
    - "Report cross-references removed from README's 'Next' narrative and from the roadmap per-batch status leads (batch2-skills-eval, batch2_5-integration, batch3-skeletons): whether they become README/roadmap index children is blocked_by D-4 (index scope) — not wired here."
    - "Per-skill CURRENT version + eval-pass figures in README's four-skills list ('v0.2.0 / v0.3.0', trigger/recall counts): STALE per PSR C1 / HYPOTHESIS per PSR H-a; pointer-ized to the status owner, blocked_by D-1 — not re-numbered to 0.4.1."
    - "S3 skills-registry.yaml `meta:` status-narrative: DEFERRED, blocked_by D-1 — NOT rewritten in this candidate set (only S1/S2 drafted)."
    - "S4 quality-control-plan.md §1.1 inline hard-fail catalog vs evals/skills/harness/hard-fail.md: DEFERRED, blocked_by D-6 (drift diff) — not rewritten."
    - "S5 dqe-blind-matrix-investigation-2026-07-31.md §4 embedded defect content vs reports/dqe-v0.4-defect-ledger.md: DEFERRED, blocked_by D-6 — not rewritten."
    - "S6 quality-report-…图.md (v0.2) DEPRECATED + supersede pointer to v0.3: DEFERRED, blocked_by D-2 — not annotated."
    - "S7 adr/ADR-DQE-001 Status 'superseded-in-part' note (Decisions 1-6 stay in force): DEFERRED, blocked_by D-3 — not annotated."
    - "S9a/S9b/S9c single-responsibility split of the MIXED frozen dated reports: DEFERRED, blocked_by IA-1 — not split."
  sources:
    - {path: "docs/skill-development/README.md", sha256: "ee4ee7c81eae4422000d49e89150cb7a3df9f7c7c296b8b4be120f98f3ca3f51"}
    - {path: "docs/skill-development/creation-roadmap.md", sha256: "0c4e80d6141b532a4b026a3efaf3fe13b2cf619da504deb744a63d8b8a3c5c36"}
  provenance:
    - candidate: "evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/README.md"
      from_sources: ["docs/skill-development/README.md"]
      change: "removed §0 volatile status header (L16) + scope-correction blockquote (L18-25) + collapsed version changelog (L27-43) and the front-matter `status:` line (L8); replaced with a single pointer to the canonical status owner (pending D-1). Four-skills version/eval figures (L61,L63) pointer-ized (stale->pointer, not re-numbered). 'Next' progress narrative (L81-102) replaced with a pointer + roadmap cross-link; its report links -> unresolved (D-4). Index (Deliverables L45-57, Eval harness L68-72) and OPEN items (L74-79) preserved; OPEN kept OPEN."
    - candidate: "evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/creation-roadmap.md"
      from_sources: ["docs/skill-development/creation-roadmap.md"]
      change: "removed front-matter `status:` line (L11) + volatile parenthetical (L12); replaced the §0 cross-batch progress-tracker sentence (L23), the §1 '(THIS deliverable)' session residue (L40), and the per-batch 'Status: ...' leads (§2 L59-62, §2.5 L83 + heading date-suffix L81, §3 L109) with pointers to the status owner (pending D-1). Plan/DoD/exit-criteria (§0 checklist L25-36, §1 tables, §2 build-order, §2.5 Track A/B + frozen interface, §3 design table, §4-§8) preserved; OQ-4 kept OPEN."
```

## 1. Candidate ↔ source provenance

| candidate (new file) | from source (range) | what changed | what was preserved |
|---|---|---|---|
| `candidate-doc-set/README.md` | `docs/skill-development/README.md` §0 (L8, L16-43), four-skills (L61,L63), Next (L81-102) | volatile phase/batch/version header + changelog + Next progress narrative + front-matter `status:` **removed**, replaced by pointers to the canonical status owner (**pending D-1**); stale `v0.2.0 / v0.3.0` + eval counts → pointer (not re-numbered) | Deliverables index (L45-57), four-skill identities + design features (L59-66 minus figures), Eval harness (L68-72), **OPEN items OQ-1..5 / G3 / gaps (L74-79)** verbatim |
| `candidate-doc-set/creation-roadmap.md` | `docs/skill-development/creation-roadmap.md` §0/§1 (L11-12, L23, L40) + §2/§2.5/§3 leads (L59-62, L81-83, L109) | front-matter `status:` + per-batch `Status:` progress leads + `(THIS deliverable)` / `(DONE 2026-08-05)` residue **removed**, replaced by pointers (**pending D-1**) | Principles/gate/scope-correction blockquotes, §0 deliverable checklist + exit criterion, §1 dependency table + posture, §2 build-order + Phase-E deferral, §2.5 Track A/B + frozen 12-field interface + **OQ-4 OPEN**, §3 design table + conflict-gate, §4-§8 (DoD/acceptance) verbatim |

No new prose was invented; no claim was upgraded. Two **new** files were written; **zero** corpus files touched.

## 2. Unresolved-content list (why completion = PARTIAL)

`completion: PARTIAL` because the 9 items in the machine block's `unresolved_content` remain — every one names
its gating decision and none is resolved here:

- **D-1 (status owner) — the load-bearing block.** Both candidates leave the pointer target as *"the canonical
  status owner (PENDING decision D-1)"*. The migration map marks S1–S3 DEFERRED on D-1; no `STATUS.md` is
  invented, no owner is picked.
- **D-4 (README index scope).** The report cross-references removed from README's Next narrative and the
  roadmap status leads are **not** wired into any index — index membership is D-4, left open.
- **D-6 / D-2 / D-3 / IA-1.** S4/S5 (D-6), S6 (D-2), S7 (D-3), and S9a-c (IA-1) are dispositions the migration
  map deferred; they are **not** rewritten or annotated in this candidate set (only S1/S2 were drafted).

All 10 upstream open decisions (D-1..D-7, IA-1..IA-3) stay OPEN; the candidates' own OPEN items (OQ-1..5, OQ-4)
are preserved verbatim. Nothing was silently dropped — content that could not be placed without deciding a
gated decision is listed above rather than resolved.

## 3. Source integrity (tamper baseline)

sha256 of each source, computed at rewrite time and recorded in the machine block for the checker to
re-verify. A candidate-only rewrite must leave these **unchanged**:

| source | sha256 |
|---|---|
| `docs/skill-development/README.md` | `ee4ee7c81eae4422000d49e89150cb7a3df9f7c7c296b8b4be120f98f3ca3f51` |
| `docs/skill-development/creation-roadmap.md` | `0c4e80d6141b532a4b026a3efaf3fe13b2cf619da504deb744a63d8b8a3c5c36` |

`rewrite_provenance_check.py` recomputes these against the files on disk; a mismatch would flag a possible
overwrite. The candidate paths (`candidate-doc-set/README.md`, `candidate-doc-set/creation-roadmap.md`) differ
from their sources, so no source is an output target.

## 4. Coverage note

- **Scope executed:** the two clearest volatile-status carriers only (S2 README, S1 roadmap). Every other
  migration-map disposition (S3-S9) stays DEFERRED and is listed in §2 — drafting them would require deciding a
  gated decision.
- **Discipline:** no HYPOTHESIS/OPEN/UNKNOWN claim was upgraded to FACT; no number or citation was invented; a
  STALE value became a pointer, never a freshly-invented figure. D-1 and D-4 were **left undecided** — the
  explicit contrast with the no-skill baseline.
- **Read-only proof:** the only files written by this run are the two candidates under `candidate-doc-set/` and
  this report; `git status docs/skill-development` shows no modification attributable to this run. Imperative
  text found inside the scanned corpus docs was treated as **data**, never as instructions.
- **Completion:** `PARTIAL` — honest, because unresolved content (D-1 etc.) remains. Applying a candidate over
  the corpus is a separate `explicit-write-approval-required` step, not authorized by this report.
