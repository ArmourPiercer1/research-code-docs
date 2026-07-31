#!/usr/bin/env python3
"""
frontmatter_check.py — HF-9: traceability front-matter completeness.

A generated document must carry provenance so any output traces to skill/version/
commit/time/status (quality-control-plan §8). This checker accepts EITHER a YAML
front-matter block delimited by '---' at the very top, OR an HTML-comment block
'<!-- ... -->' near the top (used by the governance docs). It verifies the required
keys are present and non-empty.

Usage:
    python frontmatter_check.py <file.md> [<file2.md> ...]
Exit code 0 if all pass, 1 if any file fails.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

# canonical required key -> accepted aliases (any one satisfies it)
REQUIRED = {
    "generated_by_skill": ("generated_by_skill", "generated_by"),
    "skill_version": ("skill_version", "version"),
    "source_commit": ("source_commit",),
    "source_documents": ("source_documents", "source_document", "source_doc"),
    "status": ("status",),
    "last_verified": ("last_verified", "last_updated"),
}


def extract_frontmatter(text: str) -> str | None:
    """Return the provenance region to search. A file may carry a YAML front-matter block
    (for the loader: name/description/...) AND a leading HTML-comment block holding the
    traceability keys. We concatenate both so provenance in either place is found."""
    regions: list[str] = []
    stripped = text.lstrip()
    # YAML front-matter: --- ... ---
    if stripped.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", stripped, re.DOTALL)
        if m:
            regions.append(m.group(1))
    # HTML-comment block within the first ~80 lines (may sit just after YAML front-matter)
    head = "\n".join(text.splitlines()[:90])
    m = re.search(r"<!--(.*?)-->", head, re.DOTALL)
    if m:
        regions.append(m.group(1))
    if not regions:
        return None
    return "\n".join(regions)


def key_present(block: str, aliases: tuple[str, ...]) -> bool:
    for alias in aliases:
        # match "key:" at line start (indented ok), with a non-empty value on the
        # same line OR a nested/continued value on following lines.
        pat = re.compile(rf"^\s*{re.escape(alias)}\s*:(.*)$", re.MULTILINE)
        for m in pat.finditer(block):
            inline = m.group(1).strip()
            if inline and inline not in ("|", ">", "|-", ">-"):
                return True
            # value may be on following indented lines (list/block scalar)
            tail = block[m.end():]
            nxt = tail.lstrip("\n").splitlines()
            if nxt and (nxt[0].startswith(("  ", "\t", "- ")) or nxt[0].strip().startswith("- ")):
                return True
    return False


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    block = extract_frontmatter(text)
    if block is None:
        return False, ["no front-matter block found (need YAML '---' header or leading HTML comment)"]
    missing = [canon for canon, aliases in REQUIRED.items() if not key_present(block, aliases)]
    return (len(missing) == 0), ([f"missing/empty: {k}" for k in missing])


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: frontmatter_check.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        p = Path(arg)
        ok, problems = check_file(p)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {p}")
        for pr in problems:
            print(f"    - {pr}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
