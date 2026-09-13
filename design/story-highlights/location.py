#!/usr/bin/env python3
"""Three concepts for the Location highlight, rendered at story size.

The map is a real North Carolina outline projected from public state-boundary
GeoJSON, not a traced shape, so the three cities land where they actually are.
Copy stays to what the site already claims: Charlotte, Greensboro, Shelby.
"""
import json, math, os, subprocess, sys

from build import BLUE, INK, TINT, RULE, MUTED, PHONE, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "location")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
GEO = os.path.join(TMP, "us-states.json")

# Real coordinates. Order matters only for label placement.
CITIES = [
    dict(name="Greensboro", lat=36.0726, lon=-79.7920, side="right"),
    dict(name="Charlotte", lat=35.2271, lon=-80.8431, side="right"),
    dict(name="Shelby", lat=35.2924, lon=-81.5356, side="left"),
]

MAP_W = 1000.0          # SVG user units across the state's full width
PAD = 26.0              # room for the dot rings and strokes to not clip


def rings():
    with open(GEO) as fh:
        data = json.load(fh)
    nc = [f for f in data["features"]
          if f["properties"]["name"] == "North Carolina"][0]
    geom = nc["geometry"]
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


def projector(rs):
    """Equirectangular with a cos(lat) correction — honest enough at one state."""
    lons = [p[0] for r in rs for p in r]
    lats = [p[1] for r in rs for p in r]
    lon0, lon1 = min(lons), max(lons)
    lat0, lat1 = min(lats), max(lats)
    k = math.cos(math.radians((lat0 + lat1) / 2))
    scale = (MAP_W - 2 * PAD) / ((lon1 - lon0) * k)
    height = (lat1 - lat0) * scale + 2 * PAD

    def xy(lon, lat):
        return (PAD + (lon - lon0) * k * scale,
                PAD + (lat1 - lat) * scale)
    return xy, height


RINGS = rings()
XY, MAP_H = projector(RINGS)


def outline(fill, stroke, width):
    d = " ".join(
        "M" + " L".join("%.1f,%.1f" % XY(p[0], p[1]) for p in ring) + " Z"
        for ring in RINGS)
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (d, fill, stroke, width))


def pins(r=15, label=30, halo=0):
    out = []
    for c in CITIES:
        x, y = XY(c["lon"], c["lat"])
        if halo:
            out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" '
                       'opacity="0.28"/>' % (x, y, halo, BLUE))
        out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="#FFFFFF"/>'
                   % (x, y, r + 7))
        out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>'
                   % (x, y, r, INK))
        if label:
            dx, anchor = ((r + 16, "start") if c["side"] == "right"
                          else (-(r + 16), "end"))
            out.append('<text x="%.1f" y="%.1f" text-anchor="%s" fill="%s" '
                       'font-family="Archivo" font-weight="700" font-size="%d" '
                       'dominant-baseline="middle">%s</text>'
                       % (x + dx, y, anchor, INK, label, c["name"]))
    return "".join(out)


def svg(body, cls=""):
    return ('<svg class="map %s" viewBox="0 0 %d %.1f" width="100%%" '
            'aria-hidden="true">%s</svg>' % (cls, int(MAP_W), MAP_H, body))


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
.body{{flex:1 1 auto;padding:84px 84px 210px;display:flex;flex-direction:column;
 justify-content:center;}}
.eyebrow{{font:500 25px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 text-transform:uppercase;color:{ink};opacity:0.45;}}
.map{{display:block;height:auto;}}
.bleed{{margin-left:-84px;margin-right:-84px;width:1080px;}}

.headline{{font-family:'Archivo Black',Helvetica,sans-serif;line-height:0.94;
 letter-spacing:-0.035em;font-size:110px;}}
.headline em{{font-style:normal;color:{blue};}}
.sub{{margin-top:26px;font:400 36px/1.4 Archivo,sans-serif;color:{muted};}}

/* B — map over a city list */
.rows{{margin-top:46px;border-top:3px solid {rule};}}
.row{{padding:30px 0;border-bottom:3px solid {rule};display:flex;
 align-items:baseline;gap:22px;}}
.row b{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:54px;
 letter-spacing:-0.03em;color:{blue};}}
.row span{{font:400 30px Archivo,sans-serif;color:{muted};}}

/* C — the coverage band */
.band{{margin-top:44px;background:{tint};border-radius:30px;padding:40px 44px;
 text-align:center;font:400 34px/1.4 Archivo,sans-serif;}}
.cities{{margin-top:36px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:64px;line-height:1.16;letter-spacing:-0.03em;text-align:center;}}
.cities i{{font-style:normal;color:{blue};}}
"""


def page(inner, logo, faces, crest=True):
    style = CSS.format(faces=faces, ink=INK, blue=BLUE, tint=TINT,
                       rule=RULE, muted=MUTED)
    head = ('<div class="head"><img src="%s" alt="Carolina Gloss Detailing">'
            '</div>' % logo) if crest else ""
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style>'
            '</head><body><div class="frame">%s<div class="bar"></div>'
            '<div class="body">%s</div></div></body></html>'
            % (style, head, inner))


def concept_a():
    """Map as the hero. Headline, then the state edge to edge."""
    return ('<div class="eyebrow">Where we go</div>'
            '<div class="headline" style="margin-top:22px">We come<br>'
            '<em>to you.</em></div>'
            '<p class="sub">Mobile detailing at your home or office.</p>'
            + svg(outline(TINT, BLUE, 5) + pins(15, 30), "bleed"))


def concept_b():
    """Small map for orientation, the cities carry the detail."""
    return ('<div class="eyebrow">Service area</div>'
            + svg(outline(TINT, BLUE, 6) + pins(14, 0))
            + '<div class="rows">'
            + "".join('<div class="row"><b>%s</b><span>%s</span></div>'
                      % (c["name"], s)
                      for c, s in zip(CITIES,
                                      ["and the Triad",
                                       "and the surrounding metro",
                                       "and Cleveland County"]))
            + '</div><p class="sub">We drive out. You keep your day.</p>')


def concept_c():
    """Coverage read — halos do the talking, type stays quiet."""
    return ('<div class="eyebrow" style="text-align:center">Serving</div>'
            + '<div class="cities"><i>Charlotte</i><br><i>Greensboro</i><br>'
              '<i>Shelby</i></div>'
            + svg(outline("#FFFFFF", RULE, 5) + pins(16, 0, halo=88), "bleed")
            + '<div class="band">Wherever you park it, that is where '
              'we detail it.</div>')


CONCEPTS = [
    ("a-map", "A · Map hero", concept_a),
    ("b-list", "B · Map + cities", concept_b),
    ("c-coverage", "C · Coverage", concept_c),
]


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "loc-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=7000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    for slug, _, build in CONCEPTS:
        shoot(page(build(), logo, faces), os.path.join(OUT, slug + ".png"))

    tiles = "".join(
        '<figure><img src="{s}.png"><figcaption>{n}</figcaption></figure>'.format(s=s, n=n)
        for s, n, _ in CONCEPTS)
    sheet = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1360px;background:#EFF1F4;display:flex;justify-content:center;gap:34px;
 padding:40px 34px;font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:16px;}}
img{{width:390px;height:auto;display:block;border-radius:10px;
 box-shadow:0 6px 26px rgba(15,22,32,0.16);}}
figcaption{{font:700 20px Archivo,sans-serif;color:{ink};}}
</style></head><body>{tiles}</body></html>""".format(faces=faces, ink=INK, tiles=tiles)
    src = os.path.join(OUT, "_sheet.html")
    with open(src, "w") as fh:
        fh.write(sheet)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=9000", "--window-size=1360,860",
                    "--screenshot=" + os.path.join(OUT, "00-concepts.png"),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, "00-concepts.png"))


if __name__ == "__main__":
    main()
