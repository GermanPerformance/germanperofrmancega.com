#!/usr/bin/env python3
"""Verify the site's service pages mirror the Google Business Profile.

The profile's categories and services are exported to
german-performance-gbp-categories-services.md. Every service on that list
must be answered by a page on the site, and every service or hub page on
the site must answer for at least one profile service: a page the profile
does not advertise is an orphan, and a service the site does not describe
is a promise the site does not keep.

Claims come from three places:
  landing_pages.PAGES  -- framework pages, each carrying a "gbp" tuple
  gbp_claims.LEGACY    -- hand-written pages not yet migrated
  gbp_claims.PENDING   -- agreed pages not yet built (reported, not failed)
and gbp_claims.UNCOVERED names the services the owner chose to leave
without a page. Claiming one of those is an error, so the list cannot rot.

Run from the repo root:  python3 tools/check_gbp_alignment.py
Exit code 0 = aligned, 1 = drift found.
"""

import os
import re
import sys
from collections import defaultdict

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import gbp_claims  # noqa: E402
from redirects import site_pages  # noqa: E402

REPO_ROOT = os.path.dirname(TOOLS)
PROFILE_FILE = "german-performance-gbp-categories-services.md"

# Page types that must answer for a profile service.
CLAIMING_TYPES = {"service", "hub"}

CATEGORY_RE = re.compile(r"^###\s+(.+?)\s*$")
ITEM_RE = re.compile(r"^-\s+(.+?)\s*$")
PAGE_TYPE_RE = re.compile(r'<body[^>]*\sdata-page-type="([^"]+)"')


def normalise(service):
    """One spelling for matching: case and whitespace do not distinguish."""
    return " ".join(service.split()).casefold()


def profile_services(text):
    """Every category and service in the export, {normalised: as written}.

    Secondary categories repeat the primary's generic services; the first
    spelling seen is the one reported.
    """
    found = {}
    for line in text.splitlines():
        match = CATEGORY_RE.match(line) or ITEM_RE.match(line)
        if match:
            found.setdefault(normalise(match.group(1)), match.group(1).strip())
    return found


def page_types(root):
    """{filename: data-page-type} for every page at the root."""
    types = {}
    for name in site_pages(os.listdir(root)):
        with open(os.path.join(root, name), encoding="utf-8") as fh:
            match = PAGE_TYPE_RE.search(fh.read())
        types[name] = match.group(1) if match else ""
    return types


def framework_claims():
    """The "gbp" tuple of every framework page, if the module exists yet."""
    try:
        import landing_pages
    except ImportError:
        return {}
    return {page["slug"]: tuple(page["gbp"]) for page in landing_pages.PAGES}


def _claim_problems(claims, source, profile, uncovered, existing):
    """Problems inside one claims dict: unknown services, missing pages."""
    for slug, services in sorted(claims.items()):
        if slug not in existing:
            yield slug, f"{source} claims a page that is not on disk"
        for service in services:
            key = normalise(service)
            if key not in profile:
                yield slug, f'claims "{service}", which is not on the profile'
            elif key in uncovered:
                yield slug, f'claims "{service}", which is listed as UNCOVERED'


def check(root, profile, framework, legacy, pending, uncovered):
    """Yield (subject, reason) for every way the site and profile disagree."""
    types = page_types(root)
    uncovered_keys = {normalise(s) for s in uncovered}

    for service in sorted(uncovered):
        if normalise(service) not in profile:
            yield PROFILE_FILE, f'UNCOVERED names "{service}", which is not on the profile'

    for slug in sorted(set(framework) & set(legacy)):
        yield slug, "in both landing_pages.PAGES and LEGACY (two writers)"
    for slug in sorted(set(pending) & (set(framework) | set(legacy) | set(types))):
        yield slug, "listed in PENDING but already exists"

    yield from _claim_problems(framework, "landing_pages.PAGES", profile,
                               uncovered_keys, types)
    yield from _claim_problems(legacy, "LEGACY", profile, uncovered_keys, types)
    for slug, services in sorted(pending.items()):
        for service in services:
            if normalise(service) not in profile:
                yield slug, f'PENDING claims "{service}", which is not on the profile'

    claimed = defaultdict(list)
    for source in (framework, legacy, pending):
        for slug, services in source.items():
            for service in services:
                claimed[normalise(service)].append(slug)

    for key, raw in profile.items():
        if key not in claimed and key not in uncovered_keys:
            yield PROFILE_FILE, f'no page answers for "{raw}"'

    answering = set(framework) | set(legacy)
    for slug, page_type in sorted(types.items()):
        if page_type in CLAIMING_TYPES and slug not in answering:
            yield slug, f"{page_type} page answers for no profile service"


def main():
    with open(os.path.join(REPO_ROOT, PROFILE_FILE), encoding="utf-8") as fh:
        profile = profile_services(fh.read())
    framework = framework_claims()

    problems = list(check(REPO_ROOT, profile, framework, gbp_claims.LEGACY,
                          gbp_claims.PENDING, gbp_claims.UNCOVERED))

    pending_services = {normalise(s) for v in gbp_claims.PENDING.values() for s in v}
    pending_services -= {normalise(s) for src in (framework, gbp_claims.LEGACY)
                         for v in src.values() for s in v}
    if not problems:
        print(f"OK: {len(profile)} profile services answered by "
              f"{len(framework)} framework + {len(gbp_claims.LEGACY)} legacy pages; "
              f"{len(gbp_claims.UNCOVERED)} left uncovered by choice.")
        if gbp_claims.PENDING:
            print(f"    {len(gbp_claims.PENDING)} pages still to build, covering "
                  f"{len(pending_services)} services only they answer for.")
        return 0

    by_reason = defaultdict(list)
    for subject, reason in problems:
        by_reason[reason].append(subject)
    print(f"DRIFT: {len(problems)} problem(s) between the profile and the site\n")
    for reason, subjects in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        print(f"  [{len(subjects):>3}x] {reason}")
        print(f"         e.g. {subjects[0]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
