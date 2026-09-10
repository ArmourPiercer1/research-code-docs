#!/usr/bin/env python3
"""canonical_impact_lint.py — Phase-2 (R2; revised slice §5): change-impact discharge.

Replaces timestamp-as-correctness: a change must DECLARE its impact on canonical
owners (File-3 rows) and discharge it IN THE SAME change.

Impact declaration (YAML):
    change: <id>
    changed_paths:            # every path this change touches (repo-relative)
      - docs/skill-development/README.md
    canonical_owners:         # every File-3 canonical owner this change could affect
      - path: docs/skill-development/README.md
        impact: updated       # updated | no_impact
        justification: ""     # REQUIRED (non-empty) when impact == no_impact

Checks:
  C1: every ACTUAL changed path is declared in changed_paths (no undeclared change).
  C2: every owner with impact == updated is actually updated in this change.
  C3: every owner with impact == no_impact carries a non-empty justification.
  C4: a timestamp-only change (only last_verified/last_evaluated/last_updated/date
      lines differ) does NOT count as an impact discharge — an owner declared
      'updated' whose diff is timestamp-only fails.
  C5: a non-trivial change (more than 3 changed paths, or any owner declared
      'updated') without an impact declaration file fails.

Usage:
    python canonical_impact_lint.py --impact <impact.yaml> --base <git-ref>
    python canonical_impact_lint.py --impact <impact.yaml> --base <git-ref> --worktree
        # --worktree: diff the WORKING TREE against base (pre-commit verification)
        # default: diff base..HEAD
    python canonical_impact_lint.py --base <git-ref> [--worktree]   # C5 only (no impact file)
Exit code 0 if all pass, 1 otherwise, 2 on usage/environment error.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TIMESTAMP_ONLY = re.compile(r"^\s*(last_verified|last_evaluated|last_updated)\s*:|\bdate\s*:\s*\d{4}")


def _git(*args: str, root: Path = ROOT) -> str:
    out = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def changed_paths(base: str, worktree: bool, root: Path = ROOT) -> list[str]:
    if worktree:
        # staged + unstaged + untracked (untracked = added paths)
        diff = _git("diff", "--name-only", base, root=root)
        staged = _git("diff", "--name-only", "--cached", base, root=root)
        untracked = _git("ls-files", "--others", "--exclude-standard", root=root)
        paths = set()
        for block in (diff, staged, untracked):
            paths.update(l.strip() for l in block.splitlines() if l.strip())
        return sorted(paths)
    return sorted(l.strip() for l in _git("diff", "--name-only", f"{base}..HEAD", root=root).splitlines()
                  if l.strip())


def diff_for(path: str, base: str, worktree: bool, root: Path = ROOT) -> str:
    if worktree:
        return _git("diff", base, "--", path, root=root) + _git("diff", "--cached", base, "--", path, root=root)
    return _git("diff", f"{base}..HEAD", "--", path, root=root)


def _load_impact(impact: Path) -> dict:
    import yaml
    data = yaml.safe_load(impact.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"impact declaration {impact} is not a YAML mapping")
    return data


def is_timestamp_only(diff: str) -> bool:
    changed = [l for l in diff.splitlines()
               if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
    if not changed:
        return True
    return all(TIMESTAMP_ONLY.search(l[1:]) for l in changed)


def check(impact_path: Path | None, base: str, worktree: bool, root: Path = ROOT) -> tuple[bool, list[str]]:
    problems: list[str] = []
    actual = changed_paths(base, worktree, root)

    impact = None
    if impact_path is not None:
        impact = _load_impact(impact_path)
    declared = {p.strip() for p in (impact or {}).get("changed_paths") or []}
    owners = (impact or {}).get("canonical_owners") or []

    # C5: non-trivial change without a declaration
    if impact is None:
        if len(actual) > 3:
            problems.append(f"canonical-impact-lint C5: non-trivial change ({len(actual)} changed paths) "
                            f"has no impact declaration (--impact <file>)")
        return (len(problems) == 0), problems

    # C1: actual ⊆ declared
    for p in actual:
        if p not in declared:
            problems.append(f"canonical-impact-lint C1: changed path not declared in impact contract: {p}")

    updated_declared = [o for o in owners if isinstance(o, dict) and str(o.get("impact")) == "updated"]
    if not updated_declared and not owners and len(actual) > 3:
        problems.append("canonical-impact-lint C5: non-trivial change declares no canonical owners at all")

    for o in owners:
        if not isinstance(o, dict):
            problems.append(f"canonical-impact-lint: owner entry is not a mapping: {o!r}")
            continue
        op = str(o.get("path", "")).strip()
        kind = str(o.get("impact", "")).strip()
        just = str(o.get("justification") or "").strip()
        if not op:
            problems.append("canonical-impact-lint: owner entry without 'path'")
            continue
        if kind == "no_impact":
            if not just:
                problems.append(f"canonical-impact-lint C3: owner {op} declared no_impact without justification")
        elif kind == "updated":
            if op not in actual:
                problems.append(f"canonical-impact-lint C2: owner {op} declared 'updated' but not "
                                f"changed in this change (same-change rule, R2)")
            else:
                d = diff_for(op, base, worktree, root)
                if is_timestamp_only(d):
                    problems.append(f"canonical-impact-lint C4: owner {op} change is timestamp-only — "
                                    f"does not count as impact discharge")
        else:
            problems.append(f"canonical-impact-lint: owner {op} has unknown impact {kind!r} "
                            f"(updated | no_impact)")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    args = dict()
    base = None
    worktree = False
    i = 1
    while i < len(argv):
        if argv[i] == "--impact":
            i += 1
            args["impact"] = Path(argv[i])
        elif argv[i] == "--base":
            i += 1
            base = argv[i]
        elif argv[i] == "--worktree":
            worktree = True
        else:
            print(f"unknown argument: {argv[i]}", file=sys.stderr)
            return 2
        i += 1
    if base is None:
        print("usage: canonical_impact_lint.py --base <git-ref> [--impact <impact.yaml>] [--worktree]",
              file=sys.stderr)
        return 2
    ok, problems = check(args.get("impact"), base, worktree)
    print(f"canonical_impact_lint (base={base}, worktree={worktree}): {'PASS' if ok else 'FAIL'}")
    for p in problems:
        print(f"    - {p}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
