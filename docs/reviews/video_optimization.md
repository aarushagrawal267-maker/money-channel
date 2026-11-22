# Video optimization review (22 Nov 2026)

Reviewed: 27 Shorts (40.7–55.2 s, median ~48 s), 6 long videos (8:09–10:04), thumbnails, upload flow.
The numbers, chapters and design are solid. The gaps are in **packaging and in moving viewers from one video to the next**. Ranked by expected impact:

## 1. Shorts: show the payoff in frame 1 and sentence 1
- **What:** Scene 1 states the result and shows the number on screen. Right now many open with set-up: 018 opens on a "pair" card with no number, and 029/035 open with a year.
  - 018: "Two friends invest the same three hundred dollars a month…"
    → "Seven hundred and ninety thousand dollars, or three hundred and seventy thousand. Same three hundred a month. The only difference? Ten years." (open on the `compare` scene, drop `pair`)
  - 029: "In two thousand, Netflix's founders say…"
    → "Blockbuster could have bought Netflix for fifty million dollars, Netflix's founders say. It said no. Last year Netflix made forty-five billion."
  - 035: "At the end of two thousand seven, about four in every ten phones…"
    → "Four in every ten phones sold on Earth were Nokias. Six years later, Nokia sold its phone business to Microsoft." (the 2013 deal is already sourced in the spec)
- **Where:** `scenes[0]` of each Short spec. Add a rule to AUTOPILOT A4: "scene 1 = the result; never a set-up card or a year first."
- **Why:** The Shorts feed scores "viewed vs swiped away" on the first 1–2 s.

## 2. Shorts: 30–45 s, ending on a loop instead of "Follow"
- **What:**
  - Target ~85–110 words: 30–40 s for maths, ≤45 s for stories.
  - Drop the "Follow for one money lesson every day" line that closes every Short.
  - End on a line that loops into frame 1 (018: "…so which friend will you be?") or, for paired Shorts, a pointer to the long video (#3).
- **Where:** spec `scenes`. In AUTOPILOT A4, change "95–140 words" to "85–110".
- **Why:** Percentage viewed and replays drive Shorts reach. A call to action that's the same on every video is where people swipe away, and repeating it across all Shorts adds risk under the repetitive-content policy.

## 3. Shorts → long-video bridge
- **What:**
  1. Every long video gets 2 Shorts cut from its best chapter. These pairs already exist: 029→L010, 022→L005, 020→L003, 018→L002, 032→L011.
  2. Publish the long video first. Swap 029 (Mon 30 Nov 22:30) with 030 (Tue 06:30).
  3. The Short's last line: "The full nine-minute story is linked above."
  4. **Owner, in Studio:** Short → Edit → "Related video" → choose the long video. Links in Shorts descriptions aren't clickable, and the API can't set this field.
  5. In long-video descriptions, make line 2 "Watch next: <url>". Use a new spec field `watch_next`, and have `upload.py` resolve it from `posted.json`.
- **Why:** Only long-form watch time counts toward the 4,000 hours needed to monetize.

## 4. Long-video thumbnails: one object, ≤4 words
- **What:** All 4 thumbnails use the same layout: a gold number, a 3–4 word line and a pill, 6–8 words in all, with no object.
  - Keep the flat style.
  - Add one simple icon on the left 40%: a membership card, a VHS tape next to a play button, a plane, a credit card.
  - Cut the text to ≤4 words.
  - Make the thumbnail add to the title rather than repeat it. Example for L001: card icon + "$5.9B IN FEES".
- **Where:** `thumbnail.icon` in the spec, drawn by `render_long.py`. Have Brand Guardian check it, since the owner rejected "too fancy".
- **Why:** Home-feed competitors (Two Cents, How Money Works) have stronger visuals. Identical text-only thumbnails blur together.

## 5. Long-video titles: search phrase first, ≤55 characters
- **What:** Fix these before they upload. L001 is 64 characters, gets cut off on phones, and has no live scheduled copy yet.
  - L001 → "How Costco Makes Money (It's Not the Groceries)"
  - L005 → "How Airlines Really Make Money: $4.50 a Passenger"
  - L004 ("How Credit Card Companies Really Make Money") is the model to follow.
- **Where:** the `title` field. Add the rule to AUTOPILOT A4.

## 6. Long-video outro: ~18 s, end-screen safe
- **What:** L010's outro lasts 5.7 s, and its centred text would sit under the end-screen boxes. Extend it to ~18 s, leave the left and right areas empty, and replace "If you learned something, subscribe" with "Watch next: [series title]".
- **Owner, in Studio:** end screen with "Best for viewer" + Subscribe. Use "Import from video" after the first one.
- **Where:** `v_cta` in `render_long.py` and the last scene of each long spec.
- **Why:** End screens are the main lever for session time. A 5 s outro barely fits one.

## 7. Named series and playlists
- **What:** Three formats with fixed title patterns, each long video naming the next one in its series:
  - "How X Really Makes Money": Costco, airlines, cards, UPI
  - "Rise & Fall": Blockbuster, Nokia, Kodak, WeWork
  - "Same Money, Different Result": 25 vs 35, fees, DCA

  Plus a "Money News in 60s" playlist.
- **Where:** a `series` key in `queue.json`. The owner creates the playlists (or Claude does, after #8).
- **Why:** Playlists autoplay, and a clear topic cluster feeds suggested views.

## 8. One owner session in Studio (~20 min) + scope upgrade
- **Test & Compare** on each long video's thumbnail. `render_long.py` should also write `_thumb_b` and `_thumb_c`.
- **Related videos** (#3) and **end screens** (#6).
- **Pin one question comment** per long video (L002: "Which lever surprised you most?").
- **Scope upgrade:** re-run `tools/get_youtube_token.py` with `youtube` + `youtube.force-ssl`. Claude could then make playlists, post comments and retitle videos that underperform. Move this from "Optional upgrade" to a priority.

## 9. Translations before upload
020–025 and L001–L003 have no `localizations` and are not uploaded yet. Add es/pt/hi/id/de/fr now. (016–019 are already up, so they're locked.) Translated titles cost nothing and open Hindi, Spanish, Portuguese and Indonesian search.

## 10. Weeks 1–3: measure, then act (add to AUTOPILOT A1)

| Signal | Source | Act when |
|---|---|---|
| Short % viewed | `averageViewPercentage` | <70% → shorten or re-hook; >90% → repeat the format |
| Swipe-away | Studio only (owner) | <60% viewed → hook problem |
| Long 0:30 retention | `audienceWatchRatio` × `elapsedVideoTimeRatio` | <65% → rewrite intros; fix the first cliff |
| Long CTR | Studio only | <4% after 1k impressions → new thumbnail |
| Subs per 1k views | `subscribersGained`/views | move the top 2 pillars up in `queue.json` |
| Country | `country` | India >50% → test 08:30 IST Shorts |
| Traffic source | `insightTrafficSourceType` | Shorts → long views show whether #3 works |

**Timing:** keep the current slots. At 0 subscribers the Shorts feed matters more than the hour you publish. Revisit after 3 weeks. If checking quality slips, 2 well-packaged long videos a week beat 3.

**Also:** `posted.json` calls 3inj6_vZEkQ "the live copy" of L001 but also marks it private and superseded. Confirm in Studio which Costco copy goes live on 23 Nov.
