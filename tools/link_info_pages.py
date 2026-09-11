#!/usr/bin/env python3
"""Point the existing About and Contact links at the new real URLs.

about.html and contact.html are worth nothing as orphans. Every page already
links to index.html#about and index.html#contact from both the nav and the
footer, so this is an href swap rather than new markup -- which also keeps it
clear of the redesign, since it changes no classes and no structure.

The homepage keeps its #about and #contact sections and its own anchors:
someone reading the homepage should still be able to jump down it. Only the
cross-page links are retargeted, because those are the ones that were
pointing at a fragment of another document.

ORDERING: this must run AFTER tools/apply_redesign.py. That tool rebuilds the
nav from a template, which re-inserts index.html#about and index.html#contact.
Run in the other order and every page ends up with both -- the footer pointing
at the real URL and the nav pointing at a fragment of the homepage -- which
splits the internal link signal between two addresses for the same content.

Run from the repo root:  python3 tools/link_info_pages.py
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SWAPS = [
    ('href="index.html#about"', 'href="about.html"'),
    ('href="index.html#contact"', 'href="contact.html"'),
]

# The homepage's own in-page navigation stays as anchors -- someone reading
# it should still be able to jump down it. The two new pages are NOT skipped:
# they inherit the donor's nav and footer, so their own links to About and
# Contact would otherwise still point at a fragment of the homepage.
SKIP = {"index.html"}


def main():
    changed = 0
    total = 0
    for name in sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")):
        if name in SKIP:
            continue
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html
        for old, new in SWAPS:
            total += html.count(old)
            html = html.replace(old, new)
        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            changed += 1

    print(f"{total} links retargeted across {changed} pages")
    for slug in ("about.html", "contact.html"):
        inbound = sum(
            1 for f in os.listdir(REPO_ROOT)
            if f.endswith(".html") and f != slug
            and f'href="{slug}"' in open(
                os.path.join(REPO_ROOT, f), encoding="utf-8").read())
        print(f"  {slug:14s} {inbound} inbound pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
