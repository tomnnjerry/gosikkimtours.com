import re
from urllib.parse import quote

from django.conf import settings

from .content import KINDS, catalogue
from .policies import POLICIES


def _asset_version():
    """Changes whenever a CSS/JS file changes, so browsers never run a stale copy."""
    from pathlib import Path
    root = Path(settings.BASE_DIR) / "static"
    return int(max((p.stat().st_mtime for p in root.rglob("*") if p.suffix in (".css", ".js")), default=0))


def site(request):
    cat = catalogue()
    S = settings.SITE
    regions = list(cat.regions.values())
    phone_digits = re.sub(r"\D", "", S.get("phone", ""))
    wa = re.sub(r"\D", "", S.get("whatsapp", ""))
    popular = []
    for r in regions:  # one mid-priced journey per land
        js = sorted(r["journeys"], key=lambda j: j.get("price_from_inr", 0))
        if js:
            popular.append(js[len(js) // 2])
    return {
        "SITE": S,
        "nav_regions": regions,
        "nav_themes": list(cat.themes.values()),
        "nav_kinds": [(k, v[0]) for k, v in KINDS.items()],
        "nav_popular": popular,
        "nav_posts": list(cat.posts.values())[:3],
        "nav_policies": [(k, v["nav"]) for k, v in POLICIES.items()],
        "counts": cat.counts(),
        "canonical": S["url"] + request.path,
        "tel": f"+{phone_digits}" if len(phone_digits) >= 10 else "",
        "wa_base": f"https://wa.me/{wa}" if len(wa) >= 10 else "",
        "wa_text": quote(f"Hello Go Sikkim Tours, I would like to plan a journey. (Page: {S['url']}{request.path})"),
        "GA4": getattr(settings, "GA4_ID", ""),
        "V": _asset_version(),
    }
