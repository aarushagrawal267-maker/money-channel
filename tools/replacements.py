"""Swap already-scheduled videos for re-edited versions without ever publishing twice.

pipeline/replace.txt lists spec ids whose current upload should be replaced. For each one, this checks
YouTube: once the old video is gone (the owner deleted it in Studio), its posted.json entry is marked
`superseded` + `deleted`, so tools/upload_pending.sh uploads the new version at the same schedule.
While the old copy still exists, nothing happens (no duplicate). Prints what is still waiting.

  python3 tools/replacements.py            # update posted.json; list ids still waiting for deletion
  python3 tools/replacements.py --list     # print the videos the owner must delete (title, time IST, link)
"""
import datetime as dt, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
POSTED = os.path.join(ROOT, "pipeline", "posted.json")
REPLACE = os.path.join(ROOT, "pipeline", "replace.txt")
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def main():
    if not os.path.exists(REPLACE):
        return
    ids = [l.strip() for l in open(REPLACE) if l.strip() and not l.startswith("#")]
    posted = json.load(open(POSTED))
    active = {e["id"]: e for e in posted if e["id"] in ids and not e.get("superseded") and e.get("publish_at")}
    if "--list" in sys.argv:
        for i in ids:
            e = active.get(i)
            if e:
                t = dt.datetime.fromisoformat(e["publish_at"].replace("Z", "+00:00")).astimezone(IST)
                print(f"{t:%a %d %b %I:%M %p} IST  {e.get('title', i)}  https://studio.youtube.com/video/{e['video_id']}/edit")
        return
    if not active:
        return
    from upload import youtube_client
    yt = youtube_client()
    found = set()
    vids = [e["video_id"] for e in active.values()]
    for k in range(0, len(vids), 50):
        r = yt.videos().list(part="status", id=",".join(vids[k:k + 50])).execute()
        found |= {v["id"] for v in r.get("items", [])}
    changed = False
    for i, e in active.items():
        if e["video_id"] in found:
            print(f"WAITING {i}: old copy {e['video_id']} still on YouTube (owner deletes it in Studio)")
        else:
            e["superseded"] = True
            e["deleted"] = True
            e["superseded_reason"] = "replaced by re-edited version (photos)"
            changed = True
            print(f"REPLACE {i}: old copy {e['video_id']} is deleted; new version will upload")
    if changed:
        json.dump(posted, open(POSTED, "w"), indent=2, ensure_ascii=False)
        open(POSTED, "a").write("\n")


if __name__ == "__main__":
    main()
