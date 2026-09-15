#!/usr/bin/env python3
"""Guard the supporting articles, the guides index and the post registry.

Every article in tools/posts/ must render on the blog skeleton, link the
money page it supports, carry a dated byline and the technicians' note,
link the other articles of its cluster, use clean addresses for every
local link, and render identically on a second pass. The registry must
know the dates of every article on disk, the hand-written one included,
so build_schema.py has one source of truth, and the guides index must
list every one of them.

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
from urls import href_for, page_url  # noqa: E402

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

    def test_body_links_the_page_it_supports(self):
        for post in posts.POSTS:
            body = body_of(self.pages[post["slug"]])
            expected = "/#services" if post["hub"] == posts.HOME_PAGE else href_for(post["hub"])
            self.assertIn(f'href="{expected}"', body, post["slug"])

    def test_body_carries_a_dated_byline_and_the_technicians_note(self):
        for post in posts.POSTS:
            body = body_of(self.pages[post["slug"]])
            published, modified = posts.POST_DATES[post["slug"]]
            self.assertIn(f'<time datetime="{published}">', body, post["slug"])
            if modified != published:
                self.assertIn(f'<time datetime="{modified}">', body, post["slug"])
            self.assertIn("ASE Master Technician", body, post["slug"])

    def test_further_reading_renders_every_listed_article(self):
        for post in posts.POSTS:
            body = body_of(self.pages[post["slug"]])
            self.assertTrue(post["further"], post["slug"])
            for other in post["further"]:
                self.assertIn(f'href="{href_for(other)}"', body, (post["slug"], other))

    def test_posts_link_their_cluster(self):
        for post in posts.POSTS:
            body = body_of(self.pages[post["slug"]])
            for other in posts.POSTS:
                if other is not post and other["cluster"] == post["cluster"]:
                    self.assertIn(f'href="{href_for(other["slug"])}"', body,
                                  (post["slug"], other["slug"]))

    def test_sources_are_external_and_rendered(self):
        for post in posts.POSTS:
            body = body_of(self.pages[post["slug"]])
            for label, url in post["sources"]:
                self.assertTrue(url.startswith("https://"), (post["slug"], url))
                self.assertIn(f'href="{url}" target="_blank" rel="noopener">{label}</a>', body)
            self.assertEqual("<h2>Sources</h2>" in body, bool(post["sources"]), post["slug"])

    def test_no_html_spelling_in_local_links(self):
        for slug, html in self.pages.items():
            for href in HREF_RE.findall(body_of(html)):
                if href.startswith("/"):
                    self.assertNotIn(".html", href, (slug, href))

    def test_length_is_an_article_not_a_note(self):
        for slug, html in self.pages.items():
            self.assertGreaterEqual(words_in(html), MIN_WORDS, slug)

    def test_second_render_is_identical(self):
        for post in posts.POSTS:
            self.assertEqual(self.pages[post["slug"]], build_posts.build(post, self.sk))


class GuidesIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = build_posts.build_guides(build_posts.skeleton())

    def test_head(self):
        self.assertIn(f"<title>{build_posts.GUIDES_TITLE}</title>", self.html)
        self.assertIn(f'<link rel="canonical" href="{page_url(posts.GUIDES_PAGE)}">', self.html)
        self.assertIn('<body data-page-type="info">', self.html)

    def test_every_dated_article_is_listed_once_with_its_summary(self):
        body = body_of(self.html)
        for slug in posts.POST_DATES:
            self.assertEqual(body.count(f'href="{href_for(slug)}"'), 1, slug)
            self.assertIn(posts.READING[slug], body, slug)
            self.assertIn(posts.SUMMARY[slug], body, slug)

    def test_groups_follow_the_registry(self):
        body = body_of(self.html)
        for heading, _, slugs in posts.GUIDES:
            self.assertEqual(f"<h2>{heading}</h2>" in body, bool(slugs), heading)


class Registry2(unittest.TestCase):
    def test_every_post_names_a_money_page_and_a_cluster(self):
        money = {posts.HOME_PAGE, posts.BMW_HUB, posts.MERCEDES_HUB}
        for post in posts.POSTS:
            self.assertIn(post["hub"], money, post["slug"])
            self.assertIn(post["cluster"], {"general", "bmw", "mercedes"}, post["slug"])
        for slug in posts.POST_DATES:
            self.assertIn(slug, posts.HUB_OF)
            self.assertIn(slug, posts.CLUSTER_OF)

    def test_guides_cover_every_dated_article_once(self):
        listed = [slug for _, _, slugs in posts.GUIDES for slug in slugs]
        self.assertEqual(sorted(listed), sorted(posts.POST_DATES))
        for _, hub, slugs in posts.GUIDES:
            self.assertEqual(posts.guides_for(hub), slugs)


if __name__ == "__main__":
    unittest.main(verbosity=1)
