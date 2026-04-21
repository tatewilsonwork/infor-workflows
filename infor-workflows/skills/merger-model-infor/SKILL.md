---
name: merger-model-infor
description: Build accretion/dilution analysis for M&A transactions. Models pro forma EPS impact, synergy sensitivities, and purchase price allocation. Use when evaluating a potential acquisition, preparing merger consequences analysis for a pitch, or advising on deal terms. Triggers on "merger model", "accretion dilution", "M&A model", "pro forma EPS", "merger consequences", or "deal impact analysis". Output uses INFOR Financial Group brand colors.
version: 1.4.0
---

---

## TEMPLATE REQUIREMENT

**This skill builds merger (accretion/dilution) models in Excel. Always check for an attached template file first.**

Before starting any merger model:
1. **If a template file is attached/provided**: Use that template's structure exactly — copy it and populate with the user's data
2. **If no template is attached**: Ask the user: *"Do you have a specific merger model template you'd like me to use? If not, I can build a standard structure with Assumptions, Purchase Price, Sources & Uses, Pro Forma Income Statement, Accretion/Dilution Summary, Sensitivity Tables, and Breakeven Synergies."*
3. **If building from scratch**: Follow the section order in the Workflow below and apply the INFOR formatting conventions in this skill.

**IMPORTANT**: When a template file is attached, you MUST use it as your template — do not build from scratch. Even if the template seems complex or has more features than needed, copy it and adapt it to the user's requirements.

---

## CRITICAL INSTRUCTIONS FOR CLAUDE - READ FIRST

### Core Principles
* **Every calculation must be an Excel formula** — NEVER compute values in Python and hardcode results into cells. The model must be dynamic and update when inputs change.
* **Use the template structure** — Follow the user's provided template or the standard structure in the Workflow below. Do not invent your own layout.
* **Use proper cell references** — All formulas should reference the appropriate cells. Never type numbers that should come from other cells.
* **Maintain sign convention consistency** — Follow whatever sign convention the template uses (some use negative for outflows, some use positive). Be consistent throughout.
* **Work section by section** — Complete one section fully before moving to the next, as later sections often depend on earlier ones.

### Formula Font Color Conventions (IB Standard)
* **Blue (0000FF)**: Hardcoded inputs — typed numbers that don't reference other cells
* **Black (000000)**: Formulas with calculations — any formula using operators or functions (`=B4*B5`, `=SUM()`, `=-MAX(0,B4)`)
* **Purple (800080)**: Links to cells on the **same tab** — direct references with no calculation (`=B9`, `=B45`)
* **Green (008000)**: Links to cells on **different tabs** — cross-sheet references (`=Assumptions!B5`, `='Pro Forma'!C10`)

### Cell Fill & Border Conventions (INFOR Palette)

Font colors above track formula type; fills and borders below carry the INFOR visual identity.

| Element | Fill | Text | Border / Weight | Notes |
|---------|------|------|------------------|-------|
| Title row (top of sheet / section title) | **Navy Blue (0E213F)** | White, bold | — | Used for sheet title banners and standalone table headers |
| Section header row | **Navy Blue (0E213F)** | White, bold | — | Section header boxes above a block of content |
| Table header under a section header | **Mid Blue (46566E)** | White, bold | — | When the table already sits under a Navy section header, use Mid Blue so two Navy rows don't stack |
| Subtotal row | **Light Grey (E5E3E3)** | Black, **bold** | **Black top border** (thin, ~0.75pt) | Use for subtotals (e.g., Pro Forma Net Income, Total Sources, Enterprise Value) |
| Alternate subtotal row | **Light Blue (ADB9CA)** | Black, bold | Black top border | Use only when Light Grey subtotals already appear directly above/below and you need visual separation |
| Totals row (grand total) | **Dark Grey (767171)** | White, bold | Black top border; single-line bottom accounting underline | Use for the final total of a section (e.g., Pro Forma EPS, Accretion/(Dilution) %, Total Uses) |
| Alternating row shading (body) | **Light Grey (E5E3E3)** on every other row | Black | — | Optional — matches INFOR deck-table styling |
| Gridlines (tables) | — | — | White, 0.75pt | No vertical separators between columns |
| Input cell (optional highlight) | White or very faint tint | Blue (0000FF) text per above | Thin black box border | Only if the template calls for boxed input cells |

**Rules:**
- **Never** put Navy fill directly above Mid Blue fill (or vice versa) — pick one per header stack.
- **White text** on any Navy or Mid Blue or Dark Grey fill. Black text everywhere else.
- **Subtotals are always bold with a black top border.** The top border signals "this row sums what's above it."
- **Grand totals are bold with a black top border AND an accounting-underline on the bottom.** This is the double-line "final answer" convention.
- **No vertical cell borders** inside tables — INFOR convention uses white gridlines and horizontal rules only.
- **Right-align all numeric cells**, including inside totals and subtotals rows.
- **Accretion/(Dilution) output row** is a grand total — give it the Dark Grey fill, white bold text, top border, and bottom accounting underline. It is the headline number of the model.

### Number Formatting Standards
* **Currency**: `$#,##0;($#,##0);"-"` or `$#,##0.0` depending on template
* **Per share values (EPS, share price)**: `$0.00` (two decimals)
* **Percentages**: `0.0%` (one decimal)
* **Accretion/Dilution %**: `0.0%;(0.0%)` — parentheses on dilution
* **Multiples (EV/EBITDA, P/E)**: `0.0"x"` (one decimal)
* **Share counts (millions)**: `#,##0.0` (one decimal, in millions)
* **All numeric cells**: Right-aligned

---

### Clarify Requirements First

Before filling any formulas:

* **Examine the template structure** — Identify all sections, understand the timeline (Year 1, Year 2, Year 3), note any existing formulas
* **Ask the user if anything is unclear** — If the template structure, calculation methods, or requirements are ambiguous, ask before proceeding
* **Confirm key assumptions** — Offer premium, cash/stock mix, synergy assumptions, close date, tax rate, cost of debt
* **ONLY AFTER understanding the template**, proceed to fill in formulas

---

## WORKFLOW

### Step 1: Gather Inputs

**Acquirer:**
- Company name, current share price, shares outstanding
- LTM and NTM EPS (GAAP and adjusted)
- P/E multiple
- Pre-tax cost of debt, tax rate
- Cash on balance sheet, existing debt

**Target:**
- Company name, current share price, shares outstanding (if public)
- LTM and NTM EPS or net income
- Enterprise value or equity value

**Deal Terms:**
- Offer price per share (or premium to current)
- Consideration mix: % cash vs. % stock
- New debt raised to fund cash portion
- Expected synergies (revenue and cost) and phase-in timeline
- Transaction fees and financing costs
- Expected close date

### Step 2: Purchase Price Analysis

| Item | Value |
|------|-------|
| Offer price per share | |
| Premium to current | |
| Equity value | |
| Plus: net debt assumed | |
| Enterprise value | |
| EV / EBITDA implied | |
| P/E implied | |

Format the section header (Navy Blue fill, white bold text). The final Enterprise Value and implied multiples should sit in a grand-total row (Dark Grey fill, white bold, top border, bottom accounting underline).

### Step 3: Sources & Uses

| Sources | $ | Uses | $ |
|---------|---|------|---|
| New debt | | Equity purchase price | |
| Cash on hand | | Refinance target debt | |
| New equity issued | | Transaction fees | |
| | | Financing fees | |
| **Total** | | **Total** | |

Sources MUST equal Uses — one line is the plug (typically new debt or new equity issued depending on structure). Totals rows use Dark Grey fill, white bold, top border, bottom accounting underline.

### Step 4: Pro Forma EPS (Accretion / Dilution)

Calculate year-by-year (Year 1-3):

| | Standalone | Pro Forma | Accretion/(Dilution) |
|---|-----------|-----------|---------------------|
| Acquirer net income | | | |
| Target net income | | | |
| Synergies (after tax) | | | |
| Foregone interest on cash (after tax) | | | |
| New debt interest (after tax) | | | |
| Intangible amortization (after tax) | | | |
| Pro forma net income | | | |
| Pro forma shares | | | |
| **Pro forma EPS** | | | |
| **Accretion / (Dilution) %** | | | |

- Pro forma net income and Pro forma EPS rows are subtotals (Light Grey fill, bold, black top border).
- The Accretion / (Dilution) % row is the grand total headline (Dark Grey fill, white bold, top border, bottom accounting underline).
- Show GAAP and adjusted (cash) EPS where relevant — add a second block if the user needs both.

### Step 5: Sensitivity Analysis

**Accretion/Dilution vs. Synergies and Offer Premium:**

| | $0M syn | $25M syn | $50M syn | $75M syn | $100M syn |
|---|---------|----------|----------|----------|-----------|
| 15% premium | | | | | |
| 20% premium | | | | | |
| 25% premium | | | | | |
| 30% premium | | | | | |

**Accretion/Dilution vs. Cash/Stock Mix:**

| | 100% cash | 75/25 | 50/50 | 25/75 | 100% stock |
|---|-----------|-------|-------|-------|------------|
| Year 1 | | | | | |
| Year 2 | | | | | |

Sensitivity table axes should be built with mixed references (`$A5` for row input, `B$4` for column input). Every cell must show a different value — if all are identical, the formula is not varying with inputs. Center the base case on a row/column so the matching cell ties back to the model's reported accretion/dilution.

### Step 6: Breakeven Synergies

Calculate the minimum synergies needed for the deal to be EPS-neutral in Year 1. Present as a single callout row or box using the INFOR "key output" treatment (Navy Blue fill, white bold text).

### Step 7: Output

- Excel workbook with:
  - Assumptions tab
  - Sources & uses
  - Pro forma income statement
  - Accretion/dilution summary
  - Sensitivity tables
  - Breakeven analysis
- One-page merger consequences summary for the pitch book — follow INFOR deck branding (use `brand-guidelines-infor` and the INFOR Deck Template for the slide)

---

## TEMPLATE ANALYSIS PHASE - DO THIS FIRST (WHEN USER PROVIDES A TEMPLATE)

Before filling any formulas, examine the template thoroughly:

1. **Map the structure** — Identify where each section lives and how they relate to each other. Note which sections feed into others.
2. **Understand the timeline** — Which columns are Year 1/2/3? Is there a Pro Forma column at close?
3. **Identify input vs formula cells** — Templates often use color coding, borders, or shading to indicate which cells need inputs vs formulas. Respect these conventions.
4. **Read existing labels carefully** — The row labels tell you exactly what calculation is expected. Don't assume — read what the template is asking for.
5. **Check for existing formulas** — Some templates come partially filled. Don't overwrite working formulas unless specifically asked.
6. **Note template-specific conventions** — Sign conventions, subtotal structures, whether GAAP and cash EPS are shown separately, etc.

---

## FILLING FORMULAS - GENERAL APPROACH

For each cell that needs a formula, follow this hierarchy:

### Step 1: Check the Template
* Does the cell already have a formula? If yes, verify it's correct and move on.
* Is there a comment or note indicating the expected calculation?
* Does the row/column label make the calculation obvious?
* Do neighboring cells show a pattern you should follow?

### Step 2: Check the User's Instructions
* Did the user specify a particular calculation method?
* Are there stated assumptions that affect this formula?
* Any special requirements mentioned?

### Step 3: Apply Standard Practice
* If neither template nor user specifies, use standard merger modeling conventions
* Document any assumptions you make
* If genuinely uncertain, ask the user

---

## COMMON PROBLEM AREAS

The following calculation patterns frequently cause issues across merger models. Pay special attention when you encounter these:

### Balancing Sections
* Sources must equal Uses — one item is the plug (typically new debt or new equity issued)
* Identify the plug and calculate it as the difference

### Purchase Price Allocation
* Excess of purchase price over target book value creates goodwill and identifiable intangibles
* Intangibles amortize over their useful lives → creates GAAP (but not cash) EPS drag
* Goodwill does NOT amortize under GAAP — no EPS impact unless impaired

### Interest Adjustments
* **Foregone interest on cash used**: cash × after-tax return on cash (often low — money market or short-term)
* **New debt interest**: new debt × pre-tax cost of debt × (1 - tax rate)
* Both flow through the Pro Forma income statement as below-the-line adjustments
* Interest expense should use beginning debt balance if debt is paid down over time

### Synergy Phase-In
* Year 1 is often only 25–50% of run-rate synergies — don't forget the ramp
* Synergies are after-tax in the EPS walk: `synergies × (1 - tax rate)`
* Split revenue synergies and cost synergies if the user distinguishes them

### Stock Consideration
* Stock deals use the acquirer's current (or a reference) price for the exchange ratio
* New shares issued = (stock portion of deal value) / (acquirer share price)
* Pro forma share count = acquirer existing shares + new shares issued
* Don't forget pro forma share count drives the denominator of pro forma EPS

### Tax Rate Consistency
* Tax rate on synergies and interest adjustments should match the acquirer's marginal rate
* Don't mix effective vs. marginal rates across the EPS walk

### Sensitivity Tables
* Excel's DATA TABLE function may not work with openpyxl
* Use explicit formulas that reference row/column headers via mixed references (`$A5`, `B$4`)
* Each cell should show a DIFFERENT value — if all same, formulas aren't varying correctly
* Base-case assumptions should line up with a specific cell in the table — verify it ties to the model's reported accretion/dilution

---

## VERIFICATION CHECKLIST - RUN AFTER COMPLETION

### Run Formula Validation
```bash
python /mnt/skills/public/xlsx/recalc.py model.xlsx
```
Must return success with zero errors.

### Section Balancing
- [ ] Sources equal Uses exactly
- [ ] Plug item (new debt or new equity) is calculated correctly as the balancing figure
- [ ] Equity value + net debt = Enterprise Value in the purchase price block

### Purchase Price
- [ ] Offer price × shares outstanding = equity value
- [ ] Premium = (offer price / current price) − 1
- [ ] EV / EBITDA and implied P/E use the correct numerator and denominator
- [ ] Net debt includes all debt tranches (and nets cash) per the target's balance sheet

### Pro Forma Income Statement
- [ ] Acquirer standalone net income ties to source data
- [ ] Target standalone net income ties to source data
- [ ] Synergies are after-tax and phased in correctly (Year 1 partial, Year 2+ full run-rate)
- [ ] Foregone interest on cash = cash used × after-tax return on cash
- [ ] New debt interest = new debt × cost of debt × (1 − tax rate)
- [ ] Intangible amortization is tax-effected appropriately (tax deductible for asset deals, may not be for stock deals — confirm)
- [ ] Pro forma net income = sum of all adjustments
- [ ] Pro forma shares = acquirer shares + new shares issued (stock portion only)

### Accretion / (Dilution)
- [ ] Pro forma EPS = Pro forma net income / Pro forma shares
- [ ] Accretion / Dilution = (Pro forma EPS / Standalone EPS) − 1
- [ ] Sign convention: positive = accretion, negative = dilution (shown in parentheses)
- [ ] Year 1, Year 2, Year 3 columns all populated and trending sensibly

### Sensitivity Tables
- [ ] Row and column headers contain appropriate input values
- [ ] Each data cell contains a formula (not hardcoded)
- [ ] Each data cell shows a DIFFERENT value
- [ ] Values move in expected directions (higher synergies → more accretive; higher premium → less accretive or more dilutive)
- [ ] Base case matches the model's headline accretion/dilution in the corresponding cell

### Breakeven Synergies
- [ ] Breakeven synergies make the pro forma EPS equal standalone EPS in Year 1
- [ ] Formula references the model's actual Year 1 accretion/dilution mechanics

### Formatting

Formula font colors (IB standard):
- [ ] Hardcoded inputs are blue (0000FF)
- [ ] Calculated formulas are black (000000)
- [ ] Same-tab links are purple (800080)
- [ ] Cross-tab links are green (008000)

Fills and borders (INFOR palette):
- [ ] Title rows and standalone table headers use Navy Blue (0E213F) fill with white bold text
- [ ] Section header rows use Navy Blue (0E213F) fill with white bold text
- [ ] Table headers nested under a Navy section header use Mid Blue (46566E) fill with white bold text (no stacked Navy rows)
- [ ] Subtotal rows have Light Grey (E5E3E3) fill, bold text, and a black top border
- [ ] Grand total rows (including Accretion/(Dilution) %) have Dark Grey (767171) fill, white bold text, a black top border, and a single accounting underline on the bottom
- [ ] Alternating body row shading (where used) is Light Grey (E5E3E3)
- [ ] Table gridlines are white, 0.75pt; no vertical separators
- [ ] No Navy fill stacked directly above/below Mid Blue fill
- [ ] All numbers are right-aligned, including in subtotal and total rows
- [ ] Appropriate number formats applied throughout (EPS `$0.00`, accretion/dilution `0.0%;(0.0%)`, multiples `0.0"x"`)
- [ ] No cells show error values (#REF!, #DIV/0!, #VALUE!, #NAME?)

### Logical Sanity Checks
- [ ] Numbers are reasonable order of magnitude
- [ ] Accretion/dilution magnitude is sensible (typically low single digits to mid teens)
- [ ] Accretion improves over time if synergies phase in
- [ ] Breakeven synergies is below total run-rate synergies (otherwise the deal is structurally dilutive)

---

## COMMON ERRORS TO AVOID

| Error | What Goes Wrong | How to Fix |
|-------|-----------------|------------|
| Hardcoding calculated values | Model doesn't update when inputs change | Always use formulas that reference source cells |
| Forgetting pro forma share count | Stock deals show wrong EPS | Pro forma shares = acquirer shares + new shares issued from the stock portion |
| Forgetting foregone interest on cash | Overstates accretion on cash-funded deals | Subtract cash used × after-tax return on cash |
| Pre-tax synergies in EPS walk | Overstates accretion | Synergies must be after-tax: × (1 − tax rate) |
| Year 1 uses full run-rate synergies | Overstates Year 1 accretion | Phase in — typically 25–50% in Year 1 |
| Using average or ending debt for interest | Creates circularity or wrong interest | Use beginning/opening debt balance |
| Sources ≠ Uses | Deal doesn't fund | Make one line the plug, calculated as the difference |
| Sensitivity table shows same value | Formula not varying with inputs | Check cell references — need mixed references (`$A5`, `B$4`) |
| GAAP vs. cash EPS mixed up | Amortization treated inconsistently | Show both if relevant; be explicit which one the accretion/dilution % refers to |

---

## WORKING WITH THE USER

* **If the template structure is unclear**, ask before proceeding
* **If the user's requirements conflict with the template**, confirm their preference
* **After completing each major section**, offer to show the work or run verification
* **If errors are found during verification**, fix them before moving to the next section
* **Show your work** — explain key formulas or assumptions when helpful

---

**This skill produces INFOR-branded merger (accretion/dilution) models by filling templates with correct formulas (IB-standard formula font colors), INFOR-palette fills and borders for titles/headers/subtotals/totals, and validated calculations. The skill adapts to any template structure while ensuring financial accuracy and professional presentation standards.**
