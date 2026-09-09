#!/usr/bin/env python3
"""Add an in-content "Related Services" block to every service page.

After the footer placeholders were fixed, each service page linked to related
work only from the footer. Footer links are boilerplate and carry noticeably
less weight than a link inside the content, and they sit below the final CTA
where few readers look. This puts the same relationships in the body, just
above the closing call-to-action, where someone who has finished reading about
one job is deciding what else their car needs.

Reuses the ranking from fix_footer_links (same brand first, then the same job
on other marques, then the cross-brand pages) so the two agree.

Run from the repo root:  python3 tools/add_related_services.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix_footer_links import SERVICES, brand_of, related  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRAND_TITLES = {
    "bmw": ("MORE BMW", "SERVICES"),
    "mercedes": ("MORE MERCEDES", "SERVICES"),
    "audi": ("MORE AUDI", "SERVICES"),
    "porsche": ("MORE PORSCHE", "SERVICES"),
    "volkswagen": ("MORE VOLKSWAGEN", "SERVICES"),
}
DEFAULT_TITLE = ("RELATED", "SERVICES")

CSS = """
/* Related services: in-content links between sibling service pages */
.rel-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:40px}
.rel-card{display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:20px 22px;background:var(--steel);border:1px solid rgba(255,255,255,.07);
  text-decoration:none;transition:border-color .2s,background .2s}
.rel-card:hover{border-color:var(--red);background:#232326}
.rel-name{font-family:'DM Sans',sans-serif;font-size:.95rem;color:var(--white);line-height:1.35}
.rel-go{font-family:'Space Mono',monospace;font-size:.9rem;color:var(--red-b);flex-shrink:0}
@media(max-width:600px){.rel-grid{grid-template-columns:1fr}}
"""

MARKER = 'class="rel-grid"'
ANCHOR = '<section style="background:var(--black);padding:80px 60px;text-align:center">'


def build_block(page):
    picks = related(page, limit=6)
    lead, accent = BRAND_TITLES.get(brand_of(page), DEFAULT_TITLE)
    cards = "".join(
        f'    <a href="{p}" class="rel-card">'
        f'<span class="rel-name">{SERVICES[p]}</span>'
        f'<span class="rel-go">&rarr;</span></a>\n'
        for p in picks
    )
    return (
        '<section style="background:var(--carbon)">\n'
        '  <div class="fu"><div class="sl">Keep Your Car Right</div>\n'
        f'  <h2>{lead}<br><span style="color:var(--red)">{accent}</span></h2></div>\n'
        '  <div class="rel-grid fu">\n'
        f'{cards}'
        '  </div>\n'
        '</section>\n'
    )


def main():
    changed = 0
    for page in sorted(SERVICES):
        path = os.path.join(REPO_ROOT, page)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()

        if MARKER in content:
            continue
        if ANCHOR not in content:
            print(f"  !! {page}: closing CTA section not found")
            continue

        idx = content.rindex(ANCHOR)
        content = content[:idx] + build_block(page) + content[idx:]

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        changed += 1

    if changed:
        css_path = os.path.join(REPO_ROOT, "assets", "css", "site.css")
        with open(css_path, encoding="utf-8") as fh:
            existing = fh.read()
        if ".rel-grid{" not in existing:
            with open(css_path, "a", encoding="utf-8") as fh:
                fh.write(CSS)

    print(f"related-services block added to {changed} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
