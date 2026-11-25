"""Video 051 (global/USD): term vs whole life insurance for a $1M payout. Pillar: Smart Financing & Money Traps.
Premiums are published sample rates (Policygenius); totals and ratios are computed here. Neutral explainer, not advice."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Policygenius, "How much does a $1 million life insurance policy cost?" (page updated Oct 15, 2024; read
# 2026-11-25): https://www.policygenius.com/life-insurance/million-dollar-life-insurance-policy/
# "Rate illustration valid as of 10/01/2024." $1,000,000 coverage, monthly premiums, age 30:
#  - 20-year term: female $36.90, male $48.89 (average of a composite of policies from 11 carriers, non-smokers,
#    Preferred health classification).
#  - Whole life: female $801, male $920 (sample rates, non-smokers, Preferred Plus health classification, whole life
#    policy paid up at age 100 offered through MassMutual).
# The two tables use different health classes and products, so the comparison is illustrative, not a quote.
TERM_M30, WHOLE_M30 = 48.89, 920
TERM_F30, WHOLE_F30 = 36.90, 801
RATE_DATE = "Oct 2024"
YEARS = 20

# ---------------------------------------------------------------- checks behind spoken / shown claims
ratio = WHOLE_M30 / TERM_M30
assert 18.5 < ratio < 19, ratio                         # "nearly nineteen times more"
assert round(TERM_M30) == 49                            # "forty-nine a month"
assert WHOLE_M30 == 920                                 # "nine hundred twenty"
term_20y = TERM_M30 * 12 * YEARS
whole_20y = WHOLE_M30 * 12 * YEARS
assert 11_500 < term_20y < 12_000, term_20y             # "about twelve thousand dollars"
assert round(whole_20y / 1e3) == 221, whole_20y         # "two hundred twenty-one thousand"
assert 20 < WHOLE_F30 / TERM_F30 < 23                   # women: ~21.7x (description only)
print(f"ratio {ratio:.1f}x; 20 years: term ${term_20y:,.0f} vs whole ${whole_20y:,.0f}")

spec = {
    "id": "051_insurance_types",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "SMART FINANCING",
    "disclaimer": f"Sample rates: Policygenius, {RATE_DATE} · not advice",
    "title": "Term vs Whole Life Insurance: The $1M Question",
    "description": (
        "Term vs whole life insurance: for the same $1 million payout, Policygenius sample rates for a healthy "
        f"30-year-old man were ${TERM_M30:.2f} a month for 20-year term life and ${WHOLE_M30} a month for whole life, "
        f"nearly {ratio:.0f} times more. Term covers a set number of years and then ends; whole life lasts for life "
        "and builds cash value. Which fits depends on how long someone relies on your income.\n\n"
        f"Source: Policygenius, \"How much does a $1 million life insurance policy cost?\" (rate illustration valid as "
        "of Oct 1, 2024). Term rates: average of 11 carriers, non-smokers, Preferred health class. Whole life rates: "
        "sample policy paid up at age 100 through MassMutual, non-smokers, Preferred Plus health class. For a "
        f"30-year-old woman the same tables show ${TERM_F30:.2f} vs ${WHOLE_F30}. Our 20-year totals multiply those "
        "monthly premiums by 240 months; they ignore the cash value a whole life policy builds and any dividends. "
        "Real premiums depend on your age, health, insurer, state and the date. This is a general explainer, not "
        "insurance or financial advice; compare quotes and policy documents before you buy.\n\n"
        "#lifeinsurance #personalfinance #insurance #moneytips #financialliteracy"
    ),
    "tags": ["term vs whole life insurance", "term life insurance", "whole life insurance",
             "1 million life insurance cost", "life insurance explained", "cash value life insurance",
             "personal finance", "money tips"],
    "localizations": {
        "es": {"title": "Seguro de vida a plazo vs vida entera: $1M",
               "summary": "Mismo pago de $1 millón: unos $49 al mes con seguro a plazo de 20 años, o $920 con vida entera "
                          "(tarifas de ejemplo de Policygenius, hombre de 30 años). Qué cubre cada uno."},
        "pt": {"title": "Seguro de vida temporário vs vitalício: US$1M",
               "summary": "Mesma indenização de US$1 milhão: cerca de US$49 por mês no temporário de 20 anos ou US$920 no "
                          "vitalício (taxas de exemplo da Policygenius, homem de 30 anos). O que cada um cobre."},
        "hi": {"title": "टर्म बनाम होल लाइफ़ इंश्योरेंस: $1M का सवाल",
               "summary": "एक ही $10 लाख डॉलर के कवर के लिए 30 साल के पुरुष का 20 साल का टर्म प्लान करीब $49 महीना, "
                          "होल लाइफ़ $920 महीना (Policygenius के नमूना रेट)। दोनों में क्या फ़र्क है।"},
        "id": {"title": "Asuransi Jiwa Berjangka vs Seumur Hidup: $1 Juta",
               "summary": "Untuk uang pertanggungan $1 juta yang sama: sekitar $49 per bulan untuk berjangka 20 tahun, atau "
                          "$920 untuk seumur hidup (contoh tarif Policygenius, pria 30 tahun). Apa bedanya."},
        "de": {"title": "Risikoleben vs. Kapitalleben: Die $1-Mio.-Frage",
               "summary": "Gleiche Auszahlung von 1 Mio. Dollar: rund 49 Dollar im Monat für 20 Jahre Risikoschutz oder 920 "
                          "Dollar für eine lebenslange Police (Beispieltarife von Policygenius, Mann, 30)."},
        "fr": {"title": "Assurance vie temporaire ou entière : la question à 1 M$",
               "summary": "Même capital de 1 million de dollars : environ 49 $ par mois en temporaire 20 ans, ou 920 $ en vie "
                          "entière (tarifs d'exemple Policygenius, homme de 30 ans). Ce que couvre chacune."},
    },
    "scenes": [
        # hook: the two prices on frame 0 + open loop ("Why?")
        {"say": "Same million dollar payout: forty-nine a month, or nine hundred twenty. Why?",
         "visual": {"type": "compare", "title": "$1M cover · man, 30 · per month",
                    "left": {"label": "Term, 20 yrs", "value": TERM_M30, "color": "green"},
                    "right": {"label": "Whole life", "value": WHOLE_M30, "color": "gold"}}},
        {"say": "Policy Genius sample rates, healthy thirty-year-old man: nearly nineteen times more.",
         "visual": {"type": "stat", "value": f"~{ratio:.0f}×", "label": "whole life vs 20-year term premium",
                    "sub": f"Policygenius sample rates · {RATE_DATE}", "color": "gold"}},
        {"say": "Term covers set years, then ends. Whole life lasts for life, building cash value.",
         "visual": {"type": "equation", "title": "What you're buying",
                    "lines": [{"text": "Term:", "color": "green", "size": 76},
                              {"text": "set years, then ends", "color": "text", "size": 76},
                              {"text": "Whole life:", "color": "gold", "size": 76},
                              {"text": "for life + cash value", "color": "text", "size": 76}]}},
        {"say": "Twenty years of premiums: about twelve thousand dollars, versus two hundred twenty-one thousand.",
         "visual": {"type": "bars", "title": f"Premiums paid over {YEARS} years",
                    "items": [{"label": "Term", "value": term_20y, "color": "green"},
                              {"label": "Whole life", "value": whole_20y, "color": "gold"}]}},
        {"say": "Part of that builds cash value. Term pays nothing if you outlive it.",
         "visual": {"type": "pair", "title": "The trade-off",
                    "left": {"label": "Whole life", "sub": "part → cash value", "color": "gold"},
                    "right": {"label": "Term", "sub": "$0 if you outlive it", "color": "green"}}},
        # mid-video re-hook: opens a second loop (which one question?)
        {"say": "So which is better? It depends on one question.",
         "visual": {"type": "equation", "title": "Which is better?",
                    "lines": [{"text": "It depends on", "color": "text", "size": 100},
                              {"text": "one question.", "color": "gold", "size": 110}]}},
        {"say": "How long will someone depend on your income?",
         "visual": {"type": "stat", "value": "?", "label": "How long do others rely on your income?",
                    "sub": "kids, a partner, a mortgage...", "color": "gold"}},
        {"say": "A fixed number of years? Term fits. A lifelong need? Whole life fits.",
         "visual": {"type": "pair", "title": "Match the need",
                    "left": {"label": "Term", "sub": "a fixed number of years", "color": "green"},
                    "right": {"label": "Whole life", "sub": "a lifelong need", "color": "gold"}}},
        # loop line: runs back into "Same million dollar payout: forty-nine a month, or nine hundred twenty."
        {"say": "Need first. Otherwise you're just comparing...",
         "visual": {"type": "cta", "lines": ["Need first.", "Policy second."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "051_insurance_types.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
