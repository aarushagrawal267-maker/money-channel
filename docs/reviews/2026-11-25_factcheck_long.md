# Fact check: L014 Apple 1997, L006 Inflation, L009 Rent vs Buy

Reviewer: financial-analyst agent, 25 Nov 2026. No spec files were edited.
Method: I re-ran all three specs in a scratch copy. All asserts pass, and the JSON in the repo matches the .py files.
I checked the sourced figures against primary sources where I could reach them: SEC EDGAR full text of Apple's
10-Ks for FY96–99 and FY26, BLS releases, FOMC statements, the Fed's Longer-Run Goals PDF, the FDIC, NAR, the Zillow
releases, Freddie Mac, ATTOM, NerdWallet and Clever. For L009 I re-ran the model with variant inputs.

Verdicts: **MUST FIX** means a spoken or on-screen claim is wrong or misleading. **SHOULD FIX** means it is accurate
but imprecise, missing a caveat, or likely to go stale. **OK** means it is verified.

---

## L014_apple_1997 (airs Mon 7 Dec, 23:30 IST)

### MUST FIX
None. Every figure from the filings matches EDGAR. See OK below.

### SHOULD FIX
1. **The chronology in Chapter 1 is reversed.** The current text is: "Lenders noticed. In October nineteen ninety-seven,
   Standard and Poor's cut … Apple needed a new one, fast. So it went shopping." This puts the NeXT purchase after the
   October 1997 downgrade, but Apple agreed to buy NeXT in December 1996, ten months earlier. Replace the last three
   sentences with: "And its old operating system was falling behind. Back in late nineteen ninety-six, Apple had
   already gone shopping for a new one." Update the `LOOPS` assert to match.
2. **"Cost cuts came first" leaves out the product that did sell.** The current text is: "Notice the profits started
   before the iMac even shipped. Cost cuts came first." The FY98 10-K lists the Power Macintosh G3 line, launched in
   November 1997, which was selling in Q1 FY98 when Apple made $47M. Say: "Notice the profits started before the
   iMac even shipped. Cost cuts came first, helped by a faster Power Mac G3 line launched in late nineteen
   ninety-seven."
3. **"Last year" is ambiguous in December 2026.** The current text is "Last year, Apple's profit was about a hundred and
   thirty-two billion dollars." In December 2026, "last year" would mean calendar 2025, and FY25 net income was
   $112.0B. Say: "In its latest fiscal year, which ended in September, Apple's profit was about …"
4. **The "nearly sixty-eight times" revenue growth is not adjusted for inflation.** FY97 revenue was $7.081B and FY26
   revenue was $478.834B. US prices roughly doubled over that period: the CPI-U averaged 160.5 in 1997 and was about
   331 over Oct 2025–Sep 2026. In real terms the growth is about 33×. Add "before inflation" to the speech or the
   table title, plus a description line: "Dollar figures are not adjusted for inflation; US prices roughly doubled
   between 1997 and 2026."
5. **"Real growth came from the software it bought in nineteen ninety-six" has two problems.** The deal was signed in
   1996 but closed in February 1997, and the sentence overstates software's role (the iPod and iPhone were hardware).
   Say: "Real growth would come later, built on the software it agreed to buy in nineteen ninety-six." Update the
   loop assert.
6. **The employee counts in the "then and now" table measure different things.** The 8,437 figure is regular
   employees and excludes 1,739 temporary staff and contractors (FY97 10-K). The 167,000 figure is full-time
   equivalents (FY26 10-K). This is optional; one fix is a table note: "1997: regular employees; 2026: full-time
   equivalent."

### OK
- **Financials, FY95–98 (FY97 and FY98 10-Ks).** Sales $11,062M / $9,833M / $7,081M / $5,941M. Losses −$816M and
  −$1,045M, then +$309M. FY97 quarterly losses (−120, −708, −56, −161), with Q4 FY96 at +$25M. FY98 quarterly
  profits 47 / 55 / 101 / 106.
- **Cash.** Cash and short-term investments were $1,745M, $1,459M and $2,300M.
- **NeXT.** Total cost $427M, of which $375M was written off as in-process R&D.
- **Ratings and turnover.** S&P cut Apple's debt to B− (senior) and CCC (subordinated) in October 1997. The filing
  warns of "significant voluntary employee turnover".
- **Microsoft.** The filing describes Microsoft as "an important developer of application software", and the deal
  was non-voting preferred stock.
- **Board.** "Replacing all but two former directors" on Aug 6, 1997.
- **Product line.** "Approximately 15 separate individual products to three main product families".
- **Inventory.** $437M → $78M, days of supply 31 → 6, and the cash flow line shows $359M.
- **iMac.** 278,000 units, 33% of Q4 FY98 Mac units. About 1.8M sold in FY99, and the four product lines appear in
  the FY99 10-K.
- **Employees.** 10,896 / 8,437 / 6,658, down 38.9%.
- **Officers.** Cook joined from Compaq in March 1998. Rubinstein joined in February 1997 and was formerly VP of
  Hardware Engineering at NeXT. Tevanian came from NeXT. Anderson joined in April 1996.
- **FY26 10-K.** Revenue $478,834M, net income $132,175M, iPhone $254,098M (53%), Services $123,301M, about 167,000
  full-time equivalent employees.
- **Quotes.** The D8 "90 days" quote (TNW, Jun 2, 2010) is correctly labelled as Jobs' recollection. Maclean's
  reported "boos and jeers" and the "let go of the notion" quote.
- **Compliance.** There are no stock tips. The team framing (rather than a lone hero) and the hindsight caveat are
  good.

---

## L006_inflation (airs Wed 9 Dec, 23:30 IST = 13:00 ET; the FOMC decision is 9 Dec at 14:00 ET, November CPI is 10 Dec)

### MUST FIX
1. **The "housing" weight is mislabelled.** The current text is: "Housing is the biggest piece, about thirty-six
   percent." In BLS terms, 35.625 is **Shelter**. The **Housing** major group is **44.469** (Relative importance,
   CPI-U, Dec 2025: https://www.bls.gov/cpi/tables/relative-importance/2025.htm). Say: "Shelter, meaning rent and
   the rental value of owned homes, is the biggest piece, about thirty-six percent." The visual already says
   "Shelter".
2. **The Fed rate story skips the 2024–25 cuts, and goes stale an hour after publish.** The current text is: "…to five
   and a quarter to five and a half percent by July twenty twenty-three. And this September, with inflation elevated
   again, it raised rates to between three and three-quarters and four percent." "Raised to 3.75–4%" right after
   "5.5%" reads as nonsense, because the Fed cut to 3.50–3.75% in between. The Sep 16, 2026 statement says it "decided
   to raise the target range … by 1/4 percentage point to 3-3/4 to 4 percent"; it held on Oct 28, 2026 (10–2). The
   Dec 8–9 decision is announced one hour after this video goes live.
   - **Speech:** "…by July twenty twenty-three. It cut rates in twenty twenty-four and twenty twenty-five. Then this
     September, with inflation elevated again, it raised them a quarter point, to between three and three-quarters
     and four percent, where they stood in early December."
   - **Timeline:** add an event `{"when": "2024–25", "text": "Cuts to\n3.5%–3.75%"}`, or change the last event to
     "+0.25 pt to\n3.75%–4%".
   - **Description:** "Fed rate as of 8 Dec 2026."
   - **Sources:** https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm and
     https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm

### SHOULD FIX
1. **The fixed-rate borrower "win" needs the unexpected-inflation caveat.** The current text is: "Inflation quietly
   moves value from lenders to fixed-rate borrowers." Lenders price expected inflation into the rate, so the transfer
   comes mainly from inflation that is higher than expected. Add: "…especially when inflation turns out higher than
   expected when the loan was made." In the mortgage example, say "your principal and interest payment is two
   thousand dollars a month". Property tax and insurance paid into escrow are not fixed.
2. **The I bond rate wording.** The current text is "For I bonds bought from November twenty twenty-six to April twenty
   twenty-seven, the rate is five point five one percent." It is 5.51% only for the bond's first six months: the 1.40%
   fixed part lasts for the bond's life, and the inflation part (about 4.1%) resets. Say: "…they start at five point
   five one percent, including a one point four percent fixed part that lasts for the life of the bond." TreasuryDirect,
   confirmed by Tipswatch, Oct 30, 2026.
3. **The 20-year chart and the "three homes" table are before tax.** Interest on savings is taxable, so after tax a
   3.5% rate barely keeps up with 3% inflation. Add "before tax" to the chart note and to the table title.
4. **"Prices rose 3.7% in a year" will be superseded on 10 Dec.** The visuals already date it as Sept 2026, which is
   fine. Re-check the Sept-2026 framing if the video is re-published after the November CPI release.

### OK
- **September 2026 CPI** (BLS, Oct 14, 2026, not seasonally adjusted): all items 3.7%, index 336.940, core 2.6%,
  energy 20.4%, gasoline 34.2%. Sept 2025 index 324.800. The "$360, not $370" maths is correct.
- **October 2026 CPI** (BLS, Nov 10, 2026): "BLS cannot publish 12-month percent changes for October 2026…" The next
  release is Dec 10, 8:30 ET.
- **June 2022** (9.1%, the largest since November 1981, energy 41.6%, gasoline 59.9%) and the annual averages
  2015–2025 (Minneapolis Fed).
- **1913 vs 2025.** CPI 9.9 → 321.9 = ×32.5 (3.2% a year, about 3¢ left).
- **BLS FAQ.** "About 80,000 items each month", "more than 200 categories", "over 90 percent".
- **Fed goals.** The Longer-Run Goals statement was adopted Jan 24, 2012 and reaffirmed Jan 27, 2026, and contains
  "primarily determined by monetary policy" and "with a lag". FOMC moves: Mar 2022 and Jul 2023.
- **St. Louis Fed.** The three reasons are from economist David Wheelock, and the post notes that economists don't all
  agree.
- **Real earnings** (BLS): Sep 2026 average hourly earnings +3.0%, CPI-U +3.7%, real −0.7% (seasonally adjusted).
  Jun 2022: −3.6%.
- **FDIC savings rate** 0.39% (Nov 16, 2026).
- **I bonds** 5.51% / 1.40%, with the $10K, 12-month and 3-month rules. TIPS facts are correct.
- **Compliance.** The investment wording ("historically", "can fall sharply", "not advice") is fine.

---

## L009_rent_vs_buy (airs Fri 11 Dec)

### MUST FIX
1. **"We assume it stays within that" contradicts the model's own numbers.** The current text (Chapter 5) is: "The
   buyer's home profit is tax-free only within the IRS exclusion: up to two hundred fifty thousand dollars, or five
   hundred thousand for a married couple. We assume it stays within that." In the model, the gain is (sale price −
   6%) − (price + 3% buying costs). That gain passes **$250K in year 19** and **$500K in year 29**: $303K at break-even
   (year 21) and $528K at year 30. Re-running the model with tax on the excess (15% above the exclusion):
   - Single filer: break-even moves to **year 22**, and the year-30 lead falls from $130K to **about $88K**.
   - Married couple: break-even stays at year 21, and the year-30 lead is **about $126K**.

   The fix is to make the example buyers a married couple and to tax the gain above $500K:
   - **Model:** add `- CGT * max(0, v*(1-SELL_COST) - price*(1+BUY_COST) - EXCL_JOINT)` to `b_nw`.
   - **Speech:** "…or five hundred thousand for a married couple. Our example is a married couple, so it stays
     within that until almost the end. A single owner would pass the limit around year nineteen, and break even
     about a year later."
   - **Year-30 line:** "…the buyer is ahead by about a hundred and twenty-five thousand dollars."
   - **Visual:** in the stat_grid, change "0% · tax on home profit" to sub "married couple, gain up to $500K".
   - **Description:** replace "at year 21 our example gain is above the single limit" with the single-filer
     figures above.
   - **Asserts:** update them.
   - **Source:** IRS Topic 701.
2. **The Zillow comparison puts the gap down to rates, which is wrong.** The current text is: "Back in June, when rates
   were lower, Zillow estimated buying pays off in about six years nationally." The visual note reads: "Freddie Mac
   rate then 6.48%, now 7.28%". Viewers will conclude that our 20 years against Zillow's 6 is because of rates. It
   isn't. Our own model at 6.48% still gives **12 years**. Zillow's estimate was **8.4 years at its October 2023 peak**,
   when rates were around 7.6–7.8% (same release). The main driver is the price input: Zillow's typical home value for
   October 2026 is **$364,812** (ZHVI, Zillow October market report, Nov 5, 2026), against the NAR median sale price
   of $421,900.
   - At $364,812 (price-to-rent 13.6), our model gives **9 years**.
   - At $364,812 and 6.48%, it gives **6 years**, which matches Zillow.

   Fix:
   - **Speech:** "Real cities show the same spread. Zillow's own model put the national break-even at about six
     years in June. It uses Zillow's lower typical home value and its own assumptions; plug that value into our
     model and we get about nine years at today's rate. In Columbus, Ohio, about four…"
   - **Visual note:** "Zillow's model and inputs differ from ours".
   - **Hook and Chapter 1:** say "at the median sale price" wherever "today's typical price" or "typical home today"
     is used. One caveat: ZHVI includes condos, so a single-family-only value would sit somewhat higher.
   - **Source:** https://zillow.mediaroom.com/2026-06-04-Rent-or-buy-How-long-it-takes-for-buying-a-home-to-pay-off-in-each-metro

### SHOULD FIX
1. **The hook overclaims "one number".** The current text is "It depends on one number most buyers never check." The
   model's own sensitivity table shows that ±1 percentage point on home-price growth (10 years or 30) or on investment
   return (14 years or never) moves the answer as much as the price-to-rent ratio does. Say: "It depends on a few
   numbers, and the biggest one most buyers never check." In Chapter 7, change "How long you stay and your local
   prices decide most of it" to "…decide a lot of it."
2. **The rate will be out of date.** "At today's mortgage rates" and "7.28% on November nineteenth" will be three weeks
   old by the time the video airs, and Freddie Mac publishes on Dec 3 and Dec 10. Re-check the Dec 10 release. Each
   0.25 percentage point moves the break-even by about 1–2 years: at 6.26% it is 10 years, and at 6.48% it is 12.
   Keep "on November nineteenth" in the speech, and change the hook visual sub to "Nov 19, 2026 rate".
3. **"Renting a similar home?" / "The same kind of home".** ZORI measures typical asking rents (single-family), while
   NAR's median is a sale price, so the two are not the same homes. Say "Renting a single-family home?"
4. **Renters insurance is left out, and Zillow's model includes it.** The effect is small (about $15–20 a month). One
   word in the rules bullet would cover it. This is optional.

### OK
- **NAR, October 2026** (Nov 12, 2026): single-family median $421,900, up 0.4%. The all-types median is also up 0.4%,
  so "+0.4%" holds for single-family too.
- **Zillow, Nov 12, 2026:** typical single-family rent $2,243, up 3.2% (ZORI).
- **Zillow, Jun 4, 2026:** 6.0 years nationally, Columbus 4.1, San Diego 23.3. In San Francisco, San Jose and New
  Orleans, buying never pays off within 30 years.
- **Freddie Mac:** 7.28% (Nov 19), 6.26% a year earlier, 6.48% (Jun 4).
- **Costs:** ATTOM 0.9% (Apr 9, 2026), NerdWallet $2,564, Clever 5.46% (includes the buyer's-agent fee), Redfin 2–5%,
  IRS Topics 409 and 701.
- **Arithmetic.** Payment $2,309.35, year-1 interest $24,465 and principal $3,248, all-in owning cost $3,191,
  unrecoverable costs $3,406 → $2,351 after price growth, fees at 5 years $42K, price-to-rent 15.67, break-even year 21,
  sensitivities (3 / 5 / 10 / none; 9 / 10 / 30 / 14 / none).
- **Compliance.** Assumptions are labelled on screen, there is a disclaimer, and the "invest the difference" caveat is
  included. Nothing in it reads as advice.
