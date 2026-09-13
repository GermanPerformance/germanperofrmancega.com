#!/usr/bin/env python3
"""Every service page on the site, grouped by make, in the order the nav shows them.

The nav's Services panel and the phone menu (tools/apply_redesign.py) read
this list, and the six homepage cards follow MONEY, so adding a page here
surfaces it everywhere at once. Group order is the panel's column order.
The first six entries of the first group are the owner's money services --
the Google Business Profile categories -- in the order the homepage cards
show them.
"""

# The six category pages the homepage cards link to, in the owner's order.
MONEY = [
    ("german-car-repair-snellville-ga.html",              "Auto Repair"),
    ("german-car-brake-repair-snellville-ga.html",        "Brake Repair"),
    ("german-car-transmission-repair-snellville-ga.html", "Transmission Repair"),
    ("german-car-oil-change-snellville-ga.html",          "Oil Change"),
    ("german-car-tune-up-snellville-ga.html",             "Auto Tune-Up"),
    ("german-car-ac-repair-snellville-ga.html",           "Auto Air Conditioning"),
]

GROUPS = [
    ("All German Makes", MONEY + [
        ("german-car-check-engine-light-snellville.html", "Check Engine Light"),
        ("pre-purchase-inspection-german-car-ga.html",     "Pre-Purchase Inspection"),
    ]),
    ("BMW", [
        ("bmw-oil-change-snellville-ga.html",             "Oil Change"),
        ("bmw-suspension-repair-snellville-ga.html",      "Suspension Repair"),
        ("bmw-transmission-repair-snellville-ga.html",    "Transmission Repair"),
        ("bmw-cooling-system-repair-snellville-ga.html",  "Cooling System"),
        ("bmw-battery-replacement-snellville-ga.html",    "Battery Replacement"),
        ("bmw-spark-plug-replacement-snellville-ga.html", "Spark Plugs"),
    ]),
    ("Mercedes-Benz", [
        ("mercedes-oil-change-snellville-ga.html",         "Oil Change"),
        ("mercedes-brake-service-snellville-ga.html",      "Brake Service"),
        ("mercedes-suspension-snellville-ga.html",         "Suspension Repair"),
        ("mercedes-transmission-snellville-ga.html",       "Transmission Service"),
        ("mercedes-ac-repair-snellville-ga.html",          "AC Repair"),
        ("mercedes-engine-diagnostics-snellville-ga.html", "Engine Diagnostics"),
        ("mercedes-cooling-system-snellville-ga.html",     "Cooling System"),
    ]),
    ("Audi", [
        ("audi-oil-change-snellville-ga.html",        "Oil Change"),
        ("audi-brake-service-snellville-ga.html",     "Brake Service"),
        ("audi-suspension-repair-snellville-ga.html", "Suspension Repair"),
    ]),
    ("Porsche", [
        ("porsche-oil-change-snellville-ga.html",        "Oil Change"),
        ("porsche-brake-service-snellville-ga.html",     "Brake Service"),
        ("porsche-suspension-repair-snellville-ga.html", "Suspension Repair"),
        ("porsche-inspection-snellville-ga.html",        "Full Inspection"),
    ]),
    ("Volkswagen", [
        ("volkswagen-oil-change-snellville-ga.html",    "Oil Change"),
        ("volkswagen-brake-service-snellville-ga.html", "Brake Service"),
        ("volkswagen-engine-repair-snellville-ga.html", "Engine Repair"),
    ]),
]

# Each column's heading is a link: the make's repair hub, or for the
# make-agnostic column the homepage section that presents these categories.
HUBS = {
    "All German Makes": "index.html#services",
    "BMW":              "bmw-repair-snellville-ga.html",
    "Mercedes-Benz":    "mercedes-repair-snellville-ga.html",
    "Audi":             "audi-repair-snellville-ga.html",
    "Porsche":          "porsche-repair-snellville-ga.html",
    "Volkswagen":       "volkswagen-repair-snellville-ga.html",
}
