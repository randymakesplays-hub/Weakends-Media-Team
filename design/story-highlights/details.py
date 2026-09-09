#!/usr/bin/env python3
"""Render the service-detail highlight, in the style chosen from faq_concepts.

Eight slides. An opener, six steps, a close. Each slide takes one thing that
actually happens to the car and says why it matters, rather than asking and
answering a question.

Every line is lifted from the package pages on carolinaglossdetailing.com and
tightened. Nothing here claims a duration, a deposit policy or a ceramic
coating: none are established, and Deluxe carries ceramic soap, not a coating.
"""
import os, subprocess, sys

from build import BLUE, INK, MUTED, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "details")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
PHONE = "980·690·5259"

STEPS = [
    ("hand", "Hand washed, hand finished",
     "No machines. No brushes. Two mitts and clean water, the way paint is "
     "supposed to be washed."),
    ("two-bucket", "Two buckets, two mitts",
     "Dirt goes in a separate bucket, never back onto your paint. It is the "
     "difference between clean and scratched."),
    ("wheels", "Wheels, tires and trim",
     "The part every drive-thru wash skips. Brake dust out of the barrels, "
     "trim back to black."),
    ("clay", "Clay bar",
     "Pulls the embedded grit that washing physically cannot. Run your hand "
     "over the hood after and it feels like glass."),
    ("extraction", "Hot water extraction",
     "Water goes in and comes back out with the stain. Coffee, dog, kids, "
     "gym bag. Gone, not covered up."),
    ("seal", "Strip, then seal",
     "Old wax and road film come off first, so the new protection bonds to "
     "the paint instead of sitting on top of it."),
]

CSS = """
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#FFFFFF;
 font-family:Archivo,Helvetica,sans-serif;color:{ink};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.frame{{width:1080px;height:1920px;display:flex;flex-direction:column;}}
.head{{flex:0 0 auto;padding:74px 84px 52px;display:flex;justify-content:center;}}
.head img{{width:264px;height:auto;display:block;}}
.bar{{flex:0 0 auto;height:10px;background:{blue};}}
.body{{flex:1 1 auto;padding:70px 84px 250px;display:flex;flex-direction:column;
 justify-content:center;}}
.count{{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:{ink};opacity:0.42;}}
.q{{margin:28px 0 0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:88px;
 line-height:0.94;letter-spacing:-0.035em;color:{blue};text-transform:uppercase;}}
.a{{margin:44px 0 0;font:400 37px/1.38 Archivo,sans-serif;color:{ink};}}
.mark{{margin-top:52px;width:108px;height:10px;background:{blue};}}
.lead{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:104px;
 line-height:0.92;letter-spacing:-0.035em;color:{blue};text-transform:uppercase;}}
.sub{{margin:40px 0 0;font:400 38px/1.36 Archivo,sans-serif;color:{ink};}}
.hint{{margin:56px 0 0;font:500 25px 'IBM Plex Mono',monospace;
 letter-spacing:0.1em;color:{muted};}}
.cta{{margin-top:56px;background:{blue};border-radius:28px;padding:36px 28px;
 display:flex;flex-direction:column;align-items:center;text-align:center;}}
.cta .lbl{{font:500 21px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:#FFFFFF;opacity:0.88;}}
.cta .num{{margin-top:8px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:62px;line-height:1;letter-spacing:-0.02em;color:#FFFFFF;
 white-space:nowrap;}}
"""


def frame(logo, inner):
    return ('<div class="frame"><div class="head">'
            '<img src="%s" alt="Carolina Gloss Detailing"></div>'
            '<div class="bar"></div><div class="body">%s</div></div>' % (logo, inner))


def page(inner, logo, faces):
    style = CSS.format(faces=faces, ink=INK, blue=BLUE, muted=MUTED)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style>'
            '</head><body>%s</body></html>' % (style, frame(logo, inner)))


def slides():
    out = [("00-open",
            '<div class="lead">The<br>standard</div>'
            '<div class="sub">What actually happens to your car, step by step, '
            'and why each one matters.</div>'
            '<div class="hint">TAP THROUGH &#8250;</div>')]
    for i, (slug, head, body) in enumerate(STEPS, 1):
        out.append(("%02d-%s" % (i, slug),
                    '<div class="count">%02d / %02d</div>'
                    '<div class="q">%s</div>'
                    '<div class="a">%s</div><div class="mark"></div>'
                    % (i, len(STEPS), head, body)))
    out.append(("07-close",
                '<div class="lead">Built around<br>your car</div>'
                '<div class="sub">Every vehicle is different, so your detail is built '
                'around yours. Tell us what you drive.</div>'
                '<div class="cta"><div class="lbl">CALL OR TEXT</div>'
                '<div class="num">%s</div></div>' % PHONE))
    return out


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "det-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=6000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    built = slides()
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug, inner in built:
        if only and slug not in only:
            continue
        shoot(page(inner, logo, faces), os.path.join(OUT, slug + ".png"))

    tiles = "".join('<img src="%s.png">' % slug for slug, _ in built)
    sheet = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1640px;background:#EFF1F4;display:flex;flex-wrap:wrap;gap:26px;
 padding:34px;justify-content:center;}}
img{{width:372px;height:auto;display:block;border-radius:10px;
 box-shadow:0 6px 24px rgba(15,22,32,0.15);}}
</style></head><body>{tiles}</body></html>""".format(tiles=tiles)
    src = os.path.join(OUT, "_set.html")
    with open(src, "w") as fh:
        fh.write(sheet)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=9000", "--window-size=1640,1500",
                    "--screenshot=" + os.path.join(OUT, "00-set.png"),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, "00-set.png"))


if __name__ == "__main__":
    main()
