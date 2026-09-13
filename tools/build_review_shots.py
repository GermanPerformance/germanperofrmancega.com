#!/usr/bin/env python3
"""Turn the five Google review screenshots into responsive web assets.

images/review-*.png are unretouched captures of the shop's Google reviews,
all roughly 930px wide and 460 to 1110px tall. Each one ends in Google's
"Hover to react / share" row, which is hover-state UI that means nothing on
a static page, so it is cropped off: the crop line is found by scanning up
from the bottom for that icon band and the white gap above it, then the
capture's own top margin is mirrored beneath the last line of content.
Everything else -- avatar, name, stars, date, badges, customer photos, the
kebab menu -- stays, because an obviously unedited capture is the point.

Each capture gets three widths in WebP plus a JPEG fallback, written to
assets/img/reviews/. These are pictures of text, not photographs, so the
encoders run hotter than build_shop_photos.py and the JPEG keeps full
chroma (4:4:4); subsampling smears small dark type on white.

Needs Pillow with WebP support (the python3.13 install has it).

Run from the repo root:  python3.13 tools/build_review_shots.py
"""

import os
import sys

from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO_ROOT, "images")
OUT = os.path.join(REPO_ROOT, "assets", "img", "reviews")

SLUGS = (
    "review-kayode-olaoye",
    "review-chelsea-brown",
    "review-anan-barghouti",
    "review-sahir-razi",
    "review-nageeb-alghoul",
)
WIDTHS = (420, 640)

# Luma below this is "ink"; the captures' background is pure white.
INK = 235
# The reaction row's icons are 36px tall in every capture; anything outside
# this range means the scan found something else and the crop is unsafe.
ICON_BAND = (20, 60)

WEBP_QUALITY = 90
JPEG_QUALITY = 88


def is_ink_row(px, width, y):
    return any(px[x, y] < INK for x in range(0, width, 2))


def is_ink_col(px, height, x):
    return any(px[x, y] < INK for y in range(0, height, 2))


def crop_box(image):
    """Return (top, bottom) rows that keep the review and drop the reaction
    row, keeping equal white space above the first and below the last line
    of content. Raises if the reaction row cannot be identified."""
    grey = image.convert("L")
    width, height = grey.size
    px = grey.load()

    top_margin = next(y for y in range(height) if is_ink_row(px, width, y))

    y = height - 1
    while y > 0 and not is_ink_row(px, width, y):
        y -= 1
    icon_bottom = y
    while y > 0 and is_ink_row(px, width, y):
        y -= 1
    icon_top = y + 1
    while y > 0 and not is_ink_row(px, width, y):
        y -= 1
    content_bottom = y

    band = icon_bottom - icon_top + 1
    if not ICON_BAND[0] <= band <= ICON_BAND[1]:
        raise ValueError(f"reaction row not found (bottom band is {band}px)")
    if content_bottom <= top_margin:
        raise ValueError("no content above the reaction row")

    # Mirror the top margin, but never reach into the icon band: on some
    # captures the gap above the icons is narrower than the top margin.
    return 0, min(content_bottom + 1 + top_margin, icon_top)


def renditions(source_width):
    """The fixed steps that fit, plus the source width. Nothing upscales."""
    steps = [w for w in WIDTHS if w < source_width]
    return steps + [source_width]


def flatten(image):
    """Composite any alpha onto white; the captures are white-backed."""
    if image.mode != "RGBA":
        return image.convert("RGB")
    white = Image.new("RGB", image.size, (255, 255, 255))
    white.paste(image, mask=image.getchannel("A"))
    return white


def build(slug):
    image = flatten(Image.open(os.path.join(SRC, f"{slug}.png")))
    top, bottom = crop_box(image)
    image = image.crop((0, top, image.width, bottom))
    written = []
    for width in renditions(image.width):
        height = round(image.height * width / image.width)
        frame = image.resize((width, height), Image.LANCZOS)
        webp = os.path.join(OUT, f"{slug}-{width}.webp")
        jpeg = os.path.join(OUT, f"{slug}-{width}.jpg")
        frame.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
        frame.save(jpeg, "JPEG", quality=JPEG_QUALITY, subsampling=0,
                   optimize=True, progressive=True)
        written.append((width, height, os.path.getsize(webp), os.path.getsize(jpeg)))
    return written


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in SLUGS:
        path = os.path.join(SRC, f"{slug}.png")
        if not os.path.exists(path):
            print(f"missing {os.path.relpath(path, REPO_ROOT)}", file=sys.stderr)
            return 1
        try:
            renditions_written = build(slug)
        except ValueError as err:
            print(f"{slug}: {err}", file=sys.stderr)
            return 1
        for width, height, wb, jb in renditions_written:
            print(f"{slug:24s} {width}x{height}  webp {wb//1024:3d}KB  jpg {jb//1024:3d}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
