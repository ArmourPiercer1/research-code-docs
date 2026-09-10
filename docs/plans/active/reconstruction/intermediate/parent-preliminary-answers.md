# Parent Preliminary Answers — Charter §17 (17 questions before broad coding)

<!--
generated_by: parent agent (pre-draft, round 5)
status: PRELIMINARY — based on the initial workspace audit (session turn 1) + git log;
        S2 must CONFIRM, CORRECT, or CITE phase0 evidence for every answer.
        Where this file is wrong, the phase0 deliverables win.
date: 2026-09-09
-->

Grounding used: README/CHANGELOG/KNOWN_LIMITATIONS/SUPPORT_MATRIX, docs/skill-development/**
(reports incl. dqe-v0.3/0.4/0.4.1, batch2_5, sprint6), evals coverage baseline
(intermediate/eval-coverage-baseline.md), git log 279c0ce..f404d72.

1. **Three most expensive real failure modes?**
   (a) DQE false PASS on a broken hybrid roadmap (v0.2 era): FAILed only on trivial HF-9,
   still called it "substantively high quality", predicted re-eval PASS — caught by an
   independent audit; drove the v0.3 upgrade (anti-erosion discipline, HF-13/14a/14b/15,
   decomposed HF-12A–E, non-compensatory scoring, 5 SIGNAL checkers, permanent golden-negative).
   (b) DQE false ALLOW for `controlled + release-gate` (Phase E canary D-17): a
   reproducibility experiment report stably false-ALLOWed; resolution was scoping the profile
   OUT (INCOMPLETE/unsupported-evaluation-profile) and deferring Phase E entirely.
   (c) Independent-check + blind-matrix failures (docs/skill-development/reports/
   documentation-quality-evaluator_独立检查失败复盘与升级要求.md;
   dqe-blind-matrix-investigation-2026-07-31.md; corpus-repair-report-v4.md):
   harness-level false positives/negatives (code-fence masking, dual-vocab status,
   provenance-in-comment — 3 precision bugs found while dogfooding checkers) plus corpus
   quality issues requiring v4 repair.
   Secondary (documented, cheaper): stale docs discovered mid-integration in batch2.5
   Track A; no-skill baseline silently deciding open decisions D-1/D-4 (sprint6 report).

2. **Which existing skills already solve them?**
   DQE v0.4.1 solves (a) partially (golden-negative recall 1.0 / false_pass 0 for the eoopt
   case; comprehensive report still PASSes) and (b) by profile admission (Rule 0).
   Deterministic checkers solve harness precision bugs mechanically. NOT solved:
   task-quality/multi-turn coverage for PSR/GSWE/UDM (KNOWN_LIMITATIONS #5); the three
   Batch-5 executors have light tests only (#6); cross-project generalization is single-
   corpus (#9); large-corpus behavior unmeasured (#10).

3. **Which DSH mechanisms are DSH-specific?**
   Preliminary (confirm with intermediates): TypeScript/Cordis gates (oxlint/jscpd
   configs), E2B e2e workflow, sandbox workflows, vendor-publish + python-SDK release
   pipelines, brand-guidelines machinery, `record-browser-gif`, `dsh-translate-docs`,
   `dsh-trim-cot-leakage`. Generic candidates: AGENTS.md layering, .agents/skills +
   .agents/notes with lifecycle, docs/AGENTS.md + docs/testing.md ownership, snapshot/
   replay + pre-push smallest-evidence selection, code-review/simplification skills,
   stacked-PR/worktree discipline, flaky-test policy.

4. **Which rules belong in skills vs mechanical gates?**
   Mechanical (already checker-able or should be): front-matter + disable-model-invocation,
   status vocabulary, 12-field interface completeness + no-placeholder, flow-state
   semantics (COMPLETE-scope vs approval), migration-map invariants (may_move/delete/
   overwrite=false, no target==source, no duplicate primary), rewrite provenance
   (sha256 source unchanged, candidate≠source, no fact-upgrade), maintenance proposals
   (approved:false, no auto-publish), corpus non-mutation.
   Skill (judgment): quality grading within profile (DQE), state reconstruction
   (PSR), goal/scope elicitation (GSWE), evidence synthesis + sufficiency (RES/UDM),
   IA design, rewrite craft, maintenance impact reasoning.
   Convention/AGENTS.md: where artifacts live, when to re-run PSR, review-gate points.

5. **Which artifacts are canonical / transient / auto-obsolete?**
   Canonical: .agents/skills/**/SKILL.md, evals/skills/harness/** (checkers + rubric +
   hard-fail + canonical-source-map), references/interfaces/** (frozen), release-manifest
   .yaml, VERSION, skills-registry.yaml, corpus (tests/corpus/source-seeds + golden
   fixtures). Transient: flow-state during a run, injection prompts, candidate-doc-set
   (until human promotes), smoke clean-rooms. Auto-obsolete: dated reports (superseded by
   later dated report on the same subject — rule is implicit, never stated), plans in
   docs/plans (archived on completion), execution notes.

6. **What should remain only in Git history?**
   Implementation chronology: runlog.md is the borderline case — it duplicates report
   narratives (each run already produces a dated report + git commit with message).
   Per-change rationale that is already in the commit message. Snapshot bundles
   (evals/skills/snapshots/) are already git-ignored — their provenance lives in
   SNAPSHOT-MANIFEST.yaml; fine as-is.

7. **Minimal context for a new agent to take over?**
   README.md + SUPPORT_MATRIX.md + KNOWN_LIMITATIONS.md + the active plan (+ its
   reconstruction/README) + the SKILL.md of the skill(s) in use. Today that set is
   honest (post-rename) but the "current state" must be re-verified by PSR after the
   rename commit (not yet re-run — see Q15).

8. **Which current workflows are blocked by capabilities designed before they existed?**
   scientific-workspace-reconstruction → BLOCKED at dev-test-experiment-workspace-architect
   (Batch 5 remainder, unbuilt). numerical-research-software-design → BLOCKED at the six
   Batch-4 numerical-design atoms (unbuilt). Both are *honest* BLOCKED (named blocked_by),
   which is the designed behavior — but the design debt is real: the L1 flow SKILLs were
   written ahead of their executors (skeleton-first cadence).

9. **Which status models conflate dimensions?**
   UDM decision-register status vocab: mixes epistemic status, decision lifecycle,
   freshness, implementation progress, role in one field (charter §12.6 concern; the
   register does carry E-levels separately, but the status field is still mixed).
   flow_status: COMPLETE/BLOCKED conflates "scope-complete" with "approved-to-continue"
   — in Alpha this is defensible (completion semantics pinned in release-manifest) but
   it will need the orthogonal split when apply-mode is ever added.
   Skill lifecycle (experimental/active) vs version (0.x) is handled separately — OK.

10. **Which DSH mechanisms were simplified/removed later?**
    PENDING subagent D (14,882-commit history; survey shows release churn 0.1.2-alpha.x →
    rc.1, merge-PR workflow, dual CI). Not yet answered.

11. **If half the proposed new mechanisms were removed, which capability is actually lost?**
    PENDING S2 portfolio design. Preliminary instinct: the cheap-to-cut half is the
    "second ledger" class (duplicate chronologies, extra report types); the expensive-to-
    cut half is the mechanical non-mutation + interface checks (safety posture is the
    product).

12. **Can a generic change be completed without producing new permanent artifacts?**
    Today: NO for flow runs — each documentation-refactor run writes ~10 artifacts
    (QUICKSTART §5). Some are load-bearing (flow-state, provenance); the runlog line
    duplicates the dated report (see Q6). For non-flow edits (doc fixes), the repo already
    needs only the commit — OK.

13. **Can a research route be paused/rejected/revived without falsifying history?**
    Decision level: YES — UDM has supersession with both rows retained (verified in
    runlog: LU→CG by supersede). Route level: NO mechanism exists (no route/workstream
    object in the system at all — the closest is goal-scope-note per run, which is
    session-local).

14. **Can "strong literature support" be distinguished from "verified here"?**
    PARTIAL: UDM register carries evidence_level E0–E5 and DQE has the
    FACTUAL_VALIDITY axis (VERIFIED/PARTIALLY_VERIFIED/UNVERIFIED), but nothing
    mechanically links the two today (a doc citing literature can read "verified" to a
    checker). Charter §8.3 requires the distinction be impossible to blur.

15. **After 20–50 changes, can current state be recovered without reading everything?**
    Today: DEGRADED. Evidence: creation-roadmap.md stayed "PLANNED for Batch 4" until
    manually VOIDed 2026-09-09 (stale-roadmap risk materialized); docs/skill-development/
    README banner was a Phase-1 snapshot (last_verified 2026-08-05) even though the
    release happened 2026-08-06 and the rename 2026-09-09; PSR has never been re-run
    after the release packaging. A no-context reader CAN get goal/state/next from
    README+SUPPORT_MATRIX+active plan, but "current" claims need re-verification.

16. **Can "strong literature support" be separated from in-project verification in
    artifacts?** (same family as 14, asked from the artifact side)
    PARTIAL: artifact types separate evidence (evidence-synthesis outputs) from quality
    verdicts (DQE advisory), but the handoff does not carry a provenance_policy field
    for evidence-vs-verification in all seven frozen handoff types; the Batch-5 additive
    types (rewrite-provenance-report) DO separate source sha256 vs candidate — good
    pattern to generalize.

17. **After many changes, is the system still understandable (not just demoable)?**
    Today: YES for a reader who follows the governance chain (charter → README → registry →
    reports), at the cost of reading ~15 docs. The complexity budget is the open question:
    14 skills + 3 flows + 5 checker families + 2 corpus tiers + release engineering is
    already large relative to the supported surface (1 workflow). Phase 4 simplification
    (charter §15) must test this; the ratchet needs a deletion target, not just additions.
