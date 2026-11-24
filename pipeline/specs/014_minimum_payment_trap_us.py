"""Video 014 (global/US): the credit card minimum-payment trap. All numbers simulated here."""
import json, os

BAL0, APR, FLOOR, PCT = 5000, 0.22, 35, 0.01
r = APR / 12

def simulate(fixed=None):
    """Monthly: interest accrues, then pay (minimum or fixed). Minimum = 1% of balance + interest, $35 floor."""
    bal, months, interest, yearly, first_min = BAL0, 0, 0.0, [BAL0], None
    while bal > 0.5 and months < 1200:
        i = bal * r
        interest += i; bal += i
        due = max(FLOOR, (bal - i) * PCT + i)
        first_min = first_min or due
        bal -= min(bal, fixed if fixed else due)
        months += 1
        if months % 12 == 0:
            yearly.append(bal)
    yearly.append(0)
    return months, interest, yearly, first_min

m_min, int_min, bal_min, first_min = simulate()
m_fix, int_fix, bal_fix, _ = simulate(fixed=300)

assert 140 <= first_min <= 143, first_min        # "about a hundred and forty dollars"
assert 16 <= m_min / 12 < 16.5, m_min           # "sixteen years"
assert 7500 < int_min < 8000, int_min           # "over seven and a half thousand"
assert 1.45 < int_min / BAL0 < 1.55             # "one and a half times what you spent"
assert m_fix < 24, m_fix                        # "under two years"
assert 950 < int_fix < 1100, int_fix            # "about one thousand dollars"
print(f"first min ${first_min:.0f}; min-only {m_min} mo, ${int_min:,.0f}; $300/mo {m_fix} mo, ${int_fix:,.0f}")

years = list(range(len(bal_min)))
fix_series = [bal_fix[i] if i < len(bal_fix) else 0 for i in years]

spec = {
    "id": "014_minimum_payment_trap_us",
    "currency": "usd", "voice": "af_heart", "speed": 1.06,
    "badge": "MONEY TRAP",
    "disclaimer": "Illustration · 22% APR · minimum = 1% + interest ($35 floor) · no new spending",
    "title": "Credit Card Minimum Payment Trap: $5,000 Takes 16 Years",
    "description": (
        "A $5,000 credit card balance at 22% APR. Pay only the minimum and it takes about 16 years "
        "and over $7,500 in interest to clear. Pay $300 a month and it's gone in 21 months for about $1,000.\n\n"
        "Assumptions: 22% APR (close to the 2026 US average for cards charging interest), minimum payment = "
        "1% of balance + interest with a $35 floor, no new purchases. Minimum-payment formulas vary by card issuer; "
        "check your statement. Not financial advice.\n\n"
        "#creditcard #personalfinance #debt #moneytips #financialliteracy"
    ),
    "tags": ["credit card", "minimum payment", "credit card debt", "APR", "personal finance",
             "debt payoff", "money tips", "financial literacy"],
    "scenes": [
        {"say": "Your credit card balance is five thousand dollars. But the minimum payment? Only about a hundred and forty.",
         "visual": {"type": "compare", "title": "Your card statement",
                    "left": {"label": "Balance", "value": BAL0, "color": "text"},
                    "right": {"label": "Minimum due", "value": first_min, "color": "gold"}}},
        {"say": "The average card that charges interest is now around twenty-two percent a year.",
         "visual": {"type": "stat", "value": "22%", "label": "average APR",
                    "sub": "on cards charging interest · 2026", "color": "red"}},
        {"say": "Pay only the minimum, and that five thousand takes sixteen years to clear.",
         "visual": {"type": "stat", "value": "16 yrs", "label": "to clear $5,000",
                    "sub": "paying only the minimum", "color": "red"}},
        {"say": "You'd pay over seven and a half thousand dollars in interest. One and a half times what you spent.",
         "visual": {"type": "equation",
                    "lines": [{"text": "Spent: $5,000", "color": "muted", "size": 84},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"Interest: ${int_min:,.0f}", "color": "red", "size": 100}]}},
        {"say": "Now pay a fixed three hundred a month instead. The debt is gone in under two years.",
         "visual": {"type": "line", "title": "Balance left", "x": years, "x_label": "years",
                    "series": [{"label": "Minimum only", "values": bal_min, "color": "red"},
                               {"label": "$300/month", "values": fix_series, "color": "green"}]}},
        {"say": "Total interest? About one thousand dollars, instead of over seven and a half.",
         "visual": {"type": "bars", "title": "Total interest paid",
                    "items": [{"label": "Minimum", "value": int_min, "color": "red"},
                              {"label": "$300/mo", "value": int_fix, "color": "green"}]}},
        {"say": "The rule is simple. Pay the full balance every month. If you can't, pay as much as you can, and stop using the card until it's clear.",
         "visual": {"type": "equation", "title": "The rule",
                    "lines": [{"text": "Pay it IN FULL", "color": "green", "size": 96},
                              {"text": "Can't? Pay the most you can", "color": "text", "size": 56},
                              {"text": "+ pause the card", "color": "muted", "size": 56}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Never pay", "just the minimum."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "014_minimum_payment_trap_us.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
