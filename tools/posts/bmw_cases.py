"""The BMW case studies: three anonymised, representative jobs.

Written as posts/common.py describes: year, model, engine, complaint,
finding, fix, outcome; no customer names, dates or invoices. Registered
by posts/bmw.py, which holds the dates, title and summary.
"""

import posts.sources as src
from posts.common import (
    BMW_CASES as CASES, BMW_COSTS as COSTS, BMW_DRIVETRAIN as DRIVETRAIN, BMW_HUB as HUB,
    BMW_MAINTENANCE as MAINTENANCE, INSPECTION, link,
)

CLUSTER = "bmw"
EYEBROW = "BMW Repair Guide"
HUB_LINK = link(HUB, "BMW repair in Snellville")

POST = {
    "slug": CASES,
    "hub": HUB,
    "cluster": CLUSTER,
    "sources": [src.NHTSA_RECALLS, src.CARFAX, src.BMW_BOOKS],
    "title": "BMW Repair Case Studies | German Performance",
    "description": (
        "Three representative BMW jobs from German Performance in Snellville: "
        "an N20 cold-start rattle, an N55 burning smell, and an X5 that sat "
        "low overnight."),
    "eyebrow": EYEBROW,
    "h1": 'BMW Repair <span class="accent">Case Studies</span>',
    "dek": (
        "What a BMW diagnosis looks like from the inside: the complaint, "
        "what we found, what we did and how it turned out, on three jobs "
        "we see versions of every month."),
    "intro": (
        f"The guides in this series explain BMW maintenance, the Drivetrain "
        f"Malfunction message and what moves an estimate. This one shows "
        f"the reasoning applied. The three jobs below are representative "
        f"of work that comes through our bays regularly; each is written "
        f"up as a composite, with the year, model and engine kept and the "
        f"owner left out. They were chosen because each one arrived with a "
        f"plausible wrong answer attached, and because each shows why we "
        f"insist on a diagnosis before a quote for any "
        f"{HUB_LINK}."),
    "sections": [
        ("Case one: 2013 328i, N20, a rattle for two seconds on cold start", [
            ("h3", "The complaint"),
            "The owner described a metallic rattle from the front of the "
            "engine for a second or two on the first start of the day, "
            "gone once the engine was running, and a check engine light "
            "that had come on the previous week. The car had 84,000 miles "
            "and a service history of dealer oil changes at the counter's "
            "full interval. A previous shop had cleared the code and "
            "suggested it might be a VANOS solenoid.",
            ("h3", "What we found"),
            "ISTA showed stored camshaft correlation codes for both the "
            "intake and exhaust banks, with freeze frames at cold "
            "coolant temperatures and low revs, and a VANOS solenoid "
            "actuation test that passed. That combination on an N20 of "
            "this build period points at the timing chain, not the "
            "solenoids: a chain that has stretched, and guides that have "
            "begun to break up, let the camshafts drift out of "
            "correlation until oil pressure comes up. We confirmed it by "
            "measuring cam timing against the reference and then by "
            "removing the upper timing cover, where the plastic upper "
            "guide was cracked and a piece of it was sitting in the "
            "sump.",
            ("h3", "What we did"),
            "Timing chain, both guides, the tensioner and the oil-pump "
            "drive chain and sprocket, which shares the failure on this "
            "engine, all genuine BMW, with the front crank seal and the "
            "oil filter housing gasket done while the front of the "
            "engine was open. Cam timing set with the factory locking "
            "tools, oil and filter to BMW's approval, adaptations reset "
            "in ISTA. The estimate listed the guide fragment photograph "
            "and the parts that were exposed, and the owner approved the "
            "gasket work at the same time rather than paying the labor "
            "again later.",
            ("h3", "The outcome"),
            "Silent on cold start, no correlation codes on a two-week "
            "follow-up scan, and a car that will now go another hundred "
            "thousand miles on the right oil at 7,500-mile intervals. The "
            "wrong answer, a VANOS solenoid, would have been cheaper for "
            "a month and catastrophic in a year: a chain that jumps on "
            "this engine takes the valves with it.",
        ]),
        ("Case two: 2011 335i, N55, a burning smell and a coolant warning", [
            ("h3", "The complaint"),
            "A burning smell after highway driving, a low-coolant warning "
            "that had appeared twice and been topped up twice, and a "
            "recent Drivetrain Malfunction message on a hot afternoon. "
            "112,000 miles, mixed history. The owner had been told the "
            "smell was \"probably a valve cover gasket\" and had been "
            "living with it.",
            ("h3", "What we found"),
            "The valve cover gasket was indeed weeping, but it was not "
            "the story. The oil filter housing gasket had failed and was "
            "dripping oil directly onto the serpentine belt, which was "
            "glazed and beginning to fray at one edge; on the N55 a belt "
            "that lets go can be drawn into the front crank seal and into "
            "the engine. Below it, the electric water pump was showing an "
            "excessive-current fault in ISTA's memory and the thermostat "
            "was slow to open in the actuation test, which explained both "
            "the coolant loss (through the expansion-tank cap under "
            "pressure) and the reduced-power event on a hot day, when the "
            "DME had pulled timing to protect an engine running warmer "
            "than it should.",
            ("h3", "What we did"),
            "Oil filter housing gasket and valve cover gasket together, "
            "with the coolant-pipe seals disturbed on the way in; "
            "serpentine belt, tensioner and idler; electric water pump "
            "and thermostat as a pair with fresh coolant, and the "
            "expansion tank, which was yellowed and brittle, while the "
            "system was drained. The estimate explained why the water "
            "pump was on it when the owner had come in about a smell, "
            "with the fault-memory printout and photographs of the belt.",
            ("h3", "The outcome"),
            "No smell, coolant level steady over the following month, no "
            "further reduced-power events. This is the clearest example "
            "we have of why BMW jobs cluster: five separate visits' "
            "worth of labor became one, and the belt did not get the "
            "chance to finish the engine.",
        ]),
        ("Case three: 2015 X5 xDrive35i, sitting low at the back overnight", [
            ("h3", "The complaint"),
            "The rear of the car was noticeably lower in the morning and "
            "rose after a few minutes of driving. No warning on the "
            "dash. 71,000 miles, single owner, all dealer history. The "
            "owner had read online that the compressor was the usual "
            "culprit and asked us to replace it.",
            ("h3", "What we found"),
            "The F15 X5 carries self-levelling air springs on the rear "
            "axle, and \"low overnight, rises when driven\" describes a "
            "leak, not a compressor: a compressor that has failed cannot "
            "raise the car at all, while one that is working will lift a "
            "leaking spring every morning until it wears out doing so. "
            "ISTA's level-control data showed the left rear ride-height "
            "sensor settling several millimetres below the right over an "
            "hour with the engine off, and the compressor run-time "
            "counter was climbing. A soapy-water test on the left rear "
            "spring found the bellows bubbling at the fold where it rolls "
            "over the piston, the normal place for an air spring of this "
            "age to fail.",
            ("h3", "What we did"),
            "Both rear air springs, because the right one was the same "
            "age and the same design and would have followed within the "
            "year, and the labor overlaps. The compressor was tested for "
            "output and run-time and kept; it was healthy, and would have "
            "stayed that way now that it was no longer running every "
            "night. Ride height calibrated in ISTA afterwards.",
            ("h3", "The outcome"),
            "Level in the morning, and a compressor that did not need to "
            "be bought. The owner's proposed fix would have replaced the "
            "one part that was working. On the pre-purchase inspections "
            f"we do on these cars (see our "
            f"{link(INSPECTION, 'pre-purchase inspection')} page), a "
            f"rear that sits low is one of the first things we check, "
            f"because the history report will not show it.",
        ]),
        ("What the three have in common", [
            "Each arrived with an answer already attached, from a "
            "previous shop, a forum or an honest guess, and in each case "
            "the answer was the part nearest the symptom rather than the "
            "part that had failed. Each diagnosis started with the full "
            "fault memory and its freeze frames rather than the code "
            "alone, moved to a physical test that could confirm or rule "
            "out the suspect, and ended with a written estimate that "
            "showed the evidence. And in each case the job that was "
            "actually needed was done once, with the parts around it that "
            "were exposed, rather than in instalments.",
            f"We also do two small things on every BMW we see for the "
            f"first time: a recall check against the VIN on NHTSA's "
            f"lookup, since several of the parts above have been the "
            f"subject of BMW recalls or extended coverage, and a report of "
            f"the work to CARFAX so the next owner can see what was done. "
            f"The diagnostic approach is set out in the "
            f"{link(DRIVETRAIN, 'Drivetrain Malfunction guide')}; the "
            f"intervals we used afterwards are in the "
            f"{link(MAINTENANCE, 'maintenance guide')}; and why the "
            f"estimates looked the way they did is in "
            f"{link(COSTS, 'why BMW repair costs what it does')}. If your "
            f"car is doing something that sounds like one of these, the "
            f"{link(HUB, 'BMW repair page')} is the place to start.",
        ]),
    ],
    "further": [MAINTENANCE, DRIVETRAIN, COSTS],
    "cta_heading": "Sound like your BMW?",
    "cta_text": "Call with the year, the engine and the symptom. We will tell you what we would test first, before anyone replaces anything.",
}
