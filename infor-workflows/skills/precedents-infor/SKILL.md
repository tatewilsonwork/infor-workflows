---
name: precedents-infor
description: >
  Use this skill when the user asks to build a precedent transactions table for a company.
  Researches up to 15 relevant M&A precedent transactions — with a mild preference for
  publicly traded targets at the time of acquisition (where Revenue and EBITDA are verifiable
  from filings), but a closer-comparable private target with disclosed metrics or multiples
  should be selected over a weakly comparable public one. Populates the INFOR Precedents Template.
version: 2.1.0
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

**Selection priority — comparability first, public targets as a mild tiebreaker:**

The strongest precedent is a transaction whose **target business closely resembles the input company** (sector, business model, client segment, asset class, scale). Public-target deals are mildly preferred because their financials are directly verifiable from filings — but a clearly closer-comparable **private** target with disclosed metrics or multiples should be selected over a weakly comparable public one.

Categories, in rough order of preference when comparability is roughly equal:

1. **Publicly traded targets at the time of acquisition.** Their pre-deal annual filings (10-K, 20-F, AIF, annual MD&A) make Revenue and EBITDA directly verifiable. Default tiebreaker when business-model fit is similar.
2. **Private targets with disclosed multiples** in the acquiror's deal press release, investor deck, or reputable financial news (e.g., "acquired at ~12x EBITDA" or "~3x Revenue").
3. **Private targets with disclosed absolute Revenue and/or EBITDA** in the acquiror's PR or reputable news (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global).

When choosing between candidates, weigh comparability (sector / business model / segment / scale) more heavily than public-vs-private status. Recency and disclosure quality are secondary tiebreakers. Do **not** include a thin or off-sector public deal just to fill the public quota when a tighter-fit private deal is available.

Never include a transaction where deal value (TEV) is undisclosed — a blank TEV makes the row unusable for multiple analysis.

**Search strategy — run several targeted queries across both public and private deals:**
- `"[sector] acquisition [year range] public company target 10-K revenue EBITDA"`
- `"[target name] acquired [year] 10-K annual report"` (for known public targets)
- `"[acquiror] acquires [target] press release LTM revenue EBITDA"`
- `"[sector] M&A [year range] disclosed multiples EBITDA revenue"`
- `"[company name] comparable transactions precedents investment banking"`

**For each candidate transaction — Revenue and EBITDA must be on an LTM (last-twelve-months) basis ending the most recent quarter before the announcement date.** Do **not** default to the last fiscal-year figure when a more recent quarter has been reported.

**LTM stub-period formula:**

> **LTM = YTD_MRQ + FY_prior − YTD_PYQ**

…where `YTD_MRQ` is year-to-date through the most recent reported quarter before announcement, `FY_prior` is the most recent completed fiscal year, and `YTD_PYQ` is the matching year-to-date stub from the prior year. The two YTD stubs must cover the **same calendar period** (Q1 vs. Q1, H1 vs. H1, 9M vs. 9M).

| MRQ before announce | YTD stubs to pull |
|---|---|
| Q1 | Q1 current vs. Q1 prior |
| Q2 | H1 current vs. H1 prior |
| Q3 | 9M current vs. 9M prior |
| Q4 | No stub calc — `LTM = FY` (use the 10-K directly) |

Worked example — AvidXchange acquired by TPG / Corpay, announced May 6, 2025. Most recent reported quarter is Q1 2025 (released May 7 — but Q1 had ended March 31, so the LTM convention uses Q1 stubs):
- LTM Revenue = Q1 2025 ($107.9) + FY 2024 ($438.94) − Q1 2024 ($105.6)
- LTM EBITDA = Q1 2025 ($17.517) + FY 2024 ($84.720) − Q1 2024 ($17.665)

**For each candidate transaction — retrieve the stub figures as follows:**
- **Public target:** pull each stub from its own filing — the most recent 10-Q / 6-K / interim MD&A (`YTD_MRQ`), the most recent 10-K / 20-F / AIF (`FY_prior`), and the prior-year 10-Q / 6-K / interim MD&A for the same calendar quarter (`YTD_PYQ`). Apply the same EBITDA definition (Operating Income + D&A from cash flow statement, or Adjusted EBITDA if consistently disclosed) to all three stubs. If MRQ is Q4, no stub calc is needed — use the 10-K's full-year figures.
- **Private target — disclosed metrics:** look in the acquiror's deal press release, investor presentation, or reputable financial news for explicit "$X revenue" / "$X EBITDA" / "Xx multiple" language. Treat the disclosed figure as LTM if the source labels it that way; otherwise record the period the source quotes (e.g., FY 2023, calendar 2024). For private targets, **timing can drift by several months but never by years** — get as close to LTM as the disclosed data allows. If the only available figure is two-plus years stale, do not include the deal.
- **Private target — multiples only:** if only TEV/EBITDA or TEV/Revenue is disclosed (and TEV is known), back into the implied EBITDA or Revenue and record that derived value. Note in your summary that the figure is implied from a disclosed multiple.

**Excel does the math, not you.** Stub values must be written into the cell formula (see Step 5) — never pre-sum the stubs in Python and write a single number.

**Selection criteria:**
- Similar sector / business model to the input company
- Announced or completed within the last 6–8 years (prefer recent deals)
- Disclosed deal value (TEV) — **required**
- Disclosed Revenue and/or EBITDA — required for public targets; private targets require either disclosed metrics or a disclosed multiple from which a value can be inferred

**Source discipline — this is critical:**
- All financial figures must come from: (1) target company filings (10-K, 20-F, AIF, annual MD&A), (2) acquiror deal press releases or investor decks, or (3) reputable financial news (Bloomberg, Reuters, Globe and Mail, Financial Post, WSJ, S&P Global).
- Do not fabricate or estimate financial metrics. If a figure cannot be verified after a thorough search, leave the cell blank.
- Aim for at least 80% of selected transactions to have disclosed Revenue and EBITDA. The mild public-target preference helps hit this, but do not sacrifice comparability to do so — a tightly-fit private deal with one disclosed metric is more useful than an off-sector public deal with both.

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
| I | Deal Value (TEV) | **formula string** | `f"={raw_tev}*C{row}"` — raw value in $MM of input currency. Attach a single bare-URL source comment |
| J | EBITDA | **formula string** or unset | LTM stub calc — `f"=({mrq}+{fy}-{pyq})*C{row}"` (e.g., `"=(17.517+84.720-17.665)*C7"`). FY-only / Q4 announcement — `f"={fy}*C{row}"`. Disclosed-metric private target — `f"={value}*C{row}"`. Leave unset if undisclosed. Attach a labeled multi-line source comment (see below) |
| K | Revenue | **formula string** or unset | Same LTM convention as EBITDA. Leave unset if undisclosed. Attach a labeled multi-line source comment |
| N | Target Description | `str` | ≤50 characters — see description rules below |

**FX conversion — critical:**

Cells I, J, and K are written as **formulas** that multiply the raw source-currency $MM value by the FX conversion in column C of the same row. Column C is a CapIQ array formula (`C7:C21`) that returns the rate from input currency (column B) to output currency (`$H$2`).

For example, if the source data for row 7 is a deal announced in Q2 with TEV of CAD 1,250 MM, LTM EBITDA stubs of (CAD 45 + 180 − 42) MM and LTM Revenue stubs of (CAD 220 + 850 − 205) MM:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=(45+180-42)*C7"      # LTM EBITDA = Q1 current + FY prior - Q1 prior
ws['K7'] = "=(220+850-205)*C7"    # LTM Revenue = same stub convention
```

When the workbook is opened in Excel with the CapIQ add-in active, C7 resolves to the FX rate and I/J/K display the values in the output currency set in `H2`. Do **not** pre-convert the values yourself, and do **not** pre-sum the LTM stubs — write each stub into the formula in source currency and let Excel handle both the LTM math and the FX conversion.

**Source comments — required on every written I / J / K cell:**

If a cell is left unset because the metric is undisclosed, do not attach a comment. Otherwise:

- **Column I (TEV) — single bare URL.** The comment text is the source URL and nothing else. No prefix, no label, no figure. Use the deal press release / 8-K / news article that quotes the deal value.

- **Columns J (EBITDA) and K (Revenue) — labeled, one line per stub.** The number of lines in the comment must match the number of operands in the cell formula. Each line uses the format:

  > `<Period> ($<Value>): <URL>`

  - **LTM stub calc (3 operands)** → 3 lines: MRQ, then FY, then PYQ.
  - **FY-only / Q4 announcement (1 operand)** → 1 line: `FY<year> ($<value>): <URL>`.
  - **Private target with disclosed metric (1 operand)** → 1 line labeled with the period the source quotes (e.g., `LTM ($85.0): URL` or `FY2023 ($72.0): URL`).
  - **Private target with figure implied from a multiple (1 operand)** → 1 line: `Implied from <multiple> in: URL` (no `($value)` since the figure is derived).

  Use one URL per stub. If the same filing covers two stubs (e.g., a 10-Q whose period table also shows the prior-year comparable), repeat that URL on both stub lines — do not consolidate.

```python
from openpyxl.comments import Comment

# TEV — single bare URL
ws['I7'] = "=1250*C7"
ws['I7'].comment = Comment("https://www.sec.gov/Archives/edgar/data/.../8-k.htm", "Source")

# LTM EBITDA — three stubs, three labeled lines
ws['J7'] = "=(17.517+84.720-17.665)*C7"
ws['J7'].comment = Comment(
    "Q1 2025 ($17.517): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/\n"
    "FY2024 ($84.720): https://www.globenewswire.com/news-release/2025/02/26/3032731/37161/en/AvidXchange-Announces-Fourth-Quarter-Full-Year-2024-Financial-Results.html\n"
    "Q1 2024 ($17.665): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/",
    "Source"
)

# LTM Revenue — three stubs, three labeled lines
ws['K7'] = "=(107.9+438.94-105.6)*C7"
ws['K7'].comment = Comment(
    "Q1 2025 ($107.9): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/\n"
    "FY2024 ($438.94): https://www.globenewswire.com/news-release/2025/02/26/3032731/37161/en/AvidXchange-Announces-Fourth-Quarter-Full-Year-2024-Financial-Results.html\n"
    "Q1 2024 ($105.6): https://www.avidxchange.com/press-releases/avidxchange-announces-first-quarter-2025-financial-results/",
    "Source"
)
```

The second `Comment(...)` argument is the comment author and is not the comment body — Excel only displays the first argument. Use `\n` between stub lines so each appears on its own line in the Excel comment box.

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
3. Cells I, J, K start with `=` and end with `*C{same_row}` (formulas, not raw numbers). For J and K, the formula contains the LTM stub arithmetic — e.g., `=(17.517+84.720-17.665)*C7` — so Excel does the math; no pre-summed single number unless the row legitimately uses FY-only or a single disclosed metric.
4. Every populated I / J / K cell has a `.comment`:
   - **I** — comment text is a single bare URL (starts with `http://` or `https://`).
   - **J / K** — one line per operand in the formula, each line formatted `<Period> ($<Value>): <URL>` (or `Implied from <multiple> in: URL` when derived). Operand count and line count must match (3 stubs in formula → 3 comment lines; 1 stub → 1 line).
5. Column N values are all ≤50 characters
6. No values were written to columns C, D, L, M, or any column past N
7. No values were written outside rows 7–21

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
| I7:I21 | Deal Value (TEV) | **Write here as formula** `=raw*C{row}` + single bare-URL source comment |
| J7:J21 | EBITDA (LTM) | **Write here as formula** `=(mrq+fy-pyq)*C{row}` (or `=fy*C{row}` for Q4 / `=val*C{row}` for disclosed-metric private) + labeled multi-line source comment (one line per stub) |
| K7:K21 | Revenue (LTM) | **Write here as formula** `=(mrq+fy-pyq)*C{row}` (or `=fy*C{row}` / `=val*C{row}`) + labeled multi-line source comment (one line per stub) |
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
| J | EBITDA (LTM) | Formula | `=(mrq+fy-pyq)*C{row}` (LTM stubs) or `=fy*C{row}` / `=val*C{row}`; blank if undisclosed |
| K | Revenue (LTM) | Formula | `=(mrq+fy-pyq)*C{row}` (LTM stubs) or `=fy*C{row}` / `=val*C{row}`; blank if undisclosed |
| L | TEV / EBITDA | Formula | Auto-calculated — do not write |
| M | TEV / Revenue | Formula | Auto-calculated — do not write |
| N | Target Description | String | ≤50 chars |

### Precedent Transaction Research Tips

**Good search queries (mix of public and private deals):**
- `"[target name] 10-K [year] revenue EBITDA"`
- `"[target name] 20-F annual report"` (for non-US public targets)
- `"[sector] acquisition [year range] press release"`
- `"[acquiror] acquires [target] press release financial highlights"`
- `"[sector] M&A transaction multiple disclosed EBITDA"`
- `"[sector] private company acquired [year range] disclosed revenue EBITDA"`

**Verifying financial figures — ranked by reliability:**
1. Target's own filings — for an LTM stub calc you usually need three: the most recent 10-Q / 6-K / interim MD&A (`YTD_MRQ`), the prior 10-K / 20-F / AIF (`FY_prior`), and the prior-year 10-Q / 6-K / interim MD&A for the same calendar quarter (`YTD_PYQ`). Apply the same EBITDA definition (Operating Income + D&A, or Adjusted EBITDA if consistently disclosed) across all three stubs. If the announcement falls right after a 10-K (MRQ = Q4), no stub calc is needed — use the 10-K alone.
2. Acquiror's deal announcement press release — often states "LTM Revenue of $X" and "Adjusted EBITDA of $X" to justify valuation; useful as a cross-check, and sometimes the only source for a private target.
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
- For public targets, Revenue and EBITDA should always be findable from filings on an LTM basis — do not leave them blank, and do not fall back to FY when an MRQ has been reported
- For private targets, write only the metrics that are directly disclosed or cleanly implied from a disclosed multiple; leave the rest blank. Disclosed metrics may drift from a true LTM end-date by a few months, but never by years — drop the deal if the only available figure is two-plus years stale.
- Aim for at least 80% of selected transactions to have both Revenue and EBITDA populated
