"""Экспорт всех экранов и листов prototypes.html в PNG @2x через headless Chrome.
Список берётся из самого HTML; высота обрезается автоматически по фону-маркеру #FF00FF.
  python -I src/export.py
"""
import pathlib, re, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = ROOT / "export"
OUT.mkdir(exist_ok=True)
html = (ROOT / "prototypes.html").read_text(encoding="utf-8")
items = re.findall(r'<section class="(screen|sheet)[^"]*" id="([\w-]+)"(?: data-name="([^"]+)")?', html)
url = (ROOT / "prototypes.html").as_uri()
for f in OUT.glob("*.png"):
    f.unlink()

SHEETS = {"cover": "00-oblozhka", "ds": "00-dizain-sistema"}
for i, (kind, sid, name) in enumerate(items):
    w, h = (1600, 3200) if kind == "sheet" else (375, 1600)
    fname = SHEETS.get(sid) or re.sub(r"[^\w-]+", "-", name.lower()).strip("-")
    out = OUT / f"{fname}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={w},{h}", "--virtual-time-budget=4000", f"--screenshot={out}", f"{url}#only={sid}&mark=1"],
                   check=True, capture_output=True)
    im = Image.open(out).convert("RGB")
    px = im.load(); W, H = im.size
    bottom = H
    for y in range(H - 1, 0, -1):
        if any(px[x, y] != (255, 0, 255) for x in range(0, W, 7)):
            bottom = y + 1
            break
    im.crop((0, 0, W, bottom)).save(out, optimize=True)
    print(out.name, W, "x", bottom)
