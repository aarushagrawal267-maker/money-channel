"""Long-form L003: Why most professional fund managers lose to a simple index fund.

Pillar: how markets work. Educational only: no fund names, no tickers, no recommendations.
Every spoken number is either a sourced constant (source + date in the comment) or computed
below with an assert that ties it to the words in the script.
"""
import json, os
from collections import Counter

# ---------------------------------------------------------------- sourced figures
# S&P Dow Jones Indices, SPIVA U.S. Scorecard Mid-Year 2026 (data to June 30, 2026), Report 1a,
# "All Large-Cap Funds vs S&P 500", % of funds underperforming. Primary PDF blocks automated
# fetches; figures as reproduced identically by two independent summaries of the report
# (retirementliteracyfoundation.org, assetwhisper.com), checked 2026-11-21.
LC_UNDER = {"5 yrs": 89.32, "10 yrs": 83.33, "15 yrs": 90.49, "20 yrs": 92.61}
# Same report, Report 2 (survivorship): share of large-cap funds alive in mid-2006 still alive in mid-2026.
LC_SURVIVE_20Y = 0.3652
# SPIVA U.S. Year-End 2025 (S&P DJI, March 2026): 79% of large-cap funds trailed the S&P 500 in 2025.
LC_UNDER_2025 = 0.79

# S&P DJI, U.S. Persistence Scorecard Year-End 2025 (published May 2026):
# 164 large-cap funds in the top quartile at end-2021; 0.00% still top quartile at end-2023, -2024, -2025.
PERSIST_TOPQ_START = 164
PERSIST_TOPQ_STAYED = 0
# Same report: large-cap funds above median in 2021 that stayed above median through 2025.
PERSIST_TOPHALF = 0.045

# ICI Research Perspective "Trends in the Expenses and Fees of Funds, 2025" (Vol. 32 No. 1, March 2026),
# Figure 6: asset-weighted average expense ratios, 2025.
FEE_ACTIVE = 0.0064         # actively managed equity mutual funds
FEE_INDEX = 0.0005          # index equity mutual funds

# ICI 2026 Investment Company Fact Book (April 2026), ch. 2: index mutual funds + index ETFs.
INDEX_SHARE_2025 = 0.52     # share of long-term fund assets, year-end 2025
INDEX_SHARE_2010 = 0.19     # year-end 2010
INDEX_TNA_2025 = 19.1e12    # total net assets, year-end 2025

# William F. Sharpe, "The Arithmetic of Active Management", Financial Analysts Journal 47(1), Jan/Feb 1991.
SHARPE_YEAR = 1991

# Vanguard press release, Aug 31, 2026 (50th anniversary of the Vanguard 500 Index Fund):
# First Index Investment Trust launched Aug 31, 1976; raised $11.3M vs a $150M target.
FIRST_INDEX_RAISED = 11.3e6
FIRST_INDEX_TARGET = 150e6

# Berkshire Hathaway 2017 shareholder letter (Feb 24, 2018), "The Bet is Over" section.
BET_FINAL = {"A": 21.7, "B": 42.3, "C": 87.7, "D": 2.8, "E": 27.0}   # cumulative gain 2008-2017, %
BET_ANNUAL = {"A": 2.0, "B": 3.6, "C": 6.5, "D": 0.3, "E": 2.4}      # average annual gain, %
BET_INDEX_FINAL, BET_INDEX_ANNUAL = 125.8, 8.5
BET_INDEX_2008 = -37.0      # S&P index fund, 2008
BET_HEDGE_FUNDS = 200       # "more than 200 hedge funds"
BET_FIXED_FEE = 0.025       # "fixed fees averaging a staggering 2 1/2% of assets or so"
BET_PRIZE = 1e6
BET_DONATED = 2_222_279     # received by Girls Inc. of Omaha

# RBC Wealth Management, "The Great Narrowing: S&P 500 concentration" (Jan 22, 2026):
TOP10_2025 = 0.407          # weight of 10 largest S&P 500 companies, year-end 2025 (record)
TOP10_RANGE = (0.18, 0.23)  # "hovered stably around 18%-23% between 1990 and 2015"

# ---------------------------------------------------------------- computed figures
under20 = LC_UNDER["20 yrs"] / 100
assert under20 > 0.9                                   # "more than nine out of ten"
assert 1 - under20 < 0.1                               # "fewer than one in ten" beat it
assert abs(LC_UNDER_2025 - 0.8) < 0.015                # "about four in five" trailed in 2025
assert 1 / 3 < LC_SURVIVE_20Y < 0.40                   # "just over a third" survived

PER_10K_ACTIVE = 10_000 * FEE_ACTIVE
PER_10K_INDEX = 10_000 * FEE_INDEX
assert round(PER_10K_ACTIVE) == 64 and round(PER_10K_INDEX) == 5    # "$64 vs $5 a year"
assert FEE_ACTIVE - FEE_INDEX < 0.01                   # "less than one percent"

# Fee drag illustration: $100,000, 30 years, 7% a year before fees (hypothetical).
P0, GROSS, YEARS = 100_000, 0.07, 30
def grow(fee, yrs=YEARS):
    return P0 * (1 + GROSS - fee) ** yrs
END_INDEX, END_ACTIVE = grow(FEE_INDEX), grow(FEE_ACTIVE)
FEE_GAP = END_INDEX - END_ACTIVE
assert 745_000 < END_INDEX < 755_000                   # "about seven hundred and fifty thousand"
assert 635_000 < END_ACTIVE < 637_000                  # "about six hundred and thirty-six thousand"
assert 110_000 < FEE_GAP < 115_000                     # "almost one hundred and fifteen thousand"

# Sharpe illustration: market 8%, average active dollar = market minus average fee.
MKT = 8.0
AVG_ACTIVE_NET = round(MKT - FEE_ACTIVE * 100, 2)
assert AVG_ACTIVE_NET == 7.36

# Persistence: chance of staying top half four more years by coin flip.
COIN4 = 0.5 ** 4
assert COIN4 == 0.0625                                 # "six point two five percent"
assert PERSIST_TOPHALF < COIN4                         # "worse than coin flips"

# Bet arithmetic
avg_final = sum(BET_FINAL.values()) / 5
avg_annual = sum(BET_ANNUAL.values()) / 5
assert round(avg_final, 1) == 36.3
assert abs(avg_annual - 3.0) < 0.05                    # "about three percent a year"
assert max(BET_ANNUAL.values()) == 6.5 and max(BET_FINAL.values()) == 87.7
assert min(BET_FINAL.values()) == 2.8
assert abs((1 + BET_INDEX_ANNUAL / 100) ** 10 - (1 + BET_INDEX_FINAL / 100)) < 0.01   # 8.5%/yr ~ +125.8%
assert BET_DONATED > 2.2e6                             # "over two point two million"
assert FIRST_INDEX_RAISED / FIRST_INDEX_TARGET < 0.08  # raised under a tenth of the goal
assert 0.40 < TOP10_2025 < 0.41                        # "about forty-one percent" (40.7)
assert INDEX_TNA_2025 / 1e12 == 19.1

print(f"20y under {under20:.1%} | fee gap ${FEE_GAP:,.0f} (index ${END_INDEX:,.0f}, active ${END_ACTIVE:,.0f}) "
      f"| bet avg final {avg_final:.1f}% avg annual {avg_annual:.2f}%")

# ---------------------------------------------------------------- script
S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

pct = lambda x, dp=0: f"{x * 100:.{dp}f}%"

# ---- Intro / hook
scene("Over the last twenty years, more than nine out of ten actively managed large US stock funds "
      "did worse than one simple benchmark: the S and P five hundred.",
      type="count", to=LC_UNDER["20 yrs"], dp=1, suffix="%", color="gold",
      label="of large-cap US funds trailed the S&P 500", sub="20 years to June 2026 · S&P SPIVA scorecard")
scene("And it isn't ancient history. In 2025 alone, seventy-nine percent of them fell behind.",
      type="share", title="Large-cap US funds that trailed the S&P 500",
      rows=[{"label": "In 2025", "share": LC_UNDER_2025, "color": "gold"},
            {"label": "Over 20 years", "share": under20, "color": "red", "dp": 1}],
      note="Source: S&P Dow Jones Indices, SPIVA U.S. Scorecards")
scene("These are full-time professionals with research teams and huge budgets. "
      "And they lost to a fund that does no research at all.",
      type="versus", title="Who should win?",
      left={"label": "Active fund", "value": "Experts", "sub": "analysts, research, trading", "color": "blue"},
      right={"label": "Index fund", "value": "Autopilot", "sub": "no stock picking at all", "color": "green"})
scene("In this video, we'll see why that happens, why it isn't just bad luck, "
      "and where index funds have real weaknesses too.",
      type="title", title="The Index Fund Paradox", sub="why the experts keep losing")

# ---- Chapter 1
scene("First, what is an index fund?", type="chapter", n=1, title="What is an index fund?")
scene("An index is just a list. The S and P five hundred, for example, is a list of about five hundred "
      "of the largest companies in the United States.",
      type="photo", file="assets/photos/nyse_facade_flag.jpg", layout="full", focus=[0.5, 0.45],
      value="~500", label="large US companies, one list: the S&P 500", color="gold")
scene("An index fund simply buys every company on that list, in the same proportions, and holds them. "
      "Nobody inside the fund is trying to guess which stocks will win.",
      type="equation", title="An index fund, in one line",
      lines=[{"text": "Buy the whole list.", "color": "text", "size": 100},
             {"text": "Hold it.", "color": "green", "size": 110},
             {"text": "No guessing.", "color": "muted", "size": 80}])
scene("So who decides what's on the list? For the S and P five hundred, it's a committee at "
      "S and P Dow Jones Indices, following published rules about size, profits, and how easily the shares trade.",
      type="bullets", title="Who picks the S&P 500?",
      items=["A committee at S&P Dow Jones Indices", "Big US companies", "Recently profitable", "Shares that trade easily"])
scene("Bigger companies get a bigger slice of the fund. That's called market cap weighting, "
      "and we'll come back to why it matters.",
      type="hbars", title="Bigger company, bigger slice (illustration)", format="num",
      items=[{"label": "Giant company", "value": 100, "display": "big slice", "color": "gold"},
             {"label": "Mid-size", "value": 35, "display": "smaller", "color": "green"},
             {"label": "Smaller", "value": 10, "display": "tiny", "color": "slate"}])
scene("There are index funds for almost everything: the whole US market, stocks around the world, even bonds. "
      "In this video we'll mostly use the S and P five hundred, because that's where the best long-term data is.",
      type="stat_grid", title="Index funds can track almost any list",
      items=[{"value": "US", "label": "the whole US market", "color": "green"},
             {"value": "World", "label": "global stocks", "color": "blue"},
             {"value": "Bonds", "label": "loans to governments", "sub": "and companies", "color": "gold"}])
scene("And index funds are no longer a niche idea. By the end of 2025, index funds held fifty-two percent "
      "of the money in long-term US funds, up from just nineteen percent in 2010.",
      type="columns", title="Index funds' share of US long-term fund assets",
      items=[{"label": "2010", "value": INDEX_SHARE_2010 * 100, "display": pct(INDEX_SHARE_2010), "color": "slate"},
             {"label": "2025", "value": INDEX_SHARE_2025 * 100, "display": pct(INDEX_SHARE_2025), "color": "green"}],
      note="Index mutual funds + index ETFs · Source: ICI 2026 Fact Book")

# ---- Chapter 2
scene("Now, the other side.", type="chapter", n=2, title="The active approach")
scene("An active fund manager tries to beat the index. They research companies, buy the ones they like, "
      "skip the ones they don't, and keep trading as their views change.",
      type="photo", title="What an active manager does", file="assets/photos/stock_ticker_exchange_hall.jpg",
      layout="side", focus=[0.5, 0.4], value="Beat it?", label="Research, pick stocks, trade, review",
      sub="the goal: do better than the index", color="gold")
scene("All that research and trading costs money, so active funds charge a higher yearly fee. "
      "It's called the expense ratio.",
      type="equation", title="The expense ratio",
      lines=[{"text": "A % of your money", "color": "text", "size": 100},
             {"text": "taken every year", "color": "gold", "size": 100},
             {"text": "whether the fund wins or not", "color": "muted", "size": 64}])
scene("In 2025, the average actively managed stock mutual fund charged zero point six four percent a year. "
      "The average index stock mutual fund charged just zero point zero five percent.",
      type="versus", title="Average yearly fee, US stock mutual funds (2025)",
      left={"label": "Active", "value": pct(FEE_ACTIVE, 2), "sub": "asset-weighted average", "color": "red"},
      right={"label": "Index", "value": pct(FEE_INDEX, 2), "sub": "asset-weighted average", "color": "green"},
      verdict="Source: Investment Company Institute, March 2026")
scene("On ten thousand dollars, that's sixty-four dollars a year versus five dollars. "
      "Small numbers. But they repeat every single year.",
      type="table", title="What the fee costs you",
      header=["", "Active", "Index"],
      rows=[["Fee rate", pct(FEE_ACTIVE, 2), pct(FEE_INDEX, 2)],
            ["On $10,000", f"${PER_10K_ACTIVE:.0f} / yr", f"${PER_10K_INDEX:.0f} / yr"]],
      col_colors={"1": "red", "2": "green"})
scene("That means a manager has to beat the market by more than their fee, just to tie with the index fund. "
      "So, can they?",
      type="quote", text="To win, a manager must\nbeat the market by more\nthan their own fee.",
      first_color="gold", source="The hurdle every active fund faces")

# ---- Chapter 3
scene("Why most of them lose.", type="chapter", n=3, title="The arithmetic of losing")
scene("In 1991, Nobel prize-winning economist William Sharpe published a short paper called "
      "The Arithmetic of Active Management. Its logic is so simple, it's almost annoying.",
      type="title", title="The Arithmetic of", sub="Active Management · William F. Sharpe, 1991", sub_color="gold")
scene("Think of every dollar invested in the stock market. Some of it sits in index funds. "
      "The rest is managed actively. Together, they are the market.",
      type="equation",
      lines=[{"text": "The whole market", "color": "gold", "size": 100},
             {"text": "= index investors", "color": "green", "size": 90},
             {"text": "+ active investors", "color": "blue", "size": 90}])
scene("Say the market returns eight percent in a year. Index investors get eight percent. "
      "So the average active dollar must also earn eight percent, before costs.",
      type="stat_grid", title="Before costs (illustration)",
      items=[{"value": "8%", "label": "whole market", "color": "gold"},
             {"value": "8%", "label": "index investors", "color": "green"},
             {"value": "8%", "label": "average active $", "color": "blue"}])
scene("That makes active investing a zero-sum game before costs. "
      "For every dollar that beats the market by a point, another dollar trails it by a point.",
      type="versus", title="Before costs, it's zero-sum",
      left={"label": "One dollar", "value": "+1%", "sub": "vs the market", "color": "green"},
      right={"label": "Another dollar", "value": "−1%", "sub": "vs the market", "color": "red"},
      verdict="Average: exactly the market")
scene("But then the costs come out. Take away the average fee, and the average active dollar must earn less "
      "than the market. Not because managers are foolish. It's just arithmetic.",
      type="waterfall", title="After costs (illustration)",
      steps=[{"label": "Market return", "value": MKT, "kind": "start", "display": f"{MKT:.0f}%"},
             {"label": "Average fee", "value": FEE_ACTIVE * 100, "kind": "minus", "display": f"−{FEE_ACTIVE*100:.2f}%"},
             {"label": "Avg active dollar", "value": AVG_ACTIVE_NET, "kind": "total", "display": f"{AVG_ACTIVE_NET:.2f}%"}])
scene("And fees aren't the only cost. Active funds trade more, so they pay more trading costs. "
      "And in a regular taxable account, frequent selling can mean paying tax on gains sooner.",
      type="photo", title="Costs that quietly eat returns", file="assets/photos/wall_street_sign.jpg",
      layout="side", focus=[0.4, 0.5], value="3 costs", color="red",
      label="Yearly fees, trading costs, taxes on gains from selling")
scene("Now watch what a small fee does over a long time. Imagine one hundred thousand dollars growing for "
      "thirty years, at seven percent a year before fees. This is an illustration, not a prediction.",
      type="line", title="Index fee vs active fee: $100,000 over 30 years",
      x=list(range(0, YEARS + 1, 5)),
      series=[{"label": "Index fee", "color": "green", "values": [grow(FEE_INDEX, y) for y in range(0, YEARS + 1, 5)]},
              {"label": "", "color": "red", "values": [grow(FEE_ACTIVE, y) for y in range(0, YEARS + 1, 5)]}],
      format="usd")
scene("With the average index fee, you'd end up with about seven hundred and fifty thousand dollars. "
      "With the average active fee, about six hundred and thirty-six thousand.",
      type="hbars", title="After 30 years (illustration)", format="usd",
      items=[{"label": "Index fee", "value": END_INDEX, "display": f"${END_INDEX/1e3:,.0f}K", "color": "green"},
             {"label": "Active fee", "value": END_ACTIVE, "display": f"${END_ACTIVE/1e3:,.0f}K", "color": "red"}])
scene("That's a gap of almost one hundred and fifteen thousand dollars, "
      "from a fee difference of less than one percent a year.",
      type="count", to=FEE_GAP, prefix="$", color="red",
      label="lost to the fee gap", sub="same market, same 30 years · illustration")

# ---- Chapter 4
scene("Can't you just pick the winners?", type="chapter", n=4, title="Picking the winners")
scene("It's the obvious idea: find a fund that's been beating the market, and invest with it. "
      "S and P actually tests this, in a report called the Persistence Scorecard.",
      type="photo", title="The obvious plan", file="assets/photos/chicago_stock_exchange_board.jpg",
      layout="full", focus=[0.6, 0.4], value="Keeps winning?", color="gold",
      label="Find a recent winner, invest with it")
scene("They took the large US stock funds that ranked in the top quarter of their peers in 2021. "
      "There were one hundred and sixty-four of them.",
      type="count", to=PERSIST_TOPQ_START, color="green",
      label="large-cap funds in the top quarter in 2021", sub="S&P Persistence Scorecard, year-end 2025")
scene("How many stayed in the top quarter every year through 2025? Zero. Not one.",
      type="stat", value=str(PERSIST_TOPQ_STAYED), color="red",
      label="stayed in the top quarter every year to 2025", sub="out of 164 funds")
scene("Even just staying in the top half every year was too much. Only about four and a half percent of funds did it. "
      "Pure coin flips would give you six point two five percent.",
      type="versus", title="Staying above average, 2021 to 2025",
      left={"label": "Funds that did it", "value": pct(PERSIST_TOPHALF, 1), "sub": "large-cap, top half", "color": "red"},
      right={"label": "Coin-flip odds", "value": pct(COIN4, 2), "sub": "½ × ½ × ½ × ½", "color": "slate"},
      verdict="Worse than pure luck")
scene("A big reason is luck. In any single year, plenty of managers will beat the market partly by chance, "
      "and chance doesn't repeat on command.",
      type="equation", title="Why winners fade",
      lines=[{"text": "Skill is real.", "color": "text", "size": 96},
             {"text": "But luck is louder.", "color": "gold", "size": 110},
             {"text": "And luck doesn't repeat.", "color": "muted", "size": 72}])
scene("Funds also quietly disappear. Of the large US stock funds that existed twenty years ago, "
      "just over a third were still around by mid-2026. The rest were closed or merged away.",
      type="share", title="Large-cap US funds alive in 2006…",
      rows=[{"label": "Still around in mid-2026", "share": LC_SURVIVE_20Y, "color": "gold", "dp": 1}],
      note="Source: S&P SPIVA U.S. Scorecard, mid-year 2026")
scene("So past winners rarely stay winners. Picking a fund by its recent record is a lot closer to luck than it looks.",
      type="quote", text="Past winners\nrarely stay winners.", first_color="gold",
      source="S&P Persistence Scorecard, year-end 2025")

# ---- Chapter 5
scene("Two people made this idea famous.", type="chapter", n=5, title="Bogle and Buffett")
scene("In 1975, John Bogle founded Vanguard. On August thirty-first, 1976, it launched the first index fund "
      "for everyday investors, built to track the S and P five hundred.",
      type="timeline", title="How the index fund grew up",
      events=[{"when": "1975", "text": "Bogle founds\nVanguard"},
              {"when": "1976", "text": "First index fund\nfor everyday investors", "color": "gold"},
              {"when": "1991", "text": "Sharpe's\narithmetic", "color": "blue"},
              {"when": "2007", "text": "Buffett makes\nhis bet", "color": "gold"},
              {"when": "2025", "text": "Index funds hold\nmost fund assets"}])
scene("At first, it flopped. The goal was to raise one hundred and fifty million dollars. "
      "It raised just eleven point three million.",
      type="columns", title="The first index fund's launch, 1976",
      items=[{"label": "Target", "value": FIRST_INDEX_TARGET / 1e6, "display": "$150M", "color": "slate"},
             {"label": "Raised", "value": FIRST_INDEX_RAISED / 1e6, "display": "$11.3M", "color": "gold"}],
      note="Source: Vanguard")
scene("But the idea grew into an industry. By the end of 2025, US index mutual funds and ETFs "
      "held nineteen point one trillion dollars.",
      type="stat", value=f"${INDEX_TNA_2025/1e12:.1f}T", color="green",
      label="in US index mutual funds and ETFs", sub="year-end 2025 · Investment Company Institute")
scene("Then came Warren Buffett. In 2007, he made a one million dollar bet, for charity, "
      "that a plain S and P five hundred index fund would beat hedge fund experts over the next ten years.",
      type="photo", title="Buffett's bet", file="assets/photos/warren_buffett_2010s.jpg", layout="side",
      focus=[0.3, 0.4], value="$1M", color="gold", label="for charity, 10 years: 2008 to 2017",
      sub="one S&P 500 index fund vs hedge fund experts")
scene("His opponent, Protégé Partners, picked five funds of funds. Together, they owned stakes in more than "
      "two hundred hedge funds, and they could switch managers whenever they liked.",
      type="bullets", title="The other side of the bet",
      items=["Protégé Partners", "5 funds of funds", "200+ hedge funds inside", "Free to switch managers"], color="blue")
scene("And those funds were expensive. Buffett estimated fixed fees of around two and a half percent of assets "
      "every year, before any share of the profits.",
      type="stat", value="~" + pct(BET_FIXED_FEE, 1), color="red",
      label="yearly fixed fees, Buffett's estimate", sub="plus a share of any gains")
scene("After ten years, here's the result. The index fund gained one hundred and twenty-five point eight percent. "
      "The five funds of funds gained between two point eight and eighty-seven point seven percent.",
      type="columns", title="Total gain, 2008 to 2017", highlight=5,
      items=[{"label": f"Fund {k}", "value": v, "display": f"{v:.1f}%", "color": "blue"} for k, v in BET_FINAL.items()]
            + [{"label": "Index fund", "value": BET_INDEX_FINAL, "display": f"{BET_INDEX_FINAL:.1f}%", "color": "gold"}],
      note="Source: Berkshire Hathaway 2017 shareholder letter")
scene("Per year, the index fund made eight point five percent. The best of the five made six point five, "
      "and their average was about three.",
      type="table", title="Buffett's bet, final scorecard",
      header=["", "Total gain", "Per year"],
      rows=[["Index fund", f"{BET_INDEX_FINAL:.1f}%", f"{BET_INDEX_ANNUAL:.1f}%"],
            ["Best of the 5", f"{max(BET_FINAL.values()):.1f}%", f"{max(BET_ANNUAL.values()):.1f}%"],
            ["Average of the 5", f"{avg_final:.1f}%", f"{avg_annual:.1f}%"]],
      highlight_row=0)
scene("The prize had grown to over two point two million dollars, and it went to Girls Inc. of Omaha.",
      type="count", to=BET_DONATED, prefix="$", color="green",
      label="donated to Girls Inc. of Omaha", sub="early 2018")
scene("Buffett summed it up in his letter that year: performance comes, performance goes. Fees never falter.",
      type="quote", text="Performance comes,\nperformance goes.\nFees never falter.", first_color="text", color="gold",
      source="Warren Buffett · Berkshire Hathaway letter, 2017")

# ---- Chapter 6
scene("Now, index funds aren't perfect. Here's the honest catch.", type="chapter", n=6, title="The honest catch")
scene("First, an index fund holds everything on the list, including companies that may be overpriced. "
      "It never asks whether a stock is a bargain. It just buys it.",
      type="photo", title="No judgment, by design", file="assets/photos/nyse_facade_low_angle.jpg",
      layout="full", focus=[0.5, 0.5], value="Bubbles too", color="red",
      label="It buys the bargains… and the overpriced stocks")
scene("Second, because bigger companies get bigger slices, the S and P five hundred has become top-heavy. "
      "At the end of 2025, its ten largest companies made up about forty-one percent of the whole index.",
      type="donut", title="Weight inside the S&P 500, end of 2025", dp=1, center="S&P 500", center_sub="end of 2025",
      segments=[{"label": "10 largest companies", "value": TOP10_2025 * 100, "color": "gold"},
                {"label": "The other ~490", "value": (1 - TOP10_2025) * 100, "color": "slate"}])
scene("Between 1990 and 2015, that figure mostly sat around eighteen to twenty-three percent. "
      "So today, a lot of an S and P five hundred investor's money rides on just a few giant companies.",
      type="stat_grid", title="Weight of the 10 largest S&P 500 companies",
      items=[{"value": f"{TOP10_RANGE[0]*100:.0f}–{TOP10_RANGE[1]*100:.0f}%", "label": "typical, 1990–2015", "color": "slate"},
             {"value": pct(TOP10_2025, 1), "label": "end of 2025", "sub": "a record", "color": "gold"}])
scene("Third, you get the whole market, including the crashes. In 2008, the index fund in Buffett's bet "
      "lost thirty-seven percent. No manager steps in to protect you.",
      type="stat", value=f"−{abs(BET_INDEX_2008):.0f}%", color="red",
      label="S&P 500 index fund in 2008", sub="from Buffett's 2017 letter")
scene("And fourth, an index fund will never beat the market. By design, you get the market's return, "
      "minus a small fee.",
      type="bullets", title="The honest trade-offs",
      items=["Buys overpriced stocks too", "Top-heavy in a few giants", "Takes the full crash", "Never beats the market"],
      color="gold")
scene("Some active managers do beat the index, and a few do it for years. "
      "The hard part is spotting them before the results are in, not after.",
      type="title", title="Winners do exist", sub="finding them in advance is the hard part")

# ---- Chapter 7
scene("So what does this mean for you?", type="chapter", n=7, title="What it means for you")
scene("This isn't advice to buy any particular fund. It's about the principles the evidence points to.",
      type="equation",
      lines=[{"text": "Not a fund pick.", "color": "muted", "size": 90},
             {"text": "Principles.", "color": "gold", "size": 120}])
scene("One: costs matter. Every dollar paid in fees is a dollar that stops compounding for you. "
      "Check the expense ratio of anything you own.",
      type="count", title="1 · Costs matter", **{"from": FEE_ACTIVE * 100}, to=FEE_INDEX * 100, dp=2, suffix="%",
      color="green", label="check the expense ratio", sub="average active vs average index fee, 2025")
scene("Two: diversify. Owning a broad slice of the market means no single company can sink you, "
      "though a top-heavy index is less spread out than it looks.",
      type="versus", title="2 · Diversify",
      left={"label": "One stock", "value": "1", "sub": "one bad year can sink you", "color": "red"},
      right={"label": "Whole index", "value": "~500", "sub": "but still top-heavy", "color": "green"})
scene("Three: think long term. In twenty twenty-five alone, about four in five large-cap funds trailed the S and P five hundred. "
      "Over twenty years, more than nine in ten did.",
      type="columns", title="3 · Large-cap funds that trailed the S&P 500",
      items=[{"label": k, "value": v, "display": f"{v:.0f}%"} for k, v in LC_UNDER.items()], highlight=3,
      note="Periods ending June 30, 2026 · Source: S&P SPIVA U.S. Scorecard")
scene("And four: boring is often smart. Most of investing well is avoiding big, quiet costs, "
      "and letting time do the heavy lifting.",
      type="equation", title="4 · Boring is often smart",
      lines=[{"text": "Low costs", "color": "green", "size": 100},
             {"text": "+ broad diversification", "color": "text", "size": 84},
             {"text": "+ time", "color": "gold", "size": 110}])
scene("Here's the whole video in one line. Most professionals don't lose because they're bad at their jobs. "
      "They lose because the math of costs is working against them.",
      type="quote", text="They don't lose\nbecause they're bad.\nThe math is against them.", first_color="text",
      color="gold")
scene("If this made markets make a bit more sense, subscribe. We explain how money really works, every week.",
      type="cta", lines=["How markets", "really work."], sub="Subscribe for weekly breakdowns")

# ---------------------------------------------------------------- checks
types = [s["visual"]["type"] for s in S]
for a, b in zip(types, types[1:]):
    assert a != b, f"same visual twice in a row: {a}"
words = sum(len(s["say"].split()) for s in S)
chapters = [s["visual"]["title"] for s in S if s["visual"]["type"] == "chapter"]
assert 1400 <= words <= 1700, words
assert 45 <= len(S) <= 70, len(S)
assert 6 <= len(chapters) <= 7
assert len(set(types)) >= 10

# ---------------------------------------------------------------- spec
SOURCES = [
    "S&P Dow Jones Indices, SPIVA U.S. Mid-Year 2026 Scorecard (data to June 30, 2026): https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-mid-year-2026.pdf",
    "S&P Dow Jones Indices, SPIVA U.S. Year-End 2025 Scorecard: https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2025/",
    "S&P Dow Jones Indices, U.S. Persistence Scorecard Year-End 2025: https://www.spglobal.com/spdji/en/documents/spiva/persistence-scorecard-year-end-2025.pdf",
    "Investment Company Institute, Trends in the Expenses and Fees of Funds, 2025 (March 2026): https://www.ici.org/system/files/2026-03/per32-01.pdf",
    "Investment Company Institute, 2026 Investment Company Fact Book, ch. 2: https://icifactbook.org/pdf/2026-factbook-ch2.pdf",
    "William F. Sharpe, The Arithmetic of Active Management (Financial Analysts Journal, 1991): https://web.stanford.edu/~wfsharpe/art/active/active.htm",
    "Vanguard, 50th anniversary of the Vanguard 500 Index Fund (Aug 31, 2026): https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/press-release-50th-anniversary-vanguard-500-index-fund-083126.html",
    "Berkshire Hathaway 2017 shareholder letter (the bet): https://www.berkshirehathaway.com/letters/2017ltr.pdf",
    "RBC Wealth Management, The Great Narrowing: S&P 500 concentration (Jan 22, 2026): https://www.rbcwealthmanagement.com/en-us/insights/the-great-narrowing-sp-500-concentration",
]

DESCRIPTION = (
    "Over the 20 years to June 2026, more than 9 in 10 actively managed large-cap US stock funds trailed the "
    "S&P 500. Why do full-time professionals keep losing to a fund that does no research at all? We explain what "
    "an index fund is, William Sharpe's \"arithmetic of active management\", how a fee gap of less than 1% a year "
    "compounds over 30 years, why past winners rarely stay winners, the story of the first index fund (1976) and "
    "Warren Buffett's 10-year bet against hedge funds, and the honest weaknesses of index funds: they buy "
    "overpriced stocks too, the S&P 500 is top-heavy, and you take the full market crash.\n\n"
    "The 30-year fee example is a hypothetical illustration ($100,000, 7% a year before fees, 2025 average "
    "asset-weighted expense ratios from ICI), not a prediction. This video explains how markets work; it does not "
    "recommend any fund or security.\n\n"
    "Sources:\n" + "\n".join("- " + s for s in SOURCES) + "\n\n"
    "Not financial advice. Past performance doesn't guarantee future results.\n\n"
    "#indexfunds #investing #stockmarket #personalfinance #warrenbuffett"
)

spec = {
    "id": "L003_index_funds", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "HOW MARKETS WORK", "intro_chapter": "The 92% problem",
    "disclaimer": "Past performance doesn't guarantee future results · not investment advice",
    "title": "Why 93% of Fund Managers Lose to a Simple Index Fund",
    "thumbnail": {"big": f"{LC_UNDER['20 yrs']:.1f}%", "line": "LOST TO THE INDEX", "tag": "PRO FUNDS · 20 YEARS",
                  "color": "gold", "photo": {"file": "assets/photos/nyse_facade_low_angle.jpg", "focus": [0.45, 0.4]}},
    "description": DESCRIPTION,
    "description_sources": SOURCES,
    "tags": ["index funds", "index fund vs active fund", "S&P 500", "SPIVA", "active vs passive investing",
             "expense ratio", "John Bogle", "Warren Buffett bet", "how the stock market works", "investing for beginners",
             "personal finance", "fund fees"],
    "localizations": {
        "es": {"title": "Por qué el 93% de los gestores pierde ante un fondo indexado",
               "summary": "En los 20 años hasta junio de 2026, más de 9 de cada 10 fondos activos de grandes empresas de EE. UU. quedaron por detrás del S&P 500. "
                          "Explicamos por qué: la aritmética de William Sharpe, cómo se acumulan las comisiones en 30 años, la apuesta de Warren Buffett y las debilidades reales de los fondos indexados."},
        "pt": {"title": "Por que 93% dos gestores perdem para um fundo de índice",
               "summary": "Nos 20 anos até junho de 2026, mais de 9 em cada 10 fundos ativos de grandes empresas dos EUA ficaram atrás do S&P 500. "
                          "Explicamos por quê: a aritmética de William Sharpe, o peso das taxas em 30 anos, a aposta de Warren Buffett e as fraquezas reais dos fundos de índice."},
        "hi": {"title": "93% फंड मैनेजर एक सादे इंडेक्स फंड से क्यों हार जाते हैं",
               "summary": "जून 2026 तक के 20 सालों में अमेरिका के 10 में से 9 से ज़्यादा लार्ज-कैप एक्टिव फंड S&P 500 से पीछे रहे। "
                          "हम समझाते हैं क्यों: William Sharpe का गणित, 30 साल में फीस का असर, Warren Buffett की शर्त, और इंडेक्स फंड की असली कमज़ोरियाँ।"},
        "id": {"title": "Kenapa 93% Manajer Investasi Kalah dari Reksa Dana Indeks",
               "summary": "Dalam 20 tahun hingga Juni 2026, lebih dari 9 dari 10 reksa dana aktif saham besar AS tertinggal dari S&P 500. "
                          "Kami jelaskan sebabnya: aritmetika William Sharpe, dampak biaya selama 30 tahun, taruhan Warren Buffett, dan kelemahan nyata reksa dana indeks."},
        "de": {"title": "Warum 93% der Fondsmanager gegen einen Indexfonds verlieren",
               "summary": "In den 20 Jahren bis Juni 2026 lagen mehr als 9 von 10 aktiv gemanagten US-Large-Cap-Aktienfonds hinter dem S&P 500. "
                          "Wir erklären, warum: die Arithmetik von William Sharpe, die Wirkung von Gebühren über 30 Jahre, die Wette von Warren Buffett und die echten Schwächen von Indexfonds."},
        "fr": {"title": "Pourquoi 93 % des gérants perdent face à un fonds indiciel",
               "summary": "Sur les 20 ans jusqu'à juin 2026, plus de 9 fonds actifs américains de grandes capitalisations sur 10 ont fait moins bien que le S&P 500. "
                          "Nous expliquons pourquoi : l'arithmétique de William Sharpe, l'effet des frais sur 30 ans, le pari de Warren Buffett et les vraies faiblesses des fonds indiciels."},
    },
    "scenes": S,
}
assert len(spec["title"]) <= 100 and len(spec["thumbnail"]["big"]) <= 6 and len(spec["thumbnail"]["line"]) <= 22

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L003_index_funds.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words,", len(chapters), "chapters")
print("types:", dict(Counter(types)))
