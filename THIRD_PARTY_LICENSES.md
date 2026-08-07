# Third-Party Licenses & Attribution — Research-Code-Docs v0.1.0-alpha.1

> Generated for the internal-preview release from
> [`references/documentation-methodology/upstream-method-matrix.md`](references/documentation-methodology/upstream-method-matrix.md)
> (the authoritative per-rule provenance) and the vendored `references/*/LICENSE` files.
> Last verified: 2026-08-06 against the vendored license texts.

## 0. Summary for a release reviewer

- **No upstream skill source code is redistributed in this release.** Every in-house
  skill was authored here; upstream projects contributed **methods** (how to structure a
  gate, how to run a reverse-outline reader, how an orchestrator routes) or, in one case,
  **ideas only**.
- The vendored copies under [`references/`](references/) exist for development-time
  attribution and are **excluded from the release archive**
  (`release-manifest.yaml → exclude_from_distribution`).
- **One source carries a NonCommercial restriction** (`academic-research-skills`,
  CC BY-NC 4.0). We use **ideas only** and copy nothing from it, but it is flagged below so
  that any future commercial positioning is reviewed.
- **Two sources have no upstream license file**; they are treated as reference-only and are
  neither redistributed nor relied on for released behavior.

## 1. Attribution matrix

| Upstream project | Borrow type | License | Code copied? | Ideas only? | Non-commercial restriction? | OK to publicly release *our* work? |
|---|---|---|---|---|---|---|
| **mattpocock/skills** | method-borrow / adapt (orchestration, skill structure, interview) | MIT | No | No (methods) | No | Yes — MIT permits it; keep this attribution |
| **addyosmani/agent-skills** | method-borrow / adapt (severity taxonomy, reverse-outline, source/doubt-driven review, context tiers) | MIT | No | No (methods) | No | Yes — MIT; keep attribution |
| **github/awesome-copilot** | method-borrow (codebase-knowledge / Project Map) | MIT (top level) | No | No (methods) | No | Yes — MIT; only MIT top level used |
| **research-paper-writing-skills** | method-borrow (claim/evidence matrix, paper-review) | MIT | No | No (methods) | No | Yes — MIT; keep attribution |
| **academic-research-skills** | **ideas only** (high-level review framing) | **CC BY-NC 4.0** | No | **Yes** | **Yes — NonCommercial** | Ideas-only; **do not** copy text/code; review before any commercial use |
| anthropics/skills | reference-only (read during audit) | none provided upstream | No | Not relied upon | Unknown | Not redistributed |
| pengsida/learning-research | reference-only (read during audit) | none provided upstream | No | Not relied upon | Unknown | Not redistributed |

## 2. License texts (vendored)

Full upstream license texts live next to each vendored copy:

- `references/mattpocock-skills/LICENSE` — MIT
- `references/agent-skills/LICENSE` — MIT
- `references/github-awesome-copilot/LICENSE` — MIT (note: a sub-skill
  `references/github-awesome-copilot/skills/resemble-detect/LICENSE` is Apache-2.0 and was
  **not** used or redistributed)
- `references/research-paper-writing-skills/LICENSE` — MIT
- `references/academic-research-skills/LICENSE` — **CC BY-NC 4.0**

### MIT (applies to the four MIT sources above)

> Permission is hereby granted, free of charge, to any person obtaining a copy of this
> software and associated documentation files (the "Software"), to deal in the Software
> without restriction … THE SOFTWARE IS PROVIDED "AS IS" … (full text in each vendored
> `LICENSE`). Our use is method-borrow, not redistribution of the Software; attribution is
> preserved here and in `NOTICE`.

### CC BY-NC 4.0 (academic-research-skills)

> Creative Commons Attribution-NonCommercial 4.0 International. You may share and adapt
> **for non-commercial purposes** with attribution. We do **not** copy or redistribute this
> work; we use only high-level ideas. Full text:
> `references/academic-research-skills/LICENSE`.

## 3. Redistribution guidance (before any wider release)

1. Keep `LICENSE`, `NOTICE`, and this file together in any archive.
2. Do **not** ship the `references/` tree as part of the product; if you must include any
   upstream verbatim, first re-check that project's license and add its full text here.
3. If the project is ever positioned **commercially**, re-review the `academic-research-skills`
   (CC BY-NC) dependency — confirm that only independently-derived ideas remain and that no
   protected expression was carried over.
4. If you relicense the project itself (e.g., MIT/Apache-2.0), update `LICENSE`,
   `NOTICE`, and `release-manifest.yaml → release.license`; this third-party file is
   unaffected (it governs upstreams, not our code).
