#!/usr/bin/env python3
"""Guard the breadcrumb schema against the page's visible trail.

Run from the repo root:  python3 tools/test_build_schema.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_schema as bs  # noqa: E402

URL = f"{bs.SITE}/bmw-oil-change-snellville-ga"
THREE = ('<div class="breadcrumb"><a href="/">Home</a><span>/</span>'
         '<a href="/bmw-repair-snellville-ga">BMW Repair</a><span>/</span>'
         '<span class="crumb-here">BMW Oil Change — Snellville, GA</span></div>')
TWO = ('<div class="breadcrumb"><a href="/">Home</a><span>/</span>'
       '<span class="crumb-here">Brake Repair — Snellville, GA</span></div>')
# The crumb as the hand-written pages carried it before the addresses were
# cleaned; the trail must resolve it to the same URLs.
THREE_OLD = THREE.replace('href="/"', 'href="index.html"').replace(
    'href="/bmw-repair-snellville-ga"', 'href="bmw-repair-snellville-ga.html"')


class TrailTests(unittest.TestCase):
    def test_three_level_trail_is_read_back(self):
        self.assertEqual(bs.visible_trail(THREE), (
            ("Home", "/"),
            ("BMW Repair", "/bmw-repair-snellville-ga"),
            ("BMW Oil Change — Snellville, GA", None)))
        self.assertEqual(bs.visible_crumb(THREE), "BMW Oil Change — Snellville, GA")

    def test_two_level_trail_is_read_back(self):
        self.assertEqual(bs.visible_trail(TWO), (
            ("Home", "/"), ("Brake Repair — Snellville, GA", None)))

    def test_list_items_carry_absolute_urls_and_the_page_last(self):
        for crumb in (THREE, THREE_OLD):
            items = bs.trail_items(crumb, URL)
            self.assertEqual([u for _, u in items], [
                f"{bs.SITE}/", f"{bs.SITE}/bmw-repair-snellville-ga", URL])
        schema = bs.breadcrumbs(items)
        self.assertEqual(schema["@id"], f"{URL}#breadcrumb")
        self.assertEqual([e["position"] for e in schema["itemListElement"]], [1, 2, 3])

    def test_service_name_is_the_crumb_before_the_area(self):
        entity = bs.service_entity(URL, "t", "d", bs.visible_crumb(THREE))
        self.assertEqual(entity["name"], "BMW Oil Change")

    def test_missing_crumb_falls_back_to_home_and_page(self):
        items = bs.trail_items("<main></main>", URL)
        self.assertEqual(items, [("Home", f"{bs.SITE}/"), ("", URL)])


if __name__ == "__main__":
    unittest.main(verbosity=1)
