#!/usr/bin/env python3
"""Render the news-image-01 entry: a one-page newspaper front page summing up
the world news of Friday 13 November 2026, drawn with Pillow.

The image is 1024x1024 PNG. Every headline and summary below is drawn from
what was reported on 13 November 2026 (Reuters, AP, IEA, DOJ and others, as
carried by the day's news wires): nothing is invented, and claims are
attributed where the reporting itself attributed them ("Iran says").

Run:  python3 render.py            (writes entry.png beside this file)
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 247)
INK = (17, 17, 17)
GREY = (68, 68, 68)
RED = (185, 28, 28)
SEA = (30, 58, 95)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_ship(draw, x, y, scale=1.0):
    """A small white ship silhouette on the sea strip."""
    hull = [(x, y), (x + 46 * scale, y), (x + 40 * scale, y - 13 * scale),
            (x + 7 * scale, y - 13 * scale)]
    draw.polygon(hull, fill=(240, 244, 248))
    draw.rectangle([x + 16 * scale, y - 22 * scale, x + 30 * scale, y - 13 * scale],
                   fill=(240, 244, 248))
    draw.rectangle([x + 22 * scale, y - 30 * scale, x + 24 * scale, y - 22 * scale],
                   fill=(240, 244, 248))


def draw_burst(draw, cx, cy, r, color):
    """A small explosion starburst."""
    for i in range(8):
        ang = math.pi * i / 4
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        draw.line([(cx, cy), (x2, y2)], fill=color, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    mast = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 18), title, font=mast, fill=INK)
    date_f = font(SANS_B, 23)
    date = "FRIDAY  \u00b7  13 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 96), date, font=date_f, fill=RED)
    d.line([(24, 132), (W - 24, 132)], fill=INK, width=3)
    d.line([(24, 138), (W - 24, 138)], fill=RED, width=2)

    # ---- Lead story: the Gulf -------------------------------------------
    kick = font(SANS_B, 18)
    d.text((24, 152), "THE GULF  \u2014  LEAD STORY", font=kick, fill=RED)
    head = font(SANS_B, 46)
    lead_head = "FOUR TANKERS HIT IN THE\nSTRAIT OF HORMUZ"
    y = 182
    for line in lead_head.split("\n"):
        d.text((24, y), line, font=head, fill=INK)
        y += 54
    body = font(SANS, 20)
    lead_body = ("Iran says it destroyed a US radar in Bahrain; "
                 "four tankers reported hit.")
    y = draw_lines(d, wrap(d, lead_body, body, W - 48), 24, y + 4, body, GREY, 27)

    # Sea strip with ships and bursts
    sea_y, sea_h = 330, 46
    d.rectangle([24, sea_y, W - 24, sea_y + sea_h], fill=SEA)
    for wx in range(24, W - 24, 46):
        d.arc([wx, sea_y + 34, wx + 34, sea_y + 52], 180, 360, fill=(255, 255, 255))
    draw_ship(d, 120, sea_y + 34, 1.0)
    draw_ship(d, 430, sea_y + 36, 0.85)
    draw_ship(d, 740, sea_y + 34, 1.0)
    draw_burst(d, 300, sea_y + 22, 13, (249, 115, 22))
    draw_burst(d, 620, sea_y + 18, 11, (239, 68, 68))
    draw_burst(d, 900, sea_y + 24, 12, (249, 115, 22))

    # ---- Story grid: 2 columns x 3 rows ---------------------------------
    stories = [
        ("UKRAINE", (29, 78, 216),
         "EUROPE WINS A SEAT AT UKRAINE PEACE TALKS",
         "Russia agrees to a European role in the next round; envoys say "
         "the largest prisoner swap of the war is in the works."),
        ("TECH", (12, 118, 110),
         "NVIDIA CHIEF JENSEN HUANG RESIGNS",
         "The founder quits as chief executive; finance chief Colette Kress "
         "takes over amid a chip-export row."),
        ("ASIA", (180, 83, 9),
         "TAIWAN DETAILS CHINA'S UNANNOUNCED PACIFIC DRILLS",
         "Taipei calls a large naval exercise across the western Pacific "
         "an act of intimidation."),
        ("ENERGY", (21, 128, 61),
         "IEA SEES OIL SURPLUS DESPITE GULF DANGER",
         "Supply is forecast to top demand by 1.7m barrels a day in the "
         "final quarter of the year."),
        ("TECHNOLOGY", (29, 78, 216),
         "MICROSOFT OUTAGE HITS OUTLOOK IN 74 COUNTRIES",
         "A worldwide disruption takes the email service down for users "
         "across the globe."),
        ("CRIME", (190, 18, 60),
         "US TO SEIZE $1.2BN FROM BINANCE HACK",
         "A court backs the seizure of crypto stolen on 29 October; the "
         "FBI blames North Korea."),
    ]
    col_x = [24, 524]
    col_w = 476
    row_y = [392, 580, 768]
    row_h = 174
    kicker_f = font(SANS_B, 15)
    h_f = font(SANS_B, 27)
    b_f = font(SANS, 17)
    for i, (kicker, color, headline, summary) in enumerate(stories):
        x = col_x[i % 2]
        y0 = row_y[i // 2]
        d.line([(x, y0), (x + col_w, y0)], fill=color, width=3)
        d.text((x, y0 + 10), kicker, font=kicker_f, fill=color)
        hl = wrap(d, headline, h_f, col_w)
        y = draw_lines(d, hl[:2], x, y0 + 32, h_f, INK, 32)
        draw_lines(d, wrap(d, summary, b_f, col_w)[:2], x, y + 4, b_f, GREY, 22)

    # ---- Footer: also in the news ----------------------------------------
    d.line([(24, 956), (W - 24, 956)], fill=INK, width=2)
    foot_f = font(SANS, 16)
    foot = ("ALSO: Pope Leo meets abuse survivors in Peru  \u00b7  Brooklyn collapse toll "
            "settles at eight  \u00b7  Measles ruling awaited in North America  \u00b7  "
            "Storm Charles hits Portugal")
    y = draw_lines(d, wrap(d, foot, foot_f, W - 48), 24, 968, foot_f, GREY, 21)
    credit = font(SANS, 13)
    c = "The world on Friday 13 November 2026 \u2014 as reported that day."
    cw = d.textlength(c, font=credit)
    d.text(((W - cw) / 2, 1006), c, font=credit, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
