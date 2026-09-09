# QUICKSTART — Research-Code-Docs v0.1.0-alpha.1

> For a user who knows Claude Code but not this project's internals. Goal: your **first safe run** of the
> supported workflow without reading the governance docs. Installed already? If not, do
> [INSTALL.md](INSTALL.md) first, then run `python scripts/preflight.py` and expect `PASS`.

---

## 1. What problem does this solve?

You have a **messy or mixed-responsibility documentation corpus** (one folder where a vision doc, a status
report, an architecture doc, a roadmap, and stray notes have grown tangled). This system **plans** a clean
restructure and **drafts** the rewritten documents for you to review — **without touching your originals.**

## 2. What is formally supported *right now*?

Exactly one workflow, in a non-destructive scope:

- **`documentation-refactor`** → **dry-run migration plan** + **candidate (draft) rewritten documents** +
  **advisory quality review** + **maintenance-impact proposal**.

Everything else (workspace reconstruction, numerical design) is an **experimental prefix** that will stop
honestly at a not-yet-built capability. See [SUPPORT_MATRIX.md](SUPPORT_MATRIX.md).

## 3. What should your input be?

- A folder of Markdown docs (your **corpus**), ideally under version control (Git).
- Put it inside your workspace, e.g. `corpus/`, or point the run at its path.
- Keep a backup if it is not in Git (the system won't touch it, but backups are cheap insurance).

## 4. How to invoke

The skills live under `.agents/skills/` (platform-neutral; an agent platform that reads `.agents/`
— e.g. DSH — uses the workspace as-is). **Claude Code** reads `<project>/.claude/skills/` instead, so
for a first-time Claude Code run, mirror the directory once after cloning:

```bash
mkdir .claude && cp -r .agents/skills .claude/skills        # bash
# PowerShell: New-Item .claude; Copy-Item .agents/skills .claude/skills -Recurse
# (or install an isolated workspace with: python scripts/install_workspace.py --target <ws> --skills-dir .claude/skills)
```

Then open Claude Code with the **workspace directory as the project root**, and ask (manually — nothing
auto-triggers):

```text
使用 documentation-refactor 分析 corpus/ 目录。
请设计新的文档结构，生成 dry-run migration map 和 candidate documents。
不要移动、删除或覆盖任何原文件。
```

or in English:

```text
Use documentation-refactor on the corpus/ folder. Design the target structure and produce a
dry-run migration map plus candidate documents. Do NOT move, delete, or overwrite any original file.
```

Because every skill ships `disable-model-invocation: true`, you must name it. It will route through
read-only inventory → state → goal/scope → information architecture → migration plan → candidate rewrite →
advisory quality review → maintenance proposal, recording a **flow-state** at the end.

## 5. What files get generated?

Under a run directory (e.g. `results/documentation-refactor/<run-id>/`):

```text
inventory-report.md          project-state-report.md      goal-scope-note.md
document-artifact-map.md      canonical-source-map.md      migration-map.md
candidate-doc-set/            rewrite-provenance-report.md quality-advisory.md
maintenance-impact-report.md  final-flow-state.md
```

All are **new files**. `candidate-doc-set/` holds the drafts.

## 6. Which source files are never changed?

**All of them.** In the supported scope the system performs **zero** move / delete / overwrite. Your
corpus is read-only input; the run records `source_files_changed: 0` and a corpus content hash you can
verify (see §8). If any original changes, that's a defect — report it.

## 7. How to check the output

Run the deterministic checkers over the run directory:

```bash
python evals/skills/harness/checkers/run_checks.py results/documentation-refactor/<run-id> --advisory-is-hard
```

Green HARD gates + interface/flow-state/migration/rewrite/maintenance checkers mean the artifacts are
structurally sound. Then read `final-flow-state.md` and the `## User checklist` below.

## 8. How to handle open decisions

The system **will not decide for you.** Genuine choices (e.g. "which file is the canonical status owner?")
are surfaced as **open decisions** in `open-decisions` / the migration map, left `OPEN`, and the dependent
migration steps are marked **decision-gated / DEFERRED**. You resolve them; then a follow-up run can act on
your resolution. (A no-skill assistant would have silently picked one — this system's restraint is the point.)

## 9. How to request apply-mode (actually moving/rewriting files)

Alpha does **not** implement destructive apply. Moving/rewriting real files is a **separate, explicit
write-approval** that is out of scope for this preview. If you ask the flow to "just overwrite and delete,"
it will **refuse** and return `flow_status: BLOCKED` (see §10). Treat the candidate outputs as a reviewed
draft you place by hand.

## 10. When will the flow say `BLOCKED`?

- You requested a **destructive apply** (move/delete/overwrite/publish) without an explicit, granted
  write-approval → `flow_status: BLOCKED`, `blocked_by: explicit-write-approval-required`.
- An **experimental** flow reached a capability that isn't built yet →
  `flow_status: BLOCKED`, `blocked_by: <named-missing-capability>`.

A named `blocked_by` is the **correct** honest output, not a crash.

## 11. Why isn't a DQE `ALLOW` a publishing approval?

`documentation-quality-evaluator` is an **advisory** reviewer. A high quality band / `ALLOW` says only
"this doc reads as structurally sound within a supported profile." It authorizes **nothing** — no move, no
publish, no promotion — and for unsupported profiles it returns `GATE_DECISION=INCOMPLETE`. Publishing is
always a human decision.

---

## User checklist (§4.3 — verify every run)

```text
[ ] source corpus hash unchanged (git status --porcelain empty; or compare the hash in final-flow-state)
[ ] final-flow-state scope matches what you asked for (dry-run-and-candidate-output)
[ ] open decisions were NOT silently decided (they appear OPEN / DEFERRED)
[ ] candidate docs are NOT marked canonical (they are DRAFT)
[ ] DQE result is explicitly advisory
[ ] maintenance proposals are all approved:false (nothing auto-applied)
```

If all six hold, the run behaved as designed. If any fails, capture it in the feedback record
([release plan §9.1]) and report it. More detail: [SUPPORT_MATRIX.md](SUPPORT_MATRIX.md) ·
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).
