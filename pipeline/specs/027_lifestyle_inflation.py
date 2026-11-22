"""Video 027 (global/USD): lifestyle inflation. A $5,000 raise spent in full vs. half saved and invested.
Example assumptions, all maths computed here."""
import json, os

# --- example assumptions (labelled as an example on screen and in the description)
RAISE = 5_000          # yearly raise, before tax
TAX = 0.30             # example combined tax on the extra pay (e.g. 22% federal bracket + 7.65% payroll ≈ 30%)
SAVE_SHARE = 0.5       # Sam saves half of the after-tax raise
ANNUAL, YEARS = 0.07, 20
r = ANNUAL / 12

kept_y = RAISE * (1 - TAX)
kept_m = kept_y / 12
save_m = kept_m * SAVE_SHARE

def fv(months):
    """Future value of save_m invested at the start of each month, compounded monthly."""
    return save_m * (((1 + r) ** months - 1) / r) * (1 + r) if months > 0 else 0.0

years = list(range(0, YEARS + 1))
sam = [fv(y * 12) for y in years]
alex = [0.0 for _ in years]
SAM = sam[-1]
put_in = save_m * 12 * YEARS

assert abs(kept_y - 3_500) < 1e-6                 # "you keep three thousand five hundred a year"
assert 290 < kept_m < 300, kept_m                 # "almost three hundred dollars a month"
assert 145 < save_m < 146, save_m                 # "about one hundred forty-six a month" (145.83)
assert abs(put_in - 35_000) < 1e-6                # "thirty-five thousand of it put in"
assert 76_000 < SAM < 77_000, SAM                 # "about seventy-six thousand dollars"
assert SAM / put_in > 2                           # "more than double what Sam put in"
print(f"kept/yr ${kept_y:,.0f}  kept/mo ${kept_m:,.2f}  saved/mo ${save_m:,.2f}  Sam@20y ${SAM:,.0f}  put in ${put_in:,.0f}")

spec = {
    "id": "027_lifestyle_inflation",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY TRAP",
    "disclaimer": "Example · 30% tax · assumes 7% a year · not financial advice",
    "title": "Lifestyle Inflation: Why Your Raise Leaves You No Richer",
    "description": (
        "Lifestyle inflation is when spending rises as fast as your pay, so a raise leaves you no richer. "
        f"In this example, a $5,000 raise is about ${kept_m:,.0f} a month after tax. Spend it all on upgrades and "
        f"you have nothing extra in 20 years; save half and invest it, and it could grow to about ${SAM/1e3:,.0f}K, "
        "while you still enjoy the other half.\n\n"
        "Example assumptions: $5,000 yearly raise, 30% combined tax on the extra pay (yours will differ), half of the "
        f"after-tax raise (${save_m:,.2f} a month) invested at the start of every month for 20 years at an assumed 7% "
        "average yearly return compounded monthly, no fees or taxes on the investment, no further raises. "
        "Illustration only: real returns vary, can be negative, and are not guaranteed. Not financial advice.\n\n"
        "#personalfinance #lifestyleinflation #saving #investing #moneytips"
    ),
    "tags": ["lifestyle inflation", "lifestyle creep", "what to do with a raise", "saving money", "investing",
             "personal finance", "money tips", "financial literacy", "compound interest"],
    "localizations": {
        "es": {"title": "Inflación del estilo de vida: tu aumento no te enriquece",
               "summary": "Un aumento de $5,000 puede no hacerte más rico si tus gastos suben con él. "
                          f"Si ahorras la mitad y la inviertes al 7% supuesto, podría llegar a unos ${SAM/1e3:,.0f}K en 20 años."},
        "pt": {"title": "Inflação do estilo de vida: seu aumento não te enriquece",
               "summary": "Um aumento de $5,000 pode não te deixar mais rico se os gastos subirem junto. "
                          f"Poupando metade e investindo a 7% ao ano (suposição), pode virar cerca de ${SAM/1e3:,.0f}K em 20 anos."},
        "hi": {"title": "लाइफस्टाइल इन्फ्लेशन: बढ़ी सैलरी फिर भी अमीर क्यों नहीं",
               "summary": "अगर खर्च भी साथ में बढ़ें, तो $5,000 की बढ़ोतरी आपको अमीर नहीं बनाती। "
                          f"आधी बचत 7% अनुमानित रिटर्न पर निवेश करें, तो 20 साल में करीब ${SAM/1e3:,.0f}K बन सकते हैं।"},
        "id": {"title": "Inflasi Gaya Hidup: Kenapa Naik Gaji Tak Bikin Kaya",
               "summary": "Kenaikan gaji $5,000 bisa tidak membuat Anda lebih kaya jika pengeluaran ikut naik. "
                          f"Tabung separuhnya dan investasikan dengan asumsi 7% per tahun: sekitar ${SAM/1e3:,.0f}K dalam 20 tahun."},
        "de": {"title": "Lifestyle-Inflation: Warum die Gehaltserhöhung verpufft",
               "summary": "Eine Gehaltserhöhung von $5,000 macht nicht reicher, wenn die Ausgaben mitwachsen. "
                          f"Wer die Hälfte zu angenommenen 7% anlegt, könnte in 20 Jahren etwa ${SAM/1e3:,.0f}K haben."},
        "fr": {"title": "Inflation du mode de vie : pourquoi votre hausse s'évapore",
               "summary": "Une hausse de salaire de $5,000 ne vous enrichit pas si vos dépenses montent avec elle. "
                          f"En plaçant la moitié à 7 % supposés, elle pourrait atteindre environ ${SAM/1e3:,.0f}K en 20 ans."},
    },
    "scenes": [
        {"say": "You get a five thousand dollar raise. Twenty years later, you could be no richer at all.",
         "visual": {"type": "equation", "title": "The raise trap",
                    "lines": [{"text": "+$5,000 raise", "color": "green", "size": 110},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": "+$0 wealth", "color": "red", "size": 130}]}},
        {"say": "After an example thirty percent in taxes, you keep three thousand five hundred a year. Almost three hundred dollars a month.",
         "visual": {"type": "stat", "value": f"${kept_m:,.0f}", "label": "extra a month, after tax",
                    "sub": "$5,000 − 30% tax (example) = $3,500 a year", "color": "gold"}},
        {"say": "Alex spends all of it. A nicer car, more takeout, a pricier phone plan. Sam saves half and enjoys the rest.",
         "visual": {"type": "pair", "title": "Same raise, two choices",
                    "left": {"label": "Alex", "sub": "spends it all", "color": "red"},
                    "right": {"label": "Sam", "sub": "saves half", "color": "green"}}},
        {"say": "That's about one hundred forty-six dollars a month, invested at an assumed seven percent a year. Real returns vary.",
         "visual": {"type": "equation", "title": "Sam's plan",
                    "lines": [{"text": f"${save_m:,.0f} a month", "color": "green", "size": 110},
                              {"text": "at an assumed 7% a year", "color": "text", "size": 64},
                              {"text": "for 20 years", "color": "muted", "size": 64}]}},
        {"say": "Twenty years later, Sam has about seventy-six thousand dollars. Alex's upgrades just became normal life.",
         "visual": {"type": "line", "title": "Extra wealth from the raise", "x": years, "x_label": "years",
                    "series": [{"label": "Sam", "values": sam, "color": "green"},
                               {"label": "Alex", "values": alex, "color": "red"}]}},
        {"say": "And Sam only put in thirty-five thousand of it. The rest is growth.",
         "visual": {"type": "bars", "title": "Sam after 20 years",
                    "items": [{"label": "Put in", "value": put_in, "color": "slate"},
                              {"label": "Worth", "value": SAM, "color": "green"}]}},
        {"say": "The fix is simple. Next time your pay goes up, raise your savings first, then upgrade with what's left.",
         "visual": {"type": "equation", "title": "Next raise",
                    "lines": [{"text": "Save half first", "color": "green", "size": 104},
                              {"text": "+", "color": "dim", "size": 80},
                              {"text": "enjoy the rest", "color": "gold", "size": 104}]}},
        {"say": "Save this for later, and follow for more.",
         "visual": {"type": "cta", "lines": ["Grow your", "wealth, too."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "027_lifestyle_inflation.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
