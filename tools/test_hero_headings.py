#!/usr/bin/env python3
"""Guard the hero headline and the "Why German Performance" header.

Every hero h1 renders at the homepage's tier (werkstatt's h1 rule) and
holds two lines from 900px through a `<br class="h1-br">`. The generators
still write three stacked lines, and apply_redesign.hero_h1() merges them;
the .two column's label and title move to a centred .sh above the grid
through apply_redesign.two_heading(). These tests pin both steps' output,
their idempotence, the words-never-change rule behind H1_SPLITS, and the
live pages' state, so a generator that starts emitting a form the merge
cannot read fails here before it ships a three-line hero.

Run from the repo root:  python3 tools/test_hero_headings.py
"""

import os
import re
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import apply_redesign  # noqa: E402
from redirects import site_pages  # noqa: E402

THREE = ('<h1 class="fu">AUDI<br><span class="outline">BRAKE</span>'
         '<br><span class="accent">SERVICE</span></h1>')
TWO = '<h1 class="fu">AUDI BRAKE<br class="h1-br"> <span class="accent">SERVICE</span></h1>'
UNSPACED = '<h1 class="fu">AUDI BRAKE<br class="h1-br"><span class="accent">SERVICE</span></h1>'
AMP = ('<h1 class="fu">BMW<br><span class="outline">REPAIR</span>'
       '<br><span class="accent">&amp; SERVICE</span></h1>')
NOT_FOUND = '<h1 class="fu">WRONG<br><span class="outline">TURN</span></h1>'
LANDING = ('<h1 class="fu" style="--h1-em:8.94">Brake Repair in<br>'
           '<span class="accent">Snellville,&nbsp;GA</span></h1>')

IN_COLUMN = (
    '    <div class="two fu">\n'
    '      <div>\n'
    '        <div class="sl">Why German Performance</div>\n'
    '        <h2>AUDI BRAKE<br><span class="accent">SPECIALISTS</span></h2>\n'
    '        <p class="sd">Copy.</p>\n'
    '      </div>\n'
    '    </div>\n')
LIFTED = (
    '    <div class="sh fu"><div class="sl">Why German Performance</div>'
    '<h2>AUDI BRAKE<br><span class="accent">SPECIALISTS</span></h2></div>\n'
    '    <div class="two fu">\n'
    '      <div>\n'
    '        <p class="sd">Copy.</p>\n'
    '      </div>\n'
    '    </div>\n')
FIGURE_FIRST = (
    '    <div class="two fu">\n'
    '      <figure class="svc-figure"><img src="x.jpg" alt=""></figure>\n'
    '      <div>\n'
    '        <p class="sd">Copy.</p>\n'
    '      </div>\n'
    '    </div>\n')

HERO_RE = re.compile(r'<section class="hero[^"]*">.*?</section>', re.S)
H1_RE = re.compile(r'<h1[^>]*>.*?</h1>', re.S)


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def pages():
    return sorted(site_pages(f for f in os.listdir(REPO_ROOT) if f.endswith(".html")))


def words(*lines):
    return sorted(" ".join(lines).split())


class HeroH1Tests(unittest.TestCase):
    def test_three_lines_merge_into_two(self):
        self.assertEqual(apply_redesign.hero_h1(THREE), TWO)

    def test_ampersand_stays_with_its_word(self):
        self.assertEqual(
            apply_redesign.hero_h1(AMP),
            '<h1 class="fu">BMW REPAIR<br class="h1-br"> <span class="accent">&amp;&nbsp;SERVICE</span></h1>')

    def test_404_keeps_both_words_white(self):
        self.assertEqual(apply_redesign.hero_h1(NOT_FOUND),
                         '<h1 class="fu">WRONG<br class="h1-br"> TURN</h1>')

    def test_landing_form_is_left_alone(self):
        self.assertEqual(apply_redesign.hero_h1(LANDING), LANDING)

    def test_merge_is_idempotent(self):
        once = apply_redesign.hero_h1(THREE)
        self.assertEqual(apply_redesign.hero_h1(once), once)

    def test_break_without_its_word_space_is_healed(self):
        self.assertEqual(apply_redesign.hero_h1(UNSPACED), TWO)

    def test_splits_keep_every_word(self):
        for key, (white, red) in apply_redesign.H1_SPLITS.items():
            self.assertEqual(len(key), 3, key)
            self.assertEqual(words(*key), words(white, red), key)

    def test_splits_apply(self):
        for (a, b, c), (white, red) in apply_redesign.H1_SPLITS.items():
            src = (f'<h1 class="fu">{a}<br><span class="outline">{b}</span>'
                   f'<br><span class="accent">{c}</span></h1>')
            self.assertEqual(apply_redesign.hero_h1(src), apply_redesign.h1_markup(white, red))


class TwoHeadingTests(unittest.TestCase):
    def test_in_column_header_is_lifted(self):
        self.assertEqual(apply_redesign.two_heading(IN_COLUMN), LIFTED)

    def test_lift_is_idempotent(self):
        self.assertEqual(apply_redesign.two_heading(LIFTED), LIFTED)

    def test_figure_first_block_is_left_alone(self):
        self.assertEqual(apply_redesign.two_heading(FIGURE_FIRST), FIGURE_FIRST)


class LivePageTests(unittest.TestCase):
    def test_every_hero_h1_is_two_lines_without_outline(self):
        for name in pages():
            html = read(name)
            hero = HERO_RE.search(html)
            if not hero:
                continue
            h1 = H1_RE.search(hero.group(0))
            self.assertIsNotNone(h1, name)
            self.assertNotIn('class="outline"', h1.group(0), name)
            self.assertEqual(h1.group(0).count("<br"), 1, (name, h1.group(0)))
            if "h1-br" in h1.group(0):
                self.assertIn('<br class="h1-br"> ', h1.group(0), name)

    def test_every_catalog_page_names_the_city_in_its_h1(self):
        """The money-page framework, on all twelve catalog pages since
        2026-09-15: "{service} in" over "Snellville, GA", on a .hero-svc
        hero so the first line is sized to fit (owner: the city belongs in
        the main header of every service page)."""
        import service_catalog
        for p in service_catalog.PAGES:
            html = read(p.slug)
            hero = HERO_RE.search(html)
            self.assertIsNotNone(hero, p.slug)
            self.assertIn("hero-svc", hero.group(0)[:80], p.slug)
            h1 = H1_RE.search(hero.group(0)).group(0)
            self.assertRegex(h1, r' in<br><span class="accent">Snellville,&nbsp;GA</span></h1>$', p.slug)
            self.assertIn('style="--h1-em:', h1, p.slug)

    def test_no_two_column_still_holds_its_header(self):
        for name in pages():
            self.assertIsNone(apply_redesign.TWO_HEAD_RE.search(read(name)), name)

    def test_transform_is_a_no_op_on_live_pages(self):
        for name in pages():
            if name == "index.html":
                continue
            html = read(name)
            self.assertEqual(apply_redesign.transform(html), html, name)


if __name__ == "__main__":
    unittest.main(verbosity=1)
