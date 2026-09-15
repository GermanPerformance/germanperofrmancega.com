#!/usr/bin/env python3
"""The service-page template: the markup tools/build_general_service_pages.py
renders its pages on.

It once also built the make-specific job pages from tools/brand_pages/;
those pages were retired on 2026-09-15 in favour of the brand hubs, and
brand_pages/ now holds the hubs' copy instead. What remains is a library:
build(page) renders one page dict, checks_list() writes the hero facts,
MARQUE_TOKENS says how each marque may name itself in them.

The chrome -- nav, phone menu, address block, footer, stylesheet and
script links -- comes from tools/page_chrome.py, never from a donor page,
so no page inherits another marque's copy or a stale footer. The breadcrumb
comes from tools/fix_breadcrumbs.py. tools/apply_redesign.py normalises the
template's markup after a generator runs.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_landing_pages import h1_markup  # noqa: E402
from fix_breadcrumbs import breadcrumb  # noqa: E402
from page_chrome import NAP_GRID, NAV, footer, scripts, stylesheets  # noqa: E402
import place  # noqa: E402
from urls import page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none">'
         '<path d="M3 8H13M9 4L13 8L9 12" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round"/></svg>')

# Accepted ways each marque names itself in the trust bar.
MARQUE_TOKENS = {
    "Porsche":       ("Porsche",),
    "Volkswagen":    ("Volkswagen", "VW"),
    "Mercedes-Benz": ("Mercedes",),
    "BMW":           ("BMW",),
    "Audi":          ("Audi",),
}



CHECK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><path d="M5 12.5 10 17.5 19 7"/></svg>')


def checks_list(marque=None):
    """The four trust facts, under the hero button where they get read.

    Replaces the old four-cell trust strip. The fourth line names the
    marque when the page has one, so a Porsche page never claims to fit
    BMW parts -- the guarantee the old strip's donor copy kept breaking.
    A page may set "marque": None to keep its brand in the eyebrow while
    the checklist says "factory" (tools/build_general_service_pages.py).
    """
    parts = "Genuine %s parts and fluids" % marque if marque else \
        "Genuine factory parts and fluids"
    items = ["4.5-star Google rating", "Top-rated CARFAX shop",
             "15+ years in business", parts]
    rows = "".join(
        '      <li>%s<span>%s</span></li>\n' % (CHECK_SVG, text) for text in items)
    return '    <ul class="checks fu">\n%s    </ul>' % rows


def cards_html(items):
    return "\n".join(
        f'    <div class="card"><span class="ci">{i:02d}</span>'
        f'<div class="ct">{title}</div><div class="cd">{body}</div></div>'
        for i, (title, body) in enumerate(items, 1))


def faq_html(items):
    return "\n".join(
        f'      <div class="fi fu"><button class="fq" onclick="toggleFaq(this)">'
        f'{q}<span class="ficon">+</span></button>'
        f'<div class="fa"><p>{a}</p></div></div>'
        for q, a in items)


def build(page):
    ch1, ch2 = page["cards_head"]
    wh1, wh2 = page["why_head"]
    fh1, fh2 = page["faq_head"]
    cta1, cta2 = page["cta"]
    points = "\n".join(f"        <li>{p}</li>" for p in page["why_points"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{page_url(page['slug'])}"/>
{stylesheets()}
</head>
<body data-page-type="service">

{NAV}
<main>
{breadcrumb(page['slug'])}
<section class="hero hero-svc"><div class="hbg"></div><div class="hgrid"></div>
  <div class="hc">
    <div class="eyebrow fu">{page['brand']} Specialists &nbsp;·&nbsp; Snellville, GA &nbsp;·&nbsp;<span class="eyebrow-highlight">4.5★ Rated</span></div>
    {h1_markup(page['service'])}
    <p class="sub fu">{page['sub']}</p>
    <div class="acts fu"><a href="tel:+16783957459" class="bp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a><a href="/#services" class="bg">All Services {ARROW}</a></div>
{checks_list(page.get('marque', page['brand']))}
  </div>
</section>


<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">What You Get</div><h2>{ch1}<br><span style="color:var(--red)">{ch2}</span></h2><p class="sd">{page['cards_sub']}</p></div>
  <div class="g3 fu">
{cards_html(page['cards'])}
  </div>
</section>

<section style="background:var(--black)">
  <div class="two fu">
    <div>
      <div class="sl">Why German Performance</div>
      <h2>{wh1}<br><span style="color:var(--red)">{wh2}</span></h2>
      <p class="sd" style="margin-bottom:0">{page['why_lead']}</p>
      <ul class="cl">
{points}
      </ul>
    </div>
    <div>
      {NAP_GRID}
    </div>
  </div>
</section>

<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">Common Questions</div><h2 class="fu">{fh1}<br><span style="color:var(--red)">{fh2}</span></h2></div>
    <div class="faq-list">
{faq_html(page['faqs'])}
    </div>
</section>

<div class="cta-band fu"><div><div class="cbt">{cta1}<br>{cta2}</div><div class="cbs">{page['cta_sub']}</div></div><a href="tel:+16783957459" class="bw"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a></div>

<section style="background:var(--black);padding:80px 60px;text-align:center">
  <div class="fu">
    <div class="sl" style="justify-content:center">Get Started</div>
    <h2 style="margin-bottom:20px">SNELLVILLE'S {page['brand'].upper()} <span style="color:var(--red)">SPECIALISTS</span></h2>
    <p class="sd" style="margin:0 auto 44px;text-align:center;max-width:480px">Serving Snellville, Loganville, Grayson, Lawrenceville, and all of Gwinnett County.</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="tel:+16783957459" class="bp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a>
      <a href="{place.attr(place.DIRECTIONS)}" target="_blank" rel="noopener" class="bg">Get Directions {ARROW}</a>
    </div>
  </div>
</section>

</main>
{footer(page['slug'])}
{scripts()}
</body>
</html>
"""
