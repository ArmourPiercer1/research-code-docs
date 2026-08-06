# Sprint 6A — Batch-3 control-flow routing & conflict validation

<!--
generated_by_skill: (manual eval orchestration; per 2026-08-05 directive "Batch3后续_首个闭环垂直切片与分层测试节奏计划.md" §5)
skill_version: n/a
source_commit: 07b5306
source_documents:
  - docs/third-party-suggestions/Batch3后续_首个闭环垂直切片与分层测试节奏计划.md §5 (Sprint 6A)
  - evals/skills/trigger/{documentation-refactor,scientific-workspace-reconstruction,numerical-research-software-design}.yaml
  - evals/skills/conflict/{documentation-refactor,scientific-workspace-reconstruction,numerical-research-software-design}.yaml
  - docs/skill-development/conflict-matrix.md §1 (DENY/SEQ cluster) + §2 (research delegation)
status: DECIDED — PASS (27/27; 0 co-run violations; 0 SEQ order errors)
last_verified: 2026-08-05
document_lifecycle: IN_REVIEW
-->

> **Sprint 6A goal (directive §5):** run the three L1 flows' *already-authored* trigger/conflict cases through
> **isolated** evaluators; prove correct routing + that no DENY pair ever co-starts + that SEQ order holds.
> **This is NOT a promotion.** All three flows stay `experimental` + `auto_trigger: false` +
> `disable-model-invocation: true` + manual-only regardless of the result (directive §5.4).

## Method

- **3 isolated routing evaluators** (one per flow), each given the full skill catalog + conflict-matrix §1/§2
  routing rules + that flow's **9 authored case inputs** (`3 should-trigger + 3 should-not + 3 conflict`) with the
  `set` / `expected` / `notes` answer-key fields **stripped** — a true blind routing test. Each returns a
  per-case `PRIMARY` / `SECOND` decision + a `CO_RUN_VIOLATIONS` count.
- **3 independent reviewers**, each blind-spot-checking the **hardest DENY conflict** for one flow (they did not
  see the evaluator's answer). Concordance = the reviewer independently derives the same decision.
- **Slots: 6** (3 evaluators + 3 reviewers); **0 reruns** used (cap was ≤6 + ≤2 rerun = 8). No background workflow.
- **Denominator = 27**, not the directive's estimated 24: the authored conflict sets carry **3** cases per flow
  (not 2), so the real corpus is `3 × (3+3+3) = 27`. Reported faithfully.

## Result — PASS

| Flow | should-trigger | should-not (route target) | conflict | co-run violations |
|---|---|---|---|---|
| `documentation-refactor` | 3/3 | 3/3 (→ IA, → SWR, → DQE) | 3/3 | **0** |
| `scientific-workspace-reconstruction` | 3/3 | 3/3 (→ doc-refactor, → numerical, → forensics) | 3/3 | **0** |
| `numerical-research-software-design` | 3/3 | 3/3 (→ SWR, → RQLP, → doc-refactor) | 3/3 | **0** |
| **Total** | **9/9** | **9/9** | **9/9** | **0** |

### Conflict-case detail (the load-bearing rows)

| Case | Authored expected | Evaluator decision | Pass |
|---|---|---|---|
| docref-conf-01 | route_one (read-only pass + elicitor 1Q; then exactly one of {doc-refactor, numerical}) | PRIMARY=documentation-refactor, no co-run (docs named as blocker) | ✓ |
| docref-conf-02 | route_one → SWR then doc-refactor (SEQ) | PRIMARY=SWR, SECOND=SEQ:SWR-then-doc-refactor | ✓ |
| docref-conf-03 | hold_at_blocked (design plan, no inline move/rewrite) | PRIMARY=doc-refactor, SECOND=hold-at-BLOCKED:migrate/rewrite | ✓ |
| swr-conf-01 | route_one → SWR then doc-refactor (SEQ) | PRIMARY=SWR, SECOND=SEQ:SWR-then-doc-refactor | ✓ |
| swr-conf-02 | route_one → SWR then numerical (DENY) | PRIMARY=SWR, SECOND=DENY-defer:SWR | ✓ |
| swr-conf-03 | hold_at_blocked at architect | PRIMARY=SWR, SECOND=hold-at-BLOCKED:architect+migrate | ✓ |
| nrsd-conf-01 | route_one → SWR then numerical (DENY; numerical DEFERS) | PRIMARY=SWR, SECOND=DENY-defer:SWR | ✓ |
| nrsd-conf-02 | delegate → RQLP → lit-review (never self-retrieves) | PRIMARY=numerical, SECOND=delegate:RQLP→lit-review | ✓ |
| nrsd-conf-03 | hold_at_blocked at Batch-4 core | PRIMARY=numerical, SECOND=hold-at-BLOCKED:spec/architect (not built) | ✓ |

### Independent reviewer spot-checks — 3/3 concordant

| Hardest case | Independent reviewer decision | Matches evaluator? |
|---|---|---|
| docref-conf-01 (numerical idea in messy docs) | doc-refactor first; `CO_RUN_BOTH=no`; "request names its blocker, not the elicitor case" | ✓ |
| swr-conf-02 (numerical idea in messy workspace) | `FIRST=SWR, THEN=numerical, CO_RUN_BOTH=no` | ✓ |
| nrsd-conf-01 (numerical idea in messy workspace, arriving at numerical flow) | numerical **defers**; `FIRST=SWR, THEN=numerical, CO_RUN_BOTH=no` | ✓ |

## §5.3 pass conditions

| Condition | Target | Actual |
|---|---|---|
| Total routing correct | 24/24 (est.) | **27/27** (full authored corpus) |
| DENY pair co-start count | 0 | **0** |
| SEQ pair order errors | 0 | **0** |
| Ambiguity never launches two flows | 100% | **100%** (every DENY/ambiguous case = single flow, no co-run) |
| No flow enabled `auto_trigger` due to passing | required | **held** — all three stay experimental/manual-only |

## Honest notes

- **docref-conf-01 nuance (not a failure):** the authored gold framed this as "elicitor asks one routing
  question." Both the evaluator and the *independent* reviewer instead judged the phrasing ("buried inside a
  messy documentation set") to *name* the dominant artifact, so they routed documentation-refactor-first after a
  read-only pass — no separate elicitor question, and critically **no co-run**. This is within the authored
  `route_to` set ("exactly one of {doc-refactor, numerical}") and the safety property held, so it scores correct.
  Two independent contexts converging on the same call is the point of the spot-check.
- **Scope:** Sprint 6A only eliminates obvious routing errors. It is **not** promotion; no auto-trigger, no
  install, no DQE change, no Phase E (directive §5.4 / §11).

## Post-test status (unchanged, per §5.4)

```yaml
documentation-refactor: {status: experimental, auto_trigger: false, disable_model_invocation: true, invocation: manual-only}
scientific-workspace-reconstruction: {status: experimental, auto_trigger: false, disable_model_invocation: true, invocation: manual-only}
numerical-research-software-design: {status: experimental, auto_trigger: false, disable_model_invocation: true, invocation: manual-only}
```
