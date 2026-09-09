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
  * geo -- the Maps embed contains a placeholder place ID
    (0x88f5b3e3e3e3e3e3) so its coordinates cannot be trusted, and the
    address does not resolve in OpenStreetMap. Wrong coordinates would
    misplace the map pin, which is worse than omitting the property. Supply
    the real values from the Google Business Profile to enable it.

Run from the repo root:  python3 tools/build_schema.py
"""

import html
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"

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

AREA_SERVED = ["Snellville", "Loganville", "Grayson", "Lawrenceville",
               "Stone Mountain", "Gwinnett County"]
MAKES = ["BMW", "Mercedes-Benz", "Audi", "Porsche", "Volkswagen", "MINI"]


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
        "areaServed": [{"@type": "City", "name": a} for a in AREA_SERVED],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service",
             "name": f"{m} repair and service"}} for m in MAKES
        ],
        "sameAs": [INSTAGRAM],
    }


def website():
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{SITE}/",
        "name": NAME,
        "publisher": {"@id": BUSINESS_ID},
    }


def webpage(url, title, description):
    return {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": BUSINESS_ID},
    }


def breadcrumbs(items):
    return {
        "@type": "BreadcrumbList",
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

    Service pages use .fq/.ficon; the homepage uses .faq-q/.faq-icon.
    """
    section = content[content.find('class="faq-list"'):]
    section = section[:section.find("</section>")] if "</section>" in section else section
    items = re.findall(
        r'<button class="(?:fq|faq-q)"[^>]*>(.*?)</button>\s*'
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


def service_entity(url, title, description, crumb):
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
        "areaServed": [{"@type": "City", "name": a} for a in AREA_SERVED],
    }


def blog_entity(url, title, description):
    return {
        "@type": "BlogPosting",
        "@id": f"{url}#article",
        "headline": title,
        "description": description,
        "url": url,
        "mainEntityOfPage": {"@id": f"{url}#webpage"},
        "image": f"{SITE}/og-image.jpg",
        "publisher": {"@id": BUSINESS_ID},
        "author": {"@id": BUSINESS_ID},
        "datePublished": "2026-07-28",
        "dateModified": "2026-09-09",
    }


def visible_crumb(content):
    """The service page's own breadcrumb label, so schema matches the page."""
    m = re.search(r'<div class="breadcrumb">.*?<span[^>]*>([^<]+)</span>\s*</div>',
                  content, re.S)
    return html.unescape(m.group(1).strip()) if m else ""


LD_RE = re.compile(r'\s*<script type="application/ld\+json">.*?</script>', re.S)


def main():
    pages = sorted(f for f in os.listdir(REPO_ROOT) if f.endswith(".html"))
    counts = {"service": 0, "home": 0, "post": 0}

    for name in pages:
        content = read(name)
        title, description, url = meta(content)
        if not url:
            print(f"  skip {name}: no canonical")
            continue

        graph = [business(), website(), webpage(url, title, description)]

        if name == HOME:
            graph.append(visible_faq(content))
            counts["home"] += 1
        elif name == POST:
            crumb = title.split("|")[0].strip()
            graph.append(blog_entity(url, title, description))
            graph.append(breadcrumbs([("Home", f"{SITE}/"), (crumb, url)]))
            counts["post"] += 1
        else:
            crumb = visible_crumb(content)
            graph.append(service_entity(url, title, description, crumb))
            graph.append(breadcrumbs([("Home", f"{SITE}/"), (crumb, url)]))
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
