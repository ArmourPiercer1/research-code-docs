# Phase-2 Vertical Slice — Execution Record (A8 audit + A9 verification + before/after)

<!--
generated_by_skill: Phase-2 slice execution (parent agent, manual)
skill_version: n/a
source_commit: 1dc6b86 (slice start); 8a37387 (commit A); commit B = this record's commit
source_documents: [docs/plans/active/research_code_docs_phase2_implementation_prompt.md, docs/plans/active/reconstruction/revised-phase2-vertical-slice.md]
status: VERIFIED
last_verified: 2026-09-10
date: 2026-09-10
slice_start: 1dc6b8694dac60ac355b8094e61ffebde322fba0
commit_A: 8a37387 (mechanism: 4 lints + register_check merge + A8/A9 + eval datasets + registry)
commit_B: this record's commit (slice: archive + pointers + stores + tracking + records)
note: A9 verdict VERIFIED; the slice itself awaits external review after commit B
-->

## 1. Scope

ONE candidate (the VOID `creation-roadmap.md`), the Phase-2 canonical stores, the
tracking transition, and the minimum checker set. Out of scope per slice §8: A1
apply-mode, A2/A3/A4/A6, multi-agent beyond PSR + 2 subagent calls (the two-axis
review = 2 subagents), corpus mutation beyond archive + pointers + stores, and the 6
deferred checkers (incl. dependency-graph-lint).

## 2. Stage 0 — pre-change state (A8 input, deterministic census)

- **VOID candidate census:** exactly 1 VOID/SUPERSEDED document outside
  `docs/plans/archived/` at slice start: `docs/skill-development/creation-roadmap.md`
  (banner L3: `> **VOID / superseded** (2026-09-09)`). The `docs/reconstruction-external-review/`
  mirror is archive_lint-exempt by rule (frozen external-review mirror).
- **Inbound references to the roadmap — COMPLETE re-census** (prompt §Stage-0: "re-census
  ALL references repo-wide; do not trust the old Phase-2 example that says there is exactly
  one inbound reference". Method: `git grep -c "creation-roadmap"` over the tracked tree +
  untracked `docs/plans/finished/` scan; run 2026-09-10; ~90 file-level matches in ~70 files.
  Classification per prompt §7.2; **only 7 live pointers needed re-pointing (5 files)** —
  the rest are frozen results/fixtures or historical provenance and were KEPT:

  | Reference | Class | Disposition |
  |---|---|---|
  | `.agents/skills/content-canonicalization-and-migration/SKILL.md:15` | POINTER (source_documents locator) | re-pointed to `docs/plans/archived/creation-roadmap.md` + VOID label |
  | `.agents/skills/workspace-forensics-and-inventory/SKILL.md:16` | POINTER (source_documents locator) | re-pointed + VOID label |
  | `docs/skill-development/README.md:3` | POINTER (banner link) | re-pointed to archived path |
  | `docs/skill-development/README.md:62` | POINTER (index row link) | re-pointed + "archived 2026-09-10 (VOID)" label |
  | `docs/skill-development/README.md:120` | POINTER (D5-section link, inside SUPERSEDED-2026-08-06 block) | re-pointed + "frozen history" label |
  | `docs/skill-development/conflict-matrix.md:31` | POINTER (§3 gate footnote) | re-pointed + VOID label |
  | `evals/skills/README.md:7` | POINTER (source_documents locator) | re-pointed + VOID label |
  | `.agents/skills/documentation-quality-evaluator/SKILL.md:9` (historical) | — | confirmed GONE at slice start (already re-pointed in an earlier round) |
  | `references/interfaces/migration-map.schema.md:42` | FROZEN-CONTRACT-EXAMPLE (sample path in the batch2.5-v1 schema: "a real path (existence checked)") | KEEP — D10 freeze: interfaces are additive-only, never edited; the example is version-frozen; a future schema version may re-point it |
  | `references/interfaces/rewrite-provenance-report.schema.md:41` | FROZEN-CONTRACT-EXAMPLE (abbreviated `docs/.../` sample) | KEEP — same D10 freeze |
  | `docs/prompt.md:102` | PLAIN-TEXT-HISTORY (prose inventory list, no link) | KEEP (not a pointer) |
  | `CHANGELOG.md:24` | PLAIN-TEXT-HISTORY (append-only release history) | KEEP (append-only; entries never rewritten) |
  | `docs/skill-development/reports/runlog.md:32-56` (6 lines) | PLAIN-TEXT-HISTORY (dated run chronology) | KEEP + one transition-thin Phase-2 line appended |
  | `docs/skill-development/reports/{batch1-eval-run,batch2_5-integration,batch3-skeletons,dqe-v0.4.1-freeze}-*.md` | HISTORICAL-PROVENANCE (dated run reports, 5 mentions) | KEEP (frozen run records) |
  | `docs/plans/active/reconstruction/phase0/**` (28 mentions in 4 files) | HISTORICAL-PROVENANCE (frozen-on-acceptance Phase-0 deliverables: ownership map, system map, classification, pain-point evidence) | KEEP (frozen plan documents cite pre-change file:line as audit evidence) |
  | `docs/plans/active/reconstruction/phase1/**` (19 mentions in 5 files) | HISTORICAL-PROVENANCE (frozen-on-acceptance Phase-1 deliverables) | KEEP (same) |
  | `docs/plans/active/reconstruction/{execution-notes,post-audit-reconciliation,architecture-review-disposition,revised-phase2-vertical-slice}.md` (9) | HISTORICAL-PROVENANCE (frozen-on-acceptance planning docs) | KEEP (same) |
  | `docs/reconstruction-external-review/**` (33 mentions in 10 files, incl. the mirrored roadmap doc itself) | FROZEN-RESULT (byte-frozen external-review mirror) | KEEP (sha256-verified untouched, §4.2) |
  | `evals/skills/results/**` (43 mentions in 12 files, incl. batch3 `candidate-doc-set/creation-roadmap.md` = the frozen candidate copy) | FROZEN-RESULT (dated run results + DQE prompt fixture `evals/skills/results/prompts/documentation-quality-evaluator.txt`) | KEEP (byte-frozen, §4.2) |
  | `tests/corpus/blind-runs/**` (30 files, 1 each) | FROZEN-RESULT (frozen eval corpus, inputs cite pre-change paths as historical evidence) | KEEP (digest-verified, §4.2) |
  | `docs/plans/archived/Research-Code-Docs当前进展_阻塞项与下一阶段开发计划.md:554` | HISTORICAL-PROVENANCE (frozen archive body) | KEEP |
  | NEW in this change: `phase2/*`, `reconstruction/README.md`, `decision-register.md`, D-1 note, `canonical-source-map.md`, root `README.md`, `trigger/simplification-audit.yaml`, `simplification-audit/SKILL.md`, `archive_lint.py` docstring, the implementation prompt itself | NEW-DATA / TEST-DATA (intentional references to the archived path) | created by this change |
  | untracked `docs/plans/finished/research_code_docs_phase1_final_consistency_patch.md:509` | HISTORICAL-PROVENANCE (Phase-1 repair guide, untracked by intent) | KEEP (tracking decision = Phase 3) |

- **Pre-state facts:** `docs/plans/archived/` held 8 tracked plans; `docs/plans/active/**`
  and `archived/**` were UNTRACKED (git-ignored until consistency patch P2; tracking
  transition = this slice); stores `docs/decision-notes/`, `docs/decision-register.md`,
  `docs/canonical-source-map.md` did not exist; `evals/skills/harness/canonical-source-map.md`
  held the full 10-row generic map (17-row owner table lived in the Phase-1 File 3).

## 3. A8 — simplification audit report (pre-change)

- **Candidate:** `creation-roadmap.md` — VOID (2026-09-09), superseded by the
  reconstruction charter; every batch it planned is done or superseded. Archiving is the
  single smallest change that turns the planted lint red (R1) green without touching any
  live authority.
- **Minimal change set:** (1) `git mv` to `docs/plans/archived/` (relocation only — banner
  intact, zero content edit); (2) 7 reference fixes across 5 files (the only live pointers;
  §2 census); (3) same-change owner updates per File-3 table (system-architecture D12 status
  line; reconstruction README status table = the D-1 "what is next" owner; root README
  counts/governance); (4) stores per prompt §6; (5) tracking transition of
  `docs/plans/active/**` + `archived/**` only; (6) one §7.3 stale-claim correction
  (SWR SKILL.md D14: LDM builtness).
- **Change contract:** `phase2/impact-declaration.yaml` (changed_paths + canonical_owners
  with no_impact justifications + intentionally_untracked carve-out).

## 4. A9 — focused verification (post-change, minimum checker set)

### 4.1 Contract conformance (each check mapped to its contract clause)

| Check | Verdict | Evidence |
|---|---|---|
| `archive_lint.py --repo` | **PASS** (post-move); pre-move = **R1 RED on `docs/skill-development/creation-roadmap.md` (L3)** — the planted defect, DETECTED and NAMED before the move (baseline worktree run at 8a37387) | §4.2 |
| `supersession_lint.py --repo` (persisted `--repo` mode; 9067 .md files) | 1 failing file = **pre-existing upstream** `references/academic-research-skills/docs/design/2026-05-18-ars-v3.9.4-temporal-verification-spec.md` (S2: `supersedes: handbook-2020ed`, L166) — identical to the slice-start baseline; all new store files pass | §4.2 |
| `decision_note_lint.py docs/decision-notes` | **PASS** (D-1 note in `decided/` with all 7 sections, 6 legal fields, folder↔state match) | §4.2 |
| `canonical_impact_lint.py --impact phase2/impact-declaration.yaml --base 1dc6b86 --worktree` | **PASS** (slice-level contract: base = slice start; C1 changed⊆declared incl. all 13 commit-A paths; C2 owners updated; C3 no_impact justifications; C4 no timestamp-only discharge). Supplementary run at base 8a37387 also **PASS** (commit-A-subset view) | §4.2 |
| `selftest_phase2_lints.py` | **28/28 PASS** (Commit-A cases + slice `ruling:`-alias case + 3 new banner-aware link cases; planted stale-roadmap defect-1 fixture asserts detection before scoring) | §4.2 |
| `markdown_links_check.py` (banner-aware extension, prompt §9 L406 / §5.2-4) over all touched live docs + live governance sweep | **PASS** — the new rule (live doc → archived/VOID target must be labeled historical/frozen/archived on its line; frozen sources exempt) caught one real unlabeled pointer in the root README during this pass (fixed in-change); 3 selftest cases incl. negative control | §4.2 |
| **affected existing eval cases** (prompt §9) | corpus cases whose INPUTS cite the old path (`tests/corpus/blind-runs/**` GN-ROADMAP-001 etc., 30 files) are frozen fixtures — bytes unchanged (digest, §4.2), their pre-change path citations are historical evidence, no re-scoring; the 4 A8/A9 routing/conflict yamls are NEW (untracked before, authored this slice) and parse-checked (8/8/4 trigger + 5 conflict each) | §4.2 |
| `scripts/preflight.py` | **PASS** (14 declared / 14 present, 0 issues; A8/A9 deliberately not in the frozen 0.1.0-alpha.1 manifest — recorded in registry `meta.phase2` + entry notes) | §4.2 |
| scoped `run_checks.py` over `docs` + `.agents/skills` (16 files) + `evals/skills/harness` (3) + `references/interfaces` (12), diffed against a baseline worktree at 8a37387 | **0 NEW HARD failures from this change.** Delta: +34 HARD-FAIL files, ALL in `docs/plans/**` (32 tracked + 2 untracked `finished/`) — files absent from the 8a37387 baseline checkout whose pre-existing front-matter/status-format defects are newly exposed by tracking, byte-unchanged except `reconstruction/README.md` (same pre-existing failure mode, extended status value). −1 HARD-FAIL: the roadmap's R1 (the planted control) — now advisory-only (its internal relative links, pre-existing, advisory). `.agents/skills` 0→0, `evals/skills/harness` 1→1 (the `hard-fail.md` name-match artifact on BOTH sides; zero real new), `references/interfaces` 0→0. | §4.2 |
| untouched-scope integrity (frozen set) | **byte-identical to 8a37387** — `git diff --name-status 8a37387` + `--cached` + untracked all EMPTY for: `docs/reconstruction-external-review/`, `evals/skills/results/`, `references/interfaces/`, `references/templates/`, `tests/corpus/`; tree-list sha256 digests recorded in §4.2 | §4.2 |
| planted defect detected + named + cleared | **YES** — baseline (8a37387 worktree) `archive_lint` output: `archive-lint R1: VOID/SUPERSEDED doc docs/skill-development/creation-roadmap.md lives outside docs/plans/archived/ (L3)`; cleared by the `git mv`; R3 (archived ⇒ tracked) satisfied by the tracking transition | §4.2 |

**A9 verdict: VERIFIED** — every contract clause in the minimum checker set (slice §7:
the 4 lints + preflight + scoped run_checks) passes or matches the recorded pre-existing
baseline; no deferred checker was used; no new HARD failure introduced.

### 4.2 Raw evidence (commands + results, run 2026-09-10)

```text
# baseline worktree at 8a37387 (git worktree add .baseline-8a37387 8a37387)
> .venv\Scripts\python.exe evals\skills\harness\checkers\archive_lint.py --repo
  [HARD-FAIL] docs/skill-development/creation-roadmap.md
    - archive-lint R1: VOID/SUPERSEDED doc ... lives outside docs/plans/archived/ (L3)   ← planted defect
# post-move
> .venv\Scripts\python.exe evals\skills\harness\checkers\archive_lint.py --repo
  archive_lint --repo D:\AI_Coworking\skill-build\research-code-docs: PASS
> .venv\Scripts\python.exe evals\skills\harness\checkers\decision_note_lint.py docs\decision-notes
  [PASS] docs\decision-notes
> .venv\Scripts\python.exe evals\skills\harness\checkers\supersession_lint.py --repo
  supersession_lint --repo D:\AI_Coworking\skill-build\research-code-docs: scanning 9067 .md files
  [FAIL] references\academic-research-skills\docs\design\2026-05-18-ars-v3.9.4-temporal-verification-spec.md
    - supersession-lint S2: supersedes ID 'handbook-2020ed' (L166) is not defined ...   ← pre-existing upstream, slice-start baseline
  supersession_lint --repo: FAIL (exactly 1 file — the pre-existing upstream hit; no new failures)
> .venv\Scripts\python.exe evals\skills\harness\checkers\canonical_impact_lint.py --impact docs\plans\active\reconstruction\phase2\impact-declaration.yaml --base 1dc6b8694dac60ac355b8094e61ffebde322fba0 --worktree
  canonical_impact_lint (base=1dc6b8694dac60ac355b8094e61ffebde322fba0, worktree=True): PASS
> .venv\Scripts\python.exe evals\skills\harness\checkers\canonical_impact_lint.py --impact docs\plans\active\reconstruction\phase2\impact-declaration.yaml --base 8a37387 --worktree
  canonical_impact_lint (base=8a37387, worktree=True): PASS      (supplementary, commit-A-subset view)
> .venv\Scripts\python.exe evals\skills\harness\checkers\selftest_phase2_lints.py
  ==> selftest_phase2_lints: 28 pass, 0 fail
> .venv\Scripts\python.exe evals\skills\harness\checkers\markdown_links_check.py <all touched live docs + live governance sweep>
  all PASS (one real unlabeled live→archived pointer in root README caught + fixed in this pass;
  pre-existing broken link in intermediate/dsh-current-state-findings.md — DRAFT Phase-1 evidence,
  advisory only, recorded §8)
> .venv\Scripts\python.exe scripts\preflight.py
  status: PASS   (skills: declared 14 / present 14 / manual_only 14, issues [])
# scoped run_checks diff (baseline worktree vs current, all 4 scopes: docs, .agents/skills, evals/skills/harness, references/interfaces)
  BASELINE HARD-FAIL lines: 37 (docs 36 real + 1 harness name-match artifact)   CURRENT: 70 (docs 69 real + 1)
  NEW: 34 files, all docs/plans/** (32 tracked + 2 untracked finished/; absent from the 8a37387 baseline checkout → newly exposed, pre-existing format)
  GONE: docs/skill-development/creation-roadmap.md (moved; R1 control cleared; now advisory-only)
  .agents/skills (16 files) / evals/skills/harness (3) / references/interfaces (12): zero new HARD failures
# frozen-set integrity (git tree 8a37387 vs index vs worktree — all diffs empty)
  docs/reconstruction-external-review  tree-list sha256 = 1840137252912214081112145219312148458225237155171391572061395317316120569441769055
  evals/skills/results                 tree-list sha256 = 151822459011277102721712023324313218455208184658099371121551661117624920424113822677
  references/interfaces                tree-list sha256 = 53103771491171532110795321452177253721748191224140191244176696345192131138196167225
  references/templates                 tree-list sha256 = 2511823278531621212411217118029115273319828241762121701432091222361602316137252111
  tests/corpus                         tree-list sha256 = 252145966984396419122587491841061567281541887614227375254157203822210917923632
# archive data-loss check (100% rename, blob-identical to slice start)
  git diff --cached --find-renames --summary 1dc6b86 -- <old> <new>
    rename docs/{skill-development => plans/archived}/creation-roadmap.md (100%)
  blob(1dc6b86: old path) == blob(index: new path) == 94a16dfbd111ab29117fa361391584298a47f157
```

**Mechanism-side deltas discovered during verification (fixed, declared in the impact
contract):** (a) `canonical_impact_lint` worktree mode — utf-8 git IO (GBK console
decode error on CJK paths), C-style path unquoting (core.quotepath), new-file C4
(synthesized content diff), directory-owner prefix matching, `intentionally_untracked`
carve-out; (b) `decision_note_lint` — `ruling` accepted as an alias of the `decision`
section (the slice §6 note shape); (c) `run_checks.py` CLI — multi-path invocations
silently processed only the first argument (pre-existing); now iterates all paths so a
multi-scope gate cannot under-scan. All are in-mechanism development fixes, not
incidents (row 12 ledger untouched).

## 5. Before / after (slice §5 evidence table)

| Metric | Before (1dc6b86) | After (this change) |
|---|---|---|
| roadmap location | `docs/skill-development/creation-roadmap.md` (VOID banner L3, active dir) | `docs/plans/archived/creation-roadmap.md` (banner intact, `git mv` only) |
| inbound references | 7 live pointers across 5 files (full classified census: §2 — frozen/historical mentions kept) | 0 broken / all re-pointed + labeled (7 fixed; 1 historical already gone; all frozen + plain-text refs classified and kept) |
| planted defect (archive_lint R1) | RED (VOID doc outside archived/) — detected + named at baseline | GREEN (doc inside archived/, banner intact, tracked) |
| `canonical_impact_lint` | n/a (added in commit A) | **PASS** against `phase2/impact-declaration.yaml`, base **1dc6b86** (slice-level, incl. commit-A paths), worktree; supplementary base-8a37387 run also PASS |
| `archive_lint` / `supersession_lint` | R1 red (control) + 1 pre-existing upstream S2 | R1 green; S2 = the same single pre-existing upstream hit (9067 files, `--repo` mode) |
| `markdown_links_check` (banner-aware) | pre-existing link check (no archived-pointer rule) | rule added (prompt §9/§5.2-4); all live docs PASS; 3 selftest cases incl. negative control |
| `decision_note_lint` | n/a (added in commit A) | **PASS** (D-1 note clean) |
| sha256 (frozen mirrors/results/fixtures) | digests recorded (8a37387) | **unchanged** — identical digests, empty diffs (5 frozen dirs, §4.2) |
| two-axis review | — | both axes executed via parallel subagents, results in §6 |
| persistent_artifact_count | — | **REPORT ONLY** (R10.4 predicates) — see §7 |

## 6. Two-axis review (fixed point 1dc6b86; diff = staged index vs slice start, covering commit A + commit B)

Method: `code-review` skill, two parallel subagents (standards axis + spec axis), fixed point
`1dc6b86`, diff = staged index vs slice start. Reports received in full 2026-09-10; every finding
adjudicated against the prompt text (L56-450 re-read for the exact clauses). Disposition:

### 6.1 Standards axis — findings and disposition

| # | Finding | Disposition | Evidence |
|---|---|---|---|
| S1 | execution-record front-matter `status: COMPLETE` — not in the §7 vocabulary | **FIXED before review (stale finding)** — reviewer saw the pre-fix snapshot; now `status: VERIFIED` + all 6 front-matter keys present; front-matter checker `[OK]` | record front-matter L8-9; `frontmatter_check` PASS in scoped run |
| S2 | execution-record front-matter missing keys | **FIXED before review (stale finding)** — same as S1 | record front-matter L3-14 |
| S3 | `register_check` H2 merged into the HARD tier = scope creep (prompt §5 names only the four lints) | **JUSTIFIED (judgement call, recorded)** — the prompt is silent on register_check tiering; the slice's register seed (D-1/R-001) needed a HARD state check to be load-bearing; kept in commit A (already pushed); §10.4 "no deferred Phase-3 checker required" unaffected — register_check is a Phase-1-existing checker, not a deferred one | impact-decl §commit-A comment; prompt §5 L201-223 (four lints enumerated, register_check not mentioned) |
| S4 | selftest asserts against LIVE `docs/decision-register.md` (repo-state dependence in a deterministic selftest) | **FIXED** — assertions moved to the two frozen-corpus registers (byte-frozen set, sha256-verified) with skip-if-absent guard | `selftest_phase2_lints.py` `t_register_scoped`; 28/28 |
| S5 | record §4.1 lacked the "affected existing eval cases" evidence row (prompt §9) | **FIXED** — row added (frozen corpus cases unchanged; 4 new A8/A9 datasets parse-checked) | §4.1 |
| S6 | registry A9 `class: verify` not in the §10 enum (`audit\|design\|migration\|rewrite\|maintain\|evaluate\|research-adapter\|utility`) | **FIXED** — `class: evaluate` | `skills-registry.yaml` A9 entry; `system-architecture.md:281` |
| S7 | A8/A9 `norm_sources: [revised-phase2-vertical-slice]` = a doc name, not a fact-type name | **FIXED** — `norm_sources: []` (both skills read plan/contract documents, not canonical fact stores — same pattern as DQE) | `skills-registry.yaml` A8/A9 entries |
| S8 | dead conditional in `canonical_impact_lint._unquote_git_path` (`ord(c) if ord(c) < 128 else ord(c)`) | **FIXED** — plain `out.append(ord(c))` | `canonical_impact_lint.py` |
| S9 | typo "bannned" (`archive_lint.py:9`) | **FIXED** | `archive_lint.py:9` |
| S10 | S4 docstring promised "banner OR explicit supersession marker" but the code checks banners only | **FIXED** — docstring now banner-only (marker support = deferred, not claimed) | `supersession_lint.py:12` |
| S11 | `shutil.rmtree(fx)` at selftest:304 could trip the sandbox-denied git-objects case elsewhere in the file | **FIXED** — `_rmtree` (onexc chmod) | `selftest_phase2_lints.py` `t_register_scoped` |
| S12 | supersession whole-repo scan used an ad-hoc `_supersession_scan.py` driver (deleted; not verbatim-rerunnable) | **FIXED** — `supersession_lint.py --repo` mode (persisted); record §4.2 command updated | `supersession_lint.py` `main()`; §4.2 |
| S13 | minor: `canonical_impact_lint` CLI `IndexError` when a valued flag is last | **FIXED** — bounds check → exit 2 | `canonical_impact_lint.py` `main()` |
| S14 | 10 judgement-call smells (runlog transition line, frozen CHANGELOG mention, frozen planning-doc stale counts, etc.) | **JUSTIFIED / recorded** — each mapped to a §8 entry | §8 |

Stale-finding correction recorded for the reviewer of this record: the raw HARD counts in the
standards report each include one false-positive line (a `hard-fail.md` filename matching the
case-insensitive 'HARD-FAIL' string). Authoritative re-measurement after the fix batch: baseline
36 real (docs scope) / current 69 real (docs scope); the entire delta = +34 newly-exposed
`docs/plans/**` files − 1 cleared roadmap R1 control; zero real new in the other three scopes.

### 6.2 Spec axis — findings and disposition

| # | Finding | Disposition | Evidence |
|---|---|---|---|
| P1 | Stage-0 re-census incomplete (missed `evals/skills/README.md:7`, `references/interfaces/{migration-map,rewrite-provenance-report}.schema.md`, `CHANGELOG.md:24`) | **FIXED** — complete repo-wide census with five-way classification (7 live pointers; all frozen/historical refs classified and kept) | §2 |
| P2 | banner-aware markdown-link extension missing (prompt §9 L406 "markdown link check / required banner-aware extension" + §5.2 rule 4) | **FIXED** — rule implemented in `markdown_links_check.py` (live doc → archived/VOID target must be labeled on its line; frozen sources exempt) + 3 selftest cases incl. negative control; caught 1 real unlabeled pointer (root README) in this pass | §4.1-4.2; `markdown_links_check.py` |
| P3 | impact declaration scoped to commit A only (base 8a37387; the 13 commit-A paths undeclared at slice level) | **FIXED** — `base: 1dc6b86`, all 13 commit-A paths + review-response paths declared; `canonical_impact_lint --base 1dc6b86 --worktree` = **PASS** (spec subagent had verified the old declaration FAILed C1 on the 9 commit-A paths) | `impact-declaration.yaml` header; §4.2 |
| P4 | supersession driver not persisted (same as S12) | **FIXED** — `--repo` mode | §4.2 |
| P5 | SWR D14 stale builtness claim (prompt §7.3 names it: "SWR stale builtness claim (D14 class)"; "only edit an item if current evidence still shows it is stale") | **FIXED** — evidence re-verified current (LDM SKILL.md:9 v0.1.0 experimental; Sprint 6B built it 2026-08-06); line 49 `[BLOCKED: not built]` → `[built v0.1.0, manual-only; not yet wired into this chain (D14)]`; the other 4 lines remain not-built (verified absent) | `scientific-workspace-reconstruction/SKILL.md:44-49` |
| P6 | hard-coded "5 inbound references" contradicts the census (prompt: "do not trust the old Phase-2 example…") | **FIXED** — authoritative count = **7 live pointers / 5 files**; all three docs now consistent (this record §2/§5, D-1 note, reconstruction README, impact declaration) | §2, §5; `d-1-*.md` implementation paragraph; `reconstruction/README.md` status row |
| P7 | R-001 `implementation_state: in_progress` vs slice §4.5 seed rule (`none`) | **FIXED** — `none` + clarifying note (per-phase progress lives in the status table, not the seed) | `decision-register.md` R-001 entry + change log |
| P8 | no runlog line for the real A8/A9 use (QCP §7) | **FIXED** — one transition-thin line appended (map row 13 allows the thin-pointer form during transition; full detail in this record) | `runlog.md` last line; map row 13 |
| P9 | record §6 empty (TBD) | **FIXED** — this section | §6 |
| P10 | scope creep: register_check H2 tier merge (same as S3) | **JUSTIFIED (judgement call)** — see S3 | S3 |
| P11 | 9 SATISFIED items (four lints + selftests, D-1 note/no generic status, register seed scope, single manual map + pointer harness copy, tracking transition, frozen-set integrity, planted-defect negative control, no deferred-checker dependence, artifact count report-only) | confirmed by both axes + the §4 battery | §4.1-4.2, §7 |

### 6.3 Completion gate (prompt §15) — checklist

All boxes TRUE: slice-start recaptured (1dc6b86, §2); all creation-roadmap references classified
(§2 complete census); A8/A9 implemented without dependency-graph-lint (registry entries:
search-based classification / contract-conformance only); all four lints implemented + negative
controls pass (selftest 28/28, §4.2); D-1 in `decided/` recording option A; no generic mixed
status in the new decision schema (six orthogonal fields; entry `status:`/`evidence:` claim pair
is the register_check-required state pair, documented in the register intro — §2.3's target is the
mixed DECISION state, which is carried by `decision_state` alone); register seeded only as scoped
(D-1 + R-001); canonical-source-map = one manual authority (harness copy = pointer);
`docs/plans/active/**` + `archived/**` tracked; `local/`+`scratch/` excluded; roadmap archived
without historical-data loss (100% rename, blob-identical); live pointers/current-state claims
corrected from evidence (§7.3: D12 + D14 + counts); planted stale-roadmap defect detected + named
in an isolated fixture (defect-1 case); focused-verification record complete (§4); two-axis review
with no unresolved spec blocker (this section — every finding fixed or justified); untouched-scope
integrity PASS (5 frozen dirs, digests §4.2); no deferred Phase-3 checker required; artifact count
report-only with per-artifact lifecycle/consumer (§7).

**Unresolved: none.** Items deliberately deferred (not blockers, all recorded): Phase-3 front-matter
retrofit of the 34 newly-exposed `docs/plans/**` items, `docs/plans/finished/` tracking, A8/A9
packaging into the next manifest, the 6 deferred lints, ADR-DQE-001 note migration, D19 snapshot/
corpus tracking, the 2 frozen interface-schema example paths (D10 version freeze).

## 7. persistent_artifact_count — REPORT ONLY (R10.4 + final patch P5)

Artifacts added by this change (not a gate; each carries unique_responsibility /
canonical_owner / consumer / lifecycle / archive_or_delete_condition):

| Artifact | Unique responsibility | Consumer | Lifecycle / archive condition |
|---|---|---|---|
| `docs/decision-notes/decided/d-1-what-is-next-canonical-owner.md` | durable rationale for D-1 (what-is-next ownership) | register row D-1 (proof_context); future revisits | moves to `decision-notes/archived/` when D-1 is superseded |
| `docs/decision-register.md` | single register of decided/open decisions (row 7) | D-1 owner table; A9; future lints | append-only rows; seed = D-1 + R-001 only (no backfill) |
| `docs/canonical-source-map.md` (§A owner table + §B generic rows) | the single manual canonical source map (row 5.1) | A8/A9, lints, humans | updated in the same change as any owner change (C2) |
| `evals/skills/harness/canonical-source-map.md` (thin pointer) | harness-side locator | checkers/probes that read the harness path | stays a pointer until the map moves again |
| `docs/plans/active/reconstruction/phase2/` (this record + impact-declaration) | slice evidence + change contract | external review; A9 | follows the plans/ lifecycle (archived with the phase) |
| `docs/decision-notes/{proposed,rejected,archived}/.gitkeep` ×3 | keeps the 4 lifecycle folders | decision_note_lint scope | delete a .gitkeep only when the folder is deleted |

R10.4 predicate check: **none of the fail predicates holds** — no two artifacts carry
the same canonical fact (owner vs rationale vs map vs contract are disjoint roles);
every artifact has a named consumer, a lifecycle, and an archive/delete condition; none
exists only for process ceremony; growth is tied to the Phase-2 capability gain (stores +
lints), not monotone decoration.

## 8. Intentionally untracked + pre-existing baseline reds + judgement calls (recorded, not fixed — outside the minimal set)

- `docs/plans/finished/` (2 guide docs) — OUT of the Phase-2 tracking spec (active/** +
  archived/** only); left untracked on purpose; tracking decision deferred to Phase 3.
  Declared in `impact-declaration.yaml → intentionally_untracked`.
- Pre-existing whole-repo HARD reds (never green; gates = scoped runs + preflight):
  front-matter/status-vocab failures in `references/**` (upstream mirrors),
  `tests/corpus/**`, `THIRD_PARTY_LICENSES.md`, `UNINSTALL.md`,
  `tests\最终目标设计与开发路线图.md`, 3 DQE result files.
- **34 newly-exposed `docs/plans/**` front-matter items** (32 tracked + 2 untracked `finished/`;
  byte-unchanged except the tracked `reconstruction/README.md`'s extended status value, same
  pre-existing failure mode) — JUSTIFIED as Phase-3 retrofit follow-up: the slice's tracking spec
  (active/** + archived/**) is what exposes them; rewriting Phase-0/1 frozen deliverable
  front-matter belongs to a Phase-3 docs-hygiene pass (same class as the D19 tracking targets).
  Same failure mode as the pre-existing docs-adjacent reds; zero new failure kinds.
- Pre-existing supersession S2: `references/academic-research-skills/.../2026-05-18-ars-v3.9.4-temporal-verification-spec.md`
  (`supersedes: handbook-2020ed`, L166) — upstream file, untouched.
- Advisory note: `rewrite_provenance_check` was red pre-change on the batch3
  candidate-doc-set ("source hash changed" — the VOID banner was added after the batch3
  snapshot); post-move it reads "source not found". Same advisory severity, frozen
  fixture — no action in this slice.
- Pre-existing broken link: `intermediate/dsh-current-state-findings.md` → `../AGENTS.md#conventions`
  (a Phase-1 DRAFT intermediate; the path is conceptual, pointing at the DSH checkout's AGENTS.md,
  not a file in this repo). Advisory-only (link check is not in the HARD tier); the DRAFT is
  Phase-1 input evidence — not retro-edited.
- `intermediate/eval-coverage-baseline.md` still quotes a stale "229 cases" figure — frozen
  Phase-1 planning document; the authoritative counts are computed per map row 17 at run time
  (no doc restates them). Left as frozen historical evidence.
- Frozen interface schemas keep their pre-change example paths (`migration-map.schema.md:42`,
  `rewrite-provenance-report.schema.md:41`) — D10 version freeze (additive-only; a new schema
  version = a new directory); re-pointing belongs to the next schema version, not a retro edit.
- **Judgement call (S3/P10):** `register_check` H2 tier merge — the prompt §5 names only the four
  new lints; merging the Phase-1-existing register_check into the HARD gate in commit A was a
  scope judgement (already pushed; the alternative — a separate advisory gate — would have left
  the D-1/R-001 seed unchecked as state). Recorded here so the reviewer can reverse it in Phase 3
  without touching the lints.
- CHANGELOG.md:24 (release-history mention of the roadmap) and `docs/prompt.md:102` (prose
  inventory list) — plain-text history, append-only; not pointers, kept per §2 census.
- `runlog.md` Phase-2 line — transition-thin by design (map row 13: runlog is being replaced by
  git + incident-ledger; thin pointer form allowed during transition). Full run detail lives in
  this record, so no fact is duplicated at a third layer.
