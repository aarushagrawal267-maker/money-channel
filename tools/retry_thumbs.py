"""Re-try custom thumbnails that failed during upload.

upload.py logs "thumbnail": false in pipeline/posted.json when thumbnails.set fails (the video itself is
kept). This script finds those entries and sets the thumbnail again from output/<id>_thumb.png.
thumbnails.set works with the youtube.upload scope, so it needs no extra permission.

    python3 tools/retry_thumbs.py            # retry every failed thumbnail
    python3 tools/retry_thumbs.py --dry-run  # only list what would be retried

Re-render a missing thumbnail first: Shorts `python3 pipeline/render.py --thumb-only SPEC.json output`,
long videos come out of pipeline/render_long.py.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from upload import load_posted, save_posted  # noqa: E402


def pending(posted):
    """Live (not superseded) uploads whose thumbnail upload failed."""
    return [e for e in posted if e.get("thumbnail") is False and not e.get("superseded") and e.get("video_id")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "output"), help="folder with <id>_thumb.png files")
    a = ap.parse_args()

    posted = load_posted()
    todo = pending(posted)
    if not todo:
        print("No failed thumbnails.")
        return 0
    yt = None
    failures = 0
    for e in todo:
        png = os.path.join(a.out, e["id"] + "_thumb.png")
        if not os.path.isfile(png):
            print(f"MISSING {e['id']}: {png} not found (render the thumbnail first)")
            failures += 1
            continue
        if a.dry_run:
            print(f"would set {e['id']} ({e['video_id']}) from {png}")
            continue
        if yt is None:
            from upload import youtube_client
            from googleapiclient.http import MediaFileUpload
            yt = youtube_client()
        try:
            yt.thumbnails().set(videoId=e["video_id"], media_body=MediaFileUpload(png, mimetype="image/png")).execute()
            e["thumbnail"] = True
            print(f"OK {e['id']} ({e['video_id']})")
        except Exception as ex:  # keep going; report at the end
            print(f"FAILED {e['id']}: {ex}")
            failures += 1
    if not a.dry_run:
        save_posted(posted)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
