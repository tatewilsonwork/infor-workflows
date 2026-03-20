# INFOR Workflows

INFOR Financial Group plugin with two workflows for analysts.

## Skills

- **cap-table** — Populates the INFOR Capitalization Table template from a CapIQ ticker and attached financial statements (10-K, annual report, MD&A).
- **expenses-extraction** — Fills in the INFOR Expense Report template from attached receipt images.

## Usage

Invoke either skill by name, or simply describe what you want to do:
- "Fill in the cap table for NasdaqGS:MSFT"
- "Fill in my expense report" (then attach receipt images)

## Templates

Both Excel templates are bundled in the `templates/` folder and are automatically located when each skill runs.
