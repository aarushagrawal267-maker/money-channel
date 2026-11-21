"""Fast layout check: draw every scene of a spec as a still (no voice, no video).

Usage: python3 pipeline/preview.py SPEC.json OUT_DIR [--t 3.0]
Detects Short vs long from the spec id (long ids start with "L").
Writes OUT_DIR/<id>_sheet.png (contact sheet of all scenes) for a quick visual review.
"""
import argparse, json, math, os, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R


def frames(spec, t):
    R.DEFAULT_FMT = spec.get("currency", "usd")
    if spec["id"].startswith("L"):
        import render_long as RL
        bg = RL.background()
        for sc in spec["scenes"]:
            img = bg.crop((120, 70, 120 + RL.W, 70 + RL.H))
            layer = Image.new("RGBA", (RL.W, RL.H), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            if spec.get("badge"):
                R.text_c(d, (100, 70), spec["badge"], R.font(30, "Bold"), R.col("green"), anchor="lm")
            if spec.get("disclaimer"):
                R.text_c(d, (RL.W - 100, 70), spec["disclaimer"], R.font(24, "Medium", False), R.col("dim"), anchor="rm")
            RL.VISUALS[sc["visual"]["type"]](d, sc["visual"], t, max(t + 0.5, 6.0))
            img.alpha_composite(layer)
            yield img.convert("RGB")
    else:
        for i in range(len(spec["scenes"])):
            yield R.preview_frame(spec, i, t).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out"); ap.add_argument("--t", type=float, default=6.0)
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    os.makedirs(a.out, exist_ok=True)
    ims = list(frames(spec, a.t))
    tw = 480 if spec["id"].startswith("L") else 270
    th = int(ims[0].height * tw / ims[0].width)
    cols = 4 if spec["id"].startswith("L") else 6
    rows = math.ceil(len(ims) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    p = os.path.join(a.out, spec["id"] + "_sheet.png")
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    main()
