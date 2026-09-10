#!/usr/bin/env python3
"""Guard the measurement layer.

The site shipped five phases of SEO and design work with no analytics at
all, so none of it could be shown to have moved a single phone call. This
checks that the tracking is present, that it is defined in exactly one
place, and that every phone link it depends on is dialable.

Four assertions:

  1. Every page loads assets/js/analytics.js. A page without it is a hole
     in the funnel that shows up as a missing session, not as an error.

  2. Every tel: href is E.164 (tel:+1XXXXXXXXXX). One link on the blog
     post read tel:6783957459 with no country code, which some mobile
     dialers reject outright.

  3. All tel: links point at the same number, so the conversion count
     means one thing.

  4. No inline gtag/dataLayer snippet in the markup. The tracking lives
     in analytics.js only; a second definition in a page would double-count
     or silently shadow the first.

Run from the repo root:  python3 tools/check_analytics.py
Exit code 0 = clean, 1 = at least one violation.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_JS = os.path.join(REPO_ROOT, "assets", "js", "analytics.js")

INCLUDE = re.compile(r'src="assets/js/analytics\.js')
TEL = re.compile(r'href="tel:([^"]*)"')
E164 = re.compile(r"^\+1\d{10}$")
INLINE_TAG = re.compile(r"gtag\(|dataLayer\.push|googletagmanager\.com")


def pages():
    return sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html"))


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def check_include():
    return [name for name in pages() if not INCLUDE.search(read(name))]


def check_tel_format():
    bad = []
    for name in pages():
        for lineno, line in enumerate(read(name).splitlines(), 1):
            for number in TEL.findall(line):
                if not E164.match(number):
                    bad.append((name, lineno, number))
    return bad


def check_tel_consistency():
    numbers = {}
    for name in pages():
        for number in TEL.findall(read(name)):
            numbers.setdefault(number, []).append(name)
    if len(numbers) <= 1:
        return []
    return [(n, len(files)) for n, files in sorted(
        numbers.items(), key=lambda kv: -len(kv[1]))]


def check_no_inline():
    hits = []
    for name in pages():
        for lineno, line in enumerate(read(name).splitlines(), 1):
            if INLINE_TAG.search(line):
                hits.append((name, lineno, line.strip()[:60]))
    return hits


def report(title, rows, formatter):
    print(f"\n{title}")
    print("-" * 74)
    if not rows:
        print("  OK")
        return 0
    for row in rows[:15]:
        print("  " + formatter(row))
    if len(rows) > 15:
        print(f"  ... and {len(rows) - 15} more")
    return len(rows)


def main():
    total = 0
    total += report("1. Pages missing assets/js/analytics.js",
                    check_include(), lambda r: r)
    total += report("2. tel: links that are not E.164",
                    check_tel_format(), lambda r: f"{r[0]}:{r[1]}  tel:{r[2]}")
    total += report("3. More than one phone number in tel: links",
                    check_tel_consistency(), lambda r: f"{r[0]}  ({r[1]} links)")
    total += report("4. Inline gtag/dataLayer in markup",
                    check_no_inline(), lambda r: f"{r[0]}:{r[1]}  {r[2]}")

    print()
    if not os.path.exists(ANALYTICS_JS):
        print("assets/js/analytics.js does not exist")
        return 1

    source = open(ANALYTICS_JS, encoding="utf-8").read()
    match = re.search(r'MEASUREMENT_ID\s*=\s*[\'"]([^\'"]*)[\'"]', source)
    if not match:
        print("analytics.js defines no MEASUREMENT_ID")
        total += 1
    elif (match.group(1) == "G-XXXXXXXXXX"
          or not re.match(r"^G-[A-Z0-9]{6,}$", match.group(1))):
        # Not a failure: the tracking is inert but correct until the real
        # property id is pasted in. Say so loudly rather than passing quietly.
        print(f"NOTE: MEASUREMENT_ID is {match.group(1)!r} -- tracking is "
              "inert until the real GA4 id is set.")

    if total:
        print(f"{total} analytics violation(s)")
        return 1
    print("Measurement layer intact across all pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
