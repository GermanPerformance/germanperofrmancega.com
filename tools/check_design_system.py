#!/usr/bin/env python3
"""Guard the visual system against the three ways it drifted.

The Werkstatt refresh restyled the *named* heading classes and left every
other display-type selector behind, so the site ended up rendering two
different typefaces that both claimed to be "the display font". It also
inherited 258 pictographic emoji used as iconography, in 43 distinct
glyphs, which is what made the pages read as scattered.

Three assertions, each pinned to a root cause:

  1. No pictographic emoji in markup. Icons are inline SVG or mono
     numerals; a colour emoji font is not part of the design system.
     U+2605 BLACK STAR is allowed -- it is typographic, used in "4.5*".

  2. Every selector that declares font-family: var(--font-display) either
     appears in werkstatt.css's display rule or sets its own weight AND
     font-variation-settings. Otherwise it silently falls back to weight
     400 / wdth 100 and looks like a different family.

  3. Page stylesheets declare font-size only from the token scale.
     Hardcoded rem/px sizes are what produced twelve distinct sizes
     between 11px and 18px.

  4. No inline font-size in the markup outside the scale, and no inline
     font-family at all. Inline styles override every stylesheet, so they
     are the one place drift can reappear without any sheet changing --
     seven nav links kept the display face this way after both sheets had
     been changed to move them off it.

Run from the repo root:  python3 tools/check_design_system.py
Exit code 0 = clean, 1 = at least one violation.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(REPO_ROOT, "assets", "css")
PAGE_SHEETS = ("site.css", "home.css", "post.css")

# Pictographs, dingbats, symbols. U+2605 (*) is deliberately excluded.
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF"      # pictographs, transport, symbols
    "←-⇿"               # arrows
    "☀-☄☆-⛿"               # misc symbols
    "✀-➿"               # dingbats
    "⬀-⯿"               # extra arrows and stars
    "️]"                     # variation selector-16
)

# Sizes allowed outside the token scale: 1px hairlines and 0.
SIZE_OK = re.compile(r"var\(--step|inherit|0")


def pages():
    return sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html"))


def check_emoji():
    """Assertion 1 -- no pictographic emoji anywhere in the markup."""
    hits = []
    for name in pages():
        with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                found = EMOJI.findall(line)
                if found:
                    hits.append((name, lineno, "".join(found)))
    return hits


COMMENT = re.compile(r"/\*.*?\*/", re.S)


def display_selectors():
    """Selectors werkstatt.css grants the display treatment."""
    with open(os.path.join(CSS_DIR, "werkstatt.css"), encoding="utf-8") as fh:
        css = fh.read()
    match = re.search(r"\n(h1,\s*h2,\s*h3,[^{]*)\{", css)
    if not match:
        return set()
    return {s.strip() for s in match.group(1).replace("\n", " ").split(",") if s.strip()}


def check_display_font():
    """Assertion 2 -- no display selector falls back to 400 / wdth 100."""
    covered = display_selectors()
    orphans = []
    for sheet in PAGE_SHEETS:
        with open(os.path.join(CSS_DIR, sheet), encoding="utf-8") as fh:
            css = COMMENT.sub("", fh.read())
        pattern = r"([^{}]+)\{([^}]*font-family:\s*var\(--font-display\)[^}]*)\}"
        for rule in re.finditer(pattern, css):
            body = rule.group(2)
            self_styled = "font-weight" in body and "font-variation-settings" in body
            for sel in (s.strip() for s in rule.group(1).split(",")):
                if not sel or self_styled:
                    continue
                # A descendant of a covered selector already inherits the
                # weight and width axis; only its own key part must match.
                if any(part in covered for part in sel.split()):
                    continue
                if sel not in covered:
                    orphans.append((sheet, sel))
    return orphans


def check_font_sizes():
    """Assertion 3 -- page sheets size type from the token scale only."""
    offenders = []
    for sheet in PAGE_SHEETS:
        with open(os.path.join(CSS_DIR, sheet), encoding="utf-8") as fh:
            css = COMMENT.sub("", fh.read())
        for match in re.finditer(r"font-size:\s*([^;}]+)", css):
            value = match.group(1).strip()
            if not SIZE_OK.search(value):
                line = css[: match.start()].count("\n") + 1
                offenders.append((sheet, line, value))
    return offenders


def check_inline_sizes():
    """Assertion 4 -- inline font-size must come from the scale."""
    offenders = []
    for name in pages():
        with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for match in re.finditer(r"font-size:\s*([^;\"]+)", line):
                    if not SIZE_OK.search(match.group(1)):
                        offenders.append((name, lineno, match.group(1).strip()))
                for match in re.finditer(r"style=\"[^\"]*?(font-family:[^;\"]+)", line):
                    offenders.append((name, lineno, match.group(1).strip()))
    return offenders


def report(title, rows, formatter):
    print(f"\n{title}")
    print("-" * 74)
    if not rows:
        print("  OK")
        return 0
    for row in rows[:20]:
        print("  " + formatter(row))
    if len(rows) > 20:
        print(f"  ... and {len(rows) - 20} more")
    return len(rows)


def main():
    emoji = check_emoji()
    orphans = check_display_font()
    sizes = check_font_sizes()

    total = 0
    total += report(
        f"1. Pictographic emoji in markup ({sum(len(h[2]) for h in emoji)} glyphs)",
        emoji, lambda r: f"{r[0]}:{r[1]}  {r[2]}")
    total += report(
        "2. Display-font selectors with no weight/width set",
        orphans, lambda r: f"{r[0]:10s} {r[1]}")
    total += report(
        "3. Off-scale font-size declarations",
        sizes, lambda r: f"{r[0]:10s}:{r[1]:<5d} font-size: {r[2]}")
    total += report(
        "4. Inline type declarations in markup",
        check_inline_sizes(), lambda r: f"{r[0]}:{r[1]}  {r[2]}")

    print()
    if total:
        print(f"{total} design-system violation(s)")
        return 1
    print("Design system consistent across all pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
