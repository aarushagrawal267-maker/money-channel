"""Render a long-form 16:9 (1920x1080) video from a JSON spec.

Usage: python3 render_long.py spec.json out_dir

Reuses audio, ASR caption sync and drawing helpers from render.py.
Scene visual types: chapter, title, stat, count, stat_grid, hbars, share, flywheel, bullets,
equation, line, cta, waterfall, donut, columns, versus, timeline, quote, table, photo.
Writes <id>.mp4, <id>_chapters.txt (YouTube chapters) and <id>_thumb.png.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
from render import font, col, ease, text_c, rrect, fmt

W, H, FPS = 1920, 1080, 30
CX = W // 2
TOP, BOT = 250, 880          # visual area
CAP_Y = 975

def background():
    bw, bh = W + 240, H + 140
    y = np.linspace(0, 1, bh)[:, None]
    x = np.linspace(0, 1, bw)[None, :]
    b0, b1 = np.array(R.COLORS["bg0"]), np.array(R.COLORS["bg1"])
    base = b0 + (b1 - b0) * (0.7 * y)[..., None]
    glow = np.exp(-(((x - 0.5) / 0.4) ** 2 + ((y - 0.42) / 0.35) ** 2))[..., None]
    base = base + glow * np.array([18, 36, 36])
    # two faint brand-colour washes (green low-left, gold high-right) for a little more warmth and depth
    g2 = np.exp(-(((x - 0.08) / 0.30) ** 2 + ((y - 0.95) / 0.35) ** 2))[..., None]
    g3 = np.exp(-(((x - 0.92) / 0.28) ** 2 + ((y - 0.05) / 0.30) ** 2))[..., None]
    base = base + g2 * np.array([4, 30, 14]) + g3 * np.array([22, 17, 2])
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    for gx in range(0, bw, 80):
        d.line([(gx, 0), (gx, bh)], fill=col("grid", 0.3), width=1)
    for gy in range(0, bh, 80):
        d.line([(0, gy), (bw, gy)], fill=col("grid", 0.3), width=1)
    return img

def title(d, s, t, y=TOP - 70):
    if s:
        a = ease(t / 0.4)
        text_c(d, (CX, y + 15 * (1 - a)), s, font(60, "Bold"), col("text", a))

# ------------------------------------------------------------------ visuals
def v_chapter(d, v, t, dur):
    a = ease(t / 0.5)
    n = str(v["n"])
    # huge faint chapter number behind, drifting slightly
    text_c(d, (CX + 6 * t, 520), n.zfill(2) if n.isdigit() else n, font(520, "Black"), col("green", 0.07 * a))
    f = font(38, "Black")
    lab = f"CHAPTER {n}"
    pw = f.getlength(lab) + 64
    y = 420 - 20 * (1 - a)
    rrect(d, [CX - pw / 2, y - 32, CX + pw / 2, y + 32], 32, fill=col("green", 0.16 * a), outline=col("green", a), width=3)
    text_c(d, (CX, y + 1), lab, f, col("green", a))
    tf, _ = R.fit_font(v["title"], W - 240, 110, min_size=60, step=6)
    text_c(d, (CX, 545), v["title"], tf, col("text", a))
    w = 600 * ease((t - 0.2) / 0.6)
    d.rectangle([CX - w / 2, 640, CX + w / 2, 646], fill=col("green", a))
    g = 140 * ease((t - 0.5) / 0.5)
    if g > 1:
        d.rectangle([CX + w / 2 - g, 640, CX + w / 2, 646], fill=col("gold", a))

def v_title(d, v, t, dur):
    a = ease(t / 0.5)
    text_c(d, (CX, 470), v["title"], font(120, "Black"), col("text", a))
    if v.get("sub"):
        text_c(d, (CX, 600), v["sub"], font(54, "SemiBold", False), col(v.get("sub_color", "gold"), ease((t - 0.3) / 0.5)))

def v_stat(d, v, t, dur):
    title(d, v.get("title"), t)
    a = ease(t / 0.5)
    text_c(d, (CX, 540), v["value"], font(int(260 * (0.88 + 0.12 * a)), "Black"), col(v.get("color", "gold"), a))
    text_c(d, (CX, 720), v.get("label", ""), font(52, "SemiBold", False), col("text", a))
    if v.get("sub"):
        text_c(d, (CX, 790), v["sub"], font(38, "Medium", False), col("muted", a))

def v_stat_grid(d, v, t, dur):
    title(d, v.get("title"), t)
    items = v["items"]
    n = len(items)
    cw, gap = min(520, (W - 240 - (n - 1) * 40) / n), 40
    x0 = CX - (n * cw + (n - 1) * gap) / 2
    for i, it in enumerate(items):
        a = ease((t - 0.25 * i) / 0.5)
        x = x0 + i * (cw + gap)
        y0 = 330 + 30 * (1 - a)
        c = it.get("color", "green")
        rrect(d, [x, y0, x + cw, y0 + 420], 36, fill=col(c, 0.10 * a), outline=col(c, 0.7 * a), width=4)
        text_c(d, (x + cw / 2, y0 + 170), it["value"], font(110 if len(it["value"]) < 7 else 88, "Black"), col(c, a))
        text_c(d, (x + cw / 2, y0 + 300), it["label"], font(40, "SemiBold", False), col("text", a))
        if it.get("sub"):
            text_c(d, (x + cw / 2, y0 + 355), it["sub"], font(30, "Medium", False), col("muted", a))

def v_hbars(d, v, t, dur):
    title(d, v.get("title"), t)
    items = v["items"]
    mx = max(i["value"] for i in items)
    n = len(items)
    rowh = min(150, (BOT - TOP) / n)
    y0 = TOP + ((BOT - TOP) - rowh * n) / 2 + 40
    L, Rr = 560, 1700
    for i, it in enumerate(items):
        p = ease((t - 0.2 * i) / 1.0)
        y = y0 + i * rowh
        c = it.get("color", "green")
        text_c(d, (L - 30, y), it["label"], font(46, "Bold"), col("text", min(1, p * 2)), anchor="rm")
        wbar = (Rr - L - 260) * it["value"] / mx * p
        if wbar > 4:
            rrect(d, [L, y - 40, L + max(wbar, 40), y + 40], 20, fill=col(c, 0.9))
        lab = it.get("display") or fmt(it["value"] * p if p < 0.999 else it["value"], v.get("format"))
        f = font(54, "Black")
        if L + wbar + 30 + f.getlength(lab) > W - 60 and wbar > f.getlength(lab) + 60:
            text_c(d, (L + wbar - 30, y), lab, f, col("bg0", min(1, p * 2)), anchor="rm")   # inside the bar
        else:
            text_c(d, (L + wbar + 30, y), lab, f, col("text", min(1, p * 2)), anchor="lm")

def v_share(d, v, t, dur):
    """Rows of 100% bars: highlighted share vs rest."""
    title(d, v.get("title"), t)
    rows = v["rows"]
    L, Rr = 260, 1660
    for i, row in enumerate(rows):
        y = 420 + i * 230
        a = ease((t - 0.6 * i) / 0.5)
        p = ease((t - 0.6 * i - 0.2) / 1.0)
        text_c(d, (L, y - 75), row["label"], font(44, "Bold"), col("text", a), anchor="lm")
        rrect(d, [L, y - 40, Rr, y + 40], 40, fill=col("grid", a))
        wpart = (Rr - L) * row["share"] * p
        c = row.get("color", "gold")
        if wpart > 4:
            rrect(d, [L, y - 40, L + max(80, wpart), y + 40], 40, fill=col(c, a))
        text_c(d, (Rr, y - 75), f"{row['share']*100*p:.{row.get('dp', 0)}f}%", font(56, "Black"), col(c, a), anchor="rm")
    if v.get("note"):
        text_c(d, (CX, BOT - 10), v["note"], font(34, "Medium", False), col("muted", ease((t - 1.5) / 0.5)))

def v_flywheel(d, v, t, dur):
    title(d, v.get("title"), t)
    steps = v["steps"]
    n = len(steps)
    cx, cy, rad = CX, 575, 270
    per = max(0.6, (dur - 1.0) / n)
    for i, s in enumerate(steps):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + rad * 1.55 * math.cos(ang), cy + rad * math.sin(ang)
        a = ease((t - per * i) / 0.4)
        # arrow to next
        ang2 = -math.pi / 2 + 2 * math.pi * (i + 0.5) / n
        ax, ay = cx + rad * 1.55 * math.cos(ang2), cy + rad * math.sin(ang2)
        if a > 0.5:
            d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=col("dim", a))
        f = font(40, "Bold")
        tw = f.getlength(s) + 60
        rrect(d, [x - tw / 2, y - 45, x + tw / 2, y + 45], 45,
              fill=col("green", 0.15 * a), outline=col("green", a), width=3)
        text_c(d, (x, y), s, f, col("text", a))
    # rotating arc in centre
    a = ease(t / 0.6)
    st = (t * 60) % 360
    d.arc([cx - 110, cy - 110, cx + 110, cy + 110], st, st + 300, fill=col("gold", a), width=10)
    text_c(d, (cx, cy), v.get("center", ""), font(36, "Black"), col("gold", a))

def v_bullets(d, v, t, dur):
    title(d, v.get("title"), t)
    items = v["items"]
    per = max(0.5, (dur - 0.8) / len(items))
    y0 = TOP + 120
    for i, it in enumerate(items):
        a = ease((t - per * i) / 0.4)
        y = y0 + i * 125
        d.ellipse([360, y - 18, 396, y + 18], fill=col(v.get("color", "green"), a))
        text_c(d, (430 + 20 * (1 - a), y), it, font(54, "Bold"), col("text", a), anchor="lm")

def v_equation(d, v, t, dur):
    title(d, v.get("title"), t)
    lines = v["lines"]
    y0 = 560 - (len(lines) - 1) * 75
    for i, ln in enumerate(lines):
        a = ease((t - 0.45 * i) / 0.45)
        text_c(d, (CX, y0 + i * 150 + 20 * (1 - a)), ln["text"], font(ln.get("size", 96), "Black"),
               col(ln.get("color", "text"), a))

def v_cta(d, v, t, dur):
    for i, ln in enumerate(v["lines"]):
        a = ease((t - 0.35 * i) / 0.45)
        text_c(d, (CX, 430 + i * 140), ln, font(110, "Black"), col("gold" if i else "text", a))
    if v.get("sub"):
        a = ease((t - 0.8) / 0.45)
        rrect(d, [CX - 420, 700, CX + 420, 800], 50, fill=col("green", 0.9 * a))
        text_c(d, (CX, 750), v["sub"], font(44, "Bold"), col("bg0", a))

def v_line(d, v, t, dur):
    """Landscape line chart (reuses portrait logic by drawing into a scaled box)."""
    title(d, v.get("title"), t)
    xs, series = v["x"], v["series"]
    ticks = R.nice_ticks(max(max(s["values"]) for s in series))
    mx = ticks[-1] * 1.04
    L, Rr, T, B = 360, 1620, 300, 840
    X = lambda x: L + (x - xs[0]) / (xs[-1] - xs[0]) * (Rr - L)
    Y = lambda y: B - y / mx * (B - T)
    for val in ticks:
        d.line([(L, Y(val)), (Rr, Y(val))], fill=col("grid"), width=2)
        text_c(d, (L - 20, Y(val)), fmt(val, v.get("format")),
               font(32, "Medium", False), col("muted"), anchor="rm")
    d.line([(L, B), (Rr, B)], fill=col("muted"), width=3)
    step = max(1, len(xs) // 8)
    for x in xs[::step]:
        text_c(d, (X(x), B + 40), str(x), font(32, "Medium", False), col("muted"))
    p = ease(t / max(0.8, min(3, dur * 0.6)))
    xmax = xs[0] + (xs[-1] - xs[0]) * p
    for s in series:
        c = s.get("color", "green")
        pts = [(X(x), Y(y)) for x, y in zip(xs, s["values"]) if x <= xmax]
        if len(pts) >= 2:
            d.line(pts, fill=col(c), width=8, joint="curve")
            ex, ey = pts[-1]
            d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=col(c))
            if p > 0.98:
                text_c(d, (ex - 20, ey - 30), s["label"], font(36, "Bold"), col(c), anchor="rb")

def v_count(d, v, t, dur):
    """Big number that counts up: {to, prefix, suffix, dp, label, sub, color, from}."""
    title(d, v.get("title"), t)
    p = ease(t / max(0.8, min(2.2, dur * 0.5)))
    val = v.get("from", 0) + (v["to"] - v.get("from", 0)) * p
    s = f"{v.get('prefix', '')}{val:,.{v.get('dp', 0)}f}{v.get('suffix', '')}"
    a = ease(t / 0.4)
    text_c(d, (CX, 540), s, font(230, "Black"), col(v.get("color", "gold"), a))
    text_c(d, (CX, 720), v.get("label", ""), font(52, "SemiBold", False), col("text", a))
    if v.get("sub"):
        text_c(d, (CX, 790), v["sub"], font(38, "Medium", False), col("muted", a))

def v_waterfall(d, v, t, dur):
    """Revenue -> minus costs -> result. steps: [{label, value, kind: start|minus|plus|total, color?}]"""
    title(d, v.get("title"), t)
    steps = v["steps"]
    run, tops = 0, []
    for s in steps:
        if s["kind"] in ("start", "total"):
            lo, hi = 0, s["value"]; run = s["value"]
        elif s["kind"] == "minus":
            lo, hi = run - s["value"], run; run -= s["value"]
        else:
            lo, hi = run, run + s["value"]; run += s["value"]
        tops.append((lo, hi))
    mx = max(h for _, h in tops)
    n = len(steps)
    L, Rr, T, B = 260, 1660, 300, 800
    bw = (Rr - L) / n * 0.62
    Y = lambda val: B - val / mx * (B - T)
    d.line([(L - 40, B), (Rr + 40, B)], fill=col("muted"), width=3)
    per = max(0.5, (dur - 1.0) / n)
    for i, (s, (lo, hi)) in enumerate(zip(steps, tops)):
        p = ease((t - per * i) / 0.6)
        if p <= 0:
            continue
        x = L + (i + 0.5) * (Rr - L) / n
        c = s.get("color") or {"start": "blue", "minus": "red", "plus": "green", "total": "gold"}[s["kind"]]
        if s["kind"] == "minus":   # grows downward from previous top
            y1, y2 = Y(hi), Y(hi - (hi - lo) * p)
        else:
            y1, y2 = Y(lo + (hi - lo) * p), Y(lo)
        if abs(y2 - y1) < 3:
            y2 = y1 + 3
        rrect(d, [x - bw / 2, y1, x + bw / 2, y2], 10, fill=col(c, 0.92))
        if i + 1 < n and p > 0.95:
            nxt = run_y = Y(hi if s["kind"] != "minus" else lo)
            d.line([(x + bw / 2, nxt), (x + bw / 2 + (Rr - L) / n - bw, run_y)], fill=col("dim"), width=2)
        lab = s.get("display") or ("−" if s["kind"] == "minus" else "") + fmt(s["value"], v.get("format"))
        text_c(d, (x, min(y1, y2) - 34), lab, font(42, "Black"), col("text", p))
        text_c(d, (x, B + 42), s["label"], font(34, "SemiBold", False), col("muted", p))

def v_donut(d, v, t, dur):
    """segments: [{label, value, color}], center (text), center_sub."""
    title(d, v.get("title"), t)
    segs = v["segments"]
    tot = sum(s["value"] for s in segs)
    cx, cy, r, wdt = 640, 570, 270, 90
    p = ease(t / 1.4)
    start = -90.0
    for s in segs:
        sweep = 360 * s["value"] / tot * p
        if sweep > 0.3:
            d.arc([cx - r, cy - r, cx + r, cy + r], start, start + sweep, fill=col(s.get("color", "green")), width=wdt)
        start += sweep
    a = ease((t - 0.6) / 0.5)
    text_c(d, (cx, cy - 10), v.get("center", ""), font(76, "Black"), col("text", a))
    if v.get("center_sub"):
        text_c(d, (cx, cy + 55), v["center_sub"], font(32, "Medium", False), col("muted", a))
    for i, s in enumerate(segs):
        a = ease((t - 0.5 - 0.3 * i) / 0.4)
        y = 570 - (len(segs) - 1) * 65 + i * 130
        d.ellipse([1060, y - 20, 1100, y + 20], fill=col(s.get("color", "green"), a))
        pct = s.get("display") or f"{s['value'] / tot * 100:.{v.get('dp', 0)}f}%"
        text_c(d, (1130, y - 2), pct, font(56, "Black"), col(s.get("color", "green"), a), anchor="lm")
        text_c(d, (1330, y - 2), s["label"], font(40, "SemiBold", False), col("text", a), anchor="lm")

def v_columns(d, v, t, dur):
    """Vertical columns: items [{label, value, color?, display?}], optional highlight index."""
    title(d, v.get("title"), t)
    items = v["items"]
    n = len(items)
    mx = max(i["value"] for i in items) * 1.08
    L, Rr, T, B = 240, 1680, 330, 800
    slot = (Rr - L) / n
    bw = min(170, slot * 0.6)
    d.line([(L - 20, B), (Rr + 20, B)], fill=col("muted"), width=3)
    for i, it in enumerate(items):
        p = ease((t - 0.12 * i) / 0.9)
        x = L + (i + 0.5) * slot
        h = (B - T) * it["value"] / mx * p
        c = it.get("color") or ("gold" if i == v.get("highlight") else v.get("color", "green"))
        if h > 2:
            rrect(d, [x - bw / 2, B - h, x + bw / 2, B], min(14, bw / 4), fill=col(c, 0.92))
        lab = it.get("display") or fmt(it["value"] * p if p < 0.999 else it["value"], v.get("format"))
        fs = 40 if n <= 8 else 30
        text_c(d, (x, B - h - 32), lab, font(fs, "Black"), col("text", min(1, p * 2)))
        text_c(d, (x, B + 40), str(it["label"]), font(32 if n <= 10 else 26, "SemiBold", False), col("muted"))
    if v.get("note"):
        text_c(d, (CX, B + 100), v["note"], font(32, "Medium", False), col("dim", ease((t - 1) / 0.5)))

def v_versus(d, v, t, dur):
    """Two cards: left/right {label, value, sub, color}; optional verdict line."""
    title(d, v.get("title"), t)
    cw, ch, y0 = 640, 440, 320
    for i, side in enumerate(("left", "right")):
        it = v[side]
        a = ease((t - 0.35 * i) / 0.5)
        x0 = CX - 60 - cw if i == 0 else CX + 60
        c = it.get("color", "green" if i else "blue")
        y = y0 + 30 * (1 - a)
        rrect(d, [x0, y, x0 + cw, y + ch], 36, fill=col(c, 0.10 * a), outline=col(c, 0.8 * a), width=4)
        text_c(d, (x0 + cw / 2, y + 80), it["label"], font(46, "Bold"), col("text", a))
        text_c(d, (x0 + cw / 2, y + 220), it["value"], font(120 if len(it["value"]) < 8 else 88, "Black"), col(c, a))
        if it.get("sub"):
            text_c(d, (x0 + cw / 2, y + 345), it["sub"], font(34, "Medium", False), col("muted", a))
    a = ease((t - 0.2) / 0.4)
    text_c(d, (CX, y0 + ch / 2), "vs", font(54, "Black"), col("dim", a))
    if v.get("verdict"):
        text_c(d, (CX, y0 + ch + 70), v["verdict"], font(46, "Bold"), col("gold", ease((t - 1.0) / 0.5)))

def v_timeline(d, v, t, dur):
    """Horizontal milestones: events [{when, text, color?}]."""
    title(d, v.get("title"), t)
    ev = v["events"]
    n = len(ev)
    L, Rr, y = 220, 1700, 560
    p = ease(t / max(1.0, dur * 0.7))
    d.line([(L, y), (L + (Rr - L) * p, y)], fill=col("dim"), width=6)
    for i, e in enumerate(ev):
        x = L + (Rr - L) * (i / (n - 1) if n > 1 else 0.5)
        a = ease((p * (Rr - L) - (x - L)) / 120 + 1) if n > 1 else ease(t / 0.5)
        c = e.get("color", "green")
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=col(c, a))
        up = i % 2 == 0
        text_c(d, (x, y + (-80 if up else 80)), e["when"], font(48, "Black"), col(c, a))
        for j, ln in enumerate(e["text"].split("\n")):
            yy = y + (-150 - 44 * (len(e["text"].split("\n")) - 1 - j) if up else 140 + 44 * j)
            text_c(d, (x, yy), ln, font(34, "SemiBold", False), col("text", a))

def v_quote(d, v, t, dur):
    """Big statement with a source line: {text (\\n allowed), source, color}."""
    title(d, v.get("title"), t)
    lines = v["text"].split("\n")
    y0 = 540 - (len(lines) - 1) * 60
    for i, ln in enumerate(lines):
        a = ease((t - 0.3 * i) / 0.5)
        text_c(d, (CX, y0 + i * 120), ln, font(86, "Black"), col(v.get("color", "text") if i else v.get("first_color", v.get("color", "text")), a))
    d.rectangle([CX - 60, y0 - 130, CX + 60, y0 - 124], fill=col("green", ease(t / 0.5)))
    if v.get("source"):
        text_c(d, (CX, y0 + len(lines) * 120 + 20), v["source"], font(34, "Medium", False),
               col("muted", ease((t - 0.8) / 0.5)))

def v_table(d, v, t, dur):
    """Simple table: header [..], rows [[..]], highlight_col optional."""
    title(d, v.get("title"), t)
    hdr, rows = v["header"], v["rows"]
    nc = len(hdr)
    L, Rr = 260, 1660
    cw = (Rr - L) / nc
    y0, rh = 330, min(110, 480 / max(1, len(rows)))
    a = ease(t / 0.4)
    for j, h in enumerate(hdr):
        text_c(d, (L + (j + 0.5) * cw, y0), h, font(40, "Bold"), col("muted", a))
    d.line([(L, y0 + 40), (Rr, y0 + 40)], fill=col("dim", a), width=3)
    for i, row in enumerate(rows):
        a = ease((t - 0.3 - 0.25 * i) / 0.4)
        y = y0 + 40 + (i + 0.6) * rh
        hl = v.get("highlight_row") == i
        if hl:
            rrect(d, [L - 20, y - rh / 2 + 6, Rr + 20, y + rh / 2 - 6], 18, fill=col("gold", 0.12 * a))
        for j, cell in enumerate(row):
            c = "gold" if hl else ("text" if j == 0 else v.get("col_colors", {}).get(str(j), "text"))
            text_c(d, (L + (j + 0.5) * cw, y), str(cell), font(50 if j else 44, "Black" if j else "Bold"), col(c, a))

_lc = {}   # per-render caches for photo scenes (tiles, shadows, cut-out layers, panels)

def _count_text(s, p):
    """'$1.2B' at progress p -> '$0.6B' etc. Only money/percent/multiplier values count up (not years)."""
    import re
    m = re.match(r"^(.*?)(\d[\d,]*\.?\d*)(.*)$", s)
    if not m or p >= 0.999 or not re.search(r"[$₹€£%xXKMBT]", m.group(1) + m.group(3)):
        return s
    pre, num, suf = m.groups()
    dp = len(num.split(".")[1]) if "." in num else 0
    val = float(num.replace(",", "")) * p
    return pre + (f"{val:,.{dp}f}" if "," in num else f"{val:.{dp}f}") + suf

def _value_reveal(d, v, cx, y, t, max_w, size=150, anchor="mm", underline=True):
    """Big number that counts up and settles, with a gold underline growing under it."""
    if not v.get("value"):
        return y
    b = ease((t - 0.25) / 0.5)
    p = ease((t - 0.25) / 1.1)
    f, size = R.fit_font(v["value"], max_w, size, min_size=70, step=10)
    s = _count_text(v["value"], p) if v.get("count", True) else v["value"]
    c = v.get("color", "gold")
    text_c(d, (cx, y + 18 * (1 - b)), s, f, col(c, b), anchor=anchor)
    wfull = f.getlength(v["value"])
    uw = min(wfull, 260) * ease((t - 0.7) / 0.6) if underline else 0
    ux = cx - uw / 2 if anchor == "mm" else cx
    uy = y + size * 0.56
    if uw > 2:
        rrect(d, [ux, uy, ux + uw, uy + 10], 5, fill=col(c, 0.9 * b))
    return uy + 80

def _kb_tile(path, w, h, focus, zoom, r):
    """Rounded photo tile with a slow push-in (Ken Burns); the corner mask is cached."""
    tile = R.cover(R.load_photo(path), w, h, focus, zoom).convert("RGBA")
    key = ("mask", w, h, r)
    if key not in _lc:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
        _lc[key] = m
    tile.putalpha(_lc[key])
    return tile

def _soft_shadow(w, h, r, blur=28, alpha=150):
    key = ("shadow", w, h, r, blur, alpha)
    if key not in _lc:
        pad = blur * 2
        sh = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=(0, 0, 0, alpha))
        _lc[key] = (sh.filter(ImageFilter.GaussianBlur(blur)), pad)
    return _lc[key]

def _fade(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda q: int(q * a)))
    return im

def _credit(d, path, x, y, a, anchor="rb"):
    c = R.photo_credit(path)
    if c:
        d.text((x, y), c, font=font(20, "Medium", False), fill=col("text", 0.8 * a), anchor=anchor,
               stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))

def _panel(box, color="green"):
    """Soft brand-coloured stage for a cut-out: rounded, faint vertical gradient, thin border, inner glow."""
    key = ("panel", box, color)
    if key not in _lc:
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        c = np.array(R.COLORS[color], np.float32)
        yy = np.linspace(0, 1, h)[:, None, None]
        top, bot = np.array(R.COLORS["bg1"], np.float32) * 0.6 + c * 0.4 * 0.55, np.array(R.COLORS["bg0"], np.float32)
        arr = (top + (bot - top) * yy).repeat(w, 1)
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
        im.alpha_composite(R.radial(w, h, w / 2, h * 0.42, w * 0.42, h * 0.5, color, 0.28))
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=255)
        im.putalpha(m)
        ImageDraw.Draw(im).rounded_rectangle([1, 1, w - 2, h - 2], 40, outline=col(color, 0.45), width=3)
        _lc[key] = im
    return _lc[key]

def _cut_scene_layer(path, h):
    key = ("cut", path, int(h))
    if key not in _lc:
        c = R.grade(R.fit_height(R.load_cutout(path), h), k=0.08, sat=1.05, con=1.04)
        lay, pad = R.rim(c, 3, (255, 255, 255), 0.35, 26, R.COLORS["bg0"], 0.55, R.cutout_open(path))
        _lc[key] = (lay, pad)
    return _lc[key]

def v_photo(d, v, t, dur):
    """Real photo with text. v: {"type": "photo", "file", "title"?, "value"?, "color"?, "label"?, "sub"?,
    "layout": "side" (photo left, text right; default) | "full" (wide photo, value over it) |
              "cutout" (person cut out over a soft brand panel; also chosen by "cutout": true),
    "focus"?: [fx, fy], "count"?: false (don't count the value up)}.
    All layouts push in slowly (Ken Burns); values count up with a gold underline."""
    title(d, v.get("title"), t)
    a = ease(t / 0.5)
    focus = tuple(v.get("focus", (0.5, 0.4)))
    zoom = 1.0 + 0.06 * min(1.0, max(0.0, t) / max(dur, 4.0))
    img = d._image
    layout = "cutout" if v.get("cutout") and v.get("layout", "cutout") in ("cutout", "side") else v.get("layout", "side")
    if layout == "full":
        x0, y0, x1, y1 = 150, TOP - 10, W - 150, BOT - 20
        dy = int(20 * (1 - a))
        sh, pad = _soft_shadow(x1 - x0, y1 - y0, 30)
        R.overlay(img, _fade(sh, a), x0 - pad, y0 + dy - pad + 14)
        tile = _kb_tile(v["file"], x1 - x0, y1 - y0, focus, zoom, 30)
        if v.get("value") or v.get("label"):     # soft dark scrim at the bottom so the number reads cleanly
            key = ("scrim", x1 - x0, y1 - y0)
            if key not in _lc:
                hh = y1 - y0
                g = np.clip((np.arange(hh) - hh * 0.45) / (hh * 0.55), 0, 1) ** 1.3 * 0.85
                lay = np.zeros((hh, x1 - x0, 4), np.uint8); lay[..., :3] = R.COLORS["bg0"]
                lay[..., 3] = (g[:, None].repeat(x1 - x0, 1) * 255).astype(np.uint8)
                _lc[key] = Image.fromarray(lay, "RGBA")
            sc = _lc[key].copy(); sc.putalpha(Image.fromarray(np.minimum(np.asarray(sc.getchannel("A")), np.asarray(tile.getchannel("A")))))
            tile.alpha_composite(sc)
        R.overlay(img, _fade(tile, a), x0, y0 + dy)
        d.rounded_rectangle([x0, y0 + dy, x1, y1 + dy], 30, outline=col("text", 0.18 * a), width=3)
        _credit(d, v["file"], x1 - 16, y0 + dy + 34, a)
        yv = y1 - 150
        if v.get("value"):
            _value_reveal(d, v, x0 + 60, yv, t, x1 - x0 - 120, 150, anchor="lm", underline=False)
        if v.get("label"):
            text_c(d, (x0 + 62, y1 - 55), v["label"], font(46, "Bold"), col("text", ease((t - 0.35) / 0.5)), anchor="lm")
        return
    if layout == "cutout":
        pop = 90 if v.get("title") else 150               # head pops out above the panel (clear of the title)
        ph = (BOT - 340) + pop
        c0 = R.load_cutout(v["file"])
        pw = int(min(880, max(620, c0.width * ph / c0.height + 110)))
        box = (1000 - pw, 340, 1000, BOT)
        panel = _panel(box, v.get("panel_color", "green"))
        dy = int(30 * (1 - a))
        R.overlay(img, _fade(panel, a), box[0], box[1] + dy)
        lay, pad = _cut_scene_layer(v["file"], ph)
        s = zoom
        lay2 = lay.resize((int(lay.width * s), int(lay.height * s)), Image.BILINEAR) if s > 1.001 else lay
        cx = (box[0] + box[2]) / 2
        top = box[3] - ph * s + dy
        # clip at the panel's bottom edge
        cut_h = int(box[3] + dy - (top - pad * s))
        lay2 = lay2.crop((0, 0, lay2.width, max(1, min(lay2.height, cut_h))))
        op = R.cutout_open(v["file"])
        x = cx - lay2.width / 2
        if "r" in op:                  # photo crops the person on the right: make that edge the panel's edge
            x = box[2] - (lay2.width - pad * s)
            lay2 = lay2.crop((0, 0, max(1, int(box[2] - x)), lay2.height))
        elif "l" in op:
            x = box[0] - pad * s
            lay2 = lay2.crop((int(pad * s), 0, lay2.width, lay2.height)); x += int(pad * s)
        R.overlay(img, _fade(lay2, ease((t - 0.1) / 0.5)), x, top - pad * s)
        _credit(d, v["file"], box[2] - 20, box[3] + dy - 16, a)
        rx = 1460
    else:
        x0, y0, x1, y1 = 110, TOP - 10, 1060, BOT - 10
        dx = int(30 * (1 - a))
        sh, pad = _soft_shadow(x1 - x0, y1 - y0, 30)
        R.overlay(img, _fade(sh, a), x0 - dx - pad, y0 - pad + 14)
        R.overlay(img, _fade(_kb_tile(v["file"], x1 - x0, y1 - y0, focus, zoom, 30), a), x0 - dx, y0)
        d.rounded_rectangle([x0 - dx, y0, x1 - dx, y1], 30, outline=col("text", 0.18 * a), width=3)
        _credit(d, v["file"], x1 - dx - 16, y1 - 14, a)
        rx = 1490
    b = ease((t - 0.25) / 0.5)
    y = 470 if v.get("value") else 520
    if v.get("value"):
        y = _value_reveal(d, v, rx, y, t, 760, 150)
    if v.get("label"):
        for i, ln in enumerate(R._wrap(v["label"], font(50, "Bold"), 760)[:3]):
            text_c(d, (rx, y + i * 62), ln, font(50, "Bold"), col("text", b))
        y += 62 * min(3, len(R._wrap(v["label"], font(50, "Bold"), 760))) + 20
    if v.get("sub"):
        for i, ln in enumerate(R._wrap(v["sub"], font(36, "Medium", False), 760)[:3]):
            text_c(d, (rx, y + i * 46), ln, font(36, "Medium", False), col("muted", b))

VISUALS = dict(chapter=v_chapter, title=v_title, stat=v_stat, stat_grid=v_stat_grid, hbars=v_hbars,
               share=v_share, flywheel=v_flywheel, bullets=v_bullets, equation=v_equation,
               cta=v_cta, line=v_line, count=v_count, waterfall=v_waterfall, donut=v_donut,
               columns=v_columns, versus=v_versus, timeline=v_timeline, quote=v_quote, table=v_table,
               photo=v_photo)

# ------------------------------------------------------------------ captions
def draw_caps(img, chunks, t):
    d = ImageDraw.Draw(img)
    for ch in chunks:
        if ch[0][1] - 0.05 <= t < ch[-1][2] + 0.05:
            f = font(52, "Bold")
            words = [w[0] for w in ch]
            sp = f.getlength(" ")
            widths = [f.getlength(w) for w in words]
            x = CX - (sum(widths) + sp * (len(words) - 1)) / 2
            for (w, s, e), wd in zip(ch, widths):
                d.text((x, CAP_Y), w, font=f, fill=col("gold") if s <= t < e else col("text"),
                       anchor="lm", stroke_width=6, stroke_fill=(0, 0, 0, 255))
                x += wd + sp
            break

def _photo_thumb(spec, out_dir, th, img):
    """Bold photo thumbnail: real photo on the right, fading into the dark background; huge number left."""
    from PIL import ImageEnhance
    tp = th["photo"]
    ph = R.cover(R.load_photo(tp["file"]), 760, 720, tuple(tp.get("focus", (0.5, 0.35))))
    ph = ImageEnhance.Contrast(ImageEnhance.Color(ph).enhance(1.25)).enhance(1.12).convert("RGBA")
    fade = np.clip(np.linspace(-0.2, 1.6, 760), 0, 1)[None, :].repeat(720, 0)
    ph.putalpha(Image.fromarray((fade * 255).astype(np.uint8), "L"))
    img.alpha_composite(ph, (520, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1279, 719], outline=col(th.get("color", "gold")), width=14)
    lx = 330
    size = 230
    while font(size, "Black").getlength(th["big"]) > 600 and size > 100:
        size -= 10
    text_c(d, (lx + 8, 250 + 8), th["big"], font(size, "Black"), (0, 0, 0, 160))
    text_c(d, (lx, 250), th["big"], font(size, "Black"), col(th.get("color", "gold")), stroke=12, stroke_fill=(0, 0, 0, 255))
    fsz = 80
    while True:
        lines = R._wrap(th["line"], font(fsz, "Black"), 600)
        if len(lines) <= 2 or fsz <= 54:
            break
        fsz -= 6
    for i, ln in enumerate(lines[:2]):
        text_c(d, (lx, 430 + i * fsz * 1.08), ln, font(fsz, "Black"), col("text"), stroke=8, stroke_fill=(0, 0, 0, 255))
    if th.get("tag"):
        f = font(44, "Black")
        tw = f.getlength(th["tag"]) + 56
        rrect(d, [lx - tw / 2, 610, lx + tw / 2, 690], 20, fill=col(th.get("tag_color", "green")))
        text_c(d, (lx, 650), th["tag"], f, col("bg0"))
    img.convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb.png"))

# ------------------------------------------------------------------ styled thumbnails (spec["thumbnail"]["style"])
# Inputs: big (number/short phrase), line (2-5 words), tag, photo {file, focus, zoom?}, cutout (bool; or
# photo.cutout), color (accent; default gold, red when big starts with "-"), trend ("up"/"down"; default from big).
# A "Spotlight": person cut out on a clean navy stage with a soft accent glow; text left.
# B "Colour block": solid accent panel (navy text) on the left; person/photo/chart on the right.
# C "Cinematic": full-bleed real photo, softly graded into the palette (person kept sharp, backdrop blurred).
TW, TH = 1280, 720
CAP = 0.727            # Inter cap height / em

def _tbg(glows=(), vignette=0.55):
    y = np.linspace(0, 1, TH)[:, None, None]
    b0, b1 = np.array(R.COLORS["bg0"], np.float32), np.array(R.COLORS["bg1"], np.float32)
    base = b1 + (b0 - b1) * y
    img = Image.fromarray(np.clip(base.repeat(TW, 1), 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    for g in glows:
        img.alpha_composite(R.radial(TW, TH, *g))
    if vignette:
        yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
        v = np.clip(((xx / TW - 0.5) ** 2 + (yy / TH - 0.5) ** 2) * 2.2 - 0.15, 0, 1) * vignette
        lay = np.zeros((TH, TW, 4), np.uint8); lay[..., :3] = R.COLORS["bg0"]; lay[..., 3] = (v * 255).astype(np.uint8)
        img.alpha_composite(Image.fromarray(lay, "RGBA"))
    return img

_tparts = R.thumb_parts
_text_block = R.text_block

def _cutout_layer(path, h, max_w, glow_color, rim_a=0.5, glow=24, glow_a=0.65, canvas_bottom=None, top=0):
    """Cut-out person scaled to height h (or max_w wide), with a thin light rim and a soft accent glow."""
    c = R.load_cutout(path)
    if c.width * h / c.height > max_w:
        h = c.height * max_w / c.width
    c = R.grade(R.fit_height(c, h), k=0.08, sat=1.06, con=1.04)
    lay, pad = R.rim(c, 3, (255, 255, 255), rim_a, glow, R.COLORS.get(glow_color, glow_color), glow_a, R.cutout_open(path))
    if "b" in R.cutout_open(path) and canvas_bottom is not None and top + h < canvas_bottom + 4:
        lay = R.fade_bottom(lay, 0.0, start=pad + h * 0.78)       # photo crops the body above the frame edge
    return lay, pad

def _place_cutout(img, lay, pad, path, cx, top, right_edge=None):
    """Put a cut-out layer centred on cx; if the photo crops the person at the side, push that side
    off the canvas edge (or fade it) so no straight cut line shows."""
    op = R.cutout_open(path)
    right_edge = img.width if right_edge is None else right_edge
    x = cx - lay.width / 2
    if "r" in op and x + lay.width - pad < right_edge:
        x = right_edge - (lay.width - pad)
    if "l" in op and ("r" not in op or x + pad > 0):
        a = np.asarray(lay.getchannel("A"), np.float32)
        ramp = np.clip((np.arange(lay.width) - pad) / (0.22 * (lay.width - 2 * pad)), 0, 1)[None, :]
        lay = lay.copy(); lay.putalpha(Image.fromarray((a * ramp).astype(np.uint8)))
    R.overlay(img, lay, x, top - pad)

def _subject(img, th, kind, path, box, accent, trend, style):
    """Draw the subject (cut-out person / photo / chart) into box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    tp = th.get("photo") or {}
    focus = tuple(tp.get("focus", (0.5, 0.4)))
    zoom = tp.get("zoom", 1.0)
    if kind == "cutout":
        h = (y1 - y0) * zoom
        lay, pad = _cutout_layer(path, h, (x1 - x0) * 1.05, "green" if style != "B" else "text",
                                 glow_a=0.55 if style != "B" else 0.35, canvas_bottom=TH, top=y0)
        _place_cutout(img, lay, pad, path, (x0 + x1) / 2, y0)
    elif kind == "photo":
        w, h = int((x1 - x0) * 0.86), int((y1 - y0) * 0.7)
        lay, pad = R.card(R.load_photo(path), w, h, focus, r=24, border=8, tilt=-3.5, shadow=26)
        R.overlay(img, lay, (x0 + x1) / 2 - lay.width / 2, (y0 + y1) / 2 - lay.height / 2)
    else:
        w, h = int(x1 - x0), int(y1 - y0)
        R.overlay(img, R.trend_graphic(w, h, trend, "green" if trend == "up" else "red"), x0, y0)

def thumb_image(th):
    """Styled long-video thumbnail (1280x720 RGBA) for th["style"] in A/B/C."""
    style = str(th.get("style", "A")).upper()
    big, line, tag, trend, accent = _tparts(th)
    kind, path = R.thumb_subject(th)
    tone = "green" if trend == "up" else "red"
    if style == "B":
        txt = "bg0"
        img = _tbg([(940, 360, 420, 380, tone, 0.22)], vignette=0.35)
        if kind == "photo":
            tp = th["photo"]
            ph = R.grade(R.cover(R.load_photo(path), TW - 530, TH, tuple(tp.get("focus", (0.5, 0.4)))), k=0.3).convert("RGBA")
            img.alpha_composite(ph, (530, 0))
        else:
            _subject(img, th, kind, path, (600, 40 if kind == "cutout" else 120, 1250, TH if kind == "cutout" else 640),
                     accent, trend, "B")
        panel = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        pd.polygon([(0, 0), (600, 0), (520, TH), (0, TH)], fill=col(accent))
        sh = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        ImageDraw.Draw(sh).polygon([(0, 0), (612, 0), (532, TH), (0, TH)], fill=(0, 0, 0, 140))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
        img.alpha_composite(panel)
        _text_block(img, th, 52, 360, 470, txt, txt, tag_fill="bg0", tag_text=accent, big_max=210,
                    sizes=(78, 72, 66, 60, 54, 50), max_lines=2, shadow=0)
    elif style == "C":
        if kind in ("cutout", "photo"):
            tp = th["photo"]
            focus = tuple(tp.get("focus", (0.5, 0.4)))
            src = R.load_photo(path)
            if kind == "cutout":   # the photo's own backdrop (person painted out, blurred, dimmed) + sharp person
                back = R.remove_person(path, (TW, TH), focus, zoom=1.1)
                img = R.grade(back, k=0.75, sat=0.55, con=0.9).convert("RGBA")
            else:                  # photo on the right, fading into navy under the text
                img = _tbg([], vignette=0.3)
                pw = 860
                ph = R.grade(R.cover(src, pw, TH, focus), k=0.25).convert("RGBA")
                ramp = np.clip(np.arange(pw) / 320, 0, 1) ** 1.4
                ph.putalpha(Image.fromarray((ramp[None, :].repeat(TH, 0) * 255).astype(np.uint8)))
                img.alpha_composite(ph, (TW - pw, 0))
        else:
            img = _tbg([(980, 380, 380, 300, tone, 0.30)], vignette=0.3)
            _subject(img, th, kind, path, (560, 110, 1240, 600), accent, trend, "C")
        # left-to-right navy gradient so the text always reads
        g = np.clip(1.05 - np.linspace(0, 1, TW) / 0.62, 0, 0.92) ** 1.2
        lay = np.zeros((TH, TW, 4), np.uint8); lay[..., :3] = R.COLORS["bg0"]
        lay[..., 3] = (g[None, :].repeat(TH, 0) * 255).astype(np.uint8)
        img.alpha_composite(Image.fromarray(lay, "RGBA"))
        bot = np.clip((np.linspace(0, 1, TH) - 0.7) / 0.3, 0, 1)[:, None] * 0.5
        lay2 = np.zeros((TH, TW, 4), np.uint8); lay2[..., :3] = R.COLORS["bg0"]
        lay2[..., 3] = (bot.repeat(TW, 1) * 255).astype(np.uint8)
        img.alpha_composite(Image.fromarray(lay2, "RGBA"))
        if kind == "cutout":
            lay, pad = _cutout_layer(path, 690 * th["photo"].get("zoom", 1.0), 660, "bg0", rim_a=0.0,
                                     glow=30, glow_a=0.7, canvas_bottom=TH, top=40)
            _place_cutout(img, lay, pad, path, 950, 40)
        _text_block(img, th, 60, 380, 560, accent, cue=(trend, tone) if kind != "graphic" else None)
        ImageDraw.Draw(img).rectangle([0, TH - 10, TW, TH], fill=col(accent))
    else:  # A
        img = _tbg([(930, 400, 400, 360, "green" if kind == "cutout" else tone, 0.30),
                    (1100, 120, 260, 200, accent, 0.10)])
        d = ImageDraw.Draw(img)
        for gx in range(0, TW, 64):     # faint grid, like the videos
            d.line([(gx, 0), (gx, TH)], fill=col("grid", 0.22))
        for gy in range(0, TH, 64):
            d.line([(0, gy), (TW, gy)], fill=col("grid", 0.22))
        box = (640, 40, 1250, TH) if kind == "cutout" else ((700, 90, 1260, 640) if kind == "photo" else (660, 130, 1240, 600))
        _subject(img, th, kind, path, box, accent, trend, "A")
        _text_block(img, th, 64, 370, 580 if kind == "photo" else 600, accent, big_max=250,
                    cue=(trend, tone) if kind != "graphic" else None)
    return img

def make_thumb(spec, out_dir):
    th = spec.get("thumbnail")
    if not th:
        return
    if th.get("style"):
        thumb_image(th).convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb.png"))
        return
    img = Image.new("RGBA", (1280, 720))
    bg = background().resize((1440, 810)).crop((80, 45, 1360, 765))
    img.alpha_composite(bg)
    if th.get("photo"):
        return _photo_thumb(spec, out_dir, th, img)
    d = ImageDraw.Draw(img)
    text_c(d, (640, 300), th["big"], font(250, "Black"), col(th.get("color", "gold")),
           stroke=8, stroke_fill=(0, 0, 0, 255))
    text_c(d, (640, 520), th["line"], font(92, "Black"), col("text"), stroke=6, stroke_fill=(0, 0, 0, 255))
    if th.get("tag"):
        f = font(48, "Black")
        tw = f.getlength(th["tag"]) + 60
        rrect(d, [640 - tw / 2, 596, 640 + tw / 2, 684], 22, fill=col(th.get("tag_color", "green")))
        text_c(d, (640, 640), th["tag"], f, col("bg0"))
    img.convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb.png"))

def render(spec_path, out_dir):
    spec = json.load(open(spec_path))
    spec.setdefault("tail", 16.0)   # hold the closing scene so YouTube end screens (5-20 s) have room
    R.DEFAULT_FMT = spec.get("currency", "usd")
    os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "work_" + spec["id"]); os.makedirs(work, exist_ok=True)
    audio, tl, total = R.build_audio(spec, work)
    asr = R.asr_words(audio)
    caps = []
    for sc, seg in zip(spec["scenes"], tl):
        caps += R.chunk_words(R.digit_captions(R.caption_fix(R.align_words(sc["say"], seg, asr), spec.get("caption_fix"))), max_chars=40, max_words=7)
    # chapters for the description
    lines = ["0:00 " + spec.get("intro_chapter", "Intro")]
    for sc, seg in zip(spec["scenes"], tl):
        if sc["visual"]["type"] == "chapter":
            s = int(seg["start"])
            lines.append(f"{s // 60}:{s % 60:02d} {sc['visual']['title']}")
    open(os.path.join(out_dir, spec["id"] + "_chapters.txt"), "w").write("\n".join(lines) + "\n")
    make_thumb(spec, out_dir)
    bg = background()
    out = os.path.join(out_dir, spec["id"] + ".mp4")
    tmp_out = out[:-4] + ".partial.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp_out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    for fi in range(nframes):
        t = fi / FPS
        si = max(i for i, seg in enumerate(tl) if t >= seg["start"] - 0.1 or i == 0)
        seg, sc = tl[si], spec["scenes"][si]
        ox = int(120 + 100 * math.sin(t / 9)); oy = int(70 + 50 * math.cos(t / 11))
        img = bg.crop((ox, oy, ox + W, oy + H))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        if spec.get("badge"):
            text_c(d, (100, 70), spec["badge"], font(30, "Bold"), col("green"), anchor="lm")
        if spec.get("disclaimer"):
            text_c(d, (W - 100, 70), spec["disclaimer"], font(26, "Medium", False), col("muted"), anchor="rm")
        VISUALS[sc["visual"]["type"]](d, sc["visual"], t - (seg["start"] - 0.25) + (0.6 if si == 0 else 0), seg["end"] - seg["start"])
        img.alpha_composite(layer)
        draw_caps(img, caps, t)
        ImageDraw.Draw(img).rectangle([0, H - 6, W * t / total, H], fill=col("green"))
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0 or not os.path.getsize(tmp_out):
        raise SystemExit(f"ffmpeg failed for {spec['id']}; no video written")
    os.replace(tmp_out, out)
    json.dump({"timeline": tl, "duration": total}, open(os.path.join(work, "timeline.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    print(render(sys.argv[1], sys.argv[2]))
