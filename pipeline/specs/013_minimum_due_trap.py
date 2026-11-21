"""Video 013: Credit card minimum-due trap. All numbers simulated here."""
import json, os

BAL0, RATE, GST, MINPCT, FLOOR = 50000, 0.035, 0.18, 0.05, 200

def simulate(fixed=None):
    """Monthly: pay (minimum due or fixed amount), then interest + GST accrue on what's left.
    Returns months, total interest, balance at the end of each year."""
    bal, months, interest, yearly = BAL0, 0, 0.0, [BAL0]
    while bal > 0.5 and months < 1200:
        pay = min(bal, fixed if fixed else max(bal * MINPCT, FLOOR))
        bal -= pay
        i = bal * RATE * (1 + GST)
        bal += i; interest += i; months += 1
        if months % 12 == 0:
            yearly.append(bal)
    yearly.append(0)
    return months, interest, yearly

m_min, int_min, bal_min = simulate()
m_fix, int_fix, bal_fix = simulate(fixed=5000)
years_min = m_min / 12
yearly_rate_simple = RATE * 12 * (1 + GST)

assert abs(yearly_rate_simple - 0.4956) < 0.001          # "nearly fifty percent a year"
assert 22 <= years_min < 24, years_min                  # "over twenty-two years"
assert 1.7e5 < int_min < 1.8e5, int_min                 # "about one point seven lakh"
assert int_min / BAL0 > 3.3                             # "more than three times what you borrowed"
assert m_fix == 13, m_fix                               # "thirteen months"
assert 1.2e4 < int_fix < 1.3e4, int_fix                 # "about twelve thousand"
print(f"min-only: {m_min} months ({years_min:.1f} y), interest {int_min:,.0f}; "
      f"fixed 5000: {m_fix} months, interest {int_fix:,.0f}")

years = list(range(len(bal_min)))
fix_series = [bal_fix[i] if i < len(bal_fix) else 0 for i in years]

spec = {
    "id": "013_minimum_due_trap",
    "currency": "inr", "voice": "af_heart", "speed": 1.06,
    "badge": "MONEY TRAP",
    "disclaimer": "Illustration · 3.5%/month + 18% GST · 5% minimum due · no new spends · terms vary by bank",
    "title": "Paying only the minimum on your credit card? Watch this. #shorts",
    "description": (
        "A ₹50,000 credit card bill. Pay only the minimum due and it can take over 22 years "
        "and about ₹1.7 lakh in interest to clear. Pay ₹5,000 a month and it's gone in 13 months.\n\n"
        "Assumptions: 3.5% monthly interest + 18% GST on interest, minimum due = 5% of the "
        "outstanding balance (minimum ₹200), no new spending. Interest rates and minimum-due "
        "formulas vary by bank; check your card's terms. Not financial advice.\n\n"
        "#creditcard #personalfinance #moneytips #debt #financialliteracy"
    ),
    "tags": ["credit card", "minimum due", "credit card interest", "personal finance india",
             "debt trap", "money tips", "financial literacy", "credit card tips"],
    "scenes": [
        {"say": "Your credit card bill is fifty thousand rupees. But the app says you can just pay the minimum: two thousand five hundred.",
         "visual": {"type": "compare", "title": "Your card statement",
                    "left": {"label": "Total due", "value": BAL0, "color": "text"},
                    "right": {"label": "Minimum due", "value": BAL0 * MINPCT, "color": "gold"}}},
        {"say": "Most cards in India charge around three and a half percent interest every month, plus eighteen percent GST on that interest.",
         "visual": {"type": "stat", "value": "3.5%", "label": "interest per month",
                    "sub": "+ 18% GST on the interest", "color": "red"}},
        {"say": "That's nearly fifty percent a year.",
         "visual": {"type": "stat", "value": "~50%", "label": "per year", "color": "red"}},
        {"say": "If you only ever pay the minimum, clearing that fifty thousand takes over twenty-two years.",
         "visual": {"type": "stat", "value": f"{years_min:.0f} yrs", "label": "to clear ₹50,000",
                    "sub": "paying only the minimum", "color": "red"}},
        {"say": "And you'd pay about one point seven lakh in interest. More than three times what you spent.",
         "visual": {"type": "equation",
                    "lines": [{"text": "Spent: ₹50,000", "color": "muted", "size": 80},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"Interest: ₹{int_min/1e5:.1f} L", "color": "red", "size": 100}]}},
        {"say": "Now pay a fixed five thousand every month instead. The debt is gone in thirteen months.",
         "visual": {"type": "line", "title": "Balance left (₹)", "x": years, "x_label": "years",
                    "series": [{"label": "Minimum only", "values": bal_min, "color": "red"},
                               {"label": "₹5,000/month", "values": fix_series, "color": "green"}]}},
        {"say": "Total interest? About twelve thousand, instead of one point seven lakh.",
         "visual": {"type": "bars", "title": "Total interest paid",
                    "items": [{"label": "Minimum", "value": int_min, "color": "red"},
                              {"label": "₹5,000/mo", "value": int_fix, "color": "green"}]}},
        {"say": "The rule is simple. Always pay the full bill. If you can't, pay as much as you can, and stop using the card until it's clear.",
         "visual": {"type": "equation", "title": "The rule",
                    "lines": [{"text": "Pay the FULL bill", "color": "green", "size": 92},
                              {"text": "Can't? Pay the most you can", "color": "text", "size": 56},
                              {"text": "+ pause the card", "color": "muted", "size": 56}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Never pay", "just the minimum."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "013_minimum_due_trap.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
