"""Porsche service pages, built by tools/build_service_pages.py.

One dict per page (the 911, Boxster, Cayman, Macan, Cayenne and Panamera). Every technical claim is a documented
characteristic of the marque; nothing about pricing, turnaround or
certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points,
faq_head, faqs, cta, cta_sub.
"""

PAGES = (
{
 "slug": "porsche-oil-change-snellville-ga.html",
 "brand": "Porsche",
 "h1": ("PORSCHE", "OIL", "CHANGE"),
 "title": "Porsche Oil Change Snellville GA | German Performance",
 "desc": ("Porsche oil change in Snellville, GA. A40 and C-spec approved oil, "
          "correct dry-sump fill, cartridge filter and PIWIS service reset. "
          "Call (678) 395-7459."),
 "sub": ("Porsche oil service in Snellville, GA — for the 911, Boxster, Cayman, "
         "Macan, Cayenne and Panamera. Approved oil for your exact model and "
         "year, the correct fill for a dry-sump engine, and a service reset "
         "done properly."),
 "cards_head": ("A PROPER PORSCHE", "OIL SERVICE"),
 "cards_sub": ("A Porsche oil change is not a quicker version of an ordinary "
               "one. The approvals are specific, the capacities are large, and "
               "on most modern models there is no dipstick to check your work."),
 "cards": [
   ("Porsche-Approved Oil",
    "Porsche publishes its own oil approvals — A40 across most of the gasoline "
    "range, and the newer C-series specifications on models built for "
    "particulate filters. We fill the approval and viscosity listed for your "
    "exact model and year, not a generic full synthetic that happens to be on "
    "the shelf."),
   ("Correct Dry-Sump Fill",
    "The 911, Boxster and Cayman use an integrated dry-sump system that holds "
    "far more oil than a conventional engine and drains from more than one "
    "point. Underfilling is the common outcome when the job is treated as a "
    "routine drain-and-fill."),
   ("Level Verified at Temperature",
    "Most modern Porsches have no dipstick — the level is read electronically, "
    "and only reads correctly with the engine at operating temperature on level "
    "ground. We verify it that way before the car leaves, which is the step "
    "most often skipped."),
   ("Cartridge Filter Replacement",
    "An OEM or OEM-equivalent cartridge filter with new sealing rings. We also "
    "inspect the old filter media and the magnetic drain plug for metal, which "
    "is the cheapest early warning any engine gives you."),
   ("Bore Score and IMS Awareness",
    "On the 996 and early 997, what comes out with the oil matters. Fine metal "
    "in the filter or on the plug is worth knowing about long before it becomes "
    "a noise, and we will tell you what we saw either way."),
   ("Service Reset and Inspection",
    "The maintenance reminder is reset through the factory interface rather "
    "than cleared by a generic tool, and the car gets a multi-point inspection "
    "while it is up — leaks, boots, belts, tyres and brake wear."),
 ],
 "why_head": ("PORSCHE OIL", "DONE RIGHT"),
 "why_lead": ("The reason a Porsche oil service costs more than a generic one is "
              "not the oil. It is the capacity, the approval, the dry-sump "
              "drain procedure and the fact that you cannot confirm the result "
              "with a dipstick. Get any of those wrong and the car leaves "
              "underfilled."),
 "why_points": [
   "Porsche A40 and C-series approved oils, matched to model and year",
   "Dry-sump drain and fill procedure on 911, Boxster and Cayman",
   "Electronic oil level verified at operating temperature before handover",
   "OEM or OEM-equivalent cartridge filters with new seals",
   "Filter media and magnetic plug inspected for metal, and reported to you",
   "Maintenance reminder reset through PIWIS-compatible diagnostics",
 ],
 "faq_head": ("PORSCHE OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does a Porsche need an oil change?",
    "Porsche's published interval for most modern models is 10,000 miles or "
    "once a year, whichever comes first. Short trips, track days and long "
    "periods parked are all harder on oil than steady mileage, so cars used "
    "that way are better served on a shorter interval. If your car is driven "
    "rarely, the annual limit matters more than the mileage."),
   ("What oil does my Porsche take?",
    "It depends on the model and year. Most of the gasoline range calls for an "
    "oil carrying Porsche's A40 approval, while newer models built with "
    "particulate filters use the C-series specifications. The approval matters "
    "more than the brand — an oil without it may meet a general industry "
    "standard and still be wrong for the engine."),
   ("Why is a Porsche oil change more involved than a normal one?",
    "Three reasons. The 911, Boxster and Cayman use an integrated dry-sump "
    "system that holds significantly more oil and drains from more than one "
    "point. The approvals are Porsche-specific. And most modern models have no "
    "dipstick, so the level can only be confirmed electronically with the "
    "engine warm and the car level."),
   ("Can you reset the service reminder?",
    "Yes. We reset it through the factory-level interface so the car's own "
    "maintenance schedule stays accurate, rather than clearing the message "
    "with a generic tool and leaving the underlying counter wrong."),
   ("Will you tell me if you find metal in the oil?",
    "Yes, and we look for it. We inspect the magnetic drain plug and the old "
    "filter media every time. On a 996 or an early 997 that inspection is one "
    "of the few routine chances to notice bearing wear early. If we find "
    "something we will show you and explain what it does and does not mean."),
   ("Will an independent oil change affect my Porsche warranty?",
    "No. Federal law protects your right to have routine maintenance performed "
    "by an independent shop without voiding a manufacturer warranty, as long as "
    "the correct specification parts and fluids are used and the work is "
    "documented. You leave with a written record of what was done."),
 ],
 "cta": ("PORSCHE OIL SERVICE", "DUE?"),
 "cta_sub": "Call and tell us the model and year — we will confirm the approval your engine needs.",
},
{
 "slug": "porsche-suspension-repair-snellville-ga.html",
 "brand": "Porsche",
 "h1": ("PORSCHE", "SUSPENSION", "REPAIR"),
 "title": "Porsche Suspension Repair Snellville GA | German Performance",
 "desc": ("Porsche suspension repair in Snellville, GA. Cayenne and Panamera air "
          "suspension, PASM dampers, control arms and alignment to factory spec. "
          "Call (678) 395-7459."),
 "sub": ("Porsche suspension work in Snellville, GA — air suspension on the "
         "Cayenne and Panamera, PASM dampers, control arms and bushings, and "
         "alignment to Porsche's own specification rather than a generic "
         "setting."),
 "cards_head": ("PORSCHE SUSPENSION", "WORK WE DO"),
 "cards_sub": ("Air suspension and adaptive dampers fail in ways a visual "
               "inspection will not find. Most of this work starts with a "
               "diagnosis, not a part."),
 "cards": [
   ("Air Suspension Diagnosis",
    "A Cayenne or Panamera sitting low overnight, or throwing a chassis "
    "warning, is usually a leaking strut or a compressor worn out trying to "
    "keep up with one. We find which, because replacing the compressor while "
    "the leak remains simply wears out the new one."),
   ("Air Strut and Compressor Replacement",
    "Struts and compressors replaced as a system where the evidence supports "
    "it, with the ride height sensors recalibrated afterwards so the car sits "
    "and levels the way it should."),
   ("PASM Damper Testing",
    "Porsche Active Suspension Management adjusts damping electronically. When "
    "a damper or its control fails, the system stores a fault and reverts to a "
    "fixed setting — often the first sign is that the car simply feels less "
    "composed than it used to."),
   ("Control Arms, Bushings and Ball Joints",
    "Worn bushings show up as vague steering, a clunk over expansion joints, or "
    "an alignment that will not hold. On the 911 and Cayman these are wear "
    "items, not failures, and they are worth addressing before they take the "
    "tyres with them."),
   ("Coil-Over Conversion",
    "For an out-of-warranty Cayenne, replacing a failed air system with a "
    "quality coil-over setup is a legitimate option and often the more sensible "
    "one. We will lay out both paths honestly, including what you give up."),
   ("Alignment to Porsche Specification",
    "Alignment done to the factory figures for your model, with corner "
    "balancing available for cars that see track use. Suspension work is not "
    "finished until the geometry is set."),
 ],
 "why_head": ("POR SCHE CHASSIS", "SPECIALISTS"),
 "why_lead": ("The expensive mistake with Porsche suspension is replacing the "
              "part that is complaining rather than the one that failed. A "
              "compressor that burns out is usually the symptom of a strut that "
              "has been leaking for months. We find the cause first and tell "
              "you what we found."),
 "why_points": [
   "Air suspension diagnosis on Cayenne and Panamera before any part is ordered",
   "Ride height sensor calibration after strut or compressor replacement",
   "PASM fault codes read with factory-level diagnostics, not a generic scanner",
   "Control arm and bushing replacement on 911, Boxster, Cayman and Macan",
   "Coil-over conversion offered as an honest alternative on older Cayennes",
   "Alignment to Porsche specification, with corner balancing for track cars",
 ],
 "faq_head": ("PORSCHE SUSPENSION", "FAQ"),
 "faqs": [
   ("Why is my Cayenne sitting low in the morning?",
    "That is the classic sign of a leaking air strut. The system holds the car "
    "up while it is running, but overnight the air escapes and the corner "
    "settles. The compressor then works harder every morning to bring it back, "
    "which is why a neglected leak eventually takes the compressor with it."),
   ("Should I replace air suspension with coil-overs?",
    "It is a reasonable option on an out-of-warranty Cayenne, and plenty of "
    "owners are happier for it. You lose the ride height adjustment and the "
    "adaptive damping, and you gain a system that is far cheaper to keep "
    "working. We will tell you what your car needs either way and let you "
    "decide."),
   ("What is PASM and how do I know if it has failed?",
    "PASM is Porsche's electronically adjustable damping. When a damper or its "
    "wiring fails, the car stores a fault and falls back to a fixed damper "
    "setting. Owners usually describe it as the car feeling flatter, busier or "
    "just less settled than they remember, sometimes with a chassis warning."),
   ("Do you need factory software for suspension work?",
    "For anything involving air suspension or PASM, yes. Ride height sensors "
    "have to be recalibrated after a strut is replaced, and adaptive damper "
    "faults are only readable through the chassis modules. A generic code "
    "reader will not see them."),
   ("How long do Porsche control arm bushings last?",
    "There is no single figure — heat, road surface and how the car is driven "
    "all matter more than mileage. What we look for is play in the joint and "
    "cracking in the rubber. Vague steering, a clunk over bumps, or an "
    "alignment that drifts back out are the usual reasons someone calls."),
   ("Can you align a car that is used on track?",
    "Yes, and we will ask how you use it first. A track alignment and a road "
    "alignment are different compromises, and setting one when you wanted the "
    "other wastes tyres. Corner balancing is available for cars where it is "
    "worth doing."),
 ],
 "cta": ("SOMETHING OFF IN", "THE WAY IT SITS?"),
 "cta_sub": "Call and describe what the car is doing — we will tell you what we would check first.",
},
)
