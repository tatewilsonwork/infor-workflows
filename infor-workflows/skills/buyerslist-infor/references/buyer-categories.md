# Buyer Categories — Detailed Definitions

## Strategic Buyer Categories

- **Direct Competitors** — companies in the same space gaining market share, revenue synergies, eliminating a competitor
- **Adjacent Players** — companies in adjacent markets that could expand via acquisition; product extension, cross-sell, new market entry
- **Vertical Integrators** — customers or suppliers that could integrate vertically; supply chain control, margin capture, strategic lock-in
- **Platform Builders** — large companies building a platform in the space through M&A; tuck-in acquisition, capability gap fill

## Financial Buyer Categories

- **Platform Investors** — sponsors looking to establish a new platform in this sector; consider fund size, sector focus, and deal size range
- **Add-on Buyers** — sponsors with existing portfolio companies that could acquire the target as a bolt-on; identify the specific portfolio company and the synergy rationale
- **Growth Equity** — for earlier-stage or high-growth targets; minority or majority investors

## Other Buyers (Optional Third Category)

Set by the user via `other_label`. Common examples:

| Category | What to look for |
|---|---|
| Family Offices | Active direct investors, sector familiarity, typical cheque size, recent deals |
| International Strategic Buyers | Foreign strategics with disclosed interest in the target's geography, FX/tax considerations, precedent cross-border deals |
| Sovereign Wealth Funds | Mandate fit (infra/financials/tech), direct-deal capacity, recent co-investments |
| Consortium Buyers | Plausible PE + strategic pairings, prior consortium precedents |
| SPACs | Live SPACs with sector fit, trust size vs. target EV, deadline proximity |

## Transactions Column — Category-Specific Format

The Transactions column must reflect the kind of activity the category actually does — an acquirer's M&A, an investor's rounds, a funder's cases. Pick the format that matches:

| Category | What "Transactions" means | Format example |
|---|---|---|
| Family Offices | Recent direct deals / investments | `"Target - YY, Target - YY, Target - YY"` |
| International Strategic Buyers | Recent cross-border M&A | `"Target - YY, Target - YY, Target - YY"` |
| Sovereign Wealth Funds | Recent direct deals / co-investments | `"Target - YY, Target - YY, Target - YY"` |
| SPACs | Prior de-SPAC targets / announced combinations | `"Target - YY, Target - YY"` |
| Consortium Buyers | Prior consortium transactions | `"Target (with Co-Investor) - YY, Target - YY"` |
| Venture Capital / Growth Equity | Portfolio rounds led/co-led | `"PortCo (Series B) - YY, PortCo (Seed) - YY, PortCo (Series A) - YY"` |
| Litigation Funders | Notable cases / litigations funded | `"Case name - YY, Case name - YY, Case name - YY"` |
| Corporate Venture Arms | Portfolio rounds participated in | `"PortCo (Series B) - YY, PortCo (Seed) - YY"` |
| Any other | Choose the transaction type that most naturally represents the category's activity (deals for acquirers, rounds for investors, cases for funders). If the choice is non-obvious, briefly note the convention used in the Rationale. |

Do not mix transaction types within a single sheet — every row on the Other Buyers tab should use the same transaction convention, so a reader can scan the column without recalibrating.

## Tiering Criteria

| Tier | Target Count | Criteria |
|------|-------------|---------|
| A | 5–10 | Highest strategic/financial fit, proven acquirers in the sector, clear and compelling rationale |
| B | 10–15 | Good fit but less obvious; less active M&A track record or smaller size |
| C | Remainder | Possible but lower probability; include to broaden the process if needed |

Total buyers across all sheets must not exceed **60** (20 strategic + 20 financial + 20 other, maximum per sheet). The Other sheet is optional; it is only populated when `include_other = True`.

**Quality over quantity** — a focused list of 30–50 well-researched buyers beats a list of 200 names.

## Character Limits by Column

### Strategic Buyers

| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars — use common/abbreviated name |
| C | HQ | ~12 chars — e.g., `"Toronto, CA"` |
| D | Vertical | ~12 chars — e.g., `"Wealth Mgmt"` |
| F | M&A activity | Up to 3 deals (~60–80 chars typical) |
| G | Rationale | 1 concise sentence, ~100–230 chars |

### Financial Buyers

| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| F | Sector Focus | ~12 chars |
| G | Portfolio Companies | Up to 3 portcos (~60–80 chars typical) |
| H | Rationale | 1 concise sentence, ~100–230 chars |

### Other Buyers (only when `include_other=True`)

| Column | Field | Limit |
|--------|-------|-------|
| B | Buyer name | ~20 chars |
| C | HQ | ~12 chars |
| D | Vertical | ~12 chars |
| E | Transactions | Up to 3 deals (~60–80 chars typical) |
| F | Rationale | 1 concise sentence, ~100–230 chars |

## Revenue / Fund Size Currency

The template uses **C$ (Canadian dollars)**:
- If source data is in USD, convert at approximate current rate and note the conversion
- Enter revenue as a numeric value (e.g., `450` for C$450MM) — no currency symbols
- Fund size in C$B (e.g., `3.2` for C$3.2B); deal size in C$MM (e.g., `150` for C$150MM)

## Quality Rules

- **30–40 focused buyers** beats 200 names — prioritise fit over volume
- **Research recent M&A** — buyers who just completed a deal in the sector may be hungry for more or temporarily tapped out; flag accordingly in the M&A activity column
- **Antitrust** — flag any direct competitors that may face regulatory scrutiny; note in rationale
- **Fund vintage** — sponsors near end of investment period are more motivated; avoid funds in harvest mode
- **Always ask** if the seller has specific buyers to include or exclude before finalising
