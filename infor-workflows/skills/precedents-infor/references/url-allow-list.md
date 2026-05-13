# Source Domain Allow-List — Hard Gate

URLs cited in any cell comment on column I, J, or K (both Format A's `Source:` line and every URL in Format B's per-stub list) **MUST** resolve to one of these allow-listed domain families. Sub-domains are OK; suffix-matching applies.

## Allow-Listed Domains

- The **target's** investor relations site (any sub-domain containing `investor` or beginning `ir.`)
- The **acquiror's** investor relations site (same matching rule)
- The **acquiror's parent domain on its press-release path** (see `ACQUIROR_DOMAINS` below)
- `sec.gov` (EDGAR)
- `sedarplus.ca`, `sedar.com` (Canadian filings)
- `bloomberg.com`, `reuters.com`, `wsj.com`, `ft.com`, `theglobeandmail.com`, `financialpost.com`, `spglobal.com`
- `businesswire.com`, `globenewswire.com`, `prnewswire.com` — **only** when carrying the verbatim issuer press release (not when republishing third-party deal-recap copy)

## Acquiror Parent Domain Rule

URLs from the `ACQUIROR_DOMAINS` set below are allow-listed **only** when the URL path contains one of: `/news`, `/press-release`, `/press-releases`, `/investor`, `/investors`, `/announcements`, `/newsroom`. This admits verbatim issuer press releases hosted on the parent corporate domain (where the IR sub-domain rule above does not match — e.g., `abc.xyz/investor/news/...`, `tpg.com/news-and-insights/...`, `permira.com/news-and-insights/announcements/...`, `cppinvestments.com/newsroom/...`) while excluding portfolio pages, blog posts, and other off-PR content from the same domains.

```
ACQUIROR_DOMAINS = {
    "thomabravo.com", "vistaequitypartners.com", "permira.com", "tpg.com",
    "silverlake.com", "franciscopartners.com", "hf.com", "adventinternational.com",
    "cppinvestments.com", "gic.com.sg", "crosspointcapital.com",
    "evergreencoastcapital.com", "elliottmgmt.com",
    "abc.xyz", "google.com", "microsoft.com", "oracle.com", "broadcom.com", "cisco.com",
}
PR_PATH_KEYWORDS = ("/news", "/press-release", "/press-releases",
                    "/investor", "/investors", "/announcements", "/newsroom")
```

## What's Excluded

Any other domain is **non-reputable** and may not be cited as the primary source for any $ figure or multiple in columns I, J, or K. Domains in `ACQUIROR_DOMAINS` are exempted **only** on PR-keyword paths (above); off-list analyst blogs and deal-recap sites remain excluded regardless of path. This explicitly excludes (non-exhaustive): mergersight.com, eresearch.com, financierworldwide.com, tipranks.com, marketscreener.com, channelfutures.com, channele2e.com, techcrunch.com, cnbc.com, cnet.com, growjo.com, last10k.com, fintel.io, mlq.ai, substack.com, medium.com, linkedin.com/pulse, and any analyst-blog or deal-recap site.

If the only available source for a figure is off-list: (a) keep searching primary sources, (b) fall to a lower rung (e.g., the public-target filings stub calc), or (c) drop the deal. **Never write the cell using the off-list source.**

## Programmatic Verification (Step 5b)

Before saving the workbook, programmatically verify that every URL cited in an I/J/K comment resolves to an allow-listed domain. This is the hard gate — a single off-list URL aborts the save. Run this snippet **between** the trim-empty-rows block and `wb.save(PATH)`:

```python
import re
from urllib.parse import urlparse

ALLOW_DOMAINS = {
    "sec.gov",
    "sedarplus.ca", "sedar.com",
    "bloomberg.com", "reuters.com", "wsj.com", "ft.com",
    "theglobeandmail.com", "financialpost.com", "spglobal.com",
    "businesswire.com", "globenewswire.com", "prnewswire.com",
}

ACQUIROR_DOMAINS = {
    "thomabravo.com", "vistaequitypartners.com", "permira.com", "tpg.com",
    "silverlake.com", "franciscopartners.com", "hf.com", "adventinternational.com",
    "cppinvestments.com", "gic.com.sg", "crosspointcapital.com",
    "evergreencoastcapital.com", "elliottmgmt.com",
    "abc.xyz", "google.com", "microsoft.com", "oracle.com", "broadcom.com", "cisco.com",
}
PR_PATH_KEYWORDS = ("/news", "/press-release", "/press-releases",
                    "/investor", "/investors", "/announcements", "/newsroom")

URL_RE = re.compile(r"https?://\S+")
last_data_row = 7 + n - 1   # n = number_of_transactions_written
urls_checked = 0

for row in range(7, last_data_row + 1):
    for col in ("I", "J", "K"):
        cell = ws[f"{col}{row}"]
        if cell.comment is None:
            continue
        text = cell.comment.text or ""
        for raw_url in URL_RE.findall(text):
            url = raw_url.rstrip(').,;]>"\'')
            parsed = urlparse(url)
            host = (parsed.hostname or "").lower()
            path = (parsed.path or "").lower()
            if not host:
                raise ValueError(
                    f"{col}{row}: unparseable URL {url!r}\nComment: {text!r}"
                )
            allow_listed = any(host == d or host.endswith("." + d) for d in ALLOW_DOMAINS)
            ir_site = ("investor" in host) or host.startswith("ir.") or (".ir." in host)
            acquiror_pr = (
                any(host == d or host.endswith("." + d) for d in ACQUIROR_DOMAINS)
                and any(kw in path for kw in PR_PATH_KEYWORDS)
            )
            if not (allow_listed or ir_site or acquiror_pr):
                raise ValueError(
                    f"{col}{row}: off-list source domain {host!r} in URL {url!r}\n"
                    f"Comment: {text!r}"
                )
            urls_checked += 1

print(f"URL allow-list verification: PASSED ({urls_checked} URLs checked)")
```

## How the Gate Works

- Walks every cell in `I7:K{last_data_row}` that has a `.comment`.
- Extracts every URL from the comment text via `re.findall(r"https?://\S+", text)`, stripping common trailing punctuation.
- Suffix-matches each URL's hostname against the hard-coded `ALLOW_DOMAINS` set (so `www.sec.gov` matches `sec.gov`).
- Additionally accepts any host containing `investor` or beginning `ir.` / containing `.ir.` as an investor-relations subdomain (target/acquiror IR sites vary in shape).
- Additionally accepts hosts in `ACQUIROR_DOMAINS` **only when** the URL path contains a PR keyword. A bare `tpg.com/portfolio/...` URL fails; `tpg.com/news-and-insights/...` passes.
- On any URL whose host doesn't match, raises `ValueError` with the cell reference, the offending URL, and the full comment text — **the workbook does not save.** Re-source that cell from an allow-listed domain (or drop the row) and re-run.
- On success, prints `URL allow-list verification: PASSED (n URLs checked)`.

## Test Cases — Must Pass / Must Fail

| Result | URL | Why |
|---|---|---|
| PASS | `https://abc.xyz/investor/news/2022/0308/` | Acquiror domain + `/investor` and `/news` in path |
| PASS | `https://www.tpg.com/news-and-insights/new-relic-be-acquired-francisco-partners-and-tpg-65-billion` | Acquiror domain + `/news` in path |
| PASS | `https://www.permira.com/news-and-insights/announcements/mcafee-to-be-acquired-by-an-investor-group-for-over-14-billion` | Acquiror domain + `/news` and `/announcements` in path |
| PASS | `https://www.cppinvestments.com/newsroom/qualtrics-to-be-acquired-by-silver-lake-and-cpp-investments-for-12-5-billion/` | Acquiror domain + `/newsroom` in path |
| FAIL | `https://www.tpg.com/portfolio/example-portco/` | Acquiror domain but no PR keyword in path |
| FAIL | `https://mergersight.com/post/some-recap` | Off-list domain regardless of path |

The unit tests for this gate live in [`test_allow_list.py`](../test_allow_list.py) next to the SKILL.md.

Save the workbook (`wb.save(PATH)`) only after the check passes.
