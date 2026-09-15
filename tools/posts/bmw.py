"""The BMW guides: four articles that support the BMW hub.

Maintenance, symptoms and diagnosis, what moves the bill, and case
studies. Every technical claim is a documented characteristic of the
marque or is already on the site; see posts/common.py for the facts the
closing note may state and for how the case studies are framed. No
prices, on purpose.
"""

import posts.sources as src
from posts.bmw_cases import POST as CASES_POST
from posts.common import (  # noqa: F401
    BMW_CASES as CASES, BMW_COSTS as COSTS, BMW_DRIVETRAIN as DRIVETRAIN, BMW_HUB,
    BMW_MAINTENANCE as MAINTENANCE, BRAKES, CEL, DEALER, INSPECTION, OIL, TRANSMISSION,
    TUNE_UP, link,
)

CLUSTER = "bmw"
HUB = BMW_HUB
EYEBROW = "BMW Repair Guide"

POST_DATES = {
    MAINTENANCE: ("2026-09-15", "2026-09-15"),
    DRIVETRAIN: ("2026-09-15", "2026-09-15"),
    COSTS: ("2026-09-15", "2026-09-15"),
    CASES: ("2026-09-15", "2026-09-15"),
}

READING = {
    MAINTENANCE: "BMW Maintenance Schedule Explained",
    DRIVETRAIN: "BMW Drivetrain Malfunction Explained",
    COSTS: "Why BMW Repair Costs What It Does",
    CASES: "BMW Repair Case Studies",
}

SUMMARY = {
    MAINTENANCE: "How Condition Based Service counts, which oil approval your engine needs, and where we shorten BMW's own intervals and why.",
    DRIVETRAIN: "What the message means, the causes we see by engine family, and the order we test in before anything is replaced.",
    COSTS: "Parts tiers, labor that is really about access, the coding that finishes the job, and why BMW jobs cluster. No prices.",
    CASES: "Three representative jobs from our bays: an N20 cold-start rattle, an N55 burning smell, and an X5 that sat low overnight.",
}

HUB_LINK = link(HUB, "BMW repair in Snellville")

POSTS = [
    {
        "slug": MAINTENANCE,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.BMW_BOOKS, src.ZF_OIL, src.FTC_WARRANTY, src.NHTSA_RECALLS],
        "title": "BMW Maintenance Schedule Explained | German Performance",
        "description": (
            "How BMW's Condition Based Service decides what is due, which oil "
            "approval your engine needs, and where German Performance shortens "
            "the interval, and why."),
        "eyebrow": EYEBROW,
        "h1": 'BMW Maintenance Schedule <span class="accent">Explained</span>',
        "dek": (
            "A BMW tells you when it wants service. It does not tell you how it "
            "decided, or what it is not counting. Here is how the schedule "
            "works, engine by engine, and where we deliberately get ahead of it."),
        "intro": (
            f"Most of the BMWs that come to us for {HUB_LINK} arrive with the "
            f"same question in a different form: the car says service is not due "
            f"for another 4,000 miles, so why are we suggesting an oil change "
            f"now? The short answer is that the car is counting one thing and we "
            f"are looking at several. The long answer is this guide. It covers "
            f"what Condition Based Service actually measures, which oil approval "
            f"your engine was built for, the items the counter does not track at "
            f"all, and the handful of places where more than fifteen years of BMW work "
            f"has taught us to shorten the factory interval."),
        "sections": [
            ("How Condition Based Service counts", [
                "Since the mid-2000s every BMW has carried Condition Based "
                "Service, CBS for short. Instead of a fixed mileage for each "
                "job, the car keeps a separate counter for engine oil, brake "
                "pads (front and rear), brake fluid, the cabin microfilter, "
                "spark plugs and a general vehicle check, and shows the one "
                "that is due soonest in the cluster or iDrive. Engine oil is "
                "the interesting one: the counter is not a mileage clock but a "
                "model that runs down faster with fuel consumed, engine "
                "temperature and load. A car driven hard on short trips will "
                "call for oil sooner than one cruising the interstate.",
                "That is a sensible idea, and it is also why we treat the "
                "number as a ceiling rather than a target. The model assumes "
                "the oil in the engine is the one BMW specified, that the "
                "engine is not consuming any, and that the car is not sitting "
                "for weeks between drives. Any of those being untrue makes the "
                "counter optimistic. The other thing worth knowing is that "
                "several counters are reset by hand after the work is done. "
                "If a previous shop changed the oil and never reset the "
                "counter, or reset it without doing the work, the display is "
                "telling you about the last button press, not the oil.",
            ]),
            ("Which oil your engine was built for", [
                "BMW does not specify an oil by brand; it specifies an "
                "approval, printed in the owner's booklet and on the cap of "
                "any oil that meets it. The older naturally aspirated sixes "
                "(the N52 in a 2006 to 2011 328i or 528i) were built for "
                "BMW Longlife-01. Most of the turbocharged engines that "
                "followed, the N54, N55 and N20, call for Longlife-01 or the "
                "low-ash Longlife-04, and the current B46, B48 and B58 "
                "engines moved to the thinner FE+ approvals, Longlife-14 FE+ "
                "and Longlife-17 FE+, which are 0W-20 oils designed for their "
                "tighter clearances and fuel economy targets. An M engine has "
                "its own line in the booklet again.",
                f"An oil with the right viscosity and the wrong approval is not "
                f"the same oil. The approval sets the additive package, the "
                f"ash content the catalysts and particulate filters will "
                f"tolerate, and the shear stability the timing chain and VANOS "
                f"units depend on. Our {link(OIL, 'German car oil change')} "
                f"page explains what we fill with and why; on a BMW the short "
                f"version is that we look up the engine code, not the badge on "
                f"the trunk, and fill to the approval BMW printed for it. Your "
                f"service booklet, or BMW USA's maintenance resources page for "
                f"your model year, is the authority if you want to check what "
                f"the last shop used.",
            ]),
            ("Why we shorten the oil interval on the turbo engines", [
                "BMW's own counter will typically run to 10,000 miles or "
                "twelve months on a current car, and it used to run further. "
                "On the naturally aspirated N52 we are comfortable with that. "
                "On the turbocharged direct-injection engines, the N20, N26, "
                "N54, N55, B48 and B58, and on every M engine, we recommend "
                "changing the oil at 7,000 to 7,500 miles regardless of what "
                "the display says, and sooner if the car is tracked or spends "
                "its life in Atlanta traffic.",
                "The reason is what these engines do to oil. A turbocharger "
                "puts a bearing in the exhaust stream and feeds it engine oil; "
                "direct injection lets a little fuel past the rings on cold "
                "starts and thins the sump; the timing chain, its guides and "
                "the VANOS solenoids are all lubricated by that same oil at "
                "pressure. Every N20 timing chain guide we have replaced, and "
                "every N54 or N55 turbo we have replaced for bearing play, "
                "came out of a car with a long-interval history. We cannot "
                "prove those failures would not have happened at 7,500 miles. "
                "We can tell you which cars they happened in.",
                ("callout",
                 "Shorter oil intervals do not void a BMW warranty. Federal "
                 "law prevents a manufacturer from denying warranty coverage "
                 "because routine maintenance was done by an independent shop, "
                 "as long as the work meets the specification. The FTC's page "
                 "on auto warranties in the sources below is the plain-English "
                 "version."),
            ]),
            ("There is no dipstick, and that matters", [
                "Most BMWs built since 2006 have no dipstick. The level is "
                "read by a sensor in the sump and shown in the cluster or "
                "iDrive, usually only after the engine is warm and has idled "
                "for a minute. Owners who grew up checking oil with a rag "
                "tend to stop checking altogether, and a BMW turbo engine can "
                "legitimately use a quart between services.",
                "We ask every BMW owner to learn where the oil level display "
                "is and to look at it once a month. Low oil on an N-series "
                "engine shows up first as timing chain noise on a cold start, "
                "then as VANOS codes, then as the check engine light; by that "
                "point the fix is a great deal more than a quart. The other "
                "thing the sensor cannot tell you is where the oil went. If "
                "the level is dropping and there is no blue smoke, there is a "
                "leak, and on these engines it is almost always the oil "
                "filter housing gasket or the valve cover gasket, which we "
                "cover below.",
            ]),
            ("What the counter tracks well", [
                "Some CBS items are measured directly and we trust them. "
                "Brake pads carry a wear sensor at one front and one rear "
                "wheel that closes a circuit as the pad thins, so the pad "
                "countdown is real; we still look at the other two corners "
                "and at the rotors, because BMW rotors wear with the pads and "
                f"are usually replaced together (our {link(BRAKES, 'brake repair')} "
                f"page explains the sensor and why it is part of the job). "
                f"Brake fluid is counted by time, two years, which is correct: "
                f"DOT 4 absorbs water from the air whether the car moves or "
                f"not, and old fluid is what makes an ABS pump corrode from "
                f"the inside.",
                "Spark plugs are a mileage counter, and on the turbo engines "
                "we replace them at about half of what the counter allows, "
                "because a worn plug on a boosted direct-injection engine is "
                "the most common cause of the misfire and Drivetrain "
                "Malfunction message we see. Ignition coils are not counted "
                "at all; they fail individually, usually one at a time, and "
                f"we check them whenever the plugs are out. That work sits on "
                f"our {link(TUNE_UP, 'German car tune-up')} page.",
            ]),
            ("What the counter does not track at all", [
                "This is the part of the schedule we care most about, because "
                "nothing on the dashboard will ever mention it.",
                ("list", [
                    "<strong>Cooling system plastics.</strong> The expansion "
                    "tank, thermostat housing, radiator end tanks and the "
                    "hoses' quick-connect fittings are plastic that hardens "
                    "with heat cycles. On the N52, N54 and N55 the water pump "
                    "is electric and fails without warning. We treat the whole "
                    "system as an age item from roughly eight years or "
                    "80,000 miles and inspect it at every oil service.",
                    "<strong>Oil filter housing and valve cover gaskets.</strong> "
                    "Both harden and weep on every N-series engine. The oil "
                    "filter housing gasket is the dangerous one, because it "
                    "sits directly above the serpentine belt.",
                    "<strong>Automatic transmission fluid.</strong> BMW calls "
                    "the fluid in the ZF 8HP and 6HP \"lifetime\". ZF, which "
                    "builds the transmission, publishes guidance on changing "
                    "it and says shorter intervals apply under sporty driving, "
                    "towing and frequent short trips. We service the fluid "
                    "and pan on a mileage basis, with ZF's own fluid, and "
                    f"explain the reasoning on our "
                    f"{link(TRANSMISSION, 'transmission repair')} page.",
                    "<strong>Differential and transfer-case fluid.</strong> "
                    "Also \"lifetime\" on paper. On an xDrive car the "
                    "transfer case in particular benefits from a change.",
                    "<strong>Coolant.</strong> Not counted. We change it when "
                    "cooling-system parts are replaced and on an age basis "
                    "otherwise.",
                    "<strong>Suspension bushings.</strong> Thrust-arm bushings "
                    "on the E-chassis cars and tension-strut bushings on the "
                    "F and G chassis wear into a clunk over bumps and a "
                    "shimmy under braking. They are an inspection item, not a "
                    "counter.",
                    "<strong>The battery.</strong> BMW's charging system "
                    "adapts to a battery as it ages. A new one has to be "
                    "registered with ISTA so the system starts over, and an "
                    "AGM battery has to be coded as one.",
                ]),
            ]),
            ("The schedule, in one table", [
                "What BMW's system indicates, and what we do alongside it. "
                "Intervals are our recommendation for a car driven in Georgia; "
                "your booklet is the reference for what BMW itself specifies.",
                ("table", (
                    ("Item", "What BMW's system indicates", "What we do"),
                    (
                        ("Engine oil and filter", "CBS counter, commonly 10,000 mi / 12 months",
                         "7,000&ndash;7,500 mi on turbo and M engines; the approval BMW printed for the engine code"),
                        ("Oil level", "Sensor readout in the cluster or iDrive",
                         "Check monthly; find the leak if it is dropping"),
                        ("Brake pads and rotors", "Wear sensor countdown, one axle each",
                         "Inspect all four corners; rotors with pads; new sensor every time"),
                        ("Brake fluid", "Every 2 years", "Every 2 years, DOT 4 to BMW's specification"),
                        ("Spark plugs", "Mileage counter", "About half the counter on turbo engines; coils checked with them"),
                        ("Cabin microfilter", "Mileage/time counter", "As counted, sooner in pollen season"),
                        ("Engine air filter", "Vehicle check", "Inspect at every oil service"),
                        ("Cooling system plastics", "Not counted",
                         "Inspect every service; treat as an age item from ~8 years / 80,000 mi"),
                        ("Oil filter housing and valve cover gaskets", "Not counted",
                         "Inspect every service; replace at the first sign of a weep"),
                        ("Automatic transmission fluid", "\"Lifetime\"",
                         "Fluid and pan on a mileage basis with ZF's fluid; adaptations reset"),
                        ("Differential / transfer case", "\"Lifetime\"", "Change on a mileage basis, especially xDrive"),
                        ("Battery", "Not counted",
                         "Test at every service; register and code the replacement in ISTA"),
                    ),
                )),
            ]),
            ("A note on recalls and history", [
                f"Two things sit outside any schedule and are worth doing "
                f"once. The first is a recall check: NHTSA's lookup takes the "
                f"VIN and lists any open safety recall, and BMW has had "
                f"several on the engines above that the dealer performs at no "
                f"charge. We run it on every BMW we see for the first time. "
                f"The second is the car's own record. We report every service "
                f"to CARFAX, and if you are looking at a used BMW, a "
                f"{link(INSPECTION, 'pre-purchase inspection')} that compares "
                f"the history to the counters is the cheapest insurance there "
                f"is against buying someone else's deferred maintenance.",
                f"If the counter says one thing and this guide says another, "
                f"call us with the year, the engine and the mileage. We will "
                f"tell you what we would do first. Everything above is part of "
                f"{link(HUB, 'the BMW work we do every day')}.",
            ]),
        ],
        "further": [DRIVETRAIN, COSTS, CASES],
        "cta_heading": "Not sure what your BMW is due for?",
        "cta_text": "Bring the car and the booklet. We will read the counters, look at what they do not count, and give you a written plan with photographs.",
    },
    {
        "slug": DRIVETRAIN,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.NHTSA_RECALLS, src.BMW_BOOKS],
        "title": "BMW Drivetrain Malfunction Explained | German Performance",
        "description": (
            "What BMW's Drivetrain Malfunction message means, the causes we see "
            "by engine family, and the order German Performance tests in before "
            "replacing anything."),
        "eyebrow": EYEBROW,
        "h1": 'BMW Drivetrain Malfunction <span class="accent">Explained</span>',
        "dek": (
            "The message sounds like the transmission. It almost never is. Here "
            "is what the car is actually reporting, why a code reader cannot "
            "separate the causes, and how we find the one you have."),
        "intro": (
            f"\"Drivetrain Malfunction. Drive moderately. Maximum drivetrain "
            f"output not available.\" If you own a BMW built since about 2011 "
            f"you have either seen this message or you will, usually on a cold "
            f"morning or halfway through a hard pull onto the highway. The car "
            f"goes flat, sometimes shudders, and the message stays until you "
            f"restart, at which point it may or may not come back. It is the "
            f"single most common reason a BMW arrives here for "
            f"{HUB_LINK}, and the single most misdiagnosed. This guide explains "
            f"what the message is, what causes it on each engine family, and "
            f"the order we test in so that the part we replace is the one that "
            f"failed."),
        "sections": [
            ("What the message actually is", [
                "Drivetrain Malfunction is not a fault in itself. It is BMW's "
                "name for a protective mode: the engine control module (the "
                "DME) has detected something it considers a risk to the "
                "engine or the catalysts, usually a misfire or a fuel or boost "
                "condition it cannot correct, and has pulled timing and boost "
                "to limit the damage. On the older E-chassis cars the same "
                "event reads \"Engine Malfunction, Reduced Power\". The word "
                "\"drivetrain\" makes owners think of the transmission, and "
                "we have seen cars arrive with a quote for one. In more than "
                "fifteen years the transmission has been the cause a handful of times.",
                "Because the mode is triggered by a threshold, the message "
                "often clears on a restart. That does not mean the fault is "
                "gone; it means the DME is waiting to see it again. The fault "
                "memory keeps the code, the freeze-frame data around it, and "
                "on most cars a counter of how many times it has happened. "
                "That memory is the starting point of every diagnosis, and it "
                "is the reason we ask owners not to have the codes cleared "
                "before they come in.",
            ]),
            ("The causes we see, by engine family", [
                "The message is generic. The causes are not, and they sort "
                "cleanly by which engine is under the hood.",
                ("h3", "N20 and N26 (2012&ndash;2016 four-cylinder turbo: 328i, 528i, X1, X3, Z4)"),
                "Ignition coils and spark plugs first, by a wide margin. "
                "After that, the timing chain and its guides on the 2012 to "
                "2015 engines: a stretched chain shows up as a cold-start "
                "rattle and camshaft correlation codes long before the message "
                "appears, and if it is left it does not end well. The "
                "high-pressure fuel pump and the oil filter housing gasket "
                "(which can drip onto the belt and, on this engine, let the "
                "belt into the front crank seal) round out the list.",
                ("h3", "N54 (2007&ndash;2013 twin-turbo six: 335i, 535i, 135i, Z4 35i)"),
                "The high-pressure fuel pump is the famous one, and BMW "
                "extended its warranty for a reason: a failing pump gives long "
                "cranks and a hesitation at low revs before it sets the "
                "message. Injectors are next; the early ones were revised "
                "several times and a leaking injector misfires when hot. Then "
                "boost leaks, wastegate rattle from worn actuator bushings, "
                "and the electric water pump letting the engine run hot "
                "enough to pull timing.",
                ("h3", "N55 (2010&ndash;2017 single-turbo six: 335i, 535i, X5 35i, M235i)"),
                "The plastic charge pipe cracks at its coupling and dumps "
                "boost, usually under full throttle, which is exactly when the "
                "message appears. Coils and plugs, VANOS solenoids clogged "
                "with old oil, the oil filter housing gasket, and the "
                "electric water pump follow. The N55 also has an exhaust "
                "VANOS unit that can rattle on start-up; a code for it is not "
                "the same as a failed unit.",
                ("h3", "B46, B48 and B58 (2016 on: 330i, 340i, 530i, X3, Z4, Supra)"),
                "Far fewer, and mostly ignition. Coils and plugs again, "
                "occasionally a boost-control fault from a sticking wastegate "
                "actuator, occasionally the coolant pump or thermostat on a "
                "higher-mileage B58. These engines are the reason the BMW "
                "reputation for reliability is recovering.",
                ("h3", "S55, S58 and the other M engines"),
                "Same families, higher stakes. Plugs are consumables on a "
                "tracked car; a crank hub that has slipped on an early S55 "
                "sets a correlation code before anything else. We check that "
                "first and we say so before we touch it.",
            ]),
            ("Why a code reader cannot separate them", [
                "A generic scanner reads the emissions codes the law requires "
                "every car to publish. A misfire on cylinder three, say. It "
                "does not read BMW's own fault memory in the DME, which "
                "records whether the misfire was at idle or under load, what "
                "the fuel rail pressure was doing at the time, how many times "
                "it has happened and at what coolant temperature. It cannot "
                "command the coils, drive the VANOS solenoids, run the "
                "high-pressure pump test or read the boost-pressure deviation "
                "that tells you a charge pipe is leaking. A misfire code alone "
                "has at least six causes on an N55. Replacing the coil "
                "because that is what the code named is how a car ends up "
                "with a new coil, a new plug, a new injector and the same "
                "message.",
                f"This is what factory software is for. ISTA, BMW's own "
                f"diagnostic system, reads the full fault memory with its "
                f"environmental data and then walks the technician through a "
                f"test plan for that code on that engine, live data and "
                f"component actuations included. Our page on "
                f"{link(CEL, 'check engine light diagnosis')} covers the "
                f"scan itself; the article on why German cars need "
                f"specialist diagnostics, linked below, explains the wider "
                f"point.",
            ]),
            ("The order we test in", [
                "Every Drivetrain Malfunction diagnosis here follows the same "
                "sequence, because the sequence is what stops us guessing.",
                ("list", [
                    "<strong>Read everything before clearing anything.</strong> "
                    "Full fault memory from the DME, transmission and chassis "
                    "modules, with the freeze frames. The misfire counters and "
                    "the fuel-pressure and boost-deviation values usually "
                    "point at a system before we lift the hood.",
                    "<strong>Look at the engine.</strong> Oil level, coolant "
                    "level, the belt, the charge pipe coupling, the oil filter "
                    "housing, the underside of the intake. A surprising number "
                    "of cases are visible.",
                    "<strong>Ignition first when the codes say misfire.</strong> "
                    "Plugs out and read; coils swapped between cylinders so the "
                    "misfire either follows the coil or stays put. Cheap, "
                    "quick and conclusive.",
                    "<strong>Fuel next when the pattern is hot or under load.</strong> "
                    "Rail pressure against the DME's target, cranking and "
                    "under load, using ISTA's pump test; injector correction "
                    "values per cylinder.",
                    "<strong>Boost when the message came at full throttle.</strong> "
                    "Boost-pressure deviation in live data; a smoke test of "
                    "the charge system if it points at a leak.",
                    "<strong>Timing when there is a correlation code or a "
                    "cold rattle.</strong> VANOS solenoid actuation, then "
                    "camshaft timing against the reference, then a physical "
                    "look at the chain guides on the N20.",
                    "<strong>Confirm, then quote.</strong> The written estimate "
                    "names the part that failed and shows the evidence, with "
                    "photographs. If we are unsure, the estimate says so.",
                ]),
            ]),
            ("Symptom pattern to system", [
                "A rough map, from what owners describe on the phone to where "
                "we usually end up. It is a guide to the first test, not a "
                "substitute for one.",
                ("table", (
                    ("What you notice", "Most likely system", "First test"),
                    (
                        ("Message on a cold morning, rough idle, clears when warm",
                         "Ignition (plug or coil), or injector on the N54", "Misfire counters, coil swap"),
                        ("Message under full throttle only, sudden loss of power",
                         "Boost leak: charge pipe on the N55, couplings elsewhere", "Boost deviation, smoke test"),
                        ("Long crank, hesitation off idle, then the message",
                         "High-pressure fuel pump", "Rail pressure under crank and load"),
                        ("Rattle for a second or two on start-up, then the message weeks later",
                         "Timing chain and guides (N20), VANOS", "Correlation codes, VANOS actuation, chain inspection"),
                        ("Message with a temperature warning or a fan running flat out",
                         "Electric water pump or thermostat", "Coolant temperature live data, pump actuation"),
                        ("Message with a transmission warning as well",
                         "Transmission (rare)", "Transmission fault memory, fluid level and condition"),
                    ),
                )),
            ]),
            ("Can you keep driving?", [
                "Moderately, briefly, and only if the car is not overheating "
                "and there is no rattle. The reduced-power mode exists to get "
                "you off the road safely, not to get you through the week. A "
                "misfire left to run washes fuel past the rings and into the "
                "catalytic converter, and a catalyst is one of the more "
                "expensive things on the car to replace. A cold-start rattle "
                "on an N20 is the one case where we would rather you called "
                "for a tow: a chain that has jumped takes the valves with it.",
                f"Before any of this, check the VIN against NHTSA's recall "
                f"lookup. Several of the components above have been the "
                f"subject of BMW recalls or extended warranties, and if yours "
                f"is covered the dealer performs the repair at no charge; we "
                f"will tell you if that is the case before we quote. Otherwise, "
                f"the diagnosis is where the money is saved, and it is where "
                f"every {link(HUB, 'BMW repair')} here begins.",
            ]),
        ],
        "further": [MAINTENANCE, COSTS, CASES],
        "cta_heading": "Message on the dash?",
        "cta_text": "Do not clear it. Call with the year, the engine and when it happened, and we will tell you what we would test first.",
    },
    {
        "slug": COSTS,
        "hub": HUB,
        "cluster": CLUSTER,
        "sources": [src.FTC_WARRANTY, src.FTC_MAGMOSS, src.ZF_OIL, src.CARFAX],
        "title": "Why BMW Repair Costs What It Does | German Performance",
        "description": (
            "Parts tiers, labor that is really about access, the coding that "
            "finishes the job and why BMW jobs cluster, from the technicians who "
            "write the estimates."),
        "eyebrow": EYEBROW,
        "h1": 'Why BMW Repair Costs <span class="accent">What It Does</span>',
        "dek": (
            "A BMW is not expensive to fix because of the badge. It is expensive "
            "when the wrong part goes in, when the labor is paid twice, or when "
            "the coding is left out of the quote. Here is what moves the bill."),
        "intro": (
            f"There are no prices in this article, on purpose. A number "
            f"without a diagnosis is a guess, and we do not quote guesses. "
            f"What we can do is show you the estimate from the inside: where "
            f"the parts line comes from, why the labor line on a BMW is about "
            f"reaching the part rather than the part itself, what the coding "
            f"step is and why a quote without it is not for the whole job, and "
            f"why the work on these cars tends to arrive in clusters. If you "
            f"understand those four things you can read any BMW estimate, ours "
            f"included, and know whether it is a fair one. This is the "
            f"reasoning behind every estimate we write for {HUB_LINK}."),
        "sections": [
            ("Parts: genuine, OE supplier, or aftermarket", [
                "BMW does not make most of the parts in a BMW. Mahle and Mann "
                "make the filters, Lemf&ouml;rder the control arms and "
                "bushings, ZF the transmissions and steering, Bosch the "
                "ignition, injection and sensors, Continental and Pierburg "
                "much of the cooling and emissions hardware. A genuine part "
                "is one of those parts in a BMW box, tested to BMW's "
                "specification and priced accordingly. An OE-supplier part is "
                "the same part in the supplier's own box, and on most jobs "
                "that is where the value is. Aftermarket covers everything "
                "else, from companies that make an excellent equivalent to "
                "companies that make a shape.",
                "Our default on a BMW is genuine or OE-supplier, and the "
                "choice depends on the part. A water pump, a high-pressure "
                "fuel pump, a VANOS solenoid or anything the DME talks to "
                "should be genuine or the supplier's own; the tolerances are "
                "the point. A control arm from Lemf&ouml;rder is the same "
                "control arm BMW sells. On a fifteen-year-old car there are "
                "places, an expansion tank or a set of brake rotors, where a "
                "well-made aftermarket part is a sensible choice, and the "
                "estimate says which tier each line is and why. What we will "
                "not do is fit the cheapest part to win the quote. A part "
                "fitted twice costs more than a good part fitted once, and "
                "the second labor charge is the one nobody budgets for.",
            ]),
            ("Labor is about access", [
                "Labor is billed on time, and time on a BMW is mostly about "
                "getting to the part. The engine bay on an N55 335i is packed. "
                "The oil filter housing gasket is a small ring of rubber; it "
                "sits under the intake manifold, behind the coolant pipes, and "
                "the whole lot comes off to reach it. The valve cover gasket "
                "is similar. The thermostat on an N52 is behind the fan and the "
                "belt. A starter on some of the sixes lives under the intake. "
                "None of these parts is expensive. Reaching them is the job.",
                "This is where a lower quote can hide a shortcut. There are "
                "ways to do an oil filter housing gasket faster, and they "
                "involve not replacing the coolant-pipe seals that were "
                "disturbed on the way in, which is why the same car comes "
                "back with a coolant leak. A fair estimate includes the seals "
                "and gaskets that must be renewed because they were opened, "
                "and it says so.",
            ]),
            ("Why BMW jobs cluster", [
                "When the intake is off for the oil filter housing gasket, the "
                "valve cover gasket beside it is a small part and almost no "
                "extra time. Done separately six months later it is the whole "
                "labor charge again. The same is true of the water pump and "
                "thermostat on an N52, N54 or N55, which are removed together "
                "and should be replaced together; of the expansion tank and "
                "its hoses when the cooling system is drained; of the spark "
                "plugs when a coil is being replaced; of the rear main seal on "
                "a transmission that is already out.",
                f"A good BMW estimate tells you what else is exposed while a "
                f"job is open and lets you decide. That is not upselling. It "
                f"is the cheapest moment you will ever have to do work you "
                f"will otherwise do later at full price. It is also why we "
                f"photograph what we find and put the pictures in the "
                f"estimate: you should be able to see the weep on the gasket "
                f"we are recommending, not take our word for it. The general "
                f"version of this argument is in "
                f"{link('what-affects-german-car-repair-costs.html', 'what affects German car repair costs')}; "
                f"the BMW version is that these cars were designed to be "
                f"serviced in systems, and the estimate should be too.",
            ]),
            ("The coding is part of the job", [
                f"On a modern BMW, fitting the part is not the end of the "
                f"repair. A new battery has to be registered with ISTA so the "
                f"charging system stops compensating for the old one, and if "
                f"it is an AGM battery replacing a flooded one, coded as such; "
                f"skip it and the new battery is overcharged into an early "
                f"grave. A transmission service on the ZF 8HP is followed by "
                f"an adaptation reset, or it shifts worse than before. A "
                f"replaced control module, a steering-angle sensor after an "
                f"alignment, a camera after a windshield, an injector on an "
                f"N54 (which carries a calibration value the DME needs): all "
                f"coded. The {link(TRANSMISSION, 'transmission repair')} page "
                f"covers the adaptation step in more detail.",
                "A shop without the factory software cannot do any of this, "
                "so it either leaves the step out or sends the car somewhere "
                "that can, and the price you were quoted was never for the "
                "whole job. When you compare estimates, ask whether the coding "
                "is included. It is one line on ours, and it is not optional.",
            ]),
            ("The dealer, the independent, and the same BMW job", [
                f"The dealer and a specialist independent are doing the same "
                f"repair with, in our case, the same software and the same "
                f"tier of parts. The dealer's labor rate carries the building; "
                f"ours carries more than fifteen years of seeing the same engines "
                f"every week, which is worth more on the diagnostic than on the "
                f"wrench. The dealer is still the right place for a recall or "
                f"a warranty repair, and we will tell you when that is the "
                f"case. For everything else, federal law is clear: a "
                f"manufacturer cannot condition its warranty on using the "
                f"dealer for maintenance or repairs, and the FTC has warned "
                f"manufacturers, BMW among them, about implying otherwise. "
                f"Both FTC pages are in the sources below, and the fuller "
                f"comparison is in "
                f"{link(DEALER, 'dealership vs. independent shop')}.",
                ("callout",
                 "Ask any shop what its warranty on the work is before you "
                 "compare numbers. Ours is 12 months or 12,000 miles, parts "
                 "and labor, in writing. A lower quote with no warranty is "
                 "not a lower price; it is a bet."),
            ]),
            ("Deferred maintenance is the biggest line", [
                "The largest BMW bills we write are almost never for one "
                "failure. They are for a small problem that was left. An oil "
                "filter housing gasket that weeps for a year drips onto the "
                "serpentine belt; the belt shreds, and on the N20 and N55 it "
                "can be drawn into the front crank seal and into the engine. "
                "A \"lifetime\" transmission fluid that was never changed "
                "takes the mechatronic sleeve and then the clutch packs with "
                "it. An electric water pump that was already slowing fails on "
                "the interstate and the engine overheats; on an aluminium "
                "engine that is a head gasket at best.",
                f"None of this is a reason to fear the car. It is a reason to "
                f"treat the schedule as real, including the parts of it BMW "
                f"does not count, which we set out in "
                f"{link(MAINTENANCE, 'the BMW maintenance guide')}. It also "
                f"shows up at sale: we report every service to CARFAX, and a "
                f"documented BMW is worth real money to the next owner in a "
                f"way a mystery car never is.",
            ]),
            ("How to get a real number", [
                f"Call with the year, the model, the engine if you know it, "
                f"and what the car is doing. We will tell you what we would "
                f"check first and what the diagnosis should take. A technician "
                f"then runs ISTA and a physical inspection, and you get a "
                f"written estimate with photographs of what was found, each "
                f"line marked genuine, OE-supplier or aftermarket, with the "
                f"coding included. Nothing starts until you approve it, and "
                f"if the job turns up something we did not expect, we stop and "
                f"call. That is the whole of how we price "
                f"{link(HUB, 'BMW repair')}, and it is the only honest way we "
                f"know to do it.",
            ]),
        ],
        "further": [MAINTENANCE, DRIVETRAIN, CASES],
        "cta_heading": "Want a real number for your BMW?",
        "cta_text": "Call with the year, the model and the symptom. We will tell you what we would check first and what finding out should take.",
    },
    CASES_POST,
]
