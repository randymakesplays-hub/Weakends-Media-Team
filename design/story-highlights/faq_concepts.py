#!/usr/bin/env python3
"""Four visual concepts for the FAQ highlight, rendered at story size.

Copy here is placeholder to judge the layout by; the real lines come later.
All four keep the package-frame header so the highlight reads as one family.
"""
import os, subprocess, sys

from build import BLUE, INK, TINT, RULE, MUTED, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "faq")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")

HEAD = """<div class="head"><img src="{logo}" alt="Carolina Gloss Detailing"></div>
<div class="bar"></div>"""

BASE = """
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#FFFFFF;
 font-family:Archivo,Helvetica,sans-serif;color:{ink};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.frame{{width:1080px;height:1920px;display:flex;flex-direction:column;}}
.head{{flex:0 0 auto;padding:74px 84px 52px;display:flex;justify-content:center;}}
.head img{{width:264px;height:auto;display:block;}}
.bar{{flex:0 0 auto;height:10px;background:{blue};}}
.body{{flex:1 1 auto;padding:76px 84px 220px;display:flex;flex-direction:column;}}
.tag{{font:600 25px Archivo,sans-serif;letter-spacing:0.32em;color:{ink};
 opacity:0.45;}}
"""

CONCEPTS = [
    ("a-straight", "A · Straight Q&A", """
.q{{margin:26px 0 0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:82px;
 line-height:0.96;letter-spacing:-0.03em;color:{blue};text-transform:uppercase;}}
.a{{margin:38px 0 0;font:400 36px/1.4 Archivo,sans-serif;color:{ink};}}
.rule{{margin-top:56px;height:3px;background:{rule};}}
""", """<div class="tag">FAQ</div>
<div class="q">Do you come to me?</div>
<div class="a">That is the whole idea. Home, office, apartment lot. Wherever you
park, we pull up to it.</div>
<div class="rule"></div>"""),

    ("b-objections", "B · Objection killers", """
.q{{margin:26px 0 0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:88px;
 line-height:0.94;letter-spacing:-0.035em;color:{blue};text-transform:uppercase;}}
.a{{margin:44px 0 0;font:400 37px/1.38 Archivo,sans-serif;color:{ink};}}
.mark{{margin-top:52px;width:108px;height:10px;background:{blue};}}
""", """<div class="tag">YOU MIGHT BE THINKING</div>
<div class="q">&ldquo;My car is embarrassing.&rdquo;</div>
<div class="a">We have seen worse this week. That is the job, not a judgment.
Nobody is looking at your back seat except us.</div>
<div class="mark"></div>"""),

    ("c-text-thread", "C · Text thread", """
.thread{{margin-top:40px;display:flex;flex-direction:column;gap:26px;}}
.inb,.outb{{max-width:78%;padding:28px 32px;font:400 33px/1.36 Archivo,sans-serif;}}
.inb{{align-self:flex-start;background:{tint};color:{ink};
 border-radius:28px 28px 28px 8px;}}
.outb{{align-self:flex-end;background:{blue};color:#FFFFFF;
 border-radius:28px 28px 8px 28px;}}
.stamp{{margin-top:34px;text-align:center;font:500 24px 'IBM Plex Mono',monospace;
 letter-spacing:0.08em;color:{muted};}}
""", """<div class="tag">REAL QUESTIONS</div>
<div class="thread">
<div class="inb">Hey do you guys come out to Shelby?</div>
<div class="outb">Yep. Shelby, Greensboro and Charlotte. Send me your address and
what you drive.</div>
<div class="inb">Do I need to leave a hose out?</div>
<div class="outb">Nope, we bring our own water and power.</div>
</div>
<div class="stamp">TEXT 980&#183;690&#183;5259</div>"""),

    ("d-myth", "D · Myth vs truth", """
.myth{{margin-top:34px;background:{tint};border-radius:26px;padding:36px 38px;}}
.myth .lbl{{font:500 22px 'IBM Plex Mono',monospace;letter-spacing:0.14em;
 color:{ink};opacity:0.5;}}
.myth .t{{margin-top:14px;font:400 40px/1.24 Archivo,sans-serif;color:{ink};
 opacity:0.55;text-decoration:line-through;text-decoration-thickness:3px;}}
.truth{{margin-top:44px;}}
.truth .lbl{{font:500 22px 'IBM Plex Mono',monospace;letter-spacing:0.14em;
 color:{blue};}}
.truth .t{{margin-top:16px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:60px;line-height:1.0;letter-spacing:-0.03em;color:{ink};}}
.truth .s{{margin-top:26px;font:400 34px/1.38 Archivo,sans-serif;color:{muted};}}
""", """<div class="tag">FAQ</div>
<div class="myth"><div class="lbl">WHAT PEOPLE THINK</div>
<div class="t">The tunnel wash is fine.</div></div>
<div class="truth"><div class="lbl">WHAT ACTUALLY HAPPENS</div>
<div class="t">It is what put the swirls in your paint.</div>
<div class="s">Spinning brushes drag the last car's grit across yours. That is
the haze you see in direct sun.</div></div>"""),
]


def page(css, markup, logo, faces):
    style = (BASE + css).format(faces=faces, ink=INK, blue=BLUE, tint=TINT,
                                rule=RULE, muted=MUTED)
    return ("<!doctype html><html><head><meta charset=\"utf-8\"><style>%s</style>"
            "</head><body><div class=\"frame\">%s<div class=\"body\">%s</div>"
            "</div></body></html>" % (style, HEAD.format(logo=logo), markup))


def shoot(html, path, w, h, scale=1):
    src = os.path.join(TMP, "faq-" + os.path.basename(path).replace(".png", ".html"))
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
    for slug, _, css, markup in CONCEPTS:
        shoot(page(css, markup, logo, faces),
              os.path.join(OUT, slug + ".png"), 1080, 1920)

    # side by side, scaled down, for judging the four together
    tiles = "".join(
        '<figure><img src="{s}.png"><figcaption>{n}</figcaption></figure>'.format(
            s=slug, n=name) for slug, name, _, _ in CONCEPTS)
    sheet = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1720px;background:#EFF1F4;display:flex;justify-content:center;
 align-items:flex-start;gap:34px;padding:40px 34px;
 font-family:Archivo,Helvetica,sans-serif;}}
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
                    "--virtual-time-budget=8000", "--window-size=1720,900",
                    "--screenshot=" + os.path.join(OUT, "00-concepts.png"),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, "00-concepts.png"))


if __name__ == "__main__":
    main()
