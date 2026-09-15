"""The Porsche hub: what the shop sees on a Porsche and every service it
performs on one, consolidated from the four Porsche job pages retired on
2026-09-15.

Every technical claim is a documented characteristic of the marque;
nothing about pricing, turnaround or certification is invented.
"""

from posts.common import BRAKES, INSPECTION, OIL

HUB = {
 "slug": "porsche-repair.html",
 "make": "porsche",
 "brand": "Porsche",
 "possessive": "Porsche",
 "eyebrow": "Porsche Specialists · Snellville, GA · Since 2010",
 "desc": ("Independent Porsche repair and inspection in Snellville, GA. PIWIS diagnostics, "
          "OEM parts, ASE-certified technicians, 12-month warranty. Gwinnett since 2010."),
 "sub": ("Porsche owners tend to arrive with a specific worry rather than a vague one, and usually "
         "a well-founded one. We are equipped to answer it properly, whether that is a "
         "pre-purchase inspection or a noise you would rather not ignore."),
 "tool": "PIWIS",
 "before": [
   ("A known weak point you have read about",
    "Porsche communities document failure modes thoroughly. That is useful, but it also means owners often arrive convinced of a diagnosis they have not had confirmed."),
   ("A car you are considering buying",
    "The gap between a well-kept example and a neglected one is enormous, and it is not visible from the outside."),
   ("A shop that will not commit",
    "Plenty of general shops will decline Porsche work outright, or take it on without the right tooling."),
 ],
 "services": [
   ("Pre-purchase and annual inspection",
    "A PIWIS scan of every module, engine to PDK to PASM, with every stored and pending code "
    "logged and explained; a full mechanical inspection; pad, rotor and PCCB wear measured; "
    "fluids and leaks checked; and on the 996 and 997 the IMS bearing and rear main seal "
    "assessed. You get a written report ranked by urgency, which is what a negotiation or a "
    "season of driving should start from.", INSPECTION),
   ("Oil service for a dry-sump engine",
    "Porsche publishes its own approvals, A40 across most of the gasoline range and the "
    "C-series on models built for particulate filters, and we fill the one listed for your "
    "model and year. The 911, Boxster and Cayman hold far more oil than a conventional engine "
    "and drain from more than one point; underfilling is what a routine drain-and-fill "
    "produces. The filter media and the magnetic plug are inspected for metal, the level is "
    "verified at temperature, and the reminder is reset through the factory interface.", OIL),
   ("Brakes, from iron rotors to PCCB",
    "Pads in OEM or OEM-equivalent compounds, including track compounds where the car sees "
    "one; rotors measured and inspected for heat cracking. Ceramic composite brakes take their "
    "own pads and their own wear scale, and a standard pad destroys the rotor. Brembo calipers "
    "are inspected and serviced on every job. Fluid on the two-year interval, sooner for track "
    "use, with pad and rotor measurements documented in writing.", BRAKES),
   ("Suspension: air, PASM and bushings",
    "A Cayenne or Panamera sitting low overnight is a leaking strut or a compressor worn out "
    "keeping up with one, and replacing the compressor while the leak remains wears out the "
    "new one. PASM faults revert the car to a fixed setting and it simply feels less composed. "
    "Control arm bushings on the 911 and Cayman are wear items. Alignment to Porsche's figures, "
    "corner balancing available, and an honest word on coil-over conversion for an "
    "out-of-warranty Cayenne.", None),
 ],
 "known": [
   ("IMS bearing on M96 and M97 engines",
    "Affects certain 986, 987, 996 and 997 model years. The risk varies by year and engine, and it is worth understanding where a specific car sits rather than assuming the worst or the best."),
   ("Rear main seal weeping",
    "Common on the same engine family. Often a slow seep rather than an emergency, but it needs assessing so it is not confused with something more serious."),
   ("Bore scoring on certain flat-six engines",
    "Presents as a distinctive cold-start noise and elevated oil consumption. Diagnosing it early materially changes the options available."),
   ("Coolant pipe failures on Cayenne V8 models",
    "Earlier Cayenne V8s used adhesive-bonded coolant pipes that can separate. A well-documented issue with a permanent fix."),
   ("PDK transmission service",
    "The dual-clutch unit needs fluid and filter service on schedule. It is expensive to neglect and straightforward to maintain."),
 ],
 "reviews": ("sahir", "kayode"),
 "faqs": [
  ("Do you perform Porsche pre-purchase inspections?",
   "Yes. Our inspection covers a full fault code scan, structural assessment, fluid condition and the known weak points for the specific model and year, with a written report you can use in negotiation."),
  ("Should I worry about the IMS bearing on my Porsche?",
   "It depends on the exact engine and model year, as the risk is not uniform across the M96 and M97 family. We will tell you where your specific car sits rather than generalising."),
  ("Why is a Porsche oil change more involved than a normal one?",
   "The 911, Boxster and Cayman use an integrated dry-sump system that holds far more oil than a conventional engine and drains from more than one point, and most modern Porsches read the level electronically, correctly only at operating temperature on level ground. We fill the approval listed for the model and year, verify the level that way, and inspect the filter and the magnetic plug for metal, which is the cheapest early warning the engine gives."),
  ("What are PCCB brakes and how are they different?",
   "Porsche Ceramic Composite Brakes are the optional carbon-ceramic rotors. They take their own pad compound and are measured on their own wear scale rather than by thickness alone; a standard pad on a ceramic rotor destroys it. We service them with the correct pads and record the wear indicator status in writing."),
  ("Do you have the correct Porsche diagnostic equipment?",
   "Yes. We use PIWIS, which is the factory system, giving full module access, adaptations and coding rather than generic fault code reading."),
  ("Do you service the Cayenne and Macan as well as the sports cars?",
   "Yes, the full current and recent Porsche range, including the Cayenne V8 coolant pipe issue that affects earlier models."),
 ],
 "models": "911, Boxster, Cayman, Panamera, Macan, Cayenne and Taycan.",
 "band_head": ("NOT SURE WHAT'S WRONG?", "THAT'S THE POINT OF CALLING."),
 "cta_sub": "Describe what the car is doing. We'll tell you what we'd check first.",
 "closing": ("German Performance has worked only on German cars since 2010, more than 10,000 of them "
             "through this shop. The technicians are ASE-certified and Mercedes-Benz factory-trained, "
             "one an ASE Master Technician with the advanced engine diagnostics certification, and "
             "every Porsche repair leaves with a written 12-month, 12,000-mile parts-and-labor "
             "warranty. Serving Snellville, Loganville, Grayson, Lawrenceville and all of Gwinnett County."),
}
