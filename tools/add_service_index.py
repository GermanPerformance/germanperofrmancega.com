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
    ]),
    ("Audi", [
        ("audi-oil-change-snellville-ga.html", "Oil Change"),
        ("audi-brake-service-snellville-ga.html", "Brake Service"),
        ("audi-suspension-repair-snellville-ga.html", "Suspension Repair"),
        ("audi-timing-belt-snellville-ga.html", "Timing Belt"),
        ("audi-quattro-service-snellville-ga.html", "Quattro AWD Service"),
    ]),
    ("Porsche", [
        ("porsche-brake-service-snellville-ga.html", "Brake Service"),
        ("porsche-inspection-snellville-ga.html", "Full Inspection"),
    ]),
    ("Volkswagen", [
        ("volkswagen-oil-change-snellville-ga.html", "Oil Change"),
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

CSS = """
/* Service index: in-content links to every service page */
.svc-index { margin-top: 72px; }
.svc-index-head {
  font-family: 'Space Mono', monospace;
  font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--red-bright); margin-bottom: 28px;
  display: flex; align-items: center; gap: 14px;
}
.svc-index-head::before {
  content: ''; width: 32px; height: 1px; background: var(--red-bright);
}
.svc-index-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 32px 28px;
}
.svc-group-name {
  font-family: 'Bebas Neue', sans-serif; font-size: 1.15rem;
  letter-spacing: 0.08em; color: var(--white); margin-bottom: 14px;
  padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.09);
}
.svc-group a {
  display: block; text-decoration: none; color: var(--silver);
  font-size: 0.9rem; line-height: 1.5; padding: 5px 0;
  transition: color .2s, padding-left .2s;
}
.svc-group a:hover { color: var(--white); padding-left: 6px; }
@media (max-width: 600px) {
  .svc-index-grid { grid-template-columns: 1fr 1fr; gap: 26px 18px; }
}
"""


def build_block():
    groups = []
    for name, entries in GROUPS:
        links = "".join(
            f'        <a href="{href}">{label}</a>\n'
            for href, label in entries
        )
        groups.append(
            f'      <div class="svc-group">\n'
            f'        <div class="svc-group-name">{name}</div>\n'
            f'{links}'
            f'      </div>\n'
        )
    return (
        '\n  <div class="svc-index fade-up">\n'
        '    <div class="svc-index-head">Browse services by make</div>\n'
        '    <div class="svc-index-grid">\n'
        + "".join(groups) +
        '    </div>\n'
        '  </div>\n'
    )


def main():
    path = os.path.join(REPO_ROOT, "index.html")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    if 'class="svc-index' in content:
        print("service index already present")
        return 0

    # Insert after the services grid, still inside #services.
    start = content.index('id="services"')
    end = content.index('id="performance"')
    section = content[start:end]

    marker = section.rindex("</div>\n\n</section>") if "</div>\n\n</section>" in section \
        else section.rindex("</section>")
    section = section[:marker] + build_block() + section[marker:]
    content = content[:start] + section + content[end:]

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    css_path = os.path.join(REPO_ROOT, "assets", "css", "home.css")
    with open(css_path, "a", encoding="utf-8") as fh:
        fh.write(CSS)

    total = sum(len(entries) for _, entries in GROUPS)
    print(f"service index added: {total} links across {len(GROUPS)} groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
