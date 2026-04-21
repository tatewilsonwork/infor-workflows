---
name: buyerslist-infor
description: >
  Use this skill when the user asks to build a buyer list, buyer universe, or potential acquirer list
  for a company in a sell-side M&A process. Activates on "buyer list", "buyer universe",
  "potential acquirers", "who would buy", "strategic buyers", "financial sponsors", or "sell-side process".
  Populates the INFOR Buyers List Template with strategic and financial buyers, tiered A/B/C.
version: 1.3.6
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
- **M&A activity** — brief note on relevant recent M&A (≤30 chars; e.g., "Active acquirer in sector")
- **Rationale** — why this buyer would acquire the target (≤50 chars; e.g., "Expands wealth mgmt into Quebec market")
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
- **Portfolio Companies** — relevant portfolio companies in the sector (≤30 chars; comma-separated if multiple)
- **Portfolio Overlap / Add-On Target** — specific portco that could acquire as a bolt-on, or overlap rationale (≤50 chars)
- **Tier** — A, B, or C (see Tiering Criteria below)

---

### Step 5 — Tier All Buyers

Assign every buyer a tier:

| Tier | Target Count | Criteria |
|------|-------------|---------|
| A | 5–10 | Highest strategic/financial fit, proven acquirers in the sector, clear and compelling rationale |
| B | 10–15 | Good fit but less obvious; less active M&A track record or smaller size |
| C | Remainder | Possible but lower probability; include to broaden the process if needed |

Total buyers across both sheets must not exceed **40** (20 strategic + 20 financial maximum per sheet).

**Quality over quantity** — a focused list of 30–40 well-researched buyers beats a list of 200 names.

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

**Do not write to rows 13–17** — these contain headers and COUNTIF formula links.

**Sheet 2 — `Strategic Buyers`:** Write one row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Vertical | `str` |
| E | Revenue (C$MM) | `float`/`int` or skip if unknown |
| F | M&A activity | `str` |
| G | Rationale | `str` — ≤50 chars |
| H | Tier | `str` — `"A"`, `"B"`, or `"C"` |

**Never write to rows 25–27** — these are COUNTIF total rows.

**Sheet 3 — `Financial Buyers`:** Write one row per buyer starting at row 5 (max row 24):

| Column | Field | Type |
|--------|-------|------|
| B | Buyer name | `str` |
| C | HQ | `str` |
| D | Fund Size (C$B) | `float`/`int` or skip if unknown |
| E | Avg. Deal Size (C$MM) | `float`/`int` or skip if unknown |
| F | Sector Focus | `str` |
| G | Portfolio Companies | `str` — ≤30 chars |
| H | Portfolio Overlap / Add-On Target | `str` — ≤50 chars |
| I | Tier | `str` — `"A"`, `"B"`, or `"C"` |

**Never write to rows 25–27** — these are COUNTIF total rows.

Save the file after writing all three sheets.

---

### Step 8 — Summary

Report to the user:

1. **Output file:** path to the saved file
2. **Strategic Buyers:** count by tier (e.g., "8 Tier A, 7 Tier B, 4 Tier C")
3. **Financial Buyers:** count by tier
4. **Notable Tier A buyers:** briefly highlight the strongest 2–3 names and why
5. **Reminder:** Review the list and add any relationship-specific buyers or exclusions manually before distributing

---

## Domain Reference

### Template Cell Map

| Sheet | Write range | Formula rows (do not touch) |
|-------|-------------|------------------------------|
| Summary | C4:C11 | Rows 13–17 |
| Strategic Buyers | B5:H24 (max 20 rows) | Rows 25–27 |
| Financial Buyers | B5:I24 (max 20 rows) | Rows 25–27 |

### Character Limits by Column

**Strategic Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars — use common/abbreviated name |
| C | HQ | ~12 chars — e.g., `"Toronto, CA"` |
| D | Vertical | ~12 chars — e.g., `"Wealth Mgmt"` |
| F | M&A activity | ≤30 chars |
| G | Rationale | ≤50 chars |

**Financial Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| F | Sector Focus | ~12 chars |
| G | Portfolio Companies | ≤30 chars |
| H | Portfolio Overlap / Add-On Target | ≤50 chars |

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
