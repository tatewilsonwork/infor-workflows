---
name: deckcheck-infor
description: Use this skill when the user invokes /deckcheck-infor or asks to review, proofread, or QC a PowerPoint deck. Checks grammar, spelling, tone, INFOR brand formatting (fonts, colors, alignment, sizing), and verifies factual claims (HQ locations, company descriptions, event dates) via web search. Activates on "deck check", "review this deck", "proofread deck", "QC deck", "check my deck", "deck review", or any request to review a PowerPoint for errors.
version: 1.0.0
---

# INFOR Deck Check — Workflow

This skill reviews an attached PowerPoint presentation for three categories of issues: (1) language quality — grammar, spelling, and tone; (2) formatting compliance — alignment, fonts, sizes, colors, and layout against INFOR brand standards; and (3) factual accuracy — verifiable claims like headquarters locations, company descriptions, dates of events, and other publicly available facts.

The output is a cleanly formatted review organized by category and slide, with specific, actionable suggestions.

Allowed tools: Read, Bash, Write, Glob, WebSearch, Agent

---

## Context

- Today's date: !`date +%Y-%m-%d`
- Current working directory: !`pwd`

---

## Workflow Steps

### Step 1 — Locate the Deck

If the user has attached a `.pptx` file, use that. If no file is attached, ask:

> "Please attach the PowerPoint file you'd like me to review."

Wait for the file before proceeding.

---

### Step 2 — Extract All Slide Content

Use python-pptx to extract the full contents of every slide. For each slide, capture:

- **Slide number and title** (from the title placeholder or first text box)
- **All text content** from every shape (text boxes, tables, grouped shapes, chart titles, notes)
- **Shape metadata** for formatting audit:
  - Font name, font size, bold/italic, font color (hex)
  - Shape position (left, top) and size (width, height) in inches
  - Text alignment (left, center, right)
  - Fill colors on shapes and table cells (hex)
  - Bullet characters and indentation levels
  - Paragraph spacing (space before, space after)
- **Table structure** — header row fill colors, gridline colors, row shading pattern
- **Chart details** — series colors, chart type, axis formatting
- **Image positions and sizes**

Write a single Python script using Bash that extracts all of the above and prints it as structured output. Store the extraction results for use in subsequent steps.

---

### Step 3 — Language Review (Grammar, Spelling, Tone)

Review all extracted text for:

**Grammar & Spelling**
- Misspelled words
- Subject-verb agreement errors
- Incorrect punctuation (misplaced commas, missing periods, inconsistent use of serial commas)
- Sentence fragments that are unintentional (note: bullet points are expected to be fragments)
- Duplicate words ("the the", "and and")
- Wrong word usage (e.g., "affect" vs. "effect", "its" vs. "it's", "principal" vs. "principle")

**Tone & Style**
- Inconsistent tense across slides (e.g., mixing past and present when describing the same topic)
- Overly casual language for a professional M&A / financial advisory context
- Inconsistent capitalization conventions (title case vs. sentence case within the same slide)
- Abbreviations used before being defined
- Inconsistent number formatting in body text (e.g., mixing "$5 million" and "$5MM" in prose)

**Do NOT flag:**
- Intentional bullet-point fragments
- Industry-standard abbreviations (EBITDA, LTM, NTM, AUM, TEV, etc.)
- CapIQ formulas or placeholder text (e.g., "CIQ()", "#N/A")

---

### Step 4 — Formatting Review (INFOR Brand Compliance)

Check every slide against the INFOR brand guidelines below. Flag any deviation.

#### 4a — Fonts
- **All text** must be Palatino Linotype — flag any other font
- Check font sizes against expected values:
  - Slide titles: 22 pt bold, white
  - Section headers (navy boxes): 14 pt bold, white
  - Main bullets: 12 pt (full page) / 11 pt (half/quad)
  - Sub-bullets: 11 pt (full page) / 10 pt (half/quad)
  - Footnotes/sources: 7 pt
  - Cover company name: 30 pt bold
  - Cover subtitle: 24 pt regular

#### 4b — Colors
- Navy Blue (#0E213F) — only for title bar fills, section header box fills, standalone table header fills
- Mid Blue (#46566E) — table headers under section headers, primary chart color
- Light Blue (#ADB9CA) — secondary chart color, subtotals
- Gold (#A4844B) — chart lines (mandatory for all line series)
- Dark Grey (#767171) — additional chart color, totals rows
- Light Grey (#E5E3E3) — alternating row shading, subtotals
- White text on Navy or Mid Blue fills; black text everywhere else
- Flag any colors outside the INFOR palette

#### 4c — Layout & Alignment
- Slide dimensions: 10.00 x 7.50 inches
- Title bar: left=0.26in, top=0.13in, 9.38 x 0.96in
- Section header boxes: height exactly 0.34in, navy fill
- Content area starts at ~1.47in from top
- Footer line at ~6.82in from top
- Page numbers bottom-right
- Sources/footnotes at 7 pt, bottom of slide
- Shapes that appear intended to be aligned but are offset by more than 0.05in
- Text boxes or shapes that overlap unintentionally
- Shapes that extend beyond the slide boundary

#### 4d — Bullets & Spacing
- Level 1: solid square; Level 2: dash/hyphen; Level 3: open circle
- Paragraph spacing must be symmetric (equal before and after)

#### 4e — Tables
- White gridlines (0.75 pt)
- Alternating light grey row shading
- No vertical separator lines
- Header row: Navy (standalone) or Mid Blue (under section header)

#### 4f — Charts
- Color order: Mid Blue, Light Blue, Gold, Dark Grey, Light Grey
- Line series must use Gold
- Font: Palatino Linotype, black

---

### Step 5 — Factual Verification (Web Search)

Scan all extracted text for verifiable factual claims. Use WebSearch to check:

**Always verify:**
- Company headquarters locations (city, state/province, country)
- Company founding years
- Company descriptions (what the company does — confirm against their website or profile)
- Dates of announced transactions, events, or milestones
- Names and titles of executives mentioned
- Industry rankings or market position claims (e.g., "#1 provider of...")
- Number of employees (order of magnitude)
- Number of offices or locations

**Do NOT verify:**
- Financial figures (revenue, EBITDA, multiples, valuations) — these come from CapIQ and are assumed correct
- Forward-looking estimates or projections
- CapIQ formulas or placeholder data
- Internal INFOR process descriptions

For each fact checked, record whether it was confirmed, could not be verified, or appears incorrect. Include the source URL for any corrections.

---

### Step 6 — Compile and Output the Review

Produce a cleanly formatted review as a markdown response. Organize as follows:

---

**Structure:**

```
## Deck Review: [Deck Filename]
Reviewed: [Today's Date]

### Executive Summary
[2-3 sentence overview: total issues found by category, overall quality assessment]

---

### 1. Language Issues
[Group by slide. For each issue:]

**Slide [N] — "[Slide Title]"**
- **[Issue Type]:** "[quoted text]" → [suggestion]

---

### 2. Formatting Issues
[Group by issue type, then by slide]

**Fonts**
- Slide [N]: [shape name] uses [wrong font] instead of Palatino Linotype
- Slide [N]: [element] is [X] pt, expected [Y] pt

**Colors**
- Slide [N]: [element] uses [#hex] — expected [#correct hex] ([color name])

**Alignment & Layout**
- Slide [N]: [shape] is offset by [X]in from expected position
- Slide [N]: [shapes A and B] appear misaligned (top edge differs by [X]in)

**Tables**
- Slide [N]: [specific table issue]

**Charts**
- Slide [N]: [specific chart issue]

---

### 3. Factual Verification
[For each fact checked:]

**Slide [N] — "[Slide Title]"**
- **[Claim]:** [Confirmed / Could not verify / Incorrect]
  - [If incorrect: "Found: [correct info] (Source: [URL])"]
  - [If unverified: "Could not find a reliable source to confirm this"]

---

### Summary Table

| Category | Issues Found |
|----------|-------------|
| Grammar & Spelling | [count] |
| Tone & Style | [count] |
| Font Issues | [count] |
| Color Issues | [count] |
| Alignment & Layout | [count] |
| Table / Chart Issues | [count] |
| Factual Corrections | [count] |
| Unverified Facts | [count] |
| **Total** | **[count]** |
```

---

### Severity Guidance

When reporting issues, prioritize by impact:

1. **Factual errors** — wrong HQ, wrong dates, incorrect descriptions (high impact — these undermine credibility)
2. **Spelling / grammar errors** — visible to the reader, embarrassing in a client-facing document
3. **Font violations** — non-Palatino fonts are immediately noticeable
4. **Color / branding violations** — wrong palette colors break visual consistency
5. **Alignment issues** — only flag if visually noticeable (>0.05in offset); minor sub-pixel differences are not worth reporting
6. **Tone / style** — flag only clear inconsistencies, not subjective preferences

---

## INFOR Brand Quick Reference

```
COLORS
  Navy:       #0E213F  (title bars, section headers, standalone table headers)
  Mid Blue:   #46566E  (tables under headers, primary chart, target highlight)
  Light Blue: #ADB9CA  (secondary chart, subtotals)
  Gold:       #A4844B  (chart lines, tertiary chart)
  Dark Grey:  #767171  (chart extra, totals rows)
  Light Grey: #E5E3E3  (chart extra, alternating rows, subtotals)

FONTS — Palatino Linotype everywhere
  Title:       22pt bold (white on navy)
  Header:      14pt bold (white on navy)
  Bullets:     12pt full / 11pt half
  Sub-bullets: 11pt full / 10pt half
  Footnotes:   7pt
  Cover name:  30pt bold
  Cover sub:   24pt regular

SLIDE SIZE: 10.00 x 7.50 inches

SECTION HEADER BOX: 0.34in tall, navy fill, full section width

BULLETS: Square > Dash > Open Circle

SPACING: Always symmetric (equal before and after)

TABLES: White gridlines (0.75pt), alternating light grey, no vertical lines
  Standalone header: Navy
  Under section header: Mid Blue

CHARTS: Mid Blue > Light Blue > Gold > Dark Grey > Light Grey
         Gold for lines. Black font/axis.
```
