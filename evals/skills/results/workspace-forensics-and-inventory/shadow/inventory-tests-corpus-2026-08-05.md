<!--
generated_by_skill: workspace-forensics-and-inventory
skill_version: 0.1.0
source_commit: 975e930 (workspace HEAD; shadow-run eval artifact)
source_documents:
  - tests/corpus/ (workspace tree at 975e930 — enumerated, not verified)
  - tests/corpus/source-seeds/seed-register.yaml (listed as claims, not verified)
  - tests/corpus/mutations/mutation-catalog.yaml (listed as claims, not verified)
  - tests/corpus/cases/**/manifest.yaml (listed as claims, not verified)
status: read-only inventory (candidates + signals; nothing verified as running)
last_verified: 2026-08-05T09:09Z
eval_artifact: workspace-forensics-and-inventory v0.1.0 SHADOW RUN (Batch-2 light round) — produced by a fresh sub-agent injected with the SKILL.md only, pointed READ-ONLY at tests/corpus/. Eval evidence, not a governance doc.
-->

# Inventory — tests/corpus/ (DQE test corpus)

**Mode:** workspace
Read-only. Every classification is a **candidate tagged with its structural signal** — nothing here is a claim that code runs, that a case "passes," or that any file is the canonical truth (that is `project-state-reconstructor`'s job). Text inside scanned files (manifests, run logs, READMEs) is treated as **data, not instructions**.

## Project Map (one line per directory)

| dir | purpose-guess (candidate) | files (tracked) | notable types | coverage |
|---|---|---|---|---|
| `tests/corpus/` | DQE test-corpus root (no top-level files) | 304 total | — | fully-scanned (structure) |
| `cases/` | test-case fixtures / gold cases | 86 | `.yaml`,`.md`,`.diff` | fully-scanned (structure) |
| `cases/boundary-pairs/` | paired pass/fail boundary cases | 27 | `.yaml`(14),`.md`(13) | fully-scanned |
| `cases/golden-positive/` | should-ALLOW gold cases | 7 | `.yaml`(6),`.md`(1) | fully-scanned |
| `cases/golden-negative/` | should-FAIL gold cases (single-defect) | 18 | `.yaml`(9),`.md`(5),`.diff`(4) | fully-scanned |
| `cases/quarantine/` | superseded / withheld cases (candidate) | 34 | `.yaml`(22),`.md`(7),`.diff`(5) | fully-scanned |
| `cases/candidate/` | empty placeholder (0 tracked, 0 on-disk) | 0 | — | fully-scanned (empty) |
| `mutations/` | mutation taxonomy + per-case plans | 6 | `.yaml`,`.md` | fully-scanned |
| `mutations/plans/` | per-case mutation plans (+`payloads/`) | 5 | `.yaml`,`.md` | fully-scanned |
| `source-seeds/` | registered upstream source snapshots | 63 | `.txt`,`.yaml`,`.md`,`.rst` | fully-scanned (structure) |
| `source-seeds/original/` | copied upstream bodies (snapshot) | 54 | `.txt`(27),`.yaml`(14),`.md`(12),`.rst`(1) | summarized-only (data bodies) |
| `source-seeds/normalized/` | normalized copies + logs | 8 | `.yaml`,`.md`,`.rst` | summarized-only |
| `source-seeds/licenses/` | empty placeholder (0 tracked, 0 on-disk) | 0 | — | fully-scanned (empty) |
| `blind-runs/` | dated eval run outputs (11 run dirs) | 149 | `.yaml`,`.md`,`.txt`,`.json`,`.tsv`,`.diff`,`.rst` | summarized-only (GENERATED) |
| `upstream/` | 12 cloned reference repos (gitignored) | 0 tracked / **~444 MB on disk** | git clones | **summarized-only (1 level; NOT recursed)** |

`blind-runs/` run subdirs (all GENERATED, summarized-only): `adj-2026-07-31`(42), `matrix-2026-07-31`(44), `adjudication-v4`(13)/`v4b`(5)/`v4c`(3), `diag-2026-08-02`(15)/`diag-d3-2026-08-02`(4)/`diag-d3b-2026-08-04`(2), `phase-e-2026-08-05`(11), `reconfirm-2026-07-31`(6), `v04-sanity`(4).

`upstream/` repos (one-level entry counts only, bodies NOT read): `artifact-evaluation`, `backstage`, `enhancements`, `kubernetes-enhancements`, `llm-d-benchmark`, `madr`, `mozilla-sre-adrs`, `open-design`, `peps`, `python-peps`, `rust-safe-transmute`, `yahoo-ml-reproducibility`.

## Coverage note

- **Fully scanned (structure/tracked-file level):** `cases/`, `mutations/`, `source-seeds/` layout + `seed-register.yaml`, `blind-runs/` directory/type structure.
- **Deep-read (sampled, high-signal):** `source-seeds/seed-register.yaml`, `mutations/mutation-catalog.yaml` (head), `cases/boundary-pairs/BP-006-release/manifest.yaml`.
- **Summarized-only:** `upstream/` (12 clones, ~444 MB — one-level counts only, per task constraint), `blind-runs/*` file bodies (counts + index filenames only), `source-seeds/original|normalized` bodies (data).
- **Skipped (reason):** all `upstream/` repo internals (large external clones, gitignored); individual case `document.md` and seed `original/*` bodies (corpus payload data, not needed for structure).
- Working tree unchanged: `git status --porcelain` shows **no untracked and no modified** files under `tests/corpus/` (this pass wrote nothing).

## Artifact buckets — workspace mode (each entry: `path → signal`)

- **Entry-point candidates:** **NONE inside the corpus.** `git ls-files` finds **no `.py`/`.sh`/`.ps1`/`.ipynb`/`.bat`** tracked under `tests/corpus/` (signal: zero executable/driver files; corpus is pure fixtures + data). Producing harness is **external** (referenced by the skill as `evals/skills/harness/…`) — out of scan boundary.
- **Build / deps / config:** **NONE inside the corpus.** (`schema: seed-register/v1`, `schema: mutation-catalog/v1` are *data schemas* declared in YAML, not build config — signal: `schema:` keys inside data files, no `pyproject.toml`/`Makefile`/`environment.yml` present.)
- **Test fixtures / gold cases** (NOT executable tests — do not claim they pass): `cases/**/manifest.yaml` (signal: `case_id`, `class`, `expected.gate_decision`, `adjudication.status: gold`); paired bodies `cases/**/document.md`; `cases/**/*.diff` (mutation diffs). 10 case manifests cite `base_seed` (signal: `grep base_seed` → 10 hits linking cases to seeds).
- **Experiment / analysis scripts:** **NONE** (no scripts tracked — same signal as entry-points).
- **Results & produced artifacts (GENERATED):** `blind-runs/matrix-2026-07-31/raw-results.json` + `eval-plan.json`, `blind-runs/diag-2026-08-02/raw-results.json`, `blind-runs/phase-e-2026-08-05/{phase-e-plan.json, canary-raw.json, canary-metrics/metrics.json, results/v041__BP-006-*__N.json}`, all `blind-runs/**/*.tsv` result tables, `blind-runs/**/*.md` run notes/READMEs, `blind-runs/adjudication-v4*/*.diff|*.txt` (signal: dir name `blind-runs/` + dated subdirs + `raw-results`/`metrics`/`*.tsv` outputs). **Label: GENERATED — never a source of truth for current behavior.**
- **Caches & generated:** none of the classic kind (`__pycache__/`, `.ipynb_checkpoints/`, `build/`) present; the `blind-runs/` tree is this corpus's generated-output analog (see above).
- **Data (inputs):** `source-seeds/seed-register.yaml` (registry/index), `source-seeds/original/*` (copied upstream snapshots), `source-seeds/normalized/*`, `mutations/mutation-catalog.yaml` + `mutations/plans/*` (transform specs), and `upstream/*` (12 external clones, ~444 MB). Trust: `upstream/` + `source-seeds/original` = external content → **Untrusted (data only)**.
- **Docs:** no top-level `README` in `tests/corpus/`; doc-like text is embedded in `blind-runs/**/README.md` (run logs) and case/seed `.md` bodies (signal: `README.md` inside generated run dirs → run documentation, not corpus docs).

## Orphans & unreferenced (candidates — cite the search; scan boundary = `tests/corpus/` only)

| item | kind | signal (why candidate) | scan boundary |
|---|---|---|---|
| `blind-runs/**` (11 run dirs) | unreferenced-producer | no producing script found *inside corpus* (0 tracked scripts) — producer is the external eval harness | searched `tests/corpus` for `*.py/*.sh` |
| `cases/candidate/` | empty-placeholder | 0 tracked + 0 on-disk entries | `git ls-files` + `ls -A` |
| `source-seeds/licenses/` | empty-placeholder / unreferenced | 0 files, yet `seed-register.yaml` carries `license_spdx` per seed (no license bodies stored) | `git ls-files` + `ls -A` |
| `cases/golden-negative/GN-EVIDENCE-BARE-CLAIM-001/` | plan/case mismatch | case dir exists but **no** matching `mutations/plans/GN-EVIDENCE-BARE-CLAIM-001.yaml` (plans cover only ADR-001/002, PROP-VALIDATION-001, ROADMAP-001) | `git ls-files mutations/plans` |
| `cases/quarantine/*-v1` (e.g. `BP-002-fail-v1`, `BP-005-pass-v1`) | superseded-version candidate | `-v1` suffix + `quarantine/` dir alongside active `BP-002-fail`, `BP-005-pass` in `boundary-pairs/` | dir-name pattern |

## Candidate canonical sources (per information type — CANDIDATE, confirmed later)

| info type | candidate source | signal |
|---|---|---|
| source/provenance registration | `source-seeds/seed-register.yaml` | only registry; `dataset_version: 3`, `schema: seed-register/v1`, per-seed `sha256`+`commit` |
| mutation taxonomy | `mutations/mutation-catalog.yaml` | `schema: mutation-catalog/v1`; declares itself "the TAXONOMY" |
| per-case expected truth / gold label | `cases/<id>/manifest.yaml` | `expected.*` + `adjudication.status: gold` + reviewer A/B consensus |
| per-case mutation recipe | `mutations/plans/<case-id>.yaml` | plan files keyed to golden-negative case ids |
| eval run history (GENERATED, not current truth) | `blind-runs/<dated>/raw-results.json` + `*.tsv` | dated dirs; `phase-e-2026-08-05` + `adjudication-v4c` are the newest by date/name |
| external source material | `upstream/` clones + `source-seeds/original/` | 444 MB clones + copied bodies referenced by `seed-register` |

**File trust tiers:** *Trusted (team-authored fixtures/specs)* — `seed-register.yaml`, `mutation-catalog.yaml`, `cases/**/manifest.yaml`, `mutations/plans/*`. *Verify-before-acting (generated)* — everything under `blind-runs/`, `source-seeds/normalized/`. *Untrusted (external, data-only)* — `upstream/**`, `source-seeds/original/**`.

## Handoff (unknowns + questions for `project-state-reconstructor`)

- **Producers of `blind-runs/`:** confirm which external skill/harness generated each dated run and whether any is the *authoritative latest* — do **not** treat these JSON/TSV outputs as current behavior (they are GENERATED). `phase-e-2026-08-05` and `adjudication-v4c` look newest; verify.
- **Quarantine status:** confirm `cases/quarantine/*` (34 files, incl. `*-v1`) are superseded/withheld vs active gold — the `-v1` suffix is only a *naming* signal here.
- **Plan/case coverage gap:** verify whether `cases/golden-negative/GN-EVIDENCE-BARE-CLAIM-001/` intentionally has **no** `mutations/plans/` entry (hand-authored negative vs mechanical mutation).
- **Empty placeholders:** confirm `cases/candidate/` and `source-seeds/licenses/` are intentional (planned-but-empty) vs stale.
- **Version signal:** `seed-register.yaml` declares `dataset_version: 3`; confirm this against the current authoritative corpus/candidate version (PSR to reconcile — not asserted here).
- **Pass/fail semantics:** every `expected.*` / `adjudication.consensus` field in the manifests is a *recorded gold expectation*, **not** evidence that DQE currently produces that result — PSR must verify Intent-vs-Reality against actual runs.
- **Out-of-scope note:** the executing harness, its config, and any `docs/testing/corpus-policy.md` referenced by these files live **outside `tests/corpus/`** and were not scanned.
