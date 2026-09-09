#!/usr/bin/env python3
"""preflight.py — READ-ONLY pre-install / pre-run check for Research-Code-Docs.

Verifies the environment, the installed skill set, the deterministic checkers, L3
dependencies, and name/version conflicts, then prints a YAML summary and exits:

    0 = PASS      1 = WARN (read and accept; NOT full success)      2 = FAIL

This script writes NOTHING. Writability of the candidate-output area is probed with
os.access (no temp file is created). Run it from the workspace root after install:

    python scripts/preflight.py            # human + YAML
    python scripts/preflight.py --json      # machine (YAML block only)
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
MANIFEST = WORKSPACE / "release-manifest.yaml"
REGISTRY = WORKSPACE / "docs" / "skill-development" / "skills-registry.yaml"
SKILLS_DIR = WORKSPACE / ".agents" / "skills"
CHECKERS_DIR = WORKSPACE / "evals" / "skills" / "harness" / "checkers"
NAMED_CHECKERS = [
    "interface_check", "flow_state_check", "migration_map_check",
    "rewrite_provenance_check", "maintenance_impact_check",
]
RECOMMENDED_PY = (3, 11)
OK_PY = {(3, 11), (3, 12)}  # 3.11 recommended, 3.12 is the tested dev interpreter — both PASS
MIN_PY = (3, 10)

blocking: list[str] = []
warnings: list[str] = []
actions: list[str] = []


def _yaml():
    try:
        import yaml  # noqa
        return yaml
    except Exception:
        return None


def parse_frontmatter(text: str, yaml=None) -> dict | None:
    """Line-based front-matter parse, matching Claude Code's lenient loader.

    We deliberately do NOT yaml.safe_load the block: a skill's `description:` is a long
    single line that legitimately contains ': ' (colon-space) sequences, which strict YAML
    rejects ("mapping values are not allowed here") even though Claude Code accepts it. We
    only need the flat scalar keys (name, disable-model-invocation), so we split each line
    on its first colon. `yaml` is accepted for call-site compatibility and ignored.
    """
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    fm: dict = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        low = val.lower()
        val = True if low == "true" else (False if low == "false" else val)
        fm.setdefault(key, val)  # first (top-level) occurrence wins
    return fm


# --------------------------------------------------------------------------- env
def check_environment(yaml) -> dict:
    env = {}
    v = sys.version_info
    env["python_version"] = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < MIN_PY:
        blocking.append(f"Python {v.major}.{v.minor} is below the minimum {MIN_PY[0]}.{MIN_PY[1]}.")
        env["python"] = "FAIL"
    elif (v.major, v.minor) in OK_PY:
        env["python"] = "OK"
    else:
        warnings.append(f"Python {v.major}.{v.minor} meets the minimum but the tested interpreters are 3.11/3.12.")
        env["python"] = "WARN"
    env["pyyaml"] = "OK" if yaml is not None else "FAIL"
    if yaml is None:
        blocking.append("PyYAML is not importable (the only runtime dependency). Run: uv pip install pyyaml")
    # git (optional)
    from shutil import which
    env["git"] = "present" if which("git") else "absent-optional"
    if not which("git"):
        warnings.append("Git not found: source-hash / rollback guarantees are weaker without it (optional).")
    # workspace readable
    env["workspace"] = str(WORKSPACE)
    env["workspace_readable"] = os.access(WORKSPACE, os.R_OK)
    # candidate output area writable (read-only probe: os.access, no file created)
    cand = WORKSPACE / "results"
    probe = cand if cand.exists() else WORKSPACE
    env["candidate_output_writable"] = bool(os.access(probe, os.W_OK))
    if not env["candidate_output_writable"]:
        warnings.append(f"Candidate-output area may not be writable: {probe}")
    return env


# ------------------------------------------------------------------------ skills
def check_skills(yaml) -> dict:
    out = {"declared": 0, "present": 0, "manual_only": 0, "issues": []}
    if yaml is None or not MANIFEST.exists():
        blocking.append("Cannot read release-manifest.yaml (or PyYAML missing).")
        return out
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    man_skills = {s["name"]: s for s in manifest.get("skills", [])}
    out["declared"] = len(man_skills)

    reg_versions = {}
    if REGISTRY.exists():
        reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
        for e in reg.get("skills", []):
            if isinstance(e, dict) and "name" in e and "version" in e:
                reg_versions[e["name"]] = str(e["version"])

    for name, mspec in sorted(man_skills.items()):
        skill_md = SKILLS_DIR / name / "SKILL.md"
        if not skill_md.exists():
            blocking.append(f"Skill missing on disk: .agents/skills/{name}/SKILL.md")
            out["issues"].append(f"{name}: MISSING")
            continue
        out["present"] += 1
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text, yaml)
        if fm is None:
            blocking.append(f"{name}: SKILL.md front-matter is unparseable.")
            out["issues"].append(f"{name}: BAD_FRONTMATTER")
            continue
        # disable-model-invocation must be true (release posture)
        dmi = fm.get("disable-model-invocation")
        if dmi is True:
            out["manual_only"] += 1
        else:
            blocking.append(f"{name}: disable-model-invocation is {dmi!r}, expected true (manual-only posture).")
            out["issues"].append(f"{name}: NOT_MANUAL_ONLY")
        # no auto_trigger: true anywhere in the file
        if re.search(r"auto_trigger:\s*true", text, re.I):
            blocking.append(f"{name}: found 'auto_trigger: true' in SKILL.md (release posture requires false).")
            out["issues"].append(f"{name}: AUTO_TRIGGER_TRUE")
        # version cross-check: manifest vs registry vs SKILL.md comment
        man_v = str(mspec.get("version"))
        reg_v = reg_versions.get(name)
        if reg_v and reg_v != man_v:
            blocking.append(f"{name}: manifest version {man_v} != registry version {reg_v} (integrity).")
            out["issues"].append(f"{name}: VERSION_MANIFEST_REGISTRY")
        m = re.search(r"^skill_version:\s*(.+)$", text, re.M)
        sk_v = m.group(1).strip() if m else None
        if sk_v is None:
            warnings.append(f"{name}: no skill_version line found in SKILL.md (secondary source).")
        elif sk_v != man_v:
            warnings.append(f"{name}: SKILL.md skill_version {sk_v} != manifest {man_v}.")
    if out["present"] != out["declared"]:
        actions.append("Some manifest skills are missing; re-run install_workspace.py --force or fix the install.")
    if out["manual_only"] != out["present"]:
        actions.append("A skill is not manual-only; do NOT proceed until every skill is disable-model-invocation:true.")
    return out


# -------------------------------------------------------------------- write-scope
def check_write_scope(yaml) -> dict:
    out = {"destructive_flags": []}
    if yaml is None or not REGISTRY.exists():
        return out
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    man = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"skills": []}
    man_names = {s["name"] for s in man.get("skills", [])}
    for e in reg.get("skills", []):
        if not (isinstance(e, dict) and e.get("name") in man_names):
            continue
        ws = e.get("write_scope") or {}
        for flag in ("may_move", "may_delete", "may_overwrite"):
            if ws.get(flag) is True:
                out["destructive_flags"].append(f"{e['name']}.{flag}=true")
                blocking.append(f"{e['name']}: write_scope.{flag}=true violates the non-destructive release posture.")
        if e.get("auto_trigger") is True:
            blocking.append(f"{e['name']}: registry auto_trigger=true (release posture requires false).")
    return out


# ---------------------------------------------------------------------- checkers
def check_checkers() -> dict:
    out = {"named_checkers": {}, "runner": "unknown"}
    if not CHECKERS_DIR.exists():
        blocking.append(f"Checkers directory missing: {CHECKERS_DIR}")
        out["runner"] = "MISSING"
        return out
    sys.path.insert(0, str(CHECKERS_DIR))
    try:
        import run_checks  # transitively imports all checker modules under this interpreter
    except Exception as ex:  # pragma: no cover
        blocking.append(f"run_checks.py failed to import (checkers not runnable): {ex!r}")
        out["runner"] = "IMPORT_FAIL"
        return out
    out["runner"] = "importable"
    for name in NAMED_CHECKERS:
        mod = getattr(run_checks, name, None)
        if mod is not None and callable(getattr(mod, "check_file", None)):
            out["named_checkers"][name] = "OK"
        else:
            out["named_checkers"][name] = "FAIL"
            blocking.append(f"Checker {name} missing or has no check_file().")
    # functional smoke: run the runner on one real doc (read-only); we only assert it executes
    try:
        probe = CHECKERS_DIR.parent / "canonical-source-map.md"
        if probe.exists():
            rep = run_checks.run(probe)
            out["runner"] = "runnable" if isinstance(rep, dict) and "results" in rep else "ODD_OUTPUT"
    except Exception as ex:
        blocking.append(f"run_checks.run() raised on a real doc: {ex!r}")
        out["runner"] = "RUN_FAIL"
    return out


# ------------------------------------------------------------------ L3 + conflicts
def check_l3_and_conflicts(yaml) -> tuple[dict, dict]:
    l3 = {"declared_in_registry": 0, "classification": "version-unknown (user-local; live-loader not probed)",
          "required_for_supported_flow": 0, "names": []}
    conflicts = {"duplicate_skill_dirs": [], "notes": []}
    if yaml is not None and REGISTRY.exists():
        reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
        ex = reg.get("existing_installed", []) or []
        l3["declared_in_registry"] = len(ex)
        l3["names"] = [e.get("name") for e in ex if isinstance(e, dict)]
    # the supported documentation-refactor dry-run flow uses only in-workspace atoms -> 0 required L3
    conflicts["notes"].append(
        "Supported documentation-refactor (dry-run+candidate) needs no L3 skill. Research adapters ship "
        "disable-model-invocation:true, so an installed lit-review/research stack cannot co-fire.")
    # duplicate / mismatched skill dir vs SKILL.md name
    if SKILLS_DIR.exists() and yaml is not None:
        for d in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
            md = d / "SKILL.md"
            if md.exists():
                fm = parse_frontmatter(md.read_text(encoding="utf-8", errors="replace"), yaml)
                if fm and fm.get("name") and fm["name"] != d.name:
                    conflicts["duplicate_skill_dirs"].append(f"{d.name} (front-matter name={fm['name']})")
                    warnings.append(f"Skill dir '{d.name}' declares name '{fm['name']}' (mismatch).")
    return l3, conflicts


def main(argv: list[str]) -> int:
    json_only = "--json" in argv[1:]
    yaml = _yaml()
    env = check_environment(yaml)
    skills = check_skills(yaml) if yaml else {"declared": 0, "present": 0}
    ws = check_write_scope(yaml) if yaml else {"destructive_flags": []}
    checkers = check_checkers()
    l3, conflicts = check_l3_and_conflicts(yaml)

    status = "FAIL" if blocking else ("WARN" if warnings else "PASS")
    if status == "PASS":
        actions.append("Proceed: read QUICKSTART.md and run documentation-refactor manually.")
    elif status == "WARN":
        actions.insert(0, "Read each warning and accept it explicitly before proceeding (WARN is not full success).")
    else:
        actions.insert(0, "Do NOT proceed. Resolve every blocking error, then re-run preflight.")

    report = {"preflight": {
        "status": status,
        "release_version": (WORKSPACE / "VERSION").read_text(encoding="utf-8").strip() if (WORKSPACE / "VERSION").exists() else "unknown",
        "environment": env,
        "skills": skills,
        "write_scope": ws,
        "dependencies_L3": l3,
        "checkers": checkers,
        "conflicts": conflicts,
        "warnings": warnings,
        "blocking_errors": blocking,
        "recommended_actions": actions,
    }}

    if not json_only:
        print(f"# preflight — Research-Code-Docs {report['preflight']['release_version']}")
        print(f"# status: {status}   (0=PASS 1=WARN 2=FAIL)\n")
    if yaml is not None:
        print(yaml.safe_dump(report, allow_unicode=True, sort_keys=False))
    else:
        # PyYAML missing: emit a minimal plain summary
        print(f"status: {status}")
        print(f"blocking_errors: {blocking}")
        print(f"warnings: {warnings}")
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[status]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
