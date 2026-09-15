#!/usr/bin/env python3
"""Apply the balanced redesign to every page except index.html.

index.html is hand-built; the one thing this tool writes to it is the nav
block (phone bar, nav, phone menu), so the Services menu stays in step on
all 49 pages. Its stylesheet and script versions are hand-edited. The
service, hub and info pages, the 404 page and the blog post share one
markup pattern, so the redesign reaches them by transformation rather
than by hand. Every rule below maps one piece of the old markup onto the
new system:

  * stylesheets are one inline critical block (fonts + tokens) and one
    bundle link (werkstatt + page sheet, tools/build_css.py), so a phone
    paints after one request instead of four; the legacy triple
    tokens -> page -> werkstatt is still recognised and rewritten, and
    the base no longer has to out-specify the page sheet it used to load after
  * a fixed phone bar above one nav and one mobile menu on every page,
    with the call button and hamburger grouped so the bar reads
    logo | links | call; About and Contact point at their own pages, so
    tools/link_info_pages.py is a no-op after this runs in either order;
    Services is a disclosure listing every page in tools/service_catalog.py
  * the fixed bottom call bar is removed; the phone bar and the nav
    button are the call paths on every screen
  * the hero grid overlay goes; the hero is centred by the base sheet
  * the trust strip drops from five cells to four so it splits evenly
    into 2x2 on a phone and 4x1 on a desktop
  * inline background, colour and spacing styles become classes, so the
    page sheets own the layout again
  * FAQ items become native <details>/<summary>, one open at a time
  * the footer wordmark becomes the logo, and the copyright line moves
    below the link row
  * the CARFAX Top-Rated shield sits beside every hero checklist (not the
    404's) and, linked to the CARFAX page, under the footer tagline
  * the review copy leads with the CARFAX rating and the years in
    business; Google keeps the review count, never the other way round
  * the hero headline runs two lines at the homepage's size -- the
    generators' three stacked words merge into a white line and a red one
    -- and the "Why German Performance" header leaves the half-width .two
    column for a centred .sh above the grid, like the landing pages

Idempotent: running it twice changes nothing the second time.

Run from the repo root:  python3 tools/apply_redesign.py
"""

import datetime
import functools
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_catalog import GROUPS, HUBS  # noqa: E402
import place  # noqa: E402
from redirects import site_pages  # noqa: E402
import urls  # noqa: E402
import build_css  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "34"

# The typefaces are served from assets/fonts/ (see tools/build_fonts.py):
# the @font-face rules travel inline in every page's <style id="critical">
# (tools/build_css.py), so the browser asks for the headline face as soon
# as it has the document. fonts_markup() survives only for the legacy
# Google Fonts rule below; the critical rule then replaces it. The Google Fonts
# block this replaces cost two hosts in series -- the CSS, then the file
# URLs read out of it -- before a heading could paint. Deliberately no
# <link rel="preload"> for the font: measured on an emulated slow 4G
# phone, three runs each, the 88 KB preload competed with the render-
# blocking CSS and put first paint 120 ms later and LCP 50 ms later than
# letting the stylesheet request it.
def fonts_markup():
    return f'<link rel="stylesheet" href="assets/css/fonts.css?v={VERSION}">'


GOOGLE_FONTS_RE = (r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
                   r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
                   r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">')

LOGO_NAV = (
    '<picture class="logo-pic"><source type="image/webp" '
    'srcset="assets/img/logo-144.webp 1x, assets/img/logo-288.webp 2x">'
    '<img src="assets/img/logo-144.png" alt="German Performance" width="132" '
    'height="44" decoding="async" fetchpriority="high"></picture>'
)
LOGO_FOOT = LOGO_NAV.replace(' fetchpriority="high"', ' loading="lazy"')

# The CARFAX Top-Rated shield, built by tools/build_badge.py at 128, 256
# and 384px tall. The markup carries the real dimensions of the 128px file
# so a rebuilt badge reaches every page on the next run.
BADGE = "assets/img/carfax-top-rated-2025"
BADGE_ALT = "CARFAX 2025 Top-Rated Service Center: German Performance"
CARFAX_URL = "https://www.carfax.com/Reviews-German-Performance-Snellville-GA_IY4SR7AEBP"


@functools.lru_cache(maxsize=None)
def badge_size():
    """Width and height of the 128px badge, read from its PNG header."""
    path = os.path.join(REPO_ROOT, f"{BADGE}-128.png")
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
    except FileNotFoundError:
        raise SystemExit(f"missing {BADGE}-128.png: run python3.13 "
                         "tools/build_badge.py first")
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path}: not a PNG")
    return struct.unpack(">II", head[16:24])


def badge_picture(lazy=False):
    width, height = badge_size()
    loading = ' loading="lazy"' if lazy else ''
    return (f'<picture><source type="image/webp" srcset="{BADGE}-128.webp 1x, '
            f'{BADGE}-256.webp 2x, {BADGE}-384.webp 3x"><img src="{BADGE}-128.png" '
            f'srcset="{BADGE}-128.png 1x, {BADGE}-256.png 2x, {BADGE}-384.png 3x" alt="{BADGE_ALT}" '
            f'width="{width}" height="{height}"{loading} decoding="async"></picture>')


def hero_seal_markup():
    return f'<div class="seal">{badge_picture()}</div>'


def footer_seal_markup():
    return (f'<a class="fseal" href="{CARFAX_URL}" target="_blank" rel="noopener">'
            f'{badge_picture(lazy=True)}</a>')

PHONE_ICO = (
    '<svg class="tb-ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M6.6 2.5a1.6 1.6 0 0 1 1.5 1l1 2.4a1.6 1.6 0 0 1-.4 1.8L7.4 8.9a11.6 11.6 0 0 0 '
    '5.7 5.7l1.2-1.3a1.6 1.6 0 0 1 1.8-.4l2.4 1a1.6 1.6 0 0 1 1 1.5v2.3a2.3 2.3 0 0 1-2.5 2.3 '
    'A18.4 18.4 0 0 1 2.2 5a2.3 2.3 0 0 1 2.3-2.5z"/></svg>'
)

TOPBAR = ('<div class="topbar"><a href="tel:+16783957459">'
          f'{PHONE_ICO}<span>(678) 395-7459</span></a></div>')

# The same handset without the .tb-ico class, for use inside buttons.
BTN_ICO = PHONE_ICO.replace(' class="tb-ico"', '')
CTA = f'{BTN_ICO}<span>Service My Car</span>'

# Two trust facts under every call button except the hero's, which has
# the checklist: the CARFAX rating with the years in business between
# laurels, and the warranty behind the site's shield-with-check. One laurel
# branch, mirrored in CSS for the right side. Kept on one line so the band
# rules, which match within a line, still see the band's closing div.
LAUREL = (
    '<svg class="laurel" viewBox="0 0 18 26" fill="currentColor" aria-hidden="true">'
    '<path d="M13.5 25.5Q-1.0 15.0 8.0 0.8" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
    '<ellipse cx="6.0" cy="21.3" rx="1.35" ry="3.60" transform="rotate(-85 6.0 21.3)"/>'
    '<ellipse cx="9.0" cy="18.5" rx="1.35" ry="3.60" transform="rotate(-1 9.0 18.5)"/>'
    '<ellipse cx="3.8" cy="17.1" rx="1.23" ry="3.15" transform="rotate(-71 3.8 17.1)"/>'
    '<ellipse cx="7.0" cy="15.3" rx="1.23" ry="3.15" transform="rotate(13 7.0 15.3)"/>'
    '<ellipse cx="3.0" cy="12.7" rx="1.11" ry="2.70" transform="rotate(-55 3.0 12.7)"/>'
    '<ellipse cx="6.0" cy="12.1" rx="1.11" ry="2.70" transform="rotate(29 6.0 12.1)"/>'
    '<ellipse cx="3.4" cy="8.5" rx="0.99" ry="2.25" transform="rotate(-38 3.4 8.5)"/>'
    '<ellipse cx="6.0" cy="8.7" rx="0.99" ry="2.25" transform="rotate(46 6.0 8.7)"/>'
    '<ellipse cx="4.9" cy="4.4" rx="0.87" ry="1.80" transform="rotate(-23 4.9 4.4)"/>'
    '<ellipse cx="6.9" cy="5.1" rx="0.87" ry="1.80" transform="rotate(61 6.9 5.1)"/>'
    '<ellipse cx="8.1" cy="0.5" rx="0.9" ry="2.2" transform="rotate(30 8.1 0.5)"/>'
    '</svg>'
)
SHIELD = ('<svg class="shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.6 7.5 9 4.3-1.4 7.5-4.5 7.5-9V6z"/>'
          '<path d="m9 12 2 2 4-4"/></svg>')
ASSURE = ('<div class="assure">'
          f'<span class="as">{LAUREL}<span class="as-t"><b>4.8-Star</b> on CARFAX<br>'
          f'<b>15+ Years</b> in business</span>{LAUREL}</span>'
          f'<span class="as">{SHIELD}<span class="as-t"><b>1-Year</b> service<br>'
          'warranties</span></span></div>')

CHECK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><path d="M5 12.5 10 17.5 19 7"/></svg>')

# The four trust facts the old strip carried, as a checklist under the
# hero button: the CARFAX rating, Google's review count, the years, the
# parts. The marque is read out of the strip being replaced, so a Porsche
# page keeps saying Porsche.
MARQUES = {"BMW": "BMW", "Mercedes": "Mercedes", "Audi": "Audi",
           "Porsche": "Porsche", "VW": "Volkswagen"}


def checks_list(marque=None):
    parts = f"Genuine {marque} parts and fluids" if marque else \
        "Genuine factory parts and fluids"
    items = ["4.8-star CARFAX rating", "180+ Google reviews",
             "15+ years in business", parts]
    rows = "".join(f'      <li>{CHECK_SVG}<span>{t}</span></li>\n' for t in items)
    return f'    <ul class="checks fu">\n{rows}    </ul>'


def hero_checklist(html):
    """Retire the four-cell trust strip in favour of a hero checklist.

    The strip sat between sections where it was scrolled past; the same
    four facts belong under the button, which is where the eye already
    is. Idempotent: a page that already has the list is left alone.
    """
    if 'class="checks' in html:
        return html
    marque = None
    strip = re.search(r'\n?<div class="trust">.*?\n</div>\n?', html, re.S)
    if strip:
        named = re.search(r'>([A-Za-z-]+)-Approved<', strip.group(0))
        if named:
            marque = MARQUES.get(named.group(1))
        html = html[:strip.start()] + "\n" + html[strip.end():]
    hero = re.search(r'<section class="hero"[^>]*>.*?</section>', html, re.S)
    if not hero:
        return html
    # The row is one line on generated pages and three on the 404; the
    # anchors inside it contain no divs, so the lazy match ends on its own
    # closing tag either way.
    acts = re.search(r'<div class="acts fu">.*?</div>', hero.group(0), re.S)
    if not acts:
        return html
    at = hero.start() + acts.end()
    return html[:at] + "\n" + checks_list(marque) + html[at:]


# An earlier pass put the shield on its own above the list, and one wrapped
# the pair as .proof, a class the homepage's About section already owned.
# Either is unwound before wrapping.
SEAL_RE = re.compile(r'\n[ \t]*<div class="seal">.*?</div>', re.S)
PROOF_RE = re.compile(
    r'<div class="(?:hero-proof|proof)">\s*<div class="seal">.*?</div>\s*(<ul class="checks.*?</ul>)\s*</div>', re.S)
FOOTER_SEAL_RE = re.compile(r'<a class="fseal".*?</a>', re.S)


def hero_seal(html):
    """Put the CARFAX shield beside the hero checklist, in one .hero-proof row.

    The 404 keeps its list alone; a page without a hero (the blog post) is
    left alone. Any badge already there is replaced rather than kept, so a
    rebuilt image's dimensions reach every page.
    """
    if '<div class="fu link-row">' in html:
        return html
    html = PROOF_RE.sub(lambda m: m.group(1), html)
    html = SEAL_RE.sub("", html)
    hero = re.search(r'<section class="hero[^"]*"[^>]*>.*?</section>', html, re.S)
    if not hero:
        return html
    checks = re.search(r'<ul class="checks[^>]*>.*?</ul>', hero.group(0), re.S)
    if not checks:
        return html
    start, end = hero.start() + checks.start(), hero.start() + checks.end()
    return (html[:start] + '<div class="hero-proof">\n    ' + hero_seal_markup() + '\n    '
            + html[start:end] + '\n    </div>' + html[end:])


# The generators write the hero headline as three stacked lines, white /
# white / red. The homepage sets the tier: two lines, the red one last,
# broken only from 900px (.h1-br) and wrapping naturally below. The first
# two lines merge and the third stays red. The words never change: the
# consistency checker compares the h1's text with the catalog name.
H1_RE = re.compile(
    r'<h1 class="fu">([^<]+)<br><span class="outline">([^<]+)</span>'
    r'(?:<br><span class="accent">([^<]+)</span>)?</h1>')

# Hand-chosen splits where the mechanical "A B / C" merge would leave a
# one-word red line under a long white one. Keyed by the three lines as
# written in the markup (entities included); the value is (white, red).
H1_SPLITS = {
    ("GERMAN CAR", "TUNE-UP", "SERVICE"): ("GERMAN CAR", "TUNE-UP SERVICE"),
    ("GERMAN CAR", "TRANSMISSION", "REPAIR"): ("GERMAN CAR", "TRANSMISSION REPAIR"),
}


# The space after the break is the phone's word space: below 900px the
# break is display:none and the two lines run together without it; from
# 900px a space at the start of a line collapses. index.html does the same.
H1_BR = '<br class="h1-br"> '
H1_BR_RE = re.compile(r'(<h1 class="fu">[^<]+<br class="h1-br">)(?=\S)')


def h1_markup(white, red=None):
    """The two-line hero headline; a red second line when there is one.

    An ampersand opening the red line stays with its word ("& SERVICE"),
    or a tablet wraps the line as "REPAIR &" / "SERVICE".
    """
    tail = f'<span class="accent">{red.replace("&amp; ", "&amp;&nbsp;")}</span>' if red else ""
    return f'<h1 class="fu">{white}{H1_BR}{tail}</h1>'


def hero_h1(html):
    """Merge the three-line hero headline into the homepage's two-line form.

    The 404's two-line "WRONG / TURN" keeps both words white and takes the
    responsive break. A page already in the two-line form (the landing
    pages, or a page this has run on) has no .outline span and is left
    alone, so the pass is idempotent.
    """
    def merge(m):
        a, b, c = m.groups()
        if c is None:
            return f'<h1 class="fu">{a}{H1_BR}{b}</h1>'
        white, red = H1_SPLITS.get((a, b, c), (f"{a} {b}", c))
        return h1_markup(white, red)
    html = H1_RE.sub(merge, html, count=1)
    return H1_BR_RE.sub(r'\1 ', html, count=1)


# The service pages set the "Why German Performance" label and title inside
# the left column of the .two grid, where an eleven-letter word in the wide
# display face is wider than the 400-568px column from 960px and breaks
# mid-word. The landing pages put that header in a centred .sh above the
# grid; every page now does. Figure-first and .sh-first blocks don't match.
TWO_HEAD_RE = re.compile(
    r'^([ \t]*)<div class="two fu">\n[ \t]*<div>\n'
    r'[ \t]*<div class="sl">([^\n]*?)</div>\n[ \t]*(<h2>[^\n]*?</h2>)\n', re.M)


def two_heading(html):
    """Lift the .two column's label and title into a .sh above the grid."""
    def lift(m):
        indent, label, h2 = m.groups()
        return (f'{indent}<div class="sh fu"><div class="sl">{label}</div>{h2}</div>\n'
                f'{indent}<div class="two fu">\n{indent}  <div>\n')
    return TWO_HEAD_RE.sub(lift, html)


def footer_seal(html):
    """Put the shield, linked to the CARFAX page, under the footer tagline."""
    html = FOOTER_SEAL_RE.sub("", html)
    return re.sub(r'(<div class="ftag">(?:(?!</div>).)*</div>)',
                  lambda m: m.group(1) + footer_seal_markup(), html, count=1, flags=re.S)


PRIVACY_LINK = ' · <a href="/privacy-policy">Privacy Policy</a>'
FCOPY_RE = re.compile(r'(<div class="fcopy">© \d{4} German Performance — Snellville, GA 30078)'
                      r'(?:' + re.escape(PRIVACY_LINK) + r')?(</div>)')


def footer_privacy(html):
    """Link the privacy policy from the copyright line of every page.

    Google's advertising policies require the policy to be reachable from
    every page that carries its tags. The copyright line is the one footer
    element that is byte-identical across the site and that no other tool
    rewrites, so the link survives fix_footer_links.py regenerating the
    Services column. Any earlier link is stripped and re-added, so a copy
    change here reaches every page.
    """
    return FCOPY_RE.sub(lambda m: m.group(1) + PRIVACY_LINK + m.group(2), html, count=1)


ASSURE_RE = r'[ \t]*<div class="assure">(?:(?!</div>).)*?</div>\n?'
CTA_COL_RE = (r'<div class="cta-col">\s*((?:<div class="acts">(?:(?!</div>).)*?</div>)'
              r'|(?:<a [^>]*>(?:(?!</a>).)*?</a>))\s*</div>')


def indent_block(block, indent):
    """Re-indent a div whose inner lines are one level deeper than its tags."""
    lines = [line.strip() for line in block.split("\n")]
    return "\n".join(indent + ("  " if 0 < i < len(lines) - 1 else "") + line
                     for i, line in enumerate(lines))


def trust_badges(html):
    """Put the two trust badges under every call button except the hero's.

    The button row and the badge row share a `.cta-col` so the button can
    be as wide as the badges. Any earlier row or column is stripped first
    and the column rebuilt, so the pass is idempotent and a copy change in
    ASSURE reaches every page. The hero's row is never matched because
    each pattern is scoped to its own container.
    """
    html = re.sub(ASSURE_RE, '', html, flags=re.S)
    html = re.sub(CTA_COL_RE, r'\1', html, flags=re.S)
    # Closing section: the pair of buttons, then the badges.
    html = re.sub(
        r'(<section class="cta-final">(?:(?!</section>).)*?)'
        r'^([ \t]*)(<div class="acts">(?:(?!</div>).)*?</div>)\n',
        lambda m: (m.group(1) + m.group(2) + '<div class="cta-col">\n'
                   + indent_block(m.group(3), m.group(2) + '  ') + '\n'
                   + m.group(2) + '  ' + ASSURE + '\n'
                   + m.group(2) + '</div>\n'),
        html, flags=re.S | re.M)
    # Red band: one line, the button then the badges before the band's
    # closing div.
    html = re.sub(
        r'^(<div class="cta-band fu">[^\n]*?)(<a href="tel:\+16783957459" class="bw">'
        r'(?:(?!</a>).)*?</a>)(</div>)$',
        lambda m: m.group(1) + '<div class="cta-col">' + m.group(2) + ASSURE + '</div>' + m.group(3),
        html, flags=re.M)
    # The blog post: its hours line under the button gave way to the badges.
    html = re.sub(
        r'^([ \t]*)(<a href="tel:\+16783957459" class="btn-primary">(?:(?!</a>).)*?</a>)\n'
        r'(?:[ \t]*<div class="cta-sub">[^<]*</div>\n)?',
        lambda m: (m.group(1) + '<div class="cta-col">\n'
                   + m.group(1) + '  ' + m.group(2) + '\n'
                   + m.group(1) + '  ' + ASSURE + '\n'
                   + m.group(1) + '</div>\n'),
        html, flags=re.S | re.M)
    return html

# The homepage links down its own document; every other page links into it
# or to the info pages. Panel links are page files on both.
HOME_HREFS = {
    "index.html#reviews": "#reviews",
    "index.html#services": "#services",
    "about.html": "#story",
    "index.html#faq": "#faq",
    "contact.html": "#contact",
}

CHEVRON = ('<svg class="nav-chev" viewBox="0 0 10 10" fill="none" aria-hidden="true">'
           '<path d="M2 3.5 5 6.5 8 3.5" stroke="currentColor" stroke-width="1.5" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def href(target, home):
    """The homepage links down its own document; every other page links to
    the page's clean address (tools/urls.py)."""
    return HOME_HREFS[target] if home and target in HOME_HREFS else urls.href_for(target)


def service_columns(home, indent):
    """One <li class="svc-group"> per catalog group: the hub link as its
    heading, then one link per page. Each column is a single line, so no
    closing tag ever lands at column 0 -- the generators grab the phone menu
    from a donor page with a pattern that ends at a newline and </div>."""
    rows = []
    for name, entries in GROUPS:
        head = (f'<span class="svc-group-name">'
                f'<a href="{href(HUBS[name], home)}">{name}</a></span>')
        links = "".join(f'<a href="{href(h, home)}">{label}</a>'
                        for h, label in entries)
        rows.append(f"{indent}<li class=\"svc-group\">{head}{links}</li>")
    return "\n".join(rows)


def nav_markup(home=False):
    """Phone bar, nav and phone menu.

    Services is a disclosure: on a desktop a button opens a full-width panel
    of the catalog under the bar; on a phone a <details> inside the menu.
    Only details, summary, ul, li, span and a go inside #mobile-menu: the
    nav rule below and every generator's donor grab end the menu at its
    first </div>. The homepage's button carries the section it stands for,
    so the active-link spy can light it.
    """
    h = lambda target: href(target, home)  # noqa: E731
    spy = ' data-section="#services"' if home else ""
    return f'''{TOPBAR}
<nav>
  <a href="/" class="nav-logo">{LOGO_NAV}</a>
  <ul class="nav-links">
    <li><a href="{h('index.html#reviews')}">Reviews</a></li>
    <li class="nav-dd">
      <button type="button" class="nav-dd-btn" aria-expanded="false" aria-controls="nav-services"{spy}>Services{CHEVRON}</button>
      <div class="nav-panel" id="nav-services">
        <ul class="nav-panel-grid">
{service_columns(home, "          ")}
        </ul>
      </div>
    </li>
    <li><a href="{h('guides.html')}">Guides</a></li>
    <li><a href="{h('about.html')}">About</a></li>
    <li><a href="{h('index.html#faq')}">FAQ</a></li>
    <li><a href="{h('contact.html')}">Contact</a></li>
  </ul>
  <div class="nav-right">
    <a href="tel:+16783957459" class="nav-cta">{CTA}</a>
    <button id="hamburger" onclick="toggleMenu()" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
  </div>
</nav>
<div id="mobile-menu">
  <a href="{h('index.html#reviews')}" onclick="closeMenu()">Reviews</a>
  <details class="mm-dd">
    <summary>Services{CHEVRON}</summary>
    <ul class="mm-groups">
{service_columns(home, "      ")}
    </ul>
  </details>
  <a href="{h('guides.html')}" onclick="closeMenu()">Guides</a>
  <a href="{h('about.html')}" onclick="closeMenu()">About</a>
  <a href="{h('index.html#faq')}" onclick="closeMenu()">FAQ</a>
  <a href="{h('contact.html')}" onclick="closeMenu()">Contact</a>
  <a href="tel:+16783957459" class="mcta" onclick="closeMenu()">{CTA}</a>
</div>'''


NAV = nav_markup(home=False)
# The phone bar (if present), the nav and the phone menu (if present). The
# menu match is lazy to the first </div>, which is why nothing inside the
# menu may be a div.
NAV_RE = re.compile(r'(?:<div class="topbar">.*?</div>\s*)?<nav>.*?</nav>'
                    r'(?:\s*<div id="mobile-menu">.*?</div>)?', re.S)

# The footer's two fixed columns, the same on every page. The Services
# column and the link row are the page's own (tools/fix_footer_links.py).
MAPS_URL = place.attr(place.DIRECTIONS)
FOOTER_CONTACT = ('<div class="fc"><div class="fct">Contact</div>'
                  '<a href="tel:+16783957459">(678) 395-7459</a>'
                  '<p>2144 Parkwood Rd NW</p><p>Snellville, GA 30078</p>'
                  f'<a href="{MAPS_URL}" target="_blank" rel="noopener">Get directions</a>'
                  '<p>Mon–Fri: 9:30 AM–6 PM</p></div>')
FOOTER_NAVIGATE = ('<div class="fc"><div class="fct">Navigate</div>'
                   '<a href="/">Home</a><a href="/about">About</a>'
                   '<a href="/#reviews">Reviews</a><a href="/#faq">FAQ</a>'
                   '<a href="/contact">Contact</a>'
                   '<a href="/guides">Repair Guides</a></div>')
FOOTER_CONTACT_RE = re.compile(r'<div class="fc"><div class="fct">Contact</div>.*?</div>', re.S)
FOOTER_NAVIGATE_RE = re.compile(r'<div class="fc"><div class="fct">Navigate</div>.*?</div>', re.S)
FOOTER_YEAR_RE = re.compile(r'(<div class="fcopy">© )\d{4}( German Performance)')


def footer_chrome(html, home=False):
    """One Contact column, one Navigate column and this year's copyright
    on every page. The pages no generator builds had kept whatever footer
    they were uploaded with -- a 2025 date, no directions link -- beside
    generated pages that had moved on. The homepage keeps its own Navigate
    column, which links down its own document."""
    html = FOOTER_CONTACT_RE.sub(lambda _: FOOTER_CONTACT, html, count=1)
    if not home:
        html = FOOTER_NAVIGATE_RE.sub(lambda _: FOOTER_NAVIGATE, html, count=1)
    year = datetime.date.today().year
    return FOOTER_YEAR_RE.sub(lambda m: f"{m.group(1)}{year}{m.group(2)}", html, count=1)


FOOTER_COLUMNS = f'''  <div class="ft">
    <div><div class="fb">{LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div></div>
    {FOOTER_CONTACT}
    <div class="fc"><div class="fct">Services</div><a href="/bmw-repair-snellville-ga">BMW Repair</a><a href="/mercedes-repair-snellville-ga">Mercedes-Benz Repair</a><a href="/audi-repair-snellville-ga">Audi Repair</a><a href="/porsche-repair-snellville-ga">Porsche Repair</a><a href="/volkswagen-repair-snellville-ga">Volkswagen Repair</a></div>
    {FOOTER_NAVIGATE}
  </div>'''

# (pattern, replacement) pairs applied in order to every page.
RULES = [
    # -- head: fonts from this host, base sheet before page sheet, one
    #    script for every page -----------------------------------------------
    (GOOGLE_FONTS_RE, fonts_markup()),
    (r'<link rel="preload" href="assets/fonts/[^"]*" as="font"[^>]*>\n', ''),
    # A page still linking the sheets one by one (either legacy order, with
    # or without fonts.css) gets the inline critical block and its bundle.
    (r'(?:<link rel="stylesheet" href="assets/css/fonts\.css\?v=\d+">\n)?'
     r'<link rel="stylesheet" href="assets/css/tokens\.css\?v=\d+">\n'
     r'(?:<link rel="stylesheet" href="assets/css/werkstatt\.css\?v=\d+">\n'
     r'<link rel="stylesheet" href="assets/css/(site|post|home)\.css\?v=\d+">'
     r'|<link rel="stylesheet" href="assets/css/(site|post|home)\.css\?v=\d+">\n'
     r'<link rel="stylesheet" href="assets/css/werkstatt\.css\?v=\d+">)',
     lambda m: build_css.stylesheets(m.group(1) or m.group(2), VERSION)),
    # The critical block is regenerated from fonts.css and tokens.css on
    # every pass, so an edit to either reaches every page.
    (build_css.CRITICAL_RE.pattern, lambda m: build_css.critical_markup()),
    # Every stylesheet and script carries the current cache-buster, whatever
    # order the links are in. Bump VERSION whenever a sheet changes, or a
    # browser that saw the old sheet keeps it against the new markup.
    (r'(assets/(?:css|js)/[a-z-]+\.(?:css|js))\?v=\d+', f'\\1?v={VERSION}'),
    (r'<script defer src="assets/js/site\.js\?v=\d+"></script>',
     f'<script defer src="assets/js/site.js?v={VERSION}"></script>'),
    (r'<script defer src="assets/js/analytics\.js\?v=\d+"></script>',
     f'<script defer src="assets/js/analytics.js?v={VERSION}"></script>'),

    # -- phone bar, nav and mobile menu ---------------------------------------
    (NAV_RE.pattern, NAV),

    # -- hero -----------------------------------------------------------------
    (r'<div class="hgrid"></div>', ''),
    # The checklist under the hero carries the rating; the eyebrow need not.
    # The hub generator writes a space before the span, the service one none.
    (r' &nbsp;·&nbsp; ?<span class="eyebrow-highlight">4\.5★ Rated</span>', ''),
    # Eyebrow text goes in a span so its two rules stay centred when it wraps.
    (r'<div class="eyebrow( fu)?">(?!<span>)(.*?)</div>', r'<div class="eyebrow\1"><span>\2</span></div>'),
    (r'<section class="hero" style="min-height:60vh;padding-top:150px">', '<section class="hero">'),

    # -- review copy: the CARFAX rating leads, Google keeps the count -------
    (r'<span>4\.5-star Google rating</span>', '<span>4.8-star CARFAX rating</span>'),
    (r'<span>Top-rated CARFAX shop</span>', '<span>180+ Google reviews</span>'),
    # -- the parts line says Mercedes, as the hub, eyebrow and footer do: the
    #    long form is the one hero fact that wraps beside the shield at 360px --
    (r'<span>Genuine Mercedes-Benz parts and fluids</span>', '<span>Genuine Mercedes parts and fluids</span>'),
    (r'<b>4\.5-Star</b> rated by<br><b>180\+</b> customers',
     '<b>4.8-Star</b> on CARFAX<br><b>15+ Years</b> in business'),
    (r'CARFAX Top-Rated and Google 4\.5★', 'CARFAX Top-Rated at 4.8★, 4.5★ on Google'),
    # -- the legacy pages' CTA button: directions to the listing, not to the
    #    building Google resolves the bare street address to (tools/place.py) --
    (r'href="https://maps\.google\.com/\?q=2144\+Parkwood\+Rd\+NW\+Snellville\+GA\+30078"',
     f'href="{MAPS_URL}"'),

    # -- trust strip: four cells, not five ---------------------------------
    (r'\s*<div class="ti"><div class="tv">Same</div><div class="tl">Week Appointments<br>Available</div></div>', ''),

    # -- inline styles become classes -------------------------------------
    (r'<section style="background:var\(--black\);padding:80px 60px;text-align:center">', '<section class="cta-final">'),
    (r'<section style="background:var\(--(?:carbon|black)\)">', '<section>'),
    (r'<span style="color:var\(--red\)">', '<span class="accent">'),
    (r'<span style="color:var\(--silver\)">', '<span class="crumb-here">'),
    (r'<strong style="color:var\(--white\)">', '<strong>'),
    (r'<div class="fu"><div class="sl">', '<div class="sh fu"><div class="sl">'),
    (r'<div style="max-width:820px;margin:0 auto">', '<div class="narrow">'),
    (r'<h2 style="margin-bottom:20px">', '<h2>'),
    (r'<h2 style="display:inline-block; border:none; padding:0;">', '<h2>'),
    (r'<p class="sd" style="margin:0 auto 44px;text-align:center;max-width:480px">', '<p class="sd">'),
    (r'<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">', '<div class="acts">'),
    (r'<div class="sl" style="justify-content:center">', '<div class="sl">'),
    (r'<p class="sd" style="margin-bottom:0">', '<p class="sd">'),
    (r'<div class="fu" style="margin-top:44px">', '<div class="sub-block fu">'),
    (r'<div class="rel-grid" style="margin-top:20px">', '<div class="rel-grid">'),
    (r'<p class="sd fu" style="margin-top:36px">', '<p class="sd fu note">'),
    (r'<div class="flinks fu" style="margin-top:28px">', '<div class="flinks fu">'),
    (r'<div class="fu" style="display:flex;flex-wrap:wrap;gap:18px 32px;margin-top:36px">', '<div class="fu link-row">'),

    # -- FAQ: native disclosure -------------------------------------------
    (r'<div class="fi fu"><button class="fq" onclick="toggleFaq\(this\)">(.*?)<span class="ficon">\+</span></button><div class="fa">(.*?)</div></div>',
     r'<details class="fi fu" name="faq"><summary class="fq">\1<span class="ficon" aria-hidden="true"></span></summary><div class="fa">\2</div></details>'),

    # Four generated pages plus about and contact shipped this anchor with
    # no class at all, so the band's CTA rendered as a bare link.
    (r'(<div class="cta-band fu">[^\n]*?)<a href="tel:\+16783957459">',
     r'\1<a href="tel:+16783957459" class="bw">'),

    # -- one wording on every button --------------------------------------
    # The owner's: the phone glyph, then the job. The href never changes,
    # so the number still dials and the call tracking still resolves.
    (r'(<a href="tel:\+16783957459"[^>]*class="(?:bp|bw|btn-primary)"[^>]*>)'
     r'(?:(?!</a>).)*?(</a>)', r'\1' + CTA + r'\2'),

    # -- red band: a red button on a red band is invisible ----------------
    # The band is written on one line, so stay on that line; a dot-all
    # match would reach the next .bp on the page, in the closing section.
    (r'(<div class="cta-band fu">[^\n]*?)class="bp"', r'\1class="bw"'),
    (r'(<section class="cta-final">(?:(?!</section>).)*?)class="bw"', r'\1class="bp"'),

    # -- footer --------------------------------------------------------------
    (r'<div class="fb">GERMAN <span>PERFORMANCE</span></div><div class="ftag">BMW · Mercedes · Audi · Porsche · VW</div>',
     f'<div class="fb">{LOGO_FOOT}</div><div class="ftag">German auto specialists<br>BMW · Mercedes · Audi · Porsche · VW</div>'),
    (r'(\s*<div class="fcopy">.*?</div>)(\s*<div class="flinks">.*?</div>)', r'\2\1'),
    # The blog post carried its own footer classes; give it the shared one.
    (r'<footer>\s*<div class="footer-copy">(.*?)</div>\s*<div class="footer-links">(.*?)</div>\s*</footer>',
     '<footer>\n' + FOOTER_COLUMNS + r'\n  <div class="flinks">\2</div>' + '\n' + r'  <div class="fcopy">\1</div>' + '\n</footer>'),

    # -- the fixed bottom call bar is gone ---------------------------------
    (r'\s*<div class="call-bar">.*?</div>', ''),
]

# The 404 page listed its shortcuts as eight outlined buttons in a row.
LINK_ROW_BUTTONS = re.compile(r'(<div class="fu link-row">)(.*?)(</div>)', re.S)


def transform(html):
    # Clean addresses first, so every rule below sees one form of a link,
    # and again last, so nothing a rule writes goes out with ".html" on it.
    html = urls.clean_links(html)
    for pattern, replacement in RULES:
        html = re.sub(pattern, replacement, html, flags=re.S)
    html = LINK_ROW_BUTTONS.sub(
        lambda m: m.group(1) + m.group(2).replace(' class="bg"', '') + m.group(3), html)
    html = hero_checklist(html)
    html = hero_seal(html)
    html = hero_h1(html)
    html = two_heading(html)
    html = trust_badges(html)
    html = footer_seal(html)
    html = footer_privacy(html)
    html = footer_chrome(html)
    # The blog post had no site.js; every page needs the menu script.
    if 'assets/js/site.js' not in html:
        html = html.replace(
            f'<script defer src="assets/js/analytics.js?v={VERSION}"></script>',
            f'<script defer src="assets/js/site.js?v={VERSION}"></script>\n'
            f'  <script defer src="assets/js/analytics.js?v={VERSION}"></script>')
    return urls.clean_links(html)


def main():
    pages = [f for f in site_pages(os.listdir(REPO_ROOT)) if f != "index.html"]
    changed = 0
    for name in pages:
        path = os.path.join(REPO_ROOT, name)
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        updated = transform(original)
        if updated != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(updated)
            changed += 1
    print(f"{changed} of {len(pages)} pages updated")

    # The homepage is hand-built, but its chrome must match every other
    # page's: apply the nav rule alone, with in-page anchors, and never the
    # version stamps (those refs are hand-edited).
    index = os.path.join(REPO_ROOT, "index.html")
    with open(index, encoding="utf-8") as fh:
        original = fh.read()
    updated, n = NAV_RE.subn(lambda m: nav_markup(home=True), original, count=1)
    if n != 1:
        print("index.html: nav block not found")
        return 1
    updated = footer_chrome(updated, home=True)
    updated = urls.clean_links(updated)
    # ... and its inline critical block, which is build output like the nav.
    updated, n = build_css.CRITICAL_RE.subn(lambda m: build_css.critical_markup(), updated, count=1)
    if n != 1:
        print("index.html: <style id=\"critical\"> block not found")
        return 1
    if updated != original:
        with open(index, "w", encoding="utf-8") as fh:
            fh.write(updated)
    print("index.html chrome " + ("updated" if updated != original else "current"))

    leftovers = []
    for name in pages:
        with open(os.path.join(REPO_ROOT, name), encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                for match in re.finditer(r'style="[^"]*"', line):
                    if match.group(0).startswith('style="--'):
                        continue
                    leftovers.append((name, lineno, match.group(0)))
    if leftovers:
        print(f"\n{len(leftovers)} inline style(s) remain:")
        for row in leftovers[:20]:
            print("  %s:%d  %s" % row)
        return 1
    print("No inline styles remain outside index.html.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
