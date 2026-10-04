import re

from django import template

from ..content import catalogue

register = template.Library()
STD_WIDTHS = [500, 960, 1280, 1920]
# Wikimedia only serves thumbnails at its standard widths and refuses hotlinked originals (HTTP 429),
# so every URL we emit is a thumbnail no wider than the original.
WIKI_WIDTHS = [250, 330, 500, 960, 1280, 1920]
_ORIGINAL = re.compile(r"^https://upload\.wikimedia\.org/wikipedia/commons/(?!thumb/)(\w)/(\w\w)/([^/]+)$")
_THUMB = re.compile(r"/(\d+)px-")


def _clean(url):
    return (url or "").split("?")[0]


def _fit(img, w):
    """Largest standard width <= w that is smaller than the original (thumbs at or above it fail)."""
    full = img.get("width") or 0
    ok = [x for x in WIKI_WIDTHS if x <= max(w, WIKI_WIDTHS[0]) and (not full or x < full)]
    return ok[-1] if ok else None


def _at(img, w):
    url = _clean(img.get("thumb") or img.get("url"))
    m = _ORIGINAL.match(url)
    if m:
        a, ab, name = m.groups()
        url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{a}/{ab}/{name}/960px-{name}"
    if "/thumb/" in url and _THUMB.search(url):
        fit = _fit(img, w)
        if fit:
            return _THUMB.sub(f"/{fit}px-", url, count=1)
        return _clean(img.get("url"))  # tiny originals only
    return url


@register.filter
def src(img, w=960):
    if not img:
        return ""
    return _at(img, int(w))


@register.filter
def srcset(img):
    if not img:
        return ""
    widths = sorted({_fit(img, w) for w in STD_WIDTHS} - {None})
    if not widths:
        return ""
    return ", ".join(f"{_at(img, w)} {w}w" for w in widths)


@register.filter
def inr(value):
    """Indian digit grouping: 550000 -> ₹5,50,000."""
    try:
        n = int(value)
    except (TypeError, ValueError):
        return value
    s = str(n)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
        s = f"{head},{tail}"
    return f"₹{s}"


@register.filter
def get(d, key):
    try:
        return d.get(key)
    except AttributeError:
        return None


@register.filter
def first_img(obj):
    imgs = (obj or {}).get("images") or []
    return imgs[0] if imgs else None


@register.filter
def nth_img(obj, n):
    imgs = (obj or {}).get("images") or []
    n = int(n)
    return imgs[n % len(imgs)] if imgs else None


@register.filter
def theme_name(slug):
    t = catalogue().themes.get(slug)
    return t["name"] if t else slug.replace("-", " ").capitalize()


@register.filter
def theme_url(slug):
    t = catalogue().themes.get(slug)
    return t["url"] if t else "#"


@register.filter
def place_obj(slug):
    return catalogue().places.get(slug)


@register.filter
def short_credit(img):
    if not img:
        return ""
    author = re.sub(r"\s+", " ", img.get("author") or "Unknown")
    if len(author) > 48:
        author = author[:46] + "…"
    return f"{author} · {img.get('license')}"


@register.filter
def lower_first(s):
    return s[:1].lower() + s[1:] if s else s


@register.filter
def pad2(n):
    return f"{int(n):02d}"


@register.inclusion_tag("hills/partials/photo.html")
def photo(img, alt="", cls="", sizes="(max-width: 760px) 100vw, 50vw", eager=False, credit=True):
    return {"img": img, "alt": alt or (img or {}).get("description") or "", "cls": cls, "sizes": sizes,
            "eager": eager, "credit": credit}


@register.simple_tag
def icon(name, cls=""):
    """Inline line icon from hills/icons.py."""
    from django.utils.safestring import mark_safe

    from ..icons import svg
    return mark_safe(svg(name, cls))


@register.simple_tag
def atlas(points, region=None, route=False):
    """Self-drawn SVG map (no API key, no tiles). See hills/atlas.py."""
    from django.utils.safestring import mark_safe

    from ..atlas import atlas_svg
    return mark_safe(atlas_svg(points, region=region, route=route))
