#!/usr/bin/env python3
"""
apply_adjudication.py — stamp each case manifest's `adjudication:` block from reviewer A/B results.

Consumes evals/skills/adjudication/reviewer-results-<date>.yaml and, for each case, computes a consensus
per the adjudication protocol:

  - A and B agree AND their verdict matches the corpus intent (PASS==PASS / FAIL==FAIL)
        -> consensus = <verdict>, status = gold-candidate (lockable)
  - A and B agree but their verdict is PARTIAL while the corpus intends FAIL (or any A/B-vs-intent mismatch)
        -> consensus = queued, status = candidate  (routed to the user queue — never auto-overridden)
  - A and B disagree
        -> consensus = queued (reviewer split)

Non-destructive: every manifest ends with the `adjudication:` block, so we truncate at the LAST
`adjudication:` line and re-append a fresh block, preserving all content (and comments) above it.

Usage: python scripts/apply_adjudication.py [results.yaml]
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
DEFAULT_RESULTS = ROOT / "evals" / "skills" / "adjudication" / "reviewer-results-2026-07-31.yaml"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def combined_conf(ca: str, cb: str) -> str:
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    return min([ca, cb], key=lambda c: order.get(c, 1))


def decide(va, vb, intent):
    intent = (intent or "").upper()
    if va != vb:
        return "queued", "candidate", f"reviewers disagree (A={va}, B={vb})"
    v = va
    if v == intent:
        return v, "gold", "A/B agree and match corpus intent"
    if v == "PARTIAL" and intent == "FAIL":
        return "queued", "candidate", ("reviewers agree PARTIAL; corpus intends FAIL per the "
                                       "non-compensatory hard-gate contract — USER DECISION")
    if v == "PARTIAL" and intent == "PASS":
        return "queued", "candidate", "reviewers agree PARTIAL; corpus intends PASS — USER DECISION"
    return "queued", "candidate", f"reviewers agree {v}; corpus intends {intent} — USER DECISION"


def block(reviewer_a, reviewer_b, consensus, confidence, status, notes) -> str:
    d = {"adjudication": {
        "reviewer_a": reviewer_a, "reviewer_b": reviewer_b,
        "consensus": consensus, "confidence": confidence, "status": status,
        "adjudicated_at": NOW, "notes": notes,
    }}
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True).rstrip() + "\n"


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    results_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_RESULTS
    results = yaml.safe_load(results_path.read_text(encoding="utf-8"))["results"]

    by_id = {}
    for mp in CASES.glob("**/manifest.yaml"):
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        by_id[m["case_id"]] = (mp, m)

    gold = queued = 0
    for cid, r in results.items():
        if cid not in by_id:
            print(f"  [skip] {cid}: no manifest"); continue
        mp, m = by_id[cid]
        va, ca = r["a"]; vb, cb = r["b"]
        intent = (m.get("expected", {}) or {}).get("document_quality")
        if r.get("user_decision"):
            # explicit human ruling (e.g. the D-1 FAIL-vs-PARTIAL policy) overrides the auto-queue,
            # while the reviewer signal is preserved in the block for the record.
            consensus = str(r["user_decision"]).upper()
            status = "gold"
            why = (f"USER DECISION {r.get('user_decision_ref', '')}: gold={consensus} "
                   f"(reviewers A={va}/B={vb}; ruling recorded, not overridden by auto-queue)").strip()
        else:
            consensus, status, why = decide(va, vb, intent)
        notes = why + (f" | builder_note: {r['builder_note']}" if r.get("builder_note") else "")
        conf = combined_conf(ca, cb)
        newblk = block({"verdict": va, "confidence": ca, "tag": r.get("tag")},
                       {"verdict": vb, "confidence": cb},
                       consensus, conf, status, notes)

        text = mp.read_text(encoding="utf-8")
        idx = text.rfind("\nadjudication:")
        if idx == -1:
            print(f"  [ERR ] {cid}: no adjudication block to replace"); continue
        mp.write_text(text[:idx + 1] + newblk, encoding="utf-8")
        gold += (status == "gold"); queued += (status != "gold")
        print(f"  {cid:18s} A={va:7s} B={vb:7s} intent={str(intent):4s} -> {status.upper():9s} ({consensus})")

    print(f"\n==> {gold} gold-consensus, {queued} queued for user decision")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
