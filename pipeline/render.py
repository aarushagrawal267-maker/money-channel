"""Render a finance Short (1080x1920) from a JSON spec.

Usage: python3 render.py spec.json out_dir

Spec: {"id", "voice", "speed", "badge", "disclaimer",
       "scenes": [{"say": "...", "visual": {"type": ..., ...}}]}
Visual types: pair, compare, timeline, stat, bars, equation, line, cta.
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
CAP_Y = 1430        # captions centre
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
        s = f"{v/1e7:.2f}".rstrip("0").rstrip(".")
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

VISUALS = dict(pair=v_pair, compare=v_compare, timeline=v_timeline, stat=v_stat,
               bars=v_bars, equation=v_equation, line=v_line, cta=v_cta)

# ---------------------------------------------------------------- audio
def speech_bounds(x, thr=0.02):
    idx = np.where(np.abs(x) > thr)[0]
    return (idx[0], idx[-1]) if len(idx) else (0, len(x))

def make_music(n):
    """Soft original ambient pad + pluck, procedurally generated (no licensing)."""
    t = np.arange(n) / SR
    bpm = 84
    beat = 60 / bpm
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
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
    gap = int(spec.get("gap", 0.22) * SR)
    chunks, timeline, cur = [], [], int(0.15 * SR)
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
    chunks.append(np.zeros(int(0.8 * SR))); cur += int(0.8 * SR)
    voice_track = np.concatenate(chunks).astype(np.float32)
    voice_track /= (np.max(np.abs(voice_track)) + 1e-9) / 0.9
    music = make_music(len(voice_track)) * 10 ** (-24 / 20)
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
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", audio_path, "-ar", "16000",
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
        text_c(d, (CX, 325), disclaimer, font(26, "Medium", False), col("dim"))

def preview_frame(spec, i, t, dur=6.0):
    """One still of scene i at time t (no audio): used by preview.py for quick layout checks."""
    img = make_background().copy()
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_chrome(layer, spec)
    img.alpha_composite(layer)
    vis = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    VISUALS[spec["scenes"][i]["visual"]["type"]](ImageDraw.Draw(vis), spec["scenes"][i]["visual"], t, max(dur, t + 0.5))
    img.alpha_composite(vis, (0, VIS_SHIFT))
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
        caps += chunk_words(align_words(sc["say"], seg, asr))
    bg = make_background()
    out = os.path.join(out_dir, spec["id"] + ".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
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
        st = t - (seg["start"] - 0.1)
        VISUALS[sc["visual"]["type"]](ImageDraw.Draw(vis), sc["visual"], st, seg["end"] - seg["start"])
        img.alpha_composite(vis, (0, VIS_SHIFT))
        draw_captions(img, caps, t)
        # progress bar
        ImageDraw.Draw(img).rectangle([0, H - 10, W * (t / total), H], fill=col("green"))
        proc.stdin.write(img.convert("RGB").tobytes())
        if fi == int(nframes * 0.3):
            img.convert("RGB").save(os.path.join(out_dir, spec["id"] + "_thumb_frame.png"))
    proc.stdin.close(); proc.wait()
    json.dump({"timeline": tl, "duration": total}, open(os.path.join(work, "timeline.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    print(render(sys.argv[1], sys.argv[2]))
