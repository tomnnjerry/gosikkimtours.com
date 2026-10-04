"""In-memory catalogue built from content/*.json.

Every page on the site is rendered from this catalogue. In DEBUG the catalogue
reloads when any content file changes, so writers see edits on refresh.
"""
import json
import re
from collections import OrderedDict
from pathlib import Path

from django.conf import settings
from django.urls import reverse

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_SHORT = [m[:3] for m in MONTHS]
REGION_ORDER = ["east-sikkim", "north-sikkim", "west-sikkim", "darjeeling", "kalimpong", "dooars", "bhutan"]
# Each region wears the colours it is known for.
# ground = dark sections, accent = highlights and buttons on dark, ink = accent text on light, tint = light wash
LANDS = {
    "east-sikkim": {"palette": "Tsomgo teal and rhododendron red", "short": "Gangtok and the passes",
                    "ground": "#0B3B45", "ground2": "#12505C", "accent": "#FF7A68", "ink": "#B3261E", "tint": "#E1F0F1"},
    "north-sikkim": {"palette": "Glacier indigo and primula pink", "short": "Lachung, Lachen, Gurudongmar",
                     "ground": "#1E2550", "ground2": "#28306A", "accent": "#F59AC8", "ink": "#A3306A", "tint": "#ECEBF6"},
    "west-sikkim": {"palette": "Khecheopalri moss and prayer-wheel copper", "short": "Pelling, Yuksom, Ravangla",
                    "ground": "#173A2C", "ground2": "#1F4A39", "accent": "#EE9A62", "ink": "#9A4A1A", "tint": "#E4EFE8"},
    "darjeeling": {"palette": "Toy-train blue and first-flush green", "short": "Tea, toy train, Tiger Hill",
                   "ground": "#0F2F5C", "ground2": "#173E72", "accent": "#BFE07A", "ink": "#4D6B10", "tint": "#E6ECF6"},
    "kalimpong": {"palette": "Orchid violet and marigold", "short": "Nurseries, Lava, Silk Route villages",
                  "ground": "#3D1B47", "ground2": "#4E2559", "accent": "#FFAD52", "ink": "#A0500A", "tint": "#F1E8F3"},
    "dooars": {"palette": "Sal forest and Jaldhaka jade", "short": "Rhino, elephants and tea plains",
               "ground": "#33300E", "ground2": "#433F16", "accent": "#63D6BE", "ink": "#0E6E5C", "tint": "#EFEEDD"},
    "bhutan": {"palette": "Dzong red and dragon yellow", "short": "Paro, Thimphu, Punakha",
               "ground": "#6E1A12", "ground2": "#83251A", "accent": "#FFD447", "ink": "#7E6100", "tint": "#F8E9E4"},
}

# Shiny gradients per region: `grad` = ground (dark, 3 stops), `foil` = metallic accent (light -> mid -> deep).
GRADIENTS = {
    "east-sikkim": {"grad": ("#05262D", "#0D4954", "#16707C"), "foil": ("#FFD9D1", "#FF7A68", "#D63E2C")},
    "north-sikkim": {"grad": ("#11163A", "#25306E", "#3B4796"), "foil": ("#FFE3F1", "#F59AC8", "#C74F8C")},
    "west-sikkim": {"grad": ("#0D261C", "#1C4635", "#2A6650"), "foil": ("#FFE4CF", "#EE9A62", "#B95A26")},
    "darjeeling": {"grad": ("#081D3D", "#143B70", "#1F58A3"), "foil": ("#F3FFD2", "#BFE07A", "#7DA52A")},
    "kalimpong": {"grad": ("#260E2E", "#4A2056", "#6E3480"), "foil": ("#FFE6C4", "#FFAD52", "#D9760F")},
    "dooars": {"grad": ("#1E1C06", "#3D3A12", "#5C5820"), "foil": ("#D8FFF5", "#63D6BE", "#1F9C83")},
    "bhutan": {"grad": ("#430D07", "#7C2116", "#A83A22"), "foil": ("#FFF6C8", "#FFD447", "#D9A400")},
}
for _slug, _g in GRADIENTS.items():
    LANDS[_slug].update(_g)

KINDS = OrderedDict([
    ("culture", ("Culture and history", "Palaces, forts, bazaars and old trade roads", "Walks with people who know the story of each town: the Chogyals, the tea planters, the mule traders and the Koch kings.")),
    ("spiritual", ("Monasteries and temples", "Gompas, dzongs, chortens and shrines", "Morning prayers, butter lamps and masked dances, visited at their own hours and with the dress and photo rules explained.")),
    ("nature", ("Views and nature", "Sunrises, lakes, valleys and forests", "Viewpoints at the right hour, lakes at the right month and walks short enough for anyone.")),
    ("wildlife", ("Wildlife and birds", "Rhino, elephant, red panda and hornbills", "Jeep safaris in the Dooars and quiet forest walks in the hills, timed to the season and the park rules.")),
    ("food", ("Food and markets", "Momos, thukpa, ema datshi and haat bazaars", "Market mornings, home kitchens and the dishes each hill town argues about.")),
    ("adventure", ("Treks and adventure", "Trails, rafting and high roads", "Days graded by hours, height and terrain, with registered guides and honest costs.")),
    ("tea", ("Tea gardens", "Darjeeling, Temi and the Dooars estates", "Plucking, rolling and tasting in working gardens, with the flush calendar explained.")),
    ("snow", ("Snow and high passes", "Zero Point, Nathu La, Chele La", "High-altitude days planned with permits, warm layers and time to adjust.")),
    ("craft", ("Crafts and makers", "Weaving, carving and paper", "Workshops and cooperatives where you can watch the work and buy from the maker.")),
    ("village", ("Village stays", "Homestays and farm life", "Nights with families in hill villages: home food, fields and the view from the porch.")),
])

_cache = {"stamp": None, "cat": None}


def _read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _stamp(root):
    return max((p.stat().st_mtime for p in root.rglob("*.json")), default=0)


def catalogue():
    root = Path(settings.CONTENT_DIR)
    if _cache["cat"] is None or settings.DEBUG:
        stamp = _stamp(root)
        if stamp != _cache["stamp"]:
            _cache["cat"] = Catalogue(root)
            _cache["stamp"] = stamp
    return _cache["cat"]


def month_bar(best):
    """[{'m': 'Jan', 'v': 2}, ...] for the 12-month strip."""
    best = best or [0] * 12
    return [{"m": MONTH_SHORT[i], "full": MONTHS[i], "v": best[i] if i < len(best) else 0} for i in range(12)]


def altitude_profile(stops, w=640, h=170):
    """SVG geometry for a route's altitude line: stops = [(name, metres, url)]."""
    if not stops:
        return None
    top = max(m for _, m, _ in stops) or 1
    step = 1000 if top <= 5000 else 2000
    ceiling = max(1000, ((top // step) + 1) * step)
    n = len(stops)
    base = h - 26
    pts = []
    for i, (name, m, url) in enumerate(stops):
        x = 46 + (w - 92) * (i / (n - 1) if n > 1 else 0.5)
        y = base - (h - 64) * (m / ceiling)
        pts.append({"x": round(x, 1), "y": round(y, 1), "name": name, "m": m, "url": url, "ly": round(y - 12, 1)})
    line = " ".join(f"{p['x']},{p['y']}" for p in pts)
    area = f"{pts[0]['x']},{base} {line} {pts[-1]['x']},{base}"
    grid = [{"y": round(base - (h - 64) * (v / ceiling), 1), "v": v} for v in range(0, ceiling + 1, step)]
    return {"w": w, "h": h, "base": base, "pts": pts, "line": line, "area": area, "grid": grid, "top": top}


def best_range(best):
    """'Oct – Mar' style label from a 12-int array (rating 2 = best)."""
    if not best:
        return ""
    good = {i for i, v in enumerate(best) if v == 2} or {i for i, v in enumerate(best) if v >= 1}
    if not good:
        return ""
    if len(good) == 12:
        return "All year"
    runs = []  # runs on a circular calendar, e.g. Oct..Mar
    for i in range(12):
        if i in good and (i - 1) % 12 not in good:
            run, j = [i], (i + 1) % 12
            while j in good:
                run.append(j)
                j = (j + 1) % 12
            runs.append(run)
    labels = []
    for run in runs:
        labels.append(MONTH_SHORT[run[0]] if len(run) == 1 else f"{MONTH_SHORT[run[0]]} – {MONTH_SHORT[run[-1]]}")
    return " · ".join(labels)


def _interleave(lists):
    """First photo of each list, then the second of each, and so on (no repeats)."""
    lists = [list(x) for x in lists]
    out, seen = [], set()
    for i in range(max((len(x) for x in lists), default=0)):
        for x in lists:
            if i < len(x) and x[i]["file"] not in seen:
                seen.add(x[i]["file"])
                out.append(x[i])
    return out


def _spread(objs, used):
    """Rotate each object's photos so its lead photo is one no earlier card already leads with."""
    for o in objs:
        imgs = o.get("images") or []
        for k, img in enumerate(imgs):
            if img["file"] not in used:
                if k:
                    o["images"] = imgs[k:] + imgs[:k]
                break
        if o.get("images"):
            used.add(o["images"][0]["file"])


class Catalogue:
    def __init__(self, root):
        self.root = root
        self.themes = OrderedDict((t["slug"], t) for t in _read(root / "themes.json"))
        img_file = root / "images.json"
        self.images = _read(img_file) if img_file.exists() else {}
        self.regions = OrderedDict()
        self.places = OrderedDict()
        self.experiences = OrderedDict()
        self.journeys = OrderedDict()
        self.stays = OrderedDict()
        self.guides = OrderedDict()
        self.festivals = OrderedDict()
        self.routes = OrderedDict()
        for slug in REGION_ORDER:
            base = root / slug
            if (base / "region.json").exists():
                self._load_region(slug, base)
        self.posts = OrderedDict()
        for p in (root / "journal").glob("*.json") if (root / "journal").exists() else []:
            d = _read(p)
            d["url"] = reverse("post", args=[d["slug"]])
            self.posts[d["slug"]] = d
        self.posts = OrderedDict(sorted(self.posts.items(), key=lambda kv: kv[1].get("date", ""), reverse=True))
        self._link()
        self._link_posts()

    # ---------- loading ----------
    def _load_region(self, slug, base):
        r = _read(base / "region.json")
        r["slug"] = slug
        pal = LANDS[slug]
        r.update(pal)
        r["pigment"], r["deep"] = pal["accent"], pal["ink"]
        r["url"] = reverse("region", args=[slug])
        r["places"], r["journeys"], r["stays"], r["guides"], r["festivals"], r["routes"] = [], [], [], [], [], []
        self.regions[slug] = r
        for p in sorted((base / "places").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("place", args=[slug, d["slug"]])
            self.places[d["slug"]] = d
            r["places"].append(d)
            for e in d.get("experiences", []):
                e["place"] = d["slug"]
                e["region"] = slug
                e["url"] = reverse("experience", args=[slug, d["slug"], e["slug"]])
                self.experiences[e["slug"]] = e
        for p in sorted((base / "journeys").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("journey", args=[d["slug"]])
            self.journeys[d["slug"]] = d
            r["journeys"].append(d)
        for name, store, key, view in (("stays.json", self.stays, "stays", "stay"),
                                       ("festivals.json", self.festivals, "festivals", "festival"),
                                       ("routes.json", self.routes, "routes", "route")):
            f = base / name
            for d in (_read(f) if f.exists() else []):
                d["region"] = slug
                d["url"] = reverse(view, args=[d["slug"]])
                store[d["slug"]] = d
                r[key].append(d)
        for p in sorted((base / "guides").glob("*.json")):
            d = _read(p)
            d["region"] = slug
            d["url"] = reverse("guide", args=[d["slug"]])
            self.guides[d["slug"]] = d
            r["guides"].append(d)

    def _imgs(self, *keys):
        for k in keys:
            if self.images.get(k):
                return self.images[k]
        return []

    def _link(self):
        # drop routes whose places do not exist (yet)
        for slug in [s for s, rt in self.routes.items() if rt.get("from") not in self.places or rt.get("to") not in self.places]:
            dead = self.routes.pop(slug)
            self.regions[dead["region"]]["routes"].remove(dead)
        for r in self.regions.values():
            r["images"] = self._imgs(f"region:{r['slug']}") or [
                i for p in r["places"][:6] for i in self._imgs(f"place:{p['slug']}")[:1]]
            r["best_label"] = best_range(r.get("best_months"))
            r["bar"] = month_bar(r.get("best_months"))
        for p in self.places.values():
            p["region_obj"] = self.regions[p["region"]]
            p["images"] = self._imgs(f"place:{p['slug']}")
            p["best_label"] = best_range(p.get("best_months"))
            p["bar"] = month_bar(p.get("best_months"))
            p["nearby_objs"] = [self.places[s] for s in p.get("nearby", []) if s in self.places]
            p["stay_objs"] = [self.stays[s] for s in p.get("stays", []) if s in self.stays]
            p["journey_objs"] = [j for j in self.journeys.values()
                                 if any(s["place"] == p["slug"] for s in j.get("stops", []))]
            p["festival_objs"] = [f for f in self.festivals.values() if f.get("place") == p["slug"]]
            p["route_objs"] = [rt for rt in self.routes.values() if p["slug"] in (rt.get("from"), rt.get("to"))]
        for r in self.regions.values():
            # the places most journeys stop at lead menus and supply the land's lead photos
            r["top_places"] = sorted(r["places"], key=lambda p: (-len(p["journey_objs"]), p["name"]))
            # road distance from Siliguri to the main town, painted on the milestone markers
            # (the main town if a published route reaches it, else the nearest place that one does)
            roads = self._road_km()
            reach = [p for p in r["top_places"] if roads.get(p["slug"])]
            stop = (reach[:1] if reach and reach[0] is r["top_places"][0] else sorted(reach, key=lambda p: roads[p["slug"]])[:1]) \
                or r["top_places"][:1]
            r["milestone"] = {"name": stop[0]["name"].split(" and ")[0], "km": roads.get(stop[0]["slug"])} if stop else None
            r["images"] = self._imgs(f"region:{r['slug']}") or [
                i for p in r["top_places"][:6] for i in p["images"][:1]]
        for e in self.experiences.values():
            place = self.places[e["place"]]
            e["place_obj"] = place
            e["region_obj"] = place["region_obj"]
            e["images"] = self._imgs(f"exp:{e['slug']}") or place["images"]
            e["themes"] = place.get("themes", [])
        for s in self.stays.values():
            place = self.places.get(s.get("place"))
            s["place_obj"] = place
            s["region_obj"] = self.regions[s["region"]]
            s["images"] = self._imgs(f"stay:{s['slug']}") or (place["images"] if place else [])
            s["journey_objs"] = [j for j in self.journeys.values() if s["slug"] in j.get("stays", [])]
        for j in self.journeys.values():
            j["region_obj"] = self.regions[j["region"]]
            stops = [dict(st, obj=self.places[st["place"]]) for st in j.get("stops", []) if st["place"] in self.places]
            j["stop_objs"] = stops
            j["images"] = self._imgs(f"journey:{j['slug']}") or _interleave(st["obj"]["images"] for st in stops)
            j["stay_objs"] = [self.stays[s] for s in j.get("stays", []) if s in self.stays]
            j["best_label"] = best_range(j.get("best_months"))
            j["bar"] = month_bar(j.get("best_months"))
            j["days_count"] = j.get("nights", 0) + 1
            for d in j.get("days", []):
                d["place_obj"] = self.places.get(d.get("place"))
        for g in self.guides.values():
            g["region_obj"] = self.regions[g["region"]]
            rel = [self.places[s] for s in g.get("related_places", []) if s in self.places]
            g["related_objs"] = rel
            g["images"] = self._imgs(f"guide:{g['slug']}") or _interleave(p["images"] for p in rel) or g["region_obj"]["images"]
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in g.get("sections", []))
            g["read_min"] = max(3, round(words / 220))
            for s in g.get("sections", []):
                s["anchor"] = re.sub(r"[^a-z0-9]+", "-", s.get("heading", "").lower()).strip("-")
        for f in self.festivals.values():
            place = self.places.get(f.get("place"))
            f["place_obj"] = place
            f["region_obj"] = self.regions[f["region"]]
            f["images"] = self._imgs(f"fest:{f['slug']}") or (place["images"] if place else [])
        for rt in self.routes.values():
            rt["from_obj"] = self.places.get(rt.get("from"))
            rt["to_obj"] = self.places.get(rt.get("to"))
            rt["region_obj"] = self.regions[rt["region"]]
            rt["images"] = (rt["to_obj"] or {}).get("images", []) + (rt["from_obj"] or {}).get("images", [])[:1]
        for t in self.themes.values():
            t["url"] = reverse("theme", args=[t["slug"]])
        # rooted stories: one per place, each with its own page
        self.stories = OrderedDict()
        for p in self.places.values():
            st = p.get("story")
            if st and st.get("title"):
                st["place_obj"] = p
                st["slug"] = p["slug"]
                st["region"] = p["region"]
                st["url"] = reverse("story", args=[p["slug"]])
                st["images"] = p["images"][1:] + p["images"][:1]
                self.stories[p["slug"]] = st
        # every fare we quote, flattened for the fare board
        self.fares = []
        for rt in self.routes.values():
            for o in rt.get("options", []):
                self.fares.append({"route": rt, "mode": o.get("mode", ""), "time": o.get("time", ""), "fare": o.get("fare", "")})
        # journeys: tier prices and the altitude line of the route
        for j in self.journeys.values():
            j["tier_prices"] = {t.get("name", "").lower(): t.get("price_inr") for t in (j.get("tiers") or [])}
            j["profile"] = altitude_profile([(s["obj"]["name"], s["obj"].get("altitude_m") or 0, s["obj"]["url"]) for s in j["stop_objs"]])
        self.ladder = sorted([p for p in self.places.values() if p.get("altitude_m") is not None], key=lambda p: p["altitude_m"])

    def _road_km(self, start="siliguri"):
        """Shortest road distance in km from `start` to every place, over the routes we publish."""
        if getattr(self, "_km", None) is None:
            import heapq
            graph = {}
            for rt in self.routes.values():
                d = rt.get("distance_km") or 0
                graph.setdefault(rt["from"], []).append((rt["to"], d))
                graph.setdefault(rt["to"], []).append((rt["from"], d))
            dist, queue = {start: 0}, [(0, start)]
            while queue:
                d, u = heapq.heappop(queue)
                if d > dist[u]:
                    continue
                for v, w in graph.get(u, []):
                    if d + w < dist.get(v, float("inf")):
                        dist[v] = d + w
                        heapq.heappush(queue, (d + w, v))
            self._km = dist
        return self._km

    def _link_posts(self):
        from datetime import date
        for d in self.posts.values():
            d["region_objs"] = [self.regions[r] for r in d.get("regions", []) if r in self.regions]
            d["journey_objs"] = [self.journeys[j] for j in d.get("related_journeys", []) if j in self.journeys]
            d["place_objs"] = [self.places[x] for x in d.get("related_places", []) if x in self.places]
            d["images"] = (self._imgs(f"blog:{d['slug']}") or _interleave(x["images"] for x in d["place_objs"])
                           or _interleave(r["images"] for r in d["region_objs"]))
            words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
            d["read_min"] = max(3, round(words / 220))
            d["cat_slug"] = re.sub(r"[^a-z0-9]+", "-", d.get("category", "").lower()).strip("-")
            try:
                d["date_obj"] = date.fromisoformat(d.get("date", ""))
            except ValueError:
                d["date_obj"] = None
            land = d["region_objs"][0]["slug"] if d["region_objs"] else None
            d["land"] = land
            stores = {"journey": self.journeys, "place": self.places, "stay": self.stays, "guide": self.guides, "festival": self.festivals}
            for sec in d.get("sections", []):
                sec["anchor"] = re.sub(r"[^a-z0-9]+", "-", sec.get("heading", "").lower()).strip("-")
                objs = []
                for ln in sec.get("links", []):
                    o = stores.get(ln.get("type"), {}).get(ln.get("slug"))
                    if o:
                        objs.append({"type": ln["type"], "title": o.get("title") or o.get("name"), "url": o["url"],
                                     "img": (o.get("images") or [None])[0], "obj": o})
                sec["link_objs"] = objs
        # no two cards lead with the same photo when the pool allows it
        used = set()
        for store in (self.places, self.regions, self.stories, self.experiences, self.stays, self.festivals,
                      self.journeys, self.guides, self.posts):
            _spread(store.values(), used)
        self.post_categories = OrderedDict()
        for d in self.posts.values():
            self.post_categories.setdefault(d["cat_slug"], {"slug": d["cat_slug"], "name": d.get("category"), "posts": []})["posts"].append(d)

    # ---------- queries ----------
    def theme_items(self, theme, region=None):
        def ok(x):
            return region is None or x.get("region") == region
        places = [p for p in self.places.values() if theme in p.get("themes", []) and ok(p)]
        journeys = [j for j in self.journeys.values() if theme in j.get("themes", []) and ok(j)]
        place_slugs = {p["slug"] for p in places}
        stays = [s for s in self.stays.values() if s.get("place") in place_slugs and ok(s)]
        experiences = [e for e in self.experiences.values() if e["place"] in place_slugs and ok(e)]
        return {"places": places, "journeys": journeys, "stays": stays, "experiences": experiences}

    def region_theme_pairs(self):
        """(region, theme) pairs with enough content to deserve a page."""
        out = []
        for r in self.regions:
            for t in self.themes:
                items = self.theme_items(t, r)
                if len(items["places"]) >= 2 and (items["journeys"] or len(items["places"]) >= 3):
                    out.append((r, t))
        return out

    def region_kind_pairs(self):
        """(region, kind) pairs with at least 3 experiences."""
        out = []
        for r in self.regions:
            for k in KINDS:
                if sum(1 for e in self.experiences.values() if e["region"] == r and e.get("kind") == k) >= 3:
                    out.append((r, k))
        return out

    def counts(self):
        return {
            "regions": len(self.regions), "places": len(self.places), "experiences": len(self.experiences),
            "journeys": len(self.journeys), "stays": len(self.stays), "guides": len(self.guides),
            "festivals": len(self.festivals), "routes": len(self.routes), "themes": len(self.themes),
            "posts": len(self.posts), "stories": len(getattr(self, "stories", {})),
        }

    def all_images(self):
        seen, out = set(), []
        for key, recs in self.images.items():
            for rec in recs:
                if rec["file"] not in seen:
                    seen.add(rec["file"])
                    out.append(dict(rec, used_for=key))
        return out
