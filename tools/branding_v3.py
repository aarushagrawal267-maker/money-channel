"""Channel branding v3: simple, flat, modern.

Logo: flat gold gear-coin with a bold navy "$" (Money + Mechanics), two colours only.
Banner: solid navy, logo + name + tagline + schedule, faint gear outlines at the edges.

Usage: python3 branding_v3.py "Money Mechanics" out_dir
Banner is 2560x1440; everything important sits in the centre 1546x423 (shown on every device).
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/opentype/inter/"
def F(size, w="Black", display=True):
    return ImageFont.truetype(FD + ("InterDisplay-" if display else "Inter-") + w + ".otf", int(size))

NAVY = (11, 18, 32)
GOLD = (250, 204, 21)
GREEN = (34, 197, 94)
WHITE = (248, 250, 252)
GRAY = (203, 213, 225)

def gear_polygon(cx, cy, r_out, r_root, teeth, frac=0.5, steps=12, rot=0.0):
    pts, span = [], 2 * math.pi / teeth
    for i in range(teeth):
        a0 = rot + span * i
        t0, t1 = a0 + span * (0.5 - frac / 2), a0 + span * (0.5 + frac / 2)
        for k in range(steps):
            a = a0 + (t0 - a0) * k / steps
            pts.append((cx + r_root * math.cos(a), cy + r_root * math.sin(a)))
        tp = span * 0.07
        pts += [(cx + r_out * math.cos(t0 + tp), cy + r_out * math.sin(t0 + tp)),
                (cx + r_out * math.cos(t1 - tp), cy + r_out * math.sin(t1 - tp))]
        for k in range(steps + 1):
            a = t1 + (a0 + span - t1) * k / steps
            pts.append((cx + r_root * math.cos(a), cy + r_root * math.sin(a)))
    return pts

def logo(size, bg=None, scale=0.84):
    """Flat gear-coin. Drawn at 4x and downsampled for smooth edges."""
    T = size * 4
    img = Image.new("RGBA", (T, T), (bg + (255,)) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, R = T / 2, T * scale / 2
    d.polygon(gear_polygon(c, c, R, R * 0.86, 10, 0.5, rot=-math.pi / 2 + math.pi / 10), fill=GOLD)
    rr = R * 0.70
    d.ellipse([c - rr, c - rr, c + rr, c + rr], outline=NAVY, width=int(R * 0.055))
    d.text((c, c + R * 0.03), "$", font=F(R * 0.95, "Black"), fill=NAVY, anchor="mm")
    return img.resize((size, size), Image.LANCZOS)

def outline_gear(d, cx, cy, r, color, width, teeth=12, rot=0.0):
    """Gear outline with an even stroke: filled gear, then a smaller gear cut out of it."""
    d.polygon(gear_polygon(cx, cy, r, r * 0.86, teeth, 0.5, rot=rot), fill=color)
    d.polygon(gear_polygon(cx, cy, r - width, r * 0.86 - width, teeth, 0.5 - 0.02, rot=rot), fill=NAVY + (255,))
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], outline=color, width=width)

def banner(name, out, tagline="Learn how money really works.",
           schedule="NEW SHORTS DAILY  ·  DEEP DIVES 3× A WEEK"):
    W, H = 2560, 1440
    SX0, SY0, SW, SH = (W - 1546) // 2, (H - 423) // 2, 1546, 423
    S = 2  # draw at 2x for smooth edges
    img = Image.new("RGBA", (W * S, H * S), NAVY + (255,))
    d = ImageDraw.Draw(img)
    # faint gear outlines at the edges (seen on desktop / TV, not crowding the text)
    outline_gear(d, (W - 60) * S, (H / 2 + 40) * S, 330 * S, (250, 204, 21, 255), 7 * S, 12, 0.1)
    outline_gear(d, 70 * S, (H / 2 - 30) * S, 250 * S, (34, 197, 94, 255), 7 * S, 10, 0.3)
    img = img.resize((W, H), Image.LANCZOS)
    # fade the outlines so they stay quiet
    quiet = Image.new("RGBA", (W, H), NAVY + (255,))
    img = Image.blend(quiet, img, 0.22)
    d = ImageDraw.Draw(img)

    # layout: [logo]  NAME / tagline / schedule, centred in the safe area
    logo_px = 280
    gap = 60
    margin = 90
    size = 150
    while True:
        nf = F(size, "Black")
        first, second = name.upper().split(" ", 1) if " " in name else (name.upper(), "")
        first += " "
        name_w = nf.getlength(first) + nf.getlength(second)
        if logo_px + gap + name_w <= SW - 2 * margin or size <= 80:
            break
        size -= 2
    tf = F(int(size * 0.46), "SemiBold", False)
    sf = F(int(size * 0.31), "Bold")
    total_w = logo_px + gap + name_w
    x0 = W / 2 - total_w / 2
    cy = H / 2
    cap = nf.getbbox("M")[3] - nf.getbbox("M")[1]
    g1, g2 = int(size * 0.42), int(size * 0.34)
    tag_h = tf.getbbox("Lg")[3] - tf.getbbox("Lg")[1]
    sch_h = sf.getbbox("N")[3] - sf.getbbox("N")[1]
    block = cap + g1 + tag_h + g2 + sch_h
    top = cy - block / 2
    lg = logo(logo_px)
    img.alpha_composite(lg, (int(x0), int(cy - logo_px / 2)))
    tx = x0 + logo_px + gap
    base = top + cap
    d.text((tx, base), first, font=nf, fill=WHITE, anchor="ls")
    d.text((tx + nf.getlength(first), base), second, font=nf, fill=GOLD, anchor="ls")
    d.text((tx + 4, base + g1), tagline, font=tf, fill=GRAY, anchor="lt")
    d.text((tx + 4, base + g1 + tag_h + g2), schedule, font=sf, fill=GREEN, anchor="lt")
    img.convert("RGB").save(os.path.join(out, "banner_2560x1440.png"), optimize=True)
    return img.convert("RGB"), (SX0, SY0, SW, SH)

def preview(out, b, safe, prof, name):
    SX0, SY0, SW, SH = safe
    P = Image.new("RGB", (1500, 760), (15, 15, 15)); d = ImageDraw.Draw(P)
    desk = b.crop((0, SY0, 2560, SY0 + SH)).resize((1400, int(1400 * SH / 2560)), Image.LANCZOS)
    P.paste(desk, (50, 40))
    av = prof.resize((150, 150), Image.LANCZOS); m = Image.new("L", (150, 150), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 149, 149], fill=255)
    y = 40 + desk.height + 30
    P.paste(av, (50, y), m)
    d.text((230, y + 15), name, font=F(46, "Bold"), fill=(241, 241, 241))
    d.text((230, y + 77), "@" + name.replace(" ", "") + " · Learn how money really works", font=F(24, "Medium", False), fill=(170, 170, 170))
    ph = b.crop((SX0, SY0, SX0 + SW, SY0 + SH)).resize((390, int(390 * SH / SW)), Image.LANCZOS)
    P.paste(ph, (50, 520))
    d.text((50, 490), "On a phone:", font=F(22, "Medium", False), fill=(170, 170, 170))
    d.text((520, 490), "Avatar next to videos / comments:", font=F(22, "Medium", False), fill=(170, 170, 170))
    x = 520
    for sz in (64, 40, 28):
        a = prof.resize((sz, sz), Image.LANCZOS); mm = Image.new("L", (sz, sz), 0)
        ImageDraw.Draw(mm).ellipse([0, 0, sz - 1, sz - 1], fill=255)
        P.paste(a, (x, 560 - sz // 2), mm); x += sz + 30
    P.save(os.path.join(out, "channel_page_preview.png"))

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    prof = logo(800, bg=NAVY)
    prof.convert("RGB").save(os.path.join(out, "profile_800.png"))
    logo(150, scale=0.96).save(os.path.join(out, "watermark_150.png"))
    b, safe = banner(name, out)
    preview(out, b, safe, prof, name)
    print("done")
