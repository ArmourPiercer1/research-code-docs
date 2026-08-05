---
generated_by_skill: goal-scope-and-workflow-elicitor
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [evals/skills/results/batch3/scientific-workspace-reconstruction/project-state-report.md]
artifact_type: goal-scope-note
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
scope: "Settles the goal, in/out scope, non-goals, and intended dev–test flow for reconstructing evals/skills/harness/ into a known, trustworthy state; EXCLUDES restructuring/moving files, retiring the superseded pairs, executing/importing anything, and designing the target layout (the architect + provenance/migration phases do those)."
facts: "9 confirmed constraints — see 'Confirmed constraints' (each sourced to a state-report FACT row; max upstream evidence is E2)."
hypotheses: "none (a scope note settles or defers; the PSR's 3 hypotheses H1/H2/H3 are carried as Open decisions Q-4/Q-1/Q-2, not re-asserted here)."
open_questions: "5 open decisions — see 'Open decisions' (each classified + next action); carries PSR ASK-HUMAN-1/2, U1–U5, and the test-strategy gap. Never 'none' — nothing was executed and intent is unconfirmed."
evidence_level: "n/a (goal/scope statement, not an evidence claim); constraints cite the E2 state-report FACT rows they rest on — no E3 (runtime) fact exists upstream."
next_handoff: dev-test-experiment-workspace-architect
handoff_requirements: "Architect needs: (1) the settled goal + Non-goals (esp. do-not-restructure / do-not-retire / do-not-execute); (2) the in/out scope; (3) the 9 Confirmed constraints (E2 FACTs to preserve — 11-checker wiring + check_file contract, register_check standalone, zero test suite, no harness-local manifest, PyYAML dep); (4) the 5 classified Open decisions, handed in parallel to uncertainty-and-decision-manager to register, NOT decided by the architect. NOTE: dev-test-experiment-workspace-architect is not built yet — honest BLOCKED handoff until it exists."
status: "DECIDED for the goal/scope/non-goals/constraints (recovered from the state report); 5 items OPEN in 'Open decisions' (no live user this run — human-preference items are logged, not decided)."
---

# Goal / Scope / Workflow Note — `evals/skills/harness/` reconstruction

Readable with no chat context. Settled items are stated here; every unresolved item is an Open decision below.

> **Confirmation status (no live user this run).** The goal, scope, non-goals, workflow, and constraints below are **recovered from the upstream state report** (`project-state-report.md`), grounded in its E2 FACT rows — not human-confirmed. No human was interviewed and **no human answer is invented.** Anything that needs a maintainer's preference or an action this read-only scoping phase forbids is logged as an **Open decision (OPEN)**, not decided. `document_lifecycle` is therefore `IN_REVIEW`, not `ACCEPTED`.

## Goal

Take the `evals/skills/harness/` skill-eval harness — **21 `.py`** (20 entry-point CLIs + one shared helper `_textutils.py`) and **3 governance `.md`** docs — from its *recovered static-structure* state (**max evidence E2**: present and wired coherently in source, but **never executed** this run) to a **known, trustworthy** state a maintainer can build on. "Trustworthy" here means today's open questions are closed **on evidence, not assumption**:

1. **Canonicity** — which prompt-builder (`make_injection.py` vs `make_batch.py`) and which scorer (`score_trigger.py` vs `score_all.py`) is the *canonical* one the eval flow invokes, and whether the near-duplicate is actually retired;
2. **Runs-green (the E2→E3 gap)** — whether the aggregator `run_checks.py` (11 wired checkers) and the standalone `register_check.py` actually execute green on the real Python + PyYAML stack; and
3. **Test posture** — what test/validation strategy applies to a harness that today has **zero** unit tests (only per-CLI `__main__` self-checks, and a `fixtures/` corpus that is *referenced but absent*).

This note is the **scoping front-end** of that reconstruction. It fixes the goal, in/out scope, non-goals, the intended dev–test–experiment flow, and the constraints the design must respect, then hands off to the (future) **`dev-test-experiment-workspace-architect`** to *plan* — not execute — the target workspace. It deliberately **decides none of the open questions and moves / retires / runs nothing.**

## In scope

- Fixing a single, fresh-reader-actionable **goal** for the harness reconstruction (this note).
- Declaring the load-bearing **non-goals** so the downstream architect cannot silently re-expand scope.
- Framing the intended **dev–test–experiment flow** the architect will design against (where code lives, how it is tested, how the eval machinery runs).
- Carrying every upstream **E2 FACT** forward as a **Confirmed constraint** the target design must preserve.
- Carrying every upstream **open item** (2 supersession pairs, 5 UNKNOWNs, the test-strategy gap) forward as a **classified Open decision** with a next action — nothing silently dropped (frozen-interface rule 7).
- Naming the downstream handoff (**architect**) and the parallel handoff of the open decisions to **`uncertainty-and-decision-manager`**.

## Non-goals (explicit)

Load-bearing — these exist so a downstream skill does not re-expand scope. Each is a deliberate *NOT*:

- **NOT restructuring, moving, renaming, or deleting any file now.** The architect *plans* a target layout; a later **migration** phase executes it. *(Most load-bearing: this note only frames goal/scope — no files change here.)*
- **NOT deciding the superseded-pair retirements** — `make_injection.py`↔`make_batch.py` and `score_trigger.py`↔`score_all.py` stay CANDIDATE, logged as **Q-1 / Q-2**, blocked on a caller/intent check.
- **NOT executing, importing, or running** any module, checker, builder, or scorer. This preserves the read-only, E2-capped posture (importing writes `.pyc` = a modification). "Does it run green" stays open as **Q-4**.
- **NOT deleting or re-wiring `register_check.py`.** The PSR resolved it as an **intentional standalone** of the `uncertainty-and-decision-manager` flow — not an unwired oversight and not a cleanup target.
- **NOT designing the target workspace structure** — that is the architect's job; this note supplies only its goal/scope/constraints.
- **NOT writing the test suite or building the `fixtures/` corpus** — the *strategy* is an Open decision (**Q-3**) that must be settled first.
- **NOT deep-reading or verifying** the 9 not-read checker bodies or the 3 present-only scripts (`make_grading_injection.py`, `score_grading.py`, `validate_cases.py`) — logged as **Q-5**.

## Intended workflow (dev–test–experiment)

**Reconstruction pipeline** (forensics → state → this note → architect → provenance → migration):

1. `workspace-forensics-and-inventory` → `inventory-report.md` — **DONE**.
2. `project-state-reconstructor` → `project-state-report.md` — **DONE** (this note's sole input).
3. `goal-scope-and-workflow-elicitor` → **this `goal-scope-note.md`** — **THIS STEP**.
4. `dev-test-experiment-workspace-architect` → target-workspace design/plan — **NOT BUILT YET → honest BLOCKED handoff** (named as `next_handoff`; consumes this note when it exists).
5. **Provenance** — establish *what runs* / *what is canonical* by resolving the run-green gap (Q-4) and the supersession pairs (Q-1/Q-2) — **FUTURE**.
6. **Migration** — execute the restructure/retirements once decided — **FUTURE**.
- In parallel: the **Open decisions** below go to `uncertainty-and-decision-manager` to register with status + evidence; this skill does not decide them.

**The harness's own dev–test–experiment flow** (the thing being reconstructed — what the architect designs the target layout for):

- **Where code lives:** `evals/skills/harness/` — top-level builders/scorers/validator + a `checkers/` subdir holding the 12 checker CLIs and the shared helper `_textutils.py`. Case inputs live in sibling dirs `evals/skills/{trigger,conflict,task-quality}/*.yaml` (path root resolves — F13).
- **Dependencies:** `import yaml` throughout → **PyYAML** is a runtime dep, resolved from the **repo-root manifest** (there is *no* harness-local manifest — F12); the exact stack (py3.12 + PyYAML) is hypothesis H1, folded into Q-4.
- **How it is tested — today: it is not.** No `test_*.py`/`conftest.py`/`pytest.ini` under `harness/`; the per-checker `__main__` block is a CLI self-check, not an assertion-based suite; a `fixtures/` corpus of "intentionally-bad seeds" is referenced (`run_checks.py:22,54`) but **absent** under `harness/`. Choosing the strategy is Q-3.
- **How experiments run/log:** the harness *is* the eval machinery — it builds injection/batch prompts from the case YAMLs, scores skill outputs, and gates artifacts via `run_checks.py` (HARD/ADVISORY/SIGNAL). Reconstructing this harness = reconstructing the project's own dev–test–experiment tooling.

## Confirmed constraints

Each is a settled constraint the architect must respect, sourced to a state-report FACT row. Max upstream evidence is **E2** (structured-to-run, not run).

| constraint | source (state-report) |
|---|---|
| Max recovered evidence is **E2** (present + wired in source); **no** row claims execution → no downstream artifact may assert the harness "runs" or "passes" until it is actually run | PSR `evidence_level` + `handoff_requirements`(1); F1–F13 |
| **No unit-test suite** exists under `harness/` (no `test_*.py`/`conftest.py`/`pytest.ini`); per-CLI `__main__` self-checks are **not** a suite | PSR "What is tested" + F12 |
| **No build/deps manifest** under `harness/` (no `pyproject`/`requirements*`/`Makefile`/`Dockerfile`) — the manifest is at repo root, out of this workspace's scope | PSR F12 + Inventory |
| Every builder/scorer does `import yaml` → **PyYAML is a runtime dependency** (exact version = hypothesis H1, unconfirmed) | PSR F12 (`make_injection.py:18`) |
| `run_checks.py` wires **exactly 11** checkers, classified **HARD=2 / ADVISORY=4 / SIGNAL=5**, each driven through the **`check_file(path)->(ok,problems)`** contract | PSR F2 / F3 / F4 / F5 |
| `register_check.py` is an **intentional standalone** owned by the `uncertainty-and-decision-manager` flow (`SKILL.md:113`) — unwired from `run_checks.py` **by design**; NOT a delete/cleanup/re-wire target | PSR F6 / F7 / F8 + Orphan resolution |
| `score_all.py` is a **functional superset** of `score_trigger.py` (necessary- but not-sufficient for "retired") | PSR F11 |
| **20 of 21 `.py` are entry points** (`main`+`__main__`); `_textutils.py` is the sole shared helper (no entry point) | PSR F1 / F9 / F10 |
| **Read-only posture:** importing/executing any module writes `.pyc` = a modification; the two `__pycache__/` dirs are GENERATED, not evidence | PSR Inventory + Coverage note |

## Open decisions (→ decision register)

Every unsettled item, classified + given a next action. **Not decided here.** Carries PSR ASK-HUMAN-1/2, U1–U5, and the test-strategy gap. Hand in parallel to `uncertainty-and-decision-manager`.

| id | question | classification | recommended next action |
|---|---|---|---|
| Q-1 | Which of `make_injection.py` / `make_batch.py` is the **canonical** prompt-builder the eval flow invokes, and is the other retired? *(PSR ASK-HUMAN-1; hypothesis H2 leans make_batch)* | **user-preference** | Repo-verify **first**: grep the named orchestration docs (`docs/skill-development/quality-control-plan.md`, `reports/runlog.md`) for the invoked builder name. If none names it (PSR: a repo scan cannot settle intent), confirm retirement with the maintainer. Do **not** retire in this phase. |
| Q-2 | Is `score_trigger.py` **retired** (`score_all.py` is a strict superset, F11) or still used for single-file scoring? *(PSR ASK-HUMAN-2; hypothesis H3 leans retired)* | **user-preference** | Same orchestration-doc check; if the invoked scorer is unnamed, confirm with the maintainer. Do **not** retire in this phase. |
| Q-3 | What **test/validation strategy** applies to a suite-less harness — add a pytest suite? build the `fixtures/` corpus referenced at `run_checks.py:22,54`? treat the CLI `__main__` self-checks as sufficient? | **user-preference** | Repo-verify **first** (PSR U4): glob repo-root `**/fixtures/**` and `**/tests/**` for an existing corpus. Then choose the strategy; it feeds the architect's test-layout design. |
| Q-4 | Does the harness actually **run green** (the E2→E3 gap that makes "trustworthy" real) — `run_checks.py` executes all 11 checkers without traceback (U1), `register_check.py` runs on a real `decision-register.md` (U2, registry says its run is *pending*), and the py3.12+PyYAML stack resolves (U5, H1)? | **repo-verifiable** | In the **execution-permitted** phase (architect/provenance — *not* this read-only phase), run the PSR U1/U2 commands from repo root and capture exit codes; read the repo-root manifest, then `uv venv` + import `yaml` for U5. |
| Q-5 | Are the **9 not-deep-read checker bodies** + the **3 present-only scripts** (`make_grading_injection.py`, `score_grading.py`, `validate_cases.py`) internally correct, beyond the call-site-verified `check_file` interface? *(PSR U3)* | **repo-verifiable** | Read the 9+3 bodies (PSR U3 list); no execution needed — doable read-only, but out of this scoping note's scope. |
