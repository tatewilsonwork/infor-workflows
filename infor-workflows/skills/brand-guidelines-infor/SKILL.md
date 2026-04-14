---
name: brand-guidelines-infor
description: Use this skill when creating, formatting, or reviewing any PowerPoint presentation that must follow INFOR Financial Group brand guidelines. Activates on "brand guidelines", "INFOR formatting", "format this deck", "branded presentation", "INFOR style", "make a deck", "pitch book", "discussion materials", or any request to create or fix a PowerPoint using INFOR branding. Also use when answering questions about INFOR colors, fonts, logo usage, or slide layout standards.
version: 1.0.0
---

# INFOR Brand Guidelines — PowerPoint

This skill defines the visual identity and formatting rules for all INFOR Financial Group PowerPoint presentations. Use it as the authoritative reference when generating or reviewing any deck.

Allowed tools: Read, Bash, Write, Glob

---

## Context

- Today's date: !`date +%Y-%m-%d`
- INFOR logo location: !`REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Logo - 1.png" 2>/dev/null | head -1`
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
- New deck from scratch
- Formatting check on an existing deck
- Specific slide type (cover, content, charts, tables)

### Step 2 — Locate Logo

The INFOR logo path is shown in the Context section above. If blank, search for it:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
find "${REPO_ROOT:+$REPO_ROOT/templates}" "${REPO_ROOT:+$REPO_ROOT/infor-workflows/templates}" "$HOME/.claude/plugins/infor-workflows/templates" "$HOME/AppData/Roaming/Claude/plugins/infor-workflows/templates" "$HOME" -name "INFOR Logo - 1.png" 2>/dev/null | head -1
```

### Step 3 — Apply Standards

When generating slides, enforce every rule in sections 2 through 9 above. Key checkpoints:

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

### Step 4 — Summary

Report what was created or fixed, listing any deviations from the guidelines that could not be resolved and why.

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
