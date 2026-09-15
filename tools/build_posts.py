#!/usr/bin/env python3
"""Build the supporting articles from tools/posts.py.

Each article renders on the blog skeleton: the nav, mobile menu, footer
and scripts are scraped from the hand-written dealer-vs-independent page
(the DONOR), the stylesheet link and critical block come from the tool
that owns them, and the footer is neutralised the way About and Contact
are, so it links the five brand hubs rather than one marque's services.
The closing call-to-action block is the donor's, verbatim, so the three
articles end the same way.

Run from the repo root:  python3 tools/build_posts.py
Then tools/apply_redesign.py (top bar, footer columns, version stamps),
tools/build_social_tags.py and tools/build_schema.py (BlogPosting, dated
from posts.POST_DATES).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_info_pages import neutral_footer  # noqa: E402
from page_chrome import stylesheets  # noqa: E402
from posts import AUTHOR_NOTE, DEALER, POSTS, READING  # noqa: E402
from urls import SITE, href_for, page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONOR = DEALER


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


def block_html(block):
    if isinstance(block, str):
        return f"  <p>{block}</p>"
    kind, body = block
    if kind == "callout":
        return f'  <div class="callout">{body}</div>'
    items = "\n".join(f"    <li>{item}</li>" for item in body)
    return f'  <ul class="checklist">\n{items}\n  </ul>'


def sections_html(sections):
    parts = []
    for heading, blocks in sections:
        parts.append(f"  <h2>{heading}</h2>")
        parts.extend(block_html(b) for b in blocks)
        parts.append("")
    return "\n".join(parts).rstrip()


def further_html(slugs):
    items = "\n".join(
        f'    <li><a href="{href_for(slug)}">{READING[slug]}</a></li>' for slug in slugs)
    return f"  <h2>Further reading</h2>\n  <ul class=\"checklist\">\n{items}\n  </ul>"


def cta_html(post, tail):
    return (f'  <div class="cta-block">\n    <h2>{post["cta_heading"]}</h2>\n'
            f'    <p>{post["cta_text"]}</p>\n    {tail}')


def build(post, sk):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{post['title']}</title>
<meta name="description" content="{post['description']}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{page_url(post['slug'])}">
{sk['css']}
</head>
<body data-page-type="post">

{sk['nav']}
{sk['mob']}

<main>
<div class="wrap">

  <div class="eyebrow"><span>{post['eyebrow']}</span></div>
  <h1>{post['h1']}</h1>
  <p class="dek">{post['dek']}</p>

  <p>{post['intro']}</p>

{sections_html(post['sections'])}

  <div class="callout">{AUTHOR_NOTE}</div>

{further_html(post['further'])}

{cta_html(post, sk['cta_tail'])}

</div>
</main>
{sk['footer']}

{sk['scripts']}
</body>
</html>
"""


def main():
    sk = skeleton()
    for post in POSTS:
        html = build(post, sk)
        path = os.path.join(REPO_ROOT, post["slug"])
        existed = os.path.exists(path)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"{'updated' if existed else 'wrote'} {post['slug']} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
