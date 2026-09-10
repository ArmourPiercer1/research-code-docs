# Revised Phase-2 vertical slice (repair round, R9)

```yaml
date: 2026-09-10
status: PROPOSED (D-1 DECIDED by the final external-review ruling: option A — the
         slice lands the note in decided/)
supersedes: target-capability-architecture.md §7 (original slice, kept for the record)
basis: repair guide R9 + R10 + R11; post-audit-reconciliation.md §4 (candidate pool)
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ./README.md; 2026-09-10, final consistency patch)
```

## 1. Why the original slice is revised

The repair guide (R9) rejects the original §7 slice's shape on four counts:

1. **Synthetic loop, not a simplification.** The original loop was a duplicate-census
   (PSR → WFI → UDM → LDM → before/after duplicate count). R9 requires the slice to start
   from a REAL messy repo and close ONE simplification end-to-end — the actual
   remove-side ratchet event, not a measurement exercise on a planted census.
2. **WFI as a mandatory stage.** R9: WFI participates only if actually needed. It is not a
   stage by default.
3. **Full checker portfolio on first run.** R9/R11: the slice uses the MINIMUM checker
   set; the rest ride with their build phase.
4. **Quota-style deletion proof.** R10.3: the slice's proof is the planted obsolescence
   being removed with justification, not "≥1 removal per N iterations".

## 2. The slice (one candidate, end-to-end)

**Candidate (selected from the still-live pool, post-audit-reconciliation §4):** archive
the VOID `creation-roadmap.md` (VOID since 2026-09-09, commit 62ada30, still tracked and
still referenced at 3bb307f — the D12 live class) and re-point every inbound reference.

```text
inputs:  this repo at the slice-start commit (real messy governance corpus; the
         still-live D-defects of post-audit-reconciliation §1; the planted adversarial
         defect 1 from File 5 §c — a second stale roadmap, D12 class)
chain:   1. PSR — read-only fact recovery of the governance corpus (budgeted)
         2. simplification-audit (A8) — consumer classification over the still-live
            candidate pool; WFI document-corpus inventory participates HERE, as the
            audit's mechanical half, because the audit needs the consumer graph
            (R9: participation documented, not assumed)
         3. ONE selected evidence-backed candidate (the archive-VOID-roadmap candidate;
            selection evidence: the VOID banner + 0 active consumers + D12 live instance)
         4. UDM / decision note — ONLY for the durable judgment the candidate forces:
            D-1 (which doc owns "what is next" after the roadmap leaves). DECIDED by
            the final external-review ruling (option A — the reconstruction status
            table); the note lands in docs/decision-notes/decided/ recording the
            ruling (P8: no fiat — the note records the ruling, it does not make it)
         5. host agent IMPLEMENTS — archive move + banner, inbound pointer fixes
            (DQE SKILL.md:9 class, D9/D12/G4), registry `meta:` note cleanup, the
            .gitignore / tracking transition (git add + commit of
            docs/plans/active/** + docs/plans/archived/** — the archive destination
            must be tracked for the move to be valid, final patch P2); no more,
            no less
         6. focused-verification (A9) — the smallest relevant subset (see §4)
         7. two-axis review — standards vs spec (the code-review pattern; both axes
            recorded side by side)
         8. same-change canonical-owner update (LDM direction) — status table (File 3
            row 4b), SKILL.md builtness line (D14), README flow count (D1)
outputs: the archived roadmap + fixed pointers; the D-1 decision note (decided/ —
         records the final ruling, option A); the Phase-2 canonical stores (§4.5);
         the focused-verification record; the two-axis review record; before/after
         evidence (§5); flow-state
```

## 3. Stage notes

- **Stage 2 (A8):** the audit consumes PSR's fact recovery + the WFI consumer graph.
  Output: the candidate pool ranked by evidence (each candidate names its consumers, its
  staleness proof, and its removal justification). The slice proceeds with exactly ONE
  candidate — R9's "ONE candidate", not a batch.
- **Stage 4 (D-1):** the archive is impossible without deciding where "what is next"
  points after the roadmap leaves. D-1 is DECIDED (final external-review ruling,
  option A — the reconstruction status table); the note lands in `decided/` recording
  the ruling (the D-1_LEFT_OPEN assertion class — P8: 0 silent decisions — remains the
  standing guard for future decisions). The decided note is in §6 below.
- **Stage 5 (implement):** the slice's write surface is the archive move + the named
  pointer fixes + the .gitignore / tracking transition (P2). Anything beyond that
  scope is a scope violation (change-scope input to canonical-impact-lint).
- **Stage 7 (two-axis review):** axis 1 = standards (the repo's documented conventions:
  freeze rules, banner format, pointer style); axis 2 = spec (does the change do exactly
  what the slice contract says — nothing more, nothing less). Both recorded.

## 4. Focused verification (A9 — the smallest relevant subset, I8)

| Check | Why it is in the subset |
|---|---|
| `preflight.py` | the standing structural gate (existing, unmodified) |
| `markdown_links_check` (banner-aware extension) | the archive move breaks/fixes pointers — the direct risk |
| dead-pointer check (same extension) | VOID/archived targets must resolve to the archive banner |
| `archive-lint` | the move is an archive event: banner present, supersedee dated, location in `docs/plans/archived/` |
| `supersession-lint` | the roadmap's VOID banner must satisfy the supersession annotation rule |
| `decision-note-lint` | the D-1 note's format (required sections; rejection_basis if ever rejected) |
| `canonical-impact-lint` (with change-scope input) | every file in the change's declared impact set was same-change-updated or explicitly marked no-impact (R2) |
| affected eval cases | the docref-conf-03 re-baseline + the D14 builtness-claim cases (the touched claims) |

Explicitly NOT in the subset: the full run_checks tier run, the blind-run suites, the
corpus mutation checks (no corpus touched), DQE grading (advisory only, Rule 0). If the
subset passes and any excluded check is later found relevant, it is ADDED to the slice's
verification record (ratchet-up), not discovered silently.

### 4.5 Canonical stores created during Phase 2 (final patch P8)

| Store | State at slice start | Created during Phase 2 |
|---|---|---|
| `docs/decision-notes/` (`decided/` + `proposed/` + `archived/`) | absent | yes — folder skeleton + the D-1 note in `decided/` |
| `docs/decision-register.md` | absent | yes — seeded per the import rule below (the slice's UDM interaction requires it) |
| `docs/canonical-source-map.md` (R6 single manual authority) | absent (the harness table is the interim map) | yes — created in the same change; `evals/skills/harness/canonical-source-map.md` becomes its thin pointer |
| `docs/plans/archived/` (the archive destination) | present as a directory, NOT tracked (the blanket `docs/plans/` ignore) | tracked via the Stage-5 tracking transition (P2) |
| `docs/plans/active/` (canonical working state, incl. the status table) | present, NOT tracked | tracked via the same transition (P2) |
| the status table (`reconstruction/README.md`, the D-1 owner) | present | unchanged — only becomes tracked |

**Register seed rule (initial migration/import):** the register is seeded ONLY with
entries this slice itself creates or touches — the D-1 decision (object_type:
design_decision, decided, implementation_state: not_applicable) and the reconstruction
program route (object_type: route, decided, implementation_state: none — the route the
slice itself advances). No backfill of historical decisions; each seeded entry cites
its source document. Later phases import more only through same-change updates.

Every other canonical path referenced by the slice is either already present or
explicitly deferred and not required by the slice (Phase-3 stores are NOT created
early).

## 5. Before/after evidence (the proof, all mechanically checkable)

| Evidence | Before (slice-start commit) | After (slice-end commit) |
|---|---|---|
| `creation-roadmap.md` location | `docs/skill-development/` (tracked, VOID banner) | `docs/plans/archived/` (tracked, banner intact) |
| inbound references to the old path | 1 (DQE SKILL.md:9 class) — dead-pointer count = 1 | 0 — dead-pointer count = 0 |
| planted defect 1 (second stale roadmap) | present, UNDETECTED (baseline) | DETECTED AND NAMED (canonical-impact-lint or PSR state report) |
| canonical-impact-lint on the change's impact set | (baseline run on the slice's own change) | GREEN: every impact-set member same-change-updated or no-impact declared |
| archive-lint / supersession-lint | n/a (not yet built) → built in-slice, self-tested on the planted instance | GREEN |
| decision-note-lint on D-1 note | n/a | GREEN (format) — decision state = decided, recording the final ruling (0 silent decisions) |
| sha256 of files outside the declared impact set | recorded | unchanged (0 unrelated files touched) |
| two-axis review | — | both axes recorded, no unaddressed axis-2 (spec) findings |
| persistent artifacts added | — | `persistent_artifact_count`: REPORT ONLY (this change: the D-1 note + the archived banner record) — each artifact carries unique_responsibility / canonical_owner / consumer / lifecycle / archive_or_delete_condition; fail ONLY on: two artifacts carry the same canonical fact, an artifact has no consumer, no lifecycle, exists only for process ceremony, or growth is monotone without capability gain (R10.4 + final patch P5) |

**Success criteria (checker-verifiable, no model judgment):** the after column holds on
every row; the planted defect was detected AND named; the D-1 note is in `decided/`
recording the final ruling (option A) — never silently fiat'd; the artifact-count
predicates (last evidence row) hold; the two-axis review recorded both axes.

## 6. The D-1 decision note (DECIDED — lands in `docs/decision-notes/decided/`)

```yaml
id: D-1
status: decided   # final external-review ruling: option A (2026-09-10); the note
                  # records the ruling — the slice does NOT self-decide (P8)
object_type: design_decision
epistemic_state: supported
decision_state: decided
evidence_level: E3
evidence_state: current
implementation_state: not_applicable
ruling: option A — docs/plans/active/reconstruction/README.md status table is the
  single canonical owner of "current execution status / what is next"
semantic_division: decision register = what has been decided / what remains open;
  system architecture = what the system currently is; status table = what is being
  worked on now and what comes next
problem: after creation-roadmap.md is archived, which document owns "what is next"?
evidence: at 3bb307f the roadmap is VOID (62ada30) yet still the de-facto next-pointer
  (D12 live class; File 3 row 4 split: 4b names the owner); 3 candidate homes exist.
alternatives:
  A: docs/plans/active/reconstruction/README.md status table (the single "what is next"
     owner — File 3 row 4b)
  B: the decision register's active rows (register = decisions, not scheduling)
  C: system-architecture.md (architecture map, not execution status — File 1 Q9)
why: A keeps exactly one "what is next" owner (I2); the status table already carries the
  per-round pointer and is updated in-round by the planning agent; B/C conflate decision
  state with execution status (the D5 class).
consequences: every former roadmap pointer (DQE SKILL.md:9 class) re-points to the status
  table; the roadmap's per-batch statuses are frozen history in the archive.
revisit_condition: if the status table grows beyond one screen of next-actions, or a
  second plan family appears under docs/plans/active/, revisit the single-owner rule.
```

## 7. Minimum checker set (R11) and what defers

**In the slice (4 + the preflight/links pair):** `canonical-impact-lint` (with
change-scope input), `archive-lint`, `supersession-lint`, `decision-note-lint` — plus the
existing `preflight.py` + `markdown_links_check` (banner-aware extension).

**Deferred with their build phase (6):** `duplicate-fact-lint` (Phase 3 — needs the
split owner rows as input), `release-version-lint` (Phase 3), `dependency-graph-lint`
(with the registry graph fields), `state-consistency-lint` (Phase 3), `provenance-lint`
(Phase 3), `change-scope` as a standalone checker (ships as canonical-impact-lint's
input in the slice; standalone only if it earns its own invocation).

## 8. Explicit out of scope (ratchet discipline)

- apply-mode A1 (Phase 3 — owner updates are hand-applied under the existing
  write-approval boundary)
- A2/A3/A4/A6 parked capability gaps (R12 — parked blocks in File 4)
- multi-agent machinery beyond PSR + the audit's two subagent calls
- any corpus mutation (the slice is doc-side only)
- building the 6 deferred checkers (they are not in the slice's verification)
