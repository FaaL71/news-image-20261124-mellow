#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news infographic (1024x1024 PNG).

"The Day in the World": a map-led front page. A simplified world map
carries a numbered dot for each of the day's six biggest stories, then a
timeline tells each story in two lines, with an ALSO TODAY strip for the
rest. Everything is drawn in code with PIL: no photos, no network, and
the same input always produces the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---
PAPER = (247, 243, 234)
TEAL = (13, 56, 56)
TEAL_DARK = (9, 42, 42)
AMBER = (224, 148, 38)
AMBER_DARK = (170, 106, 18)
INK = (28, 42, 42)
BODY = (72, 88, 86)
FAINT = (118, 130, 123)
PANEL = (236, 239, 232)
SEA = (214, 228, 226)
LAND = (139, 175, 162)
LAND_LINE = (106, 145, 133)
WHITE = (255, 255, 255)
RULE = (198, 205, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans.ttf", 23)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_MAP_TITLE = font("DejaVuSans-Bold.ttf", 15)
F_MAP_LABEL = font("DejaVuSans-Bold.ttf", 14)
F_NUM = font("DejaVuSans-Bold.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 23)
F_DETAIL = font("DejaVuSans.ttf", 17)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_STRIP_TITLE = font("DejaVuSans-Bold.ttf", 15)
F_STRIP = font("DejaVuSans.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 13)

# --- simplified continents, as (lon, lat) outlines ---
NORTH_AMERICA = [
    (-168, 66), (-162, 60), (-155, 58), (-150, 61), (-142, 60), (-135, 58),
    (-130, 54), (-126, 49), (-124, 43), (-121, 36), (-115, 30), (-110, 24),
    (-105, 20), (-100, 18), (-95, 16), (-92, 15), (-88, 13), (-84, 11),
    (-81, 9), (-79, 8), (-78, 7), (-80, 9), (-83, 9), (-86, 13), (-87, 15),
    (-88, 18), (-90, 21), (-91, 19), (-94, 18), (-97, 20), (-97, 26),
    (-94, 29), (-90, 29), (-85, 30), (-82, 28), (-80, 26), (-81, 31),
    (-78, 34), (-75, 37), (-74, 40), (-70, 42), (-68, 44), (-65, 45),
    (-60, 46), (-55, 47), (-54, 50), (-58, 53), (-62, 55), (-66, 58),
    (-70, 60), (-76, 62), (-82, 65), (-88, 66), (-92, 68), (-100, 69),
    (-110, 68), (-120, 69), (-130, 70), (-140, 70), (-150, 71), (-160, 71),
    (-166, 68),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 6), (-78, 2), (-80, -3), (-81, -6), (-79, -10),
    (-75, -15), (-72, -18), (-70, -22), (-70, -28), (-71, -33), (-72, -38),
    (-73, -44), (-73, -50), (-70, -53), (-66, -55), (-66, -50), (-64, -45),
    (-62, -40), (-58, -35), (-54, -34), (-50, -30), (-46, -26), (-42, -23),
    (-38, -18), (-35, -12), (-35, -7), (-37, -4), (-41, -3), (-44, -2),
    (-48, 0), (-52, 4), (-55, 6), (-60, 8), (-64, 10), (-68, 11),
    (-72, 12), (-76, 11), (-79, 10),
]
AFRICA = [
    (-6, 35), (-10, 31), (-13, 28), (-16, 23), (-17, 19), (-17, 15),
    (-16, 12), (-13, 8), (-10, 6), (-7, 4), (-4, 5), (0, 6), (4, 6),
    (7, 4), (9, 3), (9, 0), (11, -3), (13, -7), (13, -12), (12, -17),
    (13, -22), (14, -27), (16, -29), (19, -33), (24, -34), (28, -33),
    (32, -29), (35, -25), (38, -20), (40, -16), (40, -11), (42, -6),
    (44, -2), (47, 0), (51, 2), (51, 8), (48, 11), (44, 11), (41, 13),
    (39, 16), (37, 19), (35, 22), (34, 26), (32, 30), (30, 32), (26, 33),
    (22, 33), (18, 32), (14, 32), (11, 34), (10, 37), (7, 37), (3, 37),
    (-1, 35),
]
EURASIA = [
    (-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-4, 48), (-1, 49),
    (1, 51), (4, 52), (7, 54), (8, 57), (10, 59), (6, 60), (6, 62),
    (11, 64), (16, 68), (20, 70), (25, 71), (30, 70), (35, 68), (42, 67),
    (48, 68), (54, 68), (60, 69), (66, 69), (72, 71), (78, 72), (85, 73),
    (92, 75), (100, 76), (108, 76), (115, 73), (122, 72), (130, 71),
    (138, 72), (146, 72), (154, 70), (162, 69), (170, 67), (178, 65),
    (178, 63), (172, 60), (166, 60), (162, 56), (158, 52), (156, 50),
    (150, 56), (144, 59), (141, 52), (140, 46), (136, 43), (132, 42),
    (128, 39), (126, 38), (122, 38), (120, 34), (116, 32), (112, 29),
    (108, 25), (106, 20), (104, 15), (101, 10), (99, 7), (100, 4),
    (103, 1), (104, 2), (102, 6), (100, 8), (98, 10), (96, 14), (94, 17),
    (91, 21), (89, 22), (87, 21), (85, 19), (82, 17), (80, 14), (78, 8),
    (76, 10), (74, 14), (72, 19), (70, 21), (67, 24), (64, 25), (61, 25),
    (58, 25), (56, 27), (53, 26), (50, 28), (48, 30), (45, 29), (42, 29),
    (39, 28), (36, 28), (34, 29), (32, 31), (30, 31), (27, 32), (25, 32),
    (23, 33), (21, 33), (19, 32), (17, 32), (15, 32), (13, 33), (11, 34),
    (9, 35), (7, 36), (5, 37), (3, 37), (0, 36), (-2, 36), (-5, 36),
    (-8, 37), (-10, 36),
]
# Arabian peninsula as its own bump, drawn over the Eurasia edge.
ARABIA = [
    (52, 25), (50, 27), (47, 29), (44, 29), (40, 28), (36, 28), (35, 24),
    (38, 21), (40, 17), (43, 13), (45, 12), (48, 14), (51, 15), (54, 17),
    (57, 19), (59, 22), (56, 25), (53, 24),
]
AUSTRALIA = [
    (113, -22), (114, -30), (115, -34), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
    (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
    (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
    (122, -17), (118, -20), (114, -21),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-45, 60), (-40, 64), (-35, 68), (-30, 70),
    (-25, 72), (-20, 74), (-22, 76), (-30, 78), (-40, 80), (-50, 78),
    (-58, 76), (-62, 72), (-60, 68),
]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)]
JAPAN = [
    (130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
    (141, 39), (141, 42), (143, 42), (145, 44), (143, 44), (141, 41),
    (139, 38), (137, 36), (135, 34), (132, 33), (130, 32),
]
MADAGASCAR = [
    (44, -16), (47, -15), (50, -16), (50, -20), (48, -24), (45, -25),
    (43, -22), (43, -18),
]
NEW_ZEALAND = [
    (167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
    (175, -40), (173, -42), (170, -44), (167, -46),
]
LANDS = [
    NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, ARABIA, AUSTRALIA,
    GREENLAND, BRITAIN, JAPAN, MADAGASCAR, NEW_ZEALAND,
]

# --- the six stories: (number, place, lon, lat, headline, detail, tag,
#                      label dx, label dy, label anchor) ---
STORIES = [
    (1, "RIYADH", 46.7, 24.7,
     "Houthi missile hits Riyadh's tallest tower",
     "PIF Tower struck a second time in a week; 11 people hurt",
     "SAUDI ARABIA", 14, -10, "l"),
    (2, "POLAND", 21.0, 52.2,
     "NATO sends AWACS watch over Poland",
     "Surveillance jets after Russian missiles landed in Poland",
     "NATO", -14, -10, "r"),
    (3, "GAZA", 34.5, 31.5,
     "Israeli strikes kill Hamas security chief",
     "Naeem Abu Nahel among seven killed in Gaza strikes",
     "GAZA", -14, -10, "r"),
    (4, "ZAPORIZHZHIA", 35.2, 47.8,
     "Overnight strike hits apartment block",
     "Two killed, 40 wounded \u2014 among them four children",
     "UKRAINE", 14, -10, "l"),
    (5, "SANTA CLARA", -122.0, 37.4,
     "Jensen Huang back as Nvidia chief",
     "Reinstated as CEO under two weeks after resigning",
     "USA", 14, -10, "l"),
    (6, "DAKAR", -17.4, 14.7,
     "CAS restores Senegal as AFCON champions",
     "Court overturns CAF ruling; 1\u20130 win over Morocco stands",
     "FOOTBALL", -14, 18, "r"),
]

ALSO_TODAY = [
    "Russia warns Estonia of \u201copen war\u201d over border closures",
    "S&P 500 falls 0.95% as rate worries cool markets",
    "New count: 700,000+ Russian soldiers killed in Ukraine",
    "Spain\u2019s top court amnesties Carles Puigdemont",
]

# --- map geometry: equirectangular, lon -180..180, lat 84..-58 ---
MAP_X, MAP_Y, MAP_W, MAP_H = 36, 158, 952, 300


def project(lon, lat):
    x = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y + (84.0 - lat) / (84.0 + 58.0) * MAP_H
    return x, y


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_map(d):
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                fill=SEA, outline=RULE, width=2)
    d.text((MAP_X + 14, MAP_Y + 10), "WHERE TODAY HAPPENED",
           font=F_MAP_TITLE, fill=TEAL)
    for land in LANDS:
        pts = [project(lon, lat) for lon, lat in land]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for n, place, lon, lat, _h, _dt, _t, dx, dy, anchor in STORIES:
        x, y = project(lon, lat)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=AMBER,
                  outline=TEAL_DARK, width=2)
        label = str(n)
        tw = d.textlength(label, font=F_NUM)
        d.text((x - tw / 2, y - 10), label, font=F_NUM, fill=TEAL_DARK)
        lx, ly = x + dx, y + dy
        if anchor == "r":
            tw = d.textlength(place, font=F_MAP_LABEL)
            lx -= tw
        d.text((lx, ly), place, font=F_MAP_LABEL, fill=TEAL_DARK)


def draw_masthead(d):
    d.rectangle([0, 0, W, 118], fill=TEAL)
    d.rectangle([0, 118, W, 122], fill=AMBER)
    d.text((36, 22), "THE DAY IN THE WORLD", font=F_MAST, fill=WHITE)
    d.text((36, 76), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE,
           fill=(235, 196, 120))
    tag = "6 STORIES \u00b7 1 DAY"
    tw = d.textlength(tag, font=F_KICK)
    d.rectangle([W - 36 - tw - 28, 30, W - 36, 30 + 40], outline=AMBER, width=2)
    d.text((W - 36 - tw - 14, 39), tag, font=F_KICK, fill=AMBER)
    d.text((36, 132), "THE WORLD IN MAPS", font=F_KICK, fill=AMBER_DARK)


def draw_timeline(d):
    top = 482
    d.text((36, top), "THE DAY, IN ORDER", font=F_KICK, fill=TEAL)
    d.line([36, top + 28, W - 36, top + 28], fill=RULE, width=2)
    y = top + 40
    row_h = 62
    for i, (n, _place, _lon, _lat, head, detail, tag, _dx, _dy, _a) in enumerate(STORIES):
        cy = y + 22
        d.ellipse([36, cy - 15, 66, cy + 15], fill=TEAL)
        label = str(n)
        tw = d.textlength(label, font=F_NUM)
        d.text((51 - tw / 2, cy - 10), label, font=F_NUM, fill=WHITE)
        d.text((80, y), head, font=F_HEAD, fill=INK)
        d.text((80, y + 30), detail, font=F_DETAIL, fill=BODY)
        tw = d.textlength(tag, font=F_TAG)
        d.text((W - 36 - tw, y + 6), tag, font=F_TAG, fill=AMBER_DARK)
        if i < len(STORIES) - 1:
            d.line([36, y + row_h - 8, W - 36, y + row_h - 8],
                   fill=RULE, width=1)
        y += row_h
    return y


def draw_strip(d, y):
    d.rectangle([36, y, W - 36, y + 72], fill=TEAL_DARK)
    d.text((56, y + 9), "ALSO TODAY", font=F_STRIP_TITLE, fill=AMBER)
    col_w = (W - 72 - 40) // 2
    for i, item in enumerate(ALSO_TODAY):
        cx = 56 + (i % 2) * (col_w + 40)
        cy = y + 36 + (i // 2) * 20
        lines = wrap(item, F_STRIP, col_w)
        d.text((cx + 12, cy), "\u2022", font=F_STRIP, fill=AMBER)
        d.text((cx + 26, cy), lines[0], font=F_STRIP, fill=WHITE)


def draw_footer(d, y):
    d.text((36, y + 8),
           "Sources: Reuters \u00b7 AP \u00b7 Just Security \u00b7 Court of Arbitration for Sport",
           font=F_FOOT, fill=FAINT)
    d.text((36, y + 26),
           "Drawn in code \u2014 no photographs \u00b7 mellow-heron-42",
           font=F_FOOT, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_map(d)
    end = draw_timeline(d)
    draw_strip(d, end + 6)
    draw_footer(d, end + 6 + 72)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
