"""Собирает figma/run.js — ОДИН вызов use_figma, который после импорта:
  1) раскладывает: страница «Кейс» (обложка + дизайн-система), текущая страница → «Прототипы» (секция с экранами),
  2) прототип: имена, 375×812 со скроллом, переходы, стартовая точка (figma/prototype.js),
  3) переменные, текстовые стили и привязка (figma/variables.js).
Каждая фаза в try/catch — частичный успех возвращается.
  python -I src/figma_compose.py '<json: {"cover":id,"ds":id,"screens":[22 ids в порядке HTML]}>'
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ids = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {"cover": "0:0", "ds": "0:0", "screens": []}
var_js = (ROOT / "figma" / "variables.js").read_text(encoding="utf-8")
proto_js = (ROOT / "figma" / "prototype.js").read_text(encoding="utf-8").replace("__IDS__", json.dumps(ids["screens"]))

layout = r"""
const IDS = __IDS__;
const proto = figma.currentPage; proto.name = 'Прототипы';
let kase = figma.root.children.find(p => p.name === 'Кейс');
if (!kase) { kase = figma.createPage(); kase.name = 'Кейс'; }
figma.root.insertChild(0, kase);
const cover = await figma.getNodeByIdAsync(IDS.cover), ds = await figma.getNodeByIdAsync(IDS.ds);
cover.name = '00 Обложка кейса'; ds.name = '00 Дизайн-система';
kase.appendChild(cover); cover.x = 0; cover.y = 0;
kase.appendChild(ds); ds.x = cover.width + 160; ds.y = 0;
// пустые страницы кроме двух наших — удалить
for (const p of [...figma.root.children]) { if (p !== kase && p !== proto && p.children.length === 0) p.remove(); }
return { kase: kase.id, proto: proto.id };
"""

place = r"""
const IDS = __IDS__;
const fr = []; for (const id of IDS.screens) fr.push(await figma.getNodeByIdAsync(id));
const INSP = new Set([7, 19, 20, 21]); // 08, 20, 21, 22
let sec = figma.currentPage.findOne(n => n.type === 'SECTION' && n.name.startsWith('Редизайн'));
if (!sec) { sec = figma.createSection(); sec.name = 'Редизайн 2026 · 22 экрана'; figma.currentPage.appendChild(sec); }
sec.x = 0; sec.y = 0;
let xb = 120, xi = 120; const y1 = 200, y2 = 200 + 812 + 260;
for (let i = 0; i < fr.length; i++) { const f = fr[i]; sec.appendChild(f); if (INSP.has(i)) { f.x = xi; f.y = y2; xi += 375 + 80; } else { f.x = xb; f.y = y1; xb += 375 + 80; } }
// подписи рядов
await figma.loadFontAsync({ family: 'Onest', style: 'SemiBold' });
const mk = (t, y) => { const n = figma.createText(); n.fontName = { family: 'Onest', style: 'SemiBold' }; n.fontSize = 48; n.characters = t; sec.appendChild(n); n.x = 120; n.y = y; return n; };
mk('Покупатель / дистрибьютор · 18 экранов', 90); mk('Инспектор · работа офлайн · 4 экрана', y2 - 110);
sec.resizeWithoutConstraints(Math.max(xb, xi) + 40, y2 + 812 + 160);
return { section: sec.id };
"""

JS = f"""// Сгенерировано src/figma_compose.py. Один вызов use_figma после html_to_figma.
const RES = {{}};
async function phase(name, fn) {{ try {{ RES[name] = await fn(); }} catch (e) {{ RES[name] = {{ error: String(e && e.message || e) }}; }} }}
await phase('layout', async () => {{ {layout.replace('__IDS__', json.dumps(ids))} }});
await phase('prototype', async () => {{ {proto_js} }});
await phase('place', async () => {{ {place.replace('__IDS__', json.dumps(ids))} }});
await phase('variables', async () => {{ {var_js} }});
try {{ const s = figma.currentPage.findOne(n => n.type === 'SECTION'); if (s) await s.screenshot({{ scale: 0.12 }}); }} catch (e) {{ RES.shot = String(e); }}
return RES;
"""
out = ROOT / "figma" / "run.js"
out.write_text(JS, encoding="utf-8")
print("figma/run.js", len(JS), "chars")
