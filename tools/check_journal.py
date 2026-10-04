"""Validate content/journal/*.json against content/JOURNAL_SCHEMA.md.

Usage: python tools/check_journal.py [slug ...]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
sys.path.insert(0, str(Path(__file__).parent))
from check_region import BANNED  # noqa: E402

slugs = json.loads((ROOT / "_slugs.json").read_text(encoding="utf-8"))
known = {k: set() for k in ("place", "journey", "stay", "guide", "festival")}
for land in slugs.values():
    for k in known:
        known[k] |= set(land[k + "s"])
errors, warns = [], []
only = set(sys.argv[1:])
files = sorted((ROOT / "journal").glob("*.json"))
seen = set()
for f in files:
    if only and f.stem not in only:
        continue
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        errors.append(f"{f.name}: invalid JSON ({e})")
        continue
    w = f.name
    if d.get("slug") != f.stem:
        errors.append(f"{w}: slug must equal filename")
    if d["slug"] in seen:
        errors.append(f"{w}: duplicate slug")
    seen.add(d["slug"])
    for k in ("title", "category", "date", "regions", "meta_description", "summary", "sections", "faqs", "cta"):
        if not d.get(k):
            errors.append(f"{w}: missing {k}")
    if d.get("title", "").endswith("."):
        errors.append(f"{w}: title ends with full stop")
    if len(d.get("meta_description", "")) > 158:
        errors.append(f"{w}: meta_description over 158 chars")
    if len(d.get("faqs", [])) != 5:
        errors.append(f"{w}: needs exactly 5 faqs")
    if len(d.get("key_takeaways", [])) != 4:
        errors.append(f"{w}: needs exactly 4 key_takeaways")
    for r in d.get("regions", []):
        if r not in slugs:
            errors.append(f"{w}: unknown region {r}")
    for s in d.get("related_journeys", []):
        if s not in known["journey"]:
            errors.append(f"{w}: unknown journey {s}")
    for s in d.get("related_places", []):
        if s not in known["place"]:
            errors.append(f"{w}: unknown place {s}")
    words = 0
    has_table = False
    for sec in d.get("sections", []):
        if sec.get("heading", "").endswith("."):
            errors.append(f"{w}: heading ends with full stop: {sec['heading']}")
        words += len(" ".join(sec.get("paras", []) + sec.get("list", [])).split())
        has_table = has_table or bool(sec.get("table"))
        for ln in sec.get("links", []):
            if ln.get("type") not in known or ln.get("slug") not in known[ln.get("type")]:
                errors.append(f"{w}: bad link {ln}")
    if not has_table:
        errors.append(f"{w}: needs at least one table")
    if words < 1050:
        errors.append(f"{w}: only {words} words")
    text = json.dumps(d, ensure_ascii=False).lower()
    for b in BANNED:
        if b in text:
            warns.append(f"{w}: banned '{b}'")
print(f"{len(seen)} posts")
for x in warns:
    print("WARN", x)
for x in errors:
    print("ERROR", x)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
