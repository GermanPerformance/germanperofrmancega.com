#!/usr/bin/env python3
"""Which Google Business Profile services each hand-written page answers for.

The profile export lives in german-performance-gbp-categories-services.md.
Framework pages (tools/landing_pages.py) carry their own "gbp" tuple; this
module holds the claims for everything not yet migrated, the pages still
to be built, and the services the owner chose to leave without a page.
tools/check_gbp_alignment.py reads all three.

Keyword variants of one service fold into one page ("BMW Shop", "BMW
mechanic" and "Independent BMW mechanic" are all the BMW hub), and a
brand page claims the generic service it is a variant of. Categories
count as services: the "Brake shop" category is answered by the brake page.
"""

# Hand-written pages, until each is rebuilt on the framework. An entry
# here and in landing_pages.PAGES for the same file is an error.
LEGACY = {
    # make-agnostic pages
    "german-car-repair-snellville-ga.html": (
        "Auto repair shop", "Mechanic", "Car repair and maintenance service",
        "German auto repair", "German car mechanic", "German car speciaist"),
    "german-car-transmission-repair-snellville-ga.html": (
        "Transmission shop", "Transmission", "Transmission repair",
        "Transmission replacement"),
    "german-car-oil-change-snellville-ga.html": ("Oil change service", "Oil change"),
    "german-car-tune-up-snellville-ga.html": ("Auto tune up service",),
    "german-car-ac-repair-snellville-ga.html": (
        "Auto air conditioning service", "Air conditioning", "Car A/C Repair",
        "A/C Diagnostic", "A/C Recharge", "A/C Leak Repair",
        "A/C Compressor Repair"),
    "german-car-check-engine-light-snellville.html": (
        "Auto engine diagnostic", "check engine light"),
    "pre-purchase-inspection-german-car-ga.html": ("Vehicle Inspection",),

    # brand hubs
    "bmw-repair-snellville-ga.html": (
        "BMW repair", "BMW Shop", "BMW mechanic", "Independent BMW mechanic",
        "BMW specialist", "BMW dealership alternative"),
    "mercedes-repair-snellville-ga.html": (
        "Mercedes Repair", "Mercedes shop", "Mercedes mechanic",
        "Independent Mercedes mechanic", "Mercedes specialist",
        "Mercedes dealership alternative", "AMG repair"),
    "audi-repair-snellville-ga.html": (
        "Audi repair", "Audi Shop", "Audi Mechanic", "Independent Audi mechanic",
        "Audi specialist", "Audi dealership alternative"),
    "porsche-repair-snellville-ga.html": (
        "Porsche repair", "Porsche mechanic", "Independent Porsche mechanic",
        "Porsche specialist", "Porsche dealership alternative"),
    "volkswagen-repair-snellville-ga.html": (
        "Volkswagen repair", "VW mechanic", "VW specialist"),

    # brand + service pages
    "bmw-oil-change-snellville-ga.html": ("BMW Oil change",),
    "bmw-suspension-repair-snellville-ga.html": ("Steering & suspension repair",),
    "bmw-transmission-repair-snellville-ga.html": ("Transmission repair",),
    "bmw-cooling-system-repair-snellville-ga.html": (
        "Coolant Leaks", "BMW Water Pump Replacement", "BMW Thermostat Replacement"),
    "bmw-battery-replacement-snellville-ga.html": ("Battery", "Auto battery replacement"),
    "bmw-spark-plug-replacement-snellville-ga.html": ("Spark plug replacement",),
    "mercedes-oil-change-snellville-ga.html": ("Mercedes oil change",),
    "mercedes-brake-service-snellville-ga.html": ("Brakes", "Brake service & repair"),
    "mercedes-suspension-snellville-ga.html": ("Steering & suspension repair",),
    "mercedes-transmission-snellville-ga.html": ("Transmission",),
    "mercedes-ac-repair-snellville-ga.html": ("Air conditioning",),
    "mercedes-engine-diagnostics-snellville-ga.html": ("Auto engine diagnostic",),
    "mercedes-cooling-system-snellville-ga.html": (
        "Coolant Leaks", "Mercedes Water Pump Replacement",
        "Mercedes Thermostat Replacement"),
    "audi-oil-change-snellville-ga.html": ("Audi oil change",),
    "audi-brake-service-snellville-ga.html": ("Brakes",),
    "audi-suspension-repair-snellville-ga.html": ("Steering & suspension repair",),
    "porsche-oil-change-snellville-ga.html": ("Oil change",),
    "porsche-brake-service-snellville-ga.html": ("Brakes",),
    "porsche-suspension-repair-snellville-ga.html": ("Steering & suspension repair",),
    "porsche-inspection-snellville-ga.html": ("Vehicle Inspection",),
    "volkswagen-oil-change-snellville-ga.html": ("Oil change",),
    "volkswagen-brake-service-snellville-ga.html": ("Brakes",),
    "volkswagen-engine-repair-snellville-ga.html": ("Engine repair",),
}

_WATER_PUMP = ("Water Pump Replacement", "BMW Water Pump Replacement",
               "Mercedes Water Pump Replacement", "Porsche Water Pump Replacement",
               "Audi Water Pump Replacement", "VW Water Pump Replacement")
_THERMOSTAT = ("Thermostat Replacement", "BMW Thermostat Replacement",
               "Mercedes Thermostat Replacement", "Porsche Thermostat Replacement",
               "Audi Thermostat Replacement", "VW Thermostat Replacement")
_PERFORMANCE = ("BMW Performance", "Mercedes Performance", "Porsche Performance",
                "Audi Performance", "VW Performance")

# Pages agreed on 2026-09-12 but not yet built. A file that exists must
# move out of here and into landing_pages.PAGES.
PENDING = {
    "german-car-electrical-repair-snellville-ga.html": (
        "Auto electrical service", "Electrical"),
    "german-car-battery-replacement-snellville-ga.html": (
        "Battery", "Auto battery replacement"),
    "german-car-suspension-repair-snellville-ga.html": ("Steering & suspension repair",),
    "german-car-engine-repair-snellville-ga.html": ("Engine repair",),
    "german-car-exhaust-repair-snellville-ga.html": ("Exhaust",),
    "german-car-air-cabin-filter-replacement-snellville-ga.html": (
        "Air & cabin filter replacement",),
    "german-car-spark-plug-replacement-snellville-ga.html": ("Spark plug replacement",),
    "german-car-coolant-leak-repair-snellville-ga.html": ("Coolant Leaks",),
    "german-car-water-pump-replacement-snellville-ga.html": _WATER_PUMP,
    "german-car-thermostat-replacement-snellville-ga.html": _THERMOSTAT,
    "german-car-cold-air-intake-snellville-ga.html": ("Cold Air Intakes",) + _PERFORMANCE,
    "german-car-downpipe-installation-snellville-ga.html": (
        "High-flow Downpipes",) + _PERFORMANCE,
    "german-car-performance-exhaust-snellville-ga.html": (
        "Performance Exhaust System Installation",) + _PERFORMANCE,
}

# Profile services the site deliberately has no page for: the shop is
# German-only on the site, and the owner chose (2026-09-12) to leave the
# other makes on the profile alone. A page claiming one of these is an error.
UNCOVERED = frozenset({
    "Range rover shop", "Land Rover repair", "Range Rover repair",
    "Range Rover specialist", "Jaguar Repair", "Jaguar Shop",
    "Mini Cooper repair", "Mini Cooper mechanic", "European auto repair",
    "European car mechanic", "European specialist", "Import car repair",
})
