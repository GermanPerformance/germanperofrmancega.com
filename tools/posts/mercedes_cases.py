"""The Mercedes-Benz case studies: three anonymised, representative jobs.

Written as posts/common.py describes: year, model, engine, complaint,
finding, fix, outcome; no customer names, dates or invoices. Registered
by posts/mercedes.py, which holds the dates, title and summary.
"""

import posts.sources as src
from posts.common import (
    INSPECTION, MB_AIRMATIC as AIRMATIC, MB_CASES as CASES, MB_COSTS as COSTS,
    MB_SERVICE_AB as SERVICE_AB, MERCEDES_HUB as HUB, link,
)

CLUSTER = "mercedes"
EYEBROW = "Mercedes Repair Guide"
HUB_LINK = link(HUB, "Mercedes repair in Snellville")

POST = {
    "slug": CASES,
    "hub": HUB,
    "cluster": CLUSTER,
    "sources": [src.NHTSA_RECALLS, src.CARFAX, src.MB_FLUIDS],
    "title": "Mercedes Repair Case Studies | German Performance",
    "description": (
        "Three representative Mercedes-Benz jobs from German Performance: an "
        "M272 oil smell with coolant loss, a GL450 low on one corner, and a "
        "722.9 in limp mode."),
    "eyebrow": EYEBROW,
    "h1": 'Mercedes Repair <span class="accent">Case Studies</span>',
    "dek": (
        "What a Mercedes-Benz diagnosis looks like from the inside: the "
        "complaint, what we found, what we did and how it turned out, on "
        "three jobs we see versions of every month."),
    "intro": (
        f"The other guides in this series explain the service schedule, "
        f"the AIRMATIC system and what moves an estimate. This one shows "
        f"the reasoning applied. The three jobs below are representative "
        f"of work that comes through our bays regularly; each is written "
        f"up as a composite, with the year, model and engine kept and the "
        f"owner left out. They were chosen because each arrived with a "
        f"plausible wrong answer attached, and because each shows why a "
        f"diagnosis comes before a quote for any {HUB_LINK}."),
    "sections": [
        ("Case one: 2008 E350, M272, an oil smell and a coolant warning", [
            ("h3", "The complaint"),
            "A smell of hot oil after every drive, a low-coolant warning "
            "that had come on twice in a month, and a check engine light "
            "that a parts-store scanner had read as a camshaft-position "
            "code. 118,000 miles, mostly dealer history until recently. "
            "The owner had been quoted a valve cover gasket elsewhere and "
            "wanted a second opinion on the light.",
            ("h3", "What we found"),
            "The valve cover gaskets were dry. The smell was the "
            "engine-oil cooler, which on the M272 sits in the valley "
            "between the cylinder heads under the intake manifold; its "
            "two seals had hardened and oil was running down the back of "
            "the block onto the exhaust, which was the smell. The coolant "
            "loss was the plastic thermostat housing beside it, cracked "
            "at a mounting ear and weeping when hot. The code was the "
            "part that needed care: on a 2004 to 2008 M272 a camshaft-"
            "correlation code can mean the balance-shaft sprocket, which "
            "is an engine-out repair, or something far smaller. XENTRY's "
            "live data showed the camshaft deviation values and the "
            "actuation test on the adjuster solenoids; the deviation was "
            "within the range that points at the adjuster magnet on one "
            "bank, and that magnet was found weeping oil into its own "
            "connector. Balance-shaft wear was ruled out by the "
            "deviation pattern before anything was quoted, and we said "
            "so in writing.",
            ("h3", "What we did"),
            "Oil-cooler seals, thermostat and housing, and the intake-"
            "manifold gaskets and swirl-flap check while the manifold was "
            "off, with fresh coolant to the approved sheet. Both camshaft-"
            "adjuster magnets, since they are the same age and the second "
            "was beginning to sweat, and a clean of the affected "
            "connector and harness, which had not yet carried oil as far "
            "as the engine control module. Engine oil and cartridge "
            "filter to MB 229.5 with the valley open. Adaptations cleared "
            "in XENTRY. The estimate carried photographs of the wet "
            "seals, the cracked housing and the oily connector.",
            ("h3", "The outcome"),
            "No smell, coolant level steady over the following two "
            "months, no code on a follow-up scan. The wrong answer, a "
            "valve cover gasket, would have fixed nothing; the frightening "
            "answer, a balance shaft, was not the fault. Ruling it out "
            "took an hour on XENTRY and was the most valuable hour of the "
            "job.",
        ]),
        ("Case two: 2013 GL450, low at the left front overnight", [
            ("h3", "The complaint"),
            "The left front corner was down in the morning and rose "
            "within a minute of starting the car. No message on the dash "
            "yet. 96,000 miles, one previous owner. The owner had been "
            "quoted an AIRMATIC compressor and a strut together "
            "elsewhere, on the grounds that \"they usually go together\".",
            ("h3", "What we found"),
            "A car that lifts itself every morning has a working "
            "compressor. XENTRY's live data confirmed it: reservoir "
            "pressure normal, compressor building pressure at the "
            "expected rate, the left-front ride-height sensor reading "
            "low after the car had sat and correcting on start-up, and a "
            "compressor run-time counter that was high but a "
            "temperature history that was not. With the valve block "
            "closed to that corner, the left front would not hold "
            "height, which puts the leak in the strut or its line. Soapy "
            "water found the front strut bellows bubbling at the rolling "
            "fold. The line and the fitting were dry.",
            ("h3", "What we did"),
            "Both front struts, genuine, because the right one was the "
            "same age and design and would have followed, and the labor "
            "on a GL front end overlaps. The compressor was kept: it had "
            "passed the fill test, and with the leak gone it would no "
            "longer be running every night. Ride height calibrated in "
            "XENTRY at all four corners afterwards, and the compressor's "
            "relay, a common failure that is a small part, replaced as a "
            "precaution while the system was open. The estimate listed "
            "the compressor as tested and passed.",
            ("h3", "The outcome"),
            "Level in the morning and level a month later. The owner's "
            "earlier quote would have replaced the one expensive "
            "component that was working. On the pre-purchase inspections "
            f"we do on these cars (our "
            f"{link(INSPECTION, 'pre-purchase inspection')} page "
            f"describes the check) the overnight ride height and the "
            f"compressor run-time counter are among the first things we "
            f"look at, because CARFAX cannot show what a suspension is "
            f"about to do.",
        ]),
        ("Case three: 2012 C300, 722.9, harsh shifts and limp mode", [
            ("h3", "The complaint"),
            "A harsh shift between second and third that had become "
            "harsh on most shifts, and twice a drop into limp mode with a "
            "transmission warning that cleared on restart. 103,000 miles. "
            "The fluid had never been changed, on the understanding that "
            "it was sealed for life. The owner had been quoted a "
            "replacement transmission and was asking whether the car was "
            "worth it.",
            ("h3", "What we found"),
            "XENTRY's transmission fault memory held implausible-signal "
            "codes for one of the internal speed sensors, stored with the "
            "limp-mode events, and the live data showed that sensor "
            "dropping out intermittently when the fluid was hot. That "
            "pattern on a 722.9 points at the conductor plate, the "
            "electronic control plate inside the pan that carries the "
            "speed sensors and the transmission's own computer, rather "
            "than at the clutch packs or the valve body. The fluid, "
            "drained, was dark and smelt burnt, which fits: the plate "
            "lives in it. There was no metal on the magnet in the pan, "
            "and the clutch-adaptation values were within range, which "
            "is what told us the hard parts were still good.",
            ("h3", "What we did"),
            "A new conductor plate, genuine, SCN-coded to the car online "
            "through XENTRY, which is not optional and is the step a shop "
            "without the factory software cannot perform. New fluid to "
            "the approved sheet, the filter and the pan gasket, and the "
            "level set by temperature. The connector O-ring at the case, "
            "a known weep point, replaced while the pan was off. "
            "Adaptations reset and a relearn drive on the road. The "
            "estimate explained why the transmission itself was not "
            "being quoted, with the fault-memory printout and a "
            "photograph of the clean pan magnet.",
            ("h3", "The outcome"),
            "Smooth shifts, no limp mode, and a car the owner kept. The "
            "difference between the quote for a transmission and the "
            "quote for a plate is the difference between selling the car "
            "and driving it for years, and the only thing that separated "
            "them was an hour of testing. The fluid now goes on an "
            "interval, which the "
            f"{link(SERVICE_AB, 'Service A vs Service B guide')} explains.",
        ]),
        ("What the three have in common", [
            "Each arrived with an answer already attached, from a "
            "previous shop, a forum or a general rule, and in each case "
            "the answer was the part nearest the symptom, or the largest "
            "assembly it lived in, rather than the part that had failed. "
            "Each diagnosis started with XENTRY's fault memory and live "
            "data rather than a generic code, moved to a physical test "
            "that could confirm or rule out the suspect, and ended with a "
            "written estimate that showed the evidence and listed what "
            "had been tested and passed. And in each case the job that "
            "was needed was done once, with the parts around it that were "
            "exposed, rather than in instalments.",
            f"We also do two small things on every Mercedes-Benz we see "
            f"for the first time: a recall check against the VIN on "
            f"NHTSA's lookup, and a report of the work to CARFAX so the "
            f"next owner can see what was done. The tests in case two are "
            f"set out in the {link(AIRMATIC, 'AIRMATIC guide')}; the "
            f"intervals that would have prevented case three are in the "
            f"{link(SERVICE_AB, 'service guide')}; and why the estimates "
            f"looked the way they did is in "
            f"{link(COSTS, 'why Mercedes repair costs what it does')}. If "
            f"your car is doing something that sounds like one of these, "
            f"the {link(HUB, 'Mercedes repair page')} is the place to "
            f"start.",
        ]),
    ],
    "further": [SERVICE_AB, AIRMATIC, COSTS],
    "cta_heading": "Sound like your Mercedes?",
    "cta_text": "Call with the year, the engine and the symptom. We will tell you what we would test first, before anyone replaces anything.",
}
