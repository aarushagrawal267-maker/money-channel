# YouTube API audit form: answers to copy

**Why we need this:** Google locks every video uploaded through the API to **Private** until the project passes this audit. After approval, our scheduled uploads can go public on their own. Until then, I upload as Private and you click "Public" (or schedule) in YouTube Studio.

**Form link:** https://support.google.com/youtube/contact/yt_api_form

**Before you start (5 minutes):**
1. **Merge the website update.** The audit checks the privacy policy and terms pages. (Claude will tell you how; once done, these must open:
   https://aarushagrawal267-maker.github.io/privacy.html and https://aarushagrawal267-maker.github.io/terms.html)
2. **Rename the app on the consent screen** so every name matches:
   Google Cloud Console → project `money-channel` → **APIs & Services → OAuth consent screen → Branding** → App name: `Money Mechanics Uploader`. Also set **Application home page** to `https://aarushagrawal267-maker.github.io`, **Privacy policy** to `https://aarushagrawal267-maker.github.io/privacy.html`, and **Terms of service** to `https://aarushagrawal267-maker.github.io/terms.html`. Save.
3. **Find your project number:** Cloud Console → top-left project picker → `money-channel` → the **Dashboard** shows "Project number" (only digits). Write it down.
4. **Take 2 screenshots of the consent screen setup** (needed for "OAuth flow screenshots"):
   - the **Branding** page after step 2;
   - the **Data Access** page showing the 3 scopes (youtube.upload, youtube.readonly, yt-analytics.readonly).
5. Have these files from the repo folder `docs/audit/` ready to upload (Claude made them):
   `01_homepage.png`, `02_privacy_policy.png`, `03_terms_of_service.png`, `04_upload_script.pdf`.
   (If the website looks different after merging, Claude can retake them.)

Fill in the parts in **[brackets]** yourself. Everything else, copy exactly.

---

## Section 1: Request type
- **Reason:** `Complete a compliance audit to request for additional quota`
  (This is the option for a first audit. Later we choose "No change" for quota, because we only need the Private lock removed.)

## Section 2: Organization and contact
1. **Applying as:** `As an individual user`
2. **Full legal name:** [your name as on your ID]
3. **Organization's legal name:** `self`
4. **Parent company:** leave empty
5. **Primary website:** `https://aarushagrawal267-maker.github.io`
6. **Address:** Country `India`, then [your street, city, state, PIN code]
7. **Category:** `Education and E-Learning`
8. **Organization size/type:** `Independent Developer/Sole Proprietor`
9. **Primary contact:** [your name], [the channel's Gmail address]
10. **Technical contact:** tick `Same as Primary Contact`
11. **Business contact:** tick `Same as Primary Contact`

## Section 3: Business model
12. **Describe your organization's work as it relates to YouTube** (copy all):

> I run Money Mechanics (https://www.youtube.com/@MoneyMechanics-v7t), an educational YouTube channel that explains personal finance, how markets work and how businesses make money, using animated charts and narration. I publish two YouTube Shorts per day and three longer videos per week.
>
> My API client, "Money Mechanics Uploader", is a private command-line script that only I use. It is not offered to anyone else and has no other users. It uses the YouTube Data API v3 to upload my own finished videos to my own channel (videos.insert with a resumable upload), set their custom thumbnail (thumbnails.set), set the title, description, tags, category (Education), made-for-kids status (not made for kids) and a scheduled publish time (status.publishAt). It then reads back my own video's processing status (videos.list) and my own channel's basic details (channels.list). Read-only YouTube Analytics access is used only to look at my own channel's views by hour so I can choose better upload times.
>
> The tool does not access any other user's account or data, does not collect viewer data, does not download or redistribute YouTube content, and does not display YouTube content anywhere. Credentials are stored privately and never shared.
>
> I am requesting the audit because uploads from my unverified API project are locked to private. I would like my own scheduled uploads to be able to go public at their scheduled time. I am not asking for more quota; the default quota is enough.

13. **Target audience:** tick only `Internal Users`
14. **How does your API client make money:** tick `Free service (we do not charge users)`
15. **Google/YouTube representative:** `No, I do not have a Google representative`
16. **How did you learn about the API:** `Google Developer Documentation`
17. **Content Owner ID:** leave empty
18. **Google Ads Customer ID:** leave empty

## Section 4: API client overview
19. **API Client name:** `Money Mechanics Uploader`
20. **Contains "YouTube"?** `No, the name does not contain "YouTube"`
21. **Primary access URL:** `https://aarushagrawal267-maker.github.io`
22. **Privacy policy URL:** `https://aarushagrawal267-maker.github.io/privacy.html`
23. **Terms of service URL:** `https://aarushagrawal267-maker.github.io/terms.html`
24. **Publicly accessible?** `No`
25. **Demo account credentials:** leave **empty**. Never give out your Google password.
26. **Login URL:** leave empty
27. **Special instructions** (copy):

> This is a private, owner-only command-line tool with no web interface or login page, so there is no demo account. The complete upload script is attached (04_upload_script.pdf). It authenticates with OAuth 2.0 (installed-app flow) as the channel owner, uploads a video with videos.insert, sets the thumbnail with thumbnails.set, and records the uploaded video ID so the same video is never posted twice.

28. **Acknowledgment:** tick the box.

## Section 5: Use case and quota
29. **How many project numbers:** `1`
30. **Google Cloud project number:** [the digits from "Before you start" step 3]
31. **Use case category:** tick `Video Uploading & Account Management`
32. **Requires sign in with Google (OAuth 2.0)?** `Yes`
33. **Derived metrics and data storage:** leave unticked (we don't publish derived metrics).
34. **Expected API usage:** `Fewer than 1,000 requests per day`

**Uploads:**
- **Privacy policy screenshots:** `02_privacy_policy.png`
- **Homepage screenshot:** `01_homepage.png`
- **Terms of service documentation:** `03_terms_of_service.png`
- **OAuth flow screenshots:** your 2 consent-screen screenshots from "Before you start" step 4
- **Upload interface screenshots / script:** `04_upload_script.pdf` (the form allows "a complete, working upload script" instead of a screencast)

**Endpoints (tick these):**
- `youtube.videos.insert`
- `youtube.thumbnails.set`
- `youtube.videos.list`
- `youtube.channels.list`

35. **Total quota requested:** `No change / Default quota (10k quota points)`

If the form still asks for a justification or a per-day number, use:
- **Total per day / justification:** `Default (10,000 units). About 3 uploads a day (2 Shorts + up to 1 long video), each with one thumbnails.set and a few videos.list calls to confirm processing.`
- **youtube.videos.insert per day:** `5` with justification `Up to 3 of my own videos a day, plus room for one re-upload if a file fails.`
- **youtube.search.list per day:** `0` with justification `Not used.`

---

**After you submit:** Google emails within a few days to a few weeks, sometimes with questions. Forward or paste the questions to Claude (never passwords or keys) and I'll draft the replies.
