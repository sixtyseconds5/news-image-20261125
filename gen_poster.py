#!/usr/bin/env python3
"""Draw the front page for Wednesday, 25 November 2026.

Every illustration is drawn from scratch with Pillow shapes; no network,
no photos, no randomness. Running this script twice writes identical bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
MARGIN = 28

PAPER = (247, 243, 234)
INK = (24, 24, 24)
SOFT_INK = (74, 70, 62)
RULE = (24, 24, 24)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (184, 134, 11)
DARK_BAND = (28, 32, 40)
CELL_BG = (255, 255, 255)
CELL_EDGE = (198, 190, 174)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, text, cx, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    import math

    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- illustrations

def draw_lead_art(draw, x, y, w, h):
    """Courtroom chip scene: microchip, gavel, GUILTY stamp."""
    # backdrop
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210),
                   outline=CELL_EDGE, width=2)
    # microchip
    cx, cy = x + 105, y + 105
    draw.rectangle([cx - 62, cy - 62, cx + 62, cy + 62], fill=(38, 44, 54))
    draw.rectangle([cx - 40, cy - 40, cx + 40, cy + 40], fill=(212, 175, 55))
    draw.rectangle([cx - 24, cy - 24, cx + 24, cy + 24], fill=(38, 44, 54))
    for i in range(-2, 3):
        off = i * 26
        draw.rectangle([cx + off - 4, cy - 78, cx + off + 4, cy - 62],
                       fill=(212, 175, 55))
        draw.rectangle([cx + off - 4, cy + 62, cx + off + 4, cy + 78],
                       fill=(212, 175, 55))
        draw.rectangle([cx - 78, cy + off - 4, cx - 62, cy + off + 4],
                       fill=(212, 175, 55))
        draw.rectangle([cx + 62, cy + off - 4, cx + 78, cy + off + 4],
                       fill=(212, 175, 55))
    # gavel: handle + head, leaning on the chip
    gx, gy = x + w - 150, y + 58
    draw.line([gx, gy + 96, gx + 96, gy], fill=(122, 74, 30), width=13)
    draw.rectangle([gx + 62, gy - 22, gx + 128, gy + 22], fill=(96, 56, 22))
    draw.rectangle([gx + 52, gy - 26, gx + 62, gy + 26], fill=(140, 88, 40))
    draw.rectangle([gx + 128, gy - 26, gx + 138, gy + 26], fill=(140, 88, 40))
    # sound block, just below the gavel head, clear of the stamp
    draw.ellipse([gx + 72, gy + 28, gx + 138, gy + 48], fill=(96, 56, 22))
    # verdict stamp
    stamp = Image.new("RGBA", (260, 92), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 256, 88], radius=10,
                         outline=RED, width=6)
    sd.text((130, 46), "GUILTY", font=SERIF_BOLD(44), fill=RED,
            anchor="mm")
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    draw._image.paste(stamp, (x + 52, y + h - 118), stamp)


def draw_war(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 222))
    # sea
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(38, 88, 150))
    for i in range(5):
        wx = x + 14 + i * 58
        draw.arc([wx, y + h - 26, wx + 44, y + h - 8], 0, 180,
                 fill=(255, 255, 255), width=3)
    # cargo ship
    draw.polygon([(x + 52, y + h - 60), (x + 52, y + h - 34),
                  (x + 96, y + h - 34), (x + 248, y + h - 34),
                  (x + 248, y + h - 60), (x + 226, y + h - 60)],
                 fill=(52, 52, 58))
    for i, c in enumerate([(178, 34, 34), (28, 68, 128), (184, 134, 11)]):
        bx = x + 78 + i * 52
        draw.rectangle([bx, y + h - 96, bx + 46, y + h - 60], fill=c)
    draw.rectangle([x + 226, y + h - 104, x + 244, y + h - 60],
                   fill=(240, 240, 240))
    # explosion
    starburst(draw, x + w - 62, y + 34, 30, 14, 8, (232, 120, 20))
    starburst(draw, x + w - 62, y + 34, 16, 7, 8, (255, 214, 64))


def draw_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 226, 196))
    # skyline
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(120, 96, 78))
    draw.rectangle([x + 14, y + h - 62, x + 66, y + h - 30],
                   fill=(90, 96, 110))
    draw.rectangle([x + 236, y + h - 52, x + 288, y + h - 30],
                   fill=(90, 96, 110))
    # PIF tower
    tx = x + w // 2 - 34
    draw.polygon([(tx, y + 16), (tx + 68, y + 16),
                  (tx + 56, y + h - 30), (tx + 12, y + h - 30)],
                 fill=(52, 66, 92))
    for r in range(5):
        wy = y + 34 + r * 26
        draw.line([tx + 8 + r, wy, tx + 60 - r, wy],
                  fill=(255, 214, 120), width=4)
    # flame at the crown
    starburst(draw, x + w // 2, y + 22, 22, 10, 7, (232, 120, 20))
    starburst(draw, x + w // 2, y + 24, 11, 5, 7, (255, 214, 64))
    # smoke
    for i, (sx, sy, sr) in enumerate([(x + 42, y + 30, 12),
                                      (x + 62, y + 16, 15),
                                      (x + 88, y + 8, 11)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(150, 150, 150))


def draw_space(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    for sx, sy, sr in [(x + 26, y + 18, 2), (x + 90, y + 44, 2),
                       (x + 250, y + 14, 2), (x + 280, y + 56, 2),
                       (x + 150, y + 12, 2), (x + 210, y + 66, 2)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    # orbit ring
    draw.ellipse([x + 22, y - 6, x + w - 22, y + h + 22],
                 outline=(120, 150, 210), width=2)
    # satellite
    sx, sy = x + w // 2, y + h // 2 + 4
    draw.rectangle([sx - 78, sy - 12, sx - 26, sy + 12], fill=(70, 110, 190))
    draw.rectangle([sx + 26, sy - 12, sx + 78, sy + 12], fill=(70, 110, 190))
    for i in range(3):
        draw.line([sx - 74 + i * 24, sy - 12, sx - 74 + i * 24, sy + 12],
                  fill=(140, 180, 240), width=2)
        draw.line([sx + 30 + i * 24, sy - 12, sx + 30 + i * 24, sy + 12],
                  fill=(140, 180, 240), width=2)
    draw.rectangle([sx - 26, sy - 20, sx + 26, sy + 20], fill=(212, 175, 55))
    draw.rectangle([sx - 14, sy - 12, sx + 14, sy + 12], fill=(38, 44, 54))
    draw.polygon([(sx, sy - 34), (sx - 8, sy - 18), (sx + 8, sy - 18)],
                 fill=(212, 175, 55))


def draw_courts(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(228, 222, 206))
    # courthouse columns
    for i in range(4):
        cx = x + 40 + i * 66
        draw.rectangle([cx, y + 34, cx + 20, y + h - 26], fill=(245, 240, 228))
        draw.rectangle([cx - 6, y + 28, cx + 26, y + 36], fill=(210, 198, 170))
        draw.rectangle([cx - 6, y + h - 32, cx + 26, y + h - 24],
                       fill=(210, 198, 170))
    draw.polygon([(x + 12, y + 28), (x + w // 2, y + 4),
                  (x + w - 12, y + 28)], fill=(210, 198, 170))
    draw.rectangle([x + 12, y + h - 24, x + w - 12, y + h - 12],
                   fill=(210, 198, 170))
    # medal
    mx, my = x + w - 52, y + h - 42
    draw.polygon([(mx - 26, y + 6), (mx - 8, y + 6),
                  (mx, my - 26), (mx + 8, y + 6), (mx + 26, y + 6),
                  (mx + 12, my - 20), (mx - 12, my - 20)],
                 fill=RED)
    draw.ellipse([mx - 30, my - 30, mx + 30, my + 30], fill=GOLD,
                 outline=(140, 100, 10), width=3)
    draw.text((mx, my), "*", font=SERIF_BOLD(34), fill=(140, 100, 10),
              anchor="mm")


def draw_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 228))
    # grid lines
    for i in range(1, 4):
        gy = y + i * (h // 4)
        draw.line([x + 10, gy, x + w - 10, gy], fill=(190, 200, 190), width=1)
    # falling then recovering line
    pts = [(x + 16, y + 22), (x + 66, y + 34), (x + 116, y + 62),
           (x + 166, y + 78), (x + 216, y + 66), (x + 266, y + 40)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x + 266, y + 40), (x + 250, y + 32), (x + 252, y + 52)],
                 fill=RED)
    # server rack
    rx = x + w - 78
    draw.rectangle([rx, y + 14, rx + 58, y + h - 14], fill=(52, 58, 68))
    for i in range(4):
        ry = y + 18 + i * 18
        draw.rectangle([rx + 6, ry, rx + 52, ry + 12], fill=(70, 110, 190))
        draw.ellipse([rx + 10, ry + 3, rx + 17, ry + 10], fill=(120, 220, 120))


def draw_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    # sea
    draw.rectangle([x, y + h - 36, x + w, y + h], fill=(28, 68, 128))
    for i in range(5):
        wx = x + 12 + i * 58
        draw.arc([wx, y + h - 28, wx + 44, y + h - 10], 0, 180,
                 fill=(255, 255, 255), width=3)
    # tanker
    draw.polygon([(x + 40, y + h - 66), (x + 40, y + h - 36),
                  (x + 84, y + h - 36), (x + 258, y + h - 36),
                  (x + 258, y + h - 66), (x + 232, y + h - 66)],
                 fill=(120, 40, 32))
    for i in range(3):
        bx = x + 62 + i * 56
        draw.rectangle([bx, y + h - 96, bx + 48, y + h - 66],
                       fill=(230, 226, 218))
    draw.rectangle([x + 232, y + h - 104, x + 252, y + h - 66],
                   fill=(240, 240, 240))
    # naval mine
    mx, my = x + 58, y + 34
    draw.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(30, 30, 30))
    for dx, dy in [(-16, 0), (16, 0), (0, -16), (0, 16),
                   (-12, -12), (12, -12), (-12, 12), (12, 12)]:
        draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=3)
    # warning triangle
    tx, ty = x + w - 56, y + 30
    draw.polygon([(tx, ty - 18), (tx - 18, ty + 12), (tx + 18, ty + 12)],
                 fill=(255, 200, 0), outline=(30, 30, 30))
    draw.text((tx, ty - 2), "!", font=SANS_BOLD(20), fill=(30, 30, 30),
              anchor="mm")


# ---------------------------------------------------------------- page build

GRID = [
    ("WAR IN EUROPE", "Ukraine hits Russian ships in the Gulf of Finland — and off Libya",
     draw_war),
    ("MIDDLE EAST", "Houthi strike hits Riyadh's tallest tower; 11 wounded",
     draw_tower),
    ("SPACE", "NATO vows to defend space as Russia readies a nuclear satellite",
     draw_space),
    ("COURTS", "Sarkozy ordered to trial; Trump gives Giuliani the Medal of Freedom",
     draw_courts),
    ("TECH & MARKETS", "Nvidia falls 7% in Huang affair fallout; Dell lifts AI outlook",
     draw_markets),
    ("WORLD", "Iran: three tankers hit by mines in Hormuz; singer lashed 74 times",
     draw_tanker),
]

ALSO_TODAY = (
    "US CIA and ODNI suffer a cybersecurity breach \u00b7 "
    "Israeli strike kills a Hamas official in Gaza \u00b7 "
    "NATO to deploy early-warning aircraft in Poland \u00b7 "
    "GTA 6 released worldwide on 19 November \u00b7 "
    "England beat Australia in the 2nd T20I \u00b7 "
    "South Korea's education minister resigns over an exam-cheating scandal"
)


def build_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    centre(d, "THE WORLD IN ONE DAY", W // 2, 22, SERIF_BOLD(58), INK)
    centre(d, "WEDNESDAY, 25 NOVEMBER 2026", W // 2, 92,
           SANS_BOLD(24), RED)
    d.line([MARGIN, 128, W - MARGIN, 128], fill=RULE, width=3)
    d.line([MARGIN, 133, W - MARGIN, 133], fill=RULE, width=1)

    # ---- lead story ----
    lead_x, lead_y = MARGIN, 148
    lead_w, lead_h = W - 2 * MARGIN, 268
    d.text((lead_x, lead_y), "LEAD STORY  \u00b7  TECH / COURTS",
           font=SANS_BOLD(16), fill=RED)
    headline = "HUAWEI FOUND GUILTY IN U.S. TRADE-SECRETS TRIAL"
    lines = wrap(d, headline, SERIF_BOLD(38), 560)
    y = draw_lines(d, lines, lead_x, lead_y + 28, SERIF_BOLD(38), INK, 46)
    deck = ("Guilty of trade-secret theft, acquitted of racketeering in a "
            "sprawling case over its Iran business — a verdict at the heart "
            "of the U.S.\u2013China tech war.")
    deck_lines = wrap(d, deck, SERIF(20), 560)
    draw_lines(d, deck_lines, lead_x, y + 8, SERIF(20), SOFT_INK, 27)
    draw_lead_art(d, lead_x + 596, lead_y + 8, 372, 252)
    d.line([MARGIN, 428, W - MARGIN, 428], fill=RULE, width=2)

    # ---- six-story grid ----
    grid_top = 444
    cell_w, cell_h = 312, 206
    gap_x, gap_y = 16, 14
    for i, (kicker, title, art) in enumerate(GRID):
        col, row = i % 3, i // 3
        cx = MARGIN + col * (cell_w + gap_x)
        cy = grid_top + row * (cell_h + gap_y)
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=CELL_BG,
                    outline=CELL_EDGE, width=1)
        d.text((cx + 12, cy + 10), kicker, font=SANS_BOLD(14), fill=BLUE)
        tlines = wrap(d, title, SANS_BOLD(19), cell_w - 24)
        draw_lines(d, tlines, cx + 12, cy + 32, SANS_BOLD(19), INK, 24)
        art(d, cx + 8, cy + cell_h - 96, cell_w - 16, 88)

    # ---- also today ----
    strip_y = 898
    d.rectangle([MARGIN, strip_y, W - MARGIN, H - 22], fill=DARK_BAND)
    d.text((MARGIN + 14, strip_y + 10), "ALSO TODAY",
           font=SANS_BOLD(16), fill=(255, 214, 120))
    body = wrap(d, ALSO_TODAY, SANS(17), W - 2 * MARGIN - 28)
    draw_lines(d, body, MARGIN + 14, strip_y + 34, SANS(17),
               (240, 238, 230), 23)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    path = build_poster()
    print("wrote", path, os.path.getsize(path), "bytes")
