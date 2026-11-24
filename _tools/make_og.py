"""Renders the social share image (1200x630) -> website/assets/brand/og-image.jpg
Run after the website build:  python3 _tools/make_og.py   (needs Google Chrome + playwright)"""
import os
import sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "website")
sys.path.insert(0, os.path.join(SITE, "_src"))
import content as C  # noqa: E402
from shared import dot_map  # noqa: E402

html = f"""<html><head><link rel="stylesheet" href="file://{SITE}/assets/fonts/fonts.css"><style>
body{{margin:0;width:1200px;height:630px;overflow:hidden;font-family:'Space Grotesk';color:#fff;
background:radial-gradient(70% 90% at 100% 100%,rgba(255,255,255,.16),transparent 60%),linear-gradient(135deg,#C23C47,#962733)}}
.l{{position:absolute;left:72px;top:64px;width:250px}}
h1{{position:absolute;left:72px;top:236px;width:600px;margin:0;font-weight:400;font-size:58px;line-height:1.02;letter-spacing:-.03em}}
h1 span{{color:#FFE3E6}}
p{{position:absolute;left:72px;bottom:58px;margin:0;font-size:22px;color:rgba(255,255,255,.85)}}
.m{{position:absolute;right:40px;top:50px;width:470px}}
.m .dots{{fill:none;stroke-linecap:round}}.m .dots.off{{stroke:rgba(255,255,255,.28)}}.m .dots.on{{stroke:#fff}}
.m .isl.on{{fill:#fff}}.m .isl.off{{fill:rgba(255,255,255,.28)}}
</style></head><body>
<img class="l" src="file://{SITE}/assets/brand/fdsc-logo-white.svg">
<h1>Turning strategy into <span>measurable results.</span></h1>
<p>Development consulting in Tanzania &middot; www.{C.FIRM['domain']}</p>
<div class="m">{dot_map(C.worked_regions(), step=9, dot=5.6, cls='tz')}</div>
</body></html>"""
tmp = os.path.join(ROOT, "_research", "og.html")
open(tmp, "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto("file://" + tmp)
    pg.wait_for_timeout(600)
    out = os.path.join(SITE, "assets", "brand", "og-image.jpg")
    pg.screenshot(path=out, type="jpeg", quality=88)
    b.close()
print("wrote", out)
