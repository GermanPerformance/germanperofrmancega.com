#!/usr/bin/env python3
"""Fill the four widest gaps in service coverage.

BMW has eight service pages, Mercedes six and Audi five, against Porsche's
two and Volkswagen's three. That imbalance is not a reflection of what the
shop works on -- it is where the original site stopped. Each of these four
is a routine, high-intent job that every other marque on the site already
has a page for:

    porsche-oil-change            Porsche had no page for the single most
                                  common service anyone books
    porsche-suspension-repair     Cayenne and Panamera air suspension is one
                                  of the most searched Porsche faults
    volkswagen-brake-service      the only marque with no brake page
    mercedes-cooling-system       BMW has one; Mercedes cooling failures are
                                  just as well documented

Every technical claim below is a genuine, documented characteristic of the
marque. Nothing about pricing, turnaround or certification is invented, and
no page claims a capability the others do not already claim.

The skeleton -- nav, trust bar, call bar, footer -- is lifted from a live
page of the SAME marque, so the trust bar says "Porsche-Approved" on a
Porsche page. Building the brand hubs from a BMW donor is exactly how
"BMW-Approved Parts & Fluids" once shipped on the Porsche hub.

Run from the repo root:  python3 tools/build_service_pages.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"

ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none">'
         '<path d="M3 8H13M9 4L13 8L9 12" stroke="currentColor" '
         'stroke-width="1.5" stroke-linecap="round"/></svg>')

PAGES = [
{
 "slug": "porsche-oil-change-snellville-ga.html",
 "donor": "porsche-brake-service-snellville-ga.html",
 "brand": "Porsche",
 "h1": ("PORSCHE", "OIL", "CHANGE"),
 "title": "Porsche Oil Change Snellville GA | German Performance",
 "desc": ("Porsche oil change in Snellville, GA. A40 and C-spec approved oil, "
          "correct dry-sump fill, cartridge filter and PIWIS service reset. "
          "Call (678) 395-7459."),
 "crumb": "Porsche Oil Change — Snellville, GA",
 "sub": ("Porsche oil service in Snellville, GA — for the 911, Boxster, Cayman, "
         "Macan, Cayenne and Panamera. Approved oil for your exact model and "
         "year, the correct fill for a dry-sump engine, and a service reset "
         "done properly."),
 "cards_head": ("A PROPER PORSCHE", "OIL SERVICE"),
 "cards_sub": ("A Porsche oil change is not a quicker version of an ordinary "
               "one. The approvals are specific, the capacities are large, and "
               "on most modern models there is no dipstick to check your work."),
 "cards": [
   ("Porsche-Approved Oil",
    "Porsche publishes its own oil approvals — A40 across most of the gasoline "
    "range, and the newer C-series specifications on models built for "
    "particulate filters. We fill the approval and viscosity listed for your "
    "exact model and year, not a generic full synthetic that happens to be on "
    "the shelf."),
   ("Correct Dry-Sump Fill",
    "The 911, Boxster and Cayman use an integrated dry-sump system that holds "
    "far more oil than a conventional engine and drains from more than one "
    "point. Underfilling is the common outcome when the job is treated as a "
    "routine drain-and-fill."),
   ("Level Verified at Temperature",
    "Most modern Porsches have no dipstick — the level is read electronically, "
    "and only reads correctly with the engine at operating temperature on level "
    "ground. We verify it that way before the car leaves, which is the step "
    "most often skipped."),
   ("Cartridge Filter Replacement",
    "An OEM or OEM-equivalent cartridge filter with new sealing rings. We also "
    "inspect the old filter media and the magnetic drain plug for metal, which "
    "is the cheapest early warning any engine gives you."),
   ("Bore Score and IMS Awareness",
    "On the 996 and early 997, what comes out with the oil matters. Fine metal "
    "in the filter or on the plug is worth knowing about long before it becomes "
    "a noise, and we will tell you what we saw either way."),
   ("Service Reset and Inspection",
    "The maintenance reminder is reset through the factory interface rather "
    "than cleared by a generic tool, and the car gets a multi-point inspection "
    "while it is up — leaks, boots, belts, tyres and brake wear."),
 ],
 "why_head": ("PORSCHE OIL", "DONE RIGHT"),
 "why_lead": ("The reason a Porsche oil service costs more than a generic one is "
              "not the oil. It is the capacity, the approval, the dry-sump "
              "drain procedure and the fact that you cannot confirm the result "
              "with a dipstick. Get any of those wrong and the car leaves "
              "underfilled."),
 "why_points": [
   "Porsche A40 and C-series approved oils, matched to model and year",
   "Dry-sump drain and fill procedure on 911, Boxster and Cayman",
   "Electronic oil level verified at operating temperature before handover",
   "OEM or OEM-equivalent cartridge filters with new seals",
   "Filter media and magnetic plug inspected for metal, and reported to you",
   "Maintenance reminder reset through PIWIS-compatible diagnostics",
 ],
 "faq_head": ("PORSCHE OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a Porsche need an oil change?",
    "Porsche's published interval for most modern models is 10,000 miles or "
    "once a year, whichever comes first. Short trips, track days and long "
    "periods parked are all harder on oil than steady mileage, so cars used "
    "that way are better served on a shorter interval. If your car is driven "
    "rarely, the annual limit matters more than the mileage."),
   ("What oil does my Porsche take?",
    "It depends on the model and year. Most of the gasoline range calls for an "
    "oil carrying Porsche's A40 approval, while newer models built with "
    "particulate filters use the C-series specifications. The approval matters "
    "more than the brand — an oil without it may meet a general industry "
    "standard and still be wrong for the engine."),
   ("Why is a Porsche oil change more involved than a normal one?",
    "Three reasons. The 911, Boxster and Cayman use an integrated dry-sump "
    "system that holds significantly more oil and drains from more than one "
    "point. The approvals are Porsche-specific. And most modern models have no "
    "dipstick, so the level can only be confirmed electronically with the "
    "engine warm and the car level."),
   ("Can you reset the service reminder?",
    "Yes. We reset it through the factory-level interface so the car's own "
    "maintenance schedule stays accurate, rather than clearing the message "
    "with a generic tool and leaving the underlying counter wrong."),
   ("Will you tell me if you find metal in the oil?",
    "Yes, and we look for it. We inspect the magnetic drain plug and the old "
    "filter media every time. On a 996 or an early 997 that inspection is one "
    "of the few routine chances to notice bearing wear early. If we find "
    "something we will show you and explain what it does and does not mean."),
   ("Will an independent oil change affect my Porsche warranty?",
    "No. Federal law protects your right to have routine maintenance performed "
    "by an independent shop without voiding a manufacturer warranty, as long as "
    "the correct specification parts and fluids are used and the work is "
    "documented. You leave with a written record of what was done."),
 ],
 "cta": ("PORSCHE OIL SERVICE", "DUE?"),
 "cta_sub": "Call and tell us the model and year — we will confirm the approval your engine needs.",
},
{
 "slug": "porsche-suspension-repair-snellville-ga.html",
 "donor": "porsche-brake-service-snellville-ga.html",
 "brand": "Porsche",
 "h1": ("PORSCHE", "SUSPENSION", "REPAIR"),
 "title": "Porsche Suspension Repair Snellville GA | German Performance",
 "desc": ("Porsche suspension repair in Snellville, GA. Cayenne and Panamera air "
          "suspension, PASM dampers, control arms and alignment to factory spec. "
          "Call (678) 395-7459."),
 "crumb": "Porsche Suspension Repair — Snellville, GA",
 "sub": ("Porsche suspension work in Snellville, GA — air suspension on the "
         "Cayenne and Panamera, PASM dampers, control arms and bushings, and "
         "alignment to Porsche's own specification rather than a generic "
         "setting."),
 "cards_head": ("PORSCHE SUSPENSION", "WORK WE DO"),
 "cards_sub": ("Air suspension and adaptive dampers fail in ways a visual "
               "inspection will not find. Most of this work starts with a "
               "diagnosis, not a part."),
 "cards": [
   ("Air Suspension Diagnosis",
    "A Cayenne or Panamera sitting low overnight, or throwing a chassis "
    "warning, is usually a leaking strut or a compressor worn out trying to "
    "keep up with one. We find which, because replacing the compressor while "
    "the leak remains simply wears out the new one."),
   ("Air Strut and Compressor Replacement",
    "Struts and compressors replaced as a system where the evidence supports "
    "it, with the ride height sensors recalibrated afterwards so the car sits "
    "and levels the way it should."),
   ("PASM Damper Testing",
    "Porsche Active Suspension Management adjusts damping electronically. When "
    "a damper or its control fails, the system stores a fault and reverts to a "
    "fixed setting — often the first sign is that the car simply feels less "
    "composed than it used to."),
   ("Control Arms, Bushings and Ball Joints",
    "Worn bushings show up as vague steering, a clunk over expansion joints, or "
    "an alignment that will not hold. On the 911 and Cayman these are wear "
    "items, not failures, and they are worth addressing before they take the "
    "tyres with them."),
   ("Coil-Over Conversion",
    "For an out-of-warranty Cayenne, replacing a failed air system with a "
    "quality coil-over setup is a legitimate option and often the more sensible "
    "one. We will lay out both paths honestly, including what you give up."),
   ("Alignment to Porsche Specification",
    "Alignment done to the factory figures for your model, with corner "
    "balancing available for cars that see track use. Suspension work is not "
    "finished until the geometry is set."),
 ],
 "why_head": ("POR SCHE CHASSIS", "SPECIALISTS"),
 "why_lead": ("The expensive mistake with Porsche suspension is replacing the "
              "part that is complaining rather than the one that failed. A "
              "compressor that burns out is usually the symptom of a strut that "
              "has been leaking for months. We find the cause first and tell "
              "you what we found."),
 "why_points": [
   "Air suspension diagnosis on Cayenne and Panamera before any part is ordered",
   "Ride height sensor calibration after strut or compressor replacement",
   "PASM fault codes read with factory-level diagnostics, not a generic scanner",
   "Control arm and bushing replacement on 911, Boxster, Cayman and Macan",
   "Coil-over conversion offered as an honest alternative on older Cayennes",
   "Alignment to Porsche specification, with corner balancing for track cars",
 ],
 "faq_head": ("PORSCHE SUSPENSION", "FAQ"),
 "faqs": [
   ("Why is my Cayenne sitting low in the morning?",
    "That is the classic sign of a leaking air strut. The system holds the car "
    "up while it is running, but overnight the air escapes and the corner "
    "settles. The compressor then works harder every morning to bring it back, "
    "which is why a neglected leak eventually takes the compressor with it."),
   ("Should I replace air suspension with coil-overs?",
    "It is a reasonable option on an out-of-warranty Cayenne, and plenty of "
    "owners are happier for it. You lose the ride height adjustment and the "
    "adaptive damping, and you gain a system that is far cheaper to keep "
    "working. We will tell you what your car needs either way and let you "
    "decide."),
   ("What is PASM and how do I know if it has failed?",
    "PASM is Porsche's electronically adjustable damping. When a damper or its "
    "wiring fails, the car stores a fault and falls back to a fixed damper "
    "setting. Owners usually describe it as the car feeling flatter, busier or "
    "just less settled than they remember, sometimes with a chassis warning."),
   ("Do you need factory software for suspension work?",
    "For anything involving air suspension or PASM, yes. Ride height sensors "
    "have to be recalibrated after a strut is replaced, and adaptive damper "
    "faults are only readable through the chassis modules. A generic code "
    "reader will not see them."),
   ("How long do Porsche control arm bushings last?",
    "There is no single figure — heat, road surface and how the car is driven "
    "all matter more than mileage. What we look for is play in the joint and "
    "cracking in the rubber. Vague steering, a clunk over bumps, or an "
    "alignment that drifts back out are the usual reasons someone calls."),
   ("Can you align a car that is used on track?",
    "Yes, and we will ask how you use it first. A track alignment and a road "
    "alignment are different compromises, and setting one when you wanted the "
    "other wastes tyres. Corner balancing is available for cars where it is "
    "worth doing."),
 ],
 "cta": ("SOMETHING OFF IN", "THE WAY IT SITS?"),
 "cta_sub": "Call and describe what the car is doing — we will tell you what we would check first.",
},
{
 "slug": "volkswagen-brake-service-snellville-ga.html",
 "donor": "volkswagen-oil-change-snellville-ga.html",
 "brand": "Volkswagen",
 "h1": ("VOLKSWAGEN", "BRAKE", "SERVICE"),
 "title": "Volkswagen Brake Service Snellville GA | German Performance",
 "desc": ("Volkswagen brake service in Snellville, GA. Pads, rotors, electronic "
          "parking brake service mode, wear sensors and fluid flush. "
          "Call (678) 395-7459."),
 "crumb": "Volkswagen Brake Service — Snellville, GA",
 "sub": ("Volkswagen brake service in Snellville, GA — for the Golf, GTI, Golf R, "
         "Jetta, Passat, Tiguan, Atlas and Arteon. Including the electronic "
         "parking brake procedure that rear brakes on most modern VWs cannot be "
         "done without."),
 "cards_head": ("COMPLETE VOLKSWAGEN", "BRAKE SERVICE"),
 "cards_sub": ("Modern Volkswagen brakes are not a purely mechanical job any "
               "more. The rear calipers are driven by motors that have to be "
               "told what is happening."),
 "cards": [
   ("Front and Rear Pads and Rotors",
    "OEM or OEM-equivalent pads and rotors matched to your model. A GTI or "
    "Golf R runs different brake hardware and a different pad compound from a "
    "base Golf, and an Atlas carries far more weight than either."),
   ("Electronic Parking Brake Service Mode",
    "On most VWs from the Mk6 Golf onward, the rear caliper pistons are driven "
    "by electric motors that must be retracted through the factory interface "
    "before the pads come out. Forcing them back mechanically is how those "
    "motors get damaged."),
   ("Brake Wear Sensor Replacement",
    "The wear sensor is a consumable, not a reusable part. We fit a new one "
    "rather than splicing or bypassing the old, so the dashboard warning "
    "continues to mean something on the next set of pads."),
   ("Brake Fluid Flush",
    "Brake fluid absorbs moisture from the air whether the car is driven or "
    "not, which lowers its boiling point and corrodes the system from inside. "
    "Volkswagen calls for a change on a time interval, not a mileage one."),
   ("Caliper Service and Guide Pins",
    "Seized guide pins are a common cause of one pad wearing out well ahead of "
    "its partner. Cleaning and correctly lubricating them is part of the job, "
    "not an upsell."),
   ("Road Test and Bedding In",
    "New pads and rotors need a proper bedding-in cycle to transfer material "
    "evenly. Skipping it is a common cause of the judder that gets blamed on "
    "warped rotors a few thousand miles later."),
 ],
 "why_head": ("VOLKSWAGEN BRAKE", "SPECIALISTS"),
 "why_lead": ("The reason a general shop turns away rear brakes on a modern "
              "Volkswagen — or damages them — is the electronic parking brake. "
              "The caliper pistons are motor-driven and have to be put into "
              "service mode with the right software before anything is touched."),
 "why_points": [
   "Electronic parking brake retracted and reset through factory-level software",
   "Correct pad compound for Golf, GTI, Golf R, Jetta, Passat, Tiguan and Atlas",
   "New wear sensors fitted, never bypassed",
   "Brake fluid changed on Volkswagen's time-based interval",
   "Guide pins cleaned and lubricated as part of every pad replacement",
   "Bedding-in cycle completed on a road test before the car is handed back",
 ],
 "faq_head": ("VOLKSWAGEN BRAKE", "FAQ"),
 "faqs": [
   ("Why do the rear brakes on my VW need a scan tool?",
    "Because the rear caliper pistons are driven by small electric motors "
    "rather than hydraulics alone. They have to be wound back into service mode "
    "through the car's software before the old pads come out, and released "
    "again afterwards. Forcing them back by hand is what damages the actuators, "
    "and that repair costs considerably more than the brake job."),
   ("How often should Volkswagen brake fluid be changed?",
    "Volkswagen specifies brake fluid on a time interval rather than a mileage "
    "one, because the fluid absorbs moisture from the air whether or not the "
    "car is being driven. Two years is the usual figure. A car that sits is "
    "not exempt — if anything it is the more likely candidate."),
   ("My steering wheel shakes when I brake. Are the rotors warped?",
    "Usually not, despite the name everyone uses. What normally causes it is "
    "uneven pad material deposited on the rotor face, often from a set that was "
    "never properly bedded in or from sitting with hot brakes. It feels "
    "identical to warping. We measure the rotor before deciding, because the "
    "two problems have different fixes."),
   ("Do you use OEM or aftermarket brake parts?",
    "We use OEM or OEM-equivalent parts as standard. On brakes the compound "
    "matters more than the badge — the wrong pad on a Golf R will fade under "
    "heat that the correct one shrugs off. If you have a preference or you use "
    "the car on track, tell us and we will talk it through."),
   ("Does a GTI or Golf R need different brakes from a regular Golf?",
    "Yes. Both run larger brake hardware and a pad compound built for more heat "
    "than the base car ever sees. Fitting standard Golf pads to a Golf R is a "
    "cost saving that shows up the first time you use the performance you paid "
    "for."),
   ("Can you do brakes on a Tiguan or Atlas?",
    "Yes. Both are heavier than the cars most people picture when they think of "
    "a Volkswagen, and both go through brakes accordingly. They also use the "
    "electronic parking brake, so the same service-mode procedure applies."),
 ],
 "cta": ("VOLKSWAGEN BRAKES", "GRINDING OR SOFT?"),
 "cta_sub": "Call and tell us what you are hearing or feeling — we will tell you what it usually means.",
},
{
 "slug": "mercedes-cooling-system-snellville-ga.html",
 "donor": "mercedes-oil-change-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "h1": ("MERCEDES", "COOLING", "SYSTEM"),
 "title": "Mercedes Cooling System Repair Snellville | German Performance",
 "desc": ("Mercedes-Benz cooling system repair in Snellville, GA. Thermostats, "
          "water pumps, auxiliary pumps, radiators and MB-spec coolant. "
          "Call (678) 395-7459."),
 "crumb": "Mercedes Cooling System — Snellville, GA",
 "sub": ("Mercedes-Benz cooling system diagnosis and repair in Snellville, GA — "
         "for the C-Class, E-Class, S-Class, GLC, GLE, GLS and Sprinter. "
         "Pressure-tested first, so the part we replace is the one that "
         "actually failed."),
 "cards_head": ("MERCEDES COOLING", "SYSTEM SERVICE"),
 "cards_sub": ("Cooling faults on a Mercedes rarely announce themselves with a "
               "temperature gauge. By the time the needle moves, the damage is "
               "usually already done."),
 "cards": [
   ("Cooling System Pressure Test",
    "The system is pressurised cold and watched, which finds a seep long before "
    "it becomes a puddle. This is where the job starts — coolant disappearing "
    "with nothing on the driveway is the most common way these faults present."),
   ("Thermostat and Housing",
    "Mercedes thermostat housings are plastic and they harden with years of "
    "heat cycling. Many are map-controlled and electrically operated, so they "
    "can fail electrically while still looking perfect."),
   ("Water Pump Replacement",
    "A pump can fail three ways: the seal weeps, the bearing gets noisy, or the "
    "impeller erodes and stops moving coolant while everything still looks dry. "
    "The third is the one that overheats an engine with no warning."),
   ("Auxiliary Electric Water Pump",
    "The small electric pump that keeps coolant moving after shutdown and feeds "
    "the heater circuit is a known failure item across several Mercedes engine "
    "families. It is also cheap to test properly and easy to overlook."),
   ("Radiator, Expansion Tank and Hoses",
    "Expansion tanks crack at the seam and radiator end tanks split where "
    "plastic meets metal. Both leak under pressure and seal themselves when "
    "cold, which is exactly why a cold visual inspection misses them."),
   ("Correct MB-Spec Coolant",
    "Mercedes publishes its own coolant approvals, and mixing specifications or "
    "topping up with a universal product causes corrosion in an aluminium "
    "engine. We fill to the specification listed for your car."),
 ],
 "why_head": ("MERCEDES COOLING", "SPECIALISTS"),
 "why_lead": ("Almost every Mercedes cooling job we see arrives one of two ways: "
              "coolant that keeps disappearing with no visible leak, or a car "
              "that has already overheated once. The first is cheap to solve. "
              "The second is why we would rather see it early."),
 "why_points": [
   "Pressure testing before any part is quoted, not after",
   "Map-controlled thermostats tested electrically with factory-level diagnostics",
   "Auxiliary electric water pump function verified, not assumed",
   "Plastic housings, flanges and expansion tanks inspected as known weak points",
   "MB-approved coolant to the specification listed for your model",
   "System bled properly on refill so no air pocket is left behind",
 ],
 "faq_head": ("MERCEDES COOLING", "FAQ"),
 "faqs": [
   ("Why does my Mercedes lose coolant with no visible leak?",
    "Because most of these leaks only open under pressure and heat, then seal "
    "themselves as the car cools. A hairline crack in an expansion tank or a "
    "weeping plastic flange can lose coolant for months and leave nothing on "
    "the driveway. A cold pressure test is what makes it visible."),
   ("What coolant does a Mercedes take?",
    "Mercedes publishes its own coolant approvals, and the correct one depends "
    "on your model and year. This is one of the places where a universal "
    "product genuinely causes harm — the wrong chemistry attacks aluminium and "
    "the damage shows up as corrosion throughout the system, not as an "
    "immediate fault."),
   ("What is the auxiliary water pump and why does it matter?",
    "It is a small electric pump that circulates coolant independently of the "
    "engine — after shutdown to prevent heat soak, and through the heater "
    "circuit. It is a known failure item on several Mercedes engine families. "
    "A common early sign is a heater that blows cool at idle and warms up once "
    "you are moving."),
   ("My temperature gauge reads normal. Can the cooling system still be a problem?",
    "Yes, and this is the part that catches people out. The gauge on a modern "
    "Mercedes is damped and sits in the middle of its range across a wide band "
    "of real temperatures. By the time it visibly climbs, the system has "
    "usually been struggling for a while. Coolant level and pressure tell the "
    "truth much earlier."),
   ("How often should Mercedes coolant be changed?",
    "Long-life coolant does not last forever — the corrosion inhibitors deplete "
    "with time and heat even though the colour still looks fine. We check its "
    "condition rather than going by appearance, and recommend a change when the "
    "protection has dropped, not on a fixed guess."),
   ("Is it worth fixing a small coolant leak straight away?",
    "On these engines, yes. Cooling faults are cheap while they are a hose, a "
    "flange or a tank, and extremely expensive once an aluminium engine has "
    "been run hot even briefly. This is the clearest example on the car of a "
    "small bill that prevents a large one."),
 ],
 "cta": ("LOSING COOLANT OR", "RUNNING WARM?"),
 "cta_sub": "Call and describe it — coolant faults are cheapest to fix before the gauge ever moves.",
},
]


# Accepted ways each marque names itself in the trust bar.
MARQUE_TOKENS = {
    "Porsche":       ("Porsche",),
    "Volkswagen":    ("Volkswagen", "VW"),
    "Mercedes-Benz": ("Mercedes",),
    "BMW":           ("BMW",),
    "Audi":          ("Audi",),
}



CHECK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><path d="M5 12.5 10 17.5 19 7"/></svg>')


def checks_list(marque=None):
    """The four trust facts, under the hero button where they get read.

    Replaces the old four-cell trust strip. The fourth line names the
    marque when the page has one, so a Porsche page never claims to fit
    BMW parts -- the guarantee the old strip's donor copy kept breaking.
    A page may set "marque": None to keep its brand in the eyebrow while
    the checklist says "factory" (tools/build_general_service_pages.py).
    """
    parts = "Genuine %s parts and fluids" % marque if marque else \
        "Genuine factory parts and fluids"
    items = ["4.5-star Google rating", "Top-rated CARFAX shop",
             "15+ years in business", parts]
    rows = "".join(
        '      <li>%s<span>%s</span></li>\n' % (CHECK_SVG, text) for text in items)
    return '    <ul class="checks fu">\n%s    </ul>' % rows


def skeleton(donor):
    """Nav, mobile menu, trust bar, call bar, NAP grid and footer from a page
    of the same marque, so nothing marque-specific has to be rewritten."""
    src = open(os.path.join(REPO_ROOT, donor), encoding="utf-8").read()

    def grab(pattern):
        match = re.search(pattern, src, re.S)
        if not match:
            raise SystemExit(f"{donor}: no match for {pattern[:40]}")
        return match.group(0)

    return {
        "nav": grab(r"<nav>.*?</nav>"),
        "mob": grab(r'<div id="mobile-menu">.*?\n</div>'),
        "callbar": "",  # the fixed bottom call bar was removed site-wide
        "nap": grab(r'<div class="ic-grid">.*?\n      </div>'),
        "footer": grab(r"<footer>.*?</footer>"),
        "fonts": grab(r'<link rel="stylesheet" href="assets/css/fonts\.css[^>]*>'),
        # Every local stylesheet, in document order. This used to be a
        # range regex from tokens.css to werkstatt.css, which captured all
        # three sheets only while the order was tokens -> site -> werkstatt.
        # The redesign moved the page sheet last, so the range stopped at
        # werkstatt and these pages shipped without site.css at all.
        "css": "\n".join(
            re.findall(r'<link rel="stylesheet" href="assets/css/[^"]+"[^>]*>', src)),
        # Both script tags, so a new page is never missing the tracker.
        "scripts": "\n".join(
            re.findall(r'<script defer src="assets/js/[^"]+"></script>', src)),
    }


def cards_html(items):
    return "\n".join(
        f'    <div class="card"><span class="ci">{i:02d}</span>'
        f'<div class="ct">{title}</div><div class="cd">{body}</div></div>'
        for i, (title, body) in enumerate(items, 1))


def faq_html(items):
    return "\n".join(
        f'      <div class="fi fu"><button class="fq" onclick="toggleFaq(this)">'
        f'{q}<span class="ficon">+</span></button>'
        f'<div class="fa"><p>{a}</p></div></div>'
        for q, a in items)


def build(page, sk):
    line1, line2, line3 = page["h1"]
    ch1, ch2 = page["cards_head"]
    wh1, wh2 = page["why_head"]
    fh1, fh2 = page["faq_head"]
    cta1, cta2 = page["cta"]
    points = "\n".join(f"        <li>{p}</li>" for p in page["why_points"])

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
<body data-page-type="service">

{sk['nav']}
{sk['mob']}
<main>
<div class="breadcrumb"><a href="index.html">Home</a><span>/</span><span style="color:var(--silver)">{page['crumb']}</span></div>
<section class="hero"><div class="hbg"></div><div class="hgrid"></div>
  <div class="hc">
    <div class="eyebrow fu">{page['brand']} Specialists &nbsp;·&nbsp; Snellville, GA &nbsp;·&nbsp;<span class="eyebrow-highlight">4.5★ Rated</span></div>
    <h1 class="fu">{line1}<br><span class="outline">{line2}</span><br><span class="accent">{line3}</span></h1>
    <p class="sub fu">{page['sub']}</p>
    <div class="acts fu"><a href="tel:+16783957459" class="bp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a><a href="index.html#services" class="bg">All Services {ARROW}</a></div>
{checks_list(page.get('marque', page['brand']))}
  </div>
</section>


<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">What You Get</div><h2>{ch1}<br><span style="color:var(--red)">{ch2}</span></h2><p class="sd">{page['cards_sub']}</p></div>
  <div class="g3 fu">
{cards_html(page['cards'])}
  </div>
</section>

<section style="background:var(--black)">
  <div class="two fu">
    <div>
      <div class="sl">Why German Performance</div>
      <h2>{wh1}<br><span style="color:var(--red)">{wh2}</span></h2>
      <p class="sd" style="margin-bottom:0">{page['why_lead']}</p>
      <ul class="cl">
{points}
      </ul>
    </div>
    <div>
      {sk['nap']}
    </div>
  </div>
</section>

<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">Common Questions</div><h2 class="fu">{fh1}<br><span style="color:var(--red)">{fh2}</span></h2></div>
    <div class="faq-list">
{faq_html(page['faqs'])}
    </div>
</section>

<div class="cta-band fu"><div><div class="cbt">{cta1}<br>{cta2}</div><div class="cbs">{page['cta_sub']}</div></div><a href="tel:+16783957459" class="bw"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a></div>

<section style="background:var(--black);padding:80px 60px;text-align:center">
  <div class="fu">
    <div class="sl" style="justify-content:center">Get Started</div>
    <h2 style="margin-bottom:20px">SNELLVILLE'S {page['brand'].upper()} <span style="color:var(--red)">SPECIALISTS</span></h2>
    <p class="sd" style="margin:0 auto 44px;text-align:center;max-width:480px">Serving Snellville, Loganville, Grayson, Lawrenceville, and all of Gwinnett County.</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="tel:+16783957459" class="bp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg><span>Service My Car</span></a>
      <a href="https://maps.google.com/?q=2144+Parkwood+Rd+NW+Snellville+GA+30078" target="_blank" rel="noopener" class="bg">Get Directions {ARROW}</a>
    </div>
  </div>
</section>

</main>
{sk['footer']}
{sk['scripts']}
</body>
</html>
"""


def main():
    written = []
    for page in PAGES:
        sk = skeleton(page["donor"])

        # Assert the hero checklist names this marque rather than trusting
        # that it does -- copying a BMW donor is exactly how "BMW-Approved
        # Parts & Fluids" once shipped on the Porsche hub. Both short and
        # full forms count: the VW pages say "VW" deliberately, which is
        # how the marque writes it.
        page_html = build(page, sk)

        checks = page_html[page_html.find('<ul class="checks'):]
        checks = checks[:checks.find("</ul>")]
        if not any(token in checks for token in MARQUE_TOKENS[page["brand"]]):
            raise SystemExit(
                f"{page['slug']}: hero checklist does not name {page['brand']}")

        path = os.path.join(REPO_ROOT, page["slug"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page_html)
        words = len(re.sub(r"<[^>]+>", " ", page_html).split())
        written.append((page["slug"], words))

    for slug, words in written:
        print(f"  wrote {slug:48s} ~{words} words")
    print(f"\n{len(written)} service pages built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
