# INFOR Workflows

INFOR Financial Group plugin for analysts — automated deal workflows, branded presentations, and deck QC.

Current version: **1.1.0**

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| comps-infor | `/comps-infor` | Builds a public comparable companies table with 8 CapIQ tickers split into two labelled groups, written into the INFOR Comps Template |
| precedents-infor | `/precedents-infor` | Researches 8 relevant M&A precedent transactions and populates the INFOR Precedents Template with verified Revenue, EBITDA, AUM, and deal metrics |
| buyerslist-infor | `/buyerslist-infor` | Builds a strategic and financial buyer universe for a sell-side M&A process, tiered A/B/C, and populates the INFOR Buyers List Template |
| captable-infor | `/captable-infor` | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A) |
| expenses-extraction | `/expenses-extraction` | Fills in the INFOR Expense Report template from attached receipt images |
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
"Fill in my expense report" (attach receipt images)
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
│   │   ├── expenses-extraction/
│   │   └── precedents-infor/
│   ├── templates/              # Excel templates and INFOR logo
│   └── hooks/
├── outputs/                    # Deal outputs (gitignored)
└── README.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
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
