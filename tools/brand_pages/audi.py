"""Audi service pages, built by tools/build_service_pages.py.

One dict per page (the A4, A6, Q5, Q7, S and RS). Every technical claim is a documented
characteristic of the marque; nothing about pricing, turnaround or
certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points,
faq_head, faqs, cta, cta_sub.
"""

PAGES = ()
