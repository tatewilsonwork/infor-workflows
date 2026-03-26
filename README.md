# INFOR Workflows

INFOR Financial Group plugin with four automated workflows for analysts.

Current version: **v4** (`infor-workflows-v4.plugin`)

## Skills & Commands

| Command | Skill | Description |
|---------|-------|-------------|
| `/precedents [company]` | precedents | Researches 8 relevant M&A precedent transactions and populates the INFOR Precedents Template (cells B7:K14) with verified Revenue, EBITDA, AUM, and deal metrics |
| — | comps-infor | Builds a public comparable companies table with 8 CapIQ tickers split into two labelled groups, written into the INFOR Comps Template |
| — | cap-table | Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A). Covers debt, leases, options/RSUs/warrants, convertible debentures, cash, and shares outstanding |
| — | expenses-extraction | Fills in the INFOR Expense Report template from attached receipt images |

## Usage

Invoke any skill by name, command, or by describing what you want:

```
/precedents CI Financial Corp
/comps-infor Rogers Communications
"Fill in the cap table for NasdaqGS:MSFT"
"Fill in my expense report" (attach receipt images)
```

## Templates

All four Excel templates are bundled inside the plugin and located automatically at runtime. No manual setup required.

Source templates are also kept in `templates/` for reference and future updates.

## Folder Structure

```
infor-workflows/
├── infor-workflows-v4.plugin   # Current plugin — share this with other INFOR employees
├── infor-workflows/            # Plugin source tree
│   ├── commands/
│   │   └── precedents.md
│   ├── skills/
│   │   ├── cap-table/
│   │   ├── comps-infor/
│   │   ├── expenses-extraction/
│   │   └── precedents/
│   ├── templates/
│   └── hooks/
├── templates/                  # Source Excel templates
├── outputs/                    # Deal outputs
└── README.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v4 | 2026-03-26 | Added `/precedents` command and skill; bundled INFOR Precedents Template; HQ field uses ISO 2-letter country codes; improved financial data sourcing logic for public targets |
| v3 | 2026-03-23 | Added comps-infor skill; bundled all templates into plugin; removed hardcoded file paths for cross-machine compatibility |
| v2 | 2026-03-18 | Revised version with cap-table and expenses-extraction |
