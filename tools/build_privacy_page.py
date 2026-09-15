#!/usr/bin/env python3
"""Build the privacy policy page.

Google's advertising policies require a reachable privacy policy on any
site that carries its conversion tags, and the site is about to carry two:
GA4 and the Google Ads call-conversion tag, which for ad visitors swaps
the shop's number for a Google forwarding number. That last part is the
one thing a caller might reasonably want explained, so the page says it
in plain words rather than in a template's.

The page is built from the blog post's skeleton, not the info pages': a
policy is prose, and post.css already sets a 720px reading measure with
ruled headings. The footer is neutralised the same way About and Contact
are, so it links the five brand hubs rather than one marque's services.

Every fact here is already on the site or in analytics.js: no forms, the
two Google tags, the Maps embeds on the homepage and contact page, the shop's
address and number. Nothing about data practices is invented — the site
has none beyond what the tags do.

Not legal advice. The owner reads it before it goes live.

Run from the repo root:  python3 tools/build_privacy_page.py
Then tools/apply_redesign.py (adds the top bar and footer seal) and
tools/build_schema.py (the WebPage graph).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_info_pages import neutral_footer  # noqa: E402
from urls import page_url  # noqa: E402
from page_chrome import stylesheets  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONOR = "dealer-vs-independent-german-car-repair.html"
SLUG = "privacy-policy.html"
EFFECTIVE = "September 12, 2026"

TITLE = "Privacy Policy | German Performance"
DESC = ("What germanperformancega.com collects and why: no forms, Google "
        "Analytics for usage, Google Ads to measure calls from ads, and how "
        "to opt out.")

# (heading, [blocks]) — a block is a paragraph string, or a ("list", [...])
# or ("callout", "...") tuple. Kept as data so the wording is easy to read
# and edit without touching the markup.
SECTIONS = [
    ("What this site collects", [
        "Nothing you type. There are no forms, accounts, logins or "
        "newsletters on this site; the only thing it asks you to do is "
        "call. Two kinds of information are collected automatically:",
        ("list", [
            "<strong>Usage analytics (Google Analytics).</strong> Which "
            "pages were viewed, roughly where the visit came from (city-"
            "level, from the IP address), the device and browser, how you "
            "arrived, and whether the phone number or the directions link "
            "was tapped. Google Analytics sets cookies named _ga "
            "and _ga_… to tell one visit from the next.",
            "<strong>Advertising measurement (Google Ads).</strong> If you "
            "reached the site by clicking one of our Google ads, Google "
            "sets a cookie (_gcl_aw) so that a call or a tap on "
            "the number can later be credited to that ad. This tells us "
            "which ads bring in work; it is not used to build a profile "
            "of you.",
        ]),
        "Neither tool tells us who you are. We see counts and patterns, "
        "not names.",
    ]),
    ("Calls from our ads", [
        ("callout",
         "If you arrived from a Google ad, the phone number shown on the "
         "page may be a <strong>Google forwarding number</strong> that "
         "rings straight through to the shop. It works exactly like our "
         "own number."),
        "When a call comes through a forwarding number, Google records "
        "when it started, how long it lasted and the caller's phone number, "
        "and reports that to us as part of the advertising account so we "
        "know the ad led to a real conversation. Google does not record "
        "the call itself, and neither do we. Calls placed to "
        "(678) 395-7459 directly are ordinary phone calls and are not "
        "measured by Google at all.",
    ]),
    ("Services from other companies", [
        "A few parts of the site are provided by other companies, and "
        "their own privacy policies apply to what they receive:",
        ("list", [
            "<strong>Google Analytics and Google Ads</strong> — the "
            "measurement described above. Google's policy is at "
            '<a href="https://policies.google.com/privacy" rel="noopener" '
            'target="_blank">policies.google.com/privacy</a>.',
            "<strong>Google Maps</strong> — the maps on the homepage and "
            "the contact page are embedded from Google, which may set its "
            "own cookies when they load.",
            "<strong>CARFAX and Instagram</strong> — linked, not embedded. "
            "Nothing is sent to them until you follow the link.",
        ]),
    ]),
    ("What we do not do", [
        "We do not sell or rent visitor information, share it with data "
        "brokers, or use it for anything beyond running the shop and "
        "measuring its advertising. We collect no email addresses from "
        "this site and send no marketing email. Job records for cars we "
        "work on are kept at the shop as ordinary business records and "
        "are unrelated to your visit here.",
    ]),
    ("Your choices", [
        ("list", [
            "<strong>Cookies.</strong> Your browser can block or clear "
            "cookies for this site; everything on it still works without "
            "them.",
            "<strong>Analytics.</strong> Google's opt-out add-on at "
            '<a href="https://tools.google.com/dlpage/gaoptout" '
            'rel="noopener" target="_blank">tools.google.com/dlpage/gaoptout'
            "</a> stops Google Analytics on every site.",
            "<strong>Advertising.</strong> Ad personalisation is controlled "
            'at <a href="https://adssettings.google.com" rel="noopener" '
            'target="_blank">adssettings.google.com</a>. Our ads only '
            "measure; they do not follow you around the web.",
            "<strong>Calling.</strong> If you would rather not call through "
            "a forwarding number, dial (678) 395-7459 directly.",
        ]),
    ]),
    ("How long it is kept", [
        "Analytics data is kept by Google for up to 14 months and then "
        "deleted; advertising call details are kept for as long as Google "
        "Ads retains them, which is a matter of weeks. We keep no separate "
        "database of website visitors.",
    ]),
    ("Children", [
        "The site is for car owners and is not directed at children under "
        "13. We do not knowingly collect information from them.",
    ]),
    ("Changes", [
        f"If the site starts collecting anything new, this page changes "
        f"first and the date at the top changes with it. Current version: "
        f"{EFFECTIVE}.",
    ]),
    ("Questions", [
        "Ask the people who answer the phone. German Performance, "
        "2144 Parkwood Rd NW, Snellville, GA 30078 — "
        '<a href="tel:+16783957459">(678) 395-7459</a>, Monday to Friday, '
        "9:30 AM to 6 PM.",
    ]),
]


def skeleton():
    src = open(os.path.join(REPO_ROOT, DONOR), encoding="utf-8").read()

    def grab(pattern):
        match = re.search(pattern, src, re.S)
        if not match:
            raise SystemExit(f"{DONOR}: no match for {pattern[:44]}")
        return match.group(0)

    return {
        "nav": grab(r"<nav.*?</nav>"),
        "mob": grab(r'<div id="mobile-menu".*?\n</div>'),
        "footer": neutral_footer(grab(r"<footer>.*?</footer>")),
        # Not scraped: the inline critical block and the one bundle link,
        # from the tool that owns them (the privacy page is a post-sheet page).
        "css": stylesheets("post"),
        "scripts": "\n".join(
            re.findall(r'<script defer src="assets/js/[^"]+"></script>', src)),
    }


def block_html(block):
    if isinstance(block, str):
        return f"  <p>{block}</p>"
    kind, body = block
    if kind == "callout":
        return f'  <div class="callout"><p>{body}</p></div>'
    items = "\n".join(f"    <li>{item}</li>" for item in body)
    return f'  <ul class="checklist">\n{items}\n  </ul>'


def sections_html():
    parts = []
    for heading, blocks in SECTIONS:
        parts.append(f"  <h2>{heading}</h2>")
        parts.extend(block_html(b) for b in blocks)
        parts.append("")
    return "\n".join(parts).rstrip()


def build(sk):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{page_url(SLUG)}">
{sk['css']}
</head>
<body data-page-type="info">

{sk['nav']}
{sk['mob']}

<main>
<div class="wrap">

  <div class="eyebrow"><span>Effective {EFFECTIVE}</span></div>
  <h1>Privacy <span class="accent">Policy</span></h1>
  <p class="dek">German Performance is a repair shop, not a data business. This page says what the website collects, which is little, and what happens when you call from one of our ads.</p>

{sections_html()}

</div>
</main>
{sk['footer']}

{sk['scripts']}
</body>
</html>
"""


def main():
    html = build(skeleton())
    path = os.path.join(REPO_ROOT, SLUG)
    existed = os.path.exists(path)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"{'updated' if existed else 'wrote'} {SLUG} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
