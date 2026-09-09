// ── REVIEWS SLIDER ──
function goSlide(n) {
  var track = document.getElementById('rpTrack');
  var dots = document.querySelectorAll('.rp-dot');
  if (!track) return;
  currentSlide = n;
  track.style.transform = 'translateX(-' + (n * 100) + '%)';
  dots.forEach(function(d, i) { d.classList.toggle('active', i === n); });
}
var currentSlide = 0;
var totalSlides = 5;
setInterval(function() {
  currentSlide = (currentSlide + 1) % totalSlides;
  goSlide(currentSlide);
}, 4000);

// ── SERVICE TICKER ──
(function() {
  var heroItems = document.querySelectorAll('.ticker-item');
  var miniItems = document.querySelectorAll('.mini-ticker-item');
  var current = 0;
  function tick() {
    heroItems.forEach(function(el, i) { el.classList.toggle('active', i === current); });
    miniItems.forEach(function(el, i) { el.classList.toggle('active', i === current); });
    current = (current + 1) % heroItems.length;
  }
  tick();
  setInterval(tick, 1800);
})();

function toggleFaq(btn) {
  var answer = btn.nextElementSibling;
  var isOpen = answer.classList.contains('open');
  // Close all
  document.querySelectorAll('.faq-a.open').forEach(function(a) {
    a.classList.remove('open');
    a.previousElementSibling.setAttribute('aria-expanded', 'false');
  });
  // Open clicked if it was closed
  if (!isOpen) {
    answer.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
  }
}
// Fade-up on scroll - safe version
  document.querySelectorAll('.fade-up').forEach(el => el.classList.add('ready'));

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        setTimeout(() => {
          e.target.classList.remove('ready');
        }, 80);
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  // Fallback: if IntersectionObserver never fires, show everything after 1s
  setTimeout(() => {
    document.querySelectorAll('.fade-up.ready').forEach(el => el.classList.remove('ready'));
  }, 1000);

  // Smooth nav active state
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 120) current = s.getAttribute('id');
    });
    navLinks.forEach(a => {
      a.style.color = a.getAttribute('href') === '#' + current ? 'var(--white)' : '';
    });
  });
function toggleMenu() {
  var m = document.getElementById('mob-menu');
  var h = document.getElementById('ham');
  if (m.style.display === 'flex') {
    m.style.display = 'none';
    document.body.style.overflow = '';
  } else {
    m.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}
function closeMenu() {
  document.getElementById('mob-menu').style.display = 'none';
  document.body.style.overflow = '';
}
