# Journal (blog) schema

One file per post: `content/journal/<slug>.json`. Validate with `python tools/check_journal.py`
after `python tools/build_slugs.py`. House style is the same as in SCHEMA.md.

```json
{
  "slug": "sikkim-trip-cost",                 // must equal the file name
  "title": "How much does a Sikkim trip cost in 2026",   // no full stop at the end
  "category": "Budget",                       // Budget | Planning | Permits | Seasons | Food | Culture | Wildlife | Trekking
  "date": "2026-09-12",                       // ISO date
  "regions": ["east-sikkim", "north-sikkim"], // region slugs; the first sets the page colour
  "meta_description": "≤158 characters",
  "summary": "2–3 sentence answer to the title's question.",
  "key_takeaways": ["exactly 4 one-sentence takeaways"],
  "sections": [                                // 5–8 sections, 1,050+ words in total, at least one table
    {"heading": "No full stop", "paras": ["..."], "list": ["optional"],
     "table": {"head": ["..."], "rows": [["..."]]},
     "links": [{"type": "journey | place | stay | guide | festival", "slug": "an existing slug"}]}
  ],
  "related_journeys": ["journey slugs"],
  "related_places": ["place slugs"],
  "faqs": [exactly 5 faqs],
  "cta": {"title": "Short call to action", "text": "One sentence."},
  "wiki": "", "image_query": "Commons search for the lead photo"
}
```
