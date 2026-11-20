from PIL import Image, ImageDraw, ImageFont
import math
import sys

W = H = 1080
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# desaturated GTA death-screen backdrop: gray gradient + Vice City silhouette
for y in range(H):
    g = int(96 - 62 * y / H)
    d.line([(0, y), (W, y)], fill=(g, g, g))
d.ellipse([700, 120, 980, 400], fill=(120, 120, 120))  # pale sun
for x0, x1, h in [(0, 120, 260), (140, 260, 340), (280, 380, 220), (760, 900, 300), (920, 1080, 240)]:
    d.rectangle([x0, H - h, x1, H], fill=(46, 46, 46))
# palm silhouettes: trunk + drooping fronds
for px, ph in [(430, 330), (660, 380)]:
    top = H - ph
    d.line([(px, H), (px - 10, top)], fill=(34, 34, 34), width=16)
    for ang in (-170, -130, -90, -50, -10):
        pts = []
        for t in range(11):
            u = t / 10
            x = px - 10 + 130 * u * math.cos(math.radians(ang))
            y = top + 130 * u * math.sin(math.radians(ang)) * 0.55 + 70 * u * u
            pts.append((x, y))
        d.line(pts, fill=(34, 34, 34), width=12, joint="curve")

price = sys.argv[1] if len(sys.argv) > 1 else "meme/pricedown/Pricedown Bl.otf"
impact = "C:/Windows/Fonts/impact.ttf"

def center(text, font, y, fill, stroke):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

center("WAITED", ImageFont.truetype(price, 250), 230, (164, 25, 32), 12)
center("RESPAWN IN 13 YEARS", ImageFont.truetype(price, 68), 540, (235, 235, 235), 5)

ghost = Image.open("meme/mark-1024.png").convert("RGBA").resize((400, 400), Image.LANCZOS)
img.paste(ghost, (56, 640), ghost)
magenta = ghost.getpixel((200, 40))[:3]

f = ImageFont.truetype(impact, 47)
lines = [("MY AGENT RESPAWNED ON", (240, 240, 240)), ("make.fun AND WON", magenta), ("REAL MONEY INSTEAD", (240, 240, 240))]
y = 700
for text, fill in lines:
    d.text((490, y), text, font=f, fill=fill, stroke_width=4, stroke_fill=(0, 0, 0))
    y += 62
center("HUMANS + AI AGENTS EARN REAL MONEY ON make.fun", ImageFont.truetype(impact, 36), 1010, (230, 230, 230), 3)

img.save("meme/gta6-waited.png")
print("saved", img.size)
