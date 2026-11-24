"""Long-form L005: Airlines barely make money flying. Here's what pays.

Sources (checked 2026-11-22):
  [I]  IATA press release "Middle East disruptions, high fuel prices halve airline industry profitability"
       (7 June 2026) + IATA "Industry Statistics" fact sheet (updated 6/2026, next update 12/2026).
       2025 = estimate, 2026 = forecast. Historical data subject to revision (2020 loss now $137.7B;
       IATA's Aug 2021 first count was $126.4B).
  [C]  IATA Chart of the Week "Profits and Margins to Shrink in 2026 - but Remain Positive" (19 June 2026):
       "the industry has never posted a net profit margin higher than 5%".
  [B]  US Bureau of Transportation Statistics release "US Airlines gained $6.0 billion in 2025, a decrease
       over 2024" (May 12, 2026): scheduled passenger airlines, systemwide.
  [D]  Delta Air Lines December quarter and full-year 2025 results (Jan 13, 2026).
  [A]  American Airlines Group 2025 Form 10-K (Feb 2026) + Q4/FY2025 earnings release (Jan 27, 2026)
       (same figures as Short 022).
  [U1] United Airlines Holdings Form 8-K (report date June 12, 2020, signed June 15, 2020): "Multiplying MPH
       2019 EBITDA by a factor of 12 equates to a MileagePlus valuation of approximately $21.9 billion."
  [U2] Exhibit 99.1 to that 8-K (MileagePlus investor presentation, June 15, 2020): "$1.8 billion & 34%
       2019 EBITDA and margin"; "~$5.3B cash flows from sales in 2019"; "Over 100 million total members".
  [U3] United press release, July 2, 2020: $3.8B 6.50% MileagePlus senior secured notes + $3.0B term loan.
  [W]  Berkshire Hathaway 2007 shareholder letter (published Feb 2008), verbatim from the PDF.
  Break-even load factor: IATA doesn't publish it in the public release/fact sheet, so the per-flight
  example below is our own rough illustration from IATA's 2026 averages (said as such on screen).
"""
import json, os

# ---- [I] global industry, USD
REV_26, EXP_26, EBIT_26, NET_26 = 1165e9, 1117e9, 48.0e9, 23.0e9
NET_25 = 45.0e9
FUEL_26, FUEL_25, FUEL_SHARE_26 = 350e9, 252e9, 0.314
LABOR_26, LABOR_SHARE_26 = 271e9, 0.242
NONFUEL_26 = 767e9
PAX_26 = 5085e6                 # segment passengers
PER_PAX_26 = 4.5                # net profit per departing passenger, $
LF_26 = 0.84                    # passenger load factor (record)
PAX_REV_26, ANC_26, CARGO_26 = 839e9, 165e9, 162e9
NET_MARGIN = {2019: 0.031, 2023: 0.043, 2024: 0.037, 2025: 0.042, 2026: 0.020}
NET_PROFIT = {2020: -137.7e9, 2021: -40.4e9, 2022: -3.5e9, 2023: 40.5e9, 2024: 37.7e9, 2025: 45.0e9, 2026: 23.0e9}
PER_PAX_2020 = -77.4
CARGO_REV = {2019: 101, 2020: 140, 2021: 210, 2022: 206, 2023: 139, 2024: 147, 2025: 151, 2026: 162}  # $B
EBITDAR_MARGIN_2019 = 0.182
# ---- [C]
MAX_NET_MARGIN_EVER = 0.05
# ---- [B] US scheduled passenger airlines, 2025
US_NET_25, US_OPREV_25, US_BAGS_25, US_CHANGE_25 = 6.0e9, 252.6e9, 7.4e9, 1.1e9
# ---- [D] Delta FY2025, $
DAL_AMEX, DAL_REV, DAL_PRETAX = 8.2e9, 63.364e9, 6.185e9
DAL_PREMIUM = {2024: 20.599e9, 2025: 22.097e9}
DAL_MAIN = {2024: 24.497e9, 2025: 23.391e9}
# ---- [A] American FY2025
AAL_PARTNER_CASH, AAL_NET = 6.2e9, 111e6
# ---- [U1-U3] United MileagePlus
MP_VALUE, MP_EBITDA_2019, MP_MARGIN_2019, MP_MULT = 21.9e9, 1.8e9, 0.34, 12
MP_NOTES, MP_LOAN = 3.8e9, 3.0e9

# ---- derived numbers (every spoken one is asserted)
assert abs(EXP_26 - FUEL_26 - NONFUEL_26) < 1e9 and abs(REV_26 - EXP_26 - EBIT_26) < 1e9   # release ties out
other_26 = NONFUEL_26 - LABOR_26
margin_26 = NET_26 / REV_26
rev_per_pax = REV_26 / PAX_26
fuel_labor = FUEL_SHARE_26 + LABOR_SHARE_26
other_share = 1 - fuel_labor
fuel_jump = FUEL_26 / FUEL_25 - 1
assert 1.16e12 < REV_26 < 1.17e12                  # "one point one seven trillion"
assert 0.0195 < margin_26 < 0.0205                 # "two percent"
assert abs(NET_26 / PAX_26 - PER_PAX_26) < 0.05    # "four dollars and fifty cents"
assert 228.5 < rev_per_pax < 229.5                 # "two hundred and twenty-nine dollars"
assert 0.0195 < PER_PAX_26 / rev_per_pax < 0.0200  # "about two cents of every dollar"
assert fuel_labor > 0.5                            # "more than half"
assert abs(other_26 - 496e9) < 1e9                 # "everything else" in the waterfall
assert 0.38 < fuel_jump < 0.40                     # "nearly forty percent"
assert 0.5 < NET_26 / NET_25 < 0.52                # "roughly in half"
assert max(NET_MARGIN.values()) < MAX_NET_MARGIN_EVER

# per-flight illustration (our example, built from IATA 2026 averages)
SEATS = 180
pax = round(SEATS * LF_26)
flight_rev = pax * rev_per_pax
flight_profit = pax * PER_PAX_26
breakeven_pax = pax - flight_profit / rev_per_pax
assert pax == 151                                  # "about a hundred and fifty-one passengers"
assert 34_500 < flight_rev < 34_700                # "about thirty-four thousand six hundred dollars"
assert 675 < flight_profit < 685                   # "about six hundred and eighty"
assert 3 * rev_per_pax > flight_profit             # "lose three passengers ... the profit with it"
assert 685 < 3 * rev_per_pax < 690                 # "about six hundred and ninety dollars"
assert 147.5 < breakeven_pax < 148.5               # "about a hundred and forty-eight passengers"
assert 0.815 < 148 / SEATS < 0.825                 # "about eighty-two percent full"

# shocks
lost_20_22 = -(NET_PROFIT[2020] + NET_PROFIT[2021] + NET_PROFIT[2022])
made_23_26 = NET_PROFIT[2023] + NET_PROFIT[2024] + NET_PROFIT[2025] + NET_PROFIT[2026]
assert 181e9 < lost_20_22 < 182e9                  # "about a hundred and eighty-two billion"
assert 146e9 < made_23_26 < 146.5e9                # "about a hundred and forty-six billion"
assert made_23_26 < lost_20_22                     # "still not enough to win it back"

# loyalty
aal_ratio = AAL_PARTNER_CASH / AAL_NET
amex_share = DAL_AMEX / DAL_REV
assert 55 < aal_ratio < 57                         # "about fifty-six times"
assert DAL_AMEX > DAL_PRETAX                       # "more than Delta's entire pre-tax profit"
assert abs(amex_share - 1 / 8) < 0.01              # "about one in every eight dollars"
assert abs(MP_EBITDA_2019 * MP_MULT - MP_VALUE) / MP_VALUE < 0.02   # 1.8B x 12 "about" 21.9B (1.8 is rounded)
assert MP_NOTES + MP_LOAN == 6.8e9                 # "six point eight billion"
assert MP_MARGIN_2019 > EBITDAR_MARGIN_2019        # generous comparison still favours miles

# fees, premium, cargo
assert US_BAGS_25 > US_NET_25                      # bags > whole US industry's after-tax profit
assert abs(US_BAGS_25 / US_OPREV_25 - 0.029) < 0.001
assert ANC_26 > CARGO_26                           # "more than air cargo"
prem_g = DAL_PREMIUM[2025] / DAL_PREMIUM[2024] - 1
main_g = DAL_MAIN[2025] / DAL_MAIN[2024] - 1
assert 0.07 < prem_g < 0.075 and -0.05 < main_g < -0.04   # "grew seven percent" / "fell five percent"
ticket_share = PAX_REV_26 / (PAX_REV_26 + ANC_26 + CARGO_26)
assert 0.715 < ticket_share < 0.725                # "about seventy-two cents of every dollar"
assert abs(CARGO_REV[2021] / CARGO_REV[2019] - 2) < 0.1   # "about doubled"

# traveller maths (hypothetical examples, labelled on screen)
FARE, MILES, MILES_NEW = 250, 25_000, 35_000
cpm, cpm_new = FARE / MILES * 100, FARE / MILES_NEW * 100     # cents per mile
loss = 1 - cpm_new / cpm
assert cpm == 1.0 and 0.71 < cpm_new < 0.72        # "one cent" / "about seven tenths of a cent"
assert 0.28 < loss < 0.29                          # "almost thirty percent"
CARD_FEE = 95
assert round(CARD_FEE / (cpm / 100)) == 9500        # "nine thousand five hundred dollars"
BAL, APR = 2000, 0.20
assert BAL * APR == 400 and BAL * cpm / 100 == 20  # "four hundred" vs "twenty"
print(f"margin {margin_26:.2%} rev/pax ${rev_per_pax:.0f} fuel+labor {fuel_labor:.1%} flight rev ${flight_rev:,.0f} "
      f"profit ${flight_profit:.0f} BE pax {breakeven_pax:.1f} lost {lost_20_22/1e9:.1f}B made {made_23_26/1e9:.1f}B "
      f"AAL x{aal_ratio:.0f} amex {amex_share:.1%} tickets {ticket_share:.1%}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook (retention: payoff in the first 10 s,
# then the promise, then a tease of the best reveal, which pays off in chapter 3: Delta / American Express)
scene("Four dollars and fifty cents. That's all the world's airlines are expected to keep per passenger this year, after every cost.",
      type="stat", value="$4.50", label="net profit per passenger, 2026",
      sub="forecast · International Air Transport Association (IATA)", color="gold")
scene("Meanwhile, each passenger brings in about two hundred and twenty-nine dollars. About two cents of every dollar is profit.",
      type="versus", title="The average passenger, 2026",
      left={"label": "Revenue", "value": f"${rev_per_pax:.0f}", "sub": "all sources, per passenger", "color": "blue"},
      right={"label": "Net profit", "value": "$4.50", "sub": "what the airline keeps", "color": "gold"},
      verdict="About 2 cents of every dollar")
scene("So if flying barely pays, what does? The answer is hiding in your wallet, your suitcase, and the front of the plane.",
      type="title", title="What Really Pays", sub="how airlines actually make money")
scene("Here's what you'll learn. Why one flight sits just three seats from a loss. The hidden money machine behind airlines. And how to get more from your own miles.",
      type="bullets", title="What you'll learn",
      items=["Why one flight is 3 seats from a loss", "The hidden money machine", "How to get more from your miles"])
scene("And by the end, you'll see why one credit card company paid an airline more than that airline's entire profit before tax.",
      type="equation", title="Coming up",
      lines=[{"text": "One credit card deal", "color": "text", "size": 96},
             {"text": ">", "color": "muted", "size": 90},
             {"text": "an airline's entire profit", "color": "gold", "size": 96}])

# ---------------------------------------------------------------- 1
scene("Chapter one. The brutal math of flying.", type="chapter", n=1, title="The brutal math")
scene("The International Air Transport Association expects airlines to bring in about one point one seven trillion dollars this year. Net profit? Just twenty-three billion. A margin of two percent.",
      type="stat_grid", title="Global airlines, 2026 forecast",
      items=[{"value": "$1.17T", "label": "revenue", "color": "text"},
             {"value": "$23B", "label": "net profit", "color": "gold"},
             {"value": f"{margin_26 * 100:.1f}%", "label": "net margin", "color": "red"}])
scene("And that isn't bad luck. The association itself says the industry has never posted a net profit margin higher than five percent.",
      type="quote", text="\"Never posted a net profit\nmargin higher than 5%\"", first_color="text", color="gold",
      source="IATA, Chart of the Week, 19 June 2026")
scene("Look at the good years. Three point one percent in twenty nineteen. Around four percent from twenty twenty-three to twenty twenty-five. And about two percent forecast for this year.",
      type="columns", title="Airline industry net profit margin", highlight=4,
      items=[{"label": f"{y}{'*' if y >= 2025 else ''}", "value": m * 100, "display": f"{m * 100:.1f}%"}
             for y, m in NET_MARGIN.items()],
      note="Source: IATA industry statistics, June 2026 · *2025 estimate, 2026 forecast")
scene("So where does the money go? Fuel is the biggest cost, about thirty-one percent of everything airlines spend this year. Staff come next, about twenty-four percent. Together, more than half.",
      type="donut", title="Where airline costs go, 2026",
      segments=[{"label": "Fuel", "value": FUEL_SHARE_26, "color": "red", "display": "31.4%"},
                {"label": "Staff", "value": LABOR_SHARE_26, "color": "gold", "display": "24.2%"},
                {"label": "Everything else", "value": other_share, "color": "slate", "display": f"{other_share * 100:.1f}%"}],
      center="$1.12T", center_sub="total costs")
scene("Follow one year of money. Start with one point one seven trillion of revenue. Take out fuel. Take out wages. Take out planes, airports, maintenance and everything else. Before interest and tax, forty-eight billion dollars is left.",
      type="waterfall", title="Global airlines 2026: profit before interest & tax",
      steps=[{"label": "Revenue", "value": REV_26, "kind": "start", "display": "$1.17T"},
             {"label": "Fuel", "value": FUEL_26, "kind": "minus", "display": "−$350B"},
             {"label": "Staff", "value": LABOR_26, "kind": "minus", "display": "−$271B"},
             {"label": "Other costs", "value": other_26, "kind": "minus", "display": "−$496B"},
             {"label": "Left over", "value": EBIT_26, "kind": "total", "display": "$48B"}])
scene("And it's not because planes fly empty. This year, airlines are expected to fill eighty-four percent of all their seats. That's a record.",
      type="share", title="Seats filled (passenger load factor)",
      rows=[{"label": "Global airlines, 2026 forecast", "share": LF_26, "color": "green", "dp": 0}],
      note="Source: IATA, June 2026")
scene("Here's a rough example using those industry averages. Take a plane with one hundred and eighty seats, eighty-four percent full. That's about a hundred and fifty-one passengers.",
      type="equation", title="One flight (illustration)",
      lines=[{"text": "180 seats × 84% full", "color": "muted", "size": 90},
             {"text": "↓", "color": "dim", "size": 80},
             {"text": f"≈ {pax} passengers", "color": "text", "size": 120}])
scene("At two hundred and twenty-nine dollars each, they bring in about thirty-four thousand six hundred dollars. At four fifty each, the airline keeps about six hundred and eighty.",
      type="stat_grid", title="One flight at industry averages",
      items=[{"value": str(pax), "label": "passengers", "color": "text"},
             {"value": f"${flight_rev / 1e3:.1f}K", "label": "revenue", "color": "blue"},
             {"value": f"${flight_profit:.0f}", "label": "profit", "color": "gold"}])
scene("Now lose just three passengers. The plane still flies the same route, with the same crew, burning nearly the same fuel. That's about six hundred and ninety dollars of revenue gone, and the profit goes with it.",
      type="table", title="Three empty seats later",
      header=["Passengers", "Seats full", "Profit"],
      rows=[[str(pax), f"{pax / SEATS * 100:.0f}%", f"≈ ${flight_profit:.0f}"], ["148", f"{148 / SEATS * 100:.0f}%", "≈ $0"]],
      highlight_row=1, col_colors={"2": "green"})
scene("In this simple example, the break-even point is about a hundred and forty-eight passengers, roughly eighty-two percent full. Airlines fly just a few seats away from a loss. So why can't they fix that?",
      type="stat", value="3 seats", label="between profit and loss", sub="illustration using 2026 industry averages", color="red")

# ---------------------------------------------------------------- 2
scene("Chapter two. Why it's so hard.", type="chapter", n=2, title="Why it's so hard")
scene("Why is this business so tough? An empty seat can't be saved for later. Once the door closes, it's worth nothing. Most costs are fixed. Rivals can add seats on your route fast. And shocks hit everyone at once.",
      type="bullets", title="Four reasons flying barely pays", color="red",
      items=["Empty seats expire at take-off", "Most costs are fixed", "Rivals add seats fast", "Shocks hit everyone at once"])
scene("That creates a trap. Airlines buy planes to grow. More seats push fares down. Thin profits leave little cushion. And when times are good, everyone adds seats again.",
      type="flywheel", title="The airline trap", center="TRAP",
      steps=["Buy planes", "Add seats", "Fares fall", "Thin profits"])
scene("Take this year. War in the Middle East pushed the industry's fuel bill up nearly forty percent, from two hundred and fifty-two billion dollars to three hundred and fifty billion.",
      type="columns", title="Global airline fuel bill", highlight=1,
      items=[{"label": "2025", "value": FUEL_25, "display": "$252B"},
             {"label": "2026 forecast", "value": FUEL_26, "display": "$350B", "color": "red"}],
      note="Source: IATA, June 2026")
scene("That's expected to cut the industry's profit roughly in half, from forty-five billion to twenty-three.",
      type="hbars", title="Global airline net profit",
      items=[{"label": "2025 estimate", "value": NET_25, "display": "$45B", "color": "slate"},
             {"label": "2026 forecast", "value": NET_26, "display": "$23B", "color": "red"}])
scene("But nothing compares to twenty twenty. When the pandemic grounded the world, airlines lost about one hundred and thirty-eight billion dollars in a single year.",
      type="count", to=-NET_PROFIT[2020] / 1e9, prefix="−$", suffix="B", dp=1, label="global airline net loss, 2020",
      sub="IATA industry statistics", color="red")
scene("That's about seventy-seven dollars lost on every passenger who flew.",
      type="stat", value=f"−${-PER_PAX_2020:.0f}", label="lost per passenger, 2020", sub="IATA", color="red")
scene("And the losses kept coming. Forty billion more in twenty twenty-one, and three and a half billion in twenty twenty-two.",
      type="table", title="Global airline net result",
      header=["Year", "Net result"],
      rows=[[str(y), f"−${-NET_PROFIT[y] / 1e9:.1f}B"] for y in (2020, 2021, 2022)],
      col_colors={"1": "red"})
scene("Add it up. From twenty twenty to twenty twenty-two, the industry lost about a hundred and eighty-two billion dollars. Its profits since then, including this year's forecast, add up to about a hundred and forty-six billion. Still not enough to win it back. So how do airlines keep going? Follow the miles.",
      type="versus", title="Have airlines earned it back?",
      left={"label": "Lost, 2020–22", "value": f"−${lost_20_22 / 1e9:.0f}B", "sub": "pandemic years", "color": "red"},
      right={"label": "Earned, 2023–26", "value": f"${made_23_26 / 1e9:.0f}B", "sub": "incl. 2025 est. & 2026 forecast", "color": "green"},
      verdict="Not yet")

# ---------------------------------------------------------------- 3
scene("Chapter three. The miles machine.", type="chapter", n=3, title="The miles machine")
scene("So where does the real money come from? Start with miles. Airlines sell miles to banks. Banks hand them to you as credit card rewards. And you redeem them for a seat, later.",
      type="equation", title="How the miles machine works",
      lines=[{"text": "Airline sells miles to a bank", "color": "text", "size": 76},
             {"text": "Bank gives them to you", "color": "gold", "size": 76},
             {"text": "You claim a seat later", "color": "green", "size": 76}])
scene("Take American Airlines. In twenty twenty-five, it made a net profit of just one hundred and eleven million dollars. Its credit card and other partners paid it six point two billion in cash. About fifty-six times more.",
      type="columns", title="American Airlines, 2025",
      items=[{"label": "Net profit", "value": AAL_NET, "display": "$111M", "color": "slate"},
             {"label": "Cash from card & other partners", "value": AAL_PARTNER_CASH, "display": "$6.2B", "color": "gold"}],
      note="Source: American Airlines 2025 10-K · partner cash is revenue, not profit")
scene("At Delta, American Express alone paid eight point two billion dollars last year. That's more than Delta's entire pre-tax profit of six point two billion.",
      type="versus", title="Delta, 2025",
      left={"label": "Paid by American Express", "value": "$8.2B", "sub": "card partnership", "color": "gold"},
      right={"label": "Delta's pre-tax profit", "value": "$6.2B", "sub": "the whole airline", "color": "blue"},
      verdict="The card deal beats the whole airline's profit")
scene("It works out to about one in every eight dollars Delta brought in.",
      type="share", title="American Express payments as a share of Delta's revenue",
      rows=[{"label": "Delta, 2025", "share": amex_share, "color": "gold", "dp": 0}],
      note="Source: Delta full-year 2025 results")
scene("Why do airlines love this? The bank pays cash today, and the seat is only provided later. The airline decides how many miles a seat costs. And some miles are never used at all.",
      type="bullets", title="Why miles are a great business",
      items=["Cash today, seat later", "The airline sets the price", "Some miles never get used", "Members stay loyal"])
scene("How valuable is this? In twenty twenty, with planes grounded, United needed cash. So it borrowed six point eight billion dollars, backed by its loyalty program, Mileage Plus.",
      type="stat", value="$6.8B", label="borrowed against MileagePlus, July 2020",
      sub="$3.8B of bonds + a $3.0B loan · United press release", color="gold")
scene("In its filing, United valued Mileage Plus at about twenty-one point nine billion dollars. That was roughly twelve times the program's twenty nineteen cash earnings of about one point eight billion.",
      type="equation", title="United's own math (2020 SEC filing)",
      lines=[{"text": "≈ $1.8B cash earnings (2019)", "color": "muted", "size": 80},
             {"text": "× 12", "color": "dim", "size": 80},
             {"text": "≈ $21.9B", "color": "gold", "size": 130}])
scene("And look at the margin. Mileage Plus kept about thirty-four cents of cash earnings from every dollar. The airline industry as a whole managed about eighteen, even on a measure that flatters the airlines.",
      type="share", title="Cash earnings per $1 of revenue, 2019",
      rows=[{"label": "United MileagePlus", "share": MP_MARGIN_2019, "color": "gold", "dp": 0},
            {"label": "Global airline industry", "share": EBITDAR_MARGIN_2019, "color": "slate", "dp": 0}],
      note="MileagePlus EBITDA margin (United) vs industry EBITDAR margin (IATA)")
scene("In other words, a big part of an airline's value isn't the planes. It's the miles. And miles aren't the only hidden money maker.",
      type="quote", text="Not just an airline.\nA miles business.", first_color="text", color="gold")

# ---------------------------------------------------------------- 4
scene("Chapter four. Bags, front seats, and freight.", type="chapter", n=4, title="Bags, seats & freight")
scene("Next, fees. In twenty twenty-five, US airlines collected seven point four billion dollars in baggage fees, according to the US Bureau of Transportation Statistics.",
      type="stat", value="$7.4B", label="US airline baggage fees, 2025",
      sub="US Bureau of Transportation Statistics, May 2026", color="gold")
scene("Compare that with what those same airlines earned in total after tax: six billion. Fees aren't pure profit, but bags alone brought in more than the whole industry's profit. Change fees added another one point one billion.",
      type="columns", title="US airlines, 2025",
      items=[{"label": "Baggage fees", "value": US_BAGS_25, "display": "$7.4B", "color": "gold"},
             {"label": "Change fees", "value": US_CHANGE_25, "display": "$1.1B", "color": "gold"},
             {"label": "Net profit (after tax)", "value": US_NET_25, "display": "$6.0B", "color": "slate"}],
      note="Source: US Bureau of Transportation Statistics · fees are revenue, not profit")
scene("Worldwide, fees and other extras are expected to bring in a hundred and sixty-five billion dollars this year. For the first time since twenty nineteen, that's more than air cargo.",
      type="stat_grid", title="Global airlines, 2026 forecast",
      items=[{"value": "$165B", "label": "fees & other extras", "sub": "bags, seats, upgrades and more", "color": "gold"},
             {"value": "$162B", "label": "air cargo", "color": "blue"}])
scene("Then there's the front of the plane. At Delta, premium cabin ticket revenue grew seven percent last year, to about twenty-two point one billion dollars. Main cabin fell five percent.",
      type="table", title="Delta ticket revenue",
      header=["Cabin", "2024", "2025", "Change"],
      rows=[["Premium", f"${DAL_PREMIUM[2024] / 1e9:.1f}B", f"${DAL_PREMIUM[2025] / 1e9:.1f}B", f"+{prem_g * 100:.0f}%"],
            ["Main cabin", f"${DAL_MAIN[2024] / 1e9:.1f}B", f"${DAL_MAIN[2025] / 1e9:.1f}B", f"−{-main_g * 100:.0f}%"]],
      highlight_row=0)
scene("Premium cabins now bring in almost as much as the main cabin, even though they hold far fewer seats.",
      type="hbars", title="Delta ticket revenue, 2025",
      items=[{"label": "Main cabin", "value": DAL_MAIN[2025], "display": "$23.4B", "color": "slate"},
             {"label": "Premium", "value": DAL_PREMIUM[2025], "display": "$22.1B", "color": "gold"}])
scene("Why chase premium flyers? They tend to care more about comfort and flexibility than price. And they're often the most loyal members, the ones with the airline's credit card.",
      type="bullets", title="Why airlines chase the front cabin",
      items=["Less focused on price", "Pay for comfort & flexibility", "Often the most loyal members"])
scene("Finally, the belly of the plane. Cargo brought the industry about a hundred and one billion dollars in twenty nineteen. When passenger flights stopped in the pandemic, freight prices soared, and cargo hit two hundred and ten billion in twenty twenty-one.",
      type="line", title="Global air cargo revenue ($ billions)", format="num",
      x=list(CARGO_REV), series=[{"label": "Cargo", "values": list(CARGO_REV.values()), "color": "blue"}])
scene("This year, cargo is expected to bring in a hundred and sixty-two billion. Put it all together, and only about seventy-two cents of every dollar airlines earn comes from passenger tickets. So would you want to own an airline? Warren Buffett has an answer.",
      type="donut", title="Where airline revenue comes from, 2026",
      segments=[{"label": "Passenger tickets", "value": PAX_REV_26, "color": "slate", "display": f"{ticket_share * 100:.0f}%"},
                {"label": "Fees & other extras", "value": ANC_26, "color": "gold"},
                {"label": "Cargo", "value": CARGO_26, "color": "blue"}],
      center="$1.17T", center_sub="2026 forecast")

# ---------------------------------------------------------------- 5
scene("Chapter five. Buffett's warning.", type="chapter", n=5, title="Buffett's warning")
scene("Warren Buffett put it bluntly. In his letter to shareholders for twenty oh seven, he wrote that the worst sort of business is one that grows rapidly, requires significant capital to engender the growth, and then earns little or no money. Think airlines.",
      type="quote", text="\"The worst sort of business ...\nThink airlines.\"", first_color="text", color="gold",
      source="Warren Buffett, Berkshire Hathaway 2007 letter")
scene("Airlines tick every box. They grow fast. They need enormous sums for planes. And they keep very little of what they earn.",
      type="bullets", title="Buffett's \"worst sort of business\"",
      items=["Grows rapidly", "Needs significant capital", "Earns little or no money"])
scene("Then came his most famous line. If a farsighted capitalist had been present at Kitty Hawk, where the Wright brothers first flew, he would have done his successors a huge favor by shooting Orville down.",
      type="quote", text="\"...a huge favor by\nshooting Orville down.\"", first_color="text", color="gold",
      source="Warren Buffett on Kitty Hawk, Berkshire Hathaway 2007 letter")
scene("He spoke from experience. In nineteen eighty-nine, Berkshire bought U.S. Air preferred stock. Soon after, the airline went into a tailspin and stopped paying the dividend. Berkshire got lucky and sold in nineteen ninety-eight at a hefty gain. In the decade after that sale, the airline went bankrupt. Twice.",
      type="timeline", title="Buffett and US Air",
      events=[{"when": "1989", "text": "Berkshire buys\nUS Air preferred"},
              {"when": "Soon after", "text": "Dividend\nstops", "color": "red"},
              {"when": "1998", "text": "Sold at a\nhefty gain", "color": "gold"},
              {"when": "Next decade", "text": "Airline goes\nbankrupt twice", "color": "red"}])
scene("The lesson isn't that airlines are useless. They connect the world. It's that a huge, popular business can still be a poor one for the people who own it. And you're part of this machine too, every time you swipe.",
      type="equation", title="The lesson",
      lines=[{"text": "Huge & popular", "color": "text", "size": 100},
             {"text": "isn't always a", "color": "muted", "size": 64},
             {"text": "good business", "color": "gold", "size": 110}])

# ---------------------------------------------------------------- 6
scene("Chapter six. What it means for you.", type="chapter", n=6, title="What it means for you")
scene("First, know what a mile is worth. Here's a simple example. If a flight costs two hundred and fifty dollars, or twenty-five thousand miles, each mile is worth one cent.",
      type="equation", title="What is a mile worth? (example)",
      lines=[{"text": "$250 ÷ 25,000 miles", "color": "muted", "size": 96},
             {"text": "↓", "color": "dim", "size": 80},
             {"text": "= 1¢ per mile", "color": "gold", "size": 130}])
scene("Now say the airline raises that seat to thirty-five thousand miles. Same seat. Your miles are now worth about seven tenths of a cent each. You just lost almost thirty percent of their value, and nobody asked you.",
      type="columns", title="Value of one mile, same $250 seat (example)",
      items=[{"label": "25,000 miles", "value": cpm, "display": f"{cpm:.1f}¢", "color": "green"},
             {"label": "35,000 miles", "value": cpm_new, "display": f"{cpm_new:.2f}¢", "color": "red"}],
      note=f"−{loss * 100:.0f}% value, with no change to your balance")
scene("Miles are a currency printed by the airline, and it can change their value at any time. So don't hoard them. Earn them, then spend them on something you actually want.",
      type="bullets", title="Treat miles like this",
      items=["The airline's own currency", "It can change their value", "Earn and spend, don't hoard"])
scene("Second, card rewards aren't free. Say a card charges ninety-five dollars a year and earns one mile per dollar. At one cent a mile, you'd need to spend nine thousand five hundred dollars a year just to cover the fee.",
      type="stat", value="$9,500", label="yearly spending just to cover a $95 fee",
      sub="example: 1 mile per $1, miles worth 1¢", color="gold")
scene("And if you carry a balance, it gets worse. Two thousand dollars of debt at twenty percent interest costs about four hundred dollars a year. The miles from that spending are worth about twenty.",
      type="versus", title="Carrying a balance (example)",
      left={"label": "Interest paid", "value": "$400", "sub": "$2,000 at 20% for a year", "color": "red"},
      right={"label": "Miles earned", "value": "$20", "sub": "2,000 miles at 1¢", "color": "green"},
      verdict="Pay in full, or the miles cost you")
scene("And remember who the airline's best customer really is. Every time you swipe that card, your bank pays the airline. That's why they push those cards so hard.",
      type="quote", text="You fly.\nYour bank pays the airline.", first_color="text", color="gold")
scene("Airlines barely make money flying. They make it from miles, fees, front seats and freight. Now you know where to look.",
      type="equation",
      lines=[{"text": "Flying barely pays.", "color": "muted", "size": 96},
             {"text": "Miles, fees & front seats do.", "color": "gold", "size": 96}])
scene("If this changed how you see your next flight, subscribe. We break down how money really works, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

# retention: payoff number inside the first ~10 s, and the intro (before chapter 1) under ~60 s of speech
assert S[0]["say"].lower().startswith("four dollars and fifty cents")   # PER_PAX_26, asserted above
intro_words = sum(len(x["say"].split()) for x in S[:next(i for i, x in enumerate(S) if x["visual"]["type"] == "chapter")])
assert intro_words <= 150, intro_words
assert DAL_AMEX > DAL_PRETAX                       # tease: "paid an airline more than ... entire profit before tax"
for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])

spec = {
    "id": "L005_airlines", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Figures: IATA (2026 = forecast), US BTS, airline filings · education, not investment advice",
    "title": "How Airlines Really Make Money: $4.50 a Passenger",
    "intro_chapter": "The $4.50 problem",
    "thumbnail": {"big": "$4.50", "line": "PROFIT PER PASSENGER", "tag": "SO WHAT PAYS?", "color": "gold"},
    "description": (
        "The world's airlines are expected to earn about $4.50 of net profit per passenger in 2026, a 2% margin, "
        "and the industry has never had a net margin above 5%. So what actually pays? Credit card miles, bag "
        "fees, premium cabins and cargo. We break down the economics of flying, the 2020 losses, United's "
        "$21.9 billion loyalty program, Warren Buffett's airline warning, and what it means for your miles.\n\n"
        "The per-flight example (180 seats, 84% full) and the miles/card examples are simple illustrations, "
        "not airline data. 2025 industry figures are IATA estimates; 2026 figures are IATA forecasts.\n\n"
        "Sources:\n"
        "- IATA, industry outlook press release (7 June 2026): https://www.iata.org/en/pressroom/2026-releases/"
        "06-07-middle-east-disruptions-high-fuel-prices-halve-airline-industry-profitability/\n"
        "- IATA, Industry Statistics fact sheet (June 2026): "
        "https://www.iata.org/en/iata-repository/pressroom/fact-sheets/industry-statistics/\n"
        "- IATA, Chart of the Week, Profits and Margins to Shrink in 2026 (19 June 2026)\n"
        "- US Bureau of Transportation Statistics, US Airlines gained $6.0 billion in 2025 (May 12, 2026): "
        "https://www.bts.gov/newsroom\n"
        "- Delta Air Lines, December quarter and full-year 2025 results (Jan 13, 2026): https://ir.delta.com\n"
        "- American Airlines Group, 2025 Form 10-K and Q4 2025 earnings release (Jan 27, 2026): "
        "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000006201\n"
        "- United Airlines Holdings, Form 8-K and MileagePlus investor presentation (June 15, 2020): "
        "https://www.sec.gov/Archives/edgar/data/100517/000110465920073190/tm2022354d3_8k.htm\n"
        "- United, Completion of MileagePlus Senior Secured Notes Offering (July 2, 2020): "
        "https://united.mediaroom.com/2020-07-02-United-Announces-Completion-of-MileagePlus-Senior-Secured-Notes-Offering\n"
        "- Berkshire Hathaway 2007 shareholder letter: https://www.berkshirehathaway.com/letters/2007ltr.pdf\n\n"
        "For education only. Not financial advice.\n\n"
        "#airlines #businessbreakdown #frequentflyer #creditcards #personalfinance"
    ),
    "tags": ["how airlines make money", "airline business model", "airline profits", "airline miles",
             "frequent flyer programs", "credit card rewards", "baggage fees", "MileagePlus", "Delta American Express",
             "Warren Buffett airlines", "business breakdown", "economics explained"],
    "localizations": {
        "es": {"title": "Cómo ganan dinero las aerolíneas: $4.50 por pasajero",
               "summary": "Las aerolíneas del mundo ganarán unos 4,50 dólares por pasajero en 2026, un margen del 2 %. "
                          "Entonces, ¿de dónde sale el dinero? Millas vendidas a bancos, tarifas de equipaje, "
                          "cabinas premium y carga. Explicamos la economía de volar y qué significa para tus millas."},
        "pt": {"title": "Como as aéreas realmente lucram: $4.50 por passageiro",
               "summary": "As companhias aéreas do mundo devem lucrar cerca de US$ 4,50 por passageiro em 2026, "
                          "uma margem de 2%. Então, de onde vem o dinheiro? Milhas vendidas a bancos, taxas de "
                          "bagagem, cabines premium e carga. Explicamos a economia da aviação e o que isso significa "
                          "para as suas milhas."},
        "hi": {"title": "एयरलाइंस असल में पैसा कैसे कमाती हैं: $4.50 प्रति यात्री",
               "summary": "2026 में दुनिया की एयरलाइंस को हर यात्री पर लगभग 4.50 डॉलर का ही मुनाफ़ा होने का अनुमान है, "
                          "यानी सिर्फ़ 2% मार्जिन। तो पैसा कहाँ से आता है? बैंकों को बेचे गए माइल्स, बैगेज फ़ीस, "
                          "प्रीमियम सीटें और कार्गो। इस वीडियो में उड़ान का अर्थशास्त्र और आपके माइल्स पर इसका असर।"},
        "id": {"title": "Cara Maskapai Sebenarnya Cari Uang: $4.50 per Penumpang",
               "summary": "Maskapai dunia diperkirakan hanya untung sekitar 4,50 dolar AS per penumpang pada 2026, "
                          "margin 2%. Lalu dari mana uangnya? Mil yang dijual ke bank, biaya bagasi, kabin premium, "
                          "dan kargo. Kami jelaskan ekonomi penerbangan dan artinya bagi mil Anda."},
        "de": {"title": "Wie Airlines wirklich Geld verdienen: $4.50 pro Passagier",
               "summary": "Die Airlines der Welt verdienen 2026 voraussichtlich nur rund 4,50 US-Dollar pro Passagier, "
                          "eine Marge von 2 %. Woher kommt also das Geld? Meilen, die an Banken verkauft werden, "
                          "Gepäckgebühren, Premium-Kabinen und Fracht. Wir erklären die Ökonomie des Fliegens und "
                          "was sie für Ihre Meilen bedeutet."},
        "fr": {"title": "Ce que gagnent vraiment les compagnies aériennes : $4.50 par passager",
               "summary": "Les compagnies aériennes mondiales devraient gagner environ 4,50 dollars par passager en "
                          "2026, soit une marge de 2 %. D'où vient donc l'argent ? Des miles vendus aux banques, des "
                          "frais de bagages, des cabines premium et du fret. Nous expliquons l'économie du transport "
                          "aérien et ce que cela change pour vos miles."},
    },
    "scenes": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L005_airlines.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", sum(len(s["say"].split()) for s in S), "words; intro", intro_words, "words")
