"""Render a finance Short (1080x1920) from a JSON spec.

Usage: python3 render.py spec.json out_dir

Spec: {"id", "voice", "speed", "badge", "disclaimer",
       "scenes": [{"say": "...", "visual": {"type": ..., ...}}]}
Visual types: pair, compare, timeline, stat, bars, equation, line, cta, photo.
"""
import json, math, os, subprocess, sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 24000
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")
FONT_DIR = "/usr/share/fonts/opentype/inter/"

COLORS = {
    "bg0": (8, 13, 26), "bg1": (17, 27, 48), "text": (241, 245, 249),
    "muted": (148, 163, 184), "dim": (71, 85, 105), "green": (34, 197, 94),
    "gold": (250, 204, 21), "red": (248, 113, 113), "blue": (96, 165, 250),
    "slate": (148, 163, 184), "grid": (30, 41, 64),
}
CX = 540            # horizontal centre
TITLE_Y = 430       # scene title baseline area
VIS_TOP, VIS_BOT = 520, 1160
ZOOM, ZOOM_CY = 0.035, 840   # slow push-in on held visuals, centred on the visual area
CAP_Y = 1370        # captions centre (clear of the Shorts title/description overlay)
VIS_SHIFT = 70      # push visuals down to use the screen better

_fonts = {}
def font(size, weight="Bold", display=True):
    key = (size, weight, display)
    if key not in _fonts:
        name = ("InterDisplay-" if display else "Inter-") + weight + ".otf"
        _fonts[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _fonts[key]

def col(c, a=1.0):
    rgb = COLORS.get(c, c) if isinstance(c, str) else c
    return tuple(rgb) + (int(255 * max(0, min(1, a))),)

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def fmt_inr(v):
    if v >= 1e7:
        s = f"{v/1e7:,.2f}".rstrip("0").rstrip(".")
        return f"₹{s} Cr"
    if v >= 1e5:
        l = v / 1e5
        s = f"{l:.0f}" if l >= 10 else f"{l:.1f}".rstrip("0").rstrip(".")
        return f"₹{s} L"
    return "₹" + f"{v:,.0f}"

def fmt_usd(v):
    if v >= 1e9:
        return "$" + f"{v/1e9:.1f}".rstrip("0").rstrip(".") + "B"
    if v >= 1e6:
        return "$" + f"{v/1e6:.2f}".rstrip("0").rstrip(".") + "M"
    if v >= 1e5:
        return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"

DEFAULT_FMT = "usd"

def fmt(v, kind=None):
    kind = kind or DEFAULT_FMT
    if kind == "inr":
        return fmt_inr(v)
    if kind == "usd":
        return fmt_usd(v)
    return f"{v:,.0f}" if kind == "num" else str(v)

def nice_ticks(vmax, n=5):
    """Round axis steps (1/2/2.5/5 x 10^k) so labels read $100K, $200K... Returns tick values."""
    raw = vmax / n
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return [step * i for i in range(1, math.ceil(vmax / step - 1e-9) + 1)]

# ---------------------------------------------------------------- drawing utils
def text_c(d, xy, s, f, fill, anchor="mm", stroke=0, stroke_fill=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke,
           stroke_fill=stroke_fill)

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def make_background():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    b0, b1 = np.array(COLORS["bg0"]), np.array(COLORS["bg1"])
    base = b0 + (b1 - b0) * (0.6 * y + 0.0 * x)[..., None]
    glow = np.exp(-(((x - 0.5) / 0.55) ** 2 + ((y - 0.38) / 0.25) ** 2))[..., None]
    base = base + glow * np.array([20, 40, 40])
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 90):
        d.line([(gx, 0), (gx, H)], fill=col("grid", 0.35), width=1)
    for gy in range(0, H, 90):
        d.line([(0, gy), (W, gy)], fill=col("grid", 0.35), width=1)
    return img

# ---------------------------------------------------------------- scene visuals
def scene_title(d, title, t):
    if not title:
        return
    a = ease(t / 0.4)
    text_c(d, (CX, TITLE_Y + 20 * (1 - a)), title, font(54, "Bold"), col("text", a))

def v_pair(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    for i, side in enumerate((v["left"], v["right"])):
        a = ease((t - 0.15 * i) / 0.5)
        x = CX + (-215 if i == 0 else 215)
        y = 800 + 40 * (1 - a)
        c = side.get("color", "green")
        d.ellipse([x - 120, y - 200, x + 120, y + 40], fill=col(c, 0.18 * a),
                  outline=col(c, a), width=6)
        text_c(d, (x, y - 80), side["label"][0], font(130, "Black"), col(c, a))
        text_c(d, (x, y + 110), side["label"], font(58, "Bold"), col("text", a))
        text_c(d, (x, y + 180), side.get("sub", ""), font(40, "Medium", False), col("muted", a))

def v_compare(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    kind = v.get("format")
    for i, side in enumerate((v["left"], v["right"])):
        a = ease((t - 0.1 * i) / 0.4)
        k = ease((t - 0.1 * i) / 1.4)
        y = 680 + i * 280
        c = side.get("color", "green")
        rrect(d, [150, y - 110, 930, y + 110], 36, fill=col(c, 0.12 * a), outline=col(c, 0.8 * a), width=4)
        text_c(d, (200, y), side["label"], font(48, "SemiBold"), col("muted", a), anchor="lm")
        text_c(d, (880, y), fmt(side["value"] * k, kind) if k < 0.999 else fmt(side["value"], kind),
               font(96, "Black"), col(c, a), anchor="rm")

def v_timeline(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    s, e = v["start"], v["end"]
    x0, x1 = 170, 910
    X = lambda age: x0 + (age - s) / (e - s) * (x1 - x0)
    a = ease(t / 0.4)
    ay = 1080
    d.line([(x0, ay), (x1, ay)], fill=col("muted", a), width=4)
    for age in range(s, e + 1, 5):
        d.line([(X(age), ay - 12), (X(age), ay + 12)], fill=col("muted", a), width=3)
        text_c(d, (X(age), ay + 50), str(age), font(36, "Medium", False), col("muted", a))
    for i, row in enumerate(v["rows"]):
        y = 700 + i * 190
        c = row.get("color", "green")
        p = ease((t - 0.3 - 0.5 * i) / 1.2)
        xa, xb = X(row["from"]), X(row["from"]) + (X(e) - X(row["from"])) * p
        text_c(d, (x0, y - 62), row["label"], font(46, "Bold"), col("text", a), anchor="lm")
        rrect(d, [x0, y - 26, x1, y + 26], 26, fill=col("grid", 0.8 * a))
        if p > 0.01:
            rrect(d, [xa, y - 26, max(xa + 52, xb), y + 26], 26, fill=col(c, a))
            text_c(d, (xa + 20, y), f"starts at {row['from']}", font(30, "Bold", False),
                   col("bg0", min(1, p * 3)), anchor="lm")

def v_stat(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    a = ease(t / 0.5)
    sc = 0.85 + 0.15 * a
    text_c(d, (CX, 800), v["value"], font(int(240 * sc), "Black"), col(v.get("color", "gold"), a))
    text_c(d, (CX, 990), v.get("label", ""), font(44, "SemiBold", False), col("text", a))
    if v.get("sub"):
        text_c(d, (CX, 1060), v["sub"], font(34, "Medium", False), col("muted", a))

def v_bars(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    kind = v.get("format")
    items = v["items"]
    mx = max(i["value"] for i in items)
    base, top = 1110, 640
    n = len(items)
    bw = 230
    gap = (W - 2 * 180 - n * bw) / max(1, n - 1)
    for k, it in enumerate(items):
        p = ease((t - 0.15 * k) / 1.0)
        x = 180 + k * (bw + gap)
        h = (base - top) * it["value"] / mx * p
        c = it.get("color", "green")
        if h > 2:
            rrect(d, [x, base - h, x + bw, base], 24, fill=col(c, 0.9))
        text_c(d, (x + bw / 2, base - h - 50), fmt(it["value"] * p, kind) if p < 0.999 else fmt(it["value"], kind),
               font(64, "Black"), col("text", min(1, p * 2)))
        text_c(d, (x + bw / 2, base + 50), it["label"], font(44, "Bold"), col("muted", min(1, p * 2)))

def v_equation(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    lines = v["lines"]
    y0 = 840 - (len(lines) - 1) * 85
    for i, ln in enumerate(lines):
        a = ease((t - 0.45 * i) / 0.45)
        size = ln.get("size", 88)
        text_c(d, (CX, y0 + i * 170 + 30 * (1 - a)), ln["text"], font(size, "Black"),
               col(ln.get("color", "text"), a))

def v_line(d, v, t, dur):
    scene_title(d, v.get("title"), t)
    xs = v["x"]
    series = v["series"]
    ticks = nice_ticks(max(max(s["values"]) for s in series))
    mx = ticks[-1] * 1.04
    L, R, T, B = 200, 900, 580, 1110
    X = lambda x: L + (x - xs[0]) / (xs[-1] - xs[0]) * (R - L)
    Y = lambda y: B - y / mx * (B - T)
    kind = v.get("format")
    # axes + gridlines
    for val in ticks:
        d.line([(L, Y(val)), (R, Y(val))], fill=col("grid", 1), width=2)
        text_c(d, (L - 16, Y(val)), fmt(val, kind), font(28, "Medium", False), col("muted"), anchor="rm")
    d.line([(L, B), (R, B)], fill=col("muted"), width=3)
    for x in xs[::5] if len(xs) > 12 else xs:
        text_c(d, (X(x), B + 36), str(x), font(30, "Medium", False), col("muted"))
    if v.get("x_label"):
        text_c(d, (R, B + 80), v["x_label"], font(28, "Medium", False), col("dim"), anchor="rm")
    # highlight band
    hl = v.get("highlight")
    if hl:
        a = ease(t / 0.5)
        d.rectangle([X(hl["from"]), T, X(hl["to"]), B], fill=col("gold", 0.12 * a))
        if hl.get("label"):
            text_c(d, (X(hl["from"]) - 16, T + 40), hl["label"],
                   font(44, "Black"), col("gold", a), anchor="rm")
    p = ease(t / max(0.8, min(2.5, dur * 0.6))) if v.get("reveal", True) else 1.0
    xmax = xs[0] + (xs[-1] - xs[0]) * p
    ends = [Y(s["values"][-1]) for s in series]
    use_legend = len(series) > 1 and min(abs(a - b) for i, a in enumerate(ends) for b in ends[i + 1:]) < 70
    if use_legend:
        lf = font(34, "Bold")
        widths = [lf.getlength(s["label"]) + 60 for s in series]
        lx = CX - (sum(widths) + 40 * (len(series) - 1)) / 2
        for s, wd in zip(series, widths):
            c = s.get("color", "green")
            d.ellipse([lx, T - 62, lx + 26, T - 36], fill=col(c))
            text_c(d, (lx + 40, T - 49), s["label"], lf, col(c), anchor="lm")
            lx += wd + 40
    for s in series:
        c = s.get("color", "green")
        pts = [(X(x), Y(y)) for x, y in zip(xs, s["values"]) if x <= xmax]
        # interpolate end point
        for j in range(len(xs) - 1):
            if xs[j] < xmax < xs[j + 1]:
                f = (xmax - xs[j]) / (xs[j + 1] - xs[j])
                pts.append((X(xmax), Y(s["values"][j] + f * (s["values"][j + 1] - s["values"][j]))))
        if len(pts) >= 2:
            d.line(pts, fill=col(c), width=9, joint="curve")
            ex, ey = pts[-1]
            d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=col(c))
            if p > 0.98 and not use_legend:
                text_c(d, (ex - 20, ey - 40), s["label"], font(36, "Bold"), col(c), anchor="rb")
    hline = v.get("hline")
    if hline:
        a = ease((t - hline.get("at", 0)) / 0.4)
        if a > 0:
            yy = Y(hline["value"])
            for xx in range(L, R, 28):
                d.line([(xx, yy), (xx + 14, yy)], fill=col("gold", a), width=4)
            text_c(d, (L + 10, yy - 14), hline["label"], font(32, "Bold"), col("gold", a), anchor="lb")
            if hline.get("x") is not None:
                hx = X(hline["x"])
                d.ellipse([hx - 18, yy - 18, hx + 18, yy + 18], outline=col("gold", a), width=5)

def v_cta(d, v, t, dur):
    lines = v["lines"]
    for i, ln in enumerate(lines):
        a = ease((t - 0.35 * i) / 0.45)
        text_c(d, (CX, 700 + i * 150 + 30 * (1 - a)), ln, font(110, "Black"),
               col("gold" if i == len(lines) - 1 else "text", a))
    if v.get("sub"):
        a = ease((t - 0.35 * len(lines)) / 0.45)
        rrect(d, [170, 1010, 910, 1110], 50, fill=col("green", 0.9 * a))
        text_c(d, (CX, 1060), v["sub"], font(40, "Bold"), col("bg0", a))


# ---------------------------------------------------------------- real photos (assets/photos, see tools/fetch_photo.py)
ROOT = os.path.normpath(os.path.join(HERE, ".."))
_photo_cache = {}

def load_photo(path):
    if path not in _photo_cache:
        _photo_cache[path] = Image.open(os.path.join(ROOT, path)).convert("RGB")
    return _photo_cache[path]

def photo_credit(path):
    try:
        return json.load(open(os.path.join(ROOT, os.path.splitext(path)[0] + ".json"))).get("short", "")
    except (FileNotFoundError, ValueError):
        return ""

def cover(im, w, h, focus=(0.5, 0.4), zoom=1.0):
    """Crop im to w:h around focus (fractions of width/height) and resize: like CSS object-fit: cover."""
    iw, ih = im.size
    if iw / ih > w / h:
        cw, ch = ih * w / h, ih
    else:
        cw, ch = iw, iw * h / w
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(focus[0] * iw - cw / 2, 0), iw - cw)
    y0 = min(max(focus[1] * ih - ch / 2, 0), ih - ch)
    return im.resize((int(w), int(h)), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))

def photo_tile(path, w, h, focus=(0.5, 0.4), r=36):
    key = (path, w, h, tuple(focus), r)
    if key not in _photo_cache:
        tile = cover(load_photo(path), w, h, focus).convert("RGBA")
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
        tile.putalpha(mask)
        _photo_cache[key] = tile
    return _photo_cache[key]

def paste_photo(d, path, box, a=1.0, focus=(0.5, 0.4), r=36, credit=True):
    """Paste a rounded photo into the image behind ImageDraw d, fading with a; small credit in the corner."""
    x0, y0, x1, y1 = [int(v) for v in box]
    tile = photo_tile(path, x1 - x0, y1 - y0, focus, r)
    if a < 0.999:
        tile = tile.copy()
        tile.putalpha(tile.getchannel("A").point(lambda p: int(p * a)))
    d._image.alpha_composite(tile, (x0, y0))
    d.rounded_rectangle([x0, y0, x1, y1], r, outline=col("text", 0.18 * a), width=3)
    if credit:
        c = photo_credit(path)
        if c:
            d.text((x1 - 16, y1 - 14), c, font=font(20, "Medium", False), fill=col("text", 0.85 * a),
                   anchor="rb", stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))

# ---------------------------------------------------------------- cutouts, glows, simple graphics
# Shared by the thumbnails (both renderers) and the long-video photo scenes.
def _edge_band(mask, px):
    """True where a pixel is inside mask but within ~px of its outline."""
    from scipy.ndimage import binary_erosion
    return mask & ~binary_erosion(mask, iterations=px)

def _clean_cutout(src, alpha):
    """Tidy a rembg matte: drop faint specks, key out backdrop-coloured pixels near the outline
    (red-carpet fringe in hair, etc.), pull the backdrop colour out of soft edge pixels."""
    rgb = np.asarray(src, np.float32)
    a = np.asarray(alpha, np.float32) / 255
    a[a < 0.1] = 0
    outside = a < 0.05
    if outside.mean() > 0.05:
        bg = np.median(rgb[outside], 0)
        spread = np.median(np.abs(rgb[outside] - bg).sum(1))
        if spread < 90:                                   # plain backdrop: safe to key its colour
            from scipy.ndimage import label
            dist = np.abs(rgb - bg).sum(-1)
            # backdrop-coloured patches the model kept: drop them if they connect to the outside
            # (and lie near the outline), so e.g. red lips inside the face are never touched
            like = (dist < 95) | outside
            lab, _ = label(like)
            border = np.zeros_like(outside); border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
            ids = np.unique(lab[outside | (border & like)]); ids = ids[ids > 0]
            drop = np.isin(lab, ids) & _edge_band(a > 0.05, 90)
            a = np.where(drop, 0, a)
            band = _edge_band(a > 0.05, 8)
            key = np.clip((dist - 60) / 110, 0, 1)
            a = np.where(band, np.minimum(a, key), a)
            soft = band & (a > 0.05)
            k = np.maximum(a, 0.35)[..., None]
            fixed = np.clip((rgb - (1 - k) * bg) / k, 0, 255)
            rgb = np.where(soft[..., None], fixed, rgb)
            # despill: remove the backdrop's tint from the outer ~10 px (e.g. red light on blonde hair)
            from scipy.ndimage import distance_transform_edt
            depth = distance_transform_edt(a > 0.05)
            wgt = np.clip(1 - depth / 10, 0, 1)[..., None] * 0.75
            lum = rgb.mean(-1, keepdims=True)
            bgc = bg - bg.mean(); bgc = bgc / (np.linalg.norm(bgc) + 1e-6)
            proj = np.clip(((rgb - lum) * bgc).sum(-1, keepdims=True), 0, None)
            rgb = np.clip(rgb - wgt * proj * bgc, 0, 255)
    from scipy.ndimage import label
    lab, n = label(a > 0.3)
    if n > 1:                                             # drop floating specks, keep the person
        sizes = np.bincount(lab.ravel()); sizes[0] = 0
        small = np.nonzero(sizes < sizes.max() * 0.01)[0]
        a = np.where(np.isin(lab, small[small > 0]), 0, a)
        a = np.where(a <= 0.3, a * 0.6, a)               # thin the faint halo left around them
    al = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
    out.putalpha(al)
    return out

def load_cutout(path):
    """The person in a photo with the background removed, cropped to them. Computed once with rembg
    (u2net_human_seg, ~2 s) and cached as assets/photos/<name>_cut.png; delete that file to redo it."""
    key = ("cut", path)
    if key not in _photo_cache:
        cp = os.path.join(ROOT, os.path.splitext(path)[0] + "_cut.png")
        if os.path.exists(cp):
            cut = Image.open(cp).convert("RGBA")
        else:
            from rembg import remove, new_session
            src = load_photo(path)
            cut = _clean_cutout(src, remove(src, session=new_session("u2net_human_seg")).getchannel("A"))
            cut.save(cp)
        _photo_cache[("alpha", path)] = cut.getchannel("A")
        box = cut.getchannel("A").point(lambda p: 255 if p > 30 else 0).getbbox() or (0, 0) + cut.size
        # sides where the photo itself crops the person (no outline should be drawn there)
        _photo_cache[("open", path)] = "".join(k for k, hit in zip("ltrb", (box[0] <= 2, box[1] <= 2,
                                               box[2] >= cut.width - 2, box[3] >= cut.height - 2)) if hit)
        _photo_cache[key] = cut.crop(box)
    return _photo_cache[key]

def cutout_alpha(path):
    """Full-size alpha matte of the person in the original photo (same size as load_photo(path))."""
    load_cutout(path)
    return _photo_cache[("alpha", path)]

def remove_person(path, size, focus=(0.5, 0.4), zoom=1.0, sigma=22):
    """The photo's own backdrop with the person painted out (blurred fill from around them): for depth
    behind a sharp cut-out, without a ghost of their face."""
    from scipy.ndimage import gaussian_filter, binary_dilation
    w, h = size
    rgb = np.asarray(cover(load_photo(path), w, h, focus, zoom), np.float32)
    a = np.asarray(cover(cutout_alpha(path).convert("RGB"), w, h, focus, zoom).getchannel("R"), np.float32) / 255
    keep = (~binary_dilation(a > 0.1, iterations=12)).astype(np.float32)
    num = np.stack([gaussian_filter(rgb[..., i] * keep, sigma) for i in range(3)], -1)
    den = gaussian_filter(keep, sigma)[..., None]
    fill = num / np.maximum(den, 1e-3)
    if den.max() < 0.02:
        fill[:] = rgb.reshape(-1, 3).mean(0)
    out = np.where(keep[..., None] > 0.5, rgb, fill)
    out = np.stack([gaussian_filter(out[..., i], sigma * 0.6) for i in range(3)], -1)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")

def cutout_open(path):
    """Which sides ("l", "t", "r", "b") of load_cutout(path) are cropped by the photo frame."""
    load_cutout(path)
    return _photo_cache[("open", path)]

def overlay(img, layer, x, y):
    """alpha_composite layer onto img at (x, y), clipping anything outside img (offsets may be negative)."""
    x, y = int(round(x)), int(round(y))
    sx, sy = max(0, -x), max(0, -y)
    w, h = min(layer.width - sx, img.width - x - sx), min(layer.height - sy, img.height - y - sy)
    if w > 0 and h > 0:
        img.alpha_composite(layer, (x + sx, y + sy), (sx, sy, sx + w, sy + h))

def fit_height(im, h):
    return im.resize((max(1, int(im.width * h / im.height)), int(h)), Image.LANCZOS)

def fade_bottom(im, frac=0.25, start=None):
    """Fade the bottom `frac` of an RGBA image to transparent (hides where a cut-out body is cropped)."""
    im = im.copy()
    hgt = im.height
    s = hgt * (1 - frac) if start is None else start
    ramp = np.clip(1 - (np.arange(hgt) - s) / max(1, hgt - s), 0, 1)[:, None]
    a = np.asarray(im.getchannel("A"), np.float32) * ramp
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im

def rim(im, width=5, color=(255, 255, 255), alpha=0.95, glow=0, glow_color=None, glow_alpha=0.8, open_edges=""):
    """Return (image, pad): im with a thin outline (and optional soft coloured glow) around its alpha shape.
    open_edges: sides cropped by the photo frame; no outline/glow is drawn past them."""
    pad = width + glow * 2 + 4
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    base.alpha_composite(im, (pad, pad))
    a = base.getchannel("A").point(lambda p: 255 if p > 90 else 0)
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    if glow:
        g = a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(glow))
        lay = Image.new("RGBA", base.size, tuple(glow_color or color) + (0,))
        lay.putalpha(g.point(lambda p: int(p * glow_alpha)))
        out.alpha_composite(lay)
    if width:
        ring = a.filter(ImageFilter.MaxFilter(2 * width + 1)).filter(ImageFilter.GaussianBlur(0.7))
        lay = Image.new("RGBA", base.size, tuple(color) + (0,))
        lay.putalpha(ring.point(lambda p: int(p * alpha)))
        out.alpha_composite(lay)
    out.alpha_composite(base)
    if open_edges:
        a = np.asarray(out.getchannel("A")).copy()
        if "l" in open_edges: a[:, :pad] = 0
        if "r" in open_edges: a[:, -pad:] = 0
        if "t" in open_edges: a[:pad, :] = 0
        if "b" in open_edges: a[-pad:, :] = 0
        out.putalpha(Image.fromarray(a))
    return out, pad

def radial(w, h, cx, cy, rx, ry, color, strength=1.0):
    """RGBA layer: soft elliptical glow of `color`."""
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    g = np.exp(-(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)) * strength
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = COLORS.get(color, color) if isinstance(color, str) else color
    arr[..., 3] = (np.clip(g, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def grade(im, k=0.22, sat=1.12, con=1.08):
    """Nudge a real photo toward the channel palette: a little more punch, navy-tinted shadows."""
    from PIL import ImageEnhance
    rgb = im.convert("RGB")
    rgb = ImageEnhance.Contrast(ImageEnhance.Color(rgb).enhance(sat)).enhance(con)
    arr = np.asarray(rgb, np.float32)
    lum = (arr @ np.array([0.299, 0.587, 0.114], np.float32))[..., None] / 255
    navy = np.array(COLORS["bg1"], np.float32)
    w = k * (1 - lum) ** 1.5
    out = Image.fromarray(np.clip(arr * (1 - w) + navy * w, 0, 255).astype(np.uint8), "RGB")
    if im.mode == "RGBA":
        out = out.convert("RGBA"); out.putalpha(im.getchannel("A"))
    return out

def shadow_text(img, xy, s, f, fill, anchor="mm", blur=10, offset=(0, 8), alpha=0.6):
    """Text with a soft drop shadow (cleaner than a thick black outline)."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((xy[0] + offset[0], xy[1] + offset[1]), s, font=f, fill=(0, 0, 0, int(255 * alpha)), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, s, font=f, fill=fill, anchor=anchor)

def card(im, w, h, focus=(0.5, 0.4), r=28, border=10, tilt=0.0, shadow=28):
    """A real photo as a rounded white-bordered card, optionally tilted, with a soft shadow. Returns (RGBA, pad)."""
    ph = grade(cover(im, w, h, focus)).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    ph.putalpha(m)
    bw, bh = w + 2 * border, h + 2 * border
    c = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle([0, 0, bw - 1, bh - 1], r + border, fill=(255, 255, 255, 255))
    c.alpha_composite(ph, (border, border))
    if tilt:
        c = c.rotate(tilt, Image.BICUBIC, expand=True)
    pad = shadow * 2
    out = Image.new("RGBA", (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (pad, pad + shadow // 2), c.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(shadow)))
    out.alpha_composite(c, (pad, pad))
    return out, pad

def trend_of(big):
    s = str(big or "").strip()
    return "down" if s[:1] in "-−↓" else "up"

def trend_graphic(w, h, trend="up", color="green", bars=True, width=None, ss=2):
    """Simple chart mark: faint rising/falling columns + one thick line with an arrowhead and a glow."""
    W2, H2 = w * ss, h * ss
    lw = (width or max(10, h // 22)) * ss
    pts = [(0.04, 0.82), (0.26, 0.62), (0.42, 0.70), (0.66, 0.40), (0.80, 0.47), (0.95, 0.12)]
    if trend == "down":
        pts = [(x, 1.0 - y) for x, y in pts]
    P = [(x * W2, y * H2) for x, y in pts]
    lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if bars:
        n = 7
        for i in range(n):
            fx = (i + 0.5) / n
            hy = 0.22 + 0.62 * (i + 1) / n if trend == "up" else 0.22 + 0.62 * (n - i) / n
            bx = fx * W2
            d.rounded_rectangle([bx - W2 / n * 0.3, H2 * (1 - hy), bx + W2 / n * 0.3, H2], 8 * ss,
                                fill=col(color, 0.13))
    line = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    dl = ImageDraw.Draw(line)
    (x1, y1), (x2, y2) = P[-2], P[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    ah = lw * 3.2
    tip = (x2, y2)
    base = (x2 - ah * math.cos(ang), y2 - ah * math.sin(ang))
    dl.line(P[:-1] + [base], fill=col(color), width=lw, joint="curve")
    for p in P[:-1]:
        dl.ellipse([p[0] - lw / 2, p[1] - lw / 2, p[0] + lw / 2, p[1] + lw / 2], fill=col(color))
    left = (base[0] + ah * 0.62 * math.cos(ang + math.pi / 2), base[1] + ah * 0.62 * math.sin(ang + math.pi / 2))
    right = (base[0] - ah * 0.62 * math.cos(ang + math.pi / 2), base[1] - ah * 0.62 * math.sin(ang + math.pi / 2))
    dl.polygon([tip, left, right], fill=col(color))
    glow = line.filter(ImageFilter.GaussianBlur(lw * 1.4))
    lay.alpha_composite(glow); lay.alpha_composite(glow); lay.alpha_composite(line)
    return lay.resize((w, h), Image.LANCZOS)

def fit_font(text, max_w, start, weight="Black", min_size=40, step=6):
    size = start
    while font(size, weight).getlength(text) > max_w and size > min_size:
        size -= step
    return font(size, weight), size

def wrap_fit(text, max_w, sizes, max_lines, weight="Black"):
    """Wrap text into as few lines as possible (up to max_lines), at the largest size from `sizes`
    that fits max_w, with the lines balanced ("YOUR CASH IS / SHRINKING", not "YOUR CASH / IS / ...")."""
    for n in range(1, max_lines + 1):
        for s in sizes:
            if n < max_lines and s < sizes[0] * 0.9:     # fewer lines only if the text stays big
                break
            f = font(s, weight)
            lines = _wrap(text, f, max_w)
            if len(lines) <= n and all(f.getlength(l) <= max_w for l in lines):
                lo, hi = max(f.getlength(w) for w in text.split()), max_w
                while hi - lo > 4:                      # narrowest width that keeps the same line count
                    mid = (lo + hi) / 2
                    if len(_wrap(text, f, mid)) <= len(lines):
                        hi = mid
                    else:
                        lo = mid
                return _wrap(text, f, hi), s
    return _wrap(text, font(sizes[-1], weight), max_w), sizes[-1]

def thumb_subject(th):
    """What the thumbnail shows beside the text: ('cutout', path), ('photo', path) or ('graphic', None)."""
    tp = th.get("photo")
    if not tp:
        return "graphic", None
    if th.get("cutout") or tp.get("cutout"):
        return "cutout", tp["file"]
    return "photo", tp["file"]

CAP = 0.727            # Inter cap height / em

def thumb_parts(th):
    big = str(th.get("big", "")).strip()
    trend = th.get("trend") or trend_of(big)
    accent = th.get("color") or ("red" if trend == "down" else "gold")
    return big, th.get("line", "").upper(), th.get("tag", "").upper(), trend, accent

def text_block(img, th, x, yc, max_w, big_color, line_color="text", tag_fill="green", tag_text="bg0",
                big_max=230, sizes=(86, 80, 74, 68, 62, 56), max_lines=2, align="l", shadow=0.55, cue=None,
                tag_size=32):
    """Tag pill + huge number + 1-3 line headline, vertically centred on yc. Returns the number's box."""
    big, line, tag, trend, _ = thumb_parts(th)
    fb, bs = fit_font(big, max_w, big_max, min_size=90, step=4)
    if not big:
        bs, cue = 0, None
    lines, ls = wrap_fit(line, max_w, sizes, max_lines) if line else ([], 0)
    fl = font(ls, "Black") if lines else None
    tag_h, tag_gap = (int(tag_size * 1.9), int(tag_size * 0.95)) if tag else (0, 0)
    gap, lead = (34 if big else 0), ls * 1.06
    total = tag_h + tag_gap + bs * CAP + (gap + ls * CAP + lead * (len(lines) - 1) if lines else 0)
    y = yc - total / 2
    anc = {"l": "ls", "r": "rs", "m": "ms"}[align]
    d = ImageDraw.Draw(img)
    if tag:
        ft = font(tag_size, "Black")
        tw = ft.getlength(tag) + tag_size * 1.5
        tx = x if align == "l" else (x - tw if align == "r" else x - tw / 2)
        rrect(d, [tx, y, tx + tw, y + tag_h], tag_h / 2, fill=col(tag_fill))
        text_c(d, (tx + tw / 2, y + tag_h / 2 + 1), tag, ft, col(tag_text))
        y += tag_h + tag_gap
    by = y + bs * CAP
    shadow_text(img, (x, by), big, fb, col(big_color), anc, blur=12, offset=(0, 8), alpha=shadow) if shadow else \
        ImageDraw.Draw(img).text((x, by), big, font=fb, fill=col(big_color), anchor=anc)
    bw = fb.getlength(big)
    bx0 = x if align == "l" else (x - bw if align == "r" else x - bw / 2)
    if cue:   # small trend arrow right of the number, when there is room
        cw, ch = int(bs * 0.62), int(bs * 0.5)
        if bx0 + bw + 24 + cw <= x + max_w + (0 if align == "l" else -bw):
            overlay(img, trend_graphic(cw, ch, cue[0], cue[1], bars=False, width=max(7, bs // 22)),
                      bx0 + bw + 22, by - bs * CAP + (bs * CAP - ch) / 2)
    y = by + gap
    for i, ln in enumerate(lines):
        ly = y + ls * CAP + i * lead
        if shadow:
            shadow_text(img, (x, ly), ln, fl, col(line_color), anc, blur=8, offset=(0, 5), alpha=shadow * 0.9)
        else:
            ImageDraw.Draw(img).text((x, ly), ln, font=fl, fill=col(line_color), anchor=anc)
    return (bx0, by - bs * CAP, bx0 + bw, by)

def v_photo(d, v, t, dur):
    """Real photo (person, company, product, place) with optional big number and label.
    v: {"type": "photo", "file": "assets/photos/x.jpg", "title"?, "value"?, "color"?, "label"?, "focus"?: [fx, fy]}"""
    scene_title(d, v.get("title"), t)
    a = ease(t / 0.45)
    w = 940
    h = 600 if v.get("label") else 700
    x, y = CX - w // 2, 480 + int(25 * (1 - a))
    paste_photo(d, v["file"], (x, y, x + w, y + h), a, tuple(v.get("focus", (0.5, 0.4))))
    if v.get("value"):
        sc = 0.85 + 0.15 * a
        text_c(d, (CX, y + h - 85), v["value"], font(int(150 * sc), "Black"), col(v.get("color", "gold"), a),
               stroke=12, stroke_fill=(0, 0, 0, int(255 * a)))
    if v.get("label"):
        text_c(d, (CX, y + h + 50), v["label"], font(44, "SemiBold", False), col("text", a))

VISUALS = dict(pair=v_pair, compare=v_compare, timeline=v_timeline, stat=v_stat,
               bars=v_bars, equation=v_equation, line=v_line, cta=v_cta, photo=v_photo)

# ---------------------------------------------------------------- audio
def speech_bounds(x, thr=0.02):
    idx = np.where(np.abs(x) > thr)[0]
    return (idx[0], idx[-1]) if len(idx) else (0, len(x))

PROGRESSIONS = [
    [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],   # Am F C G
    [[48, 52, 55], [55, 59, 62], [57, 60, 64], [53, 57, 60]],   # C G Am F
    [[50, 53, 57], [55, 59, 62], [48, 52, 55], [57, 60, 64]],   # Dm G C Am
    [[52, 55, 59], [48, 52, 55], [55, 59, 62], [50, 54, 57]],   # Em C G D
]


def make_music(n, seed=""):
    """Soft original ambient pad + pluck, procedurally generated (no licensing).
    Tempo and chords vary per video (seeded by its id) so Shorts don't all sound alike."""
    import zlib
    h = zlib.crc32(seed.encode())
    t = np.arange(n) / SR
    bpm = 76 + h % 21 if seed else 84
    beat = 60 / bpm
    chords = PROGRESSIONS[(h // 21) % len(PROGRESSIONS)] if seed else PROGRESSIONS[0]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(n)
    bar = beat * 4
    for ci in range(int(t[-1] / bar) + 1):
        ch = chords[ci % 4]
        s0, s1 = int(ci * bar * SR), min(n, int((ci + 1) * bar * SR) + SR // 2)
        if s0 >= n:
            break
        tt = np.arange(s1 - s0) / SR
        env = np.minimum(1, tt / 0.6) * np.exp(-np.maximum(0, tt - bar) * 4)
        for m in ch:
            f = hz(m - 12)
            out[s0:s1] += 0.08 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.003 * tt))
        for k in range(8):  # eighth-note pluck arpeggio
            p0 = s0 + int(k * beat / 2 * SR)
            if p0 >= n:
                break
            m = ch[[0, 1, 2, 1][k % 4]] + 12
            ln = min(n - p0, int(0.5 * SR))
            tp = np.arange(ln) / SR
            out[p0:p0 + ln] += 0.05 * np.exp(-tp * 9) * np.sin(2 * np.pi * hz(m) * tp)
    # gentle kick on beats
    for b in range(int(t[-1] / beat) + 1):
        p0 = int(b * beat * SR)
        ln = min(n - p0, int(0.25 * SR))
        if ln <= 0:
            break
        tp = np.arange(ln) / SR
        out[p0:p0 + ln] += 0.12 * np.exp(-tp * 18) * np.sin(2 * np.pi * (50 + 60 * np.exp(-tp * 30)) * tp)
    return out / (np.max(np.abs(out)) + 1e-9)

def build_audio(spec, work):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    voice, speed = spec.get("voice", "af_heart"), spec.get("speed", 1.05)
    gap = int(spec.get("gap", 0.15) * SR)
    chunks, timeline, cur = [], [], int(0.05 * SR)   # start talking almost at once
    chunks.append(np.zeros(cur))
    for sc in spec["scenes"]:
        a, sr = k.create(sc["say"], voice=voice, speed=speed, lang="en-us")
        assert sr == SR
        s0, s1 = speech_bounds(a)
        a = a[max(0, s0 - int(0.03 * SR)): s1 + int(0.08 * SR)]
        start = cur
        chunks.append(a); cur += len(a)
        chunks.append(np.zeros(gap)); cur += gap
        timeline.append({"start": start / SR, "speech_end": (start + len(a)) / SR, "end": cur / SR})
    tail = int(spec.get("tail", 0.35) * SR)   # long videos pass a longer tail for end screens
    chunks.append(np.zeros(tail)); cur += tail
    voice_track = np.concatenate(chunks).astype(np.float32)
    voice_track /= (np.max(np.abs(voice_track)) + 1e-9) / 0.9
    music = make_music(len(voice_track), spec.get("id", "")) * 10 ** (-24 / 20)
    fade = np.minimum(1, np.arange(len(music))[::-1] / (0.8 * SR))
    mix = voice_track + music * fade
    path = os.path.join(work, "audio.wav")
    sf.write(path, mix.astype(np.float32), SR)
    return path, timeline, len(mix) / SR

# ---------------------------------------------------------------- captions
def asr_words(audio_path):
    """Word timestamps from Whisper, used to sync captions to the actual voice."""
    try:
        from faster_whisper import WhisperModel
        a16 = audio_path.replace(".wav", "_16k.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", audio_path, "-ar", "16000",
                        "-ac", "1", a16], check=True)
        a, _ = sf.read(a16, dtype="float32")
        m = WhisperModel("base.en", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(a, word_timestamps=True)
        return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    except Exception as e:  # fall back to proportional timing
        print("ASR unavailable, using estimated caption timing:", e)
        return None

def align_words(say, seg, asr):
    """Map script words onto the ASR timeline by character position within the scene."""
    if not asr:
        return word_times(say, seg["start"], seg["speech_end"])
    ws = [w for w in asr if seg["start"] - 0.05 <= (w[1] + w[2]) / 2 <= seg["end"]]
    if len(ws) < 2:
        return word_times(say, seg["start"], seg["speech_end"])
    # piecewise-linear map: fraction of characters spoken -> time
    tot = sum(len(w[0]) for w in ws)
    fr, tm, c = [0.0], [ws[0][1]], 0
    for w in ws:
        c += len(w[0]); fr.append(c / tot); tm.append(w[2])
    words = say.split()
    stot = sum(len(w) for w in words)
    out, c = [], 0
    for w in words:
        s = float(np.interp(c / stot, fr, tm)); c += len(w)
        e = float(np.interp(c / stot, fr, tm))
        out.append((w, s, e))
    return out

def word_times(say, start, end):
    words = say.split()
    weights = [len(w.strip(",.?!:;")) + 1.5 + (3 if w[-1] in ",.?!:;" else 0) for w in words]
    total = sum(weights)
    out, t = [], start
    for w, wt in zip(words, weights):
        dt = (end - start) * wt / total
        out.append((w, t, t + dt)); t += dt
    return out

_SMALL = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen".split())}
_TENS = {w: 10 * i for i, w in enumerate("x x twenty thirty forty fifty sixty seventy eighty ninety".split()) if i >= 2}
_MULT = {"thousand": 10**3, "million": 10**6, "billion": 10**9, "trillion": 10**12}
_NUMWORDS = set(_SMALL) | set(_TENS) | set(_MULT) | {"hundred"}
_PUNCT = ",.?!:;\"'"


def _parse_int(parts):
    """Spoken integer -> (value, used_big_multiplier) or None if the words aren't one clean number."""
    total, cur, last, big = 0, 0, None, False
    for i, p in enumerate(parts):
        if p == "a":
            if i != 0:
                return None
            cur, last = 1, "small"
        elif p == "and":
            if last not in ("hundred", "mult"):
                return None
        elif p in _SMALL:
            v = _SMALL[p]
            if last in ("small", "tens_unit") or (last == "tens" and v >= 10) or (last == "tens" and v == 0):
                return None
            cur += v
            last = "tens_unit" if last == "tens" else "small"
        elif p in _TENS:
            if last in ("small", "tens", "tens_unit"):
                return None
            cur += _TENS[p]; last = "tens"
        elif p == "hundred":
            if last in (None, "hundred", "mult") or cur == 0 or cur >= 100:
                return None
            cur *= 100; last = "hundred"
        elif p in _MULT:
            if last is None or last == "mult":
                return None
            total += cur * _MULT[p]; cur = 0; last = "mult"; big = big or _MULT[p] >= 10**6
        else:
            return None
    if last in (None, "and"):
        return None
    return total + cur, big


def _parse_number(parts):
    """Returns (display_number_string, value) or None. Handles years ("twenty twenty-five") and decimals."""
    if "point" in parts:
        k = parts.index("point")
        whole, frac = parts[:k], parts[k + 1:]
        if not frac or any(f not in _SMALL or _SMALL[f] > 9 for f in frac):
            return None
        w = _parse_int(whole) if whole else (0, False)
        if not w:
            return None
        s = f"{w[0]}." + "".join(str(_SMALL[f]) for f in frac)
        return s, float(s)
    r = _parse_int(parts)
    if r:
        v, big = r
        if big and v >= 10**6:
            for d, u in ((10**12, "T"), (10**9, "B"), (10**6, "M")):
                if v >= d:
                    return f"{v / d:g}{u}", v
        return (str(v) if 1900 <= v <= 2100 or v < 1000 else f"{v:,}"), v
    if parts and parts[0] in ("nineteen", "twenty") and len(parts) in (2, 3):   # spoken years
        rest = _parse_int(parts[1:])
        if rest and 10 <= rest[0] <= 99:
            v = (19 if parts[0] == "nineteen" else 20) * 100 + rest[0]
            return str(v), v
    return None


def _decimal_mult(parts):
    """'seven point two billion' -> split off the trailing multiplier so decimals scale."""
    if "point" in parts and parts[-1] in _MULT and len(parts) > 2:
        return parts[:-1], parts[-1]
    return parts, None


def digit_captions(wts):
    """Show spoken numbers as digits in captions: 'seven hundred ninety-two thousand dollars' -> '$792,000',
    'four point seven percent' -> '4.7%', 'twenty twenty-five' -> '2025'. The voice still says the words.
    Anything that doesn't parse as one clean number is left as words."""
    out, i, n = [], 0, len(wts)

    def core(w):
        return w.lower().strip(_PUNCT)

    def is_num(j):
        c = core(wts[j][0])
        return bool(c) and all(p in _NUMWORDS for p in c.split("-"))

    while i < n:
        j, parts = i, []
        while j < n:
            c = core(wts[j][0])
            nxt_num = j + 1 < n and is_num(j + 1)
            if is_num(j):
                parts += c.split("-")
            elif c == "a" and not parts and j + 1 < n and core(wts[j + 1][0]) in ("hundred", "thousand", "million", "billion"):
                parts.append("a")
            elif c == "and" and parts and parts[-1] in ("hundred", "thousand", "million", "billion") and nxt_num \
                    and wts[j - 1][0][-1] not in _PUNCT:
                parts.append("and")
            elif c == "point" and parts and nxt_num and wts[j - 1][0][-1] not in _PUNCT:
                parts.append("point")
            else:
                break
            j += 1
            if wts[j - 1][0][-1] in _PUNCT:
                break
        if not parts:
            out.append(wts[i]); i += 1; continue
        # Longest run of words that parses as one number ("two thousand seven one in..." -> "two thousand seven").
        while True:
            base, mult = _decimal_mult(parts)
            parsed = _parse_number(base)
            if parsed or j - i <= 1:
                break
            j -= 1
            parts = [p for k in range(i, j) for p in
                     (core(wts[k][0]).split("-") if is_num(k) else [core(wts[k][0])])]
        if parsed and mult:
            parsed = (f"{parsed[1]:g}{ {'thousand': 'K', 'million': 'M', 'billion': 'B', 'trillion': 'T'}[mult]}",
                      parsed[1] * _MULT[mult])
        single_small = len(parts) == 1 and parts[0] in _SMALL and _SMALL[parts[0]] <= 10
        unit, end_j = "", j
        if parsed and wts[j - 1][0][-1] not in _PUNCT and j < n:
            u = core(wts[j][0])
            if u == "percent":
                unit, end_j = "%", j + 1
            elif u in ("dollars", "dollar"):
                unit, end_j = "$", j + 1
            elif u in ("rupees", "rupee"):
                unit, end_j = "₹", j + 1
        if not parsed or (single_small and not unit) or parts[-1] in ("and", "point"):
            out.append(wts[i]); i += 1; continue
        num = parsed[0]
        txt = (unit + num) if unit in ("$", "₹") else (num + unit)
        tail = wts[end_j - 1][0]
        trail = tail[len(tail.rstrip(_PUNCT)):]
        out.append((txt + trail, wts[i][1], wts[end_j - 1][2]))
        i = end_j
    return out


def caption_fix(wts, fixes):
    """Show a different spelling in captions than the one written for the voice, e.g.
    spec "caption_fix": {"Oh-pruh": "Oprah"} (the voice needs the respelling, viewers need the name)."""
    if not fixes:
        return wts
    out = []
    for w, s, e in wts:
        core = w.rstrip(_PUNCT + ".")
        tail = w[len(core):]
        if core.endswith("'s") and core[:-2] in fixes:
            core, tail = core[:-2], "'s" + tail
        out.append((fixes.get(core, core) + tail, s, e))
    return out


def chunk_words(wts, max_chars=16, max_words=3):
    chunks, cur = [], []
    for w in wts:
        trial = " ".join(x[0] for x in cur + [w])
        if cur and (len(trial) > max_chars or len(cur) >= max_words):
            chunks.append(cur); cur = []
        cur.append(w)
        if w[0][-1] in ".?!:":
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    return chunks

def draw_captions(img, chunks, t):
    d = ImageDraw.Draw(img)
    for ch in chunks:
        if ch[0][1] - 0.05 <= t < ch[-1][2] + 0.05:
            f = font(74, "Black")
            words = [w[0].upper() for w in ch]
            space = f.getlength(" ")
            widths = [f.getlength(w) for w in words]
            total = sum(widths) + space * (len(words) - 1)
            x = CX - total / 2
            pop = ease((t - ch[0][1]) / 0.12)
            for (w, s, e), txt, wd in zip(ch, words, widths):
                active = s <= t < e
                fill = col("gold") if active else col("text")
                d.text((x, CAP_Y + 8 * (1 - pop)), txt, font=f, fill=fill, anchor="lm",
                       stroke_width=8, stroke_fill=(0, 0, 0, 255))
                x += wd + space
            break


# ---------------------------------------------------------------- Shorts thumbnail (1080x1920)
def _thumb_big(spec):
    """The headline number for the thumbnail: spec["thumbnail"]["big"], else the first stat/compare value."""
    th = spec.get("thumbnail") or {}
    try:
        th = {**json.load(open(os.path.join(HERE, "short_thumbs.json"))).get(spec["id"], {}), **th}
    except FileNotFoundError:
        pass
    if th.get("big"):
        return th["big"], th.get("color", "gold")
    strong = ("gold", "green", "red")
    for sc in spec["scenes"][:3]:
        v = sc["visual"]
        if v["type"] == "stat" and len(str(v.get("value", ""))) <= 9:
            return str(v["value"]), v.get("color") if v.get("color") in strong else "gold"
        if v["type"] == "compare":
            sides = [v["left"], v["right"]]
            pick = next((x for x in sides if x.get("color") in strong), None) or \
                max(sides, key=lambda x: x["value"] if not isinstance(x["value"], str) else 0)
            val = pick["value"] if isinstance(pick["value"], str) else fmt(pick["value"], v.get("format"))
            if len(val) <= 9:
                return val, pick.get("color") if pick.get("color") in strong else "gold"
    return None, "gold"

def _wrap(text, f, width):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])

def _photo_short_thumb(spec, out_dir, tp):
    """Photo thumbnail: the real person/company full-bleed, dark gradient, huge outlined number, bold title."""
    import numpy as np
    img = cover(load_photo(tp["file"]), W, H, tuple(tp.get("focus", (0.5, 0.35)))).convert("RGBA")
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(ImageEnhance.Color(img.convert("RGB")).enhance(1.25)).enhance(1.1).convert("RGBA")
    yy = np.linspace(0, 1, H)[:, None]
    shade = np.clip(np.maximum(0, (yy - 0.30) / 0.45) * 0.88 + np.maximum(0, (0.16 - yy) / 0.16) * 0.55, 0, 0.9)
    over = np.zeros((H, W, 4), np.uint8); over[..., 3] = (shade * 255).astype(np.uint8).repeat(W, 1)
    over[..., :3] = (6, 10, 22)
    img.alpha_composite(Image.fromarray(over, "RGBA"))
    d = ImageDraw.Draw(img)
    th = spec.get("thumbnail") or {}
    line = th.get("line") or spec["title"]
    big, color = _thumb_big(spec)
    badge = spec.get("badge")
    if badge:
        f = font(46, "Black"); bw = f.getlength(badge) + 80
        rrect(d, [CX - bw / 2, 425, CX + bw / 2, 515], 45, fill=col("green"))
        text_c(d, (CX, 470), badge, f, col("bg0"))
    y = 1000
    if big:
        size = 340
        while font(size, "Black").getlength(big) > 980 and size > 120:
            size -= 10
        text_c(d, (CX + 8, y + 10), big, font(size, "Black"), (0, 0, 0, 150))          # drop shadow
        text_c(d, (CX, y), big, font(size, "Black"), col(color), stroke=16, stroke_fill=(0, 0, 0, 255))
        ty = y + size * 0.62
    else:
        ty = 950
    for size in (96, 88, 80, 72, 66):
        f = font(size, "Black")
        lines = _wrap(line.upper(), f, 960)
        if len(lines) <= 3:
            break
    for i, ln in enumerate(lines):
        text_c(d, (CX, ty + i * size * 1.12), ln, f, col("gold") if i == 0 and len(lines) > 1 else col("text"),
               stroke=9, stroke_fill=(0, 0, 0, 255))
    path = os.path.join(out_dir, spec["id"] + "_thumb.png")
    img.convert("RGB").save(path, optimize=True)
    return path

def short_thumb_image(th):
    """Styled vertical thumbnail (1080x1920 RGBA); all text kept inside y 380-1450.
    th: big, line, tag, photo {file, focus, zoom?}, cutout, color, trend, style "A" | "B".
    A "Spotlight": number + headline on top, the person/photo/chart below on a clean navy stage.
    B "Colour block": person/photo/chart on top, solid accent panel with navy text below."""
    style = str(th.get("style", "A")).upper()
    big, line, tag, trend, accent = thumb_parts(th)
    kind, path = thumb_subject(th)
    tp = th.get("photo") or {}
    focus, zoom = tuple(tp.get("focus", (0.5, 0.4))), tp.get("zoom", 1.0)
    tone = "green" if trend == "up" else "red"
    img = make_background().copy()

    def person(top, h, cx=CX, glow="green", glow_a=0.6):
        c = load_cutout(path)
        h = h * zoom
        if c.width * h / c.height > W * 1.1:
            h = c.height * W * 1.1 / c.width
        c = grade(fit_height(c, h), k=0.08, sat=1.06, con=1.04)
        op = cutout_open(path)
        lay, pad = rim(c, 4, (255, 255, 255), 0.5, 30, COLORS.get(glow, glow), glow_a, op)
        x = cx - lay.width / 2
        if "r" in op and x + lay.width - pad < W:
            x = W - (lay.width - pad)
        if "l" in op and x + pad > 0:
            if "r" in op:
                x = -pad
            else:
                a = np.asarray(lay.getchannel("A"), np.float32)
                ramp = np.clip((np.arange(lay.width) - pad) / (0.22 * c.width), 0, 1)[None, :]
                lay = lay.copy(); lay.putalpha(Image.fromarray((a * ramp).astype(np.uint8)))
        if "b" in op and top + h < H:
            lay = fade_bottom(lay, 0.0, start=pad + h * 0.8)
        overlay(img, lay, x, top - pad)

    if style == "B":
        py = 1000                                     # panel top (left end); text sits in 1010-1440
        img.alpha_composite(radial(W, H, CX, 640, 520, 420, "green" if kind == "cutout" else tone, 0.30))
        if kind == "cutout":
            person(330, 900)
        elif kind == "photo":
            ph = grade(cover(load_photo(path), W, py + 80, focus), k=0.25).convert("RGBA")
            img.alpha_composite(ph, (0, 0))
            top = np.clip(1 - np.linspace(0, 1, py + 80) / 0.22, 0, 1) ** 2 * 0.75   # keep the very top calm
            lay = np.zeros((py + 80, W, 4), np.uint8); lay[..., :3] = COLORS["bg0"]
            lay[..., 3] = (top[:, None].repeat(W, 1) * 255).astype(np.uint8)
            img.alpha_composite(Image.fromarray(lay, "RGBA"))
        else:
            overlay(img, trend_graphic(900, 560, trend, tone), 90, 400)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).polygon([(0, py - 14), (W, py + 50), (W, H), (0, H)], fill=(0, 0, 0, 150))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        ImageDraw.Draw(img).polygon([(0, py), (W, py + 64), (W, H), (0, H)], fill=col(accent))
        text_block(img, th, CX, 1250, 960, "bg0", "bg0", tag_fill="bg0", tag_text=accent, big_max=250,
                   sizes=(88, 82, 76, 70, 64), max_lines=2, align="m", shadow=0, tag_size=42)
    else:
        img.alpha_composite(radial(W, H, CX, 1350, 560, 520, "green" if kind == "cutout" else tone, 0.32))
        if kind == "cutout":
            person(930, 1080)
        elif kind == "photo":
            lay, pad = card(load_photo(path), 880, 620, focus, r=30, border=10, tilt=-3.0, shadow=30)
            overlay(img, lay, CX - lay.width / 2, 1310 - lay.height / 2)
        else:
            overlay(img, trend_graphic(960, 620, trend, tone), 60, 960)
        text_block(img, th, CX, 650, 960, accent, big_max=300, sizes=(100, 92, 84, 76, 70), max_lines=3,
                   align="m", cue=None, tag_size=42)
    return img

def make_short_thumb(spec, out_dir):
    """Vertical Shorts thumbnail: badge, big number, title. Kept inside y 380-1450 (clear of Shorts overlays)."""
    th = spec.get("thumbnail") or {}
    if th.get("style"):
        big, color = _thumb_big(spec)
        th = {**th, "big": th.get("big") or big or "", "color": th.get("color") or (color if big else None),
              "line": th.get("line") or spec["title"].replace("#shorts", "").strip(),
              "tag": th.get("tag") or spec.get("badge", "")}
        path = os.path.join(out_dir, spec["id"] + "_thumb.png")
        short_thumb_image(th).convert("RGB").save(path, optimize=True)
        return path
    tp = (spec.get("thumbnail") or {}).get("photo")
    if tp:
        return _photo_short_thumb(spec, out_dir, tp)
    img = make_background().copy()
    d = ImageDraw.Draw(img)
    th = spec.get("thumbnail") or {}
    line = th.get("line") or spec["title"].replace("#shorts", "").strip()
    big, color = _thumb_big(spec)
    y = 470
    badge = spec.get("badge")
    if badge:
        f = font(46, "Black")
        bw = f.getlength(badge) + 80
        rrect(d, [CX - bw / 2, y - 45, CX + bw / 2, y + 45], 45, fill=col("green"))
        text_c(d, (CX, y), badge, f, col("bg0"))
    if big:
        size = 330
        while font(size, "Black").getlength(big) > 940 and size > 120:
            size -= 10
        text_c(d, (CX, 800), big, font(size, "Black"), col(color), stroke=10, stroke_fill=(0, 0, 0, 255))
        ty = 1060
    else:
        ty = 760
    for size in (110, 100, 90, 80, 72):
        f = font(size, "Black")
        lines = _wrap(line.upper(), f, 940)
        if len(lines) <= (3 if big else 5):
            break
    for i, ln in enumerate(lines):
        text_c(d, (CX, ty + i * size * 1.12), ln, f, col("text"), stroke=7, stroke_fill=(0, 0, 0, 255))
    path = os.path.join(out_dir, spec["id"] + "_thumb.png")
    img.convert("RGB").save(path, optimize=True)
    return path

# ---------------------------------------------------------------- main render
def draw_chrome(img, spec):
    d = ImageDraw.Draw(img)
    badge, disclaimer = spec.get("badge", ""), spec.get("disclaimer", "")
    if badge:
        f = font(32, "Bold")
        bw = f.getlength(badge) + 60
        rrect(d, [CX - bw / 2, 225, CX + bw / 2, 285], 30, fill=col("green", 0.18), outline=col("green"), width=2)
        text_c(d, (CX, 255), badge, f, col("green"))
    if disclaimer:
        text_c(d, (CX, 325), disclaimer, font(28, "Medium", False), col("muted"))

def preview_frame(spec, i, t, dur=6.0):
    """One still of scene i at time t (no audio): used by preview.py for quick layout checks."""
    img = make_background().copy()
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_chrome(layer, spec)
    img.alpha_composite(layer)
    vis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    VISUALS[spec["scenes"][i]["visual"]["type"]](ImageDraw.Draw(vis), spec["scenes"][i]["visual"], t, max(dur, t + 0.5))
    img.alpha_composite(vis, (0, VIS_SHIFT), (30, 0))
    return img

def render(spec_path, out_dir):
    spec = json.load(open(spec_path))
    global DEFAULT_FMT
    DEFAULT_FMT = spec.get("currency", "usd")
    os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "work"); os.makedirs(work, exist_ok=True)
    audio, tl, total = build_audio(spec, work)
    caps = []
    asr = asr_words(audio)
    for sc, seg in zip(spec["scenes"], tl):
        caps += chunk_words(digit_captions(caption_fix(align_words(sc["say"], seg, asr), spec.get("caption_fix"))))
    bg = make_background()
    out = os.path.join(out_dir, spec["id"] + ".mp4")
    tmp_out = out[:-4] + ".partial.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp_out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    for fi in range(nframes):
        t = fi / FPS
        si = 0
        for i, seg in enumerate(tl):
            if t >= seg["start"] - 0.1:
                si = i
        seg, sc = tl[si], spec["scenes"][si]
        img = bg.copy()
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_chrome(layer, spec)
        img.alpha_composite(layer)
        vis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        st = t - (seg["start"] - 0.25) + (0.6 if si == 0 else 0)   # first frame already shows the visual
        dur = seg["end"] - seg["start"]
        VISUALS[sc["visual"]["type"]](ImageDraw.Draw(vis), sc["visual"], st, dur)
        # Slow push-in while a visual is held, so the picture never sits still (retention).
        z = 1 + ZOOM * min(1.0, max(0.0, st) / max(dur, 1.0))
        if z > 1.001:
            zw, zh = int(W * z), int(H * z)
            left, top = int(CX * z - CX), int(ZOOM_CY * z - ZOOM_CY)
            vis = vis.resize((zw, zh), Image.BILINEAR).crop((left, top, left + W, top + H))
        img.alpha_composite(vis, (0, VIS_SHIFT), (30, 0))
        draw_captions(img, caps, t)
        # progress bar
        proc.stdin.write(img.convert("RGB").tobytes())
        if fi == int(nframes * 0.3):
            img.convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb_frame.png"))
    proc.stdin.close()
    if proc.wait() != 0 or not os.path.getsize(tmp_out):
        raise SystemExit(f"ffmpeg failed for {spec['id']}; no video written")
    os.replace(tmp_out, out)
    make_short_thumb(spec, out_dir)
    json.dump({"timeline": tl, "duration": total}, open(os.path.join(work, "timeline.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "--thumb-only":      # python3 render.py --thumb-only spec.json out_dir
        sp = json.load(open(sys.argv[2])); DEFAULT_FMT = sp.get("currency", "usd")
        print(make_short_thumb(sp, sys.argv[3]))
    else:
        print(render(sys.argv[1], sys.argv[2]))
