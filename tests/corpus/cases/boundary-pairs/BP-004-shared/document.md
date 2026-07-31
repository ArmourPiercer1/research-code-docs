# ADR 7 — Use content-addressed cache keys for the build graph

## Context

The build graph re-runs tasks whenever any input changes. Today the cache key is the task's mtime,
which is fragile across machines and CI checkouts (mtimes are not preserved). We want a key that is
identical for identical inputs regardless of where or when the checkout happened.

## Decision

Use a content-addressed key: `sha256(sorted(input_file_hashes) ++ normalized_command ++ tool_version)`.
The key is computed by the scheduler before dispatch and stored in the cache index.

## Consequences

- **Good:** deterministic cache hits across machines; CI and local share a cache safely.
- **Good:** a changed compiler version invalidates exactly the tasks that used it.
- **Cost:** hashing large inputs adds ~40ms/task; mitigated by memoizing file hashes within a run.
- **Risk:** hash collisions are assumed negligible at sha256; not defended against adversarially.

## Alternatives considered

- **mtime (status quo):** rejected — not portable across checkouts.
- **explicit user-declared keys:** rejected — error-prone; drifts from real inputs.
