#!/usr/bin/env python3
"""
validate_case_manifests.py — structural validation of the DQE case corpus (no model, no network).

Checks (docs/documentation-quality-evaluator_测试语料自动准备与评测流程.md §14):
  - case_id present + globally unique;
  - class is a known value; artifact_type present;
  - the `document:` path exists on disk;
  - required_blockers ∩ forbidden_blockers == ∅ (after HF-id normalization);
  - upstream-seed / mutation cases carry provenance (commit, or a base_case/base_fixture/base_seed);
  - golden-negative cases have a materialized mutation_result.yaml;
  - NO expected-label leakage: the blind `document` must not contain manifest-only keys;
  - boundary pairs are complete: every pair_id has exactly one `pass` and one `fail`.
  - gold consensus: WARN if adjudication.consensus is still pending (ERROR only with --require-consensus).

Exit code 0 iff there are no ERRORs.

Usage:
  python scripts/validate_case_manifests.py [tests/corpus/cases] [--require-consensus]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {"golden-positive", "golden-negative", "boundary-pass", "boundary-fail", "candidate"}
QUALITY_BANDS = {"PASS", "PARTIAL", "FAIL"}
GATE_DECISIONS = {"ALLOW", "BLOCK", "INCOMPLETE"}
LEAK_KEYS = ["required_blockers", "forbidden_blockers", "factual_validity_allowed", "difference_under_test"]
HF = re.compile(r"(HF-\d+[a-e]?)", re.I)


def norm_hf(xs) -> set[str]:
    out = set()
    for x in xs or []:
        m = HF.match(str(x).strip())
        if m:
            out.add(m.group(1).upper())
    return out


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    args = [a for a in argv[1:] if not a.startswith("--")]
    require_consensus = "--require-consensus" in argv
    base = ROOT / (args[0] if args else "tests/corpus/cases")

    manifests = sorted(base.glob("**/manifest.yaml"))
    # quarantined v1 snapshots (cases/quarantine/**) are archived, not live — skip them entirely.
    skipped_quarantine = [mp for mp in manifests if "quarantine" in mp.parts]
    manifests = [mp for mp in manifests if "quarantine" not in mp.parts]
    errors: list[str] = []
    warns: list[str] = []
    ids: dict[str, Path] = {}
    pairs: dict[str, set] = {}

    parsed = []
    for mp in manifests:
        try:
            m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            errors.append(f"{mp}: YAML parse error: {e}")
            continue
        parsed.append((mp, m))
        cid = m.get("case_id")
        rel = mp.relative_to(ROOT).as_posix()
        if not cid:
            errors.append(f"{rel}: missing case_id"); continue
        if cid in ids:
            errors.append(f"{rel}: duplicate case_id {cid} (also {ids[cid].relative_to(ROOT).as_posix()})")
        ids[cid] = mp

        if m.get("class") not in CLASSES:
            errors.append(f"{cid}: unknown class {m.get('class')!r}")
        if not m.get("artifact_type"):
            errors.append(f"{cid}: missing artifact_type")

        # document exists
        doc = m.get("document")
        docp = ROOT / doc if doc else None
        if not doc or not docp.is_file():
            errors.append(f"{cid}: document not found: {doc}")
        else:
            text = docp.read_text(encoding="utf-8", errors="replace")
            for k in LEAK_KEYS:
                if k in text:
                    errors.append(f"{cid}: expected-label LEAKAGE — blind document contains '{k}'")

        exp = m.get("expected", {}) or {}
        req = norm_hf(exp.get("required_blockers"))
        forb = norm_hf(exp.get("forbidden_blockers"))
        both = req & forb
        if both:
            errors.append(f"{cid}: required ∩ forbidden blockers non-empty: {sorted(both)}")

        # additive two-axis fields (ADR-DQE-001): validate enums when present
        qb = exp.get("quality_band")
        if qb is not None and str(qb).upper() not in QUALITY_BANDS:
            errors.append(f"{cid}: expected.quality_band {qb!r} not in {sorted(QUALITY_BANDS)}")
        gd = exp.get("gate_decision")
        if gd is not None and str(gd).upper() not in GATE_DECISIONS:
            errors.append(f"{cid}: expected.gate_decision {gd!r} not in {sorted(GATE_DECISIONS)}")
        cv = m.get("case_version")
        if cv is not None and not isinstance(cv, int):
            errors.append(f"{cid}: case_version must be an integer, got {cv!r}")

        src = m.get("source", {}) or {}
        kind = src.get("kind")
        if kind == "upstream-seed" and not src.get("upstream_commit"):
            errors.append(f"{cid}: upstream-seed missing upstream_commit")
        if kind == "mutation":
            if not (src.get("base_seed") or src.get("base_fixture") or (m.get("mutation") or {}).get("base_case")):
                errors.append(f"{cid}: mutation case missing base linkage")
            if m.get("class") == "golden-negative" and not (mp.parent / "mutation_result.yaml").is_file():
                errors.append(f"{cid}: golden-negative missing mutation_result.yaml (run generate_mutations.py)")

        # boundary pair bookkeeping
        pid = m.get("pair_id")
        if pid:
            pairs.setdefault(pid, set()).add(m.get("pair_role"))

        # consensus
        cons = ((m.get("adjudication") or {}).get("consensus"))
        if cons in (None, "pending"):
            (errors if require_consensus else warns).append(f"{cid}: adjudication.consensus is pending")

    for pid, roles in sorted(pairs.items()):
        if roles != {"pass", "fail"}:
            errors.append(f"boundary pair {pid}: roles must be exactly {{pass, fail}}, got {sorted(roles)}")

    print(f"# validated {len(parsed)} manifests under {base.relative_to(ROOT).as_posix()}")
    print(f"  ids: {len(ids)} unique | boundary pairs: {len(pairs)} | quarantined(skipped): {len(skipped_quarantine)}")
    for w in warns:
        print(f"  [WARN]  {w}")
    for e in errors:
        print(f"  [ERROR] {e}")
    print(f"\n==> {len(errors)} error(s), {len(warns)} warning(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
