#!/usr/bin/env python3
"""tools/urls.py: one address per page, with no file extension on it.

Run from the repo root:  python3 tools/test_urls.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import urls  # noqa: E402

SITE = "https://germanperformancega.com"


class PagePath(unittest.TestCase):
    def test_drops_the_extension(self):
        self.assertEqual(urls.page_path("index.html"), "/")
        self.assertEqual(urls.page_path("about.html"), "/about")
        self.assertEqual(urls.page_path("bmw-oil-change-snellville-ga.html"),
                         "/bmw-oil-change-snellville-ga")

    def test_refuses_what_is_not_a_page(self):
        for name in ("assets/css/site.css", "sitemap.xml", "", "about", "a/b.html"):
            with self.assertRaises(ValueError, msg=name):
                urls.page_path(name)

    def test_page_url_is_absolute(self):
        self.assertEqual(urls.page_url("index.html"), f"{SITE}/")
        self.assertEqual(urls.page_url("about.html"), f"{SITE}/about")


class HrefFor(unittest.TestCase):
    def test_rewrites_page_links_and_keeps_fragments(self):
        self.assertEqual(urls.href_for("index.html"), "/")
        self.assertEqual(urls.href_for("index.html#faq"), "/#faq")
        self.assertEqual(urls.href_for("about.html"), "/about")
        self.assertEqual(urls.href_for("contact.html#map"), "/contact#map")

    def test_leaves_everything_else_alone(self):
        for href in ("/", "/about", "/#faq", "#reviews", "tel:+16783957459",
                     "mailto:x@y.z", "https://example.com/a.html",
                     "assets/css/site.css?v=31", "assets/img/logo.webp", ""):
            self.assertEqual(urls.href_for(href), href)


class FileFor(unittest.TestCase):
    def test_is_the_inverse_of_href_for(self):
        cases = {"/": "index.html", "": "index.html", "/about": "about.html",
                 "about": "about.html", "/about#map": "about.html",
                 "/about?x=1": "about.html", "/about.html": "about.html",
                 "index.html#faq": "index.html",
                 "assets/css/site.css?v=31": "assets/css/site.css"}
        for href, name in cases.items():
            self.assertEqual(urls.file_for(href), name, href)

    def test_url_for_href_resolves_a_page_link(self):
        for href in ("/", "index.html", "index.html#faq"):
            self.assertEqual(urls.url_for_href(href), f"{SITE}/", href)
        for href in ("/about", "about.html", "/about#map"):
            self.assertEqual(urls.url_for_href(href), f"{SITE}/about", href)


class CleanLinks(unittest.TestCase):
    def test_rewrites_relative_hrefs(self):
        page = ('<a href="index.html">Home</a> <a href="index.html#faq">FAQ</a> '
                '<a href="about.html">About</a> <a href="#top">Top</a> '
                '<a href="tel:+16783957459">Call</a> '
                '<link rel="stylesheet" href="assets/css/site.css?v=31">')
        self.assertEqual(urls.clean_links(page), (
            '<a href="/">Home</a> <a href="/#faq">FAQ</a> '
            '<a href="/about">About</a> <a href="#top">Top</a> '
            '<a href="tel:+16783957459">Call</a> '
            '<link rel="stylesheet" href="assets/css/site.css?v=31">'))

    def test_rewrites_absolute_site_urls_wherever_they_appear(self):
        page = (f'<link rel="canonical" href="{SITE}/about.html">\n'
                f'<meta property="og:url" content="{SITE}/about.html">\n'
                f'<meta http-equiv="refresh" content="0; url={SITE}/index.html">\n'
                f'"@id": "{SITE}/about.html#webpage",\n'
                f'"image": "{SITE}/og-image.jpg"\n'
                '<a href="https://example.com/about.html">elsewhere</a>')
        self.assertEqual(urls.clean_links(page), (
            f'<link rel="canonical" href="{SITE}/about">\n'
            f'<meta property="og:url" content="{SITE}/about">\n'
            f'<meta http-equiv="refresh" content="0; url={SITE}/">\n'
            f'"@id": "{SITE}/about#webpage",\n'
            f'"image": "{SITE}/og-image.jpg"\n'
            '<a href="https://example.com/about.html">elsewhere</a>'))

    def test_is_idempotent(self):
        page = f'<a href="index.html#faq">x</a> {SITE}/about.html'
        once = urls.clean_links(page)
        self.assertEqual(urls.clean_links(once), once)


if __name__ == "__main__":
    unittest.main(verbosity=0)
