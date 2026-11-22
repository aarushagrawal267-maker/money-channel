# Compliance review: Penny to Billion (22 Nov 2026)

Scope: CLAUDE.md, CONTENT_PLAN.md, AUTOPILOT.md, upload.py, schedule.txt, 11 specs, live privacy page. Risk review, not legal advice; use a lawyer before any sponsorship or if a complaint arrives.

## HIGH

**1. Monetization (YPP) "inauthentic content", including the 2026 "AI personas on sensitive topics" rule.**
YouTube renamed "repetitious" to "inauthentic content" on 15 Jul 2025. It does not monetize "AI-generated content made with generic or unoriginal templates giving the impression of mass production" [1]. In July 2026 it added a category for AI personas presented as experts on sensitive topics, and finance is one of them. A disclosure label does not make such a channel eligible [2][3]. We publish 17 automated videos a week, one voice, one template. 28 of 34 Short specs end with the same line ("Follow for one money lesson every day"). Near-duplicates are scheduled close together: 001/018 (start early, ₹ vs $, 25 and 27 Nov), 013/014 (minimum-due trap), 029 + L010 (Netflix, both on 30 Nov) and 020 + L003 (index funds, same week).
Fixes:
- Script rule (AUTOPILOT A4): the narrator never speaks as a person or expert. No "I", no host name, no "as a financial expert", no personal advice ("you should buy").
- Queue rule: no topic repeated within 14 days across Shorts and long videos. A ₹/$ version of the same topic needs 4+ weeks between them and different examples. Move 018 and 029 to later dates.
- In each spec, choose the CTA from a pool of 8+ lines, and `assert` that no CTA repeats within 7 days. Vary the closing "The lesson" scene.
- Owner, before applying for YPP: review a sample; consider narrating long videos in his own (or own-cloned) voice, which needs no disclosure [4]; consider 1 Short/day until approved.
- Add to the channel About text and every description: "Researched and written with AI tools, checked against the sources listed, narrated with a synthetic voice." Honest, and shows there is no fake human expert.

**2. Errors that cannot be corrected (misleading or scam policy exposure).**
Our scopes cannot edit or delete videos; news Shorts and machine-translated titles publish unreviewed, so a wrong number stays public until the owner deletes it. YouTube's spam and scam policy covers misleading metadata and thumbnails, and any "get rich quick" framing [5].
Fixes:
- In the spec template, `assert` that every digit group in `localizations[*].title` also appears in the English title or description.
- News Shorts: two independent sources must agree on every number before the video is written. If they do not, skip the slot.
- Have a second agent fact-check each spec before `schedule.txt`.
- Owner: re-run `get_youtube_token.py` with `youtube.force-ssl` so mistakes can be fixed same day.

## MEDIUM

**3. Disclaimers are too weak to rely on.**
The on-screen disclaimer is 24–26 px dim text in the header (render.py:438, render_long.py:457), which is hard to read on a phone. Specs 017, 022, 023, 035, 036 have no advice line (acceptable: no returns shown). A disclaimer never fixes misleading content; protection comes from staying impersonal and general (US publisher's exclusion) and outside "advice"/"financial promotion" (India, UK).
Fixes:
- upload.py: `sys.exit` if a spec in pillars 1–3, or one that shows returns, has no "not financial advice" or "not investment advice" in its description.
- Renderer: when `disclaimer` mentions returns, show it for 2 s as a full-width line at 40 px or larger.

**4. India SEBI finfluencer rules (the owner is Indian, we publish Hindi titles and India stories).**
Since 29 Aug 2024, SEBI-regulated entities (brokers, AMCs, advisers) may not associate with unregistered people who give securities advice or make return claims [6]. SEBI's 29 Jan 2025 circular allows pure education only if it uses no share-price data from the last 3 months [7]. Current specs are fine (030, 038 use results, not prices).
Fixes (script rules):
- Use no Indian share price, price chart or ticker newer than 3 months. Watch the queued "IPO listing gains" and "Nifty/Sensex" topics.
- Make no return or performance claim about a named security.
- Accept no sponsorship, referral or affiliate link from SEBI-registered entities, including the companies we cover such as Zerodha. The same goes for UK firms: under FCA FG24/1 [8] that turns a video into a "financial promotion".
- If any paid link is ever added, disclose it inside the video and above the description fold. This follows the FTC Endorsement Guides [9] and India's CCPA influencer guidelines.

**5. Real people and companies (defamation, publicity rights).**
038 repeats Reuters' report of "accusations" that Dhirubhai Ambani manipulated government policy. Attributed and balanced: acceptable. But India's BNS s.356 Expl. 1 allows criminal defamation of a dead person when the words are meant to hurt the family [10].
Rules:
- Every allegation names its source in the spoken line ("Reuters reported…").
- Include the person's or company's response when one exists.
- Never put an allegation in a title or thumbnail.
- Use "reported" or "accused", never a flat statement.
- Living founders: only filings, their own words, major outlets.
- No photos, likeness, voice imitation or implied endorsement; quotes read as attributed narration ("Randolph wrote…").

**6. The `containsSyntheticMedia=false` setting.**
False is correct today. YouTube requires disclosure only for realistic content (a real person doing/saying what they didn't, realistic real places or events, AI-generated music); unrealistic animation, AI-assisted scripts and captions are exempt [4]. India's IT Amendment Rules 2026 (in force 20 Feb) cover only content indistinguishable from a real person or event and exclude good-faith educational materials [11]. Kokoro `af_heart` is a stock voice, not a copy of any real person, and the music is procedural (`make_music`).
Fixes:
- build_body: `sys.exit` unless the spec sets `contains_synthetic_media` explicitly whenever any visual type falls outside the renderer's chart and text types (for example images, footage or maps).
- Script rule: set it to true for any AI image or video that looks real, any re-enactment, any cloned voice other than the owner's, and any AI-generated music.

## LOW

**7. Trademarks.** Text-only thumbnails naming companies are nominative use. Rule: no logos, brand colours/typefaces, product photos or "official".

**8. Copyright.** Procedural music, Inter (OFL), short attributed quotes: fine. Rule: no news footage, screenshots of articles, or other channels' clips (also "reused content" [1]).

**9. Made for kids.** `False` is correct (adult topics). No cartoon mascots or kid-style themes.

**10. Privacy policy site.** The live page (main branch) still says "Money Mechanics" and has no section on how long data is kept or how it is deleted.
Fixes:
- Update the branch to "Penny to Billion" and add: "We store only an OAuth refresh token, privately. Revoke it at myaccount.google.com/permissions; nothing else is retained." Then merge the branch.
- Rename the app on the Google consent screen to match.

## Sources
[1] support.google.com/youtube/answer/1311392 · [2] TechCrunch 20 Jul 2026 (YouTube clarifies AI-slop policies) · [3] Tubefilter 13 Jul 2026 (inauthentic-content update) · [4] support.google.com/youtube/answer/14328491 · [5] support.google.com/youtube/answer/2801973 · [6] Inc42, SEBI association ban (2024) · [7] Business Standard 30 Jan 2025 (SEBI circular) · [8] fca.org.uk FG24/1 · [9] ftc.gov Disclosures 101 for influencers · [10] devgan.in/bns/section/356 · [11] Nishith Desai Associates, India SGI amendments (Feb 2026)
