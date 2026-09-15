"""The Mercedes-Benz guides: four articles that support the Mercedes-Benz hub.

Maintenance, symptoms and diagnosis, what moves the bill, and case
studies. Every technical claim is a documented characteristic of the
marque or is already on the site; see posts/common.py for the facts the
closing note may state and for how the case studies are framed. No
prices, on purpose.
"""

import posts.sources as src
from posts.common import (  # noqa: F401
    AC, BRAKES, CEL, DEALER, INSPECTION, MB_AIRMATIC as AIRMATIC, MB_CASES as CASES,
    MB_COSTS as COSTS, MB_SERVICE_AB as SERVICE_AB, MERCEDES_HUB, OIL, TRANSMISSION, link,
)
from posts.mercedes_cases import POST as CASES_POST

CLUSTER = "mercedes"
HUB = MERCEDES_HUB
EYEBROW = "Mercedes Repair Guide"

POST_DATES = {
    SERVICE_AB: ("2026-09-15", "2026-09-15"),
    AIRMATIC: ("2026-09-15", "2026-09-15"),
    COSTS: ("2026-09-15", "2026-09-15"),
    CASES: ("2026-09-15", "2026-09-15"),
}

READING = {
    SERVICE_AB: "Mercedes Service A vs Service B",
    AIRMATIC: "Mercedes AIRMATIC Problems Explained",
    COSTS: "Why Mercedes Repair Costs What It Does",
    CASES: "Mercedes Repair Case Studies",
}

SUMMARY = {
    SERVICE_AB: "What ASSYST Plus counts, what each service actually includes, the oil sheet your engine needs, and what we inspect that the sheet does not list.",
    AIRMATIC: "Why a Mercedes sits low on one corner, which component is at fault, and how XENTRY and a fill test tell a strut from a compressor.",
    COSTS: "Genuine vs OE-supplier parts, sealed assemblies, access labor, the XENTRY factor and whole-assembly quotes for repairable faults. No prices.",
    CASES: "Three representative jobs: an M272 oil smell with coolant loss, a GL450 low on one corner, and a 722.9 in limp mode that did not need a transmission.",
}

HUB_LINK = link(HUB, "Mercedes repair in Snellville")

POSTS = [
    {
        "slug": SERVICE_AB,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.MB_MANUALS, src.MB_FLUIDS, src.FTC_WARRANTY],
        "title": "Mercedes Service A vs Service B | German Performance",
        "description": (
            "What ASSYST Plus counts, what Service A and Service B include, the "
            "oil sheet your engine needs, and what German Performance inspects "
            "that the sheet leaves out."),
        "eyebrow": EYEBROW,
        "h1": 'Mercedes Service A <span class="accent">vs Service B</span>',
        "dek": (
            "The dash says \"Service B due\". Here is what that means, what "
            "each service includes, why the letter matters less than the "
            "engine under the hood, and what we look at that the sheet leaves "
            "out."),
        "intro": (
            f"Every Mercedes-Benz built since the late 1990s carries a service "
            f"computer, ASSYST and later ASSYST Plus, that counts down to the "
            f"next service and names it with a letter. Owners bring the letter "
            f"to us for {HUB_LINK} and ask what it costs; we ask what engine it "
            f"is, because the letter is only the outline. This guide explains "
            f"how the system counts, what Service A and Service B actually "
            f"cover, which oil and fluid approvals your particular engine and "
            f"transmission were built for, and the inspection items we add "
            f"because the cars that come through here have taught us to."),
        "sections": [
            ("How ASSYST Plus decides what is due", [
                "ASSYST Plus keeps a countdown in miles and in days and shows "
                "whichever runs out first, with the letter of the service that "
                "is next. On the cars sold here the pattern is one service a "
                "year or every 10,000 miles, alternating A and B: A at the "
                "first year, B at the second, A at the third and so on. The "
                "counter is reset by the technician after the work, through "
                "the cluster or through XENTRY, and the reset records which "
                "service was performed; a car whose display shows an A when "
                "it should show a B has usually been reset by hand without "
                "the work behind it.",
                "The system is honest about time, which matters more than "
                "owners expect. A Mercedes-Benz that covers 4,000 miles a "
                "year still needs the oil changed annually, because engine oil "
                "degrades with heat cycles and moisture, not only with "
                "distance. The countdown will reach zero on the calendar long "
                "before it reaches zero on the odometer, and it is right to.",
            ]),
            ("What Service A includes", [
                "Service A is the smaller of the two. Engine oil and filter "
                "to the approved sheet; a check and correction of every fluid "
                "level; tire pressures and condition; a brake inspection of "
                "pads, rotors and lines; a check of the lights, wipers and "
                "washers; the service reminder reset. On most engines since "
                "the mid-2000s the oil filter is a paper cartridge in a "
                "housing on top of the engine rather than a spin-on canister, "
                "and the housing's O-rings are replaced with it. Most of "
                "these cars also have no dipstick; the level is read through "
                "the cluster once the engine is warm, and we verify it that "
                "way after the fill.",
                f"The oil is the part that is easy to get wrong. Mercedes-Benz "
                f"approves oils by sheet number, and the sheet is printed in "
                f"the booklet and on the cap of any oil that holds the "
                f"approval. Most gasoline engines from the M272 and M273 era "
                f"onward call for MB 229.5; the newer direct-injection M276 "
                f"and M278, and the four-cylinder M274, are typically listed "
                f"for 229.5 or the low-ash 229.51 and 229.52, which the "
                f"catalysts and particulate filters on later cars depend on; "
                f"the current M256 and M264 families moved to the thinner "
                f"229.71. The number is not a formality. Our "
                f"{link(OIL, 'German car oil change')} page explains what we "
                f"fill with; on a Mercedes-Benz we look the engine code up "
                f"in the operating-fluids list linked in the sources below, "
                f"not the badge on the trunk.",
            ]),
            ("What Service B adds", [
                "Service B is Service A plus the two-year items. Brake fluid "
                "is the important one: Mercedes-Benz specifies a DOT 4 Plus "
                "fluid changed every two years, because brake fluid absorbs "
                "water from the air whether the car is driven or not, and "
                "water in the fluid lowers its boiling point and corrodes the "
                "ABS and stability-control hydraulics from the inside. The "
                "cabin (combination) filter is replaced. The engine air "
                "filter is inspected and replaced by the booklet's interval. "
                "The inspection is longer: suspension and steering "
                "components, the exhaust, the underbody, the drive belt and "
                "its tensioner, the cooling system and the battery.",
                f"Some items are neither A nor B but sit on their own "
                f"mileage in the booklet: spark plugs, the fuel filter on "
                f"older cars, the transmission fluid on many. This is why the "
                f"letter is only an outline. Two cars can both be due a "
                f"Service B and one of them is also due plugs and a "
                f"transmission service, which changes the day considerably. "
                f"Mercedes-Benz USA publishes the maintenance booklet for "
                f"every model year on the page in the sources; it is worth "
                f"ten minutes with your own.",
            ]),
            ("The transmission fluid is not lifetime", [
                f"The 7G-TRONIC (the 722.9, fitted from 2003) and the "
                f"9G-TRONIC that followed were both described as sealed for "
                f"life when new. The maintenance booklets have since put a "
                f"mileage on the fluid and filter for most of these cars, "
                f"and our experience is that the interval is the difference "
                f"between a transmission that lasts and one that does not. "
                f"The 722.9's electronic control unit, the conductor plate, "
                f"sits in the fluid, and old fluid takes its speed sensors "
                f"and the valve body with it. A service here is fluid to the "
                f"approved sheet, the filter, the pan gasket and, on the "
                f"722.9, the level set by temperature with XENTRY, because the "
                f"correct level is only correct at one fluid temperature. The "
                f"{link(TRANSMISSION, 'transmission repair')} page covers "
                f"what we do when it has been left too long.",
                "The older 722.6 five-speed has one more item of its own: the "
                "electrical connector on the side of the case has an O-ring "
                "that hardens and lets fluid wick up the harness into the "
                "transmission control module. We check it at every service "
                "on those cars, because the fix while it is a seal is trivial "
                "and the fix once it is a module is not.",
            ]),
            ("What we inspect that the sheet does not list", [
                "The booklet was written for a new car. The cars we see are "
                "not new, and each engine family has a short list of things "
                "that happen to it that no service sheet mentions. We look for "
                "them at every A and B, and we photograph what we find.",
                ("list", [
                    "<strong>M272 and M273 (2005&ndash;2012 V6 and V8):</strong> "
                    "the engine-oil cooler seals in the valley between the "
                    "heads, which weep oil down the back of the engine and "
                    "smell of it after a drive; the intake-manifold swirl "
                    "flaps; and on the early M272, the balance-shaft sprocket, "
                    "which shows itself as camshaft-correlation codes before "
                    "anything else. We covered the first of these in the "
                    "case studies.",
                    "<strong>M276 and M278 (2011 on, direct injection):</strong> "
                    "timing-chain and camshaft-adjuster noise on cold start, "
                    "and the turbocharger oil-feed lines on the M278.",
                    "<strong>Every engine:</strong> the plastic thermostat "
                    "housing and expansion tank, the electric auxiliary "
                    "coolant pump on cars that have one, and the drive belt's "
                    "tensioner, which fails before the belt does.",
                    "<strong>The camshaft-adjuster magnets:</strong> which can "
                    "weep oil into their own connector and along the harness "
                    "to the engine control module. A drop of oil in the "
                    "connector is a cheap fix. A module full of it is not.",
                    "<strong>AIRMATIC cars:</strong> ride height at all four "
                    "corners after the car has sat, and the compressor's "
                    "run-time counter in XENTRY. The dedicated guide below "
                    "explains why.",
                    "<strong>Cars with SBC brakes (the 2003&ndash;2006 E-Class and "
                    "CLS, and the SL of that era):</strong> the pump's activation count, which XENTRY "
                    "reports and which sets the unit's remaining life.",
                    f"<strong>The battery and the auxiliary battery:</strong> "
                    f"tested under load; a weak one on a modern Mercedes-Benz "
                    f"produces warnings that have nothing to do with the "
                    f"battery.",
                ]),
            ]),
            ("A vs B, side by side", [
                "A summary of the two services as we perform them. Your "
                "booklet is the reference for what Mercedes-Benz itself "
                "specifies for your model year; the added inspection is ours.",
                ("table", (
                    ("Item", "Service A", "Service B"),
                    (
                        ("Interval", "Year 1, 3, 5 &hellip; or every 10,000 mi", "Year 2, 4, 6 &hellip; or every 20,000 mi"),
                        ("Engine oil and cartridge filter", "Yes, to the approved MB sheet", "Yes, to the approved MB sheet"),
                        ("Fluid levels, tires, lights, wipers", "Checked and corrected", "Checked and corrected"),
                        ("Brake inspection", "Pads, rotors, lines", "Pads, rotors, lines, parking brake"),
                        ("Brake fluid", "&mdash;", "Replaced, DOT 4 Plus, every 2 years"),
                        ("Cabin filter", "&mdash;", "Replaced"),
                        ("Engine air filter", "Inspected", "Inspected; replaced by the booklet interval"),
                        ("Suspension, steering, exhaust, underbody", "&mdash;", "Inspected"),
                        ("Drive belt and tensioner", "&mdash;", "Inspected"),
                        ("Battery", "&mdash;", "Load-tested"),
                        ("Our added inspection (valley seals, plastics, adjusters, AIRMATIC)", "Yes, photographed", "Yes, photographed"),
                        ("Spark plugs, transmission fluid, coolant", "By the booklet's own mileage", "By the booklet's own mileage"),
                        ("Service reminder", "Reset, recorded as A", "Reset, recorded as B"),
                    ),
                )),
            ]),
            ("Does an independent service keep the warranty?", [
                f"Yes. Federal law prevents a manufacturer from denying "
                f"warranty coverage because routine maintenance or repairs "
                f"were done by an independent shop, provided the work meets "
                f"the specification; the FTC's page in the sources says so "
                f"in plain English. Our technicians are Mercedes-Benz "
                f"factory-trained, the fluids meet the sheet, the reset is "
                f"recorded in the car the same way the dealer records it, and "
                f"we report the service to CARFAX. The fuller comparison is "
                f"in {link(DEALER, 'dealership vs. independent shop')}.",
                f"If the display says a service is due and you are not sure "
                f"which, or what else the engine is due for, call with the "
                f"year and the model. We will tell you what the day should "
                f"involve before you bring the car in. Everything above is "
                f"part of {link(HUB, 'the Mercedes work we do every day')}.",
            ]),
        ],
        "further": [AIRMATIC, COSTS, CASES],
        "cta_heading": "Service light on?",
        "cta_text": "Bring the car and the booklet. We will do the service the sheet lists, inspect what it does not, and give you a written report with photographs.",
    },
    {
        "slug": AIRMATIC,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.MB_MANUALS, src.NHTSA_RECALLS, src.CARFAX],
        "title": "Mercedes AIRMATIC Problems Explained | German Performance",
        "description": (
            "Why a Mercedes-Benz sits low on one corner, which AIRMATIC part is "
            "at fault, and how German Performance tells a strut from a compressor "
            "before quoting."),
        "eyebrow": EYEBROW,
        "h1": 'Mercedes AIRMATIC Problems <span class="accent">Explained</span>',
        "dek": (
            "Symptoms, the parts behind them, and the tests that tell them "
            "apart. Most AIRMATIC repairs are one component. The expensive "
            "mistake is replacing the wrong one."),
        "intro": (
            f"AIRMATIC is Mercedes-Benz's air suspension: a rubber air spring "
            f"at each corner in place of a steel coil, a compressor to fill "
            f"them, and a control module that keeps the car level and adjusts "
            f"the damping. It rides beautifully when it works, and it is the "
            f"most common suspension complaint that comes to us for "
            f"{HUB_LINK}. It is also the system where a wrong diagnosis costs "
            f"the most, because the parts are not cheap and there are several "
            f"of them. This guide explains the symptoms, which component each "
            f"one points at, how we isolate it with XENTRY and a few simple "
            f"tests, and when a conversion to steel springs is worth "
            f"discussing."),
        "sections": [
            ("Which cars have it", [
                "AIRMATIC came in on the W220 S-Class in the late 1990s and "
                "spread across the range: the S-Class and CLS, the E-Class "
                "(standard at the rear on the wagons, optional elsewhere), "
                "the ML, GL, GLE and GLS, the R-Class, and later the C-Class "
                "and others as an option. The GL and GLS have had it as "
                "standard equipment, which is why so many of the cases we see "
                "are those. Not every Mercedes-Benz that rides on air is "
                "AIRMATIC: the S-Class, CL and SL of the same years could be "
                "ordered with Active Body Control, ABC, which is a hydraulic "
                "system with its own pump, accumulators and struts, and a "
                "different set of faults. If your car has ABC, the tests "
                "below do not apply and we diagnose it separately.",
            ]),
            ("The symptoms, and what each one points at", [
                ("h3", "One corner is low in the morning and rises when you drive"),
                "The most common complaint and the most misread. A car that "
                "can be lifted is a car with a working compressor and a "
                "leak. The leak is almost always the air spring itself, "
                "usually at the fold where the rubber bellows rolls over the "
                "piston, and occasionally a line or a fitting at the valve "
                "block. The corner that drops is the one leaking. The "
                "compressor is running every morning to make up for it, and "
                "if the leak is left long enough the compressor will "
                "eventually fail from overwork, which is how the two get "
                "confused.",
                ("h3", "The whole car is low and will not rise"),
                "Now the compressor is the suspect, or its relay, which "
                "fails more often than the compressor and is a fraction of "
                "the job. A compressor that runs but cannot build pressure "
                "has worn its piston ring; one that does not run at all "
                "usually has a relay or a fuse first. A thermal cut-out "
                "after a long run is also common: the car sits low after a "
                "drive with the compressor working hard, then rises after it "
                "cools.",
                ("h3", "The compressor runs for a long time, or often"),
                "A leak somewhere, being made up for. This is the symptom to "
                "act on early, because it is the one that turns a strut "
                "replacement into a strut and compressor replacement.",
                ("h3", "\"AIRMATIC: Visit Workshop\" or \"Vehicle too low: Stop\" on the dash"),
                "The control module has seen a ride height it cannot correct, "
                "a pressure it cannot reach, or a sensor it cannot trust. The "
                "message tells you the module is unhappy; the fault memory "
                "tells you why, and the codes are specific enough to name a "
                "corner or a circuit.",
                ("h3", "Harsh, bouncy or floaty ride with normal height"),
                "The damping side of the system rather than the air side. The "
                "adaptive dampers are controlled by valves that can fail "
                "electrically, and the strut's damper can wear out the way "
                "any damper does. A strut that has lost damping but still "
                "holds air will pass every leak test.",
                ("h3", "Leaning after a wheel or suspension job"),
                "Usually a level sensor or its linkage disturbed on the way "
                "in, or the calibration not done afterwards. Cheap to fix, "
                "and worth ruling out before anything is bought.",
            ]),
            ("The components", [
                ("list", [
                    "<strong>Air springs and struts.</strong> At the front the "
                    "air spring and damper are one unit, the strut; at the "
                    "rear on most models the spring is a separate bellows "
                    "over a conventional damper. The rubber ages with heat, "
                    "ozone and mileage, and cracks at the rolling fold.",
                    "<strong>The compressor and its relay.</strong> A small "
                    "piston pump with a dryer; the relay switches it, and "
                    "fails first.",
                    "<strong>The valve block.</strong> Distributes air to each "
                    "corner and holds it there; its O-rings and solenoids can "
                    "leak or stick.",
                    "<strong>Level sensors.</strong> One per corner (or per "
                    "axle on some cars), a small arm on a linkage that tells "
                    "the module the ride height.",
                    "<strong>The lines.</strong> Plastic, run through the "
                    "underbody, and vulnerable at the fittings.",
                    "<strong>The damping valves and the control module.</strong> "
                    "Electrical, and diagnosed through XENTRY rather than "
                    "with soap.",
                ]),
            ]),
            ("How we isolate it", [
                f"Every AIRMATIC diagnosis starts the same way, whatever the "
                f"owner has been told. We read the AIRMATIC module's fault "
                f"memory with XENTRY, the factory software, and look at the "
                f"live data: the four ride heights, the reservoir pressure, "
                f"the compressor's run time and its temperature. Then we use "
                f"XENTRY's actuations to raise and lower each corner "
                f"individually and watch what the sensors report. A corner "
                f"that will not hold its height with the valve closed has a "
                f"leak downstream of the valve block, which means the spring "
                f"or its line. A system that cannot reach pressure has a "
                f"compressor or supply-side problem. A sensor that reads a "
                f"height that does not match a tape measure is the sensor.",
                "Only then do we go under the car. A leaking spring is "
                "confirmed with soapy water on the bellows, which bubbles at "
                "the crack; lines and fittings the same way. A compressor is "
                "tested for the pressure it can build and the time it takes. "
                "Where we suspect the valve block we isolate it from the "
                "corners and watch the reservoir. The estimate names the "
                "component the tests pointed at, shows the photographs, and "
                "says which other components were tested and passed. That "
                "last part matters: it is what stops a strut job becoming a "
                "compressor job a month later, or the other way round.",
                ("callout",
                 "A car that can be raised has a working compressor. If a "
                 "shop wants to replace the compressor on a car that lifts "
                 "itself every morning, ask what test they did."),
            ]),
            ("One strut, or two?", [
                "When one front strut has failed on a car of any age, the "
                "other is the same age and the same rubber, and it will "
                "follow. We recommend replacing them in pairs at the front "
                "and in pairs at the rear, for the same reason we replace "
                "brake pads by the axle, and because the labor overlaps. We "
                "do not recommend all four at once unless all four are "
                "leaking; the tests tell us which. Whatever is replaced, the "
                "ride height is calibrated in XENTRY afterwards, which is not "
                "optional: the module has to be told where level is.",
                "Parts follow the usual tiers. The air springs in a "
                "Mercedes-Benz are made by a small number of suppliers, and "
                "a genuine or OE-supplier unit is what we fit; the "
                "aftermarket includes both remanufactured units built on the "
                "original core and cheaper new ones whose rubber does not "
                "last, and we will say which is which on the estimate.",
            ]),
            ("Converting to steel springs", [
                "There are kits that replace AIRMATIC with conventional coil "
                "springs and dampers, and we are sometimes asked about them. "
                "They are cheaper than an air strut in the short run and "
                "they remove the failure mode entirely. What they also remove "
                "is what the car was designed around: the self-levelling with "
                "a load or a trailer, the ride the car is known for, the "
                "adjustable damping, and on some models a warning on the "
                "dash that has to be coded out. On a high-mileage GL that is "
                "kept as a workhorse a conversion can make sense. On an "
                "S-Class it rarely does, and it affects the car's value. We "
                "will give you an honest answer for your car rather than a "
                "general one.",
            ]),
            ("Before you buy one", [
                f"On a pre-purchase inspection of an AIRMATIC car we check "
                f"ride height at all four corners after the car has sat, the "
                f"compressor run-time counter and the module's fault memory, "
                f"because none of that appears on a history report; CARFAX "
                f"will show you whether the suspension was ever replaced, "
                f"which is worth knowing, but not whether it is about to need "
                f"it. Our {link(INSPECTION, 'pre-purchase inspection')} page "
                f"describes the whole check. We also run the VIN against "
                f"NHTSA's recall lookup, as we do on every Mercedes-Benz we "
                f"see for the first time.",
                f"If your car is doing any of the things above, note when it "
                f"happens (overnight, after a drive, on one corner or all "
                f"four) and call. That one detail usually tells us which "
                f"test to run first, and it is where every AIRMATIC "
                f"{link(HUB, 'Mercedes repair')} here starts.",
            ]),
        ],
        "further": [SERVICE_AB, COSTS, CASES],
        "cta_heading": "Sitting low on one corner?",
        "cta_text": "Tell us when it happens and which corner. We will tell you what we would test first, and quote the part the tests point at.",
    },
    {
        "slug": COSTS,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.FTC_WARRANTY, src.FTC_MAGMOSS, src.MB_FLUIDS, src.EPA_MVAC],
        "title": "Why Mercedes Repair Costs What It Does | German Performance",
        "description": (
            "Genuine vs OE-supplier parts, sealed assemblies, access labor, the "
            "XENTRY factor and whole-assembly quotes for repairable faults. No "
            "prices."),
        "eyebrow": EYEBROW,
        "h1": 'Why Mercedes Repair Costs <span class="accent">What It Does</span>',
        "dek": (
            "A Mercedes-Benz is not expensive to fix because of the star. It "
            "is expensive when a whole assembly is quoted for a repairable "
            "fault, when the coding is left out, or when a small leak is left "
            "to become a large one. Here is what moves the bill."),
        "intro": (
            f"There are no prices here, on purpose. A number without a "
            f"diagnosis is a guess, and a Mercedes-Benz estimate built on a "
            f"guess is how owners end up paying for a transmission when a "
            f"circuit board was the fault. What this article does instead is "
            f"open up the estimate: where the parts line comes from and what "
            f"the tiers mean on this marque, why so much of the labor is "
            f"about reaching the part, what the factory software adds to a "
            f"job and why a quote without it is incomplete, and the "
            f"difference between a fault and the assembly it lives in. It is "
            f"the reasoning behind every estimate we write for {HUB_LINK}."),
        "sections": [
            ("Genuine, OE supplier, or aftermarket", [
                "Mercedes-Benz makes engines and transmissions; most of what "
                "surrounds them comes from suppliers. Bosch makes the "
                "injection, ignition and much of the electronics, "
                "Lemf&ouml;rder the suspension arms and bushings, Mahle and "
                "Behr the filters and cooling parts, ZF and Bilstein the "
                "steering and dampers, and the AIRMATIC struts come from a "
                "short list of specialists. A genuine part is one of those in "
                "a Mercedes-Benz box, tested to the factory specification. An "
                "OE-supplier part is the same part in the supplier's own box, "
                "and on most jobs that is where the value is. Aftermarket is "
                "everything else, from excellent to disposable.",
                "Our default is genuine or OE-supplier. Anything the engine "
                "or transmission control module talks to, and anything "
                "carrying fluid under pressure, should be one of those two. "
                "The estimate marks every line with its tier and the reason, "
                "and where a good aftermarket part makes sense on an older "
                "car, a set of rotors or an expansion tank, we say so. What "
                "we will not do is fit the cheapest part to win the quote. On "
                "a Mercedes-Benz that is the shortest route to doing the job "
                "twice, and the second labor charge is the one nobody budgets "
                "for.",
            ]),
            ("Sealed and cartridge assemblies", [
                "Mercedes-Benz likes the sealed unit, and it shapes the "
                "estimate. The 722.9 transmission's control electronics are "
                "one plate; the ignition coil packs on some engines are one "
                "rail; the rear air spring is a bellows and a damper in one "
                "piece on some models and two on others; the SBC brake unit "
                "on the cars of the mid-2000s is a single hydraulic-and-"
                "electronic module. Where the factory sells the assembly and "
                "not the piece inside it that failed, the parts line "
                "reflects the assembly.",
                "The useful question is whether the piece can be had "
                "separately from the supplier when it cannot be had from the "
                "dealer, and often it can. A conductor plate is available on "
                "its own; so is a compressor relay, a level sensor, a valve-"
                "block seal kit, an oil-cooler seal set. Knowing which "
                "assemblies come apart and which do not is a large part of "
                "what makes one Mercedes-Benz estimate reasonable and another "
                "not, and it comes from having done the job before.",
            ]),
            ("Labor is about access", [
                "Labor is billed on time, and time on a Mercedes-Benz is "
                "mostly about reaching the part. The oil-cooler seals on an "
                "M272 or M273 are two small rings of rubber in the valley "
                "between the cylinder heads, under the intake manifold; the "
                "manifold, the throttle body and a good deal of plumbing come "
                "off to reach them. The camshaft adjuster magnets are easy; "
                "the harness they have soaked in oil is not. The auxiliary "
                "battery on some models is behind the dash. A rear air spring "
                "is quick; a front strut on a big SUV is not. None of these "
                "parts is expensive. Reaching them is the job, and a fair "
                "estimate includes the seals and gaskets that must be renewed "
                "because they were opened on the way in.",
                f"Jobs cluster for the same reason. When the intake is off for "
                f"the valley seals, the intake-manifold flaps and the "
                f"thermostat are a small extra part and almost no extra time; "
                f"done separately they are the labor charge again. A good "
                f"estimate tells you what else is exposed while a job is open, "
                f"with photographs, and lets you decide. The general argument "
                f"is in "
                f"{link('what-affects-german-car-repair-costs.html', 'what affects German car repair costs')}; "
                f"the Mercedes-Benz version is that these cars were built to "
                f"be serviced in systems, and the estimate should be too.",
            ]),
            ("The XENTRY factor", [
                f"On a modern Mercedes-Benz, fitting the part is not the end "
                f"of the repair, and the factory software, XENTRY, is what "
                f"finishes it. A replaced control module, a conductor plate "
                f"included, has to be SCN-coded to the car online before it "
                f"does anything at all. A transmission service on the 722.9 "
                f"is followed by an adaptation reset and a level set by "
                f"temperature. An AIRMATIC strut is followed by a ride-height "
                f"calibration. Rear brake pads on cars with an electric "
                f"parking brake need the caliper put into service mode and "
                f"back. And on the SBC-equipped cars, the brake system must be "
                f"deactivated in XENTRY before the pads are touched and "
                f"reactivated afterwards; a shop that does not know this can "
                f"injure someone. Our {link(BRAKES, 'brake repair')} page "
                f"covers SBC and the parking-brake step.",
                "A shop without XENTRY cannot do any of this, so it either "
                "leaves the step out or sends the car somewhere that can, and "
                "the price you were quoted was never for the whole job. When "
                "you compare estimates, ask whether the coding, the "
                "calibration or the adaptation is included. It is one line on "
                "ours, and it is not optional.",
            ]),
            ("The fault versus the assembly", [
                f"This is where the largest Mercedes-Benz bills are saved or "
                f"lost. A 722.9 that shifts harshly and drops into limp mode "
                f"has, in our experience, a conductor plate far more often "
                f"than it has a worn transmission, and the two quotes differ "
                f"by an order of magnitude. A car that sits low on one corner "
                f"has a leaking spring, not a compressor. An engine with a "
                f"camshaft-correlation code may have a sprocket, a magnet, or "
                f"a stretched chain, and only one of those is an engine-out "
                f"job. A misfire is a plug or a coil long before it is an "
                f"injector.",
                f"The only way to tell them apart is to test, which is why "
                f"every estimate here follows a diagnosis on XENTRY and a "
                f"physical inspection, and why the estimate shows the "
                f"evidence. The AIRMATIC guide and the case studies below "
                f"walk through exactly this on real jobs. The dealer, to be "
                f"fair, tests too; the difference is usually in what is "
                f"quoted afterwards, because a dealer's parts catalogue "
                f"tends to list the assembly. Our "
                f"{link(CEL, 'check engine light')} page explains the "
                f"diagnostic itself.",
            ]),
            ("AMG, air conditioning and other specifics", [
                f"A few things move a Mercedes-Benz estimate that do not "
                f"apply to every make. AMG engines, the M156, M157 and M177 "
                f"among them, are hand-assembled units with their own parts, "
                f"their own known patterns and their own fluid sheets, and "
                f"the estimate reflects that; they are not a regular engine "
                f"with a badge. Air conditioning on most 2017-and-later cars "
                f"uses the R-1234yf refrigerant, which needs its own recovery "
                f"equipment; federal law requires anyone servicing a vehicle "
                f"air-conditioning system for pay to hold the EPA's Section "
                f"609 certification, which is in the sources and which our "
                f"technicians hold. The {link(AC, 'German car AC repair')} "
                f"page explains how we diagnose the system before any "
                f"refrigerant goes in. And the fluids themselves are an "
                f"approval, not a brand: Mercedes-Benz publishes the sheets "
                f"for oil, brake fluid, coolant and transmission fluid, and "
                f"the estimate names the sheet.",
            ]),
            ("The dealer, the independent, and the same job", [
                f"The dealer and a Mercedes-Benz specialist independent are "
                f"doing the same repair with, in our case, the same software, "
                f"factory-trained technicians and the same tier of parts. The "
                f"dealer's rate carries the building; ours carries the "
                f"judgment about what to quote. The dealer remains the right "
                f"place for a recall or a warranty repair, and we will tell "
                f"you when that is the case. For everything else, federal law "
                f"is clear that a manufacturer cannot condition its warranty "
                f"on using the dealer for maintenance or repair, and the FTC "
                f"has warned manufacturers about implying otherwise; both "
                f"pages are in the sources, and the fuller comparison is in "
                f"{link(DEALER, 'dealership vs. independent shop')}.",
                ("callout",
                 "Ask any shop what its warranty on the work is before you "
                 "compare numbers. Ours is 12 months or 12,000 miles, parts "
                 "and labor, in writing. A lower quote with no warranty is "
                 "not a lower price; it is a bet."),
            ]),
            ("How to get a real number", [
                f"Call with the year, the model, the engine if you know it, "
                f"and what the car is doing. We will tell you what we would "
                f"check first and what the diagnosis should take. A technician "
                f"then runs XENTRY and a physical inspection, and you get a "
                f"written estimate with photographs, each line marked "
                f"genuine, OE-supplier or aftermarket, the coding included, "
                f"and the components that were tested and passed listed too. "
                f"Nothing starts until you approve it, and if the job turns up "
                f"something we did not expect, we stop and call. That is the "
                f"whole of how we price {link(HUB, 'Mercedes repair')}, and "
                f"the maintenance guide, linked below, is how to need less of "
                f"it.",
            ]),
        ],
        "further": [SERVICE_AB, AIRMATIC, CASES],
        "cta_heading": "Want a real number for your Mercedes?",
        "cta_text": "Call with the year, the model and the symptom. We will tell you what we would check first and what finding out should take.",
    },
    CASES_POST,
]
