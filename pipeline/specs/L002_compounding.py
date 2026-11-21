"""Long-form L002: compound interest and the 4 levers (amount, rate, time, leaks).

Every number below is computed here. Returns are ASSUMPTIONS for illustration (7% a year nominal),
not forecasts. Monthly contributions are made at the end of each month and grow at the monthly
rate equivalent to the stated yearly rate, so "7% a year" means exactly 7% per year.
Only one sourced figure: S&P 500 total return in 2008 (Damodaran, NYU Stern; -36.55%).
"""
import json, math, os

R = 0.07            # assumed yearly return
INFL = 0.03         # assumed yearly inflation
P, YEARS = 300, 30  # monthly base case

def fv(monthly, rate, years, step=0.0):
    """Value of `monthly` invested at each month-end for `years`; `step` raises it yearly."""
    i = (1 + rate) ** (1 / 12) - 1
    b = 0.0
    for y in range(years):
        for _ in range(12):
            b = b * (1 + i) + monthly * (1 + step) ** y
    return b

def path(monthly, rate, start_age, first_age=25, last_age=65):
    """Balance at each age from first_age..last_age, investing from start_age."""
    return [fv(monthly, rate, age - start_age) if age > start_age else 0.0
            for age in range(first_age, last_age + 1)]

def K(v):
    return f"${v / 1e3:.0f}K"

# ---------------------------------------------------------------- hook: Maya vs Sam
maya_in, sam_in = 200 * 12 * 40, 400 * 12 * 20
maya, sam = fv(200, R, 40), fv(400, R, 20)
assert maya_in == sam_in == 96_000                     # "ninety-six thousand dollars" each
assert 490e3 < maya < 500e3                             # "almost half a million"
assert 200e3 < sam < 205e3                              # "about two hundred thousand"
assert 2.4 < maya / sam < 2.5                           # "almost two and a half times as much"
ages = list(range(25, 66))
maya_path, sam_path = path(200, R, 25), path(400, R, 45)
assert abs(maya_path[-1] - maya) < 1 and abs(sam_path[-1] - sam) < 1
maya_first10 = fv(200, R, 10) * (1 + R) ** 30          # Maya's first 10 years of deposits, at 65
assert 200 * 12 * 10 == 24_000                          # "just twenty-four thousand dollars"
assert 0.5 < maya_first10 / maya < 0.55                 # "more than half of her final balance"

# ---------------------------------------------------------------- ch1: $10,000 year by year
L0 = 10_000
def bal(y):
    return L0 * (1 + R) ** y
assert round(bal(1) - L0) == 700                        # "seven hundred dollars"
assert round(bal(2) - bal(1)) == 749                    # "seven hundred and forty-nine"
assert round(bal(2) - bal(1) - 700) == 49               # "that extra forty-nine"
int30 = bal(30) - bal(29)
assert 4950 < int30 < 5000                              # "almost five thousand dollars in a single year"
simple30 = L0 + 30 * L0 * R
assert round(simple30) == 31_000                              # "thirty-one thousand dollars"
assert 76e3 < bal(30) < 76.5e3                          # "about seventy-six thousand"
assert bal(30) / simple30 > 2                           # "more than double"
yb_rows = [[str(y), f"${bal(y - 1):,.0f}", f"${bal(y) - bal(y - 1):,.0f}", f"${bal(y):,.0f}"]
           for y in (1, 2, 3, 10, 20, 30)]

# ---------------------------------------------------------------- ch2: amount
base = fv(P, R, YEARS)
base_in = P * 12 * YEARS
growth_share = (base - base_in) / base
assert base_in == 108_000                               # "one hundred and eight thousand dollars"
assert 350e3 < base < 352e3                             # "about three hundred and fifty thousand"
assert 0.68 < growth_share < 0.71                       # "about seventy percent ... is growth"
f100, f500 = fv(100, R, YEARS), fv(500, R, YEARS)
assert 116e3 < f100 < 118e3                             # "about one hundred and seventeen thousand"
assert 584e3 < f500 < 586e3                             # "about five hundred and eighty-five thousand"
assert abs(fv(600, R, YEARS) / base - 2) < 1e-9         # "double what you put in, double the result"
stepup = fv(P, R, YEARS, step=0.03)
stepup_in = sum(P * 12 * 1.03 ** y for y in range(YEARS))
assert 475e3 < stepup < 485e3                           # "about four hundred and eighty thousand"

# ---------------------------------------------------------------- ch3: rate
f3, f5, f7, f9 = (fv(P, r, YEARS) for r in (0.03, 0.05, 0.07, 0.09))
assert 173e3 < f3 < 175e3                               # "about one hundred and seventy-four thousand"
assert 244e3 < f5 < 246e3                               # "about two hundred and forty-five thousand"
assert 350e3 < f7 < 352e3                               # "three hundred and fifty-one thousand"
assert f9 > 500e3                                       # "over half a million"
assert 155e3 < f9 - f7 < 165e3                          # "about one hundred and sixty thousand dollars"
assert 0.43 < (f9 - f7) / f7 < 0.5                      # "grows by almost half"
SP500_2008 = -0.3655                                    # Damodaran, S&P 500 incl. dividends, 2008
assert -0.38 < SP500_2008 < -1 / 3                      # "lost over a third ... about thirty-seven percent"
up, down = L0 * 1.5, L0 * 1.5 * 0.5
assert (0.5 + -0.5) / 2 == 0 and down == 7_500          # "average is zero ... seven thousand five hundred"
wild_avg = (0.40 + -0.20) / 2
wild_geo = math.sqrt(1.40 * 0.80) - 1
assert abs(wild_avg - 0.10) < 1e-12                     # "averages ten percent a year"
assert 0.0575 < wild_geo < 0.0585 and wild_geo < R      # "about five point eight percent, less than seven"

# ---------------------------------------------------------------- ch4: time
def dbl(r):
    return math.log(2) / math.log(1 + r)
assert abs(dbl(0.03) - 72 / 3) < 0.6                    # "about every twenty-four years"
assert abs(dbl(0.07) - 10) < 0.3 and 10 < 72 / 7 < 10.5 # "about every ten"
assert abs(dbl(0.09) - 72 / 9) < 0.1                    # "about every eight"
d35, d45, d55, d65 = (bal(a - 25) for a in (35, 45, 55, 65))
assert 19.5e3 < d35 < 20e3                              # "about twenty thousand"
assert 38.5e3 < d45 < 39e3                              # "about thirty-nine thousand"
assert 76e3 < d55 < 76.5e3                              # "seventy-six thousand"
assert 149e3 < d65 < 150e3                              # "almost one hundred and fifty thousand"
gains = [d35 - L0, d45 - d35, d55 - d45, d65 - d55]
assert gains[3] > gains[0] + gains[1] + gains[2]        # "last decade adds more than the first three combined"
s25, s35, s45 = fv(P, R, 40), fv(P, R, 30), fv(P, R, 20)
assert 740e3 < s25 < 745e3                              # "about seven hundred and forty thousand"
assert 350e3 < s35 < 352e3                              # "about three hundred and fifty thousand"
assert 150e3 < s45 < 155e3                              # "about one hundred and fifty thousand"
assert P * 12 * 10 == 36_000                            # "only thirty-six thousand dollars in contributions"
assert s35 / s25 < 0.5                                  # "cuts your ending balance by more than half"
assert 385e3 < s25 - s35 < 395e3                        # "nearly four hundred thousand dollars"

# ---------------------------------------------------------------- ch5: leaks
fee01, fee1, fee2 = fv(P, R - 0.001, YEARS), fv(P, R - 0.01, YEARS), fv(P, R - 0.02, YEARS)
assert 343e3 < fee01 < 345e3                            # "about three hundred and forty-four thousand"
assert 291e3 < fee1 < 293e3                             # "about two hundred and ninety-two thousand"
assert 244e3 < fee2 < 246e3                             # "just two hundred and forty-five thousand"
fee_lost = base - fee1
fee_share = fee_lost / base
assert 0.16 < fee_share < 0.175                         # "about one sixth of your final balance"
assert 57e3 < fee_lost < 60e3                           # "almost sixty thousand dollars"
assert abs(dbl(INFL) - 24) < 0.6                        # "prices roughly double every twenty-four years"
infl_years = list(range(0, 31, 5))
buys = [100 / (1 + INFL) ** y for y in infl_years]
assert 41 < buys[-1] < 42                               # "$100 buys about $41 of today's stuff"
base_real = base / (1 + INFL) ** YEARS
assert 144e3 < base_real < 146e3                        # "about one hundred and forty-five thousand"
real_net = (1 + R - 0.01) / (1 + INFL) - 1
assert 0.028 < real_net < 0.031                         # "roughly three percent a year"

# ---------------------------------------------------------------- ch6: which lever wins
dbl_amt = fv(2 * P, R, YEARS)
assert 700e3 < dbl_amt < 705e3                          # "about seven hundred thousand"
assert s25 > dbl_amt                                    # "ten extra years beats doubling the amount"
assert P * 12 * 40 - base_in == 36_000                  # "thirty-six thousand dollars more"
assert 2 * P * 12 * YEARS - base_in == 108_000          # "one hundred and eight thousand more"
assert 505e3 < f9 < 515e3                               # "about five hundred and ten thousand"

print(f"Maya {maya:,.0f} Sam {sam:,.0f} ratio {maya/sam:.2f} first10 {maya_first10/maya:.0%}")
print(f"base {base:,.0f} growth {growth_share:.1%} stepup {stepup:,.0f} rates {f3:,.0f} {f5:,.0f} {f9:,.0f}")
print(f"start25 {s25:,.0f} start45 {s45:,.0f} fees {fee01:,.0f} {fee1:,.0f} {fee2:,.0f} "
      f"lost {fee_lost:,.0f} ({fee_share:.1%}) real {base_real:,.0f} realnet {real_net:.2%}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ================================================================ HOOK
scene("Two friends each invest ninety-six thousand dollars. Same investment, same returns. At sixty-five, one has about two hundred thousand dollars. The other has almost half a million.",
      type="versus", title="Same $96,000 invested",
      left={"label": "Sam", "value": K(sam), "sub": "at 65", "color": "blue"},
      right={"label": "Maya", "value": K(maya), "sub": "at 65", "color": "green"})
scene("Maya puts in two hundred dollars a month, starting at twenty-five. Sam waits until forty-five, then puts in four hundred a month to catch up. Both put in exactly ninety-six thousand dollars.",
      type="table", title="Two plans, same total",
      header=["", "Maya", "Sam"],
      rows=[["Starts at", "25", "45"], ["Each month", "$200", "$400"],
            ["Years", "40", "20"], ["Total put in", f"${maya_in:,}", f"${sam_in:,}"]],
      highlight_row=3, col_colors={"1": "green", "2": "blue"})
scene("Sam saved twice as hard, yet Maya ends up with almost two and a half times as much money. Same dollars in. The only difference was when they went in.",
      type="line", title="Balance by age (assumed 7% a year)", x=ages,
      series=[{"label": "Maya", "values": maya_path, "color": "green"},
              {"label": "Sam", "values": sam_path, "color": "blue"}])
scene("That gap is compound interest, and it comes down to just four numbers. By the end of this video, you'll know how each one works, and which one people underestimate the most.",
      type="title", title="The 4 Numbers", sub="amount · rate · time · leaks")

# ================================================================ CH1
scene("First, what compounding actually is.", type="chapter", n=1, title="What compounding is")
scene("Say you invest ten thousand dollars, and it earns seven percent a year. That rate is just an assumption for this video, not a promise. After one year, you've earned seven hundred dollars.",
      type="stat", value="$700", label="earned in year one", sub="$10,000 at an assumed 7% a year", color="green")
scene("Here's the key. In year two, you earn seven percent on ten thousand seven hundred, not just on ten thousand. So you make seven hundred and forty-nine dollars. That extra forty-nine is interest on your interest.",
      type="equation", title="Year two",
      lines=[{"text": "Year 1:  7% × $10,000 = $700", "color": "muted", "size": 76},
             {"text": "Year 2:  7% × $10,700 = $749", "color": "text", "size": 76},
             {"text": "+$49 interest on interest", "color": "gold", "size": 92}])
scene("It looks tiny. But each year's growth joins the pile, and the bigger pile earns more. By year thirty, you're earning almost five thousand dollars in a single year, without adding a cent.",
      type="table", title="$10,000 at 7% a year, nothing added",
      header=["Year", "Start", "Growth", "End"], rows=yb_rows, highlight_row=5,
      col_colors={"2": "green"})
scene("This is the compounding loop. Your money earns a return. The return is added to your balance. A bigger balance earns a bigger return. And it repeats, every single year.",
      type="flywheel", title="The compounding loop", center="REPEAT",
      steps=["Money earns", "Added to balance", "Bigger balance", "Bigger return"])
scene("Compare that with simple interest, where you only ever earn on the original ten thousand. After thirty years, simple interest gets you thirty-one thousand dollars. Compounding gets you about seventy-six thousand.",
      type="versus", title="$10,000 for 30 years at 7%",
      left={"label": "Simple interest", "value": f"${simple30:,.0f}", "sub": "earns on $10,000 only", "color": "slate"},
      right={"label": "Compound interest", "value": f"${bal(30):,.0f}", "sub": "earns on everything", "color": "green"})
scene("Same starting money, same seven percent, and more than double the result, simply because the growth was allowed to grow.",
      type="quote", text="Your money earns money.\nThen that money\nearns money too.", first_color="gold")
scene("You can write the whole thing in one line. What you end up with depends on how much you put in, the rate it grows at, how long it grows, and what leaks out along the way. Those are the four levers.",
      type="equation", title="The whole idea in one line",
      lines=[{"text": "Amount × (1 + Rate) ^ Time", "color": "gold", "size": 104},
             {"text": "where Rate is what's left after fees, taxes and inflation", "color": "muted", "size": 46}])

# ================================================================ CH2 amount
scene("Lever one: how much you put in.", type="chapter", n=2, title="Lever 1: The amount")
scene("Most people don't invest one big lump. They invest a bit every month. So let's switch to a monthly example: three hundred dollars a month, for thirty years, at the same assumed seven percent.",
      type="stat_grid", title="Our base case",
      items=[{"value": "$300", "label": "every month", "color": "gold"},
             {"value": "30", "label": "years", "color": "text"},
             {"value": "7%", "label": "a year", "sub": "assumed, not promised", "color": "green"}])
scene("You'd put in one hundred and eight thousand dollars of your own money. At the end, you'd have about three hundred and fifty thousand.",
      type="count", to=round(base), prefix="$", label="after 30 years", sub=f"you put in ${base_in:,}", color="green")
scene("That means about seventy percent of the final pile is growth. Your own contributions are the smaller slice.",
      type="donut", title="What the $351K is made of", center=K(base), center_sub="after 30 years",
      segments=[{"label": "Your money in", "value": base_in, "color": "blue"},
                {"label": "Growth", "value": base - base_in, "color": "green"}])
scene("This lever is the simplest, because it's a straight line. Double what you put in, and you double what you end up with. One hundred a month becomes about one hundred and seventeen thousand. Five hundred a month becomes about five hundred and eighty-five thousand.",
      type="columns", title="Monthly amount → value after 30 years",
      items=[{"label": "$100/mo", "value": f100, "display": K(f100)},
             {"label": "$300/mo", "value": base, "display": K(base)},
             {"label": "$500/mo", "value": f500, "display": K(f500)}], highlight=2)
scene("Small increases add up too. If you raise that three hundred by three percent every year as your income grows, you'd end with about four hundred and eighty thousand instead of three hundred and fifty.",
      type="hbars", title="$300 a month for 30 years",
      items=[{"label": "Same $300", "value": base, "display": K(base), "color": "slate"},
             {"label": "Raised 3% a year", "value": stepup, "display": K(stepup), "color": "green"}])
scene("So the lesson for lever one: you don't need a big amount to start. But whatever you add over time goes straight into the machine.",
      type="bullets", title="Lever 1 in a nutshell",
      items=["Twice the money in = twice the money out", "Start with what you can", "Raise it when your income rises"])

# ================================================================ CH3 rate
scene("Lever two: the rate of return.", type="chapter", n=3, title="Lever 2: The rate")
scene("Keep everything the same, three hundred a month for thirty years, and only change the rate. At three percent, you end with about one hundred and seventy-four thousand. At five, about two hundred and forty-five thousand. At seven, three hundred and fifty-one thousand. And at nine, over half a million.",
      type="columns", title="$300 a month for 30 years, at different rates",
      items=[{"label": f"{int(r * 100)}% a year", "value": v, "display": K(v)}
             for r, v in ((0.03, f3), (0.05, f5), (0.07, f7), (0.09, f9))], highlight=3)
scene("Notice that's not a straight line. Going from seven to nine percent adds about one hundred and sixty thousand dollars. Two percentage points, and the result grows by almost half.",
      type="equation", title="Just two percentage points",
      lines=[{"text": "7% → 9%", "color": "muted", "size": 96},
             {"text": f"+{K(f9 - f7)}", "color": "gold", "size": 140},
             {"text": f"almost half as much again (+{(f9 - f7) / f7:.0%})", "color": "text", "size": 54}])
scene("So naturally, people chase higher rates. This is where it gets risky. Higher expected returns almost always come with bigger swings. Investments that can rise faster can also fall harder.",
      type="quote", text="Higher returns\ncome with\nbigger swings.", first_color="gold")
scene("For example, in two thousand and eight, the S and P five hundred, a basket of five hundred large US companies, lost over a third of its value in a single year, even including dividends.",
      type="stat", value=f"−{abs(SP500_2008) * 100:.0f}%", label="S&P 500 in 2008", sub="total return incl. dividends · source in description", color="red")
scene("And losses hurt more than gains help. If an investment rises fifty percent and then falls fifty percent, the average return is zero. But your ten thousand dollars has turned into seven thousand five hundred.",
      type="waterfall", title="+50%, then −50%",
      steps=[{"label": "Start", "value": L0, "kind": "start", "display": "$10,000"},
             {"label": "+50%", "value": up - L0, "kind": "plus", "display": "+$5,000"},
             {"label": "−50%", "value": up - down, "kind": "minus", "display": "−$7,500"},
             {"label": "End", "value": down, "kind": "total", "display": "$7,500", "color": "red"}])
scene("So a bumpy ride grows slower than its average suggests. Up forty percent, then down twenty, again and again, averages ten percent a year. But your money only grows about five point eight percent a year. Less than a steady seven.",
      type="versus", title="What you actually keep each year",
      left={"label": "Steady", "value": "7.0%", "sub": "every year", "color": "green"},
      right={"label": "+40%, then −20%", "value": f"{wild_geo * 100:.1f}%", "sub": "even though it averages 10%", "color": "red"})
scene("And be very careful with anyone promising high returns with little or no risk. Guaranteed big returns, pressure to act fast, profits that never dip. Those are classic warning signs of a scam.",
      type="bullets", title="Red flags", color="red",
      items=["\"Guaranteed\" high returns", "Pressure to act right now", "Returns that never go down", "Can't explain how it makes money"])
scene("We're not here to tell you what to invest in. The lesson for lever two is simple: a slightly better rate is powerful, but a too-good-to-be-true rate is a trap.",
      type="title", title="Better rate: powerful", sub="too-good-to-be-true rate: a trap", sub_color="red")

# ================================================================ CH4 time
scene("Lever three: time. This is the one people underestimate the most.", type="chapter", n=4, title="Lever 3: Time")
scene("There's a handy shortcut called the Rule of seventy-two. Divide seventy-two by your yearly return, and you get roughly how many years it takes your money to double.",
      type="equation", title="The Rule of 72",
      lines=[{"text": "72 ÷ rate = years to double", "color": "text", "size": 96},
             {"text": "72 ÷ 7 ≈ 10 years", "color": "gold", "size": 120}])
scene("At three percent, money doubles about every twenty-four years. At seven percent, about every ten. At nine percent, about every eight.",
      type="stat_grid", title="Years to double your money",
      items=[{"value": "24", "label": "years", "sub": "at 3% a year", "color": "slate"},
             {"value": "~10", "label": "years", "sub": "at 7% a year", "color": "green"},
             {"value": "8", "label": "years", "sub": "at 9% a year", "color": "gold"}])
scene("So at seven percent, ten thousand dollars invested at twenty-five roughly doubles every decade. About twenty thousand by thirty-five, thirty-nine thousand by forty-five, seventy-six thousand by fifty-five, and almost one hundred and fifty thousand by sixty-five.",
      type="timeline", title="$10,000 invested once at age 25",
      events=[{"when": "Age 25", "text": "$10,000", "color": "slate"},
              {"when": "35", "text": f"${d35:,.0f}"},
              {"when": "45", "text": f"${d45:,.0f}"},
              {"when": "55", "text": f"${d55:,.0f}"},
              {"when": "65", "text": f"${d65:,.0f}", "color": "gold"}])
scene("Now look at where the growth happens. The last decade adds more than the first three decades combined. Those final years are the most powerful, and you only get them if you start early.",
      type="columns", title="Growth added in each decade",
      items=[{"label": lab, "value": g, "display": f"+${g / 1e3:.1f}K"}
             for lab, g in zip(["25 to 35", "35 to 45", "45 to 55", "55 to 65"], gains)], highlight=3)
scene("Back to monthly investing: three hundred dollars a month until sixty-five. Start at twenty-five, and you end with about seven hundred and forty thousand. Start at thirty-five, about three hundred and fifty thousand. Start at forty-five, about one hundred and fifty thousand.",
      type="table", title="$300 a month until 65",
      header=["Start at", "You put in", "Value at 65"],
      rows=[["25", f"${P * 12 * 40:,}", K(s25)], ["35", f"${P * 12 * 30:,}", K(s35)],
            ["45", f"${P * 12 * 20:,}", K(s45)]],
      highlight_row=0, col_colors={"2": "green"})
scene("Waiting ten years, from twenty-five to thirty-five, saves you only thirty-six thousand dollars in contributions. But it cuts your ending balance by more than half. That's nearly four hundred thousand dollars.",
      type="versus", title="The cost of waiting ten years",
      left={"label": "Start at 35", "value": K(s35), "sub": f"put in ${P * 12 * 30:,}", "color": "blue"},
      right={"label": "Start at 25", "value": K(s25), "sub": f"put in ${P * 12 * 40:,}", "color": "green"},
      verdict=f"Waiting costs about {K(s25 - s35)}")
scene("Remember Maya? Her first ten years of deposits, just twenty-four thousand dollars, end up as more than half of her final balance.",
      type="share", title="Maya's balance at 65",
      rows=[{"label": "From her first 10 years of deposits ($24,000)", "share": maya_first10 / maya, "color": "green"}],
      note="$200 a month from 25 to 35, left to grow at an assumed 7%")
scene("That's the real power of time. Your earliest dollars are the most valuable dollars you'll ever invest, because they get the most doublings.",
      type="quote", text="Your earliest dollars\nget the most\ndoublings.", first_color="gold")

# ================================================================ CH5 leaks
scene("Lever four: the leaks. Fees, inflation, and taxes.", type="chapter", n=5, title="Lever 4: The leaks")
scene("Fees first. A fund fee of one percent a year sounds tiny. But it's charged on your whole balance, every year, so it compounds against you.",
      type="stat", value="1%", label="a year in fees sounds tiny", sub="but it's charged on your whole balance, every year", color="red")
scene("Back to three hundred a month for thirty years. With no fees, about three hundred and fifty-one thousand. With a zero point one percent fee, about three hundred and forty-four thousand. With one percent, about two hundred and ninety-two thousand. And with two percent, just two hundred and forty-five thousand.",
      type="hbars", title="$300 a month for 30 years, assumed 7% before fees",
      items=[{"label": "No fee", "value": base, "display": K(base), "color": "green"},
             {"label": "0.1% fee", "value": fee01, "display": K(fee01), "color": "green"},
             {"label": "1% fee", "value": fee1, "display": K(fee1), "color": "gold"},
             {"label": "2% fee", "value": fee2, "display": K(fee2), "color": "red"}])
scene("So a one percent fee quietly takes about one sixth of your final balance. That's almost sixty thousand dollars, for a fee that sounded like nothing.",
      type="share", title="Lost to a 1% yearly fee",
      rows=[{"label": "Share of your final balance", "share": fee_share, "color": "red"}],
      note=f"{K(fee_lost)} on $300 a month for 30 years")
scene("Next, inflation. Prices rise over time, so a future dollar buys less than a dollar today. At three percent inflation, prices roughly double every twenty-four years. That's the Rule of seventy-two again.",
      type="line", title="What $100 buys, at 3% inflation", x=infl_years,
      series=[{"label": f"buys ${buys[-1]:.0f}", "values": buys, "color": "red"}])
scene("So the three hundred and fifty-one thousand you'd have in thirty years would only buy what about one hundred and forty-five thousand buys today. That's the difference between nominal returns, the number on your statement, and real returns, what the money can actually buy.",
      type="versus", title="Your $351K in 30 years",
      left={"label": "Nominal", "value": K(base), "sub": "the number on the statement", "color": "slate"},
      right={"label": "Real", "value": K(base_real), "sub": "in today's dollars, 3% inflation", "color": "gold"})
scene("Taxes are the third leak. Many countries offer accounts where investments can grow without being taxed every year, like retirement accounts in the US, ISAs in the UK, or tax-free savings accounts in Canada. Rules differ, so check what applies to you.",
      type="bullets", title="Tax-advantaged accounts (examples)",
      items=["US: 401(k) and IRA accounts", "UK: ISAs and pensions", "Canada: TFSA and RRSP", "Rules and limits vary by country"])
scene("Now put the leaks together. An assumed seven percent return, minus a one percent fee, minus three percent inflation, leaves a real return of roughly three percent a year.",
      type="waterfall", title="From headline return to real return",
      steps=[{"label": "Return", "value": R * 100, "kind": "start", "display": "7%", "color": "green"},
             {"label": "Fee", "value": 1.0, "kind": "minus", "display": "−1%"},
             {"label": "Inflation", "value": (R - 0.01 - real_net) * 100, "kind": "minus", "display": "−3%"},
             {"label": "Real return", "value": real_net * 100, "kind": "total", "display": f"≈{real_net * 100:.1f}%"}])

# ================================================================ CH6 which lever wins
scene("So which lever matters most? Let's line them up.", type="chapter", n=6, title="Which lever wins?")
scene("Our base case: three hundred a month for thirty years, at seven percent, with no fees, ends at about three hundred and fifty-one thousand. Now let's change just one thing at a time.",
      type="stat", value=K(base), label="our base case", sub="$300 a month · 30 years · assumed 7% · no fees", color="gold")
scene("Starting ten years earlier gets you about seven hundred and forty thousand. Doubling the monthly amount, about seven hundred thousand. Two extra points of return, about five hundred and ten thousand. And a one percent fee pulls it down to two hundred and ninety-two.",
      type="table", title="Change one thing from the base case",
      header=["Change", "Value at the end"],
      rows=[["Start 10 years earlier", K(s25)], ["Double the amount", K(dbl_amt)],
            ["Rate 7% → 9%", K(f9)], ["Add a 1% fee", K(fee1)]],
      highlight_row=0)
scene("Time wins, and look at the cost. The ten extra years add just thirty-six thousand dollars of contributions. Doubling the amount adds one hundred and eight thousand. Yet the extra years still produce the bigger result.",
      type="versus", title="Time vs effort",
      left={"label": "Double the amount", "value": K(dbl_amt), "sub": f"you put in ${2 * base_in:,}", "color": "blue"},
      right={"label": "Start 10 years earlier", "value": K(s25), "sub": f"you put in ${P * 12 * 40:,}", "color": "green"},
      verdict="Time beats effort")
scene("Here's the catch. The amount, you can raise slowly. The leaks, you can shrink. The rate is partly risk and partly luck. But time is the only lever that disappears if you don't use it.",
      type="bullets", title="The four levers",
      items=["Amount: raise it over time", "Rate: higher means riskier", "Time: can't be bought back", "Leaks: keep them small"])

# ================================================================ CH7 what to do
scene("So what does this mean for you?", type="chapter", n=7, title="What to do with this")
scene("One: start as early as you can, even if the amount feels too small to matter. Small and early beat big and late, just like Maya and Sam.",
      type="columns", title="Same $96,000 put in, value at 65",
      items=[{"label": "Maya: $200/mo from 25", "value": maya, "display": K(maya), "color": "green"},
             {"label": "Sam: $400/mo from 45", "value": sam, "display": K(sam), "color": "blue"}])
scene("Two: automate it. Set up a monthly transfer so investing happens before you can spend the money, and raise it whenever your income goes up.",
      type="timeline", title="Make it automatic",
      events=[{"when": "Payday", "text": "income lands", "color": "slate"},
              {"when": "Same day", "text": "auto-transfer\nto investments"},
              {"when": "Then", "text": "spend what's left", "color": "blue"},
              {"when": "Each raise", "text": "raise the\ntransfer", "color": "gold"}])
scene("Three: watch the costs. Check what fees you're paying, because a one percent difference can cost tens of thousands of dollars over a lifetime.",
      type="stat", value=f"−{K(fee_lost)}", label="what a 1% fee cost in our example", sub="$300 a month · 30 years · assumed 7% before fees", color="red")
scene("Four: think in real terms. Ask what your money will buy, not just how big the number looks. And stay skeptical of any promise of high, guaranteed returns.",
      type="quote", text="Ask what it will buy,\nnot how big it looks.", first_color="gold")
scene("So, the four numbers that decide your wealth: how much you put in, the rate you earn, how long you give it, and how much leaks out. Of those four, time is the one you can never get back.",
      type="equation", title="The 4 numbers",
      lines=[{"text": "Amount · Rate · Time · Leaks", "color": "text", "size": 96},
             {"text": "Time is the one you can't get back.", "color": "gold", "size": 72}])
scene("If this made compounding click, subscribe. We explain how money really works, every week. And tell us in the comments: which lever surprised you most?",
      type="cta", lines=["Make time", "work for you."], sub="Subscribe for weekly money math")

words = sum(len(s["say"].split()) for s in S)
types = [s["visual"]["type"] for s in S]
for a, b in zip(types, types[1:]):
    assert a != b, (a, b)                               # no same visual twice in a row

spec = {
    "id": "L002_compounding", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "MONEY MATH",
    "disclaimer": "Illustrations · assumed returns · not investment advice",
    "intro_chapter": "Same $96,000, very different results",
    "title": "Both Invested $96,000. One Ended Up With 2.4x More | Compound Interest Explained",
    "thumbnail": {"big": "2.4X", "line": "SAME $96K INVESTED", "tag": "THE 4 NUMBERS", "color": "gold"},
    "description": (
        "Two people each invest $96,000. One ends up with about $494,000, the other about $203,000. "
        "The difference is compound interest, and it comes down to four numbers: how much you put in, "
        "the rate, time, and the leaks (fees, inflation and taxes). We work through each one with simple "
        "examples, the Rule of 72, the real cost of a 1% fee, and nominal vs real returns.\n\n"
        "Assumptions: all returns are illustrations, not forecasts. 7% a year before fees unless stated "
        "(other rates shown for comparison), monthly contributions at the end of each month, 3% yearly "
        "inflation, fees modelled as a reduction in the yearly return, no taxes in the examples. "
        "Real investments go up and down and can lose money. Tax-advantaged account rules vary by country.\n\n"
        "Source: S&P 500 total return in 2008 (-36.55%, dividends included): Damodaran, NYU Stern, "
        "Historical Returns on Stocks, Bonds and Bills: "
        "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html\n\n"
        "For education only. Not financial advice.\n\n"
        "#compoundinterest #personalfinance #investing #ruleof72 #moneymath"
    ),
    "tags": ["compound interest", "compound interest explained", "rule of 72", "investing for beginners",
             "personal finance", "start investing early", "investment fees", "inflation", "real return",
             "money math", "financial literacy"],
    "scenes": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L002_compounding.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words,", len(set(types)), "visual types")
