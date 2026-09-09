#!/usr/bin/env python3
"""Snap inline style="font-size:..." onto the token scale.

Extracting the stylesheets moved the rules out of the pages but left 55
inline font-size declarations behind, in thirteen distinct values. They are
invisible to a stylesheet-only audit and they override everything, so they
were quietly reintroducing the drift the scale exists to prevent.

Two specific inline treatments are removed rather than resized:

  * an empty absolutely-positioned div that held a 10rem lightning emoji,
    now a 10rem box containing nothing
  * a 10rem numeral painted with -webkit-text-stroke over a transparent
    fill at 10% alpha -- the same invisible-word treatment removed from
    the h1 stack, applied here to the "STAGE 2" panel

Run from the repo root:  python3 tools/fix_inline_styles.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCALE = [
    ("var(--step--2)", 11.5), ("var(--step--1)", 13.6), ("var(--step-0)", 16.8),
    ("var(--step-1)",  20.8), ("var(--step-2)",  32.0), ("var(--step-3)", 48.0),
    ("var(--step-4)",  70.4), ("var(--step-5)",  96.0),
]

DEAD_GHOST = re.compile(
    r'\s*<div style="font-size:10rem; opacity:0\.08; position:absolute;"></div>')

# The transparent-fill numeral, replaced with a solid recessive one.
STROKE_NUMERAL = re.compile(
    r'-webkit-text-stroke:1px rgba\(240,237,232,0\.1\); color:transparent;')


def nearest(rem):
    px = float(rem) * 16
    return min(SCALE, key=lambda pair: abs(pair[1] - px))[0]


def main():
    sizes = ghosts = strokes = 0
    touched = 0

    for name in sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")):
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html

        html, n = DEAD_GHOST.subn("", html)
        ghosts += n
        html, n = STROKE_NUMERAL.subn("color:var(--graphite);", html)
        strokes += n

        def snap(match):
            nonlocal sizes
            sizes += 1
            return f"font-size:{nearest(match.group(1))}"

        html = re.sub(r"font-size:\s*(\d*\.?\d+)rem", snap, html)

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            touched += 1

    print(f"{touched} pages rewritten")
    print(f"  {sizes:4d} inline font-size -> token scale")
    print(f"  {ghosts:4d} dead ghost container(s) removed")
    print(f"  {strokes:4d} transparent-fill numeral(s) given a solid colour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
