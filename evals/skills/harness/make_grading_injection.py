#!/usr/bin/env python3
"""
make_grading_injection.py — assemble ISOLATED prompts for a task-quality (grading) eval.

We never install the skill to test it. A grading eval runs by injecting the skill + references + the
TARGET DOCUMENT into a FRESH sub-agent that has none of the main session's project context. This closes
the v0.2 false-pass root cause: the evaluator ran in the main session with full eoopt context and could
"fill in" the document's gaps.

Three roles, deliberately different context envelopes:

  --role evaluator : SKILL.md + hard-fail.md + rubric.md + canonical-source-map.md + the target bytes.
                     Must run the checkers, walk ALL gates, emit the KEY=VALUE verdict block, report FILES_READ.
  --role reader    : ONLY the target bytes + the two-layer reader questions. Gets NEITHER the rubric NOR
                     hard-fail (that would bias it toward the grading criteria). This is a deliberate
                     divergence from make_batch.py / make_injection.py, which always inject SKILL.md.
  --role meta      : the human annotation + the evaluator's structured output. Judges whether the
                     evaluator caught the expected blockers/majors. No target, no skill.

Isolation caveat (honest): true filesystem sandboxing is not available here, so "isolation" = fresh
sub-agent (no main-session history) + a required read-set audit (FILES_READ) + the UNVERIFIED-forcing
rule (unopened cited sources -> SOURCE_COVERAGE penalty -> FACTUAL_VALIDITY=UNVERIFIED).

Usage:
  python make_grading_injection.py <skill> <target.md> --role evaluator [--no-checkers]
  python make_grading_injection.py <skill> <target.md> --role reader
  python make_grading_injection.py <skill> <target.md> --role meta --annotations <ann.md> --evaluator-output <out.txt>
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "evals" / "skills" / "harness"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


EVALUATOR_CONTRACT = """\
You are the `documentation-quality-evaluator` skill running as a TERMINAL QUALITY GATE, in a FRESH
process. You have NO knowledge of this project beyond the files pasted below. You MUST NOT use any
outside, prior-conversation, or assumed project knowledge to fill gaps in the target document — if the
document does not say it, it is not established. Filling gaps from outside knowledge is the exact bug
this harness exists to prevent.

Follow the injected SKILL.md workflow EXACTLY. In particular:
- Run the deterministic checkers on the target and PASTE the JSON: `python evals/skills/harness/checkers/run_checks.py <TARGET> --json`.
- Walk EVERY applicable hard gate (HF-1..HF-15). Collect ALL blockers. Do NOT stop at the first.
- A met gate is a BLOCKER and may not be downgraded to MAJOR/MINOR.
- Do NOT predict or imply a re-eval PASS while any structural gate (HF-13/14a/14b/15) or non-compensatory
  dimension is failing or unassessed.
- Separate DOCUMENT_QUALITY (judgeable from the doc) from FACTUAL_VALIDITY (needs opening the cited
  sources). If you cannot open a cited source, it is UNVERIFIED — do NOT report HF-12 verified/PASS.
- End with the machine-parseable verdict block, verbatim keys:
  DOCUMENT_QUALITY / FACTUAL_VALIDITY / READER_TEST / CHECKER_STATUS / SOURCE_COVERAGE / CONFIDENCE /
  BLOCKERS=[...] / FILES_READ=[...]
"""

READER_CONTRACT = """\
You are a FRESH READER. You have ONLY the document below — no other context, no grading rubric, no
author intent, no project background. Answer each question honestly and literally FROM THE DOCUMENT
ALONE. If the document does not let you answer, say "CANNOT ANSWER — <why>". Do NOT be charitable and do
NOT guess; a gap you have to fill is a finding about the document, not your failure.

Answer these two layers:

LAYER 1 — comprehension + location
 1. What is the goal / target of this work?
 2. What is the SINGLE primary responsibility of this document? Who is its target reader?
 3. What is the current state (FACT vs UNKNOWN), and WHERE is the canonical source of that state?
 4. Where are the key terms defined? Where do the related ADR / spec / experiment reports live?
 5. What are the open questions?

LAYER 2 — execution + refutation
 6. What is the NEXT immediately-executable piece of work, and HOW will we know it is done (its DoD)?
 7. Which methods/algorithms are DECIDED vs merely CANDIDATE?
 8. Which load-bearing claims LACK support (no handle, or only a topically-related source)?
 9. Which facts will go STALE fastest?
10. Which sections do NOT serve the document's stated goal?
11. If the gating/precondition experiment FAILS, how does the route change?
"""

META_CONTRACT = """\
You are a META-GRADER. You are given (A) the human annotation of the defects this target is KNOWN to
contain, and (B) the evaluator's structured output. Decide, per expected blocker/major, whether the
evaluator caught it. Then report:
- severe-issue recall = (expected BLOCKER/MAJOR the evaluator caught) / (total expected BLOCKER/MAJOR)
- false-pass = did the evaluator PASS (or predict/imply a re-eval PASS) a doc that should FAIL? (the
  "FAIL only on a trivial gate while calling the doc substantively good / predicting PASS" pattern
  COUNTS AS a false-pass even if the literal verdict was FAIL)
- blocker-precision = (evaluator BLOCKERs that are real) / (evaluator BLOCKERs)
Output a short table + the three numbers + PASS/FAIL of the evaluator itself against the admission bar
(recall >= 90%, false-pass = 0).
"""


REVIEWER_CONTRACT = """\
You are an INDEPENDENT REVIEWER setting a gold label for a documentation test corpus. You have ONLY the
document below, plus its declared artifact_type and evaluation profile. You do NOT have the skill under
test, its hard-fail catalog, or its rubric — and you must not reconstruct them. Judge the document on
its merits for its stated type and profile, in your OWN words.

You are NOT the evaluator-under-test. Do not emit that skill's KEY=VALUE block. Answer these only:

1. TYPE & PURPOSE — what is this document's single primary job? Is it self-contained for that job?
2. QUALITY_BAND — holistic quality of the document for its type/profile:
   PASS (good), PARTIAL (mostly good but has a real defect), or FAIL (fundamentally deficient).
3. GATE_RECOMMENDATION — should this be allowed to proceed in a release/merge workflow?
   ALLOW, BLOCK (a defect must be fixed before it proceeds), or INCOMPLETE (cannot tell without more
   info/sources). NOTE: these are two DIFFERENT axes — a document can be PARTIAL quality yet still BLOCK
   the gate on one defect; an honestly-labeled hypothesis can be PASS quality AND ALLOW.
4. TOP DEFECTS — the 1–5 most serious issues (free text). For each, tag ONE category from:
   mixed-responsibilities | state-contradiction | volatile-in-stable | non-executable-milestone |
   unsupported-claim | not-reproducible | missing-rationale | not-actionable | context-dependent |
   stale | other
5. PROVENANCE NOTE — is anything missing that only matters under a `controlled` (not `external`)
   profile? (e.g. local traceability front-matter.)
6. CONFIDENCE — HIGH / MEDIUM / LOW.

End with a compact block:
QUALITY_BAND=<PASS|PARTIAL|FAIL>
GATE_RECOMMENDATION=<ALLOW|BLOCK|INCOMPLETE>
DEFECT_TAGS=[...]
CONFIDENCE=<HIGH|MEDIUM|LOW>
"""


def build(role: str, skill: str, target: Path, opts: dict) -> str:
    skill_md = ROOT / ".claude" / "skills" / skill / "SKILL.md"
    parts: list[str] = []
    if role == "evaluator":
        parts += [EVALUATOR_CONTRACT,
                  "\n===== SKILL DEFINITION (injected) =====\n", _read(skill_md),
                  "\n===== hard-fail.md =====\n", _read(HARNESS / "hard-fail.md"),
                  "\n===== rubric.md =====\n", _read(HARNESS / "rubric.md"),
                  "\n===== canonical-source-map.md =====\n", _read(HARNESS / "canonical-source-map.md"),
                  f"\n===== TARGET (path: {target.as_posix()}) =====\n", _read(target),
                  "\n===== END TARGET =====\nProduce the full quality report now, ending with the verdict block.\n"]
    elif role == "reader":
        parts += [READER_CONTRACT,
                  f"\n===== DOCUMENT (the ONLY thing you may use) =====\n", _read(target),
                  "\n===== END DOCUMENT =====\nAnswer all 11 questions now.\n"]
    elif role == "reviewer":
        meta = f"artifact_type: {opts.get('artifact_type','(infer it)')}\nprofile: {opts.get('profile','(none given)')}\n"
        parts += [REVIEWER_CONTRACT,
                  f"\n===== DECLARED TYPE & PROFILE =====\n", meta,
                  f"\n===== DOCUMENT (the ONLY thing you may use) =====\n", _read(target),
                  "\n===== END DOCUMENT =====\nProduce your independent review now, ending with the block.\n"]
    elif role == "meta":
        ann = Path(opts["annotations"]); evo = Path(opts["evaluator_output"])
        parts += [META_CONTRACT,
                  "\n===== HUMAN ANNOTATION (expected defects) =====\n", _read(ann),
                  "\n===== EVALUATOR OUTPUT =====\n", _read(evo),
                  "\n===== END =====\nProduce the meta-grade now.\n"]
    else:
        raise SystemExit(f"unknown role: {role}")
    return "".join(parts)


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    skill, target = args[0], Path(args[1])
    role = argv[argv.index("--role") + 1] if "--role" in argv else "evaluator"
    opts = {}
    if "--annotations" in argv:
        opts["annotations"] = argv[argv.index("--annotations") + 1]
    if "--evaluator-output" in argv:
        opts["evaluator_output"] = argv[argv.index("--evaluator-output") + 1]
    if "--artifact-type" in argv:
        opts["artifact_type"] = argv[argv.index("--artifact-type") + 1]
    if "--profile" in argv:
        opts["profile"] = argv[argv.index("--profile") + 1]
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    print(build(role, skill, target, opts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
