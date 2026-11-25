"""Video 036 (global/US): how "free" apps like Instagram make money. Pillar: Business Breakdowns."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Meta Platforms, "Meta Reports Third Quarter 2026 Results" (Oct 21, 2026; quarter ended Sept 30, 2026):
# total revenue $64.60 billion; segment table: advertising revenue $63,061M, Family of Apps revenue $64,158M;
# "DAP was 3.64 billion on average for September 2026"; "Ad impressions delivered across our Family of Apps
# increased by 10% year-over-year"; "average price per ad increased by 14% year-over-year".
TOTAL_REV = 64.60e9
AD_REV = 63.061e9
FOA_REV = 64.158e9
DAP_SEP26 = 3.64e9
IMPRESSIONS_GROWTH, PRICE_PER_AD_GROWTH = 10, 14
# Meta, "Meta Reports Second Quarter 2026 Results" (Jul 29, 2026): "DAP was 3.60 billion on average for June 2026".
DAP_JUN26 = 3.60e9
# Meta defines ARPP (average revenue per person) as Family of Apps revenue divided by the average of DAP at the
# beginning and end of the quarter; computed below from the figures above.
DAYS_Q3 = 31 + 31 + 30          # July, August, September

# ---------------------------------------------------------------- checks behind spoken / shown claims
arpp = FOA_REV / ((DAP_JUN26 + DAP_SEP26) / 2)
assert abs(arpp - 17.72) < 0.005, arpp                       # "about seventeen dollars seventy"
ad_share = AD_REV / TOTAL_REV
assert round(ad_share * 100) == 98, ad_share                 # "about ninety-eight percent"
per_day = AD_REV / DAYS_Q3
assert 680e6 < per_day < 690e6, per_day                      # "about six hundred eighty-five million a day"
assert round(AD_REV / 1e9) == 63                             # "sixty-three billion dollars"
assert round(DAP_SEP26 / 1e9, 1) == 3.6                      # shown on screen ("3.64B")
assert DAYS_Q3 == 92 and DAP_SEP26 > 1e9                     # "July to September" / "billions of people"
print(f"ARPP ${arpp:.2f}; ads {ad_share:.1%} of revenue; ${per_day/1e6:.0f}M/day")

spec = {
    "id": "036_free_apps",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Source: Meta Q3 2026 results (Oct 21, 2026)",
    "title": "How Free Apps Make Money: $63B in 3 Months From Ads",
    "description": (
        "How do free apps like Instagram, Facebook and WhatsApp make money? Ads. In July to September 2026, Meta "
        f"earned ${AD_REV/1e9:.1f} billion from advertising, about {ad_share:.0%} of its revenue, or roughly "
        f"${per_day/1e6:.0f} million a day. With 3.64 billion daily users, its apps brought in about ${arpp:.2f} per "
        "person in that one quarter. Meta showed 10% more ads than a year earlier and charged 14% more for each.\n\n"
        "Sources: Meta Platforms Q3 2026 results (Oct 21, 2026) and Q2 2026 results (Jul 29, 2026). Revenue per person "
        "is Family of Apps revenue divided by average daily active people at the start and end of the quarter "
        "(Meta's definition), computed from those releases.\n\n"
        "#instagram #meta #business #socialmedia #advertising"
    ),
    "tags": ["how instagram makes money", "how free apps make money", "meta revenue", "facebook ads",
             "average revenue per user", "social media business model", "business breakdown"],
    "localizations": {
        "es": {"title": "Cómo ganan dinero las apps gratis: $63B en 3 meses",
               "summary": "Meta ganó $63.100 millones con publicidad entre julio y septiembre de 2026, unos $685 millones al día. "
                          "En Instagram y Facebook, quien paga es el anunciante: tú pagas con tu atención."},
        "pt": {"title": "Como apps grátis ganham dinheiro: US$63 bi em 3 meses",
               "summary": "A Meta faturou US$63,1 bilhões com anúncios de julho a setembro de 2026, cerca de US$685 milhões por dia. "
                          "No Instagram, quem paga é o anunciante: você paga com sua atenção."},
        "hi": {"title": "फ्री ऐप्स पैसे कैसे कमाते हैं: 3 महीने में $63B",
               "summary": "जुलाई से सितंबर 2026 में Meta ने विज्ञापनों से $63.1 अरब कमाए, यानी रोज़ लगभग $685 मिलियन। "
                          "Instagram पर पैसा विज्ञापनदाता देते हैं, आप अपने समय और ध्यान से चुकाते हैं।"},
        "id": {"title": "Cara Aplikasi Gratis Cari Uang: $63 Miliar dalam 3 Bulan",
               "summary": "Meta meraup $63,1 miliar dari iklan pada Juli-September 2026, sekitar $685 juta per hari. "
                          "Di Instagram, yang membayar adalah pengiklan; kamu membayar dengan perhatianmu."},
        "de": {"title": "Wie Gratis-Apps Geld verdienen: $63 Mrd. in 3 Monaten",
               "summary": "Meta nahm von Juli bis September 2026 63,1 Mrd. Dollar mit Werbung ein, rund 685 Mio. Dollar pro Tag. "
                          "Bei Instagram zahlen die Werbekunden, du zahlst mit deiner Aufmerksamkeit."},
        "fr": {"title": "Comment les applis gratuites gagnent 63 Md$ en 3 mois",
               "summary": "Meta a tiré 63,1 milliards de dollars de la publicité de juillet à septembre 2026, environ 685 millions "
                          "par jour. Sur Instagram, l'annonceur paie ; vous payez avec votre attention."},
    },
    "thumbnail": {"big": f"${arpp:.2f}", "line": "Meta's price on you", "color": "gold",
                  "photo": {"file": "assets/photos/social_apps_phone_screen.jpg", "focus": [0.47, 0.45]}},
    "scenes": [
        # hook: the biggest number on frame 0 + contradiction ("from free apps")
        {"say": "Six hundred and eighty-five million dollars a day, from free apps.",
         "visual": {"type": "stat", "value": f"${per_day/1e6:.0f}M", "label": "Meta ad revenue, per day",
                    "sub": "July to Sept 2026 average · Meta Q3 results", "color": "gold"}},
        {"say": "That's Meta's ad money, July to September: sixty-three billion dollars in three months.",
         "visual": {"type": "photo", "file": "assets/photos/facebook_hq_sign_menlo_park.jpg", "title": "Meta ad revenue, Q3 2026",
                    "value": f"${AD_REV/1e9:.0f}B", "color": "gold", "label": "in 3 months · Meta HQ, Menlo Park",
                    "focus": [0.5, 0.45]}},
        {"say": "Here's how. You're not the customer. Advertisers are, and they pay for your attention.",
         "visual": {"type": "pair", "title": "Who pays?",
                    "left": {"label": "You", "sub": "use it free", "color": "green"},
                    "right": {"label": "Advertisers", "sub": "pay for your time", "color": "gold"}}},
        {"say": "Versus a year earlier: ten percent more ads, and fourteen percent more per ad.",
         "visual": {"type": "bars", "title": "Growth vs a year ago (%)", "format": "num",
                    "items": [{"label": "Ads shown", "value": IMPRESSIONS_GROWTH, "color": "green"},
                              {"label": "Price per ad", "value": PRICE_PER_AD_GROWTH, "color": "gold"}]}},
        # mid-video re-hook: opens a second loop (what are you worth?)
        {"say": "Now the twist: Meta's own numbers put a price on you.",
         "visual": {"type": "photo", "file": "assets/photos/social_apps_phone_screen.jpg", "title": "The twist",
                    "label": "What are you worth to Meta?", "focus": [0.55, 0.45]}},
        {"say": "About seventeen dollars seventy per daily user, in just three months.",
         "visual": {"type": "stat", "value": f"${arpp:.2f}", "label": "revenue per daily user, one quarter",
                    "sub": "Q3 2026 · 3.64B people use Meta's apps daily", "color": "green"}},
        {"say": "When an app is free, you don't pay with money. You pay with time.",
         "visual": {"type": "equation",
                    "lines": [{"text": "Free app?", "color": "text", "size": 110},
                              {"text": "You pay", "color": "gold", "size": 110},
                              {"text": "with your time.", "color": "gold", "size": 100}]}},
        # loop line: runs back into "Six hundred and eighty-five million dollars a day..."
        {"say": "Multiply that by billions of people, and you get...",
         "visual": {"type": "cta", "lines": [f"${per_day/1e6:.0f}M a day.", "Paid by ads."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "036_free_apps.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
