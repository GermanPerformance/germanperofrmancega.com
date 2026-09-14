#!/usr/bin/env python3
"""The sitemap's <lastmod> must be the date the page actually changed.

A page edited in the working tree and not yet committed is going to be
committed at deploy time, so its date is today; an untouched page keeps
the date of its last commit.

Run from the repo root:  python3 tools/test_build_sitemap.py
"""

import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sitemap  # noqa: E402

TODAY = datetime.date(2026, 9, 12)


class ChooseDate(unittest.TestCase):
    def test_clean_committed_page_keeps_its_commit_date(self):
        self.assertEqual(build_sitemap.choose_date("2026-07-28", False, TODAY),
                         "2026-07-28")

    def test_dirty_page_is_dated_today(self):
        self.assertEqual(build_sitemap.choose_date("2026-07-28", True, TODAY),
                         "2026-09-12")

    def test_never_committed_page_is_dated_today(self):
        self.assertEqual(build_sitemap.choose_date("", False, TODAY),
                         "2026-09-12")


class PageImage(unittest.TestCase):
    """A page's og:image is listed in the image sitemap, unless it is the
    site-wide fallback card, which says nothing about the page."""

    def test_page_specific_image_is_listed(self):
        html = '<meta property="og:image" content="https://germanperformancega.com/assets/img/services/brake-repair-1100.jpg">'
        self.assertEqual(build_sitemap.page_image(html),
                         "https://germanperformancega.com/assets/img/services/brake-repair-1100.jpg")

    def test_site_fallback_card_is_not_listed(self):
        html = '<meta property="og:image" content="https://germanperformancega.com/og-image.jpg">'
        self.assertIsNone(build_sitemap.page_image(html))

    def test_page_without_image_lists_none(self):
        self.assertIsNone(build_sitemap.page_image("<html></html>"))


class UrlEntry(unittest.TestCase):
    def test_entry_with_image_carries_image_extension(self):
        lines = build_sitemap.url_entry("https://germanperformancega.com/x.html",
                                        "2026-09-14",
                                        "https://germanperformancega.com/a.jpg")
        self.assertIn("    <image:image>", lines)
        self.assertIn("      <image:loc>https://germanperformancega.com/a.jpg</image:loc>", lines)

    def test_entry_without_image_has_no_image_block(self):
        lines = build_sitemap.url_entry("https://germanperformancega.com/x.html",
                                        "2026-09-14", None)
        self.assertFalse(any("image" in l for l in lines))

    def test_ampersand_in_url_is_escaped(self):
        lines = build_sitemap.url_entry("https://germanperformancega.com/a&b.html",
                                        "2026-09-14", None)
        self.assertIn("    <loc>https://germanperformancega.com/a&amp;b.html</loc>", lines)


class Header(unittest.TestCase):
    """A browser opening sitemap.xml renders it through sitemap.xsl, so the
    owner sees a readable table instead of a raw tree. Crawlers ignore the
    processing instruction and read the same XML."""

    def test_stylesheet_instruction_follows_the_xml_declaration(self):
        lines = build_sitemap.header()
        self.assertEqual(lines[0], '<?xml version="1.0" encoding="UTF-8"?>')
        self.assertEqual(lines[1],
                         '<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>')

    def test_image_namespace_is_declared(self):
        self.assertTrue(any('xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
                            in l for l in build_sitemap.header()))


if __name__ == "__main__":
    unittest.main()
