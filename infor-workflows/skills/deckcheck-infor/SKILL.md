---
name: deckcheck-infor
description: >
  Reviews an attached PowerPoint for grammar, spelling, tone, INFOR brand formatting (fonts,
  colors, alignment, sizing), and factual accuracy (HQ locations, company descriptions, event
  dates) via web search. Produces a tiered review (Tier I / II / III) with Confidence and Impact
  scored 1–10 per suggestion, delivered as a Word (.docx) document. Activates on /deckcheck-infor,
  "deck check", "review this deck", "proofread deck", "QC deck", or "deck review".
version: 2.10.0
allowed-tools: [Read, Bash, Write, Glob, WebSearch, Agent]
---

# INFOR Deck Check — Workflow

This skill reviews an attached PowerPoint presentation for three categories of issues: (1) language quality — grammar, spelling, and tone; (2) formatting compliance — alignment, fonts, sizes, colors, and layout against INFOR brand standards; and (3) factual accuracy — verifiable claims like headquarters locations, company descriptions, dates of events, and other publicly available facts.

The output is a cleanly formatted Microsoft Word (.docx) document organized into three tiers, with specific, actionable suggestions scored on Confidence and Impact.

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. Working directory is resolved inline where needed.

---

## Workflow Steps

### Step 1 — Locate the Deck

If the user has attached a `.pptx` file, use that. If no file is attached, ask:

> "Please attach the PowerPoint file you'd like me to review."

Wait for the file before proceeding.

---

### Step 2 — Extract All Slide Content

Use python-pptx to extract the full contents of every slide. For each slide, capture:

- **Slide title** (from the title placeholder or first text box)
- **Visible slide number** — the page number printed in the bottom-right corner of the slide (typically a small text box near left≥8.5in, top≥7.0in containing just a numeral, e.g. "1", "2", "3"). This is the number the skill must use when referring to slides in the output.
  - The **title/cover slide** is expected to have no visible page number — do not flag it and refer to it as "Cover" in the output.
  - For every **non-title slide**, if no visible page number is found in the bottom-right, emit a **Formatting** suggestion: *"Slide is missing a page number in the bottom-right corner."* Use the slide's positional index (e.g. "Slide at position N") to identify it in that one case only, and give it Confidence 9 / Impact 6.
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

The authoritative source for every brand rule is [`brand-guidelines-infor/SKILL.md`](../brand-guidelines-infor/SKILL.md) — load it before this step. Audit every slide against those rules and flag any deviation. The key categories to check:

| Category | Where defined in `brand-guidelines-infor` | What to flag |
|---|---|---|
| Fonts | Section 3 — Typography (sizes per element type) | Non-Palatino fonts; wrong size for title / header / bullets / footnotes / cover |
| Colors | Section 2 — Color Palette | Colors outside the INFOR palette; Navy used outside title bars / section headers / standalone table headers; white text on non-navy/non-mid-blue fills |
| Layout & alignment | Sections 1 (slide dimensions) and 6 (layouts — title bar, section header, content area, footer, page numbers) | Slide not 10.00×7.50in; section header boxes not exactly 0.34in tall; missing page numbers in bottom-right; shapes off-grid by >0.05in; overlapping or off-slide shapes |
| Bullets & spacing | Sections 4 (bullet hierarchy: square / dash / open circle) and 5 (symmetric paragraph spacing) | Wrong glyph at each level; asymmetric before / after spacing |
| Tables | Section 7 | Missing white gridlines (0.75pt); no alternating light-grey shading; vertical separator lines present; wrong header fill (Navy when standalone, Mid Blue when under section header) |
| Charts | Section 8 | Wrong color order (must be Mid Blue → Light Blue → Gold → Dark Grey → Light Grey); line series not Gold; non-Palatino/non-black axis/labels |

For specific hex values, font-size tables, layout positions, and chart conventions, read [`brand-guidelines-infor/SKILL.md`](../brand-guidelines-infor/SKILL.md) directly — keep this file in sync with that one as the source of truth.

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

### Step 6 — Score Every Suggestion

For every issue identified in Steps 3, 4, and 5, assign two scores from **1 to 10**:

#### Confidence (1–10) — how sure you are that this is actually a mistake

| Score | Meaning |
|-------|---------|
| 9–10 | Certain — objectively wrong (misspelling, font is measurably non-Palatino, HQ city is verifiably incorrect, a number contradicts another number on the same slide) |
| 7–8 | High confidence — strong indication of an error but minor ambiguity (grammar call that depends on style, color that is close to but not exactly the brand hex) |
| 5–6 | Moderate — plausible issue but could be intentional (tone shift, unusual phrasing, a date that couldn't be fully verified online) |
| 3–4 | Low — a hunch worth flagging but easily defensible |
| 1–2 | Speculative — stylistic preference only |

#### Impact (1–10) — how much the mistake affects the reader / client perception

| Score | Meaning |
|-------|---------|
| 9–10 | Severe — factual error that undermines credibility (wrong HQ, wrong deal date, misspelled client name, wrong company description on cover) |
| 7–8 | High — visible error in prominent location (spelling error in a title, wrong font on every slide, brand color off) |
| 5–6 | Medium — noticeable but not prominent (grammar in body text, minor alignment off in a non-focal shape, color off on one chart series) |
| 3–4 | Low — small polish issue (sub-pixel alignment, 7pt footnote tweak, inconsistent comma usage) |
| 1–2 | Trivial — only noticed on close inspection |

#### Edit Categories

Bucket every suggestion into **one** of these categories:

- **Grammar & Spelling** — misspellings, typos, punctuation, subject-verb agreement
- **Formatting** — font, font size, color, bold/italic, alignment, shape position, spacing, bullet style
- **Accuracy** — a claim that is factually incorrect (HQ, date, description, executive name, etc.)
- **Inconsistency** — same thing stated differently across slides, numbers that don't reconcile, capitalization drift, tense shift
- **Tone & Style** — wording that is overly casual, inconsistent voice, or unclear phrasing
- **Unverified** — factual claim that could not be confirmed via web search (flag for analyst to double-check)

---

### Step 7 — Tier the Suggestions

Combine Confidence and Impact into a **Priority Score = Confidence + Impact** (range 2–20). Assign each suggestion to one of three tiers:

| Tier | Priority Score | Meaning |
|------|----------------|---------|
| **Tier I** | 15–20 | Fix before sending — high confidence AND high impact |
| **Tier II** | 10–14 | Strong recommendation — either very confident OR high impact (not both) |
| **Tier III** | 2–9 | Optional polish — low confidence or low impact |

**Override rules:**
- Any **Accuracy** issue with Confidence ≥ 8 is always **Tier I** regardless of impact score
- Any **Grammar & Spelling** issue with Confidence ≥ 9 is always at least **Tier II**
- Suggestions with Confidence ≤ 3 AND Impact ≤ 3 should be dropped entirely, not reported

---

### Step 8 — Output the Review as a Microsoft Word Document

Produce the review as a **Microsoft Word (.docx) file** using `python-docx`. **Only three sections — Tier I, Tier II, Tier III.** Do not group by slide or category in the top-level structure; tier comes first.

Within each tier, sort suggestions by Priority Score descending (highest first).

**File naming & location:**
- Save to the current working directory (`./`)
- Filename: `DeckReview_<OriginalDeckStem>_<YYYY-MM-DD>.docx` — strip the `.pptx` extension, keep the stem, append today's date
- If a file with that name already exists, append `_v2`, `_v3`, etc.

**Document structure (in this order):**

1. **Title** — "Deck Review: [Deck Filename]" (Heading 1)
2. **Metadata line** — "Reviewed: [Today's Date]" (italic, below the title)
3. **Executive Summary** (Heading 2) — 2–3 sentences: total suggestions across tiers, the most critical issue, overall quality read
4. **Tier I — Fix Before Sending** (Heading 2)
5. **Tier II — Strong Recommendation** (Heading 2)
6. **Tier III — Optional Polish** (Heading 2)
7. **Summary** (Heading 2) — table + category breakdown line

**Within each tier**, render every suggestion as a numbered block:

- Heading 3 line: `N. [Slide X] — [One-line description of what needs to change]`
  - `X` is the **visible page number** printed on the slide (from the bottom-right corner), not the positional index in the file. The cover slide is labelled `[Cover]`. For a non-title slide missing its page number, use `[Slide at position N]` where N is the positional index.
- Bulleted bold label lines under that heading:
  - **Change:** [Specifically what to fix — quoted original text or element, followed by the corrected version. For Accuracy, include the source URL.]
  - **Category:** [Grammar & Spelling / Formatting / Accuracy / Inconsistency / Tone & Style / Unverified]
  - **Confidence / Impact:** X/10 & Y/10

If a tier has no suggestions, write *"No suggestions in this tier."* in italic.

**Summary section** — render as a proper Word table with two columns (Tier, Count) and rows for Tier I, Tier II, Tier III, Total. Below the table, one line listing category counts: `Grammar & Spelling (n) · Formatting (n) · Accuracy (n) · Inconsistency (n) · Tone & Style (n) · Unverified (n)`.

**Styling:**
- Default font: Calibri 11 pt
- Headings: Word's built-in Heading 1 / 2 / 3 styles
- Summary table: use the "Light Grid Accent 1" or equivalent built-in table style for clean gridlines
- Page margins: 1 inch on all sides (Word default is fine)

**Implementation:**

Write a single Python script via Bash using `python-docx`. Example pattern:

```python
from docx import Document
from docx.shared import Pt, Inches
from pathlib import Path

doc = Document()
doc.add_heading(f"Deck Review: {deck_filename}", level=1)
meta = doc.add_paragraph()
meta.add_run(f"Reviewed: {today}").italic = True

doc.add_heading("Executive Summary", level=2)
doc.add_paragraph(exec_summary_text)

for tier_label, suggestions in [("Tier I — Fix Before Sending", tier1),
                                 ("Tier II — Strong Recommendation", tier2),
                                 ("Tier III — Optional Polish", tier3)]:
    doc.add_heading(tier_label, level=2)
    if not suggestions:
        p = doc.add_paragraph()
        p.add_run("No suggestions in this tier.").italic = True
        continue
    for i, s in enumerate(suggestions, 1):
        doc.add_heading(f"{i}. [{s['slide_label']}] — {s['headline']}", level=3)
        for label, value in [("Change", s["change"]),
                             ("Category", s["category"]),
                             ("Confidence / Impact", f"{s['confidence']}/10 & {s['impact']}/10")]:
            p = doc.add_paragraph(style="List Bullet")
            run = p.add_run(f"{label}: ")
            run.bold = True
            p.add_run(value)

doc.add_heading("Summary", level=2)
table = doc.add_table(rows=5, cols=2)
table.style = "Light Grid Accent 1"
# ...populate tier counts + total row
doc.add_paragraph(category_breakdown_line)

out_path = Path(f"./DeckReview_{stem}_{today}.docx")
doc.save(out_path)
```

**After saving, tell the user:**
- The absolute path to the saved .docx
- Total suggestions and tier counts
- The single most critical item (top Tier I entry)

Do not paste the full review content into the chat response — the Word document is the deliverable.

---

## INFOR Brand Reference

For colors, fonts, layout positions, table and chart conventions, see [`brand-guidelines-infor/SKILL.md`](../brand-guidelines-infor/SKILL.md) — the Quick Reference Card at the bottom of that file is a one-page cheat sheet. This skill audits decks against those rules; keeping the rules in one place avoids drift between the audit and the source of truth.
