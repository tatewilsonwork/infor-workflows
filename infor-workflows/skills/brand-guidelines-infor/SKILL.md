---
name: brand-guidelines-infor
description: >
  Use this skill when creating, formatting, or reviewing any PowerPoint presentation that must
  follow INFOR Financial Group brand guidelines. Activates on "brand guidelines", "INFOR formatting",
  "format this deck", "branded presentation", "INFOR style", "make a deck", "pitch book",
  "discussion materials", or any request to create or fix a PowerPoint using INFOR branding.
  Also use when answering questions about INFOR colors, fonts, logo usage, or slide layout standards.
version: 1.9.0
---

# INFOR Brand Guidelines — PowerPoint

This skill defines the visual identity and formatting rules for all INFOR Financial Group PowerPoint presentations. Use it as the authoritative reference when generating or reviewing any deck.

**Always start from the INFOR Deck Template** (see Section 11). The template carries the branded slide master, theme colors, fonts, and example slides for every common layout. Starting from scratch almost always loses master-level formatting (title bars, footers, page numbers, bullet styles, theme font) and produces off-brand output.

Allowed tools: Read, Bash, Write, Glob

---

## Context

- Today's date: !`date +%Y-%m-%d`
- INFOR logo location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Logo - 1.png" 2>/dev/null | head -1`
- INFOR deck template location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Deck Template.pptx" 2>/dev/null | head -1`
- INFOR theme location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFORFG.thmx" 2>/dev/null | head -1`
- Current working directory: !`pwd`

---

## 1 — Slide Dimensions

All INFOR presentations use **10.00 x 7.50 inches** (widescreen 4:3).

In code: `width = Inches(10)`, `height = Inches(7.5)`.

---

## 2 — Color Palette

Every color below is defined in the INFOR PowerPoint theme. Use the hex / RGB values when writing with python-pptx or pptxgenjs.

| Name | Hex | RGB | Theme Role | When to Use |
|------|-----|-----|------------|-------------|
| **Navy Blue** | `#0E213F` | 14, 33, 63 | accent1 | Slide title bar fill; section header boxes; top row of standalone tables (comps, street, etc.) |
| **Mid Blue** | `#46566E` | 70, 86, 110 | accent2 | Top row of tables under a section header; primary color in charts; target company highlight in comps |
| **Light Blue** | `#ADB9CA` | 173, 185, 202 | accent3 | Secondary chart color; subtotals (when light grey is already used) |
| **Gold** | `#A4844B` | 164, 132, 75 | accent4 | Lines in charts (margins, growth rates); tertiary chart color |
| **Dark Grey** | `#767171` | 118, 113, 113 | accent5 | Additional chart color; totals rows at bottom of tables |
| **Light Grey** | `#E5E3E3` | 229, 227, 227 | accent6 | Additional chart color; alternating row shading in tables; subtotals |
| **Black** | `#000000` | 0, 0, 0 | dk1 | Body text; axis lines; chart fonts |
| **White** | `#FFFFFF` | 255, 255, 255 | lt1 | Text inside navy/blue fills; table gridlines |

### Color Priority in Charts

Use colors in this order: Mid Blue, Light Blue, Gold, Dark Grey, Light Grey. **Always use Gold for line series** (margins, growth %).

### Color Rules

- Navy Blue is **only** for solid fills (title bars, section headers, standalone table headers). Never use it for chart data.
- Mid Blue is the default "first color" for all chart bars/areas.
- White text on Navy or Mid Blue fills. Black text everywhere else.

---

## 3 — Typography

**Font family:** Palatino Linotype — used for ALL text in the presentation. No exceptions.

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Slide title (in title bar) | 22 pt | Bold | White text on navy fill |
| Section header (in navy box) | 14 pt | Bold | White text on navy fill |
| Main bullets — full page | 12 pt | Regular | Black text |
| Main bullets — half / quad page | 11 pt | Regular | Black text |
| Sub-bullets — full page | 11 pt | Regular | Black text |
| Sub-bullets — half / quad page | 10 pt | Regular | Black text |
| Footnotes / sources | 7 pt | Regular | Black text, bottom of slide |
| Cover — company name | 30 pt | Bold | White text |
| Cover — subtitle | 24 pt | Regular | White text |
| Cover — date / confidentiality | 18 pt | Regular | Black or dark text |

**Rule of thumb:** when going from full-page to half/quad layout, reduce main bullet size by 1 pt and sub-bullet size by 1 pt.

---

## 4 — Bullet Styles

Three levels of bullets are used:

| Level | Symbol | Description |
|-------|--------|-------------|
| 1 — Main point | Opaque square | Solid filled square bullet |
| 2 — Sub-point | Dash / hyphen | En-dash or hyphen character |
| 3 — Detail | Open circle | Unfilled circle bullet |

Left-justify all text. Align bullets with the leftmost content edge (in-line with the title text).

---

## 5 — Paragraph Spacing

- **Always use equal spacing before and after** — e.g., 6 pt before / 6 pt after, or 3 pt before / 3 pt after.
- Adjust spacing as needed to fill the page or text box. Tighter spacing (3 pt) for dense slides; wider spacing (6 pt) for lighter slides.
- Never use asymmetric spacing (e.g., 6 pt before / 0 pt after).

---

## 6 — Slide Layouts

### 6.1 — Cover Slide

| Element | Position | Size | Details |
|---------|----------|------|---------|
| Title area | left=0.38in, top=1.99in | 9.26 x 0.98in | Company name (30 pt bold) + subtitle line (24 pt regular, e.g., "Confidential Discussion Materials") |
| Client logo | left=0.38in, top=~3.16in | ~3.08 x 0.60in | Client's logo, left-aligned below title |
| INFOR logo | left=7.65in, top=6.21in | 1.99 x 0.47in | Bottom-right corner |
| "Private and Confidential" | left=0.26in, top=6.94in | — | 18 pt Palatino Linotype, bottom-left |
| Date | left=6.69in, top=6.94in | — | 18 pt Palatino Linotype, bottom-right (e.g., "April 2026") |

The cover has a navy blue decorative bar / rounded rectangle behind the title area.

### 6.2 — Content Slides

| Element | Position | Size | Details |
|---------|----------|------|---------|
| Title bar | left=0.26in, top=0.13in | 9.38 x 0.96in | Navy fill (#0E213F), white 22 pt bold Palatino Linotype |
| Section header boxes | left=varies, top=1.13in | width=4.53in, **height=0.34in** | Navy fill (#0E213F), white 14 pt bold Palatino Linotype; stretched to cover its section |
| Content area | left=0.35in, top=~1.47in | ~9.29 x ~5.35in | Main content sits between title bar and footer line |
| Footer line | left=0.37in, top=6.82in | 9.29 x 0in | Thin horizontal separator |
| Sources / footnotes | left=1.72in, top=7.03in | ~7.8 x 0.45in | 7 pt Palatino Linotype |
| Page number | left=8.89in, top=7.06in | 0.83 x 0.40in | Bottom-right |

**Section header boxes:**
- Height is exactly **0.34 inches**.
- Width stretches to cover the section it labels (half-page = ~4.53in, full-page = ~9.29in).
- Fill: Navy Blue (#0E213F). Text: white, 14 pt, bold, Palatino Linotype.
- Position: flush with the content left edge, sitting just above the content area.

**Two-column layouts** (e.g., "Overview" left + "Capitalization" right):
- Left section: left=0.35in, width=4.53in
- Right section: left=5.12in, width=4.53in
- ~0.24in gap between columns

**Four-quadrant layouts:**
- Top-left: (0.35, 1.13) 4.53 x ~2.5in
- Top-right: (5.12, 1.13) 4.53 x ~2.5in
- Bottom-left: (0.35, ~4.06) 4.53 x ~2.5in
- Bottom-right: (5.12, ~4.06) 4.53 x ~2.5in

### 6.3 — Section Divider Slides

Used to separate major sections of the deck:
- Centered group of rounded rectangles listing all sections
- Each rectangle: ~6.30 x 0.42in, centered horizontally (~1.85in from left)
- Current section is highlighted (navy fill, white text); others are lighter
- Page number in footer area

### 6.4 — Logo Placement

| Slide Type | INFOR Logo | Client Logo |
|------------|-----------|-------------|
| Cover | Bottom-right: (7.65in, 6.21in), 1.99 x 0.47in | Below title, left-aligned |
| Content slides | Not shown (in master/footer area) | Top-right area (optional) |

The INFOR logo file is located in the templates directory as `INFOR Logo - 1.png`.

---

## 7 — Tables

| Rule | Detail |
|------|--------|
| Left stripe | Blue stripe on left side of table |
| Gridlines | White lines, 0.75 pt weight |
| Row shading | Light grey (#E5E3E3) on every other column |
| Top border | Black line on top |
| Vertical lines | None — no vertical separating lines |
| Header row (standalone) | Navy Blue (#0E213F) fill, white text |
| Header row (under section header) | Mid Blue (#46566E) fill, white text |
| Totals row | Dark Grey (#767171) |
| Subtotals row | Light Grey (#E5E3E3) or Light Blue (#ADB9CA) |
| Alignment — single value | Middle-aligned vertically |
| Alignment — list of items | Top-aligned vertically |
| Header alignment | Center across selection (do NOT merge and center) |
| Underlines | Single accounting underline (no cell borders) |

---

## 8 — Charts

| Rule | Detail |
|------|--------|
| Color order | Mid Blue first, then Light Blue, Gold, Dark Grey, Light Grey |
| Line color | Always Gold (#A4844B) for line series |
| Sizing (full width) | 23.6 cm wide |
| Sizing (half width) | 11.5 cm wide |
| Chart height | 14.5 cm |
| Gap between charts | 0.6 cm |
| Font | Black, Palatino Linotype |
| Axis line | Black |
| Tick marks | Major, outside |
| Gap width | 50 (default, use judgement) |
| Line weight | 1 pt (use judgement) |
| Axis display | No axis unless necessary (especially for line charts) |
| Data labels | Try to label all axes and data points |
| Format | Always format to size (Macabacus) |

---

## 9 — Number & Text Formats

### Periods

| Format | Example |
|--------|---------|
| Quarter | Q1-24, Q1 CY2024, Q1 FY2024 |
| Calendar year | CY2024 |
| Fiscal year | FY2024 |
| Actual | Q1-24A, FY2024A |
| Estimate | FY2024E |

### Units

| Unit | Usage |
|------|-------|
| C$MM | Default for all figures (millions) |
| C$M | Mining sector only |
| C$B | Billions |
| C$000s | Thousands |

### Footnotes

- No capitals unless a proper title
- Comma-separated, not semicolons
- Standard note: "Note: in C$MM, unless otherwise noted"

---

## 10 — Workflow: Applying Brand Guidelines

When generating or reviewing a PowerPoint:

### Step 1 — Confirm Scope

Determine what is being created or reviewed:
- New deck from scratch → **open the INFOR Deck Template** (Section 11)
- Formatting check on an existing deck → open the existing file; do not rebuild it from the template unless asked
- Specific slide type (cover, content, charts, tables) → clone the matching template slide as a starting point

### Step 2 — Locate Assets

The INFOR logo, deck template, and theme paths are shown in the Context section above. If any is blank, search for it:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Logo - 1.png" 2>/dev/null | head -1
# Repeat with "INFOR Deck Template.pptx" and "INFORFG.thmx"
```

### Step 3 — Build from Template

For any new deck, follow Section 11 — open the template, clone the sample slides that match the content you need, then edit the clones. This is the default path.

**Required slide order** (see Section 11.6):
1. Cover (clone sample #1) — leave INFOR logo untouched
2. Executive Summary (clone #2) — full-page text OK
3. Content slide(s) — must include graphical elements; preserve placeholder rectangles and grouped graphics
4. Disclaimer (clone #8) — full-page text OK
5. Contact page (clone #9) — always last; Neil + 3 `[x]` placeholders by default

Only the Executive Summary and Disclaimer may be text-only. Every other slide needs at least one graphic, table, chart, placeholder rectangle, or grouped infographic.

### Step 4 — Apply Standards

Enforce every rule in sections 2 through 9 above. Most of these are pre-applied by the template master, but verify on every slide you add or modify:

- [ ] All text is Palatino Linotype
- [ ] Correct font sizes per element type (title 22, header 14, bullets 11-12, sub-bullets 10-11, footnotes 7)
- [ ] Navy (#0E213F) used only for title bars and section header fills
- [ ] Section header boxes are exactly 0.34in tall
- [ ] INFOR logo in bottom-left (cover) / correct position
- [ ] Client logo in top-right (content slides) if applicable
- [ ] Page numbers bottom-right
- [ ] Sources/footnotes at 7 pt, bottom of slide
- [ ] Bullet styles: square, dash, open circle (levels 1/2/3)
- [ ] Equal paragraph spacing before and after
- [ ] Charts follow color order: Mid Blue, Light Blue, Gold, Dark Grey, Light Grey
- [ ] Gold for all chart line series
- [ ] Tables: white gridlines (0.75pt), alternating light grey, no vertical lines
- [ ] Number formats: C$MM default, correct period notation

### Step 5 — Summary

Report what was created or fixed, listing any deviations from the guidelines that could not be resolved and why.

---

## 11 — Starting from the INFOR Deck Template

**Default workflow for every new deck.** The template file (`INFOR Deck Template.pptx`) ships with the branded slide master, theme (`INFORFG.thmx`), Palatino Linotype theme font, accent colors, footer/page-number placeholders, and nine sample slides covering every common layout. Opening the template with `python-pptx` inherits all of this automatically. Building the same slides from a blank `Presentation()` almost always produces off-brand output because master-level settings are lost.

### 11.1 — Sample Slides in the Template

Reference these when deciding which slide to clone as a starting point:

| # | Layout | Purpose | Use When |
|---|--------|---------|----------|
| 1 | Title Slide | Cover slide with `[CLIENT NAME]`, "Internal Discussion Materials", INFOR logo, date, "Private and Confidential" | First slide of every deck |
| 2 | Main | Executive summary — full-page paragraph under the title bar | Any full-page text/bullet slide |
| 3 | Main | Two-column layout: Overview + Capitalization Summary (top), LTM Revenue Breakdown + pie chart (bottom) | Company introduction, split overview/financials |
| 4 | Main | Earnings summary — Business Updates, financial highlights comparison blocks, BBG Comparison, Management Guidance | Quarterly/earnings review, KPI comparison |
| 5 | Main | Section divider — stack of rounded rectangles listing all sections | Between major deck sections |
| 6 | With Tagline | 2×2 matrix (Gartner Magic Quadrant style) with axes, quadrant labels, Honourable Mentions sidebar | Competitive positioning, market maps |
| 7 | Main | Full-page table | Comps tables, data tables |
| 8 | Main | Disclaimer — full-page legal text | End of every external deck |
| 9 | Main | Contact page — tables for bankers with a photo placeholder | Back cover / team page |

### 11.2 — Recommended Approach: Clone-and-Edit

Open the template, **clone the sample slide whose layout matches your content**, then edit the clone's text and shapes. This preserves every master-level detail — title bar, footer line, page number placeholder, section-header proportions, table styles, bullet indentation — that you cannot cleanly reproduce from code.

```python
import copy
from pptx import Presentation
from pptx.oxml.ns import qn

TEMPLATE = r"<path from Context 'INFOR deck template location'>"

prs = Presentation(TEMPLATE)

def clone_slide(prs, source_slide):
    """Duplicate a slide, preserving shapes, layout, AND all relationships (images, charts, hyperlinks).

    Copying only the shape XML is not enough — shapes that reference relationships (pictures,
    charts, hyperlinks) carry r:embed / r:link / r:id attributes whose rIds point into the
    source slide's rels file. Without copying the rels and remapping rIds, those references
    dangle in the new slide and PowerPoint shows a red X with "The picture can't be displayed."
    """
    new_slide = prs.slides.add_slide(source_slide.slide_layout)
    # Remove placeholders that the layout auto-adds
    for shp in list(new_slide.shapes):
        new_slide.shapes._spTree.remove(shp._element)

    # Copy every non-notes relationship from the source slide and build an old→new rId map
    rid_map = {}
    for rel in source_slide.part.rels.values():
        if "notesSlide" in rel.reltype:
            continue
        if rel.is_external:
            new_rid = new_slide.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        else:
            new_rid = new_slide.part.relate_to(rel.target_part, rel.reltype)
        rid_map[rel.rId] = new_rid

    # Deep-copy shape XML and rewrite r:embed / r:link / r:id attributes so they point at the new rIds
    RID_ATTRS = (qn('r:embed'), qn('r:link'), qn('r:id'))
    for shp in source_slide.shapes:
        new_el = copy.deepcopy(shp._element)
        for el in new_el.iter():
            for attr in RID_ATTRS:
                if attr in el.attrib and el.attrib[attr] in rid_map:
                    el.attrib[attr] = rid_map[el.attrib[attr]]
        new_slide.shapes._spTree.append(new_el)
    return new_slide

def delete_slide(prs, index):
    """Remove a slide by index."""
    xml_slides = prs.slides._sldIdLst
    slides = list(xml_slides)
    xml_slides.remove(slides[index])

# Example: build a standard deck — cover, exec summary, content, disclaimer, contact
# Clone first, then delete the sample slides at the end.
cover        = clone_slide(prs, prs.slides[0])  # slide 1: Title Slide
exec_summary = clone_slide(prs, prs.slides[1])  # slide 2: Executive Summary
earnings     = clone_slide(prs, prs.slides[3])  # slide 4: Earnings / content w/ graphics
disclaimer   = clone_slide(prs, prs.slides[7])  # slide 8: Disclaimer
contact      = clone_slide(prs, prs.slides[8])  # slide 9: Contact page (ALWAYS INCLUDE)

# Now edit text in each cloned slide (see 11.4), then delete the 9 originals.
for _ in range(9):
    delete_slide(prs, 0)

prs.save("output.pptx")
```

### 11.3 — Alternative: Build from Template Layouts

If no sample slide matches, call `add_slide` with one of the template's named layouts. You still inherit the master (theme font, colors, footer, page number) but you must add content shapes yourself — follow the positions in Section 6.

```python
prs = Presentation(TEMPLATE)

# Available layouts (from the template's slide masters):
#   "Title Slide"    — cover
#   "2_Main"         — content slide with title placeholder
#   "Main"           — content slide with title + footer + page number
#   "With Tagline"   — content slide with tagline band under title

layout = next(l for m in prs.slide_masters for l in m.slide_layouts if l.name == "Main")
slide = prs.slides.add_slide(layout)
# ... add shapes per Section 6 positions ...
```

### 11.4 — Editing Cloned Slide Content

After cloning, locate shapes by their `name` or by their text placeholders. The template uses conventional names: `Title 1`, `Rectangle 14` (section header), `Text Placeholder 1` (footnote/source), `Slide Number Placeholder` (page number). Common placeholder tokens in sample text are `[CLIENT NAME]`, `[Client Name]`, `[x]`, `[QX 202X]`, `[Cap Table Placeholder]` — replace these in place, preserving run-level formatting.

```python
def replace_text(shape, new_text):
    """Replace shape text while preserving the first run's font/color/size."""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if p0.runs:
        p0.runs[0].text = new_text
        for r in p0.runs[1:]:
            r.text = ""
    else:
        p0.text = new_text
    for para in tf.paragraphs[1:]:
        para.clear()

for shape in cover.shapes:
    if shape.name == "Title 1":
        # "[CLIENT NAME]\nInternal Discussion Materials" — edit the runs individually
        ...
```

### 11.5 — Rules When Using the Template

- **Never** call `Presentation()` with no arguments for an INFOR deck. Always pass the template path.
- **Do not** modify the slide master or theme from code — the master is the source of truth for every master-level rule in Sections 2, 3, 4, 5.
- **Do** keep the Disclaimer slide (sample #8) for every external deck.
- **Do** clone the cover slide (sample #1) rather than building a cover from scratch — the navy decorative bar behind the title is an XML construct that is painful to recreate.
- **Do not** delete the template's sample slides until after you've cloned everything you need — deleting them first removes the source shapes you wanted to copy.
- **Always** use `clone_slide` exactly as shown in 11.2. The naive `deepcopy`-only version drops image/chart/hyperlink relationships and produces red-X picture placeholders in PowerPoint.
- **Do not** touch the INFOR logo on the cover (shape `Picture 1` at (7.65, 6.21)). The template embeds it correctly — leave it alone. Only edit the `Title 1`, `Subtitle 2` text, and date.
- **Do not** replace placeholder rectangles (`[Cap Table Placeholder]`, `[BBG Comparison Placeholder]`, `[Pie Chart Placeholder]`). These are intentional sizing stubs for the analyst to paste an Excel table, chart, or image into manually. Leave the rectangle and its placeholder text unchanged — resize or reposition only if the user asks.
- **Do not** flatten grouped graphics (`Group 1070`, `Group 1086`, quote-paper groups, etc.) into plain text boxes. Edit the text **inside** the group's child shape — keep the group wrapper, the paper/callout graphic, and all decorative elements.
- If the user supplies their own base deck, open that file instead of the template and apply only the edits requested. Do not rebuild from the template unless the user asks.

### 11.6 — Slide-Specific Conventions

These rules come from analyst review of generated decks. They override any generic inference:

**Required deck structure.** Every deck must include, in order:
1. Cover (clone sample #1)
2. Executive Summary (clone sample #2)
3. Content slides — one or more, using samples #3, #4, #6, or #7
4. Disclaimer (clone sample #8) — second-to-last
5. Contact page (clone sample #9) — **always the final slide**

**Text-only slides are restricted to exactly two:** the Executive Summary (#2) and the Disclaimer (#8). Every other content slide must include at least one graphical element — a table, chart, placeholder rectangle for manual insertion, grouped infographic, metric callout blocks, or quote-paper group. If the content you want to present is inherently prose (e.g., "Recent Business Developments"), restructure it into a visual format: a two-column layout with section headers (clone #3), a timeline, bullet callouts, or a combination of placeholder boxes and short commentary.

**Cover slide (#1).** Edit only: company name, subtitle ("Internal Discussion Materials" or "Confidential Discussion Materials"), date, and (optionally) the "Private and Confidential" text. Do not move or modify `Picture 1` (INFOR logo).

**Earnings slide (#4) — specific rules.**
- **Business Updates box** (top-left, `Rectangle 5` section header + adjacent text): write 2–3 short paragraphs of **professional investment-banking commentary**, not bullet-pointed metrics. Tone: observational, analytical, forward-looking. Example opener: *"Company continues to execute on its long-term strategic plan, with Q1 results reflecting momentum across core verticals..."* Metrics belong in the financial-highlights comparison blocks on the right, not here.
- **Financial highlights blocks** (top-right): keep the template's structure intact — prior-period callout, current-period callout, delta rectangle with up/down triangle, and the horizontal connector line between rows. Edit only the numbers and metric labels (Revenue, EBITDA, Gross Margin, EPS, etc.).
- **Bottom-left placeholder** (`Rectangle 2` at (0.35, 4.55), labelled `[BBG Comparison Placeholder]` or similar): **leave the placeholder rectangle in place**. Do not replace it with metrics, text, or a backlog/KPI block. The analyst pastes the Excel/BBG table in manually after generation.
- **Bottom-right quote-paper groups** (`Group 1070` at (5.14, 4.55) and `Group 1086` at (5.08, 5.72)): these are two decorative "paper" graphics holding management/analyst quotes. **Always include two quotes** (e.g., CEO + CFO, or CEO + analyst). Edit the text *inside* each group — never replace the groups with a plain `TextBox`, which deletes the paper graphic.

**Contact page (#9) — default content.** Unless the user specifies otherwise, the contact page shows **Neil Selfe** (Chief Executive Officer) with three `[x]` placeholders for additional team members to be filled in manually. Edit the first table/photo block with Neil's details; leave the other three blocks as `[x]` placeholders so the analyst can populate them.

---

## Quick Reference Card

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

SLIDE SIZE: 10.00 x 7.50 inches

SECTION HEADER BOX: 0.34in tall, navy fill, full section width

BULLETS: Square > Dash > Open Circle

CHARTS: Mid Blue > Light Blue > Gold > Dark Grey > Light Grey
         Gold for lines. Black font/axis. 1pt lines.

UNITS: C$MM (default), C$M (mining), C$B, C$000s
```
