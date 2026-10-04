"""Self-drawn SVG atlas maps. No map API, no tiles, no third-party requests.

Outlines come from content/outlines.json (Natural Earth, public domain; India's
point of view for international borders). Colours come from CSS classes, so each
map takes on its land's palette.
"""
import json
import math
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.utils.html import escape

HIGHLIGHT = {
    "darjeeling": ["West Bengal"],
    "kalimpong": ["West Bengal"],
    "dooars": ["West Bengal"],
    "east-sikkim": ["Sikkim"],
    "north-sikkim": ["Sikkim"],
    "west-sikkim": ["Sikkim"],
}
# name labels drawn on the map when their point falls inside the frame
AREA_LABELS = [("NEPAL", 87.55, 27.55), ("BHUTAN", 90.6, 27.45), ("SIKKIM", 88.62, 27.62), ("TIBET (CHINA)", 89.0, 28.25),
               ("WEST BENGAL", 88.3, 26.35), ("BANGLADESH", 89.2, 25.3), ("ASSAM", 91.3, 26.35)]
HOME_COUNTRIES = ("India", "Bhutan")


@lru_cache(maxsize=1)
def _outlines():
    p = Path(settings.CONTENT_DIR) / "outlines.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"countries": {}, "states": {}}


def _nice(n):
    for v in (10, 20, 25, 50, 100, 200, 250, 500, 1000):
        if v >= n:
            return v
    return 1000


def atlas_svg(points, region=None, route=False, min_span=0.7, legend=True, label_limit=9):
    if isinstance(points, str):
        points = json.loads(points or "[]")
    pts = [p for p in points if p.get("lat") is not None and p.get("lng") is not None]
    if not pts:
        return ""
    lats = [p["lat"] for p in pts]
    lngs = [p["lng"] for p in pts]
    lat_c = (min(lats) + max(lats)) / 2
    k = math.cos(math.radians(lat_c))
    # bounding box in projected units (x = lng*k, y = lat), padded, min span, aspect 1.15–1.75
    x0, x1 = min(lngs) * k, max(lngs) * k
    y0, y1 = min(lats), max(lats)
    span = max(x1 - x0, y1 - y0, min_span)
    pad = span * 0.22
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = max(x1 - x0 + 2 * pad, min_span)
    h = max(y1 - y0 + 2 * pad, min_span * 0.6)
    aspect = w / h
    if aspect < 1.15:
        w = h * 1.15
    elif aspect > 1.75:
        h = w / 1.75
    bx0, bx1, by0, by1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    W = 1000
    H = round(W * h / w)
    s = W / w

    def P(lng, lat):
        return (lng * k - bx0) * s, (by1 - lat) * s

    def inside_ring(ring):
        xs = [x * k for x, _ in ring]
        ys = [y for _, y in ring]
        return not (max(xs) < bx0 or min(xs) > bx1 or max(ys) < by0 or min(ys) > by1)

    def path(rings):
        parts = []
        for ring in rings:
            if not inside_ring(ring):
                continue
            pp = [P(x, y) for x, y in ring]
            parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pp) + "Z")
        return "".join(parts)

    out = _outlines()
    hl_states = set(HIGHLIGHT.get(region, []))
    svg = [f'<svg class="atlas__svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="atlas-t" xmlns="http://www.w3.org/2000/svg">',
           '<title id="atlas-t">Map of ' + escape(", ".join(p["name"] for p in pts[:12])) + "</title>",
           f'<rect class="atlas__sea" width="{W}" height="{H}"/>']
    # graticule
    step = 0.5 if w / k < 3 else (1 if w / k < 7 else 2)
    lng = math.floor(bx0 / k / step) * step
    while lng * k <= bx1:
        x = (lng * k - bx0) * s
        svg.append(f'<line class="atlas__grat" x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H}"/>')
        lng += step
    lat = math.floor(by0 / step) * step
    while lat <= by1:
        y = (by1 - lat) * s
        svg.append(f'<line class="atlas__grat" x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')
        lat += step
    for name, rings in out["countries"].items():
        d = path(rings)
        if d:
            cls = "atlas__land" if name in HOME_COUNTRIES else "atlas__land atlas__land--other"
            if region == "bhutan" and name == "Bhutan":
                cls = "atlas__land atlas__land--hl"
            svg.append(f'<path class="{cls}" d="{d}"><title>{escape(name)}</title></path>')
    for name, rings in out["states"].items():
        d = path(rings)
        if d:
            cls = "atlas__state atlas__state--hl" if name in hl_states else "atlas__state"
            svg.append(f'<path class="{cls}" d="{d}"/>')
    for label, lo, la in AREA_LABELS:
        if bx0 + w * 0.06 < lo * k < bx1 - w * 0.06 and by0 + h * 0.06 < la < by1 - h * 0.06:
            x, y = P(lo, la)
            svg.append(f'<text class="atlas__area" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{escape(label)}</text>')
    # route
    proj = [P(p["lng"], p["lat"]) for p in pts]
    if route and len(proj) > 1:
        svg.append('<polyline class="atlas__route" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in proj) + '"/>')
        route = False
    # nudge overlapping pins apart (true positions stay on the route line)
    proj = [list(xy) for xy in proj]
    for _ in range(40):
        moved = False
        for a in range(len(proj)):
            for b in range(a + 1, len(proj)):
                dx, dy = proj[b][0] - proj[a][0], proj[b][1] - proj[a][1]
                d = math.hypot(dx, dy)
                if d < 34:
                    if d < 0.01:
                        dx, dy, d = 1.0, 0.0, 1.0
                    push = (34 - d) / 2
                    ux, uy = dx / d, dy / d
                    proj[a][0] -= ux * push; proj[a][1] -= uy * push
                    proj[b][0] += ux * push; proj[b][1] += uy * push
                    moved = True
        if not moved:
            break
    proj = [(min(max(x, 18), W - 18), min(max(y, 18), H - 18)) for x, y in proj]
    if route and len(proj) > 1:
        svg.append('<polyline class="atlas__route" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in proj) + '"/>')
    # pins
    show_labels = len(pts) <= label_limit
    for i, ((x, y), p) in enumerate(zip(proj, pts), 1):
        main = " is-main" if p.get("main") else ""
        label = escape(p["name"])
        svg.append(f'<a href="{escape(p.get("url", "#"))}" class="atlas__pin{main}" data-n="{i}"><title>{label}</title>')
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15"/><text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{i}</text>')
        if show_labels:
            right = x < W - 200
            tx = x + 22 if right else x - 22
            svg.append(f'<text class="atlas__label" x="{tx:.1f}" y="{y + 5:.1f}" text-anchor="{"start" if right else "end"}">{label}</text>')
        svg.append("</a>")
    # scale bar and north arrow
    km_per_unit = 111.2
    target = (W * 0.18) / s * km_per_unit
    km = _nice(target)
    bar = km / km_per_unit * s
    svg.append(f'<g class="atlas__scale" transform="translate(24,{H - 28})"><line x1="0" y1="0" x2="{bar:.1f}" y2="0"/>'
               f'<line x1="0" y1="-6" x2="0" y2="6"/><line x1="{bar:.1f}" y1="-6" x2="{bar:.1f}" y2="6"/>'
               f'<text x="{bar / 2:.1f}" y="-10" text-anchor="middle">{km} km</text></g>')
    svg.append(f'<g class="atlas__north" transform="translate({W - 40},44)"><path d="M0,-22 L9,8 L0,2 L-9,8 Z"/><text y="26" text-anchor="middle">N</text></g>')
    svg.append("</svg>")
    html = ['<figure class="atlas">', "".join(svg)]
    if legend:
        html.append('<ol class="atlas__legend">' + "".join(
            f'<li data-n="{i}"><a href="{escape(p.get("url", "#"))}"><span>{i}</span>{escape(p["name"])}'
            + (f' <small>{p["nights"]} night{"s" if p["nights"] != 1 else ""}</small>' if p.get("nights") else "")
            + "</a></li>" for i, p in enumerate(pts, 1)) + "</ol>")
    html.append('<figcaption>Drawn by Go Sikkim Tours from Natural Earth outlines (public domain). Borders as depicted by India. Not for navigation.</figcaption></figure>')
    return "".join(html)
