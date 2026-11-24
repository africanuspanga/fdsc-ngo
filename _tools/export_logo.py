"""Exports every SVG in brand/logo/svg/ to transparent PNG and WebP (brand/logo/png, brand/logo/webp),
plus favicons. Also writes _research/logo-compare.png (original JPEG vs. new vector, overlaid).

Run:  python3 _tools/export_logo.py      (needs Google Chrome + pip install playwright pillow; cwebp optional)
"""
import os
import re
import subprocess
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, "brand", "logo", "svg")
PNG = os.path.join(ROOT, "brand", "logo", "png")
WEBP = os.path.join(ROOT, "brand", "logo", "webp")
os.makedirs(PNG, exist_ok=True)
os.makedirs(WEBP, exist_ok=True)

WIDTHS = {"fdsc-logo": [600, 1200, 2400], "fdsc-wordmark": [600, 1200, 2400], "fdsc-mark": [256, 512, 1024],
          "fdsc-app-icon": [180, 192, 512, 1024], "fdsc-favicon": [32, 48, 64]}


def render(page, svg_text, width):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]
    h = round(width * vb[3] / vb[2])
    page.set_viewport_size({"width": width + 40, "height": h + 40})
    page.set_content('<html><body style="margin:0;background:transparent">'
                     + svg_text.replace("<svg ", f'<svg id="logo" width="{width}" height="{h}" style="display:block" ', 1)
                     + "</body></html>")
    page.wait_for_timeout(60)
    return Image.open(BytesIO(page.locator("#logo").screenshot(omit_background=True)))


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page()
    for fn in sorted(os.listdir(SVG)):
        if not fn.endswith(".svg"):
            continue
        stem = fn[:-4]
        base = next((k for k in sorted(WIDTHS, key=len, reverse=True) if stem.startswith(k)), None)
        txt = open(os.path.join(SVG, fn)).read()
        for w in WIDTHS.get(base, [1200]):
            im = render(pg, txt, w)
            out = os.path.join(PNG, f"{stem}-{w}.png")
            im.save(out, optimize=True)
            if w == max(WIDTHS.get(base, [1200])) or base in ("fdsc-logo", "fdsc-wordmark"):
                wp = os.path.join(WEBP, f"{stem}-{w}.webp")
                im.save(wp, "WEBP", lossless=True, quality=100, method=6)
        print("exported", stem)

    # favicon.ico (16/32/48) from the favicon SVG
    fav = open(os.path.join(SVG, "fdsc-favicon.svg")).read()
    icos = [render(pg, fav, s) for s in (16, 32, 48)]
    icos[-1].save(os.path.join(PNG, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:-1])

    # comparison sheet: original | new | overlay (new in cyan over original)
    src = Image.open(os.path.join(ROOT, "_research", "extracted", "logoA-000.jpg")).convert("RGB")
    S = 4
    big = src.resize((src.width * S, src.height * S), Image.LANCZOS)
    full = open(os.path.join(SVG, "fdsc-logo.svg")).read()
    full_page = re.sub(r'viewBox="[^"]+"', f'viewBox="0 0 {src.width} {src.height}"', full)
    new = render(pg, full_page, src.width * S)
    new_rgb = Image.new("RGB", new.size, "white")
    new_rgb.paste(new, mask=new.split()[3])
    # overlay: original in grey, new outline in cyan
    grey = big.convert("L").convert("RGB")
    over = Image.blend(grey, new_rgb, 0.5)
    sheet = Image.new("RGB", (big.width * 3 + 40, big.height), "white")
    sheet.paste(big, (0, 0)); sheet.paste(new_rgb, (big.width + 20, 0)); sheet.paste(over, (2 * big.width + 40, 0))
    sheet.save(os.path.join(ROOT, "_research", "logo-compare.png"))
    b.close()
print("done")
