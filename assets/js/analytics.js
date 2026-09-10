/* ==========================================================================
   German Performance -- measurement

   The only conversion on this site is a phone call. There is no form, no
   cart and no signup, so "a call was started" is the single number that
   says whether any of the SEO or design work did anything. Until now the
   site had no analytics at all, which meant five phases of changes with
   no way to tell what they were worth.

   Two decisions worth knowing about:

   1. The gtag stub is defined synchronously but the library is fetched on
      idle. gtag() only pushes onto dataLayer; the library drains that
      queue whenever it arrives. So events fired in the first second are
      not lost, and ~50KB of third-party JavaScript stays off the critical
      path -- which matters here, because getting the homepage from 1.59MB
      down to 44.5KB was most of Phase 2.

   2. Clicks are caught by one delegated listener on the document rather
      than 259 inline handlers. Phone links appear in the nav, the hero,
      every card, the footer and the mobile call bar of 38 pages; wiring
      them individually would guarantee some get missed on the next edit.
   ========================================================================== */

(function () {
  'use strict';

  /* ---- Configuration ---------------------------------------------------
     Replace with the GA4 Measurement ID from
     Admin -> Data streams -> Web -> Measurement ID.
     While this is a placeholder the file is inert: no network request is
     made and nothing is sent. Everything else still works, so setting the
     id is the only step needed to turn measurement on. */
  var MEASUREMENT_ID = 'G-XXXXXXXXXX';

  /* X is a letter, so the placeholder satisfies [A-Z0-9] and would
     otherwise pass as a real id and fetch gtag against a property
     that does not exist. Rule it out explicitly. */
  var PLACEHOLDER = 'G-XXXXXXXXXX';
  var configured = MEASUREMENT_ID !== PLACEHOLDER &&
                   /^G-[A-Z0-9]{6,}$/.test(MEASUREMENT_ID);

  /* ---- gtag stub, defined before anything can fire ------------------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  if (configured) {
    gtag('js', new Date());
    gtag('config', MEASUREMENT_ID, {
      /* The pages are static and the titles are already distinct, so the
         defaults are correct; this only pins the transport so events sent
         during unload are not dropped. */
      transport_type: 'beacon'
    });

    /* Fetch the library once the page is idle. requestIdleCallback is not
       in Safari, so fall back to a timeout rather than blocking. */
    var load = function () {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
      document.head.appendChild(s);
    };
    if ('requestIdleCallback' in window) {
      requestIdleCallback(load, { timeout: 3000 });
    } else {
      setTimeout(load, 1200);
    }
  }

  /* ---- What a call is worth -------------------------------------------
     Where on the page the call started is the useful dimension: it is the
     difference between "the hero CTA works" and "people read the whole
     page and then called". Derived from the link's own position rather
     than hand-tagged, so new phone links are categorised automatically. */
  function placement(link) {
    if (link.closest('.call-bar, .cb-call')) return 'mobile_call_bar';
    if (link.closest('nav, #mobile-menu'))   return 'nav';
    if (link.closest('.hero, .hc, .hero-info')) return 'hero';
    if (link.closest('footer'))              return 'footer';
    if (link.closest('.cta-band, .cta-block, .cta')) return 'cta_band';
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

    gtag('event', 'generate_lead', {
      event_category: 'call',
      event_label: label(link),
      placement: placement(link),
      page_type: document.body.getAttribute('data-page-type') || 'unknown',
      phone: link.getAttribute('href').replace('tel:', ''),
      /* GA4 needs a value to report conversion worth. This is a unit, not
         a claim about revenue -- set it in the GA4 UI once the shop knows
         what a booked job averages. */
      value: 1,
      currency: 'USD'
    });
  }, true);

  /* A tap on Directions is local intent that is not a call but often
     precedes one, and it is the only other outbound action on the site. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest &&
               event.target.closest('a[href*="maps.google"], a[href*="goo.gl/maps"], a.cb-dir');
    if (!link) return;
    gtag('event', 'get_directions', {
      event_category: 'local_intent',
      placement: placement(link)
    });
  }, true);
})();
