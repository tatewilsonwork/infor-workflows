---
name: buyerslist-infor
description: >
  Use this skill when the user asks to build a buyer list, buyer universe, or potential acquirer list
  for a company in a sell-side M&A process. Activates on "buyer list", "buyer universe",
  "potential acquirers", "who would buy", "strategic buyers", "financial sponsors", or "sell-side process".
  Populates the INFOR Buyers List Template with strategic and financial buyers, tiered A/B/C.
version: 1.6.0
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
- **Portfolio Companies** — relevant portfolio companies in the sector (≤30 chars; comma-separated if multiple)
- **Rationale** — professional IB-style explanation of why this sponsor is a strong fit: name the specific portfolio company for bolt-on theses, or articulate the platform/growth thesis for new-platform theses (see **Rationale Writing Guidelines** below)
- **Tier** — A, B, or C (see Tiering Criteria below)

---

### Rationale Writing Guidelines

The Rationale column on both sheets now uses wrapped text with tall rows to accommodate professional, IB-style prose — not shorthand.

**Length:** 1–2 complete sentences, typically 150–350 characters. Long enough to articulate the thesis; short enough to scan quickly on a printed page.

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

- *Strategic (Adjacent Player):* "Acquisition would extend CI Financial's wealth management platform into the Quebec HNW segment, complementing its Ontario-centric advisor network and adding approximately C$4B in fee-bearing AUM with a high proportion of recurring revenue."
- *Strategic (Platform Builder):* "Target aligns with Power Corp's stated strategy to consolidate mid-market Canadian asset managers; the acquisition would accelerate scale economics and broaden product shelf into alternative fixed income."
- *PE Add-on:* "Natural bolt-on to Onex portfolio company WealthOne, where the target's advisor base and Quebec footprint would expand WealthOne's national distribution and accelerate its path to a C$50B AUM platform."
- *PE Platform:* "Birch Hill is actively deploying its recently closed C$1.4B Fund VI and has publicly targeted financial services platforms; the target offers a recurring-revenue, asset-light profile well-suited to a 5–7 year hold."

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
| G | Rationale | `str` — 1–2 professional sentences, ~150–350 chars (see Rationale Writing Guidelines) |
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
| G | Portfolio Companies | `str` — ≤30 chars |
| H | Rationale | `str` — 1–2 professional sentences, ~150–350 chars (see Rationale Writing Guidelines) |
| I | Tier | `str` — `"A"`, `"B"`, or `"C"` |

Track `n_financial` = the number of financial buyer rows written.

**Never write to rows 25–27 before row removal** — these are COUNTIF total rows.

---

### Step 7b — Remove Empty Rows and Rewrite Totals

After writing all buyers, physically delete the unused data rows so the Tier totals sit directly below the last populated buyer on each sheet. This keeps the output clean for print/PDF distribution.

Do this **before saving** and **for each buyer sheet independently**.

For each buyer sheet (do Strategic first, then Financial — the two sheets are independent so row deletions on one do not affect the other):

1. Let `n` = number of buyers written on that sheet (`n_strategic` or `n_financial`).
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

6. **Rewrite the Summary sheet cross-sheet references** to point at the new totals rows. Let `strategic_totals_start = 4 + n_strategic + 1` and `financial_totals_start = 4 + n_financial + 1`. On the `Summary` sheet:
   ```
   summary["C15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start}"
   summary["D15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start + 1}"
   summary["E15"] = f"=+'Strategic Buyers'!$H${strategic_totals_start + 2}"
   summary["C16"] = f"=+'Financial Buyers'!$I${financial_totals_start}"
   summary["D16"] = f"=+'Financial Buyers'!$I${financial_totals_start + 1}"
   summary["E16"] = f"=+'Financial Buyers'!$I${financial_totals_start + 2}"
   ```
   The `SUM` totals in column F (`F15`, `F16`, `C17:F17`) reference only the same-sheet cells C/D/E 15–17 and remain correct without changes.

7. Verify that all three sheets still open cleanly and that the tier totals reflect the buyers written (sanity-check: each tier count should be ≥ 0 and the sum across tiers on each sheet should equal `n`).

Save the file after all three sheets have been written and trimmed.

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

| Sheet | Write range | Formula rows (initial) | Notes |
|-------|-------------|------------------------|-------|
| Summary | C4:C11 | Rows 13–17 | C15:E16 cross-reference the two buyer sheets — rewrite after Step 7b |
| Strategic Buyers | B5:H24 (max 20 rows) | Rows 25–27 | Totals shift up after Step 7b empty-row deletion |
| Financial Buyers | B5:I24 (max 20 rows) | Rows 25–27 | Totals shift up after Step 7b empty-row deletion |

The buyer data rows have pre-set row height (~28.5pt) and `wrap_text=True` on the Rationale column so longer professional-language rationales render cleanly without manual formatting.

### Character Limits by Column

**Strategic Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars — use common/abbreviated name |
| C | HQ | ~12 chars — e.g., `"Toronto, CA"` |
| D | Vertical | ~12 chars — e.g., `"Wealth Mgmt"` |
| F | M&A activity | ≤30 chars |
| G | Rationale | 1–2 full sentences, ~150–350 chars (professional IB prose — see Rationale Writing Guidelines) |

**Financial Buyers:**
| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| F | Sector Focus | ~12 chars |
| G | Portfolio Companies | ≤30 chars |
| H | Rationale | 1–2 full sentences, ~150–350 chars (professional IB prose — see Rationale Writing Guidelines) |

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
