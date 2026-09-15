#!/usr/bin/env node
/* End-to-end check for assets/js/analytics.js.
 *
 * The site has no JavaScript test harness, and the tracking file is the
 * one script whose failure is invisible: a broken swap or a missing event
 * costs nothing on the page and everything in the Ads account. So this
 * drives a real Chromium against the real pages and asserts what the
 * file promises:
 *
 *   1. A visitor from an ad (gclid on the URL) gets the Google library at
 *      once, and when Google hands over a forwarding number every tel:
 *      href and every visible copy of the shop's number is swapped --
 *      but the JSON-LD is not.
 *   2. An organic visitor keeps the shop's number and gets the library
 *      only after the page is idle.
 *   3. A tap on a phone link sends generate_lead to GA4 with the right
 *      placement, and the click conversion to Google Ads.
 *   4. A tap on Directions sends get_directions.
 *
 * Google's ids are placeholders in the repo, so the script serves a copy
 * of analytics.js with test ids, and answers the gtag/js request with a
 * stub that behaves like Google does for the number swap: it calls the
 * phone_conversion_callback only when the visit carries a gclid.
 *
 * Run from the repo root, with playwright-core resolvable:
 *   NODE_PATH=/path/to/node_modules node tools/check_tracking_e2e.cjs
 * Exit code 0 = every assertion held, 1 = at least one failed.
 */

'use strict';

const fs = require('fs');
const http = require('http');
const path = require('path');
const { chromium } = require('playwright-core');

const REPO_ROOT = path.resolve(__dirname, '..');
const PAGE = 'bmw-repair';
const SHOP_TEL = 'tel:+16783957459';
const SHOP_DISPLAY = '(678) 395-7459';
const FORWARD_DISPLAY = '(770) 555-0100';
const FORWARD_TEL = 'tel:+17705550100';
const TEST_IDS = {
  MEASUREMENT_ID: 'G-TEST123456',
  ADS_ID: 'AW-123456789',
  CALL_LABEL: 'CALLLABEL01',
  CLICK_LABEL: 'CLICKLABEL1'
};

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

/* The real file with the four placeholders replaced, nothing else. */
function analyticsWithTestIds() {
  const source = fs.readFileSync(path.join(REPO_ROOT, 'assets/js/analytics.js'), 'utf8');
  return Object.entries(TEST_IDS).reduce(
    (js, [name, value]) => js.replace(new RegExp(`var ${name} = '[^']*'`), `var ${name} = '${value}'`),
    source);
}

/* What Google's library does for the swap, and nothing more. */
const GTAG_STUB = `
(function () {
  window.__gtagStubLoaded = true;
  if (!/[?&]gclid=/.test(location.search)) return;
  (window.dataLayer || []).forEach(function (call) {
    var opts = call[2];
    if (call[0] === 'config' && opts && typeof opts.phone_conversion_callback === 'function') {
      opts.phone_conversion_callback('${FORWARD_DISPLAY}', '+1 770-555-0100');
    }
  });
})();`;

/* The file behind a request, resolved the way GitHub Pages does it: "/"
   is index.html and an extensionless path is that page's .html file. */
function fileFor(url) {
  const pathname = decodeURIComponent(url.split('?')[0]);
  if (pathname === '/') return path.join(REPO_ROOT, 'index.html');
  const file = path.join(REPO_ROOT, pathname);
  return path.extname(file) ? file : `${file}.html`;
}

function serve() {
  const server = http.createServer((req, res) => {
    const file = fileFor(req.url);
    if (!file.startsWith(REPO_ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404); res.end(); return;
    }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

const failures = [];
function check(condition, message) {
  if (!condition) failures.push(message);
  console.log(`  ${condition ? 'ok  ' : 'FAIL'}  ${message}`);
}

async function openPage(browser, url) {
  const page = await browser.newPage();
  /* Routes match last-registered first: the blanket abort goes on first so
     nothing leaves the machine, then the two answers that override it. */
  await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, (route) => route.abort());
  await page.route('**/assets/js/analytics.js*', (route) =>
    route.fulfill({ contentType: 'text/javascript', body: analyticsWithTestIds() }));
  await page.route('**/gtag/js*', (route) =>
    route.fulfill({ contentType: 'text/javascript', body: GTAG_STUB }));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__gtagStubLoaded === true, null, { timeout: 8000 });
  /* Stop tel: and _blank navigations so the click is observed, not followed.
     Registered after analytics.js, so it runs after the tracking listener. */
  await page.evaluate(() => document.addEventListener('click', (e) => e.preventDefault(), true));
  return page;
}

const snapshot = (page) => page.evaluate(() => ({
  hrefs: Array.from(document.querySelectorAll('a[href^="tel:"]')).map((a) => a.getAttribute('href')),
  topbar: document.querySelector('.topbar').textContent.trim(),
  footerTel: document.querySelector('footer a[href^="tel:"]').textContent.trim(),
  jsonLd: document.querySelector('script[type="application/ld+json"]').textContent,
  gtagStart: performance.getEntriesByType('resource').find((e) => e.name.includes('gtag/js')).startTime,
  dclStart: performance.getEntriesByType('navigation')[0].domContentLoadedEventStart,
  calls: window.dataLayer.map((a) => Array.from(a))
}));

const events = (calls, name) => calls.filter((c) => c[0] === 'event' && c[1] === name).map((c) => c[2]);

async function clickAndRead(page, selector) {
  const before = (await snapshot(page)).calls.length;
  await page.click(selector);
  const { calls } = await snapshot(page);
  return calls.slice(before);
}

async function adVisit(browser, origin) {
  console.log(`\nAd visitor: ${PAGE}?gclid=TEST`);
  const page = await openPage(browser, `${origin}/${PAGE}?gclid=TEST`);
  const s = await snapshot(page);
  check(s.hrefs.length >= 5, `${s.hrefs.length} tel: links found`);
  check(s.hrefs.every((h) => h === FORWARD_TEL), 'every tel: href is the forwarding number');
  check(s.topbar.includes(FORWARD_DISPLAY), 'red bar shows the forwarding number');
  check(s.footerTel.includes(FORWARD_DISPLAY), 'footer shows the forwarding number');
  check(s.jsonLd.includes('+1-678-395-7459'), 'JSON-LD still carries the shop number');
  check(s.gtagStart < s.dclStart, 'gtag requested before DOMContentLoaded (not deferred to idle)');
  const configs = s.calls.filter((c) => c[0] === 'config').map((c) => c[1]);
  check(configs.includes(TEST_IDS.MEASUREMENT_ID), 'GA4 configured');
  check(configs.includes(TEST_IDS.ADS_ID), 'Google Ads configured');
  check(configs.includes(`${TEST_IDS.ADS_ID}/${TEST_IDS.CALL_LABEL}`), 'call conversion configured');

  const hero = await clickAndRead(page, '.hero a.bp');
  const lead = events(hero, 'generate_lead')[0];
  check(lead && lead.placement === 'hero', 'hero tap -> generate_lead placement=hero');
  check(lead && lead.forwarded === true && lead.phone === '+16783957459',
        'hero tap reports the shop number with forwarded=true');
  check(events(hero, 'conversion').some((e) => e.send_to === `${TEST_IDS.ADS_ID}/${TEST_IDS.CLICK_LABEL}`),
        'hero tap -> Google Ads click conversion');

  const closing = await clickAndRead(page, '.cta-final a.bp');
  check((events(closing, 'generate_lead')[0] || {}).placement === 'cta_final',
        'closing-section tap -> placement=cta_final');
  const band = await clickAndRead(page, '.cta-band a.bw');
  check((events(band, 'generate_lead')[0] || {}).placement === 'cta_band',
        'red band tap -> placement=cta_band');
  const directions = await clickAndRead(page, '.cta-final a[href*="google.com/maps"]');
  check(events(directions, 'get_directions').length === 1, 'directions tap -> get_directions');
  await page.close();
}

async function organicVisit(browser, origin) {
  console.log(`\nOrganic visitor: ${PAGE}`);
  const page = await openPage(browser, `${origin}/${PAGE}`);
  const s = await snapshot(page);
  check(s.hrefs.every((h) => h === SHOP_TEL), 'every tel: href is the shop number');
  check(s.topbar.includes(SHOP_DISPLAY), 'red bar shows the shop number');
  check(s.gtagStart > s.dclStart, 'gtag requested after DOMContentLoaded (idle load)');
  const topbar = await clickAndRead(page, '.topbar a');
  const lead = events(topbar, 'generate_lead')[0];
  check(lead && lead.placement === 'top_bar' && lead.forwarded === false,
        'red bar tap -> placement=top_bar, forwarded=false');
  check(lead && lead.page_type === 'hub', 'page_type read from <body>');
  await page.close();
}

async function main() {
  const server = await serve();
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  try {
    await adVisit(browser, origin);
    await organicVisit(browser, origin);
  } finally {
    await browser.close();
    server.close();
  }
  console.log(failures.length ? `\n${failures.length} assertion(s) failed` : '\nTracking behaves as documented.');
  return failures.length ? 1 : 0;
}

main().then((code) => process.exit(code), (err) => { console.error(err); process.exit(1); });
