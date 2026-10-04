"""Validate one region's content against content/SCHEMA.md.

Usage: python tools/check_region.py <region-slug> [--wiki]
--wiki also confirms every `wiki` title exists on English Wikipedia.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
THEMES = set("shoestring homestays honeymoons family-trips snow-and-passes monasteries tea-country toy-train "
             "treks-and-walks wildlife-and-birds festivals food-trails photography weekend-breaks".split())
KINDS = set("culture spiritual nature wildlife food adventure tea snow craft village".split())
TIERS = ["Budget", "Value", "Comfort"]
BANNED = ["nestled", "breathtaking", "hidden gem", "paradise", "tapestry", "embark", "delve", "unleash",
          "vibrant", "bustling", "mesmeriz", "stunning", "magical", "heaven on earth", "feast for the eyes",
          "something for everyone", "whether you're", "look no further", "ultimate guide", "in this blog",
          "in conclusion", "unforgettable", "world-class", "seamless", "elevate", "immerse", "timeless",
          "boasts", "abode of", "land of mystic", "shangri-la", "exotic", "primitive", "!"]
errors, warns = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(str(p), "missing file")
    except Exception as e:  # noqa: BLE001
        err(str(p), f"invalid JSON ({e})")
    return None


def months(where, v):
    if not (isinstance(v, list) and len(v) == 12 and all(x in (0, 1, 2) for x in v)):
        err(where, "best_months must be 12 ints of 0/1/2")


def faqs(where, v, n):
    if not isinstance(v, list) or len(v) != n:
        err(where, f"needs exactly {n} faqs (has {len(v) if isinstance(v, list) else 0})")
        return
    for f in v:
        if not f.get("q") or not f.get("a"):
            err(where, "faq missing q/a")


def heading(where, t):
    if t and t.rstrip().endswith("."):
        err(where, f"heading ends with full stop: {t!r}")
    if t and len(t) > 70:
        warns.append(f"{where}: long heading ({len(t)} chars) {t!r}")


def scan_banned(where, obj):
    text = json.dumps(obj, ensure_ascii=False).lower()
    for b in BANNED:
        if b in text:
            warns.append(f"{where}: banned word/phrase '{b}'")


def main():
    r = sys.argv[1]
    base = ROOT / r
    registry = json.loads((ROOT / "_places.json").read_text(encoding="utf-8"))
    all_places = {s for k, v in registry.items() if not k.startswith("_") for s in v}
    mine = set(registry.get(r, {}))
    wiki_titles = []
    reg = load(base / "region.json")
    places, stays, fests = {}, {}, {}
    for p in sorted((base / "places").glob("*.json")):
        d = load(p)
        if d:
            if d.get("slug") != p.stem:
                err(p.name, f"slug {d.get('slug')!r} != filename")
            places[d["slug"]] = d
    for s in load(base / "stays.json") or []:
        stays[s["slug"]] = s
    for f in load(base / "festivals.json") or []:
        fests[f["slug"]] = f
    missing = mine - set(places)
    if missing:
        err("places", f"missing place files: {sorted(missing)}")
    extra = set(places) - mine
    if extra:
        err("places", f"place files not in _places.json: {sorted(extra)}")

    if reg:
        months("region", reg.get("best_months"))
        faqs("region", reg.get("faqs"), 9)
        if len(reg.get("highlights", [])) != 6:
            err("region", "needs 6 highlights")
        if len(reg.get("months", [])) != 12:
            err("region", "needs 12 months")
        if len(reg.get("budget_day", [])) != 3:
            err("region", "needs 3 budget_day rows")
        if not reg.get("people"):
            err("region", "missing people")
        for m in reg.get("months", []):
            for g in m.get("go", []):
                if g not in all_places:
                    err(f"region month {m.get('month')}", f"unknown place '{g}'")
            for e in m.get("events", []):
                if e not in fests:
                    err(f"region month {m.get('month')}", f"unknown festival '{e}'")
        wiki_titles.append(reg.get("wiki"))
        scan_banned("region", reg)

    exp_slugs = set()
    for slug, d in places.items():
        w = f"place {slug}"
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("tagline"))
        st = d.get("story") or {}
        if not (st.get("title") and len(st.get("paras", [])) >= 3 and st.get("sources")):
            err(w, "story needs title, 3+ paras and sources")
        heading(f"{w} story", st.get("title"))
        lw = d.get("local_word") or {}
        if not (lw.get("word") and lw.get("meaning")):
            err(w, "local_word needs word and meaning")
        if not (5 <= len(d.get("costs", [])) <= 8):
            err(w, f"needs 5–7 cost rows (has {len(d.get('costs', []))})")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        for n in d.get("nearby", []):
            if n not in all_places:
                err(w, f"unknown nearby '{n}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        ex = d.get("experiences", [])
        if len(ex) != 4:
            err(w, f"needs 4 experiences (has {len(ex)})")
        for e in ex:
            heading(f"{w} exp", e.get("title"))
            faqs(f"{w} exp {e.get('slug')}", e.get("faqs"), 3)
            if e.get("kind") not in KINDS:
                err(f"{w} exp {e.get('slug')}", f"unknown kind {e.get('kind')!r}")
            if not e.get("cost"):
                err(f"{w} exp {e.get('slug')}", "missing cost")
            if e["slug"] in exp_slugs:
                err(w, f"duplicate experience slug {e['slug']}")
            exp_slugs.add(e["slug"])
            if e.get("wiki"):
                wiki_titles.append(e["wiki"])
        wiki_titles.append(d.get("wiki"))
        scan_banned(w, d)

    for p in sorted((base / "journeys").glob("*.json")):
        d = load(p)
        if not d:
            continue
        w = f"journey {d.get('slug')}"
        months(w, d.get("best_months"))
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"))
        total = sum(s.get("nights", 0) for s in d.get("stops", []))
        if total != d.get("nights"):
            err(w, f"stop nights {total} != nights {d.get('nights')}")
        if len(d.get("days", [])) != d.get("nights", 0) + 1:
            err(w, "days must equal nights + 1")
        tiers = d.get("tiers", [])
        if [t.get("name") for t in tiers] != TIERS:
            err(w, "tiers must be Budget, Value, Comfort in that order")
        elif d.get("price_from_inr") != tiers[0].get("price_inr"):
            err(w, "price_from_inr must equal the Budget tier price")
        elif not (tiers[0]["price_inr"] < tiers[1]["price_inr"] < tiers[2]["price_inr"]):
            err(w, "tier prices must rise")
        if len(d.get("save_tips", [])) < 3:
            err(w, "needs 3 save_tips")
        for s in d.get("stops", []):
            if s["place"] not in all_places:
                err(w, f"unknown stop '{s['place']}'")
        for dd in d.get("days", []):
            heading(f"{w} day {dd.get('day')}", dd.get("title"))
            if dd.get("place") and dd["place"] not in all_places:
                err(w, f"day {dd.get('day')} unknown place '{dd['place']}'")
        for s in d.get("stays", []):
            if s not in stays:
                err(w, f"unknown stay '{s}'")
        for t in d.get("themes", []):
            if t not in THEMES:
                err(w, f"unknown theme '{t}'")
        scan_banned(w, d)

    for slug, s in stays.items():
        w = f"stay {slug}"
        faqs(w, s.get("faqs"), 3)
        if s.get("place") not in all_places:
            err(w, f"unknown place '{s.get('place')}'")
        if s.get("budget") not in TIERS:
            err(w, "budget must be Budget, Value or Comfort")
        if s.get("wiki"):
            wiki_titles.append(s["wiki"])
        scan_banned(w, s)

    for p in sorted((base / "guides").glob("*.json")):
        d = load(p)
        if not d:
            continue
        w = f"guide {d.get('slug')}"
        faqs(w, d.get("faqs"), 9)
        heading(w, d.get("title"))
        words = sum(len(" ".join(s.get("paras", []) + s.get("list", [])).split()) for s in d.get("sections", []))
        if words < 1000:
            warns.append(f"{w}: only {words} words")
        for s in d.get("sections", []):
            heading(w, s.get("heading"))
        for rp in d.get("related_places", []):
            if rp not in all_places:
                err(w, f"unknown related place '{rp}'")
        scan_banned(w, d)

    for slug, f in fests.items():
        w = f"festival {slug}"
        faqs(w, f.get("faqs"), 4)
        if f.get("place") not in all_places:
            err(w, f"unknown place '{f.get('place')}'")
        if f.get("wiki"):
            wiki_titles.append(f["wiki"])
        scan_banned(w, f)

    for rt in load(base / "routes.json") or []:
        w = f"route {rt.get('slug')}"
        faqs(w, rt.get("faqs"), 4)
        for k in ("from", "to"):
            if rt.get(k) not in all_places:
                err(w, f"unknown {k} '{rt.get(k)}'")
        for o in rt.get("options", []):
            if not o.get("fare"):
                err(w, f"option {o.get('mode')} missing fare")
        scan_banned(w, rt)

    if "--wiki" in sys.argv:
        titles = sorted({t for t in wiki_titles if t})
        for i in range(0, len(titles), 40):
            q = urllib.parse.urlencode({"action": "query", "titles": "|".join(titles[i:i + 40]),
                                        "redirects": 1, "format": "json", "formatversion": 2})
            req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q,
                                         headers={"User-Agent": "GoSikkimToursBuild/1.0 (content check)"})
            data = json.load(urllib.request.urlopen(req, timeout=30))
            for pg in data["query"]["pages"]:
                if pg.get("missing") or pg.get("invalid"):
                    err("wiki", f"no Wikipedia article titled {pg.get('title')!r} (use '' or fix)")

    counts = (f"places={len(places)} experiences={len(exp_slugs)} stays={len(stays)} festivals={len(fests)} "
              f"journeys={len(list((base / 'journeys').glob('*.json')))} guides={len(list((base / 'guides').glob('*.json')))}")
    print(counts)
    for w in warns:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
