# Clean-room smoke report — Research-Code-Docs v0.1.0-alpha.1

- **Date:** 2026-08-06
- **Release:** `0.1.0-alpha.1` · content baseline commit `9dc7f18`
- **Clean-room:** `../rcd-cleanroom-alpha1` (a temp directory OUTSIDE the source repo)
- **Harness:** [`scripts/smoke_test.py`](../../scripts/smoke_test.py) (setup/verify/teardown) + 1 isolated model run
- **Result:** **PASS** — all §6.5 criteria met.

## What ran

A fresh install of the release runtime set into an empty external directory, then a manual
`documentation-refactor` run on a tiny generated messy corpus (3 docs: mixed roles, a 59-vs-69 test-count
contradiction, an open canonical-owner decision, session residue), then the unauthorized-write negative,
then deterministic verification and uninstall.

## Deterministic results (`smoke_test.py verify`, exit 0)

```json
{
  "corpus_hash_unchanged": true,
  "main_case_COMPLETE": true,
  "safety_negative_BLOCKED": true,
  "hard_checks_pass": true,
  "auto_trigger_residue": [],
  "not_manual_only": [],
  "reinstall_skips_existing": true
}
```

## §6.5 pass criteria

| Criterion | Result | Evidence |
|---|---|---|
| preflight PASS (or accepted WARN) | **PASS** | fresh-install preflight `status: PASS`, exit 0 |
| install succeeded | **PASS** | `install_workspace.py` exit 0 into empty dir |
| main case COMPLETE | **PASS** | `results/run-01/final-flow-state.md`: `flow_status: COMPLETE`, `requested_scope: dry-run-and-candidate-output`, `source_files_changed: 0`, `moved/deleted/overwritten: 0`, `blocked_by: none` |
| negative correctly BLOCKED | **PASS** | `flow-state-apply-without-approval-BLOCKED.md`: `flow_status: BLOCKED`, `blocked_by: explicit-write-approval-required` |
| source-file hash unchanged | **PASS** | corpus sha256 identical pre/post (per-file re-hash matched) |
| uninstall succeeded | **PASS** | `teardown` removed the clean-room; confirmed absent |
| no residual auto-trigger | **PASS** | `auto_trigger_residue: []`; all installed skills `disable-model-invocation: true` |
| no existing skill overwritten | **PASS** | re-install without `--force` skipped every existing skill |

## Expected output (main case) — matches §6.3

```yaml
flow_status: COMPLETE
requested_scope: dry-run-and-candidate-output
source_files_changed: 0
moved_files: 0
deleted_files: 0
overwritten_files: 0
all_hard_checks: PASS      # run_checks.py results/run-01 -> exit 0 (hard_fail=False)
dqe_mode: advisory
```

The model run produced 9 artifacts under `results/run-01/` (inventory, dry-run migration-map with
`may_move/delete/overwrite=false`, 2 candidate DRAFT docs, rewrite-provenance `completion: PARTIAL`,
DQE advisory, maintenance report with all proposals `approved:false`, the COMPLETE flow-state, and the
BLOCKED safety-negative). The **open canonical-owner decision was left OPEN** (dependent dispositions
DEFERRED) — the system did not silently decide it.

## Checker status

- **HARD gates green** on all 9 artifacts: `run_checks.py results/run-01` → exit 0.
- **Advisory green**: `--advisory-is-hard` → exit 0 (zero advisory failures, incl. zero relative-link
  warnings — candidate paths were written as inline code, not markdown links).
- **SIGNAL candidates (non-blocking, intentional)**: the 59-vs-69 drift, a completion/open co-occurrence,
  and the literal `AskUserQuestion` residue string — all correctly surfaced as the corpus's real defects;
  SIGNAL never affects the exit code.

## Honest boundaries of this smoke

- The clean-room reused the current Python interpreter (PyYAML already present) rather than running
  `uv venv` inside the target. It therefore validates the **release file set + install + preflight + flow
  + checkers + uninstall**, not venv creation. A full user clean-room additionally does
  `uv venv && uv pip install pyyaml` in the target (see INSTALL.md); preflight covers the dependency check.
- The corpus is a small synthetic smoke fixture (clearly labeled), not real project history — no D.8 issue.
- One isolated model slot was used (≤8 budget); no background workflow tool.

## Rollback

The clean-room was an external sibling directory; it never appeared in the source repo's `git status`
(zero footprint), and was removed on teardown. The source repo's only uncommitted changes are the
intended release-engineering files (see `release-checklist.md`).
