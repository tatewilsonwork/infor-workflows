---
name: earningsupdate-infor
description: >
  Use this skill when the user invokes /earningsupdate-infor or asks to build a quarterly earnings
  update deck for a public company. Populates the INFOR Earnings Update Template with a company
  overview, four KPI tiles (actual vs prior-year quarter), a Broker Estimates vs Actuals table
  sourced from a Bloomberg EEO snip, business-update bullets, management quotes, and a short
  performance summary. Activates on "earnings update", "earnings deck", "quarterly earnings",
  "earnings summary deck", or any request to build a branded update deck off a recent 10-Q/10-K
  and Bloomberg EEO snip.
version: 1.9.11
---

# INFOR Earnings Update — Workflow

This skill builds a branded 5-slide earnings update deck from a company's most recent quarter of financials, a Bloomberg EEO screenshot, and optionally an earnings call transcript. It also produces a companion capitalization table XLSX that the analyst manually inserts into the deck in place of the BBG placeholder.

Allowed tools: Read, Bash, Write, Glob, WebSearch, WebFetch

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Earnings template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Earnings Update Template.pptx" 2>/dev/null | head -1`
- Cap table template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Cap Table Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Collect Inputs

Required:
- Company name and CapIQ ticker (e.g., `NasdaqGS:VFF`)
- Reporting quarter (e.g., Q4 2025) and prior-year comparison quarter (Q4 2024)
- Most recent 10-Q / 10-K / annual report + MD&A
- Bloomberg EEO snip (image/screenshot showing consensus vs. actual for the quarter)

Optional but highly useful:
- Earnings call transcript
- Company earnings press release URL (if not web-searchable from company name + quarter)

If any required input is missing, ask in a single message:

> "To build the earnings update, I need:
> - **Company name + CapIQ ticker** (e.g., NasdaqGS:VFF)
> - **Reporting quarter** (e.g., Q4 2025)
> - **10-Q / 10-K / MD&A** attached
> - **Bloomberg EEO snip** attached (image)
>
> Optional: earnings call transcript (attach) for extra detail."

Wait for all required inputs before proceeding.

---

### Step 2 — Locate and Copy the Template

The earnings template path is shown in the Context section. If blank, search for it:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Earnings Update Template.pptx" 2>/dev/null | head -1
```

Sanitize the company name (remove special chars, replace spaces with hyphens) and copy:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Earnings Update Template.pptx" 2>/dev/null | head -1)
OUTPUT="./Earnings Update - $SANITIZED_COMPANY.pptx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
ls -lh "$OUTPUT"
```

If the copy fails or the file is 0 bytes, STOP and tell the user:
> "I could not copy the INFOR Earnings Update Template. Please confirm the file `INFOR Earnings Update Template.xlsx` exists in the `templates/` folder at the root of the `infor-workflows` plugin repository."

---

### Step 3 — Determine Reporting Currency

Read the 10-Q/10-K to identify the reporting currency. Village Farms reports in US$ despite being Canadian-listed — do NOT infer currency from exchange. Read the cover page or the "Basis of Presentation" footnote in the financial statements.

Output the currency code as one of `US$MM`, `C$MM`, `€MM`, `£MM`, `A$MM`, etc. Use this value everywhere the template says `[x]$MM` or `x$MM`.

---

### Step 4 — Populate Slide 1 (Cover)

Open the deck with python-pptx and update ONLY the date placeholder in the bottom-right. Leave the title, subtitle, logo, and all other cover elements alone.

Target shape: on slide 1 (index 0), the `Subtitle 2` PLACEHOLDER at L≈5.55in, T≈6.9in contains `[Current Month] 2026`.

Replace with `[Month YYYY]` using **today's month and year** — always the current month, never the earnings-release month. E.g., if today is 2026-04-23, use `April 2026`.

---

### Step 5 — Populate Slide 2 (Company Overview)

Slide 2 is indexed 1. Update these shapes by name:

| Shape name | Current value | Update to |
|------------|---------------|-----------|
| `Title 1` (PLACEHOLDER) | `[Client Name] Overview` | `<Company Name> Overview` |
| `TextBox 16` (L≈0.35, T≈1.45) | `[x]` / `[x]` | 6–8 bullet company description |
| `Text Placeholder 1` (footnote, line 2) | `Note: All figures in [x]$MM, ...` | Replace `[x]` with `US`, `C`, etc. |

**Do NOT touch `Rectangle 4` — the BBG placeholder at L≈5.12, T≈1.48.** The analyst will replace it manually with a Bloomberg company tearsheet screenshot and then paste in the cap table output from Step 8.

**Company description bullets** — see the Village Farms slide 2 left panel for tone. Structure:
- Bullet 1: One-sentence "what the company is" — founding year, exchange/ticker, one-line business description
- Bullet 2: Scale/footprint statement (facilities, geographies, headcount, or revenue)
- Bullets 3+: One bullet per reportable segment, naming the segment and its core activity/KPIs
- Last bullet: Key historical transactions (acquisitions, divestitures, JVs) in chronological order

Source content from the MD&A's "Overview" / "Our Business" / "Operating Segments" sections, the 10-K Item 1 "Business" section, and the company website if needed via WebSearch. Keep each bullet tight — one idea per line.

Use the **Palatino Linotype** font already set in the template. Do not restyle text.

---

### Step 6 — Populate Slide 3 (Earnings Summary)

Slide 3 is indexed 2. This is the densest slide. Each sub-region below maps to specific shapes by name.

#### 6a — Title and Section Headers

| Shape | Update |
|-------|--------|
| `Title 1` (PLACEHOLDER) | `<Company Name> Q<x> 202<x> Earnings Summary` (current quarter) |
| `Rectangle 7` (top-right section header) | `Q<x> 202<prior> vs. Q<x> 202<current> Financial Highlights` (e.g., `Q4 2024 vs. Q4 2025 Financial Highlights`) |
| `Text Placeholder 1` (footnote, line 2) | Replace `[x]` with reporting currency code |

Leave section header shapes `Rectangle 5` ("Business Updates"), `Rectangle 10` ("Broker Estimates vs Actuals"), and `Rectangle 11` ("Management Guidance") unchanged.

#### 6b — KPI Tiles (top-right quadrant)

The template ships with four KPI rows, defaulted to Revenue / Net Income / Operating Cash Flow / Gross Margin. **Pick the four metrics that best reflect this company's story** — not necessarily the defaults. Examples:
- Asset managers: AUM, Management Fees, Adj. EBITDA, Operating Margin
- Energy: Production (boe/d), Netback, FFO, Net Debt
- Banks: Net Interest Income, PCL, ROE, CET1 Ratio
- REITs: FFO/share, SSNOI Growth, Occupancy, Debt/EBITDA
- SaaS: ARR, Net Revenue Retention, Adj. EBITDA, FCF Margin

Each of the four rows has six shapes. Map by vertical row:

| Row | Prior box | Current box | Delta $ box | Delta % box / 2nd delta | Left triangle | Right triangle |
|-----|-----------|-------------|-------------|-------------------------|---------------|----------------|
| 1 | `Rectangle 1032` | `Rectangle 1034` | `Rectangle 1041` | — | `Isosceles Triangle 1039` | `Isosceles Triangle 1040` |
| 2 | `Rectangle 1043` | `Rectangle 1037` | `Rectangle 1042` | — | `Isosceles Triangle 1045` | `Isosceles Triangle 1046` |
| 3 | `Rectangle 1035` | `Rectangle 1036` | `Rectangle 1061` | — | `Isosceles Triangle 1062` | `Isosceles Triangle 1063` |
| 4 | `Rectangle 1057` | `Rectangle 1058` | `Rectangle 1064` | — | `Isosceles Triangle 1065` | `Isosceles Triangle 1066` |

For each row, set:
- Prior box line 1: prior-period value (e.g., `$45.4MM`). Wrap negatives in parentheses: `($8.7MM)`.
- Prior box line 2: `Q<x> 202<prior> <Metric Name>` (e.g., `Q4 2024 Revenue`).
- Current box line 1: current-period value.
- Current box line 2: `Q<x> 202<current> <Metric Name>`.
- Delta box line 1: signed delta with `+` or `-` sign (e.g., `+$4.2MM`, `-$0.3MM`, `+22.6%` for margin deltas).

**Triangle orientation — NEVER rotate.** The gold triangles ship in the template's intended orientation. Do **not** set `shape.rotation` on any of the `Isosceles Triangle 10xx` shapes, ever — regardless of whether the metric moved up, down, or is a "good vs. bad" direction-flipped metric like charge-offs or expenses. Negative deltas are signalled by the `-` sign / parentheses on the delta value itself; the triangles are decorative.

**Delta-box font sizing.** The delta rectangles (`Rectangle 1041`, `1042`, `1061`, `1064`) are narrow (≈1.0–1.1 inches wide) and sit between two arrows. The delta text must fit on a single line between the triangles. Start at **10 pt** (the template default) and, if the delta string wraps to a 2nd line or visibly clips, step down in 0.5 pt increments to a **minimum of 9 pt**. Never go below 9 pt — if the value still doesn't fit at 9 pt, shorten the number's formatting instead (e.g., `+C$0.9B` instead of `+C$911MM`).

**Percent deltas only — never BPS.** For margin / rate / yield metrics (gross margin, charge-off %, CET1 ratio, occupancy, etc.), the delta value is always in percentage points expressed as `%`, not basis points. Write `+14.6%`, not `+1,460 bps`. Compute delta as `current_pct − prior_pct` and format with one decimal and a `%` suffix. This applies across every delta box in all four rows.

**Currency prefix.** Use `$` for USD and EUR, `C$` for CAD — match the reporting currency. For percentages, no prefix. For counts (e.g., production volumes), use the appropriate unit (`boe/d`, `MMcf/d`, `MW`, etc.). The template uses bare `$` — replace it if the filing is in a non-USD currency.

#### 6c — Business Updates Bullets (top-left)

Target shape: `TextBox 1067` at L≈0.35, T≈1.44. Replace all `[x]` bullets with concise bullets covering the quarter's operational story.

**Must fit inside the box.** The Business Updates area runs from T≈1.44 to T≈4.13 (the Broker Estimates section header starts at T=4.18). The bullets must not overflow into that section. Target **4 bullets, max 5**, each under ~30 words. Set font to **Palatino Linotype 10 pt** for every bullet (including the first — do not let the template's first paragraph drift to 10.5/11 pt). Keep paragraph spacing uniform.

After writing, re-open the deck with python-pptx and measure the bullet text length. If 5 bullets × ~30 words still visually overflows (a safe proxy is total rendered characters > ~800 for this shape at 10 pt), drop to 4 bullets or shorten wording — do not shrink font below 10 pt. Explicitly set each paragraph's font size via `run.font.size = Pt(10)` to avoid the template inheriting 10.5 pt from the first paragraph.

Sourcing priority:
1. Earnings call transcript (if attached) — highest quality, management's own framing
2. Earnings press release (WebSearch: `"<Company Name>" Q<x> 202<x> earnings press release`) — use the company's site or a wire that reproduces the company release verbatim
3. MD&A "Highlights" or "Overview" section

Each bullet should:
- Lead with the segment or driver
- Include a concrete number (%, $, volume, rate) whenever possible
- Explain cause, not just the fact — e.g., *"International medical exports surged (+384% YoY) driven by strong demand across European markets"*

Include one bullet acknowledging headwinds or temporary issues (strikes, FX, weather, regulatory) if present in the quarter — see Village Farms bullet 7 for pattern.

#### 6d — Broker Estimates vs Actuals Table (bottom-left)

Target shape: the PPTX table (shape type 19) on slide 3 — the one with header row `['Figures in x$MM', 'Reported', 'Bloomberg Estimate', 'Variance']`.

Update the header cell `Figures in x$MM` → `Figures in <currency code>$MM` (e.g., `Figures in US$MM`, `Figures in C$MM`).

**Font — mandatory.** Every cell in the table (header row and all metric rows) must be **Palatino Linotype at 9 pt**. After writing each cell, explicitly iterate every run and set `run.font.name = "Palatino Linotype"` and `run.font.size = Pt(9)`. Do not trust inherited formatting — PowerPoint's default run fallback is Calibri, which has been observed to slip in when cells are re-written.

**Only include metrics the EEO snip actually covers.** Never write `N/A` or leave a Bloomberg Estimate / Variance cell blank. If the Bloomberg EEO snip only shows consensus for 3 metrics, the table has 3 metric rows — delete the unused rows from the table rather than filling them with `N/A`. If the company reports a metric the snip doesn't cover but the analyst needs it shown, swap the row's label for a different metric the snip *does* cover.

The template ships with 5 metric rows (Revenue, Gross Margin, Adj. EBITDA, Net Income, UPS). Treat those as defaults — keep the ones the EEO snip covers, replace / delete the rest. Common substitutions:

| Sector | Common EEO metrics |
|--------|--------------------|
| Consumer / industrial | Revenue, Gross Margin, Adj. EBITDA, Adj. EPS |
| Financials / lenders | Revenue, PPNR, Net Income, EPS |
| Asset managers | Revenue, Adj. EBITDA, AUM, Adj. EPS |
| Energy | Revenue, Adj. EBITDA, Production, CFPS |
| REITs / yield vehicles | Revenue, NOI, FFO, AFFO / share |

Populate the kept rows:

- **Reported** — from the 10-Q/10-K or the company's earnings press release
- **Bloomberg Estimate** — read directly from the EEO snip
- **Variance** — `Reported − Estimate`; format to match the metric (`+$1.2MM` for dollar metrics, `+0.8%` for margin/rate metrics, `+$0.03` for per-share)

Use parentheses for negative variances, e.g., `(0.60)`. Percentages render with one decimal (`38.7%`).

**Deleting rows.** In python-pptx, remove a table row by manipulating the underlying XML:
```python
def delete_table_row(tbl, row_idx):
    tr = tbl.rows[row_idx]._tr
    tr.getparent().remove(tr)
```
Delete from the bottom up so indices don't shift.

#### 6e — Management Quotes (bottom-right)

Two quote groups on slide 3: `Group 1070` and `Group 1086`. Each group contains three shapes — the swoosh freeform (leave alone), a quote TextBox, and an attribution TextBox.

| Group | Quote TextBox | Attribution TextBox |
|-------|---------------|---------------------|
| `Group 1070` | `TextBox 1072` | `TextBox 1073` |
| `Group 1086` | `TextBox 1088` | `TextBox 1089` |

Set the quote TextBox to a 1–3 sentence management quote, wrapped in curly quotes `"..."` (the template uses `"Quote"` with slanted double quotes). Set the attribution TextBox to `<Name> – <Role>` (en-dash, not hyphen) — e.g., `Michael DeGiglio – CEO`.

Sourcing:
- If earnings call transcript attached → pick the single most insight-dense quote per executive (CEO + CFO typically)
- Otherwise → WebSearch for `"<Company Name>" Q<x> 202<x> earnings press release` and pull direct quotes from the company's press release

Prefer quotes that are forward-looking (guidance, expansion, capital allocation) over backwards-looking ("we had a great quarter"). Keep each quote under ~60 words.

#### 6f — Performance Summary Box (bottom-left, below the table)

Target shape: `Rectangle 1111` at L≈0.35, T≈6.19 — the gold/gilded summary box. Dimensions: **4.53 in wide × 0.63 in tall**.

**Must fit inside the box.** At 11 pt Palatino Linotype the box holds roughly **2 lines ≈ 28 words / 170 characters** before overflowing. Write **one sentence ≤ 25 words / 150 characters** summarizing the quarter's overall performance relative to expectations. The sentence should:
- Mention whether the company beat, missed, or met Bloomberg consensus (pull from 6d)
- Include one qualifier highlighting the underlying story (growth, margin, mix, one-time items)
- Be readable as a standalone callout

Good example (Village Farms, 20 words): *"Village Farms reported metrics that were below Bloomberg estimates, but results still demonstrated strong growth and margin profile"*

Bad example (goeasy, 26 words, overflowed): *"Q4 2025 results were dominated by a C$159.6MM LendCare goodwill impairment and incremental C$177.9MM of charge-offs"* — too many specific figures for the box; move concrete numbers to the bullets and keep the summary high-level.

If your draft exceeds 25 words, rewrite more tightly — do not shrink the font below 11 pt. Verify with `len(sentence.split()) <= 25 and len(sentence) <= 150` before writing.

---

### Step 7 — Leave Slides 4 and 5 Untouched

Slide 4 (Disclaimer) and Slide 5 (Contact — Neil Selfe + three placeholder tables) must remain exactly as shipped in the template. Do not touch them.

---

### Step 8 — Generate Companion Cap Table

Once the deck is populated, invoke the **captable-infor** skill's workflow (Steps 2–8 of that skill) using the same 10-Q/10-K/MD&A attachments and the CapIQ ticker provided in Step 1. The cap table will be saved alongside the deck as:

```
./<SANITIZED_TICKER> - Capitalization Table.xlsx
```

The analyst will open this file, refresh CapIQ, screenshot a cropped cap table region, and paste it over `Rectangle 4` (the BBG placeholder) on slide 2 of the deck. Do NOT try to embed the xlsx into the deck programmatically — manual insertion is intentional because the analyst refreshes CapIQ market data before pasting.

---

### Step 9 — Save and Verify

Save the deck. Reopen it with python-pptx in read mode and verify:
- Slide 1: date placeholder no longer contains `[Current Month]`
- Slide 2: title no longer contains `[Client Name]`, description TextBox has no `[x]` placeholders, footnote has no `[x]` in currency string
- Slide 3: title has real quarter, top-right section header has real quarters, all four KPI rows populated, broker table has no blank cells, both management quote groups updated, summary box updated
- BBG placeholder `Rectangle 4` on slide 2 still reads `[BBG Placeholder]` (yes, on purpose — analyst fills manually)

If any placeholder `[x]` or `[Client Name]` or `Qx 202x` token remains anywhere on slides 1–3, fix it and re-save.

---

### Step 10 — Report to User

Output a brief summary:

1. **Deck file:** absolute path to saved `.pptx`
2. **Cap table file:** absolute path to saved `.xlsx`
3. **Reporting currency used:** e.g., `US$MM`
4. **KPIs selected for slide 3:** list the four metrics and why (one phrase each)
5. **Sources used for bullets / quotes:** which file or URL each major section came from
6. **Manual steps remaining:**
   - Refresh CapIQ in the cap table file and paste a screenshot over `Rectangle 4` on slide 2
   - Optionally replace `Rectangle 4` with a Bloomberg tearsheet screenshot if the analyst prefers that layout
   - Review the Performance Summary box wording before sending

---

## Reference Implementation (python-pptx)

The template uses distinctive shape names (e.g., `Rectangle 1032`, `Group 1070`, `TextBox 1067`) that are stable across the template's lifetime. Target shapes by name, not by index, because shape order can vary.

```python
from pptx import Presentation
from pptx.util import Pt

PALATINO = "Palatino Linotype"

def find_shape(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
    raise KeyError(f"Shape {name!r} not found on slide")

def find_shape_in_group(group, name):
    for s in group.shapes:
        if s.name == name:
            return s
    raise KeyError(f"Shape {name!r} not found in group {group.name!r}")

def set_text(shape, lines, size_pt=None):
    """Replace shape text with the given list of lines, preserving the first run's formatting.
    If size_pt is provided, force every run to that size + Palatino Linotype."""
    tf = shape.text_frame
    for i, line in enumerate(lines):
        if i < len(tf.paragraphs):
            p = tf.paragraphs[i]
            for r in list(p.runs[1:]):
                r._r.getparent().remove(r._r)
            if p.runs:
                p.runs[0].text = line
            else:
                p.add_run().text = line
        else:
            p = tf.add_paragraph()
            p.text = line
    while len(tf.paragraphs) > len(lines):
        p = tf.paragraphs[-1]
        p._p.getparent().remove(p._p)
    if size_pt is not None:
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.name = PALATINO
                r.font.size = Pt(size_pt)

def delete_table_row(tbl, row_idx):
    tr = tbl.rows[row_idx]._tr
    tr.getparent().remove(tr)

def set_cell_text(cell, text, size_pt=9):
    """Overwrite cell content as a single run, Palatino Linotype at size_pt."""
    tf = cell.text_frame
    # Remove all paragraphs except the first
    while len(tf.paragraphs) > 1:
        last = tf.paragraphs[-1]
        last._p.getparent().remove(last._p)
    p = tf.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    run = p.add_run()
    run.text = text
    run.font.name = PALATINO
    run.font.size = Pt(size_pt)

prs = Presentation(output_path)

# Slide 1 — cover date
slide1 = prs.slides[0]
# The date placeholder is the second "Subtitle 2" — pick by text content match
for s in slide1.shapes:
    if s.name == "Subtitle 2" and s.has_text_frame and "[Current Month]" in s.text_frame.text:
        set_text(s, [f"{month_name} {year}"])

# Slide 2
slide2 = prs.slides[1]
set_text(find_shape(slide2, "Title 1"), [f"{company_name} Overview"])
set_text(find_shape(slide2, "TextBox 16"), description_bullets)
footnote = find_shape(slide2, "Text Placeholder 1")
set_text(footnote, ["Source: Company filings, S&P CapIQ, equity research ",
                    f"Note: All figures in {currency}, except where indicated otherwise"])

# Slide 3 — title, headers, footnote
slide3 = prs.slides[2]
set_text(find_shape(slide3, "Title 1"), [f"{company_name} Q{q} {year_c} Earnings Summary"])
set_text(find_shape(slide3, "Rectangle 7"),
         [f"Q{q} {year_p} vs. Q{q} {year_c} Financial Highlights"])
footnote3 = find_shape(slide3, "Text Placeholder 1")
set_text(footnote3, ["Source: Company filings, S&P CapIQ, equity research ",
                     f"Note: All figures in {currency}, except where indicated otherwise"])

# Slide 3 — Business updates. Force 10 pt on every bullet. 4 bullets preferred, 5 max.
assert 1 <= len(business_updates) <= 5, "Business Updates must be 1-5 bullets"
set_text(find_shape(slide3, "TextBox 1067"), business_updates, size_pt=10)

# Slide 3 — KPI tiles (rows list each hold (prior_box, current_box, delta_box, tri_l, tri_r, metric))
kpi_rows = [
    ("Rectangle 1032", "Rectangle 1034", "Rectangle 1041", "Isosceles Triangle 1039", "Isosceles Triangle 1040", kpi[0]),
    ("Rectangle 1043", "Rectangle 1037", "Rectangle 1042", "Isosceles Triangle 1045", "Isosceles Triangle 1046", kpi[1]),
    ("Rectangle 1035", "Rectangle 1036", "Rectangle 1061", "Isosceles Triangle 1062", "Isosceles Triangle 1063", kpi[2]),
    ("Rectangle 1057", "Rectangle 1058", "Rectangle 1064", "Isosceles Triangle 1065", "Isosceles Triangle 1066", kpi[3]),
]
for prior, current, delta, tl, tr, m in kpi_rows:
    set_text(find_shape(slide3, prior), [m["prior_value"], f"Q{q} {year_p} {m['name']}"])
    set_text(find_shape(slide3, current), [m["current_value"], f"Q{q} {year_c} {m['name']}"])
    # Delta box — 10 pt default, step down to 9 pt if the string is long.
    # Never go below 9 pt; never use bps for rate metrics (enforce at delta-string construction time).
    delta_str = m["delta_str"]
    assert "bps" not in delta_str.lower(), "Rate deltas must be % not bps"
    delta_size = 10 if len(delta_str) <= 9 else 9
    set_text(find_shape(slide3, delta), [delta_str], size_pt=delta_size)
    # NEVER rotate triangles. Do not set shape.rotation on tl or tr.

# Slide 3 — Broker table
# Build broker_rows = [(label, reported, estimate, variance)] for ONLY the metrics
# covered by the BBG EEO snip. No N/A. The template ships with 5 metric rows;
# delete any extra rows before writing.
for shape in slide3.shapes:
    if shape.shape_type == 19:  # TABLE
        tbl = shape.table
        template_metric_rows = 5  # rows 1..5 under the header
        # Delete extra rows from the bottom up
        for row_idx in range(template_metric_rows, len(broker_rows), -1):
            delete_table_row(tbl, row_idx)
        # Header currency
        set_cell_text(tbl.cell(0, 0), f"Figures in {currency_short}", size_pt=9)
        set_cell_text(tbl.cell(0, 1), "Reported", size_pt=9)
        set_cell_text(tbl.cell(0, 2), "Bloomberg Estimate", size_pt=9)
        set_cell_text(tbl.cell(0, 3), "Variance", size_pt=9)
        # Metric rows
        for i, (label, reported, estimate, variance) in enumerate(broker_rows, start=1):
            set_cell_text(tbl.cell(i, 0), label, size_pt=9)
            set_cell_text(tbl.cell(i, 1), reported, size_pt=9)
            set_cell_text(tbl.cell(i, 2), estimate, size_pt=9)
            set_cell_text(tbl.cell(i, 3), variance, size_pt=9)
        break

# Slide 3 — Quotes
g1070 = find_shape(slide3, "Group 1070")
set_text(find_shape_in_group(g1070, "TextBox 1072"), [f"\u201C{quote1_text}\u201D"])
set_text(find_shape_in_group(g1070, "TextBox 1073"), [f"{quote1_name} \u2013 {quote1_role}"])
g1086 = find_shape(slide3, "Group 1086")
set_text(find_shape_in_group(g1086, "TextBox 1088"), [f"\u201C{quote2_text}\u201D"])
set_text(find_shape_in_group(g1086, "TextBox 1089"), [f"{quote2_name} \u2013 {quote2_role}"])

# Slide 3 — Performance summary box (must fit: <= 25 words / <= 150 chars)
assert len(performance_summary_sentence.split()) <= 25, "Summary too long — rewrite"
assert len(performance_summary_sentence) <= 150, "Summary too long — rewrite"
set_text(find_shape(slide3, "Rectangle 1111"), [performance_summary_sentence])

prs.save(output_path)
```

Use `"\u201C"` / `"\u201D"` for curly quotes and `"\u2013"` for en-dash — the template uses these characters, and reverting to plain `"` or `-` would be a formatting regression.

---

## Common Pitfalls

| Issue | Guidance |
|-------|----------|
| BBG placeholder on slide 2 | Leave `Rectangle 4` alone — analyst pastes a screenshot manually |
| Currency | Read from filing "Basis of Presentation" — don't infer from exchange (VFF is NASDAQ but reports US$; BMO is NYSE-listed but reports C$) |
| KPI metric choice | Pick 4 metrics that reflect the *company's* story, not the template defaults |
| Triangle rotation | **NEVER** rotate triangles. Leave every `Isosceles Triangle 10xx` at its template rotation. Delta sign goes on the value, not the arrow. |
| Delta font size | 10 pt default in the narrow delta rectangles; step down to 9 pt minimum if the string wraps; never below 9 pt — shorten the number format instead |
| Rate / margin deltas | Always `%` (e.g., `+14.6%`), never `bps` (`+1,460 bps` is wrong) |
| Business Updates overflow | Hard cap at 5 bullets (4 preferred), ≤30 words each, 10 pt Palatino — text must end above T≈4.13 to not collide with the Broker Estimates header at T=4.18 |
| Broker table font | Every cell forced to Palatino Linotype 9 pt via `run.font.name` + `run.font.size` — do not trust inherited formatting |
| Broker table — no N/A | Only include rows where the EEO snip provides an estimate. Delete unused rows from the template rather than writing `N/A` |
| Gold summary box overflow | ≤25 words / ≤150 chars. Keep high-level; move specific figures to the bullets |
| Negative numbers | Wrap in parentheses: `($8.7MM)`, not `-$8.7MM` — consistent with template's Village Farms example |
| Curly quotes | Use `"..."` (U+201C / U+201D), not straight `"..."` — preserves template typography |
| Attribution dash | Use en-dash `–` (U+2013), not hyphen `-` |
| Quarter label | `Q4 2025`, not `Q4'25` or `4Q25` — template uses full format |
| EEO variance sign | Reported − Estimate — a beat is `+`, a miss is `-` (or parentheses) |
| Slide 4 / 5 | NEVER modify — disclaimer and contact page are fixed |
| Cap table | Invoke captable-infor workflow as Step 8; save alongside but do not embed |
