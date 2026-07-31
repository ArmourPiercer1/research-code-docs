<!--
generated_by_skill: documentation-quality-evaluator
skill_version: 0.3.0
source_commit: n/a (workspace is not a git repo); target under review = meshkit@c7d8e9f
source_documents:
  - /tmp/b1_eval.txt (assembled grading injection: SKILL.md v0.3.0 + hard-fail.md + rubric.md + canonical-source-map.md)
  - evals/skills/task-quality/fixtures/dqe/boundary/b1-comprehensive-report.md (TARGET, read-only)
  - evals/skills/harness/checkers/run_checks.py (executed; JSON pasted below)
status: DECIDED (evaluation complete)
last_verified: 2026-07-30
-->

# Quality Report — b1-comprehensive-report.md (MeshKit Architecture)

**Target:** `evals/skills/task-quality/fixtures/dqe/boundary/b1-comprehensive-report.md`
**Artifact type (classified):** **architecture doc** — single design document; frontmatter
`generated_by_skill: scientific-software-architect`, title "Architecture — MeshKit adaptive mesh
library", primary responsibility stated verbatim as "the architecture of MeshKit (module boundaries +
the extension seams)".
**Applicable must-guard set (architecture doc):** HF-9, HF-12A/E, HF-13, HF-14b. All HF-1…HF-15 were
walked; applicability noted per gate.
**Evaluation mode:** terminal quality gate, fresh process, no prior project knowledge. Cited MeshKit
sources (ADR-1…6 / `decision-register.md`, `status.md`, CI dashboard, `adapt/base.py`,
`quality/base.py`, `core/topology.py`) are **outside this evaluation context** — judged
DOCUMENT_QUALITY from the doc; FACTUAL_VALIDITY held UNVERIFIED (see §6).

---

## Human summary

This is a **boundary "should-PASS" case**: a legitimate comprehensive single design document that
deliberately does the *right* things a hybrid-defect doc does wrong. It carries appendices that are
**explicitly subordinated**, states **one** update mechanism, and **externalizes every volatile fact**
(live status → `status.md`, test/CI → CI dashboard) instead of embedding it. The v0.3 structural gates
that exist to catch the eoopt-roadmap false-pass (HF-13 / HF-14a / HF-14b / HF-15) each **correctly do
not fire** here. **No blockers.** DOCUMENT_QUALITY = **PASS** (total 88). Because zero cited sources
were openable in this context, FACTUAL_VALIDITY = **UNVERIFIED** — so this PASS is **not** a green
terminal gate for a downstream skill (handoff rules), it means "structurally sound, facts not yet
verifiable here". Remaining items are MINOR polish (unused ADR-5/6 declaration; a couple of unhandled
structural statements; unnamed target reader).

---

## 1. Deterministic checker + signal JSON (run, not eyeballed)

Command:
`PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe evals/skills/harness/checkers/run_checks.py "evals/skills/task-quality/fixtures/dqe/boundary/b1-comprehensive-report.md" --json`

```json
{
  "path": "evals\\skills\\task-quality\\fixtures\\dqe\\boundary\\b1-comprehensive-report.md",
  "files_checked": 1,
  "hard_fail": false,
  "results": [
    {
      "file": "evals\\skills\\task-quality\\fixtures\\dqe\\boundary\\b1-comprehensive-report.md",
      "hard": {
        "frontmatter": { "pass": true, "problems": [] },
        "status_vocab": { "pass": true, "problems": [] }
      },
      "advisory": {
        "markdown_links": { "pass": true, "problems": [] },
        "placeholders": { "pass": true, "problems": [] }
      },
      "signals": {
        "state_numbers":   { "clear": true, "candidates": [] },
        "completion_open": { "clear": true, "candidates": [] },
        "roadmap_fields":  { "clear": true, "candidates": [] },
        "session_residue": { "clear": true, "candidates": [] },
        "role_mixing": {
          "clear": true,
          "candidates": [
            "section-level roles: architecture@L30, validation@L51",
            "mention-level roles: adr"
          ]
        }
      }
    }
  ]
}
```

**Reading of the JSON.** `hard_fail=false`; both HARD checkers pass (frontmatter → HF-9; status_vocab →
HF-3/HF-10). All SIGNAL checkers report `clear:true`. The only non-empty candidate list is
`role_mixing` — a **SIGNAL that does not auto-block**; it flags two section-level roles
(architecture@L30, a validation plan@L51) + a mention of ADR. This candidate is adjudicated for HF-13
in §3 (it lands on the escape hatch, not a defect). `state_numbers`, `completion_open`,
`session_residue` all clear ⇒ no HF-14a / HF-14b / session-residue candidates surfaced.
**CHECKER_STATUS = COMPLETE.**

---

## 2. Hard-gate walk — every applicable gate, all blockers (none downgraded)

| Gate | Applicable | Condition met? | Verdict | Cited basis |
|---|---|---|---|---|
| HF-1 Fabricated code state | partial (needs code) | no doc-level fab signal; not confirmable doc-only | **PASS (doc) / UNVERIFIED (source)** | §2/§3 name design-level symbols (`adapt/base.py :: Strategy`, `quality/base.py :: Metric`, `core/topology.py`), each ADR-attributed; code not opened |
| HF-2 Fabricated literature | N/A | — | N/A | no literature cited; ADR handles are internal decision records |
| HF-3 CANDIDATE-as-DECIDED | applicable | no | **PASS** | `status_vocab` PASS; decided architecture; runtime options labeled "Chosen at runtime" / "or custom", not asserted as fixed |
| HF-4 Overwrote original | N/A | — | N/A | not a rewrite output |
| HF-5 Moved/deleted files | N/A | — | N/A | not a migration |
| HF-6 Roadmap phase lacks acceptance section | N/A | — | N/A | architecture doc, not a roadmap |
| HF-7 Dropped OPEN question | partial (needs register) | unconfirmable; ADR-5/6 declared-but-unused is a candidate | **UNVERIFIED** | frontmatter lists `ADR-1..6` but body cites only ADR-1–4; cannot diff `decision-register.md` here (MINOR + factual follow-up, §7) |
| HF-8 Needs unstated chat context | applicable | no | **PASS** | reader answered Layer-1 Q1–Q4 from the doc alone (§4) |
| HF-9 Missing traceability frontmatter | applicable (must-guard) | no | **PASS** | `frontmatter_check.py` PASS; all keys present (generated_by_skill/skill_version/source_commit/source_documents/status/last_verified) |
| HF-10 ≤E2 treated as E3+ | N/A | — | N/A | no evidence-level / paper-vs-project claims |
| HF-11 Unevaled skill auto-triggered | N/A | — | N/A | registry gate, not about target content |
| **HF-12A** Traceability (doc-only) | applicable (must-guard) | no | **PASS** | every contested design decision carries a handle: core-stable→ADR-1, refinement seam→ADR-3, quality seam→ADR-4, geometry backend→ADR-2 |
| **HF-12E** Evidence-status labeling (doc-only) | applicable (must-guard) | no | **PASS (w/ MINOR)** | uniform, unambiguous `decision→ADR-N` labeling; explicit `direct/…/assumption-open` tags absent but not hidden — every claim is a decided architecture choice (MINOR, §7) |
| HF-12B/C/D Source support | applicable (needs sources) | **not verifiable here** | **UNVERIFIED** | 0 of the load-bearing cited sources openable ⇒ FACTUAL_VALIDITY=UNVERIFIED; **not** reported as "HF-12 PASS/verified" |
| **HF-13** Mixed artifact responsibilities | applicable (must-guard) | **no — escape hatch** | **PASS** | full 3-condition analysis in §3 |
| **HF-14a** State contradiction | applicable | no | **PASS** | `state_numbers` clear; the doc carries no volatile counts anywhere to contradict |
| **HF-14b** Volatile-state contamination | applicable (must-guard) | no | **PASS** | doc explicitly externalizes: "live implementation status is NOT here — see `status.md`"; "test counts/CI are NOT here — see the CI dashboard"; App B is "the *plan*, not results — results live in CI" |
| HF-15 Non-executable committed milestone | N/A | — | N/A | not a roadmap; no committed phases; App B criteria are measurable, not vague |

**BLOCKERS = [] (none).** No applicable gate's condition is met. Nothing was downgraded — there was
no met gate to downgrade. The two "UNVERIFIED" rows (HF-12B/C/D, and HF-7/HF-1 source-side) are a
**factual-validity** state, not a doc-quality failure, and are reported as such.

---

## 3. HF-13 adjudication (the crux of this boundary case)

The `role_mixing` signal surfaced `architecture@L30` + `validation@L51`. HF-13 fires only when **all
three** conditions hold. They do not:

1. **≥2 divergent-lifecycle roles as body-level PRIMARY content?** → **NO.** The architecture body
   (§1 boundaries, §2 seams, §3 data model) is the sole primary content. The risk log and validation
   plan are **Appendix A / Appendix B**, and the validation plan is explicitly the *plan* (stable
   design intent), with live results routed to CI — so it does not even carry a divergent *live-state*
   lifecycle. No live per-phase status blocks, no session-decision record embedded in the body.
2. **Not subordinated?** → **NO — it is subordinated, with one update mechanism.** Header:
   "Appendices A–B are **subordinate** to it". Section titles: "Appendix A — Risk log (**subordinate to
   §2**)", "Appendix B — Validation plan (**subordinate to the architecture**)". Single stated update
   mechanism: "this doc changes only when an ADR changes the architecture; live status → `status.md`;
   test counts/CI → CI dashboard."
3. **Observable harm?** → **NO.** No duplication, no drift/contradiction (`state_numbers`,
   `completion_open`, `session_residue` all clear), no mislocated canonical state; and the reader test
   (§4) confirms a fresh reader **can** name the single owning doc for each fact (architecture doc owns
   architecture; `status.md` owns live status; CI owns tests).

**Escape hatch satisfied** (explicit appendix/link subordination + one stated update mechanism + no
observed drift) ⇒ **HF-13 does NOT fire.** Judged by role & lifecycle, not heading count. The
`role_mixing` checker output is a SIGNAL adjudicated to the escape-hatch case — treating this doc's
breadth as a hybrid defect would be exactly the false-*fire* mirror of the v0.2 false-*pass*, and the
doc's own structure pre-empts it.

**Reverse-outline coherence (feeds Information architecture).** Thesis: MeshKit architecture = module
boundaries + extension seams. §1→boundaries, §2→seams, §3→data model all map to the thesis; App A and
App B map as explicitly-subordinated support. **No orphan section; no section maps to a different
goal** ⇒ no HF-13 IA signal, IA uncapped.

---

## 4. Two-layer no-context reader test (fresh reader, artifact-only)

A fresh sub-agent was given **only** the target text (no rubric, no hard-fail, no author intent).

**Layer 1 (comprehension + location).** Q1 goal ✔ (MeshKit architecture: boundaries + seams).
Q2 primary responsibility ✔ (quoted verbatim) — **but target reader not explicitly named** →
"CANNOT DETERMINE" for the audience (MINOR, reader-fit). Q3 state + canonical source ✔ — reader
correctly reported `status: DECIDED`, live status → `status.md`, tests → CI dashboard. Q4 where
ADR/spec/status live ✔. Q5 open questions/risks ✔ (Appendix A). **Layer-1 Q1–Q4 answerable ⇒ HF-8
PASS.** Q3 (canonical state-source) — the exact question mis-demoted in the v0.2 eoopt case — is
answered **cleanly** here.

**Layer 2 (execution + refutation).** Q6 next-step+DoD → reader noted the doc is a DECIDED architecture
doc with no task list (correct for the artifact type; **not** a misread) and still located the
measurable conformance DoD in Appendix B ("preserves a valid half-edge mesh on the 5 conformance
meshes"; "returns values in its declared range on degenerate + regular elements"). Q7 decided-vs-
candidate ✔ (architecture DECIDED; runtime-selected strategy/metric are the optional/pluggable part).
Q8 unsupported claims → surfaced `io/` and the one-way dependency rule as lacking an explicit handle,
and ADR-5/6 as declared-but-unused (all MINOR, §7). Q9 fastest-staling facts → correctly "points
elsewhere" (status.md, CI). Q10 orphans → none. Q11 fallback → located in the risk log ("keep 2
built-ins until a 3rd real need"; "benchmark before adding a 2nd backend").

**RECONCILE.** The Q2 audience gap and the Q8 handle gaps are **actionable MINORs**. The Q6 "no next
step" is a **valid trade-off** of the artifact type (architecture doc ≠ roadmap), self-attributed by
the reader, **not** a contract-misread — and the reader still produced the seam DoDs. **No
contract-misread on a core question, and none touching canonical state-source or a DoD.** ⇒ the
non-compensatory Reader-actionability trigger does **not** fire. **READER_TEST = PASS.**

---

## 5. Rubric (scored only because all applicable hard gates pass)

| Dim | Wt | Score | ×Wt | Justification (cited) |
|---|---:|---:|---:|---|
| Factual accuracy | 20 | 4.0 | 80 | Key decisions all trace to ADR handles; independent verification not possible here (UNVERIFIED), and ADR-5/6 declared-but-unused → not a full 5 |
| Information architecture | 15 | 5.0 | 75 | Each fact in its canonical home; clean boundaries; appendices explicitly subordinated; no duplication; reverse-outline: no orphans (§3) |
| Actionability | 15 | 4.0 | 60 | Concrete extension seams + **measurable** conformance criteria (App B); it is a design doc, not a task list, so no next-step list is expected |
| Evidence traceability | 15 | 4.0 | 60 | Source handles present for all contested decisions; missing E0–E5 tags and a couple of unhandled structural statements (`io/`, dependency rule) keep it below 5 |
| Uncertainty expression | 10 | 4.5 | 45 | DECIDED kept separate from volatile status; runtime options labeled optional; risks + mitigations in App A; nothing mislabeled |
| Reader fit | 10 | 4.5 | 45 | No-context reader acted immediately (§4); −0.5 for unnamed target reader |
| Maintainability | 10 | 5.0 | 50 | Strict canonical-source discipline; single update mechanism; volatile facts pointed-to, not copied (`canonical-source-map.md` compliant) |
| Concision | 5 | 5.0 | 25 | Tight; nothing removable without loss |

```
raw   = 80+75+60+60+45+45+50+25 = 440
total = 440 / 5 = 88
```

**Pass-line check:** all applicable hard gates pass ✔ · total 88 ≥ 75 ✔ · min dimension 4.0 ≥ 2.5 ✔ ·
non-compensatory rule holds ✔ ⇒ **DOCUMENT_QUALITY = PASS.**

**Non-compensatory rule (explicit).** Critical dims: DoD-clarity (App B criteria measurable — no HF-15,
N/A) · State-consistency (Evidence/Factual; HF-14a not substantiated — no state numbers) ·
Canonical-source (Maintainability 5.0; HF-14b not substantiated — facts externalized) · Claim-support
(Evidence traceability 4.0 ≥ 3.5; even at a stricter 3.5, HF-12A/E do **not** substantiate — the
unhandled items are definitional/structural, and every contested decision carries a handle) ·
Reader-actionability (Reader Layer-2 PASS, §4). **No critical dimension substantiates its paired gate
⇒ no non-compensatory FAIL.**

**Rationale anchor (architecture leans on ADRs).** The doc correctly **delegates** "why / rejected
alternative / consequences" to the ADRs (`canonical-source-map.md`: architecture rationale → ADR, do
not re-argue) and even summarizes that ADR-2 ("fat vertex" rejected + memory consequence) and ADR-3
("single hard-coded strategy" rejected + consequences) hold them. This is correct canonical discipline,
**not** a rationale-anchor cap.

---

## 6. Source coverage & factual validity

**Load-bearing cited sources (claim-supporting):** ADR-1, ADR-2, ADR-3, ADR-4 (in
`decision-register.md`) + 3 named code symbols (`adapt/base.py :: Strategy`, `quality/base.py ::
Metric`, `core/topology.py`) = **7**. Pointer-only targets (`status.md`, CI dashboard) are excluded
from the claim-support denominator (they back deliberately-externalized volatile state, not a claim).

**Opened:** 0 — these are fictional/staged MeshKit sources outside this fixture's evaluation context;
per the skill's "sources not readable here" failure mode and the task's no-outside-knowledge rule, I
did **not** fabricate their contents. ⇒ **SOURCE_COVERAGE = 0/7**, a hard floor ⇒ **FACTUAL_VALIDITY =
UNVERIFIED**. HF-12B/C/D and the source side of HF-1/HF-7 remain **UNVERIFIED**, not passed. This does
**not** rescue or damage the doc-only verdict — DOCUMENT_QUALITY is judged from the doc; the structural
gates fired (or here, correctly did not) regardless of source access.

**Terminal-gate contract.** DOCUMENT_QUALITY=PASS **with** FACTUAL_VALIDITY=UNVERIFIED is **not** a
green terminal gate. A downstream skill may proceed only on
`DOCUMENT_QUALITY=PASS AND FACTUAL_VALIDITY≠UNVERIFIED AND CHECKER_STATUS=COMPLETE AND READER_TEST=PASS`.
Here the FACTUAL_VALIDITY clause is unmet → **hold**: "structurally sound, facts not yet verifiable
here." A home-repo re-run that opens ADR-1–4 + the 3 code symbols would lift HF-12B/C/D and confirm
HF-1/HF-7.

---

## 7. Severity-labeled fix list (leverage-ordered)

- **BLOCKER** — none.
- **MAJOR** — none.
- **MINOR (evidence traceability / factual follow-up)** — frontmatter declares `ADR-1..6` but the body
  cites only ADR-1–4; **ADR-5/6 are dangling/unused**. Either cite them where they apply or trim the
  declaration. (Also gates an HF-7 "dropped OPEN question" check that is currently UNVERIFIED — cannot
  diff `decision-register.md` here.)
- **MINOR (evidence traceability)** — the `io/` box ("mesh readers/writers (format adapters)") and the
  one-way dependency rule are stated without an explicit handle, unlike core/adapt/quality/geometry.
  Add an ADR handle or mark them explicitly as self-evident structural definitions.
- **MINOR (reader fit)** — name the **target reader/audience** (e.g. "for MeshKit contributors /
  architects") so Layer-1 Q2 is fully answerable from the doc.
- **NIT (evidence-status labeling)** — consider explicit evidence-status tags (e.g. `decision`/`direct`)
  though `decision→ADR` is acceptable labeling for an architecture doc.
- **FYI** — FACTUAL_VALIDITY is UNVERIFIED only because the cited ADRs/status/CI/code are outside this
  evaluation context; re-run in the MeshKit repo to verify claim support and lift the gate.

---

## 8. Verdict block (machine-parseable — verbatim keys)

```
DOCUMENT_QUALITY=PASS
FACTUAL_VALIDITY=UNVERIFIED
READER_TEST=PASS
CHECKER_STATUS=COMPLETE
SOURCE_COVERAGE=0/7
CONFIDENCE=HIGH
BLOCKERS=[]
FILES_READ=[/tmp/b1_eval.txt (injected SKILL.md v0.3.0 + hard-fail.md + rubric.md + canonical-source-map.md + TARGET), evals/skills/task-quality/fixtures/dqe/boundary/b1-comprehensive-report.md, evals/skills/harness/checkers/run_checks.py (executed)]
```

Caller line: `VERDICT=PASS total=88 blockers=[]`
Note to caller: PASS is **not** a green terminal gate — `FACTUAL_VALIDITY=UNVERIFIED` (0/7 sources
openable here). Structurally sound; verify claim support in the MeshKit repo before any downstream
skill proceeds.
