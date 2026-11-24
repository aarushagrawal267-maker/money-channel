#!/usr/bin/env bash
# Render several specs one after another (renders use all CPUs; parallel runs just slow each other down).
# Usage: tools/render_batch.sh 015_rule_of_72 L002_compounding ...
# Skips a video whose output/<id>.mp4 was rendered from exactly the current spec .json (a SHA-256 of the
# spec is stored next to it in output/<id>.spec.sha256), so a fixed script or visual always re-renders,
# while regenerating an unchanged spec never does. Logs to output/batch.log.
# Exit code: 0 = every video rendered or already up to date; 1 = at least one render failed.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p output
failed=0
for id in "$@"; do
  spec="pipeline/specs/$id.json"
  out="output/$id.mp4"
  stamp="output/$id.spec.sha256"
  if [ ! -s "$spec" ]; then echo "$(date +%H:%M) $id FAILED: $spec not found" | tee -a output/batch.log; failed=1; continue; fi
  want=$(sha256sum "$spec" | cut -d' ' -f1)
  # Renders made before stamps existed: trust them if the mp4 is newer than the spec's source .py
  # (the .json is rewritten on every run, the .py only when the script really changes).
  if [ -s "$out" ] && [ ! -e "$stamp" ] && [ "$out" -nt "pipeline/specs/$id.py" ]; then echo "$want" > "$stamp"; fi
  if [ -s "$out" ] && [ "$(cat "$stamp" 2>/dev/null)" = "$want" ]; then
    echo "skip $id (up to date)" | tee -a output/batch.log; continue
  fi
  start=$(date +%s)
  w="output/work_$id"
  rm -rf "$w" "$stamp"
  if [[ "$id" == L* ]]; then
    python3 pipeline/render_long.py "$spec" output >/dev/null 2>>output/batch.log </dev/null
  else
    python3 pipeline/render.py "$spec" "$w" >/dev/null 2>>output/batch.log </dev/null &&
      mv "$w/$id.mp4" "$w/${id}_thumb.png" "$w/${id}_thumb_frame.png" output/ 2>/dev/null
  fi
  status=$?
  if [ "$status" -eq 0 ] && [ -s "$out" ]; then echo "$want" > "$stamp"; else failed=1; fi
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out" 2>/dev/null </dev/null)
  echo "$(date +%H:%M) $id status=$status length=${dur:-?}s took=$(( $(date +%s) - start ))s" | tee -a output/batch.log
done
exit "$failed"
