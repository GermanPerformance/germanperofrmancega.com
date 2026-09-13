#!/usr/bin/env python3
"""Guard the breadcrumb trail every make's service page carries.

A make's page sits under its repair hub, and the crumb says so: Home /
BMW Repair / BMW Oil Change. tools/fix_breadcrumbs.py writes that trail
from the catalog; tools/build_schema.py reads it back into BreadcrumbList.

Run from the repo root:  python3 tools/test_fix_breadcrumbs.py
"""

import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import apply_redesign  # noqa: E402
import fix_breadcrumbs as fb  # noqa: E402
import service_catalog as cat  # noqa: E402

MAKE_PAGE = "bmw-oil-change-snellville-ga.html"
GENERIC_PAGE = "german-car-oil-change-snellville-ga.html"
HUB = "bmw-repair-snellville-ga.html"


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


class TrailTests(unittest.TestCase):
    def test_make_page_sits_under_its_hub(self):
        self.assertEqual(fb.trail(MAKE_PAGE), (
            ("Home", "index.html"),
            ("BMW Repair", HUB),
            ("BMW Oil Change — Snellville, GA", None),
        ))

    def test_generic_page_and_hub_are_two_levels(self):
        self.assertEqual(fb.trail(GENERIC_PAGE), (
            ("Home", "index.html"),
            ("German Car Oil Change — Snellville, GA", None),
        ))
        self.assertEqual(len(fb.trail(HUB)), 2)

    def test_markup_uses_the_existing_classes_only(self):
        markup = fb.breadcrumb(MAKE_PAGE)
        self.assertEqual(markup, (
            '<div class="breadcrumb"><a href="index.html">Home</a><span>/</span>'
            f'<a href="{HUB}">BMW Repair</a><span>/</span>'
            '<span class="crumb-here">BMW Oil Change — Snellville, GA</span></div>'))
        self.assertNotIn("style=", markup)

    def test_every_make_page_trail_ends_with_its_catalog_name(self):
        for slug in fb.pages():
            *_, (label, href) = fb.trail(slug)
            self.assertIsNone(href)
            self.assertEqual(label, f"{cat.full_label(slug)} — {fb.AREA}")


class TransformTests(unittest.TestCase):
    def test_rewrites_a_live_page_once(self):
        html = read(MAKE_PAGE)
        once = fb.transform(html, MAKE_PAGE)
        self.assertEqual(once.count('<div class="breadcrumb">'), 1)
        self.assertIn(fb.breadcrumb(MAKE_PAGE), once)
        self.assertEqual(fb.transform(once, MAKE_PAGE), once)

    def test_redesign_pass_leaves_the_trail_alone(self):
        once = fb.transform(read(MAKE_PAGE), MAKE_PAGE)
        self.assertEqual(apply_redesign.transform(once), once)

    def test_page_without_a_breadcrumb_is_an_error(self):
        with self.assertRaises(SystemExit):
            fb.transform("<html><body><main></main></body></html>", MAKE_PAGE)

    def test_every_make_page_has_exactly_one_block(self):
        for slug in fb.pages():
            self.assertEqual(len(fb.BLOCK.findall(read(slug))), 1, slug)


class ScopeTests(unittest.TestCase):
    def test_only_make_pages_are_rewritten(self):
        pages = fb.pages()
        hubs = {m.hub for m in cat.MAKES}
        self.assertFalse(hubs & set(pages))
        self.assertTrue(all(cat.make_of(p) for p in pages))
        self.assertEqual(len(pages), len(cat.PAGES) - len(cat.MAKES) - len(cat.GROUPS[0][1]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
