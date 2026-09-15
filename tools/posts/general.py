"""The three general articles that support the homepage.

Two are rendered from this data by tools/build_posts.py; the third, the
dealer-vs-independent piece, is hand-written and registered here only for
its dates, title and summary. See posts/common.py for the facts every
article may state and posts/__init__.py for the whole registry.

Every fact here is already on the site or was supplied by the owner on
2026-09-15 (see common.AUTHOR_NOTE). No prices are quoted, on purpose:
the articles explain what moves a bill, and the estimate does the rest.
"""

from posts.common import (  # noqa: F401
    AUTHOR_NOTE, COSTS, DEALER, DIAGNOSTICS, HOME, HOME_PAGE, PROCESS, REPAIRS,
    SERVICES, STORY, link,
)

CLUSTER = "general"

# (datePublished, dateModified). The dealer article was retitled on
# 2026-09-15 to support the homepage directly.
POST_DATES = {
    DEALER: ("2026-07-28", "2026-09-15"),
    COSTS: ("2026-09-15", "2026-09-15"),
    DIAGNOSTICS: ("2026-09-15", "2026-09-15"),
}

READING = {
    DEALER: "German Auto Repair: Dealership vs. Independent Shop",
    COSTS: "What Affects German Car Repair Costs?",
    DIAGNOSTICS: "Why Do German Cars Need Specialist Diagnostics?",
}

# One line each, for the guides index and llms.txt.
SUMMARY = {
    DEALER: "What changes when you leave the dealer for an independent German specialist, and what the dealer is still better at.",
    COSTS: "Diagnosis, parts tier, labor access, engine family, deferred maintenance and coding: what moves the bill, with no prices quoted.",
    DIAGNOSTICS: "What a generic scanner misses on a car with dozens of control modules, and what the factory software does differently.",
}

# The hand-written article supports the homepage like the other two.
HAND_WRITTEN = {DEALER: {"hub": HOME_PAGE, "cluster": CLUSTER}}

POSTS = [
    {
        "slug": COSTS,
        "hub": HOME_PAGE,
        "cluster": CLUSTER,
        "sources": [],
        "title": "What Affects German Car Repair Costs? | German Performance",
        "description": (
            "The things that actually move the bill on a BMW, Mercedes, Audi, "
            "Porsche or VW repair, explained by the technicians who write the "
            "estimates in Snellville, GA."),
        "eyebrow": "From the Technicians",
        "h1": 'What Affects <span class="accent">German Car Repair Costs</span>?',
        "dek": (
            "A German car is not expensive to fix because of the badge. It is "
            "expensive when the diagnosis is wrong, when maintenance was put off, "
            "or when the job is done twice. Here is what actually moves the bill, "
            "from the people who write the estimates."),
        "intro": (
            "We are asked this on the phone most days, usually as \"roughly what "
            "would it cost to...\" and the honest answer is that we do not know "
            "until we have looked. What we can tell you is what we look at, and "
            "why two cars with the same complaint can leave with very different "
            "invoices. This is that explanation. There are no prices in it, "
            "because a price without a diagnosis is a guess, and you deserve a "
            "written estimate rather than a guess."),
        "sections": [
            ("Diagnosis is where money is saved or lost", [
                "The most expensive repair is the one that did not fix the car. "
                "A generic code reader tells you the engine module logged a "
                "fault; it does not tell you why. A shop working from that code "
                "alone tends to replace the part the code names, and when the "
                "light comes back, the next part along. Owners call this the "
                "parts cannon, and they pay for every shot.",
                f"The alternative is to read the whole car. Every job here starts "
                f"with the manufacturer's own software &mdash; ISTA for BMW, "
                f"XENTRY for Mercedes-Benz, ODIS for Audi and Volkswagen, PIWIS "
                f"for Porsche &mdash; which talks to every control module, shows "
                f"live data, and walks the technician through the factory's own "
                f"test plan for that fault. That is the difference between "
                f"replacing the part that failed and replacing the parts around "
                f"it. The homepage sets out what "
                f'<a href="{REPAIRS}">factory-level diagnostics</a> covers; a '
                f"{link('german-car-check-engine-light.html', 'check engine light diagnosis')} "
                f"is the usual starting point.",
                ("callout",
                 "Paying for a proper diagnosis feels like an extra line on the "
                 "bill. In our experience it is the line that keeps the other "
                 "lines short."),
            ]),
            ("Parts: OEM, OEM-equivalent, or aftermarket", [
                "Parts are the second-largest line on most invoices, and the "
                "one where you have the most say. There are three tiers. "
                "<strong>OEM</strong> is the part in the manufacturer's box. "
                "<strong>OEM-equivalent</strong> is the same part from the "
                "company that makes it for the manufacturer, in that company's "
                "own box, and it is usually where the value is. "
                "<strong>Aftermarket</strong> covers everything else, from "
                "excellent to disposable.",
                "Our default is OEM-grade parts and genuine fluids, because a "
                "German car is built to a specification and parts that miss it "
                "come back. On a newer car the answer should lean OEM. On a "
                "fifteen-year-old car there are places where a quality "
                "aftermarket part makes sense, and we will say where. What we "
                "will not do is fit the cheapest part to win the quote, because "
                "a part fitted twice costs more than a good part fitted once, "
                "and the second labor charge is the part nobody budgets for.",
            ]),
            ("Labor is about access, not the badge", [
                "Labor is billed on time, and time on a German car is mostly "
                "about access. Engine bays are packed tightly, and a gasket that "
                "costs little can sit under an intake manifold, a coolant pipe "
                "and a wiring harness that all have to come off first. The part "
                "is cheap; reaching it is not.",
                "This is why jobs cluster. When the intake is off to replace a "
                "valve cover gasket, the oil filter housing gasket underneath "
                "it is a small extra part and almost no extra time. Done "
                "separately six months later, it is the whole labor charge "
                "again. A good estimate tells you what else is exposed while a "
                "job is open, and lets you decide. That is not upselling; it is "
                "the cheapest moment to do work you will otherwise do later.",
            ]),
            ("The engine family matters more than the brand", [
                "\"German cars are expensive to fix\" is a generalisation that "
                "hides the useful detail. The cost of ownership differs far "
                "more between engine families within one make than between "
                "makes. Each family has documented patterns: timing chain "
                "guides on some, PCV valves and oil filter housing gaskets on "
                "others, high-pressure fuel pumps and injectors on the direct-"
                "injection engines, plastic cooling-system parts that age on a "
                "schedule, air suspension components on the cars that have "
                "them.",
                f"A documented pattern is cheaper to fix than a mystery, because "
                f"the shop knows what to check first and which part to fit. It "
                f"is also why a shop that works on one family of cars every week "
                f"quotes with more confidence than one that sees it twice a "
                f"year. Our make pages set out what we see on "
                f"{link('bmw-repair.html', 'BMW')}, "
                f"{link('mercedes-repair.html', 'Mercedes-Benz')}, "
                f"{link('audi-repair.html', 'Audi')}, "
                f"{link('porsche-repair.html', 'Porsche')} and "
                f"{link('volkswagen-repair.html', 'Volkswagen')}.",
            ]),
            ("Deferred maintenance compounds", [
                "The biggest bills we write are rarely for one failure. They "
                "are for a small problem that was left until it caused a large "
                "one. A weeping oil filter housing gasket drips onto a belt and "
                "the belt fails. A cooling-system plastic that should have been "
                "replaced on schedule cracks on the highway and the engine "
                "overheats. A transmission fluid the manufacturer once called "
                "\"lifetime\" is not, and the unit it protects costs far more "
                "than the service.",
                "None of this is a reason to fear the car. It is a reason to "
                "treat the schedule as real, and to fix small leaks while they "
                "are small. It also shows up at sale: we report service to "
                "CARFAX, and a documented history is worth money to the next "
                "owner in a way a mystery car never is.",
            ]),
            ("The coding after the part is part of the job", [
                f"On a modern German car, fitting the part is not the end of the "
                f"repair. A new battery has to be registered to the charging "
                f"system, which is why a "
                f"{link('bmw-repair.html', 'BMW battery replacement')} "
                f"is more than a swap. A replaced control module has to be "
                f"coded to the vehicle before it does anything at all. A "
                f"transmission service is followed by an adaptation reset, and "
                f"a suspension or windshield job by a camera calibration. Skip "
                f"these and the car works badly, or not for long.",
                f"This is where a lower quote can quietly deliver less. A shop "
                f"without the factory software cannot do the coding, so it "
                f"either leaves it out or sends the car to someone who can, and "
                f"the price you were quoted was never the whole job. The "
                f"homepage lists "
                f'<a href="{SERVICES}">the services we perform</a>, and the '
                f"factory-level software behind each of them is the reason the "
                f"estimate you get here is the full one.",
            ]),
            ("How we quote", [
                f"You call and tell us the year, the model and what the car is "
                f"doing. We say what we would check first and what finding out "
                f"should cost, so there is no surprise on the diagnostic. A "
                f"technician then runs the factory scan and a physical "
                f"inspection, and you get a written report with photographs of "
                f"what was found. Nothing starts until you approve a written "
                f"estimate, and if the work turns up something we did not "
                f"expect, we stop and call. The whole sequence is on our "
                f'homepage under <a href="{PROCESS}">how your car gets fixed</a>.',
                "Every repair leaves with a 12-month, 12,000-mile parts-and-"
                "labor warranty in writing. That is part of the cost too, and "
                "it is worth asking any shop what theirs is before you compare "
                "numbers.",
            ]),
            ("Questions to ask before you approve any estimate", [
                "Whichever shop you use, these are the questions that separate "
                "a real estimate from a hopeful one:",
                ("list", [
                    "<strong>What did the diagnosis actually find?</strong> A "
                    "fault code is a symptom. You want the cause, and the "
                    "evidence for it.",
                    "<strong>Which parts are OEM, OEM-equivalent or "
                    "aftermarket, and why?</strong> A good shop has a reason "
                    "for each choice.",
                    "<strong>What else is exposed while this job is open?</strong> "
                    "If there is a part worth doing now, you want to know now.",
                    "<strong>Is the coding or calibration included?</strong> "
                    "On a modern German car, a quote without it is not for the "
                    "whole repair.",
                    "<strong>What is the warranty on the work?</strong> Ours is "
                    "12 months or 12,000 miles, parts and labor. Any serious "
                    "shop will have a clear answer.",
                ]),
            ]),
        ],
        "further": [DIAGNOSTICS, DEALER],
        "cta_heading": "Want a real number?",
        "cta_text": "Call with the year, the model and the symptom. We will tell you what we would check first and what finding out should cost.",
    },
    {
        "slug": DIAGNOSTICS,
        "hub": HOME_PAGE,
        "cluster": CLUSTER,
        "sources": [],
        "title": "Why Do German Cars Need Specialist Diagnostics? | German Performance",
        "description": (
            "A German car has dozens of networked control modules and a generic "
            "scanner reads one of them. What the factory software sees, and why "
            "it changes the repair."),
        "eyebrow": "From the Technicians",
        "h1": 'Why Do German Cars Need <span class="accent">Specialist Diagnostics</span>?',
        "dek": (
            "The short answer: a modern BMW, Mercedes-Benz, Audi, Porsche or "
            "Volkswagen is a network of computers, and a generic scanner talks "
            "to one of them. Here is what that means for the car in your "
            "driveway, and for the bill."),
        "intro": (
            "Every German car we see has already been scanned by someone. The "
            "owner, the parts store, a general shop. It usually came with a code "
            "and a theory. Sometimes the theory is right. Often the code was "
            "cleared, the light came back, and the car arrives here with the "
            "same fault and one new part. This article explains why that "
            "happens, what a specialist actually does differently, and when "
            "you need it."),
        "sections": [
            ("One car, dozens of computers", [
                "A current German car carries dozens of control modules; the "
                "count depends on the model and the options. "
                "The engine has one. So do the transmission, the brakes and "
                "stability control, the steering, the instrument cluster, the "
                "body electronics, the climate system, each door, the seats, "
                "the lighting, the driver-assistance cameras and radar, and the "
                "gateway that lets them all talk to each other. A fault in one "
                "shows up as a symptom in another, and a symptom is not a cause.",
            ]),
            ("What a generic scanner sees, and what it does not", [
                "The port under your dashboard is an OBD-II port, and OBD-II is "
                "an emissions standard. It was written so any tool could read "
                "the engine module's emissions-related faults. That is what a "
                "generic scanner does, and it does it well. It reads one module, "
                "and the generic codes that module is required to publish.",
                "What it cannot see is everything else: the manufacturer-"
                "specific codes in the engine module, and the modules for the "
                "transmission, chassis, body, comfort and driver-assistance "
                "systems that speak the manufacturer's own protocol. It cannot "
                "run a test, command a component, read an adaptation or code a "
                "part. It can clear a code, which turns the light off. A "
                "cleared code is not a fixed car; it is a car that has stopped "
                "telling you about the fault until it recurs.",
            ]),
            ("What the factory software does differently", [
                f"Each manufacturer writes its own diagnostic system for its "
                f"dealer network, and an independent shop can invest in the "
                f"same systems. We run ISTA for BMW and MINI, XENTRY for "
                f"Mercedes-Benz, ODIS for Audi and Volkswagen, and PIWIS for "
                f"Porsche. Between them they cover every car we work on, and "
                f"they are described on our {link('about.html', 'About page')} "
                f"and in the "
                f'<a href="{REPAIRS}">what we repair</a> section of the homepage.',
                "The difference is not a longer list of codes. It is what the "
                "software lets a technician do with them:",
                ("list", [
                    "<strong>Read every module,</strong> with the manufacturer-"
                    "specific faults and the freeze-frame data recorded when "
                    "each one set.",
                    "<strong>Watch live data</strong> from sensors across the "
                    "car at once, so a sensor that reads plausibly on its own "
                    "can be caught disagreeing with the others.",
                    "<strong>Follow the factory's guided test plan</strong> "
                    "for that fault on that model, which is the manufacturer's "
                    "own knowledge of what usually causes it.",
                    "<strong>Command components</strong> &mdash; a fuel pump, a "
                    "solenoid, a fan &mdash; to prove whether the part or the "
                    "wiring to it has failed.",
                    "<strong>Read and reset adaptations</strong>, register "
                    "batteries, code replacement modules and calibrate cameras "
                    "and radar.",
                ]),
            ]),
            ("Symptoms are not causes", [
                "Three patterns we see constantly show why the first code is "
                "rarely the answer.",
                "<strong>Voltage.</strong> A battery that is weak, or was "
                "replaced but never registered, lets system voltage sag during "
                "cranking. Modules across the car log faults about their own "
                "sensors that are really about the voltage they were fed. On a "
                "generic scanner that looks like several unrelated failures; "
                "read across every module with the timestamps, it is one "
                "cause.",
                "<strong>Misfires.</strong> A misfire code names a cylinder, not "
                "a part. The cause can be an ignition coil, a spark plug, an "
                "injector, a vacuum leak, or, on some engines, a stretched "
                "timing chain that has moved the cam timing. Swapping the coil "
                "is the cheap guess. Reading fuel trims, camshaft correlation "
                "and the injector data is how the guess becomes a diagnosis.",
                "<strong>Shift complaints.</strong> A harsh or slow shift is "
                "often blamed on the transmission. The transmission module "
                "keeps its own adaptation values and its own fault memory, and "
                "reading those tells you whether the unit is failing, whether "
                "it has simply learned around a worn part, or whether the "
                "fault is electrical and the transmission is fine.",
            ]),
            ("The part is not fixed until the car knows about it", [
                f"On a modern German car, fitting the part is half the repair. "
                f"A new battery has to be registered so the charging system "
                f"stops charging it as if it were the old, tired one, which is "
                f"why a {link('bmw-repair.html', 'BMW battery replacement')} "
                f"is a diagnostic job as well as a mechanical one. A replacement "
                f"control module is a blank until it is coded to the vehicle "
                f"and its options. A service is not complete until the service "
                f"computer is reset. A windshield, a suspension repair or an "
                f"alignment on a car with driver assistance ends with a camera "
                f"calibration, or the car's safety systems are looking at the "
                f"wrong piece of road.",
                f"None of that is possible without the factory software, which "
                f"is one reason the tools matter more than the sign over the "
                f"door. We wrote about the rest of that comparison in "
                f"{link(DEALER, 'German Auto Repair: Dealership vs. Independent Shop')}.",
            ]),
            ("Why a wrong diagnosis costs more than a right one", [
                f"A guess is cheaper than a diagnosis only if it is right. When "
                f"it is wrong, you have paid for a part, the labor to fit it, "
                f"and the diagnosis you now need anyway, and the fault has had "
                f"time to do more damage. We went through the arithmetic in "
                f"{link(COSTS, 'What Affects German Car Repair Costs?')}; the "
                f"short version is that the diagnostic line on the estimate is "
                f"the one that keeps the others short.",
            ]),
            ("What specialist diagnostics looks like here", [
                f"You call and describe the year, the model and the symptom. "
                f"We say what we would check first and what finding out should "
                f"cost. The car is scanned on the factory software for its "
                f"marque, every module, and then physically inspected, because "
                f"the software points and the technician confirms. You get a "
                f"written report with photographs, and nothing proceeds until "
                f"you approve a written estimate. That sequence is the "
                f'<a href="{PROCESS}">five steps on our homepage</a>, and the '
                f'<a href="{SERVICES}">services we perform</a> are listed there '
                f"with what each includes.",
                f"The people doing it have worked only on German cars since "
                f"2010, more than 10,000 of them through this shop. The "
                f"technician who leads our electrical and engine diagnostics is "
                f"an ASE Master Technician with the advanced engine diagnostics "
                f"certification and Mercedes-Benz factory training, and trains "
                f"the junior technicians here on the same method. "
                f'<a href="{STORY}">More about the shop</a> is on the homepage.',
            ]),
            ("When you need it, and when you do not", [
                f"Not every visit needs a deep scan. An oil change does not, "
                f"though it does need the service reset the generic tool cannot "
                f"do. Brake pads and rotors do not, unless the car has electric "
                f"parking brake actuators that must be retracted first. What "
                f"does need it:",
                ("list", [
                    f"A check engine light, especially one that has come back "
                    f"after being cleared. Start with a "
                    f"{link('german-car-check-engine-light.html', 'check engine light diagnosis')}.",
                    "Anything intermittent or electrical: a warning that comes "
                    "and goes, a module that drops out, a battery that keeps "
                    "dying.",
                    "A drivability complaint: a misfire, a hesitation, a rough "
                    "idle, a shift that has changed.",
                    "Any warning on the instrument cluster that is not the "
                    "engine light. Those come from modules a generic scanner "
                    "never sees.",
                    f"A car you are about to buy. A "
                    f"{link('german-car-pre-purchase-inspection.html', 'pre-purchase inspection')} "
                    f"reads every module's fault memory, including faults that "
                    f"were cleared before the sale.",
                ]),
            ]),
        ],
        "further": [COSTS, DEALER],
        "cta_heading": "Light on? Start with the scan.",
        "cta_text": "Bring it in for a diagnostic on the factory software and see what the car has been trying to say.",
    },
]
