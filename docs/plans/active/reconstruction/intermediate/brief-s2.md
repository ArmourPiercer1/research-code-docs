# S2 Brief — target-architecture synthesis subagent (READY TO LAUNCH)

Write exactly five files (create nothing else), all under
`D:\AI_Coworking\skill-build\research-code-docs\docs\plans\active\reconstruction\phase1\`:

1. `target-workflow-invariants.md`
2. `target-capability-architecture.md`
3. `canonical-information-model.md`
4. `skill-change-matrix.md`
5. `eval-plan.md`

## Inputs (read in full)

- Charter: `docs\plans\active\research_software_agent_workflow_reconstruction_charter.md`
  — §8 (12 invariants), §9 (capability model), §10 (mechanism decisions), §11 (portfolio
  YAML schema), §12 (8 candidate changes), §14 (eval strategy), §16 (long-task rules),
  §17 (17 questions), §18 (non-goals), §20 (acceptance criteria).
- Phase 0: `..\phase0\current-system-map.md`, `..\phase0\existing-skill-classification.md`,
  `..\phase0\current-information-ownership-map.md`, `..\phase0\pain-point-evidence.md`.
- DSH intermediates: `..\intermediate\dsh-current-state-findings.md`,
  `..\intermediate\dsh-history-findings.md` (and `..\phase1\dsh-workflow-evidence-map.md`
  + `dsh-transferability-crosswalk.md` if present at launch; otherwise cite the
  intermediates directly and mark S1-dependent rows "PENDING-S1").
- `..\intermediate\parent-preliminary-answers.md` — parent's PRELIMINARY answers to the
  17 §17 questions from the initial audit. Use as a starting point: every answer you
  keep must be re-grounded in phase0 evidence (cite it); correct anything the phase0
  deliverables contradict; replace PENDING items with real answers.
- `..\intermediate\eval-coverage-baseline.md` — ground-truth per-skill case counts from
  the case YAMLs; your eval-coverage statements must match it.

Ground rules (charter §0, §15): this is an architecture PROPOSAL for review, not an
implementation. Prefer deleting/simplifying existing abstractions over adding new ones.
A new Skill is justified only if an agent must repeatedly apply non-trivial judgment or
orchestration (charter §10). Everything must trace to phase0 evidence or DSH evidence —
cite file:line / commit hash.

## File 1 — target-workflow-invariants.md

For each of the 12 charter §8 invariants: (a) exact statement; (b) current-system
compliance verdict for research-code-docs — SATISFIED / PARTIAL / VIOLATED — with
evidence from phase0 (which files, which duplication, which mixed-dimension status);
(c) proposed mechanical enforcement (schema / checker / test / CI / convention — name
concretely, e.g. "new checker: duplicate-fact-lint over the 14 canonical owners"), or
an explicit "judgment-only" with rationale; (d) the acceptance criterion(s) from §20
that verify it. End with the 17 charter §17 questions, each ANSWERED (not listed) based
on the phase0 findings — these answers constrain Files 2–5.

## File 2 — target-capability-architecture.md

Organize by the five §9 lifecycle families (repository / change / research / multi-agent
/ knowledge). For EVERY potential capability listed in §9 (and any the phase0 audit
shows is additionally needed): current-state mapping (which existing skill/checker/doc
covers it today, with citations), gap assessment, and the §10 mechanism-layer decision —
Skill / repository convention / AGENTS.md / schema / deterministic checker / test / CI
gate / Git-PR convention / canonical doc format / human approval boundary / external tool
/ no automation — with one-line justification (checker-enforceable things do NOT get a
skill; Git-recorded history does NOT get a second ledger). Then: the proposed vertical
slice for Phase 2 (charter §15 Phase 2) — one closed loop chosen so that it exercises the
highest-value new mechanisms, named end-to-end (inputs → capabilities → outputs → evals).

## File 3 — canonical-information-model.md

The charter §13 canonical-source map for the TARGET system. Table, one row per
information type (at minimum the §13 list: current repository state; project
architecture; package/module contracts; current roadmap/active routes; evidence;
experiment results/provenance; open decisions; durable decision rationale; execution
plans; task dependency graph; session handoff; incident history; implementation
history). Columns: information type | TARGET canonical owner (file/path convention) |
lifecycle (created → updated → archived → deleted) | update trigger | archive/delete
rule | allowed references (who may link in) | forbidden duplications (concrete current
examples from phase0 that this rule eliminates). Differences from the phase0 current
ownership map must be explicit deltas (add a "change vs current" column or callouts).

## File 4 — skill-change-matrix.md

The charter §11 proposed portfolio. Use the exact §11 YAML schema (name, problem,
current_owner, proposed_action keep|refine|merge|split|replace|add|remove,
why_this_must_be_a_skill, trigger, non_trigger, inputs, outputs, canonical_or_transient,
reads, writes, upstream, downstream, invariants, mechanical_checks, failure_modes,
evals, dsh_basis, research_specific_delta). One entry per: all 14 current skills, the 3
L1 control flows, the eval harness (as a component), and the 8 charter §12 candidate
changes (12.1–12.8 — each evaluated, with proposed_action, NOT assumed). proposed_action
must MATCH the phase0 classification label; where you disagree, say why with evidence.
Entries without a convincing `why_this_must_be_a_skill` must default to another
mechanism (name it) or removal.

## File 5 — eval-plan.md

The charter §14 strategy, concretized for THIS repo: (a) atomic skill evals — reuse the
existing injection mechanism (make_injection/make_batch/make_grading_injection) and case
YAML format; list which existing case files carry over, which new cases are required per
§14.1 (trigger, non-trigger, write-scope, interface, fact/hypothesis separation,
refuse-to-overclaim, checker compatibility, context boundedness); (b) workflow evals —
the four §14.2 scenarios (A messy repository, B greenfield, C competing research routes,
D long multi-agent task) with concrete inputs drawn from this repo's corpus
(tests/corpus/, docs/skill-development/ as corpus, DSH as greenfield reference);
(c) adversarial evals — the 12 §14.3 injected defects, each mapped to a detector
(checker/adjudicator/human) with the expected system behavior; (d) longitudinal evals —
the §14.4 simulated-iteration protocol with the nine tracked metrics, and what
"understandable after many changes" operationally means here. Define pass criteria and
the eval-runner cadence (which runs in preflight vs manual).

Header blocks for all five files: generated_by (phase1-target-synthesis-subagent),
inputs list, method, date (2026-09-09), status: DRAFT-for-review (architecture
proposal, pending human review per charter §15). English. Dense, citation-first.

## Reply format

Files written; §17 questions answered (17/17?); number of capabilities and their
mechanism-layer distribution; proposed_action distribution across the portfolio; the
Phase-2 vertical slice you proposed (3–5 lines); top 5 risks to the proposal.
