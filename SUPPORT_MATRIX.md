# SUPPORT MATRIX — Research-Code-Docs v0.1.0-alpha.1

> What the preview **formally supports**, what is **experimental**, and what is **unsupported**.
> "Supported" here means: intended for Alpha use, manual + non-destructive, and exercised at least once
> on a real corpus. It does **not** mean production-grade or auto-runnable.

| Capability | Status | Meaning / boundary |
|---|---|---|
| Document-corpus inventory | **Supported** | read-only enumeration + candidate canonical sources; never mutates |
| Project-state recovery | **Supported (advisory)** | recovers FACT-vs-UNKNOWN state; **not** a runtime-execution proof |
| Information architecture | **Supported** | designs the target split/canonical homes; **designs only, executes nothing** |
| Dry-run migration | **Supported** | per-source disposition map + rollback; **never moves or deletes** |
| Candidate rewriting | **Supported** | writes **new** candidate files only; originals byte-for-byte unchanged (sha256-verified) |
| DQE quality review | **Supported (profiles only)** | advisory grade within supported profiles; **not** a universal terminal gate |
| Maintenance impact | **Supported (proposal-only)** | proposes canonical updates; **does not modify canonical docs** |
| `documentation-refactor` closed loop | **Supported (dry-run + candidate scope)** | COMPLETE means the plan+candidates are produced, not that migration ran |
| The 11 atomic skills as manual advisory tools | **Supported** | each `disable-model-invocation:true`, human-review-required |
| Workspace reconstruction flow | **Experimental (prefix)** | routes real atoms then **BLOCKED** at `dev-test-experiment-workspace-architect` (Batch 5) |
| Numerical design flow | **Experimental (prefix)** | routes real atoms then **BLOCKED** at the numerical-design core (Batch 4) |
| Auto-trigger | **Unsupported** | disabled by construction; every skill is manual-only |
| Destructive apply (move/delete/overwrite) | **Unsupported in Alpha** | requires a separate future design + explicit write-approval |
| Auto-publish / candidate→canonical | **Unsupported** | proposals only; a human promotes |
| Experiment reproducibility-release gate | **Unsupported** | DQE returns `GATE_DECISION=INCOMPLETE / unsupported-evaluation-profile` |
| Full numerical / workspace closed loops | **Unsupported** | their core atoms (Batch 4 / Batch 5 remainder) are not built |

## Safety invariants (hold across every supported capability)

```text
manual invocation only          no auto-trigger
isolated workspace              no writes outside the workspace
candidate-output only           originals never moved / deleted / overwritten
human review required           DQE ALLOW authorizes nothing
explicit approval to apply      unauthorized write request -> flow_status=BLOCKED
```

See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for the detailed caveats behind each "Supported" row,
and [release-manifest.yaml](release-manifest.yaml) for the machine-readable version.
