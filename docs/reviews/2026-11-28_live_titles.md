# Live titles: search-first rewrite (28 Nov 2026)

Why: Analytics for 20–25 Nov show YouTube search as our #2 traffic source (15 views, versus 33 from the Shorts feed). The top performer is the Rule of 72 Short, with a clear question title and 99% watched. So each public video's title should start with the phrase people type, and the first sentence of its description should repeat it. Search snippets and the collapsed description show only about the first 150 characters.

Rules used: title ≤60 characters, search phrase first and then the hook, no "#shorts", and every number matches the spec's voice lines or description. Lead ≤300 characters, opening with the same search phrase. Character counts are in brackets. Nothing here was applied. Apply with `tools/seo_live.py titles ID` once `seo_live.py check` says the force-ssl scope is present: set the spec `title`, swap the first paragraph of `description` for the lead, then re-run the spec `.py` so its asserts still pass.

| Video | Current title | Proposed title | Proposed description lead | Verdict | Why |
|---|---|---|---|---|---|
| `014_minimum_payment_trap_us` | Credit Card Minimum Payment Trap: $5,000 Takes 16 Years | (keep) | (keep) | Keep both | Title already leads with the exact query ("credit card minimum payment") and pays off with spec numbers ($5,000, 16 years). The lead already says "credit card balance" and "minimum" in sentence 1. |
| `015_rule_of_72` | Rule of 72: How Fast Does Your Money Double? | (keep) | The Rule of 72 tells you how fast your money doubles: divide 72 by your yearly return. At 4% that's 18 years, at 7% about 10, at 10% about 7.2, and the exact answers (17.7, 10.2 and 7.3 years) are very close. (208) | Keep title, new lead | Title is our best performer (99% watched); don't touch. The current lead never says "Rule of 72". The new lead puts the query first and keeps the same numbers. |
| `016_buying_a_share` | What Happens When You Buy a Stock? (Not What You Think) | (keep) | What happens when you buy a stock? Your money almost never goes to the company. Your broker routes the order to an exchange or a market maker, it's matched with a seller, and one business day later (T+1) the cash and shares swap hands. (235) | Keep title, new lead | Title already starts with the common query "what happens when you buy a stock". Adding that phrase to the lead backs it up in the snippet. The rest of the lead is the current text, shortened. |
| `017_upi_free` | Who Pays for India's Free UPI? 25 Billion Payments a Month | **Is UPI Free? Who Pays for 25 Billion Payments a Month** (53) | Is UPI free? For customers, yes: in October 2026 Indians made about 25.5 billion UPI payments and paid nothing. So who pays? Merchants pay zero by law, the government pays banks an incentive, and apps like PhonePe and Paytm earn from loans and insurance instead. (262) | Change | "Is UPI free" is the question Indians are typing now, after the 0.4% merchant-fee news. The hook stays the same. 25 billion matches the voice ("over twenty-five billion"), and 25.5 billion matches the description. |
| `018_start_early_us` | Start Investing at 25 vs 35: $792K vs $368K | (keep) | Start investing at 25 vs 35: two friends invest the same $300 a month at an assumed 7% a year. At 65, one has about $792K and the other about $368K, even though the gap in money put in is only $36,000. (201) | Keep title, new lead | Strong title: query first plus concrete numbers, the same pattern as our winner. The current lead opens with "Two friends", so it's missing the searched phrase. |
| `019_real_hourly_wage` | Your Real Hourly Wage Is Lower Than You Think | **Real Hourly Wage: How a $60K Salary Becomes $18/Hour** (52) | How to calculate your real hourly wage: a $60,000 salary is $28.85 an hour on paper, but after taxes, commuting, unpaid extra time and work costs it's about $18.15 an hour in this example, over a third less. (207) | Change | People search "real hourly wage (calculator)" and "true hourly wage", not "your real hourly wage". The new title leads with that phrase. "How...Becomes" describes the worked example honestly ($60K and about $18 are both in the voice script). |
| `023_inflation_100` | What $100 Will Buy in 30 Years (Inflation Explained) | **What Will $100 Be Worth in 30 Years? (3% Inflation)** (51) | What will $100 be worth in 30 years? At 3% inflation a year, $100 in cash buys about $74 of today's goods after 10 years, $55 after 20 and $41 after 30. Just to keep up, it has to grow to $134, $181 and $243. (208) | Change | "What will $100 be worth in X years" is the natural question form. Putting "3% inflation" in the title states the assumption up front. Removing "Inflation Explained" leaves that phrase to L006 ("Inflation Explained: Why Your Money Quietly Shrinks", 9 Dec). The 33% retention is a pacing problem, not a packaging one: the title is paid off in line 1 ($41). |
| `020_index_funds_vs_managers` | 93% of Fund Managers Lose to the S&P 500. Here's Why | **Do Fund Managers Beat the S&P 500? 93% Lost Over 20 Years** (57) | Do fund managers beat the S&P 500? Mostly not. S&P's SPIVA scorecard shows 93% of US large-cap funds trailed it over the 20 years to June 30, 2026 (83% over 10 years, 90% over 15). A big reason is fees. (202) | Change (fixes clash with L003) | The Short takes the question query "do fund managers beat the S&P 500" and keeps 93% (its voice line 1). The long video moves to "index funds explained" (below), so the two no longer share a title or a lead phrase. |
| `021_bnpl` | How Buy Now, Pay Later Makes Money (It's Not Interest) | (keep) | How does buy now, pay later make money? Mostly from the store: a CFPB study found big BNPL lenders charged partner merchants about 3% per sale (2021). Some also charge late fees, and the quiet risk is stacking several plans at once. (232) | Keep title, new lead | Title already starts with the exact query, and "(It's Not Interest)" is paid off in scene 2. The current lead opens with "Pay-in-4 plans", so "buy now, pay later" never appears in the snippet. |
| `022_airline_loyalty` | How Airlines Really Make Money: Credit Cards | **How Airlines Make Money From Credit Cards: $6.2B vs $111M** (57) | How do airlines make money from credit cards? They sell miles to banks. In 2025, American Airlines' card and other partners paid it $6.2 billion in cash while it made $111 million in net profit, and American Express paid Delta $8.2 billion. (240) | Change | Narrows the Short to "how airlines make money from credit cards", the angle used by the top articles on this topic. This stops it competing with L005 "How Airlines Really Make Money: $4.50 a Passenger" (4 Dec). $6.2B vs $111M is the opening line and matches the thumbnail ("$6.2B / More than its profit"). |
| `039_dca_vs_lump` | Lump Sum vs Dollar-Cost Averaging: Which Wins More? | (keep) | (keep) | Keep both | Title is exactly the search phrase plus a question. The lead already opens with "Lump sum vs dollar-cost averaging:" and gives the answer (68%, Vanguard). |
| `L001_costco` | How Costco Makes Money (It's Not the Groceries) | (keep) | How does Costco make money? Not mainly from products, which earned it only about 2 cents of operating profit per dollar in fiscal 2026. Membership fees of $5.9 billion, under 2% of revenue, brought in about half of its operating profit. (236) | Keep title, new lead | Title is the top query plus a hook the video pays off ("Costco isn't really in the business of selling you groceries"), and it pairs with the thumbnail "IT'S NOT GROCERIES". The current lead starts with "$297 billion" instead of the query. |
| `L002_compounding` | Compound Interest Explained: Same $96K, 2.4x the Money | (keep) | Compound interest explained with real numbers: two people each invest $96,000, and one ends with about $494,000 while the other has about $203,000. We break down the four levers (amount, rate, time, leaks), the Rule of 72 and the real cost of a 1% fee. (252) | Keep title, new lead | "Compound interest explained" is first, and "Same $96K, 2.4x" matches the thumbnail ("2.4X / SAME $96K INVESTED"). It's a little abstract, but changing it would break that pairing. The lead needs the query phrase in sentence 1. |
| `L003_index_funds` | Why 93% of Fund Managers Lose to a Simple Index Fund | **Index Funds Explained: Why 9 in 10 Fund Managers Lose** (53) | Index funds explained: what an index fund is, and why more than 9 in 10 actively managed large-cap US stock funds trailed the S&P 500 over the 20 years to June 2026. Plus the fee math, Buffett's 10-year bet and the real weaknesses of index funds. (246) | Change (fixes clash with 020) | The long video covers what an index fund is (chapter 1), active vs passive, Buffett's bet and the downsides, so it should own the broad query "index funds explained". "9 in 10" is what the voice says ("more than nine out of ten"). The thumbnail's 92.6% stays as the visual number, so the title and thumbnail don't repeat each other. |

## Notes
- **020 vs L003 clash fixed.** The Short takes the question query ("Do fund managers beat the S&P 500?", 93% over 20 years). The long video takes "Index funds explained", the broad query that matches its full explainer and its chapters. Neither title nor lead shares an opening phrase with the other any more.
- **Pairs to keep apart later:** 022 ↔ L005 (airlines; fixed above by moving the Short to "...from credit cards") and 023 ↔ L006 (inflation; fixed by dropping "Inflation Explained" from the Short).
- **Leads:** 018, 021, L001 and L002 lost search value only because the description opens with a story or a number instead of the query. Changing just the lead is low-risk.
- **The JSON below** lists only videos with a change. When only the lead changes, `title` repeats the current title unchanged. "lead" replaces the first paragraph of the description; keep the assumptions, sources and hashtags that follow it.
- **Search phrasing** comes from a WebSearch check of how people word these queries (airline credit cards, "what happens when you buy a stock", "real hourly wage calculator"). No YouTube API was called.

```json
{
  "015_rule_of_72": {
    "title": "Rule of 72: How Fast Does Your Money Double?",
    "lead": "The Rule of 72 tells you how fast your money doubles: divide 72 by your yearly return. At 4% that's 18 years, at 7% about 10, at 10% about 7.2, and the exact answers (17.7, 10.2 and 7.3 years) are very close."
  },
  "016_buying_a_share": {
    "title": "What Happens When You Buy a Stock? (Not What You Think)",
    "lead": "What happens when you buy a stock? Your money almost never goes to the company. Your broker routes the order to an exchange or a market maker, it's matched with a seller, and one business day later (T+1) the cash and shares swap hands."
  },
  "017_upi_free": {
    "title": "Is UPI Free? Who Pays for 25 Billion Payments a Month",
    "lead": "Is UPI free? For customers, yes: in October 2026 Indians made about 25.5 billion UPI payments and paid nothing. So who pays? Merchants pay zero by law, the government pays banks an incentive, and apps like PhonePe and Paytm earn from loans and insurance instead."
  },
  "018_start_early_us": {
    "title": "Start Investing at 25 vs 35: $792K vs $368K",
    "lead": "Start investing at 25 vs 35: two friends invest the same $300 a month at an assumed 7% a year. At 65, one has about $792K and the other about $368K, even though the gap in money put in is only $36,000."
  },
  "019_real_hourly_wage": {
    "title": "Real Hourly Wage: How a $60K Salary Becomes $18/Hour",
    "lead": "How to calculate your real hourly wage: a $60,000 salary is $28.85 an hour on paper, but after taxes, commuting, unpaid extra time and work costs it's about $18.15 an hour in this example, over a third less."
  },
  "023_inflation_100": {
    "title": "What Will $100 Be Worth in 30 Years? (3% Inflation)",
    "lead": "What will $100 be worth in 30 years? At 3% inflation a year, $100 in cash buys about $74 of today's goods after 10 years, $55 after 20 and $41 after 30. Just to keep up, it has to grow to $134, $181 and $243."
  },
  "020_index_funds_vs_managers": {
    "title": "Do Fund Managers Beat the S&P 500? 93% Lost Over 20 Years",
    "lead": "Do fund managers beat the S&P 500? Mostly not. S&P's SPIVA scorecard shows 93% of US large-cap funds trailed it over the 20 years to June 30, 2026 (83% over 10 years, 90% over 15). A big reason is fees."
  },
  "021_bnpl": {
    "title": "How Buy Now, Pay Later Makes Money (It's Not Interest)",
    "lead": "How does buy now, pay later make money? Mostly from the store: a CFPB study found big BNPL lenders charged partner merchants about 3% per sale (2021). Some also charge late fees, and the quiet risk is stacking several plans at once."
  },
  "022_airline_loyalty": {
    "title": "How Airlines Make Money From Credit Cards: $6.2B vs $111M",
    "lead": "How do airlines make money from credit cards? They sell miles to banks. In 2025, American Airlines' card and other partners paid it $6.2 billion in cash while it made $111 million in net profit, and American Express paid Delta $8.2 billion."
  },
  "L001_costco": {
    "title": "How Costco Makes Money (It's Not the Groceries)",
    "lead": "How does Costco make money? Not mainly from products, which earned it only about 2 cents of operating profit per dollar in fiscal 2026. Membership fees of $5.9 billion, under 2% of revenue, brought in about half of its operating profit."
  },
  "L002_compounding": {
    "title": "Compound Interest Explained: Same $96K, 2.4x the Money",
    "lead": "Compound interest explained with real numbers: two people each invest $96,000, and one ends with about $494,000 while the other has about $203,000. We break down the four levers (amount, rate, time, leaks), the Rule of 72 and the real cost of a 1% fee."
  },
  "L003_index_funds": {
    "title": "Index Funds Explained: Why 9 in 10 Fund Managers Lose",
    "lead": "Index funds explained: what an index fund is, and why more than 9 in 10 actively managed large-cap US stock funds trailed the S&P 500 over the 20 years to June 2026. Plus the fee math, Buffett's 10-year bet and the real weaknesses of index funds."
  }
}
```
