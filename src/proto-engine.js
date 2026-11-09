/* Движок кликабельного прототипа УРАЛХИМ.
   Ожидает до себя: const ORDER (порядок экранов), NOTES (описания), разметку #store (экраны), #phone, .pv-list.
   Состояние: корзина, заявки, уведомления, очередь синхронизации. Всё кликабельно:
   1) правила экрана (R) → 2) data-go → 3) общие поведения (чипсы, сегменты, степперы…) → 4) запасной тост. */
(() => {
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const norm = s => (s || '').replace(/\s+/g, ' ').trim();
const fmt = n => Math.round(n).toLocaleString('ru-RU').replace(/ /g, ' ') + ' ₽';
const fmtT = t => (Math.round(t * 1000) / 1000).toLocaleString('ru-RU').replace(/ /g, ' ');
const store = {}; $$('#store > section.screen').forEach(s => store[s.id] = s);
const SCR = Object.values(store);
const phone = $('#phone'), frame = phone.parentElement, list = $('.pv-list');
const hist = [];
let current = null;

/* ---------- оверлеи: тост и шторка ---------- */
frame.insertAdjacentHTML('beforeend', '<div class="pv-toast" hidden></div><div class="pv-ov" hidden><div class="pv-sheet"></div></div>');
const toastEl = $('.pv-toast', frame), ov = $('.pv-ov', frame), sheet = $('.pv-sheet', frame);
let toastT;
function toast(msg, action) {
  toastEl.innerHTML = '<span>' + msg + '</span>' + (action ? '<b data-tgo="' + action.go + '">' + action.label + '</b>' : '');
  toastEl.hidden = false; toastEl.classList.remove('out'); clearTimeout(toastT);
  toastT = setTimeout(() => { toastEl.classList.add('out'); setTimeout(() => toastEl.hidden = true, 220); }, action ? 3600 : 2400);
}
toastEl.addEventListener('click', e => { const b = e.target.closest('[data-tgo]'); if (b) { toastEl.hidden = true; go(b.dataset.tgo); } });
function openSheet({ title, text = '', items = [], buttons = [] }) {
  sheet.innerHTML = '<div class="handle"></div><div class="ps-t">' + title + '</div>' + (text ? '<div class="ps-x">' + text + '</div>' : '') +
    (items.length ? '<div class="ps-list">' + items.map((it, i) => '<div class="ps-i' + (it.on ? ' on' : '') + '" data-i="' + i + '"><div><b>' + it.label + '</b>' + (it.sub ? '<span>' + it.sub + '</span>' : '') + '</div>' + (it.on ? '<em>✓</em>' : '<em>›</em>') + '</div>').join('') + '</div>' : '') +
    (buttons.length ? '<div class="ps-btns">' + buttons.map((b, i) => '<div class="btn ' + (b.kind || 'pri') + ' full" data-b="' + i + '"><span class="lbl">' + b.label + '</span></div>').join('') + '</div>' : '');
  ov.hidden = false; requestAnimationFrame(() => ov.classList.add('in'));
  sheet.onclick = e => {
    const i = e.target.closest('[data-i]'), b = e.target.closest('[data-b]');
    if (i) { closeSheet(); items[+i.dataset.i].act && items[+i.dataset.i].act(); }
    if (b) { closeSheet(); buttons[+b.dataset.b].act && buttons[+b.dataset.b].act(); }
  };
}
function closeSheet() { ov.classList.remove('in'); setTimeout(() => ov.hidden = true, 200); }
ov.addEventListener('click', e => { if (e.target === ov) closeSheet(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !ov.hidden) closeSheet(); });

/* ---------- навигация ---------- */
function note(id) {
  const n = NOTES[id]; if (!n) return; const i = ORDER.indexOf(id);
  $('#pv-num').textContent = 'Экран ' + (i + 1) + ' из ' + ORDER.length;
  $('#pv-t').textContent = n[0]; $('#pv-l').textContent = n[1];
  $('#pv-u').innerHTML = n[2].map(x => '<li>' + x + '</li>').join('');
}
function show(id, push) {
  if (!store[id]) id = 's-home';
  if (push && current && current !== id) hist.push(current);
  phone.innerHTML = ''; phone.appendChild(store[id]); phone.scrollTop = 0; current = id;
  list.querySelectorAll('a').forEach(a => a.classList.toggle('on', a.dataset.id === id));
  note(id); history.replaceState(null, '', '#screen=' + id);
  ON_SHOW[id] && ON_SHOW[id]();
}
const go = id => show(id, true);
const back = () => show(hist.pop() || 's-home', false);
window.pvShow = show;

/* ---------- состояние ---------- */
const S = { bell: 3, sync: 3, orderNo: 1602, group: 1, checklist: 5, doneTasks: 1, insp: false, filters: 1 };
const cart = () => store['s-cart'];
const groups = () => $$('.body > .card', cart());
const rowsOf = g => $$(':scope > .row', g).filter(r => r.style.display !== 'none');
const UNITS = { 'меш.': { t: 0.025, step: 40 }, 'МКР': { t: 1, step: 1 }, 'т': { t: 1, step: 1 } };
function stepVal(st) { const b = $('.val b', st); const m = norm(b.textContent).match(/^([\d\s,]+)\s*(.*)$/); return { n: parseFloat(m[1].replace(/\s/g, '').replace(',', '.')), u: m[2] || 'т' }; }
function stepSet(st, n, u) { const k = UNITS[u] || UNITS['т']; $('.val b', st).textContent = fmtT(n) + ' ' + u; const sm = $('.val small', st); if (sm) sm.textContent = '= ' + fmtT(n * k.t) + ' т'; }
function stepTons(st) { const v = stepVal(st); return v.n * (UNITS[v.u] || UNITS['т']).t; }
function rowTons(r) { const st = $('.stepper', r); if (st) return stepTons(st); const m = norm(r.textContent).match(/(\d[\d\s]*)\s*т\s*·/); return m ? +m[1].replace(/\s/g, '') : 0; }
function rowPrice(r) { return +r.dataset.price; }
function rowName(r) { return norm($('.ttl15', r).textContent); }
function initCartRows() { groups().forEach(g => rowsOf(g).forEach(r => { const m = norm($('.t3.num', r).textContent).match(/^([\d\s]+)₽\/т/); r.dataset.price = m ? m[1].replace(/\s/g, '') : 0; })); }
initCartRows();
const CART0 = groups().map(g => rowsOf(g).map(r => r.cloneNode(true)));
function groupSum(g) { return rowsOf(g).reduce((a, r) => a + rowPrice(r) * rowTons(r), 0); }
function groupTons(g) { return rowsOf(g).reduce((a, r) => a + rowTons(r), 0); }
function cartCount() { return groups().reduce((a, g) => a + rowsOf(g).length, 0); }
function recalc() {
  const gs = groups();
  gs.forEach((g, gi) => {
    rowsOf(g).forEach(r => { const b = $('.t3.num b', r); if (b) b.textContent = fmt(rowPrice(r) * rowTons(r)); });
    const n = rowsOf(g).length; g.style.display = n ? '' : 'none';
    const foot = $(':scope > .stack', g);
    if (foot) foot.innerHTML = '<div class="between"><span class="t2">' + n + ' ' + plural(n, 'позиция', 'позиции', 'позиций') + ' · <b class="num" style="color:var(--t1)">' + fmtT(groupTons(g)) + ' т</b></span><span class="num" style="font-size:20px;font-weight:700">' + fmt(groupSum(g)) + '</span></div><div class="between t3" style="margin-top:-6px"><span>без НДС</span><span class="num">с НДС ' + fmt(groupSum(g) * 1.2) + '</span></div>';
  });
  const live = gs.filter(g => rowsOf(g).length).length;
  const ban = $('.banner.info', cart()); if (ban) ban.style.display = live > 1 ? '' : 'none';
  const h = $('.top h1 span', cart()); if (h) h.textContent = cartCount();
  badges();
}
function plural(n, a, b, c) { n = Math.abs(n) % 100; const n1 = n % 10; if (n > 10 && n < 20) return c; if (n1 > 1 && n1 < 5) return b; if (n1 === 1) return a; return c; }
function restoreCart() { groups().forEach((g, gi) => { rowsOf(g).forEach(r => r.remove()); const anchor = $(':scope > .stack', g) || $(':scope > .btn', g); CART0[gi].forEach(r => g.insertBefore(r.cloneNode(true), anchor)); }); recalc(); }
function clearCart() { groups().forEach(g => rowsOf(g).forEach(r => r.remove())); recalc(); }
function badges() {
  const c = cartCount();
  SCR.forEach(s => {
    $$('.tab-i[data-go="s-cart"]', s).forEach(t => { let b = $('.tab-b', t); if (!b && c) { $('.tab-ic', t).insertAdjacentHTML('beforeend', '<span class="tab-b"></span>'); b = $('.tab-b', t); } if (b) { b.textContent = c; b.style.display = c ? '' : 'none'; } });
    $$('[data-go="s-notif"] .dot-b', s).forEach(b => { b.textContent = S.bell; b.style.display = S.bell ? '' : 'none'; });
    $$('.tab-i[data-go="s-sync"] .tab-b', s).forEach(b => { b.textContent = S.sync; b.style.display = S.sync ? '' : 'none'; });
  });
}

/* ---------- правила экранов ---------- */
const RULES = [];
const R = (screen, sel, text, fn) => RULES.push({ screen, sel, text, fn });
function matchRule(el) {
  for (const r of RULES) {
    if (r.screen !== '*' && r.screen !== current) continue;
    const t = el.closest(r.sel); if (!t || !phone.contains(t)) continue;
    if (r.text && !norm(t.textContent).startsWith(r.text)) continue;
    return { r, t };
  }
  return null;
}
const ON_SHOW = {};

// --- вход и регистрация
R('s-login', '.btn', 'Войти по коду', () => openSheet({ title: 'Код из SMS', text: 'Отправили код на +7 912 ***-**-89. В прототипе подойдёт любой.', items: [{ label: '4 8 1 5', sub: 'код из SMS' }], buttons: [{ label: 'Войти', act: () => { go('s-home'); toast('Добро пожаловать, Алексей!'); } }, { label: 'Отправить ещё раз', kind: 'sec', act: () => toast('Код отправлен повторно') }] }));
R('s-login', '.link', 'Забыли пароль', () => toast('Ссылка для сброса пароля отправлена на почту'));
R('s-login', '.btn', 'Войти', () => { go('s-home'); toast('Добро пожаловать, Алексей!'); });
R('s-login', '.pv-demo', '', () => { S.insp = true; go('s-insp'); toast('Демо: роль «Инспектор»'); });
R('s-reg', '.btn', 'Продолжить', (t) => {
  const cb = $('.cbx', store['s-reg']); if (!cb.classList.contains('on')) { toast('Отметьте согласие на обработку данных'); return; }
  openSheet({ title: 'Шаг 2 из 2 · пароль', text: 'Придумайте пароль. После проверки менеджером придёт письмо с подтверждением доступа.', items: [{ label: '••••••••••', sub: 'пароль, не меньше 8 символов' }], buttons: [{ label: 'Отправить на подключение', act: () => { show('s-login', false); toast('Заявка на подключение отправлена. Ответ — в течение рабочего дня'); } }] });
});

// --- главная
R('s-home', '.company', '', () => openSheet({ title: 'Компания и договор', items: [{ label: 'ООО «АгроСнаб-Урал»', sub: 'Договор 77-П/2026 · RUB', on: true }, { label: 'ООО «АгроСнаб-Урал»', sub: 'Договор 12-Э/2026 · USD', act: () => toast('Договор 12-Э/2026: задолженности нет') }, { label: 'ИП Петров А. Н.', sub: 'Договор 5-Р/2025 · RUB', act: () => toast('Компания переключена: ИП Петров А. Н.') }] }));
R('s-home', '.btn', 'Подтвердить', () => confirm1567());
R('s-home', '.card.tight:not(.row):not(.stack)', '', (t) => { const p = $('.pill', t); go('s-orders'); if (p) filterOrders(norm(p.textContent)); });
R('s-home', '.card.tight.row', 'Вагон 58213488', () => wagon2());
R('s-home', '.card', 'Повторить', () => { restoreCart(); go('s-cart'); toast('Позиции заявки № 1489 в корзине'); });
function confirm1567() {
  openSheet({ title: 'График по заявке № 1567', text: 'Отгрузка 96 т: Азотофосфат 33:3 и нитрат кальция, ст. Баженово, 18–20 ноября. Согласовано менеджером Лукьяновой С. А.', buttons: [{ label: 'Подтвердить график', act: () => {
    const h = store['s-home']; const card = $$('.card', h).find(c => norm(c.textContent).startsWith('Заявка № 1567')); if (card) card.remove();
    const em = $$('.sec h2 em', h)[0]; if (em) em.textContent = '1';
    const oc = $$('.card', store['s-orders']).find(c => norm(c.textContent).startsWith('№ 1567')); if (oc) { oc.style.border = ''; const bn = $('.banner', oc); if (bn) bn.remove(); }
    const nr = $$('.nrow', store['s-notif']).find(n => norm(n.textContent).startsWith('Подтвердите')); if (nr && nr.classList.contains('unread')) { nr.classList.remove('unread'); S.bell = Math.max(0, S.bell - 1); }
    badges(); toast('График по заявке № 1567 подтверждён');
  } }, { label: 'Предложить другую дату', kind: 'sec', act: () => go('s-chat') }] });
}
function wagon2() { openSheet({ title: 'Вагон 58213488 · 68 т', text: 'Сейчас: ст. Углеуральская. Задержка на 1 день из-за перегруза узла, новое прибытие на ст. Баженово ≈ 15 ноября.', buttons: [{ label: 'Сообщить о проблеме', kind: 'sec', act: () => go('s-issue') }, { label: 'Открыть заявку № 1489', act: () => go('s-order') }] }); }

// --- каталог
const INDUSTRIAL = [
  { name: 'Карбамид марки Б, навал', npk: [['N', '46']], price: '32 000 ₽/т · навал, вагон 68 т', badge: 'N46' },
  { name: 'Селитра аммиачная, МКР 1000', npk: [['N', '34,4']], price: '22 500 ₽/т · от 20 т', badge: 'N34' },
  { name: 'Кислота азотная неконцентрированная', npk: [['HNO₃', '56 %']], price: 'по запросу · цистерны', badge: 'HNO₃' },
];
function catSeg(ind) {
  const c = store['s-cat']; const cards = $$('.pcard', c);
  cards.forEach(p => p.style.display = (p.dataset.ind === '1') === ind ? '' : 'none');
  if (ind && !cards.some(p => p.dataset.ind)) {
    const tpl = cards[1]; const anchor = cards[cards.length - 1].nextSibling;
    INDUSTRIAL.forEach(it => { const n = tpl.cloneNode(true); n.dataset.ind = '1'; n.style.display = ''; $('.pname', n).textContent = it.name;
      $('.npk', n).innerHTML = it.npk.map(([a, b]) => '<span><i>' + a + '</i>' + b + '</span>').join(''); $('.price', n).innerHTML = '<b class="num">' + it.price.split(' · ')[0] + '</b> · ' + it.price.split(' · ')[1];
      $('.pimg', n).innerHTML = '<span style="font-weight:700;color:var(--blue);font-size:15px">' + it.badge + '</span>'; $('.pimg', n).style.background = '#E8E9F4';
      const btn = $('.btn', n); btn.className = 'btn s pri'; $('.lbl', btn).textContent = 'В корзину';
      tpl.parentNode.insertBefore(n, anchor); });
  }
  $('.between .t3 b', c).textContent = ind ? '12 продуктов' : '84 продукта';
  const chips = $('.chips', c); chips.innerHTML = ind ? '<span class="chip on"><span class="lbl">Все</span> <span class="n">12</span></span><span class="chip"><span class="lbl">Карбамид</span></span><span class="chip"><span class="lbl">Селитры</span></span><span class="chip"><span class="lbl">Кислоты</span></span><span class="chip"><span class="lbl">ADBLUE</span></span>'
    : '<span class="chip on"><span class="lbl">Все</span> <span class="n">84</span></span><span class="chip"><span class="lbl">Водорастворимые</span> <span class="n">23</span></span><span class="chip"><span class="lbl">Азотные</span> <span class="n">14</span></span><span class="chip"><span class="lbl">Комплексные</span></span>';
}
R('s-cat', '.seg > div', '', (t) => { selectIn(t); catSeg(norm(t.textContent).startsWith('Пром')); });
R('s-cat', '.top .icon-btn', '', () => openSheet({ title: 'Избранное · 3', items: [{ label: 'SOLAR Универсал 18:18:18', sub: '112 400 ₽/т', act: () => go('s-prod') }, { label: 'Нитрат кальция безводный', sub: '64 800 ₽/т', act: () => go('s-prod') }, { label: 'Карбамид марки Б, навал', sub: '32 000 ₽/т', act: () => go('s-prod') }] }));
R('s-cat', '.sbtn', '', (t) => generic(t));
R('s-cat', '.pcard .btn', '', (t) => addFromCatalog(t));
R('s-cat', '.pcard', '', (t) => { if (t.dataset.ind) { toast('Карточка промышленного продукта — по образцу SOLAR'); } go('s-prod'); });
function addFromCatalog(btn) {
  const p = btn.closest('.pcard'); const name = norm($('.pname', p).textContent);
  if (btn.classList.contains('sec')) { go('s-cart'); return; }
  const price = +norm($('.price b', p).textContent).replace(/[^\d]/g, '') || 0;
  const ind = !!p.dataset.ind; const g = groups()[ind ? 1 : 0];
  const exist = rowsOf(g).find(r => rowName(r).startsWith(name.slice(0, 14)));
  if (exist) { const st = $('.stepper', exist); if (st) { const v = stepVal(st); stepSet(st, v.n + (UNITS[v.u] || UNITS['т']).step, v.u); } }
  else {
    const tpl = rowsOf(groups()[0])[1] || CART0[0][1]; const r = tpl.cloneNode(true);
    r.dataset.price = price; $('.ttl15', r).textContent = name;
    const img = $('img', p); $('.pimg', r).innerHTML = img ? '<img src="' + img.getAttribute('src') + '" style="height:56px">' : $('.pimg', p).innerHTML;
    const mkr = /МКР/.test(name), bulk = /навал/.test(name);
    stepSet($('.stepper', r), mkr ? 20 : bulk ? 68 : 40, mkr ? 'МКР' : bulk ? 'т' : 'меш.');
    g.insertBefore(r, $(':scope > .stack', g) || $(':scope > .btn', g));
  }
  recalc(); btn.className = 'btn s sec'; $('.lbl', btn).textContent = 'В корзине ✓';
  toast('Добавлено: ' + name.split(',')[0], { label: 'В корзину', go: 's-cart' });
}

// --- карточка товара
R('s-prod', '.icon-btn:not([data-go])', '', (t) => { if ($('path[d^="M12 15V4"]', t)) toast('Ссылка на продукт скопирована'); else { t.classList.toggle('fav-off'); toast(t.classList.contains('fav-off') ? 'Удалено из избранного' : 'Добавлено в избранное'); } });
R('s-prod', '.seg > div', '', (t) => { selectIn(t); const mkr = norm(t.textContent).startsWith('МКР'); const st = $('.dock .stepper', store['s-prod']); stepSet(st, mkr ? 1 : 40, mkr ? 'МКР' : 'меш.'); if (mkr) $('.val small', st).textContent = '= 0,6 т'; prodBtn(); toast(mkr ? 'Фасовка МКР 600 кг: шаг — 1 мешок (0,6 т)' : 'Фасовка мешок 25 кг: шаг — 40 мешков (1 т)'); });
R('s-prod', '.link', 'Все 13', (t) => { const box = t.closest('.stack'); if (box.dataset.full) return; box.dataset.full = 1; [['Азот аммонийный', '3,6 %'], ['Азот нитратный', '5,4 %'], ['Азот амидный', '9 %'], ['Бор (B)', '0,02 %'], ['Медь (Cu)', '0,01 %'], ['Железо (Fe)', '0,1 %'], ['Марганец (Mn)', '0,05 %'], ['Молибден (Mo)', '0,01 %'], ['Цинк (Zn)', '0,01 %']].forEach(([a, b]) => box.insertAdjacentHTML('beforeend', '<div class="kv"><span>' + a + '</span><b>' + b + '</b></div>')); t.textContent = 'Свернуть'; });
R('s-prod', '.link', 'Свернуть', (t) => { const box = t.closest('.stack'); $$('.kv', box).slice(4).forEach(k => k.remove()); delete box.dataset.full; t.textContent = 'Все 13'; });
const ACC = { 'Описание': 'Водорастворимое NPK-удобрение 18:18:18 с магнием и микроэлементами в хелатной форме. Для фертигации и листовых подкормок овощных, плодовых и цветочных культур. Норма: 2–5 кг/га на подкормку.', 'Упаковка': 'Мешок 25 кг с полиэтиленовым вкладышем; МКР 600 кг. Хранить в сухом закрытом складе, на поддонах, не выше 8 ярусов. Срок хранения — 3 года.', 'Транспортировка': 'Ж/д крытыми вагонами и автотранспортом. Отгрузка со ст. Березники, норма загрузки вагона — 68 т.', 'Документы': '<span class="pv-doc">Сертификат соответствия.pdf</span><span class="pv-doc">Паспорт безопасности.pdf</span><span class="pv-doc">Рекомендации по применению.pdf</span>' };
R('s-prod', '.lrow', '', (t) => { const nx = t.nextElementSibling; if (nx && nx.classList.contains('acc')) { nx.remove(); t.classList.remove('open'); return; } const k = Object.keys(ACC).find(k => norm(t.textContent).startsWith(k)); t.insertAdjacentHTML('afterend', '<div class="acc t2">' + ACC[k] + '</div>'); t.classList.add('open'); });
R('s-prod', '.pv-doc', '', (t) => toast('Скачан: ' + t.textContent));
R('s-prod', '.dock .btn', '', () => { const st = $('.dock .stepper', store['s-prod']); const v = stepVal(st); const g = groups()[0]; let r = rowsOf(g).find(r => rowName(r).startsWith('SOLAR Универсал'));
  if (!r) { restoreCart(); r = rowsOf(groups()[0]).find(r => rowName(r).startsWith('SOLAR Универсал')); }
  const cs = $('.stepper', r); const cv = stepVal(cs); stepSet(cs, cv.n + v.n, cv.u === v.u ? cv.u : v.u); recalc(); go('s-cart'); toast('SOLAR Универсал: +' + fmtT(stepTons(st)) + ' т в заявке 1'); });
function prodBtn() { const st = $('.dock .stepper', store['s-prod']); const b = $('.dock .btn .num', store['s-prod']); if (b) b.textContent = fmt(112400 * stepTons(st)); }

// --- корзина
R('s-cart', '.link', 'Очистить', () => openSheet({ title: 'Очистить корзину?', text: 'Удалим все позиции обеих заявок. Повторить прошлую заявку можно будет одним нажатием.', buttons: [{ label: 'Очистить', kind: 'pri pv-danger', act: () => { clearCart(); go('s-cart-empty'); } }, { label: 'Отмена', kind: 'sec' }] }));
R('s-cart', '.sbtn', '', (t) => generic(t));
R('s-cart', '.icon-btn:not([data-go])', '', (t) => { const r = t.closest('.row[data-price]'); const n = rowName(r); r.remove(); recalc(); toast('Удалено: ' + n.split(',')[0]); if (!cartCount()) go('s-cart-empty'); });
R('s-cart', '.btn', 'Оформить заявку 2', () => { S.group = 2; go('s-checkout'); });
R('s-cart', '.btn', 'Оформить заявку 1', () => { S.group = 1; go('s-checkout'); });
R('s-cart', '.row[data-price]', '', () => go('s-prod'));
ON_SHOW['s-cart'] = () => { if (!cartCount()) show('s-cart-empty', false); };

// --- оформление
const STATIONS = [['Баженово, Свердловская ж/д', '780707'], ['Красноуфимск, Свердловская ж/д', '781302'], ['Богданович, Свердловская ж/д', '781006'], ['Сухой Лог, Свердловская ж/д', '780306']];
function renderCheckout() {
  const c = store['s-checkout']; const g = groups()[S.group - 1]; const rows = rowsOf(g);
  $('.top .ttl', c).textContent = S.group === 1 ? 'Заявка 1 · Сельхоз' : 'Заявка 2 · Промышленное';
  const sum = groupSum(g), tons = groupTons(g);
  $('.body > .card', c).innerHTML = rows.map(r => '<div class="kv"><span>' + rowName(r).split(',')[0] + ' · ' + fmtT(rowTons(r)) + ' т</span><b>' + fmt(rowPrice(r) * rowTons(r)) + '</b></div>').join('') +
    '<div class="kv"><span>НДС 20 %</span><b>' + fmt(sum * 0.2) + '</b></div><div class="kv" style="border:0;font-size:16px"><span style="color:var(--t1);font-weight:600">Итого · ' + fmtT(tons) + ' т</span><b>' + fmt(sum * 1.2) + '</b></div>';
  $('.dock .btn .lbl', c).textContent = 'Отправить заявку · ' + fmt(sum * 1.2);
}
ON_SHOW['s-checkout'] = () => { if (!rowsOf(groups()[S.group - 1]).length) S.group = rowsOf(groups()[0]).length ? 1 : 2; renderCheckout(); };
R('s-checkout', '.field', 'Станция', (t) => openSheet({ title: 'Станция назначения', text: 'Последние станции из ваших заявок', items: STATIONS.map(([n, code]) => ({ label: n, sub: 'код ' + code, on: norm($('b', t).textContent) === n, act: () => { $('b', t).textContent = n; $('.t3', t).textContent = code; toast('Станция: ' + n.split(',')[0]); } })) }));
R('s-checkout', '.field', 'Грузополучатель', (t) => openSheet({ title: 'Грузополучатель', items: [['ООО «АгроСнаб-Урал»', 'ОКПО 12345678 · Екатеринбург'], ['ООО «Урал-Агро»', 'ОКПО 87654321 · Сухой Лог']].map(([n, s]) => ({ label: n, sub: s, on: norm($('b', t).textContent) === n, act: () => { $('b', t).textContent = n; } })) }));
R('s-checkout', '.field', 'Договор', (t) => openSheet({ title: 'Договор', items: [['77-П/2026 · RUB', 'до 31.12.2026'], ['12-Э/2026 · USD', 'экспортный']].map(([n, s]) => ({ label: n, sub: s, on: norm($('b', t).textContent) === n, act: () => { $('b', t).textContent = n; } })) }));
R('s-checkout', '.seg > div', 'Самовывоз', (t) => { selectIn(t); toast('Самовывоз со склада ст. Березники — станция не нужна'); });
R('s-checkout', '.dock .btn', '', () => sendOrder());
function sendOrder() {
  const g = groups()[S.group - 1]; const rows = rowsOf(g); if (!rows.length) { toast('В заявке нет позиций'); return; }
  const no = S.orderNo++; const sum = groupSum(g) * 1.2, tons = groupTons(g);
  const names = rows.map(r => rowName(r).split(',')[0]).join(' · ');
  // новая карточка в «Заявках»
  const ol = store['s-orders']; const anchor = $$('.card', ol)[0];
  anchor.insertAdjacentHTML('beforebegin', '<div class="card stack pv-new" style="gap:10px" data-go="s-order" data-pill="Согласование"><div class="between"><span class="ttl15 num">№ ' + no + ' · от 09.11</span><span class="pill neu"><span class="lbl">Согласование</span></span></div><div class="t2">' + names + '</div><div class="between"><span class="t3 num">' + fmtT(tons) + ' т · ответ до 11 нояб.</span><span class="num ttl15">' + fmt(sum) + '</span></div></div>');
  // главная: счётчики
  const h = store['s-home']; const kp = $$('.card.tight', h).find(c => norm(c.textContent).includes('На согласовании')); if (kp) { const a = $('.amount', kp); a.textContent = +a.textContent + 1; }
  const em = $$('.sec h2 em', h).find(e => /активн/.test(e.textContent)); if (em) em.textContent = (parseInt(em.textContent) + 1) + ' активных';
  // уведомление
  const nf = store['s-notif']; const lab = $$('.label', nf)[0]; lab.insertAdjacentHTML('afterend', '<div class="card tight row nrow unread" data-go="s-orders" data-t="Заявки"><div class="ico ok">' + ICON_OK + '</div><div style="flex:1"><div class="ttl15">Заявка № ' + no + ' принята в работу</div><div class="t3">Лукьянова С. А. ответит до 11 ноября · сейчас</div></div></div>'); S.bell++;
  // успех
  const sc = store['s-success']; $('div[style*="font:var(--font-display)"]', sc).innerHTML = 'Заявка № ' + no + '<br>отправлена';
  const kv = $$('.kv b', sc); kv[0].textContent = fmtT(tons) + ' т · ' + rows.length + ' ' + plural(rows.length, 'позиция', 'позиции', 'позиций'); kv[1].textContent = fmt(sum); kv[2].textContent = norm($('.field b', store['s-checkout']).textContent).split(',')[0]; kv[3].textContent = norm($('.seg .on', $$('.seg', store['s-checkout'])[1]).textContent) + ' ноября';
  rows.forEach(r => r.remove()); recalc();
  const other = groups()[S.group === 1 ? 1 : 0]; const rem = $$('.card.row', sc).pop(); rem.style.display = rowsOf(other).length ? '' : 'none';
  if (rowsOf(other).length) $('.t2', rem).innerHTML = 'В корзине осталась <b>заявка ' + (S.group === 1 ? 2 : 1) + '</b> · ' + (S.group === 1 ? 'Промышленное' : 'Сельхоз') + ', ' + fmtT(groupTons(other)) + ' т';
  hist.length = 0; show('s-success', false);
}
const ICON_OK = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
R('s-success', '.link', 'Оформить', () => { S.group = rowsOf(groups()[1]).length ? 2 : 1; go('s-checkout'); });
R('s-success', '.btn', 'Открыть заявку', () => { go('s-orders'); toast('Новая заявка — первая в списке'); });

// --- пустая корзина
R('s-cart-empty', '.btn', 'Повторить', () => { restoreCart(); show('s-cart', true); toast('Заявка № 1489 повторена: станция и грузополучатель подставлены'); });

// --- заявки
function filterOrders(label) {
  const ol = store['s-orders']; const key = norm(label).replace(/ \d+$/, '').toLowerCase();
  const map = { 'все': '', 'на согласовании': 'согласование', 'согласование': 'согласование', 'подтверждены': 'подтвержд', 'отгружаются': 'отгрузка', 'в пути': 'в пути' };
  const k = key in map ? map[key] : key;
  $$('.chip', ol).forEach(c => c.classList.toggle('on', norm(c.textContent).toLowerCase().replace(/ \d+$/, '') === key || (!k && /^все/i.test(norm(c.textContent)))));
  $$('.body > .card', ol).forEach(c => { if (c.dataset.arch) { c.style.display = 'none'; return; } const p = $('.pill', c); c.style.display = !k || (p && norm(p.textContent).toLowerCase().includes(k)) ? '' : 'none'; });
}
R('s-orders', '.chip', '', (t) => filterOrders(norm(t.textContent)));
R('s-orders', '.seg > div', '', (t) => { selectIn(t); const arch = norm(t.textContent).startsWith('Архив'); const ol = store['s-orders']; $('.chips', ol).style.display = arch ? 'none' : '';
  if (arch && !$('[data-arch]', ol)) { const body = $('.body', ol); [['1460', 'Карбамид марки Б, навал', '136 т', '4 216 000 ₽'], ['1402', 'SOLAR Универсал 18:18:18', '8 т', '1 078 900 ₽'], ['1377', 'Селитра аммиачная, МКР 1000', '60 т', '1 620 000 ₽']].forEach(([n, p, t, s]) => body.insertAdjacentHTML('beforeend', '<div class="card stack" style="gap:10px" data-arch="1" data-go="s-order"><div class="between"><span class="ttl15 num">№ ' + n + '</span><span class="pill neu"><span class="lbl">Доставлена</span></span></div><div class="t2">' + p + '</div><div class="between"><span class="t3 num">' + t + '</span><span class="num ttl15">' + s + '</span></div></div>')); }
  $$('.body > .card', ol).forEach(c => c.style.display = arch ? (c.dataset.arch ? '' : 'none') : (c.dataset.arch ? 'none' : ''));
  if (!arch) filterOrders('Все'); });
R('s-orders', '.top .icon-btn', '', (t) => { if (t.dataset.go) return go(t.dataset.go); openSheet({ title: 'Поиск заявки', text: 'Номер, продукт или станция', items: [{ label: '№ 1489', sub: 'Карбамид марки Б · в пути', act: () => go('s-order') }, { label: '№ 1567', sub: 'Азотофосфат 33:3 · подтверждена', act: () => go('s-order') }] }); });
R('s-orders', '.body > .card', '', () => go('s-order'));
ON_SHOW['s-orders'] = () => { const ol = store['s-orders']; const n = $$('.body > .card', ol).filter(c => !c.dataset.arch).length; const sg = $('.seg > div', ol); if (sg) sg.textContent = 'Активные · ' + n; };

// --- заявка и трекинг
const ORDER_TABS = {
  'Состав': '<div class="card stack pv-panel" style="gap:2px"><div class="kv"><span>Карбамид марки Б, навал</span><b>136 т</b></div><div class="kv"><span>Цена по договору</span><b>32 000 ₽/т</b></div><div class="kv"><span>НДС 20 %</span><b>725 333 ₽</b></div><div class="kv" style="border:0"><span style="color:var(--t1);font-weight:600">Итого</span><b>4 352 000 ₽</b></div></div>',
  'Документы': '<div class="card pv-panel" style="padding:14px 16px">' + [['Счёт № 4398', 'оплачен 26.10'], ['УПД № 1189', 'от 06.11'], ['Сертификат качества', 'партия 2611-04'], ['Ж/д накладная ЭА123456', 'вагон 58213470']].map(([a, b]) => '<div class="lrow pv-dl"><div class="ico info" style="width:36px;height:36px">⤓</div><div style="flex:1"><div class="ttl15">' + a + '</div><div class="t3">' + b + ' · PDF</div></div></div>').join('') + '</div>',
  'История': '<div class="card pv-panel"><div class="tl">' + [['Вагоны в пути', '06.11, 14:20'], ['Отгружено 136 т', '06.11, 09:05'], ['Счёт оплачен', '26.10, 16:40'], ['Подтверждена менеджером', '25.10, 11:12'], ['Отправлена', '24.10, 18:30']].map(([a, b], i, arr) => '<div class="tl-i"><div class="tl-dot"><b></b>' + (i < arr.length - 1 ? '<i></i>' : '') + '</div><div class="tl-c"><div class="ttl15" style="font-weight:500">' + a + '</div><div class="t3 num">' + b + '</div></div></div>').join('') + '</div></div>',
};
R('s-order', '.seg > div', '', (t) => { selectIn(t); const body = t.closest('.body'); const k = norm(t.textContent); $$(':scope > .pv-panel', body).forEach(p => p.remove());
  $$(':scope > .card', body).forEach(c => c.style.display = k === 'Отгрузка' ? '' : 'none'); if (ORDER_TABS[k]) body.insertAdjacentHTML('beforeend', ORDER_TABS[k]); });
R('s-order', '.pv-dl', '', (t) => toast('Скачан: ' + norm($('.ttl15', t).textContent) + '.pdf'));
R('s-order', '.t3.num', 'Накладная', () => toast('Номер накладной ЭА123456 скопирован'));
R('s-order', '.link', 'Ещё 6 станций', (t) => { const it = t.closest('.tl-i'); const st = ['Кунгур · 07.11, 03:10', 'Шаля · 07.11, 11:45', 'Шамары · 07.11, 19:20', 'Первоуральск · ожидается 13.11', 'Екатеринбург-Сорт. · ожидается 13.11', 'Богданович · ожидается 14.11'];
  it.outerHTML = st.map((s, i) => '<div class="tl-i"><div class="tl-dot"><b class="' + (i < 3 ? '' : 'fut') + '" style="width:10px;height:10px;margin-top:5px"></b><i class="' + (i < 2 ? '' : 'fut') + '"></i></div><div class="tl-c"><div class="t2">' + s.split(' · ')[0] + '</div><div class="t3 num">' + s.split(' · ')[1] + '</div></div></div>').join(''); });
R('s-order', '.card.tight.row', '', () => wagon2());
R('s-order', '.top .icon-btn', '', (t) => { if (t.dataset.go) return back(); openSheet({ title: 'Заявка № 1489', items: [{ label: 'Повторить заявку', sub: 'те же позиции, станция, грузополучатель', act: () => { restoreCart(); go('s-cart'); toast('Позиции заявки № 1489 в корзине'); } }, { label: 'Скачать все документы', sub: 'ZIP · 4 файла', act: () => toast('Скачан архив документов по заявке № 1489') }, { label: 'Отменить заявку', sub: 'недоступно: вагоны в пути', act: () => toast('Нельзя отменить: вагоны уже в пути') }] }); });
R('s-order', '.card', 'Прибытие', () => toast('Дата прибытия пересчитывается по данным РЖД каждые 3 часа'));

// --- обращение и чат
R('s-issue', '.chip', '', (t) => selectIn(t, true));
R('s-issue', '.ph-t', '', (t) => addPhoto(t));
R('s-issue', '.dock .btn', '', () => { const nf = store['s-notif']; const lab = $$('.label', nf)[0]; lab.insertAdjacentHTML('afterend', '<div class="card tight row nrow" data-go="s-chat"><div class="ico info">' + ICON_OK + '</div><div style="flex:1"><div class="ttl15">Обращение № 3021 зарегистрировано</div><div class="t3">Недовес 1,2 т · ответ до 11 ноября</div></div></div>'); back(); toast('Обращение № 3021 отправлено. Ответ — в течение 2 рабочих дней'); });
function chatSend() { const c = store['s-chat']; const inp = $('.pv-input', c); const txt = norm(inp.textContent); if (!txt) { inp.focus(); return; }
  const body = $('.body', c); const tm = new Date().toTimeString().slice(0, 5); body.insertAdjacentHTML('beforeend', '<div class="bub out">' + txt.replace(/</g, '&lt;') + '<i>' + tm + ' ✓</i></div>'); inp.textContent = ''; phone.scrollTop = phone.scrollHeight;
  setTimeout(() => { body.insertAdjacentHTML('beforeend', '<div class="bub in">Приняла, уточню и вернусь в течение часа.<i>' + tm + '</i></div>'); if (current === 's-chat') phone.scrollTop = phone.scrollHeight; }, 1200); }
R('s-chat', '.dock .icon-btn', '', (t) => { if (t.style.background) chatSend(); else toast('Файл прикреплён: Акт выгрузки.pdf'); });
R('s-chat', '.top .icon-btn', '', (t) => t.dataset.go ? back() : toast('Звонок: Лукьянова Светлана, +7 343 210-45-67'));
R('s-chat', '.bub.file', '', () => toast('Скачан: ЖД накладная ЭА123457.pdf'));

// --- уведомления
R('s-notif', '.chip', '', (t) => { selectIn(t); const k = norm(t.textContent).replace(/ \d+$/, ''); const types = { 'Заявки': /заявк|вагон|обращени/i, 'Финансы': /счёт|оплат/i, 'Новости': /агроволг|новост/i };
  $$('.nrow', store['s-notif']).forEach(n => n.style.display = k === 'Все' || (types[k] && types[k].test(n.textContent)) ? '' : 'none'); });
R('s-notif', '.top .icon-btn', '', (t) => { if (t.dataset.go) return back(); $$('.nrow.unread', store['s-notif']).forEach(n => n.classList.remove('unread')); S.bell = 0; badges(); toast('Все уведомления прочитаны'); });
R('s-notif', '.nrow', '', (t) => { if (t.classList.contains('unread')) { t.classList.remove('unread'); S.bell = Math.max(0, S.bell - 1); badges(); } if (norm(t.textContent).startsWith('Подтвердите')) { go('s-home'); setTimeout(confirm1567, 150); } else if (t.dataset.go) go(t.dataset.go); });

// --- финансы
R('s-fin', '.chip', '', (t) => { selectIn(t); const k = norm(t.textContent); const card = $('.card[style*="var(--blue)"]', store['s-fin']); const a = $('.amount', card);
  if (k.startsWith('USD')) { a.innerHTML = '0 <small>$</small>'; $('div', card).textContent = 'Договор 12-Э/2026 · задолженности нет'; } else if (k.startsWith('EUR')) { a.innerHTML = '0 <small>€</small>'; $('div', card).textContent = 'Договоров в EUR нет'; } else { a.innerHTML = '1 845 000 <small>₽</small>'; $('div', card).textContent = 'К оплате до 15 ноября'; } });
R('s-fin', '.btn', 'Счёт', () => toast('Скачан: Счёт № 4412 от 01.11.2026.pdf'));
R('s-fin', '.btn', 'Реквизиты', () => openSheet({ title: 'Реквизиты для оплаты', text: 'АО «ОХК «УРАЛХИМ» · ИНН 7703647595<br>р/с 40702810400000012345 · ПАО Сбербанк<br>БИК 044525225<br>Назначение: оплата по счёту № 4412 от 01.11.2026, в т. ч. НДС 20 %', buttons: [{ label: 'Скопировать реквизиты', act: () => toast('Реквизиты скопированы') }, { label: 'Поделиться PDF', kind: 'sec', act: () => toast('PDF со счётом отправлен в мессенджер') }] }));
R('s-fin', '.link', 'Операции', () => toast('Операции с остатком — в списке ниже'));
R('s-fin', '.link', 'Все', () => toast('Показаны все счета за 2026 год'));
R('s-fin', '.lrow', '№', (t) => { const n = norm($('.ttl15', t).textContent); openSheet({ title: 'Счёт ' + n.split(' · ')[0], text: n.split(' · ')[1] + ' · ' + norm($('.t3', t).textContent), buttons: [{ label: 'Скачать PDF', act: () => toast('Скачан: Счёт ' + n.split(' · ')[0] + '.pdf') }, { label: 'Открыть заявку', kind: 'sec', act: () => go('s-order') }] }); });
R('s-fin', '.lrow', 'Акт сверки', () => openSheet({ title: 'Акт сверки', text: 'За какой период?', items: ['Октябрь 2026', 'III квартал 2026', 'С начала 2026 года'].map(p => ({ label: p, act: () => toast('Акт сверки за ' + p.toLowerCase() + ' запрошен — пришлём push до 2 дней') })) }));
R('s-fin', '.lrow', 'Перенести', () => openSheet({ title: 'Перенос остатка', text: 'Свободный остаток 1 274 300 ₽ перенесём с договора 77-П/2026', items: [{ label: 'На договор 12-Э/2026', sub: 'USD · по курсу ЦБ на дату переноса', act: () => toast('Заявка на перенос создана, менеджер свяжется') }] }));
R('s-fin', '.lrow', 'Вернуть', () => openSheet({ title: 'Возврат средств', text: 'Вернём 1 274 300 ₽ на расчётный счёт …4567 в течение 10 рабочих дней.', buttons: [{ label: 'Создать заявку на возврат', act: () => toast('Заявка на возврат создана') }, { label: 'Отмена', kind: 'sec' }] }));
R('s-fin', '.card.row', 'Свободный', () => toast('Свободный остаток можно перенести или вернуть'));

// --- профиль и новости
R('s-profile', '.link', 'Сменить', () => store['s-home'] && RULES.find(r => r.screen === 's-home' && r.sel === '.company').fn());
R('s-profile', '.top .icon-btn', '', () => openSheet({ title: 'Настройки', items: [{ label: 'Уведомления', sub: 'push: заявки, вагоны, счета', on: true }, { label: 'Вход по Face ID', sub: 'включён', on: true }, { label: 'Язык', sub: 'Русский' }] }));
R('s-profile', '.btn', 'Позвонить', () => toast('Звонок: Лукьянова Светлана, +7 343 210-45-67'));
R('s-profile', '.lrow', 'Договоры', () => openSheet({ title: 'Договоры', items: [{ label: '77-П/2026 · RUB', sub: 'действует до 31.12.2026', act: () => go('s-fin') }, { label: '12-Э/2026 · USD', sub: 'экспортный', act: () => go('s-fin') }] }));
R('s-profile', '.lrow', 'Избранное', () => RULES.find(r => r.screen === 's-cat' && r.sel === '.top .icon-btn').fn());
R('s-profile', '.lrow', 'Станции', () => openSheet({ title: 'Станции и грузополучатели', items: STATIONS.map(([n, c]) => ({ label: n, sub: 'код ' + c })) }));
R('s-profile', '.lrow', 'Обучение', () => openSheet({ title: 'Обучение · 11 из 12', items: [{ label: 'Фертигация с SOLAR', sub: 'сертификат получен', on: true }, { label: 'Хранение МКР', sub: 'сертификат получен', on: true }, { label: 'Продажи промышленной химии', sub: 'не пройден · 25 мин', act: () => toast('Курс откроется в браузере') }] }));
R('s-profile', '.lrow', 'Помощь', () => openSheet({ title: 'Помощь и контакты', items: [{ label: 'Чат с менеджером', sub: 'Лукьянова Светлана', act: () => go('s-chat') }, { label: '8-800-707-16-69', sub: 'бесплатно, 9:00–18:00 МСК', act: () => toast('Звонок на 8-800-707-16-69') }, { label: 'lksd@uralchem.com', sub: 'поддержка ЛК', act: () => toast('Откроется почтовое приложение') }] }));
R('s-profile', '.btn', 'Выйти', () => openSheet({ title: 'Выйти из аккаунта?', buttons: [{ label: 'Выйти', act: () => { hist.length = 0; show('s-login', false); } }, { label: 'Отмена', kind: 'sec' }] }));
R('s-news', '.chip', '', (t) => selectIn(t));
R('s-news', '.card', '', (t) => openSheet({ title: norm(($('.ttl16', t) || $('.ttl15', t)).textContent), text: 'Полный текст новости откроется на сайте uralchem.ru. В приложении — короткий анонс и ссылка на продукт.', buttons: [{ label: 'Открыть продукт', act: () => go('s-prod') }, { label: 'Закрыть', kind: 'sec' }] }));

// --- фильтры каталога
R('s-filters', '.chip', '', (t) => { t.classList.toggle('on'); filtersCount(); });
R('s-filters', '.link', 'Сбросить', () => { $$('.chip', store['s-filters']).forEach(c => c.classList.remove('on')); $('.tgl', store['s-filters']).classList.remove('on'); filtersCount(); });
R('s-filters', '.tgl', '', (t) => { t.classList.toggle('on'); filtersCount(); });
R('s-filters', '.btn', 'Показать', () => { const n = S.filters; const b = $('[data-go="s-filters"] .pill', store['s-cat']); if (b) { b.textContent = n; b.style.display = n ? '' : 'none'; } show(hist.pop() || 's-cat', false); toast(n ? 'Фильтров применено: ' + n : 'Фильтры сброшены'); });
function filtersCount() { const f = store['s-filters']; S.filters = $$('.chip.on', f).length + ($('.tgl.on', f) ? 1 : 0); const n = Math.max(6, 84 - S.filters * 12); $('.btn .lbl', f).textContent = 'Показать ' + n + ' ' + plural(n, 'продукт', 'продукта', 'продуктов'); }

// --- инспектор
R('s-insp', '.icon-btn', '', () => toast('Новых уведомлений нет'));
R('s-insp', '.card.tight.row', '', (t) => { go('s-insp-run'); toast(norm($('.ttl15', t).textContent) + ' · чек-лист по образцу'); });
R('s-insp', '.between', 'Выполнено', (t) => { const nx = t.nextElementSibling; if (nx && nx.classList.contains('pv-done')) { nx.remove(); return; } t.insertAdjacentHTML('afterend', '<div class="pv-done stack" style="gap:8px">' + Array.from({ length: S.doneTasks }, (_, i) => '<div class="ck done">' + ICON_OK.replace(/22/g, '16') + '<span>' + (i === 0 ? '07:30 · Приёмка вагона 58213470' : '08:30 · Инспекция склада, Красноуфимск') + '</span></div>').join('') + '</div>'); });
R('s-insp-run', '.ck', '', (t) => { const done = t.classList.toggle('done'); runProgress(done ? 1 : -1); });
R('s-insp-run', '.seg > div', '', (t) => { selectIn(t); const ok = norm(t.textContent).startsWith('Соотв'); toast(ok ? 'Пункт 5: соответствует' : 'Пункт 5: замечание — добавьте описание'); });
R('s-insp-run', '.ph-t', '', (t) => addPhoto(t));
R('s-insp-run', '.btn', 'Черновик', () => { show('s-insp', false); toast('Черновик сохранён на устройстве'); });
R('s-insp-run', '.btn', '', () => runNext());
function runProgress(d) { S.checklist = Math.max(0, Math.min(9, S.checklist + d)); const c = store['s-insp-run']; $('.prog i', c).style.width = Math.round(S.checklist / 9 * 100) + '%'; const b = $('.between.t3 b', c); if (b) b.textContent = S.checklist + ' из 9';
  const btn = $$('.dock .btn', c)[1]; $('.lbl', btn).textContent = S.checklist >= 9 ? 'Завершить инспекцию' : 'Следующий пункт'; }
function runNext() {
  const c = store['s-insp-run'];
  if (S.checklist >= 9) { S.sync++; S.doneTasks = 2; const ins = store['s-insp']; const first = $('.body > .card', ins); if (first) first.remove(); const h = $$('.between .t2', ins).find(e => /Выполнено/.test(e.textContent)); if (h) h.textContent = 'Выполнено · 2';
    const big = $('div[style*="font-size:22px"]', ins); if (big) big.textContent = '3 задачи на сегодня'; queueAdd('Инспекция склада · Красноуфимск', '9 из 9 пунктов · отчёт'); badges(); show('s-insp', false); toast('Инспекция завершена. Отчёт отправим при подключении'); return; }
  const card = $('.body > .card', c);
  if (card) { card.outerHTML = '<div class="ck done">' + ICON_OK.replace(/22/g, '16') + '<span>5. Условия хранения · замечание</span></div>'; runProgress(1); return; }
  const next = $$('.ck', c).find(k => !k.classList.contains('done')); if (next) { next.classList.add('done'); runProgress(1); }
  else { while (S.checklist < 9) runProgress(1); }
  if (S.checklist === 7) { $('.body', c).insertAdjacentHTML('beforeend', '<div class="ck">' + '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="7"/></svg>' + '<span>8. Фото общего вида склада</span></div><div class="ck"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="7"/></svg><span>9. Подпись представителя склада</span></div>'); }
}
R('s-remark', '.chip', '', (t) => selectIn(t, true));
R('s-remark', '.ph-l', '', (t) => { if (t.classList.contains('add')) { addPhoto(t); } else toast('Фото: ворота № 3, 08:47'); });
R('s-remark', '.top .icon-btn', '', () => back());
R('s-remark', '.dock .btn', '', () => { S.sync++; queueAdd('Замечание · ' + norm($('.chip.on', store['s-remark']).textContent), '3 фото · 6,2 МБ · сейчас'); badges(); go('s-sync'); toast('Замечание сохранено на устройстве'); });
function queueAdd(t, s) { const sy = store['s-sync']; const card = $$('.card', sy)[1]; card.insertAdjacentHTML('afterbegin', '<div class="lrow"><div class="ico warn" style="width:36px;height:36px">⏳</div><div style="flex:1"><div class="ttl15">' + t + '</div><div class="t3">' + s + '</div></div></div>');
  const em = $('.sec h2 em', sy); if (em) em.textContent = S.sync; const ban = $('.banner span:nth-child(2)', store['s-insp']); if (ban) ban.textContent = 'Нет сети · ' + S.sync + ' ' + plural(S.sync, 'изменение ждёт', 'изменения ждут', 'изменений ждут') + ' отправки'; }
R('s-sync', '.btn', 'Повторить', () => toast('Сети нет — повторим автоматически, как только появится'));
R('s-sync', '.tgl', '', (t) => { t.classList.toggle('on'); toast(t.classList.contains('on') ? 'Фото — только по Wi-Fi' : 'Фото — по любой сети'); });
R('s-sync', '.lrow', 'Хранить', (t) => openSheet({ title: 'Хранить офлайн-данные', items: ['3 дня', '7 дней', '14 дней'].map(d => ({ label: d, on: norm($('.t3', t).textContent) === d, act: () => { $('.t3', t).textContent = d; } })) }));
R('s-sync', '.lrow', '', (t) => toast(norm($('.ttl15', t).textContent) + ' — ждёт сети'));
R('*', '.tab-i', 'Объекты', () => openSheet({ title: 'Объекты · 3', items: [{ label: 'Склад ООО «АгроСнаб-Урал»', sub: 'Красноуфимск · 1,2 км', act: () => go('s-insp-run') }, { label: 'ООО «Урал-Агро»', sub: 'Сухой Лог · 64 км', act: () => go('s-insp-run') }, { label: 'ст. Богданович', sub: 'приёмка вагонов · 38 км', act: () => go('s-insp-run') }] }));
R('*', '.tab-i', 'Профиль', (t) => { if (t.dataset.go !== 's-insp') return go(t.dataset.go); openSheet({ title: 'Пётр Смирнов · инспектор', text: 'Сюрвейерская компания «УралКонтроль». Офлайн-данные хранятся 7 дней.', buttons: [{ label: 'Выйти', act: () => { hist.length = 0; show('s-login', false); } }, { label: 'Закрыть', kind: 'sec' }] }); });

/* ---------- общие поведения ---------- */
function selectIn(el, multi) { if (multi === true && el.closest('.wrap')) { $$('.chip', el.parentElement).forEach(c => c.classList.remove('on')); el.classList.add('on'); return; }
  $$(':scope > *', el.parentElement).forEach(c => c.classList.toggle('on', c === el)); }
function addPhoto(t) { const tile = t.classList.contains('add') ? t : null; if (!tile) { toast('Фото открыто на весь экран'); return; }
  const n = tile.cloneNode(false); n.className = tile.className.replace('add', '').trim(); n.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 8.5A1.5 1.5 0 0 1 5.5 7h2.3l1.5-2.2h5.4L16.2 7h2.3A1.5 1.5 0 0 1 20 8.5v9.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18z"/><circle cx="12" cy="13" r="3.5"/></svg><span>IMG_' + (2042 + Math.floor(Math.random() * 50)) + '</span>'; n.style.background = 'linear-gradient(160deg,#A39F8A,#6E6A58)'; n.style.color = '#fff';
  tile.parentElement.insertBefore(n, tile); toast('Фото добавлено'); }
function editable(el) { const b = $('b', el) || el; if (b.isContentEditable) return; const ph = el.classList.contains('ph');
  if (ph) { b.textContent = ''; el.classList.remove('ph'); b.style.fontWeight = '400'; } b.contentEditable = 'true'; b.classList.add('pv-edit'); el.classList.add('pv-focus'); b.focus();
  const r = document.createRange(); r.selectNodeContents(b); r.collapse(false); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
  b.addEventListener('blur', () => { el.classList.remove('pv-focus'); }, { once: true }); }
function searchInput(el) { if ($('.pv-input', el)) { $('.pv-input', el).focus(); return; }
  const txt = [...el.childNodes].filter(n => n.nodeType === 3 && norm(n.textContent)); const ph = txt.map(n => n.textContent).join('').trim(); txt.forEach(n => n.remove());
  el.insertAdjacentHTML('beforeend', '<span class="pv-input" contenteditable="true" data-ph="' + ph + '"></span>'); const inp = $('.pv-input', el); inp.focus();
  if (current === 's-cat') inp.addEventListener('input', () => { const q = norm(inp.textContent).toLowerCase(); $$('.pcard', store['s-cat']).forEach(p => { if (p.dataset.ind && !$('.seg .on', store['s-cat']).textContent.includes('Пром')) return; p.style.display = !q || norm(p.textContent).toLowerCase().includes(q) ? '' : 'none'; }); });
  if (current === 's-chat') inp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); chatSend(); } });
}
function generic(el) {
  const c = el.closest('.sbtn'); if (c) { const st = c.closest('.stepper'); const v = stepVal(st); const k = UNITS[v.u] || UNITS['т']; const plus = c === st.lastElementChild; const min = k.step;
    const nv = plus ? v.n + k.step : v.n - k.step; if (nv < min) { toast('Минимальный заказ — ' + fmtT(min * k.t) + ' т'); return true; } stepSet(st, nv, v.u);
    if (current === 's-prod' && st.closest('.dock')) { if (v.u === 'МКР') $('.val small', st).textContent = '= ' + fmtT(nv * 0.6) + ' т'; prodBtn(); }
    if (current === 's-cart') recalc(); return true; }
  const seg = el.closest('.seg > div'); if (seg) { selectIn(seg); return true; }
  const chip = el.closest('.chip'); if (chip) { if (chip.closest('.wrap')) chip.classList.toggle('on'); else selectIn(chip); return true; }
  const tg = el.closest('.tgl'); if (tg) { tg.classList.toggle('on'); return true; }
  const cb = el.closest('.cbx'); if (cb) { cb.classList.toggle('on'); cb.innerHTML = cb.classList.contains('on') ? ICON_OK.replace(/22/g, '16') : ''; return true; }
  const srch = el.closest('.search'); if (srch && !srch.dataset.go) { searchInput(srch); return true; }
  const fld = el.closest('.field'); if (fld) { editable(fld); return true; }
  return false;
}
const FALLBACK = '.btn, .icon-btn, .lrow, .link, .card.row, .card.tight, .pcard, .ck, .ph-t, .ph-l, .fab, .chip, .tab-i';

/* ---------- клик ---------- */
phone.addEventListener('click', e => {
  if (e.target.closest('.pv-input, .pv-edit')) return;
  const m = matchRule(e.target); if (m) { m.r.fn(m.t); return; }
  const g = e.target.closest('[data-go]'); if (g && phone.contains(g)) { g.dataset.go === 'back' ? back() : go(g.dataset.go); return; }
  if (generic(e.target)) return;
  const f = e.target.closest(FALLBACK); if (f && phone.contains(f)) { toast('«' + norm(f.textContent).slice(0, 36) + '» — в прототипе без отдельного экрана'); return; }
  // промах: подсветить кликабельные зоны, как в Figma
  phone.classList.add('pv-hint'); clearTimeout(phone._h); phone._h = setTimeout(() => phone.classList.remove('pv-hint'), 700);
});

/* ---------- вход-демо для инспектора и стартовая подготовка ---------- */
const lg = store['s-login']; const sup = $$('.t3', lg).pop(); if (sup) sup.insertAdjacentHTML('afterend', '<div class="pv-demo link" style="text-align:center;font-size:14px">Демо: войти как инспектор →</div>');
const o1602 = $$('.body > .card', store['s-orders']).find(c => norm(c.textContent).startsWith('№ 1602')); if (o1602) o1602.remove();
const em8 = $$('.sec h2 em', store['s-home']).find(e => /активн/.test(e.textContent)); if (em8) em8.textContent = '7 активных';
const kp0 = $$('.card.tight', store['s-home']).find(c => norm(c.textContent).includes('На согласовании')); if (kp0) $('.amount', kp0).textContent = '1';
const s1602 = $$('.nrow', store['s-notif']).find(n => norm(n.textContent).startsWith('Заявка № 1602')); if (s1602) s1602.remove();
recalc(); badges(); prodBtn();

/* ---------- панель сбоку ---------- */
list.addEventListener('click', e => { const a = e.target.closest('a'); if (!a) return; e.preventDefault(); show(a.dataset.id, true); });
const step = d => { const i = ORDER.indexOf(current); show(ORDER[(i + d + ORDER.length) % ORDER.length], true); };
$('#pv-prev').onclick = () => step(-1); $('#pv-next').onclick = () => step(1);
const reset = $('#pv-reset'); if (reset) reset.onclick = () => { location.hash = '#screen=s-login'; location.reload(); };
$$('[data-clone]').forEach(b => { const c = store[b.dataset.clone].cloneNode(true); c.removeAttribute('id'); $$('[data-go]', c).forEach(x => x.removeAttribute('data-go')); b.appendChild(c); });
$$('[data-open]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); show(a.dataset.open, true); $('#proto').scrollIntoView({ behavior: 'smooth' }); }));
const start = (location.hash.match(/screen=([a-z0-9-]+)/) || [])[1];
show(store[start] ? start : 's-login', false);
if (store[start] && start !== 's-login') setTimeout(() => $('#proto').scrollIntoView(), 50);
window.pv = { show, S, cartCount, groups, rowsOf, toast, openSheet };
})();
