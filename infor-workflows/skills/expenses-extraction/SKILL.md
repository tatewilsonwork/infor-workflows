---
name: expenses-extraction
description: Fill in the INFOR expense report template from attached receipt images. Activates when the user wants to log expenses, submit receipts, or fill out the INFOR expense report.
version: 1.6.0
---

# INFOR Expense Report — Workflow & Domain Knowledge

This skill guides you through reading receipt images and writing the correct values into the INFOR expense report Excel template (IFI sheet only).

Allowed tools: Read, Bash, Write, Glob

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Expense Report Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Collect Inputs

Run immediately without waiting for arguments. Ask the user in a single message:

> "Please attach all receipt images (snips or photos) to your reply."

Wait for at least one receipt image before proceeding.

---

### Step 2 — Locate and Copy the Template

Use the template path shown in the Context section above. If blank, search for it — check the repo's templates directory first, then the plugin cache, then fall back to $HOME:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Expense Report Template.xlsx" 2>/dev/null | head -1
```

Copy the template to the current working directory:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Expense Report Template.xlsx" 2>/dev/null | head -1)
OUTPUT="./[YYYY-MM-DD] Expense Report.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

Use today's date for the filename. **If the result is `COPY_FAILED` — STOP immediately. Do NOT proceed. Tell the user the template could not be found.**

---

### Step 3 — Detect Data Start Row

Open the copied file with openpyxl (**do not** use `data_only=True` — preserve all formulas).

Always use the **IFI** sheet. Scan column B from row 1 downward to find the header row where column B contains "Date" (case-insensitive). The first data row is `header_row + 1`.

Find the **write start row**: the first row at or after the first data row where column B is empty.

---

### Step 4 — Parse Each Attached Receipt

For each attached receipt image, extract using the domain knowledge below:

| Field | What to extract |
|-------|----------------|
| **Date** | Date on the receipt as `datetime.date`; `None` if not visible |
| **Vendor** | Name of the restaurant or travel provider |
| **Category** | `"Meals - Deal Related"` or `"Travel-Deal Related"` |
| **Description** | `"Dinner - [Vendor]"` or `"Travel - [Vendor]"` |
| **Total** | Final total including tip as a float |
| **HST** | Dollar amount only if explicitly labeled on receipt; `None` otherwise |

Process all receipts before writing.

---

### Step 5 — Write to the IFI Sheet

One row per receipt starting at the write start row:

| Column | Value | Rule |
|--------|-------|------|
| **B** | Date (`datetime.date`) | Leave empty if `None` |
| **C** | Description string | Always write |
| **J** | Total amount (float) | Always write |
| **K** | Expense category string | Always write |
| **R** | HST amount (float) | Only write if HST was explicit on the receipt |

Do not write to any other columns. Do not modify rows above the write start row. Save after writing all rows.

---

### Step 6 — Summary

Report to the user:

1. **Output file** path
2. **Receipts processed** — one line per receipt: date, description, amount, category, HST status
3. **Blanks** — any fields left empty and why
4. **Reminder** — open in Excel to fill in remaining columns before submitting

---

## Domain Reference

### Column Map

| Column | Field | Notes |
|--------|-------|-------|
| B | Date | `datetime.date`; leave empty if not visible |
| C | Description | `"Dinner - [Vendor]"` or `"Travel - [Vendor]"` |
| J | Amount Incl Tips | Final total as float |
| K | Expense Category | `"Meals - Deal Related"` or `"Travel-Deal Related"` |
| R | HST | Only overwrite formula if HST explicitly shown on receipt |

Write **only** to columns B, C, J, K, and (conditionally) R. Leave all other columns untouched.

### Description Format

| Receipt type | Column C value |
|-------------|---------------|
| Restaurant / café / bar / food | `"Dinner - [Restaurant Name]"` |
| Uber / Lyft / taxi | `"Travel - [Provider]"` |
| Airline | `"Travel - [Airline]"` |
| Train / bus | `"Travel - [Provider]"` |
| Parking / hotel | `"Travel - [Vendor]"` |

Always use "Dinner" for all food/restaurant receipts regardless of time of day.

### Expense Category Decision Tree

**"Meals - Deal Related"** — restaurant, café, bar, or food delivery.

**"Travel-Deal Related"** — Uber/Lyft/taxi, airline, train/bus, hotel, parking, car rental.

### Amount Rule (Column J)

- Use the final "Total" line on the receipt.
- If tip is shown separately and not yet included, add it to the subtotal.
- **Currency:** If non-CAD, note it and ask the user for the exchange rate — do not convert silently.
- Enter as a plain float, not a formatted string.

### HST Rule (Column R)

The template has an auto-calculate formula in column R. **Only overwrite** when the receipt explicitly shows:
- `HST`, `HST/TVQ`, or `Harmonized Sales Tax`

**Do NOT overwrite** for GST only, QST/PST separately, no tax breakdown, or an ambiguous "Tax" label.

### Date Parsing

Accept: `MM/DD/YYYY`, `DD/MM/YYYY`, `Month DD YYYY`, `MMM DD YYYY`, `YYYY-MM-DD`.

If day/month order is ambiguous, default to **MM/DD/YYYY**. If no date visible, write `None` to column B.

### Common Pitfalls

- Do not write to columns A, D–I, L–Q, S — user-managed or formula columns.
- Do not delete HST formulas — only replace when HST is explicitly confirmed.
- Do not guess the date — blank is better than wrong.
- One receipt = one row always.
- Use the legal/display name from the receipt header (e.g., `"Dinner - Earls Kitchen + Bar"` not `"Dinner - Restaurant"`).
