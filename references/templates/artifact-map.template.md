<!--
generated_by_skill: document-information-architect
skill_version: 0.1.0
source_commit: <repo@commit at generation time>
source_documents: [<hybrid doc or corpus>, <forensics inventory if present>, <PSR state report if present>]
status: CANDIDATE information architecture (a design plan; open decisions listed; no file moved, no prose rewritten)
last_verified: <YYYY-MM-DDTHH:MM:SSZ>
-->

# Artifact Map — <corpus-or-doc>

A **design plan**: where each responsibility and information-type should live. Nothing here is rewritten prose
or an executed file move — the split plan is a hand-off to `content-canonicalization-and-migration` (dry-run
first) and `technical-document-rewriter` (writes the target docs).

## Role inventory (what this material is carrying)
| role / responsibility | serving sections (evidence) | audience | update-frequency |
|---|---|---|---|
| long-term vision | §1, §2 | stakeholders | rare / on pivot |
| phase roadmap | §4 | implementers | per phase |
| live status/progress | §3, §5 | team | continuous (volatile) |
| ADR / rationale | §6 | future maintainers | append-on-decision |
| session/handover notes | §9 | none (transient) | one-time |

## Information-type → canonical home (one per type)
| info type | canonical home (target doc) | note |
|---|---|---|
| current behavior | code + state report | never copied into a stable doc |
| progress / status | status tracker | volatile → pointer only (HF-14b cure) |
| architecture rationale | ADR | why + rejected alternative |
| phase plan | roadmap | measurable DoD per committed phase |
| literature basis | evidence map (`research-evidence-synthesizer`) | E-levels; no project-fact upgrade |

## Target doc-set (one responsibility each)
| target doc | purpose (1 line) | audience | lifecycle | owns info-types |
|---|---|---|---|---|
| `vision.md` | why this project exists | stakeholders | living, rare | vision, non-goals |
| `roadmap.md` | phased plan + DoD | implementers | living per phase | phase plan |
| `status/state-report.md` | verified current state | team | continuous | current behavior, progress (canonical) |
| `adr/ADR-NNN.md` | one decision each | maintainers | append-only | rationale |

## Split & linking plan (existing section → target)
| existing section | → target doc | link left behind |
|---|---|---|
| `MEGA.md §3 status log` | `status/state-report.md` | MEGA links to state report (no copy) |
| `MEGA.md §6 decisions` | `adr/ADR-001…` | roadmap links to ADRs |
| `MEGA.md §9 session notes` | drop / archive | — (transient; raise as open decision) |

## Open decisions (for elicitor / decision-manager — do not pick silently)
1. Is the §9 session/handover material still needed, or archived?
2. Of `A.md` vs `B.md`, which is the canonical architecture doc?

## Coverage note
- Inputs used: <forensics inventory? PSR state?>. Assumptions marked **provisional (needs PSR)**: <…>.
- Every existing section is assigned above (or listed as an open decision).
