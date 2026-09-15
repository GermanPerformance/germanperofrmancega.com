#!/usr/bin/env python3
"""Every map on the site points at the shop's Google listing, not the building.

Run from the repo root:  python3 tools/test_place.py
"""

import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_schema  # noqa: E402
import place  # noqa: E402
from redirects import site_pages  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The old form: a bare street address, which Google resolves to the
# building entity rather than the Business Profile.
BUILDING_QUERY_RE = re.compile(r'href="https://maps\.google\.com/\?q=2144')
EMBED_RE = re.compile(r'<iframe src="([^"]+output=embed)"')
DIRECTIONS_RE = re.compile(r'<a href="([^"]+)"[^>]*>Get [Dd]irections')


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


class UrlTests(unittest.TestCase):
    def test_the_place_id_is_on_every_maps_urls_link(self):
        for url in (place.PLACE, place.DIRECTIONS, place.WRITE_REVIEW):
            self.assertIn(place.PLACE_ID, url)

    def test_the_profile_link_is_the_listing_cid(self):
        self.assertEqual(place.PROFILE, f"https://maps.google.com/?cid={place.CID}")
        self.assertEqual(int("394ab91e9085b6d4", 16), int(place.CID))

    def test_the_embed_names_the_shop_not_just_the_street(self):
        # A bare-address query returns gcid:compound_building; the name
        # in front of it returns the auto_repair_shop listing.
        self.assertTrue(place.EMBED.startswith("https://www.google.com/maps?q=German+Performance,"))
        self.assertTrue(place.EMBED.endswith("&output=embed"))

    def test_attr_escapes_the_ampersands_only(self):
        self.assertEqual(place.attr("https://x/?a=1&b=2"), "https://x/?a=1&amp;b=2")
        self.assertNotIn("&amp;amp;", place.attr(place.DIRECTIONS))

    def test_geo_is_the_listings_own_pin(self):
        self.assertEqual(place.GEO, {"latitude": 33.8456418, "longitude": -84.0556775})


class SchemaTests(unittest.TestCase):
    def test_has_map_and_same_as_lead_with_the_listing(self):
        entity = build_schema.business()
        self.assertEqual(entity["hasMap"], place.PLACE)
        self.assertEqual(entity["sameAs"][0], place.PROFILE)
        self.assertEqual(entity["geo"], {"@type": "GeoCoordinates", **place.GEO})


class PageTests(unittest.TestCase):
    pages = site_pages(os.listdir(REPO_ROOT))

    def test_no_page_links_the_building(self):
        for name in self.pages:
            self.assertIsNone(BUILDING_QUERY_RE.search(read(name)), name)

    def test_every_directions_link_carries_the_place_id(self):
        seen = 0
        for name in self.pages:
            for href in DIRECTIONS_RE.findall(read(name)):
                self.assertEqual(href, place.attr(place.DIRECTIONS), name)
                seen += 1
        self.assertGreaterEqual(seen, len(self.pages))

    def test_every_embed_is_the_listing(self):
        embeds = {name: EMBED_RE.findall(read(name)) for name in self.pages}
        found = {name: srcs for name, srcs in embeds.items() if srcs}
        self.assertEqual(set(found), {"index.html", "contact.html"})
        for name, srcs in found.items():
            self.assertEqual(srcs, [place.attr(place.EMBED)], name)


if __name__ == "__main__":
    unittest.main()
