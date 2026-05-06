"""Tests for the precedents-infor URL allow-list gate.

Mirrors the verification logic in SKILL.md Step 5b. If SKILL.md and this file
diverge, treat SKILL.md as authoritative and update this file to match.
"""

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


def is_allowed(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = (parsed.path or "").lower()
    if not host:
        return False
    allow_listed = any(host == d or host.endswith("." + d) for d in ALLOW_DOMAINS)
    ir_site = ("investor" in host) or host.startswith("ir.") or (".ir." in host)
    acquiror_pr = (
        any(host == d or host.endswith("." + d) for d in ACQUIROR_DOMAINS)
        and any(kw in path for kw in PR_PATH_KEYWORDS)
    )
    return allow_listed or ir_site or acquiror_pr


CASES = [
    (True,  "https://abc.xyz/investor/news/2022/0308/"),
    (True,  "https://www.tpg.com/news-and-insights/new-relic-be-acquired-francisco-partners-and-tpg-65-billion"),
    (True,  "https://www.permira.com/news-and-insights/announcements/mcafee-to-be-acquired-by-an-investor-group-for-over-14-billion"),
    (True,  "https://www.cppinvestments.com/newsroom/qualtrics-to-be-acquired-by-silver-lake-and-cpp-investments-for-12-5-billion/"),
    (False, "https://www.tpg.com/portfolio/example-portco/"),
    (False, "https://mergersight.com/post/some-recap"),
]


def main() -> int:
    failures = 0
    for expected, url in CASES:
        actual = is_allowed(url)
        label = "PASS" if expected else "FAIL"
        ok = actual == expected
        marker = "OK" if ok else "MISMATCH"
        print(f"[{marker}] expected={label:<4} got={'PASS' if actual else 'FAIL':<4}  {url}")
        if not ok:
            failures += 1

    print()
    if failures:
        print(f"{failures} of {len(CASES)} cases failed")
        return 1
    print(f"All {len(CASES)} cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
