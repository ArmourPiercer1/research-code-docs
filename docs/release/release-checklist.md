# Release checklist — Research-Code-Docs v0.1.0-alpha.1

> The Alpha release gate (directive §10.1) + the R0.5 packaging steps (§12). Checked items are verified;
> `[~]` = pending the clean-room smoke run / packaging. Update this file as items complete.

## Alpha release gate (§10.1)

| # | Gate item | Status | Evidence |
|---|---|---|---|
| 1 | system version fixed | **[x]** | `VERSION` = `0.1.0-alpha.1`; `release-manifest.yaml` |
| 2 | release manifest complete | **[x]** | `release-manifest.yaml` parses; 14 skills = registry; supported/experimental/unsupported split |
| 3 | install / uninstall docs complete | **[x]** | `INSTALL.md`, `UNINSTALL.md` |
| 4 | preflight PASS | **[x]** | `python scripts/preflight.py` → `status: PASS` (exit 0) |
| 5 | clean-room smoke main case PASS | **[x]** | `results/run-01/final-flow-state.md` COMPLETE; `smoke-report-2026-08-06.md` |
| 6 | safety negative PASS (BLOCKED) | **[x]** | `flow-state-apply-without-approval-BLOCKED.md` → `blocked_by: explicit-write-approval-required` |
| 7 | source hash unchanged | **[x]** | smoke `verify`: `corpus_hash_unchanged: true` |
| 8 | support matrix complete | **[x]** | `SUPPORT_MATRIX.md`, `SUPPORTED_ENVIRONMENTS.md` |
| 9 | known limitations complete | **[x]** | `KNOWN_LIMITATIONS.md` |
| 10 | license / notice complete | **[x]** | `LICENSE`, `NOTICE`, `THIRD_PARTY_LICENSES.md` |
| 11 | changelog complete | **[x]** | `CHANGELOG.md` |
| 12 | tag points to a fixed commit | **[~]** | `v0.1.0-alpha.1` → packaging commit (local; push gated on owner) |
| 13 | all skills still manual-only | **[x]** | preflight: 14/14 `disable-model-invocation: true` |
| 14 | auto-trigger all false | **[x]** | preflight: no `auto_trigger: true`; registry all false |

## Hard limits honored (§13)

- [x] Phase E not restored · [x] DQE discriminator logic unchanged (no SKILL.md edit) ·
  [x] no auto-trigger enabled · [x] no user-global default install · [x] no destructive apply implemented ·
  [x] no large test-corpus expansion · [x] model slots ≤ 8 (1 clean-room agent) · [x] no background workflow tool.

## R0.5 packaging steps (§12)

- [~] freeze release commit (adds release-engineering files; no skill/logic change)
- [~] run this checklist (all §10.1 green)
- [~] tag `v0.1.0-alpha.1` at the frozen commit **(local; owner pushes)**
- [~] internal release notes (this file + `CHANGELOG.md` + the smoke report)

## Distribution hygiene (§8.2 / §8.3) — exclude from any archive

`.venv/` · `**/__pycache__/` · `*.pyc` · `tests/corpus/upstream|blind-runs/` · `evals/skills/snapshots/` ·
`references/` upstreams (see `THIRD_PARTY_LICENSES.md` before shipping any subset). Encoded in
`release-manifest.yaml → exclude_from_distribution`.
