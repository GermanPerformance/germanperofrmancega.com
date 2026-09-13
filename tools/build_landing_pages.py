#!/usr/bin/env python3
"""Build the service landing pages from tools/landing_pages.py.

One template for every category and service page. The hero leads: the H1
is "{service} in Snellville, GA" on two lines, the title mirrors it, the
sub expounds it, and the breadcrumb carries the same service with the dash
tools/build_schema.py splits on, so the Service entity's name is the
service and nothing else. Then: what is included (photo, promise, six
cards), two Google reviews, how the job goes from the call to pick-up, the
FAQ, the red band asking for the booking, and the related services. Every
section closes on the one call to action.

The chrome is not scraped from a donor page. The nav, phone menu, hero
checklist, CARFAX shield and trust badges come from tools/apply_redesign.py,
the footer columns from tools/fix_footer_links.py, the related-services
block from tools/add_related_services.py and the review cards from
tools/reviews.py, so a page written here is already in the form those
passes produce and each of them is a no-op on it. main() refuses to write
a page the redesign pass would change: template drift fails the build
instead of shipping.

The two-line H1: line 2 ("Snellville, GA") cannot break, so only line 1
can wrap. h1_em() estimates the line's width in em from glyph widths
measured on Archivo 800 at width 100 (2026-09-12), and the h1 carries it
as --h1-em; site.css sizes the h1 so that line fits the hero column at
every width, never leaving the display scale. The width-axis factors per
breakpoint live in site.css beside that rule.

JSON-LD is not written here; tools/build_schema.py adds it from the page.

Run from the repo root:  python3 tools/build_landing_pages.py
Then tools/build_schema.py and tools/build_sitemap.py.
"""

import datetime
import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import apply_redesign as redesign  # noqa: E402
from add_related_services import build_block as related_block  # noqa: E402
from fix_footer_links import build_blocks as footer_blocks  # noqa: E402
from landing_pages import (AREA_LINE, DEFAULT_CTA_SUB, DEFAULT_STEPS,  # noqa: E402
                           PAGES)
from reviews import REVIEWS  # noqa: E402

REPO_ROOT = os.path.dirname(TOOLS)
SITE = "https://germanperformancega.com"
PLACE = "Snellville, GA"
TEL = "tel:+16783957459"
MAPS = "https://maps.google.com/?q=2144+Parkwood+Rd+NW+Snellville+GA+30078"
DEFAULT_EYEBROW = "BMW · Mercedes · Audi · Porsche · VW"
MARQUE_RE = re.compile(r"BMW|Mercedes|Audi|Porsche|Volkswagen|\bVW\b")
PHOTO_WIDTHS = (420, 640, 800, 1100)
OG_FALLBACK = "og-image.jpg"
REVIEWS_LINE = "4.8 stars on CARFAX. 4.5 stars across 180+ Google reviews."

# Advance widths in em of Archivo ExtraBold, uppercase, width axis 100,
# letter-spacing -0.03em, measured in Chromium on 2026-09-12. The space is
# derived from measured strings. Anything unlisted is taken as a wide glyph.
GLYPH_EM = {
    "A": .717, "B": .715, "C": .722, "D": .725, "E": .669, "F": .611, "G": .785,
    "H": .757, "I": .299, "J": .600, "K": .740, "L": .593, "M": .884, "N": .757,
    "O": .780, "P": .668, "Q": .780, "R": .720, "S": .667, "T": .645, "U": .753,
    "V": .699, "W": .949, "X": .706, "Y": .702, "Z": .652, "&": .786, "/": .273,
    "-": .303, ",": .288, " ": .135,
}
UNKNOWN_GLYPH_EM = .80
H1_MARGIN = 1.03  # the measurement's error band, so the line never wraps

FONTS = redesign.fonts_markup()
STAR = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m12 2 3.09 '
        '6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>')
PHOTO_SIZES = "(min-width: 960px) 580px, 100vw"


# -- everything the service name decides ------------------------------------

def headline(service):
    return f"{service} in {PLACE}"


def title(service):
    return f"{headline(service)} | German Performance"


def crumb(service):
    # build_schema.service_entity() splits the crumb on " — " for the name.
    return f"{service} — {PLACE}"


def band_head(service):
    return ("BOOK YOUR", service.upper())


def h1_em(service):
    """Estimated width of the H1's first line, in em, with the safety margin."""
    line = f"{service} in".upper()
    width = sum(GLYPH_EM.get(ch, UNKNOWN_GLYPH_EM) for ch in line)
    return round(width * H1_MARGIN, 2)


def h1_markup(service):
    place = PLACE.replace(" ", "&nbsp;")
    return (f'<h1 class="fu" style="--h1-em:{h1_em(service):.2f}">{service} in<br>'
            f'<span class="accent">{place}</span></h1>')


def section_cta():
    return f'<div class="acts section-cta fu"><a href="{TEL}" class="bp">{redesign.CTA}</a></div>'


def two_line(h2_1, h2_2, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return f'<h2{attr}>{h2_1}<br><span class="accent">{h2_2}</span></h2>'


# -- head ---------------------------------------------------------------------

def og_image(page):
    photo = page.get("photo")
    if photo:
        return f'{photo["base"]}-{PHOTO_WIDTHS[-1]}.jpg'
    return OG_FALLBACK


def social_tags(page):
    t, d, url = title(page["service"]), page["desc"], f'{SITE}/{page["slug"]}'
    image = f"{SITE}/{og_image(page)}"
    return "\n".join((
        f'<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{image}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{image}">',
    ))


# -- sections -----------------------------------------------------------------

def hero(page):
    return f'''<section class="hero hero-svc"><div class="hbg"></div>
  <div class="hc">
    <div class="eyebrow fu"><span>{page.get("eyebrow", DEFAULT_EYEBROW)}</span></div>
    {h1_markup(page["service"])}
    <p class="sub fu">{page["sub"]}</p>
    <div class="acts fu"><a href="{TEL}" class="bp">{redesign.CTA}</a></div>
    <div class="hero-proof">
    {redesign.hero_seal_markup()}
{redesign.checks_list()}
    </div>
  </div>
</section>'''


def photo_picture(photo):
    base = photo["base"]
    srcset = lambda ext: ", ".join(f"{base}-{w}.{ext} {w}w" for w in PHOTO_WIDTHS)  # noqa: E731
    return (f'<picture><source type="image/webp" sizes="{PHOTO_SIZES}" srcset="{srcset("webp")}">'
            f'<source type="image/jpeg" sizes="{PHOTO_SIZES}" srcset="{srcset("jpg")}">'
            f'<img src="{base}-640.jpg" alt="{photo["alt"]}" width="{photo["width"]}" '
            f'height="{photo["height"]}" loading="lazy" decoding="async"></picture>')


def included(page):
    h1, h2 = page.get("cards_head", ("WHAT'S INCLUDED", f"IN {page['service'].upper()}"))
    promise = "\n".join(f"        <li>{p}</li>" for p in page["promise"])
    cards = "\n".join(
        f'    <div class="card"><span class="ci">{i:02d}</span><h3 class="ct">{t}</h3>'
        f'<div class="cd">{d}</div></div>'
        for i, (t, d) in enumerate(page["cards"], 1))
    return f'''<section>
  <div class="sh fu"><div class="sl">What's included</div>{two_line(h1, h2)}</div>
  <div class="two fu">
    <figure class="svc-figure">{photo_picture(page["photo"])}</figure>
    <div>
      <p class="sd">{page["intro"]}</p>
      <ul class="cl">
{promise}
      </ul>
    </div>
  </div>
  <div class="g3 fu">
{cards}
  </div>
  {section_cta()}
</section>'''


def review_card(key):
    r = REVIEWS[key]
    avatar = r["avatar"]
    if "image" in avatar:
        head = (f'<img class="gr-avatar" src="{avatar["image"]}" alt="" width="{avatar["width"]}" '
                f'height="{avatar["height"]}" loading="lazy" decoding="async">')
    else:
        head = f'<span class="gr-avatar gr-avatar--{avatar["key"]}" aria-hidden="true">{avatar["letter"]}</span>'
    price = '\n      <p class="gr-price">Great price</p>' if r["price"] else ""
    photos = "".join(
        f'\n        <img src="{p["src"]}" alt="{p["alt"]}" width="{p["width"]}" height="{p["height"]}" '
        'loading="lazy" decoding="async">' for p in r["photos"])
    photos = f'\n      <div class="gr-photos">{photos}\n      </div>' if photos else ""
    return f'''    <article class="gr-card" aria-labelledby="review-{key}-name">
      <header class="gr-profile">
        {head}
        <div class="gr-person">
          <h3 class="gr-name" id="review-{key}-name">{r["name"]}</h3>
          <p class="gr-meta">{r["meta"]}</p>
        </div>
      </header>
      <div class="gr-rating" role="img" aria-label="5 out of 5 stars">{STAR * 5}</div>{price}
      <blockquote class="gr-quote"><p>{r["quote"]}</p></blockquote>{photos}
    </article>'''


def reviews_section(page):
    cards = "\n".join(review_card(k) for k in page["reviews"])
    return f'''<section>
  <div class="sh fu"><div class="sl">Reviews</div>{two_line("WHAT PEOPLE", "ARE SAYING")}<p class="sd">{REVIEWS_LINE}</p></div>
  <div class="gr-wall gr-pair fu" aria-label="Customer reviews from Google">
{cards}
  </div>
  {section_cta()}
</section>'''


def steps_section(page):
    steps = page.get("steps", DEFAULT_STEPS)
    items = "\n".join(
        f'    <li><span class="step-n" aria-hidden="true">{i:02d}</span><h3 class="step-t">{t}</h3>'
        f'<p class="step-d">{d}</p></li>'
        for i, (t, d) in enumerate(steps, 1))
    return f'''<section>
  <div class="sh fu"><div class="sl">How it works</div>{two_line("FROM YOUR CALL", "TO PICK-UP")}</div>
  <ol class="steps steps-{len(steps)} fu">
{items}
  </ol>
  <p class="sd fu note">{AREA_LINE}</p>
  {section_cta()}
</section>'''


def faq(page):
    items = "\n".join(
        f'      <details class="fi fu" name="faq"><summary class="fq">{q}'
        f'<span class="ficon" aria-hidden="true"></span></summary>'
        f'<div class="fa"><p>{a}</p></div></details>'
        for q, a in page["faqs"])
    return f'''<section>
  <div class="sh fu"><div class="sl">Common Questions</div>{two_line(page["service"].upper(), "FAQ", "fu")}</div>
    <div class="faq-list">
{items}
    </div>
  {section_cta()}
</section>'''


def band(page):
    l1, l2 = band_head(page["service"])
    return (f'<div class="cta-band fu"><div><div class="cbt">{l1}<br>{l2}</div>'
            f'<div class="cbs">{page.get("cta_sub", DEFAULT_CTA_SUB)}</div></div>'
            f'<div class="cta-col"><a href="{TEL}" class="bw">{redesign.CTA}</a>'
            f'{redesign.ASSURE}</div></div>')


def footer(slug):
    services_col, flinks = footer_blocks(slug)
    year = datetime.date.today().year
    return f'''<footer>
  <div class="ft">
    <div><div class="fb">{redesign.LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div>{redesign.footer_seal_markup()}</div>
    <div class="fc"><div class="fct">Contact</div><a href="{TEL}">(678) 395-7459</a><p>2144 Parkwood Rd NW</p><p>Snellville, GA 30078</p><a href="{MAPS}" target="_blank" rel="noopener">Get directions</a><p>Mon–Fri: 9:30 AM–6 PM</p></div>
    {services_col}
    <div class="fc"><div class="fct">Navigate</div><a href="index.html">Home</a><a href="about.html">About</a><a href="index.html#reviews">Reviews</a><a href="index.html#faq">FAQ</a><a href="contact.html">Contact</a><a href="dealer-vs-independent-german-car-repair.html">Dealer vs. Independent</a></div>
  </div>
  {flinks}
  <div class="fcopy">© {year} German Performance — Snellville, GA 30078{redesign.PRIVACY_LINK}</div>
</footer>'''


def build(page):
    v = redesign.VERSION
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title(page["service"])}</title>
<meta name="description" content="{page["desc"]}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{SITE}/{page["slug"]}"/>
{social_tags(page)}
{FONTS}
<link rel="stylesheet" href="assets/css/tokens.css?v={v}">
<link rel="stylesheet" href="assets/css/werkstatt.css?v={v}">
<link rel="stylesheet" href="assets/css/site.css?v={v}">
</head>
<body data-page-type="service">
{redesign.NAV}
<main>
<div class="breadcrumb"><a href="index.html">Home</a><span>/</span><span class="crumb-here">{crumb(page["service"])}</span></div>
{hero(page)}

{included(page)}

{reviews_section(page)}

{steps_section(page)}

{faq(page)}

{band(page)}

{related_block(page["slug"])}
</main>
{footer(page["slug"])}
<script defer src="assets/js/site.js?v={v}"></script>
<script defer src="assets/js/analytics.js?v={v}"></script>
</body>
</html>
'''


def hero_checks(markup):
    start = markup.index('<ul class="checks')
    return markup[start:markup.index("</ul>", start)]


def verify(page, markup):
    """Raise if the page is not in the form the site's passes leave it in."""
    if redesign.transform(markup) != markup:
        raise SystemExit(f"{page['slug']}: apply_redesign would change this page; "
                         "the template has drifted from its rules")
    checks = hero_checks(markup)
    if "Genuine factory parts and fluids" not in checks or MARQUE_RE.search(checks):
        raise SystemExit(f"{page['slug']}: hero checklist names a marque")


def main():
    for page in PAGES:
        markup = build(page)
        verify(page, markup)
        with open(os.path.join(REPO_ROOT, page["slug"]), "w", encoding="utf-8") as fh:
            fh.write(markup)
        words = len(re.sub(r"<[^>]+>", " ", markup).split())
        print(f"  wrote {page['slug']:52s} ~{words} words  h1 line {h1_em(page['service'])}em")
    print(f"\n{len(PAGES)} landing pages built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
