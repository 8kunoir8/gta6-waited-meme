from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1080
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# Vice City sunset: purple -> magenta -> orange horizon, dark ground below
horizon = 780
for y in range(H):
    if y < horizon:
        t = y / horizon
        if t < 0.55:
            u = t / 0.55
            c = (int(46 + 140 * u), int(20 + 20 * u), int(70 + 60 * u))
        else:
            u = (t - 0.55) / 0.45
            c = (int(186 + 64 * u), int(40 + 100 * u), int(130 - 70 * u))
    else:
        c = (28, 18, 38)
    d.line([(0, y), (W, y)], fill=c)

# synthwave sun with widening stripe gaps below its center
cx, cy, r = 840, 470, 150
for y in range(cy - r, cy + r):
    dy = y - cy
    if dy > 0 and (dy // 16) % 2 == 1:
        continue
    half = int(math.sqrt(r * r - dy * dy))
    t = (y - (cy - r)) / (2 * r)
    d.line([(cx - half, y), (cx + half, y)], fill=(255, int(190 - 90 * t), int(90 + 40 * t)))

# palm silhouettes
for px, ph in [(150, 420), (930, 460)]:
    top = horizon - ph
    d.line([(px, horizon), (px - 12, top)], fill=(24, 14, 32), width=18)
    for ang in (-170, -130, -90, -50, -10):
        pts = []
        for t in range(11):
            u = t / 10
            x = px - 12 + 140 * u * math.cos(math.radians(ang))
            y = top + 140 * u * math.sin(math.radians(ang)) * 0.55 + 75 * u * u
            pts.append((x, y))
        d.line(pts, fill=(24, 14, 32), width=13, joint="curve")

# ghost out of its logo disc: drop everything outside r=415 and disc magenta
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
gw = 560
ghost = ghost.resize((gw, int(ghost.height * gw / ghost.width)), Image.LANCZOS)
img.paste(ghost, (161, 463), ghost)

# store counter over the ghost's lower body: he is the customer
d.rectangle([0, 780, W, 830], fill=(74, 42, 62))
d.line([(0, 780), (W, 780)], fill=(120, 70, 96), width=6)
d.rectangle([0, 830, W, H], fill=(40, 24, 40))

# price card standing on the counter
d.rectangle([810, 620, 1030, 780], fill=(245, 240, 235), outline=(20, 16, 24), width=6)
price = "meme/pricedown/Pricedown Bl.otf"
impact = "C:/Windows/Fonts/impact.ttf"
d.text((838, 630), "GTA 6", font=ImageFont.truetype(price, 52), fill=(20, 16, 24))
d.text((838, 688), "$70", font=ImageFont.truetype(price, 78), fill=(164, 25, 32))

# shop signage on the counter front: the pitch, in the scene's own voice
d.text((60, 872), "make.fun", font=ImageFont.truetype(impact, 56), fill=(240, 240, 240))
d.text((60, 950), "HUMANS + AI AGENTS EARN USDC HERE", font=ImageFont.truetype(impact, 30), fill=(236, 42, 140))
since = "CUSTOMER SINCE 2013"
f30 = ImageFont.truetype(impact, 30)
d.text((W - 60 - d.textlength(since, font=f30), 950), since, font=f30, fill=(200, 190, 205))


def center(text, size, y, fill):
    f = ImageFont.truetype(price, size)
    while d.textlength(text, font=f) > W - 70:
        size -= 4
        f = ImageFont.truetype(price, size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0))


center("DIED WAITING FOR GTA 6.", 92, 60, (245, 245, 245))
center("STILL PAYING $70 DAY ONE.", 66, 190, (236, 42, 140))

img.save("meme/gta6-dayone.png")
print("saved", img.size)
