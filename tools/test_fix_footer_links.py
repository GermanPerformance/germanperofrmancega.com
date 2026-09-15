#!/usr/bin/env python3
"""Guard the related-service ranking the footers and rel-grids share.

Run from the repo root:  python3 tools/test_fix_footer_links.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fix_footer_links as ffl  # noqa: E402


class RankingTests(unittest.TestCase):
    def test_generic_page_ranks_the_homepage_then_its_siblings(self):
        picks = ffl.related("german-car-brake-repair-snellville-ga.html")
        self.assertEqual(picks[0], "index.html")
        generic = {"index.html"} | {p for p in ffl.SERVICES if ffl.brand_of(p) == "german-car"}
        self.assertTrue(all(p in generic for p in picks), picks)
        # every make-agnostic page but itself, so nothing links a retired job page
        self.assertEqual(len(picks), len(generic) - 1, picks)

    def test_only_make_agnostic_pages_are_ranked(self):
        for page in ffl.SERVICES:
            self.assertEqual(ffl.brand_of(page), "german-car", page)

    def test_ranking_never_includes_the_page_itself(self):
        for page in ffl.SERVICES:
            self.assertNotIn(page, ffl.related(page))

    def test_every_ranked_page_has_a_label(self):
        for page in ffl.SERVICES:
            for pick in ffl.related(page):
                self.assertIn(pick, ffl.TARGETS)

    def test_homepage_is_linked_as_the_general_repair_page(self):
        self.assertEqual(ffl.TARGETS["index.html"], "German Auto Repair")
        self.assertNotIn("index.html", ffl.SERVICES)
        self.assertIn("index.html", ffl.related("german-car-brake-repair-snellville-ga.html"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
