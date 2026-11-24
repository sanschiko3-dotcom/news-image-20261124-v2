"""Build-time renderer for the news-image-20261124 v2 front page.

Draws a 1024x1024 broadsheet, "THE WORLD TODAY — Tuesday, 24 November
2026", with Pillow (build time only; the shipped entry program main.py
just copies the PNG, standard library only).

Design: one dominant lead story with a full fact deck and a schematic
map panel, six secondary stories in a 3x2 grid (each with a headline
plus a fact body), one full-width story, and an ALSO TODAY strip.
Every story carries numbers, names or places, so a reader who missed
the day can tell what happened from the image alone.

Deterministic: fixed palette, fixed geometry, no randomness, no
network, no timestamps in the PNG. Run:  python3 render.py
(writes entry.png next to this file)
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (164, 30, 34)
NAVY = (16, 42, 74)
GREY = (90, 88, 80)
LIGHT_GREY = (120, 118, 110)
RULE = (150, 140, 120)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = font("DejaVuSerif-Bold.ttf", 66)
SERIF_HEAD = font("DejaVuSerif-Bold.ttf", 40)
SERIF_SUB = font("DejaVuSerif-Bold.ttf", 27)
SANS_B = font("DejaVuSans-Bold.ttf", 21)
SANS_B_SM = font("DejaVuSans-Bold.ttf", 16)
SANS = font("DejaVuSans.ttf", 19)
SANS_SM = font("DejaVuSans.ttf", 15)
SANS_XS = font("DejaVuSans.ttf", 13)
KICK = font("DejaVuSans-Bold.ttf", 19)
KICK_SM = font("DejaVuSans-Bold.ttf", 15)
DATE_F = font("DejaVuSans-Bold.ttf", 20)


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill, leading):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    yy = y
    for line in wrap_text(draw, text, fnt, width):
        draw.text((x, yy), line, font=fnt, fill=fill)
        yy += leading
    return yy


def headline_block(draw, x, y, text, fnt, width, fill, leading):
    """Draw a wrapped headline; returns the y just below the last line."""
    return para(draw, x, y, text, fnt, width, fill, leading)


# ---------------------------------------------------------------- icons
# Small schematic glyphs, drawn in one colour, ~30x30 px.

def icon_sun(draw, x, y, col):
    draw.ellipse([x + 8, y + 8, x + 22, y + 22], fill=col)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(x + 15 + 13 * math.cos(a), y + 15 + 13 * math.sin(a)),
                   (x + 15 + 18 * math.cos(a), y + 15 + 18 * math.sin(a))],
                  fill=col, width=3)


def icon_radar(draw, x, y, col):
    for r in (14, 9, 4):
        draw.ellipse([x + 15 - r, y + 15 - r, x + 15 + r, y + 15 + r],
                     outline=col, width=2)
    draw.line([(x + 15, y + 15), (x + 28, y + 4)], fill=col, width=3)
    draw.ellipse([x + 26, y + 2, x + 30, y + 6], fill=col)


def icon_doc(draw, x, y, col):
    draw.rectangle([x + 7, y + 3, x + 23, y + 27], outline=col, width=2)
    for i, ly in enumerate((10, 16, 22)):
        draw.line([(x + 11, y + ly), (x + 19, y + ly)], fill=col, width=2)


def icon_court(draw, x, y, col):
    draw.polygon([(x + 3, y + 10), (x + 15, y + 2), (x + 27, y + 10)],
                 fill=col)
    for cx in (7, 13, 19):
        draw.rectangle([x + cx, y + 12, x + cx + 2, y + 22], fill=col)
    draw.rectangle([x + 3, y + 24, x + 27, y + 27], fill=col)


def icon_chart(draw, x, y, col):
    pts = [(x + 3, y + 24), (x + 10, y + 18), (x + 16, y + 20),
           (x + 23, y + 10), (x + 28, y + 6)]
    draw.line(pts, fill=col, width=3, joint="curve")
    draw.polygon([(x + 28, y + 6), (x + 22, y + 5), (x + 27, y + 12)],
                 fill=col)


def icon_quake(draw, x, y, col):
    pts = [(x + 3, y + 8), (x + 9, y + 22), (x + 14, y + 10),
           (x + 19, y + 24), (x + 25, y + 8), (x + 28, y + 16)]
    draw.line(pts, fill=col, width=3, joint="curve")


# ------------------------------------------------------- lead map panel
def draw_map_panel(d, x, y, w, h):
    """Schematic Mediterranean / Libya coast panel for the lead story."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 48, 84))
    # sea shading: lighter band at the top (open sea)
    for i in range(70):
        t = i / 70
        c = tuple(int((18, 48, 84)[k] + ((38, 88, 138)[k] - (18, 48, 84)[k]) * t)
                  for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    d.text((x + 14, y + 12), "MEDITERRANEAN SEA",
           font=font("DejaVuSans-Bold.ttf", 15), fill=(185, 210, 235))
    # Libya coastline: sand-coloured land along the bottom
    d.polygon([(x, y + h), (x, y + 190), (x + 90, y + 168),
               (x + 180, y + 182), (x + 260, y + 162), (x + w, y + 176),
               (x + w, y + h)], fill=(214, 196, 150))
    d.text((x + 238, y + h - 30), "LIBYA",
           font=font("DejaVuSans-Bold.ttf", 17), fill=(90, 74, 44))
    # Benghazi port marker on the coast
    bx, by = x + 300, y + 168
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 255, 255),
              outline=(164, 30, 34), width=2)
    d.text((bx - 38, by + 14), "BENGHAZI",
           font=font("DejaVuSans-Bold.ttf", 15), fill=(90, 74, 44))
    # corvette silhouette at anchor, bow to the right
    hx, hy = x + 78, y + 128
    d.polygon([(hx, hy), (hx + 128, hy), (hx + 142, hy + 14),
               (hx + 8, hy + 14)], fill=(24, 28, 34))
    d.rectangle([hx + 38, hy - 14, hx + 88, hy], fill=(36, 42, 50))
    d.rectangle([hx + 62, hy - 28, hx + 72, hy - 14], fill=(36, 42, 50))
    d.text((hx + 8, hy + 20), "MERKURY",
           font=font("DejaVuSans-Bold.ttf", 14), fill=(200, 215, 230))
    # blast starburst at the bow
    ex, ey = hx + 148, hy - 2
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(ex + 8 * math.cos(a), ey + 8 * math.sin(a)),
                (ex + 24 * math.cos(a), ey + 24 * math.sin(a))],
               fill=(255, 150, 40), width=4)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 196, 70))
    # two sea drones closing in, dashed approach lines
    for (dx, dy) in ((x + 60, y + 52), (x + 150, y + 38)):
        d.ellipse([dx - 7, dy - 4, dx + 7, dy + 4], fill=(16, 16, 16))
        d.line([(dx - 14, dy - 4), (dx + 14, dy - 4)], fill=(16, 16, 16),
               width=2)
    d.line([(x + 60, y + 52), (ex - 26, ey - 8)], fill=(255, 255, 255),
           width=2)
    d.line([(x + 150, y + 38), (ex - 20, ey - 18)], fill=(255, 255, 255),
           width=2)


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=SERIF_B)) / 2, 6), title,
           font=SERIF_B, fill=INK)
    d.text((28, 82), "TUESDAY, 24 NOVEMBER 2026", font=DATE_F, fill=INK)
    right = "THE DAY IN ONE PAGE"
    d.text((W - 28 - d.textlength(right, font=DATE_F), 82), right,
           font=DATE_F, fill=GREY)
    d.rectangle([28, 110, W - 28, 113], fill=RED)
    d.rectangle([28, 116, W - 28, 117], fill=INK)

    # ---- lead story: text left, map right ----
    lx, ly = 28, 132
    d.text((lx, ly), "WAR AT SEA", font=KICK, fill=RED)
    y = headline_block(d, lx, ly + 28,
                       "UKRAINE SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
                       SERIF_HEAD, 580, INK, 44)
    para(d, lx, y + 8,
         "President Zelensky confirms seven naval drones sank the "
         "corvette Merkury at Benghazi on Sunday \u2014 one of Russia's "
         "newest warships, commissioned in 2023. A Ka-27 helicopter "
         "aboard was destroyed, and the cargo ship MV Angara was "
         "also hit.",
         font("DejaVuSans.ttf", 18), 580, INK, 23)
    draw_map_panel(d, 632, 132, 364, 276)

    d.rectangle([28, 420, W - 28, 421], fill=RULE)

    # ---- six secondary stories, 3 x 2 grid ----
    stories = [
        ("CLIMATE", icon_sun, "COP31 COLLAPSES IN ANTALYA",
         "Talks run nearly 50 hours into overtime, then break up: 90+ "
         "nations, the whole EU included, reject a draft that never says "
         "'fossil fuels'."),
        ("SECURITY", icon_radar, "NATO COUNTS 25 AIRSPACE VIOLATIONS",
         "The alliance logs 25 Russian airspace violations in 2026; "
         "debris from a 20 Nov incident is found in Poland, and Putin "
         "signals openness to Article 5-style guarantees."),
        ("MIDDLE EAST", icon_doc, "US SANCTIONS IRAN; QATAR MEDIATES",
         "The US Treasury imposes new sanctions on Iran as Qatar mediates "
         "talks between Washington and Tehran."),
        ("JUSTICE", icon_court, "14 STATES BACK ROHINGYA CASE AT ICJ",
         "Fourteen countries support the genocide case against Myanmar at "
         "the International Court of Justice."),
        ("MARKETS", icon_chart, "HUANG RETURNS AS NVIDIA CEO",
         "Jensen Huang is back as Nvidia chief executive, and the Nasdaq "
         "jumps 6.51% on the day."),
        ("DISASTER", icon_quake, "NEPAL SHAKEN BY 5.6 QUAKE",
         "A magnitude 5.6 earthquake shakes Nepal."),
    ]
    col_w, row_h, gap_x, gap_y = 312, 168, 16, 12
    for i, (kick, icon, head, body) in enumerate(stories):
        cx = 28 + (i % 3) * (col_w + gap_x)
        cy = 436 + (i // 3) * (row_h + gap_y)
        icon(d, cx, cy + 2, RED)
        d.text((cx + 38, cy + 6), kick, font=KICK_SM, fill=RED)
        yy = headline_block(d, cx, cy + 32, head, SANS_B, col_w, INK, 25)
        para(d, cx, yy + 4, body, SANS_SM, col_w, (52, 52, 48), 19)
        if i % 3 < 2:
            d.line([(cx + col_w + 8, cy + 4), (cx + col_w + 8,
                                               cy + row_h - 8)],
                   fill=(205, 198, 180), width=1)

    d.rectangle([28, 788, W - 28, 789], fill=RED)
    d.rectangle([28, 792, W - 28, 793], fill=INK)

    # ---- full-width story ----
    icon_court(d, 28, 806, RED)
    d.text((66, 810), "TECH UNDER FIRE", font=KICK_SM, fill=RED)
    headline_block(d, 66, 834, "STATES SUE SPACEX OVER GROK ABUSE IMAGES",
                   SERIF_SUB, 930, INK, 32)
    para(d, 66, 868,
         "Oregon and Virginia sue SpaceX, alleging its Grok chatbot "
         "generated sexual images of children.",
         font("DejaVuSans.ttf", 16), 930, (52, 52, 48), 20)

    d.rectangle([28, 900, W - 28, 901], fill=RULE)

    # ---- also today strip ----
    d.text((28, 912), "ALSO TODAY", font=KICK_SM, fill=RED)
    para(d, 28, 936,
         "Russian cargo ship Sparta II ablaze in the Baltic after a drone "
         "strike \u2022 Trump\u2013Putin\u2013Xi summit makes no progress on "
         "ending the war \u2022 Measles claims a ninth life in Pennsylvania "
         "\u2022 Car bomb explodes in Villavicencio, Colombia \u2022 Tripoli "
         "voices \u2018grave concern\u2019 as fighting reaches Libya\u2019s "
         "ports \u2022 COP31 called climate diplomacy\u2019s \u2018darkest "
         "moment\u2019",
         SANS_SM, W - 56, (52, 52, 48), 19)

    d.text((28, 992), "Sources: BBC, AP, Reuters, France 24  \u00b7  "
                      "24 November 2026",
           font=SANS_XS, fill=LIGHT_GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
