"""Video 031 (global/USD): the real cost of a $35,000 car loan, 72 vs 48 months, plus the 20/4/10 guideline.
Example APR, all maths computed here."""
import json, os

PRICE = 35_000
APR = 0.07                 # example APR, same for both terms so only the length changes
r = APR / 12

def payment(principal, months):
    """Standard amortising loan payment."""
    return principal * r / (1 - (1 + r) ** -months)

p72, p48 = payment(PRICE, 72), payment(PRICE, 48)
tot72, tot48 = p72 * 72, p48 * 48
int72, int48 = tot72 - PRICE, tot48 - PRICE
extra = int72 - int48

# 20/4/10 rule of thumb: 20% down, loan of 4 years or less, car costs under 10% of gross income
DOWN, RULE_MONTHS, RULE_SHARE = 0.20, 48, 0.10
loan_rule = PRICE * (1 - DOWN)
p_rule = payment(loan_rule, RULE_MONTHS)
income_needed = p_rule * 12 / RULE_SHARE   # payment alone; insurance etc. would push this higher

assert 42_900 < tot72 < 43_000, tot72          # "almost forty-three thousand"
assert 596 < p72 < 597, p72                    # "about five hundred ninety-seven a month"
assert 838 < p48 < 839, p48                    # "about eight hundred thirty-eight"
assert 7_900 < int72 < 8_000, int72            # "almost eight thousand in interest"
assert 5_200 < int48 < 5_250, int48            # "about fifty-two hundred"
assert 2_700 < extra < 2_750, extra            # "over twenty-seven hundred dollars more"
assert loan_rule == 28_000
assert 670 < p_rule < 671, p_rule              # "about six hundred seventy a month"
assert 80_000 < income_needed < 81_000, income_needed   # "over eighty thousand dollars a year"
print(f"72m ${p72:,.2f}/mo total ${tot72:,.0f} int ${int72:,.0f} | 48m ${p48:,.2f}/mo total ${tot48:,.0f} "
      f"int ${int48:,.0f} | extra ${extra:,.0f} | rule pay ${p_rule:,.2f} income ${income_needed:,.0f}")

spec = {
    "id": "031_car_loan_cost",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "disclaimer": "Example · 7% APR on both loans · your rate and costs will differ",
    "title": "Car Loan Math: 72 vs 48 Months on a $35,000 Car",
    "description": (
        "A 72-month car loan makes the monthly payment look smaller, but you pay more in total. "
        f"On a $35,000 car at an example 7% APR, 72 months costs about ${int72:,.0f} in interest versus "
        f"about ${int48:,.0f} over 48 months: roughly ${extra:,.0f} more for the same car. We also run the "
        "20/4/10 rule of thumb.\n\n"
        "Assumptions: $35,000 borrowed in full, 7% APR on both terms (an example; real rates depend on your credit "
        "and the lender, and longer loans can carry different rates), fixed monthly payments, no fees, taxes or "
        "add-ons. The 20/4/10 rule is a common guideline, not a law: put 20% down, borrow for 4 years or less, and "
        "keep car costs under 10% of gross income. The income figure uses the loan payment alone. "
        "Not financial advice.\n\n"
        "#carloan #personalfinance #debt #moneytips #financialliteracy"
    ),
    "tags": ["car loan", "auto loan", "72 month car loan", "car payment", "20/4/10 rule", "how much car can I afford",
             "car loan interest", "personal finance", "money tips"],
    "localizations": {
        "es": {"title": "Préstamo de auto: 72 vs 48 meses por un auto de $35,000",
               "summary": f"Con una tasa de ejemplo del 7%, el préstamo a 72 meses cuesta unos ${int72:,.0f} en intereses, "
                          f"frente a ${int48:,.0f} a 48 meses. Además, la regla 20/4/10."},
        "pt": {"title": "Financiamento de carro: 72 x 48 meses em um carro de $35,000",
               "summary": f"Com juros de exemplo de 7% ao ano, 72 meses custam cerca de ${int72:,.0f} em juros, "
                          f"contra ${int48:,.0f} em 48 meses. E a regra 20/4/10."},
        "hi": {"title": "कार लोन का गणित: $35,000 की कार, 72 बनाम 48 महीने",
               "summary": f"7% के उदाहरण APR पर 72 महीने के लोन में करीब ${int72:,.0f} ब्याज लगता है, "
                          f"जबकि 48 महीने में ${int48:,.0f}। साथ में 20/4/10 नियम।"},
        "id": {"title": "Hitung Kredit Mobil: 72 vs 48 Bulan untuk Mobil $35,000",
               "summary": f"Dengan contoh bunga 7% per tahun, tenor 72 bulan memakan bunga sekitar ${int72:,.0f}, "
                          f"dibanding ${int48:,.0f} untuk 48 bulan. Plus aturan 20/4/10."},
        "de": {"title": "Autokredit: 72 vs. 48 Monate bei einem $35,000-Auto",
               "summary": f"Bei einem Beispielzins von 7% kosten 72 Monate rund ${int72:,.0f} Zinsen, "
                          f"48 Monate nur ${int48:,.0f}. Dazu die 20/4/10-Faustregel."},
        "fr": {"title": "Crédit auto : 72 ou 48 mois pour une voiture à $35,000",
               "summary": f"Avec un taux d'exemple de 7 %, 72 mois coûtent environ ${int72:,.0f} d'intérêts, "
                          f"contre ${int48:,.0f} sur 48 mois. Plus la règle 20/4/10."},
    },
    "scenes": [
        {"say": "A thirty-five thousand dollar car can cost you almost forty-three thousand. Here's how.",
         "visual": {"type": "equation", "title": "The real price",
                    "lines": [{"text": "$35,000 car", "color": "text", "size": 110},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"${tot72:,.0f} paid", "color": "red", "size": 130}]}},
        {"say": "Take a seventy-two month loan at an example seven percent A-P-R. The payment looks friendly: about five hundred ninety-seven a month.",
         "visual": {"type": "stat", "value": f"${p72:,.0f}", "label": "a month for 72 months",
                    "sub": "$35,000 at 7% APR (example)", "color": "gold"}},
        {"say": "Over forty-eight months, it's about eight hundred thirty-eight.",
         "visual": {"type": "compare", "title": "Monthly payment",
                    "left": {"label": "72 months", "value": p72, "color": "green"},
                    "right": {"label": "48 months", "value": p48, "color": "slate"}}},
        {"say": "But look at the interest. Seventy-two months: almost eight thousand dollars. Forty-eight months: about fifty-two hundred.",
         "visual": {"type": "bars", "title": "Total interest paid",
                    "items": [{"label": "72 mo", "value": int72, "color": "red"},
                              {"label": "48 mo", "value": int48, "color": "slate"}]}},
        {"say": "Same car, same rate. Two extra years of payments cost you over twenty-seven hundred dollars more.",
         "visual": {"type": "stat", "value": f"+${extra/1e3:.1f}K", "label": "extra interest for 2 more years",
                    "sub": "same car · same rate", "color": "red"}},
        {"say": "A common guideline: twenty percent down, four years at most, and car costs under ten percent of your gross income.",
         "visual": {"type": "equation", "title": "The 20/4/10 guideline",
                    "lines": [{"text": "20% down", "color": "green", "size": 96},
                              {"text": "4 years max", "color": "gold", "size": 96},
                              {"text": "10% of income", "color": "text", "size": 96}]}},
        {"say": "For this car, that's a payment of about six hundred seventy a month. By that guide, you'd want to earn over eighty thousand dollars a year, before even counting insurance.",
         "visual": {"type": "compare", "title": "This car, by 20/4/10",
                    "left": {"label": "Payment", "value": p_rule, "color": "gold"},
                    "right": {"label": "Income / yr", "value": income_needed, "color": "green"}}},
        {"say": "Look past the monthly payment. Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Check the", "total cost."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "031_car_loan_cost.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
