"""Build the Chung & Rea concept site (no dependencies apart from opencc for 简体).

    python3 _build/pages.py && python3 _build/fonts.py

English at /, Traditional Chinese (Hong Kong wording) at /zh/, Simplified at /sc/.
Every string is written as L(english, traditional). Simplified is converted from the
traditional text with OpenCC (hk2s); pass a third argument to L() to override it.
"""
import json
import os

try:
    import opencc
    _HK2S = opencc.OpenCC("hk2s")
except ImportError:  # pip install opencc-python-reimplemented
    raise SystemExit("pip install opencc-python-reimplemented")

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
V = "1"  # cache-bust: bump on every CSS/JS change

LANG = "en"


def L(en, zh, sc=None):
    if LANG == "en":
        return en
    if LANG == "zh":
        return zh
    if sc is not None:
        return sc
    out = _HK2S.convert(zh)
    for a, b in SC_WORDS:
        out = out.replace(a, b)
    return out


# Mainland wording where hk2s keeps Hong Kong terms
SC_WORDS = [("选单", "菜单"), ("私隐", "隐私"), ("泊车", "停车"), ("电邮程式", "邮件程序"), ("程式", "程序"), ("电邮", "邮件"), ("资讯专员办公室", "信息专员办公室"), ("萤幕", "屏幕"), ("登记", "登记")]


# ------------------------------------------------------------------ facts (sources in README)
PHONE = "0141 248 2204"
TEL = "+441412482204"
FAX = "0141 248 2527"
EMAIL = "info@chungrea.com"
OFFICIAL = "https://chungrea.com/"
SLAB = "https://slab.org.uk/solicitor-finder/ccmc-limited-t-a-chung-and-rea-solicitors"
SLAB_EST = "https://www.slab.org.uk/guidance/eligibility-estimators/"
UXC = "https://ux-circles.com/professionals"
BASE = "https://uxcircles.github.io/chungrea/"
HOME = [-4.2691408, 55.8585039]  # The Pentagon Centre, 36 Washington Street (OpenStreetMap)
ROUTES = json.load(open(os.path.join(BUILD, "routes.json")))

LANGS = [("en", "", "English", "en-GB"), ("zh", "zh/", "繁體", "zh-Hant-HK"), ("sc", "sc/", "简体", "zh-Hans")]
HTML_LANG = {"en": "en-GB", "zh": "zh-Hant-HK", "sc": "zh-Hans"}


def pent(cls="pent", label=None):
    """The signature: a pentagon, from the Pentagon Centre the office sits in."""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 100 96" {aria}><path d="M50 3 97 37 79 93H21L3 37Z"/></svg>'


def address():
    return L("322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ",
             "Glasgow G3 8AZ，36 Washington Street，Pentagon Centre 322A 室")


# ------------------------------------------------------------------ shared pieces
def head(prefix, slug, title, desc):
    alts = "".join(
        f'<link rel="alternate" hreflang="{h}" href="{BASE}{d}{slug if slug != "index.html" else ""}">\n'
        for _, d, _, h in LANGS
    )
    zh_pre = ""
    if LANG in ("zh", "sc"):
        s = "tc" if LANG == "zh" else "sc"
        zh_pre = (f'<link rel="preload" href="{prefix}assets/fonts/noto-serif-{s}-700.woff2" as="font" type="font/woff2" crossorigin>\n')
    return f'''<!doctype html>
<html lang="{HTML_LANG[LANG]}" class="l-{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
{alts}<link rel="alternate" hreflang="x-default" href="{BASE}{slug if slug != "index.html" else ""}">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#1f2a8f">
<link rel="preload" href="{prefix}assets/fonts/young-serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefix}assets/fonts/schibsted-grotesk.woff2" as="font" type="font/woff2" crossorigin>
{zh_pre}<link rel="stylesheet" href="{prefix}assets/site.css?v={V}">
<script defer src="{prefix}assets/site.js?v={V}"></script>
</head>
'''


def nav_items():
    return [
        ("services.html", L("What we handle", "服務範圍")),
        ("index.html#legal-aid", L("Legal aid", "法律援助")),
        ("contact.html", L("Visit &amp; contact", "到訪及聯絡")),
    ]


def lang_links(prefix, slug, cls):
    target = "" if slug == "index.html" else slug
    out = []
    for code, d, label, h in LANGS:
        cur = ' aria-current="true"' if code == LANG else ""
        out.append(f'<a href="{prefix}{d}{target}" lang="{h}" hreflang="{h}"{cur}>{label}</a>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


def header(prefix, pg, slug):
    links = "".join(
        f'<a href="{pg}{h}"{" aria-current=page" if h == slug else ""}>{t}</a>' for h, t in nav_items()
    )
    return f'''<body>
<a class="skip" href="#main">{L("Skip to content", "跳至內容")}</a>
<div class="concept-bar" role="note">
  <div class="wrap concept-in">
    <p><span class="concept-tag">{L("Concept", "概念")}</span><span>{L('Redesign concept. Not the <a href="' + OFFICIAL + '" target="_blank" rel="noopener">official Chung &amp; Rea website</a>.', '重新設計概念，並非 <a href="' + OFFICIAL + '" target="_blank" rel="noopener">Chung &amp; Rea 官方網站</a>。')}</span></p>
    <a href="{UXC}" target="_blank" rel="noopener">{L("Designed by", "設計")} <strong>UX CIRCLES</strong> ↗</a>
  </div>
</div>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{pg}index.html">
      {pent("brand-mark")}
      <span class="brand-name">Chung <span class="amp">&amp;</span> Rea</span>
      <span class="brand-sub">{L("Solicitors &amp; Notaries Public", "律師及公證人")}</span>
    </a>
    <nav class="nav" aria-label="{L('Main', '主選單')}">{links}</nav>
    {lang_links(prefix, slug, "langs")}
    <a class="head-call" href="tel:{TEL}"><span class="sr">{L("Call", "致電")} </span>{PHONE}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{L("Menu", "選單")}</button>
  </div>
  <div class="menu" id="menu" hidden>
    <nav class="wrap" aria-label="{L('Menu', '選單')}">
      {links}
      <a href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      {lang_links(prefix, slug, "menu-langs")}
    </nav>
  </div>
</header>
<main id="main">
'''


def footer(prefix, pg, slug):
    return f'''</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <p class="foot-name">{pent("foot-mark")} Chung &amp; Rea</p>
      <p>{L("Solicitors &amp; Notaries Public", "律師及公證人")}<br>{address()}</p>
      <p><a href="tel:{TEL}">{PHONE}</a> · {L("Fax", "傳真")} {FAX}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <p>{L("Chung &amp; Rea is the trading name of CCMC Limited, registered in Scotland, company number SC534437. Registered office: 322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ.",
            "Chung &amp; Rea 為 CCMC Limited 的營業名稱。公司於蘇格蘭註冊，編號 SC534437。註冊辦事處：322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ。")}</p>
      <p>{L('Registered with the <a href="' + SLAB + '" target="_blank" rel="noopener">Scottish Legal Aid Board</a> for civil legal aid.',
            '已在<a href="' + SLAB + '" target="_blank" rel="noopener">蘇格蘭法律援助委員會</a>登記，可處理民事法律援助個案。')}</p>
    </div>
    <div class="foot-links">
      <a href="{pg}services.html">{L("What we handle", "服務範圍")}</a>
      <a href="{pg}contact.html">{L("Visit &amp; contact", "到訪及聯絡")}</a>
      <a href="{pg}privacy.html">{L("Privacy notice", "私隱聲明")}</a>
      <a href="{pg}accessibility.html">{L("Accessibility", "無障礙聲明")}</a>
      {lang_links(prefix, slug, "foot-langs")}
    </div>
  </div>
  <div class="wrap foot-concept">
    <p>{L('Unofficial redesign concept by <a href="' + UXC + '" target="_blank" rel="noopener">UX CIRCLES</a>. Information on this page is general and is not legal advice.',
          '非官方重新設計概念，由 <a href="' + UXC + '" target="_blank" rel="noopener">UX CIRCLES</a> 製作。本網站內容只屬一般資料，並非法律意見。')}</p>
  </div>
</footer>
<nav class="mbar" aria-label="{L('Quick actions', '快速聯絡')}">
  <a href="tel:{TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>{L("Call", "致電")}</a>
  <a href="mailto:{EMAIL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v12H3zM3 7l9 6 9-6"/></svg>{L("Email", "電郵")}</a>
  <a href="{pg}contact.html#book" class="mbar-main">{pent("mbar-pent")}{L("Book a meeting", "預約會面")}</a>
</nav>
</body>
</html>
'''


# ------------------------------------------------------------------ the letter (hero object)
def letter():
    return f'''<div class="letter" id="letter">
  <div class="letter-top">
    <p class="letter-from">{L("Worksheet", "工作紙")} · Chung &amp; Rea</p>
    <svg class="letter-stamp" viewBox="0 0 100 96" role="img" aria-label="{L("Chung and Rea stamp", "Chung &amp; Rea 印章")}"><path d="M50 3 97 37 79 93H21L3 37Z"/><text x="50" y="58" text-anchor="middle">C&amp;R</text><text x="50" y="76" text-anchor="middle" class="st-s">GLASGOW</text></svg>
  </div>
  <h2 class="letter-title">{L("Your refusal letter, in three lines", "你的拒絕信，三行看清楚")}</h2>
  <form class="letter-form" novalidate>
    <div class="ln">
      <label for="d-date"><span class="no">1</span>{L("Date the decision was sent", "決定的寄出日期")}</label>
      <input type="date" id="d-date" name="date" required>
    </div>
    <fieldset class="ln">
      <legend><span class="no">2</span>{L("Where are you now?", "你現在身在何處？")}</legend>
      <div class="seg">
        <label><input type="radio" name="where" value="14" checked><span>{L("In the UK", "在英國")}</span></label>
        <label><input type="radio" name="where" value="28"><span>{L("Outside the UK", "在英國境外")}</span></label>
      </div>
    </fieldset>
    <div class="ln ln-out" aria-live="polite">
      <p class="out-label"><span class="no">3</span>{L("Appeal form usually due by", "上訴表格一般須於此日前送達")}</p>
      <p class="out" id="d-out"><span class="out-empty">{L("Enter the date above", "請先輸入上方日期")}</span></p>
      <p class="out-note" id="d-note"></p>
    </div>
  </form>
  <p class="letter-small">{L("An estimate, not legal advice. Your letter states whether you have a right of appeal and the exact time limit; some decisions are certified with no appeal. If you are close to or past the date, call today.",
                            "這只是估算，並非法律意見。你的信會列明有沒有上訴權及確實期限；部分決定被核證為不可上訴。如果期限將至或已過，請今天就致電。")}</p>
  <div class="letter-act">
    <a class="btn btn-ink" href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a>
    <a class="btn btn-line" href="contact.html#book" id="letter-book">{L("Book a meeting", "預約會面")}</a>
  </div>
</div>'''


def SERVICES():
    return [
    ("asylum", L("Asylum", "庇護申請"),
     L("Claims for protection, screening and substantive interviews, fresh claims, and appeals to the First-tier Tribunal.",
       "保護申請、篩選面談及實質面談、新申請（fresh claim），以及向初級審裁處提出上訴。")),
    ("immigration", L("Immigration", "移民"),
     L("Family visas, leave to remain, settlement and citizenship applications, and refusals that need a second look.",
       "家庭簽證、居留許可、永久居留及入籍申請，以及需要重新審視的拒簽個案。")),
    ("deportation", L("Deportation", "遞解出境"),
     L("Deportation and removal decisions, detention and bail, and the human rights arguments that can stop removal.",
       "遞解及遣送決定、羈留與保釋，以及可阻止遣送的人權理據。")),
    ("judicial-review", L("Judicial review", "司法覆核"),
     L("Challenging Home Office decisions in the Court of Session. In Scotland the petition normally has to be lodged within three months.",
       "於蘇格蘭最高民事法院（Court of Session）挑戰內政部的決定。在蘇格蘭，呈請一般須於三個月內提交。")),
    ("personal-injury", L("Personal injury", "人身傷害"),
     L("Claims for injuries at work, on the road or in public places.", "工作、道路交通或公眾地方受傷的索償。")),
    ("notary", L("Notary public", "公證服務"),
     L("Certified copies, affidavits and witnessed signatures for documents that will be used abroad.",
       "為將在海外使用的文件辦理核證副本、誓章及見證簽署。")),
]


def services_ledger(pg, full=False):
    rows = []
    for i, (sid, name, text) in enumerate(SERVICES(), 1):
        more = f'<a class="row-link" href="{pg}services.html#{sid}" aria-label="{name}: {L("more", "更多")}">→</a>' if not full else ""
        rows.append(f'<li id="{sid if full else "s-" + sid}"><span class="row-no">{i:02d}</span><h3>{name}</h3><p>{text}</p>{more}</li>')
    return '<ol class="ledger">' + "".join(rows) + "</ol>"


def map_block(prefix):
    data = {
        "home": HOME,
        "mark": prefix + "assets/img/pin.svg",
        "label": "Chung &amp; Rea",
        "routes": [
            {"name": L(n, {"Anderston": "Anderston 站", "Glasgow Central": "Glasgow Central 中央車站"}[n]),
             "short": L({"Anderston": "Anderston", "Glasgow Central": "Central"}[n], {"Anderston": "Anderston", "Glasgow Central": "中央車站"}[n]), "min": r["min"], "start": r["start"], "coords": r["coords"]}
            for n, r in ROUTES.items()
        ],
    }
    a, c = ROUTES["Anderston"]["min"], ROUTES["Glasgow Central"]["min"]
    return f'''<div class="map" data-map>
  <img class="map-fallback" src="{prefix}assets/img/map-sketch.svg" alt="{L("Sketch map: the office on Washington Street, a short walk from Anderston station and Glasgow Central", "簡圖：辦事處位於 Washington Street，鄰近 Anderston 站及 Glasgow Central 中央車站")}" width="800" height="560" loading="lazy">
</div>
<script type="application/json" id="map-data">{json.dumps(data, ensure_ascii=False)}</script>
<ul class="walks">
  <li><strong>{a} {L("min", "分鐘")}</strong> {L("walk from Anderston station (Argyle Line)", "由 Anderston 火車站（Argyle 線）步行")}</li>
  <li><strong>{c} {L("min", "分鐘")}</strong> {L("walk from Glasgow Central", "由 Glasgow Central 中央車站步行")}</li>
</ul>'''


def booking_form():
    return f'''<form class="book" id="book-form" novalidate>
  <div class="f-row">
    <label for="f-name">{L("Your name", "姓名")}</label>
    <input id="f-name" name="name" autocomplete="name" required>
  </div>
  <div class="f-row">
    <label for="f-phone">{L("Phone", "電話")}</label>
    <input id="f-phone" name="phone" type="tel" autocomplete="tel" required>
  </div>
  <div class="f-row">
    <label for="f-topic">{L("What is it about?", "事項")}</label>
    <select id="f-topic" name="topic">
      {"".join(f"<option>{name}</option>" for _, name, _ in SERVICES())}
      <option>{L("Not sure", "不確定")}</option>
    </select>
  </div>
  <div class="f-row">
    <label for="f-lang">{L("Language for the meeting", "會面語言")}</label>
    <select id="f-lang" name="lang">
      <option>English</option><option>{L("Cantonese", "廣東話")}</option><option>{L("Mandarin", "普通話")}</option>
    </select>
  </div>
  <div class="f-row f-wide">
    <label for="f-deadline">{L("Deadline on your letter, if any", "信上的期限（如有）")}</label>
    <input id="f-deadline" name="deadline" type="date">
  </div>
  <div class="f-row f-wide">
    <label for="f-msg">{L("Anything we should know (optional)", "其他補充（可選填）")}</label>
    <textarea id="f-msg" name="msg" rows="4"></textarea>
  </div>
  <p class="f-err" id="f-err" role="alert" hidden>{L("Please add your name and a phone number.", "請填寫姓名及電話。")}</p>
  <button class="btn btn-ink" type="submit">{L("Open email to send", "開啟電郵發送")}</button>
  <p class="f-note">{L("This opens your email app with your answers filled in. Nothing is stored on this website.", "按下後會開啟你的電郵程式並填好內容。本網站不會儲存任何資料。")}</p>
</form>'''


# ------------------------------------------------------------------ pages
def page_home(prefix, pg):
    return f'''
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-words">
      <h1>{L("Bring the letter to Washington Street", "收到內政部的信，帶來 Washington Street 給我們看")}</h1>
      <p class="lede">{L("Asylum, immigration, deportation and judicial review solicitors in Glasgow city centre. Legal aid for those who qualify, and a solicitor who can talk it through in English, Cantonese or Mandarin.",
                         "格拉斯哥市中心的庇護、移民、遞解出境及司法覆核律師。合資格者可申請法律援助，並可用英語、廣東話或普通話與律師詳談。")}</p>
      <p class="hero-phone"><a href="tel:{TEL}">{PHONE}</a><span>{L("3 minutes from Anderston station", "距 Anderston 站步行 3 分鐘")}</span></p>
    </div>
    {letter()}
  </div>
</section>

<section class="sec" id="work">
  <div class="wrap">
    <div class="sec-head">
      <h2>{L("What we handle", "我們處理的事務")}</h2>
      <a class="more" href="{pg}services.html">{L("All services", "全部服務")} →</a>
    </div>
    {services_ledger(pg)}
  </div>
</section>

<section class="sec sec-blue" id="legal-aid">
  <div class="wrap aid">
    <div>
      <h2>{L("Legal aid covers immigration and asylum work in Scotland", "在蘇格蘭，移民及庇護事務可獲法律援助")}</h2>
      <p>{L("We are registered with the Scottish Legal Aid Board, and immigration, asylum and nationality is one of the case types we take on under legal aid. Whether you qualify depends on your income and savings, and for some work on the merits of the case. We check this with you at the first meeting.",
            "本所已在蘇格蘭法律援助委員會（SLAB）登記，移民、庇護及國籍個案是我們以法律援助承辦的類別之一。是否合資格取決於你的收入及儲蓄，部分工作亦視乎案情。我們會在首次會面時與你一同核實。")}</p>
      <p class="aid-links"><a href="{SLAB}" target="_blank" rel="noopener">{L("Our entry on the SLAB solicitor finder", "SLAB 律師名錄中的本所資料")} ↗</a><a href="{SLAB_EST}" target="_blank" rel="noopener">{L("SLAB eligibility estimators", "SLAB 資格估算工具")} ↗</a></p>
    </div>
    <ul class="bring">
      <li class="bring-h">{L("Please bring", "會面時請帶備")}</li>
      <li>{L("Every letter from the Home Office or the tribunal, with envelopes", "內政部或審裁處的所有信件，連信封")}</li>
      <li>{L("Passport, BRP or other ID", "護照、BRP 或其他身份證明")}</li>
      <li>{L("Proof of income or benefits, for legal aid", "收入或福利證明（申請法律援助用）")}</li>
      <li>{L("Any earlier decisions or solicitor's letters", "以往的決定或律師信件")}</li>
    </ul>
  </div>
</section>

<section class="sec" id="languages">
  <div class="wrap tongues">
    <p class="tongue" lang="en">English</p>
    <p class="tongue" lang="zh-Hant-HK">廣東話</p>
    <p class="tongue" lang="zh-Hans">普通话</p>
    <p class="tongues-note">{L("Staff at the firm speak Cantonese and Mandarin, so you can explain your situation in your own words. Tell us when you book and we will arrange it.",
                               "本所有會說廣東話及普通話的同事，你可以用自己的語言說明情況。預約時告訴我們即可安排。")}</p>
  </div>
</section>

<section class="sec sec-stone" id="visit">
  <div class="wrap visit">
    <div>
      <h2>{L("The Pentagon Centre, by the Clyde", "Pentagon Centre，克萊德河畔")}</h2>
      <p class="addr">{address()}</p>
      <p>{L("The office is wheelchair accessible, there is parking nearby, and we can visit clients who are housebound.",
            "辦事處設有輪椅通道，附近可泊車；如你行動不便無法外出，我們可以上門探訪。")}</p>
      <p><a class="btn btn-ink" href="{pg}contact.html#book">{L("Book a meeting", "預約會面")}</a></p>
    </div>
    <div>{map_block(prefix)}</div>
  </div>
</section>
'''


def page_services(prefix, pg):
    return f'''
<section class="page-head">
  <div class="wrap">
    <h1>{L("What we handle", "我們處理的事務")}</h1>
    <p class="lede">{L("The firm's work areas, as listed on its own site and with the Scottish Legal Aid Board. Ask us if your matter is not here.",
                       "以下是本所官方網站及蘇格蘭法律援助委員會所列的業務範圍。如你的事項不在其中，歡迎查詢。")}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">{services_ledger(pg, full=True)}</div>
</section>
<section class="sec sec-blue">
  <div class="wrap times">
    <h2>{L("Time limits worth knowing", "需要留意的期限")}</h2>
    <dl>
      <div><dt>14 {L("days", "日")}</dt><dd>{L("Most in-country appeals to the First-tier Tribunal, from the date the decision was sent", "大部分在英國境內向初級審裁處提出的上訴，由決定寄出日起計")}</dd></div>
      <div><dt>28 {L("days", "日")}</dt><dd>{L("Most appeals made from outside the UK, from the date you received the decision", "大部分在英國境外提出的上訴，由收到決定日起計")}</dd></div>
      <div><dt>3 {L("months", "個月")}</dt><dd>{L("Judicial review petitions to the Court of Session, from the date the grounds arose", "向 Court of Session 提出司法覆核呈請，由理據產生之日起計")}</dd></div>
    </dl>
    <p class="small">{L("General information only. Your own letter is what counts; bring it to us.", "以上只屬一般資料，一切以你收到的信件為準，請帶來給我們看。")}</p>
  </div>
</section>
'''


def page_contact(prefix, pg):
    return f'''
<section class="page-head">
  <div class="wrap">
    <h1>{L("Visit and contact", "到訪及聯絡")}</h1>
    <p class="lede">{address()}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap contact">
    <div class="contact-ways">
      <a class="way" href="tel:{TEL}"><span>{L("Phone", "電話")}</span><strong>{PHONE}</strong></a>
      <a class="way" href="mailto:{EMAIL}"><span>{L("Email", "電郵")}</span><strong>{EMAIL}</strong></a>
      <p class="way"><span>{L("Fax", "傳真")}</span><strong>{FAX}</strong></p>
      <p class="small">{L("Appointments by arrangement. If your letter has a deadline in the next few days, say so when you call.",
                          "會面須預約。如你的信件期限只剩數天，致電時請先說明。")}</p>
    </div>
    <div id="book">
      <h2>{L("Book a meeting", "預約會面")}</h2>
      {booking_form()}
    </div>
  </div>
</section>
<section class="sec sec-stone">
  <div class="wrap visit">
    <div>
      <h2>{L("Finding the office", "如何前來")}</h2>
      <p>{L("The Pentagon Centre is on Washington Street, between Argyle Street and Broomielaw. Ask for office 322A.",
            "Pentagon Centre 位於 Washington Street，介乎 Argyle Street 與 Broomielaw 之間。請找 322A 室。")}</p>
      <p>{L("Wheelchair accessible. Parking nearby. Home visits for housebound clients.", "設輪椅通道，附近可泊車，行動不便者可安排上門。")}</p>
    </div>
    <div>{map_block(prefix)}</div>
  </div>
</section>
'''


def page_privacy(prefix, pg):
    return f'''
<section class="page-head"><div class="wrap"><h1>{L("Privacy notice", "私隱聲明")}</h1>
<p class="lede">{L("Draft for Chung &amp; Rea to review. The current website has no privacy notice.", "供 Chung &amp; Rea 審閱的草稿。現有網站並無私隱聲明。")}</p></div></section>
<section class="sec"><div class="wrap prose">
<h2>{L("Who we are", "我們是誰")}</h2>
<p>{L("CCMC Limited, trading as Chung &amp; Rea (company SC534437), 322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ, is the controller of personal information you give us.",
      "CCMC Limited（以 Chung &amp; Rea 名義經營，公司編號 SC534437），地址 322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ，是你所提供個人資料的控制者。")}</p>
<h2>{L("What this website collects", "本網站收集甚麼資料")}</h2>
<p>{L("Nothing. The booking form opens your own email app; we only receive what you choose to send. The site sets no cookies and uses no analytics. The map loads tiles from OpenFreeMap when you scroll to it.",
      "沒有。預約表格只會開啟你自己的電郵程式，我們只會收到你選擇發送的內容。本網站不使用 Cookie 或分析工具。地圖在你捲動到該處時才會從 OpenFreeMap 載入。")}</p>
<h2>{L("When you instruct us", "委託我們之後")}</h2>
<p>{L("We use your information to give legal advice and act for you, to apply for legal aid, and to meet our legal and regulatory duties. This can include special category data such as health, religion or ethnicity where your case needs it. We share it only as your case requires: for example with the Home Office, the tribunal or courts, the Scottish Legal Aid Board, interpreters and counsel.",
      "我們使用你的資料提供法律意見、代表你行事、申請法律援助，以及履行法律和監管責任。如案件需要，可能包括健康、宗教或種族等特殊類別資料。我們只會按案件需要分享，例如給內政部、審裁處或法院、蘇格蘭法律援助委員會、傳譯員及大律師。")}</p>
<h2>{L("Your rights", "你的權利")}</h2>
<p>{L('You can ask for a copy of your information, ask us to correct it, and in some cases ask us to delete or restrict it. Write to <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>. You can also complain to the Information Commissioner\'s Office at ico.org.uk.',
      '你可以要求取得資料副本、要求更正，並在某些情況下要求刪除或限制使用。請電郵 <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>。你亦可向資訊專員辦公室（ico.org.uk）投訴。')}</p>
</div></section>
'''


def page_access(prefix, pg):
    return f'''
<section class="page-head"><div class="wrap"><h1>{L("Accessibility", "無障礙聲明")}</h1></div></section>
<section class="sec"><div class="wrap prose">
<p>{L("This concept is built to WCAG 2.2 AA: it works with a keyboard and screen readers, text can be enlarged to 200%, colours meet contrast guidelines, and motion is reduced if your device asks for it.",
      "此概念網站按 WCAG 2.2 AA 標準製作：可用鍵盤及屏幕閱讀器操作，文字可放大至 200%，顏色符合對比度要求，並會按你裝置的設定減少動畫。")}</p>
<p>{L("The office is wheelchair accessible and there is parking nearby. There is no induction loop. Home visits are available for clients who are housebound.",
      "辦事處設有輪椅通道，附近可泊車，但未設感應環路系統。行動不便無法外出的客戶可安排上門探訪。")}</p>
<p>{L(f'If something does not work for you, call <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.',
      f'如有任何不便，請致電 <a href="tel:{TEL}">{PHONE}</a> 或電郵 <a href="mailto:{EMAIL}">{EMAIL}</a>。')}</p>
</div></section>
'''


def page_404(prefix, pg):
    return f'''
<section class="lost">
  <div class="wrap">
    {pent("lost-pent")}
    <h1>{L("This page is not on file", "找不到這一頁")}</h1>
    <p class="lede">{L("The link may be old. The phone still works:", "連結可能已失效，但電話仍然可以打通：")} <a href="tel:{TEL}">{PHONE}</a></p>
    <p><a class="btn btn-ink" href="{pg}index.html">{L("Back to the home page", "返回首頁")}</a></p>
  </div>
</section>
'''


PAGES = [
    ("index.html", page_home,
     lambda: L("Chung &amp; Rea · Immigration and asylum solicitors, Glasgow", "Chung &amp; Rea · 格拉斯哥移民及庇護律師"),
     lambda: L("Asylum, immigration, deportation and judicial review solicitors in Glasgow city centre. Legal aid. English, Cantonese and Mandarin.",
               "格拉斯哥市中心的庇護、移民、遞解出境及司法覆核律師。可申請法律援助。英語、廣東話、普通話。")),
    ("services.html", page_services, lambda: L("What we handle · Chung &amp; Rea", "服務範圍 · Chung &amp; Rea"),
     lambda: L("Asylum, immigration, deportation, judicial review, personal injury and notary services in Glasgow.", "格拉斯哥的庇護、移民、遞解出境、司法覆核、人身傷害及公證服務。")),
    ("contact.html", page_contact, lambda: L("Visit and contact · Chung &amp; Rea", "到訪及聯絡 · Chung &amp; Rea"),
     lambda: L("322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ. Call 0141 248 2204.", "322A Pentagon Centre, 36 Washington Street, Glasgow G3 8AZ。電話 0141 248 2204。")),
    ("privacy.html", page_privacy, lambda: L("Privacy notice · Chung &amp; Rea", "私隱聲明 · Chung &amp; Rea"), lambda: L("Privacy notice.", "私隱聲明。")),
    ("accessibility.html", page_access, lambda: L("Accessibility · Chung &amp; Rea", "無障礙聲明 · Chung &amp; Rea"), lambda: L("Accessibility statement.", "無障礙聲明。")),
]


def build():
    global LANG
    for code, d, _, _ in LANGS:
        LANG = code
        prefix = "../" if d else ""
        for slug, fn, title, desc in PAGES:
            out = head(prefix, slug, title(), desc()) + header(prefix, "", slug) + fn(prefix, "") + footer(prefix, "", slug)
            os.makedirs(os.path.join(ROOT, d), exist_ok=True)
            open(os.path.join(ROOT, d, slug), "w", encoding="utf-8").write(out)
    # 404: GitHub Pages serves it from any path, so use absolute links
    LANG = "en"
    abs_ = "/chungrea/"
    out = head(abs_, "404.html", "Page not found · Chung &amp; Rea", "Page not found.") + header(abs_, abs_, "404.html") + page_404(abs_, abs_) + footer(abs_, abs_, "404.html")
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(out)
    print("built")


if __name__ == "__main__":
    build()
