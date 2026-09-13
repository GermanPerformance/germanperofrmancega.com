"""Mercedes-Benz service pages, built by tools/build_service_pages.py.

One dict per page (the C, E and S-Class, GLC, GLE and AMG). Every technical claim is a documented
characteristic of the marque; nothing about pricing, turnaround or
certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points,
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
 "slug": "mercedes-oil-change-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "h1": ("MERCEDES", "OIL", "CHANGE"),
 "title": "Mercedes Oil Change Snellville GA | German Performance",
 "desc": ("Mercedes oil change in Snellville, GA. MB 229.5 or 229.51-approved "
          "oil by engine, OEM cartridge filter, leak check and ASSYST reset. "
          "Call (678) 395-7459."),
 "sub": ("Mercedes-Benz oil service in Snellville, GA — for the C, E and "
         "S-Class, GLC, GLE, GLS, CLA and AMG. The MB approval sheet your "
         "engine is listed on, an OEM filter, the leaks these engines develop "
         "checked, and the ASSYST reminder reset properly."),
 "cards_head": ("A PROPER MERCEDES", "OIL SERVICE"),
 "cards_sub": ("Mercedes-Benz approves oil by sheet number, not viscosity, runs "
               "its own service schedule, and on most current models gives you "
               "no dipstick. A generic oil change gets at least one of those "
               "wrong."),
 "cards": [
   ("The Right MB Approval Sheet",
    "Mercedes publishes approval sheets: 229.5 for most gasoline engines, the "
    "low-ash 229.51 and 229.52 for diesels and engines with particulate "
    "filters, and 229.71 for the newest low-viscosity applications. We fill "
    "the sheet your engine is listed on. An oil that meets a general standard "
    "but is not on the sheet is the wrong oil."),
   ("Cartridge Filter From the Top",
    "On most Mercedes engines the filter is a cartridge under a cap on top of "
    "the engine, with its own sealing rings. We fit an OEM or OEM-equivalent "
    "element with new rings and a new drain plug washer, so the housing does "
    "not weep afterwards."),
   ("Level Confirmed the Mercedes Way",
    "Newer models have no dipstick; the level is read through the instrument "
    "cluster, and only correctly with the engine warm and the car level. "
    "Older models with a dipstick still need the reading taken at "
    "temperature. We confirm it either way before the car leaves."),
   ("The Leaks These Engines Get",
    "The M272 and M273 V6 and V8 are known for oil cooler seals that leak "
    "into the engine valley and for valve cover gaskets; the turbocharged "
    "M276 and M278 for the oil feed lines to the turbos. We look at all of "
    "them while the car is up and tell you what we found."),
   ("ASSYST Service Reset",
    "The maintenance reminder runs on Mercedes' ASSYST Plus schedule, which "
    "alternates Service A and Service B. We reset it through "
    "Mercedes-compatible diagnostics so the car's own schedule and the next "
    "service type stay correct, rather than clearing the message."),
   ("Diesel and AMG Handled Properly",
    "BlueTEC diesels need the low-ash 229.51 or 229.52 grades to protect the "
    "particulate filter. AMG engines run larger capacities and are hard on "
    "oil. Both get the approval and the interval Mercedes specifies, not a "
    "shortcut."),
 ],
 "why_head": ("MERCEDES OIL", "DONE RIGHT"),
 "why_lead": ("An oil change on a Mercedes is a checklist: the approval sheet, "
              "the cartridge and its rings, the level without a dipstick, the "
              "leaks these engines develop, and a reset that keeps ASSYST "
              "honest. Miss one and the car comes back."),
 "why_points": [
   "MB 229.5, 229.51, 229.52 or 229.71 oil matched to your engine's approval sheet",
   "OEM cartridge filters with new sealing rings and drain washer",
   "Electronic oil level confirmed at operating temperature before handover",
   "Oil cooler seals, valve covers and turbo lines inspected for the known leaks",
   "ASSYST Plus reset through Mercedes-compatible diagnostics",
   "Low-ash oil for BlueTEC diesels, correct capacity for AMG engines",
 ],
 "faq_head": ("MERCEDES OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a Mercedes need an oil change?",
    "Mercedes' ASSYST Plus schedule calls for service roughly every 10,000 "
    "miles or once a year, alternating between the smaller Service A and the "
    "larger Service B. That is the ceiling. Cars that do short trips, sit for "
    "long periods or are driven hard are better served around 7,500 miles, "
    "and on a car that is driven little the annual limit matters more than "
    "the mileage."),
   ("What oil does my Mercedes take?",
    "Mercedes approves oil by sheet number. Most gasoline engines take an oil "
    "carrying the 229.5 approval, diesels and engines with particulate "
    "filters need the low-ash 229.51 or 229.52 grades, and some of the newest "
    "engines call for 229.71. The sheet number matters more than the brand or "
    "the viscosity on the label; we confirm it against your engine before "
    "filling."),
   ("What is the difference between Service A and Service B?",
    "Service A is the oil and filter change with an inspection and fluid "
    "checks. Service B adds the cabin filter, brake fluid and a longer "
    "checklist. The car alternates between them and tells you which is due; "
    "we reset the reminder so the next one it asks for is the right one."),
   ("My Mercedes has no dipstick — how do you check the level?",
    "Through the instrument cluster, with the engine at operating "
    "temperature and the car on level ground, which is the only way the "
    "reading is accurate. We verify it before the car leaves rather than "
    "relying on the fill quantity in the book."),
   ("Why is my Mercedes leaking oil?",
    "On the V6 and V8 engines of the 2000s and early 2010s it is usually the "
    "oil cooler seals, which leak into the valley between the cylinder banks, "
    "or the valve cover gaskets. On the turbocharged engines that followed, "
    "the turbo oil feed lines are a known point. We look for all of them at "
    "every oil service and tell you what we found, and what it does and does "
    "not need."),
   ("Will an independent oil change affect my Mercedes warranty?", WARRANTY),
 ],
 "cta": ("MERCEDES OIL SERVICE", "DUE?"),
 "cta_sub": "Call with the model and year — we will confirm the approval sheet your engine is on.",
},
{
 "slug": "mercedes-brake-service-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "h1": ("MERCEDES", "BRAKE", "REPAIR"),
 "title": "Mercedes Brake Repair Snellville GA | German Performance",
 "desc": ("Mercedes brake repair in Snellville, GA. Pads, rotors, wear sensors, "
          "SBC and electric parking brake service mode, DOT 4 Plus flush. "
          "Call (678) 395-7459."),
 "sub": ("Mercedes-Benz brake repair in Snellville, GA — pads, rotors, "
         "sensors, fluid and the electronics around them, on everything from "
         "a C-Class to an AMG. Including the Sensotronic system on the models "
         "that have it, which has to be put to sleep before anyone touches a "
         "caliper."),
 "cards_head": ("MERCEDES BRAKE", "SERVICE"),
 "cards_sub": ("Mercedes brakes are conventional in the parts and specific in "
               "the procedure: wear sensors on both axles, an electric parking "
               "brake that needs a service mode, rotors that are replaced "
               "rather than machined, and on some models a brake-by-wire "
               "system with rules of its own."),
 "cards": [
   ("Pads and Rotors Together",
    "Mercedes rotors are built light and wear with the pads; the minimum "
    "thickness is stamped on the rotor hat and most reach it by the second "
    "set of pads. We measure every rotor and replace it at or near the limit "
    "rather than machining it thin, and fit OEM or OEM-equivalent pads "
    "matched to the car."),
   ("Wear Sensors on Both Axles",
    "Most Mercedes carry a wear sensor at the front and one at the rear, and "
    "once a sensor has tripped the warning it is finished. We replace the "
    "sensors with the pads so the light stays off, and so the next warning "
    "is a real one."),
   ("SBC Put Into Service Mode",
    "The E-Class, CLS and SL of the mid-2000s use Sensotronic Brake Control, "
    "a brake-by-wire system that can clamp the calipers on its own. It has to "
    "be deactivated with Mercedes-compatible diagnostics before the pads come "
    "out, and its activation counter read — if the pump is near its limit "
    "you should hear it from us, not from a warning."),
   ("Electric Parking Brake Service Mode",
    "On the current cars the rear calipers carry the parking brake motors. "
    "The rear pads cannot be changed without putting the system into service "
    "mode and cycling it afterwards; forcing the pistons back damages the "
    "actuators. We do it through the diagnostics the car expects."),
   ("AMG and Performance Brakes",
    "AMG cars carry larger rotors, some of them composite, and pads with a "
    "compound that squeals and dusts by design. We fit the specified parts, "
    "measure the rotors to their own limits, and can advise on a quieter "
    "street compound if that suits how the car is used."),
   ("DOT 4 Plus Fluid Flush",
    "Mercedes specifies its own DOT 4 Plus fluid on a two-year interval, "
    "because the fluid absorbs water and the ABS and stability control depend "
    "on it. We flush with the specified fluid and bleed through the system, "
    "the stability control unit included where the car requires it."),
 ],
 "why_head": ("MERCEDES BRAKES", "DONE RIGHT"),
 "why_lead": ("A Mercedes brake job that ignores the electronics ends with a "
              "warning light, a parking brake that will not release, or on an "
              "SBC car a system that clamps a caliper mid-repair. The parts "
              "are straightforward; the procedure is where the experience "
              "shows."),
 "why_points": [
   "Rotors measured against the stamped minimum and replaced, not machined thin",
   "Wear sensors on both axles replaced with the pads",
   "SBC deactivated and its activation counter read before any caliper work",
   "Electric parking brake put in service mode and cycled after rear pads",
   "OEM or OEM-equivalent pads and rotors, AMG compounds where specified",
   "DOT 4 Plus flush on Mercedes' two-year schedule, stability control bled where required",
 ],
 "faq_head": ("MERCEDES BRAKE REPAIR", "FAQ"),
 "faqs": [
   ("How do I know my Mercedes brakes need work?",
    "The wear sensor puts a message in the instrument cluster before the pads "
    "are gone, and that is the earliest reliable warning. A pulsing pedal, a "
    "pull to one side, a grinding noise or a longer pedal than you are used "
    "to all mean it is past time. We measure pads and rotors at every service "
    "so you usually hear it from us first."),
   ("Why do Mercedes rotors get replaced with the pads?",
    "They are built thin for weight and they wear along with the pads; by the "
    "second set they are usually at or under the minimum thickness stamped on "
    "the rotor. Machining a rotor that close to the limit leaves it below it. "
    "Replacing them with the pads is what the car was designed for."),
   ("What is SBC and why does it matter for a brake job?",
    "Sensotronic Brake Control is the brake-by-wire system on the 2003 to "
    "2006 E-Class and CLS and the SL of that era. It can apply the brakes on "
    "its own, so it has to be deactivated with Mercedes-compatible "
    "diagnostics before anyone opens a caliper. It also counts its own "
    "activations and warns when the pump is near the end of its service "
    "life; we read that counter and tell you where yours stands."),
   ("Can you change the rear pads on a car with an electric parking brake?",
    "Yes, but only with the system in service mode. The parking brake motors "
    "sit on the rear calipers, and pushing the pistons back against them "
    "damages the actuators. We put the system into service mode, do the "
    "work, and cycle it afterwards so it releases and holds correctly."),
   ("How often should the brake fluid be changed?",
    "Mercedes specifies every two years regardless of mileage, using its DOT "
    "4 Plus fluid. Brake fluid absorbs water from the air, which lowers its "
    "boiling point and corrodes the ABS unit from the inside. It is part of "
    "Service B on the schedule for that reason."),
   ("Why do my AMG brakes squeal and leave so much dust?",
    "The pad compound. Performance pads are made to bite hard when they are "
    "hot, and they squeal and dust at street temperatures as a result. It is "
    "normal, not a fault. If the car is used mostly on the road we can fit a "
    "quieter compound; if it sees track days, keep the specified one."),
 ],
 "cta": ("MERCEDES BRAKES", "DUE?"),
 "cta_sub": "Call with the model and year — we will tell you what the job involves on your car.",
},
{
 "slug": "mercedes-cooling-system-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "h1": ("MERCEDES COOLING", "SYSTEM", "REPAIR"),
 "title": "Mercedes Cooling System Repair Snellville | German Performance",
 "desc": ("Mercedes-Benz cooling system repair in Snellville, GA. Thermostats, "
          "water pumps, auxiliary pumps, radiators and MB-spec coolant. "
          "Call (678) 395-7459."),
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
)
