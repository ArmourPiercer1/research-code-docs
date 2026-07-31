#!/usr/bin/env python3
"""
validate_mutation_semantics.py — SEMANTIC post-checks on the DQE case corpus (no model, no network).

Where validate_case_manifests.py checks structure, this checks that a mutation/fixture actually carries
its intended defect cleanly and introduced no secondary defect. It exists because the 2026-07-31 matrix
shipped two invalid fixtures that "generated fine": a stale measurable gate survived (GN-ROADMAP-001) and
a dangling TOC was left behind (GN-PROP-001). See docs/skill-development/reports/dqe-v0.4-defect-ledger.md
(D-12).

Checks per live case (cases/quarantine/** is skipped — archived, not live):
  1. TOC anchor resolution — every `[..](#anchor)` inside a `<!-- toc -->` block must resolve to a real
     heading (GitHub slug). A dangling anchor is a secondary defect. (catches D-08)
  2. Retired-status contamination — a document-level `status: DECIDED` (retired by ADR-DQE-001) MUST NOT
     co-occur with a claim-level unverified/in-progress marker (HYPOTHESIS / 尚未验证 / design review in
     progress) in the same document. (catches D-07, D-09)
  3. Mutation post-conditions — for golden-negatives with a mutation_result.yaml carrying
     `postconditions`, re-verify assert_absent (gone) / assert_present (present) against the CURRENT
     document, so a later hand-edit cannot silently invalidate the mutation.
  4. Profile-pair byte equality — for a boundary pair whose two members declare DIFFERENT
     provenance_policy, the two documents MUST be byte-identical (the only difference under test is the
     profile, not the bytes). (guards the BP-004 control)

Exit code 0 iff there are no ERRORs.

Usage:
  python scripts/validate_mutation_semantics.py [tests/corpus/cases]
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
TOC_OPEN, TOC_CLOSE = re.compile(r"<!--\s*toc\s*-->", re.I), re.compile(r"<!--\s*/toc\s*-->", re.I)
TOC_ANCHOR = re.compile(r"\]\(#([^)]+)\)")
FRONTMATTER = re.compile(r"^\s*<!--(.*?)-->", re.S)
# Strong claim-level labels that must NOT sit under a document-level `status: DECIDED`. Deliberately
# narrow: a plain open question like "(design review in progress)" in an accepted doc is legitimate
# (ADR-DQE-001), so it is NOT a contamination marker — only an explicit unverified-claim label is.
UNVERIFIED_MARKERS = ["HYPOTHESIS", "尚未验证"]


def gh_slug(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)   # drop punctuation except word chars / space / hyphen
    s = re.sub(r"\s", "-", s)        # GitHub replaces EACH whitespace char (does not collapse runs)
    return s


def heading_slugs(text: str) -> set[str]:
    out: set[str] = set()
    in_fence = False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(ln)
        if m:
            out.add(gh_slug(m.group(2)))
    return out


def toc_anchors(text: str) -> list[str]:
    lines = text.split("\n")
    inside, anchors = False, []
    for ln in lines:
        if TOC_OPEN.search(ln):
            inside = True; continue
        if TOC_CLOSE.search(ln):
            inside = False; continue
        if inside:
            anchors += TOC_ANCHOR.findall(ln)
    return anchors


def dangling_toc(text: str) -> list[str]:
    slugs = heading_slugs(text)
    return [a for a in toc_anchors(text) if a not in slugs]


def frontmatter_block(text: str) -> str:
    m = FRONTMATTER.match(text)
    return m.group(1) if m else ""


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    base = ROOT / (args[0] if args else "tests/corpus/cases")

    manifests = [mp for mp in sorted(base.glob("**/manifest.yaml")) if "quarantine" not in mp.parts]
    errors: list[str] = []
    warns: list[str] = []
    checked = 0
    pairs: dict[str, list] = {}

    for mp in manifests:
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        cid = m.get("case_id", mp.parent.name)
        doc_rel = m.get("document")
        docp = ROOT / doc_rel if doc_rel else None
        if not docp or not docp.is_file():
            continue                       # structural validator already flags a missing document
        text = docp.read_text(encoding="utf-8", errors="replace")
        checked += 1

        # 1. dangling TOC
        for a in dangling_toc(text):
            errors.append(f"{cid}: dangling TOC anchor '#{a}' (no matching heading) — {doc_rel}")

        # 2. retired-status contamination
        fm = frontmatter_block(text)
        if re.search(r"^\s*status:\s*DECIDED\s*$", fm, re.I | re.M):
            hits = [mk for mk in UNVERIFIED_MARKERS if mk in text]
            if hits:
                errors.append(f"{cid}: retired `status: DECIDED` co-occurs with unverified marker(s) "
                              f"{hits} — use document_lifecycle (ADR-DQE-001) — {doc_rel}")
            else:
                warns.append(f"{cid}: uses retired `status: DECIDED` header (ADR-DQE-001 prefers "
                             f"document_lifecycle) — {doc_rel}")

        # 3. mutation post-conditions re-check
        mr = mp.parent / "mutation_result.yaml"
        if mr.is_file():
            mrd = (yaml.safe_load(mr.read_text(encoding="utf-8")) or {}).get("mutation_result", {}) or {}
            post = mrd.get("postconditions") or {}
            for s in post.get("assert_absent", []) or []:
                if s in text:
                    errors.append(f"{cid}: postcondition assert_absent VIOLATED — {s!r} still present")
            for s in post.get("assert_present", []) or []:
                if s not in text:
                    errors.append(f"{cid}: postcondition assert_present VIOLATED — {s!r} missing")
            if post.get("assert_no_dangling_toc") and dangling_toc(text):
                errors.append(f"{cid}: assert_no_dangling_toc set but dangling anchors remain")

        # 4. gather boundary-pair members for the byte-equality check
        pid = m.get("pair_id")
        if pid:
            pairs.setdefault(pid, []).append({
                "cid": cid, "sha": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "path": docp.resolve(),
                "policy": ((m.get("profile") or {}).get("provenance_policy")),
            })

    for pid, members in sorted(pairs.items()):
        if len(members) == 2:
            a, b = members
            if a["policy"] and b["policy"] and a["policy"] != b["policy"]:
                if a["sha"] != b["sha"]:
                    errors.append(f"boundary pair {pid}: members declare different provenance_policy "
                                  f"({a['policy']} vs {b['policy']}) but documents are NOT byte-identical "
                                  f"— a profile pair's only difference must be the profile")

    print(f"# semantic-validated {checked} live documents under {base.relative_to(ROOT).as_posix()}")
    for w in warns:
        print(f"  [WARN]  {w}")
    for e in errors:
        print(f"  [ERROR] {e}")
    print(f"\n==> {len(errors)} error(s), {len(warns)} warning(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
