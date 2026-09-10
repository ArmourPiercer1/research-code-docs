# S1 Brief — DSH synthesis subagent (READY TO LAUNCH)

Write exactly two files (create nothing else):

1. `D:\AI_Coworking\skill-build\research-code-docs\docs\plans\active\reconstruction\phase1\dsh-workflow-evidence-map.md`
2. `D:\AI_Coworking\skill-build\research-code-docs\docs\plans\active\reconstruction\phase1\dsh-transferability-crosswalk.md`

## Inputs (read in full)

- Charter: `docs\plans\active\research_software_agent_workflow_reconstruction_charter.md`
  — §4, §5 (9-link evidence chain, §5.1 source priority, §5.2 questions, §5.3 table),
  §6 (negative evidence, 4 questions), §7 (transferability labels).
- `docs\plans\active\reconstruction\intermediate\dsh-current-state-findings.md`
- `docs\plans\active\reconstruction\intermediate\dsh-history-findings.md`
- For the "relevance here" judgment: `docs\plans\active\reconstruction\phase0\existing-skill-classification.md`
  and `docs\plans\active\reconstruction\phase0\pain-point-evidence.md` (if present at launch;
  if a phase0 file is missing, proceed and mark the relevance column
  "PENDING-PHASE0" for the affected rows).
- You may re-inspect `D:\deepseek-harness\` directly (read-only) to fill citation gaps —
  never invent; prefer the two intermediate files, verify against the repo when in doubt.

## File 1 — dsh-workflow-evidence-map.md

One section per DSH mechanism (cover at minimum every mechanism in the two intermediate
files; verified reality: 11 skills in `.agents/skills/` — dsh-archive-agent-notes,
dsh-ci-test-reliability, dsh-code-review, dsh-doc, dsh-find-simplifications,
dsh-merging-stacked-prs, dsh-pre-push-checks, dsh-prose-standard, dsh-translate-docs,
dsh-trim-cot-leakage, record-browser-gif; `.agents/notes/` (~2555 files); root+subtree
AGENTS.md; docs/AGENTS.md, docs/testing.md, docs/architecture.md, docs/postmortem/;
.github/workflows (ci.yml, ci-master.yml, e2e.yml, expected-filenames.yml, …) +
.gitlab-ci.yml; repo-root snapshots/; pre-push/test-selection scripts; stacked-PR/worktree
practice). For each mechanism, complete the charter §5 nine links:

```text
observed DSH mechanism → problem it was solving → historical evidence the problem
mattered → how DSH encoded the solution → how the solution evolved → what later got
removed or simplified → whether the same problem exists here → what generic principle
is transferable → what must NOT be copied
```

Every link must carry at least one citation (file:line or commit hash) from the
intermediate files or the DSH repo. Close the file with: (a) a merged NEGATIVE-EVIDENCE
summary (deletions/simplifications with the charter §6 four answers), and (b) the
"DSH keeps both .claude/ and .agents/" observation and its meaning for multi-platform
layout (evidence-cited).

## File 2 — dsh-transferability-crosswalk.md

The charter §5.3 table, at minimum these columns, one row per mechanism in File 1:

| DSH mechanism | Original problem | Historical evidence | Generic principle | Relevance here | Proposed adaptation | DSH-specific parts to reject |

Plus: a §7 label per row — `DIRECTLY TRANSFERABLE` / `TRANSFERABLE AFTER GENERALIZATION`
/ `RESEARCH-SPECIFIC ADAPTATION REQUIRED` / `DSH-SPECIFIC — DO NOT COPY` — with one line
of reasoning each (use the charter §7 example reasoning as the calibration bar). Remember:
"DSH has this Skill" is NOT sufficient justification for creating an equivalent skill in
research-code-docs; rows whose honest label is DSH-SPECIFIC must say what (if anything)
research-code-docs needs instead (possibly: nothing).

Header blocks for both files: generated_by (phase1-dsh-synthesis-subagent), inputs list,
method, date (2026-09-09), status: DRAFT-for-review. English. Dense, citation-first.

## Reply format

Files written; number of mechanisms covered; label distribution (how many of each §7
label); the 5 mechanisms with the strongest case for adaptation and the 5 with the
strongest case for rejection (one line each).
