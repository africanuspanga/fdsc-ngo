"""Serves website/ locally, screenshots every page (desktop + phone) and reports problems:
horizontal overflow, console errors, broken images, tap targets under 44px on phones.

Run:  python3 _tools/check_site.py [--shots]     (screenshots go to _research/site-shots/)
"""
import functools
import http.server
import os
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "website")
SHOTS = os.path.join(ROOT, "_research", "site-shots")
PAGES = ["index.html", "about.html", "services.html", "work.html", "contact.html", "404.html"]
VIEWS = {"desktop": {"width": 1440, "height": 900}, "phone": {"width": 390, "height": 844}, "small": {"width": 320, "height": 640}}

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
handler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
shots = "--shots" in sys.argv
os.makedirs(SHOTS, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for vname, vp in VIEWS.items():
        ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=vname != "desktop", has_touch=vname != "desktop")
        for page in PAGES:
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda ex: errs.append(str(ex)))
            pg.goto(BASE + page, wait_until="networkidle")
            # reveal everything for screenshots
            pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            pg.wait_for_timeout(500)
            pg.evaluate("window.scrollTo(0, 0)")
            res = pg.evaluate("""() => {
              const out = {};
              out.overflow = document.documentElement.scrollWidth - window.innerWidth;
              out.broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src.split('/').pop());
              if (window.innerWidth < 500) {
                out.small = [...document.querySelectorAll('a,button,input,select,textarea')].filter(el => {
                  const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
                  if (!r.width || cs.visibility === 'hidden' || el.closest('[hidden]') || el.closest('.marquee') || el.closest('.mnav:not(.open)')) return false;
                  if (el.closest('p') || el.closest('.foot ul') || el.closest('.crumbs') || el.closest('.foot__bar')) return false; // inline text links
                  return r.height < 44;
                }).map(el => (el.textContent || el.name || el.tagName).trim().slice(0, 30));
                const wide = [...document.querySelectorAll('body *')].filter(el => el.getBoundingClientRect().right > window.innerWidth + 1 && !el.closest('.marquee') && !el.closest('.mnav') && !el.classList.contains('phead__mark') && getComputedStyle(el).position !== 'fixed');
                out.wide = wide.slice(0, 5).map(el => el.tagName + '.' + el.className);
              }
              return out;
            }""")
            flag = []
            if res["overflow"] > 0: flag.append(f"h-overflow {res['overflow']}px")
            if res["broken"]: flag.append(f"broken img {res['broken']}")
            if res.get("small"): flag.append(f"small targets {res['small'][:6]}")
            if res.get("wide"): flag.append(f"wide {res['wide']}")
            if errs: flag.append(f"console {errs[:3]}")
            print(f"{vname:<7} {page:<14} {'OK' if not flag else ' | '.join(flag)}")
            if shots:
                pg.screenshot(path=os.path.join(SHOTS, f"{vname}-{page[:-5]}.png"), full_page=True)
            pg.close()
        ctx.close()
    b.close()
srv.shutdown()
