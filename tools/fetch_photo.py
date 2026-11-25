"""Find and download real, openly licensed photos (people, companies, places, objects) for videos.

Uses the Openverse API (Flickr, museums, etc.). Only licenses that allow commercial use and editing
without share-alike: CC BY, CC0, Public Domain Mark. Every saved photo gets a .json with the credit,
which upload.py adds to the video description automatically.

  python3 tools/fetch_photo.py search "Sara Blakely" [--n 8] [--out DIR]   # candidates + contact sheet
  python3 tools/fetch_photo.py get <openverse_id> <name>                    # -> assets/photos/<name>.jpg/.json

Pick photos that clearly show the subject, are sharp, and aren't misleading (right person, right company).
No logos-as-endorsement, no photos implying someone endorses the channel.
"""
import argparse, io, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(ROOT, "assets", "photos")
API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "PennyToBillion/1.0 (educational video tool)"}
LICENSES = "by,cc0,pdm"


def _get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(20 * (i + 1) if "429" in str(e) else 3 * (i + 1))   # Openverse: 20 searches/min, 200/day


def search(q, n=8, out=None):
    from PIL import Image
    url = API + "?" + urllib.parse.urlencode({"q": q, "license": LICENSES, "page_size": 20, "mature": "false"})
    res = json.loads(_get(url))["results"]
    out = out or os.path.join("/tmp", "photo_" + "".join(c if c.isalnum() else "_" for c in q))
    os.makedirs(out, exist_ok=True)
    got = []
    for r in res:
        if len(got) >= n:
            break
        if (r.get("width") or 0) < 600:
            continue
        try:
            data = _get(API + r["id"] + "/thumb/?full_size=true&compressed=false")
            im = Image.open(io.BytesIO(data)).convert("RGB")
        except Exception:  # noqa: BLE001
            continue
        k = len(got)
        im.save(os.path.join(out, f"{k}.jpg"), quality=90)
        got.append({"k": k, "id": r["id"], "title": r["title"], "creator": r.get("creator"),
                    "license": r["license"], "version": r.get("license_version"), "source": r.get("source"),
                    "size": im.size})
    # contact sheet with numbers
    if got:
        from PIL import ImageDraw
        tiles = [Image.open(os.path.join(out, f"{g['k']}.jpg")) for g in got]
        cols, tw, th = 4, 360, 240
        sheet = Image.new("RGB", (cols * tw, ((len(tiles) + cols - 1) // cols) * th), (20, 20, 20))
        for i, t in enumerate(tiles):
            t.thumbnail((tw - 8, th - 8))
            x, y = (i % cols) * tw + 4, (i // cols) * th + 4
            sheet.paste(t, (x, y))
            ImageDraw.Draw(sheet).text((x + 6, y + 6), str(i), fill=(255, 255, 0))
        sheet.save(os.path.join(out, "sheet.jpg"))
    json.dump(got, open(os.path.join(out, "candidates.json"), "w"), indent=1)
    for g in got:
        print(f"[{g['k']}] {g['id']}  {g['size'][0]}x{g['size'][1]}  {g['license']} {g['version']}  "
              f"{g['creator']!s:.25}  {g['title'][:60]}")
    print("sheet:", os.path.join(out, "sheet.jpg"))


def get(oid, name):
    from PIL import Image
    meta = json.loads(_get(API + oid + "/"))
    if meta["license"] not in LICENSES.split(","):
        sys.exit(f"license {meta['license']} not allowed")
    data = _get(API + oid + "/thumb/?full_size=true&compressed=false")
    im = Image.open(io.BytesIO(data)).convert("RGB")
    os.makedirs(PHOTOS, exist_ok=True)
    im.save(os.path.join(PHOTOS, name + ".jpg"), quality=90)
    lic = {"by": "CC BY", "cc0": "CC0", "pdm": "Public Domain"}[meta["license"]]
    if meta.get("license_version") and meta["license"] == "by":
        lic += " " + meta["license_version"]
    credit = {"title": meta.get("title"), "creator": meta.get("creator") or "unknown",
              "license": lic, "license_url": meta.get("license_url"),
              "source_url": meta.get("foreign_landing_url"), "openverse_id": oid,
              "short": f"Photo: {meta.get('creator') or 'unknown'} / {lic}"}
    json.dump(credit, open(os.path.join(PHOTOS, name + ".json"), "w"), indent=1)
    print(f"saved assets/photos/{name}.jpg {im.size}  {credit['short']}")


def credit_for(path):
    """Credit dict for a photo file path relative to the repo (or None)."""
    j = os.path.join(ROOT, os.path.splitext(path)[0] + ".json")
    return json.load(open(j)) if os.path.exists(j) else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("q"); s.add_argument("--n", type=int, default=8); s.add_argument("--out")
    g = sub.add_parser("get"); g.add_argument("id"); g.add_argument("name")
    a = ap.parse_args()
    search(a.q, a.n, a.out) if a.cmd == "search" else get(a.id, a.name)
