"""Serves website/ locally WITH the security headers from website/vercel.json, screenshots every page
(desktop + phone) and reports problems: horizontal overflow, console errors (including CSP violations),
broken images, tap targets under 44px on phones, heading levels that skip, and broken internal links/anchors.

Run:  python3 _tools/check_site.py [--shots]     (screenshots go to _research/site-shots/)
"""
import functools
import http.server
import json
import os
import re
import sys
import threading
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "website")
SHOTS = os.path.join(ROOT, "_research", "site-shots")
PAGES = ["index.html", "about.html", "services.html", "work.html", "contact.html", "privacy.html", "404.html"]
VIEWS = {"desktop": {"width": 1440, "height": 900}, "phone": {"width": 390, "height": 844}, "small": {"width": 320, "height": 640}}

# headers that apply to every path in vercel.json ("/(.*)")
VJ = json.load(open(os.path.join(SITE, "vercel.json")))
ALL_HEADERS = [h for rule in VJ.get("headers", []) if rule["source"] == "/(.*)" for h in rule["headers"]]


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        for h in ALL_HEADERS:
            self.send_header(h["key"], h["value"])
        super().end_headers()

    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=SITE))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
shots = "--shots" in sys.argv
os.makedirs(SHOTS, exist_ok=True)


def check_links():
    """Every internal href points at a file that exists, and every #anchor exists on its page."""
    ids = {p: set(re.findall(r'\sid="([^"]+)"', open(os.path.join(SITE, p)).read())) for p in PAGES}
    bad = []
    for p in PAGES:
        for href in re.findall(r'href="([^"]+)"', open(os.path.join(SITE, p)).read()):
            u = urlparse(href)
            if u.scheme in ("http", "https", "mailto", "tel") or href.startswith("//"):
                continue
            path = u.path.lstrip("/") or (p if href.startswith("#") else "index.html")
            if not os.path.exists(os.path.join(SITE, path)):
                bad.append(f"{p}: {href} (missing file)")
            elif u.fragment and path in ids and u.fragment not in ids[path]:
                bad.append(f"{p}: {href} (missing anchor)")
    return bad


links = check_links()
print("internal links", "OK" if not links else links)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for vname, vp in VIEWS.items():
        ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=vname != "desktop", has_touch=vname != "desktop")
        for page in PAGES:
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
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
              let last = 0; out.skips = [];
              document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
                const n = +h.tagName[1];
                if (last && n > last + 1) out.skips.push(`h${last}->h${n} "${h.textContent.trim().slice(0, 24)}"`);
                last = n;
              });
              out.h1 = document.querySelectorAll('h1').length;
              if (window.innerWidth < 500) {
                out.small = [...document.querySelectorAll('a,button,input,select,textarea,summary')].filter(el => {
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
            if res["h1"] != 1: flag.append(f"{res['h1']} h1")
            if res["skips"]: flag.append(f"heading skips {res['skips'][:3]}")
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
