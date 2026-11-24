# FDSC: brand, company profile and website (Draft 1)

**Firm:** Frontline Development Services Consulting Limited (FDSC) · **Domain:** www.fdsc.co.tz
**Office:** Victoria Noble Centre, Plot No. 89, Block 45B, Kinondoni · P.O. Box 105471, Dar es Salaam
**Phone / WhatsApp:** +255 786 266 441 · **Email:** info@fdsc.co.tz, fdscltd@gmail.com

## What's here

| Folder | Contents |
|---|---|
| `company-profile/FDSC-Company-Profile-2026.pdf` | 13-page A4 portrait company profile. Page previews in `company-profile/previews/` |
| `website/` | Static website, ready to upload: Home, About, Services, Our work (map + filterable record of all 28 assignments), Contact, 404 |
| `brand/logo/svg/` | Logo rebuilt as clean vectors: full logo (colour, reversed, black, white), wordmark without tagline, S-disc mark, app icon, favicon |
| `brand/logo/png/`, `brand/logo/webp/` | Transparent PNG and WebP exports at 600 / 1200 / 2400 px (marks 256-1024 px), favicon.ico |
| `DRAFT-1-NOTES.md` | What we changed and what we need from FDSC |
| `_research/` | Source material: the client's two PDFs' images, downloaded photos (with credits), map data, logo comparison |
| `_tools/` | Build scripts (logo, assets, map, fonts, checks) |

## Identity

- **Logo:** recreated from the 454 px JPEG in the Word profile. Exact circle, traced S swoosh (true cut-out, works on any background), redrawn F/D/C, tagline set in Arial and outlined. Side-by-side check: `_research/logo-compare.png`.
- **Colours (red and white only):** FDSC Red `#C23C47` (sampled from the logo) · Deep red `#962733` (gradients, hover) · red for small text on white `#B0303B` · Blush `#FCEEEF` (tints) · White `#FFFFFF` · Ink `#141414` (body text, as in the logo's letters) · Grey `#5F5F5F` (secondary text)
- **Type:** Space Grotesk (headings, figures) + Instrument Sans (text). Free Google Fonts, self-hosted in `website/assets/fonts/`.
- **Signature elements:** the S-disc mark on every page; a dot-matrix map of Tanzania with the regions FDSC has worked in shown in red.

## Editing

All facts (services, values, assignments, clients, contacts) live in **one file**: `website/_src/content.py`. The website and the PDF both read from it.

- Website: `python3 website/_src/build.py`
- Company profile: `python3 company-profile/build_profile.py --preview` (needs Google Chrome + `pip install playwright segno pillow`). It also copies the PDF to `website/assets/docs/` for the download buttons.
- Logo: `python3 _tools/build_logo.py` then `python3 _tools/export_logo.py`
- Photos and partner logos: `python3 _tools/prepare_assets.py` (photo list and slugs at the top of the script)
- Map: `python3 _tools/build_map.py` (regions are highlighted automatically from the `regions` of each assignment)
- Social share image: `python3 _tools/make_og.py`
- Site QA (overflow, broken images, tap targets, console errors; desktop/phone/320 px): `python3 _tools/check_site.py --shots`

## Previewing the website

```
cd website && python3 -m http.server 8800
```
then open http://127.0.0.1:8800.

## Publishing

Upload the contents of `website/` (except `_src/`) to the web root of fdsc.co.tz on any host (cPanel, Vercel, Netlify). The enquiry form opens the visitor's email app addressed to info@fdsc.co.tz, so no server code is needed.

## Photos

All photos are free-licence (Pexels / Unsplash). Credits and locations: `website/assets/img/PHOTO-CREDITS.md`. Five are from neighbouring countries (Malawi, Uganda, likely Ethiopia) and are used without a Tanzanian caption. Replace with FDSC's own fieldwork photos when available.
