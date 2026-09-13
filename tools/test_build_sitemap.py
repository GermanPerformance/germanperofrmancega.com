#!/usr/bin/env python3
"""The sitemap's <lastmod> must be the date the page actually changed.

A page edited in the working tree and not yet committed is going to be
committed at deploy time, so its date is today; an untouched page keeps
the date of its last commit.

Run from the repo root:  python3 tools/test_build_sitemap.py
"""

import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sitemap  # noqa: E402

TODAY = datetime.date(2026, 9, 12)


class ChooseDate(unittest.TestCase):
    def test_clean_committed_page_keeps_its_commit_date(self):
        self.assertEqual(build_sitemap.choose_date("2026-07-28", False, TODAY),
                         "2026-07-28")

    def test_dirty_page_is_dated_today(self):
        self.assertEqual(build_sitemap.choose_date("2026-07-28", True, TODAY),
                         "2026-09-12")

    def test_never_committed_page_is_dated_today(self):
        self.assertEqual(build_sitemap.choose_date("", False, TODAY),
                         "2026-09-12")


if __name__ == "__main__":
    unittest.main()
