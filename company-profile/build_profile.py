"""Builds the FDSC company profile (A4 portrait) from website/_src/content.py.

Run:  python3 company-profile/build_profile.py            -> profile.html + FDSC-Company-Profile.pdf
      python3 company-profile/build_profile.py --preview  -> also PNG page previews in company-profile/previews/
Needs Google Chrome and `pip install playwright segno`.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "website", "_src"))
import content as C  # noqa: E402
from shared import icon, logo_svg, dot_map, qr_svg  # noqa: E402

F = C.FIRM
OUT_HTML = os.path.join(HERE, "profile.html")
OUT_PDF = os.path.join(HERE, "FDSC-Company-Profile.pdf")
FONTS = "../website/assets/fonts/"
PARTNERS = "../website/assets/partners/"

MARK = logo_svg("fdsc-mark.svg", "mark", label=False)
MARK_W = logo_svg("fdsc-mark-white.svg", "mark", label=False)
LOGO_REV = logo_svg("fdsc-logo-white.svg", "logo")   # all-white logo for red pages
LOGO = logo_svg("fdsc-logo.svg", "logo")


def run(kicker, n, dark=False):
    return (f'<div class="run"><span class="kick">{kicker}</span>{MARK_W if dark else MARK}</div>'
            f'<div class="folio"><span>FDSC &middot; Company profile</span><span>{n:02d}</span></div>')


CONTENTS = [("About FDSC", 3), ("Vision, mission and values", 4), ("Why partner with us", 5),
            ("Our services", 6), ("Sectors and approach", 7), ("Where we work", 8),
            ("Selected work", 9), ("Assignment record", 10), ("Clients and partners", 12), ("Contact", 13)]


# ---------------------------------------------------------------------------------------------
def p_cover():
    return f"""<section class="page dark cover">
  <img class="cover__img" src="img/hero-njombe.jpg" alt="">
  <div class="cover__shade"></div>
  <div class="cover__glow"></div>
  <header class="cover__top">{LOGO_REV}<span class="cover__tag">Company profile</span></header>
  <div class="cover__body">
    <p class="eyebrow">Development and management consulting &middot; Since {F['founded']}</p>
    <h1>Turning strategy into <span class="hl">measurable results.</span></h1>
    <p class="cover__lede">Research, evaluation, capacity building and advisory services for government, development partners, NGOs and business across Tanzania.</p>
  </div>
  <footer class="cover__foot">
    <span>{icon('pin')} Dar es Salaam, Tanzania</span>
    <span>{icon('globe')} www.{F['domain']}</span>
    <span>{icon('phone')} {F['phone']}</span>
  </footer>
  <p class="cover__credit">Smallholder farmland, Makete, Njombe</p>
</section>"""


def p_contents():
    rows = "".join(f'<li><span class="n">{i + 1:02d}</span><span class="t">{t}</span><span class="pg">{p:02d}</span></li>'
                   for i, (t, p) in enumerate(CONTENTS))
    s = C.STATS
    return f"""<section class="page light">
  {run('Introduction', 2)}
  <p class="statement">{C.INTRO}</p>
  <div class="two">
    <div>
      <h2 class="h-sm">Contents</h2>
      <ol class="toc">{rows}</ol>
    </div>
    <div class="glance">
      <h2 class="h-sm">At a glance</h2>
      <div class="stat"><span class="big">{s['years']}<small>yrs</small></span><p>Delivering development and management consulting since {F['founded']}</p></div>
      <div class="stat"><span class="big">{s['assignments']}</span><p>Assignments for government, development partners, NGOs and business</p></div>
      <div class="stat"><span class="big">{s['clients']}</span><p>Clients, from the Ministry of Finance and Planning to Solidaridad and Rikolto</p></div>
      <div class="stat"><span class="big">{s['mainland']}<small>/26</small></span><p>Mainland regions reached, plus Unguja and Pemba in Zanzibar</p></div>
    </div>
  </div>
</section>"""


def p_about():
    paras = "".join(f"<p>{t}</p>" for t in C.ABOUT)
    chips = "".join(f'<li>{icon("check")}{a}</li>' for a in C.AUDIENCES)
    return f"""<section class="page light">
  {run('01 &middot; About FDSC', 3)}
  <h2 class="h-xl">A Tanzanian consultancy built on evidence and trust.</h2>
  <div class="about">
    <div class="about__text">{paras}
      <div class="facts">
        <div><span>Founded</span><b>{F['founded']}, Dar es Salaam</b></div>
        <div><span>Registration</span><b>Companies Act, 2002</b></div>
        <div><span>Reach</span><b>Mainland Tanzania and Zanzibar</b></div>
      </div>
    </div>
    <figure class="about__img"><img src="img/community-meeting.jpg" alt=""><figcaption>Community meeting, East Africa</figcaption></figure>
  </div>
  <div class="glass who">
    <h3 class="h-xs">Who we work with</h3>
    <ul class="chips">{chips}</ul>
  </div>
</section>"""


def p_values():
    vals = "".join(f'<li><span class="n">{i + 1:02d}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(C.VALUES))
    return f"""<section class="page dark values-page">
  <div class="dots-bg"></div>
  {MARK_W.replace('class="mark"', 'class="mark watermark"')}
  {run('02 &middot; Vision, mission and values', 4, dark=True)}
  <h2 class="h-xl">What drives us.</h2>
  <div class="vm">
    <div class="glass-d"><span class="label">Our vision</span><p>{C.VISION}</p></div>
    <div class="glass-d"><span class="label">Our mission</span><p>{C.MISSION}</p></div>
  </div>
  <h3 class="h-sm on-dark">Our core values</h3>
  <ol class="values">{vals}</ol>
</section>"""


def p_why():
    items = "".join(f'<li><span class="n">{i + 1:02d}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(C.WHY))
    rep = C.repeat_clients()
    mx = max(n for _, n in rep)
    bars = "".join(f'<div class="bar"><span class="bl">{c.replace(" East and Central Africa", "").replace(" Swiss Intercooperation", "").replace("Ministry of Finance and Planning", "Ministry of Finance &amp; Planning")}</span>'
                   f'<span class="bv">{n}</span><span class="bt"><i style="width:{n / mx * 100:.0f}%"></i></span></div>' for c, n in rep)
    total = sum(n for _, n in rep)
    return f"""<section class="page light">
  {run('03 &middot; Why partner with us', 5)}
  <div class="why">
    <div class="why__l">
      <h2 class="h-xl">Why clients choose FDSC.</h2>
      <p class="lead">Since our establishment we have taken on high-level assignments for respected public and private organisations, local and international. Our experts attract clients who want continuing support, well beyond the contract period.</p>
      <div class="glass chart">
        <span class="label">Clients who come back</span>
        <p class="chart__note">Five organisations account for <b>{total} of our {C.STATS['assignments']}</b> assignments.</p>
        {bars}
        <p class="chart__foot">Number of assignments per client since {F['founded']}</p>
      </div>
      <figure class="why__img"><img src="img/field-discussion.jpg" alt=""><figcaption>Qualitative fieldwork</figcaption></figure>
    </div>
    <ol class="reasons">{items}</ol>
  </div>
</section>"""


def p_services():
    cards = ""
    for s in C.SERVICES:
        pts = "".join(f"<li>{p}</li>" for p in s["points"][:3])
        cards += (f'<article class="svc glass"><div class="svc__hd"><span class="svc__ic">{icon(s["icon"])}</span>'
                  f'<span class="svc__n">{C.SERVICES.index(s) + 1:02d}</span><h3>{s["title"]}</h3></div>'
                  f'<p>{s["short"]}</p><ul>{pts}</ul></article>')
    return f"""<section class="page light">
  {run('04 &middot; Our services', 6)}
  <div class="head-row">
    <h2 class="h-xl">Nine ways we help.</h2>
    <p class="lead">We design and deliver tailor-made, practical solutions to organisational, programme, economic and social challenges, for the public and private sectors alike.</p>
  </div>
  <div class="svc-grid">{cards}</div>
</section>"""


def p_sectors():
    cards = "".join(f'<article class="sector"><img src="img/{s["img"]}.jpg" alt=""><div><h3>{s["title"]}</h3><p>{s["text"]}</p></div></article>'
                    for s in C.SECTORS)
    steps = "".join(f'<li><span class="dot">{i + 1}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(C.APPROACH))
    return f"""<section class="page dark">
  <div class="dots-bg"></div>
  {run('05 &middot; Sectors and approach', 7, dark=True)}
  <h2 class="h-xl">Sectors we know from the inside.</h2>
  <div class="sectors">{cards}</div>
  <h3 class="h-sm on-dark">How we work</h3>
  <ol class="steps">{steps}</ol>
</section>"""


def p_map():
    regions = sorted({r for a in C.ASSIGNMENTS for r in a["regions"] if r not in C.ZANZIBAR} | {"Songwe"})
    by = C.by_type()
    mx = max(n for _, n in by)
    bars = "".join(f'<div class="bar"><span class="bl">{t}</span><span class="bv">{n}</span><span class="bt"><i style="width:{n / mx * 100:.0f}%"></i></span></div>' for t, n in by)
    m = dot_map(C.worked_regions(), step=8.2, dot=5.0, cls="tzmap", cities=["Mwanza", "Arusha", "Kigoma", "Dodoma", "Dar es Salaam", "Mbeya"])
    return f"""<section class="page light">
  {run('06 &middot; Where we work', 8)}
  <h2 class="h-xl">From Kigoma to Kilimanjaro, Mbeya to Pemba.</h2>
  <div class="mapwrap">
    <div class="map">{m}
      <div class="legend"><span><i class="on"></i>Regions where we have delivered assignments</span><span><i></i>Not yet</span></div>
    </div>
    <div class="map__side">
      <div class="stat"><span class="big">{C.STATS['mainland']}<small>of 26</small></span><p>Mainland regions</p></div>
      <div class="stat"><span class="big">2<small>islands</small></span><p>Unguja and Pemba, Zanzibar</p></div>
      <div class="glass chart">
        <span class="label">Our work by type</span>
        {bars}
      </div>
    </div>
  </div>
  <div class="zones">{''.join(f'<div class="zone glass"><b>{z["name"]}</b><span>{z["regions"]}</span><p>{z["text"]}</p></div>' for z in C.ZONES)}</div>
  <p class="regions"><b>Mainland regions reached ({len(regions)}):</b> {", ".join(regions)}. <b>Zanzibar:</b> Unguja and Pemba.</p>
</section>"""


def p_featured():
    cards = ""
    for f in C.featured():
        a = f["a"]
        cards += (f'<article class="feat"><div class="feat__img"><img src="img/{f["img"]}.jpg" alt=""><span class="tag">{f["label"]}</span></div>'
                  f'<div class="feat__b"><h3>{f["headline"].replace("AGRI-CONNECT", '<span class="nw">AGRI-CONNECT</span>')}</h3><p>{f["summary"]}</p>'
                  f'<div class="meta"><span>{a["client"].split(" (")[0]}</span><span>{a["where"]}</span></div></div></article>')
    return f"""<section class="page dark">
  <div class="dots-bg"></div>
  {run('07 &middot; Selected work', 9, dark=True)}
  <div class="head-row">
    <h2 class="h-xl">Selected work.</h2>
    <p class="lead on-dark">A few of the programmes we have evaluated, measured and strengthened. The full record follows.</p>
  </div>
  <div class="feats">{cards}</div>
</section>"""


def record_rows(items):
    out = ""
    for a in items:
        donor = ' <span class="eu">EU-funded</span>' if a.get("donor") == "EU" else ""
        out += (f'<tr><td class="per">{a["period"].replace(" - ", "&ndash;")}</td>'
                f'<td class="cl">{a["client"]}</td>'
                f'<td class="as"><b>{a["title"].replace("TASP II", "TASP&nbsp;II")}</b><span>{a["where"]}{donor}</span></td>'
                f'<td class="ty"><span class="pill t-{a["type"]}">{C.TYPES_SHORT[a["type"]]}</span></td></tr>')
    return out


def p_record(part):
    half = 14
    items = C.ASSIGNMENTS[:half] if part == 1 else C.ASSIGNMENTS[half:]
    n = 10 if part == 1 else 11
    head = ('<h2 class="h-lg">Assignment record</h2><p class="lead">Every assignment since our first in 2014, newest first.</p>'
            if part == 1 else '<h2 class="h-lg">Assignment record <span class="muted">(continued)</span></h2>')
    return f"""<section class="page light">
  {run('08 &middot; Assignment record', n)}
  <div class="rec-head">{head}</div>
  <table class="rec"><thead><tr><th>Period</th><th>Client</th><th>Assignment</th><th>Type</th></tr></thead>
  <tbody>{record_rows(items)}</tbody></table>
</section>"""


def p_clients():
    tiles = "".join(f'<div class="lg"><img src="img/logo-{s}.jpg" alt="{n}"></div>' for s, n in C.CLIENTS)
    return f"""<section class="page dark">
  <div class="dots-bg"></div>
  {run('09 &middot; Clients and partners', 12, dark=True)}
  <h2 class="h-xl">Trusted by the organisations we serve.</h2>
  <p class="lead on-dark">FDSC is proud to have worked with, and earned the trust of, these organisations.</p>
  <div class="logos">{tiles}
    <div class="lg lg--note"><span class="label">Funding behind the work</span><p>Programmes we have evaluated and supported were funded by the <b>European Union</b>, <b>Irish Aid</b> and the <b>Belgian Development Cooperation (DGD)</b>, among others.</p></div>
  </div>
</section>"""


def p_back():
    return f"""<section class="page dark back">
  <img class="back__img" src="img/tea-hills.jpg" alt="">
  <div class="back__shade"></div>
  <div class="cover__glow"></div>
  {run('10 &middot; Contact', 13, dark=True)}
  <div class="back__body">
    <h2 class="h-hero">Let&rsquo;s build lasting impact together.</h2>
    <p class="lead on-dark">Tell us about your programme, evaluation or capacity need. We will reply within two working days with a first view of how we can help.</p>
    <div class="contact">
      <div class="glass-d"><span class="label">{icon('pin')} Office</span><p>{F['office'].replace(', Dar es Salaam', '')}<br>{F['po_box']}</p></div>
      <div class="glass-d"><span class="label">{icon('phone')} Phone / WhatsApp</span><p>{F['phone']}</p></div>
      <div class="glass-d"><span class="label">{icon('mail')} Email</span><p>{F['email']}<br>{F['email_alt']}</p></div>
      <div class="glass-d qrbox">{qr_svg(F['url'], dark='#962733')}<p><span class="label">{icon('globe')} Website</span>www.{F['domain']}</p></div>
    </div>
  </div>
  <footer class="back__foot">{LOGO_REV}<span>{F['name']} &middot; {F['registration']}</span></footer>
</section>"""


CSS = r"""
@font-face{font-family:'Space Grotesk';font-weight:300;src:url(fonts/SpaceGrotesk-300.ttf) format('truetype')}
@font-face{font-family:'Space Grotesk';font-weight:400;src:url(fonts/SpaceGrotesk-400.ttf) format('truetype')}
@font-face{font-family:'Space Grotesk';font-weight:500;src:url(fonts/SpaceGrotesk-500.ttf) format('truetype')}
@font-face{font-family:'Space Grotesk';font-weight:600;src:url(fonts/SpaceGrotesk-600.ttf) format('truetype')}
@font-face{font-family:'Instrument Sans';font-weight:400;src:url(fonts/InstrumentSans-400.ttf) format('truetype')}
@font-face{font-family:'Instrument Sans';font-weight:500;src:url(fonts/InstrumentSans-500.ttf) format('truetype')}
@font-face{font-family:'Instrument Sans';font-weight:600;src:url(fonts/InstrumentSans-600.ttf) format('truetype')}
@font-face{font-family:'Instrument Sans';font-weight:700;src:url(fonts/InstrumentSans-700.ttf) format('truetype')}
@font-face{font-family:'Instrument Sans';font-style:italic;font-weight:400;src:url(fonts/InstrumentSans-Italic-400.ttf) format('truetype')}
@page{size:A4;margin:0}
:root{--red:#C23C47;--red-700:#AE303C;--red-800:#962733;--red-900:#7C1E29;--red-200:#F6C6CB;--red-50:#FCEEEF;--pink:#FFE1E4;
  --ink:#141414;--muted:#5F5F5F;--line:#E9E3E3;--paper:#FBF8F8}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Instrument Sans',system-ui,sans-serif;font-size:9.2pt;line-height:1.55;color:var(--ink);background:#7a8494}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;padding:17mm 16mm 18mm;page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto}
@media screen{.page{margin:10mm auto;box-shadow:0 10px 40px rgba(0,0,0,.35)}}
h1,h2,h3,.big,.statement,.n,.label,.kick,.eyebrow{font-family:'Space Grotesk',sans-serif}
h1,h2,h3{text-wrap:balance}
p,li{text-wrap:pretty}
.light{background:radial-gradient(90% 55% at 100% 0%,rgba(194,60,71,.07),transparent 62%),radial-gradient(70% 40% at 0% 100%,rgba(194,60,71,.04),transparent 60%),#fff}
.dark{color:#fff;background:radial-gradient(110% 70% at 100% 105%,rgba(255,255,255,.16),transparent 60%),radial-gradient(80% 50% at 0% -5%,rgba(110,24,34,.35),transparent 62%),linear-gradient(160deg,var(--red),var(--red-800))}
.dots-bg{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.2) .55px,transparent .7px);background-size:3.2mm 3.2mm;
  -webkit-mask-image:radial-gradient(80% 60% at 85% 100%,#000 10%,transparent 70%);mask-image:radial-gradient(80% 60% at 85% 100%,#000 10%,transparent 70%);pointer-events:none}
.page>*{position:relative}
.page>.dots-bg,.page>.watermark{position:absolute}
/* running head / folio */
.run{display:flex;justify-content:space-between;align-items:center;margin-bottom:11mm}
.kick{font-size:6.8pt;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.dark .kick{color:var(--pink)}
.run .mark{height:8.5mm;width:auto}
.folio{position:absolute!important;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:6.6pt;color:var(--muted);letter-spacing:.04em}
.dark .folio{color:rgba(255,255,255,.72)}
/* type */
.h-hero{font-size:40pt;line-height:1.02;font-weight:400;letter-spacing:-.02em;color:#fff}
.h-xl{font-size:27pt;line-height:1.08;font-weight:400;letter-spacing:-.018em;max-width:150mm}
.h-xl + .lead{margin-top:5mm}
.h-lg{font-size:19pt;font-weight:400;letter-spacing:-.01em}
.h-sm{font-size:10.5pt;font-weight:600;letter-spacing:-.005em;margin-bottom:4mm}
.h-xs{font-size:8.6pt;font-weight:600;margin-bottom:3mm}
.dark .h-xl{color:#fff}
.on-dark{color:#fff}
.lead{font-size:10.6pt;line-height:1.55;color:var(--muted);max-width:132mm}
.lead.on-dark{color:rgba(255,255,255,.9)}
.muted{color:var(--muted)}
.label{display:inline-flex;align-items:center;gap:1.6mm;font-size:6.8pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.dark .label{color:var(--pink)}
.label .ic{width:3.6mm;height:3.6mm}
.eyebrow{font-size:7.4pt;letter-spacing:.16em;text-transform:uppercase;color:var(--pink);margin-bottom:6mm}
.ic{width:5mm;height:5mm;flex:none}
.glass{background:#fff;border:.3mm solid var(--line);border-radius:3mm}
.glass-d{background:linear-gradient(160deg,rgba(255,255,255,.14),rgba(255,255,255,.06));border:.3mm solid rgba(255,255,255,.3);border-radius:3mm;padding:6mm}
/* cover */
.cover{padding:0}
.cover__img{position:absolute;left:0;right:0;bottom:0;width:100%;height:43%;object-fit:cover;object-position:center 55%}
.cover__shade{position:absolute;inset:0;background:linear-gradient(180deg,transparent 78%,rgba(20,20,20,.38) 100%)}
.cover__glow{position:absolute;inset:0;background:radial-gradient(60% 40% at 95% 25%,rgba(255,255,255,.14),transparent 70%);pointer-events:none}
.cover__top{position:absolute;top:16mm;left:16mm;right:16mm;display:flex;justify-content:space-between;align-items:flex-start}
.cover__top .logo{width:62mm;height:auto}
.cover__tag{font-family:'Space Grotesk';font-size:7.4pt;letter-spacing:.16em;text-transform:uppercase;color:var(--pink);padding-top:2mm}
.cover__body{position:absolute;top:70mm;left:16mm;right:22mm}
.cover h1{font-size:44pt;line-height:1.0;font-weight:400;letter-spacing:-.025em;color:#fff;max-width:165mm}
.cover h1 .hl{color:var(--pink)}
.cover__lede{margin-top:7mm;font-size:11pt;line-height:1.5;color:rgba(255,255,255,.92);max-width:118mm}
.cover__foot{position:absolute;left:16mm;right:16mm;bottom:15mm;display:flex;justify-content:space-between;gap:4mm;padding:4.2mm 6mm;border-radius:3mm;
  background:#fff;font-size:8.2pt;color:var(--ink);font-weight:500}
.cover__foot span{display:inline-flex;align-items:center;gap:2mm}
.cover__foot .ic{width:4mm;height:4mm;color:var(--red)}
.cover__credit{position:absolute;right:16mm;bottom:8mm;font-size:5.8pt;color:rgba(255,255,255,.75)}
/* contents */
.statement{font-size:19pt;line-height:1.28;font-weight:400;letter-spacing:-.012em;max-width:168mm;margin-bottom:14mm}
.two{display:grid;grid-template-columns:1fr 70mm;gap:12mm}
.toc{list-style:none;border-top:.3mm solid var(--line)}
.toc li{display:grid;grid-template-columns:10mm 1fr auto;align-items:baseline;padding:4.4mm 0;border-bottom:.3mm solid var(--line);font-size:10.5pt}
.toc .n{font-size:8pt;color:var(--red);font-weight:600}
.toc .pg{font-family:'Space Grotesk';font-size:9pt;color:var(--muted)}
.glance{display:flex;flex-direction:column}
.glance .stat{padding:4mm 0 4.4mm;border-top:.3mm solid var(--line);display:block;flex:1}
.glance .stat:last-child{border-bottom:.3mm solid var(--line)}
.big{display:block;font-size:34pt;line-height:1;font-weight:300;letter-spacing:-.03em;color:var(--ink)}
.big small{font-size:12pt;letter-spacing:0;margin-left:1.2mm;color:var(--muted);font-weight:400}
.stat p{font-size:8.2pt;color:var(--muted);margin-top:1.6mm;line-height:1.4}
/* about */
.about{display:grid;grid-template-columns:1fr 74mm;gap:10mm;margin-top:9mm}
.about__text p{margin-bottom:3.6mm;font-size:9.8pt;line-height:1.6}
.about__text p:first-child{font-size:11.2pt;line-height:1.5}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:6mm;border-top:.3mm solid var(--line);padding-top:4mm}
.facts span{display:block;font-size:6.8pt;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-family:'Space Grotesk';font-weight:600}
.facts b{font-weight:600;font-size:8.6pt}
.about__img{position:relative;min-height:100mm;border-radius:3mm;overflow:hidden}
.about__img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:40% center}
figcaption{position:absolute;left:3mm;bottom:3mm;font-size:6pt;color:#fff;background:rgba(20,20,20,.55);padding:.8mm 2mm;border-radius:1mm}
.who{margin-top:9mm;padding:6mm 7mm}
.chips{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:2.6mm 5mm}
.chips li{display:flex;align-items:center;gap:2mm;font-size:8.8pt}
.chips .ic{width:4mm;height:4mm;color:var(--red)}
/* values */
.watermark{right:-30mm;bottom:-12mm;height:175mm;width:auto;opacity:.08}
.vm{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:10mm 0 12mm}
.vm p{font-family:'Space Grotesk';font-size:12.4pt;line-height:1.42;font-weight:400;color:#fff;margin-top:4mm}
.values{list-style:none;border-top:.3mm solid rgba(255,255,255,.3)}
.values li{display:grid;grid-template-columns:14mm 42mm 1fr;align-items:baseline;padding:5.2mm 0;border-bottom:.3mm solid rgba(255,255,255,.3)}
.values .n{color:var(--pink);font-size:8.4pt;font-weight:600}
.values b{font-family:'Space Grotesk';font-weight:500;font-size:14pt;color:#fff}
.values p{color:rgba(255,255,255,.9);font-size:9.8pt}
/* why */
.why{display:grid;grid-template-columns:78mm 1fr;gap:10mm}
.why__l{display:flex;flex-direction:column}
.why__img{position:relative;flex:1;min-height:40mm;margin-top:5mm;border-radius:3mm;overflow:hidden}
.why__img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%}
.why .lead{margin:6mm 0 8mm;font-size:9.8pt}
.chart{padding:6mm}
.chart__note{font-size:8.6pt;margin:2.5mm 0 4mm;color:var(--ink)}
.chart__foot{font-size:6.6pt;color:var(--muted);margin-top:3mm}
.bar{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:1.2mm 3mm;margin:3mm 0;font-size:7.8pt}
.bar .bt{grid-column:1/-1}
.bt{height:2.6mm;background:#F1EBEB;border-radius:2mm;overflow:hidden}
.bt i{display:block;height:100%;background:linear-gradient(90deg,var(--red-200),#E58A93);border-radius:2mm}
.bar:first-of-type .bt i{background:linear-gradient(90deg,var(--red-800),var(--red))}
.bv{font-family:'Space Grotesk';font-weight:600;text-align:right}
.reasons{list-style:none;border-top:.3mm solid var(--line)}
.nw{white-space:nowrap}
.reasons li{display:grid;grid-template-columns:11mm 1fr;padding:7mm 0;border-bottom:.3mm solid var(--line)}
.reasons .n{font-size:8.4pt;color:var(--red);font-weight:600;padding-top:.8mm}
.reasons b{font-family:'Space Grotesk';font-size:12.2pt;font-weight:500;display:block;margin-bottom:1.2mm}
.reasons p{color:var(--muted);font-size:9.3pt}
/* services */
.head-row{display:grid;grid-template-columns:1fr 84mm;gap:8mm;align-items:end;margin-bottom:7mm}
.head-row .lead{font-size:9pt}
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);column-gap:4mm;row-gap:0}
.head-row + .svc-grid{margin-top:-1.5mm}
.svc{padding:4.2mm 4.6mm 4mm;display:grid;grid-row:span 3;grid-template-rows:subgrid;row-gap:0;margin-bottom:3.6mm}
.svc__hd{display:grid;grid-template-columns:8mm 1fr;gap:2mm;align-content:start;margin-bottom:2mm}
.svc__n{justify-self:end;font-family:'Space Grotesk';font-size:7.4pt;font-weight:500;color:var(--muted)}
.svc__hd h3{grid-column:1/-1}
.svc__ic{width:8mm;height:8mm;border-radius:2mm;display:grid;place-items:center;background:var(--red-50);border:.3mm solid rgba(194,60,71,.18);color:var(--red)}
.svc__ic .ic{width:4.6mm;height:4.6mm}
.svc h3{font-size:10pt;font-weight:600;line-height:1.2;letter-spacing:-.01em}
.svc p{font-size:7.8pt;color:var(--muted);line-height:1.4;margin-bottom:2.6mm}
.svc ul{list-style:none;align-self:start;border-top:.3mm solid var(--line);padding-top:2.2mm}
.svc li{font-size:7.4pt;line-height:1.32;padding:.5mm 0 .5mm 3.4mm;position:relative}
.svc li::before{content:"";position:absolute;left:0;top:1.9mm;width:1.4mm;height:1.4mm;border-radius:50%;background:var(--red)}
/* sectors */
.sectors{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm;margin:9mm 0 10mm}
.sector{border-radius:3mm;overflow:hidden;background:#fff;color:var(--ink)}
.sector img{width:100%;height:40mm;object-fit:cover;display:block}
.sector div{padding:4.4mm 5mm 5mm}
.sector h3{font-size:11.6pt;font-weight:500;color:var(--ink);margin-bottom:1.6mm}
.sector p{font-size:8.2pt;color:var(--muted);line-height:1.45}
.steps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;position:relative;padding-top:2mm}
.steps::before{content:"";position:absolute;left:4mm;right:calc((100% - 15mm) / 4 - 4mm);top:6mm;height:.4mm;background:rgba(255,255,255,.55)}
.steps .dot{position:relative;display:grid;place-items:center;width:8mm;height:8mm;border-radius:50%;background:var(--red-800);border:.4mm solid rgba(255,255,255,.7);font-family:'Space Grotesk';font-size:8pt;font-weight:600;color:#fff;margin-bottom:3.6mm}
.steps li:first-child .dot{border-color:#fff;background:#fff;color:var(--red)}
.steps b{font-family:'Space Grotesk';font-size:11pt;font-weight:500;color:#fff;display:block;margin-bottom:1.2mm}
.steps p{font-size:8pt;color:rgba(255,255,255,.9);line-height:1.45}
/* map */
.mapwrap{display:grid;grid-template-columns:1fr 62mm;gap:6mm;margin-top:6mm}
.tzmap{width:100%;height:auto;display:block}
.tzmap .dots{fill:none;stroke-linecap:round}
.tzmap .dots.off{stroke:#E2DCDC}
.tzmap .dots.on{stroke:var(--red)}
.tzmap .isl.on{fill:var(--red)}
.tzmap .isl.off{fill:#E2DCDC}
.tzmap .city circle{fill:var(--ink);stroke:#fff;stroke-width:2.2}
.tzmap .city text{font-family:'Space Grotesk';font-size:15px;font-weight:600;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}
.legend{display:flex;gap:6mm;margin-top:3mm;font-size:7.4pt;color:var(--muted)}
.legend span{display:inline-flex;align-items:center;gap:1.8mm}
.legend i{width:2.6mm;height:2.6mm;border-radius:50%;background:#E2DCDC}
.legend i.on{background:var(--red)}
.map__side .stat{padding:3mm 0 4mm;border-bottom:.3mm solid var(--line)}
.map__side .stat:first-child{border-top:.3mm solid var(--line)}
.map__side .chart{margin-top:6mm;padding:5mm}
.map__side .bar{font-size:7.4pt;margin:2.6mm 0}
.map__side .bar:first-of-type .bt i{background:linear-gradient(90deg,var(--red-800),var(--red))}
.zones{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm;margin-top:6mm}
.zone{padding:3.8mm 5mm}
.zone b{display:block;font-family:'Space Grotesk';font-weight:600;font-size:10.4pt;margin-bottom:1mm}
.zone span{display:block;font-size:7.4pt;color:var(--red);font-weight:600;line-height:1.35;margin-bottom:2mm}
.zone p{font-size:8pt;color:var(--muted);line-height:1.42}
.regions{margin-top:5mm;font-size:7.6pt;color:var(--muted);line-height:1.55;border-top:.3mm solid var(--line);padding-top:3mm}
.regions b{color:var(--ink)}
/* featured */
.feats{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm}
.feat{display:grid;grid-template-columns:38mm 1fr;border-radius:3mm;overflow:hidden;background:#fff;height:68mm}
.feat__img{position:relative}
.feat__img img{width:100%;height:100%;object-fit:cover;display:block}
.tag{position:absolute;left:2.5mm;top:2.5mm;font-size:6pt;font-weight:600;letter-spacing:.06em;color:#fff;background:var(--red);border:.25mm solid rgba(255,255,255,.4);padding:.8mm 2mm;border-radius:5mm}
.feat__b{padding:4.6mm 4.6mm 4mm;display:flex;flex-direction:column}
.feat h3{font-size:10.8pt;font-weight:500;line-height:1.22;color:var(--ink);margin-bottom:2mm}
.feat p{font-size:7.9pt;line-height:1.45;color:var(--muted)}
.meta{margin-top:auto;padding-top:2.6mm;border-top:.3mm solid var(--line);display:flex;flex-direction:column;gap:.4mm;font-size:6.9pt;color:var(--muted)}
.meta span:first-child{color:var(--red);font-weight:600}
/* record */
.rec-head{margin-bottom:5mm}
.rec-head .lead{margin-top:2.5mm;font-size:9pt}
.rec{width:100%;border-collapse:collapse;font-size:7.5pt}
.rec th{text-align:left;font-family:'Space Grotesk';font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;padding:0 2.5mm 2.4mm 0;border-bottom:.4mm solid var(--red)}
.rec td{padding:1.9mm 2.5mm 1.9mm 0;border-bottom:.3mm solid var(--line);vertical-align:top;line-height:1.38}
.rec .per{width:26mm;font-family:'Space Grotesk';font-weight:500;white-space:nowrap;font-size:7.4pt}
.rec .cl{width:32mm;font-weight:600;font-size:7.3pt}
.rec .as b{font-weight:500;display:block}
.rec .as span{display:block;color:var(--muted);font-size:6.8pt;margin-top:.3mm}
.rec .ty{width:25mm;padding-right:0}
.rec .as span.eu{display:inline-block;margin-top:0}
.eu{display:inline-block;margin-left:1.2mm;padding:0 1.4mm;border-radius:1mm;background:#F1EDED;color:#3A3A3A;font-size:6.2pt;font-weight:600}
.pill{display:inline-block;padding:.6mm 2mm;border-radius:5mm;font-size:6.3pt;font-weight:600;line-height:1.3}
.pill{background:var(--red-50);color:var(--red-800)}.t-eval{background:var(--red);color:#fff}
/* clients */
.logos{display:grid;grid-template-columns:repeat(4,1fr);gap:3.5mm;margin-top:9mm}
.lg{height:33mm;background:#fff;border-radius:2.6mm;display:grid;place-items:center;padding:4mm 5mm}
.lg img{max-width:100%;max-height:22mm;object-fit:contain}
.lg--note{grid-column:span 3;background:linear-gradient(160deg,rgba(255,255,255,.14),rgba(255,255,255,.06));border:.3mm solid rgba(255,255,255,.3);box-shadow:none;place-items:start;align-content:center;padding:5mm 7mm}
.lg--note p{font-size:9.4pt;color:rgba(255,255,255,.92);margin-top:2mm;line-height:1.5}
.lg--note b{color:#fff;font-weight:600}
/* back */
.back__img{position:absolute;left:0;right:0;bottom:0;height:36%;width:100%;object-fit:cover}
.back__shade{position:absolute;inset:0;background:linear-gradient(180deg,transparent 64%,rgba(20,20,20,.18) 76%,rgba(20,20,20,.68) 100%)}
.back__body{margin-top:14mm}
.back__body .lead{margin:7mm 0 10mm;font-size:11pt;max-width:125mm}
.contact{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.contact .glass-d{padding:5mm 5.5mm}
.contact p{font-size:10pt;color:#fff;margin-top:2mm;line-height:1.45}
.qrbox{display:flex;gap:4mm;align-items:center}
.qrbox .qr{width:21mm;height:21mm;flex:none;background:#fff;padding:2mm;border-radius:1.6mm}
.qrbox p{margin-top:0}
.qrbox .label{display:flex;margin-bottom:1.6mm}
.back__foot{position:absolute!important;left:16mm;right:16mm;bottom:17mm;display:flex;align-items:flex-end;justify-content:space-between;gap:8mm;font-size:6.8pt;color:rgba(255,255,255,.9)}
.back__foot .logo{width:44mm;height:auto}
.back__foot span{text-align:right;max-width:80mm}
""".replace("FONTS ", FONTS)


def build():
    pages = [p_cover(), p_contents(), p_about(), p_values(), p_why(), p_services(), p_sectors(), p_map(),
             p_featured(), p_record(1), p_record(2), p_clients(), p_back()]
    html = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>FDSC Company Profile</title><style>{CSS}</style></head><body>
{''.join(pages)}
</body></html>"""
    open(OUT_HTML, "w").write(html)
    print("wrote", OUT_HTML, f"({len(pages)} pages)")
    return len(pages)


def render(preview=False):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1000, "height": 1400})
        pg.goto("file://" + OUT_HTML, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        # overflow check: any element sticking out of its page
        issues = pg.evaluate("""() => {
          const out = [];
          document.querySelectorAll('.page').forEach((p, i) => {
            const pr = p.getBoundingClientRect();
            p.querySelectorAll('h1,h2,h3,p,li,tr,.glass,.glass-d,.svc,.feat,.lg,.stat,.contact,.steps,.reasons,.chips,.logos').forEach(el => {
              const r = el.getBoundingClientRect();
              if (r.height && (r.bottom > pr.bottom - 58 || r.right > pr.right + 1)) out.push(`p${i + 1}: ${el.tagName}.${el.className} bottom ${Math.round(pr.bottom - r.bottom)}px`);
            });
          });
          return out.slice(0, 25);
        }""")
        for i in issues:
            print("  overflow?", i)
        pg.pdf(path=OUT_PDF, format="A4", print_background=True, prefer_css_page_size=True)
        if preview:
            prev = os.path.join(HERE, "previews")
            os.makedirs(prev, exist_ok=True)
            for i, el in enumerate(pg.query_selector_all(".page")):
                el.screenshot(path=os.path.join(prev, f"p{i + 1:02d}.png"))
        b.close()
    print("wrote", OUT_PDF, f"{os.path.getsize(OUT_PDF) / 1e6:.1f} MB")
    docs = os.path.join(ROOT, "website", "assets", "docs")
    os.makedirs(docs, exist_ok=True)
    shutil.copy(OUT_PDF, os.path.join(docs, os.path.basename(OUT_PDF)))


if __name__ == "__main__":
    build()
    render(preview="--preview" in sys.argv)
