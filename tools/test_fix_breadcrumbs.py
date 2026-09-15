#!/usr/bin/env python3
"""Guard the breadcrumb trail every catalog page carries.

A hub and a make-agnostic page are two levels: Home / BMW Repair —
Snellville, GA. tools/fix_breadcrumbs.py writes that trail from the
catalog for the generators; tools/build_schema.py reads it back into
BreadcrumbList. Since the make job pages were consolidated into the hubs
(2026-09-15) there is no third level and nothing for main() to rewrite.

Run from the repo root:  python3 tools/test_fix_breadcrumbs.py
"""

import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import apply_redesign  # noqa: E402
import fix_breadcrumbs as fb  # noqa: E402
import service_catalog as cat  # noqa: E402

GENERIC_PAGE = "german-car-oil-change.html"
HUB = "bmw-repair.html"


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


class TrailTests(unittest.TestCase):
    def test_hub_is_two_levels(self):
        self.assertEqual(fb.trail(HUB), (
            ("Home", "index.html"),
            ("BMW Repair — Snellville, GA", None),
        ))

    def test_generic_page_is_two_levels(self):
        self.assertEqual(fb.trail(GENERIC_PAGE), (
            ("Home", "index.html"),
            ("German Car Oil Change — Snellville, GA", None),
        ))

    def test_markup_uses_the_existing_classes_only(self):
        markup = fb.breadcrumb(HUB)
        self.assertEqual(markup, (
            '<div class="breadcrumb"><a href="/">Home</a><span>/</span>'
            '<span class="crumb-here">BMW Repair — Snellville, GA</span></div>'))
        self.assertNotIn("style=", markup)

    def test_every_catalog_trail_ends_with_its_catalog_name(self):
        for page in cat.PAGES:
            *_, (label, href) = fb.trail(page.slug)
            self.assertIsNone(href)
            self.assertEqual(label, f"{cat.full_label(page.slug)} — {fb.AREA}")
            self.assertEqual(len(fb.trail(page.slug)), 2, page.slug)


class TransformTests(unittest.TestCase):
    def test_live_pages_already_carry_the_trail(self):
        for slug in (HUB, GENERIC_PAGE):
            html = read(slug)
            self.assertEqual(html.count('<div class="breadcrumb">'), 1, slug)
            self.assertEqual(fb.transform(html, slug), html, slug)

    def test_redesign_pass_leaves_the_trail_alone(self):
        once = fb.transform(read(HUB), HUB)
        self.assertEqual(apply_redesign.transform(once), once)

    def test_page_without_a_breadcrumb_is_an_error(self):
        with self.assertRaises(SystemExit):
            fb.transform("<html><body><main></main></body></html>", HUB)


class ScopeTests(unittest.TestCase):
    def test_nothing_is_left_to_rewrite(self):
        self.assertEqual(fb.pages(), ())


if __name__ == "__main__":
    unittest.main(verbosity=1)
