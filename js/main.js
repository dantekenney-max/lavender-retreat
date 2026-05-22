/* ─── Nav scroll ─── */
const nav = document.querySelector('.nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  });
}

/* ─── Mobile nav ─── */
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');
const mobileOverlay = document.getElementById('mobileOverlay');
const mobileClose = document.getElementById('mobileClose');
function openNav() { mobileNav.classList.add('open'); mobileOverlay.classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeNav() { mobileNav.classList.remove('open'); mobileOverlay.classList.remove('open'); document.body.style.overflow = ''; }
if (hamburger) { hamburger.addEventListener('click', openNav); }
if (mobileClose) { mobileClose.addEventListener('click', closeNav); }
if (mobileOverlay) { mobileOverlay.addEventListener('click', closeNav); }

/* ─── Scroll reveal ─── */
const reveals = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
reveals.forEach(el => revealObserver.observe(el));

/* ─── FAQ accordion ─── */
document.querySelectorAll('.faq-item').forEach(item => {
  item.querySelector('.faq-question').addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

/* ─── Gallery filter ─── */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.masonry-item').forEach(item => {
      item.style.display = (filter === 'all' || item.dataset.category === filter) ? 'block' : 'none';
    });
  });
});

/* ─── Form feedback ─── */
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', e => {
    if (form.dataset.netlify === undefined) e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = 'Sent — Thank You';
      btn.style.background = '#7A9E7E';
      btn.style.color = 'white';
      setTimeout(() => {
        btn.textContent = orig;
        btn.style.background = '';
        btn.style.color = '';
        form.reset();
      }, 3500);
    }
  });
});

/* ─── Smooth hero parallax ─── */
const heroBg = document.querySelector('.hero-bg');
if (heroBg) {
  window.addEventListener('scroll', () => {
    heroBg.style.transform = `translateY(${window.scrollY * 0.28}px)`;
  }, { passive: true });
}

/* ─── Active nav link ─── */
const path = window.location.pathname.split('/').pop();
document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(a => {
  if (a.getAttribute('href') === path || (path === '' && a.getAttribute('href') === 'index.html')) {
    a.classList.add('active');
  }
});
