---
name: focused-verification
description: FOCUSED VERIFICATION of an implemented change against its explicit change contract — capture the actual changed paths (git diff/base vs HEAD or working tree), check them against the declared scope and impact declaration (changed ⊆ declared; every impacted canonical owner updated in the same change or justified no_impact), run the SMALLEST sufficient set of checks (the change's lints + self-tests + preflight — each check justified by the contract, no deferred dependency-graph gate), verify untouched-scope integrity by hash, and record a verification record with per-check evidence. It answers "did the change do exactly what it declared, and is the rest of the repo intact?". Use AFTER a concrete change is implemented (archive move, pointer fixes, store creation) and BEFORE its commit is accepted. NOT for verifying unimplemented plans (simplification-audit is pre-change), NOT for whole-repo release review (release gates own those), NOT for code-quality review of implementation style (code-review skill).
disable-model-invocation: true
---

<!--
skill_version: 0.1.0
status: experimental (manual/orchestrator-only; Phase-2 vertical slice, 2026-09-10)
generated_by_skill: manual authoring (Phase-2 vertical slice; per research_code_docs_phase2_implementation_prompt.md §2.2 A9)
source_commit: 1dc6b8694dac60ac355b8094e61ffebde322fba0
source_documents:
  - docs/plans/active/research_code_docs_phase2_implementation_prompt.md §2.2 (A9 spec)
  - docs/plans/active/reconstruction/revised-phase2-vertical-slice.md §3 (chain: ... → host → A9 → two-axis review)
  - evals/skills/harness/checkers/ (the check corpus A9 draws its minimal set from)
  - evals/skills/harness/checkers/canonical_impact_lint.py (change-level impact discharge check)
last_verified: 2026-09-10
-->

# Focused Verification

> **Experimental · manual-only · READ-ONLY** (writes exactly one artifact: its own
> verification record). Given an *implemented* change and its **change contract** (the audited change
> set + impact declaration from `simplification-audit`), this skill verifies three things and only
> three: **the change did exactly what it declared**, **the declared canonical impacts were discharged
> in the same change**, and **nothing outside the declared scope moved** (hash integrity). It runs the
> **smallest sufficient check set** — every check it runs is justified by a contract line; it does not
> substitute a whole-repo release review, and it does not wait on a future (deferred) dependency-graph
> checker that Phase 2 deliberately does not build.

## Purpose

Produce a **verification record**: per-check PASS/FAIL with the exact command, output fingerprint, and
evidence (file:line / commit / sha256), covering (1) changed-path conformance against the contract,
(2) canonical-impact discharge (R2 — no timestamp-only discharges), (3) the minimal targeted check set
(the change's lints + their self-tests + preflight), and (4) untouched-scope integrity. The record is
the artifact the two-axis review reads; a FAIL anywhere makes the change **not verified** — the record
says which check, with evidence, and the smallest action that would clear it.

## Trigger conditions

Engage when:
- A concrete change is **implemented and pending acceptance** (an archive move + pointer fixes, store
  creation + tracking transition, a lint portfolio landing) and its contract (from
  `simplification-audit`) is available.
- The **Phase-2 vertical slice** needs its gate evidence: "the change did what the candidate said, in
  the scope it said, and nothing else moved."
- A commit's claims ("I only touched X") must be **recomputed** from `git diff`, not trusted.

## Do-not-trigger conditions

- The change is **not yet implemented** → `simplification-audit` (A8) first; A9 verifies reality, not
  intent.
- The request is a **whole-repo release review** or a spec/standards review of the diff's *content
  quality* → the release gates and the two-axis (standards/spec) review own those; A9 is the mechanical
  half of "did it do what it said".
- The request is **code-quality review** of how the implementation is written → `code-review`.

## Inputs

- `contract` — the change contract: `impact-declaration.yaml` (changed_paths + canonical_owners) and
  the audited change set (simplification-audit report).
- `base` — the git ref the change is measured against (the pre-change commit).
- `scope` — the declared change scope (directories/files the change claims ownership of).
- `checks` — the minimal check set, each entry = command + the contract line that justifies it.

## Context budget

Verification is **evidence-first, reading-second**: start from `git diff --name-only` and the
contract, then read only the diffs of declared files and the specific lines a failing check points at.
Keep working context under **~2,000 focused lines**; a failing check that needs more context is
investigated in a focused follow-up, not by re-reading the repo. `whole_repo_allowed: false` —
repo-wide steps are the *hash integrity* pass (mechanical, no reading) and the lint runs (the
checkers read what they read; A9 reads their reports).

## Workflow

1. **Capture actual changes.** `git diff --name-only <base>..HEAD` (or `--worktree` before commit),
   plus untracked-new files in scope. Build the **actual change set**; compare against
   `contract.changed_paths`:
   - actual ⊄ declared → **undeclared change** (FAIL, per path);
   - declared ⊄ actual → **missing declared work** (FAIL, per path);
   - equal → conformance PASS, recorded with both lists.
2. **Canonical-impact discharge (R2).** Run
   `canonical_impact_lint.py --impact <impact-declaration.yaml> --base <base> [--worktree]`:
   every impacted owner updated in the same change or justified `no_impact`; timestamp-only changes
   (last_verified/last_evaluated/last_updated/date) do **not** count as discharge.
3. **Run the minimal check set.** Each check must map to a contract line (record the mapping):
   - the change's own lints + their **self-tests** (planted defects caught — a planted defect not
     caught is a release blocker);
   - `scripts/preflight.py` (the standing preflight must stay green);
   - `run_checks.py` over the **touched scopes** (not the whole repo, unless the contract says so);
   - the target-specific checker(s) the change introduced or relied on (e.g. `archive_lint.py --repo`
     for an archive move).
   A check that is **not** justified by the contract is not run here (it belongs to the release gate
   or a later change) — and that exclusion is *recorded*, not silent.
4. **Untouched-scope integrity.** For the declared **untouched** set (the complement the contract
   names — at minimum: every tracked file outside scope): compare sha256 (or `git status` porcelain +
   `git diff --stat`) before/after; any moved hash outside scope = FAIL, per file.
5. **Record the verification record.** `verification-record.md`: contract ref + base commit · actual
   vs declared change set (both lists) · impact-discharge result · per-check table (check · command ·
   justification · PASS/FAIL · evidence fingerprint) · untouched-scope integrity (method + result) ·
   explicit list of checks **deliberately not run** and why (e.g. "no deferred dependency-graph
   checker exists in Phase 2; not required by contract") · verdict: **VERIFIED** / **NOT VERIFIED**
   (with the smallest clearing action per FAIL).
6. **Verdict discipline.** ANY FAIL → NOT VERIFIED. No "verified with notes". The record carries the
   failing check's evidence so the next action is mechanical, not re-discovered.

## Verification discipline (the gates that keep this skill in its lane)

- **Recompute, don't trust.** The commit message / plan's "only touched X" is an input to recompute
  from `git diff`, never a result.
- **Smallest sufficient set.** A check runs because a contract line requires it; the record maps every
  check to that line. No drive-by repo-wide review; no check whose purpose is "just in case".
- **No deferred-checker dependencies.** A check that does not exist yet (a future dependency-graph
  lint) may be *named* in the not-run list — it may not gate this change.
- **Timestamp ≠ discharge.** R2: bumping last_verified/last_evaluated on a canonical owner is not
  updating it (canonical_impact_lint C4 enforces this mechanically).
- **Frozen scope is byte-identical.** Frozen mirrors / results / fixtures in the untouched set are
  hash-compared, not eyeballed.
- **One artifact out.** This skill writes exactly its verification record (and the record's
  evidence files if the change's working folder convention wants them); it edits nothing in the
  verified scope.

## Quality gates (on this skill's own output)

- Actual-vs-declared change sets are both listed in full; every delta has a PASS/FAIL.
- Impact discharge ran (or is recorded as not-applicable with the reason); no timestamp-only
  discharge accepted.
- Every check in the record maps to a contract line; every *excluded* check is named with its
  exclusion reason.
- Untouched-scope integrity states its method (sha256 set / git porcelain) and its result (count +
  any deltas, per file).
- The verdict is one word of {VERIFIED, NOT VERIFIED}; NOT VERIFIED lists the smallest clearing
  action per failing check.
- The record carries traceability front-matter (or fails its own HF-9).

## Outputs

- `verification-record.md` — a **new** file in the change's working folder (e.g.
  `docs/plans/active/reconstruction/phase2/`). Sections: Contract ref + base · Change-set conformance
  (declared vs actual) · Impact discharge (R2) · Minimal check set (table with justifications) ·
  Checks not run (named + why) · Untouched-scope integrity · Verdict + clearing actions.

## Handoff rules

- **VERIFIED** → hand to the two-axis review (standards + spec) as the mechanical half of the gate;
  the review may then accept the change.
- **NOT VERIFIED** → back to the host with the per-FAIL clearing actions; re-run A9 after the fix
  (a fresh record, not an edited one — the record is append-only history).

## Failure modes

- **Pre-commit verification (worktree dirty)** → run with `--worktree`; name it as such in the record
  (post-commit re-verification is a different, cheaper pass against the commit).
- **The contract is missing or stale** (audit predates the implemented change) → record
  NOT VERIFIED with reason "contract mismatch: implemented set ≠ audited set"; the host re-audits
  (A8) before A9 can pass. Do not paper over by editing the contract.
- **A lint fails for a pre-existing (not this change's) reason** → record it as a **pre-existing
  failure** with the baseline evidence (it fails on `<base>` too — show it), and keep the verdict
  honest: NOT VERIFIED for this change's gate if the contract required that lint green, with the
  clearing action = fix or re-scope the contract.
- **Hash integrity over a huge untouched set** → use `git status --porcelain` +
  `git diff --name-only <base>` (mechanical, no reading); sha256 a bounded sample of frozen artifacts
  if git state is ambiguous (e.g. untracked-then-tracked transitions).

## References to load

- `docs/plans/active/research_code_docs_phase2_implementation_prompt.md` §2.2 (the A9 spec this skill
  implements) and §8 (the gate this record feeds).
- `evals/skills/harness/checkers/canonical_impact_lint.py` (R2 enforcement).
- `evals/skills/harness/checkers/run_checks.py` (tiering: HARD/ADVISORY/SIGNAL — what "green" means).
- `scripts/preflight.py` (the standing preflight A9 must keep green).

## Scripts to run

- `evals/skills/harness/checkers/canonical_impact_lint.py --impact <impact.yaml> --base <ref> [--worktree]`
- `evals/skills/harness/checkers/selftest_phase2_lints.py` (planted-defect self-tests for the lint
  portfolio, when the change touched it)
- `scripts/preflight.py`
- `evals/skills/harness/checkers/run_checks.py <touched-scope>`
- `evals/skills/harness/checkers/archive_lint.py --repo` (for archive-move changes)
