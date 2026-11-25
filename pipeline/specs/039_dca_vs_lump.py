"""Video 039 (global/USD): lump sum vs investing in monthly steps.
Historical win rates are sourced constants (Vanguard, Feb 2023); the $12,000 example is computed here."""
import json, os

# --- sourced: Vanguard research, Finlay & Zorn, "Cost averaging: Invest now or temporarily hold your cash?",
#     February 2023. https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf
#     (read 2026-11-22). Figure 2: lump sum beat cost averaging 68% of the time; cost averaging beat staying
#     in cash 69% of the time. Basis: MSCI World Index returns 1976-2022, 100% equity, a lump sum vs. splitting
#     it into three equal monthly parts, wealth compared after one year on a rolling basis.
#     The paper's summary: lump sum beat cost averaging "two-thirds of the time"; cost averaging can limit
#     drawdown and investor regret in a severe downturn, but with lower expected returns.
LS_BEATS_CA = 68         # %
CA_BEATS_CASH = 69       # %
STUDY_FROM, STUDY_TO = 1976, 2022

# --- illustration (computed): $12,000 now vs. $1,000 at the start of each month, steady 7% a year,
#     uninvested cash earns nothing (same simplification as the Vanguard paper), value after 12 months.
TOTAL, MONTHS, ANNUAL = 12_000, 12, 0.07
g = (1 + ANNUAL) ** (1 / 12)
lump = TOTAL * (1 + ANNUAL)
monthly = sum(TOTAL / MONTHS * g ** (MONTHS - k) for k in range(MONTHS))
ahead = lump - monthly

assert abs(LS_BEATS_CA / 100 - 2 / 3) < 0.02           # "about two-thirds of the time"
assert abs(lump - 12_840) < 1e-6                         # "twelve thousand eight hundred forty"
assert 12_440 < monthly < 12_460, monthly                # "about twelve thousand four hundred fifty"
assert 385 < ahead < 395, ahead                          # "about three hundred ninety dollars ahead"
assert TOTAL / MONTHS == 1_000                           # "a thousand a month"
print(f"lump ${lump:,.0f}  monthly ${monthly:,.0f}  ahead ${ahead:,.0f}")

spec = {
    "id": "039_dca_vs_lump",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "disclaimer": "Past results don't guarantee future returns · not financial advice",
    "title": "Lump Sum vs Dollar-Cost Averaging: Which Wins More?",
    "description": (
        "Lump sum vs dollar-cost averaging: if you already have the cash, investing it all at once has beaten "
        f"splitting it into three monthly parts about two-thirds of the time ({LS_BEATS_CA}% in Vanguard's study of "
        f"global stocks, {STUDY_FROM}–{STUDY_TO}), because stocks usually beat cash. Splitting it over three months "
        f"still beat sitting in cash {CA_BEATS_CASH}% of the time, and it can make a drop easier to live with.\n\n"
        "Sources:\n"
        "- Vanguard, Finlay & Zorn, \"Cost averaging: Invest now or temporarily hold your cash?\", February 2023 "
        "(MSCI World Index returns 1976–2022, 100% stocks, lump sum vs. three equal monthly parts, compared after one "
        "year): https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf\n\n"
        "Our own example (not from the Vanguard study): $12,000 invested at once vs. $1,000 at the start of each month for 12 months, a steady "
        "7% yearly return, uninvested cash earns nothing, no fees or taxes. Real markets don't move steadily; returns "
        "vary, can be negative, and past results don't guarantee future returns. Not financial advice.\n\n"
        "#investing #dollarcostaveraging #personalfinance #stockmarket #moneytips"
    ),
    "tags": ["lump sum vs dollar cost averaging", "dollar cost averaging", "lump sum investing", "investing basics",
             "Vanguard research", "stock market", "personal finance", "money tips", "financial literacy"],
    "localizations": {
        "es": {"title": "Todo de una vez o cada mes: ¿qué gana más al invertir?",
               "summary": f"Según Vanguard (acciones globales, {STUDY_FROM}–{STUDY_TO}), invertir todo de una vez ganó "
                          f"a repartirlo el {LS_BEATS_CA}% de las veces. Pero repartirlo superó al efectivo el {CA_BEATS_CASH}%."},
        "pt": {"title": "Tudo de uma vez ou todo mês: o que rende mais?",
               "summary": f"Segundo a Vanguard (ações globais, {STUDY_FROM}–{STUDY_TO}), investir tudo de uma vez venceu "
                          f"o aporte parcelado em {LS_BEATS_CA}% das vezes. Mas parcelar venceu o dinheiro parado em {CA_BEATS_CASH}%."},
        "hi": {"title": "एकमुश्त निवेश या हर महीने: कौन ज़्यादा जीतता है?",
               "summary": f"Vanguard के अध्ययन ({STUDY_FROM}–{STUDY_TO}, ग्लोबल शेयर) में एकमुश्त निवेश {LS_BEATS_CA}% बार "
                          f"किस्तों से आगे रहा। फिर भी किस्तों में निवेश {CA_BEATS_CASH}% बार नकद रखने से बेहतर रहा।"},
        "id": {"title": "Sekaligus atau Bertahap: Mana yang Lebih Sering Menang?",
               "summary": f"Menurut riset Vanguard (saham global, {STUDY_FROM}–{STUDY_TO}), investasi sekaligus menang "
                          f"{LS_BEATS_CA}% dari waktu. Tapi investasi bertahap tetap mengalahkan uang tunai {CA_BEATS_CASH}% dari waktu."},
        "de": {"title": "Einmalanlage oder Sparplan: Was gewinnt öfter?",
               "summary": f"Laut Vanguard (globale Aktien, {STUDY_FROM}–{STUDY_TO}) schlug die Einmalanlage das gestaffelte "
                          f"Investieren in {LS_BEATS_CA}% der Fälle. Gestaffelt schlug aber Bargeld in {CA_BEATS_CASH}% der Fälle."},
        "fr": {"title": "Tout investir d'un coup ou chaque mois : qui gagne ?",
               "summary": f"Selon Vanguard (actions mondiales, {STUDY_FROM}–{STUDY_TO}), investir d'un coup a battu "
                          f"l'investissement étalé {LS_BEATS_CA} % du temps. Mais étaler a battu le cash {CA_BEATS_CASH} % du temps."},
    },
    "thumbnail": {"photo": {"file": "assets/photos/nyse_traders_gotfryd.jpg", "focus": [0.5, 0.5]},
                  "big": f"{LS_BEATS_CA}%", "color": "gold"},
    "scenes": [
        {"say": "You have twelve thousand dollars to invest. All at once, or a thousand a month? History has a favorite.",
         "visual": {"type": "pair", "title": "$12,000 to invest",
                    "left": {"label": "All now", "sub": "one lump sum", "color": "gold"},
                    "right": {"label": "Monthly", "sub": "$1,000 × 12", "color": "blue"}}},
        {"say": "Vanguard studied global stocks from nineteen seventy-six to twenty twenty-two. Investing all at once beat splitting it over three months about two-thirds of the time.",
         "visual": {"type": "photo", "file": "assets/photos/nyse_trading_floor_gotfryd.jpg",
                    "title": f"Vanguard · global stocks · {STUDY_FROM}–{STUDY_TO}",
                    "value": f"{LS_BEATS_CA}%", "color": "gold", "label": "of the time, lump sum beat 3 monthly parts",
                    "focus": [0.5, 0.45]}},
        {"say": "Why? Stocks usually beat cash. So money waiting on the sidelines usually missed growth.",
         "visual": {"type": "equation", "title": "Why lump sum usually wins",
                    "lines": [{"text": "Stocks usually", "color": "text", "size": 80},
                              {"text": "beat cash", "color": "green", "size": 110},
                              {"text": "Cash waiting = missed growth", "color": "red", "size": 64}]}},
        {"say": "In our own example, a steady seven percent year leaves all at once about three hundred ninety dollars ahead.",
         "visual": {"type": "compare", "title": "Our example: steady 7% year",
                    "left": {"label": "All now", "value": lump, "color": "gold"},
                    "right": {"label": "Monthly", "value": monthly, "color": "blue"}}},
        {"say": "But if the market drops right after you invest, spreading it out wins. And splitting it over three months still beat cash sixty-nine percent of the time.",
         "visual": {"type": "photo", "file": "assets/photos/stock_screens_tokyo_board.jpg",
                    "title": "If the market drops right after",
                    "value": f"{CA_BEATS_CASH}%", "color": "green", "label": "of the time, 3 monthly parts beat cash",
                    "focus": [0.5, 0.4]}},
        {"say": "So if fear of a crash would keep you in cash, investing in steps beats waiting. And if you invest from each paycheck, keep going. That's investing as soon as you can.",
         "visual": {"type": "equation", "title": "The real lesson",
                    "lines": [{"text": "Investing in steps", "color": "blue", "size": 88},
                              {"text": "beats", "color": "dim", "size": 72},
                              {"text": "waiting in cash", "color": "green", "size": 100}]}},
        {"say": "Follow if this changed how you think about money.",
         "visual": {"type": "cta", "lines": ["Time in", "the market."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "039_dca_vs_lump.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
