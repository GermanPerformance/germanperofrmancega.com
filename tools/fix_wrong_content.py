#!/usr/bin/env python3
"""Repair wrong-brand and wrong-service content left by the page template.

Three distinct bugs, all the same copy-paste root cause:

  A. Four pages carry the BMW oil-change FAQ wholesale, in both the visible
     HTML and the FAQPage JSON-LD, under their own headings.
  B. Three pages carry BMW oil-change service cards under correct headings.
  C. All 30 pages advertise "BMW-Approved Oil & Filters" in the trust bar,
     including every Mercedes, Audi, Porsche and VW page.

FAQ text is generated once and written to both the visible HTML and the
JSON-LD, so the two cannot disagree -- Google requires markup to match
visible content.

Run from the repo root:  python3 tools/fix_wrong_content.py
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# A. Correct FAQ sets for the four pages carrying BMW oil-change questions.
# --------------------------------------------------------------------------

FAQ_SETS = {
"mercedes-brake-service-snellville-ga.html": [
 ("How often do Mercedes brake pads need replacing?",
  "It depends heavily on how you drive. Most Mercedes owners see 30,000–70,000 miles from a set of pads, with front pads wearing faster than rears. Your car will tell you before it becomes urgent — Mercedes uses electronic wear sensors that trigger a dashboard message when the pads reach their limit."),
 ("Why is my brake warning light still on after new pads?",
  "Because the wear sensor was almost certainly not replaced. Mercedes brake wear sensors are consumable — once the pad wears down to them, the sensor circuit is destroyed and a new pad alone will not clear the message. We fit new sensors with every pad replacement and reset the service message before the car leaves."),
 ("Do you replace rotors every time, or can they be resurfaced?",
  "We measure them and let the numbers decide. Every Mercedes rotor has a minimum thickness stamped on it. If the rotor is above spec and the surface is true, resurfacing is fine. If it is below spec, warped, or heat-cracked, it gets replaced — we will show you the measurement either way."),
 ("How often should Mercedes brake fluid be flushed?",
  "Every two years, regardless of mileage. Brake fluid is hygroscopic, meaning it absorbs moisture from the air over time. That moisture lowers the fluid's boiling point and can cause a soft pedal or brake fade under hard use. We flush and refill with the correct DOT specification for your model."),
 ("Can I use aftermarket brake pads on my Mercedes?",
  "You can, but we generally recommend OEM or OEM-equivalent compounds. Mercedes tunes pad friction material to match the car's ABS and stability control calibration, and cheaper pads often bring noise, more dust, and a different pedal feel. We will talk through the options for your model before ordering anything."),
 ("Do you service AMG and performance brake systems?",
  "Yes. We service the full Mercedes range including AMG models with multi-piston calipers and larger composite rotors. These systems use different pad compounds and torque specifications than the standard range, and we set them up to the correct specification."),
],
"audi-timing-belt-snellville-ga.html": [
 ("When does an Audi timing belt need to be replaced?",
  "For most belt-driven Audi engines the interval falls between 90,000 and 105,000 miles, or around seven years — whichever comes first. Age matters as much as mileage, because the rubber hardens and cracks even on a car that has not been driven much. We confirm the exact interval for your engine by VIN before quoting."),
 ("Does my Audi have a timing belt or a timing chain?",
  "It depends on the engine, not the model year alone. Many older 2.0T, 2.7T and 3.0 V6 engines use belts, while a number of newer Audi engines use chains. The two require completely different service, so we confirm which one your car has from the VIN rather than assuming."),
 ("Why do you replace the water pump at the same time?",
  "On most belt-driven Audi engines the water pump is turned by the timing belt itself. Nearly all of the labor in replacing that pump is the same labor as the belt job. Replacing it while the front of the engine is already apart avoids paying for that work twice when the pump fails later."),
 ("What happens if an Audi timing belt breaks?",
  "On an interference engine — which covers most Audi engines — a snapped belt lets the valves and pistons collide. That typically means bent valves and often damaged pistons and cylinder heads, turning a planned maintenance job into a major engine repair. This is the failure that timing belt intervals exist to prevent."),
 ("Do you replace the tensioner and idler pulleys too?",
  "Always, with no exceptions. The tensioner and idlers wear on the same clock as the belt. Fitting a new belt onto a worn tensioner leaves the engine exposed to exactly the failure the job was meant to prevent, so we replace the complete kit every time."),
 ("How long does an Audi timing belt replacement take?",
  "Plan on the car being with us for a full day. The exact time depends on the engine and how much has to come off the front of the car to reach the timing cover. We will give you a firm timeframe once we confirm your engine, so you can plan around it."),
],
"volkswagen-engine-repair-snellville-ga.html": [
 ("What are the most common VW engine problems you see?",
  "Four come up again and again on the EA888 and related engines: timing chain tensioner failure on earlier versions, carbon buildup on the intake valves of direct-injection engines, oil consumption from worn piston rings or the PCV system, and coolant leaks from the water pump and thermostat housing. We diagnose which one you actually have before recommending work."),
 ("Do you do walnut blasting for carbon buildup?",
  "Yes. Direct-injection VW engines spray fuel straight into the cylinder, so no fuel ever washes over the back of the intake valves. Carbon accumulates there and causes rough idle, misfires and lost power. Walnut shell blasting media strips that deposit off without damaging the valves or the port."),
 ("Can you repair my VW engine instead of replacing it?",
  "Usually, yes. Most of what gets called \"engine failure\" is a specific component — a tensioner, a gasket, a turbo, a PCV valve — rather than the whole engine. We diagnose the actual fault first and tell you honestly when a repair makes sense and when it does not."),
 ("What causes the oil leaks on my Volkswagen?",
  "The usual suspects are the valve cover gasket, the oil filter housing gasket, the rear main seal, and the cam chain cover. Each one drips in a distinctive place, so we clean the area, run the engine, and pinpoint the actual source rather than replacing gaskets speculatively."),
 ("Do you work on both TSI and TDI engines?",
  "Yes, we service both gasoline TSI and diesel TDI Volkswagen engines. The diagnostic approach differs — TDI work brings in injectors, glow plugs and emissions components that gasoline engines do not have — and we have the VW-specific tooling for both."),
 ("How do you diagnose a VW engine problem?",
  "We start with a full scan using VCDS and ODIS, the same software VW dealers use, so we can read every control module rather than just pulling a generic code. From there we look at live data, and where the symptoms call for it, run compression and leak-down tests to confirm the mechanical condition before quoting."),
],
"bmw-transmission-repair-snellville-ga.html": [
 ("Does a BMW transmission really need a fluid service?",
  "Yes, despite the \"lifetime fill\" label. That phrase refers to the design life of the transmission, not the life of your car. In practice we recommend a fluid and filter service somewhere around 60,000–80,000 miles — it is one of the cheapest things you can do to avoid a very expensive repair later."),
 ("What are the warning signs of BMW transmission trouble?",
  "Harsh or delayed shifts, a shudder at light throttle, slipping between gears, a transmission fault message, or the car dropping into limp mode and refusing to shift past a low gear. Any of these are worth diagnosing early, because the cheap fixes are only available before the damage spreads."),
 ("Do you service ZF 8-speed automatics and DCT gearboxes?",
  "Yes. We service the ZF 6-speed and 8-speed automatics used across most of the BMW range, along with DCT dual-clutch and older SMG units. Each has its own fluid specification and service procedure, and we follow the correct one for your gearbox."),
 ("Can you repair a BMW transmission instead of replacing it?",
  "Very often, yes. A large share of BMW transmission faults trace back to the mechatronic unit, valve body or individual solenoids rather than the gearset itself. Those are repairable at a fraction of the cost of a replacement transmission, which is why we diagnose thoroughly before quoting."),
 ("What is a mechatronic unit and why does it fail?",
  "It is the combined valve body and control module that sits inside the transmission and actually commands the gear changes. It fails through worn solenoids, internal wiring faults, or leaking adapter seals — and because it is electronic as well as hydraulic, it needs proper diagnosis rather than guesswork."),
 ("Do you reset the transmission adaptations after service?",
  "Yes. A BMW transmission continuously learns and adapts to clutch wear and your driving style. After a fluid service or repair, those stored adaptations no longer match the hardware, so we reset them with BMW-compatible software and road-test the car to let it relearn correctly."),
],
}

# --------------------------------------------------------------------------
# B. Correct service cards for pages carrying BMW oil-change cards.
#    Keyed by file -> old card title -> (icon, new title, new description).
# --------------------------------------------------------------------------

CARD_SETS = {
"mercedes-transmission-snellville-ga.html": {
 "OEM Oil Filter Replacement": ("\U0001f9ea", "Transmission Fluid &amp; Filter Service",
  "We drain and refill with the correct Mercedes-spec ATF, replace the filter and pan gasket, and set the fluid level at the specified temperature — the step most shops skip and the one that determines whether the service actually works."),
 "BMW-Approved Full Synthetic": ("\U0001f527", "Conductor Plate &amp; Valve Body",
  "The conductor plate is a known failure point on 722.6 and later Mercedes transmissions, causing harsh shifts, limp mode and speed sensor faults. We test it properly and replace or rebuild the valve body rather than condemning the whole unit."),
 "Service Interval Reset": ("⚙️", "7G- and 9G-Tronic Service",
  "We service the full range of modern Mercedes automatics, including 7G-Tronic and 9G-Tronic units. Each has its own fluid specification, fill procedure and adaptation reset, and we follow the correct one for your gearbox."),
},
"mercedes-suspension-snellville-ga.html": {
 "BMW-Approved Full Synthetic": ("\U0001f4a8", "AIRMATIC &amp; Air Suspension Repair",
  "Sagging corners, a harsh ride or a suspension warning message usually trace back to a leaking air strut, a failing compressor, or a valve block. We pinpoint which before replacing anything — these are expensive parts to guess at."),
 "Service Interval Reset": ("\U0001f529", "Control Arms &amp; Bushings",
  "Mercedes front suspensions use multiple control arms per side, and worn bushings show up as vague steering, clunks over bumps and uneven tire wear. We replace the specific arms that are worn and align the car afterwards."),
},
"bmw-differential-service-snellville-ga.html": {
 "OEM Oil Filter Replacement": ("\U0001f6e2️", "Differential Fluid Service",
  "We drain and refill your differential with the correct BMW-spec gear oil, including limited-slip additive where your diff requires it. Old, broken-down fluid is the most common cause of differential whine and premature wear."),
 "BMW-Approved Full Synthetic": ("\U0001f50a", "Whine &amp; Noise Diagnosis",
  "A differential that howls under load, whines on deceleration or clunks on take-up is telling you something specific. We road-test the car and isolate whether the noise is really the diff, a worn wheel bearing, or a failing driveshaft joint."),
 "Service Interval Reset": ("\U0001f6e0️", "Seals &amp; Cover Gasket Repair",
  "Differential leaks come from the pinion seal, the axle output seals, or the rear cover gasket. We find the actual source, replace the seal, and refill to the correct level — running a differential low on fluid destroys it quickly."),
},
}

# --------------------------------------------------------------------------
# C. Brand-appropriate trust bar and road-test copy.
# --------------------------------------------------------------------------

BRAND_LABELS = [
    ("bmw", "BMW"), ("mercedes", "Mercedes"), ("audi", "Audi"),
    ("porsche", "Porsche"), ("volkswagen", "VW"),
]

TRUST_OLD = '<div class="tv">OEM</div><div class="tl">BMW-Approved<br>Oil & Filters</div>'
ROADTEST_OLD = "Your BMW is road-tested before pickup"


def brand_label(filename):
    """Marque for a page, or a neutral label for the cross-brand pages."""
    for prefix, label in BRAND_LABELS:
        if filename.startswith(prefix):
            return label
    return None


def build_faq_html(pairs):
    """Visible FAQ accordion items."""
    return "\n".join(
        f'      <div class="fi fu"><button class="fq" onclick="toggleFaq(this)">{q}'
        f'<span class="ficon">+</span></button><div class="fa"><p>{a}</p></div></div>'
        for q, a in pairs
    )


def build_faq_jsonld(pairs):
    """FAQPage JSON-LD built from the same source strings as the HTML."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }, indent=2, ensure_ascii=False)


FAQ_LIST_RE = re.compile(r'(<div class="faq-list">\n).*?(\n    </div>)', re.S)
JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json">\n).*?(\n</script>)', re.S)


def fix_faqs(page, content):
    pairs = FAQ_SETS[page]

    content, n1 = FAQ_LIST_RE.subn(
        lambda m: m.group(1) + build_faq_html(pairs) + m.group(2), content, count=1)
    content, n2 = JSONLD_RE.subn(
        lambda m: m.group(1) + build_faq_jsonld(pairs) + m.group(2), content, count=1)

    if (n1, n2) != (1, 1):
        raise SystemExit(f"{page}: FAQ html={n1}, jsonld={n2} (expected 1,1)")
    return content


def fix_cards(page, content):
    for old_title, (icon, new_title, new_desc) in CARD_SETS[page].items():
        pattern = re.compile(
            r'<div class="card"><span class="ci">[^<]*</span>'
            r'<div class="ct">' + re.escape(old_title) + r'</div>'
            r'<div class="cd">.*?</div></div>', re.S)
        replacement = (f'<div class="card"><span class="ci">{icon}</span>'
                       f'<div class="ct">{new_title}</div>'
                       f'<div class="cd">{new_desc}</div></div>')
        content, n = pattern.subn(lambda _: replacement, content, count=1)
        if n != 1:
            raise SystemExit(f"{page}: card {old_title!r} matched {n} times (expected 1)")
    return content


def main():
    pages = sorted(
        f for f in os.listdir(REPO_ROOT)
        if f.endswith(".html") and f not in ("index.html",)
        and "dealer-vs-independent" not in f
    )

    counts = {"faq": 0, "cards": 0, "trust": 0, "roadtest": 0}

    for page in pages:
        path = os.path.join(REPO_ROOT, page)
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        content = original

        if page in FAQ_SETS:
            content = fix_faqs(page, content)
            counts["faq"] += 1

        if page in CARD_SETS:
            content = fix_cards(page, content)
            counts["cards"] += 1

        # C. Trust bar: name the page's own marque, and describe parts and
        # fluids generally -- "Oil & Filters" is wrong on a brake page.
        label = brand_label(page)
        if TRUST_OLD in content:
            new_label = f"{label}-Approved" if label else "Factory-Approved"
            content = content.replace(
                TRUST_OLD,
                f'<div class="tv">OEM</div><div class="tl">{new_label}<br>Parts & Fluids</div>')
            counts["trust"] += 1

        if ROADTEST_OLD in content and label != "BMW":
            subject = f"Your {label}" if label else "Your car"
            content = content.replace(
                ROADTEST_OLD, f"{subject} is road-tested before pickup")
            counts["roadtest"] += 1

        if content != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)

    print(f"FAQ sets replaced:      {counts['faq']}")
    print(f"card sets replaced:     {counts['cards']}")
    print(f"trust bars re-branded:  {counts['trust']}")
    print(f"road-test copy fixed:   {counts['roadtest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
