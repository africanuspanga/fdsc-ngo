"""Helpers shared by the website build and the company-profile build: icons, logo SVGs,
the dot-matrix Tanzania map and the QR code."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOGO_DIR = os.path.join(ROOT, "brand", "logo", "svg")

# 24x24 line icons (stroke = currentColor)
ICONS = {
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9z"/>',
    "chart": '<path d="M3 21h18"/><path d="M6 17v-4"/><path d="M11 17V9"/><path d="M16 17v-6"/><path d="m4 9 5-4 4 3 7-5"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M15.5 4.6a3.2 3.2 0 0 1 0 6.3"/><path d="M17.5 14.2c2.1.7 3.5 2.9 3.5 5.8"/>',
    "building": '<path d="M3 21h18"/><path d="M5 21V8l7-4 7 4v13"/><path d="M9 11h.01M15 11h.01M9 15h.01M15 15h.01"/><path d="M10.5 21v-3h3v3"/>',
    "spark": '<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.6.5 1.1 1.3 1.1 2.1V16h5v-.1c0-.8.5-1.6 1.1-2.1A6 6 0 0 0 12 3z"/>',
    "data": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7"/><path d="M3 13h18"/>',
    "leaf": '<path d="M20 4C11 4 5 8.5 5 15.5V20h4.5C16.5 20 20 13 20 4z"/><path d="M5 20 14 11"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "arrow-up-right": '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    "phone": '<path d="M5 4h3.5l1.8 4.6-2.3 1.4a11 11 0 0 0 6 6l1.4-2.3L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5A16 16 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "download": '<path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "whatsapp": '<path d="M4 20l1.3-4A8 8 0 1 1 8.2 19z"/><path d="M9 9.2c.2 2.6 2.6 5 5.4 5.6l1.2-1.4-1.8-1-1 .8a4.3 4.3 0 0 1-2.2-2.2l.8-1-1-1.8z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "quote": '<path d="M9 7H6a2 2 0 0 0-2 2v3h4v5H4"/><path d="M20 7h-3a2 2 0 0 0-2 2v3h4v5h-4"/>',
}


def icon(name, cls="ic", size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def logo_svg(fn, cls="logo", label=True):
    """Inline one of the brand/logo/svg files (minus its <title>)."""
    s = open(os.path.join(LOGO_DIR, fn)).read().strip()
    s = re.sub(r"<title>.*?</title>", "", s)
    if not label:
        s = s.replace('role="img" aria-label="FDSC - Frontline Development Services Consulting"', 'aria-hidden="true"')
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)


# ---- dot-matrix map -----------------------------------------------------------------------
_MAP = json.load(open(os.path.join(HERE, "tz_map.json")))


def _polys(d):
    out = []
    for part in d.split("M")[1:]:
        pts = [tuple(map(float, p.split())) for p in part.rstrip("Z").split("L")]
        out.append(pts)
    return out


_REG = {k: _polys(v["d"]) for k, v in _MAP["regions"].items()}


def _inside(x, y, poly):
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def _region_at(x, y):
    for name, polys in _REG.items():
        for p in polys:
            if _inside(x, y, p):
                return name
    return None


CITIES = {"Dar es Salaam": (39.28, -6.82), "Dodoma": (35.74, -6.17), "Arusha": (36.68, -3.37),
          "Mwanza": (32.90, -2.52), "Mbeya": (33.46, -8.90), "Kigoma": (29.63, -4.88),
          "Zanzibar": (39.20, -6.16), "Songea": (35.65, -10.68), "Moshi": (37.34, -3.35)}


def project(lon, lat):
    p = _MAP["proj"]
    return (lon - p["lon0"]) * p["kx"] * p["scale"], (p["lat1"] - lat) * p["scale"]


def dot_map(on, step=9.0, dot=5.2, cls="tzmap", cities=None, outline=False, island_boost=True):
    """SVG of Tanzania as a hex grid of dots. `on` = set of region names to highlight.
    Dots are drawn as zero-length round-capped strokes, one path per state (small file)."""
    vb = _MAP["viewBox"]
    w, h = map(float, vb.split()[2:])
    on_d, off_d = [], []
    row = 0
    y = step / 2
    while y < h:
        x = step / 2 + (step / 2 if row % 2 else 0)
        while x < w:
            r = _region_at(x, y)
            if r:
                (on_d if r in on else off_d).append(f"M{x:.1f} {y:.1f}h0")
            x += step
        y += step * 0.866
        row += 1
    # the islands are too small for the grid: draw their outlines as solid shapes
    islands = ""
    if island_boost:
        for name in ("Zanzibar North", "Zanzibar South & Central", "Zanzibar Urban/West", "North Pemba", "South Pemba"):
            st = "on" if name in on else "off"
            islands += f'<path class="isl {st}" d="{_MAP["regions"][name]["d"]}"/>'
    lines = ""
    if outline:
        lines = "".join(f'<path class="rb" d="{v["d"]}"/>' for v in _MAP["regions"].values())
    labels = ""
    for name in (cities or []):
        cx, cy = project(*CITIES[name])
        left = name in ("Dar es Salaam", "Zanzibar")          # coastal: label inland
        tx = cx - 9 if left else cx + 9
        labels += (f'<g class="city"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2"/>'
                   f'<text x="{tx:.1f}" y="{cy + 4.5:.1f}" text-anchor="{"end" if left else "start"}">{name}</text></g>')
    return (f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="Map of Tanzania showing the regions where FDSC has worked">'
            f'{lines}<path class="dots off" stroke-width="{dot}" d="{"".join(off_d)}"/>'
            f'<path class="dots on" stroke-width="{dot}" d="{"".join(on_d)}"/>{islands}{labels}</svg>')


def qr_svg(url, cls="qr", dark="#0B1F3A"):
    import io
    import segno
    q = segno.make(url, error="m")
    w, h = q.symbol_size(border=0)
    buf = io.BytesIO()
    q.save(buf, kind="svg", dark=dark, light=None, border=0, scale=1, xmldecl=False, svgns=True, nl=False)
    path = re.search(r"<path[^>]+/>", buf.getvalue().decode()).group(0)
    return (f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges" role="img" aria-label="QR code: {url}">{path}</svg>')
