---
name: buyerslist-infor
description: >
  Use this skill when the user asks to build a buyer list, buyer universe, or potential acquirer list
  for a company in a sell-side M&A process. Activates on "buyer list", "buyer universe",
  "potential acquirers", "who would buy", "strategic buyers", "financial sponsors", or "sell-side process".
  Populates the INFOR Buyers List Template with strategic and financial buyers, tiered A/B/C, plus an
  optional third category (e.g., family offices, international strategics, sovereign wealth, SPACs)
  when the user wants buyers that don't fit cleanly as Strategic or Financial.
version: 1.8.0
---

# INFOR Buyers List — Workflow & Domain Knowledge

This skill builds a buyer universe for a sell-side M&A process by identifying strategic and financial buyers, tiering them A/B/C, and writing the results into the INFOR Buyers List Template.

Allowed tools: Read, Bash, Write, Glob, WebSearch

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Buyers List Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

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

Research potential strategic acquirers across these four categories. Aim for **15–20 total** strategic buyers.

**Direct Competitors** — companies in the same space gaining market share, revenue synergies, eliminating a competitor

**Adjacent Players** — companies in adjacent markets that could expand via acquisition; product extension, cross-sell, new market entry

**Vertical Integrators** — customers or suppliers that could integrate vertically; supply chain control, margin capture, strategic lock-in

**Platform Builders** — large companies building a platform in the space through M&A; tuck-in acquisition, capability gap fill

For each strategic buyer, gather:
- **Buyer name** — use the common trading/brand name, keep concise
- **HQ** — City, Country (abbreviated)
- **Vertical** — their primary industry vertical (abbreviated)
- **Rev. (C$MM)** — estimated annual revenue in Canadian dollars; convert if USD/other, enter as numeric or leave blank if unknown
- **M&A activity** — up to **3** most relevant recent acquisitions, formatted as `"Target Name #1 - YY, Target Name #2 - YY, Target Name #3 - YY"` where `YY` is the 2-digit year the deal was announced. If more than 3 deals exist, select the most relevant (by sector/thesis fit first, then recency). Leave blank if no disclosed M&A.
- **Rationale** — professional IB-style explanation of why this buyer is a strong fit for the target (see **Rationale Writing Guidelines** below)
- **Tier** — A, B, or C (see Tiering Criteria below)

---

### Step 4 — Identify Financial Buyers

Research PE/financial sponsors across these three categories. Aim for **10–15 total** financial buyers.

**Platform Investors** — sponsors looking to establish a new platform in this sector; consider fund size, sector focus, and deal size range

**Add-on Buyers** — sponsors with existing portfolio companies that could acquire the target as a bolt-on; identify the specific portfolio company and the synergy rationale

**Growth Equity** — for earlier-stage or high-growth targets; minority or majority investors

For each financial buyer, gather:
- **Buyer name** — fund/firm name
- **HQ** — City, Country (abbreviated)
- **Fund Size (C$B)** — most recent fund size in C$ billions; numeric or blank if unknown
- **Avg. Deal Size (C$MM)** — typical deal size range midpoint in C$ millions; numeric or blank if unknown
- **Sector Focus** — 1–2 word description of their investment focus
- **Portfolio Companies** — up to **3** most relevant portfolio companies in the sector, formatted as `"PortCo Name #1 (Current), PortCo Name #2 (Exited), PortCo Name #3 (Current)"`. Use `(Current)` for live holdings and `(Exited)` for realized investments. If more than 3 exist, select the most relevant (by sector/thesis fit first, then recency). Leave blank if none in-sector.
- **Rationale** — professional IB-style explanation of why this sponsor is a strong fit: name the specific portfolio company for bolt-on theses, or articulate the platform/growth thesis for new-platform theses (see **Rationale Writing Guidelines** below)
- **Tier** — A, B, or C (see Tiering Criteria below)

---

### Step 4b — Identify Other Buyers (conditional)

**Skip this step entirely if `include_other = False`.**

If `include_other = True`, research **5–10 buyers** that fit the user-specified `other_label` category. Use the same quality bar as Strategic/Financial — names must be specific, researched, and justified.

Tailor the research lens to the category. Examples:

| Category | What to look for |
|---|---|
| Family Offices | Active direct investors, sector familiarity, typical cheque size, recent deals |
| International Strategic Buyers | Foreign strategics with disclosed interest in the target's geography, FX/tax considerations, precedent cross-border deals |
| Sovereign Wealth Funds | Mandate fit (infra/financials/tech), direct-deal capacity, recent co-investments |
| Consortium Buyers | Plausible PE + strategic pairings, prior consortium precedents |
| SPACs | Live SPACs with sector fit, trust size vs. target EV, deadline proximity |

For each Other buyer, gather:
- **Buyer name** — common name, concise
- **HQ** — City, Country (abbreviated)
- **Vertical** — primary vertical or investment focus (abbreviated)
- **Transactions** — up to **3** most relevant recent transactions. The *type* of transaction must fit the buyer category — see the table below. Leave blank if none disclosed.
- **Rationale** — professional IB-style explanation of why this buyer fits (see **Rationale Writing Guidelines** below)
- **Tier** — A, B, or C (see Tiering Criteria below)

**Category-specific Transactions guidance.** The Transactions column must reflect the kind of activity the category actually does — an acquirer's M&A, an investor's rounds, a funder's cases. Pick the format that matches:

| Category | What "Transactions" means | Format example |
|---|---|---|
| Family Offices | Recent direct deals / investments | `"Target - YY, Target - YY, Target - YY"` |
| International Strategic Buyers | Recent cross-border M&A | `"Target - YY, Target - YY, Target - YY"` |
| Sovereign Wealth Funds | Recent direct deals / co-investments | `"Target - YY, Target - YY, Target - YY"` |
| SPACs | Prior de-SPAC targets / announced combinations | `"Target - YY, Target - YY"` |
| Consortium Buyers | Prior consortium transactions | `"Target (with Co-Investor) - YY, Target - YY"` |
| Venture Capital / Growth Equity | Portfolio rounds led/co-led | `"PortCo (Series B) - YY, PortCo (Seed) - YY, PortCo (Series A) - YY"` |
| Litigation Funders | Notable cases / litigations funded | `"Case name - YY, Case name - YY, Case name - YY"` |
| Corporate Venture Arms | Portfolio rounds participated in | `"PortCo (Series B) - YY, PortCo (Seed) - YY"` |
| Any other | Choose the transaction type that most naturally represents the category's activity (deals for acquirers, rounds for investors, cases for funders). If the choice is non-obvious, briefly note the convention used in the Rationale. |

Do not mix transaction types within a single sheet — every row on the Other Buyers tab should use the same transaction convention, so a reader can scan the column without recalibrating.

---

### Rationale Writing Guidelines

The Rationale column on both sheets uses wrapped text with tall rows to accommodate professional, IB-style prose — but keep it tight.

**Length:** 1 concise sentence (rarely 2), typically 100–230 characters. Scannable on a printed page. Cut any word that does not add a thesis-level fact.

**Voice and register:**
- Write in declarative, analytical, client-facing investment banking language
- Lead with the strategic/financial thesis, not the buyer's history
- Use precise business vocabulary ("platform extension", "vertical integration", "geographic whitespace", "revenue synergies", "cross-sell", "recurring revenue mix", "deployment mode", "bolt-on", "margin accretion")
- Avoid hype, hedges, and generic filler ("great fit", "synergies abound", "obvious acquirer")
- No bullets, no sentence fragments, no abbreviations inside the rationale itself (spell out "management" not "mgmt")

**Content by buyer type:**

| Buyer type | What the rationale must answer |
|---|---|
| Direct Competitor | What share/scale/cost benefit is unlocked? Any anti-trust overhang? |
| Adjacent Player | Which adjacent capability/segment does the target fill? Why now? |
| Vertical Integrator | What margin or supply-chain control is captured? |
| Platform Builder | How does the target advance the acquirer's stated M&A roadmap? |
| PE — Platform | Why is this target the right first platform investment in the sector for the fund? Mention fund vintage/deployment mode if relevant. |
| PE — Add-on | Name the specific portfolio company and the operational or commercial synergy with the target. |
| PE — Growth Equity | What is the growth thesis (revenue CAGR, TAM, path to scale)? |

**Strong examples:**

- *Strategic (Adjacent Player):* "Extends CI Financial's wealth platform into the Quebec HNW segment, complementing its Ontario advisor network and adding ~C$4B in recurring-revenue AUM."
- *Strategic (Platform Builder):* "Aligns with Power Corp's stated strategy to consolidate mid-market Canadian asset managers and broadens its product shelf into alternative fixed income."
- *PE Add-on:* "Natural bolt-on to Onex portfolio company WealthOne, where the target's advisor base and Quebec footprint expand WealthOne's national distribution."
- *PE Platform:* "Birch Hill is deploying its recently closed C$1.4B Fund VI against financial services platforms; target fits its recurring-revenue, asset-light profile."

**Weak examples (do not write these):**

- "Good fit for wealth expansion" — too short, no specificity
- "Would synergize well with buyer's portfolio" — filler, no thesis
- "Active acquirer in the space" — belongs in the M&A activity column, not Rationale

---

### Step 5 — Tier All Buyers

Assign every buyer a tier:

| Tier | Target Count | Criteria |
|------|-------------|---------|
| A | 5–10 | Highest strategic/financial fit, proven acquirers in the sector, clear and compelling rationale |
| B | 10–15 | Good fit but less obvious; less active M&A track record or smaller size |
| C | Remainder | Possible but lower probability; include to broaden the process if needed |

Total buyers across all sheets must not exceed **60** (20 strategic + 20 financial + 20 other, maximum per sheet). The Other sheet is optional; it is only populated when `include_other = True` (Step 4b).

**Quality over quantity** — a focused list of 30–50 well-researched buyers beats a list of 200 names.

---

### Step 6 — Locate and Copy the Template

The template path is shown in the Context section above. If blank, search for it:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Buyers List Template.xlsx" 2>/dev/null | head -1
```

Sanitize the company name for use as a filename (remove special characters, replace spaces with hyphens).

Copy the template to the current working directory:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Buyers List Template.xlsx" 2>/dev/null | head -1)
OUTPUT="./$SANITIZED_COMPANY_NAME - Buyers List.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

**If the result is `COPY_FAILED` or the file is missing — STOP immediately. Do NOT create a manual buyers list. Tell the user:**

> "I could not copy the INFOR Buyers List Template. Please confirm the file `INFOR Buyers List Template.xlsx` exists in the `templates/` folder of the infor-workflows plugin."

---

### Step 7 — Write to Excel (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

**Sheet 1 — `Summary`:** Write target company info to column C:

| Cell | Value |
|------|-------|
| C4 | Company name |
| C5 | Headquarters |
| C6 | Founded (year) |
| C7 | Employees |
| C8 | Revenue |
| C9 | Ownership |
| C10 | Key Business Lines |
| C11 | Key Value Drivers |

**Do not write to rows 13–17 in Step 7** — these contain headers and COUNTIF formula links. Row 17 (and a new row 18) are rewritten in Step 7c only when `include_other = True`.

**Sheet 2 — `Strategic Buyers`:** Write one row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Vertical | `str` |
| E | Revenue (C$MM) | `float`/`int` or skip if unknown |
| F | M&A activity | `str` — up to 3 deals as `"Target - YY, Target - YY, Target - YY"` |
| G | Rationale | `str` — 1 concise sentence (rarely 2), ~100–230 chars (see Rationale Writing Guidelines) |
| H | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_strategic` = the number of strategic buyer rows written.

**Never write to rows 25–27 before row removal** — these are COUNTIF total rows.

**Sheet 3 — `Financial Buyers`:** Write one row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Fund Size (C$B) | `float`/`int` or skip if unknown |
| E | Avg. Deal Size (C$MM) | `float`/`int` or skip if unknown |
| F | Sector Focus | `str` |
| G | Portfolio Companies | `str` — up to 3 portcos as `"Name (Current), Name (Exited), Name (Current)"` |
| H | Rationale | `str` — 1 concise sentence (rarely 2), ~100–230 chars (see Rationale Writing Guidelines) |
| I | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_financial` = the number of financial buyer rows written.

**Never write to rows 25–27 before row removal** — these are COUNTIF total rows.

**Sheet 4 — `Other Buyers`:** Only write this sheet if `include_other = True`. One row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Vertical | `str` |
| E | Transactions | `str` — up to 3 deals as `"Target - YY, Target - YY, Target - YY"` |
| F | Rationale | `str` — 1 concise sentence (rarely 2), ~100–230 chars (see Rationale Writing Guidelines) |
| G | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_other` = the number of other buyer rows written.

**Never write to rows 25–27 before row removal** — these are COUNTIF total rows.

---

### Step 7b — Remove Empty Rows and Rewrite Totals

After writing all buyers, physically delete the unused data rows so the Tier totals sit directly below the last populated buyer on each sheet. This keeps the output clean for print/PDF distribution.

Do this **before saving** and **for each buyer sheet independently**.

For each buyer sheet — do Strategic first, then Financial, then Other (if `include_other = True`). The sheets are independent so row deletions on one do not affect the others:

1. Let `n` = number of buyers written on that sheet (`n_strategic`, `n_financial`, or `n_other`).
2. Let `last_data_row = 4 + n` (data starts at row 5).
3. Let `first_empty = last_data_row + 1` and `last_empty = 24`.
4. If `first_empty <= last_empty`, delete the empty rows: `ws.delete_rows(first_empty, last_empty - first_empty + 1)`.
5. After deletion, the three tier-total rows (previously 25, 26, 27) now sit at `last_data_row + 1`, `+ 2`, `+ 3`. **Explicitly rewrite the COUNTIF formulas** at the new locations so they reference the correct shortened data range — do not rely on openpyxl to translate them.

   - **Strategic Buyers** (tier column is `H`):
     ```
     ws[f"H{last_data_row + 1}"] = f'=COUNTIF($H$5:$H${last_data_row},"A")'
     ws[f"H{last_data_row + 2}"] = f'=COUNTIF($H$5:$H${last_data_row},"B")'
     ws[f"H{last_data_row + 3}"] = f'=COUNTIF($H$5:$H${last_data_row},"C")'
     ```
   - **Financial Buyers** (tier column is `I`):
     ```
     ws[f"I{last_data_row + 1}"] = f'=COUNTIF($I$5:$I${last_data_row},"A")'
     ws[f"I{last_data_row + 2}"] = f'=COUNTIF($I$5:$I${last_data_row},"B")'
     ws[f"I{last_data_row + 3}"] = f'=COUNTIF($I$5:$I${last_data_row},"C")'
     ```
   - **Other Buyers** (tier column is `G`):
     ```
     ws[f"G{last_data_row + 1}"] = f'=COUNTIF($G$5:$G${last_data_row},"A")'
     ws[f"G{last_data_row + 2}"] = f'=COUNTIF($G$5:$G${last_data_row},"B")'
     ws[f"G{last_data_row + 3}"] = f'=COUNTIF($G$5:$G${last_data_row},"C")'
     ```

5b. **Force the tier-total rows back to height 14.25.** `openpyxl.delete_rows` does not shift `row_dimensions` entries, so the three total rows inherit the 28.5pt height from the old buyer-row dimensions at their new positions. Explicitly reset them (this step is mandatory on every run, even when no rows were deleted, to guarantee the output):
   ```
   for offset in (1, 2, 3):
       ws.row_dimensions[last_data_row + offset].height = 14.25
   ```

6. **Rewrite the Summary sheet cross-sheet references** to point at the new totals rows. Let `strategic_totals_start = 4 + n_strategic + 1` and `financial_totals_start = 4 + n_financial + 1`. On the `Summary` sheet:
   ```
   summary["C15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start}"
   summary["D15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start + 1}"
   summary["E15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start + 2}"
   summary["C16"] = f"=+'Financial Buyers'!$I${financial_totals_start}"
   summary["D16"] = f"=+'Financial Buyers'!$I${financial_totals_start + 1}"
   summary["E16"] = f"=+'Financial Buyers'!$I${financial_totals_start + 2}"
   ```
   The `SUM` totals in column F (`F15`, `F16`) reference only the same-sheet cells and remain correct. The overall `Total` row is handled in Step 7c below.

7. Verify that all buyer sheets still open cleanly and that the tier totals reflect the buyers written (sanity-check: each tier count should be ≥ 0 and the sum across tiers on each sheet should equal `n`).

---

### Step 7c — Handle the Other Buyers Sheet and Summary Total Row

The template ships with an `Other Buyers` tab and a `Total` row at Summary row 17. Finalize both based on `include_other`.

**Case A — `include_other = False` (user declined the third category):**

1. Delete the `Other Buyers` sheet entirely:
   ```
   del wb["Other Buyers"]
   ```
2. Leave the Summary sheet unchanged — `Total` stays at row 17 with its existing `=SUM(C15:C16)` formulas.

**Case B — `include_other = True` (user specified a category):**

**Do NOT rename the `Other Buyers` tab.** Renaming the sheet in openpyxl has been observed to (a) turn sheet gridlines back on, (b) insert a spurious narrow column, and (c) drop the Tier conditional-formatting rules — because `showGridLines`, `column_dimensions`, and `conditional_formatting` do not always transfer cleanly across a rename. Keeping the tab literally titled `Other Buyers` avoids all three issues. The user-specific category name still appears prominently on the Summary sheet (cell B17, written below), so no information is lost.

1. **Capture the styling of the existing rows BEFORE overwriting anything.** The new row 17 should inherit the buyer-row styling from row 16, and the new row 18 should inherit the Total-row styling from the current row 17:
   ```
   from copy import copy
   financial_style = {c.column_letter: (copy(c.font), copy(c.fill), copy(c.border), copy(c.alignment), c.number_format) for c in summary[16]}
   total_style     = {c.column_letter: (copy(c.font), copy(c.fill), copy(c.border), copy(c.alignment), c.number_format) for c in summary[17]}
   financial_row_height = summary.row_dimensions[16].height
   total_row_height     = summary.row_dimensions[17].height
   ```
2. **Write the new row 17 (Other Buyers) and new row 18 (Total).** Let `other_totals_start = 4 + n_other + 1` (the new location of the Tier A total on the `Other Buyers` sheet after Step 7b trimming). Cross-sheet formulas reference the tab by its literal name `'Other Buyers'`. Cell `B17` carries the user-specified `other_label` so a reader still sees exactly which category the row represents:
   ```
   summary["B17"] = other_label
   summary["C17"] = f"=+'Other Buyers'!$G${other_totals_start}"
   summary["D17"] = f"=+'Other Buyers'!$G${other_totals_start + 1}"
   summary["E17"] = f"=+'Other Buyers'!$G${other_totals_start + 2}"
   summary["F17"] = "=SUM(C17:E17)"

   summary["B18"] = "Total"
   summary["C18"] = "=SUM(C15:C17)"
   summary["D18"] = "=SUM(D15:D17)"
   summary["E18"] = "=SUM(E15:E17)"
   summary["F18"] = "=SUM(F15:F17)"

   for col, (font, fill, border, alignment, number_format) in financial_style.items():
       cell = summary[f"{col}17"]
       cell.font, cell.fill, cell.border, cell.alignment, cell.number_format = font, fill, border, alignment, number_format
   for col, (font, fill, border, alignment, number_format) in total_style.items():
       cell = summary[f"{col}18"]
       cell.font, cell.fill, cell.border, cell.alignment, cell.number_format = font, fill, border, alignment, number_format
   if financial_row_height is not None:
       summary.row_dimensions[17].height = financial_row_height
   if total_row_height is not None:
       summary.row_dimensions[18].height = total_row_height
   ```

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
| Other Buyers (optional) | B5:G24 (max 20 rows) | Rows 25–27 | Sheet is deleted if `include_other=False`. If `include_other=True`, the tab stays titled `Other Buyers` (never renamed — rename corrupts gridlines, columns, and conditional formatting in openpyxl) and the category name is written to Summary cell B17. Totals shift up after Step 7b empty-row deletion. |

The buyer data rows have pre-set row height (~28.5pt) and `wrap_text=True` on the Rationale column so longer professional-language rationales render cleanly without manual formatting.

### Character Limits by Column

**Strategic Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars — use common/abbreviated name |
| C | HQ | ~12 chars — e.g., `"Toronto, CA"` |
| D | Vertical | ~12 chars — e.g., `"Wealth Mgmt"` |
| F | M&A activity | Up to 3 deals, `"Target - YY, Target - YY, Target - YY"` format (~60–80 chars typical) |
| G | Rationale | 1 concise sentence (rarely 2), ~100–230 chars (professional IB prose — see Rationale Writing Guidelines) |

**Financial Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| F | Sector Focus | ~12 chars |
| G | Portfolio Companies | Up to 3 portcos, `"Name (Current), Name (Exited), Name (Current)"` format (~60–80 chars typical) |
| H | Rationale | 1 concise sentence (rarely 2), ~100–230 chars (professional IB prose — see Rationale Writing Guidelines) |

**Other Buyers** (only when `include_other=True`):
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| D | Vertical | ~12 chars |
| E | Transactions | Up to 3 deals, `"Target - YY, Target - YY, Target - YY"` format (~60–80 chars typical) |
| F | Rationale | 1 concise sentence (rarely 2), ~100–230 chars (professional IB prose — see Rationale Writing Guidelines) |

### Buyer Category Definitions

**Strategic:**
- **Direct Competitors** — same market, would gain share or eliminate rivalry
- **Adjacent Players** — neighbouring market, looking to expand via acquisition
- **Vertical Integrators** — upstream/downstream player seeking control over the value chain
- **Platform Builders** — acquirer using M&A to build a sector platform (tuck-in logic)

**Financial:**
- **Platform Investors** — establishing a new sector platform; look for funds in deployment mode with sector focus
- **Add-on Buyers** — existing portco that could bolt-on the target; name the specific portco in column G
- **Growth Equity** — minority/majority growth investors; relevant for high-growth or pre-profitability targets

**Other** (user-defined via `other_label` — common examples):
- **Family Offices** — active direct investors; typical cheque size and sector familiarity matter
- **International Strategic Buyers** — foreign strategics with disclosed interest in the target's geography
- **Sovereign Wealth Funds** — mandate-fit funds with direct-deal capacity
- **Consortium Buyers** — plausible PE + strategic pairings with consortium precedent
- **SPACs** — live SPACs with sector fit, adequate trust size, and deadline runway

### Tiering Criteria

| Tier | Criteria |
|------|---------|
| A | Clear strategic or financial fit; active M&A track record; has done comparable deals; motivated; no obvious blockers |
| B | Reasonable fit; less active acquirer or smaller; may need more convincing |
| C | Possible but speculative; include to broaden process if Tier A/B interest is limited |

### Revenue / Fund Size Currency

The template uses **C$ (Canadian dollars)**:
- If source data is in USD, convert at approximate current rate and note the conversion
- Enter revenue as a numeric value (e.g., `450` for C$450MM) — no currency symbols
- Fund size in C$B (e.g., `3.2` for C$3.2B); deal size in C$MM (e.g., `150` for C$150MM)

### Quality Rules

- **30–40 focused buyers** beats 200 names — prioritise fit over volume
- **Research recent M&A** — buyers who just completed a deal in the sector may be hungry for more or temporarily tapped out; flag accordingly in the M&A activity column
- **Antitrust** — flag any direct competitors that may face regulatory scrutiny; note in rationale
- **Fund vintage** — sponsors near end of investment period are more motivated; avoid funds in harvest mode
- **Always ask** if the seller has specific buyers to include or exclude before finalising
