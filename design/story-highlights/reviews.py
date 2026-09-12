#!/usr/bin/env python3
"""Three concepts for the Reviews highlight, rendered at story size.

Every word is verbatim from a real Google review on carolinaglossdetailing.com,
with the reviewer's own name, review count and date intact. Nothing is smoothed
or shortened — the oddly specific phrases are what make a review read as real,
so "cup holders and vents" stays in.

Headline number is 5.0 from 33 reviews, per the Google Business Profile.
"""
import math, os, subprocess, sys

from build import BLUE, INK, TINT, RULE, MUTED, PHONE, CHROME, b64, font_faces

# Google's own four-colour G. The one mark on the slide that buys credibility.
GOOGLE_G = (
    '<svg class="gmark" viewBox="0 0 48 48" width="{s}" height="{s}" aria-hidden="true">'
    '<path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8'
    'c-6.627,0-12-5.373-12-12s5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657'
    'C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24s8.955,20,20,20s20-8.955,20-20'
    'C44,22.659,43.862,21.35,43.611,20.083z"/>'
    '<path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12'
    'c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4'
    'C16.318,4,9.656,8.337,6.306,14.691z"/>'
    '<path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238'
    'C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025'
    'C9.505,39.556,16.227,44,24,44z"/>'
    '<path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571'
    'l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/></svg>')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "reviews")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")

RATING, COUNT = "5.0", 33

REVIEWS = [
    dict(name="Starr Cotton", meta="Local Guide · 30 reviews", when="3 weeks ago",
         text="Great experience from start to finish. Prompt, professional, and "
              "transparent about what my car needed. They removed deep stains from "
              "the seats that I thought were permanent. Worth every penny!",
         pull="They removed deep stains from the seats that I thought were permanent."),
    dict(name="Jahmek Bracey", meta="2 reviews", when="4 weeks ago",
         text="Dallas did an outstanding job detailing my car. The attention to "
              "detail was incredible, it honestly looked better than when I first "
              "got it. Every inch of the interior was spotless, from the carpets "
              "and seats to the cup holders and vents.",
         pull="It honestly looked better than when I first got it."),
    dict(name="Salena Duffy", meta="8 reviews", when="4 weeks ago",
         text="This is top-of-the-line service. My husband gifted me with a detail "
              "for Mother's Day! He arrived on time at my home, and it was "
              "professional from beginning to end!",
         pull="He arrived on time at my home."),
    dict(name="biana", meta="2 reviews", when="5 months ago",
         text="I just bought my car used off Craigslist and Dallas really brought "
              "it back to life!! Dealership quality and reasonably priced at that.",
         pull="Dealership quality and reasonably priced at that."),
    dict(name="Tyler Spikes", meta="2 reviews", when="a week ago",
         text="If I could give more than 5 stars I would. Not only does my car look "
              "like a brand new vehicle, the professionalism and quality is top "
              "tier. The communication was great.",
         pull="If I could give more than 5 stars I would."),
]


def star(size, colour):
    pts = []
    for i in range(10):
        r = 11 if i % 2 == 0 else 4.6
        a = math.pi * 2 * i / 10 - math.pi / 2
        pts.append("%.1f,%.1f" % (12 + r * math.cos(a), 12 + r * math.sin(a)))
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true">'
            '<polygon points="%s" fill="%s"/></svg>' % (size, size, " ".join(pts), colour))


def stars(size=26, colour=None):
    return ('<span class="stars">' + star(size, colour or BLUE) * 5 + "</span>")


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
/* Everything sits optically centred, biased up out of Instagram's bottom UI. */
.body{{flex:1 1 auto;padding:84px 84px 210px;display:flex;flex-direction:column;
 justify-content:center;}}
.eyebrow{{font:500 25px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 text-transform:uppercase;color:{ink};opacity:0.45;}}
.stars{{display:inline-flex;gap:5px;align-items:center;}}

/* A — the receipt */
.card{{margin-top:36px;border:2px solid {rule};border-radius:26px;padding:44px 42px;}}
.who{{display:flex;gap:20px;align-items:center;}}
.av{{width:74px;height:74px;border-radius:50%;background:{blue};color:#FFFFFF;
 display:grid;place-items:center;font:700 32px Archivo,sans-serif;flex:0 0 auto;}}
.who .id b{{display:block;font:700 32px Archivo,sans-serif;}}
.who .id span{{display:block;margin-top:4px;font:400 23px 'IBM Plex Mono',monospace;
 color:{muted};}}
.rate{{margin-top:26px;display:flex;align-items:center;gap:16px;}}
.rate .when{{font:400 23px 'IBM Plex Mono',monospace;color:{muted};}}
.quote{{margin-top:26px;font:400 34px/1.42 Archivo,sans-serif;}}
.verified{{margin-top:40px;display:flex;align-items:center;gap:14px;
 font:500 24px 'IBM Plex Mono',monospace;color:{muted};}}

/* B — the pull quote */
.mark{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:150px;
 line-height:0.6;color:{blue};height:96px;}}
.pull{{margin-top:14px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:88px;line-height:0.98;letter-spacing:-0.035em;color:{ink};}}
.attrib{{margin-top:54px;padding-top:32px;border-top:3px solid {rule};
 display:flex;align-items:center;gap:20px;}}
.attrib .id b{{display:block;font:700 30px Archivo,sans-serif;}}
.attrib .id span{{display:block;margin-top:3px;font:400 22px 'IBM Plex Mono',monospace;
 color:{muted};}}
.gmark{{display:block;flex:0 0 auto;}}
.proof{{margin-top:26px;display:flex;align-items:center;gap:16px;
 font:500 25px 'IBM Plex Mono',monospace;color:{muted};}}

/* close — the only slide that asks for the booking */
.ask{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:104px;line-height:0.94;
 letter-spacing:-0.035em;}}
.ask em{{font-style:normal;color:{blue};}}
.sub{{margin-top:28px;font:400 36px/1.4 Archivo,sans-serif;color:{muted};}}
.cta{{margin-top:52px;background:{blue};border-radius:28px;padding:38px 28px;
 text-align:center;}}
.cta .lbl{{font:500 21px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:#FFFFFF;opacity:0.9;}}
.cta .num{{margin-top:8px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:62px;letter-spacing:-0.02em;color:#FFFFFF;}}

/* C — the number */
.big{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:250px;
 line-height:0.82;letter-spacing:-0.05em;color:{blue};}}
.from{{margin-top:26px;font:400 38px/1.3 Archivo,sans-serif;}}
.from b{{font-weight:700;}}
.mini{{margin-top:52px;display:flex;flex-direction:column;gap:20px;}}
.mini div{{background:{tint};border-radius:22px;padding:26px 30px;}}
.mini p{{margin:0;font:400 27px/1.36 Archivo,sans-serif;}}
.mini small{{display:block;margin-top:10px;font:400 21px 'IBM Plex Mono',monospace;
 color:{muted};}}
"""


def frame(inner, logo, crest=False):
    head = ('<div class="head"><img src="%s" alt="Carolina Gloss Detailing"></div>'
            % logo) if crest else ""
    return ('<div class="frame">%s<div class="bar"></div>'
            '<div class="body%s">%s</div></div>'
            % (head, "", inner))


def page(inner, logo, faces, crest=False):
    style = CSS.format(faces=faces, ink=INK, blue=BLUE, tint=TINT, rule=RULE, muted=MUTED)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style>'
            '</head><body>%s</body></html>' % (style, frame(inner, logo, crest)))


def concept_a():
    r = REVIEWS[0]
    return ('<div class="eyebrow">Google review</div>'
            '<div class="card">'
            '<div class="who"><span class="av">S</span>'
            '<span class="id"><b>{name}</b><span>{meta}</span></span></div>'
            '<div class="rate">{stars}<span class="when">{when}</span></div>'
            '<p class="quote">{text}</p></div>'
            '<div class="verified">{s2} 5.0 from 33 reviews on Google</div>'
            ).format(stars=stars(30), s2=star(24, BLUE), **r)


def pull_size(text):
    """Short quotes get bigger type, so every slide fills the frame the same."""
    n = len(text)
    return 132 if n <= 35 else 112 if n <= 55 else 96 if n <= 75 else 84


def pullquote(r):
    return ('<div class="mark">&ldquo;</div>'
            '<div class="pull" style="font-size:{size}px">{pull}</div>'
            '<div class="attrib">{gmark}'
            '<span class="id"><b>{name}</b><span>{meta}</span></span></div>'
            '<div class="proof">{stars} {rating} from {count} reviews on Google</div>'
            ).format(stars=stars(24), gmark=GOOGLE_G.format(s=54),
                     size=pull_size(r["pull"]), rating=RATING, count=COUNT, **r)


def open_slide():
    return ('<div class="eyebrow">What people say</div>'
            '<div class="big">{rating}</div>'
            '<div class="rate" style="margin-top:22px">{stars}</div>'
            '<p class="from">from <b>{count} reviews</b> on Google</p>'
            '<div class="proof">{gmark} Every word on these slides is theirs</div>'
            ).format(stars=stars(40), gmark=GOOGLE_G.format(s=40),
                     rating=RATING, count=COUNT)


def close_slide():
    return ('<div class="ask">Your turn.<br><em>Book it.</em></div>'
            '<p class="sub">Mobile detailing across Charlotte, Greensboro '
            'and Shelby. We come to you.</p>'
            '<div class="cta"><div class="lbl">CALL OR TEXT</div>'
            '<div class="num">{phone}</div></div>').format(phone=PHONE)


def concept_b():
    return pullquote(REVIEWS[0])


def verify():
    """Every pull has to appear in the reviewer's own text, case aside."""
    bad = [r["name"] for r in REVIEWS
           if r["pull"].rstrip(".!").lower() not in r["text"].lower()]
    if bad:
        sys.exit("pull quote not found in review text: " + ", ".join(bad))


def concept_c():
    minis = "".join(
        '<div><p>&ldquo;{pull}&rdquo;</p><small>{name} &middot; {meta}</small></div>'.format(**r)
        for r in REVIEWS[1:4])
    return ('<div class="eyebrow">What people say</div>'
            '<div class="big">5.0</div>'
            '<div class="rate" style="margin-top:22px">{stars}</div>'
            '<p class="from">from <b>33 reviews</b> on Google</p>'
            '<div class="mini">{minis}</div>').format(stars=stars(40), minis=minis)


CONCEPTS = [
    ("a-receipt", "A · The receipt", concept_a, False),
    ("b-pullquote", "B · The pull quote", concept_b, False),
    ("c-number", "C · The number", concept_c, True),
]


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "rev-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=7000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def sheet_of(items, out, faces):
    """Contact sheet of already-rendered PNGs. items is (slug, caption) pairs."""
    tile = 390 if len(items) <= 3 else 210
    tiles = "".join(
        '<figure><img src="{s}.png"><figcaption>{n}</figcaption></figure>'.format(s=s, n=n)
        for s, n in items)
    width = len(items) * (tile + 34) + 34
    sheet = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:{width}px;background:#EFF1F4;display:flex;justify-content:center;gap:34px;
 padding:40px 34px;font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;}}
img{{width:{tile}px;height:auto;display:block;border-radius:10px;
 box-shadow:0 6px 26px rgba(15,22,32,0.16);}}
figcaption{{font:700 18px Archivo,sans-serif;color:{ink};}}
</style></head><body>{tiles}</body></html>""".format(
        faces=faces, ink=INK, tiles=tiles, width=width, tile=tile)
    src = os.path.join(OUT, "_sheet-" + out.replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(sheet)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=9000",
                    "--window-size=%d,%d" % (width, tile * 1920 // 1080 + 130),
                    "--screenshot=" + os.path.join(OUT, out),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, out))


def main():
    verify()
    os.makedirs(OUT, exist_ok=True)
    logo = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    for slug, _, build, crest in CONCEPTS:
        shoot(page(build(), logo, faces, crest), os.path.join(OUT, slug + ".png"))

    # The shipping set: open on the number, five quotes, close on the booking.
    slides = ([("00-open", open_slide(), True)]
              + [("%02d-%s" % (i, r["name"].split()[0].lower()), pullquote(r), False)
                 for i, r in enumerate(REVIEWS, 1)]
              + [("06-close", close_slide(), True)])
    for slug, inner, crest in slides:
        shoot(page(inner, logo, faces, crest), os.path.join(OUT, "set-" + slug + ".png"))
    sheet_of([("set-" + s, s.split("-", 1)[1].title()) for s, _, _ in slides],
             "00-set.png", faces)

    sheet_of([(s, n) for s, n, _, _ in CONCEPTS], "00-concepts.png", faces)


if __name__ == "__main__":
    main()
