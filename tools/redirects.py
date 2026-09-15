#!/usr/bin/env python3
"""The URLs that used to exist, and where each one now points.

Six service pages were removed on 2026-09-12 (their subjects are covered
by broader pages; a seventh, fleet service, was retired without a stub on
2026-09-15 once its successor became the homepage itself). On 2026-09-15
the 23 make-specific job pages (bmw-oil-change, mercedes-brake-service
and so on) were consolidated into the five brand hubs, whose "services we
perform" cards carry their copy, so each forwards to its hub; the three
earlier stubs that had pointed at a job page now point at the hub too, so
no address chains through two redirects. They had all been live and in
the sitemap, so search engines, the Google Business Profile and other
sites may still hold their URLs. GitHub Pages cannot send a 301, so each
old URL keeps a stub page that redirects on arrival: an instant meta
refresh, which Google documents as a permanent-redirect signal, plus a
canonical to the new URL and a script for browsers.
tools/build_redirects.py writes them.

Every tool that walks the pages at the repo root imports REDIRECTS and
leaves these files alone: they carry no chrome, no analytics, no schema,
and must never appear in the sitemap. Add a row here when a page is
retired; remove one only when the old URL has had no traffic for a year.
"""

REDIRECTS = {
    # retired 2026-09-12
    "audi-quattro-service-snellville-ga.html": "audi-repair-snellville-ga.html",
    "audi-timing-belt-snellville-ga.html": "audi-repair-snellville-ga.html",
    "bmw-differential-service-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-wheel-alignment-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "german-car-emissions-repair-snellville-ga.html": "german-car-check-engine-light-snellville.html",
    "volkswagen-timing-chain-snellville-ga.html": "volkswagen-repair-snellville-ga.html",
    # consolidated into the brand hubs 2026-09-15
    "bmw-oil-change-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-suspension-repair-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-transmission-repair-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-cooling-system-repair-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-battery-replacement-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "bmw-spark-plug-replacement-snellville-ga.html": "bmw-repair-snellville-ga.html",
    "mercedes-oil-change-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-brake-service-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-suspension-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-transmission-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-cooling-system-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-ac-repair-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "mercedes-engine-diagnostics-snellville-ga.html": "mercedes-repair-snellville-ga.html",
    "audi-oil-change-snellville-ga.html": "audi-repair-snellville-ga.html",
    "audi-brake-service-snellville-ga.html": "audi-repair-snellville-ga.html",
    "audi-suspension-repair-snellville-ga.html": "audi-repair-snellville-ga.html",
    "porsche-oil-change-snellville-ga.html": "porsche-repair-snellville-ga.html",
    "porsche-brake-service-snellville-ga.html": "porsche-repair-snellville-ga.html",
    "porsche-suspension-repair-snellville-ga.html": "porsche-repair-snellville-ga.html",
    "porsche-inspection-snellville-ga.html": "porsche-repair-snellville-ga.html",
    "volkswagen-oil-change-snellville-ga.html": "volkswagen-repair-snellville-ga.html",
    "volkswagen-brake-service-snellville-ga.html": "volkswagen-repair-snellville-ga.html",
    "volkswagen-engine-repair-snellville-ga.html": "volkswagen-repair-snellville-ga.html",
}


def is_redirect(name):
    return name in REDIRECTS


def site_pages(names):
    """The real pages among a listing: .html files that are not stubs."""
    return sorted(n for n in names if n.endswith(".html") and not is_redirect(n))
