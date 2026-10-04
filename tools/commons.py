"""Wikimedia Commons image lookup with full attribution.

Only freely licensed files are kept (CC0, Public domain, CC BY, CC BY-SA).
Every record carries author, license and the Commons source page so the site
can credit the photo under the image and on /photo-credits/.
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request

UA = "GoSikkimToursBuild/1.0 (https://gosikkimtours.com; content build script)"
WIKI_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
OK_LICENSES = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[1-4]\.0|cc by(-sa)?$|cc by(-sa)? [1-4]\.0)", re.I)
SKIP_WORDS = re.compile(r"(map|locator|logo|flag|emblem|seal|diagram|chart|icon|svg|coat of arms|plan\b|banner|kingdom|empire|dynasty|"
                        r"subah|BCE|\bc\. ?\d|institute|walden|massachusetts|political|with rivers|b1[5-8]ddb|\.png$)", re.I)


def _get(api, params, tries=3):
    params = {**params, "format": "json", "formatversion": "2"}
    url = api + "?" + urllib.parse.urlencode(params)
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return {}


def _strip(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()


def _record(page, width):
    info = (page.get("imageinfo") or [None])[0]
    if not info:
        return None
    meta = info.get("extmetadata", {})
    lic = _strip(meta.get("LicenseShortName", {}).get("value", ""))
    if not OK_LICENSES.search(lic):
        return None
    if info.get("width", 0) < 1000 or info.get("height", 0) < 600:
        return None
    if info.get("mime") not in ("image/jpeg", "image/webp"):  # PNGs on Wikipedia are mostly maps and banners
        return None
    title = page["title"]
    if SKIP_WORDS.search(title):
        return None
    author = _strip(meta.get("Artist", {}).get("value", "")) or "Unknown author"
    author = re.sub(r"\s+", " ", author)[:120]
    desc = _strip(meta.get("ImageDescription", {}).get("value", ""))
    desc = re.sub(r"\s+", " ", desc)[:220]
    return {
        "file": title,
        "url": info.get("url"),
        "thumb": info.get("thumburl") or info.get("url"),
        "width": info.get("width"),
        "height": info.get("height"),
        "landscape": info.get("width", 0) >= info.get("height", 1),
        "description": desc,
        "author": author,
        "license": lic,
        "license_url": meta.get("LicenseUrl", {}).get("value", ""),
        "source": info.get("descriptionurl"),
    }


def file_info(titles, width=1600):
    """Metadata for a list of 'File:...' titles."""
    out = []
    for i in range(0, len(titles), 20):
        data = _get(COMMONS_API, {
            "action": "query", "titles": "|".join(titles[i:i + 20]),
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": width,
        })
        for page in data.get("query", {}).get("pages", []):
            rec = _record(page, width)
            if rec:
                out.append(rec)
    return out


def article_images(wiki_title, limit=12, width=1600):
    """Images used on an English Wikipedia article, lead image first."""
    lead = _get(WIKI_API, {"action": "query", "titles": wiki_title, "redirects": 1,
                           "prop": "pageimages", "piprop": "name"})
    pages = lead.get("query", {}).get("pages", [])
    lead_name = pages[0].get("pageimage") if pages else None
    imgs = _get(WIKI_API, {"action": "query", "titles": wiki_title, "redirects": 1,
                           "prop": "images", "imlimit": 50})
    names = []
    if lead_name:
        names.append("File:" + lead_name.replace("_", " "))
    for p in imgs.get("query", {}).get("pages", []):
        for im in p.get("images", []):
            t = im["title"]
            if t not in names and re.search(r"\.(jpe?g|png|webp)$", t, re.I) and not SKIP_WORDS.search(t):
                names.append(t)
    names = names[: limit * 2]
    recs = file_info(names, width)
    order = {n: i for i, n in enumerate(names)}
    recs.sort(key=lambda r: order.get(r["file"], 999))
    return recs[:limit]


def search_images(query, limit=6, width=1600):
    data = _get(COMMONS_API, {
        "action": "query", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": limit * 3,
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": width,
    })
    pages = sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 0))
    out = [r for r in (_record(p, width) for p in pages) if r]
    return out[:limit]


if __name__ == "__main__":
    import sys
    print(json.dumps(article_images(sys.argv[1], 4), indent=2))
