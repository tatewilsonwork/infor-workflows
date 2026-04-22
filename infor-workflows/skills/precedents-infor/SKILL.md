---
name: precedents-infor
description: >
  Use this skill when the user asks to build a precedent transactions table
  for a company. Researches 8 relevant M&A precedent transactions with disclosed Revenue, EBITDA,
  and AUM (where applicable) sourced from company press releases, financial statements, or reputable
  news sources, and populates the INFOR Precedents Template with the results.
version: 1.7.0
---

# INFOR Precedent Transactions Table — Workflow

This skill builds a precedent transactions table by researching 8 relevant M&A deals and writing the transaction data into the INFOR Precedents Template (cells B7:M14 only).

Allowed tools: Read, Bash, Write, Glob, WebSearch

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Precedents Template.xlsx" 2>/dev/null | head -1`
- Outputs folder: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); echo "${REPO_ROOT:-.}/outputs"`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Confirm Company

If the company name or website was not passed with the command, ask:

> "Please provide the name or website of the company you'd like me to build a precedent transactions table for."

Wait for the company before proceeding.

---

### Step 2 — Determine Sector and AUM Relevance

Before searching, identify:
1. **Sector / business type** of the target company (e.g., wealth management, insurance, SaaS, industrial)
2. **AUM relevance** — only include AUM data (column J) if the target company operates in an industry where AUM is a standard valuation metric:
   - **Include AUM:** asset managers, wealth managers, private equity firms, hedge funds, insurance companies, REITs, and other financial services firms where AUM drives revenue
   - **Leave J blank:** all other sectors (technology, industrials, healthcare, energy, etc.)

Use WebSearch to confirm the company's sector if not obvious from the name/website.

---

### Step 3 — Research 8 Precedent Transactions

Search for 8 relevant M&A transactions where the **target company** is comparable to the input company.

**Prioritise transactions with fully disclosed financials** — select them in this order of preference:
1. Publicly traded targets (their annual filings are public — LTM Revenue and EBITDA are always available; NTM estimates often in analyst reports or deal press releases)
2. Private targets where the acquiror's press release discloses LTM Revenue and EBITDA
3. Private targets with disclosed deal value only (include if deal value is confirmed and strategic fit is strong)

Never include a transaction where deal value is undisclosed — a blank TEV makes the row unusable for multiple analysis.

**Search strategy — run several targeted queries:**
- `"[sector] acquisition [year range] annual report revenue EBITDA site:sec.gov OR site:sedar.com"`
- `"[sector] M&A [year range] press release LTM revenue EBITDA disclosed"`
- `"[company name] comparable transactions precedents investment banking"`
- `"[target name] acquired [year] annual report financial statements"`
- `"[target name] acquired [year] NTM forward estimates consensus analyst"`

**For each candidate transaction — retrieve financials as follows:**
- **LTM Revenue and EBITDA:** If the target was publicly traded, use the most recent annual filing (10-K, AIF, annual MD&A) before deal announcement. If private, look in the acquiror's deal press release for phrases like "LTM Revenue of $X", "trailing twelve months EBITDA of $X".
- **NTM Revenue and EBITDA:** Forward estimates at the time of deal announcement. Sources in order of preference: (1) acquiror's deal press release or investor presentation quoting "forward revenue of $X" or "NTM EBITDA of $X"; (2) analyst consensus estimates cited in deal commentary; (3) company guidance issued before or concurrent with the announcement. Leave as `None` if no forward estimate is disclosed — NTM is best-effort only.
- **AUM:** typically disclosed in the deal announcement PR for financial services transactions — look for "$X billion in assets under management" or "AUM of $X".

**Selection criteria:**
- Similar sector/business model to the input company
- Announced or completed within the last 6–8 years (prefer recent deals)
- Disclosed deal value (TEV) — **required; do not include a deal with no deal value**
- Disclosed Revenue and EBITDA — required for public targets; best-effort for private targets
- If AUM is relevant: disclosed AUM from deal PR or target filing

**Source discipline — this is critical:**
- Revenue, EBITDA, and AUM figures must come from: (1) target company filings (10-K, AIF, annual MD&A), (2) acquiror deal press releases or investor decks, or (3) reputable financial news (Bloomberg, Reuters, Globe and Mail, Financial Post, WSJ, S&P Global)
- Do not fabricate or estimate financial metrics — if you cannot verify a figure from a legitimate source after a thorough search, mark it as `None`
- Aim for at least 6 of 8 transactions to have disclosed Revenue and EBITDA

**Currency:** Use the currency as stated in the original source. Enter the ISO 3-letter code in column B (e.g., `"USD"`, `"CAD"`, `"GBP"`). The template's FX formulas convert to output currency automatically.

---

### Step 4 — Locate and Copy the Template

The template path is shown in the Context section above. If blank, locate it dynamically:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Precedents Template.xlsx" 2>/dev/null | head -1
```

The output folder path is also in the Context section. If blank, use:
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

Write to the `Sheet1` sheet only. **Write exactly the 8 data rows, columns B through M (B7:M14). Touch no other cells.**

For each of rows 7 through 14, write the following columns:

| Column | Field | Python type | Notes |
|--------|-------|-------------|-------|
| B | Currency | `str` | ISO code, e.g. `"USD"`, `"CAD"` |
| C | Announce Date | `datetime.date` | Use `datetime.date(YYYY, M, D)` |
| D | Target | `str` | Full legal name of target company |
| E | Acquiror | `str` | Full legal name of acquiror |
| F | Deal Value | `float` or `int` | $MM numeric, no currency symbol |
| G | Target HQ | `str` | ISO 2-letter country code (e.g., `"CA"`, `"US"`, `"GB"`) |
| H | LTM Revenue | `float` or `int` or `None` | LTM Revenue in $MM; `None` if undisclosed |
| I | NTM Revenue | `float` or `int` or `None` | NTM Revenue in $MM; `None` if undisclosed |
| J | LTM EBITDA | `float` or `int` or `None` | LTM EBITDA in $MM; `None` if undisclosed |
| K | NTM EBITDA | `float` or `int` or `None` | NTM EBITDA in $MM; `None` if undisclosed |
| L | Target AUM | `float` or `int` or `None` | AUM in $MM; `None` if not applicable or undisclosed |
| M | Target Description | `str` | ≤50 characters — see description rules below |

**Description rules (column K):**
- Column K has a cell width of 50 characters — descriptions that exceed this will overflow or be cut off visually
- Describe **what the company does or sells** — product, service, asset class, client segment, or business model
- **Do not include geography** — country and region are already captured in column G (Target HQ)
- Target 35–50 characters; never exceed 50
- No trailing punctuation; title case preferred
- Examples of good descriptions (count the characters):
  - `"Diversified multi-asset & alternatives manager"` (47)
  - `"Independent wealth advisory platform"` (37)
  - `"Retail mutual fund & wealth manager"` (36)
  - `"Mid-market private credit manager"` (33)
  - `"SaaS-based insurance distribution platform"` (43)
  - `"Life and health insurance provider"` (35)

**Writing None values:** If a field is `None` (undisclosed), skip writing that cell entirely — do not write `None` or empty string, just leave it unset so the cell remains blank.

**Do NOT write to** columns N through AE — these contain CapIQ formulas that auto-populate when the file is opened in Excel.

Save the file after writing all rows.

---

### Step 6 — Verify Output

After saving, re-open the file and spot-check:
1. All 8 rows (7–14) have values in columns B, C, D, E
2. Dates are `datetime.date` objects (not strings)
3. Numeric fields (F, H, I, J, K, L) are numeric types (not strings)
4. Column M values are all ≤50 characters
5. No values were written to columns N or beyond

Report any issues found and fix before delivering.

---

### Step 7 — Summary

Report to the user:

1. **Output file:** computer:// link to the saved file
2. **Transactions populated:** list of 8 deals with target, acquiror, and deal value
3. **Missing data:** note any LTM/NTM Revenue, LTM/NTM EBITDA, or AUM fields left blank due to non-disclosure
4. **Sources:** brief summary of where financial figures were sourced
5. **Reminder:** Open in Excel with the CapIQ add-in active — columns P onward (TEV, multiples) will auto-populate via CapIQ FX conversion formulas

---

## Domain Reference

### Template Cell Map — Sheet1

| Cells | Purpose | Notes |
|-------|---------|-------|
| B7:M14 | 8 transaction data rows — **write here only** | 8 rows × 12 input columns |
| N7:N14 | FX conversion — CapIQ array formula | **Never overwrite** |
| P7:AE14 | Output columns (TEV, multiples, formatted fields) | **Never overwrite — all formulas** |

### Column Reference

| Col | Header | Type | Unit |
|-----|--------|------|------|
| B | Input Currency | String | ISO code (USD/CAD/GBP/EUR/AUD) |
| C | Announce Date | Date | — |
| D | Target | String | — |
| E | Acquiror | String | — |
| F | Deal Value | Numeric | $MM in currency of col B |
| G | Target HQ | String | ISO 2-letter country code (CA, US, GB, AU, etc.) |
| H | LTM Revenue | Numeric | $MM LTM; None if undisclosed |
| I | NTM Revenue | Numeric | $MM NTM; None if undisclosed |
| J | LTM EBITDA | Numeric | $MM LTM; None if undisclosed |
| K | NTM EBITDA | Numeric | $MM NTM; None if undisclosed |
| L | Target AUM | Numeric | $MM; None if N/A or undisclosed |
| M | Target Description | String | ≤50 chars |

### AUM Sectors Reference

Include AUM (column J) only when the target is in one of these sectors:
- Asset management (mutual funds, ETFs, separately managed accounts)
- Wealth management / financial advisory
- Private equity / private credit / venture capital
- Hedge funds / alternative investments
- Insurance (AUM = investment portfolio)
- Real estate investment trusts (REITs) / real estate managers
- Pension fund managers / defined benefit plan administrators

For all other sectors, leave column J blank.

### Precedent Transaction Research Tips

**Good search queries:**
- `"[target name] annual report 10-K [year] revenue EBITDA"`
- `"[sector] acquisition [year range] press release LTM revenue EBITDA"`
- `"[acquiror] acquires [target] press release financial highlights"`
- `"[sector] M&A transaction [geography] disclosed financials"`

**Verifying financial figures — ranked by reliability:**
1. Target's own annual report (10-K, AIF, annual MD&A) — income statement gives Revenue; EBITDA = Operating Income + D&A from cash flow statement
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
- Never include a deal with no deal value — the TEV column must be populated for the row to be useful
- For public targets, Revenue and EBITDA should always be findable from filings — do not leave them blank
- For private targets, mark undisclosed H and I as None; include the deal only if TEV is confirmed
- Aim for at least 6 of 8 deals to have disclosed Revenue and EBITDA
