"""Channel branding v2: "the money machine".

Logo = a gold coin whose edge is a gear (Money + Mechanics).
Banner = metallic gears + gold coin stacks + glowing growth arrow around the channel name.

Usage: python3 branding_v2.py "Money Mechanics" out_dir
Outputs: profile_800.png, banner_2560x1440.png, watermark_150.png, channel_page_preview.png
Banner safe area (shown on every device) at 2560x1440 = centre 1546 x 423 (= 1235 x 338 at 2048 x 1152).
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FD = "/usr/share/fonts/opentype/inter/"
def F(size, w="Black", display=True):
    return ImageFont.truetype(FD + ("InterDisplay-" if display else "Inter-") + w + ".otf", int(size))

# ---------------------------------------------------------------- metal colour ramps
GOLD = [(0.00, (110, 72, 12)), (0.20, (196, 142, 40)), (0.38, (252, 214, 112)), (0.50, (255, 243, 196)),
        (0.62, (236, 186, 72)), (0.80, (160, 108, 22)), (1.00, (232, 190, 90))]
GOLD_FACE = [(0.0, (128, 84, 16)), (0.3, (190, 140, 46)), (0.5, (226, 186, 100)), (0.7, (176, 124, 34)),
             (1.0, (146, 98, 22))]
GOLD_SYM = [(0.0, (190, 130, 26)), (0.35, (255, 222, 128)), (0.5, (255, 248, 215)), (0.65, (250, 205, 90)),
            (1.0, (206, 150, 40))]
EMERALD = [(0.0, (3, 46, 36)), (0.25, (8, 110, 80)), (0.45, (45, 200, 145)), (0.55, (120, 240, 190)),
           (0.7, (16, 170, 115)), (0.88, (5, 80, 58)), (1.0, (60, 205, 150))]
SILVER = [(0.0, (70, 80, 95)), (0.3, (160, 170, 185)), (0.5, (240, 244, 250)), (0.7, (150, 160, 175)),
          (1.0, (200, 208, 220))]
GOLD_TEXT = [(0.0, (255, 246, 200)), (0.40, (250, 208, 96)), (0.52, (214, 150, 36)), (0.70, (240, 186, 66)),
             (1.0, (255, 226, 140))]
NAVY0, NAVY1 = (5, 9, 20), (13, 24, 46)

def ramp(t, stops):
    xs = [s[0] for s in stops]
    out = np.empty(t.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(t, xs, [s[1][c] for s in stops])
    return out

def metal(mask, stops, sheen=2, phase=0.8, vgrad=0.3, bevel=10, strength=1.0, light=(-0.7, -0.7)):
    """Shade a mask like polished metal: conic sheen + top light + bevelled edges (bump mapping)."""
    m = np.asarray(mask, np.float32) / 255.0
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.arctan2(yy - H / 2, xx - W / 2)
    t = 0.5 + 0.5 * np.cos(sheen * ang - phase)
    t = (1 - vgrad) * t + vgrad * (1 - yy / H)
    rgb = ramp(np.clip(t, 0, 1), stops)
    if bevel:
        h = np.asarray(mask.filter(ImageFilter.GaussianBlur(bevel)), np.float32) / 255.0
        gy, gx = np.gradient(h)
        shade = -(gx * light[0] + gy * light[1])
        shade /= (np.abs(shade).max() + 1e-6)
        rgb += shade[..., None] * strength * 120
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), m * 255]).astype(np.uint8), "RGBA")

def metal_text(mask, stops, bbox, bevel=4, strength=0.8):
    m = np.asarray(mask, np.float32) / 255.0
    H, W = m.shape
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    t = np.clip((yy - bbox[1]) / max(1, bbox[3] - bbox[1]), 0, 1)
    rgb = ramp(t, stops)
    if bevel:
        h = np.asarray(mask.filter(ImageFilter.GaussianBlur(bevel)), np.float32) / 255.0
        gy, gx = np.gradient(h)
        shade = (gx + gy) * 0.7
        shade /= (np.abs(shade).max() + 1e-6)
        rgb += shade[..., None] * strength * 90
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), m * 255]).astype(np.uint8), "RGBA")

def gear_polygon(cx, cy, r_out, r_root, teeth, frac=0.48, steps=10, rot=0.0):
    pts = []
    span = 2 * math.pi / teeth
    for i in range(teeth):
        a0 = rot + span * i
        t0, t1 = a0 + span * (0.5 - frac / 2), a0 + span * (0.5 + frac / 2)
        for k in range(steps):
            a = a0 + (t0 - a0) * k / steps
            pts.append((cx + r_root * math.cos(a), cy + r_root * math.sin(a)))
        tp = span * 0.06
        pts += [(cx + r_out * math.cos(t0 + tp), cy + r_out * math.sin(t0 + tp)),
                (cx + r_out * math.cos(t1 - tp), cy + r_out * math.sin(t1 - tp))]
        for k in range(steps + 1):
            a = t1 + (a0 + span - t1) * k / steps
            pts.append((cx + r_root * math.cos(a), cy + r_root * math.sin(a)))
    return pts

def shadow_of(img, blur, offset, alpha=0.6, color=(0, 0, 0)):
    a = img.split()[3].filter(ImageFilter.GaussianBlur(blur))
    a = a.point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", img.size, color + (0,))
    sh.putalpha(a)
    out = Image.new("RGBA", (img.width + abs(offset[0]) * 2, img.height + abs(offset[1]) * 2), (0, 0, 0, 0))
    return sh, offset

def star_polygon(cx, cy, r, points=5, inner=0.45, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = rot + math.pi * i / points
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

# ---------------------------------------------------------------- the logo: gear-edged gold coin
def arc_text(draw_mask, text, c, r, size, start_deg, top=True, spacing=1.12):
    f = F(size, "Bold")
    widths = [f.getlength(ch) * spacing for ch in text]
    total = sum(widths)
    ang_total = total / r
    a = math.radians(start_deg) - (ang_total / 2 if top else -ang_total / 2)
    for ch, w in zip(text, widths):
        da = w / r
        mid = a + (da / 2 if top else -da / 2)
        tile = Image.new("L", (int(size * 2), int(size * 2)), 0)
        ImageDraw.Draw(tile).text((size, size), ch, font=f, fill=255, anchor="mm")
        rot = -(math.degrees(mid) + 90) if top else (90 - math.degrees(mid))
        tile = tile.rotate(rot, resample=Image.BICUBIC)
        x, y = c + r * math.cos(mid), c + r * math.sin(mid)
        draw_mask.paste(255, (int(x - size), int(y - size)), tile)
        a += da if top else -da

def coin_gear(S, teeth=12, top_text="MONEY MECHANICS", bottom_text="HOW MONEY WORKS", symbol="$", detail=True):
    c = S / 2
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gear = Image.new("L", (S, S), 0)
    ImageDraw.Draw(gear).polygon(gear_polygon(c, c, 0.48 * S, 0.43 * S, teeth, 0.5), fill=255)
    img.alpha_composite(metal(gear, GOLD, sheen=2, phase=0.9, vgrad=0.25, bevel=S * 0.012, strength=1.0))
    d = ImageDraw.Draw(img)
    rg = 0.392 * S
    d.ellipse([c - rg, c - rg, c + rg, c + rg], outline=(84, 54, 8, 255), width=max(2, int(S * 0.011)))
    face = Image.new("L", (S, S), 0)
    rf = 0.378 * S
    ImageDraw.Draw(face).ellipse([c - rf, c - rf, c + rf, c + rf], fill=255)
    img.alpha_composite(metal(face, GOLD_FACE, sheen=2, phase=2.5, vgrad=0.2, bevel=S * 0.012, strength=-0.9))
    if detail:
        # engraved ring text + beads, like a real coin
        eng = Image.new("L", (S, S), 0)
        ed = ImageDraw.Draw(eng)
        arc_text(eng, top_text, c, 0.305 * S, 0.054 * S, -90, top=True)
        arc_text(eng, bottom_text, c, 0.305 * S, 0.054 * S, 90, top=False)
        for side in (0, 180):
            a = math.radians(side)
            ed.polygon(star_polygon(c + 0.305 * S * math.cos(a), c + 0.305 * S * math.sin(a), 0.022 * S), fill=255)
        k = max(1, int(S * 0.0035))
        hi = Image.new("RGBA", (S, S), (255, 236, 170, 0)); hi.putalpha(ImageChops.offset(eng, k, k).point(lambda v: int(v * 0.55)))
        lo = Image.new("RGBA", (S, S), (96, 62, 10, 0)); lo.putalpha(eng.point(lambda v: int(v * 0.85)))
        img.alpha_composite(hi); img.alpha_composite(lo)
        beads = Image.new("L", (S, S), 0)
        bd = ImageDraw.Draw(beads)
        rb, br = 0.356 * S, 0.0062 * S
        for i in range(84):
            a = 2 * math.pi * i / 84
            x, y = c + rb * math.cos(a), c + rb * math.sin(a)
            bd.ellipse([x - br, y - br, x + br, y + br], fill=255)
        img.alpha_composite(metal(beads, GOLD_SYM, sheen=2, phase=0.9, vgrad=0.3, bevel=S * 0.003, strength=1.0))
    # embossed symbol
    sm = Image.new("L", (S, S), 0)
    ImageDraw.Draw(sm).text((c, c + S * 0.012), symbol, font=F(S * (0.50 if detail else 0.60), "Black"), fill=255, anchor="mm")
    sh = Image.new("RGBA", (S, S), (60, 36, 4, 0))
    sh.putalpha(ImageChops.offset(sm.filter(ImageFilter.GaussianBlur(S * 0.01)), int(S * 0.01), int(S * 0.016)).point(lambda v: int(v * 0.8)))
    img.alpha_composite(sh)
    k = max(3, int(S * 0.012) | 1)
    ol = Image.new("RGBA", (S, S), (70, 42, 6, 0))
    ol.putalpha(sm.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.GaussianBlur(S * 0.002)).point(lambda v: int(v * 0.9)))
    img.alpha_composite(ol)
    img.alpha_composite(metal(sm, GOLD_SYM, sheen=2, phase=0.4, vgrad=0.45, bevel=S * 0.009, strength=1.25))
    return img

def mech_gear(S, teeth, stops, spokes=5, rot=0.0):
    c = S / 2
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    d.polygon(gear_polygon(c, c, 0.48 * S, 0.405 * S, teeth, 0.46, rot=rot), fill=255)
    rw = 0.31 * S
    d.ellipse([c - rw, c - rw, c + rw, c + rw], fill=0)
    for k in range(spokes):
        a = rot + 2 * math.pi * k / spokes
        d.line([(c, c), (c + 0.33 * S * math.cos(a), c + 0.33 * S * math.sin(a))], fill=255, width=int(0.075 * S))
    rh = 0.12 * S
    d.ellipse([c - rh, c - rh, c + rh, c + rh], fill=255)
    ra = 0.045 * S
    d.ellipse([c - ra, c - ra, c + ra, c + ra], fill=0)
    return metal(m, stops, sheen=2, phase=rot + 0.7, vgrad=0.3, bevel=S * 0.012, strength=1.0)

def plain_coin_face(S):
    """Top face of a stacked coin (seen from above, before squashing)."""
    c = S / 2
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).ellipse([0, 0, S - 1, S - 1], fill=255)
    img.alpha_composite(metal(m, GOLD, sheen=2, phase=0.9, vgrad=0.2, bevel=S * 0.02, strength=1.0))
    f = Image.new("L", (S, S), 0); r = 0.40 * S
    ImageDraw.Draw(f).ellipse([c - r, c - r, c + r, c + r], fill=255)
    img.alpha_composite(metal(f, GOLD_FACE, sheen=2, phase=2.5, bevel=S * 0.015, strength=-0.8))
    s = Image.new("L", (S, S), 0)
    ImageDraw.Draw(s).text((c, c + S * 0.02), "$", font=F(S * 0.55, "Black"), fill=255, anchor="mm")
    img.alpha_composite(metal(s, GOLD_SYM, sheen=2, phase=0.4, bevel=S * 0.012, strength=1.2))
    return img

def coin_stack(n, w, seed=0):
    """A stack of n gold coins, w px wide. Returns RGBA image and its height."""
    rng = np.random.default_rng(seed)
    fh = int(w * 0.34)                 # squashed face height
    th = int(w * 0.11)                 # coin thickness
    H = fh + th * n + 10
    img = Image.new("RGBA", (w + 40, H), (0, 0, 0, 0))
    face = plain_coin_face(w * 2).resize((w, fh), Image.LANCZOS)
    for i in range(n):
        dx = int(rng.normal(0, w * 0.025)) + 20
        y = H - fh - th - i * th
        edge = Image.new("L", (w + 40, H), 0)
        ed = ImageDraw.Draw(edge)
        ed.rectangle([dx, y + fh / 2, dx + w, y + fh / 2 + th], fill=255)
        ed.ellipse([dx, y + th, dx + w, y + th + fh], fill=255)
        # side of the coin: darker gold with ridges
        side = Image.new("RGBA", (w + 40, H), (0, 0, 0, 0))
        sd = np.zeros((H, w + 40, 4), np.uint8)
        xs = np.arange(w + 40)
        tone = 0.55 + 0.45 * np.cos((xs - dx - w * 0.35) / w * math.pi * 1.2)
        ridge = 0.85 + 0.15 * (np.sin(xs * 1.3) > 0)
        col = np.array([200, 140, 34]) * np.clip(tone * ridge, 0.25, 1.2)[:, None]
        sd[..., :3] = np.clip(col, 0, 255)[None, :, :]
        sd[..., 3] = np.asarray(edge)
        img.alpha_composite(Image.fromarray(sd, "RGBA"))
        img.alpha_composite(face, (dx, y))
    return img

# ---------------------------------------------------------------- assets
def profile(out, size=800):
    S = size * 3
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
    g = np.exp(-(((xx - 0.42) / 0.5) ** 2 + ((yy - 0.36) / 0.5) ** 2))[..., None]
    bg = np.array([2, 26, 20]) + g * np.array([16, 96, 68])
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
    coin = coin_gear(int(S * 0.88))
    off = int((S - coin.width) / 2)
    glow = Image.new("RGBA", (S, S), (250, 204, 21, 0))
    ga = Image.new("L", (S, S), 0); ga.paste(coin.split()[3], (off, off))
    glow.putalpha(ga.filter(ImageFilter.GaussianBlur(S * 0.05)).point(lambda v: int(v * 0.45)))
    img.alpha_composite(glow)
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sa = Image.new("L", (S, S), 0)
    sa.paste(coin.split()[3], (off, off + int(S * 0.02)))
    sh.putalpha(sa.filter(ImageFilter.GaussianBlur(S * 0.025)).point(lambda v: int(v * 0.6)))
    img.alpha_composite(sh)
    img.alpha_composite(coin, (off, off))
    img = img.resize((size, size), Image.LANCZOS)
    img.convert("RGB").save(os.path.join(out, "profile_800.png"))
    return img

def watermark(out, size=150):
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    coin = coin_gear(int(S * 0.9), detail=False)
    off = (S - coin.width) // 2
    sa = Image.new("L", (S, S), 0); sa.paste(coin.split()[3], (off, off + int(S * 0.02)))
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sh.putalpha(sa.filter(ImageFilter.GaussianBlur(S * 0.02)).point(lambda v: int(v * 0.7)))
    img.alpha_composite(sh); img.alpha_composite(coin, (off, off))
    img.resize((size, size), Image.LANCZOS).save(os.path.join(out, "watermark_150.png"))

def paste_rot(canvas, im, center, angle=0.0, scale_y=1.0, blur=0.0, alpha=1.0):
    if scale_y != 1.0:
        im = im.resize((im.width, max(1, int(im.height * scale_y))), Image.LANCZOS)
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1:
        a = im.split()[3].point(lambda v: int(v * alpha)); im.putalpha(a)
    canvas.alpha_composite(im, (int(center[0] - im.width / 2), int(center[1] - im.height / 2)))

def drop_shadow(canvas, im, center, blur, dy, alpha=0.55):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a)
    canvas.alpha_composite(sh, (int(center[0] - im.width / 2), int(center[1] - im.height / 2 + dy)))

def banner(name, out, tagline="Learn how money really works.", chips=("NEW SHORTS DAILY", "DEEP DIVES 3× A WEEK")):
    W, H = 2560, 1440
    SX0, SY0, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423
    cy = SY0 + SH / 2
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    xn, yn = xx / W, yy / H
    base = np.array(NAVY0, np.float32) + (np.array(NAVY1) - np.array(NAVY0)) * (0.6 + 0.4 * np.sin(yn * math.pi))[..., None]
    em = np.exp(-(((xn - 0.18) / 0.22) ** 2 + ((yn - 0.52) / 0.22) ** 2))[..., None] * np.array([10, 70, 52])
    go = np.exp(-(((xn - 0.86) / 0.18) ** 2 + ((yn - 0.48) / 0.22) ** 2))[..., None] * np.array([70, 50, 6])
    ce = np.exp(-(((xn - 0.5) / 0.32) ** 2 + ((yn - 0.5) / 0.16) ** 2))[..., None] * np.array([8, 22, 30])
    img = Image.fromarray(np.clip(base + em + go + ce, 0, 255).astype(np.uint8)).convert("RGBA")

    # perspective-free fine grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
    for x in range(0, W, 80):
        gd.line([(x, 0), (x, H)], fill=(40, 60, 90, 38), width=1)
    for y in range(0, H, 80):
        gd.line([(0, y), (W, y)], fill=(40, 60, 90, 38), width=1)
    img.alpha_composite(grid)

    # background candlesticks (uptrend), soft
    rng = np.random.default_rng(11)
    candles = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(candles)
    price = 0.0; n = 64
    for i in range(n):
        x = 30 + i * (W - 60) / n
        o = price; price += rng.normal(0.9, 2.2); cl = price
        hi_, lo_ = max(o, cl) + abs(rng.normal(0, 1.2)), min(o, cl) - abs(rng.normal(0, 1.2))
        Y = lambda p: SY0 + SH - 30 - (p + 6) * 4.2
        up = cl >= o
        colr = (34, 197, 94, 70) if up else (248, 113, 113, 55)
        cd.line([(x + 9, Y(hi_)), (x + 9, Y(lo_))], fill=colr, width=3)
        cd.rectangle([x, Y(max(o, cl)), x + 18, Y(min(o, cl)) + 2], fill=colr)
    # fade candles out behind the text block
    fade = Image.fromarray((255 * np.clip(np.abs(xn - 0.5) / 0.30, 0.15, 1.0) ** 1.5).astype(np.uint8))
    ca = ImageChops.multiply(candles.split()[3], fade); candles.putalpha(ca)
    img.alpha_composite(candles.filter(ImageFilter.GaussianBlur(1.2)))

    # glowing growth arrow sweeping across, behind everything
    pts = []
    for i in range(41):
        u = i / 40
        x = -40 + u * (W - 140)
        y = SY0 + SH + 40 - (u ** 1.8) * (SH + 30) + 22 * math.sin(u * 13) * (1 - u)
        pts.append((x, y))
    line = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(line)
    for a_, b_ in zip(pts, pts[1:]):
        u = a_[0] / W
        colr = tuple(int(v) for v in np.array([34, 197, 94]) * (1 - u) + np.array([250, 204, 21]) * u)
        ld.line([a_, b_], fill=colr + (255,), width=12)
    tip = (W - 70, pts[-1][1] - 48)
    ang = math.atan2(tip[1] - pts[-1][1], tip[0] - pts[-1][0])
    hl = 70
    ld.line([pts[-1], tip], fill=(250, 204, 21, 255), width=12)
    ld.polygon([(tip[0] + 18 * math.cos(ang), tip[1] + 18 * math.sin(ang)),
                (tip[0] - hl * math.cos(ang - 0.45), tip[1] - hl * math.sin(ang - 0.45)),
                (tip[0] - hl * math.cos(ang + 0.45), tip[1] - hl * math.sin(ang + 0.45))], fill=(250, 204, 21, 255))
    u2 = np.clip((np.abs(xn - 0.5) - 0.27) / 0.09, 0, 1)
    fade2 = Image.fromarray((255 * np.maximum(0.04, u2 * u2 * (3 - 2 * u2))).astype(np.uint8))
    la = ImageChops.multiply(line.split()[3], fade2); line.putalpha(la)
    glow = line.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(glow); img.alpha_composite(glow); img.alpha_composite(line)

    # bokeh
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bok)
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(SY0 - 120, SY0 + SH + 120)
        if SX0 + 200 < x < SX0 + SW - 200:
            continue
        r = rng.uniform(4, 22)
        colr = (250, 204, 21) if rng.random() < 0.55 else (52, 211, 153)
        bd.ellipse([x - r, y - r, x + r, y + r], fill=colr + (int(rng.uniform(25, 90)),))
    img.alpha_composite(bok.filter(ImageFilter.GaussianBlur(5)))

    # ---- right side: the money machine (gears meshing with the gold coin-gear)
    gold_c, gold_d = (2335, cy - 25), 440
    big = coin_gear(gold_d * 2, teeth=12).resize((gold_d, gold_d), Image.LANCZOS)
    em_d = 300
    em_pitch = (0.48 + 0.405) / 2 * em_d + (0.48 + 0.43) / 2 * gold_d - 12
    a = math.radians(142)
    em_c = (gold_c[0] + em_pitch * math.cos(a), gold_c[1] + em_pitch * math.sin(a))
    emg = mech_gear(em_d * 2, 10, EMERALD, rot=0.3).resize((em_d, em_d), Image.LANCZOS)
    sv_d = 180
    sv_pitch = (0.48 + 0.405) / 2 * sv_d + (0.48 + 0.43) / 2 * gold_d - 8
    a2 = math.radians(218)
    sv_c = (gold_c[0] + sv_pitch * math.cos(a2), gold_c[1] + sv_pitch * math.sin(a2))
    svg = mech_gear(sv_d * 2, 8, SILVER, spokes=4, rot=0.2).resize((sv_d, sv_d), Image.LANCZOS)
    for g_, c_ in ((emg, em_c), (svg, sv_c), (big, gold_c)):
        drop_shadow(img, g_, c_, 16, 18, 0.6)
    img.alpha_composite(emg, (int(em_c[0] - em_d / 2), int(em_c[1] - em_d / 2)))
    img.alpha_composite(svg, (int(sv_c[0] - sv_d / 2), int(sv_c[1] - sv_d / 2)))
    halo = Image.new("RGBA", (W, H), (250, 204, 21, 0)); ha = Image.new("L", (W, H), 0)
    ha.paste(big.split()[3], (int(gold_c[0] - gold_d / 2), int(gold_c[1] - gold_d / 2)))
    halo.putalpha(ha.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.35)))
    img.alpha_composite(halo)
    img.alpha_composite(big, (int(gold_c[0] - gold_d / 2), int(gold_c[1] - gold_d / 2)))

    # ---- left side: coin stacks + emerald gear peeking in + flying coins
    lg_d = 420
    lg = mech_gear(lg_d * 2, 12, EMERALD, spokes=6, rot=0.1).resize((lg_d, lg_d), Image.LANCZOS)
    drop_shadow(img, lg, (40, cy - 70), 16, 16)
    paste_rot(img, lg, (40, cy - 70), alpha=0.95)
    for (n, w, x, base, seed) in ((9, 210, 300, SY0 + SH + 40, 1), (6, 170, 470, SY0 + SH + 60, 2), (4, 150, 150, SY0 + SH + 70, 3)):
        st = coin_stack(n, w, seed)
        drop_shadow(img, st, (x, base - st.height / 2), 14, 12, 0.6)
        img.alpha_composite(st, (int(x - st.width / 2), int(base - st.height)))
    fc = coin_gear(360, teeth=12, detail=False)
    paste_rot(img, fc.resize((150, 150), Image.LANCZOS), (420, SY0 + 40), angle=18, scale_y=0.8)
    paste_rot(img, fc.resize((96, 96), Image.LANCZOS), (165, SY0 + 70), angle=-25, scale_y=0.7, blur=1.5)
    paste_rot(img, fc.resize((80, 80), Image.LANCZOS), (2080, SY0 + SH + 10), angle=30, scale_y=0.75, blur=2.0, alpha=0.9)

    # sparkles on the gold
    sp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); spd = ImageDraw.Draw(sp)
    for (x, y, r) in ((gold_c[0] - 120, gold_c[1] - 150, 34), (420 + 40, SY0 + 15, 22), (300 - 70, SY0 + SH - 170, 20), (2470, SY0 + 70, 26)):
        spd.polygon(star_polygon(x, y, r, 4, 0.18, 0), fill=(255, 250, 225, 235))
    img.alpha_composite(sp.filter(ImageFilter.GaussianBlur(5))); img.alpha_composite(sp)

    # ---- centre text block (inside the safe area)
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).ellipse([SX0 + 120, SY0 - 30, SX0 + SW - 120, SY0 + SH + 30], fill=170)
    dark = Image.new("RGBA", (W, H), NAVY0 + (0,)); dark.putalpha(shade.filter(ImageFilter.GaussianBlur(90)))
    img.alpha_composite(dark)

    words = name.upper().split(" ", 1)
    first, second = words[0] + " ", (words[1] if len(words) > 1 else "")
    size = 176
    while True:
        fnt = F(size, "Black")
        wtot = fnt.getlength(first) + fnt.getlength(second)
        if wtot <= SW - 230 or size < 90:
            break
        size -= 4
    x0 = W / 2 - wtot / 2
    cap = fnt.getbbox("M")[3] - fnt.getbbox("M")[1]
    block = cap + 92 + 62 + 76            # title cap height + tagline + chips
    name_y = SY0 + (SH - block) / 2 + cap
    tmask1 = Image.new("L", (W, H), 0); ImageDraw.Draw(tmask1).text((x0, name_y), first, font=fnt, fill=255, anchor="ls")
    x1 = x0 + fnt.getlength(first)
    tmask2 = Image.new("L", (W, H), 0); ImageDraw.Draw(tmask2).text((x1, name_y), second, font=fnt, fill=255, anchor="ls")
    both = ImageChops.lighter(tmask1, tmask2)
    tsh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tsh.putalpha(ImageChops.offset(both, 0, 10).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.85)))
    img.alpha_composite(tsh)
    asc = fnt.getbbox("M")
    bbox = (0, name_y + asc[1] - asc[3], W, name_y)
    white = metal_text(tmask1, [(0, (255, 255, 255)), (0.6, (236, 241, 247)), (1, (196, 207, 222))], bbox, bevel=3, strength=0.5)
    gold = metal_text(tmask2, GOLD_TEXT, bbox, bevel=4, strength=0.9)
    img.alpha_composite(white); img.alpha_composite(gold)

    # tagline
    tf = F(64, "SemiBold", False)
    d = ImageDraw.Draw(img)
    tag_y = name_y + 92
    parts = tagline.split("really")
    if len(parts) == 2:
        segs = [(parts[0], (226, 232, 240)), ("really", (52, 211, 153)), (parts[1], (226, 232, 240))]
    else:
        segs = [(tagline, (226, 232, 240))]
    tw = sum(tf.getlength(s) for s, _ in segs)
    x = W / 2 - tw / 2
    for s, colr in segs:
        d.text((x, tag_y), s, font=tf, fill=colr + (255,), anchor="lm"); x += tf.getlength(s)

    # chips
    cf = F(40, "Bold")
    chip_y0, chip_h = tag_y + 62, 76
    widths = [cf.getlength(c_) + 120 for c_ in chips]
    gap = 28
    x = W / 2 - (sum(widths) + gap * (len(chips) - 1)) / 2
    chip_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cl = ImageDraw.Draw(chip_layer)
    for i, (c_, wd) in enumerate(zip(chips, widths)):
        accent = (52, 211, 153) if i == 0 else (250, 204, 21)
        cl.rounded_rectangle([x, chip_y0, x + wd, chip_y0 + chip_h], chip_h // 2, fill=(9, 18, 34, 215), outline=accent + (255,), width=4)
        ix, iy = x + 48, chip_y0 + chip_h / 2
        if i == 0:
            cl.polygon([(ix - 13, iy - 16), (ix - 13, iy + 16), (ix + 16, iy)], fill=accent + (255,))
        else:
            cl.rounded_rectangle([ix - 16, iy - 15, ix + 16, iy + 17], 5, outline=accent + (255,), width=4)
            cl.line([(ix - 16, iy - 5), (ix + 16, iy - 5)], fill=accent + (255,), width=4)
            cl.line([(ix - 7, iy - 22), (ix - 7, iy - 10)], fill=accent + (255,), width=4)
            cl.line([(ix + 7, iy - 22), (ix + 7, iy - 10)], fill=accent + (255,), width=4)
        cl.text((x + 82, iy + 1), c_, font=cf, fill=(241, 245, 249, 255), anchor="lm")
        x += wd + gap
    img.alpha_composite(chip_layer)

    # gentle vignette
    vig = np.clip(1 - 0.55 * (((xn - 0.5) / 0.75) ** 2 + ((yn - 0.5) / 0.62) ** 2), 0.45, 1)
    arr = np.asarray(img.convert("RGB"), np.float32) * vig[..., None]
    final = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    final.save(os.path.join(out, "banner_2560x1440.png"), optimize=True)
    return final, (SX0, SY0, SW, SH)

def page_preview(out, banner_img, safe, prof, name, handle, tagline):
    """Rough channel-page mock-up (desktop + phone) to judge the look. Not for upload."""
    SX0, SY0, SW, SH = safe
    P = Image.new("RGB", (1500, 1080), (15, 15, 15)); d = ImageDraw.Draw(P)
    desk = banner_img.crop((0, SY0, 2560, SY0 + SH)).resize((1400, int(1400 * SH / 2560)), Image.LANCZOS)
    P.paste(desk, (50, 40))
    av = prof.resize((150, 150), Image.LANCZOS)
    m = Image.new("L", (150, 150), 0); ImageDraw.Draw(m).ellipse([0, 0, 149, 149], fill=255)
    P.paste(av, (50, 40 + desk.height + 30), m)
    tx = 230; ty = 40 + desk.height + 45
    d.text((tx, ty), name, font=F(46, "Bold"), fill=(241, 241, 241))
    d.text((tx, ty + 62), f"{handle} · {tagline}", font=F(24, "Medium", False), fill=(170, 170, 170))
    d.rounded_rectangle([tx, ty + 104, tx + 170, ty + 150], 23, fill=(241, 241, 241))
    d.text((tx + 85, ty + 127), "Subscribe", font=F(24, "SemiBold", False), fill=(15, 15, 15), anchor="mm")
    # phone
    ph = banner_img.crop((SX0, SY0, SX0 + SW, SY0 + SH)).resize((390, int(390 * SH / SW)), Image.LANCZOS)
    px, py = 1050, 470
    d.rounded_rectangle([px - 20, py - 30, px + 410, py + 560], 40, outline=(80, 80, 80), width=4, fill=(10, 10, 10))
    P.paste(ph, (px, py))
    av2 = prof.resize((96, 96), Image.LANCZOS); m2 = Image.new("L", (96, 96), 0); ImageDraw.Draw(m2).ellipse([0, 0, 95, 95], fill=255)
    P.paste(av2, (px + 147, py + ph.height + 20), m2)
    d.text((px + 195, py + ph.height + 135), name, font=F(30, "Bold"), fill=(241, 241, 241), anchor="mm")
    d.text((px + 195, py + ph.height + 175), handle, font=F(20, "Medium", False), fill=(170, 170, 170), anchor="mm")
    # small avatars as seen next to videos
    d.text((50, 980), "Avatar next to videos / comments:", font=F(22, "Medium", False), fill=(170, 170, 170))
    x = 440
    for sz in (64, 40, 28):
        a = prof.resize((sz, sz), Image.LANCZOS); mm = Image.new("L", (sz, sz), 0); ImageDraw.Draw(mm).ellipse([0, 0, sz - 1, sz - 1], fill=255)
        P.paste(a, (x, 992 - sz // 2), mm); x += sz + 30
    P.save(os.path.join(out, "channel_page_preview.png"))

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    prof = profile(out)
    watermark(out)
    b, safe = banner(name, out)
    handle = "@" + name.replace(" ", "")
    page_preview(out, b, safe, prof, name, handle, "Learn how money really works")
    # safe-area check image (for review only)
    chk = b.copy(); ImageDraw.Draw(chk).rectangle([safe[0], safe[1], safe[0] + safe[2], safe[1] + safe[3]], outline=(255, 60, 60), width=6)
    chk.resize((1280, 720)).save(os.path.join(out, "_safe_check.png"))
    print("done")
