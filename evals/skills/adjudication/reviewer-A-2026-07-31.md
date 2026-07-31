<!--
generated_by: isolated Reviewer A sub-agent (general-purpose, no DQE skill/hard-fail/rubric)
blind_run: tests/corpus/blind-runs/adj-2026-07-31
last_verified: 2026-07-31
-->

# Reviewer A — raw verdicts (blind, isolated)

Reviewer A read ONLY the 20 blind inputs + their declared type/profile; no manifests, no `.secret/`,
no SKILL.md. Verbatim deliverable:

```
BLIND=cd367ad16743 VERDICT=PARTIAL TAGS=[state-contradiction,other] CONF=MEDIUM — Strong KEP body, but its signoff checklist marks "Test plan" and "Graduation criteria" as in place and the TOC lists them, yet those sections are absent from the body.
BLIND=a9eb72624f93 VERDICT=PASS TAGS=[none] CONF=HIGH — Clean roadmap: architecture summarized + linked (not inlined), measurable DoDs, deferred phase left uncommitted, provenance front-matter present.
BLIND=982e524e5a69 VERDICT=FAIL TAGS=[volatile-in-stable,state-contradiction] CONF=MEDIUM — Stable design doc embeds a bare live "69 项测试全部通过" with no dynamic-source pointer and asserts "core is done / balancer ready" while OQ-2 says the balancer design is still under review.
BLIND=f522dfdc3f12 VERDICT=PASS TAGS=[none] CONF=HIGH — Honestly labels the claim a HYPOTHESIS (尚未验证), states evidence status as project-inference with no experiment run, separates the plausibility analogy from measurement, and gives a concrete verify plan with metric + gate.
BLIND=505078bada12 VERDICT=PASS TAGS=[none] CONF=HIGH — Textbook ADR: context, decision with a concrete key formula, consequences (good/cost/risk), and alternatives with rejection rationale; external so no local front-matter required.
BLIND=ea43fe43ebf9 VERDICT=FAIL TAGS=[unsupported-claim,not-reproducible] CONF=HIGH — Labels the claim "VERIFIED"/"settled" and tells downstream to rely on it, backed only by a theoretical mechanism with no experiment, data, or reproduction handle.
BLIND=43cd9d759a79 VERDICT=FAIL TAGS=[mixed-responsibilities,volatile-in-stable] CONF=HIGH — A roadmap that also inlines a full architecture spec, a "(live)" status table with bare counts (31/47, 69/94 "today"), and a working-session/AskUserQuestion log.
BLIND=113a972f8c39 VERDICT=PASS TAGS=[none] CONF=HIGH — Complete, well-argued PEP; Rejected outcome but exemplary writing, with each alternative analyzed and rejected on stated grounds plus compatibility and teaching plans.
BLIND=9e615e24f830 VERDICT=PASS TAGS=[none] CONF=HIGH — Correct stable design doc: dated frozen snapshot, defers live counts to status/current.md, and balancer-under-review is consistent with OQ-2; provenance front-matter present.
BLIND=0b3bbf03c604 VERDICT=PARTIAL TAGS=[non-executable-milestone,state-contradiction] CONF=MEDIUM — The committed·next phase carries a vague 验收 line ("效果达标即可，具体算例与阈值届时定") that conflicts with its own concrete GO ≥20% gate.
BLIND=a725f23cf666 VERDICT=FAIL TAGS=[non-executable-milestone,not-actionable] CONF=HIGH — Both committed phases lack any measurable gate ("先测试有效维，再决定", "先跑几个核函数…好就用").
BLIND=acf40c450dc7 VERDICT=PASS TAGS=[none] CONF=HIGH — Reproducible experiment report: pins data-processing and training git commits, tool versions (TF models v1.10.0, TF v1.8), full hyperparameters, hardware (V100), and target metric.
BLIND=327009803262 VERDICT=PARTIAL TAGS=[not-reproducible,unsupported-claim] CONF=MEDIUM — Method and hyperparameters remain, but the code commits, tool versions, and inference hardware needed to reproduce the headline 74% accuracy and 11ms latency have been stripped out.
BLIND=73cbc7fd3252 VERDICT=PASS TAGS=[none] CONF=HIGH — Complete, self-consistent format-decision doc with background, inspiration/rationale, and a full envelope/metadata/component specification.
BLIND=cc596130ffe9 VERDICT=PARTIAL TAGS=[missing-frontmatter] CONF=HIGH — Body is an excellent ADR, but as a controlled artifact it lacks the required traceability front-matter (skill/version/commit/time/status).
BLIND=cb9fd2230330 VERDICT=PARTIAL TAGS=[missing-rationale] CONF=MEDIUM — Opens at "## Format" with no Background/Context/decision rationale; complete as a format spec but incomplete as an ADR of its declared type.
BLIND=6ea29bd05566 VERDICT=PASS TAGS=[none] CONF=HIGH — Exemplary research phase: question + minimal experiment + measurable metric (median effective-dim over 30 runs) + explicit numeric GO/MODIFY/STOP + downstream routing.
BLIND=8cb331163a92 VERDICT=FAIL TAGS=[mixed-responsibilities,volatile-in-stable] CONF=HIGH — Stable format ADR contaminated with an inlined live rollout status (47/47, 312 repos this week, 68% complete), a deploy/on-call runbook, and a session log.
BLIND=8e2f5cadfa89 VERDICT=PASS TAGS=[none] CONF=HIGH — Complete KEP that adds Test Plan, Graduation Criteria, and Feature Enablement/Rollback on top of full design details and PRR; consistent throughout.
BLIND=d932b2314eab VERDICT=PASS TAGS=[none] CONF=HIGH — Every committed phase states question + experiment + metric + numeric GO/MODIFY/STOP + downstream routing, the deferred phase is left uncommitted, and provenance is present.
```
