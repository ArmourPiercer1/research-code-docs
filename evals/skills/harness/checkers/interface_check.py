#!/usr/bin/env python3
"""
interface_check.py — Batch-2.5 frozen handoff-interface contract (references/interfaces/README.md).

Validates that an inter-skill handoff artifact carries the frozen header (directive §5): the 12 fields,
legal status/evidence tokens, a real (non-chat) source, an explicit downstream requirement, and no silently
dropped open questions. It is **opt-in**: a file is only checked if its front-matter declares `artifact_type:`
(so it is safe to run over a whole directory — governance docs, schemas, and templates are skipped).

Aliases (so this does NOT require changing the HARD frontmatter_check):
    produced_by_skill  <-  generated_by_skill
    source_artifacts   <-  source_documents

Contract mirrors the other checkers: check_file(path) -> (ok: bool, problems: list[str]).
Registered in run_checks.py as ADVISORY; run the Batch-2.5 chains with --advisory-is-hard to enforce it.

Usage: python interface_check.py <file.md> [...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ARTIFACT_TYPES = {
    "inventory-report", "project-state-report", "goal-scope-note", "document-artifact-map",
    "literature-search-plan", "research-evidence-map", "decision-register",
    # Batch-5 additive extension (directive Batch3后续 §6): new downstream handoff types the doc-refactor
    # executor tail produces. Additive — re-means none of the seven above; see references/interfaces/README.md.
    "migration-map", "rewrite-provenance-report", "maintenance-impact-report",
}
# Known artifact types that are NOT frozen inter-skill handoffs (§5.2). They legitimately declare an
# artifact_type but are terminal/advisory outputs, so the frozen 12-field handoff payload does not apply —
# skip them. An artifact_type that is neither frozen nor here is treated as a likely typo of a frozen name
# and still validated (so it fails loudly), which is the point of the opt-in.
KNOWN_NON_FROZEN = {"quality-report", "quality-advisory"}
DOC_LIFECYCLE = {"DRAFT", "IN_REVIEW", "ACCEPTED", "DEPRECATED"}
EVIDENCE = {"E0", "E1", "E2", "E3", "E4", "E5"}

# canonical interface field -> accepted aliases (first found wins)
REQUIRED = {
    "artifact_type": ("artifact_type",),
    "document_lifecycle": ("document_lifecycle",),
    "produced_by_skill": ("produced_by_skill", "generated_by_skill"),
    "skill_version": ("skill_version", "version"),
    "source_artifacts": ("source_artifacts", "source_documents", "source_document"),
    "scope": ("scope",),
    "facts": ("facts",),
    "hypotheses": ("hypotheses",),
    "open_questions": ("open_questions",),
    "evidence_level": ("evidence_level",),
    "next_handoff": ("next_handoff",),
    "handoff_requirements": ("handoff_requirements",),
}

PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME)\b|\bxxx\b", re.IGNORECASE)


def _is_placeholder(val: str) -> bool:
    """A value is a placeholder only if it is a BARE stub — the whole value is a single <...> token, or it
    carries an explicit TODO/TBD/FIXME/xxx. A real value that merely *contains* an angle-bracket path pattern
    (e.g. `.claude/skills/<skill>/SKILL.md`) is NOT a placeholder."""
    v = val.strip()
    if re.fullmatch(r"<[^>]*>", v):
        return True
    if v in ("...", "-", "--"):
        return True
    return bool(PLACEHOLDER.search(v))

_EVIDENCELIKE = re.compile(r"\bE([0-9]{1,2})\b")


def extract_frontmatter(text: str) -> str | None:
    """Same region logic as frontmatter_check: a YAML '---' header and/or a leading HTML comment."""
    regions: list[str] = []
    stripped = text.lstrip()
    if stripped.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", stripped, re.DOTALL)
        if m:
            regions.append(m.group(1))
    head = "\n".join(text.splitlines()[:90])
    m = re.search(r"<!--(.*?)-->", head, re.DOTALL)
    if m:
        regions.append(m.group(1))
    return "\n".join(regions) if regions else None


def field_value(block: str, aliases: tuple[str, ...]) -> tuple[bool, str]:
    """Return (present, inline_value). present=True if any alias has a non-empty inline value OR a
    following-line list/block. inline_value is the scalar on the same line (\"\" for a list/block)."""
    for alias in aliases:
        pat = re.compile(rf"^\s*{re.escape(alias)}\s*:(.*)$", re.MULTILINE)
        for m in pat.finditer(block):
            inline = m.group(1).strip()
            if inline and inline not in ("|", ">", "|-", ">-"):
                return True, inline
            tail = block[m.end():]
            nxt = tail.lstrip("\n").splitlines()
            if nxt and (nxt[0].startswith(("  ", "\t", "- ")) or nxt[0].strip().startswith("- ")):
                return True, ""  # present as a list/block scalar
    return False, ""


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        return v[1:-1].strip()
    return v


def _body_has_open_items(text: str) -> bool:
    """Conservative: is there a section whose heading names open/unknown/gap/contradiction, with >=1 data
    row (markdown table row that is not header/separator) or list item beneath it?"""
    heading = re.compile(r"(?im)^#{1,6}\s+.*(open decision|open question|unknown|unresolved|gap|contradict)")
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if heading.match(ln):
            for body_ln in lines[i + 1:i + 40]:
                if re.match(r"^#{1,6}\s", body_ln):
                    break  # next heading — section ended
                s = body_ln.strip()
                if s.startswith(("- ", "* ")) or re.match(r"^\d+\.\s", s):
                    return True
                if s.count("|") >= 2 and not re.match(r"^\|?\s*:?-{2,}", s) \
                        and "---" not in s and not re.search(r"(?i)\b(id|question|gap|item|claim)\b\s*\|", s):
                    return True
    return False


def check_file(path: Path) -> tuple[bool, list[str]]:
    if path.name.endswith(".template.md"):
        return True, []  # templates carry placeholders by design — not real artifacts
    text = path.read_text(encoding="utf-8", errors="replace")
    block = extract_frontmatter(text)
    if block is None:
        return True, []
    at_present, at_val = field_value(block, REQUIRED["artifact_type"])
    if not at_present:
        return True, []  # opt-in: not a declared handoff artifact
    at_norm = _strip_quotes(at_val).split()[0] if at_val else ""
    if at_norm in KNOWN_NON_FROZEN:
        return True, []  # a declared but non-handoff artifact (e.g. DQE's quality-report) — not frozen

    problems: list[str] = []
    values: dict[str, str] = {}
    for canon, aliases in REQUIRED.items():
        present, val = field_value(block, aliases)
        if not present:
            problems.append(f"missing/empty required interface field: {canon}")
            continue
        if val and _is_placeholder(val):
            problems.append(f"{canon} still holds a placeholder value: {val!r}")
        values[canon] = _strip_quotes(val)

    # -- semantic checks (only when the field was present) --
    at = values.get("artifact_type", "")
    if at and at not in ARTIFACT_TYPES:
        problems.append(f"artifact_type not in the frozen set: {at!r}")

    dl = values.get("document_lifecycle", "")
    if dl and not any(tok in dl.upper() for tok in DOC_LIFECYCLE):
        problems.append(f"document_lifecycle without a legal token (DRAFT|IN_REVIEW|ACCEPTED|DEPRECATED): {dl!r}")

    ev = values.get("evidence_level", "")
    if ev:
        low = ev.lower()
        if not (low.startswith(("n/a", "na")) or any(tok in ev.upper() for tok in EVIDENCE)):
            problems.append(f"evidence_level must be E0..E5 or 'n/a (<why>)': {ev!r}")
        for m in _EVIDENCELIKE.finditer(ev.upper()):
            if ("E" + m.group(1)) not in EVIDENCE:
                problems.append(f"illegal evidence level in evidence_level: E{m.group(1)}")

    # rule 5: missing must be an *explicit* absence, not a bare token
    for f in ("facts", "hypotheses", "evidence_level"):
        v = values.get(f, "")
        if v and v.lower() in {"none", "n/a", "na", "-"}:
            problems.append(f"{f} is a bare '{v}'; declare the reason explicitly, e.g. \"none (<why>)\"")

    # rule 1 + no-chat-dependence: the source must be a real artifact/corpus
    src_present, _ = field_value(block, REQUIRED["source_artifacts"])
    src_line = re.search(r"(?im)^\s*(source_artifacts|source_documents)\s*:(.*)$", block)
    src_text = (src_line.group(2) if src_line else "")
    # include following list lines for the chat/conversation scan
    if src_line:
        tail = block[src_line.end():]
        for ln in tail.lstrip("\n").splitlines():
            if ln.startswith(("  ", "\t", "- ")) or ln.strip().startswith("- "):
                src_text += " " + ln
            elif ln.strip() and not ln[0].isspace():
                break
    if re.search(r"(?i)\b(chat|conversation|this session|the thread)\b", src_text):
        problems.append("source must be a real artifact/corpus, not chat/conversation (no-chat-dependence)")

    # rule 7: open questions never silently drop
    oq = values.get("open_questions", "")
    if oq and re.match(r"(?i)^\s*(none|n/?a|0)\b", oq) and _body_has_open_items(text):
        problems.append("open_questions says 'none/0' but the body has an open/unknown/gap section with rows")

    # de-dup, keep order
    seen: set[str] = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: interface_check.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        skipped = (not problems) and (p.name.endswith(".template.md")
                                      or extract_frontmatter(p.read_text(encoding="utf-8", errors="replace") or "") is None
                                      or not field_value(extract_frontmatter(p.read_text(encoding="utf-8", errors="replace")) or "", ("artifact_type",))[0])
        tag = "SKIP" if skipped else ("PASS" if ok else "FAIL")
        print(f"[{tag}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
