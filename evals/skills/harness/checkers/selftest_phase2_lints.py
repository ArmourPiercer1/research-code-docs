#!/usr/bin/env python3
"""selftest_phase2_lints.py — planted-defect self-tests for the Phase-2 lint portfolio.

Pattern (classification H5): each NEW checker carries a planted defect it must catch —
a planted defect not caught is a release blocker. Also runs the canonical-impact-lint
scenarios required by the Phase-2 implementation prompt §5.5 and the isolated
planted stale-roadmap defect (eval-plan §c defect 1 / revised slice §5).

Exit code 0 = all self-tests pass, 1 = at least one failed.
"""
from __future__ import annotations
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO_ROOT = HERE.parents[3]
TMP_AREA = REPO_ROOT / ".lint-fixtures-tmp"   # inside the workspace (sandbox-writable)
import archive_lint          # noqa: E402
import supersession_lint     # noqa: E402
import decision_note_lint    # noqa: E402
import canonical_impact_lint # noqa: E402
import register_check        # noqa: E402

PASS, FAIL = 0, 0
_fx_counter = 0


def report(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
    else:
        PASS += 1
    print(f"[{tag}] {name}" + (f"  -- {detail}" if detail and not ok else ""))


def make_fixture(files: dict[str, str]) -> Path:
    """Create a temp fixture repo mirroring the governance path layout.
    (os.makedirs, not tempfile.mkdtemp: mkdtemp dirs are write-denied under the
    DSH file sandbox, which breaks nested dir creation.)"""
    TMP_AREA.mkdir(exist_ok=True)
    global _fx_counter
    _fx_counter += 1
    root = TMP_AREA / f"fixture-{os.getpid()}-{_fx_counter}"
    root.mkdir(exist_ok=True)
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return root


VOID_BANNER = ("> **⛔ VOID / SUPERSEDED (2026-09-01).** This plan is retired. Governing plan: "
               "[docs/plans/active/charter.md](../../plans/active/charter.md).")


# ---------------------------------------------------------------- archive_lint
def t_archive():
    fx = make_fixture({
        "docs/plans/active/charter.md": "# Charter\n",
        # planted 1: VOID doc outside archived/ (the D12 zombie class)
        "docs/skill-development/stale-roadmap.md": f"# Stale Roadmap\n\n{VOID_BANNER}\n",
        # planted 2: archived VOID doc that lost its replacement pointer
        "docs/plans/archived/lost-pointer.md":
            "> **⛔ VOID / SUPERSEDED (2026-08-01).** Retired. No replacement named.\n",
        # clean 1: archived VOID doc with date + replacement pointer
        "docs/plans/archived/good.md": f"# Good\n\n{VOID_BANNER}\n",
        # clean 2: active doc that only MENTIONS 'VOID' in prose
        "docs/active-prose.md": "# Doc\n\nThe old plan was declared VOID in 2026; see the changelog.\n",
        # clean 3: frozen mirror is exempt
        "docs/reconstruction-external-review/snapshot.md": f"# Snap\n\n{VOID_BANNER}\n",
    })
    archive_lint.ROOT = fx
    try:
        ok, probs = archive_lint.check_file(fx / "docs/skill-development/stale-roadmap.md")
        report("archive: planted VOID doc outside archived/ caught (R1)",
               (not ok) and any("R1" in p and "stale-roadmap" in p for p in probs), str(probs))
        ok, probs = archive_lint.check_file(fx / "docs/plans/archived/lost-pointer.md")
        report("archive: planted lost replacement pointer caught (R2)",
               (not ok) and any("R2" in p for p in probs), str(probs))
        ok, _ = archive_lint.check_file(fx / "docs/plans/archived/good.md")
        report("archive: clean archived doc passes", ok)
        ok, _ = archive_lint.check_file(fx / "docs/active-prose.md")
        report("archive: prose mention without banner passes", ok)
        ok, _ = archive_lint.check_file(fx / "docs/reconstruction-external-review/snapshot.md")
        report("archive: frozen mirror exempt", ok)
    finally:
        _rmtree(fx)


# ---------------------------------------------------------- supersession_lint
def t_supersession():
    fx = make_fixture({
        "docs/decision-notes/decided/d-001.md":
            "# D-001\n\n```yaml\n- id: D-001\n  supersedes: D-000\n```\n- id: D-000\n",
        "docs/notes/bad-path.md": "# Bad\n\nsupersedes: no-such-doc-xyz123.md\n",
        "docs/notes/bad-id.md": "# Bad\n\nsuperseded_by: D-999\n",
        "docs/notes/zombie-ref.md": "# Zombie\n\nsupersedes: stale-roadmap.md\n",
        "docs/notes/quoted-empty.md": '# QE\n\nsupersedes: ""\nsuperseded_by: \'\'\n',
        "docs/skill-development/stale-roadmap.md": f"# Stale\n\n{VOID_BANNER}\n",
    })
    supersession_lint.ROOT = fx
    try:
        ok, _ = supersession_lint.check_file(fx / "docs/notes/quoted-empty.md")
        report("supersession: quoted-empty values pass (upstream ADR style)", ok)
        ok, _ = supersession_lint.check_file(fx / "docs/decision-notes/decided/d-001.md")
        report("supersession: same-file ID lineage passes", ok)
        ok, probs = supersession_lint.check_file(fx / "docs/notes/bad-path.md")
        report("supersession: planted missing path target caught (S1)",
               (not ok) and any("S1" in p for p in probs), str(probs))
        ok, probs = supersession_lint.check_file(fx / "docs/notes/bad-id.md")
        report("supersession: planted missing ID (S2) + missing reason (S5) caught",
               (not ok) and any("S2" in p for p in probs) and any("S5" in p for p in probs), str(probs))
        ok, probs = supersession_lint.check_file(fx / "docs/notes/zombie-ref.md")
        report("supersession: planted ref to VOID doc outside archive caught (S4)",
               (not ok) and any("S4" in p for p in probs), str(probs))
    finally:
        _rmtree(fx)


# -------------------------------------------------------- decision_note_lint
GOOD_NOTE = """# D-1 note

```yaml
id: D-1
object_type: design_decision
epistemic_state: supported
decision_state: decided
evidence_level: E3
evidence_state: current
implementation_state: not_applicable
problem: Which doc owns "what is next"?
decision: Option A — the status table.
evidence_basis: Final external-review ruling (2026-09-10).
alternatives: "Option B register rows; Option C architecture doc."
why: Single mutable owner; decisions stay in the register.
consequences: Status table is the only what-is-next authority.
revisit_condition: If a second what-is-next owner proves necessary.
```
"""
BAD_NOTE = GOOD_NOTE.replace("decision_state: decided", "decision_state: decided  # wrong folder") \
    .replace("implementation_state: not_applicable", "") \
    .replace("revisit_condition: If a second what-is-next owner proves necessary.", "")
# slice §6 shape: the decision is carried as `ruling:` (no literal `decision:` key)
RULING_NOTE = GOOD_NOTE.replace("decision: Option A — the status table.", "ruling: Option A — the status table.")


def t_decision_note():
    fx = make_fixture({
        "docs/decision-notes/decided/good.md": GOOD_NOTE,
        "docs/decision-notes/decided/bad.md": BAD_NOTE,          # N2 (no impl_state) + N3 (no revisit)
        "docs/decision-notes/proposed/mismatch.md": GOOD_NOTE,   # N4 folder vs decision_state
        "docs/decision-notes/rejected/no-basis.md":
            GOOD_NOTE.replace("decision_state: decided", "decision_state: rejected"),
        "docs/decision-notes/decided/ruling-shape.md": RULING_NOTE,
        "docs/other/note-lookalike.md": GOOD_NOTE,               # out of scope
    })
    decision_note_lint.ROOT = fx
    try:
        ok, _ = decision_note_lint.check_file(fx / "docs/decision-notes/decided/good.md")
        report("decision-note: clean decided note passes", ok)
        ok, _ = decision_note_lint.check_file(fx / "docs/decision-notes/decided/ruling-shape.md")
        report("decision-note: slice §6 ruling-shape note passes (decision alias)", ok)
        ok, probs = decision_note_lint.check_file(fx / "docs/decision-notes/decided/bad.md")
        report("decision-note: planted missing fields caught (N2+N3)",
               (not ok) and any("N2" in p and "implementation_state" in p for p in probs)
               and any("N3" in p and "revisit_condition" in p for p in probs), str(probs))
        ok, probs = decision_note_lint.check_file(fx / "docs/decision-notes/proposed/mismatch.md")
        report("decision-note: planted folder/decision_state mismatch caught (N4)",
               (not ok) and any("N4" in p for p in probs), str(probs))
        ok, probs = decision_note_lint.check_file(fx / "docs/decision-notes/rejected/no-basis.md")
        report("decision-note: planted rejected note w/o rejection_basis caught (N5)",
               (not ok) and any("N5" in p for p in probs), str(probs))
        ok, _ = decision_note_lint.check_file(fx / "docs/other/note-lookalike.md")
        report("decision-note: out-of-scope file passes vacuously", ok)
    finally:
        _rmtree(fx)


# ------------------------------------------------------ canonical_impact_lint
def _gitc(root: Path, *args: str) -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   check=True, capture_output=True, env=env)


def _rmtree(p: Path) -> None:
    import stat
    def onerror(func, path, exc):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except OSError:
            pass
    shutil.rmtree(p, onexc=onerror)


def t_canonical_impact():
    TMP_AREA.mkdir(exist_ok=True)
    global _fx_counter
    _fx_counter += 1
    fx = TMP_AREA / f"impact-{os.getpid()}-{_fx_counter}"
    (fx / "docs").mkdir(parents=True)
    impdir = TMP_AREA / f"impact-decls-{os.getpid()}-{_fx_counter}"  # OUTSIDE the fixture repo
    impdir.mkdir(exist_ok=True)
    owner = fx / "docs/owner.md"
    owner.write_text("# Owner\n\nlast_verified: 2026-01-01\nbody line\n", encoding="utf-8")
    other = fx / "docs/other.md"
    other.write_text("# Other\n", encoding="utf-8")
    _gitc(fx, "init", "-q")
    _gitc(fx, "add", "-A")
    _gitc(fx, "commit", "-qm", "base")
    base = subprocess.run(["git", "-C", str(fx), "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    try:
        # S1: unrelated change, fully declared → PASS
        (fx / "docs/unrelated.md").write_text("# New\n", encoding="utf-8")
        imp1 = impdir / "imp1.yaml"
        imp1.write_text("change: s1\nchanged_paths: [docs/unrelated.md]\ncanonical_owners: []\n",
                        encoding="utf-8")
        ok, probs = canonical_impact_lint.check(imp1, base, worktree=True, root=fx)
        report("impact: unrelated declared change passes (S1)", ok, str(probs))

        # S2: owner declared updated but not changed → FAIL (C2)
        imp2 = impdir / "imp2.yaml"
        imp2.write_text(
            "change: s2\nchanged_paths: [docs/unrelated.md, docs/owner.md]\n"
            "canonical_owners:\n  - {path: docs/owner.md, impact: updated}\n", encoding="utf-8")
        ok, probs = canonical_impact_lint.check(imp2, base, worktree=True, root=fx)
        report("impact: omitted impacted owner fails (S2)",
               (not ok) and any("C2" in p for p in probs), str(probs))

        # S3: timestamp-only change to the stale owner → FAIL (C4)
        owner.write_text("# Owner\n\nlast_verified: 2026-09-10\nbody line\n", encoding="utf-8")
        ok, probs = canonical_impact_lint.check(imp2, base, worktree=True, root=fx)
        report("impact: timestamp-only owner change fails (S3)",
               (not ok) and any("C4" in p for p in probs), str(probs))

        # S4 (control): substantive owner change → PASS
        owner.write_text("# Owner\n\nlast_verified: 2026-09-10\nbody line UPDATED\n", encoding="utf-8")
        ok, probs = canonical_impact_lint.check(imp2, base, worktree=True, root=fx)
        report("impact: substantive owner update passes (control)", ok, str(probs))

        # S5: non-trivial change with no declaration → FAIL (C5)
        (fx / "docs/a.md").write_text("a\n", encoding="utf-8")
        (fx / "docs/b.md").write_text("b\n", encoding="utf-8")
        (fx / "docs/c.md").write_text("c\n", encoding="utf-8")
        (fx / "docs/d.md").write_text("d\n", encoding="utf-8")
        ok, probs = canonical_impact_lint.check(None, base, worktree=True, root=fx)
        report("impact: non-trivial change w/o declaration fails (S5)",
               (not ok) and any("C5" in p for p in probs), str(probs))
    finally:
        _rmtree(fx)
        _rmtree(impdir)


# ------------------------------------------- planted stale-roadmap (defect 1)
def t_planted_defect1():
    fx = make_fixture({
        "docs/plans/active/charter.md": "# Charter\n",
        # the planted defect: a second stale VOID roadmap, D12 class (slice §5)
        "docs/skill-development/legacy-batch-roadmap.md":
            "# Legacy Batch Roadmap\n\n"
            "> **⛔ VOID / SUPERSEDED (2026-07-15).** Retired. "
            "Governing plan: [docs/plans/active/charter.md](../../plans/active/charter.md).\n",
        # an inbound reference treating it as current authority (the D12 pointer class)
        "docs/skill-development/index.md":
            "# Index\n\nCurrent build plan: [legacy-batch-roadmap.md](legacy-batch-roadmap.md) §2.\n",
    })
    # verify the fixture change was applied BEFORE scoring
    assert "VOID / SUPERSEDED" in (fx / "docs/skill-development/legacy-batch-roadmap.md").read_text(encoding="utf-8")
    archive_lint.ROOT = fx
    try:
        ok, probs = archive_lint.check_file(fx / "docs/skill-development/legacy-batch-roadmap.md")
        report("defect-1: planted stale roadmap detected AND named",
               (not ok) and any("R1" in p and "legacy-batch-roadmap" in p for p in probs), str(probs))
    finally:
        _rmtree(fx)


# --------------------------------------------------------------- register H2
def t_register_scoped():
    # frozen-corpus regression guard: the two existing registers live in the
    # byte-frozen evals/skills/results/ set (sha256-verified per slice); skipped
    # if a future checkout lacks them so the selftest stays repo-state independent
    for rel in ("evals/skills/results/batch2_5/research-chain/decision-register.md",
                "evals/skills/results/uncertainty-and-decision-manager/e2e/decision-register.md"):
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        ok, probs = register_check.check_file(p)
        report(f"register: existing {rel.split('/')[-1]} passes (frozen-corpus guard)", ok, str(probs))
    # planted: VERIFIED at E2 (HF-10)
    fx = make_fixture({"docs/decision-notes/decided/r.md": ""})
    reg = fx / "register.md"
    reg.write_text(
        "# R\n\n## Register\n\n```yaml\n"
        "- id: D-001\n  statement: s\n  status: VERIFIED\n  evidence: E2\n"
        "  source: x.md\n  disposition: supported\n```\n", encoding="utf-8")
    ok, probs = register_check.check_file(reg)
    report("register: planted VERIFIED-at-E2 entry caught",
           (not ok) and any("E2" in p for p in probs), str(probs))
    _rmtree(fx)


# ------------------------------------- markdown_links_check banner-aware (§9)
def t_links_banner_aware():
    import markdown_links_check as mlc
    fx = make_fixture({
        "docs/plans/active/charter.md": "# Charter\n",
        "docs/plans/archived/old-plan.md":
            "# Old Plan\n\n"
            "> **⛔ VOID / SUPERSEDED (2026-08-01).** Retired. Governing plan: "
            "[charter.md](../../plans/active/charter.md).\n",
        # planted: live doc links to the archived plan WITHOUT a historical label
        "docs/live-unlabeled.md":
            "# Live\n\nCurrent build plan: [old-plan.md](plans/archived/old-plan.md) §2.\n",
        # clean: labeled on its line
        "docs/live-labeled.md":
            "# Live\n\nSee [old-plan.md](plans/archived/old-plan.md) (frozen history, VOID 2026-08-01).\n",
        # clean: frozen source (eval corpus) may link unlabeled — historical evidence
        "tests/corpus/frozen-case.md":
            "# Case\n\nRef [old-plan.md](../../docs/plans/archived/old-plan.md)\n",
    })
    orig_root = mlc.ROOT
    mlc.ROOT = fx
    try:
        ok, probs = mlc.check_file(fx / "docs/live-unlabeled.md")
        report("links: unlabeled live→archived pointer caught (banner-aware, §5.2-4/§9)",
               (not ok) and any("archive-pointer" in p for p in probs), str(probs))
        ok, probs = mlc.check_file(fx / "docs/live-labeled.md")
        report("links: labeled live→archived pointer passes", ok, str(probs))
        ok, probs = mlc.check_file(fx / "tests/corpus/frozen-case.md")
        report("links: frozen-source link exempt (historical evidence)", ok, str(probs))
    finally:
        mlc.ROOT = orig_root
        _rmtree(fx)


if __name__ == "__main__":
    t_archive()
    t_supersession()
    t_decision_note()
    t_canonical_impact()
    t_planted_defect1()
    t_register_scoped()
    t_links_banner_aware()
    try:
        shutil.rmtree(TMP_AREA)
    except OSError:
        pass
    print(f"\n==> selftest_phase2_lints: {PASS} pass, {FAIL} fail")
    raise SystemExit(1 if FAIL else 0)
