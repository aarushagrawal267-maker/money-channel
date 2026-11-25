"""Video 044 (global/USD): Apple's profit machine today (fiscal 2026): devices vs Services margins.
Pillar: Business Breakdowns. Airs the day after the long video "Apple in 1997: The Turnaround That Saved the
Company", so this Short is about today's numbers only (title must not compete with the long one)."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Apple Inc. Form 10-K for the fiscal year ended September 26, 2026 (SEC EDGAR, accession 0000320193-26-000026,
# https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000026/aapl-20260926.htm, read 2026-11-25).
# Amounts in $ millions, fiscal 2026 (fiscal 2025 in brackets):
NET_SALES_PRODUCTS = 355_533      # (307,003)
NET_SALES_SERVICES = 123_301      # (109,158)
NET_SALES_TOTAL = 478_834         # (416,161)
GM_PRODUCTS = 139_659             # gross margin $, products (112,887)
GM_SERVICES = 93_943              # gross margin $, services (82,314)
GM_TOTAL = 233_602                # (195,201)
GM_PCT_PRODUCTS = 39.3            # 10-K "Products gross margin percentage" (36.8%); helped by product mix + tariff refunds
GM_PCT_SERVICES = 76.2            # 10-K "Services gross margin percentage" (75.4%)
NET_INCOME = 132_175              # (112,010)
# Apple's fiscal year is 52 or 53 weeks ending on the last Saturday of September. Fiscal 2025 ended Sept 27, 2025
# and fiscal 2026 ended Sept 26, 2026 -> a 52-week (364-day) year.
FY_DAYS = 364
# Apple newsroom, "Apple reports fourth quarter results" (Nov 2, 2026): fiscal 2026 "all-time record revenue" of $479B.

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert NET_SALES_PRODUCTS + NET_SALES_SERVICES == NET_SALES_TOTAL
assert GM_PRODUCTS + GM_SERVICES == GM_TOTAL
assert abs(GM_PRODUCTS / NET_SALES_PRODUCTS * 100 - GM_PCT_PRODUCTS) < 0.05
assert abs(GM_SERVICES / NET_SALES_SERVICES * 100 - GM_PCT_SERVICES) < 0.05
per_day = NET_INCOME * 1e6 / FY_DAYS
per_sec = per_day / 86_400
assert 4_150 < per_sec < 4_250, per_sec                          # "four thousand two hundred dollars ... every second"
assert round(per_day / 1e6) == 363, per_day                      # "≈ $363M a day" (on screen)
assert round(NET_INCOME / 1e3) == 132                            # "one hundred thirty-two billion dollars"
svc_sales_share = NET_SALES_SERVICES / NET_SALES_TOTAL
assert 0.24 < svc_sales_share < 0.27, svc_sales_share            # "about a quarter" of sales (25.8%)
svc_gp_share = GM_SERVICES / GM_TOTAL
assert round(svc_gp_share * 100) == 40, svc_gp_share              # "forty percent of gross profit"
assert round(GM_PCT_SERVICES) == 76 and round(GM_PCT_PRODUCTS) == 39   # "seventy-six cents" / "thirty-nine"
print(f"${per_sec:,.0f}/s, ${per_day/1e6:,.0f}M/day; services {svc_sales_share:.1%} of sales, "
      f"{svc_gp_share:.1%} of gross profit")

spec = {
    "id": "044_apple_profit",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Source: Apple fiscal 2026 Form 10-K · not investment advice",
    "title": "How Apple Makes $4,200 Profit Every Second",
    "description": (
        "How does Apple make so much money? In fiscal 2026 (year to Sept 26, 2026) Apple's net income was "
        f"${NET_INCOME/1e3:.1f} billion: about ${per_day/1e6:,.0f} million a day, or roughly ${per_sec:,.0f} every "
        "second. Devices like the iPhone bring in most of the sales, but Services (App Store, iCloud, Apple Music and "
        f"more) are the profit engine: {svc_sales_share:.0%} of sales, yet {svc_gp_share:.0%} of gross profit, with a "
        f"{GM_PCT_SERVICES}% gross margin versus {GM_PCT_PRODUCTS}% on products.\n\n"
        "Sources: Apple Inc. Form 10-K for fiscal 2026 (fiscal year ended Sept 26, 2026; SEC EDGAR); Apple newsroom, "
        "\"Apple reports fourth quarter results\" (Nov 2, 2026). Per-day and per-second figures are our own math: net "
        f"income divided by the {FY_DAYS}-day fiscal year. Gross margin is sales minus the direct cost of those sales, "
        "before operating costs and tax; Apple says its fiscal 2026 products margin was helped by product mix and "
        "tariff refunds. Apple's App Store fees have been challenged by regulators and courts, which is a risk to "
        "Services profits. This is a business explainer, not investment advice.\n\n"
        "#apple #business #iphone #appstore #businessmodel"
    ),
    "tags": ["how apple makes money", "apple profit", "apple services", "apple net income 2026",
             "apple business model", "iphone profit", "app store", "business breakdown", "gross margin"],
    "localizations": {
        "es": {"title": "Cómo Apple gana $4.200 de beneficio cada segundo",
               "summary": "En su año fiscal 2026, Apple ganó 132.200 millones de dólares netos, unos 4.200 por segundo. "
                          "Los servicios son solo un 26% de las ventas, pero el 40% del beneficio bruto."},
        "pt": {"title": "Como a Apple lucra US$4.200 a cada segundo",
               "summary": "No ano fiscal de 2026, a Apple teve lucro líquido de US$132,2 bilhões, cerca de US$4.200 por segundo. "
                          "Serviços são só 26% das vendas, mas 40% do lucro bruto."},
        "hi": {"title": "Apple हर सेकंड $4,200 मुनाफ़ा कैसे कमाता है",
               "summary": "वित्त वर्ष 2026 में Apple का शुद्ध मुनाफ़ा $132.2 अरब रहा, यानी हर सेकंड करीब $4,200। "
                          "Services बिक्री का सिर्फ़ 26% हैं, पर सकल मुनाफ़े का 40%।"},
        "id": {"title": "Cara Apple Raup Laba $4.200 Setiap Detik",
               "summary": "Pada tahun fiskal 2026, laba bersih Apple $132,2 miliar, sekitar $4.200 per detik. "
                          "Layanan hanya 26% dari penjualan, tapi 40% dari laba kotor."},
        "de": {"title": "Wie Apple jede Sekunde $4.200 Gewinn macht",
               "summary": "Im Geschäftsjahr 2026 erzielte Apple 132,2 Mrd. Dollar Nettogewinn, rund 4.200 Dollar pro Sekunde. "
                          "Services sind nur 26 % des Umsatzes, aber 40 % des Bruttogewinns."},
        "fr": {"title": "Comment Apple gagne 4 200 $ de profit par seconde",
               "summary": "Sur l'exercice 2026, Apple a dégagé 132,2 milliards de dollars de bénéfice net, environ 4 200 $ par "
                          "seconde. Les services font 26 % des ventes, mais 40 % de la marge brute."},
    },
    "scenes": [
        # hook: the biggest number on frame 0 + open loop ("From what?")
        {"say": "Apple clears four thousand two hundred dollars profit every second. From what?",
         "visual": {"type": "stat", "value": f"${round(per_sec, -2):,.0f}", "label": "Apple profit, every second",
                    "sub": f"fiscal 2026 net income ÷ {FY_DAYS} days", "color": "gold"}},
        {"say": "Fiscal twenty twenty-six profit: one hundred thirty-two billion dollars.",
         "visual": {"type": "equation", "title": "Apple net income, fiscal 2026",
                    "lines": [{"text": f"${NET_INCOME/1e3:.1f}B", "color": "gold", "size": 130},
                              {"text": f"÷ {FY_DAYS} days", "color": "text", "size": 80},
                              {"text": f"≈ ${per_day/1e6:,.0f}M a day", "color": "green", "size": 96}]}},
        {"say": "Most sales are devices like the iPhone. Services are about a quarter.",
         "visual": {"type": "compare", "title": "Apple sales, fiscal 2026",
                    "left": {"label": "Devices", "value": NET_SALES_PRODUCTS * 1e6, "color": "blue"},
                    "right": {"label": "Services", "value": NET_SALES_SERVICES * 1e6, "color": "green"}}},
        # mid-video re-hook: opens a second loop (why is the smaller part the profit engine?)
        {"say": "But here's the twist: the smaller part is the profit engine.",
         "visual": {"type": "pair", "title": "The twist",
                    "left": {"label": "Devices", "sub": "most of the sales", "color": "blue"},
                    "right": {"label": "Services", "sub": "fattest margins", "color": "green"}}},
        {"say": "After direct costs, Apple keeps seventy-six cents per Services dollar. Devices: thirty-nine.",
         "visual": {"type": "bars", "title": "Gross margin: ¢ kept per $1 sold", "format": "num",
                    "items": [{"label": "Devices", "value": GM_PCT_PRODUCTS, "color": "blue"},
                              {"label": "Services", "value": GM_PCT_SERVICES, "color": "green"}]}},
        {"say": "Services: a quarter of sales, but forty percent of gross profit.",
         "visual": {"type": "stat", "value": f"{svc_gp_share:.0%}", "label": "of Apple's gross profit is Services",
                    "sub": f"from just {svc_sales_share:.0%} of sales · fiscal 2026", "color": "green"}},
        {"say": "Why? Every phone needs new parts. Software costs far less to deliver.",
         "visual": {"type": "pair", "title": "Why the gap?",
                    "left": {"label": "iPhone", "sub": "new parts each sale", "color": "slate"},
                    "right": {"label": "Software", "sub": "cheap to deliver", "color": "gold"}}},
        {"say": "The lesson: one sale pays once. A loyal customer pays again and again.",
         "visual": {"type": "equation", "title": "The lesson",
                    "lines": [{"text": "One sale pays once.", "color": "text", "size": 84},
                              {"text": "A loyal customer", "color": "gold", "size": 92},
                              {"text": "pays again and again.", "color": "gold", "size": 84}]}},
        # loop line: runs back into "Apple clears four thousand two hundred dollars profit every second..."
        {"say": "Do that at Apple's scale, and that's how...",
         "visual": {"type": "cta", "lines": [f"${round(per_sec, -2):,.0f}", "every second."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
# ---------------------------------------------------------------- retention checks (AUTOPILOT "Retention rules")
words = [len(s["say"].split()) for s in spec["scenes"]]
for s in spec["scenes"]:
    assert len(s["say"].split()) <= 14, s["say"]                        # one visual per ~4 s
assert len(spec["scenes"][0]["say"].split()) <= 12                         # hook: payoff first, ~2 s
for a, b in zip(spec["scenes"], spec["scenes"][1:]):
    assert a["visual"]["type"] != b["visual"]["type"], a["say"]           # never the same visual twice in a row
assert 80 <= sum(words) <= 105, sum(words)                                 # ~30-40 s
assert "follow" not in spec["scenes"][-1]["say"].lower()                   # loop line, not a spoken CTA
assert "1997" not in spec["title"]                                         # must not compete with the L014 long video
print(f"{len(words)} scenes, {sum(words)} words (~{sum(words) / 2.9:.0f} s)")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "044_apple_profit.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
