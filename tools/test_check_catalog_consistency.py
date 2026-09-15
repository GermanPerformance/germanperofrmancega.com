#!/usr/bin/env python3
"""Guard the checker that keeps every service page's name in step with
the catalog.

Run from the repo root:  python3 tools/test_check_catalog_consistency.py
"""

import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import check_catalog_consistency as ccc  # noqa: E402
import fix_breadcrumbs as fb  # noqa: E402
import service_catalog as cat  # noqa: E402
from urls import href_for, page_url  # noqa: E402

SLUG = "bmw-repair-snellville-ga.html"
HUB = "mercedes-repair-snellville-ga.html"
GENERIC = "german-car-tune-up-snellville-ga.html"


def page(slug, title=None, h1=None, crumb=None, desc="A fine page.", canonical=None,
         page_type=None, nav=True):
    """A minimal page carrying only what the checker reads."""
    title = title or ccc.expected_name(slug)
    h1 = h1 or ccc.expected_name(slug).upper().replace(" ", "<br>")
    crumb = crumb or fb.breadcrumb(slug)
    canonical = canonical or page_url(slug)
    page_type = page_type or ("hub" if slug in {m.hub for m in cat.MAKES} else "service")
    links = "".join(f'<a href="{href_for(h)}">{l}</a>' for _, e in cat.GROUPS for h, l in e) if nav else ""
    return (f'<title>{title} Snellville GA | German Performance</title>\n'
            f'<meta name="description" content="{desc}">\n'
            f'<link rel="canonical" href="{canonical}"/>\n'
            f'<body data-page-type="{page_type}"><nav>{links}</nav>\n'
            f'{crumb}\n<h1 class="fu">{h1}</h1>')


class NameTests(unittest.TestCase):
    def test_expected_names(self):
        self.assertEqual(ccc.expected_name(SLUG), "BMW Repair")
        self.assertEqual(ccc.expected_name(HUB), "Mercedes Repair")
        self.assertEqual(ccc.expected_name(GENERIC), "Tune-Up")
        self.assertEqual(ccc.expected_name("german-car-ac-repair-snellville-ga.html"), "AC Repair")
        self.assertEqual(ccc.expected_name("pre-purchase-inspection-german-car-ga.html"),
                         "Pre-Purchase Inspection")

    def test_h1_text_collapses_markup(self):
        self.assertEqual(ccc.h1_text('<h1 class="fu">BMW<br><span class="outline">OIL</span>'
                                     '<br><span class="accent">CHANGE</span></h1>'),
                         "BMW OIL CHANGE")


class RuleTests(unittest.TestCase):
    def problems(self, **kw):
        slug = kw.pop("slug", SLUG)
        return list(ccc.check_page(slug, page(slug, **kw)))

    def test_clean_page_passes(self):
        self.assertEqual(self.problems(), [])
        self.assertEqual(self.problems(slug=HUB), [])
        self.assertEqual(self.problems(slug=GENERIC), [])

    def test_hub_may_use_the_column_heading(self):
        self.assertEqual(self.problems(slug=HUB, title="Mercedes-Benz Repair",
                                       h1="MERCEDES-BENZ<br>REPAIR"), [])

    def test_hub_in_the_money_page_framework_passes(self):
        # "{Make} Repair in Snellville, GA" as title and two-line H1, the
        # form tools/build_brand_hubs.py writes.
        self.assertEqual(self.problems(
            slug=HUB, title="Mercedes Repair in Snellville, GA",
            h1='Mercedes Repair in<br><span class="accent">Snellville,&nbsp;GA</span>'), [])

    def test_hub_title_may_carry_the_short_form_in_brackets(self):
        slug = "volkswagen-repair-snellville-ga.html"
        self.assertEqual(self.problems(slug=slug, title="Volkswagen (VW) Repair",
                                       h1="VOLKSWAGEN<br>REPAIR"), [])

    def test_wrong_title(self):
        self.assertTrue(any("title" in p for p in self.problems(title="BMW Service")))

    def test_h1_must_name_make_and_job(self):
        self.assertTrue(any("h1" in p for p in self.problems(h1="VW<br>REPAIR",
                                                              slug="volkswagen-repair-snellville-ga.html")))
        self.assertTrue(any("h1" in p for p in self.problems(h1="BMW<br>SERVICE")))

    def test_generic_h1_may_drop_the_auto_prefix(self):
        slug = "german-car-ac-repair-snellville-ga.html"
        self.assertEqual(self.problems(slug=slug, title="German Car AC Repair",
                                       h1="GERMAN CAR<br>AC REPAIR"), [])

    def test_hub_and_generic_page_stay_two_crumbs(self):
        three = ('<div class="breadcrumb"><a href="/">Home</a><span>/</span>'
                 '<a href="/bmw-repair-snellville-ga">BMW Repair</a><span>/</span>'
                 '<span class="crumb-here">BMW Oil Change — Snellville, GA</span></div>')
        self.assertTrue(any("breadcrumb" in p for p in self.problems(crumb=three)))
        self.assertTrue(any("breadcrumb" in p for p in self.problems(slug=GENERIC, crumb=three)))

    def test_description_bounds(self):
        self.assertTrue(any("description" in p for p in self.problems(desc="")))
        self.assertTrue(any("description" in p for p in self.problems(desc="x" * 161)))

    def test_canonical_and_page_type(self):
        self.assertTrue(any("canonical" in p for p in self.problems(canonical="https://example.com/x.html")))
        # The ".html" spelling is a second address for the same page, not its own.
        self.assertTrue(any("canonical" in p for p in self.problems(canonical=page_url(SLUG) + ".html")))
        self.assertTrue(any("data-page-type" in p for p in self.problems(slug=GENERIC, page_type="hub")))
        self.assertTrue(any("data-page-type" in p for p in self.problems(slug=HUB, page_type="service")))

    def test_nav_must_carry_the_whole_catalog(self):
        self.assertTrue(any("nav" in p for p in self.problems(nav=False)))


if __name__ == "__main__":
    unittest.main(verbosity=1)
