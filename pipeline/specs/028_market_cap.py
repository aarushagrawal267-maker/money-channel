"""Video 028 (global/US): market cap vs revenue, why a company's value isn't its sales. Pillar: How Markets Work."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Revenue and net income, last full fiscal year (SEC XBRL company facts from each Form 10-K):
# Walmart FY2026 (Feb 1, 2025 - Jan 31, 2026), Form 10-K filed Mar 13, 2026: total revenues $713,163M,
# consolidated net income attributable to Walmart $21,893M.
WMT_REVENUE = 713.163e9
WMT_NET_INCOME = 21.893e9
# Microsoft FY2026 (Jul 1, 2025 - Jun 30, 2026), Form 10-K filed Jul 29, 2026: revenue $331,839M, net income $133,749M.
MSFT_REVENUE = 331.839e9
MSFT_NET_INCOME = 133.749e9
# Shares outstanding, cover page of the latest filing (SEC EDGAR):
# Microsoft Form 10-Q filed Oct 28, 2026: 7,426,194,552 shares as of Oct 22, 2026.
# Walmart Form 10-Q filed Aug 28, 2026: 7,933,746,241 shares as of Aug 26, 2026.
MSFT_SHARES = 7_426_194_552
WMT_SHARES = 7_933_746_241
# Closing share prices on Nov 18, 2026 (stockanalysis.com price history, checked 2026-11-22; MSFT close also
# reported by Gotrade news, Nov 19, 2026).
PRICE_DATE = "Nov 18, 2026"
MSFT_PRICE = 508.29
WMT_PRICE = 127.36

# ---------------------------------------------------------------- checks behind spoken / shown claims
msft_cap = MSFT_PRICE * MSFT_SHARES
wmt_cap = WMT_PRICE * WMT_SHARES
assert 3.75e12 < msft_cap < 3.85e12, msft_cap          # "about three point eight trillion dollars"
assert 0.95e12 < wmt_cap < 1.05e12, wmt_cap            # "about one trillion"
sales_ratio = WMT_REVENUE / MSFT_REVENUE
assert 2.0 < sales_ratio < 2.3, sales_ratio            # "more than twice as much"
value_ratio = msft_cap / wmt_cap
assert 3.5 < value_ratio < 4.0, value_ratio            # "almost four times as much"
msft_margin = MSFT_NET_INCOME / MSFT_REVENUE
wmt_margin = WMT_NET_INCOME / WMT_REVENUE
assert round(msft_margin * 100) == 40, msft_margin     # "about forty cents of every dollar"
assert round(wmt_margin * 100) == 3, wmt_margin        # "about three cents"
msft_ps = msft_cap / MSFT_REVENUE
wmt_ps = wmt_cap / WMT_REVENUE
assert round(msft_ps) == 11, msft_ps                   # "about eleven dollars per dollar of sales"
assert round(wmt_ps, 1) == 1.4, wmt_ps                 # "about one dollar forty"
assert round(MSFT_PRICE) == 508 and round(MSFT_SHARES / 1e9, 1) == 7.4
cap_b = {"Microsoft": round(msft_cap / 1e9), "Walmart": round(wmt_cap / 1e9)}
print(f"MSFT cap ${msft_cap/1e12:.3f}T ({msft_ps:.1f}x sales, {msft_margin:.1%} margin); "
      f"WMT cap ${wmt_cap/1e12:.3f}T ({wmt_ps:.2f}x sales, {wmt_margin:.1%} margin); "
      f"sales {sales_ratio:.2f}x, value {value_ratio:.2f}x")

spec = {
    "id": "028_market_cap",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": f"Share prices as of {PRICE_DATE} · not a recommendation",
    "title": "Market Cap vs Revenue: Walmart Sells More, Worth Less",
    "description": (
        "Market cap is a company's share price times its number of shares, and it is not the same as revenue. "
        f"Walmart's yearly sales ($713 billion) are more than double Microsoft's ($332 billion), yet on {PRICE_DATE} "
        f"Microsoft was worth about ${msft_cap/1e12:.1f} trillion and Walmart about ${wmt_cap/1e12:.1f} trillion. "
        f"The difference is profit: Microsoft kept about {msft_margin:.0%} of its revenue as net income, Walmart about "
        f"{wmt_margin:.0%}.\n\n"
        "Sources: Walmart Form 10-K for fiscal 2026 (year to Jan 31, 2026, filed Mar 13, 2026) and Form 10-Q "
        "(filed Aug 28, 2026, shares outstanding); Microsoft Form 10-K for fiscal 2026 (year to Jun 30, 2026, filed "
        f"Jul 29, 2026) and Form 10-Q (filed Oct 28, 2026, shares outstanding); closing prices on {PRICE_DATE}. "
        "Market caps change every trading day. Not financial advice and not a recommendation to buy or sell any stock.\n\n"
        "#stockmarket #investing #marketcap #business #personalfinance"
    ),
    "tags": ["market cap", "market capitalization explained", "market cap vs revenue", "price to sales",
             "walmart", "microsoft", "how the stock market works", "investing basics"],
    "localizations": {
        "es": {"title": "Capitalización vs ingresos: Walmart vende más y vale menos",
               "summary": "La capitalización bursátil es el precio de la acción por el número de acciones, no las ventas. "
                          "Walmart vende más del doble que Microsoft, pero Microsoft vale casi cuatro veces más."},
        "pt": {"title": "Valor de mercado x receita: Walmart vende mais e vale menos",
               "summary": "Valor de mercado é o preço da ação vezes o número de ações, não as vendas. "
                          "O Walmart vende mais que o dobro da Microsoft, mas a Microsoft vale quase quatro vezes mais."},
        "hi": {"title": "मार्केट कैप बनाम बिक्री: Walmart ज़्यादा बेचकर भी कम कीमती",
               "summary": "मार्केट कैप = शेयर का दाम × शेयरों की संख्या, यह बिक्री नहीं है। "
                          "Walmart की बिक्री Microsoft से दोगुनी से ज़्यादा है, फिर भी Microsoft लगभग चार गुना ज़्यादा मूल्यवान है।"},
        "id": {"title": "Kapitalisasi Pasar vs Pendapatan: Walmart Jual Lebih Banyak",
               "summary": "Kapitalisasi pasar adalah harga saham dikali jumlah saham, bukan penjualan. "
                          "Penjualan Walmart lebih dari dua kali Microsoft, tetapi Microsoft bernilai hampir empat kali lipat."},
        "de": {"title": "Börsenwert vs. Umsatz: Warum Walmart weniger wert ist",
               "summary": "Der Börsenwert ist Aktienkurs mal Anzahl der Aktien, nicht der Umsatz. "
                          "Walmart setzt mehr als doppelt so viel um wie Microsoft, doch Microsoft ist fast viermal so viel wert."},
        "fr": {"title": "Capitalisation vs chiffre d'affaires : Walmart vend plus",
               "summary": "La capitalisation boursière, c'est le cours de l'action multiplié par le nombre d'actions, pas les ventes. "
                          "Walmart vend plus du double de Microsoft, mais Microsoft vaut presque quatre fois plus."},
    },
    "thumbnail": {"big": f"{wmt_margin * 100:.0f}¢", "line": "Profit per $1 sold", "color": "gold",
                  "photo": {"file": "assets/photos/walmart_store_front.jpg", "focus": [0.82, 0.3]}},
    "scenes": [
        {"say": "Walmart sells more than twice as much as Microsoft. Yet Microsoft is worth almost four times as much. How?",
         "visual": {"type": "compare", "title": "Sales, last fiscal year",
                    "left": {"label": "Walmart", "value": WMT_REVENUE, "color": "gold"},
                    "right": {"label": "Microsoft", "value": MSFT_REVENUE, "color": "blue"}}},
        {"say": "Because a company's value isn't its sales. Its value, called market cap, is the share price times the number of shares.",
         "visual": {"type": "photo", "file": "assets/photos/walmart_store_front.jpg",
                    "title": "Market cap = price × shares",
                    "label": "a company's value isn't its sales", "focus": [0.55, 0.35]}},
        {"say": "Microsoft: about five hundred and eight dollars a share, times seven point four billion shares. That's about three point eight trillion dollars. Walmart? About one trillion.",
         "visual": {"type": "bars", "title": "Market cap ($ billions)", "format": "num",
                    "items": [{"label": "Microsoft", "value": cap_b["Microsoft"], "color": "blue"},
                              {"label": "Walmart", "value": cap_b["Walmart"], "color": "gold"}]}},
        {"say": "Investors aren't buying sales. They're buying future profits. Microsoft kept about forty cents of every dollar it sold as profit. Walmart kept about three cents.",
         "visual": {"type": "photo", "file": "assets/photos/microsoft_sign_campus.jpg",
                    "title": "Profit from each $1 of sales",
                    "value": "40¢", "color": "blue", "label": "Microsoft · Walmart: about 3¢",
                    "focus": [0.4, 0.4]}},
        {"say": "So investors pay about eleven dollars for each dollar of Microsoft's yearly sales, and about one dollar forty for Walmart's. And that value moves every time the share price does.",
         "visual": {"type": "equation", "title": "Value per $1 of sales",
                    "lines": [{"text": f"Microsoft ${msft_ps:.0f}", "color": "blue", "size": 100},
                              {"text": f"Walmart ${wmt_ps:.2f}", "color": "gold", "size": 100},
                              {"text": f"prices as of {PRICE_DATE}", "color": "muted", "size": 46}]}},
        {"say": "There's a new one every day. Follow so you don't miss it.",
         "visual": {"type": "cta", "lines": ["Sales aren't", "value."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "028_market_cap.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
