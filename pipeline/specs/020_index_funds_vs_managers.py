"""Video 020 (global/US): most active large-cap funds trail the S&P 500 over the long run. Pillar: How Markets Work."""
import json, os

# ---------------------------------------------------------------- sourced facts
# S&P Dow Jones Indices, SPIVA U.S. Scorecard Mid-Year 2026 (data to June 30, 2026), Report 1a,
# "All Large-Cap Funds vs S&P 500", % of funds underperforming. The primary PDF blocks automated fetches;
# figures as reproduced by several independent summaries (and identical to the constants in L003_index_funds.py),
# checked 2026-11-21: 10 yrs 83.33%, 15 yrs 90.49%, 20 yrs 92.61%.
UNDER = {10: 83.33, 15: 90.49, 20: 92.61}
# Morningstar, "2026 US Fund Fee Study" (May 2026, data to Dec 31, 2025), Key Takeaways:
# asset-weighted average fee in 2025: broad index funds 0.09%, actively managed funds 0.57%.
FEE_ACTIVE, FEE_INDEX = 0.0057, 0.0009

# ---------------------------------------------------------------- checks behind spoken claims
pct = {y: round(v) for y, v in UNDER.items()}
assert pct == {10: 83, 15: 90, 20: 93}, pct        # "eighty-three ... ninety ... ninety-three percent"
BAL = 10_000
fee_active, fee_index = BAL * FEE_ACTIVE, BAL * FEE_INDEX
assert round(fee_active) == 57 and round(fee_index) == 9   # "fifty-seven dollars versus nine"
assert fee_active / fee_index > 6                          # active costs over six times more
print({y: f"{v}%" for y, v in UNDER.items()}, f"fees ${fee_active:.0f} vs ${fee_index:.0f}")

spec = {
    "id": "020_index_funds_vs_managers",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": "Past results don't guarantee future ones · not financial advice",
    "title": "93% of Fund Managers Lose to the S&P 500. Here's Why",
    "description": (
        "S&P's SPIVA scorecard compares actively managed funds with their benchmark. Through June 30, 2026, "
        "83% of US large-cap funds trailed the S&P 500 over 10 years, 90% over 15 years and 93% over 20 years. "
        "A big reason is cost: in 2025 the average actively managed fund charged about 0.57% a year versus "
        "0.09% for broad index funds (asset-weighted).\n\n"
        "Sources: S&P Dow Jones Indices, SPIVA U.S. Scorecard Mid-Year 2026, Report 1a (data to June 30, 2026); "
        "Morningstar 2026 US Fund Fee Study (May 2026, data to Dec 31, 2025). Past performance doesn't guarantee "
        "future results. Not financial advice.\n\n"
        "#indexfunds #investing #stockmarket #sp500 #personalfinance"
    ),
    "tags": ["index funds", "spiva", "active vs passive", "s&p 500", "fund managers", "expense ratio",
             "investing basics", "stock market", "personal finance"],
    "scenes": [
        {"say": "Ninety-three percent of US large-cap fund managers trailed the S&P five hundred over the last twenty years.",
         "visual": {"type": "stat", "value": "93%", "label": "of large-cap funds trailed the S&P 500",
                    "sub": "20 years to June 2026 · S&P SPIVA scorecard", "color": "red"}},
        {"say": "That's from S&P's SPIVA scorecard. And it's not a fluke. Over ten years, eighty-three percent fell behind. Over fifteen, ninety percent.",
         "visual": {"type": "bars", "title": "% that trailed the S&P 500", "format": "num",
                    "items": [{"label": "10 yrs", "value": pct[10], "color": "gold"},
                              {"label": "15 yrs", "value": pct[15], "color": "gold"},
                              {"label": "20 yrs", "value": pct[20], "color": "red"}]}},
        {"say": "Why? An S&P five hundred index fund simply holds the companies in the index. No stock picking, no star manager to pay.",
         "visual": {"type": "pair", "title": "Two ways to invest",
                    "left": {"label": "Index", "sub": "holds it all", "color": "green"},
                    "right": {"label": "Active", "sub": "picks stocks", "color": "slate"}}},
        {"say": "In twenty twenty-five, active funds charged about zero point five seven percent a year on average. Broad index funds, about zero point zero nine. On ten thousand dollars, that's fifty-seven dollars versus nine, every year.",
         "visual": {"type": "compare", "title": "Yearly fee on $10,000",
                    "left": {"label": "Active fund", "value": fee_active, "color": "red"},
                    "right": {"label": "Index fund", "value": fee_index, "color": "green"}}},
        {"say": "So to win, a manager must beat the market by more than their fee, year after year. Over decades, very few do.",
         "visual": {"type": "equation", "title": "To win, a manager must",
                    "lines": [{"text": "Beat the market", "color": "text", "size": 92},
                              {"text": "+ cover the fee", "color": "gold", "size": 80},
                              {"text": "for decades", "color": "muted", "size": 64}]}},
        {"say": "There's a new one every day. Follow so you don't miss it.",
         "visual": {"type": "cta", "lines": ["Hard to beat", "the market."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "020_index_funds_vs_managers.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
