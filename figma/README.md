# Перенос в Figma

Starter-план Figma: **6 вызовов MCP в месяц, судя по всему на аккаунт, а не на команду**. 08.11.2026 квота кончилась в «Новых проектах», New2 и «Своих проектах».

Целевой файл (пустой, создан 08.11.2026): [УРАЛХИМ — ЛК партнёра · Редизайн 2026](https://www.figma.com/design/kBTlxUlUBkURN2cdjhBju6), команда «Свои проекты», первая страница `0:1`.
Есть и старый черновик в New2 (`0ZiD08orz1A578mig90EW3`) с первой версией из 9 фреймов. Его можно удалить.

## Способ А — через MCP (нужна квота: Professional или новый месяц), 3 вызова
1. `html_to_figma` fileKey `kBTlxUlUBkURN2cdjhBju6`, nodeId `0:1`, cssSelector из строки 2 таблицы ниже.
2. `html_to_figma` — то же для строки 3.
3. `python -I src/figma_compose.py '{"cover":"<id>","ds":"<id>","screens":[22 id по порядку HTML]}'` → `use_figma` с содержимым `figma/run.js`. Один вызов делает раскладку («Кейс» + «Прототипы»), прототип, переменные и стили, в конце снимает скриншот. Скрипт прогнан на имитации API, все фазы проходят.

## Способ Б — без MCP, вручную (лимитов нет) → **[figma-plugin/ИНСТРУКЦИЯ.md](../figma-plugin/ИНСТРУКЦИЯ.md)**
Локальный плагин `figma-plugin/` делает раскладку, переменные, стили и прототип одной командой. Ниже — старый вариант через Scripter.
1. **Макеты:** открыть `http://localhost:5178/prototypes.html` и захватить страницу в Figma расширением [Figma для Chrome](https://help.figma.com/hc/en-us/articles/9067379354135-Figma-Chrome-extension) или плагином html.to.design. Захватывать лучше по одному экрану через `#only=<id>`: `#only=cover`, `#only=ds`, `#only=s-home` и т. д.
2. **Переменные и стили:** в Figma запустить плагин **Scripter**, вставить `figma/variables.js` и выполнить на странице с экранами.
3. **Прототип:** там же через Scripter выполнить `figma/prototype.js`, подставив в `SCREEN_IDS` id экранов (выделить экраны и выполнить `figma.currentPage.selection.map(n=>n.id)`).
4. Запасной вариант: PNG из `export/` (картинки) и `tokens/tokens.json` через плагин Tokens Studio.

## Старый план (для справки)

## Подготовка (локально, без Figma)
```bash
python -I src/tokens.py        # tokens.json → tokens/tokens.css + figma/variables.js
python -I src/build.py         # prototypes.html
python -I src/figma_links.py   # figma/prototype.js (связи прототипа)
python -I src/build.py --inline <scratch>/figma.html   # версия с картинками в base64
```

## Вызовы
| # | Инструмент | Что делает |
|---|---|---|
| 1 | `create_session` | fileKey `0ZiD08orz1A578mig90EW3` |
| 2 | `html_to_figma` | cssSelector `#cover, #ds, #s-home, #s-cat, #s-prod, #s-cart, #s-checkout, #s-order, #s-fin, #s-insp, #s-login, #s-reg, #s-notif, #s-orders, #s-profile, #s-filters, #s-success, #s-cart-empty, #s-chat, #s-issue` — 20 фреймов (лимит 20 за вызов) |
| 3 | `html_to_figma` | cssSelector `#s-news, #s-insp-run, #s-remark, #s-sync` — оставшиеся 4 экрана |
| 4 | `use_figma` | удалить старые 1:2…9:2; страница «Кейс» = обложка + дизайн-система; страница «Прототипы» = секция с 22 экранами в 2 ряда (покупатель 01–07 и 09–19, инспектор 08 и 20–22); затем **содержимое `figma/variables.js`** на странице «Прототипы»: коллекции Primitives / Tokens / Dimensions, 10 текстовых стилей УРАЛХИМ/*, привязка заливок, обводок, радиусов и текста к переменным |
| 5 | `use_figma` | содержимое `figma/prototype.js` с подставленным `SCREEN_IDS` (22 id экранов в порядке HTML): имена фреймов, 375×812 со скроллом, ON_CLICK → Navigate/Back, стартовая точка «Прототип УРАЛХИМ» |

Порядок id в `SCREEN_IDS` = порядок секций в `prototypes.html`: 01–08, затем 09–22.

## Что получится в Figma
- **Переменные**: 27 примитивов, 29 семантических токенов (алиасы на примитивы, режим Light), space/radius/size; скоупы выставлены (тексты — только TEXT_FILL, обводки — STROKE_COLOR).
- **Текстовые стили**: УРАЛХИМ/display, h1, h2, title, title-s, body, body-s, caption, label, tab — шрифт Onest.
- **Макеты**: обложка кейса, лист дизайн-системы, 22 экрана: 18 покупателя и 4 инспектора.
- **Прототип**: ~108 переходов (3 иконочные кнопки без подписи — вручную), Present с экрана «Вход».

## Ограничения
- html_to_figma даёт плоские слои, не компоненты; таббар при скролле длинных экранов уезжает вместе с контентом (закрепить вручную: Fix position when scrolling).
- Если квоты нет — альтернатива без MCP: перетащить `export/*.png` в Figma (картинки, не слои); переменные — импорт `tokens/tokens.json` плагином Tokens Studio / Variables Import.
