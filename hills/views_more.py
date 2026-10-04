"""Journal, policies, contact, how-we-work, newsletter and search index."""
import json

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .content import catalogue
from .forms import EnquiryForm, SubscribeForm
from .models import Subscriber
from .policies import POLICIES, UPDATED
from .views import COMPANY_FAQS, _get, crumbs, faq_ld, img_url, ld, org_ld


def journal(request, cat=None):
    c = catalogue()
    posts = list(c.posts.values())
    category = None
    if cat:
        category = c.post_categories.get(cat)
        if not category:
            raise Http404
        posts = category["posts"]
    trail = [("Blog", reverse("journal"))] + ([(category["name"], request.path)] if category else [])
    items, bc = crumbs(*trail)
    return render(request, "hills/journal.html", {"posts": posts, "category": category,
                                                  "cats": list(c.post_categories.values()), "crumbs": items, "ld": ld(bc)})


def post(request, slug):
    c = catalogue()
    d = _get(c.posts, slug)
    items, bc = crumbs(("Blog", reverse("journal")), (d["title"], d["url"]))
    article = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": d["title"],
               "description": d.get("summary"), "datePublished": d.get("date"), "image": img_url(d),
               "author": {"@type": "Organization", "name": settings.SITE["byline"]},
               "publisher": {"@type": "Organization", "name": settings.SITE["name"]}}
    more = [x for x in c.posts.values() if x is not d and (
        x["cat_slug"] == d["cat_slug"] or set(x.get("regions", [])) & set(d.get("regions", [])))][:3]
    return render(request, "hills/post.html", {"d": d, "more": more, "crumbs": items,
                                               "ld": ld(bc, article, faq_ld(d.get("faqs", [])))})


def policies(request):
    items, bc = crumbs(("Policies", reverse("policies")))
    return render(request, "hills/policies.html", {"policies": [dict(v, slug=k) for k, v in POLICIES.items()],
                                                   "crumbs": items, "ld": ld(bc)})


def policy(request, slug):
    pol = POLICIES.get(slug)
    if not pol:
        raise Http404
    items, bc = crumbs(("Policies", reverse("policies")), (pol["title"], request.path))
    sections = [{"heading": h, "blocks": [b if isinstance(b, dict) else {"p": b} for b in body]} for h, body in pol["sections"]]
    others = [(k, v["nav"]) for k, v in POLICIES.items() if k != slug]
    return render(request, "hills/policy.html", {"pol": pol, "slug": slug, "sections": sections, "others": others,
                                                 "updated": UPDATED, "crumbs": items, "ld": ld(bc)})


def contact(request):
    items, bc = crumbs(("Contact", reverse("contact")))
    form = EnquiryForm(initial={"source_page": request.path, "kind": "quick"})
    return render(request, "hills/contact.html", {"form": form, "crumbs": items, "ld": ld(bc, org_ld())})


def how_we_work(request):
    items, bc = crumbs(("How we work", reverse("how_we_work")))
    return render(request, "hills/how_we_work.html", {"crumbs": items, "counts": catalogue().counts(),
                                                      "faqs": COMPANY_FAQS[:6], "ld": ld(bc, faq_ld(COMPANY_FAQS[:6]))})


def subscribe(request):
    if request.method != "POST":
        return redirect("home")
    form = SubscribeForm(request.POST)
    ok = form.is_valid() and not form.cleaned_data.get("website")
    if ok:
        Subscriber.objects.get_or_create(email=form.cleaned_data["email"].lower(),
                                         defaults={"source_page": form.cleaned_data.get("source_page", "")[:300]})
    return render(request, "hills/subscribed.html", {"ok": ok, "crumbs": crumbs(("Blog", reverse("journal")))[0]})


def search_index(request):
    """Compact JSON index for the on-site search overlay: [title, url, kind, context]."""
    c = catalogue()
    rows = [[r["name"], r["url"], "Destination", r.get("short", "")] for r in c.regions.values()]
    rows += [[p["name"], p["url"], "Place", p["region_obj"]["name"]] for p in c.places.values()]
    rows += [[j["title"], j["url"], f"Package · {j['nights']} nights · from ₹{j.get('price_from_inr', '')}", j["region_obj"]["name"]] for j in c.journeys.values()]
    rows += [[e["title"], e["url"], "Experience", e["place_obj"]["name"]] for e in c.experiences.values()]
    rows += [[s["name"], s["url"], "Stay", s["region_obj"]["name"]] for s in c.stays.values()]
    rows += [[g["title"], g["url"], "Guide", g["region_obj"]["name"]] for g in c.guides.values()]
    rows += [[d["title"], d["url"], "Blog", d.get("category", "")] for d in c.posts.values()]
    rows += [[f["name"], f["url"], "Festival", f["region_obj"]["name"]] for f in c.festivals.values()]
    rows += [[t["name"], t["url"], "Style", ""] for t in c.themes.values()]
    rows += [[st["title"], st["url"], "Story", st["place_obj"]["name"]] for st in c.stories.values()]
    rows += [[f"{rt['from_obj']['name']} to {rt['to_obj']['name']}", rt["url"], "Route and fares", rt["region_obj"]["name"]]
             for rt in c.routes.values() if rt.get("from_obj") and rt.get("to_obj")]
    resp = HttpResponse(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), content_type="application/json")
    resp["Cache-Control"] = "public, max-age=3600"
    return resp
