"""BMW service pages, built by tools/build_service_pages.py.

One dict per page (the 3, 5 and 7 Series, X3, X5 and M cars). Every technical
claim is a documented characteristic of the marque; nothing about pricing,
turnaround or certification is invented. The dict shape is the one
build_service_pages renders: slug, brand, [marque], h1 (three lines), title,
desc, sub, cards_head, cards_sub, cards, why_head, why_lead, why_points,
faq_head, faqs, cta, cta_sub.
"""

WARRANTY = (
    "No. Federal law protects your right to have routine maintenance and "
    "repairs performed by an independent shop without voiding a manufacturer "
    "warranty, as long as the correct specification parts and fluids are used "
    "and the work is documented. You leave with a written record of what was "
    "done.")

PAGES = (
{
 "slug": "bmw-oil-change-snellville-ga.html",
 "brand": "BMW",
 "h1": ("BMW", "OIL", "CHANGE"),
 "title": "BMW Oil Change Snellville GA | German Performance",
 "desc": ("BMW oil change in Snellville, GA. Longlife-approved oil for your "
          "engine code, OEM cartridge filter, leak check and CBS reset. "
          "Call (678) 395-7459."),
 "sub": ("BMW oil service in Snellville, GA — for the 3, 5 and 7 Series, the X "
         "models, Z4 and M cars. The Longlife approval your engine calls for, "
         "an OEM cartridge filter, the leaks these engines are known for "
         "checked, and CBS reset so the car's own schedule stays right."),
 "cards_head": ("A PROPER BMW", "OIL SERVICE"),
 "cards_sub": ("BMW publishes an approval for every engine, sets its own "
               "interval, and on most models since the mid-2000s gives you no "
               "dipstick. Each of those is a place a generic oil change goes "
               "wrong."),
 "cards": [
   ("The Right Longlife Approval",
    "BMW's Longlife specifications are not interchangeable. LL-01 covers most "
    "of the older gasoline range, LL-04 the diesels and many turbocharged "
    "engines, and the newest engines call for the thin LL-17 FE+ grade. We "
    "fill the approval and viscosity BMW lists for your engine code, not a "
    "full synthetic that happens to say European on the jug."),
   ("An Interval That Suits the Engine",
    "CBS will stretch the reminder toward 15,000 miles. The turbocharged N20, "
    "N55, B48 and B58 and every M engine are better served at 7,000 to 10,000 "
    "— oil that has spent a year in a hot turbo engine is not the oil that "
    "went in. We set the reminder to the interval we actually recommend, and "
    "tell you why."),
   ("Cartridge Filter and Drain Washer",
    "An OEM or OEM-equivalent cartridge filter with new O-rings on the housing "
    "cap, and a new crush washer on the drain plug. Reusing either is how a "
    "BMW ends up with a slow drip on the garage floor a month later."),
   ("Level Set Electronically",
    "Most BMWs built since the mid-2000s have no dipstick; the level is read "
    "by a sensor and shown through iDrive, and it only reads correctly with "
    "the engine warm. We verify it that way before handover rather than "
    "trusting the fill quantity in the book."),
   ("The Leaks We Look For",
    "The oil filter housing gasket, the oil cooler gasket beneath it and the "
    "valve cover gasket are the three leaks these engines are known for, and "
    "a leak from the housing lands on the serpentine belt. We check all three "
    "while the car is up and tell you what we found."),
   ("CBS Reset and Inspection",
    "Condition Based Service is reset through BMW-compatible diagnostics so "
    "the car's own schedule stays accurate — the vehicle check, brake fluid "
    "and microfilter counters included where they are due. The car gets a "
    "multi-point inspection while it is on the lift."),
 ],
 "why_head": ("BMW OIL", "DONE RIGHT"),
 "why_lead": ("The difference between a BMW oil change and an ordinary one is "
              "not the oil. It is the approval, the interval, the filter "
              "housing that leaks if its seals are reused, and the fact that "
              "you cannot check the result with a dipstick. We treat each of "
              "those as part of the job."),
 "why_points": [
   "BMW Longlife-approved oil matched to your engine code and year",
   "Intervals set for turbocharged and M engines, not the CBS maximum",
   "OEM cartridge filters with new housing O-rings and drain washer",
   "Electronic oil level verified at operating temperature before handover",
   "Filter housing, oil cooler and valve cover gaskets inspected every time",
   "CBS reset through BMW-compatible diagnostics, and a written record",
 ],
 "faq_head": ("BMW OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a BMW need an oil change?",
    "BMW's Condition Based Service will typically call for a change somewhere "
    "between 10,000 and 15,000 miles. For the turbocharged engines and the M "
    "cars we recommend 7,000 to 10,000 miles or once a year, whichever comes "
    "first. Extended intervals are where the timing-chain and oil-consumption "
    "problems on these engines tend to start."),
   ("What oil does my BMW take?",
    "It depends on the engine. Most older gasoline engines call for BMW "
    "Longlife-01, many turbocharged and diesel engines for Longlife-04, and "
    "the newest B-series engines for the thinner Longlife-17 FE+ grade. The "
    "approval is in your owner's manual and we confirm it against the engine "
    "code before we fill."),
   ("Why does my BMW have no dipstick?",
    "Since the mid-2000s most BMWs read the oil level with a sensor in the pan "
    "and show it through iDrive. It only reads accurately with the engine at "
    "operating temperature on level ground, which is how we check it. If the "
    "display ever shows the level dropping between services, that is worth a "
    "call rather than a top-up."),
   ("Is it normal for a BMW to use oil between changes?",
    "Some consumption on a turbocharged engine is normal and BMW allows for "
    "it. What matters is the rate. A car that needs a quart every few thousand "
    "miles should be looked at — the usual causes are the valve cover gasket, "
    "the filter housing gasket or the crankcase ventilation valve, none of "
    "which are expensive to catch early."),
   ("Will you reset the service light?",
    "Yes. We reset Condition Based Service through BMW-compatible diagnostics, "
    "so the oil counter and the other service items are correct, rather than "
    "clearing the message with a generic tool and leaving the schedule wrong."),
   ("Will an independent oil change affect my BMW warranty?", WARRANTY),
 ],
 "cta": ("BMW OIL SERVICE", "DUE?"),
 "cta_sub": "Call with the model and year — we will confirm the Longlife approval your engine needs.",
},
{
 "slug": "bmw-suspension-repair-snellville-ga.html",
 "brand": "BMW",
 "h1": ("BMW", "SUSPENSION", "REPAIR"),
 "title": "BMW Suspension Repair Snellville GA | German Performance",
 "desc": ("BMW suspension repair in Snellville, GA. Thrust arm and tension strut "
          "bushings, struts, EDC dampers, X5 air springs and alignment to spec. "
          "Call (678) 395-7459."),
 "sub": ("BMW suspension repair in Snellville, GA — control arms and bushings, "
         "struts and shocks, EDC adaptive dampers, rear air springs and the "
         "alignment that follows, on the 3, 5 and 7 Series, X models and M "
         "cars."),
 "cards_head": ("BMW SUSPENSION", "REPAIR"),
 "cards_sub": ("BMW suspensions are precise when they are right and vague when "
               "they are not. The parts that go are well known by chassis: the "
               "fluid-filled front bushings on the older cars, the tension "
               "struts on the newer ones, the rear subframe mounts, and the air "
               "springs under the X5."),
 "cards": [
   ("Thrust Arm and Tension Strut Bushings",
    "On the E-chassis 3 and 5 Series the front thrust arm bushings are "
    "hydraulic-filled and fail with a shimmy under braking; on the F and G "
    "cars the tension struts and their bushings do the same job and fail the "
    "same way. We replace them with OEM or OEM-equivalent parts, not the "
    "softer aftermarket bushing that lasts a year."),
   ("Struts, Shocks and EDC Dampers",
    "Conventional dampers are replaced in axle pairs with new mounts and "
    "bearings. Cars with Electronic Damper Control carry adaptive dampers that "
    "need the correct part for the car and, on some models, coding afterwards. "
    "We fit what the car was built with and finish the job through "
    "BMW-compatible diagnostics where it needs it."),
   ("Rear Subframe and Trailing Arm Bushings",
    "The rear subframe mounts and trailing arm bushings on the 3 Series are a "
    "known wear point that shows up as a clunk over bumps and a rear end that "
    "feels loose in corners. They are a press job done properly with the "
    "subframe supported, not a shortcut."),
   ("xDrive and Ride Height",
    "xDrive cars use different front struts and control arms from the "
    "rear-drive version of the same model, and the ride-height sensors on "
    "cars with adaptive headlights or air suspension have to read correctly "
    "afterwards. We fit the right parts for the drivetrain and check the "
    "sensors."),
   ("X5 and X6 Air Suspension",
    "The rear air springs on the X5 and X6 crack with age and the compressor "
    "works itself to death keeping up. A car that sits low at the back "
    "overnight is telling you. We replace the springs and, where it is tired, "
    "the compressor, with OEM-equivalent parts."),
   ("Alignment to BMW Specification",
    "Every suspension repair ends with a four-wheel alignment to BMW's figures "
    "for the model, with the car loaded the way BMW specifies. An arm swap "
    "without an alignment eats a set of tires."),
 ],
 "why_head": ("BMW SUSPENSION", "DONE RIGHT"),
 "why_lead": ("A BMW that wanders, shimmies under braking or clunks over bumps "
              "almost always has one of a short list of worn parts. Knowing "
              "the list by chassis, fitting parts that last, and aligning the "
              "car afterwards is the difference between fixing it once and "
              "fixing it twice."),
 "why_points": [
   "Thrust arm and tension strut bushings — the wear point on every 3 and 5 Series",
   "Struts and shocks in pairs with new mounts; EDC dampers coded where required",
   "Rear subframe and trailing arm bushings pressed properly",
   "Correct parts for xDrive, and ride-height sensors verified afterwards",
   "X5 and X6 rear air springs and compressors",
   "Four-wheel alignment to BMW's specification after every repair",
 ],
 "faq_head": ("BMW SUSPENSION", "FAQ"),
 "faqs": [
   ("Why does my BMW shimmy when I brake?",
    "On most 3 and 5 Series it is the front thrust arm or tension strut "
    "bushings. They are filled with fluid and lose it with age, and the arm "
    "can then move under braking load; the steering wheel shakes and the car "
    "feels loose. It is one of the most common repairs on these cars and a "
    "straightforward one."),
   ("What is EDC and does it change the repair?",
    "Electronic Damper Control is BMW's adaptive damping — the dampers adjust "
    "electronically to the road and the driving mode. Replacing them means "
    "fitting the correct adaptive part for the car rather than a conventional "
    "damper, and on some models coding the system afterwards with "
    "BMW-compatible diagnostics. A conventional damper on an EDC car leaves a "
    "fault and a hard ride."),
   ("Why does my X5 sit low at the back in the morning?",
    "The rear air springs. They are rubber, they crack with age and they let "
    "the air out overnight; the compressor pumps the car back up when you "
    "start it, until it wears out too. Replacing the springs is the repair; "
    "if the compressor has been running constantly for a while it may need "
    "replacing as well."),
   ("What causes a clunk from the rear over bumps?",
    "Usually the rear subframe mounts or the trailing arm bushings, both of "
    "which are known wear points on the 3 Series in particular. Sway bar end "
    "links and shock mounts are the other candidates. We find it on the lift "
    "before we replace anything."),
   ("Do I need an alignment after suspension work?",
    "Yes. Any control arm, strut or bushing replacement changes the geometry, "
    "and BMW's tolerances are tight. We align the car to BMW's specification "
    "after the repair. Skipping it costs a set of tires."),
   ("Do you use factory parts?",
    "OEM or OEM-equivalent parts from the manufacturers that supply BMW. "
    "Bushings and arms are where cheap parts show up fastest — softer rubber "
    "that fails within a year — so we do not use them."),
 ],
 "cta": ("BMW SUSPENSION", "FEELING LOOSE?"),
 "cta_sub": "Call and describe it — the symptom usually names the part on a BMW.",
},
)
