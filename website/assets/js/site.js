/* FDSC website - small progressive enhancements. Everything works without JS. */
(function () {
  var d = document;

  // header border on scroll
  var top = d.querySelector('.top');
  var onScroll = function () { if (top) top.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // mobile menu
  var btn = d.querySelector('.menu-btn'), nav = d.getElementById('mnav');
  if (btn && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('.i-open').hidden = open; btn.querySelector('.i-close').hidden = !open;
      d.body.style.overflow = open ? 'hidden' : '';
    };
    btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
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

  // contact form -> opens the visitor's email app, addressed to FDSC (no server needed)
  var form = d.getElementById('enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var f = new FormData(form);
      var subject = 'Enquiry: ' + (f.get('service') || 'General') + ' - ' + (f.get('org') || f.get('name'));
      var body = [
        'Name: ' + f.get('name'),
        'Organisation: ' + (f.get('org') || '-'),
        'Email: ' + f.get('email'),
        'Phone: ' + (f.get('phone') || '-'),
        'Service: ' + (f.get('service') || '-'),
        '', f.get('message')
      ].join('\n');
      window.location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var note = d.getElementById('form-note');
      if (note) note.textContent = 'Your email app should open with the message ready to send. If it does not, email ' + form.dataset.to + ' directly.';
    });
  }

  // reveal on scroll
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  var y = d.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
