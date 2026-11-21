# Channel Setup Guide (step by step)

Total time: about 1.5 hours, done once. Do the parts in order.

---

## PART 1: Create the YouTube channel (about 30 minutes)

### Step 1: Create a separate Google account
1. Go to **accounts.google.com/signup** and create a new Gmail account just for the channel.
   This keeps the channel separate from your personal email, and makes it easier to sell or hand over later.
2. Turn on **2-Step Verification** at **myaccount.google.com/security**.
   This is **required** for YouTube monetization later, and it protects the channel from hackers.

### Step 2: Pick a channel name
- Short, easy to spell, and about money. Some ideas: *The Money Lesson*, *Money in Minutes*,
  *Compound Daily*, *Cents & Sense*, *Money Explained Daily*.
- Check that the **@handle** is free while you create it (Step 3 shows it).
- Check that nobody big already uses the same name: search it on YouTube.

### Step 3: Create the channel (as a Brand Account)
1. Log in to **youtube.com** with the new Gmail account.
2. Go to **youtube.com/account**, click **"Add or manage your channel(s)"**, then **"Create a channel"**.
3. Type your channel name and click **Create**.
   This creates a **Brand Account**: the channel has its own name, and you can add managers later without sharing your password.
4. Set your **@handle**: YouTube Studio → **Customization → Basic info → Handle**.

### Step 4: Verify your phone number
1. Go to **youtube.com/verify**, enter your phone number, and type in the code.
2. This unlocks **custom thumbnails**, **videos longer than 15 minutes** and live streaming.
   Thumbnails matter a lot for long videos, so don't skip this.

### Step 5: Channel settings (YouTube Studio → Settings, bottom left)
| Where | Set it to |
|---|---|
| **Channel → Basic info → Country of residence** | **India** (must be your real country; it matters for monetization and tax) |
| **Channel → Basic info → Keywords** | personal finance, investing, money, business, economics, financial literacy |
| **Channel → Advanced settings → Audience** | **"No, set this channel as not made for kids"** |
| **Upload defaults → Advanced settings → Category** | **Education** |
| **Upload defaults → Advanced settings → Video language** | **English** |
| **Upload defaults → Advanced settings → Comments visibility** | **Hold potentially inappropriate comments for review** (keeps scam bots out) |
| **Community → Automated filters → Blocked words** | whatsapp, telegram, whats app, +1, crypto advisor, investment manager, dm me, contact me |
| **Channel → Feature eligibility** | Check that "Intermediate features" is on (it is after phone verification) |

### Step 6: Branding (I'll make these, you upload them)
In **YouTube Studio → Customization → Branding**:
- **Profile picture:** 800×800 px
- **Banner:** 2560×1440 px (keep everything important in the centre 1546×423)
- **Video watermark:** 150×150 px (a small subscribe button in the corner of every video)

In **Customization → Basic info**:
- **Description:** I'll write it.
- **Contact email:** use the channel's Gmail address.

Tell me your channel name and I'll create all of these.

### Step 7: Rules to know before the first upload
- **AI disclosure:** when uploading, YouTube asks about "altered or synthetic content".
  For our chart and narration videos, the answer is normally **No**, because there are no realistic fake people or events.
  If we ever use realistic AI footage of people or real places, we answer **Yes**.
- **Shorts** must be **under 3 minutes** and vertical. Ours are about 45 seconds.

---

## PART 2: Let the pipeline upload for you (about 30 minutes)

### Step 8: Create a Google Cloud project
1. Go to **console.cloud.google.com**, logged in with the **channel's Gmail account**.
2. Accept the terms. At the top, click the project dropdown, then **New Project**.
   Name it `money-channel` and click **Create**. It's free and needs no credit card.

### Step 9: Turn on the YouTube API
1. Menu → **APIs & Services → Library**.
2. Search **"YouTube Data API v3"**, open it, click **Enable**.
3. Also search **"YouTube Analytics API"** and click **Enable**. We use it to find your best upload times.

### Step 10: Set up the consent screen
1. Menu → **APIs & Services → OAuth consent screen**. On newer screens this is called **Google Auth Platform**.
2. Click **Get started**:
   - **App name:** money-channel uploader
   - **Support email:** the channel's Gmail
   - **Audience:** **External**
   - **Contact email:** the channel's Gmail
3. Under **Audience**, click **"Publish app"** to move it from *Testing* to *In production*.
   **Important:** in *Testing* mode, Google expires your login every 7 days and uploads would stop.
   Since only you use the app, no Google review is needed. You'll just see an "unverified app" warning, which is normal.

### Step 11: Create the login key (OAuth client)
1. Menu → **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. **Application type:** **Desktop app**. Name: `uploader`. Click **Create**.
3. Click **Download JSON** and rename the file to **`client_secret.json`**.
   **Keep this file private.** Don't send it in chat and don't upload it anywhere.

### Step 12: Run the one-time authorization script (on your computer)
1. Install **Python 3** from **python.org**. On Windows, tick **"Add Python to PATH"** during install.
2. Get the script `money-channel/tools/get_youtube_token.py` from this session and save it
   in the **same folder** as `client_secret.json`.
3. Open a terminal in that folder (Windows: click the folder's address bar, type `cmd`, press Enter) and run:
   ```
   pip install google-auth-oauthlib
   python get_youtube_token.py
   ```
4. A browser opens:
   - Log in with the **channel's Gmail account**.
   - When asked which account or channel, **pick the channel name**, not your personal profile.
   - If you see **"Google hasn't verified this app"**, click **Advanced → Go to money-channel uploader**.
   - Allow the permissions.
5. The terminal prints **3 values**: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
   Keep the window open for Part 4.

### Step 13: Apply for public API uploads (10 minutes, then wait)
Videos uploaded through a new API project are **locked to private** until Google approves an audit.
1. Search **"YouTube API Services Audit and Quota Extension Form"** and open Google's official form.
2. Fill it in. **Tell me when you're there and I'll write every answer for you.**
3. Approval usually takes a few weeks. Until then we use **"batch and schedule"**:
   I make the videos, and you upload and schedule them in YouTube Studio (about 15 minutes a week).

---

## PART 3: GitHub, the channel's storage (about 15 minutes)

This session is temporary. GitHub stores the code, the topic list and the record of what's been posted,
so every scheduled run can continue where the last one stopped.

### Step 14: Create the repository
1. Create a free account at **github.com** if you don't have one.
2. Click **+ → New repository**.
   - **Name:** `money-channel`
   - **Visibility:** **Private**
   - Leave everything else empty and click **Create repository**.

### Step 15: Connect GitHub to Claude
1. Go to **https://claude.ai/connect-github** and connect your GitHub account.
2. Install the **Claude GitHub App** and give it access to the `money-channel` repository.
3. Tell me the repo name (like `yourname/money-channel`) and I'll save all the work into it.

---

## PART 4: Save the keys in your Claude cloud environment (about 5 minutes)

1. In this Claude session, open the **cloud environment menu** in the title bar, then click **Edit**.
2. Add these as **environment variables** (name = value), copied from the Step 12 terminal:
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`
3. Optional but recommended: get a free key at **pexels.com/api** and add `PEXELS_API_KEY`.
   It gives better background footage for long videos.
4. Under **Repositories** in the same settings, add the `money-channel` repo if the option is there.
5. Save. **New sessions** pick these up, so the scheduled runs will have them.

Never paste these values into the chat.

---

## PART 5: Monetization (later, when you qualify)

| Requirement | Details |
|---|---|
| **Subscribers** | 1,000 |
| **Plus one of** | 4,000 public watch hours in 12 months (long videos), **or** 10 million Shorts views in 90 days |
| **2-Step Verification** | On (done in Step 1) |
| **Google AdSense account** | One per person. Create it during the monetization application |
| **No active Community Guidelines strikes** | Keep content original and accurate |

When approved, submit your **US tax info in AdSense** (YouTube asks for it). Without it, more tax is held back on earnings from US viewers.

---

## Checklist: send me these (none are secret)

- [ ] Channel name and @handle
- [ ] Channel link
- [ ] GitHub repo name (e.g. `yourname/money-channel`)
- [ ] Confirmation that the 3 YouTube keys are saved in the environment settings
- [ ] Whether you added a Pexels key
- [ ] Tell me when you open the API audit form, so I can write the answers
