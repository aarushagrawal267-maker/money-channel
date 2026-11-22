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

1. **Long-form CTR × retention.** 8,000 h = 480,000 min. At ~3.5 min watched per view that's **~137k long views a year, ~900 per long video**. In practice 2–3 videos that keep pulling search/suggested views carry the total.
2. **Shorts for subscribers.** Rule of thumb: 1–3 subs per 1,000 Shorts views, so 1,000 subs ≈ 0.3–1M Shorts views. Check against our data by week 3.
3. **Binge paths.** Playlists, end screens and Short→long links turn one view into several.
4. **Looking authentic.** YPP review checks for mass-produced "inauthentic" content. Real sourcing, varied visuals and opinionated analysis matter more than volume.

**Realistic timeline:** 1,000 subs in **month 2–6** (needs at least one Short above 100k views). 8,000 hours in **month 8–14** if long videos average ~900 views. Many faceless channels never get there. What decides it: long videos reaching 4%+ CTR and keeping 35%+ of viewers. The 20M-Shorts route is possible but rare.

## 2. Experiments, weeks 1–6

Weeks 1–2 are already rendered: tag them (hook, length, title style) as the **baseline**. Tests start with the week-3 specs (Wed 25 Nov). Spread each test's versions evenly across pillars so topic doesn't skew results.

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
- Age-normalise: `dimensions=day&filters=video==ID`, sum days 0–6. Never compare videos of different ages.
- Hook strength: `dimensions=elapsedVideoTimeRatio`, metrics `audienceWatchRatio,relativeRetentionPerformance` (one video per call); read the drop before ratio 0.1. "Viewed vs swiped away" is Studio-only, so engagedViews÷views stands in.
- Traffic/audience: `insightTrafficSourceType` (SHORTS, YT_SEARCH, RELATED_VIDEO…), `country`.
- Impressions/CTR aren't in the Analytics API. Create a **Reporting API** job for the reach report (`channel_reach_basic_a1`; verify name) with the same read-only scope. Data starts at job creation, so **create it now**.

**Decision rule:** at least 6 videos per version; compare medians; act only if one leads by **25%+ on the primary metric in 2 separate weeks** without losing on the secondary. Log decisions in `docs/analytics/`. Expect ~1 test in 3 to find a winner; on "no difference", keep the cheaper option.

**Frequency check (week 4):** if the weaker Shorts slot's median is under 40% of the stronger one's, drop to 1 Short a day plus news, and spend the effort on long videos.

## 3. Series that compound

Each series gets a playlist, a fixed on-screen badge and a consistent title format:
1. **How They Make Money:** Costco, airlines, credit cards, Visa, Spotify. A long video plus 2 cutdown Shorts.
2. **Billion-Dollar Mistakes:** Blockbuster, Nokia, Kodak, WeWork, Yahoo, Toys "R" Us. This is the weekly case-study long video, the most proven faceless format.
3. **Founder Files:** sourced "age when it happened" timelines (Buffett after 50, Knight, Blakely, Dhirubhai, Murthy). No myths.
4. **Penny to Billion Math:** our signature. Scale and compounding visuals ("a penny doubled for 30 days", "how long $1 billion lasts at $1M a day"). Brand recall plus a strong channel trailer.
5. **Money Trap #N:** numbered financing traps (minimum payment, BNPL, car loans, whole life).
6. **Sunday Money News:** same slot every week, so it becomes a habit.

## 4. Topics most likely to reach a global audience

- **Prioritise from the queue:** Kodak, WeWork, McDonald's real estate, Apple profit, Phil Knight, Spanx, save for $1M, rent vs buy, "$10K a month online" lies, term vs whole life, free apps. Long: L012 Nokia, L014 Apple 1997, L011 Buffett, L009 rent vs buy.
- **India stories that travel:** UPI, Tata Nano (failure story), Dhirubhai, IPL.
- **Deprioritise:** Zerodha, no-cost EMI, Amul, minimum_due_in (repeats the US Short). Reframe quick_commerce globally ("Why 10-minute delivery keeps losing money": Getir, Gopuff).

**10 new topics:**
1. **A penny doubled for 30 days vs $1M today**: signature Short; compounding is back-loaded.
2. **How long would $1 billion last at $1M a day?** Makes scale concrete; very shareable.
3. **Costco's $1.50 hot dog since 1985**: its inflation-adjusted price, and loss leaders.
4. **The Big Mac Index**: what burger prices say about currencies (Economist data).
5. **How Visa makes money without lending a cent**: a toll-booth model (10-K margins).
6. **Yahoo said no to $44.6B**: Microsoft's 2008 offer vs the 2017 Verizon sale.
7. **LEGO's near-collapse and comeback**: too many products, then focus (annual reports).
8. **The 4% rule, explained**: big US/UK search demand; maths and limits, no advice.
9. **Why prices end in .99**: the left-digit effect, academically sourced.
10. **Toys "R" Us**: how buyout debt sank a profitable brand.

**Seasonal:** "new-year money reset" in week 6; US tax season Jan–Apr; India Budget (1 Feb) as the news Short.

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

**D. More permissions for Claude (10 min, most useful).** When you're back, Claude prepares an updated `tools/get_youtube_token.py`; run it like last time and approve. Claude can then build playlists and fix titles itself.

**E. Advanced features.** Settings → Channel → Feature eligibility → if "Advanced features" is off, verify your phone. This unlocks title/thumbnail testing.

**F. Weekly, ~10 min (optional, valuable):**
1. **End screens:** Content → long video → Editor → End screen → "Import from video" (first time: add "Best for viewer" + Subscribe) → Save.
2. **Short → long link:** Content → Shorts → pencil → "Related video" → matching long video → Save.
3. **Test & Compare:** Content → long video → thumbnail → "Test & compare" → add Claude's extra thumbnails.

## 6. Off-YouTube distribution (legitimate, low effort)

1. **Website articles (Claude, no owner effort):** each long script + charts + sources as a page on the GitHub Pages site with the video embedded. Brings Google traffic; embedded plays count. Do it from the main session (fresh sessions can't push there).
2. **Instagram/Facebook Reels (owner, 20 min every 2 weeks):** schedule the same Short files in Meta Business Suite.
3. **LinkedIn (owner, 5 min a week):** the case-study long video plus 3 takeaways.
4. **Reddit/Quora:** genuine answers only, following each forum's rules; no automation. Low priority.

**Avoid:** sub-for-sub groups, "comment X to get Y" prompts, misleading thumbnails, mass-messaging friends. They hurt reach or break policy. Genuine questions to viewers are fine.
