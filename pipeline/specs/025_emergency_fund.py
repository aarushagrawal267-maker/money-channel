"""Video 025 (global/USD): emergency fund, how much and where. Numbers computed or sourced here."""
import json, os

ESSENTIALS = 3_000                      # example: essential spending per month
low, high = 3 * ESSENTIALS, 6 * ESSENTIALS
FDIC = 250_000                          # FDIC standard insurance amount (fdic.gov)
# S&P 500 closing high 3,386.15 on 19 Feb 2020 to close of 2,237.40 on 23 Mar 2020 (S&P Dow Jones Indices)
SP_HI, SP_LO = 3386.15, 2237.40
drop = 1 - SP_LO / SP_HI
after = high * (1 - drop)

assert low == 9_000 and high == 18_000          # "nine thousand to eighteen thousand"
assert 0.33 < drop < 0.35, drop                 # "about a third"
assert 11_800 < after < 12_000, after           # "about twelve thousand"
assert FDIC == 250_000                          # "two hundred fifty thousand dollars"
print(f"fund ${low:,}-${high:,}; 2020 drop {drop:.1%}; $18,000 -> ${after:,.0f}")

spec = {
    "id": "025_emergency_fund",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "SAFETY NET",
    "disclaimer": "Example · $3,000/month of essentials · not financial advice",
    "title": "Emergency fund: how much you need, and where to keep it #shorts",
    "description": (
        "A common guideline is 3 to 6 months of essential expenses. With $3,000 a month of essentials, that's "
        "$9,000 to $18,000. Keep it somewhere safe and easy to reach, like a high-yield savings account at an "
        "FDIC-insured bank, not in the stock market, which can fall right when you need the cash.\n\n"
        "Example: $3,000 a month of essentials (rent, food, bills, insurance, transport). "
        "Sources: FDIC standard deposit insurance is $250,000 per depositor, per insured bank, per ownership "
        "category (fdic.gov). The S&P 500 fell about 34% from its 19 Feb 2020 close to its 23 Mar 2020 close "
        "(S&P Dow Jones Indices). Savings rates change often; check the current rate before opening an account. "
        "Not financial advice.\n\n"
        "#emergencyfund #personalfinance #savings #moneytips #budgeting"
    ),
    "tags": ["emergency fund", "high yield savings account", "savings", "personal finance", "budgeting",
             "FDIC", "money tips", "financial literacy"],
    "scenes": [
        {"say": "If your paycheck stopped tomorrow, how many months could you last?",
         "visual": {"type": "equation", "title": "Paycheck stops.",
                    "lines": [{"text": "How many months", "color": "text", "size": 96},
                              {"text": "could you last?", "color": "gold", "size": 110}]}},
        {"say": "The common guideline: keep three to six months of essential expenses. Rent, food, bills, insurance, getting to work.",
         "visual": {"type": "stat", "value": "3–6", "label": "months of essential expenses",
                    "sub": "the common guideline", "color": "gold"}},
        {"say": "If your essentials cost three thousand dollars a month, that's nine thousand to eighteen thousand dollars.",
         "visual": {"type": "bars", "title": "At $3,000 a month",
                    "items": [{"label": "3 months", "value": low, "color": "blue"},
                              {"label": "6 months", "value": high, "color": "green"}]}},
        {"say": "Where should it live? Not in the stock market. In early twenty twenty, US stocks fell about a third in about a month, just as millions lost their jobs.",
         "visual": {"type": "compare", "title": "$18,000 in stocks, 2020",
                    "left": {"label": "February", "value": high, "color": "text"},
                    "right": {"label": "March", "value": after, "color": "red"}}},
        {"say": "Keep it in a high-yield savings account at a bank insured by the FDIC. Deposits are covered up to two hundred fifty thousand dollars, per depositor, per bank.",
         "visual": {"type": "pair", "title": "Where it lives",
                    "left": {"label": "Savings", "sub": "insured · steady", "color": "green"},
                    "right": {"label": "Market", "sub": "can drop fast", "color": "red"}}},
        {"say": "It earns some interest, and you can move it to checking in a day or two.",
         "visual": {"type": "equation", "title": "High-yield savings",
                    "lines": [{"text": "FDIC insured", "color": "green", "size": 88},
                              {"text": "earns interest", "color": "text", "size": 88},
                              {"text": "cash in 1–2 days", "color": "gold", "size": 88}]}},
        {"say": "Starting from zero? Aim for one month first. Then build.",
         "visual": {"type": "stat", "value": "1 month", "label": "a great first goal",
                    "sub": f"= ${ESSENTIALS:,} in this example", "color": "green"}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Build your", "safety net."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "025_emergency_fund.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
