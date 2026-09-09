<!--
generated_by_skill: research-question-and-literature-planner
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<the open research question>, <originating decision/goal if any>]
artifact_type: literature-search-plan
document_lifecycle: IN_REVIEW
scope: <one line: what question this scopes; excludes retrieval/summary/synthesis (delegated)>
facts: none (no retrieval performed; seeds are labeled "to confirm — not findings")
hypotheses: <pointer+count to the decision-tied questions the search will inform>
open_questions: <pointer+count to the questions + transfer warning retrieval must resolve; never 'none'>
evidence_level: <target E-standard the question can support, e.g. "E2 cap (cross-domain → analogy/indirect)">
next_handoff: <lit-review | wos-research | deep-research | paper-fetch-skill>
handoff_requirements: <what retrieval needs: seed query + in/out scope + inclusion/exclusion + stop criterion>
status: search plan (scoping artifact; NO retrieval performed, NO papers read)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Search Plan — <topic>

A **scoping artifact**, produced *before* retrieval. It contains no retrieved papers and no summaries — the
named retrieval skill executes it.

## Question(s) + the decision they inform
- Refined question: <answerable question>
- Decision it informs: <why we are searching — what choice this feeds>

## Scope (in / out)
- **In:** <domains, sub-topics, time window, venues, languages>
- **Out:** <explicitly excluded — a scope of "everything" is a defect>

## Inclusion / exclusion criteria
| include if | exclude if |
|---|---|
| <study type / method match / recency / relevance> | <off-topic / below quality floor / wrong domain> |

## Stop criteria (pick one, make it explicit)
- <saturation: no new methods in N consecutive sources | fixed budget of N sources | coverage of top-K venues>

## Evidence / quality standard (→ E0–E5)
- Strong evidence for this question = <…> (E-level it can support)
- Weak/indirect = <…>
- **Transfer warning:** <if cross-domain: this question can only get analogy/indirect evidence → set expectations; becomes the synthesizer's transfer-assumption input>

## Expected evidence types
- <benchmarks / proofs / empirical studies / method papers / reviews>

## Route (delegate retrieval — this skill stops here)
- **Chosen:** <lit-review | wos-research | deep-research | paper-fetch-skill>
- **Why it (not the others):** <justification; deep-research only for multi-source web fan-out>
- Seed query / seeds handed over: <…>

`ROUTE retrieval=<skill> because=<one line>`
