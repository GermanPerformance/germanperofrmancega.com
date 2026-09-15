"""The BMW hub: what the shop sees on a BMW and every service it performs
on one, consolidated from the six BMW job pages retired on 2026-09-15. Six cards,
two rows of three; the battery job lives with diagnostics and electrical.

Every technical claim is a documented characteristic of the marque;
nothing about pricing, turnaround or certification is invented. The
credential sentence in "closing" is the owner's (2026-09-15).
"""

from posts.common import CEL, OIL, TRANSMISSION, TUNE_UP

HUB = {
 "slug": "bmw-repair-snellville-ga.html",
 "make": "bmw",
 "brand": "BMW",
 "possessive": "BMW",
 "eyebrow": "BMW Specialists · Snellville, GA · Since 2010",
 "desc": ("Independent BMW repair in Snellville, GA. ISTA factory diagnostics, OEM parts, "
          "ASE-certified technicians, 12-month warranty. Serving Gwinnett County since 2010."),
 "sub": ("Most people find us because something on their BMW is behaving oddly and the last "
         "shop wanted to start replacing parts to find out why. We diagnose first, using the "
         "same software the dealer runs, and tell you what we actually found."),
 "tool": "ISTA",
 "before": [
   ("A warning you can't interpret",
    "BMW dashboards report symptoms, not causes. A drivetrain malfunction message can mean a coil, a fuel injector, a boost leak or a timing issue, and a generic code reader will not tell them apart."),
   ("A repair bill that keeps growing",
    "The expensive version of a cheap diagnosis is paying for two or three parts before the right one gets replaced. That is the pattern we most often hear about from people calling us second."),
   ("Nobody explaining the why",
    "Being told a car needs a part is not the same as understanding what failed and what happens if it waits. You should get both."),
 ],
 # (title, body, the make-agnostic page that covers the same job, or None)
 "services": [
   ("Diagnostics, electrical and the battery",
    "Every job starts on the factory software. ISTA talks to every control module, shows live "
    "data and walks the technician through BMW's own test plan for the fault, which is how a "
    "drivetrain malfunction gets traced to one coil, one injector or one boost leak rather than "
    "a parts list. Electrical faults get the same treatment: a parasitic-draw test when the "
    "battery keeps dying, and a new AGM battery of the correct rating registered to the "
    "Intelligent Battery Sensor, because an unregistered battery is overcharged as if it were "
    "the old one and dies early. You get a written report with photographs before anything is "
    "approved.", CEL),
   ("Oil service to the Longlife approval",
    "BMW's Longlife specifications are not interchangeable: LL-01 for most of the older gasoline "
    "range, LL-04 for the diesels and many turbocharged engines, LL-17 FE+ for the newest B-series. "
    "We fill the approval BMW lists for your engine code, fit an OEM cartridge filter with new "
    "O-rings, set the level electronically with the engine warm, check the three leaks these "
    "engines are known for, and reset Condition Based Service properly. The turbocharged N20, "
    "N55, B48, B58 and every M engine are better served at 7,000 to 10,000 miles than the "
    "15,000 the reminder will stretch to.", OIL),
   ("Cooling system: pump, thermostat, tank",
    "Plastic is the weak point. The electric water pump on the N52, N54 and N55, the "
    "map-controlled thermostat, the expansion tank and the radiator end tanks all age on a "
    "schedule and fail gradually, then suddenly. We pressure-test the system cold to find a "
    "seep before it is a puddle, replace the pump and thermostat together when one has failed, "
    "and fill with the BMW-specification coolant, never a universal product mixed into it.", None),
   ("Suspension: thrust arms, EDC, air springs",
    "On the E-chassis 3 and 5 Series the hydraulic thrust arm bushings fail with a shimmy under "
    "braking; on the F and G cars the tension struts do the same. Cars with Electronic Damper "
    "Control need the correct adaptive damper and, on some models, coding afterwards. The rear "
    "air springs on the X5 and X6 crack with age and a car that sits low at the back overnight "
    "is telling you. Every repair ends with a four-wheel alignment to BMW's figures.", None),
   ("Transmission service on the ZF 6HP and 8HP",
    "The fluid BMW once called lifetime is not. We drain, inspect the pan for debris, replace the "
    "filter and gasket, refill with the ZF-approved fluid and set the level at the specified "
    "temperature, then reset the adaptations so the car relearns its shifts. Harsh or delayed "
    "shifts are tested at the mechatronic unit and solenoids before anything is condemned; a "
    "valve body repair is often the answer, a rebuild rarely the first one.", TRANSMISSION),
   ("Spark plugs, coils and misfires",
    "A misfire is diagnosed on live data before anything is replaced, because plugs, coils, "
    "injectors and compression all produce one. The N20, N54, N55, B58 and S55 each take a "
    "different plug and heat range; we fit the OEM specification, test every coil while the "
    "cover is off, check the valve cover gasket and plug tubes for the oil that kills coils, "
    "and road-test before the car leaves.", TUNE_UP),
 ],
 "known": [
   ("Cooling system failures",
    "Plastic thermostat housings, water pumps and expansion tanks are a known weak point across the N-series and B-series engines. They tend to fail gradually and then suddenly, which is why we pressure-test rather than wait for a leak to be visible."),
   ("Oil leaks from the valve cover and filter housing",
    "The gaskets harden with heat and age. Oil dripping onto a hot exhaust is the burning smell owners usually describe, and catching it early keeps it a gasket job rather than a contaminated belt or damaged sensor."),
   ("Timing chain concerns on N20 and N26 engines",
    "Chain guide wear on certain model years produces a distinctive rattle on cold start. This is worth diagnosing promptly, because the failure mode is severe."),
   ("Carbon buildup on direct-injection engines",
    "No fuel washes the back of the intake valves, so deposits accumulate and cause rough idle, misfires and lost power. Walnut blasting removes them without damaging the port."),
   ("Electrical faults and battery registration",
    "A new battery must be registered to the charging system or the car will overcharge it and shorten its life. It is a coding step, not a parts step, and it is routinely skipped."),
 ],
 "reviews": ("nageeb", "sahir"),
 "faqs": [
  ("Do I have to take my BMW to the dealer for service?",
   "No. Under the Magnuson-Moss Warranty Act a dealer cannot void your factory warranty because an independent shop performed routine maintenance or repairs, provided the work is done correctly with appropriate parts. We document everything so your records are dealer-presentation ready."),
  ("Do you use the same diagnostic software as a BMW dealer?",
   "Yes. We run ISTA, which gives us access to every control module, live data, adaptations and coding, rather than the generic fault codes a basic OBD-II scanner reads."),
  ("What is the drivetrain malfunction message on my BMW?",
   "It is the car protecting itself after detecting a fault it considers serious enough to reduce power. The underlying cause varies widely -- ignition, fuel delivery, boost control and sensors are all candidates -- so it needs a proper scan rather than a guess."),
  ("How often does a BMW need an oil change?",
   "Condition Based Service will stretch the reminder toward 15,000 miles. On the turbocharged N20, N55, B48 and B58 engines and on every M engine we recommend 7,000 to 10,000 miles or once a year, because oil that has spent a year in a hot turbocharged engine is not the oil that went in. We set the reminder to the interval we recommend and tell you why."),
  ("Why does a new BMW battery need to be registered?",
   "The Intelligent Battery Sensor tracks the battery's age and adjusts the charging strategy to it. Register the new battery and the car charges it correctly; skip it and the alternator treats the new battery as an old one and overcharges it, which shortens its life. Registration is done through ISTA and is part of every battery we fit."),
  ("Can you reset the BMW service indicator?",
   "Yes. Every BMW service we perform includes the correct Condition Based Service reset, so your dashboard reflects what has actually been done."),
 ],
 "models": "1, 2, 3, 4, 5, 6, 7 and 8 Series, X1 through X7, Z4, and the full M range.",
 "band_head": ("NOT SURE WHAT'S WRONG?", "THAT'S THE POINT OF CALLING."),
 "cta_sub": "Describe what the car is doing. We'll tell you what we'd check first.",
 "closing": ("German Performance has worked only on German cars since 2010, more than 10,000 of them "
             "through this shop. The technicians are ASE-certified and Mercedes-Benz factory-trained, "
             "one an ASE Master Technician with the advanced engine diagnostics certification, and "
             "every BMW repair leaves with a written 12-month, 12,000-mile parts-and-labor warranty. "
             "Serving Snellville, Loganville, Grayson, Lawrenceville and all of Gwinnett County."),
}
