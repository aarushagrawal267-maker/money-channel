"""Video 037 (global/USD, US credit system): what moves a FICO Score, plus a do/don't list.
Factor weights are sourced constants (myFICO); the utilization example is computed here."""
import json, os

# --- sourced: myFICO, "What's in my FICO Scores?" https://www.myfico.com/credit-education/whats-in-your-credit-score
#     (checked 2026-11-22). myFICO notes the importance of each category can vary from person to person.
FACTORS = {                       # share of a FICO Score, general weights
    "Payment history": 35,
    "Amounts owed": 30,
    "Length of history": 15,
    "New credit": 10,
    "Credit mix": 10,
}
# --- sourced (qualitative, checked 2026-11-22):
#   myFICO "Amounts owed": a low credit utilization ratio has a more positive impact on FICO Scores.
#     https://www.myfico.com/credit-education/credit-scores/amount-of-debt
#   myFICO "Credit checks and inquiries": soft inquiries, such as viewing your own credit report, will not affect
#     your FICO Scores; only apply for and open new credit accounts as needed.
#     https://www.myfico.com/credit-education/credit-reports/credit-checks-and-inquiries

# --- example (computed): using $300 of a $1,000 card limit
USED, LIMIT = 300, 1_000
util = USED / LIMIT

assert sum(FACTORS.values()) == 100
assert FACTORS["New credit"] == FACTORS["Credit mix"] == 10                    # "ten each"
assert FACTORS["Payment history"] == 35 and FACTORS["Payment history"] > 100 / 3   # "over a third"
assert FACTORS["Payment history"] + FACTORS["Amounts owed"] == 65                   # "almost two-thirds"
assert abs(65 - 200 / 3) < 2                                                         # 65% vs two-thirds (66.7%)
assert abs(util - 0.30) < 1e-9                                                      # "thirty percent"
print({k: f"{v}%" for k, v in FACTORS.items()}, f"util {util:.0%}")

spec = {
    "id": "037_credit_score",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY TRAP",
    "disclaimer": "FICO weights per myFICO · general guide · not financial advice",
    "title": "Credit Score Factors: What Actually Moves Your FICO",
    "description": (
        "What actually moves your credit score? FICO says a score is built from five parts: payment history 35%, "
        "amounts owed 30%, length of credit history 15%, new credit 10% and credit mix 10%. So the biggest wins are "
        "paying every bill on time and keeping balances low compared to your limits. Checking your own score does "
        "not hurt it.\n\n"
        "Sources:\n"
        "- myFICO, \"What's in my FICO Scores?\" (factor weights; importance can vary by person), "
        "https://www.myfico.com/credit-education/whats-in-your-credit-score (checked 22 Nov 2026)\n"
        "- myFICO, \"Amounts owed\" (low utilization helps), "
        "https://www.myfico.com/credit-education/credit-scores/amount-of-debt (checked 22 Nov 2026)\n"
        "- myFICO, \"Credit checks and inquiries\" (checking your own report doesn't affect your score), "
        "https://www.myfico.com/credit-education/credit-reports/credit-checks-and-inquiries (checked 22 Nov 2026)\n\n"
        "This covers US FICO Scores; other countries and scoring models differ. The $300-of-$1,000 figure is an "
        "example. General education, not financial advice.\n\n"
        "#creditscore #personalfinance #credit #moneytips #financialliteracy"
    ),
    "tags": ["credit score", "FICO score", "how to improve credit score", "credit utilization", "payment history",
             "credit cards", "personal finance", "money tips", "financial literacy"],
    "localizations": {
        "es": {"title": "Puntaje de crédito: qué mueve de verdad tu FICO",
               "summary": "Según FICO, tu puntaje se forma así: historial de pagos 35%, deudas 30%, antigüedad 15%, "
                          "crédito nuevo 10% y tipos de crédito 10%."},
        "pt": {"title": "Score de crédito: o que realmente mexe no seu FICO",
               "summary": "Segundo a FICO, o score é formado por: histórico de pagamentos 35%, valores devidos 30%, "
                          "tempo de histórico 15%, crédito novo 10% e mix de crédito 10%."},
        "hi": {"title": "क्रेडिट स्कोर: आपका FICO असल में किससे बदलता है",
               "summary": "FICO के अनुसार स्कोर पांच हिस्सों से बनता है: समय पर भुगतान 35%, बकाया रकम 30%, "
                          "क्रेडिट इतिहास 15%, नया क्रेडिट 10% और क्रेडिट मिक्स 10%।"},
        "id": {"title": "Skor Kredit: Apa yang Benar-Benar Menggerakkan FICO",
               "summary": "Menurut FICO, skor dibentuk dari: riwayat pembayaran 35%, jumlah utang 30%, lama riwayat "
                          "kredit 15%, kredit baru 10%, dan jenis kredit 10%."},
        "de": {"title": "Kredit-Score: Was deinen FICO-Score wirklich bewegt",
               "summary": "Laut FICO setzt sich der Score so zusammen: Zahlungshistorie 35%, offene Schulden 30%, "
                          "Dauer der Kredithistorie 15%, neue Kredite 10% und Kreditmix 10%."},
        "fr": {"title": "Score de crédit : ce qui fait vraiment bouger votre FICO",
               "summary": "Selon FICO, le score se compose ainsi : historique de paiement 35 %, montants dus 30 %, "
                          "ancienneté 15 %, nouveaux crédits 10 % et diversité des crédits 10 %."},
    },
    "scenes": [
        # hook: the key number on frame 0 + open loop ("guess which")
        {"say": "One habit makes up thirty-five percent of your credit score. Guess which.",
         "visual": {"type": "stat", "value": "35%", "label": "of a FICO Score",
                    "sub": "one habit · source: myFICO", "color": "gold"}},
        {"say": "FICO says your score has five parts. They're not equal.",
         "visual": {"type": "equation", "title": "What's in a FICO Score",
                    "lines": [{"text": f"{k}  {v}%", "color": c, "size": 68}
                              for (k, v), c in zip(list(FACTORS.items())[:3], ["gold", "green", "text"])]
                             + [{"text": f"New credit, mix  {FACTORS['New credit']}% each", "color": "muted", "size": 60}]}},
        {"say": "The answer: paying every bill on time. Autopay helps.",
         "visual": {"type": "pair", "title": "Payment history · 35%",
                    "left": {"label": "On time", "sub": "every bill", "color": "green"},
                    "right": {"label": "Late", "sub": "hurts most", "color": "red"}}},
        {"say": "Second, thirty percent: amounts owed, like how much of your limits you use.",
         "visual": {"type": "stat", "value": f"{FACTORS['Amounts owed']}%", "label": "amounts owed",
                    "sub": "incl. how much of your card limits you use", "color": "green"}},
        {"say": "Three hundred dollars on a one thousand dollar limit: thirty percent. Lower is better.",
         "visual": {"type": "compare", "title": "Example: 30% of the limit used",
                    "left": {"label": "Balance", "value": USED, "color": "gold"},
                    "right": {"label": "Limit", "value": LIMIT, "color": "slate"}}},
        # mid-video re-hook: opens a second loop (what feels risky but isn't?)
        {"say": "Now the twist: one thing that feels risky doesn't hurt.",
         "visual": {"type": "equation", "title": "The twist",
                    "lines": [{"text": "Feels risky.", "color": "text", "size": 110},
                              {"text": "Doesn't hurt.", "color": "green", "size": 110}]}},
        {"say": "Checking your own score doesn't lower it. Just don't open many cards at once.",
         "visual": {"type": "pair", "title": "Quick rules",
                    "left": {"label": "Check", "sub": "your own score", "color": "green"},
                    "right": {"label": "Apply", "sub": "few at a time", "color": "red"}}},
        {"say": "Focus on those two: together, almost two-thirds of your score.",
         "visual": {"type": "stat", "value": "65%", "label": "on-time payments + low balances",
                    "sub": "35% + 30%", "color": "green"}},
        # loop line: runs back into "One habit makes up thirty-five percent..."
        {"say": "Pay on time, keep balances low, and remember:",
         "visual": {"type": "cta", "lines": ["On time.", "Low balances."],
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

out = os.path.join(os.path.dirname(__file__), "037_credit_score.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
