#!/usr/bin/env python3
"""Guard the catalog every service list on the site derives from.

tools/service_catalog.py is the one place a page, a make or a service
name lives. The nav panel, phone menu, brand-hub grids, footer columns,
related-services blocks, breadcrumbs and llms.txt all read it, so a row
that is wrong here is wrong on every page at once. These tests pin the
shape the consumers rely on and the naming rules the site follows.

Run from the repo root:  python3 tools/test_service_catalog.py
"""

import os
import sys
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import redirects  # noqa: E402
import service_catalog as cat  # noqa: E402

SERVICE_ORDER = [key for key, _ in cat.SERVICES]
RETIRED_LABELS = ("VW ", "Brake Service", "Transmission Service",
                  "Spark Plugs", "Full Inspection")


class RowTests(unittest.TestCase):
    def test_slugs_are_unique(self):
        slugs = [p.slug for p in cat.PAGES]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_slug_is_a_live_page(self):
        for page in cat.PAGES:
            self.assertTrue(os.path.isfile(os.path.join(REPO_ROOT, page.slug)),
                            f"missing page: {page.slug}")
            self.assertFalse(redirects.is_redirect(page.slug),
                             f"{page.slug}: a redirect stub is not a page")

    def test_keys_resolve(self):
        makes = {m.key for m in cat.MAKES}
        for page in cat.PAGES:
            self.assertIn(page.service, SERVICE_ORDER, page.slug)
            if page.make is not None:
                self.assertIn(page.make, makes, page.slug)

    def test_each_make_has_exactly_one_hub(self):
        for make in cat.MAKES:
            hubs = [p for p in cat.pages_for(make.key) if p.service == "repair"]
            self.assertEqual([p.slug for p in hubs], [make.hub], make.key)


class DerivedShapeTests(unittest.TestCase):
    """What apply_redesign, build_brand_hubs, build_llms_txt and
    test_nav_menu read: the names and shapes must not move."""

    def test_groups_are_the_generic_column_then_the_makes(self):
        names = [name for name, _ in cat.GROUPS]
        self.assertEqual(names, [cat.GENERIC_GROUP, cat.MAKES_GROUP])
        for name, _ in cat.GROUPS:
            self.assertIn(name, cat.HUBS)

    def test_money_services_lead_the_generic_column(self):
        _, first = cat.GROUPS[0]
        self.assertEqual(tuple(first[:len(cat.MONEY)]), tuple(cat.MONEY))

    def test_makes_column_is_the_hubs_in_make_order(self):
        column = dict(cat.GROUPS)[cat.MAKES_GROUP]
        self.assertEqual(column, cat.hubs())
        self.assertEqual([h for h, _ in column][:2],
                         ["bmw-repair.html", "mercedes-repair.html"])

    def test_labels_are_unique_within_a_column(self):
        for name, entries in cat.GROUPS:
            labels = [label for _, label in entries]
            self.assertEqual(len(labels), len(set(labels)), name)

    def test_every_entry_is_a_catalog_page(self):
        for _, entries in cat.GROUPS:
            for href, _ in entries:
                self.assertEqual(cat.nav_label(href), dict(entries)[href])


class NamingTests(unittest.TestCase):
    def test_no_retired_spelling_survives(self):
        labels = [label for _, entries in cat.GROUPS for _, label in entries]
        labels += [cat.full_label(p.slug) for p in cat.PAGES]
        for label in labels:
            for retired in RETIRED_LABELS:
                self.assertNotIn(retired, label)
            if "Cooling System" in label:
                self.assertIn("Cooling System Repair", label)

    def test_hubs_are_named_make_then_repair_everywhere(self):
        self.assertEqual(cat.full_label("mercedes-repair.html"),
                         "Mercedes Repair")
        self.assertEqual(cat.full_label("volkswagen-repair.html"),
                         "Volkswagen Repair")
        self.assertEqual(cat.nav_label("bmw-repair.html"), "BMW Repair")

    def test_no_make_has_job_pages_any_more(self):
        for page in cat.PAGES:
            if page.make is not None:
                self.assertEqual(page.service, "repair", page.slug)

    def test_generic_pages_keep_their_own_names(self):
        self.assertEqual(cat.full_label("german-car-oil-change.html"),
                         "German Car Oil Change")
        self.assertEqual(cat.nav_label("german-car-ac-repair.html"),
                         "Auto Air Conditioning")
        self.assertEqual(cat.nav_label("german-car-pre-purchase-inspection.html"),
                         "Pre-Purchase Inspection")


class HelperTests(unittest.TestCase):
    def test_hub_for_every_make_page(self):
        for page in cat.PAGES:
            hub = cat.hub_for(page.slug)
            if page.make is None:
                self.assertIsNone(hub, page.slug)
            else:
                self.assertEqual(hub, cat.make(page.make).hub, page.slug)

    def test_service_pages_exclude_hubs_and_keep_order(self):
        pages = cat.service_pages()
        hubs = {m.hub for m in cat.MAKES}
        self.assertEqual(len(pages), len(cat.PAGES) - len(cat.MAKES))
        self.assertFalse(hubs & set(pages))
        generic = [p for p in pages if cat.make_of(p) is None]
        self.assertEqual(generic, [h for h, _ in cat.GROUPS[0][1]])
        self.assertEqual(pages.index(generic[0]), len(pages) - len(generic))

    def test_hubs_lists_every_make_in_order(self):
        self.assertEqual(cat.hubs(), tuple((m.hub, f"{m.short} Repair") for m in cat.MAKES))

    def test_ranking_groups(self):
        self.assertEqual(cat.ranking_group("oil"), "oil")
        self.assertEqual(cat.ranking_group("plugs"), "ignition")
        self.assertEqual(cat.ranking_group("tune-up"), "ignition")
        for key in ("cel", "diagnostics", "engine"):
            self.assertEqual(cat.ranking_group(key), "engine")
        self.assertEqual(cat.ranking_group("repair"), "general")

    def test_unknown_slug_is_an_error(self):
        for helper in (cat.full_label, cat.nav_label, cat.make_of,
                       cat.service_of, cat.hub_for):
            with self.assertRaises(SystemExit):
                helper("no-such-page.html")


if __name__ == "__main__":
    unittest.main(verbosity=1)
