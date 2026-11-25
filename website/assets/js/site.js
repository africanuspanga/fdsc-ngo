/* FDSC website - small progressive enhancements. Everything works without JS. */
(function () {
  var d = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // analytics events: only sent when Vercel Web Analytics is switched on (see ANALYTICS in _src/build.py)
  var track = function (name, data) { if (window.va) window.va('event', { name: name, data: data }); };

  // UTM parameters from the landing URL are kept for the visit and added to enquiries
  var utm = {};
  try {
    var qs = new URLSearchParams(window.location.search);
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function (k) { if (qs.get(k)) utm[k] = qs.get(k).slice(0, 100); });
    if (Object.keys(utm).length) sessionStorage.setItem('fdsc_utm', JSON.stringify(utm));
    else utm = JSON.parse(sessionStorage.getItem('fdsc_utm') || '{}');
  } catch (err) { utm = {}; }

  // header border on scroll + back-to-top button
  var top = d.querySelector('.top'), totop = d.querySelector('.totop');
  var onScroll = function () {
    var y = window.scrollY;
    if (top) top.classList.toggle('scrolled', y > 8);
    if (totop) totop.classList.toggle('show', y > window.innerHeight * 1.5);
  };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    var brand = d.querySelector('.brand'); if (brand) brand.focus({ preventScroll: true });
  });

  // mobile menu: Esc closes, focus stays inside while open, returns to the button on close
  var btn = d.querySelector('.menu-btn'), nav = d.getElementById('mnav');
  if (btn && nav) {
    var isOpen = function () { return nav.classList.contains('open'); };
    var setOpen = function (open, restoreFocus) {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
      btn.querySelector('.i-open').hidden = open; btn.querySelector('.i-close').hidden = !open;
      d.body.style.overflow = open ? 'hidden' : '';
      if (open) { var first = nav.querySelector('a'); if (first) setTimeout(function () { first.focus(); }, 50); }
      else if (restoreFocus) btn.focus();
    };
    btn.addEventListener('click', function () { setOpen(!isOpen(), true); });
    d.addEventListener('keydown', function (e) {
      if (!isOpen()) return;
      if (e.key === 'Escape') { setOpen(false, true); return; }
      if (e.key !== 'Tab') return;
      var items = [btn].concat([].slice.call(nav.querySelectorAll('a')));
      var i = items.indexOf(d.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && (i === items.length - 1 || i === -1)) { e.preventDefault(); items[0].focus(); }
    });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false, false); }); });
    window.addEventListener('resize', function () { if (isOpen() && window.innerWidth > 1020) setOpen(false, false); });
  }

  // tabs (sectors)
  d.querySelectorAll('[data-tabs]').forEach(function (wrap) {
    var tabs = wrap.querySelectorAll('[role="tab"]');
    var select = function (t) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
        d.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); n.focus(); select(n); }
      });
    });
  });

  // assignment record filter + search
  var rec = d.getElementById('record-list');
  if (rec) {
    var items = rec.querySelectorAll('.rec'), fbtns = d.querySelectorAll('.fbtn'), q = d.getElementById('q');
    var empty = d.getElementById('rec-empty'), count = d.getElementById('rec-count');
    var type = 'all';
    var apply = function () {
      var term = (q && q.value || '').trim().toLowerCase(), shown = 0;
      items.forEach(function (li) {
        var ok = (type === 'all' || li.dataset.type === type) && (!term || li.textContent.toLowerCase().indexOf(term) > -1);
        li.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = shown + (shown === 1 ? ' assignment' : ' assignments');
    };
    fbtns.forEach(function (b) {
      b.addEventListener('click', function () {
        type = b.dataset.type;
        fbtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        apply();
      });
    });
    if (q) q.addEventListener('input', apply);
  }

  // contact form -> checks the fields, then opens the visitor's email app addressed to FDSC (no server needed)
  var form = d.getElementById('enquiry');
  if (form) {
    var msgs = {
      name: 'Please enter your name.',
      email: 'Please enter your email address so we can reply.',
      emailBad: 'This email address looks incomplete. Please check it, for example name@organisation.org.',
      message: 'Please tell us briefly how we can help.'
    };
    var setErr = function (el, text) {
      var box = d.getElementById(el.id + '-err');
      if (box) box.textContent = text || '';
      if (text) { el.setAttribute('aria-invalid', 'true'); el.setAttribute('aria-describedby', el.id + '-err'); }
      else { el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby'); }
    };
    var check = function (el) {
      var v = el.value.trim();
      if (el.name === 'email') {
        el.value = v;
        if (!v) return setErr(el, msgs.email), false;
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return setErr(el, msgs.emailBad), false;
      } else if (el.required && !v) return setErr(el, msgs[el.name]), false;
      setErr(el, ''); return true;
    };
    // checked on submit, then live while the visitor fixes a field (no blur check: a message appearing on blur
    // pushes the Send button down and swallows the click)
    var req = form.querySelectorAll('[required]');
    req.forEach(function (el) {
      el.addEventListener('input', function () { if (el.hasAttribute('aria-invalid')) check(el); });
    });

    var lastBody = '';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = null;
      req.forEach(function (el) { if (!check(el) && !bad) bad = el; });
      if (bad) { bad.focus(); return; }
      var f = new FormData(form), g = function (k) { return String(f.get(k) || '').trim(); };
      var subject = 'Enquiry: ' + (g('service') || 'General') + ' - ' + (g('org') || g('name'));
      var lines = [
        'Name: ' + g('name'),
        'Organisation: ' + (g('org') || '-'),
        'Email: ' + g('email'),
        'Phone: ' + (g('phone') || '-'),
        'Service: ' + (g('service') || '-'),
        '', g('message')
      ];
      var src = Object.keys(utm).map(function (k) { return k.replace('utm_', '') + '=' + utm[k]; }).join(', ');
      if (src) lines.push('', '(Found FDSC via: ' + src + ')');
      lastBody = 'To: ' + form.dataset.to + '\nSubject: ' + subject + '\n\n' + lines.join('\n');
      track('Enquiry form', { service: g('service') || 'General' });
      window.location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      var note = d.getElementById('form-note');
      if (note) note.textContent = 'Your email app should now be open with the message ready. Press send there to reach us.';
      var fb = d.getElementById('form-fb'); if (fb) fb.hidden = false;
    });

    var copyBtn = d.getElementById('copy-msg');
    if (copyBtn) copyBtn.addEventListener('click', function () {
      var label = copyBtn.querySelector('span');
      var done = function (ok) {
        label.textContent = ok ? 'Copied. Paste it into a new email' : 'Copy failed. Please select and copy your message';
        setTimeout(function () { label.textContent = 'Copy message'; }, 4000);
      };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(lastBody).then(function () { done(true); }, function () { done(false); });
      else {
        var ta = d.createElement('textarea'); ta.value = lastBody; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
        d.body.appendChild(ta); ta.select();
        var ok = false; try { ok = d.execCommand('copy'); } catch (err) { ok = false; }
        d.body.removeChild(ta); done(ok);
      }
    });
  }

  // conversion events for calls, WhatsApp, email, proposal buttons and PDF downloads
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href');
    if (h.indexOf('tel:') === 0) track('Call');
    else if (h.indexOf('wa.me') > -1) track('WhatsApp');
    else if (h.indexOf('mailto:') === 0) track('Email');
    else if (/\.pdf$/.test(h)) track('Profile download');
    else if (/contact\.html$/.test(h) && a.classList.contains('btn')) track('Proposal button', { page: location.pathname });
  });

  // reveal on scroll
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  var y = d.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
