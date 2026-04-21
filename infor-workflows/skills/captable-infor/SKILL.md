---
name: captable-infor
description: >
  Use this skill when extracting financial data from MD&A, 10-K, 10-Q, annual reports, or financial
  statements to populate a capitalization table. Activates for tasks involving shares outstanding,
  debt schedules, lease obligations, options/RSU/warrant tables, convertible debentures, cash balances,
  preferred shares, or non-controlling interest sourced from company filings.
version: 1.3.6
---

# INFOR Capitalization Table — Workflow & Domain Knowledge

This skill guides you through populating the INFOR capitalization table template from a CapIQ ticker and attached financial statements, and provides domain knowledge for accurate data extraction.

Allowed tools: Read, Bash, Write, Glob

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Cap Table Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Collect Inputs

Ask the user for the CapIQ ticker if not already provided, and confirm at least one document is attached (10-K, 10-Q, annual report, or financial statement PDF).

If either is missing, ask in a single message:

> "Please provide the CapIQ ticker for the company and attach the relevant financial statements or MD&A with your reply.
>
> - **Ticker format:** Exchange:Ticker — for example `NasdaqGS:MSFT`
> - **Documents to attach:** Most recent 10-K or annual report — I need the balance sheet, long-term debt note, lease footnote, equity compensation footnote, and shares outstanding disclosure to fill in the template."

Wait for both the ticker and at least one attached document before proceeding.

---

### Step 2 — Locate and Copy the Template

The template path is shown in the Context section above. If the path is blank, search for it — check the repo's templates directory first, then the plugin cache, then fall back to $HOME:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Cap Table Template.xlsx" 2>/dev/null | head -1
```

Sanitize the ticker for use as a filename by replacing `:` with `-` (e.g., `NasdaqGS:MSFT` → `NasdaqGS-MSFT`).

Copy the template to the current working directory using this exact shell pattern (note the quoting — required because the path contains spaces):
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Cap Table Template.xlsx" 2>/dev/null | head -1)
OUTPUT="./$SANITIZED_TICKER - Capitalization Table.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

Then verify the output file exists and has non-zero size:
```bash
ls -lh "$OUTPUT"
```

**If the result is `COPY_FAILED`, the file is missing, or its size is 0 bytes — STOP immediately. Do NOT proceed. Do NOT create a manual cap table or output data in any other format. Tell the user:**

> "I could not copy the INFOR Cap Table Template. Please confirm the file `INFOR Cap Table Template.xlsx` exists in the `templates/` folder at the root of the `infor-workflows` plugin repository."

---

### Step 3 — Update Header Inputs (openpyxl)

Open the copied file with openpyxl (NOT data_only — preserve all formulas).

Update ONLY this cell in the `Cap with Links` sheet:

| Cell | Value |
|------|-------|
| F3 | CapIQ ticker exactly as provided (e.g., `NasdaqGS:MSFT`) |

**Do not modify any other header cells.** Cell F6 already contains a `=TODAY()-1` formula — leave it untouched. Do not modify F4, F5, F7, F10, F11, or any formula cells.

---

### Step 4 — Extract Financial Data

Read the attached documents and extract all items listed in the Domain Reference section below. Use the most recent balance sheet date available.

**Source tracking:** For every value extracted, record its source in this format:
`"[Document Name] - Page [#], [Section Name]"`
You will attach these as cell comments in Step 5.

---

### Step 5 — Write Extracted Data to Excel

**CRITICAL: All extracted data must be written into the copied INFOR template .xlsx file using openpyxl. Never output the data as a markdown table, plain text, or any format other than the .xlsx file. If openpyxl is not available, stop and tell the user: "Please install openpyxl: `pip install openpyxl`"**

Using openpyxl (write mode, preserve formulas — do NOT use data_only=True):

Write each section into the correct rows and columns per the Template Row Map below. Use Python `datetime.date` objects for date cells and numeric values (not strings) for amount cells.

**Color coding:** Apply blue text `Font(color="0000FF")` to every hardcoded value cell you write. Do NOT recolor formula cells.

**Cell comments:** Attach a single openpyxl `Comment` to the **first cell in each row** (col B). One comment per row only:
```python
from openpyxl.comments import Comment
ws["B91"].comment = Comment("Rogers 2024 Annual Report - Page 87, Note 12: Long-Term Debt", "INFOR")
```

**Never write to formula total cells** E73, F73, F75, F76, F77, F87, F99, F111, F123, F137.

Write the file.

---

### Step 6 — Recalculate and Verify

Run the recalc script if available:
```bash
python "[xlsx_skill_scripts_path]/recalc.py" "./[SANITIZED_TICKER] - Capitalization Table.xlsx"
```

If unavailable, skip this step. Then check for `#REF!`, `#DIV/0!`, `#VALUE!`, or `#NAME?` errors in cells you wrote and fix any found.

Perform the cross-checks listed in the Domain Reference below before delivering.

---

### Step 7 — Summary

Report to the user:

1. **Output file:** path to the saved file
2. **CapIQ auto-populated fields** (will refresh when file is opened in Excel with CapIQ connection): share price, company name, FYE, currency, report dates, revenue & EBITDA consensus estimates, analyst coverage, average target price
3. **Fields populated from MD&A:** list each section and what was found
4. **Items not found:** any line items missing from the attached documents (user should fill these manually in blue)
5. **Reminder:** Open in Excel with the CapIQ add-in active to refresh market data

---

## Domain Reference

### Template Row Map

| Section | Description | Input Columns | Rows | Formula Totals (do NOT overwrite) |
|---------|-------------|---------------|------|----------------------------------|
| Header | Ticker | F3 | — | — |
| I | Preferred Shares, NCI | F52, F53 | — | — |
| II | Options / Warrants / RSUs / DSUs | B (type), C (amount, M shares), D (strike) | 57–72 | E73, F73, F75, F76, F77 |
| III | Convertible Debentures / Preferred | B (type), C (face, $M), D (shares/1000), E (strike) | 81–86 | F87 |
| IV | Debt Schedule | B (facility), E (maturity date), F (amount, $M) | 91–98 | F99 |
| V | Lease Obligations | B (type), E (date), F (amount, $M) | 103–110 | F111 |
| VI | Cash & Equivalents | B (type), E (date), F (amount, $M) | 115–122 | F123 |
| VII | Basic Shares Outstanding | B (description), E (date), F (amount, M shares) | 127–136 | F137 |

**Never write to formula total cells** E73, F73, F75, F76, F77, F87, F99, F111, F123, F137. These are SUM/formula cells that auto-total the rows above them.

### Unit Conventions

- **Always match the template's existing unit.** The template uses millions for all figures.
  - Filing reports in **thousands** → divide by 1,000
  - Filing reports in **full units** (e.g., 22,841,361 shares) → divide by 1,000,000
  - Filing already in **millions** → enter as-is
- **Currency:** Never convert — input exactly as stated in the filing.
- **Dates:** Use the balance sheet date for debt, cash, and lease figures. For shares (Section VII col E), use the subsequent-event date from the capital stock note.

### Cell Comments — Source Citations

Every hardcoded cell must have an openpyxl `Comment` attached (one per row, on col B):
```
"[Document Name] - Page [#], [Section Name]"
```
Examples:
- `"Rogers 2024 Annual Report - Page 87, Note 12: Long-Term Debt"`
- `"MSFT 2024 10-K - Page 14, Consolidated Balance Sheet"`

### GAAP vs. IFRS Differences

| Item | US GAAP | IFRS |
|------|---------|------|
| Debt note label | "Long-Term Debt" | "Borrowings" or "Loans and Borrowings" |
| Lease standard | ASC 842 — finance + operating leases separately | IFRS 16 — single lease liability, row 103 only |
| Equity comp note | "Stock-Based Compensation" | "Share-Based Payments" |

**IFRS lease:** Write F103 as a formula `ws["F103"] = current + noncurrent` — not a scalar. Leave row 104 blank.

### Where to Find Each Data Item

**Basic Shares Outstanding:** Capital stock note — use the subsequent-event date (e.g., "As at Feb 18, 2026, 22,841,361 shares outstanding"). Divide full-unit counts by 1,000,000.

**Cash:** Balance sheet first line of current assets. Also capture short-term investments and restricted cash separately.

**Long-Term Debt:** "Long-Term Debt" or "Borrowings" footnote. Enter each tranche at face value; add a separate negative row for unamortized discount/issuance costs. Always include the revolving credit facility even at $0 — label "Revolving Credit Facility (undrawn)".

**Leases:** ASC 842 or IFRS 16 footnote. Use the discounted lease liability balance, not undiscounted payments.

**Options/Warrants/RSUs/DSUs:** Stock-based compensation footnote. Enter one row per exercise-price tranche for options — do NOT aggregate to WAEP. RSUs/DSUs use $0 strike. **Always exclude PSUs.**

**Convertible Debentures:** Face amount (col C), shares per $1,000 face = 1,000 / conversion price (col D), conversion price (col E).

**Preferred Shares / NCI:** Balance sheet equity section. Enter 0 if none.

### Fallback — No Documents Attached

- **US filers:** `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[ticker]&type=10-K`
- **Canadian filers:** `https://www.sedarplus.ca`

### Common Pitfalls

| Issue | Guidance |
|-------|----------|
| Face vs. carrying value | Enter face value; add negative row for issuance costs |
| Revolver at $0 | Always include — label "Revolving Credit Facility (undrawn)" |
| IFRS leases | Write F103 as formula, not scalar; leave row 104 blank |
| PSUs | Always exclude from Section II |
| Options aggregated | Enter one row per tranche, not single WAEP row |
| Shares date | Use capital stock note subsequent-event date, not balance sheet date |
| RSU/DSU strike | Use $0 |
| Convertible preferred | If convertible → Section III; if not → F52 |

### Cross-Checks

1. F17 (Basic Shares) = F137 — formula-linked
2. F99 (Total Debt) should tie to balance sheet carrying value
3. F123 (Total Cash) should be positive
4. Section II contains no PSUs
5. Revolver appears in Section IV even at $0
6. IFRS: only row 103 populated in Section V; row 104 blank
7. Options appear as one row per tranche, not single WAEP row
8. Section VII col E dates reflect capital stock note subsequent-event date
