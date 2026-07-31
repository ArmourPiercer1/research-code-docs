<!--
generated_by_skill: (manual, Phase-1 test-corpus governance authoring)
skill_version: n/a
source_commit: upstream seeds pinned in tests/corpus/upstream/UPSTREAM-COMMITS.tsv
source_documents:
  - docs/documentation-quality-evaluator_测试语料自动准备与评测流程.md (§2, §5, §13)
  - docs/skill-development/quality-control-plan.md
  - working-constraints (memory): isolation / read-only-audit / no-fabrication
status: DECIDED (v0 corpus policy)
last_verified: 2026-07-31
-->

# Test-Corpus Policy — `documentation-quality-evaluator`

This policy governs the DQE evaluation corpus under `tests/corpus/`. It adapts the third-party
eval-flow doc (§2/§5/§13) to **this** workspace, which already carries a working eval harness under
`evals/skills/`. The corpus **feeds** that harness; it does not replace it.

## 1. Seed ≠ positive (the load-bearing rule)

A document being on GitHub, or from a famous project, is **never** grounds for `PASS`. Every seed is
`source-only` until it is (a) bound to a `profile` (provenance policy + evidence requirement + reader
test), and (b) given a gold label by **two reviewers who are not the evaluator-under-test** (see
`adjudication-protocol.md`). Public seeds enter the corpus as `candidate`, not `golden-positive`.

## 2. Upstream & snapshots are read-only

- `tests/corpus/upstream/` (the 12 manually-cloned repos) and `tests/corpus/source-seeds/original/`
  are **immutable**. No cleaning, no format fixes, no mutation happens there.
- All normalization, mutation, and case construction happen in **derived** copies
  (`normalized/`, `cases/`). Every derived file records its base + operation.

## 3. Provenance is mandatory

Each seed in `source-seeds/seed-register.yaml` records: repo URL, commit SHA, in-repo path,
file SHA-256, license SPDX (or `NONE`), copy-permitted flag, and local use mode
(`snapshot` / `excerpt` / `structure-reference` / `ideas-only` / `reference-only`).
Commit SHAs are pinned in `tests/corpus/upstream/UPSTREAM-COMMITS.tsv`; we never rely on a floating
`main`/`master` for regression.

## 4. Licensing & quarantine

| License class | Seeds | Local handling |
|---|---|---|
| Apache-2.0 | backstage, enhancements(=KEP), llm-d-benchmark, open-design | copy snapshot + attribution |
| MIT / dual-MIT | yahoo, rust-safe-transmute (Apache∨MIT), madr (MIT∨CC0) | copy snapshot + attribution |
| Public-domain / CC0 | peps | copy snapshot + attribution |
| BSD-style (+ ACM on data) | artifact-evaluation (`docs/` BSD; `xml/`=ACM) | copy `docs/` as reference only; **never** copy `xml/` |
| **NONE** | **mozilla-sre-adrs** | **QUARANTINE — clone reference only, do NOT copy any body text into the publishable corpus** |

A seed whose license cannot be confirmed, or whose reviewers dispute its meaning, goes to
`cases/quarantine/` and keeps only a clone reference.

## 5. Allowed vs forbidden normalization

**Allowed (mechanical only):** CRLF→LF, UTF-8 re-encode, strip GitHub-UI nav residue, RST→Markdown
(with a saved conversion log), rewrite absolute repo paths to fixture-internal ones, add missing code
fences, fix format errors the converter itself introduced.

**Forbidden (semantic):** adding arguments the source lacks, supplying missing alternatives, changing a
technical conclusion, changing a status header, deleting open questions, or beautifying to make a doc
pass the evaluator. Any normalization that risks semantics is skipped and the file is kept verbatim
(tool = `none`), noted in its normalization log.

## 6. Evaluator ↔ gold-label isolation

The `documentation-quality-evaluator` skill **never sets the first gold label**. It only ever sees a
**blind** input (random case ID, class-name directory stripped, `expected.*` withheld). The
authoritative expected labels live in each case's `manifest.yaml` and are read **only** by the
comparator/scorer, never mounted into an evaluator run. Reviewer A/B run **without** the DQE skill,
hard-fail catalog, or rubric internals.

## 7. Single-defect negatives & minimal-difference pairs

Prefer `golden-negative` cases built as **one** controlled mutation of an adjudicated positive, so a
failure is attributable to a specific defect rather than to general messiness. Prefer `boundary-pairs`
that differ by exactly the **one** condition under test. A mutation that introduces unrelated defects
is demoted to `candidate/`, not gold.

## 8. Every negative declares required **and** forbidden blockers

`required_blockers` = gates that MUST fire (may be empty for a case that should soft-FAIL on score, not
a hard gate). `forbidden_blockers` = gates that must NOT fire — the anti-over-firing guard that catches
HF-9/HF-13/HF-14/HF-15 abuse. A negative with an empty `required_blockers` still declares its
`required_findings` (the MAJOR issues the evaluator must name) and its expected `document_quality: FAIL`.

## 9. Overfitting guards

- Reserve **≥3 of the 15** first-batch cases as **hidden holdout**: their expected labels are withheld
  from any DQE-tuning iteration (marked `holdout: true` in the manifest).
- The DQE `SKILL.md` must never encode a specific case's answer (e.g. "if you see 59 and 69, fire
  HF-14a"). Case-specific patterns live only here, in the harness.
- Mutation phrasings are varied (different numbers, zh/en, scattered sections) so the evaluator cannot
  key on a fixed token.

## 10. Traceability

Every generated corpus file (register, catalog, manifest, report, script output) carries a front-matter
block or header recording source commit(s) + generation context. Nothing here is pushed to GitHub or
installed into the live Claude Code loader.
