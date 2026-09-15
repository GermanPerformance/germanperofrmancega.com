# tools/

Plain Python 3, no dependencies. Run everything from the repo root.

## Where things are decided

- `service_catalog.py` — every service page: its make, its job, its one
  name. The nav, hub grids, footer, related blocks, breadcrumbs, `llms.txt`
  and the consistency checker derive from it. Add a page here first.
- `brand_pages/<make>.py` — the copy for a make's pages (`build_service_pages.py`).
- `landing_pages.py` — the copy for the category landing pages (`build_landing_pages.py`).
- `gbp_claims.py` — which Google Business Profile services each page answers for.
- `place.py` — the shop's Google listing (place ID, CID, pin) and every Maps URL: embed, directions, `hasMap`, `sameAs`, write-a-review.
- `redirects.py` — retired URLs and their successors (stubs, never in the sitemap).
- `page_chrome.py` — the nav, footer, address block and asset links every generated page shares.
- `apply_redesign.py` — `VERSION` (bump when a stylesheet or script changes)
  and the "run last" normaliser every page passes through.

## Pipeline

```
python3 tools/build_service_pages.py          # brand_pages/*.py -> make pages
python3 tools/build_general_service_pages.py  # three category pages on the same template
python3 tools/build_brand_hubs.py             # five make hubs
python3 tools/build_info_pages.py             # about, contact
python3 tools/build_landing_pages.py          # landing_pages.py -> category landing pages
python3 tools/build_privacy_page.py
python3 tools/apply_redesign.py               # nav, chrome, footer columns, version stamps
python3 tools/fix_footer_links.py             # footer Services column + link row
python3 tools/add_related_services.py         # in-body related block + hub link row
python3 tools/fix_breadcrumbs.py              # Home / <Make> Repair / <Make> <Job>
python3 tools/build_social_tags.py            # Open Graph / Twitter (before schema: og:image)
python3 tools/build_schema.py                 # JSON-LD from the page as it stands
python3 tools/build_sitemap.py
python3 tools/build_llms_txt.py
python3 tools/build_redirects.py
```

A second pass must change nothing (`git status` clean after re-running).

## Checkers and tests

```
for c in check_links check_faq check_analytics check_design_system check_contrast \
         check_gbp_alignment check_catalog_consistency check_hero_lines; do
  python3 tools/$c.py || break
done
for t in tools/test_*.py; do python3 $t || break; done
```

`check_hero_lines.py` and `check_tracking_e2e.cjs` need Playwright's
chrome-headless-shell and skip without it. Never drive Chrome.app headless
for measurements; use the shell.
