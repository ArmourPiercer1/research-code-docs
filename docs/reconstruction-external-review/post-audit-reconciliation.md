# Post-Audit Reconciliation — Phase 0 findings vs current `main`

```text
generated_by: parent agent (repair round, per repair guide R1)
scope:        every D/P finding used by the Phase 1 proposal or the Phase 2 slice,
              re-verified against current main (HEAD 3bb307f, 2026-09-10)
baseline:     Phase 0 audit ran at HEAD f404d72 (18 commits); post-audit commits:
              098f2bb (track frozen contracts), 4e839b2 (stale doc fixes),
              4df8f7f (recorded install state), 3bb307f (sanitized external-review copy)
              (62ada30 / f404d72 are pre-audit boundary commits, listed for completeness)
method:       each D-item re-opened on current main (file:line or git ls-files);
              status = RESOLVED-BY-CURRENT-MAIN | PARTIALLY-RESOLVED | STILL-LIVE
              Historical cost figures in pain-point-evidence.md are NOT rewritten
              (repair guide §3.3) — they remain valid historical evidence.
date:         2026-09-10
status:       part of the Phase-1 repair round (repair guide §1)
sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ./README.md; 2026-09-10, repair round)
```

## 1. Discrepancy ledger D1–D19 (current-system-map §G + ownership-map §3)

| ID | Audit finding (at f404d72) | Current-main status (3bb307f) | Current evidence | Architecture consequence |
|---|---|---|---|---|
| D1 | README undercounts L1 flows ("2 experimental L1 flows" vs 3 shipped) | **STILL-LIVE** | README.md:30 unchanged | Phase 2 slice's same-change owner updates include this line (status row 4b) |
| D2 | evals/skills/README.md stale (checker census, HF catalog, empty regression/) | **STILL-LIVE** | evals/skills/README.md layout block unchanged; 4df8f7f only added the install cross-reference line | Not a Phase-2 target by itself; covered by the row-6b/17 computed-census rule; candidate for a future simplification audit |
| D3 | documentation-refactor SKILL.md "v0 SKELETON / NOT BUILT" vs Sprint-6B COMPLETE | **RESOLVED-BY-CURRENT-MAIN** | 4e839b2: SKILL.md status/banner/chain/expected-result rewritten to post-6B state; verified by re-read | Phase 1 statements citing D3 as a live exemplar updated (I2(b), I6(b), I11(b), Q10, eval-plan defect 6); D14 becomes the live exemplar of this class |
| D4 | docref-conf-03 expected BLOCKED-at-Batch-5; dataset_version never bumped | **RESOLVED-BY-CURRENT-MAIN** | 4e839b2: case re-baselined (hold_at_blocked at apply-gate, blocked_by=explicit-write-approval-required), dataset_version 2 | Same as D3 |
| D5 | checker-tier bookkeeping mismatch (release-manifest signal list vs run_checks.py classification) | **STILL-LIVE** | release-manifest.yaml `checkers.signal` unchanged (markdown_links_check + register_check + placeholders_check listed as signal; run_checks.py:46-58 still ADVISORY/unregistered) | Feeds the R11 re-trim: release-manifest checker tier becomes a generated view of run_checks.py, not a second hand list |
| D6 | "workspace-only isolation" vs all-14 user-level installed, untracked | **PARTIALLY-RESOLVED** | 4df8f7f: install state now recorded (docs/skill-development/README.md "Recorded install state"; evals/skills/README.md cross-reference). The registry meta `isolation:` line still reads "workspace-only; nothing here is installed…" — corrected in this repair round | Row 16 (install state) stands; A5 (preflight record) is the durable mechanical half. User ruling 2026-09-10: the install is a deliberate Mode-B test fixture, not a defect |
| D7 | registry PSR upstream "(PLANNED; self-inventories until built)" — WFI built 2026-08-05 | **STILL-LIVE** | skills-registry.yaml:89 comment unchanged | Phase 2 same-change updates (roster notes); long-term the note derives from the graph (R7) |
| D8 | task-quality/reader_test "pending" in registry while case files exist, no run recorded | **STILL-LIVE** | skills-registry.yaml:102 `task_quality: pending` unchanged | Eval-plan: task-quality runs must be RECORDED (existing D8 gap) — carried into the slice's focused-verification records |
| D9 | DQE SKILL.md:21 cites docs/third-party-suggestions/… — archived + git-ignored since f404d72 | **STILL-LIVE** | DQE SKILL.md:21 pointer unchanged (4e839b2 fixed line 9 only) | Phase 2 same-change updates: pointer → archived path (frozen-directive label per row 9) |
| D10 | frozen interfaces/templates git-untracked ("frozen" with no history) | **RESOLVED-BY-CURRENT-MAIN** | 098f2bb: 24 files tracked (11 schemas + README + 12 templates); `git ls-files references` verified | Row 3/11 Δ updated; Q5 "no git history" statement corrected; the eval-plan defect-1 fixture re-anchored to D12 (see §2) |
| D11 | deep-research listed as installed L3, absent from live loader | **STILL-LIVE** | skills-registry.yaml:538 row unchanged; live loader unchanged (byte-identical 14-skill install) | A5 preflight record closes it mechanically when built; until then the roster line stays flagged |
| D12 | VOID roadmap still referenced (DQE:9; system-architecture status line) | **PARTIALLY-RESOLVED** | 4e839b2: DQE SKILL.md:9 → ADR-DQE-001 (fixed). system-architecture.md status line "DECIDED for Phase 1" without charter pointer still stale; roadmap still tracked and unarchived | **STILL-LIVE for the Phase-2 slice as its selected simplification candidate** (archive + pointer fixes = the ratchet event; the D-1 decision note lands with it) |
| D13 | "134 case files" claim vs measured 41 YAML/229 cases | **STILL-LIVE** | docs/skill-development/README.md:82 unchanged | Row 17 computed census is the fix; the hand count becomes a link-to-computation |
| D14 | SWR SKILL.md:49 lists LDM "[BLOCKED: not built]" — LDM built in Sprint 6B | **STILL-LIVE** | SWR SKILL.md:49 unchanged | NOW the live exemplar of the stale-builtness class (D3 was its twin; D3 resolved). Phase 2 same-change updates |
| D15 | candidate-doc-set copies drifting from live docs (unapplied) | **STILL-LIVE** | evals/skills/results/batch3/documentation-refactor-closure/candidate-doc-set/ unchanged | Candidate set re-validated or archived (row 11 rule); not a Phase-2 target itself |
| D16 | "nothing was modified" restated in 5+ places per release | **STILL-LIVE** | restatements unchanged (runlog:57, smoke-report:82-84, final-flow-state:53-57, sprint6:20-21) | Row 1 (git owns chronology) + state-consistency-lint (deferred, R11) |
| D17 | corpus dataset version + census in 4 places, code defaults not read from manifest | **STILL-LIVE** | aggregate_eval_results.py:248-29 defaults unchanged | Row 6b (split) + row 17 computed census |
| D18 | safety posture in 5 copies | **STILL-LIVE** | manifest:43-51 / README:37-41 / SUPPORT_MATRIX:28-34 / CHANGELOG:58-65 unchanged | Row-6c split (release reproducibility metadata) |
| D19 | "PRESERVED" frozen DQE snapshots vs empty dir (untracked in f39fbb2) | **STILL-LIVE (reframed)** | snapshot bundles now EXIST on disk (21 files) — built post-audit — but `git ls-files evals/skills/snapshots/` = 0: the "freeze" still has no version history, the audit's core defect | Row 6c: snapshots become tracked (reproducibility metadata is a canonical family); the registry claim is only true once tracking lands |

**Net:** RESOLVED 3 (D3, D4, D10) · PARTIALLY-RESOLVED 2 (D6, D12) · STILL-LIVE 14.

## 2. Pain points P1–P10 (cost evidence — figures NOT rewritten)

All P-items are historical cost events and remain valid as measured history. Their
current-main status, for the purpose of "which defect does Phase 2 still attack":

- **P5 (stale/duplicated current state — the only still-active top-3 failure mode):**
  STILL-LIVE, but its verified-instance list shrinks: D3/D4/D12-partial/D10 resolved by
  098f2bb/4e839b2/4df8f7f; live instances now = D1, D2, D5, D7, D9, D11, D13, D14, D15,
  D16, D17, D18, D19. The disease is the same; the Phase-2 slice must be re-anchored to
  live instances only (done in revised-phase2-vertical-slice.md).
- **P1 (63M-token runaway) / P3 (2.6M):** one-shot paid costs — the fix (change-scope
  selection, A9) stands on those measurements; the incidents themselves are closed.
- **P2 (DQE false pass) / P4 (canary):** closed as events; their guardrails (HF-13/14/15,
  advisory freeze, A6 deferral) are current and unchanged.
- **P7–P10:** as audited; no post-audit commit touches them.

## 3. Phase 1 statements corrected by this reconciliation

Statements in the Phase 1 proposal that described a RESOLVED defect as live are updated
in place (this round):

1. `target-workflow-invariants.md` I2(b): D3 cited as live duplication → marked resolved,
   D14 named as the live exemplar of the same class.
2. `target-workflow-invariants.md` I6(b): live-gap list re-anchored (D4 resolved; D14/D7
   live).
3. `target-workflow-invariants.md` I11(b): "creation-roadmap … still referenced (D12)" →
   partially resolved (DQE:9 fixed; system-architecture line + unarchived file remain).
4. `target-workflow-invariants.md` Q5: "D10: frozen contract … currently has no git
   history" → corrected (24 files tracked since 098f2bb).
5. `target-workflow-invariants.md` Q10: "(D3, D14)" → "(D14; D3 resolved 4e839b2)".
6. `canonical-information-model.md` row 1 Δ: tracking gap → partially realized
   (interfaces/templates tracked; upstream pins + snapshots still ignored).
7. `canonical-information-model.md` row 3 Δ: "(currently 0 tracked files under
   references/)" → "(24 files tracked since 098f2bb)".
8. `canonical-information-model.md` row 16 Δ: D6 "untracked" → "recorded since 4df8f7f".
9. `eval-plan.md` adversarial defect 1: fixture anchored to "the D10 live instance" →
   re-anchored to the D12 live class (VOID roadmap not yet archived).
10. `eval-plan.md` adversarial defect 6: "(the D3/D14 live class)" → "(the D14 live
    class; D3 is the resolved exemplar)".
11. `skill-change-matrix.md` header label-census "KEEP×13" → "KEEP×15" (the file's own
    §6 row-by-row census — internal inconsistency, not a review item).
12. `docs/skill-development/skills-registry.yaml` meta `isolation:` line → records the
    documented Mode-B test install (closes the D6 residue; user ruling 2026-09-10).

Historical cost figures (P1 63M tokens/11h; P3 2.6M; the canary 0.7M) are unchanged
everywhere, including in the sanitized external-review copy (it describes the audit-time
state; this reconciliation is the current-state layer).

## 4. Consequence for Phase 2 targeting (input to R9)

The slice must not re-solve D3/D4/D10 (already solved) and must not treat the D6 install
as a defect. Still-live, real, and small — the slice's candidate pool:

| Candidate class (repair guide §11.3) | Still-live instance | Size | Decision needed? |
|---|---|---|---|
| obsolete roadmap authority | creation-roadmap.md VOID since 2026-09-09, tracked, unarchived, 2 inbound refs (D12-residue) | archive + 2 pointer fixes | YES — D-1 (which doc owns "what is next" after the roadmap leaves) |
| duplicated status owner | D1 (README flow count), D13 (case count), D7/D9 stale notes | N small owner updates | NO (mechanical same-change updates) |
| stale builtness claim | D14 (SWR LDM line) | 1 line | NO |
| frozen-without-history | D19 (snapshots untracked) | git add + claim check | NO |

Selected: the **obsolete roadmap authority** (largest single governance overhead,
ratchet remove-side, and the one that forces a durable human judgment — D-1 — so the
slice exercises the decision-note mechanism on real data). Full design:
`revised-phase2-vertical-slice.md`.
