# Research-Software Documentation Skills System — Phase 0 Audit & Phase 1 Architecture Proposal (de-identified)

**What the system is.** An internal agent-skills system for research-software documentation governance: 14 manual-only skills, 3 L1 control flows, deterministic checkers, an eval harness, and a DQE advisory evaluator (an LLM-judged documentation-quality evaluator whose verdicts advise but never gate).

**What these 14 documents are.** Phase 0: a read-only audit of the current system (a current-system map, a per-skill classification, an information-ownership map, and pain-point evidence). Phase 1: a study of a separately-maintained reference agent-harness codebase ("DSH") — a per-mechanism evidence map (M1–M32) and a transferability crosswalk — plus a proposed target architecture (workflow invariants incl. 17 answered questions, a capability architecture, a canonical information model, a skill-change portfolio, and an eval plan) submitted for human review. Repair round (2026-09-10): an external review produced a 12-item repair contract (R1–R12); every item was verified against the current repository state and executed in place — the five Phase-1 documents above were revised, and three new documents were added (a post-audit reconciliation, a revised Phase-2 vertical slice, and a per-item review disposition).

## Reading order for a reviewer

1. `post-audit-reconciliation.md` — where the system actually stands now: which audit defects the current main already resolved, which are partial, and which are still live (with current evidence).
2. `architecture-review-disposition.md` — the per-item disposition of the 12 repair items (decision, evidence, change made, residual risk) plus the 12-point consistency pass and the final gate status.
3. `revised-phase2-vertical-slice.md` — the current Phase-2 slice: one real simplification end-to-end (simplification-audit → one candidate → decision note → implementation → focused verification → two-axis review), with the minimum checker set.
4. `phase0/pain-point-evidence.md` — why bother: the measured costs (P1–P10) that motivate the reconstruction.
5. `phase1/dsh-transferability-crosswalk.md` — what to borrow from DSH, mechanism by mechanism (M1–M32, labeled DT / TAG / RSA / DN).
6. `phase1/target-workflow-invariants.md` — the proposed rules, incl. the 17 answered questions (Q1–Q17).
7. `phase1/skill-change-matrix.md` — the proposed portfolio (every current skill evaluated; new additions justified).
8. `phase1/eval-plan.md` — how the target would be validated.

Supporting detail, in dependency order: `phase0/current-system-map.md`, `phase0/existing-skill-classification.md`, `phase0/current-information-ownership-map.md`, `phase1/dsh-workflow-evidence-map.md`, `phase1/target-capability-architecture.md`, `phase1/canonical-information-model.md`.

## Sanitization note

Only de-identification substitutions were applied; no content was restructured, summarized, or re-flowed. Each file carries a `sanitization:` line in its header. Replaced: local absolute paths → `<repo-root>` / `<dsh-checkout>` / `<user-home>` / `<local-path>`; the project's own repository names (current and former) → `the project` / `<former-repo-name>`; the reference system's company name → `the DSH project` (the neutral acronym DSH is kept); one personal research-corpus directory name → `<personal-research-corpus>`. Everything else is verbatim: evidence quotes (incl. Chinese), IDs (D1–D19, M1–M32, P1–P10, I1–I12, Q1–Q17, C1–C15, A1–A10, S/H/G items), commit hashes, dates, token counts, third-party attributions (mattpocock, addyosmani, Master-cai, Imbad0202 and their repos/licenses), and platform names (Claude Code, GitHub, Web of Science, OpenAlex, etc.).

## Status

DRAFT proposal. Repair round complete (2026-09-10): all 12 review items dispositioned (12/12 consistency pass; final gate 14/14 with ONE explicitly open item — the D-1 human ruling on the canonical "what is next" owner, which the revised slice leaves in `proposed/` for the reviewer to decide). No implementation started.
