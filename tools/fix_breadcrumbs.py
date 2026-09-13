#!/usr/bin/env python3
"""Give every make's service page the breadcrumb that says where it lives.

Home / BMW Repair / BMW Oil Change. The middle crumb is the make's repair
hub, so a reader on a BMW page can step up to everything else the shop
does on a BMW, and search engines see the page as part of that hub rather
than a loose leaf. The trail comes from tools/service_catalog.py, so the
names match the nav, the hub grid and the footer, and tools/build_schema.py
reads it back into the page's BreadcrumbList.

Hubs and the make-agnostic pages keep their two-level crumb: a hub is the
top of its own trail, and the category pages hang from the homepage's
services section, which is not a page.

The generators that build make pages emit this trail themselves via
breadcrumb(), so on their output this is a no-op; the hand-written pages
are the ones it rewrites. Idempotent. Runs after tools/apply_redesign.py
(which normalises the crumb's classes) and before tools/build_schema.py.

Run from the repo root:  python3 tools/fix_breadcrumbs.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import (PAGES, full_label, hub_for, hubs,  # noqa: E402
                             make_of)

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
        parts.append(f'<a href="{href}">{label}</a>' if href
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
