---
name: brand-guidelines-infor
description: >
  Visual formatting of INFOR Financial Group PowerPoint decks — colors, fonts, layouts, tables,
  charts, logo placement, slide dimensions, template structure. Activates on /brand-guidelines-infor,
  "brand guidelines", "INFOR formatting", "format this deck", "branded presentation", "INFOR style",
  "make a deck", "pitch book", "discussion materials". For the words on the slide (voice, bullets,
  titles, number / period notation), use `infor-deck-writing` instead — this skill governs visuals only.
version: 2.9.0
allowed-tools: [Read, Bash, Write, Glob]
---

# INFOR Brand Guidelines — PowerPoint

This skill defines the visual identity and formatting rules for all INFOR Financial Group PowerPoint presentations. Use it as the authoritative reference when generating or reviewing the look of a deck.

## Scope — Visual vs. Voice

This skill governs **visual formatting only** — slide dimensions, colors, fonts, layouts, bullet styles, tables, charts, logo placement, and template structure.

**Writing the words on a slide is handled by [`infor-deck-writing`](../infor-deck-writing/SKILL.md).** Whenever you draft, edit, or rewrite any text that will appear on a slide — titles, bullets, headlines, paragraphs, footnotes, callout copy, KPI captions, quotes, source lines — load and follow `infor-deck-writing` (which routes to the right recipe file under [`references/`](../infor-deck-writing/references/) per deliverable type).

`infor-deck-writing` is the authoritative reference for:
- INFOR voice (formal, institutional, Canadian English, defined-term capitalisation, hedged forward-looking claims, semicolon-chained bullets)
- Title and bullet conventions (Title-Case noun phrases, length budgets, fragment vs. sentence rules, punctuation)
- Number, currency, multiple, range, and period notation (`C$MM`, `~`, `x`, en-dash ranges, `FY2024A` / `FY2025E` / `FY2026F`, `LTM`)
- Defined-term and boilerplate patterns (engagement line, teaser disclaimer, confidentiality stamp, source-line format)
- Per-slide-type recipes (executive summary, investment highlights, market overview, valuation commentary, fairness opinion language, etc.)

**Minimum voice rules — fallback when `infor-deck-writing` is not loaded.** If for any reason you cannot load the writing skill, fall back to these defaults so the words still pass an INFOR smoke test:

- Third person ("the Company", "Management", "INFOR"). No first-person, no contractions, no exclamation marks.
- Canadian English: favourable, colour, centres, amongst. `Acquirors` (not "Acquirers").
- Titles are Title-Case noun phrases — never full sentences or questions.
- Bullets are content-rich (15–35 words standard) and may chain related ideas with semicolons; no terminal periods on fragments.
- Forward-looking claims are hedged: "expected to", "anticipated", "could", "may". No absolute superlatives without proof.
- Numbers: `C$MM` default, `~` for approximate, `x` for multiples, en-dash for ranges, `FY2024A` / `FY2025E` / `FY2026F`, `LTM`.
- Defined terms capitalised after first use — `the Company`, `the Transaction`, `the Process`, `Management`.
- Top-of-slide note on every financial slide: `Note: All figures in C$MM unless indicated otherwise; FYE [Month Day]`.
- Avoid: delve, embark, harness, supercharge, transformative-without-proof, em-dash overuse, undefended hype.

Treat these as the minimum — the full guidance in `infor-deck-writing` always takes precedence when both are available.

**Always start from the INFOR Deck Template** (see [`references/deck-template.md`](references/deck-template.md)). The template carries the branded slide master, theme colors, fonts, and example slides for every common layout. Starting from scratch almost always loses master-level formatting (title bars, footers, page numbers, bullet styles, theme font) and produces off-brand output.

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. INFOR logo, deck template, theme, and working directory are resolved inline in Section 10 Step 2.

**Detailed reference** (loaded on demand): [`references/deck-template.md`](references/deck-template.md) — the `clone_slide` helper (preserves image / chart / hyperlink relationships), nine sample-slide layout map, alternative `add_slide` workflow for non-matching layouts, slide-specific conventions (deck structure, cover, earnings slide #4 quote groups, contact page), and template-edit rules.

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

## 9 — Number, Text & Footnote Formats — see `infor-deck-writing`

Number, currency, multiple, range, and period notation — and footnote / source-line conventions — are governed by [`infor-deck-writing`](../infor-deck-writing/SKILL.md) Section 3. Use that skill's reference for `C$MM` / `~` / `x` / en-dash ranges / `FY2024A` / `FY2025E` / `FY2026F` / `LTM`, and for the top-of-slide currency note (`Note: All figures in C$MM unless indicated otherwise; FYE [Month Day]`).

This skill does not duplicate those rules.

---

## 10 — Workflow: Applying Brand Guidelines

When generating or reviewing a PowerPoint:

### Step 1 — Confirm Scope

Determine what is being created or reviewed:
- New deck from scratch → **open the INFOR Deck Template** (Section 11)
- Formatting check on an existing deck → open the existing file; do not rebuild it from the template unless asked
- Specific slide type (cover, content, charts, tables) → clone the matching template slide as a starting point

### Step 2 — Locate Assets

Locate the INFOR logo, deck template, and theme via the plugin's shared helper:
```bash
bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Logo - 1.png"
bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Deck Template.pptx"
bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFORFG.thmx"
```

### Step 3 — Build from Template

For any new deck, follow [`references/deck-template.md`](references/deck-template.md) — open the template, clone the sample slides that match the content you need, then edit the clones. This is the default path.

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
- [ ] Number / period notation per `infor-deck-writing` Section 3 (C$MM default, ~ for approximate, FY2024A / FY2025E / FY2026F, LTM)
- [ ] All on-slide text drafted using `infor-deck-writing` (voice, titles, bullets, defined terms, footnotes)

### Step 5 — Summary

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

WORDS, UNITS & PERIOD NOTATION: governed by `infor-deck-writing`
  (titles, bullets, voice, C$MM, FY2024A/E/F, footnotes, etc.)
```
