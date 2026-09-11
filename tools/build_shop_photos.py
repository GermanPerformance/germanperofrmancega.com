#!/usr/bin/env python3
"""Turn the six shop photos into responsive web assets.

photo1.webp .. photo6.webp in the repo root are the owner's own photographs
of customer cars in the bay, all portrait and roughly 800 x 1020;
photo2_replace.png is a sharper 1122 x 1402 take of the lift scene and
supersedes photo2.webp. The widest rendition never exceeds the source:
nothing is upscaled.

Each photo gets a descriptive slug and three widths in WebP plus a JPEG
fallback, written to assets/img/shop/.

Needs Pillow with WebP support (the python3.13 install has it).

Run from the repo root:  python3.13 tools/build_shop_photos.py
"""

import os
import sys

from PIL import Image, ImageOps

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO_ROOT, "assets", "img", "shop")

# source file -> slug used in the asset names
PHOTOS = {
    "photo1.webp": "bmw-2-series",
    "photo2_replace.png": "bmw-m3-on-lift",
    "photo3.webp": "bmw-5-series",
    "photo4.webp": "mercedes-amg-gt",
    "photo5.webp": "mercedes-amg-gle",
    "photo6.webp": "porsche-cayenne-gts",
}
WIDTHS = (420, 640, 800, 1100)


def renditions(source_width):
    """Widths to write: the fixed steps that fit, plus the source width when
    it is meaningfully (10%+) wider than the largest step that fit."""
    steps = [w for w in WIDTHS if w <= source_width]
    if source_width > steps[-1] * 1.1 and source_width < WIDTHS[-1]:
        steps.append(source_width)
    return steps


def build(name, slug):
    image = ImageOps.exif_transpose(Image.open(os.path.join(REPO_ROOT, name)))
    image = image.convert("RGB")
    written = []
    for width in renditions(image.width):
        height = round(image.height * width / image.width)
        frame = image.resize((width, height), Image.LANCZOS)
        webp = os.path.join(OUT, f"{slug}-{width}.webp")
        jpeg = os.path.join(OUT, f"{slug}-{width}.jpg")
        frame.save(webp, "WEBP", quality=78, method=6)
        frame.save(jpeg, "JPEG", quality=74, optimize=True, progressive=True)
        written.append((width, height, os.path.getsize(webp), os.path.getsize(jpeg)))
    return written


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, slug in PHOTOS.items():
        path = os.path.join(REPO_ROOT, name)
        if not os.path.exists(path):
            print(f"missing {name}", file=sys.stderr)
            return 1
        for width, height, wb, jb in build(name, slug):
            print(f"{slug:22s} {width}x{height}  webp {wb//1024:3d}KB  jpg {jb//1024:3d}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
