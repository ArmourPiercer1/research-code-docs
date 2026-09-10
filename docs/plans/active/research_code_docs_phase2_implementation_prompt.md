# Research-Code-Docs — Phase 2 Implementation Prompt

> Repository: `ArmourPiercer1/research-code-docs`
>
> Approved baseline: `1dc6b8694dac60ac355b8094e61ffebde322fba0`
>
> Review status:
>
> ```text
> Phase 1 architecture: ACCEPTED
> Phase 2 implementation: GO
> ```
>
> This prompt authorizes **Phase 2 only**. It does not authorize Phase 3 expansion.

## 0. Mission

Implement and execute the revised Phase-2 vertical slice defined by:

```text
docs/reconstruction-external-review/revised-phase2-vertical-slice.md
```

The purpose of Phase 2 is to prove one real closed loop:

```text
recover current reality
→ identify one evidence-backed simplification
→ capture the durable decision
→ implement the simplification
→ run the narrowest sufficient verification
→ review against standards + originating contract
→ update canonical owners in the same change
```

Do not broaden Phase 2 into a general rewrite of the repository.

## 1. Mandatory Stage 0 — recapture the real slice-start state

Before writing implementation code:

1. Verify the local base commit is the approved baseline or a descendant whose intervening changes are fully understood:

```text
1dc6b8694dac60ac355b8094e61ffebde322fba0
```

2. Record `git status`, `git diff`, `git ls-files`, and `git check-ignore` for the paths Phase 2 will touch.

3. `docs/plans/` contains important local/untracked planning state. Before staging, moving, or editing it:
   - inventory it;
   - hash the existing files;
   - identify which files are canonical active/archive state;
   - keep `docs/plans/local/**` and `docs/plans/scratch/**` untracked;
   - never delete an untracked file merely because Git does not know about it.

4. Re-census **all current references** to:
   - `docs/skill-development/creation-roadmap.md`
   - `creation-roadmap.md`

   using repository search (`git grep`, `rg`, or equivalent).

   Classify every match as:
   - `CURRENT-AUTHORITY / CURRENT-POINTER`
   - `HISTORICAL-PROVENANCE`
   - `FROZEN-RESULT / FIXTURE`
   - `PLAIN-TEXT HISTORY`
   - `DEAD / STALE`

   Do not trust the old Phase-2 example that says there is exactly one inbound reference or that it is `DQE SKILL.md:9`.

   The current repository state is authoritative.

5. Recompute the Phase-2 before-state table from the actual baseline. Historical counts in the proposal are examples/evidence, not executable constants.

If the real state materially invalidates the selected simplification candidate, stop and report BLOCKED with evidence. Do not force the fixture to fit the plan.

## 2. Binding implementation clarifications from final audit

These clarify remaining cross-document inconsistencies without reopening the architecture.

### 2.1 A8 must not depend on deferred `dependency-graph-lint`

The generic portfolio text still names `dependency-graph-lint` as an upstream/mechanical source for `simplification-audit`, while the revised slice defers that checker to Phase 3.

For **Phase-2 A8**, use:

```text
PSR state recovery
+ WFI inventory / document-corpus map
+ deterministic repo search / reference census
+ consumer classification by the A8 skill
```

Do not pull `dependency-graph-lint` into Phase 2 merely to satisfy the stale generic dependency line.

Later phases may enrich A8 with the canonical dependency graph.

### 2.2 A9 must not depend on deferred dependency graph

For **Phase-2 focused-verification**, compute the mechanical scope from:

```text
git diff / changed paths
+ the explicit Phase-2 change contract
+ existing registry/known path ownership where available
```

The selection judgment remains in `focused-verification`.

Do not implement the Phase-3 `dependency-graph-lint` as a prerequisite.

The Phase-2 `change-scope` component may be a small internal/helper component of `canonical-impact-lint` / `focused-verification`; do not create a standalone permanent abstraction unless it earns independent use.

### 2.3 Do not introduce a generic mixed `status` field into the new decision schema

The accepted state model is:

```yaml
object_type:
epistemic_state:
decision_state:
evidence_level:
evidence_state:
implementation_state:
```

When materializing D-1 and the new register, do **not** copy an extra generic:

```yaml
status: decided
```

from illustrative prose.

If document lifecycle metadata is genuinely required, name it explicitly, e.g. `document_lifecycle:`. Do not recreate the old overloaded `status` vocabulary.

## 3. Small stale-spec corrections may be folded into Phase 2

Do not start another documentation-only repair round.

While executing Phase 2, correct these obvious point-in-time statements in the same change if touched:

- target prose that still says the blanket `docs/plans/` ignore is active;
- slice prose that hard-codes the old inbound-reference count/locator;
- any equivalent audit-time wording superseded by the actual `1dc6b86` state.

Preserve historical statements when they are explicitly historical. Correct only current-state claims.

## 4. Build the minimum Phase-2 mechanisms

Phase 2 requires the following mechanisms and **no larger portfolio**.

### 4.1 New Skill: `simplification-audit` (A8)

Implement the minimum useful version.

Required behavior:
- read-only over the target repository during analysis;
- classify production/current consumers vs historical/test/fixture-only consumers;
- distinguish “zero current consumers” from “I did not search enough”;
- output a FEW strong candidates, not a giant lint list;
- every candidate records candidate, evidence, consumer analysis, why removal/simplification is safe or uncertain, proposed action, and uncertainty/human gate if any.

Phase-2 inputs:

```text
PSR + WFI + deterministic reference search
```

Do not require the Phase-3 dependency graph.

Keep manual/orchestrator-only invocation until its eval passes.

### 4.2 New Skill: `focused-verification` (A9)

Implement the minimum useful version.

Split responsibilities:

```text
machine:
  compute changed paths / declared impact surface / available relevant checks

skill:
  choose the narrowest evidence set sufficient for this change
```

Required output:
- change scope;
- selected checks;
- why each check is relevant;
- explicitly excluded checks;
- verification results;
- any ratchet-up discovered during execution.

Do not recreate a universal “run everything” aggregate. Do not re-run already-passing checks without a reason.

Keep manual/orchestrator-only invocation until its eval passes.

## 5. Build only the four Phase-2 lints

Implement:

```text
canonical-impact-lint
archive-lint
supersession-lint
decision-note-lint
```

Do NOT implement in Phase 2:

```text
duplicate-fact-lint
release-version-lint
dependency-graph-lint
state-consistency-lint
provenance-lint
standalone change-scope checker
```

unless a concrete Phase-2 failure proves one is unavoidable. If that happens, stop and report the evidence before broadening scope.

### 5.1 `canonical-impact-lint`

Phase-2 semantics are deliberately narrow:

```text
input:
  declared impact contract / impact set
  actual changed paths

check:
  every declared impacted canonical owner is
  updated in the same change
  OR explicitly discharged as no-impact
```

Do not claim that Phase-2 automatically infers every semantic dependency in the repository.

A missing/empty impact declaration for a non-trivial change must fail.

A timestamp update alone must never clear the check.

Self-tests must include:
1. unrelated change → correct owner does not fail;
2. declared impacted owner omitted → fail;
3. timestamp-only edit on stale owner → still fail.

### 5.2 `archive-lint`

For the declared Phase-2 archive class:
- VOID/SUPERSEDED canonical plan must reside in the allowed archive area when lifecycle requires archival;
- archive destination must be tracked;
- required supersession/banner metadata must survive;
- active status pointers must not keep treating the archived plan as current authority.

### 5.3 `supersession-lint`

At minimum validate:
- referenced `supersedes` / `superseded_by` target exists;
- no trivial self-cycle;
- superseded/falsified durable decision carries required annotation/lineage;
- archive move preserves lineage.

Do not attempt to solve general graph theory in Phase 2.

### 5.4 `decision-note-lint`

Validate the accepted note format:

```text
Problem / Question
Decision
Evidence basis
Alternatives considered
Why
Consequences
Revisit condition
```

For rejected notes also require `rejection_basis`.

Validate the orthogonal state fields where present.

Do not infer that `decision_state: decided` implies `implementation_state: implemented`.

## 6. Create only the canonical stores required by this slice

Create/track:

```text
docs/decision-notes/
  proposed/
  decided/
  rejected/
  archived/

docs/decision-register.md

docs/canonical-source-map.md

docs/plans/active/**
docs/plans/archived/**
```

Do not create unrelated Phase-3 stores.

### 6.1 D-1

Materialize D-1 in `docs/decision-notes/decided/` with the final ruling:

```text
Option A:
docs/plans/active/reconstruction/README.md
is the single canonical owner of
“current execution status / what is next”.
```

Use the orthogonal state model and no generic mixed `status` key.

### 6.2 Decision register seed

Seed only:
- D-1;
- the reconstruction-program route advanced by this slice.

Do not backfill the entire historical decision corpus in Phase 2.

Every entry must cite its source.

### 6.3 Canonical source map

Create `docs/canonical-source-map.md` as the single manually authoritative ownership map.

Convert the existing harness-side canonical-source map into a thin pointer or generated/non-authoritative view.

Do not maintain two hand-written ownership maps.

## 7. Execute the real simplification slice

After the minimum mechanisms above exist and self-test:

```text
PSR
→ simplification-audit
→ select ONE evidence-backed candidate
→ D-1 decided note/register state
→ host implementation
→ focused-verification
→ two-axis review
→ same-change canonical-owner maintenance
```

The expected candidate remains `archive the VOID creation-roadmap`, but re-verify it from the actual slice-start state.

### 7.1 Archive operation

Move the retired roadmap to the tracked archive.

Preserve its historical content and supersession banner.

Do not rewrite it into a new current-state document.

### 7.2 Reference handling

Use the Stage-0 census.

For each old-path reference:
- current pointer → update to the new canonical/current target;
- current reference to the archived plan as history → repoint to archived location and label it historical if needed;
- frozen result / fixture → do not silently rewrite historical evidence merely to make link counts pretty;
- provenance locator → preserve semantics, using archived path or commit-qualified locator as appropriate;
- stale/dead live pointer → fix.

Do not use a hard-coded “one inbound reference” assumption.

### 7.3 Same-change current-owner updates

At minimum re-check:
- current status / what-next owner;
- SWR stale builtness claim (D14 class);
- README L1/flow-count current-state claim (D1 class);
- system-architecture current status pointer if still stale;
- registry narrative/meta residue if still live.

Only edit an item if current evidence still shows it is stale.

## 8. Keep adversarial fixtures isolated from the live repo

The planted stale-roadmap defect is an eval fixture.

Do not leave a synthetic stale roadmap in the canonical repository.

Use a temporary fixture copy, isolated worktree, or dedicated eval fixture path and verify the fixture mutation actually occurred before scoring it.

The real repo simplification and the planted-defect eval are two evidence channels; do not conflate them.

## 9. Verification requirements

Run the narrow Phase-2 evidence set:

```text
existing preflight
markdown link check / required banner-aware extension
canonical-impact-lint
archive-lint
supersession-lint
decision-note-lint
affected existing eval cases
new A8/A9 atomic cases
new checker self-tests
```

### 9.1 Negative controls are mandatory

Every new checker must demonstrate:

```text
pre-fix / planted bad state → FAIL
post-fix state → PASS
```

A checker that only passes the final state is not proven.

For A8/A9, include at least:
- correct trigger;
- non-trigger / overlap case;
- one adversarial case.

### 9.2 Do not require deferred checks

Phase-2 completion must not depend on:

```text
duplicate-fact-lint
dependency-graph-lint
release-version-lint
state-consistency-lint
provenance-lint
```

## 10. Two-axis review

Before declaring completion, perform and record:

### Axis 1 — repository standards
- write boundaries;
- current-state vs historical prose;
- canonical ownership;
- note lifecycle;
- archive semantics;
- no silent decisions;
- no duplicate mutable authority.

### Axis 2 — originating Phase-2 contract
- one simplification;
- minimum mechanisms only;
- no Phase-3 expansion;
- no unrelated cleanup;
- all required evidence produced.

Any unresolved Axis-2 blocker means Phase 2 is not complete.

## 11. Required before/after evidence

Record actual measurements from the real slice-start state, not copied proposal numbers.

At minimum:
- base commit;
- final commit;
- roadmap old/new path;
- actual current-reference census before/after;
- tracked/untracked state of required canonical stores;
- declared impact set;
- actual changed paths;
- new checker negative-control results;
- focused-verification selection + results;
- untouched-scope integrity evidence;
- two-axis review result;
- `persistent_artifact_count` (REPORT ONLY).

For every persistent artifact record:
- unique responsibility;
- canonical owner;
- consumer;
- lifecycle;
- archive/delete condition.

Do not use artifact count as a correctness quota.

## 12. Stop / BLOCK conditions

Stop and report `BLOCKED` instead of improvising if:
- the current repository state invalidates the chosen simplification candidate;
- required untracked planning files are missing or unexpectedly different;
- an archive operation would destroy historical evidence;
- a new checker cannot demonstrate a negative control;
- A8/A9 cannot run without pulling in a deferred Phase-3 mechanism;
- the declared impact set cannot be made explicit;
- the implementation would require a new durable authority duplicating an existing one;
- an unresolved human decision appears that is not already covered by D-1.

Do not silently broaden scope.

## 13. Explicit Phase-2 non-goals

Do NOT implement:

```text
repo-bootstrap
next-discriminating-experiment
route-manager skill
dependency-graph-lint
duplicate-fact-lint
release-version-lint
state-consistency-lint
provenance-lint
A2 / A3 / A4 / A6 parked capabilities
full multi-agent scheduler
stacked-PR machinery
new DQE terminal gate
```

Do not redesign the architecture unless the vertical slice produces concrete contradictory evidence.

## 14. Suggested commit structure

Prefer a dedicated branch/worktree.

A useful structure is:

```text
Commit A:
  minimum Phase-2 mechanisms
  A8 + A9
  four lints
  their self-tests / atomic evals

Commit B:
  canonical stores
  D-1 decided note/register seed
  tracking transition
  real roadmap archive + live pointer/current-owner fixes
  focused verification + two-axis evidence
```

Both commits may be in one PR/change set.

The same-change canonical-owner rule applies to the actual behavior/state change and its affected owners; do not use commit separation to leave the integrated branch with a false current-state claim.

## 15. Phase-2 completion gate

Do not claim COMPLETE unless all are true:

```text
[ ] actual slice-start state recaptured
[ ] all creation-roadmap references classified
[ ] A8 implemented without Phase-3 dependency-graph-lint
[ ] A9 implemented without Phase-3 dependency-graph-lint
[ ] canonical-impact-lint implemented + negative controls pass
[ ] archive-lint implemented + negative controls pass
[ ] supersession-lint implemented + negative controls pass
[ ] decision-note-lint implemented + negative controls pass
[ ] D-1 exists in decided/ and records option A
[ ] no generic mixed status field introduced in the new decision schema
[ ] decision register seeded only as scoped
[ ] canonical-source-map has one manual authority
[ ] harness map is pointer/generated, not second authority
[ ] docs/plans/active and docs/plans/archived required files are tracked
[ ] local/scratch planning state remains excluded
[ ] retired roadmap archived without historical-data loss
[ ] current live pointers/current-state claims corrected from actual evidence
[ ] planted stale-roadmap defect detected and named in an isolated fixture
[ ] focused-verification record complete
[ ] two-axis review has no unresolved spec blocker
[ ] untouched-scope integrity check passes
[ ] no deferred Phase-3 checker is required for completion
[ ] persistent artifact count is report-only and every artifact has a lifecycle/consumer
[ ] final Git state contains no required canonical artifact left untracked
```

When all pass, update the canonical current-status owner to record:

```text
Phase 2: COMPLETE
```

and report concrete evidence, not merely the agent's self-assessment.

If any item fails, report:

```text
Phase 2: BLOCKED
blocked_by:
evidence:
next smallest action:
```
