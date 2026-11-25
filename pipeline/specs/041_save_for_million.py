"""Video 041 (global/USD): how much to save each month to reach $1 million by 50, 60 or 65, starting at 25.
Pillar: Money Math. Illustration only: every number is computed here from stated assumptions (no sourced data)."""
import json, os

# ---------------------------------------------------------------- assumptions (illustration, not a forecast)
GOAL = 1_000_000
START_AGE = 25
TARGET_AGES = (50, 60, 65)
ANNUAL = 0.07              # assumed average yearly return, compounded monthly (same convention as 018_start_early_us)
INFL = 0.03                # assumed yearly inflation, for the "what will a million buy" caveat
r = ANNUAL / 12

def monthly_needed(years):
    """Deposit at the end of each month so the balance reaches GOAL after `years` (future value of an annuity)."""
    n = years * 12
    return GOAL * r / ((1 + r) ** n - 1)

need = {a: monthly_needed(a - START_AGE) for a in TARGET_AGES}
put_in = {a: need[a] * (a - START_AGE) * 12 for a in TARGET_AGES}
growth65 = GOAL - put_in[65]
ratio_50_65 = need[50] / need[65]
real_value_65 = GOAL / (1 + INFL) ** (65 - START_AGE)       # a million at 65, in today's dollars

# balance path for the age-65 plan (for the line chart)
ages = list(range(START_AGE, 66))
def balance(months, pmt):
    return pmt * ((1 + r) ** months - 1) / r
bal65 = [balance((a - START_AGE) * 12, need[65]) for a in ages]
dep65 = [need[65] * (a - START_AGE) * 12 for a in ages]

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert 380 < need[65] < 382, need[65]                     # "about three hundred eighty dollars a month"
assert 555 < need[60] < 556, need[60]                     # "about five hundred fifty-five a month"
assert 1234 < need[50] < 1235, need[50]                   # "over twelve hundred thirty a month"
assert 3 < ratio_50_65 < 3.3, ratio_50_65                  # "more than triple"
assert 65 - 50 == 15                                       # "fifteen years earlier"
assert 182_500 < put_in[65] < 183_500, put_in[65]          # "just one hundred eighty-three thousand"
assert 816_500 < growth65 < 817_500, growth65              # "the other eight hundred seventeen thousand"
assert 306_000 < real_value_65 < 307_000, real_value_65    # "about three hundred seven thousand today"
assert 65 - START_AGE == 40                                # "in forty years"
assert abs(bal65[-1] - GOAL) < 1e-6
print({a: round(need[a], 2) for a in TARGET_AGES}, f"put in ${put_in[65]:,.0f}, growth ${growth65:,.0f}, "
      f"x{ratio_50_65:.2f}, real ${real_value_65:,.0f}")

spec = {
    "id": "041_save_for_million",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY MATH",
    "thumbnail": {"big": f"${need[65]:,.0f}/MO", "line": "From age 25, 7%/yr", "color": "gold",
                  "photo": {"file": "assets/photos/retired_couple_hand_in_hand.jpg", "focus": [0.5, 0.35]}},
    "disclaimer": "Assumes 7%/yr · returns vary, can be negative · not advice",
    "title": "How Much to Save a Month for $1 Million by 50, 60, 65",
    "description": (
        "How much do you need to save each month to become a millionaire? Starting at 25 with an assumed 7% "
        f"yearly return, reaching $1 million by 65 takes about ${need[65]:,.0f} a month, by 60 about "
        f"${need[60]:,.0f}, and by 50 about ${need[50]:,.0f}: over three times as much to get there 15 years sooner. "
        f"In the age-65 plan you put in about ${put_in[65]/1e3:,.0f}K and growth does the rest.\n\n"
        "Assumptions (our own illustration, not a forecast): deposits at the end of each month from age 25, a steady "
        "7% yearly return compounded monthly, no fees or taxes. With an assumed 3% yearly inflation, $1 million in "
        f"40 years buys about what ${real_value_65/1e3:,.0f}K buys today. Real returns vary year to year, can be "
        "negative, and past results don't guarantee future returns. Not financial advice.\n\n"
        "#millionaire #investing #personalfinance #compoundinterest #retirement"
    ),
    "tags": ["how much to save to become a millionaire", "save 1 million dollars", "how to become a millionaire",
             "compound interest", "retirement savings", "investing for beginners", "personal finance",
             "money math", "financial independence"],
    "localizations": {
        "es": {"title": "Cuánto ahorrar al mes para $1 millón a los 50, 60 o 65",
               "summary": f"Empezando a los 25 con un 7% anual supuesto: unos ${need[65]:,.0f} al mes para llegar a $1 millón "
                          f"a los 65, ${need[60]:,.0f} a los 60 y ${need[50]:,.0f} a los 50. El tiempo hace casi todo el trabajo."},
        "pt": {"title": "Quanto poupar por mês para US$1 milhão aos 50, 60 ou 65",
               "summary": f"Começando aos 25 com 7% ao ano (suposição): cerca de US${need[65]:,.0f} por mês para US$1 milhão "
                          f"aos 65, US${need[60]:,.0f} aos 60 e US${need[50]:,.0f} aos 50. O tempo faz quase todo o trabalho."},
        "hi": {"title": "50, 60 या 65 तक $1 मिलियन के लिए हर महीने कितना बचाएँ?",
               "summary": f"25 की उम्र से, 7% सालाना रिटर्न मानकर: 65 तक $1 मिलियन के लिए हर महीने लगभग ${need[65]:,.0f}, "
                          f"60 तक ${need[60]:,.0f} और 50 तक ${need[50]:,.0f}। ज़्यादातर काम समय करता है।"},
        "id": {"title": "Berapa Menabung per Bulan untuk $1 Juta di Usia 50, 60, 65",
               "summary": f"Mulai usia 25 dengan asumsi imbal hasil 7% per tahun: sekitar ${need[65]:,.0f} per bulan untuk "
                          f"$1 juta di usia 65, ${need[60]:,.0f} di usia 60, dan ${need[50]:,.0f} di usia 50."},
        "de": {"title": "Wie viel sparen für 1 Million $ mit 50, 60 oder 65?",
               "summary": f"Ab 25, bei angenommenen 7 % pro Jahr: rund {need[65]:,.0f} $ im Monat für 1 Million $ mit 65, "
                          f"{need[60]:,.0f} $ mit 60 und {need[50]:,.0f} $ mit 50. Die Zeit erledigt den Großteil."},
        "fr": {"title": "Combien épargner par mois pour 1 M$ à 50, 60 ou 65 ans",
               "summary": f"Dès 25 ans, avec 7 % par an supposés : environ {need[65]:,.0f} $ par mois pour 1 million $ à 65 ans, "
                          f"{need[60]:,.0f} $ à 60 ans et {need[50]:,.0f} $ à 50 ans. Le temps fait l'essentiel."},
    },
    "scenes": [
        # hook: the payoff number on frame 0 + open loop (what about earlier?)
        {"say": "A million dollars by sixty-five? About three hundred eighty dollars a month.",
         "visual": {"type": "photo", "file": "assets/photos/retired_couple_hand_in_hand.jpg", "title": "$1 million by 65",
                    "value": f"${need[65]:,.0f}/mo", "label": "start at 25 · 7% a year, assumed", "color": "gold",
                    "focus": [0.5, 0.4]}},
        {"say": "Starting at twenty-five, at an assumed seven percent a year.",
         "visual": {"type": "equation", "title": "The assumptions",
                    "lines": [{"text": "Start at 25", "color": "text", "size": 96},
                              {"text": "7% a year (assumed)", "color": "gold", "size": 84},
                              {"text": "Goal: $1,000,000", "color": "green", "size": 84}]}},
        {"say": "By sixty? About five hundred fifty-five a month.",
         "visual": {"type": "compare", "title": "Monthly savings needed", "format": "usd",
                    "left": {"label": "By 65", "value": round(need[65]), "color": "green"},
                    "right": {"label": "By 60", "value": round(need[60]), "color": "gold"}}},
        {"say": "By fifty? Over twelve hundred thirty a month.",
         "visual": {"type": "stat", "value": f"${need[50]:,.0f}", "label": "a month → $1 million by 50",
                    "sub": "start at 25 · 7% a year, assumed", "color": "red"}},
        {"say": "Fifteen years sooner costs more than triple, every month.",
         "visual": {"type": "bars", "title": "Saved per month, from age 25", "format": "usd",
                    "items": [{"label": "By 65", "value": round(need[65]), "color": "green"},
                              {"label": "By 60", "value": round(need[60]), "color": "gold"},
                              {"label": "By 50", "value": round(need[50]), "color": "red"}]}},
        # mid-video re-hook: second loop (where does the rest come from?)
        {"say": "The twist: at sixty-five you've put in just one hundred eighty-three thousand.",
         "visual": {"type": "line", "title": "The age-65 plan", "x": ages, "x_label": "age", "format": "usd",
                    "series": [{"label": "Account", "values": [round(v) for v in bal65], "color": "green"},
                               {"label": "You put in", "values": [round(v) for v in dep65], "color": "slate"}]}},
        {"say": "Growth adds the other eight hundred seventeen thousand.",
         "visual": {"type": "equation", "title": "Where the million comes from",
                    "lines": [{"text": f"You: ${put_in[65]/1e3:,.0f}K", "color": "text", "size": 96},
                              {"text": f"Growth: ${growth65/1e3:,.0f}K", "color": "green", "size": 96},
                              {"text": "= $1,000,000", "color": "gold", "size": 96}]}},
        {"say": "One catch: prices rise too, say three percent a year.",
         "visual": {"type": "photo", "file": "assets/photos/grocery_aisle_prices.jpg", "title": "The catch",
                    "value": "+3%/yr", "label": "prices rise too (example)", "color": "red", "focus": [0.5, 0.45]}},
        {"say": "So that million buys what three hundred seven thousand buys today.",
         "visual": {"type": "compare", "title": "A million in 40 years", "format": "usd",
                    "left": {"label": "On paper", "value": GOAL, "color": "gold"},
                    "right": {"label": "Today's money", "value": round(real_value_65, -3), "color": "red"}}},
        {"say": "Start early, and raise it with every pay rise.",
         "visual": {"type": "photo", "file": "assets/photos/construction_worker_welding.jpg", "title": "The lesson",
                    "value": "Start early", "label": "and raise it with every pay rise", "color": "gold",
                    "focus": [0.45, 0.4]}},
        # loop line: runs back into "A million dollars by sixty-five?..."
        {"say": "Early starters get the small magic number.",
         "visual": {"type": "cta", "lines": ["$1M by 65?", f"${need[65]:,.0f} a month."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "041_save_for_million.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
