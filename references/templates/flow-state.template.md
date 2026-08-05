<!--
generated_by_skill: <control-flow name, e.g. documentation-refactor>
skill_version: 0.1.0
source_commit: <repo@commit at run time>
source_documents: [<the target the flow was invoked on>, <upstream artifacts consumed>]
document_lifecycle: IN_REVIEW
last_verified: <YYYY-MM-DD>
-->

# Flow-State — <flow-name> run on <target>

A control-flow **status record** (contract: `references/interfaces/flow-state.schema.md`). The flow routes to
existing skills, persists their artifacts, records state, and **stops honestly at any missing capability** — it
does not copy an atomic skill's writing rules or fake a closed loop.

```yaml
flow_name: <documentation-refactor | scientific-workspace-reconstruction | numerical-research-software-design>
flow_version: 0.1.0
flow_status: <RUNNING | BLOCKED | COMPLETE>
current_stage: <the real last stage reached — skill name / step>
completed_artifacts:
  - <path to each artifact that actually exists on disk>
open_decisions:
  - <decisions aggregated upward from the atomic skills; [] if none>
blocked_by: <REQUIRED IF BLOCKED: the missing capability / not-yet-built skill; "none" only when not blocked>
next_skill: <the next skill to run | "human decision" | "none (terminal)">
next_input: <what next_skill consumes: artifact path(s) / decision id>
quality_advisory: <DQE-advisory pointer/verdict, or "not run" — advisory only, authorizes NOTHING>
source_commit: <repo@commit>
```

## What ran (route trace)
- <stage → skill → artifact produced> (one line each; only stages that actually ran)

## Why it stopped here
- <for a BLOCKED run: the named missing capability + which batch will provide it; this is a truthful
  capability boundary, not a failure>

## Next handoff
- <the concrete next action + who/what performs it (a human decision, or a named skill once it exists)>
