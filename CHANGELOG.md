# Changelog — Research-Code-Docs

All notable changes to this project. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions use the system-level release version
(see [VERSION](VERSION) / [release-manifest.yaml](release-manifest.yaml)), which is distinct from the
per-skill `skill_version`s.

## [0.1.0-alpha.1] — 2026-08-06 — Internal Preview

First packaged, installable, verifiable, rollback-able internal-preview release. Content baseline:
commit `9dc7f18` (Sprint 6 — the first real `documentation-refactor` closed loop). This release adds no
skill logic on top of that baseline; it is **release engineering** (packaging, install, preflight, smoke
test, licensing, docs).

### Added
- **First `documentation-refactor` closed loop** (dry-run migration + candidate rewrite + advisory
  quality review + maintenance proposal), formally supported at dry-run + candidate-output scope.
- **Artifact interfaces** — the frozen 12-field handoff contract (`references/interfaces/`) plus the
  Batch-5 additive types (migration-map, rewrite-provenance-report, maintenance-impact-report).
- **flow-state** contract + honest-BLOCKED semantics for the L1 control flows.
- **Three Batch-5 doc executors** — `content-canonicalization-and-migration` (dry-run),
  `technical-document-rewriter` (candidate-output, never overwrites), `living-design-maintainer`
  (proposal-only) — each with its own deterministic checker.
- **Deterministic checkers** wired into `run_checks.py` (HARD: front-matter, status-vocab; ADVISORY:
  interface, flow-state, migration, rewrite, maintenance; + signal checkers).
- **Release engineering** — `VERSION`, `release-manifest.yaml`, `scripts/preflight.py` (read-only),
  `scripts/install_workspace.py`, `scripts/smoke_test.py`, and the clean-room procedure.
- **Release docs** — `INSTALL.md`, `UNINSTALL.md`, `QUICKSTART.md`, `SUPPORTED_ENVIRONMENTS.md`,
  `SUPPORT_MATRIX.md`, `KNOWN_LIMITATIONS.md`, `LICENSE`, `NOTICE`, `THIRD_PARTY_LICENSES.md`, `README.md`.

### Included (from the baseline, now formally packaged)
- **11 atomic skills** usable as manual advisory tools (DQE 0.4.1; PSR/GSWE/UDM 0.2.0; the 7 Batch-2/5
  atoms 0.1.0).
- **2 experimental L1 flows** — `scientific-workspace-reconstruction`,
  `numerical-research-software-design` — prefix-only, stop honestly at unbuilt capabilities.

### Safety
- **Manual-only** — every skill ships `disable-model-invocation: true`; **no auto-trigger** anywhere.
- **No destructive writes** — originals are never moved, deleted, or overwritten (sha256-verified).
- **DQE advisory-only** — an ALLOW authorizes nothing; unsupported profiles return
  `GATE_DECISION=INCOMPLETE`.
- **Explicit-approval block** — an unauthorized overwrite/delete request yields
  `flow_status=BLOCKED / blocked_by=explicit-write-approval-required`.
- **Isolated install** — workspace-local by default; nothing written to a user-global loader.

### Known limitations
See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md). Highlights: COMPLETE means dry-run + candidate scope
only (not applied migration); some Batch-1 skills lack full task-quality/multi-turn tests; the workspace
and numerical flows do not yet close a loop; single-corpus generalization evidence; large-corpus
performance unmeasured.

### Not included (explicitly unsupported in Alpha)
auto-trigger · destructive apply · auto-publish · candidate→canonical · universal terminal gate ·
experiment reproducibility-release admission · full numerical/workspace closed loops. See
[SUPPORT_MATRIX.md](SUPPORT_MATRIX.md).

[0.1.0-alpha.1]: https://github.com/ArmourPiercer1/research-code-docs/releases/tag/v0.1.0-alpha.1
