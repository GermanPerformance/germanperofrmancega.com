#!/usr/bin/env python3
"""The URLs that used to exist, and where each one now points.

Six service pages were removed on 2026-09-12 (their subjects are covered
by broader pages; a seventh, fleet service, was retired without a stub on
2026-09-15 once its successor became the homepage itself). They had been live and in the sitemap, so search
engines, the Google Business Profile and other sites may still hold
their URLs. GitHub Pages cannot send a 301, so each old URL keeps a stub
page that redirects on arrival: an instant meta refresh, which Google
documents as a permanent-redirect signal, plus a canonical to the new
URL and a script for browsers. tools/build_redirects.py writes them.

Every tool that walks the pages at the repo root imports REDIRECTS and
leaves these files alone: they carry no chrome, no analytics, no schema,
and must never appear in the sitemap. Add a row here when a page is
retired; remove one only when the old URL has had no traffic for a year.
"""

REDIRECTS = {
    "audi-quattro-service-snellville-ga.html": "audi-repair-snellville-ga.html",
    "audi-timing-belt-snellville-ga.html": "audi-repair-snellville-ga.html",
    "bmw-differential-service-snellville-ga.html": "bmw-transmission-repair-snellville-ga.html",
    "bmw-wheel-alignment-snellville-ga.html": "bmw-suspension-repair-snellville-ga.html",
    "german-car-emissions-repair-snellville-ga.html": "german-car-check-engine-light-snellville.html",
    "volkswagen-timing-chain-snellville-ga.html": "volkswagen-engine-repair-snellville-ga.html",
}


def is_redirect(name):
    return name in REDIRECTS


def site_pages(names):
    """The real pages among a listing: .html files that are not stubs."""
    return sorted(n for n in names if n.endswith(".html") and not is_redirect(n))
