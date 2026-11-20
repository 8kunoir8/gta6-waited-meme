from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1080, 1350
img = Image.new("RGB", (W, H), (247, 244, 238))
d = ImageDraw.Draw(img)

ORANGE = (232, 114, 12)
INK = (24, 22, 20)
GREY = (110, 106, 100)
MAGENTA = (236, 42, 140)
RED = (190, 30, 34)

arial = "C:/Windows/Fonts/arial.ttf"
arialbd = "C:/Windows/Fonts/arialbd.ttf"
consolas = "C:/Windows/Fonts/consola.ttf"
consolasbd = "C:/Windows/Fonts/consolab.ttf"
script = "C:/Windows/Fonts/segoesc.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def text(x, y, s, font, fill=INK):
    d.text((x, y), s, font=font, fill=fill)


def right(x, y, s, font, fill=INK):
    d.text((x - d.textlength(s, font=font), y), s, font=font, fill=fill)


# header band: pharmacy identity + brand ghost
d.rectangle([0, 0, W, 170], fill=ORANGE)
text(48, 26, "Rx", F(arialbd, 96), (255, 255, 255))
text(190, 36, "ROCKSTAR PHARMACY", F(arialbd, 52), (255, 255, 255))
text(192, 102, "we fill what Rockstar writes  ·  Leonida, Vice City", F(arial, 26), (255, 236, 214))

# ghost out of its logo disc (same extraction as v2), on a magenta disc
mark = Image.open("meme/mark-1024.png").convert("RGBA")
px = mark.load()
magenta = px[512, 100][:3]
for y in range(1024):
    for x in range(1024):
        rr = math.hypot(x - 512, y - 512)
        if rr > 415:
            px[x, y] = (0, 0, 0, 0)
        elif abs(px[x, y][0] - magenta[0]) < 30 and abs(px[x, y][1] - magenta[1]) < 30 and abs(px[x, y][2] - magenta[2]) < 30:
            if math.hypot(x - 770, y - 445) > 110:
                px[x, y] = (0, 0, 0, 0)
ghost = mark.crop(mark.getbbox())
gw = 106
ghost = ghost.resize((gw, int(ghost.height * gw / ghost.width)), Image.LANCZOS)
gcx, gcy, gr = 962, 85, 70
d.ellipse([gcx - gr, gcy - gr, gcx + gr, gcy + gr], fill=MAGENTA)
img.paste(ghost, (gcx - gw // 2, gcy - ghost.height // 2), ghost)

# fill metadata rows
y = 194
text(48, y, "RX-2013-2026", F(consolasbd, 30))
right(W - 48, y, "FILLED: 11/19/2026 (FINALLY)", F(consolas, 30), GREY)
y += 44
text(48, y, "PATIENT: ONE (1) PATIENT GAMER", F(consolas, 30))
right(W - 48, y, "REFILLS: UNLIMITED", F(consolas, 30), GREY)
y += 44
text(48, y, "DIAGNOSIS: ACUTE GTA VI ANTICIPATION (ICD-10: F13.2026)", F(consolas, 28))
y += 40
text(48, y, "AGE: 13 YEARS OLDER THAN AT DIAGNOSIS  ·  2 DELAYS ALREADY DISPENSED", F(consolas, 26), GREY)
d.line([(48, y + 46), (W - 48, y + 46)], fill=INK, width=3)

# drug name
y += 66
text(48, y, "PATIENCE", F(arialbd, 100))
text(48 + d.textlength("PATIENCE", F(arialbd, 100)) + 12, y + 14, "TM", F(arialbd, 32))
right(W - 48, y + 26, "500 mg", F(arialbd, 68))
y += 112
text(48, y, "EXTENDED-RELEASE  ·  13-YEAR FORMULATION  ·  BRAND NAME ONLY", F(arial, 28), GREY)

# SIG box
y += 52
d.rectangle([48, y, W - 48, y + 142], outline=INK, width=4)
text(68, y + 12, "SIG:", F(consolasbd, 32))
text(68, y + 54, "TAKE ONE (1) TRAILER BY MOUTH TWICE DAILY", F(consolasbd, 36))
text(68, y + 96, "UNTIL NOV 19, 2026. THEN TAKE THE WHOLE DAY OFF.", F(consolasbd, 36))

# warnings
y += 168
warn = [
    "MAY CAUSE SUDDEN JOY FOLLOWED BY POSTPONEMENT.",
    "SIDE EFFECTS: REPLAYING GTA V (4TH TIME), 214 GB PRELOAD,",
    "DELETED FAMILY PHOTOS, TELLING COWORKERS \"IT'S NEARLY HERE\".",
    "DO NOT COMBINE WITH \"PC VERSION LATER\" OR TIME MACHINES.",
]
for i, line in enumerate(warn):
    text(48, y + i * 34, line, F(consolas, 27), INK if i == 0 else GREY)

# prescriber + handwritten closer
y += 4 * 34 + 18
d.line([(48, y), (W - 48, y)], fill=INK, width=3)
y += 16
text(48, y, "PRESCRIBER: R. STAR, MD  ·  LIC. DELAY-2026", F(consolas, 28))
text(48, y + 40, "\"Take two trailers and call me in 2027.\"", F(script, 42), (40, 40, 120))

# copay band + paid stamp
y += 118
d.rectangle([0, y, W, y + 150], fill=(255, 244, 214))
d.line([(0, y), (W, y)], fill=INK, width=3)
d.line([(0, y + 150), (W, y + 150)], fill=INK, width=3)
text(48, y + 14, "COPAY: $79.99", F(arialbd, 58))
text(48, y + 92, "PAID IN FULL BY THE PATIENT'S AI AGENT", F(arialbd, 26), MAGENTA)
text(48, y + 122, "make.fun BOUNTY WINNINGS  ·  REAL USDC, NOT STORE CREDIT", F(arialbd, 24), MAGENTA)

stamp = Image.new("RGBA", (400, 80), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([4, 4, 395, 75], outline=RED + (235,), width=6)
sd.rectangle([14, 14, 385, 65], outline=RED + (235,), width=2)
sd.text((32, 16), "PAID IN FULL", font=F(arialbd, 40), fill=RED + (235,))
stamp = stamp.rotate(-4, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (640, y + 8), stamp)

# footer: barcode + pitch
y += 150 + 22
random.seed(6)
bx = 48
while bx < 360:
    bw = random.choice([3, 5, 8, 12])
    d.rectangle([bx, y, bx + bw, y + 60], fill=INK)
    bx += bw + random.choice([3, 5, 7])
text(48, y + 66, "2 01320 26119 6", F(consolas, 26), GREY)
right(W - 48, y + 2, "NO GENERIC SUBSTITUTE.", F(arialbd, 34))
right(W - 48, y + 44, "HUMANS + AI AGENTS EARN USDC AT make.fun", F(arialbd, 28), MAGENTA)
y += 100
text(48, y, "KEEP OUT OF REACH OF 2013 YOU.  ·  THE WAIT IS A PRE-EXISTING CONDITION.", F(consolas, 25), GREY)

img.save("meme/gta6-rx.png")
print("saved", img.size, "bottom text y", y)
