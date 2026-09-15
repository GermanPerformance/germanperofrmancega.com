#!/usr/bin/env python3
"""Write a redirect stub at every retired URL in tools/redirects.py.

Each stub is the smallest page that moves a visitor on: an instant meta
refresh (Google reads a 0-second refresh as a permanent redirect), a
canonical naming the successor, `location.replace` so the old URL does
not sit in the browser's history, and one visible link for anyone whose
browser did none of that. No stylesheet, no analytics, no schema, no
description -- there is nothing here to index, and the other tools skip
these files by name.

The link text is the successor's own <title> without the site name, so a
stub never describes a page in words the page itself does not use.

Idempotent. Run from the repo root:  python3 tools/build_redirects.py
"""

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redirects import REDIRECTS  # noqa: E402
from urls import href_for, page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_NAME = "German Performance"


def page_title(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        match = re.search(r"<title>(.*?)</title>", fh.read(), re.S)
    if not match:
        raise SystemExit(f"{name}: no <title>")
    return html.unescape(match.group(1).strip())


def short_title(title):
    return re.sub(r"\s*\|\s*" + re.escape(SITE_NAME) + r"\s*$", "", title)


def stub(old, new, new_title):
    url = page_url(new)
    label = html.escape(short_title(new_title))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Moved: {label}</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<script>location.replace("{url}")</script>
</head>
<body>
<p>This page has moved to <a href="{href_for(new)}">{label}</a>.</p>
</body>
</html>
"""


def main():
    written = 0
    for old, new in sorted(REDIRECTS.items()):
        target = os.path.join(REPO_ROOT, new)
        if not os.path.exists(target):
            raise SystemExit(f"{old}: successor {new} is not on disk")
        if new in REDIRECTS:
            raise SystemExit(f"{old}: successor {new} is itself a redirect")
        content = stub(old, new, page_title(new))
        path = os.path.join(REPO_ROOT, old)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current != content:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            written += 1
        print(f"  {old} -> {new}")
    print(f"redirects: {written} of {len(REDIRECTS)} stubs written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
