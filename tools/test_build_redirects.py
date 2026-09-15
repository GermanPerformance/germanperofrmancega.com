#!/usr/bin/env python3
"""A retired URL must land the visitor, and the crawler, on its successor.

Run from the repo root:  python3 tools/test_build_redirects.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_redirects  # noqa: E402
import build_sitemap  # noqa: E402
from redirects import REDIRECTS, site_pages  # noqa: E402
from urls import page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"


class Mapping(unittest.TestCase):
    def test_every_target_is_a_real_page_on_disk(self):
        for old, new in REDIRECTS.items():
            self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, new)), f"{old} -> {new} missing")

    def test_no_target_is_itself_a_redirect(self):
        for old, new in REDIRECTS.items():
            self.assertNotIn(new, REDIRECTS, f"{old} -> {new} would chain")

    def test_site_pages_excludes_stubs_and_non_html(self):
        names = ["index.html", "audi-timing-belt-snellville-ga.html", "robots.txt", "about.html"]
        self.assertEqual(site_pages(names), ["about.html", "index.html"])


class Stub(unittest.TestCase):
    def setUp(self):
        self.html = build_redirects.stub("audi-timing-belt-snellville-ga.html",
                                         "audi-repair.html",
                                         "Audi Repair & Service Snellville GA | German Performance")

    def test_instant_meta_refresh_to_the_absolute_url(self):
        self.assertIn(f'<meta http-equiv="refresh" content="0; url={SITE}/audi-repair">', self.html)

    def test_canonical_names_the_successor(self):
        self.assertIn(f'<link rel="canonical" href="{SITE}/audi-repair">', self.html)

    def test_browsers_get_a_script_and_people_get_a_link(self):
        self.assertIn(f'location.replace("{SITE}/audi-repair")', self.html)
        self.assertIn('<a href="/audi-repair">Audi Repair &amp; Service Snellville GA</a>', self.html)

    def test_successor_is_named_without_its_extension(self):
        self.assertNotIn(".html", self.html.split("<title>")[1])

    def test_stub_is_not_indexable_content(self):
        self.assertNotIn('name="description"', self.html)
        self.assertNotIn("analytics.js", self.html)
        self.assertNotIn("application/ld+json", self.html)


class Sitemap(unittest.TestCase):
    def test_a_page_canonicalised_elsewhere_is_not_listed(self):
        self.assertFalse(build_sitemap.is_own_canonical(
            "audi-timing-belt-snellville-ga.html", f"{SITE}/audi-repair"))
        self.assertTrue(build_sitemap.is_own_canonical(
            "audi-repair.html", f"{SITE}/audi-repair"))
        self.assertFalse(build_sitemap.is_own_canonical(
            "audi-repair.html", f"{SITE}/audi-repair.html"))
        self.assertTrue(build_sitemap.is_own_canonical("index.html", f"{SITE}/"))


class OnDisk(unittest.TestCase):
    def test_every_stub_exists_and_is_current(self):
        for old, new in REDIRECTS.items():
            path = os.path.join(REPO_ROOT, old)
            self.assertTrue(os.path.exists(path), f"{old} not built")
            with open(path, encoding="utf-8") as fh:
                self.assertIn(f'url={page_url(new)}"', fh.read())

    def test_no_stub_in_the_sitemap(self):
        with open(os.path.join(REPO_ROOT, "sitemap.xml"), encoding="utf-8") as fh:
            sitemap = fh.read()
        for old in REDIRECTS:
            self.assertNotIn(old, sitemap)


if __name__ == "__main__":
    unittest.main()
