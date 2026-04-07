# INFOR Workflows

INFOR Financial Group plugin with four automated workflows for analysts.

Current version: **0.5.1**

## Skills

| Skill | Description |
|-------|-------------|
| precedents | Researches 8 relevant M&A precedent transactions and populates the INFOR Precedents Template (cells B7:K14) with verified Revenue, EBITDA, AUM, and deal metrics |
| comps-infor | Builds a public comparable companies table with 8 CapIQ tickers split into two labelled groups, with a short description for each company, written into the INFOR Comps Template |
| cap-table | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A). Covers debt, leases, options/RSUs/warrants, convertible debentures, cash, and shares outstanding |
| expenses-extraction | Fills in the INFOR Expense Report template from attached receipt images |

## Usage

Invoke any skill by name, command, or by describing what you want:

```
/comps-infor Rogers Communications
"Build a precedents table for CI Financial Corp"
"Fill in the cap table for NasdaqGS:MSFT"
"Fill in my expense report" (attach receipt images)
```

## Installation

In Co-work, open the **Customize** panel → **Add plugin** → type the repo name. Co-work will install all skills and templates automatically. No manual setup required.

## Templates

All four Excel templates are included in the plugin source tree (`infor-workflows/templates/`) and are installed automatically when you add the plugin. Skills locate them at runtime — no manual path configuration needed.

## Folder Structure

```
infor-workflows/
├── infor-workflows/            # Plugin source tree (installed via "Add plugin")
│   ├── skills/
│   │   ├── cap-table/
│   │   ├── comps-infor/
│   │   ├── expenses-extraction/
│   │   └── precedents/
│   ├── templates/              # Excel templates bundled with the plugin
│   └── hooks/
├── outputs/                    # Deal outputs (gitignored)
└── README.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.5.1 | 2026-04-07 | comps-infor skill now writes one-line descriptions (≤50 chars) into column AM for each comparable company |
| 0.5.0 | 2026-04-07 | Bundled Excel templates in plugin source for cross-machine installs; fixed template discovery to check plugin cache paths; fixed precedents outputs folder fallback; added Installation section to README |
| v4 / 0.4.2 | 2026-03-26 | Added `/precedents` command and skill; bundled INFOR Precedents Template; HQ field uses ISO 2-letter country codes; improved financial data sourcing logic for public targets |
| v3 | 2026-03-23 | Added comps-infor skill; bundled all templates into plugin; removed hardcoded file paths for cross-machine compatibility |
| v2 | 2026-03-18 | Revised version with cap-table and expenses-extraction |
