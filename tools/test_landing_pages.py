#!/usr/bin/env python3
"""Guard the landing-page framework and the contract every entry must keep.

Run from the repo root:  python3 tools/test_landing_pages.py
"""

import html as htmlmod
import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import add_related_services  # noqa: E402
import apply_redesign  # noqa: E402
import build_landing_pages as blp  # noqa: E402
import build_schema  # noqa: E402
import landing_pages  # noqa: E402
import reviews  # noqa: E402
from urls import page_url  # noqa: E402

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
HEADING_RE = re.compile(r"<h([1-6])[^>]*>", re.S)
META_RE = r'<meta (?:property|name)="{name}" content="([^"]*)"'
REQUIRED = ("slug", "service", "gbp", "desc", "sub", "photo", "intro", "promise",
            "cards", "reviews", "faqs")


def text(markup):
    """Rendered text: a <br> reads as a space, every other tag as nothing."""
    flat = re.sub(r"<br\s*/?>", " ", markup)
    return " ".join(htmlmod.unescape(re.sub(r"<[^>]+>", "", flat)).split())


def meta(markup, name):
    match = re.search(META_RE.format(name=re.escape(name)), markup)
    return match.group(1) if match else None


def main_of(markup):
    return markup[markup.index("<main>"):markup.index("</main>")]


class DerivationTests(unittest.TestCase):
    def test_headline_is_service_in_place(self):
        self.assertEqual(blp.headline("Brake Repair"), "Brake Repair in Snellville, GA")

    def test_title_mirrors_the_headline(self):
        self.assertEqual(blp.title("Brake Repair"),
                         "Brake Repair in Snellville, GA | German Performance")

    def test_crumb_keeps_the_dash_the_schema_splits_on(self):
        crumb = blp.crumb("Brake Repair")
        entity = build_schema.service_entity("https://x/y.html", "t", "d", crumb)
        self.assertEqual(entity["name"], "Brake Repair")

    def test_h1_reads_as_the_headline(self):
        self.assertEqual(text(blp.h1_markup("Brake Repair")), "Brake Repair in Snellville, GA")

    def test_h1_carries_its_measured_width(self):
        # Calibrated 2026-09-12 against Archivo 800 at width 100: 8.679em.
        em = blp.h1_em("Brake Repair")
        self.assertAlmostEqual(em, 8.679 * blp.H1_MARGIN, delta=0.1)
        self.assertIn(f'style="--h1-em:{em:.2f}"', blp.h1_markup("Brake Repair"))

    def test_band_asks_for_the_booking(self):
        self.assertEqual(blp.band_head("Brake Repair"), ("BOOK YOUR", "BRAKE REPAIR"))


class EntryContractTests(unittest.TestCase):
    def test_every_entry_is_complete(self):
        for page in landing_pages.PAGES:
            for key in REQUIRED:
                self.assertIn(key, page, f"{page['slug']}: missing {key}")
            self.assertTrue(page["gbp"], f"{page['slug']}: claims no profile service")
            self.assertEqual(len(page["cards"]), 6, page["slug"])
            self.assertEqual(len(page["promise"]), 3, page["slug"])
            self.assertEqual(len(page["reviews"]), 2, page["slug"])
            self.assertGreaterEqual(len(page["faqs"]), 4, page["slug"])

    def test_service_fits_the_hero_on_two_lines(self):
        for page in landing_pages.PAGES:
            self.assertLessEqual(len(page["service"]), landing_pages.SERVICE_MAX_CHARS,
                                 f"{page['slug']}: service name too long for a two-line H1")

    def test_description_is_search_length(self):
        for page in landing_pages.PAGES:
            n = len(page["desc"])
            self.assertTrue(120 <= n <= 160, f"{page['slug']}: description is {n} chars")
            self.assertIn("Snellville", page["desc"], page["slug"])
            self.assertIn(page["service"].casefold(), page["desc"].casefold(), page["slug"])

    def test_sub_expounds_the_headline(self):
        for page in landing_pages.PAGES:
            sub = page["sub"].casefold()
            self.assertIn(page["service"].casefold(), sub, page["slug"])
            self.assertIn("snellville", sub, page["slug"])

    def test_reviews_exist_and_match_the_homepage(self):
        with open(os.path.join(REPO_ROOT, "index.html"), encoding="utf-8") as fh:
            home = fh.read()
        for key, review in reviews.REVIEWS.items():
            self.assertIn(review["quote"], home, f"review {key}: quote drifted from index.html")
            self.assertIn(review["name"], home, key)
        for page in landing_pages.PAGES:
            for key in page["reviews"]:
                self.assertIn(key, reviews.REVIEWS, f"{page['slug']}: unknown review {key}")

    def test_photo_assets_exist(self):
        for page in landing_pages.PAGES:
            base = page["photo"]["base"]
            for width in blp.PHOTO_WIDTHS:
                for ext in ("jpg", "webp"):
                    path = os.path.join(REPO_ROOT, f"{base}-{width}.{ext}")
                    self.assertTrue(os.path.isfile(path), f"{page['slug']}: missing {path}")
            self.assertTrue(page["photo"]["alt"], page["slug"])

    def test_slugs_are_unique(self):
        slugs = [p["slug"] for p in landing_pages.PAGES]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_no_entry_is_also_built_elsewhere(self):
        import build_brand_hubs
        import build_general_service_pages
        import posts
        others = {p["slug"] for p in build_general_service_pages.PAGES}
        others |= set(build_brand_hubs.SLUGS) | set(posts.POST_DATES)
        for page in landing_pages.PAGES:
            self.assertNotIn(page["slug"], others, f"{page['slug']}: two writers")


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {p["slug"]: blp.build(p) for p in landing_pages.PAGES}
        cls.by_slug = {p["slug"]: p for p in landing_pages.PAGES}

    def test_redesign_pass_is_a_no_op(self):
        for slug, markup in self.pages.items():
            self.assertEqual(apply_redesign.transform(markup), markup, slug)

    def test_no_inline_styles_but_custom_properties(self):
        for slug, markup in self.pages.items():
            self.assertNotRegex(markup, r'style="(?!--)', slug)

    def test_title_and_h1_agree_and_fit(self):
        for slug, page in self.by_slug.items():
            markup = self.pages[slug]
            self.assertEqual(text(H1_RE.search(markup).group(1)), blp.headline(page["service"]))
            self.assertEqual(len(H1_RE.findall(markup)), 1, slug)
            title = blp.title(page["service"])
            self.assertIn(f"<title>{title}</title>", markup)
            self.assertLessEqual(len(title), 60, slug)

    def test_hero_is_scoped_for_the_two_line_rule(self):
        for slug, markup in self.pages.items():
            self.assertIn('<section class="hero hero-svc">', markup, slug)

    def test_one_call_to_action_everywhere(self):
        for slug, markup in self.pages.items():
            body = main_of(markup)
            hero = body[body.index('<section class="hero'):body.index("</section>")]
            self.assertEqual(hero.count('class="bp"'), 1, slug)
            self.assertNotIn("All Services", hero, slug)
            self.assertNotIn("Get Directions", body, slug)
            self.assertNotIn('class="cta-final"', body, slug)
            self.assertNotIn('class="bg"', body, slug)
            # Every content section closes on the same button.
            self.assertEqual(body.count('<div class="acts section-cta fu">'), 4, slug)
            for anchor in re.findall(r'<a href="tel:[^"]+"[^>]*>(.*?)</a>', body, re.S):
                self.assertIn("Service My Car", anchor, slug)

    def test_heading_outline_has_no_gaps(self):
        for slug, markup in self.pages.items():
            levels = [int(n) for n in HEADING_RE.findall(main_of(markup))]
            self.assertEqual(levels[0], 1, slug)
            for prev, cur in zip(levels, levels[1:]):
                self.assertLessEqual(cur - prev, 1, f"{slug}: h{prev} -> h{cur}")
            self.assertGreaterEqual(levels.count(3), 6 + 4 + 2, slug)  # cards, steps, reviews

    def test_sections_in_the_agreed_order(self):
        for slug, page in self.by_slug.items():
            body = main_of(self.pages[slug])
            marks = ['class="hero hero-svc"', 'class="svc-figure', 'class="g3 fu"',
                     'class="gr-wall gr-pair', 'class="steps steps-4 fu"', 'class="faq-list"',
                     'class="cta-band fu"', 'class="rel-grid fu"']
            positions = [body.index(m) for m in marks]
            self.assertEqual(positions, sorted(positions), slug)
            self.assertNotIn('class="ic-grid"', body, slug)
            self.assertNotIn("Why German Performance", body, slug)

    def test_band_copy_is_derived(self):
        for slug, page in self.by_slug.items():
            l1, l2 = blp.band_head(page["service"])
            self.assertIn(f'<div class="cbt">{l1}<br>{l2}</div>', self.pages[slug], slug)

    def test_social_tags(self):
        for slug, page in self.by_slug.items():
            markup = self.pages[slug]
            self.assertEqual(meta(markup, "og:title"), blp.title(page["service"]), slug)
            self.assertEqual(meta(markup, "og:description"), page["desc"], slug)
            self.assertEqual(meta(markup, "og:url"), page_url(slug), slug)
            self.assertEqual(meta(markup, "og:type"), "website", slug)
            self.assertEqual(meta(markup, "twitter:card"), "summary_large_image", slug)
            image = meta(markup, "og:image")
            self.assertTrue(image.startswith(blp.SITE + "/"), slug)
            self.assertTrue(os.path.isfile(os.path.join(REPO_ROOT, image[len(blp.SITE) + 1:])), slug)
            self.assertEqual(meta(markup, "twitter:image"), image, slug)

    def test_photo_markup(self):
        for slug, page in self.by_slug.items():
            markup = self.pages[slug]
            figure = re.search(r'<figure class="svc-figure[^"]*">(.*?)</figure>', markup, re.S)
            self.assertIsNotNone(figure, slug)
            fig = figure.group(1)
            self.assertIn('<source type="image/webp"', fig, slug)
            self.assertIn(f'alt="{page["photo"]["alt"]}"', fig, slug)
            self.assertRegex(fig, r'width="\d+" height="\d+" loading="lazy" decoding="async"', slug)

    def test_checklist_is_make_agnostic(self):
        for slug, markup in self.pages.items():
            checks = markup[markup.index('<ul class="checks'):]
            checks = checks[:checks.index("</ul>")]
            self.assertIn("Genuine factory parts and fluids", checks, slug)
            self.assertIsNone(blp.MARQUE_RE.search(checks), slug)

    def test_faq_questions_are_visible_to_the_schema(self):
        for slug, page in self.by_slug.items():
            found = build_schema.visible_faq(self.pages[slug])
            names = [q["name"] for q in found["mainEntity"]]
            self.assertEqual(names, [htmlmod.unescape(q) for q, _ in page["faqs"]])

    def test_related_block_is_the_one_the_tool_writes(self):
        for slug, markup in self.pages.items():
            self.assertEqual(len(add_related_services.BLOCK.findall(markup)), 1, slug)
            self.assertIn(add_related_services.build_block(slug), markup, slug)
            self.assertEqual(markup.count(add_related_services.MARKER), 1, slug)

    def test_page_carries_chrome_and_scripts(self):
        for slug, markup in self.pages.items():
            self.assertIn(apply_redesign.NAV, markup, slug)
            self.assertIn('<body data-page-type="service">', markup, slug)
            self.assertIn(f'assets/js/analytics.js?v={apply_redesign.VERSION}', markup, slug)
            self.assertIn('href="/privacy-policy"', markup, slug)
            self.assertIn(f'<link rel="canonical" href="{page_url(slug)}"/>', markup, slug)
            self.assertNotIn('.html"', markup, slug)
            self.assertIn(">Get directions<", markup, slug)


class LiveFileTests(unittest.TestCase):
    def test_pages_on_disk_carry_the_headline(self):
        for page in landing_pages.PAGES:
            path = os.path.join(REPO_ROOT, page["slug"])
            self.assertTrue(os.path.isfile(path), page["slug"])
            with open(path, encoding="utf-8") as fh:
                markup = fh.read()
            self.assertEqual(text(H1_RE.search(markup).group(1)), blp.headline(page["service"]))
            self.assertIn('"@type": "Service"', markup, page["slug"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
