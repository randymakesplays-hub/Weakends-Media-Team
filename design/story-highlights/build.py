#!/usr/bin/env python3
"""Render the three Carolina Gloss package stories to 1080x1920 PNGs.

One layout, three variants. Copy lives in PACKAGES; everything else is shared,
so the three images read as siblings. Fonts and the logo are base64 embedded
so each render page is self contained.
"""
import base64, glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONT_DIR = os.environ.get("CGD_FONTS", "/tmp/claude-0/-home-user-Weakends-Media-Team/"
                          "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad/fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# Palette sampled straight from assets/logo.png. Three colors, nothing else:
# white ground, neutral black type, and the Carolina blue that is 35% of the crest.
# The blue is too light for small text on white, so it only ever appears as a fill
# (pills, blocks, rules) with black on top of it.
INK = "#17181A"          # logo black, no blue cast
BLUE = "#79A9EE"         # logo Carolina blue
TINT = "#EDF3FD"         # BLUE washed into white, for cards
RULE = "#D7E5F8"         # BLUE washed into white, for dividers
MUTED = "rgba(23,24,26,0.62)"   # the same black, stepped back
BLUE_DEEP = "#4F86D9"    # a darker tone of BLUE, only to give the rosette depth

PHONE = "980\u00b7690\u00b75259"
CITIES = "CHARLOTTE \u00b7 GREENSBORO \u00b7 SHELBY"
PRICE_LINE = ("Priced on your vehicle size and condition. "
              "We lock that number in before we touch the car.")

PACKAGES = [
    dict(slug="01-standard", title="Standard", popular=False,
         sub="Your everyday fresh. Start the day in a clean car.",
         plus="WHAT YOU GET",
         rows=[("Hand wash, top to bottom", "Two mitts and clean water. No brushes, no swirl marks."),
               ("Wheels, tires and trim", "Brake dust out of the barrels, trim back to black."),
               ("Full interior vacuum", "Seats, rails, under the mats, and the trunk."),
               ("Glass, inside and out", "Streak free on both sides. You notice it driving at night."),
               ("Vinyl sanitized, leather refreshed", "Dash, doors, console and every vent wiped down.")],
         best="A car that gets cleaned regularly and just needs bringing back."),
    dict(slug="02-gloss", title="Gloss", popular=True,
         sub="The one everybody\u2019s actually looking for. A full in and out makeover.",
         plus="EVERYTHING IN STANDARD, PLUS",
         rows=[("Light clay bar", "Pulls the grit washing cannot reach. Run your hand over the hood after."),
               ("Hot water extraction", "Coffee, dog, kids, gym bag. Gone, not covered up."),
               ("Two bucket wash", "Dirt goes in its own bucket, never back onto your paint."),
               ("Leather and vinyl conditioned", "So it stops drying out and cracking in the Carolina sun."),
               ("Wheels and tires, second pass", "Faces, barrels and lug seats done properly, then dressed.")],
         best="Most people, and anyone whose car has not been detailed in a while."),
    dict(slug="03-deluxe", title="Deluxe", popular=False,
         sub="The final boss. Fresh, sealed, basically a brand new car.",
         plus="EVERYTHING IN GLOSS, PLUS",
         rows=[("Full clay bar", "The whole body decontaminated panel by panel, not a spot treatment."),
               ("Chemical strip wash", "Old wax and road film off so the new protection bonds."),
               ("Ceramic soap", "Lays down a slick layer. Water sheets straight off your paint."),
               ("Hand wax and spray sealant", "Months of protection against pollen, sun and road salt."),
               ("Interior shampooed and conditioned", "Comes back looking like a lease return.")],
         best="Selling it, gifting it, or you just love the thing."),
]


ROSETTE = ('<svg class="rosette" viewBox="0 0 240 262" aria-label="Number one most popular"><path d="M96 150 L126 150 L86 254 L71 238 L56 254 Z" fill="{deep}"/><path d="M144 150 L114 150 L154 254 L169 238 L184 254 Z" fill="{blue}"/><polygon points="120.0,14.0 129.4,30.6 142.5,16.7 147.7,35.1 163.7,24.8 164.3,43.8 182.3,37.6 178.4,56.3 197.4,54.6 189.1,71.8 207.9,74.7 195.7,89.3 213.3,96.7 198.0,108.0 213.3,119.3 195.7,126.7 207.9,141.3 189.1,144.2 197.4,161.4 178.4,159.7 182.3,178.4 164.3,172.2 163.7,191.2 147.7,180.9 142.5,199.3 129.4,185.4 120.0,202.0 110.6,185.4 97.5,199.3 92.3,180.9 76.3,191.2 75.7,172.2 57.7,178.4 61.6,159.7 42.6,161.4 50.9,144.2 32.1,141.3 44.3,126.7 26.7,119.3 42.0,108.0 26.7,96.7 44.3,89.3 32.1,74.7 50.9,71.8 42.6,54.6 61.6,56.3 57.7,37.6 75.7,43.8 76.3,24.8 92.3,35.1 97.5,16.7 110.6,30.6" fill="{blue}"/><circle cx="120" cy="108" r="78" fill="{deep}"/><circle cx="120" cy="108" r="60" fill="{blue}" stroke="#FFFFFF" stroke-width="5"/><text x="120" y="99" text-anchor="middle" fill="#FFFFFF" font-family="Archivo Black, Helvetica, sans-serif" font-size="46">#1</text><text x="120" y="129" text-anchor="middle" fill="#FFFFFF" font-family="Archivo, Helvetica, sans-serif" font-weight="700" font-size="13" letter-spacing="0.4">MOST POPULAR</text></svg>')


def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def font_faces():
    """Map the downloaded Google woff2 files onto @font-face rules."""
    files = {os.path.basename(p): p for p in glob.glob(os.path.join(FONT_DIR, "*.woff2"))}
    def find(prefix):
        for name, path in files.items():
            if name.startswith(prefix):
                return path
        sys.exit("missing font file for %s in %s" % (prefix, FONT_DIR))
    faces = [("Archivo", "100 900", find("k3kPo8UDI")),
             ("Archivo Black", "400", find("HTxqL289")),
             ("IBM Plex Mono", "400", find("-F63fjpt")),
             ("IBM Plex Mono", "500", find("-F6qfjpt"))]
    return "\n".join(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:block;"
        "src:url(data:font/woff2;base64,%s) format('woff2');}" % (fam, wt, b64(path))
        for fam, wt, path in faces)


def row_html(title, desc, last):
    edge = "border-bottom:2px solid %s;" % RULE if last else ""
    return (
        '<div style="padding:27px 0;border-top:2px solid {rule};{edge}">'
        '<div style="font:600 29px/1.2 Archivo,sans-serif;color:{ink};">{t}</div>'
        '<div style="margin-top:6px;font:400 25px/1.34 Archivo,sans-serif;color:{muted};">{d}</div>'
        '</div>'
    ).format(rule=RULE, edge=edge, ink=INK, muted=MUTED, t=title, d=desc)


def page(pkg, logo_uri, faces):
    ribbon = ('%s' % ROSETTE.format(blue=BLUE, deep=BLUE_DEEP)) if pkg["popular"] else ""
    rows = "".join(row_html(t, d, i == len(pkg["rows"]) - 1)
                   for i, (t, d) in enumerate(pkg["rows"]))
    return """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}}
html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#fff;
 font-family:Archivo,Helvetica,sans-serif;-webkit-font-smoothing:antialiased;
 text-rendering:geometricPrecision;color:{ink};}}
.frame{{width:1080px;height:1920px;display:flex;flex-direction:column;background:#fff;
 position:relative;overflow:hidden;}}
.rosette{{position:absolute;top:26px;right:56px;width:236px;height:auto;display:block;}}
.head{{flex:0 0 auto;padding:74px 84px 52px;display:flex;flex-direction:column;
 align-items:center;}}
.head img{{width:264px;height:auto;display:block;}}
.bar{{flex:0 0 auto;height:10px;background:{blue};}}
.body{{flex:1 1 auto;padding:44px 84px 0;display:flex;flex-direction:column;}}
h1{{margin:0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:112px;
 line-height:0.9;letter-spacing:-0.03em;color:{blue};text-transform:uppercase;}}
.sub{{margin:22px 0 0;font:400 34px/1.34 Archivo,sans-serif;color:{ink};min-height:92px;}}
.plus{{margin-top:44px;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:0.14em;
 color:{ink};opacity:0.5;}}
.rows{{margin-top:16px;}}
.price{{margin:34px 0 0;font:400 24px/1.4 Archivo,sans-serif;color:{muted};}}
.cta{{margin-top:34px;background:{blue};border-radius:28px;padding:36px 28px;
 display:flex;flex-direction:column;align-items:center;text-align:center;}}
.cta .lbl{{font:500 21px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:#FFFFFF;opacity:0.88;}}
.cta .num{{margin-top:8px;font-family:'Archivo Black',Helvetica,sans-serif;font-size:62px;
 line-height:1;letter-spacing:-0.02em;color:#FFFFFF;white-space:nowrap;}}
</style></head><body><div class="frame">{ribbon}
<div class="head"><img src="{logo}" alt="Carolina Gloss Detailing"></div>
<div class="bar"></div>
<div class="body">
<h1>{title}</h1>
<p class="sub">{sub}</p>
<div class="plus">{plus}</div>
<div class="rows">{rows}</div>
<p class="price">{price}</p>
<div class="cta"><div class="lbl">CALL OR TEXT</div><div class="num">{phone}</div></div>
</div></div></body></html>""".format(
        faces=faces, ink=INK, blue=BLUE, tint=TINT, muted=MUTED,
        logo=logo_uri, ribbon=ribbon,
        title=pkg["title"], sub=pkg["sub"], plus=pkg["plus"], rows=rows,
        price=PRICE_LINE, phone=PHONE)


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = os.environ.get("CGD_TMP", "/tmp/claude-0/-home-user-Weakends-Media-Team/"
                         "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
    logo_uri = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    if "--canvas" in sys.argv:
        write_canvas()
        return
    measure = "--measure" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for pkg in PACKAGES:
        if only and pkg["slug"] not in only:
            continue
        html_path = os.path.join(tmp, "render-%s.html" % pkg["slug"])
        with open(html_path, "w") as fh:
            fh.write(page(pkg, logo_uri, faces))
        if measure:
            probe = html_path.replace(".html", "-probe.html")
            with open(probe, "w") as fh:
                fh.write(open(html_path).read().replace("</body>", """
<script>window.addEventListener('load',function(){
 var f=document.querySelector('.frame'),c=document.querySelector('.cta');
 var gap=f.getBoundingClientRect().bottom-c.getBoundingClientRect().bottom;
 var p=document.createElement('pre');p.id='M';
 p.textContent='bottomGap='+Math.round(gap)+' bodyScroll='+document.body.scrollHeight;
 document.body.appendChild(p);});</script></body>"""))
            dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                                  "--virtual-time-budget=6000", "--dump-dom",
                                  "file://" + probe], capture_output=True, text=True).stdout
            line = dom.split('<pre id="M">')[1].split("</pre>")[0] if '<pre id="M">' in dom else "?"
            print("%-14s %s" % (pkg["slug"], line))
            continue
        png = os.path.join(OUT, pkg["slug"] + ".png")
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--virtual-time-budget=6000", "--window-size=1080,1920",
                        "--screenshot=" + png, "file://" + html_path],
                       capture_output=True)
        print("wrote", png)




# --- canvas export -----------------------------------------------------------
# `python3 build.py --canvas` rewrites the .dc.html so the editable canvas and
# the rendered PNGs never drift apart. Same layout, same copy; the header block
# additionally accepts a real photo behind a dark scrim once the client has one.

def canvas_section(pkg, idx):
    ribbon = (ROSETTE.format(blue=BLUE, deep=BLUE_DEEP).replace(
                  'class="rosette"',
                  'style="position:absolute;top:26px;right:56px;width:236px;height:auto;display:block;"')
              ) if pkg["popular"] else ""
    rows = []
    for i, (t, d) in enumerate(pkg["rows"]):
        edge = "border-bottom:2px solid %s;" % RULE if i == len(pkg["rows"]) - 1 else ""
        rows.append(
            '<div style="padding:27px 0;border-top:2px solid %s;%s">'
            '<div style="font:600 29px/1.2 \'Archivo\',sans-serif;color:%s;">%s</div>'
            '<div style="margin-top:6px;font:400 25px/1.34 \'Archivo\',sans-serif;color:%s;">%s</div>'
            '</div>' % (RULE, edge, INK, t, MUTED, d))
    return """
  <div style="display:flex;flex-direction:column;gap:22px;flex:0 0 auto;">
    <sc-if value="{{{{ showLabels }}}}" hint-placeholder-val="{{{{ true }}}}">
      <div style="font:500 30px 'IBM Plex Mono',monospace;color:#8A95A2;letter-spacing:0.04em;">{label}</div>
    </sc-if>
    <section data-screen-label="{label}" style="width:1080px;height:1920px;flex:0 0 auto;position:relative;overflow:hidden;background:#FFFFFF;display:flex;flex-direction:column;">{ribbon}
      <div style="flex:0 0 auto;padding:74px 84px 52px;display:flex;flex-direction:column;align-items:center;">
        <img src="assets/logo.png" alt="Carolina Gloss Detailing" style="width:264px;height:auto;display:block;">
      </div>
      <div style="flex:0 0 auto;height:10px;background:{blue};"></div>
      <div style="flex:1 1 auto;padding:44px 84px 0;box-sizing:border-box;display:flex;flex-direction:column;">
        <h1 style="margin:0;font-family:'Archivo Black',Helvetica,sans-serif;font-size:112px;line-height:0.9;letter-spacing:-0.03em;color:{blue};text-transform:uppercase;">{title}</h1>
        <p style="margin:22px 0 0;font:400 34px/1.34 'Archivo',sans-serif;color:{ink};min-height:92px;text-wrap:pretty;">{sub}</p>
        <div style="margin-top:44px;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:0.14em;color:{ink};opacity:0.5;">{plus}</div>
        <div style="margin-top:16px;">{rows}</div>
        <p style="margin:34px 0 0;font:400 24px/1.4 'Archivo',sans-serif;color:{muted};text-wrap:pretty;">{price}</p>
        <div style="margin-top:34px;background:{blue};border-radius:28px;padding:36px 28px;display:flex;flex-direction:column;align-items:center;text-align:center;">
          <div style="font:500 21px 'IBM Plex Mono',monospace;letter-spacing:0.16em;color:#FFFFFF;opacity:0.88;">CALL OR TEXT</div>
          <div style="margin-top:8px;font-family:'Archivo Black',Helvetica,sans-serif;font-size:62px;line-height:1;letter-spacing:-0.02em;color:#FFFFFF;white-space:nowrap;">{phone}</div>
        </div>
      </div>
    </section>
  </div>
""".format(label=pkg["slug"].replace("-", " ").title(), ink=INK, blue=BLUE,
           tint=TINT, muted=MUTED,
           ribbon=ribbon, title=pkg["title"], sub=pkg["sub"], plus=pkg["plus"],
           rows="".join(rows), price=PRICE_LINE, phone=PHONE)


CANVAS_PROPS = ('{&quot;showLabels&quot;:{&quot;editor&quot;:&quot;boolean&quot;,&quot;default&quot;:true,'
                '&quot;tsType&quot;:&quot;boolean&quot;,&quot;section&quot;:&quot;Export&quot;}}')


def write_canvas():
    sections = "".join(canvas_section(p, i + 1) for i, p in enumerate(PACKAGES))
    doc = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<meta name="design_doc_mode" content="canvas">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="./image-slot.js"></script>
<style>
  body {{ margin:0; background:#E7E9EC; -webkit-font-smoothing:antialiased; }}
</style>
</helmet>

<div style="display:flex;flex-wrap:wrap;align-items:flex-start;gap:80px;padding:80px;background:#E7E9EC;font-family:'Archivo',Helvetica,sans-serif;">
{sections}
</div>

</x-dc>
<script type="text/x-dc" data-dc-script data-props="{props}">
class Component extends DCLogic {{
  renderVals() {{
    return {{ showLabels: this.props.showLabels ?? true }};
  }}
}}

</script>
</body>
</html>
""".format(sections=sections, props=CANVAS_PROPS)
    path = os.path.join(HERE, "Story Highlights - Services.dc.html")
    with open(path, "w") as fh:
        fh.write(doc)
    print("wrote", path)

if __name__ == "__main__":
    main()
