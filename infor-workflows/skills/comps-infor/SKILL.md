---
name: comps-infor
description: >
  Use this skill when the user invokes /comps-infor or asks to build a public comparables table
  (comps, trading comps, public comps) for a company. Populates the INFOR Comps Template with
  18 CapIQ tickers split into three labelled groups, plus a short description for each company.
version: 1.9.10
---

# INFOR Public Comparables Table — Workflow

This skill builds a public comparable companies table by selecting 18 peers and writing their CapIQ tickers, group labels, and one-line descriptions into the INFOR Comps Template.

Allowed tools: Read, Bash, Write, Glob, WebSearch

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Collect Input

Ask for the target company name if not already provided:

> "Please provide the name of the company you'd like me to build a comparable companies table for."

Wait for the company name before proceeding.

---

### Step 2 — Select 18 Public Comparables

Using your knowledge of public markets (and WebSearch if needed to verify current tickers or identify relevant peers), select **18 publicly traded comparable companies** for the target.

**Grouping logic — pick ONE dimension and apply it to all three groups. Never mix.**

All three group labels must share the same grouping dimension — either **all geography** or **all sector/vertical**. Do not combine the two axes in the same table.

- **By Geography** — when the target operates in a specific region and regional peers are meaningful. All three labels are regions (e.g., `"Canadian Peers"`, `"U.S. Peers"`, `"European Peers"`; or `"Canada"`, `"U.S."`, `"Rest of World"`).
- **By Sector / Vertical** — when the target spans geographies but has distinct business lines or sub-sectors. All three labels are business types (e.g., `"Core Software"`, `"Payments & FinTech"`, `"Data & Analytics"`).

**Invalid — do not produce tables like this:**
- ❌ `"Large-Cap Engineering Consultants"`, `"MEP Firms"`, `"European Engineering Consultants"` — mixes sector (first two) with geography (third)
- ❌ `"U.S. Software"`, `"European Software"`, `"Payments & FinTech"` — mixes geography with sector
- ❌ `"Canadian Peers"`, `"U.S. Peers"`, `"Global SaaS"` — mixes geography with sector

Before writing to the file, read back your three group labels and confirm they answer the same question ("where?" or "what?"). If they don't, re-group.

Split the 18 comparables into **three groups of exactly 6**. Each group must have a clear, concise label (3–6 words max).

**Ticker format:** Use CapIQ format — `Exchange:Ticker` (e.g., `NasdaqGS:MSFT`, `NasdaqGM:RPD`, `TSX:RY`, `NYSE:JPM`).

**Nasdaq tier — verify, don't guess.** Nasdaq has three tiers (`NasdaqGS`, `NasdaqGM`, `NasdaqCM`) and CapIQ treats them as distinct prefixes. Defaulting to `NasdaqGS` for every Nasdaq name will silently break the lookup for anything actually on GM or CM (e.g., `NasdaqGM:RPD`, not `NasdaqGS:RPD`). If you are not certain of the tier, **use WebSearch to confirm before writing it**. See the Domain Reference for the full tier table.

For each company, draft a short description (see Description Rules in the Domain Reference). Proceed directly to writing the file — do not pause for user confirmation.

---

### Step 3 — Locate and Copy the Template

The template path is shown in the Context section above. If blank, search for it — check the repo's templates directory first, then the plugin cache, then fall back to $HOME:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1
```

Sanitize the target company name for use as a filename (remove special characters, replace spaces with hyphens).

Copy the template to the current working directory:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TEMPLATE=$(find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Comps Template.xlsx" 2>/dev/null | head -1)
OUTPUT="./$SANITIZED_COMPANY_NAME - Comparable Companies.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

**If the result is `COPY_FAILED` or the file is missing — STOP immediately. Do NOT create a manual comps table. Tell the user the template could not be found.**

---

### Step 4 — Write to Excel (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

Write **exactly 39 cells** in the `Comps` sheet (3 group labels + 18 tickers + 18 descriptions). No other cells should be touched.

| Cell | Value |
|------|-------|
| D9   | Group 1 label (e.g., `"Canadian Peers"`) — replaces `[Group #1]` |
| B10  | Ticker 1 in CapIQ format (e.g., `"TSX:RY"`) |
| B11  | Ticker 2 |
| B12  | Ticker 3 |
| B13  | Ticker 4 |
| B14  | Ticker 5 |
| B15  | Ticker 6 |
| AL10 | Description for company 1 |
| AL11 | Description for company 2 |
| AL12 | Description for company 3 |
| AL13 | Description for company 4 |
| AL14 | Description for company 5 |
| AL15 | Description for company 6 |
| D19  | Group 2 label (e.g., `"U.S. Peers"`) — replaces `[Group #2]` |
| B20  | Ticker 7 |
| B21  | Ticker 8 |
| B22  | Ticker 9 |
| B23  | Ticker 10 |
| B24  | Ticker 11 |
| B25  | Ticker 12 |
| AL20 | Description for company 7 |
| AL21 | Description for company 8 |
| AL22 | Description for company 9 |
| AL23 | Description for company 10 |
| AL24 | Description for company 11 |
| AL25 | Description for company 12 |
| D29  | Group 3 label (e.g., `"European Peers"`) — replaces `[Group #3]` |
| B30  | Ticker 13 |
| B31  | Ticker 14 |
| B32  | Ticker 15 |
| B33  | Ticker 16 |
| B34  | Ticker 17 |
| B35  | Ticker 18 |
| AL30 | Description for company 13 |
| AL31 | Description for company 14 |
| AL32 | Description for company 15 |
| AL33 | Description for company 16 |
| AL34 | Description for company 17 |
| AL35 | Description for company 18 |

All 39 values are plain strings. Do not modify any other cell. Leave AL9, AL19, AL29 (group header rows) blank.

Save the file.

---

### Step 5 — Summary

Report to the user in Markdown using the exact structure below.

**Output file:** path to the saved file

Then, for each of the three groups, emit a block in this format:

```
**[Group Label]**

[Company Name] ([CapIQ Ticker])
- One-line description of the company (what it is / who it serves)
   - One-line description of the product or service offering
- One-line rationale for including in comps (how it is similar to [Target Company])

[Company Name] ([CapIQ Ticker])
- …
   - …
- …
```

Repeat for all 6 companies in the group. Then move to the next group header. All 18 companies must appear.

**Content rules for the bullets:**
- First bullet (company description): what the company is — business model, client segment, end market. One line.
- Sub-bullet (product/service offering): the specific product, platform, or service the company sells. One line. Must be a nested bullet under the first bullet (3-space indent + `-`).
- Third bullet (inclusion rationale): **why this company is a relevant comp for the target** — the shared dimension(s): business model, size, end market, growth profile, or geography. Reference the target by name. One line.
- Every bullet is a single line. No trailing punctuation. Title case for company/product names only.

After all three groups, emit a **Group Rationale** section:

```
**Group Rationale**

**[Group 1 Label]**
- One-line reason this group is relevant to [Target Company]
- One-line reason this group is relevant to [Target Company]

**[Group 2 Label]**
- …
- …

**[Group 3 Label]**
- …
- …
```

Each group gets exactly 2 one-line bullets explaining why that group (as a category) is a meaningful comp set for the target — e.g., *"Global engineering consultancies share MCW's project-based revenue model and public-sector client concentration."* Focus on the category-level fit, not the individual companies.

Close with:

**Reminder:** Open in Excel with the CapIQ add-in active to populate all market data, multiples, and statistics automatically.

---

## Domain Reference

### Template Cell Map

| Cell | Purpose |
|------|---------|
| D9        | Group 1 section header (text label — replaces `[Group #1]`) |
| B10–B15   | CapIQ tickers for Group 1 companies (6 rows) |
| AL10–AL15 | One-line descriptions for Group 1 companies |
| D19       | Group 2 section header (text label — replaces `[Group #2]`) |
| B20–B25   | CapIQ tickers for Group 2 companies (6 rows) |
| AL20–AL25 | One-line descriptions for Group 2 companies |
| D29       | Group 3 section header (text label — replaces `[Group #3]`) |
| B30–B35   | CapIQ tickers for Group 3 companies (6 rows) |
| AL30–AL35 | One-line descriptions for Group 3 companies |

All other cells (D10–D15, D20–D25, D30–D35 and beyond columns E onward) contain CapIQ array formulas that auto-populate from the column B ticker when opened in Excel. **Never overwrite these.** Rows 17, 27, 37 contain Group Average formulas; rows 39–41 contain Global aggregates. Column AL cells are plain text input — no formulas.

### Description Rules

Column AL has a width of ~66 characters. Descriptions that exceed this will overflow visually.

- Describe **what the company does or sells** — product, service, asset class, client segment, or business model
- Target **45–65 characters**; **never exceed 65**
- Use the extra length to add meaningful specificity (e.g., end market, product focus, client segment) — do not pad with filler
- **Do not include geography** — already visible from the exchange prefix in the ticker (e.g., `TSX:RY` signals Canada)
- No trailing punctuation; title case preferred
- Examples (character counts):
  - `"Multi-asset & alternatives manager for institutional LPs"` (56)
  - `"Retail wealth platform offering mutual funds, ETFs, and advisory"` (64)
  - `"Independent advisory across M&A and capital markets"` (51)
  - `"Global payments & merchant acquiring for SMBs and enterprise"` (60)
  - `"Enterprise SaaS for financial services workflows and compliance"` (63)

### CapIQ Ticker Format

| Exchange | Format | Example |
|----------|--------|---------|
| Nasdaq Global Select | `NasdaqGS:TICK` | `NasdaqGS:MSFT` |
| Nasdaq Global Market | `NasdaqGM:TICK` | `NasdaqGM:RPD` |
| Nasdaq Capital Market | `NasdaqCM:TICK` | `NasdaqCM:XYZ` |
| NYSE | `NYSE:TICK` | `NYSE:JPM` |
| NYSE American | `NYSEAM:TICK` | `NYSEAM:XYZ` |
| NYSE Arca | `NYSEArca:TICK` | `NYSEArca:XYZ` |
| TSX | `TSX:TICK` | `TSX:RY` |
| TSX Venture | `TSXV:TICK` | `TSXV:XYZ` |
| London Stock Exchange | `LSE:TICK` | `LSE:HSBA` |
| ASX | `ASX:TICK` | `ASX:CBA` |

**⚠️ Nasdaq tier accuracy — critical**

Nasdaq has **three tiers** and CapIQ treats them as distinct exchange prefixes. Guessing `NasdaqGS` for every Nasdaq-listed company will silently break the CapIQ lookups for any company that is actually listed on GM or CM.

- **NasdaqGS** (Global Select) — top tier; large caps and most well-known names (AAPL, MSFT, GOOGL, AMZN).
- **NasdaqGM** (Global Market) — mid tier; many small-to-mid caps. Common miss: **Rapid7 is `NasdaqGM:RPD`**, not `NasdaqGS:RPD`.
- **NasdaqCM** (Capital Market) — entry tier; smaller / newer issuers.

**Rule:** If you are not 100% certain a Nasdaq name is on Global Select, **use WebSearch to verify the tier before writing the ticker**. A quick query like `"<company> nasdaq tier global select market capital"` or checking the company's Capital IQ / investor-relations page usually resolves it. Do not default to `NasdaqGS`.

### Grouping Guidelines

**One dimension, applied consistently.** All three group labels must share the same axis — either all geography or all sector/vertical. Mixing the two (e.g., two sector labels and one regional label) is not allowed.

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
