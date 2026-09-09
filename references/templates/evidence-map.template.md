<!--
generated_by_skill: research-evidence-synthesizer
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<retrieved evidence bundle / literature-ingest store>, <the design decision it informs>]
artifact_type: research-evidence-map
document_lifecycle: IN_REVIEW
scope: <one line: which decision this organizes evidence for; no retrieval; no fact upgrade>
facts: none (paper/analogy capped ≤ E2; any in-project trial isolated at its own level — D.8)
hypotheses: <pointer+count to claim–evidence matrix rows (E-level + channel each)>
open_questions: <pointer+count to Unresolved gaps (mark any routed back to RQLP); never 'none' if a gap exists>
evidence_level: <max E-level, capped by channel: cross-domain-analogy ≤ E2; unevidenced assumption = E0>
next_handoff: uncertainty-and-decision-manager
handoff_requirements: <what the register needs: per-claim E-level+channel + transfer card assumptions+E-cap + unresolved gaps>
status: evidence map (CANDIDATE-level; no project-verified fact asserted; nothing retrieved here)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Evidence Map — <topic / decision>

Design-decision-facing. Every source→claim link carries an **E-level + channel**; paper/analogy evidence is
**never** presented as a project-verified fact (constraint D.8). This organizes retrieved evidence; it does not
retrieve, and it does not assign the final DECIDED status (that is `uncertainty-and-decision-manager`).

## Source inventory (read-only; nothing searched-for here)
| handle | what it claims | setting/domain | channel to our problem |
|---|---|---|---|
| [S1] Author 2019 | method M converges under assumption A | matrix manifolds | cross-domain-analogy |

## Claim–evidence matrix
| candidate claim | supports | contradicts | E-level | channel |
|---|---|---|---|---|
| M is applicable to our solver | [S1],[S3] | [S4] | E2 (cap) | cross-domain-analogy |
| tolerance τ suffices | [S2] | — | E1 | project-inference |

## Method-transfer cards
### Card: method M (matrix-manifold origin → our implicit-constraint solver)
- **Origin setting:** <where M is established>
- **Our setting:** <our problem>
- **Assumptions the transfer relies on:** <A1 smoothness, A2 constraint qualification, …>
- **Evidenced vs assumed:** A1 evidenced by [S1]; A2 **assumed** (no source) → gap G2
- **E-level cap:** E2 — capped by the weakest (unevidenced) assumption; NOT a direct/project fact

## Unresolved gaps (+ what would close each)
| # | gap | what closes it |
|---|---|---|
| G2 | A2 (constraint qualification) untested in our setting | a direct in-project experiment, or a same-domain source |

## Coverage note
- Sources used: <…>. Evidenced vs assumed split stated per card. Decisions routed to the register
  (`uncertainty-and-decision-manager`), not decided here.
