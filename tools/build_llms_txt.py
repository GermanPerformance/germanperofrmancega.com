#!/usr/bin/env python3
"""Write llms.txt: a short map of the site for AI answer engines.

Google ignores the file, but Perplexity, Claude and OpenAI's crawlers (all
allowed in robots.txt) read it as a hint about which pages matter and what
each one is for. It is built from tools/service_catalog.py so it lists
exactly the pages the nav does, plus About, Contact and the one article;
regenerate it whenever the catalogue changes.

Run from the repo root:  python3 tools/build_llms_txt.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import GROUPS, HUBS  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"

INTRO = """# German Performance

> Independent German auto repair in Snellville, Georgia (Gwinnett County),
> family-owned since 2010. BMW, Mercedes-Benz, Audi, Porsche and Volkswagen
> only, diagnosed on each manufacturer's own factory software (ISTA,
> XENTRY, ODIS, PIWIS). Written estimate before any work; 12-month /
> 12,000-mile warranty. 2144 Parkwood Rd NW, Snellville, GA 30078.
> (678) 395-7459. Monday-Friday 9:30 AM-6:00 PM.

Serves Snellville, Loganville, Grayson, Lawrenceville, Stone Mountain and
the rest of Gwinnett County. CARFAX 2025 Top-Rated Service Center, 4.8 stars
on CARFAX, 180+ Google reviews.
"""

INFO = [
    ("about.html", "About", "Who runs the shop, the factory software it runs for each marque, and how a job proceeds"),
    ("contact.html", "Contact", "Address, hours, map, and what to have ready before calling"),
    ("dealer-vs-independent-german-car-repair.html", "Dealer vs. independent", "What changes when you leave the dealer for an independent German specialist"),
]


def link(slug, label, note=""):
    url = f"{SITE}/{slug}" if slug != "index.html#services" else f"{SITE}/"
    return f"- [{label}]({url})" + (f": {note}" if note else "")


def brand_note(brand):
    return "Brand hub: every service the shop performs on that marque" if brand != "All German Makes" \
        else "Services for every German marque"


def body():
    lines = [INTRO, "## Services by marque", ""]
    for brand, pages in GROUPS:
        hub = HUBS.get(brand)
        if hub and hub != "index.html#services":
            lines.append(link(hub, f"{brand} repair and service", brand_note(brand)))
        else:
            lines.append(f"- {brand}")
        for slug, label in pages:
            lines.append(f"  {link(slug, label)}")
        lines.append("")
    lines += ["## About the shop", ""]
    lines += [link(*row) for row in INFO]
    lines += ["", "## Policies", "", link("privacy-policy.html", "Privacy policy"), ""]
    return "\n".join(lines)


def main():
    path = os.path.join(REPO_ROOT, "llms.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body())
    print(f"llms.txt: {sum(len(p) for _, p in GROUPS)} service pages listed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
