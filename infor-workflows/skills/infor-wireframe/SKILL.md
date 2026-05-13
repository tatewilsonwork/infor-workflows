---
name: infor-wireframe
description: >
  Slide-by-slide wireframe for a new INFOR Financial Group PowerPoint deliverable — CIM, pitch,
  fairness opinion, or teaser. Outputs page order, slide purpose, recommended layout, and content
  blocks that another agent or analyst can use to draft the deck. Activates on /infor-wireframe,
  "wireframe a CIM", "outline a pitch", "plan a fairness opinion", "teaser wireframe",
  "draft the deck order", "what slides go in a CIM", "skeleton of a pitch book".
version: 2.9.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# INFOR Deck Wireframe — Slide-by-Slide Plans for the Four Deliverable Types

This skill turns "we need a CIM / pitch / fairness opinion / teaser for [Company]" into a
slide-by-slide wireframe an analyst (or another AI agent) can follow to build the deck. The
wireframes are calibrated from a corpus of INFOR example decks across all four deliverable types
and encode the typical slide order, recurring slide types, common section dividers, layout
patterns, and the visual building blocks (tables, charts, KPI tiles, timelines, valuation
methodologies) that INFOR uses.

This skill outputs **structure** — what slides to include, what each one is for, what goes on it,
how to lay it out. It does not write the words on the slide and it does not render the PowerPoint.
Two companion skills handle those:

- **[`infor-deck-writing`](../infor-deck-writing/SKILL.md)** — all on-slide text (titles, bullets,
  headlines, paragraphs, footnotes, voice, defined terms, number / period notation, slide-type
  recipes). When the wireframe is approved and the analyst starts drafting copy, hand off to this
  skill.
- **[`brand-guidelines-infor`](../brand-guidelines-infor/SKILL.md)** — visual formatting (slide
  dimensions, colors, fonts, layouts, tables, charts, logo placement, template structure) and the
  required deck scaffolding (Cover → Executive Summary → Content → Disclaimer → Contact, all built
  from the INFOR Deck Template). When the wireframe is converted into actual slides, hand off to
  this skill.

The wireframe sits **between** the kick-off conversation and the drafting / formatting work. It is
the one place where the analyst can see the whole deck in outline form before any words or shapes
are committed.

---

## When to use this skill

Activate whenever the user asks for the **shape** of an INFOR deck rather than the words inside it.
Some examples:

- "Wireframe a CIM for [Company]"
- "What slides should go in a pitch for [Company]?"
- "Outline a fairness opinion presentation for the [Transaction] special committee"
- "Build me a teaser skeleton for Project [Codename]"
- "Plan the deck — I want to see the page order before I start writing"
- "How long should this CIM be?" / "Which sections does a fairness opinion need?"
- "Compare the slide order for a full CIM vs. a slim CIM"
- "Give me the wireframe and I'll fill in the bullets"

**Do NOT** use this skill for:

- Writing the actual slide text (use [`infor-deck-writing`](../infor-deck-writing/SKILL.md))
- Building or formatting the PowerPoint file (use
  [`brand-guidelines-infor`](../brand-guidelines-infor/SKILL.md))
- Reviewing / proofing an existing deck (use
  [`deckcheck-infor`](../deckcheck-infor/SKILL.md))
- Generating data tables (comps, precedents, buyers list, cap table — use the respective
  `*-infor` skills)
- Strategic reviews, formal valuations, or earnings update decks (those have their own structures
  — see the limitations note in Section 6)

---

## What the wireframe contains

Every wireframe this skill produces has the same shape, regardless of deliverable type:

1. **Header** — deliverable type, target Company, Project codename (if applicable), recommended
   page count, and any user-supplied parameters (transaction type, audience, timing).
2. **Section map** — the major sections of the deck and the page range each occupies.
3. **Slide-by-slide table** — one row per slide with:
   - Slide number
   - Slide title (placeholder / suggested)
   - Purpose (one sentence — what this slide is for)
   - Content blocks (the building blocks that go on the slide — e.g., engagement-line paragraph,
     KPI tiles, two-column overview, comps table, methodology bullets, charts)
   - Layout pattern (which INFOR Deck Template sample slide to clone — see
     [`brand-guidelines-infor` Section 11.1](../brand-guidelines-infor/SKILL.md))
   - Status — **Standard** (always include), **Optional** (include if applicable), or
     **Situational** (include only when the noted condition is met)
4. **Per-slide notes** — for non-obvious slides, a short paragraph explaining when to include,
   remove, or modify, plus pointers to the most relevant `infor-deck-writing` recipe.
5. **Handoff line** — a one-line instruction at the end pointing to `infor-deck-writing` for copy
   drafting and `brand-guidelines-infor` for slide construction.

---

## Deliverable types and references

Each deliverable type has its own reference file with the full wireframe. Open the one that matches
the user's request:

| Deliverable | Reference | Typical length | When to use |
|-------------|-----------|----------------|-------------|
| **Teaser** | [`references/teaser-wireframe.md`](references/teaser-wireframe.md) | 2 pages (standard) | Anonymised / lightly-anonymised first-look document distributed to potential buyers in a sell-side or capital-raise process |
| **CIM** | [`references/cim-wireframe.md`](references/cim-wireframe.md) | 30–80 slides | Detailed Confidential Information Memorandum for qualified buyers under NDA, post-teaser. Full company, market, financial and process detail |
| **Pitch deck** | [`references/pitch-wireframe.md`](references/pitch-wireframe.md) | 25–50 slides | INFOR-authored discussion materials for a client board, special committee, or management — covers situation, valuation, buyer universe, process, INFOR credentials, and case studies |
| **Fairness opinion** | [`references/fairness-opinion-wireframe.md`](references/fairness-opinion-wireframe.md) | 35–50 slides | Presentation accompanying INFOR's written fairness opinion to a special committee under MI 61-101, summarising the methodologies, valuation range, and the opinion conclusion |

Slim, expanded, and variant structures (for example, a 2-slide vs. 4-slide teaser; a CIM with vs.
without Appendix; a pitch with vs. without LBO analysis) are all flagged inside each reference
file.

---

## Workflow

When invoked, follow this loop:

### Step 1 — Diagnose the deliverable type

If the user has named the deliverable (CIM, pitch, fairness opinion, teaser), use it. Otherwise
ask which of the four. If they describe something outside the four (formal valuation, strategic
review, earnings update), see Section 6 below — fall back to the closest type and note the
limitation, or hand off to a more specific skill if one exists.

### Step 2 — Gather context

Ask (only if not already provided) the minimum context needed to tailor the wireframe:

- **Company name** and (if known) Project codename
- **Transaction context** — sell-side / buy-side / capital raise / refinancing / fairness on a
  signed transaction / unsolicited bid / strategic review
- **Audience** — Board, Special Committee, Management, prospective buyers, lenders
- **Depth** — full / standard / slim version
- **Any constraints** — page-count target, must-have sections, sections to omit, attached source
  material

Default to the standard structure if the user does not specify a depth.

### Step 3 — Open the matching reference

Read the relevant reference file from `references/`. It contains the full slide-by-slide
wireframe, including Standard / Optional / Situational tags and notes on when to include or omit
each slide.

### Step 4 — Tailor the wireframe

Adjust the standard wireframe to the gathered context:

- Drop any slide whose Situational condition is not met (e.g., omit LBO analysis if the
  Transaction is not a take-private; omit the SOTP methodology in a Fairness Opinion if the
  business is not diversified).
- Add any user-requested slides not in the standard wireframe, flagged as **User-added**.
- Re-number slides after additions / deletions.
- If the user specified a slim or expanded depth, follow the variant guidance inside the
  reference file.

### Step 5 — Output the wireframe

Present the wireframe as a Markdown document with:

1. A one-paragraph header (deliverable, Company, Project codename, page count, key parameters).
2. The section map.
3. The slide-by-slide table.
4. Per-slide notes for any Optional / Situational / User-added slide whose inclusion the analyst
   should think about.
5. A handoff line such as: *"Hand off to [`infor-deck-writing`](../infor-deck-writing/SKILL.md)
   for slide copy and [`brand-guidelines-infor`](../brand-guidelines-infor/SKILL.md) for
   PowerPoint construction from the INFOR Deck Template."*

Keep slide titles as **suggestions / placeholders** — they will be refined when copy is drafted.
Do not write any bullets, paragraphs, or numbers on the slide here; that is the job of
`infor-deck-writing` and the analyst.

### Step 6 — Offer the next step

End by offering to (a) draft the copy for any specific slide using `infor-deck-writing`, or
(b) hand the wireframe to `brand-guidelines-infor` to build the actual `.pptx` from the INFOR Deck
Template. Wait for the user's direction before doing either.

---

## Anti-patterns (avoid)

- Do not invent INFOR-specific section names, slide titles, or conventions that are not supported
  by the references or the existing `infor-deck-writing` / `brand-guidelines-infor` skills. The
  vocabulary the wireframe uses must already exist in the corpus.
- Do not draft copy. The wireframe is a plan, not a draft. If you find yourself writing bullets,
  KPI captions, or paragraphs, stop and switch to `infor-deck-writing`.
- Do not invent valuation methodologies, deal terms, financial figures, or precedent transaction
  details. The wireframe says *where* those things go; producing them is the job of the relevant
  data-table skill (`comps-infor`, `precedents-infor`, `buyerslist-infor`, `captable-infor`,
  `lbo-model`) or the analyst.
- Do not skip the Disclaimer or Contact slide. Every external INFOR deck ends with the Disclaimer
  followed by the Contact page (see
  [`brand-guidelines-infor` Section 11.6](../brand-guidelines-infor/SKILL.md)). The wireframe
  must include them.
- Do not omit the section dividers. INFOR decks navigate through repeating tab-style section
  dividers (a single slide carrying just the section name in a rounded rectangle stack with the
  current section highlighted). They are part of the structure, not decoration.
- Do not produce a wireframe longer than the reference's expanded length without flagging it as
  non-standard.

---

## Quick reference card

```
WIREFRAME PRODUCES
  • Section map (which sections, in what order, how many pages each)
  • Slide-by-slide table (#, title, purpose, content blocks, layout, status)
  • Per-slide notes for Optional / Situational slides

WIREFRAME DOES NOT PRODUCE
  • Slide copy → infor-deck-writing
  • Slide PowerPoint → brand-guidelines-infor (clone from INFOR Deck Template)
  • Data tables (comps, precedents, buyers) → respective *-infor skills
  • Fairness opinion conclusion language → infor-deck-writing (verbatim recipes)

DELIVERABLE TYPES (open the matching reference under references/)
  • Teaser            — references/teaser-wireframe.md            (2 pp standard)
  • CIM               — references/cim-wireframe.md               (30–80 pp)
  • Pitch             — references/pitch-wireframe.md             (25–50 pp)
  • Fairness Opinion  — references/fairness-opinion-wireframe.md  (35–50 pp)

ALWAYS
  • Cover, Disclaimer, Contact bookend every deck (see brand-guidelines-infor §11.6)
  • Section-divider slides between major sections
  • Tag each slide Standard / Optional / Situational
  • End with a handoff line to infor-deck-writing and brand-guidelines-infor
```

---

## 6 — Limitations

The wireframes in `references/` cover the four target deliverable types and are calibrated from a
corpus of representative INFOR example decks (multiple decks per type for CIM, pitch, and teaser;
a smaller sample for fairness opinion). Confidence is highest where the corpus shows a strong
pattern across decks; situational slides reflect divergence between decks and should be evaluated
case-by-case.

Out-of-scope deliverables — **strategic review**, **formal valuation**, **earnings update** —
share components with the four target types (formal valuations in particular overlap heavily with
fairness opinions and add an explicit fair-market-value range; strategic reviews overlap with
pitches and add a longer alternatives-analysis section). For these, fall back to the closest of
the four wireframes, flag the gap to the user, and consider directing them to the
`earningsupdate-infor` skill for earnings updates specifically. Do not invent a wireframe for
deliverables outside the supported set without explicit user direction.

For all on-slide copy decisions, defer to [`infor-deck-writing`](../infor-deck-writing/SKILL.md).
For all visual / template / formatting decisions, defer to
[`brand-guidelines-infor`](../brand-guidelines-infor/SKILL.md).
