# Starting from the INFOR Deck Template

**Default workflow for every new deck.** The template file (`INFOR Deck Template.pptx`) ships with the branded slide master, theme (`INFORFG.thmx`), Palatino Linotype theme font, accent colors, footer/page-number placeholders, and nine sample slides covering every common layout. Opening the template with `python-pptx` inherits all of this automatically. Building the same slides from a blank `Presentation()` almost always produces off-brand output because master-level settings are lost.

## Sample Slides in the Template

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

## Recommended Approach: Clone-and-Edit

Open the template, **clone the sample slide whose layout matches your content**, then edit the clone's text and shapes. This preserves every master-level detail — title bar, footer line, page number placeholder, section-header proportions, table styles, bullet indentation — that you cannot cleanly reproduce from code.

```python
import copy
from pptx import Presentation
from pptx.oxml.ns import qn

TEMPLATE = r"<path from find_template.sh 'INFOR Deck Template.pptx'>"

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

# Now edit text in each cloned slide (see below), then delete the 9 originals.
for _ in range(9):
    delete_slide(prs, 0)

prs.save("output.pptx")
```

## Alternative: Build from Template Layouts

If no sample slide matches, call `add_slide` with one of the template's named layouts. You still inherit the master (theme font, colors, footer, page number) but you must add content shapes yourself — follow the positions in Section 6 of [`../SKILL.md`](../SKILL.md).

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

## Editing Cloned Slide Content

After cloning, locate shapes by their `name` or by their text placeholders. The template uses conventional names: `Title 1`, `Rectangle 14` (section header), `Text Placeholder 1` (footnote/source), `Slide Number Placeholder` (page number). Common placeholder tokens in sample text are `[CLIENT NAME]`, `[Client Name]`, `[x]`, `[QX 202X]`, `[Cap Table Placeholder]` — replace these in place, preserving run-level formatting.

For run-formatting preservation, prefer the shared helper `set_text` from [`../../../scripts/pptx_helpers.py`](../../../scripts/pptx_helpers.py) — it mutates `runs[0].text` in place so the template's font / size / color survives:

```python
import sys, os
sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", "./infor-workflows") + "/scripts")
from pptx_helpers import set_text, find_shape

set_text(find_shape(cover, "Title 1"), ["Project Atlas", "Internal Discussion Materials"])
```

## Rules When Using the Template

- **Never** call `Presentation()` with no arguments for an INFOR deck. Always pass the template path.
- **Do not** modify the slide master or theme from code — the master is the source of truth for every master-level rule in [`../SKILL.md`](../SKILL.md) Sections 2, 3, 4, 5.
- **Do** keep the Disclaimer slide (sample #8) for every external deck.
- **Do** clone the cover slide (sample #1) rather than building a cover from scratch — the navy decorative bar behind the title is an XML construct that is painful to recreate.
- **Do not** delete the template's sample slides until after you've cloned everything you need — deleting them first removes the source shapes you wanted to copy.
- **Always** use `clone_slide` exactly as shown above. The naive `deepcopy`-only version drops image/chart/hyperlink relationships and produces red-X picture placeholders in PowerPoint.
- **Do not** touch the INFOR logo on the cover (shape `Picture 1` at (7.65, 6.21)). The template embeds it correctly — leave it alone. Only edit the `Title 1`, `Subtitle 2` text, and date.
- **Do not** replace placeholder rectangles (`[Cap Table Placeholder]`, `[BBG Comparison Placeholder]`, `[Pie Chart Placeholder]`). These are intentional sizing stubs for the analyst to paste an Excel table, chart, or image into manually. Leave the rectangle and its placeholder text unchanged — resize or reposition only if the user asks.
- **Do not** flatten grouped graphics (`Group 1070`, `Group 1086`, quote-paper groups, etc.) into plain text boxes. Edit the text **inside** the group's child shape — keep the group wrapper, the paper/callout graphic, and all decorative elements.
- If the user supplies their own base deck, open that file instead of the template and apply only the edits requested. Do not rebuild from the template unless the user asks.

## Slide-Specific Conventions

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
- **Business Updates box** (top-left, `Rectangle 5` section header + adjacent text): this is the prose-commentary slot — 2–3 short paragraphs of investment-banking commentary, not bullet-pointed metrics. Draft the actual words using [`infor-deck-writing`](../../infor-deck-writing/SKILL.md) (see the earnings / business-update voice rules and recipes there). Metrics belong in the financial-highlights comparison blocks on the right, not here.
- **Financial highlights blocks** (top-right): keep the template's structure intact — prior-period callout, current-period callout, delta rectangle with up/down triangle, and the horizontal connector line between rows. Edit only the numbers and metric labels (Revenue, EBITDA, Gross Margin, EPS, etc.).
- **Bottom-left placeholder** (`Rectangle 2` at (0.35, 4.55), labelled `[BBG Comparison Placeholder]` or similar): **leave the placeholder rectangle in place**. Do not replace it with metrics, text, or a backlog/KPI block. The analyst pastes the Excel/BBG table in manually after generation.
- **Bottom-right quote-paper groups** (`Group 1070` at (5.14, 4.55) and `Group 1086` at (5.08, 5.72)): these are two decorative "paper" graphics holding management/analyst quotes. **Always include two quotes** (e.g., CEO + CFO, or CEO + analyst). Edit the text *inside* each group — never replace the groups with a plain `TextBox`, which deletes the paper graphic.

**Contact page (#9) — default content.** Unless the user specifies otherwise, the contact page shows **Neil Selfe** (Chief Executive Officer) with three `[x]` placeholders for additional team members to be filled in manually. Edit the first table/photo block with Neil's details; leave the other three blocks as `[x]` placeholders so the analyst can populate them.
