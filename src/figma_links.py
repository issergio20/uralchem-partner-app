"""Из data-go связей prototypes.html генерирует figma/prototype.js — скрипт use_figma,
который на странице с импортированными экранами:
  • переименовывает фреймы по data-name (порядок как в HTML),
  • делает экраны 375×812 со скроллом по вертикали,
  • вешает ON_CLICK → NAVIGATE (по тексту кликабельного элемента) и BACK (кнопка-стрелка в шапке),
  • ставит стартовую точку flow «Вход».
Запуск: python -I src/figma_links.py
"""
import json, pathlib, re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / "prototypes.html").read_text(encoding="utf-8")
VOID = {"img", "br", "input", "meta", "link", "hr"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.screen = None; self.names = {}; self.order = []
        self.stack = []; self.open = []; self.links = []; self.texts = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "screen" in (a.get("class") or ""):
            self.screen = a["id"]; self.names[a["id"]] = a.get("data-name", a["id"]); self.order.append(a["id"])
        if tag in VOID:
            return
        self.stack.append(tag)
        if "data-go" in a and self.screen:
            self.open.append({"depth": len(self.stack), "go": a["data-go"], "text": "", "screen": self.screen})

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        d = len(self.stack)
        while self.open and self.open[-1]["depth"] == d:
            self.links.append(self.open.pop())
        self.stack.pop()
        if tag == "section":
            self.screen = None

    def handle_data(self, data):
        for o in self.open:
            o["text"] += data
        t = re.sub(r"\s+", " ", data).strip()
        if self.screen and len(t) >= 8:
            self.texts.setdefault(self.screen, []).append(t)


p = P(); p.feed(html)
names = p.names
links = []
for l in p.links:
    t = re.sub(r"\s+", " ", l["text"]).strip()
    t = re.sub(r"^\d+\s*", "", t) if l["go"] != "back" else t  # бейджи-цифры в начале
    links.append({"from": names[l["screen"]], "to": "BACK" if l["go"] == "back" else names[l["go"]], "text": t[:40]})

data = {"order": [names[i] for i in p.order], "links": links, "start": names.get("s-login")}
# уникальный текст каждого экрана — по нему плагин находит экран после захвата страницы
from collections import Counter
cnt = Counter(t for sid in p.order for t in set(p.texts.get(sid, [])))
unique = {}
for sid in p.order:
    cands = [t for t in p.texts.get(sid, []) if cnt[t] == 1]
    assert cands, f"нет уникального текста у {sid}"
    unique[names[sid]] = cands[:3]
(ROOT / "figma" / "links.json").write_text(json.dumps({**data, "unique": unique}, ensure_ascii=False, indent=1), encoding="utf-8")
JS = r"""// Сгенерировано src/figma_links.py — кликабельный прототип. Запускать на странице с экранами.
// SCREEN_IDS: id импортированных фреймов экранов в порядке HTML (подставить из ответа html_to_figma).
const SCREEN_IDS = __IDS__;
const D = __DATA__;
const frames = [];
for (let i = 0; i < SCREEN_IDS.length; i++) { const f = await figma.getNodeByIdAsync(SCREEN_IDS[i]); f.name = D.order[i]; frames.push(f); }
const byName = Object.fromEntries(frames.map(f => [f.name, f]));
// экраны 375×812 со скроллом
for (const f of frames) { if (f.height > 812) { f.clipsContent = true; f.overflowDirection = 'VERTICAL'; f.resizeWithoutConstraints(375, 812); } }
const norm = s => s.replace(/\s+/g, ' ').trim();
const out = { linked: 0, missed: [] };
const trans = { type: 'DISSOLVE', easing: { type: 'EASE_OUT' }, duration: 0.18 };
function holder(f, t) { // поднимаемся от текста до ближайшего контейнера с фоном/рамкой, но не выше экрана
  let n = t.parent, best = t.parent;
  while (n && n !== f) { if ('fills' in n && Array.isArray(n.fills) && n.fills.length) { best = n; break; } n = n.parent; }
  return best === f ? t : best;
}
for (const L of D.links) {
  const f = byName[L.from]; if (!f) continue;
  let target = null;
  if (L.to === 'BACK') {
    target = f.findOne(n => n.type !== 'TEXT' && Math.abs(n.width - 40) < 2 && Math.abs(n.height - 40) < 2 && n.absoluteBoundingBox.y - f.absoluteBoundingBox.y < 120 && n.absoluteBoundingBox.x - f.absoluteBoundingBox.x < 30);
  } else if (L.text) {
    const key = norm(L.text).slice(0, 18);
    const t = f.findOne(n => n.type === 'TEXT' && norm(n.characters).startsWith(key)) || f.findOne(n => n.type === 'TEXT' && key.startsWith(norm(n.characters)) && norm(n.characters).length > 3);
    if (t) target = holder(f, t);
  }
  if (!target) { out.missed.push(L.from + ' → ' + L.to + ' «' + L.text + '»'); continue; }
  const action = L.to === 'BACK' ? { type: 'BACK' } : { type: 'NODE', destinationId: byName[L.to].id, navigation: 'NAVIGATE', transition: trans, preserveScrollPosition: false };
  await target.setReactionsAsync([{ trigger: { type: 'ON_CLICK' }, actions: [action] }]);
  out.linked++;
}
const start = byName[D.start]; if (start) figma.currentPage.flowStartingPoints = [{ nodeId: start.id, name: 'Прототип УРАЛХИМ' }];
return out;
"""
(ROOT / "figma").mkdir(exist_ok=True)
(ROOT / "figma" / "prototype.js").write_text(JS.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print(len(p.order), "screens,", len(links), "links,", sum(1 for l in links if not l["text"] and l["to"] != "BACK"), "icon-only (skipped in Figma)")
