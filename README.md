# INFOR Workflows

INFOR Financial Group plugin for analysts — automated deal workflows, branded presentations, and deck QC.

Current version: **2.7.0** — see [CHANGELOG.md](CHANGELOG.md) for per-version changes. Contributors: see [CLAUDE.md](CLAUDE.md).

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [comps-infor](infor-workflows/skills/comps-infor/SKILL.md) | `/comps-infor` | Builds a public comparable companies table with 18 CapIQ tickers split into three labelled groups, written into the INFOR Comps Template |
| [precedents-infor](infor-workflows/skills/precedents-infor/SKILL.md) | `/precedents-infor` | Researches up to 15 relevant M&A precedent transactions and populates the INFOR Precedents Template with verified Revenue, EBITDA, and deal metrics |
| [buyerslist-infor](infor-workflows/skills/buyerslist-infor/SKILL.md) | `/buyerslist-infor` | Builds a strategic and financial buyer universe for a sell-side M&A process, tiered A/B/C, and populates the INFOR Buyers List Template |
| [captable-infor](infor-workflows/skills/captable-infor/SKILL.md) | `/captable-infor` | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A) |
| [earningsupdate-infor](infor-workflows/skills/earningsupdate-infor/SKILL.md) | `/earningsupdate-infor` | Builds a branded 5-slide quarterly earnings update deck from a recent 10-Q/10-K and Bloomberg EEO snip — company overview, KPI tiles, Broker Estimates vs Actuals table, business updates, and management quotes |
| [lbo-model](infor-workflows/skills/lbo-model/SKILL.md) | `/lbo-model` | Builds an LBO (Leveraged Buyout) model in Excel from scratch — Sources & Uses, Operating Model, Debt Schedule, Returns Analysis — with every calculation as an Excel formula |
| [brand-guidelines-infor](infor-workflows/skills/brand-guidelines-infor/SKILL.md) | `/brand-guidelines-infor` | Applies or reviews INFOR brand standards on PowerPoint decks — colors, fonts, layouts, charts, tables. Cross-links to `infor-deck-writing` for all on-slide text |
| [infor-deck-writing](infor-workflows/skills/infor-deck-writing/SKILL.md) | `/infor-deck-writing` | Writes slide-ready text in INFOR voice: executive summaries, investment highlights, market overviews, valuation commentary, buyer commentary, fairness-opinion language. Calibrated from a corpus of INFOR CIMs, pitches, teasers, fairness opinions, and formal valuations |
| [infor-wireframe](infor-workflows/skills/infor-wireframe/SKILL.md) | `/infor-wireframe` | Produces a slide-by-slide wireframe (page order, purpose, content blocks, recommended layout) for a new CIM, pitch, fairness opinion, or teaser. Hands off to `infor-deck-writing` for copy and `brand-guidelines-infor` for construction |
| [deckcheck-infor](infor-workflows/skills/deckcheck-infor/SKILL.md) | `/deckcheck-infor` | Reviews an attached deck for grammar/spelling, INFOR brand formatting, and factual accuracy; delivers a tiered review (Tier I/II/III) with Confidence and Impact scores as a Word (.docx) document |

## Usage

Invoke any skill by name, command, or by describing what you want:

```
/comps-infor Rogers Communications
/precedents-infor CI Financial Corp
/buyerslist-infor Dye & Durham
/deckcheck-infor (attach a .pptx)
/earningsupdate-infor (attach 10-Q + Bloomberg EEO snip)
/lbo-model (then describe deal structure + operating projections)
"Fill in the cap table for NasdaqGS:MSFT"
"Format this deck to INFOR brand guidelines"
"Draft an executive summary for [Company]"
"Write 5 investment highlights for the teaser"
"Rewrite these notes in INFOR voice"
"Wireframe a CIM for [Company]"
"Plan the slide order for a fairness opinion"
"Outline a pitch for [Company]"
```

## Installation

In Co-work, open the **Customize** panel → **Add plugin** → type the repo name. Co-work will install all skills and templates automatically. No manual setup required.

## Templates

All Excel templates and the INFOR logo are included in the plugin source tree (`infor-workflows/templates/`) and are installed automatically when you add the plugin. Skills locate them at runtime — no manual path configuration needed.

## Output Files

Every skill saves its output (`.xlsx`, `.pptx`, or `.docx`) to the **current working directory**. When invoked from the repo root, outputs land at the project root and are excluded from git via `.gitignore` patterns on `/*.xlsx`, `/*.pptx`, and `/*.docx`. When invoked elsewhere, outputs land in whatever directory you ran from.

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
│   │   ├── earningsupdate-infor/
│   │   ├── infor-deck-writing/
│   │   ├── infor-wireframe/
│   │   ├── lbo-model/
│   │   └── precedents-infor/
│   ├── scripts/                # Shared helpers (find_template.sh, pptx_helpers.py) + tests
│   └── templates/              # Excel templates and INFOR logo
└── README.md
```
