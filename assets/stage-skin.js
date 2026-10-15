/* Website skin for Lecture Stage pages, added by publish_lecture.py (the engine page is untouched).
   - Moves the engine's toolbar buttons (by id, so their handlers keep working) into a floating dock
     centred under the slide; the dock fades when the mouse rests and returns on any movement.
   - Slide picker in the dock, and "type a slide number, then Enter" to jump.
   Every step checks that the element exists, so an engine change degrades to the plain toolbar. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const tools = document.querySelector('.bar .tools');
  if (!tools || !$('bNext') || typeof go !== 'function' || typeof DATA === 'undefined') return;

  const svg = d => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  const ICON = {
    bPrev: svg('<path d="M15 6l-6 6 6 6"/>'),
    bNext: svg('<path d="M9 6l6 6-6 6"/>'),
    bAsk: svg('<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 4.6a3.2 3.2 0 0 1 0 6.1M21 20c0-2.8-1.8-5.1-4.3-5.8"/>'),
    bAll: svg('<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    bTs: svg('<path d="M4 20V4M4 20h16"/><path d="M7 16c2-8 5-10 7-10s3 3 5 4"/>'),
    bSplit: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 5v14"/>'),
    bZoom: svg('<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3M11 8v6M8 11h6"/>'),
    bPres: svg('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>'),
    bFull: svg('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>'),
    bBlack: svg('<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>')
  };
  const NAME = { bPrev: 'Previous slide', bNext: 'Next slide', bAsk: 'Ask the class', bAll: 'Reveal all', bTs: 'Figure lab',
    bSplit: 'Slide width', bZoom: 'Zoom slide', bPres: 'Presenter notes', bFull: 'Full screen', bBlack: 'Blackout' };
  const GROUPS = [['bPrev', 'PICK', 'bNext'], ['bAsk', 'bAll', 'bTs'], ['bSplit', 'splitRange', 'bZoom', 'bPres', 'bFull', 'bBlack']];

  const dock = document.createElement('div');
  dock.className = 'skin-dock';
  dock.setAttribute('role', 'toolbar');
  dock.setAttribute('aria-label', 'Lecture controls');

  const pick = document.createElement('select');
  pick.className = 'pick';
  pick.title = 'Jump to a slide (or type its number, then Enter)';
  pick.setAttribute('aria-label', 'Jump to slide');
  pick.innerHTML = DATA.map((s, i) => '<option value="' + i + '">' + s.n + ' / ' + DATA.length + ' · ' +
    String(s.title || '').replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</option>').join('');
  pick.addEventListener('change', () => { go(+pick.value); pick.blur(); });
  const goTag = document.createElement('span');
  goTag.className = 'skin-go';
  goTag.hidden = true;

  function iconise(id) {
    const b = $(id);
    if (!b) return null;
    const key = (b.querySelector('kbd') || {}).textContent;
    const tip = NAME[id] + (key ? ' (' + key.trim() + ')' : '');
    b.title = tip;
    b.setAttribute('aria-label', tip);
    if (id === 'bSplit') {
      const pct = (b.textContent.match(/(\d+)\s*%/) || [, '50'])[1];
      b.classList.add('wide');
      b.innerHTML = ICON.bSplit + '<span>' + pct + '%</span>';
    } else {
      b.innerHTML = ICON[id];
    }
    return b;
  }

  GROUPS.forEach((g, gi) => {
    if (gi) { const s = document.createElement('span'); s.className = 'dsep'; dock.appendChild(s); }
    g.forEach(id => {
      if (id === 'PICK') { dock.appendChild(pick); dock.appendChild(goTag); return; }
      const el = id === 'splitRange' ? $(id) : iconise(id);
      if (el) { el.removeAttribute('style'); dock.appendChild(el); }
    });
  });
  document.body.appendChild(dock);

  // The engine rewrites the width button's label on every change; put the icon back.
  const split = $('bSplit');
  if (split) new MutationObserver(() => { if (!split.querySelector('svg')) iconise('bSplit'); placeDock(); })
    .observe(split, { childList: true, characterData: true, subtree: true });

  // Keep the picker in step with the engine's slide counter.
  const ctr = $('ctr');
  const sync = () => { if (typeof cur === 'number') pick.value = cur; };
  if (ctr) new MutationObserver(sync).observe(ctr, { childList: true, characterData: true, subtree: true });
  sync();

  // Placement and fade.
  let idleT = 0, buf = '', bufT = 0;
  function placeDock() {
    const wrap = document.querySelector('.slidewrap');
    const w = dock.offsetWidth, vw = innerWidth;
    let x = vw / 2;
    if (wrap && vw >= 900) { const r = wrap.getBoundingClientRect(); x = r.left + r.width / 2; }
    dock.style.left = Math.max(w / 2 + 12, Math.min(vw - w / 2 - 12, x)) + 'px';
  }
  function showDock() {
    if (dock.classList.contains('idle')) placeDock();
    dock.classList.remove('idle');
    clearTimeout(idleT);
    idleT = setTimeout(() => {
      if (dock.matches(':hover') || document.activeElement === pick || buf) return showDock();
      dock.classList.add('idle');
    }, 2800);
  }
  ['mousemove', 'touchstart', 'pointerdown'].forEach(ev => document.addEventListener(ev, showDock, { passive: true }));
  addEventListener('resize', placeDock);
  placeDock();
  showDock();
  requestAnimationFrame(placeDock);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeDock);
  pick.addEventListener('change', placeDock);

  // Type a slide number, then Enter. Runs before the engine's key handler (capture phase).
  function setBuf(v) {
    buf = v;
    goTag.hidden = !v;
    goTag.textContent = v ? 'Go to ' + v + ' ⏎' : '';
    clearTimeout(bufT);
    if (v) { showDock(); bufT = setTimeout(() => setBuf(''), 4000); }
  }
  const overlayOpen = () => ['ask', 'tslab', 'zoom', 'black'].some(id => $(id) && $(id).classList.contains('on'));
  document.addEventListener('keydown', e => {
    const tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.metaKey || e.ctrlKey || e.altKey || overlayOpen()) return;
    if (/^[0-9]$/.test(e.key)) { e.preventDefault(); e.stopImmediatePropagation(); setBuf((buf + e.key).slice(-3)); return; }
    if (buf && e.key === 'Enter') {
      e.preventDefault(); e.stopImmediatePropagation();
      const n = +buf, i = DATA.findIndex(s => s.n === n);
      setBuf('');
      go(i >= 0 ? i : Math.min(Math.max(n - 1, 0), DATA.length - 1));
      return;
    }
    if (buf && (e.key === 'Escape' || e.key === 'Backspace')) { e.preventDefault(); e.stopImmediatePropagation(); setBuf(e.key === 'Escape' ? '' : buf.slice(0, -1)); }
  }, true);

  // Book panel: figures and worked examples from the Cengel knowledge base (book.json, written by the publish step).
  const bookSvg = svg('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>');
  fetch('book.json', { cache: 'no-cache' }).then(r => (r.ok ? r.json() : {})).then(BOOK => {
    if (!BOOK || !Object.keys(BOOK).length) return;
    const btn = document.createElement('button');
    btn.className = 'tb'; btn.id = 'skinBook'; btn.innerHTML = bookSvg;
    btn.title = 'Book figure or example for this slide (K)'; btn.setAttribute('aria-label', btn.title);
    const ts = $('bTs');
    ts && ts.parentNode === dock ? ts.after(btn) : dock.appendChild(btn);
    const chip = document.createElement('button');
    chip.className = 'skin-chip'; chip.hidden = true;
    const eyebrow = $('eyebrow');
    if (eyebrow) eyebrow.after(chip);
    const ov = document.createElement('div');
    ov.className = 'skin-book'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', 'Book');
    document.body.appendChild(ov);
    const esc = t => String(t || '').replace(/&/g, '&amp;').replace(/</g, '&lt;');
    const entry = () => (typeof cur === 'number' && DATA[cur] ? BOOK[String(DATA[cur].n)] : null);
    function refresh() {
      const e = entry();
      btn.disabled = !e;
      chip.hidden = !e;
      if (e) chip.textContent = 'Çengel: ' + [...e.figures.map(f => 'Fig. ' + f.id), ...e.examples.map(x => 'Ex. ' + x.id)].join(' · ');
      if (!e) ov.classList.remove('on');
      placeDock();
    }
    function open() {
      const e = entry();
      if (!e) return;
      const figs = e.figures.map(f => f.image
        ? '<figure class="bk-fig"><img src="' + esc(f.image) + '" alt="Cengel figure ' + esc(f.id) + '"><figcaption><b>Figure ' + esc(f.id) + '</b> ' + esc(f.caption) + ' <span>Çengel 9e, p. ' + f.page + '</span></figcaption></figure>'
        : '<div class="bk-fig bk-pending"><b>Figure ' + esc(f.id) + '</b> ' + esc(f.caption) + '<span>Çengel 9e, p. ' + f.page + '. The page image appears here once the book pages are rendered.</span></div>');
      ov.innerHTML = '<div class="bk-wrap"><div class="bk-bar"><span>Çengel and Boles, Thermodynamics 9e (SI)</span><button class="bk-close" aria-label="Close (Esc)">Close <kbd>Esc</kbd></button></div>' +
        figs.join('') + e.examples.map(x => x.html).join('') + '</div>';
      ov.querySelector('.bk-close').onclick = close;
      ov.classList.add('on');
      ov.scrollTop = 0;
    }
    function close() { ov.classList.remove('on'); }
    btn.addEventListener('click', () => (ov.classList.contains('on') ? close() : open()));
    chip.addEventListener('click', open);
    if (ctr) new MutationObserver(refresh).observe(ctr, { childList: true, characterData: true, subtree: true });
    refresh();
    document.addEventListener('keydown', e => {
      const tag = e.target.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.metaKey || e.ctrlKey || e.altKey) return;
      if (ov.classList.contains('on')) {
        if (e.key === 'Escape' || e.key.toLowerCase() === 'k') { e.preventDefault(); e.stopImmediatePropagation(); close(); }
        else if (!['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '].includes(e.key)) e.stopImmediatePropagation();
        return;
      }
      if (e.key.toLowerCase() === 'k' && !overlayOpen()) { e.preventDefault(); e.stopImmediatePropagation(); open(); }
    }, true);
  }).catch(() => {});
})();
