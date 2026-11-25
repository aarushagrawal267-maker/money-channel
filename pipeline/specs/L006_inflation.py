"""Long-form L006 (money math, USD): Inflation, explained: why your money quietly shrinks.

Sources (checked 2026-11-25):
  [CPI26] BLS, "Consumer Price Index - September 2026" (released Oct 14, 2026): all items +3.7% over 12 months
          (NSA); all items less food & energy +2.6%; energy +20.4%; food +2.5%; gasoline +34.2%.
  [CPI10] BLS, "Consumer Price Index - October 2026" (released Nov 10, 2026) + BLS notice "12-month changes
          for October 2026": "BLS did not collect survey data for October 2025 because of a lapse in
          appropriations", so no 12-month change for October 2026. Next release Dec 10, 2026.
  [IDX]   BLS series CUUR0000SA0 (CPI-U, US city average, NSA, 1982-84=100): Jun 2021 271.696,
          Jun 2022 296.311, Sep 2025 324.800, Sep 2026 336.940.
  [CPI22] BLS, "Consumer Price Index - June 2022" (Jul 13, 2022): all items +9.1% over 12 months, "the largest
          12-month increase since the period ending November 1981"; energy +41.6%; gasoline +59.9%.
  [MPLS]  Federal Reserve Bank of Minneapolis, "Consumer Price Index, 1913-" (annual averages from BLS):
          1913 9.9 ... 2025 321.9, and annual % changes 2015-2025.
  [FAQ]   BLS, CPI Questions and Answers: prices of "about 80,000 items each month"; "more than 200
          categories"; CPI-U covers "over 90 percent of the U.S. population"; weights from the Consumer
          Expenditure Surveys.
  [RI]    BLS, Relative importance of components in the CPI, December 2025 (CPI-U): shelter 35.625,
          food 13.698, energy 6.383 (shelter = rent + owners' equivalent rent; the broader Housing group is 44.469,
          not used).
  [FED]   FOMC, Statement on Longer-Run Goals and Monetary Policy Strategy (adopted effective Jan 24, 2012;
          reaffirmed effective Jan 27, 2026): 2% goal measured by the PCE price index; "The inflation rate
          over the longer run is primarily determined by monetary policy"; policy works "with a lag".
  [STL]   St. Louis Fed, Open Vault, "The Fed's Inflation Target: Why 2 Percent?" (Jan 16, 2019): measurement
          bias, room to cut interest rates, avoiding deflation; economists don't all agree.
  [FOMC]  FOMC statements: Mar 16, 2022 (raised to 1/4-1/2 percent, i.e. from 0-1/4); Jul 26, 2023
          (5-1/4 to 5-1/2 percent); Sep 18, 2024 (first cut, by 1/2 point to 4-3/4 to 5 percent); Dec 10, 2025
          (lowered to 3-1/2 to 3-3/4 percent); Sep 16, 2026 (raised by 1/4 point to 3-3/4 to 4 percent; "Inflation
          remains elevated"); Oct 28, 2026 (held at 3-3/4 to 4 percent). Next decision Dec 9, 2026 (after we publish).
  [RE]    BLS Real Earnings: Jun 2022 release (Jul 13, 2022) real average hourly earnings -3.6% (SA) Jun 2021 -
          Jun 2022 (Table A-1: average hourly earnings +5.1%, CPI-U SA +9.0%); Sep 2026 release (Oct 14, 2026): real AHE -0.7% Sep 2025 - Sep 2026; Table A-1: average
          hourly earnings +3.0%, CPI-U +3.7%.
  [FDIC]  FDIC national rates (Nov 16, 2026): savings 0.39%.
  [TD-I]  TreasuryDirect, I bonds: 5.51% for bonds issued Nov 1, 2026 - Apr 30, 2027, including a 1.40% fixed
          rate; 5.51% applies to a bond's first six months (the 1.40% fixed part lasts for its life, the inflation part
          resets every 6 months); up to $10,000 electronic per SSN per calendar year; cash in
          after 12 months; lose last 3 months of interest if cashed before 5 years; earns up to 30 years.
  [TD-T]  TreasuryDirect, TIPS: principal goes up with inflation (CPI) and down with deflation; fixed rate paid
          every six months on the adjusted principal; at maturity the greater of adjusted or original
          principal; terms 5, 10, 30 years.
Hypothetical (labelled on screen): $10,000 example, the 3.5% savings rate, the $2,000 fixed mortgage payment,
the 3% inflation used in the 20-year and mortgage illustrations.
Left out (not confirmed or not needed): money-supply growth figures, current high-yield savings rates.
"""
import json, math, os

# ---- [IDX] CPI-U index levels
CPI = {"2021-06": 271.696, "2022-06": 296.311, "2025-09": 324.800, "2026-09": 336.940}
YOY_SEP26 = 0.037                       # [CPI26] published, rounded
CORE_SEP26, ENERGY_SEP26, GAS_SEP26 = 0.026, 0.204, 0.342
YOY_JUN22, ENERGY_JUN22, GAS_JUN22 = 0.091, 0.416, 0.599   # [CPI22]
# ---- [MPLS] annual averages and annual inflation
ANNUAL_CPI = {1913: 9.9, 1930: 16.7, 1940: 14.0, 1950: 24.1, 1960: 29.6, 1970: 38.8, 1980: 82.4,
              1990: 130.7, 2000: 172.2, 2010: 218.1, 2025: 321.9}
ANNUAL_INF = {2015: 0.1, 2016: 1.3, 2017: 2.1, 2018: 2.4, 2019: 1.8, 2020: 1.2, 2021: 4.7, 2022: 8.0,
              2023: 4.1, 2024: 2.9, 2025: 2.6}
# ---- [FAQ] / [RI]
ITEMS_PRICED, CATEGORIES, POP_COVERED = 80_000, 200, 0.90
W_SHELTER, W_FOOD, W_ENERGY = 35.625, 13.698, 6.383
# ---- [FED] / [FOMC]
FED_TARGET = 0.02
RATE_2022_TOP_BEFORE, RATE_2023 = 0.0025, (0.0525, 0.055)
RATE_SEP24 = (0.0475, 0.05)                 # first cut, Sep 18, 2024
RATE_DEC25 = (0.035, 0.0375)                # after the Dec 10, 2025 cut
RATE_SEP26 = (0.0375, 0.04)                 # +1/4 point, Sep 16, 2026; held Oct 28, 2026
# ---- [RE]
REAL_AHE_JUN22, REAL_AHE_SEP26, AHE_SEP26 = -0.036, -0.007, 0.030
AHE_JUN22, CPI_SA_JUN22 = 0.051, 0.090      # [RE] Table A-1, Jun 2022 release (CPI-U seasonally adjusted)
# ---- [FDIC]
SAVINGS_AVG = 0.0039
# ---- [TD-I]
IBOND_RATE, IBOND_FIXED, IBOND_LIMIT = 0.0551, 0.0140, 10_000

# ---------------------------------------------------------------- derived (every spoken number asserted)
P = 10_000
r = CPI["2026-09"] / CPI["2025-09"]                      # price ratio over the latest year
assert abs(round((r - 1) * 100, 1) - YOY_SEP26 * 100) < 1e-9       # index ratio reproduces BLS's 3.7%
assert abs(round((CPI["2022-06"] / CPI["2021-06"] - 1) * 100, 1) - YOY_JUN22 * 100) < 1e-9   # and the 9.1% peak
assert 3.73 < (r - 1) * 100 < 3.75                       # "three point seven four percent"
cash_real = P / r
lost = P - cash_real
assert 359.5 < lost < 361                                # hook: "about three hundred and sixty dollars"
assert 9635 < cash_real < 9645                           # "about nine thousand six hundred and forty"
assert round(P * YOY_SEP26) == 370                             # "not three hundred and seventy"
sav_real = P * (1 + SAVINGS_AVG) / r
ex_rate = 0.035                                          # example rate, not a quote
ex_real = P * (1 + ex_rate) / r
assert 322 < P - sav_real < 323.5                        # "about three hundred and twenty-three"
assert 22 < P - ex_real < 23.5                           # "about twenty-three"
bite = P * (1 + ex_rate) - ex_real
assert 372.5 < bite < 373.5                              # "about three hundred and seventy-three"
assert 9976.5 < ex_real < 9977.5                         # "about nine thousand nine hundred and seventy-seven"
real_ret = (1 + ex_rate) / r - 1
assert -0.0025 < real_ret < -0.002

# long run
dollar_1913 = ANNUAL_CPI[2025] / ANNUAL_CPI[1913]
cagr = dollar_1913 ** (1 / (2025 - 1913)) - 1
cents_left = 100 / dollar_1913
assert 32.4 < dollar_1913 < 32.6                         # "about thirty-two dollars and fifty cents"
assert 0.031 < cagr < 0.033                              # "a little over three percent a year"
assert 2.95 < cents_left < 3.15                          # "about three cents"
assert 0.965 < 1 - 1 / dollar_1913 < 0.975               # "about ninety-seven percent"
assert (2022 + 5 / 12) - (1981 + 10 / 12) > 40           # Jun 2022 vs Nov 1981: "more than forty years"
assert max(ANNUAL_INF[y] for y in range(2015, 2021)) <= 2.4 and ANNUAL_INF[2022] == 8.0
assert sum(ANNUAL_INF[y] <= 2.1 for y in range(2015, 2021)) == 5   # "around two percent or less" (2018: 2.4)

# basket weights
w_other = 100 - W_SHELTER - W_FOOD - W_ENERGY
assert round(W_SHELTER) == 36 and round(W_FOOD) == 14 and round(W_ENERGY) == 6
assert round(ENERGY_JUN22 * 100) == 42 and round(GAS_JUN22 * 100) == 60
assert round(ENERGY_SEP26 * 100) == 20 and round(GAS_SEP26 * 100) == 34

# doubling times
dbl_2 = math.log(2) / math.log(1 + FED_TARGET)
dbl_37 = math.log(2) / math.log(1 + YOY_SEP26)
assert round(dbl_2) == 35 and round(dbl_37) == 19         # "about every thirty-five / nineteen years"

# wages
assert abs((1 + AHE_SEP26) / (1 + YOY_SEP26) - 1 - REAL_AHE_SEP26) < 0.001   # 3.0% vs 3.7% -> about -0.7%
assert abs((1 + AHE_JUN22) / (1 + CPI_SA_JUN22) - 1 - REAL_AHE_JUN22) < 0.001 # 5.1% vs 9.0% -> about -3.6%

# fixed-rate borrower (illustration, 3% a year)
PAY, INF_EX = 2000, 0.03
pay10, pay20 = PAY / (1 + INF_EX) ** 10, PAY / (1 + INF_EX) ** 20
assert 1485 < pay10 < 1492                               # "about fourteen hundred and ninety"
assert 1100 < pay20 < 1110                               # "about eleven hundred"

# 20 years at 3% inflation (illustration)
yrs = list(range(0, 21))
path = lambda rate: [P * ((1 + rate) / (1 + INF_EX)) ** n for n in yrs]
cash20, sav20, ex20 = path(0)[-1], path(SAVINGS_AVG)[-1], path(ex_rate)[-1]
assert 5500 < cash20 < 5560                              # "about five thousand five hundred"
assert 10900 < ex20 < 11100                              # "about eleven thousand"

assert RATE_SEP24[1] < RATE_2023[1] and RATE_DEC25[1] < RATE_SEP24[1]           # cuts in 2024 and 2025
assert abs(RATE_SEP26[0] - RATE_DEC25[0] - 0.0025) < 1e-9                       # "a quarter point"
# I bonds: the composite should sit above the fixed rate
assert IBOND_RATE > IBOND_FIXED
print(f"r={r:.5f} lost ${lost:.1f} sav ${P - sav_real:.1f} ex ${P - ex_real:.1f} bite ${bite:.1f} "
      f"1913 x{dollar_1913:.2f} cagr {cagr:.4f} dbl {dbl_2:.1f}/{dbl_37:.1f} pay {pay10:.0f}/{pay20:.0f} "
      f"20y {cash20:.0f}/{sav20:.0f}/{ex20:.0f}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook (payoff in the first 10 s, then the
# promise, then a tease that pays off in chapter 5: fixed-rate borrowers come out ahead)
scene("Ten thousand dollars in a drawer quietly lost about three hundred and sixty dollars over the latest year of US price data. Nobody took a single bill.",
      type="stat", value=f"−${lost:.0f}", label="buying power lost by $10,000 in cash",
      sub="Sept 2025 → Sept 2026 · US consumer prices (BLS)", color="red")
scene("On paper, it's still ten thousand. But at today's prices, it buys only what about nine thousand six hundred and forty bought a year ago.",
      type="versus", title="The same $10,000",
      left={"label": "On paper", "value": "$10,000", "sub": "the number never changes", "color": "slate"},
      right={"label": "Buying power", "value": f"${round(cash_real, -1):,.0f}", "sub": "in last year's prices", "color": "red"},
      verdict="Prices rose 3.7% in a year")
scene("That's inflation. It never sends you a bill. It just shrinks what every dollar can do.",
      type="title", title="Inflation, Explained", sub="why your money quietly shrinks")
scene("Here's what you'll learn. What inflation really measures. What causes it. Who wins and who loses. And what you can actually do about it.",
      type="bullets", title="What you'll learn",
      items=["What inflation really measures", "What causes it", "Who wins, who loses", "What you can do about it"])
scene("And by the end, you'll see why some people actually come out ahead when prices rise, and how to tell which side you're on.",
      type="equation", title="Coming up",
      lines=[{"text": "Prices rise", "color": "text", "size": 100},
             {"text": "↓", "color": "dim", "size": 80},
             {"text": "some people win", "color": "gold", "size": 100}])

# ---------------------------------------------------------------- 1
scene("Chapter one. What inflation actually is.", type="chapter", n=1, title="What inflation is")
scene("Inflation is a rise in prices across the whole economy. Not one thing getting pricier, but most things, over time. So each dollar buys a little less.",
      type="quote", text="Prices go up.\nEach dollar buys less.", first_color="text", color="gold")
scene("In the US, it's measured by the Bureau of Labor Statistics. Every month, it records the prices of about eighty thousand items, sorted into more than two hundred categories.",
      type="stat_grid", title="How the US measures prices",
      items=[{"value": "80,000", "label": "prices checked monthly", "sub": "approx., BLS", "color": "gold"},
             {"value": "200+", "label": "categories", "color": "blue"},
             {"value": "90%+", "label": "of people covered", "sub": "CPI-U", "color": "green"}])
scene("Rent, groceries, gas, car insurance, doctor visits, phone bills. Together they form a basket, and the price of that basket is the Consumer Price Index, or C-P-I.",
      type="bullets", title="The basket", color="gold",
      items=["Rent & housing", "Groceries & restaurants", "Gas & electricity", "Cars, insurance, doctors, phones"])
scene("The basket is weighted by what households actually spend. Shelter, meaning rent and the rental value of owned homes, is the biggest piece, about thirty-six percent. Food is about fourteen. Energy, about six.",
      type="donut", title="What's in the US price basket (CPI-U)",
      segments=[{"label": "Shelter", "value": W_SHELTER, "color": "gold", "display": f"{W_SHELTER:.0f}%"},
                {"label": "Food", "value": W_FOOD, "color": "green", "display": f"{W_FOOD:.0f}%"},
                {"label": "Energy", "value": W_ENERGY, "color": "red", "display": f"{W_ENERGY:.0f}%"},
                {"label": "Everything else", "value": w_other, "color": "slate", "display": f"{w_other:.0f}%"}],
      center="CPI-U", center_sub="weights, Dec 2025")
scene("The headline number compares the basket with a year earlier. In September twenty twenty-five, the index stood at three twenty-four point eight. By September twenty twenty-six, three thirty-six point nine. A rise of three point seven percent. Sounds small. So is it?",
      type="equation", title="How the headline number works",
      lines=[{"text": f"{CPI['2025-09']:.1f} → {CPI['2026-09']:.1f}", "color": "muted", "size": 100},
             {"text": "Sept 2025 → Sept 2026", "color": "dim", "size": 60},
             {"text": f"= +{YOY_SEP26 * 100:.1f}%", "color": "gold", "size": 130}])

# ---------------------------------------------------------------- 2
scene("Chapter two. The real numbers.", type="chapter", n=2, title="The real numbers")
scene("Three point seven percent is the latest yearly figure, for September twenty twenty-six. That's well above the Federal Reserve's goal of two percent, which uses a slightly different measure.",
      type="stat", value=f"{YOY_SEP26 * 100:.1f}%", label="US inflation, 12 months to Sept 2026",
      sub="CPI-U · Bureau of Labor Statistics, 14 Oct 2026", color="gold")
scene("And if you're looking for October's number, there isn't one. The twenty twenty-five government shutdown meant October twenty twenty-five prices were never collected, so there's nothing to compare against. The next report is due December tenth.",
      type="quote", text="\"BLS did not collect survey data\nfor October 2025\"", first_color="text", color="gold",
      source="BLS notice, 10 Nov 2026 · no 12-month figure for October 2026")
scene("Now zoom out. From twenty fifteen to twenty twenty, yearly inflation mostly stayed around two percent or less. Then it jumped. Four point seven percent in twenty twenty-one, and eight percent for twenty twenty-two as a whole.",
      type="columns", title="US inflation by year (annual average)", highlight=7,
      items=[{"label": str(y), "value": max(v, 0.15), "display": f"{v:.1f}%"} for y, v in ANNUAL_INF.items()],
      note="Source: BLS CPI-U annual averages, via Minneapolis Fed")
scene("The worst moment came in June twenty twenty-two. Prices were up nine point one percent from a year before. The biggest yearly jump in more than forty years.",
      type="count", to=YOY_JUN22 * 100, suffix="%", dp=1, label="peak: 12 months to June 2022",
      sub="largest since November 1981 · BLS", color="red")
scene("Now the really long view. Something that cost one dollar in nineteen thirteen cost about thirty-two dollars and fifty cents in twenty twenty-five.",
      type="line", title="What $1 of 1913 goods cost later", format="usd",
      x=list(ANNUAL_CPI), series=[{"label": f"${dollar_1913:.2f}", "values": [v / ANNUAL_CPI[1913] for v in ANNUAL_CPI.values()], "color": "gold"}])
scene("That works out to a little over three percent a year, on average, for more than a century. Put the other way, a nineteen thirteen dollar now buys about three cents' worth. Ninety-seven percent of its buying power, gone. So why do prices keep rising at all?",
      type="stat_grid", title="US prices since 1913",
      items=[{"value": f"{cagr * 100:.1f}%", "label": "average a year", "sub": "1913–2025", "color": "gold"},
             {"value": f"{cents_left:.0f}¢", "label": "what a 1913 dollar buys", "sub": "in 1913 goods", "color": "red"},
             {"value": f"−{(1 - 1 / dollar_1913) * 100:.0f}%", "label": "buying power lost", "color": "red"}])

# ---------------------------------------------------------------- 3
scene("Chapter three. What causes it.", type="chapter", n=3, title="What causes it")
scene("Economists usually point to three engines. Demand. Supply shocks. And money and credit.",
      type="bullets", title="Three engines of inflation", color="gold",
      items=["Too much demand", "Supply shocks", "Money & credit"])
scene("First, demand. When people, businesses and governments try to buy more than the economy can make, sellers raise prices. Too much money chasing too few goods.",
      type="equation", title="1 · Demand",
      lines=[{"text": "More buyers", "color": "text", "size": 96},
             {"text": "+ the same goods", "color": "muted", "size": 80},
             {"text": "= higher prices", "color": "gold", "size": 110}])
scene("Second, supply shocks. When something essential suddenly gets scarce or expensive, like oil, the cost ripples through everything. In June twenty twenty-two, energy prices were up forty-two percent in a year. Gasoline, sixty percent.",
      type="stat_grid", title="2 · Supply shock: June 2022 vs a year earlier",
      items=[{"value": f"+{ENERGY_JUN22 * 100:.1f}%", "label": "energy", "color": "red"},
             {"value": f"+{GAS_JUN22 * 100:.1f}%", "label": "gasoline", "color": "red"},
             {"value": f"+{YOY_JUN22 * 100:.1f}%", "label": "all items", "color": "gold"}])
scene("And it's happening again. In the year to September, energy rose about twenty percent and gasoline thirty-four. But prices without food and energy rose just two point six percent.",
      type="hbars", title="12 months to Sept 2026",
      items=[{"label": "Gasoline", "value": GAS_SEP26, "display": f"+{GAS_SEP26 * 100:.1f}%", "color": "red"},
             {"label": "Energy", "value": ENERGY_SEP26, "display": f"+{ENERGY_SEP26 * 100:.1f}%", "color": "red"},
             {"label": "All items", "value": YOY_SEP26, "display": f"+{YOY_SEP26 * 100:.1f}%", "color": "gold"},
             {"label": "Excl. food & energy", "value": CORE_SEP26, "display": f"+{CORE_SEP26 * 100:.1f}%", "color": "slate"}])
scene("Third, money and credit. When borrowing is cheap and money flows freely, spending can outrun what the economy produces. The Federal Reserve itself says inflation over the longer run is primarily determined by monetary policy.",
      type="quote", text="\"Primarily determined\nby monetary policy\"", first_color="text", color="gold",
      source="Federal Reserve, Statement on Longer-Run Goals (reaffirmed Jan 2026)")
scene("And inflation can feed itself. If people expect higher prices, workers push for bigger raises, businesses raise prices to cover them, and the cycle keeps turning. So who's supposed to stop it?",
      type="flywheel", title="How inflation can feed itself", center="LOOP",
      steps=["Expect higher prices", "Push for raises", "Costs go up", "Prices rise"])

# ---------------------------------------------------------------- 4
scene("Chapter four. Why the Fed aims for two percent.", type="chapter", n=4, title="Why the Fed aims for 2%")
scene("The US Federal Reserve aims for inflation of two percent a year, measured by a cousin of the C-P-I called the P-C-E price index. It made that goal official in January twenty twelve, and reaffirmed it this January.",
      type="stat", value="2%", label="the Fed's longer-run inflation goal",
      sub="PCE price index · adopted 2012, reaffirmed Jan 2026", color="green")
scene("Why not zero? A St. Louis Fed economist gives three reasons. Price measures may run slightly high, so two percent measured may be closer to zero in reality. Falling prices, called deflation, may do more harm. And a little inflation leaves room to cut interest rates in a recession. Not every economist agrees.",
      type="bullets", title="Why not 0%?", color="green",
      items=["Price measures may run a little high", "Deflation may do more harm", "Room to cut rates in a recession"])
scene("The Fed's main tool is interest rates. To fight the twenty twenty-two surge, it raised its key rate from near zero in March twenty twenty-two to five and a quarter to five and a half percent by July twenty twenty-three. It cut rates in twenty twenty-four and twenty twenty-five, to three and a half to three and three-quarters percent. Then this September, with inflation elevated again, it raised them a quarter point, to between three and three-quarters and four percent, where they stood as this video was made.",
      type="timeline", title="The Fed's key interest rate",
      events=[{"when": "Mar 2022", "text": "First hike\nfrom near 0%"},
              {"when": "Jun 2022", "text": "Inflation\npeaks at 9.1%", "color": "red"},
              {"when": "Jul 2023", "text": "Rate reaches\n5.25%–5.5%", "color": "gold"},
              {"when": "2024–25", "text": "Cuts to\n3.5%–3.75%", "color": "green"},
              {"when": "Sep 2026", "text": "+0.25 pt to\n3.75%–4%", "color": "red"}])
scene("Higher rates make borrowing more expensive. People and businesses spend less, and price pressure cools. But it works with a lag, so the Fed is always steering by the rear-view mirror.",
      type="equation", title="How higher rates cool prices",
      lines=[{"text": "Higher rates", "color": "gold", "size": 96},
             {"text": "→ less borrowing & spending", "color": "text", "size": 76},
             {"text": "→ prices cool, with a lag", "color": "green", "size": 76}])
scene("And even the target adds up. At two percent, prices double about every thirty-five years. At three point seven percent, about every nineteen. But inflation doesn't hit everyone the same way. Some people actually win.",
      type="columns", title="Years for prices to double",
      items=[{"label": "at 2% a year", "value": dbl_2, "display": f"{dbl_2:.0f} yrs", "color": "green"},
             {"label": "at 3.7% a year", "value": dbl_37, "display": f"{dbl_37:.0f} yrs", "color": "red"}],
      note="If inflation stayed at that rate · simple math, not a forecast")

# ---------------------------------------------------------------- 5
scene("Chapter five. Who wins and who loses.", type="chapter", n=5, title="Who wins, who loses")
scene("Start with the losers. Cash savers. Money in a drawer, or in an account paying less than inflation, loses buying power every year. The national average savings rate is just zero point three nine percent, according to the Federal Deposit Insurance Corporation.",
      type="versus", title="Savers, November 2026",
      left={"label": "Average savings rate", "value": f"{SAVINGS_AVG * 100:.2f}%", "sub": "FDIC national rate", "color": "slate"},
      right={"label": "Inflation", "value": f"{YOY_SEP26 * 100:.1f}%", "sub": "12 months to Sept 2026", "color": "red"},
      verdict="Savers fall behind")
scene("Now the winners. Borrowers with fixed-rate loans. Say your fixed mortgage payment, principal and interest, is two thousand dollars a month. If prices rise three percent a year, in ten years that payment feels like about fourteen hundred and ninety in today's money. In twenty years, about eleven hundred.",
      type="columns", title="A fixed $2,000 loan payment, in today's dollars (example)",
      items=[{"label": "Today", "value": PAY, "display": "$2,000", "color": "slate"},
             {"label": "In 10 years", "value": pay10, "display": f"${pay10:,.0f}", "color": "green"},
             {"label": "In 20 years", "value": pay20, "display": f"${pay20:,.0f}", "color": "green"}],
      note="Example: principal & interest only, 3% inflation a year · only helps if your income keeps up")
scene("That's the twist. Inflation quietly moves value from lenders to fixed-rate borrowers. The bank gets paid back in cheaper dollars, especially when inflation turns out higher than expected when the loan was made, and as long as the borrower's income keeps rising.",
      type="equation", title="The twist",
      lines=[{"text": "Fixed payment", "color": "text", "size": 96},
             {"text": "+ rising prices & pay", "color": "muted", "size": 80},
             {"text": "= cheaper debt", "color": "gold", "size": 110}])
scene("Workers are in the middle. It depends on whether pay keeps up. In the year to June twenty twenty-two, average hourly pay rose about five percent, but prices rose about nine. So real pay, meaning pay after inflation, fell three point six percent. In the year to September twenty twenty-six, average pay rose three percent, but prices rose three point seven. Real pay fell zero point seven percent.",
      type="table", title="US average hourly pay vs prices (seasonally adjusted)",
      header=["12 months to", "Pay", "Prices", "Real pay"],
      rows=[["June 2022", f"+{AHE_JUN22 * 100:.1f}%", f"+{CPI_SA_JUN22 * 100:.1f}%", f"−{-REAL_AHE_JUN22 * 100:.1f}%"],
            ["Sept 2026", f"+{AHE_SEP26 * 100:.1f}%", f"+{YOY_SEP26 * 100:.1f}%", f"−{-REAL_AHE_SEP26 * 100:.1f}%"]],
      col_colors={"3": "red"})
scene("So, roughly. Cash savers and lenders tend to lose. Fixed-rate borrowers tend to win. Workers win or lose depending on their raises. To know which side you're on, you need one simple formula.",
      type="bullets", title="Who inflation hits",
      items=["Cash savers & lenders: tend to lose", "Fixed-rate borrowers: tend to win", "Workers: depends on raises"])

# ---------------------------------------------------------------- 6
scene("Chapter six. The math of buying power.", type="chapter", n=6, title="The math of buying power")
scene("Here it is. Your real return is one plus your interest rate, divided by one plus inflation, minus one. As a shortcut: your rate minus inflation.",
      type="equation", title="Your real return",
      lines=[{"text": "(1 + your rate) ÷ (1 + inflation) − 1", "color": "text", "size": 76},
             {"text": "≈", "color": "dim", "size": 80},
             {"text": "your rate − inflation", "color": "gold", "size": 100}])
scene("That's why our drawer lost about three hundred and sixty dollars, not three hundred and seventy. Prices rose three point seven four percent, and ten thousand divided by one point zero three seven four is about nine thousand six hundred and forty.",
      type="stat", value=f"${round(cash_real, -1):,.0f}", label=f"= $10,000 ÷ {r:.4f}",
      sub=f"lost ≈ ${lost:.0f}, not ${P * YOY_SEP26:.0f}", color="gold")
scene("Now compare three homes for that ten thousand over the same year, before tax. In cash, down about three hundred and sixty. At the average savings rate, down about three hundred and twenty-three. At three and a half percent, an example rate, not a quote, down only about twenty-three.",
      type="table", title="$10,000 for a year, before tax (Sept 2025 → Sept 2026)",
      header=["Where", "Earned", "Buying power"],
      rows=[["Cash", "0%", f"−${lost:.0f}"],
            ["Avg savings", f"{SAVINGS_AVG * 100:.2f}%", f"−${P - sav_real:.0f}"],
            ["Example rate", f"{ex_rate * 100:.1f}%", f"−${P - ex_real:.0f}"]],
      highlight_row=2, col_colors={"2": "red"})
scene("Here's that last one, step by step. Ten thousand, plus three hundred and fifty of interest, minus about three hundred and seventy-three lost to higher prices. You end with about nine thousand nine hundred and seventy-seven in buying power.",
      type="waterfall", title="$10,000 at an example 3.5% rate",
      steps=[{"label": "Start", "value": P, "kind": "start", "display": "$10,000"},
             {"label": "Interest", "value": P * ex_rate, "kind": "plus", "display": f"+${P * ex_rate:.0f}"},
             {"label": "Price rise", "value": bite, "kind": "minus", "display": f"−${bite:.0f}"},
             {"label": "Buying power", "value": ex_real, "kind": "total", "display": f"${ex_real:,.0f}"}])
scene("Over twenty years, at three percent inflation, the gap gets huge. Cash ends up worth about five thousand five hundred in today's money. At three and a half percent, about eleven thousand, before tax. So what can you actually do?",
      type="line", title="$10,000 over 20 years, 3% inflation, before tax (example)", format="usd",
      x=yrs, series=[{"label": "3.5%", "values": path(ex_rate), "color": "green"},
                     {"label": "Cash", "values": path(0), "color": "red"}])

# ---------------------------------------------------------------- 7
scene("Chapter seven. What you can do.", type="chapter", n=7, title="What you can do")
scene("Here are four practical moves. None of them is a product pitch, and none of them is magic.",
      type="bullets", title="Four moves",
      items=["Let your emergency fund earn", "Understand inflation-protected bonds", "Invest long-term money for growth",
             "Check your raise against inflation"])
scene("First, your emergency fund. It needs to be safe and easy to reach, so it shouldn't swing with markets. But it doesn't have to earn nothing. Some banks pay more than the national average, and rates change, so compare.",
      type="equation", title="1 · Your emergency fund",
      lines=[{"text": "Safe", "color": "text", "size": 96},
             {"text": "+ easy to reach", "color": "text", "size": 96},
             {"text": "+ earning something", "color": "gold", "size": 96}])
scene("Second, inflation-protected bonds from the US Treasury. With TIPS, the principal rises with the C-P-I and interest is paid on the adjusted amount. Held to maturity, you never get back less than the original principal. I bonds work differently: the rate itself has an inflation part that resets every six months.",
      type="table", title="Inflation-protected US Treasury bonds",
      header=["", "TIPS", "I bonds"],
      rows=[["Linked to", "CPI", "CPI"], ["What adjusts", "Principal", "Interest rate"],
            ["Terms", "5, 10, 30 yrs", "Up to 30 yrs"]],
      col_colors={"1": "gold", "2": "green"})
scene("I bonds bought from November twenty twenty-six to April twenty twenty-seven start at five point five one percent, including a one point four percent fixed part that lasts for the life of the bond. But there are trade-offs. You can buy up to ten thousand dollars a year electronically. You can't cash out for twelve months. And before five years, you lose the last three months of interest.",
      type="stat_grid", title="I bonds: the fine print (1.40% of the rate is fixed for life)",
      items=[{"value": f"{IBOND_RATE * 100:.2f}%", "label": "first 6 months", "sub": "if bought Nov 2026–Apr 2027", "color": "green"},
             {"value": "$10K", "label": "yearly limit", "sub": "per person, electronic", "color": "gold"},
             {"value": "12 mo", "label": "before you can cash out", "sub": "−3 months' interest before 5 yrs", "color": "red"}])
scene("These are built to keep pace with inflation, not to make you rich. Whether they fit depends on your goals and your timeline.",
      type="quote", text="Built to keep pace,\nnot to get rich.", first_color="text", color="gold")
scene("Third, money you won't need for many years. Over long periods, a diversified mix of investments has historically had a better chance of beating inflation than cash. But it can fall sharply, sometimes for years, and past results don't guarantee future ones.",
      type="versus", title="Match the money to the timeline",
      left={"label": "Needed soon", "value": "Savings", "sub": "safe, reachable, may trail prices", "color": "blue"},
      right={"label": "Needed in 10+ yrs", "value": "Invested", "sub": "can beat prices, can also fall", "color": "green"},
      verdict="Not advice · investments can lose value")
scene("Fourth, check your raise against inflation. A three percent raise in a year when prices rise three point seven percent is a small pay cut in disguise.",
      type="stat", value=f"−{-REAL_AHE_SEP26 * 100:.1f}%", label="a 3.0% raise when prices rise 3.7%",
      sub="your real raise · use the formula", color="red")
scene("Inflation never takes your money. It takes what your money can do. Now you know how to measure it, and how to keep up.",
      type="title", title="Measure it. Keep up.", sub="inflation takes what your money can do")
scene("If this changed how you see your savings, subscribe. We break down how money really works, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

# ---------------------------------------------------------------- retention checks
assert S[0]["say"].lower().startswith("ten thousand dollars in a drawer quietly lost about three hundred and sixty")            # payoff (lost, asserted) in first ~10 s
first_ch = next(i for i, x in enumerate(S) if x["visual"]["type"] == "chapter")
intro_words = sum(len(x["say"].split()) for x in S[:first_ch])
assert intro_words <= 150, intro_words
assert pay10 < PAY                                                        # tease: fixed-rate borrowers win (ch 5)
for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])
types = {x["visual"]["type"] for x in S}
assert len(types - {"chapter", "cta"}) >= 10, types
n_ch = sum(x["visual"]["type"] == "chapter" for x in S)
assert 6 <= n_ch <= 7, n_ch
words = sum(len(x["say"].split()) for x in S)
assert 1400 <= words <= 1700, words
# each chapter's last scene ends with an open loop (a question or a forward line), except the final chapter
ch_idx = [i for i, x in enumerate(S) if x["visual"]["type"] == "chapter"]
for i in ch_idx[1:]:
    assert S[i - 1]["say"].rstrip().endswith(("?", "win.", "formula.")), S[i - 1]["say"][-40:]

spec = {
    "id": "L006_inflation", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "MONEY MATH",
    "disclaimer": "Data: BLS, Federal Reserve, FDIC, TreasuryDirect · examples labelled · education, not advice",
    "title": "Inflation Explained: Why Your Money Quietly Shrinks",
    "intro_chapter": "The $360 drawer",
    "thumbnail": {"big": f"−${lost:.0f}", "line": "LOST FROM $10K CASH", "tag": "NOBODY TOOK IT", "color": "red"},
    "description": (
        "Inflation explained simply: what the Consumer Price Index (CPI) measures, why US prices rose 3.7% in "
        f"the year to September 2026, and why $10,000 in cash lost about ${lost:.0f} of buying power. We cover "
        "the 9.1% peak of June 2022, what causes inflation, why the Fed targets 2%, who wins and who loses, and "
        "what you can do: emergency savings, TIPS and I bonds, and long-term investing.\n\n"
        "Assumptions: the $10,000 example uses the CPI-U index for September 2025 (324.800) and September 2026 "
        "(336.940). The 3.5% savings rate, the $2,000 fixed mortgage payment and the 3% inflation rate in the "
        "20-year and mortgage examples are illustrations, not quotes or forecasts. Savings examples are before "
        "tax. The Fed's target range is as of 25 Nov 2026 (3.75%–4%; its next decision is 9 Dec 2026). The I bond "
        "rate of 5.51% applies to the first six months; the 1.40% fixed part lasts for the life of the bond. There is no 12-month CPI figure "
        "for October 2026 because October 2025 prices were not collected during the 2025 government shutdown.\n\n"
        "Sources:\n"
        "- BLS, Consumer Price Index, September 2026 (Oct 14, 2026) and October 2026 (Nov 10, 2026): "
        "https://www.bls.gov/cpi/\n"
        "- BLS, CPI-U series CUUR0000SA0: https://data.bls.gov/timeseries/CUUR0000SA0\n"
        "- BLS, Consumer Price Index, June 2022 (Jul 13, 2022): https://www.bls.gov/news.release/archives/cpi_07132022.htm\n"
        "- BLS, CPI Questions and Answers: https://www.bls.gov/cpi/questions-and-answers.htm\n"
        "- BLS, Relative importance of CPI components, December 2025: "
        "https://www.bls.gov/cpi/tables/relative-importance/2025.htm\n"
        "- BLS, Real Earnings (June 2022 and September 2026): https://www.bls.gov/news.release/realer.htm\n"
        "- Federal Reserve Bank of Minneapolis, Consumer Price Index 1913-: "
        "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-\n"
        "- Federal Reserve, Statement on Longer-Run Goals and Monetary Policy Strategy (reaffirmed Jan 2026): "
        "https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf\n"
        "- Federal Reserve FOMC statements (Mar 16, 2022; Jul 26, 2023; Sep 18, 2024; Dec 10, 2025; Sep 16, 2026; "
        "Oct 28, 2026): "
        "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm\n"
        "- St. Louis Fed, The Fed's Inflation Target: Why 2 Percent? (Jan 16, 2019): "
        "https://www.stlouisfed.org/open-vault/2019/january/fed-inflation-target-2-percent\n"
        "- FDIC, National Rates and Rate Caps (Nov 16, 2026): https://www.fdic.gov/national-rates-and-rate-caps\n"
        "- TreasuryDirect, I bonds: https://www.treasurydirect.gov/savings-bonds/i-bonds/\n"
        "- TreasuryDirect, TIPS: https://www.treasurydirect.gov/marketable-securities/tips/\n\n"
        "For education only. Not financial advice. No product is recommended; investments can lose value and "
        "past results don't guarantee future ones.\n\n"
        "#inflation #personalfinance #economics #savings #moneymath"
    ),
    "tags": ["inflation explained", "what is inflation", "consumer price index", "CPI", "inflation 2026",
             "purchasing power", "why prices rise", "federal reserve 2 percent", "real return", "I bonds",
             "TIPS", "savings and inflation", "money math", "personal finance"],
    "localizations": {
        "es": {"title": "La inflación explicada: por qué tu dinero se encoge",
               "summary": f"Qué mide el IPC, por qué los precios en EE. UU. subieron un 3,7% en el año hasta "
                          f"septiembre de 2026 y por qué $10,000 en efectivo perdieron unos ${lost:.0f} de poder de "
                          "compra. Causas, el objetivo del 2% de la Fed, quién gana y quién pierde, y qué puedes hacer."},
        "pt": {"title": "Inflação explicada: por que seu dinheiro encolhe",
               "summary": f"O que o CPI mede, por que os preços nos EUA subiram 3,7% no ano até setembro de 2026 e "
                          f"por que $10,000 em dinheiro perderam cerca de ${lost:.0f} de poder de compra. Causas, a "
                          "meta de 2% do Fed, quem ganha e quem perde, e o que você pode fazer."},
        "hi": {"title": "महंगाई समझिए: आपका पैसा चुपचाप कैसे घटता है",
               "summary": f"CPI क्या मापता है, सितंबर 2026 तक के साल में अमेरिका में कीमतें 3.7% क्यों बढ़ीं, और नकद "
                          f"$10,000 की ख़रीदने की ताक़त लगभग ${lost:.0f} क्यों घट गई। महंगाई के कारण, Fed का 2% लक्ष्य, "
                          "किसे फ़ायदा और किसे नुकसान, और आप क्या कर सकते हैं।"},
        "id": {"title": "Inflasi Dijelaskan: Kenapa Uangmu Diam-diam Menyusut",
               "summary": f"Apa yang diukur CPI, kenapa harga di AS naik 3,7% dalam setahun hingga September 2026, "
                          f"dan kenapa uang tunai $10,000 kehilangan sekitar ${lost:.0f} daya beli. Penyebab, target 2% "
                          "The Fed, siapa untung dan rugi, dan apa yang bisa kamu lakukan."},
        "de": {"title": "Inflation erklärt: Warum dein Geld still schrumpft",
               "summary": f"Was der Verbraucherpreisindex misst, warum die US-Preise im Jahr bis September 2026 um "
                          f"3,7 % stiegen und warum $10,000 in bar rund ${lost:.0f} Kaufkraft verloren. Ursachen, "
                          "das 2-%-Ziel der Fed, Gewinner und Verlierer und was du tun kannst."},
        "fr": {"title": "L'inflation expliquée : pourquoi votre argent fond",
               "summary": f"Ce que mesure l'indice des prix, pourquoi les prix américains ont augmenté de 3,7 % sur "
                          f"l'année jusqu'à septembre 2026 et pourquoi $10,000 en espèces ont perdu environ "
                          f"${lost:.0f} de pouvoir d'achat. Causes, la cible de 2 % de la Fed, gagnants et perdants, "
                          "et ce que vous pouvez faire."},
    },
    "scenes": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L006_inflation.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words; intro", intro_words, "words; types", len(types))
