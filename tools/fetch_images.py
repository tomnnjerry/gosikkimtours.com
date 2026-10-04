"""Build content/images.json: credited Wikimedia Commons photos for every page.

Usage: python tools/fetch_images.py [region ...] [--force]

Incremental: keys already in images.json are kept unless --force.
Sources, in order: the entity's English Wikipedia article images (curated by
editors, so they show the right place), then a Commons search on `image_query`.
North East places also reuse the hand-checked photos from the Shillong Trip
project when the slugs match.
"""
import json
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import commons  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = CONTENT / "images.json"
SISTER = Path(r"C:\Projects\15\shillongtrip.com\content\images.json")
REGIONS = ["nepal", "rajasthan", "ladakh", "north-east", "kerala", "goa", "up-bihar"]
BAD_TITLE = re.compile(r"(ISS\d|satellite|NASA|Landsat|Sentinel|portrait|stamp|banknote|coin|\bmap\b|locator|svg|protest|riot|clash|election|rally|"
                       r"minister|president|police|army|military|curfew|flood|earthquake|damage|destroyed|collapse|"
                       r"accident|relief|topograph|physical|elevation|burning|smoke|strike|bandh|meeting|delegation|signing|logo|poster)", re.I)


# Hand-picked sources for keys where the automatic pick was wrong or weak.
# ("wiki", title) uses that article's images; ("query", text) a Commons search.
OVERRIDES = {
    "place:assagao-and-anjuna": ("query", "Anjuna beach Goa"),
    "place:pangong-tso": ("query", "Pangong Tso lake Ladakh"),
    "place:bodh-gaya": ("query", "Mahabodhi Temple South Wall"),
}


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def thumb_from_original(url, width=1280):
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w)/(\w\w)/(.+)$", url)
    if not m:
        return url
    base, a, ab, name = m.groups()
    return f"{base}/thumb/{a}/{ab}/{name}/{width}px-{name}"


def sister_images():
    if not SISTER.exists():
        return {}
    data = json.loads(SISTER.read_text(encoding="utf-8"))
    out = {}
    for slug, recs in data.items():
        conv = []
        for r in recs:
            if not r.get("url"):
                continue
            conv.append({
                "file": r.get("file"), "url": r["url"],
                "thumb": thumb_from_original(r["url"]) if (r.get("width") or 0) > 1280 else r["url"],
                "width": r.get("width"), "height": r.get("height"),
                "landscape": (r.get("width") or 1) >= (r.get("height") or 1),
                "description": r.get("alt", ""), "author": r.get("author", ""),
                "license": r.get("license", ""), "license_url": r.get("license_url", ""), "source": r.get("source", ""),
            })
        out[slug] = conv
    return out


def clean(recs):
    seen, out = set(), []
    for r in recs:
        if r["file"] in seen or BAD_TITLE.search(r["file"]):
            continue
        seen.add(r["file"])
        out.append(r)
    return out


def landscape_first(recs):
    return sorted(recs, key=lambda r: 0 if r.get("landscape") else 1)


def for_entity(wiki, query, n, prefer_landscape=True):
    recs = []
    if wiki:
        recs += commons.article_images(wiki, n + 2)
    if len(clean(recs)) < n and query:
        words = query.split()
        # progressively shorter queries: specific searches often return nothing
        for k in sorted({len(words), 4, 3} & set(range(3, len(words) + 1)), reverse=True):
            recs += commons.search_images(" ".join(words[:k]), n)
            if len(clean(recs)) >= n:
                break
    recs = clean(recs)
    return (landscape_first(recs) if prefer_landscape else recs)[:n]


def jobs_for_region(slug):
    base = CONTENT / slug
    jobs = []
    if not (base / "region.json").exists():
        return jobs
    reg = read(base / "region.json")
    # region pages use their places' lead photos (country/state articles carry news photos)
    for p in sorted((base / "places").glob("*.json")):
        d = read(p)
        jobs.append((f"place:{d['slug']}", d.get("wiki"), d.get("image_query") or d.get("name"), 6))
        for e in d.get("experiences", []):
            jobs.append((f"exp:{e['slug']}", e.get("wiki"), e.get("image_query") or e.get("title"), 3))
    if (base / "stays.json").exists():
        for s in read(base / "stays.json"):
            jobs.append((f"stay:{s['slug']}", s.get("wiki"), s.get("image_query") or s.get("name"), 3))
    if (base / "festivals.json").exists():
        for f in read(base / "festivals.json"):
            jobs.append((f"fest:{f['slug']}", f.get("wiki"), f.get("image_query") or f.get("name"), 3))
    return jobs


def main():
    force = "--force" in sys.argv
    regions = [a for a in sys.argv[1:] if not a.startswith("--")] or REGIONS
    images = read(OUT) if OUT.exists() else {}
    # re-apply the current filter to photos saved by earlier runs
    images = {k: [r for r in v if not BAD_TITLE.search(r["file"]) and not commons.SKIP_WORDS.search(r["file"])]
              for k, v in images.items() if not k.startswith("region:")}
    sister = sister_images()
    if "journal" in regions or len(regions) == len(REGIONS):
        posts = sorted((CONTENT / "journal").glob("*.json")) if (CONTENT / "journal").exists() else []
        regions = [r for r in regions if r != "journal"] + ["journal"]
    for slug in regions:
        if slug == "journal":
            jobs = [(f"blog:{d['slug']}", d.get("wiki"), d.get("image_query") or d.get("title"), 3)
                    for d in (read(p) for p in posts)]
            jobs = [j for j in jobs if force or not images.get(j[0])]
        else:
            jobs = [j for j in jobs_for_region(slug) if force or not images.get(j[0])]
        print(f"{slug}: {len(jobs)} lookups")

        def run(job):
            key, wiki, query, n = job
            try:
                recs = for_entity(wiki, query, n)
            except Exception as e:  # noqa: BLE001
                print("  fail", key, e)
                recs = []
            if key.startswith("place:") and slug == "north-east":
                extra = sister.get(key.split(":", 1)[1], [])
                recs = clean(extra + recs)[:n]
            return key, recs

        with ThreadPoolExecutor(max_workers=3) as pool:
            for key, recs in pool.map(run, jobs):
                images[key] = recs
                if not recs:
                    print("  no photo:", key)
        OUT.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    for key, (how, val) in OVERRIDES.items():
        picked = commons.article_images(val, 6) if how == "wiki" else commons.search_images(val, 6)
        picked = clean([r for r in picked if r.get("landscape")] + [r for r in picked if not r.get("landscape")])
        if picked:
            images[key] = clean(picked + images.get(key, []))[:6]
        else:
            print("  override found nothing:", key)
    OUT.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    total = len({r["file"] for v in images.values() for r in v})
    print(f"done: {len(images)} keys, {total} unique photos")


if __name__ == "__main__":
    main()
