#!/usr/bin/env python3
"""Expand the dealer-vs-independent post and link it into the site.

The post was 378 words and had zero inbound links. Pouring links into a thin
page wastes them, so it is expanded first: a real comparison table, an honest
section on what the dealer is still better at, and practical guidance for a
reader deciding whether to switch. Contextual links to the relevant service
pages are woven into the prose rather than bolted on as a list.

Saying plainly where the dealer wins is deliberate. A comparison page that
only flatters its author reads as marketing; naming the cases where you are
not the right answer is what makes the rest credible.

Run from the repo root:  python3 tools/expand_post.py
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "dealer-vs-independent-german-car-repair.html"

CSS = """
/* Comparison table */
.spec-table{width:100%;border-collapse:collapse;margin:28px 0 8px;font-size:.95rem}
.spec-table th,.spec-table td{padding:14px 16px;text-align:left;border-bottom:1px solid rgba(255,255,255,.08);vertical-align:top}
.spec-table thead th{font-family:'Space Mono',monospace;font-size:.68rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--silver);border-bottom:1px solid rgba(255,255,255,.18)}
.spec-table tbody th{font-weight:400;color:var(--white);width:26%}
.spec-table td{color:var(--light)}
.spec-table .yes{color:var(--gold)}
.spec-table .no{color:var(--muted)}
.table-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.callout{border-left:2px solid var(--red);padding:4px 0 4px 20px;margin:28px 0;color:var(--light)}
.checklist{list-style:none;padding:0;margin:20px 0}
.checklist li{padding:9px 0 9px 28px;position:relative;color:var(--light);line-height:1.6}
.checklist li::before{content:'\\2713';position:absolute;left:0;color:var(--gold);font-weight:700}
"""

# Inserted after the existing "tools are the same" paragraph.
AFTER_TOOLS = """
  <p>What that access buys you is the work a generic scanner cannot touch. Registering a
  new battery to the charging system so it charges at the right rate, which is why a
  <a href="bmw-battery-replacement-snellville-ga.html">BMW battery replacement</a> is not
  simply a swap. Resetting the service computer after an
  <a href="bmw-oil-change-snellville-ga.html">oil change</a>. Reading the transmission's
  own adaptation values rather than guessing at a shift complaint. Calibrating driver
  assistance cameras after a windshield or suspension job.</p>
"""

# Replaces the two-column compare block.
TABLE = """
  <div class="table-scroll">
  <table class="spec-table">
    <thead>
      <tr><th scope="col">&nbsp;</th><th scope="col">Dealer service dept.</th><th scope="col">Independent specialist</th></tr>
    </thead>
    <tbody>
      <tr><th scope="row">Diagnostic software</th>
        <td>Factory systems</td>
        <td>Factory systems, at a shop that has invested in them</td></tr>
      <tr><th scope="row">Parts</th>
        <td>OEM</td>
        <td>OEM or OEM-equivalent, your choice on older cars</td></tr>
      <tr><th scope="row">Technician focus</th>
        <td>Every model in one brand's range</td>
        <td>German makes only</td></tr>
      <tr><th scope="row">Who you talk to</th>
        <td>A service advisor relaying to the tech</td>
        <td>The person doing the work</td></tr>
      <tr><th scope="row">Continuity</th>
        <td>Rarely the same technician twice</td>
        <td>The same technician across visits</td></tr>
      <tr><th scope="row">Typical lead time</th>
        <td>Often one to two weeks</td>
        <td>Usually the same week</td></tr>
      <tr><th scope="row">Recall work</th>
        <td class="yes">Yes &mdash; dealer only</td>
        <td class="no">No</td></tr>
      <tr><th scope="row">Warranty-covered repairs</th>
        <td class="yes">Yes &mdash; dealer only</td>
        <td class="no">No</td></tr>
      <tr><th scope="row">Software update campaigns</th>
        <td class="yes">Yes</td>
        <td class="no">Limited</td></tr>
    </tbody>
  </table>
  </div>
  <p>The last three rows matter, and they are the reason this is not a straight
  "independent is better" argument.</p>
"""

# Inserted before the closing CTA.
NEW_SECTIONS = """
  <h2>When the dealer is still the right call</h2>
  <p>There are jobs we will tell you to take to the dealer, and it is worth knowing which
  before you need them.</p>
  <p><strong>Open recalls and warranty repairs.</strong> These are paid for by the
  manufacturer and can only be carried out by a franchised dealer. If your car has an open
  recall, that work is free at the dealer and it would be absurd to pay us for it. The same
  goes for anything still covered by the factory warranty &mdash; claim it.</p>
  <p><strong>Goodwill claims on recently expired warranties.</strong> Manufacturers
  sometimes cover a repair just outside the warranty period, but that decision runs through
  the dealer network. If your car is a few months or a few thousand miles past expiry on an
  expensive component, ask the dealer first.</p>
  <p><strong>Brand-wide software campaigns.</strong> Some updates are distributed only
  through the manufacturer's own network. We can flash and code a great deal, but not every
  campaign is available outside a dealership.</p>
  <div class="callout">A useful rule: if the manufacturer is paying, go to the dealer. If
  you are paying, the comparison above applies.</div>

  <h2>How to judge any independent shop</h2>
  <p>Not every independent shop is equipped for German cars, and the gap between one that
  is and one that is not is wide. Whether or not you end up with us, these are the questions
  worth asking:</p>
  <ul class="checklist">
    <li><strong>Which factory software do you run?</strong> A specific answer &mdash; ISTA,
    XENTRY, ODIS, PIWIS &mdash; means something. "We have a scanner" does not.</li>
    <li><strong>Do you report service records to CARFAX?</strong> Documented history
    protects your resale value, and gaps in it cost you at sale.</li>
    <li><strong>OEM or aftermarket parts, and do I get a say?</strong> On a newer car the
    answer should lean OEM. On a fifteen-year-old car a good shop will talk you through
    where a quality aftermarket part is sensible.</li>
    <li><strong>What warranty comes with the work?</strong> Ours is 12 months or 12,000
    miles. Any serious shop will have a clear answer.</li>
    <li><strong>Will you show me what you replaced?</strong> A shop confident in its
    diagnosis has no reason to refuse.</li>
  </ul>

  <h2>What switching actually involves</h2>
  <p>Less than people expect. Bring whatever service records you have, or just the VIN
  &mdash; much of the history is readable from the car itself. On a first visit we scan
  every module and build a baseline, which tends to surface anything a previous shop
  cleared without fixing. From there you get a written report with photographs, and nothing
  proceeds without your approval.</p>
  <p>If you are not ready to commit to a repair, a
  <a href="pre-purchase-inspection-german-car-ga.html">pre-purchase inspection</a> or a
  straightforward <a href="german-car-check-engine-light-snellville.html">check engine
  light diagnosis</a> is a low-stakes way to see how a shop works before trusting it with
  anything major.</p>
"""


def main():
    path = os.path.join(REPO_ROOT, PAGE)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    if "spec-table" in content:
        print("post already expanded")
        return 0

    # 1. Extra detail after the diagnostics paragraph.
    anchor = "clears a code and calls it done.</p>"
    if anchor not in content:
        raise SystemExit("diagnostics paragraph not found")
    content = content.replace(anchor, anchor + "\n" + AFTER_TOOLS, 1)

    # 2. Replace the two-column comparison with a real table.
    compare = re.search(r'  <div class="compare">.*?\n  </div>\n', content, re.S)
    if not compare:
        raise SystemExit("compare block not found")
    content = content[:compare.start()] + TABLE + content[compare.end():]

    # 3. New sections before the closing call-to-action block.
    closing = '<div class="cta-block">'
    if closing not in content:
        raise SystemExit("closing CTA block not found")
    content = content.replace(closing, NEW_SECTIONS + "\n  " + closing, 1)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    css_path = os.path.join(REPO_ROOT, "assets", "css", "post.css")
    with open(css_path, encoding="utf-8") as fh:
        existing = fh.read()
    if ".spec-table{" not in existing:
        with open(css_path, "a", encoding="utf-8") as fh:
            fh.write(CSS)

    print("post expanded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
