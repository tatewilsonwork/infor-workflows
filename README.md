# INFOR Workflows

INFOR Financial Group plugin for analysts — automated deal workflows, branded presentations, and deck QC.

Current version: **1.9.5**

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| comps-infor | `/comps-infor` | Builds a public comparable companies table with 8 CapIQ tickers split into two labelled groups, written into the INFOR Comps Template |
| precedents-infor | `/precedents-infor` | Researches 8 relevant M&A precedent transactions and populates the INFOR Precedents Template with verified Revenue, EBITDA, AUM, and deal metrics |
| buyerslist-infor | `/buyerslist-infor` | Builds a strategic and financial buyer universe for a sell-side M&A process, tiered A/B/C, and populates the INFOR Buyers List Template |
| captable-infor | `/captable-infor` | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A) |
| brand-guidelines-infor | `/brand-guidelines-infor` | Applies or reviews INFOR brand standards on PowerPoint decks — colors, fonts, layouts, charts, tables |
| deckcheck-infor | `/deckcheck-infor` | Reviews an attached deck for grammar/spelling, INFOR brand formatting compliance, and factual accuracy via web search |

## Usage

Invoke any skill by name, command, or by describing what you want:

```
/comps-infor Rogers Communications
/precedents-infor CI Financial Corp
/buyerslist-infor Dye & Durham
/deckcheck-infor (attach a .pptx)
"Fill in the cap table for NasdaqGS:MSFT"
"Format this deck to INFOR brand guidelines"
```

## Installation

In Co-work, open the **Customize** panel → **Add plugin** → type the repo name. Co-work will install all skills and templates automatically. No manual setup required.

## Templates

All Excel templates and the INFOR logo are included in the plugin source tree (`infor-workflows/templates/`) and are installed automatically when you add the plugin. Skills locate them at runtime — no manual path configuration needed.

## Folder Structure

```
infor-workflows/
├── infor-workflows/            # Plugin source tree (installed via "Add plugin")
│   ├── skills/
│   │   ├── brand-guidelines-infor/
│   │   ├── buyerslist-infor/
│   │   ├── captable-infor/
│   │   ├── comps-infor/
│   │   ├── deckcheck-infor/
│   │   └── precedents-infor/
│   └── templates/              # Excel templates and INFOR logo
├── outputs/                    # Deal outputs (gitignored)
└── README.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.9.5 | 2026-04-22 | Removed `expenses-extraction` skill and the bundled `INFOR Expense Report Template.xlsx`; pruned all references from the main README (skills table, usage examples, folder structure); bumped plugin + marketplace manifests to 1.9.5 |
| 1.3.4 | 2026-04-21 | Repo cleanup: unified all skills and plugin manifests to v1.3.4; removed empty `hooks/` directory; pruned stale entries from `.claude/settings.local.json`; standardized SKILL.md frontmatter style; tightened plugin description |
| 1.3.1 | 2026-04-20 | brand-guidelines-infor: fixed `clone_slide` helper to copy slide relationships (was dropping image rels, causing broken red-X logo on cover); added slide-specific conventions from test-output review — required deck structure (cover → exec summary → graphical content → disclaimer → contact page), text-only slides restricted to exec summary and disclaimer, preserve placeholder rectangles and grouped graphics, Business Updates box takes IB-tone prose (not metrics), cover INFOR logo must not be touched, earnings slide includes two quote-paper graphics, contact page defaults to Neil + 3 `[x]` placeholders |
| 1.3.0 | 2026-04-20 | brand-guidelines-infor now starts from the bundled `INFOR Deck Template.pptx` (with `INFORFG.thmx` theme) and clones the template's sample slides as starting points, preserving master-level formatting (title bars, footers, page numbers, theme font) that was previously lost when building decks from scratch |
| 1.2.1 | 2026-04-16 | deckcheck-infor now delivers the tiered review as a Microsoft Word (.docx) document saved to `outputs/` instead of an inline markdown response |
| 1.2.0 | 2026-04-16 | deckcheck-infor output restructured into three tiers (I/II/III) with Confidence and Impact scores (1–10) and edit category tagging per suggestion |
| 1.1.0 | 2026-04-16 | Added deckcheck-infor skill — reviews decks for grammar/spelling, INFOR brand formatting, and factual accuracy via web search |
| 1.0.5 | 2026-04-15 | Added brand-guidelines-infor skill and INFOR logo asset; defines all PowerPoint formatting rules for INFOR presentations |
| 1.0.3 | 2026-04-10 | Removed confirmation steps from buyerslist-infor, comps-infor, and precedents-infor for faster execution |
| 1.0.2 | 2026-04-09 | Removed confirmation step from comps-infor and precedents-infor skills |
| 0.7.1 | 2026-04-07 | Renamed cap-table → captable-infor and precedents → precedents-infor for naming consistency |
| 0.7.0 | 2026-04-07 | Added buyerslist-infor skill and INFOR Buyers List Template; builds strategic and financial buyer universe for sell-side M&A, tiered A/B/C |
| 0.6.0 | 2026-04-07 | Repo cleanup: removed duplicate templates, stale .plugin file, and commands/ directory; fixed template discovery path; version history and README tidied |
| 0.5.1 | 2026-04-07 | comps-infor skill now writes one-line descriptions into column AM for each comparable company |
| 0.5.0 | 2026-04-07 | Bundled Excel templates in plugin source for cross-machine installs; fixed template discovery to check plugin cache paths |
| 0.4.2 | 2026-03-26 | Added precedents command and skill; bundled INFOR Precedents Template |
| 0.3.0 | 2026-03-23 | Added comps-infor skill; bundled all templates into plugin; removed hardcoded file paths |
| 0.2.0 | 2026-03-18 | Revised version with cap-table and expenses-extraction |
