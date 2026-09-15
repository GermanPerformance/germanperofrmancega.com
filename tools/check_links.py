#!/usr/bin/env python3
"""Verify every internal link on the site resolves.

Checks two classes of link that both silently 404 in a static site:
  1. file targets   -- href="/foo"            -> foo.html must exist on disk
  2. anchor targets -- href="/foo#bar"        -> "bar" must be an id in foo.html

Links are written in their clean form (tools/urls.py): "/" is index.html
and "/foo" is foo.html. The old "foo.html" form still resolves, so a
stray one is not a broken link -- check_catalog_consistency.py is what
refuses it. A third class is a link to a retired address: its redirect
stub is on disk, so the link resolves, but a live page linking it sends
readers through a redirect, and it fails here.

Run from the repo root:  python3 tools/check_links.py
Exit code 0 = all links resolve, 1 = broken links found.
"""

import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redirects import is_redirect  # noqa: E402
from urls import file_for  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Schemes we never resolve locally.
EXTERNAL_PREFIXES = ("http://", "https://", "tel:", "mailto:", "javascript:", "data:")

HREF_RE = re.compile(r'href="([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')


def html_files(root):
    """Every HTML page at the repo root, sorted for stable output."""
    return sorted(f for f in os.listdir(root) if f.endswith(".html"))


def ids_in(path, _cache={}):
    """Set of element ids declared in a file. Cached; missing file -> empty set."""
    if path not in _cache:
        try:
            with open(path, encoding="utf-8") as fh:
                _cache[path] = set(ID_RE.findall(fh.read()))
        except OSError:
            _cache[path] = set()
    return _cache[path]


def split_href(href, source):
    """Resolve an href to (target_file, anchor). Returns None if not checkable."""
    if href.startswith(EXTERNAL_PREFIXES) or href.startswith("//"):
        return None
    if href in ("#", ""):
        return None

    path, _, anchor = href.partition("#")
    # A bare "#anchor" refers to the current page; anything else is a
    # clean address or an asset path, both served from the repo root.
    target = source if path == "" else file_for(href)
    return target, anchor


def check(root):
    """Yield (source, href, reason) for every broken internal link."""
    for source in html_files(root):
        with open(os.path.join(root, source), encoding="utf-8") as fh:
            content = fh.read()

        for href in HREF_RE.findall(content):
            resolved = split_href(href, source)
            if resolved is None:
                continue
            target, anchor = resolved

            target_path = os.path.join(root, target)
            if not os.path.isfile(target_path):
                yield source, href, f"missing file: {target}"
                continue
            # A retired address still resolves (its stub is on disk), so a
            # stale link would pass unnoticed and send readers and crawlers
            # through a redirect. Only a stub may link a stub's successor.
            if is_redirect(target) and not is_redirect(source):
                yield source, href, f"links a retired page: {target}"
                continue

            if anchor and anchor not in ids_in(target_path):
                yield source, href, f'missing id "{anchor}" in {target}'


def main():
    broken = list(check(REPO_ROOT))

    if not broken:
        total = len(html_files(REPO_ROOT))
        print(f"OK: all internal links resolve across {total} pages.")
        return 0

    # Group by reason so 240 identical failures read as one line, not 240.
    by_reason = defaultdict(list)
    for source, href, reason in broken:
        by_reason[reason].append(source)

    print(f"BROKEN: {len(broken)} internal links across "
          f"{len({s for s, _, _ in broken})} pages\n")
    for reason, sources in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        print(f"  [{len(sources):>3}x] {reason}")
        print(f"         e.g. {sources[0]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
