"""Prepares photos and partner logos for the website and the company profile.

  photos:  _research/photos/*.jpg  ->  website/assets/img/<slug>-800.webp, <slug>-1600.webp
                                     company-profile/img/<slug>.jpg (2000 px, for print)
  logos:   _research/extracted/*.png (pulled from the client's two PDFs with `pdfimages -png`)
           -> website/assets/partners/<slug>.png (trimmed, 2x, white background)

Run:  python3 _tools/prepare_assets.py      (needs: pip install pillow numpy)
"""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PH = os.path.join(ROOT, "_research", "photos")
EX = os.path.join(ROOT, "_research", "extracted")
WEB = os.path.join(ROOT, "website", "assets", "img")
PRT = os.path.join(ROOT, "website", "assets", "partners")
PRO = os.path.join(ROOT, "company-profile", "img")
for d in (WEB, PRT, PRO):
    os.makedirs(d, exist_ok=True)

PHOTOS = {
    "hero-njombe": "cover-aerial-farmland-makete-njombe.jpg",
    "mbeya-plots": "cover-aerial-farmland-kyimo-mbeya-portrait.jpg",
    "njombe-fields": "cover-aerial-fields-njombe.jpg",
    "coffee": "coffee-cherries-hand-picking.jpg",
    "coffee-harvest": "coffee-women-harvesting.jpg",
    "community-meeting": "community-meeting-under-tree.jpg",
    "dar-harbour": "dar-es-salaam-harbour-aerial.jpg",
    "dar-skyline": "dar-es-salaam-skyline-cathedral.jpg",
    "field-discussion": "field-discussion-outdoor-interview.jpg",
    "seedling": "hands-seedling-uganda.jpg",
    "market-zanzibar": "horticulture-vegetable-market-zanzibar.jpg",
    "vegetables": "horticulture-woman-watering-vegetables-tanzania.jpg",
    "kilimanjaro": "kilimanjaro-maize-moshi.jpg",
    "evaluation-meeting": "professional-woman-evaluation-conference.jpg",
    "office-meeting": "professionals-women-office-meeting.jpg",
    "rice-harvest": "rice-farmer-harvesting.jpg",
    "rice-aerial": "rice-paddies-aerial-tanzania.jpg",
    "schoolgirls": "schoolgirls-arusha.jpg",
    "stone-town-girls": "schoolgirls-stone-town-zanzibar.jpg",
    "tea-farmer": "tea-farmer-rungwe-mbeya.jpg",
    "tea-hills": "tea-plantation-hills.jpg",
    "women-harvest": "women-carrying-harvest-arusha.jpg",
    "greens": "women-farmer-harvesting-greens-malawi.jpg",
    "women-group": "women-group-meeting-under-tree.jpg",
    "seaweed": "zanzibar-seaweed-farmers.jpg",
    "stone-town": "zanzibar-stone-town-aerial.jpg",
}

FULL_BLEED = {"hero-njombe", "tea-hills", "mbeya-plots"}

# (slug, image file, optional alpha mask file, display name)
LOGOS = [
    ("solidaridad", "p5-012.png", None, "Solidaridad East & Central Africa"),
    ("rikolto", "p5-013.png", None, "Rikolto"),
    ("helvetas", "p5-000.png", None, "HELVETAS Swiss Intercooperation"),
    ("tnc", "p6-008.png", None, "The Nature Conservancy"),
    ("trias", "p5-008.png", None, "Trias"),
    ("hanns-seidel", "p6-007.png", None, "Hanns Seidel Foundation"),
    ("govt-tanzania", "p5-015.png", None, "Government of Tanzania (Ministry of Finance and Planning)"),
    ("tbs", "p5-005.png", None, "Tanzania Bureau of Standards"),
    ("tacri", "p6-013.png", None, "Tanzania Coffee Research Institute"),
    ("trit", "p5-007.png", None, "Tea Research Institute of Tanzania"),
    ("sbt", "p6-004.png", None, "Sugar Board of Tanzania"),
    ("amdt", "p5-016.png", None, "Agricultural Markets Development Trust"),
    ("femina", "p6-015.png", "p6-016.png", "FEMINA Hip"),
    ("restless", "p5-003.png", None, "Restless Development"),
    ("thrdc", "p6-002.png", None, "Tanzania Human Rights Defenders Coalition"),
    ("songas", "p5-001.png", None, "Songas"),
    ("irdp", "p5-009.png", None, "Institute of Rural Development Planning"),
]


def save_photo(slug, fn):
    im = ImageOps.exif_transpose(Image.open(os.path.join(PH, fn))).convert("RGB")
    for w in (800, 1600):
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
        r.save(os.path.join(WEB, f"{slug}-{w}.webp"), "WEBP", quality=80, method=6)
    pw = 2000 if slug in FULL_BLEED else 1400          # print: >=240 dpi full-bleed, >=400 dpi in columns
    p = im.resize((pw, round(im.height * pw / im.width)), Image.LANCZOS) if im.width > pw else im
    p.save(os.path.join(PRO, f"{slug}.jpg"), quality=80, optimize=True, progressive=True)


def save_logo(slug, fn, mask_fn):
    im = Image.open(os.path.join(EX, fn)).convert("RGB")
    if mask_fn:  # composite on white using the PDF's soft mask
        m = Image.open(os.path.join(EX, mask_fn)).convert("L").resize(im.size)
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=m)
        im = bg
    a = np.array(im).astype(int)
    ink = (a.min(axis=2) < 235)
    ys, xs = np.where(ink)
    im = im.crop((max(xs.min() - 2, 0), max(ys.min() - 2, 0), min(xs.max() + 3, im.width), min(ys.max() + 3, im.height)))
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    im.save(os.path.join(PRT, f"{slug}.png"), optimize=True)
    im.save(os.path.join(PRT, f"{slug}.webp"), "WEBP", quality=90, method=6)
    im.save(os.path.join(PRO, f"logo-{slug}.jpg"), quality=90, optimize=True)   # print: small, sits on white tiles
    return im.size


if __name__ == "__main__":
    for slug, fn in PHOTOS.items():
        save_photo(slug, fn)
    print(f"photos: {len(PHOTOS)} -> {WEB} (webp) and {PRO} (jpg)")
    for slug, fn, mask, name in LOGOS:
        print("logo", slug, save_logo(slug, fn, mask))
