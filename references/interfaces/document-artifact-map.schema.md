<!--
generated_by_skill: (manual, Batch-2.5 interface freeze per 2026-08-05 directive §5)
skill_version: n/a
source_commit: 7919bc4 (workspace HEAD at freeze time)
source_documents: [references/interfaces/README.md, references/templates/artifact-map.template.md, .claude/skills/document-information-architect/SKILL.md]
document_lifecycle: ACCEPTED
status: DECIDED (frozen interface v1)
last_verified: 2026-08-05
-->

# Interface schema — `document-artifact-map`

Produced by **`document-information-architect`**. Intended consumers are
**`content-canonicalization-and-migration`** and **`technical-document-rewriter`** — **both are Batch-5 and
not built yet**, so in Batch 2.5 this artifact's `next_handoff` is an **honest BLOCKED marker** (directive §9,
§10.1). See [README.md](README.md) for the common header + rules.

## Specialization of the frozen header

| field | value for this artifact |
|---|---|
| `artifact_type` | `document-artifact-map` |
| `facts` | **`none (...)`** — an artifact map is a **design plan**, not a fact record. Fact-dependent home assignments are marked **provisional (needs PSR)**, not asserted. |
| `hypotheses` | pointer+count to the *provisional* assignments (home choices that depend on a PSR fact not yet verified). |
| `open_questions` | pointer+count to the *Open decisions* (canonical-home ambiguities left for a human — never picked silently). Never "none" if any ambiguity exists. |
| `evidence_level` | `n/a (design plan; makes no evidence claim)`. |
| `next_handoff` | **`BLOCKED:content-canonicalization-and-migration, technical-document-rewriter (Batch 5 — not built)`** — the runnable doc-refactor prefix ends here. The plan is complete and handed to a human / DQE-advisory for review, not executed. |
| `handoff_requirements` | what a (future) migration/rewriter skill will need: the target doc-set, the per-type canonical home, the split & linking plan, and the resolved open decisions. |

## Handoff rule

- **A plan, never an execution.** The map assigns homes and a split plan but does **not** move, rewrite, or
  delete files. An artifact map that reports a file was moved/rewritten is an `INTERFACE_DEFECT` (lane
  violation) — the directive §7 forbids IA executing move/rewrite/delete.
- **One canonical home per information-type** (the HF-13 cure); **volatile state is a pointer, never copied**
  into a stable doc (the HF-14b cure). A map that copies volatile counts into a stable target is a
  `SKILL_DEFECT`.
- Because the downstream capability does **not exist**, `next_handoff` is `BLOCKED:<missing-capability>`.
  This is a correct, honest stop — a `MISSING_CAPABILITY`, not a failure (directive §10.1).

## Conformant header example

```yaml
---
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: 7919bc4
source_documents: [.../inventory-report.md, .../project-state-report.md, .../goal-scope-note.md]
artifact_type: document-artifact-map
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05T12:00:00Z
scope: "Target information architecture for the docs/skill-development corpus; a plan only — no file moved/rewritten."
facts: "none (a design plan; fact-dependent home assignments flagged 'provisional (needs PSR)')"
hypotheses: "5 provisional home assignments — see 'Coverage note'"
open_questions: "3 canonical-home ambiguities — see 'Open decisions'"
evidence_level: "n/a (design plan; no evidence claim)"
next_handoff: "BLOCKED:content-canonicalization-and-migration, technical-document-rewriter (Batch 5 — not built)"
handoff_requirements: "A future migration/rewriter needs the target doc-set + per-type home + split/linking plan + resolved open decisions."
---
```
