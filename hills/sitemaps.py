from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import KINDS, MONTHS, catalogue


class StaticSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return ["home", "lands", "journeys", "stays", "experiences", "guides", "festivals", "routes", "themes",
                "seasons", "tools", "tool_season", "tool_budget", "tool_permits", "tool_altitude", "stories", "fares", "plan", "about", "faq",
                "photo_credits", "html_sitemap", "journal", "policies", "contact", "how_we_work"]

    def location(self, item):
        return reverse(item)


class ContentSitemap(Sitemap):
    def items(self):
        cat = catalogue()
        urls = []
        for store in (cat.regions, cat.places, cat.experiences, cat.journeys, cat.stays, cat.guides,
                      cat.festivals, cat.routes, cat.themes, cat.stories):
            urls += [o["url"] for o in store.values()]
        for r in cat.regions:
            urls += [reverse("region_month", args=[r, m.lower()]) for m in MONTHS]
        urls += [reverse("region_theme", args=[r, t]) for r, t in cat.region_theme_pairs()]
        urls += [reverse("experience_kind", args=[k]) for k in KINDS]
        urls += [d["url"] for d in cat.posts.values()]
        urls += [reverse("journal_cat", args=[k]) for k in cat.post_categories]
        from .policies import POLICIES
        urls += [reverse("policy", args=[k]) for k in POLICIES]
        urls += [reverse("region_kind", args=[r, k]) for r, k in cat.region_kind_pairs()]
        return urls

    def location(self, item):
        return item


SITEMAPS = {"static": StaticSitemap, "content": ContentSitemap}
