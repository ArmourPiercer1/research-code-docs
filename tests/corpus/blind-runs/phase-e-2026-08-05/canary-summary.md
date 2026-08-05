# Phase E — canary result (2026-08-05): FAILED → Phase E HALTED

Per `DQE_D3决策与PhaseE安全准入计划` §8, the 2-slot canary is a hard go/no-go gate: *"canary 不通过则 Phase E
自动停止."* It did not pass. **The full 61-slot matrix was NOT launched.** Cost of the canary: ~0.69M tokens
(5 evaluator slots). This is the safety design working as intended — a ~0.7M-token probe caught a defect that
would have guaranteed an admission failure across the ~5.6M-token matrix, and surfaced a contract conflict no
amount of running the matrix would resolve.

## What the canary checked vs found

| check (§8) | expected | observed | ok |
|---|---|---|---|
| BP-006-audit gate | ALLOW | ALLOW | ✅ |
| BP-006-audit terminal_green | false | false (UNVERIFIED) | ✅ |
| BP-006-audit HF-9 silent | yes | yes (blockers=[]) | ✅ |
| BP-006-release gate | **BLOCK** | **ALLOW ×3 (stable)** | ❌ |
| BP-006-release HF-9 silent | yes | yes (blockers=[]) | ✅ |
| files_checked ≥ 1 | yes | 1 on every run | ✅ |
| no extra agent fan-out | yes | yes (direct calls) | ✅ |

Aggregated (candidate arm, BP-006 pair): `gate_expectation_mismatch_count=1`, `golden_negative_false_pass=1`,
`boundary_pair_ordering=0.0`, `three_run_verdict_consistency=1.0` (the ALLOW is **stable**),
`terminal_contract_mismatch_count=0`, `checker_execution_compliance=1.0`.

## BP-006-release — three runs (same frozen candidate bundle, same input)

| run | QUALITY_BAND | GATE_DECISION | READER_TEST | blockers | finding_codes (abbrev) |
|---|---|---|---|---|---|
| 1 | PARTIAL | **ALLOW** | PASS | [] | missing-evidence-levels, non-reproducible-data-access, missing-traceability-frontmatter |
| 2 | **FAIL** | **ALLOW** | **FAIL** | [] | not-reproducible, missing-code-version, missing-hyperparameters, inaccessible-training-data, broken-evidence-links, unverified-metrics, not-release-ready |
| 3 | PARTIAL | **ALLOW** | PASS | [] | missing-hyperparameters, gated-training-data, broken-evidence-links, metrics-unverified, not-reproducible |

**Run 2 is the smoking gun:** the evaluator rated the document `QUALITY_BAND=FAIL` and `READER_TEST=FAIL`,
named every reproducibility defect, and *still* emitted `GATE_DECISION=ALLOW` under a **controlled +
release-gate** profile. A FAIL-quality, reader-FAIL, non-reproducible document was allowed to proceed.

## Root cause — the D-16 × OQ-REPRO=A contract collision

Two user-accepted rulings are in direct conflict, now proven empirically:

- **D-16 (`D16_DECISION=ACCEPT`)** made `GATE_DECISION` a deterministic 3-rule derivation where **the rubric
  total and `FACTUAL_VALIDITY` do NOT move `GATE_DECISION`** — only a hard-gate BLOCKER forces BLOCK
  (else missing-required → INCOMPLETE, else ALLOW). This was the fix for the audit-mode 3-way instability.
- **OQ-REPRO=A (`HF_REPRO=NOT_ADOPTED`)** asserted that a non-reproducible controlled release-gate report
  BLOCKs *via the rubric non-compensatory rule + reader Layer-2*, **without** a dedicated reproducibility
  hard gate (`required_blockers: []`).

D-16 **severed the exact path** OQ-REPRO=A depended on. With no hard gate for "not reproducible" and the
rubric/reader forbidden from moving the gate, the default (rule 3) is **ALLOW** — even at `QUALITY_BAND=FAIL`.
So the BP-006-release BLOCK that OQ-REPRO=A promised is now unreachable unless the evaluator happens to map
the reproducibility gaps onto HF-12A/E (a judgment call). The earlier D.3 sample happened to fire HF-12A/E
(BLOCK×3); this canary sample did not (ALLOW×3). The gate is **framing-dependent**, and under D-16 the
default resolves to a **false ALLOW**.

## This is a CONTRACT-class failure (plan §9.3) — user decision required

The fix reverses or amends one of the user's own rulings, so it is not mine to choose. It is not a broad
rewrite, and the ≥2/3-stable-reproduction bar for touching behavior is met (3/3 ALLOW on a clean fixture).
Candidate resolutions are enumerated in the checkpoint message / defect ledger D-17.

## Secondary observations (not the halt cause)
- **required-finding vocabulary mismatch:** the evaluator emits free-form codes (`not-reproducible`,
  `inaccessible-training-data`) instead of the manifest's controlled `missing-code-version` /
  `missing-execution-entry` / … → `required_finding_recall=0.0` on this case. Fixable by manifest synonyms
  or steering the evaluator's FINDING_CODES vocabulary.
- **reader_test instability:** PASS/FAIL/PASS across the three release runs — the reproducibility-execution
  reader test does not reliably FAIL on a non-reproducible doc (same root as the gate issue).

Artifacts: `results/v041__BP-006-{audit__1,release__1,release__2,release__3}.json`, `canary-raw.json`,
`canary-metrics/`.
