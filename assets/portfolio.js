/*
  Small progressive enhancements. Content is readable without JavaScript.
  Page-level behaviour lives in init(scope) so the single-file phone preview can call
  window.PB.init(root) after it swaps pages, instead of keeping its own copy of this code.
*/
(() => {
  const root = document.documentElement;
  /* Motion policy: follow the device setting unless the visitor chose otherwise with the footer switch. */
  let motionChoice = null;
  try { motionChoice = localStorage.getItem('pb-motion'); } catch (_) {}
  const osReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reduced = motionChoice === 'full' ? false : motionChoice === 'reduced' ? true : osReduced;
  root.dataset.motion = reduced ? 'reduced' : 'full';
  const dataSaver = navigator.connection?.saveData === true;
  const ROLES = ['Robotics Software Engineer', 'ROS 2 Developer', 'Robotics Simulation Engineer'];

  /* ---------- theme: follow the device on first visit, remember an explicit choice ---------- */
  const media = matchMedia('(prefers-color-scheme: dark)');
  const readChoice = () => { try { return localStorage.getItem('pb-color-mode'); } catch (_) { return null; } };
  function renderTheme(mode) {
    root.dataset.theme = mode;
    const dark = mode === 'dark';
    document.querySelectorAll('.theme-toggle').forEach(b => {
      b.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
      b.setAttribute('title', `Switch to ${dark ? 'light' : 'dark'} mode`);
      b.setAttribute('aria-pressed', String(dark));
      if (b.firstElementChild) b.firstElementChild.textContent = dark ? '☀' : '☾';
    });
  }
  const choice = readChoice();
  root.dataset.theme = choice === 'dark' || choice === 'light' ? choice : (media.matches ? 'dark' : 'light');
  media.addEventListener?.('change', e => { if (!readChoice()) renderTheme(e.matches ? 'dark' : 'light'); });

  /* ---------- image viewer (one overlay for the whole document) ---------- */
  const overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Expanded project image');
  overlay.innerHTML = '<button class="lightbox-close" type="button" aria-label="Close expanded image">×</button><img alt="">';
  const picture = overlay.querySelector('img');
  const closeBtn = overlay.querySelector('button');
  let returnFocus = null;
  function closeViewer() {
    overlay.classList.remove('is-open');
    picture.removeAttribute('src');
    returnFocus?.focus?.();
  }
  closeBtn.addEventListener('click', closeViewer);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeViewer(); });

  /* ---------- floating jump button ---------- */
  const jump = document.createElement('button');
  jump.className = 'jump-toggle';
  jump.type = 'button';
  function syncJump() {
    const up = scrollY > Math.max(350, innerHeight * 0.7);
    jump.textContent = up ? '↑' : '↓';
    jump.title = up ? 'Back to top' : 'Jump to bottom';
    jump.setAttribute('aria-label', jump.title);
    jump.dataset.up = String(up);
    jump.classList.toggle('is-visible', root.scrollHeight > innerHeight + 350);
  }
  jump.addEventListener('click', () => scrollTo({ top: jump.dataset.up === 'true' ? 0 : root.scrollHeight, behavior: reduced ? 'auto' : 'smooth' }));
  addEventListener('scroll', syncJump, { passive: true });

  /* ---------- global keys / resize ---------- */
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if (overlay.classList.contains('is-open')) { closeViewer(); return; }
    const menu = document.querySelector('.menu-toggle'), links = document.querySelector('.nav-links');
    if (menu && links?.classList.contains('is-open')) { menu.setAttribute('aria-expanded', 'false'); links.classList.remove('is-open'); menu.focus(); }
  });
  addEventListener('resize', () => {
    if (innerWidth > 780) {
      const menu = document.querySelector('.menu-toggle'), links = document.querySelector('.nav-links');
      menu?.setAttribute('aria-expanded', 'false');
      links?.classList.remove('is-open');
    }
    syncJump();
  }, { passive: true });

  /* ---------- video: card loops play only while visible; nothing autoplays on reduced motion / data saver ---------- */
  let videoObserver = null;
  function watchCardVideos(scope) {
    const vids = scope.querySelectorAll('video[data-card-video]');
    if (!vids.length) return;
    vids.forEach(v => { v.muted = true; });
    if (reduced || dataSaver || !('IntersectionObserver' in window)) return; // poster stays as a still image
    videoObserver ??= new IntersectionObserver(entries => entries.forEach(e => {
      const v = e.target;
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    }), { threshold: 0.25 });
    vids.forEach(v => videoObserver.observe(v));
  }

  /* ---------- motion layer (skipped entirely when motion is reduced) ---------- */
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  let globalsReady = false;
  function setupGlobals() {
    if (globalsReady) return;
    globalsReady = true;
    if (reduced) return;
    const bar = document.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);
    let ticking = false;
    const frame = () => {
      ticking = false;
      const max = root.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
      document.querySelector('.site-header')?.classList.toggle('is-scrolled', scrollY > 24);
      const copy = document.querySelector('.hero-copy');
      if (copy && scrollY < innerHeight) {
        copy.style.transform = `translateY(${(scrollY * 0.12).toFixed(1)}px)`;
        copy.style.opacity = String(Math.max(0.25, 1 - scrollY / (innerHeight * 0.9)).toFixed(2));
      }
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
    frame();
  }

  function enhance(scope) {
    setupGlobals();
    // theme toggle spins when pressed (works in every motion mode: it is a tiny, user-triggered effect)
    scope.querySelectorAll('.theme-toggle').forEach(b => b.addEventListener('click', () => {
      b.firstElementChild?.animate([{ transform: 'rotate(0) scale(1)' }, { transform: 'rotate(180deg) scale(.6)' }, { transform: 'rotate(360deg) scale(1)' }], { duration: 520, easing: 'cubic-bezier(.2,.8,.2,1)' });
    }));

    // footer: motion switch
    scope.querySelectorAll('footer').forEach(f => {
      if (f.querySelector('.motion-toggle')) return;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'motion-toggle';
      b.setAttribute('aria-pressed', String(!reduced));
      b.textContent = reduced ? 'Animations: off' : 'Animations: on';
      b.title = 'Turn page animations on or off';
      b.addEventListener('click', () => {
        try { localStorage.setItem('pb-motion', reduced ? 'full' : 'reduced'); } catch (_) {}
        location.reload();
      });
      f.append(b);
    });
    if (reduced) return;

    // staggered reveal: index inside each group drives the delay
    const groups = ['.stack-grid', '.research-grid', '.education-content', '.secondary-grid', '.archive-grid', '.contact-actions', '.about-links', '.evidence-gallery'];
    groups.forEach(sel => scope.querySelectorAll(sel).forEach(g => [...g.children].forEach((c, i) => c.style.setProperty('--i', i))));
    // detail pages: reveal copy blocks as they scroll in
    if ('IntersectionObserver' in window) {
      const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io2.unobserve(e.target); } }), { threshold: 0.06, rootMargin: '0px 0px 40px 0px' });
      scope.querySelectorAll('.detail-main > h2, .detail-main > p, .detail-main > ul > li, .detail-figure, .comparison, .evidence-link, .interior-head .shell > *').forEach((el, i) => {
        if (el.classList.contains('reveal')) return;
        el.classList.add('reveal', 'can-reveal');
        if (el.matches('li, .evidence-link')) el.style.setProperty('--i', [...el.parentElement.children].indexOf(el));
        io2.observe(el);
      });
    }

    // scrollspy: highlight the nav link of the section on screen (home page)
    const spyLinks = [...scope.querySelectorAll('.nav-links a[href*="#"]')];
    const spy = spyLinks.map(a => ({ a, sec: document.getElementById(a.getAttribute('href').split('#')[1]) })).filter(x => x.sec);
    if (spy.length && 'IntersectionObserver' in window && scope.querySelector('.hero')) {
      const so = new IntersectionObserver(es => es.forEach(e => {
        if (!e.isIntersecting) return;
        spy.forEach(x => x.a.classList.toggle('is-active', x.sec === e.target)); // hero has no link: clears the rest
      }), { rootMargin: '-45% 0px -50% 0px' });
      spy.forEach(x => so.observe(x.sec));
      const heroEl = scope.querySelector('.hero');
      if (heroEl) so.observe(heroEl);
    }

    if (fine) {
      // cursor-following light on hero and cards
      const hero = scope.querySelector('.hero');
      hero?.addEventListener('pointermove', e => {
        const r = hero.getBoundingClientRect();
        hero.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        hero.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      }, { passive: true });
      scope.querySelectorAll('.project-card, .stack-card, .research-card, .simple-cert').forEach(c => c.addEventListener('pointermove', e => {
        const r = c.getBoundingClientRect();
        c.style.setProperty('--px', (e.clientX - r.left) + 'px');
        c.style.setProperty('--py', (e.clientY - r.top) + 'px');
      }, { passive: true }));
    }
  }

  /* ---------- per-page setup ---------- */
  function init(scope = document) {
    // navigation menu
    const menu = scope.querySelector('.menu-toggle'), links = scope.querySelector('.nav-links');
    if (menu && links) {
      menu.addEventListener('click', () => {
        const open = menu.getAttribute('aria-expanded') !== 'true';
        menu.setAttribute('aria-expanded', String(open));
        links.classList.toggle('is-open', open);
      });
      links.addEventListener('click', e => {
        if (e.target.closest('a')) { menu.setAttribute('aria-expanded', 'false'); links.classList.remove('is-open'); }
      });
    }

    // theme buttons
    scope.querySelectorAll('.theme-toggle').forEach(b => b.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      renderTheme(next);
      try { localStorage.setItem('pb-color-mode', next); } catch (_) {}
    }));
    renderTheme(root.dataset.theme);

    scope.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

    // scroll reveal
    if (!reduced && !dataSaver && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver(entries => entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      }), { threshold: 0.08, rootMargin: '0px 0px 35px 0px' });
      scope.querySelectorAll('.reveal').forEach(el => { el.classList.add('can-reveal'); io.observe(el); });
    }

    // Test 06 / Test 07 switcher: pause whichever recording is hidden
    const comparison = scope.querySelector('[data-comparison]');
    if (comparison) {
      const buttons = comparison.querySelectorAll('[data-view]');
      const panels = comparison.querySelectorAll('[data-panel]');
      buttons.forEach(btn => btn.addEventListener('click', () => {
        buttons.forEach(b => { const on = b === btn; b.setAttribute('aria-pressed', String(on)); b.classList.toggle('is-active', on); });
        panels.forEach(p => {
          p.hidden = p.dataset.panel !== btn.dataset.view;
          if (p.hidden) p.querySelectorAll('video').forEach(v => v.pause());
        });
      }));
    }

    // image viewer links
    scope.querySelectorAll('a[data-lightbox]').forEach(a => a.addEventListener('click', e => {
      e.preventDefault();
      returnFocus = a;
      picture.src = a.href;
      picture.alt = a.querySelector('img')?.alt || 'Expanded project image';
      if (!overlay.isConnected) document.body.append(overlay);
      overlay.classList.add('is-open');
      closeBtn.focus();
    }));
    if (!overlay.isConnected) document.body.append(overlay);
    if (!jump.isConnected) document.body.append(jump);

    watchCardVideos(scope);

    // hero roles: short delay, type in, stay visible, then change to the next role
    const target = scope.querySelector('[data-typing-role]');
    if (target) {
      let role = 0;
      if (reduced) {
        // no typing movement: hold each role, then cross-fade (Web Animations API, so it is not switched off by CSS)
        target.textContent = ROLES[0];
        const swap = () => {
          if (!target.isConnected) return;
          target.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 260, fill: 'forwards' }).finished.then(() => {
            role = (role + 1) % ROLES.length;
            target.textContent = ROLES[role];
            target.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 260, fill: 'forwards' });
            setTimeout(swap, 2400);
          });
        };
        setTimeout(swap, 2400);
      } else {
        let pos = 0, removing = false;
        target.textContent = '';
        const tick = () => {
          if (!target.isConnected) return;
          const word = ROLES[role];
          pos = removing ? Math.max(0, pos - 1) : Math.min(word.length, pos + 1);
          target.textContent = word.slice(0, pos);
          if (!removing && pos === word.length) { removing = true; setTimeout(tick, 1900); return; } // stays visible
          if (removing && pos === 0) { removing = false; role = (role + 1) % ROLES.length; setTimeout(tick, 280); return; }
          setTimeout(tick, removing ? 32 : 70);
        };
        setTimeout(tick, 700); // short delay before the first role appears
      }
    }

    enhance(scope);
    syncJump();
  }

  window.PB = { init, syncJump };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => init());
  else init();
})();
