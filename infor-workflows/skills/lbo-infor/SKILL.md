---
name: lbo-infor
description: This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill builds a target-company capitalization table first (via captable-infor), embeds it in the LBO workbook, and links balance-sheet-derived assumptions (cash, shares outstanding, debt, EV inputs) from the cap table. Fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure. Output uses INFOR Financial Group brand colors.
version: 1.9.0
---

---

## TEMPLATE REQUIREMENT

**This skill uses templates for LBO models. Always check for an attached template file first.**

Before starting any LBO model:
1. **Build the target capitalization table FIRST** — see the *CAP TABLE INTEGRATION* section below. Every LBO built with this skill begins with a populated cap table (via `captable-infor`) that is then embedded in the LBO workbook. Balance-sheet-derived LBO assumptions (cash, shares O/S, debt, etc.) are linked from the cap table, not hardcoded.
2. **If a template file is attached/provided**: Use that template's structure exactly - copy it and populate with the user's data
3. **If no template is attached**: Ask the user: *"Do you have a specific LBO template you'd like me to use? If not, I can use the standard template which includes Sources & Uses, Operating Model, Debt Schedule, and Returns Analysis."*
4. **If using the standard template**: Copy `examples/LBO_Model.xlsx` as your starting point and populate it with the user's assumptions

**IMPORTANT**: When a file like `LBO_Model.xlsx` is attached, you MUST use it as your template - do not build from scratch. Even if the template seems complex or has more features than needed, copy it and adapt it to the user's requirements. Never decide to "build from scratch" when a template is provided.

---

## CRITICAL INSTRUCTIONS FOR CLAUDE - READ FIRST

### Core Principles
* **Every calculation must be an Excel formula** - NEVER compute values in Python and hardcode results into cells. The model must be dynamic and update when inputs change.
* **Use the template structure** - Follow the organization in `examples/LBO_Model.xlsx` or the user's provided template. Do not invent your own layout.
* **Use proper cell references** - All formulas should reference the appropriate cells. Never type numbers that should come from other cells.
* **Company-state inputs come from the cap table** - Any assumption that describes the target's current balance sheet (cash, shares outstanding, debt by tranche, leases, preferred, NCI, dilutive securities) must be populated as a cross-tab link into the embedded `Cap with Links` sheet, NOT typed as a hardcoded number. Deal-specific inputs (offer price, fees, new debt, synergies) remain hardcoded blue inputs. See *CAP TABLE INTEGRATION* below.
* **Maintain sign convention consistency** - Follow whatever sign convention the template uses (some use negative for outflows, some use positive). Be consistent throughout.
* **Work section by section** - Complete one section fully before moving to the next, as later sections often depend on earlier ones.

### Formula Font Color Conventions (IB Standard)
* **Blue (0000FF)**: Hardcoded inputs - typed numbers that don't reference other cells
* **Black (000000)**: Formulas with calculations - any formula using operators or functions (`=B4*B5`, `=SUM()`, `=-MAX(0,B4)`)
* **Purple (800080)**: Links to cells on the **same tab** - direct references with no calculation (`=B9`, `=B45`)
* **Green (008000)**: Links to cells on **different tabs** - cross-sheet references (`=Assumptions!B5`, `='Operating Model'!C10`)

### Cell Fill & Border Conventions (INFOR Palette)

Font colors above track formula type; fills and borders below carry the INFOR visual identity.

| Element | Fill | Text | Border / Weight | Notes |
|---------|------|------|------------------|-------|
| Title row (top of sheet / section title) | **Navy Blue (0E213F)** | White, bold | — | Used for sheet title banners and standalone table headers |
| Section header row | **Navy Blue (0E213F)** | White, bold | — | Section header boxes above a block of content |
| Table header under a section header | **Mid Blue (46566E)** | White, bold | — | When the table already sits under a Navy section header, use Mid Blue so two Navy rows don't stack |
| Subtotal row | **Light Grey (E5E3E3)** | Black, **bold** | **Black top border** (thin, ~0.75pt) | Use for subtotals (e.g., Gross Profit, Total Sources, Total Debt) |
| Alternate subtotal row | **Light Blue (ADB9CA)** | Black, bold | Black top border | Use only when Light Grey subtotals already appear directly above/below and you need visual separation |
| Totals row (grand total) | **Dark Grey (767171)** | White, bold | Black top border; single-line bottom accounting underline | Use for the final total of a section (e.g., Ending Debt Balance, Total Equity Value) |
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

### Number Formatting Standards
* **Currency**: `$#,##0;($#,##0);"-"` or `$#,##0.0` depending on template
* **Percentages**: `0.0%` (one decimal)
* **Multiples**: `0.0"x"` (one decimal)
* **MOIC/Detailed Ratios**: `0.00"x"` (two decimals for precision)
* **All numeric cells**: Right-aligned

---

### Clarify Requirements First

Before filling any formulas:

* **Examine the template structure** - Identify all sections, understand the timeline (which columns are which periods), note any existing formulas
* **Ask the user if anything is unclear** - If the template structure, calculation methods, or requirements are ambiguous, ask before proceeding
* **Confirm key assumptions** - Any key inputs, calculation preferences, or specific requirements
* **ONLY AFTER understanding the template**, proceed to fill in formulas

---

## CAP TABLE INTEGRATION — STEP 0 (DO THIS FIRST)

**Every LBO model built with this skill begins with a target-company capitalization table.** The cap table is the source of truth for the target's opening balance sheet — cash, shares outstanding, debt, leases, preferred, NCI, and dilutive securities. The LBO's Assumptions tab still *lists* all of these line items, but they are **linked** from the embedded cap table rather than typed in as hardcoded numbers.

### Step 0a — Build the cap table

Run the **`captable-infor`** skill on the target company first. Follow that skill's workflow in full — collect the CapIQ ticker and attached filings, copy the `INFOR Cap Table Template.xlsx`, populate the `Cap with Links` sheet (shares outstanding, options/warrants/RSUs, convertibles, debt schedule, leases, cash, preferred, NCI), and attach cell comments citing the source for each extracted value.

The output is a standalone cap table workbook (e.g., `NasdaqGS-MSFT - Capitalization Table.xlsx`). Verify it recalcs cleanly and the cross-checks in the captable-infor skill all pass before proceeding.

### Step 0b — Embed cap table tabs in the LBO workbook

Copy the `Cap Summary` and `Cap with Links` sheets from the cap table workbook into the LBO workbook so all cross-sheet formulas resolve within one file. Preserve formulas — do NOT flatten to values. Copy cell-by-cell with openpyxl, preserving `cell.value`, `cell.font`, `cell.fill`, `cell.border`, `cell.alignment`, `cell.number_format`, and any comments.

**Resulting LBO workbook tab order:**
1. `Cap Summary` — from captable-infor (reference view)
2. `Cap with Links` — from captable-infor (**source of truth** for linked assumptions)
3. `Assumptions` — LBO deal and operating assumptions
4. `Sources & Uses`
5. `Operating Model`
6. `Debt Schedule`
7. `Returns`

(If the user's LBO template has a different tab order, insert the two cap table tabs as the leftmost tabs and adjust downstream tab names accordingly.)

### Step 0c — Link balance-sheet assumptions to `Cap with Links`

On the LBO Assumptions tab, every line item below must be a cross-tab formula pointing into `Cap with Links`. These cells render in **green (008000)** per the IB-standard formula color convention (cross-tab links).

| LBO Assumption line item | `Cap with Links` cell | Formula |
|---|---|---|
| Cash & Equivalents | F123 | `='Cap with Links'!F123` |
| Basic Shares Outstanding | F137 | `='Cap with Links'!F137` |
| Total Debt | F99 | `='Cap with Links'!F99` |
| Lease Obligations | F111 | `='Cap with Links'!F111` |
| Convertible Debentures | F87 | `='Cap with Links'!F87` |
| Dilutive Options / Warrants / RSUs (TSM dilutive shares) | F73 | `='Cap with Links'!F73` |
| Preferred Shares | F52 | `='Cap with Links'!F52` |
| Non-Controlling Interest | F53 | `='Cap with Links'!F53` |

**Do not delete these rows from the Assumptions tab.** They must remain visible as labeled line items so the reader can see the full opening balance sheet — they are simply now populated by cross-tab formulas instead of typed-in blue values.

### Step 0d — Derived values (Equity Value, Net Debt, Enterprise Value)

With the inputs above linked from the cap table, the LBO's headline purchase-price figures are derived formulas on the LBO Assumptions or Sources & Uses tab:

- **Diluted Shares** = Basic Shares + TSM dilutive shares (links to F137 + F73 via the Assumptions rows above)
- **Equity Purchase Price** = Offer Price per Share (hardcoded blue input) × Diluted Shares
- **Net Debt** = Total Debt + Lease Obligations (if treated as debt) − Cash
- **Enterprise Value** = Equity Purchase Price + Net Debt + Preferred + NCI + Convertibles-at-face (if settled in cash at close)

Every one of these is a formula that traces back to `Cap with Links` through the Assumptions tab — never typed numbers.

### What stays hardcoded (blue inputs) in Assumptions

These describe the **deal** or the **forecast**, not the target's current balance sheet, and remain typed-in blue inputs:

- Offer price per share and implied premium
- Target tax rate (if overriding reported ETR)
- Transaction fees (advisory, financing, legal)
- New capital structure at close (term loan size, notes, revolver commitment, drawn balance)
- Pricing on new debt (SOFR spread, fixed coupon, OID, upfront fees)
- Sponsor equity check
- Operating model drivers (revenue growth, margin expansion, capex %, NWC %)
- Exit year and exit multiple
- Synergies, if modeled

### Rule of thumb

> If a number describes the **target's current state**, link it from `Cap with Links` (green cross-tab formula).
> If a number describes the **deal terms or the forecast**, hardcode it as a blue input.

### Verification add-on (run during the main checklist)

- [ ] `Cap Summary` and `Cap with Links` tabs are present in the LBO workbook
- [ ] Every balance-sheet-derived assumption on the LBO Assumptions tab is a green cross-tab formula, not a blue hardcoded number
- [ ] Changing any value on `Cap with Links` propagates through to Assumptions → Sources & Uses → Returns
- [ ] The cap table's own internal cross-checks (F17=F137, revolver present, no PSUs, etc.) still pass after the tabs were copied into the LBO workbook

---

## TEMPLATE ANALYSIS PHASE - DO THIS FIRST

Before filling any formulas, examine the template thoroughly:

1. **Map the structure** - Identify where each section lives and how they relate to each other. Note which sections feed into others.

2. **Understand the timeline** - Which columns represent which periods? Is there a "Closing" or "Pro Forma" column? Where does the projection period start?

3. **Identify input vs formula cells** - Templates often use color coding, borders, or shading to indicate which cells need inputs vs formulas. Respect these conventions.

4. **Read existing labels carefully** - The row labels tell you exactly what calculation is expected. Don't assume - read what the template is asking for.

5. **Check for existing formulas** - Some templates come partially filled. Don't overwrite working formulas unless specifically asked.

6. **Note template-specific conventions** - Sign conventions, subtotal structures, how sections are organized, whether there are separate tabs for different components, etc.

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
* If neither template nor user specifies, use standard LBO modeling conventions
* Document any assumptions you make
* If genuinely uncertain, ask the user

---

## COMMON PROBLEM AREAS

The following calculation patterns frequently cause issues across LBO models. Pay special attention when you encounter these:

### Balancing Sections
* When two sections must equal (e.g., Sources = Uses), one item is typically the "plug" (balancing figure)
* Identify which item is the plug and calculate it as the difference

### Tax Calculations
* Tax formulas should only reference the relevant income line and tax rate
* Should NOT reference unrelated sections (e.g., debt schedules)
* Consider whether losses create tax shields or are simply ignored

### Interest and Circular References
* Interest calculations can create circularity if they reference balances affected by cash flows
* Use **Beginning Balance** (not average or ending) to break circular references
* Pattern: Interest → Cash Flow → Paydown → Ending Balance (if interest uses ending balance, this circles back)

### Debt Paydown / Cash Sweeps
* When multiple debt tranches exist, there's usually a priority order
* Cash sweep should respect the priority waterfall
* Balances cannot go negative - use MAX or MIN functions appropriately

### Returns Calculations (IRR/MOIC)
* Cash flows must have correct signs: Investment = negative, Proceeds = positive
* If using XIRR, need corresponding dates
* If using IRR, cash flows should be in consecutive periods
* MOIC = Total Proceeds / Total Investment

### Sensitivity Tables
* Excel's DATA TABLE function may not work with openpyxl
* May need explicit formulas that reference row/column headers
* Each cell should show a DIFFERENT value - if all same, formulas aren't varying correctly
* Use mixed references (e.g., $A5 for row input, B$4 for column input)

---

## VERIFICATION CHECKLIST - RUN AFTER COMPLETION

### Run Formula Validation
```bash
python /mnt/skills/public/xlsx/recalc.py model.xlsx
```
Must return success with zero errors.

### Section Balancing
- [ ] Any sections that must balance (Sources/Uses, Assets/Liabilities) balance exactly
- [ ] Plug items are calculated correctly as the balancing figure
- [ ] Amounts that should match across sections are consistent

### Income/Operating Projections
- [ ] Revenue/top-line builds correctly from drivers or growth rates
- [ ] All cost and expense items calculated appropriately
- [ ] Subtotals and totals sum correctly
- [ ] Margins and ratios are reasonable
- [ ] Links to assumptions are correct

### Balance Sheet (if applicable)
- [ ] Assets = Liabilities + Equity (must balance)
- [ ] All items link to appropriate schedules or roll-forwards
- [ ] Beginning balances = prior period ending balances
- [ ] Check row included and shows zero

### Cash Flow (if applicable)
- [ ] Starts with correct income figure
- [ ] Non-cash items added/subtracted appropriately
- [ ] Working capital changes have correct signs
- [ ] Ending Cash = Beginning Cash + Net Cash Flow
- [ ] Cash balances are consistent across statements

### Supporting Schedules
- [ ] Roll-forward schedules balance (Beginning + Changes = Ending)
- [ ] Schedules link correctly to main statements
- [ ] Calculated items use appropriate drivers
- [ ] All periods are calculated consistently

### Debt/Financing Schedules (if applicable)
- [ ] Beginning balances tie to sources or prior period
- [ ] Interest calculated on appropriate balance (typically beginning)
- [ ] Paydowns respect cash availability and priority
- [ ] Ending balances cannot be negative
- [ ] Totals sum tranches correctly

### Returns/Output Analysis
- [ ] Exit/terminal values calculated correctly
- [ ] All relevant adjustments included
- [ ] Cash flow signs are correct (negative for investment, positive for proceeds)
- [ ] IRR/MOIC formulas reference complete ranges
- [ ] Results are reasonable for the scenario

### Sensitivity Tables (if applicable)
- [ ] Row and column headers contain appropriate input values
- [ ] Each data cell contains a formula (not hardcoded)
- [ ] Each data cell shows a DIFFERENT value
- [ ] Values move in expected directions
- [ ] Base case appears where headers match base assumptions

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
- [ ] Grand total rows have Dark Grey (767171) fill, white bold text, a black top border, and a single accounting underline on the bottom
- [ ] Alternating body row shading (where used) is Light Grey (E5E3E3)
- [ ] Table gridlines are white, 0.75pt; no vertical separators
- [ ] No Navy fill stacked directly above/below Mid Blue fill
- [ ] All numbers are right-aligned, including in subtotal and total rows
- [ ] Appropriate number formats applied throughout
- [ ] No cells show error values (#REF!, #DIV/0!, #VALUE!, #NAME?)

### Logical Sanity Checks
- [ ] Numbers are reasonable order of magnitude
- [ ] Trends make sense (growth, decline, stabilization as expected)
- [ ] No obviously wrong values (negative where should be positive, impossible percentages, etc.)
- [ ] Key outputs are within reasonable ranges for the type of analysis

---

## COMMON ERRORS TO AVOID

| Error | What Goes Wrong | How to Fix |
|-------|-----------------|------------|
| Hardcoding calculated values | Model doesn't update when inputs change | Always use formulas that reference source cells |
| Wrong cell references after copying | Formulas point to wrong cells | Verify all links, use appropriate $ anchoring |
| Circular reference errors | Model can't calculate | Use beginning balances for interest-type calcs, break the circle |
| Sections don't balance | Totals that should match don't | Ensure one item is the plug (calculated as difference) |
| Negative balances where impossible | Paying/using more than available | Use MAX(0, ...) or MIN functions appropriately |
| IRR/return errors | Wrong signs or incomplete ranges | Check cash flow signs and ensure formula covers all periods |
| Sensitivity table shows same value | Formula not varying with inputs | Check cell references - need mixed references ($A5, B$4) |
| Roll-forwards don't tie | Beginning ≠ prior ending | Verify links between periods |
| Inconsistent sign conventions | Additions become subtractions or vice versa | Follow template's convention consistently throughout |

---

## WORKING WITH THE USER

* **If the template structure is unclear**, ask before proceeding
* **If the user's requirements conflict with the template**, confirm their preference
* **After completing each major section**, offer to show the work or run verification
* **If errors are found during verification**, fix them before moving to the next section
* **Show your work** - explain key formulas or assumptions when helpful

---

**This skill produces INFOR-branded LBO models by (1) first building the target's capitalization table via `captable-infor` and embedding it in the LBO workbook, (2) linking balance-sheet-derived assumptions (cash, shares O/S, debt, leases, preferred, NCI, dilutives) from `Cap with Links` rather than hardcoding them, (3) filling templates with correct formulas (IB-standard formula font colors), (4) applying INFOR-palette fills and borders for titles/headers/subtotals/totals, and (5) validating calculations. The skill adapts to any template structure while ensuring financial accuracy and professional presentation standards.**
