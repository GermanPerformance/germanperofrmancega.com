#!/usr/bin/env python3
"""Guard the chrome every generated page shares.

Run from the repo root:  python3 tools/test_page_chrome.py
"""

import datetime
import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import apply_redesign as redesign  # noqa: E402
import page_chrome as pc  # noqa: E402
import service_catalog as cat  # noqa: E402

PAGE = "porsche-oil-change-snellville-ga.html"


class HeadTests(unittest.TestCase):
    def test_stylesheets_are_fonts_then_the_cascade_at_version(self):
        links = pc.stylesheets()
        hrefs = re.findall(r'href="([^"]+)"', links)
        v = redesign.VERSION
        self.assertEqual(hrefs, [f"assets/css/fonts.css?v={v}", f"assets/css/tokens.css?v={v}",
                                 f"assets/css/werkstatt.css?v={v}", f"assets/css/site.css?v={v}"])
        self.assertNotIn("fonts.googleapis", links)

    def test_scripts_carry_the_tracker(self):
        self.assertIn("assets/js/site.js?v=", pc.scripts())
        self.assertIn("assets/js/analytics.js?v=", pc.scripts())

    def test_nav_is_the_redesign_block(self):
        self.assertEqual(pc.NAV, redesign.NAV)
        self.assertTrue(pc.NAV.startswith('<div class="topbar">'))
        self.assertTrue(pc.NAV.rstrip().endswith("</div>"))

    def test_nap_grid_names_the_shop(self):
        self.assertIn("2144 Parkwood Rd NW", pc.NAP_GRID)
        self.assertIn("(678) 395-7459", pc.NAP_GRID)
        self.assertTrue(pc.NAP_GRID.startswith('<div class="ic-grid">'))


class FooterTests(unittest.TestCase):
    def test_service_page_footer_uses_its_related_links(self):
        html = pc.footer(PAGE)
        self.assertIn('<div class="fct">Services</div><a href="index.html#services">All Services</a>', html)
        self.assertIn("porsche-brake-service-snellville-ga.html", html)
        self.assertIn(str(datetime.date.today().year), html)
        self.assertIn("Get directions", html)
        self.assertIn(redesign.PRIVACY_LINK, html)

    def test_neutral_footer_lists_the_hubs(self):
        col, flinks = pc.neutral_blocks()
        for hub, label in cat.hubs()[:3]:
            self.assertIn(f'<a href="{hub}">{label}</a>', col)
        for hub, label in cat.hubs():
            self.assertIn(f'<a href="{hub}">{label}</a>', flinks)
        self.assertNotIn("porsche", col)

    def test_footer_is_stable_under_the_redesign_pass(self):
        html = pc.footer(PAGE)
        self.assertEqual(redesign.footer_privacy(redesign.footer_seal(html)), html)


if __name__ == "__main__":
    unittest.main(verbosity=1)
