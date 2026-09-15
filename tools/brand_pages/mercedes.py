"""The Mercedes hub: what the shop sees on a Mercedes-Benz and every service
it performs on one, consolidated from the seven Mercedes job pages retired
on 2026-09-15. Six cards, two rows of three; cooling and air conditioning
share one.

Every technical claim is a documented characteristic of the marque;
nothing about pricing, turnaround or certification is invented. The hero
checklist says "Mercedes", the form apply_redesign.py keeps (the long form
wrapped on phones). The credential sentence in "closing" is the owner's.
"""

from posts.common import AC, BRAKES, CEL, OIL, TRANSMISSION

HUB = {
 "slug": "mercedes-repair-snellville-ga.html",
 "make": "mercedes",
 "brand": "Mercedes-Benz",
 "possessive": "Mercedes",
 "eyebrow": "Mercedes-Benz Specialists · Snellville, GA · Since 2010",
 "desc": ("Independent Mercedes repair in Snellville, GA. XENTRY factory diagnostics, OEM parts, "
          "factory-trained technicians, 12-month warranty. Gwinnett since 2010."),
 "sub": ("A Mercedes rarely fails loudly. It sags a little at one corner, or shifts less smoothly "
         "than it did, or shows a message with no obvious cause. We find out which system is "
         "actually responsible before anything gets replaced."),
 "tool": "XENTRY",
 "before": [
   ("Symptoms that creep rather than break",
    "Air suspension settling overnight, a gearbox that hesitates when cold, a slow oil weep. Easy to live with, expensive to ignore."),
   ("Quotes for whole assemblies",
    "A great deal of Mercedes work gets quoted as complete units when the failure is one component inside it. Conductor plates and valve bodies are the common example."),
   ("No clear picture of urgency",
    "You should know which of the findings needs attention now and which can reasonably wait until next time."),
 ],
 "services": [
   ("Diagnostics on XENTRY",
    "The factory software reads every module, not the one a parts-store scanner sees: engine, "
    "transmission, ABS, ESP, SRS, AIRMATIC and the rest. Fault codes say what failed; live data "
    "and component tests say why. A check engine light or limp mode leaves here with a confirmed "
    "cause and a written report with photographs, not a cleared code and a theory. Our technicians "
    "are Mercedes-Benz factory-trained.", CEL),
   ("Service A, Service B and the oil approvals",
    "ASSYST Plus alternates the two services, and each has its own sheet of work. The oil is the "
    "one Mercedes lists for your engine: 229.5 for most gasoline engines, the low-ash 229.51 or "
    "229.52 for BlueTEC diesels and engines with particulate filters, 229.71 for the newest "
    "low-viscosity applications. Cartridge filter with new rings, level confirmed warm through "
    "the cluster, the M272 and M273 oil cooler seals and the M276 and M278 turbo feed lines "
    "looked at while the car is up, and the reminder reset to the next correct service.", OIL),
   ("Brakes, SBC and the parking brake",
    "Mercedes rotors are light and wear with the pads; we measure them against the minimum "
    "stamped on the hat and replace rather than machine thin. Wear sensors go on both axles with "
    "the pads. The mid-2000s E-Class, CLS and SL carry Sensotronic Brake Control, which has to be "
    "put to sleep on XENTRY before a caliper is touched; current cars need the electric parking "
    "brake in service mode for the rear pads. DOT 4 Plus fluid on its two-year interval, bled "
    "through the stability control unit where the car requires it.", BRAKES),
   ("AIRMATIC, ABC and conventional suspension",
    "A corner that sits low overnight is a leaking strut, a tired compressor or a valve block, "
    "and XENTRY's fill and actuation tests tell them apart before an expensive part is guessed "
    "at. Active Body Control on the S-Class, CL and SL is hydraulic and fails through leaks and "
    "pressure loss. Control arms are replaced individually where worn, dampers in axle pairs "
    "with new mounts, and the ride height is set before the alignment because the geometry "
    "depends on it.", None),
   ("Transmission service: 722.6, 7G- and 9G-Tronic",
    "Fluid and filter to the Mercedes specification, with the level set at the fluid temperature "
    "the transmission's own sensor reports, which is the step a generic fluid change skips. Harsh "
    "shifts, limp mode and phantom speed-sensor faults are tested at the conductor plate, the "
    "13-pin connector and the valve body before the unit is condemned; on the 722.6 and later "
    "they are usually repairable without replacing the transmission. Adaptations reset and "
    "relearned on the road afterwards.", TRANSMISSION),
   ("Cooling system and air conditioning",
    "The cooling system is pressure-tested cold first, because coolant that disappears with "
    "nothing on the driveway is how these faults present: the plastic, map-controlled thermostat "
    "housing that fails electrically while looking perfect, a water pump whose impeller has "
    "stopped moving coolant, the auxiliary electric pump on the heater circuit, an expansion "
    "tank cracked at the seam. Filled to the Mercedes coolant approval, never topped up with a "
    "universal product. Air conditioning gets a full HVAC diagnostic on XENTRY, leaks found with "
    "dye and repaired before any recharge, and the correct refrigerant: R134a on the older cars, "
    "R1234yf on most from 2017.", AC),
 ],
 "known": [
   ("AIRMATIC and air suspension",
    "Leaking air struts, a failing compressor or a faulty valve block all produce the same sagging corner. Testing tells them apart, and the difference in cost is substantial."),
   ("Conductor plate and valve body faults",
    "On 722.6 and later transmissions these cause harsh shifts, limp mode and phantom speed sensor faults. Frequently repairable without replacing the transmission."),
   ("Balance shaft wear on some M272 engines",
    "Certain model years suffer premature sprocket wear, which sets timing correlation codes. Diagnosis matters because the remedy is significant work and should never be guessed at."),
   ("Oil leaks and cooling",
    "Valve cover gaskets, oil cooler seals and the thermostat housing are the usual sources. We locate the actual leak rather than replacing gaskets speculatively."),
   ("Electronic wear sensors on the brakes",
    "The sensor is consumed along with the pad. Fitting pads without new sensors leaves the warning on the dash and the reset undone."),
 ],
 "reviews": ("anan", "chelsea"),
 "faqs": [
  ("Will servicing my Mercedes outside the dealer affect my warranty?",
   "No. Federal law protects your right to use an independent shop for maintenance and repairs without voiding the factory warranty, as long as the work is performed correctly with appropriate parts. We keep thorough records for exactly this reason."),
  ("What is the difference between Service A and Service B?",
   "ASSYST Plus alternates them, roughly every 10,000 miles or once a year. Service A is the oil and filter, fluid levels, tire pressures and a set of checks. Service B adds the cabin filter, the brake fluid on its two-year interval, and a longer inspection list. We do the sheet the car is due for, with the oil on the Mercedes approval for your engine, and reset the reminder to the next correct service."),
  ("Why does checking Mercedes transmission fluid need a scan tool?",
   "Because the level is only meaningful at a specific fluid temperature. Checking it cold or hot gives a misleading reading, which is how transmissions end up incorrectly filled."),
  ("Can the conductor plate be repaired without replacing the transmission?",
   "Usually, yes. On the 722.6 and later units the conductor plate, the valve body and the 13-pin connector cause most of the harsh shifting, limp mode and speed-sensor faults we see, and each is replaceable on its own. We test them before a transmission is condemned, and a whole-unit quote for one of these faults deserves a second opinion."),
  ("My Mercedes sits lower on one side overnight. What is that?",
   "Usually an air suspension leak, most often a strut, though the compressor or valve block can produce the same symptom. It is worth diagnosing early, because a failing compressor that runs constantly tends to destroy itself."),
  ("Do you service AMG models?",
   "Yes. AMG variants use different components and torque specifications than the standard range, and we set them up to the correct specification."),
 ],
 "models": "A, C, E and S-Class, CLA, CLS, GLA, GLB, GLC, GLE, GLS, G-Class, SL, SLK, Sprinter, and AMG variants.",
 "band_head": ("NOT SURE WHAT'S WRONG?", "THAT'S THE POINT OF CALLING."),
 "cta_sub": "Describe what the car is doing. We'll tell you what we'd check first.",
 "closing": ("German Performance has worked only on German cars since 2010, more than 10,000 of them "
             "through this shop. The technicians are ASE-certified and Mercedes-Benz factory-trained, "
             "one an ASE Master Technician with the advanced engine diagnostics certification, and "
             "every Mercedes repair leaves with a written 12-month, 12,000-mile parts-and-labor "
             "warranty. Serving Snellville, Loganville, Grayson, Lawrenceville and all of Gwinnett County."),
}
