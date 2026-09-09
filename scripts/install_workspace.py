#!/usr/bin/env python3
"""install_workspace.py — copy the Research-Code-Docs release runtime set into an
ISOLATED target workspace, preserving the repo-relative layout the skills depend on.

Why a curated copy (not just `.agents/skills/`): the skills invoke deterministic
checkers under `evals/skills/harness/checkers/`, load harness reference docs
(`canonical-source-map.md`, `hard-fail.md`, `rubric.md`), and read
`references/interfaces|templates`. Those must sit at the SAME relative paths beside
the skills directory for a run to work. The 3 executor checkers resolve the workspace
root from their own location (`parents[4]`), so preserving the layout is sufficient.

Skills directory: the source repo keeps skills under `.agents/skills/` (platform-neutral;
matches the DSH `.agents/skills` convention). The install target uses the same by default;
pass `--skills-dir .claude/skills` when the target project is a Claude Code workspace
(Claude Code discovers `<project>/.claude/skills/`, not `.agents/skills/`).

SAFETY (matches the release posture):
  - READ-ONLY with respect to the SOURCE repo (never writes into --source).
  - Writes ONLY inside the user-chosen --target directory.
  - NEVER installs to a user-global / live Claude Code loader.
  - Refuses to overwrite an existing skill in the target unless --force.
  - Skips __pycache__/*.pyc; never copies .venv, tests/corpus, snapshots, references/ upstreams.

Exit codes:  0 = installed cleanly   1 = installed with skipped conflicts (WARN)   2 = error
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Runtime set (relative to the source repo root). Directories are copied whole
# (minus the ignore patterns); files are copied individually.
# The skills directory is the only path-sensitive entry: the SOURCE layout is
# .agents/skills; the TARGET layout is chosen by --skills-dir (default: same).
SKILLS_SRC = ".agents/skills"
RUNTIME_DIRS = [
    SKILLS_SRC,
    "evals/skills/harness/checkers",
    "references/interfaces",
    "references/templates",
]
RUNTIME_FILES = [
    "evals/skills/harness/canonical-source-map.md",
    "evals/skills/harness/rubric.md",
    "evals/skills/harness/hard-fail.md",
    "references/documentation-methodology/upstream-method-matrix.md",
    "VERSION",
    "release-manifest.yaml",
    "pyproject.toml",
    "scripts/preflight.py",
    "scripts/smoke_test.py",
    "scripts/install_workspace.py",
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_LICENSES.md",
    "INSTALL.md",
    "UNINSTALL.md",
    "QUICKSTART.md",
    "SUPPORTED_ENVIRONMENTS.md",
    "SUPPORT_MATRIX.md",
    "KNOWN_LIMITATIONS.md",
    "CHANGELOG.md",
    "README.md",
]
_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")


def _repo_root() -> Path:
    # scripts/install_workspace.py -> parents[1] == repo root
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Install the release runtime set into an isolated workspace.")
    ap.add_argument("--target", required=True, help="Isolated workspace directory to install INTO (created if absent).")
    ap.add_argument("--source", default=None, help="Source repo root (default: this script's repo).")
    ap.add_argument("--skills-dir", default=SKILLS_SRC,
                    help=f"Where skills are placed in the TARGET (default: {SKILLS_SRC}; "
                         "use .claude/skills for a Claude Code project).")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be copied; write nothing.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing skills/files in the target.")
    ap.add_argument("--list", action="store_true", help="Print the runtime set and exit.")
    args = ap.parse_args(argv)
    skills_dst = args.skills_dir.strip("/").strip("\\").replace("\\", "/")

    if args.list:
        print("Release runtime set:")
        for d in RUNTIME_DIRS:
            print(f"  [dir]  {d}/")
        for f in RUNTIME_FILES:
            print(f"  [file] {f}")
        return 0

    source = Path(args.source).resolve() if args.source else _repo_root()
    target = Path(args.target).resolve()

    if not (source / "release-manifest.yaml").exists():
        print(f"ERROR: --source does not look like a release repo (no release-manifest.yaml): {source}", file=sys.stderr)
        return 2
    if target == source:
        print("ERROR: --target must be an isolated directory, not the source repo itself.", file=sys.stderr)
        return 2

    print(f"source : {source}")
    print(f"target : {target}")
    print(f"mode   : {'DRY-RUN (no writes)' if args.dry_run else ('FORCE overwrite' if args.force else 'safe (skip existing skills)')}")
    print("-" * 70)

    warned = False

    # Directories
    for rel in RUNTIME_DIRS:
        src = source / rel
        if not src.exists():
            print(f"ERROR: missing in source: {rel}", file=sys.stderr)
            return 2
        dst = target / (skills_dst if rel == SKILLS_SRC else rel)
        if rel == SKILLS_SRC:
            # per-skill conflict guard
            for skill in sorted(p for p in src.iterdir() if p.is_dir()):
                sdst = dst / skill.name
                if sdst.exists() and not args.force:
                    print(f"  SKIP (exists): {skills_dst}/{skill.name}  (use --force to overwrite)")
                    warned = True
                    continue
                print(f"  {'would copy' if args.dry_run else 'copy'}: {skills_dst}/{skill.name}/")
                if not args.dry_run:
                    if sdst.exists():
                        shutil.rmtree(sdst)
                    sdst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(skill, sdst, ignore=_IGNORE)
        else:
            print(f"  {'would copy' if args.dry_run else 'copy'}: {rel}/")
            if not args.dry_run:
                if dst.exists() and args.force:
                    shutil.rmtree(dst)
                dst.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, dst, ignore=_IGNORE, dirs_exist_ok=True)

    # Files
    for rel in RUNTIME_FILES:
        src = source / rel
        if not src.exists():
            # scripts/smoke_test.py & docs may not exist yet during bootstrap; warn, don't fail
            print(f"  (absent in source, skipped): {rel}")
            continue
        dst = target / rel
        if dst.exists() and not args.force:
            print(f"  SKIP (exists): {rel}  (use --force to overwrite)")
            warned = True
            continue
        print(f"  {'would copy' if args.dry_run else 'copy'}: {rel}")
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    print("-" * 70)
    if args.dry_run:
        print("DRY-RUN complete — nothing written.")
        return 0
    if warned:
        print("Installed with SKIPPED conflicts (existing files left untouched). Re-run with --force to overwrite.")
        print("Next: create the venv (see INSTALL.md) then run  python scripts/preflight.py  in the target.")
        return 1
    print("Installed. Next: create the venv (see INSTALL.md) then run  python scripts/preflight.py  in the target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
