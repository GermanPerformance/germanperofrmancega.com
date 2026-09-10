#!/usr/bin/env python3
"""Apply the balanced redesign to every page except index.html.

index.html is hand-built. The 33 service and hub pages, the 404 page and
the blog post share one markup pattern, so the redesign reaches them by
transformation rather than by hand. Every rule below maps one piece of the
old markup onto the new system:

  * stylesheets load tokens -> werkstatt (base) -> page sheet, so the base
    no longer has to out-specify the page sheet it used to load after
  * one nav and one mobile menu on every page, with the call button and
    hamburger grouped so the bar reads logo | links | call
  * the hero grid overlay goes; the hero is centred by the base sheet
  * the trust strip drops from five cells to four so it splits evenly
    into 2x2 on a phone and 4x1 on a desktop
  * inline background, colour and spacing styles become classes, so the
    page sheets own the layout again
  * FAQ items become native <details>/<summary>, one open at a time
  * the footer wordmark becomes the logo, and the copyright line moves
    below the link row

Idempotent: running it twice changes nothing the second time.

Run from the repo root:  python3 tools/apply_redesign.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "4"

LOGO_NAV = (
    '<picture class="logo-pic"><source type="image/webp" '
    'srcset="assets/img/logo-144.webp 1x, assets/img/logo-288.webp 2x">'
    '<img src="assets/img/logo-144.png" alt="German Performance" width="132" '
    'height="44" decoding="async" fetchpriority="high"></picture>'
)
LOGO_FOOT = LOGO_NAV.replace(' fetchpriority="high"', ' loading="lazy"')

NAV = f'''<nav>
  <a href="index.html" class="nav-logo">{LOGO_NAV}</a>
  <ul class="nav-links"><li><a href="index.html#services">Services</a></li><li><a href="index.html#about">About</a></li><li><a href="index.html#reviews">Reviews</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="index.html#contact">Contact</a></li></ul>
  <div class="nav-right">
    <a href="tel:+16783957459" class="nav-cta">Call Now</a>
    <button id="hamburger" onclick="toggleMenu()" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
  </div>
</nav>
<div id="mobile-menu">
  <a href="index.html#services" onclick="closeMenu()">Services</a>
  <a href="index.html#about" onclick="closeMenu()">About</a>
  <a href="index.html#reviews" onclick="closeMenu()">Reviews</a>
  <a href="index.html#faq" onclick="closeMenu()">FAQ</a>
  <a href="index.html#contact" onclick="closeMenu()">Contact</a>
  <a href="tel:+16783957459" class="mcta" onclick="closeMenu()">Call (678) 395-7459</a>
</div>'''

FOOTER_COLUMNS = f'''  <div class="ft">
    <div><div class="fb">{LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div></div>
    <div class="fc"><div class="fct">Contact</div><a href="tel:+16783957459">(678) 395-7459</a><p>2144 Parkwood Rd NW</p><p>Snellville, GA 30078</p><p>Mon–Fri: 9:30 AM–6 PM</p></div>
    <div class="fc"><div class="fct">Services</div><a href="bmw-repair-snellville-ga.html">BMW Repair</a><a href="mercedes-repair-snellville-ga.html">Mercedes-Benz Repair</a><a href="audi-repair-snellville-ga.html">Audi Repair</a><a href="porsche-repair-snellville-ga.html">Porsche Repair</a><a href="volkswagen-repair-snellville-ga.html">Volkswagen Repair</a></div>
    <div class="fc"><div class="fct">Navigate</div><a href="index.html">Home</a><a href="index.html#about">About</a><a href="index.html#reviews">Reviews</a><a href="index.html#faq">FAQ</a><a href="dealer-vs-independent-german-car-repair.html">Dealer vs. Independent</a></div>
  </div>'''

# (pattern, replacement) pairs applied in order to every page.
RULES = [
    # -- head: base sheet before page sheet, one script for every page ----
    (r'<link rel="stylesheet" href="assets/css/tokens\.css\?v=\d+">\n'
     r'<link rel="stylesheet" href="assets/css/(site|post)\.css\?v=\d+">\n'
     r'<link rel="stylesheet" href="assets/css/werkstatt\.css\?v=\d+">',
     f'<link rel="stylesheet" href="assets/css/tokens.css?v={VERSION}">\n'
     f'<link rel="stylesheet" href="assets/css/werkstatt.css?v={VERSION}">\n'
     f'<link rel="stylesheet" href="assets/css/\\1.css?v={VERSION}">'),
    (r'<script defer src="assets/js/site\.js\?v=\d+"></script>',
     f'<script defer src="assets/js/site.js?v={VERSION}"></script>'),
    (r'<script defer src="assets/js/analytics\.js\?v=\d+"></script>',
     f'<script defer src="assets/js/analytics.js?v={VERSION}"></script>'),

    # -- nav and mobile menu ------------------------------------------------
    (r'<nav>.*?</nav>(?:\s*<div id="mobile-menu">.*?</div>)?', NAV),

    # -- hero -----------------------------------------------------------------
    (r'<div class="hgrid"></div>', ''),
    # The trust strip under the hero carries the rating; the eyebrow need not.
    (r' &nbsp;·&nbsp;<span class="eyebrow-highlight">4\.5★ Rated</span>', ''),
    # Eyebrow text goes in a span so its two rules stay centred when it wraps.
    (r'<div class="eyebrow( fu)?">(?!<span>)(.*?)</div>', r'<div class="eyebrow\1"><span>\2</span></div>'),
    (r'<section class="hero" style="min-height:60vh;padding-top:150px">', '<section class="hero">'),

    # -- trust strip: four cells, not five ---------------------------------
    (r'\s*<div class="ti"><div class="tv">Same</div><div class="tl">Week Appointments<br>Available</div></div>', ''),

    # -- inline styles become classes -------------------------------------
    (r'<section style="background:var\(--black\);padding:80px 60px;text-align:center">', '<section class="cta-final">'),
    (r'<section style="background:var\(--(?:carbon|black)\)">', '<section>'),
    (r'<span style="color:var\(--red\)">', '<span class="accent">'),
    (r'<span style="color:var\(--silver\)">', '<span class="crumb-here">'),
    (r'<strong style="color:var\(--white\)">', '<strong>'),
    (r'<div class="fu"><div class="sl">', '<div class="sh fu"><div class="sl">'),
    (r'<div style="max-width:820px;margin:0 auto">', '<div class="narrow">'),
    (r'<h2 style="margin-bottom:20px">', '<h2>'),
    (r'<h2 style="display:inline-block; border:none; padding:0;">', '<h2>'),
    (r'<p class="sd" style="margin:0 auto 44px;text-align:center;max-width:480px">', '<p class="sd">'),
    (r'<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">', '<div class="acts">'),
    (r'<div class="sl" style="justify-content:center">', '<div class="sl">'),
    (r'<p class="sd" style="margin-bottom:0">', '<p class="sd">'),
    (r'<div class="fu" style="margin-top:44px">', '<div class="sub-block fu">'),
    (r'<div class="rel-grid" style="margin-top:20px">', '<div class="rel-grid">'),
    (r'<p class="sd fu" style="margin-top:36px">', '<p class="sd fu note">'),
    (r'<div class="flinks fu" style="margin-top:28px">', '<div class="flinks fu">'),
    (r'<div class="fu" style="display:flex;flex-wrap:wrap;gap:18px 32px;margin-top:36px">', '<div class="fu link-row">'),

    # -- FAQ: native disclosure -------------------------------------------
    (r'<div class="fi fu"><button class="fq" onclick="toggleFaq\(this\)">(.*?)<span class="ficon">\+</span></button><div class="fa">(.*?)</div></div>',
     r'<details class="fi fu" name="faq"><summary class="fq">\1<span class="ficon" aria-hidden="true"></span></summary><div class="fa">\2</div></details>'),

    # -- red band: a red button on a red band is invisible ----------------
    # The band is written on one line, so stay on that line; a dot-all
    # match would reach the next .bp on the page, in the closing section.
    (r'(<div class="cta-band fu">[^\n]*?)class="bp"', r'\1class="bw"'),
    (r'(<section class="cta-final">(?:(?!</section>).)*?)class="bw"', r'\1class="bp"'),

    # -- footer --------------------------------------------------------------
    (r'<div class="fb">GERMAN <span>PERFORMANCE</span></div><div class="ftag">BMW · Mercedes · Audi · Porsche · VW</div>',
     f'<div class="fb">{LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div>'),
    (r'(\s*<div class="fcopy">.*?</div>)(\s*<div class="flinks">.*?</div>)', r'\2\1'),
    # The blog post carried its own footer classes; give it the shared one.
    (r'<footer>\s*<div class="footer-copy">(.*?)</div>\s*<div class="footer-links">(.*?)</div>\s*</footer>',
     '<footer>\n' + FOOTER_COLUMNS + r'\n  <div class="flinks">\2</div>' + '\n' + r'  <div class="fcopy">\1</div>' + '\n</footer>'),

    # -- call bar: two buttons, no hours line -----------------------------
    (r'\s*<div class="cb-hours">.*?</div>', ''),
]

# The 404 page listed its shortcuts as eight outlined buttons in a row.
LINK_ROW_BUTTONS = re.compile(r'(<div class="fu link-row">)(.*?)(</div>)', re.S)


def transform(html):
    for pattern, replacement in RULES:
        html = re.sub(pattern, replacement, html, flags=re.S)
    html = LINK_ROW_BUTTONS.sub(
        lambda m: m.group(1) + m.group(2).replace(' class="bg"', '') + m.group(3), html)
    # The blog post had no site.js; every page needs the menu script.
    if 'assets/js/site.js' not in html:
        html = html.replace(
            f'<script defer src="assets/js/analytics.js?v={VERSION}"></script>',
            f'<script defer src="assets/js/site.js?v={VERSION}"></script>\n'
            f'  <script defer src="assets/js/analytics.js?v={VERSION}"></script>')
    return html


def main():
    pages = sorted(f for f in os.listdir(REPO_ROOT)
                   if f.endswith(".html") and f != "index.html")
    changed = 0
    for name in pages:
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        updated = transform(original)
        if updated != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(updated)
            changed += 1
    print(f"{changed} of {len(pages)} pages updated")

    leftovers = []
    for name in pages:
        with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for match in re.finditer(r'style="[^"]*"', line):
                    if match.group(0).startswith('style="--'):
                        continue
                    leftovers.append((name, lineno, match.group(0)))
    if leftovers:
        print(f"\n{len(leftovers)} inline style(s) remain:")
        for row in leftovers[:20]:
            print("  %s:%d  %s" % row)
        return 1
    print("No inline styles remain outside index.html.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
