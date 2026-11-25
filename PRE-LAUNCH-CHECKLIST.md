# FDSC website: pre-launch checklist

**Project:** fdsc.co.tz static website · **Date:** 25 November 2026 · **Checked against:** Pre-Launch Checklists 01-08 (09 Conversion & Monetization and 10 App Store do not apply: no product, pricing or app)

Key: ✅ done · ➕ added in this pass · ⬜ needs FDSC or the person deploying · N/A does not apply to this site

Re-run the automated checks after any change: `python3 website/_src/build.py && python3 _tools/check_site.py`. It serves the site with the real security headers and checks overflow at 1440/390/320 px, console errors (including CSP), broken images, tap targets, one `<h1>` per page, heading order and internal links/anchors. Current result: all 21 page/size combinations pass.

## 01 · Launch essentials

| Item | Status |
|---|---|
| Custom 404 page | ✅ `404.html`, branded, links home and to Contact, `noindex`. Vercel serves it automatically for unknown URLs |
| Privacy policy | ➕ `privacy.html` (linked in every footer, dated). ⬜ FDSC to read and approve the wording |
| Terms & conditions | N/A (no accounts, payments or user content) |
| Thank-you page | N/A (form opens the visitor's email app; on-page confirmation instead) |
| Real contact details | ✅ address, phone, WhatsApp, two emails, hours. ⬜ FDSC to confirm hours and which email the form uses (DRAFT-1-NOTES, Q8) |
| Cookie consent banner | N/A (no cookies; Vercel Web Analytics is cookieless if switched on) |
| Analytics installed | ⬜ Ready but off. Turn on Web Analytics for the project in Vercel, then set `ANALYTICS = True` in `website/_src/build.py` and rebuild |
| Conversion events | ➕ Wired up (call, WhatsApp, email, proposal buttons, PDF download, enquiry form). They start sending when analytics is on (custom events need a Vercel Pro plan) |
| Favicon set | ✅ `favicon.ico`, SVG favicon, 180 px apple-touch-icon, 192/512 manifest icons |
| Meta title + description per page | ➕ Shortened to 48-56 / 145-161 characters |
| Social preview image | ✅ 1200×630 `og-image.jpg`. ➕ width/height/alt and Twitter tags added. ⬜ Test by pasting the live URL into WhatsApp |
| One clear CTA per page; CTA above the fold | ✅ "Request a proposal" in the hero and header |
| Sticky mobile CTA | ➕ "Contact us" now stays in the sticky header on phones (hidden on the Contact page itself), plus the WhatsApp button |
| Form validation | ➕ Inline messages under each field, focus moves to the first problem, accepts any phone format |
| Loading state | N/A (nothing is sent to a server) |
| Success / error state | ➕ Confirmation note, plus a "Copy message" fallback for visitors with no email app (common on office PCs and webmail users) |
| Spam protection | N/A while the form uses the visitor's email app. Needed if FDSC later wants a server-side form |
| Submissions actually arrive | ⬜ Send a real test from a phone and a desktop after launch |
| HTTPS forced | ✅ Vercel does this. ➕ HSTS header added. ⬜ In Vercel → Domains, add `fdsc.co.tz` and redirect it to `www.fdsc.co.tz` (the canonical URLs use www) |
| Mobile friendly | ✅ Checked at 390 and 320 px. ⬜ Try on a real phone |
| Images compressed | ✅ WebP, 800/1600 px `srcset`, lazy below the fold |
| Alt text | ✅ Every image has alt text; decorative ones use `alt=""` |
| Colour contrast (AA) | ✅ Body grey 6.4:1, red text 6:1, white on red buttons 4.9:1 |
| Page speed | ⬜ Run PageSpeed Insights on the live URL (mobile) |
| No secrets in the frontend | ✅ None; static HTML only. ➕ `.env` patterns added to `.gitignore` |

## 02 · Polish & fixes

| Item | Status |
|---|---|
| No horizontal scroll / overflow at 320, 390, 1440 px | ✅ automated check |
| Mobile menu opens, closes, closes on tap, Esc | ✅ |
| Mobile menu traps focus | ➕ focus moves into the menu, Tab cycles inside it, Esc returns focus to the button |
| Breakpoints | ✅ 1440, 1020, 680, 390, 320 |
| Touch targets ≥ 44 px | ✅ automated check |
| No broken links | ➕ internal links and #anchors now checked automatically. External: wa.me, Google Maps |
| Footer links real, no dead nav items | ✅ |
| Logo links home; phone and email clickable | ✅ |
| No placeholder text | ✅ searched for lorem, ipsum, TODO, example.com, John Doe, 123-456 |
| Unique page titles | ✅ |
| Copyright year dynamic | ✅ JS sets the current year. ➕ build year written into the HTML too, so it shows without JS |
| Success / error messages | ➕ see Forms above |
| Favicon shows, custom 404 works | ✅ |
| No console errors | ✅ automated check, with the CSP header applied |
| Chrome, Safari, Firefox, iOS Safari | ⬜ Chrome checked automatically; check the others by hand after deploy |

## 03 · SEO

| Item | Status |
|---|---|
| No accidental `noindex` | ✅ only on `404.html` |
| `robots.txt` links the sitemap | ✅ |
| `sitemap.xml` lists every public page | ➕ privacy page added, `lastmod` dates added |
| Search Console and Bing Webmaster Tools | ⬜ verify the domain and submit `https://www.fdsc.co.tz/sitemap.xml` |
| Canonical tags | ✅ every page. ➕ removed from the 404 page |
| One version of the domain | ⬜ see HTTPS above |
| Title 50-60 / description 150-160 chars | ➕ fixed (Home, Services and Our work were too long) |
| Exactly one `<h1>`, no skipped heading levels | ➕ fixed: Services cards and footer headings were `<h3>` straight after an `<h1>`/`<h2>`; now checked automatically |
| Alt text, clean URLs, internal links | ✅ (`/services.html` style URLs, descriptive anchors) |
| Open Graph + Twitter tags | ➕ completed |
| Schema (JSON-LD) | ➕ `ProfessionalService` (hours, map, services), `WebSite`, `BreadcrumbList` on inner pages, `FAQPage` on Contact. ⬜ Check one page in Google's Rich Results Test after launch |
| Core Web Vitals | ⬜ after launch, in PageSpeed Insights / Search Console |
| Backlinks, Google Business Profile | ⬜ see 08 |

## 04 · Security (static site, so most items do not apply)

| Item | Status |
|---|---|
| API keys hidden, env vars, keys in git | ✅ none exist; git history scanned |
| `.env` in `.gitignore` | ➕ |
| HTTPS + HSTS | ➕ `Strict-Transport-Security: max-age=63072000` (no `includeSubDomains`, so FDSC's mail or cPanel subdomains are not affected) |
| Security headers | ➕ `Content-Security-Policy` (same-origin only), `Permissions-Policy`, plus the existing `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`. ⬜ Check the live site on securityheaders.com |
| Directory listing disabled | ✅ Vercel does not list directories |
| Auth, sessions, uploads, database, payments, rate limits, AI | N/A |

Note: the CSP blocks third-party scripts. If FDSC later adds a chat widget, map embed or another analytics tool, add its domain to `Content-Security-Policy` in `website/vercel.json`.

## 05 · Performance

| Item | Status |
|---|---|
| Images in WebP at display size, lazy loading | ✅ |
| JS/CSS size | ✅ one 31 KB stylesheet and one 10 KB script, served compressed by Vercel; no framework or bundle to split |
| Scripts deferred | ✅ |
| Fonts self-hosted, `font-display: swap`, subset, preloaded | ✅ |
| CDN + caching | ✅ Vercel CDN; `/assets/` cached 30 days, CSS/JS cache-busted with `?v=` |
| Lighthouse 90+ on mobile | ⬜ run on the live URL |
| Backend, database, API items | N/A |

## 06 · UX features

| Item | Status |
|---|---|
| Accessible mobile menu, sticky header, skip link | ✅ (focus trap ➕) |
| Back-to-top button | ➕ appears after 1.5 screens, sits above the WhatsApp button |
| Site search | N/A (the assignment record has its own search and filters) |
| Hover and `:focus-visible` styles, reduced motion | ✅ |
| Copy button | ➕ "Copy message" on the enquiry form |
| Form success / error states | ➕ |
| Expandable FAQ | ➕ six questions on the Contact page (`<details>`), built from the same facts as the rest of the site |
| "Last updated" on policies | ➕ privacy notice |
| Print stylesheet | ➕ hides navigation and buttons; useful for printing the assignment record |
| Floating contact button | ✅ WhatsApp |
| UTM tracking | ➕ UTM tags from the landing URL are added to the enquiry email ("Found FDSC via: ...") |
| Dark mode, cookie banner, password toggle, confirmation modals | N/A |

## 07 · UX laws (design review)

Five-item navigation and one primary action ("Request a proposal") on every page (Hick, Von Restorff). Logo top-left goes home, contact top-right (Jakob). Content is chunked into cards, steps and filters (Miller, proximity, common region). The enquiry form has four required fields and accepts any phone format (Parkinson, Postel). The page ends with a clear next step and a confirmation after sending (peak-end). No changes needed beyond the items above.

## 08 · AI & online visibility

| Item | Status |
|---|---|
| Website with About, Services, Contact, FAQ and schema | ➕ FAQ and FAQ schema added; the rest was there |
| `llms.txt` | ➕ `/llms.txt` (summary, key facts, links to every page and service, FAQ) and `/llms-full.txt` (full text and all 28 assignments). Both are generated from `content.py`, so they stay in step with the site |
| Google Business Profile, Google Maps, Bing Places, Apple Business Connect | ⬜ FDSC to claim. Use exactly: Frontline Development Services Consulting Limited · Natai Plaza, Coca-Cola Road, Dar es Salaam (P.O. Box 105471) · +255 786 266 441 · www.fdsc.co.tz |
| LinkedIn company page, Facebook | ⬜ FDSC: do they exist? Once they do, add the URLs (they go into the schema as `sameAs` and in the footer) |
| Directories, reviews, press | ⬜ Optional: client case mentions, Tanzanian business directories, AfrEA or EES evaluator listings |
| Wikipedia / Wikidata, YouTube, podcasts, Yelp, G2 etc. | N/A for now |
