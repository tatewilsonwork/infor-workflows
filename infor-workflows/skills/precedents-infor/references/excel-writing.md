# Writing the Precedents Workbook (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

Write to the `Sheet1` sheet only. **Write up to 15 data rows, rows 7 through 21, in the specific columns listed below. Touch no other cells.**

## Cell Map

For each populated row N (where N is between 7 and 21):

| Column | Field | Python type | Notes |
|--------|-------|-------------|-------|
| B | Input Currency | `str` | ISO 3-letter code, e.g. `"USD"`, `"CAD"`, `"GBP"`, `"EUR"`, `"AUD"` |
| E | Announce Date | `datetime.date` | Use `datetime.date(YYYY, M, D)` |
| F | Target Legal Name | `str` | Full legal name of target company |
| G | Acquiror Legal Name | `str` | Full legal name of acquiror |
| H | HQ Country Code | `str` | ISO 2-letter country code (e.g., `"CA"`, `"US"`, `"GB"`) |
| I | Deal Value (TEV) | **formula string** | `f"={raw_tev}*C{row}"` — raw value in $MM of input currency. Attach a Quote + Source comment (Format A) |
| J | EBITDA | **formula string** or unset | See formula precedence below. Format A or B comment depending on rung |
| K | Revenue | **formula string** or unset | Same precedence as EBITDA |
| N | Target Description | `str` | ≤50 characters — see description rules below |

## FX Conversion — Critical

Cells I, J, and K are written as **formulas** that multiply the raw source-currency $MM value by the FX conversion in column C of the same row. Column C is a CapIQ array formula (`C7:C21`) that returns the rate from input currency (column B) to output currency (`$H$2`).

**FX is applied exactly once:**
- $ LTM figures and stub-period figures are in **input currency**, so the formula multiplies by `C{row}` to convert.
- A disclosed multiple is **dimensionless**, and `I{row}` is already in **output currency** (its own formula did the FX). Dividing `I{row}` by a multiple yields output-currency $MM directly. Adding `*C{row}` would double-apply FX. **Never write `=I7/12.5*C7`.** The multiple-derived formula is `=I7/<multiple>` — full stop.

## Formula Precedence by Source Rung

### Rung 1 — Disclosed $ LTM (preferred path)

Row 7 is a deal whose press release / 8-K discloses LTM Revenue of CAD 880 MM and LTM EBITDA of CAD 195 MM:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=195*C7"              # disclosed LTM EBITDA
ws['K7'] = "=880*C7"              # disclosed LTM Revenue
```

### Rung 2 — Disclosed Multiple (when no $ LTM is disclosed)

Same row, deal source quotes 12.5x LTM EBITDA and 2.8x LTM Revenue:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"             # TEV in output currency after FX
ws['J7'] = "=I7/12.5"             # EBITDA = TEV / 12.5x — no *C7 (I7 already converted)
ws['K7'] = "=I7/2.8"              # Revenue = TEV / 2.8x — no *C7 either
```

### Rung 3 — Calculated Stub (public-target fallback only)

Same TEV but LTM is built from filings:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=(45+180-42)*C7"      # LTM EBITDA = Q1 current + FY prior - Q1 prior
ws['K7'] = "=(220+850-205)*C7"    # LTM Revenue = same stub convention
```

When the workbook is opened in Excel with the CapIQ add-in active, C7 resolves to the FX rate and I/J/K display the values in the output currency set in `H2`. Do **not** pre-convert the values yourself, and do **not** pre-sum the LTM stubs in Python — write each stub into the formula in source currency and let Excel handle both the LTM math and the FX conversion.

## Source Comments — Required on Every Written I / J / K Cell

If a cell is left unset because the metric is undisclosed, do not attach a comment. Otherwise pick the format by source-path:

### Format A — Quote + Source

Used for column I (TEV) and for any J/K cell whose formula has a single operand (disclosed $ LTM rung 1, disclosed multiple rung 2, FY-only / Q4, disclosed non-LTM private $ figure rung 4). Two-block format with a blank line between:

```
Quote: "<short verbatim quote from the source containing the figure or multiple>"

Source: <URL>
```

- The quote must be **verbatim from the source** — do not paraphrase. Copy the sentence or clause that directly supports the figure or multiple. Keep it short (one or two clauses, typically under 200 characters).
- Always close the quote with `"`. If the verbatim text contains a colon, em dash, or other punctuation, preserve it inside the quotes.
- One blank line between Quote and Source.
- The Source line is a single URL pointing to the specific document the quote was taken from.

### Format B — Multi-Stub Labeled Lines

Used **only** for the calculated LTM stub-calc case (rung 3, 3-operand formula `=(mrq+fy-pyq)*C{row}`). One line per stub, no Quote prefix:

```
<Period> ($<Value>): <URL>
```

- 3 lines: MRQ first, then FY, then PYQ.
- One URL per stub. If the same filing covers two stubs (e.g., a 10-Q whose period table also shows the prior-year comparable), repeat that URL on both stub lines — do not consolidate.

This per-stub labeled format is preserved for the multi-source case so a reviewer can map each operand of the formula directly to its source filing.

## Comment Examples

```python
from openpyxl.comments import Comment

# TEV (column I) — Format A
ws['I7'] = "=6000*C7"
ws['I7'].comment = Comment(
    'Quote: "OpenText agreed to acquire Micro Focus for $6.0 billion in total enterprise value"\n'
    '\n'
    'Source: https://investors.opentext.com/press-releases/press-releases-details/2023/OpenText-Buys-Micro-Focus/default.aspx',
    "Source"
)

# K (Revenue) from a disclosed multiple — Format A; formula references I, no *C{row}
ws['K7'] = "=I7/2.3"
ws['K7'].comment = Comment(
    'Quote: "Total purchase price is 2.3x Micro Focus\' TTM revenues"\n'
    '\n'
    'Source: https://investors.opentext.com/press-releases/press-releases-details/2023/OpenText-Buys-Micro-Focus/default.aspx',
    "Source"
)

# J (EBITDA) from a disclosed $ LTM — Format A
ws['J7'] = "=85.0*C7"
ws['J7'].comment = Comment(
    'Quote: "Reported LTM Adjusted EBITDA of $85.0 million"\n'
    '\n'
    'Source: https://example.com/deal-press-release.htm',
    "Source"
)

# J (EBITDA) from a calculated LTM stub — Format B
ws['J7'] = "=(17.517+84.720-17.665)*C7"
ws['J7'].comment = Comment(
    "Q1 2025 ($17.517): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/\n"
    "FY2024 ($84.720): https://www.globenewswire.com/news-release/2025/02/26/3032731/37161/en/AvidXchange-Announces-Fourth-Quarter-Full-Year-2024-Financial-Results.html\n"
    "Q1 2024 ($17.665): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/",
    "Source"
)
```

Notes:
- The second `Comment(...)` argument is the comment author and is not the comment body — Excel only displays the first argument.
- Use `\n` between every line break and `\n\n` for the blank line between Quote and Source in Format A. In Excel, the blank line gives the comment readable separation.
- Escape apostrophes in the Python string literal as needed (`Focus\'` inside a single-quoted string, or use a double-quoted string for the outer literal).

## Cells That Must NOT Be Touched

- C7:C21 — CapIQ FX array formulas
- L7:L21 and M7:M21 — TEV/EBITDA and TEV/Revenue ratio formulas
- D, anything outside rows 7–21, or any cell in row 23 (averages)

## Description Rules (Column N)

Column N has a width of ~50 — descriptions that exceed this will overflow visually.

- Describe **what the company does or sells** — product, service, asset class, client segment, or business model
- **Do not include geography** — country is already captured in column H
- Target 35–50 characters; never exceed 50
- No trailing punctuation; title case preferred
- Examples:
  - `"Diversified multi-asset & alternatives manager"` (47)
  - `"Independent wealth advisory platform"` (37)
  - `"Mid-market private credit manager"` (33)
  - `"SaaS-based insurance distribution platform"` (43)
  - `"Life and health insurance provider"` (35)

## Missing Values

If EBITDA or Revenue is undisclosed for a transaction, **skip writing that cell entirely** — do not write `None`, `""`, or `0`. Just leave it unset so the column-L / column-M ratio formula returns `"n/a "` via `IFERROR`.

## Number of Rows

Populate as many rows as you have well-sourced transactions, up to 15. Do not fabricate transactions to fill the table — fewer high-quality rows is better than padding.

## Trim Empty Rows Before Saving — Required When Fewer Than 15 Transactions

After writing all rows, delete any unused data rows so the table ends at the last populated transaction and flows directly into the averages row. Visually-blank rows above the averages row are not acceptable in the deliverable.

```python
n = number_of_transactions_written         # rows 7 through 7+n-1 are populated
if n < 15:
    first_empty_row = 7 + n
    rows_to_drop = 15 - n
    ws.delete_rows(idx=first_empty_row, amount=rows_to_drop)
```

`ws.delete_rows` shifts cells below the deletion up and updates relative-reference formulas accordingly — the L/M averages row that started at row 23 moves to row `23 - rows_to_drop`, and `AVERAGE(L7:L21)` / `AVERAGE(M7:M21)` collapse to the populated range. After saving, re-open and confirm the averages row references the correct data range and is not `#REF!`. If it is, rewrite explicitly:

```python
new_avg_row = 23 - rows_to_drop
last_data_row = 7 + n - 1
ws.cell(row=new_avg_row, column=12).value = f'=IFERROR(AVERAGE(L7:L{last_data_row}),"n/a ")'  # column L
ws.cell(row=new_avg_row, column=13).value = f'=IFERROR(AVERAGE(M7:M{last_data_row}),"n/a ")'  # column M
```

(The exact form of the original averages formula may differ — preserve `IFERROR(...,"n/a ")` wrapping if it was present.)

If the column-C CapIQ formula in the template is a single multi-cell array spanning C7:C21, deleting rows from inside that array can produce a `#REF!` in Excel. The column-C formulas in this template are per-cell (one CIQ call per row), so `delete_rows` works cleanly — but if a `#REF!` appears in column C of a remaining row during Step 6 verification, that's the diagnosis.
