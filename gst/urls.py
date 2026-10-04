from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from hills.sitemaps import SITEMAPS

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("hills.urls")),
]

handler404 = "hills.views.not_found"
