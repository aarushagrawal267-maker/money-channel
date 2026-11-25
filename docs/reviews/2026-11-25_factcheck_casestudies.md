# Fact-check: case-study Shorts 042 / 047 / 052 (25 Nov 2026)

Scope: `pipeline/specs/042_kodak`, `047_sara_blakely`, `052_wework` (.py constants/asserts + .json say/visuals/title/description/localizations). JSONs match the .py files. No files edited.

Overall: every spoken number checks out against primary or reputable sources. There are no factual errors in the English scripts. Two fixes are needed before upload (both in 047), plus some optional caveats.

---

## 042_kodak: "Kodak Invented the Digital Camera. Then It Lost to It"

**MUST FIX:** none.

**SHOULD FIX**
- Sales/margin compare (scene 8 visual, description): $15.97B (1996) vs $6.02B (2011) and 48% vs 15% are not like-for-like. The 1996 figures include businesses Kodak later sold, for example the Health Group (sold to Onex in 2007 for up to $2.55B, with about $2.54B in revenue; Kodak 8-K, Jan 10, 2007). Add to the description: "1996 figures include businesses Kodak later sold, such as its Health Group (2007)." The on-screen visuals can stay.
- `localizations.es.summary`: "pero el cine fotográfico seguía pagando las cuentas" ("cine" means cinema) → "pero la película fotográfica seguía pagando las cuentas".

**OK**
- Sasson 1975 prototype: 100×100 px, 3.6 kg ≈ 8 lb, 23 s to record to tape, first photo Dec 1975 (IEEE Spectrum; ETHW milestone). Sasson received the 2009 National Medal of Technology for the digital camera, so "invented" in the title is defensible.
- 1996 10-K: sales $15,968M, COGS $8,326M, so gross margin is 47.9%, rounded to 48% (EDGAR FY1996 10-K).
- 2011 10-K: net sales $6,022M; cost of sales $5,135M; gross profit $887M; "gross profit margin 15%" (2010: 27%). Chapter 11 filed Jan 19, 2012; dedicated-capture phase-out announced Feb 9, 2012, 21 days later, so "weeks later" is right.
- 2005: No. 1 in the US with a 24.9% share (IDC via AP/NBC, Feb 9, 2006). Note that IDC counts shipments, so "top seller" is fine.
- Emerged Sept 3, 2013 (8-K).

---

## 047_sara_blakely: "Sara Blakely: $5,000 in Savings to Billion-Dollar Spanx"

**MUST FIX**
1. Hook (scene 1 `say`) states an estimate as fact. Billionaire status was a Forbes estimate, and Forbes/Fortune later put her below $1B (2020–21), which the description itself admits. Current text: `"Five thousand dollars in savings. Twelve years later: a billionaire. How?"` → `"Five thousand dollars in savings. Twelve years later, Forbes said: billionaire. How?"` (12 words, meets the hook ≤12 assert; total 96 words). Source: Forbes World's Billionaires, Mar 2012 (via The Week / Marketplace, Mar 14, 2012); Fortune, Sept 20, 2025 (net worth fell below $1B in 2020). Scene 6 can stay as is, or become "By twenty twelve, she was on Forbes' billionaires list." to avoid repeating the line.
2. `localizations.hi.title`: "Sara Blakely: 5,000 डॉलर की बचत से अरबों की Spanx". "अरबों" means "worth billions" (plural), which overstates a $1.0–1.2B valuation. Change to "Sara Blakely: 5,000 डॉलर की बचत से अरब डॉलर की Spanx". Source: Reuters via CNBC, Oct 20, 2021 ($1.2B valuation).

**SHOULD FIX**
- `localizations.id.title`: "Spanx Miliaran" (= "billions") → "Spanx Bernilai $1 Miliar". Same reason as the Hindi title.
- Scene 7, "she'd never taken a single outside investor": true as of 2012 (Forbes: "owns 100% ... zero debt, has never taken outside investment"). The visual title "(Forbes, 2012)" carries the date, so this is fine. Don't reuse the line without the date, because Blackstone bought a majority stake in 2021. Fortune's 2025 piece repeats "never had a single investor" without reconciling this.

**OK**
- $5,000 savings; founded 2000 at age 29; 7 years selling fax machines door to door; national sales trainer at Danka; mills said no, then one agreed; Oprah's Favorite Things, Nov 2000; $4M then $10M in sales (company figures, attributed to Fortune). Sources: Fortune Sept 20, 2025; CNBC Apr 3, 2019; CNN Oct 21, 2021.
- Forbes 2012: youngest self-made woman billionaire, age 41 (born Feb 1971). Spanx valued at about $1B by four banks, corroborated by Forbes.
- Blackstone, Oct 2021: majority stake at a $1.2B valuation; price undisclosed; Blakely kept a significant stake (Reuters/CNBC; CNN).
- Lesson is usable, and the script contains no hero-worship.

---

## 052_wework: "WeWork: From a $47B Valuation to Bankruptcy"

**MUST FIX:** none.

**SHOULD FIX**
- Scene 3 net loss: $1.93B is the consolidated net loss in the S-1, which includes noncontrolling interests. The net loss attributable to WeWork was $1,610,792K, and many outlets report "$1.6B". Viewers may comment that the figure is wrong, so add to the description: "($1.93B total net loss; $1.61B attributable to WeWork shareholders)."
- Scene 5 visual sub: "as of June 30, 2019 · IPO filing" → "undiscounted, ~15-yr leases · June 30, 2019 · S-1". This makes clear that $47.2B is nominal future rent, not a present value that can be compared with the $47B valuation.
- Scene 7 bars label "Left over" (26%) can read as profit, but WeWork was still loss-making. Change it to "Everything else".
- Scene 8 visual: the assets/liabilities are "as of June 30, 2023" (Reuters). Title "Chapter 11 filing, Nov 2023" → "Chapter 11 filing (June 30, 2023 figures)", or add that wording as a sub.

**OK**
- $47B valuation after a $2B SoftBank round, Jan 8, 2019 (Reuters/Euronews; Bloomberg). The private-round caveat is shown.
- S-1 (Aug 14, 2019): 2018 revenue $1,821,751K and net loss $(1,927,419)K, so $1.06 lost per $1 of revenue. US initial lease terms are "approximately 15 years". Lease obligations are $47.2B undiscounted as of June 30, 2019 (verified on EDGAR).
- IPO withdrawn Sept 30, 2019, after the filing "failed to generate enthusiasm" (AP). Neumann stepped down Sept 24 (NPR). No allegations are made.
- Chapter 11 filed Nov 6, 2023 (NJ). Reuters: assets $15.06B, liabilities $18.66B, and space took 74% of Q2 2023 revenue. Emerged June 2024 (AP).
