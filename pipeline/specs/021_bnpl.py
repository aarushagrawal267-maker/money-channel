"""Video 021 (global/US): Buy Now, Pay Later: why it feels free, how lenders earn, the traps. Pillar: Money Traps."""
import json, os

# ---------------------------------------------------------------- sourced facts
# CFPB, "Buy Now, Pay Later: Market Trends and Consumer Impacts" (Sept 2022), sec. 4.2.1: effective
# discount rate charged to partnered merchants by the five lenders surveyed: 3.84% (2019), 3.46% (2020), 3.08% (2021).
MERCHANT_FEE_2021 = 0.0308
# LendingTree BNPL statistics page (updated Nov 17, 2026). Surveys are self-reported, nonprobability samples.
#  - "68% of BNPL users agree that the loans cause them to overspend" (BNPL survey, March 2026, 2,049 US adults).
#  - "47% of users say they've paid late in the past year, up from 41% in 2025 and 34% in 2024"
#    (late-payment survey, March 17-23, 2026, 2,060 US adults).
OVERSPEND_2026 = 68
LATE = {"2024": 34, "2025": 41, "2026": 47}
# CFPB, "Consumer Use of Buy Now, Pay Later and Other Unsecured Debt" (Jan 13, 2025), Table 4 / summary:
# about 63% of BNPL borrowers (62.8%) originated multiple simultaneous loans at some point in 2022;
# about one in three (32.6%) did so across multiple firms.
STACKED_2022 = 0.628
# CFPB data spotlight "BNPL market report" (Dec 2025): 4 of 6 large lenders charged late fees in 2019-2023.

# ---------------------------------------------------------------- checks behind spoken claims
PRICE, N = 200, 4
inst = PRICE / N
assert inst == 50                                           # "four payments of fifty"
fee = PRICE * MERCHANT_FEE_2021
store_gets = PRICE - fee
assert 2.5 < MERCHANT_FEE_2021 * 100 < 3.5                  # "about three percent"
assert 5.5 < fee < 6.5, fee                                  # "about six dollars on two hundred"
assert LATE["2026"] - LATE["2024"] == 13                    # up 13 points in two years
assert 0.6 <= STACKED_2022 < 0.65                           # "about six in ten"
print(f"store keeps ${store_gets:.2f} of ${PRICE}; fee ${fee:.2f}")

spec = {
    "id": "021_bnpl",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY TRAP",
    "disclaimer": "Survey figures are self-reported · not financial advice",
    "title": "How Buy Now, Pay Later Makes Money (It's Not Interest)",
    "description": (
        "Pay-in-4 plans feel free, but lenders mostly earn from the store: a CFPB study found big BNPL lenders "
        "charged partner merchants about 3% per sale (2021). Some also charge late fees, and nearly half of users "
        "in a 2026 LendingTree survey said they paid late in the past year. The quiet risk is stacking several "
        "plans at once.\n\n"
        "Sources: CFPB, 'Buy Now, Pay Later: Market Trends and Consumer Impacts' (Sept 2022); CFPB, 'Consumer Use "
        "of Buy Now, Pay Later and Other Unsecured Debt' (Jan 2025, 2022 data); LendingTree BNPL surveys "
        "(March 2026, self-reported, ~2,050 US adults each; page updated Nov 17, 2026). Not financial advice.\n\n"
        "#buynowpaylater #bnpl #personalfinance #debt #moneytips"
    ),
    "tags": ["buy now pay later", "bnpl", "pay in 4", "klarna", "afterpay", "affirm", "late fees",
             "personal finance", "money traps", "debt"],
    "localizations": {
        "es": {"title": "Compra ahora, paga después: cómo ganan (no es el interés)",
               "summary": "Dividir $200 en 4 pagos de $50 sin intereses parece gratis, pero los prestamistas cobran sobre todo a la tienda: cerca del 3% por venta, según la CFPB. "
                          "Algunos también cobran recargos por pagos atrasados, y el riesgo silencioso es acumular varios planes a la vez."},
        "pt": {"title": "Compre agora, pague depois: como lucram (não são os juros)",
               "summary": "Dividir $200 em 4 parcelas de $50 sem juros parece de graça, mas as empresas ganham principalmente da loja: cerca de 3% por venda, segundo a CFPB. "
                          "Algumas também cobram multa por atraso, e o risco silencioso é acumular vários parcelamentos ao mesmo tempo."},
        "hi": {"title": "Buy Now, Pay Later पैसे कैसे कमाता है (ब्याज से नहीं)",
               "summary": "$200 को बिना ब्याज $50 की 4 किस्तों में बाँटना मुफ़्त लगता है, पर कंपनियाँ ज़्यादातर दुकान से कमाती हैं: CFPB के मुताबिक हर बिक्री पर करीब 3%। "
                          "कुछ लेट फीस भी लेती हैं, और असली ख़तरा है एक साथ कई प्लान चलाना।"},
        "id": {"title": "Cara Layanan Paylater Cari Untung (Bukan dari Bunga)",
               "summary": "Membagi $200 jadi 4 cicilan $50 tanpa bunga terasa gratis, tapi penyedianya terutama dibayar oleh toko: sekitar 3% per penjualan, menurut CFPB. "
                          "Sebagian juga memungut denda keterlambatan, dan risiko diam-diamnya adalah menumpuk beberapa cicilan sekaligus."},
        "de": {"title": "Buy Now, Pay Later: So verdienen Anbieter (nicht mit Zinsen)",
               "summary": "$200 zinsfrei in 4 Raten zu $50 aufzuteilen wirkt kostenlos, doch die Anbieter verdienen vor allem am Händler: laut CFPB etwa 3% pro Verkauf. "
                          "Manche verlangen zudem Mahngebühren, und das stille Risiko ist, mehrere Ratenpläne gleichzeitig laufen zu haben."},
        "fr": {"title": "Payer plus tard : d'où vient l'argent (pas des intérêts)",
               "summary": "Payer $200 en 4 fois $50 sans intérêts semble gratuit, mais les prêteurs gagnent surtout sur le commerçant : environ 3 % par vente, selon la CFPB. "
                          "Certains facturent aussi des frais de retard, et le risque discret est de cumuler plusieurs paiements à la fois."},
    },
    "thumbnail": {"big": "3%", "color": "gold", "photo": {"file": "assets/photos/online_shopping_phone_cart.jpg", "focus": [0.5, 0.5]}},
    "scenes": [
        {"say": "Split two hundred dollars into four payments of fifty, with no interest. So how does the lender make money?",
         "visual": {"type": "equation", "title": "Pay in 4",
                    "lines": [{"text": "$200", "color": "text", "size": 140},
                              {"text": "= 4 × $50", "color": "gold", "size": 96},
                              {"text": "0% interest", "color": "green", "size": 64}]}},
        {"say": "Mostly from the store. A CFPB study found that in twenty twenty-one, lenders charged partner stores about three percent per sale. About six dollars on two hundred.",
         "visual": {"type": "compare", "title": "On a $200 sale",
                    "left": {"label": "You pay", "value": PRICE, "color": "text"},
                    "right": {"label": "Store keeps", "value": store_gets, "color": "gold"}}},
        {"say": "Stores pay because it helps them sell. In a LendingTree survey, sixty-eight percent of users said BNPL makes them overspend.",
         "visual": {"type": "photo", "file": "assets/photos/online_shopping_phone_cart.jpg", "focus": [0.5, 0.5],
                    "value": f"{OVERSPEND_2026}%", "label": "of users say BNPL makes them overspend",
                    "color": "gold"}},
        {"say": "Some lenders also charge late fees. And forty-seven percent of users said they paid late in the past year, up from thirty-four percent in twenty twenty-four.",
         "visual": {"type": "bars", "title": "% of users who paid late", "format": "num",
                    "items": [{"label": y, "value": v, "color": "red" if y == "2026" else "slate"}
                              for y, v in LATE.items()]}},
        {"say": "Then there's stacking. The CFPB found about six in ten borrowers had several loans open at once. Small payments add up fast.",
         "visual": {"type": "photo", "file": "assets/photos/bill_due_dates_planner.jpg", "focus": [0.55, 0.5],
                    "title": "Stacking", "value": "6 in 10", "label": "had several BNPL loans at once",
                    "color": "red"}},
        {"say": "The rule: only use it for things you could pay for today, and track every plan you have.",
         "visual": {"type": "equation", "title": "The rule",
                    "lines": [{"text": "Could you pay today?", "color": "green", "size": 76},
                              {"text": "No? Don't split it.", "color": "text", "size": 64},
                              {"text": "Track every plan", "color": "muted", "size": 64}]}},
        {"say": "Save this for later, and follow for more.",
         "visual": {"type": "cta", "lines": ["Pay later", "is still paying."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "021_bnpl.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
