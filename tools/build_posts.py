#!/usr/bin/env python3
"""Build the supporting articles and the guides index from tools/posts/.

Each article renders on the blog skeleton: the nav, mobile menu, footer
and scripts are scraped from the hand-written dealer-vs-independent page
(the DONOR), the stylesheet link and critical block come from the tool
that owns them, and the footer is neutralised the way About and Contact
are, so it links the five brand hubs rather than one marque's services.
The closing call-to-action block is the donor's, verbatim, plus one link
to the money page the article supports.

Every article carries a byline with its dates (from posts.POST_DATES), a
Sources list when it cites anything outside the site, and the closing
note about who wrote it. guides.html lists every article, grouped by the
page it supports, so the nav has one place to point at.

Run from the repo root:  python3 tools/build_posts.py
Then tools/apply_redesign.py (top bar, footer columns, version stamps),
tools/build_social_tags.py and tools/build_schema.py (BlogPosting, dated
from posts.POST_DATES).
"""

import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_info_pages import neutral_footer  # noqa: E402
from page_chrome import stylesheets  # noqa: E402
from posts import (  # noqa: E402
    AUTHOR_NOTE, DEALER, GUIDES, GUIDES_PAGE, HOME_PAGE, POST_DATES, POSTS, READING,
    SERVICES, SUMMARY,
)
from service_catalog import full_label  # noqa: E402
from urls import SITE, href_for, page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONOR = DEALER
AUTHOR = "By the technicians at German Performance"

GUIDES_TITLE = "German Car Repair Guides | German Performance"
GUIDES_DESCRIPTION = (
    "Repair and maintenance guides for BMW, Mercedes-Benz and other German cars, "
    "written by the technicians at German Performance in Snellville, GA.")
GUIDES_INTRO = (
    "What we have learned from more than 10,000 German cars, written down. "
    "Each guide supports one of our repair pages: what to maintain, how we "
    "diagnose a symptom, what moves a bill, and jobs from our own bays. No "
    "prices are quoted anywhere; a written estimate after a diagnosis is the "
    "only honest number.")


def skeleton():
    with open(os.path.join(REPO_ROOT, DONOR), encoding="utf-8") as fh:
        src = fh.read()

    def grab(pattern):
        match = re.search(pattern, src, re.S)
        if not match:
            raise SystemExit(f"{DONOR}: no match for {pattern[:44]}")
        return match.group(0)

    return {
        "nav": grab(r"<nav.*?</nav>"),
        "mob": grab(r'<div id="mobile-menu".*?\n</div>'),
        "footer": neutral_footer(grab(r"<footer>.*?</footer>")),
        "css": stylesheets("post"),
        "scripts": "\n".join(
            re.findall(r'<script defer src="assets/js/[^"]+"></script>', src)),
        # The donor's closing block, minus its heading and line: the
        # button and the trust row are the parts every article shares.
        "cta_tail": grab(r'<div class="cta-col">\s*<a href="tel:.*?</div>\s*</div>\s*</div>'),
    }


# -- blocks -------------------------------------------------------------------

def table_html(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "\n".join(
        "      <tr>" + f"<th>{row[0]}</th>" + "".join(f"<td>{cell}</td>" for cell in row[1:]) + "</tr>"
        for row in rows)
    return (f'  <div class="table-scroll"><table class="spec-table">\n'
            f"    <thead><tr>{head}</tr></thead>\n    <tbody>\n{body}\n    </tbody>\n"
            f"  </table></div>")


def block_html(block):
    if isinstance(block, str):
        return f"  <p>{block}</p>"
    kind, body = block
    if kind == "callout":
        return f'  <div class="callout">{body}</div>'
    if kind == "h3":
        return f"  <h3>{body}</h3>"
    if kind == "table":
        return table_html(*body)
    if kind == "list":
        items = "\n".join(f"    <li>{item}</li>" for item in body)
        return f'  <ul class="checklist">\n{items}\n  </ul>'
    raise SystemExit(f"build_posts: unknown block kind {kind!r}")


def sections_html(sections):
    parts = []
    for heading, blocks in sections:
        parts.append(f"  <h2>{heading}</h2>")
        parts.extend(block_html(b) for b in blocks)
        parts.append("")
    return "\n".join(parts).rstrip()


def pretty_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def byline_html(slug):
    published, modified = POST_DATES[slug]
    line = f'{AUTHOR} &middot; <time datetime="{published}">{pretty_date(published)}</time>'
    if modified != published:
        line += f' &middot; Updated <time datetime="{modified}">{pretty_date(modified)}</time>'
    return f'  <p class="byline">{line}</p>'


def sources_html(sources):
    if not sources:
        return ""
    items = "\n".join(
        f'    <li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>'
        for label, url in sources)
    return f'  <h2>Sources</h2>\n  <ul class="sources">\n{items}\n  </ul>\n\n'


def further_html(slugs):
    items = "\n".join(
        f'    <li><a href="{href_for(slug)}">{READING[slug]}</a></li>' for slug in slugs)
    return f"  <h2>Further reading</h2>\n  <ul class=\"checklist\">\n{items}\n  </ul>"


def hub_link(hub):
    """The one link every article carries to the money page it supports."""
    if hub == HOME_PAGE:
        return f'<a href="{SERVICES}">Every service we perform</a>'
    return f'<a href="{href_for(hub)}">{full_label(hub)} in Snellville, GA</a>'


def cta_html(post, tail):
    return (f'  <div class="cta-block">\n    <h2>{post["cta_heading"]}</h2>\n'
            f'    <p>{post["cta_text"]}</p>\n'
            f'    <p class="cta-link">{hub_link(post["hub"])}</p>\n    {tail}')


# -- pages --------------------------------------------------------------------

def page(sk, title, description, slug, body, page_type="post"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{page_url(slug)}">
{sk['css']}
</head>
<body data-page-type="{page_type}">

{sk['nav']}
{sk['mob']}

<main>
<div class="wrap">

{body}

</div>
</main>
{sk['footer']}

{sk['scripts']}
</body>
</html>
"""


def build(post, sk):
    body = f"""  <div class="eyebrow"><span>{post['eyebrow']}</span></div>
  <h1>{post['h1']}</h1>
  <p class="dek">{post['dek']}</p>
{byline_html(post['slug'])}

  <p>{post['intro']}</p>

{sections_html(post['sections'])}

{sources_html(post['sources'])}  <div class="callout">{AUTHOR_NOTE}</div>

{further_html(post['further'])}

{cta_html(post, sk['cta_tail'])}"""
    return page(sk, post["title"], post["description"], post["slug"], body)


def guides_group(heading, hub, slugs):
    items = "\n".join(
        f'    <li><h3><a href="{href_for(slug)}">{READING[slug]}</a></h3><p>{SUMMARY[slug]}</p></li>'
        for slug in slugs)
    return (f"  <h2>{heading}</h2>\n  <p>Guides that support {hub_link(hub).replace('Every service we perform', 'the services we perform')}.</p>\n"
            f'  <ul class="guide-list">\n{items}\n  </ul>')


def build_guides(sk):
    groups = "\n\n".join(guides_group(*g) for g in GUIDES if g[2])
    body = f"""  <div class="eyebrow"><span>From the Technicians</span></div>
  <h1>German Car <span class="accent">Repair Guides</span></h1>
  <p class="dek">{GUIDES_INTRO}</p>

{groups}

  <div class="callout">{AUTHOR_NOTE}</div>

  <div class="cta-block">
    <h2>Have a question the guides do not answer?</h2>
    <p>Call with the year, the model and the symptom. We will tell you what we would check first.</p>
    <p class="cta-link">{hub_link(HOME_PAGE)}</p>
    {sk['cta_tail']}"""
    return page(sk, GUIDES_TITLE, GUIDES_DESCRIPTION, GUIDES_PAGE, body, page_type="info")


def write(slug, html):
    path = os.path.join(REPO_ROOT, slug)
    existed = os.path.exists(path)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"{'updated' if existed else 'wrote'} {slug} ({len(html):,} bytes)")


def main():
    sk = skeleton()
    for post in POSTS:
        write(post["slug"], build(post, sk))
    write(GUIDES_PAGE, build_guides(sk))
    return 0


if __name__ == "__main__":
    sys.exit(main())
