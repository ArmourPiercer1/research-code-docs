<!--
generated_by_skill: (manual, Phase-1 test-corpus governance authoring)
skill_version: n/a
source_commit: upstream seeds pinned in tests/corpus/upstream/UPSTREAM-COMMITS.tsv
source_documents:
  - docs/documentation-quality-evaluator_测试语料自动准备与评测流程.md (§9, §10)
  - evals/skills/harness/make_grading_injection.py (reviewer/reader/evaluator roles)
status: DECIDED (v0 adjudication protocol)
last_verified: 2026-07-31
-->

# Adjudication Protocol — setting gold labels without the evaluator

Turns a `candidate` case into a `golden-*` case by two **independent** reviewers who do **not** use the
`documentation-quality-evaluator` skill. Realizes eval-flow doc §9.

## 1. Roles (mutually isolated)

| Role | Sees | Never sees | Tool |
|---|---|---|---|
| **Corpus Builder** (this session) | everything | — | fetch/snapshot/normalize/mutate scripts |
| **Reviewer A** | the document + the *simplified* reviewer rubric below | the DQE skill, hard-fail.md, rubric.md, the other reviewer, the manifest's `expected.*` | fresh sub-agent, `make_grading_injection.py --role reviewer` |
| **Reviewer B** | same as A, spawned separately | same as A | fresh sub-agent |
| **Evaluator-under-test** | a **blind** copy only | any `expected.*`, class-dir name, manifest | later round; `--role evaluator` |

Reviewer A/B deliberately get a *thinner* context than the evaluator: a short rubric, **not** the
HF-1..15 catalog. This keeps their gold labels independent of the exact gates the evaluator will be
graded against (so a passing evaluator is not merely echoing the label-setter).

## 2. Simplified reviewer rubric (what A/B answer)

For the given `artifact_type` + `profile`, answer only:

1. **Type & purpose** — what is this document's single primary job? Is it self-contained for that job?
2. **Verdict** — would you `PASS`, `FAIL`, or `PARTIAL` this as *that type* under *that profile*?
3. **Top defects** — list the 1–5 most serious issues (free text) and, for each, tag a *category*:
   `mixed-responsibilities` / `state-contradiction` / `volatile-in-stable` / `non-executable-milestone` /
   `unsupported-claim` / `missing-rationale` / `not-reproducible` / `not-actionable` /
   `context-dependent` / `stale` / `other`.
4. **Provenance note** — is anything missing that only matters under a `controlled` (not `external`)
   profile? (e.g. local traceability front-matter.)
5. **Confidence** — HIGH / MEDIUM / LOW.

Reviewers propose labels in their **own** words; the Builder maps their category tags to HF ids **after**
both have answered — reviewers are not told the HF taxonomy.

## 3. Flow

```
Corpus Builder materializes candidate (+ human annotation for negatives)
  → Reviewer A (isolated sub-agent) proposes verdict + defects + confidence
  → Reviewer B (isolated sub-agent) proposes verdict + defects + confidence
  → Builder compares:
      • verdicts agree AND defect categories overlap on the intended one
            → consensus recorded → case promoted candidate → golden-*
      • verdicts disagree, OR a negative's intended defect is missed by both
            → case stays candidate; entry appended to evals/skills/adjudication/queue.md
              (never fabricate consensus)
  → consensus + confidence written into manifest.adjudication
```

## 4. What the AI does automatically vs what the user spot-checks

**Automatic (this protocol):** type triage, license/SHA/path registration, mechanical normalization,
mutation + diff, Reviewer A/B initial reads, disagreement list, manifest drafts, blind-suite build,
result aggregation.

**Reserved for user spot-check (eval-flow §9.4):** any case where A/B **materially** disagree on a
blocker; whether a given public doc should count as a positive at all; unclear licenses; whether a
mutation changed the source's technical meaning; HF-13/HF-15 escape-hatch borderlines; and cases where
reviewers **and** evaluator are all low-confidence. The user is **not** asked to read every file — only
to rule on the queue and to sample ≥1 case per artifact type in the first batch.

## 5. Promotion states

`source-only` → `candidate` (materialized + manifest drafted) → `golden-*` (A/B consensus + confidence)
→ (later) `locked` once the blind eval matrix has run without contradicting the label.
A case may regress to `quarantine` at any step on unresolved dispute.
