"""Video 022 (global/US): US airlines earn billions selling miles to credit card banks. Pillar: Business Breakdowns."""
import json, os

# ---------------------------------------------------------------- sourced facts
# American Airlines Group Form 10-K for 2025 (filed Feb 2026, SEC EDGAR aal-20251231.htm), MD&A:
# "During 2025 and 2024, cash payments from co-branded credit card and other partners were $6.2 billion
# and $6.1 billion, respectively."
AAL_PARTNER_CASH_2025 = 6.2e9
# American Airlines Q4/FY2025 earnings release (Jan 27, 2026): full-year 2025 GAAP net income $111 million.
AAL_NET_INCOME_2025 = 111e6
# Delta Air Lines Q4/FY2025 earnings release (Jan 13, 2026): "American Express remuneration in 2025 grew
# 11 percent to $8.2 billion"; FY2025 GAAP operating revenue $63,364M; GAAP pre-tax income $6,185M.
DAL_AMEX_2025 = 8.2e9
DAL_REVENUE_2025 = 63.364e9
DAL_PRETAX_2025 = 6.185e9

# ---------------------------------------------------------------- checks behind spoken claims
assert AAL_PARTNER_CASH_2025 / AAL_NET_INCOME_2025 > 50      # partners paid ~56x its net profit
assert DAL_AMEX_2025 > DAL_PRETAX_2025                       # "more than Delta's entire pre-tax profit"
share = DAL_AMEX_2025 / DAL_REVENUE_2025
assert abs(share - 1 / 8) < 0.01, share                      # "about one in every eight dollars" of revenue
print(f"AAL partner cash / net income = {AAL_PARTNER_CASH_2025 / AAL_NET_INCOME_2025:.0f}x; "
      f"Amex = {share:.1%} of Delta revenue")

spec = {
    "id": "022_airline_loyalty",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Partner payments are revenue, not profit · source: company filings",
    "title": "How Airlines Really Make Money: Credit Cards",
    "description": (
        "In 2025 American Airlines earned $111 million in net profit, while its co-branded credit card and "
        "other partners paid it $6.2 billion in cash. American Express paid Delta $8.2 billion, more than Delta's "
        "$6.2 billion pre-tax profit and about 13% of its revenue. The trick: airlines sell miles to banks, get "
        "cash today, and provide the seat later.\n\n"
        "Sources: American Airlines Group 2025 Form 10-K and Q4 2025 earnings release (Jan 27, 2026); Delta Air "
        "Lines December quarter and full-year 2025 results (Jan 13, 2026). Partner payments are revenue, not "
        "profit.\n\n"
        "#airlines #creditcards #business #frequentflyer #personalfinance"
    ),
    "tags": ["airline business model", "airline miles", "credit card rewards", "delta amex",
             "american airlines", "frequent flyer", "loyalty programs", "business breakdown"],
    "scenes": [
        {"say": "In twenty twenty-five, American Airlines made a hundred and eleven million dollars in profit. Its credit card and other partners paid it six point two billion.",
         "visual": {"type": "compare", "title": "American Airlines, 2025",
                    "left": {"label": "Net profit", "value": AAL_NET_INCOME_2025, "color": "slate"},
                    "right": {"label": "Card partners", "value": AAL_PARTNER_CASH_2025, "color": "gold"}}},
        {"say": "That's because airlines don't just sell seats. They sell miles. Banks buy them in bulk and give them to you as card rewards.",
         "visual": {"type": "equation", "title": "What airlines really sell",
                    "lines": [{"text": "Airline sells miles", "color": "text", "size": 76},
                              {"text": "↓", "color": "dim", "size": 72},
                              {"text": "Bank gives them to you", "color": "gold", "size": 66}]}},
        {"say": "Delta's card partner, American Express, paid it eight point two billion dollars in twenty twenty-five.",
         "visual": {"type": "stat", "value": "$8.2B", "label": "paid to Delta by American Express",
                    "sub": "2025 · Delta earnings release, Jan 2026", "color": "gold"}},
        {"say": "That's more than Delta's entire pre-tax profit of six point two billion, and about one in every eight dollars it brought in.",
         "visual": {"type": "bars", "title": "Delta, 2025",
                    "items": [{"label": "From Amex", "value": DAL_AMEX_2025, "color": "gold"},
                              {"label": "Pre-tax profit", "value": DAL_PRETAX_2025, "color": "slate"}]}},
        {"say": "Why do airlines love it? They get the cash today, and only provide the seat later, when you redeem.",
         "visual": {"type": "pair", "title": "Why airlines love miles",
                    "left": {"label": "Cash", "sub": "paid today", "color": "green"},
                    "right": {"label": "Seat", "sub": "given later", "color": "slate"}}},
        {"say": "So you might be the passenger. But one of the airline's biggest customers is your bank.",
         "visual": {"type": "equation",
                    "lines": [{"text": "You fly.", "color": "text", "size": 110},
                              {"text": "Your bank pays", "color": "gold", "size": 110},
                              {"text": "the airline.", "color": "gold", "size": 110}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Not just seats.", "Miles."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "022_airline_loyalty.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
