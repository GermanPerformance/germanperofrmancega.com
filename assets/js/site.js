/* German Performance -- one script for every page.
   The clean address, scroll reveal, the hiding nav, the Services panel,
   the mobile menu, and the active nav link. */
(function () {
  'use strict';

  /* Every page has one address, without ".html" (the homepage is "/"),
     and that is what the canonical, the sitemap and every link say. The
     host serves the ".html" spelling too and cannot redirect it, so a
     visitor who arrives that way gets the clean address in the bar
     without a reload; the canonical tag is what search engines follow. */
  var clean = location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
  if (clean !== location.pathname && window.history && history.replaceState) {
    try { history.replaceState(history.state, '', clean + location.search + location.hash); } catch (e) {}
  }

  /* Scroll reveal. Hero children animate with CSS on load, so skip them. */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = Array.prototype.slice.call(document.querySelectorAll('.fu'))
    .filter(function (el) { return !el.closest('.hc'); });

  if (!reduce && 'IntersectionObserver' in window) {
    targets.forEach(function (el) { el.classList.add('r'); });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.remove('r');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el) { observer.observe(el); });
    /* Safety net: nothing may stay hidden if the observer never fires. */
    setTimeout(function () {
      targets.forEach(function (el) { el.classList.remove('r'); });
    }, 1500);
  }

  /* Active nav link follows the section in view. The Services button is
     not a link, so it names its section in data-section. */
  var links = Array.prototype.slice.call(document.querySelectorAll(
    '.nav-links > li > a[href^="#"], .nav-links > li > [data-section]'));
  var target = function (el) { return el.getAttribute('data-section') || el.getAttribute('href'); };
  var sections = links.map(function (a) { return document.querySelector(target(a)); });
  if (links.length && 'IntersectionObserver' in window) {
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        current = entry.target.id;
        links.forEach(function (a) {
          a.classList.toggle('on', target(a) === '#' + current);
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { if (s) spy.observe(s); });
  }

  /* The Services panel under the desktop nav. A click toggles it. A
     pointer that can hover opens it on the way in, after a beat so a mouse
     crossing the bar to the call button does not flash it, and closes it
     on the way out. Escape, a click elsewhere, focus tabbing out of the
     item and the nav hiding all close it. Under 960px the panel is not
     displayed; the phone menu has its own <details>. */
  var dd = document.querySelector('.nav-dd');
  var ddBtn = dd ? dd.querySelector('.nav-dd-btn') : null;
  var setPanel = function (open) {
    if (!dd || !ddBtn || dd.classList.contains('open') === open) return;
    dd.classList.toggle('open', open);
    ddBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  };
  if (dd && ddBtn) {
    var hoverTimer = 0;
    var later = function (open, ms) {
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () { setPanel(open); }, ms);
    };
    ddBtn.addEventListener('click', function () {
      clearTimeout(hoverTimer);
      setPanel(!dd.classList.contains('open'));
    });
    if (window.matchMedia('(hover: hover)').matches) {
      dd.addEventListener('mouseenter', function () { later(true, 80); });
      dd.addEventListener('mouseleave', function () { later(false, 120); });
    }
    /* A link inside the panel closes it, which matters for the in-page
       #services link on the homepage, where nothing reloads. */
    dd.addEventListener('click', function (e) {
      if (e.target.closest('a')) setPanel(false);
    });
    /* Only a real focus move out of the item closes it. Safari and Firefox
       blur the button on a mousedown anywhere with a null relatedTarget,
       and closing then would pull a link out from under the click. */
    dd.addEventListener('focusout', function (e) {
      if (e.relatedTarget && !dd.contains(e.relatedTarget)) setPanel(false);
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target)) setPanel(false);
    });
  }

  /* Any link in the phone menu closes it; the services group's links
     carry no inline handler of their own. */
  var menu = document.getElementById('mobile-menu');
  if (menu) {
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) window.closeMenu();
    });
  }

  /* The nav leaves on the way down and comes back on the way up, the way
     a reader expects. The red phone bar above it never moves. */
  var nav = document.querySelector('nav');
  if (nav) {
    var last = window.pageYOffset;
    var queued = false;
    var travel = 0;        /* distance covered since the direction last flipped */
    var THRESHOLD = 160;   /* nothing hides while the hero is still in view */
    var HIDE_AFTER = 48;   /* downward travel before the nav leaves */
    var SHOW_AFTER = 8;    /* upward travel before it comes back */

    /* Travel accumulates rather than being compared frame to frame. A slow
       drag moves a few pixels per frame, so a per-frame threshold never
       fires and the nav would never hide; adding the movement up means
       speed does not change the behaviour, only how soon it happens. */
    var update = function () {
      queued = false;
      var y = window.pageYOffset;
      var step = y - last;
      last = y;

      if ((menu && menu.classList.contains('open')) || y <= THRESHOLD) {
        nav.classList.remove('nav-up');
        travel = 0;
        return;
      }
      if (!step) return;
      if ((step > 0) !== (travel > 0)) travel = 0;   /* direction flipped */
      travel += step;

      if (travel >= HIDE_AFTER) {
        nav.classList.add('nav-up');
        setPanel(false);
        travel = 0;
      } else if (travel <= -SHOW_AFTER) {
        nav.classList.remove('nav-up');
        travel = 0;
      }
    };

    window.addEventListener('scroll', function () {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(update);
    }, { passive: true });

    /* An anchor landing must not arrive under a hidden nav. */
    window.addEventListener('hashchange', function () {
      nav.classList.remove('nav-up');
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    window.closeMenu();
    if (dd && dd.classList.contains('open')) {
      setPanel(false);
      ddBtn.focus();
    }
  });
})();

function setMenu(open) {
  var menu = document.getElementById('mobile-menu');
  var button = document.getElementById('hamburger');
  if (!menu) return;
  menu.classList.toggle('open', open);
  if (!open) {
    var group = menu.querySelector('details');
    if (group) group.open = false;
  }
  var nav = document.querySelector('nav');
  if (nav && open) nav.classList.remove('nav-up');
  if (button) {
    button.classList.toggle('open', open);
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  document.body.style.overflow = open ? 'hidden' : '';
}
function toggleMenu() {
  var menu = document.getElementById('mobile-menu');
  setMenu(!(menu && menu.classList.contains('open')));
}
function closeMenu() { setMenu(false); }
