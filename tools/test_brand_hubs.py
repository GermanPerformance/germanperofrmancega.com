#!/usr/bin/env python3
"""Guard the brand hubs: the money pages after the homepage.

Each hub must be titled "{Make} Repair in Snellville, GA", carry the copy
its module promises (services, weak points, two real reviews, six FAQs
that never name another marque), link the seven make-agnostic pages, the
other four hubs and its own guides, name its marque in the hero checklist,
and be written in the form apply_redesign.transform() leaves it in.

Run from the repo root:  python3 tools/test_brand_hubs.py
"""

import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import apply_redesign as redesign  # noqa: E402
import build_brand_hubs as hubs  # noqa: E402
import build_landing_pages as blp  # noqa: E402
import check_faq  # noqa: E402
import posts  # noqa: E402
from brand_pages import HUBS  # noqa: E402
from reviews import REVIEWS  # noqa: E402
from service_catalog import GROUPS, GENERIC_GROUP, MAKES, full_label  # noqa: E402
from urls import href_for, page_url  # noqa: E402

FAQ_RE = re.compile(r'<summary class="fq">(.*?)<span', re.S)
ANSWER_RE = re.compile(r'<div class="fa"><p>(.*?)</p></div>', re.S)


def main_of(html):
    return html[html.index("<main>"):html.index("</main>")]


class EntryTests(unittest.TestCase):
    def test_one_hub_per_make_in_catalog_order(self):
        self.assertEqual([h["slug"] for h in HUBS], [m.hub for m in MAKES])

    def test_each_entry_carries_its_copy(self):
        for h in HUBS:
            self.assertEqual(len(h["before"]), 3, h["slug"])
            self.assertIn(len(h["services"]), (4, 6), h["slug"])  # full rows only
            self.assertEqual(len(h["known"]), 5, h["slug"])
            self.assertEqual(len(h["reviews"]), 2, h["slug"])
            self.assertEqual(len(h["faqs"]), 6, h["slug"])
            for key in h["reviews"]:
                self.assertIn(key, REVIEWS, (h["slug"], key))
            for _, body, general in h["services"]:
                self.assertGreaterEqual(len(body.split()), 50, h["slug"])
                if general:
                    self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, general)), general)

    def test_title_and_description_fit_a_result(self):
        for h in HUBS:
            title = blp.title(full_label(h["slug"]))
            self.assertLessEqual(len(title), 60, title)
            self.assertTrue(120 <= len(h["desc"]) <= 160, (h["slug"], len(h["desc"])))

    def test_faqs_never_name_another_marque(self):
        for h in HUBS:
            own = check_faq.BRANDS[h["make"]]
            text = " ".join(q + " " + a for q, a in h["faqs"])
            for other, pattern in check_faq.BRAND_PATTERNS.items():
                if other != own:
                    self.assertIsNone(re.search(pattern, text), (h["slug"], other))


class RenderedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {h["slug"]: hubs.build(h) for h in HUBS}

    def test_head_is_the_money_page_framework(self):
        for h in HUBS:
            html = self.pages[h["slug"]]
            service = full_label(h["slug"])
            self.assertIn(f"<title>{service} in Snellville, GA | German Performance</title>", html)
            self.assertIn(f'<meta name="description" content="{h["desc"]}">', html)
            self.assertIn(f'<link rel="canonical" href="{page_url(h["slug"])}"/>', html)
            self.assertIn('<body data-page-type="hub">', html)

    def test_hero_is_two_lines_and_names_the_marque(self):
        for h in HUBS:
            html = self.pages[h["slug"]]
            self.assertIn('<section class="hero hero-svc">', html)
            self.assertIn(f'>{full_label(h["slug"])} in<br><span class="accent">Snellville,&nbsp;GA</span></h1>', html)
            self.assertIn(f"Genuine {h['possessive']} parts and fluids", blp.hero_checks(html))

    def test_long_names_lower_the_phone_floor(self):
        for h in HUBS:
            em = blp.h1_em(full_label(h["slug"]))
            floor = "--h1-min:" in self.pages[h["slug"]].split("</h1>")[0]
            self.assertEqual(floor, em > blp.H1_EM_PHONE_MAX, h["slug"])

    def test_body_links_the_general_pages_the_other_hubs_and_the_guides(self):
        generic = [slug for slug, _ in dict(GROUPS)[GENERIC_GROUP]]
        for h in HUBS:
            body = main_of(self.pages[h["slug"]])
            for slug in generic:
                self.assertIn(f'href="{href_for(slug)}"', body, (h["slug"], slug))
            for m in MAKES:
                if m.hub != h["slug"]:
                    self.assertIn(f'href="{href_for(m.hub)}"', body, (h["slug"], m.hub))
            self.assertIn('href="/">German auto repair shop in Snellville, GA</a>', body)
            self.assertIn(f'href="{href_for(posts.GUIDES_PAGE)}"', body)
            for slug in posts.guides_for(h["slug"]):
                self.assertIn(f'href="{href_for(slug)}" class="card"', body, (h["slug"], slug))
            for _, _, general in h["services"]:
                if general:
                    self.assertIn(f'href="{href_for(general)}">{full_label(general)} for every German make', body)

    def test_guides_grid_fills_its_rows(self):
        """Four guides sit two across, six three across: never an orphan card."""
        for h in HUBS:
            slugs = posts.guides_for(h["slug"])
            section = hubs.guides_section(h)
            self.assertEqual(bool(section), bool(slugs), h["slug"])
            if slugs:
                self.assertIn(f'<div class="{hubs.grid_class(len(slugs))} fu">', section)
                self.assertEqual(section.count('class="card"'), len(slugs))

    def test_faq_schema_source_matches_the_module(self):
        for h in HUBS:
            body = main_of(self.pages[h["slug"]])
            self.assertEqual(FAQ_RE.findall(body), [q for q, _ in h["faqs"]], h["slug"])
            self.assertEqual(ANSWER_RE.findall(body), [a for _, a in h["faqs"]], h["slug"])

    def test_reviews_and_credentials_are_on_the_page(self):
        for h in HUBS:
            body = main_of(self.pages[h["slug"]])
            for key in h["reviews"]:
                self.assertIn(f'id="review-{key}-name"', body, (h["slug"], key))
                self.assertIn(REVIEWS[key]["quote"], body, (h["slug"], key))
            self.assertIn("ASE Master Technician", body, h["slug"])
            self.assertIn("12-month, 12,000-mile", body, h["slug"])

    def test_page_is_a_transform_fixpoint(self):
        for slug, html in self.pages.items():
            self.assertEqual(redesign.transform(html), html, slug)
            hubs.verify(next(h for h in HUBS if h["slug"] == slug), html)

    def test_second_render_is_identical(self):
        for h in HUBS:
            self.assertEqual(self.pages[h["slug"]], hubs.build(h))


class LiveFileTests(unittest.TestCase):
    def test_every_hub_on_disk_is_the_one_the_tool_writes(self):
        for h in HUBS:
            with open(os.path.join(REPO_ROOT, h["slug"]), encoding="utf-8") as fh:
                live = fh.read()
            self.assertIn(f"<title>{full_label(h['slug'])} in Snellville, GA | German Performance</title>", live)
            self.assertEqual(live.count(f'"@id": "{page_url(h["slug"])}#service"'), 1, h["slug"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
