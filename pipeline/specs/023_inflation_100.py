"""Video 023 (global/USD): what $100 buys after 10/20/30 years of inflation. All numbers computed here."""
import json, os

P, INF, FED = 100, 0.03, 0.02
years = list(range(0, 31))
buys = {n: P / (1 + INF) ** n for n in (10, 20, 30)}      # today's-dollar buying power of $100 cash
need = {n: P * (1 + INF) ** n for n in (10, 20, 30)}      # what $100 must grow to, just to keep up
need_path = [P * (1 + INF) ** n for n in years]
cash_path = [P for _ in years]
fed30 = P / (1 + FED) ** 30

assert round(buys[10]) == 74 and round(buys[20]) == 55 and round(buys[30]) == 41   # "74 / 55 / 41"
assert round(need[10]) == 134 and round(need[20]) == 181 and round(need[30]) == 243  # "134 / 181 / 243"
assert round(fed30) == 55                                 # "about fifty-five dollars" at the 2% target
print({n: (round(buys[n], 2), round(need[n], 2)) for n in buys}, round(fed30, 2))

spec = {
    "id": "023_inflation_100",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "disclaimer": "Illustration · assumes 3% inflation a year · real inflation varies",
    "title": "What $100 Will Buy in 30 Years (Inflation Explained)",
    "description": (
        f"At 3% inflation a year, $100 in cash buys about ${buys[10]:.0f} of today's goods after 10 years, "
        f"${buys[20]:.0f} after 20 and ${buys[30]:.0f} after 30. To just keep up, that $100 has to grow to "
        f"${need[10]:.0f}, ${need[20]:.0f} and ${need[30]:.0f}.\n\n"
        "Assumptions: a steady 3% inflation rate every year (a round number; actual inflation changes year to "
        "year). The US Federal Reserve's longer-run goal is 2% inflation, measured by the PCE price index "
        f"(source: federalreserve.gov); at 2%, $100 buys about ${fed30:.0f} of today's goods after 30 years.\n\n"
        "#inflation #personalfinance #moneytips #savings #financialliteracy"
    ),
    "tags": ["inflation", "purchasing power", "cost of living", "money math", "personal finance",
             "savings", "money tips", "financial literacy", "federal reserve"],
    "scenes": [
        {"say": "Put a hundred dollar bill in a drawer. In thirty years, it'll only buy what forty-one dollars buys today.",
         "visual": {"type": "compare", "title": "What $100 buys",
                    "left": {"label": "Today", "value": P, "color": "text"},
                    "right": {"label": "In 30 years", "value": buys[30], "color": "red"}}},
        {"say": "That's with prices rising three percent a year. A simple round number. Real inflation changes every year.",
         "visual": {"type": "stat", "value": "3%", "label": "prices rise each year",
                    "sub": "assumed · real inflation varies", "color": "gold"}},
        {"say": "After ten years, your hundred buys about seventy-four dollars of today's stuff. After twenty, fifty-five. After thirty, forty-one.",
         "visual": {"type": "bars", "title": "What $100 cash can buy",
                    "items": [{"label": "10 years", "value": buys[10], "color": "slate"},
                              {"label": "20 years", "value": buys[20], "color": "gold"},
                              {"label": "30 years", "value": buys[30], "color": "red"}]}},
        {"say": "Flip it around. Just to keep up, that hundred has to grow to one thirty-four in ten years, one eighty-one in twenty, and two forty-three in thirty.",
         "visual": {"type": "line", "title": "Just to keep up", "x": years, "x_label": "years",
                    "series": [{"label": "Needed", "values": need_path, "color": "green"},
                               {"label": "Cash in a drawer", "values": cash_path, "color": "red"}]}},
        {"say": "Even at the Federal Reserve's two percent target, thirty years cuts a hundred dollars down to about fifty-five.",
         "visual": {"type": "stat", "value": f"${fed30:.0f}", "label": "what $100 buys after 30 years",
                    "sub": "at the Fed's 2% inflation target", "color": "gold"}},
        {"say": "So money you won't need for years has to grow faster than prices, just to stand still.",
         "visual": {"type": "equation", "title": "What really counts",
                    "lines": [{"text": "your growth", "color": "green", "size": 96},
                              {"text": "− inflation", "color": "red", "size": 96},
                              {"text": "= real growth", "color": "gold", "size": 110}]}},
        {"say": "Follow for tomorrow's money lesson.",
         "visual": {"type": "cta", "lines": ["Prices never", "stand still."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "023_inflation_100.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
