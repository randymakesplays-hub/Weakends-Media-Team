#!/usr/bin/env python3
"""Ten concepts for the Location highlight, rendered at story size.

The map is a real North Carolina outline projected from public state-boundary
GeoJSON, so Charlotte, Greensboro and Shelby land where they actually are.
Copy stays to what the site already claims: those three cities, mobile.
"""
import json, math, os, subprocess, sys

from build import BLUE, INK, TINT, RULE, MUTED, PHONE, CHROME, b64, font_faces

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "location")
TMP = ("/tmp/claude-0/-home-user-Weakends-Media-Team/"
       "e694c530-fc11-54a2-af59-d2f4859a017f/scratchpad")
GEO = os.path.join(HERE, "assets", "us-states.json")

CHARLOTTE = dict(name="Charlotte", lat=35.2271, lon=-80.8431, side="right")
GREENSBORO = dict(name="Greensboro", lat=36.0726, lon=-79.7920, side="right")
SHELBY = dict(name="Shelby", lat=35.2924, lon=-81.5356, side="left")
CITIES = [GREENSBORO, CHARLOTTE, SHELBY]


def load_rings():
    with open(GEO) as fh:
        data = json.load(fh)
    nc = [f for f in data["features"]
          if f["properties"]["name"] == "North Carolina"][0]
    geom = nc["geometry"]
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


RINGS = load_rings()
LONS = [p[0] for r in RINGS for p in r]
LATS = [p[1] for r in RINGS for p in r]
FULL = (min(LONS), min(LATS), max(LONS), max(LATS))


class Map(object):
    """Equirectangular with a cos(lat) correction — honest enough at one state."""

    def __init__(self, width, bbox=None, pad=0.0):
        lon0, lat0, lon1, lat1 = bbox or FULL
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        self.scale = (width - 2 * pad) / ((lon1 - lon0) * self.k)
        self.lon0, self.lat1, self.pad = lon0, lat1, pad
        self.width = width
        self.height = (lat1 - lat0) * self.scale + 2 * pad

    def xy(self, lon, lat):
        return (self.pad + (lon - self.lon0) * self.k * self.scale,
                self.pad + (self.lat1 - lat) * self.scale)

    def at(self, city):
        return self.xy(city["lon"], city["lat"])

    def path(self):
        return " ".join(
            "M" + " L".join("%.1f,%.1f" % self.xy(p[0], p[1]) for p in ring) + " Z"
            for ring in RINGS)

    def outline(self, fill="none", stroke="none", width=0, extra=""):
        return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" '
                'stroke-linejoin="round" %s/>'
                % (self.path(), fill, stroke, width, extra))

    def svg(self, body, cls="", style=""):
        return ('<svg class="map %s" viewBox="0 0 %.0f %.1f" width="%.0f" '
                'height="%.1f" style="%s" aria-hidden="true">%s</svg>'
                % (cls, self.width, self.height, self.width, self.height,
                   style, body))


def inside(lon, lat):
    """Ray cast against the state outline, for the halftone fill."""
    hit = False
    for ring in RINGS:
        n = len(ring)
        for i in range(n):
            x0, y0 = ring[i]
            x1, y1 = ring[(i + 1) % n]
            if (y0 > lat) != (y1 > lat):
                if lon < x0 + (lat - y0) * (x1 - x0) / (y1 - y0):
                    hit = not hit
    return hit


def dots(m, cities=CITIES, r=15, ring=0, ring_fill="#FFFFFF", fill=None):
    out = []
    for c in cities:
        x, y = m.at(c)
        if ring:
            out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>'
                       % (x, y, r + ring, ring_fill))
        out.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>'
                   % (x, y, r, fill or INK))
    return "".join(out)


def labels(m, cities=CITIES, size=30, colour=None, gap=30, side=None):
    out = []
    for c in cities:
        x, y = m.at(c)
        where = side or c["side"]
        dx, anchor = ((gap, "start") if where == "right" else (-gap, "end"))
        out.append('<text x="%.1f" y="%.1f" text-anchor="%s" fill="%s" '
                   'font-family="Archivo" font-weight="700" font-size="%d" '
                   'dominant-baseline="middle">%s</text>'
                   % (x + dx, y, anchor, colour or INK, size, c["name"]))
    return "".join(out)


CSS = """
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:1080px;height:1920px;overflow:hidden;background:#FFFFFF;
 font-family:Archivo,Helvetica,sans-serif;color:{ink};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.frame{{width:1080px;height:1920px;display:flex;flex-direction:column;
 overflow:hidden;position:relative;}}
.head{{flex:0 0 auto;padding:66px 84px 44px;display:flex;justify-content:center;}}
.head img{{width:240px;height:auto;display:block;}}
.bar{{flex:0 0 auto;height:10px;background:{blue};}}
.body{{flex:1 1 auto;padding:72px 84px 180px;display:flex;flex-direction:column;
 overflow:hidden;}}
.map{{display:block;}}
.grow{{flex:1 1 auto;}}
.eyebrow{{font:500 25px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 text-transform:uppercase;opacity:0.5;}}
.h{{font-family:'Archivo Black',Helvetica,sans-serif;line-height:0.9;
 letter-spacing:-0.04em;font-size:128px;}}
.h em{{font-style:normal;color:{blue};}}
.sub{{margin-top:24px;font:400 34px/1.35 Archivo,sans-serif;color:{muted};}}

/* dark variants */
.dark{{background:{ink};color:#FFFFFF;}}
.dark .sub{{color:rgba(255,255,255,0.66);}}
.dark .eyebrow{{opacity:0.6;}}
.blue{{background:{blue};color:#FFFFFF;}}
.blue .sub{{color:rgba(255,255,255,0.82);}}

.bleed{{margin-left:-84px;margin-right:-84px;}}
.clip{{overflow:hidden;}}
/* The map takes whatever height is left and crops, so nothing floats in a void. */
.mapwrap{{flex:1 1 auto;display:flex;align-items:center;overflow:hidden;
 margin-left:-84px;margin-right:-84px;}}

.cta{{flex:0 0 auto;margin-top:40px;background:{blue};border-radius:28px;
 padding:34px 28px;text-align:center;}}
.cta .lbl{{font:500 21px 'IBM Plex Mono',monospace;letter-spacing:0.16em;
 color:#FFFFFF;opacity:0.9;}}
.cta .num{{margin-top:6px;font-family:'Archivo Black',Helvetica,sans-serif;
 font-size:58px;letter-spacing:-0.02em;color:#FFFFFF;}}
.dark .cta,.blue .cta{{background:#FFFFFF;}}
.dark .cta .lbl,.blue .cta .lbl{{color:{ink};opacity:0.62;}}
.dark .cta .num,.blue .cta .num{{color:{ink};}}

/* city rows */
.rows{{border-top:3px solid {rule};}}
.row{{padding:26px 0;border-bottom:3px solid {rule};display:flex;
 align-items:baseline;gap:20px;}}
.row b{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:56px;
 letter-spacing:-0.03em;color:{blue};}}
.row span{{font:400 28px Archivo,sans-serif;color:{muted};}}

/* tiles */
.tiles{{display:flex;flex-direction:column;gap:22px;}}
.tile{{background:{tint};border-radius:28px;padding:32px 36px;display:flex;
 align-items:center;justify-content:space-between;gap:24px;}}
.tile b{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:62px;
 letter-spacing:-0.03em;}}
.tile .map{{flex:0 0 auto;opacity:0.9;}}

/* stacked type */
.stack{{font-family:'Archivo Black',Helvetica,sans-serif;font-size:126px;
 line-height:0.92;letter-spacing:-0.045em;}}
.stack i{{font-style:normal;display:block;}}
.stack i:last-child{{color:{blue};}}

/* split */
.slab{{background:{ink};margin:-72px -84px 0;padding:72px 84px 60px;
 display:flex;flex-direction:column;justify-content:center;}}
.slab .eyebrow{{color:#FFFFFF;}}
"""


def frame(inner, logo, crest=True, cls="", body_cls=""):
    head = ('<div class="head"><img src="%s" alt="Carolina Gloss Detailing">'
            '</div>' % logo) if crest else ""
    return ('<div class="frame %s">%s<div class="bar"></div>'
            '<div class="body %s">%s</div></div>' % (cls, head, body_cls, inner))


def page(inner, logo, faces, crest=True, cls="", body_cls=""):
    style = CSS.format(faces=faces, ink=INK, blue=BLUE, tint=TINT,
                       rule=RULE, muted=MUTED)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s</style>'
            '</head><body>%s</body></html>'
            % (style, frame(inner, logo, crest, cls, body_cls)))


# ---------------------------------------------------------------- concepts

CTA = ('<div class="cta"><div class="lbl">CALL OR TEXT</div>'
       '<div class="num">%s</div></div>' % PHONE)


def head(eyebrow, headline, sub="", size=None):
    s = ' style="margin-top:18px;font-size:%dpx"' % size if size else \
        ' style="margin-top:18px"'
    return ('<div class="eyebrow">%s</div><div class="h"%s>%s</div>%s'
            % (eyebrow, s, headline,
               '<p class="sub">%s</p>' % sub if sub else ""))


def c01_giant(logo, faces):
    """Solid blue state at scale, cropped by the frame. No pale silhouette."""
    m = Map(1860)
    body = (m.outline(fill=BLUE)
            + dots(m, r=22, ring=11, ring_fill="#FFFFFF")
            + labels(m, size=40, gap=40))
    return page(
        head("Where we go", 'We come<br><em>to you.</em>')
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-300px")
        + '</div>' + CTA, logo, faces)


def c02_invert(logo, faces):
    """Black field, blue state, white type. Loudest of the set."""
    m = Map(1640)
    body = (m.outline(fill=BLUE)
            + dots(m, r=20, ring=10, ring_fill=INK, fill="#FFFFFF")
            + labels(m, size=38, colour="#FFFFFF", gap=38))
    return page(
        head("Service area",
             'Charlotte.<br>Greensboro.<br><em>Shelby.</em>', size=104)
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-200px")
        + '</div>'
        + '<p class="sub" style="margin:0">Mobile detailing. We come to you.</p>',
        logo, faces, cls="dark")


def c03_radar(logo, faces):
    """Rings pushing out of Charlotte — reach, without claiming a radius."""
    m = Map(1720)
    cx, cy = m.at(CHARLOTTE)
    rings = "".join(
        '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" '
        'stroke-width="5" opacity="%.2f"/>' % (cx, cy, r, BLUE, op)
        for r, op in ((150, 0.6), (300, 0.44), (450, 0.3), (600, 0.2),
                      (750, 0.12)))
    body = (m.outline(fill=TINT, stroke=BLUE, width=6) + rings
            + dots(m, r=20, ring=10) + labels(m, size=38, gap=38))
    return page(
        head("Where we go", 'We drive<br><em>the miles.</em>',
             "You keep your day.")
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-260px")
        + '</div>' + CTA, logo, faces)


def c04_route(logo, faces):
    """A dashed run across the three cities. Movement, not a static pin drop."""
    m = Map(1720)
    pts = [m.at(SHELBY), m.at(CHARLOTTE), m.at(GREENSBORO)]
    run = ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" '
           'stroke-width="11" stroke-linecap="round" stroke-dasharray="2 30"/>'
           % (pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1],
              BLUE))
    body = (m.outline(fill=TINT, stroke=BLUE, width=5) + run
            + dots(m, r=20, ring=10) + labels(m, size=38, gap=38))
    return page(
        head("Mobile detailing", "We drive.<br><em>You don't.</em>")
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-260px")
        + '</div>' + CTA, logo, faces)


def c05_zoom(logo, faces):
    """Cropped into the corridor so the cities read at street scale."""
    m = Map(1240, bbox=(-82.3, 34.8, -79.2, 36.5))
    # Greensboro sits near the right edge of this crop, so its label goes left.
    body = (m.outline(fill=TINT, stroke=BLUE, width=7) + dots(m, r=24, ring=12)
            + labels(m, [SHELBY, CHARLOTTE], size=46, gap=46, side="right")
            + labels(m, [GREENSBORO], size=46, gap=46, side="left"))
    return page(
        head("Service area", 'Three cities.<br><em>One drive.</em>', size=112)
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-160px")
        + '</div>' + CTA, logo, faces)


def c06_halftone(logo, faces):
    """Dot grid that tightens toward the three cities. Reads as coverage."""
    m = Map(1500)
    cells = []
    step = 0.075
    lon = FULL[0]
    while lon <= FULL[2]:
        lat = FULL[1]
        while lat <= FULL[3]:
            if inside(lon, lat):
                d = min(math.hypot((lon - c["lon"]) * 0.82, lat - c["lat"])
                        for c in CITIES)
                r = max(5.0, 15.5 - d * 7.0)
                op = max(0.34, min(0.95, 1.15 - d * 0.5))
                x, y = m.xy(lon, lat)
                cells.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" '
                             'opacity="%.2f"/>' % (x, y, r, BLUE, op))
            lat += step
        lon += step
    body = ("".join(cells) + dots(m, r=18, ring=9)
            + labels(m, size=36, gap=36))
    return page(
        head("Where we go", 'We come<br><em>to you.</em>')
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-210px")
        + '</div>' + CTA, logo, faces)


def c07_split(logo, faces):
    """Hard horizontal edge: dark map slab on top, white type below."""
    m = Map(1420)
    body = (m.outline(fill=BLUE)
            + dots(m, r=18, ring=9, ring_fill=INK, fill="#FFFFFF")
            + labels(m, size=34, colour="#FFFFFF", gap=34))
    return page(
        '<div class="slab"><div class="eyebrow">Service area</div>'
        '<div class="bleed clip" style="margin-top:26px;margin-bottom:-30px">'
        + m.svg(body, style="margin-left:-170px") + '</div></div>'
        '<div class="grow"></div>'
        '<div class="h" style="font-size:112px">Charlotte<br>Greensboro<br>'
        '<em>Shelby</em></div>'
        '<div class="grow"></div>' + CTA,
        logo, faces)


def c08_tiles(logo, faces):
    """One tile per city, each with its own locator. The systematic option."""
    tiles = []
    for c in (CHARLOTTE, GREENSBORO, SHELBY):
        m = Map(320)
        loc = (m.outline(fill="#FFFFFF", stroke=RULE, width=5)
               + dots(m, [c], r=16, ring=8, ring_fill="#FFFFFF", fill=BLUE))
        tiles.append('<div class="tile"><b>%s</b>%s</div>'
                     % (c["name"], m.svg(loc)))
    return page(
        head("Where we go", 'We come<br><em>to you.</em>', size=112)
        + '<div class="grow"></div>'
        + '<div class="tiles">' + "".join(tiles) + '</div>'
        + '<div class="grow"></div>' + CTA,
        logo, faces)


def c09_type(logo, faces):
    """Type does the work; the map anchors it. All three cities equal weight."""
    m = Map(1500)
    body = (m.outline(fill=TINT, stroke=BLUE, width=6)
            + dots(m, r=18, ring=9))
    return page(
        '<div class="eyebrow">Serving</div>'
        '<div class="stack" style="margin-top:24px"><i>Charlotte</i>'
        '<i>Greensboro</i><i>Shelby</i></div>'
        '<div class="mapwrap">' + m.svg(body, style="margin-left:-210px")
        + '</div>'
        '<p class="sub" style="margin:0">Mobile detailing across North Carolina. '
        'We come to you.</p>',
        logo, faces)


def c10_blue(logo, faces):
    """Carolina blue field, white state knocked out. The brand-colour play."""
    m = Map(1720)
    body = (m.outline(fill="#FFFFFF", extra='opacity="0.5"')
            + dots(m, r=20, ring=10, ring_fill=BLUE, fill=INK)
            + labels(m, size=38, colour="#FFFFFF", gap=38))
    return page(
        head("Where we go", 'We come<br>to you.')
        + '<div class="mapwrap">' + m.svg(body, style="margin-left:-260px")
        + '</div>' + CTA, logo, faces, cls="blue")


CONCEPTS = [
    ("01-giant", "01 · Giant", c01_giant),
    ("02-invert", "02 · Black invert", c02_invert),
    ("03-radar", "03 · Radar", c03_radar),
    ("04-route", "04 · Route", c04_route),
    ("05-zoom", "05 · Zoom crop", c05_zoom),
    ("06-halftone", "06 · Halftone", c06_halftone),
    ("07-split", "07 · Split slab", c07_split),
    ("08-tiles", "08 · City tiles", c08_tiles),
    ("09-type", "09 · Type led", c09_type),
    ("10-blue", "10 · Blue field", c10_blue),
]


def shoot(html, path, w=1080, h=1920, scale=1):
    src = os.path.join(TMP, "loc-" + os.path.basename(path).replace(".png", ".html"))
    with open(src, "w") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=%d" % scale,
                    "--virtual-time-budget=9000", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + path, "file://" + src], capture_output=True)
    print("wrote", path)


def sheet(faces, cols=5):
    tiles = "".join(
        '<figure><img src="{s}.png"><figcaption>{n}</figcaption></figure>'.format(
            s=s, n=n) for s, n, _ in CONCEPTS)
    tile = 300
    width = cols * (tile + 30) + 40
    rows = (len(CONCEPTS) + cols - 1) // cols
    html = """<!doctype html><html><head><meta charset="utf-8"><style>
{faces}
*{{box-sizing:border-box;}} html,body{{margin:0;padding:0;}}
body{{width:{width}px;background:#EFF1F4;display:grid;
 grid-template-columns:repeat({cols},{tile}px);gap:30px 30px;
 justify-content:center;padding:36px 20px;font-family:Archivo,Helvetica,sans-serif;}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:12px;}}
img{{width:{tile}px;height:auto;display:block;border-radius:9px;
 box-shadow:0 6px 22px rgba(15,22,32,0.18);}}
figcaption{{font:700 17px Archivo,sans-serif;color:{ink};}}
</style></head><body>{tiles}</body></html>""".format(
        faces=faces, ink=INK, tiles=tiles, width=width, cols=cols, tile=tile)
    src = os.path.join(OUT, "_sheet.html")
    with open(src, "w") as fh:
        fh.write(html)
    height = rows * (tile * 1920 // 1080 + 45) + 80
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--virtual-time-budget=12000",
                    "--window-size=%d,%d" % (width, height),
                    "--screenshot=" + os.path.join(OUT, "00-concepts.png"),
                    "file://" + src], capture_output=True)
    print("wrote", os.path.join(OUT, "00-concepts.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = "data:image/png;base64," + b64(os.path.join(HERE, "assets", "logo.png"))
    faces = font_faces()
    for slug, _, build in CONCEPTS:
        shoot(build(logo, faces), os.path.join(OUT, slug + ".png"))
    sheet(faces)


if __name__ == "__main__":
    main()
