#!/usr/bin/env python3
"""Draw the front page for 20 November 2026 and save it as entry.png.

Everything here is drawn from scratch with Pillow: no photo, no download,
no font outside the machine. The picture is a newspaper front page whose
lead is the first-ever Trump-Xi-Putin trilateral summit in Shenzhen, with
three more panels for the day's other big stories and a ticker of the rest.

Run:  python3 gen_image.py   (writes assets/entry.png, 1024x1024)
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "assets/entry.png"

PAPER = (246, 241, 229)
INK = (24, 24, 22)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (176, 141, 58)
GREY = (90, 88, 80)
RULE = (60, 58, 50)
SKY = (196, 214, 228)
SKYLINE = (120, 138, 158)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    """Split text into lines that fit `width` pixels."""
    lines: list[str] = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, fnt,
         width: int, fill=INK, leading: int | None = None) -> int:
    """Draw wrapped text; return the y just below the last line."""
    step = leading or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def flag_us(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    stripe = h / 13
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(30, 48, 96))
    for r in range(5):
        for c in range(6):
            cx = x + cw * (0.12 + 0.176 * c)
            cy = y + ch * (0.14 + 0.19 * r)
            d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill="white")


def flag_cn(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon([(x + w * 0.20, y + h * 0.10), (x + w * 0.26, y + h * 0.28),
               (x + w * 0.11, y + h * 0.20), (x + w * 0.29, y + h * 0.20),
               (x + w * 0.14, y + h * 0.28)], fill=(255, 222, 0))
    for sx, sy in [(0.42, 0.10), (0.50, 0.22), (0.50, 0.36), (0.42, 0.46)]:
        d.polygon([(x + w * sx, y + h * sy),
                   (x + w * (sx + 0.03), y + h * (sy + 0.06)),
                   (x + w * (sx - 0.02), y + h * (sy + 0.03)),
                   (x + w * (sx + 0.08), y + h * (sy + 0.03)),
                   (x + w * (sx + 0.03), y + h * (sy + 0.06))],
                  fill=(255, 222, 0))


def flag_ru(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def pole_flag(d: ImageDraw.ImageDraw, x: int, y: int, h: int,
              painter) -> None:
    """A flag on a pole: pole top at (x, y), flag hangs to the right."""
    d.line([x, y, x, y + h], fill=(70, 60, 40), width=3)
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=GOLD)
    painter(d, x + 2, y + 4, 46, 30)


def figure(d: ImageDraw.ImageDraw, cx: int, base: int, suit, tie,
           skin=(214, 178, 140), hair=(240, 240, 235)) -> None:
    """A seated leader: head, hair, shoulders, tie. `base` is the table line."""
    d.ellipse([cx - 17, base - 108, cx + 17, base - 74], fill=skin)
    d.pieslice([cx - 18, base - 110, cx + 18, base - 84], 180, 360, fill=hair)
    d.polygon([(cx - 34, base - 74), (cx + 34, base - 74),
               (cx + 26, base - 8), (cx - 26, base - 8)], fill=suit)
    d.polygon([(cx - 6, base - 74), (cx + 6, base - 74),
               (cx + 4, base - 40), (cx - 4, base - 40)], fill=tie)
    d.polygon([(cx - 10, base - 74), (cx, base - 62), (cx + 10, base - 74)],
              fill=(250, 250, 245))


def skyline(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int) -> None:
    """Shenzhen towers against the sky."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    import random
    rnd = random.Random(20261120)
    x = x0 + 8
    while x < x1 - 30:
        bw = rnd.randint(26, 52)
        bh = rnd.randint(40, 110)
        d.rectangle([x, y1 - bh, x + bw, y1], fill=SKYLINE)
        for wy in range(y1 - bh + 8, y1 - 6, 12):
            for wx in range(x + 5, x + bw - 5, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(232, 226, 200))
        x += bw + rnd.randint(4, 14)
    d.rectangle([x0, y1 - 4, x1, y1], fill=(96, 110, 126))


def scales(d: ImageDraw.ImageDraw, cx: int, top: int, h: int) -> None:
    """Balanced scales of justice, `h` pixels tall."""
    bottom = top + h
    d.line([cx, top, cx, bottom - 6], fill=INK, width=4)
    d.line([cx - 46, top + 10, cx + 46, top + 10], fill=INK, width=4)
    d.ellipse([cx - 6, top - 5, cx + 6, top + 5], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * 46
        d.line([px, top + 10, px - 15, top + 34], fill=INK, width=2)
        d.line([px, top + 10, px + 15, top + 34], fill=INK, width=2)
        d.pieslice([px - 18, top + 30, px + 18, top + 54], 0, 180, fill=GOLD)
    d.rectangle([cx - 26, bottom - 6, cx + 26, bottom], fill=INK)


def cyclone(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """A storm spiral with rain and a coastline."""
    for k in range(7):
        rr = r * (0.22 + 0.11 * k)
        a0 = 200 + k * 55
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a0 + 250,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    d.rectangle([cx - 100, cy + r - 6, cx + 100, cy + r + 12], fill=(46, 90, 60))
    d.rectangle([cx - 100, cy + r - 6, cx + 100, cy + r], fill=(222, 200, 140))
    for i in range(7):
        x = cx - 90 + i * 30
        d.line([x, cy + r - 16, x - 5, cy + r - 6], fill=(180, 200, 220), width=2)


def clock(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """A clock face showing a decision pushed into next year."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=4)
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang - 90)
        d.line([cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a),
                cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a)],
               fill=INK, width=3)
    d.line([cx, cy, cx, cy - r + 18], fill=INK, width=4)
    d.line([cx, cy, cx + r - 24, cy + 10], fill=INK, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def build() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin
    d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=RULE, width=1)

    # ---- Masthead ----
    y = 30
    d.text((W // 2, y), "THE WORLD IN ONE DAY", font=font(SERIF, 62),
           fill=INK, anchor="ma")
    y = 110
    d.line([m, y, W - m, y], fill=RULE, width=3)
    y += 10
    d.text((W // 2, y), "FRIDAY, 20 NOVEMBER 2026  •  SHENZHEN — THE HAGUE — ODISHA — WASHINGTON",
           font=font(SANS, 21), fill=NAVY, anchor="ma")
    y += 30
    d.line([m, y, W - m, y], fill=RULE, width=3)

    # ---- Lead: the trilateral summit ----
    y += 10
    lead_top = y
    skyline(d, m, y, W - m, y + 108)
    pole_flag(d, m + 52, y + 12, 96, flag_us)
    pole_flag(d, W // 2 - 24, y + 8, 96, flag_cn)
    pole_flag(d, W - m - 98, y + 12, 96, flag_ru)
    table_y = y + 186
    figure(d, W // 2 - 190, table_y, (32, 44, 78), (178, 34, 52))
    figure(d, W // 2, table_y, (40, 40, 40), (222, 41, 16),
           hair=(30, 30, 30))
    figure(d, W // 2 + 190, table_y, (52, 52, 58), (0, 57, 166),
           hair=(200, 200, 200))
    d.rectangle([m, table_y, W - m, table_y + 26], fill=(122, 84, 52))
    d.rectangle([m, table_y, W - m, table_y + 6], fill=(150, 110, 70))
    for cx, name in [(W // 2 - 190, "TRUMP"), (W // 2, "XI"),
                     (W // 2 + 190, "PUTIN")]:
        d.text((cx, table_y + 32), name, font=font(SANS, 17), fill=INK,
               anchor="ma")
    y = table_y + 58
    d.text((W // 2, y), "THREE NUCLEAR POWERS, ONE TABLE",
           font=font(SERIF, 40), fill=INK, anchor="ma")
    y += 50
    y = para(d, m + 28, y,
             "Trump, Xi and Putin hold the first-ever trilateral summit in "
             "Shenzhen — and declare: \u201cA nuclear war cannot be won and "
             "must never be fought.\u201d",
             font(SERIF_R, 24), W - 2 * m - 56, leading=30)
    y += 8
    d.line([m, y, W - m, y], fill=RULE, width=2)
    lead_bottom = y

    # ---- Three panels ----
    y = lead_bottom + 10
    panel_h = 222
    col_w = (W - 2 * m - 32) // 3
    panels = [
        ("THE HAGUE", "COURT: MYANMAR COMMITTED GENOCIDE",
         "The world court rules Myanmar committed genocide against the "
         "Rohingya minority.", "scales"),
        ("ODISHA, INDIA", "CYCLONE AKVAN SLAMS THE COAST",
         "300,000 people evacuated as the storm makes landfall, with heavy "
         "rain and rescue teams deployed.", "storm"),
        ("WASHINGTON", "IRAN DECISION PUSHED TO 2027",
         "Trump says there is no rush on Iran: \u201cWe\u2019ll see what "
         "happens after January 1.\u201d", "clock"),
    ]
    for i, (kicker, head, body, art) in enumerate(panels):
        x0 = m + i * (col_w + 16)
        x1 = x0 + col_w
        d.rectangle([x0, y, x1, y + panel_h], outline=RULE, width=2)
        d.text((x0 + 12, y + 8), kicker, font=font(SANS, 15), fill=RED)
        hy = y + 30
        hy = para(d, x0 + 12, hy, head, font(SERIF, 24), col_w - 24,
                  leading=28)
        art_y = y + 112
        if art == "scales":
            scales(d, x0 + col_w // 2, art_y, 52)
        elif art == "storm":
            d.rectangle([x0 + 8, art_y - 4, x1 - 8, art_y + 38],
                        fill=(64, 84, 110))
            cyclone(d, x0 + col_w // 2, art_y + 14, 20)
        else:
            clock(d, x0 + col_w // 2, art_y + 26, 26)
        by = y + panel_h - 60
        para(d, x0 + 12, by, body, font(SERIF_R, 16), col_w - 24, leading=18)
        if i < 2:
            d.line([x1 + 8, y, x1 + 8, y + panel_h], fill=RULE, width=1)
    y += panel_h + 10
    d.line([m, y, W - m, y], fill=RULE, width=3)

    # ---- Ticker: also today ----
    y += 8
    d.text((m, y), "ALSO TODAY", font=font(SANS, 19), fill=RED)
    y += 28
    items = [
        "Voyager 1 passes one light-day from Earth — the farthest any human-made object has flown",
        "GTA 6 sales pass $1.8 billion, overtaking a blockbuster film's global run",
        "Europe ready for talks with Russia on ending the war in Ukraine, leaders say",
        "Houthi attack damages a tower in Riyadh, Saudi Arabia says",
        "Engine trouble forces Japan's Hayabusa2 probe to abandon its asteroid landing",
    ]
    for item in items:
        d.text((m + 14, y), "•", font=font(SANS, 18), fill=NAVY)
        y = para(d, m + 34, y, item, font(SERIF_R, 18), W - 2 * m - 34,
                 leading=22)
        y += 1
    y += 4
    d.line([m, y, W - m, y], fill=RULE, width=3)

    # ---- Footer ----
    y += 8
    d.text((W // 2, y), "THE WORLD IN ONE DAY  —  FRIDAY, 20 NOVEMBER 2026",
           font=font(SANS, 19), fill=NAVY, anchor="ma")
    y += 26
    d.text((W // 2, y), "One image summing up the day's world news.",
           font=font(SERIF_R, 16), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    pic = build()
    pic.save(OUT, optimize=True)
    import os
    print(f"wrote {OUT}: {pic.size}, {os.path.getsize(OUT)} bytes")
