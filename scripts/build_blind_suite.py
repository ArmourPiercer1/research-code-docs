#!/usr/bin/env python3
"""
build_blind_suite.py — assemble a BLIND run directory from the DQE gold/candidate corpus.

For each selected case it:
  - copies the case `document` to  blind-runs/<run-id>/inputs/<blind-id>.<ext>  (random UUID name);
  - writes  params/<blind-id>.yaml  with ONLY artifact_type + allowed profile (NO expected labels,
    NO class-name);
  - records  .secret/mapping.tsv  (blind-id -> case-id -> manifest) — read ONLY by the comparator.

The evaluator run (make_grading_injection.py --role evaluator) is pointed at inputs/ + params/ and must
never read .secret/ or tests/corpus/cases. Order is shuffled so a pair's two members are not adjacent.

Usage:
  python scripts/build_blind_suite.py --all                       # every case
  python scripts/build_blind_suite.py GP-ADR-001 GN-ADR-001       # specific cases
  python scripts/build_blind_suite.py --sample 6 --seed 7         # random subset
  python scripts/build_blind_suite.py --all --run-id smoke        # named run dir
"""
from __future__ import annotations
import random
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "corpus" / "cases"
RUNS = ROOT / "tests" / "corpus" / "blind-runs"


def load_manifests(picked: list[str]) -> list[tuple[Path, dict]]:
    out = []
    for mp in sorted(CASES.glob("**/manifest.yaml")):
        m = yaml.safe_load(mp.read_text(encoding="utf-8"))
        if picked and m.get("case_id") not in picked:
            continue
        out.append((mp, m))
    return out


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    raw = argv[1:]
    value_flags = {"--seed", "--run-id", "--sample"}
    skip = {i + 1 for i, a in enumerate(raw) if a in value_flags}   # exclude each value-flag's VALUE
    picked = [a for i, a in enumerate(raw) if not a.startswith("--") and i not in skip]
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 1337
    run_id = argv[argv.index("--run-id") + 1] if "--run-id" in argv else \
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sample = int(argv[argv.index("--sample") + 1]) if "--sample" in argv else None

    mans = load_manifests(picked)
    if not mans:
        raise SystemExit("no cases selected")
    rng = random.Random(seed)
    rng.shuffle(mans)
    if sample:
        mans = mans[:sample]

    run = RUNS / run_id
    (run / "inputs").mkdir(parents=True, exist_ok=True)
    (run / "params").mkdir(parents=True, exist_ok=True)
    (run / ".secret").mkdir(parents=True, exist_ok=True)

    mapping = ["blind_id\tcase_id\tmanifest\tpair_id"]
    for mp, m in mans:
        cid = m["case_id"]
        doc = ROOT / m["document"]
        ext = doc.suffix.lstrip(".") or "md"
        blind_id = uuid.UUID(int=rng.getrandbits(128)).hex[:12]     # rng-seeded -> reproducible
        shutil.copyfile(doc, run / "inputs" / f"{blind_id}.{ext}")
        prof = m.get("profile", {}) or {}
        (run / "params" / f"{blind_id}.yaml").write_text(yaml.safe_dump({
            "blind_id": blind_id,
            "artifact_type": m.get("artifact_type"),
            "profile": prof,          # provenance_policy etc. — allowed; contains NO expected labels
        }, sort_keys=False, allow_unicode=True), encoding="utf-8")
        mapping.append(f"{blind_id}\t{cid}\t{mp.relative_to(ROOT).as_posix()}\t{m.get('pair_id','')}")

    (run / ".secret" / "mapping.tsv").write_text("\n".join(mapping) + "\n", encoding="utf-8")
    (run / "README.md").write_text(
        f"# Blind run {run_id}\n\n"
        f"- {len(mans)} case(s), shuffle seed {seed}.\n"
        "- Evaluator/reviewer runs read ONLY `inputs/` + `params/`.\n"
        "- `.secret/mapping.tsv` maps blind_id -> case_id and is for the COMPARATOR ONLY. Do NOT mount it "
        "into an evaluator run.\n"
        "- Nothing here exposes expected verdicts or class-name directories.\n", encoding="utf-8")

    print(f"# blind suite -> {run.relative_to(ROOT).as_posix()}  ({len(mans)} case(s), seed {seed})")
    for line in mapping[1:]:
        bid, cid, *_ = line.split("\t")
        print(f"  {bid}  <-  {cid}")
    print(f"\n==> inputs/ + params/ ready; expected labels isolated in .secret/mapping.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
