"""Video 034 (global/US): what a Fed rate change does to your loans and savings. Pillar: How Markets Work."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Federal Reserve FOMC statement, Sept 16, 2026: "raise the target range for the federal funds rate by
# 1/4 percentage point to 3-3/4 to 4 percent". FOMC statement, Oct 28, 2026: "maintain the target range for the
# federal funds rate at 3-3/4 to 4 percent" (federalreserve.gov press releases monetary20260916a / monetary20261028a).
FED_LOW, FED_HIGH = 3.75, 4.00
HIKE_SEP_2026 = 0.25
RANGE_DATE = "Oct 28, 2026"

# ---------------------------------------------------------------- illustrative example (assumptions, not sourced)
LOAN, YEARS = 300_000, 30
RATE_BEFORE = 0.06
RATE_AFTER = RATE_BEFORE + HIKE_SEP_2026 / 100
SAVINGS = 10_000

def payment(principal, annual_rate, years):
    r, n = annual_rate / 12, years * 12
    return principal * r / (1 - (1 + r) ** -n)

pay_before = payment(LOAN, RATE_BEFORE, YEARS)
pay_after = payment(LOAN, RATE_AFTER, YEARS)
extra_month = pay_after - pay_before
extra_year = extra_month * 12
extra_interest_savings = SAVINGS * HIKE_SEP_2026 / 100

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert (FED_LOW, FED_HIGH) == (3.75, 4.00)                       # "three and three quarters to four percent"
assert abs(RATE_AFTER - 0.0625) < 1e-12                          # "six to six and a quarter percent"
assert round(pay_before) == 1799 and round(pay_after) == 1847, (pay_before, pay_after)
assert abs(extra_month - 48.50) < 0.01, extra_month             # "about forty-eight dollars fifty a month"
assert 550 < extra_year < 600, extra_year                        # (yearly extra; no longer spoken)
assert abs(extra_interest_savings - 25) < 1e-9                   # "twenty-five dollars more a year"
print(f"payment ${pay_before:,.2f} -> ${pay_after:,.2f} (+${extra_month:.2f}/mo, +${extra_year:.0f}/yr); "
      f"savings +${extra_interest_savings:.0f}/yr")

spec = {
    "id": "034_rates_and_you",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": f"Loan example is illustrative · Fed range as of {RANGE_DATE}",
    "title": "Fed Rate Hike Explained: What It Does to Your Loan",
    "description": (
        "What does a Federal Reserve interest rate change mean for you? The Fed raised its federal funds target "
        f"range by a quarter point to 3.75%-4% on Sept 16, 2026, and held it there on {RANGE_DATE}. Variable-rate "
        f"loans and credit cards tend to follow (adjustable loans at their next reset): on a ${LOAN:,} loan over {YEARS} years, going from 6% to 6.25% "
        f"raises the monthly payment from about ${pay_before:,.0f} to ${pay_after:,.0f}. Fixed-rate loans you already "
        "have don't change, and savings rates tend to rise, often slowly.\n\n"
        "Sources: Federal Reserve FOMC statements of Sept 16, 2026 and Oct 28, 2026 (federalreserve.gov). The loan "
        "and savings figures are illustrative examples computed for this video, not offers or forecasts; the Fed's "
        "range may have changed since. Not financial advice.\n\n"
        "#interestrates #federalreserve #personalfinance #loans #economy"
    ),
    "tags": ["fed rate hike", "federal funds rate", "interest rates explained", "variable rate loan",
             "how fed rates affect you", "savings rates", "federal reserve", "personal finance"],
    "localizations": {
        "es": {"title": "Subida de tasas de la Fed: qué le pasa a tu préstamo",
               "summary": "La Fed subió su tasa a 3,75%-4% en septiembre de 2026. En un préstamo variable de $300,000 a 30 "
                          "años, pasar de 6% a 6,25% sube la cuota unos $48.50 al mes."},
        "pt": {"title": "Alta de juros do Fed: o que acontece com seu empréstimo",
               "summary": "O Fed elevou sua taxa para 3,75%-4% em setembro de 2026. Num empréstimo variável de $300.000 em 30 "
                          "anos, passar de 6% para 6,25% aumenta a parcela em cerca de $48,50 por mês."},
        "hi": {"title": "Fed की ब्याज दर बढ़ी: आपके लोन पर क्या असर होता है?",
               "summary": "Fed ने सितंबर 2026 में दर 3.75%-4% की। 30 साल के $300,000 के वेरिएबल लोन पर 6% से 6.25% होने पर "
                          "किस्त लगभग $48.50 महीना बढ़ जाती है।"},
        "id": {"title": "Suku Bunga The Fed Naik: Apa Dampaknya pada Pinjamanmu",
               "summary": "The Fed menaikkan suku bunga ke 3,75%-4% pada September 2026. Pada pinjaman variabel $300.000 selama "
                          "30 tahun, naik dari 6% ke 6,25% menambah cicilan sekitar $48,50 per bulan."},
        "de": {"title": "Fed-Zinserhöhung erklärt: Was sie mit deinem Kredit macht",
               "summary": "Die Fed hob ihren Leitzins im September 2026 auf 3,75 bis 4 %. Steigt der Zins eines variablen Kredits über $300.000 "
                          "und 30 Jahre von 6 % auf 6,25 %, steigt die Monatsrate um etwa $48,50."},
        "fr": {"title": "Hausse des taux de la Fed : l'effet sur votre prêt",
               "summary": "La Fed a relevé son taux à 3,75 %-4 % en septembre 2026. Sur un prêt variable de 300 000 $ sur 30 ans, "
                          "passer de 6 % à 6,25 % augmente la mensualité d'environ 48,50 $."},
    },
    "thumbnail": {"big": "3.75%", "color": "gold",
                  "photo": {"file": "assets/photos/federal_reserve_building_blue_sky.jpg", "focus": [0.5, 0.4]}},
    "scenes": [
        {"say": "One decision in Washington can change your loan payment. The Fed's target rate is now three and three quarters to four percent, after a quarter point rise in September.",
         "visual": {"type": "photo", "file": "assets/photos/federal_reserve_building.jpg", "focus": [0.5, 0.45],
                    "title": "The Federal Reserve", "value": "3.75%", "label": "to 4%: the Fed's target range",
                    "color": "gold"}},
        {"say": "That's the rate banks charge each other overnight. When it rises, banks' prime rate usually follows, and so do credit cards and variable rate loans.",
         "visual": {"type": "equation", "title": "How it reaches you",
                    "lines": [{"text": "Fed rate ↑", "color": "gold", "size": 96},
                              {"text": "Banks' prime rate ↑", "color": "text", "size": 80},
                              {"text": "Cards & variable loans ↑", "color": "red", "size": 68}]}},
        {"say": "Say you owe three hundred thousand dollars over thirty years at a variable rate. If it rises from six to six and a quarter percent at its next reset, you pay about forty-eight dollars fifty more a month.",
         "visual": {"type": "compare", "title": f"Monthly payment, ${LOAN // 1000}K over {YEARS} yrs",
                    "left": {"label": "At 6%", "value": pay_before, "color": "slate"},
                    "right": {"label": "At 6.25%", "value": pay_after, "color": "red"}}},
        {"say": "A fixed rate loan you already have? No change.",
         "visual": {"type": "photo", "file": "assets/photos/suburban_houses_texas.jpg", "focus": [0.5, 0.5],
                    "title": "Loans you already have", "value": "No change", "label": "on a fixed-rate loan",
                    "color": "green"}},
        {"say": "Savers can win. If your bank passed on the full quarter point, ten thousand dollars in savings would earn twenty-five dollars more a year. Banks often pass it on slowly. And cuts work in reverse.",
         "visual": {"type": "equation", "title": "If your bank passes it on",
                    "lines": [{"text": "$10,000 × 0.25%", "color": "text", "size": 92},
                              {"text": f"= ${extra_interest_savings:.0f} more a year", "color": "green", "size": 92}]}},
        {"say": "Save this for later, and follow for more.",
         "visual": {"type": "cta", "lines": ["One rate.", "Your wallet."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "034_rates_and_you.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
