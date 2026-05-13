---
name: infor-deck-writing
description: >
  Writing, drafting, or rewriting slide-ready text for an INFOR Financial Group PowerPoint —
  exec summaries, investment highlights, company overviews, market pages, valuation and buyer
  commentary, KPI tiles, teaser headlines, fairness-opinion language. Activates on /infor-deck-writing,
  "write slide text", "draft a bullet", "draft an exec summary", "INFOR voice", "rewrite in INFOR voice",
  "investment highlight bullet", "market overview", "valuation commentary", "teaser copy",
  "punch up these bullets", or any request to turn raw notes into slide-ready language for a
  CIM, pitch, teaser, fairness opinion, or formal valuation.
version: 2.10.0
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch]
---

# INFOR Deck Writing — Voice, Style, and Slide-Ready Text

This skill teaches Claude to write text that sounds like it was drafted by an INFOR Financial Group analyst. It covers tone, sentence structure, slide-writing conventions, recurring vocabulary, and per-slide-type recipes — calibrated from a corpus of CIMs, pitch books, teasers, fairness opinions, formal valuations, and strategic reviews.

**Companion skill — formatting:** for visual formatting (fonts, colors, layout, table styles, file structure) use [`brand-guidelines-infor`](../brand-guidelines-infor/SKILL.md). This skill is about **what the words say**, not how they look on the slide.

**Companion reference — slide-type recipes:** detailed templates and verbatim opening lines live in [`references/`](references/), split by deliverable type so only the relevant ~150 lines load on demand instead of the full corpus. Pick the file that matches the request:

| Request maps to | Open |
|---|---|
| Teaser cover line, teaser page 1 / page 2 | [`references/teaser-recipes.md`](references/teaser-recipes.md) |
| CIM executive summary, CIM section framing | [`references/cim-recipes.md`](references/cim-recipes.md) |
| Pitch firm-overview, buyer-approach, risks, timeline, summary | [`references/pitch-recipes.md`](references/pitch-recipes.md) |
| Fairness opinion language, formal valuation | [`references/fairness-opinion-recipes.md`](references/fairness-opinion-recipes.md) |
| Strategic review section structure | [`references/strategic-review-recipes.md`](references/strategic-review-recipes.md) |
| Investment Highlights, Company Overview, Industry, Process, Buyer Commentary, Valuation Commentary, Management Bios, Financial Summary (cross-cutting — appears in multiple deliverables) | [`references/building-blocks.md`](references/building-blocks.md) |

---

## When to use this skill

Activate whenever the deliverable is **slide text**, regardless of the deck type. Some examples:

- "Draft an executive summary for [Company]"
- "Write 5 investment highlights for the teaser"
- "Rewrite these notes in INFOR voice for the company overview slide"
- "Draft a paragraph about [Company]'s market opportunity"
- "Give me a 1-sentence company description"
- "Write valuation commentary for the DCF slide"
- "Draft a buyer-list intro paragraph"
- "Punch this bullet up — make it sound like INFOR"
- "Write a teaser headline / one-liner positioning statement"
- "Draft language for a fairness opinion conclusion"

**Do NOT** use this skill for:
- Visual formatting (use `brand-guidelines-infor`)
- Building data tables — comps, precedents, buyer lists, cap tables (use the respective `*-infor` skills)
- Proofreading a finished deck (use `deckcheck-infor`)
- Financial modeling

---

## 1 — Tone & Voice

INFOR writes for sophisticated readers: special committees, boards, institutional investors, family offices, strategic acquirers, and PE sponsors. The voice is **formal, precise, and confident, but always defensible**.

### Core rules

| Rule | Detail |
|------|--------|
| **Formality** | Institutional. No contractions, no slang, no jokes, no rhetorical questions, no exclamation marks. |
| **Person** | Third person; "the Company", "Management", "INFOR". First-person plural ("we", "us", "our") used in fairness opinions and pitch commentary where INFOR is the speaker. Never "I" or "you". |
| **Assertion vs. hedging** | Measured-superlative positioning ("leading", "well-positioned", "preeminent") is fine when supported. Forward-looking claims are hedged ("expected to", "anticipated", "could", "may"). Never use absolute superlatives ("the best", "the only") without proof. |
| **Sentence length** | Medium-long. Most slide-body sentences run 18–35 words. Compound sentences with semicolons are the house style. |
| **Spelling** | **Canadian English** — `favourable`, `colour`, `centres`, `realise/realize` (both ok), `amongst`. Never `favor`, `color`, `centers`. |
| **Quotation marks** | Curly quotes (`"…"` and `'…'`), not straight. Use `("Term")` to define a capitalised short form on first use, then refer to the defined term throughout: `the "Company"`, `the "Transaction"`, `the "Process"`. |
| **Em-dash** | Em-dash (—) is used for asides and to introduce a clarification. Don't overuse — at most one per sentence, and never adjacent bullets both leading with em-dashes. |
| **Semicolons** | Used liberally to chain related clauses inside a single bullet. INFOR bullets often look like: *"[Clause]; [Clause]; [Clause]"* rather than three separate bullets. |
| **Ampersand** | Use sparingly. `&` appears in titles and tile labels ("Key Figures & Highlights", "Revenue & Margin"); body text uses "and". |
| **Acronyms** | Spell out on first use, then parenthesise the acronym in defined-term style: `discounted cash flow ("DCF")`, `last twelve months ("LTM")`, `assets under management ("AUM")`. |

### What INFOR sounds like — and what it doesn't

✅ INFOR voice:
> "The Company is a leading software-as-a-service ("SaaS") provider of whole-person wellbeing solutions for employers, health plans and other organizations; the Company's holistic product suite of digital solutions allows organizations to provide best-in-class content and expertise at scale."

❌ Not INFOR voice (too casual, padded, AI-flavoured):
> "We're excited to dive into how this company is fundamentally transforming the wellbeing space! By leveraging cutting-edge tech, they're helping organizations unlock the full potential of their workforce."

The first sentence: measured ("leading", not "fundamentally transforming"), defines its terms ("SaaS"), uses semicolon-chained structure, drops in concrete positioning ("whole-person wellbeing"), and says nothing it can't defend. The second: hype words, undefined "tech", unsupported claims, exclamation mark, first-person plural in marketing register rather than advisory register.

---

## 2 — Slide-writing conventions

### Titles

Titles are **noun phrases in Title Case** — never full sentences, never questions. They land in the navy title bar at the top of the slide.

Common patterns (use these as templates):

| Pattern | Examples |
|---------|----------|
| Plain section name | `Executive Summary`, `Investment Highlights`, `Company Overview`, `Market Opportunity`, `Management Team`, `Financial Summary`, `Process Considerations`, `Buyer Universe`, `Approach to Value`, `Valuation Methodologies`, `Precedent Transactions`, `Comparable Companies` |
| Section name + qualifier | `Core Investment Highlights`, `Expanded Investment Highlights`, `Key Investment Highlights`, `Key Process Milestones`, `Key Financial Figures for Fairness Opinion`, `Illustrative Valuation`, `Basis of Valuation` |
| Positioning headline (for an individual highlight box) | `Competitive Moat via Differentiated Platform`, `Predictable & Profitable Model`, `Favourable Industry Dynamics Support Growth`, `Top-Tier Origination Platform`, `Sustainable Supply & Regenerative Farming`, `Recession-Proof, Non-Discretionary Offering` |
| Process/methodology | `Approach to Determine Fairness`, `Buyer Approach Strategy`, `Strategic Exit Considerations`, `Illustrative Timeline & Key Workstreams`, `Proposed Terms of Engagement`, `Summary and Near-Term Next Steps` |
| "Select…" | `Select Potential Acquirors – Financial Sponsors`, `Select Potential Acquirors – Strategic Acquirors`, `Select Customers`, `Select MEP Customers` |

Notes:
- The word "Acquirors" (not "Acquirers") is INFOR's house spelling.
- "(Cont'd)" is used on continuation slides: `Executive Summary (Cont'd)`.
- Section dividers use the section name centred in a stack of rounded rectangles, with the current section highlighted.

### Bullets

INFOR bullets are usually **complete thoughts written as fragments or near-complete sentences** — substantive, content-rich, often semicolon-chained. They are **not Pithy 5-word summaries**.

| Bullet type | Length | Example |
|-------------|--------|---------|
| **Short** (tile labels, KPI captions) | 2–6 words | `Diversified revenue mix`, `Run-Rate EBITDA`, `Top-Tier Management Team` |
| **Standard** (most body bullets) | 15–35 words | "Long-standing relationships with federal agencies, universities, healthcare systems and major developers, supported by 60+ institutional energy partnerships and tier 1 bidder status" |
| **Dense** (investment-highlight sub-bullets, valuation commentary) | 35–80 words, often two clauses joined by a semicolon | "Asset-light SaaS model (once content is produced, it can be utilized by thousands of end users) and contracts are multi-year in nature resulting in consistently high margins; strong operating leverage through its existing infrastructure (technology and human capital) and extensive proprietary content base" |

**Bullet terminations:**
- Fragments and list items — **no terminal period**. INFOR rarely terminates bullets with periods unless the bullet is a true multi-sentence paragraph.
- Disclaimers, footnotes, and legal language — full sentences with periods.
- Never mix terminated and unterminated bullets within the same list.

**Bullet rhythm:**
- A slide section usually pairs a **bold headline** (or small navy section header) with **2–4 supporting bullets** underneath.
- Numbered investment-highlight slides typically show **5–6 numbered items**, each with a one-line headline + 1–3 sub-bullets.
- Mix bullet lengths inside a section so the page doesn't look like a wall of identical lines.

### Punctuation specifics

- **Semicolons inside a bullet** are the signature INFOR move. Use them to chain a positioning statement with its supporting evidence.
- **Parentheticals** are used to define terms, give footnote markers, or insert a quick numeric aside: `(MHSS)`, `(~$125MM FY2022F Revenue)`, `(1)`.
- **Footnote markers** are `(1)`, `(2)`, `(3)`, etc., placed inline at the end of a phrase. Footnote text sits at the bottom of the slide at 7 pt, no trailing period unless it's a full sentence.
- **Ranges**: `7.5–10.5x`, `FY2025 – FY2029`, `~13.75–14.25%` — use en-dash (–) for numeric ranges, with optional spaces for readability. Don't use a hyphen for ranges.
- **Approximation marker**: `~` immediately before the number, no space: `~$46MM`, `~90%`, `~125`.
- **Plus markers**: `+13MM`, `60+`, `1,800+` used for "more than" in tile callouts.

---

## 3 — Numbers, units, and time-period notation in body text

| Element | Format | Example |
|---------|--------|---------|
| Default currency | `C$` + figure | `C$25MM`, `C$1.4B` |
| Default unit | `C$MM` (millions) | Always declared in a top-of-slide note: `Note: All figures in C$MM unless indicated otherwise` |
| US dollars | `US$` or `USD` | `US$193B`, `US$4B` |
| Approximation | `~` immediately before figure | `~C$46MM`, `~15%`, `~900` |
| Percentage | `12%`, `~5%`, never `12 percent` | |
| Multiples | `x` lower-case, no space | `7.5x`, `10.0–11.5x`, `3.0x LTM Adj. EBITDA` |
| Range | en-dash `–`, optional spaces | `FY2025 – FY2029`, `13.75–14.25%` |
| Fiscal year | `FY2024A` (actual), `FY2025E` (estimate), `FY2026F` (forecast) | |
| Calendar year | `CY2024`, `CY2024E` | |
| Quarter | `Q1-24`, `Q1 2024`, `Q1 CY2024`, `Q1 FY2024` (mix; pick one and stay consistent) | |
| Trailing twelve months | `LTM` (preferred), `TTM` (also seen) | `LTM Adj. EBITDA` |
| Pro forma / run-rate | `pro forma`, `run-rate`, `PF` in tables | "Run-Rate EBITDA as at Dec-24E" |
| FYE declaration | "FYE December 31", "FYE September 30" | Appears in the top note of every financial slide |

**Always declare** the currency and FYE in a top-of-slide footnote (7 pt at the bottom or a small note at the top): `Note: All figures in C$MM unless indicated otherwise; FYE December 31`.

---

## 4 — Vocabulary — INFOR house words

Use these. They appear repeatedly across decks and signal INFOR voice.

### Positioning verbs and adjectives

`leading`, `well-positioned`, `preeminent`, `flagship`, `best-in-class`, `top-tier`, `blue-chip`, `differentiated`, `defensible`, `proprietary`, `mission-critical`, `comprehensive`, `fully-integrated`, `end-to-end`, `one-stop shop`, `scalable`, `asset-light`, `capital-light`, `sticky`, `recurring`, `diversified`, `resilient`, `compelling`, `attractive`, `robust`, `meaningful`, `material`, `high-quality`, `long-standing`, `established`, `proven`, `actionable`, `near-term`

### Growth / momentum

`tailwinds`, `favourable industry dynamics`, `secular growth`, `structural support`, `accelerating`, `expanding`, `scaling`, `penetrating`, `capturing`, `unlocking`, `unrealised operating leverage`, `further operating leverage yet to be realized`, `cross-selling opportunities`, `runway`, `whitespace`

### Process verbs

| Use these | Avoid these (off-brand AI flavour) |
|-----------|------------------------------------|
| enable, drive, support, deliver, facilitate, execute, advance, accelerate, enhance, strengthen, broaden, deepen, position, capture, address, serve, deploy, scale | delve into, dive deep, embark on, unlock the power of, harness, supercharge, revolutionise, transform (without specifics), tapestry, journey, ecosystem (over-used), at the end of the day |

`leverage` and `utilize` **are** used by INFOR — `the platform leverages AI/ML`, `MHR is utilized on 99% of days` — so they aren't banned, but prefer the simpler verb (`uses`, `employs`, `applies`) when the meaning is identical.

### Transaction verbs (boilerplate)

`has engaged`, `is contemplating`, `is exploring`, `is considering`, `intends to pursue`, `is evaluating`, `seeking to`, `in connection with`, `pursuant to`, `subject to`, `contingent upon`

### Qualifiers

`highly`, `significantly`, `substantially`, `materially`, `meaningfully`, `disproportionately`, `expected to`, `anticipated`, `forecasted`, `projected`, `assumed`, `contemplated`, `likely`, `could`, `may`, `where applicable`

### House boilerplate (verbatim — use as-is)

**Engagement line** (on every teaser and CIM page 1):
> [Company Name] ("[Defined Term]" or the "Company") has engaged INFOR Financial Inc. ("INFOR") as its exclusive financial advisor in connection with [a potential sale / a potential majority divestiture of the shares / exploring financing alternatives / a potential capital raise of C$XXMM / a Transaction with the Company] (the "Transaction").

**Teaser purpose line:**
> The purpose of this Teaser is to provide an overview description of the Company to assist potential buyers in their consideration of a submission of an Expression of Interest ("EOI").

**Default top-of-slide note:**
> Note: All figures in C$MM unless indicated otherwise; FYE [Month Day]

**Confidentiality stamp** (top right corner, every slide):
> Strictly Private & Confidential

**Teaser disclaimer (verbatim):**
> While the information contained herein is believed to be accurate and reliable, none of the Company, INFOR Financial Inc. ("INFOR"), or their employees, officers, directors, shareholders or stakeholders, make any representations or warranties, expressed or implied, as to the accuracy, reliability or completeness of such information embodied herein and none of them shall have any liability for such information, nor for the accuracy, reliability or completeness of such information. This document is not meant to be and should not be distributed to any other parties. In furnishing this document, INFOR reserves the right to amend, replace, or rescind the document at any time and undertakes no obligation to provide the recipient with access to any additional information. In all cases, interested parties should conduct their own investigation and analysis of the Company and the information contained herein.

**Defined-term capitalisation pattern** — once introduced, always capitalise: `the Company`, `Management`, `the Transaction`, `the Process`, `the Confidentiality Agreement`, `the Special Committee`, `the Board`, `the Purchaser`, `the Consideration`, `the Fairness Opinion`, `the Arrangement Agreement`.

---

## 5 — Slide-type recipes

Recipes live in [`references/`](references/), split by deliverable so the model loads only the relevant ~150–300 lines on demand. See the table at the top of this file for which file to open per request. The recipes cover:

**By deliverable:**
- [`teaser-recipes.md`](references/teaser-recipes.md) — cover line, page 1 ("The Opportunity"), page 2, full worked example
- [`cim-recipes.md`](references/cim-recipes.md) — executive summary, section map, disclaimer boilerplate
- [`pitch-recipes.md`](references/pitch-recipes.md) — INFOR firm overview, buyer approach strategy, risks & mitigants, illustrative timeline, summary & next steps
- [`fairness-opinion-recipes.md`](references/fairness-opinion-recipes.md) — cover, disclaimer, introduction, independence, assumptions & limitations, scope of review, approach to fairness, conclusion; plus formal valuation additions (valuation date, methodology weighting, implied range)
- [`strategic-review-recipes.md`](references/strategic-review-recipes.md) — section structure, alternatives comparison, recommendation pattern

**Cross-cutting building blocks** ([`building-blocks.md`](references/building-blocks.md)) — these appear in multiple deliverables so they live in one place:
- Investment Highlights (Core + Expanded)
- Company Overview / Business Description
- Business Segments
- Industry / Market Overview
- Process — Key Process Milestones / Timeline
- Buyer-List Commentary
- Valuation Commentary (Comps, Precedents, DCF, Football Field)
- Management Team / Bios
- Financial Summary / KPI Tile Blocks

---

## 6 — Workflow: turning raw notes into INFOR slide text

When given source material (call notes, management slides, a CIM draft, a research blurb, or a one-line ask), follow this loop:

### Step 1 — Clarify the slide type and audience

Ask (only if not obvious from context) which slide type and which deck type the text is for. The slide type drives the structure (see the recipes table at the top of this file); the deck type drives the formality dial:

| Deck type | Formality dial | Defended forward-looking claims |
|-----------|----------------|-------------------------------|
| Teaser | Highest pitch energy, most compressed | Aspirational but credible |
| CIM | Detailed, fact-rich, neutral-positive | Always sourced to Management |
| Pitch | Confident, advisor-voice, references INFOR's track record | "We believe", "INFOR expects" |
| Fairness Opinion / Formal Valuation | Legal, cautious, exhaustively caveated | Hedged, multiple methodologies |
| Strategic Review | Diagnostic, options-oriented | Lays out alternatives, doesn't recommend |

### Step 2 — Identify defended facts vs. unsupported hype

Read the source material and pull out:
- **Facts** with attribution (Management projections, public filings, third-party sources)
- **Positioning claims** the source already supports (e.g., "largest network of 57 locations" — defensible if true)
- **Hype words** without backup ("amazing", "industry-disrupting", "revolutionary") — drop or replace with measured equivalents

### Step 3 — Draft using the appropriate recipe

Open the matching recipe file in [`references/`](references/) (see the table at the top of this SKILL.md). Use the template's opening line and structure. Adapt verbatim examples to the target Company.

### Step 4 — Apply the INFOR style filter

Run your draft through this checklist:

- [ ] Title is a Title-Case noun phrase, no full sentence, no question
- [ ] All claims are measured ("leading"/"preeminent" with proof, not "best ever")
- [ ] All forward-looking statements are hedged ("expected to", "could", "anticipated")
- [ ] Bullets are content-rich (not 5-word summaries) and not over-padded either
- [ ] Semicolons used inside bullets to chain related ideas where it fits
- [ ] No exclamation marks, no rhetorical questions, no contractions
- [ ] Canadian English (`favourable`, not `favorable`)
- [ ] Defined terms capitalised consistently ("the Company", "the Transaction")
- [ ] All acronyms expanded on first use: `discounted cash flow ("DCF")`
- [ ] Currency, percentage, multiple, and period notation match Section 3
- [ ] No AI-style verbs (delve, embark, harness, supercharge, transform-without-proof)
- [ ] No em-dash overuse, no bullet starting with "And", no orphaned periods
- [ ] Bullet terminations consistent across the list (all unterminated or all sentences)
- [ ] Total text fits the slide — see Section 7 on length budgets

### Step 5 — Cut

INFOR copy is dense but never bloated. Make a final pass and cut every word that doesn't earn its place. Specifically:
- Adjective stacks (`robust, scalable, attractive, sustainable platform`) → keep the one or two that say something specific
- "It is important to note that…" → just say the thing
- "In addition" / "Furthermore" / "Moreover" at the start of a bullet → drop unless the bullet really is a continuation
- "Various", "several", "numerous" without a number → replace with the number, or cut

---

## 7 — Length budgets per slide element

Slides are 10" × 7.5". Palatino Linotype 11–12 pt body text at standard leading fits roughly:

| Element | Hard ceiling | Comfortable target |
|---------|--------------|--------------------|
| Slide title (in navy bar) | ~70 characters / one line | 30–55 characters |
| Section header (in navy box) | ~40 characters / one line | 15–35 characters |
| Positioning headline (above a bullet group) | ~80 characters / one line | 30–60 characters |
| Standard bullet | ~250 characters / 2 lines | 100–180 characters (1–1.5 lines) |
| Dense bullet (exec summary, valuation) | ~400 characters / 3 lines | 200–320 characters |
| Investment-highlight paragraph (numbered item) | 60–90 words | 35–60 words |
| Executive summary paragraph (full-page text) | 1,400–1,800 characters | 900–1,300 characters |
| KPI tile caption | 2–4 words below the figure | 2–3 words |
| Footnote (7 pt at bottom) | one line, ~180 characters | ~100 characters |

When you exceed the ceiling, you're writing for a Word doc, not a slide. **Cut.**

For full-page text slides (Executive Summary, Disclaimer): write tight, multi-clause sentences and let semicolons carry the structure. Avoid stacks of 5+ short bullets — INFOR's exec summary is typically 1–2 dense paragraphs followed by a numbered list of 5–6 investment highlights.

---

## 8 — Editorial anti-patterns (avoid these)

These were not observed in the INFOR corpus and will read as off-brand or AI-generated:

| Anti-pattern | Why it's wrong | Fix |
|--------------|----------------|-----|
| "We're excited to…", "I believe…" | Wrong register; INFOR is institutional | Drop the meta-comment; just state the fact |
| Exclamation marks | Never used | Remove |
| Rhetorical questions in titles or bullets | Never used | Convert to a noun-phrase title or assertion |
| "Delve into", "embark on", "harness", "unlock the full power of" | AI-flavoured | Use plain verbs: `analyze`, `pursue`, `apply`, `realize` |
| "Transformative", "revolutionary", "game-changing" without proof | Hype without evidence | Replace with measured positioning + the concrete proof |
| "Best-of-breed", "world-class" — actually OK | Both appear in INFOR decks, sparingly | OK if defensible |
| Em-dash in every sentence | Looks AI-generated | Use one em-dash per bullet max; prefer semicolons or parentheses |
| Bullet of identical length × 6 | Visually monotonous | Vary lengths; mix short and standard bullets |
| Bullets starting with "This", "These", "It" | Padding | Start with the noun: "The Company…", "The platform…", "Management…" |
| Same opening word in 3 consecutive bullets | Sloppy editing | Vary openers; track the first word as you go |
| "In conclusion", "To summarize" | Wasted line | Just write the conclusion |
| Marketing adjectives stacked 3+ deep | Empty | Pick the strongest one and add evidence |
| American spelling (`favorable`, `color`) | Wrong register | Canadian spelling |
| "Acquirer" | INFOR uses `Acquiror` | Use `Acquirors` in deck text |
| Unterminated bullet next to terminated bullet | Inconsistent | Pick one termination style and apply across the list |
| Sources line missing on a slide with data | Looks ungrounded | Always cite: `Source: Bloomberg, Company filings, Mergermarket, equity research, INFOR Financial estimates` |
| Currency or period notation undeclared | Looks careless | Always include the top-of-slide note declaring C$MM and FYE |

---

## 9 — Quick reference card

```
TONE: institutional, formal, confident, hedged. No I/you. No exclamation marks.

VOICE PRINTS:
  "The Company is a leading [sector] provider of …"
  "Founded in [year], [Company] is a [positioning] …"
  "The Company has engaged INFOR Financial Inc. ("INFOR") as its exclusive
   financial advisor in connection with [purpose] (the "Transaction")"
  "[Company] is well positioned to capture …"
  "Management expects/anticipates/projects …"

TITLES: noun phrase, Title Case, no period, no question mark.
        e.g., "Investment Highlights", "Approach to Value",
              "Favourable Industry Dynamics Support Growth"

BULLETS: content-rich, 15–35 words for standard, 35–80 words for dense.
         Semicolons chain related clauses inside one bullet.
         No terminal period on fragments; periods only for full sentences.
         Vary length across a section; vary opening word.

NUMBERS: C$MM default, ~ for approximate, x for multiples, en-dash for ranges,
         FY2024A / FY2025E / FY2026F, LTM, Q1-24.

CANADIAN: favourable, colour, centres, amongst. Acquirors (not Acquirers).

DEFINED TERMS: ("Term") on first use; capitalise thereafter.
               the Company, Management, the Transaction, the Process.

HEDGING: forward-looking statements use "expected to", "anticipated",
         "could", "may". Never absolute promises.

BANNED: delve, embark, harness, supercharge, revolutionary,
        rhetorical questions, exclamation marks, contractions, "I/you".

SOURCE LINE: every data slide needs Source: at the bottom.

TOP NOTE: every financial slide needs "Note: All figures in C$MM unless
          indicated otherwise; FYE [Month Day]".

CONFIDENTIALITY: every slide carries "Strictly Private & Confidential".
```

---

For per-slide-type templates and verbatim opening lines, see the recipe files in [`references/`](references/) — the routing table at the top of this file maps every request type to the right file.
