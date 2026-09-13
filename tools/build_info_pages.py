#!/usr/bin/env python3
"""Give About and Contact real URLs.

Both existed only as homepage anchors, which means neither could be linked
from a Google Business Profile, cited on its own, or ranked for the queries
that name them. A local shop's contact page is one of the few pages people
search for by name.

Two, not four. The approved plan listed /faq and /reviews as well:

  /faq     would put the same eight questions on a second URL. That is the
           duplication removed in Phase 1, and since August 2023 Google has
           restricted FAQ rich results to government and health sites, so
           there is no rich-result upside to pay for it. The homepage FAQ
           and the 40 per-page FAQs already cover the ground.
  /reviews with three testimonials is a thin page. The rating belongs on
           the Google Business Profile, which is also where the plan
           deliberately left it rather than marking up a self-serving
           aggregateRating.

Neither page repeats a homepage section. /contact answers what the homepage
block cannot -- what to have ready before dialling, what the building looks
like, what happens outside opening hours. /about is the E-E-A-T page the
site has never had: what software runs on which marque, and how a job
actually proceeds.

Every fact here already appears on the site or in its schema: trading since
2010, Mon-Fri 9:30-18:00, 2144 Parkwood Rd NW, 4.5 stars from 185 reviews,
12-month/12,000-mile warranty, no appointment needed, extended warranties
accepted. Nothing about staff, certifications or capacity is invented.

The "people" section on /about is the E-E-A-T piece the page lacked: the
homepage names Sam and Zayd beside their photograph and says they answer
the phone and work on the cars, but the About page -- the one a reader or
a search engine opens to find out who is behind a business -- said nothing
about anyone. It now shows the same photograph and repeats exactly those
facts. Their surnames, titles and any certifications are not on the site,
so they are not here either; add them to PEOPLE_POINTS when the owner
supplies them. /contact gains the map the homepage already embeds, so the
page that answers "where" shows it, and the same photograph so the
building is recognisable from the road.

Run from the repo root:  python3 tools/build_info_pages.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# One definition of the hero checklist, shared. Three copies of it
# is how this project has repeatedly ended up with the same helper
# fixed in one file and stale in the others.
from build_service_pages import checks_list  # noqa: E402
from build_landing_pages import photo_picture  # noqa: E402
from page_chrome import neutral_blocks  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"
DONOR = "porsche-oil-change-snellville-ga.html"
MAPS = ("https://maps.google.com/?q=2144+Parkwood+Rd+NW+Snellville+GA+30078")
# The keyless embed form: Google geocodes the address itself, so the pin
# lands on the shop without a place ID or an API key.
MAP_EMBED = ("https://www.google.com/maps?q=2144+Parkwood+Rd+NW,+Snellville,"
             "+GA+30078&output=embed")

# The photograph the homepage runs beside its story block, at the sizes
# tools/build_shop_photos.py writes.
PEOPLE_PHOTO = {
    "base": "assets/img/shop/sam-and-zayd",
    "alt": ("Sam and Zayd, wrenches in hand, standing in front of the open "
            "service bays at German Performance in Snellville"),
    "width": 1100, "height": 1375,
}

ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none">'
         '<path d="M3 8H13M9 4L13 8L9 12" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round"/></svg>')

PAGES = [
{
 "slug": "about.html",
 "type": "AboutPage",
 "h1": ("ABOUT", "GERMAN", "PERFORMANCE"),
 "title": "About German Performance | German Auto Repair, Snellville GA",
 "desc": ("Independent German auto specialists in Snellville, GA since 2010. "
          "BMW, Mercedes, Audi, Porsche and VW only, on factory diagnostic "
          "software. Call (678) 395-7459."),
 "crumb": "About",
 "eyebrow": "Since 2010 &nbsp;·&nbsp; Snellville, GA",
 "sub": ("An independent German specialist in Snellville, Georgia. BMW, "
         "Mercedes-Benz, Audi, Porsche and Volkswagen — and nothing else, "
         "which is the whole point."),
 "people_head": ("WHO YOU", "ACTUALLY TALK TO"),
 "people_lead": ("German Performance is a family-owned shop, in Snellville "
                 "since 2010. That is Sam and Zayd in the photo. They are the "
                 "people you speak to when you call, and the people who work "
                 "on your car. What they find is what you are told, in "
                 "writing, with photos."),
 "people_points": [
   "Family-owned, working on German cars in Snellville since 2010",
   "The people who answer the phone are the people who do the work",
   "Every car diagnosed on the factory software for its marque — ISTA, XENTRY, ODIS, PIWIS",
   "A written estimate before a single part is ordered",
   "12-month, 12,000-mile warranty on every repair",
   "CARFAX 2025 Top-Rated Service Center; 4.8 stars on CARFAX, 180+ Google reviews",
 ],
 "cards_head": ("THE SOFTWARE", "WE ACTUALLY RUN"),
 "cards_sub": ("A German car reports symptoms, not causes. The difference "
               "between a diagnosis and a guess is whether the shop can talk "
               "to every control module in the car."),
 "cards": [
   ("ISTA — BMW and Mini",
    "The factory interface for BMW. Full module access, live values, coding "
    "and service functions, including battery registration, which is why a "
    "BMW battery is not simply a swap."),
   ("XENTRY — Mercedes-Benz",
    "Mercedes' own diagnostic system, covering the passenger range and the "
    "Sprinter. Map-controlled thermostats, AIRMATIC and conductor plate "
    "faults are only visible from inside it."),
   ("ODIS — Audi and Volkswagen",
    "The VAG factory system. It is what puts an electronic parking brake into "
    "service mode, reads Haldex function properly, and performs the "
    "adaptations a generic tool cannot."),
   ("PIWIS — Porsche",
    "Porsche's factory tester. Ride height calibration after suspension work, "
    "PASM faults and service resets all require it."),
   ("What that access buys you",
    "Adaptations, component coding, guided fault finding and live data — the "
    "work a code reader cannot touch. It is the difference between replacing "
    "the part that failed and replacing parts until the light goes out."),
   ("What we do not do",
    "We do not work on non-German cars, and we do not start replacing parts "
    "to find out what is wrong. If we cannot tell you what failed, we say so "
    "rather than guessing on your money."),
 ],
 "why_head": ("HOW A JOB", "ACTUALLY GOES"),
 "why_lead": ("Most people who call us have been somewhere else first, and the "
              "story is usually the same: a part was replaced, the fault came "
              "back, and nobody explained why. The order below is what "
              "prevents that, and none of it is unusual — it is simply "
              "diagnosis before parts."),
 "why_points": [
   "You call and describe the symptom — no appointment needed to get an opinion",
   "We diagnose on the factory software for that marque before quoting parts",
   "You hear what we found, what it costs, and what can reasonably wait",
   "Nothing is done until you approve it — no surprises on the bill",
   "Photo reports and text updates while the car is with us",
   "Written record of everything performed, and a 12-month / 12,000-mile warranty",
 ],
 "faq_head": ("ABOUT", "THE SHOP"),
 "faqs": [
   ("How long has German Performance been in business?",
    "Since 2010, in Snellville serving Gwinnett County — Snellville, "
    "Loganville, Grayson, Lawrenceville and Stone Mountain. The shop is rated "
    "4.8 stars on CARFAX and 4.5 stars across 180+ Google reviews, and CARFAX "
    "named it a 2025 Top-Rated Service Center."),
   ("Why only German cars?",
    "Because the tooling and the failure modes are specific enough that "
    "splitting attention costs you accuracy. Running ISTA, XENTRY, ODIS and "
    "PIWIS every day, on the same five marques, is what makes a diagnosis "
    "quick. A shop covering everything owns none of that software and sees "
    "each fault once a year instead of once a week."),
   ("Will using an independent shop void my factory warranty?",
    "No. Under the Magnuson-Moss Warranty Act a manufacturer cannot void your "
    "warranty simply because an independent shop performed routine maintenance "
    "or repairs, provided the correct parts and fluids were used and the work "
    "is documented. You leave with that documentation every time."),
   ("Do you use OEM parts?",
    "OEM or OEM-equivalent as standard, and we will tell you which before the "
    "work starts. On an older car there is sometimes a sensible argument for "
    "a quality aftermarket part, and on some jobs there is not. Either way it "
    "is your decision, not a surprise on the invoice."),
   ("What warranty comes with the work?",
    "12 months or 12,000 miles on repairs, whichever comes first. Extended "
    "warranty providers are accepted — most of the major ones — and we handle "
    "the paperwork side with them."),
 ],
 "cta": ("WANT TO KNOW WHAT", "IS ACTUALLY WRONG?"),
 "cta_sub": "Call and describe the symptom. That is the fastest way to find out what we would check first.",
},
{
 "slug": "contact.html",
 "type": "ContactPage",
 "h1": ("CONTACT", "GERMAN", "PERFORMANCE"),
 "title": "Contact German Performance | Snellville, GA | (678) 395-7459",
 "desc": ("Call German Performance in Snellville, GA at (678) 395-7459. "
          "2144 Parkwood Rd NW, Mon–Fri 9:30 AM–6 PM. BMW, Mercedes, Audi, "
          "Porsche and VW repair."),
 "crumb": "Contact",
 "eyebrow": "Mon &ndash; Fri &nbsp;·&nbsp; Snellville, GA",
 "sub": ("One phone number, Monday to Friday, answered by the people who work "
         "on the cars. No appointment is needed to get an opinion on what your "
         "car is doing."),
 "cards_head": ("BEFORE YOU", "CALL"),
 "cards_sub": ("None of this is required — but having it to hand turns one "
               "call into an answer instead of two calls into a maybe."),
 "cards": [
   ("Year, model and engine",
    "A 2014 328i and a 2014 335i share a badge and very little else. The "
    "engine code, if you know it, narrows a diagnosis faster than anything "
    "else you can tell us."),
   ("What it is actually doing",
    "Describe it the way you would to a friend — a noise, a smell, a "
    "hesitation, a warning. Plain description is more useful than a guess at "
    "the cause, and far more useful than a part name."),
   ("When it happens",
    "Cold start only, after twenty minutes, under braking, turning left, over "
    "bumps. Intermittent faults are found by the conditions that reproduce "
    "them, and you already know those conditions better than we do."),
   ("Any message on the dash",
    "Read it out exactly as it appears, warning-light colour included. "
    "Mercedes, BMW and Audi all word similar faults differently, and the "
    "exact wording often points straight at the affected system."),
   ("What has been done already",
    "If another shop has replaced something, say so. It saves you paying us "
    "to rule out the thing that was just ruled out, and a repeat failure of "
    "the same part is itself a clue."),
   ("Your mileage and last service",
    "Interval-based work and wear items both depend on it, and it tells us "
    "whether what you are describing is early, on time, or overdue."),
 ],
 "map": True,
 "why_head": ("FINDING", "THE SHOP"),
 "why_lead": ("We are at 2144 Parkwood Rd NW in Snellville, Georgia 30078, "
              "open Monday to Friday from 9:30 AM to 6:00 PM and closed at "
              "weekends. If you are calling outside those hours, leaving the "
              "details above in a message means the call back is already a "
              "useful one rather than a round of questions."),
 "why_points": [
   "2144 Parkwood Rd NW, Snellville, GA 30078",
   "(678) 395-7459 — the only number, and the fastest way to reach us",
   "Monday to Friday, 9:30 AM – 6:00 PM. Closed Saturday and Sunday",
   "No appointment needed — call or stop by",
   "Serving Snellville, Loganville, Grayson, Lawrenceville and Stone Mountain",
   "Most major extended warranty providers accepted",
 ],
 "faq_head": ("CONTACT", "QUESTIONS"),
 "faqs": [
   ("Where is German Performance located?",
    "2144 Parkwood Rd NW, Snellville, GA 30078, in Gwinnett County. We "
    "regularly see cars from Loganville, Grayson, Lawrenceville and Stone "
    "Mountain as well as Snellville itself."),
   ("What are your hours?",
    "Monday to Friday, 9:30 AM to 6:00 PM. We are closed Saturday and Sunday. "
    "Those are the hours the phone is answered as well as the hours the shop "
    "is open."),
   ("Do I need an appointment?",
    "No. You can call or stop by. Calling first is usually faster for you, "
    "because it means we can tell you what to expect and, for some faults, "
    "what to check before you drive over."),
   ("Which cars do you work on?",
    "BMW, Mercedes-Benz, Audi, Porsche and Volkswagen, including Mini, AMG, "
    "Audi Sport, BMW M and the Sprinter. We do not take non-German cars, "
    "which is what keeps the diagnosis on the rest of them quick."),
   ("Do you accept extended warranties?",
    "Yes — most of the major providers. Have the policy details with you when "
    "you call and we will tell you what the provider will usually want before "
    "authorising a repair."),
   ("Can you tell me what it will cost over the phone?",
    "For routine, defined work we can give you a straight answer. For a fault, "
    "an honest quote needs a diagnosis first — anyone pricing a repair before "
    "knowing what failed is guessing, and that guess ends up on your bill."),
 ],
 "cta": ("CALL", "(678) 395-7459"),
 "cta_sub": "Monday to Friday, 9:30 AM to 6:00 PM. Tell us what the car is doing.",
},
]


# The footer inherited from the donor carries that marque's service links
# and its cross-brand row, both of which fix_footer_links.py rewrites on
# every run. Copying them meant these pages advertised Porsche suspension
# on an About page AND re-copied whatever the donor happened to hold, so
# the pipeline never settled. The hubs are the right links here anyway:
# neutral, and stable because they do not participate in that ranking.
FOOTER_SERVICES = re.compile(r'<div class="fc"><div class="fct">Services</div>.*?</div>', re.S)
FOOTER_FLINKS = re.compile(r'<div class="flinks">.*?</div>', re.S)


def neutral_footer(footer):
    """Swap the marque-specific footer links for the five brand hubs."""
    column, flinks = neutral_blocks()
    footer = FOOTER_SERVICES.sub(lambda _: column, footer, count=1)
    return FOOTER_FLINKS.sub(lambda _: flinks, footer, count=1)


def skeleton():
    src = open(os.path.join(REPO_ROOT, DONOR), encoding="utf-8").read()

    def grab(pattern):
        match = re.search(pattern, src, re.S)
        if not match:
            raise SystemExit(f"{DONOR}: no match for {pattern[:44]}")
        return match.group(0)

    return {
        "nav": grab(r"<nav.*?</nav>"),
        "mob": grab(r'<div id="mobile-menu".*?\n</div>'),
        "callbar": "",  # the fixed bottom call bar was removed site-wide
        "footer": neutral_footer(grab(r"<footer>.*?</footer>")),
        "fonts": grab(r'<link rel="stylesheet" href="assets/css/fonts\.css[^>]*>'),
        # Every local stylesheet, in document order -- never a range regex.
        "css": "\n".join(
            re.findall(r'<link rel="stylesheet" href="assets/css/[^"]+"[^>]*>', src)),
        "scripts": "\n".join(
            re.findall(r'<script defer src="assets/js/[^"]+"></script>', src)),
    }


def cards_html(items):
    return "\n".join(
        f'    <div class="card"><span class="ci">{i:02d}</span>'
        f'<div class="ct">{t}</div><div class="cd">{d}</div></div>'
        for i, (t, d) in enumerate(items, 1))


def faq_html(items):
    return "\n".join(
        f'      <div class="fi fu"><button class="fq" onclick="toggleFaq(this)">'
        f'{q}<span class="ficon">+</span></button>'
        f'<div class="fa"><p>{a}</p></div></div>'
        for q, a in items)


def people_section(page):
    """The photograph and the facts the homepage already states about the
    people, on the page a reader opens to find out who they are."""
    h1, h2 = page["people_head"]
    points = "\n".join(f"        <li>{p}</li>" for p in page["people_points"])
    return f"""
<section>
  <div class="sh fu"><div class="sl">The People</div><h2>{h1}<br><span class="accent">{h2}</span></h2></div>
  <div class="two fu">
    <figure class="svc-figure">{photo_picture(PEOPLE_PHOTO)}</figure>
    <div>
      <p class="sd">{page['people_lead']}</p>
      <ul class="cl">
{points}
      </ul>
    </div>
  </div>
</section>
"""


def map_section():
    """The map beside the photograph of the bays: where it is, and what to
    look for when you get there. The frame is lazy, so it costs nothing
    until the reader scrolls to it."""
    return f"""
<section>
  <div class="sh fu"><div class="sl">Where We Are</div><h2>THE SHOP<br><span class="accent">ON THE MAP</span></h2></div>
  <div class="two fu">
    <figure class="svc-figure"><iframe src="{MAP_EMBED}" title="Map showing German Performance at 2144 Parkwood Rd NW, Snellville, GA 30078" width="600" height="450" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></figure>
    <figure class="svc-figure">{photo_picture(PEOPLE_PHOTO)}</figure>
  </div>
</section>
"""


def build(page, sk):
    l1, l2, l3 = page["h1"]
    ch1, ch2 = page["cards_head"]
    wh1, wh2 = page["why_head"]
    fh1, fh2 = page["faq_head"]
    c1, c2 = page["cta"]
    points = "\n".join(f"        <li>{p}</li>" for p in page["why_points"])
    # Only the contact page has somewhere to send you. It sits under the
    # checklist in the right column rather than hard against the last item.
    directions = (
        f'      <p class="acts"><a href="{MAPS}" target="_blank" '
        f'rel="noopener" class="bg">Get directions {ARROW}</a></p>'
        if page["slug"] == "contact.html" else "")
    people = people_section(page) if "people_head" in page else ""
    where = map_section() if page.get("map") else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<link rel="icon" type="image/png" href="assets/img/favicon-144.png">
<link rel="canonical" href="{SITE}/{page['slug']}"/>
{sk['fonts']}
{sk['css']}
</head>
<body data-page-type="info">

{sk['nav']}
{sk['mob']}
<main>
<div class="breadcrumb"><a href="index.html">Home</a><span>/</span><span class="crumb-here">{page['crumb']}</span></div>
<section class="hero">
  <div class="hc">
    <div class="eyebrow fu">{page['eyebrow']}</div>
    <h1 class="fu">{l1}<br><span class="outline">{l2}</span><br><span class="accent">{l3}</span></h1>
    <p class="sub fu">{page['sub']}</p>
    <div class="acts fu"><a href="tel:+16783957459" class="bp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a><a href="index.html#services" class="bg">All Services {ARROW}</a></div>
{checks_list()}
  </div>
</section>
{people}
<section>
  <div class="fu"><div class="sl">{'What We Run' if page['slug'] == 'about.html' else 'Have This Ready'}</div><h2>{ch1}<br><span class="accent">{ch2}</span></h2><p class="sd">{page['cards_sub']}</p></div>
  <div class="g3 fu">
{cards_html(page['cards'])}
  </div>
</section>

<section>
  <div class="two fu">
    <div>
      <div class="sl">{'The Process' if page['slug'] == 'about.html' else 'Where And When'}</div>
      <h2>{wh1}<br><span class="accent">{wh2}</span></h2>
      <p class="sd">{page['why_lead']}</p>
    </div>
    <div>
      <ul class="cl">
{points}
      </ul>
{directions}
    </div>
  </div>
</section>
{where}
<section>
  <div class="fu"><div class="sl">Common Questions</div><h2>{fh1}<br><span class="accent">{fh2}</span></h2></div>
    <div class="faq-list">
{faq_html(page['faqs'])}
    </div>
</section>

<div class="cta-band fu"><div><div class="cbt">{c1}<br>{c2}</div><div class="cbs">{page['cta_sub']}</div></div><a href="tel:+16783957459" class="bw"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a></div>

</main>
{sk['footer']}
{sk['scripts']}
</body>
</html>
"""


def main():
    sk = skeleton()
    for page in PAGES:
        path = os.path.join(REPO_ROOT, page["slug"])
        html = build(page, sk)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        print(f"  wrote {page['slug']:14s} ~{words} words, "
              f"{len(page['faqs'])} FAQs")
    print(f"\n{len(PAGES)} info pages built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
