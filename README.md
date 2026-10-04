# gosikkimtours.com

Django site for Go Sikkim Tours: affordable trips to Sikkim, Darjeeling, Kalimpong, the Dooars
and Bhutan. Every page is rendered from JSON in `content/` (no database content); the database
only stores enquiries and newsletter sign-ups.

## Run it locally

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser      # to read enquiries at /admin/
python manage.py runserver
```

## Project layout

| Path | What it is |
| --- | --- |
| `gst/` | Django settings and root URLs |
| `hills/content.py` | Loads `content/*.json` into an in-memory catalogue (reloads on change in DEBUG) |
| `hills/views.py`, `hills/views_more.py` | Page views |
| `hills/atlas.py` | Self-drawn SVG maps from `content/outlines.json` (no map API) |
| `hills/policies.py` | Policy page drafts (every `[BRACKETED]` value needs confirming) |
| `templates/hills/` | Templates |
| `static/css/site.css`, `static/js/hills.js` | Styles and behaviour |
| `content/` | All site content. See `content/SCHEMA.md` and `content/JOURNAL_SCHEMA.md` |
| `tools/` | Content build and check scripts |

## Editing content

1. Edit or add JSON under `content/<region>/` following `content/SCHEMA.md`.
2. Validate: `python tools/check_region.py <region>` (add `--wiki` to confirm Wikipedia titles).
3. For blog posts: `python tools/build_slugs.py && python tools/check_journal.py`.
4. Photos: `python tools/fetch_images.py [region ...]` adds credited Wikimedia Commons photos to
   `content/images.json` for anything new (`--force` refreshes everything).
5. Render every page: `python tools/smoke.py` must report `0 failures`.

Prices, fares and permit rules in the content are indicative planning figures. Review them each
season.

## Before launch

- Contact details default to hello@gosikkimtours.com and +91 99546 34102 (`SITE` in `gst/settings.py`); override with `GST_EMAIL`,
  `GST_PHONE`, `GST_WHATSAPP` (digits with country code), and the office address.
- Replace the `[BRACKETED]` placeholders in `hills/policies.py`, `templates/hills/about.html`,
  `templates/hills/contact.html` and the footer in `templates/hills/base.html`, and have the
  policies reviewed.
- Production environment: `DJANGO_DEBUG=0`, a long random `DJANGO_SECRET_KEY`,
  `DJANGO_ALLOWED_HOSTS=gosikkimtours.com,www.gosikkimtours.com`, then
  `python manage.py collectstatic` and `GST_HASHED_STATIC=1`. Optional `GST_GA4` for analytics.
