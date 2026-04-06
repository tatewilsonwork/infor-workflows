---
name: comps-infor
description: Use this skill when the user invokes /comps-infor or asks to build a public comparables table (comps, trading comps, public comps) for a company. Populates the INFOR Comps Template with 8 CapIQ tickers split into two labelled groups.
version: 1.0.0
---

# INFOR Public Comparables Table — Workflow

This skill builds a public comparable companies table by selecting 8 peers and writing their CapIQ tickers plus group labels into the INFOR Comps Template.

Allowed tools: Read, Bash, Write, Glob, WebSearch

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Collect Input

Ask for the target company name if not already provided:

> "Please provide the name of the company you'd like me to build a comparable companies table for."

Wait for the company name before proceeding.

---

### Step 2 — Select 8 Public Comparables

Using your knowledge of public markets (and WebSearch if needed to verify current tickers or identify relevant peers), select **8 publicly traded comparable companies** for the target.

**Grouping logic — choose ONE of the following that best fits:**

- **By Geography** — when the target operates in a specific region and regional peers are meaningful (e.g., Canadian banks, European industrials). Label groups by region (e.g., "Canadian Peers", "U.S. Peers").
- **By Sector / Vertical** — when the target spans geographies but has distinct business lines or sub-sectors. Label groups by business type (e.g., "Core Software", "Payments & FinTech").

Split the 8 comparables into **two groups of exactly 4**. Each group must have a clear, concise label (3–6 words max).

**Ticker format:** Use CapIQ format — `Exchange:Ticker` (e.g., `NasdaqGS:MSFT`, `TSX:RY`, `NYSE:JPM`).

Before proceeding, present the proposed comps to the user in this format and ask for confirmation:

```
**Group 1 — [Label]**
1. Company Name — NasdaqGS:TICK
2. Company Name — NYSE:TICK
3. Company Name — TSX:TICK
4. Company Name — NasdaqGS:TICK

**Group 2 — [Label]**
5. Company Name — NasdaqGS:TICK
6. Company Name — NYSE:TICK
7. Company Name — NasdaqGS:TICK
8. Company Name — NYSE:TICK

Proceed with these comparables, or let me know of any changes.
```

Wait for confirmation or revisions before writing to the file.

---

### Step 3 — Locate and Copy the Template

The template path is shown in the Context section above. If blank, search for it — check the repo's templates directory first, then the plugin cache, then fall back to $HOME:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1
```

Sanitize the target company name for use as a filename (remove special characters, replace spaces with hyphens).

Copy the template to the current working directory:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1)
OUTPUT="./$SANITIZED_COMPANY_NAME - Comparable Companies.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

**If the result is `COPY_FAILED` or the file is missing — STOP immediately. Do NOT create a manual comps table. Tell the user the template could not be found.**

---

### Step 4 — Write to Excel (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

Write **exactly 10 cells** in the `Comps` sheet. No other cells should be touched.

| Cell | Value |
|------|-------|
| B9  | Group 1 label (e.g., `"Canadian Peers"`) |
| B10 | Ticker 1 in CapIQ format (e.g., `"TSX:RY"`) |
| B11 | Ticker 2 |
| B12 | Ticker 3 |
| B13 | Ticker 4 |
| B17 | Group 2 label (e.g., `"U.S. Peers"`) |
| B18 | Ticker 5 |
| B19 | Ticker 6 |
| B20 | Ticker 7 |
| B21 | Ticker 8 |

All 10 values are plain strings. Do not modify any other cell.

Save the file.

---

### Step 5 — Summary

Report to the user:

1. **Output file:** path to the saved file
2. **Group 1 — [Label]:** list the 4 companies with tickers
3. **Group 2 — [Label]:** list the 4 companies with tickers
4. **Reminder:** Open in Excel with the CapIQ add-in active to populate all market data, multiples, and statistics automatically

---

## Domain Reference

### Template Cell Map

| Cell | Purpose |
|------|---------|
| B9  | Group 1 section header (text label) |
| B10–B13 | CapIQ tickers for Group 1 companies (4 rows) |
| B17 | Group 2 section header (text label) |
| B18–B21 | CapIQ tickers for Group 2 companies (4 rows) |

All other cells (D9, D10–D13, D17, D18–D21 and beyond) contain CapIQ array formulas that auto-populate when opened in Excel. **Never overwrite these.**

### CapIQ Ticker Format

| Exchange | Format | Example |
|----------|--------|---------|
| Nasdaq Global Select | `NasdaqGS:TICK` | `NasdaqGS:MSFT` |
| NYSE | `NYSE:TICK` | `NYSE:JPM` |
| TSX | `TSX:TICK` | `TSX:RY` |
| TSX Venture | `TSXV:TICK` | `TSXV:XYZ` |
| London Stock Exchange | `LSE:TICK` | `LSE:HSBA` |
| ASX | `ASX:TICK` | `ASX:CBA` |

### Grouping Guidelines

**Use Geography when:**
- Target is a regional business (e.g., Canadian insurance, Australian banks)
- Investor audience cares about geographic comparability
- Strong regional peer sets exist

**Use Sector / Vertical when:**
- Target is multinational or operates across regions
- Business has distinct lines (e.g., SaaS vs. payments)
- Sector-specific multiples are more meaningful than geography

### Comparable Company Selection Criteria

Select peers that are similar on as many of these dimensions as possible:
- Business model (revenue type, margin profile)
- End market / vertical
- Size (market cap within 0.3x–3x of target where possible)
- Geography (primary)
- Growth profile (high-growth vs. mature)

Prefer listed companies with active CapIQ coverage and liquid trading. Avoid shell companies, SPACs, or companies under going M&A that may distort multiples.
