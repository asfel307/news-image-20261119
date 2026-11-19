#!/usr/bin/env python3
"""Draw the one-day world news infographic for Thursday 19 November 2026.

Everything here is drawn from scratch with Pillow: a masthead, one lead
story with a night-skyline illustration, five smaller story cards, and a
sources footer. Run it from this directory; it writes entry.png beside it.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

INK = (13, 22, 38)          # deep navy page background
PAPER = (250, 247, 238)     # warm paper for the story cards
PAPER_EDGE = (214, 206, 188)
LEAD_BG = (24, 34, 64)      # lead panel, slightly lighter navy
AMBER = (245, 176, 65)
CORAL = (232, 93, 74)
TEAL = (45, 160, 150)
SKY = (84, 141, 212)
PLUM = (146, 94, 178)
LEAF = (74, 148, 74)
WHITE = (255, 255, 255)
SOFT = (226, 231, 240)      # pale text on dark panels
MUTED = (96, 104, 122)      # grey text on paper
DARK_TEXT = (28, 32, 46)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def load_typefaces():
    """Return the (bold, regular) DejaVu faces at a few fixed sizes."""
    bold_path = FONT_DIR / "DejaVuSans-Bold.ttf"
    plain_path = FONT_DIR / "DejaVuSans.ttf"
    faces = {}
    for size in (19, 22, 24, 26, 29, 32, 40, 52):
        faces[("bold", size)] = ImageFont.truetype(str(bold_path), size)
        faces[("plain", size)] = ImageFont.truetype(str(plain_path), size)
    return faces


def wrap_words(pencil, sentence, face, max_width):
    """Split a sentence into lines that fit inside max_width pixels."""
    lines = []
    current = ""
    for word in sentence.split():
        trial = f"{current} {word}".strip()
        if pencil.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(pencil, lines, left, top, face, colour, gap):
    """Draw stacked lines and return the y just below the last one."""
    y = top
    for line in lines:
        pencil.text((left, y), line, font=face, fill=colour)
        y += face.size + gap
    return y


def night_skyline(pencil, left, top, right, bottom):
    """A night city skyline with a moon and lit windows, for the lead art."""
    pencil.rectangle([left, top, right, bottom], fill=(16, 24, 54))
    # stars
    for sx, sy, sr in (
        (left + 24, top + 18, 2), (left + 90, top + 44, 2),
        (left + 150, top + 12, 3), (left + 210, top + 52, 2),
        (left + 260, top + 26, 2), (left + 300, top + 60, 2),
        (left + 60, top + 70, 2), (left + 180, top + 78, 2),
    ):
        pencil.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=WHITE)
    # moon
    pencil.ellipse([right - 92, top + 16, right - 28, top + 80], fill=(250, 232, 170))
    pencil.ellipse([right - 84, top + 28, right - 62, top + 50], fill=(228, 205, 140))
    # building silhouettes, back row then front row
    base = bottom
    back = [(0, 150, 46, 96), (52, 128, 44, 118), (102, 168, 50, 78),
            (158, 138, 46, 108), (210, 172, 48, 74), (264, 142, 46, 104)]
    for dx, dh, dw, _ in back:
        pencil.rectangle([left + dx, base - dh, left + dx + dw, base],
                         fill=(38, 50, 88))
    front = [(18, 108, 58), (84, 84, 52), (142, 122, 56), (204, 92, 54),
             (264, 116, 52)]
    for dx, dh, dw in front:
        pencil.rectangle([left + dx, base - dh, left + dx + dw, base],
                         fill=(22, 30, 58))
        # lit windows on the front row
        for wy in range(base - dh + 12, base - 10, 20):
            for wx in (left + dx + 10, left + dx + dw - 16):
                pencil.rectangle([wx, wy, wx + 6, wy + 8], fill=AMBER)
    pencil.rectangle([left, base - 4, right, base], fill=(10, 15, 30))


def three_heads(pencil, cx, cy, r, colour):
    """Three round heads above a shared table line: a summit in miniature."""
    for dx in (-r * 2, 0, r * 2):
        pencil.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], fill=colour)
    pencil.rectangle([cx - 2 * r - 8, cy + r + 6, cx + 2 * r + 8, cy + r + 12],
                     fill=colour)


def capitol_dome(pencil, cx, cy, _r, colour):
    """A small capitol dome: drum, cupola and a flag on top."""
    pencil.rectangle([cx - 26, cy + 6, cx + 26, cy + 26], fill=colour)
    pencil.pieslice([cx - 22, cy - 18, cx + 22, cy + 14], 180, 360, fill=colour)
    pencil.rectangle([cx - 3, cy - 26, cx + 3, cy - 16], fill=colour)
    pencil.rectangle([cx + 3, cy - 26, cx + 16, cy - 18], fill=CORAL)
    for dx in (-20, -7, 6, 19):
        pencil.rectangle([cx + dx - 2, cy + 12, cx + dx + 2, cy + 26],
                         fill=PAPER)


def cyclone_swirl(pencil, cx, cy, _r, colour):
    """Concentric broken arcs suggesting a cyclone seen from above."""
    for i, radius in enumerate((26, 20, 14, 8)):
        start = 20 + i * 55
        pencil.arc([cx - radius, cy - radius, cx + radius, cy + radius],
                   start, start + 250, fill=colour, width=4)
    pencil.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=colour)


def space_probe(pencil, cx, cy, _r, colour):
    """A deep-space probe: dish, body and a long antenna."""
    pencil.line([cx - 24, cy + 18, cx + 4, cy - 6], fill=colour, width=4)
    pencil.polygon([(cx - 26, cy + 2), (cx + 2, cy - 14), (cx + 10, cy + 8)],
                   fill=colour)
    pencil.rectangle([cx + 2, cy - 2, cx + 22, cy + 10], fill=colour)
    pencil.line([cx + 22, cy + 4, cx + 30, cy - 14], fill=colour, width=3)
    pencil.ellipse([cx + 27, cy - 17, cx + 33, cy - 11], fill=AMBER)
    for sx, sy in ((cx - 30, cy - 18), (cx + 28, cy + 20), (cx - 8, cy - 24)):
        pencil.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)


def torii_gate(pencil, cx, cy, _r, colour):
    """A vermilion gate with two pillars and a double beam."""
    pencil.rectangle([cx - 24, cy - 14, cx - 16, cy + 24], fill=colour)
    pencil.rectangle([cx + 16, cy - 14, cx + 24, cy + 24], fill=colour)
    pencil.rectangle([cx - 30, cy - 20, cx + 30, cy - 12], fill=colour)
    pencil.rectangle([cx - 24, cy - 8, cx + 24, cy - 2], fill=colour)
    pencil.ellipse([cx - 5, cy + 6, cx + 5, cy + 16], fill=AMBER)


ICONS = {
    "summit": three_heads,
    "dome": capitol_dome,
    "storm": cyclone_swirl,
    "probe": space_probe,
    "gate": torii_gate,
}


def story_card(pencil, faces, box, tag, tag_colour, icon, title, body):
    """Paint one story card: tag + icon row, bold title, short body."""
    x0, y0, x1, y1 = box
    pencil.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PAPER,
                             outline=PAPER_EDGE, width=2)
    pencil.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=tag_colour)
    # tag chip
    chip = faces[("bold", 19)]
    chip_w = pencil.textlength(tag, font=chip) + 22
    pencil.rounded_rectangle([x0 + 16, y0 + 22, x0 + 16 + chip_w, y0 + 50],
                             radius=13, fill=tag_colour)
    pencil.text((x0 + 27, y0 + 26), tag, font=chip, fill=WHITE)
    # pictogram in a tinted disc at the top right
    disc_cx, disc_cy, disc_r = x1 - 48, y0 + 52, 34
    pencil.ellipse([disc_cx - disc_r, disc_cy - disc_r,
                    disc_cx + disc_r, disc_cy + disc_r],
                   fill=tag_colour)
    ICONS[icon](pencil, disc_cx, disc_cy, 10, WHITE)
    # title and body
    title_face = faces[("bold", 29)]
    body_face = faces[("plain", 22)]
    inner_w = (x1 - x0) - 32
    title_lines = wrap_words(pencil, title, title_face, inner_w)
    y = put_lines(pencil, title_lines, x0 + 16, y0 + 66, title_face,
                  DARK_TEXT, 4)
    body_lines = wrap_words(pencil, body, body_face, inner_w)
    put_lines(pencil, body_lines, x0 + 16, y + 8, body_face, MUTED, 5)


def build_sheet():
    """Compose the whole 1024x1024 sheet and return the image."""
    faces = load_typefaces()
    sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), INK)
    pencil = ImageDraw.Draw(sheet)

    # ---- masthead ------------------------------------------------------
    mast = "THE WORLD IN ONE DAY"
    mast_face = faces[("bold", 52)]
    mast_w = pencil.textlength(mast, font=mast_face)
    pencil.text(((CANVAS_W - mast_w) / 2, 14), mast, font=mast_face, fill=WHITE)
    date_line = "THURSDAY  •  19 NOVEMBER 2026"
    date_face = faces[("bold", 26)]
    date_w = pencil.textlength(date_line, font=date_face)
    pencil.text(((CANVAS_W - date_w) / 2, 78), date_line, font=date_face,
                fill=AMBER)
    pencil.line([28, 116, CANVAS_W - 28, 116], fill=(52, 66, 96), width=2)

    # ---- lead story: GTA VI -------------------------------------------
    pencil.rounded_rectangle([16, 128, 1008, 384], radius=16, fill=LEAD_BG,
                             outline=(52, 66, 96), width=2)
    pencil.rounded_rectangle([32, 146, 32 + 264, 174], radius=13, fill=CORAL)
    pencil.text((43, 150), "LEAD STORY  •  GAMES", font=faces[("bold", 19)],
                fill=WHITE)
    headline = "GTA VI launches worldwide"
    head_face = faces[("bold", 40)]
    pencil.text((32, 186), headline, font=head_face, fill=WHITE)
    lead_body = ("Unlocks at midnight in each market, starting in New "
                 "Zealand — 13 years after GTA V. Early reviews: 99 on "
                 "Metacritic.")
    lead_lines = wrap_words(pencil, lead_body, faces[("plain", 24)], 596)
    put_lines(pencil, lead_lines, 32, 244, faces[("plain", 24)], SOFT, 7)
    pencil.text((32, 344), "Sources: Reuters, AP",
                font=faces[("plain", 19)], fill=(170, 180, 200))
    night_skyline(pencil, 660, 146, 992, 368)

    # ---- middle row: three stories ------------------------------------
    middle = [
        ("DIPLOMACY", SKY, "summit",
         "Trump, Xi, Putin in Shenzhen",
         "First three-way talks at APEC. Nuclear arms and Ukraine on "
         "agenda. (Yonhap, Reuters)"),
        ("U.S. POLITICS", PLUM, "dome",
         "Jeffries picked for Speaker",
         "House Democrats pick him 251–11. Full House vote 3 January; "
         "would be the first Black Speaker. (AP, NPR)"),
        ("WEATHER", TEAL, "storm",
         "Cyclone Akvan nears India",
         "Severe storm, red alert; schools shut in Odisha. Landfall "
         "expected Friday. (IMD, The Hindu)"),
    ]
    card_w = 325
    for i, (tag, colour, icon, title, body) in enumerate(middle):
        x0 = 16 + i * (card_w + 8)
        story_card(pencil, faces, (x0, 396, x0 + card_w, 688),
                   tag, colour, icon, title, body)

    # ---- bottom row: two stories --------------------------------------
    bottom = [
        ("SPACE", (52, 92, 160), "probe",
         "Voyager 1 reaches one light-day",
         "NASA marks the milestone today — the farthest human-made object "
         "from Earth. (NASA, Reuters)"),
        ("ASIA", LEAF, "gate",
         "India–Japan 2+2 talks in Tokyo",
         "Foreign and defence ministers discuss defence ties and a free "
         "Indo-Pacific. (PIB, The Hindu)"),
    ]
    wide_w = 492
    for i, (tag, colour, icon, title, body) in enumerate(bottom):
        x0 = 16 + i * (wide_w + 8)
        story_card(pencil, faces, (x0, 700, x0 + wide_w, 948),
                   tag, colour, icon, title, body)

    # ---- footer: sources ----------------------------------------------
    footer = ("Sources: Reuters · AP · Yonhap · NPR · IMD · The Hindu · "
              "NASA · PIB  —  Thursday 19 November 2026")
    foot_face = faces[("plain", 19)]
    foot_w = pencil.textlength(footer, font=foot_face)
    pencil.text(((CANVAS_W - foot_w) / 2, 968), footer, font=foot_face,
                fill=(170, 180, 200))
    return sheet


def main():
    """Render the sheet and save it as entry.png beside this file."""
    sheet = build_sheet()
    target = Path(__file__).resolve().parent / "entry.png"
    sheet.save(target, format="PNG", optimize=True)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
