// Urban Gaz Limited — Site JS

// ── NAV SCROLL & HAMBURGER ─────────────────────────────
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

hamburger && hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close nav on link click (mobile)
navLinks && navLinks.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => navLinks.classList.remove('open'));
});

// ── SMOOTH SCROLL ──────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id === '#admin') return; // handled separately
    const el = document.querySelector(id);
    if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth' }); }
  });
});

// ── REVEAL ON SCROLL ───────────────────────────────────
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const delay = parseInt(e.target.dataset.delay || 0);
      setTimeout(() => e.target.classList.add('visible'), delay);
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

// ── COUNTER ANIMATION ──────────────────────────────────
function animateCount(el, target, duration = 1800) {
  const suffix = el.dataset.suffix || '';
  const isDecimal = target % 1 !== 0;
  const start = performance.now();
  function step(now) {
    const p = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    const val = target * ease;
    el.textContent = (isDecimal ? val.toFixed(2) : Math.floor(val).toLocaleString()) + suffix;
    if (p < 1) requestAnimationFrame(step);
    else el.textContent = (isDecimal ? target.toFixed(2) : target.toLocaleString()) + suffix;
  }
  requestAnimationFrame(step);
}

const statObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      document.querySelectorAll('.stat-count').forEach(el => {
        animateCount(el, parseFloat(el.dataset.target));
      });
      statObs.disconnect();
    }
  });
}, { threshold: 0.5 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) statObs.observe(heroStats);

// ── LIVE DEMO SIMULATION ───────────────────────────────
(function liveDemo() {
  const clock = document.getElementById('demoClock');
  const dFlow = document.getElementById('demoFlow');
  const dPress = document.getElementById('demoPressure');
  const dTemp = document.getElementById('demoTemp');
  const dSig = document.getElementById('demoSignal');
  const fBar = document.getElementById('flowBar');
  const pBar = document.getElementById('pressBar');
  const tBar = document.getElementById('tempBar');
  const sBar = document.getElementById('sigBar');
  const alert = document.getElementById('demoAlert');
  const hFlow = document.getElementById('heroFlow');
  const hPressure = document.getElementById('heroPressure');
  if (!clock) return;

  let flow = 12.3, pressure = 2.41, temp = 22.1, signal = -73;

  function tick() {
    const c1 = document.getElementById('demoClock');
    const c2 = document.getElementById('demoClock2');
    const now = new Date();
    const t = now.toLocaleTimeString('en-GB');
    if (c1) c1.textContent = t;
    if (c2) c2.textContent = t;
    flow = Math.max(0.1, Math.min(160, flow + (Math.random() - 0.5) * 1.2));
    pressure = Math.max(0.5, Math.min(10, pressure + (Math.random() - 0.5) * 0.15));
    temp = Math.max(10, Math.min(55, temp + (Math.random() - 0.5) * 0.5));
    signal = Math.max(-110, Math.min(-40, signal + (Math.random() - 0.5) * 3));

    if (dFlow) dFlow.textContent = flow.toFixed(1);
    if (dPress) dPress.textContent = pressure.toFixed(2);
    if (dTemp) dTemp.textContent = temp.toFixed(1);
    if (dSig) dSig.textContent = Math.round(signal);

    if (fBar) fBar.style.width = Math.min(100, (flow / 160) * 100) + '%';
    if (pBar) pBar.style.width = Math.min(100, (pressure / 10) * 100) + '%';
    if (tBar) tBar.style.width = Math.min(100, ((temp - 10) / 45) * 100) + '%';
    if (sBar) sBar.style.width = Math.min(100, ((signal + 110) / 70) * 100) + '%';

    // Sync hero cards
    if (hFlow) hFlow.textContent = flow.toFixed(1) + ' m³/h';
    if (hPressure) hPressure.textContent = pressure.toFixed(2) + ' bar';

    // Alert
    if (alert) {
      if (flow > 140) {
        alert.innerHTML = '<span class="alert-warn">⚠ High flow detected — possible leak — UGL-BD-04471</span>';
      } else if (pressure < 0.9) {
        alert.innerHTML = '<span class="alert-warn">⚠ Low pressure warning — check upstream — UGL-BD-04471</span>';
      } else {
        alert.innerHTML = '<span class="alert-ok">✓ All parameters within normal range — Unit ID: UGL-BD-04471</span>';
      }
    }
  }

  tick();
  setInterval(tick, 1500);
})();

// ── CONTACT FORM ───────────────────────────────────────
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = contactForm.querySelector('button[type="submit"]');
    btn.textContent = 'Submitting...';
    btn.disabled = true;
    btn.style.opacity = '0.7';

    try {
      const formData = new FormData(contactForm);
      await fetch(contactForm.action, {
        method: "POST",
        body: formData,
        headers: { 'Accept': 'application/json' }
      });

      btn.textContent = '✓ Request Submitted — We\'ll contact you shortly!';
      btn.style.background = '#16a34a';
      btn.style.opacity = '1';
      
      setTimeout(() => {
        btn.textContent = 'Submit Request →';
        btn.style.background = '';
        btn.disabled = false;
        contactForm.reset();
      }, 4000);
      
    } catch (error) {
      console.error(error);
      btn.textContent = '⚠ Error Sending — Try Again';
      btn.style.background = '#dc2626';
      btn.style.opacity = '1';
      
      setTimeout(() => {
        btn.textContent = 'Submit Request →';
        btn.style.background = '';
        btn.disabled = false;
      }, 3000);
    }
  });
}

// ── ADMIN MODAL ────────────────────────────────────────
const adminBtn = document.getElementById('adminBtn');
const adminModal = document.getElementById('adminModal');
const modalClose = document.getElementById('modalClose');
const adminLogin = document.getElementById('adminLogin');

adminBtn && adminBtn.addEventListener('click', e => {
  e.preventDefault();
  adminModal.classList.add('open');
});
modalClose && modalClose.addEventListener('click', () => adminModal.classList.remove('open'));
adminModal && adminModal.addEventListener('click', e => {
  if (e.target === adminModal) adminModal.classList.remove('open');
});
adminLogin && adminLogin.addEventListener('click', () => {
  const u = document.getElementById('adminUser').value;
  const p = document.getElementById('adminPass').value;
  if (!u || !p) { alert('Please enter credentials.'); return; }
  adminLogin.textContent = '⚠ Access Denied — Attempt Logged';
  adminLogin.style.background = '#dc2626';
  setTimeout(() => {
    adminLogin.textContent = 'Login to Operations Hub';
    adminLogin.style.background = '';
    adminModal.classList.remove('open');
  }, 2500);
});

// ── IMAGE LIGHTBOX ─────────────────────────────────────
(function initLightbox() {
  // Build overlay
  const overlay = document.createElement('div');
  overlay.id = 'imgLightbox';
  overlay.innerHTML = `
    <div class="lb-backdrop"></div>
    <div class="lb-inner">
      <button class="lb-close" aria-label="Close">✕</button>
      <img class="lb-img" src="" alt="">
      <p class="lb-caption"></p>
    </div>
  `;
  document.body.appendChild(overlay);

  const lbImg    = overlay.querySelector('.lb-img');
  const lbCap    = overlay.querySelector('.lb-caption');
  const lbClose  = overlay.querySelector('.lb-close');
  const backdrop = overlay.querySelector('.lb-backdrop');

  function open(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt;
    lbCap.textContent = alt;
    overlay.classList.add('lb-open');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    overlay.classList.remove('lb-open');
    document.body.style.overflow = '';
    setTimeout(() => { lbImg.src = ''; }, 300);
  }

  // Attach to all site images (except logo/nav)
  const SELECTORS = '.wt-img, .install-img, .feat-img, .hero-img, .poster-img, .gallery-img, .ceo-photo';
  document.querySelectorAll(SELECTORS).forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => open(img.src, img.alt || 'Urban Gaz'));
  });

  lbClose.addEventListener('click', close);
  backdrop.addEventListener('click', close);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();

// ── OPS MAP PIN INTERACTION ────────────────────────────
(function initMap() {
  const tooltip = document.getElementById('mapTooltip');
  const opsMap  = document.getElementById('opsMap');
  const selUnit = document.getElementById('selectedUnit');
  if (!opsMap || !tooltip) return;

  const pins = opsMap.querySelectorAll('.device-pin');
  pins.forEach(pin => {
    const id  = pin.dataset.id  || 'UGL-BD-????';
    const loc = pin.dataset.loc || 'Unknown';
    const isActive = pin.classList.contains('active-pin');
    const status = isActive ? 'Online' : 'Pending';

    pin.addEventListener('mouseenter', () => {
      tooltip.textContent = `${id} \u00b7 ${loc} \u00b7 ${status}`;
      tooltip.style.opacity = '1';
    });
    pin.addEventListener('mousemove', e => {
      const r = opsMap.getBoundingClientRect();
      tooltip.style.left = (e.clientX - r.left + 12) + 'px';
      tooltip.style.top  = (e.clientY - r.top  - 36) + 'px';
    });
    pin.addEventListener('mouseleave', () => {
      tooltip.style.opacity = '0';
    });
    pin.addEventListener('click', () => {
      if (selUnit && isActive) selUnit.textContent = `${id} \u00b7 ${loc}`;
    });
  });
})();
