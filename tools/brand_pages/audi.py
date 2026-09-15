"""The Audi hub: what the shop sees on an Audi and every service it performs
on one, consolidated from the three Audi job pages retired on 2026-09-15.

Every technical claim is a documented characteristic of the marque;
nothing about pricing, turnaround or certification is invented. "VW 502 00"
and its siblings are the names of the oil standards, which check_faq.py
allows on an Audi page.
"""

from posts.common import BRAKES, CEL, OIL

HUB = {
 "slug": "audi-repair-snellville-ga.html",
 "make": "audi",
 "brand": "Audi",
 "possessive": "Audi",
 "eyebrow": "Audi Specialists · Snellville, GA · Since 2010",
 "desc": ("Independent Audi repair in Snellville, GA. ODIS and VCDS diagnostics, OEM parts, "
          "ASE-certified technicians, 12-month warranty. Gwinnett County since 2010."),
 "sub": ("Audi shares a great deal of engineering with Volkswagen, which means the failure "
         "patterns are well understood by anyone who works on both. We do, and we confirm what "
         "your car actually has by VIN before quoting anything."),
 "tool": "ODIS and VCDS",
 "before": [
   ("Oil consumption you were told is normal",
    "Some consumption is normal. A quart every thousand miles usually is not, and it has identifiable causes worth investigating."),
   ("Belt or chain, and nobody is sure which",
    "The interval and the risk are completely different between the two, and it depends on the engine rather than the model year."),
   ("Rough running with no stored fault",
    "Carbon buildup rarely sets a clean code early on. It shows up as a car that simply does not feel right."),
 ],
 "services": [
   ("Diagnostics on ODIS and VCDS",
    "Full module access, live data, adaptations and coding rather than generic fault codes. "
    "Carbon buildup on the FSI and TFSI engines, a 2.0T using oil, a mechatronic fault in an "
    "S tronic and a Haldex unit that has never been serviced all present vaguely, and the "
    "factory software is what separates them. Written report with photographs before any "
    "work is approved.", CEL),
   ("Oil service to the VW standard",
    "Audi lists an oil standard per engine: VW 502 00 for most older gasoline engines, 504 00 "
    "for the longlife schedule, 508 00 for the newest 2.0T and 3.0T that run 0W-20, 507 00 for "
    "the TDI. They are not interchangeable. OEM cartridge filter with new rings, the oil cooler "
    "and filter housing gaskets checked with the housing open, the PCV valve and level history "
    "checked on a 2.0T, a listen for the timing chain tensioner on the 2008 to 2013 engines, "
    "and the reminder reset through the car.", OIL),
   ("Brakes and the electronic parking brake",
    "Rotors measured against their minimum and replaced near it, with OEM or OEM-equivalent "
    "pads matched to the car. Since the 2009 A4 the parking brake motors live on the rear "
    "calipers and the rear pads cannot be changed without service mode on the factory "
    "software; forcing the pistons back breaks the actuators. The rear axle has no wear sensor, "
    "so all four corners are measured every visit. Brake fluid on Audi's two-year interval, "
    "with the ABS pump cycled where the car needs it.", BRAKES),
   ("Suspension: control arms, adaptive dampers, air",
    "The four upper links per side on the A4 and A6 are the most common wear point on the car "
    "and are replaced as a kit on the older ones. Dampers go on in axle pairs with new mounts; "
    "magnetic ride and Dynamic Chassis Control need the correct adaptive part and calibration. "
    "Air suspension on the allroad, A8 and Q7 loses a strut first and then the compressor; the "
    "RS4 and RS6 Dynamic Ride Control dampers leak with age. Every repair ends with an "
    "alignment to Audi's figures.", None),
 ],
 "known": [
   ("Carbon buildup on FSI and TFSI engines",
    "Direct injection means no fuel washes the intake valves. Deposits cause rough idle, misfires and lost power, and walnut blasting is the proper remedy."),
   ("Oil consumption on certain 2.0T engines",
    "Piston ring design and PCV system faults are the usual causes. Diagnosis determines which, and the difference in remedy is large."),
   ("Timing belt intervals on belt-driven engines",
    "Most belt-driven Audi engines are interference designs, so a failure is catastrophic rather than inconvenient. We replace the complete kit including the water pump."),
   ("quattro and Haldex driveline service",
    "The Haldex unit in transverse quattro systems needs periodic fluid and filter service that is frequently missed entirely, and it fails quietly."),
   ("Mechatronic faults in S tronic transmissions",
    "Hesitation, jerky low-speed shifts and clutch faults often trace to the mechatronic unit rather than the gearbox itself."),
 ],
 "reviews": ("kayode", "chelsea"),
 "faqs": [
  ("Does my Audi have a timing belt or a timing chain?",
   "It depends on the engine, not the model year alone. Several older 2.0T, 2.7T and 3.0 V6 engines use belts while many newer engines use chains. We confirm from the VIN rather than assuming, because the service is completely different."),
  ("Why does my Audi use so much oil?",
   "On certain 2.0T engines the common causes are piston ring design and a failing PCV system. Both are identifiable, and treating consumption as simply normal is how engines end up damaged."),
  ("Which oil standard does my Audi need?",
   "The one Audi lists for your engine code: VW 502 00 on most older gasoline engines, 504 00 on the longlife schedule, 508 00 on the newest engines built for 0W-20, and 507 00 on the TDI. They are not interchangeable, and a thin-oil engine given a thicker grade, or the reverse, is a common cause of complaints. We fill the listed standard and reset the reminder through the car."),
  ("Do the rear pads need anything special on an Audi with an electronic parking brake?",
   "Yes. The parking brake motors sit on the rear calipers, and the system has to be put into service mode with the factory software before the pads come out and cycled afterwards. Forcing the pistons back mechanically damages the actuators. It is part of every rear brake job here."),
  ("Can you service quattro all-wheel drive?",
   "Yes, including Haldex fluid and filter service on transverse quattro systems and differential service on longitudinal ones. It is routinely skipped maintenance."),
  ("Do you use the same software an Audi dealer uses?",
   "We run ODIS and VCDS, which give full module access, live data, adaptations and coding rather than generic fault codes."),
 ],
 "models": "A3, A4, A5, A6, A7, A8, Q3, Q5, Q7, Q8, TT, R8, and S and RS performance variants.",
 "band_head": ("NOT SURE WHAT'S WRONG?", "THAT'S THE POINT OF CALLING."),
 "cta_sub": "Describe what the car is doing. We'll tell you what we'd check first.",
 "closing": ("German Performance has worked only on German cars since 2010, more than 10,000 of them "
             "through this shop. The technicians are ASE-certified and Mercedes-Benz factory-trained, "
             "one an ASE Master Technician with the advanced engine diagnostics certification, and "
             "every Audi repair leaves with a written 12-month, 12,000-mile parts-and-labor warranty. "
             "Serving Snellville, Loganville, Grayson, Lawrenceville and all of Gwinnett County."),
}
