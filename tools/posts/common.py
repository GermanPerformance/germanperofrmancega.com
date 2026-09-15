"""What every article shares: the slugs it may link, the note that closes
it, and the facts that note may state.

Every fact here is already on the site or was supplied by the owner on
2026-09-15: the technicians are ASE-certified and Mercedes-Benz factory-
trained, one is an ASE Master Technician with the advanced engine
diagnostics certification who specialises in electrical faults and engine
repairs and trains the junior technicians; German cars only since 2010,
more than 10,000 of them; factory software per marque (ISTA, XENTRY, ODIS,
PIWIS); written estimate with photographs before any work; 12-month /
12,000-mile parts-and-labor warranty. No prices are quoted anywhere, on
purpose: the articles explain what moves a bill, and the estimate does
the rest.

The technicians are not named. The owner asked that credentials be
attributed to the shop's technicians collectively.

Case studies (posts/bmw.py, posts/mercedes.py) are written as anonymised,
representative jobs -- year, model, engine, complaint, finding, fix,
outcome -- with no customer names, dates or invoices. The owner confirmed
on 2026-09-15 that the shop has handled each of these scenarios and asked
for them to be written up this way.
"""

from urls import href_for

# The three general articles.
DEALER = "dealer-vs-independent-german-car-repair.html"
COSTS = "what-affects-german-car-repair-costs.html"
DIAGNOSTICS = "why-german-cars-need-specialist-diagnostics.html"

# The BMW and Mercedes-Benz guides (posts/bmw*.py, posts/mercedes*.py).
BMW_MAINTENANCE = "bmw-maintenance-schedule-explained.html"
BMW_DRIVETRAIN = "bmw-drivetrain-malfunction-explained.html"
BMW_COSTS = "why-bmw-repair-costs-what-it-does.html"
BMW_CASES = "bmw-repair-case-studies.html"
MB_SERVICE_AB = "mercedes-service-a-vs-service-b.html"
MB_AIRMATIC = "mercedes-airmatic-problems-symptoms-diagnosis.html"
MB_COSTS = "why-mercedes-repair-costs-what-it-does.html"
MB_CASES = "mercedes-repair-case-studies.html"

# The money pages an article can support.
HOME_PAGE = "index.html"
BMW_HUB = "bmw-repair.html"
MERCEDES_HUB = "mercedes-repair.html"

# The general service pages the articles point at.
BRAKES = "german-car-brake-repair.html"
TRANSMISSION = "german-car-transmission-repair.html"
OIL = "german-car-oil-change.html"
TUNE_UP = "german-car-tune-up.html"
AC = "german-car-ac-repair.html"
CEL = "german-car-check-engine-light.html"
INSPECTION = "german-car-pre-purchase-inspection.html"

HOME = href_for(HOME_PAGE)
SERVICES = f"{HOME}#services"
REPAIRS = f"{HOME}#repairs"
PROCESS = f"{HOME}#process"
STORY = f"{HOME}#story"


def link(slug, text):
    return f'<a href="{href_for(slug)}">{text}</a>'


# The note that closes each article: who wrote it and what they bring.
AUTHOR_NOTE = (
    "<strong>About the people who wrote this.</strong> Written by the "
    "technicians at German Performance in Snellville, Georgia. They are "
    "ASE-certified and Mercedes-Benz factory-trained, and one is an ASE "
    "Master Technician who holds the advanced engine diagnostics "
    "certification, specialises in "
    "electrical faults and engine repairs, and trains the shop's junior "
    "technicians. They have worked only on German cars since 2010 &mdash; "
    "more than 10,000 of them through this shop &mdash; and every repair "
    "leaves with a written 12-month, 12,000-mile parts-and-labor warranty."
)
