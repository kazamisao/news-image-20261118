"""Draw the news-image-20261118 entry: a one-page broadsheet of the world
news of Wednesday, 18 November 2026.

Renders at 3x with Pillow and downscales with LANCZOS (pil_image_craft).
Pure vector drawing: no photos, no raster assets. Deterministic: no clock,
no unseeded random. Writes news.png next to this file.

Layout (1024x1024): masthead with the date; a hero panel on the Kerch
Bridge collapse with a Kyiv counter-strike note; four panels (Bahrain
drones, Trump in Manila, Cyclone Akvan, Nvidia/Huang); an "Also today"
strip (UK sanctions, Canada-China trade, Dhoni, Hormuz tanker).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 3  # supersample factor
W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (246, 241, 227)
CREAM = (255, 251, 238)
NAVY = (22, 35, 63)
NAVY_DK = (14, 24, 46)
INK = (27, 27, 27)
RED = (179, 39, 30)
GOLD = (217, 164, 65)
GREY = (110, 108, 100)
SKY_TOP = (28, 40, 78)
SKY_HOR = (232, 150, 74)
SEA_TOP = (30, 58, 96)
SEA_BOT = (16, 32, 58)


def fnt(path, size):
    return ImageFont.truetype(path, int(round(size * S)))


def sc(v):
    return int(round(v * S))


def X(x):
    return sc(x)


def Y(y):
    return sc(y)


def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])],
                fill=fill, outline=outline, width=sc(width))


def ell(d, box, fill=None, outline=None, width=1):
    d.ellipse([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])],
              fill=fill, outline=outline, width=sc(width))


def poly(d, pts, fill=None, outline=None):
    d.polygon([(sc(x), sc(y)) for x, y in pts], fill=fill, outline=outline)


def seg(d, pts, fill, width=1):
    d.line([(sc(x), sc(y)) for x, y in pts], fill=fill, width=sc(width))


def hline(d, x0, x1, y, fill, width=1):
    d.line([(sc(x0), sc(y)), (sc(x1), sc(y))], fill=fill, width=sc(width))


def vline(d, x, y0, y1, fill, width=1):
    d.line([(sc(x), sc(y0)), (sc(x), sc(y1))], fill=fill, width=sc(width))


def txt(d, pos, s, font, fill):
    d.text((sc(pos[0]), sc(pos[1])), s, font=font, fill=fill)


def tracked(d, pos, s, font, fill, gap=5):
    """Draw caps text with extra letter spacing (gap in final px)."""
    x, y = pos
    for ch in s:
        d.text((sc(x), sc(y)), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) / S + gap


def wrap(d, text, font, max_w):
    """Greedy word wrap to max_w (final px)."""
    out, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= sc(max_w):
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def block(d, x, y, lines, font, fill, leading=1.28):
    """Draw wrapped lines; return the y just below the last line."""
    size = font.size / S
    for ln in lines:
        txt(d, (x, y), ln, font, fill)
        y += size * leading
    return y


def fit(d, path, size, text, max_w, min_size=14):
    """Largest size <= size that fits text on one line."""
    s = size
    while s > min_size:
        f = fnt(path, s)
        if d.textlength(text, font=f) <= sc(max_w):
            return f
        s -= 1
    return fnt(path, min_size)


def gradient(d, box, top, bottom):
    """Vertical gradient across a box (final px coords)."""
    x0, y0, x1, y1 = box
    for i in range(sc(y1 - y0)):
        t = i / max(1, sc(y1 - y0) - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(sc(x0), sc(y0) + i), (sc(x1), sc(y0) + i)], fill=c)


# ---------------------------------------------------------------- masthead
def masthead(d):
    txt(d, (24, 12), "THE WORLD", fnt(SERIF_B, 56), NAVY)
    # right-hand tag, two lines, right aligned
    tag = fnt(SANS_B, 21)
    for i, line in enumerate(["ONE DAY IN", "WORLD NEWS"]):
        w = d.textlength(line, font=tag) / S
        txt(d, (1000 - w, 18 + i * 26), line, tag, RED)
    hline(d, 24, 1000, 80, NAVY, 2)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    df = fit(d, SERIF_B, 24, date, 620)
    w = d.textlength(date, font=df) / S
    x = (W - w) / 2
    ell(d, (x - 22, 89, x - 10, 101), fill=RED)
    ell(d, (x + w + 10, 89, x + w + 22, 101), fill=RED)
    txt(d, (x, 83), date, df, NAVY)


# ---------------------------------------------------------------- hero art
def hero_art(d, box):
    """Kerch Bridge at dusk: deck broken, arch span down in the strait."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    horizon = y0 + 148
    gradient(d, (x0, y0, x1, horizon), SKY_TOP, SKY_HOR)
    gradient(d, (x0, horizon, x1, y1), SEA_TOP, SEA_BOT)
    # low sun, upper right
    ell(d, (x0 + 852, y0 + 26, x0 + 908, y0 + 82), fill=(250, 214, 150))
    ell(d, (x0 + 868, y0 + 42, x0 + 892, y0 + 66), fill=(254, 236, 190))
    deck_y = y0 + 150
    # towers
    for tx in (x0 + 205, x0 + 785):
        rect(d, (tx - 5, deck_y - 108, tx + 5, deck_y), fill=NAVY_DK)
        rect(d, (tx - 34, deck_y - 108, tx + 34, deck_y - 100), fill=NAVY_DK)
        rect(d, (tx - 30, deck_y - 62, tx + 30, deck_y - 54), fill=NAVY_DK)
    # stay cables from tower tops to the deck
    for tx in (x0 + 205, x0 + 785):
        for dx in (-120, -70, -25, 25, 70, 120):
            seg(d, [(tx, deck_y - 104), (tx + dx, deck_y)], (200, 205, 220), 1)
    # intact deck, left and right of the gap
    hline(d, x0, x0 + 420, deck_y, (235, 238, 244), 7)
    hline(d, x0 + 600, x1, deck_y, (235, 238, 244), 7)
    # the arch: left half stands, right half has fallen away
    cx, cy, rx, ry = x0 + 510, deck_y, 200, 72
    pts = []
    for deg in range(180, 100, -3):
        a = math.radians(deg)
        pts.append((cx + rx * math.cos(a), cy - ry * math.sin(a)))
    seg(d, pts, (235, 238, 244), 6)
    # fallen span: a deck slab tilted down into the water
    poly(d, [(x0 + 424, deck_y - 4), (x0 + 520, deck_y + 46),
             (x0 + 528, deck_y + 56), (x0 + 430, deck_y + 6)],
         fill=(190, 196, 208))
    # arch fragment plunging with it
    seg(d, [(x0 + 470, deck_y - 58), (x0 + 540, deck_y + 40)],
        (210, 216, 226), 6)
    # fire glow at the break
    ell(d, (x0 + 486, deck_y - 22, x0 + 522, deck_y + 8), fill=(240, 140, 50))
    ell(d, (x0 + 496, deck_y - 12, x0 + 514, deck_y + 2), fill=(252, 210, 110))
    # smoke rising from the break: a narrow plume, not a cloud
    for (sx, sy, sr) in ((500, 108, 16), (508, 84, 20), (496, 60, 16),
                         (510, 40, 12)):
        ell(d, (x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr),
            fill=(120, 122, 128))
    # waves and splash around the fallen span
    for wy in (deck_y + 30, deck_y + 52, deck_y + 74):
        for wx in range(x0 + 30, x1 - 60, 90):
            seg(d, [(wx, wy), (wx + 34, wy)], (150, 175, 205), 2)
    for (sx, sy, sr) in ((540, 210, 22), (512, 216, 15), (566, 214, 12)):
        d.arc([sc(x0 + sx - sr), sc(y0 + sy - sr), sc(x0 + sx + sr),
               sc(y0 + sy + sr)], 180, 360, fill=(210, 222, 235),
              width=sc(2))


# ---------------------------------------------------------------- hero caption
def hero_caption(d):
    rect(d, (12, 336, 1012, 442), fill=NAVY)
    txt(d, (28, 346), "KERCH BRIDGE FALLS", fnt(SERIF_B, 42), (255, 255, 255))
    deck = ("Ukraine hits Putin's Crimea link a second day \u2014 a road span "
            "falls into the strait and road and rail traffic stops.")
    df = fnt(SANS, 18)
    end = block(d, 28, 394, wrap(d, deck, df, 630), df, (214, 220, 232), 1.3)
    assert end <= 442, "hero deck overflows the caption band"
    vline(d, 692, 350, 432, (120, 132, 160), 1)
    txt(d, (708, 348), "KYIV: RUSSIA STRIKES BACK",
        fnt(SANS_B, 16), GOLD)
    kyiv = ("Northern and Southern Dnipro bridges hit; metro damaged, "
            "power and heat cut.")
    kf = fnt(SANS, 16)
    end = block(d, 708, 374, wrap(d, kyiv, kf, 288), kf, (232, 236, 244), 1.3)
    assert end <= 442, "Kyiv note overflows the hero caption band"


# ---------------------------------------------------------------- panels
def icon_bahrain(d, x, y):
    """Night sky, radar arcs, a drone."""
    rect(d, (x, y, x + 220, y + 106), fill=(16, 26, 52))
    for r in (24, 44, 64):
        d.arc([sc(x + 8 - r), sc(y + 98 - r), sc(x + 8 + r), sc(y + 98 + r)],
              270, 360, fill=(110, 190, 120), width=sc(2))
    # drone silhouette
    bx, by = x + 118, y + 34
    ell(d, (bx - 26, by - 8, bx + 26, by + 8), fill=(235, 238, 244))
    seg(d, [(bx - 34, by - 14), (bx + 34, by - 14)], (235, 238, 244), 3)
    seg(d, [(bx - 34, by + 14), (bx + 34, by + 14)], (235, 238, 244), 3)
    for px in (bx - 34, bx + 34):
        ell(d, (px - 8, by - 22, px + 8, by - 6), fill=(180, 185, 195))
        ell(d, (px - 8, by + 6, px + 8, by + 22), fill=(180, 185, 195))
    # two distant drones, panel-local coords
    for (dx, dy) in ((186, 28), (202, 50)):
        ell(d, (x + dx - 5, y + dy - 3, x + dx + 5, y + dy + 3),
            fill=(235, 238, 244))
    txt(d, (x + 80, y + 82), "INTERCEPTED", fnt(SANS_B, 14), (110, 190, 120))


def icon_manila(d, x, y):
    """Jet over a bay skyline at sunrise."""
    gradient(d, (x, y, x + 220, y + 106), (250, 214, 150), (250, 240, 245))
    ell(d, (x + 168, y + 12, x + 206, y + 50), fill=(240, 170, 60))
    # skyline
    base = y + 106
    for (bx, bw, bh) in ((0, 34, 34), (38, 26, 52), (68, 40, 28),
                         (112, 30, 60), (146, 28, 40), (178, 42, 48)):
        rect(d, (x + bx, base - bh, x + bx + bw, base), fill=NAVY)
    # jet
    jx, jy = x + 96, y + 30
    poly(d, [(jx - 46, jy), (jx - 18, jy - 7), (jx + 34, jy - 7),
             (jx + 52, jy), (jx + 34, jy + 7), (jx - 18, jy + 7)],
         fill=(255, 255, 255))
    poly(d, [(jx - 6, jy - 6), (jx + 10, jy - 26), (jx + 18, jy - 6)],
         fill=(255, 255, 255))
    poly(d, [(jx - 2, jy + 6), (jx + 8, jy + 22), (jx + 16, jy + 6)],
         fill=(255, 255, 255))
    seg(d, [(jx - 52, jy + 2), (jx - 78, jy + 6)], (255, 255, 255), 2)


def icon_akvan(d, x, y):
    """Cyclone spiral over waves."""
    rect(d, (x, y, x + 220, y + 106), fill=(24, 68, 96))
    cx, cy = x + 110, y + 52
    for r in (46, 36, 26, 16):
        d.arc([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
              20 + r, 300 + r, fill=(235, 240, 245), width=sc(3))
    ell(d, (cx - 6, cy - 6, cx + 6, cy + 6), fill=(250, 214, 150))
    for wx in range(x + 8, x + 212, 34):
        seg(d, [(wx, y + 92), (wx + 20, y + 92)], (150, 200, 225), 2)


def icon_nvidia(d, x, y):
    """A chip with an upward arrow."""
    rect(d, (x, y, x + 220, y + 106), fill=(20, 44, 40))
    cx, cy = x + 88, y + 53
    rect(d, (cx - 34, cy - 34, cx + 34, cy + 34), fill=(28, 92, 66))
    rect(d, (cx - 20, cy - 20, cx + 20, cy + 20), fill=(52, 140, 96))
    for px in range(cx - 26, cx + 27, 13):
        rect(d, (px - 2, cy - 44, px + 2, cy - 34), fill=(200, 210, 205))
        rect(d, (px - 2, cy + 34, px + 2, cy + 44), fill=(200, 210, 205))
    for py in range(cy - 26, cy + 27, 13):
        rect(d, (cx - 44, py - 2, cx - 34, py + 2), fill=(200, 210, 205))
        rect(d, (cx + 34, py - 2, cx + 44, py + 2), fill=(200, 210, 205))
    # upward arrow, right side
    ax = x + 178
    poly(d, [(ax, y + 22), (ax - 14, y + 44), (ax - 6, y + 44),
             (ax - 6, y + 82), (ax + 6, y + 82), (ax + 6, y + 44),
             (ax + 14, y + 44)], fill=(110, 190, 120))


PANELS = [
    ("THE GULF", "Drones over Bahrain",
     "Iran's third attack in five days on a US radar at Isa air base. "
     "Bahrain and the US say every drone was intercepted \u2014 no damage, "
     "no injuries.", icon_bahrain),
    ("ASIA", "Trump lands in Manila",
     "Quad talks open ahead of a China visit. Xi, Trump and Putin are due "
     "to meet in Shenzhen on Thursday.", icon_manila),
    ("WEATHER", "Cyclone Akvan builds",
     "The Bay of Bengal storm is set to turn severe by Thursday. "
     "Chennai\u2013Yangon flights are cancelled.", icon_akvan),
    ("TECH", "Huang open to return",
     "Nvidia's former chief says he would take the top job back. Trump "
     "backs him; the board refuses. The US curbs China's remote chip "
     "access.", icon_nvidia),
]


def panels(d):
    y0 = 454
    for i, (kicker, head, body, icon) in enumerate(PANELS):
        x = 12 + i * 252
        rect(d, (x, y0, x + 244, y0 + 336), fill=CREAM, outline=NAVY, width=1)
        rect(d, (x, y0, x + 244, y0 + 6), fill=RED)
        icon(d, x + 12, y0 + 18)
        tracked(d, (x + 12, y0 + 134), kicker, fnt(SANS_B, 15), RED, 4)
        hf = fnt(SERIF_B, 25)
        block(d, x + 12, y0 + 158, wrap(d, head, hf, 220), hf, NAVY, 1.15)
        bf = fnt(SANS, 16)
        end = block(d, x + 12, y0 + 212, wrap(d, body, bf, 220), bf, INK, 1.28)
        assert end <= y0 + 336, f"panel {kicker} body overflows its box"


# ---------------------------------------------------------------- also strip
ALSO = [
    ("UK SANCTIONS",
     "Britain sanctions Israeli settlement firms in a push for a two-state solution."),
    ("TRADE",
     "Canada and China extend trade deals as Xi meets PM Carney before APEC."),
    ("CRICKET",
     "MS Dhoni retires from IPL play and becomes Chennai Super Kings mentor."),
    ("HORMUZ",
     "India condemns the attack on LPG tanker MT Tara Gas; 21 of 24 crew ashore safe."),
]


def also_strip(d):
    hline(d, 12, 1012, 798, NAVY, 2)
    tracked(d, (24, 808), "ALSO TODAY", fnt(SANS_B, 18), RED, 5)
    for i, (lead, body) in enumerate(ALSO):
        x = 24 + i * 244
        txt(d, (x, 838), lead, fnt(SANS_B, 18), NAVY)
        bf = fnt(SANS, 16)
        end = block(d, x, 862, wrap(d, body, bf, 232), bf, INK, 1.28)
        assert end < 936, f"ALSO item {lead} collides with the footer rule"


def footer(d):
    hline(d, 12, 1012, 936, NAVY, 1)
    note = ("Drawn in code with Pillow  \u00b7  Events first reported Wednesday, "
            "18 November 2026  \u00b7  Sources: AP, Reuters, BBC, Al Jazeera")
    ff = fnt(SANS, 15)
    w = d.textlength(note, font=ff) / S
    txt(d, ((W - w) / 2, 950), note, ff, GREY)


def render():
    img = Image.new("RGB", (sc(W), sc(H)), PAPER)
    d = ImageDraw.Draw(img)
    rect(d, (4, 4, 1020, 1020), outline=NAVY, width=2)
    masthead(d)
    hero_art(d, (12, 110, 1012, 336))
    hero_caption(d)
    panels(d)
    also_strip(d)
    footer(d)
    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(HERE, "news.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
