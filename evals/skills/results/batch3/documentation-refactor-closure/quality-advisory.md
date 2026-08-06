<!--
generated_by_skill: documentation-quality-evaluator
skill_version: 0.4.1
source_commit: 07b5306
source_documents:
  - evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/README.md
  - evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/creation-roadmap.md
  - evals/skills/results/batch3/documentation-refactor-closure/rewrite-provenance-report.md
artifact_type: quality-advisory
document_lifecycle: IN_REVIEW
status: DEFERRED (advisory read of a candidate DRAFT set; authorizes nothing)
last_verified: 2026-08-06T00:00:00Z
-->

# Quality Advisory — documentation-refactor closure candidate set

**Advisory checkpoint, NOT a publish gate.** DQE v0.4.1 is frozen as an advisory / profile-scoped
evaluator. This report grades **read-only**; its verdict **authorizes nothing**. An ADVISORY/ALLOW here
never triggers a publish, move, or overwrite, and it does **not** authorize replacing the live
`docs/skill-development/` documents. Applying any candidate over the corpus is a separate
explicit-write-approval step, blocked until at least **D-1** and **D-4** are decided (see §5).

## Advisory verdict (task-prescribed line)

```
QUALITY_BAND=PASS · GATE_DECISION=ADVISORY_ONLY (not a publish gate) · HF-14b=PASS · HF-13=PASS (moving to single-responsibility) · FACT_DISCIPLINE=PASS · D-1_LEFT_OPEN=YES · CONFIDENCE=HIGH
```

## Structured verdict block (DQE-native, two-axis)

```
QUALITY_BAND=PASS                 # holistic quality of the drafted candidates on the disciplines assessed
GATE_DECISION=ADVISORY_ONLY       # v0.4.1 advisory freeze — authorizes nothing; NOT a terminal/publish gate
GATE_REASON=advisory-checkpoint   # not a terminal gate by construction; a candidate DRAFT at completion=PARTIAL
MERITS_READING=ALLOW-advisory     # under controlled+audit no applicable hard gate fires at BLOCKER severity; this ALLOW is advisory and is NOT a green terminal gate
DOCUMENT_QUALITY=PASS             # compat map (advisory)
FACTUAL_VALIDITY=PARTIALLY_VERIFIED   # both live sources opened + sha256 machine-verified unchanged; preserved lines not exhaustively diffed; S3-S9 deferrals taken on provenance+open-decisions corroboration
READER_TEST=NOT_RUN               # advisory scope — no two-layer no-context reader spawned; so no green terminal gate (consistent with ADVISORY_ONLY)
CHECKER_STATUS=COMPLETE           # run_checks.py run on all 3 files; JSON in §3
SOURCE_COVERAGE=2/2               # docs/skill-development/README.md + creation-roadmap.md both opened
CONFIDENCE=HIGH                   # deterministic-grounded on the S1/S2 executed scope; MEDIUM on S3-S9 deferral completeness
BLOCKERS=[]                       # none (controlled+audit: HF-14b cured; HF-13 not tripped; HF-9 satisfied)
FINDING_CODES=[staging-relative-links-unresolved, one-self-reported-count-preserved, pointer-target-pending-d1]
EVALUATION_PROFILE={artifact_type: rewrite-output over roadmap+architecture-index, provenance_policy: controlled, decision_mode: audit}
FILES_READ=[candidate-doc-set/README.md, candidate-doc-set/creation-roadmap.md, rewrite-provenance-report.md, batch2_5/document-chain/open-decisions.md, docs/skill-development/README.md, docs/skill-development/creation-roadmap.md, .claude/skills/documentation-quality-evaluator/SKILL.md, evals/skills/harness/hard-fail.md]
```

## 1. Evaluation profile (echoed)

- **artifact_type** — rewrite output (`HF-4`/`HF-9` guarded) drafting cured versions of a stable
  README index (architecture-index-like) and a **roadmap**; both are stable-design types, so HF-14b/HF-13
  apply. The third file is a `rewrite-provenance-report` (provenance record).
- **provenance_policy: controlled** (our own workspace docs). Not inferred — set for this advisory frame.
- **decision_mode: audit** (this is an advisory checkpoint, explicitly **not** release-gate). This is the
  load-bearing profile fact: under `controlled + audit`, HF-14b is **at most MAJOR**, never a lone BLOCK —
  and here the HF-14b condition is not even met (it was cured; see §2).

## 2. Discipline assessment (the gates that matter here)

**HF-14b (volatile-in-stable) = PASS — the cure was applied correctly.**
Both candidates **REMOVE** the volatile status/progress block from the stable doc and **replace it with a
pointer** — the right cure, not the wrong one (copying counts into a stable doc). Verified against the live
sources:
- README candidate — the live `## Phase-1 ✅ · DQE FROZEN · Batch 2 4/4 · Batch 2.5 DONE · Batch 3 skeletons`
  header (source L16), the scope-correction blockquote (L18-25), the collapsed `<details>` changelog (L27-43),
  and the front-matter `status:` progress line (L8) are all **gone**, replaced by a single pointer to *"the
  canonical status owner (PENDING decision D-1)."* No count is embedded as a current claim.
- roadmap candidate — the per-batch `**Status: …**` leads (source §0 L23, §2 L59-62, §2.5 L81-83, §3 L109) and
  the front-matter `status:` line are replaced by pointers; the plan/DoD/exit-criteria bodies are preserved.

There is **no bare undated "current" fact left embedded** in either stable doc, so the HF-14b trigger
condition is absent. (Even had it been present, `controlled + audit` caps it at MAJOR — never a lone BLOCK.)

**HF-13 (mixed responsibilities) = PASS / correct direction.** The rewrite **reduces** the original
role-mixing disease: each candidate is now single-responsibility (stable index; stable plan; provenance
record), with volatile status extracted out to a pointer. The `artifact_role_mixing` checker reported only
**mention-level** roles (`adr, status` on the README; `handover_session, open_questions, research_review,
status, validation` on the roadmap) — mention-level is explicitly **not** HF-13 body-level co-residence.

**Fact discipline (constraint D.8 / HF-3 / HF-7 / HF-10 / HF-12A-E) = PASS.**
- OPEN/HYPOTHESIS items kept **open**: OQ-1..OQ-5, G3, the real-task gap, and all 10 upstream decisions
  (D-1..D-7, IA-1..IA-3) carried verbatim; the provenance front-matter states `open_questions: carried,
  never 'none'`.
- **No fabricated facts, no re-numbered stale figures.** The stale per-skill version figures (`v0.2.0` at
  source L61, `v0.3.0` at L63) and the self-reported eval counts are **pointer-ized, not re-numbered to
  0.4.1**. Note the live README is internally contradictory here (L61 says "now at v0.2.0" while L63 says
  "v0.3.0"); the candidate **correctly did not propagate either figure** — a clean fact-discipline win.
- **D-1 left UNDECIDED (see §5).** The candidates invent **no** `STATUS.md` and pick **no** status owner —
  the deliberate contrast with a no-skill baseline that would.

**Provenance = strong and machine-corroborated.**
- Every candidate traces to a source line-range (§1 table in the provenance report); I opened both live
  sources and confirmed the cited removed ranges are genuinely volatile and the preserved index/plan is intact.
- `completion: PARTIAL` is **honest** — the 9-item `unresolved_content` ledger is non-empty and each item
  names its gating decision. The `rewrite_provenance` advisory checker **PASSES**, which means it recomputed
  the recorded source sha256 against the on-disk `docs/skill-development/` files and they **match** — a real
  tamper check proving the sources are unmodified, candidate paths ≠ source paths, and completion is not
  falsely COMPLETE. `may_overwrite / may_move / may_delete` all `false`.

**HF-9 (traceability front-matter) = PASS.** All three files carry complete traceability front-matter
(`frontmatter_check` PASS on each): `generated_by_skill`, `skill_version`, `source_commit`,
`source_documents`, `document_lifecycle`, `last_verified`.

## 3. Deterministic checker + signal results (run, not eyeballed)

`run_checks.py` over the three files — `hard_fail=false` everywhere:

| file | frontmatter (HF-9) | status_vocab (HF-3/10) | notable advisory / signal |
|---|---|---|---|
| candidate `README.md` | PASS | PASS | `markdown_links` FAIL — 12 relative links unresolved **in staging** (see finding A) |
| candidate `creation-roadmap.md` | PASS | PASS | `completion_open` SIGNAL at §8 (see finding B); `role_mixing` mention-level only |
| `rewrite-provenance-report.md` | PASS | PASS | `rewrite_provenance` PASS (hash-verified, honest PARTIAL); all advisory clear |

**Adjudicated signals (a checker emits a raw candidate; the evaluator maps it):**
- **Finding A — README relative links (advisory, MINOR / staging artifact, NOT a content defect).** The 12
  broken links (`current-skills-audit.md`, `system-architecture.md`, `reports/…`, `../../references/…`, etc.)
  resolve relative to the candidate's isolated staging directory, where the sibling docs do not exist. They
  are **correct relative to the source home** (`docs/skill-development/README.md`) and will resolve if/when
  the candidate is applied there. This is expected for an out-of-home DRAFT — but it makes **link-integrity
  verification in-situ a required apply-step check** (see §5).
- **Finding B — roadmap §8 `completion_open` SIGNAL = NOISE (not HF-14b/HF-15).** The checker flagged
  "done" + "open" co-occurring in `## 8. Milestone acceptance`. The "done" is the definition-of-done phrasing
  *"Batch 1 is 'done' when:"* and the "open" is inside an acceptance criterion (*"a reader can extract …
  open-questions"*). This is a DoD/acceptance section, not a completion-vs-open contradiction. Cleared.
- **role_mixing SIGNALs** — all mention-level (adjudicated under HF-13 above): not a defect.

## 4. What is good (summary)

The candidate set demonstrates the intended `volatile-state → pointer` cure with discipline: volatile status
removed (not copied) from stable docs; stale/contradictory figures pointer-ized (not re-invented); all OPEN
items and all 10 upstream decisions carried; D-1 and D-4 left undecided; honest `completion: PARTIAL` backed
by a non-empty unresolved-content ledger; complete traceability front-matter; and machine-verified read-only
provenance (sources byte-unchanged). On every discipline the task named, the candidates hold.

## 5. What a human must still resolve before ANY apply

This is a candidate DRAFT at **completion=PARTIAL** (only migration splits **S1**/**S2** were executed of ~9).
Do **not** treat this advisory as clearance to apply. Load-bearing open items:

- **D-1 (canonical status owner) — UNDECIDED by design, and must stay so until a human picks it.** Both
  candidates leave every status pointer as *"the canonical status owner (PENDING decision D-1)"*. The cure is
  structurally correct but **cannot be fully wired** until the owner is chosen (README §0, README "Next",
  roadmap §0/§1/§2/§2.5/§3 all depend on it). The candidates correctly do **not** invent a `STATUS.md` or an
  owner — confirm that choice is a human decision (IA recommendation in `open-decisions.md`: make the standing
  PSR state report the owner; not decided here).
- **D-4 (README index scope) — UNDECIDED.** The report cross-references removed from README's "Next" narrative
  and the roadmap status leads are **not** wired into any index; whether the ~15 `reports/`+`adr/` files are
  "orphans to index" or a deliberate append area is D-4, left open.
- **DEFERRED dispositions S3–S9 (not drafted in this set):** S3 (`skills-registry.yaml meta:`) and S4/S5
  blocked_by **D-6** (drift diff vs `hard-fail.md` / defect-ledger); S6 (v0.2 quality report deprecation)
  blocked_by **D-2**; S7 (`ADR-DQE-001` superseded-in-part note) blocked_by **D-3**; S9a-c (split the MIXED
  frozen dated reports) blocked_by **IA-1**. Each requires deciding its gated decision first.
- **Finding-A link integrity** must be verified in the target home at apply time.
- **One consistency item for confirmation (MINOR, not a blocker):** the roadmap candidate preserves the
  gate-rule blockquote's self-reported *"trigger 28/28 + discriminative e2e"* (source L16) while pointer-izing
  the other self-reported counts (e.g. §2 "32/32"). This is defensible as a **historical foundational
  gate-pass** (the basic-eval unlock of Batch 2), not live progress — but a human should confirm it should
  stay verbatim rather than also be softened, for consistency with the STALE/HYPOTHESIS treatment applied
  elsewhere.

## 6. Disposition

`GATE_DECISION=ADVISORY_ONLY`. On the merits, under the `controlled + audit` profile no applicable hard gate
fires at BLOCKER severity, so the native reading is an **advisory ALLOW** — but per the v0.4.1 freeze that
ALLOW **authorizes nothing**: it is not a green terminal gate (independently barred here by
`READER_TEST=NOT_RUN` and `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`), and it does **not** permit replacing the
live `docs/skill-development/` docs. This advisory is one input for a human/independent reviewer alongside the
still-open decisions above; the apply step remains an explicit, separately-authorized write, blocked on at
least D-1 and D-4.
