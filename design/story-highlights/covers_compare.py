#!/usr/bin/env python3
"""Three ground treatments for the highlight covers, side by side at profile size.

Icons are redrawn for all three: finer strokes, more considered geometry, and
sized to about 42% of the circle instead of 63%. Filling the circle is most of
what made the first pass read cheap.
"""
import os, subprocess
from build import BLUE, INK, CHROME, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "covers")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")


def icons(c):
    """Icon set drawn in colour `c`. 120x120 grid, 6.5 stroke."""
    s = ('fill="none" stroke="%s" stroke-width="6.5" stroke-linecap="round" '
         'stroke-linejoin="round"' % c)
    return [
        # layered tiers, offset so it reads as depth rather than a menu glyph
        ("packages", "Packages",
         '<path d="M60 20 L100 42 L60 64 L20 42 Z" %s/>'
         '<path d="M20 60 L60 82 L100 60" %s/>'
         '<path d="M20 78 L60 100 L100 78" %s/>' % (s, s, s)),
        ("location", "Location",
         '<path d="M60 104 C60 104 26 72 26 48 A34 34 0 1 1 94 48 C94 72 60 104 60 104 Z" %s/>'
         '<circle cx="60" cy="47" r="12" %s/>' % (s, s)),
        ("reviews", "Reviews",
         '<path d="M60 18 L73.4 45.2 L103.4 49.6 L81.7 70.7 L86.8 100.6 '
         'L60 86.5 L33.2 100.6 L38.3 70.7 L16.6 49.6 L46.6 45.2 Z" %s/>' % s),
        # diagonal split reads as a transformation, not a battery level
        ("before-after", "Before / After",
         '<rect x="18" y="26" width="84" height="68" rx="10" %s/>'
         '<path d="M60 26 L60 94" %s/>'
         '<path d="M28 94 L28 36 A10 10 0 0 1 38 26 L60 26 L60 94 Z" fill="%s" '
         'stroke="none" opacity="0.9"/>' % (s, s, c)),
        ("book", "Book",
         '<rect x="22" y="28" width="76" height="70" rx="12" %s/>'
         '<path d="M22 50 L98 50" %s/><path d="M42 20 L42 36" %s/>'
         '<path d="M78 20 L78 36" %s/>'
         '<path d="M48 72 L57 81 L74 64" %s/>' % (s, s, s, s, s)),
        ("faq", "FAQ",
         '<circle cx="60" cy="60" r="40" %s/>'
         '<path d="M47 48 A13 13 0 1 1 60 68 L60 74" %s/>'
         '<path d="M60 88 L60 88.5" %s/>' % (s, s, s)),
    ]


TREATMENTS = [
    ("A", "Near-black circle, blue icon", INK, BLUE, None),
    ("B", "Blue circle, white icon", BLUE, "#FFFFFF", None),
    ("C", "White circle, black icon, blue ring", "#FFFFFF", INK, BLUE),
]


def row(label, note, bg, fg, ring):
    edge = ("box-shadow:inset 0 0 0 5px %s;" % ring) if ring else ""
    cells = "".join(
        '<figure><div class="c" style="background:{bg};{edge}">'
        '<svg viewBox="0 0 120 120">{i}</svg></div>'
        '<figcaption>{l}</figcaption></figure>'.format(bg=bg, edge=edge, i=icon, l=lab)
        for _, lab, icon in icons(fg))
    return ('<section><h2>{label} &nbsp;<span>{note}</span></h2>'
            '<div class="row">{cells}</div></section>').format(
                label=label, note=note, cells=cells)


def main():
    os.makedirs(OUT, exist_ok=True)
    sections = "".join(row(*t) for t in TREATMENTS)
    html = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;background:#FFFFFF;font-family:Archivo,Helvetica,sans-serif;
 padding:44px 40px 48px;}}
section{{margin-bottom:40px;}}
section:last-child{{margin-bottom:0;}}
h2{{margin:0 0 22px;font:700 20px Archivo,sans-serif;color:{ink};
 letter-spacing:0.02em;}}
h2 span{{font-weight:400;color:rgba(23,24,26,0.55);}}
.row{{display:flex;align-items:flex-start;justify-content:space-between;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:12px;
 width:150px;}}
.c{{width:118px;height:118px;border-radius:50%;display:flex;align-items:center;
 justify-content:center;}}
.c svg{{width:50px;height:50px;display:block;}}
figcaption{{font:600 14px Archivo,sans-serif;color:{ink};text-align:center;}}
</style></head><body>{sections}</body></html>""".format(
        faces=font_faces(), ink=INK, sections=sections)
    src = os.path.join(TMP, "covers-compare.html")
    with open(src, "w") as fh:
        fh.write(html)
    png = os.path.join(OUT, "00-treatments.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=6000", "--window-size=1080,860",
                    "--screenshot=" + png, "file://" + src], capture_output=True)
    print("wrote", png)


if __name__ == "__main__":
    main()
