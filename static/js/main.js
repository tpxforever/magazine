/* ============================================
   CINEMAWORDS — Main JS
============================================ */

// ---- SCROLL-TRIGGERED NAV ----
const nav = document.getElementById('nav');
if (nav) {
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ---- MOBILE NAV ----
const burger = document.getElementById('navBurger');
const mobileNav = document.getElementById('navMobile');
if (burger && mobileNav) {
  burger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
    const isOpen = mobileNav.classList.contains('open');
    burger.setAttribute('aria-expanded', isOpen);
  });
}

// ---- REVEAL ON SCROLL ----
const revealEls = document.querySelectorAll('.reveal');
if (revealEls.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  );
  revealEls.forEach(el => observer.observe(el));
}

// ---- RATING BAR ANIMATE ----
const ratingBar = document.querySelector('.rating-bar__fill');
if (ratingBar) {
  setTimeout(() => {
    // width already set via inline style — just ensure it visually transitions in
    const w = ratingBar.style.width;
    ratingBar.style.width = '0';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        ratingBar.style.width = w;
      });
    });
  }, 400);
}

// ---- SMOOTH TYPING EFFECT FOR HERO (optional flair) ----
// Adds a blinking cursor to the hero headline
const heroHeadline = document.querySelector('.hero__headline');
if (heroHeadline) {
  heroHeadline.style.opacity = '1'; // override reveal for hero
}

// ---- CUSTOM CURSOR (subtle) ----
// Only on desktop
if (window.matchMedia('(pointer: fine)').matches) {
  const cursor = document.createElement('div');
  cursor.style.cssText = `
    position: fixed; width: 8px; height: 8px; border-radius: 50%;
    background: rgba(201, 168, 76, 0.7); pointer-events: none;
    z-index: 9999; transition: transform 0.15s ease, opacity 0.3s ease;
    transform: translate(-50%, -50%);
  `;
  document.body.appendChild(cursor);

  let mx = 0, my = 0;
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx + 'px';
    cursor.style.top = my + 'px';
  });

  document.addEventListener('mousedown', () => {
    cursor.style.transform = 'translate(-50%, -50%) scale(2)';
    cursor.style.opacity = '0.4';
  });
  document.addEventListener('mouseup', () => {
    cursor.style.transform = 'translate(-50%, -50%) scale(1)';
    cursor.style.opacity = '1';
  });

  // Hide over interactive elements
  document.querySelectorAll('a, button, input, textarea, select').forEach(el => {
    el.addEventListener('mouseenter', () => { cursor.style.opacity = '0'; });
    el.addEventListener('mouseleave', () => { cursor.style.opacity = '1'; });
  });
}

// ---- AUTO-DISMISS MESSAGES ----
document.querySelectorAll('.message').forEach(msg => {
  setTimeout(() => {
    msg.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    msg.style.opacity = '0';
    msg.style.transform = 'translateX(20px)';
    setTimeout(() => msg.remove(), 400);
  }, 5000);
});
