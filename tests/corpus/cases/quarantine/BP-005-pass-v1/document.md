<!--
skill_version: 0.1.0
generated_by_skill: research-evidence-synthesizer
source_commit: eoopt@c3d4e5f
source_documents: [references/noise-robustness-notes.md]
status: DECIDED
last_verified: 2026-07-30
-->

# Evidence note — noise robustness of the projected-gradient variant

## Claim under assessment

- **HYPOTHESIS (尚未验证):** the projected-gradient variant is more stable than the baseline under
  strong observation noise (σ ≥ 0.2).
  - **Evidence status:** `project-inference` — no in-project experiment has been run yet.
  - **Why plausible:** the projection step bounds the step norm, which *should* damp noise-driven
    overshoot; this is an analogy from the constrained-optimization literature, not a measured result.
  - **To verify:** 3 benchmarks × 5 noise levels × 10 seeds; metric = success rate at σ=0.2; decision
    gate GO if ≥ 15 pts over baseline.

## What is NOT claimed

We do **not** assert the variant *is* more stable — only that it is a hypothesis worth the experiment above.
