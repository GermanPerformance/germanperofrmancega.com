#!/usr/bin/env python3
"""Verify FAQ structured data matches the visible page content.

Google requires FAQPage markup to match what the user actually sees. This
catches the bug class where a page's schema was copied from another page:
every Question.name in the JSON-LD must appear verbatim in the rendered HTML
of the same page, and the page's own topic must not be contradicted.

Run from the repo root:  python3 tools/check_faq.py
Exit code 0 = consistent, 1 = mismatch found.
"""

import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redirects import site_pages  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.S)
# Every page now renders a question as <details><summary class="fq">; the
# button form is kept so the check still reads any page not yet converted.
QUESTION_BTN_RE = re.compile(
    r'<(button|summary) class="(?:fq|faq-q)"[^>]*>(.*?)</\1>', re.S)

# Marques, so we can flag a page describing a brand it does not serve.
BRANDS = {"bmw": "BMW", "mercedes": "Mercedes", "audi": "Audi",
          "porsche": "Porsche", "volkswagen": "VW"}
# "VW 502 00", "VW 504 00", "VW 507 00" and "VW 508 00" are the names of the
# oil standards every Volkswagen Group engine is approved for, so an Audi
# page has to say them; that is the standard's name, not another marque.
BRAND_PATTERNS = {"BMW": r"\bBMW\b", "Mercedes": r"Mercedes", "Audi": r"\bAudi\b",
                  "Porsche": r"Porsche", "VW": r"\bVW\b(?!\s*50[2478]\s*00)|Volkswagen"}


def visible_questions(content):
    """Question text as rendered, with the +/- icon span stripped."""
    out = []
    for _tag, raw in QUESTION_BTN_RE.findall(content):
        text = re.sub(r'<span class="(?:ficon|faq-icon)"[^>]*>.*?</span>', "", raw, flags=re.S)
        out.append(html.unescape(re.sub(r"<[^>]+>", "", text)).strip())
    return out


def schema_questions(content):
    """Question names declared in every FAQPage on the page.

    Handles both a bare FAQPage and one nested inside an @graph, which is how
    the site now emits it.
    """
    out = []
    for block in JSONLD_RE.findall(content):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON-LD: {exc}") from exc
        nodes = data.get("@graph") or [data]
        for node in nodes:
            if node.get("@type") != "FAQPage":
                continue
            for entity in node.get("mainEntity", []):
                if entity.get("@type") == "Question":
                    out.append(entity["name"].strip())
    return out


def own_brand(filename):
    return next((v for k, v in BRANDS.items() if filename.startswith(k)), None)


def check_page(page, content):
    """Yield problem strings for one page."""
    try:
        schema = schema_questions(content)
    except ValueError as exc:
        yield str(exc)
        return

    visible = visible_questions(content)

    for question in schema:
        if question not in visible:
            yield f'schema question not visible on page: "{question}"'

    # A page whose FAQ names a marque it is not about is copy-paste damage.
    brand = own_brand(page)
    if brand and schema:
        faq_text = " ".join(schema)
        for other, pattern in BRAND_PATTERNS.items():
            if other != brand and re.search(pattern, faq_text):
                yield f"FAQ on a {brand} page mentions {other}"


def main():
    pages = site_pages(os.listdir(REPO_ROOT))
    problems = []

    for page in pages:
        with open(os.path.join(REPO_ROOT, page), encoding="utf-8") as fh:
            content = fh.read()
        for problem in check_page(page, content):
            problems.append((page, problem))

    if problems:
        print(f"FAQ INCONSISTENCIES: {len(problems)}\n")
        for page, problem in problems:
            print(f"  {page}\n    {problem}")
        return 1

    checked = sum(1 for p in pages
                  if schema_questions(open(os.path.join(REPO_ROOT, p),
                                           encoding="utf-8").read()))
    print(f"OK: FAQ schema matches visible content on all {checked} pages with FAQs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
