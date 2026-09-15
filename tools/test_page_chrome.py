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
from urls import href_for  # noqa: E402

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
        self.assertIn('<div class="fct">Services</div><a href="/#services">All Services</a>', html)
        self.assertIn('href="/porsche-brake-service-snellville-ga"', html)
        self.assertNotIn(".html", html)
        self.assertIn(str(datetime.date.today().year), html)
        self.assertIn("Get directions", html)
        self.assertIn(redesign.PRIVACY_LINK, html)

    def test_neutral_footer_lists_the_hubs(self):
        col, flinks = pc.neutral_blocks()
        for hub, label in cat.hubs()[:3]:
            self.assertIn(f'<a href="{href_for(hub)}">{label}</a>', col)
        for hub, label in cat.hubs():
            self.assertIn(f'<a href="{href_for(hub)}">{label}</a>', flinks)
        self.assertNotIn("porsche", col)

    def test_footer_is_stable_under_the_redesign_pass(self):
        html = pc.footer(PAGE)
        self.assertEqual(redesign.footer_chrome(redesign.footer_privacy(redesign.footer_seal(html))), html)

    def test_redesign_pass_brings_an_old_footer_up_to_date(self):
        old = ('<footer><div class="ft">'
               '<div class="fc"><div class="fct">Contact</div><a href="tel:+16783957459">(678) 395-7459</a>'
               '<p>2144 Parkwood Rd NW</p><p>Snellville, GA 30078</p><p>Mon–Fri: 9:30 AM–6 PM</p></div>'
               '<div class="fc"><div class="fct">Navigate</div><a href="index.html">Home</a></div>'
               '</div><div class="fcopy">© 2025 German Performance — Snellville, GA 30078</div></footer>')
        new = redesign.footer_chrome(old)
        self.assertIn(redesign.FOOTER_CONTACT, new)
        self.assertIn(redesign.FOOTER_NAVIGATE, new)
        self.assertIn(f"© {datetime.date.today().year} German Performance", new)
        self.assertEqual(redesign.footer_chrome(new), new)

    def test_homepage_keeps_its_own_navigate_column(self):
        old = ('<div class="fc"><div class="fct">Contact</div><p>x</p></div>'
               '<div class="fc"><div class="fct">Navigate</div><a href="#about">About</a></div>'
               '<div class="fcopy">© 2025 German Performance</div>')
        new = redesign.footer_chrome(old, home=True)
        self.assertIn('<a href="#about">About</a>', new)
        self.assertIn(redesign.FOOTER_CONTACT, new)


if __name__ == "__main__":
    unittest.main(verbosity=1)
