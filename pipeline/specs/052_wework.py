"""Video 052 (global/US): WeWork, from a $47B valuation to Chapter 11. Pillar: Case Studies."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Reuters (Jan 8, 2019): WeWork received $2 billion of new funding from SoftBank, valuing it at $47 billion.
# CNBC (Nov 6, 2023): "Valued in 2019 at $47 billion in a round led by Masayoshi Son's SoftBank".
VALUATION_2019 = 47e9
VALUATION_YEAR = 2019
# WeWork Companies / The We Company Form S-1 (SEC EDGAR, filed Aug 14, 2019), selected financial data
# ($ thousands): 2018 revenue 1,821,751; 2018 net loss (1,927,419). Risk factors: "The average length of the
# initial term of our U.S. leases is approximately 15 years, and our future undiscounted minimum lease cost
# payment obligations under signed operating and finance leases was $47.2 billion as of June 30, 2019";
# leases "are for terms that are significantly longer than the terms of our membership agreements".
REV_2018 = 1_821.751e6
NET_LOSS_2018 = 1_927.419e6
LEASE_OBLIGATIONS = 47.2e9
US_LEASE_YEARS = 15
# AP (Sept 30, 2019, via Fox 35 / The Daily Record): new leaders formally suspended the planned stock market debut;
# the company failed to generate enthusiasm "after its IPO filings revealed massive losses". IPO filing withdrawn
# Sept 30, 2019 (CBS News, TechCrunch). NPR (Sept 24, 2019): co-founder Adam Neumann stepped down as CEO.
IPO_PULLED_YEAR, IPO_PULLED_MONTH = 2019, 9
# Reuters (Nov 7, 2023, Roumeliotis/Knauth/Dey): Chapter 11 filed Monday (Nov 6, 2023) in New Jersey; "listed
# assets of $15.06 billion and liabilities of $18.66 billion as of June 30"; "Paying for space consumed 74% of
# WeWork's revenue in the second quarter of 2023, the last time it reported financial results."
CH11_YEAR = 2023
ASSETS_2023, LIABILITIES_2023 = 15.06e9, 18.66e9
SPACE_COST_SHARE_Q2_2023 = 74
# AP (June 12, 2024, via NY1): WeWork emerged from bankruptcy (description only).

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert round(VALUATION_2019 / 1e9) == 47                      # "forty-seven billion dollars"
assert CH11_YEAR - VALUATION_YEAR == 4                        # "bankrupt by twenty twenty-three"
assert round(REV_2018 / 1e9, 1) == 1.8                        # "one point eight billion revenue"
assert round(NET_LOSS_2018 / 1e9, 1) == 1.9                   # "one point nine billion lost"
loss_per_dollar = NET_LOSS_2018 / REV_2018
assert round(loss_per_dollar, 2) == 1.06, loss_per_dollar     # "a dollar six lost per dollar of revenue"
assert round(LEASE_OBLIGATIONS / 1e9) == 47                   # "also about forty-seven billion"
assert SPACE_COST_SHARE_Q2_2023 == 74                         # "seventy-four percent"
assert LIABILITIES_2023 > ASSETS_2023                         # shown: liabilities exceeded assets
gap = LIABILITIES_2023 - ASSETS_2023
assert round(gap / 1e9, 1) == 3.6                              # description: "$3.6 billion more"
print(f"2018: rev ${REV_2018/1e9:.2f}B, loss ${NET_LOSS_2018/1e9:.2f}B ({loss_per_dollar:.3f} per $1); "
      f"leases ${LEASE_OBLIGATIONS/1e9:.1f}B; 2023 gap ${gap/1e9:.1f}B")

spec = {
    "id": "052_wework",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "CASE STUDY",
    "disclaimer": "Sources: WeWork S-1, Reuters, AP, CNBC · see description",
    "title": "WeWork: From a $47B Valuation to Bankruptcy",
    "description": (
        "WeWork was valued at $47 billion in a SoftBank funding round in January 2019 and filed for Chapter 11 "
        "bankruptcy in November 2023. Its 2019 IPO filing showed why: in 2018 it lost $1.93 billion on $1.82 "
        "billion of revenue (about $1.06 lost per dollar of revenue), and it had signed $47.2 billion of future "
        "lease payments, with U.S. leases averaging about 15 years while members signed much shorter deals. "
        "After the filings revealed massive losses (AP), the IPO was pulled in September 2019; co-founder Adam "
        "Neumann had stepped down as CEO days earlier. By Q2 2023, paying for space took 74% of revenue, and the "
        "bankruptcy filing listed $18.66 billion of liabilities against $15.06 billion of assets as of June 30, 2023 (Reuters). The 2018 net loss includes minority owners' share; the loss attributable to WeWork was about $1.6 billion. "
        "WeWork emerged from bankruptcy in June 2024 under new owners. The lesson: a valuation is an opinion; "
        "profit and cash flow pay the bills.\n\n"
        "Sources: Reuters (Jan 8, 2019; Nov 7, 2023); WeWork Form S-1 (SEC, Aug 14, 2019); AP (Sept 30, 2019; "
        "June 12, 2024); NPR (Sept 24, 2019); CNBC (Nov 6, 2023). The 2019 valuation was a private funding-round "
        "price, not a stock market value. Educational content, not investment advice.\n\n"
        "#wework #business #casestudy #startups #valuation"
    ),
    "tags": ["wework", "wework bankruptcy", "wework ipo", "what happened to wework", "wework valuation",
             "softbank wework", "business case study", "startup valuation", "business lessons"],
    "localizations": {
        "es": {"title": "WeWork: de 47.000 millones de dólares a la quiebra",
               "summary": "En 2019 WeWork fue valorada en 47.000 millones de dólares; en 2023 se acogió al Capítulo 11. Perdía más de lo que ingresaba y firmó 47.200 millones en alquileres futuros. La lección: una valoración no es un beneficio."},
        "pt": {"title": "WeWork: de 47 bilhões de dólares à falência",
               "summary": "Em 2019 a WeWork foi avaliada em 47 bilhões de dólares; em 2023 pediu recuperação judicial (Chapter 11). Perdia mais do que faturava e assinou 47,2 bilhões em aluguéis futuros. A lição: valuation não é lucro."},
        "hi": {"title": "WeWork: 47 अरब डॉलर के मूल्यांकन से दिवालियापन तक",
               "summary": "2019 में WeWork का मूल्य 47 अरब डॉलर आँका गया और 2023 में उसने Chapter 11 दिवालियापन के लिए आवेदन किया। कंपनी कमाई से ज़्यादा घाटे में थी और 47.2 अरब डॉलर का भविष्य का किराया साइन कर चुकी थी। सीख: वैल्यूएशन मुनाफ़ा नहीं है।"},
        "id": {"title": "WeWork: Dari Valuasi $47 Miliar ke Kebangkrutan",
               "summary": "Pada 2019 WeWork divaluasi 47 miliar dolar; pada 2023 mengajukan Chapter 11. Kerugiannya lebih besar dari pendapatannya, dan ia menandatangani sewa masa depan 47,2 miliar dolar. Pelajarannya: valuasi bukan laba."},
        "de": {"title": "WeWork: Von 47 Mrd. $ Bewertung zur Insolvenz",
               "summary": "2019 wurde WeWork mit 47 Milliarden Dollar bewertet, 2023 folgte die Insolvenz nach Chapter 11. Die Verluste waren höher als der Umsatz, dazu 47,2 Milliarden Dollar künftige Mieten. Die Lehre: Eine Bewertung ist kein Gewinn."},
        "fr": {"title": "WeWork : de 47 milliards de dollars à la faillite",
               "summary": "En 2019, WeWork était valorisée 47 milliards de dollars ; en 2023, elle s'est placée sous le Chapter 11. Elle perdait plus qu'elle ne gagnait et avait signé 47,2 milliards de loyers futurs. La leçon : une valorisation n'est pas un profit."},
    },
    "thumbnail": {"big": f"${VALUATION_2019 / 1e9:.0f}B", "color": "gold",
                  "photo": {"file": "assets/photos/wework_miami_sign.jpg", "focus": [0.5, 0.3]}},
    "scenes": [
        # hook: the big number on frame 0 + open loop ("why?")
        {"say": "Forty-seven billion dollars in twenty nineteen. Bankrupt by twenty twenty-three. Why?",
         "visual": {"type": "photo", "file": "assets/photos/wework_miami_sign.jpg", "focus": [0.5, 0.35],
                    "value": f"${VALUATION_2019 / 1e9:.0f}B", "label": f"WeWork's valuation, Jan {VALUATION_YEAR}", "color": "gold"}},
        {"say": "It signed long office leases, then rented desks on shorter deals.",
         "visual": {"type": "pair", "title": "The business model",
                    "left": {"label": "Leases", "sub": f"~{US_LEASE_YEARS} years (US)", "color": "red"},
                    "right": {"label": "Members", "sub": "much shorter deals", "color": "green"}}},
        {"say": "Twenty eighteen: revenue one point eight billion. Losses, one point nine billion.",
         "visual": {"type": "compare", "title": "2018 (from its IPO filing)",
                    "left": {"label": "Revenue", "value": REV_2018, "color": "green"},
                    "right": {"label": "Net loss", "value": NET_LOSS_2018, "color": "red"}}},
        {"say": "That's a dollar six lost per dollar of revenue.",
         "visual": {"type": "equation", "title": "Every dollar in",
                    "lines": [{"text": "$1.00 of revenue", "color": "text", "size": 96},
                              {"text": f"${loss_per_dollar:.2f} lost", "color": "red", "size": 130}]}},
        # mid-video re-hook: opens a second loop (the same number, on the other side)
        {"say": "Now the twist: its future rent bill was also about forty-seven billion.",
         "visual": {"type": "photo", "file": "assets/photos/wework_empty_floor_sf.jpg", "focus": [0.5, 0.45],
                    "value": f"${LEASE_OBLIGATIONS / 1e9:.1f}B", "label": "future lease payments (June 2019)", "color": "red"}},
        {"say": "After the filing showed huge losses, the I-P-O was pulled.",
         "visual": {"type": "pair", "title": f"Sept {IPO_PULLED_YEAR}",
                    "left": {"label": "IPO", "sub": "planned", "color": "slate"},
                    "right": {"label": "Pulled", "sub": "lukewarm demand (AP)", "color": "red"}}},
        {"say": "By twenty twenty-three, space costs ate seventy-four percent of revenue.",
         "visual": {"type": "bars", "title": "Share of revenue, Q2 2023 (%)", "format": "num",
                    "items": [{"label": "Space", "value": SPACE_COST_SHARE_Q2_2023, "color": "red"},
                              {"label": "Everything else", "value": 100 - SPACE_COST_SHARE_Q2_2023, "color": "slate"}]}},
        {"say": "That November, WeWork filed for Chapter eleven bankruptcy.",
         "visual": {"type": "compare", "title": f"Chapter 11 filing, Nov {CH11_YEAR}",
                    "left": {"label": "Assets", "value": ASSETS_2023, "color": "slate"},
                    "right": {"label": "Liabilities", "value": LIABILITIES_2023, "color": "red"}}},
        {"say": "The lesson: a valuation is an opinion. Profit and cash are facts.",
         "visual": {"type": "photo", "file": "assets/photos/wework_coworking_vancouver.jpg", "focus": [0.5, 0.5],
                    "title": "Valuation = opinion", "label": "Profit + cash = facts"}},
        # loop line: runs back into "Forty-seven billion dollars in twenty nineteen..."
        {"say": "Forget that, and you go from...",
         "visual": {"type": "cta", "lines": ["Valuation", "≠ profit."],
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
assert len(spec["title"]) < 60, len(spec["title"])
print(f"{len(words)} scenes, {sum(words)} words (~{sum(words) / 2.9:.0f} s)")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "052_wework.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
