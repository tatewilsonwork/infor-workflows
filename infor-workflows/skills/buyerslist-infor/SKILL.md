---
name: buyerslist-infor
description: >
  Use this skill when the user asks to build a buyer list, buyer universe, or potential acquirer list
  for a company in a sell-side M&A process. Activates on /buyerslist-infor, "buyer list", "buyer universe",
  "potential acquirers", "who would buy", "strategic buyers", "financial sponsors", or "sell-side process".
  Populates the INFOR Buyers List Template with strategic and financial buyers, tiered A/B/C, plus an
  optional third category (e.g., family offices, international strategics, sovereign wealth, SPACs)
  when the user wants buyers that don't fit cleanly as Strategic or Financial.
version: 2.10.0
allowed-tools: [Read, Bash, Write, Glob, WebSearch]
---

# INFOR Buyers List — Workflow

This skill builds a buyer universe for a sell-side M&A process by identifying strategic and financial buyers, tiering them A/B/C, and writing the results into the INFOR Buyers List Template.

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. Template location and working directory are resolved inline in Step 6.

**Detailed references** (loaded on demand):
- [`references/buyer-categories.md`](references/buyer-categories.md) — Strategic / Financial / Other category definitions, tiering criteria, transactions-format table by category, character limits, currency conventions, quality rules
- [`references/rationale-style.md`](references/rationale-style.md) — IB-voice writing guide for the Rationale column (length, register, content by buyer type, strong vs. weak examples)
- [`references/excel-writing.md`](references/excel-writing.md) — full Steps 7, 7b, 7c (openpyxl details — cell maps for each sheet, COUNTIF rewriting after row deletion, Other Buyers sheet handling, template-formatting preservation rules)

---

## Workflow Steps

### Step 1 — Collect Input

Ask the user for the following if not already provided:

> "Please provide:
> - **Company name** and a brief description of the business
> - **Any buyer preferences** — specific buyers to include or exclude, or a preference toward strategic vs. financial buyers
>
> I'll research the rest."

Wait for a company name before proceeding.

Then ask a **separate follow-up** about an additional buyer category beyond Strategic and Financial:

> "Would you like me to also build a third list of buyers that don't fit cleanly into Strategic or Financial? Common examples: **Family Offices**, **International Strategic Buyers**, **Sovereign Wealth Funds**, **Consortium Buyers**, **SPACs**, or any other category specific to this process.
>
> Reply with the **category name** you'd like (e.g., "Family Offices") or **"no"** to skip."

Record the user's response as `other_label`:
- If the user answers `"no"`, `"skip"`, `"none"`, or declines → set `include_other = False`.
- Otherwise → set `include_other = True` and capture `other_label` as the exact buyer category name provided (trimmed, title-cased). `other_label` is only used as the row label on the Summary sheet (cell B17) — it is **not** used as an Excel sheet name, so no length or character-set restrictions apply. The tab itself stays titled `Other Buyers`.

---

### Step 2 — Research the Target

Use WebSearch to gather the following for the Summary sheet:

| Field | What to find |
|-------|-------------|
| Company | Full legal name |
| Headquarters | City, Province/State, Country |
| Founded | Year founded |
| Employees | Approximate headcount |
| Revenue | Most recent annual revenue (note currency) |
| Ownership | Public / Private / PE-backed / Family-owned |
| Key Business Lines | 1–2 sentence description of main products/services |
| Key Value Drivers | Top 2–3 strategic assets (e.g., customer base, IP, recurring revenue, market position) |

---

### Step 3 — Identify Strategic Buyers

Research potential strategic acquirers across the four categories defined in [`references/buyer-categories.md`](references/buyer-categories.md) (Direct Competitors, Adjacent Players, Vertical Integrators, Platform Builders). Aim for **15–20 total** strategic buyers.

For each strategic buyer, gather:
- **Buyer name** — use the common trading/brand name, keep concise
- **HQ** — City, Country (abbreviated)
- **Vertical** — their primary industry vertical (abbreviated)
- **Rev. (C$MM)** — estimated annual revenue in Canadian dollars; convert if USD/other, enter as numeric or leave blank if unknown
- **M&A activity** — up to **3** most relevant recent acquisitions, formatted as `"Target Name #1 - YY, Target Name #2 - YY, Target Name #3 - YY"` where `YY` is the 2-digit year the deal was announced. If more than 3 deals exist, select the most relevant (by sector/thesis fit first, then recency). Leave blank if no disclosed M&A.
- **Rationale** — professional IB-style explanation of why this buyer is a strong fit for the target (see [`references/rationale-style.md`](references/rationale-style.md))
- **Tier** — A, B, or C (see Tiering Criteria in [`references/buyer-categories.md`](references/buyer-categories.md))

---

### Step 4 — Identify Financial Buyers

Research PE/financial sponsors across the three categories defined in [`references/buyer-categories.md`](references/buyer-categories.md) (Platform Investors, Add-on Buyers, Growth Equity). Aim for **10–15 total** financial buyers.

For each financial buyer, gather:
- **Buyer name** — fund/firm name
- **HQ** — City, Country (abbreviated)
- **Fund Size (C$B)** — most recent fund size in C$ billions; numeric or blank if unknown
- **Avg. Deal Size (C$MM)** — typical deal size range midpoint in C$ millions; numeric or blank if unknown
- **Sector Focus** — 1–2 word description of their investment focus
- **Portfolio Companies** — up to **3** most relevant portfolio companies in the sector, formatted as `"PortCo Name #1 (Current), PortCo Name #2 (Exited), PortCo Name #3 (Current)"`. Use `(Current)` for live holdings and `(Exited)` for realized investments. If more than 3 exist, select the most relevant. Leave blank if none in-sector.
- **Rationale** — professional IB-style explanation (see [`references/rationale-style.md`](references/rationale-style.md)); name the specific portfolio company for bolt-on theses
- **Tier** — A, B, or C

---

### Step 4b — Identify Other Buyers (Conditional)

**Skip this step entirely if `include_other = False`.**

If `include_other = True`, research **5–10 buyers** that fit the user-specified `other_label` category. Use the same quality bar as Strategic/Financial — names must be specific, researched, and justified.

For each Other buyer, gather:
- **Buyer name** — common name, concise
- **HQ** — City, Country (abbreviated)
- **Vertical** — primary vertical or investment focus (abbreviated)
- **Transactions** — up to **3** most relevant recent transactions. The *type* of transaction must fit the buyer category — see the format table in [`references/buyer-categories.md`](references/buyer-categories.md). Leave blank if none disclosed.
- **Rationale** — IB-style explanation (see [`references/rationale-style.md`](references/rationale-style.md))
- **Tier** — A, B, or C

Do not mix transaction types within a single sheet — every row on the Other Buyers tab should use the same transaction convention, so a reader can scan the column without recalibrating.

---

### Step 5 — Tier All Buyers

Assign every buyer a tier (A / B / C) per the criteria in [`references/buyer-categories.md`](references/buyer-categories.md). Total buyers across all sheets must not exceed 60 (max 20 per sheet).

**Quality over quantity** — a focused list of 30–50 well-researched buyers beats a list of 200 names.

---

### Step 6 — Locate and Copy the Template

Resolve the template via the plugin's shared helper:
```bash
bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Buyers List Template.xlsx"
```

Sanitize the company name for use as a filename via the shared helper:
```bash
SANITIZED_COMPANY_NAME=$(bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/sanitize_name.sh" "$COMPANY_NAME")
```

Copy the template to the current working directory:
```bash
TEMPLATE=$(bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Buyers List Template.xlsx")
OUTPUT="./$SANITIZED_COMPANY_NAME - Buyers List.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

**If the result is `COPY_FAILED` or the file is missing — STOP immediately.** Do NOT create a manual buyers list. Tell the user the template could not be located.

---

### Step 7 — Write to Excel (openpyxl)

See [`references/excel-writing.md`](references/excel-writing.md) for the full Steps 7, 7b, and 7c implementation. Highlights:

- **Step 7**: write cell values per the cell maps in each sheet (Summary C4:C11, then buyer rows starting at row 5 on each buyer sheet).
- **Step 7b**: after writing buyers, physically delete unused rows on each buyer sheet, then **explicitly rewrite the COUNTIF formulas at the new locations** (openpyxl does not translate the references for you). Reset the tier-total row heights back to 14.25 pt. Update the cross-sheet COUNTIF references on the Summary sheet.
- **Step 7c**: handle the `Other Buyers` sheet — delete it if `include_other = False`; if `include_other = True`, **do NOT rename the tab** (rename corrupts gridlines/columns/CF in openpyxl), instead write `other_label` to Summary `B17`, add a new Total row at 18, and copy styling from rows 16/17.

**Preserve template formatting — do NOT touch:** conditional formatting, `ws.sheet_view`, column dimensions, or row dimensions (other than the specific height resets in 7b). The template ships every formatting setting the output needs.

Save the file after Step 7c.

---

### Step 8 — Summary

Report to the user:

1. **Output file:** path to the saved file
2. **Strategic Buyers:** count by tier (e.g., "8 Tier A, 7 Tier B, 4 Tier C")
3. **Financial Buyers:** count by tier
4. **Other Buyers** (only if `include_other = True`): count by tier, labelled with `other_label`
5. **Notable Tier A buyers:** briefly highlight the strongest 2–3 names and why
6. **Reminder:** Review the list and add any relationship-specific buyers or exclusions manually before distributing

---

## Domain Reference

### Template Cell Map

| Sheet | Write range | Formula rows (initial) | Notes |
|-------|-------------|------------------------|-------|
| Summary | C4:C11 | Rows 13–17 | C15:E16 cross-reference Strategic/Financial — rewrite after Step 7b. If `include_other=True`, row 17 becomes the Other Buyers cross-reference and Total shifts to row 18 (Step 7c). |
| Strategic Buyers | B5:H24 (max 20 rows) | Rows 25–27 | Totals shift up after Step 7b empty-row deletion |
| Financial Buyers | B5:I24 (max 20 rows) | Rows 25–27 | Totals shift up after Step 7b empty-row deletion |
| Other Buyers (optional) | B5:G24 (max 20 rows) | Rows 25–27 | Sheet is deleted if `include_other=False`. If `include_other=True`, the tab stays titled `Other Buyers` (never renamed) and the category name is written to Summary cell B17. Totals shift up after Step 7b empty-row deletion. |

The buyer data rows have pre-set row height (~28.5pt) and `wrap_text=True` on the Rationale column so longer professional-language rationales render cleanly without manual formatting.

For category definitions, character limits, transaction-format conventions, currency rules, and quality rules see [`references/buyer-categories.md`](references/buyer-categories.md).
