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
│   ├── pptx_helpers.py            Shared python-pptx helpers (set_text, write_bulleted_shape, …)
│   └── test_pptx_helpers.py       Unit tests for the helpers
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
- **python-pptx formatting** — `set_text`, `write_bulleted_shape`, `set_cell_text`, `find_shape`, `find_shape_in_group`, `fmt_broker_value` live in [`infor-workflows/scripts/pptx_helpers.py`](infor-workflows/scripts/pptx_helpers.py) with brand constants (`PALATINO`, `COLOR_UP`, `COLOR_DOWN`). Skills import them via:
  ```python
  import sys, os
  sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", "./infor-workflows") + "/scripts")
  from pptx_helpers import set_text, write_bulleted_shape, find_shape
  ```

### Versioning
- Plugin version (in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)) bumps when any skill ships a behavior change or a new skill is added.
- Each skill's own `version:` in its frontmatter bumps independently when that skill changes.
- Update [CHANGELOG.md](CHANGELOG.md) when bumping the plugin version. Format: Keep-a-Changelog (`## [x.y.z] — YYYY-MM-DD` with Added / Changed / Fixed sections).

### Templates
All templates live in [`infor-workflows/templates/`](infor-workflows/templates/). They are binary `.xlsx`, `.pptx`, `.thmx`, `.png` — keep them in git. If a template changes, increment the corresponding skill's version because the cell map / shape names may move.

### Output files
Every file-producing skill writes to the **current working directory** (`./`). When invoked from the repo root, generated files land at the project root; `.gitignore` patterns on `/*.xlsx`, `/*.pptx`, and `/*.docx` keep them out of git without affecting the tracked templates under `infor-workflows/templates/`. When invoked elsewhere, outputs land in whatever cwd the analyst was in. The legacy `outputs/` directory is still gitignored defensively but no skill writes there anymore.

## Testing

```bash
python -m unittest infor-workflows/scripts/test_pptx_helpers.py
python infor-workflows/skills/precedents-infor/test_allow_list.py
```

Both should pass before opening a PR. The `pptx_helpers` tests build fresh in-memory decks; the allow-list test runs the URL gate against PASS/FAIL fixtures.

End-to-end smoke testing (e.g., invoking `/comps-infor` against a real CapIQ workbook) is manual — there is no fixture deck checked into the repo.

## Conventions Claude should respect

These appear in user memory (`~/.claude/projects/.../memory/`) and apply across skills:

- **Excel does the math, not Claude.** For any Excel-based deliverable (precedents, comps, captable, LBO), arithmetic must live in cell formulas — never pre-compute in Python and write a scalar. The reviewer can audit a formula; they can't audit a number.

## Recent PRs worth knowing about

- [#72](https://github.com/tatewilsonwork/infor-workflows/pull/72) — shared template-finder script + README fix
- [#73](https://github.com/tatewilsonwork/infor-workflows/pull/73) — pptx_helpers module + tests + progressive-disclosure splits on 4 long SKILL.md files

Older history is in `git log` and [CHANGELOG.md](CHANGELOG.md).
