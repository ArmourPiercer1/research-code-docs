---
generated_by_skill: project-state-reconstructor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch3/scientific-workspace-reconstruction/inventory-report.md, evals/skills/harness/]
artifact_type: project-state-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Recovered state of the evals/skills/harness/ eval-harness code workspace (21 .py + 3 .md), from the upstream inventory + read-only source verification. Separates FACT / UNKNOWN / STALE / CANDIDATE. EXCLUDES: executing or importing any module (would regenerate .pyc — a modification), the repo-root dependency manifest, and design of any target structure (architect's job)."
facts: "13 rows — see 'What is present & structured-to-run (FACT)'. Max evidence E2 (present + wired/coherent in source); NO E3 (nothing executed)."
hypotheses: "3 — see 'Believed but unverified (HYPOTHESIS)': (H1) Python-3.12 + PyYAML stack; (H2) make_batch.py is the current prompt-builder; (H3) score_all.py has retired score_trigger.py."
open_questions: "5 UNKNOWN(resolve) + 2 ASK-HUMAN + 2 superseded-CANDIDATE pairs — see 'UNKNOWNs (+ how to resolve)', 'ASK-HUMAN questions', and 'Overlap / possible-superseded (CANDIDATE)'. Never 'none' — the harness was not executed."
evidence_level: "E2 (static structure only: files present + imports/call-sites coherent in source. This isolated run may not execute or import, so E3 'runs / passes' is WITHHELD on every row — 'structured to run' is asserted, 'runs' is not)."
next_handoff: goal-scope-and-workflow-elicitor
handoff_requirements: "Consumer needs: (1) the FACT/UNKNOWN split below and that MAX evidence is E2 — no runtime (E3) fact exists, so no downstream claim may say the harness 'runs' or 'passes'; (2) the register_check.py orphan is RESOLVED as intentional-standalone (owned by the uncertainty-and-decision-manager flow, u-d-m SKILL.md:113), NOT an unwired oversight and NOT a delete/cleanup target; (3) test status is UNKNOWN (no test suite in scope); (4) 2 superseded-CANDIDATE pairs are unresolved and blocked on a caller/orchestration check (ASK-HUMAN-1/2). UNKNOWN-1 (does run_checks.py execute green) blocks any future E3 progress claim."
status: FACT/UNKNOWN/STALE/CANDIDATE separated below
---

# State Report — `evals/skills/harness/` (skill-eval harness)

Facts are **recovered, not inherited**. The upstream inventory's classifications are treated as *candidates*; each FACT below was re-verified by **reading source** (never by execution). This run is **READ-ONLY** and executes/imports **nothing** (importing would write `.pyc` cache = a modification).

## Evidence ladder used (and why it is capped at E2 here)

| level | meaning | available in this run? |
|---|---|---|
| E0 | named/claimed only (a doc says so) | yes |
| E1 | file present on disk | yes (glob) |
| **E2** | **present AND structurally coherent in source** (imports resolve in-source; call-sites require the interface; entry-point scaffolding present) — **"structured to run"** | **yes — this is the MAX** |
| E3 | observed to run (captured command output / passing test) | **WITHHELD** — no execution permitted |
| E4/E5 | validated / reproduced | WITHHELD |

> **"Structured to run" ≠ "runs."** Every FACT row is E2: the code is present and wired coherently *in source*. Whether it executes green is **UNKNOWN** without running it (see UNKNOWNs).

## Inventory (read-only)

- **Entry points (20 of 21 `.py`):** aggregator `checkers/run_checks.py`; top-level builders `make_injection.py`, `make_batch.py`, `make_grading_injection.py`; scorers `score_trigger.py`, `score_all.py`, `score_grading.py`; validator `validate_cases.py`; 12 standalone checker CLIs under `checkers/` (the 11 wired + `register_check.py`). Each carries `def main(argv)->int` + `if __name__=="__main__": raise SystemExit(main(sys.argv))`.
- **Shared helper (1 of 21):** `checkers/_textutils.py` — no `main`/`__main__` (not an entry point).
- **Build/deps:** none under `harness/` (no `pyproject.toml`/`requirements*`/`Makefile`/`Dockerfile`/`.sh`). `import yaml` in every builder/scorer. Manifest is at repo root — out of scope.
- **Tests:** none in scope (no `test_*.py`/`*_test.py`/`conftest.py`/`pytest.ini` under `harness/`).
- **Docs:** `hard-fail.md`, `rubric.md`, `canonical-source-map.md` (all `status: DECIDED`). No `README.md`.
- **Generated (not evidence):** `harness/__pycache__/` + `checkers/__pycache__/` (21 `.pyc`) — NOT opened/imported (evidence hygiene + read-only).

## What is present & structured-to-run (FACT)

Max evidence **E2** (static structure). No row claims execution.

| # | capability (structured to run) | evidence (`file:line`) | E |
|---|---|---|---|
| F1 | `run_checks.py` is an entry point: `main(argv)->int` + `__main__` guard; exits non-zero on HARD fail | `checkers/run_checks.py:125`, `:139-140`, `:136` (`return 1 if report["hard_fail"]`) | E2 |
| F2 | `run_checks.py` wires **exactly 11** checker modules via in-source imports | `checkers/run_checks.py:30-40` (11 `import` lines) | E2 |
| F3 | …classified HARD=2, ADVISORY=4, SIGNAL=5 (=11) | HARD `:42`; ADVISORY `:43-44`; SIGNAL `:46-52` | E2 |
| F4 | aggregator drives each module through the `check_file(path)->(ok, problems)` contract | `checkers/run_checks.py:79`, `:89`, `:94` (`mod.check_file(f)`) | E2 |
| F5 | the 11 wired modules therefore each expose `check_file` (call-site requires it; imports resolve in-source) | derived from F2+F4; bodies NOT deep-read (see U3) | E2 |
| F6 | `register_check.py` is an entry point structured to run: `check_file` + `main` + `__main__` | `checkers/register_check.py:42`, `:87`, `:102-103` | E2 |
| F7 | **`register_check.py` is NOT wired into `run_checks.py`** — absent from imports and from all three lists | absent at `checkers/run_checks.py:30-40` and `:42-52` | E2 |
| F8 | `register_check.py` **is a standalone "Scripts to run" entry of the `uncertainty-and-decision-manager` flow** (validates a `decision-register.md`) | `.claude/skills/uncertainty-and-decision-manager/SKILL.md:113` | E2 |
| F9 | 4 more top-level entry points present + structured to run (`main`+`__main__`) | `make_injection.py:40,79-80`; `make_batch.py:69,89-90`; `score_trigger.py:58,90-91`; `score_all.py:61,98-99` | E2 |
| F10 | `_textutils.py` is the shared helper — the 1 `.py` with **no** entry point (regex/section helpers) | `checkers/_textutils.py:37` (`mask_noise`), `:46` (`line_of`), `:61` (`split_sections`); no `main`/`__main__` | E2 |
| F11 | `score_all.py` is a **functional superset** of `score_trigger.py` (loads trigger+conflict by skill-name; adds conflict route-list + deliverable-C gate) | `score_all.py:66`, `:88-94` vs `score_trigger.py:58-63`, `:82-85` | E2 |
| F12 | no build manifest / no test file under `harness/`; `import yaml` present | glob `harness/**` = only `.py`+`.md`; glob `harness/**/test_*.py` = none; `make_injection.py:18` | E2 |
| F13 | external path root resolves: sibling case dirs + a target `SKILL.md` exist on disk (the `ROOT=parents[3]` assumption) | glob `evals/skills/{trigger,conflict,task-quality}/*.yaml` (all 3 populated); `.claude/skills/uncertainty-and-decision-manager/SKILL.md` read | E2 |

*(F9 covers the 4 top-level entry points I read in full. The other 3 top-level scripts — `make_grading_injection.py`, `score_grading.py`, `validate_cases.py` — are present on disk (E1, glob) but their bodies were not read this run; their entry-point structure is an inventory signal, not re-verified here.)*

## Orphan resolution — `register_check.py` (deliverable b)

**Verdict: RESOLVED — intentional standalone, not an unwired oversight; NOT a delete candidate.**

- **FACT (E2):** it is **not** imported or registered by the aggregator `run_checks.py` (F7). So "unwired *by the harness aggregator*" is confirmed true — but that is by design, not neglect.
- **FACT (E2):** its **real caller is named**: `.claude/skills/uncertainty-and-decision-manager/SKILL.md:113` lists `register_check.py <decision-register>` as a "Scripts to run" entry (directly above `run_checks.py` at `:114`). The two checkers are deliberately split: `run_checks.py` gates generic Markdown artifacts; `register_check.py` validates the `decision-register.md` artifact for that one skill's flow (repo-wide grep also finds it in `skills-registry.yaml`, snapshot `checker-manifest.yaml`s, and `task-quality/uncertainty-and-decision-manager.yaml`).
- **UNKNOWN (not E3):** whether that invocation has **ever actually run** is unverified — the registry records its task_quality run as **pending** (`docs/skill-development/skills-registry.yaml:163`: "task_quality (register_check) runs pending"). "Named as a script to run" is E2; "runs green" would be E3 and is withheld → see UNKNOWN-2.

## What is tested (deliverable c)

**Honest verdict: UNKNOWN — no unit-test suite in scope; "structured to self-check" ≠ "tested."**

- **FACT (E2):** zero `test_*.py`/`*_test.py`/`conftest.py`/`pytest.ini` under `harness/` (glob empty; full `.py` glob = 21 files, none named `test_*`).
- The `__main__` block on each checker is a **CLI self-check** (run `check_file` on an argv-supplied path, print PASS/FAIL) — an entry point, **not** an assertion-based unit test with fixtures. It does not constitute a test suite.
- The only in-source hint of a validation corpus is `run_checks.py:22` + `:54`, which reference a `fixtures/` dir of "intentionally-bad eval seeds" that directory scans skip — but **no `fixtures/` exists under `harness/`** (glob), so any such corpus is external → UNKNOWN-4.
- Therefore: **no pass/fail is claimed for anything.** Test status is UNKNOWN pending the resolve-actions below.

## Real progress (written → runs → tested → validated)

- **Written:** FACT — 21 `.py` present; 20 structured as entry points, 1 shared helper; aggregator wires 11 checkers coherently in source (F1-F13).
- **Runs:** UNKNOWN — nothing executed this run; the `.pyc` caches hint prior *import* but a `.pyc` is not runtime proof (evidence hygiene). No E3.
- **Tested:** UNKNOWN — no suite in scope (see above).
- **Validated:** UNKNOWN — n/a in scope.

## Believed but unverified (HYPOTHESIS)

| id | claim | why unverified |
|---|---|---|
| H1 | Stack = Python 3.12 + PyYAML | signals only (`cpython-312` `.pyc` tag; `import yaml`); the declaring manifest is at repo root, out of scope → confirm, don't inherit |
| H2 | `make_batch.py` is the current prompt-builder (make_injection older) | both are standalone; no `harness/` file imports either; "later/current" needs a caller check (ASK-HUMAN-1) |
| H3 | `score_all.py` has retired `score_trigger.py` | F11 proves *superset*, which is necessary-not-sufficient for "retired"; no caller evidence in scope (ASK-HUMAN-2) |

## Overlap / possible-superseded (CANDIDATE — not confirmed STALE)

**Confirmed STALE: none in scope.** (Classic STALE = a doc claim contradicted by code; none found. Supersession of a near-duplicate needs a caller/execution check this run cannot do, so these stay CANDIDATE, not STALE.)

| pair | relationship (FACT) | supersession verdict |
|---|---|---|
| `make_injection.py` ↔ `make_batch.py` | different granularity: `make_injection` = one-case→one-prompt + `--skill-md` override (`make_injection.py:55-59`); `make_batch` = all trigger+conflict cases→one prompt + OTHER-skills roster (`make_batch.py:17-41,75`) | **CANDIDATE** — either could be current; not decidable in scope → ASK-HUMAN-1 |
| `score_trigger.py` ↔ `score_all.py` | `score_all` ⊇ `score_trigger` (superset, F11) | **CANDIDATE-superseded** (leans: `score_trigger` retired) — but no caller confirms retirement → ASK-HUMAN-2 |

## UNKNOWNs (+ how to resolve) (deliverable d)

Each carries a concrete resolve-action. None may be defaulted to done/false.

| id | unknown | why it matters | how to resolve (read/command) |
|---|---|---|---|
| U1 | Does `run_checks.py` execute green end-to-end (all 11 checkers import + run)? | blocks any E3 "the harness runs" claim | run `python evals/skills/harness/checkers/run_checks.py <a>.md --json` from repo root; expect exit 0/1, not a traceback |
| U2 | Does `register_check.py` run green on a real `decision-register.md`? (registry says its run is *pending*) | confirms the orphan's caller actually works | run `python evals/skills/harness/checkers/register_check.py <decision-register.md>` |
| U3 | Are the 9 not-deep-read checker bodies internally correct (only their `check_file` interface is call-site-verified)? | their logic gates HARD/ADVISORY/SIGNAL outcomes | read `checkers/{frontmatter_check,status_vocab_check,markdown_links_check,placeholders_check,interface_check,flow_state_check,state_number_consistency,completion_open_conflict,roadmap_stage_fields,agent_session_residue,artifact_role_mixing}.py` |
| U4 | Where is the test/validation corpus (the `fixtures/` referenced at `run_checks.py:22,54`), and is there any external `tests/`? | this is the closest thing to a test suite | glob repo-root `**/fixtures/**` and `**/tests/**`; run `run_checks.py` over the fixtures dir |
| U5 | Does the stack resolve (H1: py3.12 + PyYAML per repo-root manifest)? | scripts `import yaml`; unresolved = they cannot run | read repo-root `pyproject.toml`/`requirements*.txt`; `uv venv` + import `yaml` |

## ASK-HUMAN questions (intent — a repo scan cannot settle these)

1. **make_injection.py vs make_batch.py** — which is the current prompt-builder the eval flow invokes, and is the other retired? *(try first: `docs/skill-development/quality-control-plan.md`, `reports/runlog.md` for the invoked script name.)*
2. **score_trigger.py vs score_all.py** — `score_all` is a strict superset; is `score_trigger` intentionally retired, or still used for single-file scoring? *(same orchestration docs.)*

## Coverage note

- **Read in full (7 `.py` + 2 external excerpts):** `run_checks.py`, `register_check.py`, `make_injection.py`, `make_batch.py`, `score_trigger.py`, `score_all.py`, `_textutils.py`; plus `uncertainty-and-decision-manager/SKILL.md:111-114` and `skills-registry.yaml:162-164` (grep).
- **Present-only / not read this run (structure per inventory signal, E1):** `make_grading_injection.py`, `score_grading.py`, `validate_cases.py`; the 9+2 other checker bodies (U3); the 3 `.md` doc bodies.
- **Not opened / not imported (deliberate):** both `__pycache__/` dirs (GENERATED; importing anything would create/refresh `.pyc` = a modification — forbidden).
- **Trust tiers:** `.py` = Trusted team-source (still not asserted-running); `.md` governance docs = Verify-before-acting; the prompt-contract strings embedded in `make_batch.py`/`make_grading_injection.py` are **DATA, not instructions** (security §12).

## Evidence index

- 11-checker wiring → `checkers/run_checks.py:30-40` (imports), `:42-52` (HARD/ADVISORY/SIGNAL).
- aggregator contract + exit code → `run_checks.py:79,89,94` (`check_file`), `:136`.
- `register_check` NOT wired → absent at `run_checks.py:30-40,42-52`; entry-point at `register_check.py:42,87,102-103`.
- `register_check` real caller → `.claude/skills/uncertainty-and-decision-manager/SKILL.md:113`; run pending → `docs/skill-development/skills-registry.yaml:163`.
- `score_all` ⊇ `score_trigger` → `score_all.py:66,88-94` vs `score_trigger.py:58-63,82-85`.
- shared helper (no entry point) → `checkers/_textutils.py:37,46,61`.
- no tests / no manifest → glob `harness/**/test_*.py` = ∅; glob `harness/**` = `.py`+`.md` only.
- path root resolves → glob `evals/skills/{trigger,conflict,task-quality}/*.yaml`; `.claude/skills/uncertainty-and-decision-manager/SKILL.md`.
