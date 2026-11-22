# Money Mechanics: project notes for Claude

Faceless YouTube finance channel run by Claude. Owner is non-technical, in India, and follows step-by-step
instructions with screenshots. Explain in plain language, one step at a time. Never ask for credentials in chat.

## Decisions already made (do not re-ask)
- **Channel:** Money Mechanics, handle **@MoneyMechanics-v7t** (cleaner handles were all unavailable). Channel Gmail: the owner's channel account.
- **Niche:** money education: personal finance, smart financing, how markets work, business breakdowns, money news, earning more, and **case studies of top businesses and business founders** (owner request 22 Nov 2026: ~1 in 4 Shorts, and 1 of the 3 long videos every week). See `CONTENT_PLAN.md` pillar 7. Founder/company stories must be sourced, no myths or hero worship, and end with a usable lesson.
- **Audience:** global first (US/UK/CA/AU + English-speaking India). English. **USD by default**; ₹ only for India-story videos (~1 in 5).
- **Schedule:** 2 Shorts/day at **6:30 AM IST** (8 PM ET / 5 PM PT) and **10:30 PM IST** (noon ET / 5 PM UK); 3 long videos/week (Mon/Wed/Fri) at **11:30 PM IST** (1 PM ET / 6 PM UK), 8–12 min. Uploads go up early with `--publish-at`; YouTube publishes at the slot.
- **Style:** dark navy + green + gold, animated charts and text, AI voice (Kokoro `af_heart`), word-synced captions. Owner prefers **simple, clean design** (rejected both a plain and a "too fancy" version; approved flat style in `branding/`).
- **Rules:** every spoken number is computed in the spec file with `assert`s, or sourced (sources in description). No stock tips, no get-rich-quick claims, on-screen disclaimer when returns are shown. Vary pillars and visuals to avoid YouTube's "inauthentic content" policy.

## Repo layout
- `pipeline/render.py`: vertical Short renderer (spec JSON → mp4). Visual types: pair, compare, timeline, stat, bars, equation, line, cta.
- `pipeline/render_long.py`: 16:9 long-form renderer (chapters file + thumbnail). Types: chapter, title, stat, count, stat_grid, hbars, share, flywheel, bullets, equation, line, cta, waterfall, donut, columns, versus, timeline, quote, table.
- `pipeline/preview.py SPEC.json OUT_DIR`: contact sheet of every scene in seconds (no voice). Always check it before rendering.
- `pipeline/upload.py SPEC.json VIDEO.mp4 [--thumb] [--chapters] [--publish-at ISO+tz]`: uploads, sets thumbnail, waits for processing, appends to `pipeline/posted.json`. Refuses to re-upload an id already posted.
- `pipeline/queue.json`: topic queue (40 Shorts, 9 long) with pillar/currency/status; neighbouring Shorts must differ in pillar.
- `tools/voice_check.py`: transcribes the voice track and diffs it against the script to catch mispronunciations.
- `tools/render_batch.sh id1 id2 ...`: renders one at a time into `output/` (gitignored), logs to `output/batch.log`.
- `docs/AUDIT_FORM_ANSWERS.md` + `docs/audit/`: owner's copy-paste answers and evidence files for the YouTube API audit form.
- `pipeline/specs/*.py`: one file per video; running it validates numbers and writes the JSON spec.
  - Shorts: `001_start_early` (INR), `013_minimum_due_trap` (INR), `014_minimum_payment_trap_us`, `015_rule_of_72`, `016_buying_a_share`, `017_upi_free` (INR), `018_start_early_us`, `019_real_hourly_wage`, `020_index_funds_vs_managers`, `021_bnpl`, `022_airline_loyalty`, `023_inflation_100`, `024_expense_ratio`, `025_emergency_fund`.
  - Long: `L001_costco` (~8 min, figures checked against FY2026 release + 10-K), `L002_compounding` (~10 min), `L003_index_funds` (~9 min; SPIVA figures from secondary write-ups, S&P PDFs block automated fetches).
- `tools/get_youtube_token.py`: one-time OAuth script (owner already ran it).
- `tools/branding_v3.py`: final branding generator. `branding/` holds the final files + `CHANNEL_DESCRIPTION.md`.
- `site/`: homepage + privacy policy, published at https://aarushagrawal267-maker.github.io (repo `aarushagrawal267-maker/aarushagrawal267-maker.github.io`), used by the Google consent screen.
- `setup.sh`: installs Python deps and downloads the Kokoro voice model into `models/` (gitignored, ~350 MB).

## Environment gotchas
- `edge-tts` does not work (WebSocket blocked by proxy); use Kokoro (`kokoro-onnx`).
- `faster-whisper` decode via `av` fails; pass a numpy array (render.py converts to 16 kHz wav with ffmpeg and reads with soundfile).
- Rendering: Short ≈ 1–1.5 min, 3-min long video ≈ 4.5 min on 4 CPUs.
- Banner safe area: 1546x423 centred on 2560x1440.
- Voice (Kokoro) gotchas: write numbers as words; hyphenated acronyms break ("FDIC-insured" -> "f dick and short"; say "insured by the FDIC"); "PhonePe" -> write "Phone-Pay"; "Paytm" -> "PayTM"; "IPO" -> "I-P-O". After every render run `tools/voice_check.py SPEC.json output/work_<id>/[work/]audio.wav` and read the non-number differences.
- Render times: Short ≈ 1 min; 9–10 min long video ≈ 10–11 min.

## Setup status
- [x] Channel created, settings, branding
- [x] Google Cloud project `money-channel`, consent screen **In production** (unverified, owner-only; warning screen is expected)
- [x] OAuth Desktop client created; owner ran the token script
- [x] Env vars saved (`YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`); token works, scopes: youtube.upload, youtube.readonly, yt-analytics.readonly.
- [x] `pipeline/upload.py` built; private test upload of 014 succeeded 2026-11-21 (https://youtu.be/Ss1WYNrD6Kk, logged as `test` in posted.json).
- [x] Audit form answers drafted (`docs/AUDIT_FORM_ANSWERS.md`). Site privacy policy expanded + `terms.html` added on branch `claude/friendly-gates-8o3lq0` of the Pages repo; **live site serves `main`, needs merging before the audit**.
- [x] **Private lock is gone:** Google's revision history (Nov 2, 2026) says uploads from unverified API projects are no longer restricted to private. Scheduled uploads with `publishAt` work (verified 2026-11-22). The audit form is **not needed** (only for more quota). Website update for the audit was never merged and isn't required.
- [x] Week 1 uploaded and scheduled 2026-11-22 (Mon 23 – Sun 29 Nov); see `pipeline/posted.json`. The news Short slot (Sun 29, 10:30 PM IST) is still open.
- Our OAuth scopes (youtube.upload, youtube.readonly) **cannot** edit or delete a video after upload (videos.update → 403). To change a scheduled video, re-upload; the owner deletes/unschedules old copies in Studio. Old private copies marked `superseded` in posted.json: Ss1WYNrD6Kk, dhFkCh-pj-U, 3inj6_vZEkQ.

## Next steps for Claude
1. Get owner feedback on week 1; fix what they flag.
2. News Short for week 1 (Sun 29 Nov, 10:30 PM IST): research on the day it's made (rule 6), add as `026_news_...`.
3. After approval, set up scheduled tasks (fresh session per fire) for the upload times above, with failure notifications. Each run: setup.sh → pick next approved item from queue.json → render → upload with `--publish-at` → commit posted.json/queue.json.
4. Keep writing specs from `queue.json` a week ahead.
