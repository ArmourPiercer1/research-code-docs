# UNINSTALL & ROLLBACK — Research-Code-Docs v0.1.0-alpha.1

> The preview is designed to be **trivially removable**. In workspace-local mode (the default) the whole
> installation is one isolated directory plus its `.venv`. Removing it returns you to the pre-install
> state. **The skills never wrote outside the workspace** — no user-global config, no changes to your
> other projects, no edits to your source corpus.

---

## 1. What this system created (and only this)

| Location | Created by | Safe to delete? |
|---|---|---|
| `<workspace>/.agents/skills/<14 skills>/` (or `.claude/skills/` when installed with `--skills-dir`) | install | Yes |
| `<workspace>/evals/`, `references/`, `scripts/`, `VERSION`, `release-manifest.yaml`, `*.md` | install | Yes |
| `<workspace>/.venv/` | `uv venv` | Yes (regenerable) |
| `<workspace>/results/…` **or** `evals/skills/results/<run>/…` | a flow run (candidate outputs) | Yes — **but this is your generated work; keep if wanted** |
| your corpus (e.g. `<workspace>/corpus/…`) | **you** | **Do NOT delete on uninstall** |

The system did **not** create or modify:

- any file under a user-global `~/.claude/` (Mode B was not used),
- any of your other projects or installed third-party skills,
- your original source documents (verify with §4).

## 2. Uninstall — Mode A (workspace-local, default)

**Keep your generated candidate outputs and corpus first** if you want them:

```bash
# optional: move your outputs and corpus somewhere safe before removing the workspace
mv <workspace>/results            ~/keep/rcd-results     2>/dev/null || true
mv <workspace>/corpus             ~/keep/rcd-corpus      2>/dev/null || true
```

Then remove the workspace:

```bash
rm -rf <workspace>          # the entire isolated install, incl. .venv
```

PowerShell:

```powershell
Move-Item <workspace>\results  $HOME\keep\rcd-results  -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force <workspace>
```

That is the complete uninstall. There is nothing else to clean up.

## 3. Uninstall — if you installed via `git clone`

```bash
cd research-code-docs
git status                 # confirm no unexpected tracked changes
# your candidate outputs are untracked; move them out if you want to keep them, then:
cd .. && rm -rf research-code-docs
```

To roll back to a specific release instead of deleting: `git checkout v0.1.0-alpha.1` (once the tag
exists), or `git checkout <release-commit>`.

## 4. Confirm no original document was modified (recommended)

The safety promise of this preview is that your source corpus is byte-for-byte unchanged. Verify it:

```bash
# if your corpus is a git repo:
cd <your-corpus>
git status --porcelain      # expect EMPTY = nothing changed

# content hash of a directory (git repos), compare before/after a run:
git ls-files -s <dir> | git hash-object --stdin
```

A flow's `final-flow-state.md` also records `source_files_changed: 0 / moved: 0 / deleted: 0 /
overwritten: 0` and the corpus hash. If any of those is non-zero for a dry-run/candidate scope, treat it
as a defect and report it (see §9.1 feedback record in the release plan).

## 5. Clean up generated candidate outputs (optional, explicit)

Candidate outputs are **new files only** (never overwrites). Remove them if you no longer want them:

```bash
rm -rf <workspace>/results/<run-id>/candidate-doc-set/
rm -rf <workspace>/results/<run-id>/                 # or the whole run
```

## 6. What uninstall must NOT do

```text
- delete your source corpus
- delete candidate outputs unless you explicitly choose to
- remove any other skill (including installed third-party skills)
- modify global Claude configuration
```

If you ever used **Mode B** (user-level, non-default): remove only the `~/.claude/skills/<14 skills>/`
directories this preview added, and nothing else under `~/.claude/`. Verify each is the preview's copy
(check `VERSION` / the skill's front-matter) before deleting.
