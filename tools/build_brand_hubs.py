#!/usr/bin/env python3
"""Build one repair hub per marque from tools/brand_pages/<make>.py.

The hubs are the site's money pages after the homepage: "BMW Repair in
Snellville, GA" is what someone searching "bmw repair snellville" should
land on, and it has to answer them. Each hub carries what usually brings
that marque in, every service the shop performs on it (the copy of the
job pages retired on 2026-09-15, consolidated), the marque's known weak
points, two of the shop's real Google reviews, six questions, the seven
make-agnostic service pages, the guides written for that marque, the
other four makes and the shop's credentials.

Copy structure is Before-After-Bridge: the symptom that made someone
search and the fear behind it (paying for parts until the noise stops);
knowing what is wrong and what it costs before committing; marque-specific
diagnosis on the factory software from a shop that only works on German
cars. The only conversion is a phone call, so every call to action asks
the owner to describe the symptom, not to schedule.

The page is written in the form the site's passes leave it in, on the
landing framework's helpers (hero, reviews, FAQ, band), and verify()
refuses to write a page apply_redesign.transform() would change. Every
failure mode named in the copy is a documented characteristic of the
marque; nothing about pricing, turnaround or certification is invented.

Run from the repo root:  python3 tools/build_brand_hubs.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_redesign as redesign  # noqa: E402
import build_landing_pages as blp  # noqa: E402
from brand_pages import HUBS  # noqa: E402
from build_service_pages import MARQUE_TOKENS  # noqa: E402
from fix_breadcrumbs import breadcrumb  # noqa: E402
from page_chrome import NAV, neutral_footer, scripts, stylesheets  # noqa: E402
from posts import GUIDES_PAGE, READING, SUMMARY, guides_for  # noqa: E402
from service_catalog import GENERIC_GROUP, GROUPS, HOME, full_label, hubs  # noqa: E402
from urls import href_for, page_url  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The make-agnostic column, led by the homepage as the general repair page
# under the profile's category name. From the catalog, so a page added
# there reaches the hubs on the next build.
UNIVERSAL = ((HOME, "Auto Repair"),) + dict(GROUPS)[GENERIC_GROUP]
SLUGS = tuple(h["slug"] for h in HUBS)
OTHER_MAKES_LINE = (
    "{brand} is one of the five makes we work on. German Performance is an independent "
    '<a href="{home}">German auto repair shop in Snellville, GA</a> for BMW, Mercedes-Benz, '
    "Audi, Porsche and Volkswagen, and nothing else.")


def article(noun, upper=False):
    """"an Audi", "a BMW": the indefinite article the marque takes."""
    a = "an" if noun[0].upper() in "AEIOU" else "a"
    return a.upper() if upper else a


def page_for(hub):
    """The landing helpers read a page dict keyed on its service name."""
    return {**hub, "service": full_label(hub["slug"])}


# -- sections -----------------------------------------------------------------

def cards(items):
    return "\n".join(
        f'    <div class="card"><span class="ci">{i:02d}</span><h3 class="ct">{t}</h3>'
        f'<div class="cd">{d}</div></div>'
        for i, (t, d) in enumerate(items, 1))


def before_section(hub):
    return f'''<section>
  <div class="sh fu"><div class="sl">Why people call us</div>{blp.two_line("WHAT USUALLY BRINGS", f"{article(hub['possessive'], upper=True)} {hub['possessive'].upper()} IN")}<p class="sd">Almost everyone who calls is somewhere in one of these three situations.</p></div>
  <div class="g3 fu">
{cards(hub["before"])}
  </div>
</section>'''


def service_card(i, title, body, general):
    more = (f' <a href="{href_for(general)}">{full_label(general)} for every German make &rarr;</a>'
            if general else "")
    return (f'    <div class="card"><span class="ci">{i:02d}</span><h3 class="ct">{title}</h3>'
            f'<div class="cd">{body}{more}</div></div>')


def grid_class(count):
    """Full rows only: three across for six cards, two across for four. An
    orphan card in a last row is the asymmetry the owner asked us to avoid."""
    return "g3" if count % 3 == 0 else "g2"


def services_section(hub):
    items = "\n".join(service_card(i, *row) for i, row in enumerate(hub["services"], 1))
    return f'''<section>
  <div class="sh fu"><div class="sl">{hub["brand"]} services</div>{blp.two_line("WHAT WE DO", f"ON YOUR {hub['possessive'].upper()}")}<p class="sd">Every job on {article(hub["possessive"])} {hub["possessive"]} starts on {hub["tool"]}, the factory software, and ends with a written 12-month, 12,000-mile warranty.</p></div>
  <div class="{grid_class(len(hub["services"]))} fu">
{items}
  </div>
  {blp.section_cta()}
</section>'''


def known_section(hub):
    return f'''<section>
  <div class="sh fu"><div class="sl">Known weak points</div>{blp.two_line("WHAT WE LOOK FOR", f"ON {article(hub['possessive'], upper=True)} {hub['possessive'].upper()}")}<p class="sd">Every marque has its own failure patterns. Knowing them is the difference between diagnosing a car and experimenting on it.</p></div>
  <div class="g3 fu">
{cards(hub["known"])}
  </div>
</section>'''


def universal_section(hub):
    universal = "\n".join(
        f'    <a href="{href_for(h)}" class="rel-card"><span class="rel-name">{n}</span>'
        f'<span class="rel-go">&rarr;</span></a>' for h, n in UNIVERSAL)
    return f'''<section>
  <div class="sh fu"><div class="sl">Any German make</div>{blp.two_line("THE SERVICES", "WE PERFORM")}<p class="sd"><strong>Models we service:</strong> {hub["models"]}</p></div>
  <div class="rel-grid fu">
{universal}
  </div>
</section>'''


def guides_section(hub):
    slugs = guides_for(hub["slug"])
    if not slugs:
        return ""
    items = "\n".join(
        f'    <a href="{href_for(s)}" class="card"><span class="ci">{i:02d}</span>'
        f'<h3 class="ct">{READING[s]}</h3><div class="cd">{SUMMARY[s]}</div></a>'
        for i, s in enumerate(slugs, 1))
    return f'''<section>
  <div class="sh fu"><div class="sl">{hub["brand"]} guides</div>{blp.two_line("FROM THE", "TECHNICIANS")}<p class="sd">What we have learned on the {hub["possessive"]}s that come through the shop, written down: what to maintain, how we diagnose a symptom, what moves a bill, and jobs from our own bays. <a href="{href_for(GUIDES_PAGE)}">All repair guides &rarr;</a></p></div>
  <div class="{grid_class(len(slugs))} fu">
{items}
  </div>
</section>

'''


def other_makes_section(hub):
    others = "".join(
        f'<a href="{href_for(h)}">{label}</a>' for h, label in hubs() if h != hub["slug"])
    return f'''<section>
  <div class="sh fu"><div class="sl">Other German makes</div>{blp.two_line("WE ALSO", "SPECIALISE IN")}<p class="sd">{OTHER_MAKES_LINE.format(brand=hub["brand"], home=href_for(HOME))}</p></div>
  <div class="flinks fu">{others}<a href="{href_for(GUIDES_PAGE)}">Repair Guides</a></div>
</section>'''


def closing_section(hub):
    return f'''<section>
  <div class="sh fu"><div class="sl">Get Started</div>{blp.two_line(f"SNELLVILLE'S {hub['possessive'].upper()}", "SPECIALISTS")}<p class="sd">{hub["closing"]}</p></div>
  {blp.section_cta()}
</section>'''


# -- page ---------------------------------------------------------------------

def build(hub):
    page = page_for(hub)
    v = redesign.VERSION
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{blp.title(page["service"])}</title>
<meta name="description" content="{hub["desc"]}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{page_url(hub["slug"])}"/>
{stylesheets()}
</head>
<body data-page-type="hub">
{NAV}
<main>
{breadcrumb(hub["slug"])}
{blp.hero(page, marque=hub["possessive"])}

{before_section(hub)}

{services_section(hub)}

{known_section(hub)}

{blp.reviews_section(page)}

{blp.faq(page)}

{blp.band(page)}

{universal_section(hub)}

{guides_section(hub)}{other_makes_section(hub)}

{closing_section(hub)}
</main>
{neutral_footer()}
<script defer src="assets/js/site.js?v={v}"></script>
<script defer src="assets/js/analytics.js?v={v}"></script>
</body>
</html>
'''


def verify(hub, markup):
    """Raise if the page is not in the form the site's passes leave it in,
    or if its hero checklist fails to name the marque -- copying a BMW
    donor is how "BMW-Approved Parts" once shipped on the Porsche hub."""
    if redesign.transform(markup) != markup:
        raise SystemExit(f"{hub['slug']}: apply_redesign would change this page; "
                         "the template has drifted from its rules")
    checks = blp.hero_checks(markup)
    if not any(token in checks for token in MARQUE_TOKENS[hub["brand"]]):
        raise SystemExit(f"{hub['slug']}: hero checklist does not name {hub['brand']}")
    if len(hub["desc"]) > 160 or len(blp.title(page_for(hub)["service"])) > 60:
        raise SystemExit(f"{hub['slug']}: title or description too long for a result")


def main():
    for hub in HUBS:
        markup = build(hub)
        verify(hub, markup)
        path = os.path.join(REPO_ROOT, hub["slug"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(markup)
        words = len(re.sub(r"<[^>]+>", " ", markup[markup.index("<main>"):]).split())
        print(f"  wrote {hub['slug']:40s} ~{words} words, {len(hub['services'])} services, "
              f"{len(hub['faqs'])} FAQs")
    print(f"\n{len(HUBS)} brand hubs built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
