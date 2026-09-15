#!/usr/bin/env python3
"""Verify the service-page hero H1 renders on two lines at every width.

The framework promises "{service} in" over "Snellville, GA" (see
tools/build_landing_pages.py and the .hero-svc rule in assets/css/site.css).
The CSS sizes the first line from an estimate; this renders each framework
page in Playwright's chrome-headless-shell at phone, tablet and desktop
widths and counts the line boxes the first line actually occupies.

Never the Chrome.app binary: an orphaned headless Chrome once blocked the
owner's own browser for two days. The shell is driven directly with a hard
timeout; if it is not installed the check is skipped, not failed.

Run from the repo root:  python3 tools/check_hero_lines.py
Exit code 0 = two lines everywhere (or skipped), 1 = a first line wrapped.
"""

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

from service_catalog import PAGES  # noqa: E402

REPO_ROOT = os.path.dirname(TOOLS)
SHELL_GLOB = os.path.expanduser(
    "~/Library/Caches/ms-playwright/chromium_headless_shell-*/"
    "chrome-headless-shell-mac-arm64/chrome-headless-shell")
WIDTHS = (320, 375, 390, 640, 768, 1024, 1440)
TIMEOUT = 90

# Writes the number of line boxes the H1's first text run occupies, and the
# H1's rendered size, into the title once fonts have loaded.
PROBE = """<script>
document.fonts.ready.then(function () {
  var h1 = document.querySelector('.hero-svc h1');
  var range = document.createRange();
  range.selectNodeContents(h1.firstChild);
  document.title = JSON.stringify({
    lines: range.getClientRects().length,
    px: Math.round(parseFloat(getComputedStyle(h1).fontSize)),
  });
});
</script>"""


def shell_binary():
    found = sorted(glob.glob(SHELL_GLOB))
    return found[-1] if found else None


def probe_copy(slug, folder):
    """A copy of the page that resolves assets from the repo and reports."""
    with open(os.path.join(REPO_ROOT, slug), encoding="utf-8") as fh:
        html = fh.read()
    base = f'<base href="file://{REPO_ROOT}/">'
    html = html.replace("<head>", f"<head>{base}", 1).replace("</body>", PROBE + "</body>", 1)
    path = os.path.join(folder, slug)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path


def measure(binary, path, width):
    cmd = [binary, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--virtual-time-budget=6000", f"--window-size={width},1200",
           "--dump-dom", f"file://{path}"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT).stdout
    m = re.search(r"<title>(\{.*?\})</title>", out, re.S)
    return json.loads(m.group(1).replace("&quot;", '"')) if m else None


# Every page on the two-line hero: the landing pages and the five brand hubs.
# Every catalog page carries the two-line H1 since 2026-09-15: the seven
# general pages and the five hubs.
SLUGS = tuple(p.slug for p in PAGES)


def check(binary):
    """Yield (slug, width, reason) for every render that broke the promise."""
    with tempfile.TemporaryDirectory() as folder:
        for slug in SLUGS:
            path = probe_copy(slug, folder)
            for width in WIDTHS:
                result = measure(binary, path, width)
                if result is None:
                    yield slug, width, "no measurement (fonts or script failed)"
                elif result["lines"] != 1:
                    yield slug, width, f'first line wraps ({result["lines"]} line boxes) at {result["px"]}px'


def main():
    binary = shell_binary()
    if not binary:
        print("SKIP: chrome-headless-shell not installed; hero line check not run.")
        return 0
    broken = list(check(binary))
    if not broken:
        print(f"OK: hero H1 holds two lines on {len(SLUGS)} page(s) at "
              f"{', '.join(str(w) for w in WIDTHS)}px.")
        return 0
    print(f"WRAPPED: {len(broken)} render(s) broke the two-line hero\n")
    for slug, width, reason in broken:
        print(f"  {slug} @ {width}px: {reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
