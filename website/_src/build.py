"""Builds the FDSC static website from content.py.

Run:  python3 website/_src/build.py
Writes index.html, about.html, services.html, work.html, contact.html, 404.html, sitemap.xml, robots.txt
and copies brand files into website/assets/brand/. Upload everything in website/ except _src/.
"""
import html
import json
import os
import shutil
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
ROOT = os.path.dirname(SITE)
sys.path.insert(0, HERE)
import content as C  # noqa: E402
from shared import icon, dot_map  # noqa: E402

F = C.FIRM
IMG = os.path.join(SITE, "assets", "img")
VER = "3"  # bump to bust caches of css/js
PDF = "assets/docs/FDSC-Company-Profile-2026.pdf"
NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("work.html", "Our work"), ("contact.html", "Contact")]
e = html.escape


# ---- helpers -------------------------------------------------------------------------------
def pic(slug, alt, sizes="(max-width: 700px) 100vw, 50vw", cls="", eager=False, base=""):
    w, h = Image.open(os.path.join(IMG, f"{slug}-1600.webp")).size
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{base}assets/img/{slug}-1600.webp" srcset="{base}assets/img/{slug}-800.webp 800w, '
            f'{base}assets/img/{slug}-1600.webp 1600w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def head(title, desc, path, base=""):
    url = F["url"] + "/" + ("" if path == "index.html" else path)
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": F["name"],
          "alternateName": "FDSC", "url": F["url"], "logo": F["url"] + "/assets/brand/fdsc-logo.svg",
          "image": F["url"] + "/assets/brand/og-image.jpg", "email": F["email"], "telephone": F["phone"],
          "foundingDate": str(F["founded"]), "description": C.INTRO,
          "address": {"@type": "PostalAddress", "streetAddress": "Victoria Noble Centre, Plot No. 89, Block 45B, Kinondoni",
                      "postOfficeBoxNumber": "105471", "addressLocality": "Dar es Salaam", "addressCountry": "TZ"},
          "areaServed": ["Tanzania", "Zanzibar", "East Africa"]}
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FDSC">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F['url']}/assets/brand/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#C23C47">
<link rel="icon" href="{base}favicon.ico" sizes="48x48">
<link rel="icon" href="{base}assets/brand/fdsc-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preload" href="{base}assets/fonts/SpaceGrotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/InstrumentSans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/fonts/fonts.css">
<link rel="stylesheet" href="{base}assets/css/site.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(path, base=""):
    links = "".join(f'<a href="{base}{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{base}{h}"{" aria-current=\"page\"" if h == path else ""}>{t}{icon("arrow")}</a>' for h, t in NAV)
    return f"""<header class="top">
  <div class="wrap top__in">
    <a class="brand" href="{base}index.html" aria-label="FDSC home"><img class="logo" src="{base}assets/brand/fdsc-wordmark.svg" width="188" height="100" alt="FDSC"></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="top__cta"><a class="btn btn--red" href="{base}contact.html">Request a proposal{icon('arrow')}</a></div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu">
      <span class="i-open">{icon('menu')}</span><span class="i-close" hidden>{icon('close')}</span></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile">
  {mlinks}
  <a class="btn btn--red" href="{base}contact.html">Request a proposal</a>
  <div class="mnav__contact">
    <a href="tel:{F['phone_href']}">{icon('phone')}{F['phone']}</a>
    <a href="mailto:{F['email']}">{icon('mail')}{F['email']}</a>
  </div>
</nav>
<main id="main">
"""


def footer(base=""):
    nav = "".join(f'<li><a href="{base}{h}">{t}</a></li>' for h, t in NAV)
    svc = "".join(f'<li><a href="{base}services.html#{s["slug"]}">{s["nav"]}</a></li>' for s in C.SERVICES[:6])
    return f"""</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot__in">
      <div>
        <img class="logo" src="{base}assets/brand/fdsc-logo-white.svg" width="226" height="120" alt="FDSC - Frontline Development Services Consulting" loading="lazy">
        <p>Pragmatic, innovative and sustainable development consulting. Dar es Salaam, Tanzania, since {F['founded']}.</p>
        <a class="foot__dl" href="{base}{PDF}" download>{icon('download')}Company profile (PDF)</a>
      </div>
      <div><h3>Explore</h3><ul>{nav}</ul></div>
      <div><h3>Services</h3><ul>{svc}</ul></div>
      <div class="foot__c"><h3>Contact</h3><ul>
        <li>{icon('pin')}<span>{F['office']}<br>{F['po_box']}</span></li>
        <li>{icon('phone')}<a href="tel:{F['phone_href']}">{F['phone']}</a></li>
        <li>{icon('mail')}<span><a href="mailto:{F['email']}">{F['email']}</a><br><a href="mailto:{F['email_alt']}">{F['email_alt']}</a></span></li>
      </ul></div>
    </div>
    <div class="foot__bar"><span>&copy; <span id="year">2026</span> {F['name']}. All rights reserved.</span><span>{F['registration']}</span></div>
  </div>
</footer>
<a class="wa" href="https://wa.me/{F['whatsapp']}" target="_blank" rel="noopener" aria-label="Chat with FDSC on WhatsApp"><img src="{base}assets/img/whatsapp-112.png" width="56" height="56" alt=""></a>
<script src="{base}assets/js/site.js?v={VER}" defer></script>
</body>
</html>
"""


def cta(base=""):
    return f"""<section class="wrap rv" aria-labelledby="cta-h">
  <div class="cta">
    {pic('tea-hills', '', sizes='100vw', base=base)}
    <div class="cta__in">
      <h2 class="h2" id="cta-h">Let&rsquo;s build lasting impact together.</h2>
      <p>Tell us about your programme, evaluation or capacity need. We reply within two working days with a first view of how we can help.</p>
      <div class="cta__btns"><a class="btn btn--white" href="{base}contact.html">Request a proposal{icon('arrow')}</a>
      <a class="btn btn--ghost-w" href="{base}{PDF}" download>{icon('download')}Company profile</a></div>
    </div>
  </div>
</section>"""


def phead(crumb, title, lead):
    return f"""<section class="phead">
  <img class="phead__mark" src="assets/brand/fdsc-mark.svg" alt="" width="420" height="480">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
    <h1 class="h1">{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""


def tzmap(cities=True):
    return dot_map(C.worked_regions(), step=9.0, dot=5.4, cls="tzmap",
                   cities=["Mwanza", "Arusha", "Kigoma", "Dodoma", "Dar es Salaam", "Mbeya"] if cities else None)


def work_card(f, base=""):
    a = f["a"]
    return f"""<article class="wcard rv">
  <div class="wcard__img">{pic(f['img'], '', sizes='(max-width: 700px) 100vw, 33vw', base=base)}<span class="wcard__tag">{f['label']}</span></div>
  <div class="wcard__b">
    <p class="wcard__meta">{e(a['client'].split(' (')[0])} &middot; {a['period'].replace(' - ', '&ndash;')}</p>
    <h3>{f['headline']}</h3>
    <p>{f['summary']}</p>
    <a class="link" href="{base}work.html#record">See the full record{icon('arrow')}</a>
  </div>
</article>"""


def stats_band():
    s = C.STATS
    return f"""<section class="wrap rv" aria-label="FDSC in numbers">
  <div class="stats">
    <div class="stat"><b>{s['years']}<small>years</small></b><span>Consulting across Tanzania since {F['founded']}</span></div>
    <div class="stat"><b>{s['assignments']}</b><span>Assignments delivered for {s['clients']} clients</span></div>
    <div class="stat"><b>{s['mainland']}<small>of 26</small></b><span>Mainland regions reached, plus Unguja and Pemba</span></div>
    <div class="stat"><b>5</b><span>Clients who have hired us again, some five times</span></div>
  </div>
</section>"""


# ---- pages ---------------------------------------------------------------------------------
def page_home():
    logos = "".join(f'<img src="assets/partners/{s}.webp" alt="{e(n)}" loading="lazy" height="44">' for s, n in C.CLIENTS)
    tabs, panes = "", ""
    sec_icons = ["leaf", "building", "people", "globe"]
    for i, s in enumerate(C.SECTORS):
        on = i == 0
        tabs += (f'<button class="tab" role="tab" id="t{i}" aria-controls="p{i}" aria-selected="{"true" if on else "false"}" '
                 f'tabindex="{0 if on else -1}"><span class="tab__ic">{icon(sec_icons[i])}</span>{s["title"]}</button>')
        panes += (f'<div class="pane" role="tabpanel" id="p{i}" aria-labelledby="t{i}"{"" if on else " hidden"}>'
                  f'{pic(s["img"], s["title"], sizes="(max-width: 1020px) 100vw, 640px", eager=False)}'
                  f'<div class="pane-txt"><h3>{s["title"]}</h3><p>{s["text"]}</p></div></div>')
    why_icons = ["clock", "building", "people", "leaf", "target", "pin", "arrow-up-right"]
    whys = "".join(f'<article class="card rv"><span class="card__ic">{icon(why_icons[i])}</span><h3>{t}</h3><p>{d}</p></article>'
                   for i, (t, d) in enumerate(C.WHY))
    svcs = "".join(f'<a class="card svc rv" href="services.html#{s["slug"]}"><div class="svc__top"><span class="card__ic card__ic--soft">{icon(s["icon"])}</span>'
                   f'<span class="num">{i + 1:02d}</span></div><h3>{s["title"]}</h3><p>{s["short"]}</p></a>' for i, s in enumerate(C.SERVICES))
    steps = "".join(f'<li><span class="ck">{i + 1}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(C.APPROACH))
    feats = "".join(work_card(f) for f in C.featured()[:3])
    s = C.STATS
    body = f"""
<section class="hero">
  <div class="wrap hero__in">
    <div>
      <p class="eyebrow">Development and management consulting in Tanzania</p>
      <h1 class="h1">Turning strategy into <span class="accent">measurable results.</span></h1>
      <p class="lead">We help government, development partners, foundations, NGOs and businesses find out what works, strengthen the people and systems behind it, and prove the results.</p>
      <div class="hero__btns"><a class="btn btn--red" href="contact.html">Request a proposal{icon('arrow')}</a><a class="btn btn--line" href="work.html">See our work</a></div>
      <p class="hero__trust">Trusted since {F['founded']} by <b>Solidaridad</b>, <b>Rikolto</b>, <b>HELVETAS</b>, <b>TNC</b> and the <b>Ministry of Finance and Planning</b>.</p>
    </div>
    <div class="mapcard">
      {tzmap()}
      <div class="chip chip--a"><span class="chip__ic">{icon('pin')}</span><div><b>{s['mainland']} of 26</b><span>mainland regions reached</span></div></div>
      <div class="chip chip--b"><span class="chip__ic chip__ic--soft">{icon('chart')}</span><div><b>{s['assignments']} assignments</b><span>delivered since {F['founded']}</span></div></div>
    </div>
  </div>
</section>

<section class="trusted" aria-label="Clients and partners">
  <p class="trusted__label">Organisations we have worked with</p>
  <div class="marquee"><div class="marquee__track">{logos}{logos.replace('alt="', 'aria-hidden="true" alt="')}</div></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split__img rv">{pic('community-meeting', 'A community meeting under a tree', sizes='(max-width: 1020px) 100vw, 45vw')}<span class="cap">Listening comes first</span></div>
    <div class="rv">
      <p class="eyebrow">About FDSC</p>
      <h2 class="h2">A Tanzanian consultancy built on <span class="accent">evidence and trust.</span></h2>
      <p class="lead" style="margin-top:20px">{C.ABOUT[1]}</p>
      <p class="quote">&ldquo;We listen first, then shape each solution around the client&rsquo;s real needs.&rdquo;</p>
      <div class="facts">
        <div><span>Founded</span><b>{F['founded']}, Dar es Salaam</b></div>
        <div><span>Clients</span><b>{s['clients']} organisations</b></div>
        <div><span>Reach</span><b>Mainland and Zanzibar</b></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="tabs rv" data-tabs>
      <div>
        <p class="eyebrow">Sectors</p>
        <h2 class="h2">Understanding the sectors that <span class="accent">shape Tanzania&rsquo;s future.</span></h2>
        <div class="tabs__list" role="tablist" aria-label="Sectors">{tabs}</div>
      </div>
      <div class="tabs__panel">{panes}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="why">
      <div class="why__intro rv">
        <p class="eyebrow">Why FDSC</p>
        <h2 class="h2">Why clients <span class="accent">choose us.</span></h2>
        <p class="lead">More than a decade of work for respected public and private organisations, local and international.</p>
      </div>
      {whys}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head rv">
      <div><p class="eyebrow">Services</p><h2 class="h2">Nine ways <span class="accent">we help.</span></h2></div>
      <p class="lead">Tailor-made, practical solutions to organisational, programme, economic and social challenges, for the public and private sectors alike.</p>
    </div>
    <div class="svc-grid">{svcs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap approach">
    <div class="rv">
      <p class="eyebrow">How we work</p>
      <h2 class="h2">Our approach for <span class="accent">results that last.</span></h2>
      <ul class="checks">{steps}</ul>
      <a class="btn btn--red" href="contact.html">Start a conversation{icon('arrow')}</a>
    </div>
    <div class="photos rv">
      <figure>{pic('tea-farmer', 'Smallholder tea farmer in Rungwe, Mbeya', sizes='(max-width: 1020px) 50vw, 25vw')}<figcaption>Value chains<span>Tea farmer, Rungwe, Mbeya</span></figcaption></figure>
      <figure>{pic('women-harvest', 'Two women carrying a harvest in Arusha', sizes='(max-width: 1020px) 50vw, 25vw')}<figcaption>Communities<span>Farmers, Arusha</span></figcaption></figure>
    </div>
  </div>
</section>

{stats_band()}

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center rv">
      <p class="eyebrow">Selected work</p>
      <h2 class="h2">Recent <span class="accent">assignments.</span></h2>
      <p class="lead">Evaluations, baselines and technical assistance for programmes across Tanzania.</p>
    </div>
    <div class="work-grid">{feats}</div>
    <p style="text-align:center;margin-top:36px"><a class="btn btn--line" href="work.html">View all {s['assignments']} assignments</a></p>
  </div>
</section>

{cta()}
"""
    return (head(f"FDSC | Development consulting in Tanzania: evaluation, research and capacity building",
                 "Frontline Development Services Consulting (FDSC) is a Tanzanian consultancy delivering evaluations, baseline studies, M&E systems, gender analysis and capacity building since 2014.",
                 "index.html") + header("index.html") + body + footer())


def page_about():
    paras = "".join(f'<p class="{"lead" if i == 0 else ""}">{t}</p>' for i, t in enumerate(C.ABOUT))
    vals = "".join(f'<li class="rv"><span class="n">{i + 1:02d}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(C.VALUES))
    reasons = "".join(f'<li class="rv"><span class="n">{i + 1:02d}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(C.WHY))
    rep = C.repeat_clients()
    mx = max(n for _, n in rep)
    bars = "".join(f'<div class="bar"><span>{c.replace(" East and Central Africa", "").replace(" Swiss Intercooperation", "")}</span>'
                   f'<span class="bar__t"><i style="width:{n / mx * 100:.0f}%"></i></span><b>{n}</b></div>' for c, n in rep)
    wall = "".join(f'<div class="rv"><img src="assets/partners/{s}.webp" alt="{e(n)}" loading="lazy"></div>' for s, n in C.CLIENTS)
    aud = "".join(f'<li>{icon("check")}{a}</li>' for a in C.AUDIENCES)
    body = f"""{phead('About', 'A Tanzanian consultancy built on <span class="accent">evidence and trust.</span>', C.INTRO)}
<section class="section">
  <div class="wrap split">
    <div class="rv">{paras}
      <div class="facts">
        <div><span>Founded</span><b>{F['founded']}, Dar es Salaam</b></div>
        <div><span>Registration</span><b>Companies Act, 2002</b></div>
        <div><span>Reach</span><b>Mainland Tanzania and Zanzibar</b></div>
      </div>
    </div>
    <div class="split__img rv">{pic('office-meeting', 'Professionals in a meeting', sizes='(max-width: 1020px) 100vw, 50vw')}</div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Purpose</p><h2 class="h2">What <span class="accent">drives us.</span></h2></div></div>
    <div class="vm">
      <div class="card rv"><span class="label">Our vision</span><p>{C.VISION}</p></div>
      <div class="card rv"><span class="label">Our mission</span><p>{C.MISSION}</p></div>
    </div>
    <h3 class="h3" style="margin:56px 0 8px">Our core values</h3>
    <ol class="values">{vals}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Why FDSC</p><h2 class="h2">Why clients <span class="accent">choose us.</span></h2></div>
      <p class="lead">Our experts attract clients who want continuing support, well beyond the contract period.</p></div>
    <ol class="reasons">{reasons}</ol>
    <div class="card rv" style="margin-top:40px;padding:32px">
      <span class="label">Clients who come back</span>
      <p class="muted" style="margin-bottom:20px">Five organisations account for {sum(n for _, n in rep)} of our {C.STATS['assignments']} assignments.</p>
      <div class="bars">{bars}</div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Who we work with</p><h2 class="h2">Clients and <span class="accent">partners.</span></h2></div>
      <ul class="checks" style="margin:0">{aud}</ul></div>
    <div class="logo-wall">{wall}</div>
    <p class="muted" style="margin-top:24px;font-size:15px">Programmes we have evaluated and supported were funded by the European Union, Irish Aid and the Belgian Development Cooperation (DGD), among others.</p>
  </div>
</section>
{cta()}
"""
    body = body.replace('<ul class="checks" style="margin:0">', '<ul class="checks aud" style="margin:0">')
    return (head("About FDSC | Frontline Development Services Consulting, Tanzania",
                 "Founded in 2014 in Dar es Salaam, FDSC provides development and management consulting to government, development partners, NGOs and business across Tanzania.",
                 "about.html") + header("about.html") + body + footer())


def page_services():
    det = ""
    for i, s in enumerate(C.SERVICES):
        pts = "".join(f"<li>{icon('check')}<span>{p}</span></li>" for p in s["points"])
        det += (f'<article class="svc-detail rv" id="{s["slug"]}"><span class="card__ic card__ic--soft">{icon(s["icon"])}</span>'
                f'<div><h3>{s["title"]}</h3><p>{s["short"]}</p></div><ul>{pts}</ul></article>')
    secs = "".join(f'<article class="sector rv">{pic(x["img"], x["title"], sizes="(max-width: 700px) 100vw, 25vw")}<div><h3>{x["title"]}</h3><p>{x["text"]}</p></div></article>' for x in C.SECTORS)
    steps = "".join(f'<li class="rv"><span class="dot">{i + 1}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(C.APPROACH))
    body = f"""{phead('Services', 'Nine ways <span class="accent">we help.</span>', 'We work with ministries, departments and agencies, companies, foundations, international and local NGOs and SMEs, designing tailor-made, innovative and sustainable solutions to organisational, programme, economic and social challenges.')}
<section class="section">
  <div class="wrap">{det}</div>
</section>
<section class="section section--tint">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Sectors</p><h2 class="h2">Sectors we know <span class="accent">from the inside.</span></h2></div>
      <p class="lead">Our work spans farms and cooperatives, ministries and agencies, and community programmes.</p></div>
    <div class="sector-grid">{secs}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">How we work</p><h2 class="h2">Four steps, <span class="accent">no surprises.</span></h2></div></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>
{cta()}
"""
    return (head("Services | FDSC: evaluation, M&E, gender, training and value chain consulting",
                 "Programme management; research, monitoring, evaluation and learning; gender; organisational development; training; data; performance management; business and agribusiness value chains.",
                 "services.html") + header("services.html") + body + footer())


def page_work():
    s = C.STATS
    by = C.by_type()
    mx = max(n for _, n in by)
    bars = "".join(f'<div class="bar"><span>{t}</span><span class="bar__t"><i style="width:{n / mx * 100:.0f}%"></i></span><b>{n}</b></div>' for t, n in by)
    feats = "".join(work_card(f) for f in C.featured())
    counts = {k: sum(1 for a in C.ASSIGNMENTS if a["type"] == k) for k in C.TYPES}
    fb = f'<button class="fbtn" type="button" data-type="all" aria-pressed="true">All<span class="c">{len(C.ASSIGNMENTS)}</span></button>'
    fb += "".join(f'<button class="fbtn" type="button" data-type="{k}" aria-pressed="false">{C.TYPES_SHORT[k]}<span class="c">{counts[k]}</span></button>' for k in C.TYPES)
    rows = ""
    for a in C.ASSIGNMENTS:
        eu = '<span class="eu">EU-funded</span>' if a.get("donor") == "EU" else ""
        rows += (f'<li class="rec" data-type="{a["type"]}"><div><span class="rec__per">{a["period"].replace(" - ", "&ndash;")}</span>'
                 f'<span class="rec__cl">{e(a["client"])}</span></div>'
                 f'<div><span class="rec__t">{e(a["title"])}</span><span class="rec__w">{e(a["where"])}{eu}</span></div>'
                 f'<div class="rec__ty"><span class="pill t-{a["type"]}">{C.TYPES_SHORT[a["type"]]}</span></div></li>')
    zones = "".join(f'<article class="card rv"><h3>{z["name"]}</h3><p style="color:var(--red-text);font-size:14px;font-weight:600;margin-bottom:8px">{z["regions"]}</p><p>{z["text"]}</p></article>' for z in C.ZONES)
    body = f"""{phead('Our work', 'From Kigoma to Kilimanjaro, <span class="accent">Mbeya to Pemba.</span>', f'{s["assignments"]} assignments since {F["founded"]}: evaluations, baseline studies, M&amp;E systems, training and technical assistance for {s["clients"]} clients.')}
<section class="section">
  <div class="wrap mapsec">
    <div class="rv">{tzmap()}
      <div class="legend"><span><i class="on"></i>Regions where we have delivered assignments</span><span><i></i>Not yet</span></div></div>
    <div class="rv">
      <p class="eyebrow">Where we work</p>
      <h2 class="h2">Nationwide <span class="accent">coverage.</span></h2>
      <div class="kpis">
        <div class="kpi"><b>{s['mainland']}<small>of 26</small></b><span>Mainland regions</span></div>
        <div class="kpi"><b>2</b><span>Islands: Unguja and Pemba</span></div>
      </div>
      <span class="label">Our work by type</span>
      <div class="bars">{bars}</div>
    </div>
  </div>
  <div class="wrap" style="margin-top:56px"><div class="why" style="grid-template-columns:repeat(4,1fr)">{zones}</div></div>
</section>
<section class="section section--tint">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Selected work</p><h2 class="h2">Programmes we have <span class="accent">measured and strengthened.</span></h2></div></div>
    <div class="work-grid">{feats}</div>
  </div>
</section>
<section class="section" id="record">
  <div class="wrap">
    <div class="section-head rv"><div><p class="eyebrow">Assignment record</p><h2 class="h2">Every assignment, <span class="accent">newest first.</span></h2></div>
      <p class="lead" id="rec-count" aria-live="polite">{len(C.ASSIGNMENTS)} assignments</p></div>
    <div class="filters" role="group" aria-label="Filter by type">{fb}
      <label class="search"><span class="sr-only">Search assignments</span>{icon('search')}<input id="q" type="search" placeholder="Search client, region, project"></label></div>
    <ul class="record" id="record-list">{rows}</ul>
    <p class="empty" id="rec-empty" hidden>No assignments match. Try another search or filter.</p>
  </div>
</section>
{cta()}
"""
    return (head("Our work | FDSC assignments across Tanzania and Zanzibar",
                 "28 evaluations, baseline studies, M&E systems, training and technical assistance assignments for Solidaridad, Rikolto, HELVETAS, TNC, the Ministry of Finance and Planning and others.",
                 "work.html") + header("work.html") + body + footer())


def page_contact():
    opts = "".join(f"<option>{s['title'][0].upper() + s['title'][1:]}</option>" for s in C.SERVICES)
    body = f"""{phead('Contact', 'Let&rsquo;s build lasting <span class="accent">impact together.</span>', 'Tell us about your programme, evaluation or capacity need. We reply within two working days.')}
<section class="section">
  <div class="wrap contact-grid">
    <div class="cinfo rv">
      <a href="tel:{F['phone_href']}"><span class="card__ic">{icon('phone')}</span><div><span>Call us</span><b>{F['phone']}</b></div></a>
      <a href="https://wa.me/{F['whatsapp']}" target="_blank" rel="noopener"><img class="wa-ic" src="assets/img/whatsapp-112.png" width="44" height="44" alt=""><div><span>WhatsApp</span><b>Chat with us</b></div></a>
      <a href="mailto:{F['email']}"><span class="card__ic card__ic--soft">{icon('mail')}</span><div><span>Email</span><b>{F['email']}</b></div></a>
      <a href="mailto:{F['email_alt']}"><span class="card__ic card__ic--soft">{icon('mail')}</span><div><span>Alternative email</span><b>{F['email_alt']}</b></div></a>
      <a href="{F['maps']}" target="_blank" rel="noopener"><span class="card__ic card__ic--soft">{icon('pin')}</span><div><span>Office (opens Google Maps)</span><b>{F['office']}</b></div></a>
      <div class="ci"><span class="card__ic card__ic--soft">{icon('clock')}</span><div><span>Postal address and hours</span><b>{F['po_box']}<br>{F['hours']}</b></div></div>
    </div>
    <form class="form rv" id="enquiry" data-to="{F['email']}" novalidate>
      <h2>Send us an enquiry</h2>
      <p class="muted">Fields marked * are required.</p>
      <div class="row">
        <div class="field"><label for="f-name">Your name *</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-org">Organisation</label><input id="f-org" name="org" autocomplete="organization"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <div class="field"><label for="f-svc">Service of interest</label><select id="f-svc" name="service"><option value="">Choose one (optional)</option>{opts}<option>Something else</option></select></div>
      <div class="field"><label for="f-msg">How can we help? *</label><textarea id="f-msg" name="message" required></textarea></div>
      <button class="btn btn--red" type="submit">Send enquiry{icon('arrow')}</button>
      <p class="form__note" id="form-note" aria-live="polite">This opens your email app with the message ready to send to {F['email']}.</p>
    </form>
  </div>
</section>
"""
    return (head("Contact FDSC | Dar es Salaam, Tanzania",
                 f"Contact Frontline Development Services Consulting: {F['phone']}, {F['email']}. {F['office']}.",
                 "contact.html") + header("contact.html") + body + footer())


def page_404():
    b = "/"
    body = f"""<section class="phead" style="min-height:50vh">
  <div class="wrap"><p class="crumbs">Error 404</p><h1 class="h1">This page has <span class="accent">moved or never existed.</span></h1>
  <p class="lead">Try the home page, or get in touch and we will point you in the right direction.</p>
  <div class="hero__btns" style="margin-top:28px"><a class="btn btn--red" href="/">Go to the home page{icon('arrow')}</a><a class="btn btn--line" href="/contact.html">Contact us</a></div></div>
</section>"""
    return (head("Page not found | FDSC", "This page could not be found.", "404.html", base=b).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"')
            + header("", base=b) + body + footer(base=b))


# ---- brand files, sitemap -------------------------------------------------------------------
def copy_brand():
    dst = os.path.join(SITE, "assets", "brand")
    os.makedirs(dst, exist_ok=True)
    svg = os.path.join(ROOT, "brand", "logo", "svg")
    png = os.path.join(ROOT, "brand", "logo", "png")
    for fn in ("fdsc-wordmark.svg", "fdsc-logo.svg", "fdsc-logo-white.svg", "fdsc-mark.svg", "fdsc-favicon.svg"):
        shutil.copy(os.path.join(svg, fn), os.path.join(dst, fn))
    shutil.copy(os.path.join(png, "fdsc-app-icon-180.png"), os.path.join(dst, "apple-touch-icon.png"))
    shutil.copy(os.path.join(png, "fdsc-app-icon-192.png"), os.path.join(dst, "icon-192.png"))
    shutil.copy(os.path.join(png, "fdsc-app-icon-512.png"), os.path.join(dst, "icon-512.png"))
    shutil.copy(os.path.join(png, "favicon.ico"), os.path.join(SITE, "favicon.ico"))
    json.dump({"name": F["name"], "short_name": "FDSC", "start_url": "/", "display": "standalone",
               "background_color": "#ffffff", "theme_color": "#C23C47",
               "icons": [{"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(SITE, "site.webmanifest"), "w"), indent=1)


def write(fn, s):
    open(os.path.join(SITE, fn), "w").write(s)
    print("wrote", fn, f"{len(s) / 1024:.0f} KB")


if __name__ == "__main__":
    copy_brand()
    write("index.html", page_home())
    write("about.html", page_about())
    write("services.html", page_services())
    write("work.html", page_work())
    write("contact.html", page_contact())
    write("404.html", page_404())
    urls = "".join(f"<url><loc>{F['url']}/{'' if h == 'index.html' else h}</loc></url>" for h, _ in NAV)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {F['url']}/sitemap.xml\n")
