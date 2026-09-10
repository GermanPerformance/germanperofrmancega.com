#!/usr/bin/env python3
"""Give the homepage's services section real links to the service pages.

The #services section contained zero <a> elements: all 30 service pages were
reachable only from footer boilerplate, which carries far less weight than an
in-content link and gives the reader no way to navigate from the section that
describes the work.

The service cards list generic jobs ("Oil & Filter Service") while the pages
are brand-specific, so linking those list items would mean picking one marque
arbitrarily. Instead this adds a brand index below the cards: every service
page, grouped by make, in the section where a reader is already deciding what
they need.

Run from the repo root:  python3 tools/add_service_index.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUPS = [
    ("BMW", [
        ("bmw-oil-change-snellville-ga.html", "Oil Change"),
        ("bmw-suspension-repair-snellville-ga.html", "Suspension Repair"),
        ("bmw-transmission-repair-snellville-ga.html", "Transmission Repair"),
        ("bmw-cooling-system-repair-snellville-ga.html", "Cooling System"),
        ("bmw-battery-replacement-snellville-ga.html", "Battery Replacement"),
        ("bmw-spark-plug-replacement-snellville-ga.html", "Spark Plugs"),
        ("bmw-wheel-alignment-snellville-ga.html", "Wheel Alignment"),
        ("bmw-differential-service-snellville-ga.html", "Differential Service"),
    ]),
    ("Mercedes-Benz", [
        ("mercedes-oil-change-snellville-ga.html", "Oil Change"),
        ("mercedes-brake-service-snellville-ga.html", "Brake Service"),
        ("mercedes-suspension-snellville-ga.html", "Suspension Repair"),
        ("mercedes-transmission-snellville-ga.html", "Transmission Service"),
        ("mercedes-ac-repair-snellville-ga.html", "AC Repair"),
        ("mercedes-engine-diagnostics-snellville-ga.html", "Engine Diagnostics"),
        ("mercedes-cooling-system-snellville-ga.html", "Cooling System"),
    ]),
    ("Audi", [
        ("audi-oil-change-snellville-ga.html", "Oil Change"),
        ("audi-brake-service-snellville-ga.html", "Brake Service"),
        ("audi-suspension-repair-snellville-ga.html", "Suspension Repair"),
        ("audi-timing-belt-snellville-ga.html", "Timing Belt"),
        ("audi-quattro-service-snellville-ga.html", "Quattro AWD Service"),
    ]),
    ("Porsche", [
        ("porsche-oil-change-snellville-ga.html", "Oil Change"),
        ("porsche-brake-service-snellville-ga.html", "Brake Service"),
        ("porsche-suspension-repair-snellville-ga.html", "Suspension Repair"),
        ("porsche-inspection-snellville-ga.html", "Full Inspection"),
    ]),
    ("Volkswagen", [
        ("volkswagen-oil-change-snellville-ga.html", "Oil Change"),
        ("volkswagen-brake-service-snellville-ga.html", "Brake Service"),
        ("volkswagen-engine-repair-snellville-ga.html", "Engine Repair"),
        ("volkswagen-timing-chain-snellville-ga.html", "Timing Chain"),
    ]),
    ("All German Makes", [
        ("german-car-check-engine-light-snellville.html", "Check Engine Light"),
        ("german-car-ac-repair-snellville-ga.html", "AC Repair"),
        ("german-car-tune-up-snellville-ga.html", "Tune-Up"),
        ("german-car-emissions-repair-snellville-ga.html", "Emissions Repair"),
        ("pre-purchase-inspection-german-car-ga.html", "Pre-Purchase Inspection"),
        ("german-car-fleet-service-snellville-ga.html", "Fleet Service"),
    ]),
]



# Each make's heading is the entry point to its repair hub.
HUBS = {
    "BMW": "bmw-repair-snellville-ga.html",
    "Mercedes-Benz": "mercedes-repair-snellville-ga.html",
    "Audi": "audi-repair-snellville-ga.html",
    "Porsche": "porsche-repair-snellville-ga.html",
    "Volkswagen": "volkswagen-repair-snellville-ga.html",
}


def group_heading(name):
    hub = HUBS.get(name)
    if not hub:
        return f'        <div class="svc-group-name">{name}</div>\n'
    return (f'        <div class="svc-group-name"><a href="{hub}">{name} '
            f'<span class="svc-hub-go">&rarr;</span></a></div>\n')


def build_block():
    groups = []
    for name, entries in GROUPS:
        links = "".join(
            f'        <a href="{href}">{label}</a>\n'
            for href, label in entries
        )
        groups.append(
            f'      <div class="svc-group">\n'
            f'{group_heading(name)}'
            f'{links}'
            f'      </div>\n'
        )
    return (
        '\n  <div class="svc-index fu">\n'
        '    <div class="svc-index-head"><div class="sl">Browse services by make</div></div>\n'
        '    <div class="svc-index-grid">\n'
        + "".join(groups) +
        '    </div>\n'
        '  </div>\n'
    )


def main():
    path = os.path.join(REPO_ROOT, "index.html")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    block = build_block()

    if 'class="svc-index' in content:
        # Replace rather than skip. Skipping meant that adding a service
        # page could never surface it in the homepage index -- the block
        # was written once and then frozen.
        # Consume the leading blank line and indent too. build_block()
        # emits them, so a regex that starts at <div left one behind on
        # every run and the block drifted right by two spaces each time.
        existing = re.compile(
            r'\n\s*<div class="svc-index.*?\n  </div>\n', re.S)
        updated, n = existing.subn(block, content, count=1)
        if n != 1:
            print("service index present but not replaceable")
            return 1
        if updated == content:
            print("service index already current")
            return 0
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(updated)
        total = sum(len(e) for _, e in GROUPS)
        print(f"service index updated: {total} links across {len(GROUPS)} groups")
        return 0

    # Insert after the services grid, still inside #services.
    start = content.index('id="services"')
    end = content.index('id="performance"')
    section = content[start:end]

    marker = section.rindex("</div>\n\n</section>") if "</div>\n\n</section>" in section \
        else section.rindex("</section>")
    section = section[:marker] + block + section[marker:]
    content = content[:start] + section + content[end:]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    total = sum(len(entries) for _, entries in GROUPS)
    print(f"service index added: {total} links across {len(GROUPS)} groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
