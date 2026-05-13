---
name: precedents-infor
description: >
  Use this skill when the user invokes /precedents-infor or asks to build a precedent transactions
  table for a company. Researches up to 15 relevant M&A precedent transactions — with a mild
  preference for publicly traded targets at the time of acquisition (where Revenue and EBITDA are
  verifiable from filings), but a closer-comparable private target with disclosed metrics or
  multiples should be selected over a weakly comparable public one. Populates the INFOR Precedents
  Template.
version: 2.10.0
allowed-tools: [Read, Bash, Write, Glob, WebSearch]
---

# INFOR Precedent Transactions Table — Workflow

This skill builds a precedent transactions table by researching up to 15 relevant M&A deals and writing the transaction data into the INFOR Precedents Template (rows 7–21, specific columns only — see the cell map).

Today's date is available from the system context (`currentDate`) — do not shell out to `date`. Template location, outputs folder, and working directory are resolved inline in Step 4.

**Detailed references** (loaded on demand):
- [`references/source-ladder.md`](references/source-ladder.md) — the 4-rung source selection ladder, stub-calc cap, "disclosed" definition, pro-forma rules
- [`references/url-allow-list.md`](references/url-allow-list.md) — allowed source domains, acquiror-domain PR-path rule, the Step 5b Python verification gate, test cases
- [`references/excel-writing.md`](references/excel-writing.md) — cell map, FX conversion rules, formula precedence by rung, comment formats, row trimming

Pure-logic tests for the URL allow-list live in [`test_allow_list.py`](test_allow_list.py) next to this file.

---

## Workflow Steps

### Step 1 — Confirm Company

If the company name or website was not passed with the command, ask:

> "Please provide the name or website of the company you'd like me to build a precedent transactions table for."

Wait for the company before proceeding.

---

### Step 2 — Determine Sector

Identify the **sector / business type** of the target company (e.g., wealth management, insurance, SaaS, industrial). Use WebSearch to confirm if it isn't obvious from the name or website. The sector drives the search queries in Step 3.

---

### Step 3 — Research Up to 15 Precedent Transactions

Search for up to 15 relevant M&A transactions where the **target company** is comparable to the input company.

**Selection priority — comparability first, public targets as a mild tiebreaker.** The strongest precedent is a transaction whose **target business closely resembles the input company** (sector, business model, client segment, asset class, scale). Public-target deals are mildly preferred because their financials are directly verifiable from filings — but a clearly closer-comparable **private** target with disclosed metrics or multiples should be selected over a weakly comparable public one.

Never include a transaction where deal value (TEV) is undisclosed — a blank TEV makes the row unusable for multiple analysis.

**Search strategy — run several targeted queries across both public and private deals:**
- `"[sector] acquisition [year range] public company target 10-K revenue EBITDA"`
- `"[target name] acquired [year] 10-K annual report"` (for known public targets)
- `"[acquiror] acquires [target] press release LTM revenue EBITDA"`
- `"[sector] M&A [year range] disclosed multiples EBITDA revenue"`
- `"[company name] comparable transactions precedents investment banking"`

**Source priority — work the 4-rung ladder top-down for each candidate.** Stop at the first rung that produces a usable figure:

1. **Disclosed LTM $ figure** in the transaction's own sources (deal PR, 8-K, transcript, major news) — preferred for public AND private targets
2. **Disclosed transaction multiple** → derive metric in-cell as `=I{row}/multiple`. Supersedes the filings-stub fallback (rung 3), not merely preferred over it
3. **Calculated LTM stub from target filings** — public-target fallback only. Capped at 2 rows per table (the most token-expensive route)
4. **Disclosed non-LTM private $ figure** — fallback for private targets only; period drift may be months, never years

See [`references/source-ladder.md`](references/source-ladder.md) for the full rung-by-rung guidance, the stub-period formula and worked example, the stub-calc cap and selection rule (with required selection log in the response), the "disclosed" definition, and the pro-forma rules.

**Source domain allow-list — hard gate, in prose AND in code.** URLs cited in any cell comment on column I, J, or K MUST resolve to an allow-listed domain. See [`references/url-allow-list.md`](references/url-allow-list.md) for the full list, the acquiror-domain PR-path rule, and the Python verification snippet (Step 5b). Off-list sources are blocked at save-time.

**Currency:** Use the currency as stated in the original source — when EBITDA / Revenue are written as $ figures (`*C{row}` formulas), they must be in the **same currency** as TEV, matching the ISO 3-letter code entered in column B. The template's column C FX formula converts to the output currency. Multiple-derived J/K cells (`=I{row}/multiple`) are dimensionless and inherit currency from I — do not add `*C{row}`.

- Do not fabricate or estimate financial metrics. If a figure cannot be verified from an allow-listed source after a thorough search, leave the cell blank.
- Aim for at least 80% of selected transactions to have both Revenue and EBITDA populated. The mild public-target preference helps hit this, but do not sacrifice comparability to do so — a tightly-fit private deal with one disclosed metric is more useful than an off-sector public deal with both.

---

### Step 4 — Locate and Copy the Template

Resolve the template via the plugin's shared helper:
```bash
bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Precedents Template.xlsx"
```

Sanitize the company name for use as a filename via the shared helper:
```bash
SANITIZED_COMPANY_NAME=$(bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/sanitize_name.sh" "$COMPANY_NAME")
```

Copy the template to the current working directory:
```bash
TEMPLATE=$(bash "${CLAUDE_PLUGIN_ROOT:-./infor-workflows}/scripts/find_template.sh" "INFOR Precedents Template.xlsx")
OUTPUT="./$SANITIZED_COMPANY_NAME - Precedent Transactions.xlsx"
cp "$TEMPLATE" "$OUTPUT" && echo "COPY_OK" || echo "COPY_FAILED"
```

Confirm the copy succeeded before proceeding.

---

### Step 5 — Write Transaction Data to Excel (openpyxl)

Open the copied file with openpyxl. **Do NOT use `data_only=True`** — preserve all formulas.

Write to the `Sheet1` sheet only. Up to 15 data rows (rows 7–21), specific columns only.

Quick cell map:

| Column | Field | Notes |
|--------|-------|-------|
| B | Input Currency | ISO 3-letter (USD/CAD/GBP/EUR/AUD) |
| E | Announce Date | `datetime.date` |
| F | Target Legal Name | string |
| G | Acquiror Legal Name | string |
| H | HQ Country Code | ISO 2-letter |
| I | Deal Value (TEV) | formula `=raw*C{row}` + Format A comment |
| J | EBITDA | formula by rung + Format A or B comment |
| K | Revenue | formula by rung + Format A or B comment |
| N | Target Description | string, ≤50 chars |

See [`references/excel-writing.md`](references/excel-writing.md) for:
- Full cell map and FX conversion rules
- Formula precedence per rung (rung 1 disclosed $ LTM, rung 2 disclosed multiple, rung 3 calculated stub) with code examples
- Format A (Quote + Source) and Format B (multi-stub labeled lines) comment formats with code examples
- Column N description rules
- Row-trimming snippet for `n < 15` and the averages-row rewrite

**Excel does the math, not you.** Whether the cell value is a single disclosed figure or a stub calc, it must live in a cell formula — never pre-sum the stubs in Python and write a single number for the calculated case.

---

### Step 5b — URL Allow-List Verification

Before saving the workbook, run the URL allow-list verification snippet from [`references/url-allow-list.md`](references/url-allow-list.md). This is the hard gate — a single off-list URL aborts the save with a `ValueError` naming the cell, the URL, and the comment text.

Save the workbook (`wb.save(PATH)`) only after the check passes.

---

### Step 6 — Verify Output

After saving, re-open the file and spot-check:
1. Exactly `n` data rows remain (rows 7 through 7+n-1), each with values in B, E, F, G, H, I, and N. No blank data rows between the last transaction and the averages row.
2. Dates in column E are `datetime.date` objects (not strings)
3. Cells I, J, K start with `=` (formulas, not raw numbers). Tail check by source path:
   - **I** — always ends with `*C{same_row}` (e.g., `=1250*C7`)
   - **J / K from disclosed $ LTM** — single operand ending `*C{same_row}` (e.g., `=85.0*C7`) ✓
   - **J / K from disclosed multiple** — references `I{same_row}` and divides by the multiple (e.g., `=I7/12.5`). **No `*C{row}`** — column I is already in output currency ✓
   - **J / K from calculated stub** — three operands with arithmetic, ending `*C{same_row}` (e.g., `=(17.517+84.720-17.665)*C7`) ✓
   - **J / K from FY-only / disclosed non-LTM private $** — single operand ending `*C{same_row}` ✓
   - What's never valid: a pre-summed scalar where the source path was a stub calc, OR a `*C{row}` tail on a `=I{row}/multiple` formula (would double-apply FX)
4. Every populated I / J / K cell has a `.comment`. Format A for 1-operand formulas (TEV, $ LTM, multiple, FY-only, non-LTM private $): starts with `Quote: "`, blank line, `Source: http...`. Format B for 3-operand stub-calc formulas: exactly 3 `<Period> ($<Value>): <URL>` lines. Format mismatch is a fail.
5. Column N values are all ≤50 characters
6. No values were written to columns C, D, L, M, or any column past N
7. After row deletion, the averages row at `23 - rows_to_drop` references the populated data range correctly — no `#REF!` and the AVERAGE range matches `L7:L{last_data_row}` / `M7:M{last_data_row}`
8. Column C of the remaining data rows is intact (no `#REF!` in any populated row's C cell)
9. **Source-rung consistency.** For each row using a 3-operand stub formula, the response must contain an explicit log stating that no disclosed $ LTM and no disclosed multiple were found in the deal-source documents. A stub calc with no rung-1 / rung-2 search log is a fail — re-do the row with the disclosed value.
10. **All Source URLs in I/J/K comments resolve to allow-listed domains** — re-run the Step 5b check on the saved file as a final audit.
11. **Stub-calc row count.** Count rows whose J or K cell formula matches the 3-operand stub pattern `=(...+...-...)*C{row}` (a row counts **once** even if both J and K use the stub form). The count must be **≤ 2**. On failure: drop the lowest-comparability stub-calc rows until the count is ≤ 2, then re-run the Step 5b URL allow-list verification on the trimmed workbook before saving. Do not replace the dropped rows — the total table simply has fewer rows.

Report any issues found and fix before delivering.

---

### Step 7 — Summary

Report to the user:

1. **Output file:** computer:// link to the saved file
2. **Transactions populated:** list of deals with target, acquiror, deal value, and a `[Public]` or `[Private]` tag for the target's status at announcement
3. **Source mix:** how many public-target vs. private-target rows are included; for any private-target row, briefly note whether financials are directly disclosed or implied from a disclosed multiple
4. **Missing data:** note any EBITDA or Revenue cells left blank due to non-disclosure
5. **Sources:** brief summary of where financial figures were sourced (filings vs. acquiror PRs vs. news)
6. **Reminder:** Open in Excel with the CapIQ add-in active — column C (FX rate) will populate, and columns I/J/K formulas will resolve to output-currency $MM. Columns L/M (multiples) and the averages row (originally row 23, shifted up by however many rows were trimmed) auto-calculate.

---

## Worked Examples — Rung 2 (Disclosed Multiple)

These complement the AvidXchange stub-calc example in [`references/source-ladder.md`](references/source-ladder.md) by showing rung 2 in action.

**Micro Focus / OpenText (announced August 25, 2022).** OpenText's deal press release quotes "6.3x Micro Focus' pro forma TTM adjusted EBITDA" and separately calls out "$400M of run-rate cost savings." The multiple is on standalone Micro Focus (pro forma for divestitures), **not** synergy-inclusive. Correct: `J{row} = "=I{row}/6.3"` with a Format A (Quote + Source) comment. Wrong: a 3-operand stub calc from FY21 + H1 stubs, even though the underlying data is available — rung 2 is required when the multiple is disclosed.

**Citrix / Vista (announced January 31, 2022).** Source quotes "~24.8x LTM EBITDA." Correct: `J{row} = "=I{row}/24.8"` — no `*C{row}`.

---

## Domain Reference

### Template Cell Map — Sheet1

| Cells | Purpose | Notes |
|-------|---------|-------|
| H2 | Output currency (CAD or USD) | Pre-set in template; do not modify |
| B7:B21 | Input currency (ISO code) | **Write here** |
| C7:C21 | FX conversion — CapIQ array formula | **Never overwrite** |
| E7:E21 | Announce date | **Write here** (`datetime.date`) |
| F7:F21 | Target legal name | **Write here** |
| G7:G21 | Acquiror legal name | **Write here** |
| H7:H21 | Target HQ country code (ISO 2-letter) | **Write here** |
| I7:I21 | Deal Value (TEV) | **Write as formula** `=raw*C{row}` + Format A comment |
| J7:J21 | EBITDA (LTM) | **Write as formula.** Preferred `=ltm*C{row}` (disclosed $ LTM). `=I{row}/multiple` (disclosed multiple, no `*C{row}`). Public-target fallback `=(mrq+fy-pyq)*C{row}`. Format A or B comment per rung |
| K7:K21 | Revenue (LTM) | **Write as formula.** Same precedence as EBITDA. Format A or B comment per rung |
| L7:L21 | TEV / EBITDA | **Never overwrite — formula** |
| M7:M21 | TEV / Revenue | **Never overwrite — formula** |
| N7:N21 | Target description (≤50 chars) | **Write here** |
| L23, M23 | Averages of multiples | **Never overwrite — formula** |

### HQ Country Codes — Common Examples

| Country | Code | Country | Code |
|---------|------|---------|------|
| Canada | CA | Australia | AU |
| United States | US | France | FR |
| United Kingdom | GB | Germany | DE |
| Ireland | IE | Netherlands | NL |

### Handling Undisclosed Metrics

- Never include a deal with no deal value — TEV must be populated for the row to be useful
- For both public and private targets, look for a disclosed $ LTM figure in the deal sources first
- If no $ LTM is disclosed but a transaction multiple is, derive the metric in-cell as `=I{row}/multiple`. No `*C{row}`.
- For public targets where neither $ LTM nor a multiple is disclosed, fall back to the stub-period filings calc
- For private targets, write only the metrics that are directly disclosed; leave the rest blank
- Aim for at least 80% of selected transactions to have both Revenue and EBITDA populated
