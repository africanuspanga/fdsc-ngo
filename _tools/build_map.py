"""Turns the Tanzania region boundaries (geoBoundaries ADM1, OpenStreetMap data, ODbL) into compact
SVG paths: website/_src/tz_map.json  {"viewBox": "...", "regions": {name: {"d": ..., "cx":, "cy":}}}

Source file: _research/geo/tza-adm1.geojson (2015 boundaries: Songwe is still part of Mbeya).
Run:  python3 _tools/build_map.py
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_research", "geo", "tza-adm1.geojson")
OUT = os.path.join(ROOT, "website", "_src", "tz_map.json")

W = 600.0          # output width in SVG units
TOL = 0.012        # Douglas-Peucker tolerance in degrees (~1.3 km)


def dp(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return dp(pts[: idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]


g = json.load(open(SRC))
rings = {}
for f in g["features"]:
    name = f["properties"]["shapeName"]
    geom = f["geometry"]
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    rings[name] = [poly[0] for poly in polys]  # outer rings only (no lakes cut out)

lons = [p[0] for rs in rings.values() for r in rs for p in r]
lats = [p[1] for rs in rings.values() for r in rs for p in r]
lon0, lon1, lat0, lat1 = min(lons), max(lons), min(lats), max(lats)
kx = math.cos(math.radians((lat0 + lat1) / 2))
scale = W / ((lon1 - lon0) * kx)
H = (lat1 - lat0) * scale


def proj(p):
    return ((p[0] - lon0) * kx * scale, (lat1 - p[1]) * scale)


def simplify_ring(r, tol):
    """Douglas-Peucker on a closed ring: split at the point farthest from the start first."""
    pts = [tuple(p) for p in r]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    k = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
    return dp(pts[: k + 1], tol)[:-1] + dp(pts[k:] + [pts[0]], tol)[:-1]


out = {}
for name, rs in rings.items():
    parts, area_sum, cx_sum, cy_sum = [], 0, 0, 0
    for r in rs:
        s = simplify_ring(r, TOL)
        if len(s) < 4:                      # tiny islands: keep a finer outline
            s = simplify_ring(r, TOL / 6)
        if len(s) < 3:
            continue
        xy = [proj(p) for p in s]
        a = cx = cy = 0                     # polygon centroid (for labels / dots)
        for (x0, y0), (x1, y1) in zip(xy, xy[1:] + xy[:1]):
            c = x0 * y1 - x1 * y0
            a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
        if abs(a) > 1e-9:
            area_sum += a / 2; cx_sum += cx / 6; cy_sum += cy / 6
        parts.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in xy) + "Z")
    if not parts:
        print("skipped (no outline):", name)
        continue
    out[name] = {"d": "".join(parts), "cx": round(cx_sum / area_sum, 1), "cy": round(cy_sum / area_sum, 1)}

json.dump({"viewBox": f"0 0 {W:.0f} {H:.0f}", "proj": {"lon0": lon0, "lat1": lat1, "kx": kx, "scale": scale}, "regions": out}, open(OUT, "w"), separators=(",", ":"))
print(f"{len(out)} regions, viewBox 0 0 {W:.0f} {H:.0f}, {os.path.getsize(OUT) / 1024:.0f} KB -> {OUT}")
