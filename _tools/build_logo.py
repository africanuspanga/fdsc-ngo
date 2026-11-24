"""Rebuilds the FDSC logo as clean vectors from the only source we have (a 454 x 355 px JPEG
embedded in the client's Word profile: _research/extracted/logoA-000.jpg).

How each part is made:
  * Red disc   - an exact circle fitted (least squares) to the disc edge.
  * S swoosh   - traced at 8x from the JPEG: white inside the disc, red tails outside it.
                 Disc + swoosh are written as one path with fill-rule="evenodd", so the S is a
                 true cut-out (works on any background, no masks).
  * F          - redrawn from measured rectangles with round ends.
  * D, C       - traced at 8x (organic curves in the original lettering).
  * Tagline    - set in Arial and converted to outlines, word by word at the measured positions
                 (keeps the gap in "Develo pment" where the swoosh tail passes through).

Run:  python3 _tools/build_logo.py      (needs: pip install potracer pillow numpy fonttools)
Writes SVGs to brand/logo/svg/. Then run _tools/export_logo.py for PNG/WebP.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
import potrace
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_research", "extracted", "logoA-000.jpg")
OUT = os.path.join(ROOT, "brand", "logo", "svg")
os.makedirs(OUT, exist_ok=True)

RED = "#C23C47"   # sampled median of the disc in the client's file
INK = "#141414"
S = 8             # supersampling factor for tracing

rgb = np.array(Image.open(SRC).convert("RGB")).astype(float)
H, W = rgb.shape[:2]


def up(a, blur):
    im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    im = im.resize((W * S, H * S), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(S * blur))
    return np.array(im).astype(float) / 255


def trace(mask, turd=40, alpha=1.0, tol=0.4):
    """Potrace a boolean mask (True = shape) -> SVG path data in 1x source coordinates."""
    path = potrace.Bitmap(~mask).trace(  # potracer fills False pixels
        turdsize=turd, alphamax=alpha, opticurve=True, opttolerance=tol)
    f = lambda p: f"{p.x / S:.2f} {p.y / S:.2f}"
    parts = []
    for c in path:
        d = [f"M{f(c.start_point)}"]
        for s in c.segments:
            d.append(f"L{f(s.c)}L{f(s.end_point)}" if s.is_corner else f"C{f(s.c1)} {f(s.c2)} {f(s.end_point)}")
        parts.append("".join(d) + "Z")
    return "".join(parts)


R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
red = (R - G > 70) & (R - B > 60)

# ---- 1. disc: least-squares circle on the left/right edges of the red area -------------
pts = []
for y in range(H):
    row = np.where(red[y])[0]
    if len(row) > 40:
        pts += [(row.min() - 0.5, y), (row.max() + 0.5, y)]
pts = np.array(pts, float)


def fit(p):
    A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
    c = np.linalg.lstsq(A, (p ** 2).sum(1), rcond=None)[0]
    return c[0], c[1], np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)


cx, cy, cr = fit(pts)
for _ in range(6):
    d = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - cr)
    pts = pts[d < 1.5]
    cx, cy, cr = fit(pts)
print(f"disc centre ({cx:.2f}, {cy:.2f}) r {cr:.2f}")

# ---- 2. swoosh --------------------------------------------------------------------------
# Body (inside the disc): whiteness, smoothed to remove JPEG noise, then carried radially out to
# the disc edge so it meets the tails cleanly.
# Tails (outside the disc): too thin to trace from a 454 px JPEG, so each is rebuilt as a tapered
# stroke along a centreline measured from the redness centroids (see _research notes in README).
from PIL import ImageDraw

whiteness = np.clip((G - 60) / 195.0, 0, 1)
wu = up(whiteness, 0.85)
yy, xx = np.mgrid[0:H * S, 0:W * S]
px, py = (xx + 0.5) / S, (yy + 0.5) / S
dist = np.hypot(px - cx, py - cy)
ang = np.arctan2(py - cy, px - cx)
EDGE = 2.0                                   # rim width where the JPEG blends red/white
body = (wu > 0.5) & (dist < cr - EDGE)
ring = (dist >= cr - EDGE) & (dist < cr)
sx = np.clip(((cx + (cr - EDGE - 0.2) * np.cos(ang)) * S).astype(int), 0, W * S - 1)
sy = np.clip(((cy + (cr - EDGE - 0.2) * np.sin(ang)) * S).astype(int), 0, H * S - 1)
body[ring] = (wu[sy, sx] > 0.5)[ring]


def catmull(points, n=24):
    """Smooth centreline through the given points (Catmull-Rom, endpoints repeated)."""
    P = np.array(points, float)
    P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2])
    return np.array(out)


def tapered(points, widths):
    """Polygon for a stroke along `points` whose width falls from widths[0] to a sharp tip."""
    c = catmull(points)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
    t = seg / seg[-1]
    wt = np.interp(t, np.linspace(0, 1, len(widths)), widths)
    tang = np.gradient(c, axis=0)
    tang /= np.hypot(tang[:, 0], tang[:, 1])[:, None]
    nrm = np.c_[-tang[:, 1], tang[:, 0]]
    left, right = c + nrm * wt[:, None] / 2, c - nrm * wt[:, None] / 2
    return np.vstack([left, right[::-1]])


# centrelines measured on the source (1x px), from inside the disc edge out to the tip
TAIL_BL = [(205.0, 214.0), (200.3, 222.0), (192.3, 231.0), (184.0, 239.5), (177.2, 248.0),
           (171.4, 256.0), (167.0, 263.0), (161.8, 271.5)]
TAIL_BL_W = [5.2, 6.2, 5.6, 4.6, 3.4, 2.2, 1.3, 0.0]
TAIL_TR = [(317.0, 63.5), (324.0, 61.2), (332.0, 59.6), (340.0, 58.0), (348.0, 56.0), (356.0, 54.0),
           (362.0, 52.6)]
TAIL_TR_W = [3.6, 4.0, 3.6, 2.6, 1.7, 0.9, 0.0]

tails = Image.new("L", (W * S, H * S), 0)
dr = ImageDraw.Draw(tails)
for pts, ws in ((TAIL_BL, TAIL_BL_W), (TAIL_TR, TAIL_TR_W)):
    poly = tapered(pts, ws) * S
    dr.polygon([tuple(v) for v in poly], fill=255)
tails = np.array(tails) > 127
# Red layer = disc minus the S channel, plus the tails (allowed to tuck under the disc edge but never
# into the channel). Built as one clean 8x raster and traced once, so the disc edge and the tails
# join without slivers. The S is a real hole in the path (transparent on any background).
red_layer = ((dist < cr) & ~body) | (tails & ~body & (dist >= cr - 2.5))
sm = Image.fromarray((red_layer * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(S * 0.22))
MARK_D = trace(np.array(sm) > 127, turd=60, alpha=1.25, tol=0.3)


# ---- 3. letters ------------------------------------------------------------------------
# D and C are monoline strokes (10 px). Tracing their edges picks up 8 px JPEG block ripples, so
# instead: cast rays from the bowl centre, take the midpoint between the inner and outer edge on
# each ray (the centreline), smooth it, and redraw a clean constant-width stroke with round ends.
dark = np.clip((150 - (R + G + B) / 3) / 120.0, 0, 1) * (~red)
du = up(dark, 0.4)


du[:, : int(72 * S)] = 0          # keep the F out of the D's ray scan


def val(x, y):
    return du[np.clip((y * S).astype(int), 0, H * S - 1), np.clip((x * S).astype(int), 0, W * S - 1)]


def centreline(c, a0, a1, step=0.5, wmin=7.5, wmax=12.5, rmin=18, rmax=62, smooth=6.0):
    rs = np.arange(rmin, rmax, 0.04)
    out = []
    for a in np.radians(np.arange(a0, a1, step)):
        v = (val(c[0] + rs * np.cos(a), c[1] + rs * np.sin(a)) > 0.5).astype(int)
        ins, outs = np.where(np.diff(v) == 1)[0], np.where(np.diff(v) == -1)[0]
        if len(ins) and len(outs) and outs[-1] > ins[-1]:     # outermost stroke on this ray
            r0, r1 = rs[ins[-1]], rs[outs[-1]]
            if wmin < r1 - r0 < wmax:
                out.append((a, (r0 + r1) / 2, r1 - r0))
    A = np.array(out)
    # rays that cross the D stem junction are rejected; fill those gaps by interpolation
    full = np.radians(np.arange(np.degrees(A[0, 0]), np.degrees(A[-1, 0]) + step / 2, step))
    A = np.c_[full, np.interp(full, A[:, 0], A[:, 1]), np.interp(full, A[:, 0], A[:, 2])]
    k = np.exp(-0.5 * (np.arange(-30, 31) * step / smooth) ** 2); k /= k.sum()
    pad = lambda v: np.r_[np.full(30, v[0]), v, np.full(30, v[-1])]
    r = np.convolve(pad(A[:, 1]), k, "valid")
    w = np.convolve(pad(A[:, 2]), k, "valid")
    pts = np.c_[c[0] + r * np.cos(A[:, 0]), c[1] + r * np.sin(A[:, 0])]
    return pts, w


def stroke_into(draw, pts, w, cap_start=True, cap_end=True):
    t = np.gradient(pts, axis=0)
    t /= np.hypot(t[:, 0], t[:, 1])[:, None]
    n = np.c_[-t[:, 1], t[:, 0]]
    L, Rr = pts + n * w[:, None] / 2, pts - n * w[:, None] / 2
    draw.polygon([tuple(v * S) for v in np.vstack([L, Rr[::-1]])], fill=255)
    for i, on in ((0, cap_start), (-1, cap_end)):
        if on:
            x, y, rr = pts[i][0] * S, pts[i][1] * S, w[i] / 2 * S
            draw.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)


canvas = Image.new("L", (W * S, H * S), 0)
dr = ImageDraw.Draw(canvas)
# C: centre fitted to its round section; the opening faces right (angles in screen degrees)
c_pts, c_w = centreline((414.27, 159.60), 20, 345)
c_pts = c_pts[5:-5]                      # source terminals stop ~2 px short of the last clean ray
stroke_into(dr, c_pts, np.full(len(c_pts), 10.0))
# D bowl incl. the hook at upper left; ends inside the stem at the bottom
d_pts, d_w = centreline((109.4, 160.4), -150, 108, rmax=50)
stroke_into(dr, d_pts, d_w, cap_start=True, cap_end=False)
# D stem (ruler straight); its foot meets the bowl's outer edge (y 207.6 at x 102)
dr.rectangle([92.2 * S, 122 * S, 102.2 * S, 200 * S], fill=255)
dr.rounded_rectangle([92.2 * S, 190 * S, 102.2 * S, 207.8 * S], radius=1.4 * S, fill=255)
cm = Image.fromarray(np.array(canvas)).filter(ImageFilter.GaussianBlur(S * 0.2))
DC = trace(np.array(cm) > 127, turd=60, alpha=1.2, tol=0.4)
print(f"C centreline {len(c_pts)} pts, D centreline {len(d_pts)} pts, D width {d_w.min():.1f}-{d_w.max():.1f}")
print("D start", np.round(d_pts[:3], 1).tolist(), "D end", np.round(d_pts[-2:], 1).tolist())


def rrect(x0, y0, x1, y1, rl, rr):
    """Horizontal bar with optional round ends (rl/rr = radius or 0)."""
    h = y1 - y0
    d = f"M{x0 + rl:.2f} {y0:.2f}H{x1 - rr:.2f}"
    d += f"A{rr:.2f} {h / 2:.2f} 0 0 1 {x1 - rr:.2f} {y1:.2f}" if rr else f"H{x1:.2f}V{y1:.2f}"
    d += f"H{x0 + rl:.2f}"
    d += f"A{rl:.2f} {h / 2:.2f} 0 0 1 {x0 + rl:.2f} {y0:.2f}" if rl else f"H{x0:.2f}V{y0:.2f}"
    return d + "Z"


# Measured from the source (1x px): stem x 24.0-34.0, top bar y 111.6-121.6 to x 60.4,
# crossbar y 152.2-162.0 from x 14.0 to 70.4, stem bottom (rounded) at y 208.4.
SW_ = 10.0
F = (f"M24.0 111.6H55.4A5 5 0 0 1 55.4 121.6H34.0V203.4A5 5 0 0 1 24.0 203.4Z"
     + rrect(14.0, 152.2, 70.4, 162.2, 5, 5))

# ---- 4. tagline in Arial outlines --------------------------------------------------------
font = TTFont("/System/Library/Fonts/Supplemental/Arial.ttf")
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
upm = font["head"].unitsPerEm
cap = font["OS/2"].sCapHeight

tag = dark[226:270] > 0.5
cols = np.where(tag.any(0))[0]
rows = np.where(tag.any(1))[0] + 226
groups, start = [], cols[0]
for a, b in zip(cols[:-1], cols[1:]):
    if b - a > 4:
        groups.append((start, a)); start = b
groups.append((start, cols[-1]))
# find baseline = most common bottom of the letters in "Frontline" (no descenders)
fr = dark[226:270, groups[0][0]: groups[0][1] + 1] > 0.5
top = rows.min()
base = 226 + np.where(fr.any(1))[0].max() + 1
size_h = (base - top) / (cap / upm)
words = ["Frontline", "Develo", "pment", "Services", "Consulting"]


def ink_extent(text):
    """Ink left/right of a word at 1 unit = 1 font unit, pen starting at x=0."""
    from fontTools.pens.boundsPen import BoundsPen
    x, lo, hi = 0, None, None
    for ch in text:
        g = cmap[ord(ch)]
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            lo = x + bp.bounds[0] if lo is None else min(lo, x + bp.bounds[0])
            hi = x + bp.bounds[2] if hi is None else max(hi, x + bp.bounds[2])
        x += hmtx[g][0]
    return lo, hi


fits = [((g1 + 1 - g0) / (ink_extent(w)[1] - ink_extent(w)[0])) * upm for w, (g0, g1) in zip(words, groups)]
size_w = float(np.median(fits))
print("tagline word boxes", groups, "cap top", top, "baseline", base)
print(f"size from cap height {size_h:.2f}px, from word widths {size_w:.2f}px ({[round(f, 2) for f in fits]})")
SX = SY = size_w / upm   # Arial; widths fit within 0.4%. Centre the caps on the measured cap band:
base = (top + base) / 2 + cap * SY / 2


def word_path(text, x_left):
    pen = SVGPathPen(gs)
    lo, _ = ink_extent(text)
    x = x_left - lo * SX
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (SX, 0, 0, -SY, x, base)))
        x += hmtx[g][0] * SX
    return pen.getCommands()


TAG = ""
for wtxt, (g0, g1) in zip(words, groups):
    TAG += word_path(wtxt, g0)

INK_D = F + DC

# ---- 5. write the logo family ---------------------------------------------------------
# bounding boxes (1x px) incl. tails: full logo ~ x 7-447, y 40-262
def svg(vb, body, title="FDSC - Frontline Development Services Consulting"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{body}</svg>\n")


def p(d, fill, evenodd=False):
    return f'<path fill="{fill}"{" fill-rule=\"evenodd\"" if evenodd else ""} d="{d}"/>'


PAD = 6


def bbox(mask):
    ys, xs = np.where(mask)
    return xs.min() / S, ys.min() / S, (xs.max() + 1) / S, (ys.max() + 1) / S


rx0, ry0, rx1, ry1 = bbox(np.array(sm) > 127)          # disc + tails
lx0, ly0, lx1, ly1 = bbox(np.array(cm) > 127)          # D + C
print(f"mark bbox {rx0:.1f},{ry0:.1f} - {rx1:.1f},{ry1:.1f}; D/C bbox {lx0:.1f},{ly0:.1f} - {lx1:.1f},{ly1:.1f}")
X0, X1 = 7.0, max(lx1, 447.0)                          # tagline starts at x 7; C ends ~449
FULL_VB = f"{X0 - PAD:.2f} {ry0 - PAD:.2f} {X1 - X0 + 2 * PAD:.2f} {max(ry1, 262) - ry0 + 2 * PAD:.2f}"
WORD_VB = f"{14 - PAD:.2f} {ry0 - PAD:.2f} {X1 - 14 + 2 * PAD:.2f} {ry1 - ry0 + 2 * PAD:.2f}"
MARK_VB = f"{rx0 - 3:.2f} {ry0 - 3:.2f} {rx1 - rx0 + 6:.2f} {ry1 - ry0 + 6:.2f}"
DISC_VB = f"{cx - cr - 3:.2f} {cy - cr - 3:.2f} {2 * cr + 6:.2f} {2 * cr + 6:.2f}"

files = {
    # full lockup with tagline
    "fdsc-logo.svg": svg(FULL_VB, p(MARK_D, RED, True) + p(INK_D + TAG, INK)),
    "fdsc-logo-reversed.svg": svg(FULL_VB, p(MARK_D, RED, True) + p(INK_D + TAG, "#FFFFFF")),
    "fdsc-logo-black.svg": svg(FULL_VB, p(MARK_D, INK, True) + p(INK_D + TAG, INK)),
    "fdsc-logo-white.svg": svg(FULL_VB, p(MARK_D, "#FFFFFF", True) + p(INK_D + TAG, "#FFFFFF")),
    # FDSC letters only (no tagline) - for small sizes, headers, favicons of wide format
    "fdsc-wordmark.svg": svg(WORD_VB, p(MARK_D, RED, True) + p(INK_D, INK)),
    "fdsc-wordmark-reversed.svg": svg(WORD_VB, p(MARK_D, RED, True) + p(INK_D, "#FFFFFF")),
    "fdsc-wordmark-white.svg": svg(WORD_VB, p(MARK_D, "#FFFFFF", True) + p(INK_D, "#FFFFFF")),
    # the S-disc symbol on its own
    "fdsc-mark.svg": svg(MARK_VB, p(MARK_D, RED, True)),
    "fdsc-mark-white.svg": svg(MARK_VB, p(MARK_D, "#FFFFFF", True)),
}
for fn, s in files.items():
    open(os.path.join(OUT, fn), "w").write(s)
    print(f"wrote {fn:<28} {len(s):>6} bytes")

# app icon / favicon: disc filling a rounded square isn't the brand, so use the disc on white
# with the tails clipped to the square.
ICON = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
        f'<clipPath id="r"><rect width="512" height="512" rx="112"/></clipPath>'
        f'<rect width="512" height="512" rx="112" fill="#FFFFFF"/>'
        f'<g clip-path="url(#r)"><g transform="translate(256 248) scale({168 / cr:.4f}) translate({-cx:.2f} {-cy:.2f})">'
        f'{p(MARK_D, RED, True)}</g></g></svg>\n')
open(os.path.join(OUT, "fdsc-app-icon.svg"), "w").write(ICON)
FAV = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{DISC_VB}">'
       f'<clipPath id="c"><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{cr + 3:.2f}"/></clipPath>'
       f'<g clip-path="url(#c)">{p(MARK_D, RED, True)}</g></svg>\n')
open(os.path.join(OUT, "fdsc-favicon.svg"), "w").write(FAV)
print("wrote fdsc-app-icon.svg, fdsc-favicon.svg")
