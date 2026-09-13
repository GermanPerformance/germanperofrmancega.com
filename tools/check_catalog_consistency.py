#!/usr/bin/env python3
"""Every service page is named the way the catalog names it.

tools/service_catalog.py decides what each page is called -- "BMW Oil
Change", "Mercedes Brake Repair", "Tune-Up" -- and the nav, hubs, footer
and breadcrumbs are generated from it. The page's own <title> and <h1>
are not generated on the hand-written pages, so they can drift: "Brake
Service" in the heading under "Brake Repair" in the menu, "VW" in the
title under "Volkswagen" in the column. This checks, for every catalog
page:

  - the title and the h1 carry the catalog name (make and job for a make's
    page, the job for a make-agnostic one; the h1 may drop a leading
    "Auto", a hub may use its column heading, and a hub title may add the
    short form in brackets)
  - a make's page has a three-step breadcrumb under its hub, everything
    else two
  - the canonical is the page's own URL and the description fits a result
  - data-page-type says hub on a hub and service elsewhere
  - the nav on the page lists the whole catalog (a stale regeneration)

Run from the repo root:  python3 tools/check_catalog_consistency.py
Exit 1 with one line per problem.
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import service_catalog as cat  # noqa: E402
from fix_breadcrumbs import breadcrumb  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"
DESCRIPTION_MAX = 160

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')
PAGE_TYPE_RE = re.compile(r'<body[^>]*data-page-type="([^"]+)"')
NAV_RE = re.compile(r"(<nav>.*?</nav>)", re.S)
CRUMB_RE = re.compile(r'<div class="breadcrumb">(.*?)</div>')

_HUBS = {m.hub: m for m in cat.MAKES}
_MAKES = {m.key: m for m in cat.MAKES}
_GENERIC_PREFIX = re.compile(r"^German (?:Car )?")


def expected_name(slug):
    """What the title and h1 must carry."""
    label = cat.full_label(slug)
    return label if cat.make_of(slug) else _GENERIC_PREFIX.sub("", label)


def name_pattern(slug):
    """The name as a regex: a hub may use the column heading, and its
    title may add the short form in brackets ("Volkswagen (VW) Repair")."""
    make = cat.make_of(slug)
    name = expected_name(slug)
    if not make:
        return re.escape(name)
    m = _MAKES[make]
    job = re.escape(name[len(m.short) + 1:])
    return rf"(?:{re.escape(m.short)}|{re.escape(m.heading)})(?: \([A-Z]+\))? {job}"


def h1_text(fragment):
    text = re.sub(r"<br\b[^>]*>", " ", fragment)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\s+", " ", text).strip()


def _first(pattern, content):
    m = pattern.search(content)
    return m.group(1) if m else ""


def check_breadcrumb(slug, content):
    """A make's page carries the catalog's three-step trail exactly; a hub
    or a make-agnostic page keeps its own two-step crumb (Home, then the
    page), whatever it chooses to call itself."""
    if cat.hub_for(slug) and slug not in _HUBS:
        if breadcrumb(slug) not in content:
            yield "breadcrumb is not the catalog's three-step trail under the hub"
        return
    block = _first(CRUMB_RE, content)
    if block.count("<a ") != 1 or 'class="crumb-here"' not in block:
        yield "breadcrumb should be two steps: Home, then this page"


def check_page(slug, content):
    pattern = name_pattern(slug)
    title = html.unescape(_first(TITLE_RE, content)).strip()
    if not re.search(pattern, title):
        yield f'title "{title}" does not carry "{expected_name(slug)}"'

    h1 = h1_text(_first(H1_RE, content))
    h1_pattern = re.sub(r"^\(\?:", "(?:", pattern)
    h1_pattern = h1_pattern.replace(re.escape("Auto "), "(?:Auto )?", 1)
    if not re.search(h1_pattern, h1, re.I):
        yield f'h1 "{h1}" does not carry "{expected_name(slug)}"'

    yield from check_breadcrumb(slug, content)

    desc = _first(DESC_RE, content)
    if not desc:
        yield "description missing"
    elif len(desc) > DESCRIPTION_MAX:
        yield f"description is {len(desc)} characters (max {DESCRIPTION_MAX})"

    canonical = _first(CANONICAL_RE, content)
    if canonical != f"{SITE}/{slug}":
        yield f'canonical "{canonical}" is not this page'

    kind = "hub" if slug in _HUBS else "service"
    if _first(PAGE_TYPE_RE, content) != kind:
        yield f'data-page-type is not "{kind}"'

    nav = _first(NAV_RE, content)
    missing = [h for _, entries in cat.GROUPS for h, _ in entries if f'href="{h}"' not in nav]
    if missing:
        yield f"nav is missing {len(missing)} catalog pages (stale regeneration?)"


def main():
    problems = 0
    for page in cat.PAGES:
        path = os.path.join(REPO_ROOT, page.slug)
        if not os.path.isfile(path):
            print(f"{page.slug}: missing")
            problems += 1
            continue
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        for problem in check_page(page.slug, content):
            print(f"{page.slug}: {problem}")
            problems += 1
    if problems:
        print(f"\n{problems} naming problem(s) across the catalog.")
        return 1
    print(f"OK: all {len(cat.PAGES)} catalog pages are named as the catalog names them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
