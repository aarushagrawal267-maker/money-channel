"""Upload a rendered video to the Penny to Billion channel (YouTube Data API v3).

Usage:
    python3 pipeline/upload.py SPEC.json VIDEO.mp4 [--thumb PNG] [--chapters TXT]
                               [--publish-at 2026-11-23T06:30:00+05:30] [--privacy private]
                               [--dry-run] [--test] [--no-log]

Reads title / description / tags from the spec JSON. For long videos, pass --chapters
(the <id>_chapters.txt written by render_long.py) and they are added to the description.

Credentials come from env vars YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN; they are
never printed. On success the upload is appended to pipeline/posted.json.

Scheduled uploads (--publish-at) go public by themselves at that time (Google lifted the private lock
for unverified projects on 2 Nov 2026). Our scopes can't edit or delete a video after upload.
"""
import argparse, datetime as dt, json, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
POSTED = os.path.join(HERE, "posted.json")
CATEGORY_EDUCATION = "27"
RETRY_STATUS = {500, 502, 503, 504}
MAX_TITLE, MAX_DESC, MAX_TAGS_CHARS = 100, 5000, 500
AI_LINE = "Made with AI assistance: scripts are researched and written with AI and narrated by a synthetic voice; every number is checked against the sources listed."
SUBSCRIBE_LINE = "New money lesson every day. Subscribe: https://www.youtube.com/channel/UC-DK-CcVvDnkZoehOWGWlBg?sub_confirmation=1"


def youtube_client():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    missing = [v for v in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(v)]
    if missing:
        sys.exit(f"Missing environment variables: {', '.join(missing)}")
    creds = Credentials(
        None, refresh_token=os.environ["YT_REFRESH_TOKEN"].strip(),
        client_id=os.environ["YT_CLIENT_ID"].strip(), client_secret=os.environ["YT_CLIENT_SECRET"].strip(),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.readonly"])
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def fit_tags(tags):
    """YouTube caps the tag list at 500 chars (tags with spaces count their quotes)."""
    out, total = [], 0
    for t in tags:
        t = t.replace("<", "").replace(">", "").strip()
        cost = len(t) + (2 if " " in t else 0) + (1 if out else 0)
        if t and total + cost <= MAX_TAGS_CHARS:
            out.append(t); total += cost
    return out


def build_body(spec, chapters=None, privacy="private", publish_at=None):
    title = spec["title"].replace("<", "").replace(">", "")
    if len(title) > MAX_TITLE:
        sys.exit(f"Title is {len(title)} chars (max {MAX_TITLE}): {title}")
    lines = spec.get("description", "").rstrip().split("\n")
    tags_line = lines.pop() if lines and lines[-1].startswith("#") else ""
    body = "\n".join(lines).rstrip()
    # Hashtags: first 3 show above the title, so keep the broad ones first and the list short.
    hashtags = [h for h in tags_line.split() if h.startswith("#") and h.lower() != "#shorts"][:4]
    if not spec["id"].startswith("L"):
        hashtags.append("#shorts")
    desc = body
    if chapters:
        desc += "\n\nChapters\n" + chapters.strip()
    desc += "\n\n" + AI_LINE + "\n\n" + SUBSCRIBE_LINE
    if hashtags:
        desc += "\n\n" + " ".join(hashtags)
    desc += "\n"
    desc = desc.replace("<", "").replace(">", "")
    if len(desc.encode("utf-8")) > MAX_DESC:
        sys.exit(f"Description too long ({len(desc.encode('utf-8'))} bytes, max {MAX_DESC}).")
    status = {
        "privacyStatus": privacy,
        "selfDeclaredMadeForKids": False,
        "embeddable": True,
        "license": "youtube",
        "publicStatsViewable": True,
        # Animated charts + text narrated by a synthetic voice: not realistic altered content.
        "containsSyntheticMedia": bool(spec.get("contains_synthetic_media", False)),
    }
    if publish_at:
        status["privacyStatus"] = "private"   # required by the API for scheduled videos
        status["publishAt"] = publish_at
    body = {
        "snippet": {
            "title": title, "description": desc, "tags": fit_tags(spec.get("tags", [])),
            "categoryId": CATEGORY_EDUCATION, "defaultLanguage": "en", "defaultAudioLanguage": "en",
        },
        "status": status,
    }
    # Translated title/description shown to viewers whose YouTube language matches (global reach).
    # Spec: "localizations": {"es": {"title": ..., "summary": ...}, ...}. The localized description is
    # the translated summary followed by the full English description (keeps sources + disclaimers).
    locs = {}
    for lang, l10n in (spec.get("localizations") or {}).items():
        t = l10n["title"].replace("<", "").replace(">", "")[:MAX_TITLE]
        d = (l10n.get("summary", "").strip() + "\n\n" + desc).strip()
        if len(d.encode("utf-8")) > MAX_DESC:
            d = l10n.get("summary", "").strip() + "\n\n" + SUBSCRIBE_LINE
        locs[lang] = {"title": t, "description": d}
    if locs:
        body["localizations"] = locs
    return body


def resumable_upload(request):
    response, retry = None, 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"  uploaded {status.progress():.0%}", flush=True)
        except Exception as e:  # HttpError or network error
            code = getattr(getattr(e, "resp", None), "status", None)
            transient = code in RETRY_STATUS or code is None
            if not transient or retry >= 8:
                raise
            retry += 1
            wait = min(64, 2 ** retry) * random.uniform(0.5, 1.0)
            print(f"  transient error ({code or type(e).__name__}), retry {retry} in {wait:.0f}s", flush=True)
            time.sleep(wait)
    return response


def wait_for_processing(yt, vid, timeout=600):
    """Poll videos.list until YouTube finishes processing our upload (or give up after `timeout` s)."""
    end = time.time() + timeout
    while True:
        items = yt.videos().list(part="status,processingDetails", id=vid).execute().get("items", [])
        if items:
            st = items[0].get("processingDetails", {}).get("processingStatus")
            if st in ("succeeded", "failed", "terminated") or items[0]["status"].get("uploadStatus") in ("processed", "rejected", "failed"):
                return st or items[0]["status"].get("uploadStatus")
        if time.time() > end:
            return "still processing"
        time.sleep(15)


def load_posted():
    if os.path.exists(POSTED):
        with open(POSTED) as f:
            return json.load(f)
    return []


def log_posted(entry):
    posted = load_posted()
    posted.append(entry)
    with open(POSTED, "w") as f:
        json.dump(posted, f, indent=2, ensure_ascii=False)
        f.write("\n")


def parse_publish_at(s):
    if not s:
        return None
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        sys.exit("--publish-at needs a timezone, e.g. 2026-11-23T06:30:00+05:30")
    if t <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15):
        sys.exit("--publish-at must be at least 15 minutes in the future")
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("video")
    ap.add_argument("--thumb"); ap.add_argument("--chapters")
    ap.add_argument("--publish-at"); ap.add_argument("--privacy", default="private",
                                                     choices=["private", "unlisted", "public"])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--allow-repeat", action="store_true")
    ap.add_argument("--test", action="store_true", help="mark as a test upload in posted.json (doesn't block a real upload later)")
    a = ap.parse_args()

    spec = json.load(open(a.spec))
    if not os.path.getsize(a.video):
        sys.exit("Video file is empty")
    if not a.allow_repeat and any(p["id"] == spec["id"] and not p.get("test") and not p.get("superseded") for p in load_posted()):
        sys.exit(f"{spec['id']} is already in posted.json; refusing to upload it twice (use --allow-repeat).")
    chapters = open(a.chapters).read() if a.chapters else None
    body = build_body(spec, chapters, a.privacy, parse_publish_at(a.publish_at))

    if a.dry_run:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        return

    from googleapiclient.http import MediaFileUpload
    yt = youtube_client()
    print(f"Uploading {os.path.basename(a.video)} ({os.path.getsize(a.video)/1e6:.1f} MB)...", flush=True)
    parts = "snippet,status" + (",localizations" if "localizations" in body else "")
    req = yt.videos().insert(part=parts, body=body, notifySubscribers=True,
                             media_body=MediaFileUpload(a.video, mimetype="video/mp4",
                                                        chunksize=8 * 1024 * 1024, resumable=True))
    resp = resumable_upload(req)
    vid = resp["id"]
    print(f"Uploaded: https://youtu.be/{vid}  (status: {resp['status'].get('privacyStatus')})")

    # Log immediately, so a crash or timeout later can never leave an unlogged video on YouTube.
    entry = {
        "id": spec["id"], "video_id": vid, "url": f"https://youtu.be/{vid}",
        "title": body["snippet"]["title"],
        "uploaded_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publish_at": body["status"].get("publishAt"),
        "privacy": resp["status"].get("privacyStatus"),
        **({"test": True} if a.test else {}),
    }
    if not a.no_log:
        log_posted(entry)

    thumb_ok = None
    if a.thumb:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(a.thumb, mimetype="image/png")).execute()
            thumb_ok = True
            print("Thumbnail set.")
        except Exception as e:  # don't lose the upload over a thumbnail error
            thumb_ok = False
            print(f"WARNING: thumbnail failed: {e}")
    try:
        processing = wait_for_processing(yt, vid)
    except Exception as e:
        processing = f"unknown ({type(e).__name__})"
    print(f"Processing: {processing}")
    if not a.no_log:
        posted = load_posted()
        for e in posted:
            if e.get("video_id") == vid:
                e.update({"thumbnail": thumb_ok, "processing": processing})
        with open(POSTED, "w") as f:
            json.dump(posted, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(json.dumps({"video_id": vid, "thumbnail": thumb_ok}))


if __name__ == "__main__":
    main()
