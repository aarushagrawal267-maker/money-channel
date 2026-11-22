# Fact check: Penny to Billion specs (week 1 + week 2)

Reviewer: financial-analyst agent. Date: 2026-11-22/23 (IST). Scope: all 28 specs in the brief, in publish order.
Method: every spec was re-run in a scratch copy (all `assert`s pass); key sourced figures re-checked against primary
sources where reachable (SEC EDGAR full-text + filings, company releases, Fed/FOMC, CFPB, ICI, IATA, Morningstar,
Vanguard, Damodaran, WGC, Zerodha charges page); maths recomputed independently; spoken wording checked for
overstatement.

Upload status when checked (pipeline/posted.json): **L001 is already uploaded and scheduled** (1rV4WFA_DW8).
016-019 are also uploaded (outside this brief). 023 and everything after it are **not uploaded yet**, so fixes
there cost only a re-render.

Verdict scale: **OK** = verified, no change needed. **Minor** = accurate but could mislead or is imprecise; fix
if cheap / before upload. **MUST FIX** = a spoken or on-screen claim is wrong or misattributed; fix before upload.

---

## MUST FIX (4)

| # | Video (publish IST) | Exact claim | What's wrong / correct figure + source | Suggested replacement |
|---|---|---|---|---|
| 1 | **030_zerodha** (1 Dec 06:30) | Scene 1 "charges nothing when you buy shares to keep"; scene 2 "Investors who buy and hold pay zero"; scene 6 "So investing really can be free"; CTA "Free to invest." | Only the **brokerage** is ₹0. Zerodha charges delivery investors a DP charge of **₹15.34 per scrip on every sell** (₹9.50 of it is Zerodha's own fee) and an **AMC of ₹300 + GST a year** on non-BSDA accounts (BSDA free only up to ₹4 lakh). Zerodha itself booked **₹180 crore of AMC income in FY26**. STT 0.1% each side and stamp duty also apply. Sources: https://zerodha.com/charges (checked 22 Nov 2026); Lapaas Voice/Inc42 FY26 breakdown, Aug 2026 https://lapaasvoice.com/zerodha-fy26-profit-rises-1-2-to-%e2%82%b94283-crore-brokerage-income-falls-10-7/ | Scene 1: "Zerodha, one of India's biggest stockbrokers, charges zero brokerage when you buy shares to keep. Yet in its latest financial year, it made about forty-three billion rupees in profit." Scene 2: "The trick? Investors who buy and hold pay no brokerage, just small fixed charges. Traders pay per order: up to twenty rupees for every intraday, futures or options trade." (visual left sub: "₹0 brokerage"). Scene 6: "So investing can cost very little. Most of the bill is paid by people who trade a lot." CTA: "Cheap to invest. / Paid to trade." Description: add "Delivery investors still pay a DP charge (₹15.34 per stock sold), an annual maintenance charge on most accounts, and taxes such as STT and stamp duty." |
| 2 | **033_raise_vs_switch** (2 Dec 22:30) | Hook: "Staying loyal to one employer could cost you about sixty-two thousand dollars over ten years." (+ visual "$62K gap") | The $62K comes entirely from an **assumed 10% bump per switch vs 3% for staying** (a 7-point premium). Real US data shows a far smaller premium: Atlanta Fed Wage Growth Tracker (3-month moving average of median wage growth, data to Sept 2026, released 8 Oct 2026): **job switchers 4.7%, job stayers 3.4%**. Re-running the spec's own model with those medians gives a 10-year gap of **about $11K**, not $62K. The hook states the example as a general fact before saying it's an example. Source: https://www.atlantafed.org/chcs/wage-growth-tracker | Hook: "In this example, switching jobs every three years earns about sixty-two thousand dollars more over ten years than staying. Here's the math, and the catch." Hook visual: "$62K gap (example)". Add one line to "The catch" scene: "And real bumps are often smaller. In US data, job switchers' pay recently grew about four point seven percent a year, versus three point four for people who stayed." Add Atlanta Fed source to description. (Alternative: keep the hook but call Leo's +10% "a strong switch" on screen.) |
| 3 | **039_dca_vs_lump** (5 Dec 22:30) | Hook frames "$12,000: all at once, or **a thousand a month**?", then scene 2 "Investing all at once beat spreading it out about two-thirds of the time" (68%) and scene 5 "it still beat leaving the money in cash sixty-nine percent of the time." | The Vanguard 68% / 69% figures are for a **three-month split** (lump sum split into 3 equal parts invested a month apart), 100% equity, compared after one year (Figure 2 notes). The script attaches them to a 12-month, $1,000-a-month plan the study did not measure for those numbers. The spec's own docstring has it right; the script and description ("spreading it out") don't. Source: Vanguard, Finlay & Zorn, Feb 2023, Fig. 2 notes: https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf | Scene 2: "Vanguard studied global stocks from nineteen seventy-six to twenty twenty-two. Investing all at once beat splitting it over three months about two-thirds of the time." Visual sub: "vs 3 monthly parts · Vanguard · 1976–2022". Scene 5: "But if the market drops right after you invest, spreading it out wins. And splitting it over three months still beat leaving the money in cash sixty-nine percent of the time." Description: "...investing it all at once beat splitting it into three monthly parts about two-thirds of the time..." (The $1,000-a-month 7% example can stay; it's computed and labelled.) |
| 4 | **035_nokia_fall** (3 Dec 22:30) | Scene 5 visual compares "Paid, 2013: $7.17B" with "Written off, 2015: $7.6B"; spec asserts `WRITEOFF_USD > DEAL_TOTAL_USD` ("write-off bigger than the price"). | The side-by-side tells viewers Microsoft wrote off **more than it paid**. Not so on Microsoft's own accounts: FY2014 10-K Note 9: "total purchase price of **$9.5 billion**, including cash acquired of $1.5 billion... cash of $7.1 billion and Nokia's repurchase of convertible notes of $2.1 billion". The $7.2B (EUR 5.44B) headline is the announced price at signing. Source: Microsoft 10-K FY2014 (filed Jul 31, 2014) https://www.sec.gov/Archives/edgar/data/789019/000119312514289961/d722626d10k.htm | Say: "In twenty thirteen, Microsoft agreed to buy Nokia's phone business, plus a patent licence, for about seven point two billion dollars. Two years later, Microsoft wrote off seven point six billion dollars tied to the deal, and cut up to seven thousand eight hundred jobs." Visual: replace the compare with a stat "$7.6B written off · 2015 · Microsoft". Delete the `WRITEOFF_USD > DEAL_TOTAL_USD` assert/comment. |

---

## Per-video results (publish order)

### 023_inflation_100 (23 Nov 22:30, not yet uploaded): **Minor**
Maths re-checked: 100/1.03^n = 74.4 / 55.4 / 41.2; 100·1.03^n = 134.4 / 180.6 / 242.7; 100/1.02^30 = 55.2. Fed 2% PCE goal correct.

| Claim | Verdict | Note / fix |
|---|---|---|
| "money you won't need for years has to grow faster than prices, just to stand still" | Minor (logic) | To stand still it must grow **as fast as** prices; faster is real growth. Replace: "So money you won't need for years has to grow at least as fast as prices, just to stand still." Cheap to fix today since 023 isn't uploaded. |
| Hook "In thirty years, it'll only buy what forty-one dollars buys today." | Minor | Stated as certain before the 3% assumption arrives. Optional: "At three percent inflation, in thirty years it would only buy what forty-one dollars buys today." |
| CTA "Prices never stand still." | Minor | Absolute claim (deflation happens). Optional: "Prices rarely stand still." |
| All numbers, Fed 2% target | OK | |

### L001_costco (23 Nov 23:30, ALREADY SCHEDULED): **OK (2 optional nits)**
Verified against Costco FY2026 release and 10-K: net sales $297,247M, fees $5,907M (FY25 $5,323M), revenue $303,154M, merchandise costs $264,279M, SG&A $27,190M, op income $11,685M (FY25 $10,383M), net income $9,226M; 84.1M paid members, 42.3M Executive, 75.2% of sales, renewal 92.3% / 89.8%, "less than 4,000 active SKUs", "significantly lower gross margins ... than most other retailers", Kirkland "a growing portion", 939 warehouses (647 US/PR, 115 Canada, 177 other). Sources: release via https://finviz.com/news/395411/costco-wholesale-corporation-reports-fourth-quarter-and-fiscal-year-2026-operating-results ; 10-K https://www.sec.gov/Archives/edgar/data/0000909832/000090983226000093/cost-20260830.htm

| Claim | Verdict | Note |
|---|---|---|
| Bullet "Renewed automatically by most" | Minor | No source found for an auto-renewal share. Next time: "Renewed year after year by most". Not worth a re-upload alone. |
| "on all those products, it made almost nothing" | Minor | Products left ~$5.8B operating profit (~2¢/$). The next scenes give the real number, so acceptable hyperbole; "very little" would be safer. |
| FY26 net income $9.2B | OK | Includes a small one-off IEEPA tariff-refund benefit ($0.15/share in Q4); immaterial. |

### L002_compounding (25 Nov 23:30): **OK**
All 40+ asserts reproduce. Damodaran S&P 500 2008 total return -36.55% confirmed (https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html). Maya $494K vs Sam $203K (2.43x); last decade > first three combined (73.6K vs 66.1K); 1% fee costs 16.8% / $59K; real return (1.06/1.03)-1 = 2.9%; +40/-20 geometric 5.83%. Uses effective-annual 7% (correctly documented).

### 020_index_funds_vs_managers (26 Nov 06:30): **OK (minor wording)**
SPIVA U.S. Mid-Year 2026, Report 1a, All Large-Cap vs S&P 500: 10y 83.33%, 15y 90.49%, 20y 92.61% (matches; S&P PDF blocks fetches, confirmed via transcriptions e.g. https://retirementliteracyfoundation.org/guides/active-vs-index-funds-spiva/). Morningstar 2026 US Fund Fee Study: active 0.57%, broad index 0.09% (2025, asset-weighted) confirmed verbatim in the PDF.

| Claim | Verdict | Note |
|---|---|---|
| "Ninety-three percent of US large-cap fund managers trailed" / title "93% of Fund Managers Lose" | Minor | SPIVA counts **funds**, not managers. Prefer "large-cap funds". |
| Fee numbers differ from L003 (0.64% / 0.05%) the next day | Minor (consistency) | Both correct: Morningstar = all US funds and ETFs; ICI = equity mutual funds only. Consider a sub-label "all US funds (Morningstar)". |

### 021_bnpl (26 Nov 22:30): **OK (minor)**
CFPB Sept 2022 report §4.2.1: effective discount rate to partnered merchants 3.84% (2019), 3.46% (2020), **3.08% (2021)**, verified in the PDF (https://files.consumerfinance.gov/f/documents/cfpb_buy-now-pay-later-market-trends-consumer-impacts_report_2022-09.pdf). Merchant fees were 61.9% of lender revenue in 2021, which supports "mostly from the store". LendingTree 68% overspend, 47%/41%/34% late confirmed (https://www.lendingtree.com/personal/buy-now-pay-later-loan-statistics/). CFPB Jan 2025: ~63% had simultaneous loans in 2022.

| Claim | Verdict | Note |
|---|---|---|
| "A CFPB study found lenders charged partner stores about three percent per sale." | Minor | Data is 2021, five lenders. Better: "A CFPB study of twenty twenty-one data found big lenders charged partner stores about three percent per sale." |

### 022_airline_loyalty (27 Nov 06:30): **OK (minor)**
AAL 2025 10-K verbatim: "cash payments from co-branded credit card and other partners were $6.2 billion and $6.1 billion" (https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/aal-20251231.htm); AAL FY25 GAAP net income $111M. Delta FY25 release: Amex $8.2B, GAAP revenue $63,364M, GAAP pre-tax $6,185M (https://news.delta.com/sites/default/files/2026-01/delta-air-lines-announces-december-quarter-and-full-year-2025-results-vf.pdf).

| Claim | Verdict | Note |
|---|---|---|
| "That's because airlines don't just sell seats." | Minor | The cause-and-effect between small profit and partner cash is loose. Optional: "How? Airlines don't just sell seats. They sell miles." |
| "more than Delta's entire pre-tax profit of six point two billion" | OK | GAAP figure includes $1.2B mark-to-market investment gains; adjusted pre-tax was $5.0B, so the claim is even stronger on that basis. |

### 001_start_early (27 Nov 22:30, INR): **OK (minor)**
FV recomputed: Rahul ₹3.25 Cr, Aman ₹94.9 L, gap ₹2.30 Cr, last 5 years +₹1.48 Cr.

| Claim | Verdict | Note |
|---|---|---|
| "about twelve percent a year" | Minor | Model uses 1%/month = **12.68% effective**. This is the usual Indian SIP-calculator convention, so OK, but the description should say "12% a year, compounded monthly (about 12.7% effective)". Also add "before inflation" (at ~6% inflation, ₹3.25 Cr in 35 years buys roughly ₹42 L of today's goods). |

### L003_index_funds (27 Nov 23:30): **OK (minor)**
Verified: SPIVA 20y 92.61%, 5y 89.32%, 20-yr survivorship 36.52%; 2025 calendar year 79%; Persistence YE2025: 164 top-quartile large-cap funds in 2021, 0% stayed; top half 4.5% (https://genuineimpact.substack.com/p/what-persists-is-failure); ICI Fact Book 2026 Fig. 6.4: active equity MF 0.64%, index equity MF 0.05% (2025) (https://www.icifactbook.org/pdf/2026-factbook-ch6.pdf); ICI ch.2: index funds 52% of long-term fund assets (19% in 2010), $19.1T (https://icifactbook.org/pdf/2026-factbook-ch2.pdf); RBC top-10 weight 40.7%, 18-23% 1990-2015; Buffett 2017 letter scorecard (125.8% / 8.5%; funds A-E), $2,222,279 to Girls Inc.; fee-drag maths ($750.6K vs $635.9K, gap $114.7K).

| Claim | Verdict | Note |
|---|---|---|
| "In December 2007, he made a one million dollar bet" | Minor | Exact month not confirmed by a primary source; the bet ran 1 Jan 2008 to 31 Dec 2017 (Long Now: https://longnow.org/ideas/warren-buffett-wins-million-dollar-long-bet/). Safer: "In 2007, he made a one million dollar bet". |
| "For every manager who beats the market by a point, another trails it by a point." | Minor | Sharpe's arithmetic is dollar-weighted. Better: "For every dollar that beats the market by a point, another dollar trails it by a point." |

### 024_expense_ratio (28 Nov 06:30): **Minor**
| Claim | Verdict | Note |
|---|---|---|
| "Assume it earns seven percent a year before fees." Title "A 1% Investment Fee Can Cost You $120,000" | Minor | Code compounds 7%/12 monthly = **7.23% effective**. At exactly 7% a year (L002's convention) the results are $657K vs $540K, gap **$117K**, fees $60,951 vs $3,488, so "over a hundred and twenty thousand" would no longer hold. The description does say "compounded monthly", so it isn't wrong. Either say "seven percent a year, compounded monthly" on screen, or switch to the effective rate and retitle "$117,000". |

### 025_emergency_fund (28 Nov 22:30): **OK**
S&P 500 closes 3,386.15 (19 Feb 2020) and 2,237.40 (23 Mar 2020): -33.9%. FDIC $250,000 per depositor, per insured bank, per ownership category. Optional: "a US bank insured by the FDIC" for non-US viewers.

### 028_market_cap (29 Nov 06:30): **OK**
Walmart FY26 revenue $713.16B, net income attributable $21.89B; MSFT FY26 revenue $331.8B, net income $133.7B (https://news.microsoft.com/source/2026/07/29/microsoft-cloud-and-ai-strength-fuels-fourth-quarter-results-4); closes 18 Nov 2026: MSFT $508.29, WMT $127.36. Note: MSFT's GAAP net income includes ~$5B of OpenAI-related gains (non-GAAP $128.8B = 38.8% margin), so "about forty cents" still holds.

### 027_lifestyle_inflation (30 Nov 06:30): **OK**
Maths reproduces ($291.67/mo kept, $145.83 saved, $76.4K vs $35K in). Same note as 024: "7% a year" is 7%/12 monthly (7.23% effective), disclosed in the description. 30% example tax (22% + 7.65%) is reasonable and labelled.

### 029_netflix_blockbuster (30 Nov 22:30): **OK**
S-1 2000 revenue $35.9M / loss $57.4M; Blockbuster bankruptcy Sept 2010; 2025 Netflix revenue $45.18B; dispute over the $50M offer is attributed both ways. Good handling.

### L010_netflix_blockbuster (30 Nov 23:30): **OK (minor)**
Spot-checked: Hastings' "a thousand times our size" whisper in Dallas is in the No Rules Rules excerpt (https://www.cbsnews.com/news/book-excerpt-netflix-no-rules-rules-reed-hastings-erin-meyer); Q3 2026 revenue $12.87B, op margin 34.6% vs 28.2%; 2026 forecast $51.1B; all asserts reproduce.

| Claim | Verdict | Note |
|---|---|---|
| "an operating margin of about thirty-five percent, up from twenty-eight percent a year earlier" | Minor | Q3 2025's 28.2% was depressed by a one-off ~$619M Brazilian tax charge (Netflix Q3 2025 letter; ~31.5% guided before it). Add: "...up from twenty-eight percent a year earlier, when a one-off tax charge in Brazil hit." |

### 030_zerodha (1 Dec 06:30): **MUST FIX** (see top)
Figures themselves check out: FY26 net profit ₹4,283 Cr (FY25 ₹4,231 Cr), brokerage ₹2,738 Cr, interest ₹2,269 Cr (https://inc42.com/buzz/zerodhas-bland-fy26-net-profit-up-a-mere-1-at-); SEBI FY26 loss-makers 87.7% (https://www.businesstoday.in/personal-finance/story/87-7-of-fo-traders-lost-money-in-fy26-despite-sebi-curbs-why-retail-investors-keep-losing-567419-2026-11-14). "MTF ~10% of revenue" is Kamath's "currently" figure; reported FY26 MTF + delayed-payment income was ₹448 Cr (about 5% of ~₹8,500 Cr), so keep the word "now".

### 031_car_loan_cost (1 Dec 22:30): **OK**
Amortisation reproduces ($596.72 / $838.12; interest $7,963 / $5,230; 20/4/10 payment $670.49, income $80.5K). The "same rate" caveat is disclosed.

### 032_buffett_after_50 (2 Dec 06:30): **OK**
Forbes real-time figure $154B as of 1 Nov 2026 confirmed (https://www.forbes.com.au/news/billionaires/the-top-10-richest-people-in-the-world-december-2025/). 616x over 44 years = 15.7%/yr, doubling every 4.75 years. Smoothed curve labelled.

### 033_raise_vs_switch (2 Dec 22:30): **MUST FIX** (see top). Maths itself is right ($78,286 vs $95,357; 10-year gap $62K).

### L004_credit_cards_business (2 Dec 23:30): **OK**
Verified: NY Fed Q3 2026 card balances $1.285T, +$22B q/q, record (https://www.newyorkfed.org/newsevents/news/research/2026/20261110); FOMC/G.19 rate series as cited; CFPB Dec 2025 report: interest $160B (2024) vs $105B (2022), ~half revolve, 15% minimum-only (https://www.orrick.com/en/Insights/2026/01/Trends-and-Takeaways-from-the-2025-Credit-CARD-Act-Report), late fees $17.0B, annual fees $8.7B, rewards $47.5B, total fees $31.3B (secondary, CFPB PDF fetch blocked); Visa FY26 net revenue $45.9B, GAAP net income $23.5B (https://investor.visa.com/news/news-details/2026/Visa-Fiscal-Fourth-Quarter-and-Full-Year-2026-Financial-Results/default.aspx); Capital One 10-K Table 8 (2024: NII $22,088M, revenue $28,164M, provision $10,272M, net $3,292M, NCO 5.88%) and rewards $9.0B, verified in the filing (https://www.sec.gov/Archives/edgar/data/927628/000092762826000024/cof-20251231.htm). Not re-fetched: the CFPB tier-level figures (rewards by tier, late-fee split by tier) because the PDF blocks automated fetches; treat as unverified by this review.

### 034_rates_and_you (3 Dec 06:30): **OK (minor)**
FOMC 16 Sept 2026 raised to 3.75-4.00%; 28 Oct 2026 held (10-2) (https://federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm). Payment maths $1,798.65 → $1,847.15.

| Claim | Verdict | Note |
|---|---|---|
| "Say you owe three hundred thousand dollars over thirty years at a variable rate. Going from six percent to six and a quarter adds about forty-eight dollars fifty a month." | Minor | Adjustable mortgages reset on their own schedule and index, not the day the Fed moves. Optional: "...at a variable rate. If your rate rises from six percent to six and a quarter at its next reset, the payment goes up about forty-eight dollars fifty a month." Re-check the range if the Dec FOMC meeting moves before publish (it's after 3 Dec). |

### 035_nokia_fall (3 Dec 22:30): **MUST FIX** (see top)
Other figures OK: Nokia Q4 2007 40% (own estimate), Gartner Q2 2013 14.0%, Elop memo quote, EUR 5.44B / ~$7.2B announced, $7.6B impairment July 2015.

### 036_free_apps (4 Dec 06:30): **OK**
Meta Q3 2026: revenue $64.60B, DAP 3.64B (Sept), impressions +10%, price per ad +14% confirmed (https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Third-Quarter-2026-Results/). The $63.061B ad-revenue line wasn't separately re-fetched, but it's consistent with total revenue.

### 037_credit_score (4 Dec 22:30): **OK**
myFICO 35/30/15/10/10 weights; "checking your own score doesn't hurt it" is correct.

### L005_airlines (4 Dec 23:30): **OK**
IATA 7 June 2026 release verified: revenue $1.165T, net $23.0B (2.0%), $4.50/pax, fuel $350B vs $252B (31.4% of costs), labour $271B, load factor 84.0% record, ancillary $165B > cargo $162B "for the first time since 2019", tickets $839B (https://www.iata.org/en/pressroom/2026-releases/06-07-middle-east-disruptions-high-fuel-prices-halve-airline-industry-profitability/). BTS 2025: net $6.0B, bags $7.4B, change fees $1.1B (https://www.bts.gov/newsroom/us-airlines-gained-60-billion-2025-decrease-over-2024). Delta premium $22,097M (+7%), main cabin $23,391M (-5%), checked in the release PDF. AAL/Delta as in 022. Buffett 2007 letter quotes are verbatim. The per-flight break-even is labelled as an illustration (it assumes no per-passenger cost); fine.

### 038_dhirubhai (5 Dec 06:30): **OK (minor)**
RIL FY26 gross revenue ₹1,175,919 Cr ($124.0B) confirmed (https://www.ril.com/sites/default/files/2026-04/24042026_Media_Release_RIL_Q4_FY2025-26_Financial_and_Operational_Performance.pdf).

| Claim | Verdict | Note |
|---|---|---|
| Hook "Its founder once worked at a petrol station in Yemen." | Minor | Stated as fact, then hedged in the next scene ("obituaries say"). Hook: "Its founder is said to have started out at a petrol station in Yemen." |

### 039_dca_vs_lump (5 Dec 22:30): **MUST FIX** (see top). Example maths OK ($12,840 vs $12,450). Spec's "cash earns nothing (same as Vanguard)" is correct for the LS-vs-CA comparison.

### 040_gold_fear (6 Dec 06:30): **OK**
WGC Q3 2026: central banks 321t (+42% y/y), LBMA average $4,262 (+23% y/y), ETFs +211t (https://www.gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3/). -12.5% vs Q1 average rounds to "about thirteen percent".

---

## Cross-cutting notes
1. **Compounding convention is inconsistent.** L002 uses an effective 7% a year (and says so). 024, 027 and 001 use rate/12 monthly (7% → 7.23%, 12% → 12.68%). Pick one house rule; effective-annual is safest because it matches what "7% a year" means to a viewer. Only 024's headline figure changes materially ($123K → $117K).
2. **Same-week numbers that look inconsistent but are both right:** fees in 020 (Morningstar, all funds) vs L003 (ICI, equity mutual funds). Label the universe on screen.
3. **Disputed or secondary-only figures handled well:** Netflix $50M offer (both sides shown), SPIVA via transcriptions, Dhirubhai's early jobs. Keep doing this.
