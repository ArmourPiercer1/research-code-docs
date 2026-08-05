<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents:
  - docs/third-party-suggestions/Batch2_5集成冲刺与Batch3最小控制流开发计划.md (§5 minimal interface freeze, §7 exit conditions)
  - references/templates/*.template.md (the artifact bodies this header sits on)
  - evals/skills/harness/checkers/frontmatter_check.py (HF-9 required keys + aliases)
  - docs/skill-development/system-architecture.md §7 (status + evidence vocabulary)
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1; fields + semantics + handoff rules locked; layout/wording NOT frozen)
last_verified: 2026-08-05
-->

# Frozen Handoff Interfaces (`batch2.5-v1`)

> **What is frozen (directive §5.2):** the **fields**, their **semantics**, the **handoff rules**, and the
> **required/optional** relationships of the seven inter-skill artifacts. **What is NOT frozen:** Markdown
> layout, heading style, exact wording, and non-critical extra fields. A downstream skill must be able to
> consume an upstream artifact **from the artifact alone — no chat context** (directive §5.1, §7).

This freeze exists so Batch 2.5's two real integration chains (document-corpus chain and research-evidence
chain) can be validated at the **interface**, not re-tested as single skills. It is deliberately minimal — the
smallest contract that lets one skill's output be consumed by the next.

## The seven frozen interfaces

| `artifact_type` | produced by | consumed by (this system's chains) |
|---|---|---|
| `inventory-report` | `workspace-forensics-and-inventory` | `project-state-reconstructor` |
| `project-state-report` | `project-state-reconstructor` | `goal-scope-and-workflow-elicitor`, `document-information-architect` |
| `goal-scope-note` | `goal-scope-and-workflow-elicitor` | `document-information-architect`, `research-question-and-literature-planner`, `uncertainty-and-decision-manager` |
| `document-artifact-map` | `document-information-architect` | `content-canonicalization-and-migration`, `technical-document-rewriter` *(Batch 5 — not built yet → honest BLOCKED handoff)* |
| `literature-search-plan` | `research-question-and-literature-planner` | `lit-review` / `wos-research` / `deep-research` / `paper-fetch-skill` (installed retrieval) |
| `research-evidence-map` | `research-evidence-synthesizer` | `uncertainty-and-decision-manager` |
| `decision-register` | `uncertainty-and-decision-manager` | `documentation-quality-evaluator` (advisory), human/orchestrator |

Each has a `<name>.schema.md` in this directory that specializes the common header below.

## The common frozen header (every handoff artifact carries this)

Every handoff artifact carries these fields in its front-matter block (a YAML `---` header **or** a leading
`<!-- -->` HTML comment — both are accepted, matching `frontmatter_check.py`). Content-bearing fields
(`facts`/`hypotheses`/`open_questions`) are **short pointers + counts into the body**, not the full content —
they tell a downstream reader *where to look* and *how many*, so nothing is silently dropped.

```yaml
# ---- FROZEN HANDOFF INTERFACE (batch2.5-v1) ----
# Identity + provenance (these also satisfy HF-9 frontmatter_check):
generated_by_skill:   # REQUIRED. The producing skill. Interface alias: produced_by_skill (either accepted).
skill_version:        # REQUIRED. Producing skill's version, e.g. 0.1.0.
source_commit:        # REQUIRED. repo@commit at generation time.
source_documents:     # REQUIRED, non-empty. Upstream artifact path(s) / corpus root this was built FROM.
                      #   Interface alias: source_artifacts (either accepted). This is the traceability spine.
# Interface classification + state:
artifact_type:        # REQUIRED. Exactly one of the seven names above.
document_lifecycle:   # REQUIRED. DRAFT | IN_REVIEW | ACCEPTED | DEPRECATED (also satisfies HF-9 'status').
last_verified:        # REQUIRED. ISO-8601 timestamp.
# Payload pointers (locate, don't inline):
scope:                # REQUIRED. One line: what this artifact covers AND what it deliberately excludes.
facts:                # REQUIRED. Pointer+count to VERIFIED-fact rows, or the literal "none (<why>)".
hypotheses:           # REQUIRED. Pointer+count to hypothesis/candidate rows, or "none (<why>)".
open_questions:       # REQUIRED. Pointer+count to open/unknown/gap items. MUST reflect the body — if the
                      #   body has ≥1 open item, this may NOT be "none" (open questions never silently drop).
evidence_level:       # REQUIRED. Max/overall E-level carried (E0..E5), or "n/a (<why — no evidence claims>)".
# Handoff contract:
next_handoff:         # REQUIRED. Downstream skill name, OR "human decision", OR "BLOCKED:<missing-capability>".
handoff_requirements: # REQUIRED, non-empty. What the downstream must have/do to consume this (explicit).
# ---- END FROZEN HANDOFF INTERFACE ----
```

### Field rules (directive §5.1)

1. **Source-traceable.** `source_documents` (≡ `source_artifacts`) is non-empty and names real upstream
   artifacts or the corpus root — never "chat" or "the conversation".
2. **Status vocabulary consistent.** `document_lifecycle` is a legal token; any `E`-level is `E0..E5`; any
   claim STATUS in the body is from the fixed set (`system-architecture.md §7`). `status_vocab_check`
   enforces the tokens.
3. **Downstream can locate.** `facts`/`hypotheses`/`open_questions` point to named body sections + give a
   count, so the consumer finds the payload without reading chat.
4. **No chat dependence.** A fresh reader with only this artifact can act on it.
5. **Missing ≠ false / done / verified.** A required field is never blank or a placeholder. "Nothing here"
   is expressed as an explicit `none (<why>)` / `n/a (<why>)` — an *asserted* absence, not a gap.
6. **Downstream requirements explicit.** `handoff_requirements` says what the next skill needs (inputs,
   confirmations, access) to proceed.
7. **Open questions never silently drop.** If the body carries open items, `open_questions` reflects them.
   `interface_check.py` cross-checks this.

## Checker

`evals/skills/harness/checkers/interface_check.py` validates any file that **declares** `artifact_type:` in
its front-matter against this contract (files without `artifact_type` are skipped — the checker is opt-in, so
it is safe to run over a whole directory). It accepts the aliases `produced_by_skill`↔`generated_by_skill`
and `source_artifacts`↔`source_documents`, so it does **not** require changing the HARD `frontmatter_check`.

`interface_check` is registered in `run_checks.py` as an **ADVISORY** check for the interface artifacts (it
does not gate the HARD exit code, which stays `frontmatter_check` + `status_vocab_check`); run it with
`--advisory-is-hard` when you want the interface contract enforced as a blocker (as the Batch-2.5 chains do).

## Not frozen

Layout, heading order, prose, and extra fields a skill finds useful (e.g., the inventory's `Coverage note`,
the evidence map's `Method-transfer cards`). Add fields freely; do not remove or re-mean a frozen one without
a new interface version (`batch2.5-v2`).
