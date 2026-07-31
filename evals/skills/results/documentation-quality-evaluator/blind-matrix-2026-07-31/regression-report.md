<!--
generated_by: aggregate_eval_results.py + manual root-cause analysis
skill_version_under_test: documentation-quality-evaluator 0.3.0
corpus: dataset_version 3 (20 gold cases + 3 stability repeats = 26 runs)
raw: tests/corpus/blind-runs/matrix-2026-07-31/raw-results.json
metrics: evals/skills/results/documentation-quality-evaluator/blind-matrix-2026-07-31/metrics.json
status: DQE v0.3 does NOT meet the §17 promotion bar — stays `experimental`
last_verified: 2026-07-31
-->

# Blind-matrix regression report — DQE v0.3 (2026-07-31)

**Verdict: the §17 promotion bar is NOT MET on all 7 metrics.** `documentation-quality-evaluator` v0.3
stays `experimental` + manual-only. This is the eval **working as designed** — a 26-run blind matrix
surfaced concrete, reproducible defects. Nothing was changed in the skill.

| §17 metric | got | bar | ok |
|---|---|---|---|
| golden-negative false PASS | **2** | 0 | ❌ |
| golden-positive false hard FAIL | **3** | 0 | ❌ |
| required-blocker recall | **0.75** | ≥0.90 | ❌ |
| forbidden-blocker violation rate | **0.115** | ≤0.05 | ❌ |
| boundary-pair ordering | **0.6** (3/5) | 1.0 | ❌ |
| 3-run verdict consistency | **0.33** (1/3) | 1.0 | ❌ |
| max score stddev | **6.18** | ≤5 | ❌ |

## What passed (context — it is not all broken)

All 5 golden-positives' **current** runs passed; BP-001/002/003 orderings correct; BP-001-fail perfectly
stable (FAIL×3, Jaccard 1.0); HF-13/14a/14b/15/12E/10 all fired correctly on their clean negatives
(GN-ADR-002, BP-001-fail, BP-002-fail, BP-003-fail, BP-005-fail). The evaluator is largely sound; the
failures cluster on a few identifiable causes.

## Root causes (skill defects vs fixture ambiguities)

### SKILL DEFECT 1 — HF-9 is not profile-aware (highest-leverage) 🔴
The evaluator hard-FAILs **external-profile** documents for missing local traceability front-matter:
- `BP-004-external` → FAIL `[HF-9]` (forbidden violation; breaks the BP-004 pair — its whole purpose)
- `GP-EXP-001` (external Yahoo recipe) → FAIL `[HF-9]`
- `GP-PROP-002` repeat-2 (external PEP) → FAIL `[HF-9]` (the sole stability break for that case)

One defect causes **2 positive false-fails + 1 forbidden violation + 1 broken ordering + 1 stability
failure**. `frontmatter_check.py` (HF-9) fires regardless of profile, and `hard-fail.md`/`SKILL.md` never
instruct the model to downgrade HF-9 to MINOR under `provenance_policy: external`. The BP-004 pair exists
precisely to test this and the skill failed the external side.
**Fix (v0.4):** make HF-9 profile-gated — external ⇒ HF-9 is a MINOR finding, never a blocker; controlled
⇒ blocker (as today). Feed `provenance_policy` into the gate.

### SKILL DEFECT 2 — HF-12A recall gap → a golden-negative false-PASSED 🔴
`GN-EXP-001` (Yahoo recipe with git commits/env/versions stripped but the "74% accuracy" claim kept) →
**PASS** (total 76.5), missed HF-12A. A load-bearing result claim whose reproduction handles were all
removed must fire HF-12A (doc-only). **Fix:** sharpen HF-12A for result/metric claims — a quantitative
outcome with no code/experiment handle and no assumption label is unsupported.

### SKILL DEFECT 3 — HF-15 recall + stability gap → a golden-negative false-PASSED 🔴
`GN-ROADMAP-001` (Phase-1 committed DoD vaguened to "届时定", Phase-2 gate intact) → **PASS/PASS/FAIL**.
It missed the single vague committed phase when sibling phases had good gates, and was unstable.
**Fix:** HF-15 must fire on **any** committed phase with a non-measurable DoD, independent of siblings.

### SKILL DEFECT 4 — HF-13 / HF-14a over-firing (forbidden violations) 🟠
- `BP-002-fail` fired `HF-13` (forbidden) — a single architecture doc with a maturity snapshot is not a
  4-role hybrid.
- `GN-PROP-001` fired `HF-14a` (forbidden) — likely read the stale TOC anchors (sections removed) as a
  contradiction.
Rate 11.5% vs the ≤5% bar. **Fix:** tighten HF-13 (needs ≥2 divergent-lifecycle *body* roles, not a
status snapshot) and HF-14a (a dangling TOC entry ≠ a state contradiction).

### FIXTURE AMBIGUITY A — BP-005-pass 🟡 (corpus, not skill)
`BP-005-pass` front-matter says `status: DECIDED` while its body is a labeled `HYPOTHESIS (尚未验证)`.
The evaluator fired `HF-3` (candidate-as-decided) + `HF-14a`. The fixture invites this — a "DECIDED"
evidence note containing an unverified hypothesis is genuinely mixed-signal.
**Fix (corpus):** change BP-005-pass status to non-DECIDED (or drop it) so the *only* signal under test
is the honest hypothesis label → isolates HF-12E cleanly.

### FIXTURE AMBIGUITY B — BP-002-fail 🟡 (corpus, not skill)
`BP-002-fail` says `status: DECIDED` + "The core is done" while `OQ-2` is "design review in progress" —
a real incidental contradiction, so the `HF-14a` fire is partly legitimate (like the earlier GN-PROP-001
checklist finding). The intended sole defect was HF-14b.
**Fix (corpus):** remove the "core is done"/`DECIDED` over-claim so HF-14b is the lone defect, OR accept
HF-14a as a second intended blocker and drop it from `forbidden_blockers`.

## Recommended path to v0.4 + re-eval

1. **Skill (v0.4):** fix Defects 1–4 (HF-9 profile-gating is the top lever). Attribute each change in
   `upstream-method-matrix.md`; bump only DQE to 0.4.0.
2. **Corpus:** clean Fixtures A & B (both are the same "status:DECIDED over-claim" pattern), re-review.
3. **Re-run** this exact 26-run matrix (`build_blind_suite` → workflow → `aggregate_eval_results.py`);
   the run dir + plan are reusable.
4. Promote to `provisional-gate` only when all 7 §17 metrics clear.

No skill or fixture was modified in this round. The corpus, plan, and harness are unchanged and ready to
re-run against a v0.4 skill.
