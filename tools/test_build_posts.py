#!/usr/bin/env python3
"""Guard the two supporting articles and the post registry.

Every article in tools/posts.py must render on the blog skeleton, link the
homepage where it lists the shop's services, carry the technicians' note,
use clean addresses only, and render identically on a second pass. The
registry must know the dates of every article on disk, the hand-written
one included, so build_schema.py has one source of truth.

Run from the repo root:  python3 tools/test_build_posts.py
"""

import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import build_posts  # noqa: E402
import posts  # noqa: E402
from urls import page_url  # noqa: E402

MIN_WORDS = 900
HREF_RE = re.compile(r'href="([^"]+)"')


def body_of(html):
    return re.search(r"<main>(.*?)</main>", html, re.S).group(1)


def words_in(html):
    text = re.sub(r"<[^>]+>", " ", body_of(html))
    return len(text.split())


class Registry(unittest.TestCase):
    def test_every_post_has_dates_and_every_dated_post_exists(self):
        for post in posts.POSTS:
            self.assertIn(post["slug"], posts.POST_DATES)
        for slug, (published, modified) in posts.POST_DATES.items():
            self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, slug)), slug)
            self.assertRegex(published, r"^\d{4}-\d{2}-\d{2}$")
            self.assertRegex(modified, r"^\d{4}-\d{2}-\d{2}$")
            self.assertLessEqual(published, modified, slug)

    def test_the_hand_written_article_is_in_the_registry(self):
        self.assertIn("dealer-vs-independent-german-car-repair.html", posts.POST_DATES)

    def test_titles_carry_the_site_name_once(self):
        for post in posts.POSTS:
            self.assertTrue(post["title"].endswith(" | German Performance"), post["slug"])
            self.assertEqual(post["title"].count("|"), 1, post["slug"])
            self.assertLessEqual(len(post["description"]), 160, post["slug"])


class Rendered(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sk = build_posts.skeleton()
        cls.pages = {p["slug"]: build_posts.build(p, sk) for p in posts.POSTS}
        cls.sk = sk

    def test_head_and_body_type(self):
        for post in posts.POSTS:
            html = self.pages[post["slug"]]
            self.assertIn(f"<title>{post['title']}</title>", html)
            self.assertIn(f'<link rel="canonical" href="{page_url(post["slug"])}">', html)
            self.assertIn('<body data-page-type="post">', html)
            self.assertIn(f'<meta name="description" content="{post["description"]}">', html)

    def test_body_links_the_homepage_services(self):
        for slug, html in self.pages.items():
            self.assertIn('href="/#services"', body_of(html), slug)

    def test_body_carries_the_technicians_note_and_further_reading(self):
        for slug, html in self.pages.items():
            body = body_of(html)
            self.assertIn("ASE Master Technician", body, slug)
            self.assertIn('href="/dealer-vs-independent-german-car-repair"', body, slug)

    def test_posts_link_each_other(self):
        slugs = [p["slug"] for p in posts.POSTS]
        for slug in slugs:
            for other in slugs:
                if other != slug:
                    self.assertIn(f'href="{page_url(other).replace(build_posts.SITE, "")}"',
                                  body_of(self.pages[slug]), (slug, other))

    def test_no_html_spelling_in_body_links(self):
        for slug, html in self.pages.items():
            for href in HREF_RE.findall(body_of(html)):
                self.assertNotIn(".html", href, (slug, href))

    def test_length_is_an_article_not_a_note(self):
        for slug, html in self.pages.items():
            self.assertGreaterEqual(words_in(html), MIN_WORDS, slug)

    def test_second_render_is_identical(self):
        for post in posts.POSTS:
            self.assertEqual(self.pages[post["slug"]], build_posts.build(post, self.sk))


if __name__ == "__main__":
    unittest.main(verbosity=1)
