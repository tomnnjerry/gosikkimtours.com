"""Build content/_slugs.json: every slug per region, used by tools/check_journal.py.

Usage: python tools/build_slugs.py   (run after adding or renaming content)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
REGIONS = ["east-sikkim", "north-sikkim", "west-sikkim", "darjeeling", "kalimpong", "dooars", "bhutan"]


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    out = {}
    for r in REGIONS:
        base = ROOT / r
        if not (base / "region.json").exists():
            continue
        lists = {name: read(base / f"{name}.json") if (base / f"{name}.json").exists() else [] for name in ("stays", "festivals")}
        out[r] = {
            "places": sorted(p.stem for p in (base / "places").glob("*.json")),
            "journeys": sorted(p.stem for p in (base / "journeys").glob("*.json")),
            "guides": sorted(p.stem for p in (base / "guides").glob("*.json")),
            "stays": [s["slug"] for s in lists["stays"]],
            "festivals": [f["slug"] for f in lists["festivals"]],
        }
    (ROOT / "_slugs.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} regions, {sum(len(v['places']) for v in out.values())} places")


if __name__ == "__main__":
    main()
