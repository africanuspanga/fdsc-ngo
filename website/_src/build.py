"""Builds the FDSC static website from content.py.

Run:  python3 website/_src/build.py
Writes index.html, about.html, services.html, work.html, contact.html, privacy.html, 404.html, sitemap.xml,
robots.txt, llms.txt and llms-full.txt, and copies brand files into website/assets/brand/.
Upload everything in website/ except _src/.
"""
import datetime
import html
import json
import os
import re
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
VER = "4"  # bump to bust caches of css/js
PDF = "assets/docs/FDSC-Company-Profile.pdf"
NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("work.html", "Our work"), ("contact.html", "Contact")]
TODAY = datetime.date.today()
# Vercel Web Analytics (cookieless, so no consent banner needed). Turn on Analytics for the project in the
# Vercel dashboard first, then set this to True and rebuild. Off, the pages load no analytics script at all.
ANALYTICS = False
e = html.escape


def plain(s):
    """Content strings carry a little HTML (entities, <span>); strip it for meta tags, JSON-LD and llms.txt."""
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ---- helpers -------------------------------------------------------------------------------
def pic(slug, alt, sizes="(max-width: 700px) 100vw, 50vw", cls="", eager=False, base=""):
    w, h = Image.open(os.path.join(IMG, f"{slug}-1600.webp")).size
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{base}assets/img/{slug}-1600.webp" srcset="{base}assets/img/{slug}-800.webp 800w, '
            f'{base}assets/img/{slug}-1600.webp 1600w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def head(title, desc, path, base="", crumb=None, extra_ld=None, index=True):
    url = F["url"] + "/" + ("" if path == "index.html" else path)
    org = {"@type": "ProfessionalService", "@id": F["url"] + "/#org", "name": F["name"],
           "alternateName": "FDSC", "url": F["url"] + "/", "logo": F["url"] + "/assets/brand/fdsc-logo.svg",
           "image": F["url"] + "/assets/brand/og-image.jpg", "email": F["email"], "telephone": F["phone"],
           "foundingDate": str(F["founded"]), "description": C.INTRO, "slogan": C.HEADLINE,
           "address": {"@type": "PostalAddress", "streetAddress": F["street"],
                       "postOfficeBoxNumber": "105471", "addressLocality": "Dar es Salaam", "addressCountry": "TZ"},
           "openingHours": "Mo-Fr 08:30-17:00", "hasMap": F["maps"],
           "areaServed": [{"@type": "Country", "name": "Tanzania"}, {"@type": "Place", "name": "Zanzibar"}],
           "knowsAbout": [plain(s["title"]) for s in C.SERVICES]}
    graph = [org, {"@type": "WebSite", "@id": F["url"] + "/#site", "url": F["url"] + "/", "name": "FDSC",
                   "publisher": {"@id": F["url"] + "/#org"}, "inLanguage": "en-GB"}]
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": F["url"] + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    graph += extra_ld or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    canon = f'<link rel="canonical" href="{url}">' if index else '<meta name="robots" content="noindex">'
    va = '\n<script src="/_vercel/insights/script.js" defer></script>' if ANALYTICS else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canon}
<meta property="og:type" content="website">
<meta property="og:site_name" content="FDSC">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F['url']}/assets/brand/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="FDSC logo, the line &ldquo;{e(C.HEADLINE)}&rdquo; and a dot map of Tanzania">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{F['url']}/assets/brand/og-image.jpg">
<meta name="theme-color" content="#C23C47">
<link rel="icon" href="{base}favicon.ico" sizes="48x48">
<link rel="icon" href="{base}assets/brand/fdsc-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preload" href="{base}assets/fonts/SpaceGrotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/InstrumentSans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/fonts/fonts.css">
<link rel="stylesheet" href="{base}assets/css/site.css?v={VER}">{va}
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(path, base=""):
    links = "".join(f'<a href="{base}{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{base}{h}"{" aria-current=\"page\"" if h == path else ""}>{t}{icon("arrow")}</a>' for h, t in NAV)
    here = " top__cta--here" if path == "contact.html" else ""
    return f"""<header class="top">
  <div class="wrap top__in">
    <a class="brand" href="{base}index.html" aria-label="FDSC home"><img class="logo" src="{base}assets/brand/fdsc-wordmark.svg" width="188" height="100" alt="FDSC"></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="top__cta{here}"><a class="btn btn--red" href="{base}contact.html"><span class="top__lg">Request a proposal</span><span class="top__sm">Contact us</span>{icon('arrow')}</a></div>
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
      <div><h2>Explore</h2><ul>{nav}</ul></div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div class="foot__c"><h2>Contact</h2><ul>
        <li>{icon('pin')}<span>{F['office']}<br>{F['po_box']}</span></li>
        <li>{icon('phone')}<a href="tel:{F['phone_href']}">{F['phone']}</a></li>
        <li>{icon('mail')}<span><a href="mailto:{F['email']}">{F['email']}</a><br><a href="mailto:{F['email_alt']}">{F['email_alt']}</a></span></li>
      </ul></div>
    </div>
    <div class="foot__bar"><span>&copy; <span id="year">{TODAY.year}</span> {F['name']}. All rights reserved.</span><span>{F['registration']} &middot; <a href="{base}privacy.html">Privacy notice</a></span></div>
  </div>
</footer>
<button class="totop" type="button" aria-label="Back to top">{icon('arrow-up')}</button>
<a class="wa" href="https://wa.me/{F['whatsapp']}" target="_blank" rel="noopener" aria-label="Chat with FDSC on WhatsApp (opens in a new tab)"><img src="{base}assets/img/whatsapp-112.png" width="56" height="56" alt=""></a>
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
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span aria-current="page">{crumb}</span></nav>
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
    return (head("FDSC | Development consulting and evaluation in Tanzania",
                 f"Tanzanian consultancy delivering evaluations, baseline studies, M&E systems, gender analysis and capacity building for government, donors and NGOs since {F['founded']}.",
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
    return (head("About FDSC | Development consultancy in Dar es Salaam",
                 "Founded in 2014 in Dar es Salaam, FDSC provides development and management consulting to government, development partners, NGOs and business across Tanzania.",
                 "about.html", crumb="About") + header("about.html") + body + footer())


def page_services():
    det = ""
    for i, s in enumerate(C.SERVICES):
        pts = "".join(f"<li>{icon('check')}<span>{p}</span></li>" for p in s["points"])
        det += (f'<article class="svc-detail rv" id="{s["slug"]}"><span class="card__ic card__ic--soft">{icon(s["icon"])}</span>'
                f'<div><h2>{s["title"]}</h2><p>{s["short"]}</p></div><ul>{pts}</ul></article>')
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
    return (head("Services | Evaluation, M&E, gender and training | FDSC",
                 "Programme management, research and evaluation, M&E, gender, organisational development, training, data and agribusiness value chain consulting in Tanzania.",
                 "services.html", crumb="Services") + header("services.html") + body + footer())


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
    return (head(f"Our work | {s['assignments']} assignments across Tanzania | FDSC",
                 f"{s['assignments']} evaluations, baselines, M&E systems, training and advisory assignments for Solidaridad, Rikolto, HELVETAS, TNC, the Ministry of Finance and others since {F['founded']}.",
                 "work.html", crumb="Our work") + header("work.html") + body + footer())


def faq_ld():
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C.FAQ]}


def faq_html():
    def linkify(t):
        t = e(t)
        t = t.replace(F["email"], f'<a href="mailto:{F["email"]}">{F["email"]}</a>')
        return t.replace(F["phone"], f'<a href="https://wa.me/{F["whatsapp"]}" target="_blank" rel="noopener">{F["phone"]}</a>')
    return "".join(f'<details class="qa"><summary>{e(q)}</summary><p>{linkify(a)}</p></details>' for q, a in C.FAQ)


def page_contact():
    opts = "".join(f"<option>{s['title'][0].upper() + s['title'][1:]}</option>" for s in C.SERVICES)

    def field(fid, name, label, req=False, kind="input", attrs=""):
        star = " *" if req else ""
        r = " required" if req else ""
        ctl = (f'<textarea id="{fid}" name="{name}"{r}{attrs}></textarea>' if kind == "textarea"
               else f'<input id="{fid}" name="{name}"{r}{attrs}>')
        err = f'<p class="err" id="{fid}-err"></p>' if req else ""
        return f'<div class="field"><label for="{fid}">{label}{star}</label>{ctl}{err}</div>'

    body = f"""{phead('Contact', 'Let&rsquo;s build lasting <span class="accent">impact together.</span>', 'Tell us about your programme, evaluation or capacity need. We reply within two working days.')}
<section class="section">
  <div class="wrap contact-grid">
    <div class="cinfo rv">
      <a href="tel:{F['phone_href']}"><span class="card__ic">{icon('phone')}</span><div><span>Call us</span><b>{F['phone']}</b></div></a>
      <a href="https://wa.me/{F['whatsapp']}" target="_blank" rel="noopener"><img class="wa-ic" src="assets/img/whatsapp-112.png" width="44" height="44" alt=""><div><span>WhatsApp (opens in a new tab)</span><b>Chat with us</b></div></a>
      <a href="mailto:{F['email']}"><span class="card__ic card__ic--soft">{icon('mail')}</span><div><span>Email</span><b>{F['email']}</b></div></a>
      <a href="mailto:{F['email_alt']}"><span class="card__ic card__ic--soft">{icon('mail')}</span><div><span>Alternative email</span><b>{F['email_alt']}</b></div></a>
      <a href="{F['maps']}" target="_blank" rel="noopener"><span class="card__ic card__ic--soft">{icon('pin')}</span><div><span>Office (opens Google Maps)</span><b>{F['office']}</b></div></a>
      <div class="ci"><span class="card__ic card__ic--soft">{icon('clock')}</span><div><span>Postal address and hours</span><b>{F['po_box']}<br>{F['hours']}</b></div></div>
    </div>
    <form class="form rv" id="enquiry" data-to="{F['email']}" novalidate>
      <h2>Send us an enquiry</h2>
      <p class="muted">Fields marked * are required.</p>
      <div class="row">
        {field('f-name', 'name', 'Your name', True, attrs=' autocomplete="name"')}
        {field('f-org', 'org', 'Organisation', attrs=' autocomplete="organization"')}
      </div>
      <div class="row">
        {field('f-email', 'email', 'Email', True, attrs=' type="email" autocomplete="email" inputmode="email"')}
        {field('f-phone', 'phone', 'Phone', attrs=' type="tel" autocomplete="tel"')}
      </div>
      <div class="field"><label for="f-svc">Service of interest</label><select id="f-svc" name="service"><option value="">Choose one (optional)</option>{opts}<option>Something else</option></select></div>
      {field('f-msg', 'message', 'How can we help?', True, kind='textarea')}
      <button class="btn btn--red" type="submit">Send enquiry{icon('arrow')}</button>
      <p class="form__note" id="form-note" aria-live="polite">This opens your email app with the message ready to send to {F['email']}.</p>
      <div class="form__fb" id="form-fb" hidden>
        <p>No email app opened? Copy your message and send it to <a href="mailto:{F['email']}">{F['email']}</a> from any email account, such as Gmail or Outlook on the web.</p>
        <button class="btn btn--line" type="button" id="copy-msg">{icon('copy')}<span>Copy message</span></button>
      </div>
    </form>
  </div>
</section>
<section class="section section--tint" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="rv">
      <p class="eyebrow">FAQ</p>
      <h2 class="h2" id="faq-h">Questions we <span class="accent">often hear.</span></h2>
      <p class="lead">Can&rsquo;t see yours? Call <a class="ul" href="tel:{F['phone_href']}">{F['phone']}</a> or email <a class="ul" href="mailto:{F['email']}">{F['email']}</a>.</p>
    </div>
    <div class="faq__list rv">{faq_html()}</div>
  </div>
</section>
"""
    return (head("Contact FDSC | Development consultants in Dar es Salaam",
                 f"Contact Frontline Development Services Consulting: {F['phone']}, {F['email']}. {F['office']}.",
                 "contact.html", crumb="Contact", extra_ld=[faq_ld()]) + header("contact.html") + body + footer())


def page_privacy():
    va = ("<h2>Visitor statistics</h2><p>We use Vercel Web Analytics to count visits to each page. It does not use "
          "cookies and does not identify individual visitors: we only see totals, such as how many people opened the "
          "Services page this month.</p>") if ANALYTICS else ""
    mail = f'<a href="mailto:{F["email"]}">{F["email"]}</a>'
    body = f"""{phead('Privacy notice', 'Privacy <span class="accent">notice.</span>', 'How we handle the personal information you share with us through this website, by email, by phone or on WhatsApp.')}
<section class="section">
  <div class="wrap">
    <div class="prose">
      <p class="muted">Last updated {C.PRIVACY_UPDATED}</p>
      <h2>Who we are</h2>
      <p>This website belongs to {F['name']} (FDSC), {F['office']}, {F['po_box']}. You can reach us at {mail} or {F['phone']}.</p>
      <h2>What this website collects</h2>
      <p>Nothing that identifies you. The site sets no cookies, has no accounts and does not store anything you type. The enquiry form does not send anything by itself: it opens your own email app with your message ready, and nothing reaches us until you press send there.</p>
      <p>If you arrive through a link with campaign tags (such as utm_source=linkedin), your browser keeps those tags until you close the tab and adds them to the end of your enquiry, so we can see which links bring people to us. You can delete that line before you send.</p>
      {va}
      <h2>What we receive when you contact us</h2>
      <p>When you email, call or message us on WhatsApp, we receive what you choose to share: usually your name, organisation, email address, phone number and your message.</p>
      <h2>How we use it</h2>
      <p>To reply to you, to prepare a proposal and, if we work together, to deliver and manage the assignment. We do not sell your information or add you to marketing lists.</p>
      <h2>Who we share it with</h2>
      <p>Only the consultants who work with us on your request, the companies that run our email and phone services, and public authorities where the law requires it.</p>
      <h2>How long we keep it</h2>
      <p>Enquiries for as long as we need to answer and follow them up. Records of assignments for as long as our contracts and Tanzanian law require.</p>
      <h2>Your rights</h2>
      <p>Under Tanzania&rsquo;s Personal Data Protection Act, 2022, you can ask to see the personal information we hold about you, ask us to correct or delete it, and object to how we use it. Email {mail} or write to us at {F['po_box']}.</p>
      <h2>Other websites</h2>
      <p>Links to WhatsApp and Google Maps take you to services that have their own privacy policies.</p>
      <h2>Changes to this notice</h2>
      <p>If the way we handle information changes, we will update this page and the date at the top.</p>
    </div>
  </div>
</section>
"""
    return (head("Privacy notice | FDSC",
                 "How Frontline Development Services Consulting handles the personal information you share through this website, by email, by phone or on WhatsApp.",
                 "privacy.html", crumb="Privacy notice") + header("privacy.html") + body + footer())


def page_404():
    b = "/"
    body = f"""<section class="phead" style="min-height:50vh">
  <div class="wrap"><p class="crumbs">Error 404</p><h1 class="h1">This page has <span class="accent">moved or never existed.</span></h1>
  <p class="lead">Try the home page, or get in touch and we will point you in the right direction.</p>
  <div class="hero__btns" style="margin-top:28px"><a class="btn btn--red" href="/">Go to the home page{icon('arrow')}</a><a class="btn btn--line" href="/contact.html">Contact us</a></div></div>
</section>"""
    return (head("Page not found | FDSC", "This page could not be found.", "404.html", base=b, index=False)
            + header("", base=b) + body + footer(base=b))


# ---- llms.txt (plain-language summary for AI assistants, see llmstxt.org) -------------------
def llms(full=False):
    s, u = C.STATS, F["url"]
    lc = lambda t: t if t[:2].isupper() else t[0].lower() + t[1:]   # keep acronyms such as M&E
    rep = ", ".join(f"{c} ({n})" for c, n in C.repeat_clients())
    L = [f"# {F['name']} (FDSC)", "",
         f"> {C.INTRO} Based in Dar es Salaam. {s['assignments']} assignments for {s['clients']} clients, in "
         f"{s['mainland']} of Tanzania's 26 mainland regions plus Unguja and Pemba (Zanzibar).", "",
         f"- Legal name: {F['name']} (FDSC). {F['registration']}.",
         f"- Office: {F['office']}. Postal address: {F['po_box']}.",
         f"- Phone and WhatsApp: {F['phone']}",
         f"- Email: {F['email']} (alternative: {F['email_alt']})",
         f"- Office hours: {F['hours']}",
         f"- Website: {u}/",
         f"- Clients and partners: {', '.join(n for _, n in C.CLIENTS)}",
         f"- Clients who have hired FDSC more than once (number of assignments): {rep}",
         "- Programmes FDSC has evaluated or supported were funded by the European Union, Irish Aid and the "
         "Belgian Development Cooperation (DGD), among others.", "",
         "## Pages", "",
         f"- [Home]({u}/): overview, sectors, services, approach and selected work",
         f"- [About]({u}/about.html): history, vision, mission, core values, why clients choose FDSC, clients and partners",
         f"- [Services]({u}/services.html): the nine services in detail, sectors and the four-step approach",
         f"- [Our work]({u}/work.html): map of regions reached and the full record of all {s['assignments']} assignments, newest first",
         f"- [Contact]({u}/contact.html): enquiry form, phone, WhatsApp, email, office address and FAQ",
         f"- [Company profile (PDF)]({u}/{PDF}): 13-page A4 company profile", "",
         "## Services", ""]
    L += [f"- [{plain(x['title'])[0].upper() + plain(x['title'])[1:]}]({u}/services.html#{x['slug']}): {plain(x['short'])} "
          f"Includes: {'; '.join(lc(plain(p)) if i else plain(p) for i, p in enumerate(x['points']))}." for x in C.SERVICES]
    L += ["", "## Sectors", ""]
    L += [f"- [{x['title']}]({u}/services.html): {plain(x['text'])}" for x in C.SECTORS]
    L += ["", "## Selected work", ""]
    L += [f"- [{plain(f['headline'])}]({u}/work.html): {plain(f['summary'])} Client: {f['a']['client']}. "
          f"Where: {f['a']['where']}. When: {f['a']['period']}." for f in C.featured()]
    L += ["", "## Frequently asked questions", ""]
    L += [f"- [{q}]({u}/contact.html#faq): {a}" for q, a in C.FAQ]
    if not full:
        L += ["", "## Optional", "",
              f"- [Full text and every assignment]({u}/llms-full.txt): about, vision, mission, values, approach and the complete assignment record",
              f"- [Privacy notice]({u}/privacy.html)"]
        return "\n".join(L) + "\n"
    L += ["", "## About FDSC", ""] + [p + "\n" for p in map(plain, C.ABOUT)]
    L += [f"Vision: {C.VISION}", "", f"Mission: {C.MISSION}", "", "Core values:", ""]
    L += [f"- {t}: {d}" for t, d in C.VALUES]
    L += ["", "Why clients choose FDSC:", ""] + [f"- {t}: {d}" for t, d in C.WHY]
    L += ["", "Who FDSC works with: " + ", ".join(C.AUDIENCES) + ".", "", "## How FDSC works", ""]
    L += [f"{i + 1}. {t}: {d}" for i, (t, d) in enumerate(C.APPROACH)]
    L += ["", "## Where FDSC works", ""]
    L += [f"- {z['name']} ({z['regions']}): {z['text']}" for z in C.ZONES]
    L += ["", f"## Assignment record ({s['assignments']} assignments, newest first)", ""]
    for a in C.ASSIGNMENTS:
        eu = " EU-funded." if a.get("donor") == "EU" else ""
        L.append(f"- {a['period'].replace(' - ', ' to ')} | {a['client']} | {C.TYPES[a['type']]}: {a['title']}. "
                 f"Where: {a['where']}.{eu}")
    return "\n".join(L) + "\n"


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
    write("privacy.html", page_privacy())
    write("404.html", page_404())
    write("llms.txt", llms())
    write("llms-full.txt", llms(full=True))
    pages = [h for h, _ in NAV] + ["privacy.html"]
    urls = "".join(f"<url><loc>{F['url']}/{'' if h == 'index.html' else h}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>" for h in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {F['url']}/sitemap.xml\n")
