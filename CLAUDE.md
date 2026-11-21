# Money Mechanics: project notes for Claude

Faceless YouTube finance channel run by Claude. Owner is non-technical, in India, and follows step-by-step
instructions with screenshots. Explain in plain language, one step at a time. Never ask for credentials in chat.

## Decisions already made (do not re-ask)
- **Channel:** Money Mechanics, handle **@MoneyMechanics-v7t** (cleaner handles were all unavailable). Channel Gmail: the owner's channel account.
- **Niche:** money education: personal finance, smart financing, how markets work, business breakdowns, money news, earning more. See `CONTENT_PLAN.md`.
- **Audience:** global first (US/UK/CA/AU + English-speaking India). English. **USD by default**; ₹ only for India-story videos (~1 in 5).
- **Schedule:** 2 Shorts/day at **6:30 AM IST** and **10:30 PM IST**; 3 long videos/week (Mon/Wed/Fri), 8–12 min.
- **Style:** dark navy + green + gold, animated charts and text, AI voice (Kokoro `af_heart`), word-synced captions. Owner prefers **simple, clean design** (rejected both a plain and a "too fancy" version; approved flat style in `branding/`).
- **Rules:** every spoken number is computed in the spec file with `assert`s, or sourced (sources in description). No stock tips, no get-rich-quick claims, on-screen disclaimer when returns are shown. Vary pillars and visuals to avoid YouTube's "inauthentic content" policy.

## Repo layout
- `pipeline/render.py`: vertical Short renderer (spec JSON → mp4). Visual types: pair, compare, timeline, stat, bars, equation, line, cta.
- `pipeline/render_long.py`: 16:9 long-form renderer (chapters file + thumbnail). Types: chapter, title, stat, stat_grid, hbars, share, flywheel, bullets, equation, line, cta.
- `pipeline/specs/*.py`: one file per video; running it validates numbers and writes the JSON spec.
  - Done: `001_start_early` (INR), `013_minimum_due_trap` (INR), `014_minimum_payment_trap_us` (USD), `L001_costco` (long, FY2026 Costco figures; rendered but not yet reviewed).
- `tools/get_youtube_token.py`: one-time OAuth script (owner already ran it).
- `tools/branding_v3.py`: final branding generator. `branding/` holds the final files + `CHANNEL_DESCRIPTION.md`.
- `site/`: homepage + privacy policy, published at https://aarushagrawal267-maker.github.io (repo `aarushagrawal267-maker/aarushagrawal267-maker.github.io`), used by the Google consent screen.
- `setup.sh`: installs Python deps and downloads the Kokoro voice model into `models/` (gitignored, ~350 MB).

## Environment gotchas
- `edge-tts` does not work (WebSocket blocked by proxy); use Kokoro (`kokoro-onnx`).
- `faster-whisper` decode via `av` fails; pass a numpy array (render.py converts to 16 kHz wav with ffmpeg and reads with soundfile).
- Rendering: Short ≈ 1–1.5 min, 3-min long video ≈ 4.5 min on 4 CPUs.
- Banner safe area: 1546x423 centred on 2560x1440.

## Setup status
- [x] Channel created, settings, branding
- [x] Google Cloud project `money-channel`, consent screen **In production** (unverified, owner-only; warning screen is expected)
- [x] OAuth Desktop client created; owner ran the token script
- [ ] Owner saves env vars in the Claude environment: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (optional `PEXELS_API_KEY`)
- [ ] YouTube API audit form (needed for public API uploads; until approved, API uploads are locked to **private**). Draft the answers for the owner.

## Next steps for Claude
1. Check the env vars exist (don't print values). Build `pipeline/upload.py` (YouTube Data API v3: videos.insert resumable upload, thumbnails.set, `publishAt` scheduling, category 27 Education, `selfDeclaredMadeForKids=false`, `containsSyntheticMedia=false` for chart videos).
2. Test with one **private** upload of an existing sample; confirm with the owner.
3. Build a topic queue + posted log (`pipeline/queue.json`, `pipeline/posted.json`) committed to the repo so scheduled runs never repeat.
4. Review/fix `L001_costco`, add more long-form visual variety, then make week 1: 14 Shorts + 3 long videos for owner approval.
5. Draft the audit form answers.
6. After approval, set up scheduled tasks (fresh session per fire) for the upload times above, with failure notifications.
