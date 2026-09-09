#!/usr/bin/env python3
"""Snap the page stylesheets onto the token type scale.

Audited across four page types, the site rendered 57 distinct type styles.
Twelve different font sizes sat between 11px and 18px, and body copy used
five weights (300/400/500/700/800) for text at the same level -- .section-desc
at 300 next to .sd at 400, both being the same kind of paragraph.

None of that was hierarchy. It was accumulated drift, and it is what makes
the pages read as unresolved even though each section looks fine alone.

This maps every hardcoded font-size to the nearest token step and collapses
the weight set to four deliberate values:

    300 -> 400   there is no "light" tier; it was an accident of two sheets
    500 -> 600   <strong> at 500 is not perceptibly bold
    400, 600, 700, 800 kept -- body, emphasis, sub-head, display

Run from the repo root:  python3 tools/unify_type.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(REPO_ROOT, "assets", "css")
SHEETS = ("site.css", "home.css", "post.css")

# Token -> the px size it resolves to at a 1440px viewport, which is what
# the snapping compares against.
SCALE = [
    ("var(--step--2)", 11.5),
    ("var(--step--1)", 13.6),
    ("var(--step-0)",  16.8),
    ("var(--step-1)",  20.8),
    ("var(--step-2)",  32.0),
    ("var(--step-3)",  48.0),
    ("var(--step-4)",  70.4),
    ("var(--step-5)",  96.0),
]

WEIGHT_MAP = {"300": "400", "500": "600"}

REM = re.compile(r"^\.?\d*\.?\d+rem$")
CLAMP = re.compile(r"^clamp\(([^,]+),[^,]+,\s*([^)]+)\)$")


def to_px(value):
    """Resolve a CSS length to px at a 1440px viewport, or None."""
    value = value.strip()
    clamp = CLAMP.match(value)
    if clamp:
        # A clamp's ceiling is what a desktop actually renders.
        value = clamp.group(2).strip()
    if value.endswith("rem"):
        return float(value[:-3]) * 16
    if value.endswith("px"):
        return float(value[:-2])
    return None


def nearest(px):
    return min(SCALE, key=lambda pair: abs(pair[1] - px))[0]


def snap_sizes(css):
    changes = []

    def replace(match):
        raw = match.group(1).strip()
        important = ""
        if raw.endswith("!important"):
            raw, important = raw[: -len("!important")].strip(), "!important"
        if raw.startswith("var(") or raw in ("inherit", "0"):
            return match.group(0)
        px = to_px(raw)
        if px is None:
            return match.group(0)
        token = nearest(px)
        changes.append((raw, token))
        return f"font-size:{token}{important}"

    css = re.sub(r"font-size:\s*([^;}]+)", replace, css)
    return css, changes


def snap_weights(css):
    changes = []

    def replace(match):
        weight = match.group(1)
        if weight in WEIGHT_MAP:
            changes.append((weight, WEIGHT_MAP[weight]))
            return f"font-weight:{WEIGHT_MAP[weight]}"
        return match.group(0)

    css = re.sub(r"font-weight:\s*(\d{3})", replace, css)
    return css, changes


def main():
    total_sizes = total_weights = 0
    for name in SHEETS:
        path = os.path.join(CSS_DIR, name)
        with open(path, encoding="utf-8") as fh:
            css = fh.read()

        css, sizes = snap_sizes(css)
        css, weights = snap_weights(css)

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(css)

        distinct = sorted({old for old, _ in sizes}, key=lambda v: to_px(v) or 0)
        print(f"{name}: {len(sizes)} font-size -> scale "
              f"({len(distinct)} distinct values collapsed), "
              f"{len(weights)} font-weight normalised")
        total_sizes += len(sizes)
        total_weights += len(weights)

    print(f"\ntotal: {total_sizes} sizes, {total_weights} weights")
    return 0


if __name__ == "__main__":
    sys.exit(main())
