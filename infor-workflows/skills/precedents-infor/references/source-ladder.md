# Source Selection — The 4-Rung Ladder

For each precedent transaction, Revenue and EBITDA must be on an LTM (last-twelve-months) basis ending the most recent quarter before the announcement date. Work this ladder top-down — stop at the first rung that produces a usable figure.

## Rung 1 — Disclosed LTM (or close-to-LTM) $ Figure in Transaction Sources

**Strongly preferred for public AND private targets.**

Look first in:
- The acquiror's deal press release
- Deal-supplement investor deck or 8-K exhibit
- Deal conference call / earnings call transcript discussing the transaction
- Reputable financial news coverage of the transaction (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global)

Many deal announcements explicitly disclose "LTM Revenue of $X" and "LTM (or Adjusted) EBITDA of $Y" — those are typically the figures the buyer used to value the deal and what an investment banker would cite.

Use the disclosed figure as the cell value **as-is**; do not "recalculate" over it. A reasonable sanity check against filings is fine — but if the deal source says $107.9 LTM Revenue, the cell value is $107.9.

## Rung 2 — Disclosed Transaction Multiple → Derive from TEV

**Required when available — supersedes the filings-stub fallback (rung 3), not merely preferred over it.**

If the deal source quotes a multiple but not the absolute $ figure (e.g., "acquired at ~12.5x LTM EBITDA" or "~3.0x Revenue"), derive the metric by dividing TEV by the multiple. Write the cell as a formula referencing the TEV cell directly:
- `=I7/12.5` for J7 (EBITDA)
- `=I7/3.0` for K7 (Revenue)

**Do not multiply by `C{row}`** — column I is already converted to output currency, so the derived metric inherits that conversion.

The multiple reflects how the buyer valued the deal. Use it for both public and private targets when no $ LTM is disclosed.

**Do not skip a disclosed multiple — common bad reasons agents reach for the stub calc instead:**
- The multiple says "approximately Nx" or "~Nx" — still rung 2.
- Wanting to verify from filings — verifying is fine, but the cell value is the disclosed multiple.
- "It's pro forma" — see the pro-forma note below.
- Wanting the standalone number rather than the deal number — the precedents table shows what buyers paid, not target-standalone fundamentals.

**"Pro forma" almost never means synergies.** In deal-source multiples, "pro forma" almost always means pro forma for divestitures or continuing operations — not pro forma for buyer synergies. Synergies are virtually always called out as a separate line item ("$X of expected run-rate cost savings"), not embedded in the headline multiple. Treat the multiple as synergy-inclusive only if the source explicitly says "including synergies," "post-synergy," or "synergized."

## Rung 3 — Calculated LTM from Target Filings (Public-Target Fallback Only)

If, and only if, neither a disclosed $ figure nor a disclosed multiple can be found in the transaction sources, calculate LTM from the target's own filings using the stub-period formula below.

**At most 2 rows in the final table may use this 3-operand stub calc — see the "Stub-calc cap" sub-section below for the selection rule.**

**LTM stub-period formula:**

> **LTM = YTD_MRQ + FY_prior − YTD_PYQ**

…where `YTD_MRQ` is year-to-date through the most recent reported quarter before announcement, `FY_prior` is the most recent completed fiscal year, and `YTD_PYQ` is the matching year-to-date stub from the prior year. The two YTD stubs must cover the **same calendar period** (Q1 vs. Q1, H1 vs. H1, 9M vs. 9M).

| MRQ before announce | YTD stubs to pull |
|---|---|
| Q1 | Q1 current vs. Q1 prior |
| Q2 | H1 current vs. H1 prior |
| Q3 | 9M current vs. 9M prior |
| Q4 | No stub calc — `LTM = FY` (use the 10-K directly) |

Worked example — AvidXchange acquired by TPG / Corpay, announced May 6, 2025:
- LTM Revenue = Q1 2025 ($107.9) + FY 2024 ($438.94) − Q1 2024 ($105.6)
- LTM EBITDA = Q1 2025 ($17.517) + FY 2024 ($84.720) − Q1 2024 ($17.665)

For the stub calc, pull each stub from its own filing — the most recent 10-Q / 6-K / interim MD&A (`YTD_MRQ`), the most recent 10-K / 20-F / AIF (`FY_prior`), and the prior-year 10-Q / 6-K / interim MD&A for the same calendar quarter (`YTD_PYQ`). Apply the same EBITDA definition (Operating Income + D&A from cash flow statement, or Adjusted EBITDA if consistently disclosed) across all three stubs. If MRQ is Q4, no stub calc is needed — use the 10-K's full-year figures.

**Pre-write checkpoint — before writing a 3-operand stub formula for J or K.** State in your response which deal sources you searched for a disclosed $ LTM figure and a disclosed multiple, and what you found. Required search set: the acquiror deal press release, 8-K exhibit / investor deck, and at least one of (Bloomberg, Reuters, WSJ, Globe and Mail, Financial Post, S&P Global) deal coverage. If a multiple was found but rejected, the rejection reason must be checked against the bad-reasons list in rung 2.

### Stub-Calc Cap — At Most 2 Rows Per Table

The 3-operand stub-calc path (rung 3) is by far the most token-expensive route to a row: it requires pulling and reading three separate filings (MRQ, FY prior, PYQ) plus reconciling EBITDA definitions across them. A table that leans heavily on stub calcs burns context that's better spent on broadening rung-1 / rung-2 search across more deals.

**Cap:** at most **2 rows** in the final table may use the 3-operand stub formula `=(mrq+fy-pyq)*C{row}` in either column J or column K. A row with stub-calc on J only, K only, or both J and K counts as **one** row against the cap.

**Selection rule when more than 2 stub-calc candidates exist:** rank the stub-calc candidates by comparability to the input company on sector, business model, client segment, asset class, and scale. Keep the top **2** most comparable. **Drop the remaining stub-calc candidates entirely from the table — do not replace them.** The total table simply has fewer rows. Rungs 1, 2, and 4 remain **uncapped** — only rung 3 is limited.

**Filtering must happen BEFORE pulling the filings for the dropped candidates.** Identify all rung-3 candidates first, apply the comparability ranking, decide which ≤ 2 to keep, and only then fetch the MRQ / FY / PYQ filings for those kept rows. Do not compute stubs you will not write.

**Selection log — required in the response.** Briefly state how many stub-calc candidates were identified, which 2 were kept, and which were dropped. Format: `X stub-calc candidates identified; kept the 2 most comparable: [Deal A], [Deal B]; dropped: [Deal C, ...].` If 2 or fewer rung-3 candidates exist in the first place, state that and skip the ranking.

## Rung 4 — Disclosed Non-LTM Period $ Figure (Private-Target Fallback)

For private targets where rungs 1 and 2 fail, use whatever absolute Revenue / EBITDA figure is disclosed (e.g., FY 2023, calendar 2024). Label the period in the comment and accept that timing may drift by months, but never by years — drop the deal if the only available figure is two-plus years stale.

**There is no filings-based fallback for private targets.** If rungs 1, 2, and 4 all fail for a private target, leave the cell blank (or drop the deal if both Revenue and EBITDA are missing).

## Selection Criteria — Overall

- Similar sector / business model to the input company
- Announced or completed within the last 6–8 years (prefer recent deals)
- Disclosed deal value (TEV) — **required**
- Disclosed Revenue and/or EBITDA — required for public targets; private targets require either disclosed metrics or a disclosed multiple from which a value can be inferred

Never include a transaction where deal value (TEV) is undisclosed — a blank TEV makes the row unusable for multiple analysis.

## "Disclosed" — Precise Definition

A $ figure or multiple is "disclosed" only if it appears in:
- the target's or acquiror's deal press release;
- an 8-K / 6-K / 40-F exhibit or investor deck filed with the announcement;
- the deal-day conference call transcript; or
- major news (Bloomberg, Reuters, WSJ, FT, Globe and Mail, Financial Post, S&P Global) **quoting deal-day materials**.

Numbers computed post-hoc by analysis blogs (mergersight, eResearch, etc.) are **implied by a third party**, not disclosed, and do **not** satisfy rung 1 or rung 2 — even if the blog domain were somehow allow-listed, the figure itself would still be implied rather than disclosed.

## Currency

Use the currency as stated in the original source — when EBITDA / Revenue are written as $ figures (`*C{row}` formulas), they must be in the **same currency** as TEV, matching the ISO 3-letter code entered in column B. The template's column C FX formula converts to the output currency, and the `*C{row}` factor applies that conversion. **Multiple-derived J/K cells (`=I{row}/multiple`) are dimensionless inputs and inherit their currency from I — currency consistency is automatic; do not add `*C{row}`.**
