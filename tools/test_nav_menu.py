#!/usr/bin/env python3
"""Guard the nav's Services menu and the catalog behind it.

The menu is generated from tools/service_catalog.py by apply_redesign.py's
nav_markup(), then written to every page by a regex that ends the phone
menu at its first </div>; the generators copy the same block from a donor
page with a pattern that ends at a newline followed by </div>. These tests
pin the invariants both of those depend on, so a change to the markup that
would truncate the menu on 44 pages fails here first.

Run from the repo root:  python3 tools/test_nav_menu.py
"""

import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import apply_redesign  # noqa: E402
import service_catalog  # noqa: E402
from urls import href_for  # noqa: E402

MOB_GRAB = re.compile(r'<div id="mobile-menu">.*?\n</div>', re.S)
NAV_GRAB = re.compile(r"<nav>.*?</nav>", re.S)


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def ids_in(html):
    return set(re.findall(r'\sid="([^"]+)"', html))


def mobile_menu(html):
    start = html.index('<div id="mobile-menu">')
    return html[start:]


class CatalogTests(unittest.TestCase):
    def all_hrefs(self):
        hrefs = [h for _, entries in service_catalog.GROUPS for h, _ in entries]
        hrefs += list(service_catalog.HUBS.values())
        return hrefs

    def test_every_href_resolves(self):
        for href in self.all_hrefs():
            name, _, anchor = href.partition("#")
            path = os.path.join(REPO_ROOT, name)
            self.assertTrue(os.path.isfile(path), f"missing page: {name}")
            if anchor:
                self.assertIn(anchor, ids_in(read(name)), f"{href}: no such id")

    def test_money_services_lead_the_first_group(self):
        _, first = service_catalog.GROUPS[0]
        self.assertEqual(first[:6], service_catalog.MONEY)

    def test_no_duplicate_pages(self):
        pages = [h for _, entries in service_catalog.GROUPS for h, _ in entries]
        self.assertEqual(len(pages), len(set(pages)))

    def test_every_group_has_a_heading_link(self):
        for name, _ in service_catalog.GROUPS:
            self.assertIn(name, service_catalog.HUBS)


class NavMarkupTests(unittest.TestCase):
    def setUp(self):
        self.home = apply_redesign.nav_markup(home=True)
        self.page = apply_redesign.nav_markup(home=False)

    def test_home_links_down_its_own_document(self):
        for anchor in ('href="#reviews"', 'href="#story"', 'href="#services"',
                       'href="#faq"', 'href="#contact"'):
            self.assertIn(anchor, self.home)
        self.assertNotIn('href="/#', self.home)
        self.assertNotIn('href="/about"', self.home)

    def test_other_pages_link_into_the_homepage(self):
        for target in ('href="/#reviews"', 'href="/about"',
                       'href="/#services"', 'href="/#faq"',
                       'href="/contact"'):
            self.assertIn(target, self.page)
        self.assertNotIn('href="#', self.page)

    def test_every_link_is_a_clean_address(self):
        for markup in (self.home, self.page):
            self.assertNotIn(".html", markup)
        self.assertIn('<a href="/" class="nav-logo">', self.page)

    def test_tuning_is_gone(self):
        for markup in (self.home, self.page):
            self.assertNotIn("#performance", markup)
            self.assertNotIn(">Tuning<", markup)

    def test_nav_tag_stays_bare(self):
        self.assertIn("\n<nav>\n", self.page)

    def test_phone_menu_contains_no_div(self):
        for markup in (self.home, self.page):
            menu = mobile_menu(markup)
            body = menu[len('<div id="mobile-menu">'):]
            self.assertNotIn("<div", body)
            # Only the menu's own closer may sit at column 0.
            self.assertEqual(body.count("\n</div>"), 1)
            self.assertTrue(body.rstrip().endswith("\n</div>"))

    def test_generator_grabs_return_whole_blocks(self):
        mob = MOB_GRAB.search(self.page).group(0)
        self.assertTrue(mob.endswith("\n</div>"))
        self.assertIn('class="mcta"', mob)
        self.assertIn("</details>", mob)
        nav = NAV_GRAB.search(self.page).group(0)
        self.assertIn('class="nav-panel"', nav)
        self.assertIn('class="nav-cta"', nav)

    def test_nav_rule_is_idempotent(self):
        updated, n = apply_redesign.NAV_RE.subn(apply_redesign.NAV, self.page)
        self.assertEqual(n, 1)
        self.assertEqual(updated, self.page)

    def test_phone_details_do_not_join_the_faq_group(self):
        self.assertNotRegex(self.page, r'<details class="mm-dd"[^>]*\sname=')

    def test_spy_hook_is_home_only(self):
        self.assertIn('data-section="#services"', self.home)
        self.assertNotIn("data-section", self.page)

    def test_every_catalog_entry_is_in_both_menus(self):
        nav = NAV_GRAB.search(self.page).group(0)
        mob = mobile_menu(self.page)
        for _, entries in service_catalog.GROUPS:
            for href, label in entries:
                link = f'<a href="{href_for(href)}">{label}</a>'
                self.assertIn(link, nav)
                self.assertIn(link, mob)


class TransformTests(unittest.TestCase):
    def test_transform_is_idempotent_on_a_live_page(self):
        once = apply_redesign.transform(read("about.html"))
        self.assertEqual(apply_redesign.transform(once), once)


class HomepageTests(unittest.TestCase):
    def test_cards_follow_the_money_order(self):
        html = read("index.html")
        section = html[html.index('<section id="services">'):]
        section = section[:section.index("</section>")]
        hrefs = re.findall(r'<a href="([^"]+)" class="bg"', section)
        self.assertEqual(hrefs, [href_for(h) for h, _ in service_catalog.MONEY])


if __name__ == "__main__":
    unittest.main(verbosity=1)
