document.querySelectorAll('.fu').forEach(el=>el.classList.add('r'));
const obs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){setTimeout(()=>e.target.classList.remove('r'),80);obs.unobserve(e.target)}})},{threshold:.05,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.fu').forEach(el=>obs.observe(el));
setTimeout(()=>{document.querySelectorAll('.fu.r').forEach(el=>el.classList.remove('r'))},1000);
function toggleFaq(btn){const fi=btn.closest('.fi'),open=fi.classList.contains('open');document.querySelectorAll('.fi.open').forEach(i=>i.classList.remove('open'));if(!open)fi.classList.add('open')}
function toggleMenu(){document.getElementById('mobile-menu').classList.toggle('open');document.getElementById('hamburger').classList.toggle('open');document.body.style.overflow=document.getElementById('mobile-menu').classList.contains('open')?'hidden':''}
function closeMenu(){document.getElementById('mobile-menu').classList.remove('open');document.getElementById('hamburger').classList.remove('open');document.body.style.overflow=''}
