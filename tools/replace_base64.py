#!/usr/bin/env python3
"""Swap inlined base64 images for real, responsive image files.

index.html inlined six images as base64, including the same 312KB logo twice.
Base64 does not compress, so the homepage shipped ~1.12MB gzipped as
render-blocking HTML -- the nav logo alone was 426KB sitting ahead of all body
content, which is why first paint took 7.3s.

Also upgrades the 30 service pages from the full-size german-performance-logo.jpg
(640x350 delivered for a 44px render) to the same shared responsive logo.

Run from the repo root:  python3 tools/replace_base64.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The cropped logo is 3:1, so width follows from the rendered height.
LOGO_RATIO = 3

# alt text -> (basename, available widths, intrinsic w/h of the largest)
GALLERY = {
    "BMW M3 Competition": ("bmw-m3-competition", [640, 960], (960, 1200)),
    "Audi R8": ("audi-r8", [640], (640, 960)),
    "Porsche GT3": ("porsche-gt3", [640], (640, 960)),
    "Mercedes C63S": ("mercedes-c63s", [640, 960], (960, 640)),
}

# Alt text describing what is actually in frame: these are badge detail
# shots, so claiming they show the workshop would be inaccurate.
GALLERY_ALT = {
    "bmw-m3-competition": "Close-up of a BMW M3 Competition badge",
    "audi-r8": "Close-up of an Audi R8 badge",
    "porsche-gt3": "Close-up of a Porsche GT3 badge",
    "mercedes-c63s": "Close-up of a Mercedes-AMG C63 S badge",
}

IMG_RE = re.compile(r'<img\b[^>]*>', re.S)
B64_RE = re.compile(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+')


def attr(tag, name):
    m = re.search(rf'{name}="([^"]*)"', tag)
    return m.group(1) if m else ""


def rendered_height(tag, default):
    """Pixel height the CSS actually paints the logo at."""
    m = re.search(r'height:\s*(\d+)px', attr(tag, "style"))
    return int(m.group(1)) if m else default


def logo_picture(height, *, eager):
    width = height * LOGO_RATIO
    loading = ' decoding="async" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return (
        '<picture class="logo-pic">'
        '<source type="image/webp" '
        'srcset="assets/img/logo-144.webp 1x, assets/img/logo-288.webp 2x">'
        f'<img src="assets/img/logo-144.png" alt="German Performance" '
        f'width="{width}" height="{height}"{loading}>'
        '</picture>'
    )


def gallery_picture(alt):
    base, widths, (iw, ih) = GALLERY[alt]
    webp = ", ".join(f"assets/img/gallery/{base}-{w}.webp {w}w" for w in widths)
    jpg = ", ".join(f"assets/img/gallery/{base}-{w}.jpg {w}w" for w in widths)
    sizes = "(max-width:600px) 100vw, 50vw"
    largest = max(widths)
    return (
        '<picture class="gallery-pic">'
        f'<source type="image/webp" sizes="{sizes}" srcset="{webp}">'
        f'<source type="image/jpeg" sizes="{sizes}" srcset="{jpg}">'
        f'<img src="assets/img/gallery/{base}-{largest}.jpg" '
        f'alt="{GALLERY_ALT[base]}" width="{iw}" height="{ih}" '
        'loading="lazy" decoding="async">'
        '</picture>'
    )


def replace_in(path, default_logo_height):
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    stats = {"logo": 0, "gallery": 0}
    first_logo = [True]

    def swap(match):
        tag = match.group(0)
        if not B64_RE.search(tag):
            return tag
        alt = attr(tag, "alt")
        if alt in GALLERY:
            stats["gallery"] += 1
            return gallery_picture(alt)
        # Everything else inlined is the logo.
        height = rendered_height(tag, default_logo_height)
        eager = first_logo[0]      # nav logo is above the fold
        first_logo[0] = False
        stats["logo"] += 1
        return logo_picture(height, eager=eager)

    content = IMG_RE.sub(swap, content)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return stats


def upgrade_service_logos():
    """Service pages ship a 640x350 JPEG for a 44px-tall render."""
    old = ('<img src="german-performance-logo.jpg" alt="German Performance" '
           'width="640" height="350">')
    new = logo_picture(44, eager=True)
    count = 0
    for name in sorted(os.listdir(REPO_ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        if old not in content:
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content.replace(old, new))
        count += 1
    return count


def main():
    total = {"logo": 0, "gallery": 0}
    for page, default_height in [("index.html", 72),
                                 ("dealer-vs-independent-german-car-repair.html", 52)]:
        stats = replace_in(os.path.join(REPO_ROOT, page), default_height)
        print(f"{page}: {stats['logo']} logo, {stats['gallery']} gallery")
        total["logo"] += stats["logo"]
        total["gallery"] += stats["gallery"]

    swapped = upgrade_service_logos()
    print(f"service pages upgraded to responsive logo: {swapped}")

    remaining = 0
    for name in os.listdir(REPO_ROOT):
        if name.endswith(".html"):
            with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
                remaining += len(B64_RE.findall(fh.read()))
    print(f"base64 images remaining on the site: {remaining}")
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
