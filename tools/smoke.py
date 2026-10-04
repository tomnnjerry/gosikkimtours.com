"""Render every URL in the sitemap plus utility pages; report failures."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gst.settings")
import django; django.setup()
from django.conf import settings
settings.ALLOWED_HOSTS = ["*"]
from django.test import Client
from hills.sitemaps import SITEMAPS
c = Client()
urls = []
for cls in SITEMAPS.values():
    sm = cls()
    urls += [sm.location(i) for i in sm.items()]
urls += ["/sitemap.xml", "/robots.txt", "/llms.txt", "/does-not-exist/"]
bad = 0
for u in urls:
    try:
        r = c.get(u)
        ok = r.status_code == 200 or (u == "/does-not-exist/" and r.status_code == 404)
        if not ok:
            bad += 1; print(r.status_code, u)
    except Exception as e:
        bad += 1; print("EXC", u, type(e).__name__, str(e)[:300])
print(f"{len(urls)} urls, {bad} failures")
