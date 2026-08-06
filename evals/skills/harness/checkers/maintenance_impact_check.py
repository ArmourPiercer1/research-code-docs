#!/usr/bin/env python3
"""
maintenance_impact_check.py — proposal-only maintenance contract (references/interfaces/maintenance-impact-report.schema.md).

Validates the machine block emitted by `living-design-maintainer` (directive Batch3后续 §6.3). The load-bearing
rules are PROPOSAL-ONLY (no overwrite / no auto-accept / no auto-publish), SINGLE SOURCE OF TRUTH (one canonical
home per info-type; no volatile-into-stable), and CANDIDATE != CANONICAL (an unapproved candidate is never
marked canonical). Opt-in: a file is only checked if it carries a fenced ```yaml block with a top-level
`maintenance_impact:` mapping.

Checks (directive §6.3):
  1. every proposed update points at a known canonical type/home (non-empty; not a candidate/handoff/session)
  2. volatile facts are not proposed into a stable doc (content_kind volatile + target_lifecycle stable)
  3. single source of truth (no info_type mapped to two different canonical homes)
  4. an unapproved candidate is not marked canonical (approved:false + a canonicalizing/publishing action)

Contract mirrors the other checkers: check_file(path) -> (ok: bool, problems: list[str]).
Registered in run_checks.py as ADVISORY; run the doc-refactor closure with --advisory-is-hard to enforce it.

Usage: python maintenance_impact_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

_TRUEISH = {True, "true", "yes", "1", 1}
_FALSEISH = {False, "false", "no", "0", 0, None, "", "none"}
_BAD_CANONICAL = re.compile(r"(?i)candidate-doc-set|/candidate|\bhandoff\b|\bsession\b|\btransient\b")


def _find_block(text: str) -> str | None:
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL):
        body = m.group(1)
        if re.search(r"(?im)^\s*maintenance_impact\s*:", body):
            return body
    return None


def _is_true(v) -> bool:
    return (v in _TRUEISH) or (isinstance(v, str) and v.strip().lower() in {"true", "yes", "1"})


def _is_approved(v) -> bool:
    if isinstance(v, str):
        return v.strip().lower() in {"true", "yes", "1", "approved", "accepted"}
    return v in _TRUEISH


def _action_marks_canonical(action: str) -> bool:
    a = action.strip().lower()
    if a.startswith("propose"):
        return False
    return ("publish" in a) or ("mark-canonical" in a) or ("canonicalize" in a) \
        or ("set-canonical" in a) or ("make-canonical" in a) \
        or (a in {"accept", "mark-accepted", "canonical"})


def check_file(path: Path) -> tuple[bool, list[str]]:
    if path.name.endswith((".template.md", ".schema.md")):
        return True, []
    text = path.read_text(encoding="utf-8", errors="replace")
    block = _find_block(text)
    if block is None:
        return True, []
    if yaml is None:
        return True, []

    problems: list[str] = []
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as e:
        return False, [f"maintenance_impact block is not valid YAML: {e}"]
    mi = data.get("maintenance_impact")
    if not isinstance(mi, dict):
        return False, ["maintenance_impact: block present but not a mapping"]

    # proposal-only flags
    for flag, want_false in (("may_overwrite", True), ("auto_accept_candidates", True), ("auto_publish", True)):
        if flag not in mi:
            problems.append(f"maintenance_impact.{flag} missing — v0 must declare it false")
        elif _is_true(mi.get(flag)):
            problems.append(f"maintenance_impact.{flag} is true — v0 is proposal-only "
                            f"(no overwrite / no auto-accept / no auto-publish)")

    updates = mi.get("proposed_updates")
    if not isinstance(updates, list) or not updates:
        problems.append("maintenance_impact.proposed_updates missing/empty")
        updates = []

    home_by_type: dict[str, set[str]] = {}
    for i, u in enumerate(updates):
        tag = f"proposed_updates[{i}]"
        if not isinstance(u, dict):
            problems.append(f"{tag} is not a mapping")
            continue
        info_type = str(u.get("info_type", "")).strip()
        canonical = str(u.get("canonical", "")).strip()
        tlc = str(u.get("target_lifecycle", "")).strip().lower()
        ck = str(u.get("content_kind", "")).strip().lower()
        action = str(u.get("action", "")).strip()
        approved = u.get("approved")

        if not info_type:
            problems.append(f"{tag} missing info_type")
        # 1. canonical must be a known home, not a candidate/handoff/session
        if not canonical:
            problems.append(f"{tag} missing canonical home")
        elif _BAD_CANONICAL.search(canonical):
            problems.append(f"{tag} canonical points at a candidate/handoff/session, not a canonical home: {canonical!r}")
        # 2. volatile-into-stable
        if ck == "volatile" and tlc == "stable":
            problems.append(f"{tag} proposes volatile content into a stable home (HF-14b boundary violation)")
        # 4. unapproved candidate must not be marked canonical
        if not _is_approved(approved) and _action_marks_canonical(action):
            problems.append(f"{tag} action {action!r} would mark an UNAPPROVED candidate canonical "
                            f"(approved={approved!r}) — v0 proposes acceptance, it does not perform it")
        # collect for single-source-of-truth
        if info_type and canonical:
            home_by_type.setdefault(info_type, set()).add(canonical)

    # 3. single source of truth
    for it, homes in home_by_type.items():
        if len(homes) > 1:
            problems.append(f"info_type {it!r} is proposed into {len(homes)} different canonical homes "
                            f"({sorted(homes)}) — a single source of truth must have exactly one")

    seen: set[str] = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: maintenance_impact_check.py <file.md> [...]", file=sys.stderr)
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
