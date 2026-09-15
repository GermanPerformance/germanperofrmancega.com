/* ==========================================================================
   German Performance -- measurement

   The only conversion on this site is a phone call. There is no form, no
   cart and no signup, so "a call was started" is the single number that
   says whether any of the SEO, design or advertising work did anything.

   Two destinations, one file:

     GA4 (MEASUREMENT_ID)  -- every phone tap as generate_lead, with where
                              on the page it happened; directions taps.
     Google Ads (ADS_ID)   -- the same tap as a secondary "phone number
                              click" conversion, and, for visitors who
                              arrived from an ad, a real call: Google
                              swaps the shop's number for a forwarding
                              number and counts the calls that connect.
                              That call action is the primary conversion;
                              the click is observation only, or the same
                              call would count twice.

   Three decisions worth knowing about:

   1. The gtag stub is defined synchronously but the library is fetched on
      idle. gtag() only pushes onto dataLayer; the library drains that
      queue whenever it arrives. So events fired in the first second are
      not lost, and ~50KB of third-party JavaScript stays off the critical
      path -- which matters here, because getting the homepage from 1.59MB
      down to 44.5KB was most of Phase 2. The one exception is a visitor
      who arrived from an ad: the library loads at once, because until it
      does the page still shows the real number and a tap in that first
      second would be a call nobody could attribute.

   2. Clicks are caught by one delegated listener on the document rather
      than 300-odd inline handlers. Phone links appear in the red bar, the
      nav, the hero, the closing section and the footer of 44 pages;
      wiring them individually would guarantee some get missed on the
      next edit.

   3. The forwarding-number swap is done here, not by Google's default
      replacer. Google is handed the number as the page shows it and
      calls swapNumber() with the forwarding number; that function
      rewrites every tel: href and every visible occurrence of the digits,
      and leaves the JSON-LD alone so search engines still see the shop's
      own number. Buttons that read "Service My Car" show no digits, but
      their href is rewritten too, so a call from any of them is counted.
   ========================================================================== */

(function () {
  'use strict';

  /* ---- Configuration ---------------------------------------------------
     Four ids to paste, from two places:

       MEASUREMENT_ID  GA4: Admin -> Data streams -> Web -> Measurement ID
       ADS_ID          Google Ads: Goals -> Conversions -> any action ->
                       Tag setup -> "Install the tag yourself" (AW-...)
       CALL_LABEL      the label on the "Calls from website" action
       CLICK_LABEL     the label on the "Phone number click" action

     While an id is a placeholder its half is inert: no request is made and
     nothing is sent. Everything else still works, so pasting the ids is
     the only step needed to turn measurement on.

     PHONE_DISPLAY must match the number exactly as the page renders it
     (the red bar and the footer); Google provisions the forwarding number
     against it and the swap looks for those characters. */
  var MEASUREMENT_ID = 'G-5B2HHVSS3Y';
  var ADS_ID = 'AW-XXXXXXXXXX';
  var CALL_LABEL = 'XXXXXXXXXXX';
  var CLICK_LABEL = 'XXXXXXXXXXX';
  var PHONE_DISPLAY = '(678) 395-7459';

  /* X is a letter, so a placeholder satisfies its own pattern and would
     otherwise pass as a real id and fetch gtag against a property that
     does not exist. Each is ruled out by name. */
  function isSet(value, placeholder, shape) {
    return value !== placeholder && shape.test(value);
  }
  var ga4Configured = isSet(MEASUREMENT_ID, 'G-XXXXXXXXXX', /^G-[A-Z0-9]{6,}$/);
  var adsConfigured = isSet(ADS_ID, 'AW-XXXXXXXXXX', /^AW-\d{9,}$/);
  var callConfigured = adsConfigured &&
                       isSet(CALL_LABEL, 'XXXXXXXXXXX', /^[A-Za-z0-9_-]{8,}$/);
  var clickConfigured = adsConfigured &&
                        isSet(CLICK_LABEL, 'XXXXXXXXXXX', /^[A-Za-z0-9_-]{8,}$/);
  /* Only the live site reports. A local build served from localhost, a
     file:// preview or a GitHub Pages preview domain would otherwise send
     real page views and phone taps into the production property. */
  var LIVE_HOSTS = /(^|\.)germanperformancega\.com$/;
  var onLiveSite = LIVE_HOSTS.test(window.location.hostname);
  var configured = onLiveSite && (ga4Configured || adsConfigured);

  /* ---- gtag stub, defined before anything can fire ------------------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  /* ---- Did this visitor come from an ad? -----------------------------
     Google's auto-tagging puts gclid (or gbraid/wbraid on iOS) on the
     landing URL and the library then keeps it in a first-party cookie
     for later pages. Either sign means the swap will be wanted. */
  function fromAd() {
    return /[?&](gclid|gbraid|wbraid)=/.test(window.location.search) ||
           /(^|;\s*)_gcl_(aw|gb)=/.test(document.cookie);
  }

  /* ---- The forwarding-number swap ------------------------------------ */
  function e164(number) {
    var digits = String(number).replace(/\D/g, '');
    return '+' + (digits.length === 10 ? '1' + digits : digits);
  }

  function swapLinks(href) {
    document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
      if (!link.hasAttribute('data-tel-original')) {
        link.setAttribute('data-tel-original', link.getAttribute('href'));
      }
      link.setAttribute('href', href);
    });
  }

  function textNodesShowing(needle) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentNode ? node.parentNode.nodeName : '';
        if (parent === 'SCRIPT' || parent === 'STYLE') return NodeFilter.FILTER_REJECT;
        return node.nodeValue.indexOf(needle) > -1
          ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    return nodes;
  }

  function swapText(formatted) {
    textNodesShowing(PHONE_DISPLAY).forEach(function (node) {
      node.nodeValue = node.nodeValue.split(PHONE_DISPLAY).join(formatted);
    });
  }

  /* Google calls this only for visitors it has matched to an ad click;
     everyone else keeps the shop's own number. */
  function swapNumber(formatted, mobile) {
    swapLinks('tel:' + e164(mobile || formatted));
    swapText(formatted);
  }

  /* ---- Configure and load --------------------------------------------- */
  if (configured) {
    gtag('js', new Date());
    if (ga4Configured) {
      gtag('config', MEASUREMENT_ID, {
        /* The pages are static and the titles are already distinct, so the
           defaults are correct; this only pins the transport so events sent
           during unload are not dropped. */
        transport_type: 'beacon'
      });
    }
    if (adsConfigured) {
      gtag('config', ADS_ID);
    }
    if (callConfigured) {
      gtag('config', ADS_ID + '/' + CALL_LABEL, {
        phone_conversion_number: PHONE_DISPLAY,
        phone_conversion_callback: swapNumber
      });
    }

    /* One library serves both ids; whichever is configured names it. Fetch
       it at once for ad visitors, otherwise after the page has loaded and
       gone idle, so its 170 KB never competes with the fonts and photos
       a first paint is waiting on. requestIdleCallback is not in Safari,
       so fall back to a timeout rather than blocking. */
    var load = function () {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' +
              (ga4Configured ? MEASUREMENT_ID : ADS_ID);
      document.head.appendChild(s);
    };
    var whenIdle = function () {
      if ('requestIdleCallback' in window) {
        requestIdleCallback(load, { timeout: 3000 });
      } else {
        setTimeout(load, 1200);
      }
    };
    if (fromAd()) {
      load();
    } else if (document.readyState === 'complete') {
      whenIdle();
    } else {
      window.addEventListener('load', whenIdle, { once: true });
    }
  }

  /* ---- What a call is worth -------------------------------------------
     Where on the page the call started is the useful dimension: it is the
     difference between "the hero CTA works" and "people read the whole
     page and then called". Derived from the link's own position rather
     than hand-tagged, so new phone links are categorised automatically. */
  function placement(link) {
    if (link.closest('.topbar'))                 return 'top_bar';
    if (link.closest('nav, #mobile-menu'))       return 'nav';
    if (link.closest('.hero, .hc'))              return 'hero';
    if (link.closest('footer'))                  return 'footer';
    if (link.closest('.cta-final'))              return 'cta_final';
    if (link.closest('.cta-band, .cta-block'))   return 'cta_band';
    if (link.closest('.section-cta'))            return 'section_cta';
    if (link.closest('#contact, .contact-cell')) return 'contact';
    return 'body';
  }

  function label(link) {
    var text = (link.textContent || '').trim().replace(/\s+/g, ' ');
    return text.slice(0, 60) || 'tel link';
  }

  /* One listener, capture phase, so it still sees the click if something
     downstream calls stopPropagation. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href^="tel:"]');
    if (!link) return;

    var original = link.getAttribute('data-tel-original');
    gtag('event', 'generate_lead', {
      event_category: 'call',
      event_label: label(link),
      placement: placement(link),
      page_type: document.body.getAttribute('data-page-type') || 'unknown',
      /* The shop's number even when a forwarding number was dialled, so
         the report has one value for "phone"; forwarded says which. */
      phone: (original || link.getAttribute('href')).replace('tel:', ''),
      forwarded: original !== null,
      /* GA4 needs a value to report conversion worth. This is a unit, not
         a claim about revenue -- set it in the GA4 UI once the shop knows
         what a booked job averages. */
      value: 1,
      currency: 'USD'
    });

    if (clickConfigured) {
      gtag('event', 'conversion', { send_to: ADS_ID + '/' + CLICK_LABEL });
    }
  }, true);

  /* A tap on Directions is local intent that is not a call but often
     precedes one, and it is the only other outbound action on the site. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest &&
               event.target.closest('a[href*="google.com/maps"], a[href*="maps.google"], a[href*="goo.gl/maps"]');
    if (!link) return;
    gtag('event', 'get_directions', {
      event_category: 'local_intent',
      placement: placement(link)
    });
  }, true);
})();
