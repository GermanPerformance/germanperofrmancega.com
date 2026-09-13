"""Audi service pages, built by tools/build_service_pages.py.

One dict per page (the A4, A6, Q5, Q7, S and RS). Every technical claim is a
documented characteristic of the marque; nothing about pricing, turnaround
or certification is invented. The dict shape is the one build_service_pages
renders: slug, brand, [marque], h1 (three lines), title, desc, sub,
cards_head, cards_sub, cards, why_head, why_lead, why_points, faq_head,
faqs, cta, cta_sub.
"""

PAGES = (
{
 "slug": "audi-oil-change-snellville-ga.html",
 "brand": "Audi",
 "h1": ("AUDI", "OIL", "CHANGE"),
 "title": "Audi Oil Change Snellville GA | German Performance",
 "desc": ("Audi oil change in Snellville, GA. VW 502/504/508-approved oil for "
          "your engine, OEM filter, 2.0T consumption and leak check, service "
          "reset. Call (678) 395-7459."),
 "sub": ("Audi oil service in Snellville, GA — for the A3, A4, A5, A6, Q3, Q5, "
         "Q7, S and RS models. The VW 502, 504 or 508 approval your engine "
         "calls for, an OEM filter, the consumption and leak points these "
         "engines are known for checked, and the reminder reset properly."),
 "cards_head": ("A PROPER AUDI", "OIL SERVICE"),
 "cards_sub": ("Audi engines are approved for specific VW oil standards that "
               "changed by generation, run intervals that depend on which one "
               "you have, and — on the 2.0T especially — have a well-documented "
               "appetite for oil when the wrong one goes in."),
 "cards": [
   ("The Right VW Approval",
    "Audi lists an oil standard per engine: VW 502 00 for most older gasoline "
    "engines, 504 00 for the longlife schedule, 508 00 for the newest 2.0T and "
    "3.0T engines that run 0W-20, and 507 00 for the TDI. They are not "
    "interchangeable — a 508 00 engine given a thicker 502 oil, or the "
    "reverse, is a common cause of complaints. We fill the standard Audi lists "
    "for your engine code."),
   ("The 2.0T's Consumption",
    "The EA888 2.0T is known for oil consumption, especially the earlier "
    "versions, and for a crankcase ventilation valve that fails and pulls oil "
    "into the intake. We check the level history, the PCV valve and the "
    "intake for signs of it, so you know whether your engine is using oil and "
    "why."),
   ("Cartridge Filter and Cooler Seals",
    "An OEM or OEM-equivalent cartridge filter with new sealing rings and a "
    "new drain plug washer. While the filter housing is open we look at the "
    "oil cooler and filter housing gaskets, the usual source of the oil smell "
    "after a drive."),
   ("Level Confirmed Correctly",
    "The 2.0T holds less oil than it looks like it should and reads the level "
    "electronically on newer cars. We verify the level with the engine warm "
    "and the car level before handover rather than trusting the fill quantity "
    "in the book."),
   ("Timing Chain Awareness",
    "On the 2008 to 2013 2.0T the timing chain tensioner is a known failure, "
    "and oil that has been left too long is part of what wears the chain. We "
    "listen for it cold and tell you what we hear. Catching it as a rattle is "
    "a repair; missing it is an engine."),
   ("Service Reminder Reset",
    "The oil life monitor is reset through Audi-compatible diagnostics or the "
    "MMI, whichever the car supports, so the schedule it reports is the one we "
    "set. The car gets a multi-point inspection while it is on the lift."),
 ],
 "why_head": ("AUDI OIL", "DONE RIGHT"),
 "why_lead": ("Audi has changed its oil standard three times in fifteen years, "
              "and the engine that consumed the most oil in that period is the "
              "one under most of the hoods we see. Getting the approval, the "
              "level and the interval right is the whole job."),
 "why_points": [
   "VW 502 00, 504 00, 508 00 or 507 00 oil matched to your engine code",
   "Intervals set for the engine you have, not the longest one on the sticker",
   "OEM cartridge filters with new sealing rings and drain washer",
   "Oil level verified at operating temperature before handover",
   "PCV valve, cooler gasket and consumption checked on every 2.0T",
   "Oil life monitor reset through Audi-compatible diagnostics",
 ],
 "faq_head": ("AUDI OIL CHANGE", "FAQ"),
 "faqs": [
   ("How often does an Audi need an oil change?",
    "Audi's schedule is 10,000 miles or once a year on most models. For the "
    "turbocharged engines, and for any 2.0T with a history of consumption, we "
    "recommend 5,000 to 7,500 miles. The longer interval assumes the "
    "longlife-approved oil and steady highway driving; short trips and "
    "stop-start use are harder on the oil than the mileage suggests."),
   ("Which oil standard does my Audi need?",
    "The engine code decides it. Older gasoline engines are approved for VW "
    "502 00, the longlife schedule uses 504 00, the newest 2.0T and 3.0T "
    "engines are built for the thin 508 00 grade, and the diesels use 507 "
    "00. Audi prints the standard on the oil filler cap, and that is what "
    "goes in — an oil that meets a general industry grade but not the VW "
    "standard is the wrong oil for the engine."),
   ("Is it normal for my Audi to use oil?",
    "Some consumption on a turbocharged engine is normal, but the 2.0T has a "
    "documented history of using more than it should, particularly 2009 to "
    "2011 cars, and Audi revised the pistons and rings because of it. If "
    "yours needs a quart between changes it is worth measuring properly and "
    "checking the crankcase ventilation valve, which is a common and "
    "inexpensive cause."),
   ("Why does my Audi smell like burning oil after driving?",
    "On the 2.0T the usual sources are the oil filter housing gasket and the "
    "oil cooler seal, both of which drip onto hot parts below. The valve cover "
    "gasket and the rear main seal are the other candidates. We check the "
    "filter housing and cooler at every oil service and tell you what we "
    "found."),
   ("Will you reset the service reminder?",
    "Yes, through Audi-compatible diagnostics or the car's own menu, so the "
    "oil life monitor and the inspection counter are correct rather than "
    "simply cleared."),
   ("Does my Audi have to go to the dealer for oil changes under warranty?",
    "No. The Magnuson-Moss Warranty Act stops a manufacturer from requiring "
    "dealer maintenance as a condition of the warranty. What Audi can insist "
    "on is the correct VW-standard oil, the right filter and a record of the "
    "service — all of which you get here, in writing."),
 ],
 "cta": ("AUDI OIL SERVICE", "DUE?"),
 "cta_sub": "Call with the model and year — we will confirm the VW standard your engine needs.",
},
{
 "slug": "audi-brake-service-snellville-ga.html",
 "brand": "Audi",
 "h1": ("AUDI", "BRAKE", "REPAIR"),
 "title": "Audi Brake Repair Snellville GA | German Performance",
 "desc": ("Audi brake repair in Snellville, GA. Pads, rotors, wear sensor, "
          "electronic parking brake service mode, S and RS brakes, fluid "
          "flush. Call (678) 395-7459."),
 "sub": ("Audi brake repair in Snellville, GA — pads, rotors, sensors, fluid "
         "and the electronic parking brake, from an A4 to an RS. Done in the "
         "order the car requires, with the parts the car was built for."),
 "cards_head": ("AUDI BRAKE", "SERVICE"),
 "cards_sub": ("An Audi brake job is conventional at the front and electronic at "
               "the back: a wear sensor on one axle only, an electronic parking "
               "brake that has to be put into service mode, and rotors sized "
               "for the weight of a quattro that are replaced rather than "
               "machined."),
 "cards": [
   ("Pads and Rotors Together",
    "Audi rotors are light and wear with the pads, and on the heavier quattro "
    "sedans and SUVs they wear quickly. We measure every rotor against its "
    "minimum and replace it when it is near the limit, with OEM or "
    "OEM-equivalent pads and rotors matched to the car."),
   ("Electronic Parking Brake Service Mode",
    "Since the 2009 A4 most Audis carry the parking brake motors on the rear "
    "calipers. The rear pads cannot be replaced without putting the system "
    "into service mode with Audi-compatible diagnostics, and it must be "
    "cycled afterwards. Forcing the pistons back breaks the actuators; we "
    "have seen it."),
   ("Wear Sensor Where Fitted",
    "Most Audis carry a wear sensor on the front axle only. The rear pads give "
    "no warning, which is how a car ends up with a rear rotor scored by a pad "
    "worn to the backing plate. We measure all four corners every time the "
    "car is up."),
   ("S and RS Brakes",
    "The S and RS models carry large multi-piston front calipers, wave or "
    "drilled rotors, and pads with a compound that is noisy cold by design. "
    "Wave rotors cannot be machined. We fit the specified parts and measure "
    "the rotors to their own limits, and can advise on a quieter street pad "
    "if the car never sees a track."),
   ("Brake Fluid on Audi's Schedule",
    "Audi specifies a brake fluid change every two years regardless of "
    "mileage, because the fluid absorbs water and the ABS and stability "
    "control depend on it. We flush it with the DOT 4 grade Audi specifies "
    "and bleed every corner, running the ABS pump through diagnostics on "
    "the cars that need it to purge the unit."),
   ("Warning Lights Resolved",
    "Brake and parking brake warnings on an Audi are logged in the ABS and "
    "parking brake modules, and they do not always clear when the fault is "
    "fixed. We read the codes before and after, and clear them through the "
    "diagnostics the car expects."),
 ],
 "why_head": ("AUDI BRAKES", "DONE RIGHT"),
 "why_lead": ("The parts on an Audi brake job are straightforward. What "
              "separates a good one from a bad one is the parking brake "
              "service mode, the rear pads nobody measured, and rotors that "
              "were machined below their minimum. We do the whole job, in the "
              "right order."),
 "why_points": [
   "Rotors measured against their minimum and replaced, not machined thin",
   "Electronic parking brake put in service mode and cycled after rear pads",
   "All four corners measured — the rears have no sensor",
   "OEM or OEM-equivalent pads and rotors; S and RS compounds where specified",
   "Brake fluid flushed on Audi's two-year schedule, ABS bled where required",
   "ABS and parking brake modules read and cleared through diagnostics",
 ],
 "faq_head": ("AUDI BRAKE REPAIR", "FAQ"),
 "faqs": [
   ("How do I know my Audi brakes need work?",
    "The front wear sensor puts a warning in the cluster before the front "
    "pads are finished. The rears give no warning on most models, so grinding "
    "from the back, a longer pedal, a pull or a pulsing through the wheel are "
    "the signs. Pad and rotor thickness go on the inspection sheet at every "
    "visit, so the rears get caught before they grind."),
   ("Can my Audi's rotors be machined instead of replaced?",
    "Rarely worth it. They are made thin for weight and wear along with the pads, and a "
    "quattro sedan or SUV is heavy enough to wear them fast. By the second set "
    "they are usually at or below the minimum thickness stamped on the rotor. "
    "Machining one that close to the limit leaves it under it, so replacing "
    "them with the pads is the right call."),
   ("Do the rear pads need anything special on an Audi with an electronic parking brake?",
    "Yes — the parking brake has to be in service mode first. The rear "
    "calipers carry the parking brake motors, and pushing a piston back "
    "against a live actuator strips it. Service mode is entered with "
    "Audi-compatible diagnostics, the pads go in, and the system is cycled "
    "afterwards to seat them and confirm it holds."),
   ("Why does Audi want the brake fluid changed every two years?",
    "Because it absorbs water. Moisture lowers the boiling point — the pedal "
    "goes long on a hot descent — and it corrodes the ABS unit from the "
    "inside, which is the expensive part. Audi puts the flush on the "
    "schedule every two years regardless of mileage, and it is inexpensive "
    "next to an ABS module."),
   ("Why do my S or RS brakes squeal?",
    "The pad compound. Performance pads bite hardest when hot and squeal cold "
    "as a result. That is the compound doing its job, not a problem with the "
    "brakes. If the car never sees a track we "
    "can fit a quieter street compound; if it does, keep the one Audi "
    "specifies."),
   ("Will the brake warning light go off once the work is done?",
    "Usually, but not always. Some faults stay logged in the ABS or parking "
    "brake module until they are cleared with diagnostics, and a parking "
    "brake that was forced during a previous repair will keep a fault stored. "
    "We read and clear the modules as part of the job."),
 ],
 "cta": ("AUDI BRAKES", "DUE?"),
 "cta_sub": "Tell us the model and year on the phone — the parking brake alone changes what the job involves.",
},
{
 "slug": "audi-suspension-repair-snellville-ga.html",
 "brand": "Audi",
 "h1": ("AUDI", "SUSPENSION", "REPAIR"),
 "title": "Audi Suspension Repair Snellville GA | German Performance",
 "desc": ("Audi suspension repair in Snellville, GA. Upper control arm kits, "
          "struts, adaptive dampers, air suspension, RS DRC and alignment to "
          "spec. Call (678) 395-7459."),
 "sub": ("Audi suspension repair in Snellville, GA — control arms and bushings, "
         "struts and shocks, adaptive dampers, air suspension on the allroad, "
         "A8 and Q7, and the alignment that follows, from an A4 to an RS."),
 "cards_head": ("AUDI SUSPENSION", "REPAIR"),
 "cards_sub": ("Audi's front suspension is a multi-link design with more arms "
               "and more bushings than most cars, which is why it steers the "
               "way it does and why it wears the way it does. The failures are "
               "well known by generation, and so is the fix."),
 "cards": [
   ("Upper Control Arms",
    "The A4, A6 and their S models use four upper links per side, and their "
    "ball joints and bushings are the most common wear point on the car — a "
    "clunk over bumps and a steering wheel that is never quite centred. On "
    "the older cars they are replaced as a kit, both sides, with OEM or "
    "OEM-equivalent arms; on the newer ones the same joints go, and we "
    "replace what has failed."),
   ("Struts, Shocks and Adaptive Dampers",
    "Dampers go on in axle pairs — one new and one tired leaves the car "
    "uneven — with new top mounts and bearings, since a worn mount is often "
    "the noise that was blamed on the strut. Cars with Audi's adaptive damping — magnetic ride on the TT "
    "and R8, Dynamic Chassis Control on the later models — need the correct "
    "adaptive part and, where the car requires it, calibration afterwards. We "
    "fit what the car was built with."),
   ("Air Suspension",
    "The allroad, A8 and Q7 with air suspension lose it the same way: a strut "
    "that leaks overnight, then a compressor that wears out keeping up. A car "
    "that sits low at one corner in the morning is telling you. The leaking "
    "strut is the repair; if the compressor has been running hot to keep up, "
    "it comes out too, before it fails on the road."),
   ("RS Dynamic Ride Control",
    "The RS4 and RS6 use hydraulically cross-linked dampers that hold the car "
    "flat in corners and are known to leak with age. When they do, the ride "
    "goes soft and the fluid shows on the damper. We diagnose it properly and "
    "replace the dampers with the correct DRC units."),
   ("Bearings, Links and the Noise You Hear",
    "A hum that rises with speed is a wheel bearing; a click on turns is a CV "
    "joint; a rattle over small bumps is a sway bar link. They are easy to "
    "confuse and cheap to misdiagnose. We find the noise on the lift before "
    "we replace anything."),
   ("Alignment to Audi Specification",
    "Every suspension repair ends with a four-wheel alignment to Audi's "
    "figures for the model. On a multi-link front end the arms set the camber "
    "and caster; replace them without an alignment and the car will pull and "
    "wear its tires inside a few thousand miles."),
 ],
 "why_head": ("AUDI SUSPENSION", "DONE RIGHT"),
 "why_lead": ("An Audi with a clunk in the front, a wheel that will not centre "
              "or a corner that sags overnight has one of a short list of "
              "problems. Knowing the list by generation, replacing arms as the "
              "sets they are, and aligning the car afterwards is the whole "
              "difference."),
 "why_points": [
   "Upper control arms replaced as complete kits on the cars that need it",
   "Struts and shocks in pairs with new mounts; adaptive dampers where fitted",
   "Air suspension struts and compressors on the allroad, A8 and Q7",
   "RS Dynamic Ride Control dampers diagnosed and replaced correctly",
   "Bearings, CV joints and links identified on the lift, not guessed",
   "Four-wheel alignment to Audi's specification after every repair",
 ],
 "faq_head": ("AUDI SUSPENSION", "FAQ"),
 "faqs": [
   ("Why does my Audi clunk over bumps?",
    "On an A4 or A6 it is usually one of the upper control arm ball joints, "
    "which are the best-known wear point on Audi's multi-link front "
    "suspension. Sway bar links and strut mounts make a similar noise, so the "
    "car goes on the lift and gets rocked, pried and listened to before any "
    "arm is ordered. On the older cars, if one arm has gone the rest are "
    "close behind, which is why they are replaced as a set."),
   ("Why is my steering wheel off-centre?",
    "Worn control arm bushings let the geometry move, and the wheel is the "
    "first thing you notice. An alignment on worn arms is wasted — it will "
    "drift again within weeks — so we check the arms first and align the car "
    "after the repair."),
   ("Why does my Audi sit low at one corner in the morning?",
    "That is the air suspension. A strut is leaking overnight and the "
    "compressor is pumping the car back up when you start it; it will keep "
    "doing that until the compressor wears out too. Replacing the strut is "
    "the repair, and the compressor if it has been working overtime for a "
    "while."),
   ("What is Dynamic Ride Control and how does it fail?",
    "DRC is the hydraulic system on the RS4 and RS6 that links the dampers "
    "diagonally to keep the car flat in corners. The dampers leak with age; "
    "the ride goes soft and there is fluid on the damper body. The fix is the "
    "correct DRC damper, not a conventional replacement, which would leave "
    "the system unbalanced."),
   ("Why does an Audi need an alignment after control arms?",
    "Because on the multi-link front end the arms are the geometry — camber "
    "and caster are set by their lengths and their bushings — so new arms "
    "move it. The car is aligned to Audi's figures after every repair; "
    "without that, it pulls and eats the inside edge of the front tires."),
   ("Which parts do you use for Audi control arms?",
    "The manufacturers that supply Audi, in OEM or OEM-equivalent form. "
    "Control arms are where a cheap part shows first — a ball joint loose "
    "again within a year, and the alignment gone with it — so we do not fit "
    "them."),
 ],
 "cta": ("AUDI SUSPENSION", "FEELING LOOSE?"),
 "cta_sub": "Call and describe the noise or the pull — on an Audi it usually points to one arm.",
},
)
