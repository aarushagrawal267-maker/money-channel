"""Improve videos that are already on the channel (needs the youtube.force-ssl permission).

  python3 tools/seo_live.py check              # prints whether the token can edit videos
  python3 tools/seo_live.py titles ID [ID...]  # re-apply title/description/tags/translations from the spec
  python3 tools/seo_live.py playlists          # put every posted video into its topic playlist

Safe to run repeatedly: playlists are found by title (or pipeline/playlists.json) and videos already
in a playlist are skipped. Only the snippet/localizations parts are updated, never status, so a
scheduled video keeps its publish time.
"""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from upload import youtube_client, build_body  # noqa: E402

POSTED = os.path.join(ROOT, "pipeline", "posted.json")
QUEUE = os.path.join(ROOT, "pipeline", "queue.json")
PL_FILE = os.path.join(ROOT, "pipeline", "playlists.json")

PLAYLISTS = {  # pillar -> (title, description)
    "money_math": ("Money Math: How Your Money Grows",
                   "Compound interest, inflation, the Rule of 72 and the simple math behind building wealth."),
    "financing_traps": ("Debt & Credit Traps (and How to Avoid Them)",
                        "Credit cards, minimum payments, buy now pay later, car loans and emergency funds, explained with real numbers."),
    "markets": ("How the Stock Market Works",
                "Stocks, index funds, fees, interest rates and market basics, explained simply."),
    "business": ("How Companies Make Money",
                 "Business models explained: Costco, airlines, credit cards, free apps and more."),
    "case_study": ("Business Case Studies & Founder Stories",
                   "Why companies win or fail and what founders actually did, with sources and a lesson you can use."),
    "earn_more": ("Earn More: Salary & Career Money",
                  "Raises, job switches and your real hourly wage, with the math behind each decision."),
    "news": ("Money News Explained", "The week's biggest money and business story, explained in under a minute."),
}
PILLAR_ALIAS = {"founder": "case_study"}


def scopes(yt):
    from google.auth.transport.requests import Request
    c = yt._http.credentials
    c.refresh(Request())
    info = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/tokeninfo?access_token=" + c.token))
    return info.get("scope", "")


def live_posts():
    seen = {}
    for p in json.load(open(POSTED)):
        if not p.get("superseded") and p.get("video_id"):
            seen[p["id"]] = p["video_id"]   # last upload of an id wins
    return seen


def spec_for(vid_id):
    return json.load(open(os.path.join(ROOT, "pipeline", "specs", vid_id + ".json")))


def cmd_titles(yt, ids):
    posts = live_posts()
    for i in ids:
        spec = spec_for(i)
        chapters = None
        chap = os.path.join(ROOT, "output", i + "_chapters.txt")
        if i.startswith("L") and os.path.exists(chap):
            chapters = open(chap).read()
        body = build_body(spec, chapters=chapters)
        parts = ["snippet"]
        req = {"id": posts[i], "snippet": body["snippet"]}
        if body.get("localizations"):
            req["localizations"] = body["localizations"]
            parts.append("localizations")
        yt.videos().update(part=",".join(parts), body=req).execute()
        print(f"updated {i} ({posts[i]}): {body['snippet']['title']}")


def cmd_playlists(yt):
    q = json.load(open(QUEUE))
    pillar = {it["spec"]: it["pillar"] for it in q["shorts"] + q["long"] if it.get("spec")}
    saved = json.load(open(PL_FILE)) if os.path.exists(PL_FILE) else {}
    existing = {}
    req = yt.playlists().list(part="snippet", mine=True, maxResults=50)
    while req:
        r = req.execute()
        existing.update({p["snippet"]["title"]: p["id"] for p in r["items"]})
        req = yt.playlists().list_next(req, r)
    added = 0
    for vid_id, video in live_posts().items():
        pl = PILLAR_ALIAS.get(pillar.get(vid_id), pillar.get(vid_id))
        if vid_id.split("_")[0].isdigit() and "news" in vid_id:
            pl = "news"
        if pl not in PLAYLISTS:
            continue
        title, desc = PLAYLISTS[pl]
        pid = saved.get(pl) or existing.get(title)
        if not pid:
            pid = yt.playlists().insert(part="snippet,status", body={
                "snippet": {"title": title, "description": desc, "defaultLanguage": "en"},
                "status": {"privacyStatus": "public"}}).execute()["id"]
            print("created playlist:", title)
        saved[pl] = pid
        items, req = set(), yt.playlistItems().list(part="contentDetails", playlistId=pid, maxResults=50)
        while req:
            r = req.execute()
            items.update(it["contentDetails"]["videoId"] for it in r["items"])
            req = yt.playlistItems().list_next(req, r)
        if video in items:
            continue
        yt.playlistItems().insert(part="snippet", body={"snippet": {
            "playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": video}}}).execute()
        added += 1
        print(f"added {vid_id} to {title}")
    json.dump(saved, open(PL_FILE, "w"), indent=2)
    print(f"playlists done, {added} added")


def main():
    yt = youtube_client()
    have = scopes(yt)
    if "youtube.force-ssl" not in have and "auth/youtube " not in have + " ":
        print("NO_EDIT_PERMISSION: token only has:", have)
        sys.exit(2)
    if sys.argv[1:2] == ["check"]:
        print("OK: token can edit videos")
    elif sys.argv[1:2] == ["titles"]:
        cmd_titles(yt, sys.argv[2:])
    elif sys.argv[1:2] == ["playlists"]:
        cmd_playlists(yt)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
