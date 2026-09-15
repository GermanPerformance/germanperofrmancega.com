#!/usr/bin/env python3
"""The chrome every generated page shares, from the tools that own it.

The page generators used to scrape their nav, footer, stylesheet links
and address block from a live "donor" page of the same marque. That
copied whatever the donor happened to carry -- a 2025 copyright, a
second fonts.css link, a footer column the redesign had since replaced
-- and it tied each generator to a page that another generator might be
rewriting. Nothing here is scraped: the nav and phone menu come from
tools/apply_redesign.py, the footer's service links from
tools/fix_footer_links.py, and the address block is the one block, so a
page built from this needs no later pass to look like the others.

Run nothing here; tools/build_service_pages.py, build_brand_hubs.py and
build_landing_pages.py import it.
"""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_redesign as redesign  # noqa: E402
import build_css  # noqa: E402
from fix_footer_links import build_blocks  # noqa: E402
from service_catalog import GENERIC_GROUP, GROUPS, HOME, HOME_LABEL, hubs  # noqa: E402
from urls import href_for  # noqa: E402

SITE = "https://germanperformancega.com"
FAVICON = '<link rel="icon" type="image/png" href="assets/img/favicon-144.png">'
SCRIPTS = ("site", "analytics")

# Phone bar, nav and phone menu, exactly as tools/apply_redesign.py writes
# them on every page.
NAV = redesign.NAV

# The shop's address block, as the service pages' "Why German Performance"
# section shows it beside the reasons.
NAP_GRID = '''<div class="ic-grid">
        <div class="ic"><div class="il">Location</div><div class="iv">Snellville, GA</div><div class="is">2144 Parkwood Rd NW<br>Snellville, GA 30078</div></div>
        <div class="ic"><div class="il">Hours</div><div class="iv">Mon – Fri</div><div class="is">9:30 AM – 6:00 PM<br>Sat – Sun: Closed</div></div>
        <div class="ic"><div class="il">Phone</div><div class="iv">(678) 395-7459</div><div class="is">Same-week slots usually available</div></div>
        <div class="ic"><div class="il">Serving</div><div class="iv">Gwinnett County</div><div class="is">Snellville · Loganville · Grayson · Lawrenceville</div></div>
      </div>'''


def stylesheets(kind="site"):
    """The inline critical block, then the one bundle link (tools/build_css.py)."""
    return build_css.stylesheets(kind, redesign.VERSION)


def scripts():
    v = redesign.VERSION
    return "\n".join(f'<script defer src="assets/js/{name}.js?v={v}"></script>'
                     for name in SCRIPTS)


def footer_with(services_col, flinks):
    year = datetime.date.today().year
    return f'''<footer>
  <div class="ft">
    <div><div class="fb">{redesign.LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div>{redesign.footer_seal_markup()}</div>
    {redesign.FOOTER_CONTACT}
    {services_col}
    {redesign.FOOTER_NAVIGATE}
  </div>
  {flinks}
  <div class="fcopy">© {year} German Performance — Snellville, GA 30078{redesign.PRIVACY_LINK}</div>
</footer>'''


def footer(slug):
    """A service page's footer: its own related links in the Services
    column and the link row, as tools/fix_footer_links.py ranks them."""
    return footer_with(*build_blocks(slug))


def neutral_blocks():
    """The Services column and link row for pages that belong to no make:
    About, Contact, the guides index, the general articles. Three hubs in
    the column, all five in the row."""
    links = [f'<a href="{href_for(h)}">{n}</a>' for h, n in hubs()]
    column = ('<div class="fc"><div class="fct">Services</div>'
              '<a href="/#services">All Services</a>'
              + "".join(links[:3]) + "</div>")
    return column, '<div class="flinks">' + "".join(links) + "</div>"


def neutral_footer():
    return footer_with(*neutral_blocks())


def make_blocks():
    """The Services column and link row for a page that belongs to one
    make (a hub, a make's guide): the homepage and the seven general
    services, never the other makes -- a BMW page has no reason to send
    its reader to the Porsche page (owner, 2026-09-15). Three services in
    the column, the homepage and the other four in the row."""
    general = dict(GROUPS)[GENERIC_GROUP]
    links = [f'<a href="{href_for(h)}">{n}</a>' for h, n in general]
    column = ('<div class="fc"><div class="fct">Services</div>'
              '<a href="/#services">All Services</a>'
              + "".join(links[:3]) + "</div>")
    home = f'<a href="{href_for(HOME)}">{HOME_LABEL}</a>'
    return column, '<div class="flinks">' + home + "".join(links[3:]) + "</div>"


def make_footer():
    return footer_with(*make_blocks())
