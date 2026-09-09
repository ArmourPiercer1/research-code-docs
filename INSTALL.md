# INSTALL — Research-Code-Docs v0.1.0-alpha.1 (internal preview)

> **Posture:** manual-only · non-destructive · workspace-local. Installing this preview means
> placing an **isolated copy** of the skill workspace where Claude Code can find it. Nothing is
> installed to your user-global loader by default, nothing auto-triggers, and no source document
> is ever moved, deleted, or overwritten by the skills.

Read [QUICKSTART.md](QUICKSTART.md) after installing for your first safe run.

---

## 1. Supported platforms

| Platform | Status | Note |
|---|---|---|
| Windows 11 + Claude Code | **supported (tested)** | primary development + smoke-test platform |
| WSL2 | support-candidate | verify path behavior; run a smoke test |
| Linux | support-candidate | expected to work; not yet smoke-tested |
| macOS | experimental | unverified |

Full matrix + the meaning of *supported / tested / experimental / unsupported*:
[SUPPORTED_ENVIRONMENTS.md](SUPPORTED_ENVIRONMENTS.md).

## 2. Python version

- **Recommended: Python 3.11.** Support-candidate: **3.12** (the development venv is 3.12).
- Minimum: **3.10** (`pyproject.toml → requires-python = ">=3.10"`).
- Python is needed only to run the **deterministic checkers** (front-matter, interface, flow-state,
  migration/rewrite/maintenance). The skills themselves are Markdown instructions executed by Claude.

## 3. Claude Code / Skills directory requirement

- The skills live under **`.agents/skills/`** inside the workspace — a platform-neutral layout that
  matches the DSH `.agents/skills` convention. An agent platform that reads `.agents/skills` (e.g. DSH),
  when opened with the **workspace directory as the project root**, discovers all 14 skills there.
- **Claude Code note:** Claude Code natively reads `<project>/.claude/skills/`, not `.agents/skills/`.
  Install with `--skills-dir .claude/skills` (see §6) so a Claude Code project sees the skills.
- Every skill ships with `disable-model-invocation: true` — it will **only** run when you invoke it
  **manually** (`/<skill-name>` or by explicit request). None auto-trigger.
- The skills reference their checkers and templates by **workspace-relative path**
  (`evals/skills/harness/checkers/…`, `references/interfaces|templates/…`). This is why the install
  copies the whole runtime set, not just the skills directory — see §7.

## 4. Required dependencies

- **Python ≥ 3.10** and **PyYAML ≥ 6.0** (the only runtime dependency; from `pyproject.toml`).
- **[uv](https://docs.astral.sh/uv/)** recommended to create the environment (or plain `venv` + `pip`).

## 5. Optional dependencies

- **Git** — recommended. Enables the source-hash / rollback guarantees the checkers and smoke test
  rely on. Without Git you can still run, with weaker rollback assurance (see SUPPORTED_ENVIRONMENTS).
- **Claude Code** desktop/CLI/IDE — to actually invoke the skills. (This repo is the skill *content*;
  Claude Code is the runtime that reads it.)

## 6. Install commands

### Option 1 — clone (simplest; the clone *is* the workspace)

```bash
git clone https://github.com/ArmourPiercer1/research-code-docs.git
cd research-code-docs
uv venv                 # creates .venv (Python from your uv toolchain)
uv pip install pyyaml   # the single runtime dep (or: uv sync)
python scripts/preflight.py     # expect PASS (or accepted WARN)
```

### Option 2 — install the runtime set into a separate isolated workspace

Use this when you want the corpus you are refactoring to live in a clean directory that contains
*only* the release runtime set. From a clone (the source), run the bundled installer:

```bash
# read-only w.r.t. the source; writes only into <target>; refuses to clobber existing skills
python scripts/install_workspace.py --target /path/to/isolated-workspace
python scripts/install_workspace.py --target /path/to/isolated-workspace --dry-run   # preview first
python scripts/install_workspace.py --list                                            # show the set
# Claude Code target (its discovery dir is .claude/skills, not .agents/skills):
python scripts/install_workspace.py --target /path/to/isolated-workspace --skills-dir .claude/skills
```

Then in the target:

```bash
cd /path/to/isolated-workspace
uv venv && uv pip install pyyaml
python scripts/preflight.py
```

PowerShell (Windows) is identical except for path separators; the installer is cross-platform Python.

### Install modes (per §2.2 of the release plan)

- **Mode A — workspace-local (RECOMMENDED, default for Alpha).** The isolated directory above *is*
  your agent project root; `.agents/skills/` sits inside it (default). This is the tested path.
  For a Claude Code project, add `--skills-dir .claude/skills` so the skills land in Claude Code's
  discovery directory.
- **Mode B — user-level (`~/.claude/skills/`) — NOT the default.** Only with an explicit understanding
  of the risk: a user-global copy would make these skills visible to *every* project, and the skills'
  workspace-relative checker/template paths will not resolve outside a workspace that also contains
  `evals/…` and `references/…`. Alpha does **not** recommend or script this.

### Install principles (enforced by the installer)

```text
copy into an isolated workspace skill directory
never overwrite an existing skill without --force (explicit confirmation)
never modify installed third-party skills
never write to a user-global / live loader by default
```

## 7. Target directories (what gets placed where)

Installed into `<workspace>/` (layout preserved so the skills resolve their paths):

```text
.agents/skills/<14 skills>/                 the skills (manual-only; .claude/skills/ with --skills-dir)
evals/skills/harness/checkers/*.py          the deterministic checkers
evals/skills/harness/{canonical-source-map,hard-fail,rubric}.md   harness reference docs the skills load
references/interfaces/*.schema.md + README.md   the frozen handoff interfaces
references/templates/*.template.md          the output templates
references/documentation-methodology/upstream-method-matrix.md    provenance
VERSION · release-manifest.yaml · pyproject.toml
scripts/{preflight,smoke_test,install_workspace}.py
LICENSE · NOTICE · THIRD_PARTY_LICENSES.md · *.md docs
```

Your **corpus** (the docs you want refactored) is separate — copy it under the workspace (e.g.
`corpus/`) or point the flow at it. The skills only *read* it.

## 8. Conflict check

Before/at install, confirm:

- No **same-named skill** already exists in the target skills directory (default `.agents/skills/`)
  (the installer skips and warns; `--force` overwrites — only after you confirm it is not user-modified).
- No **different-version** copy is present (compare against [`VERSION`](VERSION) /
  [`release-manifest.yaml`](release-manifest.yaml)).
- You are **not** overwriting user-modified skills.
- No unresolved conflict with an installed `research`/literature skill (the new research adapters
  ship `disable-model-invocation: true` and never auto-fire, so co-existence is safe; see
  [SUPPORT_MATRIX.md](SUPPORT_MATRIX.md)).

`scripts/preflight.py` reports all of the above (§9).

## 9. Post-install preflight (required)

```bash
python scripts/preflight.py            # human-readable + YAML summary
echo $?                                # 0 = PASS · 1 = WARN · 2 = FAIL   (Windows: $LASTEXITCODE)
```

Preflight is **read-only**. It verifies the environment, that every manifest skill is present with the
expected version, that all skills are `disable-model-invocation: true` with no `auto_trigger: true`, that
the six named checkers import and run, classifies L3 dependencies, and flags name/version conflicts.
**Do not proceed on a FAIL.** A WARN must be read and accepted, not treated as success.

## 10. Rollback / uninstall

Because Mode A is a self-contained directory, rollback is simply removing that directory (and the venv).
Full, safe procedure — including how to keep your corpus and candidate outputs — is in
[UNINSTALL.md](UNINSTALL.md). If you installed via `git clone`, `git checkout .` / deleting the clone
restores the pre-install state; the skills never modified anything outside the workspace.
