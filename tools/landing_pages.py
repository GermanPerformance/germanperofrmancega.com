#!/usr/bin/env python3
"""The service landing pages, one entry each, built by tools/build_landing_pages.py.

Every entry names its service once. The H1 ("{service} in Snellville, GA"),
the title, the breadcrumb, the Service schema, the section headings and the
red band's ask all derive from that field, so the wording cannot drift
between them. "gbp" lists the Google Business Profile services the page
answers for; tools/check_gbp_alignment.py holds the site to it.

The hero rules the owner set on 2026-09-12:
  * The H1 is two lines: "{service} in" over "Snellville, GA". Keep the
    service to SERVICE_MAX_CHARS or fewer; the generator sizes the line to
    fit, and a longer name would have to shrink below the display scale.
  * The sub expounds the H1: it restates the service and the place, then says
    for whom, what is included, and the promise --
    "{Service} in Snellville, GA for {makes}: {included}, {how we do it}."
  * One call to action, "Service My Car", in the hero and after every section.

Fields:
  slug        the file at the repo root
  service     the service, in title case, as the H1 reads it (<= 19 chars)
  gbp         profile services this page answers for (see the .md export)
  desc        meta description, 120-160 characters, naming the service and Snellville
  eyebrow     optional; the line above the H1 (default: the makes)
  sub         the hero paragraph (see the rule above)
  photo       {"base": path without size/extension, "alt": ..., "width", "height"}
  intro       the paragraph beside the photo, opening "What's included"
  promise     three checklist lines beside the photo
  cards_head  optional two-line H2 over the cards (default: WHAT'S INCLUDED IN / {SERVICE})
  cards       six (title, body) pairs
  reviews     two keys from tools/reviews.py
  steps       optional override of DEFAULT_STEPS, four (title, body) pairs
  faqs        (question, answer) pairs, at least four
  cta_sub     optional override of the line under the band's ask

Treat PAGES as read-only data: build a new tuple rather than editing one in place.
"""

SERVICE_MAX_CHARS = 19
MAKES = "BMW, Mercedes-Benz, Audi, Porsche and Volkswagen"

# What happens after the call, in the shop's own words (index.html #process,
# about.html). Four steps: the service pages need the promise, not the tour.
DEFAULT_STEPS = (
    ("Call",
     "Tell us the year, the model and what the car is doing. We say what we "
     "would check first and what finding out should cost."),
    ("Diagnose",
     "A technician runs the factory software your car speaks — ISTA, XENTRY, "
     "ODIS or PIWIS — and a physical inspection, then sends a written report "
     "with photos."),
    ("Approve",
     "Nothing starts until you approve the written estimate, and nothing is "
     "added to the bill without a call."),
    ("Repair",
     "The work is done with OEM-grade parts and genuine fluids, road-tested, "
     "and handed back with a service record and a 12-month, 12,000-mile "
     "warranty."),
)
AREA_LINE = ("Serving Snellville, Loganville, Grayson, Lawrenceville and all of "
             "Gwinnett County.")
DEFAULT_CTA_SUB = ("Call and tell us the make, model and year. Same-week slots "
                   "usually available.")

PAGES = (
{
 "slug": "german-car-brake-repair-snellville-ga.html",
 "service": "Brake Repair",
 "gbp": ("Brake shop", "Brakes", "Auto brake repair", "Auto brake replacement",
         "Brake service & repair"),
 "desc": ("Brake repair in Snellville, GA for BMW, Mercedes, Audi, Porsche and "
          "VW. Pads, rotors, sensors and fluid to factory spec, 12-month "
          "warranty. Call (678) 395-7459."),
 "sub": (f"Brake repair in Snellville, GA for {MAKES}: pads, rotors, wear "
         "sensors and fluid fitted to factory specification, measured before "
         "we recommend anything and bedded in before you drive away."),
 "photo": {
   "base": "assets/img/services/brake-repair",
   "alt": ("Brake repair at German Performance in Snellville: a technician "
           "torques a drilled rotor and blue caliper on a lifted BMW"),
   "width": 1100, "height": 1375,
 },
 "intro": ("German brakes are built to fade late and stop hard, and they are "
           "designed to be replaced as a system rather than a pad at a time. "
           "Doing it the way the manufacturer intended is what keeps that "
           "pedal feel."),
 "promise": (
   "Rotors measured against the published minimum thickness, never judged by eye",
   "OEM or OEM-equivalent pads and rotors in the compound the car was designed around",
   "Every brake job carries a 12-month, 12,000-mile warranty",
 ),
 "cards": (
   ("Pads and Rotors",
    "German rotors are designed to wear with the pads and carry a published "
    "minimum thickness. We measure every rotor and replace pads and rotors "
    "together when the specification calls for it, with OEM or OEM-equivalent "
    "parts in the compound the car was designed around."),
   ("Brake Fluid Service",
    "Brake fluid absorbs water from the air, and every German manufacturer "
    "publishes a fixed replacement interval, usually two years, regardless of "
    "mileage. We flush the system with fluid to the DOT specification the car "
    "requires, including the ABS unit where the factory procedure calls for "
    "it."),
   ("Wear Sensors and Warnings",
    "Most German cars carry electronic wear sensors that trigger the brake "
    "warning on the dash. A sensor that has warned is a one-time part and is "
    "replaced with the pads, and the service reminder is reset through the "
    "factory interface rather than cleared with a generic tool."),
   ("Calipers and Hoses",
    "Sticking caliper pistons and slide pins wear one pad faster than the "
    "other and overheat the rotor. We check every caliper for free movement, "
    "rebuild or replace what has seized, and replace rubber hoses that have "
    "started to swell or crack."),
   ("Electronic Parking Brake",
    "Many current German models use an electronic parking brake that must be "
    "put into service mode with the factory software before the rear pads can "
    "be changed. Forcing it is how the actuators get destroyed."),
   ("ABS and Stability Faults",
    "ABS, DSC and ESP warnings usually trace to a wheel speed sensor, a "
    "reluctor ring or a wiring fault rather than the module itself. We read "
    "the fault with the factory software and repair the cause, which is "
    "nearly always the cheaper part."),
 ),
 "reviews": ("kayode", "anan"),
 "faqs": (
   ("How do I know my brakes need attention?",
    "A brake warning on the dash, a grinding or squealing noise, a pulsing "
    "pedal under braking, or a longer stopping distance are the usual signs. "
    "Most German cars warn you electronically before the pads are through, "
    "but a noise or a change in feel is worth checking sooner."),
   ("Do you have to replace the rotors with the pads?",
    "Often, yes. German rotors are made to wear with the pads and carry a "
    "minimum thickness stamped on the hub; once they are at or near it, new "
    "pads on old rotors wear fast and stop poorly. We measure them and tell "
    "you where they stand before you decide."),
   ("Why does brake fluid need changing if I have not lost any?",
    "Brake fluid absorbs moisture from the air over time, which lowers its "
    "boiling point and corrodes the ABS unit from the inside. That is why "
    "every German manufacturer publishes a fixed interval, usually two years, "
    "regardless of mileage."),
   ("Can you do the rear brakes on a car with an electronic parking brake?",
    "Yes. The parking brake actuators have to be retracted through the "
    "factory diagnostic software before the pads come out, and put back into "
    "service afterwards. It is a routine job with the right tools and a very "
    "expensive one without them."),
   ("Will aftermarket pads hurt my car?",
    "Cheap pads can. The wrong compound changes pedal feel, can glaze the "
    "rotor and often produces the dust and squeal owners complain about. We "
    "fit OEM or OEM-equivalent pads in the compound the car was designed "
    "around; if you want a performance compound, we will tell you the "
    "trade-offs."),
   ("Will my brake warning light go off?",
    "Yes, once the sensor that triggered it is replaced. A wear sensor that "
    "has warned has been worn through and is a one-time part. We replace it "
    "with the pads and reset the service reminder through the factory "
    "interface so the car's own schedule stays accurate."),
 ),
},
)
