// Сгенерировано src/tokens.py из tokens/tokens.json — не править руками.
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
