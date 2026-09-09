#!/usr/bin/env python3
"""Render the Instagram story-highlight cover set.

Treatment C: white ground, black icon, Carolina blue ring.

Uploaded at 1080x1920 like any story, and Instagram crops a circle out of the
centre for the profile row. Exactly how wide that crop is has shifted over the
years, so the ring is drawn well inside the likely crop rather than out at its
edge. Because the ground and Instagram's profile are both white, a crop wider
than the ring just shows more white and still reads correctly. A ring sized to
the crop would clip the moment the crop tightened.

Proportions carry over from the approved comparison sheet: ring stroke about
4% of the ring diameter, icon about 42% of it.
"""
import os, subprocess, sys

from build import BLUE, INK, CHROME, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "covers")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")

RING = 520      # ring diameter on the 1080 canvas
STROKE = 22     # ring weight
ICON = 218      # icon box inside the ring


def icons(c):
    """The six glyphs drawn in colour `c`, on a shared 120x120 grid."""
    s = ('fill="none" stroke="%s" stroke-width="6.5" stroke-linecap="round" '
         'stroke-linejoin="round"' % c)
    return [
        ("services", "Services",
         '<path d="M60 20 L100 42 L60 64 L20 42 Z" %s/>'
         '<path d="M20 60 L60 82 L100 60" %s/>'
         '<path d="M20 78 L60 100 L100 78" %s/>' % (s, s, s)),
        ("location", "Location",
         '<path d="M60 104 C60 104 26 72 26 48 A34 34 0 1 1 94 48 C94 72 60 104 60 104 Z" %s/>'
         '<circle cx="60" cy="47" r="12" %s/>' % (s, s)),
        ("reviews", "Reviews",
         '<path d="M60 18 L73.4 45.2 L103.4 49.6 L81.7 70.7 L86.8 100.6 '
         'L60 86.5 L33.2 100.6 L38.3 70.7 L16.6 49.6 L46.6 45.2 Z" %s/>' % s),
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


def page(icon, faces):
    return """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#FFFFFF;
 display:flex;align-items:center;justify-content:center;}}
.ring{{width:{ring}px;height:{ring}px;border-radius:50%;background:#FFFFFF;
 box-shadow:inset 0 0 0 {stroke}px {blue};display:flex;align-items:center;
 justify-content:center;}}
.ring svg{{width:{icon}px;height:{icon}px;display:block;}}
</style></head><body>
<div class="ring"><svg viewBox="0 0 120 120">{i}</svg></div>
</body></html>""".format(faces=faces, ring=RING, stroke=STROKE, blue=BLUE,
                         icon=ICON, i=icon)


def sheet(faces):
    """How the six read side by side at profile size, on Instagram's white."""
    cells = "".join(
        '<figure><div class="c"><svg viewBox="0 0 120 120">{i}</svg></div>'
        '<figcaption>{l}</figcaption></figure>'.format(i=icon, l=label)
        for _, label, icon in icons(INK))
    return """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:340px;background:#FFFFFF;display:flex;
 align-items:center;justify-content:space-between;padding:0 46px;
 font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:14px;
 width:150px;}}
.c{{width:124px;height:124px;border-radius:50%;background:#FFFFFF;
 box-shadow:inset 0 0 0 5px {blue};display:flex;align-items:center;
 justify-content:center;}}
.c svg{{width:52px;height:52px;display:block;}}
figcaption{{font:600 15px Archivo,sans-serif;color:{ink};text-align:center;}}
</style></head><body>{cells}</body></html>""".format(
        faces=faces, blue=BLUE, ink=INK, cells=cells)


def shoot(html, path, w, h, scale=1):
    src = os.path.join(TMP, "cover-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=6000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    faces = font_faces()
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug, _, icon in icons(INK):
        if only and slug not in only:
            continue
        shoot(page(icon, faces), os.path.join(OUT, slug + ".png"), 1080, 1920)
    shoot(sheet(faces), os.path.join(OUT, "00-row-preview.png"), 1080, 340, scale=2)


if __name__ == "__main__":
    main()
