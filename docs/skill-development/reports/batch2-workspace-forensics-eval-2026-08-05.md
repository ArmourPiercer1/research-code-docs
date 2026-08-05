<!--
generated_by_skill: (manual, Batch-2 light eval round per 2026-08-05 directive §8)
skill_version: workspace-forensics-and-inventory 0.1.0
source_commit: 975e930 (workspace HEAD at eval time; internal report)
source_documents:
  - .claude/skills/workspace-forensics-and-inventory/SKILL.md
  - evals/skills/{trigger,conflict,reader-tests}/workspace-forensics-and-inventory.yaml
  - evals/skills/results/workspace-forensics-and-inventory/shadow/inventory-tests-corpus-2026-08-05.md
  - docs/third-party-suggestions/Research-Code-Docs当前进展_阻塞项与下一阶段开发计划.md §8 (light test spec)
status: DECIDED (light round PASSED; skill stays experimental + manual-only)
last_verified: 2026-08-05
-->

# Batch 2 · `workspace-forensics-and-inventory` v0.1.0 — Light Eval Round

> **Result: PASS.** Trigger 8/8, one real read-only shadow run (`tests/corpus/` — verified untouched),
> one no-context reader test (actionable + no over-claim), and a clear value-add over a no-skill baseline.
> The skill stays **experimental + `disable-model-invocation: true`** (manual/orchestrator-only) — the light
> round validates *advisory manual use*, not auto-trigger. Tested via injected-prompt sub-agents; nothing
> installed or pushed.

## 0. What this skill is

The read-only **inventory** front of the workspace / doc-refactor chains: it enumerates + classifies raw
artifacts by structural signal (entry-point candidates, tests, experiment scripts, results, caches, data,
docs), flags orphan/unreferenced candidates, and nominates CANDIDATE canonical sources — **without moving/
deleting/modifying anything and without asserting what runs**. It feeds `project-state-reconstructor`, which
does the verified FACT/UNKNOWN interpretation (conflict-matrix §67, previously PROJECTED, is now real).

## 1. Test posture (light, per directive §8)

Deliberately NOT DQE's heavy corpus. First round = 3 should-trigger · 3 should-not · 2 boundary/conflict ·
1 real shadow run · 1 no-context reader test · 1 no-skill comparison. Regression cases are added only after a
**real** failure appears.

## 2. Trigger + boundary routing — 8/8

A fresh sub-agent injected with the SKILL.md only (no other governance docs) routed all 8 cases correctly:

| id | input (abbrev) | expected | got |
|---|---|---|---|
| wfi-trig-01 | "inventory this inherited repo, read-only" | ENGAGE | ENGAGE ✅ |
| wfi-trig-02 | "map entry points / orphans / unreferenced results" | ENGAGE | ENGAGE ✅ |
| wfi-trig-03 | "catalog docs by type, flag overlap/contradiction" | ENGAGE (corpus mode) | ENGAGE ✅ |
| wfi-not-01 | "review src/solver.py for bugs" | ROUTE code-review | ROUTE code-review ✅ |
| wfi-not-02 | "fix this KeyError" | ROUTE diagnosing-bugs | ROUTE diagnosing-bugs ✅ |
| wfi-not-03 | "design how to split ROADMAP.md" | ROUTE document-information-architect | ROUTE d-i-a ✅ |
| wfi-conf-01 | "what actually runs + is tested, with evidence" | ROUTE project-state-reconstructor | ROUTE PSR ✅ |
| wfi-conf-02 | "delete orphans and move results into archive/" | ROUTE workspace-migration-planner | ROUTE migration ✅ |

The two boundary cases are the ones that define forensics' identity: **read-only vs verified-state** (→ PSR)
and **read-only vs mutate** (→ migration-planner). Both routed correctly.

## 3. Real shadow run — `tests/corpus/` (read-only)

A fresh sub-agent injected with the SKILL.md produced a full inventory of the DQE test corpus. Output:
`evals/skills/results/workspace-forensics-and-inventory/shadow/inventory-tests-corpus-2026-08-05.md`.

- **Read-only proven, not trusted:** `git status --porcelain tests/corpus/` = empty after the run (the
  working tree under the target was untouched). The report itself confirms `git status` was clean.
- **Discipline held:** every classification is `path → signal`; `blind-runs/`/`results/` labeled **GENERATED**;
  `upstream/` (~444 MB clones) correctly summarized-only per the context budget; file trust tiers assigned;
  a Coverage note present.
- **Found real candidates:** a plan/case coverage gap (`GN-EVIDENCE-BARE-CLAIM-001` has no matching
  `mutations/plans/` entry), two empty placeholders, and quarantine `-v1` supersede candidates — each with the
  search that surfaced it, and each **handed to PSR to confirm** rather than asserted.
- **No over-claim:** it explicitly states nothing is "verified as running" and that gold `expected.*` fields
  are recorded expectations, "not evidence that DQE currently produces that result."
- HARD checker (front-matter + status vocab) on the output = green.

## 4. No-context reader test — PASS

A separate fresh reader, given ONLY the inventory report, answered the two-layer protocol and emitted:

```
READER_CAN_ACT=YES        # could list mode, entry-point candidates, 5 orphan candidates, 7-item PSR handoff
OVERCLAIM_DETECTED=NO     # could NOT conclude any code "runs"/tests "pass" from the report alone
```

This is the inverse of the DQE reader test: a correct inventory must be **actionable** yet must **not** let a
reader over-conclude that anything verifiably runs. Both conditions held.

## 5. No-skill baseline comparison — skill adds value

A no-skill sub-agent inventoried the same `tests/corpus/` (also read-only). It produced a good *narrative*
summary, but:

| dimension | no-skill baseline | with the skill |
|---|---|---|
| candidate + signal tagging | ✗ (asserts "flows in one direction", "provenance is rigorous" as fact) | ✓ every classification `→ signal` |
| GENERATED hygiene | partial (mentions outputs) | ✓ explicit "GENERATED — never a source of truth" |
| orphan / unreferenced candidates | ✗ none | ✓ 5, each with the cited search |
| candidate canonical sources | ✗ | ✓ per info-type, tagged CANDIDATE |
| file trust tiers | ✗ | ✓ Trusted / Verify / Untrusted |
| coverage note | ✗ (no scanned-vs-skipped) | ✓ structured |
| PSR handoff / unknowns | ✗ | ✓ 7 items |
| over-claim risk | narrates the D-16/D-17 story as fact | defers to PSR; no run/pass claim |

The baseline is a fine read; the skill's added value is precisely the **inventory discipline** (candidate-not-
claim, hygiene, handoff) that keeps the artifact usable by the downstream fact-recovery step without smuggling
in unverified interpretation.

## 6. Verdict + honest scope

- **Light round: PASS.** The skill triggers correctly, respects read-only + the context budget, produces a
  disciplined inventory, and beats no-skill on the dimensions that matter.
- **Stays manual-only.** `disable-model-invocation: true`; the round validates advisory use, not auto-trigger.
- **Not yet exercised:** document-corpus mode on a real messy doc corpus (only workspace mode was shadow-run);
  a second real workspace. Add these — and any regression case — when a real need/failure appears (directive
  §8), not preemptively.
- Nothing installed or pushed.
