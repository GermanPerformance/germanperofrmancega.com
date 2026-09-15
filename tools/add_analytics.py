#!/usr/bin/env python3
"""Wire assets/js/analytics.js into every page.

Two edits per page, both deliberately tiny -- the front-end work is being
done in parallel, so this stays out of the markup a redesign would touch:

  * one deferred <script> next to the existing per-page script include
  * data-page-type on <body>, so a call from a brand hub can be told apart
    from a call off the homepage without maintaining a URL list in GA4

Run from the repo root:  python3 tools/add_analytics.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import hubs  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "3"
INCLUDE = f'<script defer src="assets/js/analytics.js?v={VERSION}"></script>'

# The five brand hubs share the -repair suffix with service
# pages like bmw-transmission-repair-…, so they come from the catalog
# rather than a pattern.
HUBS = {slug for slug, _ in hubs()}

EXISTING_SCRIPT = re.compile(
    r'(<script defer src="assets/js/(?:home|site)\.js\?v=\d+"></script>)')
BODY_OPEN = re.compile(r"<body(?![^>]*data-page-type)([^>]*)>")


def page_type(name):
    if name == "index.html":
        return "home"
    if name == "404.html":
        return "error"
    if name in HUBS:
        return "hub"
    if name.startswith("dealer-vs-"):
        return "post"
    return "service"


def main():
    added_script = added_attr = 0
    no_anchor = []

    for name in sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")):
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html

        if "assets/js/analytics.js" not in html:
            html, n = EXISTING_SCRIPT.subn(r"\1\n" + INCLUDE, html, count=1)
            if n:
                added_script += 1
            elif "</body>" in html:
                html = html.replace("</body>", f"  {INCLUDE}\n</body>", 1)
                added_script += 1
                no_anchor.append(name)

        html, n = BODY_OPEN.subn(
            lambda m: f'<body data-page-type="{page_type(name)}"{m.group(1)}>',
            html, count=1)
        added_attr += n

        if html != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)

    print(f"{added_script} pages given the analytics include")
    print(f"{added_attr} pages given data-page-type")
    if no_anchor:
        print(f"  {len(no_anchor)} had no per-page script to anchor to, "
              f"appended before </body>: {', '.join(no_anchor)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
