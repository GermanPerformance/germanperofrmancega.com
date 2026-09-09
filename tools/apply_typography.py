#!/usr/bin/env python3
"""Swap the type system to Archivo + IBM Plex Mono.

Condensed Bebas Neue in heavy red reads as tuner shop or gym -- generic
American aftermarket. The shop's actual advantage is factory-trained
precision, so the type should read engineered rather than loud.

Archivo carries a real width axis, so display type can be genuinely wide:
the proportion of a manufacturer wordmark (Porsche, Audi) rather than a
condensed poster face. One superfamily now covers display and body, which
also means one fewer font to download.

Space Mono gives way to IBM Plex Mono. The monospace micro-labels are the
most characterful part of the existing design and exactly right for a
service-manual aesthetic -- an earlier plan to drop them entirely was wrong.
Plex has genuine engineering-documentation heritage and is more legible at
the 0.6-0.75rem these labels use.

Net: two families instead of three.

Run from the repo root:  python3 tools/apply_typography.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(REPO_ROOT, "assets", "css")

OLD_FONTS_LINK = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?family=[^"]*" rel="stylesheet">')
NEW_FONTS_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Archivo:wdth,wght@62..125,300..900&'
    'family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">')

# Display type gets the width axis; body sits at normal width.
CSS_SUBS = [
    (re.compile(r"'Bebas Neue',\s*sans-serif"), "var(--font-display)"),
    (re.compile(r"'DM Sans',\s*sans-serif"), "var(--font-body)"),
    (re.compile(r"'Space Mono',\s*monospace"), "var(--font-mono)"),
]

HTML_SUBS = [
    ("font-family:'Bebas Neue',sans-serif", "font-family:var(--font-display)"),
    ("font-family:'Space Mono',monospace", "font-family:var(--font-mono)"),
]


def main():
    # --- stylesheets ---
    for name in ("site.css", "home.css", "post.css"):
        path = os.path.join(CSS_DIR, name)
        with open(path, encoding="utf-8") as fh:
            css = fh.read()
        for pattern, replacement in CSS_SUBS:
            css = pattern.sub(replacement, css)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(css)
        print(f"{name}: font families mapped to tokens")

    # --- pages ---
    links, inline = 0, 0
    for name in sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")):
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        original = content

        content, n = OLD_FONTS_LINK.subn(NEW_FONTS_LINK, content)
        links += n
        for old, new in HTML_SUBS:
            if old in content:
                inline += content.count(old)
                content = content.replace(old, new)

        if content != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)

    print(f"pages: {links} font links swapped, {inline} inline declarations mapped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
