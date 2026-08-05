#!/usr/bin/env python3
"""
flow_state_check.py — Batch-3 control-flow `flow-state` contract (references/interfaces/flow-state.schema.md).

Validates the orchestrator status output emitted by the three L1 control flows. The load-bearing rule is
HONEST BLOCKED: a `flow_status: BLOCKED` MUST name a non-empty `blocked_by` (an un-built capability that is
named, not hidden as a silent stop). Opt-in: a file is only checked if it carries a fenced ```yaml block that
contains `flow_status:` (so it is safe to run over a directory).

Contract mirrors the other checkers: check_file(path) -> (ok: bool, problems: list[str]).
Registered in run_checks.py as ADVISORY; run the Batch-3 skeletons with --advisory-is-hard to enforce it.

Usage: python flow_state_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

FLOW_STATUS = {"RUNNING", "BLOCKED", "COMPLETE"}
REQUIRED = [
    "flow_name", "flow_version", "flow_status", "current_stage", "completed_artifacts",
    "open_decisions", "blocked_by", "next_skill", "next_input", "quality_advisory", "source_commit",
]
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME)\b|\bxxx\b", re.IGNORECASE)


def _is_placeholder(val: str) -> bool:
    """Bare stub only: the whole value is a single <...> token, or it carries TODO/TBD/FIXME/xxx. A value that
    merely contains an angle-bracket path pattern is not a placeholder."""
    v = val.strip()
    if re.fullmatch(r"<[^>]*>", v):
        return True
    if v in ("...", "-", "--"):
        return True
    return bool(PLACEHOLDER.search(v))

_EMPTYISH = {"", "none", "n/a", "na", "null", "-", "[]"}


def find_flow_block(text: str) -> str | None:
    """Return the contents of the first fenced ```yaml (or bare ```) block that contains 'flow_status:'."""
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL):
        body = m.group(1)
        if re.search(r"(?im)^\s*flow_status\s*:", body):
            return body
    return None


def _field(block: str, key: str) -> tuple[bool, str]:
    """(present, inline_value). present if key has a non-empty inline value OR a following list/block."""
    m = re.search(rf"(?im)^\s*{re.escape(key)}\s*:(.*)$", block)
    if not m:
        return False, ""
    inline = m.group(1).strip()
    if inline and inline not in ("|", ">", "|-", ">-"):
        return True, inline
    tail = block[m.end():]
    nxt = tail.lstrip("\n").splitlines()
    if nxt and (nxt[0].startswith(("  ", "\t", "- ")) or nxt[0].strip().startswith("- ")):
        return True, ""  # present as a list/block
    return False, ""


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        return v[1:-1].strip()
    return v


def check_file(path: Path) -> tuple[bool, list[str]]:
    if path.name.endswith(".template.md") or path.name.endswith(".schema.md"):
        return True, []  # templates/schemas carry placeholder/example blocks by design
    text = path.read_text(encoding="utf-8", errors="replace")
    block = find_flow_block(text)
    if block is None:
        return True, []  # opt-in: not a flow-state artifact

    problems: list[str] = []
    values: dict[str, str] = {}
    for key in REQUIRED:
        present, val = _field(block, key)
        if not present:
            problems.append(f"missing/empty flow-state field: {key}")
            continue
        if val and _is_placeholder(val):
            problems.append(f"{key} still holds a placeholder value: {val!r}")
        values[key] = _strip_quotes(val)

    status = values.get("flow_status", "").upper()
    if status and status not in FLOW_STATUS:
        problems.append(f"flow_status not in {{RUNNING,BLOCKED,COMPLETE}}: {values.get('flow_status')!r}")

    # THE load-bearing rule: BLOCKED must name a real blocked_by.
    if status == "BLOCKED":
        bb = values.get("blocked_by", "")
        if not bb or bb.strip().lower() in _EMPTYISH:
            problems.append("flow_status=BLOCKED but blocked_by is empty/none — a BLOCKED flow MUST name the "
                            "missing capability (honest stop, not a hidden gap)")
    # COMPLETE should not still be pointing at an un-built blocker
    if status == "COMPLETE":
        bb = values.get("blocked_by", "")
        if bb and bb.strip().lower() not in _EMPTYISH:
            problems.append(f"flow_status=COMPLETE but blocked_by is set ({bb!r}) — contradictory")

    # next_skill must be a real value (a terminal flow says so explicitly)
    ns = values.get("next_skill", "")
    if ns and ns.strip().lower() in {"", "none"}:
        problems.append("next_skill is bare 'none'; say 'none (terminal)' or name the next skill/human step")

    seen: set[str] = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: flow_state_check.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        block = find_flow_block(p.read_text(encoding="utf-8", errors="replace"))
        tag = "SKIP" if (block is None and not problems) else ("PASS" if ok else "FAIL")
        print(f"[{tag}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
