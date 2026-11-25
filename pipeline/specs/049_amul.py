"""Video 049 (India story for a global viewer): Amul's cooperative model, most of the rupee goes to farmers. Pillar: Business Breakdowns."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Jayen Mehta (then COO, now managing director of GCMMF, the federation that markets Amul), Rural Voice dialogue
# "Sahakar se Samriddhi", reported by Rural Voice (eng.ruralvoice.in, 25 Jun 2022): "In India, farmers get about
# 80-85 per cent of the rupee spent by the consumer. In other parts of the world, only one-third goes to the
# farmer; the rest is shared equally between the retailer and the processor." This is AMUL'S OWN figure (not an
# independent audit), so the video attributes it ("Amul says" / on-screen "Amul's own estimate").
FARMER_SHARE_LOW, FARMER_SHARE_HIGH = 80, 85
FARMER_SHARE_ELSEWHERE = 1 / 3
# GCMMF FY2025-26 results (5 Apr 2026, as published by DeshGujarat and Dairy Industries International, 7 Apr 2026):
# Amul brand turnover "crossed the ₹1 Lakh Crore mark for the financial year 2025-26", up 11% "over a base of
# Rs. 90,000 crores in 2024-25"; GCMMF sales turnover ₹73,450 crore (+11.4% from ₹65,911 crore); "3.6 million
# farmers"; "31 million Liters of milk every day"; "its 18 member district cooperatives".
CRORE = 1e7
LAKH_CRORE = 1e5 * CRORE                                    # = 1 trillion rupees
BRAND_TURNOVER_FY26 = 1 * LAKH_CRORE                         # "crossed" -> spoken as "topped"
BRAND_TURNOVER_FY25 = 90_000 * CRORE
GCMMF_TURNOVER_FY26 = 73_450 * CRORE
FARMERS = 3.6e6
MILK_LITRES_PER_DAY = 31e6
DISTRICT_UNIONS = 18
# Three-tier "Amul model": village dairy cooperative societies collect milk, district milk unions (owned by the
# societies) process it, the state federation (GCMMF) markets it. Source: Amul, "The Amul Model" / "A note on the
# achievements of the dairy cooperatives" (amul.com): "dairy cooperative societies at the village level federated
# under a milk union at the district level and a federation of member unions at the state level".
# FX for the one USD equivalent: rupee closed at 93.44 per US dollar on 18 Nov 2026 (PTI, via Telangana Today).
INR_PER_USD = 93.44
INR_PER_USD_FY26_LOW = 85.0                                   # conservative bound for rates during Apr 2025-Mar 2026

# ---------------------------------------------------------------- checks behind spoken / shown claims
per_100 = (FARMER_SHARE_LOW, FARMER_SHARE_HIGH)
assert per_100[0] == 80                                       # "about eighty rupees of every hundred"
left_over = 100 - FARMER_SHARE_LOW
assert left_over == 20                                        # "at most twenty rupees for everything else"
assert round(FARMER_SHARE_ELSEWHERE * 100) == 33              # "about a third" (bars show 33)
assert abs(BRAND_TURNOVER_FY25 * 1.11 - BRAND_TURNOVER_FY26) / BRAND_TURNOVER_FY26 < 0.01   # +11% is consistent
usd_now = BRAND_TURNOVER_FY26 / INR_PER_USD
usd_fy = BRAND_TURNOVER_FY26 / INR_PER_USD_FY26_LOW
assert usd_now > 10e9 and usd_fy > 10e9                       # "over ten billion dollars" at today's or last year's rates
assert round(usd_now / 1e9, 1) == 10.7                        # on screen "≈ $10.7B"
assert FARMERS == 3_600_000                                   # "three point six million"
assert MILK_LITRES_PER_DAY == 31_000_000 and DISTRICT_UNIONS == 18
assert GCMMF_TURNOVER_FY26 < BRAND_TURNOVER_FY26              # description: federation's own sales are a part of it
print(f"farmers get ₹{per_100[0]}-{per_100[1]} of ₹100; brand ₹{BRAND_TURNOVER_FY26 / LAKH_CRORE:.0f} lakh crore "
      f"≈ ${usd_now / 1e9:.1f}B; GCMMF ₹{GCMMF_TURNOVER_FY26 / CRORE:,.0f} Cr")

spec = {
    "id": "049_amul",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "INDIA STORY",
    "disclaimer": "Sources: GCMMF / Amul (FY2025-26), Rural Voice · see description",
    "title": "Amul Business Model: ₹80 of Every ₹100 to Farmers",
    "description": (
        "How does Amul's business model work? Amul is a cooperative owned by about 3.6 million dairy farmers in "
        "Gujarat, India. Amul says farmers get about ₹80-85 of every ₹100 a shopper spends on its products, compared "
        "with about a third in many other countries (Amul's own estimate, not an independent audit). That leaves "
        "little for everything else, yet the Amul brand topped ₹1 lakh crore (₹1 trillion, about $10.7 billion) in "
        "sales in FY2025-26, on about 31 million litres of milk a day. The lesson: a thin margin on huge volume can "
        "build a giant.\n\n"
        "How it works: village dairy cooperatives collect the milk, 18 district unions process it, and the Gujarat "
        "Cooperative Milk Marketing Federation (GCMMF) sells it under the Amul brand. GCMMF's own sales were ₹73,450 "
        "crore; the brand figure also includes the district unions.\n\n"
        "Sources: GCMMF FY2025-26 results (5 Apr 2026, via DeshGujarat and Dairy Industries International); Jayen "
        "Mehta, GCMMF, quoted by Rural Voice (25 Jun 2022); Amul, 'The Amul Model' and 'A note on the achievements of the dairy cooperatives' (amul.com). Dollar figure at "
        "₹93.44 per $ (PTI, 18 Nov 2026). 1 crore = 10 million; 1 lakh crore = 1 trillion.\n\n"
        "#amul #india #business #cooperative #businessmodel"
    ),
    "tags": ["amul business model", "amul case study", "how amul works", "amul cooperative", "gcmmf",
             "dairy cooperative", "indian business", "business breakdown", "india"],
    "localizations": {
        "es": {"title": "El modelo de Amul: ₹80 de cada ₹100 para los granjeros",
               "summary": "Amul es una cooperativa de 3,6 millones de ganaderos en la India. Según Amul, el productor recibe unas 80 de cada 100 rupias, y aun así su marca vende más de 10.000 millones de dólares al año."},
        "pt": {"title": "O modelo da Amul: ₹80 de cada ₹100 para os produtores",
               "summary": "A Amul é uma cooperativa de 3,6 milhões de produtores de leite na Índia. Segundo a Amul, o produtor recebe cerca de 80 de cada 100 rúpias, e mesmo assim a marca vende mais de 10 bilhões de dólares por ano."},
        "hi": {"title": "Amul का बिज़नेस मॉडल: हर ₹100 में से ₹80 किसानों को",
               "summary": "Amul 36 लाख डेयरी किसानों की सहकारी संस्था है। Amul के मुताबिक हर ₹100 में से करीब ₹80-85 किसानों को जाते हैं, फिर भी ब्रांड की बिक्री ₹1 लाख करोड़ के पार है।"},
        "id": {"title": "Model Bisnis Amul: ₹80 dari Tiap ₹100 untuk Peternak",
               "summary": "Amul adalah koperasi milik 3,6 juta peternak sapi perah di India. Menurut Amul, peternak menerima sekitar 80 dari tiap 100 rupee, namun penjualan mereknya tetap di atas 10 miliar dolar setahun."},
        "de": {"title": "Amuls Geschäftsmodell: ₹80 von ₹100 für die Bauern",
               "summary": "Amul ist eine Genossenschaft von 3,6 Millionen Milchbauern in Indien. Laut Amul erhalten sie rund 80 von 100 Rupien, und trotzdem setzt die Marke über 10 Milliarden Dollar im Jahr um."},
        "fr": {"title": "Le modèle d'Amul : ₹80 sur ₹100 pour les éleveurs",
               "summary": "Amul est une coopérative de 3,6 millions d'éleveurs laitiers en Inde. Selon Amul, ils touchent environ 80 roupies sur 100, et pourtant la marque vend plus de 10 milliards de dollars par an."},
    },
    "scenes": [
        # hook: the surprising number on frame 0 + open loop ("why?")
        {"say": "Spend a hundred rupees on Amul: about eighty goes to farmers. Why?",
         "visual": {"type": "stat", "value": f"₹{per_100[0]}–{per_100[1]}", "label": "of every ₹100 goes to farmers",
                    "sub": "Amul's own estimate (GCMMF, 2022)", "color": "gold"}},
        {"say": "Amul's Jayen Mehta says elsewhere, farmers often get about a third.",
         "visual": {"type": "bars", "title": "Farmers' share of ₹100 spent", "format": "num",
                    "items": [{"label": "Amul", "value": per_100[0], "color": "green"},
                              {"label": "Elsewhere", "value": round(FARMER_SHARE_ELSEWHERE * 100), "color": "slate"}]}},
        {"say": "Because farmers own it. Three point six million of them.",
         "visual": {"type": "pair", "title": "3.6 million owners",
                    "left": {"label": "Farmers", "sub": "own the business", "color": "green"},
                    "right": {"label": "Amul", "sub": "sells for them", "color": "gold"}}},
        {"say": "Villages collect the milk, eighteen district unions process it, one federation sells it.",
         "visual": {"type": "equation", "title": "The Amul model",
                    "lines": [{"text": "Village: collects", "color": "text", "size": 80},
                              {"text": f"{DISTRICT_UNIONS} unions: process", "color": "text", "size": 80},
                              {"text": "Federation: sells", "color": "gold", "size": 80}]}},
        # mid-video re-hook: opens a second loop (how can that be big?)
        {"say": "Now the twist: that leaves Amul at most twenty rupees for everything else.",
         "visual": {"type": "compare", "title": "Of every ₹100 (Amul's estimate)",
                    "left": {"label": "Farmers", "value": per_100[0], "color": "green"},
                    "right": {"label": "Everything else", "value": left_over, "color": "red"}}},
        {"say": "Yet Amul brand sales topped one lakh crore rupees: over ten billion dollars.",
         "visual": {"type": "equation", "title": "Amul brand sales, FY2025-26",
                    "lines": [{"text": "₹1 lakh crore+", "color": "green", "size": 110},
                              {"text": f"≈ ${usd_now / 1e9:.1f} billion", "color": "text", "size": 72},
                              {"text": "source: GCMMF, April 2026", "color": "muted", "size": 44}]}},
        {"say": "That's from thirty-one million litres of milk, every single day.",
         "visual": {"type": "stat", "value": f"{MILK_LITRES_PER_DAY / 1e6:.0f}M", "label": "litres of milk, every day",
                    "sub": f"from {FARMERS / 1e6:.1f} million farmer-owners", "color": "gold"}},
        {"say": "The lesson: thin margins on huge volume can build a giant.",
         "visual": {"type": "pair", "title": "The lesson",
                    "left": {"label": "Thin margin", "sub": "per litre", "color": "slate"},
                    "right": {"label": "Huge volume", "sub": "every day", "color": "green"}}},
        # loop line: runs back into "Spend a hundred rupees on Amul..."
        {"say": "So next time you buy a packet of milk, remember...",
         "visual": {"type": "cta", "lines": ["₹80 of ₹100.", "Farmer-owned."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "049_amul.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
