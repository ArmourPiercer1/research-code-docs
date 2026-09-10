#!/usr/bin/env python3
"""decision_note_lint.py — Phase-2 (revised slice §5/§6; R3/R4/R5): decision-note format.

Scope: files under docs/decision-notes/{proposed,decided,rejected,archived}/*.md
(a repo root anywhere; the lint resolves the repo root itself). A file outside that
tree passes vacuously.

Rules (prompt §5.4 + the R4.5 revised state schema, frozen per invariants I4.1):
  N1: the note carries a non-empty `id:`.
  N2: all six orthogonal state fields are present with values in the legal sets:
        object_type:          claim | route | experiment | design_decision | requirement | artifact
        epistemic_state:      unknown | hypothesis | inferred | observed | supported | contradicted
        decision_state:       not_applicable | proposed | decided | rejected | deferred | superseded
        evidence_level:       E0..E5
        evidence_state:       current | stale | contradicted
        implementation_state: not_applicable | none | planned | in_progress | implemented | blocked
      (A generic `status:` field is NOT part of the format — prompt §2.3.)
  N3: the seven required content sections are present and non-empty:
        problem (or question), decision, evidence_basis (or evidence),
        alternatives (or alternatives_considered), why, consequences, revisit_condition
  N4: the folder state matches decision_state — decided/ ⇒ decided; proposed/ ⇒
      proposed; rejected/ ⇒ rejected; archived/ ⇒ decided|rejected|deferred|superseded.
      implementation_state is never inferred from decision_state (independent field).
  N5: a note in rejected/ carries a non-empty `rejection_basis` (R5 explicit bases).

Usage:
    python decision_note_lint.py <file.md> [...]
Exit code 0 if all pass, 1 otherwise.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DECISION_NOTES = ("docs", "decision-notes")

OBJECT_TYPE = {"claim", "route", "experiment", "design_decision", "requirement", "artifact"}
EPISTEMIC = {"unknown", "hypothesis", "inferred", "observed", "supported", "contradicted"}
DECISION = {"not_applicable", "proposed", "decided", "rejected", "deferred", "superseded"}
EVIDENCE_LEVEL = {"E0", "E1", "E2", "E3", "E4", "E5"}
EVIDENCE_STATE = {"current", "stale", "contradicted"}
IMPL = {"not_applicable", "none", "planned", "in_progress", "implemented", "blocked"}
FOLDER_ALLOWED = {
    "proposed": {"proposed"},
    "decided": {"decided"},
    "rejected": {"rejected"},
    "archived": {"decided", "rejected", "deferred", "superseded"},
}
CONTENT_ALIASES = {
    "problem": ("problem", "question"),
    # the slice §6 note shape carries the decision as `ruling:` — accept both
    "decision": ("decision", "ruling"),
    "evidence_basis": ("evidence_basis", "evidence"),
    "alternatives": ("alternatives", "alternatives_considered"),
    "why": ("why",),
    "consequences": ("consequences",),
    "revisit_condition": ("revisit_condition",),
}
def _key_value(text: str, key: str) -> str | None:
    """Return the value of a top-level-or-indented `key:` line, or None if absent/empty.
    Accepts an inline value OR a block value on following indented/'- ' lines."""
    pat = re.compile(rf"^\s*{re.escape(key)}\s*:\s*(.*?)\s*$", re.MULTILINE)
    for m in pat.finditer(text):
        inline = m.group(1).strip()
        if inline and inline not in ("|", ">", "|-", ">-", "null", "~"):
            return inline
        tail = text[m.end():].lstrip("\n").splitlines()
        if tail and (tail[0].startswith(("  ", "\t", "- "))):
            return tail[0].strip()
    return None


def _in_scope(path: Path) -> str | None:
    """Return the stage folder name if the file is a decision note, else None."""
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        return None
    if tuple(parts[:2]) != DECISION_NOTES or len(parts) < 3:
        return None
    if parts[2] not in FOLDER_ALLOWED:
        return None
    if parts[3] == "README.md":
        return None
    return parts[2]


def check_file(path: Path) -> tuple[bool, list[str]]:
    stage = _in_scope(path)
    if stage is None:
        return True, []
    text = path.read_text(encoding="utf-8", errors="replace")
    problems: list[str] = []

    if not _key_value(text, "id"):
        problems.append("decision-note-lint N1: missing/empty 'id'")

    for field, legal in (("object_type", OBJECT_TYPE), ("epistemic_state", EPISTEMIC),
                         ("decision_state", DECISION), ("evidence_level", EVIDENCE_LEVEL),
                         ("evidence_state", EVIDENCE_STATE), ("implementation_state", IMPL)):
        v = _key_value(text, field)
        if v is None:
            problems.append(f"decision-note-lint N2: missing/empty '{field}'")
        elif v not in legal:
            problems.append(f"decision-note-lint N2: '{field}' value {v!r} not in legal set "
                            f"{sorted(legal)}")

    for canon, aliases in CONTENT_ALIASES.items():
        if not any(_key_value(text, a) for a in aliases):
            problems.append(f"decision-note-lint N3: missing/empty required section "
                            f"{canon!r} (aliases: {', '.join(aliases)})")

    ds = _key_value(text, "decision_state")
    if ds is not None and ds not in FOLDER_ALLOWED[stage]:
        problems.append(f"decision-note-lint N4: folder '{stage}/' does not match "
                        f"decision_state: {ds!r} (allowed: {sorted(FOLDER_ALLOWED[stage])})")

    if stage == "rejected" and not _key_value(text, "rejection_basis"):
        problems.append("decision-note-lint N5: rejected/ note has no non-empty 'rejection_basis' (R5)")

    return (len(problems) == 0), problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: decision_note_lint.py <file.md> [...]", file=sys.stderr)
        return 2
    ok_all = True
    for arg in argv[1:]:
        ok, problems = check_file(Path(arg))
        print(f"[{'PASS' if ok else 'FAIL'}] {arg}")
        for p in problems:
            print(f"    - {p}")
        ok_all = ok_all and ok
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
