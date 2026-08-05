#!/usr/bin/env python3
"""
run_checks.py — run all deterministic checkers over a file or directory.

Classifies results into HARD gates (a fail here is a release blocker), ADVISORY
checks (quality hygiene), and SIGNAL checks (v0.3 — candidates the model adjudicates for
HF-13/14/15; they NEVER block or change the exit code). Prints a JSON summary and exits
non-zero if any HARD gate fails.

    HARD:     frontmatter_check (HF-9), status_vocab_check (HF-3/HF-10)
    ADVISORY: markdown_links_check, placeholders_check, interface_check (batch2.5 handoff contract),
              flow_state_check (batch3 control-flow status contract)
    SIGNAL:   state_number_consistency (HF-14a), completion_open_conflict (HF-14b),
              roadmap_stage_fields (HF-6/HF-15), agent_session_residue (HF-13/HF-8),
              artifact_role_mixing (HF-13)

Usage:
    python run_checks.py <path> [--json] [--advisory-is-hard]
    <path> may be a single .md file or a directory (recursively globs *.md,
    ignoring .venv/, references/mattpocock-skills/, and node_modules/).
    NOTE: directory scans skip fixtures/ (intentionally-bad seeds); pass a fixture FILE
    directly to run the checkers on it (single-file path bypasses the ignore filter).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter_check          # noqa: E402
import status_vocab_check         # noqa: E402
import markdown_links_check       # noqa: E402
import placeholders_check         # noqa: E402
import interface_check             # noqa: E402
import flow_state_check            # noqa: E402
import state_number_consistency   # noqa: E402
import completion_open_conflict   # noqa: E402
import roadmap_stage_fields       # noqa: E402
import agent_session_residue      # noqa: E402
import artifact_role_mixing       # noqa: E402

HARD = [("frontmatter", frontmatter_check), ("status_vocab", status_vocab_check)]
ADVISORY = [("markdown_links", markdown_links_check), ("placeholders", placeholders_check),
            ("interface", interface_check), ("flow_state", flow_state_check)]
# SIGNAL: advisory candidates for the model. `ok=True` = no candidate. NEVER sets hard_fail.
SIGNAL = [
    ("state_numbers", state_number_consistency),
    ("completion_open", completion_open_conflict),
    ("roadmap_fields", roadmap_stage_fields),
    ("session_residue", agent_session_residue),
    ("role_mixing", artifact_role_mixing),
]

IGNORE_PARTS = {".venv", "node_modules", "fixtures"}  # fixtures/ holds intentionally-bad eval seeds
IGNORE_SUBPATH = ("references/mattpocock-skills",)


def gather(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    files = []
    for p in sorted(path.rglob("*.md")):
        parts = set(p.parts)
        if parts & IGNORE_PARTS:
            continue
        rel = p.as_posix()
        if any(sub in rel for sub in IGNORE_SUBPATH):
            continue
        files.append(p)
    return files


def run(path: Path, advisory_is_hard: bool = False) -> dict:
    files = gather(path)
    report = {"path": str(path), "files_checked": len(files), "hard_fail": False, "results": []}
    for f in files:
        entry = {"file": str(f), "hard": {}, "advisory": {}, "signals": {}}
        for name, mod in HARD:
            ok, problems = mod.check_file(f)
            entry["hard"][name] = {"pass": ok, "problems": problems}
            if not ok:
                report["hard_fail"] = True
            # non-blocking v0.4 deprecation notes (never affect hard_fail / exit code)
            if hasattr(mod, "warnings"):
                notes = mod.warnings(f)
                if notes:
                    entry.setdefault("notes", []).extend(notes)
        for name, mod in ADVISORY:
            ok, problems = mod.check_file(f)
            entry["advisory"][name] = {"pass": ok, "problems": problems}
            if advisory_is_hard and not ok:
                report["hard_fail"] = True
        for name, mod in SIGNAL:
            ok, problems = mod.check_file(f)
            # SIGNAL is informational only — it NEVER sets report["hard_fail"] or the exit code.
            entry["signals"][name] = {"clear": ok, "candidates": problems}
        report["results"].append(entry)
    return report


def print_human(report: dict) -> None:
    print(f"# run_checks over {report['path']}  ({report['files_checked']} file(s))")
    for e in report["results"]:
        hard_ok = all(v["pass"] for v in e["hard"].values())
        adv_ok = all(v["pass"] for v in e["advisory"].values())
        signalled = [n for n, v in e["signals"].items() if not v["clear"]]
        tag = "OK" if (hard_ok and adv_ok) else ("HARD-FAIL" if not hard_ok else "advisory")
        if hard_ok and adv_ok and signalled:
            tag = "OK+signals"
        print(f"\n[{tag}] {e['file']}")
        for cat in ("hard", "advisory"):
            for name, res in e[cat].items():
                if not res["pass"]:
                    print(f"  ({cat}) {name}: FAIL")
                    for p in res["problems"]:
                        print(f"      - {p}")
        for name, res in e["signals"].items():
            if not res["clear"]:
                print(f"  (signal) {name}:")
                for p in res["candidates"]:
                    print(f"      - {p}")
    print(f"\n==> hard_fail = {report['hard_fail']}  (signals never affect this)")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if not args:
        print("usage: run_checks.py <path> [--json] [--advisory-is-hard]", file=sys.stderr)
        return 2
    report = run(Path(args[0]), advisory_is_hard=("--advisory-is-hard" in flags))
    if "--json" in flags:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_human(report)
    return 1 if report["hard_fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
