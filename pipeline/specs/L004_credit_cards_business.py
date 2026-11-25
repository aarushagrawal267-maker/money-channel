"""Long-form L004: How credit card companies really make money.

Sources (checked 2026-11-22):
  [NYF] New York Fed, Household Debt and Credit Report, Q3 2026 (press release Nov 10, 2026):
        credit card balances $1.285T ("$1.29 trillion"), up $22B from Q2 2026.
  [G19] Federal Reserve G.19 Consumer Credit release, Nov 6, 2026, Terms of Credit table,
        commercial bank credit card plans, accounts assessed interest (%): 2021 16.45, 2022 17.91,
        2023 22.15, 2024 22.89, 2025 22.32, Q3 2026 (preliminary) 22.36. All accounts Q3 2026: 21.19.
  [CFPB] CFPB, The Consumer Credit Card Market (report to Congress, Dec 30, 2025; data for 2024):
        interest assessed $160B in 2024 vs $105B in 2022 (+52%); cardholders +9.5%; fees $31.3B
        (late $17.0B, annual $8.7B, other $5.6B); fees = 16% of the cost of cards; ~50% of accounts
        revolve; ~15% of general purpose cardholders pay only the minimum (highest since at least 2015);
        purchase volume $3.6T; rewards earned $47.5B; rewards redeemed by tier (Figure 103, 2024):
        superprime $18.5B, prime plus $16.6B, prime $5.0B, below-prime $2.9B; deep subprime hold ~14% of
        accounts but generate 40% of late fees, superprime + prime plus hold 59% of accounts and pay 7.8%.
  [VIRF] Visa USA Interchange Reimbursement Fees, rates effective Oct 24, 2026 (Visa's published default
        rates; large merchants can negotiate lower). Consumer credit, card present:
        Retail Credit-Performance Threshold III: All Other Products 1.51% + $0.10, Traditional Rewards
        1.65% + $0.10, Signature Preferred 2.10% + $0.10, Infinite (spend qualified) 2.30% + $0.10.
        Signature Preferred: Supermarket Tier I 1.65% + $0.05, Travel 2.40% + $0.10, Restaurant 2.60%.
  [V10K] Visa FY2026 Form 10-K (fiscal year ended Sep 30, 2026; filed Nov 5, 2026) and Q4 FY2026
        earnings release (8-K, Oct 27, 2026), $ millions: net revenue 45,903; net income 23,504;
        service 19,918; data processing 23,374; international 15,251; other 5,677; client incentives
        (18,317); nominal payments volume FY2026 $15,338B. "Visa is not a financial institution. We do
        not issue cards, extend credit or set rates and fees for account holders..." "Generally, IRFs
        are paid by acquirers to issuers."
  [COF] Capital One 2025 Form 10-K (filed Feb 19, 2026), Table 8 Credit Card Business Results, 2024
        column ($ millions): net interest income 22,088; non-interest income 6,076; total net revenue
        28,164; provision for credit losses 10,272; non-interest expense 13,576; pre-tax 4,316; tax 1,024;
        net income 3,292; net charge-off rate 5.88%. Note 18: interchange fees, net (consolidated, 2024)
        4,882, "presented net of customer reward expenses of ... $9.0 billion" (2024). 2024 is used
        because 2025 is distorted by the Discover acquisition (May 2025).
  [FRB] Agarwal, Presbitero, Silva & Wix, "Who Pays For Your Rewards? Redistribution in the Credit Card
        Market", Federal Reserve FEDS 2023-007 (Jan 2023): ~$15B a year redistributed from poorer/less
        educated to richer/more educated areas. (Authors' views, not the Fed's.)
  [BOS] Schuh, Shy & Stavins, "Who Gains and Who Loses from Credit Card Payments?", Boston Fed Public
        Policy Discussion Paper 10-3 (2010): each cash-using household pays $149 a year to card-using
        households; each card-using household receives $1,133.
  [CARD] Credit CARD Act of 2009 / Regulation Z 12 CFR 1026.5(b)(2)(ii): statements must be mailed or
        delivered at least 21 days before the payment due date.
  [L001] Costco FY2026 net income $9,226M on revenue $303,154M (see L001_costco.py).
"""
import json, os

# ---- [NYF]
CARD_BAL = 1.285e12
CARD_BAL_QOQ = 22e9
# ---- [G19]
APR_HIST = {2021: 16.45, 2022: 17.91, 2023: 22.15, 2024: 22.89, 2025: 22.32, 2026: 22.36}  # 2026 = Q3 prelim
APR = APR_HIST[2026] / 100
APR_ALL = 21.19 / 100
# ---- [CFPB]
INTEREST_24, INTEREST_22 = 160e9, 105e9
FEES_24 = 31.3e9
LATE_24, ANNUAL_24, OTHER_FEES_24 = 17.0e9, 8.7e9, 5.6e9
REVOLVE_SHARE = 0.50
MIN_ONLY_SHARE = 0.15
PURCHASES_24 = 3.6e12
REWARDS_24 = 47.5e9
REDEEMED = {"Superprime": 18.5e9, "Prime plus": 16.6e9, "Prime": 5.0e9, "Below prime": 2.9e9}
DEEP_SUB_ACCTS, DEEP_SUB_LATE = 0.14, 0.40
TOP_ACCTS, TOP_LATE = 0.59, 0.078
# ---- [VIRF] (rate, fixed $) on a $100 card-present purchase
SALE = 100
IRF = {"Basic": (0.0151, 0.10), "Rewards": (0.0165, 0.10), "Premium": (0.0210, 0.10), "Top tier": (0.0230, 0.10)}
IRF_PREMIUM_BY_STORE = {"Supermarket": (0.0165, 0.05), "Retail store": (0.0210, 0.10),
                        "Travel": (0.0240, 0.10), "Restaurant": (0.0260, 0.0)}
# ---- [V10K] $
V_REV, V_NI = 45_903e6, 23_504e6
V_GROSS = {"service": 19_918e6, "data": 23_374e6, "intl": 15_251e6, "other": 5_677e6}
V_INCENTIVES = 18_317e6
V_PAY_VOL = 15_338e9
# ---- [COF] 2024 credit card business, $
C_NII, C_NONII, C_REV = 22_088e6, 6_076e6, 28_164e6
C_PROV, C_EXP, C_PRETAX, C_TAX, C_NI = 10_272e6, 13_576e6, 4_316e6, 1_024e6, 3_292e6
C_NCO_RATE = 0.0588
C_IX_NET, C_REWARDS = 4_882e6, 9.0e9
# ---- [FRB], [BOS], [CARD], [L001]
REDISTRIB = 15e9
CASH_PAYS, CARD_GETS = 149, 1133
GRACE_MIN_DAYS = 21
COSTCO_MARGIN = 9_226e6 / 303_154e6

# ---- derived numbers (every spoken one is asserted)
fee = {k: round(SALE * r + f, 2) for k, (r, f) in IRF.items()}
fee_store = {k: round(SALE * r + f, 2) for k, (r, f) in IRF_PREMIUM_BY_STORE.items()}
assert fee == {"Basic": 1.61, "Rewards": 1.75, "Premium": 2.20, "Top tier": 2.40}, fee   # "a dollar sixty", "two forty"
assert fee_store == {"Supermarket": 1.70, "Retail store": 2.20, "Travel": 2.50, "Restaurant": 2.60}, fee_store
store_keeps = SALE - fee["Premium"]
assert abs(store_keeps - 97.80) < 1e-9                    # "ninety-seven dollars and eighty cents"
assert 50e9 < 0.02 * PURCHASES_24 < 100e9                 # "tens of billions of dollars"
assert 1.28e12 < CARD_BAL < 1.30e12                       # "one point two nine trillion" (NY Fed rounds to $1.29T)
interest_5k = 5000 * APR
assert abs(interest_5k - 1118) < 0.5                      # "about eleven hundred dollars a year"
assert 3.0 < interest_5k / 365 < 3.1                      # "roughly three dollars a day"
interest_growth = INTEREST_24 / INTEREST_22 - 1
assert 0.52 <= interest_growth < 0.53                     # "up fifty-two percent"
assert abs(LATE_24 + ANNUAL_24 + OTHER_FEES_24 - FEES_24) < 1e6   # fee breakdown ties out
assert 0.16 <= FEES_24 / (INTEREST_24 + FEES_24) < 0.17   # matches CFPB's "16 percent of the cost"
c_interest_share = C_NII / C_REV
assert 0.78 < c_interest_share < 0.79                     # "almost four out of every five dollars"
assert abs(C_NII + C_NONII - C_REV) < 1e6
assert abs(C_REV - C_PROV - C_EXP - C_PRETAX) < 1e6       # waterfall ties out
assert abs(C_PRETAX - C_TAX - C_NI) < 1e6
c_margin = C_NI / C_REV
assert 0.115 < c_margin < 0.12                            # "about twelve cents"
assert 0.055 < C_NCO_RATE < 0.06                          # "nearly six percent"
c_ix_gross = C_IX_NET + C_REWARDS
rewards_of_ix = C_REWARDS / c_ix_gross
assert 0.64 < rewards_of_ix < 0.67                        # "about two of every three swipe-fee dollars"
assert 13.8e9 < c_ix_gross < 13.95e9                      # "$13.9B"
rewards_vs_cost = REWARDS_24 / (INTEREST_24 + FEES_24)
assert 0.24 < rewards_vs_cost < 0.26                      # "about a quarter"
top2 = (REDEEMED["Superprime"] + REDEEMED["Prime plus"]) / sum(REDEEMED.values())
assert 0.80 < top2 < 0.83                                 # "about four out of every five"
v_margin = V_NI / V_REV
assert 0.51 < v_margin < 0.52                             # "about fifty-one cents"
assert abs(sum(V_GROSS.values()) - V_INCENTIVES - V_REV) < 1e6   # Visa revenue ties out
v_per_100 = V_REV / V_PAY_VOL * 100
assert 0.29 < v_per_100 < 0.31                            # "about thirty cents per hundred dollars"
assert 15e12 < V_PAY_VOL < 15.5e12                        # "over fifteen trillion dollars"
assert 0.029 < COSTCO_MARGIN < 0.031                      # "about three cents"
rewards_2pct = 1000 * 12 * 0.02
assert rewards_2pct == 240                                # "two hundred and forty dollars"
assert interest_5k / rewards_2pct > 4                     # "more than four times over"
net_carry = rewards_2pct - interest_5k
assert abs(net_carry + 878) < 0.5                         # "-$878"
print(f"interest $5k {interest_5k:.0f}; growth {interest_growth:.1%}; COF interest {c_interest_share:.1%} "
      f"margin {c_margin:.1%}; rewards/ix {rewards_of_ix:.1%}; top2 {top2:.1%}; visa {v_margin:.1%} "
      f"{v_per_100:.2f}c/$100; rewards/cost {rewards_vs_cost:.1%}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook
scene("Americans now owe about one point two nine trillion dollars on their credit cards. A record. And it grew another twenty-two billion in just three months.",
      type="count", to=1.29, prefix="$", suffix="T", dp=2, label="owed on US credit cards", sub="Q3 2026 · New York Fed", color="red")
scene("In twenty twenty-four alone, card companies charged one hundred and sixty billion dollars in interest. Plus another thirty-one billion in fees.",
      type="photo", file="assets/photos/credit_cards_fanned.jpg", layout="full", focus=[0.5, 0.5],
      value="$160B", label="interest charged to US cardholders in 2024, plus $31.3B in fees", color="gold")
scene("So who actually gets all that money? The answer involves several companies on every swipe, a fee you never see, and a rewards system that's quietly paid for by someone else.",
      type="title", title="Follow the Swipe", sub="how credit card companies really make money")

# ---------------------------------------------------------------- 1
scene("Chapter one. The players.", type="chapter", n=1, title="The players")
scene("Every card payment involves five parties. You. Your bank, which gave you the card. The network, like Visa or Mastercard. The store. And the store's bank, which handles its card payments.",
      type="bullets", title="Five parties on every swipe",
      items=["You, the cardholder", "Your bank (the issuer)", "The network (Visa, Mastercard)", "The store",
             "The store's bank (the acquirer)"])
scene("The two that people mix up are the network and your bank. The network runs the rails that move the payment. Your bank lends you the money and sends you the bill.",
      type="versus", title="Two very different jobs",
      left={"label": "The network", "value": "Rails", "sub": "moves the payment", "color": "blue"},
      right={"label": "Your bank", "value": "Lender", "sub": "lends money, sends the bill", "color": "gold"},
      verdict="Different jobs, very different profits")
scene("Visa says it plainly in its annual report. It does not issue cards, extend credit, or set the rates and fees you pay. That's your bank's job.",
      type="quote", text="\"We do not issue cards,\nextend credit or set\nrates and fees\"", first_color="text", color="text",
      source="Visa fiscal 2026 annual report (10-K)")
scene("When you tap your card, the store's bank sends the request through the network to your bank, which approves it in moments. Then the money flows back the other way, minus a few small cuts.",
      type="photo", title="One tap, in order", file="assets/photos/card_payment_terminal.jpg", layout="side",
      focus=[0.45, 0.5], value="One tap", color="gold", label="Store → store's bank → network → your bank",
      sub="money flows back, minus fees")

# ---------------------------------------------------------------- 2
scene("Chapter two. The swipe fee.", type="chapter", n=2, title="The swipe fee")
scene("The biggest cut is the interchange fee, also called the swipe fee. The store pays it, and it goes to the bank that issued your card. On a one hundred dollar purchase with a premium rewards card, Visa's published rate works out to two dollars and twenty cents.",
      type="photo", file="assets/photos/credit_cards_visa_mc_amex.jpg", layout="full", focus=[0.5, 0.5],
      value="$2.20", label="swipe fee on a $100 premium-card purchase · goes to your bank", color="gold")
scene("And the fancier the card, the bigger the fee. A basic Visa credit card costs the store about a dollar sixty on that same purchase. A top-tier card, about two forty.",
      type="table", title="Swipe fee on a $100 store purchase (Visa)",
      header=["Card", "Rate", "On $100"],
      rows=[[k, f"{r * 100:.2f}% + 10¢", f"${fee[k]:.2f}"] for k, (r, _) in IRF.items()],
      highlight_row=3, col_colors={"1": "muted", "2": "gold"})
scene("Where you shop matters too. On a premium rewards card, a hundred dollar grocery run can cost the store as little as a dollar seventy. A restaurant meal, two sixty.",
      type="hbars", title="Swipe fee on $100, premium rewards card",
      items=[{"label": k, "value": v, "display": f"${v:.2f}", "color": "gold" if k == "Restaurant" else "green"}
             for k, v in fee_store.items()])
scene("So follow that hundred dollars. The swipe fee goes to your bank, and before its own processing charges, the store ends up with about ninety-seven dollars and eighty cents.",
      type="waterfall", title="A $100 premium-card sale",
      steps=[{"label": "Sale", "value": SALE, "kind": "start", "display": "$100"},
             {"label": "Swipe fee", "value": fee["Premium"], "kind": "minus", "display": "−$2.20"},
             {"label": "Store gets", "value": store_keeps, "kind": "total", "display": "$97.80"}])
scene("Now multiply that by every swipe in America. In twenty twenty-four, people bought three point six trillion dollars of stuff on credit cards. A cut of around two percent of that is tens of billions of dollars a year.",
      type="count", to=3.6, prefix="$", suffix="T", dp=1, label="spent on US credit cards", sub="2024 · CFPB", color="text")
scene("And notice who never sees this fee. You. It's built into the store's prices. So everyone pays it, even people paying with cash.",
      type="equation", title="Who really pays the swipe fee",
      lines=[{"text": "Swipe fee", "color": "gold", "size": 96},
             {"text": "→ built into prices", "color": "text", "size": 84},
             {"text": "→ everyone pays, even cash users", "color": "muted", "size": 60}])

# ---------------------------------------------------------------- 3
scene("Chapter three. The interest engine.", type="chapter", n=3, title="The interest engine")
scene("Swipe fees are steady money. But for the banks, the real engine is interest. The Federal Reserve says the average rate on cards that actually charged interest was twenty-two point three six percent in the third quarter of twenty twenty-six.",
      type="photo", file="assets/photos/federal_reserve_building.jpg", layout="side", focus=[0.5, 0.45],
      value=f"{APR * 100:.2f}%", label="average rate on cards charged interest", color="red",
      sub="Q3 2026 (preliminary) · Federal Reserve G.19")
scene("That rate jumped fast. In twenty twenty-one it was about sixteen and a half percent. Within two years it passed twenty-two, and it has stayed there.",
      type="line", title="Average card rate when interest is charged (%)", format="num",
      x=list(APR_HIST), series=[{"label": "22.36%", "values": list(APR_HIST.values()), "color": "red"}])
scene("Here's what that means. Carry a five thousand dollar balance for a year at that rate, and you'd pay about eleven hundred dollars in interest. That's roughly three dollars, every single day.",
      type="equation", title="$5,000 balance kept for a year",
      lines=[{"text": f"$5,000 × {APR * 100:.2f}%", "color": "muted", "size": 84},
             {"text": f"= ${interest_5k:,.0f} a year", "color": "red", "size": 120},
             {"text": f"≈ ${interest_5k / 365:.0f} every day", "color": "text", "size": 60}])
scene("Across the country, interest charges hit one hundred and sixty billion dollars in twenty twenty-four. That's up fifty-two percent in just two years, while the number of cardholders grew less than ten percent.",
      type="columns", title="Interest charged to US cardholders", highlight=1,
      items=[{"label": "2022", "value": INTEREST_22, "display": "$105B", "color": "slate"},
             {"label": "2024", "value": INTEREST_24, "display": "$160B", "color": "red"}],
      note="Source: CFPB credit card market report, Dec 2025")
scene("Now look inside a big card bank. In twenty twenty-four, Capital One's credit card business brought in twenty-eight point two billion dollars. Almost four out of every five of those dollars came from interest, after its own borrowing costs.",
      type="donut", title="Capital One card business revenue, 2024",
      segments=[{"label": "Interest (net)", "value": C_NII, "color": "red"},
                {"label": "Swipe fees & other", "value": C_NONII, "color": "blue"}],
      center="$28.2B", center_sub="card revenue")
scene("Why so much? Because about half of all card accounts carry a balance from month to month. And about fifteen percent of cardholders pay only the minimum, the highest share since at least twenty fifteen.",
      type="share", title="US credit card accounts, 2024",
      rows=[{"label": "Carry a balance month to month", "share": REVOLVE_SHARE, "color": "gold"},
            {"label": "Pay only the minimum", "share": MIN_ONLY_SHARE, "color": "red"}],
      note="Source: CFPB, 2024 data (general purpose cards for minimum payers)")

# ---------------------------------------------------------------- 4
scene("Chapter four. The fees.", type="chapter", n=4, title="The fees")
scene("Interest isn't the only charge. In twenty twenty-four, cardholders paid thirty-one point three billion dollars in fees. Late fees were the biggest piece, at seventeen billion. Annual fees came next, at a record eight point seven billion.",
      type="donut", title="Credit card fees paid in 2024",
      segments=[{"label": "Late fees", "value": LATE_24, "color": "red", "display": "$17B"},
                {"label": "Annual fees", "value": ANNUAL_24, "color": "gold", "display": "$8.7B"},
                {"label": "Other fees", "value": OTHER_FEES_24, "color": "blue", "display": "$5.6B"}],
      center="$31.3B", center_sub="total fees · CFPB")
scene("And late fees don't land evenly. People with the lowest credit scores hold about fourteen percent of card accounts, but pay forty percent of all late fees. People with the best scores hold fifty-nine percent of accounts, and pay under eight percent.",
      type="table", title="Who pays the late fees (2024)",
      header=["Credit score", "Accounts", "Late fees"],
      rows=[["Lowest scores", f"{DEEP_SUB_ACCTS:.0%}", f"{DEEP_SUB_LATE:.0%}"],
            ["Best scores", f"{TOP_ACCTS:.0%}", f"{TOP_LATE * 100:.1f}%"]],
      highlight_row=0, col_colors={"1": "muted", "2": "red"})
scene("Annual fees work differently. People with excellent credit are the most likely to pay them, usually to unlock premium rewards. The test is simple: a fee is only worth it if the perks you actually use are worth more.",
      type="photo", title="Annual fees", file="assets/photos/card_network_logos_sign.jpg", layout="side",
      focus=[0.5, 0.5], value="$8.7B", color="gold", label="in annual fees, 2024, most on premium cards",
      sub="Worth it only if the perks you really use are worth more than the fee")
scene("So fees fall hardest on people with the weakest credit. Keep that in mind, because the next part is about who benefits.",
      type="quote", text="Fees fall hardest on\nthe weakest credit scores.", first_color="text", color="red",
      source="CFPB: lowest scores, 14% of accounts, 40% of late fees")

# ---------------------------------------------------------------- 5
scene("Chapter five. Who pays for rewards?", type="chapter", n=5, title="Who pays for rewards?")
scene("Here's the part everyone loves. In twenty twenty-four, cardholders earned forty-seven and a half billion dollars in rewards. Cash back, points and miles.",
      type="count", to=47.5, prefix="$", suffix="B", dp=1, label="in card rewards earned", sub="2024 · CFPB", color="green")
scene("But put that next to what cardholders paid. One hundred and sixty billion in interest, plus thirty-one billion in fees. Rewards are only about a quarter of that.",
      type="columns", title="US cardholders, 2024",
      items=[{"label": "Interest paid", "value": INTEREST_24, "display": "$160B", "color": "red"},
             {"label": "Fees paid", "value": FEES_24, "display": "$31.3B", "color": "gold"},
             {"label": "Rewards earned", "value": REWARDS_24, "display": "$47.5B", "color": "green"}],
      note="Source: CFPB credit card market report, Dec 2025")
scene("So where does the reward money come from? Largely from swipe fees. Capital One's rewards cost nine billion dollars in twenty twenty-four, and it subtracts that straight from its swipe fee income. About two of every three swipe fee dollars went back out as rewards.",
      type="waterfall", title="Capital One swipe-fee income, 2024",
      steps=[{"label": "Swipe fees", "value": c_ix_gross, "kind": "start", "display": f"${c_ix_gross / 1e9:.1f}B"},
             {"label": "Rewards", "value": C_REWARDS, "kind": "minus", "display": "−$9.0B"},
             {"label": "Kept", "value": C_IX_NET, "kind": "total", "display": f"${C_IX_NET / 1e9:.1f}B"}])
scene("And it becomes a loop. Rewards make people use their cards more. More spending means more swipe fees, and for some people, bigger balances. The interest and fees on those balances help fund even richer rewards.",
      type="flywheel", title="The rewards loop", center="LOOP",
      steps=["Rewards", "More spending", "Swipe fees", "Bigger balances", "Interest + fees"])
scene("So who collects the rewards? Mostly people with the best credit. In twenty twenty-four, superprime cardholders redeemed eighteen and a half billion dollars of rewards. Below-prime cardholders, under three billion.",
      type="hbars", title="Rewards redeemed by credit score, 2024",
      items=[{"label": k, "value": v, "display": f"${v / 1e9:.1f}B",
              "color": "green" if i < 2 else "slate"} for i, (k, v) in enumerate(REDEEMED.items())])
scene("Together, the two highest credit groups took about four out of every five reward dollars.",
      type="share", title="Share of rewards redeemed, 2024",
      rows=[{"label": "Two best credit-score groups", "share": top2, "color": "green"},
            {"label": "Everyone else", "share": 1 - top2, "color": "slate"}],
      note="Source: CFPB (general purpose cards)")
scene("Economists in a study published by the Federal Reserve looked at this closely. They estimate that rewards cards move about fifteen billion dollars a year from poorer, less educated areas to richer, more educated ones.",
      type="quote", text="About $15 billion a year\nflows from poorer areas\nto richer ones.", first_color="gold", color="text",
      source="Agarwal, Presbitero, Silva & Wix · Federal Reserve FEDS 2023-007")
scene("Cash users chip in too, because most stores charge one price however you pay. A Boston Fed study estimated each household paying cash hands about one hundred and forty-nine dollars a year to card users, while each card-using household gains about eleven hundred.",
      type="versus", title="The hidden transfer at the checkout",
      left={"label": "Cash household", "value": f"−${CASH_PAYS}", "sub": "pays per year", "color": "red"},
      right={"label": "Card household", "value": f"+${CARD_GETS:,}", "sub": "gains per year", "color": "green"},
      verdict="Boston Fed estimate, 2010 study")
scene("That's why critics call rewards a reverse Robin Hood. The money tends to flow from people who carry balances or pay cash, to people who pay in full with premium cards.",
      type="title", title="Reverse Robin Hood", sub="rewards flow from those who pay interest to those who don't", sub_color="gold")

# ---------------------------------------------------------------- 6
scene("Chapter six. The network versus the bank.", type="chapter", n=6, title="Network vs bank")
scene("Now, the network. In its fiscal year ending September twenty twenty-six, Visa brought in forty-five point nine billion dollars of revenue. Its net profit was twenty-three point five billion.",
      type="photo", title="Visa, fiscal 2026", file="assets/photos/visa_hq_san_francisco.jpg", layout="side",
      focus=[0.5, 0.4], value="$45.9B", color="text", label="net revenue",
      sub=f"$23.5B net income · {v_margin * 100:.0f}% net profit margin")
scene("That's about fifty-one cents of profit on every dollar of revenue. For comparison, Costco keeps about three cents.",
      type="columns", title="Net profit per $1 of revenue", highlight=0,
      items=[{"label": "Visa (FY2026)", "value": v_margin * 100, "display": f"{v_margin * 100:.0f}¢", "color": "gold"},
             {"label": "Costco (FY2026)", "value": COSTCO_MARGIN * 100, "display": f"{COSTCO_MARGIN * 100:.0f}¢", "color": "slate"}])
scene("Visa gets there by taking a tiny slice of a huge flow. Over fifteen trillion dollars was paid on Visa cards that year. Its revenue works out to about thirty cents for every hundred dollars.",
      type="stat", value=f"{v_per_100 * 100:.0f}¢", label="Visa revenue per $100 paid on its cards",
      sub="FY2026: $45.9B revenue ÷ $15.3T payments volume", color="green")
scene("Why so profitable? Visa doesn't lend, so it never loses money when someone can't pay. Your bank funds your rewards. Visa runs the network and charges small fees on a giant volume. It even paid eighteen point three billion dollars in incentives to banks and partners to win their business.",
      type="bullets", title="Why the network's margin is so high",
      items=["No loans, so no credit losses", "Your bank funds the rewards", "Small fees on giant volume",
             "Paid $18.3B in client incentives"])
scene("Now compare a card bank. Capital One's card business in twenty twenty-four: twenty-eight point two billion in revenue. Minus ten point three billion set aside for loans that won't be repaid. Minus thirteen point six billion in running costs and marketing. Minus taxes. Left over: three point three billion.",
      type="waterfall", title="Capital One card business, 2024",
      steps=[{"label": "Revenue", "value": C_REV, "kind": "start"},
             {"label": "Credit losses", "value": C_PROV, "kind": "minus"},
             {"label": "Running costs", "value": C_EXP, "kind": "minus"},
             {"label": "Taxes", "value": C_TAX, "kind": "minus", "display": "−$1.0B"},
             {"label": "Net profit", "value": C_NI, "kind": "total"}])
scene("So Visa keeps about fifty-one cents of each revenue dollar. Capital One's card business kept about twelve. The difference is risk. In twenty twenty-four, Capital One wrote off nearly six percent of its card loans.",
      type="versus", title="Profit per $1 of revenue",
      left={"label": "Visa", "value": f"{v_margin * 100:.0f}¢", "sub": "network · FY2026", "color": "gold"},
      right={"label": "Capital One cards", "value": f"{c_margin * 100:.0f}¢", "sub": "lender · 2024", "color": "blue"},
      verdict=f"The lender carries the risk: {C_NCO_RATE * 100:.2f}% of card loans written off")

# ---------------------------------------------------------------- 7
scene("Chapter seven. What it means for you.", type="chapter", n=7, title="What it means for you")
scene("Here's the good news. On most cards, if you pay the full statement balance by the due date, you pay no interest on purchases. And by law, your bill must reach you at least twenty-one days before it's due.",
      type="timeline", title="The interest-free window",
      events=[{"when": "Buy", "text": "Use your card\nas normal"},
              {"when": "Bill", "text": "Statement\narrives"},
              {"when": "21+ days", "text": "Time to pay,\nby law"},
              {"when": "$0", "text": "Pay in full:\nno interest", "color": "gold"}])
scene("Do that, and the math flips in your favor. Say you put a thousand dollars a month on a card with two percent cash back, and pay in full. That's two hundred and forty dollars a year back, and zero interest.",
      type="table", title="$1,000 a month on a 2% cash back card (example)",
      header=["You…", "Rewards", "Interest"],
      rows=[["Pay in full", f"+${rewards_2pct:.0f}", "$0"],
            ["Carry $5,000", f"+${rewards_2pct:.0f}", f"−${interest_5k:,.0f}"]],
      highlight_row=0, col_colors={"1": "green", "2": "red"})
scene("But carry a five thousand dollar balance at today's average rate, and the interest is more than four times the rewards. You'd be about eight hundred and seventy-eight dollars a year behind.",
      type="equation", title="Carrying a balance",
      lines=[{"text": f"+${rewards_2pct:.0f} rewards", "color": "green", "size": 84},
             {"text": f"− ${interest_5k:,.0f} interest", "color": "muted", "size": 84},
             {"text": f"= −${-net_carry:,.0f} a year", "color": "red", "size": 120}])
scene("So, four simple rules. Pay the full statement balance every month. Set up autopay so you're never late. Only pay an annual fee if you'd use the perks anyway. And if you already carry a balance, pay it down before chasing rewards.",
      type="bullets", title="Four rules",
      items=["Pay the full balance, every month", "Autopay: never pay a late fee", "Annual fee only if perks > fee",
             "Carry a balance? Pay it off first"])
scene("Remember who this business makes the most money from: people who pay late and carry balances. Your goal is to be the customer they make the least money from.",
      type="quote", text="Be the customer\nthey make the\nleast money from.", first_color="text", color="gold")
scene("If this changed how you see your wallet, subscribe. We break down how money really works, every week.",
      type="cta", lines=["Follow", "the money."], sub="Subscribe for weekly breakdowns")

for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])

spec = {
    "id": "L004_credit_cards_business", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Figures: NY Fed, Federal Reserve, CFPB, Visa & Capital One filings · education, not financial advice",
    "title": "How Credit Card Companies Really Make Money",
    "intro_chapter": "Intro",
    "thumbnail": {"big": "$160B", "line": "IN CARD INTEREST", "tag": "WHO REALLY PAYS?", "color": "gold",
                  "photo": {"file": "assets/photos/credit_cards_visa_mc_amex.jpg", "focus": [0.5, 0.5]}},
    "description": (
        "How do credit card companies really make money? Americans owe $1.29 trillion on credit cards, and in "
        "2024 card issuers charged $160 billion in interest plus $31.3 billion in fees. We follow the money from "
        "swipe fees (what a store pays on a $100 purchase) to interest, late and annual fees, who really pays "
        "for rewards, and why Visa keeps about 51 cents of profit per revenue dollar while a big card bank keeps "
        "about 12.\n\n"
        "Assumptions: the $5,000 example keeps the balance at $5,000 for a year at the Fed's Q3 2026 average "
        "rate on accounts assessed interest (22.36%), with interest paid monthly (no compounding). The 2% cash "
        "back card is an example, not a specific product. Swipe fees are Visa's published US default rates "
        "(card present, retail); large merchants can negotiate lower, and stores also pay network and "
        "processor fees not shown.\n\n"
        "Sources:\n"
        "- New York Fed, Household Debt and Credit Report, Q3 2026 (Nov 10, 2026): https://www.newyorkfed.org/microeconomics/hhdc\n"
        "- Federal Reserve G.19 Consumer Credit, Nov 6, 2026 release (credit card plans, accounts assessed "
        "interest): https://www.federalreserve.gov/releases/g19/current/\n"
        "- CFPB, The Consumer Credit Card Market report (Dec 30, 2025; 2024 data): "
        "https://www.consumerfinance.gov/data-research/research-reports/the-consumer-credit-card-market-2025/\n"
        "- Visa USA Interchange Reimbursement Fees, effective Oct 24, 2026: "
        "https://usa.visa.com/support/small-business/regulations-fees.html\n"
        "- Visa fiscal 2026 Form 10-K (filed Nov 5, 2026) and Q4 FY2026 results (Oct 27, 2026): https://investor.visa.com\n"
        "- Capital One 2025 Form 10-K (filed Feb 19, 2026), Credit Card business results and rewards note "
        "(2024 figures): https://investor.capitalone.com\n"
        "- Agarwal, Presbitero, Silva & Wix, \"Who Pays For Your Rewards?\", Federal Reserve FEDS 2023-007: "
        "https://www.federalreserve.gov/econres/feds/who-pays-for-your-rewards-redistribution-in-the-credit-card-market.htm\n"
        "- Schuh, Shy & Stavins, \"Who Gains and Who Loses from Credit Card Payments?\", Boston Fed (2010)\n"
        "- Credit CARD Act of 2009 / Regulation Z 12 CFR 1026.5(b)(2)(ii) (21-day rule)\n"
        "- Costco FY2026 results (net income $9.2B on $303.2B revenue)\n\n"
        "For education only. Not financial advice.\n\n"
        "#creditcards #personalfinance #businessbreakdown #creditcarddebt #moneytips"
    ),
    "tags": ["how credit card companies make money", "credit card business model", "interchange fees",
             "swipe fees", "credit card interest", "credit card rewards", "who pays for credit card rewards",
             "visa business model", "credit card late fees", "credit card debt", "business breakdown",
             "personal finance"],
    "localizations": {
        "es": {"title": "Cómo ganan dinero realmente las tarjetas de crédito",
               "summary": "Los estadounidenses deben 1,29 billones de dólares en tarjetas de crédito, y en 2024 los "
                          "bancos cobraron 160.000 millones en intereses y 31.300 millones en comisiones. Seguimos el "
                          "dinero: comisiones por pago, intereses, cargos y quién paga de verdad las recompensas."},
        "pt": {"title": "Como as empresas de cartão de crédito realmente lucram",
               "summary": "Os americanos devem US$ 1,29 trilhão no cartão de crédito, e em 2024 os bancos cobraram "
                          "US$ 160 bilhões em juros e US$ 31,3 bilhões em tarifas. Seguimos o dinheiro: taxas de "
                          "transação, juros, tarifas e quem realmente paga pelas recompensas."},
        "hi": {"title": "क्रेडिट कार्ड कंपनियाँ असल में पैसे कैसे कमाती हैं",
               "summary": "अमेरिकियों पर क्रेडिट कार्ड का 1.29 ट्रिलियन डॉलर बकाया है, और 2024 में बैंकों ने 160 अरब "
                          "डॉलर ब्याज और 31.3 अरब डॉलर फ़ीस वसूली। स्वाइप फ़ीस, ब्याज, लेट फ़ीस और रिवॉर्ड्स का "
                          "असली खर्च कौन उठाता है, यह आसान भाषा में समझिए।"},
        "id": {"title": "Cara Perusahaan Kartu Kredit Benar-benar Untung",
               "summary": "Warga AS berutang US$1,29 triliun di kartu kredit, dan pada 2024 bank menagih US$160 miliar "
                          "bunga plus US$31,3 miliar biaya. Kita telusuri uangnya: biaya gesek, bunga, denda, dan "
                          "siapa yang sebenarnya membayar hadiah kartu."},
        "de": {"title": "Wie Kreditkartenfirmen wirklich Geld verdienen",
               "summary": "Amerikaner schulden 1,29 Billionen Dollar auf Kreditkarten, und 2024 berechneten Banken 160 "
                          "Milliarden Dollar Zinsen plus 31,3 Milliarden Gebühren. Wir folgen dem Geld: "
                          "Händlergebühren, Zinsen, Gebühren und wer Prämien wirklich bezahlt."},
        "fr": {"title": "Comment les cartes de crédit gagnent vraiment de l'argent",
               "summary": "Les Américains doivent 1 290 milliards de dollars sur leurs cartes de crédit, et en 2024 les "
                          "banques ont facturé 160 milliards d'intérêts et 31,3 milliards de frais. Suivons l'argent : "
                          "commissions, intérêts, frais et qui paie vraiment les récompenses."},
    },
    "scenes": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L004_credit_cards_business.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", sum(len(s["say"].split()) for s in S), "words")
