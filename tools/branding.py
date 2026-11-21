"""Generate channel branding: profile picture, banner, watermark.

Usage: python3 branding.py "Money Mechanics" out_dir
Logo concept: a gear (mechanics) with a rising chart arrow inside (money growing).
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-{}.otf"
NAVY0, NAVY1 = (8, 13, 26), (17, 27, 48)
GREEN, GOLD, WHITE, MUTED, GRID = (34, 197, 94), (250, 204, 21), (241, 245, 249), (148, 163, 184), (30, 41, 64)

def f(size, w="Black"):
    return ImageFont.truetype(FONT.format(w), size)

def gradient(w, h, glow=(0.5, 0.45), gs=(0.5, 0.5)):
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(0, 1, w)[None, :]
    base = np.array(NAVY0) + (np.array(NAVY1) - np.array(NAVY0)) * (0.8 * y)[..., None]
    g = np.exp(-(((x - glow[0]) / gs[0]) ** 2 + ((y - glow[1]) / gs[1]) ** 2))[..., None]
    base = base + g * np.array([16, 44, 40])
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")

def gear_polygon(cx, cy, r_out, r_in, teeth=8, tooth_frac=0.42, steps=12):
    pts = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth
        span = 2 * math.pi / teeth
        t0, t1 = a0 + span * (0.5 - tooth_frac / 2), a0 + span * (0.5 + tooth_frac / 2)
        # valley up to tooth start
        for k in range(steps):
            a = a0 + (t0 - a0) * k / steps
            pts.append((cx + r_in * math.cos(a), cy + r_in * math.sin(a)))
        # tooth (slight taper)
        taper = span * 0.04
        pts.append((cx + r_out * math.cos(t0 + taper), cy + r_out * math.sin(t0 + taper)))
        pts.append((cx + r_out * math.cos(t1 - taper), cy + r_out * math.sin(t1 - taper)))
        for k in range(steps + 1):
            a = t1 + (a0 + span - t1) * k / steps
            pts.append((cx + r_in * math.cos(a), cy + r_in * math.sin(a)))
    return pts

def draw_logo(size, bg=True):
    """Logo mark rendered at 3x then downsampled for smooth edges."""
    S = size * 3
    img = gradient(S, S, glow=(0.5, 0.42), gs=(0.55, 0.55)) if bg else Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = S / 2
    r_out, r_in = S * 0.40, S * 0.335
    d.polygon(gear_polygon(c, c, r_out, r_in, teeth=8), fill=GREEN)
    d.ellipse([c - S * 0.27, c - S * 0.27, c + S * 0.27, c + S * 0.27], fill=NAVY0)
    # rising chart arrow inside the gear
    w = S * 0.026
    pts = [(c - S * 0.17, c + S * 0.10), (c - S * 0.06, c - S * 0.01), (c + 0.0 * S, c + S * 0.05), (c + S * 0.15, c - S * 0.11)]
    d.line(pts, fill=GOLD, width=int(w * 1.6), joint="curve")
    for p in pts[:-1]:
        d.ellipse([p[0] - w, p[1] - w, p[0] + w, p[1] + w], fill=GOLD)
    # arrow head
    tip = (c + S * 0.19, c - S * 0.155)
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    hl = S * 0.085
    left = (tip[0] - hl * math.cos(ang - 0.5), tip[1] - hl * math.sin(ang - 0.5))
    right = (tip[0] - hl * math.cos(ang + 0.5), tip[1] - hl * math.sin(ang + 0.5))
    d.polygon([tip, left, right], fill=GOLD)
    return img.resize((size, size), Image.LANCZOS)

def profile(out, size=800):
    img = draw_logo(size)
    img.convert("RGB").save(os.path.join(out, "profile_800.png"))

def watermark(out, size=150):
    img = Image.new("RGBA", (size * 3, size * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([6, 6, size * 3 - 6, size * 3 - 6], fill=NAVY0 + (235,), outline=GREEN, width=14)
    mark = draw_logo(int(size * 3 * 0.86), bg=False)
    img.alpha_composite(mark, ((size * 3 - mark.width) // 2, (size * 3 - mark.height) // 2))
    img.resize((size, size), Image.LANCZOS).save(os.path.join(out, "watermark_150.png"))

def banner(name, out):
    W, H = 2048, 1152
    img = gradient(W, H, glow=(0.5, 0.5), gs=(0.35, 0.3))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 64):
        d.line([(x, 0), (x, H)], fill=GRID + (110,))
    for y in range(0, H, 64):
        d.line([(0, y), (W, y)], fill=GRID + (110,))
    # faint rising chart across the background
    rng = np.random.default_rng(7)
    xs = np.linspace(0, W, 60)
    ys = 900 - np.cumsum(rng.normal(6, 14, 60))
    ys = ys - (ys.min() - 260)
    ch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ch).line(list(zip(xs, ys)), fill=GREEN + (60,), width=6, joint="curve")
    img.alpha_composite(ch.filter(ImageFilter.GaussianBlur(1)))
    # safe area (visible on all devices): 1546 x 423, centred
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    # fit logo + text block inside the safe area with a margin
    margin = 60
    avail = 1546 - 2 * margin
    size = 132
    while True:
        name_font = f(size)
        logo_px = int(size * 2.0)
        nw = d.textlength(name.upper(), font=name_font)
        if logo_px + 40 + nw <= avail or size <= 70:
            break
        size -= 4
    tag_font = ImageFont.truetype(FONT.format("SemiBold"), int(size * 0.38))
    sub_font = ImageFont.truetype(FONT.format("Bold"), int(size * 0.27))
    logo = draw_logo(logo_px, bg=False)
    total = logo_px + 40 + nw
    x0 = W / 2 - total / 2
    cy = H / 2
    img.alpha_composite(logo, (int(x0), int(cy - logo_px / 2)))
    tx = x0 + logo_px + 40
    d.text((tx, cy - size * 0.55), name.upper(), font=name_font, fill=WHITE, anchor="lm")
    d.text((tx + 4, cy + size * 0.30), "How money, markets & business really work", font=tag_font, fill=GOLD, anchor="lm")
    pill = "NEW SHORTS DAILY  ·  DEEP DIVES 3x A WEEK"
    pw = d.textlength(pill, font=sub_font) + 48
    py0, py1 = cy + size * 0.68, cy + size * 0.68 + size * 0.42
    d.rounded_rectangle([tx, py0, tx + pw, py1], int(size * 0.21), fill=(14, 52, 42), outline=GREEN, width=3)
    d.text((tx + 24, (py0 + py1) / 2), pill, font=sub_font, fill=GREEN, anchor="lm")
    img.convert("RGB").save(os.path.join(out, "banner_2048x1152.png"))
    # preview with the safe area marked (for checking only, do not upload)
    prev = img.copy(); pd = ImageDraw.Draw(prev)
    pd.rectangle([sx0, sy0, sx0 + 1546, sy0 + 423], outline=(255, 80, 80, 255), width=4)
    prev.convert("RGB").resize((1024, 576)).save(os.path.join(out, "banner_preview_safe_area.png"))

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    profile(out); watermark(out); banner(name, out)
    print("done:", sorted(os.listdir(out)))
