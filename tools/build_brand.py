#!/usr/bin/env python3
"""
Regenerate the vector brand assets for PDX Hackerspace (CTRL-H).

    python3 tools/build_brand.py

Writes SVGs into brand/logo, brand/illustrations and brand/patterns.
No third-party dependencies. Geometry is traced from the wood-engraved sign
(brand/reference/sign-wood-engraved.webp) so the mark matches what is on the wall.

Edit the constants here, never the generated SVGs by hand.
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Palette (keep in sync with brand/tokens.css and DESIGN.md) -------------
INK = "#16181D"
PAPER = "#FBF8F1"
NIGHT = "#1F5A85"
STEEL = "#A9B4B6"
RAINBOW = {
    "red": "#E2382D",
    "orange": "#F28A0F",
    "yellow": "#F7CB2D",
    "green": "#6DB33F",
    "blue": "#119FD6",
    "violet": "#7468C2",
}
R_ORDER = ["red", "orange", "yellow", "green", "blue", "violet"]

# ---- Logo geometry (viewBox 0 0 1000 1000, badge centred at 500,500) -------
CX, CY, R_OUT = 500, 500, 480
HEX_R = 30  # radius of the small "caret" hexagons
# Small hexagons: (x, y, colour used in the full-colour badge)
CARET_HEXES = [
    (326, 422, "yellow"),
    (385, 422, "red"),
    (267, 488, "blue"),
    (385, 488, "orange"),
    (385, 555, "violet"),
]
H = dict(x0=481, x1=533, x2=655, x3=707, y0=396, y1=713, c0=529, c1=595)
TEXT_FONT = "'Space Grotesk','Avenir Next','Futura','Helvetica Neue',Arial,sans-serif"


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(points):
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)


def hex_points(cx, cy, r, pointy=True):
    start = -90 if pointy else 0
    return [
        (cx + r * math.cos(math.radians(start + 60 * k)),
         cy + r * math.sin(math.radians(start + 60 * k)))
        for k in range(6)
    ]


def h_points():
    w = H["x1"] - H["x0"]
    t = (w / 2) * math.tan(math.radians(30))  # pointed tip height
    lm = (H["x0"] + H["x1"]) / 2
    rm = (H["x2"] + H["x3"]) / 2
    x0, x1, x2, x3 = H["x0"], H["x1"], H["x2"], H["x3"]
    y0, y1, c0, c1 = H["y0"], H["y1"], H["c0"], H["c1"]
    return [
        (x0, y0 + t), (lm, y0), (x1, y0 + t), (x1, c0), (x2, c0), (x2, y0 + t),
        (rm, y0), (x3, y0 + t), (x3, y1 - t), (rm, y1), (x2, y1 - t), (x2, c1),
        (x1, c1), (x1, y1 - t), (lm, y1), (x0, y1 - t),
    ]


def slot_polys(r_in=398, r_out=428, trim=0.1):
    """Six light-bar slots that run inside the outer hexagon's edges."""
    inner = hex_points(CX, CY, r_in)
    outer = hex_points(CX, CY, r_out)
    polys = []
    for i in range(6):
        j = (i + 1) % 6

        def lerp(a, b, t):
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

        polys.append([
            lerp(outer[i], outer[j], trim), lerp(outer[i], outer[j], 1 - trim),
            lerp(inner[i], inner[j], 1 - trim), lerp(inner[i], inner[j], trim),
        ])
    return polys


def mark_shapes(fill_hex=None, fill_h=None):
    """The caret-hexes + H. fill_hex(color_name) -> fill string."""
    out = []
    for x, y, c in CARET_HEXES:
        f = fill_hex(c) if fill_hex else "currentColor"
        out.append(f'<polygon points="{pts(hex_points(x, y, HEX_R))}" fill="{f}"/>')
    out.append(f'<polygon points="{pts(h_points())}" fill="{fill_h or "currentColor"}"/>')
    return "\n  ".join(out)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
    print("wrote", rel)


def rainbow_gradient(gid, x1, y1, x2, y2, order=R_ORDER):
    stops = "".join(
        f'<stop offset="{i / (len(order) - 1):.3f}" stop-color="{RAINBOW[c]}"/>'
        for i, c in enumerate(order)
    )
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}">{stops}</linearGradient>')


# ---- Logo files --------------------------------------------------------------
def build_logo():
    # Mark only: tight viewBox around the caret + H, single colour (currentColor)
    mx0, my0 = 267 - 26 - 4, 396 - 4
    mw, mh = (707 + 4) - mx0, (713 + 4) - my0
    vb = f"{fmt(mx0)} {fmt(my0)} {fmt(mw)} {fmt(mh)}"
    write("brand/logo/ctrlh-mark.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="CTRL-H">
  {mark_shapes()}
</svg>""")

    # Mark in rainbow
    defs = rainbow_gradient("hgrad", 0, 396, 0, 713)
    write("brand/logo/ctrlh-mark-rainbow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="CTRL-H">
  <defs>{defs}</defs>
  {mark_shapes(lambda c: RAINBOW[c], "url(#hgrad)")}
</svg>""")

    slots = slot_polys()
    verts = hex_points(CX, CY, R_OUT)
    holes = hex_points(CX, CY, R_OUT - 22)

    def text_block(fill_pdx, fill_hs, fill_est):
        return f"""
  <g font-family="{TEXT_FONT}" text-anchor="middle" font-weight="600">
    <text x="500" y="252" font-size="62" letter-spacing="4" fill="{fill_pdx}">PDX</text>
    <text x="500" y="338" font-size="64" letter-spacing="3" fill="{fill_hs}">HACKERSPACE</text>
    <text x="500" y="806" font-size="40" letter-spacing="2" fill="{fill_est}">EST. 2014</text>
  </g>"""

    # Full-colour badge on ink (the LED-sign look)
    grads = [rainbow_gradient("hgrad", 0, 396, 0, 713),
             rainbow_gradient("tgrad", 300, 0, 700, 0,
                              ["violet", "blue", "red", "orange", "yellow", "green"])]
    slot_svg = []
    for i, p in enumerate(slots):
        a, b = p[0], p[1]
        rot = R_ORDER[i:] + R_ORDER[:i]
        grads.append(rainbow_gradient(f"s{i}", a[0], a[1], b[0], b[1], rot))
        slot_svg.append(f'<polygon points="{pts(p)}" fill="url(#s{i})"/>')
    write("brand/logo/ctrlh-badge.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="PDX Hackerspace, established 2014">
  <defs>{''.join(grads)}</defs>
  <polygon points="{pts(verts)}" fill="{INK}"/>
  {chr(10).join('  ' + s for s in slot_svg).strip()}
  {text_block(RAINBOW['blue'], 'url(#tgrad)', RAINBOW['blue'])}
  {mark_shapes(lambda c: RAINBOW[c], "url(#hgrad)")}
</svg>""")

    # Single-colour badge: for laser, CNC, vinyl, rubber stamps, embroidery digitising.
    # currentColor = the engraved / cut / stitched areas.
    write("brand/logo/ctrlh-badge-mono.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="PDX Hackerspace, established 2014">
  <polygon points="{pts(verts)}" fill="none" stroke="currentColor" stroke-width="6"/>
  {chr(10).join(f'  <polygon points="{pts(p)}" fill="currentColor"/>' for p in slots).strip()}
  {chr(10).join(f'  <circle cx="{fmt(x)}" cy="{fmt(y)}" r="7" fill="currentColor"/>' for x, y in holes).strip()}
  {text_block('currentColor', 'currentColor', 'currentColor')}
  {mark_shapes()}
</svg>""")

    # Hexagon-only outline (for framing, stickers, die-cut lines)
    write("brand/logo/ctrlh-hex-outline.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
  <polygon points="{pts(verts)}" fill="none" stroke="currentColor" stroke-width="8"/>
</svg>""")


# ---- Pixel-sprite mascots ----------------------------------------------------
# One character per pixel. '.' = transparent. Drawn in the chunky style of the
# Nyan mural: black outline, flat fills, no anti-aliasing.
SPRITE_COLORS = {
    "K": INK, "W": "#FFFFFF",
    "B": "#7A4A2A", "b": "#C48A55", "p": "#F2A3B5",            # sasquatch fur / face / blush
    "G": "#7BD36B", "g": "#4E9A44",                             # alien greens
    "S": STEEL, "s": "#D9E0E1",                                 # saucer metal
    "Y": RAINBOW["yellow"], "R": RAINBOW["red"], "O": RAINBOW["orange"],
    "C": RAINBOW["blue"], "V": RAINBOW["violet"], "N": RAINBOW["green"],
    "o": "#FBE3B8",                                             # kitty cream
    "D": NIGHT,                                                 # ninja suit
    "L": "#EFE3CC",                                             # llama wool
    "q": "#DDF2FA",                                             # helmet glass
    "H": "#8A3B1F",                                             # pirate hair (auburn)
}

SASQUATCH = """
......K..K......
....KKBKKBKK....
...KBBBBBBBBK...
..KBBBBBBBBBBK..
..KBBbbbbbbBBK..
..KBbbKbbKbbBK..
..KBbbKbbKbbBK..
..KBbpbbbbpbBK..
..KBBbbKKbbBBK..
.KBBBBbbbbBBBBK.
KBBBBBBBBBBBBBBK
KBBKBBBBBBBBKBBK
KBBKBBbbbbBBKBBK
KBBKBBbbbbBBKBBK
KBBKBBBBBBBBKBBK
KbbKKBBBBBBKKbbK
.KK.KBBBKBBBK.KK
....KBBK.KBBK...
...KBBBK.KBBBK..
...KKKKK.KKKKK..
"""

SASQUATCH_GOGGLES = """
......K..K......
....KKBKKBKK....
...KBBBBBBBBK...
..KBBBBBBBBBBK..
.KKKKKKKKKKKKKK.
.KKYCCYKKYCCYKK.
..KKKKKbbKKKKK..
..KBbpbbbbpbBK..
..KBBbbKKbbBBK..
.KBBBBbbbbBBBBK.
KBBBBBBBBBBBBBBK
KBBKBBBBBBBBKBBK
KBBKBBbbbbBBKBBK
KBBKBBbbbbBBKBBK
KBBKBBBBBBBBKBBK
KbbKKBBBBBBKKbbK
.KK.KBBBKBBBK.KK
....KBBK.KBBK...
...KBBBK.KBBBK..
...KKKKK.KKKKK..
"""

ALIEN = """
...K........K...
....K......K....
....YK....KY....
.....KKKKKK.....
...KKGGGGGGKK...
..KGGGGGGGGGGK..
.KGGGGGGGGGGGGK.
.KGKKKGGGGKKKGK.
.KGKWKGGGGKWKGK.
.KGKKKGGGGKKKGK.
..KGGGGGGGGGGK..
...KGGGKKGGGK...
....KKGGGGKK....
...KGGgGGgGGK...
..KGKGgGGgGKGK..
..KK.KGGGGK.KK..
....KGK..KGK....
....KK....KK....
"""

SAUCER = """
.......KKKKKK.......
.....KKCCCCCCKK.....
....KCCWCCCCCCCK....
....KCCCCCCCCCCK....
..KKKKKKKKKKKKKKKK..
.KSSSSSSSSSSSSSSSSK.
KSsYSSsRSSsNSSsYSSsK
.KSSSSSSSSSSSSSSSSK.
..KKKKKKKKKKKKKKKK..
"""

SPARKLE = """
...K...
...K...
.......
KK.K.KK
.......
...K...
...K...
"""

HEX_PIXEL = """
...KKKK...
..KYYYYK..
.KYYYYYYK.
KYYYYYYYYK
.KYYYYYYK.
..KYYYYK..
...KKKK...
"""


# Original CTRL-H mascot: an orange-and-white cat astronaut in a glass helmet, antenna LED on
# top and a status LED on the collar. Stands upright; no pastry, no rainbow trail.
SPACECAT = """
..........R...........
..........K...........
.......KKKKKKKK.......
.....KKqqqqqqqqKK.....
....KqqKqqqqqqKqqK....
...KqqKOKqqqqKWKqqK...
...KqKOOOKKKKWWWKqK...
..KqqKOOOWWWWWWWKqqK..
..KqqKOKKWWWKKWWKqqK..
..KqqKOKKWWWKKWWKqqK..
..KqqKWpWWppWWpWKqqK..
..KqqKWWWKWWKWWWKqqK..
...KqKWWWWKKWWWWKqK...
....KKKKKKKKKKKKKK....
.....KCCCCNNCCCCK.....
.....KssssssssssK.....
....KKssssCCssssKK....
...KsKssssCCssssKsK...
...KWKssssssssssKWK...
....K.KssssssssK.K....
......KssKKKKssK......
......KssK..KssK......
.....KKKKK..KKKKK.....
"""

# ---- Table symbols (signs/tables) ----
KITTY = """
.K............K.
.KK..........KK.
.KOK........KOK.
.KOpKKKKKKKKpOK.
.KOOOOKOKOOOOOK.
KOOOOOOOOOOOOOOK
KOOKKOOOOOOKKOOK
KOOKWOOOOOOKWOOK
KoOOOOOppOOOOOoK
KooOOOKOOKOOOooK
.KOOOOOKKOOOOOK.
..KKOOOOOOOOKK..
...KOOoooooOOK..
..KOOooooooOOOK.
..KOOooooooOOOK.
..KOOKooooKOOOKK
..KKKKKKKKKKKKK.
"""

NINJA = """
.....KKKKKK.....
....KDDDDDDK....
...KDDDDDDDDK...
...KRRRRRRRRKRR.
...KbbbbbbbbK.RR
...KbKKbbKKbK...
...KDDDDDDDDK...
....KDDDDDDK....
...KKDDDDDDKK...
..KDDDDDDDDDDK..
.KDDKDDDDDDKDDK.
.KDDKRRRRRRKDDK.
.KbbKDDDDDDKbbK.
..KKKDDKKDDKKK..
....KDDKKDDK....
....KDDKKDDK....
...KKKKK.KKKKK..
"""

DOGGIE = """
....KKKKKKKK....
...KbbbbbbbbK...
.KKbbbbbbbbbbKK.
KBBKbbbbbbbbKBBK
KBBKbKKbbKKbKBBK
KBBKbKWbbKWbKBBK
KBBKbbbbbbbbKBBK
.KBKbbbKKbbbKBK.
..KKbbbKKbbbKK..
...KbbKbbKbbK...
...KbbbRRbbbK...
....KKKRRKKK....
...KCCCYCCCCK...
..KBBBBBBBBBBK..
..KBbbBBBBbbBK..
..KbbKBBBBKbbK..
..KKKK.KK.KKKK..
"""

PIRATE = """
......KKKK......
....KKKWWKKK....
..KKKKWKKWKKKK..
.KKKKKKWWKKKKKK.
KYYYYYYYYYYYYYYK
KHHHHHbbbbbbbHHK
KHbKKKbbbbbKKbHK
KHKKKKbbbbbKWbHK
KHbKKKbbbbbbbbHK
KHbbbbbbKbbbbbHK
KHbpbbbbbbbbpbYK
KHHbbKbbbbKbbHHK
KHHKbbKKKKbbKHHK
KHHHKKbbbbKKHHHK
KHHKRWRWRWRWKHHK
.KKRWRWRWRWRWKK.
.KKKKKKKKKKKKKK.
"""

ROBOT = """
.......RR.......
.......KK.......
...KKKKKKKKKK...
...KSSSSSSSSK...
..KKSCCSSCCSKK..
..KSSCCSSCCSSK..
...KSSSSSSSSK...
...KSYKYKYKSK...
...KKKKKKKKKK...
.....KSSSSK.....
..KKKKKKKKKKKK..
.KSKSSSSSSSSKSK.
.KSKSSRNCSSSKSK.
.KSKSSSSSSSSKSK.
.KKKKKKKKKKKKKK.
....KSSKKSSK....
...KKKKK.KKKKK..
"""

LLAMA = """
...K.K..........
...KLKLK........
..KLLLLLK.......
.KLKLLLLK.......
KLLLLLLLK.......
KKLLLLLLK.......
.KKKLLLLK.......
....KLLLK.......
....KRYCK.......
....KLLLK.......
....KLLLKKKKKKK.
....KLLLLLLLLLLK
...KLLRRYYNNCCLK
...KLLLLLLLLLLK.
...KLLLLLLLLLLK.
....KLKLK.KLKLK.
....KLKLK.KLKLK.
....KKKKK.KKKKK.
"""

TABLE_SPRITES = {"kitty": KITTY, "ninja": NINJA, "doggie": DOGGIE, "pirate": PIRATE,
                 "robot": ROBOT, "llama": LLAMA}


def sprite_svg(art, scale=10, colors=None):
    colors = colors or SPRITE_COLORS
    rows = [r for r in art.strip("\n").split("\n")]
    w, h = max(len(r) for r in rows), len(rows)
    bad = [i for i, r in enumerate(rows) if len(r) != w]
    assert not bad, f"sprite rows {bad} are not {w} pixels wide"
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{colors[c]}"/>')
            x += run
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w * scale}" height="{h * scale}" shape-rendering="crispEdges">\n  '
            + "\n  ".join(rects) + "\n</svg>")


def build_sprites():
    write("brand/illustrations/sasquatch.svg", sprite_svg(SASQUATCH))
    write("brand/illustrations/sasquatch-safety-goggles.svg", sprite_svg(SASQUATCH_GOGGLES))
    write("brand/illustrations/alien.svg", sprite_svg(ALIEN))
    write("brand/illustrations/saucer.svg", sprite_svg(SAUCER))
    write("brand/illustrations/sparkle.svg", sprite_svg(SPARKLE))
    white = dict(SPRITE_COLORS, K="#FFFFFF")
    write("brand/illustrations/sparkle-white.svg", sprite_svg(SPARKLE, colors=white))
    write("brand/illustrations/hex-pixel.svg", sprite_svg(HEX_PIXEL))
    write("brand/illustrations/spacecat.svg", sprite_svg(SPACECAT))
    for name, art in TABLE_SPRITES.items():
        write(f"brand/illustrations/{name}.svg", sprite_svg(art))


# ---- Electronics icons (vector, not pixel) -----------------------------------
LED_COLORS = {"red": RAINBOW["red"], "green": RAINBOW["green"], "amber": RAINBOW["orange"],
              "blue": RAINBOW["blue"], "yellow": RAINBOW["yellow"], "violet": RAINBOW["violet"]}


def led_svg(color):
    c = LED_COLORS[color]
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 120" role="img" aria-label="{color} LED">
  <defs><radialGradient id="glow"><stop offset="0" stop-color="{c}" stop-opacity=".55"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>
  <circle cx="30" cy="26" r="30" fill="url(#glow)"/>
  <path d="M22 66 V100 M38 66 V84 L44 92 V112" fill="none" stroke="{STEEL}" stroke-width="4" stroke-linecap="round"/>
  <path d="M14 60 V28 a16 16 0 0 1 32 0 V60 Z" fill="{c}" stroke="{INK}" stroke-width="3.5"/>
  <rect x="10" y="58" width="40" height="8" rx="1.5" fill="{c}" stroke="{INK}" stroke-width="3.5"/>
  <path d="M21 26 a9 9 0 0 1 7 -9" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>
</svg>"""


RESISTOR_BANDS = ["#16181D", "#7A4A2A", RAINBOW["red"], RAINBOW["orange"], RAINBOW["yellow"],
                  RAINBOW["green"], RAINBOW["blue"], RAINBOW["violet"], "#8A8F94", "#FFFFFF"]
GOLD = "#C9A227"


def resistor_svg(bands):
    """bands: list of colour hex strings, 3-5 of them. Last band is drawn apart (tolerance)."""
    xs = [56, 72, 88, 104, 120][:len(bands)]
    if len(bands) <= 4:
        xs = [56, 74, 92, 118][:len(bands)]
    shapes = ('<rect x="40" y="4" width="34" height="44" rx="12"/>'
              '<rect x="106" y="4" width="34" height="44" rx="12"/>'
              '<rect x="60" y="9" width="60" height="34"/>')
    band_svg = "".join(f'<rect x="{x}" y="0" width="9" height="52" fill="{b}"/>' for x, b in zip(xs, bands))
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 52" role="img" aria-label="resistor">
  <defs><clipPath id="body">{shapes}</clipPath></defs>
  <path d="M2 26 H40 M140 26 H178" stroke="{STEEL}" stroke-width="4" stroke-linecap="round"/>
  <g fill="{INK}" stroke="{INK}" stroke-width="6">{shapes}</g>
  <g fill="#E9CFA1">{shapes}</g>
  <g clip-path="url(#body)">{band_svg}</g>
</svg>"""


def build_icons():
    for name in LED_COLORS:
        write(f"brand/illustrations/led-{name}.svg", led_svg(name))
    # 1k ohm, 5% : brown black red gold
    write("brand/illustrations/resistor.svg",
          resistor_svg([RESISTOR_BANDS[1], RESISTOR_BANDS[0], RESISTOR_BANDS[2], GOLD]))
    # The "rainbow" resistor: R-O-Y-G (purely decorative)
    write("brand/illustrations/resistor-rainbow.svg",
          resistor_svg([RAINBOW["red"], RAINBOW["orange"], RAINBOW["yellow"], RAINBOW["green"], RAINBOW["blue"]]))


# ---- Equipment diagrams ------------------------------------------------------
# A cereal-box filament bunker, drawn front-on: body, flip lid, side catch, and
# the spool behind the translucent wall. Two push-fit fittings stand in the lid:
# the outside one, near the catch edge, feeds filament up from the spool; the
# middle one is only a holder and doesn't go through the lid. In storage the
# PTFE tube loops from the outside fitting to the middle one, so the filament
# end stays inside the tube. Both states share the same geometry, so a right/wrong
# pair on a sign differs only where it is making its point: shut and looped, or
# lid up with the catch open, the tube out of its fitting and the spool left
# outside. While printing, the tube runs from the outside fitting to a generic
# printer drawn beside the box, and the middle fitting stands empty.
import math as _math

BK = dict(
    body=(50, 124, 250, 152),      # x, y, w, h
    lid=(42, 96, 266, 28),         # closed lid, sitting on the rim
    hinge=(308, 110),              # lid pivot, at the back right
    spool=(175, 204, 50),          # cx, cy, r
    ports=(64, 161),               # left edge of the outside and middle fittings
    tilt=16,                       # how far the lid tips in the open state
)
PORT_W, PORT_H = 28, 28            # fitting body on top of the lid


def _rot(x, y, deg, cx, cy):
    a = _math.radians(deg)
    return (cx + (x - cx) * _math.cos(a) - (y - cy) * _math.sin(a),
            cy + (x - cx) * _math.sin(a) + (y - cy) * _math.cos(a))


def bunker_svg(stored=True, printing=False):
    bx, by, bw, bh = BK["body"]
    lx, ly, lw, lh = BK["lid"]
    hx, hy = BK["hinge"]
    sx, sy, sr = BK["spool"]
    pa, pb = BK["ports"]
    tilt = 0 if stored else BK["tilt"]
    wall = f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"'
    mouth_y = ly - PORT_H - 10          # top of a fitting collar

    def port(x):
        """A push-fit fitting standing in the lid, mouth up."""
        return (f'<rect x="{x}" y="{ly - PORT_H}" width="{PORT_W}" height="{PORT_H}"/>'
                f'<rect x="{x - 6}" y="{mouth_y}" width="{PORT_W + 12}" height="14"/>')

    lid_t = "" if stored else f' transform="rotate({tilt} {hx} {hy})"'
    lid = (f'<g{lid_t}><g fill="{STEEL}" {wall}>{port(pa)}{port(pb)}</g>'
           f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{PAPER}" {wall}/></g>')

    # Side catch: clipped over the lid joint, or swung open below it.
    cx0 = bx - 14
    def catch(top, hook_at_top):
        hook_y = top - 4 if hook_at_top else top + 34
        return (f'<rect x="{cx0}" y="{top}" width="26" height="48" fill="{STEEL}" {wall}/>'
                f'<rect x="{cx0 - 7}" y="{hook_y}" width="40" height="15" fill="{INK}"/>')
    latch = (catch(ly + 10, True) if stored
             else f'<g transform="rotate(16 {cx0 + 13} {by + 18})">{catch(by + 18, False)}</g>')

    spool = (f'<g fill="none" stroke="{STEEL}" stroke-width="6">'
             f'<circle cx="{sx}" cy="{sy}" r="{sr}"/>'
             f'<circle cx="{sx}" cy="{sy}" r="{sr - 14}" stroke-width="3"/></g>'
             f'<circle cx="{sx}" cy="{sy}" r="14" fill="{STEEL}"/>')
    if not stored:
        # The spool has been taken out and left on the bench beside the box.
        ox, oy = bx + bw + 62, by + bh + 3 - sr
        spool = (f'<circle cx="{ox}" cy="{oy}" r="{sr}" fill="{PAPER}" {wall}/>'
                 f'<circle cx="{ox}" cy="{oy}" r="{sr - 14}" fill="none" stroke="{STEEL}" stroke-width="4"/>'
                 f'<circle cx="{ox}" cy="{oy}" r="14" fill="{STEEL}" stroke="{INK}" stroke-width="3"/>')

    def tube(d):
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="10" stroke-linecap="round"/>')

    def filament(d):
        return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'

    ax, bx2 = pa + PORT_W / 2, pb + PORT_W / 2      # centre line of each fitting
    top = mouth_y + 2
    printer = ""
    view = "24 -12 296 294"
    feed = filament(f"M{sx - 36} {sy - 35} C{sx - 47} {sy - 52} {ax - 2} {ly + 42} {ax} {ly + 24}")
    if printing:
        # A generic printer: frame, gantry with the toolhead, bed. Floor shared with the bunker.
        fx, fy, fw, fh = 360, 40, 200, by + bh - 40
        px = fx + 50                                  # fitting on the printer's top
        printer = (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{PAPER}" {wall}/>'
                   f'<rect x="{fx + 22}" y="{fy + 22}" width="{fw - 44}" height="{fh - 44}" fill="none" '
                   f'stroke="{STEEL}" stroke-width="4"/>'
                   f'<rect x="{fx + 22}" y="{fy + 70}" width="{fw - 44}" height="12" fill="{STEEL}" {wall}/>'
                   f'<rect x="{fx + 74}" y="{fy + 58}" width="46" height="56" fill="{STEEL}" {wall}/>'
                   f'<rect x="{fx + 91}" y="{fy + 114}" width="12" height="14" fill="{INK}"/>'
                   f'<rect x="{fx + 40}" y="{fy + fh - 58}" width="{fw - 80}" height="14" fill="{STEEL}" {wall}/>'
                   f'<g fill="{STEEL}" {wall}><rect x="{px - PORT_W / 2}" y="{fy - PORT_H}" width="{PORT_W}" height="{PORT_H}"/>'
                   f'<rect x="{px - PORT_W / 2 - 6}" y="{fy - PORT_H - 10}" width="{PORT_W + 12}" height="14"/></g>')
        ptop = fy - PORT_H - 8
        hose = tube(f"M{ax} {top} C{ax} {top - 90} {px} {ptop - 90} {px} {ptop}")
        strand = feed
        view = "24 -40 556 322"
    if stored and not printing:
        # The tube loops from one lid fitting to the other, both ends home.
        hose = tube(f"M{ax} {top} C{ax} {top - 70} {bx2} {top - 70} {bx2} {top}")
        # Filament: up from the spool into the outside fitting. Its end waits in the tube.
        strand = feed
    elif not printing:
        # Lid up, the tube pulled out of the outside fitting and left hanging.
        hx0, hy0 = _rot(ax, top, tilt, hx, hy)
        hose = tube(f"M{hx0:.0f} {hy0:.0f} C{hx0 - 76:.0f} {hy0 + 16:.0f} "
                    f"{bx - 44} {by + 70} {bx - 16} {by + bh + 2}")
        strand = ""
        view = "24 -12 400 294"

    label = ("filament bunker shut, catch clipped, PTFE tube running from its outside lid fitting into a 3D printer"
             if printing else
             "filament bunker shut, catch clipped, PTFE tube looped from the outside lid fitting to the middle one"
             if stored else
             "filament bunker with the lid up, the catch open, the tube out of its fitting and the spool outside")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{label}">
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{PAPER}" {wall}/>
  {spool}
  {strand}
  {hose}
  {lid}
  <circle cx="{hx}" cy="{hy}" r="6" fill="{STEEL}" stroke="{INK}" stroke-width="3"/>
  {latch}{printer}
</svg>"""


def build_diagrams():
    write("brand/illustrations/bunker-latched.svg", bunker_svg(stored=True))
    write("brand/illustrations/bunker-open.svg", bunker_svg(stored=False))
    write("brand/illustrations/bunker-printing.svg", bunker_svg(printing=True))


# ---- Patterns ----------------------------------------------------------------
def build_patterns():
    # Seamless pointy-top honeycomb outline tile
    r = 20
    w = math.sqrt(3) * r
    h = 3 * r
    cells = [(w / 2, r), (0, r + 1.5 * r), (w, r + 1.5 * r), (w / 2, r + 3 * r), (0, -r / 2), (w, -r / 2)]
    polys = "".join(f'<polygon points="{pts(hex_points(x, y, r))}"/>' for x, y in cells)
    write("brand/patterns/honeycomb.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" width="{fmt(w)}" height="{fmt(h)}">
  <g fill="none" stroke="currentColor" stroke-width="1.5">{polys}</g>
</svg>""")

    # The rainbow trail: six stepped bars, like the mural.
    bars = []
    bw, bh, seg = 60, 10, 6
    for i, c in enumerate(R_ORDER):
        for s in range(seg):
            dy = 0 if s % 2 == 0 else 3
            bars.append(f'<rect x="{s * bw}" y="{i * bh + dy}" width="{bw}" height="{bh}" fill="{RAINBOW[c]}"/>')
    write("brand/patterns/rainbow-trail.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw * seg} {bh * 6 + 3}" preserveAspectRatio="none" shape-rendering="crispEdges">
  {''.join(bars)}
</svg>""")


if __name__ == "__main__":
    build_logo()
    build_sprites()
    build_icons()
    build_diagrams()
    build_patterns()
