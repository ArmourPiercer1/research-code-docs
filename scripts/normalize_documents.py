#!/usr/bin/env python3
"""
normalize_documents.py — produce MECHANICALLY-normalized copies of the snapshot seeds for use as
evaluation inputs, in tests/corpus/source-seeds/normalized/<seed-id>/document.<ext>.

Allowed (docs/testing/corpus-policy.md §5): CRLF/CR -> LF, ensure UTF-8, ensure single trailing
newline. RST is KEPT as .rst (tool=none) — we do NOT convert PEP-2026 to Markdown, to avoid any
semantic drift; the evaluator reads RST as plain text.

FORBIDDEN and NOT done here: any content/semantic change (no added arguments, no filled alternatives,
no status edits, no beautifying). The script asserts the normalized text equals the source with ONLY
line-endings/trailing-newline differing, and records a normalization.yaml log with before/after SHAs.

By default normalizes seeds whose register use_mode == "snapshot" (the case inputs). Pass seed ids to
override.

Usage:
  python scripts/normalize_documents.py                 # the snapshot seeds
  python scripts/normalize_documents.py SEED-PEP-2026   # specific seeds
"""
from __future__ import annotations
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SEEDS_DIR = ROOT / "tests" / "corpus" / "source-seeds"
REGISTER = SEEDS_DIR / "seed-register.yaml"
ORIGINAL = SEEDS_DIR / "original"
NORMALIZED = SEEDS_DIR / "normalized"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_lf(text: str) -> str:
    """The ONLY transform: normalize newlines to LF and guarantee exactly one trailing newline."""
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    return t.rstrip("\n") + "\n"


def semantic_equal(a: str, b: str) -> bool:
    """True iff a and b differ only by line-endings / trailing whitespace-newlines."""
    norm = lambda s: [ln.rstrip() for ln in s.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n").split("\n")]
    return norm(a) == norm(b)


def normalize(seed: dict) -> str:
    sid = seed["seed_id"]
    ext = Path(seed["source"]["path"]).suffix.lstrip(".") or "txt"
    src = ORIGINAL / sid / f"source-document.{ext}"
    if not src.is_file():
        raise SystemExit(f"[{sid}] no snapshot body at {src} (run snapshot_sources.py; quarantined seeds cannot be normalized)")

    raw = src.read_bytes()
    text = raw.decode("utf-8")               # strict: seeds are UTF-8; a failure is a real problem
    out_text = canonical_lf(text)
    if not semantic_equal(text, out_text):
        raise SystemExit(f"[{sid}] refusing to write: normalization changed more than line-endings")

    out_dir = NORMALIZED / sid
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"document.{ext}"
    out_bytes = out_text.encode("utf-8")
    out_file.write_bytes(out_bytes)

    ops = ["line-ending-normalization(->LF)", "utf-8-reencode", "single-trailing-newline"]
    (out_dir / "normalization.yaml").write_text(yaml.safe_dump({
        "normalization": {
            "source_seed": sid,
            "tool": "none" if ext == "rst" else "custom-script",
            "rst_to_markdown": False,
            "operations": ops,
            "semantic_changes": False,
            "diff_review_required": True,
            "bytes_before": len(raw), "bytes_after": len(out_bytes),
            "sha256_before": sha256_bytes(raw), "sha256_after": sha256_bytes(out_bytes),
            "normalized_at": NOW,
        }
    }, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return f"{sid}: {src.name} -> normalized/{sid}/{out_file.name} ({len(raw)}B -> {len(out_bytes)}B)"


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    seeds = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))["seeds"]
    picked = [a for a in argv[1:] if not a.startswith("--")]
    targets = [s for s in seeds if (s["seed_id"] in picked) if picked] or \
              [s for s in seeds if s.get("use_mode") == "snapshot"]
    for s in targets:
        print("  " + normalize(s))
    print(f"\n==> normalized {len(targets)} seed(s) into {NORMALIZED.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
