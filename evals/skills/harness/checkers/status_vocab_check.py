#!/usr/bin/env python3
"""
status_vocab_check.py — HF-3 / HF-10 support: legality of status + evidence tokens.

The system uses a fixed status vocabulary and evidence-level scale
(system-architecture §7). This checker finds status/evidence tokens and flags any
that are not in the allowed sets. It also flags an explicit 'status:' front-matter
field whose value contains NO legal token (a blank/omitted status).

What it looks for:
  * Inline status tags written as a bare UPPERCASE token from the set, or as
    'status: X' / 'Status: X' fields, or bracketed '[HYPOTHESIS]' style tags.
  * Evidence levels written as a standalone E0..E5 token; anything like E6/E7 is illegal.

This is intentionally conservative: it reports *illegal* tokens (a likely HF-3/HF-10),
not every place a status is missing (that is a soft-rubric concern).

Usage: python status_vocab_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

STATUS = {"FACT", "VERIFIED", "DECIDED", "BASELINE", "HYPOTHESIS",
          "CANDIDATE", "OPEN", "DEFERRED", "REJECTED", "STALE"}
EVIDENCE = {"E0", "E1", "E2", "E3", "E4", "E5"}
# Lifecycle statuses (system-architecture §11) are a SEPARATE, legal vocabulary that also
# appears in a 'status:' field (registry entries, SKILL.md provenance). Accept either.
LIFECYCLE = {"experimental", "active", "planned", "deprecated", "replaced",
             "retired", "reference-only", "in-progress"}
# Authored-document lifecycle (ADR-DQE-001 D-14): the doc-level `document_lifecycle:` field.
# This is DISTINCT from the skill/registry LIFECYCLE above and from claim STATUS.
DOC_LIFECYCLE = {"DRAFT", "IN_REVIEW", "ACCEPTED", "DEPRECATED"}

# tokens that look like a status/evidence tag but are NOT in the vocabulary
STATUSLIKE = re.compile(r"\b([A-Z]{4,})\b")
EVIDENCELIKE = re.compile(r"\bE([0-9]{1,2})\b")

# words that are all-caps but legitimately not status tokens — don't flag these
ALLOW_UPPER = {
    "FACT", "TODO", "NOTE", "WARN", "INFO", "PASS", "FAIL", "SKILL", "YAML", "JSON",
    "HTML", "HTTP", "HTTPS", "MIT", "ADR", "ADRS", "PRD", "PRISMA", "OCR", "API",
    "APIS", "CLI", "MCP", "RNG", "GPT", "GDF", "BM25", "SPECTER", "WOS", "README",
    "CONTEXT", "MEMORY", "UNKNOWN", "TRUE", "FALSE", "NULL", "AND", "OR", "NOT",
    "GO", "STOP", "MODIFY", "OQ", "HF", "DENY", "COND", "SEQ", "LIVE",
    "KEEP", "SPLIT", "REPLACE", "REMOVE", "REFERENCE",
}


def strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so schema examples ('status: <one-of...>') aren't validated as real fields."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = strip_code_fences(path.read_text(encoding="utf-8", errors="replace"))
    problems: list[str] = []

    # 1) explicit 'status:' fields whose value carries no legal token (research OR lifecycle)
    for m in re.finditer(r"(?im)^\s*status\s*:\s*(.+)$", text):
        val = m.group(1).strip()
        if not val or val.lower() in {"n/a", "na", "none", "-"}:
            continue
        has_research = any(tok in val.upper() for tok in STATUS)
        has_lifecycle = any(tok in val.lower() for tok in LIFECYCLE)
        if not (has_research or has_lifecycle):
            problems.append(f"status field without a legal token: {val!r}")

    # 1b) explicit 'document_lifecycle:' fields (ADR-DQE-001 D-14) must carry a legal doc-lifecycle token
    for m in re.finditer(r"(?im)^\s*document_lifecycle\s*:\s*(.+)$", text):
        val = m.group(1).strip()
        if not val or val.lower() in {"n/a", "na", "none", "-"}:
            continue
        if not any(tok in val.upper() for tok in DOC_LIFECYCLE):
            problems.append(f"document_lifecycle field without a legal token "
                            f"(DRAFT|IN_REVIEW|ACCEPTED|DEPRECATED): {val!r}")

    # 2) illegal evidence levels (E6+ etc.)
    for m in EVIDENCELIKE.finditer(text):
        tok = "E" + m.group(1)
        if tok not in EVIDENCE:
            problems.append(f"illegal evidence level: {tok}")

    # de-duplicate while preserving order
    seen = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def warnings(path: Path) -> list[str]:
    """Non-blocking v0.4 deprecation notes (do NOT affect pass/fail or exit code). A leading frontmatter
    block that still uses a legacy `status:` for document-level state, without a `document_lifecycle:`
    field, is nudged toward `document_lifecycle` (ADR-DQE-001 D-14)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"\s*<!--(.*?)-->", text, re.S) or re.match(r"\s*---\n(.*?)\n---", text, re.S)
    if not m:
        return []
    fm = m.group(1)
    has_status = re.search(r"(?im)^\s*status\s*:", fm)
    has_lifecycle = re.search(r"(?im)^\s*document_lifecycle\s*:", fm)
    if has_status and not has_lifecycle:
        return ["legacy 'status:' front-matter field is deprecated for document-level state; "
                "prefer 'document_lifecycle:' (ADR-DQE-001 D-14). Non-blocking."]
    return []


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: status_vocab_check.py <file.md> [...]", file=sys.stderr)
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
