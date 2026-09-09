# Research-Software Documentation Skills System — Phase 0 Audit & Phase 1 Architecture Proposal (de-identified)

**What the system is.** An internal agent-skills system for research-software documentation governance: 14 manual-only skills, 3 L1 control flows, deterministic checkers, an eval harness, and a DQE advisory evaluator (an LLM-judged documentation-quality evaluator whose verdicts advise but never gate).

**What these 11 documents are.** Phase 0: a read-only audit of the current system (a current-system map, a per-skill classification, an information-ownership map, and pain-point evidence). Phase 1: a study of a separately-maintained reference agent-harness codebase ("DSH") — a per-mechanism evidence map (M1–M32) and a transferability crosswalk — plus a proposed target architecture (workflow invariants incl. 17 answered questions, a capability architecture, a canonical information model, a skill-change portfolio, and an eval plan) submitted for human review.

## Reading order for a reviewer

1. `phase0/pain-point-evidence.md` — why bother: the measured costs (P1–P10) that motivate the reconstruction.
2. `phase1/dsh-transferability-crosswalk.md` — what to borrow from DSH, mechanism by mechanism (M1–M32, labeled DT / TAG / RSA / DN).
3. `phase1/target-workflow-invariants.md` — the proposed rules, incl. the 17 answered questions (Q1–Q17).
4. `phase1/skill-change-matrix.md` — the proposed portfolio (every current skill evaluated; new additions justified).
5. `phase1/eval-plan.md` — how the target would be validated.

Supporting detail, in dependency order: `phase0/current-system-map.md`, `phase0/existing-skill-classification.md`, `phase0/current-information-ownership-map.md`, `phase1/dsh-workflow-evidence-map.md`, `phase1/target-capability-architecture.md`, `phase1/canonical-information-model.md`.

## Sanitization note

Only de-identification substitutions were applied; no content was restructured, summarized, or re-flowed. Each file carries a `sanitization:` line in its header. Replaced: local absolute paths → `<repo-root>` / `<dsh-checkout>` / `<user-home>` / `<local-path>`; the project's own repository names (current and former) → `the project` / `<former-repo-name>`; the reference system's company name → `the DSH project` (the neutral acronym DSH is kept); one personal research-corpus directory name → `<personal-research-corpus>`. Everything else is verbatim: evidence quotes (incl. Chinese), IDs (D1–D19, M1–M32, P1–P10, I1–I12, Q1–Q17, C1–C15, A1–A10, S/H/G items), commit hashes, dates, token counts, third-party attributions (mattpocock, addyosmani, Master-cai, Imbad0202 and their repos/licenses), and platform names (Claude Code, GitHub, Web of Science, OpenAlex, etc.).

## Status

DRAFT proposal awaiting internal human review; no implementation started.
