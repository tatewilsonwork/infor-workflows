---
name: precedents-infor
description: >
  Use this skill when the user asks to build a precedent transactions table for a company.
  Researches up to 15 relevant M&A precedent transactions — prioritising publicly traded
  targets at the time of acquisition (where Revenue and EBITDA are verifiable from filings) —
  with private targets included only when multiples or Revenue/EBITDA are disclosed in
  acquiror press releases or reputable sources, and populates the INFOR Precedents Template.
version: 1.9.8
---

# INFOR Precedent Transactions Table — Workflow

This skill builds a precedent transactions table by researching up to 15 relevant M&A deals and writing the transaction data into the INFOR Precedents Template (rows 7–21, specific columns only — see the cell map).

Allowed tools: Read, Bash, Write, Glob, WebSearch

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. Template location, outputs folder, and working directory are resolved inline in Step 4.

---

## Workflow Steps

### Step 1 — Confirm Company

If the company name or website was not passed with the command, ask:

> "Please provide the name or website of the company you'd like me to build a precedent transactions table for."

Wait for the company before proceeding.

---

### Step 2 — Determine Sector

Identify the **sector / business type** of the target company (e.g., wealth management, insurance, SaaS, industrial). Use WebSearch to confirm if it isn't obvious from the name or website. The sector drives the search queries in Step 3.

---

### Step 3 — Research Up to 15 Precedent Transactions

Search for up to 15 relevant M&A transactions where the **target company** is comparable to the input company.

**Selection priority — public targets first:**

1. **Publicly traded targets at the time of acquisition** (strongly preferred). Their pre-deal annual filings (10-K, 20-F, AIF, annual MD&A) make Revenue and EBITDA directly verifiable.
2. **Private targets with disclosed multiples** in the acquiror's deal press release, investor deck, or reputable financial news (e.g., "acquired at ~12x EBITDA" or "~3x Revenue").
3. **Private targets with disclosed absolute Revenue and/or EBITDA** in the acquiror's PR or reputable news (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global).

Never include a transaction where deal value (TEV) is undisclosed — a blank TEV makes the row unusable for multiple analysis.

**Search strategy — run several targeted queries, biased toward public targets:**
- `"[sector] acquisition [year range] public company target 10-K revenue EBITDA"`
- `"[target name] acquired [year] 10-K annual report"` (for known public targets)
- `"[acquiror] acquires [target] press release LTM revenue EBITDA"`
- `"[sector] M&A [year range] disclosed multiples EBITDA revenue"`
- `"[company name] comparable transactions precedents investment banking"`

**For each candidate transaction — retrieve financials as follows:**
- **Public target:** pull Revenue and EBITDA from the most recent annual filing (10-K, 20-F, AIF, annual MD&A) before the announcement date. Use the LTM figure as of the announcement quarter where available; otherwise use the most recent fiscal year. EBITDA = Operating Income + D&A from the cash flow statement (or Adjusted EBITDA if disclosed and consistent with peers).
- **Private target — disclosed metrics:** look in the acquiror's deal press release, investor presentation, or reputable financial news for explicit "$X revenue" / "$X EBITDA" / "Xx multiple" language.
- **Private target — multiples only:** if only TEV/EBITDA or TEV/Revenue is disclosed (and TEV is known), back into the implied EBITDA or Revenue and record that derived value. Note in your summary that the figure is implied from a disclosed multiple.

**Selection criteria:**
- Similar sector / business model to the input company
- Announced or completed within the last 6–8 years (prefer recent deals)
- Disclosed deal value (TEV) — **required**
- Disclosed Revenue and/or EBITDA — required for public targets; private targets require either disclosed metrics or a disclosed multiple from which a value can be inferred

**Source discipline — this is critical:**
- All financial figures must come from: (1) target company filings (10-K, 20-F, AIF, annual MD&A), (2) acquiror deal press releases or investor decks, or (3) reputable financial news (Bloomberg, Reuters, Globe and Mail, Financial Post, WSJ, S&P Global).
- Do not fabricate or estimate financial metrics. If a figure cannot be verified after a thorough search, leave the cell blank.
- Aim for at least 80% of selected transactions to have disclosed Revenue and EBITDA (public-target priority makes this easy to hit).

**Currency:** Use the currency as stated in the original source — TEV, EBITDA, and Revenue must all be in the **same currency**, matching the ISO 3-letter code entered in column B (e.g., `"USD"`, `"CAD"`, `"GBP"`). The template's column C FX formula converts to the output currency, and our formulas in I/J/K (see Step 5) apply that conversion automatically.

---

### Step 4 — Locate and Copy the Template

Locate the template dynamically:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Precedents Template.xlsx" 2>/dev/null | head -1
```

Resolve the output folder:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); echo "${REPO_ROOT:-.}/outputs"
```

Sanitize the company name for use as a filename (remove special characters, replace spaces with hyphens).

Create the outputs folder if it doesn't exist, then copy the template:
```bash
mkdir -p "[outputs_folder]"
cp "[template_path]" "[outputs_folder]/[SANITIZED_COMPANY_NAME] - Precedent Transactions.xlsx"
```

Confirm the copy succeeded before proceeding.

---

### Step 5 — Write Transaction Data to Excel (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

Write to the `Sheet1` sheet only. **Write up to 15 data rows, rows 7 through 21, in the specific columns listed below. Touch no other cells.**

For each populated row N (where N is between 7 and 21), write the following:

| Column | Field | Python type | Notes |
|--------|-------|-------------|-------|
| B | Input Currency | `str` | ISO 3-letter code, e.g. `"USD"`, `"CAD"`, `"GBP"` |
| E | Announce Date | `datetime.date` | Use `datetime.date(YYYY, M, D)` |
| F | Target Legal Name | `str` | Full legal name of target company |
| G | Acquiror Legal Name | `str` | Full legal name of acquiror |
| H | HQ Country Code | `str` | ISO 2-letter country code (e.g., `"CA"`, `"US"`, `"GB"`) |
| I | Deal Value (TEV) | **formula string** | `f"={raw_tev}*C{row}"` — raw value in $MM of input currency |
| J | EBITDA | **formula string** or unset | `f"={raw_ebitda}*C{row}"`; leave unset if undisclosed |
| K | Revenue | **formula string** or unset | `f"={raw_revenue}*C{row}"`; leave unset if undisclosed |
| N | Target Description | `str` | ≤50 characters — see description rules below |

**FX conversion — critical:**

Cells I, J, and K are written as **formulas** that multiply the raw source-currency $MM value by the FX conversion in column C of the same row. Column C is a CapIQ array formula (`C7:C21`) that returns the rate from input currency (column B) to output currency (`$H$2`).

For example, if the source data for row 7 is TEV of CAD 1,250 MM, EBITDA of CAD 180 MM, Revenue of CAD 850 MM:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=180*C7"
ws['K7'] = "=850*C7"
```

When the workbook is opened in Excel with the CapIQ add-in active, C7 resolves to the FX rate and I/J/K display the values in the output currency set in `H2`. Do **not** pre-convert the values yourself — write the source-currency number into the formula and let Excel handle FX.

**Do NOT touch any other column.** In particular, do not write to:
- C7:C21 — CapIQ FX array formulas
- L7:L21 and M7:M21 — TEV/EBITDA and TEV/Revenue ratio formulas
- D, anything outside rows 7–21, or any cell in row 23 (averages)

**Description rules (column N):**
- Column N has a width of ~50 — descriptions that exceed this will overflow visually
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

**Writing missing values:** If EBITDA or Revenue is undisclosed for a transaction, **skip writing that cell entirely** — do not write `None`, `""`, or `0`. Just leave it unset so the column-L / column-M ratio formula returns `"n/a "` via `IFERROR`.

**Number of rows:** Populate as many rows as you have well-sourced transactions, up to 15. Do not fabricate transactions to fill the table — fewer high-quality rows is better than padding. Leave unused rows (B/E/F/G/H/I/J/K/N) blank.

Save the file after writing all rows.

---

### Step 6 — Verify Output

After saving, re-open the file and spot-check:
1. Each populated row has values in B, E, F, G, H, I, and N
2. Dates in column E are `datetime.date` objects (not strings)
3. Cells I, J, K start with `=` and reference `C{same_row}` (i.e., they are formulas, not raw numbers)
4. Column N values are all ≤50 characters
5. No values were written to columns C, D, L, M, or any column past N
6. No values were written outside rows 7–21

Report any issues found and fix before delivering.

---

### Step 7 — Summary

Report to the user:

1. **Output file:** computer:// link to the saved file
2. **Transactions populated:** list of deals with target, acquiror, deal value, and a `[Public]` or `[Private]` tag for the target's status at announcement
3. **Source mix:** how many public-target vs. private-target rows are included; for any private-target row, briefly note whether financials are directly disclosed or implied from a disclosed multiple
4. **Missing data:** note any EBITDA or Revenue cells left blank due to non-disclosure
5. **Sources:** brief summary of where financial figures were sourced (filings vs. acquiror PRs vs. news)
6. **Reminder:** Open in Excel with the CapIQ add-in active — column C (FX rate) will populate, and columns I/J/K formulas will resolve to output-currency $MM. Columns L/M (multiples) and row 23 (averages) auto-calculate.

---

## Domain Reference

### Template Cell Map — Sheet1

| Cells | Purpose | Notes |
|-------|---------|-------|
| H2 | Output currency (CAD or USD) | Pre-set in template; do not modify |
| B7:B21 | Input currency (ISO code) | **Write here** |
| C7:C21 | FX conversion — CapIQ array formula | **Never overwrite** |
| E7:E21 | Announce date | **Write here** (`datetime.date`) |
| F7:F21 | Target legal name | **Write here** |
| G7:G21 | Acquiror legal name | **Write here** |
| H7:H21 | Target HQ country code (ISO 2-letter) | **Write here** |
| I7:I21 | Deal Value (TEV) | **Write here as formula** `=raw*C{row}` |
| J7:J21 | EBITDA | **Write here as formula** `=raw*C{row}` |
| K7:K21 | Revenue | **Write here as formula** `=raw*C{row}` |
| L7:L21 | TEV / EBITDA | **Never overwrite — formula** |
| M7:M21 | TEV / Revenue | **Never overwrite — formula** |
| N7:N21 | Target description (≤50 chars) | **Write here** |
| L23, M23 | Averages of multiples | **Never overwrite — formula** |

### Column Reference

| Col | Header | Type | Unit |
|-----|--------|------|------|
| B | Input Currency | String | ISO code (USD/CAD/GBP/EUR/AUD) |
| C | FX Conversion | Formula | CapIQ — do not write |
| E | Announce Date | Date | — |
| F | Target | String | — |
| G | Acquiror | String | — |
| H | Target HQ | String | ISO 2-letter (CA, US, GB, AU, etc.) |
| I | TEV | Formula | `=raw*C{row}` — raw in $MM of column B currency |
| J | EBITDA | Formula | `=raw*C{row}`; blank if undisclosed |
| K | Revenue | Formula | `=raw*C{row}`; blank if undisclosed |
| L | TEV / EBITDA | Formula | Auto-calculated — do not write |
| M | TEV / Revenue | Formula | Auto-calculated — do not write |
| N | Target Description | String | ≤50 chars |

### Precedent Transaction Research Tips

**Good search queries (public-target priority):**
- `"[target name] 10-K [year] revenue EBITDA"`
- `"[target name] 20-F annual report"` (for non-US public targets)
- `"[sector] public company acquisition [year range] press release"`
- `"[acquiror] acquires [target] press release financial highlights"`
- `"[sector] M&A transaction multiple disclosed EBITDA"`

**Verifying financial figures — ranked by reliability:**
1. Target's own annual filing (10-K, 20-F, AIF, annual MD&A) — income statement gives Revenue; EBITDA = Operating Income + D&A from cash flow statement
2. Acquiror's deal announcement press release — often states "LTM Revenue of $X" and "Adjusted EBITDA of $X" to justify valuation
3. Acquiror's investor presentation or deal supplement filed with the announcement
4. Bloomberg, Reuters, Financial Post, or WSJ deal coverage that quotes disclosed metrics

**HQ country codes — common examples:**

| Country | Code | Country | Code |
|---------|------|---------|------|
| Canada | CA | Australia | AU |
| United States | US | France | FR |
| United Kingdom | GB | Germany | DE |
| Ireland | IE | Netherlands | NL |

**Handling undisclosed metrics:**
- Never include a deal with no deal value — TEV must be populated for the row to be useful
- For public targets, Revenue and EBITDA should always be findable from filings — do not leave them blank
- For private targets, write only the metrics that are directly disclosed or cleanly implied from a disclosed multiple; leave the rest blank
- Aim for at least 80% of selected transactions to have both Revenue and EBITDA populated
