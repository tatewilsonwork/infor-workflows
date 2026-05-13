# Changelog

All notable changes to the **infor-workflows** plugin. The version listed is the plugin version from [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json); every skill's `version:` frontmatter is kept in lock-step with the plugin version (see [CLAUDE.md](CLAUDE.md) → Versioning).

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are YYYY-MM-DD.

## [2.9.0] — 2026-05-13 ([#77](https://github.com/tatewilsonwork/infor-workflows/pull/77))

### Added
- `clone_slide()` and `delete_slide()` helpers in [`infor-workflows/scripts/pptx_helpers.py`](infor-workflows/scripts/pptx_helpers.py) — duplicate a template slide while remapping `r:embed` / `r:link` / `r:id` attributes so pictures, charts, and hyperlinks render correctly in the copy instead of showing red-X placeholders. 5 new unit tests cover the rId rewiring (30 total in `test_pptx_helpers.py`, up from 25).
- `infor-deck-writing/references/` directory — six per-deliverable recipe files (`teaser-recipes.md`, `cim-recipes.md`, `pitch-recipes.md`, `fairness-opinion-recipes.md`, `strategic-review-recipes.md`) plus a cross-cutting `building-blocks.md`. Each loads on demand so a typical drafting request reads ~150–300 lines instead of the previous 787.

### Changed
- `deckcheck-infor` deduplicates the brand-rules block. Step 4 (Formatting Review) and the bottom "Quick Reference Card" now point at [`brand-guidelines-infor/SKILL.md`](infor-workflows/skills/brand-guidelines-infor/SKILL.md) as the source of truth instead of restating colors / fonts / layouts inline. Removes a drift risk: brand changes only need to be edited in one place.
- `brand-guidelines-infor/references/deck-template.md` imports `clone_slide` / `delete_slide` from the shared `pptx_helpers` module instead of carrying its own ~30-line copy of the function.
- Single-version policy bump: plugin 2.8.0 → 2.9.0; every skill's `version:` synced to 2.9.0.

### Removed
- `infor-workflows/skills/infor-deck-writing/slide-type-recipes.md` (787 lines) — split into the six files under `references/` above. Cross-references throughout the plugin updated.

## [2.8.0] — 2026-05-13 ([#76](https://github.com/tatewilsonwork/infor-workflows/pull/76), [#75](https://github.com/tatewilsonwork/infor-workflows/pull/75), [#74](https://github.com/tatewilsonwork/infor-workflows/pull/74))

### Added
- `allowed-tools` array in every skill's frontmatter — the harness now enforces tool restrictions instead of relying on prose `Allowed tools:` lines (#74).
- Repo-root [`CLAUDE.md`](CLAUDE.md) — contributor brief on plugin layout, conventions, version policy, shared helpers, and testing (#74).
- `CHANGELOG.md` (this file) (#74).
- `lbo-model` rewritten to build the LBO workbook from scratch via openpyxl — five standard tabs (Assumptions, Sources & Uses, Operating Model, Debt Schedule, Returns), PE-standard conventions, every calculation an Excel formula. No template required (#75).
- `/<skill-name>` slash command listed in every skill's `description:` so the router fires reliably on the slash form for all 10 skills (#76).

### Changed
- **Single plugin version policy** — every skill's `version:` frontmatter field is now kept in lock-step with the plugin version. Per-skill version drift is no longer allowed. All 10 skills bumped to 2.8.0 (#76).
- All file-producing skills now write outputs to the **current working directory** (`./`). Previously `precedents-infor` wrote to `${REPO_ROOT}/outputs/` and `deckcheck-infor` wrote to a relative `outputs/`. `.gitignore` now ignores `/*.xlsx`, `/*.pptx`, `/*.docx` at the repo root so generated files don't pollute git status (#75).
- `lbo-model` aligned with the other nine skills' style — YAML folded-scalar description, Title-Case section headers, standard "Workflow Steps + Domain Reference" outline (#75).
- README skill table now links each skill name to its `SKILL.md` file. `infor-deck-writing` and `infor-wireframe` rows now show their slash commands (previously dashed) (#76).
- Tightened skill descriptions on `brand-guidelines-infor`, `infor-deck-writing`, `infor-wireframe`, and `deckcheck-infor` (~25–40% shorter each) by removing redundant prose while preserving the trigger phrases the router uses (#74).

### Removed
- Broken references in the old `lbo-model` SKILL.md to `examples/LBO_Model.xlsx` (which never existed in the repo) and the load-bearing dependency on `/mnt/skills/public/xlsx/recalc.py` (#75).

## [2.7.0] — 2026-05-12 ([#73](https://github.com/tatewilsonwork/infor-workflows/pull/73), [#72](https://github.com/tatewilsonwork/infor-workflows/pull/72), [#71](https://github.com/tatewilsonwork/infor-workflows/pull/71))

### Added
- `infor-wireframe` skill — slide-by-slide wireframe for CIM, pitch, fairness opinion, or teaser decks, with per-deliverable wireframe references checked in alongside the skill.
- `infor-workflows/scripts/pptx_helpers.py` — shared python-pptx helpers (`set_text`, `write_bulleted_shape`, `set_cell_text`, `find_shape`, `find_shape_in_group`, `fmt_broker_value`, brand-color constants).
- `infor-workflows/scripts/test_pptx_helpers.py` — 25 unit tests for the helpers, building fresh in-memory decks (no fixture files).
- `infor-workflows/scripts/find_template.sh` — single helper that resolves an INFOR template by filename across all known install paths.
- Per-skill `references/` directories under the four longest skills (`earningsupdate-infor`, `precedents-infor`, `buyerslist-infor`, `brand-guidelines-infor`), loaded on demand via progressive disclosure.

### Changed
- Split the four longest SKILL.md files (`earningsupdate-infor` 885 → 207 lines; `precedents-infor` 571 → 228; `buyerslist-infor` 517 → 188; `brand-guidelines-infor` 502 → 333) — moved deep detail into `references/` while keeping the workflow step-by-step in `SKILL.md`. Total SKILL.md surface dropped from 2,475 to 956 lines (−61%).
- Replaced six per-skill `find ... -name TEMPLATE | head -1` blocks with a single-line call to the shared template-finder script. Future install-path changes are a one-script edit.
- `earningsupdate-infor` driver code now imports from `pptx_helpers` instead of redefining the helpers inline.
- README now lists `earningsupdate-infor` in the skill table and usage examples (previously missing).
- `brand-guidelines-infor` v2.1.0 cross-links to `infor-deck-writing` for all on-slide-text guidance; this skill governs visuals only.

## [2.5.0] — 2026-05-12

### Added
- `infor-deck-writing` skill — INFOR voice, slide-ready text, per-slide-type recipes (executive summary, investment highlights, market overview, valuation commentary, fairness-opinion language, etc.) calibrated from a corpus of CIMs, pitches, teasers, and fairness opinions.

## [2.4.0] — 2026-05-06

### Changed
- `precedents-infor`: single-source cell comments now use the `Quote: "..."` / `Source: ...` two-block format (Format A). Multi-stub comments retain the three-line `<Period> ($<Value>): <URL>` format (Format B).

## [2.3.0] — 2026-05-06

### Added
- `precedents-infor`: when a deal source quotes a multiple (e.g., `12.5x LTM EBITDA`) but not the absolute figure, the skill now derives Revenue/EBITDA in-cell as `=I{row}/multiple`. Required when available — supersedes the filings-stub fallback.

## [2.2.0] — 2026-05-06

### Changed
- `precedents-infor`: disclosed LTM figures in deal sources are now strongly preferred over filings-derived stub calcs (rung 1 > rung 3). Empty rows are trimmed before save so the table flows directly into the averages row.

## [2.1.0] — 2026-05-05

### Added
- `precedents-infor`: required LTM stub-period formulas (`=(MRQ + FY − PYQ)*C{row}`) for EBITDA and Revenue when the source path is filings-derived. Cell comments must enumerate each stub with its filing URL.

## [2.0.0] — 2026-05-05

### Changed
- Major version bump across the plugin and all skills to reset versioning lineage after the 1.9.x iteration burst on earningsupdate, buyerslist, and precedents.

## [1.9.x] — 2026-04-22 to 2026-05-04

A long iteration run on three skills, captured as a band:

- **`earningsupdate-infor`** — Added at v1.9.10. Subsequent v1.9.11 through v1.9.20 hardened slide 2 / slide 3 formatting: rPr preservation, character / word caps, broker table $ / % formatting, delta color by direction, no-rotate triangles, variance color, segment-prefix bolding, variable-length bullets, Macabacus placeholder, plain `$` on slide values (currency code only in the footnote). Consolidated bullet writing into a single `write_bulleted_shape` helper with a post-write `buChar` assert.
- **`buyerslist-infor`** — Optional third "Other Buyers" category (v1.7.0); template-tampering hardening (v1.9.0). Tab is never renamed in openpyxl (rename corrupts gridlines / columns / conditional formatting).
- **`comps-infor`** — Single-axis grouping rule (all-geography or all-sector; never mix). Refreshed template; description column moved AM → AL.
- **`captable-infor`** — FX-convert options strikes (v1.9.9). Convert / cash-settled handling clarified.
- **`lbo-model`** — Replaced internal `lbo-infor` with the externalized `lbo-model` skill from `financial-analysis` (v1.9.20).
- **`expenses-extraction`** — Removed (v1.9.5). Out of scope for the plugin.

## [1.8.0] — 2026-04-22

### Changed
- `buyerslist-infor`: Other Buyers tab is kept literally titled `Other Buyers` (never renamed in openpyxl). The user-supplied category label is written to the Summary sheet `B17` instead.

## [1.7.0] — 2026-04-22

### Added
- Optional third buyer category on `buyerslist-infor` (family offices, sovereign wealth, SPACs, consortium buyers, etc.) — user provides the label; the skill writes to the `Other Buyers` tab.

## [1.5.0 — 1.6.0] — 2026-04-22

### Changed
- Buyer Rationale column expanded to professional IB-prose length with wrap-text and tall row heights.
- M&A activity and Portfolio Companies columns standardised to `"Target - YY, Target - YY, Target - YY"` format (max 3 per cell, sector / thesis fit first).

## [1.4.0] — 2026-04-21

### Added
- `lbo-infor` skill (later replaced by `lbo-model`).
- Cap-table → LBO integration; Revenue / EBITDA forecasts link from cap table into LBO model.

### Changed
- `captable-infor`: convertible-debenture / cash-settled handling refined.

## [1.0.0 — 1.3.x] — 2026-04-15 to 2026-04-21

### Added
- `comps-infor`, `precedents-infor`, `buyerslist-infor`, `captable-infor`, `brand-guidelines-infor`, `deckcheck-infor`, original `lbo-infor` skills.
- INFOR Excel and PowerPoint templates bundled with the plugin source.
- Marketplace manifest at `.claude-plugin/marketplace.json` for Co-work installation.
- Templates discovered by walking from the repo root, allowing cross-machine installs.

## Older

The first 102 commits cover the initial scaffolding of the plugin (v0.1 → v1.0), repeated template refreshes, and the gradual migration from session-scoped paths to bundled templates. See `git log` for the full history.
