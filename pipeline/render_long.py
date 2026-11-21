"""Render a long-form 16:9 (1920x1080) video from a JSON spec.

Usage: python3 render_long.py spec.json out_dir

Reuses audio, ASR caption sync and drawing helpers from render.py.
Scene visual types: chapter, stat, stat_grid, hbars, share, flywheel, bullets,
equation, line, cta, title.
Writes <id>.mp4, <id>_chapters.txt (YouTube chapters) and <id>_thumb.png.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
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
    text_c(d, (CX, 430 - 20 * (1 - a)), f"CHAPTER {v['n']}", font(40, "Bold"), col("green", a))
    text_c(d, (CX, 540), v["title"], font(110, "Black"), col("text", a))
    w = 600 * ease((t - 0.2) / 0.6)
    d.rectangle([CX - w / 2, 630, CX + w / 2, 636], fill=col("green", a))

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
        text_c(d, (L + wbar + 30, y), lab, font(54, "Black"), col("text", min(1, p * 2)), anchor="lm")

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
    mx = max(max(s["values"]) for s in series) * 1.1
    L, Rr, T, B = 360, 1620, 300, 840
    X = lambda x: L + (x - xs[0]) / (xs[-1] - xs[0]) * (Rr - L)
    Y = lambda y: B - y / mx * (B - T)
    for frac in (0.25, 0.5, 0.75, 1.0):
        val = mx / 1.1 * frac
        d.line([(L, Y(val)), (Rr, Y(val))], fill=col("grid"), width=2)
        text_c(d, (L - 20, Y(val)), v.get("ylabels", {}).get(str(frac)) or fmt(val, v.get("format")),
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

VISUALS = dict(chapter=v_chapter, title=v_title, stat=v_stat, stat_grid=v_stat_grid, hbars=v_hbars,
               share=v_share, flywheel=v_flywheel, bullets=v_bullets, equation=v_equation,
               cta=v_cta, line=v_line)

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

def make_thumb(spec, out_dir):
    th = spec.get("thumbnail")
    if not th:
        return
    img = Image.new("RGBA", (1280, 720))
    bg = background().resize((1440, 810)).crop((80, 45, 1360, 765))
    img.alpha_composite(bg)
    d = ImageDraw.Draw(img)
    text_c(d, (640, 300), th["big"], font(250, "Black"), col(th.get("color", "gold")),
           stroke=8, stroke_fill=(0, 0, 0, 255))
    text_c(d, (640, 520), th["line"], font(92, "Black"), col("text"), stroke=6, stroke_fill=(0, 0, 0, 255))
    if th.get("tag"):
        f = font(48, "Black")
        tw = f.getlength(th["tag"]) + 60
        rrect(d, [640 - tw / 2, 600, 640 + tw / 2, 680], 20, fill=col("red"))
        text_c(d, (640, 640), th["tag"], f, col("text"))
    img.convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb.png"))

def render(spec_path, out_dir):
    spec = json.load(open(spec_path))
    R.DEFAULT_FMT = spec.get("currency", "usd")
    os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "work_" + spec["id"]); os.makedirs(work, exist_ok=True)
    audio, tl, total = R.build_audio(spec, work)
    asr = R.asr_words(audio)
    caps = []
    for sc, seg in zip(spec["scenes"], tl):
        caps += R.chunk_words(R.align_words(sc["say"], seg, asr), max_chars=40, max_words=7)
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
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
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
            text_c(d, (W - 100, 70), spec["disclaimer"], font(24, "Medium", False), col("dim"), anchor="rm")
        VISUALS[sc["visual"]["type"]](d, sc["visual"], t - (seg["start"] - 0.1), seg["end"] - seg["start"])
        img.alpha_composite(layer)
        draw_caps(img, caps, t)
        ImageDraw.Draw(img).rectangle([0, H - 6, W * t / total, H], fill=col("green"))
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    json.dump({"timeline": tl, "duration": total}, open(os.path.join(work, "timeline.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    print(render(sys.argv[1], sys.argv[2]))
