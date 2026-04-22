# INFOR Workflows

INFOR Financial Group plugin for analysts — automated deal workflows, branded presentations, and deck QC.

Current version: **1.9.0**

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| comps-infor | `/comps-infor` | Builds a public comparable companies table with 18 CapIQ tickers split into three labelled groups, written into the INFOR Comps Template |
| precedents-infor | `/precedents-infor` | Researches 8 relevant M&A precedent transactions and populates the INFOR Precedents Template with verified Revenue, EBITDA, AUM, and deal metrics |
| buyerslist-infor | `/buyerslist-infor` | Builds a strategic and financial buyer universe for a sell-side M&A process, tiered A/B/C, and populates the INFOR Buyers List Template |
| captable-infor | `/captable-infor` | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A) |
| lbo-infor | `/lbo-infor` | Builds an LBO model in Excel for PE transactions — starts from a populated cap table (via captable-infor), links balance-sheet assumptions, and fills in Sources & Uses, Operating Model, Debt Schedule, and Returns Analysis |
| expenses-extraction | `/expenses-extraction` | Fills in the INFOR Expense Report template from attached receipt images |
| brand-guidelines-infor | `/brand-guidelines-infor` | Applies or reviews INFOR brand standards on PowerPoint decks — colors, fonts, layouts, charts, tables |
| deckcheck-infor | `/deckcheck-infor` | Reviews an attached deck for grammar/spelling, INFOR brand formatting, and factual accuracy; delivers a tiered review (Tier I/II/III) with Confidence and Impact scores as a Word (.docx) document |

## Usage

Invoke any skill by name, command, or by describing what you want:

```
/comps-infor Rogers Communications
/precedents-infor CI Financial Corp
/buyerslist-infor Dye & Durham
/deckcheck-infor (attach a .pptx)
"Fill in the cap table for NasdaqGS:MSFT"
"Build an LBO model for Dye & Durham"
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
│   │   ├── lbo-infor/
│   │   └── precedents-infor/
│   └── templates/              # Excel templates and INFOR logo
├── outputs/                    # Deal outputs (gitignored)
└── README.md
```
