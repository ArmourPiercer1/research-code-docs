---
generated_by_skill: documentation-quality-evaluator
skill_version: 0.4.1
source_commit: 7919bc4
source_documents: [evals/skills/results/batch2_5/research-chain/decision-register.md]
artifact_type: quality-report
document_lifecycle: IN_REVIEW
last_verified: 2026-08-05
evaluation_profile: "{artifact_type: decision-register, provenance_policy: controlled, decision_mode: audit, evidence_requirement: labeled-only, reader_profile: decision-gate-comprehension, output_mode: audit}"
scope: "ADVISORY quality report on the research-chain terminal artifact decision-register.md (v0.4.1 advisory freeze, isolated run). Grades the register; the two named upstreams were read for provenance context only. Records advice, not authorization — a human/gate decides."
---

# Quality Advisory — Decision Register (manifold-optimization backbone for a general equality-constrained solver core)

> **This is an ADVISORY report** produced by `documentation-quality-evaluator` v0.4.1 in its frozen
> advisory / profile-scoped posture. It grades one artifact and returns advice. It is **read-only** with
> respect to the target and authorizes **no** action (see the closing line).

## Structured verdict (machine-parseable)

```
QUALITY_BAND=PASS
GATE_DECISION=ALLOW            # ADVISORY — not a green terminal gate; a human/gate decides
GATE_REASON=none
DOCUMENT_QUALITY=PASS
FACTUAL_VALIDITY=PARTIALLY_VERIFIED
READER_TEST=PASS
CHECKER_STATUS=COMPLETE
SOURCE_COVERAGE=2/4           # 2 internal upstreams opened & verified; 2 named external DOIs not opened
CONFIDENCE=HIGH               # on the doc-only structural verdict; factual caveat below caps only the literature-support claim
BLOCKERS=[]
FINDING_CODES=[gap-task-dod-qualitative(MINOR), contingency-not-fully-enumerated(MINOR), intro-frontmatter-redundancy(NIT), factual-validity-partial(FYI)]
EVALUATION_PROFILE={artifact_type:decision-register, provenance_policy:controlled, decision_mode:audit}
FILES_READ=[SKILL.md, hard-fail.md, rubric.md, decision-register.md, research-evidence-map.md, literature-search-plan.md]
```

`VERDICT gate=ALLOW quality=PASS total=90 blockers=[]` (advisory)

## Evaluation profile selected — and why (stated, not silently inferred)

Per the caller's framing ("the register is an internal evidence/decision artifact — pick the profile
accordingly; do not silently infer a controlled/release-gate profile") I selected and **state**:

| field | value | why |
|---|---|---|
| `artifact_type` | `decision-register` | Declared in the target's front-matter and confirmed by structure (per-item status/evidence/locator/disposition register). |
| `provenance_policy` | `controlled` | An internal, system-generated artifact (`generated_by_skill: uncertainty-and-decision-manager`) carrying our traceability front-matter + `document_lifecycle: IN_REVIEW` — not `external`/`legacy`. Stated honestly; **not** inferred as anything stricter. |
| `decision_mode` | `audit` | This is an **advisory review** of an `IN_REVIEW` artifact. I deliberately did **not** infer `release-gate` (the caller warned against it, and the v0.4.1 posture is advisory). |

**Profile-admission check (Rule 0, run BEFORE the gate rules).** The unsupported set is
`{artifact_type: experiment-report, provenance_policy: controlled, decision_mode: release-gate}`. My triple
is `{decision-register, controlled, audit}` → **not** in the unsupported set → Rule 0 does **not** fire, so a
terminal *advisory* verdict is in scope (no `unsupported-evaluation-profile`). Both `provenance_policy` and
`decision_mode` are present, so Rule 1's missing-profile INCOMPLETE also does not fire.

Note: the profile choice does **not** move any gate here — the register carries complete front-matter, so HF-9
passes under `controlled`, `legacy`, or `external` alike; and HF-14b is type-gated off a decision register (see
table).

## Deterministic checkers (run, not eyeballed) — `run_checks.py --json`

```json
{
  "path": "evals\\skills\\results\\batch2_5\\research-chain\\decision-register.md",
  "files_checked": 1,
  "hard_fail": false,
  "results": [{
    "hard": {
      "frontmatter": { "pass": true, "problems": [] },
      "status_vocab": { "pass": true, "problems": [] }
    },
    "advisory": {
      "markdown_links": { "pass": true, "problems": [] },
      "placeholders":   { "pass": true, "problems": [] },
      "interface":      { "pass": true, "problems": [] }
    },
    "signals": {
      "state_numbers":   { "clear": true, "candidates": [] },
      "completion_open": { "clear": true, "candidates": [] },
      "roadmap_fields":  { "clear": true, "candidates": [] },
      "session_residue": { "clear": true, "candidates": [] },
      "role_mixing":     { "clear": true, "candidates": ["mention-level roles: handover_session, research_review, status"] }
    }
  }]
}
```

`CHECKER_STATUS=COMPLETE`. The lone `role_mixing` candidate is **mention-level** — it fires on the front-matter
`next_handoff` / `handoff_requirements` words and the term "status", **not** on a second body-level role. It is a
SIGNAL, adjudicated below as **not** HF-13 (`clear: true` confirms the checker agrees). The checker wrote nothing
(JSON to stdout only).

## Hard-gate walk — every applicable gate; all blockers collected

Applicable minimum set for a decision register (hard-fail.md §Per-artifact applicability):
**HF-3, HF-7, HF-9, HF-10, HF-12A/E**. Remaining gates walked and dispositioned so the fix list is complete.

| Gate | Applies | Result | Cited basis |
|---|---|---|---|
| **HF-3** candidate/hypothesis-as-DECIDED/FACT | yes | **PASS** | H-1=`HYPOTHESIS`, O-A1/O-A2/O-G1/O-G2/O-G3=`OPEN`, O-G4=`DEFERRED`; **no** `DECIDED`/`FACT`/`VERIFIED`/`BASELINE`/`CANDIDATE` entry (register block L40–L116; front-matter `facts: "none"`). `status_vocab` PASS. No candidate↔fact bleed. |
| **HF-7** silently dropped OPEN question | yes | **PASS** | All upstream open items carried through: RES `CL-5→H-1`, `CL-6→O-A1`, `CL-7→O-A2`, `G1–G4→O-G1..O-G4` (change log L131–L139; front-matter `open_questions` "Never 'none'"). Nothing dropped vs research-evidence-map.md. |
| **HF-9** missing traceability front-matter | yes | **PASS** | Complete front-matter (skill/version/`source_commit: 7919bc4`/sources/`document_lifecycle: IN_REVIEW`/`last_verified`), L1–L16. `frontmatter` checker PASS. Present ⇒ not fired under any `provenance_policy`. |
| **HF-10** ≤E2 evidence treated as E3+ project-verified | yes | **PASS** | Every entry capped ≤E2; register states only E3+ (direct in-project) may be "verified" and none exists (L23–L24, L44–L46). H-1=E2 (channel cap), O-A1/O-A2/O-G1/O-G2/O-G4=E0, O-G3=E1. No analogy laundered to a fact. |
| **HF-12A** claim traceability (doc-only) | yes | **PASS** | Every entry carries a re-openable `source:` locator (`research-evidence-map.md#CL-5`, `DOI:10.1137/110845768#retraction`, `literature-search-plan.md#cross-domain-transfer-warning`, …) and a status/disposition label. |
| **HF-12E** evidence-status labeling (doc-only) | yes | **PASS** | Each conclusion tagged with channel + level (H-1 "cross-domain-analogy, channel cap"; O-A1/O-A2 "project-inference / assumed, unevidenced"; O-G3 "single partial signal"). Channels kept separate. |
| HF-12B/C/D actual support (source access) | partial | **UNVERIFIED (not failed)** | Internal provenance chain (register↔evidence-map↔search-plan) opened & faithful; the two inline external DOIs were not opened here → contributes to `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`, not a gate failure. |
| HF-1 fabricated code state | no | N/A | Register makes no code-behavior claim. |
| HF-2 fabricated literature | no (not in set) | PASS (no red flag) | Cited DOIs are well-formed and consistent with the RES inventory; not independently resolved (see factual caveat). |
| HF-8 needs unstated chat context | walked | **PASS** | Self-contained; no-context reader answered Layer-1 Q1–Q4 (below). `session_residue` clear. |
| **HF-13** mixed artifact responsibilities | walked | **PASS (not fired)** | Single-role artifact. The role_mixing candidate is mention-level (handoff/status words), not ≥2 body-level roles of divergent lifecycle. No duplication/drift. |
| **HF-14a** state contradiction | walked | **PASS** | `state_numbers` clear; front-matter counts (1 HYPOTHESIS, 6 OPEN/DEFERRED) match the body exactly. No contradictory values. |
| **HF-14b** volatile-in-stable | **N/A (type-gated)** | N/A | Type-gated to stable-design docs (roadmap/architecture/vision/ADR/algorithm-spec). A decision/uncertainty register **owns** its live status/evidence facts (like a state report) → HF-14b does not apply. Even if argued, `decision_mode=audit` ⇒ MAJOR at most, never a lone BLOCK; and every entry is dated (`last_verified: 2026-08-05`) with a source pointer. `completion_open` clear. |
| HF-15 non-executable committed milestone | no | N/A | Not a roadmap; no committed phases. `roadmap_fields` clear. |

**Blockers: none.** GATE_DECISION derivation → Rule 0 not fired · Rule 1 not fired (profile complete, checkers
COMPLETE, reader test ran, type classified, no required section missing) · Rule 2 not fired (no BLOCKER) →
**Rule 3 ⇒ ALLOW (advisory).**

## Soft rubric (scored only because all applicable hard gates pass)

| Dimension | Wt | Score | Justification |
|---|---:|---:|---|
| Factual accuracy | 20 | 4.5 | Every entry traces to a re-openable locator; E-levels/dispositions match research-evidence-map.md faithfully (H-1↔CL-5, O-A1↔CL-6, O-A2↔CL-7, O-G1..4↔G1..4). Terminal external DOIs not re-opened here (−0.5). |
| Information architecture | 15 | 4.5 | Clean single-role register; explicitly routes code facts → state report, stable terms → domain-modeling, evidence → RES map (L21–L24). No role bleed. |
| Actionability | 15 | 4.0 | Each item has a disposition + concrete route (BACK to RQLP / in-project experiment); H-1 promotion gate explicit (L125–L127). Per-gap acceptance metrics are qualitative (−1.0; appropriate for the type — metrics belong downstream). |
| Evidence traceability | 15 | 5.0 | Exemplary: source locator + E-level + channel + disposition on every entry; channels (analogy vs project-inference) separated. |
| Uncertainty expression | 10 | 5.0 | HYPOTHESIS/OPEN/DEFERRED kept distinct; no DECIDED/FACT; E2 cap enforced; assumptions labeled E0. |
| Reader fit | 10 | 4.5 | No-context reader answered all Layer-1 + core Layer-2 questions. |
| Maintainability | 10 | 4.5 | Single-source discipline; append-only SUPERSEDE reversal policy; dated stamps; volatile facts pointed-to, not copied. |
| Concision | 5 | 3.5 | Some restatement between front-matter and the "Discipline held" intro (−1.5). |

```
raw   = 4.5·20 + 4.5·15 + 4.0·15 + 5.0·15 + 5.0·10 + 4.5·10 + 4.5·10 + 3.5·5 = 450
total = raw / 5 = 90
```

**QUALITY_BAND=PASS** — total 90 ≥ 75; min dimension 3.5 ≥ 2.5; **non-compensatory rule holds** (no critical
dimension < 3.5, and none substantiates a paired structural gate). ADR/decision rationale anchor: satisfied —
the register records *why the decision is uncertain* (A1/A2 unevidenced, no head-to-head), names the standing
alternative (reject/defer to standard NLP: SQP/AL/interior-point), and the consequences (H-1 cannot promote
until A1/A2 + O-G4). It correctly records **no** decision, so "rejected alternative" is documented as a route,
not a taken choice.

## No-context reader test (two-layer) — PASS

A fresh reader given **only** the register (no rubric/hard-fail/chat) answered every Layer-1 comprehension +
location question (Q1–Q5) and all core Layer-2 questions (Q6 next-step+DoD, Q7 decided-vs-candidate, Q11
fallback). It independently confirmed: nothing is DECIDED/verified; the E2 cap is held; H-1's two enabling
assumptions are honestly labeled E0 and "not papered over". `READER_TEST=PASS`; HF-8 clear.

**RECONCILE of the reader's caveats:**
- *Per-gap DoD is qualitative* (reader Q6) → **valid trade-off / MINOR**, not a defect: a decision register's job
  is to record state + disposition + route; crisp acceptance metrics belong to the downstream
  research-question-and-literature-planner / experiment plan. Not a contract-misread; HF-15 is N/A here.
- *Contingency not enumerated as a full tree* (reader Q11) → **MINOR**: the routes, the reject/defer alternative,
  and the SUPERSEDE reversal policy are all present; the reader could answer the fallback question.
- *Front-matter/intro redundancy* (reader Q10) → **NIT** (concision). Defensible defensive redundancy.

None is a contract-misread on a core question, so none feeds the non-compensatory FAIL.

## Explicit note — what is CORRECT here and must NOT be graded as a defect

Per the evaluation directive, the following are **correct behaviors of this artifact type** and are **rewarded,
not penalized**:

1. **E2-capped, analogy-only evidence (H-1 at E2).** The register carries the RES cross-domain-analogy cap
   unchanged and refuses to promote paper/analogy past E2. This is **HF-10 compliance** and, per hard-fail.md's
   HF-12D asymmetry, an **explicitly-labeled transfer gap is rewarded**. Capping H-1 at E2 is right, not a gap.
2. **OPEN enabling assumptions at E0 (O-A1, O-A2) and OPEN/DEFERRED gaps (O-G1–O-G4).** A decision register is
   *supposed* to hold uncertainty. Labeling A1/A2 as `OPEN`/E0 and routing the gaps is **HF-12A/E + HF-7
   compliance**. Their presence is the artifact working as designed — not incompleteness.
3. **No entry is DECIDED (all `decided_by: null`).** Correct: no human/gate has decided (directive §3.2). The
   register records state; it does not decide. Grading "no DECIDED entry" as a shortfall would be **wrong** — the
   decision is genuinely unmade, and the register says so explicitly and consistently.

## Fix list (severity-ordered; all non-blocking — advisory only)

1. **MINOR** `gap-task-dod-qualitative` — optionally add a one-line measurable acceptance per gap-closing task
   (or a pointer to where the downstream planner/experiment will define it). Improves Actionability; not required
   for this artifact type.
2. **MINOR** `contingency-not-fully-enumerated` — a compact "if A1 fails → …/ if A2 fails → …/ if O-G4 fails → reject/defer"
   line would make the fallback explicit rather than inferred.
3. **NIT** `intro-frontmatter-redundancy` — trim the overlap between the front-matter narrative fields and the
   "Discipline held" intro.
4. **FYI** `factual-validity-partial` — the two inline external DOIs (S2 10.1137/110845768, S5 10.1007/s10589-021-00336-w)
   were not opened in this isolated run; `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`. The register does not *assert*
   those papers' contents (it carries the RES E2 cap), so this caps only the deepest literature-support claim.

## Factual-validity & confidence notes

- **Verified:** the internal provenance chain — the register faithfully and conservatively transcribes
  research-evidence-map.md (E-levels, channels, dispositions, routes) and literature-search-plan.md's transfer
  warning; no evidence is laundered upward. (`SOURCE_COVERAGE=2/4` on load-bearing cited sources opened.)
- **Not verified here:** the terminal external primary literature (the DOIs / papers S1–S5). Out of scope for
  this read-restricted isolated run and no live fetch performed → `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`.
- **Confidence** in the doc-only structural verdict is **HIGH** (clean deterministic checkers + full gate walk +
  a confirming no-context reader test). One method caveat: `canonical-source-map.md` was not loaded (read-scope
  restriction); it grounds HF-14b, which is N/A for this artifact type, so the omission does not affect the verdict.

## Authority & read-only assertions

- This evaluator asserts **no authority** to publish, move, delete, overwrite, install, or enable auto-trigger on
  anything. `GATE_DECISION=ALLOW` is **advisory** — it means "structurally sound within a supported profile," not
  "approved to proceed." A **human/gate decides**. Because `FACTUAL_VALIDITY=PARTIALLY_VERIFIED`, this ALLOW is
  additionally **not** a green *terminal* gate.
- **Read-only run:** exactly one file was written — this report (`quality-advisory.md`). No other file was created,
  moved, deleted, or modified; the target was not altered.

---

**ADVISORY ONLY — this report records advice, not authorization. It authorizes no action (no publish, move,
delete, overwrite, install, or auto-trigger). A human/gate makes the base/reject/defer decision and any
downstream action.**
