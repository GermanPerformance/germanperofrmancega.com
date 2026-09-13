#!/usr/bin/env python3
"""Build three of the make-agnostic category pages the homepage cards link to.

The brake page moved to tools/build_landing_pages.py, the framework every
category page will migrate to; the three here follow it in turn.

The Google Business Profile lists the shop under auto repair, brake shop,
transmission shop and oil change service, and until now the site had a
page for each of those only per make (bmw-transmission-repair, and so on).
These four cover the job for every make the shop works on, the way the
existing tune-up and AC pages already do:

    german-car-repair               the primary category, and the page a
                                    search for the shop's own trade lands on
    german-car-transmission-repair  the money service with no general page
    german-car-oil-change           the most common job anyone books

The skeleton, the template and the checklist come from
tools/build_service_pages.py. The pages set "marque": None, so the eyebrow
reads "German Car Specialists" while the hero checklist says "Genuine
factory parts and fluids" and never names a make it might not fit. Every
technical claim below is a documented characteristic of the marques, and
no page claims a capability the site does not already claim elsewhere.

Run from the repo root:  python3 tools/build_general_service_pages.py
Then tools/apply_redesign.py, which normalises the template's markup.
"""

import os
import re
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

from build_service_pages import build, skeleton  # noqa: E402

REPO_ROOT = os.path.dirname(TOOLS)

# A general page: its NAP grid and footer name no marque.
DONOR = "german-car-tune-up-snellville-ga.html"
BRAND = "German Car"
MAKES = "BMW, Mercedes-Benz, Audi, Porsche and Volkswagen"

MARQUE_RE = re.compile(r"BMW|Mercedes|Audi|Porsche|Volkswagen|\bVW\b")

PAGES = [
{
 "slug": "german-car-repair-snellville-ga.html",
 "donor": DONOR, "brand": BRAND, "marque": None,
 "h1": ("GERMAN AUTO", "REPAIR", "&amp; SERVICE"),
 "title": "German Auto Repair Snellville GA | German Performance",
 "desc": ("German auto repair in Snellville, GA for BMW, Mercedes, Audi, "
          "Porsche and VW: factory diagnostics, engine, electrical and "
          "suspension. Call (678) 395-7459."),
 "sub": (f"Repair and service for {MAKES} in Snellville, GA. Diagnosis on the "
         "factory software for your make, a written estimate before any part "
         "is ordered, and the work done to the specification the car was "
         "built to."),
 "cards_head": ("WHAT WE", "REPAIR"),
 "cards_sub": ("A German car tells you what is wrong in more detail than most, "
               "if the tools can read it. Every repair here starts by reading "
               "the car properly, and ends with the fault gone rather than the "
               "light off."),
 "cards": [
   ("Factory-Level Diagnostics",
    "ISTA for BMW, XENTRY for Mercedes-Benz, ODIS for Audi and Volkswagen, "
    "PIWIS for Porsche. A generic scanner reads the engine module and little "
    "else; the factory software reads every control unit on the car, with the "
    "live data and the guided tests that come with it."),
   ("Engine Repair",
    "Oil leaks from valve cover, oil filter housing and timing cover gaskets, "
    "timing chain guides, PCV valves, water pumps, high-pressure fuel pumps "
    "and injectors. The failures on each engine family are well documented, "
    "and so are the right parts to fix them."),
   ("Electrical and Module Faults",
    "Battery and charging faults, wiring and connector damage, failed control "
    "modules and the coding and programming that follow a replacement. A new "
    "module on a modern German car is not working until it is coded to the "
    "vehicle."),
   ("Cooling System",
    "Plastic radiators, expansion tanks, thermostats and electric water pumps "
    "age on a schedule. We pressure-test the system, find the leak rather than "
    "guess at it, and replace what has failed with OEM or OEM-equivalent "
    "parts."),
   ("Suspension and Steering",
    "Control arm bushings, ball joints, tie rods, shocks, struts and air "
    "suspension components, then a four-wheel alignment to the factory "
    "specification once the parts are in. Worn bushings are the most common "
    "cause of the clunks and wander owners report."),
   ("Drivetrain and Differential",
    "Driveshaft center bearings and flex discs, CV axles and boots, "
    "differential and transfer case fluid services and seals. Fluids the "
    "manufacturer once called lifetime still wear, and the units they protect "
    "are expensive to replace."),
 ],
 "why_head": ("REPAIRED THE WAY", "IT WAS BUILT"),
 "why_lead": ("Most bad experiences with German car repair come from a shop "
              "treating the car like any other. It is not. The tools, the "
              "specifications and the parts are specific, and following them "
              "is the difference between a repair that holds and one that "
              "comes back."),
 "why_points": [
   f"Factory diagnostic software for {MAKES}",
   "OEM or OEM-equivalent parts, matched to the chassis and build date",
   "A written estimate before work starts, and a call before anything changes",
   "Torque specifications and one-time-use fasteners followed as the manufacturer publishes them",
   "Fluids to the approval the manufacturer lists, never a generic equivalent",
   "A one-year service warranty on the work we perform",
 ],
 "faq_head": ("GERMAN AUTO REPAIR", "FAQ"),
 "faqs": [
   ("Do you work on all German makes?",
    "Yes. BMW and MINI, Mercedes-Benz, Audi, Porsche and Volkswagen are what "
    "the shop is set up for, with the factory-level diagnostic software for "
    "each. If you drive something else German, call and ask; we will tell you "
    "honestly whether we are the right shop for it."),
   ("Will an independent shop void my warranty?",
    "No. Federal law protects your right to have maintenance and repairs "
    "performed by an independent shop without voiding a manufacturer warranty, "
    "as long as the correct parts and fluids are used and the work is "
    "documented. You leave with a written record of what was done."),
   ("Do you use genuine parts?",
    "We use genuine or OEM-equivalent parts, which means parts made by the "
    "supplier that builds them for the factory, or by a manufacturer that "
    "meets the same specification. Where a genuine part is the only right "
    "choice, that is what goes on the car, and the estimate says so."),
   ("Can you read the same fault codes the dealer can?",
    "Yes. We run the factory diagnostic platforms rather than a generic "
    "scanner, so we see every control unit the dealer sees, with the same live "
    "data, guided tests and coding functions. That is what makes the "
    "difference on an intermittent electrical fault."),
   ("How do you estimate a repair?",
    "Diagnosis first, then a written estimate that lists the parts and the "
    "labor before anything is ordered. If something changes once the car is "
    "apart, you get a call and a choice, not a surprise on the invoice."),
   ("Do you offer a warranty on repairs?",
    "Yes. The work we perform carries a one-year service warranty. Keep the "
    "invoice: it is the record the warranty runs on, and the one a future "
    "buyer will ask to see."),
 ],
 "cta": ("SOMETHING NOT RIGHT", "WITH YOUR CAR?"),
 "cta_sub": "Call and tell us what it is doing. We will tell you what the diagnosis involves and what happens next.",
},
{
 "slug": "german-car-transmission-repair-snellville-ga.html",
 "donor": DONOR, "brand": BRAND, "marque": None,
 "h1": ("GERMAN CAR", "TRANSMISSION", "REPAIR"),
 "title": "German Car Transmission Repair Snellville | German Performance",
 "desc": ("German car transmission repair in Snellville, GA: fluid and filter "
          "service, mechatronic and valve body faults, DSG and PDK work. "
          "Call (678) 395-7459."),
 "sub": (f"Transmission service and repair for {MAKES} in Snellville, GA. "
         "Fluid and filter at the real interval, the electronic faults that "
         "cause most complaints, and the adaptations that make a repair feel "
         "like new."),
 "cards_head": ("WHAT A GERMAN", "TRANSMISSION NEEDS"),
 "cards_sub": ("The transmissions in these cars are excellent, and most of "
               "their reputation for trouble comes from the word lifetime on "
               "the fluid. Serviced on time and diagnosed properly, the "
               "majority never need to come out of the car."),
 "cards": [
   ("Fluid and Filter Service",
    "ZF, Mercedes-Benz 7G and 9G, Aisin and Porsche PDK units all have a fluid "
    "the manufacturer once called lifetime and a filter built into the pan. "
    "Fluid degrades; we replace it and the filter with the specified fluid, "
    "filled and level-checked at the temperature the procedure requires."),
   ("Mechatronic and Valve Body",
    "Harsh shifts, flares between gears and gearbox warnings very often trace "
    "to the valve body and its solenoids or the mechatronic unit rather than "
    "the gearbox itself. Diagnosed with the factory software, that is a "
    "repair, not a rebuild."),
   ("Adaptation and Software",
    "Modern transmissions learn how they shift. After a fluid service or a "
    "repair the adaptations are reset and relearned through the factory "
    "diagnostic interface, and the software updates the manufacturer has "
    "released for shift quality are applied where they exist."),
   ("DSG and PDK Service",
    "Volkswagen and Audi DSG and S tronic, BMW DCT and Porsche PDK use wet "
    "clutches that share their fluid with the gearbox. Each carries a "
    "published fluid interval, 40,000 miles on the common DSG units, and "
    "skipping it is the most common way to shorten their life."),
   ("Torque Converter and Shudder",
    "A shudder at light throttle is usually the torque converter's lock-up "
    "clutch, and it often responds to a fluid service before it becomes a "
    "converter. We diagnose it on the road and with live data, and tell you "
    "which one you are looking at."),
   ("Leaks, Seals and Mounts",
    "Pan gaskets, the plastic sleeve where the wiring harness enters the case, "
    "cooler lines and output seals are the usual leak points, and a worn "
    "transmission mount makes a good gearbox feel rough. All of them are "
    "routine to put right."),
 ],
 "why_head": ("DIAGNOSED BEFORE", "IT IS REBUILT"),
 "why_lead": ("The expensive mistake with a German transmission is replacing "
              "it for a fault that lives in the valve body, the software or "
              "the fluid. We read the car properly first, so the repair "
              "matches the fault and nothing more."),
 "why_points": [
   "Factory diagnostic software for the transmission control unit, with live data and adaptation values",
   "Fluid and filter services with the specified fluid, filled at the correct temperature",
   "Valve body, mechatronic and solenoid repairs where the fault is electronic",
   "DSG, DCT and PDK clutch-pack fluid services at the published interval",
   "Adaptations reset and relearned after every service and repair",
   "A road test with live data before the car is handed back",
 ],
 "faq_head": ("TRANSMISSION", "FAQ"),
 "faqs": [
   ("My transmission fluid is supposed to be lifetime. Does it really need changing?",
    "ZF, which builds the automatics in most BMW models and many Audi and "
    "Porsche models, publishes its own interval of roughly 50,000 to 75,000 "
    "miles for the fluid the car makers once called lifetime. Fluid degrades "
    "with heat and mileage whatever the label says, and the unit it protects "
    "costs far more than the service."),
   ("What does a slipping or jerking shift usually mean?",
    "On a German automatic it most often means the fluid is degraded, the "
    "valve body or mechatronic unit has a fault, or the adaptations have "
    "drifted. All three are diagnosed with the factory software and live "
    "data. A worn-out gearbox is the least common cause, not the first "
    "assumption."),
   ("Do you service DSG and PDK transmissions?",
    "Yes. Volkswagen and Audi DSG and S tronic, BMW DCT and Porsche PDK all "
    "carry a fixed fluid and filter interval, 40,000 miles on the common "
    "Volkswagen and Audi units, and use a fill procedure that depends on "
    "temperature. We follow the factory procedure for each."),
   ("Can you repair the transmission rather than replace it?",
    "Very often. Valve bodies, solenoids, mechatronic units, seals, cooler "
    "lines and mounts are all repairable in the car. When the internal "
    "clutches or hard parts are worn we will tell you, show you the evidence, "
    "and go through the options for a rebuilt or a replacement unit."),
   ("Why does the car need to relearn after a transmission service?",
    "Modern transmissions adjust their shift points and pressures as the "
    "clutches wear. After new fluid or a repair those learned values are "
    "wrong for the new condition, so they are reset through the factory "
    "interface and the gearbox relearns on the road test. Skipping that step "
    "is why some services feel worse before they feel better."),
   ("Will a transmission service fix a shudder?",
    "Sometimes. A shudder at light throttle is usually the torque converter's "
    "lock-up clutch, and degraded fluid is a common cause. A fluid service "
    "with the specified fluid is the first step; if the shudder stays, the "
    "converter is the next conversation, and we will have diagnosed it rather "
    "than guessed."),
 ],
 "cta": ("SLIPPING, JERKING", "OR STUCK IN GEAR?"),
 "cta_sub": "Call and tell us the make, model and what the car is doing. We will tell you what the diagnosis involves.",
},
{
 "slug": "german-car-oil-change-snellville-ga.html",
 "donor": DONOR, "brand": BRAND, "marque": None,
 "h1": ("GERMAN CAR", "OIL", "CHANGE"),
 "title": "German Car Oil Change Snellville GA | German Performance",
 "desc": ("German car oil change in Snellville, GA: approved oil, OEM filter "
          "and a service reset for BMW, Mercedes, Audi, Porsche and VW. "
          "Call (678) 395-7459."),
 "sub": (f"Oil service for {MAKES} in Snellville, GA. The oil carrying the "
         "approval your engine lists, an OEM filter with new seals, the level "
         "checked the way the car requires, and the reminder reset through "
         "the factory interface."),
 "cards_head": ("A PROPER GERMAN", "OIL SERVICE"),
 "cards_sub": ("Every German manufacturer publishes its own oil approvals, its "
               "own capacities and its own reset procedure. An oil change that "
               "ignores them is cheaper for a reason."),
 "cards": [
   ("Approved Oil for Your Engine",
    "BMW Longlife-01 and LL-04, Mercedes-Benz 229.5 and 229.51, VW 502 00, "
    "504 00 and 507 00, Porsche A40 and C40. The approval on the bottle "
    "matters more than the brand, and the wrong one is the fastest way to a "
    "clogged particulate filter or a timing chain that stretches early."),
   ("OEM Filter and Seals",
    "A cartridge filter from the manufacturer's supplier, with the new O-rings "
    "and crush washer that come with it. Reused seals and cheap filter media "
    "are where the leaks and the low-pressure warnings come from."),
   ("Correct Fill and Level Check",
    "Capacities on these engines run from six to more than ten quarts, and "
    "many modern models have no dipstick. We fill to the published capacity "
    "and confirm the level electronically with the engine at the temperature "
    "the procedure specifies."),
   ("Service Reset",
    "The service reminder and the condition-based service data are reset "
    "through the factory interface, so the car's own schedule stays accurate. "
    "A generic tool clears the message and leaves the counter wrong."),
   ("Multi-Point Inspection",
    "While the car is on the lift we look at the things an oil change is the "
    "cheapest chance to catch: leaks, boots, belts, tires, brake wear and the "
    "state of the old oil and filter. Anything we find goes on the invoice, "
    "whether or not you act on it."),
   ("Interval Advice",
    "Every German manufacturer publishes a mileage-or-time interval, and most "
    "of these engines are better served on the shorter end when the car makes "
    "short trips or sits. We will tell you what the manufacturer says and "
    "what we would do with your car."),
 ],
 "why_head": ("MORE THAN A", "DRAIN AND FILL"),
 "why_lead": ("The oil change is the one service every owner buys, and the one "
              "where the corners are easiest to cut. The right approval, the "
              "right fill and the right reset cost a little more, and they "
              "are the reason these engines reach the mileage they were built "
              "for."),
 "why_points": [
   "Oil carrying the exact manufacturer approval your engine lists, matched to model and year",
   "OEM or OEM-equivalent cartridge filters with new seals every time",
   "Filled to the published capacity and level-checked electronically where there is no dipstick",
   "Service reminder and condition-based service data reset through the factory interface",
   "Old oil and filter inspected for metal and coolant, and reported to you",
   "Multi-point inspection while the car is up on the lift",
 ],
 "faq_head": ("OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a German car need an oil change?",
    "The published intervals run from 10,000 miles or one year on most "
    "current models to longer on some. Short trips, heat, towing and long "
    "periods parked are all harder on oil than steady mileage, so cars used "
    "that way are better served sooner. If the car is driven rarely, the time "
    "limit matters more than the mileage."),
   ("What oil does my car take?",
    "It depends on the engine and the year, and the answer is an approval "
    "code rather than a brand: BMW LL-01 or LL-04, Mercedes-Benz 229.5 or "
    "229.51, VW 502 00, 504 00 or 507 00, Porsche A40 or C40, among others. "
    "We look up the approval for your exact car and fill that. An oil that "
    "meets a general industry standard can still be wrong for the engine."),
   ("Why is a German car oil change more involved than a quick-lube one?",
    "Capacity, approval and procedure. These engines hold more oil, the oil "
    "has to carry a specific manufacturer approval, the filter is a cartridge "
    "with its own seals, and many cars need the level confirmed "
    "electronically at temperature and the reminder reset with factory "
    "tools. None of that happens in a ten-minute bay."),
   ("Can you reset the service reminder?",
    "Yes. We reset it through the factory-level interface so the car's own "
    "maintenance schedule stays accurate, rather than clearing the message "
    "with a generic tool and leaving the underlying counter wrong."),
   ("Do you check anything else during an oil change?",
    "Yes. The car gets a multi-point inspection while it is on the lift: "
    "leaks, boots, belts, tires, brake wear, and the condition of the old oil "
    "and filter. We also check the magnetic drain plug and the filter media "
    "for metal, which is the cheapest early warning any engine gives you."),
   ("Will an independent oil change affect my warranty?",
    "No. Federal law protects your right to have routine maintenance "
    "performed by an independent shop without voiding a manufacturer "
    "warranty, as long as the correct specification parts and fluids are "
    "used and the work is documented. You leave with a written record of "
    "what was done."),
 ],
 "cta": ("OIL SERVICE", "DUE?"),
 "cta_sub": "Call and tell us the make, model and year. We will confirm the approval your engine needs.",
},
]


def hero_checks(page_html):
    start = page_html.find('<ul class="checks')
    return page_html[start:page_html.find("</ul>", start)]


def main():
    sk = skeleton(DONOR)
    written = []
    for page in PAGES:
        page_html = build(page, sk)

        # The inverse of build_service_pages' guard: a make-agnostic page
        # must say "factory" and must not name a marque it might not fit.
        checks = hero_checks(page_html)
        if "Genuine factory parts and fluids" not in checks or MARQUE_RE.search(checks):
            raise SystemExit(f"{page['slug']}: hero checklist names a marque")

        path = os.path.join(REPO_ROOT, page["slug"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page_html)
        words = len(re.sub(r"<[^>]+>", " ", page_html).split())
        written.append((page["slug"], words))

    for slug, words in written:
        print(f"  wrote {slug:52s} ~{words} words")
    print(f"\n{len(written)} general service pages built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
