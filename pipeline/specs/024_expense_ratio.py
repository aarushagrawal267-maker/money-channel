"""Video 024 (global/USD): how a 1% fee compares with 0.05% over 30 years. All numbers simulated here."""
import json, os

START, MONTHLY, YEARS, GROSS = 10_000, 500, 30, 0.07
FEES = {"low": 0.0005, "high": 0.01}

def simulate(fee):
    """Monthly: add the contribution, grow at GROSS/12, then the fund takes fee/12 of the balance."""
    bal, paid, path = START, 0.0, [START]
    for m in range(1, YEARS * 12 + 1):
        bal += MONTHLY
        bal *= 1 + GROSS / 12
        f = bal * fee / 12
        paid += f; bal -= f
        if m % 12 == 0:
            path.append(bal)
    return bal, paid, path

low, low_paid, _ = simulate(FEES["low"])
high, high_paid, _ = simulate(FEES["high"])
invested = START + MONTHLY * 12 * YEARS
gap = low - high

assert invested == 190_000                    # "one hundred ninety thousand dollars of your own money"
assert 685_000 < low < 690_000, low           # "nearly six hundred and ninety thousand"
assert 560_000 < high < 565_000, high         # "about five hundred and sixty thousand"
assert 120_000 < gap < 125_000, gap           # "over a hundred and twenty thousand dollars"
assert 62_000 < high_paid < 63_000, high_paid # "over sixty-two thousand in fees"
assert 3_550 < low_paid < 3_650, low_paid     # "about thirty-six hundred"
print(f"low ${low:,.0f} (fees ${low_paid:,.0f}); high ${high:,.0f} (fees ${high_paid:,.0f}); gap ${gap:,.0f} ({gap/low:.1%})")

spec = {
    "id": "024_expense_ratio",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HIDDEN COSTS",
    "thumbnail": {"big": f"−${gap/1e3:,.0f}K", "line": "Same plan, smaller pile", "color": "red",
                  "photo": {"file": "assets/photos/dollar_bills_100s.jpg", "focus": [0.55, 0.5]}},
    "disclaimer": "Illustration · assumes 7% a year before fees · not financial advice",
    "title": "A 1% Investment Fee Can Cost You $120,000. Here's How",
    "description": (
        "Same plan, two funds: $10,000 to start plus $500 a month for 30 years. With a 0.05% yearly fee you'd end "
        f"with about ${low/1e3:,.0f}K. With a 1% fee, about ${high/1e3:,.0f}K. The gap is about "
        f"${gap/1e3:,.0f}K: the fees plus the growth those fees would have earned. A fund's yearly fee is called its "
        "expense ratio, and it's listed on the fund's fact sheet.\n\n"
        "Assumptions: 7% average yearly return before fees, compounded monthly; fees charged monthly as a share "
        "of the balance; no taxes or other costs. Illustration only: real returns vary and are not guaranteed. "
        "Not financial advice.\n\n"
        "#expenseratio #investing #indexfunds #personalfinance #moneytips"
    ),
    "tags": ["expense ratio", "investment fees", "mutual fund fees", "index funds", "investing basics",
             "personal finance", "retirement savings", "financial literacy"],
    "localizations": {
        "es": {"title": "Una comisión del 1% puede costarte $120,000. Así es como",
               "summary": f"Mismo plan, dos fondos: $10,000 al inicio más $500 al mes durante 30 años, con un 7% anual supuesto. Con una comisión anual del 0.05% terminarías con unos ${low/1e3:,.0f}K; con un 1%, unos ${high/1e3:,.0f}K. "
                          "Esa comisión se llama ratio de gastos (expense ratio) y aparece en la ficha del fondo."},
        "pt": {"title": "Uma taxa de 1% pode te custar $120,000. Veja como",
               "summary": f"Mesmo plano, dois fundos: $10,000 iniciais mais $500 por mês durante 30 anos, com 7% ao ano (suposição). Com taxa anual de 0.05% você terminaria com cerca de ${low/1e3:,.0f}K; com 1%, cerca de ${high/1e3:,.0f}K. "
                          "Essa taxa se chama taxa de despesas (expense ratio) e aparece na lâmina do fundo."},
        "hi": {"title": "1% फीस आपको $120,000 का नुकसान कैसे करा सकती है",
               "summary": f"एक ही प्लान, दो फंड: शुरुआत में $10,000 और फिर 30 साल तक हर महीने $500, 7% सालाना अनुमानित रिटर्न पर। 0.05% सालाना फीस पर करीब ${low/1e3:,.0f}K बनते हैं, 1% फीस पर करीब ${high/1e3:,.0f}K। "
                          "इस सालाना फीस को एक्सपेंस रेशियो कहते हैं, और यह फंड की फैक्ट शीट पर लिखा होता है।"},
        "id": {"title": "Biaya Investasi 1% Bisa Menelan $120,000. Begini Caranya",
               "summary": f"Rencana sama, dua reksa dana: $10,000 di awal plus $500 per bulan selama 30 tahun, dengan asumsi 7% per tahun. Dengan biaya tahunan 0.05% hasilnya sekitar ${low/1e3:,.0f}K; dengan biaya 1%, sekitar ${high/1e3:,.0f}K. "
                          "Biaya tahunan ini disebut expense ratio dan tercantum di fact sheet reksa dana."},
        "de": {"title": "1% Fondsgebühr kann Sie $120,000 kosten. So funktioniert's",
               "summary": f"Gleicher Plan, zwei Fonds: $10,000 zum Start plus $500 im Monat über 30 Jahre, bei angenommenen 7% pro Jahr. Mit 0.05% Jahresgebühr hätten Sie am Ende etwa ${low/1e3:,.0f}K, mit 1% etwa ${high/1e3:,.0f}K. "
                          "Diese jährliche Gebühr heißt Kostenquote (Expense Ratio) und steht im Factsheet des Fonds."},
        "fr": {"title": "Des frais de 1 % peuvent vous coûter $120,000. Voici comment",
               "summary": f"Même plan, deux fonds : $10,000 au départ plus $500 par mois pendant 30 ans, à 7 % par an supposés. Avec 0.05 % de frais annuels, vous finiriez avec environ ${low/1e3:,.0f}K ; avec 1 %, environ ${high/1e3:,.0f}K. "
                          "Ces frais annuels s'appellent le ratio de frais (expense ratio) et figurent sur la fiche du fonds."},
    },
    "scenes": [
        {"say": "A one percent fee sounds tiny. On this plan, it could cost you over a hundred and twenty thousand dollars.",
         "visual": {"type": "equation", "title": "A \"tiny\" fee",
                    "lines": [{"text": "1% a year", "color": "text", "size": 110},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"−${gap/1e3:,.0f}K", "color": "red", "size": 150}]}},
        {"say": "The plan: ten thousand dollars to start, plus five hundred a month, for thirty years.",
         "visual": {"type": "photo", "file": "assets/photos/retired_couple_hand_in_hand.jpg", "title": "The plan",
                    "value": "$500/mo", "label": "+ $10,000 to start, for 30 years", "color": "gold",
                    "focus": [0.5, 0.45]}},
        {"say": "Assume it earns seven percent a year before fees. Real returns vary.",
         "visual": {"type": "stat", "value": "7%", "label": "assumed yearly return, before fees",
                    "sub": "real returns vary · not guaranteed", "color": "gold"}},
        {"say": "Fund A charges five hundredths of a percent a year. Fund B charges one percent.",
         "visual": {"type": "pair", "title": "Two funds, same plan",
                    "left": {"label": "A", "sub": "0.05% a year", "color": "green"},
                    "right": {"label": "B", "sub": "1% a year", "color": "red"}}},
        {"say": "After thirty years: Fund A, nearly six hundred and ninety thousand. Fund B, about five hundred and sixty.",
         "visual": {"type": "compare", "title": "After 30 years",
                    "left": {"label": "Fund A", "value": low, "color": "green"},
                    "right": {"label": "Fund B", "value": high, "color": "red"}}},
        {"say": "Fund B takes over sixty-two thousand in fees. Fund A, about thirty-six hundred.",
         "visual": {"type": "bars", "title": "Fees paid over 30 years",
                    "items": [{"label": "Fund A", "value": low_paid, "color": "green"},
                              {"label": "Fund B", "value": high_paid, "color": "red"}]}},
        {"say": "That's over a hundred and twenty thousand dollars, gone to fees and the growth they took with them.",
         "visual": {"type": "photo", "file": "assets/photos/dollar_bills_100s.jpg", "value": f"${gap/1e3:,.0f}K",
                    "label": "lost to fees + the growth they took", "color": "red", "focus": [0.5, 0.5]}},
        {"say": "That yearly fee is called the expense ratio. Check it on the fund's fact sheet before you invest.",
         "visual": {"type": "equation", "title": "Before you invest",
                    "lines": [{"text": "Check the", "color": "muted", "size": 72},
                              {"text": "EXPENSE RATIO", "color": "gold", "size": 104},
                              {"text": "on the fund's fact sheet", "color": "muted", "size": 56}]}},
        {"say": "Follow for the next breakdown.",
         "visual": {"type": "cta", "lines": ["Small fees.", "Big bills."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "024_expense_ratio.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
