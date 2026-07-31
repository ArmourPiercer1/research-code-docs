#!/usr/bin/env python3
"""
score_grading.py — score a documentation-quality-evaluator run against a golden task-quality case.

Reads the evaluator's structured KEY=VALUE block out of its output and compares it to the golden case
(loaded from evals/skills/task-quality/<skill>.yaml by id). Computes the §8 admission metrics:

  - severe_issue_recall = |required_blockers ∩ reported BLOCKERS| / |required_blockers|   (>= 0.90)
  - false_pass          = 1 if the doc that should FAIL was PASSed OR a forbidden report pattern
                          matched (e.g. "FAIL only on a trivial gate but predict a re-eval PASS") (== 0)
  - blocker_soundness   = reported blockers that are in the allowed/expected set

The false-pass check is deliberately stricter than the literal verdict: the v0.2 report returned
verdict=FAIL yet declared the doc "substantively high quality" and predicted PASS — that IS a false
pass. `forbidden_report_patterns` in the case catch that signature.

Usage: python score_grading.py <case-id> <evaluator-output.txt> [--skill documentation-quality-evaluator]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[3]


def parse_block(text: str) -> dict:
    """Pull KEY=VALUE lines from the evaluator output (last occurrence wins)."""
    out: dict[str, str] = {}
    for key in ("DOCUMENT_QUALITY", "FACTUAL_VALIDITY", "READER_TEST", "CHECKER_STATUS",
                "SOURCE_COVERAGE", "CONFIDENCE", "VERDICT"):
        for m in re.finditer(rf"(?m)^\s*{key}\s*=\s*(.+?)\s*$", text):
            out[key] = m.group(1).strip()
    m = re.search(r"BLOCKERS\s*=\s*\[([^\]]*)\]", text)
    out["BLOCKERS"] = [b.strip() for b in re.split(r"[,\s]+", m.group(1)) if b.strip()] if m else []
    return out


def load_case(skill: str, case_id: str) -> dict:
    p = ROOT / "evals" / "skills" / "task-quality" / f"{skill}.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    for c in data.get("cases", []):
        if c.get("id") == case_id:
            return c
    raise SystemExit(f"case {case_id!r} not found in {p}")


def load_manifest(path: Path) -> dict:
    """Adapt a tests/corpus per-case manifest (§8) to the internal case shape used below.

    The corpus manifest carries `forbidden_blockers` (absent from the legacy inline yaml), so a run that
    fires an unrelated hard gate is caught here as a forbidden-blocker VIOLATION — the design's
    "无关硬门滥用率" metric.
    """
    m = yaml.safe_load(path.read_text(encoding="utf-8"))
    exp = m.get("expected", {}) or {}
    return {
        "id": m.get("case_id"),
        "expected": {
            "verdict": exp.get("document_quality"),
            "required_blockers": exp.get("required_blockers", []),
            "forbidden_blockers": exp.get("forbidden_blockers", []),
        },
        "forbidden_report_patterns": m.get("forbidden_report_patterns", []),
    }


def norm(tokens) -> set[str]:
    """Normalize HF ids: 'HF-14-...' -> 'HF-14a'? keep the leading HF-<n><letter?> token."""
    out = set()
    for t in tokens:
        m = re.match(r"(HF-\d+[a-e]?)", t.strip(), re.I)
        if m:
            out.add(m.group(1).upper().replace("HF-", "HF-"))
    return out


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    if "--manifest" in argv:
        # corpus mode: score against a tests/corpus per-case manifest (has forbidden_blockers)
        man_path = Path(argv[argv.index("--manifest") + 1])
        if len(args) < 1:
            print("usage: score_grading.py <evaluator-output.txt> --manifest <manifest.yaml>", file=sys.stderr)
            return 2
        case = load_manifest(man_path)
        case_id, out_path, skill = case["id"], Path(args[0]), "documentation-quality-evaluator"
    else:
        # legacy mode: <case-id> <output> [--skill <name>]
        if len(args) < 2:
            print("usage: score_grading.py <case-id> <evaluator-output.txt> [--skill <name>]\n"
                  "   or: score_grading.py <evaluator-output.txt> --manifest <manifest.yaml>", file=sys.stderr)
            return 2
        skill = argv[argv.index("--skill") + 1] if "--skill" in argv else "documentation-quality-evaluator"
        case_id, out_path = args[0], Path(args[1])
        case = load_case(skill, case_id)

    exp = case.get("expected", {})
    text = out_path.read_text(encoding="utf-8", errors="replace")
    block = parse_block(text)

    verdict = block.get("DOCUMENT_QUALITY") or block.get("VERDICT") or "?"
    reported = norm(block.get("BLOCKERS", []))
    required = norm(exp.get("required_blockers", exp.get("must_flag", [])))
    forbidden_b = norm(exp.get("forbidden_blockers", []))
    recall = (len(required & reported) / len(required)) if required else 1.0
    violated = reported & forbidden_b                         # forbidden gates the evaluator wrongly fired

    # forbidden report patterns (the "false-pass-in-substance" signature)
    forbidden = case.get("forbidden_report_patterns", [])
    fired = [pat for pat in forbidden if re.search(pat, text, re.I | re.S)]

    expected_verdict = str(exp.get("verdict", exp.get("expected_verdict", ""))).upper()
    literal_pass = verdict.upper() in ("PASS",)
    false_pass = int((expected_verdict == "FAIL" and literal_pass) or bool(fired))

    print(f"# grading score — case {case_id}  (skill {skill})")
    print(f"  parsed verdict block : {block}")
    print(f"  DOCUMENT_QUALITY     : {verdict}   (expected {expected_verdict or '?'})")
    print(f"  required blockers    : {sorted(required)}")
    print(f"  forbidden blockers   : {sorted(forbidden_b)}")
    print(f"  reported blockers    : {sorted(reported)}")
    print(f"  missed blockers      : {sorted(required - reported)}")
    print(f"  severe_issue_recall  : {recall:.2f}   (bar >= 0.90)")
    print(f"  forbidden VIOLATION  : {sorted(violated) if violated else 'none'}   (bar == none)")
    print(f"  forbidden patterns   : {'FIRED ' + str(fired) if fired else 'none'}")
    print(f"  false_pass           : {false_pass}   (bar == 0)")

    gate_ok = (recall >= 0.90) and (false_pass == 0) and (not violated) and (
        expected_verdict == "" or verdict.upper().startswith(expected_verdict))
    print(f"\n==> evaluator {'PASS' if gate_ok else 'FAIL'} against admission bar for this case")
    return 0 if gate_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
