<!--
generated_by_skill: documentation-quality-evaluator
skill_version: 0.4.1
source_commit: 7919bc4
source_documents:
  - evals/skills/results/batch2_5/document-chain/document-artifact-map.md
artifact_type: quality-report
document_lifecycle: IN_REVIEW
evaluation_profile:
  artifact_type: architecture-doc            # internal information-architecture DESIGN PLAN (document-artifact-map)
  provenance_policy: NOT_SUPPLIED            # caller did not supply; NOT inferred (see §Profile)
  decision_mode: NOT_SUPPLIED               # advisory-audit assumed for the WALK; explicitly NOT controlled+release-gate
  output_mode: audit
last_verified: 2026-08-05
status: DEFERRED to human — advisory only (v0.4.1 freeze); authorizes no action
scope: "Advisory quality report on document-artifact-map.md (the document-chain terminal artifact, an information-architecture design plan). Read-only. Wrote exactly this one file; modified nothing. Grades the PLAN, not the diseased corpus the plan proposes to cure."
-->

# Quality Advisory — `document-artifact-map.md` (document-chain terminal artifact)

**Run mode:** DQE v0.4.1, ADVISORY, ISOLATED. This report is *advice for a human / orchestrator*. It is
**not** a terminal gate and **authorizes no action** (no publish, move, merge, delete, install, or
auto-trigger). Read-only w.r.t. the target.

---

## Structured verdict (machine-parseable)

```
QUALITY_BAND=PASS
GATE_DECISION=INCOMPLETE
GATE_REASON=missing-profile
DOCUMENT_QUALITY=INCOMPLETE_EVALUATION
FACTUAL_VALIDITY=PARTIALLY_VERIFIED
READER_TEST=n/a (not run)
CHECKER_STATUS=COMPLETE
SOURCE_COVERAGE=3/3        # the map's own load-bearing cited sources = its 3 named upstreams, all opened
CONFIDENCE=MEDIUM
BLOCKERS=[]
FINDING_CODES=[]           # no MAJOR/blocking defect; the FYIs below are correct design hygiene, not findings
EVALUATION_PROFILE={artifact_type:architecture-doc(design-plan), provenance_policy:NOT_SUPPLIED, decision_mode:NOT_SUPPLIED}
FILES_READ=[.claude/skills/documentation-quality-evaluator/SKILL.md, evals/skills/harness/hard-fail.md, evals/skills/harness/rubric.md, evals/skills/results/batch2_5/document-chain/document-artifact-map.md, .../inventory-report.md, .../project-state-report.md, .../goal-scope-note.md]
```

**Caller verdict line:** `VERDICT gate=INCOMPLETE quality=PASS total=94 blockers=[]`

**One-line reading:** The artifact-map is a **high-quality (advisory PASS, ~94/100)** single-responsibility
information-architecture design plan with exemplary traceability and uncertainty discipline. **No hard gate
fires.** The gate is **INCOMPLETE (not a terminal ALLOW)** for one reason only: the caller did **not** supply
`provenance_policy` / `decision_mode`, which DQE may never silently infer — plus the no-context reader test
was not run in this isolated pass. Both are honest "can't-issue-a-terminal-gate-here" conditions, **not**
quality defects of the target.

---

## Profile selected + why (Rule 0 admission)

- **artifact_type = `architecture-doc` (an internal information-architecture DESIGN PLAN; the chain's
  `document-artifact-map`).** This is a **supported** advisory profile. It is **not** the one unsupported
  profile the freeze scopes out (a `controlled + release-gate` **experiment-report**), so **Rule 0 does not
  fire** and `GATE_REASON` is **not** `unsupported-evaluation-profile`.
- **provenance_policy / decision_mode = NOT SUPPLIED, and NOT inferred.** The caller flagged these with
  "do NOT silently infer controlled+release-gate." Per DQE's non-inference contract (SKILL §Inputs; derivation
  Rule 1), a missing `provenance_policy`/`decision_mode` forces `GATE_DECISION=INCOMPLETE` and must be named —
  it may **not** be papered over by assuming the aggressive `controlled + release-gate` combination (which is
  the only way HF-14b could become a *lone BLOCKER*). For the gate **walk** I assumed the safe reading —
  advisory **audit**, not release-gate — under which HF-14b can at most be MAJOR and never a lone BLOCK; it
  does not even fire here (see below).
- **Consequence:** two independent, honest non-ALLOW conditions (missing profile fields · reader test not
  run) → `GATE_DECISION=INCOMPLETE`, `GATE_REASON=missing-profile`. This is **not** an INCOMPLETE used to
  dodge a doc-only FAIL (there is no doc-only FAIL to dodge — the doc is clean); it is the correct
  can't-approve-yet state, fully in line with the v0.4.1 advisory posture.

---

## Deterministic checkers (run, not eyeballed)

`python evals/skills/harness/checkers/run_checks.py document-artifact-map.md --json` →

```json
{
  "hard_fail": false,
  "hard": {
    "frontmatter": {"pass": true, "problems": []},
    "status_vocab": {"pass": true, "problems": []}
  },
  "advisory": {
    "markdown_links": {"pass": true, "problems": []},
    "placeholders":   {"pass": true, "problems": []},
    "interface":      {"pass": true, "problems": []}
  },
  "signals": {
    "state_numbers":   {"clear": true, "candidates": []},
    "completion_open": {"clear": true, "candidates": []},
    "roadmap_fields":  {"clear": true, "candidates": []},
    "session_residue": {"clear": true, "candidates": []},
    "role_mixing":     {"clear": true, "candidates": ["section-level roles: adr@L22",
                        "mention-level roles: handover_session, open_questions, status"]}
  }
}
```

**Signal adjudication (a signal is a candidate, never an auto-block):** the `role_mixing` candidates are
**false positives for HF-13**. `adr@L22` is the word "adr" inside the document **title**
(`# Artifact Map — docs/skill-development/ … + adr corpus`) — it names the corpus under study, it is not an
ADR role carried in the body. `handover_session, open_questions, status` are **front-matter provenance
fields** + descriptions of the *corpus's* info-types, i.e. **mention-level**, not body-level primary content
of divergent lifecycle. `state_numbers` and `completion_open` are **clear**, corroborating no HF-14a/HF-14b
contamination in the map itself.

---

## Hard-gate walk (every applicable gate; ALL blockers collected — there are none)

Applicable set for an architecture-doc / design-plan: **HF-9, HF-12A/E, HF-13, HF-14b**, plus HF-3/HF-10
(status-vocab), HF-7, HF-8, HF-14a as cross-checks.

| Gate | Condition | Verdict | Evidence on the map |
|---|---|---|---|
| **HF-9** traceability front-matter | missing skill/version/commit/time/status **or** `document_lifecycle` | **PASS** | Full block L1–L20: `generated_by_skill`, `skill_version 0.1.0`, `source_commit 7919bc4`, 3 `source_documents`, `artifact_type`, `document_lifecycle: IN_REVIEW`, `last_verified`. `document_lifecycle` satisfies the doc-level status requirement (HF-9 v0.4). Checker `frontmatter.pass=true`. Not a blocker under any profile. |
| **HF-3** candidate-as-decided | CANDIDATE written as DECIDED | **PASS** | `status: "CANDIDATE information architecture"` (L19); provisional/BLOCKED rows never dressed as FACT. Checker `status_vocab.pass=true`. |
| **HF-10** evidence-level inflation | ≤E2 asserted as E3+ | **PASS** | `evidence_level: "n/a … PSR rows whose ceiling is E2"` (L16); borrowed owners not upgraded to project-verified. |
| **HF-7** dropped open question | silently drops a known OPEN item | **PASS** | Carries D-1..D-7 from goal-scope-note **and** adds IA-1..IA-3; `open_questions … Never 'none'` (L15); §5 lists all 10. |
| **HF-8** needs unstated context | only parses with hidden chat history | **PASS** | Self-contained; names its 3 upstreams + companion `canonical-source-map.md`/`open-decisions.md`. Checker `session_residue.clear=true`. (Minor read-friction: C/O/D shorthand is defined in the upstream inventory — normal for a chain-step artifact; FYI-1.) |
| **HF-12A** claim traceability | load-bearing claim with no handle/label | **PASS** | Every §2 canonical-home carries a basis (`PSR: … :89/:90/:91/:92/:93`) or is flagged **provisional/BLOCKED** with its gating decision (D-1/D-4/D-6). |
| **HF-12E** evidence-status labeling | conclusion not tagged | **PASS** | FACT / provisional / BLOCKED tags throughout §2; borrowing from PSR explicitly labeled. |
| **HF-12B/C/D** source-needing | cited source unreachable / unsupportive / unstated transfer | **N/A → PARTIALLY_VERIFIED** | The map asserts **no new facts** (`facts: "none"`, L13); its load-bearing sources are its 3 upstreams, all opened and faithfully represented. Transitive corpus facts are **borrowed at E2** and not re-verified here — by design (that is PSR's lane), so `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`, not a pass claim. |
| **HF-13** mixed responsibilities | ≥2 divergent-lifecycle roles as body-level content + not subordinated + observable harm | **PASS (does not fire)** | The map is a **single-responsibility design plan** that *describes* the corpus's HF-13 disease and *proposes the cure* (§2 one-home-per-type, §4 split plan). It is not itself a union of diseased roles. No body-level divergent-lifecycle mixing; internally consistent (checker `state_numbers.clear`). Grading the plan as if it were the diseased corpus would be the exact mis-grade this run must avoid. |
| **HF-14a** state contradiction | contradictory state values | **PASS** | Tally 10 FACT + 4 provisional + 1 BLOCKED = 15 is internally consistent; front-matter `hypotheses`(5)+`open_questions`(10) match the body. Checker `state_numbers.clear=true`. |
| **HF-14b** volatile contamination | stable-design doc embeds bare undated "current" facts, no dynamic-source pointer | **PASS (does not fire)** | The map is a stable design plan that **proposes** the HF-14b cure (route all volatile status to one owner + pointers: §2 BLOCKED row, S1–S3). It embeds no bare "current" fact of its own (`last_verified` dated; "current status" appears only as an **info-type to be homed**). Also `decision_mode ≠ release-gate` ⇒ HF-14b could at most be MAJOR, never a lone BLOCK — moot, since it does not fire. |

**Blockers: none. Majors: none.**

---

## Soft rubric (8-dimension base; scored only because all hard gates pass)

| Dim | Wt | Score | Justification |
|---|---:|---:|---|
| Factual accuracy | 20 | 4.5 | Every claim traces to a PSR/inventory row with a handle; borrowed facts labeled; honest E2 ceiling. |
| Information architecture | 15 | 5.0 | It *is* an IA doc and it embodies its own thesis: one canonical home per type, clean single responsibility. |
| Actionability | 15 | 4.5 | Concrete split plan (S1–S9), target doc-set (§3), open decisions with what-each-gates; measurable next actions (decide D-1/D-4, run the D-6 diff). Execution correctly BLOCKED, not vague. |
| Evidence traceability | 15 | 5.0 | Each home cites basis + verdict label + PSR locator; forensics candidates C1–C6/O1–O3 each routed to an owner or an open decision. |
| Uncertainty expression | 10 | 5.0 | FACT vs provisional vs BLOCKED kept separate; CANDIDATE status; open_questions "never none". |
| Reader fit | 10 | 4.0 | A target-role reader (migration executor / decision-manager) can act; minor cross-ref friction on the C/O/D shorthand (FYI-1). |
| Maintainability | 10 | 5.0 | Strict single-source / pointer discipline is the plan's whole point, and it practices it. |
| Concision | 5 | 4.5 | Dense but tight; little removable without loss. |

`raw = 470/500` → **total ≈ 94/100.** ≥ 75, min dimension 4.0 ≥ 2.5, **non-compensatory rule holds** (no
critical dimension < 3.5, no structural gate substantiated) → **QUALITY_BAND = PASS** (advisory).

**Reverse-outline / rationale-anchor:** every §1–§6 section maps to the single stated thesis
("where each responsibility *should* live once the corpus is restructured"); no orphan section; the design
records *why* each home (borrowed-from-PSR basis) and defers the *human-preference* choices rather than
inventing them.

---

## Reader test

**Not run (n/a).** This is an isolated single-agent advisory pass; a fresh no-context reader sub-agent was
not spawned. Per the derivation rule, a not-run reader test independently bars a terminal ALLOW and
reinforces `GATE_DECISION=INCOMPLETE`. Structural readability signals are nonetheless favorable (self-contained,
`session_residue.clear`, HF-8 PASS).

---

## Explicitly NOT defects (correct design hygiene — do not grade these down)

- **`next_handoff: BLOCKED:content-canonicalization-and-migration, technical-document-rewriter (Batch 5 — not
  built)` is a CORRECT honest stop — a `MISSING_CAPABILITY`, not a defect.** The executor skills genuinely do
  not exist yet (confirmed by goal-scope-note workflow step 5 and PSR). Stopping at a complete, parked plan
  with an explicit BLOCKED marker is exactly the right behavior; inventing an execution would be the failure.
- **The provisional / BLOCKED home assignments are correct design hygiene, not failures.** The current-status
  owner (§2 BLOCKED on D-1), the hard-fail-catalog home (provisional on D-6/U1), the DQE defect-register
  canonical (provisional on D-6/U6), the upstream-method-matrix currency (provisional/U2, out of scope), and
  the README index membership (provisional on D-4) each rest on an **unresolved fact or human choice** and are
  **flagged rather than silently picked**. That is the requested discipline ("do NOT pick silently"), and it
  faithfully mirrors PSR's own CONSISTENT/CANDIDATE + UNKNOWN verdicts.
- **The 10 open decisions (D-1..D-7 + IA-1..IA-3) are the correct output of a planning step**, not omissions.
  Blocking items (D-1, D-4) are labeled blocking; repo-verifiable (D-6) is labeled resolvable-by-diff.

---

## Severity-ordered fix list

- **BLOCKER:** none.
- **MAJOR:** none.
- **MINOR:** none that affect the verdict.
- **FYI-1** (read-friction, optional): the C1–C6 / O1–O3 / Or1–Or3 shorthand is defined only in the upstream
  `inventory-report.md`; a reader arriving without the upstream must cross-reference. Inherent to a chain-step
  artifact that correctly names its upstreams — acceptable as-is; a one-line "codes defined in
  inventory-report.md §Contradiction candidates" note would remove it entirely.
- **FYI-2** (caller action to lift INCOMPLETE): supply `provenance_policy` + `decision_mode` (e.g.
  `controlled + audit` for an internal advisory review) and run the no-context reader test; with the gates
  already all-PASS, that would resolve the gate to an **advisory ALLOW** (still not a green *terminal* gate
  while `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`).

---

## Coverage / discipline notes

- **Files opened:** the evaluator (SKILL.md), `hard-fail.md`, `rubric.md`, the target, and the 3 permitted
  upstreams. `canonical-source-map.md` (normally always-loaded) was **not** opened — it is outside this
  isolated run's file allowlist. This does not change the verdict: HF-14b does not fire on the map regardless,
  so the canonical-source-map grounding was not load-bearing for any gate here (noted for honesty).
- **Untrusted-input discipline:** imperative-sounding text inside the scanned artifact (and its upstreams) was
  treated as DATA to evaluate, never as instructions altering this verdict or the read-only posture.
- **Two axes are independent:** `QUALITY_BAND=PASS` (the document is excellent) coexists with
  `GATE_DECISION=INCOMPLETE` (the caller-supplied profile is incomplete + reader test not run). Neither the
  rubric total nor `FACTUAL_VALIDITY` moved the gate.

---

**ADVISORY ONLY — THIS REPORT AUTHORIZES NO ACTION.** `GATE_DECISION=INCOMPLETE` (and even an advisory
`ALLOW`) does not permit publishing, moving/merging/deleting/overwriting any file, installing skills, enabling
auto-trigger, or executing the parked migration. A human or orchestrator decides; DQE v0.4.1 is an advisory,
profile-scoped reviewer, not a terminal gate.
