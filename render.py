#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page (1024x1024 PNG).

Drawn programmatically with PIL so every letter is crisp. Run:
    python3 render.py            -> writes entry.png next to this file
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (16, 38, 63)
NAVY2 = (24, 56, 92)
RED = (180, 35, 24)
GOLD = (217, 164, 65)
GREEN = (31, 122, 61)
TEAL = (20, 120, 90)
WHITE = (255, 255, 255)
BORDER = (206, 198, 180)
GREY = (90, 88, 82)
LIGHT = (238, 232, 219)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 19)
    draw.text((x, y), text, font=f, fill=color)
    return y + 26


def panel(draw, x, y, w, h, accent=RED):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=WHITE, outline=BORDER, width=2)
    draw.rectangle([x, y + 8, x + 7, y + h - 8], fill=accent)


def icon_controller(draw, cx, cy):
    # game controller with a "VI" badge (GTA VI launch)
    draw.rounded_rectangle([cx - 88, cy - 42, cx + 88, cy + 42], radius=22,
                           fill=NAVY2)
    draw.ellipse([cx - 78, cy - 30, cx - 38, cy + 10], fill=(12, 28, 48))
    draw.ellipse([cx + 38, cy - 30, cx + 78, cy + 10], fill=(12, 28, 48))
    # d-pad
    draw.rectangle([cx - 62, cy - 22, cx - 54, cy + 2], fill=WHITE)
    draw.rectangle([cx - 70, cy - 14, cx - 46, cy - 6], fill=WHITE)
    # buttons
    for bx, by, c in ((cx + 48, cy - 20, GOLD), (cx + 62, cy - 6, RED),
                      (cx + 34, cy - 6, GREEN)):
        draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=c,
                     outline=WHITE, width=2)
    # VI badge
    draw.ellipse([cx - 26, cy + 6, cx + 26, cy + 40], fill=GOLD,
                 outline=WHITE, width=3)
    f = font(SANS_B, 22)
    t = "VI"
    draw.text((cx - draw.textlength(t, font=f) / 2, cy + 10), t,
              font=f, fill=NAVY)


def icon_trio(draw, cx, cy, r):
    # three leaders: US, China, Russia as coloured dots in a ring
    cols = [(35, 68, 140), (180, 35, 24), (232, 120, 30)]
    for i, c in enumerate(cols):
        a = math.radians(90 + i * 120)
        x = cx + r * 0.62 * math.cos(a)
        y = cy + r * 0.62 * math.sin(a)
        draw.ellipse([x - 14, y - 14, x + 14, y + 14], fill=c,
                     outline=WHITE, width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY2, width=3)
    f = font(SANS_B, 22)
    draw.text((cx - 6, cy - 11), "3", font=f, fill=NAVY2)


def icon_gavel(draw, cx, cy):
    # Speaker's gavel (compact: fits a ~60px strip)
    draw.rounded_rectangle([cx - 40, cy - 22, cx + 40, cy - 4], radius=7,
                           fill=(90, 60, 30))
    draw.rectangle([cx - 6, cy - 4, cx + 6, cy + 30], fill=(120, 82, 40))
    draw.ellipse([cx - 12, cy + 26, cx + 12, cy + 36], fill=(90, 60, 30))
    draw.rectangle([cx - 48, cy + 40, cx + 48, cy + 46], fill=NAVY2)


def icon_cyclone(draw, cx, cy, r):
    # spiral storm
    for i, rr in enumerate(range(r, 8, -9)):
        start = 20 + i * 55
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], start, start + 230,
                 fill=NAVY2 if i % 2 == 0 else RED, width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)


def icon_dish(draw, cx, cy):
    # deep-space dish beaming a signal (Voyager 1) — compact, no tall arcs
    draw.polygon([(cx - 32, cy - 14), (cx + 32, cy - 14), (cx, cy + 10)],
                 fill=NAVY2)
    draw.line([cx, cy + 10, cx, cy + 24], fill=NAVY2, width=4)
    draw.line([cx - 18, cy + 24, cx + 18, cy + 24], fill=NAVY2, width=4)
    for sx, sy in ((-56, -6), (56, -10), (70, 8)):
        draw.ellipse([cx + sx - 3, cy + sy - 3, cx + sx + 3, cy + sy + 3],
                     fill=GOLD)


def icon_flags(draw, cx, cy):
    # two flags side by side: India and Japan
    # India: saffron / white / green with wheel dot
    x0, y0 = cx - 78, cy - 34
    draw.rectangle([x0, y0, x0 + 66, y0 + 14], fill=(255, 153, 51))
    draw.rectangle([x0, y0 + 14, x0 + 66, y0 + 28], fill=WHITE)
    draw.rectangle([x0, y0 + 28, x0 + 66, y0 + 42], fill=(19, 136, 8))
    draw.ellipse([x0 + 26, y0 + 15, x0 + 40, y0 + 27], outline=NAVY2, width=2)
    # Japan: white with red disc
    x1 = cx + 12
    draw.rectangle([x1, y0, x1 + 66, y0 + 42], fill=WHITE,
                   outline=BORDER, width=2)
    draw.ellipse([x1 + 21, y0 + 9, x1 + 45, y0 + 33], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 134], fill=GOLD)
    f_title = font(SERIF, 52)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 12), title,
           font=f_title, fill=WHITE)
    f_date = font(SANS_B, 34)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 72), date,
           font=f_date, fill=GOLD)

    # ---------- lead story: GTA VI ----------
    lx, ly, lw, lh = 28, 152, 968, 330
    panel(d, lx, ly, lw, lh, accent=RED)
    tx = lx + 28
    y = ly + 18
    y = kicker(d, tx, y, "LEAD  ·  CULTURE — GAMING")
    f_h = font(SERIF, 42)
    lines = wrap(d, "GTA VI unlocks worldwide after 13 years",
                 f_h, 600)
    y = draw_text_block(d, tx, y + 4, 600, lines, f_h, INK, leading=50)
    f_s = font(SANS, 22)
    sub = ("Rockstar's Vice City return rolls out at midnight in each "
           "market; early reviews score 99 on Metacritic.")
    lines = wrap(d, sub, f_s, 600)
    y = draw_text_block(d, tx, y + 8, 600, lines, f_s, GREY, leading=28)
    f_tag = font(SANS_B, 20)
    d.text((tx, ly + lh - 44), "16m copies already sold, Sensor Tower says.",
           font=f_tag, fill=NAVY2)
    # illustration on the right
    ix = lx + lw - 300
    d.rectangle([ix, ly + 18, lx + lw - 22, ly + lh - 18], fill=LIGHT)
    icon_controller(d, ix + 130, ly + 160)

    # ---------- row 2: two panels ----------
    ry, rh = 502, 216
    pw = (968 - 20) // 2
    # Shenzhen trilateral
    x = 28
    panel(d, x, ry, pw, rh, accent=NAVY2)
    tx = x + 26
    y = ry + 14
    y = kicker(d, tx, y, "DIPLOMACY  ·  SHENZHEN", color=NAVY2)
    f_h2 = font(SERIF, 29)
    lines = wrap(d, "Trump, Xi, Putin meet in Shenzhen", f_h2, pw - 150)
    y = draw_text_block(d, tx, y + 2, pw - 150, lines, f_h2, INK, leading=35)
    lines = wrap(d, "First-ever trilateral at APEC; arms and Ukraine "
                    "on the agenda.",
                 font(SANS, 21), pw - 150)
    draw_text_block(d, tx, y + 6, pw - 150, lines, font(SANS, 21), GREY,
                    leading=26)
    icon_trio(d, x + pw - 72, ry + rh - 66, 46)
    # Jeffries
    x = 28 + pw + 20
    panel(d, x, ry, pw, rh, accent=RED)
    tx = x + 26
    y = ry + 14
    y = kicker(d, tx, y, "US  ·  POLITICS")
    lines = wrap(d, "Jeffries nominated for Speaker", f_h2, pw - 150)
    y = draw_text_block(d, tx, y + 2, pw - 150, lines, f_h2, INK, leading=35)
    lines = wrap(d, "Democrats pick him 251–11; he would be the first "
                    "Black Speaker.",
                 font(SANS, 21), pw - 150)
    draw_text_block(d, tx, y + 6, pw - 150, lines, font(SANS, 21), GREY,
                    leading=26)
    icon_gavel(d, x + pw - 72, ry + rh - 64)

    # ---------- row 3: three panels ----------
    ry3, rh3 = 738, 216
    pw3 = (968 - 40) // 3
    # Cyclone Akvan
    x = 28
    panel(d, x, ry3, pw3, rh3, accent=NAVY2)
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "WEATHER  ·  INDIA", color=NAVY2)
    f_h3 = font(SERIF, 26)
    lines = wrap(d, "Cyclone Akvan nears India", f_h3, pw3 - 48)
    y = draw_text_block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "Red alerts; schools shut. Landfall due Friday.",
                 font(SANS, 20), pw3 - 48)
    draw_text_block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY,
                    leading=25)
    icon_cyclone(d, x + pw3 // 2, ry3 + rh3 - 34, 20)
    # Voyager 1
    x = 28 + pw3 + 20
    panel(d, x, ry3, pw3, rh3, accent=GOLD)
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "SPACE  ·  NASA", color=(160, 110, 20))
    lines = wrap(d, "Voyager 1, one light-day away", f_h3, pw3 - 48)
    y = draw_text_block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "NASA marks the milestone today; a signal takes a day.",
                 font(SANS, 20), pw3 - 48)
    draw_text_block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY,
                    leading=25)
    icon_dish(d, x + pw3 // 2, ry3 + rh3 - 28)
    # India–Japan 2+2
    x = 28 + 2 * (pw3 + 20)
    panel(d, x, ry3, pw3, rh3, accent=TEAL)
    tx = x + 24
    y = ry3 + 14
    y = kicker(d, tx, y, "ASIA  ·  DEFENCE", color=TEAL)
    lines = wrap(d, "India–Japan 2+2 talks in Tokyo", f_h3, pw3 - 48)
    y = draw_text_block(d, tx, y + 2, pw3 - 48, lines, f_h3, INK, leading=31)
    lines = wrap(d, "Ministers review defence.",
                 font(SANS, 20), pw3 - 48)
    draw_text_block(d, tx, y + 6, pw3 - 48, lines, font(SANS, 20), GREY,
                    leading=25)
    icon_flags(d, x + pw3 // 2, ry3 + rh3 - 34)

    # ---------- footer ----------
    f_f = font(SANS, 18)
    foot = ("Sources: Reuters · AP · Yonhap · IMD · NASA · PIB — "
            "All events of Thursday 19 November 2026")
    d.text(((W - d.textlength(foot, font=f_f)) / 2, 972), foot,
           font=f_f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
