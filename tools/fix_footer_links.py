#!/usr/bin/env python3
"""Replace the placeholder service-pageN.html links in every service page footer.

The page template shipped with unfilled placeholders (service-page1..5.html),
producing 240 site-wide 404s. Rather than pointing all 30 pages at the same five
services, this builds a per-page related-service list ranked by genuine topical
proximity:

  1. same brand, different service   (BMW oil change -> BMW spark plugs)
  2. same service, different brand   (BMW oil change -> Mercedes oil change)
  3. universal german-car services   (check engine light, tune-up, ...)

Run from the repo root:  python3 tools/fix_footer_links.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import (GROUPS, full_label, make_of, ranking_group,  # noqa: E402
                             service_of, service_pages)
from urls import href_for  # noqa: E402

# Every non-hub page and the name it carries in a mixed list, in catalog
# order: each make's pages in the order its nav column shows them, then
# the make-agnostic pages. The order matters -- within a ranking tier
# related() keeps it, so the footer reads the way the menu does.
SERVICES = {p: full_label(p) for p in service_pages()}

# Pages that apply to every marque -- used as the fallback tier.
UNIVERSAL = [h for h, _ in dict(GROUPS)["All German Makes"]]


def brand_of(filename):
    """The make's key, or "german-car" for a make-agnostic page."""
    return make_of(filename) or "german-car"


def category_of(filename):
    return ranking_group(service_of(filename))


def related(page, limit=8):
    """Related services for one page, ranked by topical proximity.

    A make's page leads with that make's other jobs. A make-agnostic page
    leads with the same job on each make -- the brake page's nearest
    neighbours are the Mercedes, Audi, Porsche and VW brake pages, not the
    other general pages.
    """
    brand, category = brand_of(page), category_of(page)
    others = [p for p in SERVICES if p != page]

    same_brand = [p for p in others if brand_of(p) == brand]
    same_service = [p for p in others if category_of(p) == category and p not in same_brand]
    universal = [p for p in UNIVERSAL if p != page]

    generic = brand == "german-car"
    tiers = ((same_service, same_brand) if generic else (same_brand, same_service))
    ranked, seen = [], {page}
    for tier in (*tiers, universal, others):
        for p in tier:
            if p not in seen:
                seen.add(p)
                ranked.append(p)
    return ranked[:limit]


def build_blocks(page):
    """Return the replacement footer 'Services' column and .flinks row."""
    picks = related(page)
    column = "".join(f'<a href="{href_for(p)}">{SERVICES[p]}</a>' for p in picks[:3])
    services_col = (
        '<div class="fc"><div class="fct">Services</div>'
        '<a href="/#services">All Services</a>'
        f"{column}</div>"
    )
    flinks = '<div class="flinks">' + "".join(
        f'<a href="{href_for(p)}">{SERVICES[p]}</a>' for p in picks[3:8]
    ) + "</div>"
    return services_col, flinks


# The two blocks carrying placeholder hrefs.
SERVICES_COL_RE = re.compile(
    r'<div class="fc"><div class="fct">Services</div>.*?</div>', re.S)
FLINKS_RE = re.compile(r'<div class="flinks">.*?</div>', re.S)


def main():
    changed = 0
    for page in sorted(SERVICES):
        path = os.path.join(REPO_ROOT, page)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()

        services_col, flinks = build_blocks(page)

        content, n_col = SERVICES_COL_RE.subn(lambda _: services_col, content, count=1)
        content, n_fl = FLINKS_RE.subn(lambda _: flinks, content, count=1)

        if (n_col, n_fl) != (1, 1):
            print(f"ERROR: {page}: matched services-col={n_col}, flinks={n_fl} (expected 1,1)")
            return 1

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        changed += 1

    print(f"Rewrote footer links on {changed} service pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
