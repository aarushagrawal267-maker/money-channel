"""Video 030 (India story for a global viewer): how Zerodha profits with ₹0 delivery brokerage. Pillar: Business Breakdowns."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Zerodha FY2025-26 (year to Mar 31, 2026), from Zerodha's blog post "16 years of Zerodha: Fresh enthusiasm"
# (Nithin Kamath, zerodha.com/z-connect, Aug 26, 2026; figures are in charts there), as reported by Inc42
# (Aug 26, 2026, net profit corrected Aug 28, 2026) and Lapaas Voice (Aug 26, 2026):
# net profit ₹4,283 crore (FY25 ₹4,231 crore); brokerage income ₹2,738 crore; interest income ₹2,269 crore.
# IANS (Aug 27, 2026) quoting the same post: profit "approximately Rs 4,300 crore".
CRORE = 1e7
PROFIT_FY26 = 4283 * CRORE
BROKERAGE_FY26 = 2738 * CRORE
INTEREST_FY26 = 2269 * CRORE
# Same Zerodha blog post (text): "MTF [margin trading facility] currently makes up ~10% of our revenue."
MTF_SHARE = 0.10
# Zerodha charges page (zerodha.com/charges, checked 2026-11-22): equity delivery ₹0 brokerage; equity intraday
# and futures "0.03% or Rs. 20/executed order whichever is lower"; options "Flat Rs. 20 per executed order".
DELIVERY_FEE, MAX_ORDER_FEE = 0, 20
# SEBI, "Profitability of Individual Traders in the Equity Derivatives Segment (FY25-FY26)", Aug 2026:
# "The share of loss-making individuals declined 3.2 percentage points, to 87.7% in FY26".
FO_LOSERS_FY26 = 0.877

# ---------------------------------------------------------------- checks behind spoken / shown claims
bn = lambda v: v / 1e9                                       # rupees -> billions of rupees
assert round(bn(PROFIT_FY26)) == 43                          # "about forty-three billion rupees"
assert round(bn(BROKERAGE_FY26)) == 27                       # "about twenty-seven billion"
assert round(bn(INTEREST_FY26)) == 23                        # "about twenty-three billion"
assert INTEREST_FY26 / BROKERAGE_FY26 > 0.8                  # "almost as big"
assert abs(MTF_SHARE - 1 / 10) < 1e-9                        # "about a tenth of its revenue"
assert 0.85 < FO_LOSERS_FY26 < 0.9                           # "nearly nine in ten"
assert DELIVERY_FEE == 0 and MAX_ORDER_FEE == 20             # "zero" / "up to twenty rupees an order"
print(f"profit ₹{bn(PROFIT_FY26):.2f}B, brokerage ₹{bn(BROKERAGE_FY26):.2f}B, interest ₹{bn(INTEREST_FY26):.2f}B, "
      f"F&O losers {FO_LOSERS_FY26:.1%}")

spec = {
    "id": "030_zerodha",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "INDIA STORY",
    "disclaimer": "Figures: Zerodha (FY2025-26), SEBI · not financial advice",
    "title": "How Zerodha Makes Money With ₹0 Brokerage",
    "description": (
        "Zerodha, one of India's biggest stockbrokers, charges ₹0 brokerage when you buy shares to hold, yet it "
        "earned about ₹4,283 crore (about ₹43 billion) in net profit in the year to March 2026. The money comes from "
        "traders, who pay up to ₹20 per intraday, futures or options order (brokerage of about ₹2,738 crore), from "
        "interest income (about ₹2,269 crore) and from margin loans (about 10% of revenue). SEBI found 87.7% of "
        "individual futures and options traders lost money in FY2025-26.\n\n"
        "Sources: Zerodha, '16 years of Zerodha: Fresh enthusiasm' (Nithin Kamath, 26 Aug 2026), FY2025-26 figures as "
        "reported by Inc42 (26-28 Aug 2026) and IANS (27 Aug 2026); Zerodha charges page (checked 22 Nov 2026); SEBI, "
        "'Profitability of Individual Traders in the Equity Derivatives Segment (FY25-FY26)' (Aug 2026). "
        "1 crore = 10 million. Not financial advice.\n\n"
        "#zerodha #india #stockmarket #business #fintech"
    ),
    "tags": ["zerodha", "how zerodha makes money", "zero brokerage", "discount broker", "futures and options",
             "f&o traders", "sebi study", "indian stock market", "business breakdown"],
    "localizations": {
        "es": {"title": "Cómo gana dinero Zerodha con comisión de ₹0",
               "summary": "El bróker indio Zerodha no cobra comisión por comprar acciones para conservar, pero ganó unos "
                          "₹43 mil millones en el año a marzo de 2026. Pagan los traders, los intereses y los préstamos."},
        "pt": {"title": "Como a Zerodha ganha dinheiro com corretagem de ₹0",
               "summary": "A corretora indiana Zerodha não cobra corretagem para comprar e manter ações, mas lucrou cerca "
                          "de ₹43 bilhões no ano até março de 2026. Quem paga são os traders, os juros e os empréstimos."},
        "hi": {"title": "₹0 ब्रोकरेज पर भी Zerodha कैसे कमाता है?",
               "summary": "Zerodha डिलीवरी पर ₹0 ब्रोकरेज लेता है, फिर भी मार्च 2026 तक के साल में लगभग ₹4,283 करोड़ "
                          "का मुनाफ़ा कमाया। पैसा ट्रेडर्स, ब्याज और मार्जिन लोन से आता है।"},
        "id": {"title": "Cara Zerodha Menghasilkan Uang dengan Komisi ₹0",
               "summary": "Broker India Zerodha tidak memungut komisi untuk membeli saham jangka panjang, tetapi laba "
                          "sekitar ₹43 miliar pada tahun hingga Maret 2026. Uangnya dari trader, bunga, dan pinjaman."},
        "de": {"title": "Wie Zerodha mit ₹0 Gebühren Geld verdient",
               "summary": "Der indische Broker Zerodha verlangt für Kaufen und Halten keine Gebühr, verdiente aber im Jahr "
                          "bis März 2026 rund ₹43 Milliarden. Es zahlen Trader, Zinsen und Wertpapierkredite."},
        "fr": {"title": "Comment Zerodha gagne de l'argent avec ₹0 de courtage",
               "summary": "Le courtier indien Zerodha ne facture rien pour acheter et garder des actions, mais a gagné "
                          "environ ₹43 milliards sur l'année à mars 2026. Les traders, les intérêts et les prêts paient."},
    },
    "scenes": [
        {"say": "Zerodha, one of India's biggest stockbrokers, charges nothing when you buy shares to keep. Yet in its latest financial year, it made about forty-three billion rupees in profit.",
         "visual": {"type": "stat", "value": "₹43B", "label": "Zerodha's profit, year to March 2026",
                    "sub": "₹4,283 crore · ₹0 brokerage to buy and hold", "color": "gold"}},
        {"say": "The trick? Investors who buy and hold pay zero. Traders pay. Every intraday, futures or options order costs up to twenty rupees.",
         "visual": {"type": "pair", "title": "Who pays brokerage",
                    "left": {"label": "Investors", "sub": "₹0 to buy & hold", "color": "green"},
                    "right": {"label": "Traders", "sub": "up to ₹20 an order", "color": "gold"}}},
        {"say": "That brokerage brought in about twenty-seven billion rupees. Almost as big: interest income, about twenty-three billion.",
         "visual": {"type": "bars", "title": "Zerodha income, ₹ billion", "format": "num",
                    "items": [{"label": "Brokerage", "value": round(bn(BROKERAGE_FY26)), "color": "gold"},
                              {"label": "Interest", "value": round(bn(INTEREST_FY26)), "color": "green"}]}},
        {"say": "It also lends traders money to buy shares. These margin loans are now about a tenth of its revenue.",
         "visual": {"type": "equation", "title": "Third money maker",
                    "lines": [{"text": "Margin loans", "color": "text", "size": 100},
                              {"text": "≈ 10% of revenue", "color": "gold", "size": 84}]}},
        {"say": "The catch: India's market regulator found that in the same year, nearly nine in ten individual futures and options traders lost money.",
         "visual": {"type": "stat", "value": f"{FO_LOSERS_FY26:.1%}", "label": "of individual F&O traders lost money",
                    "sub": "FY2025-26 · source: SEBI study, Aug 2026", "color": "red"}},
        {"say": "So investing really can be free. The bill is paid by people who trade a lot.",
         "visual": {"type": "equation",
                    "lines": [{"text": "Investing: free", "color": "green", "size": 100},
                              {"text": "Trading: paid", "color": "gold", "size": 100}]}},
        {"say": "Follow if this changed how you think about money.",
         "visual": {"type": "cta", "lines": ["Free to invest.", "Paid to trade."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "030_zerodha.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
