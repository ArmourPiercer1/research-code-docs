# Hard-Fail Catalog (HF-1 … HF-15)

<!--
generated_by_skill: (manual, Phase-1 governance authoring; v0.3 gates added for the hybrid-roadmap false-pass)
skill_version: n/a
source_commit: mattpocock/skills vendored snapshot (plugin.json v1.2.0; no pinned commit)
source_documents:
  - docs/skill-development/quality-control-plan.md §1.1
  - docs/skill-development/reports/documentation-quality-evaluator_独立检查失败复盘与升级要求.md (v0.3 HF-13/14/15 + HF-12 split)
status: DECIDED (v0.3 hard-fail catalog)
last_verified: 2026-07-30
-->


A hard fail is **binary** and is a **release blocker** regardless of soft score
(quality-control-plan §1.1). `check` = how it is detected: `script` (deterministic checker),
`model` (grader judgment), or both.

> **Anti-erosion rule (v0.3, load-bearing).** A hard gate may **not** be silently downgraded to
> MAJOR/MINOR by narrative judgment. If a gate's condition is met, it is a **BLOCKER**. The evaluator
> must walk **every applicable gate and collect ALL blockers** — it may not stop at the first (a
> trivial blocker like HF-9 does **not** excuse skipping the structural gates HF-13/14/15). This rule
> exists because the v0.2 evaluator found the eoopt roadmap's defects but reclassified them as
> compensable soft findings (even the existing HF-6 was talked down to "MAJOR"), then let HF-9
> short-circuit the structural analysis. See the report above.

> **Two-axis verdict + profile severity (v0.4, ADR-DQE-001).** A checker reports a **raw finding**; the
> evaluator maps its **severity** using the caller-supplied `evaluation_profile`
> (`provenance_policy ∈ {controlled, legacy, external}`, `decision_mode ∈ {release-gate, audit}`). The
> verdict has two independent axes: `QUALITY_BAND` (holistic quality) and `GATE_DECISION`
> (ALLOW / BLOCK / INCOMPLETE). A **BLOCKER forces `GATE_DECISION=BLOCK`**; a missing required
> section/input/profile forces `GATE_DECISION=INCOMPLETE` (non-ALLOW, "can't-approve-yet"). DQE **must not
> silently infer** `provenance_policy`/`decision_mode`; if absent ⇒ `GATE_DECISION=INCOMPLETE`. Only HF-9
> and HF-14b are profile-severity-mapped; **HF-12A and HF-15 are unchanged**, and HF-13/HF-14a keep their
> v0.3 thresholds.

| ID | Condition | Check | Detected by |
|---|---|---|---|
| HF-1 | Fabricated **code state** — claims behavior not present in code/tests. | model + script | grader; `run_checks.py` symbol spot-check when a symbol is named |
| HF-2 | Fabricated **literature** — a citation with no resolvable source. | model + script | grader; citation-resolvable check |
| HF-3 | A `CANDIDATE`/`HYPOTHESIS` written as `DECIDED`/`FACT`. | script + model | `status_vocab_check.py` (illegal/blank status) + grader |
| HF-4 | **Overwrote an original** a rewrite skill was told not to touch. | script | no-overwrite diff guard (rewrite skills) |
| HF-5 | **Moved/deleted** files without explicit approval. | script | write-scope guard |
| HF-6 | Roadmap **phase lacks an acceptance *section*** (presence). | script | `roadmap_stage_fields` signal (DoD field absent) + grader |
| HF-7 | Silently **dropped a known OPEN question**. | model | grader diff vs decision register |
| HF-8 | Output only makes sense **with unstated conversation context**. | model | no-context reader test |
| HF-9 | Missing **traceability front-matter** (skill/version/commit/time/status **or** `document_lifecycle`). **Severity is profile-dependent (v0.4, see §HF-9).** | script + model | `frontmatter_check.py` (raw finding) + grader maps severity by `provenance_policy` |
| HF-10 | Treats **paper/indirect evidence (≤E2) as project-verified (E3+)**. | script + model | evidence-level tag check + grader |
| HF-11 | A skill **without passing evals auto-triggered**. | script | registry guard (`auto_trigger` vs `evals`) |
| HF-12 | A **load-bearing claim** is unsupported / mis-supported (see HF-12A–E below). | model + script | grader claim→evidence map + `run_checks` where a symbol/citation is named |
| **HF-13** | **Mixed artifact responsibilities** — one file carries multiple formal doc roles of **divergent lifecycle** as body-level content, with observable harm. | model | grader, fed by `artifact_role_mixing` + `state_number_consistency` signals |
| **HF-14a** | **State contradiction** — mutually contradictory state values in the doc/corpus. | model + script | grader confirming a `state_number_consistency` candidate |
| **HF-14b** | **Volatile-state contamination** — a *stable-design* doc embeds volatile state with no single dynamic source. **BLOCKER only under `controlled + release-gate` (v0.4, see §HF-14b map).** | model + script | grader (type + profile-gated) + `completion_open_conflict` signal |
| **HF-15** | **Non-executable committed milestone** — a *committed* roadmap phase's acceptance is non-measurable/vague. | model | grader, fed by `roadmap_stage_fields` (vague-DoD flag) |

## HF-12 — claim→evidence support, decomposed (v0.3)

**Adopted from research-paper-writing's claim→evidence rule (MIT), sharpened per the third-party audit
§3.3/§5.4.** For state reports, evidence matrices, roadmaps, and algorithm specs, every load-bearing
claim ("X converges", "Y is the bottleneck", "Z was chosen because…") is checked on five axes. The
axes are **partitioned by what they require**, so the evaluator can never report "HF-12 PASS" on
citation density alone when it never opened a source (the exact v0.2 bug — it passed HF-12 "纪律很强"
while its own report said "本区无参考库，逐条解析未做").

| Sub-gate | Question | Requires | Feeds |
|---|---|---|---|
| **HF-12A** Traceability | Does a load-bearing claim carry a source/experiment/ADR/decision handle **or** an explicit `assumption`/`OPEN` label? | doc only | DOCUMENT_QUALITY |
| **HF-12E** Evidence-status labeling | Is each conclusion tagged: `direct` / `same-domain-indirect` / `cross-domain-analogy` / `project-inference` / `assumption-open`? | doc only | DOCUMENT_QUALITY |
| **HF-12B** Source accessibility | Does the cited target exist and is it reachable by the evaluator? | source access | FACTUAL_VALIDITY |
| **HF-12C** Actual support | Does the source support **this specific** conclusion, not merely the topic? | source access | FACTUAL_VALIDITY |
| **HF-12D** Transfer assumptions | Is the leap from the source's domain to this project's claim **stated** (e.g. matrix-manifold result → general implicit-constraint manifold)? | source access | FACTUAL_VALIDITY |

- **HF-12A / HF-12E are doc-only** → they contribute to `DOCUMENT_QUALITY` and fire even with zero
  source access. A bare load-bearing claim with no handle and no `assumption/OPEN` label → FAIL.
- **HF-12B / HF-12C / HF-12D need source access.** When cited sources are unread/unreadable, these are
  **UNVERIFIED**, not passed: `SOURCE_COVERAGE` drops, `FACTUAL_VALIDITY ≤ PARTIALLY_VERIFIED`, and the
  report may **not** claim "HF-12 verified/PASS".
- **HF-12D asymmetry:** *reward* an explicitly labeled transfer gap and fire only where the leap is
  **unstated**. (The eoopt doc self-flags one such gap — "把 ManES 式切空间 CMA-ES 落到 eoopt 数值投影隐式
  流形（非矩阵流形）是方法学空白" — that instance is compliant; the many unlabeled transfers are not.)

## HF-9 — profile-aware traceability severity (v0.4)

`frontmatter_check.py` reports a **raw finding** (present / missing). The evaluator maps severity by
`provenance_policy`:

| `provenance_policy` | missing local traceability front-matter |
|---|---|
| `controlled` | **HF-9 BLOCKER** (a doc our system gates for release/merge) |
| `legacy` | **MAJOR** migration finding — not a lone BLOCK, unless the caller explicitly asks for a controlled gate |
| `external` | **MINOR / N-A** — an upstream doc (GitHub, paper appendix, RFC/PEP/KEP) is **never** hard-failed for lacking *our* front-matter |

- A document that carries a `document_lifecycle:` field (`DRAFT|IN_REVIEW|ACCEPTED|DEPRECATED`) **satisfies
  the doc-level status requirement** even without a legacy `status:` field; a legacy `status:` is still
  accepted but is deprecated (ADR-DQE-001 D-14). A document-level `ACCEPTED`/`DECIDED` is **not** a
  claim-level verification.
- HF-9 is the canonical example of the v0.4 rule: **the same raw finding is a BLOCKER, a MAJOR, or N-A
  depending only on the profile.** This is what fixes the v0.3 HF-9 false-fails on external docs (D-01).

## HF-13 — mixed artifact responsibilities (v0.3)

Fires only when **all** hold (a comprehensive single design report must NOT trip this):
1. **≥2 roles of divergent lifecycle** co-reside as **body-level primary content** — divergent =
   different canonical source **and** different natural update-frequency (e.g. a stable roadmap body
   carrying live per-phase `完成状态` blocks + a `用户决定 (本轮 AskUserQuestion)` session record).
2. **Not subordinated** — the divergent roles are not placed under an explicit `附/appendix/详见 <link>/
   see <doc>` structure with a single stated update mechanism.
3. **Observable harm** — concrete duplication, an actual drift/contradiction (e.g. the 59-vs-69
   split), a mislocated canonical state, or a reader who cannot name the single owning doc.

**Escape hatch (protects a legitimate comprehensive report):** explicit appendix/link subordination
+ one stated update mechanism + no observed drift → **not** HF-13. Judge by **role & lifecycle**, never
by heading count. The report emits: inferred role list, each role's update frequency, the conflicting
sections, and recommended split targets. **A hybrid file is a *defect surface*, not a comfortable union
of gate sets** — do not "merge the applicable HF sets" and relax; hybridity itself is the finding.

## HF-14a / HF-14b — volatile state (v0.3, profile-qualified v0.4)

- **HF-14a State contradiction** applies to **all artifact types**. Two locations assert incompatible
  state about the **same state variable, same scope, same time** (test counts, completion, dates, phase
  status — e.g. "59 tests pass" vs "69 tests pass", both claimed current). Near-binary; the grader confirms
  a candidate surfaced by `state_number_consistency`. **Does NOT fire on** (v0.4 contract sync, D-03): a
  dangling TOC / removed-section anchor (that is **link/navigation integrity**, not a state contradiction);
  a missing metadata field; `document_lifecycle` differing from a claim status; a stable architecture with
  a non-blocking open question; a historical snapshot next to a clearly-dated current value.
- **HF-14b Volatile contamination** applies **only to stable-design types** (roadmap / architecture /
  vision / ADR / algorithm-spec). A stable doc embeds volatile counts/progress/completion **without a
  timestamped pointer to a single dynamic source** (per `canonical-source-map.md`). **Type-gated: does
  NOT apply to state-report / experiment-report / status types** — those are *supposed* to carry live,
  timestamped numbers (this protects a legitimate state report from a false-fail).

### HF-14b severity map (v0.4, ADR-DQE-001 Decision 6 / D-7)

HF-14b is **BLOCKER only** when ALL hold: (1) a stable-design `artifact_type`; (2) `provenance_policy:
controlled` **and** `decision_mode: release-gate`; (3) the doc is a declared canonical / BASELINE /
ACCEPTED design; (4) a dynamic fact is written as a bare **current** claim ("当前"/"目前"/"现有 N 项测试
通过"/undated active progress); (5) **no escape hatch** (an `as-of` date · a canonical dynamic-source
pointer · an auto-update mechanism · an explicit "historical snapshot" label · subordination to a status
appendix); (6) real drift risk / false ownership.

| profile / mode | handling |
|---|---|
| controlled + release-gate | **BLOCKER** |
| controlled + audit | MAJOR finding (does not force BLOCK) |
| legacy + audit | MAJOR migration finding |
| external + audit | MINOR/MAJOR — never a lone BLOCK |
| status / experiment report | N/A (owns its live facts) |
| dated snapshot + pointer | PASS / escape |
| two conflicting *current* dynamic values | that is HF-14a, not HF-14b |

This is a **narrowing** of HF-14b, not an expansion — it does not mean "any test count auto-fails".
Regression triad (byte-identical): `BP-002-fail` (release-gate → BLOCK) · `BP-002-audit` (audit → ALLOW) ·
`BP-002-external` (external → ALLOW).

## HF-15 — non-executable committed milestone (v0.3)

Reconciled with HF-6: **HF-6 = acceptance *section* absent (presence, script-detectable). HF-15 =
a *committed* phase's acceptance is present but *non-measurable/vague* (quality, model).** HF-15 fires
only on phases that are **committed** (`✅/🔨/进行中/next`, or lacking an explicit deferral marker).
Phases explicitly marked `远期/后移/待调研/未来` with an acknowledged-open DoD are **not** HF-15 blockers
(they may be MINOR).

**Vague-acceptance blocklist (canonical location — the `roadmap_stage_fields` checker imports this same
list so checker and gate agree):**
`算例届时定` · `届时定` · `跑通即可` · `与基线对照` (alone) · `效果足够好` · `三选一或组合` · `二选一` ·
`后续调研确定` · `后续决定` · `待补充调研` (as the DoD itself) · `效果好` · `明显提升` (no metric).

**Research-phase escape (protects a legitimate research roadmap):** a phase whose DoD is "evidence to
make a decision" passes **iff** it states research-question + minimal-experiment + **metric** +
**GO/MODIFY/STOP** + downstream-route impact. `roadmap_stage_fields` surfaces GO/STOP/metric markers so
the grader can net them against vague-phrase hits.

## Per-artifact applicability

Not every HF applies to every artifact. Each `task-quality` case declares
`hard_fails_guarded: [...]`. Minimum sets by artifact type:

| Artifact | Must guard |
|---|---|
| state report | HF-1, HF-8, HF-9, HF-12A/E, HF-14a |
| goal/scope note | HF-7, HF-8, HF-9 |
| decision register | HF-3, HF-7, HF-9, HF-10, HF-12A/E |
| quality report | HF-8, HF-9 |
| roadmap | HF-6, HF-7, HF-9, HF-12A/E, **HF-13, HF-14a, HF-14b, HF-15** |
| technical-proposal | HF-8, HF-9, HF-12A/E — plus a **release-readiness** check: a `release-gate` proposal missing validation / acceptance / rollback ⇒ `GATE_DECISION=INCOMPLETE` (non-ALLOW) via the proposal rubric + non-compensatory rule; **no dedicated hard gate** (OQ-REPRO/proposal-gate deferred) |
| architecture doc | HF-9, HF-12A/E, HF-13, HF-14b |
| algorithm spec | HF-9, HF-10, HF-12A/E |
| evidence matrix | HF-2, HF-9, HF-10, HF-12A–E |
| experiment report | HF-1, HF-9, HF-10, HF-14a |
| **mixed / hybrid corpus** | **HF-13 first**, then the union of member-type gates — but hybridity is itself the primary finding (HF-13), not a reason to relax. |
| any rewrite output | HF-4, HF-9 |
| any migration | HF-5, HF-9 |

> **Note on the "union of gates" trap.** The v0.2 report classified the eoopt roadmap as a
> "复合型" doc and computed its applicable gates as the **union** of the member types — treating
> breadth as coverage. That is exactly backwards: a file that needs the union of many types' gates is
> a candidate **HF-13**. Classify hybridity as a defect first, then evaluate members.
