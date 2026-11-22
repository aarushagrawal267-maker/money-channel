# Code review: upload automation (22 Nov 2026)

Scope: `pipeline/upload.py`, `tools/upload_pending.sh`, `tools/channel_titles.py`, `tools/render_batch.sh`, `setup.sh`, renderer failure paths, `docs/AUTOPILOT.md`. Read-only review; nothing was changed or uploaded.

**Overall:** the structure is good. The channel-title check fails closed (line 10), `publishAt` is tz-checked and normalised to UTC, and `resumable_upload` relies on googleapiclient's error-state query, so a dropped final chunk does not create a second video. The weak spots are the time between upload and logging, half-rendered files, and failures that go unreported.

## HIGH

**H1. Video uploaded but not logged** (`pipeline/upload.py:197-223`)
`log_posted` runs only after the thumbnail upload and up to 10 minutes of `wait_for_processing`. Two things can stop the script before it logs. First, `videos().list()` errors (5xx, quotaExceeded) are not caught. Second, the scheduled run calls the script through the Bash tool, which kills commands after 2 minutes by default (10 at most). When that happens the video is on YouTube but missing from `posted.json`, and the next run's only guard is the title match.
```diff
     vid = resp["id"]
+    if not a.no_log:
+        log_posted({"id": spec["id"], "video_id": vid, "publish_at": body["status"].get("publishAt"),
+                    "title": body["snippet"]["title"], "processing": "pending", ...})
-    processing = wait_for_processing(yt, vid)
+    try: processing = wait_for_processing(yt, vid, timeout=120)
+    except Exception as e: processing = f"unknown ({type(e).__name__})"
+    # then update the entry just written instead of appending
```
AUTOPILOT A7/B1: run `tools/upload_pending.sh > output/upload.log 2>&1` in the background (`run_in_background`), then read the log.

**H2. A half-rendered long video gets uploaded** (`pipeline/render_long.py:440-463`, `tools/upload_pending.sh:20`)
`render_long.py` writes straight to `output/<id>.mp4` and never checks `proc.wait()`. A long render takes 10–11 minutes, longer than the Bash tool's 10-minute limit. If the render crashes or is killed partway, a non-empty mp4 is left behind: either short but playable, or missing its moov atom. Line 20 only checks `-s`, so the next run uploads the broken file and logs it as done. That slot is never retried.
```diff
-    out = os.path.join(out_dir, spec["id"] + ".mp4")
+    final = os.path.join(out_dir, spec["id"] + ".mp4"); out = final + ".part.mp4"
 ...
-    proc.stdin.close(); proc.wait()
+    proc.stdin.close()
+    if proc.wait() != 0: sys.exit(f"ffmpeg failed for {spec['id']}")
+    os.replace(out, final)
```
Make the same change in `render.py:491`. In `upload_pending.sh`, `[ -s ... ] || tools/render_batch.sh "$id" || { echo "RENDER FAILED $id"; continue; }`. `render_batch.sh` also needs to `exit 1` when any `status` is non-zero, because today it always exits 0.

**H3. ffmpeg swallows the schedule list** (`tools/upload_pending.sh:11,20`, `pipeline/render.py:355`)
The loop reads `schedule.txt` from stdin. When a missing mp4 triggers a render, `asr_words` runs `ffmpeg` without `-nostdin`, and it inherits that stdin. ffmpeg reads stdin while it runs (keyboard commands), so it eats bytes from later lines. Those videos are then garbled or skipped without any message.
```diff
-grep -v '^#' pipeline/schedule.txt | while read -r id when; do
+while read -r id when <&3; do
 ...
-done
+done 3< <(grep -v '^#' pipeline/schedule.txt)
```
Also add `"-nostdin"` to every ffmpeg call and pass `</dev/null` to `render_batch.sh` and `upload.py`. Using fd 3 also removes the subshell, so the loop can count failures (see M1).

**H4. Duplicate risk for Costco and 014 on Mon 23 Nov** (`pipeline/posted.json`, `tools/channel_titles.py:9`)
`3inj6_vZEkQ` (Costco, private) is marked `superseded`, so its title is left out of `ON_CHANNEL`. The later entry's note says "3inj6_vZEkQ is the live copy". If the owner publishes it, Monday's retry run will upload a second Costco video for 23:30 IST.
Separately, `O_m56QwX76o` (014 duplicate) is still scheduled for 2026-11-23T17:00Z unless the owner has deleted it.
`CLAUDE.md:48` says `Ss1WYNrD6Kk` and `dhFkCh-pj-U` are superseded, but `posted.json` treats them as the live public copies. Settle which copies are live before the retry trigger fires. Consider a separate `"reupload": true` flag instead of overloading `superseded`.

## MEDIUM

**M1. Quota or auth errors do not stop the loop, and the script always exits 0** (`tools/upload_pending.sh:23-25`)
The loop stops only on `uploadLimitExceeded`. On `quotaExceeded` (the daily API quota, 403), `invalid_grant` or a 401, it keeps rendering and trying every remaining item. Each long video costs about 10 minutes of render time. Because the pipeline ends with the loop, the scheduled task sees success even when nothing uploaded.
```diff
-  out=$(python3 pipeline/upload.py ... 2>&1)
+  out=$(python3 pipeline/upload.py ... 2>&1 </dev/null); rc=$?
+  [ $rc -ne 0 ] && fails=$((fails+1))
-  if grep -q uploadLimitExceeded <<<"$out"; then
+  if grep -qE 'uploadLimitExceeded|quotaExceeded|invalid_grant|HttpError 401' <<<"$out"; then
 ...
+exit $(( fails > 0 ))
```

**M2. Spec errors are ignored** (`upload_pending.sh:15`)
If a spec's `assert` fails, the run continues with the stale `.json` committed in git. That means uploading numbers that failed the check, against the channel rules. Fix: `(cd pipeline/specs && python3 "$id.py" >/dev/null) || { echo "SPEC FAILED $id"; fails=$((fails+1)); continue; }`.

**M3. Stale mp4 uploaded with new metadata** (`upload_pending.sh:20`)
If a spec's voice text or visuals are fixed after rendering, the old `output/<id>.mp4` still passes `-s` and goes up with the new title. Store a hash of the spec next to the mp4 (`output/<id>.spechash`) and re-render when it differs. The mtime test in `render_batch.sh:11` will not work, because line 15 rewrites the JSON on every run.

**M4. Fresh-container setup can fail silently** (`setup.sh:12`, `upload_pending.sh:7`, `render.py:17`)
- `curl` has no `-f` and keeps partial files. A 404 page or a timed-out download is saved as the model and passes `[ -s ]` forever. Fix: `curl -fsSL ... -o "models/$f.part" && mv "models/$f.part" "models/$f"`.
- Fonts come from the system package `fonts-inter` (`/usr/share/fonts/opentype/inter/`), which `setup.sh` never installs. Fix: `[ -d /usr/share/fonts/opentype/inter ] || apt-get install -y fonts-inter`, or vendor the fonts into the repo.
- Line 7 ignores a failed `./setup.sh` and only checks one of the two model files. Fix: `./setup.sh || exit 1`.
- `asr_words` (`render.py:362`) quietly falls back to estimated caption timing if Whisper is missing. Print `WARNING` to stderr so the batch log shows it.

**M5. Gaps in the title guard** (`upload_pending.sh:17`)
- `grep -Fxq "$title"` reads a title that starts with `-` as a grep option. grep then exits 2, the title counts as "not found", and the video is uploaded twice. Use `grep -Fxq -- "$title"`.
- `upload.py` strips `<>` from titles but the check uses the raw spec title. Compare `build_body(spec)["snippet"]["title"]` instead.
- The guard lives only in the driver, so a manual `upload.py` call skips it. Move it into `upload.py` (it costs about 1 unit per 50 videos).
- Titles are never put into code, so quotes, `$` and `&` are safe today.

**M6. Failed thumbnails are never retried** (`upload.py:201-209`)
A failure is logged as `"thumbnail": false` and then forgotten, and AUTOPILOT B2 does not check that field. `thumbnails.set` works with the `youtube.upload` scope, so add `tools/retry_thumbs.py` for entries with `thumbnail: false`, and add that check to B2. Also confirm the thumbnail file exists before uploading, so a missing PNG stops the upload instead of producing a video without a thumbnail.

## LOW

- **L1.** `log_posted` (`upload.py:148`) is not atomic. A crash mid-write corrupts `posted.json`, and `channel_titles.py:9` then stops every run. Write to a temp file and `os.replace`. Two runs that both append can conflict in git at the closing `]`: commit right after each run with `git pull --rebase` and retry, or switch to JSON Lines.
- **L2.** Parsing `schedule.txt` (`upload_pending.sh:11,18`): a CRLF line, a trailing `# comment`, or a time with no zone makes the Python heredoc print a traceback. `$(...)` then comes back empty, so the slot is treated as "not missed" and only `upload.py` stops it, with a stack trace. The 20-minute check also runs before a render of up to 11 minutes. `upload.py` re-checks for 15 minutes, which is safe, but the message is unclear. Validate the time once, in Python, after rendering.
- **L3.** `resumable_upload` (`upload.py:117`) treats every non-HTTP exception (`code is None`) as transient, including programming errors, so a bug costs about 4 minutes of retries. Limit the retry to `OSError`, `httplib2.HttpLib2Error` and `ssl.SSLError`.
- **L4.** The fallback for long localised descriptions (`upload.py:101`) drops sources and disclaimers for that language. Keep the disclaimer line.
- **L5.** `AUTOPILOT.md:4` says scheduled tasks start a fresh session, but `CLAUDE.md` says they fire into the original session. The `upload.py` docstring (lines 14-15) still describes the old private-only lock.

## Suggested order
H4 (before Mon 12:30 IST), then H1, H3, H2, M1, M2, M4. Together these make every failure either stop the run or show up clearly in the log.
