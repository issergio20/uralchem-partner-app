// Сгенерировано src/figma_compose.py. Один вызов use_figma после html_to_figma.
const RES = {};
async function phase(name, fn) { try { RES[name] = await fn(); } catch (e) { RES[name] = { error: String(e && e.message || e) }; } }
await phase('layout', async () => { 
const IDS = {"cover": "0:0", "ds": "0:0", "screens": []};
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
 });
await phase('prototype', async () => { // Сгенерировано src/figma_links.py — кликабельный прототип. Запускать на странице с экранами.
// SCREEN_IDS: id импортированных фреймов экранов в порядке HTML (подставить из ответа html_to_figma).
const SCREEN_IDS = [];
const D = {"order": ["01 Главная — покупатель", "02 Каталог", "03 Карточка товара", "04 Корзина", "05 Оформление заявки", "06 Заявка — трекинг", "07 Финансы", "08 Инспектор — задачи, офлайн", "09 Вход", "10 Подключение компании по ИНН", "11 Уведомления", "12 Заявки — список", "13 Профиль", "14 Фильтры каталога", "15 Заявка отправлена", "16 Пустая корзина", "17 Чат с менеджером", "18 Обращение по вагону", "19 Новости", "20 Инспекция — чек-лист", "21 Новое замечание", "22 Синхронизация"], "links": [{"from": "01 Главная — покупатель", "to": "11 Уведомления", "text": ""}, {"from": "01 Главная — покупатель", "to": "02 Каталог", "text": "Продукт, марка или NPK"}, {"from": "01 Главная — покупатель", "to": "06 Заявка — трекинг", "text": "Подтвердить"}, {"from": "01 Главная — покупатель", "to": "06 Заявка — трекинг", "text": "Посмотреть"}, {"from": "01 Главная — покупатель", "to": "07 Финансы", "text": "Счёт № 4412 · 1 845 000 ₽Оплатить до 15 "}, {"from": "01 Главная — покупатель", "to": "12 Заявки — список", "text": "Все"}, {"from": "01 Главная — покупатель", "to": "06 Заявка — трекинг", "text": "Вагон 58213470Карбамид марки Б · 68 т≈ 1"}, {"from": "01 Главная — покупатель", "to": "12 Заявки — список", "text": "Все"}, {"from": "01 Главная — покупатель", "to": "07 Финансы", "text": "ФинансыПодробнее Свободный остаток1 274 "}, {"from": "01 Главная — покупатель", "to": "02 Каталог", "text": "Новаязаявка"}, {"from": "01 Главная — покупатель", "to": "04 Корзина", "text": "Повторить№ 1489"}, {"from": "01 Главная — покупатель", "to": "17 Чат с менеджером", "text": "Обращениеменеджеру"}, {"from": "01 Главная — покупатель", "to": "19 Новости", "text": "Новость · 21 окт.«МультиСтарт» — новое б"}, {"from": "01 Главная — покупатель", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "01 Главная — покупатель", "to": "02 Каталог", "text": "Каталог"}, {"from": "01 Главная — покупатель", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "01 Главная — покупатель", "to": "04 Корзина", "text": "Корзина"}, {"from": "01 Главная — покупатель", "to": "13 Профиль", "text": "Профиль"}, {"from": "02 Каталог", "to": "11 Уведомления", "text": ""}, {"from": "02 Каталог", "to": "14 Фильтры каталога", "text": "Фильтры 1"}, {"from": "02 Каталог", "to": "03 Карточка товара", "text": "SOLAR Универсал 18:18:18+3MgO+МЭ N18P18K"}, {"from": "02 Каталог", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "02 Каталог", "to": "02 Каталог", "text": "Каталог"}, {"from": "02 Каталог", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "02 Каталог", "to": "04 Корзина", "text": "Корзина"}, {"from": "02 Каталог", "to": "13 Профиль", "text": "Профиль"}, {"from": "03 Карточка товара", "to": "BACK", "text": ""}, {"from": "03 Карточка товара", "to": "04 Корзина", "text": "В корзину112 400 ₽"}, {"from": "04 Корзина", "to": "16 Пустая корзина", "text": "Очистить"}, {"from": "04 Корзина", "to": "05 Оформление заявки", "text": "Оформить заявку 1"}, {"from": "04 Корзина", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "04 Корзина", "to": "02 Каталог", "text": "Каталог"}, {"from": "04 Корзина", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "04 Корзина", "to": "04 Корзина", "text": "Корзина"}, {"from": "04 Корзина", "to": "13 Профиль", "text": "Профиль"}, {"from": "05 Оформление заявки", "to": "BACK", "text": ""}, {"from": "05 Оформление заявки", "to": "15 Заявка отправлена", "text": "Отправить заявку · 1 426 560 ₽"}, {"from": "06 Заявка — трекинг", "to": "BACK", "text": ""}, {"from": "06 Заявка — трекинг", "to": "18 Обращение по вагону", "text": "Проблема"}, {"from": "06 Заявка — трекинг", "to": "17 Чат с менеджером", "text": "Чат с менеджером"}, {"from": "07 Финансы", "to": "BACK", "text": ""}, {"from": "07 Финансы", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "07 Финансы", "to": "02 Каталог", "text": "Каталог"}, {"from": "07 Финансы", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "07 Финансы", "to": "04 Корзина", "text": "Корзина"}, {"from": "07 Финансы", "to": "13 Профиль", "text": "Профиль"}, {"from": "08 Инспектор — задачи, офлайн", "to": "20 Инспекция — чек-лист", "text": "Начать инспекцию"}, {"from": "08 Инспектор — задачи, офлайн", "to": "21 Новое замечание", "text": "Замечание"}, {"from": "08 Инспектор — задачи, офлайн", "to": "08 Инспектор — задачи, офлайн", "text": "Задачи"}, {"from": "08 Инспектор — задачи, офлайн", "to": "20 Инспекция — чек-лист", "text": "Объекты"}, {"from": "08 Инспектор — задачи, офлайн", "to": "21 Новое замечание", "text": "Замечания"}, {"from": "08 Инспектор — задачи, офлайн", "to": "22 Синхронизация", "text": "Синхр."}, {"from": "08 Инспектор — задачи, офлайн", "to": "08 Инспектор — задачи, офлайн", "text": "Профиль"}, {"from": "09 Вход", "to": "01 Главная — покупатель", "text": "Войти"}, {"from": "09 Вход", "to": "10 Подключение компании по ИНН", "text": "Компания ещё не подключена? Подключение "}, {"from": "10 Подключение компании по ИНН", "to": "BACK", "text": ""}, {"from": "11 Уведомления", "to": "BACK", "text": ""}, {"from": "11 Уведомления", "to": "06 Заявка — трекинг", "text": "Подтвердите график по заявке № 1567Срок "}, {"from": "11 Уведомления", "to": "06 Заявка — трекинг", "text": "Вагон 58213470 — Пермь-СортировочнаяЗаяв"}, {"from": "11 Уведомления", "to": "07 Финансы", "text": "Выставлен счёт № 4412 на 1 845 000 ₽Опла"}, {"from": "11 Уведомления", "to": "12 Заявки — список", "text": "Заявка № 1602 принята менеджеромЛукьянов"}, {"from": "11 Уведомления", "to": "19 Новости", "text": "«Уралхим» на «Агроволге-2026»Новости · 1"}, {"from": "12 Заявки — список", "to": "11 Уведомления", "text": ""}, {"from": "12 Заявки — список", "to": "06 Заявка — трекинг", "text": "№ 1567 · от 02.11Подтверждена Азотофосфа"}, {"from": "12 Заявки — список", "to": "06 Заявка — трекинг", "text": "№ 1489 · от 24.10В пути Карбамид марки Б"}, {"from": "12 Заявки — список", "to": "06 Заявка — трекинг", "text": "№ 1602 · от 07.11Согласование SOLAR Унив"}, {"from": "12 Заявки — список", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "12 Заявки — список", "to": "02 Каталог", "text": "Каталог"}, {"from": "12 Заявки — список", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "12 Заявки — список", "to": "04 Корзина", "text": "Корзина"}, {"from": "12 Заявки — список", "to": "13 Профиль", "text": "Профиль"}, {"from": "13 Профиль", "to": "17 Чат с менеджером", "text": "Написать"}, {"from": "13 Профиль", "to": "07 Финансы", "text": "Финансы и счета1 к оплате"}, {"from": "13 Профиль", "to": "18 Обращение по вагону", "text": "Обращения2"}, {"from": "13 Профиль", "to": "19 Новости", "text": "Новости"}, {"from": "13 Профиль", "to": "09 Вход", "text": "Выйти"}, {"from": "13 Профиль", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "13 Профиль", "to": "02 Каталог", "text": "Каталог"}, {"from": "13 Профиль", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "13 Профиль", "to": "04 Корзина", "text": "Корзина"}, {"from": "13 Профиль", "to": "13 Профиль", "text": "Профиль"}, {"from": "14 Фильтры каталога", "to": "02 Каталог", "text": "Показать 34 продукта"}, {"from": "15 Заявка отправлена", "to": "04 Корзина", "text": "Оформить"}, {"from": "15 Заявка отправлена", "to": "06 Заявка — трекинг", "text": "Открыть заявку"}, {"from": "15 Заявка отправлена", "to": "01 Главная — покупатель", "text": "На главную"}, {"from": "16 Пустая корзина", "to": "04 Корзина", "text": "Повторить заявку"}, {"from": "16 Пустая корзина", "to": "02 Каталог", "text": "Перейти в каталог"}, {"from": "16 Пустая корзина", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "16 Пустая корзина", "to": "02 Каталог", "text": "Каталог"}, {"from": "16 Пустая корзина", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "16 Пустая корзина", "to": "04 Корзина", "text": "Корзина"}, {"from": "16 Пустая корзина", "to": "13 Профиль", "text": "Профиль"}, {"from": "17 Чат с менеджером", "to": "BACK", "text": ""}, {"from": "17 Чат с менеджером", "to": "06 Заявка — трекинг", "text": "Заявка № 1489 · Карбамид, 136 тВ пути"}, {"from": "18 Обращение по вагону", "to": "BACK", "text": ""}, {"from": "18 Обращение по вагону", "to": "06 Заявка — трекинг", "text": "Отправить обращение"}, {"from": "19 Новости", "to": "BACK", "text": ""}, {"from": "19 Новости", "to": "01 Главная — покупатель", "text": "Главная"}, {"from": "19 Новости", "to": "02 Каталог", "text": "Каталог"}, {"from": "19 Новости", "to": "12 Заявки — список", "text": "Заявки"}, {"from": "19 Новости", "to": "04 Корзина", "text": "Корзина"}, {"from": "19 Новости", "to": "13 Профиль", "text": "Профиль"}, {"from": "20 Инспекция — чек-лист", "to": "BACK", "text": ""}, {"from": "20 Инспекция — чек-лист", "to": "21 Новое замечание", "text": "Описать замечание →"}, {"from": "21 Новое замечание", "to": "BACK", "text": ""}, {"from": "21 Новое замечание", "to": "22 Синхронизация", "text": "Сохранить замечание"}, {"from": "22 Синхронизация", "to": "08 Инспектор — задачи, офлайн", "text": "Задачи"}, {"from": "22 Синхронизация", "to": "20 Инспекция — чек-лист", "text": "Объекты"}, {"from": "22 Синхронизация", "to": "21 Новое замечание", "text": "Замечания"}, {"from": "22 Синхронизация", "to": "22 Синхронизация", "text": "Синхр."}, {"from": "22 Синхронизация", "to": "08 Инспектор — задачи, офлайн", "text": "Профиль"}], "start": "09 Вход"};
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
 });
await phase('place', async () => { 
const IDS = {"cover": "0:0", "ds": "0:0", "screens": []};
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
 });
await phase('variables', async () => { // Сгенерировано src/tokens.py из tokens/tokens.json — не править руками.
// Выполняется в use_figma на странице с макетами. Идемпотентно: повторный запуск переиспользует коллекции и стили.
const D = {"prim": {"white": "#FFFFFF", "blue/950": "#1E2050", "blue/900": "#272A6B", "blue/700": "#3A3E8C", "blue/300": "#C9CAE6", "blue/100": "#E8E9F4", "green/700": "#006B3C", "green/600": "#00844A", "green/500": "#00A55A", "green/50": "#E3F5EC", "gray/900": "#232324", "gray/800": "#474850", "gray/600": "#5A6B80", "gray/300": "#B4B4C8", "gray/200": "#DCDDE8", "gray/150": "#E4E5EE", "gray/100": "#EEEFF5", "gray/50": "#F4F5F7", "orange/800": "#8A5300", "orange/500": "#FFA61A", "orange/50": "#FFF1D6", "red/700": "#B42323", "red/500": "#D23C3C", "red/50": "#FDE8E8", "sky/700": "#005FCC", "sky/500": "#0073FF", "sky/50": "#E6F1FF"}, "sem": {"bg": "gray/50", "surface": "white", "surface-2": "gray/100", "surface-3": "gray/150", "surface-brand": "blue/100", "surface-inverse": "blue/900", "surface-dark": "blue/950", "border": "gray/200", "border-strong": "gray/300", "text-primary": "gray/900", "text-secondary": "gray/800", "text-tertiary": "gray/600", "text-brand": "blue/900", "text-on-brand": "white", "text-on-brand-muted": "blue/300", "action-primary": "green/600", "action-primary-pressed": "green/700", "action-brand": "blue/900", "accent": "green/500", "badge": "red/500", "success-fg": "green/600", "success-bg": "green/50", "warning-fg": "orange/800", "warning-bg": "orange/50", "warning-fill": "orange/500", "danger-fg": "red/700", "danger-bg": "red/50", "info-fg": "sky/700", "info-bg": "sky/50"}, "space": {"0": 0, "1": 4, "2": 8, "3": 12, "4": 16, "5": 20, "6": 24, "8": 32, "10": 40, "12": 48}, "radius": {"s": 8, "m": 12, "l": 14, "xl": 16, "2xl": 20, "full": 999}, "size": {"button-l": 52, "button-m": 44, "button-s": 36, "field": 56, "tabbar": 84, "icon": 24, "icon-s": 20, "screen": 375}, "typo": {"display": {"size": 28, "lh": 34, "w": 700}, "h1": {"size": 22, "lh": 28, "w": 700}, "h2": {"size": 18, "lh": 24, "w": 600}, "title": {"size": 16, "lh": 22, "w": 600}, "title-s": {"size": 15, "lh": 21, "w": 600}, "body": {"size": 15, "lh": 22, "w": 400}, "body-s": {"size": 14, "lh": 20, "w": 400}, "caption": {"size": 13, "lh": 18, "w": 400}, "label": {"size": 12, "lh": 16, "w": 600}, "tab": {"size": 11, "lh": 14, "w": 500}}, "family": "Onest"};
const hex = h => ({ r: parseInt(h.slice(1,3),16)/255, g: parseInt(h.slice(3,5),16)/255, b: parseInt(h.slice(5,7),16)/255 });
const toHex = c => '#' + [c.r,c.g,c.b].map(x => Math.round(x*255).toString(16).padStart(2,'0')).join('').toUpperCase();
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const allVars = await figma.variables.getLocalVariablesAsync();
function coll(name){ return cols.find(c=>c.name===name) || figma.variables.createVariableCollection(name); }
function getVar(c, name, type){ return allVars.find(v=>v.variableCollectionId===c.id && v.name===name) || figma.variables.createVariable(name, c, type); }
const out = { created: {}, bound: { fills: 0, strokes: 0, radius: 0, text: 0 } };

// 1. Primitives
const cP = coll('Primitives'); const mP = cP.modes[0].modeId; cP.renameMode(mP, 'Value');
const P = {};
for (const [n, h] of Object.entries(D.prim)) { const v = getVar(cP, 'color/' + n, 'COLOR'); v.setValueForMode(mP, hex(h)); v.scopes = []; v.hiddenFromPublishing = true; P[n] = v; }
// 2. Semantic (alias)
const cS = coll('Tokens'); const mS = cS.modes[0].modeId; cS.renameMode(mS, 'Light');
const S = {};
const scopeFor = n => n.startsWith('text') ? ['TEXT_FILL'] : n.startsWith('border') ? ['STROKE_COLOR'] : ['FRAME_FILL','SHAPE_FILL','STROKE_COLOR','TEXT_FILL'];
for (const [n, ref] of Object.entries(D.sem)) { const v = getVar(cS, 'color/' + n, 'COLOR'); v.setValueForMode(mS, figma.variables.createVariableAlias(P[ref])); v.scopes = scopeFor(n); S[n] = v; }
// 3. Dimensions
const cD = coll('Dimensions'); const mD = cD.modes[0].modeId; cD.renameMode(mD, 'Value');
const R = {};
for (const [k, val] of Object.entries(D.space)) { const v = getVar(cD, 'space/' + k, 'FLOAT'); v.setValueForMode(mD, val); v.scopes = ['GAP','WIDTH_HEIGHT']; }
for (const [k, val] of Object.entries(D.radius)) { const v = getVar(cD, 'radius/' + k, 'FLOAT'); v.setValueForMode(mD, val); v.scopes = ['CORNER_RADIUS']; R[val] = v; }
for (const [k, val] of Object.entries(D.size)) { const v = getVar(cD, 'size/' + k, 'FLOAT'); v.setValueForMode(mD, val); v.scopes = ['WIDTH_HEIGHT']; }
out.created.variables = Object.keys(D.prim).length + Object.keys(D.sem).length + Object.keys(D.space).length + Object.keys(D.radius).length + Object.keys(D.size).length;

// 4. Text styles
const W = { 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold' };
const avail = await figma.listAvailableFontsAsync();
const styleName = w => { const want = W[w]; const f = avail.find(f => f.fontName.family === D.family && f.fontName.style.replace(' ','') === want); return f ? f.fontName.style : want; };
const styles = await figma.getLocalTextStylesAsync();
const TS = {};
for (const [k, t] of Object.entries(D.typo)) {
  const fn = { family: D.family, style: styleName(t.w) }; await figma.loadFontAsync(fn);
  const s = styles.find(s => s.name === 'УРАЛХИМ/' + k) || figma.createTextStyle();
  s.name = 'УРАЛХИМ/' + k; s.fontName = fn; s.fontSize = t.size; s.lineHeight = { unit: 'PIXELS', value: t.lh };
  TS[t.size + '/' + t.w + '/' + t.lh] = TS[t.size + '/' + t.w + '/' + t.lh] || s;
}
out.created.textStyles = Object.keys(D.typo).length;

// 5. Binding on current page
const byHex = {}; for (const [n, ref] of Object.entries(D.sem)) { (byHex[D.prim[ref]] = byHex[D.prim[ref]] || []).push(n); }
const pick = (h, isText) => { const c = byHex[h]; if (!c) return null; const pref = isText ? c.find(n => n.startsWith('text')) : c.find(n => !n.startsWith('text')); return S[pref || c[0]]; };
const wOf = st => /bold/i.test(st) ? (/semi/i.test(st) ? 600 : 700) : /medium/i.test(st) ? 500 : 400;
const nodes = figma.currentPage.findAll(n => 'fills' in n);
for (const n of nodes) {
  const isText = n.type === 'TEXT';
  if (Array.isArray(n.fills) && n.fills.length) {
    let ch = false; const f = n.fills.map(p => { if (p.type !== 'SOLID' || p.boundVariables?.color) return p; const v = pick(toHex(p.color), isText); if (!v) return p; ch = true; out.bound.fills++; return figma.variables.setBoundVariableForPaint(p, 'color', v); });
    if (ch) { if (isText) { for (const s of n.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(s.fontName); } n.fills = f; }
  }
  if ('strokes' in n && Array.isArray(n.strokes) && n.strokes.length) {
    let ch = false; const s2 = n.strokes.map(p => { if (p.type !== 'SOLID') return p; const v = pick(toHex(p.color), false); if (!v) return p; ch = true; out.bound.strokes++; return figma.variables.setBoundVariableForPaint(p, 'color', v); });
    if (ch) n.strokes = s2;
  }
  if ('topLeftRadius' in n && n.type !== 'TEXT') {
    for (const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius']) { const r = n[k]; if (r && R[r]) { n.setBoundVariable(k, R[r]); out.bound.radius++; } }
  }
  if (isText && typeof n.fontName === 'object' && typeof n.fontSize === 'number' && n.fontName.family === D.family) {
    const lh = n.lineHeight && n.lineHeight.unit === 'PIXELS' ? Math.round(n.lineHeight.value) : null; const s = lh ? TS[n.fontSize + '/' + wOf(n.fontName.style) + '/' + lh] : null;
    if (s) { await figma.loadFontAsync(n.fontName); await n.setTextStyleIdAsync(s.id); out.bound.text++; }
  }
}
out.collections = [cP.id, cS.id, cD.id];
return out;
 });
try { const s = figma.currentPage.findOne(n => n.type === 'SECTION'); if (s) await s.screenshot({ scale: 0.12 }); } catch (e) { RES.shot = String(e); }
return RES;
