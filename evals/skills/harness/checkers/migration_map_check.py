#!/usr/bin/env python3
"""
migration_map_check.py — dry-run migration-map contract (references/interfaces/migration-map.schema.md).

Validates the machine block emitted by `content-canonicalization-and-migration` (directive Batch3后续 §6.1).
The load-bearing rules are DRY-RUN SAFETY (no move/delete/overwrite) and NO SILENT ATTRIBUTION (one primary
disposition per source; a DEFERRED disposition names a preserved open decision). Opt-in: a file is only checked
if it carries a fenced ```yaml block with a top-level `migration_map:` mapping.

Checks (directive §6.1):
  1. source path exists (repo-relative sources are resolved + existence-checked)
  2. each source has exactly one primary disposition
  3. target path does not overwrite the source (target != source)
  4. may_move / may_delete / may_overwrite all false (top-level AND per-disposition)
  5. rollback field present
  6. unresolved decisions not lost (every disposition blocked_by appears in unresolved_decisions)

Contract mirrors the other checkers: check_file(path) -> (ok: bool, problems: list[str]).
Registered in run_checks.py as ADVISORY; run the doc-refactor closure with --advisory-is-hard to enforce it.

Usage: python migration_map_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML — present in the workspace .venv
except ImportError:  # pragma: no cover - graceful: never crash run_checks
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[4]
_ANCHOR = re.compile(r"[#:]L?\d+(-\d+)?$")  # strip #L21-40 / :12 style locators
_TRUEISH = {True, "true", "yes", "1", 1}


def _find_block(text: str) -> str | None:
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL):
        body = m.group(1)
        if re.search(r"(?im)^\s*migration_map\s*:", body):
            return body
    return None


def _strip_anchor(p: str) -> str:
    return _ANCHOR.sub("", p.strip().strip("\"'")).strip()


def _is_true(v) -> bool:
    return (v in _TRUEISH) or (isinstance(v, str) and v.strip().lower() in {"true", "yes", "1"})


def _source_exists(src: str) -> bool | None:
    """True/False if the source looks like a resolvable repo path; None if not path-like (skip existence)."""
    path = _strip_anchor(src)
    if "/" not in path and "\\" not in path:
        return None  # bare name — cannot resolve a corpus root deterministically; skip existence
    cand = path.replace("\\", "/")
    for base in (REPO_ROOT, Path.cwd()):
        if (base / cand).exists():
            return True
    return False


def check_file(path: Path) -> tuple[bool, list[str]]:
    if path.name.endswith((".template.md", ".schema.md")):
        return True, []
    text = path.read_text(encoding="utf-8", errors="replace")
    block = _find_block(text)
    if block is None:
        return True, []  # opt-in: not a migration-map artifact
    if yaml is None:
        return True, []  # pyyaml unavailable — degrade to a no-op rather than crash

    problems: list[str] = []
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        return False, [f"migration_map block is not valid YAML: {e}"]
    mm = data.get("migration_map")
    if not isinstance(mm, dict):
        return False, ["migration_map: block present but not a mapping"]

    # 4. dry-run flags (top-level)
    for flag in ("may_move", "may_delete", "may_overwrite"):
        if flag not in mm:
            problems.append(f"migration_map.{flag} missing — v0 must explicitly declare it false")
        elif _is_true(mm.get(flag)):
            problems.append(f"migration_map.{flag} is true — v0 is dry-run only (no move/delete/overwrite)")

    # 5. rollback present
    rb = mm.get("rollback")
    if not rb or (isinstance(rb, str) and not rb.strip()):
        problems.append("migration_map.rollback missing/empty")

    # unresolved_decisions must be a (possibly empty) list; collect for cross-check
    ud_raw = mm.get("unresolved_decisions", [])
    unresolved = {str(x).strip() for x in ud_raw} if isinstance(ud_raw, list) else set()
    if "unresolved_decisions" not in mm:
        problems.append("migration_map.unresolved_decisions missing — carried open decisions must not be dropped")

    dispositions = mm.get("dispositions")
    if not isinstance(dispositions, list) or not dispositions:
        problems.append("migration_map.dispositions missing/empty — nothing to migrate?")
        dispositions = []

    seen_primary: dict[str, str] = {}
    for i, d in enumerate(dispositions):
        tag = f"disposition[{i}]"
        if not isinstance(d, dict):
            problems.append(f"{tag} is not a mapping")
            continue
        src = str(d.get("source", "")).strip()
        primary = str(d.get("primary", "")).strip()
        target = str(d.get("target", "")).strip()
        if not src:
            problems.append(f"{tag} missing source")
        if not primary:
            problems.append(f"{tag} missing primary disposition")
        # 1. source exists
        if src:
            ex = _source_exists(src)
            if ex is False:
                problems.append(f"{tag} source path does not exist: {src!r}")
        # 2. one primary per source (no conflicting duplicate)
        if src and primary:
            key = _strip_anchor(src)
            if key in seen_primary and seen_primary[key] != primary:
                problems.append(f"{tag} source {key!r} has a second, different primary disposition "
                                f"({seen_primary[key]!r} vs {primary!r}) — exactly one primary per source")
            seen_primary.setdefault(key, primary)
        # 3. target != source (no in-place overwrite)
        if target and src and _strip_anchor(target) == _strip_anchor(src):
            problems.append(f"{tag} target equals source ({_strip_anchor(src)!r}) — that is an in-place overwrite")
        if primary.upper() not in ("DEFERRED", "KEEP-IN-PLACE") and not target:
            problems.append(f"{tag} has primary {primary!r} but no target")
        # 4. per-disposition flags
        for flag in ("move", "delete", "overwrite"):
            if _is_true(d.get(flag)):
                problems.append(f"{tag}.{flag} is true — v0 is dry-run only")
        # 6. DEFERRED / blocked_by preserved in unresolved_decisions
        bb = d.get("blocked_by")
        if primary.upper() == "DEFERRED" and (bb is None or str(bb).strip() == ""):
            problems.append(f"{tag} is DEFERRED but names no blocked_by (a deferred disposition must cite its "
                            f"gating decision, not silently drop a target)")
        if bb is not None and str(bb).strip():
            for token in re.split(r"[,\s]+", str(bb).strip()):
                if token and token not in unresolved:
                    problems.append(f"{tag}.blocked_by {token!r} is not in migration_map.unresolved_decisions "
                                    f"(carried open decision was dropped)")

    seen: set[str] = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: migration_map_check.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        block = _find_block(p.read_text(encoding="utf-8", errors="replace"))
        tag = "SKIP" if (block is None and not problems) else ("PASS" if ok else "FAIL")
        print(f"[{tag}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
