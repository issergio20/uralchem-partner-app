"""Мини-сайт кейса: index.html (Описание проекта) · prototip.html (Прототипы: кликабельный + до/после) · ui-kit.html.
Берёт стили и экраны из собранного prototypes.html, поэтому запускать после build.py:
  python -I src/build.py && python -I src/site.py
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from icons import svg, P as ICONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
board = (ROOT / "prototypes.html").read_text(encoding="utf-8")
STYLE = re.search(r"<style>(.*?)</style>", board, re.S).group(1)
SCREENS = re.findall(r'<section class="screen[^"]*" id="[\w-]+".*?</section>', board, re.S)
SB = re.search(r'<div class="sb">.*?</span></div>', board, re.S).group(0)
T = json.loads((ROOT / "tokens" / "tokens.json").read_text(encoding="utf-8"))
FIGMA = "https://www.figma.com/design/0ZiD08orz1A578mig90EW3/%D0%A3%D0%A0%D0%90%D0%9B%D0%A5%D0%98%D0%9C-%E2%80%94-%D0%9B%D0%9A-%D0%BF%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D0%B0-%C2%B7-%D0%A0%D0%B5%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-2026?node-id=0-1&t=X1AbiOfTo47yDXY6-1"

SITE_CSS = r"""
.h2s,.kit-sec,.ba{scroll-margin-top:92px}
body.site{padding:0;background:var(--bg);min-height:100vh;display:flex;flex-direction:column}
.hdr{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.hdr-in{max-width:1240px;margin:0 auto;height:72px;padding:0 24px;display:flex;align-items:center;gap:24px}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--t1);min-width:0}
.brand img{height:18px;flex:none}
.brand span{font-size:13px;color:var(--t3);border-left:1px solid var(--border);padding-left:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.menu-top{margin-left:auto;display:flex;gap:4px}
.menu-top a{height:40px;padding:0 16px;border-radius:12px;display:flex;align-items:center;font-size:15px;font-weight:600;color:var(--t2);text-decoration:none;white-space:nowrap}
.menu-top a:hover{background:var(--surface-2)}
.menu-top a.on{background:var(--blue);color:#fff}
.wrapx{max-width:1240px;margin:0 auto;padding:48px 24px 96px;width:100%;flex:1}
.ph1{font-size:44px;line-height:52px;font-weight:700;color:var(--blue);letter-spacing:-.02em}
.plead{font-size:19px;line-height:29px;color:var(--t2);max-width:860px;margin-top:14px}
.eyeb{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--green-a);margin-bottom:12px}
.h2s{font-size:28px;line-height:34px;font-weight:700;margin:64px 0 20px;color:var(--t1)}
.h3s{font-size:18px;line-height:24px;font-weight:600;margin:28px 0 12px}
.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.box{background:var(--surface);border-radius:20px;padding:24px}
.box h4{font-size:18px;line-height:24px;font-weight:600;margin:12px 0 8px}
.box p,.box li{font-size:15px;line-height:23px;color:var(--t2)}
.box ul{padding-left:18px}
.tagx{display:inline-flex;height:26px;padding:0 10px;border-radius:999px;font-size:12px;font-weight:700;align-items:center;letter-spacing:.04em}
.meta{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--border);border-radius:20px;overflow:hidden;margin-top:36px}
.meta div{background:var(--surface);padding:18px 20px}
.meta small{display:block;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--t3)}
.meta b{display:block;font-size:16px;line-height:22px;font-weight:600;margin-top:6px}
.hero-row{display:grid;grid-template-columns:1fr 360px;gap:48px;align-items:center}
.hero-phone{zoom:.82;justify-self:center;border-radius:40px;overflow:hidden;box-shadow:0 30px 70px rgba(39,42,107,.22);height:812px}
.metric2{border-left:3px solid var(--green);padding:4px 0 4px 18px}
.metric2 b{font-size:32px;line-height:40px;color:var(--blue);display:block}
.metric2 span{font-size:15px;line-height:22px;color:var(--t2)}
.links a{color:var(--blue);font-weight:600}
.cta{display:inline-flex;align-items:center;gap:8px;height:52px;padding:0 22px;border-radius:14px;background:var(--green-a);color:#fff;font-weight:600;text-decoration:none;margin-top:28px;margin-right:10px}
.cta.sec{background:var(--surface);color:var(--blue);border:1.5px solid var(--border)}
.foot{border-top:1px solid var(--border);background:var(--surface)}
.foot div{max-width:1240px;margin:0 auto;padding:20px 24px;font-size:13px;color:var(--t3);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
/* прототип */
.pv{display:grid;grid-template-columns:240px 399px minmax(0,1fr);gap:28px;align-items:start}
.pv-list{background:var(--surface);border-radius:20px;padding:12px;position:sticky;top:96px;max-height:calc(100vh - 120px);overflow:auto}
.pv-list .grp{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--t3);padding:12px 10px 6px}
.pv-list a{display:block;padding:8px 10px;border-radius:10px;font-size:14px;line-height:19px;color:var(--t2);text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pv-list a:hover{background:var(--surface-2)}
.pv-list a.on{background:var(--blue);color:#fff;font-weight:600}
.phone{width:399px;height:836px;border-radius:54px;background:#111226;padding:12px;box-shadow:0 30px 80px rgba(17,18,38,.35);position:sticky;top:96px}
.phone-in{width:375px;height:812px;border-radius:42px;overflow-y:auto;overflow-x:hidden;background:#fff;scrollbar-width:none}
.phone-in::-webkit-scrollbar{display:none}
.phone-in .screen{box-shadow:none}
.phone-in .screen{overflow:clip}
.phone-in .sb{position:sticky;top:0;z-index:7}
.phone-in .tab,.phone-in .dock{position:sticky;bottom:0;z-index:7}
.phone-in .tab-i{cursor:pointer;border-radius:12px;transition:color .15s}
.phone-in .tab-i:hover{color:var(--blue)}
.phone-in .fab{z-index:8}
.phone-in .btn:active,.phone-in .card:active,.phone-in .chip:active,.phone-in .lrow:active,.phone-in .tab-i:active{transform:scale(.98);transition:transform .08s}
.phone-in.pv-hint [data-go],.phone-in.pv-hint .btn,.phone-in.pv-hint .chip,.phone-in.pv-hint .card.row,.phone-in.pv-hint .card.tight,.phone-in.pv-hint .lrow,.phone-in.pv-hint .icon-btn,.phone-in.pv-hint .field,.phone-in.pv-hint .search,.phone-in.pv-hint .sbtn,.phone-in.pv-hint .seg>div,.phone-in.pv-hint .link,.phone-in.pv-hint .pcard,.phone-in.pv-hint .ck,.phone-in.pv-hint .tgl,.phone-in.pv-hint .cbx{box-shadow:inset 0 0 0 2px rgba(0,95,204,.55);background-color:rgba(0,115,255,.07)}
.phone{position:sticky}
.pv-toast{position:absolute;left:24px;right:24px;bottom:110px;z-index:30;background:#1E2050;color:#fff;border-radius:14px;padding:12px 14px;font-size:14px;line-height:19px;display:flex;gap:12px;align-items:center;box-shadow:0 10px 30px rgba(17,18,38,.35);animation:pvIn .2s ease-out}
.pv-toast[hidden],.pv-ov[hidden]{display:none!important}
.phone-in .chips{overflow-x:auto;scrollbar-width:none;margin-right:-16px;padding-right:16px}
.phone-in .chips::-webkit-scrollbar{display:none}
.pv-toast span{flex:1}.pv-toast b{color:#7BE3AE;cursor:pointer;white-space:nowrap}
.pv-toast.out{opacity:0;transform:translateY(8px);transition:.2s}
.pv-ov{position:absolute;inset:12px;border-radius:42px;overflow:hidden;z-index:40;background:rgba(17,18,38,0);display:flex;align-items:flex-end;transition:background .2s}
.pv-ov.in{background:rgba(17,18,38,.42)}
.pv-sheet{width:100%;background:#fff;border-radius:22px 22px 0 0;padding:10px 16px 30px;transform:translateY(100%);transition:transform .22s ease-out;max-height:80%;overflow:auto}
.pv-ov.in .pv-sheet{transform:none}
.pv-sheet .handle{margin:0 auto 12px}
.ps-t{font-size:18px;line-height:24px;font-weight:700;color:var(--t1)}
.ps-x{font-size:14px;line-height:21px;color:var(--t2);margin-top:6px}
.ps-list{margin-top:10px}
.ps-i{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--surface-2);cursor:pointer}
.ps-i>div{flex:1;min-width:0}.ps-i b{display:block;font-size:15px;line-height:21px;font-weight:600;color:var(--t1)}.ps-i span{display:block;font-size:13px;color:var(--t3)}
.ps-i em{font-style:normal;color:var(--t3);font-size:18px}.ps-i.on em{color:var(--ok)}
.ps-btns{display:flex;flex-direction:column;gap:8px;margin-top:16px}
.pv-danger{background:var(--err)!important}
@keyframes pvIn{from{opacity:0;transform:translateY(8px)}}
.pv-focus{border:2px solid var(--blue)!important}
.pv-edit{outline:none;display:block;min-height:22px}
.pv-input{flex:1;outline:none;color:var(--t1);min-width:0}
.pv-input:empty::before{content:attr(data-ph);color:var(--t3)}
.acc{padding:0 0 14px;font-size:14px;line-height:21px;color:var(--t2);display:flex;flex-direction:column;gap:6px}
.pv-doc{color:var(--blue);font-weight:600;cursor:pointer}
.lrow.open .chev svg{transform:rotate(180deg)}
.fav-off{color:var(--t3)!important}
.pv-new{box-shadow:inset 0 0 0 2px var(--green)}
.pv-path{margin-top:20px;background:var(--bg);border-radius:16px;padding:14px 16px;font-size:14px;line-height:21px;color:var(--t2)}
.pv-path b{color:var(--t1)}.pv-path ol{margin:6px 0 0 18px}
.pv-demo{cursor:pointer}
.pv-note{background:var(--surface);border-radius:20px;padding:24px;position:sticky;top:96px}
.pv-note h3{font-size:22px;line-height:28px;font-weight:700}
.pv-note .lead2{font-size:15px;line-height:23px;color:var(--t2);margin-top:8px}
.pv-note ul{margin:14px 0 0 18px;font-size:15px;line-height:23px;color:var(--t2)}
.pv-note .nav2{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap}.pv-note .nav2 .btn{flex:1 1 auto;min-width:0}
.hint{font-size:13px;color:var(--t3);margin-top:16px;line-height:19px}
.ba{background:var(--surface);border-radius:24px;padding:28px;margin-bottom:24px}
.ba-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}
.ba-head h3{font-size:22px;line-height:28px;font-weight:700}
.ba-grid{display:grid;grid-template-columns:auto auto 1fr;gap:32px;margin-top:20px;align-items:start}
.ba-col small{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
.ba-old{display:flex;gap:12px}
.ba-old .sc{width:240px;max-height:650px;overflow-y:auto;border-radius:24px;border:1px solid var(--border);background:#fff;scrollbar-width:thin}
.ba-old img{width:100%;display:block}
.ba-new{width:300px;height:650px;border-radius:30px;overflow-y:auto;overflow-x:hidden;border:1px solid var(--border);scrollbar-width:thin}
.ba-new .screen{zoom:.8;box-shadow:none}
.ba-list{font-size:15px;line-height:23px;color:var(--t2);padding-left:18px}
.ba-list li{margin-bottom:8px}
.subnav{display:flex;gap:8px;margin:28px 0 8px;flex-wrap:wrap}
.subnav a{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--border);background:var(--surface);display:flex;align-items:center;font-size:14px;font-weight:600;color:var(--t2);text-decoration:none}
/* ui kit */
.kit-sec{background:var(--surface);border-radius:24px;padding:28px;margin-bottom:24px}
.kit-sec>h2{font-size:24px;line-height:30px;font-weight:700}
.kit-sec>p{font-size:15px;line-height:22px;color:var(--t3);margin-top:4px}
.kit-row{display:flex;flex-wrap:wrap;gap:20px 24px;align-items:flex-start;margin-top:20px}
.kit-item{display:flex;flex-direction:column;gap:8px;min-width:0}
.kit-item>code{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:var(--t3)}
.kit-pad{background:var(--bg);border-radius:16px;padding:16px}
.kit-bare{border:1px solid var(--border);border-radius:16px;overflow:hidden;background:var(--surface)}
.kit-bare .tab{position:relative}
.kit-375{width:375px;max-width:100%}
.ic-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px;margin-top:20px}
.ic-grid div{background:var(--bg);border-radius:12px;padding:14px 6px 10px;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--blue)}
.ic-grid code{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:var(--t3)}
.kit-toc{display:flex;flex-wrap:wrap;gap:8px;margin:28px 0 28px}
.kit-toc a{height:34px;padding:0 12px;border-radius:999px;background:var(--surface);border:1px solid var(--border);display:flex;align-items:center;font-size:13px;font-weight:600;color:var(--t2);text-decoration:none}
@media (max-width:1100px){.pv{grid-template-columns:1fr 399px}.pv-note{grid-column:1 / -1;position:static}.ba-grid{grid-template-columns:1fr}.meta{grid-template-columns:repeat(2,1fr)}.g4{grid-template-columns:repeat(2,1fr)}.hero-row{grid-template-columns:1fr}}
@media (max-width:760px){.hdr-in{height:auto;padding:12px 16px;flex-wrap:wrap;gap:10px}.menu-top{margin-left:0;width:100%;overflow-x:auto}.menu-top a{height:36px;padding:0 12px;font-size:14px}
 .wrapx{padding:28px 16px 64px}.ph1{font-size:32px;line-height:38px}.plead{font-size:17px;line-height:26px}
 .g2,.g3,.g4,.meta{grid-template-columns:1fr}.pv{grid-template-columns:1fr}.pv-list{position:static;max-height:220px}
 .pv{grid-template-columns:minmax(0,1fr)}
 .phone{width:auto;height:auto;padding:0;background:none;box-shadow:none;position:relative;border-radius:0}
 .pv-ov{inset:0;border-radius:24px}
 .phone-in{width:100%;height:740px;border-radius:24px;border:1px solid var(--border)}
 .phone-in .screen{zoom:.9}
 .ds-row{flex-wrap:wrap;gap:6px 16px}.ds-row code{width:100%}
 .kit-375,.kit-bare,.kit-pad{max-width:100%;overflow-x:auto}.ba-old{flex-wrap:wrap}.ba-old .sc{width:46%}
 .kit-sec,.ba{padding:18px}.hero-phone{display:none}.box{padding:18px}}
"""

PAGES = [("index.html", "Описание проекта"), ("prototip.html", "Прототипы"), ("ui-kit.html", "UI kit")]


def page(fname, title, body, extra_js=""):
    nav = "".join(f'<a href="{f}"{" class=\"on\"" if f == fname else ""}>{t}</a>' for f, t in PAGES)
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · УРАЛХИМ — ЛК партнёра</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{STYLE}{SITE_CSS}</style></head>
<body class="site">
<header class="hdr"><div class="hdr-in"><a class="brand" href="index.html"><img src="assets/logo.png" alt="УРАЛХИМ"><span>Личный кабинет партнёра · редизайн 2026</span></a><nav class="menu-top">{nav}<a class="fig" href="{FIGMA}" target="_blank" rel="noopener">Figma {svg("ext", 16)}</a></nav></div></header>
<main class="wrapx">{body}</main>
<footer class="foot"><div><span>Кейс Ivanov Sergio · 2026 · данные в макетах демонстрационные</span><span class="links"><a href="{FIGMA}" target="_blank" rel="noopener">Figma</a> · <a href="prototypes.html">Все макеты одним полотном</a></span></div></footer>
{extra_js}
</body></html>"""


def screen(sid):
    for s in SCREENS:
        if f'id="{sid}"' in s:
            return s
    raise KeyError(sid)


def frag(html, start):
    """Фрагмент от тега, начинающегося с `start`, до его парного </div> (с учётом вложенности)."""
    i = html.index(start)
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", html[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return html[i:i + m.end()]
    raise ValueError(start)


# ======================= 1. ОПИСАНИЕ ПРОЕКТА =======================
problems = [
    ("Главная без иерархии", "9 равноценных виджетов на 2300 px. Новости стоят первыми, а вагоны в пути и долг — на четвёртом экране прокрутки."),
    ("Две сущности, одни статусы", "«Заявки» и «Заказы» показывают одинаковые 7 внутренних статусов вроде «Утверждена в ЛК» и «Отправлена в клиентский сервис»."),
    ("Количество в «0.025 т»", "Шаг степпера — один мешок, для вагонных партий это неудобно. Мешки и МКР не различаются, цены и итога нет."),
    ("Трекинг без даты прибытия", "12 станций с одинаковым временем, станции повторяются. Нет ответа на главный вопрос: когда вагон будет на моей станции."),
    ("Статусы — цветные точки", "Точку 8 px плохо видно при дальтонизме. Серые подписи на сером дают контраст около 3:1, белый на #00A55A — 3,2:1."),
    ("Таббар не про работу", "Заявок в таббаре нет. В макете там «Уведомления», в живом приложении — «Обращения»."),
]
solutions = [
    ("Главная = «требует действия»", "Сверху подтверждения и счета, ниже вагоны с датой прибытия, счётчики заявок, финансы и быстрые действия. Новости и обучение переехали в профиль."),
    ("Единый жизненный цикл", "Одна сущность «Заявка» и 5 понятных статусов: согласование → подтверждена → отгрузка → в пути → доставлена."),
    ("Единицы от фасовки и цены", "Мешки считаются в штуках с пересчётом в тонны, навал — в тоннах и вагонах. Цена за тонну видна в каталоге, итог с НДС — в корзине и на кнопке."),
    ("Трекинг с датой прибытия", "Видны дата прибытия, текущая станция и оставшийся путь. Промежуточные станции свёрнуты, накладная копируется, обращение создаётся прямо из вагона."),
    ("Офлайн для инспектора", "Задачи дня, чек-лист, замечания с фото и очередь синхронизации работают без сети."),
    ("Доступная визуальная система", "Статус показан пилюлей с текстом. Для кнопок взят Green action #00844A с контрастом 4,8:1. Шрифт Onest, токены в формате W3C DTCG."),
]
about = f"""
<div class="hero-row"><div>
<div class="eyeb">Кейс · B2B · мобильное приложение · iOS</div>
<h1 class="ph1">Описание проекта</h1>
<p class="plead">«Личный кабинет партнёра» — приложение «Уралхима» для дистрибьюторов минеральных удобрений и проверяющих. Через него заказывают продукцию вагонами, следят за отгрузками, сверяют счета и проводят инспекции складов. Задача — перестроить ключевые сценарии вокруг вопроса «что требует моего внимания сейчас» и собрать дизайн-систему.</p>
<a class="cta" href="prototip.html">{svg("grid", 20)}Смотреть прототип</a><a class="cta sec" href="ui-kit.html">UI kit</a>
</div><div class="hero-phone">{screen("s-home")}</div></div>

<div class="meta">
<div><small>Клиент</small><b>АО «ОХК «УРАЛХИМ»</b></div>
<div><small>Продукт</small><b>ЛК партнёра, iOS</b></div>
<div><small>Роль</small><b>UX/UI-дизайн</b></div>
<div><small>Объём</small><b>22 экрана, UI kit, прототип</b></div>
<div><small>Год</small><b>2026</b></div>
</div>

<h2 class="h2s">Исходные данные</h2>
<div class="g3">
<div class="box"><span class="tagx" style="background:#E8E9F4;color:var(--blue)">МАКЕТ</span><h4>~360 экранов в Figma</h4><p>Вайрфреймы и UI для 4 ролей: покупатель, сюрвейер, инспектор, хранитель. Плюс UI-kit с палитрой и типографикой на Unity Sans.</p></div>
<div class="box"><span class="tagx" style="background:#E8E9F4;color:var(--blue)">ЖИВОЕ ПРИЛОЖЕНИЕ</span><h4>App Store, версия 1.1.2</h4><p>«Личный кабинет партнера», 5 оценок со средней 5,0, только iPhone. В RuStore и Google Play приложения нет, веб-версия — lk.uralchem.ru.</p></div>
<div class="box"><span class="tagx" style="background:#E8E9F4;color:var(--blue)">АНАЛИЗ</span><h4>UX- и UI-аудит</h4><p>Сценарии работы (JTBD), 20 проблем с приоритетами, новая информационная архитектура, спецификация экранов, аудит контраста и визуальной системы.</p></div>
</div>

<h2 class="h2s">Что мешало</h2>
<div class="g3">{"".join(f'<div class="box"><span class="tagx" style="background:var(--err-bg);color:var(--err)">ПРОБЛЕМА</span><h4>{h}</h4><p>{p}</p></div>' for h, p in problems)}</div>

<h2 class="h2s">Что изменили</h2>
<div class="g3">{"".join(f'<div class="box"><span class="tagx" style="background:var(--ok-bg);color:var(--ok)">РЕШЕНИЕ</span><h4>{h}</h4><p>{p}</p></div>' for h, p in solutions)}</div>

<h2 class="h2s">Навигация</h2>
<div class="g2">
<div class="box"><h4 style="margin-top:0">Покупатель</h4><p>Главная · Каталог · Заявки · Корзина · Профиль. Уведомления — колокольчик в шапке. Обращения создаются из заявки или вагона, финансы, новости и обучение — в профиле.</p></div>
<div class="box"><h4 style="margin-top:0">Инспектор</h4><p>Задачи · Объекты · Замечания · Синхронизация · Профиль. Всё работает без сети, изменения копятся в очереди и уходят при подключении.</p></div>
</div>

<h2 class="h2s">Как измерим</h2>
<div class="g4">
<div class="metric2"><b>≤ 2 мин</b><span>от входа до отправленной повторной заявки</span></div>
<div class="metric2"><b>−30 %</b><span>звонков менеджеру «где мой вагон»</span></div>
<div class="metric2"><b>≥ 90 %</b><span>успешных задач на тесте: найти NPK 18:18:18 и узнать дату прибытия</span></div>
<div class="metric2"><b>↓</b><span>заявок, возвращённых из-за ошибок в станции или грузополучателе</span></div>
</div>

<h2 class="h2s">Что сделано</h2>
<div class="g3">
<div class="box"><h4 style="margin-top:0">Прототипы</h4><p>22 экрана: 18 для покупателя и 4 для инспектора, 111 переходов. Сравнение старой и новой версии по 8 ключевым экранам.</p><p class="links" style="margin-top:10px"><a href="prototip.html">Открыть →</a></p></div>
<div class="box"><h4 style="margin-top:0">UI kit и токены</h4><p>80 переменных: палитра, семантика, отступы, радиусы; 10 текстовых стилей и все компоненты из макетов. Единый источник — tokens.json.</p><p class="links" style="margin-top:10px"><a href="ui-kit.html">Открыть →</a></p></div>
<div class="box"><h4 style="margin-top:0">Figma</h4><p>Файл для переноса и плагин, который сам раскладывает экраны, создаёт переменные и проставляет переходы прототипа.</p><p class="links" style="margin-top:10px"><a href="{FIGMA}">Открыть Figma →</a></p></div>
</div>
<p class="hint">Исследований с пользователями не было: выводы о поведении — гипотезы, план проверки в analysis/ux-audit.md. Номера, суммы и станции в макетах демонстрационные.</p>
"""

# ======================= 2. ПРОТОТИПЫ =======================
NOTES = {
    "s-login": ("Вход", "Почта или телефон, вход по коду из SMS и заметный путь «подключить компанию».", ["Активное поле с рамкой бренда", "Телефон поддержки прямо на экране"]),
    "s-reg": ("Подключение по ИНН", "Регистрация из 6 шагов превратилась в 2: реквизиты подтягиваются из ЕГРЮЛ.", ["Проверка ИНН на лету", "Прогресс «Шаг 1 из 2»"]),
    "s-home": ("Главная покупателя", "За 5 секунд видно, что срочно и где груз.", ["Блок «Требует действия»: подтвердить график, оплатить счёт", "Вагоны в пути с датой прибытия и прогрессом", "Счётчики заявок по статусам, финансы двумя цифрами", "Быстрые действия: новая заявка, повтор, обращение"]),
    "s-cat": ("Каталог", "Продукт находится за 2 экрана без знания дерева разделов.", ["Поиск по марке и формуле NPK", "Чипсы групп с количеством, фильтр с бейджем", "Цена за тонну без НДС", "Кнопка превращается в степпер «40 меш. = 1 т»"]),
    "s-filters": ("Фильтры", "Шторка с фасовкой, типом, культурой и способом внесения.", ["Кнопка показывает число результатов", "Переключатель «Только в наличии»"]),
    "s-prod": ("Карточка товара", "Вместо обрезанных табов — короткий экран с главным.", ["NPK-чипсы и переключатель фасовки", "Крупная цена за тонну, наличие, минимальный заказ", "4 ключевых показателя состава и «Все 13»", "Липкий низ: степпер и сумма на кнопке"]),
    "s-cart": ("Корзина", "Явно показано, что корзина делится на заявки по направлениям.", ["У каждой заявки свой итог без НДС и с НДС", "Своя кнопка «Оформить» у каждой группы"]),
    "s-cart-empty": ("Пустая корзина", "Пустое состояние сразу предлагает повторить прошлую заявку.", ["Станция и грузополучатель подставятся сами"]),
    "s-checkout": ("Оформление заявки", "Один экран вместо цепочки модальных окон.", ["Доставка подставлена из прошлой заявки", "Период отгрузки декадой, а не точной датой", "Расчёт с НДС и сумма на кнопке"]),
    "s-success": ("Заявка отправлена", "Понятно, что будет дальше и когда.", ["Срок ответа менеджера", "Напоминание о второй заявке в корзине"]),
    "s-orders": ("Заявки", "Список с единым словарём статусов и подсветкой «требует действия».", ["Сегменты «Активные / Архив»", "Мини-прогресс жизненного цикла в карточке"]),
    "s-order": ("Заявка и трекинг", "Главный вопрос «когда приедет» — сверху и крупно.", ["5 шагов жизненного цикла", "Дата прибытия и оставшийся путь", "Таймлайн со свёрнутыми станциями, копируемая накладная", "Проблема и чат с менеджером в один тап"]),
    "s-issue": ("Обращение по вагону", "Контекст подставлен, расхождение посчитано автоматически.", ["Тип проблемы чипсами", "Сравнение «по накладной / фактически»", "Фото и документы"]),
    "s-chat": ("Чат с менеджером", "Переписка привязана к заявке.", ["Чип заявки со статусом в шапке", "Файлы прямо в ленте"]),
    "s-notif": ("Уведомления", "У каждого уведомления понятное действие и переход.", ["Фильтры по типам с количеством", "Группировка по дням, отметка непрочитанных"]),
    "s-fin": ("Финансы", "Одна главная цифра «к оплате» вместо трёх валют в строку.", ["Выбор договора и валюты", "Счета со статусами-пилюлями", "Акт сверки и операции с остатком — вторым планом"]),
    "s-profile": ("Профиль", "Хаб второстепенных разделов и личный менеджер.", ["Смена компании", "Звонок или сообщение менеджеру", "Финансы, документы, обращения, избранное"]),
    "s-news": ("Новости", "Новости ушли с главной, но остались под рукой.", ["Рубрики, крупная главная новость"]),
    "s-insp": ("Инспектор — задачи на день", "Работа на объекте без сети.", ["Плашка офлайна с очередью изменений", "Ближайшая задача крупно, остальные по времени", "Кнопка «Замечание» всегда под рукой"]),
    "s-insp-run": ("Инспекция — чек-лист", "Пошаговый чек-лист с фото по каждому пункту.", ["Прогресс 5 из 9", "«Соответствует / Замечание» в один тап"]),
    "s-remark": ("Новое замечание", "Фото, категория, критичность и описание.", ["Привязка к пункту чек-листа", "Сохранение на устройстве без сети"]),
    "s-sync": ("Синхронизация", "Видно, что и сколько ждёт отправки.", ["Очередь с размерами файлов", "Фото только по Wi-Fi"]),
}
ORDER_BUY = ["s-login", "s-reg", "s-home", "s-cat", "s-filters", "s-prod", "s-cart", "s-checkout", "s-success", "s-cart-empty",
             "s-orders", "s-order", "s-issue", "s-chat", "s-notif", "s-fin", "s-profile", "s-news"]
ORDER_INSP = ["s-insp", "s-insp-run", "s-remark", "s-sync"]
lst = '<div class="grp">Покупатель</div>' + "".join(f'<a href="#screen={s}" data-id="{s}">{NOTES[s][0]}</a>' for s in ORDER_BUY)
lst += '<div class="grp">Инспектор</div>' + "".join(f'<a href="#screen={s}" data-id="{s}">{NOTES[s][0]}</a>' for s in ORDER_INSP)

PAIRS = [
    ("Главная", ["source/ui-home.png", "source/wf-home.png"], "Макет: UI и вайрфрейм", "s-home",
     ["9 одинаковых блоков → блок «Требует действия» сверху", "Заявки и Заказы с одинаковыми статусами → одна сущность, 4 счётчика", "Три кнопки баланса одного веса → финансы двумя цифрами", "Дерево каталога на главной убрано, есть поиск"]),
    ("Каталог", ["source/ui-catalog.png", "store/app-1.jpg"], "Макет и живое приложение", "s-cat",
     ["Мультивыбор чекбоксами и «Выделить всё» убраны", "Цена за тонну и NPK вместо мелкого «Минимальное кол-во: 0.025»", "Количество в мешках с пересчётом в тонны"]),
    ("Карточка товара", ["source/ui-product.png", "store/app-4.jpg"], "Макет и живое приложение", "s-prod",
     ["Обрезанные табы → аккордеоны", "13 строк состава → 4 ключевых и «Все 13»", "Добавлены цена, наличие, минимальный заказ, выбор фасовки"]),
    ("Корзина", ["source/wf-cart.png"], "Вайрфрейм", "s-cart",
     ["Деление на заявки было видно только по мелкой подписи → явный баннер и отдельные кнопки", "Сноска «цены уточнит менеджер» под кнопкой → итог с НДС", "Цели нажатия 36–44 px"]),
    ("Трекинг заказа", ["store/app-2.jpg"], "Живое приложение", "s-order",
     ["12 станций с одинаковым временем → дата прибытия, текущая станция, остаток пути", "Промежуточные станции свёрнуты", "Статус заявки и 5 шагов жизненного цикла"]),
    ("Уведомления", ["store/app-3.jpg"], "Живое приложение", "s-notif",
     ["Опечатки и внутренние статусы («Новая продажа») → понятные тексты с действием", "Иконки по типу события, переход в нужный экран"]),
    ("Профиль", ["store/app-5.jpg"], "Живое приложение", "s-profile",
     ["Баланс «USD» при рублёвой сумме → раздел «Финансы» с договором и валютой", "Менеджер с кнопками связи", "Новости и обучение переехали сюда с главной"]),
    ("Вход", ["source/ui-auth.png"], "Макет", "s-login",
     ["Пустой на 2/3 экран и подписи капсом 9 px → понятный заголовок и крупные поля", "Вход по SMS и подключение компании по ИНН", "Таббар на экране входа убран"]),
]
pairs_html = ""
for title, imgs, cap, sid, pts in PAIRS:
    pairs_html += f"""<div class="ba" id="ba-{sid}"><div class="ba-head"><h3>{title}</h3><a class="link" href="#screen={sid}" data-open="{sid}">Открыть в прототипе →</a></div>
<div class="ba-grid"><div class="ba-col"><small style="color:var(--err)">Было · {cap}</small><div class="ba-old">{"".join(f'<div class="sc"><img src="{i}" alt="{title}, старая версия" loading="lazy"></div>' for i in imgs)}</div></div>
<div class="ba-col"><small style="color:var(--ok)">Стало</small><div class="ba-new" data-clone="{sid}"></div></div>
<div class="ba-col"><small style="color:var(--t3)">Что изменилось</small><ul class="ba-list">{"".join(f"<li>{p}</li>" for p in pts)}</ul></div></div></div>"""

store = "".join(SCREENS)
proto_body = f"""
<div class="eyeb">22 экрана · сквозной сценарий · всё кликабельно</div>
<h1 class="ph1">Прототипы</h1>
<p class="plead">Новая версия — живой прототип: кликабельно всё, корзина, суммы, заявки и уведомления меняются по ходу сценария от входа до отправленной заявки и отслеживания вагона. Ниже сравнение старой и новой версий по 8 экранам. Старая версия — статичные экраны из исходного макета и скриншоты живого приложения.</p>
<div class="subnav"><a href="#proto">Кликабельный прототип</a><a href="#ba">Было → стало</a></div>
<h2 class="h2s" id="proto">Кликабельный прототип</h2>
<div class="pv"><nav class="pv-list">{lst}</nav><div class="phone"><div class="phone-in" id="phone"></div></div>
<div class="pv-note"><div class="eyeb" id="pv-num"></div><h3 id="pv-t"></h3><p class="lead2" id="pv-l"></p><ul id="pv-u"></ul>
<div class="nav2"><span class="btn m sec" id="pv-prev">{svg("back", 18)}<span class="lbl">Назад</span></span><span class="btn m blue" id="pv-next"><span class="lbl">Следующий экран</span>{svg("chev", 18)}</span></div>
<div class="pv-path"><b>Сквозной сценарий</b><ol><li>Вход → «Войти»</li><li>Главная → «Подтвердить» график по заявке № 1567</li><li>Каталог → «В корзину», степперы, фильтры, поиск</li><li>Корзина → «Оформить заявку 1» → станция, период</li><li>«Отправить заявку» → новая заявка первой в списке «Заявки»</li><li>Заявка № 1489 → вкладки, вагоны, «Проблема», чат</li><li>Инспектор: «Демо: войти как инспектор» на экране входа → чек-лист → замечание → синхронизация</li></ol></div><p class="hint">Кликабельно всё: кнопки, карточки, чипсы, поля, степперы, таббар. Промах по пустому месту подсвечивает активные зоны, как в Figma. Состояние живое: корзина, суммы, счётчики и списки меняются по ходу сценария.</p><span class="btn s sec" id="pv-reset" style="margin-top:12px"><span class="lbl">Начать сценарий заново</span></span></div></div>
<h2 class="h2s" id="ba">Было → стало</h2>
{pairs_html}
<div id="store" hidden>{store}</div>"""

ENGINE = (ROOT / "src" / "proto-engine.js").read_text(encoding="utf-8")
proto_js = "<script>const ORDER = " + json.dumps(ORDER_BUY + ORDER_INSP) + ", NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n" + ENGINE + "</script>"

# ======================= 3. UI KIT =======================
def item(code, html, pad=True, w=None):
    st = f' style="width:{w}px;max-width:100%"' if w else ""
    inner = f'<div class="kit-pad"{st}>{html}</div>' if pad else f'<div class="kit-bare"{st}>{html}</div>'
    return f'<div class="kit-item">{inner}<code>{code}</code></div>'

def sec(sid, title, sub, body):
    return f'<section class="kit-sec" id="{sid}"><h2>{title}</h2><p>{sub}</p>{body}</section>'

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

tab_buyer = re.search(r'<nav class="tab">.*?</nav>', screen("s-home"), re.S).group(0)
tab_insp = re.search(r'<nav class="tab">.*?</nav>', screen("s-insp"), re.S).group(0)
L = lambda t: f'<span class="lbl">{t}</span>'
kit = []
kit.append(sec("colors", "Цвета", "Палитра (Primitives) и семантические токены (Tokens). Семантика ссылается на палитру.",
    '<div class="ds-grid" style="grid-template-columns:repeat(auto-fill,minmax(120px,1fr))">' +
    "".join(f'<div class="ds-sw"><div style="background:{v["$value"]}"></div><p><b>{"/".join(p)}</b>{v["$value"]}</p></div>' for p, v in leaves(T["primitive"]["color"])) +
    '</div><h3 class="h3s">Семантика</h3><div class="ds-grid" style="grid-template-columns:repeat(auto-fill,minmax(170px,1fr))">' +
    "".join(f'<div class="ds-sw"><div style="background:{res(v["$value"])}"></div><p><b>color/{p[-1]}</b>{v["$value"].strip("{}").replace("primitive.color.", "")}</p></div>' for p, v in leaves(T["semantic"]["color"])) + "</div>"))
kit.append(sec("type", "Типографика", "Onest — открытая замена фирменного Unity Sans. Для тонн и рублей используются табличные цифры.",
    "".join(f'<div class="ds-row"><code>УРАЛХИМ/{k} · {v["$value"]["fontSize"]}/{v["$value"]["lineHeight"]} · {v["$value"]["fontWeight"]}</code><span style="font:var(--font-{k})" class="num">Карбамид марки Б · 68 т · 4 352 000 ₽</span></div>' for k, v in T["typography"].items())))
kit.append(sec("grid", "Сетка, отступы, радиусы", "Экран 375, поля 16, шаг 4/8. Между секциями 20, внутри карточек 12–16.",
    '<div class="kit-row"><div style="flex:1;min-width:280px">' + "".join(f'<div class="ds-row"><code>space/{k} · {v["$value"]}</code><span style="height:14px;width:{v["$value"]};background:var(--green);border-radius:3px"></span></div>' for k, v in T["space"].items()) +
    '</div><div class="kit-row" style="margin-top:0">' + "".join(f'<div style="text-align:center"><div style="width:72px;height:72px;background:#E8E9F4;border:2px solid var(--blue);border-radius:{v["$value"]}"></div><div class="t3" style="margin-top:6px">radius/{k}<br>{v["$value"]}</div></div>' for k, v in T["radius"].items()) +
    '</div></div><div class="kit-row">' + "".join(item(f"size/{k} · {v['$value']}", f'<div style="width:{min(int(v["$value"][:-2]), 200)}px;height:{min(int(v["$value"][:-2]), 84)}px;background:#E8E9F4;border-radius:8px"></div>') for k, v in T["size"].items() if k != "screen") + "</div>"))
kit.append(sec("icons", "Иконки", f"{len(ICONS)} иконок, контур 1,8 px, сетка 24×24. Цвет наследуется от текста.",
    '<div class="ic-grid">' + "".join(f'<div>{svg(n, 24)}<code>{n}</code></div>' for n in ICONS) + "</div>"))
kit.append(sec("buttons", "Кнопки", "Размеры L 52 / M 44 / S 36. Подпись в одну строку, длинная обрезается многоточием, а паддинги остаются прежними.",
    '<div class="kit-row">' +
    item(".btn.pri", f'<div class="btn pri">{L("Основная")}</div>') + item(".btn.blue", f'<div class="btn blue">{L("Бренд")}</div>') +
    item(".btn.sec", f'<div class="btn sec">{L("Вторичная")}</div>') + item(".btn.out", f'<div class="btn out">{L("Контурная")}</div>') +
    item(".btn.white", f'<div class="btn white" style="box-shadow:0 0 0 1px var(--border)">{L("На тёмном")}</div>') + item(".btn.dis", f'<div class="btn dis">{L("Недоступна")}</div>') +
    '</div><div class="kit-row">' +
    item(".btn.m", f'<div class="btn m pri">{svg("cart", 18)}{L("M · 44")}</div>') + item(".btn.s", f'<div class="btn s pri">{svg("cart", 18)}{L("S · 36")}</div>') +
    item(".btn + icon", f'<div class="btn sec">{svg("alert", 18)}{L("Проблема")}</div>') +
    item(".btn.full + цена", f'<div class="btn pri" style="width:240px;flex-direction:column;gap:0;line-height:1.15">{L("В корзину")}<span class="num" style="font-size:13px;font-weight:500;opacity:.9">112 400 ₽</span></div>') +
    item("длинная подпись → …", f'<div class="btn pri" style="width:220px">{L("Отправить заявку · 1 426 560 ₽")}</div>') +
    item("две кнопки в ряд", f'<div class="row" style="gap:8px;width:300px"><div class="btn s pri" style="flex:1">{L("Подтвердить")}</div><div class="btn s sec" style="flex:1">{L("Посмотреть график")}</div></div>') +
    item(".fab", f'<div class="fab" style="position:static">{svg("camera", 22)}{L("Замечание")}</div>') + "</div>"))
kit.append(sec("inputs", "Поля ввода", "Высота 56, подпись над значением. Состояния: пустое, заполненное, фокус, ошибка.",
    '<div class="kit-row">' +
    item(".field.ph", '<div class="field ph" style="width:300px"><div class="fl"><small>Рабочий email</small><b>name@company.ru</b></div></div>') +
    item(".field", f'<div class="field" style="width:300px"><div class="fl"><small>Грузополучатель</small><b>ООО «АгроСнаб-Урал»</b></div><span class="chev">{svg("chev", 20)}</span></div>') +
    item("фокус", f'<div class="field" style="width:300px;border:2px solid var(--blue)"><div class="fl"><small style="color:var(--blue)">ИНН компании</small><b class="num">6658 012345</b></div><span style="color:var(--ok)">{svg("check", 22)}</span></div>') +
    item(".field.err", '<div class="stack" style="width:300px;gap:8px"><div class="field err"><div class="fl"><small style="color:var(--err)">Станция назначения</small><b class="ph" style="color:var(--t3);font-weight:400">Не выбрана</b></div></div><div class="field-err">Укажите станцию назначения</div></div>') +
    item("textarea", '<div class="field" style="width:300px;min-height:88px;align-items:flex-start"><div class="fl"><small>Комментарий</small><b style="font-weight:400">Выгрузка только в будни</b></div></div>') +
    item(".search", f'<div class="search" style="width:300px">{svg("search", 20)}Продукт, марка или NPK</div>') + "</div>"))
kit.append(sec("choice", "Выбор и количество", "Чипсы, сегменты, переключатели, флажки и степпер количества с пересчётом единиц.",
    '<div class="kit-row">' +
    item(".chip / .chip.on", f'<div class="wrap" style="width:340px"><span class="chip on">{L("Все")} <span class="n">84</span></span><span class="chip">{L("Водорастворимые")} <span class="n">23</span></span><span class="chip">{L("Азотные")}</span></div>') +
    item(".chip + icon", f'<span class="chip" style="color:var(--blue)">{svg("filter", 18)}{L("Фильтры")} <span class="pill info" style="height:18px;padding:0 6px">1</span></span>') +
    item(".seg", '<div class="seg" style="width:300px"><div class="on">Отгрузка</div><div>Состав</div><div>Документы</div></div>') +
    item(".seg + icons", f'<div class="seg" style="width:340px"><div class="on">{svg("leaf", 18)}Сельхоз</div><div>{svg("factory", 18)}Промышленное</div></div>') +
    item(".tgl", '<div class="row"><span class="tgl on"><i></i></span><span class="tgl"><i></i></span></div>') +
    item(".cbx", f'<div class="row"><span class="cbx on">{svg("check", 16)}</span><span class="cbx"></span></div>') +
    item(".stepper", f'<div class="stepper" style="width:170px"><div class="sbtn">{svg("minus", 18)}</div><div class="val"><b>40 меш.</b><small>= 1 т</small></div><div class="sbtn">{svg("plus", 18)}</div></div>') +
    item(".npk", '<div class="npk"><span><i>N</i>18</span><span><i>P₂O₅</i>18</span><span><i>K₂O</i>18</span><span><i>MgO</i>3</span></div>') + "</div>"))
kit.append(sec("status", "Статусы и прогресс", "Статус — пилюля с текстом и при необходимости иконкой, а не цветная точка.",
    '<div class="kit-row">' +
    item(".pill (5 статусов заявки)", f'<div class="wrap" style="width:360px"><span class="pill neu">{L("Согласование")}</span><span class="pill info">{L("Подтверждена")}</span><span class="pill warn">{L("Отгрузка")}</span><span class="pill ok">{L("В пути")}</span><span class="pill err">{L("Отклонена")}</span></div>') +
    item(".pill + icon", f'<div class="wrap"><span class="pill ok">{svg("check", 14)}{L("Оплачен")}</span><span class="pill warn">{svg("wifioff", 14)}{L("Офлайн")}</span></div>') +
    item(".dot-b / .tab-b", '<div class="row" style="gap:24px"><div class="icon-btn soft">' + svg("bell", 22) + '<span class="dot-b">3</span></div><div class="nrow unread card tight" style="width:120px;height:44px"></div></div>') +
    item(".prog", '<div class="prog" style="width:300px"><i style="width:64%"></i></div>') +
    item(".mini-lc", '<div class="mini-lc" style="width:300px"><i class="d"></i><i class="d"></i><i class="d"></i><i class="c"></i><i></i></div>') +
    item(".lc (жизненный цикл)", frag(screen("s-order"), '<div class="lc">'), w=360) +
    item(".tl (таймлайн)", frag(screen("s-order"), '<div class="tl">'), w=340) +
    item(".ck (чек-лист)", f'<div class="stack" style="width:320px;gap:8px"><div class="ck done">{svg("check", 16)}<span>Пломбы на месте</span></div><div class="ck">{svg("dot", 16)}<span>Отбор пробы (3 точки)</span></div></div>') + "</div>"))
kit.append(sec("cards", "Карточки", "Белая поверхность, радиус 16, внутренний отступ 12–16. Все карточки — фрагменты из макетов.",
    '<div class="kit-row">' +
    item(".pcard (каталог)", frag(screen("s-cat"), '<div class="pcard" data-go="s-prod">'), w=375) +
    item("KPI-счётчик", '<div class="card tight" style="width:160px"><div class="amount" style="font-size:24px;line-height:30px">2</div><span class="pill ok"><span class="lbl">В пути</span></span></div>') +
    item("требует действия", frag(screen("s-home"), '<div class="card stack" style="gap:14px">'), w=375) +
    item("вагон в пути", frag(screen("s-home"), '<div class="card stack" style="gap:12px" data-go="s-order">'), w=375) +
    item("ETA / тёмная карточка", frag(screen("s-order"), '<div class="card" style="background:var(--blue);color:#fff">'), w=375) +
    item("заявка в списке", frag(screen("s-orders"), '<div class="card stack" style="gap:10px" data-go="s-order">'), w=375) +
    item("уведомление", frag(screen("s-notif"), '<div class="card tight row nrow unread"'), w=375) +
    item("меню профиля", frag(screen("s-profile"), '<div class="card menu">'), w=375) + "</div>"))
kit.append(sec("banners", "Баннеры и сообщения", "Информационный, предупреждение, офлайн. Иконка слева, текст до двух строк.",
    '<div class="kit-row">' +
    item(".banner.info", f'<div class="banner info" style="width:340px"><span>{svg("info", 20)}</span><span>В корзине <b>2 заявки</b>: разные направления оформляются отдельно.</span></div>') +
    item("предупреждение", f'<div class="banner" style="width:340px;background:var(--warn-bg);color:var(--warn);font-weight:600">{svg("alert", 20)} Расхождение 1,2 т — выше нормы 0,5 %</div>') +
    item("офлайн", f'<div class="banner" style="width:340px;background:#1E2050;color:#FFD592">{svg("wifioff", 20)}<span>Нет сети · 3 изменения ждут отправки</span></div>') +
    item(".day / .bub (чат)", '<div class="stack" style="width:340px;gap:10px"><div class="day">Сегодня</div><div class="bub in">Вагон задержали на сутки, прибытие 15 ноября.<i>08:12</i></div><div class="bub out">Спасибо, переносим выгрузку.<i>08:20 ✓✓</i></div></div>') + "</div>"))
kit.append(sec("nav", "Навигация", "Статус-бар, шапки экранов, таббары покупателя и инспектора, нижняя панель действий, шторка.",
    '<div class="kit-row">' +
    item(".sb + .top (корневой экран)", SB + '<div class="top"><h1>Каталог</h1><div class="icon-btn soft">' + svg("bell", 22) + '<span class="dot-b">3</span></div></div>', pad=False, w=375) +
    item(".top (вложенный экран)", f'<div class="top" style="padding-top:14px"><div class="icon-btn soft">{svg("back", 22)}</div><div class="ttl">Заявка № 1489</div><div class="icon-btn soft">{svg("dots", 22)}</div></div>', pad=False, w=375) +
    item(".top + компания", f'<div class="top" style="padding-top:14px"><div class="company"><b>ООО «АгроСнаб-Урал» {svg("chevd", 18)}</b><span>Договор 77-П/2026 · RUB</span></div><div class="icon-btn soft">{svg("bell", 22)}</div></div>', pad=False, w=375) +
    item(".tab (покупатель)", tab_buyer, pad=False, w=375) + item(".tab (инспектор)", tab_insp, pad=False, w=375) +
    item(".dock", f'<div class="dock" style="padding-bottom:14px"><div class="btn sec" style="flex:1">{L("Проблема")}</div><div class="btn blue" style="flex:1.3">{L("Чат с менеджером")}</div></div>', pad=False, w=375) +
    item(".sheet-m (шторка)", '<div style="background:#7A7C93;padding-top:24px;width:375px"><div class="sheet-m" style="gap:14px;padding-bottom:20px"><div class="handle"></div><div class="between"><span style="font:var(--font-h1)">Фильтры</span><span class="link">Сбросить</span></div><div class="wrap"><span class="chip on"><span class="lbl">Мешок 25 кг</span></span><span class="chip"><span class="lbl">МКР 1000 кг</span></span></div></div></div>', pad=False) + "</div>"))
kit.append(sec("media", "Медиа и аватары", "Пакшоты из макета, плитки фото, аватары с инициалами, иконки-плашки.",
    '<div class="kit-row">' +
    item(".pimg", '<div class="row" style="gap:8px"><div class="pimg"><img src="assets/pack-solar-micro.png"></div><div class="pimg"><img src="assets/pack-azotofosfat.png"></div><div class="pimg" style="background:#E8E9F4;color:var(--blue);flex-direction:column;font-weight:700;font-size:15px;line-height:18px">N<span style="font-size:20px">46</span></div></div>') +
    item(".ph-t / .ph-l", f'<div class="row" style="gap:8px"><div class="ph-t">{svg("camera", 22)}<span>IMG_2041</span></div><div class="ph-t add">{svg("plus", 24)}<span>Добавить</span></div><div class="ph-l s" style="width:84px;flex:none">{svg("camera", 22)}</div></div>') +
    item(".ava", '<div class="row" style="gap:10px"><div class="ava">АУ</div><div class="ava" style="background:#fff;color:var(--blue);box-shadow:0 0 0 1px var(--border)">СЛ</div><div class="ava" style="width:40px;height:40px;font-size:14px">СЛ</div></div>') +
    item(".ico (плашки)", f'<div class="row" style="gap:8px"><div class="ico warn">{svg("clock", 22)}</div><div class="ico info">{svg("doc", 22)}</div><div class="ico ok">{svg("check", 22)}</div><div class="ico blue">{svg("train", 22)}</div><div class="mi">{svg("wallet", 20)}</div></div>') +
    item(".big-ok", f'<div class="row" style="gap:12px"><div class="big-ok">{svg("check", 44)}</div><div class="big-ok" style="background:var(--surface-2);color:var(--blue)">{svg("cart", 44)}</div></div>') + "</div>"))

toc = [("colors", "Цвета"), ("type", "Типографика"), ("grid", "Сетка"), ("icons", "Иконки"), ("buttons", "Кнопки"), ("inputs", "Поля"),
       ("choice", "Выбор"), ("status", "Статусы"), ("cards", "Карточки"), ("banners", "Баннеры и чат"), ("nav", "Навигация"), ("media", "Медиа")]
kit_body = f"""<div class="eyeb">Дизайн-система · tokens.json → CSS и переменные Figma</div>
<h1 class="ph1">UI kit</h1>
<p class="plead">Все элементы, из которых собраны 22 экрана, на тех же стилях, что и макеты: правка токена меняет и прототипы, и UI kit. Единый источник — tokens/tokens.json (W3C DTCG).</p>
<div class="kit-toc">{"".join(f'<a href="#{a}">{b}</a>' for a, b in toc)}</div>
{"".join(kit)}"""

(ROOT / "index.html").write_text(page("index.html", "Описание проекта", about), encoding="utf-8")
(ROOT / "prototip.html").write_text(page("prototip.html", "Прототипы", proto_body, proto_js), encoding="utf-8")
(ROOT / "ui-kit.html").write_text(page("ui-kit.html", "UI kit", kit_body), encoding="utf-8")
missing = set(NOTES) ^ {re.search(r'id="([\w-]+)"', s).group(1) for s in SCREENS}
print("index.html, prototip.html, ui-kit.html;", len(SCREENS), "screens; notes mismatch:", missing or "none")
