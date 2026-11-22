"""Print the title of every video on the channel (one per line), including scheduled and private ones.
Used by upload_pending.sh to avoid uploading the same video twice."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from upload import youtube_client

HERE = os.path.dirname(os.path.abspath(__file__))
# old copies we deliberately replaced (kept private on the channel) don't count as "already uploaded"
retired = {e["video_id"] for e in json.load(open(os.path.join(HERE, "..", "pipeline", "posted.json"))) if e.get("superseded")}
yt = youtube_client()
uploads = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
tok = None
while True:
    r = yt.playlistItems().list(part="snippet", playlistId=uploads, maxResults=50, pageToken=tok).execute()
    for it in r["items"]:
        if it["snippet"]["resourceId"]["videoId"] not in retired:
            print(it["snippet"]["title"])
    tok = r.get("nextPageToken")
    if not tok:
        break
