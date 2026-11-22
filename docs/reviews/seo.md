# SEO review: YouTube search discoverability (22 Nov 2026)

Week 2 is **not uploaded yet** (`posted.json`), so you can still change its titles. After upload, our scopes can't edit them. Already right: titles mostly under 60 characters with the search phrase first, hashtags capped at 4 + `#shorts`, `defaultLanguage`/`defaultAudioLanguage` = `en`, and localized descriptions keep the English sources.

## Top 10 recommendations (ranked)

1. **Stop the Netflix Short and long video from competing (30 Nov, same day).** `029` "Netflix vs Blockbuster: The $50 Million 'No'" and `L010` "Netflix vs Blockbuster: The $50M Deal That Got Away" go after the same query. Split them by YouTube autocomplete phrases. The long video owns "netflix vs blockbuster / why blockbuster failed". The Short owns "why blockbuster didn't buy netflix" (examples 1–2 below). Change `title` in `pipeline/specs/029_*.py` and `L010_*.py`, then re-run them. Apply the same split to later pairs: `035`↔`L012` Nokia, `032`↔`L011` Buffett, `038`↔`L013` Dhirubhai, `016`↔`L008`, `023`↔`L006`.

2. **Put the searched phrase first in the 5 week 2 titles that don't.** People search for these phrases, but they aren't at the start of these titles. Edit `title` in each spec:
   - `L005` → "How Airlines Make Money: $4.50 Profit Per Passenger"
   - `035` → "Why Nokia Lost the Smartphone War: 40% to Sold Off"
   - `028` → "Market Cap Explained: Why Microsoft Beats Walmart". Autocomplete has "market cap explained" but not "market cap vs revenue".
   - `036` → "How Instagram & Facebook Make Money: $63B in 3 Months". The $63B is Meta-wide, so a title naming only Instagram would mislead.
   - `031` → "72-Month Car Loan vs 48: The $2,734 Difference"

3. **Repeat the title's search phrase in the first 150 characters of the description.** Search results and the collapsed description show only the opening, and 5 week 2 specs don't do this. `L010` and `L005` start with a story, `035` starts "At the end of 2007…", and `038` starts with Reliance revenue, not "Dhirubhai Ambani". `029` doesn't either once its title changes. Add this rule to AUTOPILOT A4. Add a check in `upload.py` (`seo_lint(spec)`, called before `build_body`, warning in `--dry-run`): title ≤60 characters; the first 3 words of the title appear in `description[:150]`; 3–5 hashtags.

4. **Supply accurate English captions.** We already have the exact script and word timings (`render.py` word-synced captions), so writing an `<id>.en.srt` next to each mp4 is cheap. Uploaded captions get names and numbers right where auto-captions fail ("Zerodha", "Dhirubhai", "crore"). They also feed YouTube's caption auto-translate and give auto-dubbing a clean source. Evidence that captions improve search ranking is thin; it mostly comes from vendors. Uploading needs `captions.insert` with the `youtube.force-ssl` scope. **Owner action:** re-run `tools/get_youtube_token.py` with the broader scopes (already proposed in AUTOPILOT "Optional upgrade"). Until then, the owner can upload the .srt in Studio → Subtitles.

5. **Keep the 6 translation languages, and make sure auto-dubbing is on.** es, pt, hi, id, de and fr are exactly YouTube's "Expressive Speech" auto-dub languages (plus Italian), and translated titles can show in search for those speakers. But a Spanish title that opens English audio loses viewers fast. **Owner action:** Studio → Settings → Upload defaults → Advanced → allow automatic dubbing. Check retention by country in the Wednesday analytics, and drop any language that doesn't hold viewers after 3 weeks. Hindi: keep brand names in Latin script. `029` has "नेटफ्लिक्स बनाम ब्लॉकबस्टर" while `L010` correctly keeps "Netflix". Add this to the A4 rule.

6. **Build series with playlists, not title prefixes.** Don't add "Case Study:" to titles. It uses up the first, most-weighted words on a phrase nobody searches. Series identity already comes from the badge and the thumbnail `tag`. Add playlists, which show up in search and lengthen viewing sessions: Business Case Studies, Founder Stories, Money Math, How Markets Work, India Money Stories. **Owner action** in Studio (or Claude via API after the scope upgrade). Also make the series hashtag the 3rd hashtag every time (`#casestudy`, `#founderstory`, `#businessbreakdown`). It's 4th in `029`.

7. **Move chapters up and link related videos.** `build_body` adds chapters after the source list, which is about 20 lines in `L010` and far below the fold. Insert `Chapters` after the first paragraph instead (split `body` at the first `"\n\n"`). Add an optional spec field `"related": ["L010_netflix_blockbuster"]`: `build_body` looks up its URL in `posted.json` and adds "Full story: <url>". Upload the long video before its Short (fix order in `tools/upload_pending.sh`). Links in Shorts descriptions aren't clickable, so **owner action:** set each Short's "Related video" in Studio.

8. **Re-angle the weak or overlapping queue topics** (evidence: YouTube autocomplete, which shows that people search a phrase, not how many):
   - Strong, move up: `mcdonalds_real_estate` ("…real estate business model"), `ipl` ("how ipl makes money"), `kodak`, `wework`, `rent_vs_buy`, `insurance_types`, `mortgage_prepay`, `save_for_million`, `tata_nano`, `L014`, `L015`.
   - `quick_commerce` (marked usd): the searches are Indian ("10 minute delivery india"). Make it an INR India story: "How Blinkit and Zepto Deliver in 10 Minutes".
   - `side_income`: the searches are "side income ideas". Use "Is a $500/Month Side Hustle Worth It? 10-Year Math".
   - `online_income_ads` → "Make Money Online Courses: Why the $10K Ads Lie".
   - `crash_and_sip`: uses the Indian term SIP but is set to usd. Either INR "Should You Stop Your SIP in a Crash?" or US "Keep Investing in a Market Crash?".
   - `raise_vs_inflation`: competes with `027` and `033`. Merge it or drop it.
   - `dividends_buybacks`: little search interest. Use "Why Companies Buy Back Their Own Stock".
   - `bonds_friend`: title should start "Bonds Explained".

9. **Tags: low effort.** YouTube says tags play a "minimal role" except for misspellings. Keep 8–12 per video. Spend the time on misspellings for names: "dhirubai ambani", "zerodah", "warren buffet".

10. **Channel keywords and the old titles.** Add to the Studio keywords in `CHANNEL_DESCRIPTION.md`: "penny to billion", "business case studies", "how money works", "personal finance for beginners". The description's first line is already strong. **Owner action:** in Studio, remove "#shorts" from the titles of live `014`/`015` and scheduled `016`. Hashtags don't belong in titles, and A4 already says so.

## Five rewritten week 2 titles + description openers

1. **029 (Short):** "Why Blockbuster Didn't Buy Netflix for $50 Million"
   Opener: "Why didn't Blockbuster buy Netflix? In 2000, Netflix's co-founders say they offered the company for $50 million, and Blockbuster said no."
2. **L010 (long):** "Netflix vs Blockbuster: Why Blockbuster Really Failed"
   Opener: "Why did Blockbuster fail while Netflix grew to $45 billion a year? A Netflix vs Blockbuster case study: late fees, the $50M offer and 3 lessons."
3. **L005 (long):** "How Airlines Make Money: $4.50 Profit Per Passenger"
   Opener: "How do airlines make money? The world's airlines are expected to earn about $4.50 net profit per passenger in 2026. So what pays? Miles, bag fees and cargo."
4. **035 (Short):** "Why Nokia Lost the Smartphone War: 40% to Sold Off"
   Opener: "Why did Nokia lose the smartphone war? At the end of 2007 it sold about 4 in 10 of the world's phones; in 2013 it sold its phone business to Microsoft."
5. **028 (Short):** "Market Cap Explained: Why Microsoft Beats Walmart"
   Opener: "Market cap explained: share price times shares, not revenue. Walmart sells over twice as much as Microsoft, yet Microsoft is worth almost 4x more."

The numbers in these openers come from the current specs. Re-run each spec `.py` after editing.

## Sources
- Hashtags: https://support.google.com/youtube/answer/6390658
- Tags "minimal role": https://support.google.com/youtube/answer/146402
- Translated metadata in search: https://support.google.com/youtube/answer/4792576
- Auto-dubbing, 27 languages, Expressive Speech (4 Feb 2026): https://blog.youtube/news-and-events/youtube-auto-dubbing-expressive-speech/
- 3Play Media dubbing guide: https://www.3playmedia.com/blog/youtube-dubbing-guide/
- YouTube autocomplete (suggestqueries.google.com, ds=yt), checked 22 Nov 2026.
