"""Video 043 (global/USD): $500 a month of side income, spent vs invested for 10 years. Pillar: Earn More.
All growth figures are computed here from a stated assumption (7% a year, not guaranteed)."""
import json, os

# ---------------------------------------------------------------- sourced facts
# IRS Tax Topic No. 554, Self-employment tax (page last reviewed 09-Nov-2026, read 2026-11-25): "This rate consists of
# 12.4% for Social Security and 2.9% for Medicare taxes"; "You usually must pay self-employment tax if you had net
# earnings from self-employment of $400 or more." (Description only: why "after tax" matters for US side income.)
SE_SOCIAL_SECURITY, SE_MEDICARE = 12.4, 2.9
SE_THRESHOLD = 400

# ---------------------------------------------------------------- assumptions + computed example
MONTHLY, YEARS = 500, 10           # $500 left after tax, every month, for 10 years
ANNUAL = 0.07                      # ASSUMED average return per year (not guaranteed); no fees, no tax on growth
months = YEARS * 12

def grow(annual):
    """Deposit at the end of each month, monthly compounding equivalent to `annual` per year.
    Returns year-end balances (index 0..YEARS) and growth earned in each year."""
    g = (1 + annual) ** (1 / 12) - 1
    bal, bals, growth = 0.0, [0.0], []
    for _ in range(YEARS):
        earned = 0.0
        for _ in range(12):
            i = bal * g
            earned += i
            bal += i + MONTHLY
        bals.append(bal)
        growth.append(earned)
    return bals, growth

bals, growth = grow(ANNUAL)
fv = bals[-1]
put_in = MONTHLY * months
gain = fv - put_in
contrib = [MONTHLY * 12 * y for y in range(YEARS + 1)]
fv_low, fv_high = grow(0.04)[0][-1], grow(0.10)[0][-1]    # description: sensitivity

g = (1 + ANNUAL) ** (1 / 12) - 1
assert abs(fv - MONTHLY * ((1 + g) ** months - 1) / g) < 0.01     # loop matches the annuity formula
assert put_in == 60_000                                           # "sixty thousand dollars over ten years"
assert 85_000 < fv < 86_000, fv                                   # "about eighty-five thousand dollars"
assert 25_000 < gain < 26_000, gain                               # "about twenty-five thousand more"
assert growth[0] < 200, growth[0]                                 # "year one, under two hundred dollars"
assert growth[-1] > 5_000, growth[-1]                             # "year ten, over five thousand"
assert abs(SE_SOCIAL_SECURITY + SE_MEDICARE - 15.3) < 1e-9        # description: 15.3% self-employment tax
print(f"put in ${put_in:,}  worth ${fv:,.0f}  growth ${gain:,.0f}  y1 ${growth[0]:,.0f}  y10 ${growth[-1]:,.0f}  "
      f"4%: ${fv_low:,.0f}  10%: ${fv_high:,.0f}")

spec = {
    "id": "043_side_income",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "EARN MORE",
    "disclaimer": "Assumed 7%/yr, not guaranteed · not financial advice",
    "title": "$500/Month Side Income: What It's Worth in 10 Years",
    "description": (
        "What is $500 a month of side income worth in 10 years? Spend it and that's $60,000 of extras. Invest it "
        f"at an assumed 7% a year and it could grow to about ${fv:,.0f}: your own ${put_in:,} plus about "
        f"${gain:,.0f} of growth. Most of that growth comes late: about ${growth[0]:,.0f} in year one versus "
        f"${growth[-1]:,.0f} in year ten.\n\n"
        f"Assumptions (our own math): $500 left after tax, invested at the end of every month for {YEARS} years; "
        f"a steady 7% yearly return (at 4% it would be about ${fv_low:,.0f}, at 10% about ${fv_high:,.0f}); no fees, "
        "no tax on the growth, no inflation adjustment. Real returns vary, can be negative and are not guaranteed. "
        f"Taxes: in the US, side income is usually subject to income tax, and if you're self-employed with net "
        f"earnings of ${SE_THRESHOLD} or more, self-employment tax of {SE_SOCIAL_SECURITY + SE_MEDICARE:.1f}% "
        f"({SE_SOCIAL_SECURITY}% Social Security + {SE_MEDICARE}% Medicare; IRS Tax Topic 554). Set tax money aside "
        "before you invest; rules differ in other countries. Educational only, not financial advice.\n\n"
        "#sideincome #sidehustle #investing #personalfinance #compoundinterest"
    ),
    "tags": ["side income", "side hustle", "500 a month invested", "invest 500 a month", "compound interest",
             "spend or invest", "earn more money", "personal finance", "self employment tax"],
    "localizations": {
        "es": {"title": "Ingreso extra de $500/mes: cuánto vale en 10 años",
               "summary": f"Gastarlo: $60.000 en 10 años. Invertirlo a un 7% anual supuesto: unos ${fv:,.0f}".replace(",", ".")
                          + ". El crecimiento llega tarde, y los impuestos van primero."},
        "pt": {"title": "Renda extra de US$500/mês: quanto vale em 10 anos",
               "summary": f"Gastar: US$60.000 em 10 anos. Investir a 7% ao ano (suposição): cerca de US${fv:,.0f}".replace(",", ".")
                          + ". O crescimento vem no fim, e os impostos vêm antes."},
        "hi": {"title": "$500 महीने की साइड इनकम: 10 साल में कितनी?",
               "summary": f"खर्च करें तो 10 साल में $60,000। 7% सालाना (अनुमान) पर निवेश करें तो लगभग ${fv:,.0f}। "
                          "बढ़त बाद के सालों में आती है, और टैक्स पहले अलग रखें।"},
        "id": {"title": "Penghasilan Sampingan $500/Bulan: Nilainya dalam 10 Tahun",
               "summary": f"Dihabiskan: $60.000 dalam 10 tahun. Diinvestasikan dengan asumsi 7% per tahun: sekitar ${fv:,.0f}".replace(",", ".")
                          + ". Pertumbuhan datang belakangan, pajak disisihkan dulu."},
        "de": {"title": "$500 Nebeneinkommen im Monat: Wert nach 10 Jahren",
               "summary": f"Ausgegeben: 60.000 Dollar in 10 Jahren. Angelegt bei angenommenen 7 % pro Jahr: rund {fv:,.0f} Dollar".replace(",", ".")
                          + ". Das Wachstum kommt spät, die Steuer zuerst."},
        "fr": {"title": "500 $/mois de revenu d'appoint : combien en 10 ans ?",
               "summary": f"Dépensés : 60 000 $ en 10 ans. Investis à 7 % par an (hypothèse) : environ {fv:,.0f} $".replace(",", " ")
                          + ". La croissance arrive tard, et l'impôt passe d'abord."},
    },
    "scenes": [
        # hook: the biggest number on frame 0 + contradiction/open loop ("or zero?")
        {"say": "Five hundred a month on the side: spent, or eighty-five thousand dollars?",
         "visual": {"type": "stat", "value": f"${fv / 1e3:.1f}K", "label": "$500 a month, invested 10 years",
                    "sub": "assumed 7% a year · not guaranteed", "color": "green"}},
        {"say": "Say a side gig nets five hundred a month, after tax.",
         "visual": {"type": "pair", "title": "The setup",
                    "left": {"label": "Side gig", "sub": "$500 a month", "color": "green"},
                    "right": {"label": "Tax", "sub": "set aside first", "color": "slate"}}},
        {"say": "Spend it all: sixty thousand dollars over ten years.",
         "visual": {"type": "equation", "title": "Option 1: spend it",
                    "lines": [{"text": f"${MONTHLY} × {months} months", "color": "text", "size": 88},
                              {"text": f"= ${put_in:,} spent", "color": "gold", "size": 110}]}},
        {"say": "Invest it instead, at an assumed seven percent a year...",
         "visual": {"type": "line", "title": "Option 2: invest it (assumed 7%/yr)", "format": "usd",
                    "x": list(range(YEARS + 1)), "x_label": "years",
                    "series": [{"label": "Put in", "values": contrib, "color": "slate"},
                               {"label": "Invested", "values": bals, "color": "green"}]}},
        {"say": "...and it could grow to about eighty-five thousand dollars.",
         "visual": {"type": "compare", "title": "After 10 years",
                    "left": {"label": "You put in", "value": put_in, "color": "slate"},
                    "right": {"label": "Worth", "value": fv, "color": "green"}}},
        # mid-video re-hook: opens a second loop (why does it feel like nothing at first?)
        {"say": "Here's the catch: early years feel like nothing.",
         "visual": {"type": "equation", "title": "The catch",
                    "lines": [{"text": "Early years", "color": "text", "size": 110},
                              {"text": "feel like nothing.", "color": "gold", "size": 100}]}},
        {"say": "Year one, growth adds under two hundred dollars. Year ten, over five thousand.",
         "visual": {"type": "bars", "title": "Growth earned in that year",
                    "items": [{"label": "Year 1", "value": growth[0], "color": "slate"},
                              {"label": "Year 10", "value": growth[-1], "color": "green"}]}},
        {"say": "Sixty thousand is your own money. Time adds about twenty-five thousand more.",
         "visual": {"type": "stat", "value": f"+${gain / 1e3:.1f}K", "label": "added by growth over 10 years",
                    "sub": f"on ${put_in:,} put in · assumed 7%", "color": "green"}},
        {"say": "No shortcut. Just a steady habit and patience.",
         "visual": {"type": "pair", "title": "The real formula",
                    "left": {"label": "Habit", "sub": "every month", "color": "green"},
                    "right": {"label": "Time", "sub": "10+ years", "color": "gold"}}},
        # loop line: runs back into "Five hundred a month on the side: spent, or eighty-five thousand dollars?"
        {"say": "So what will your five hundred become?",
         "visual": {"type": "cta", "lines": ["$500 a month.", "Spend or grow?"],
                    "sub": "Follow for daily money lessons"}},
    ],
}
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "043_side_income.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
