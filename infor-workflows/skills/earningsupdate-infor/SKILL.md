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
version: 1.9.10
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

**Triangle orientation.** The template ships with triangles pointing upward. When a metric *declined* (delta negative), rotate both triangles 180° (`shape.rotation = 180`) so they point down. Use the metric's desirable direction — for cost / expense metrics where lower is better, still rotate by the sign of the change, not "good vs. bad."

**Currency prefix.** Use `$` for USD and EUR, `C$` for CAD — match the reporting currency. For percentages, no prefix. For counts (e.g., production volumes), use the appropriate unit (`boe/d`, `MMcf/d`, `MW`, etc.). The template uses bare `$` — replace it if the filing is in a non-USD currency.

#### 6c — Business Updates Bullets (top-left)

Target shape: `TextBox 1067` at L≈0.35, T≈1.44. Replace all `[x]` bullets with 5–7 concise bullets covering the quarter's operational story.

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

Read the Bloomberg EEO snip (image input) and populate the five metric rows:

| Row label | Populate |
|-----------|----------|
| Revenue | Reported (from 10-Q/10-K), Bloomberg Estimate (from EEO snip), Variance = Reported − Estimate |
| Gross Margin | Same pattern — percentages with one decimal (e.g., `38.7%`) |
| Adj. EBITDA | Same pattern |
| Net Income | Same pattern, wrap negatives in parentheses |
| UPS (x$) | Update header to `EPS (<currency>$)` if BBG shows EPS; otherwise leave `UPS` if the company reports "Units Per Share" or similar. Populate actual vs. estimate in native currency. |

Variance format: match the metric — `+$1.2MM` for dollar metrics, `+0.8%` for margins, `+$0.03` for EPS. Use parentheses for negative variances.

If the Bloomberg EEO snip only shows estimates (no actuals), pull actuals from the 10-Q/10-K press release tables. If a metric isn't covered by BBG consensus (e.g., UPS for a company that reports EPS), delete that row rather than invent a number.

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

Target shape: `Rectangle 1111` at L≈0.35, T≈6.19 — the gold/gilded summary box.

Write one complete sentence summarizing the quarter's overall performance relative to expectations. The sentence should:
- Mention whether the company beat, missed, or met Bloomberg consensus (pull from 6d)
- Include one qualifier highlighting the underlying story (growth, margin, mix, one-time items)
- Be readable as a standalone callout

Example from Village Farms: *"Village Farms reported metrics that were below Bloomberg estimates, but results still demonstrated strong growth and margin profile"*

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

def set_text(shape, lines):
    """Replace shape text with the given list of lines, preserving the first run's formatting."""
    tf = shape.text_frame
    # Keep paragraph 0 formatting; replace text of existing paragraphs, add/remove as needed
    for i, line in enumerate(lines):
        if i < len(tf.paragraphs):
            p = tf.paragraphs[i]
            # Clear existing runs except the first, set first run's text
            for r in list(p.runs[1:]):
                r._r.getparent().remove(r._r)
            if p.runs:
                p.runs[0].text = line
            else:
                p.add_run().text = line
        else:
            p = tf.add_paragraph()
            p.text = line
    # Remove leftover paragraphs if we wrote fewer lines than existed
    while len(tf.paragraphs) > len(lines):
        p = tf.paragraphs[-1]
        p._p.getparent().remove(p._p)

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
    set_text(find_shape(slide3, delta), [m["delta_str"]])
    if m["delta_sign"] < 0:
        find_shape(slide3, tl).rotation = 180
        find_shape(slide3, tr).rotation = 180

# Slide 3 — Broker table
for shape in slide3.shapes:
    if shape.shape_type == 19:  # TABLE
        tbl = shape.table
        tbl.cell(0, 0).text_frame.paragraphs[0].runs[0].text = f"Figures in {currency_short}"
        for i, row in enumerate(broker_rows, start=1):
            for j, val in enumerate(row[1:], start=1):
                tbl.cell(i, j).text_frame.paragraphs[0].runs[0].text = val
        break

# Slide 3 — Quotes
g1070 = find_shape(slide3, "Group 1070")
set_text(find_shape_in_group(g1070, "TextBox 1072"), [f"\u201C{quote1_text}\u201D"])
set_text(find_shape_in_group(g1070, "TextBox 1073"), [f"{quote1_name} \u2013 {quote1_role}"])
g1086 = find_shape(slide3, "Group 1086")
set_text(find_shape_in_group(g1086, "TextBox 1088"), [f"\u201C{quote2_text}\u201D"])
set_text(find_shape_in_group(g1086, "TextBox 1089"), [f"{quote2_name} \u2013 {quote2_role}"])

# Slide 3 — Performance summary box
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
| Triangle direction | Rotate 180° when delta is negative — triangles ship pointing up |
| Negative numbers | Wrap in parentheses: `($8.7MM)`, not `-$8.7MM` — consistent with template's Village Farms example |
| Curly quotes | Use `"..."` (U+201C / U+201D), not straight `"..."` — preserves template typography |
| Attribution dash | Use en-dash `–` (U+2013), not hyphen `-` |
| Quarter label | `Q4 2025`, not `Q4'25` or `4Q25` — template uses full format |
| EEO variance sign | Reported − Estimate — a beat is `+`, a miss is `-` (or parentheses) |
| Slide 4 / 5 | NEVER modify — disclaimer and contact page are fixed |
| Cap table | Invoke captable-infor workflow as Step 8; save alongside but do not embed |
