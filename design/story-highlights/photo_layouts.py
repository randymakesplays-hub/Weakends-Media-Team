#!/usr/bin/env python3
"""Four ways a photo can sit in a service-detail slide.

Rendered with a labelled placeholder zone so the layout is judged on its own,
before any real photograph exists. Swap PHOTO for a file path to test a shot.
"""
import os, subprocess, sys

from build import BLUE, INK, MUTED, TINT, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "photo-layouts")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
PHOTO = os.environ.get("CGD_PHOTO", "")   # optional real image to drop in

HEAD = 'Clay bar'
BODY = ('Pulls the embedded grit that washing physically cannot. Run your hand '
        'over the hood after and it feels like glass.')
SHOT = 'MACRO &#183; CLAY BAR ON WET PAINT'


def zone(cls):
    if PHOTO:
        return '<div class="%s" style="background-image:url(%s)"></div>' % (
            cls, "data:image/png;base64," + b64(PHOTO))
    return '<div class="%s ph"><span>%s</span></div>' % (cls, SHOT)


LAYOUTS = [
    ("a-band", "A · Band under the header", """
.photo{{flex:0 0 auto;height:620px;background-size:cover;background-position:center;}}
.body{{flex:1 1 auto;padding:60px 84px 250px;display:flex;flex-direction:column;
 justify-content:center;}}
""", lambda: zone("photo") + '<div class="body">%s</div>' % TEXT),

    ("b-full-bleed", "B · Full bleed behind the type", """
.stage{{flex:1 1 auto;position:relative;background-size:cover;
 background-position:center;}}
.scrim{{position:absolute;inset:0;background:linear-gradient(180deg,
 rgba(23,24,26,0.15) 0%, rgba(23,24,26,0.82) 62%, rgba(23,24,26,0.94) 100%);}}
.body{{position:absolute;left:0;right:0;bottom:0;padding:0 84px 250px;}}
.body .count{{color:#FFFFFF;opacity:0.6;}}
.body .h{{color:#FFFFFF;}}
.body .p{{color:rgba(255,255,255,0.88);}}
""", lambda: '<div class="stage%s"%s>%s<div class="body">%s</div></div>' % (
        "" if PHOTO else " ph",
        (' style="background-image:url(data:image/png;base64,%s)"' % b64(PHOTO))
        if PHOTO else "",
        '<div class="scrim"></div>' if PHOTO else "", TEXT)),

    ("c-window", "C · Framed window", """
.body{{flex:1 1 auto;padding:56px 84px 230px;display:flex;flex-direction:column;
 justify-content:center;}}
.photo{{height:520px;border-radius:30px;overflow:hidden;background-size:cover;
 background-position:center;margin-bottom:52px;}}
""", lambda: '<div class="body">%s%s</div>' % (zone("photo"), TEXT)),

    ("d-inset", "D · Square inset beside the number", """
.body{{flex:1 1 auto;padding:56px 84px 230px;display:flex;flex-direction:column;
 justify-content:center;}}
.photo{{width:380px;height:380px;border-radius:24px;overflow:hidden;
 background-size:cover;background-position:center;margin-bottom:46px;}}
""", lambda: '<div class="body">%s%s</div>' % (zone("photo"), TEXT)),
]

TEXT = ('<div class="count">04 / 06</div>'
        '<div class="h">%s</div><div class="p">%s</div>' % (HEAD, BODY))

BASE = """
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#FFFFFF;
 font-family:Archivo,Helvetica,sans-serif;color:{ink};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.frame{{width:1080px;height:1920px;display:flex;flex-direction:column;}}
.head{{flex:0 0 auto;padding:64px 84px 44px;display:flex;justify-content:center;}}
.head img{{width:236px;height:auto;display:block;}}
.bar{{flex:0 0 auto;height:10px;background:{blue};}}
.count{{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:{ink};opacity:0.42;}}
.h{{margin:24px 0 0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:82px;
 line-height:0.95;letter-spacing:-0.035em;color:{blue};text-transform:uppercase;}}
.p{{margin:34px 0 0;font:400 35px/1.38 Archivo,sans-serif;color:{ink};}}
.ph{{background:{tint};display:flex;align-items:center;justify-content:center;}}
.ph span{{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:0.14em;
 color:{blue};opacity:0.7;text-align:center;}}
"""


def page(css, inner, logo, faces):
    style = (BASE + css).format(faces=faces, ink=INK, blue=BLUE, tint=TINT,
                                muted=MUTED)
    head = ('<div class="head"><img src="%s" alt="Carolina Gloss Detailing"></div>'
            '<div class="bar"></div>' % logo)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style>'
            '</head><body><div class="frame">%s%s</div></body></html>'
            % (style, head, inner))


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "pl-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=8000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    for slug, _, css, build in LAYOUTS:
        shoot(page(css, build(), logo, faces), os.path.join(OUT, slug + ".png"))

    tiles = "".join(
        '<figure><img src="{s}.png"><figcaption>{n}</figcaption></figure>'.format(
            s=slug, n=name) for slug, name, _, _ in LAYOUTS)
    sheet = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1720px;background:#EFF1F4;display:flex;justify-content:center;
 gap:34px;padding:40px 34px;font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;}}
img{{width:380px;height:auto;display:block;border-radius:10px;
 box-shadow:0 6px 26px rgba(15,22,32,0.16);}}
figcaption{{font:700 20px Archivo,sans-serif;color:{ink};}}
</style></head><body>{tiles}</body></html>""".format(faces=faces, ink=INK, tiles=tiles)
    src = os.path.join(OUT, "_sheet.html")
    with open(src, "w") as fh:
        fh.write(sheet)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=9000", "--window-size=1720,900",
                    "--screenshot=" + os.path.join(OUT, "00-layouts.png"),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, "00-layouts.png"))


if __name__ == "__main__":
    main()
