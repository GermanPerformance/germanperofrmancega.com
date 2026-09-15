#!/usr/bin/env python3
"""One address per page: the file's name without ".html", the homepage "/".

GitHub Pages serves about.html at /about as well as at /about.html, and
index.html at / as well as at /index.html, and it redirects neither. So
every page has two working addresses, and whichever one the site links
to is the one search engines take as the page's vote for itself. The
sitemap, the canonicals and every outside listing name the clean form,
so every link the site writes must too: 515 "Home" links to /index.html
against a sitemap that says / had Google weighing two homepages.

This module is the only place the clean form is spelled out. Generators
call href_for() / page_url() when they write a link; apply_redesign.py
runs clean_links() over every page as its normaliser, so a hand-written
".html" link anywhere on the site comes out clean too; checkers call
file_for() to find the file behind a clean address. The catalog and the
tools keep naming pages by file name -- that is what is on disk -- and
only the addresses change.
"""

import re

SITE = "https://germanperformancega.com"
HOME = "index.html"
EXTENSION = ".html"

# A local page link: a bare file name at the repo root, with or without a
# fragment. Nothing with a scheme, a slash or a query string.
PAGE_HREF_RE = re.compile(r'^(?P<name>[A-Za-z0-9._-]+\.html)(?P<fragment>#[^"]*)?$')
LOCAL_HREF_RE = re.compile(r'href="(?P<href>[A-Za-z0-9._-]+\.html(?:#[^"]*)?)"')
# The site's own absolute URL to a page, wherever it appears: canonical,
# og:url, meta refresh, JSON-LD "@id" and "url".
SITE_PAGE_URL_RE = re.compile(re.escape(SITE) + r'/(?P<name>[A-Za-z0-9._-]+)\.html\b')


def page_path(name):
    """The address a page file is served at: "/" for the homepage, "/about"
    for about.html. A ValueError for anything that is not a page file."""
    if "/" in name or not name.endswith(EXTENSION) or name == EXTENSION:
        raise ValueError(f"not a page file: {name!r}")
    if name == HOME:
        return "/"
    return "/" + name[:-len(EXTENSION)]


def page_url(name):
    return SITE + page_path(name)


def href_for(href):
    """A local page link in its clean form. Anything else -- an anchor, a
    scheme, an asset, an already clean address -- is returned as it came."""
    m = PAGE_HREF_RE.match(href)
    if not m:
        return href
    return page_path(m.group("name")) + (m.group("fragment") or "")


def file_for(href):
    """The file behind a local address, clean or not: "/" and "" are the
    homepage, "/about" and "about.html" are about.html. Fragments and query
    strings are dropped; a path that is not a page (an asset) comes back
    with only those dropped."""
    path = href.partition("#")[0].partition("?")[0].lstrip("/")
    if path == "":
        return HOME
    if "/" in path or "." in path:
        return path
    return path + EXTENSION


def url_for_href(href):
    return page_url(file_for(href))


def clean_links(html):
    """Every local page link and every absolute link to a page on this site,
    in clean form. Idempotent; leaves other hosts' URLs and assets alone."""
    html = LOCAL_HREF_RE.sub(lambda m: f'href="{href_for(m.group("href"))}"', html)
    return SITE_PAGE_URL_RE.sub(lambda m: page_url(m.group("name") + EXTENSION), html)
