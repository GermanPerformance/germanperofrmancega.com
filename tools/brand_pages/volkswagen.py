"""The Volkswagen hub: what the shop sees on a VW and every service it
performs on one, consolidated from the three VW job pages retired on
2026-09-15.

Every technical claim is a documented characteristic of the marque;
nothing about pricing, turnaround or certification is invented. The hero
checklist says "VW", the marque's own short form.
"""

from posts.common import BRAKES, OIL, TRANSMISSION

HUB = {
 "slug": "volkswagen-repair-snellville-ga.html",
 "make": "volkswagen",
 "brand": "Volkswagen",
 "possessive": "VW",
 "eyebrow": "Volkswagen Specialists · Snellville, GA · Since 2010",
 "desc": ("Independent Volkswagen repair in Snellville, GA. ODIS and VCDS diagnostics, OEM "
          "parts, ASE-certified technicians, 12-month warranty. Gwinnett since 2010."),
 "sub": ("Volkswagen engines share their design with Audi, and so do their failure patterns. The "
         "advantage of a shop that works on both every week is that we have usually seen your "
         "specific problem before."),
 "tool": "ODIS and VCDS",
 "before": [
   ("A rattle on cold start",
    "On the EA888 family this is worth taking seriously rather than waiting to see whether it gets worse."),
   ("Being quoted a replacement engine",
    "Most of what gets called engine failure is one component. It is worth a second opinion before accepting that number."),
   ("A coolant smell with no visible leak",
    "The usual sources hide behind covers and only show themselves under pressure."),
 ],
 "services": [
   ("Engine repair on the EA888, TDI and VR6",
    "Diagnosed on VCDS and the factory software before a part is touched. The EA888 timing chain "
    "goes back in as a complete kit, chain, tensioner, guides and phasers, so you are not back for "
    "the piece that was skipped. Walnut blasting clears the carbon that direct injection leaves on "
    "the intake valves. Oil leaks are traced with dye to the cam cover, oil cooler, pan or rear "
    "main seal. A failed turbo is replaced with its cause, oil starvation, a boost leak or a "
    "failed PCV, fixed at the same time.", None),
   ("Oil service to the VW standard",
    "The standard is printed on the filler cap and it is what goes in: 502 00 for the older 1.8T "
    "and 2.0T, 504 00 for the longlife schedule, 508 00 for the 2018-on engines built for 0W-20, "
    "and the low-ash 507 00 the TDI's particulate filter depends on. OEM cartridge filter, a fresh "
    "housing O-ring and drain washer, the housing and oil cooler seals inspected, the PCV valve "
    "checked on a 2.0T that is using oil, and a listen for the tensioner on the 2008 to 2013 "
    "engines.", OIL),
   ("Brakes and the electronic parking brake",
    "OEM or OEM-equivalent pads and rotors matched to the model, because a GTI or Golf R runs "
    "different hardware from a base Golf and an Atlas carries far more weight than either. From "
    "the Mk6 Golf onward the rear pistons are retracted through the factory interface, never "
    "forced. Wear sensors replaced, not spliced; guide pins cleaned and lubricated; fluid on "
    "Volkswagen's time interval; and a proper bedding-in road test, which is what prevents the "
    "judder that gets blamed on warped rotors.", BRAKES),
   ("DSG and drivetrain service",
    "The dual-clutch gearbox has a scheduled fluid and filter service at 40,000 miles that an "
    "oil change does not cover, and skipping it is the usual cause of hesitation and rough "
    "low-speed shifting. We service it to the Volkswagen procedure, reset the adaptations, and "
    "tell you when the next one is due. 4Motion Haldex units get the same treatment.", TRANSMISSION),
 ],
 "known": [
   ("Timing chain tensioner on earlier EA888 engines",
    "The original tensioner design can allow chain slack on cold start. The rattle is the warning, and the failure is severe, so it should not be left."),
   ("Carbon buildup on direct-injection engines",
    "Deposits on the intake valves cause rough idle, misfires and lost power. Walnut blasting removes them properly."),
   ("Water pump and thermostat housing leaks",
    "The composite housings become brittle with heat cycling. A very common source of slow coolant loss."),
   ("DSG transmission service",
    "The dual-clutch gearbox needs fluid and filter service on schedule. Skipping it is a frequent cause of shift quality complaints."),
   ("Oil leaks from the valve cover and filter housing",
    "Hardened gaskets are the usual culprit. We confirm the actual source rather than replacing gaskets speculatively."),
 ],
 "reviews": ("chelsea", "sahir"),
 "faqs": [
  ("What is the rattle on cold start on my VW?",
   "On earlier EA888 engines it is commonly the timing chain tensioner allowing slack before oil pressure builds. It is worth diagnosing quickly, because the consequence of a failure is serious."),
  ("Which VW oil standard does my engine need?",
   "The one printed on the filler cap: 502 00 for the older 1.8T and 2.0T, 504 00 for the longlife schedule, 508 00 for the 2018-on engines built for 0W-20, and the low-ash 507 00 for every TDI, because ordinary oil's ash clogs the particulate filter. A thin-oil engine given a thicker grade, or a TDI given a gasoline oil, is a real problem, so we fill the standard the engine was built for."),
  ("Do you work on both TSI and TDI engines?",
   "Yes. Diesel work brings in injectors, glow plugs and emissions components that gasoline engines do not have, and we have the VW-specific tooling for both."),
  ("Why do the rear brakes on my VW need a scan tool?",
   "From the Mk6 Golf onward the rear caliper pistons are driven by the parking brake motors, and they have to be retracted through the factory interface before the pads come out and cycled afterwards. Forcing them back mechanically is how those motors get damaged. It is part of every rear brake job here, not an extra."),
  ("Does my DSG transmission need servicing?",
   "Yes. The dual-clutch unit has a scheduled fluid and filter service, and neglecting it is a common cause of hesitation and rough low-speed shifting."),
  ("Can you repair my VW engine rather than replace it?",
   "Usually. Most of what is described as engine failure turns out to be a specific component such as a tensioner, gasket, turbo or PCV valve. We diagnose before quoting."),
 ],
 "models": "Golf, GTI, Jetta, Passat, Tiguan, Atlas, Arteon, Beetle, and TDI diesel models.",
 "band_head": ("NOT SURE WHAT'S WRONG?", "THAT'S THE POINT OF CALLING."),
 "cta_sub": "Describe what the car is doing. We'll tell you what we'd check first.",
 "closing": ("German Performance has worked only on German cars since 2010, more than 10,000 of them "
             "through this shop. The technicians are ASE-certified and Mercedes-Benz factory-trained, "
             "one an ASE Master Technician with the advanced engine diagnostics certification, and "
             "every Volkswagen repair leaves with a written 12-month, 12,000-mile parts-and-labor "
             "warranty. Serving Snellville, Loganville, Grayson, Lawrenceville and all of Gwinnett County."),
}
