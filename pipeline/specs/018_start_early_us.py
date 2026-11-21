"""Video 018 (global/USD remake of 001): same $300/month, start at 25 vs 35. All numbers computed here."""
import json, os

MONTHLY, ANNUAL, END = 300, 0.07, 65
r = ANNUAL / 12

def fv(months):
    """Future value of a monthly investment made at the start of each month, compounded monthly."""
    return MONTHLY * (((1 + r) ** months - 1) / r) * (1 + r) if months > 0 else 0

ages = list(range(25, END + 1))
maya = [fv((a - 25) * 12) for a in ages]
jake = [fv(max(0, (a - 35) * 12)) for a in ages]
M65, J65 = maya[-1], jake[-1]
M_inv, J_inv = MONTHLY * 12 * (END - 25), MONTHLY * 12 * (END - 35)

# sanity checks behind every spoken / shown claim
assert 785_000 < M65 < 800_000, M65          # "about seven hundred and ninety thousand"
assert 360_000 < J65 < 370_000, J65          # "under three hundred and seventy thousand"
assert M_inv == 144_000 and J_inv == 108_000 # "one hundred forty-four thousand" / "one hundred eight"
assert M_inv - J_inv == 36_000               # "just thirty-six thousand more"
assert M65 - J65 > 400_000                   # "over four hundred thousand more"
assert abs(maya[ages.index(55)] - J65) < 1   # Maya at 55 == Jake at 65
assert M65 / J65 > 2                         # "more than double"; also "less than half" (scene 8)
print(f"M65={M65:,.0f} J65={J65:,.0f} diff={M65 - J65:,.0f}")

spec = {
    "id": "018_start_early_us",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "INVESTING BASICS",
    "disclaimer": "Illustration · assumes 7% a year · returns vary · not financial advice",
    "title": f"Same $300 a month. ${M65/1e3:.0f}K vs ${J65/1e3:.0f}K. Why? #shorts",
    "description": (
        "Two friends invest the same $300 every month. One starts at 25, the other at 35. "
        f"At 65, one has about ${M65/1e3:,.0f}K and the other about ${J65/1e3:,.0f}K, "
        "even though the gap in money put in is only $36,000.\n\n"
        "Assumptions: $300 invested at the start of every month until age 65, an assumed 7% average yearly "
        "return compounded monthly, no fees or taxes. Illustration only: real returns vary year to year, "
        "can be negative, and are not guaranteed. Not financial advice.\n\n"
        "#investing #compoundinterest #personalfinance #retirement #moneytips"
    ),
    "tags": ["compound interest", "start investing early", "investing for beginners", "retirement savings",
             "personal finance", "money tips", "financial literacy", "power of compounding"],
    "scenes": [
        {"say": "Two friends invest the same three hundred dollars a month. One ends up with more than double.",
         "visual": {"type": "pair", "title": "Same amount. Same return.",
                    "left": {"label": "Maya", "sub": "$300 / month", "color": "green"},
                    "right": {"label": "Jake", "sub": "$300 / month", "color": "slate"}}},
        {"say": "At sixty-five, Maya has about seven hundred and ninety thousand dollars. Jake? Under three hundred and seventy thousand.",
         "visual": {"type": "compare", "title": "Money at age 65",
                    "left": {"label": "Maya", "value": M65, "color": "green"},
                    "right": {"label": "Jake", "value": J65, "color": "slate"}}},
        {"say": "The only difference: Maya started at twenty-five. Jake waited until thirty-five.",
         "visual": {"type": "timeline", "title": "The only difference", "start": 25, "end": END,
                    "rows": [{"label": "Maya", "from": 25, "color": "green"},
                             {"label": "Jake", "from": 35, "color": "slate"}]}},
        {"say": "Both earn an assumed seven percent a year. Real returns vary, and some years are negative.",
         "visual": {"type": "stat", "value": "7%", "label": "assumed average yearly return",
                    "sub": "real returns vary · not guaranteed", "color": "gold"}},
        {"say": "Maya puts in one hundred and forty-four thousand dollars. Jake puts in one hundred and eight thousand.",
         "visual": {"type": "bars", "title": "Money put in",
                    "items": [{"label": "Maya", "value": M_inv, "color": "green"},
                              {"label": "Jake", "value": J_inv, "color": "slate"}]}},
        {"say": "Just thirty-six thousand more, but Maya ends up with over four hundred thousand more.",
         "visual": {"type": "equation",
                    "lines": [{"text": "+$36K put in", "color": "muted", "size": 84},
                              {"text": "↓", "color": "dim", "size": 84},
                              {"text": f"+${(M65 - J65)/1e3:,.0f}K at 65", "color": "green", "size": 110}]}},
        {"say": "By fifty-five, Maya already has what Jake ends with at sixty-five. Ten years early.",
         "visual": {"type": "line", "title": "Growth by age", "x": ages, "x_label": "age",
                    "series": [{"label": "Maya", "values": maya, "color": "green"},
                               {"label": "Jake", "values": jake, "color": "slate"}],
                    "hline": {"value": J65, "label": "Jake at 65 = Maya at 55", "x": 55, "at": 2.2}}},
        {"say": "Compounding saves its biggest gains for the end. Waiting doesn't just delay them, it cuts them off.",
         "visual": {"type": "equation", "title": "What waiting costs",
                    "lines": [{"text": "10 years late", "color": "text", "size": 96},
                              {"text": "=", "color": "dim", "size": 80},
                              {"text": "less than half", "color": "red", "size": 110}]}},
        {"say": "Start when you can, even small. Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Start early.", "Even small."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "018_start_early_us.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
