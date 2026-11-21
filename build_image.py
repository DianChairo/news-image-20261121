#!/usr/bin/env python3
"""Draw the 21 November 2026 front page: six stories, pure Pillow shapes."""

import math
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
NAVY_SOFT = (38, 54, 92)
CRIMSON = (164, 22, 35)
GOLD = (201, 162, 39)
TEAL = (20, 82, 74)
GREEN = (30, 86, 49)
INK = (26, 26, 26)
GREY = (92, 92, 88)
CARD = (255, 255, 255)
LINE = (210, 203, 188)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def para(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=GOLD, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             200, 340, fill=GOLD, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             20, 160, fill=GOLD, width=3)


def scales(draw, cx, cy, s, colour):
    draw.line([cx, cy - s, cx, cy + s], fill=colour, width=4)
    draw.line([cx - s, cy - s + 8, cx + s, cy - s + 8], fill=colour, width=4)
    for sx in (cx - s, cx + s):
        draw.line([sx, cy - s + 8, sx, cy + 2], fill=colour, width=3)
        draw.polygon([(sx - 16, cy + 2), (sx + 16, cy + 2),
                      (sx, cy + 20)], outline=colour, width=3)
    draw.ellipse([cx - 6, cy + s - 4, cx + 6, cy + s + 4], fill=colour)


def padlock(draw, cx, cy, w, h, colour):
    draw.arc([cx - w // 2, cy - h // 2 - 14, cx + w // 2, cy + 6],
             180, 360, fill=colour, width=6)
    draw.rounded_rectangle([cx - w // 2, cy - 8, cx + w // 2, cy + h // 2],
                           radius=6, fill=colour)
    draw.ellipse([cx - 5, cy + 2, cx + 5, cy + 12], fill=PAPER)
    draw.rectangle([cx - 2, cy + 10, cx + 2, cy + 22], fill=PAPER)


def cross(draw, cx, cy, s, colour):
    draw.rectangle([cx - s // 4, cy - s, cx + s // 4, cy + s], fill=colour)
    draw.rectangle([cx - s, cy - s // 4, cx + s, cy + s // 4], fill=colour)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    centred(d, W // 2, 14, "THE WORLD TODAY", font(SERIF, 58), (250, 246, 236))
    centred(d, W // 2, 82, "SATURDAY 21 NOVEMBER 2026  ·  WORLD NEWS IN ONE PAGE",
            font(SANS_BOLD, 19), GOLD)
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # ---- lead story: COP31 -------------------------------------------
    d.rounded_rectangle([24, 140, 1000, 396], radius=14, fill=NAVY)
    d.rectangle([24, 140, 40, 396], fill=GOLD)
    d.text((62, 158), "CLIMATE  ·  COP31  ·  ANTALYA", font=font(SANS_BOLD, 20),
           fill=GOLD)
    y = para(d, (62, 192),
             "COP31 spills into overtime as draft deal drops fossil-fuel exit",
             font(SERIF, 36), (250, 246, 236), 560, 43)
    para(d, (62, y + 8),
         "Negotiators worked past the deadline after the draft "
         "stripped out every mention of ending fossil-fuel use.",
         font(SANS, 20), (214, 220, 232), 600, 28)
    globe(d, 852, 268, 84)
    d.text((772, 356), "TALKS RUN LATE", font=font(SANS_BOLD, 17), fill=GOLD)

    # ---- middle grid: four stories ------------------------------------
    cards = [
        dict(x0=24, y0=412, x1=500, y1=596, bar=CRIMSON,
             kicker="UKRAINE", icon="burst",
             head="Ballistic missiles hit Kryvyi Rih",
             body="Russia struck the Ukrainian city of Kryvyi Rih with "
                  "ballistic missiles."),
        dict(x0=524, y0=412, x1=1000, y1=596, bar=TEAL,
             kicker="MYANMAR", icon="scales",
             head="Myanmar rejects ICJ genocide ruling",
             body="Myanmar called the International Court of Justice "
                  "ruling \u201cunfair\u201d and rejected it."),
        dict(x0=24, y0=612, x1=500, y1=796, bar=NAVY_SOFT,
             kicker="CYBERCRIME", icon="lock",
             head="Bank data leaked in n0n ransomware attack",
             body="JPMorgan, Visa and Mastercard data leaked in a "
                  "breach claimed by the n0n group."),
        dict(x0=524, y0=612, x1=1000, y1=796, bar=GOLD,
             kicker="BRAZIL", icon="cross",
             head="Bolsonaro in hospital in Brasilia",
             body="Former president Jair Bolsonaro was hospitalised "
                  "in Brasilia."),
    ]
    for c in cards:
        d.rounded_rectangle([c["x0"], c["y0"], c["x1"], c["y1"]],
                            radius=12, fill=CARD, outline=LINE, width=2)
        d.rounded_rectangle([c["x0"], c["y0"], c["x1"], c["y0"] + 10],
                            radius=5, fill=c["bar"])
        d.text((c["x0"] + 20, c["y0"] + 24), c["kicker"],
               font=font(SANS_BOLD, 17), fill=c["bar"])
        icon_cx = c["x1"] - 52
        icon_cy = c["y0"] + 48
        if c["icon"] == "burst":
            starburst(d, icon_cx, icon_cy, 30, 13, 8, CRIMSON)
            d.ellipse([icon_cx - 8, icon_cy - 8, icon_cx + 8, icon_cy + 8],
                      fill=GOLD)
        elif c["icon"] == "scales":
            scales(d, icon_cx, icon_cy, 26, TEAL)
        elif c["icon"] == "lock":
            padlock(d, icon_cx, icon_cy, 44, 40, NAVY_SOFT)
        else:
            d.ellipse([icon_cx - 32, icon_cy - 32, icon_cx + 32, icon_cy + 32],
                      outline=GOLD, width=4)
            cross(d, icon_cx, icon_cy, 20, CRIMSON)
        y = para(d, (c["x0"] + 20, c["y0"] + 52), c["head"],
                 font(SERIF, 27), INK, c["x1"] - c["x0"] - 110, 33)
        para(d, (c["x0"] + 20, y + 6), c["body"], font(SANS, 19), GREY,
             c["x1"] - c["x0"] - 40, 26)

    # ---- bottom strip: cricket ---------------------------------------
    d.rounded_rectangle([24, 812, 1000, 948], radius=14, fill=GREEN)
    d.text((52, 828), "SPORT  ·  CRICKET  ·  WELLINGTON TEST",
           font=font(SANS_BOLD, 19), fill=(196, 224, 196))
    para(d, (52, 858), "India fight back in Wellington",
         font(SERIF, 30), (255, 255, 255), 660, 38)
    para(d, (52, 902), "Jaiswal and Rahul led India\u2019s "
         "fightback in the Wellington Test.",
         font(SANS, 20), (220, 235, 220), 660, 27)
    bat = Image.new("RGBA", (220, 120), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bat)
    bd.rounded_rectangle([20, 44, 150, 76], radius=8, fill=(232, 214, 170))
    bd.rectangle([150, 54, 196, 66], fill=(120, 72, 20))
    bat = bat.rotate(-24, resample=Image.BICUBIC, center=(110, 60))
    img.paste(bat, (760, 830), bat)
    d.ellipse([880, 900, 916, 936], fill=CRIMSON, outline=(255, 255, 255),
              width=2)

    # ---- footer --------------------------------------------------------
    centred(d, W // 2, 968,
            "Six stories from Saturday 21 November 2026, verified from "
            "wire reports.",
            font(SANS, 17), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
