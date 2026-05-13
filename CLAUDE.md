# Contributor brief — infor-workflows

This file is loaded automatically when Claude Code opens this repo. It orients you (and future contributors) to the plugin's layout and conventions.

## What this repo is

A single Claude Code plugin, **`infor-workflows`**, containing ten skills that automate INFOR Financial Group analyst deliverables — comps, precedents, buyer lists, cap tables, branded decks, earnings updates, LBO models, deck QC, and supporting voice / wireframe skills. Analysts install the plugin via the Co-work marketplace and invoke skills with `/<skill-name>` or by describing the task in plain English.

User-facing overview: [README.md](README.md). Per-version changes: [CHANGELOG.md](CHANGELOG.md).

## Layout

```
.claude-plugin/marketplace.json    Marketplace manifest — points at infor-workflows/ as the plugin root
infor-workflows/
├── skills/                        One directory per skill (10 total)
│   └── <skill-name>/
│       ├── SKILL.md               Workflow + frontmatter (name, description, version, allowed-tools)
│       └── references/            Progressive-disclosure detail loaded on demand
├── scripts/                       Plugin-wide helpers + tests
│   ├── find_template.sh           Resolves a template filename across install paths
│   ├── sanitize_name.sh           Sanitizes a string for safe use as a filename component
│   ├── pptx_helpers.py            Shared python-pptx helpers (set_text, write_bulleted_shape, clone_slide, …)
│   ├── test_pptx_helpers.py       Unit tests for the Python helpers
│   └── test_shell_helpers.py      Unit tests for the bash helpers
└── templates/                     Excel + PowerPoint templates shipped with the plugin
README.md
CHANGELOG.md
CLAUDE.md                          ← you are here
```

The nesting (`infor-workflows/infor-workflows/`) exists because `marketplace.json` points `source: "./infor-workflows"` — the inner directory is the actual plugin root. Don't flatten it without also updating the marketplace manifest.

## Adding or modifying a skill

A skill is a directory under `infor-workflows/skills/<name>/` with at least `SKILL.md`. Frontmatter:

```yaml
---
name: <skill-name>           # must match the directory name
description: >               # one paragraph; lead with the trigger phrases users say
  Use this skill when …
version: x.y.z
allowed-tools: [Read, Bash, Write, Glob, WebSearch]
---
```

`allowed-tools` is enforced by the harness — list only what the workflow actually needs. Tighter is better.

**Description length:** keep it focused. The router uses this field to decide whether to load the skill, and trigger phrases (`"comps"`, `"buyer list"`, `/deckcheck-infor`) are what fire it. Avoid prose that doesn't add a trigger. Aim under ~500 chars unless the skill genuinely covers many distinct user intents.

## Conventions

### Progressive disclosure
Long workflows split into a short `SKILL.md` (workflow + step outline) plus `references/<topic>.md` files loaded on demand. The pattern was introduced by [`infor-wireframe`](infor-workflows/skills/infor-wireframe/) and applied to the long skills in PR #73. New skills longer than ~250 lines should follow it.

### Shared helpers (don't re-implement)
- **Templates** — never hardcode template paths or re-implement the `find` search. Use `bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR X Template.xlsx"` from the skill, and the script handles every install path.
- **Filename sanitization** — never re-implement the "remove special chars, replace spaces with hyphens" logic per skill. Use `SANITIZED=$(bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/sanitize_name.sh" "$RAW_NAME")` — handles company names, CapIQ tickers (`NasdaqGS:MSFT` → `NasdaqGS-MSFT`), ampersands, leading / trailing whitespace, consecutive specials.
- **python-pptx formatting** — `set_text`, `write_bulleted_shape`, `set_cell_text`, `find_shape`, `find_shape_in_group`, `fmt_broker_value` live in [`infor-workflows/scripts/pptx_helpers.py`](infor-workflows/scripts/pptx_helpers.py) with brand constants (`PALATINO`, `COLOR_UP`, `COLOR_DOWN`). Skills import them via:
  ```python
  import sys, os
  sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", "./infor-workflows") + "/scripts")
  from pptx_helpers import set_text, write_bulleted_shape, find_shape
  ```

### Versioning — single plugin version, all skills tied to it

There is one version for the entire plugin. **Any change to any skill bumps the plugin version, and every skill's `version:` frontmatter field is kept in lock-step.** No per-skill version drift.

- Plugin version lives in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json).
- Every [`SKILL.md`](infor-workflows/skills/) carries a `version:` frontmatter field that **must equal** the plugin version. When you bump the plugin, bump all ten skills to match.
- Update [CHANGELOG.md](CHANGELOG.md) on every bump. Format: Keep-a-Changelog (`## [x.y.z] — YYYY-MM-DD` with Added / Changed / Fixed sections). One CHANGELOG covers the plugin; per-skill changelogs are not maintained.

Why one version: with 10 skills sharing helpers, templates, and conventions, drift between skill versions creates support questions ("which version of which skill am I running?") with no useful answer. A single number for the whole plugin keeps the bug-report / changelog story simple.

### Templates
All templates live in [`infor-workflows/templates/`](infor-workflows/templates/). They are binary `.xlsx`, `.pptx`, `.thmx`, `.png` — keep them in git. If a template changes, increment the corresponding skill's version because the cell map / shape names may move.

### Output files
Every file-producing skill writes to the **current working directory** (`./`). When invoked from the repo root, generated files land at the project root; `.gitignore` patterns on `/*.xlsx`, `/*.pptx`, and `/*.docx` keep them out of git without affecting the tracked templates under `infor-workflows/templates/`. When invoked elsewhere, outputs land in whatever cwd the analyst was in. The legacy `outputs/` directory is still gitignored defensively but no skill writes there anymore.

## Testing

```bash
python -m unittest infor-workflows/scripts/test_pptx_helpers.py    # pptx helpers (set_text, clone_slide, …)
python -m unittest infor-workflows/scripts/test_shell_helpers.py   # find_template.sh + sanitize_name.sh
python infor-workflows/skills/precedents-infor/test_allow_list.py  # precedents URL allow-list gate
```

All three should pass before opening a PR. CI runs them automatically on every PR and push to `main` — see [`.github/workflows/tests.yml`](.github/workflows/tests.yml). The same workflow also enforces the single-version policy, the `/<skill-name>` mention rule, and the `allowed-tools` frontmatter requirement.

End-to-end smoke testing (e.g., invoking `/comps-infor` against a real CapIQ workbook) is manual — there is no fixture deck checked into the repo.

## Skill relationships

The skills aren't independent — they compose into common workflows. When an analyst kicks off a real deliverable, expect to chain several skills:

```
                           ┌─────────────────────┐
                           │  infor-wireframe    │  (plan the deck)
                           └──────────┬──────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                ▼                     ▼                     ▼
   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
   │ infor-deck-writing │  │ brand-guidelines   │  │ Data-table skills  │
   │ (words on slides)  │  │ (visual format)    │  │ (comps / precedents│
   │                    │  │                    │  │  / buyerslist /    │
   │                    │  │                    │  │  captable)         │
   └────────────────────┘  └──────────┬─────────┘  └─────────┬──────────┘
                                      │                       │
                                      └───────┬───────────────┘
                                              ▼
                                  ┌────────────────────┐
                                  │  Output deck       │
                                  └──────────┬─────────┘
                                             │
                                             ▼
                                  ┌────────────────────┐
                                  │  deckcheck-infor   │  (QC the result)
                                  └────────────────────┘
```

Typical chains by deliverable:

| Deliverable | Skill chain |
|---|---|
| **CIM** | `infor-wireframe` → `infor-deck-writing` → `brand-guidelines-infor` + (`comps-infor` / `precedents-infor` / `buyerslist-infor` / `captable-infor` for embedded tables) → `deckcheck-infor` |
| **Teaser** | `infor-wireframe` → `infor-deck-writing` → `brand-guidelines-infor` → `deckcheck-infor` |
| **Pitch deck** | `infor-wireframe` → `infor-deck-writing` → `brand-guidelines-infor` + (`comps-infor` / `precedents-infor` / `buyerslist-infor`) → `deckcheck-infor` |
| **Fairness opinion** | `infor-wireframe` → `infor-deck-writing` (fairness-opinion-recipes) → `brand-guidelines-infor` + (`comps-infor` / `precedents-infor`) → `deckcheck-infor` |
| **Quarterly earnings update** | `earningsupdate-infor` (built-in; also invokes `captable-infor` as Step 8) |
| **LBO model** | `lbo-model` (standalone — produces .xlsx, not a deck) |

Cross-skill rules embedded in the SKILL.md files:
- `brand-guidelines-infor` defers all on-slide-text guidance to `infor-deck-writing` (don't restate voice rules)
- `deckcheck-infor` defers all visual-formatting rules to `brand-guidelines-infor` (don't restate brand colors / fonts)
- `infor-wireframe` hands off to `infor-deck-writing` for copy and `brand-guidelines-infor` for construction
- `earningsupdate-infor` invokes `captable-infor` directly as a sub-step

Skills that don't compose with the rest of the chain: `lbo-model` (produces an Excel model, not slide content).

## Conventions Claude should respect

These appear in user memory (`~/.claude/projects/.../memory/`) and apply across skills:

- **Excel does the math, not Claude.** For any Excel-based deliverable (precedents, comps, captable, LBO), arithmetic must live in cell formulas — never pre-compute in Python and write a scalar. The reviewer can audit a formula; they can't audit a number.

## Recent PRs worth knowing about

- [#72](https://github.com/tatewilsonwork/infor-workflows/pull/72) — shared template-finder script + README fix
- [#73](https://github.com/tatewilsonwork/infor-workflows/pull/73) — pptx_helpers module + tests + progressive-disclosure splits on 4 long SKILL.md files

Older history is in `git log` and [CHANGELOG.md](CHANGELOG.md).
