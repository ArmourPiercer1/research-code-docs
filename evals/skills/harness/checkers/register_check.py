#!/usr/bin/env python3
"""
register_check.py — validate a decision-register.md (HF-3 / HF-10 support).

A decision register embeds its entries as a fenced ```yaml list inside a '## Register'
section. Each entry must have:
    id, statement, status (in the vocabulary), evidence (E0..E5), source (non-empty).
This checker also flags any entry whose `status`/`notes` claims "verified" while its
evidence level is E2 or lower (paper/indirect evidence presented as in-project proof).

Usage: python register_check.py <decision-register.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

STATUS = {"FACT", "VERIFIED", "DECIDED", "BASELINE", "HYPOTHESIS",
          "CANDIDATE", "OPEN", "DEFERRED", "REJECTED", "STALE"}
EVIDENCE = {"E0", "E1", "E2", "E3", "E4", "E5"}
LOW_EVIDENCE = {"E0", "E1", "E2"}
DISPOSITION = {"supported", "needs-evidence", "needs-experiment"}
REQUIRED = ("id", "statement", "status", "evidence", "source", "disposition")
NEEDS_REASON_STATUS = {"REJECTED", "DEFERRED", "STALE"}


def extract_entries(text: str):
    """Find the '## Register' section and parse the first fenced yaml block in it."""
    m = re.search(r"^##\s+Register\b(.*?)(?=^\#\#\s|\Z)", text, re.MULTILINE | re.DOTALL)
    region = m.group(1) if m else text
    fence = re.search(r"```ya?ml\s*\n(.*?)```", region, re.DOTALL)
    if not fence:
        return None
    try:
        data = yaml.safe_load(fence.group(1))
    except yaml.YAMLError as e:
        return ("yamlerror", str(e))
    return data


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = extract_entries(text)
    problems: list[str] = []
    if entries is None:
        return False, ["no fenced ```yaml register block found under '## Register'"]
    if isinstance(entries, tuple) and entries[0] == "yamlerror":
        return False, [f"register YAML parse error: {entries[1]}"]
    if not isinstance(entries, list):
        return False, ["register block is not a YAML list of entries"]
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            problems.append(f"entry #{i}: not a mapping")
            continue
        tag = e.get("id", f"#{i}")
        for key in REQUIRED:
            if not str(e.get(key, "")).strip():
                problems.append(f"{tag}: missing/empty '{key}'")
        st = str(e.get("status", "")).strip().upper()
        if st and st not in STATUS:
            problems.append(f"{tag}: illegal status {st!r}")
        ev = str(e.get("evidence", "")).strip().upper()
        if ev and ev not in EVIDENCE:
            problems.append(f"{tag}: illegal evidence {ev!r}")
        # HF-10: an item literally marked VERIFIED/FACT while its in-project evidence is <= E2.
        # (We check the status field only, not freeform notes, to avoid flagging entries whose
        #  note explicitly says e.g. "do not call verified".)
        if st in {"VERIFIED", "FACT"} and ev in LOW_EVIDENCE:
            problems.append(f"{tag}: status {st} at {ev} (only E3+ in-project proof may be VERIFIED/FACT)")
        # disposition legality (v0.2, from research-paper-writing claim-evidence map)
        disp = str(e.get("disposition", "")).strip().lower()
        if disp and disp not in DISPOSITION:
            problems.append(f"{tag}: illegal disposition {disp!r} (want one of {sorted(DISPOSITION)})")
        # a DECIDED/BASELINE commitment must not still be needs-evidence
        if st in {"DECIDED", "BASELINE"} and disp == "needs-evidence":
            problems.append(f"{tag}: {st} item still disposition=needs-evidence (decide on evidence, not before)")
        # reversal/close-out requires a reason (v0.2, ADR supersede-lifecycle)
        has_reason = bool(str(e.get("reason", "")).strip())
        if st in NEEDS_REASON_STATUS and not has_reason:
            problems.append(f"{tag}: status {st} requires a 'reason'")
        if str(e.get("superseded_by", "")).strip() and not has_reason:
            problems.append(f"{tag}: superseded entry requires a 'reason'")
    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: register_check.py <decision-register.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        print(f"[{'PASS' if ok else 'FAIL'}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
