# INFOR Workflows

INFOR Financial Group plugin with three automated workflows for analysts.

Current version: **v3** (`infor-workflows-v3.plugin`)

## Skills

- **cap-table** — Populates the INFOR Capitalization Table from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A). Covers debt, leases, options/RSUs/warrants, convertible debentures, cash, and shares outstanding.
- **comps-infor** — Builds a public comparable companies table with 8 CapIQ tickers split into two labelled groups, written into the INFOR Comps Template.
- **expenses-extraction** — Fills in the INFOR Expense Report template from attached receipt images.

## Usage

Invoke any skill by name, or simply describe what you want to do:
- "Fill in the cap table for NasdaqGS:MSFT"
- "Build a comps table for Rogers Communications"
- "Fill in my expense report" (then attach receipt images)

## Templates

All three Excel templates are bundled inside the plugin and located automatically at runtime. No manual setup required.

Source templates are also kept in `templates/` for reference and future updates.

## Folder Structure

```
infor-workflows/
├── infor-workflows-v3.plugin   # Current plugin — share this with other INFOR employees
├── old/
│   └── infor-workflows-v2.plugin
├── templates/                  # Source Excel templates
├── outputs/                    # Deal outputs
└── README.md
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3 | 2026-03-23 | Added comps-infor skill; bundled all 3 templates into plugin; removed hardcoded file paths for cross-machine compatibility |
| v2 | 2026-03-18 | Initial release with cap-table and expenses-extraction |
