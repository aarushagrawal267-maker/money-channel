"""Video 024 (global/USD): how a 1% fee compares with 0.05% over 30 years. All numbers simulated here."""
import json, os

START, MONTHLY, YEARS, GROSS = 10_000, 500, 30, 0.07
FEES = {"low": 0.0005, "high": 0.01}

def simulate(fee):
    """Monthly: add the contribution, grow at GROSS/12, then the fund takes fee/12 of the balance."""
    bal, paid, path = START, 0.0, [START]
    for m in range(1, YEARS * 12 + 1):
        bal += MONTHLY
        bal *= 1 + GROSS / 12
        f = bal * fee / 12
        paid += f; bal -= f
        if m % 12 == 0:
            path.append(bal)
    return bal, paid, path

low, low_paid, _ = simulate(FEES["low"])
high, high_paid, _ = simulate(FEES["high"])
invested = START + MONTHLY * 12 * YEARS
gap = low - high

assert invested == 190_000                    # "one hundred ninety thousand dollars of your own money"
assert 685_000 < low < 690_000, low           # "nearly six hundred and ninety thousand"
assert 560_000 < high < 565_000, high         # "about five hundred and sixty thousand"
assert 120_000 < gap < 125_000, gap           # "over a hundred and twenty thousand dollars"
assert 62_000 < high_paid < 63_000, high_paid # "over sixty-two thousand in fees"
assert 3_550 < low_paid < 3_650, low_paid     # "about thirty-six hundred"
print(f"low ${low:,.0f} (fees ${low_paid:,.0f}); high ${high:,.0f} (fees ${high_paid:,.0f}); gap ${gap:,.0f} ({gap/low:.1%})")

spec = {
    "id": "024_expense_ratio",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HIDDEN COSTS",
    "disclaimer": "Illustration · assumes 7% a year before fees · not financial advice",
    "title": "A 1% Investment Fee Can Cost You $120,000. Here's How",
    "description": (
        "Same plan, two funds: $10,000 to start plus $500 a month for 30 years. With a 0.05% yearly fee you'd end "
        f"with about ${low/1e3:,.0f}K. With a 1% fee, about ${high/1e3:,.0f}K. The gap is about "
        f"${gap/1e3:,.0f}K: the fees plus the growth those fees would have earned. A fund's yearly fee is called its "
        "expense ratio, and it's listed on the fund's fact sheet.\n\n"
        "Assumptions: 7% average yearly return before fees, compounded monthly; fees charged monthly as a share "
        "of the balance; no taxes or other costs. Illustration only: real returns vary and are not guaranteed. "
        "Not financial advice.\n\n"
        "#expenseratio #investing #indexfunds #personalfinance #moneytips"
    ),
    "tags": ["expense ratio", "investment fees", "mutual fund fees", "index funds", "investing basics",
             "personal finance", "retirement savings", "financial literacy"],
    "scenes": [
        {"say": "A one percent fee sounds tiny. On this plan, it could cost you over a hundred and twenty thousand dollars.",
         "visual": {"type": "equation", "title": "A \"tiny\" fee",
                    "lines": [{"text": "1% a year", "color": "text", "size": 110},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"−${gap/1e3:,.0f}K", "color": "red", "size": 150}]}},
        {"say": "The plan: ten thousand dollars to start, plus five hundred a month, for thirty years.",
         "visual": {"type": "equation", "title": "The plan",
                    "lines": [{"text": "$10,000 to start", "color": "text", "size": 80},
                              {"text": "+ $500 a month", "color": "text", "size": 80},
                              {"text": "for 30 years", "color": "muted", "size": 64},
                              {"text": "= $190,000 put in", "color": "gold", "size": 92}]}},
        {"say": "Assume it earns seven percent a year before fees. Real returns vary.",
         "visual": {"type": "stat", "value": "7%", "label": "assumed yearly return, before fees",
                    "sub": "real returns vary · not guaranteed", "color": "gold"}},
        {"say": "Fund A charges five hundredths of a percent a year. Fund B charges one percent.",
         "visual": {"type": "pair", "title": "Two funds, same plan",
                    "left": {"label": "A", "sub": "0.05% a year", "color": "green"},
                    "right": {"label": "B", "sub": "1% a year", "color": "red"}}},
        {"say": "After thirty years: Fund A, nearly six hundred and ninety thousand. Fund B, about five hundred and sixty.",
         "visual": {"type": "compare", "title": "After 30 years",
                    "left": {"label": "Fund A", "value": low, "color": "green"},
                    "right": {"label": "Fund B", "value": high, "color": "red"}}},
        {"say": "Fund B takes over sixty-two thousand in fees. Fund A, about thirty-six hundred.",
         "visual": {"type": "bars", "title": "Fees paid over 30 years",
                    "items": [{"label": "Fund A", "value": low_paid, "color": "green"},
                              {"label": "Fund B", "value": high_paid, "color": "red"}]}},
        {"say": "That's over a hundred and twenty thousand dollars, gone to fees and the growth they took with them.",
         "visual": {"type": "stat", "value": f"${gap/1e3:,.0f}K", "label": "lost to the higher fee",
                    "sub": "fees + the growth they would have earned", "color": "red"}},
        {"say": "That yearly fee is called the expense ratio. Check it on the fund's fact sheet before you invest.",
         "visual": {"type": "equation", "title": "Before you invest",
                    "lines": [{"text": "Check the", "color": "muted", "size": 72},
                              {"text": "EXPENSE RATIO", "color": "gold", "size": 104},
                              {"text": "on the fund's fact sheet", "color": "muted", "size": 56}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Small fees.", "Big bills."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "024_expense_ratio.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
