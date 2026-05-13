---
name: lbo-model
description: >
  Builds an LBO (Leveraged Buyout) model in Excel from scratch using openpyxl — Sources & Uses,
  Operating Model, Debt Schedule, and Returns Analysis tabs — for private equity transactions,
  deal materials, or investment committee presentations. Every calculation is an Excel formula
  (never a Python-computed scalar) so the model is dynamic. Activates on /lbo-model, "LBO model",
  "leveraged buyout", "PE model", "build an LBO", "Sources and Uses", "returns analysis", or any
  request to model a sponsor-led acquisition with debt financing.
version: 2.9.0
allowed-tools: [Read, Bash, Write, Glob]
---

# INFOR LBO Model — Workflow

This skill builds a leveraged-buyout model from the analyst's inputs. Unlike the table-population skills in this plugin, the LBO skill **constructs the workbook structure itself** — there is no LBO template. The model has four standard tabs (Assumptions, Sources & Uses, Operating Model, Debt Schedule, Returns) and follows PE-standard sign conventions and formula-color coding.

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. Working directory is resolved inline where needed.

---

## Workflow Steps

### Step 1 — Collect Inputs

Ask the user for the inputs below in a single message. Every input is required unless flagged optional.

> "To build the LBO model, please provide:
> - **Target company name and a brief description** (sector, business model)
> - **Transaction structure** — purchase price (Enterprise Value) and any assumed debt
> - **Financing assumptions** — sponsor equity %, debt tranches (label, size, rate, tenor, amortization), any preferred / mezz
> - **Operating projections** — Revenue (Year 0 / LTM) and growth rate by year, EBITDA margin by year, D&A % of revenue, capex % of revenue, working-capital change % of revenue change, tax rate
> - **Exit assumptions** — exit year (typically Year 5), exit EBITDA multiple (or held flat at entry multiple)
> - **Optional** — fees (advisory, financing, OID), minimum cash balance, cash sweep priority"

Wait for all required inputs before proceeding. If the user provides a partial set, ask only for the missing items — don't repeat what they've already given.

For inputs the user can't immediately provide (sector benchmarks, default tax rate), suggest standard PE assumptions and confirm before applying them:
- Tax rate: 25% (US), 26.5% (Canada)
- Minimum cash: $10M
- Cash sweep: senior secured first, then sub debt
- Exit multiple: held at entry

---

### Step 2 — Sanitize the Output Filename

Sanitize the target company name (remove special characters, replace spaces with hyphens) and form the output path:

```
./<SANITIZED_COMPANY_NAME> - LBO Model.xlsx
```

The file is written to the current working directory.

---

### Step 3 — Build the Workbook Structure

Create the workbook with openpyxl using five tabs in this order. Section 1 of the Domain Reference details the cell map for each tab; this step describes the build order and dependencies.

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
wb.remove(wb.active)  # remove the default sheet — we'll add named tabs explicitly

assumptions = wb.create_sheet("Assumptions")
sources_uses = wb.create_sheet("Sources & Uses")
operating = wb.create_sheet("Operating Model")
debt = wb.create_sheet("Debt Schedule")
returns = wb.create_sheet("Returns")
```

Build order matters because later tabs reference earlier ones. Build `Assumptions` first (no dependencies), then `Sources & Uses` (references Assumptions), then `Operating Model` (references Assumptions for growth / margin drivers), then `Debt Schedule` (references Sources & Uses for opening balances and Operating Model for FCF available for paydown), then `Returns` (references everything).

**Every calculation must be an Excel formula.** Never compute a value in Python and write it as a scalar. The model has to update when the user tweaks an input cell, and the reviewer audits formulas, not numbers.

---

### Step 4 — Populate Assumptions

The `Assumptions` tab is the single input sheet — every other tab references it. Layout in column B (label) and column C (value), with timeline columns D–H for the five projection years where assumptions vary by year.

Group by section, with blank rows between groups:

| Section | Rows | Inputs |
|---------|------|--------|
| Transaction | 4–9 | Enterprise Value, Assumed Debt, Refinanced Debt, Transaction Fees, OID, Min Cash |
| Sources of Funds | 11–16 | Senior Secured ($), Sub Debt ($), Preferred ($), Sponsor Equity ($, plug) |
| Operating | 18–24 | Revenue (Year 0), Revenue growth Y1–Y5, EBITDA margin Y1–Y5, D&A % rev, Capex % rev, ΔNWC % Δrev, Tax rate |
| Debt Detail | 26–32 | Per-tranche: Initial balance, Rate, Tenor (yrs), Amort %/yr, Mandatory paydown, Cash sweep flag |
| Exit | 34–37 | Exit year, Exit EBITDA multiple, Hold period |

All hardcoded input cells use **blue font (`Font(color="0000FF")`)**. Use the standard color coding throughout the workbook — see Domain Reference Section 2.

---

### Step 5 — Populate Sources & Uses

Layout: column B labels, column C values. Sources must equal Uses.

**Uses** (rows 4–8):
- Purchase Price = Assumptions Enterprise Value (cross-sheet link, **green font**)
- Refinanced Debt = Assumptions Refinanced Debt
- Transaction Fees = Assumptions Transaction Fees
- OID = Assumptions OID
- **Total Uses** = `=SUM(C4:C8)` (black font — formula)

**Sources** (rows 11–15):
- Senior Secured = Assumptions Senior Secured
- Sub Debt = Assumptions Sub Debt
- Preferred = Assumptions Preferred
- Sponsor Equity (the **plug**) = `=C9-SUM(C11:C13)` (Total Uses − the three sized tranches). Color this cell black (formula).
- **Total Sources** = `=SUM(C11:C14)` (black font)

**Balance check** (row 17): `=C15-C9` — must equal zero. Format as `$#,##0;($#,##0);"-"` so a non-zero variance is visible.

---

### Step 6 — Populate Operating Model

Layout: column B labels, column C is "Year 0" (LTM / pre-deal), columns D–H are "Year 1" through "Year 5".

Build downward from revenue to free cash flow available for debt paydown:

| Row | Item | Formula pattern (Year 1, column D) |
|-----|------|-----------------------------------|
| 4 | Revenue | `=C4*(1+Assumptions!D19)` — Year 0 × (1 + growth) |
| 5 | EBITDA | `=D4*Assumptions!D21` — Revenue × EBITDA margin |
| 6 | D&A | `=-D4*Assumptions!$C$23` — −1 × Revenue × D&A % |
| 7 | EBIT | `=D5+D6` |
| 8 | Interest Expense | `=-'Debt Schedule'!D[interest_row]` — link to debt schedule total |
| 9 | EBT | `=D7+D8` |
| 10 | Taxes | `=-MAX(0,D9)*Assumptions!$C$25` — apply tax rate only on positive EBT |
| 11 | Net Income | `=D9+D10` |
| 12 | + D&A (add back) | `=-D6` |
| 13 | − Capex | `=-D4*Assumptions!$C$24` |
| 14 | − ΔNWC | `=-(D4-C4)*Assumptions!$C$25` |
| 15 | **Free Cash Flow** | `=D11+D12+D13+D14` |
| 16 | − Mandatory Debt Paydown | `=-'Debt Schedule'!D[mandatory_row]` |
| 17 | **Cash Available for Sweep** | `=D15+D16` |

Copy the Year 1 column rightward across D–H using anchor references (`$C$23`, `$C$24`, etc. on the Assumptions cells, regular D references on adjacent operating-model cells).

The interest-expense and mandatory-paydown links point at the Debt Schedule — these create a forward reference that Excel resolves correctly because we use **beginning balance** for interest (see Step 7).

---

### Step 7 — Populate Debt Schedule

The debt schedule is one block per tranche (Senior Secured, Sub Debt, Preferred), then a summary row aggregating across tranches.

Per tranche (5 rows, then 1 blank):

| Item | Year 1 formula (column D) | Notes |
|------|---------------------------|-------|
| Beginning Balance | `=C[ending_row]` for Year 1; for Y2+ it's the prior-year ending of the same tranche | Use prior period — breaks circularity |
| Interest Expense | `=D[begin_row]*Assumptions!$C$[rate_cell]` | Computed on **beginning** balance, not ending |
| Mandatory Paydown | `=-MIN(D[begin_row], Assumptions!$C$[amort_cell]*Assumptions!$C$[initial_balance])` | MIN guards against paying more than outstanding |
| Optional Sweep | `=-MAX(0, MIN(D[begin_row]+D[mandatory_row], 'Operating Model'!D17))` for the senior tranche; lower tranches get the residual sweep after seniors are paid | Senior priority |
| Ending Balance | `=D[begin_row]+D[mandatory_row]+D[sweep_row]` | Cannot go negative — the MIN/MAX guards above prevent it |

**Critical: use beginning balance for interest, not ending or average.** Using ending balance creates a circular reference (Interest → Cash Flow → Paydown → Ending Balance → Interest). The PE-standard convention is beginning balance.

**Summary row** (one for the aggregate across all tranches):
- Total Interest = `=SUM(<each tranche's interest row>)`
- Total Mandatory Paydown = `=SUM(<each tranche's mandatory row>)`

These are the rows that `Operating Model!D8` and `Operating Model!D16` reference.

---

### Step 8 — Populate Returns

Compute exit equity value and sponsor returns. Layout: column B labels, column C "Entry" (Year 0), columns D–H "Year 1" through "Year 5".

| Row | Item | Formula |
|-----|------|---------|
| 4 | Exit EBITDA (year-by-year reference) | `='Operating Model'!D5` |
| 5 | Exit Multiple | `=Assumptions!$C$[exit_multiple]` (constant across years if held flat) |
| 6 | Enterprise Value at Exit | `=D4*D5` |
| 7 | Net Debt at Exit | `='Debt Schedule'!D[total_ending]` |
| 8 | **Equity Value at Exit** | `=D6-D7` |
| 9 | Initial Sponsor Equity | `='Sources & Uses'!$C$14` (negative for IRR convention) |
| 10 | Exit Year Marker | 1 if year = exit year else 0 |
| 11 | Sponsor Cash Flow | `=IF(D10=1, D8, 0)` for proceeds; entry equity outflow lives at row 9 column C as a negative value |

**IRR** at row 13: `=IRR(C[cash_flow_row]:H[cash_flow_row])` over the entry-to-exit cash flow series. Entry is negative, exit is positive.

**MOIC** at row 14: `=[exit equity proceeds]/(-[entry equity])`. Use signed numbers so the ratio is positive.

**Sensitivity tables** (optional): two 2-D sensitivity blocks — IRR by Exit Multiple × Exit Year, and IRR by Revenue Growth × Exit Multiple. Each cell is a formula that recomputes returns given the row/column inputs; see the Sensitivity Tables note in the Domain Reference.

---

### Step 9 — Apply Formatting Standards

Apply the conventions from Section 2 of the Domain Reference to every cell:

- Font colors: blue inputs, black formulas, purple same-tab links, green cross-tab links
- Number formats: `$#,##0;($#,##0);"-"` for dollars, `0.0%` for percentages, `0.0"x"` for multiples, `0.00"x"` for MOIC
- All numeric cells right-aligned
- Section headers: bold + bottom border (apply to row 1 of each tab plus each section divider row)
- Column widths: B = 32 (label column wider), C–H = 14

Save the workbook to `./<SANITIZED_COMPANY_NAME> - LBO Model.xlsx`.

---

### Step 10 — Verify

Run the verification checklist in Section 3 of the Domain Reference. The minimum checks:

- [ ] Sources & Uses balances exactly (Sources row − Uses row = 0)
- [ ] No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#CIRCULAR!` errors
- [ ] Debt Schedule ending balances are all ≥ 0
- [ ] Operating Model Free Cash Flow is reasonable order of magnitude
- [ ] Returns IRR and MOIC are positive (or negative if the deal is intentionally unprofitable for a stress case)
- [ ] Every input cell is blue, every formula cell is black/purple/green per the color convention

If `python /mnt/skills/public/xlsx/recalc.py "$OUTPUT"` is available in the Claude Code environment, run it for a full recalc + error scan. If not, skip — the manual checks above cover the same ground.

---

### Step 11 — Report

Tell the user:
- The output file path
- The plug Sponsor Equity dollar amount (so they can sanity-check the cap structure)
- Headline IRR and MOIC at the base case
- Any assumptions you defaulted (tax rate, min cash, sweep priority) — they may want to override
- Reminder: open in Excel to see live recalc; the entire model is formula-driven, so changing any assumption updates everything downstream

---

## Domain Reference

### 1 — Tab Cell Maps

Each tab uses column B for labels and column C onward for values / years. The exact rows depend on how many debt tranches the user specifies — the tables above use a typical 3-tranche structure (Senior + Sub + Preferred). If the user provides more tranches, expand the Debt Schedule block-by-block following the same pattern.

### 2 — Formula Color Conventions

| Color | Meaning | Example |
|-------|---------|---------|
| **Blue** (`Font(color="0000FF")`) | Hardcoded input — typed number, no cell reference | `0.25` for 25% tax rate |
| **Black** (`Font(color="000000")`) | Formula with calculation | `=B4*B5`, `=SUM(C4:C8)`, `=-MAX(0,B4)` |
| **Purple** (`Font(color="800080")`) | Same-tab direct link (no calculation) | `=B9`, `=$C$25` |
| **Green** (`Font(color="008000")`) | Cross-tab direct link | `=Assumptions!C19`, `='Operating Model'!D5` |

The color tells the reviewer at a glance whether a cell is an input they can edit (blue) or downstream output they should not (everything else).

### 3 — Number Formatting Standards

| Type | Format string | Examples |
|------|---------------|----------|
| Dollar | `$#,##0;($#,##0);"-"` or `$#,##0.0` | $1,234, ($567), $1,234.5 |
| Percent | `0.0%` | 25.0%, (3.5%) |
| Multiple (EBITDA, EV) | `0.0"x"` | 8.5x |
| MOIC / detailed ratio | `0.00"x"` | 2.45x |
| Year | `0` or `"Year "0` | 2024, Year 1 |

All numeric cells right-aligned. Label cells (column B) left-aligned.

### 4 — Common Problem Areas

**Balancing sections.** When two sections must equal (Sources = Uses), one item is the "plug" calculated as the difference. In an LBO that's almost always **Sponsor Equity** — every other source is sized, and the equity fills whatever's left. Calculate it as `Total Uses − sum of other sources`.

**Tax calculations.** Tax formula should reference EBT (earnings before tax) and the tax-rate cell only. Do not reference unrelated sections like debt. Use `=-MAX(0, EBT)*tax_rate` so losses don't generate negative taxes (in a simple LBO model — more sophisticated models handle NOL carryforwards explicitly).

**Interest and circular references.** Interest calculated on **beginning balance** breaks the circularity that would otherwise loop Interest → Cash Flow → Paydown → Ending Balance → Interest. This is the PE-standard convention. Average balance is more accurate but requires Excel's iterative calculation enabled, which most reviewers won't have on.

**Debt paydown / cash sweeps.** When multiple tranches exist, the sweep waterfall is **senior first**. Each tranche gets `MIN(beginning_balance + mandatory_paydown, available_sweep_cash)`. Available sweep = FCF − mandatory paydowns − minimum cash. Lower tranches get the residual after seniors are paid. Use `MAX(0, ...)` to clamp at zero so balances can't go negative.

**Returns calculations.**
- Cash flow signs: entry equity is **negative**, exit proceeds are **positive**
- IRR over the entry-to-exit cash flow series: `=IRR(C[row]:H[row])` where C is entry (negative) and the exit-year column is the positive exit equity (zeros elsewhere)
- MOIC = Total Proceeds / Total Invested = `=exit_equity / -entry_equity` (signed so the result is positive)
- For dividend recaps mid-hold, add interim positive cash flows to the IRR range

**Sensitivity tables.** Excel's native DATA TABLE function doesn't survive openpyxl writes — the DATATABLE formulas drop. Build sensitivities as **explicit formulas** that reference row and column input cells:
- Row input across columns D–H (e.g., exit multiples 7.0x, 8.0x, 9.0x, 10.0x, 11.0x)
- Column input down rows 4–8 (e.g., exit years 3, 4, 5, 6, 7)
- Each data cell: `=IRR(...with row/column inputs substituted in...)` using mixed references (`$A5` for row, `B$4` for column) so copy-fill works
- **Sanity check:** every data cell should show a different value. If they're all identical, the references aren't varying — likely missing `$` anchors.

### 5 — Common Errors to Avoid

| Error | Symptom | Fix |
|-------|---------|-----|
| Hardcoded calculated values | Model doesn't update when inputs change | Always use formulas referencing source cells |
| Circular reference on interest | Excel shows `#CIRCULAR!` or zeros | Use **beginning** balance for interest, not ending |
| Sources ≠ Uses | Balance check shows non-zero | Sponsor Equity must be the plug = `Total Uses − sum(other sources)` |
| Negative debt balances | Ending balance < 0 | Wrap paydowns in `MIN(balance, paydown)` and `MAX(0, sweep)` |
| Wrong cash flow signs in IRR | IRR formula returns `#NUM!` or implausible value | Entry equity negative, exit equity positive, zeros in between |
| Sensitivity table shows same value | All cells identical regardless of input | Mixed references — `$A5` (row), `B$4` (column); not all-absolute, not all-relative |
| Inconsistent tax sign | Net income drifts from EBT | Tax = `=-MAX(0, EBT)*rate` (negative outflow) |
| Roll-forward doesn't tie | Beginning Year 2 ≠ Ending Year 1 | Explicit cross-period link — don't rely on copy-fill alone |

### 6 — Full Verification Checklist

After Step 9 saves the workbook, run through:

**Section balancing**
- [ ] Sources − Uses = 0 (Sources & Uses tab balance row)
- [ ] Every per-tranche debt block: Beginning + Mandatory + Sweep = Ending

**Income / operating projections**
- [ ] Revenue builds from Year 0 × (1 + growth) chain
- [ ] EBITDA margin × Revenue produces EBITDA
- [ ] Tax = `-MAX(0, EBT)*rate` — no negative taxes
- [ ] FCF = NI + D&A − Capex − ΔNWC
- [ ] Cash Available for Sweep = FCF − Mandatory Paydown

**Debt schedule**
- [ ] Year 1 Beginning Balance = Sources & Uses tranche size
- [ ] Year N Beginning = Year (N−1) Ending for every tranche
- [ ] Interest = Beginning × Rate (not Ending, not Average)
- [ ] Mandatory paydown clamped at outstanding balance
- [ ] Sweep waterfall: senior gets first claim; subordinated gets residual
- [ ] No ending balance < 0

**Returns**
- [ ] Entry Sponsor Equity is negative (the IRR convention)
- [ ] Exit proceeds appear only in the exit-year column
- [ ] IRR formula range covers entry through exit year
- [ ] MOIC = exit equity / |entry equity|, returns a positive ratio

**Formatting**
- [ ] Blue text on every hardcoded input
- [ ] Black on formulas, purple on same-tab links, green on cross-tab links
- [ ] No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#CIRCULAR!` anywhere
- [ ] Numbers right-aligned, formats applied per Section 3

**Logical sanity**
- [ ] Order of magnitude reasonable (a $500M deal shouldn't produce a $5B exit equity)
- [ ] IRR within plausible PE range (typically 15–35%; flag anything outside)
- [ ] Multiples consistent (entry and exit usually within 1–2 turns of each other unless intentional multiple expansion)

### 7 — When to Ask the User

- **Template structure unclear** — if the user gave a partial structure but you can't fill in the gaps, ask before guessing
- **Operating projections missing details** — if margins or growth are flat-lined or unstated, propose a default (e.g., 8% revenue growth tapering to 4%) and confirm
- **Capital structure ambiguous** — if the user says "75% debt" without specifying tranches, propose a default split (50% senior, 25% sub) and confirm before building
- **Sensitivity tables not requested** — sensitivities are optional; skip them unless asked

When in doubt, offer to show the assumptions sheet for review before building the rest. The user can override anything in blue, and the model recalculates automatically.
