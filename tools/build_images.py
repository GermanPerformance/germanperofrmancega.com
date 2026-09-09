#!/usr/bin/env python3
"""Turn the source images into responsive, web-sized assets.

The logo is a 1536x1024 PNG whose artwork occupies only part of the canvas --
the rest is transparent padding -- yet it was inlined as base64 at full size
and rendered about 108px wide. Cropping to the real bounding box and encoding
to WebP takes it from ~312KB to a few KB.

Needs only cwebp/dwebp and sips, both already present. The PNG alpha bounding
box is found with the standard library: zlib inflates the image data and the
scanlines are un-filtered by hand, which avoids depending on Pillow.

Run from the repo root:  python3 tools/build_images.py
"""

import os
import struct
import subprocess
import sys
import zlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO_ROOT, "images")
OUT = os.path.join(REPO_ROOT, "assets", "img")

# Gallery photos: rendered in a 2-column grid, so ~640 CSS px is the widest a
# card gets. 640w and 960w (for 1.5-2x screens) is the useful range.
GALLERY = ["bmw-m3-competition", "audi-r8", "porsche-gt3", "mercedes-c63s"]
GALLERY_WIDTHS = [640, 960]

# Logo renders at ~72px tall in the nav; 144/288 covers 1x and 2x.
LOGO_WIDTHS = [144, 288]


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}\n{result.stderr}")


def png_rgba(path):
    """Decode an 8-bit RGBA PNG to (width, height, pixels bytes)."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path}: not a PNG")

    width = height = None
    idat = bytearray()
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", body[:10])
            if (depth, color) != (8, 6):
                raise SystemExit(
                    f"{path}: expected 8-bit RGBA (depth 8, color 6), got {depth}/{color}")
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
        pos += 12 + length

    raw = zlib.decompress(bytes(idat))
    stride = width * 4
    out = bytearray(height * stride)
    prev = bytearray(stride)

    # Undo the per-scanline filter (PNG spec section 9).
    at = 0
    for y in range(height):
        ftype = raw[at]
        line = bytearray(raw[at + 1:at + 1 + stride])
        at += 1 + stride
        if ftype == 1:      # Sub
            for i in range(4, stride):
                line[i] = (line[i] + line[i - 4]) & 0xFF
        elif ftype == 2:    # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:    # Average
            for i in range(stride):
                left = line[i - 4] if i >= 4 else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:    # Paeth
            for i in range(stride):
                a = line[i - 4] if i >= 4 else 0
                b = prev[i]
                c = prev[i - 4] if i >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        elif ftype != 0:
            raise SystemExit(f"{path}: unknown filter type {ftype}")
        out[y * stride:(y + 1) * stride] = line
        prev = line

    return width, height, bytes(out)


def alpha_bbox(width, height, pixels, threshold=8):
    """Tightest box containing pixels more opaque than `threshold`."""
    min_x, min_y, max_x, max_y = width, height, -1, -1
    for y in range(height):
        row = y * width * 4
        for x in range(width):
            if pixels[row + x * 4 + 3] > threshold:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
    if max_x < 0:
        raise SystemExit("logo is fully transparent")
    return min_x, min_y, max_x - min_x + 1, max_y - min_y + 1


def build_logo():
    src = os.path.join(SRC, "german-performance-logo.png")
    width, height, pixels = png_rgba(src)
    x, y, w, h = alpha_bbox(width, height, pixels)
    print(f"logo: {width}x{height} -> content box {w}x{h} at ({x},{y}) "
          f"[{100 - (w * h * 100 // (width * height))}% of canvas was padding]")

    for target in LOGO_WIDTHS:
        webp = os.path.join(OUT, f"logo-{target}.webp")
        run(["cwebp", "-quiet", "-crop", str(x), str(y), str(w), str(h),
             "-resize", str(target), "0", "-resize_mode", "down_only",
             "-q", "90", "-alpha_q", "100", "-m", "6", src, "-o", webp])

    # PNG fallback comes from the WebP via dwebp so it is pixel-identical and
    # keeps its alpha; sips can silently drop the alpha channel here.
    run(["dwebp", "-quiet", os.path.join(OUT, f"logo-{LOGO_WIDTHS[0]}.webp"),
         "-o", os.path.join(OUT, f"logo-{LOGO_WIDTHS[0]}.png")])

    return w, h


def source_width(path):
    """Pixel width of an image, via sips."""
    out = subprocess.run(["sips", "-g", "pixelWidth", path],
                         capture_output=True, text=True).stdout
    return int(out.strip().split(":")[-1])


def build_gallery():
    for name in GALLERY:
        src = os.path.join(SRC, f"{name}.jpg")
        native = source_width(src)
        for width in GALLERY_WIDTHS:
            # Never upscale. cwebp guards this itself with down_only, but sips
            # will happily enlarge a 800px source to 960 and produce a file
            # larger than the original.
            if width > native:
                print(f"  skip {name}-{width}: source is only {native}px wide")
                continue
            run(["cwebp", "-quiet", "-q", "78", "-sharp_yuv", "-m", "6",
                 "-resize", str(width), "0", "-resize_mode", "down_only",
                 src, "-o", os.path.join(OUT, "gallery", f"{name}-{width}.webp")])
            # --resampleWidth, not -Z: -Z constrains the longest side, which
            # would mis-size the 800x1200 portrait sources.
            run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "60",
                 "--resampleWidth", str(width), src,
                 "--out", os.path.join(OUT, "gallery", f"{name}-{width}.jpg")])


def report():
    print("\nGenerated assets:")
    total = 0
    for root, _, files in os.walk(OUT):
        for f in sorted(files):
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            total += size
            rel = os.path.relpath(path, REPO_ROOT)
            print(f"  {size / 1024:8.1f} KB  {rel}")
    print(f"  {total / 1024:8.1f} KB  TOTAL")


def main():
    os.makedirs(os.path.join(OUT, "gallery"), exist_ok=True)
    build_logo()
    build_gallery()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
