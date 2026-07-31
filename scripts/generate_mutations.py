#!/usr/bin/env python3
"""
generate_mutations.py — materialize DQE golden-negatives from tests/corpus/mutations/plans/*.yaml.

Each plan applies ONE controlled mutation to a base (a normalized seed or an existing frozen fixture)
and writes, under tests/corpus/cases/golden-negative/<case-id>/:
    document.<ext>        the mutated fixture (the blind input)
    mutation.diff         unified diff base -> mutated
    mutation_result.yaml  machine-readable summary + assertions

Supported ops: remove-sections | append-file | delete-substrings | remove-lines | insert-after.

Assertions (a failed assertion aborts, so a stale/no-op plan can never silently ship):
  - the mutated text DIFFERS from the base;
  - removed headings are gone; the append marker is present; each delete-substring existed;
    remove-lines removed >= 1 line; the insert anchor matched;
  - every heading named in `forbidden_unrelated_changes` is BYTE-IDENTICAL between base and mutated.

Usage:
  python scripts/generate_mutations.py                 # all plans
  python scripts/generate_mutations.py GN-ADR-001      # one case
"""
from __future__ import annotations
import difflib
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLANS = ROOT / "tests" / "corpus" / "mutations" / "plans"
NORMALIZED = ROOT / "tests" / "corpus" / "source-seeds" / "normalized"
OUT = ROOT / "tests" / "corpus" / "cases" / "golden-negative"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def heading_at(line: str):
    m = HEADING.match(line)
    return (len(m.group(1)), m.group(2).strip()) if m else None


def section_span(lines: list[str], title: str):
    """Return (start, end) line indices for the section under heading `title`, or None."""
    for i, ln in enumerate(lines):
        h = heading_at(ln)
        if h and h[1].lower() == title.lower():
            lvl = h[0]
            for j in range(i + 1, len(lines)):
                hj = heading_at(lines[j])
                if hj and hj[0] <= lvl:
                    return (i, j)
            return (i, len(lines))
    return None


def remove_sections(text: str, headings: list[str], changed: list) -> str:
    lines = text.split("\n")
    for title in headings:
        span = section_span(lines, title)
        if not span:
            raise SystemExit(f"remove-sections: heading '{title}' not found in base")
        del lines[span[0]:span[1]]
        changed.append({"section": title, "action": "removed"})
    return "\n".join(lines)


def append_file(text: str, payload_rel: str, changed: list) -> str:
    payload = (ROOT / payload_rel).read_text(encoding="utf-8")
    marker = next((l.strip() for l in payload.split("\n") if l.strip()), "")
    out = text.rstrip("\n") + "\n" + payload.rstrip("\n") + "\n"
    if marker and marker not in out:
        raise SystemExit("append-file: marker not present after append")
    changed.append({"section": marker, "action": "appended"})
    return out


def delete_substrings(text: str, subs: list[str], changed: list) -> str:
    for s in subs:
        if s not in text:
            raise SystemExit(f"delete-substrings: substring not found (stale plan?): {s!r}")
        text = text.replace(s, "")
        changed.append({"substring": s, "action": "deleted"})
    return text


def replace_text(text: str, edits: list[dict], changed: list) -> str:
    for e in edits:
        find, repl = e["find"], e["replace"]
        if find not in text:
            raise SystemExit(f"replace-text: find not present (stale plan?): {find!r}")
        text = text.replace(find, repl)
        changed.append({"find": find[:70], "action": "replaced"})
    return text


def remove_lines(text: str, pattern: str, max_removals, changed: list) -> str:
    rx = re.compile(pattern)
    out, removed = [], 0
    cap = max_removals if isinstance(max_removals, int) else 10 ** 9
    for ln in text.split("\n"):
        if removed < cap and rx.search(ln):
            removed += 1
            continue
        out.append(ln)
    if removed < 1:
        raise SystemExit(f"remove-lines: pattern matched nothing: {pattern}")
    changed.append({"pattern": pattern, "action": "removed-lines", "count": removed})
    return "\n".join(out)


def insert_after(text: str, anchor: str, ins: str, changed: list) -> str:
    rx = re.compile(anchor)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if rx.search(ln):
            lines.insert(i + 1, ins)
            changed.append({"anchor": anchor, "action": "inserted-after"})
            return "\n".join(lines)
    raise SystemExit(f"insert-after: anchor matched nothing: {anchor}")


def load_base(plan: dict) -> tuple[str, str, str]:
    b = plan["base"]
    ext = b["ext"]
    if b["kind"] == "normalized-seed":
        p = NORMALIZED / b["ref"] / f"document.{ext}"
    elif b["kind"] == "fixture":
        p = ROOT / b["ref"]
    else:
        raise SystemExit(f"unknown base kind: {b['kind']}")
    if not p.is_file():
        raise SystemExit(f"base not found: {p}")
    return p.read_text(encoding="utf-8"), ext, p.as_posix()


def run_plan(plan_path: Path) -> str:
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    cid = plan["case_id"]
    base, ext, base_path = load_base(plan)
    text = base
    changed: list = []
    for op in plan.get("operations", []):
        kind = op["op"]
        if kind == "remove-sections":
            text = remove_sections(text, op["headings"], changed)
        elif kind == "append-file":
            text = append_file(text, op["payload"], changed)
        elif kind == "delete-substrings":
            text = delete_substrings(text, op["substrings"], changed)
        elif kind == "replace-text":
            text = replace_text(text, op["edits"], changed)
        elif kind == "remove-lines":
            text = remove_lines(text, op["pattern"], op.get("max_removals"), changed)
        elif kind == "insert-after":
            text = insert_after(text, op["anchor"], op["text"], changed)
        else:
            raise SystemExit(f"[{cid}] unknown op: {kind}")

    if text == base:
        raise SystemExit(f"[{cid}] mutation was a no-op (mutated == base)")

    # invariant: forbidden_unrelated_changes sections stay byte-identical
    bl, ml = base.split("\n"), text.split("\n")
    for title in plan.get("forbidden_unrelated_changes", []):
        sb, sm = section_span(bl, title), section_span(ml, title)
        if sb and sm:
            if bl[sb[0]:sb[1]] != ml[sm[0]:sm[1]]:
                raise SystemExit(f"[{cid}] forbidden change: section '{title}' was modified")
        elif sb and not sm:
            raise SystemExit(f"[{cid}] forbidden change: section '{title}' vanished")

    out_dir = OUT / cid
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"document.{ext}").write_text(text, encoding="utf-8")
    diff = "\n".join(difflib.unified_diff(base.split("\n"), text.split("\n"),
                                          fromfile=f"base:{base_path}", tofile=f"mutated:{cid}", lineterm=""))
    (out_dir / "mutation.diff").write_text(diff + "\n", encoding="utf-8")
    (out_dir / "mutation_result.yaml").write_text(yaml.safe_dump({
        "mutation_result": {
            "case_id": cid, "mutation_id": plan.get("mutation_id"),
            "base_kind": plan["base"]["kind"], "base_ref": plan["base"]["ref"], "base_path": base_path,
            "base_sha256": sha(base), "mutated_sha256": sha(text),
            "changed_ranges": changed,
            "intended_blockers": plan.get("intended_blockers", []),
            "intended_findings": plan.get("intended_findings", []),
            "forbidden_unrelated_changes": plan.get("forbidden_unrelated_changes", []),
            "forbidden_changes_verified": True,
            "generated_at": NOW,
        }
    }, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return f"{cid}: {len(base)}B -> {len(text)}B; {len(changed)} change-op(s) -> cases/golden-negative/{cid}/"


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    picked = [a for a in argv[1:] if not a.startswith("--")]
    plans = [PLANS / f"{c}.yaml" for c in picked] if picked else sorted(PLANS.glob("*.yaml"))
    for p in plans:
        print("  " + run_plan(p))
    print(f"\n==> generated {len(plans)} golden-negative(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
