#!/usr/bin/env python3
"""The breadcrumb every catalog page carries, from tools/service_catalog.py.

Home / BMW Repair — Snellville, GA on a hub; Home / German Car Oil Change
— Snellville, GA on a make-agnostic page; and, when a make had job pages
(until 2026-09-15), Home / BMW Repair / BMW Oil Change, the three-level
trail that made a job page part of its hub. The names match the nav, the
hub grids and the footer, and tools/build_schema.py reads the trail back
into the page's BreadcrumbList.

The generators emit the trail themselves via breadcrumb(); main() rewrites
the crumb on any make job page that is hand-written, which since the
consolidation is none, so the pipeline no longer runs this file. It stays
as the library the generators and the consistency checker import.

Run from the repo root:  python3 tools/fix_breadcrumbs.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import (PAGES, full_label, hub_for, hubs,  # noqa: E402
                             make_of)
from urls import href_for  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREA = "Snellville, GA"
HOME = ("Home", "index.html")
BLOCK = re.compile(r'<div class="breadcrumb">.*?</div>')
_HUB_LABELS = dict(hubs())


def trail(slug):
    """((label, href), ...) ending with the page itself, which has no href."""
    here = (f"{full_label(slug)} — {AREA}", None)
    hub = hub_for(slug)
    if hub is None or hub == slug:
        return (HOME, here)
    return (HOME, (_HUB_LABELS[hub], hub), here)


def breadcrumb(slug):
    parts = []
    for label, href in trail(slug):
        parts.append(f'<a href="{href_for(href)}">{label}</a>' if href
                     else f'<span class="crumb-here">{label}</span>')
    return '<div class="breadcrumb">' + "<span>/</span>".join(parts) + "</div>"


def transform(html, slug):
    updated, n = BLOCK.subn(lambda _: breadcrumb(slug), html, count=1)
    if n != 1:
        raise SystemExit(f"{slug}: no breadcrumb block to rewrite")
    return updated


def pages():
    """The make pages that are not hubs: the ones that get a third level."""
    return tuple(p.slug for p in PAGES
                 if make_of(p.slug) and hub_for(p.slug) != p.slug)


def main():
    changed = 0
    for slug in pages():
        path = os.path.join(REPO_ROOT, slug)
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        updated = transform(original, slug)
        if updated == original:
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(updated)
        changed += 1
    print(f"breadcrumbs: {changed} of {len(pages())} make pages rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
