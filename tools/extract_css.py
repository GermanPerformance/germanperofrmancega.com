#!/usr/bin/env python3
"""Move inline CSS into shared stylesheets.

The 30 service pages each carried a byte-identical 9.7KB <style> block --
about 40% of the page -- and index.html had its CSS spread across seven
blocks, five of them inside <body> and one after </footer>. That makes every
visual change a 32-file edit and stops the browser caching any of it.

Selector overlap between the service and homepage sheets is only ~29%, and
both define the same selectors with different values, so merging them into
one file would change rendering. Instead:

    tokens.css   design tokens, shared by all 32 pages
    site.css     the 30 service pages
    home.css     index.html
    post.css     the blog post

Block order is preserved when concatenating, so the cascade is unchanged.

Run from the repo root:  python3 tools/extract_css.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(REPO_ROOT, "assets", "css")
VERSION = 1     # bump to bust the cache when the CSS changes

HOME = "index.html"
POST = "dealer-vs-independent-german-car-repair.html"

STYLE_RE = re.compile(r'[ \t]*<style[^>]*>(.*?)</style>\n?', re.S)
ROOT_RE = re.compile(r':root\s*\{.*?\}\s*', re.S)

# Union of the tokens the three page types defined. Values were already
# consistent; --carbon differed only as #111 vs #111111, and the same colour
# was named --red-b on service pages and --red-bright elsewhere. Both names
# are kept so no existing rule breaks.
TOKENS = """/* Design tokens, shared by every page.
   Single source of truth for the site's colour system. */
:root {
  --black: #0a0a0a;
  --carbon: #111111;
  --steel: #1c1c1e;
  --mid: #2a2a2a;
  --muted: #555;
  --silver: #9a9a9a;
  --light: #d4d4d4;
  --white: #f0ede8;
  --red: #c0392b;
  --gold: #d4a017;
  --gold-light: #f0b820;

  /* Same colour, two historical names: service pages used --red-b,
     the homepage and blog used --red-bright. */
  --red-bright: #e74c3c;
  --red-b: #e74c3c;
}
"""


def page_type(name):
    if name == HOME:
        return "home"
    if name == POST:
        return "post"
    return "site"


def extract(name):
    """Pull every <style> block out of a page, in document order."""
    path = os.path.join(REPO_ROOT, name)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    blocks = STYLE_RE.findall(content)
    if not blocks:
        return None, content

    css = "\n".join(b.strip() for b in blocks)
    # Tokens now live in tokens.css.
    css = ROOT_RE.sub("", css, count=1)

    content = STYLE_RE.sub("", content)
    return css, content


def link_tags(sheet):
    return (f'<link rel="stylesheet" href="assets/css/tokens.css?v={VERSION}">\n'
            f'<link rel="stylesheet" href="assets/css/{sheet}.css?v={VERSION}">\n')


def main():
    os.makedirs(CSS_DIR, exist_ok=True)

    pages = sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html"))
    sheets = {}
    rewritten = {}

    for name in pages:
        css, content = extract(name)
        if css is None:
            print(f"  skip {name}: no <style> block")
            continue
        kind = page_type(name)
        # Every service page must produce identical CSS, or they have drifted.
        if kind in sheets and sheets[kind] != css:
            raise SystemExit(f"{name}: CSS differs from other '{kind}' pages")
        sheets[kind] = css
        rewritten[name] = content

    with open(os.path.join(CSS_DIR, "tokens.css"), "w", encoding="utf-8") as fh:
        fh.write(TOKENS)

    for kind, css in sheets.items():
        with open(os.path.join(CSS_DIR, f"{kind}.css"), "w", encoding="utf-8") as fh:
            fh.write(css + "\n")
        print(f"assets/css/{kind}.css: {len(css) / 1024:.1f} KB")

    for name, content in rewritten.items():
        # Stylesheets go where the first <style> was: in <head>, before the
        # Google Fonts link so page CSS still wins over nothing, and well
        # ahead of any body content.
        tags = link_tags(page_type(name))
        anchor = '<link href="https://fonts.googleapis.com/css2'
        if anchor in content:
            idx = content.index(anchor)
            end = content.index(">", idx) + 2
            content = content[:end] + tags + content[end:]
        else:
            content = content.replace("</head>", tags + "</head>", 1)
        with open(os.path.join(REPO_ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(content)

    print(f"\n{len(rewritten)} pages now load shared stylesheets")
    left = sum(len(STYLE_RE.findall(open(os.path.join(REPO_ROOT, p),
                                        encoding='utf-8').read())) for p in pages)
    print(f"inline <style> blocks remaining: {left}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
