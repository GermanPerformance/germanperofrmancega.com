#!/usr/bin/env python3
"""Write llms.txt: a short map of the site for AI answer engines.

Google ignores the file, but Perplexity, Claude and OpenAI's crawlers (all
allowed in robots.txt) read it as a hint about which pages matter and what
each one is for. It is built from tools/service_catalog.py so it lists
exactly the pages the nav does, plus the guides (tools/posts/), About
and Contact;
regenerate it whenever the catalogue changes.

Run from the repo root:  python3 tools/build_llms_txt.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from posts import GUIDES_PAGE, HOME_PAGE, READING, SUMMARY, guides_for  # noqa: E402
from service_catalog import GENERIC_GROUP, GENERIC_HUB, GROUPS, MAKES  # noqa: E402
from urls import SITE, page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
]

HUB_NOTE = "Brand hub: what the shop sees on that marque, every service it performs on it, and its guides"


def link(slug, label, note=""):
    url = f"{SITE}/" if slug == GENERIC_HUB else page_url(slug)
    return f"- [{label}]({url})" + (f": {note}" if note else "")


def guide_lines(hub, indent="  "):
    return [f"{indent}{link(slug, READING[slug], SUMMARY[slug])}" for slug in guides_for(hub)]


def body():
    columns = dict(GROUPS)
    lines = [INTRO, "## Services", "", "Services for every German marque:", ""]
    lines += [link(slug, label) for slug, label in columns[GENERIC_GROUP]]
    lines += ["", "## Makes", ""]
    for m in MAKES:
        lines.append(link(m.hub, f"{m.heading} repair", HUB_NOTE))
        lines += [f"  {link(slug, label)}" for slug, label in columns.get(m.heading, ())]
        lines += guide_lines(m.hub)
    lines += ["", "## Guides", "",
              link(GUIDES_PAGE, "German car repair guides",
                   "Every guide, grouped by the repair page it supports"),
              *guide_lines(HOME_PAGE, indent="")]
    lines += ["", "## About the shop", ""]
    lines += [link(*row) for row in INFO]
    lines += ["", "## Policies", "", link("privacy-policy.html", "Privacy policy"), ""]
    return "\n".join(lines)


def main():
    path = os.path.join(REPO_ROOT, "llms.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body())
    print(f"llms.txt: {sum(len(p) for _, p in GROUPS)} service pages, "
          f"{len(READING)} guides listed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
