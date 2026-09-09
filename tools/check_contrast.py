#!/usr/bin/env python3
"""Check the design tokens against WCAG AA contrast requirements.

Lighthouse flagged colour contrast on both page types. Rather than fixing
individual rules, this validates the token palette itself, so a colour cannot
regress during a redesign without failing here first.

Thresholds (WCAG 2.1 AA):
    4.5:1  normal body text
    3.0:1  large text (>=24px, or >=18.66px bold) and UI boundaries

Run from the repo root:  python3 tools/check_contrast.py
Exit code 0 = every declared pair passes, 1 = at least one fails.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_CSS = os.path.join(REPO_ROOT, "assets", "css", "tokens.css")

# (foreground token, background token, minimum ratio, what it is used for)
PAIRS = [
    ("--white",      "--black",   4.5, "primary text on page ground"),
    ("--white",      "--carbon",  4.5, "primary text on raised panels"),
    ("--white",      "--steel",   4.5, "primary text on cards"),
    ("--light",      "--black",   4.5, "body copy"),
    ("--light",      "--carbon",  4.5, "body copy on panels"),
    ("--light",      "--steel",   4.5, "body copy on cards"),
    ("--silver",     "--black",   4.5, "secondary text"),
    ("--silver",     "--carbon",  4.5, "secondary text on panels"),
    ("--silver",     "--steel",   4.5, "secondary text on cards"),
    ("--muted",      "--black",   4.5, "tertiary text, footer copy"),
    ("--muted",      "--carbon",  4.5, "tertiary text on panels"),
    ("--gold",       "--black",   4.5, "precision accent, spec labels"),
    ("--gold",       "--carbon",  4.5, "precision accent on panels"),
    ("--gold",       "--steel",   4.5, "precision accent on cards"),
    ("--red-b",      "--black",   4.5, "action text under 24px"),
    ("--red-b",      "--carbon",  4.5, "action text on panels"),
    ("--red-b",      "--steel",   4.5, "action text on cards"),
    # Large display type and solid buttons only need 3:1.
    ("--red",        "--black",   3.0, "display type / large headings"),
    ("--white",      "--red",     4.5, "button label on the action colour"),
]


def parse_tokens(path):
    with open(path, encoding="utf-8") as fh:
        css = fh.read()
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", css))


def to_rgb(value):
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = luminance(to_rgb(fg)), luminance(to_rgb(bg))
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    tokens = parse_tokens(TOKENS_CSS)
    failures = []

    print(f"{'foreground':16s}{'background':14s}{'ratio':>7s}  {'min':>5s}  use")
    print("-" * 88)
    for fg, bg, minimum, use in PAIRS:
        if fg not in tokens or bg not in tokens:
            failures.append((fg, bg, "token not defined"))
            print(f"{fg:16s}{bg:14s}{'--':>7s}  {minimum:5.1f}  MISSING TOKEN")
            continue
        r = ratio(tokens[fg], tokens[bg])
        ok = r >= minimum
        mark = "" if ok else "   <-- FAILS"
        if not ok:
            failures.append((fg, bg, f"{r:.2f} < {minimum}"))
        print(f"{fg:16s}{bg:14s}{r:7.2f}  {minimum:5.1f}  {use}{mark}")

    print()
    if failures:
        print(f"{len(failures)} contrast failure(s)")
        return 1
    print(f"All {len(PAIRS)} token pairs meet WCAG AA.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
