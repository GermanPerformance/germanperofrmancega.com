#!/usr/bin/env python3
"""Build one repair hub per marque.

The site had 30 service pages and no brand page, so nothing targeted the
higher-volume "BMW repair Snellville" style query, and the 30 service pages
had no parent. These hubs are that parent.

Copy structure is Before-After-Bridge:

  Before  the symptom that made someone search, and the real fear behind it
          -- paying to have parts replaced until the noise stops
  After   knowing what is actually wrong and what it costs before committing
  Bridge  marque-specific diagnosis with the factory software, from a shop
          that only works on German cars

Offer alignment matters here because the only conversion is a phone call to a
shop open Mon-Fri. Asking a worried owner to "schedule service" demands a
commitment they are not ready to make. Asking them to describe the symptom and
hear what we would check first matches where they actually are.

Every failure mode named below is a genuine, well-documented issue for that
marque. Nothing about pricing, turnaround or certifications is invented.

Run from the repo root:  python3 tools/build_brand_hubs.py
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://germanperformancega.com"
TEMPLATE_PAGE = "bmw-oil-change-snellville-ga.html"

BRANDS = [
{
 "slug": "bmw-repair-snellville-ga.html",
 "brand": "BMW",
 "possessive": "BMW",
 "h1": ('BMW', 'REPAIR', '&amp; SERVICE'),
 "title": "BMW Repair Snellville GA | BMW Specialists | German Performance",
 "desc": "Independent BMW repair and service in Snellville, GA. Factory ISTA diagnostics, OEM parts, 12-month warranty. Serving Gwinnett County. Call (678) 395-7459.",
 "crumb": "BMW Repair — Snellville, GA",
 "sub": "Most people find us because something on their BMW is behaving oddly and the last shop wanted to start replacing parts to find out why. We diagnose first, using the same software the dealer runs, and tell you what we actually found.",
 "tool": "ISTA",
 "before": [
   ("A warning you can't interpret",
    "BMW dashboards report symptoms, not causes. A drivetrain malfunction message can mean a coil, a fuel injector, a boost leak or a timing issue, and a generic code reader will not tell them apart."),
   ("A repair bill that keeps growing",
    "The expensive version of a cheap diagnosis is paying for two or three parts before the right one gets replaced. That is the pattern we most often hear about from people calling us second."),
   ("Nobody explaining the why",
    "Being told a car needs a part is not the same as understanding what failed and what happens if it waits. You should get both."),
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
 "models": "1, 2, 3, 4, 5, 6, 7 and 8 Series, X1 through X7, Z4, and the full M range.",
 "faq": [
  ("Do I have to take my BMW to the dealer for service?",
   "No. Under the Magnuson-Moss Warranty Act a dealer cannot void your factory warranty because an independent shop performed routine maintenance or repairs, provided the work is done correctly with appropriate parts. We document everything so your records are dealer-presentation ready."),
  ("Do you use the same diagnostic software as a BMW dealer?",
   "Yes. We run ISTA, which gives us access to every control module, live data, adaptations and coding, rather than the generic fault codes a basic OBD-II scanner reads."),
  ("What is the drivetrain malfunction message on my BMW?",
   "It is the car protecting itself after detecting a fault it considers serious enough to reduce power. The underlying cause varies widely -- ignition, fuel delivery, boost control and sensors are all candidates -- so it needs a proper scan rather than a guess."),
  ("Can you reset the BMW service indicator?",
   "Yes. Every BMW service we perform includes the correct Condition Based Service reset, so your dashboard reflects what has actually been done."),
 ],
},
{
 "slug": "mercedes-repair-snellville-ga.html",
 "brand": "Mercedes-Benz",
 "possessive": "Mercedes",
 "h1": ('MERCEDES-BENZ', 'REPAIR', '&amp; SERVICE'),
 "title": "Mercedes Repair Snellville GA | Mercedes-Benz Specialists | German Performance",
 "desc": "Independent Mercedes-Benz repair and service in Snellville, GA. XENTRY diagnostics, OEM parts, 12-month warranty. Serving Gwinnett County. Call (678) 395-7459.",
 "crumb": "Mercedes-Benz Repair — Snellville, GA",
 "sub": "A Mercedes rarely fails loudly. It sags a little at one corner, or shifts less smoothly than it did, or shows a message with no obvious cause. We find out which system is actually responsible before anything gets replaced.",
 "tool": "XENTRY/DAS",
 "before": [
   ("Symptoms that creep rather than break",
    "Air suspension settling overnight, a gearbox that hesitates when cold, a slow oil weep. Easy to live with, expensive to ignore."),
   ("Quotes for whole assemblies",
    "A great deal of Mercedes work gets quoted as complete units when the failure is one component inside it. Conductor plates and valve bodies are the common example."),
   ("No clear picture of urgency",
    "You should know which of the findings needs attention now and which can reasonably wait until next time."),
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
 "models": "A, C, E and S-Class, CLA, CLS, GLA, GLB, GLC, GLE, GLS, G-Class, SL, SLK, Sprinter, and AMG variants.",
 "faq": [
  ("Will servicing my Mercedes outside the dealer affect my warranty?",
   "No. Federal law protects your right to use an independent shop for maintenance and repairs without voiding the factory warranty, as long as the work is performed correctly with appropriate parts. We keep thorough records for exactly this reason."),
  ("Why does checking Mercedes transmission fluid need a scan tool?",
   "Because the level is only meaningful at a specific fluid temperature. Checking it cold or hot gives a misleading reading, which is how transmissions end up incorrectly filled."),
  ("My Mercedes sits lower on one side overnight. What is that?",
   "Usually an air suspension leak, most often a strut, though the compressor or valve block can produce the same symptom. It is worth diagnosing early, because a failing compressor that runs constantly tends to destroy itself."),
  ("Do you service AMG models?",
   "Yes. AMG variants use different components and torque specifications than the standard range, and we set them up to the correct specification."),
 ],
},
{
 "slug": "audi-repair-snellville-ga.html",
 "brand": "Audi",
 "possessive": "Audi",
 "h1": ('AUDI', 'REPAIR', '&amp; SERVICE'),
 "title": "Audi Repair Snellville GA | Audi Specialists | German Performance",
 "desc": "Independent Audi repair and service in Snellville, GA. ODIS and VCDS diagnostics, OEM parts, 12-month warranty. Serving Gwinnett County. Call (678) 395-7459.",
 "crumb": "Audi Repair — Snellville, GA",
 "sub": "Audi shares a great deal of engineering with Volkswagen, which means the failure patterns are well understood by anyone who works on both. We do, and we confirm what your car actually has by VIN before quoting anything.",
 "tool": "ODIS and VCDS",
 "before": [
   ("Oil consumption you were told is normal",
    "Some consumption is normal. A quart every thousand miles usually is not, and it has identifiable causes worth investigating."),
   ("Belt or chain, and nobody is sure which",
    "The interval and the risk are completely different between the two, and it depends on the engine rather than the model year."),
   ("Rough running with no stored fault",
    "Carbon buildup rarely sets a clean code early on. It shows up as a car that simply does not feel right."),
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
 "models": "A3, A4, A5, A6, A7, A8, Q3, Q5, Q7, Q8, TT, R8, and S and RS performance variants.",
 "faq": [
  ("Does my Audi have a timing belt or a timing chain?",
   "It depends on the engine, not the model year alone. Several older 2.0T, 2.7T and 3.0 V6 engines use belts while many newer engines use chains. We confirm from the VIN rather than assuming, because the service is completely different."),
  ("Why does my Audi use so much oil?",
   "On certain 2.0T engines the common causes are piston ring design and a failing PCV system. Both are identifiable, and treating consumption as simply normal is how engines end up damaged."),
  ("Can you service quattro all-wheel drive?",
   "Yes, including Haldex fluid and filter service on transverse quattro systems and differential service on longitudinal ones. It is routinely skipped maintenance."),
  ("Do you use the same software an Audi dealer uses?",
   "We run ODIS and VCDS, which give full module access, live data, adaptations and coding rather than generic fault codes."),
 ],
},
{
 "slug": "porsche-repair-snellville-ga.html",
 "brand": "Porsche",
 "possessive": "Porsche",
 "h1": ('PORSCHE', 'REPAIR', '&amp; SERVICE'),
 "title": "Porsche Repair Snellville GA | Porsche Specialists | German Performance",
 "desc": "Independent Porsche repair, service and inspection in Snellville, GA. PIWIS diagnostics, OEM parts, 12-month warranty. Serving Gwinnett County. Call (678) 395-7459.",
 "crumb": "Porsche Repair — Snellville, GA",
 "sub": "Porsche owners tend to arrive with a specific worry rather than a vague one, and usually a well-founded one. We are equipped to answer it properly, whether that is a pre-purchase inspection or a noise you would rather not ignore.",
 "tool": "PIWIS",
 "before": [
   ("A known weak point you have read about",
    "Porsche communities document failure modes thoroughly. That is useful, but it also means owners often arrive convinced of a diagnosis they have not had confirmed."),
   ("A car you are considering buying",
    "The gap between a well-kept example and a neglected one is enormous, and it is not visible from the outside."),
   ("A shop that will not commit",
    "Plenty of general shops will decline Porsche work outright, or take it on without the right tooling."),
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
 "models": "911, Boxster, Cayman, Panamera, Macan, Cayenne and Taycan.",
 "faq": [
  ("Do you perform Porsche pre-purchase inspections?",
   "Yes. Our inspection covers a full fault code scan, structural assessment, fluid condition and the known weak points for the specific model and year, with a written report you can use in negotiation."),
  ("Should I worry about the IMS bearing on my Porsche?",
   "It depends on the exact engine and model year, as the risk is not uniform across the M96 and M97 family. We will tell you where your specific car sits rather than generalising."),
  ("Do you have the correct Porsche diagnostic equipment?",
   "Yes. We use PIWIS, which is the factory system, giving full module access, adaptations and coding rather than generic fault code reading."),
  ("Do you service the Cayenne and Macan as well as the sports cars?",
   "Yes, the full current and recent Porsche range, including the Cayenne V8 coolant pipe issue that affects earlier models."),
 ],
},
{
 "slug": "volkswagen-repair-snellville-ga.html",
 "brand": "Volkswagen",
 "possessive": "VW",
 "h1": ('VOLKSWAGEN', 'REPAIR', '&amp; SERVICE'),
 "title": "Volkswagen Repair Snellville GA | VW Specialists | German Performance",
 "desc": "Independent Volkswagen repair and service in Snellville, GA. ODIS and VCDS diagnostics, OEM parts, 12-month warranty. Serving Gwinnett County. Call (678) 395-7459.",
 "crumb": "Volkswagen Repair — Snellville, GA",
 "sub": "Volkswagen engines share their design with Audi, and so do their failure patterns. The advantage of a shop that works on both every week is that we have usually seen your specific problem before.",
 "tool": "ODIS and VCDS",
 "before": [
   ("A rattle on cold start",
    "On the EA888 family this is worth taking seriously rather than waiting to see whether it gets worse."),
   ("Being quoted a replacement engine",
    "Most of what gets called engine failure is one component. It is worth a second opinion before accepting that number."),
   ("A coolant smell with no visible leak",
    "The usual sources hide behind covers and only show themselves under pressure."),
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
 "models": "Golf, GTI, Jetta, Passat, Tiguan, Atlas, Arteon, Beetle, and TDI diesel models.",
 "faq": [
  ("What is the rattle on cold start on my VW?",
   "On earlier EA888 engines it is commonly the timing chain tensioner allowing slack before oil pressure builds. It is worth diagnosing quickly, because the consequence of a failure is serious."),
  ("Do you work on both TSI and TDI engines?",
   "Yes. Diesel work brings in injectors, glow plugs and emissions components that gasoline engines do not have, and we have the VW-specific tooling for both."),
  ("Does my DSG transmission need servicing?",
   "Yes. The dual-clutch unit has a scheduled fluid and filter service, and neglecting it is a common cause of hesitation and rough low-speed shifting."),
  ("Can you repair my VW engine rather than replace it?",
   "Usually. Most of what is described as engine failure turns out to be a specific component such as a tensioner, gasket, turbo or PCV valve. We diagnose before quoting."),
 ],
},
]

# Which existing service pages belong to each hub.
SERVICE_LINKS = {
 "BMW": [("bmw-oil-change-snellville-ga.html","Oil Change"),
   ("bmw-suspension-repair-snellville-ga.html","Suspension Repair"),
   ("bmw-transmission-repair-snellville-ga.html","Transmission Repair"),
   ("bmw-cooling-system-repair-snellville-ga.html","Cooling System Repair"),
   ("bmw-battery-replacement-snellville-ga.html","Battery Replacement"),
   ("bmw-spark-plug-replacement-snellville-ga.html","Spark Plugs"),
   ("bmw-wheel-alignment-snellville-ga.html","Wheel Alignment"),
   ("bmw-differential-service-snellville-ga.html","Differential Service")],
 "Mercedes-Benz": [("mercedes-oil-change-snellville-ga.html","Oil Change"),
   ("mercedes-brake-service-snellville-ga.html","Brake Service"),
   ("mercedes-suspension-snellville-ga.html","Suspension Repair"),
   ("mercedes-transmission-snellville-ga.html","Transmission Service"),
   ("mercedes-ac-repair-snellville-ga.html","AC Repair"),
   ("mercedes-engine-diagnostics-snellville-ga.html","Engine Diagnostics")],
 "Audi": [("audi-oil-change-snellville-ga.html","Oil Change"),
   ("audi-brake-service-snellville-ga.html","Brake Service"),
   ("audi-suspension-repair-snellville-ga.html","Suspension Repair"),
   ("audi-timing-belt-snellville-ga.html","Timing Belt"),
   ("audi-quattro-service-snellville-ga.html","Quattro AWD Service")],
 "Porsche": [("porsche-brake-service-snellville-ga.html","Brake Service"),
   ("porsche-inspection-snellville-ga.html","Full Inspection"),
   ("pre-purchase-inspection-german-car-ga.html","Pre-Purchase Inspection")],
 "Volkswagen": [("volkswagen-oil-change-snellville-ga.html","Oil Change"),
   ("volkswagen-engine-repair-snellville-ga.html","Engine Repair"),
   ("volkswagen-timing-chain-snellville-ga.html","Timing Chain")],
}

UNIVERSAL = [("german-car-check-engine-light-snellville.html","Check Engine Light"),
             ("german-car-ac-repair-snellville-ga.html","AC Repair"),
             ("german-car-tune-up-snellville-ga.html","Tune-Up"),
             ("german-car-emissions-repair-snellville-ga.html","Emissions Repair")]


def skeleton():
    """Nav, mobile menu, trust bar, call bar and footer from a live page."""
    src = open(os.path.join(REPO_ROOT, TEMPLATE_PAGE), encoding="utf-8").read()
    grab = lambda p: re.search(p, src, re.S).group(0)
    return {
        "nav": grab(r'<nav>.*?</nav>'),
        "mob": grab(r'<div id="mobile-menu">.*?\n</div>'),
        "trust": grab(r'<div class="trust">.*?\n</div>'),
        "callbar": grab(r'<div class="call-bar">.*?\n</div>'),
        "footer": grab(r'<footer>.*?</footer>'),
        "scripts": grab(r'<script defer src="assets/js/site\.js[^>]*></script>'),
        "fonts": grab(r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*<link href="https://fonts\.googleapis[^>]*>'),
    }


def cards(items):
    return "\n".join(
        f'    <div class="card"><div class="ct">{t}</div><div class="cd">{d}</div></div>'
        for t, d in items)


def build(b, sk):
    url = f"{SITE}/{b['slug']}"
    svc = SERVICE_LINKS[b["brand"]]
    line1, line2, line3 = b["h1"]

    service_cards = "\n".join(
        f'    <a href="{h}" class="rel-card"><span class="rel-name">{b["possessive"]} {n}</span>'
        f'<span class="rel-go">&rarr;</span></a>' for h, n in svc)
    universal_cards = "\n".join(
        f'    <a href="{h}" class="rel-card"><span class="rel-name">{n}</span>'
        f'<span class="rel-go">&rarr;</span></a>' for h, n in UNIVERSAL)

    other = "".join(
        f'<a href="{o["slug"]}">{o["brand"]}</a>'
        for o in BRANDS if o["slug"] != b["slug"])

    faq_html = "\n".join(
        f'      <div class="fi fu"><button class="fq" onclick="toggleFaq(this)">{q}'
        f'<span class="ficon">+</span></button><div class="fa"><p>{a}</p></div></div>'
        for q, a in b["faq"])

    # The skeleton comes from a BMW page, so the trust bar names BMW. Re-brand
    # it -- shipping "BMW-Approved" on the Porsche hub is the same copy-paste
    # bug that was fixed across the service pages in Phase 1.
    trust = sk["trust"].replace(
        "BMW-Approved", f"{b['possessive']}-Approved")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{b["title"]}</title>
<meta name="description" content="{b["desc"]}">
<link rel="icon" type="image/png" href="assets/img/logo-144.png">
<link rel="canonical" href="{url}"/>
{sk["fonts"]}
<link rel="stylesheet" href="assets/css/tokens.css?v=2">
<link rel="stylesheet" href="assets/css/site.css?v=2">
<link rel="stylesheet" href="assets/css/werkstatt.css?v=2">
{sk["scripts"]}
</head>
<body>
{sk["nav"]}
{sk["mob"]}
<main>
<div class="breadcrumb"><a href="index.html">Home</a><span>/</span><span style="color:var(--silver)">{b["crumb"]}</span></div>
<section class="hero"><div class="hbg"></div><div class="hgrid"></div>
  <div class="hc">
    <div class="eyebrow fu">{b["brand"]} Specialists &nbsp;·&nbsp; Snellville, GA &nbsp;·&nbsp; <span style="color:var(--gold);font-weight:700">4.5★ Rated</span></div>
    <h1 class="fu">{line1}<br><span class="outline">{line2}</span><br><span class="accent">{line3}</span></h1>
    <p class="sub fu">{b["sub"]}</p>
    <div class="acts fu"><a href="tel:+16783957459" class="bp">Call and describe the symptom</a><a href="index.html#services" class="bg">All Services <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M9 4L13 8L9 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></a></div>
  </div>
</section>
{trust}

<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">Why people call us</div>
  <h2>WHAT USUALLY BRINGS<br><span style="color:var(--red)">A {b["possessive"].upper()} IN</span></h2>
  <p class="sd">Almost everyone who calls is somewhere in one of these three situations.</p></div>
  <div class="g3 fu">
{cards(b["before"])}
  </div>
</section>

<section style="background:var(--black)">
  <div class="fu"><div class="sl">Known weak points</div>
  <h2>WHAT WE LOOK FOR<br><span style="color:var(--red)">ON A {b["possessive"].upper()}</span></h2>
  <p class="sd">Every marque has its own failure patterns. Knowing them is the difference between diagnosing a car and experimenting on it.</p></div>
  <div class="g3 fu">
{cards(b["known"])}
  </div>
</section>

<section style="background:var(--carbon)">
  <div class="fu"><div class="sl">{b["brand"]} services</div>
  <h2>WHAT WE DO<br><span style="color:var(--red)">ON YOUR {b["possessive"].upper()}</span></h2></div>
  <div class="rel-grid fu">
{service_cards}
  </div>
  <div class="fu" style="margin-top:44px">
    <div class="sl">Any German make</div>
    <div class="rel-grid" style="margin-top:20px">
{universal_cards}
    </div>
  </div>
  <p class="sd fu" style="margin-top:36px"><strong style="color:var(--white)">Models we service:</strong> {b["models"]}</p>
</section>

<div class="cta-band fu"><div><div class="cbt">NOT SURE WHAT'S WRONG?<br>THAT'S THE POINT OF CALLING.</div><div class="cbs">Describe what the car is doing. We'll tell you what we'd check first.</div></div><a href="tel:+16783957459" class="bp">Call (678) 395-7459</a></div>

<section style="background:var(--carbon)">
  <div style="max-width:820px;margin:0 auto">
    <div class="sl fu">Common Questions</div><h2 class="fu">{b["brand"].upper()} <span style="color:var(--red)">FAQ</span></h2>
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>

<section style="background:var(--black)">
  <div class="fu"><div class="sl">Other German makes</div>
  <h2>WE ALSO<br><span style="color:var(--red)">SPECIALISE IN</span></h2></div>
  <div class="flinks fu" style="margin-top:28px">{other}<a href="dealer-vs-independent-german-car-repair.html">Dealer vs. Independent</a></div>
</section>

<section style="background:var(--black);padding:80px 60px;text-align:center">
  <div class="fu">
    <div class="sl" style="justify-content:center">Get Started</div>
    <h2 style="margin-bottom:20px">SNELLVILLE'S {b["possessive"].upper()} <span style="color:var(--red)">SPECIALISTS</span></h2>
    <p class="sd" style="margin:0 auto 44px;text-align:center;max-width:480px">Serving Snellville, Loganville, Grayson, Lawrenceville, and all of Gwinnett County.</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="tel:+16783957459" class="bp">Call (678) 395-7459</a>
      <a href="https://maps.google.com/?q=2144+Parkwood+Rd+NW+Snellville+GA+30078" target="_blank" rel="noopener" class="bg">Get Directions</a>
    </div>
  </div>
</section>
</main>
{sk["callbar"]}
{sk["footer"]}
</body></html>
'''


def main():
    sk = skeleton()
    for b in BRANDS:
        path = os.path.join(REPO_ROOT, b["slug"])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(b, sk))
        print(f"wrote {b['slug']}")
    print(f"\n{len(BRANDS)} brand hubs built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
