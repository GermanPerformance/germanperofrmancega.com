#!/usr/bin/env python3
"""Add an in-content "Related Services" block to every service page.

After the footer placeholders were fixed, each service page linked to related
work only from the footer. Footer links are boilerplate and carry noticeably
less weight than a link inside the content, and they sit below the final CTA
where few readers look. This puts the same relationships in the body, just
above the closing call-to-action, where someone who has finished reading about
one job is deciding what else their car needs.

Reuses the ranking from fix_footer_links (same brand first, then the same job
on other marques, then the cross-brand pages) so the two agree.

This writes markup only. It used to append a stylesheet block to
site.css when the literal ".rel-grid{" was absent -- a substring test that
went false the moment .rel-grid moved into a selector list, so the block was
re-appended on every run. Worse, it still declared 'DM Sans' and 'Space
Mono', which stopped being loaded when the type system moved to Archivo and
IBM Plex Mono, so .rel-name and .rel-go silently fell back to system fonts.
A markup generator has no business writing stylesheets; the classes it emits
are styled in the design system.

Run from the repo root:  python3 tools/add_related_services.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix_footer_links import SERVICES, brand_of, related  # noqa: E402
from service_catalog import (MAKES, full_label, hub_for, hubs, make_of,  # noqa: E402
                             service_of, service_pages)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRAND_TITLES = {m.key: (f"MORE {m.short.upper()}", "SERVICES") for m in MAKES}
DEFAULT_TITLE = ("RELATED", "SERVICES")
_SHORT = {m.key: m.short for m in MAKES}
_HUB_LABELS = dict(hubs())


def generic_page_for(service):
    """The make-agnostic page for a job, if the site has one."""
    return next((p for p in service_pages()
                 if make_of(p) is None and service_of(p) == service), None)


def parents_row(page):
    """On a make's page, the two places it belongs: every job the shop does
    on that make, and the same job for every make. Reuses the footer's
    link-row class, as the hubs do for their sister makes."""
    hub = hub_for(page)
    if hub is None:
        return ""
    links = [f'<a href="{hub}">All {_SHORT[make_of(page)]} services</a>']
    generic = generic_page_for(service_of(page))
    if generic:
        links.append(f'<a href="{generic}">{full_label(generic)}</a>')
    return '  <div class="flinks fu">' + "".join(links) + "</div>\n"


# The block this writes carries class="rel-grid fu", so a marker with the
# closing quote never matched and every run appended another copy. Three
# blocks had accumulated on 30 pages before it was noticed.
MARKER = 'class="rel-grid'
# The block and the closing section it sits above, as tools/apply_redesign.py
# leaves them. The pre-redesign forms (inline styles) went unmatched for a
# while, so this tool silently rewrote nothing on any page.
BLOCK = re.compile(
    r'<section>\s*\n'
    r'  <div class="sh fu"><div class="sl">Keep Your Car Right</div>.*?</section>\n',
    re.S)
ANCHOR = '<section class="cta-final">'


def build_block(page):
    picks = related(page, limit=6)
    lead, accent = BRAND_TITLES.get(brand_of(page), DEFAULT_TITLE)
    cards = "".join(
        f'    <a href="{p}" class="rel-card">'
        f'<span class="rel-name">{SERVICES[p]}</span>'
        f'<span class="rel-go">&rarr;</span></a>\n'
        for p in picks
    )
    return (
        '<section>\n'
        '  <div class="sh fu"><div class="sl">Keep Your Car Right</div>\n'
        f'  <h2>{lead}<br><span class="accent">{accent}</span></h2></div>\n'
        '  <div class="rel-grid fu">\n'
        f'{cards}'
        '  </div>\n'
        f'{parents_row(page)}'
        '</section>\n'
    )


def main():
    changed = 0
    for page in sorted(SERVICES):
        path = os.path.join(REPO_ROOT, page)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        original = content

        block = build_block(page)

        if MARKER in content:
            # Replace rather than skip, so adding a service refreshes the
            # related links on every page that should now point at it.
            updated, n = BLOCK.subn(block, content, count=1)
            if n != 1:
                print(f"  !! {page}: rel-grid present but not replaceable")
                continue
            content = updated
        else:
            if ANCHOR not in content:
                print(f"  !! {page}: closing CTA section not found")
                continue
            idx = content.rindex(ANCHOR)
            content = content[:idx] + block + content[idx:]

        if content == original:
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        changed += 1

    print(f"related-services block written on {changed} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
