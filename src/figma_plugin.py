"""Собирает локальный плагин Figma: figma-plugin/manifest.json + code.js.
Команды: 1) Разложить экраны  2) Переменные и стили  3) Кликабельный прототип  · Всё сразу.
Берёт figma/links.json (src/figma_links.py) и тело figma/variables.js (src/tokens.py).
  python -I src/figma_plugin.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
links = json.loads((ROOT / "figma" / "links.json").read_text(encoding="utf-8"))
var_body = (ROOT / "figma" / "variables.js").read_text(encoding="utf-8")
OUT = ROOT / "figma-plugin"
OUT.mkdir(exist_ok=True)

manifest = {
    "name": "УРАЛХИМ · макеты, токены, прототип",
    "id": "uralchem-redesign-local",
    "api": "1.0.0",
    "main": "code.js",
    "editorType": ["figma"],
    "documentAccess": "dynamic-page",
    "networkAccess": {"allowedDomains": ["none"]},
    "menu": [
        {"name": "1. Разложить экраны", "command": "layout"},
        {"name": "2. Переменные и стили", "command": "vars"},
        {"name": "3. Кликабельный прототип", "command": "proto"},
        {"separator": True},
        {"name": "Всё сразу (1 → 2 → 3)", "command": "all"},
    ],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

CODE = r"""// УРАЛХИМ · локальный плагин. Сгенерировано src/figma_plugin.py — не править руками.
const L = __LINKS__;
const norm = s => (s || '').replace(/\s+/g, ' ').trim();
const SECTION = 'Редизайн 2026 · 22 экрана';
const INSP = new Set(['08 Инспектор — задачи, офлайн', '20 Инспекция — чек-лист', '21 Новое замечание', '22 Синхронизация']);

function hasText(root, list, exact) {
  return !!root.findOne(n => n.type === 'TEXT' && list.some(t => { const c = norm(n.characters); return c === t || (!exact && c.startsWith(t)); }));
}

// ---------- 1. Найти экраны в захвате и разложить ----------
async function layout() {
  const page = figma.currentPage;
  const already = page.findOne(n => n.type === 'SECTION' && n.name === SECTION);
  const pool = page.findAll(n => n.type === 'FRAME' && Math.abs(n.width - 375) < 2 && n.height >= 700);
  const found = {}, used = new Set();
  // два прохода: сначала точное совпадение подписи, потом по началу строки; фрейм достаётся одному экрану
  for (const exact of [true, false]) {
    for (const name of L.order) {
      if (found[name]) continue;
      const c = pool.filter(f => !used.has(f) && ![...used].some(u => u.findOne(n => n === f) || f.findOne(n => n === u)) && hasText(f, L.unique[name], exact)).sort((a, b) => a.height - b.height);
      if (c.length === 1 || (c.length > 1 && !exact)) { found[name] = c[0]; used.add(c[0]); }
      else if (c.length > 1 && exact) { // несколько вложенных кандидатов (подпись + экран) — берём самый низкий, если они вложены друг в друга
        if (c.every(x => x === c[0] || x.findOne(n => n === c[0]))) { found[name] = c[0]; used.add(c[0]); }
      }
    }
  }
  const miss = L.order.filter(n => !found[n]);
  if (!Object.keys(found).length) throw new Error('Экраны не найдены. Сначала захватите prototypes.html на эту страницу.');
  const sec = already || figma.createSection(); sec.name = SECTION; if (!already) page.appendChild(sec);
  const wrappers = new Set();
  let xb = 120, xi = 120; const y1 = 200, y2 = 200 + 1500 + 260;
  for (const name of L.order) {
    const f = found[name]; if (!f) continue;
    let top = f; while (top.parent && top.parent.type !== 'PAGE' && top.parent !== sec) top = top.parent;
    if (top !== f && top.parent && top.parent.type === 'PAGE') wrappers.add(top);
    sec.appendChild(f); f.name = name;
    if (INSP.has(name)) { f.x = xi; f.y = y2; xi += 455; } else { f.x = xb; f.y = y1; xb += 455; }
  }
  // обложка и дизайн-система → страница «Кейс»
  const sheets = page.findAll(n => n.type === 'FRAME' && Math.abs(n.width - 1600) < 2);
  const cover = sheets.find(f => hasText(f, ['УРАЛХИМ — Личный кабинет партнёра.'])) ;
  const ds = sheets.find(f => hasText(f, ['Токены и компоненты']));
  let kase = figma.root.children.find(p => p.name === 'Кейс');
  if ((cover || ds) && !kase) { kase = figma.createPage(); kase.name = 'Кейс'; figma.root.insertChild(0, kase); }
  if (cover) { let t = cover; while (t.parent && t.parent.type !== 'PAGE') t = t.parent; if (t !== cover) wrappers.add(t); kase.appendChild(cover); cover.name = '00 Обложка кейса'; cover.x = 0; cover.y = 0; }
  if (ds) { let t = ds; while (t.parent && t.parent.type !== 'PAGE') t = t.parent; if (t !== ds) wrappers.add(t); kase.appendChild(ds); ds.name = '00 Дизайн-система'; ds.x = 1760; ds.y = 0; }
  page.name = 'Прототипы';
  // остатки захвата убираем в сторону и прячем
  let wy = y2 + 1800;
  for (const w of wrappers) { if (w.removed) continue; w.name = 'Захват страницы — остаток, можно удалить'; w.x = 0; w.y = wy; w.visible = false; wy += w.height + 200; }
  // подписи рядов
  await figma.loadFontAsync({ family: 'Onest', style: 'SemiBold' }).catch(() => figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' }));
  if (!already) {
    for (const [t, y] of [['Покупатель / дистрибьютор · 18 экранов', 90], ['Инспектор · работа офлайн · 4 экрана', y2 - 110]]) {
      const n = figma.createText();
      try { n.fontName = { family: 'Onest', style: 'SemiBold' }; } catch (e) { n.fontName = { family: 'Inter', style: 'Semi Bold' }; }
      n.fontSize = 48; n.characters = t; sec.appendChild(n); n.x = 120; n.y = y;
    }
  }
  sec.resizeWithoutConstraints(Math.max(xb, xi) + 40, y2 + 1500 + 160);
  return `Экраны: ${Object.keys(found).length} из ${L.order.length}` + (miss.length ? ` (не найдены: ${miss.join(', ')})` : '') + (cover ? ', обложка' : '') + (ds ? ', дизайн-система' : '');
}

// ---------- 2. Переменные, стили, привязка ----------
async function vars() {
__VARS__
}

// ---------- 3. Прототип ----------
async function proto() {
  const page = figma.currentPage;
  const byName = {};
  for (const name of L.order) { const f = page.findOne(n => n.type === 'FRAME' && n.name === name); if (f) byName[name] = f; }
  if (!Object.keys(byName).length) throw new Error('Сначала выполните «1. Разложить экраны».');
  for (const f of Object.values(byName)) { if (f.height > 812) { f.clipsContent = true; f.overflowDirection = 'VERTICAL'; f.resizeWithoutConstraints(375, 812); } }
  // ряды после обрезки до 812
  const sec = page.findOne(n => n.type === 'SECTION' && n.name === SECTION);
  if (sec) { for (const n of sec.children) { if (n.type === 'FRAME' && INSP.has(n.name)) n.y = 200 + 812 + 260; if (n.type === 'TEXT' && n.characters.startsWith('Инспектор')) n.y = 200 + 812 + 150; } sec.resizeWithoutConstraints(sec.width, 200 + 812 * 2 + 260 + 160); }
  const trans = { type: 'DISSOLVE', easing: { type: 'EASE_OUT' }, duration: 0.18 };
  const holder = (f, t) => { let n = t.parent; while (n && n !== f) { if ('fills' in n && Array.isArray(n.fills) && n.fills.length) return n; n = n.parent; } return t; };
  let ok = 0; const miss = [];
  for (const k of L.links) {
    const f = byName[k.from]; if (!f) continue;
    let target = null;
    if (k.to === 'BACK') {
      target = f.findOne(n => n.type !== 'TEXT' && Math.abs(n.width - 40) < 2 && Math.abs(n.height - 40) < 2 && n.absoluteBoundingBox.y - f.absoluteBoundingBox.y < 130 && n.absoluteBoundingBox.x - f.absoluteBoundingBox.x < 30);
    } else if (k.text && byName[k.to]) {
      const key = norm(k.text).slice(0, 18);
      const t = f.findOne(n => n.type === 'TEXT' && norm(n.characters).startsWith(key)) || f.findOne(n => n.type === 'TEXT' && norm(n.characters).length > 3 && key.startsWith(norm(n.characters)));
      if (t) target = holder(f, t);
    }
    if (!target) { miss.push(k.from + ' → ' + k.to); continue; }
    const action = k.to === 'BACK' ? { type: 'BACK' } : { type: 'NODE', destinationId: byName[k.to].id, navigation: 'NAVIGATE', transition: trans, preserveScrollPosition: false };
    await target.setReactionsAsync([{ trigger: { type: 'ON_CLICK' }, actions: [action] }]);
    ok++;
  }
  if (byName[L.start]) page.flowStartingPoints = [{ nodeId: byName[L.start].id, name: 'Прототип УРАЛХИМ' }];
  return `Переходов: ${ok} из ${L.links.length}` + (miss.length ? ` (без пары: ${miss.length})` : '') + '. Запуск: Present';
}

(async () => {
  const cmd = figma.command || 'all';
  const msgs = [];
  try {
    if (cmd === 'layout' || cmd === 'all') msgs.push(await layout());
    if (cmd === 'vars' || cmd === 'all') { const r = await vars(); msgs.push(`Переменных ${r.created.variables}, стилей ${r.created.textStyles}; привязано заливок ${r.bound.fills}, радиусов ${r.bound.radius}, текстов ${r.bound.text}`); }
    if (cmd === 'proto' || cmd === 'all') msgs.push(await proto());
    figma.closePlugin('УРАЛХИМ: ' + msgs.join(' · '));
  } catch (e) {
    figma.closePlugin('УРАЛХИМ, ошибка: ' + (e && e.message || e) + (msgs.length ? ' · сделано: ' + msgs.join(' · ') : ''));
  }
})();
"""
code = CODE.replace("__LINKS__", json.dumps(links, ensure_ascii=False)).replace("__VARS__", var_body)
(OUT / "code.js").write_text(code, encoding="utf-8")
print("figma-plugin/manifest.json + code.js", len(code), "chars")
