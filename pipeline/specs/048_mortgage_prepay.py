"""Video 048 (global/US): one extra mortgage payment a year, what it saves on a $400K 30-year loan.
Pillar: Money Math. Rate is sourced (Freddie Mac PMMS); every other number is computed here."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Freddie Mac Primary Mortgage Market Survey (freddiemac.com/pmms, read 2026-11-25): "The 30-year fixed-rate
# mortgage averaged 7.28% as of November 19, 2026, up from last week when it averaged 7.11%. A year ago at this
# time, the 30-year FRM averaged 6.26%."
RATE = 0.0728
RATE_DATE = "Nov 19, 2026"

# ---------------------------------------------------------------- example loan (assumptions)
LOAN, YEARS = 400_000, 30
r, N = RATE / 12, YEARS * 12

def payment(principal):
    """Standard fixed-rate monthly payment (principal + interest only; no taxes or insurance)."""
    return principal * r / (1 - (1 + r) ** -N)

pay = payment(LOAN)
interest_normal = pay * N - LOAN

def amortise(extra_every_12=False):
    """Month-by-month schedule. With the extra, one more full monthly payment goes to principal each 12th month.
    Returns (months to pay off, total interest, total extra paid, year-end balances)."""
    bal, m, interest, extra_paid, yearly = float(LOAN), 0, 0.0, 0.0, [float(LOAN)]
    while bal > 0.005:
        m += 1
        i = bal * r
        interest += i
        bal -= min(pay - i, bal)
        if extra_every_12 and m % 12 == 0 and bal > 0:
            x = min(pay, bal)
            bal -= x
            extra_paid += x
        if m % 12 == 0:
            yearly.append(max(bal, 0.0))
    if m % 12:
        yearly.append(0.0)
    return m, interest, extra_paid, yearly

m0, int0, _, bal_normal = amortise(False)
m1, int1, extra_paid, bal_extra = amortise(True)
saved = int0 - int1
months_early = m0 - m1

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert m0 == N and abs(int0 - interest_normal) < 0.01              # schedule matches the formula
assert round(RATE * 100, 1) == 7.3                                  # "about seven point three percent"
assert 2_735 < pay < 2_740, pay                                     # "about twenty-seven hundred forty a month"
assert 585_000 < interest_normal < 586_000, interest_normal         # "about five hundred eighty-five thousand"
assert interest_normal > LOAN                                       # "more than you borrowed"
assert m1 == 23 * 12 + 9, m1                                        # "twenty-three years and nine months"
assert 72 <= months_early < 78, months_early                        # "about six years early"
assert 142_500 < saved < 143_500, saved                             # "about one hundred forty-three thousand"
assert 62_000 < extra_paid < 63_500, extra_paid                     # "about sixty-three thousand extra" (description)
print(f"pay ${pay:,.2f}; interest ${int0:,.0f} -> ${int1:,.0f}; saved ${saved:,.0f}; payoff {m1} months "
      f"({months_early} early); extra paid ${extra_paid:,.0f}")

years_axis = list(range(0, YEARS + 1))
bal_extra_full = bal_extra + [0.0] * (len(years_axis) - len(bal_extra))
assert len(bal_normal) == len(years_axis) == len(bal_extra_full)

spec = {
    "id": "048_mortgage_prepay",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "thumbnail": {"big": f"${interest_normal/1e3:,.0f}K", "line": "More than you borrowed", "color": "red",
                  "photo": {"file": "assets/photos/single_family_home_brick.jpg", "focus": [0.45, 0.5]}},
    "disclaimer": f"Example · {RATE*100:.2f}% avg rate (Freddie Mac, {RATE_DATE}) · yours will differ",
    "title": "One Extra Mortgage Payment a Year: $143K Saved?",
    "description": (
        "What does one extra mortgage payment a year save? On a $400,000, 30-year fixed loan at 7.28% (the US "
        f"average in late November 2026), the monthly payment is about ${pay:,.0f} and total interest is about "
        f"${interest_normal/1e3:,.0f}K. Adding one extra monthly payment each year pays the loan off in 23 years and "
        f"9 months, about 6 years early, and cuts interest by about ${saved/1e3:,.0f}K, for about "
        f"${extra_paid/1e3:,.0f}K of extra payments.\n\n"
        "Source: Freddie Mac Primary Mortgage Market Survey, 30-year fixed-rate average of 7.28% as of Nov 19, 2026 "
        "(freddiemac.com/pmms).\n\n"
        "Assumptions (our own example): principal and interest only (no property tax, insurance or PMI), the extra "
        "payment is made once a year and applied fully to principal, rate fixed for the whole loan. Interest saved "
        "is in plain dollars, not adjusted for inflation or for what that money could have earned elsewhere. Before "
        "prepaying, check your loan has no prepayment penalty, tell your lender to apply extra money to principal, "
        "and keep an emergency fund and pay off higher-interest debt first. Not financial advice.\n\n"
        "#mortgage #homebuying #personalfinance #debtfree #realestate"
    ),
    "tags": ["extra mortgage payment", "pay off mortgage early", "mortgage prepayment", "one extra payment a year",
             "mortgage interest", "30 year mortgage", "mortgage rates", "personal finance", "money math"],
    "localizations": {
        "es": {"title": "Un pago extra de hipoteca al año: ¿$143K ahorrados?",
               "summary": f"Hipoteca de $400.000 a 30 años al 7,28%: un pago extra al año la liquida en 23 años y 9 meses "
                          f"y ahorra unos ${saved/1e3:,.0f}K en intereses."},
        "pt": {"title": "Uma parcela extra do financiamento por ano: US$143 mil?",
               "summary": f"Financiamento de US$400 mil em 30 anos a 7,28%: uma parcela extra por ano quita em 23 anos e 9 "
                          f"meses e economiza cerca de US${saved/1e3:,.0f} mil em juros."},
        "hi": {"title": "साल में एक एक्स्ट्रा होम लोन EMI: $143K की बचत?",
               "summary": f"$400,000 का 30 साल का होम लोन, 7.28% ब्याज: साल में एक एक्स्ट्रा किस्त से लोन 23 साल 9 महीने में "
                          f"खत्म और लगभग ${saved/1e3:,.0f}K ब्याज की बचत।"},
        "id": {"title": "Satu Cicilan KPR Ekstra per Tahun: Hemat $143 Ribu?",
               "summary": f"KPR $400.000 tenor 30 tahun bunga 7,28%: satu cicilan ekstra per tahun melunasinya dalam 23 tahun "
                          f"9 bulan dan menghemat sekitar ${saved/1e3:,.0f} ribu bunga."},
        "de": {"title": "Eine Extra-Rate pro Jahr: 143.000 $ Zinsen gespart?",
               "summary": f"Hypothek über 400.000 $, 30 Jahre, 7,28 %: Eine zusätzliche Monatsrate pro Jahr tilgt sie in "
                          f"23 Jahren und 9 Monaten und spart rund {saved/1e3:,.0f}.000 $ Zinsen."},
        "fr": {"title": "Une mensualité de prêt en plus par an : 143 000 $ ?",
               "summary": f"Prêt immobilier de 400 000 $ sur 30 ans à 7,28 % : une mensualité en plus par an le solde en "
                          f"23 ans et 9 mois et économise environ {saved/1e3:,.0f} 000 $ d'intérêts."},
    },
    "scenes": [
        # hook: payoff number on frame 0 + open loop (how?)
        {"say": "One extra mortgage payment a year: about one hundred forty-three thousand saved.",
         "visual": {"type": "photo", "file": "assets/photos/houses_dc_logan_circle.jpg", "title": "One extra payment a year",
                    "value": f"${saved/1e3:,.0f}K", "label": "interest saved · $400K, 30 years", "color": "green",
                    "focus": [0.5, 0.45]}},
        {"say": "Late November's average American rate: about seven point three percent.",
         "visual": {"type": "equation", "title": "30-year fixed, US average",
                    "lines": [{"text": f"{RATE*100:.2f}%", "color": "gold", "size": 150},
                              {"text": f"Freddie Mac · {RATE_DATE}", "color": "muted", "size": 50}]}},
        {"say": "Borrow four hundred thousand for thirty years: about twenty-seven hundred forty a month.",
         "visual": {"type": "photo", "file": "assets/photos/house_keys_on_money.jpg", "title": "The loan",
                    "value": f"${pay:,.0f}/mo", "label": "$400K borrowed for 30 years", "color": "gold",
                    "focus": [0.5, 0.5]}},
        {"say": "Interest alone: about five hundred eighty-five thousand.",
         "visual": {"type": "compare", "title": "Over 30 years", "format": "usd",
                    "left": {"label": "Borrowed", "value": LOAN, "color": "blue"},
                    "right": {"label": "Interest", "value": round(interest_normal, -3), "color": "red"}}},
        {"say": "More than you borrowed. The trick: thirteen payments a year, not twelve.",
         "visual": {"type": "equation", "title": "The trick",
                    "lines": [{"text": "12 payments a year", "color": "muted", "size": 84},
                              {"text": "→ 13", "color": "gold", "size": 150}]}},
        {"say": "The extra goes straight to the balance, so interest shrinks.",
         "visual": {"type": "pair", "title": "Where the extra goes",
                    "left": {"label": "Balance", "sub": "goes down faster", "color": "green"},
                    "right": {"label": "Interest", "sub": "shrinks with it", "color": "red"}}},
        {"say": "Debt-free in twenty-three years and nine months, about six years early.",
         "visual": {"type": "line", "title": "Loan balance", "x": years_axis, "x_label": "year", "format": "usd",
                    "series": [{"label": "12 payments", "values": [round(v) for v in bal_normal], "color": "slate"},
                               {"label": "13 payments", "values": [round(v) for v in bal_extra_full], "color": "green"}]}},
        {"say": "Total interest falls to about four hundred forty-two thousand.",
         "visual": {"type": "bars", "title": "Total interest paid", "format": "usd",
                    "items": [{"label": "12 a year", "value": round(int0, -3), "color": "red"},
                              {"label": "13 a year", "value": round(int1, -3), "color": "green"}]}},
        {"say": "First, check for prepayment penalties, and keep an emergency fund.",
         "visual": {"type": "photo", "file": "assets/photos/piggy_bank_coins.jpg", "title": "Before you do it",
                    "label": "No penalty? Emergency fund ready?", "focus": [0.55, 0.5]}},
        # loop line: runs back into "One extra mortgage payment a year..."
        {"say": "Thirteen payments instead of twelve. That's all it takes.",
         "visual": {"type": "cta", "lines": ["13 payments,", "not 12."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
assert 441_500 < int1 < 442_500, int1                               # "about four hundred forty-two thousand"
# ---------------------------------------------------------------- retention checks (AUTOPILOT "Retention rules")
words = [len(s["say"].split()) for s in spec["scenes"]]
for s in spec["scenes"]:
    assert len(s["say"].split()) <= 14, s["say"]                        # one visual per ~4 s
assert len(spec["scenes"][0]["say"].split()) <= 12                         # hook: payoff first, ~2 s
for a, b in zip(spec["scenes"], spec["scenes"][1:]):
    assert a["visual"]["type"] != b["visual"]["type"], a["say"]           # never the same visual twice in a row
assert 80 <= sum(words) <= 105, sum(words)                                 # ~30-40 s
assert "follow" not in spec["scenes"][-1]["say"].lower()                   # loop line, not a spoken CTA
print(f"{len(words)} scenes, {sum(words)} words (~{sum(words) / 2.9:.0f} s)")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "048_mortgage_prepay.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
