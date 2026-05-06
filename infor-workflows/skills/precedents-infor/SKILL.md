---
name: precedents-infor
description: >
  Use this skill when the user asks to build a precedent transactions table for a company.
  Researches up to 15 relevant M&A precedent transactions — with a mild preference for
  publicly traded targets at the time of acquisition (where Revenue and EBITDA are verifiable
  from filings), but a closer-comparable private target with disclosed metrics or multiples
  should be selected over a weakly comparable public one. Populates the INFOR Precedents Template.
version: 2.4.0
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

**Source priority — find a disclosed figure first; only calculate from filings when nothing is disclosed.**

Work this ladder top-down for both public and private targets. Stop at the first rung that produces a usable figure.

1. **Disclosed LTM (or close-to-LTM) $ figure in the transaction's own sources — strongly preferred for public AND private targets.** Look first in the acquiror's deal press release, deal-supplement investor deck or 8-K exhibit, deal conference call / earnings call transcript discussing the transaction, or reputable financial news coverage of the transaction (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global). Many deal announcements explicitly disclose "LTM Revenue of $X" and "LTM (or Adjusted) EBITDA of $Y" — those are typically the figures the buyer used to value the deal and what an investment banker would cite. Use the disclosed figure as the cell value as-is; do not "recalculate" over it. A reasonable sanity check against filings is fine — but if the deal source says $107.9 LTM Revenue, the cell value is $107.9.
2. **Disclosed transaction multiple → derive from TEV.** If the deal source quotes a multiple but not the absolute $ figure (e.g., "acquired at ~12.5x LTM EBITDA" or "~3.0x Revenue"), derive the metric by dividing TEV by the multiple. Write the cell as a formula referencing the TEV cell directly — e.g., `=I7/12.5` for J7 (EBITDA) or `=I7/3.0` for K7 (Revenue). **Do not multiply by `C{row}`** — column I is already converted to output currency, so the derived metric inherits that conversion. **This rung is required when available — a disclosed multiple supersedes the filings-stub fallback (rung 3), not merely preferred over it.** The multiple reflects how the buyer valued the deal. Use it for both public and private targets when no $ LTM is disclosed.
3. **Calculated LTM from target filings — public-target fallback only.** If, and only if, neither a disclosed $ figure nor a disclosed multiple can be found in the transaction sources, calculate LTM from the target's own filings using the stub-period formula below.
4. **Disclosed non-LTM period $ figure — private-target fallback.** For private targets where steps 1 and 2 fail, use whatever absolute Revenue / EBITDA figure is disclosed (e.g., FY 2023, calendar 2024). Label the period in the comment and accept that timing may drift by months, but never by years — drop the deal if the only available figure is two-plus years stale.

There is no filings-based fallback for private targets. If steps 1, 2, and 4 all fail for a private target, leave the cell blank (or drop the deal if both Revenue and EBITDA are missing).

**Do not skip a disclosed multiple — common bad reasons agents reach for the stub calc instead:**
- The multiple says "approximately Nx" or "~Nx" — still rung 2.
- Wanting to verify from filings — verifying is fine, but the cell value is the disclosed multiple.
- "It's pro forma" — see the pro-forma note below.
- Wanting the standalone number rather than the deal number — the precedents table shows what buyers paid, not target-standalone fundamentals.

**"Pro forma" almost never means synergies.** In deal-source multiples, "pro forma" almost always means pro forma for divestitures or continuing operations — not pro forma for buyer synergies. Synergies are virtually always called out as a separate line item ("$X of expected run-rate cost savings"), not embedded in the headline multiple. Treat the multiple as synergy-inclusive only if the source explicitly says "including synergies," "post-synergy," or "synergized."

**LTM stub-period formula — used only for step 3 (public-target fallback):**

> **LTM = YTD_MRQ + FY_prior − YTD_PYQ**

…where `YTD_MRQ` is year-to-date through the most recent reported quarter before announcement, `FY_prior` is the most recent completed fiscal year, and `YTD_PYQ` is the matching year-to-date stub from the prior year. The two YTD stubs must cover the **same calendar period** (Q1 vs. Q1, H1 vs. H1, 9M vs. 9M).

| MRQ before announce | YTD stubs to pull |
|---|---|
| Q1 | Q1 current vs. Q1 prior |
| Q2 | H1 current vs. H1 prior |
| Q3 | 9M current vs. 9M prior |
| Q4 | No stub calc — `LTM = FY` (use the 10-K directly) |

Worked example — AvidXchange acquired by TPG / Corpay, announced May 6, 2025. If the deal press release / 8-K / Corpay investor deck disclosed an LTM figure, that figure goes in the cell directly (step 1). Only if no LTM is disclosed would you fall back to the stub calc:
- LTM Revenue = Q1 2025 ($107.9) + FY 2024 ($438.94) − Q1 2024 ($105.6)
- LTM EBITDA = Q1 2025 ($17.517) + FY 2024 ($84.720) − Q1 2024 ($17.665)

For the stub calc, pull each stub from its own filing — the most recent 10-Q / 6-K / interim MD&A (`YTD_MRQ`), the most recent 10-K / 20-F / AIF (`FY_prior`), and the prior-year 10-Q / 6-K / interim MD&A for the same calendar quarter (`YTD_PYQ`). Apply the same EBITDA definition (Operating Income + D&A from cash flow statement, or Adjusted EBITDA if consistently disclosed) across all three stubs. If MRQ is Q4, no stub calc is needed — use the 10-K's full-year figures.

**Pre-write checkpoint — before writing a 3-operand stub formula for J or K.** State in your response which deal sources you searched for a disclosed $ LTM figure and a disclosed multiple, and what you found. Required search set: the acquiror deal press release, 8-K exhibit / investor deck, and at least one of (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global) deal coverage. If a multiple was found but rejected, the rejection reason must be checked against the bad-reasons list above.

**Excel does the math, not you.** Whether the cell value is a single disclosed figure or a stub calc, it must live in a cell formula (see Step 5) — never pre-sum the stubs in Python and write a single number for the calculated case.

**Selection criteria:**
- Similar sector / business model to the input company
- Announced or completed within the last 6–8 years (prefer recent deals)
- Disclosed deal value (TEV) — **required**
- Disclosed Revenue and/or EBITDA — required for public targets; private targets require either disclosed metrics or a disclosed multiple from which a value can be inferred

**Source discipline — this is critical:**
- All financial figures must come from: (1) target company filings (10-K, 20-F, AIF, annual MD&A), (2) acquiror deal press releases or investor decks, or (3) reputable financial news (Bloomberg, Reuters, Globe and Mail, Financial Post, WSJ, S&P Global).
- Do not fabricate or estimate financial metrics. If a figure cannot be verified after a thorough search, leave the cell blank.
- Aim for at least 80% of selected transactions to have disclosed Revenue and EBITDA. The mild public-target preference helps hit this, but do not sacrifice comparability to do so — a tightly-fit private deal with one disclosed metric is more useful than an off-sector public deal with both.

**Currency:** Use the currency as stated in the original source — when EBITDA / Revenue are written as $ figures (`*C{row}` formulas), they must be in the **same currency** as TEV, matching the ISO 3-letter code entered in column B. The template's column C FX formula converts to the output currency, and the `*C{row}` factor applies that conversion. **Multiple-derived J/K cells (`=I{row}/multiple`) are dimensionless inputs and inherit their currency from I — currency consistency is automatic; do not add `*C{row}`.**

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
| I | Deal Value (TEV) | **formula string** | `f"={raw_tev}*C{row}"` — raw value in $MM of input currency. Attach a Quote + Source comment (Format A) |
| J | EBITDA | **formula string** or unset | Disclosed $ LTM in transaction source (preferred) — `f"={ltm}*C{row}"` (e.g., `"=85.0*C7"`). **Disclosed multiple — `f"=I{row}/{multiple}"` (e.g., `"=I7/12.5"`) — no `*C{row}` because I is already in output currency.** Calculated LTM stub calc (public-target fallback) — `f"=({mrq}+{fy}-{pyq})*C{row}"` (e.g., `"=(17.517+84.720-17.665)*C7"`). FY-only / Q4 announcement — `f"={fy}*C{row}"`. Disclosed non-LTM private-target $ figure — `f"={value}*C{row}"`. Leave unset if undisclosed. Comment: Format A (Quote + Source) for 1-operand formulas; Format B (3-line stub list) for stub calc — see below |
| K | Revenue | **formula string** or unset | Same precedence as EBITDA. For a disclosed Revenue multiple, use `f"=I{row}/{multiple}"` (e.g., `"=I7/3.0"`) — no `*C{row}`. Leave unset if undisclosed. Comment: same format rules as J |
| N | Target Description | `str` | ≤50 characters — see description rules below |

**FX conversion — critical:**

Cells I, J, and K are written as **formulas** that multiply the raw source-currency $MM value by the FX conversion in column C of the same row. Column C is a CapIQ array formula (`C7:C21`) that returns the rate from input currency (column B) to output currency (`$H$2`).

**Disclosed-$-LTM example** (rung 1, preferred path) — row 7 is a deal whose press release / 8-K discloses LTM Revenue of CAD 880 MM and LTM EBITDA of CAD 195 MM:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=195*C7"              # disclosed LTM EBITDA
ws['K7'] = "=880*C7"              # disclosed LTM Revenue
```

**Disclosed-multiple example** (rung 2 — used when no $ LTM figure is disclosed but a multiple is) — same row, deal source quotes 12.5x LTM EBITDA and 2.8x LTM Revenue:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"             # TEV in output currency after FX
ws['J7'] = "=I7/12.5"             # EBITDA = TEV / 12.5x — no *C7 (I7 already converted)
ws['K7'] = "=I7/2.8"              # Revenue = TEV / 2.8x — no *C7 either
```

**Calculated-stub example** (rung 3 — public-target fallback when neither $ LTM nor multiples are disclosed) — same TEV but LTM is built from filings:
```python
ws['B7'] = "CAD"
ws['I7'] = "=1250*C7"
ws['J7'] = "=(45+180-42)*C7"      # LTM EBITDA = Q1 current + FY prior - Q1 prior
ws['K7'] = "=(220+850-205)*C7"    # LTM Revenue = same stub convention
```

When the workbook is opened in Excel with the CapIQ add-in active, C7 resolves to the FX rate and I/J/K display the values in the output currency set in `H2`. Do **not** pre-convert the values yourself, and do **not** pre-sum the LTM stubs in Python — write each stub into the formula in source currency and let Excel handle both the LTM math and the FX conversion.

**Critical — FX is applied exactly once:**
- $ LTM figures and stub-period figures are in **input currency**, so the formula multiplies by `C{row}` to convert.
- A disclosed multiple is **dimensionless**, and `I{row}` is already in **output currency** (its own formula did the FX). Dividing `I{row}` by a multiple yields output-currency $MM directly. Adding `*C{row}` would double-apply FX. **Never write `=I7/12.5*C7`.** The multiple-derived formula is `=I7/<multiple>` — full stop.

**Source comments — required on every written I / J / K cell:**

If a cell is left unset because the metric is undisclosed, do not attach a comment. Otherwise pick the format by source-path:

**Format A — Quote + Source.** Used for column I (TEV) and for any J/K cell whose formula has a single operand (disclosed $ LTM rung 1, disclosed multiple rung 2, FY-only / Q4, disclosed non-LTM private $ figure rung 4). Two-block format with a blank line between:

```
Quote: "<short verbatim quote from the source containing the figure or multiple>"

Source: <URL>
```

- The quote must be **verbatim from the source** — do not paraphrase. Copy the sentence or clause that directly supports the figure or multiple. Keep it short (one or two clauses, typically under 200 characters).
- Always close the quote with `"`. If the verbatim text contains a colon, em dash, or other punctuation, preserve it inside the quotes.
- One blank line between Quote and Source.
- The Source line is a single URL pointing to the specific document the quote was taken from.

**Format B — Multi-stub labeled lines.** Used **only** for the calculated LTM stub-calc case (rung 3, 3-operand formula `=(mrq+fy-pyq)*C{row}`). One line per stub, no Quote prefix:

```
<Period> ($<Value>): <URL>
```

- 3 lines: MRQ first, then FY, then PYQ.
- One URL per stub. If the same filing covers two stubs (e.g., a 10-Q whose period table also shows the prior-year comparable), repeat that URL on both stub lines — do not consolidate.

This per-stub labeled format is preserved for the multi-source case so a reviewer can map each operand of the formula directly to its source filing.

```python
from openpyxl.comments import Comment

# TEV (column I) — Format A
ws['I7'] = "=1250*C7"
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

# J (EBITDA) from a calculated LTM stub — Format B (unchanged)
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

**Number of rows:** Populate as many rows as you have well-sourced transactions, up to 15. Do not fabricate transactions to fill the table — fewer high-quality rows is better than padding.

**Trim empty rows before saving — required when fewer than 15 transactions are populated.**

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

Save the file after trimming.

---

### Step 6 — Verify Output

After saving, re-open the file and spot-check:
1. Exactly `n` data rows remain (rows 7 through 7+n-1), each with values in B, E, F, G, H, I, and N. There should be no blank data rows between the last transaction and the averages row.
2. Dates in column E are `datetime.date` objects (not strings)
3. Cells I, J, K start with `=` (formulas, not raw numbers). Tail check by source path:
   - **I** — always ends with `*C{same_row}` (e.g., `=1250*C7`). Always.
   - **J / K from disclosed $ LTM** — single operand ending `*C{same_row}` (e.g., `=85.0*C7`). ✓
   - **J / K from disclosed multiple** — references `I{same_row}` and divides by the multiple (e.g., `=I7/12.5`). **No `*C{row}`** — column I is already in output currency. ✓
   - **J / K from calculated stub** — three operands with arithmetic, ending `*C{same_row}` (e.g., `=(17.517+84.720-17.665)*C7`). ✓
   - **J / K from FY-only / disclosed non-LTM private $ figure** — single operand ending `*C{same_row}`. ✓
   - What's never valid: a pre-summed scalar where the source path was a stub calc, OR a `*C{row}` tail on a `=I{row}/multiple` formula (would double-apply FX).
4. Every populated I / J / K cell has a `.comment`. Comment format depends on source-path:
   - **Format A — Quote + Source.** Required for column I (TEV) and for any J/K with a 1-operand formula (disclosed $ LTM, disclosed multiple, FY-only, non-LTM private $). Comment text starts with `Quote: "`, contains a verbatim quote closed with `"`, then a blank line, then `Source: <URL>`. Verify:
     - Starts with `Quote: "` and contains a closing `"` for the quoted text
     - Has a blank line (i.e., `\n\n`) between Quote and Source blocks
     - Source line starts with `Source: http`
   - **Format B — Multi-stub labeled lines.** Required for J/K with the 3-operand stub-calc formula `=(mrq+fy-pyq)*C{row}`. Comment text is exactly 3 lines, each formatted `<Period> ($<Value>): <URL>` (MRQ, FY, PYQ). No `Quote:` prefix. Stub line count must equal formula operand count.
   - **Format mismatch is a fail.** A `=I{row}/multiple` cell with a 3-line stub comment is wrong; a `=(a+b-c)*C{row}` cell with a Quote/Source comment is wrong.
5. Column N values are all ≤50 characters
6. No values were written to columns C, D, L, M, or any column past N
7. After row deletion, the averages row at `23 - rows_to_drop` references the populated data range correctly — no `#REF!` and the AVERAGE range matches `L7:L{last_data_row}` / `M7:M{last_data_row}`.
8. Column C of the remaining data rows is intact (no `#REF!` in any populated row's C cell).
9. **Source-rung consistency.** For each row using a 3-operand stub formula (`=(mrq+fy-pyq)*C{row}`), the response must contain an explicit log stating that no disclosed $ LTM and no disclosed multiple were found in the deal-source documents. A stub calc with no rung-1 / rung-2 search log is a fail — re-do the row with the disclosed value.

Report any issues found and fix before delivering.

---

### Step 7 — Summary

Report to the user:

1. **Output file:** computer:// link to the saved file
2. **Transactions populated:** list of deals with target, acquiror, deal value, and a `[Public]` or `[Private]` tag for the target's status at announcement
3. **Source mix:** how many public-target vs. private-target rows are included; for any private-target row, briefly note whether financials are directly disclosed or implied from a disclosed multiple
4. **Missing data:** note any EBITDA or Revenue cells left blank due to non-disclosure
5. **Sources:** brief summary of where financial figures were sourced (filings vs. acquiror PRs vs. news)
6. **Reminder:** Open in Excel with the CapIQ add-in active — column C (FX rate) will populate, and columns I/J/K formulas will resolve to output-currency $MM. Columns L/M (multiples) and the averages row (originally row 23, shifted up by however many rows were trimmed) auto-calculate.

---

## Worked Examples — Rung 2 (Disclosed Multiple)

These complement the AvidXchange stub-calc example in Step 3 by showing rung 2 in action.

**Micro Focus / OpenText (announced August 25, 2022).** OpenText's deal press release quotes "6.3x Micro Focus' pro forma TTM adjusted EBITDA" and separately calls out "$400M of run-rate cost savings." The multiple is on standalone Micro Focus (pro forma for divestitures), **not** synergy-inclusive. Correct: `J{row} = "=I{row}/6.3"` with a Format A (Quote + Source) comment. Wrong: a 3-operand stub calc from FY21 + H1 stubs, even though the underlying data is available — rung 2 is required when the multiple is disclosed.

**Citrix / Vista (announced January 31, 2022).** Source quotes "~24.8x LTM EBITDA." Correct: `J{row} = "=I{row}/24.8"` — no `*C{row}`.

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
| I7:I21 | Deal Value (TEV) | **Write here as formula** `=raw*C{row}` + Quote/Source comment (Format A). |
| J7:J21 | EBITDA (LTM) | **Write here as formula.** Preferred: `=ltm*C{row}` from disclosed $ LTM in deal source. **`=I{row}/multiple` from disclosed multiple — no `*C{row}`.** Public-target fallback: `=(mrq+fy-pyq)*C{row}` from filings. Other: `=fy*C{row}` (Q4 / private FY). Comment: Format A (Quote + Source) for 1-operand formulas; Format B (3-line stub list) for stub calc. |
| K7:K21 | Revenue (LTM) | **Write here as formula.** Same precedence as EBITDA, including `=I{row}/multiple` for disclosed Revenue multiples. Comment: same format rules as J. |
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
| J | EBITDA (LTM) | Formula | Preferred `=ltm*C{row}` (disclosed $ LTM) or `=I{row}/multiple` (disclosed multiple, no FX); fallback `=(mrq+fy-pyq)*C{row}` (calc stubs); also `=fy*C{row}`; blank if undisclosed |
| K | Revenue (LTM) | Formula | Same precedence as EBITDA, incl. `=I{row}/multiple` for disclosed Revenue multiples; blank if undisclosed |
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

**Sourcing financial figures — preferred order (matches the Step 3 ladder):**
1. Acquiror's deal announcement press release / 8-K exhibit — often states "LTM Revenue of $X" and "Adjusted EBITDA of $X" to justify valuation. **First place to look for both public and private targets.**
2. Acquiror's investor presentation or deal supplement filed with the announcement
3. Bloomberg, Reuters, Financial Post, WSJ, or Globe and Mail deal coverage that quotes disclosed metrics, or deal-day conference call transcripts
4. Target's own filings — used only when the deal sources above don't disclose LTM. For a stub calc you usually need three: the most recent 10-Q / 6-K / interim MD&A (`YTD_MRQ`), the prior 10-K / 20-F / AIF (`FY_prior`), and the prior-year 10-Q / 6-K / interim MD&A for the same calendar quarter (`YTD_PYQ`). Apply the same EBITDA definition (Operating Income + D&A, or Adjusted EBITDA if consistently disclosed) across all three stubs. If MRQ = Q4, use the 10-K alone.

**HQ country codes — common examples:**

| Country | Code | Country | Code |
|---------|------|---------|------|
| Canada | CA | Australia | AU |
| United States | US | France | FR |
| United Kingdom | GB | Germany | DE |
| Ireland | IE | Netherlands | NL |

**Handling undisclosed metrics:**
- Never include a deal with no deal value — TEV must be populated for the row to be useful
- For both public and private targets, look for a disclosed $ LTM figure in the deal sources first. If found, use it as-is — do not "recalculate" over a disclosed LTM.
- If no $ LTM is disclosed but a transaction multiple is, derive the metric in-cell as `=I{row}/multiple`. No `*C{row}` — column I is already in output currency.
- For public targets where neither $ LTM nor a multiple is disclosed, fall back to the stub-period filings calc — do not leave Revenue / EBITDA blank, and do not fall back to bare FY when an MRQ has been reported.
- For private targets, write only the metrics that are directly disclosed (as a $ figure or via a multiple); leave the rest blank. Disclosed metrics may drift from a true LTM end-date by a few months, but never by years — drop the deal if the only available figure is two-plus years stale.
- Aim for at least 80% of selected transactions to have both Revenue and EBITDA populated
