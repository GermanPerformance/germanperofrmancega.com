#!/usr/bin/env python3
"""Replace 258 pictographic emoji with a coherent icon language.

The pages carried 43 distinct colour emoji used as iconography. 222 of the
258 were in span.ci -- the bullet position of service cards -- where 43
different pictograms carried no more information than one consistent mark
would, while destroying the cohesion of every grid they appeared in. A fire
emoji sat on the turbo row and a broom on a cleaning service.

Colour emoji also render in the system emoji font, so they ignore the
design system entirely: they cannot take the palette, they do not scale
with the type, and they look different on every OS.

Three replacements, chosen by what the position actually does:

  span.ci (222)        -> a two-digit mono index, numbered per grid.
                          A service manual numbers its callouts; it does
                          not illustrate them. This is the position where
                          the pictograms were purely decorative.

  span.service-icon (6),
  span.trust-badge (5) -> inline SVG drawn as technical line marks:
                          1.5px stroke, no fill, currentColor, on the same
                          24px grid. These positions are the top of a
                          category card, where an icon does carry meaning.

  div.perf-icon-large (6) -> deleted. A 80px faded emoji in the corner of
                          a text row was decoration with no referent.

  span.dot (14)        -> emptied; the marquee separator is drawn in CSS
                          as a 3px square instead of a U+2726 glyph.

Run from the repo root:  python3 tools/fix_icons.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF←-⇿☀-☄☆-⛿✀-➿⬀-⯿️]+")

# --- the icon set -----------------------------------------------------------
# 24px grid, 1.5 stroke, no fill. Drawn as instrument marks rather than
# illustrations: a calibration crosshair, a vented disc, a piston and rod.
SVG = {
    "crosshair": '<circle cx="12" cy="12" r="7.5"/><circle cx="12" cy="12" r="1.6"/>'
                 '<path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3"/>',
    "disc":      '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/>'
                 '<path d="M14.5 14.5 18.4 18.4M9.5 9.5 5.6 5.6'
                 'M14.5 9.5 18.4 5.6M9.5 14.5 5.6 18.4"/>',
    "bolt":      '<path d="M13 2 5 13h6l-2 9 8-11h-6l2-9Z"/>',
    "piston":    '<rect x="7" y="3" width="10" height="7" rx="1"/>'
                 '<path d="M9 6h6M12 10v5"/><circle cx="12" cy="18.5" r="3.2"/>',
    "thermo":    '<path d="M14 14.4V5a2 2 0 1 0-4 0v9.4a4 4 0 1 0 4 0Z"/>'
                 '<path d="M12 8v7"/>',
    "magnifier": '<circle cx="10.5" cy="10.5" r="7"/><path d="M15.6 15.6 21 21'
                 'M10.5 7.5v6M7.5 10.5h6"/>',
    "phone":     '<path d="M6.4 3h3l1.5 4-2 1.5a11 11 0 0 0 5.6 5.6L16 12l4 1.5v3'
                 'a2 2 0 0 1-2.2 2A16 16 0 0 1 4.5 5.2 2 2 0 0 1 6.4 3Z"/>',
    "gear":      '<circle cx="12" cy="12" r="3.4"/><circle cx="12" cy="12" r="7.4"/>'
                 '<path d="M12 4.6V2M12 19.4V22M4.6 12H2M19.4 12H22'
                 'M17.2 6.8 19 5M6.8 17.2 5 19M17.2 17.2 19 19M6.8 6.8 5 5"/>',
    "check":     '<path d="M4 12.4 9.4 17.8 20 6.6"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="1.5"/>'
                 '<rect x="9" y="2" width="6" height="4" rx="1"/>'
                 '<path d="M9 11h6M9 15h6"/>',
    "shield":    '<path d="M12 2 20 5.4v6c0 5-3.5 8.6-8 10.6-4.5-2-8-5.6-8-10.6v-6L12 2Z"/>'
                 '<path d="M9 12l2.2 2.2L15.4 10"/>',
}

# Matched on the card's own heading text, not on document order, so the
# mapping survives a section being reordered.
BY_HEADING = [
    ("scheduled maintenance",   "crosshair"),
    ("brakes",                  "disc"),
    ("electrical",              "bolt"),
    ("engine &",                "piston"),
    ("cooling",                 "thermo"),
    ("pre-purchase",            "magnifier"),
    ("contact us",              "phone"),
    ("what we fix",             "gear"),
    ("preferred shop",          "check"),
    ("our guarantee",           "shield"),
    ("digital inspection",      "clipboard"),
]


def icon_markup(name):
    return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{SVG[name]}</svg>')


def heading_after(html, pos, window=340):
    """The card title that follows this icon, lowercased."""
    tail = html[pos:pos + window]
    match = re.search(r'<(?:h3|div)[^>]*class="(?:service-name|trust-card-title)"[^>]*>'
                      r'([^<]+)', tail)
    return match.group(1).strip().lower() if match else ""


def pick_icon(heading):
    for needle, name in BY_HEADING:
        if needle in heading:
            return name
    return None


def replace_svg_icons(html, counters):
    """span.service-icon and span.trust-badge -> inline SVG."""
    pattern = re.compile(
        r'<span class="(service-icon|trust-badge)">\s*[^<]*?\s*</span>')

    def sub(match):
        heading = heading_after(html, match.end())
        name = pick_icon(heading)
        if name is None:
            counters["unmapped"] += 1
            return match.group(0)
        counters["svg"] += 1
        return (f'<span class="{match.group(1)} ico-wrap">'
                f'{icon_markup(name)}</span>')

    return pattern.sub(sub, html)


def replace_ci_numerals(html, counters):
    """span.ci -> a two-digit index, restarting at each grid."""
    tokens = list(re.finditer(r'class="g[2-5]\b|<span class="ci">[^<]*</span>', html))
    out, cursor, index = [], 0, 0
    for token in tokens:
        if token.group(0).startswith('class="g'):
            index = 0
            continue
        index += 1
        counters["ci"] += 1
        out.append(html[cursor:token.start()])
        out.append(f'<span class="ci">{index:02d}</span>')
        cursor = token.end()
    out.append(html[cursor:])
    return "".join(out)


def strip_decoration(html, counters):
    """Remove the oversized decorative emoji and the marquee glyph."""
    html, n = re.subn(r'\s*<div class="perf-icon-large">[^<]*</div>', "", html)
    counters["perf"] += n
    html, n = re.subn(r'<span class="dot">[^<]*</span>',
                      '<span class="dot" aria-hidden="true"></span>', html)
    counters["dot"] += n
    return html


def main():
    counters = {"svg": 0, "ci": 0, "perf": 0, "dot": 0, "stray": 0, "unmapped": 0}
    touched = 0

    for name in sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")):
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html

        html = replace_svg_icons(html, counters)
        html = replace_ci_numerals(html, counters)
        html = strip_decoration(html, counters)

        # Anything left is a stray glyph inside link or button text.
        html, n = EMOJI.subn("", html)
        counters["stray"] += n
        # Removing an inline glyph from link text leaves a leading space.
        # This used to be a blanket re.sub(r">\\s+([A-Z(])", r">\\1"), which
        # also matched '</strong> Under' and deleted the word space in
        # twelve places of running prose. Scope it to the elements a glyph
        # was actually removed from: anchors and buttons.
        html = re.sub(r"(<(?:a|button)\b[^>]*>)\s+(?=[A-Z(])", r"\1", html)

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            touched += 1

    print(f"{touched} pages rewritten")
    print(f"  {counters['svg']:4d} emoji -> inline SVG icons")
    print(f"  {counters['ci']:4d} emoji -> mono grid index")
    print(f"  {counters['perf']:4d} decorative icon blocks removed")
    print(f"  {counters['dot']:4d} marquee glyphs -> CSS square")
    print(f"  {counters['stray']:4d} stray glyphs stripped")
    if counters["unmapped"]:
        print(f"  {counters['unmapped']:4d} UNMAPPED -- heading not in BY_HEADING")
    return 1 if counters["unmapped"] else 0


if __name__ == "__main__":
    sys.exit(main())
