# evals/skills — Evaluation harness

<!--
generated_by_skill: (manual, Phase-1 governance authoring)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents: [docs/skill-development/quality-control-plan.md, docs/skill-development/creation-roadmap.md]
status: DECIDED (v0.1 harness layout)
last_verified: 2026-07-30T09:47:06Z
-->

This tree holds the **evaluation suite** for the research-software documentation Skills system.
It is **workspace-only** — nothing here installs or triggers a skill in the live loader (the
deliberate Mode B user-level test install of 2026-08-07 is a separate, documented act — see
`docs/skill-development/README.md`, "Recorded install state").

## Why a harness at all

The working constraint is: **do not install a skill to test it.** So every eval works by
**injecting a skill's `SKILL.md` body into a fresh sub-agent's prompt**, feeding it a case input,
and scoring the result. Deterministic checks run first (hard gates); a model grader
(`documentation-quality-evaluator`) runs only if the hard gates pass.

## Layout

```text
evals/skills/
├── README.md                ← this file (case schema + how to run)
├── harness/
│   ├── rubric.md            ← the 8-dimension soft rubric + anchors (grader loads this)
│   ├── hard-fail.md         ← HF-1..HF-11 catalog (grader + checkers load this)
│   ├── checkers/            ← deterministic checkers (Python stdlib + pyyaml)
│   │   ├── frontmatter_check.py
│   │   ├── status_vocab_check.py
│   │   ├── markdown_links_check.py
│   │   ├── placeholders_check.py
│   │   └── run_checks.py    ← runs all checkers over a path; prints JSON
│   ├── score_trigger.py     ← scores a filled trigger-results file vs expected labels
│   └── make_injection.py    ← builds the sub-agent injection prompt for a case
├── trigger/<skill>.yaml     ← 10 should-trigger + 10 should-not + 5 short-ambiguous
├── conflict/<skill>.yaml    ← 5 conflict cases (defer/hand-off is correct)
├── multi-turn/<skill>.yaml  ← 3 multi-turn cases
├── task-quality/<skill>.yaml← ≥2 real historical tasks + rubric anchors
├── reader-tests/<skill>.yaml← no-context reader questions for produced artifacts
├── regression/              ← previously-failed cases, re-run after any edit
└── results/<skill>/<date>.md← timestamped run outputs + verdicts
```

## Case schema (all `*.yaml` case files)

```yaml
skill: <skill-name>
skill_version: <semver>          # the version the cases target
dataset_version: <int>           # bump when cases change; prevents overfitting
cases:
  - id: <skill>-<set>-<nn>       # e.g. dqe-trig-01
    set: should-trigger | should-not | short-ambiguous | conflict | multi-turn | task-quality | reader
    real: true|false             # true = drawn from an actual project in this environment
    input: |                     # what the user says / the situation
      ...
    context: |                   # optional: files present, prior turns (for multi-turn/real)
      ...
    expected:                    # what "correct" looks like
      decision: engage | decline | route            # for trigger/conflict sets
      route_to: <skill or null>                      # when decision == route/decline
      must_mention: [ ... ]                          # substrings the justification should contain
      must_not: [ ... ]                              # e.g. "does not start interviewing"
      hard_fails_guarded: [HF-3, HF-8]               # for task-quality: which HFs this case probes
    notes: |
      why this case exists / which conflict-matrix row it maps to
```

## How to run (isolation-respecting)

1. **Validate + deterministic checks** (no model):
   ```bash
   .venv/Scripts/python.exe evals/skills/harness/checkers/run_checks.py <path-to-doc-or-dir>
   ```
2. **Trigger eval** — for each case, build an injection prompt and spawn a sub-agent:
   ```bash
   .venv/Scripts/python.exe evals/skills/harness/make_injection.py trigger/<skill>.yaml <case-id>
   ```
   The orchestrator (this session) spawns an `Explore`/general sub-agent with that prompt,
   collects its `decision/route`, writes them into a results file, then:
   ```bash
   .venv/Scripts/python.exe evals/skills/harness/score_trigger.py trigger/<skill>.yaml <results.json>
   ```
3. **Task-quality / reader-test** — a sub-agent runs the skill to produce an artifact;
   a grader sub-agent (running `documentation-quality-evaluator`) scores it with `rubric.md` + `hard-fail.md`;
   `run_checks.py` provides the hard-gate pre-filter.
4. **Record** the verdict + skill version + timestamp under `results/<skill>/<date>.md`.

## Pass targets

Per `docs/skill-development/quality-control-plan.md` §10. In short: trigger ≥ 9/10 engage and
≥ 9/10 decline; conflict cases all defer correctly; no hard-fail; soft ≥ 75 with no dimension < 50.
`documentation-quality-evaluator` must clear its bar before Batch 2 starts.
