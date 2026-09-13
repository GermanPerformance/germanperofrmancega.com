#!/usr/bin/env python3
"""Guard the Google Business Profile <-> site alignment checker.

Run from the repo root:  python3 tools/test_gbp_alignment.py
"""

import os
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import check_gbp_alignment as cga  # noqa: E402

PROFILE = """# Google Business Profile Categories & Services

## Primary Category

### Auto repair shop

- Brakes
- Oil change
- Range Rover repair

## Secondary Categories

### Brake shop

- Brakes
- Brake service & repair
"""


def write_pages(root, pages):
    for name, page_type in pages.items():
        with open(os.path.join(root, name), "w", encoding="utf-8") as fh:
            fh.write(f'<html><body data-page-type="{page_type}"></body></html>')


class ProfileParsingTests(unittest.TestCase):
    def test_categories_and_items_are_both_services(self):
        services = cga.profile_services(PROFILE)
        self.assertIn(cga.normalise("Auto repair shop"), services)
        self.assertIn(cga.normalise("Brake shop"), services)
        self.assertIn(cga.normalise("Brakes"), services)

    def test_repeated_items_collapse_to_one(self):
        services = cga.profile_services(PROFILE)
        self.assertEqual(services[cga.normalise("Brakes")], "Brakes")
        self.assertEqual(len(services), 6)

    def test_headings_and_blockquotes_are_not_services(self):
        services = cga.profile_services(PROFILE)
        self.assertNotIn(cga.normalise("Primary Category"), services)
        self.assertNotIn(cga.normalise("Google Business Profile Categories & Services"), services)

    def test_normalise_ignores_case_and_spacing(self):
        self.assertEqual(cga.normalise("  Brake   Service & Repair "),
                         cga.normalise("brake service & repair"))


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        write_pages(self.root, {
            "brake.html": "service",
            "oil.html": "service",
            "about.html": "info",
        })
        self.profile = cga.profile_services(PROFILE)
        self.framework = {"brake.html": ("Auto repair shop", "Brake shop", "Brakes",
                                         "Brake service & repair")}
        self.legacy = {"oil.html": ("Oil change",)}
        self.uncovered = frozenset({"Range Rover repair"})

    def tearDown(self):
        self.tmp.cleanup()

    def problems(self, **overrides):
        args = dict(root=self.root, profile=self.profile, framework=self.framework,
                    legacy=self.legacy, pending={}, uncovered=self.uncovered)
        args.update(overrides)
        return list(cga.check(**args))

    def test_aligned_site_has_no_problems(self):
        self.assertEqual(self.problems(), [])

    def test_unclaimed_profile_service_is_reported(self):
        problems = self.problems(legacy={})
        self.assertTrue(any("Oil change" in reason for _, reason in problems),
                        problems)
        self.assertTrue(any("oil.html" in subject for subject, _ in problems),
                        problems)

    def test_pending_page_covers_its_services_without_existing(self):
        pending = {"oil-planned.html": ("Oil change",)}
        problems = self.problems(legacy={}, pending=pending)
        self.assertFalse(any("Oil change" in reason for _, reason in problems),
                         problems)

    def test_pending_slug_that_exists_is_reported(self):
        pending = {"oil.html": ("Oil change",)}
        problems = self.problems(pending=pending)
        self.assertTrue(any("oil.html" == subject and "PENDING" in reason
                            for subject, reason in problems), problems)

    def test_service_page_without_a_claim_is_reported(self):
        write_pages(self.root, {"orphan.html": "service"})
        problems = self.problems()
        self.assertTrue(any(subject == "orphan.html" for subject, _ in problems),
                        problems)

    def test_info_pages_need_no_claim(self):
        write_pages(self.root, {"contact.html": "info", "404.html": "error",
                                "index.html": "home"})
        self.assertEqual(self.problems(), [])

    def test_claim_of_unknown_service_is_reported(self):
        legacy = {"oil.html": ("Oil change", "Oil chnage")}
        problems = self.problems(legacy=legacy)
        self.assertTrue(any("Oil chnage" in reason for _, reason in problems),
                        problems)

    def test_claim_by_missing_page_is_reported(self):
        legacy = {"oil.html": ("Oil change",), "ghost.html": ("Brakes",)}
        problems = self.problems(legacy=legacy)
        self.assertTrue(any(subject == "ghost.html" for subject, _ in problems),
                        problems)

    def test_claiming_an_uncovered_service_is_reported(self):
        legacy = {"oil.html": ("Oil change", "Range Rover repair")}
        problems = self.problems(legacy=legacy)
        self.assertTrue(any("Range Rover repair" in reason for _, reason in problems),
                        problems)

    def test_uncovered_service_missing_from_profile_is_reported(self):
        problems = self.problems(uncovered=frozenset({"Range Rover repair", "Jaguar"}))
        self.assertTrue(any("Jaguar" in reason for _, reason in problems), problems)

    def test_two_writers_for_one_page_is_reported(self):
        legacy = {"oil.html": ("Oil change",), "brake.html": ("Brakes",)}
        problems = self.problems(legacy=legacy)
        self.assertTrue(any(subject == "brake.html" and "LEGACY" in reason
                            for subject, reason in problems), problems)


class LiveSiteTests(unittest.TestCase):
    def test_the_repo_is_aligned(self):
        self.assertEqual(cga.main(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
