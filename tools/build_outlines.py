"""Build content/outlines.json for the self-drawn SVG atlas maps (no map API, no tiles).

Sources (public domain, Natural Earth, https://www.naturalearthdata.com):
- ne_10m_admin_0_countries_ind: country outlines as seen from India's point of view
  (so India's borders follow the official Survey of India depiction).
- ne_10m_admin_1_states_provinces: Indian state lines. Lines inside Jammu and Kashmir
  and Ladakh are left out; the national outline above covers that area.

Usage: python tools/build_outlines.py   (downloads the two files into .cache/ on first run)
"""
import json
import sys
sys.setrecursionlimit(100000)
import math
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILES = {"countries": "ne_10m_admin_0_countries_ind.geojson", "states": "ne_10m_admin_1_states_provinces.geojson"}
COUNTRIES = ["India", "Nepal", "Bhutan", "Bangladesh", "Pakistan", "China", "Myanmar", "Sri Lanka", "Afghanistan"]
SKIP_STATES = {"Jammu and Kashmir", "Ladakh"}
BOX = (84.5, 24.0, 94.5, 30.5)  # lng/lat window we ever draw: the Eastern Himalaya


def fetch(name):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / name
    if not p.exists():
        print("downloading", name)
        urllib.request.urlretrieve(BASE + name, p)
    return json.loads(p.read_text(encoding="utf-8"))


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def rings(geom, eps, min_pts=4):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out = []
    for poly in polys:
        ring = poly[0]
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        if max(xs) < BOX[0] or min(xs) > BOX[2] or max(ys) < BOX[1] or min(ys) > BOX[3]:
            continue
        pts = [(round(x, 3), round(y, 3)) for x, y in ring]
        mid = len(pts) // 2  # closed rings start and end on the same point: simplify each half
        simp = rdp(pts[: mid + 1], eps)[:-1] + rdp(pts[mid:], eps)
        if len(simp) >= min_pts:
            out.append(simp)
    return out


def main():
    countries = fetch(FILES["countries"])
    states = fetch(FILES["states"])
    out = {"countries": {}, "states": {}}
    for f in countries["features"]:
        name = f["properties"].get("ADMIN")
        if name in COUNTRIES:
            out["countries"][name] = rings(f["geometry"], 0.004)
    for f in states["features"]:
        p = f["properties"]
        if p.get("admin") == "India" and p.get("name") not in SKIP_STATES:
            out["states"][p["name"]] = rings(f["geometry"], 0.004)
    dest = ROOT / "content" / "outlines.json"
    dest.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    n = sum(len(r) for v in out["countries"].values() for r in v) + sum(len(r) for v in out["states"].values() for r in v)
    print(f"wrote {dest} · {len(out['countries'])} countries · {len(out['states'])} states · {n} points · {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
