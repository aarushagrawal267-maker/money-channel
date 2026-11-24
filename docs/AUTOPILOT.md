# Autopilot runbook (owner is away; Claude runs the channel)

The owner asked (22 Nov 2026): "handle all the things on my channel, make it popular, do everything
that maximises my global audience." Scheduled tasks start a fresh session that follows one section here.
Read `CLAUDE.md` and `CONTENT_PLAN.md` first. The owner is non-technical: reports are short and in plain language.

## 0. Start of every run
1. `cd` into the `money-channel` repo, then run `git fetch origin claude/friendly-gates-8o3lq0 && git checkout claude/friendly-gates-8o3lq0 && git pull`.
   All work is committed and pushed **to this branch** (owner's instruction).
2. Check `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` exist (never print them).
3. `./setup.sh` (installs deps + voice model; a fresh container has no `models/` or `output/`).

## A. Weekly production (Wednesday)
Goal: next week's 13 Shorts + 3 long videos written, checked, rendered, uploaded and scheduled.
1. **Analytics review.** Use the YouTube Analytics API (`yt-analytics.readonly`, `youtubeAnalytics.reports.query`,
   ids=channel==MINE) for the last 7 and 28 days: views, estimatedMinutesWatched, averageViewPercentage,
   subscribersGained per video; views by country; traffic sources. Write a short note in
   `docs/analytics/<date>.md`: what worked (topics, title styles, lengths), what didn't, what you'll change.
   Act on it: move better-performing topic types up in `pipeline/queue.json`; adjust title style.
   Only change upload times if data covers 3+ weeks; record the change in `CLAUDE.md`.
2. **Slots.** The first Monday–Sunday week whose slots are not yet in `pipeline/schedule.txt` (stay about one week ahead): Shorts at 06:30 and 22:30 IST; long videos Mon/Wed/Fri 23:30 IST.
   Leave **Sunday 22:30 IST** for the news Short (section C). Also fill any empty slot in the next 10 days.
3. **Pick topics** from `pipeline/queue.json` (status `idea`), keeping: neighbouring Shorts on different
   pillars; ~1 in 5 India stories (₹); ~3 case-study Shorts and **1 case-study long video** per week
   (pillar 7); don't repeat a topic covered in the last 4 weeks (check `posted.json` titles).
4. **Write specs** in `pipeline/specs/` (next free number; long ids `L0xx_`). Copy the structure of the
   existing ones. Independent topics can be written by parallel subagents; give each the rules below
   and review their work. Rules:
   - every spoken/shown number computed with `assert`s or sourced (Python constant + source/date comment;
     sources listed in the description). Prefer primary sources. If unconfirmed, leave it out.
   - Shorts 30–40 s (~80–100 words), payoff-first hook (see Retention rules below).
     Long 8–12 min (1,400–1,700 words), 6–7 chapters, ≥10 visual types, never the same visual twice in a row, `thumbnail` set.
   - spoken numbers in words; see voice gotchas in `CLAUDE.md`.
   - no stock tips, no "buy this", no get-rich-quick; on-screen disclaimer when returns are shown;
     founder stories: no myths or hero worship, end with a usable lesson.
   - **Title**: under 60 characters, the searchable phrase first, a curiosity gap, no `#shorts`, no clickbait
     that the video doesn't pay off. **Description**: 2–3 sentence summary with natural search phrases first,
     then assumptions/sources/disclaimer, 3–5 broad hashtags on the last line (upload.py adds the subscribe
     line and `#shorts`).
   - **Localizations** (global reach): add `"localizations"` for `es`, `pt`, `hi`, `id`, `de`, `fr`, each
     `{"title": ..., "summary": ...}` (natural translation, same numbers and currency, Hindi in Devanagari,
     ≤60 characters where possible). upload.py turns these into translated titles/descriptions.
   - **Specialist rules (from docs/reviews/, 23 Nov 2026):**
     - Shorts: open on the payoff (the surprising number or result), not the setup; aim for 30–40 s
       (~80–100 words); one visual per ~4 s; end with a varied closing line (never the same line as the
       previous Short; ideally one that loops back to the opening). Short title must differ from its
       matching long video's title (they shouldn't compete in search).
     - Long videos are the priority for monetisation (from Feb 2027 YPP needs 1,000 subs + 8,000 long-form
       watch hours/12 months): write the title + thumbnail idea before the script; make 2–3 Shorts from
       each long video and publish the long one first; renderer adds a 16 s end-screen hold automatically.
     - No topic repeated within 14 days (incl. $ and ₹ versions of the same idea). The narrator never
       speaks as a person or claimed expert ("I", "as a financial advisor").
     - Allegations about real people/companies: always name the source, never in a title or thumbnail.
     - Localized titles keep brand/person names in Latin script (also in Hindi).
     - Shorts get a vertical thumbnail automatically (render.py make_short_thumb: badge + key number +
       title). If the auto-picked number isn't the key one, add an override in pipeline/short_thumbs.json.
   - **Retention rules (every video, 24 Nov 2026).** Goal: viewers watch to the end.
     - **Payoff before explanation.** No slow preambles ("hi guys", "in this video", "today we'll look at").
     - **Shorts hook:** first line ≤ 12 words (~2 s) opens on the biggest number, a contradiction or a
       surprising claim, plus an open loop the video answers later ("...so what went wrong?", "guess which").
       Scene 1's visual shows that number/claim, so frame 0 hooks.
     - **Shorts pacing:** ≤ 14 words per scene `say` (= a visual change every ~4 s); split longer lines into
       two scenes with different visuals; never the same visual type twice in a row. Put
       `assert len(s["say"].split()) <= 14` for every scene in the spec (copy the block in `035_nokia_fall.py`).
     - **Shorts re-hook** around the middle ("But here's the catch", "Now the twist") that opens a second loop.
     - **Shorts ending:** a short usable lesson, then a last line that flows back into the first line so the
       Short loops ("...Ask Nokia." -> "Nokia once sold..."). Keep the on-screen follow pill on the `cta`
       visual; never a spoken "follow/subscribe" line.
     - **Long hook:** the payoff number or claim inside the first 10 s; then a clear promise of what the viewer
       will learn; then a tease of the best reveal ("by the end, you'll see why..."). Intro ≤ ~60 s.
     - **Long chapters:** end each chapter's last scene with a one-line open loop into the next chapter
       ("So how do airlines keep going? Follow the miles."). A visual change at least every ~8 s.
     - Retention never beats accuracy: every number in a hook or tease is asserted or sourced; keep hedges.
5. **Check**: `python3 pipeline/preview.py <spec.json> <scratch dir>` and look at every sheet; fix overflow.
   `tools/render_batch.sh <ids...>`, then `python3 tools/voice_check.py` on each; fix real mispronunciations
   (not number formatting noise) and re-render.
6. Add the new ids and times to `pipeline/schedule.txt`, set their `queue.json` status to `rendered`,
   commit and push.
7. `tools/upload_pending.sh`. It stops at YouTube's daily upload limit (~10/day); the daily task finishes the rest.
8. Commit and push `pipeline/posted.json`. Report to the owner: what's scheduled, what you learned from analytics.

## B. Daily check (every day)
1. `tools/upload_pending.sh` (does nothing if all is uploaded; re-renders anything missing first).
2. Check every `posted.json` entry (not `superseded`) whose publish time has passed is `public` and
   processed; flag anything `rejected`/`failed` or a `MISSED SLOT` line.
3. Commit and push `posted.json` if it changed. Keep the run short when there is nothing to do;
   tell the owner only about problems or newly scheduled videos.

## C. News Short (Saturday)
1. Find this week's biggest global money/business story (economy, markets, a big company move) that a
   general audience cares about. Use 2+ reputable sources, check dates, and avoid politics framed as opinion.
2. Write `pipeline/specs/<next number>_news_<slug>.py` (same rules as A4, badge `MONEY NEWS`,
   explain it simply and say what it means for an ordinary person). Add localizations.
3. Preview, render, voice check; add to `schedule.txt` for **Sunday 22:30 IST**; run `tools/upload_pending.sh`;
   commit and push.

## Specialist agents (owner request, 23 Nov 2026)
The owner asked Claude to keep using the *appropriate* specialist agents (not every agent) to manage and improve the channel.
Use them as reviewers/helpers; Claude applies the changes itself so edits don't collide.
- Every weekly production run: before rendering, have a **Financial Analyst** agent fact-check the week's specs
  (MUST FIX items get fixed before upload); use **general-purpose** agents in parallel to write specs.
- Every 4 weeks (or when analytics show a drop): **Video Optimization Specialist** (hooks, titles, thumbnails, retention),
  **SEO Specialist** (search, titles, localizations), **Growth Hacker** (experiments from analytics),
  **Short-Video Editing Coach** (pacing, audio, captions). Reports go in `docs/reviews/<date>_<topic>.md`.
- When the pipeline code changes: **Code Reviewer**. Quarterly or when YouTube policy news appears: **Legal Compliance Checker**.
- When visuals/branding change: **Brand Guardian** (owner prefers simple, clean design).
Skip agents unrelated to a YouTube finance channel.

## Guardrails
- Our OAuth scopes are upload + read-only: **we cannot edit or delete a video after upload**.
  Get it right before uploading. If something already uploaded is wrong, tell the owner exactly which
  video to delete in Studio (title + date) and re-upload a fixed copy only after it's deleted.
- Never upload the same spec id twice (upload.py refuses; don't override with `--allow-repeat`
  unless the earlier copy is marked `superseded` in `posted.json`).
- Never print credentials. Never change channel settings. No paid promotion.
- Stay within the content rules in `CLAUDE.md`. When unsure about a fact, leave it out.
- If YouTube errors repeat (auth, quota, upload limit) for 2 runs, stop and notify the owner plainly.

## Optional upgrade (needs the owner, later)
Re-running `tools/get_youtube_token.py` with the broader `youtube` + `youtube.force-ssl` scopes would let
Claude also edit titles after upload, delete mistakes, build playlists and upload caption files.
Suggest it to the owner when they're back; don't block on it.

## Editing live videos and playlists
`tools/seo_live.py` (titles from specs, topic playlists) needs the youtube.force-ssl permission. The owner
granted it on 23 Nov 2026, but this long-running session still has the old token in its environment
(`seo_live.py check` prints NO_EDIT_PERMISSION). Fresh sessions get the new token, so run it there:
`create_session` with `source_url` = the money-channel repo and `source_revision` = claude/friendly-gates-8o3lq0,
asking it to run `./setup.sh` if needed, then `python3 tools/seo_live.py playlists` (and `titles <ids>` after a
title change), and to report the output only. `upload_pending.sh` also calls `playlists` at the end; it is
skipped quietly here.

