#!/usr/bin/env python3
"""
snapshot_sources.py — materialize immutable seed snapshots from tests/corpus/upstream into
tests/corpus/source-seeds/original/<seed-id>/, driven by seed-register.yaml.

For each seed with copy_permitted: true
  - byte-exact copy  upstream/<path>  ->  original/<seed-id>/source-document.<ext>
  - verify the copy's SHA-256 equals the register's sha256 (abort on any mismatch)
  - write SOURCE.yaml (provenance) + SHA256SUMS.txt
  - copy the owning repo's LICENSE file(s) -> original/<seed-id>/LICENSE.txt

For each seed with copy_permitted: false (quarantine / license-restricted)
  - write ONLY a SOURCE.yaml reference stub + LICENSE-REFERENCE.txt; copy NO body.

Upstream and original/ are read-only inputs/outputs of record; this script never touches upstream.

Usage:
  python scripts/snapshot_sources.py            # materialize snapshots
  python scripts/snapshot_sources.py --check     # re-verify existing snapshots vs the register (no writes)
"""
from __future__ import annotations
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "tests" / "corpus" / "upstream"
REGISTER = ROOT / "tests" / "corpus" / "source-seeds" / "seed-register.yaml"
ORIGINAL = ROOT / "tests" / "corpus" / "source-seeds" / "original"

LICENSE_NAMES = ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE-MIT", "LICENSE-APACHE",
                 "LICENSE.MIT", "LICENSE.CC0-1.0", "COPYING", "LICENCE", "LICENCE.rst"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def repo_dir_of(rel_path: str) -> Path:
    return UPSTREAM / Path(rel_path).parts[0]


def find_licenses(repo: Path) -> list[Path]:
    return [repo / n for n in LICENSE_NAMES if (repo / n).is_file()]


def load_seeds() -> list[dict]:
    return yaml.safe_load(REGISTER.read_text(encoding="utf-8"))["seeds"]


def materialize(seed: dict) -> tuple[str, str]:
    sid = seed["seed_id"]
    src = seed["source"]
    rel = src["path"]
    upstream_file = UPSTREAM / rel
    out_dir = ORIGINAL / sid
    out_dir.mkdir(parents=True, exist_ok=True)

    if not seed.get("copy_permitted", False):
        # quarantine / reference-only: NO body copy
        (out_dir / "SOURCE.yaml").write_text(yaml.safe_dump({
            "seed_id": sid, "content_copied": False, "use_mode": seed.get("use_mode"),
            "status": seed.get("status"), "reason": "copy_permitted=false (see cautions)",
            "repository": src["repository"], "commit": src["commit"], "path": rel,
            "sha256_upstream": src["sha256"], "size_bytes": src.get("size_bytes"),
            "license_spdx": src["license_spdx"], "snapshotted_at": NOW,
        }, sort_keys=False, allow_unicode=True), encoding="utf-8")
        (out_dir / "LICENSE-REFERENCE.txt").write_text(
            f"License: {src['license_spdx']}\nRepository: {src['repository']}\nCommit: {src['commit']}\n"
            f"No license file present upstream; body intentionally NOT copied (quarantine).\n", encoding="utf-8")
        # ensure no stray body was left from a previous run
        for stray in out_dir.glob("source-document.*"):
            stray.unlink()
        return sid, "quarantined (no body copied)"

    if not upstream_file.is_file():
        raise SystemExit(f"[{sid}] upstream file missing: {upstream_file}")

    ext = Path(rel).suffix.lstrip(".") or "txt"
    dst = out_dir / f"source-document.{ext}"
    shutil.copyfile(upstream_file, dst)  # byte-exact
    got = sha256(dst)
    if got != src["sha256"]:
        raise SystemExit(f"[{sid}] SHA-256 mismatch after copy: register={src['sha256']} got={got}")
    if got != sha256(upstream_file):
        raise SystemExit(f"[{sid}] copy differs from upstream (should be impossible)")

    (out_dir / "SHA256SUMS.txt").write_text(f"{got}  source-document.{ext}\n", encoding="utf-8")
    (out_dir / "SOURCE.yaml").write_text(yaml.safe_dump({
        "seed_id": sid, "content_copied": True, "use_mode": seed.get("use_mode"),
        "status": seed.get("status"), "artifact_type_candidate": seed.get("artifact_type_candidate"),
        "repository": src["repository"], "commit": src["commit"], "path": rel,
        "sha256": got, "size_bytes": len(dst.read_bytes()), "license_spdx": src["license_spdx"],
        "snapshotted_at": NOW,
    }, sort_keys=False, allow_unicode=True), encoding="utf-8")

    lics = find_licenses(repo_dir_of(rel))
    if lics:
        blob = "".join(f"===== {p.name} =====\n" + p.read_text(encoding="utf-8", errors="replace") + "\n"
                       for p in lics)
        (out_dir / "LICENSE.txt").write_text(blob, encoding="utf-8")
        note = f"copied {len(lics)} license file(s)"
    else:
        (out_dir / "LICENSE.txt").write_text(
            f"Declared license (no file found in repo root): {src['license_spdx']}\n", encoding="utf-8")
        note = "no license file in repo root; declared SPDX recorded"
    return sid, f"copied {dst.name} ({len(dst.read_bytes())} B); {note}"


def check(seed: dict) -> tuple[str, bool, str]:
    sid = seed["seed_id"]
    src = seed["source"]
    out_dir = ORIGINAL / sid
    if not seed.get("copy_permitted", False):
        bodies = list(out_dir.glob("source-document.*"))
        ok = not bodies
        return sid, ok, "OK (no body, as required)" if ok else f"VIOLATION: quarantined body present: {bodies}"
    ext = Path(src["path"]).suffix.lstrip(".") or "txt"
    dst = out_dir / f"source-document.{ext}"
    if not dst.is_file():
        return sid, False, "MISSING snapshot"
    got = sha256(dst)
    ok = got == src["sha256"]
    return sid, ok, "OK (sha matches register)" if ok else f"SHA MISMATCH register={src['sha256']} got={got}"


NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    seeds = load_seeds()
    if "--check" in argv:
        bad = 0
        for s in seeds:
            sid, ok, msg = check(s)
            print(f"  [{'OK ' if ok else 'FAIL'}] {sid}: {msg}")
            bad += (0 if ok else 1)
        print(f"\n==> snapshot check: {len(seeds)-bad}/{len(seeds)} OK, {bad} failing")
        return 0 if bad == 0 else 1
    for s in seeds:
        sid, msg = materialize(s)
        print(f"  {sid}: {msg}")
    print(f"\n==> materialized {len(seeds)} seed records into {ORIGINAL.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
