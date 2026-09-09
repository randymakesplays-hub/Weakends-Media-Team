#!/usr/bin/env python3
"""Render the FAQ highlight: concept B, objection killers.

Eight slides. An opener, six objections, a close. Every slide names the thing
that actually stops someone booking rather than the polite version of the
question, and answers it in one breath.

The block is vertically centred rather than top-aligned. Top-aligned left a
third of the frame empty under a short answer, which read as unfinished.

Every answer traces to carolinaglossdetailing.com. Nothing here claims a
duration, a deposit policy or a coating, because none of those are established.
"""
import os, subprocess, sys

from build import BLUE, INK, MUTED, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faq")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
PHONE = "980·690·5259"

OBJECTIONS = [
    ("embarrassing", "My car is embarrassing.",
     "We have seen worse this week. That is the job, not a judgment. You are not "
     "the first person to apologize for their back seat."),
    ("water-power", "I don’t have a hose or an outlet.",
     "You do not need one. The van brings its own water and power. All we need is "
     "the space around the car and the keys."),
    ("time", "I don’t have time to sit around.",
     "You do not have to. Hand over the keys and go back inside. We work in your "
     "driveway while you get on with your day."),
    ("stains", "Those stains are never coming out.",
     "Usually they are. Hot water extraction pulls the stain back out of the "
     "fabric instead of covering it. Send a photo first and we will be honest "
     "about what is coming out."),
    ("which-one", "I don’t know which one I need.",
     "Text a photo of your car. We will tell you straight, even when the answer "
     "is the cheapest one."),
    ("cost", "What is this going to cost me?",
     "Depends on the size of the vehicle and how rough it is. Tell us what you "
     "drive and we come back with your exact price, locked in before we touch "
     "the car."),
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
            '<div class="lead">Before you<br>book</div>'
            '<div class="sub">Six things people say before they hand over the keys, '
            'and the honest answer to each one.</div>'
            '<div class="hint">TAP THROUGH &#8250;</div>')]
    for i, (slug, q, a) in enumerate(OBJECTIONS, 1):
        out.append(("%02d-%s" % (i, slug),
                    '<div class="count">%02d / %02d</div>'
                    '<div class="q">&ldquo;%s&rdquo;</div>'
                    '<div class="a">%s</div><div class="mark"></div>'
                    % (i, len(OBJECTIONS), q, a)))
    out.append(("07-close",
                '<div class="lead">Still<br>wondering?</div>'
                '<div class="sub">Send a photo of your car and where you are parked. '
                'You get a straight answer and your exact price back.</div>'
                '<div class="cta"><div class="lbl">CALL OR TEXT</div>'
                '<div class="num">%s</div></div>' % PHONE))
    return out


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "faqb-" + os.path.basename(path).replace(".png", ".html"))
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
