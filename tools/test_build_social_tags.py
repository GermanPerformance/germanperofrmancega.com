#!/usr/bin/env python3
"""Every page must carry Open Graph and Twitter Card tags that mirror its
own title, description and canonical, in the exact form the landing-page
generator already writes them, so a page built by any tool and a page
maintained by transformation share one head.

Run from the repo root:  python3 tools/test_build_social_tags.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_social_tags as social  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>German Car Oil Change Snellville GA | German Performance</title>
<meta name="description" content="German car oil change in Snellville, GA. Call (678) 395-7459.">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="https://germanperformancega.com/german-car-oil-change.html"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
</head>
<body></body>
</html>
"""


class ChooseImage(unittest.TestCase):
    def test_service_keyword_in_slug_picks_that_service_photo(self):
        self.assertEqual(social.choose_image("german-car-oil-change.html"),
                         "assets/img/services/oil-change-1100.jpg")
        self.assertEqual(social.choose_image("german-car-ac-repair.html"),
                         "assets/img/services/ac-repair-1100.jpg")

    def test_brand_hub_picks_a_photo_of_that_brand(self):
        self.assertEqual(social.choose_image("bmw-repair.html"),
                         "assets/img/shop/bmw-m3-on-lift-1100.jpg")

    def test_about_page_shows_the_people(self):
        self.assertEqual(social.choose_image("about.html"),
                         "assets/img/shop/sam-and-zayd-1100.jpg")

    def test_no_matching_photo_falls_back_to_the_site_image(self):
        self.assertEqual(social.choose_image("audi-repair.html"), "og-image.jpg")
        self.assertEqual(social.choose_image("guides.html"), "og-image.jpg")
        self.assertEqual(social.choose_image("bmw-maintenance-schedule-explained.html"),
                         "og-image.jpg")


class Transform(unittest.TestCase):
    def test_block_is_inserted_after_the_canonical(self):
        out = social.transform(PAGE, "german-car-oil-change.html")
        canonical = '<link rel="canonical" href="https://germanperformancega.com/german-car-oil-change.html"/>\n'
        expected = canonical + "\n".join((
            '<meta property="og:type" content="website">',
            '<meta property="og:title" content="German Car Oil Change Snellville GA | German Performance">',
            '<meta property="og:description" content="German car oil change in Snellville, GA. Call (678) 395-7459.">',
            '<meta property="og:url" content="https://germanperformancega.com/german-car-oil-change.html">',
            '<meta property="og:image" content="https://germanperformancega.com/assets/img/services/oil-change-1100.jpg">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:title" content="German Car Oil Change Snellville GA | German Performance">',
            '<meta name="twitter:description" content="German car oil change in Snellville, GA. Call (678) 395-7459.">',
            '<meta name="twitter:image" content="https://germanperformancega.com/assets/img/services/oil-change-1100.jpg">',
        )) + "\n"
        self.assertIn(expected, out)
        self.assertIn('<link rel="preconnect"', out.split(expected)[1])

    def test_running_twice_changes_nothing(self):
        once = social.transform(PAGE, "german-car-oil-change.html")
        self.assertEqual(social.transform(once, "german-car-oil-change.html"), once)

    def test_existing_image_is_kept_when_the_block_is_refreshed(self):
        once = social.transform(PAGE, "german-car-oil-change.html")
        custom = once.replace("services/oil-change-1100.jpg", "shop/bmw-5-series-1100.jpg")
        retitled = custom.replace("<title>German Car Oil Change Snellville GA", "<title>German Car Oil Service Snellville GA")
        out = social.transform(retitled, "german-car-oil-change.html")
        self.assertIn('og:title" content="German Car Oil Service Snellville GA | German Performance"', out)
        self.assertIn('og:image" content="https://germanperformancega.com/assets/img/shop/bmw-5-series-1100.jpg"', out)
        self.assertNotIn("oil-change-1100.jpg", out)

    def test_legacy_self_closing_block_is_replaced_not_duplicated(self):
        legacy = PAGE.replace(
            '<link rel="canonical" href="https://germanperformancega.com/german-car-oil-change.html"/>\n',
            '<link rel="canonical" href="https://germanperformancega.com/german-car-oil-change.html">\n'
            '<meta property="og:type" content="website" />\n'
            '<meta property="og:url" content="https://germanperformancega.com/german-car-oil-change.html" />\n'
            '<meta property="og:title" content="Old Title" />\n'
            '<meta property="og:description" content="Old description." />\n'
            '<meta property="og:image" content="https://germanperformancega.com/og-image.jpg" />\n')
        out = social.transform(legacy, "german-car-oil-change.html")
        self.assertEqual(out.count("og:type"), 1)
        self.assertEqual(out.count("og:image"), 1)
        self.assertNotIn("Old Title", out)
        self.assertIn('og:image" content="https://germanperformancega.com/og-image.jpg">', out)
        self.assertIn('twitter:card', out)

    def test_page_without_canonical_is_left_alone(self):
        page = PAGE.replace('<link rel="canonical" href="https://germanperformancega.com/german-car-oil-change.html"/>\n', "")
        self.assertEqual(social.transform(page, "404.html"), page)

    def test_quotes_in_a_title_are_escaped_for_the_attribute(self):
        page = PAGE.replace("<title>German Car Oil Change Snellville GA", '<title>BMW "M" Oil Change Snellville GA')
        out = social.transform(page, "german-car-oil-change.html")
        self.assertIn('og:title" content="BMW &quot;M&quot; Oil Change Snellville GA | German Performance"', out)


class RealPages(unittest.TestCase):
    def test_the_landing_page_generator_output_is_already_canonical(self):
        name = "german-car-brake-repair.html"
        with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
            page = fh.read()
        self.assertEqual(social.transform(page, name), page)


if __name__ == "__main__":
    unittest.main()
