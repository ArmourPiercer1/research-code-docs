# SUPPORTED ENVIRONMENTS — Research-Code-Docs v0.1.0-alpha.1

> Four status words, used strictly and never interchangeably:
>
> - **supported** — an intended target; issues here are treated as release defects.
> - **tested** — actually exercised by the clean-room smoke test on this release.
> - **experimental** — expected to work but not validated; use at your own risk, feedback welcome.
> - **unsupported** — not a target for this Alpha; may not work and will not be fixed for Alpha.

---

## Operating systems / runtimes

| Item | Alpha status | Notes |
|---|---|---|
| Windows 11 + Claude Code workspace | **supported · tested** | primary dev + smoke-test platform (this release) |
| WSL2 | **support-candidate** (experimental) | verify path behavior; run a local smoke test before trusting |
| Linux (x86-64) | **support-candidate** (experimental) | expected to work; not smoke-tested this release |
| macOS | **experimental / unverified** | not exercised |

## Python

| Item | Alpha status | Notes |
|---|---|---|
| Python 3.11 | **supported (recommended)** | preferred interpreter |
| Python 3.12 | **support-candidate · tested** | development venv is 3.12 (checkers run here) |
| Python 3.10 | **support-candidate** | minimum per `pyproject.toml` (`requires-python >=3.10`) |
| Python ≤ 3.9 | **unsupported** | below minimum |
| PyYAML ≥ 6.0 | **required** | the only runtime dependency |

## Filesystem / paths

| Item | Alpha status | Notes |
|---|---|---|
| ASCII paths | **supported · tested** | |
| Chinese / non-ASCII path segments | **needs smoke test** (experimental) | run checkers with `PYTHONIOENCODING=utf-8`; the dev corpus contains CJK filenames and passes, but treat as verify-first |
| Non-UTF-8 file *names* | **experimental** | validate before relying on hash/rollback |
| Spaces in paths | **supported** | quote paths |

## Version control

| Item | Alpha status | Notes |
|---|---|---|
| Git repository (corpus under git) | **supported (recommended)** | enables `git status --porcelain` + content-hash source-unchanged proof and tag rollback |
| Non-Git directory | **usable, reduced assurance** | works, but the hash/rollback safety checks are weaker; keep an external backup |

## Claude Code surfaces

| Item | Alpha status | Notes |
|---|---|---|
| Claude Code CLI / desktop / IDE, workspace opened at the install dir | **supported** | how the skills are discovered and invoked manually |
| User-global (`~/.claude/skills/`) install | **unsupported as default** (Mode B) | workspace-relative checker/template paths do not resolve outside a full workspace |

## Scale (measured?)

| Item | Alpha status | Notes |
|---|---|---|
| Small corpus (tens of docs) | **supported · tested** | the smoke + real closed loop ran on `docs/skill-development/` |
| Large corpus (hundreds+ of docs) | **experimental** | performance + context budget not yet measured (see KNOWN_LIMITATIONS §10) |

---

Anything not listed is **unsupported for this Alpha**. Report environment issues per the feedback record
in the release plan (§9.1). See [SUPPORT_MATRIX.md](SUPPORT_MATRIX.md) for *capability* status and
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for the boundaries.
