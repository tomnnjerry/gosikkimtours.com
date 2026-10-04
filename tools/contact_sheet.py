"""Contact sheet of each place's lead photo, for eyeballing the image set."""
import io, json, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
from commons import UA
ROOT = Path(__file__).resolve().parent.parent
imgs = json.loads((ROOT / "content/images.json").read_text(encoding="utf-8"))
prefix = sys.argv[1] if len(sys.argv) > 1 else "place:"
out = sys.argv[2] if len(sys.argv) > 2 else "sheet.jpg"
keys = sorted(k for k in imgs if k.startswith(prefix))
W, H, cols = 220, 160, 8
rows = (len(keys) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (H + 18)), "white")
d = ImageDraw.Draw(sheet)
for i, k in enumerate(keys):
    x, y = (i % cols) * W, (i // cols) * (H + 18)
    d.text((x + 3, y + H + 3), k.split(":", 1)[1][:34], fill="black")
    if not imgs[k]:
        continue
    url = imgs[k][0]["thumb"].split("?")[0]
    import re
    url = re.sub(r"/\d+px-", "/330px-", url) if "/thumb/" in url else url
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
        im = Image.open(io.BytesIO(data)).convert("RGB"); im.thumbnail((W - 4, H)); sheet.paste(im, (x + 2, y))
    except Exception as e:
        d.text((x + 3, y + 60), "ERR", fill="red")
sheet.save(out, quality=80)
print(out, len(keys))
