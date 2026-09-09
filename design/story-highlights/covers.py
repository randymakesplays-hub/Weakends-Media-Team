#!/usr/bin/env python3
"""Render the Instagram story-highlight cover set.

Uploaded at 1080x1920 like any story, but Instagram crops a circle out of the
centre for the profile row. So the whole canvas is brand blue rather than a
drawn circle: whatever Instagram crops, it lands inside the fill and nothing
clips. The icon sits dead centre, well inside the crop.

One system for every highlight: same ground, same icon weight, same size.
Only the glyph changes. Run `python3 covers.py` for the set plus a contact
sheet showing how the row reads on the profile.
"""
import os, subprocess, sys

from build import BLUE, INK, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "covers")
TMP = os.environ.get("CGD_TMP", "/tmp/claude-0/-home-user-Weakends-Media-Team/"
                     "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")

# Icons live on a 120x120 grid, white on the blue ground. Strokes are heavy and
# shapes solid on purpose: the row renders about 60px wide on a phone, where
# hairlines disappear.
S = 'fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"'
STAR = ("60.0,14.0 71.2,44.6 103.7,45.8 78.1,65.9 87.0,97.2 60.0,79.0 33.0,97.2 "
        "41.9,65.9 16.3,45.8 48.8,44.6")

COVERS = [
    ("packages", "PACKAGES",
     '<rect x="34" y="24" width="52" height="16" rx="8" fill="#FFFFFF"/>'
     '<rect x="22" y="52" width="76" height="16" rx="8" fill="#FFFFFF"/>'
     '<rect x="10" y="80" width="100" height="16" rx="8" fill="#FFFFFF"/>'),
    ("location", "LOCATION",
     '<path d="M60 110 C60 110 22 74 22 48 A38 38 0 1 1 98 48 C98 74 60 110 60 110 Z" %s/>'
     '<circle cx="60" cy="47" r="14" %s/>' % (S, S)),
    ("reviews", "REVIEWS",
     '<polygon points="%s" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="9" '
     'stroke-linejoin="round"/>' % STAR),
    ("before-after", "BEFORE / AFTER",
     '<circle cx="60" cy="60" r="42" %s/>'
     '<path d="M60 18 A42 42 0 0 1 60 102 Z" fill="#FFFFFF"/>' % S),
    ("book", "BOOK",
     '<rect x="36" y="14" width="48" height="92" rx="12" %s/>'
     '<circle cx="60" cy="90" r="5" fill="#FFFFFF"/>' % S),
    ("faq", "FAQ",
     '<path d="M22 26 h76 a14 14 0 0 1 14 14 v34 a14 14 0 0 1 -14 14 h-30 '
     'l-20 18 v-18 h-26 a14 14 0 0 1 -14 -14 v-34 a14 14 0 0 1 14 -14 Z" %s/>'
     '<text x="60" y="74" text-anchor="middle" fill="#FFFFFF" '
     'font-family="Archivo Black, Helvetica, sans-serif" font-size="46">?</text>' % S),
]


def page(icon, faces):
    return """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:{blue};
 display:flex;align-items:center;justify-content:center;}}
svg{{width:360px;height:360px;display:block;}}
</style></head><body>
<svg viewBox="0 0 120 120">{icon}</svg>
</body></html>""".format(faces=faces, blue=BLUE, icon=icon)


def sheet(faces):
    """How the six read side by side at profile size, on Instagram's white."""
    circles = "".join(
        '<figure><div class="c"><svg viewBox="0 0 120 120">{i}</svg></div>'
        '<figcaption>{l}</figcaption></figure>'.format(i=icon, l=label)
        for _, label, icon in COVERS)
    return """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:420px;background:#FFFFFF;display:flex;
 align-items:center;justify-content:center;gap:34px;
 font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;}}
.c{{width:132px;height:132px;border-radius:50%;background:{blue};
 display:flex;align-items:center;justify-content:center;}}
.c svg{{width:74px;height:74px;display:block;}}
figcaption{{font:600 17px Archivo,sans-serif;color:{ink};letter-spacing:0.04em;
 text-align:center;}}
</style></head><body>{circles}</body></html>""".format(
        faces=faces, blue=BLUE, ink=INK, circles=circles)


def shoot(html, path, w, h):
    src = os.path.join(TMP, "cover-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=6000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    faces = font_faces()
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug, _, icon in COVERS:
        if only and slug not in only:
            continue
        shoot(page(icon, faces), os.path.join(OUT, slug + ".png"), 1080, 1920)
    shoot(sheet(faces), os.path.join(OUT, "00-row-preview.png"), 1080, 420)


if __name__ == "__main__":
    main()
