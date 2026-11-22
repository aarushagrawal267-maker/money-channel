# Growth plan: Penny to Billion (review, 22 Nov 2026)

**Headline:** the monetisation target moved. From **1 Feb 2027**, new channels need **1,000 subs + 8,000 long-form watch hours (12 months)** or **20M Shorts views (90 days)** ([YouTube blog](https://blog.youtube/news-and-events/new-opportunities-to-earn-and-changes-to-the-youtube-partner-program/)). We can't reach the old 4,000-hour bar in 10 weeks, so plan for 8,000. Shorts watch time doesn't count toward those hours. **Long videos make the money; Shorts bring subscribers and testing data.**

## Ranked actions (impact ÷ effort)

| # | Action | Who | Impact | Effort |
|---|---|---|---|---|
| 1 | Better long-video packaging: thumbnail + title written before the script, A/B tested | Claude | Very high | Low |
| 2 | Each week, cut 2–3 Shorts from that week's long video and link them to it | Claude + owner (link) | High | Low |
| 3 | Recurring series + playlists (section 3) | Claude / owner | High | Low |
| 4 | Re-authorise broader scopes (Studio step D) | Owner, once | High | 10 min |
| 5 | Run the 6-week experiment grid (section 2) | Claude | High | Medium |
| 6 | Comment-spam filter (step A) | Owner, once | Medium (trust) | 5 min |
| 7 | Channel layout + trailer (step B) | Owner, once | Medium | 10 min |
| 8 | Text article per long video on the website | Claude | Medium, slow | Low |
| 9 | Re-post Shorts as Reels; LinkedIn post for case studies | Owner | Low–medium | Medium |

## 1. What gets a new channel from 0 to monetised, and when

1. **Long-form click-through × retention.** One long video picked up by search or suggested is worth more than 50 average Shorts. Rough maths: 8,000 h = 480,000 min. At about 3.5 min watched per view, that's **~137k long-form views a year, ~900 per long video** at 3 a week. Most channels get there because 2–3 videos keep pulling views for months, not because every video does well.
2. **Shorts for subscribers.** Rule of thumb: 1–3 subs per 1,000 Shorts views, so 1,000 subs ≈ 0.3–1M Shorts views. Check this against our own numbers by week 3.
3. **Series and binge paths.** Playlists, end screens and Short→long links turn one view into several.
4. **Looking authentic.** The YPP review checks for "inauthentic", mass-produced content. Real sourcing, varied visuals and opinionated analysis protect the channel's approval. That matters more than posting volume.

**Realistic timeline (from 0):** 1,000 subs in **month 2–6** (needs at least one Short above 100k views). 8,000 hours in **month 8–14** if long videos average ~900 views. Many faceless channels never make it. The deciding factor is whether case-study and "how X makes money" long videos get a CTR above 4% and keep 35%+ of viewers. If Shorts take off instead, the 20M-views route is possible but rare.

## 2. Experiments, weeks 1–6

Weeks 1–2 are already rendered. Tag them afterwards (hook type, length, title style) and treat them as the **baseline**. Changes start with the week-3 specs (written Wed 25 Nov). Test one variable per Short. Spread each test's versions evenly across pillars so the topic doesn't skew the result.

| Weeks | Variable | Arms | Primary metric | Secondary |
|---|---|---|---|---|
| 1–6 | Pillar / topic | all 7 pillars | views at 7 days | subs per 1k views |
| 3–4 | Hook (first sentence) | surprising number / direct question / story cold open ("In 2000, Blockbuster could have bought Netflix…") | engagedViews ÷ views | averageViewPercentage |
| 4–5 | Short length | 25–34 s / 45–55 s | averageViewPercentage | subs per 1k views |
| 3–6 | Title style | number first ("$7,600 to pay off $5,000") / question / plain search phrase | views at 7 days | subs per 1k views |
| 3–6 | Slot | 06:30 vs 22:30 IST (already running) | views at 72 h | country mix |
| 2–6 | Long titles/thumbnails | search phrase ("How Costco Makes Money") vs story ("The $50M 'No' That Killed Blockbuster") | Test & Compare watch-time share, CTR | avg view duration |

**Reading it from the API** (`youtubeAnalytics.reports.query`, ids=channel==MINE):
- Per video: `dimensions=video`, `filters=creatorContentType==SHORTS` (or `VIDEO_ON_DEMAND`), metrics `views,engagedViews,averageViewPercentage,averageViewDuration,estimatedMinutesWatched,subscribersGained,likes,shares`.
- Age-normalise: query `dimensions=day&filters=video==ID` and add up days 0–6. Never compare a 2-day-old video with a 3-week-old one.
- Hook strength: `dimensions=elapsedVideoTimeRatio`, metrics `audienceWatchRatio,relativeRetentionPerformance`, one video per call. Read the drop before ratio 0.1. Studio's "viewed vs swiped away" isn't in the API, so engagedViews÷views stands in for it.
- Traffic and audience: `insightTrafficSourceType` (SHORTS, YT_SEARCH, RELATED_VIDEO, BROWSE…), `country`.
- Impressions and CTR aren't in the Analytics API. Create a **YouTube Reporting API** job for the reach report (`channel_reach_basic_a1`; check the name in the docs) under the same read-only scope. It only covers dates from job creation onward, so **create it now**.

**Decision rule:** each version needs at least 6 videos. Compare medians, not averages. Act only if one version leads by **25% or more on the main metric in 2 separate weeks** and doesn't lose on the secondary metric. Record every decision in `docs/analytics/`. Expect about 1 test in 3 to produce a clear winner. "No difference" is a valid result: keep the cheaper option.

**Frequency check (week 4):** if the weaker Shorts slot's median is under 40% of the stronger one's, drop to 1 Short a day plus the news Short. Spend the saved effort on long videos.

## 3. Series that compound

Each series gets a playlist, a fixed on-screen badge and a consistent title format:
1. **How They Make Money:** Costco, airlines, credit cards, Visa, Spotify. A long video plus 2 cutdown Shorts.
2. **Billion-Dollar Mistakes:** Blockbuster, Nokia, Kodak, WeWork, Yahoo, Toys "R" Us. This is the weekly case-study long video, the most proven faceless format.
3. **Founder Files:** sourced "age when it happened" timelines (Buffett after 50, Knight, Blakely, Dhirubhai, Murthy). No myths.
4. **Penny to Billion Math:** our signature. Scale and compounding visuals ("a penny doubled for 30 days", "how long $1 billion lasts at $1M a day"). Brand recall plus a strong channel trailer.
5. **Money Trap #N:** numbered financing traps (minimum payment, BNPL, car loans, whole life).
6. **Sunday Money News:** same slot every week, so it becomes a habit.

## 4. Topics most likely to reach a global audience

- **From the queue, prioritise:** Kodak, WeWork, McDonald's real estate, Apple profit, Phil Knight, Spanx, save for $1M, rent vs buy, "$10K a month online" ads are lies, term vs whole life, car loan cost, free apps. Long: L012 Nokia, L014 Apple 1997, L011 Buffett, L009 rent vs buy.
- **India stories that work worldwide:** UPI, Tata Nano (a failure story), Dhirubhai, IPL.
- **Deprioritise:** Zerodha, no-cost EMI, Amul, minimum_due_in (repeats the US Short). Reframe quick_commerce globally ("Why 10-minute delivery keeps losing money": Getir, Gopuff, sourced).

**10 new topics:**
1. **A penny doubled for 30 days vs $1M today**: the brand's signature Short; shows how compounding back-loads.
2. **How long would $1 billion last?** Spend $1M a day and the scale becomes concrete. Highly shareable.
3. **Costco's $1.50 hot dog since 1985**: what inflation says it "should" cost, and why it's a loss leader.
4. **The Big Mac Index**: what burger prices say about currencies (The Economist data). Works in every country.
5. **How Visa makes money without lending a cent**: a toll-booth model with very high margins (10-K).
6. **Yahoo said no to $44.6B**: Microsoft's 2008 offer vs the 2017 sale to Verizon. A Billion-Dollar Mistakes episode.
7. **LEGO's near-collapse and comeback**: too many products, then focus. Taken from LEGO's annual reports.
8. **The 4% rule, explained**: huge US/UK search demand. Show the maths and its limits, no advice.
9. **Why prices end in .99**: the left-digit effect, with academic sources. Pure curiosity, works everywhere.
10. **Toys "R" Us**: how a leveraged buyout's debt sank a profitable brand. Teaches leverage.

**Seasonal:** "New-year money reset" maths in week 6 (28 Dec – 3 Jan). US tax season Jan–Apr. India Budget on 1 Feb as the news Short.

## 5. Owner one-time steps in YouTube Studio (studio.youtube.com, computer)

**A. Block scam comments (5 min).** Finance channels attract "contact my advisor on WhatsApp" bots.
1. Settings → Community → Automated filters.
2. Under Blocked words, add: whatsapp, telegram, wa.me, t.me, investment manager, account manager, crypto expert, signal app.
3. Set "Hold potentially inappropriate comments for review" to **Increase strictness**. Save.

**B. Channel layout (10 min).**
1. Customization → Layout.
2. "Channel trailer for people who haven't subscribed" → Add → pick the long video with the most views (Costco for now).
3. "Featured video for returning subscribers" → Add → the newest long video.
4. Featured sections → Add section: Popular videos, Shorts, then each series playlist. Publish.

**C. Playlists (15 min; skip if you do D).**
1. Content → Playlists → New playlist.
2. Create these as Public, using the series names in section 3: How They Make Money, Billion-Dollar Mistakes, Founder Files, Penny to Billion Math, Money Traps, Sunday Money News.
3. Add the matching videos.

**D. Give Claude more permissions (10 min, most useful).** When you're back, Claude will prepare an updated `tools/get_youtube_token.py`. Run it like last time and approve. Claude can then build playlists and fix titles itself.

**E. Check advanced features.** Settings → Channel → Feature eligibility → if "Advanced features" isn't on, verify your phone number. This unlocks title/thumbnail testing.

**F. Weekly, about 10 min (optional but valuable):**
1. **End screens:** Content → long video → Editor → End screen → "Import from video" (the first time: add "Best for viewer" video + Subscribe) → Save.
2. **Short → long link:** Content → Shorts → pencil → "Related video" → choose the matching long video → Save.
3. **Test & Compare:** Content → long video → thumbnail → "Test & compare" → add the extra thumbnails Claude leaves in `output/`.

## 6. Off-YouTube distribution (legitimate, low effort)

1. **Website articles (Claude, zero owner effort):** turn each long script, charts and sources into a page on the GitHub Pages site with the video embedded. This brings Google search traffic, and embedded plays count. Fresh sessions can't push to the Pages repo, so do it from the main session.
2. **Instagram/Facebook Reels (owner, 20 min every 2 weeks):** schedule the same Short files in Meta Business Suite.
3. **LinkedIn (owner, 5 min a week):** share the case-study long video with 3 takeaways. That audience fits business stories.
4. **Reddit/Quora:** only genuine answers that follow each forum's rules. No automated posting. Low priority.

**Avoid:** sub-for-sub groups, "comment X to get Y" prompts, misleading thumbnails, and mass-messaging friends. All of these hurt reach or break policy. Real questions to viewers are fine.
