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
 "slug": "volkswagen-brake-service-snellville-ga.html",
 "brand": "Volkswagen",
 "h1": ("VOLKSWAGEN", "BRAKE", "SERVICE"),
 "title": "Volkswagen Brake Service Snellville GA | German Performance",
 "desc": ("Volkswagen brake service in Snellville, GA. Pads, rotors, electronic "
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
