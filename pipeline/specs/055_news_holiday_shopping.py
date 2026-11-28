"""Video 055 (global, news): record US Thanksgiving online spending and the Cyber Monday pitch. Pillar: Money News.
Made Sat 28 Nov 2026, airs Sun 29 Nov 22:30 IST (before Cyber Monday, Nov 30)."""
import json, os

# ---------------------------------------------------------------- sourced facts (checked 2026-11-28)
# Adobe Analytics, Thanksgiving Day 2026 result, as reported by Reuters (via Investing.com, Nov 27-28, 2026),
# Seeking Alpha (Nov 2026: "Thanksgiving delivered record $7.1B in sales") and CNBC (Nov 27, 2026):
# US online spending on Thanksgiving Day $7.1 billion, up 10.4% YoY, above Adobe's $6.9B forecast.
THANKSGIVING_2026, THANKSGIVING_GROWTH = 7.1e9, 0.104
# Adobe, 2025 holiday recap / TechCrunch (Nov 29, 2025): Thanksgiving 2025 online spending $6.4 billion.
THANKSGIVING_2025 = 6.4e9
# Adobe news release, Sept 28, 2026 ("U.S. Holiday Shopping Season to Hit Record $275.1 Billion Online"),
# all FORECASTS: Cyber Monday (Nov 30) "$15.1 billion, up 6.2% YoY"; buy now, pay later Nov-Dec "$21.3 billion";
# discounts "up to 30% off listed price" in Cyber Week, peak by category: electronics 30%, toys 29%, TVs 23%.
CYBER_MONDAY_FC = 15.1e9
BNPL_SEASON_FC = 21.3e9
PEAK_DISCOUNT = {"Electronics": 30, "Toys": 29, "TVs": 23}

# illustration (not a statistic): a $200 gadget at the peak electronics discount
PRICE, OFF = 200, PEAK_DISCOUNT["Electronics"] / 100
SALE = PRICE * (1 - OFF)
SAVED = PRICE - SALE

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert round(THANKSGIVING_2026 / 1e9, 1) == 7.1                           # "seven point one billion"
assert 0.09 <= THANKSGIVING_GROWTH <= 0.11                                  # "up about ten percent"
assert 0.08 <= THANKSGIVING_2026 / THANKSGIVING_2025 - 1 <= 0.12           # bars 2025 vs 2026 consistent with ~10%
assert CYBER_MONDAY_FC > 15e9                                               # "over fifteen billion"
assert round(BNPL_SEASON_FC / 1e9) == 21                                    # "about twenty one billion"
assert SALE == 140 and SAVED == 60                                          # "$200 at 30% off = $140", "save sixty"

spec = {
    "id": "055_news_holiday_shopping",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY NEWS",
    "disclaimer": "Source: Adobe Analytics via Reuters, CNBC · Nov 2026 · forecasts marked",
    "title": "Thanksgiving Shoppers Spent a Record $7.1B Online. Who Wins?",
    "description": (
        "Americans spent a record $7.1 billion online on Thanksgiving Day 2026, up 10.4% from last year, "
        "according to Adobe Analytics. Adobe expects Cyber Monday (Nov 30) to top $15 billion, with discounts "
        "of up to 30% on electronics, and buy now, pay later spending of about $21.3 billion this season. "
        "Here's the simple rule that decides whether a sale actually saves you money.\n\n"
        "The $200 gadget is an illustration. Cyber Monday, discount and buy now, pay later figures are Adobe's "
        "forecasts (Sept 28, 2026), not results. Thanksgiving 2025: $6.4 billion (Adobe).\n\n"
        "Sources: Adobe Analytics Thanksgiving 2026 data as reported by Reuters (via Investing.com, Nov 27-28, "
        "2026), CNBC (Nov 27, 2026) and Seeking Alpha; Adobe news release, U.S. Holiday Shopping Season to Hit "
        "Record $275.1 Billion Online (Sept 28, 2026): "
        "https://news.adobe.com/news/2026/09/adobe-us-holiday-shopping-season-to-hit-record ; "
        "Adobe 2025 holiday recap / TechCrunch (Nov 29, 2025).\n\n"
        "For education only. Not financial advice.\n\n"
        "#blackfriday #cybermonday #moneynews #personalfinance #shopping"
    ),
    "tags": ["thanksgiving online sales 2026", "black friday 2026", "cyber monday 2026", "adobe analytics",
             "holiday shopping", "black friday deals", "are black friday deals worth it", "buy now pay later",
             "money news", "personal finance"],
    "localizations": {
        "es": {"title": "Récord de $7.100 millones en compras online en Thanksgiving",
               "summary": "Los estadounidenses gastaron un récord de 7.100 millones de dólares online en Thanksgiving 2026 (Adobe). Para Cyber Monday se esperan más de 15.000 millones. La regla simple para saber si una oferta te ahorra dinero de verdad."},
        "pt": {"title": "Recorde: US$ 7,1 bilhões em compras online no Thanksgiving",
               "summary": "Os americanos gastaram um recorde de US$ 7,1 bilhões online no Thanksgiving 2026 (Adobe). Para a Cyber Monday, a previsão passa de US$ 15 bilhões. A regra simples para saber se uma promoção economiza de verdade."},
        "hi": {"title": "Thanksgiving पर रिकॉर्ड $7.1 अरब की ऑनलाइन ख़रीदारी",
               "summary": "Adobe के मुताबिक़ अमेरिकियों ने Thanksgiving 2026 पर रिकॉर्ड 7.1 अरब डॉलर ऑनलाइन ख़र्च किए। Cyber Monday पर 15 अरब डॉलर से ज़्यादा का अनुमान है। सेल से सच में पैसे बचते हैं या नहीं, यह आसान नियम बताता है।"},
        "id": {"title": "Rekor $7,1 Miliar Belanja Online Saat Thanksgiving",
               "summary": "Warga AS belanja online rekor 7,1 miliar dolar saat Thanksgiving 2026 (Adobe). Cyber Monday diperkirakan lebih dari 15 miliar dolar. Aturan sederhana untuk tahu apakah diskon benar-benar menghemat uang."},
        "de": {"title": "Rekord: 7,1 Mrd. $ Online-Umsatz an Thanksgiving",
               "summary": "Amerikaner gaben an Thanksgiving 2026 online einen Rekord von 7,1 Milliarden Dollar aus (Adobe). Für den Cyber Monday werden über 15 Milliarden erwartet. Die einfache Regel, ob ein Rabatt wirklich spart."},
        "fr": {"title": "Record : 7,1 Md$ d'achats en ligne à Thanksgiving",
               "summary": "Les Américains ont dépensé un record de 7,1 milliards de dollars en ligne à Thanksgiving 2026 (Adobe). Le Cyber Monday devrait dépasser 15 milliards. La règle simple pour savoir si une promo fait vraiment économiser."},
    },
    "thumbnail": {"big": f"${THANKSGIVING_2026 / 1e9:.1f}B", "line": "Spent online in one day", "color": "gold",
                  "photo": {"file": "assets/photos/black_friday_mall.jpg", "focus": [0.5, 0.5]}},
    "scenes": [
        # hook: payoff number on frame 0 + open loop ("who really wins?")
        {"say": "Seven point one billion dollars online, on Thanksgiving alone. Who really wins?",
         "visual": {"type": "photo", "file": "assets/photos/black_friday_mall.jpg", "focus": [0.5, 0.5],
                    "value": f"${THANKSGIVING_2026 / 1e9:.1f}B", "label": "spent online, Thanksgiving 2026 (Adobe)",
                    "color": "gold"}},
        {"say": "That's a record, up about ten percent on last year.",
         "visual": {"type": "bars", "title": "US online spend, Thanksgiving Day", "format": "usd",
                    "items": [{"label": "2025", "value": THANKSGIVING_2025, "color": "slate"},
                              {"label": "2026", "value": THANKSGIVING_2026, "color": "gold"}]}},
        {"say": "And Adobe expects Cyber Monday to top fifteen billion.",
         "visual": {"type": "stat", "value": f"${CYBER_MONDAY_FC / 1e9:.1f}B",
                    "label": "Cyber Monday, Nov 30", "sub": "Adobe forecast", "color": "green"}},
        {"say": "The pitch? Up to thirty percent off electronics.",
         "visual": {"type": "photo", "file": "assets/photos/black_friday_electronics_shopper.jpg",
                    "focus": [0.5, 0.4], "value": "-30%", "label": "peak electronics discount (Adobe forecast)",
                    "color": "red"}},
        # mid-video re-hook
        {"say": "The catch: a sale only saves on things you needed.",
         "visual": {"type": "pair", "title": "The catch",
                    "left": {"label": "Needed it", "sub": "you saved", "color": "green"},
                    "right": {"label": "Didn't", "sub": "you spent", "color": "red"}}},
        {"say": "A two hundred dollar gadget at thirty percent off costs one forty.",
         "visual": {"type": "equation", "title": "Example",
                    "lines": [{"text": f"${PRICE} − 30%", "color": "text", "size": 110},
                              {"text": f"= ${SALE:.0f}", "color": "gold", "size": 140}]}},
        {"say": "Didn't plan to buy it? You didn't save sixty. You spent one forty.",
         "visual": {"type": "compare", "title": "Unplanned buy", "format": "usd",
                    "left": {"label": "\"Saved\"", "value": SAVED, "color": "green"},
                    "right": {"label": "Spent", "value": SALE, "color": "red"}}},
        {"say": "Buy now, pay later? About twenty one billion expected this season.",
         "visual": {"type": "stat", "value": f"${BNPL_SEASON_FC / 1e9:.1f}B",
                    "label": "buy now, pay later, Nov–Dec", "sub": "Adobe forecast", "color": "gold"}},
        {"say": "The rule: write your list before the sale, not during it.",
         "visual": {"type": "equation", "title": "The rule",
                    "lines": [{"text": "List first.", "color": "text", "size": 120},
                              {"text": "Sale second.", "color": "gold", "size": 120}]}},
        # loop line: runs back into "...Who really wins?"
        {"say": "Then the winner is you, not the checkout.",
         "visual": {"type": "cta", "lines": ["List first.", "Then shop."], "sub": "Follow for daily money lessons"}},
    ],
}
# ---------------------------------------------------------------- retention checks (AUTOPILOT "Retention rules")
words = [len(s["say"].split()) for s in spec["scenes"]]
for s in spec["scenes"]:
    assert len(s["say"].split()) <= 14, s["say"]
assert len(spec["scenes"][0]["say"].split()) <= 12
for a, b in zip(spec["scenes"], spec["scenes"][1:]):
    assert a["visual"]["type"] != b["visual"]["type"], a["say"]
assert 80 <= sum(words) <= 105, sum(words)
assert "follow" not in spec["scenes"][-1]["say"].lower()
assert len(spec["title"]) <= 60, len(spec["title"])
print(f"{len(words)} scenes, {sum(words)} words (~{sum(words) / 2.9:.0f} s)")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "055_news_holiday_shopping.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
