#!/usr/bin/env python3
"""Turn the CARFAX Top-Rated badge into the two sizes the site renders.

images/carfax-top-rated-2025.png is the shield CARFAX issues to a Top-Rated
Service Center, with the shop's name on the ribbon: a 1122 x 1402 RGBA export,
1.2MB. The hero shows it 104px tall on phones and 128px from 640px, the
footer 64px. Three renditions, 128, 256 and 384px tall, cover 1x, 2x and 3x
screens at every one of those sizes. Each frame is quantised to 256 colours
first -- six times smaller than RGBA with no visible change on the ribbon
gradient or the fox -- then written as lossless WebP, which beats both lossy
WebP and the palette PNG at every size, and as that palette PNG for the
browsers without WebP. Both keep the alpha channel.

A kit export that arrives on an opaque white canvas has that white knocked
out from the corners first; the shield's dark outer border stops the fill
reaching the white rim inside it. Nothing is upscaled: a source shorter than
256px only gets the sizes it can honestly fill, and the tool says so.

Needs Pillow (the python3.13 install has it).

Run from the repo root:  python3.13 tools/build_badge.py [source.png]
"""

import os
import sys

from PIL import Image, ImageDraw, UnidentifiedImageError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO_ROOT, "images", "carfax-top-rated-2025.png")
OUT = os.path.join(REPO_ROOT, "assets", "img")
SLUG = "carfax-top-rated-2025"
HEIGHTS = (128, 256, 384)
COLOURS = 256

# A corner pixel this light, and fully opaque, means the export has no alpha
# and the canvas around the shield is white. Pixels within FILL_TOLERANCE of
# that white (anti-aliased edges) go with it.
WHITE_FLOOR = 240
FILL_TOLERANCE = 40


def load(path):
    """Open the source as RGBA, or explain what is missing."""
    if not os.path.exists(path):
        raise SystemExit(
            f"missing {os.path.relpath(path, REPO_ROOT)}: save the CARFAX "
            "Top-Rated badge from the shop kit there (largest size, "
            "transparent background if you have it) and run again")
    try:
        with Image.open(path) as image:
            return image.convert("RGBA")
    except UnidentifiedImageError as err:
        raise SystemExit(f"{path}: not an image Pillow can read ({err})")


def corners(image):
    width, height = image.size
    return ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))


def is_opaque_white(pixel):
    red, green, blue, alpha = pixel
    return alpha == 255 and min(red, green, blue) >= WHITE_FLOOR


def knock_out_white(image):
    """Return a copy with any white canvas reachable from a corner made
    transparent. A source that already has a transparent surround is
    returned unchanged."""
    seeds = [xy for xy in corners(image) if is_opaque_white(image.getpixel(xy))]
    if not seeds:
        return image
    cleared = image.copy()
    for xy in seeds:
        # A seed already cleared by an earlier corner's fill is skipped, or
        # floodfill would spread the transparent value through the shield.
        if is_opaque_white(cleared.getpixel(xy)):
            ImageDraw.floodfill(cleared, xy, (0, 0, 0, 0), thresh=FILL_TOLERANCE)
    return cleared


def trim(image):
    """Crop to the opaque artwork so the sizes below measure the shield."""
    box = image.getchannel("A").getbbox()
    if box is None:
        raise SystemExit("the badge is fully transparent after trimming")
    return image.crop(box)


def renditions(image):
    """(height, frame) for each target height the source can fill."""
    fits = [h for h in HEIGHTS if h <= image.height]
    if not fits:
        raise SystemExit(
            f"source is only {image.height}px tall; the smallest rendition "
            f"is {HEIGHTS[0]}px and nothing is upscaled")
    return [(h, image.resize((round(image.width * h / image.height), h),
                             Image.LANCZOS)) for h in fits]


def write(height, frame):
    png = os.path.join(OUT, f"{SLUG}-{height}.png")
    webp = os.path.join(OUT, f"{SLUG}-{height}.webp")
    palette = frame.quantize(colors=COLOURS, method=Image.Quantize.FASTOCTREE,
                             dither=Image.Dither.FLOYDSTEINBERG)
    palette.save(png, "PNG", optimize=True)
    palette.convert("RGBA").save(webp, "WEBP", lossless=True, method=6)
    return (frame.width, height, os.path.getsize(png), os.path.getsize(webp))


def main(argv):
    source = argv[1] if len(argv) > 1 else SOURCE
    badge = trim(knock_out_white(load(source)))
    os.makedirs(OUT, exist_ok=True)
    print(f"{os.path.relpath(source, REPO_ROOT)}: {badge.width} x {badge.height} after trim")
    for height, frame in renditions(badge):
        width, _, png_bytes, webp_bytes = write(height, frame)
        print(f"  {height}px: {width} x {height}  png {png_bytes / 1024:.1f}KB  "
              f"webp {webp_bytes / 1024:.1f}KB")
    skipped = [h for h in HEIGHTS if h > badge.height]
    if skipped:
        print(f"  skipped {skipped}: taller than the source; a larger export "
              "from the CARFAX kit would fill them", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
