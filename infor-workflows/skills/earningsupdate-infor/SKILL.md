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
version: 1.9.13
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
| `TextBox 16` (L≈0.35, T≈1.45) | `[x]` / `[x]` | 7–9 bullet company description, filling the left column down to ~T=6.85 |
| `Text Placeholder 1` (footnote, line 2) | `Note: All figures in [x]$MM, ...` | Replace `[x]` with `US`, `C`, etc. |

**Do NOT touch `Rectangle 4` — the BBG placeholder at L≈5.12, T≈1.48.** The analyst will replace it manually with a Bloomberg company tearsheet screenshot and then paste in the cap table output from Step 8.

**Company description bullets** — see the Village Farms slide 2 left panel for tone. Target **7–9 bullets** so the description fills the left column down to roughly T=6.85 (just above the footer at T=7.03). Too-few bullets leaves obvious white space. Structure:
- Bullet 1 (main, 10.5 pt): One-sentence "what the company is" — founding year, exchange/ticker, one-line business description
- Bullet 2 (main, 10.5 pt): Scale/footprint statement (facilities, geographies, headcount, or revenue)
- Bullet 3 (main, 10.5 pt): Financial snapshot — most recent revenue, EBITDA, margin, or balance-sheet anchor (loan book, AUM, production)
- Bullets 4–6+ (sub, 10 pt): One sub-bullet per reportable segment or major business line, naming the segment and its core activity/KPIs
- Second-to-last bullet (main, 10.5 pt): Key historical transactions (acquisitions, divestitures, JVs) in chronological order
- Last bullet (main, 10.5 pt): Governance / leadership / credit-rating note, or one notable recent milestone

Do not pad with fluff — if the filing genuinely only supports 6 bullets of real content, stop at 6. But for most public companies, 7–9 bullets of real description is the right density. Do not let total height exceed T≈6.85 — if it does, tighten wording before shrinking font.

Source content from the MD&A's "Overview" / "Our Business" / "Operating Segments" sections, the 10-K Item 1 "Business" section, and the company website if needed via WebSearch. Keep each bullet tight — one idea per line.

**Bullet formatting — mandatory.** The template ships `TextBox 16` with two seed paragraphs: paragraph 0 is a **main bullet** (Palatino Linotype 10.5 pt, square bullet character, `marL="180975" indent="-180975"`) and paragraph 1 is a **sub-bullet** (Palatino Linotype 10 pt, dash bullet character, `marL="360000" indent="-180000"`). When you add a new paragraph beyond those two, python-pptx creates it with an empty `<a:pPr/>` and no run properties — the result inherits PowerPoint's theme default, which is **Calibri 18 pt with no bullet character**. This is the bug that showed up on goeasy bullets 3+.

Fix: for every bullet you write, **copy the paragraph-level `pPr` element** from the template paragraph that matches the desired level (0 = main, 1 = sub), and **explicitly set `run.font.name = "Palatino Linotype"` and `run.font.size = Pt(10.5)` or `Pt(10)`** on every run. Do not trust inherited formatting. See the `set_bullets` helper in the reference implementation.

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

**Delta-box font size — fixed 10 pt.** All four delta rectangles (`Rectangle 1041`, `1042`, `1061`, `1064`) use Palatino Linotype at a fixed **10 pt** — **minimum and only** size. Every delta box on the slide must match. Do not step down to 9 pt. If a delta string doesn't fit in the ≈1.0–1.1 in wide box at 10 pt, **shorten the number format** before anything else:
- `+C$0.9B` instead of `+C$911MM`
- `+$1.2B` instead of `+$1,234MM`
- `+14.6%` instead of `+1,460 bps` (bps is banned anyway — see next rule)

If the formatted number is already compact and still doesn't fit, drop the trailing `MM`/`B` unit (readers infer from the prior/current boxes). Never decrease font size below 10 pt.

**Delta-box color — green up, red down.** Color the delta value text based purely on the **direction of movement**, not whether the change is "good" or "bad" for the company:
- Positive delta (current > prior) → **green** `#00B050`
- Negative delta (current < prior) → **red** `#C00000`
- Zero change → leave template default (black)

This applies even when the "good" direction is inverted — for charge-off rates, cost ratios, or expense metrics, a positive delta is still green because the metric went up. The color reflects arithmetic direction, not business interpretation. Set the color explicitly via `run.font.color.rgb = RGBColor.from_string("00B050")` / `"C00000"`.

**Percent deltas only — never BPS.** For margin / rate / yield metrics (gross margin, charge-off %, CET1 ratio, occupancy, etc.), the delta value is always in percentage points expressed as `%`, not basis points. Write `+14.6%`, not `+1,460 bps`. Compute delta as `current_pct − prior_pct` and format with one decimal and a `%` suffix. This applies across every delta box in all four rows.

**Currency prefix.** Use `$` for USD and EUR, `C$` for CAD — match the reporting currency. For percentages, no prefix. For counts (e.g., production volumes), use the appropriate unit (`boe/d`, `MMcf/d`, `MW`, etc.). The template uses bare `$` — replace it if the filing is in a non-USD currency.

#### 6c — Business Updates Bullets (top-left)

Target shape: `TextBox 1067` at L≈0.35, T≈1.44. Replace all `[x]` bullets with concise bullets covering the quarter's operational story.

**Must fit inside the box.** The Business Updates area runs from T≈1.44 to T≈4.13 (the Broker Estimates section header starts at T=4.18). The bullets must not overflow into that section. Target **4 bullets, max 5**, each under ~30 words. Keep paragraph spacing uniform.

**Bullet formatting — mandatory.** All bullets must use the INFOR square bullet character at **level 0 (main)**, **Palatino Linotype 10 pt**. The template's paragraph 0 has the correct `pPr` (bullet character, indent, spacing). When you add paragraphs beyond paragraph 0, python-pptx creates them with an empty `<a:pPr/>` and no `rPr` — the result is Calibri with **no bullet character**. This is the bug that left bullets 3+ on goeasy without bullets.

Fix: for every bullet, **copy paragraph 0's `pPr` element** onto the new paragraph, and **explicitly set `run.font.name = "Palatino Linotype"` and `run.font.size = Pt(10)`** on every run. Do not use sub-bullets (level 1) here — all four/five bullets are main points at level 0 with the same square bullet glyph. See `set_bullets` in the reference implementation.

After writing, re-open the deck with python-pptx and measure the bullet text length. If 5 bullets × ~30 words still visually overflows (a safe proxy is total rendered characters > ~800 for this shape at 10 pt), drop to 4 bullets or shorten wording — do not shrink font below 10 pt.

**Content style — narrative, not metric listings.** The Business Updates section on the LEFT should read like a pithy quarterly narrative, not a bulleted list of financial metrics. The RIGHT-side KPI tiles and Broker table already carry the numbers. The LEFT side is for:

1. **Key events / decisions of the quarter** — strategic actions, management changes, capital allocation choices, one-time charges, impairments, guidance revisions, segment wind-downs, major contracts won/lost, acquisitions or divestitures
2. **Operating commentary on segment performance** — "why" the numbers moved, not "what" the numbers are (the tiles show "what"). One bullet per material segment is typical.
3. **Forward outlook** — guidance for next quarter / full year, upcoming catalysts (product launches, facility ramps, regulatory decisions), capital plan

Aim for roughly **2 event bullets + 1–2 segment commentary bullets + 1 outlook bullet**. Light numerical anchoring is fine (one or two figures per bullet for context) but a bullet that is *primarily* a metric statement — e.g., *"Revenue of C$406.3MM was effectively flat vs. Q4 2024 (-0.2%)"* — belongs on the right side, not the left. Instead, write *"Revenue stayed flat as yield compression from the 35% rate cap and LendCare charge-offs offset growth in the easyfinancial direct channel."*

Sourcing priority:
1. Earnings call transcript (if attached) — highest quality, management's own framing
2. Earnings press release (WebSearch: `"<Company Name>" Q<x> 202<x> earnings press release`) — use the company's site or a wire that reproduces the company release verbatim
3. MD&A "Highlights" or "Overview" section

Each bullet should:
- Lead with the driver or event (not the metric)
- Explain cause and consequence, not just the fact
- Be written in full prose sentences — no sentence fragments or metric-first phrasing

Good example (Village Farms): *"International medical exports surged on strong demand across European markets, with Germany and the UK both scaling materially."*

Bad example (goeasy v3): *"Gross consumer loans receivable grew 19.8% YoY to C$5.51B, with Q4 originations of C$951.5MM (+16.9% YoY) demonstrating continued robust customer demand"* — reads as two metrics and a platitude; belongs on the right side.

Include one bullet covering forward outlook / management guidance for the coming year.

#### 6d — Broker Estimates vs Actuals Table (bottom-left)

Target shape: the PPTX table (shape type 19) on slide 3 — the one with header row `['Figures in x$MM', 'Reported', 'Bloomberg Estimate', 'Variance']`.

Update the header cell `Figures in x$MM` → `Figures in <currency code>$MM` (e.g., `Figures in US$MM`, `Figures in C$MM`).

**Font — mandatory.** Every cell in the table (header row and all metric rows) must be **Palatino Linotype at 9 pt**. After writing each cell, explicitly iterate every run and set `run.font.name = "Palatino Linotype"` and `run.font.size = Pt(9)`. Do not trust inherited formatting — PowerPoint's default run fallback is Calibri, which has been observed to slip in when cells are re-written.

**Always exactly 5 metric rows — never delete.** The table must always have 5 populated metric rows (6 rows total including header). **Never** write `N/A`. **Never** delete rows. If the Bloomberg EEO snip only shows consensus for 3 of the template's default metrics, **swap** the other two row labels for different metrics the snip *does* cover — pick substitutions so all 5 rows have real Reported / Estimate / Variance values.

The template's 5 default metric rows are Revenue, Gross Margin, Adj. EBITDA, Net Income, UPS. Change the label on any row where the EEO snip lacks consensus. Common substitute metrics by sector:

| Sector | Preferred 5 metrics (all typically on EEO) |
|--------|-------------------------------------------|
| Consumer / industrial | Revenue, Gross Margin %, Adj. EBITDA, Adj. EBITDA Margin %, Adj. EPS |
| Financials / lenders | Revenue, PPNR, Net Income, ROE %, EPS |
| Asset managers | Revenue, Adj. EBITDA, AUM, Management Fees, Adj. EPS |
| Energy | Revenue, Adj. EBITDA, Production, Netback, CFPS |
| REITs / yield vehicles | Revenue, NOI, FFO, AFFO / share, Occupancy % |
| SaaS | Revenue, ARR, Adj. EBITDA, FCF, Adj. EPS |

Before writing, read the EEO snip and inventory which metrics the snip actually shows consensus for. Build a list of 5 metrics all present on the snip — combine template defaults + sector substitutes. Only then begin writing.

If the EEO snip genuinely shows fewer than 5 metrics (rare — most EEOs cover 6-8), use the lowest-quality filler from the sector row above that the analyst can still manually source (e.g., street consensus from a research note) — but prefer to expand your read of the snip first. Never leave a cell empty or `N/A`.

Populate each row:

- **Reported** — from the 10-Q/10-K or the company's earnings press release
- **Bloomberg Estimate** — read directly from the EEO snip
- **Variance** — `Reported − Estimate`; format to match the metric (`+$1.2MM` for dollar metrics, `+0.8%` for margin/rate metrics, `+$0.03` for per-share)

Use parentheses for negative variances, e.g., `(0.60)`. Percentages render with one decimal (`38.7%`).

#### 6e — Management Quotes (bottom-right)

Two quote groups on slide 3: `Group 1070` and `Group 1086`. Each group contains three shapes — the swoosh freeform (leave alone), a quote TextBox, and an attribution TextBox.

| Group | Quote TextBox | Attribution TextBox |
|-------|---------------|---------------------|
| `Group 1070` | `TextBox 1072` | `TextBox 1073` |
| `Group 1086` | `TextBox 1088` | `TextBox 1089` |

Set the quote TextBox to a 1–3 sentence management quote, wrapped in curly quotes `"..."` (the template uses `"Quote"` with slanted double quotes). Set the attribution TextBox to `<Name> – <Role>` (en-dash, not hyphen) — e.g., `Michael DeGiglio – CEO`.

**Formatting preservation — just call `set_text(shape, [line])`.** The template ships the quote TextBoxes (`TextBox 1072`, `TextBox 1088`) with **Palatino Linotype 10.5 pt italic**, and the attribution TextBoxes (`TextBox 1073`, `TextBox 1089`) with **Palatino Linotype 10.5 pt bold**. The `set_text` helper preserves the template's run-level `rPr` (font, size, italic, bold, color) automatically — just mutate the text without passing `size_pt` / `color_hex`. Do not add an explicit `run.font.italic = True` or similar; trust the template.

**Quotes must address THE key item of the quarter — not general strategy.** The section header says "Management Guidance" — the analyst wants to see management's own words about whatever made this quarter noteworthy: the goodwill impairment, the credit-loss spike, the guidance cut, the reorg, the acquisition close, the margin inflection. Generic confidence language ("we're committed to long-term shareholder value", "we have a clear plan to execute with urgency") fails this test even if the CEO said it verbatim.

Before picking quotes, identify the **single most important event or result** driving this quarter's narrative. That is usually:
1. The largest negative surprise vs. BBG consensus (from Slide 3 Broker table), OR
2. The largest one-time charge or impairment (from MD&A / press release), OR
3. The biggest operational shift (segment wind-down, management change, guidance revision)

Then find management's words on **that specific item**. Example for goeasy Q4 2025 (LendCare goodwill impairment + charge-off spike):
- Good: *"We are taking decisive action on LendCare — accelerating the integration, right-sizing the credit book, and recognizing the C$160MM goodwill impairment today rather than extending the problem into 2026."*
- Bad (too generic): *"My top priority is to ensure we manage credit well and deliver the strong performance we expect of ourselves."*

If the transcript / press release doesn't contain a direct quote addressing the key item, it is acceptable to use a closely adjacent quote (e.g., one quote on the item + one on the response plan) — but do not fall back to generic mission-statement language.

Sourcing:
- If earnings call transcript attached → pick the two most insight-dense quotes that directly address the key item (CEO + CFO typically). Scan Q&A as well as prepared remarks — analyst questions often pull out the most pointed management responses.
- Otherwise → WebSearch for `"<Company Name>" Q<x> 202<x> earnings press release` and pull direct quotes from the company's press release. If the press release lacks a pointed quote, WebSearch for a post-earnings interview or sell-side note that quotes management.

Keep each quote under ~60 words.

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
from copy import deepcopy
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

PALATINO = "Palatino Linotype"
COLOR_UP   = "00B050"  # green — positive delta
COLOR_DOWN = "C00000"  # red   — negative delta

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

def _pPr_of(paragraph):
    """Return the paragraph-level <a:pPr> element, or None if absent."""
    for child in paragraph._p:
        if child.tag.endswith("}pPr"):
            return child
    return None

def _first_run_rPr(paragraph):
    """Return a deepcopy of the first run's <a:rPr> element, or None if the paragraph has no runs or no rPr."""
    for r in paragraph.runs:
        for child in r._r:
            if child.tag.endswith("}rPr"):
                return deepcopy(child)
        return None
    return None

def set_text(shape, lines, size_pt=None, color_hex=None):
    """Replace shape text preserving the template's run formatting.

    Strategy:
      - For each existing paragraph we're rewriting: mutate the first run's .text in place
        (keeps its rPr — font, size, bold, italic, color). Remove subsequent runs on that paragraph.
      - For new paragraphs beyond the existing count: add_paragraph, copy pPr from para 0,
        and copy the first run's rPr from para 0 so the new run inherits the full formatting.
      - size_pt / color_hex act as explicit OVERRIDES on top of the preserved formatting.
        Pass them only when the caller intentionally wants to override (e.g. delta boxes).
    """
    tf = shape.text_frame
    template_pPr = _pPr_of(tf.paragraphs[0])
    template_rPr = _first_run_rPr(tf.paragraphs[0])

    for i, line in enumerate(lines):
        if i < len(tf.paragraphs):
            p = tf.paragraphs[i]
            # Remove runs after the first — but keep the first to preserve its rPr
            for r in list(p.runs[1:]):
                r._r.getparent().remove(r._r)
            if p.runs:
                # MUTATE text in place — preserves font/size/bold/italic/color
                p.runs[0].text = line
                run = p.runs[0]
            else:
                run = p.add_run()
                run.text = line
                if template_rPr is not None:
                    # Graft a fresh copy of the template rPr onto the new run
                    existing = [c for c in run._r if c.tag.endswith("}rPr")]
                    for e in existing:
                        run._r.remove(e)
                    run._r.insert(0, deepcopy(template_rPr))
        else:
            p = tf.add_paragraph()
            # Replace any auto-inserted empty pPr with a copy of paragraph 0's pPr
            if template_pPr is not None:
                for child in list(p._p):
                    if child.tag.endswith("}pPr"):
                        p._p.remove(child)
                p._p.insert(0, deepcopy(template_pPr))
            run = p.add_run()
            run.text = line
            if template_rPr is not None:
                existing = [c for c in run._r if c.tag.endswith("}rPr")]
                for e in existing:
                    run._r.remove(e)
                run._r.insert(0, deepcopy(template_rPr))
        # Apply overrides if requested
        if size_pt is not None:
            run.font.name = PALATINO
            run.font.size = Pt(size_pt)
        if color_hex is not None:
            run.font.color.rgb = RGBColor.from_string(color_hex)

    while len(tf.paragraphs) > len(lines):
        p = tf.paragraphs[-1]
        p._p.getparent().remove(p._p)

def set_bullets(shape, items, default_sizes=(10.5, 10.0, 9.0)):
    """Write bullets with explicit levels.
    items: list of (text, level) tuples. level 0 = main, 1 = sub, 2 = detail.
    Copies the template's pPr AND first-run rPr for the matching level from the shape's seed paragraphs.
    Falls back to Palatino Linotype at default_sizes[level] if no template rPr is present."""
    tf = shape.text_frame
    # Harvest pPr + rPr templates per level from existing seed paragraphs
    level_pPr, level_rPr = {}, {}
    for p in tf.paragraphs:
        lvl = p.level
        if lvl not in level_pPr:
            pPr = _pPr_of(p)
            if pPr is not None:
                level_pPr[lvl] = deepcopy(pPr)
        if lvl not in level_rPr:
            rPr = _first_run_rPr(p)
            if rPr is not None:
                level_rPr[lvl] = rPr
    # Fallback: if only level 0 available, reuse it for missing levels
    base_pPr = level_pPr.get(0)
    base_rPr = level_rPr.get(0)

    # Remove all paragraphs after the first, and clear runs/pPr on the first
    while len(tf.paragraphs) > 1:
        last = tf.paragraphs[-1]
        last._p.getparent().remove(last._p)
    first = tf.paragraphs[0]
    for r in list(first.runs):
        r._r.getparent().remove(r._r)
    for child in list(first._p):
        if child.tag.endswith("}pPr"):
            first._p.remove(child)

    for i, (text, level) in enumerate(items):
        if i == 0:
            p = first
        else:
            p = tf.add_paragraph()
            for child in list(p._p):
                if child.tag.endswith("}pPr"):
                    p._p.remove(child)
        # Apply pPr for this level
        pPr = level_pPr.get(level) or base_pPr
        if pPr is not None:
            p._p.insert(0, deepcopy(pPr))
        run = p.add_run()
        run.text = text
        # Prefer template rPr (preserves bold, italic, color, font)
        rPr = level_rPr.get(level) or base_rPr
        if rPr is not None:
            existing = [c for c in run._r if c.tag.endswith("}rPr")]
            for e in existing:
                run._r.remove(e)
            run._r.insert(0, deepcopy(rPr))
        else:
            run.font.name = PALATINO
            run.font.size = Pt(default_sizes[level])

def set_cell_text(cell, text, size_pt=9):
    """Overwrite cell content as a single run, Palatino Linotype at size_pt."""
    tf = cell.text_frame
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

# Slide 2 description — pass each bullet with its level (0 = main 10.5 pt, 1 = sub 10 pt).
# Example shape: [("Founded in ...", 0), ("Operates two segments", 0),
#                 ("Segment A does X", 1), ("Segment B does Y", 1),
#                 ("Key transactions: ...", 0)]
set_bullets(find_shape(slide2, "TextBox 16"), description_bullets_with_levels)

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

# Slide 3 — Business updates. ALL bullets at level 0 (main) with square bullet, 10 pt.
# 4 bullets preferred, 5 max.
assert 1 <= len(business_updates) <= 5, "Business Updates must be 1-5 bullets"
set_bullets(
    find_shape(slide3, "TextBox 1067"),
    [(text, 0) for text in business_updates],
    default_sizes=(10.0, 10.0, 10.0),  # level 0 at 10 pt for this shape specifically
)

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
    # Delta box — FIXED 10 pt for every delta. No step-down.
    # Rate deltas must be %, never bps.
    # Color based purely on direction: positive = green, negative = red.
    delta_str = m["delta_str"]
    assert "bps" not in delta_str.lower(), "Rate deltas must be % not bps"
    sign = m["delta_sign"]  # +1 / -1 / 0
    color = COLOR_UP if sign > 0 else (COLOR_DOWN if sign < 0 else None)
    set_text(find_shape(slide3, delta), [delta_str], size_pt=10, color_hex=color)
    # NEVER rotate triangles. Do not set shape.rotation on tl or tr.

# Slide 3 — Broker table
# Build broker_rows = [(label, reported, estimate, variance)] with EXACTLY 5 rows.
# Every row must have real values — if the EEO snip lacks a template default metric,
# swap that row's label for a different metric the snip DOES cover.
assert len(broker_rows) == 5, "Broker table must have exactly 5 rows"
for r in broker_rows:
    for v in r[1:]:
        assert v and v.strip().lower() not in ("n/a", "na", "-"), f"Broker cell cannot be N/A: {r}"

for shape in slide3.shapes:
    if shape.shape_type == 19:  # TABLE
        tbl = shape.table
        # Header row
        set_cell_text(tbl.cell(0, 0), f"Figures in {currency_short}", size_pt=9)
        set_cell_text(tbl.cell(0, 1), "Reported", size_pt=9)
        set_cell_text(tbl.cell(0, 2), "Bloomberg Estimate", size_pt=9)
        set_cell_text(tbl.cell(0, 3), "Variance", size_pt=9)
        # Metric rows — always 5
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
| Delta font size | **Fixed 10 pt**, all four delta boxes. No step-down. If text doesn't fit, shorten the number format (`+C$0.9B` not `+C$911MM`) — never drop below 10 pt. |
| Delta color | Positive delta → green `#00B050`; negative delta → red `#C00000`. Direction-based, not "good/bad" — charge-off rate going up is green. |
| Rate / margin deltas | Always `%` (e.g., `+14.6%`), never `bps` (`+1,460 bps` is wrong) |
| `set_text` must preserve formatting | The helper mutates `paragraph.runs[0].text` in place (preserving the template's `rPr` — font, size, bold, italic, color). It only creates fresh runs for brand-new paragraphs beyond the template's seed count, and when it does, it grafts a copy of paragraph 0's `rPr` onto the new run. **Do not pass `size_pt` / `color_hex` unless you intentionally want to override.** Overriding on shapes like `Title 1`, `Rectangle 7`, `Rectangle 1111`, `Subtitle 2` (date), or the quote/attribution TextBoxes would wipe out the template's bold/italic/color formatting. |
| Bullet formatting (slide 2 + slide 3 business updates) | Use `set_bullets` which harvests each level's `pPr` AND `rPr` from the template's seed paragraphs. If the template has a seed paragraph for level 0 (Palatino 10.5 pt main bullet) and level 1 (Palatino 10 pt sub-bullet), new bullets at each level get both formatting layers. Empty `pPr` + missing `rPr` → PowerPoint falls back to Calibri 18 pt with no bullet character. |
| Slide 2 main vs. sub bullets | Main bullets (level 0) = 10.5 pt, sub-bullets (level 1) = 10 pt. Description bullets use both levels to group segment-level detail under summary bullets. |
| Business Updates overflow | Hard cap at 5 bullets (4 preferred), ≤30 words each, 10 pt Palatino, **all at level 0** (square bullet). Text must end above T≈4.13 to not collide with the Broker Estimates header at T=4.18. |
| Broker table font | Every cell forced to Palatino Linotype 9 pt via `run.font.name` + `run.font.size` — do not trust inherited formatting |
| Broker table — always 5 rows | **Never delete rows. Never write N/A.** If the EEO snip doesn't cover a template default metric, swap that row's label for a different metric the snip *does* cover. 5 real rows, no exceptions. |
| Management quote focus | Quotes must address THE key item of the quarter (the largest surprise, charge, or inflection) — not generic strategy language. If the transcript/press release lacks a pointed quote on the key item, expand the search (Q&A section, post-earnings interviews). |
| Business Updates tone | Narrative prose, not metric listings. Left side is events + segment commentary + outlook; right side carries the numbers. A bullet that is primarily a metric (`"Revenue grew 19.8% YoY to $5.51B"`) belongs in the KPI tiles, not here. |
| Slide 2 density | Target **7–9 bullets** in the description so the left column fills down to T≈6.85. Fewer bullets leaves obvious white space; more risks overflowing the footer at T=7.03. |
| Gold summary box overflow | ≤25 words / ≤150 chars. Keep high-level; move specific figures to the bullets |
| Negative numbers | Wrap in parentheses: `($8.7MM)`, not `-$8.7MM` — consistent with template's Village Farms example |
| Curly quotes | Use `"..."` (U+201C / U+201D), not straight `"..."` — preserves template typography |
| Attribution dash | Use en-dash `–` (U+2013), not hyphen `-` |
| Quarter label | `Q4 2025`, not `Q4'25` or `4Q25` — template uses full format |
| EEO variance sign | Reported − Estimate — a beat is `+`, a miss is `-` (or parentheses) |
| Slide 4 / 5 | NEVER modify — disclaimer and contact page are fixed |
| Cap table | Invoke captable-infor workflow as Step 8; save alongside but do not embed |
