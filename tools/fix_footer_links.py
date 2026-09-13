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

# Canonical display names, harvested from the homepage footer so link text
# stays consistent with what already ships.
SERVICES = {
    "bmw-oil-change-snellville-ga.html": "BMW Oil Change",
    "bmw-transmission-repair-snellville-ga.html": "BMW Transmission Repair",
    "bmw-suspension-repair-snellville-ga.html": "BMW Suspension Repair",
    "bmw-cooling-system-repair-snellville-ga.html": "BMW Cooling System",
    "bmw-battery-replacement-snellville-ga.html": "BMW Battery Replacement",
    "bmw-spark-plug-replacement-snellville-ga.html": "BMW Spark Plugs",
    "porsche-oil-change-snellville-ga.html": "Porsche Oil Change",
    "porsche-suspension-repair-snellville-ga.html": "Porsche Suspension Repair",
    "volkswagen-brake-service-snellville-ga.html": "Volkswagen Brake Service",
    "mercedes-cooling-system-snellville-ga.html": "Mercedes Cooling System",
    "mercedes-brake-service-snellville-ga.html": "Mercedes Brake Service",
    "mercedes-engine-diagnostics-snellville-ga.html": "Mercedes Diagnostics",
    "mercedes-oil-change-snellville-ga.html": "Mercedes Oil Change",
    "mercedes-transmission-snellville-ga.html": "Mercedes Transmission",
    "mercedes-suspension-snellville-ga.html": "Mercedes Suspension",
    "mercedes-ac-repair-snellville-ga.html": "Mercedes AC Repair",
    "audi-brake-service-snellville-ga.html": "Audi Brake Service",
    "audi-oil-change-snellville-ga.html": "Audi Oil Change",
    "audi-suspension-repair-snellville-ga.html": "Audi Suspension",
    "porsche-inspection-snellville-ga.html": "Porsche Inspection",
    "porsche-brake-service-snellville-ga.html": "Porsche Brake Service",
    "volkswagen-engine-repair-snellville-ga.html": "VW Engine Repair",
    "volkswagen-oil-change-snellville-ga.html": "VW Oil Change",
    "german-car-ac-repair-snellville-ga.html": "German Car AC Repair",
    "german-car-check-engine-light-snellville.html": "Check Engine Light",
    "german-car-tune-up-snellville-ga.html": "German Car Tune-Up",
    "pre-purchase-inspection-german-car-ga.html": "Pre-Purchase Inspection",
    "german-car-repair-snellville-ga.html": "German Auto Repair",
    "german-car-brake-repair-snellville-ga.html": "German Car Brake Repair",
    "german-car-transmission-repair-snellville-ga.html": "German Car Transmission Repair",
    "german-car-oil-change-snellville-ga.html": "German Car Oil Change",
}

# Pages that apply to every marque -- used as the fallback tier.
UNIVERSAL = [
    "german-car-repair-snellville-ga.html",
    "german-car-brake-repair-snellville-ga.html",
    "german-car-transmission-repair-snellville-ga.html",
    "german-car-oil-change-snellville-ga.html",
    "german-car-tune-up-snellville-ga.html",
    "german-car-ac-repair-snellville-ga.html",
    "german-car-check-engine-light-snellville.html",
    "pre-purchase-inspection-german-car-ga.html",
]

BRANDS = ["bmw", "mercedes", "audi", "porsche", "volkswagen", "german-car", "pre-purchase"]

# Normalise service names so the same job matches across brands, e.g.
# "suspension-repair" (BMW) and "suspension" (Mercedes) are one category.
CATEGORY_ALIASES = [
    ("oil-change", "oil"),
    ("brake", "brakes"),
    ("suspension", "suspension"),
    ("transmission", "transmission"),
    ("ac-repair", "ac"),
    ("engine-repair", "engine"),
    ("engine-diagnostics", "engine"),
    ("cooling-system", "cooling"),
    ("battery", "battery"),
    ("spark-plug", "ignition"),
    ("inspection", "inspection"),
    ("check-engine-light", "engine"),
    ("tune-up", "ignition"),
]


def brand_of(filename):
    return next((b for b in BRANDS if filename.startswith(b)), "german-car")


def category_of(filename):
    return next((cat for key, cat in CATEGORY_ALIASES if key in filename), "general")


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
    column = "".join(f'<a href="{p}">{SERVICES[p]}</a>' for p in picks[:3])
    services_col = (
        '<div class="fc"><div class="fct">Services</div>'
        '<a href="index.html#services">All Services</a>'
        f"{column}</div>"
    )
    flinks = '<div class="flinks">' + "".join(
        f'<a href="{p}">{SERVICES[p]}</a>' for p in picks[3:8]
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
