#!/usr/bin/env python3
"""Draw the 21 November 2026 front page: one image, six stories.

Pure Pillow shapes and text, no photos, no network. Renders entry.png
at 1024x1024 in the same directory as this script.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (250, 244, 231)
CARD = (255, 250, 238)
NAVY = (16, 42, 67)
NAVY_DARK = (10, 30, 50)
CRIMSON = (178, 34, 52)
GOLD = (212, 144, 20)
INK = (24, 24, 22)
BODY = (70, 70, 64)
MUTED = (118, 108, 90)
WHITE = (255, 255, 255)
CREAM_LINE = (212, 144, 20)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap returning lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(draw, x, y, text, fnt, color, max_width, leading):
    """Draw wrapped text; return the y position after the last line."""
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x, y, width, color, height=4):
    draw.rectangle([x, y, x + width, y + height], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    mast = load(SANS_BOLD, 50)
    d.text((34, 28), "THE WORLD IN ONE PAGE", font=mast, fill=WHITE)
    sub = load(SANS_BOLD, 22)
    d.text((34, 84), "SATURDAY 21 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
           font=sub, fill=GOLD)
    issue = load(SANS, 22)
    tag = "No. 325"
    d.text((W - 34 - d.textlength(tag, font=issue), 84), tag,
           font=issue, fill=WHITE)
    d.rectangle([0, 118, W, 124], fill=CRIMSON)

    # ---- Lead story: COP31 ----------------------------------------------
    d.rectangle([24, 138, 1000, 404], fill=NAVY)
    d.rectangle([24, 138, 1000, 144], fill=GOLD)
    kick = load(SANS_BOLD, 24)
    d.text((52, 156), "CLIMATE  /  ANTALYA", font=kick, fill=GOLD)
    num = load(SANS_BOLD, 34)
    d.text((1000 - 52 - d.textlength("01", font=num), 150), "01",
           font=num, fill=GOLD)
    rule(d, 52, 192, 46, GOLD)
    head = load(SANS_BOLD, 44)
    y = draw_block(d, 52, 206,
                   "COP31 spills into overtime as draft deal drops fossil fuels",
                   head, WHITE, 920, 50)
    rule(d, 52, y + 8, 46, GOLD)
    deck = load(SANS, 25)
    draw_block(d, 52, y + 24,
               "Nearly 200 nations haggle into Saturday in Turkey after the "
               "draft text strips out every mention of ending fossil-fuel use.",
               deck, WHITE, 920, 31)

    # ---- Story grid -----------------------------------------------------
    stories = [
        ("WAR  /  UKRAINE", CRIMSON,
         "Russian strike on Kryvyi Rih kills 2, wounds 42",
         "Missiles hit the city centre on Friday night; four of the injured are children.",
         "02"),
        ("JUSTICE  /  THE HAGUE", NAVY,
         "Myanmar calls ICJ genocide ruling 'unfair'",
         "A day after the court found Myanmar guilty of genocide, its government rejects it.",
         "03"),
        ("BUSINESS  /  CYBER", CRIMSON,
         "Hackers leak JPMorgan, Visa and Mastercard data",
         "Group n0n exposes customer names and emails via vendors; no card numbers.",
         "04"),
        ("AMERICAS  /  BRAZIL", NAVY,
         "Bolsonaro in hospital with intestinal blockage",
         "The jailed ex-president, 71, is stable in hospital after severe abdominal pain.",
         "05"),
    ]
    card_w, card_h = 476, 216
    xs = [24, 524]
    ys = [418, 648]
    kick_f = load(SANS_BOLD, 21)
    head_f = load(SANS_BOLD, 27)
    body_f = load(SANS, 19)
    num_f = load(SANS_BOLD, 28)
    for i, (kicker, accent, headline, body, number) in enumerate(stories):
        x, y = xs[i % 2], ys[i // 2]
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD,
                    outline=NAVY, width=2)
        d.rectangle([x, y, x + 8, y + card_h], fill=accent)
        tx = x + 26
        d.text((tx, y + 14), kicker, font=kick_f, fill=accent)
        rule(d, tx, y + 42, 46, accent)
        hy = draw_block(d, tx, y + 54, headline, head_f, INK, 424, 35)
        # Narrow body column so the corner number never collides with text.
        draw_block(d, tx, hy + 8, body, body_f, BODY, 400, 24)
        d.text((x + card_w - 26 - d.textlength(number, font=num_f),
                y + card_h - 38), number, font=num_f, fill=NAVY)

    # ---- Bottom strip: cricket ------------------------------------------
    d.rectangle([24, 878, 1000, 984], fill=GOLD)
    d.text((52, 890), "SPORT  /  WELLINGTON", font=kick_f, fill=NAVY_DARK)
    storm = load(SANS_BOLD, 28)
    d.text((52, 914), "Jaiswal and Rahul hit back for India in Wellington",
           font=storm, fill=INK)
    storm_body = load(SANS, 21)
    d.text((52, 950),
           "India reach 159/1 at stumps on Day 2, replying to New Zealand's 368.",
           font=storm_body, fill=(74, 54, 8))
    d.ellipse([892, 896, 968, 972], outline=NAVY_DARK, width=4)
    circ = load(SANS_BOLD, 34)
    label = "06"
    d.text((930 - d.textlength(label, font=circ) / 2, 914), label,
           font=circ, fill=NAVY_DARK)

    # ---- Footer ---------------------------------------------------------
    foot = load(SANS, 19)
    d.text((24, 994), "Compiled from verified reports  |  One image, six stories",
           font=foot, fill=MUTED)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
