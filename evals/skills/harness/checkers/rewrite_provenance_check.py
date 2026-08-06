#!/usr/bin/env python3
"""
rewrite_provenance_check.py — candidate-output rewrite contract (references/interfaces/rewrite-provenance-report.schema.md).

Validates the machine block emitted by `technical-document-rewriter` (directive Batch3后续 §6.2). The
load-bearing rules are NO OVERWRITE (candidate paths differ from sources; recorded source hashes still match the
files on disk — a real tamper check) and HONEST COMPLETION (never COMPLETE while content is unresolved). Opt-in:
a file is only checked if it carries a fenced ```yaml block with a top-level `rewrite_provenance:` mapping.

Checks (directive §6.2):
  1. candidate path != source path
  2. recorded source sha256 == current file hash (source unchanged — no overwrite)
  3. provenance map complete (every candidate maps to >=1 source range)
  4. unresolved_content non-empty => completion must NOT be COMPLETE
  5. every candidate doc that exists carries traceability front-matter

Contract mirrors the other checkers: check_file(path) -> (ok: bool, problems: list[str]).
Registered in run_checks.py as ADVISORY; run the doc-refactor closure with --advisory-is-hard to enforce it.

Usage: python rewrite_provenance_check.py <file.md> [...]
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[4]
_ANCHOR = re.compile(r"[#:]L?\d+(-\d+)?$")
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
_TRUEISH = {True, "true", "yes", "1", 1}
_TRACE_PRODUCER = re.compile(r"(?im)^\s*(generated_by_skill|produced_by_skill)\s*:\s*\S")
_TRACE_SOURCE = re.compile(r"(?im)^\s*(source_documents|source_artifacts)\s*:")


def _find_block(text: str) -> str | None:
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL):
        body = m.group(1)
        if re.search(r"(?im)^\s*rewrite_provenance\s*:", body):
            return body
    return None


def _norm(p: str) -> str:
    return _ANCHOR.sub("", str(p).strip().strip("\"'")).replace("\\", "/").strip()


def _is_true(v) -> bool:
    return (v in _TRUEISH) or (isinstance(v, str) and v.strip().lower() in {"true", "yes", "1"})


def _resolve(rel: str) -> Path | None:
    rel = _norm(rel)
    if not rel:
        return None
    for base in (REPO_ROOT, Path.cwd()):
        cand = base / rel
        if cand.exists():
            return cand
    return None


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
        return False, [f"rewrite_provenance block is not valid YAML: {e}"]
    rp = data.get("rewrite_provenance")
    if not isinstance(rp, dict):
        return False, ["rewrite_provenance: block present but not a mapping"]

    # v0 flags
    if "may_overwrite" not in rp:
        problems.append("rewrite_provenance.may_overwrite missing — v0 must declare it false")
    elif _is_true(rp.get("may_overwrite")):
        problems.append("rewrite_provenance.may_overwrite is true — v0 writes candidate output only")
    for flag in ("may_move", "may_delete"):
        if _is_true(rp.get(flag)):
            problems.append(f"rewrite_provenance.{flag} is true — v0 writes candidate output only")

    sources = rp.get("sources") or []
    source_paths = {_norm(s.get("path", "")) for s in sources if isinstance(s, dict)}

    # 2. source hashes unchanged
    for s in sources:
        if not isinstance(s, dict):
            continue
        sp = s.get("path", "")
        h = str(s.get("sha256", "")).strip()
        if not _HEX64.match(h):
            continue  # only compare when a real hash was recorded
        f = _resolve(sp)
        if f is None:
            problems.append(f"source not found to verify hash: {sp!r}")
            continue
        actual = hashlib.sha256(f.read_bytes()).hexdigest()
        if actual.lower() != h.lower():
            problems.append(f"source hash changed since rewrite (possible overwrite): {sp!r}")

    # 3 + 1. provenance completeness + candidate != source
    prov = rp.get("provenance")
    if not isinstance(prov, list) or not prov:
        problems.append("rewrite_provenance.provenance missing/empty — no candidate is traced to a source")
        prov = []
    for i, e in enumerate(prov):
        tag = f"provenance[{i}]"
        if not isinstance(e, dict):
            problems.append(f"{tag} is not a mapping")
            continue
        cand = _norm(e.get("candidate", ""))
        froms = e.get("from_sources") or []
        if not cand:
            problems.append(f"{tag} missing candidate")
        if not isinstance(froms, list) or not any(str(x).strip() for x in froms):
            problems.append(f"{tag} has no from_sources — every candidate must trace to >=1 source range")
        # candidate must not equal any source path
        if cand and (cand in source_paths or cand in {_norm(x) for x in froms}):
            problems.append(f"{tag} candidate path equals a source path ({cand!r}) — that is an overwrite")
        # 5. candidate file (if present) carries traceability front-matter
        if cand:
            cf = _resolve(cand)
            if cf is not None and cf.suffix.lower() == ".md":
                head = "\n".join(cf.read_text(encoding="utf-8", errors="replace").splitlines()[:90])
                if not _TRACE_PRODUCER.search(head) or not _TRACE_SOURCE.search(head):
                    problems.append(f"{tag} candidate {cand!r} lacks traceability front-matter "
                                    f"(generated_by_skill + source_documents)")

    # 4. completion vs unresolved
    completion = str(rp.get("completion", "")).strip().upper()
    unresolved = rp.get("unresolved_content") or []
    n_unresolved = len([x for x in unresolved if str(x).strip()]) if isinstance(unresolved, list) else 0
    if completion == "COMPLETE" and n_unresolved > 0:
        problems.append(f"completion=COMPLETE but unresolved_content has {n_unresolved} item(s) — "
                        f"cannot claim COMPLETE while content is unresolved")
    if not completion:
        problems.append("rewrite_provenance.completion missing (PARTIAL | COMPLETE)")

    seen: set[str] = set()
    uniq = [p for p in problems if not (p in seen or seen.add(p))]
    return (len(uniq) == 0), uniq


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: rewrite_provenance_check.py <file.md> [...]", file=sys.stderr)
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
