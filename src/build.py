"""Сборка прототипов.

  python -I src/build.py              -> prototypes.html (картинки по относительным путям)
  python -I src/build.py --inline OUT -> OUT (картинки в base64, для html_to_figma)

Открыть кликабельный прототип: prototypes.html#proto=s-login
"""
import base64, json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from icons import svg

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "prototypes.src.html").read_text(encoding="utf-8")
more = (ROOT / "src" / "screens-more.html").read_text(encoding="utf-8")
tokens_css = (ROOT / "tokens" / "tokens.css").read_text(encoding="utf-8")
T = json.loads((ROOT / "tokens" / "tokens.json").read_text(encoding="utf-8"))

SB = ('<div class="sb"><span class="sb-t">9:41</span><img class="sb-logo" src="assets/logo.png" alt="УРАЛХИМ">'
      '<span class="sb-r"><svg width="17" height="11" viewBox="0 0 17 11"><rect x="0" y="7" width="3" height="4" rx="1"/><rect x="4.5" y="5" width="3" height="6" rx="1"/>'
      '<rect x="9" y="2.5" width="3" height="8.5" rx="1"/><rect x="13.5" y="0" width="3" height="11" rx="1"/></svg>'
      '<svg width="25" height="12" viewBox="0 0 25 12"><rect x=".5" y=".5" width="21" height="11" rx="3" fill="none" stroke="currentColor" opacity=".4"/>'
      '<rect x="2" y="2" width="18" height="8" rx="2"/><rect x="22.5" y="4" width="1.8" height="4" rx=".9" opacity=".4"/></svg></span></div>')

BUYER = [("home", "Главная", "home", "s-home"), ("grid", "Каталог", "cat", "s-cat"), ("clip", "Заявки", "req", "s-orders"),
         ("cart", "Корзина", "cart", "s-cart"), ("user", "Профиль", "prof", "s-profile")]
INSP = [("clip", "Задачи", "tasks", "s-insp"), ("pin", "Объекты", "obj", "s-insp-run"), ("camera", "Замечания", "rem", "s-remark"),
        ("sync", "Синхр.", "sync", "s-sync"), ("user", "Профиль", "prof", "s-insp")]


def tabbar(items, active, badges):
    out = ['<nav class="tab">']
    for ic, label, key, go in items:
        b = f'<span class="tab-b">{badges[key]}</span>' if key in badges else ""
        out.append(f'<div class="tab-i{" on" if key == active else ""}" data-go="{go}"><span class="tab-ic">{svg(ic, 24)}{b}</span>{label}</div>')
    out.append('<div class="home-ind"></div></nav>')
    return "".join(out)


# ---------- лист «Дизайн-система» из tokens.json ----------
def leaves(node, path=()):
    for k, v in node.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" in v:
            yield path + (k,), v
        elif isinstance(v, dict):
            yield from leaves(v, path + (k,))


def res(v):
    m = re.fullmatch(r"\{(.+)\}", v) if isinstance(v, str) else None
    if not m:
        return v
    n = T
    for p in m.group(1).split("."):
        n = n[p]
    return res(n["$value"])


def ds_sheet():
    prim = "".join(f'<div class="ds-sw"><div style="background:{v["$value"]}"></div><p><b>{"/".join(p)}</b>{v["$value"]}</p></div>'
                   for p, v in leaves(T["primitive"]["color"]))
    sem_rows = "".join(
        f'<div class="ds-row"><span style="width:40px;height:40px;border-radius:10px;background:{res(v["$value"])};border:1px solid var(--border);flex:none"></span>'
        f'<code>color/{p[-1]}</code><span class="t3">{v["$value"].strip("{}").replace("primitive.color.", "")} · {res(v["$value"])}</span>'
        f'<span class="t2" style="flex:1">{v.get("$description", "")}</span></div>'
        for p, v in leaves(T["semantic"]["color"]))
    typo = "".join(
        f'<div class="ds-row"><code>УРАЛХИМ/{k}<br>{v["$value"]["fontSize"]} / {v["$value"]["lineHeight"]} · {v["$value"]["fontWeight"]}</code>'
        f'<span style="font:var(--font-{k})">Карбамид марки Б · 68 т · 4 352 000 ₽</span></div>'
        for k, v in T["typography"].items())
    space = "".join(f'<div class="ds-row"><code>space/{k} · {v["$value"]}</code><span style="height:16px;width:{v["$value"]};background:var(--green);border-radius:3px"></span></div>'
                    for k, v in T["space"].items())
    rad = "".join(f'<div style="text-align:center"><div style="width:72px;height:72px;background:#E8E9F4;border:2px solid var(--blue);border-radius:{v["$value"]}"></div><div class="t3" style="margin-top:6px">radius/{k}<br>{v["$value"]}</div></div>'
                  for k, v in T["radius"].items())
    comps = f'''
      <div class="btn pri">Основная</div><div class="btn blue">Бренд</div><div class="btn sec">Вторичная</div><div class="btn out">Контурная</div>
      <div class="btn m pri">M · 44</div><div class="btn s pri">S · 36</div>
      <span class="chip on">Чипс активный <span class="n">84</span></span><span class="chip">Чипс <span class="n">23</span></span>
      <span class="pill neu">Согласование</span><span class="pill info">Подтверждена</span><span class="pill warn">Отгрузка</span><span class="pill ok">В пути</span><span class="pill err">Отклонена</span>
      <div class="npk"><span><i>N</i>18</span><span><i>P</i>18</span><span><i>K</i>18</span></div>
      <div class="stepper" style="width:170px"><div class="sbtn">{svg("minus", 18)}</div><div class="val"><b>40 меш.</b><small>= 1 т</small></div><div class="sbtn">{svg("plus", 18)}</div></div>
      <div class="seg" style="width:300px"><div class="on">Отгрузка</div><div>Состав</div><div>Документы</div></div>
      <span class="tgl on"><i></i></span><span class="tgl"><i></i></span><span class="cbx on">{svg("check", 16)}</span><span class="cbx"></span>
      <div class="field" style="width:320px"><div class="fl"><small>Станция назначения</small><b>Баженово, Свердловская ж/д</b></div></div>
      <div class="search" style="width:320px">{svg("search", 20)}Продукт, марка или NPK</div>
      <div style="width:375px;border:1px solid var(--border)">{tabbar(BUYER, "home", {"cart": "3"})}</div>'''
    return f'''<section class="sheet" id="ds">
  <div class="eyebrow">Дизайн-система · tokens.json → переменные Figma</div>
  <h1>Токены и компоненты</h1>
  <p class="lead">Единый источник — <b>tokens/tokens.json</b> (W3C DTCG). Из него собираются CSS-переменные прототипа и коллекции переменных Figma: <b>Primitives</b> (палитра), <b>Tokens</b> (семантика, алиасы на палитру, режим Light), <b>Dimensions</b> (отступы, радиусы, размеры) и 10 текстовых стилей <b>УРАЛХИМ/*</b>.</p>
  <h2>Палитра · Primitives</h2><div class="ds-grid">{prim}</div>
  <div class="ds-cols"><div><h2>Семантика · Tokens</h2>{sem_rows}</div>
  <div><h2>Типографика · Onest</h2>{typo}<h2>Отступы · space</h2>{space}<h2>Радиусы · radius</h2><div class="ds-comp" style="gap:20px">{rad}</div></div></div>
  <h2>Компоненты</h2><div class="ds-comp">{comps}</div>
</section>'''


FIGMA = "https://www.figma.com/design/0ZiD08orz1A578mig90EW3/%D0%A3%D0%A0%D0%90%D0%9B%D0%A5%D0%98%D0%9C-%E2%80%94-%D0%9B%D0%9A-%D0%BF%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D0%B0-%C2%B7-%D0%A0%D0%B5%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-2026?node-id=0-1&t=X1AbiOfTo47yDXY6-1"
HDR = (f'<header class="hdr board-hdr"><div class="hdr-in">'
       f'<a class="back-btn" href="index.html">{svg("back", 20)}Назад к кейсу</a>'
       f'<a class="brand" href="index.html"><img src="assets/logo.png" alt="УРАЛХИМ"><span>Все макеты одним полотном</span></a>'
       f'<nav class="menu-top"><a href="index.html">Описание проекта</a><a href="prototip.html">Прототипы</a><a href="ui-kit.html">UI kit</a>'
       f'<a class="fig" href="{FIGMA}" target="_blank" rel="noopener">Figma {svg("ext", 16)}</a></nav></div></header>')
html = src.replace("{{hdr}}", HDR).replace("{{more}}", more).replace("{{ds}}", ds_sheet()).replace("{{tokens}}", tokens_css).replace("{{sb}}", SB)
html = re.sub(r"\{\{tab:(\w+)\}\}", lambda m: tabbar(BUYER, m.group(1), {"cart": "3"}), html)
html = re.sub(r"\{\{tab0:(\w+)\}\}", lambda m: tabbar(BUYER, m.group(1), {}), html)
html = re.sub(r"\{\{tabi:(\w+)\}\}", lambda m: tabbar(INSP, m.group(1), {"sync": "3"}), html)
html = re.sub(r"\{\{i:(\w+)(?::(\d+))?\}\}", lambda m: svg(m.group(1), int(m.group(2) or 20)), html)
assert "{{" not in html, html[html.index("{{"):html.index("{{") + 40]

# подписи кнопок, чипсов и статусов → <span class="lbl"> с многоточием (текст не наезжает на паддинги)
def _wrap_lbl(m):
    open_tag, icon, text = m.group(1), m.group(2) or "", m.group(3)
    if not text.strip():
        return m.group(0)
    lead = text[:len(text) - len(text.lstrip())]
    return f'{open_tag}{icon}{lead}<span class="lbl">{text.strip()}</span>{" " if text.endswith(" ") else ""}'
html = re.sub(r'(<(?:div|span) class="(?:btn|chip|pill)\b[^"]*"[^>]*>)((?:\s*<svg\b.*?</svg>)?)([^<]+)', _wrap_lbl, html, flags=re.S)

if len(sys.argv) > 2 and sys.argv[1] == "--inline":
    def inline(m):
        p = ROOT / m.group(1)
        return 'src="data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'
    html = re.sub(r'src="(assets/[^"]+\.png)"', inline, html)
    pathlib.Path(sys.argv[2]).write_text(html, encoding="utf-8")
    print("inline ->", sys.argv[2], len(html) // 1024, "KB")
else:
    (ROOT / "prototypes.html").write_text(html, encoding="utf-8")
    print("prototypes.html", len(html) // 1024, "KB,", html.count('class="screen'), "screens")
