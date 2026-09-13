"""Volkswagen service pages, built by tools/build_service_pages.py.

One dict per page (the GTI, Golf R, Jetta, Passat, Tiguan and Atlas). Every technical claim is a documented
characteristic of the marque; nothing about pricing, turnaround or
certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points,
faq_head, faqs, cta, cta_sub.
"""

PAGES = (
{
 "slug": "volkswagen-oil-change-snellville-ga.html",
 "brand": "Volkswagen",
 "h1": ("VOLKSWAGEN", "OIL", "CHANGE"),
 "title": "Volkswagen Oil Change Snellville GA | German Performance",
 "desc": ("Volkswagen oil change in Snellville, GA. VW 502/504/508-approved "
          "oil, low-ash 507 for TDI, OEM filter, seal and PCV check, reset. "
          "Call (678) 395-7459."),
 "sub": ("Volkswagen oil service in Snellville, GA — for the Golf, GTI, Golf "
         "R, Jetta, Passat, Tiguan, Atlas and TDI. The VW standard your engine "
         "is built for, an OEM filter, the seals these engines leak from "
         "checked, and the reminder reset through the car."),
 "cards_head": ("A PROPER VOLKSWAGEN", "OIL SERVICE"),
 "cards_sub": ("Volkswagen changed the oil its 2.0T runs on in 2018, its "
               "diesels need a low-ash grade to keep the particulate filter "
               "alive, and the DSG has its own service the oil change does not "
               "cover. Each is a way the job gets done wrong."),
 "cards": [
   ("The Right VW Standard",
    "Volkswagen approves oil by standard: 502 00 for the older 1.8T and 2.0T, "
    "504 00 for the longlife schedule on the third-generation 2.0T, 508 00 — "
    "a thin 0W-20 — for the 2018-on engines built for it, and 507 00 for the "
    "TDI. A 508 00 engine given thicker oil, or a TDI given a high-ash "
    "gasoline oil, is a real problem. Check the filler cap: the standard is "
    "printed on it, and it is what goes in."),
   ("TDI Low-Ash Oil",
    "The TDI's particulate filter clogs with the ash from ordinary oil. "
    "Volkswagen's 507 00 standard is low-ash for exactly that reason, and it "
    "is the only oil the diesels should see. We stock it and we use it."),
   ("Cartridge Filter and Housing Seals",
    "The filter is a cartridge in a housing on the block, and the housing's "
    "O-ring is a one-use part. We fit an OEM or OEM-equivalent element, a "
    "fresh O-ring and a new drain washer every time, and with the housing "
    "open we inspect the housing and oil cooler seals — the usual source of "
    "the smell after a drive on a 2.0T."),
   ("Consumption and the PCV Valve",
    "The 2.0T has a documented history of oil consumption, and a failed "
    "crankcase ventilation valve is the most common cause that is cheap to "
    "fix. We check the valve and the level history, and tell you whether the "
    "engine is using oil and why."),
   ("Timing Chain Awareness",
    "The 2008 to 2013 2.0T's timing chain tensioner is a known failure. A "
    "cold-start rattle is the warning; skipped oil changes are part of what "
    "causes it. We listen for it at every service."),
   ("Reminder Reset, DSG Noted",
    "The service reminder is reset through the car's own menu or "
    "Volkswagen-compatible diagnostics. If you have a DSG, its fluid and "
    "filter are a separate service at 40,000 miles — the oil change does not "
    "cover it, and we will tell you when it is due."),
 ],
 "why_head": ("VOLKSWAGEN OIL", "DONE RIGHT"),
 "why_lead": ("A Volkswagen oil change is a specific oil standard, a cartridge "
              "filter with seals that must be new, a level check done warm, "
              "and an honest look at the seals and the ventilation valve these "
              "engines wear out. The oil brand is the least of it."),
 "why_points": [
   "VW 502 00, 504 00, 508 00 or 507 00 oil matched to your engine code",
   "Low-ash 507 00 for every TDI, to protect the particulate filter",
   "OEM cartridge filters with new sealing rings and drain washer",
   "Oil level verified at operating temperature before handover",
   "Filter housing, oil cooler seal and PCV valve checked on every 2.0T",
   "Reminder reset through the car; DSG service flagged when it is due",
 ],
 "faq_head": ("VOLKSWAGEN OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a Volkswagen need an oil change?",
    "Volkswagen puts most models on a 10,000-mile or twelve-month schedule, "
    "whichever arrives first. That assumes the "
    "longlife-approved oil and steady driving. For the turbocharged 2.0T and "
    "the Golf R we recommend 5,000 to 7,500 miles, and on a car that mostly "
    "does short trips the annual limit matters more than the mileage."),
   ("Which VW oil standard does my engine need?",
    "The year and the engine decide it. The older 1.8T and 2.0T are approved "
    "for VW 502 00, the longlife schedule uses 504 00, the 2018-on 2.0T runs "
    "the thin 508 00 grade, and the TDI needs the low-ash 507 00. The "
    "standard is printed on the filler cap and in the manual; we confirm it "
    "against your engine code before filling."),
   ("My Volkswagen is using oil — should I worry?",
    "A little consumption on a turbocharged engine is normal. The 2.0T is "
    "known for using more than it should on some model years, and the "
    "crankcase ventilation valve is the first thing to check because it is a "
    "common, inexpensive cause. If yours needs a quart between changes, it is "
    "worth measuring properly."),
   ("Does an oil change include the DSG?",
    "No. The DSG dual-clutch transmission has its own fluid and filter, on a "
    "40,000-mile schedule, and it is a separate service. We will tell you "
    "when yours is due rather than letting it go unnoticed."),
   ("Will you reset the service light?",
    "Yes, through the car's own menu or Volkswagen-compatible diagnostics, so "
    "the service interval display is correct and the next reminder comes "
    "when it should."),
   ("Can an independent shop service a Volkswagen under warranty?",
    "Yes. The Magnuson-Moss Warranty Act means a manufacturer cannot require "
    "you to use the dealer for maintenance. What it can require is the "
    "correct specification oil and filter, and a record that the work was "
    "done. We use both, and you leave with the record."),
 ],
 "cta": ("VOLKSWAGEN OIL SERVICE", "DUE?"),
 "cta_sub": "Tell us the year and engine on the phone and the right standard will be on the shelf when you arrive.",
},
{
 "slug": "volkswagen-brake-service-snellville-ga.html",
 "brand": "Volkswagen",
 "h1": ("VOLKSWAGEN", "BRAKE", "REPAIR"),
 "title": "Volkswagen Brake Repair Snellville GA | German Performance",
 "desc": ("Volkswagen brake repair in Snellville, GA. Pads, rotors, electronic "
          "parking brake service mode, wear sensors and fluid flush. "
          "Call (678) 395-7459."),
 "sub": ("Volkswagen brake service in Snellville, GA — for the Golf, GTI, Golf R, "
         "Jetta, Passat, Tiguan, Atlas and Arteon. Including the electronic "
         "parking brake procedure that rear brakes on most modern VWs cannot be "
         "done without."),
 "cards_head": ("COMPLETE VOLKSWAGEN", "BRAKE SERVICE"),
 "cards_sub": ("Modern Volkswagen brakes are not a purely mechanical job any "
               "more. The rear calipers are driven by motors that have to be "
               "told what is happening."),
 "cards": [
   ("Front and Rear Pads and Rotors",
    "OEM or OEM-equivalent pads and rotors matched to your model. A GTI or "
    "Golf R runs different brake hardware and a different pad compound from a "
    "base Golf, and an Atlas carries far more weight than either."),
   ("Electronic Parking Brake Service Mode",
    "On most VWs from the Mk6 Golf onward, the rear caliper pistons are driven "
    "by electric motors that must be retracted through the factory interface "
    "before the pads come out. Forcing them back mechanically is how those "
    "motors get damaged."),
   ("Brake Wear Sensor Replacement",
    "The wear sensor is a consumable, not a reusable part. We fit a new one "
    "rather than splicing or bypassing the old, so the dashboard warning "
    "continues to mean something on the next set of pads."),
   ("Brake Fluid Flush",
    "Brake fluid absorbs moisture from the air whether the car is driven or "
    "not, which lowers its boiling point and corrodes the system from inside. "
    "Volkswagen calls for a change on a time interval, not a mileage one."),
   ("Caliper Service and Guide Pins",
    "Seized guide pins are a common cause of one pad wearing out well ahead of "
    "its partner. Cleaning and correctly lubricating them is part of the job, "
    "not an upsell."),
   ("Road Test and Bedding In",
    "New pads and rotors need a proper bedding-in cycle to transfer material "
    "evenly. Skipping it is a common cause of the judder that gets blamed on "
    "warped rotors a few thousand miles later."),
 ],
 "why_head": ("VOLKSWAGEN BRAKE", "SPECIALISTS"),
 "why_lead": ("The reason a general shop turns away rear brakes on a modern "
              "Volkswagen — or damages them — is the electronic parking brake. "
              "The caliper pistons are motor-driven and have to be put into "
              "service mode with the right software before anything is touched."),
 "why_points": [
   "Electronic parking brake retracted and reset through factory-level software",
   "Correct pad compound for Golf, GTI, Golf R, Jetta, Passat, Tiguan and Atlas",
   "New wear sensors fitted, never bypassed",
   "Brake fluid changed on Volkswagen's time-based interval",
   "Guide pins cleaned and lubricated as part of every pad replacement",
   "Bedding-in cycle completed on a road test before the car is handed back",
 ],
 "faq_head": ("VOLKSWAGEN BRAKE", "FAQ"),
 "faqs": [
   ("Why do the rear brakes on my VW need a scan tool?",
    "Because the rear caliper pistons are driven by small electric motors "
    "rather than hydraulics alone. They have to be wound back into service mode "
    "through the car's software before the old pads come out, and released "
    "again afterwards. Forcing them back by hand is what damages the actuators, "
    "and that repair costs considerably more than the brake job."),
   ("How often should Volkswagen brake fluid be changed?",
    "Volkswagen specifies brake fluid on a time interval rather than a mileage "
    "one, because the fluid absorbs moisture from the air whether or not the "
    "car is being driven. Two years is the usual figure. A car that sits is "
    "not exempt — if anything it is the more likely candidate."),
   ("My steering wheel shakes when I brake. Are the rotors warped?",
    "Usually not, despite the name everyone uses. What normally causes it is "
    "uneven pad material deposited on the rotor face, often from a set that was "
    "never properly bedded in or from sitting with hot brakes. It feels "
    "identical to warping. We measure the rotor before deciding, because the "
    "two problems have different fixes."),
   ("Do you use OEM or aftermarket brake parts?",
    "We use OEM or OEM-equivalent parts as standard. On brakes the compound "
    "matters more than the badge — the wrong pad on a Golf R will fade under "
    "heat that the correct one shrugs off. If you have a preference or you use "
    "the car on track, tell us and we will talk it through."),
   ("Does a GTI or Golf R need different brakes from a regular Golf?",
    "Yes. Both run larger brake hardware and a pad compound built for more heat "
    "than the base car ever sees. Fitting standard Golf pads to a Golf R is a "
    "cost saving that shows up the first time you use the performance you paid "
    "for."),
   ("Can you do brakes on a Tiguan or Atlas?",
    "Yes. Both are heavier than the cars most people picture when they think of "
    "a Volkswagen, and both go through brakes accordingly. They also use the "
    "electronic parking brake, so the same service-mode procedure applies."),
 ],
 "cta": ("VOLKSWAGEN BRAKES", "GRINDING OR SOFT?"),
 "cta_sub": "Call and tell us what you are hearing or feeling — we will tell you what it usually means.",
},
)
