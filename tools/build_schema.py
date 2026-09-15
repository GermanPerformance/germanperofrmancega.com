#!/usr/bin/env python3
"""Generate structured data for every page.

The site had no business schema at all: index.html carried zero JSON-LD and
the service pages had only FAQPage. For a local service business the
LocalBusiness entity is the single most important piece of markup, so every
page now emits one shared @graph:

    AutoRepair  #business   the shop itself, referenced by everything else
    WebSite     #website
    WebPage     #webpage    this page, linked to both of the above

plus, per page type:

    service pages   Service + BreadcrumbList (+ the existing FAQPage)
    homepage        FAQPage, converted from malformed microdata
    blog post       BlogPosting + BreadcrumbList

Deliberately omitted:

  * aggregateRating -- a rating a business publishes about itself is
    self-serving, produces no stars, and risks a manual action. The 4.5/185
    figures stay as on-page text and the Google Business Profile carries the
    rating.
  * aggregateRating on the Service entities, for the same reason.

geo was omitted while the only coordinates to hand came from a Maps embed
with a placeholder place ID. It is now emitted from GEO below, which two
independent sources agree on to within 200 m (see the note on GEO). If the
Google Business Profile shows a different pin, GEO is the value to correct.

Run from the repo root:  python3 tools/build_schema.py
"""

import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import place  # noqa: E402
from redirects import site_pages  # noqa: E402
from urls import SITE, url_for_href  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = "index.html"
POST = "dealer-vs-independent-german-car-repair.html"

BUSINESS_ID = f"{SITE}/#business"
WEBSITE_ID = f"{SITE}/#website"

# Verified against the site's own copy and confirmed with the owner.
NAME = "German Performance"
PHONE = "+1-678-395-7459"
STREET = "2144 Parkwood Rd NW"
CITY = "Snellville"
REGION = "GA"
POSTAL = "30078"
FOUNDED = "2010"
INSTAGRAM = "https://www.instagram.com/germanperformance.auto"
CARFAX = "https://www.carfax.com/Reviews-German-Performance-Snellville-GA_IY4SR7AEBP"
FACEBOOK = "https://www.facebook.com/GermanPerformance1/"
YELP = "https://www.yelp.com/biz/german-performance-snellville-2"
# The Google Business Profile (permanent ?cid= link), the map that opens
# the listing rather than the building, and the pin exactly where the
# listing puts it: all from tools/place.py, which also documents why.
GOOGLE_BUSINESS_PROFILE = place.PROFILE
MAP = place.PLACE
GEO = place.GEO

AREA_SERVED = ["Snellville", "Loganville", "Grayson", "Lawrenceville",
               "Stone Mountain", "Gwinnett County"]
AREA_TYPES = {"Gwinnett County": "AdministrativeArea"}


def area_served():
    return [{"@type": AREA_TYPES.get(a, "City"), "name": a} for a in AREA_SERVED]
# The five marques with a hub page. MINI is worked on (it runs on ISTA,
# see About) but has no page of its own, so it is not offered here.
MAKES = ["BMW", "Mercedes-Benz", "Audi", "Porsche", "Volkswagen"]


def business():
    return {
        "@type": "AutoRepair",
        "@id": BUSINESS_ID,
        "name": NAME,
        "url": f"{SITE}/",
        "telephone": PHONE,
        "priceRange": "$$",
        "foundingDate": FOUNDED,
        "image": f"{SITE}/og-image.jpg",
        "logo": f"{SITE}/assets/img/logo-288.webp",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": CITY,
            "addressRegion": REGION,
            "postalCode": POSTAL,
            "addressCountry": "US",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:30",
            "closes": "18:00",
        }],
        "geo": {"@type": "GeoCoordinates", **GEO},
        "areaServed": area_served(),
        "hasMap": MAP,
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service",
             "name": f"{m} repair and service"}} for m in MAKES
        ],
        "sameAs": same_as(),
    }


def same_as():
    """Every profile the shop controls, the Google one first when known."""
    profiles = [GOOGLE_BUSINESS_PROFILE, INSTAGRAM, FACEBOOK, YELP, CARFAX]
    return [p for p in profiles if p]


def website():
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{SITE}/",
        "name": NAME,
        "publisher": {"@id": BUSINESS_ID},
    }


def webpage(url, title, description, image=None):
    node = {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": BUSINESS_ID},
    }
    if image:
        node["primaryImageOfPage"] = {"@type": "ImageObject", "url": image}
    return node


def breadcrumbs(items):
    return {
        "@type": "BreadcrumbList",
        "@id": f"{items[-1][1]}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": url}
            for i, (name, url) in enumerate(items, 1)
        ],
    }


def strip_tags(fragment):
    """Visible text of an HTML fragment, with the +/- accordion icon removed."""
    fragment = re.sub(r'<span class="(ficon|faq-icon)">.*?</span>', "", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def read(name):
    with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def meta(content):
    title = re.search(r"<title>(.*?)</title>", content, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', content)
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', content)
    return (html.unescape(title.group(1).strip()) if title else "",
            html.unescape(desc.group(1).strip()) if desc else "",
            canon.group(1).strip() if canon else "")


def visible_faq(content):
    """Build FAQPage from whatever accordion the page actually renders.

    Derived from the visible HTML rather than from any existing JSON-LD, for
    two reasons: Google requires the markup to match what the reader sees,
    and reading the page's own schema back made this generator destructive --
    once the FAQPage was nested inside an @graph, a second run could no
    longer find it and silently dropped the FAQ.

    Three markups exist across the site and all three must parse:
      .fq/.ficon on a <button>      -- service pages
      .faq-q/.faq-icon on a <button> -- the older homepage
      .fq on a <summary> inside <details> -- the rewritten homepage

    The last one is a native disclosure widget and needs no JavaScript,
    which is why it is worth supporting rather than arguing with. Matching
    only <button> meant the homepage silently produced no FAQ at all.
    """
    # No closing quote: the container is class="faq-list fu" on some pages,
    # and matching the quote silently found nothing and returned the last
    # character of the document.
    start = content.find('class="faq-list')
    if start == -1:
        return None
    section = content[start:]
    section = section[:section.find("</section>")] if "</section>" in section else section
    items = re.findall(
        r'<(?:button|summary) class="(?:fq|faq-q)"[^>]*>(.*?)</(?:button|summary)>\s*'
        r'<div class="(?:fa|faq-a)"[^>]*>(.*?)</div>', section, re.S)
    if not items:
        return None
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in items
        ],
    }


def service_entity(url, title, description, crumb, image=None):
    # The breadcrumb label carries a location suffix ("BMW Oil Change --
    # Snellville, GA") because that is what the page renders. The service
    # itself is just the service; its area is expressed by areaServed.
    service_name = re.split(r"\s+[--\u2014]\s+", crumb)[0].strip()
    return {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": service_name,
        "serviceType": service_name,
        "description": description,
        "url": url,
        "provider": {"@id": BUSINESS_ID},
        "areaServed": area_served(),
        "mainEntityOfPage": {"@id": f"{url}#webpage"},
        **({"image": image} if image else {}),
    }


def headline(title):
    """The article's own title: Google wants the headline without the site
    name that the <title> carries for the browser tab."""
    return re.sub(r"\s*\|\s*" + re.escape(NAME) + r"\s*$", "", title)


def blog_entity(url, title, description):
    return {
        "@type": "BlogPosting",
        "@id": f"{url}#article",
        "headline": headline(title),
        "description": description,
        "url": url,
        "mainEntityOfPage": {"@id": f"{url}#webpage"},
        "image": f"{SITE}/og-image.jpg",
        "publisher": {"@id": BUSINESS_ID},
        "author": {"@id": BUSINESS_ID},
        "datePublished": "2026-07-28",
        "dateModified": "2026-09-09",
    }


def social_image(content):
    """The page's og:image, if it declares one -- the service pages do."""
    m = re.search(r'<meta property="og:image" content="([^"]*)"', content)
    return m.group(1).strip() if m else None


CRUMB_BLOCK_RE = re.compile(r'<div class="breadcrumb">(.*?)</div>', re.S)
CRUMB_STEP_RE = re.compile(r'<a href="([^"]+)">([^<]+)</a>|<span[^>]*>([^<]+)</span>\s*$')


def visible_trail(content):
    """The page's own breadcrumb, so schema matches what it renders:
    ((label, href), ...) with the page itself last and without an href.
    Home / BMW Repair / BMW Oil Change on a make's page, two steps on a
    hub or a make-agnostic page, nothing on a page with no crumb."""
    block = CRUMB_BLOCK_RE.search(content)
    if not block:
        return ()
    steps = []
    for href, linked, here in CRUMB_STEP_RE.findall(block.group(1)):
        label = html.unescape((linked or here).strip())
        steps.append((label, href or None))
    return tuple(steps)


def visible_crumb(content):
    """The page's own label: the last step of its trail."""
    trail = visible_trail(content)
    return trail[-1][0] if trail else ""


def trail_items(content, url):
    """BreadcrumbList items for the page: every linked step at its own URL,
    then the page itself."""
    steps = visible_trail(content) or (("Home", "index.html"), ("", None))
    linked = [(label, url_for_href(href)) for label, href in steps[:-1]]
    return linked + [(steps[-1][0], url)]


LD_RE = re.compile(r'\s*<script type="application/ld\+json">.*?</script>', re.S)

# Pages that describe the business rather than a job it performs. They get
# the matching WebPage subtype instead of a Service entity.
INFO_PAGES = {"about.html": "AboutPage", "contact.html": "ContactPage",
              "privacy-policy.html": "WebPage"}


def main():
    pages = site_pages(os.listdir(REPO_ROOT))
    counts = {"service": 0, "home": 0, "post": 0}

    for name in pages:
        content = read(name)
        title, description, url = meta(content)
        if not url:
            print(f"  skip {name}: no canonical")
            continue

        image = social_image(content)
        graph = [business(), website(), webpage(url, title, description, image)]

        if name == HOME:
            faq = visible_faq(content)
            if faq:
                graph.append(faq)
            else:
                print("  !! index.html: no FAQ found in the visible markup")
            counts["home"] += 1
        elif name == POST:
            crumb = title.split("|")[0].strip()
            graph.append(blog_entity(url, title, description))
            graph.append(breadcrumbs([("Home", f"{SITE}/"), (crumb, url)]))
            counts["post"] += 1
        elif name in INFO_PAGES:
            # The policy uses the post layout, which has no breadcrumb;
            # its title's first segment is the label a crumb would carry.
            crumb = visible_crumb(content) or title.split("|")[0].strip()
            # The WebPage node is already in the graph; narrow its type
            # rather than adding a second page entity for the same URL.
            graph[2]["@type"] = INFO_PAGES[name]
            graph.append(breadcrumbs([("Home", f"{SITE}/"), (crumb, url)]))
            faq = visible_faq(content)
            if faq:
                graph.append(faq)
            counts["info"] = counts.get("info", 0) + 1
        else:
            crumb = visible_crumb(content)
            graph.append(service_entity(url, title, description, crumb, image))
            trail = breadcrumbs(trail_items(content, url))
            graph[2]["breadcrumb"] = {"@id": trail["@id"]}
            graph.append(trail)
            faq = visible_faq(content)
            if faq:
                graph.append(faq)
            counts["service"] += 1

        payload = json.dumps({"@context": "https://schema.org", "@graph": graph},
                             indent=2, ensure_ascii=False)
        block = f'\n<script type="application/ld+json">\n{payload}\n</script>'

        # Replace every existing JSON-LD block with the single new graph.
        content = LD_RE.sub("", content)
        content = content.replace("</head>", block + "\n</head>", 1)

        with open(os.path.join(REPO_ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(content)

    print(f"service pages: {counts['service']}, homepage: {counts['home']}, "
          f"blog: {counts['post']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
