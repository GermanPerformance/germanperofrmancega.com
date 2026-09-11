/* German Performance -- one script for every page.
   Scroll reveal, the hiding nav, the mobile menu, and the active nav link. */
(function () {
  'use strict';

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

  /* Active nav link follows the section in view. */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  if (links.length && 'IntersectionObserver' in window) {
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        current = entry.target.id;
        links.forEach(function (a) {
          a.classList.toggle('on', a.getAttribute('href') === '#' + current);
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { if (s) spy.observe(s); });
  }

  /* The nav leaves on the way down and comes back on the way up, the way
     a reader expects. The red phone bar above it never moves. */
  var nav = document.querySelector('nav');
  if (nav) {
    var last = window.pageYOffset;
    var queued = false;
    var THRESHOLD = 160;   /* nothing hides while the hero is still in view */
    var DELTA = 6;         /* trackpad jitter must not flicker the bar */

    var update = function () {
      queued = false;
      var y = window.pageYOffset;
      var menu = document.getElementById('mobile-menu');
      var menuOpen = !!(menu && menu.classList.contains('open'));

      if (menuOpen || y <= THRESHOLD) {
        nav.classList.remove('nav-up');
      } else if (y > last + DELTA) {
        nav.classList.add('nav-up');
      } else if (y < last - DELTA) {
        nav.classList.remove('nav-up');
      }
      last = y;
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
    if (e.key === 'Escape') window.closeMenu();
  });
})();

function setMenu(open) {
  var menu = document.getElementById('mobile-menu');
  var button = document.getElementById('hamburger');
  if (!menu) return;
  menu.classList.toggle('open', open);
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
