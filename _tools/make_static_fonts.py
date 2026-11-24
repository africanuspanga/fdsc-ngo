"""Makes fixed-weight TTFs from the variable web fonts, for the PDF.
(Chrome embeds variable fonts in PDFs as Type 3 glyph drawings: big files, poor for print shops.
Static TrueType instances embed as normal subset fonts.)

Run:  python3 _tools/make_static_fonts.py     -> company-profile/fonts/*.ttf
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "website", "assets", "fonts")
OUT = os.path.join(ROOT, "company-profile", "fonts")
os.makedirs(OUT, exist_ok=True)

JOBS = [("SpaceGrotesk-latin.woff2", "SpaceGrotesk", [300, 400, 500, 600]),
        ("InstrumentSans-latin.woff2", "InstrumentSans", [400, 500, 600, 700]),
        ("InstrumentSans-italic-latin.woff2", "InstrumentSans-Italic", [400])]

for fn, name, weights in JOBS:
    for w in weights:
        f = TTFont(os.path.join(SRC, fn))
        axes = {a.axisTag: a for a in f["fvar"].axes}
        loc = {"wght": w}
        if "wdth" in axes:
            loc["wdth"] = 100
        st = instancer.instantiateVariableFont(f, loc, updateFontNames=False)
        st.flavor = None
        out = os.path.join(OUT, f"{name}-{w}.ttf")
        st.save(out)
        print("wrote", os.path.basename(out), os.path.getsize(out) // 1024, "KB")
