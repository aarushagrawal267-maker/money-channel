#!/usr/bin/env bash
# Upload every video in pipeline/schedule.txt that isn't on the channel yet, in schedule order, with its
# publish time. Renders first if the .mp4 is missing or out of date with its spec (a fresh container has no output/).
# Never uploads twice: skips ids scheduled in pipeline/posted.json AND titles already on the channel.
# Stops cleanly at YouTube's daily upload limit (run again later) and on quota/auth errors.
# Exit code: 0 = all done or cleanly stopped at the daily limit; 1 = something failed (see output).
set -uo pipefail
cd "$(dirname "$0")/.."
[ -s models/kokoro-v1.0.onnx ] || ./setup.sh </dev/null || exit 1

# Titles already on the channel (scheduled, public or private, except retired copies).
ON_CHANNEL=$(python3 tools/channel_titles.py </dev/null) || { echo "Could not read the channel's videos; stopping to avoid duplicates."; exit 1; }
failures=0

# Read the schedule on fd 3 so nothing inside the loop (ffmpeg, python) can swallow schedule lines.
while read -r id when <&3; do
  [ -z "${id:-}" ] && continue
  [[ "$id" == \#* ]] && continue
  done_already=$(python3 - "$id" </dev/null <<'PY'
import json, sys
print(any(e["id"] == sys.argv[1] and e.get("publish_at") and not e.get("superseded")
          for e in json.load(open("pipeline/posted.json"))))
PY
)
  [ "$done_already" = "True" ] && continue
  if ! (cd pipeline/specs && python3 "$id.py" >/dev/null </dev/null); then
    echo "FAILED $id: spec checks failed; not uploading it"; failures=$((failures + 1)); continue
  fi
  title=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "pipeline/specs/$id.json" </dev/null)
  if grep -Fxq -- "$title" <<<"$ON_CHANNEL"; then echo "SKIP $id: already on the channel"; continue; fi
  if [ "$(python3 -c "import datetime as d,sys;print(d.datetime.fromisoformat(sys.argv[1])<=d.datetime.now(d.timezone.utc)+d.timedelta(minutes=20))" "$when" </dev/null)" = "True" ]; then
    echo "MISSED SLOT $id $when (not uploaded; give it a new time in schedule.txt)"; failures=$((failures + 1)); continue
  fi
  # Renders if the mp4 is missing or was made from an older version of the spec (skips otherwise).
  if ! tools/render_batch.sh "$id" </dev/null || [ ! -s "output/$id.mp4" ]; then
    echo "FAILED $id: render failed"; failures=$((failures + 1)); continue
  fi
  extra=()
  [[ $id == L* ]] && extra=(--chapters "output/${id}_chapters.txt")
  [ -s "output/${id}_thumb.png" ] && extra+=(--thumb "output/${id}_thumb.png")
  echo "=== $id $when"
  out=$(python3 pipeline/upload.py "pipeline/specs/$id.json" "output/$id.mp4" --publish-at "$when" "${extra[@]}" 2>&1 </dev/null)
  rc=$?
  echo "$out" | grep -vE "uploaded [0-9]+%" | tail -3
  if grep -q uploadLimitExceeded <<<"$out"; then echo "STOPPED: YouTube daily upload limit; run again later."; break; fi
  if grep -qE "quotaExceeded|invalid_grant|unauthorized|insufficientPermissions|HttpError 40[13]" <<<"$out"; then
    echo "STOPPED: YouTube API quota or login problem; see the error above."; failures=$((failures + 1)); break
  fi
  if [ $rc -ne 0 ]; then echo "FAILED $id: upload error"; failures=$((failures + 1)); fi
done 3< <(grep -v '^#' pipeline/schedule.txt)

# Put new uploads into their topic playlists (needs the manage permission; skipped quietly without it).
python3 tools/seo_live.py playlists </dev/null 2>&1 | grep -E "created|done|NO_EDIT" | tail -3

[ "$failures" -eq 0 ] || { echo "$failures problem(s); see above."; exit 1; }
