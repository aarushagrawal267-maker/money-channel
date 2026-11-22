#!/usr/bin/env bash
# Render several specs one after another (renders use all CPUs; parallel runs just slow each other down).
# Usage: tools/render_batch.sh 015_rule_of_72 L002_compounding ...
# Skips a video whose .mp4 is newer than its spec .json. Logs to output/batch.log.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p output
for id in "$@"; do
  spec="pipeline/specs/$id.json"
  out="output/$id.mp4"
  if [ -s "$out" ] && [ "$out" -nt "$spec" ]; then echo "skip $id (up to date)" | tee -a output/batch.log; continue; fi
  start=$(date +%s)
  if [[ "$id" == L* ]]; then r=pipeline/render_long.py; w="output/work_$id"; else r=pipeline/render.py; w="output/work_$id"; fi
  rm -rf "$w"
  if [[ "$id" == L* ]]; then python3 "$r" "$spec" output >/dev/null 2>>output/batch.log
  else python3 "$r" "$spec" "$w" >/dev/null 2>>output/batch.log && mv "$w/$id.mp4" "$w/${id}_thumb.png" "$w/${id}_thumb_frame.png" output/ 2>/dev/null; fi
  status=$?
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out" 2>/dev/null)
  echo "$(date +%H:%M) $id status=$status length=${dur:-?}s took=$(( $(date +%s) - start ))s" | tee -a output/batch.log
done
