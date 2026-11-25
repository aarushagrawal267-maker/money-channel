"""Long-form L009 (financing traps, USD): Rent vs buy, the full math.

Sources (checked 2026-11-25):
  [NAR] National Association of Realtors, "Existing-Home Sales Decreased 5.5% in October" (Nov 12, 2026):
        median existing single-family home price $421,900 in October 2026 (all types $416,700, up 0.4% from
        $414,900 a year earlier).
  [Z]   Zillow press release "A house doesn't have to mean a mortgage: Renting requires $14K less income than
        buying" (Nov 12, 2026, PR Newswire): typical US single-family rent $2,243/month in October 2026 (Zillow
        Observed Rent Index), up 3.2% from a year ago.
  [ZB]  Zillow press release "Rent or buy: How long it takes for buying a home to pay off in each metro"
        (Jun 4, 2026): typical buyer breaks even vs renting in "about six years nationally"; Columbus, OH 4.1 years;
        San Diego 23.3 years; San Francisco, San Jose and New Orleans: buying never surpasses renting within 30 years.
        Zillow's numeric assumptions are not given in the release.
  [FM]  Freddie Mac Primary Mortgage Market Survey (Nov 19, 2026): 30-year fixed averaged 7.28%; 6.26% a year
        earlier. Jun 4, 2026 release: 6.48%.
  [AT]  ATTOM 2025 property tax analysis (Apr 9, 2026): effective tax rate on US single-family homes 0.9%.
  [NW]  NerdWallet home insurance pricing report (Oct 2, 2026): typical US premium $2,564 a year in early 2026
        (dwelling coverage $300K-$500K, around a ~$410K typical rebuild cost).
  [RF]  Redfin, "What Are Closing Costs" (Apr 24, 2026): buyers usually pay 2%-5% of the purchase price.
  [CL]  Clever Real Estate, "True Cost of Selling a Home: 2026 Edition" (updated Oct 26, 2026): average agent
        commission 5.46% of the sale price.
  [IRS] IRS Topic 409 (most net capital gain taxed at no more than 15% for most individuals) and Topic 701
        (home-sale gain exclusion up to $250,000 single / $500,000 married filing jointly, 2-of-5-year tests).
Assumptions (ours, said on screen): 20% down, 3% buying costs (inside Redfin's range), 6% selling costs (agent fees
~5.5% plus other costs), maintenance 1% of value a year (rule of thumb), home prices, rent, tax, insurance and
repairs grow 3% a year, investments earn 6% a year, 15% tax on investment gains when cashed out, home gain
tax-free (within the IRS exclusion), no mortgage-interest deduction, no renters insurance, no PMI (20% down).
"""
import json, os
from collections import Counter

# ---- sourced
PRICE = 421_900          # [NAR] Oct 2026 median existing single-family
PRICE_YOY = 0.004        # [NAR] all-types median, Oct 2026 vs Oct 2025
RENT = 2_243             # [Z] Oct 2026 typical single-family rent, $/month
RENT_YOY = 0.032         # [Z]
RATE = 0.0728            # [FM] Nov 19, 2026
RATE_YR_AGO = 0.0626     # [FM]
TAX_RATE = 0.009         # [AT]
INSURANCE = 2_564        # [NW] $/year
BUY_RANGE = (0.02, 0.05) # [RF]
COMMISSION = 0.0546      # [CL]
CGT = 0.15               # [IRS] Topic 409
EXCL_SINGLE, EXCL_JOINT = 250_000, 500_000   # [IRS] Topic 701
ZILLOW_BE, ZILLOW_COLUMBUS, ZILLOW_SD = 6, 4.1, 23.3   # [ZB]
# ---- assumptions (labelled as such on screen)
DOWN, BUY_COST, SELL_COST, MAINT = 0.20, 0.03, 0.06, 0.01
GROWTH, RETURN = 0.03, 0.06     # home prices / rent / costs; investments
YEARS = 30
assert BUY_RANGE[0] <= BUY_COST <= BUY_RANGE[1] and SELL_COST > COMMISSION


def model(price=PRICE, rent=RENT, rate=RATE, g=GROWTH, r=RETURN, years=YEARS, rg=GROWTH):
    """Monthly simulation. Whoever spends less each month invests the difference at r.
    Returns (payment, rows) with rows[y] = (owner $/mo in year y, rent $/mo, buyer net worth, renter net worth),
    net worth = what each would have if they cashed out at the end of year y (y=0: day one)."""
    loan = price * (1 - DOWN)
    i = rate / 12
    pmt = loan * i / (1 - (1 + i) ** -360)
    mr = (1 + r) ** (1 / 12) - 1
    renter = basis_r = price * (DOWN + BUY_COST)
    buyer_pf = basis_b = 0.0
    bal = loan
    rows = [(0, 0, price * (1 - SELL_COST) - loan, renter)]
    for y in range(1, years + 1):
        v0 = price * (1 + g) ** (y - 1)
        rent_m = rent * (1 + rg) ** (y - 1)   # rent growth stays 3% when only home prices change
        own_m = (pmt if y <= 30 else 0) + (TAX_RATE * v0 + INSURANCE * (1 + g) ** (y - 1) + MAINT * v0) / 12
        for _ in range(12):
            if y <= 30:
                bal = bal * (1 + i) - pmt
            renter *= 1 + mr
            buyer_pf *= 1 + mr
            if own_m > rent_m:
                renter += own_m - rent_m; basis_r += own_m - rent_m
            else:
                buyer_pf += rent_m - own_m; basis_b += rent_m - own_m
        v = price * (1 + g) ** y
        b_nw = v * (1 - SELL_COST) - max(bal, 0) + buyer_pf - CGT * (buyer_pf - basis_b)
        r_nw = renter - CGT * (renter - basis_r)
        rows.append((own_m, rent_m, b_nw, r_nw))
    return pmt, rows


def breakeven(**kw):
    _, rows = model(**kw)
    return next((y for y in range(1, len(rows)) if rows[y][2] >= rows[y][3]), None)


# ---- base case: every spoken number asserted
pmt, ROWS = model()
down = PRICE * DOWN
loan = PRICE - down
closing = PRICE * BUY_COST
cash = down + closing
tax_m = PRICE * TAX_RATE / 12
ins_m = INSURANCE / 12
maint_m = PRICE * MAINT / 12
own_m = pmt + tax_m + ins_m + maint_m
gap_m = own_m - RENT
# year-one interest vs principal
bal, int_y1 = loan, 0.0
for _ in range(12):
    it = bal * RATE / 12; int_y1 += it; bal = bal + it - pmt
prin_y1 = loan - bal
paid_y1 = 12 * pmt
lost_return_y1 = cash * RETURN
gone_m = (int_y1 + PRICE * TAX_RATE + INSURANCE + PRICE * MAINT + lost_return_y1) / 12
apprec_y1 = PRICE * GROWTH
net_gone_m = gone_m - apprec_y1 / 12
value_5 = PRICE * (1 + GROWTH) ** 5
sell_5 = value_5 * SELL_COST
fees_5 = closing + sell_5
ratio = PRICE / (12 * RENT)
BE = breakeven()
gap = {y: ROWS[y][3] - ROWS[y][2] for y in (1, 5, 10, 15, 20, 30)}   # renter minus buyer

assert abs(pmt - 2_309.35) < 0.01                 # "two thousand three hundred nine dollars"
assert down == 84_380 and loan == 337_520         # "about eighty-four thousand" / "three hundred thirty-seven and a half thousand"
assert round(closing) == 12_657                   # "almost thirteen thousand"
assert round(cash) == 97_037                      # "about ninety-seven thousand"
assert abs(tax_m - 316.4) < 0.1                   # "about three hundred sixteen"
assert abs(ins_m - 213.7) < 0.1                   # "about two hundred fourteen"
assert abs(maint_m - 351.6) < 0.1                 # "about three hundred fifty"
assert 3_190 < own_m < 3_192                      # "about three thousand one hundred ninety"
assert 945 < gap_m < 950                          # "about nine hundred fifty more"
assert 27_700 < paid_y1 < 27_750                  # "about twenty-seven thousand seven hundred"
assert 24_400 < int_y1 < 24_500                   # "about twenty-four and a half thousand" (24,465)
assert 3_200 < prin_y1 < 3_300                    # "only about three thousand two hundred"
assert 0.11 < prin_y1 / paid_y1 < 0.12            # donut: ~12% principal
assert 5_800 < lost_return_y1 < 5_850             # "about five thousand eight hundred"
assert 3_390 < gone_m < 3_420                     # "about three thousand four hundred a month"
assert apprec_y1 == 12_657                        # "about twelve thousand seven hundred"
assert 1_050 < apprec_y1 / 12 < 1_060             # "about a thousand fifty-five a month"
assert 2_340 < net_gone_m < 2_360                 # "about two thousand three hundred fifty"
assert 488_500 < value_5 < 489_500                # "about four hundred eighty-nine thousand"
assert 29_000 < sell_5 < 29_500                   # "about twenty-nine thousand"
assert 41_500 < fees_5 < 42_500                   # "about forty-two thousand"
assert 15.6 < ratio < 15.75                       # "about fifteen point seven"
assert 26_900 < 12 * RENT < 27_000                # "about twenty-seven thousand" a year of rent
assert BE == 21 and 0 < gap[20] < 0.002 * ROWS[20][3]   # lines cross between year 20 and 21: "around year twenty"
assert 42_000 < gap[5] < 44_000                   # "about forty-three thousand dollars ahead"
assert 40_000 < gap[10] < 42_000                  # "about forty-one thousand"
assert 125_000 < -gap[30] < 135_000               # buyer "ahead by about a hundred and thirty thousand"
assert ROWS[0][3] > ROWS[0][2]                    # renter starts ahead
assert gap[5] > gap[10] > gap[15] > gap[20] > 0      # "the gap slowly shrinks" (after year 5)
assert ROWS[20][0] < ROWS[20][1]                  # by year 20 rent > owner's monthly cost
# home gain at break-even is within the married exclusion (single: partly taxable, see description)
gain_21 = PRICE * (1 + GROWTH) ** 21 * (1 - SELL_COST) - PRICE - closing
assert EXCL_SINGLE < gain_21 < EXCL_JOINT

# ---- sensitivity: change one number, keep everything else
SENS_RATIO = {x: breakeven(price=12 * RENT * x) for x in (10, 12, 14, 18)}
assert SENS_RATIO == {10: 3, 12: 5, 14: 10, 18: None}      # "about three / five / ten / not within thirty"
S_RATE6 = breakeven(rate=0.06)
S_G4, S_G2 = breakeven(g=0.04), breakeven(g=0.02)
S_R5, S_R7 = breakeven(r=0.05), breakeven(r=0.07)
print('sens', (S_RATE6, S_G4, S_G2, S_R5, S_R7))
assert (S_RATE6, S_G4, S_G2, S_R5, S_R7) == (9, 10, 30, 14, None)
assert breakeven(price=12 * RENT * 18, years=60) is None and breakeven(r=0.07, years=60) is None
print(f"pmt {pmt:,.2f} own {own_m:,.0f} gap {gap_m:,.0f} | int1 {int_y1:,.0f} prin1 {prin_y1:,.0f} | gone {gone_m:,.0f} "
      f"net {net_gone_m:,.0f} | fees5 {fees_5:,.0f} | ratio {ratio:.2f} | BE {BE} | gaps {gap}")

K = lambda v: f"${v / 1e6:.2f}M" if v >= 1e6 else f"${v / 1e3:,.0f}K"
S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook (payoff in the first line)
scene("At today's mortgage rates, a typical American house could take about twenty years to beat renting. Or five. It depends on one number most buyers never check.",
      type="count", to=20, suffix=" years", label="to beat renting, typical US house", sub="Nov 2026 rates · our model, assumptions below", color="gold")
scene("Same rent, same street, a cheaper price, and the answer flips. Most rent versus buy advice skips this part.",
      type="versus", title="Break-even vs renting",
      left={"label": "Typical home today", "value": "~20 yrs", "sub": "price = 15.7 years of rent", "color": "red"},
      right={"label": "Same rent, cheaper home", "value": "~5 yrs", "sub": "price = 12 years of rent", "color": "green"},
      verdict="One number moves the answer")
scene("So we'll run the full math nobody shows you: the mortgage, property tax, insurance, repairs, the fees to buy and sell, and what your down payment could have earned instead.",
      type="bullets", title="The full math",
      items=["Mortgage, tax, insurance, repairs", "Fees to buy and to sell", "What your cash could earn instead"])
scene("By the end, you'll know that one number for your own city, and you'll have a five-question checklist to use before you sign anything.",
      type="title", title="Rent vs Buy", sub="the full math, and a checklist")

# ---------------------------------------------------------------- 1
scene("Chapter one. The two homes.", type="chapter", n=1, title="The two homes")
scene("We'll use real, current US numbers. In October, the median existing single-family home sold for four hundred twenty-one thousand nine hundred dollars, according to the National Association of Realtors.",
      type="stat", value=f"${PRICE:,}", label="median US single-family home price", sub="existing homes, October 2026 · NAR", color="gold")
scene("Renting a similar home? Zillow says the typical single-family rent in October was two thousand two hundred forty-three dollars a month, up three point two percent from a year earlier.",
      type="versus", title="The same kind of home",
      left={"label": "Buy", "value": f"${PRICE / 1e3:,.1f}K", "sub": "median price · NAR", "color": "blue"},
      right={"label": "Rent", "value": f"${RENT:,}", "sub": "a month · Zillow, Oct 2026", "color": "green"})
scene("Our buyer puts twenty percent down, about eighty-four thousand dollars, and borrows the rest, about three hundred thirty-seven and a half thousand, on a thirty-year fixed mortgage.",
      type="equation", title="The buyer's loan",
      lines=[{"text": f"${PRICE:,} × 20% = ${down:,.0f} down", "color": "muted", "size": 76},
             {"text": f"Loan: ${loan:,.0f}", "color": "gold", "size": 120},
             {"text": "30-year fixed", "color": "text", "size": 56}])
scene("The rate: Freddie Mac's weekly survey put the average thirty-year fixed rate at seven point two eight percent on November nineteenth. A year earlier, it was six point two six.",
      type="columns", title="30-year fixed mortgage rate (Freddie Mac)", highlight=1, color="blue",
      items=[{"label": "Nov 2025", "value": RATE_YR_AGO * 100, "display": "6.26%"},
             {"label": "Nov 19, 2026", "value": RATE * 100, "display": "7.28%"}])
scene("On top of the down payment come closing costs. Redfin says buyers usually pay two to five percent of the price. We'll use three percent: almost thirteen thousand dollars.",
      type="stat", value=f"${closing:,.0f}", label="closing costs to buy (3%, our assumption)", sub="Redfin: buyers usually pay 2%–5%", color="red")
scene("So the buyer needs about ninety-seven thousand dollars in cash on day one. The renter keeps that money and invests it. Now, what does owning really cost each month? More than the mortgage.",
      type="stat_grid", title="Cash on day one",
      items=[{"value": f"${down:,.0f}", "label": "down payment", "sub": "20%", "color": "blue"},
             {"value": f"${closing:,.0f}", "label": "closing costs", "sub": "3%", "color": "red"},
             {"value": f"${cash:,.0f}", "label": "total cash", "sub": "the renter invests this", "color": "gold"}])

# ---------------------------------------------------------------- 2
scene("Chapter two. The monthly bill.", type="chapter", n=2, title="The monthly bill")
scene("The mortgage payment, principal plus interest, is about two thousand three hundred nine dollars a month, fixed for thirty years.",
      type="count", to=round(pmt), prefix="$", label="mortgage payment a month", sub=f"${loan:,.0f} at 7.28% for 30 years", color="blue")
scene("Then property tax. The data firm Attom puts the average effective rate on US single-family homes at about zero point nine percent of the value a year. Here, that's about three hundred sixteen dollars a month.",
      type="equation", title="Property tax",
      lines=[{"text": f"${PRICE:,} × 0.9% ÷ 12", "color": "muted", "size": 84},
             {"text": f"≈ ${tax_m:,.0f} a month", "color": "gold", "size": 120},
             {"text": "national average rate · ATTOM, 2025", "color": "text", "size": 48}])
scene("Home insurance: NerdWallet's typical US premium in early twenty twenty-six was two thousand five hundred sixty-four dollars a year. About two hundred fourteen a month, and far more in some states.",
      type="stat", value=f"${INSURANCE:,}", label="typical home insurance a year", sub=f"≈ ${ins_m:,.0f} a month · NerdWallet, 2026", color="gold")
scene("And repairs. A common rule of thumb says set aside about one percent of the home's value every year. It's a rough guide, not data: older homes can need more. Here, about three hundred fifty a month.",
      type="quote", text="Budget about 1% of\nthe home's value a year", first_color="text", color="gold",
      source=f"rule of thumb for repairs · here ≈ ${maint_m:,.0f} a month")
scene("Add it up, and owning costs about three thousand one hundred ninety dollars a month. Renting the same kind of home: two thousand two hundred forty-three.",
      type="waterfall", title="Monthly cost, year one",
      steps=[{"label": "Mortgage", "value": pmt, "kind": "start", "display": f"${pmt:,.0f}"},
             {"label": "Tax", "value": tax_m, "kind": "plus", "display": f"+${tax_m:,.0f}", "color": "red"},
             {"label": "Insurance", "value": ins_m, "kind": "plus", "display": f"+${ins_m:,.0f}", "color": "red"},
             {"label": "Repairs", "value": maint_m, "kind": "plus", "display": f"+${maint_m:,.0f}", "color": "red"},
             {"label": "Owning", "value": own_m, "kind": "total", "display": f"${own_m:,.0f}"},
             {"label": "Renting", "value": RENT, "kind": "start", "display": f"${RENT:,}", "color": "green"}])
scene("That's about nine hundred fifty dollars a month more to own. But that comparison is unfair to the buyer, because part of that payment isn't a cost at all.",
      type="equation", title="Owning vs renting, per month",
      lines=[{"text": f"${own_m:,.0f} − ${RENT:,}", "color": "muted", "size": 90},
             {"text": f"≈ ${gap_m:,.0f} more to own", "color": "red", "size": 120},
             {"text": "but is it all a cost?", "color": "gold", "size": 60}])

# ---------------------------------------------------------------- 3
scene("Chapter three. Money gone, money kept.", type="chapter", n=3, title="Money gone, money kept")
scene("In year one, the buyer pays the bank about twenty-seven thousand seven hundred dollars. About twenty-four and a half thousand of it is interest. Only about three thousand two hundred pays down the loan.",
      type="donut", title="Mortgage payments, year one",
      segments=[{"label": f"Interest (${int_y1 / 1e3:.1f}K)", "value": int_y1, "color": "red"},
                {"label": f"Loan payoff (${prin_y1 / 1e3:.1f}K)", "value": prin_y1, "color": "green"}],
      center=f"${paid_y1 / 1e3:.1f}K", center_sub="paid in year one")
scene("That loan payoff is savings. It's still yours. So the honest comparison is the money that's gone for good: interest, tax, insurance and repairs. These are often called unrecoverable costs.",
      type="bullets", title="Gone for good (unrecoverable)", color="red",
      items=["Mortgage interest", "Property tax", "Insurance", "Repairs"])
scene("Plus one that's easy to miss: that ninety-seven thousand dollars of cash. Invested at six percent a year, our assumption, it could have earned about five thousand eight hundred dollars in year one.",
      type="equation", title="What the cash could have earned",
      lines=[{"text": f"${cash:,.0f} × 6% a year", "color": "muted", "size": 84},
             {"text": f"≈ ${lost_return_y1:,.0f} in year one", "color": "gold", "size": 116},
             {"text": "assumed return, not guaranteed", "color": "text", "size": 52}])
scene("Add it all up, and the buyer's money that's gone is about three thousand four hundred dollars a month. The renter's rent is gone too: two thousand two hundred forty-three.",
      type="hbars", title="Money gone for good, per month (year one)",
      items=[{"label": "Owning", "value": gone_m, "display": f"${gone_m:,.0f}", "color": "red"},
             {"label": "Renting", "value": RENT, "display": f"${RENT:,}", "color": "green"}])
scene("Now the buyer's big advantage: the house can grow in value. At an assumed three percent a year, that's about twelve thousand seven hundred dollars in year one. But prices don't always rise. Over the past year, the national median rose just zero point four percent.",
      type="stat_grid", title="Home price growth",
      items=[{"value": "+3%", "label": "our assumption, a year", "sub": f"≈ ${apprec_y1:,.0f} in year one", "color": "green"},
             {"value": "+0.4%", "label": "actual, past year", "sub": "US median, Oct 2026 · NAR", "color": "gold"}])
scene("Take that growth off, and owning costs about two thousand three hundred fifty a month, against two thousand two hundred forty-three for renting. Close. So why could break-even take twenty years? Two big fees: one to get in, one to get out.",
      type="versus", title="Money gone, minus price growth (per month)",
      left={"label": "Owning", "value": f"${net_gone_m:,.0f}", "sub": "if prices rise 3% a year", "color": "blue"},
      right={"label": "Renting", "value": f"${RENT:,}", "sub": "rent", "color": "green"},
      verdict="Close. So why so long?")

# ---------------------------------------------------------------- 4
scene("Chapter four. The fees to get in and out.", type="chapter", n=4, title="The fees to get in and out")
scene("Getting in costs those closing costs. Getting out costs more. In one twenty twenty-six survey, agent commissions alone averaged about five and a half percent of the sale price. We assume six percent in total to sell.",
      type="share", title="Fees as a share of the home price",
      rows=[{"label": "To buy (closing costs)", "share": BUY_COST, "color": "gold", "dp": 0},
            {"label": "To sell (agents + other costs)", "share": SELL_COST, "color": "red", "dp": 0}],
      note="Our assumptions · Redfin: 2–5% to buy · Clever (2026): agent fees avg 5.46%")
scene("Sell after five years, and the house might be worth about four hundred eighty-nine thousand dollars. Six percent of that is about twenty-nine thousand. Add the thirteen thousand to buy, and that's about forty-two thousand dollars in fees.",
      type="equation", title="Buy now, sell in 5 years",
      lines=[{"text": f"${closing / 1e3:.1f}K to buy + ${sell_5 / 1e3:.1f}K to sell", "color": "muted", "size": 80},
             {"text": f"≈ ${fees_5 / 1e3:.0f}K in fees", "color": "red", "size": 130},
             {"text": f"if the home is worth ${value_5 / 1e3:.0f}K by then", "color": "text", "size": 52}])
scene("To come out ahead, the buyer has to win those fees back, through rising prices and paying down the loan, before the renter's investments pull too far ahead.",
      type="flywheel", title="How the buyer catches up", center="Equity",
      steps=["Prices rise", "Loan shrinks", "Rent keeps rising", "Payment stays fixed"])
scene("Fees come first. Time pays them back, slowly. So when does the buyer actually catch up? Let's run all thirty years.",
      type="quote", text="Fees come first.\nTime pays them back.", first_color="text", color="gold")

# ---------------------------------------------------------------- 5
scene("Chapter five. The break-even year.", type="chapter", n=5, title="The break-even year")
scene("Here are the rules. Each month, whoever spends less invests the difference at six percent. Rent, home prices, tax, insurance and repairs all rise three percent a year. These are assumptions, not predictions.",
      type="bullets", title="The rules (our assumptions)",
      items=["Whoever spends less invests the gap at 6%", "Rent and home prices rise 3% a year",
             "Tax, insurance, repairs rise 3% too"])
scene("When we compare, the renter pays fifteen percent tax on investment gains, a typical US rate on long-term gains. The buyer's home profit is usually tax-free, up to a limit. And the buyer pays the six percent to sell.",
      type="stat_grid", title="When each side cashes out",
      items=[{"value": "15%", "label": "tax on investment gains", "sub": "IRS: at most 15% for most people", "color": "blue"},
             {"value": "0%", "label": "tax on home profit", "sub": "up to $250K / $500K married", "color": "green"},
             {"value": "6%", "label": "cost to sell the home", "sub": "our assumption", "color": "red"}])
scene("Here's how far ahead the renter would be if both cashed out. The renter starts ahead, with all that cash invested. The buyer starts behind, because of the fees. Then the gap slowly shrinks.",
      type="columns", title="Renter's lead if both cashed out", color="green", highlight=1,
      items=[{"label": f"Year {y}", "value": gap[y], "display": K(gap[y])} for y in (1, 5, 10, 15, 20)],
      note="our model · assumptions above · not a prediction")
scene("After five years, the renter is about forty-three thousand dollars ahead. After ten, still about forty-one thousand ahead.",
      type="table", title="Wealth if cashed out (our model)",
      header=["Year", "Buyer", "Renter", "Ahead"],
      rows=[[str(y), K(ROWS[y][2]), K(ROWS[y][3]), ("Renter +" if gap[y] > 0 else "Buyer +") + K(abs(gap[y]))]
            for y in (1, 5, 10, 20, 30)],
      col_colors={"1": "gold", "2": "green", "3": "text"})
scene("Then, around year twenty, the lines cross. Rent keeps rising every year, while the mortgage payment stays fixed. By then, the rent costs more than owning each month, and the buyer pulls ahead.",
      type="timeline", title="Thirty years, two paths",
      events=[{"when": "Year 0", "text": "Buyer pays\n$97K cash"},
              {"when": "Year 5", "text": "Renter ahead\nby ~$43K"},
              {"when": "Year 20", "text": "Lines\ncross"},
              {"when": "Year 30", "text": "Mortgage\npaid off"}])
scene("By year thirty, with the mortgage paid off, the buyer is ahead by about a hundred and thirty thousand dollars.",
      type="stat", value=f"+{K(-gap[30])}", label="buyer ahead after 30 years", sub="our model · assumed 3% price growth, 6% returns", color="gold")
scene("But only if the renter really invests the difference, every month, for decades. Many people don't. A mortgage forces you to save. Renting doesn't. So is buying a bad deal? Not necessarily. Watch what happens when we change one number.",
      type="quote", text="Renting wins only if you\ninvest the difference.", first_color="text", color="green")

# ---------------------------------------------------------------- 6
scene("Chapter six. Change one number.", type="chapter", n=6, title="Change one number")
scene("That number is the price-to-rent ratio. Divide the home's price by a full year of rent. Here, four hundred twenty-one thousand nine hundred, divided by about twenty-seven thousand, is about fifteen point seven.",
      type="equation", title="Price-to-rent ratio",
      lines=[{"text": f"${PRICE:,} ÷ (${RENT:,} × 12)", "color": "muted", "size": 84},
             {"text": f"≈ {ratio:.1f}", "color": "gold", "size": 150},
             {"text": "years of rent to buy the home", "color": "text", "size": 54}])
scene("Keep the same rent, and change only the price. At twelve times a year's rent, break-even drops to about five years. At ten times, about three. At fourteen, about ten. And at eighteen, the buyer doesn't catch up within thirty years.",
      type="hbars", title="Break-even year, by price-to-rent ratio", format="num",
      items=[{"label": "10×", "value": SENS_RATIO[10], "display": "3 yrs", "color": "green"},
             {"label": "12×", "value": SENS_RATIO[12], "display": "5 yrs", "color": "green"},
             {"label": "14×", "value": SENS_RATIO[14], "display": "10 yrs", "color": "gold"},
             {"label": "15.7× (ours)", "value": BE, "display": "~20 yrs", "color": "gold"},
             {"label": "18×", "value": 31, "display": "30+ yrs", "color": "red"}])
scene("Real cities show the same spread. Back in June, when rates were lower, Zillow estimated buying pays off in about six years nationally. In Columbus, Ohio, about four. In San Diego, over twenty-three. In San Francisco and San Jose, never within thirty years.",
      type="columns", title="Zillow: years for buying to pay off (June 2026)", format="num", highlight=1,
      items=[{"label": "Columbus", "value": ZILLOW_COLUMBUS, "display": "4.1"},
             {"label": "US", "value": ZILLOW_BE, "display": "~6"},
             {"label": "San Diego", "value": ZILLOW_SD, "display": "23.3"},
             {"label": "San Francisco", "value": 30, "display": "never", "color": "red"}],
      note="Zillow's own model · Freddie Mac rate then 6.48%, now 7.28%")
scene("Other dials matter too. A six percent mortgage rate: about nine years. Home prices rising four percent a year: about ten. Only two percent: about thirty. Investments earning five percent: about fourteen. Earning seven: the renter stays ahead for over thirty years.",
      type="table", title="Change one thing (everything else the same)",
      header=["Change", "Break-even"],
      rows=[["Our base case", "~20 yrs"], ["Mortgage rate 6%", f"{S_RATE6} yrs"], ["Prices +4% a year", f"{S_G4} yrs"],
            ["Prices +2% a year", f"{S_G2} yrs"], ["Investments earn 5%", f"{S_R5} yrs"], ["Investments earn 7%", "30+ yrs"]],
      highlight_row=0, col_colors={"1": "gold"})
scene("From three years to more than thirty, from small changes. So anyone who says renting is throwing money away, or that buying is always a trap, is skipping the math. How do you find your own answer? Five questions.",
      type="quote", text="\"Renting is throwing money away\"\nskips the math.", first_color="text", color="gold")

# ---------------------------------------------------------------- 7
scene("Chapter seven. Your checklist.", type="chapter", n=7, title="Your checklist")
scene("One: how long will you stay? Two: what's the price-to-rent ratio where you live? Three: what's the full monthly cost, not just the mortgage? Four: can you afford the fees to buy and to sell? Five: if you rent, will you really invest the difference?",
      type="bullets", title="Rent or buy: 5 questions",
      items=["How long will you stay?", "Price ÷ yearly rent where you live?", "Full monthly cost, not just the mortgage?",
             "Can you afford the fees to buy and sell?", "Will you invest the difference?"])
scene("For question one: short stays usually favor renting, because the fees come first. With our numbers, selling after five years leaves the buyer about forty-three thousand dollars behind.",
      type="stat", value=f"−{K(gap[5])}", label="buyer vs renter after 5 years", sub="our model · fees come first", color="red")
scene("For question three, use the same list we did: interest, tax, insurance, about one percent for repairs, and what your cash could earn. Take off the price growth you expect, then compare that with the rent.",
      type="equation", title="Your own comparison",
      lines=[{"text": "Interest + tax + insurance + repairs", "color": "muted", "size": 64},
             {"text": "+ lost return − price growth", "color": "muted", "size": 64},
             {"text": "vs. rent", "color": "gold", "size": 120}])
scene("And remember what the math leaves out. Owning gives you stability and control over your home. Renting gives you flexibility, and the landlord pays for the new roof. Only you can put a price on those.",
      type="versus", title="What the math leaves out",
      left={"label": "Owning", "value": "Stability", "sub": "your home, your rules", "color": "blue"},
      right={"label": "Renting", "value": "Flexibility", "sub": "easy to move, no roof bills", "color": "green"})
scene("Rent versus buy isn't a moral question. It's a math question, and a life question. How long you stay and your local prices decide most of it. Run your own numbers before you sign anything.",
      type="title", title="Run your own numbers", sub="how long you stay + local prices decide it")
scene("If this helped, subscribe. We break down how money really works, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

# ---------------------------------------------------------------- checks
types = [s["visual"]["type"] for s in S]
for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])
words = sum(len(s["say"].split()) for s in S)
chapters = [s["visual"]["title"] for s in S if s["visual"]["type"] == "chapter"]
assert 1400 <= words <= 1700, words
assert 40 <= len(S) <= 70, len(S)
assert 6 <= len(chapters) <= 7
assert len(set(types)) >= 10
# retention: payoff number inside the first ~10 s; intro (before chapter 1) under ~60 s of speech
assert S[0]["say"].startswith("At today's mortgage rates, a typical American house could take about twenty years")
intro_words = sum(len(x["say"].split()) for x in S[:types.index("chapter")])
assert intro_words <= 150, intro_words
# every chapter's last scene ends with a one-line open loop into the next chapter
LOOPS = ["Now, what does owning really cost each month?", "part of that payment isn't a cost at all",
         "So why could break-even take twenty years?", "So when does the buyer actually catch up?",
         "Watch what happens when we change one number.", "How do you find your own answer? Five questions."]
ends = [S[k - 1]["say"] for k, t in enumerate(types) if t == "chapter" and k > types.index("chapter")]
assert len(ends) == len(LOOPS) and all(l in e for l, e in zip(LOOPS, ends)), ends

SOURCES = [
    "National Association of Realtors, Existing-Home Sales Decreased 5.5% in October (Nov 12, 2026): https://www.nar.realtor/newsroom/existing-home-sales-decreased-5-5-percent-october-nar-report",
    "Zillow, A house doesn't have to mean a mortgage: Renting requires $14K less income than buying (Nov 12, 2026; typical single-family rent, Zillow Observed Rent Index): https://s25.q4cdn.com/975009107/files/doc_news/A-house-doesnt-have-to-mean-a-mortgage-Renting-requires-14K-less-income-than-buying-2026.pdf",
    "Zillow, Rent or buy: How long it takes for buying a home to pay off in each metro (Jun 4, 2026): https://zillow.mediaroom.com/2026-06-04-Rent-or-buy-How-long-it-takes-for-buying-a-home-to-pay-off-in-each-metro",
    "Freddie Mac, Primary Mortgage Market Survey (Nov 19, 2026 and Jun 4, 2026): https://www.freddiemac.com/pmms",
    "ATTOM, 2025 property tax analysis (Apr 9, 2026): https://www.attomdata.com/news/market-trends/home-sales-prices/2025-annual-tax-report",
    "NerdWallet, Home insurance pricing report 2026 (Oct 2, 2026): https://www.nerdwallet.com/insurance/homeowners/home-insurance-pricing-report-2026",
    "Redfin, What are closing costs (Apr 24, 2026): https://www.redfin.com/blog/closing-costs-when-buying-a-home/",
    "Clever Real Estate, True cost of selling a home: 2026 edition (Oct 26, 2026): https://listwithclever.com/research/how-much-does-it-cost-to-sell-a-house/",
    "IRS Topic 409, Capital gains and losses: https://www.irs.gov/taxtopics/tc409",
    "IRS Topic 701, Sale of your home: https://www.irs.gov/taxtopics/tc701",
]

DESCRIPTION = (
    "Rent vs buy a home: we run the full math for a typical US house at today's mortgage rates, including "
    "property tax, insurance, repairs, closing and selling costs, and what your down payment could earn if you "
    "rented instead. With our assumptions, buying takes about 20 years to beat renting, but one number, the "
    "price-to-rent ratio, can cut that to 5 years or push it past 30. Plus a 5-question checklist.\n\n"
    f"Our example: ${PRICE:,} home (NAR median single-family, Oct 2026), ${RENT:,}/month rent (Zillow typical "
    f"single-family rent, Oct 2026), 20% down, 30-year fixed at 7.28% (Freddie Mac, Nov 19, 2026), property tax "
    f"0.9% a year (ATTOM), insurance ${INSURANCE:,} a year (NerdWallet).\n"
    "Assumptions (ours, not predictions): 3% to buy, 6% to sell, repairs 1% of value a year (a rule of thumb), "
    "home prices, rent and costs grow 3% a year, investments earn 6% a year, whoever spends less each month "
    "invests the difference, 15% tax on investment gains when cashed out, the home's gain is tax-free (true up to "
    "$250,000 single / $500,000 married; at year 21 our example gain is above the single limit), no "
    "mortgage-interest deduction (it only helps if you itemize), no renters insurance. Real returns, prices and "
    "rents vary and can be negative. Zillow's break-even estimates use Zillow's own model and assumptions.\n\n"
    "Sources:\n" + "\n".join("- " + s for s in SOURCES) + "\n\n"
    "For education only. Not financial advice. Past results don't guarantee future returns.\n\n"
    "#rentvsbuy #realestate #personalfinance #homebuying #mortgage"
)

spec = {
    "id": "L009_rent_vs_buy", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "MONEY TRAPS",
    "disclaimer": "Illustration · assumed returns & growth · not financial advice",
    "title": "Rent vs Buy a Home: The Full Math Nobody Shows You",
    "intro_chapter": "20 years or 5?",
    "thumbnail": {"big": "20 YRS", "line": "TO BEAT RENTING?", "tag": "RENT VS BUY: FULL MATH", "color": "gold"},
    "description": DESCRIPTION,
    "tags": ["rent vs buy", "rent or buy a house", "renting vs buying a home", "is renting throwing money away",
             "price to rent ratio", "break even buying a house", "mortgage rates 2026", "home buying",
             "real estate math", "personal finance", "first time home buyer", "opportunity cost"],
    "localizations": {
        "es": {"title": "Alquilar o comprar casa: las cuentas que nadie te muestra",
               "summary": "Alquilar o comprar vivienda en EE. UU.: hacemos todas las cuentas con una casa típica "
                          "y las tasas hipotecarias actuales (7,28%), incluyendo impuestos, seguro, reparaciones, "
                          "costos de compra y venta, y lo que podría rendir el pago inicial. Con nuestros supuestos, "
                          "comprar tarda unos 20 años en superar al alquiler, pero un solo número puede bajarlo a 5."},
        "pt": {"title": "Alugar ou comprar casa: a conta que ninguém mostra",
               "summary": "Alugar ou comprar imóvel nos EUA: fazemos a conta completa com uma casa típica e os "
                          "juros atuais (7,28%), incluindo impostos, seguro, reparos, custos de compra e venda e o "
                          "que a entrada poderia render. Com nossas premissas, comprar leva cerca de 20 anos para "
                          "superar o aluguel, mas um único número pode reduzir isso para 5."},
        "hi": {"title": "किराया या घर ख़रीदें: पूरा हिसाब जो कोई नहीं दिखाता",
               "summary": "अमेरिका में किराए पर रहें या घर ख़रीदें? आज की 7.28% मॉर्गेज दर पर एक सामान्य घर का "
                          "पूरा हिसाब: टैक्स, बीमा, मरम्मत, ख़रीदने-बेचने का ख़र्च, और डाउन पेमेंट निवेश करने पर "
                          "कितना कमाता। हमारी मान्यताओं पर ख़रीदना लगभग 20 साल में किराए से आगे निकलता है, "
                          "लेकिन एक संख्या इसे 5 साल तक ला सकती है।"},
        "id": {"title": "Sewa atau Beli Rumah: Hitungan Lengkap yang Jarang Dibahas",
               "summary": "Sewa atau beli rumah di AS: kami hitung lengkap untuk rumah biasa dengan bunga KPR saat "
                          "ini (7,28%), termasuk pajak, asuransi, perbaikan, biaya beli dan jual, serta hasil yang "
                          "bisa didapat dari uang muka. Dengan asumsi kami, membeli butuh sekitar 20 tahun untuk "
                          "mengalahkan sewa, tetapi satu angka bisa memangkasnya jadi 5 tahun."},
        "de": {"title": "Mieten oder kaufen: Die ganze Rechnung, die keiner zeigt",
               "summary": "Mieten oder kaufen in den USA: Wir rechnen ein typisches Haus zum aktuellen Zins von "
                          "7,28 % komplett durch, mit Grundsteuer, Versicherung, Reparaturen, Kauf- und "
                          "Verkaufskosten und dem, was das Eigenkapital anderswo bringen könnte. Mit unseren "
                          "Annahmen dauert es rund 20 Jahre, bis Kaufen das Mieten schlägt; eine Zahl kann daraus "
                          "5 Jahre machen."},
        "fr": {"title": "Louer ou acheter : le vrai calcul que personne ne montre",
               "summary": "Louer ou acheter aux États-Unis : nous faisons le calcul complet pour une maison type au "
                          "taux actuel de 7,28 %, avec taxe foncière, assurance, travaux, frais d'achat et de vente, "
                          "et ce que l'apport aurait pu rapporter. Avec nos hypothèses, acheter met environ 20 ans à "
                          "battre la location, mais un seul chiffre peut ramener cela à 5 ans."},
    },
    "scenes": S,
}
assert len(spec["title"]) < 60, len(spec["title"])
assert len(spec["thumbnail"]["big"]) <= 6 and len(spec["thumbnail"]["line"]) <= 22
assert all(len(l["title"]) <= 60 for l in spec["localizations"].values())

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L009_rent_vs_buy.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words,", len(chapters), "chapters, intro", intro_words, "words, title",
      len(spec["title"]), "chars")
print("types:", dict(Counter(types)))
