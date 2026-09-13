"""Mercedes-Benz service pages, built by tools/build_service_pages.py.

One dict per page (the C, E and S-Class, GLC, GLE and AMG). Every technical claim is a documented
characteristic of the marque; nothing about pricing, turnaround or
certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points,
faq_head, faqs, cta, cta_sub.
"""

PAGES = (
{
 "slug": "mercedes-cooling-system-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "h1": ("MERCEDES", "COOLING", "SYSTEM"),
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
