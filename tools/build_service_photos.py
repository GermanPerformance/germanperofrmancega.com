#!/usr/bin/env python3
"""Turn the homepage service photos into responsive web assets.

The owner dropped six shop photos in the repo root, one per service card
on the homepage, all portrait and roughly 1122 x 1402. The cards display
them at a 4:3 aspect ratio via CSS object-fit: cover, so the source is
resized (never cropped) and the browser handles the crop. The widest
rendition never exceeds the source: nothing is upscaled.

Each photo gets a descriptive slug and up to four widths in WebP plus a
JPEG fallback, written to assets/img/services/.

Needs Pillow with WebP support (the python3.13 install has it).

Run from the repo root:  python3.13 tools/build_service_photos.py
"""

import os
import sys

from PIL import Image, ImageOps

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO_ROOT, "assets", "img", "services")

# source file -> slug used in the asset names, in the order the cards
# appear on the homepage
PHOTOS = {
    "Auto repair service image 1.png": "auto-repair",
    "Break repair service image 1.png": "brake-repair",
    "Transmission repair service image 2.png": "transmission-repair",
    "Oil change repair service image 3.png": "oil-change",
    "Auto Tune Up Service.png": "tune-up",
    "Air conditioning repair service image 4.png": "ac-repair",
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
