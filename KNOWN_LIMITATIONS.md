# KNOWN LIMITATIONS — Research-Code-Docs v0.1.0-alpha.1

> Honest boundaries of the internal preview. None of these block Alpha use; all are things you must
> know so you neither over-trust the output nor mistake a designed stop for a bug.

1. **`documentation-refactor` COMPLETE = dry-run + candidate-output only.**
   `flow_status: COMPLETE` means the migration *plan* and *candidate* documents were produced — **not**
   that any file was migrated. Applying the plan (moving/rewriting real files) is a separate, un-granted
   explicit write-approval that this Alpha does not implement.

2. **Candidate relative links may need re-verification after placement.**
   Candidate documents are written to an isolated staging directory; links that point at a document's
   *eventual* canonical home can appear "broken" in staging and must be re-checked when the candidate is
   actually placed. The checkers flag this; it is expected for candidate-output mode.

3. **DQE is advisory, not an auto-publish approver.**
   A DQE `ALLOW` / high quality band authorizes nothing — no move, publish, or promotion. It is one
   advisory input for a human reviewer, and only within its supported profiles.

4. **The controlled-experiment reproducibility-release profile is unsupported.**
   For that profile DQE deliberately returns `GATE_DECISION=INCOMPLETE / unsupported-evaluation-profile`
   rather than a possibly-wrong ALLOW. Do not use DQE as a blanket automatic terminal gate.

5. **Some Batch-1 skills still lack full task-quality and multi-turn tests.**
   `project-state-reconstructor`, `goal-scope-and-workflow-elicitor`, and
   `uncertainty-and-decision-manager` passed trigger/conflict evals but their soft-scoring / multi-turn
   coverage is pending. Treat their output as advisory and review it.

6. **The three new Batch-5 executors used light tests only.**
   `content-canonicalization-and-migration`, `technical-document-rewriter`, and
   `living-design-maintainer` passed a *light* round (routing + one real closed-loop shadow + reader +
   checker self-tests). Light testing is **not** production promotion; they stay experimental + manual.

7. **The workspace and numerical flows do not close a full loop.**
   `scientific-workspace-reconstruction` stops (honestly, `BLOCKED`) at
   `dev-test-experiment-workspace-architect` (Batch 5, unbuilt); `numerical-research-software-design`
   stops at the numerical-design core atoms (Batch 4, unbuilt). A named `blocked_by` is the correct
   output, not an error.

8. **All auto-triggering is off.** Every skill ships `disable-model-invocation: true`. Nothing runs
   unless you invoke it. This is intentional and not configurable in Alpha.

9. **Generalization evidence is limited.** Validation so far is mainly against **one** real
   single-project corpus (`docs/skill-development/`) plus synthetic fixtures. Cross-project / cross-domain
   generalization is not yet demonstrated.

10. **Large-corpus performance and context budget are unmeasured.**
    Runs so far are on small corpora (tens of docs). Behavior, latency, and context cost on hundreds+ of
    documents have not been systematically measured; expect to chunk large corpora manually.

---

**How to report something that looks wrong.** Use the run-feedback record in the release plan (§9.1):
capture `run_id`, `flow_status`, `blocked_by`, `source_files_changed`, whether a no-context reader could
act on the output, and any skill/interface/harness defect. A new regression is added **only** when a real
run exposes a reproducible error (release plan §9.2) — not preemptively.
