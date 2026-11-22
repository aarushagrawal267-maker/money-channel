# Video optimization review (22 Nov 2026)

Scope: 27 rendered Shorts (40.7–55.2 s, median ~48 s), 6 long videos (8:09–10:04), thumbnails, upload flow.
Overall the production is strong: numbers are checked, chapters exist, the design is clean and descriptions read well.
The gaps are in **packaging and flow between videos**. Ranked by expected impact:

## 1. Shorts: show the payoff in frame 1 and sentence 1
- **What:** The first scene must state the result (biggest number or contrast) and show it on screen. Many Shorts open with set-up: 018 opens on a "pair" card (M and J circles, no number), 029 and 035 open with a year.
  - 018 now: "Two friends invest the same three hundred dollars a month. One ends up with more than double."
    → "Seven hundred and ninety thousand dollars, or three hundred and seventy thousand. Same three hundred a month. The only difference? Ten years." (open on the `compare` scene, drop the `pair` scene)
  - 029 now: "In two thousand, Netflix's founders say they offered…"
    → "Blockbuster could have bought Netflix for fifty million dollars, Netflix's founders say. It said no. Last year Netflix made forty-five billion."
  - 035 now: "At the end of two thousand seven, about four in every ten phones…"
    → "Four in every ten phones sold on Earth were Nokias. Six years later, Nokia sold its phone business to Microsoft." (2013 deal is already sourced in the spec)
- **Where:** `scenes[0]` in each Short spec; add the rule to `docs/AUTOPILOT.md` A4 ("scene 1 = the result, never a set-up card; no year as the first word").
- **Why:** The Shorts feed decides on "viewed vs swiped away" in the first 1–2 s. A number beats a set-up.

## 2. Shorts: 30–45 s, and end on a loop, not "Follow"
- **What:** Cut to ~85–110 words (math/explainer 30–40 s, stories ≤45 s). Drop the closing "Follow for one money lesson every day" (it's on every Short). End with a line that loops back into the first frame (e.g. 018: "…so which friend are you going to be?" then frame 1 again) or, for paired Shorts, a pointer to the long video (#3).
- **Where:** spec `scenes`; change AUTOPILOT A4 from "95–140 words" to "85–110".
- **Why:** Ranking is driven by percentage viewed and replays. A generic call to action in the last 3 s is where people swipe, and it's identical on every video (a risk under the repetitive-content rules).

## 3. Build a Shorts → long-video bridge
- **What:**
  1. Every long video gets 2 "satellite" Shorts made from its best chapter. Pairs that already exist: 029→L010, 022→L005, 020→L003, 018→L002, 032→L011 (next).
  2. Publish the long video **first**. Move 029 from Mon 30 Nov 22:30 to Tue 06:30 (swap with 030) so the link works on day one.
  3. The paired Short's last line: "The full nine-minute story is linked above."
  4. **Owner (Studio, about 1 min per Short):** Content → Short → Edit → "Related video" → choose the long video. This is the only clickable link a Short gets (description links in Shorts aren't clickable), and the API can't set it.
  5. Long descriptions: line 2 = "Watch next: <url>" for the previous long video in the same series. New spec field `watch_next: "L00x_id"`; `upload.py` looks the url up in `posted.json`.
- **Why:** Shorts views don't count toward the 4,000 watch hours needed to monetize. Long videos do, and a Short is the cheapest way to send viewers to them.

## 4. Long-video thumbnails: break the single template
- **What:** All four thumbnails are the same layout (gold number, 3–4 word line, red pill), with 6–8 words and no object. Keep the flat style but: (a) add one simple flat icon on the left 40% (membership card, VHS tape against a play button, plane, credit card); (b) at most 4 words: drop the pill, or drop the line; (c) the thumbnail should add to the title, not repeat it. Example for L001: icon of a membership card, "$5.9B IN FEES".
- **Where:** `thumbnail` field (new `icon` key) plus `render_long.py` thumbnail drawing. Run Brand Guardian before rollout (the owner rejected "too fancy" designs).
- **Why:** On the Home feed you compete with Two Cents, How Money Works and Logically Answered. Text-only thumbnails that all look alike blur together.

## 5. Long-video titles: search phrase first, ≤55 characters
- **What:** L001 is 64 characters and gets cut off on phones. Fix these before they upload (L001 has no live scheduled copy in `posted.json`; L005 uploads 4 Dec):
  - L001 → "How Costco Makes Money (It's Not the Groceries)"
  - L005 → "How Airlines Really Make Money: $4.50 a Passenger"
  - L010 is good. L004 ("How Credit Card Companies Really Make Money") is the model: start with the phrase people search.
- **Where:** `title` field; AUTOPILOT A4: "≤55 characters; start with 'How X makes money' or 'X explained' when that's the search phrase."

## 6. Long-video outro: 15–20 s, laid out for the end screen
- **What:** L010's outro card lasts 5.7 s and its centred text would sit under end-screen elements. Extend it to ~18 s, leave the left and right boxes empty, and replace "If you learned something, subscribe" with a spoken "Watch next: [series title]" line.
- **Owner (Studio, once per long video):** add an end screen with "Best for viewer" plus Subscribe. Use "Import from video" after the first one.
- **Where:** `render_long.py` `v_cta` plus the last scene of each long spec.
- **Why:** End screens are the biggest driver of session time. A 5 s outro barely gives room for one.

## 7. Turn pillars into named series with playlists
- **What:** Three recurring formats with fixed title patterns:
  - **"How X Really Makes Money"** (Costco, airlines, credit cards, UPI)
  - **"Rise & Fall"** case studies (Netflix/Blockbuster, Nokia, Kodak, WeWork)
  - **"Same Money, Different Result"** maths (25 vs 35, fees, DCA)

  Each long video ends by naming the next one in its series. A "Money News in 60s" playlist holds the Sunday news Shorts.
- **Where:** `queue.json` (add a `series` key). Playlists are owner-made in Studio (or ours after #8).
- **Why:** Series playlists autoplay into each other and give the algorithm a clear topic cluster to recommend from.

## 8. One owner session in Studio (~20 min) plus a scope upgrade
- **Studio:**
  - Set up Test & Compare on each long video's thumbnail, with 3 variants. Have `render_long.py` write `_thumb_b.png` and `_thumb_c.png`.
  - Set "Related video" on each paired Short (#3).
  - Add end screens (#6).
  - Pin one question comment per long video (e.g. L002: "Which lever surprised you most?").
- **Scope:** re-run `tools/get_youtube_token.py` with `youtube` + `youtube.force-ssl`. Claude can then build playlists, post comments and retitle videos that underperform. Already listed in AUTOPILOT "Optional upgrade". Promote it to a priority.

## 9. Backfill translations before upload
- **What:** 020–025 and L001–L003 have no `localizations` and haven't been uploaded yet. Add es/pt/hi/id/de/fr now. 016–019 are already up and can't be changed through the API.
- **Why:** Translated titles cost nothing and open Hindi, Spanish, Portuguese and Indonesian search. India alone is a large share of English finance viewers.

## 10. Measure weeks 1–3 and act on it
Add these to AUTOPILOT A1 (Analytics API unless noted):

| Signal | How | Action threshold |
|---|---|---|
| Short % viewed | `averageViewPercentage` per Short | <70% → cut length or rewrite the hook; >90% → keep that format |
| Swipe-away rate | Studio only (owner screenshot) | <60% "viewed" → hook problem |
| Long 30 s retention | `audienceWatchRatio` by `elapsedVideoTimeRatio` | <65% at 0:30 → rewrite intros; find the first cliff and fix that chapter type |
| Long CTR | Studio only (impressions CTR) | <4% after 1k impressions → swap thumbnail / Test & Compare |
| Subs per 1k views | `subscribersGained` / views | rank pillars; move the top 2 up in `queue.json` |
| Country mix | `country` dimension | if India >50%, test 08:30 IST Shorts; if US/UK lead, keep times |
| Traffic sources | `insightTrafficSourceType` | Shorts feed → long ("SHORTS" source) shows if #3 works |

**Timing and cadence:** keep the current slots. They're reasonable for US evening and UK teatime, and the Shorts feed matters more than the publish hour at 0 subscribers. Change only after 3 weeks of data, as the plan says. Keep 3 long videos a week only if each still gets the full check. If quality or checking slips, 2 well-packaged long videos beat 3.

## Also noticed
- `posted.json` notes contradict each other on L001: 3inj6_vZEkQ is called "the live copy" but marked private and superseded. Confirm in Studio which Costco copy goes live on 23 Nov.
