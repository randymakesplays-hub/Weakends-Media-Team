#!/usr/bin/env python3
"""Four glyph options for the Services cover, shown at profile size."""
import os, subprocess
from build import BLUE, INK, CHROME, font_faces

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "covers")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
S = ('fill="none" stroke="%s" stroke-width="6.5" stroke-linecap="round" '
     'stroke-linejoin="round"' % INK)

OPTIONS = [
    ("Car", "the thing being serviced",
     '<path d="M14 76 L20 58 C22 51 27 47 34 47 L70 47 C76 47 81 49 85 54 '
     'L95 66 L102 68 C106 69 108 72 108 76 L108 82 L14 82 Z" %s/>'
     '<circle cx="36" cy="82" r="9" %s/><circle cx="86" cy="82" r="9" %s/>'
     % (S, S, S)),
    ("Spray bottle", "the work itself",
     '<rect x="40" y="44" width="40" height="60" rx="10" %s/>'
     '<path d="M52 44 L52 30 L42 30 L42 20 L66 20 L66 30 L60 30 L60 44" %s/>'
     '<path d="M78 26 L92 20" %s/><path d="M80 34 L95 32" %s/>'
     '<path d="M78 42 L92 44" %s/>' % (S, S, S, S, S)),
    ("Shine", "the result, and the brand word",
     '<path d="M58 18 L66 50 L98 58 L66 66 L58 98 L50 66 L18 58 L50 50 Z" %s/>'
     '<path d="M92 76 L95 88 L107 91 L95 94 L92 106 L89 94 L77 91 L89 88 Z" %s/>'
     % (S, S)),
    ("Layers", "what is there now",
     '<path d="M60 20 L100 42 L60 64 L20 42 Z" %s/>'
     '<path d="M20 60 L60 82 L100 60" %s/>'
     '<path d="M20 78 L60 100 L100 78" %s/>' % (S, S, S)),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    cells = "".join(
        '<figure><div class="c"><svg viewBox="0 0 120 120">{i}</svg></div>'
        '<figcaption><b>{n}</b><span>{d}</span></figcaption></figure>'.format(
            i=icon, n=name, d=note) for name, note, icon in OPTIONS)
    html = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:340px;background:#FFFFFF;display:flex;
 align-items:center;justify-content:space-around;
 font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;
 width:230px;}}
.c{{width:140px;height:140px;border-radius:50%;background:#FFFFFF;
 box-shadow:inset 0 0 0 6px {blue};display:flex;align-items:center;
 justify-content:center;}}
.c svg{{width:59px;height:59px;display:block;}}
figcaption{{display:flex;flex-direction:column;gap:5px;text-align:center;}}
figcaption b{{font:700 17px Archivo,sans-serif;color:{ink};}}
figcaption span{{font:400 14px Archivo,sans-serif;color:rgba(23,24,26,0.55);}}
</style></head><body>{cells}</body></html>""".format(
        faces=font_faces(), blue=BLUE, ink=INK, cells=cells)
    src = os.path.join(TMP, "services-options.html")
    open(src, "w").write(html)
    png = os.path.join(OUT, "00-services-options.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=6000", "--window-size=1080,340",
                    "--screenshot=" + png, "file://" + src], capture_output=True)
    print("wrote", png)


if __name__ == "__main__":
    main()
