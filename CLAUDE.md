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
- `pipeline/render_long.py`: 16:9 long-form renderer (chapters file + thumbnail). Types: chapter, title, stat, count, stat_grid, hbars, share, flywheel, bullets, equation, line, cta, waterfall, donut, columns, versus, timeline, quote, table.
- `pipeline/preview.py SPEC.json OUT_DIR`: contact sheet of every scene in seconds (no voice). Always check it before rendering.
- `pipeline/upload.py SPEC.json VIDEO.mp4 [--thumb] [--chapters] [--publish-at ISO+tz]`: uploads, sets thumbnail, waits for processing, appends to `pipeline/posted.json`. Refuses to re-upload an id already posted.
- `pipeline/queue.json`: topic queue (40 Shorts, 9 long) with pillar/currency/status; neighbouring Shorts must differ in pillar.
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

## Setup status
- [x] Channel created, settings, branding
- [x] Google Cloud project `money-channel`, consent screen **In production** (unverified, owner-only; warning screen is expected)
- [x] OAuth Desktop client created; owner ran the token script
- [x] Env vars saved (`YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`); token works, scopes: youtube.upload, youtube.readonly, yt-analytics.readonly.
- [x] `pipeline/upload.py` built; private test upload of 014 succeeded 2026-11-21 (https://youtu.be/Ss1WYNrD6Kk, logged as `test` in posted.json).
- [x] Audit form answers drafted (`docs/AUDIT_FORM_ANSWERS.md`). Site privacy policy expanded + `terms.html` added on branch `claude/friendly-gates-8o3lq0` of the Pages repo; **live site serves `main`, needs merging before the audit**.
- [ ] Owner submits the audit form. Until approved, API uploads are locked to **private**; owner publishes in Studio.
- [ ] Owner approves week 1 (14 Shorts incl. 1 news Short made fresh on the day, + L001–L003).

## Next steps for Claude
1. Get owner feedback on week 1 and the private test upload; fix what they flag.
2. News Short for week 1: research on the day it's made (rule 6), add as `026_news_...`.
3. After approval, set up scheduled tasks (fresh session per fire) for the upload times above, with failure notifications. Each run: setup.sh → pick next approved item from queue.json → render → upload with `--publish-at` → commit posted.json/queue.json.
4. Keep writing specs from `queue.json` a week ahead.
