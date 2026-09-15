#!/usr/bin/env python3
"""Every service page on the site: which make it is for, which job it
covers, and the one name it goes by.

This is the single source the site's lists derive from. The nav's
Services panel and the phone menu (tools/apply_redesign.py), the brand
hubs' service grids (tools/build_brand_hubs.py), the footer columns and
related-services blocks (tools/fix_footer_links.py,
tools/add_related_services.py), the breadcrumbs, llms.txt and the
consistency checker all read it, so adding a page here surfaces it
everywhere at once and a name changed here changes on every page.

Three tables and nothing else:

  SERVICES  the jobs, in the order every make's column lists them, each
            with its one label ("Brake Repair", never "Brake Service")
  MAKES     the marques, in column order: the column heading, the short
            name page labels use, and the make's repair hub
  PAGES     one row per page: slug, make (None for the make-agnostic
            pages), service, and for make-agnostic pages the name they
            carry in mixed lists ("German Car Oil Change")

MONEY is the six category pages the homepage cards link to, in the
owner's order, under the Google Business Profile's own names, so the
"Services" column reads the way the profile does. The profile's primary
category, "Auto repair shop", is the homepage itself (the general repair
page was folded into it on 2026-09-15), so the sixth card is the
diagnostics page. GROUPS and HUBS are derived from the tables in the
shape the consumers have always read: GROUPS is one
(heading, ((href, label), ...)) per column, HUBS maps each heading to the
link it carries.
"""

from collections import namedtuple

Service = namedtuple("Service", "key label")
Make = namedtuple("Make", "key heading short hub")
Page = namedtuple("Page", "slug make service label")

# The jobs, in column order. A make's column lists the pages it has in
# this order, so every column reads the same way. "repair" is the hub
# itself and never appears inside a column; the make-agnostic repair
# page is the homepage.
SERVICES = (
    Service("oil",          "Oil Change"),
    Service("brakes",       "Brake Repair"),
    Service("suspension",   "Suspension Repair"),
    Service("transmission", "Transmission Repair"),
    Service("cooling",      "Cooling System Repair"),
    Service("ac",           "AC Repair"),
    Service("diagnostics",  "Engine Diagnostics"),
    Service("engine",       "Engine Repair"),
    Service("battery",      "Battery Replacement"),
    Service("plugs",        "Spark Plug Replacement"),
    Service("tune-up",      "Tune-Up"),
    Service("cel",          "Check Engine Light"),
    Service("inspection",   "Inspection"),
    Service("repair",       "Repair"),
)

MAKES = (
    Make("bmw",        "BMW",           "BMW",        "bmw-repair-snellville-ga.html"),
    Make("mercedes",   "Mercedes-Benz", "Mercedes",   "mercedes-repair-snellville-ga.html"),
    Make("audi",       "Audi",          "Audi",       "audi-repair-snellville-ga.html"),
    Make("porsche",    "Porsche",       "Porsche",    "porsche-repair-snellville-ga.html"),
    Make("volkswagen", "Volkswagen",    "Volkswagen", "volkswagen-repair-snellville-ga.html"),
)

# The six category pages the homepage cards link to, in the owner's order,
# under the Google Business Profile's own names. "Auto repair shop" is the
# homepage, so the cards run brake shop through engine diagnostic.
MONEY = (
    ("german-car-brake-repair-snellville-ga.html",        "Brake Repair"),
    ("german-car-transmission-repair-snellville-ga.html", "Transmission Repair"),
    ("german-car-oil-change-snellville-ga.html",          "Oil Change"),
    ("german-car-tune-up-snellville-ga.html",             "Auto Tune-Up"),
    ("german-car-ac-repair-snellville-ga.html",           "Auto Air Conditioning"),
    ("german-car-check-engine-light-snellville.html",     "Check Engine Light"),
)

PAGES = (
    # make-agnostic pages, in the order the "Services" column shows
    Page("german-car-brake-repair-snellville-ga.html",        None, "brakes",       "German Car Brake Repair"),
    Page("german-car-transmission-repair-snellville-ga.html", None, "transmission", "German Car Transmission Repair"),
    Page("german-car-oil-change-snellville-ga.html",          None, "oil",          "German Car Oil Change"),
    Page("german-car-tune-up-snellville-ga.html",             None, "tune-up",      "German Car Tune-Up"),
    Page("german-car-ac-repair-snellville-ga.html",           None, "ac",           "German Car AC Repair"),
    Page("german-car-check-engine-light-snellville.html",     None, "cel",          "Check Engine Light"),
    Page("pre-purchase-inspection-german-car-ga.html",        None, "inspection",   "Pre-Purchase Inspection"),
    # BMW
    Page("bmw-repair-snellville-ga.html",                 "bmw", "repair",       None),
    Page("bmw-oil-change-snellville-ga.html",             "bmw", "oil",          None),
    Page("bmw-suspension-repair-snellville-ga.html",      "bmw", "suspension",   None),
    Page("bmw-transmission-repair-snellville-ga.html",    "bmw", "transmission", None),
    Page("bmw-cooling-system-repair-snellville-ga.html",  "bmw", "cooling",      None),
    Page("bmw-battery-replacement-snellville-ga.html",    "bmw", "battery",      None),
    Page("bmw-spark-plug-replacement-snellville-ga.html", "bmw", "plugs",        None),
    # Mercedes-Benz
    Page("mercedes-repair-snellville-ga.html",             "mercedes", "repair",       None),
    Page("mercedes-oil-change-snellville-ga.html",         "mercedes", "oil",          None),
    Page("mercedes-brake-service-snellville-ga.html",      "mercedes", "brakes",       None),
    Page("mercedes-suspension-snellville-ga.html",         "mercedes", "suspension",   None),
    Page("mercedes-transmission-snellville-ga.html",       "mercedes", "transmission", None),
    Page("mercedes-cooling-system-snellville-ga.html",     "mercedes", "cooling",      None),
    Page("mercedes-ac-repair-snellville-ga.html",          "mercedes", "ac",           None),
    Page("mercedes-engine-diagnostics-snellville-ga.html", "mercedes", "diagnostics",  None),
    # Audi
    Page("audi-repair-snellville-ga.html",            "audi", "repair",     None),
    Page("audi-oil-change-snellville-ga.html",        "audi", "oil",        None),
    Page("audi-brake-service-snellville-ga.html",     "audi", "brakes",     None),
    Page("audi-suspension-repair-snellville-ga.html", "audi", "suspension", None),
    # Porsche
    Page("porsche-repair-snellville-ga.html",            "porsche", "repair",     None),
    Page("porsche-oil-change-snellville-ga.html",        "porsche", "oil",        None),
    Page("porsche-brake-service-snellville-ga.html",     "porsche", "brakes",     None),
    Page("porsche-suspension-repair-snellville-ga.html", "porsche", "suspension", None),
    Page("porsche-inspection-snellville-ga.html",        "porsche", "inspection", None),
    # Volkswagen
    Page("volkswagen-repair-snellville-ga.html",        "volkswagen", "repair", None),
    Page("volkswagen-oil-change-snellville-ga.html",    "volkswagen", "oil",    None),
    Page("volkswagen-brake-service-snellville-ga.html", "volkswagen", "brakes", None),
    Page("volkswagen-engine-repair-snellville-ga.html", "volkswagen", "engine", None),
)

# How the related-services ranking groups jobs: a BMW spark-plug page and
# the tune-up page are the same neighbourhood, as are the three engine
# pages. Anything unlisted is its own group.
RELATED_GROUPS = {
    "plugs": "ignition", "tune-up": "ignition",
    "cel": "engine", "diagnostics": "engine", "engine": "engine",
    "repair": "general",
}

GENERIC_GROUP = "Services"
GENERIC_HUB = "index.html#services"

# The homepage is the make-agnostic repair page: the general repair page
# was deleted on 2026-09-15 because it covered the same offering. It is
# not in PAGES (no generator writes its chrome from the catalog), but the
# related blocks and footer rows link to it where they linked to that
# page, under the name that page went by.
HOME = "index.html"
HOME_LABEL = "German Auto Repair"

_SERVICES = {s.key: s for s in SERVICES}
_ORDER = {s.key: i for i, s in enumerate(SERVICES)}
_MAKES = {m.key: m for m in MAKES}
_PAGES = {p.slug: p for p in PAGES}
_MONEY = dict(MONEY)


def _check_tables():
    if len(_PAGES) != len(PAGES):
        raise SystemExit("service_catalog: duplicate slug in PAGES")
    for p in PAGES:
        if p.service not in _SERVICES:
            raise SystemExit(f"service_catalog: {p.slug}: unknown service {p.service!r}")
        if p.make is not None and p.make not in _MAKES:
            raise SystemExit(f"service_catalog: {p.slug}: unknown make {p.make!r}")
        if p.make is None and not p.label:
            raise SystemExit(f"service_catalog: {p.slug}: make-agnostic pages need a label")
    for m in MAKES:
        if _PAGES.get(m.hub, Page(None, None, None, None)).service != "repair":
            raise SystemExit(f"service_catalog: {m.key}: hub {m.hub} is not its repair page")
    for slug, _ in MONEY:
        if slug not in _PAGES:
            raise SystemExit(f"service_catalog: MONEY page {slug} is not in PAGES")


def _page(slug):
    try:
        return _PAGES[slug]
    except KeyError:
        raise SystemExit(f"service_catalog: {slug}: not in catalog") from None


def make(key):
    return _MAKES[key]


def make_of(slug):
    """The make's key, or None for a make-agnostic page."""
    return _page(slug).make


def service_of(slug):
    return _page(slug).service


def hub_for(slug):
    """The repair hub a make's page sits under; None for make-agnostic pages."""
    key = make_of(slug)
    return _MAKES[key].hub if key else None


def full_label(slug):
    """The page's name in a mixed list: "BMW Oil Change", "German Car Oil Change"."""
    p = _page(slug)
    if p.make is None:
        return p.label
    return f"{_MAKES[p.make].short} {_SERVICES[p.service].label}"


def nav_label(slug):
    """The page's name inside its own column, where the heading names the
    make: the job alone, or the profile's category name for a money page."""
    p = _page(slug)
    if p.make is not None:
        return _SERVICES[p.service].label
    return _MONEY.get(slug, p.label)


def ranking_group(service_key):
    return RELATED_GROUPS.get(service_key, service_key)


def pages_for(make_key):
    """A make's pages, hub first, then in SERVICES order."""
    mine = [p for p in PAGES if p.make == make_key]
    return tuple(sorted(mine, key=lambda p: (p.service != "repair", _ORDER[p.service])))


def _generic_column():
    extras = tuple((p.slug, nav_label(p.slug)) for p in PAGES
                   if p.make is None and p.slug not in _MONEY)
    return MONEY + extras


def _make_column(m):
    return tuple((p.slug, nav_label(p.slug)) for p in pages_for(m.key)
                 if p.service != "repair")


def service_pages():
    """Every page that is not a hub: the makes' pages in column order, then
    the make-agnostic pages in the order their column shows them."""
    by_make = [p.slug for m in MAKES for p in pages_for(m.key) if p.service != "repair"]
    return tuple(by_make) + tuple(h for h, _ in _generic_column())


def hubs():
    return tuple((m.hub, f"{m.short} Repair") for m in MAKES)


_check_tables()

GROUPS = ((GENERIC_GROUP, _generic_column()),) + tuple(
    (m.heading, _make_column(m)) for m in MAKES)

HUBS = {GENERIC_GROUP: GENERIC_HUB, **{m.heading: m.hub for m in MAKES}}
