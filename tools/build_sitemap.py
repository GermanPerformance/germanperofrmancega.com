#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages actually on disk.

The previous sitemap was a hand-maintained list with no <lastmod>, so search
engines had no signal about what had changed. It also risked drifting out of
sync with the real page set.

<priority> and <changefreq> are deliberately omitted: Google has ignored both
for years, so they add noise rather than signal.

Pages marked noindex (404.html) are excluded.

Run from the repo root:  python3 tools/build_sitemap.py
"""

import datetime
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"


def last_modified(name):
    """Date of the file's last commit, or today if uncommitted."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", name],
        cwd=REPO_ROOT, capture_output=True, text=True)
    date = result.stdout.strip()
    return date or datetime.date.today().isoformat()


def is_indexable(path):
    with open(path, encoding="utf-8") as fh:
        head = fh.read(4000)
    return "noindex" not in head


def canonical(path, name):
    """Prefer the page's own canonical so the sitemap cannot contradict it."""
    with open(path, encoding="utf-8") as fh:
        m = re.search(r'<link rel="canonical" href="([^"]*)"', fh.read())
    if m:
        return m.group(1)
    return f"{SITE}/" if name == "index.html" else f"{SITE}/{name}"


def main():
    urls = []
    for name in sorted(os.listdir(REPO_ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(REPO_ROOT, name)
        if not is_indexable(path):
            print(f"  excluded (noindex): {name}")
            continue
        urls.append((canonical(path, name), last_modified(name)))

    # Homepage first, then the rest alphabetically.
    urls.sort(key=lambda u: (u[0] != f"{SITE}/", u[0]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, date in urls:
        lines += ["  <url>", f"    <loc>{url}</loc>",
                  f"    <lastmod>{date}</lastmod>", "  </url>"]
    lines.append("</urlset>")

    with open(os.path.join(REPO_ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"sitemap.xml: {len(urls)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
