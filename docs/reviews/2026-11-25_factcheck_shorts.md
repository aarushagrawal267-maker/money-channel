# Fact-check: Shorts 041–054 (25 Nov 2026)

Reviewer: financial-analyst agent (Morgan). No files edited. I ran a copy of every spec in the scratchpad: all asserts pass and the regenerated JSON is identical to the repo JSON for all 11.
Sources were checked live on 25 Nov 2026 unless a line says otherwise.

**Summary:** 1 Short has MUST FIX items (049 Amul). 7 have SHOULD FIX items. 3 are clean (041, 048, 051).

---

## 041_save_for_million: OK
Annuity math checks out: $380.98 / $555.23 / $1,234.46 a month, x3.24, $182,870 put in, $817,130 growth, and $306,557 in today's money at 3% inflation. The 7% is nominal and compounded monthly (7.23% effective), and the description says so. The disclaimer is present.

## 043_side_income: SHOULD FIX
- Math OK: $85,526 total, $25,526 of growth, $190 in year 1, $5,380 in year 10. Uses 7% effective (041 uses 7% nominal, a small inconsistency across the channel). IRS Topic 554 figures (12.4% + 2.9%, $400 threshold) are correct.
- **SHOULD:** The hook `"Five hundred a month on the side: eighty-five thousand dollars, or zero?"` is a false binary, because spending the money buys $60K of goods. Suggest `"Five hundred a month on the side: spent, or eighty-five thousand dollars?"` (12 words).

## 044_apple_profit: SHOULD FIX
- All 10-K figures match the FY2026 10-K on EDGAR (aapl-20260926.htm): products $355,533M, services $123,301M, total $478,834M, GM $139,659M (39.3%) / $93,943M (76.2%), net income $132,175M. The 10-K says the products GM rose "primarily due to product mix and tariff refunds". The fiscal year has 364 days, so $4,203 a second and $363M a day are correct. Services are 25.8% of sales and 40.2% of gross profit.
- **SHOULD:** `"Why? Every phone needs new parts. Software costs far less to deliver."` Services is not just software. It includes licensing (e.g. Google's search-default payments), advertising, AppleCare and payments, and licensing is close to pure margin and isn't paid by loyal customers. This framing also weakens the "loyal customer pays again and again" lesson. Suggest `"Why? Every phone needs new parts. Services like the App Store cost far less to deliver."` (14 words), and add to the description: "Services also include licensing, such as payments from Google to be the default search engine."

## 045_no_cost_emi: SHOULD FIX
- Verified:
  - **SBI Card worked example** (sbicard.com/sbi-card-en/assets/docs/html/personal/offers/calculator/cal-tc.html): ₹35,000, 6 months, 14%, cashback 3.96% = ₹1,386, loan ₹33,614, EMI ₹5,833, total ₹35,000. The page also says "due to RBI guidelines on usage of this term, SBI Card does not promote this as 'No Cost'".
  - **RBI circular RBI/2013-14/292** (17 Sept 2013): the "camouflaged … processing fee" and "the very concept of zero percent interest is non-existent" quotes are correct.
  - **HDFC:** ₹99–₹699 + GST, and GST is applied to the interest component.
  - **FX:** ₹93.44 on 18 Nov 2026 (PTI / Telangana Today, provisional; ThePrint gives 93.41). The ≈ $375 figure is fine.
  - **Math:** EMI 5,833, GST ₹249.48.
- **SHOULD:** `"Plus a processing fee: H-D-F-C lists ninety-nine to six hundred ninety-nine rupees."` Many no-cost offers waive the fee, and other HDFC pages list ₹199 or ₹299. Suggest `"Often a processing fee too: H-D-F-C lists ninety-nine to six hundred ninety-nine rupees."` (13 words).
- **SHOULD:** The SBI Card page itself says nothing about GST. The "you pay 18% GST on that interest" step rests on HDFC's rule applied to SBI's example. That is fine in practice, but the description should say "banks usually charge 18% GST on the interest (HDFC states this explicitly)".

## 046_bonds_friend: SHOULD FIX
- Math OK: price at 5% = $922.78 (−$77.22), the yield-to-maturity check passes, and the price curve is monotonic.
- **SHOULD (framing):** `"Hold to maturity, and if he pays, you get your thousand."` together with `"Sell early, and that drop is real."` implies the loss disappears if you hold. It does not: a holder earns 4% while new bonds pay 5%, which is the same ~$77 in present value. This is a common misconception and the Short reinforces it. Suggest replacing the last line with `"Hold, and you earn four percent while new bonds pay five."` (11 words), and adding one sentence to the description: "Holding to maturity avoids a realised loss, but you still earn less than new bonds pay."

## 048_mortgage_prepay: OK
Freddie Mac PMMS confirmed: "averaged 7.28% as of November 19, 2026, up from last week when it averaged 7.11%". The math checks out: $2,736.85 a month, interest $585,266 → $442,057, $143,209 saved, paid off in 285 months (75 months early), $62,948 extra paid. The caveats (prepayment penalty, emergency fund, nominal dollars) are present. On the day of rendering, re-check PMMS (a Thanksgiving-week release may be dated Wed 25 Nov).

## 049_amul: MUST FIX
- Verified:
  - **FY26 results** (DeshGujarat / Dairy Industries International): brand turnover crossed ₹1 lakh crore (+11% on ₹90,000 Cr); GCMMF turnover ₹73,450 Cr (from ₹65,911 Cr); 3.6M farmers; 18 member district cooperatives.
  - **Milk volume:** 31M litres a day (PTI coverage of the FY26 release).
  - **Dollar conversion:** ≈ $10.7B is correct.
- **MUST, wrong attribution of the headline claim.** The cited source (Rural Voice, 25 Jun 2022) quotes Jayen Mehta: *"In India, farmers get about 80-85 per cent of the rupee spent by the consumer."* That is about Indian dairy in general, not Amul. Yet the Short presents it as an Amul-specific figure (hook, bars labelled "Amul", sub "Amul's own estimate (GCMMF, 2022)", and the title).
  - **Fix:** Cite an Amul-specific statement instead. GCMMF chairman's speech, 50th Annual General Body Meeting (amul.com): *"of Rs. 100 a consumer spends on Amul products, Rs. 80-85 goes back to the dairy farmer"*. The same claim appears in the 49th AGM speech, and the 41st (2015) has "80%". I saw this wording in search snippets only, because amul.com returned 403/404 to automated fetches, so confirm it in a browser.
  - Change the sub from `"Amul's own estimate (GCMMF, 2022)"` to `"Amul's own claim (GCMMF AGM speech)"`.
  - Keep Rural Voice only as the source for the "one-third elsewhere" quote (scene 2 wording is fine).
- **MUST, factual framing.** `"Now the twist: that leaves Amul at most twenty rupees for everything else."` The ₹20 is out of the *consumer's* ₹100, so it also covers retailer and distributor margins, not just Amul. Change to `"Now the twist: that leaves at most twenty rupees for everything else, shops included."` (14 words).
- **SHOULD:** In the hook, say the claim is Amul's: `"Amul says of every hundred rupees you spend, about eighty reach farmers."` (12 words). Optionally soften the title to "Amul Business Model: Why Farmers Get ₹80 of ₹100". YourStory (Jul 2026) notes the figure is self-reported and has never been audited, which the description already says.

## 050_dividends_buybacks: SHOULD FIX
- Verified against the S&P DJI release of 18 Dec 2025: "The 12-month September 2025 expenditure was a record $1.020 trillion"; "dividends set a record $664.9 billion"; total $1.685T. The 1% excise tax on net buybacks is confirmed. The example math is correct.
- **SHOULD:** The data is 14 months old. No newer S&P DJI release turned up (Q4 2025 through Q2 2026 releases should exist), so look one up on spglobal.com/spdji before publishing. The on-screen "12 months to Sept 2025" label keeps the current version accurate. If you update, note that third parties put the figure at about $1.10T for the 12 months to June 2026 (Neuberger Berman/Bloomberg), so "over a trillion" still holds.

## 051_insurance_types: OK
Policygenius page (updated Oct 15, 2024; "Rate illustration valid as of 10/01/2024") confirmed exactly: 20-year term $36.90 F / $48.89 M (Preferred, composite of 11 carriers); whole life $801 F / $920 M (Preferred Plus, MassMutual, paid up at 100). The math is correct: 18.8x, $11,734 vs $220,800. The framing is neutral and the different health classes are disclosed. The rates are 2 years old but labelled "Oct 2024" on screen.

## 053_crash_and_sip: SHOULD FIX
- S&P 500 closes confirmed (AP/NPR, 28 Mar 2013): 1,565.15 (9 Oct 2007), 676.53 (9 Mar 2009), 1,569.19 (28 Mar 2013). That is a −56.8% fall and ~5.4 years to recover. The illustration math is correct: 84.56 units, $8,456, +40.9%, −29.5% at the midpoint.
- **SHOULD:** `"Most people quit here."` is an unsourced behavioural claim. Change to `"Many people quit here."`, which matches the description.
- **SHOULD (reads as advice):** The closing line `"Keep buying through the drop, and even a round trip pays."` is an imperative. Suggest `"Buying through the drop is why even a round trip paid here."` (12 words).

## 054_narayana_murthy: SHOULD FIX
- Verified:
  - **Seed money:** ₹10,000 of ₹10,250 (Business Today / Business Standard, 15 Mar 2024).
  - **1993 IPO:** undersubscribed; Morgan Stanley took 13% at the ₹95 offer price.
  - **Murthy quote:** "I was wrongly idealistic" (Business Today, 4 Jan 2024, CNBC-TV18).
  - **FY26 revenue:** $20,158M (Infosys, 23 Apr 2026) and ₹178,650 Cr, +9.6% (PTI/ThePrint).
  - **Founding:** 1981, Pune, seven founders.
  - The criticism adds balance.
- **SHOULD:** `"first Indian company on Nasdaq"`: Infosys's own 20-F says "first India-registered company" listed on a US exchange, and Cognizant (US-registered, Indian operations) listed on Nasdaq in 1998. Suggest `"By nineteen ninety-nine, it was the first India-registered company on Nasdaq."` (12 words), and use the same wording in the description.
