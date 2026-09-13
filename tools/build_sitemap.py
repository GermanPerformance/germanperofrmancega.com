#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages actually on disk.

The previous sitemap was a hand-maintained list with no <lastmod>, so search
engines had no signal about what had changed. It also risked drifting out of
sync with the real page set.

<priority> and <changefreq> are deliberately omitted: Google has ignored both
for years, so they add noise rather than signal.

Pages marked noindex (404.html) are excluded, and so is any page whose
canonical names a different URL: a redirect stub (tools/redirects.py) or
a page canonicalised elsewhere must not be listed, or the sitemap would
contradict the page and repeat the target.

Run from the repo root:  python3 tools/build_sitemap.py
"""

import datetime
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"


def choose_date(commit_date, dirty, today):
    """The page's last commit date, unless it has changed since: a page
    edited in the working tree will be committed when the site deploys, so
    its date is today. A page git has never seen is dated today too."""
    if dirty or not commit_date:
        return today.isoformat()
    return commit_date


def git(*args):
    result = subprocess.run(["git", *args], cwd=REPO_ROOT,
                            capture_output=True, text=True)
    return result.stdout.strip()


def last_modified(name):
    """Date of the file's last real change, see choose_date."""
    commit_date = git("log", "-1", "--format=%cs", "--", name)
    dirty = bool(git("status", "--porcelain", "--", name))
    return choose_date(commit_date, dirty, datetime.date.today())


def own_url(name):
    return f"{SITE}/" if name == "index.html" else f"{SITE}/{name}"


def is_own_canonical(name, canonical):
    """True when the page's canonical is its own URL."""
    return canonical == own_url(name)


def is_indexable(path):
    with open(path, encoding="utf-8") as fh:
        head = fh.read(4000)
    return "noindex" not in head


def canonical(path, name):
    """Prefer the page's own canonical so the sitemap cannot contradict it."""
    with open(path, encoding="utf-8") as fh:
        m = re.search(r'<link rel="canonical" href="([^"]*)"', fh.read())
    return m.group(1) if m else own_url(name)


def main():
    urls = []
    for name in sorted(os.listdir(REPO_ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(REPO_ROOT, name)
        if not is_indexable(path):
            print(f"  excluded (noindex): {name}")
            continue
        url = canonical(path, name)
        if not is_own_canonical(name, url):
            print(f"  excluded (canonical elsewhere): {name}")
            continue
        urls.append((url, last_modified(name)))

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
