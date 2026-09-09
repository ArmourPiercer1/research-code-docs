# DSH Workflow Evidence Map (Phase 1)

> generated_by: phase1-dsh-synthesis-subagent
> inputs: charter §4–§7 (`docs/plans/active/research_software_agent_workflow_reconstruction_charter.md`); `intermediate/dsh-current-state-findings.md` (CSF); `intermediate/dsh-history-findings.md` (DHF); `phase0/existing-skill-classification.md` (ESC); `phase0/pain-point-evidence.md` (PPE); `<dsh-checkout>\` (read-only, spot-check only). All phase0 files were present at launch — no PENDING-PHASE0 marks.
> method: one section per mechanism of the CSF §10 register (M1–M32, verified 32/32 rows); each section completes the charter §5 nine-link chain; CSF/DHF are the primary evidence, DSH (a separately-maintained agent-harness codebase used as the reference system; hereafter "DSH") repo re-inspected only to fill citation gaps; "here" = the project (an agent-skills repository for research-software documentation), judged against ESC/PPE.
> date: 2026-09-09
> status: DRAFT-for-review
> sanitization: de-identified for external review (paths→placeholders; project/vendor names→neutral; see ../README.md)

Citation convention: `CSF §n` / `DHF A.x|B.x` = the two intermediate files; `file:line` and commit hashes are as recorded in those intermediates (spot-verified there, not re-derived). Enforcement split inherited from CSF §10/§13: 14 machine-enforced / 10 mixed / 8 prose-only of 32.

## M1 — Layered AGENTS.md standing orders (root + 15 subtree + CLAUDE.md symlink)

1. **Observed mechanism.** 20 in-repo `AGENTS.md` files; root (154 lines) owns standing orders, every subtree file opens by linking up; rules are 1–3 lines pointing to their home (CSF §1, §10 M1; DSH `AGENTS.md`, `packages/AGENTS.md:3`).
2. **Problem it solved.** Agents need in-context rules every session without loading everything; rules drifted and accumulated across sessions (CSF §10 M1).
3. **Historical evidence it mattered.** Root file grew 341 B (`b67e81ac97`) → 54,446 B peak (`4d89bb3e74`, 2026-07-02); the compression trigger records "8,130 words in 50 commits with the same rule stated two and three times" (`aa36b3b36b`, 2026-07-04) (DHF A.7).
4. **How encoded.** Root = standing-order owner; subtree files "supplement the repo-wide conventions"; each rule links to rationale (Agent Note) or detail (doc); machine-checked word budgets (`verify-doc-budgets`, manifest ceilings incl. AGENTS.md 1950) (CSF §1 cross-ref pattern, §6.2).
5. **Evolution.** 78% cut in one commit (`7702a33531`: 54,446→11,702 B) — worked examples relocated to `docs/AGENTS.md`, `docs/testing.md`, Agent Notes, not deleted; bounded accretion back to 16,478 B / 154 lines at HEAD (DHF A.7; CSF §0).
6. **Removed/simplified.** Worked examples out of the root file; the file never grew past its budget again (budget gate first caught its own standard at 1,057 > 1,000 words) (DHF A.7).
7. **Same problem here?** Yes — "current state" is stated in ≥6 places (registry meta, README, system-architecture §13, roadmap, runlog, conflict-matrix header, CHANGELOG) and the copies drift (ESC §4 problem 8; G1; PPE P5). There is no single in-context standing-order file; each of 14 SKILL.md files carries its own conventions.
8. **Transferable principle.** One canonical in-context standing-order owner per subtree; every rule is a pointer to its home (rationale vs detail); instruction files carry a machine-checked word budget so accretion is visible.
9. **Must NOT copy.** DSH's ~30 concrete standing orders (ESM, branded ids, plugin-not-loop-change, model-visible⟺logged…); the 1,950-word ceiling values; the CLAUDE.md symlink pair (see closing §D).

## M2 — Agent Notes as RFC/decision records (why + rejected alternatives)

1. **Observed mechanism.** `.agents/notes/` corpus: 852 English notes (proposed 26 / implemented 645 / rejected 10 / archived 171); path encodes `{lifecycle}/{class}/yyyy-mm-dd-topic`; mandatory `Alternatives considered`; "every new note triggers a supersession check" (CSF §3.1–3.2, §10 M2; `.agents/notes/README.md:9,19`).
2. **Problem it solved.** Code/tests show what, not why; rationale lost when agents turn over (CSF §10 M2).
3. **Historical evidence it mattered.** ADR/RFC trees unified 2026-06-18 after ~40 cross-refs needed machine-checkable rewriting (`7c400e9c02`); uniform format 2026-07-05 justified by "nineteen files show what convention alone achieves" (`e6fad266a6`); "non-trivial change requires a note" adopted 2026-07-19 because review alone couldn't classify triviality (`b1b57a0ac5`) (DHF A.8).
4. **How encoded.** Per-lifecycle skeleton gated by `verify-agent-note-format` (present-tense Decision/Consequences in `implemented/`, proposal-era headings banned); closed 6-class set gated by `verify-agent-note-classification`; trilingual triplet + pairing gate; proposed→implemented is a *rewrite*, not a move (CSF §3.1–3.2).
5. **Evolution.** Name/location churn: ADR → RFC → Agent Note; `docs/adr/`+`docs/rfc/` → `docs/rfc/` → `.agents/notes/` (2026-07-19, `e8eddc7ef8`); generated `INDEX.md` deleted after ~1 month (`4779d04af8`); frozen sealed archive added 2026-07-26 (`37140bf823`); supersession check mandated 2026-07-27 (`6241eb6044`) (DHF A.8).
6. **Removed/simplified.** `INDEX.md` ("centralized inventory creates a merge hotspot without providing discovery"); rejected notes deleted as full triplets when they no longer prevent a mistake; consolidation rule (2026-07-25, `45034edd1a`) lets a successor absorb a fully-superseded note and delete it (CSF §3.2; DHF A.8.6).
7. **Same problem here?** Yes, acute — the decision backlog has "no cheap durable home" (PPE cross-cutting obs. 3): ≥4 blocking human rounds (P7), D-17 status stored inconsistently in 4 files, ADR-DQE-001's OQ-REPRO=A rationale "falsified but never annotated" (P4). UDM's decision register + ADR-DQE-001 exist but corrections land in narrative reports, not the record (PPE cross-cutting obs. 2).
8. **Transferable principle.** Decision notes with path-encoded lifecycle, mandatory alternatives considered, supersession-checked at creation, frozen archive for retired ones; the note is an RFC, not a log.
9. **Must NOT copy.** The trilingual `.zh.md`/`.i18n.yaml` triplet and pairing gate (M15); SHA-256 content sealing (M18 — overkill at this corpus size); research evidence needs richer provenance fields (source, strength, verification state) than DSH's class folders give — charter §7 example.

## M3 — Skills catalog with frontmatter trigger contract

1. **Observed mechanism.** 11 skills, each a `SKILL.md` whose YAML frontmatter (`name`+`description`) is the trigger contract; `disable-model-invocation`/`user-invocable` flags for explicit-invocation-only skills; cross-skill relative links form a workflow graph (CSF §2, §10 M3; `.agents/skills/dsh-translate-docs/SKILL.md:4-6`).
2. **Problem it solved.** Situational procedures must load on demand, not as standing prose (CSF §10 M3).
3. **Historical evidence it mattered.** Skills were created as standing orders bloated (M1 history); `dsh-doc-standards` (56 lines) later absorbed into `dsh-doc` — consolidation as a first-class operation (`0b5eba0c8d`, 2026-08-25) (DHF B.6; CSF §2).
4. **How encoded.** Frontmatter + `verify-skill-invocation-metadata` aligning frontmatter with per-skill `agents/openai.yaml` (vacuous today — no such file in checkout); invocation internals runtime-side (UNKNOWN) (CSF §2).
5. **Evolution.** Skill set grew to 11 then consolidated (dsh-doc-standards in; OpenAI metadata out, `8c420de301`) (DHF B.6).
6. **Removed/simplified.** `dsh-doc-standards` skill deleted; OpenAI skill metadata removed; Codex-metadata gate currently passes vacuously (CSF §2; DHF B.6).
7. **Same problem here?** Mechanism already exists — all 14 SKILL.md files carry frontmatter, and a frontmatter checker is in the H5 family (ESC H5). The open gap is trigger-evidence: which of the 3 retrieval skills (`wos-research`, `scansci-pdf`, `paper-fetch-skill`) is load-bearing is decided by trigger evals (DHF B.7 candidate 2; ESC S5/S7 boundaries).
8. **Transferable principle.** Frontmatter is the single trigger contract; non-triggers written explicitly; cross-skill links express the workflow graph; overlapping skills get consolidation-or-delete, with the survivor owning every unique proposition.
9. **Must NOT copy.** The Codex `agents/openai.yaml` metadata (absent even in DSH); `disable-model-invocation` semantics tied to DSH's runtime provider (UNKNOWN internals, CSF §12).

## M4 — Pre-release "remove at first tagged release" stance

1. **Observed mechanism.** Standing rule: "Remove at the first tagged release. Until then, prefer correct foundations to compatibility shims: rename or repackage freely… Backends reject old on-disk formats" (DSH `AGENTS.md:5-7`; CSF §0, §10 M4).
2. **Problem it solved.** Pre-1.0 compatibility debt; shims and legacy paths outlive their need (CSF §10 M4).
3. **Historical evidence it mattered.** The stance is the documented engine behind the whole deletion volume: 12+ package removals, ~60 implemented simplification notes in 3 months; "the lifetime of a pre-release abstraction can be hours" (dumble→tsdown same day, `630bbddf9a`) (DHF A.9, B.2.3).
4. **How encoded.** Prose standing order at root and per sub-project (`native/landlock-run/AGENTS.md:7`); no gate — it licenses the gates (CSF §10 M4 enforcement = prose).
5. **Evolution.** Stable since day one; backends fail closed on old formats (`9186824e87`, 2026-08-10) (DHF A.13).
6. **Removed/simplified.** It removes other things (see negative-evidence summary §C); itself never modified.
7. **Same problem here?** Yes — repo is v0.1.0-alpha.1 with frozen bundles, frozen 12-field interfaces, a VOID-but-still-tracked roadmap, and skeleton flows written ahead of executors (ESC G2, S13, S14; PPE P10). Every "freeze" currently behaves like a compatibility promise no one needs yet.
8. **Transferable principle.** Declare a deletion license while pre-release: rename/repackage freely, reject old formats, keep the seam (abstraction) but delete the second implementation.
9. **Must NOT copy.** Nothing structural — but the stance does not erase provenance obligations: DSH still pinned `SCHEMA_VERSION`/`SESSION_FORMAT_VERSION` and froze the archive (DHF A.13; M18). Here: freezing a decision record (ADR) is fine; freezing a *format* pre-release is the debt.

## M5 — Narrow fast git hooks (staged lint+fix, whitespace, vendor manifest; pre-push typecheck only)

1. **Observed mechanism.** `lefthook.yml`: pre-commit = staged translation-pairing, archive-seal guard, staged Oxlint auto-fix+bounded retry, whitespace, vendor-manifest; pre-push = incremental typecheck only; "Keep these local checkpoints fast; CI owns the full repository-wide gate matrix" (CSF §6.1; DSH `lefthook.yml:1-2`).
2. **Problem it solved.** Full pre-push suites delay every push, amplify unrelated flakes, duplicate CI (CSF §10 M5).
3. **Historical evidence it mattered.** Day-one hooks (`9d20a36cc4`) ran typecheck at pre-commit + tests/hygiene at pre-push; the superseding note chain 2026-06-11-quality-gates → 2026-07-06-parallel-pre-push-gates → 2026-07-22-fast-local-git-hooks carries explicit `Supersedes` sections; rationale: "agents already run the tests; hooks add only cheap high-confidence defects" (DHF A.1; CSF §11.8; `31c0589439`).
4. **How encoded.** Hook boundary doctrine in the note + skill: "a complete local rehearsal is reserved for an explicit request, CI diagnosis, or a repository-wide change" (fast-local note:19, cited CSF §7.2).
5. **Evolution.** Three successive redesigns of the same hook/CI symmetry, each note superseding the last (DHF A.1; CSF §11.8).
6. **Removed/simplified.** The `check:pre-push` aggregate deleted — "do not recreate the removed `check:pre-push` aggregate" is now a standing skill instruction (`dsh-pre-push-checks/SKILL.md:68`) (CSF §11.1).
7. **Same problem here?** Partially — the repo has **no git hooks at all** (no `lefthook.yml`/`.github` at root, verified on disk 2026-09-09); enforcement = `run_checks.py` tiers invoked manually or at release, and one checker (`register_check.py`) is orphaned because "a checker that must be remembered to run is not mechanically enforced" (ESC H2). The failure mode is the inverse: no cheap local checkpoint exists.
8. **Transferable principle.** Three-way split: cheap local checkpoint / agent-selected behavioral evidence / exhaustive outer gate; local hooks contain only high-confidence cheap defects; the removed aggregate is named so it is not recreated.
9. **Must NOT copy.** Lefthook itself, translation-pairing hook, vendor-manifest hook (no vendored source here); installing hook infrastructure before the repo has an outer gate (CI or release preflight as the "CI" — `preflight.py` exists, ESC G6).

## M6 — Gate runner with modes + validated dependency graphs

1. **Observed mechanism.** `scripts/run-gates.ts` — single source of gate inventory; modes (`ci-primary/static/coverage/snapshot/artifacts/consumers/doc-sync/doc-quick`…); `needs` vs `after` edges, `allowFailure`, per-gate timing, `DSH_GATE_FAIL_FAST` (CSF §6.2, §10 M6).
2. **Problem it solved.** Long sequential aggregate chains; per-leaf CI jobs duplicating setup; script/YAML inventory drift (CSF §10 M6).
3. **Historical evidence it mattered.** Born `7cd4868056` (2026-07-06 "split primary gates into broad lanes"); the 2026-07-21 rewire routing doc-sync through the scheduler **caught that `verify-cordis-api` had never been gated** — the inventory self-audited (DHF A.1, A.11 row 13; `6fc7dd4c02`).
4. **How encoded.** Package scripts are thin names; the runner owns validated dependency graphs; CI topology itself test-pinned (`scripts/ci-workflow.spec.ts` pins fail-fast flags per job, `c13d1a4285`, `161c6591be`) (CSF §6.2; DHF A.11 row 15).
5. **Evolution.** Scheduler ← doc-sync leaf list (2026-07-21); fail-fast added 2026-08-31 (`161c6591be`, note `2026-08-27-gate-runner-fail-fast.md`) (DHF A.1).
6. **Removed/simplified.** Per-leaf YAML duplication collapsed into one graph; dead `serial-linux` job removed with its dangling references (`e6b494ed17`) (DHF A.1, B.2.8).
7. **Same problem here?** Partially — `run_checks.py` is the analog (HARD/ADVISORY/SIGNAL tiers, ESC H1) but is a flat tier list, not a dependency graph, and its own inventory drifted (H2 orphan; release-manifest's signal list contradicts the runner — D5, ESC G6). The 63M-token P1 runaway was, in part, a plan-inventory failure (PPE P1).
8. **Transferable principle.** One place owns the check inventory + order; the inventory is itself tested; fail-fast on blocking failures; a check that is not in the inventory does not exist.
9. **Must NOT copy.** The 40+ DSH gate leaves (verify-*, catalogs, consumer smokes); mode taxonomy sized for a monorepo CI; here the runner has ~18 checkers — a graph is not yet worth it, but "single source of truth + tested inventory" is.

## M7 — Per-file 100% coverage gate on package src

1. **Observed mechanism.** `test:coverage`: v8 per-file 100% on `packages/*/*/src`; "an uncovered line is often dead code the gate flags for deletion, not a missing test"; `/* v8 ignore */` requires a stated reason (CSF §4.2, §10 M7; DSH `docs/testing.md:10`).
2. **Problem it solved.** Dead code and assertion-free tests accumulate invisibly under aggregate coverage (CSF §10 M7).
3. **Historical evidence it mattered.** Day-one gate `bfb034830f` (2026-06-11); postmortem 0001 proved the limit — 178 green unit tests **and** 100% coverage, product dead on connect (`6d37b6c33d`); acknowledged gap: "100%-coverage pressure can produce assertion-free tests — mutation testing is the planned counterweight", still in `proposed/` (DHF A.1, A.4; CSF §9).
4. **How encoded.** Vitest v8 in the `ci-coverage` lane; uncovered locations printed on failure (`4f7b9ac5ee`); zero-build Windows coverage lane (`e2ef25b06e`) (DHF A.1).
5. **Evolution.** Bar unchanged since day one (the one stable gate); only tooling churn (ESLint→Oxlint beside it) (DHF A.1).
6. **Removed/simplified.** Nothing in the gate; the knip dead-code scanner that covered adjacent territory was removed (`907c6334c1`) — coverage partially inherited that role (DHF B.2.1; CSF §11.3).
7. **Same problem here?** Weakly — Python checkers are validated by planted-defect self-tests ("catches 9 planted defects", ESC H5) rather than line coverage; the live analog is the *assertion-free instrument* risk (DQE v0.2.0 false pass, PPE P2), which line coverage cannot catch.
8. **Transferable principle.** A coverage gate as a *deletion prompt* (uncovered = suspect), per-file granularity so dead files are visible, stated reasons for every exclusion.
9. **Must NOT copy.** The 100% bar and v8 machinery — a pre-release-scale TypeScript choice (CSF §10 M7 "semi-generic (100% bar is a choice)"; DHF A.13 "only feasible at pre-release scale with agent labor"); adopting it for ~18 Python checkers would tax, not clean.

## M8 — Keyless recorded-session snapshot tier

1. **Observed mechanism.** `snapshots/` corpus (session/sdk/acp/web owner trees, 655 files): committed `session.jsonl` = replay input **and** expected output; `record`/`replay`/`refresh` modes; typed redaction tokens; `workspace.expected/` = "independent oracle which record and refresh never rewrite"; CI forces read-only `DSH_SNAPSHOT=replay` (CSF §7.1, §10 M8; `snapshots/AGENTS.md:9,13`).
2. **Problem it solved.** LLM nondeterminism must not block keyless CI; fixtures can drift to encode regressions (postmortem 0002: refresh accepted `UNKNOWN_TOOL` results as new expected outputs — "it proved deterministic replay of the regression rather than successful filesystem behavior", `4afc701e98:19`) (CSF §10 M8).
3. **Historical evidence it mattered.** Introduced 2026-06-19, one day after postmortem 0001 (`1a1ce734ba`); the note records the hand-authored `llm.json` draft replaced by the persisted session log — "record-once, replay-forever" (`2026-06-19-acp-snapshot-tests.md`) (DHF A.3).
4. **How encoded.** Closed `snapshot.yml` manifest per scenario; fixture guards (orphan dirs, unscrubbed headers fail before comparison); `dsh-llm-replay` serves recorded streams keyless; `UNKNOWN_TOOL` rejection in fresh runs + fixtures (CSF §7.1; DHF A.3).
5. **Evolution.** example-local → support package (`556f847064`) → keyless refresh (`9d2cf8ce82`) → web browser lane (`6d3c25f494`) → 2026-08-24 corpus migration (shipped profiles via `dsh`, 12 commits) → envelope projection (`b6e61f61ac`) (DHF A.3).
6. **Removed/simplified.** TUI snapshot tier (`10bb9cbf4a`); "golden" naming → "expected" (`0893aaa7cb`); ACP-as-universal-controller superseded (2026-08-24) (DHF A.3 Deletions).
7. **Same problem here?** Yes — DQE's blind corpus + frozen bundles + adjudication are the recorded-evidence machinery, and the canary found **every LLM-judged signal unstable** across runs while deterministic checkers were stable (PPE P2 unresolved); the P10 provenance gap means "frozen" evidence is partly git-untracked and one preservation claim is already false (registry:26 vs empty dir).
8. **Transferable principle.** Record-once/replay-forever for nondeterministic components; replay is read-only in the gate; refresh = fixture production, never correctness review (0002 lesson); every fixture diff is reviewed; the expected-output oracle is never rewritten by the recorder.
9. **Must NOT copy.** Profile-driven composition manifests, `dsh-llm-replay` server, four owner trees; here replay means pinned seeds + captured model outputs (or deterministic re-grading), not a session-log corpus.

## M9 — Minimal-evidence pre-push skill (change-scope → surface-matched checks)

1. **Observed mechanism.** `dsh-pre-push-checks`: `change-scope` report first (versioned JSON of committed paths vs verified merge base; "the command never guesses or fetches a base"), then per-surface evidence selection (focused tests; `doc-sync`; keyless snapshots; real-API e2e), never repeat a passing check, test-selection vs coverage-selection separation (`vitest related` + scoped `--coverage.include`), lease-protected rewrites, push procedure (CSF §2.1, §7.2, §10 M9; `dsh-pre-push-checks/SKILL.md:19-64`).
2. **Problem it solved.** Agents reflexively run full suites or push unvalidated; "a lot of work" is not a cost when agents do the labor (CSF §10 M9; founding ADR `2026-06-11-quality-gates.md:11-15`).
3. **Historical evidence it mattered.** The superseded full aggregate (`check:pre-push`) was removed precisely because it delayed pushes and amplified unrelated flakes (`31c0589439`); the skill exists since `671cbe173e` (2026-07-06) as the standing procedure root `AGENTS.md:89-95` points at (DHF A.1; CSF §7.2).
4. **How encoded.** Skill prose + one machine piece (`scripts/change-scope.ts`, 248 lines); division of labor repeated in three places: hooks = cheap local defects; agent-selected checks = behavioral evidence for the diff; CI = exhaustive coverage (CSF §7.2).
5. **Evolution.** Full aggregate → agent-selected minimal evidence (2026-07-22 boundary); `gh stack sync` is the sole ordering exception (publish then validate) (CSF §2.1; DHF A.1).
6. **Removed/simplified.** The `check:pre-push` aggregate — named in the skill so it is not recreated (`SKILL.md:68`) (CSF §11.1).
7. **Same problem here?** Yes, and paid for — P1: a background workflow's serialized `args` fan-out burned **~63M tokens / ~11 h for zero data**; the system's response was a pre-launch plan validator + hard caps (`MAX_EVAL_RUNS=64`), i.e. evidence-scope discipline *after* the incident (PPE P1; `benchmark-changelog.md:132-134`). `run_checks.py` tiers are coarse (HARD/ADVISORY/SIGNAL) with no change-scope selection.
8. **Transferable principle** (charter §7 example): "smallest relevant evidence" generalizes to **smallest discriminating experiment** — pick the narrowest check that would fail for the regression; never re-run a passing check; separate *selection* of evidence from the *standard* it must meet; scope the standard to the selected set.
9. **Must NOT copy.** `change-scope.ts` implementation, vitest-specific commands, `gh stack sync` exception, lease-protected-rewrite ritual (single-author repo); the mechanism here is a pre-launch *eval-plan* scope check (already half-built as `validate_eval_plan.py`).

## M10 — CI as exhaustive matrix (PR gates + master standby drills + failover runbook)

1. **Observed mechanism.** `ci.yml` (pull_request only) gathers all jobs into `all checks passed`; `ci-master.yml` re-runs the complete unsharded aggregate serially on self-hosted VMs; failover switch via `vars.DSH_CI_FAILOVER_LINUX` + runbook (CSF §5.1–5.2, §10 M10; DSH `ci.yml:655-677`).
2. **Problem it solved.** Local proof insufficient; enterprise runner-pool degradation (CSF §10 M10).
3. **Historical evidence it mattered.** Day-one CI `86955b96a4`; fresh-clone failures "invisible locally because lib/ persists between runs" — 1,519 `no-unsafe-*` errors from step ordering (`fa91bbac54`); standby-lane note: "a defect in [PR] gate inventory or dependency graph could omit work while the required aggregate stays green" (`2026-07-21-serial-cross-platform-ci-reference.md`, `c86d85724d`) (DHF A.2).
4. **How encoded.** PR-only vs master-only lanes keep PR panels clean (`.github/AGENTS.md:1`); required CI must run on portable (hosted) capacity (`2026-07-23-portable-required-pull-request-ci.md`); latency is observed from timestamps, never encoded as a canceling timeout (DHF A.2).
5. **Evolution.** CI split `61f910d1c6` (2026-08-19); ReFS block-clone fix for a fresh-checkout failure on the self-hosted VM (`4032a0a428`); zero-build coverage lane + fail-fast (2026-08-31) (DHF A.2).
6. **Removed/simplified.** Dead hosted `serial-linux` job (`if: false` since 2026-07-30) removed with its `TODO` references (`e6b494ed17`) (DHF B.2.8).
7. **Same problem here?** No — the repo has **no CI at all** (no `.github/` at root, verified 2026-09-09); outer gate = release `preflight.py` (read-only, exit 0/1/2, ESC G6). The problem class (local proof hides order/dependency defects) has not yet appeared here; 18 commits total.
8. **Transferable principle.** Required gate set must stay runnable on portable capacity; an independent serial full-aggregate is the completeness oracle; performance is observed, not timed-out.
9. **Must NOT copy.** The matrix itself, failover variables, Wine-on-Linux exception, failover runbook — none has a failure mode here yet; charter §12.1 keeps CI "optional" at bootstrap and the ratchet says add it after a concrete need (M5 link 9 same warning).

## M11 — Postmortem → guardrail loop (4 incidents, each ends in tests/gates/rules)

1. **Observed mechanism.** `docs/postmortem/` genre: incident write-ups of bugs that "reached a place it shouldn't have"; opens with Executive summary; **links the guardrails the postmortem motivated**; every postmortem at HEAD ends in tests, gate scripts, or AGENTS.md rules (CSF §4.4, §10 M11; `docs/postmortem/README.md:7,9`).
2. **Problem it solved.** Subtle systemic bugs that escape despite green suites (CSF §10 M11).
3. **Historical evidence it mattered.** 0001 (`6d37b6c33d`): ACP crash at 100% coverage — regression guard landed **in the same commit as the postmortem**, "Verified it fails when `export default apply` is restored"; 0002 (`4afc701e98`): `!!js` object left 7 filesystem scenarios calling absent tools; 0003 (`cd88a339fa`): agent validated a *replacement* server, bare HTTP 200 treated as success; 0004 (`6343d8f6e6`): shared stderr prefix misclassified child failures (CSF §4.4; DHF A.7).
4. **How encoded.** Boundary fixed twice: postmortem = backward-looking failure record ("the only tier where war-story narrative belongs"); Agent Note `bug-fix` = the durable decision it motivates; writing criterion = subtle + systemic + costly to rediscover (CSF §4.4; DHF A.7).
5. **Evolution.** Genre created 2026-06-18 with postmortem 0001 in one commit (code fix + README + layout line + testing rules); 3 more incidents added, each ending in machine guardrails (DHF A.7).
6. **Removed/simplified.** Nothing — the tier is additive and stable; its guardrails *are* other mechanisms (export rule, `verify-cordis-config`, `UNKNOWN_TOOL` guard, `RunnerFailureRule`, web-surface URL) (CSF §4.4 pattern line).
7. **Same problem here?** Yes, repeatedly — P2 (false pass → v0.3 program, ~70M-token causal chain), P3 (corpus defects → mutation postconditions + `validate_mutation_semantics.py`), P6 (3 checker precision bugs found dogfooding), P4 (two rulings colliding). The 4-way defect taxonomy (SKILL/FIXTURE/CONTRACT/HARNESS) is the *classification* half of the loop; the guardrail *genre* and same-change rule are missing — retrospectives are one-off undated docs (PPE P2: "the retrospective doc itself is undated").
8. **Transferable principle.** Incident → named, machine-preferred guardrail (test/gate/rule) landing in the same change; the guardrail proves the incident (fails without the fix); incident tier is the origin of standing orders; a separate durable-decision record carries the "why".
9. **Must NOT copy.** Zero-padded bilingual numbering, "reached a place it shouldn't have" product framing; here guardrails may be checker rules, corpus postconditions, or ADR annotations (P4's ADR was falsified and never annotated — the loop's weakest link is the annotation step).

## M12 — Doc tier taxonomy + one-home-per-fact + word budgets

1. **Observed mechanism.** `docs/AGENTS.md`: tier table fixing the home of each fact type (root AGENTS = standing orders, architecture.md = ordered map, Agent Notes = active decision records, postmortem = incident stories, package README = per-package contract); writing rules (current-state prose, one line per paragraph, slop checklist); wordcount budgets with relocate→condense→raise; machine-checkable relative links only (CSF §4.1, §10 M12; `docs/AGENTS.md:15-29,60-75`).
2. **Problem it solved.** Docs accumulated restated rules and stale summaries; review alone didn't hold (CSF §10 M12).
3. **Historical evidence it mattered.** "Root AGENTS.md reached 8,130 words in 50 commits with the same rule stated two and three times" (`aa36b3b36b`, 2026-07-04); the gate's first catch was the standard itself (1,057 > 1,000 words, shipped condensed to 984); ~40 cross-refs rewritten to machine-checkable links when the ADR/RFC trees unified (`7c400e9c02`) (DHF A.7; A.11 rows 1, 4).
4. **How encoded.** `verify-doc-budgets` (manifest of per-file word ceilings: AGENTS.md 1950, docs/AGENTS.md 1320, testing.md 1300…), `verify-md-links` (missing targets + dead `#fragment` anchors rejected), `verify-md-wrap` (CSF §6.2; DHF A.11 rows 1–4).
5. **Evolution.** Cross-link convention (2026-06-18) → tiers + budgets (2026-07-04) → final standard with dsh-doc/dsh-prose-standard owning placement + editorial judgment (`0b5eba0c8d`, 2026-08-25) (DHF A.7).
6. **Removed/simplified.** Worked examples out of root AGENTS (relocated, not deleted); flat catalogs → per-subsystem generated pages (`f7323354bb`); `docs/cookbook/` split out (2026-06-13) (DHF A.7).
7. **Same problem here?** Yes — the sharpest live pain: "current state" in ≥6 docs, 7 verified live drift instances (SKILL.md:27-28 vs registry:333; README:68 vs :70; quality-control-plan vs hard-fail.md), VOID roadmap still referenced, D-17 split across 4 files (ESC §4 problem 8; PPE P5; P4d). No tier table exists: which doc owns "what is built/passing/deferred" is undecided (D-1 open, PPE P5).
8. **Transferable principle** (charter §7: "generalizes well"). Exactly one home per fact type; current-state docs describe reality, not chronology; standing-order/instruction files carry word budgets; all cross-references machine-checkable.
9. **Must NOT copy.** The specific ceiling values; the tutorial/reference split and website projection (no product doc site); the tier table must be rebuilt around *this* repo's fact types (skill roster, flow state, decision register, corpus, release state) — the table is the design artifact, not the copy.

## M13 — Generated catalogs (tool/config/persistence/Cordis/client) never hand-edited

1. **Observed mechanism.** `docs/*catalog*.md` generated from source; `verify-*-catalog` freshness gates in doc-quick; "generated catalogs are never hand-edited" (CSF §4.5.4, §10 M13; CSF §6.2 gate list).
2. **Problem it solved.** Hand-maintained API tables drift from source (CSF §10 M13).
3. **Historical evidence it mattered.** 2026-06-20: core-data-structures catalog (`0f7abc9808`) + fully generated Cordis catalog (`4e5c08ef82`) — "verify-don't-generate" promoted to "fully generated with freshness gate"; landing the original gate "surfaced three events the table had been missing" (DHF B.6; A.7).
4. **How encoded.** Generation scripts + freshness gates in the doc-sync lane; superseded `verify-event-taxonomy` hand-verified table replaced by generation (`4e5c08ef82`) (DHF A.7, B.6).
5. **Evolution.** Flat catalogs deleted 2026-07-30 (`f7323354bb`) → per-subsystem `cordis-surface` regions generated into each subsystem page (DHF A.7).
6. **Removed/simplified.** Hand-edited flat catalog dirs; the hand-verified event taxonomy gate (superseded, not deleted) (DHF B.6).
7. **Same problem here?** Yes — `skills-registry.yaml` meta block is hand-maintained and already stale (D6/D7/D11, ESC G1); `canonical-source-map.md` (10 rows) is hand-maintained and consumed by two skills (ESC H4); "what is built" is re-stated in 6+ places (ESC §4 problem 8).
8. **Transferable principle.** Derive, never hand-edit, what is derivable; a freshness check makes drift a failure, not a cleanup; the derived artifact is the one home.
9. **Must NOT copy.** The six DSH catalog families (no TS API tables here); do not generate for facts with no machine source — registry *narrative* notes are judgment, only the roster fields (name/path/version/writes/evals) are derivable from SKILL.md + disk.

## M14 — `type-equiv` fences: docs paste source types, gate re-extracts & compares

1. **Observed mechanism.** `docs/subsystems/*.md` paste source-equivalent type declarations as ` ```ts type-equiv ` fences, registered in `scripts/type-equiv.manifest.json`, re-extracted and compared by `verify-type-equiv` (CSF §4.5.5, §10 M14; `docs/development.md:159-167`).
2. **Problem it solved.** Type reference docs drift from source (CSF §10 M14).
3. **Historical evidence it mattered.** `doc-typecheck.ts` 2026-06-14 (`6a528be569`) → `verify-type-equiv.ts` 2026-06-20 (`07048983e0`) — the prose rule "fenced ts blocks must compile; verbatim type pastes" gained a checker (DHF A.11 row 3).
4. **How encoded.** Manifest + re-extract-and-compare gate in doc-quick (CSF §6.2).
5. **Evolution.** Doc-typecheck → type-equiv (compile-check, then drift-check) (DHF A.11).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** Already solved differently — the frozen 12-field handoff + 11 artifact types are checked by `interface_check.py` against the schemas in `references/interfaces/` (ESC H5); no TS type-doc surface exists.
8. **Transferable principle.** Where docs quote source-of-truth structures, paste-and-recompare (drift check), don't paraphrase-and-hope.
9. **Must NOT copy.** The Typert/Cordis mechanics entirely (CSF §10 M14 "DSH-specific"); `interface_check.py` already fills the niche — a second doc-drift gate would be a duplicate ledger (charter §10: "do not create another permanent ledger").

## M15 — Bilingual triplet + pairing records + merge driver + briefing tool

1. **Observed mechanism.** Every human-facing doc = `foo.md` + `foo.zh.md` + `foo.i18n.yaml` (blob-hash pairing record); `verify-translation-pairing` gate; pre-commit staged pairing check; merge driver installed by `scripts/install-lefthook.mjs`; `gen-translation-brief` briefing-driven updates; `dsh-translate-docs` user-invocable-only (CSF §0, §6.3, §10 M15; DHF A.11 row 5).
2. **Problem it solved.** EN/ZH docs diverge; merging one side must not break the other (CSF §10 M15).
3. **Historical evidence it mattered.** Bilingual contract + pairing gate `4d89bb3e74` (2026-07-02); sidecar consistency records `ec05295a0c` (2026-07-03); universalized to triplets `b4d032c1a2` (2026-07-26) (DHF A.8.9, A.11 row 5).
4. **How encoded.** Triplet is the atomic unit; machine-checked header tokens stay English verbatim; format gate skips `.zh.md`, pairing gate checks consistency; "a green pairing hash does not prove translation quality" (CSF §3.1; CSF §2.1 dsh-code-review line 46-48).
5. **Evolution.** Pairing → sidecar records → universal triplets (2026-07-26) (DHF A.8).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** No — docs are EN-dominant with occasional Chinese retrospective docs; no paired-document obligation, no merge-conflict pressure observed (18 commits, single author); ESC records no i18n pain.
8. **Transferable principle.** If paired representations become mandatory, the pairing needs a machine-checked consistency record and a merge-safety story — but only when the obligation exists.
9. **Must NOT copy.** The triplet + sidecar + merge driver + briefing tool: an organizational (the DSH project) requirement mechanized as gates (DHF A.13 "an organizational requirement, mechanized as gates"); not a need of the project at any current corpus size.

## M16 — Issue/PR policy engine (types, priorities, kind/area labels, owner line, board lifecycle)

1. **Observed mechanism.** `.github/issue-management/` — `config.json` (Project board, statuses, fields) + `policy.mjs` (808 lines) with 17KB test suite, executed by a GitHub App; enforced vocabulary: Issue Types, p0–p3, `kind/*` PR labels, retired aliases **reserved so they cannot be recreated**, `Owner: @user` line parsing (CSF §6.4, §10 M16; `policy.mjs:10-37`).
2. **Problem it solved.** Ad-hoc issue vocabulary; unowned items; board state not reflecting PR reality (CSF §10 M16).
3. **Historical evidence it mattered.** Unified label taxonomy note `2026-08-08-unified-github-label-taxonomy.md`; the policy is the mechanical half of the `AGENTS.md:132` standing order (CSF §6.4).
4. **How encoded.** Trusted-branch policy checkout (not PR head); write-capable App token minted only on `changes_requested` (CSF §6.4, §10 M32).
5. **Evolution.** Ad-hoc labels → enforced vocabulary (2026-08-08) (DHF A.7 label note).
6. **Removed/simplified.** Retired label aliases reserved, not deleted (recreation is the failure) (CSF §6.4).
7. **Same problem here?** Partially — the *vocabulary* problem exists (10-value claim-status mixes epistemic + process states, ESC §4 problem 5; colliding decision-ID namespaces, PPE P4), but it is carried by the UDM register + `status_vocab_check`, not a GitHub board; no issue tracker is observed in the repo.
8. **Transferable principle.** A closed, machine-enforced status vocabulary; retired states reserved so they cannot silently reappear; ownership line is parseable.
9. **Must NOT copy.** The GitHub App + Project board plumbing (semi-generic surface, GitHub-specific carrier, CSF §10 M16); here the fix is orthogonalizing the UDM status field (charter §12.6) and merging `register_check` into the runner (ESC H2), not a board engine.

## M17 — No-"golden"-filenames check

1. **Observed mechanism.** `scripts/check-expected-filenames.sh` + `expected-filenames.yml` workflow (path-filtered on `*golden*`): tracked non-vendor filenames must not contain "golden" — the "tests describe behavior, not golden truth" doctrine made mechanical (CSF §5.5, §10 M17; DSH `AGENTS.md:124`; `check-expected-filenames.sh:18-25`).
2. **Problem it solved.** The doctrine needs a mechanical name or it erodes (CSF §10 M17).
3. **Historical evidence it mattered.** Repo-wide "golden" → "expected" rename `0893aaa7cb` (2026-07-19) + corpus rename `caf386f59c` (2026-08-24); gate `b7cdad6360` (DHF A.3 Deletions, A.11 row 12).
4. **How encoded.** Path-filtered workflow runs the filename check (CSF §5.5).
5. **Evolution.** Doctrine (day-one AGENTS.md) → rename (2026-07-19) → gate (DHF A.11).
6. **Removed/simplified.** All "golden" names from tracked non-vendor files (DHF A.3).
7. **Same problem here?** Inverted — this repo's corpus **deliberately** uses goldens: adjudicated gold labels (promotion path `source-only→candidate→golden→locked`, ESC H6; `adjudication-protocol.md:54-78`) and a permanent golden-negative (eoopt roadmap, "recall 1.0, false_pass 0", ESC S1 evidence; `README.md:42-43`).
8. **Transferable principle.** Fixture naming should make the fixture's *role* (behavior-describing vs truth-asserting) legible, and the role distinction should be enforced where it matters.
9. **Must NOT copy.** The filename ban — it would fight the corpus design (adjudicated gold is the point of the DQE machinery); take only the meta-lesson (a doctrine worth keeping gets a cheap mechanical name) if naming drift appears.

## M18 — Frozen sealed archive for low-value implemented notes

1. **Observed mechanism.** `archived/{kind}/` triplets: only implemented notes archive; only permitted edit = `Archived: YYYY-MM-DD` line + sidecar re-record + inbound-link repair; permanently frozen, sealed by path + SHA-256 in an append-only manifest (`verify-archived-agent-notes`, `--write` proves all existing seals match); `.rgignore` excludes the archive from search; all evolving doc gates exclude archive sources (CSF §3.2, §10 M18; `2026-07-26-frozen-agent-note-archive.md:19-21`).
2. **Problem it solved.** Active corpus maintenance cost grows with records that no longer guide; search noise from stale facts (CSF §10 M18).
3. **Historical evidence it mattered.** `37140bf823` (2026-07-26) — the archive landed the same day as universal triplets, when the note corpus already outgrew active-tree search (171 archived triplets at HEAD; 126 of them TUI-related, CSF §11.2).
4. **How encoded.** Semantic judgment (dsh-archive-agent-notes skill, calibrated examples 248–1,498 words) owns classification; the verifier owns the frozen boundary ("stated split", `2026-07-26-frozen-agent-note-archive.md`) (CSF §3.2; DHF A.8.10).
5. **Evolution.** No archival → freeze + manifest (2026-07-26); CI fetch-depth 2 + `DSH_ARCHIVE_BASE_REF` so the standby lane compares against the frozen baseline (`d606ab6877`) (DHF A.8, A.2).
6. **Removed/simplified.** 126 TUI triplets relocated (not edited) with the TUI removal (CSF §11.2) — the freeze made a mass relocation safe.
7. **Same problem here?** Yes — superseded material accumulates in the *active* tree: VOID roadmap still tracked + referenced (ESC G2), 8 superseded plans in `docs/plans/archived/` (git-ignored), 18 dated reports committed as living docs, candidate-doc-set already drifting from its originals (ESC §4 problem 7, 12; PPE P5, P9).
8. **Transferable principle.** Archive = frozen history: only *settled* (implemented/decided) records move; the move is a relocation with link repair, never an edit; evolving standards must exclude archived material or they force edits to history; supersession happens at creation, not at cleanup (M19).
9. **Must NOT copy.** Content-hash sealing + append-only manifest + CI full-history baseline — designed for 852 trilingual notes; for a ~14-skill repo, `docs/plans/archived/` + a no-edit convention + supersession links carry the same value at a fraction of the machinery (charter §0: prefer the smaller abstraction).

## M19 — Supersession-on-creation rule

1. **Observed mechanism.** "Every new Agent Note triggers a supersession check" — scoped audit of active notes at authoring time; classify full/partial; consolidate or archive qualifying triplets **in the same PR**; partial supersession keeps both cross-linked (CSF §3.2, §10 M19; `.agents/notes/AGENTS.md:5`; `6241eb6044` 2026-07-27).
2. **Problem it solved.** Replacement notes leave redundant active authorities behind (CSF §10 M19).
3. **Historical evidence it mattered.** Consolidation rule first landed 2026-07-25 (`45034edd1a` + `5feb05fef8` — first consolidations); the supersession check became a standing rule 2026-07-27 (`6241eb6044`) after the corpus grew enough that stale active notes were a retrieval hazard (DHF A.8.8–10).
4. **How encoded.** Prose rule in README + notes/AGENTS.md + the `dsh-archive-agent-notes` skill workflow; **explicitly no gate** — "No automated gate attempts to classify" (CSF §3.2; `b1b57a0ac5`).
5. **Evolution.** Supersedes clause → consolidation rule (2026-07-25) → supersession check on every new note (2026-07-27) (DHF A.10 supersession-machinery line).
6. **Removed/simplified.** Fully-superseded notes consolidated into successors and deleted (`5feb05fef8`) (CSF §3.2).
7. **Same problem here?** Yes — P4: ADR-DQE-001's OQ-REPRO=A rationale falsified by the canary but **never annotated**; D-17 status split across 4 files (OPEN vs scope-out); P5: two DECIDED quality reports for the same target with neither DEPRECATED; VOID roadmap still referenced (ESC G2; PPE P4d, P5). The supersession step is the exact missing link.
8. **Transferable principle.** Creation of a new decision/record triggers the search for what it supersedes; the supersede and the retire land in the **same change**; reversal is by cross-linked supersession, never silent rewrite (charter §8.5).
9. **Must NOT copy.** Nothing structural — it is a prose rule with zero infrastructure; do not add a gate (DSH explicitly rejected one, `b1b57a0ac5:37`); the research version must also cover *evidence* supersession (a new result supersedes an E-level claim), which DSH's note-only rule does not address.

## M20 — Skill self-maintenance loop (private periodic tool + operator + two-adapter consensus)

1. **Observed mechanism.** `dsh-code-review` kept current by a single designated operator running a private periodic tool: selects merged PRs in a 2-UTC-day window, collects pre-merge human feedback with commit anchors, classifies adopted items against the current skill via two independently configured reviewer adapters, drafts a revised SKILL.md, loops until both adapters approve, operator Discard/Batch/Promotes (draft PR, evidence URLs) (CSF §2.2, §10 M20; `docs/cookbook/maintaining-dsh-code-review.md:61-62`).
2. **Problem it solved.** Review skill drifts from actual PR review practice (CSF §10 M20).
3. **Historical evidence it mattered.** Proposed note `2026-07-13-human-review-skill-maintenance.md` (still proposed at HEAD); observed run 2026-07-15: 62 PRs, 426 human feedback items, **0 candidates** — the loop is designed to mostly no-op (DHF A.12).
4. **How encoded.** Prose workflow + out-of-repo private infrastructure (tool source/adapters/credentials private by design); spec lives in the note tree (CSF §2.2).
5. **Evolution.** Still parked in `proposed/` — not built, not archived (CSF §2.2; DHF A.13 "parked").
6. **Removed/simplified.** Nothing (not yet built).
7. **Same problem here?** The drift exists (ESC D3: SKILL.md:47 stale vs Sprint 6B; D14: SWR lists a built skill as "not built"; G1: stale registry notes) but is caught by dogfooding — the system ran its own atoms over its own governance corpus and found the defects (PPE P5: "caught by the system's own agent"); there is no human-PR-feedback source to harvest (18 commits, single user).
8. **Transferable principle.** A judgment-bearing skill should have a named, periodic re-grounding against real usage evidence; drift is a measured failure mode, not an anecdote.
9. **Must NOT copy.** The private tool + two-adapter consensus + operator ceremony — out-of-repo infrastructure by design (CSF §2.2) that a solo research repo cannot staff. Needed instead (possibly nothing new): the already-demonstrated dogfood audit (PSR over the governance corpus, batch-2.5 style) made *periodic*, plus the M12 tier table so stale claims have a named home to be stale in.

## M21 — Stacked-PR-native landing (official GitHub stack object, `gh stack merge`)

1. **Observed mechanism.** Every same-repo chain of ≥2 dependent PRs must use GitHub's official stack object before landing; `PullRequest.stack`/`stackEntry.position` GraphQL is the membership authority (not base-branch inference); same-author unstacked chains auto-linked bottom-to-top; `gh stack merge <stack> --yes --merge` all-or-nothing; hard-stops on cross-fork/missing support (CSF §8, §10 M21; `2026-08-02-native-github-stacks-and-optional-rebases.md:7-9`).
2. **Problem it solved.** Branch-base chains lack stack identity — no atomic landing, no trunk rules per layer, no retarget ownership (CSF §8 item 2).
3. **Historical evidence it mattered.** Ownership decision note `2026-08-02-native-github-stacks-and-optional-rebases.md`; stacked-PR orchestration first captured 2026-06-21 (`a96b1e3ae7`) (DHF A.1 context; CSF §8).
4. **How encoded.** `dsh-merging-stacked-prs` skill (executable checklist) + stack cookbook + standing order `AGENTS.md:131` (lease rules); authority lives in GitHub server state, not repo tooling (CSF §8 items 1–3, §10 M21).
5. **Evolution.** Branch-base chains → native stack object (2026-08-02); base-branch inference demoted from authority (CSF §8).
6. **Removed/simplified.** Base-branch inference as membership authority; no repo-side mechanical stack tooling ever built (CSF §8 item 6 "What is NOT done").
7. **Same problem here?** No — single repo, 18 commits, no PR stacks; parallel work is subagents, not branches (ESC; PPE P8 subagent runs). Research alternatives are not implementation dependencies at all (charter §1 mission 3).
8. **Transferable principle** (charter §7 example). "DSH PR stacks solve implementation dependency; research alternatives are not automatically PR stacks." If stacked branches ever appear: membership authority lives in the server object, never in branch-name or base inference; land all-or-nothing.
9. **Must NOT copy.** The `gh stack` procedure, GraphQL checks, auto-linking — no PR workflow exists here; building stack machinery now is governance without a failure mode (charter §18).

## M22 — One worktree per PR branch + per-worktree hook install

1. **Observed mechanism.** Stack cookbook ground rule: **one worktree per PR branch** ("parallel fixes never share a checkout", line 9); fix lands on the PR that *introduced* the issue, then flows up-stack; delegated-fix trust-but-verify: "a sub-agent's report describes intent, not necessarily what landed… for a regression guard, prove it FAILS on the unfixed code" (line 22); worktree-local lefthook installer so parallel worktrees carry their own hooks (CSF §8 item 4, §7.3, §10 M22; `2026-07-27-worktree-local-lefthook.md`).
2. **Problem it solved.** Shared checkouts break parallel stack fixes; shared hooks cross-contaminate worktrees (CSF §10 M22).
3. **Historical evidence it mattered.** Every `pnpm install` in a linked worktree previously rewrote shared hooks (absolute binary path from the installing worktree) → the installer (format-1 upgrade, per-worktree `core.hooksPath`, ownership markers, rollback) (`2026-07-27-worktree-local-lefthook.md`) (CSF §7.3).
4. **How encoded.** Cookbook prose + machine installer; triage-verify-map-propagate review procedure (CSF §8 item 4; §7.3).
5. **Evolution.** Shared hooks → worktree-local (2026-07-27) (CSF §7.3).
6. **Removed/simplified.** The shared hook path (each worktree now owns `$GIT_DIR/dsh-hooks`) (CSF §7.3).
7. **Same problem here?** Partially — no worktree practice (single checkout; subagents share the workspace), so the *hook-plumbing* half is absent; but the **trust-but-verify** half is live: P8's no-skill subagent "decided D-1 by fiat" and a subagent's self-report is exactly the "intent, not what landed" surface (PPE P8; charter §8.3 "agent self-report with external evidence").
8. **Transferable principle.** Parallel fixes get isolated working state; the fix attaches to the introducing unit; delegated output is verified against the artifact, never the report (external evidence over self-report, charter §8.7).
9. **Must NOT copy.** The lefthook installer + worktree hook path (no hooks exist here, M5); "one worktree per branch" is a git-branch workflow that this repo's subagent-parallel model does not use — adopt the trust-but-verify rule into multi-agent execution contracts (charter §16.6–8) instead of the checkout topology.

## M23 — Test-reliability skill (topology model, atomic allocation, no-masking) + flake diagnosis reference

1. **Observed mechanism.** `dsh-ci-test-reliability`: 4-layer execution topology (file→worker→gate process→shared host); atomic resource allocation (`listen(0)`, `mkdtemp`, unique namespaces); exact capture/restore of process-global state; quiescent teardown; "Do not hide the failure in a snapshot normalizer, retry wrapper, broader timeout, global serialization setting, or weaker assertion" (`references/ci-flake-diagnosis.md:46`); 8-class failure taxonomy + smallest-topology reproduction ladder (CSF §2.1, §10 M23).
2. **Problem it solved.** Probabilistic failures under real CI concurrency; "passes alone" specs; failure classes the repo actually paid for (CSF §10 M23).
3. **Historical evidence it mattered.** ~19 verified flake-fix commits: fixed sleep → poll (`a72ebda723`); "failures rotate across cases as load shifts, so per-case widening only moved the flake" → lane-level 90s budgets (`84692044af`); "make windows coverage timing assertions deterministic" — 40 ms fixed settle → `vi.waitFor` on the observable outcome (`0868e5d128`); two skill rules born from paid failures (`2026-08-28-ci-test-reliability-skill.md:19`) (DHF A.5).
4. **How encoded.** Prose skill (advisory) + read-only diagnosis reference; **no** flaky registry/marker/regex gate ever introduced — the note explicitly rejected "a generic stress runner or regex gate immediately" (`2026-08-28-ci-test-reliability-skill.md:35`) (DHF A.5; CSF §9, §11.10).
5. **Evolution.** Ad-hoc July fixes → doctrine in `docs/testing.md` ("a spec that passes only when it runs alone is a defect in the spec") → skill `94c714d813` (2026-08-28) → platform/budget extension `596a13d1cb` (2026-08-29) (DHF A.5; CSF §9).
6. **Removed/simplified.** Rejected: generic stress runner, regex flake gate, flaky registry, broad textual policy (all recorded rejections); per-case `MULTI_PROCESS_TEST_TIMEOUT_MS` constant deleted in favor of lane budgets (`90505636cd`) (DHF A.5; CSF §11.10).
7. **Same problem here?** Yes — P6 (recurring harness false-negatives: 3 checker precision bugs, hardcoded doc-path ran with `files_checked=0`); P1 (workflow serialized `args` → per-character fan-out); canary found every LLM-judged signal unstable while deterministic checkers were stable (PPE P2 unresolved). The masking temptation is live: DQE's `warnings()` hook that "never affects hard_fail/exit code" and the SIGNAL tier that "never auto-block" (ESC P5, P6) are the research analog of "hiding the failure in a weaker assertion."
8. **Transferable principle.** Fix at the owner, never mask (blacklist: generic retry, timeout without named awaited state, swallowed errors, weakened assertions, normalizing away instability); reproduce at the smallest topology that shows the failure; prove the guardrail fails on the unfixed system; a later high-signal defect class can justify a narrow executed check (record the rejection, don't pre-build).
9. **Must NOT copy.** The 4-layer CI topology model and DSH's port/path/platform rules (tuned to shared Linux runners); the research analog's topology is workflow→slot→agent and its "shared host" is the LLM's run-to-run variance — the doctrine transfers, the inventory does not.

## M24 — Real-API e2e key gating with honest self-skip (preflight fails on missing secret; retry 2)

1. **Observed mechanism.** `test:e2e` key-gated real-API suites self-skip without their key so keyless CI stays green, **but** preflight hard-fails if the secret is missing "so a self-skipping suite can't report false green"; bounded `retry: 2` where the external provider is the nondeterminism source; `pull_request` (not `pull_request_target`) so fork code runs without secrets (CSF §5.3, §10 M24; `e2e.yml:15-18,63-65`).
2. **Problem it solved.** External provider nondeterminism + keyless fork CI (CSF §10 M24).
3. **Historical evidence it mattered.** `2026-06-19-real-api-e2e-ci.md`; the only generic retry in the repo originated `ab19fed77c` (2026-06-13, "one retry for transient flakes"), scoped to this lane; snapshot lane explicitly retry-free (DHF A.5 Machinery).
4. **How encoded.** Security model documented in workflow comments; self-skip + preflight pair is the honesty mechanism (CSF §5.3).
5. **Evolution.** Key gating + retry (2026-06) → preflight secret check (DHF A.5).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** Yes — L3 research skills call external services (WoS API, MinerU cloud OCR, Zotero, scansci-pdf's 13+ download sources) and heavy optional backends are pulled by default skill configuration (DHF B.3.11 analog); `preflight.py` (read-only exit 0/1/2) already exists as the gate carrier (ESC G6); P10 shows pin/provenance gaps for exactly this external-dependency surface.
8. **Transferable principle.** External-dependent checks self-skip on missing credentials, **but missing credential is itself a loud failure** (honest self-skip); retry is bounded and allowed only where the external provider is the nondeterminism source; the security model (what may run with secrets) is documented where the run happens.
9. **Must NOT copy.** The `e2e.yml` lane design and fork/Dependabot skip logic; adapt to skill preflight — list external dependencies per skill, check credentials before the run, and fail (not skip-green) when absent.

## M25 — Sandbox kernel-proof lanes with self-skip run-guards

1. **Observed mechanism.** `sandbox.yml` (master-only, outside PR verdict): keyless real-kernel confinement proofs fanned over OS×runner (bwrap / landlock x86 / landlock arm / seatbelt); each leg greps `Test Files 2 passed (2)` so "a self-skip on the very platform that exists to prove it is a failure, not a pass"; Landlock legs also run a packed-distribution rehearsal (CSF §5.4, §10 M25; `sandbox.yml:39-41,104-113`).
2. **Problem it solved.** "A leg that lost its runner would otherwise pass as a false green" (CSF §10 M25).
3. **Historical evidence it mattered.** Postmortem 0004 (`6343d8f6e6`): shared `landlock-run:` stderr prefix + any nonzero exit misattributed to sandbox failure; broad signature rules + missing partial-ABI composition coverage let it through (CSF §4.4).
4. **How encoded.** Per-leg pass-summary grep + `RunnerFailureRule` with status-gated fatal evidence + `partial-landlock` snapshot pinning the product path (CSF §4.4, §5.4).
5. **Evolution.** Postmortem 0004 → guardrails (rule + native-boundary cases + snapshot composition) (CSF §4.4).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** No — no sandbox product exists; the closest analog, `smoke_test.py` clean-room (planted state-contradiction + safety-negative, actual PASS run recorded), already embodies the "proving platform can't self-skip" idea for release (ESC G6).
8. **Transferable principle.** A proof lane's self-skip is a failure on the platform it exists to prove; grep the pass summary, don't trust exit codes.
9. **Must NOT copy.** The bwrap/landlock/seatbelt matrix and pack→install→confine rehearsal — they prove a product that the project does not ship.

## M26 — GUI-PR GIF evidence chain (real server, real model, recorded commit, assets branch)

1. **Observed mechanism.** `record-browser-gif` + deterministic `scripts/encode_gif.py`; record the worktree's exact commit, build that tree, fresh scratch `DSH_HOME`/workspace/session per server, one storyboard = one evidence run; standing rule: **every product-user-visible GUI PR must include one** (CSF §2 row 11, §8 item 5, §10 M26; `record-browser-gif/SKILL.md:27-32`).
2. **Problem it solved.** PR bodies claim GUI changes reviewers can't verify; fixtures misattribute evidence (CSF §10 M26).
3. **Historical evidence it mattered.** Postmortem 0003 (`cd88a339fa`): a Web agent validated a *replacement* server instead of the GUI hosting its session — bare Vite HTTP 200 treated as success; evidence cited from the persisted session event log with sequence numbers (CSF §4.4); `2026-08-08-browser-gif-evidence-chain.md` (CSF §10 M26).
4. **How encoded.** Skill + shipped encoder + per-worktree recording discipline (CSF §8 item 5).
5. **Evolution.** Evidence chain formalized 2026-08-08 (note date) (CSF §10 M26).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** The claim-verification problem exists (DQE's whole purpose; P8: baseline agent's self-made decisions), but the *carrier* differs — there is no GUI; evidence for a change here = eval outputs, corpus artifacts, dated reports, which are already required (ESC H6; PPE P8).
8. **Transferable principle.** A user-visible claim needs captured evidence produced from the **exact commit** that made the claim (not a fixture, not a parallel server); the evidence is part of the change, not the PR body.
9. **Must NOT copy.** The GIF + assets-branch pipeline (no GUI to record); the research analog already exists (corpus + blind-run JSON + reports) — the only missing piece is P10's provenance fix: evidence files tracked at a pinned commit.

## M27 — Model-visible ⟺ logged doctrine + snapshot-required rule

1. **Observed mechanism.** Standing order: anything model-visible is logged (`AGENTS.md:110,127`); "every non-trivial model- or product-user-visible change adds/updates a keyless recorded-session scenario in the same PR"; both SDKs project the loop in the same PR (CSF §4.2, §10 M27; `docs/testing.md:52-54`).
2. **Problem it solved.** Model-facing behavior invisible to tests; transcript claims not verifiable (CSF §10 M27).
3. **Historical evidence it mattered.** Postmortem 0001 (unit tests hand-mounted the plugin — the load path was invisible); the snapshot-required obligation codified `f09cc81c03` (2026-06-19) (DHF A.3, A.4).
4. **How encoded.** Snapshot tier (M8) + standing order + "record vs refresh" discipline; CI forces replay (CSF §4.2, §7.1).
5. **Evolution.** 2026-08-24 corpus migration: scenarios launch shipped profiles through `dsh` (no hidden entrypoints) (DHF A.3; `snapshots/AGENTS.md`).
6. **Removed/simplified.** ACP-as-universal-controller (2026-08-24) (DHF A.3).
7. **Same problem here?** Partially — the doctrine's analog ("what the evaluator sees must be a persisted, checkable surface") is already partly practiced: flow-state `corpus_content_hash` (`final-flow-state.md:57`), blind-run result JSONs, corpus seed SHA-256 pins (ESC H6; PPE P10) — but P10 shows the persisted surface is partly git-untracked and one preservation claim is false.
8. **Transferable principle.** The model's (evaluator's) input/output surface is a test surface: record it, don't infer it; a visible-behavior change updates its evidence in the same change.
9. **Must NOT copy.** The event-sourced session core and its snapshot manifests (DSH-specific, CSF §10 M27); here the fix is closing the P10 tracking gap (track the frozen bundles + upstream pins), not adding a new logging doctrine.

## M28 — Package README contract (kind→template, Model Experience, Known Limitations, Dev Note)

1. **Observed mechanism.** Frontmatter `kind` from a 4-label set maps 1:1 to a README template; canonical section sequence (Summary → TOC → Use this package → Understand the implementation → Further Exploration → **Model Experience** → **Known Limitations and Deferred Work** → Dev Note); the docs check derives the expected kind from mechanical facts; Model Experience + Known Limitations are gated; Dev Note = "the only slop zone" (CSF §4.5, §10 M28; `dsh-doc/SKILL.md:49-58,60-68`).
2. **Problem it solved.** Package docs drift into enumeration/identity narration; model-context effects undocumented (CSF §10 M28).
3. **Historical evidence it mattered.** Cookbook `adding-a-package.md` §4 + `dsh-doc` templates; gates `verify-package-readme-model-experience` / `verify-package-readme-limitations` in doc-quick; subsystem-ownership gate `9d37d7155a` (2026-08-09) + `4ba47e665b` (2026-08-23) (DHF A.7; CSF §4.5, §6.2).
4. **How encoded.** Section-sequence convention + 2 structure gates + kind derivation; reference example `packages/session/session-persistence-jsonl/README.md` (CSF §4.5.6).
5. **Evolution.** `dsh-doc` rebuilt to own the standard `0b5eba0c8d` (2026-08-25), absorbing `dsh-doc-standards` (DHF A.7, B.6).
6. **Removed/simplified.** `dsh-doc-standards` skill (56 lines) absorbed into `dsh-doc` (128 + references + templates) (DHF B.6).
7. **Same problem here?** Yes — 14 heterogeneous SKILL.md files with no canonical section sequence; per-skill `last_verified` HTML-comment headers drift (PPE P9); repo-level `KNOWN_LIMITATIONS.md` is the only honest-limitations surface, and skill-level limitations live in scattered `KNOWN_LIMITATIONS.md` fragments (ESC S13/S14 evidence). Charter §11 already mandates a skill schema for the portfolio review.
8. **Transferable principle.** A documented unit has a canonical section sequence; gated *honest* sections (Known Limitations: durable consumer gaps only, or an explicit allowlist entry); the doc check derives expected structure from mechanical facts, not from the author's claim.
9. **Must NOT copy.** The Model Experience section (token/KV effects — DSH product-specific, CSF §10 M28); the 4-kind template set — if the charter §11 skill schema lands, the research-native kind set (L1 control / L2 atomic / evaluator) maps onto the same template machinery.

## M29 — Invariant-companion rule (publish `./invariant` only for diverging observations)

1. **Observed mechanism.** `packages/AGENTS.md:19`: publish `./invariant` only for diverging observations; gate rejects empty companions; 209 explained-empty companions + a synthetic probe deleted, 39 real checks remain; omission documented per package README and enforced by `verify-package-invariants` (CSF §10 M29; `2026-08-28-omit-unneeded-invariant-companions.md`; DHF B.5.8).
2. **Problem it solved.** Empty/invented invariant checks became ceremony (CSF §10 M29).
3. **Historical evidence it mattered.** The 209-companion deletion itself is the evidence: a universal "every unit asserts a negative" policy produced explained-empty files (DHF B.5.8; A.10 pattern 1).
4. **How encoded.** Rule + gate that rejects empties + per-package omission documentation (CSF §10 M29 enforcement: mixed).
5. **Evolution.** Universal companion requirement → "independent observations" requirement (2026-08-28); shipped configs mount no invariants (2026-08-03, dev/test-only) (DHF B.5.7).
6. **Removed/simplified.** 209 empty companions + synthetic probe; invariants-from-shipped-config (DHF B.5.7–8).
7. **Same problem here?** Yes, in miniature — per-skill "MUST NOT" lists and registry `conflicts` fields are the declaration surface; DHF B.5(d) names the candidate directly: per-skill/flow "declares no-X" sections that are empty for most skills (e.g. the frozen-interface `KNOWN_NON_FROZEN` exclusion, ESC H5) — universal declaration, sparse substance.
8. **Transferable principle.** A policy that forces every unit to publish an artifact asserting a negative produces explained-empty files; require declaration only where independent observations exist, and mechanically check what *is* declared.
9. **Must NOT copy.** The Cordis `./invariant` export itself (CSF §10 M29 "DSH-specific (Cordis invariants)"); the research application is a design rule for the skill schema (charter §11), not a new mechanism.

## M30 — COT-leakage prose standard (8-class taxonomy, keep-rules, recall batteries)

1. **Observed mechanism.** `dsh-prose-standard` (complete-proposition preservation; required prose coverage across Markdown/JSDoc/comments/prompts/strings) + `dsh-trim-cot-leakage` (8-class taxonomy of reasoning-transcript leakage: dead session citations, stack/PR vantage, change narration, review choreography, hedges; keep rules; recall batteries as probes, not gates) (CSF §2 rows 10, §10 M30; `dsh-trim-cot-leakage/SKILL.md:42`).
2. **Problem it solved.** Agent-authored prose carries session vantage (dead citations, "used to", reviewer choreography) that rots (CSF §10 M30).
3. **Historical evidence it mattered.** `2026-08-09-committed-artifact-citations.md`; "make technical prose concrete" tightening `a27efdef36` (2026-08-09) (DHF A.8.11).
4. **How encoded.** Prose standing order (`AGENTS.md:144`) + two skills; batteries are recall probes, explicitly not gates (CSF §10 M30 enforcement: prose).
5. **Evolution.** Committed-artifact-citations rule (2026-08-09) → trim skill (CSF §10 M30).
6. **Removed/simplified.** Nothing.
7. **Same problem here?** Yes — every governance doc is agent-authored and session-vantage has already rotted: SKILL.md:27-28 "v0 SKELETON STOPS HERE" one day stale (ESC D3); runlog "logged-retroactively" batch entries (PPE P9); phantom `wrote=[… memory]` lines with no artifact home (PPE P9; ownership map §2.3); "last_verified" headers that duplicate git (ESC §4 problem 10).
8. **Transferable principle.** Repo prose is a set of current-state facts, not a session transcript: dead references and session vantage are a defect class; prose quality stays advisory (skill), reference validity is mechanical (checker).
9. **Must NOT copy.** The 8-class COT taxonomy tuned for code comments/JSDoc/prompts; a standalone trim skill — here the subset (stale-claim/dead-reference detection) belongs to the documentation skill and a stale-reference checker, not a new skill (charter §10: don't create a Skill to restate a check).

## M31 — Simplification-audit skill (consumer classification, protected seams, note coalescence)

1. **Observed mechanism.** `dsh-find-simplifications`: starts from repo context; declares protected designs; defines strong vs thin candidates (no production consumer; only tests/docs consume; mirrored facts; seams with unused methods; speculative generality; hand-rolled vs maintained dependency, `SKILL.md:17-31`); mandates consumer classification (production vs non-production vs ambiguous corpus, lines 75-83); superseded-note coalescence; Agent Note output, not direct deletion; "prefer a few well-proven candidates over a pile of thin guesses" (CSF §2.1, §10 M31; DHF A.12).
2. **Problem it solved.** Surface area accretes; simplification ideas scattered and unproven (CSF §10 M31).
3. **Historical evidence it mattered.** ~60 implemented + ~25 archived simplification notes produced by this discipline (DHF A.10); the NIH audit proposed ~30 dependency swaps and **all were rejected with recorded evidence** (`2026-07-26-dependency-swaps-rejected-by-nih-audit.md`) — a full audit can end in "delete nothing" (DHF A.10, B.4).
4. **How encoded.** Skill with internal evidence standards; calls `dsh-archive-agent-notes`; protected-seam declaration in the skill body (`SKILL.md:15`) (CSF §2.1).
5. **Evolution.** The skill is the standing entry point for the repo-maintenance workflow; its own rejections are recorded notes (DHF A.12 "follow the code, keep judgment active").
6. **Removed/simplified.** Whatever the audits found (TUI, 209 companions, knip, stdio/echo agents — see §C).
7. **Same problem here?** Yes — charter §12.2 names this adaptation explicitly. Targets already inventoried: orphaned `register_check.py` (ESC H2), VOID-but-tracked roadmap + runlog chronology (ESC G2/G3), 4 owners of "canonical source" (ESC §4 problem 1), duplicated governance boilerplate across 14 skill folders (DHF B.3.8 analog), D1–D14 discrepancy set (ESC §5).
8. **Transferable principle.** Simplification = evidence-backed candidates only: consumer classification first (a test-only consumer is not a consumer); protected seams declared up front; strong-vs-thin candidate bar; the audit writes decision notes, not diffs; recorded rejections prevent re-auditing.
9. **Must NOT copy.** DSH's protected-seam list (dual LLM adapters, JSONL persistence seam) and the note-tree output mechanics; the research target list is charter §12.2's (orphan scripts, stale notebooks, duplicated pipelines, multiple implementations of one algorithm, non-reproducible result artifacts, obsolete config paths, prototypes-as-dependencies, abandoned branches, speculative abstractions, tests/docs as the only consumers of obsolete behavior).

## M32 — Trusted-branch policy checkout + least-privilege App token

1. **Observed mechanism.** `issue-lifecycle.yml:44-62`: workflows check out the **trusted default-branch policy** (not the PR head) and mint a write-capable App token only on `changes_requested` reviews (CSF §6.4, §10 M32).
2. **Problem it solved.** PR head can't be trusted to mutate board/labels; token over-minting (CSF §10 M32).
3. **Historical evidence it mattered.** Part of the issue-management rollout (2026-08-08 label-taxonomy era); the trust model was written into the standby-runbook variable-trust discussion (`d606ab6877`) (CSF §6.4; DHF A.2).
4. **How encoded.** Workflow checkout + conditional token mint (CSF §6.4).
5. **Evolution.** Single design; no churn recorded.
6. **Removed/simplified.** Nothing.
7. **Same problem here?** No — no GitHub App, no PR-head-vs-default trust boundary at 18 commits / local single-author workflow (ESC; disk check: no `.github/` at root).
8. **Transferable principle.** Run policy from the trusted branch, never from the change under review; mint credentials at minimum scope for the exact operation.
9. **Must NOT copy.** The GitHub App plumbing entirely — no analog exists here; if remote review ever appears, the principle (policy from trusted branch) transfers before the machinery does.

---

## C. Merged negative-evidence summary (charter §6)

Deletions/simplifications that survived the audit, each with the charter §6 four answers. Sources: DHF Part B (B.1–B.6), CSF §11; the project's candidates from DHF B.7 cross-checked against ESC/PPE.

| # | Removed/simplified | (1) Why it seemed useful | (2) Evidence it cost more than it bought | (3) What replaced it | (4) Same pattern here? |
|---|---|---|---|---|---|
| C1 | knip dead-code gate (`6796a36cc4`→`907c6334c1`, 2026-08-19) | Automatic unused-file/export/dependency detection | Needed per-workspace entry lists + ignore exceptions = "a second approximation of the executable graph"; generic result stayed advisory (DHF B.2.1) | No repo-wide static unused-code check; removals justified from call sites + manifests + generated artifacts + Loader paths | **Strongest transfer** (DHF B.7.1): any check needing a per-skill exception inventory to tolerate how the system actually loads — audit DQE rules that need per-skill carve-outs for orchestrator-invoked skills; "the exceptions are the cost" |
| C2 | `check:pre-push` aggregate + heavy hooks (`31c0589439`, 2026-07-22) | Full local rehearsal before every push | Delayed pushes, amplified unrelated flakes, duplicated CI; agents already run the tests (DHF A.1) | 3-way split: cheap hooks / agent-selected evidence / exhaustive CI (M5, M9) | Partial — inverse: here there are no local checkpoints at all (M5 link 7); the anti-pattern to avoid is recreating the aggregate as "run everything before commit" |
| C3 | TUI package (`1119c537d0`→`10bb9cbf4a`, 2026-08-04; 18-day life) | First interactive surface; TUI snapshots proved terminal state | No shipped composition after the implicit terminal app was removed — product-sized frontend (renderer, adapters, 879-line smoke) for zero deployment (DHF B.1) | Headless profile (non-interactive) + Web (rich UI) | **TUI-pattern** (DHF B.7.2): any of the 14 skills whose only consumer is one L1 flow/orchestrator — trigger-evidence check decides keep/merge/delete; prime suspects: overlapping retrieval skills (`wos-research`/`scansci-pdf`/`paper-fetch-skill`) |
| C4 | `dsh-cli-demo` (`dc57f7d854`, 2026-08-08) | Demo CLI showing one-shot behavior | Assembled a *different* tree than the shipped profile — "didn't prove the shipped profile" (DHF B.1) | Headless profile + test-only `dsh-loader-smoke` | **cli-demo-pattern** (DHF B.7.4): the eval harness must enter the 3 L1 flows through their real entry points, or it is a cli-demo (postmortem-0001 lesson applied to harnesses) |
| C5 | `dsh-repository-plugin` (`993550e6c8`, 2026-08-09) | Second install mechanism for repository-form plugins | Duplicated the profile-bundle install path and exposed LESS configuration — "strictly dominated by the one it duplicated" (DHF B.1) | Installable profile bundles only | Any parallel mechanism strictly dominated by an existing one (e.g. a second decision-register beside UDM's; a second canonical-source table beside `canonical-source-map.md`) |
| C6 | SDK project toolchain, 4 packages (`daf90bda7e`, 2026-08-11) | Developer scaffolding for SDK consumers | Unreleased, no consumers, no public release — 4 packages + templates + adapters "for a nonexistent audience" (DHF B.1) | Runtime SDK moved unchanged | Any skill/atom maintained for an audience that doesn't exist yet (Batch-4/5 planned atoms are honest-BLOCKED — the correct version of this; a *built* atom with no consumer would be the failure) |
| C7 | Mutable session summary (`2026-06-19-drop-mutable-session-summary.md`) | Future session picker (recency, title, preview) | `update()` had **zero production callers**; `firstPrompt` never read; "existed only to be read by its own contract test" (DHF B.3.1) | Metadata = `SessionHeader`; rest derivable from the log | **Direct analog** (DHF B.7.3): any flow-state/registry field read only by its own eval assertion — delete or find the product reader; DSH's generalization: "a passing test pins current behavior, not necessarily correct behavior" |
| C8 | SQLite second authoritative store (`2026-08-30-jsonl-only-session-persistence.md`) | Stronger DB/WAL store + opt-in differential backend | Shipped profiles don't select it; every contract/recovery rule/migration carried a second impl + test matrix (DHF B.3.2) | JSONL sole first-party impl; seam stays backend-neutral | Any second source of truth beside flow-state + git (e.g. a separately-maintained registry JSON duplicating what flow files + git already say) (DHF B.3.2d) |
| C9 | ACP editor-bridge UI (`2026-07-23-acp-automation-only-protocol.md`) | Zed-style editor UI translating durable events | A *second* interactive UI duplicating TUI + Web; "even a coherent service-bounded bridge couldn't make editor cards belong in an automation protocol" (DHF B.3.4) | Narrow automation transport; TUI + Web own human interaction | Any L1 flow that grew presentation it doesn't own (a research flow that renders its own reports instead of handing off to the writing skill) (DHF B.3.4d) |
| C10 | 209 empty invariant companions (`2026-08-28-omit-unneeded-invariant-companions.md`) | Universal "every package asserts its invariants" completeness | 209 explained-empty companions + 1 synthetic probe — ceremony without observations (DHF B.5.8) | Declare only for independent observations; gate checks what *is* declared | Per-skill "declares no-X" sections empty for most skills (M29 link 7) |
| C11 | Generated Agent Note `INDEX.md` (`4779d04af8`, ~1 month old) | Centralized inventory for discovery | "Creates a merge hotspot without providing discovery that tree navigation or search cannot provide" (DHF B.2.6) | The lifecycle/class tree + search; README as curated entry point | Any generated index over skills/flows duplicating tree+search (DHF B.7.6 analog); also: a `docs/plans` INDEX would repeat this failure |
| C12 | `dsh-doc-standards` skill (`0b5eba0c8d`, 2026-08-25) | Separate documentation-standards skill | Overlap with `dsh-doc`; absorb-and-delete rule applied (DHF B.6) | `dsh-doc` + references/templates owns every unique proposition | 14-skill catalog overlap probe (e.g. prose-editor vs readability-auditor vs review-auditor adjacency; WFI↔PSR boundary, ESC S5) — consolidation only when the successor owns every unique proposition |
| C13 | Packed-fixture migrator — **removal proposed 2026-07-26, still unlanded at HEAD** | One-time fixture layout migration | "A documented transition outliving its transition window — even in a repo that deletes aggressively"; trigger condition ("no open PR needs it") is not self-checking (DHF B.6.1) | — (still open) | **Packed-migrator-pattern** (DHF B.7.8): every documented transition whose trigger condition is not self-checking will outlive its window — give each a mechanical closure trigger or a review date (applies to this reconstruction plan's own phased gates) |
| C14 | Tag `legacy-agent-team-pre-vnext` (2026-08-29) — feature branch frozen, not merged | Full Agent-Teams GUI on a side branch | Master deliberately did not merge it; re-derived Agent Teams on its own path (`570aff0e27`→`42e0781cda`); tag declares "production authority = retired; reference value = retained" (DHF B.6 tag forensics) | Re-derivation on mainline; frozen branch as reference/regression fixture | **Frozen-branch template** (DHF B.7.7): for abandoned flow prototypes in `docs/skill-development/` — freeze, declare authority retired, keep reference value, never develop on the frozen record |
| C15 | Tool swaps: Yarn→pnpm (`dabc2ff411`), dumble→tsdown (`630bbddf9a`), ESLint→Oxlint (`95a995968b`) | Each was the current best option | Ecosystem alignment / phantom-dep safety / linter churn — "the lint stack is not a sacred surface — only the enforced rule set is stable"; one swap honestly "a wash within noise" (DHF B.2.2–4) | The healthier-ecosystem option | Any toolchain dependency (OCR/paper-fetch backend) swapped while the corpus is still small — the pre-release window for cheap swaps (DHF B.2.2d) |

**Rejected simplifications (negative evidence that not every deletion is right).** All 10 live in `rejected/simplification/` because each losing proposal "remains a tempting, meaningful mistake" (DHF B.4). The rejections cluster around four guards: (1) the durable log is the replay tape — shrinkage bounded by replay needs; (2) crash-recovery semantics can depend on "ceremonial" structure; (3) seams are kept even with one backend if the split is the clean boundary; (4) testability (fake-clock determinism) can beat deletion volume — e.g. the `node:timers/promises` swap was rejected because the PR **falsified the parity premise** (vitest fake clock doesn't intercept it). Each rejection was proven against a named consumer or invariant; "a full evidence-driven audit can end in 'delete nothing'" (NIH audit, DHF B.4). For the project: the frozen 12-field interface and the corpus policy are the local analogs of "seams kept despite looking premature" — do not simplify them on instinct (M4 link 8: keep the seam, delete the second implementation).

**Deliberately NOT built** (CSF §11.10): a `superseded/` lifecycle folder; a CI diff-classification gate for note-required changes; a generic stress runner or regex flake gate. Value: DSH records *why mechanisms were not built* — the research analog should do the same for every rejected checker/skill in the Phase-1 portfolio (charter §11 `proposed_action: remove`).

**Transfer-candidate roll-up** (DHF B.7, 10 items, verified against ESC/PPE): C1 exception-inventory gates; C3 surface-without-consumer; C7 test-only consumer; C4 harness-doesn't-prove-shipped-path; two-trees-N%-identical boilerplate (B.3.8 → shared governance preamble across the 14 skill folders / 3 flow docs); C10 invariant-companion declarations; C14 frozen-branch template; C13 non-self-checking transition triggers; the Agent-Note maturation sequence (B.7.9: backfill → unify → uniform format → rename → require-for-non-trivial → consolidate → freeze-archive, each gate added *after* a drift incident); and the perf-gate lesson (B.7.10: quality scores are interpreted signals unless a calibrated, deterministic, opt-in harness with a named budget exists — do not gate on host-relative scores; applies to DQE's LLM-judged band, PPE P2).

## D. "DSH keeps both `.claude/` and `.agents/`" — observation and meaning

**Observation (evidence-cited).** DSH's first commit `b67e81ac97` (2026-06-10) is "Initialize repo with README, AGENTS.md, and CLAUDE.md symlink" — the `.claude`/`.agents` dual-platform coexistence is a **day-one design**, not an accumulation (DHF header/history-size line; parent spot-check). At HEAD: `CLAUDE.md` is a symlink of `AGENTS.md` at root and `packages/` with the rule "edit the real file" (`AGENTS.md:150`, CSF §0); the skill catalog lives in `.agents/skills/` (11 skills, CSF §2); `.claude/skills` exists but is **empty in this checkout** — a discovery stub, not a parallel copy (CSF §0; CSF §12 UNKNOWN: "likely a Claude-Code skill-discovery placeholder"). The single tag in the repo (`legacy-agent-team-pre-vnext`, 2026-08-29) is a frozen reference branch, unrelated to platform layout (DHF B.6 tag forensics).

**Meaning for multi-platform layout.**
1. **One canonical instruction file, N platform views.** DSH never maintains two instruction trees: `AGENTS.md` is the single source; `CLAUDE.md` is a symlink. Platform adaptation costs a symlink, not a second copy with its own drift history.
2. **One canonical skill home, per-platform discovery stubs.** Skills are maintained once (`.agents/skills/`); the `.claude/` side exists only so a platform that discovers there can find them — and an *empty* stub is the accepted state when the platform's catalog is served by another mechanism.
3. **Implication for the project.** The repo's 14 skills are currently installed **user-level** in `<user-home>\.claude\skills` (ESC D6 — the workspace-isolation claim contradicted disk), with the workspace `.agents/` tree present at root (verified on disk 2026-09-09). The DSH pattern says: pick **one** canonical skill location (the workspace tree, so the roster is version-controlled and `installed-skills.yaml`/preflight can diff it — ESC A5), and treat the user-level install as a *view* (record copy-hash vs source, as ESC A5 proposes) — never as a second maintenance site. Do **not** create a parallel `.claude/skills` mirror in the repo: that is exactly the duplication the symlink/stub pattern exists to avoid, and it would re-introduce ESC D6's drift with a second tracked copy.
