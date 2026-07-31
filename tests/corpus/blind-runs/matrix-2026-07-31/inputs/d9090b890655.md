<!--
skill_version: 0.1.0
generated_by_skill: research-evidence-synthesizer
source_commit: eoopt@c3d4e5f
source_documents: [references/noise-robustness-notes.md]
status: DECIDED
last_verified: 2026-07-30
-->

# Evidence note — noise robustness of the projected-gradient variant

## Claim

- **VERIFIED:** the projected-gradient variant is more stable than the baseline under strong observation
  noise (σ ≥ 0.2). The projection step bounds the step norm and damps noise-driven overshoot, so the
  variant is the stable choice.

This is settled; downstream phases can rely on the variant being more robust.
