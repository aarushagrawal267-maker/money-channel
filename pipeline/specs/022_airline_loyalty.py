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
    "localizations": {
        "es": {"title": "El negocio real de las aerolíneas: tarjetas de crédito",
               "summary": "En 2025, American Airlines ganó $111 millones netos, mientras su tarjeta de crédito y otros socios le pagaron $6.2 mil millones. "
                          "American Express pagó a Delta $8.2 mil millones, más que su beneficio antes de impuestos. El truco: venden millas a los bancos, cobran hoy y dan el asiento después."},
        "pt": {"title": "O verdadeiro negócio das aéreas: cartões de crédito",
               "summary": "Em 2025, a American Airlines lucrou $111 milhões, enquanto seu cartão de crédito e outros parceiros lhe pagaram $6.2 bilhões. "
                          "A American Express pagou $8.2 bilhões à Delta, mais que o lucro antes de impostos dela. O truque: vender milhas aos bancos, receber hoje e entregar o assento depois."},
        "hi": {"title": "एयरलाइंस की असली कमाई: क्रेडिट कार्ड",
               "summary": "2025 में American Airlines का शुद्ध मुनाफ़ा $111 मिलियन था, जबकि उसके क्रेडिट कार्ड और दूसरे पार्टनर्स ने उसे $6.2 अरब दिए। "
                          "American Express ने Delta को $8.2 अरब दिए, जो Delta के टैक्स से पहले के मुनाफ़े से भी ज़्यादा है। तरीका: बैंकों को माइल्स बेचो, पैसा आज लो, सीट बाद में दो।"},
        "id": {"title": "Sumber Uang Maskapai yang Sebenarnya: Kartu Kredit",
               "summary": "Pada 2025, American Airlines meraup laba bersih $111 juta, sementara kartu kredit dan mitra lainnya membayarnya $6.2 miliar. "
                          "American Express membayar Delta $8.2 miliar, lebih besar dari laba sebelum pajak Delta. Triknya: jual mil ke bank, terima uang sekarang, beri kursinya nanti."},
        "de": {"title": "Womit Airlines wirklich Geld verdienen: Kreditkarten",
               "summary": "2025 erzielte American Airlines $111 Millionen Nettogewinn, während Kreditkarte und andere Partner ihr $6.2 Milliarden zahlten. "
                          "American Express zahlte Delta $8.2 Milliarden, mehr als Deltas Gewinn vor Steuern. Der Trick: Meilen an Banken verkaufen, heute kassieren, den Sitz später liefern."},
        "fr": {"title": "Le vrai filon des compagnies aériennes : la carte de crédit",
               "summary": "En 2025, American Airlines a dégagé $111 millions de bénéfice net, tandis que sa carte de crédit et d'autres partenaires lui ont versé $6.2 milliards. "
                          "American Express a versé $8.2 milliards à Delta, plus que son bénéfice avant impôts. L'astuce : vendre des miles aux banques, encaisser aujourd'hui, fournir le siège plus tard."},
    },
    "thumbnail": {"big": f"${AAL_PARTNER_CASH_2025 / 1e9:.1f}B", "line": "More than its profit", "color": "gold",
                  "photo": {"file": "assets/photos/american_airlines_737_at_gate.jpg", "focus": [0.62, 0.45]}},
    "scenes": [
        {"say": "In twenty twenty-five, American Airlines made a hundred and eleven million dollars in profit. Its credit card and other partners paid it six point two billion.",
         "visual": {"type": "compare", "title": "American Airlines, 2025",
                    "left": {"label": "Net profit", "value": AAL_NET_INCOME_2025, "color": "slate"},
                    "right": {"label": "Card partners", "value": AAL_PARTNER_CASH_2025, "color": "gold"}}},
        {"say": "A big reason: airlines don't just sell seats. They sell miles. Banks buy them in bulk and give them to you as card rewards.",
         "visual": {"type": "equation", "title": "What airlines really sell",
                    "lines": [{"text": "Airline sells miles", "color": "text", "size": 76},
                              {"text": "↓", "color": "dim", "size": 72},
                              {"text": "Bank gives them to you", "color": "gold", "size": 66}]}},
        {"say": "Delta's card partner, American Express, paid it eight point two billion dollars in twenty twenty-five.",
         "visual": {"type": "photo", "file": "assets/photos/delta_a350_in_flight.jpg", "focus": [0.5, 0.5],
                    "title": "Delta, 2025", "value": "$8.2B", "label": "paid to Delta by American Express",
                    "color": "gold"}},
        {"say": "That's more than Delta's entire pre-tax profit of six point two billion, and about one in every eight dollars it brought in.",
         "visual": {"type": "bars", "title": "Delta, 2025",
                    "items": [{"label": "From Amex", "value": DAL_AMEX_2025, "color": "gold"},
                              {"label": "Pre-tax profit", "value": DAL_PRETAX_2025, "color": "slate"}]}},
        {"say": "Why do airlines love it? They get the cash today, and only provide the seat later, when you redeem.",
         "visual": {"type": "pair", "title": "Why airlines love miles",
                    "left": {"label": "Cash", "sub": "paid today", "color": "green"},
                    "right": {"label": "Seat", "sub": "given later", "color": "slate"}}},
        {"say": "So you might be the passenger. But one of the airline's biggest customers is your bank.",
         "visual": {"type": "photo", "file": "assets/photos/american_airlines_777_cabin.jpg", "focus": [0.5, 0.55],
                    "title": "You fly. Your bank pays the airline.", "value": "Your bank",
                    "label": "one of the airline's biggest customers", "color": "gold"}},
        {"say": "Share this with someone who needs it.",
         "visual": {"type": "cta", "lines": ["Not just seats.", "Miles."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "022_airline_loyalty.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
