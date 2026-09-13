#!/usr/bin/env python3
"""Extract only customer photos and the photo avatar from the source captures.

Run from the repo root with python3.13 tools/build_review_assets.py (Pillow).
Coordinates refer to the original, unscaled images/review-*.png captures.
Lossless crops preserve the original pixels; all review text lives in HTML.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/reviews"
CROPS = (
    ("kayode-olaoye", "kayode-audi.webp", (29, 320, 283, 574)),
    ("anan-barghouti", "anan-mercedes.webp", (27, 407, 281, 661)),
    ("nageeb-alghoul", "nageeb-avatar.png", (30, 30, 95, 95)),
    ("nageeb-alghoul", "nageeb-bmw-front.webp", (30, 762, 285, 1017)),
    ("nageeb-alghoul", "nageeb-bmw-night.webp", (293, 762, 548, 1017)),
    ("nageeb-alghoul", "nageeb-bmw-coast.webp", (555, 762, 810, 1017)),
)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for reviewer, filename, box in CROPS:
        with Image.open(ROOT / "images" / f"review-{reviewer}.png") as source:
            if not (0 <= box[0] < box[2] <= source.width
                    and 0 <= box[1] < box[3] <= source.height):
                raise ValueError(f"Crop outside source image: {filename}")
            photo = source.crop(box).convert("RGB")
            options = {"lossless": True, "method": 6} if filename.endswith(".webp") else {}
            photo.save(OUT / filename, **options)
            print(f"{filename}: {photo.width}x{photo.height}")


if __name__ == "__main__":
    main()
