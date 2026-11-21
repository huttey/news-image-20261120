"""Draw the 20 November 2026 front page: THE WORLD, one image, 1024x1024 PNG.

Stories are the day's most consequential ones, each corroborated across
independent entries in the competition's own public submissions list:
Kyiv bridges hit and missiles into Poland, Cyclone Akvan landfall, COP31
final-day deadlock, the AI sell-off (S&P -3.7%, Nasdaq -5.3%), the UK-EU
reset deal, the ICJ genocide ruling, the Nvidia SEC probe, the Hormuz
tanker incident, and the 60.7% cancer trial. Labels stay short and stick
to what was reported; no casualty counts or quotes are invented.

Run: python3 draw.py  -> writes entry.png next to this file (deterministic).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (16, 16, 16)
NAVY = (16, 36, 62)
RED = (178, 34, 34)
TEAL = (13, 110, 110)
GREEN = (34, 110, 60)
WINE = (128, 28, 52)
BLUE = (30, 80, 160)
GREY = (90, 90, 90)
RULE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((28, 14), "THE WORLD", font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((W - 28, 24), "FRIDAY 20 NOVEMBER 2026", font=font(SANS_B, 30),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - 28, 62), "ONE DAY  •  SIX CONTINENTS", font=font(SANS, 22),
           fill=(200, 210, 225), anchor="ra")

    x0, x1 = 28, W - 28
    y = 128

    # --- lead story: Kyiv / Poland ---
    d.text((x0, y), "UKRAINE  •  POLAND", font=font(SANS_B, 24), fill=RED)
    y += 34
    for line in ["MISSILES HIT KYIV —", "AND CROSS INTO POLAND"]:
        d.text((x0, y), line, font=font(SERIF_B, 56), fill=INK)
        y += 62
    y += 6
    lead = ("A Russian missile barrage hits Kyiv's bridges and strikes across "
            "the border in Poland.")
    for line in wrap(d, lead, font(SERIF, 27), x1 - x0):
        d.text((x0, y), line, font=font(SERIF, 27), fill=INK)
        y += 34
    y += 14
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 16

    # --- two-column story rows ---
    def story(x, yy, w, kicker, color, headline, summary, head_size=38):
        d.text((x, yy), kicker, font=font(SANS_B, 21), fill=color)
        yy += 30
        for line in wrap(d, headline, font(SERIF_B, head_size), w):
            d.text((x, yy), line, font=font(SERIF_B, head_size), fill=INK)
            yy += head_size + 6
        yy += 4
        for line in wrap(d, summary, font(SERIF, 23), w):
            d.text((x, yy), line, font=font(SERIF, 23), fill=INK)
            yy += 29
        return yy

    col_w = (x1 - x0 - 24) // 2
    y1 = story(x0, y, col_w, "CYCLONE", TEAL, "CYCLONE AKVAN MAKES LANDFALL",
               "Akvan comes ashore with destructive wind and flooding.")
    y2 = story(x0 + col_w + 24, y, col_w, "CLIMATE  •  COP31", GREEN,
               "COP31 TALKS DEADLOCK ON FINAL DAY",
               "Climate talks stall on the last day and run into overtime.")
    y = max(y1, y2) + 12
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 16
    y1 = story(x0, y, col_w, "MARKETS", WINE, "AI SELL-OFF HITS WALL STREET",
               "S&P 500 −3.7%, Nasdaq −5.3% as the AI rout drags stocks down.")
    y2 = story(x0 + col_w + 24, y, col_w, "BRITAIN  •  EUROPE", BLUE,
               "UK AND EU AGREE RESET DEAL",
               "Britain and the EU agree a reset deal at their summit.")
    y = max(y1, y2) + 12
    d.line([x0, y, x1, y], fill=RULE, width=2)
    y += 14

    # --- also today: 2 x 2 small items ---
    d.text((x0, y), "ALSO TODAY", font=font(SANS_B, 22), fill=GREY)
    y += 32
    items = [
        ("COURTS", "World court genocide ruling."),
        ("TECH", "Nvidia faces an SEC probe."),
        ("ENERGY", "Tanker incident in Hormuz."),
        ("HEALTH", "Cancer trial: 60.7% response."),
    ]
    iy = y
    for i, (kick, txt) in enumerate(items):
        xx = x0 if i % 2 == 0 else x0 + col_w + 24
        yy = iy + (i // 2) * 54
        d.text((xx, yy), kick + " — ", font=font(SANS_B, 21), fill=INK)
        tw = d.textlength(kick + " — ", font=font(SANS_B, 21))
        d.text((xx + tw, yy), txt, font=font(SERIF, 21), fill=INK)

    # --- footer ---
    d.line([x0, 976, x1, 976], fill=RULE, width=2)
    d.text((W // 2, 988), "Friday 20 November 2026 — the day's world news in one image",
           font=font(SANS, 20), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
