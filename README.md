# Research-Code-Docs

**v0.1.0-alpha.1 — Internal Controlled Preview** · manual-only · non-destructive · documentation-focused

> Research-Code-Docs is an internal, controlled preview of a Skills system for **research-software
> documentation governance**. It formally supports a **manual, non-destructive documentation-refactor
> dry-run / candidate-output** workflow; other workflows are experimental prefixes; all auto-triggering,
> destructive writes, and universal terminal-gate approval are **off**.

This repository is the **skill content + eval harness**, not a runtime. You run it with
[Claude Code](https://claude.com/claude-code) opened on this workspace, invoking skills **manually**.

## Start here

| If you want to… | Read |
|---|---|
| Install the preview | [INSTALL.md](INSTALL.md) |
| Run it safely the first time | [QUICKSTART.md](QUICKSTART.md) |
| Know exactly what's supported | [SUPPORT_MATRIX.md](SUPPORT_MATRIX.md) · [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) |
| Check your environment | `python scripts/preflight.py` · [SUPPORTED_ENVIRONMENTS.md](SUPPORTED_ENVIRONMENTS.md) |
| Remove it | [UNINSTALL.md](UNINSTALL.md) |
| See the machine manifest | [release-manifest.yaml](release-manifest.yaml) · [VERSION](VERSION) |
| Understand licensing | [LICENSE](LICENSE) · [NOTICE](NOTICE) · [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) |
| See what changed | [CHANGELOG.md](CHANGELOG.md) |

## What's in the box (this release)

- **1 supported workflow** — `documentation-refactor` (dry-run migration + candidate rewrite + advisory
  review + maintenance proposal).
- **11 atomic skills** usable as manual advisory tools; **2 experimental** L1 flows that stop honestly at
  unbuilt capabilities. Phase-2 (2026-09-10) adds two more atomic governance skills —
  `simplification-audit` (A8) and `focused-verification` (A9) — registered `experimental` +
  `disable-model-invocation`, **not yet in the release manifest** (next packaging pass).
- **Deterministic checkers** (front-matter, status-vocab, archive, supersession, decision-note,
  interface, flow-state, migration, rewrite, maintenance, register) + the change-level
  `canonical_impact_lint` + a planted-defect self-test suite + a read-only `preflight.py` and a
  clean-room `smoke_test.py`.

## Safety posture (non-negotiable in Alpha)

```text
manual invocation only · no auto-trigger · isolated workspace · candidate-output only
originals never moved/deleted/overwritten · DQE ALLOW authorizes nothing
unauthorized write request → flow_status=BLOCKED
```

## Project governance (developers)

The design/governance lives under [docs/skill-development/](docs/skill-development/) (architecture,
conflict matrix, skills registry, eval reports) and [docs/](docs/) (canonical source map, decision
register + decision notes); the batch creation roadmap (frozen history, VOID 2026-09-09) is
archived at [docs/plans/archived/creation-roadmap.md](docs/plans/archived/creation-roadmap.md);
execution status / what-is-next lives in the
[reconstruction status table](docs/plans/active/reconstruction/README.md) (D-1). The clean-room
release procedure is
[docs/release/clean-room-smoke-test.md](docs/release/clean-room-smoke-test.md).

---
*Internal preview — not a public release. See [LICENSE](LICENSE) before sharing.*
