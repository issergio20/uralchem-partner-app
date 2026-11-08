"""Генерация из tokens/tokens.json:
  tokens/tokens.css      — CSS-переменные (+ короткие алиасы, которыми пользуются прототипы)
  figma/variables.js     — скрипт Plugin API для use_figma: коллекции переменных, текстовые стили,
                           привязка заливок/радиусов/текста к токенам на текущей странице.
Запуск: python -I src/tokens.py
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tokens" / "tokens.json").read_text(encoding="utf-8"))


def leaves(node, path=()):
    for k, v in node.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" in v:
            yield path + (k,), v
        elif isinstance(v, dict):
            yield from leaves(v, path + (k,))


def resolve(ref):
    m = re.fullmatch(r"\{(.+)\}", ref) if isinstance(ref, str) else None
    if not m:
        return ref
    node = T
    for p in m.group(1).split("."):
        node = node[p]
    return resolve(node["$value"])


prim = {"/".join(p[2:]): v["$value"] for p, v in leaves(T["primitive"]["color"], ("primitive", "color"))}
sem = {p[-1]: v["$value"] for p, v in leaves(T["semantic"]["color"])}
space = {k: int(v["$value"][:-2]) for k, v in T["space"].items()}
radius = {k: int(v["$value"][:-2]) for k, v in T["radius"].items()}
size = {k: int(v["$value"][:-2]) for k, v in T["size"].items()}
typo = {k: v["$value"] for k, v in T["typography"].items()}
family = T["font"]["family"]["$value"]

# ---------- CSS ----------
css = [":root{"]
for name, val in prim.items():
    css.append(f"  --p-{name.replace('/', '-')}:{val};")
for name, ref in sem.items():
    pname = ref.strip("{}").split(".", 2)[2].replace(".", "-")
    css.append(f"  --color-{name}:var(--p-{pname});")
for k, v in space.items():
    css.append(f"  --space-{k}:{v}px;")
for k, v in radius.items():
    css.append(f"  --radius-{k}:{v}px;")
for k, v in size.items():
    css.append(f"  --size-{k}:{v}px;")
for k, v in typo.items():
    css.append(f"  --font-{k}:{v['fontWeight']} {v['fontSize']}/{v['lineHeight']} \"{family}\",system-ui,sans-serif;")
# короткие алиасы, исторически используемые в прототипах
alias = {"bg": "bg", "surface": "surface", "surface-2": "surface-2", "border": "border", "border-strong": "border-strong",
         "t1": "text-primary", "t2": "text-secondary", "t3": "text-tertiary", "blue": "action-brand",
         "green": "accent", "green-a": "action-primary", "green-p": "action-primary-pressed",
         "ok": "success-fg", "ok-bg": "success-bg", "warn": "warning-fg", "warn-bg": "warning-bg", "warn-f": "warning-fill",
         "err": "danger-fg", "err-bg": "danger-bg", "info": "info-fg", "info-bg": "info-bg"}
for a, s in alias.items():
    css.append(f"  --{a}:var(--color-{s});")
css.append("  --blue-2:var(--p-blue-700);")
css.append("}")
(ROOT / "tokens" / "tokens.css").write_text("\n".join(css) + "\n", encoding="utf-8")

# ---------- Figma script ----------
data = {
    "prim": prim,
    "sem": {k: v.strip("{}").split(".", 2)[2].replace(".", "/") for k, v in sem.items()},
    "space": space, "radius": radius, "size": size,
    "typo": {k: {"size": int(v["fontSize"][:-2]), "lh": int(v["lineHeight"][:-2]), "w": v["fontWeight"]} for k, v in typo.items()},
    "family": family,
}
JS = r"""// Сгенерировано src/tokens.py из tokens/tokens.json — не править руками.
// Выполняется в use_figma на странице с макетами. Идемпотентно: повторный запуск переиспользует коллекции и стили.
const D = __DATA__;
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
"""
(ROOT / "figma").mkdir(exist_ok=True)
js = JS.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(ROOT / "figma" / "variables.js").write_text(js, encoding="utf-8")
print("tokens.css,", "variables.js", len(js), "chars;", len(prim), "primitives,", len(sem), "semantic")
