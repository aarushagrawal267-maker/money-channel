#!/usr/bin/env bash
# Upload every video in pipeline/schedule.txt that isn't scheduled yet (per pipeline/posted.json),
# in time order, skipping slots already in the past. Renders first if the .mp4 is missing
# (a fresh container has no output/). Stops at YouTube's daily upload limit; just run it again later.
set -uo pipefail
cd "$(dirname "$0")/.."
[ -s models/kokoro-v1.0.onnx ] || ./setup.sh
# Titles already on the channel (scheduled, public or private), so we never upload twice even if
# posted.json is out of date (e.g. a run that couldn't push).
ON_CHANNEL=$(python3 tools/channel_titles.py) || { echo "Could not read the channel's videos; stopping to avoid duplicates."; exit 1; }
grep -v '^#' pipeline/schedule.txt | while read -r id when; do
  [ -z "$id" ] && continue
  done_already=$(python3 -c "import json,sys;print(any(e['id']=='$id' and e.get('publish_at') and not e.get('superseded') for e in json.load(open('pipeline/posted.json'))))")
  [ "$done_already" = "True" ] && continue
  (cd pipeline/specs && python3 "$id.py" >/dev/null)
  title=$(python3 -c "import json;print(json.load(open('pipeline/specs/$id.json'))['title'])")
  if grep -Fxq "$title" <<<"$ON_CHANNEL"; then echo "SKIP $id: a video titled '$title' is already on the channel"; continue; fi
  if [ "$(python3 -c "import datetime as d;print(d.datetime.fromisoformat('$when')<=d.datetime.now(d.timezone.utc)+d.timedelta(minutes=20))")" = "True" ]; then
    echo "MISSED SLOT $id $when (not uploaded; pick a new time)"; continue; fi
  [ -s "output/$id.mp4" ] || tools/render_batch.sh "$id"
  extra=""; [[ $id == L* ]] && extra="--thumb output/${id}_thumb.png --chapters output/${id}_chapters.txt"
  echo "=== $id $when"
  out=$(python3 pipeline/upload.py "pipeline/specs/$id.json" "output/$id.mp4" --publish-at "$when" $extra 2>&1)
  echo "$out" | grep -vE "uploaded [0-9]+%" | tail -3
  if grep -q uploadLimitExceeded <<<"$out"; then echo "STOPPED: YouTube daily upload limit; run again later."; break; fi
done
