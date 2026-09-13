#!/usr/bin/env python3
"""Give every page the Open Graph and Twitter Card tags a shared link needs.

Only the homepage and the brake landing page carried them; a service page
pasted into a text, a Facebook post or a Google Business update rendered
as a bare URL with no image. The tags are derived from what the page
already declares -- its <title>, meta description and canonical -- so they
cannot drift from it, and they are written in exactly the form
tools/build_landing_pages.py emits, so a page built by that generator is
untouched here (its test asserts as much).

The image is the page's own og:image when it has one (the landing pages
set theirs from the page photo). Otherwise it is chosen from the slug:
the six service photographs in assets/img/services/ for the services they
show, a photograph of the marque for the brand hubs, the people for the
About page, and the site image for everything else. A block this tool
wrote earlier is refreshed in place, keeping its image.

index.html is hand-built and carries its own tags, so it is skipped, as
is any page without a canonical (the 404).

Idempotent. Run from the repo root after the generators and before
tools/build_schema.py, which reads og:image for Service.image:

    python3 tools/build_social_tags.py
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redirects import site_pages  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"
FALLBACK = "og-image.jpg"

# Ordered: the first slug fragment that matches decides. "repair" alone is
# last so "brake-repair" and "ac-repair" are not swallowed by it.
SERVICE_PHOTOS = (
    ("oil-change", "assets/img/services/oil-change-1100.jpg"),
    ("brake", "assets/img/services/brake-repair-1100.jpg"),
    ("transmission", "assets/img/services/transmission-repair-1100.jpg"),
    ("ac-repair", "assets/img/services/ac-repair-1100.jpg"),
    ("tune-up", "assets/img/services/tune-up-1100.jpg"),
)
BRAND_PHOTOS = {
    "bmw-repair": "assets/img/shop/bmw-m3-on-lift-1100.jpg",
    "mercedes-repair": "assets/img/shop/mercedes-amg-gt-1100.jpg",
    "porsche-repair": "assets/img/shop/porsche-cayenne-gts-1100.jpg",
    "german-car-repair": "assets/img/services/auto-repair-1100.jpg",
}
PAGE_PHOTOS = {"about.html": "assets/img/shop/sam-and-zayd-1100.jpg"}

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)">')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"\s*/?>\n')
IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]*)"\s*/?>')
# The block this tool writes, or the older self-closing form the privacy
# page generator used to write; either is replaced whole.
BLOCK_RE = re.compile(
    r'<meta property="og:type" content="website"\s*/?>\n'
    r'(?:<meta (?:property="og:|name="twitter:)[a-z_]+" content="[^"]*"\s*/?>\n)+')


def choose_image(name):
    """A photograph that shows what the page is about, or the site image."""
    if name in PAGE_PHOTOS:
        return PAGE_PHOTOS[name]
    slug = name[:-len(".html")] if name.endswith(".html") else name
    for prefix, photo in BRAND_PHOTOS.items():
        if slug.startswith(prefix):
            return photo
    for fragment, photo in SERVICE_PHOTOS:
        if fragment in slug:
            return photo
    return FALLBACK


def social_block(title, description, url, image):
    return "\n".join((
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{image}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{description}">',
        f'<meta name="twitter:image" content="{image}">',
    )) + "\n"


def attribute(text):
    """Title text as it must appear inside a double-quoted attribute."""
    return html.escape(html.unescape(text.strip()), quote=True)


def transform(page, name):
    canonical = CANONICAL_RE.search(page)
    title = TITLE_RE.search(page)
    description = DESC_RE.search(page)
    if not (canonical and title and description):
        return page
    existing = IMAGE_RE.search(page)
    image = existing.group(1) if existing else f"{SITE}/{choose_image(name)}"
    block = social_block(attribute(title.group(1)), description.group(1),
                         canonical.group(1), image)
    without = BLOCK_RE.sub("", page, count=1)
    return without.replace(canonical.group(0), canonical.group(0) + block, 1)


def main():
    pages = [f for f in site_pages(os.listdir(REPO_ROOT)) if f != "index.html"]
    changed = skipped = 0
    for name in pages:
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        updated = transform(original, name)
        if updated == original:
            if not CANONICAL_RE.search(original):
                skipped += 1
                print(f"  skip {name}: no canonical")
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(updated)
        changed += 1
    print(f"social tags: {changed} of {len(pages)} pages updated, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
