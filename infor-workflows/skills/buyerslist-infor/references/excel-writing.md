# Writing the Buyers List Workbook (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

## ⚠️ Preserve Template Formatting — Do NOT Touch It

The template already contains every piece of formatting the output needs: gridlines hidden, buyer-row heights and wrap-text set, column widths sized, and Tier A/B/C conditional formatting (bold green / yellow / red font on the Tier column) applied on every buyer sheet. Every run that has modified this formatting has produced a broken output. Specifically, on every buyer sheet:

- **Do NOT add, modify, or remove conditional formatting.** The template's Tier CF rules already live on `H5:H24` (Strategic), `I5:I24` (Financial), and `G5:G24` (Other Buyers). Do not call `ws.conditional_formatting.add(...)` or touch `ws.conditional_formatting` in any way. In particular, do not apply Excel's built-in "Good / Neutral / Bad" (pastel green/yellow/pink fills) styles — those are the classic default dxfs and will override the template's bold-font styling.
- **Do NOT touch `ws.sheet_view`.** Reassigning `ws.sheet_view`, creating a `SheetView()`, or setting `showGridLines` flips gridlines back on in the saved file. The template has already set `showGridLines="0"` — leave it alone.
- **Do NOT insert or delete columns** on any buyer sheet (`ws.insert_cols`, `ws.delete_cols`). Column widths and the trailing buffer column come from the template — modifying them leaves stray narrow columns or gaps in the column-dimensions list.
- **Do NOT reassign `ws.row_dimensions[r]`** wholesale. Setting a specific row height (e.g. resetting total-row heights in Step 7b) is fine; replacing the whole dimension object is not.
- **Row deletion is only permitted in Step 7b** (trimming unused buyer rows between the last buyer and the tier-total rows). No other row operations.
- **You may** only write cell values, write formulas, and in Step 7c copy individual cell styling (font/fill/border/alignment/number_format) onto the new Summary rows 17 and 18. Nothing else.

If, after loading the copied template and writing cell values, the output appears to be missing gridlines-off, conditional formatting, or correct columns — **stop and investigate**. The cause is upstream (wrong template copy, bad openpyxl version, etc.), not something to patch by layering on extra formatting.

## Step 7 — Write Cell Values

### Sheet 1 — `Summary`

Write target company info to column C:

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

### Sheet 2 — `Strategic Buyers`

One row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Vertical | `str` |
| E | Revenue (C$MM) | `float`/`int` or skip if unknown |
| F | M&A activity | `str` — up to 3 deals as `"Target - YY, Target - YY, Target - YY"` |
| G | Rationale | `str` — 1 concise sentence, ~100–230 chars |
| H | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_strategic` = the number of strategic buyer rows written.

**Never write to rows 25–27 before row removal** — these are COUNTIF total rows.

### Sheet 3 — `Financial Buyers`

One row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Fund Size (C$B) | `float`/`int` or skip if unknown |
| E | Avg. Deal Size (C$MM) | `float`/`int` or skip if unknown |
| F | Sector Focus | `str` |
| G | Portfolio Companies | `str` — up to 3 portcos as `"Name (Current), Name (Exited), Name (Current)"` |
| H | Rationale | `str` — 1 concise sentence, ~100–230 chars |
| I | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_financial` = the number of financial buyer rows written.

### Sheet 4 — `Other Buyers`

Only write this sheet if `include_other = True`. One row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Vertical | `str` |
| E | Transactions | `str` — up to 3 deals as `"Target - YY, Target - YY, Target - YY"` |
| F | Rationale | `str` — 1 concise sentence, ~100–230 chars |
| G | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_other` = the number of other buyer rows written.

## Step 7b — Remove Empty Rows and Rewrite Totals

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

## Step 7c — Handle the Other Buyers Sheet and Summary Total Row

The template ships with an `Other Buyers` tab and a `Total` row at Summary row 17. Finalize both based on `include_other`.

### Case A — `include_other = False` (user declined the third category)

1. Delete the `Other Buyers` sheet entirely:
   ```
   del wb["Other Buyers"]
   ```
2. Leave the Summary sheet unchanged — `Total` stays at row 17 with its existing `=SUM(C15:C16)` formulas.

### Case B — `include_other = True` (user specified a category)

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
