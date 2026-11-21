# Money Mechanics: video pipeline

Faceless finance channel: 2 Shorts a day + 3 long videos a week.

| Folder / file | What it is |
|---|---|
| `CONTENT_PLAN.md` | Channel strategy, pillars, first 60 topics |
| `SETUP_GUIDE.md` | Step-by-step channel + API setup |
| `pipeline/render.py` | Renders a vertical Short (1080x1920) from a JSON spec |
| `pipeline/render_long.py` | Renders a long 16:9 video, chapters and thumbnail |
| `pipeline/specs/` | One Python file per video: script + numbers, with checks that fail if a spoken number is wrong |
| `tools/` | YouTube token script, branding generators |
| `branding/` | Final profile picture, banner, watermark, channel description |
| `site/` | Homepage + privacy policy (for Google's consent screen) |

Run `./setup.sh` in a fresh session, then e.g.:

    cd pipeline && python3 specs/014_minimum_payment_trap_us.py && python3 render.py specs/014_minimum_payment_trap_us.json ../output

Credentials (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN) live in the cloud environment settings, never in this repo.
