"""Video 015 (global/USD): the Rule of 72. Every number computed and checked here."""
import json, math, os

RATES = [4, 7, 10]                      # % per year, compounded yearly
rule = {r: 72 / r for r in RATES}       # Rule of 72 estimate (years to double)
exact = {r: math.log(2) / math.log(1 + r / 100) for r in RATES}

assert rule[4] == 18                                  # "eighteen years"
assert 10 < rule[7] < 10.5                            # "about ten years" (10.3)
assert rule[10] == 7.2                                # "just over seven"
assert round(exact[4], 1) == 17.7                     # "seventeen point seven"
assert round(exact[7], 1) == 10.2                     # "ten point two"
assert round(exact[10], 1) == 7.3                     # "seven point three"
assert all(abs(rule[r] - exact[r]) < 0.35 for r in RATES)   # "very close" (under 4 months off)

# $1,000 left to compound for 30 years at each rate
P, YEARS = 1000, 30
years = list(range(YEARS + 1))
paths = {r: [P * (1 + r / 100) ** y for y in years] for r in RATES}
end = {r: paths[r][-1] for r in RATES}
assert 3200 < end[4] < 3300                           # "about three thousand two hundred"
assert 7500 < end[7] < 7700                           # "about seven and a half thousand"
assert 17000 < end[10] < 18000                        # "over seventeen thousand"
assert 4 < YEARS / exact[10] < 4.2                    # "doubles four times" at 10%

# Works for prices too: 3% inflation
INF = 3
assert 72 / INF == 24                                 # "about twenty-four years"
assert 23 < math.log(2) / math.log(1 + INF / 100) < 24
print({r: (round(rule[r], 2), round(exact[r], 2), round(end[r])) for r in RATES})

f1 = lambda x: f"{x:.1f}"
spec = {
    "id": "015_rule_of_72",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "disclaimer": "Illustration · yearly compounding · returns not guaranteed · not financial advice",
    "title": "Rule of 72: How Fast Does Your Money Double?",
    "description": (
        "Divide 72 by your yearly return and you get roughly how many years your money takes to double. "
        "At 4% that's 18 years, at 7% about 10, at 10% about 7.2. The exact answers (17.7, 10.2 and 7.3 years) "
        "are very close.\n\n"
        "Assumptions: returns compounded once a year; $1,000 example left untouched for 30 years. "
        "Rates are examples only: real returns vary and are not guaranteed. Not financial advice.\n\n"
        "#ruleof72 #compoundinterest #personalfinance #investing #moneytips"
    ),
    "tags": ["rule of 72", "compound interest", "doubling time", "money math", "personal finance",
             "investing basics", "inflation", "financial literacy"],
    "scenes": [
        {"say": "How long does it take for your money to double? There's a trick that answers it in about one second.",
         "visual": {"type": "equation", "title": "The question",
                    "lines": [{"text": "$1,000 → $2,000", "color": "green", "size": 100},
                              {"text": "how many years?", "color": "muted", "size": 64}]}},
        {"say": "It's called the Rule of seventy-two. Divide seventy-two by your yearly return. The answer is roughly how many years it takes.",
         "visual": {"type": "equation", "title": "The Rule of 72",
                    "lines": [{"text": "72 ÷ return %", "color": "gold", "size": 110},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": "≈ years to double", "color": "text", "size": 76}]}},
        {"say": "At four percent, seventy-two divided by four is eighteen years.",
         "visual": {"type": "stat", "value": "18 yrs", "label": "to double at 4% a year",
                    "sub": "72 ÷ 4 = 18", "color": "gold"}},
        {"say": "At seven percent, about ten years. At ten percent, just over seven.",
         "visual": {"type": "bars", "title": "Years to double", "format": "num",
                    "items": [{"label": "at 4%", "value": rule[4], "color": "slate"},
                              {"label": "at 7%", "value": rule[7], "color": "blue"},
                              {"label": "at 10%", "value": rule[10], "color": "green"}]}},
        {"say": "Is it accurate? The exact answers are seventeen point seven, ten point two, and seven point three years. Very close.",
         "visual": {"type": "equation", "title": "Rule vs exact",
                    "lines": [{"text": "rule  ·  exact", "color": "muted", "size": 56},
                              {"text": f"4%:  {f1(rule[4])}  ·  {f1(exact[4])}", "color": "text", "size": 84},
                              {"text": f"7%:  {f1(rule[7])}  ·  {f1(exact[7])}", "color": "text", "size": 84},
                              {"text": f"10%:  {f1(rule[10])}  ·  {f1(exact[10])}", "color": "green", "size": 84}]}},
        {"say": "And doubling stacks. At ten percent, money doubles about four times in thirty years. One thousand dollars becomes over seventeen thousand.",
         "visual": {"type": "line", "title": "$1,000 over 30 years", "x": years, "x_label": "years",
                    "series": [{"label": "10%", "values": paths[10], "color": "green"},
                               {"label": "7%", "values": paths[7], "color": "blue"},
                               {"label": "4%", "values": paths[4], "color": "slate"}]}},
        {"say": "It works on prices too. At three percent inflation, prices double in about twenty-four years.",
         "visual": {"type": "stat", "value": "24 yrs", "label": "for prices to double at 3% inflation",
                    "sub": "72 ÷ 3 = 24", "color": "red"}},
        {"say": "Seventy-two, divided by the rate. Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["72 ÷ rate", "= years to 2×"],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "015_rule_of_72.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
