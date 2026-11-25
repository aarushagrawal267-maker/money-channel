"""Video 038 (India story for a global viewer): Dhirubhai Ambani, from a job in Aden to Reliance. Pillar: Founder story."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Born 28 Dec 1932 (Britannica); died 6 July 2002, aged 69 (Reuters obituary via Dawn, 8 July 2002; VOA, 7 July 2002).
BORN_YEAR, DIED_AGE = 1932, 69
# Early career. Reuters (via Dawn, 8 July 2002): "At 17 he went to Yemen to join his eldest brother, working as a
# petrol station attendant and later as a clerk for a local Burmah Shell affiliate". VOA (7 July 2002): left India
# at 17 to work as a gas pump attendant in Yemen. Britannica: went to Aden at 17, clerk at A. Besse & Co.
# DETAILS VARY between accounts (petrol pump vs clerk, exact years), so the script attributes them ("obituaries say").
ADEN_AGE = 17
# Return to India and trading business: RIL "Our history" says 1957 (yarn trading in Mumbai); VOA and Business
# Today (19 June 2026) say 1958. Conflicting, so no year is spoken ("back in Mumbai").
# 1977 IPO. RIL "Our history" (ril.com, accessed Nov 2026): "The issue is oversubscribed seven times".
# Business Standard (7 June 2012): Reliance "issued 2.8 million equity shares of Rs 10 each in its first equity
# sale to the public investors in November 1977".
IPO_YEAR, IPO_SHARES, IPO_PRICE, OVERSUB = 1977, 2.8e6, 10, 7
# RIL Q4 / FY2025-26 media release (24 Apr 2026): "Gross Revenue increased by 9.8% Y-o-Y to ₹ 1,175,919 crore
# ($ 124.0 billion)".
CRORE = 1e7
RIL_REV_FY26 = 1_175_919 * CRORE
RIL_REV_FY26_USD = 124.0e9
# Criticism. Reuters (via Dawn, 8 July 2002): Reliance's growth "prompted accusations that his success owed as
# much to manipulating government policy as to shrewd business decisions"; Ambani: "Controversy is the price to
# be paid for success." VOA (7 July 2002) reports similar criticism.

# ---------------------------------------------------------------- checks behind spoken / shown claims
ipo_raised = IPO_SHARES * IPO_PRICE
assert ipo_raised == 2.8 * CRORE                             # "two point eight crore rupees"
assert ipo_raised == 28e6                                    # "that's twenty-eight million"
bids = ipo_raised * OVERSUB
assert abs(bids - 19.6 * CRORE) < 1                          # demand ≈ 7x the shares on offer (shown)
ipo_age = IPO_YEAR - BORN_YEAR - 1                           # Nov 1977, before his 28 Dec birthday
assert ipo_age == 44                                         # "at forty-four"
lakh_crore = RIL_REV_FY26 / (1e5 * CRORE)
assert 11 < lakh_crore < 12, lakh_crore                      # "over eleven lakh crore rupees"
assert round(RIL_REV_FY26_USD / 1e9) == 124                  # "about a hundred and twenty-four billion dollars"
assert DIED_AGE + 1 == 70                                    # timeline runs to 70
print(f"IPO ₹{ipo_raised / CRORE:.1f} Cr at age {ipo_age}; FY26 revenue ₹{lakh_crore:.2f} lakh crore")

spec = {
    "id": "038_dhirubhai",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "FOUNDER STORY",
    "disclaimer": "Sources: RIL, Reuters, VOA, Business Standard · see description",
    "title": "Dhirubhai Ambani: From a Job in Yemen to Reliance",
    "description": (
        f"Reliance Industries brought in ₹{lakh_crore:.2f} lakh crore (about $124 billion) in FY2025-26. Its founder, "
        "Dhirubhai Ambani, left India at 17 for Aden, in today's Yemen, where obituaries say he worked at a petrol "
        "station and then as a clerk (accounts of these early details vary). Back in Mumbai he traded yarn and "
        "spices, and in 1977 took Reliance public: a ₹2.8 crore (₹28 million) issue oversubscribed seven times. "
        "His methods also drew criticism, reported by Reuters at his death in 2002. (1 crore = 10 million; "
        "1 lakh crore = 1 trillion.)\n\n"
        "Sources: Reliance Industries Q4 FY2025-26 media release (24 Apr 2026); RIL 'Our history' (ril.com); "
        "Business Standard (7 Jun 2012) on the 1977 issue; Reuters obituary via Dawn (8 Jul 2002); Voice of "
        "America (7 Jul 2002); Encyclopaedia Britannica. Educational content, not investment advice.\n\n"
        "#reliance #india #business #entrepreneurship #founderstory"
    ),
    "tags": ["dhirubhai ambani", "reliance industries", "reliance ipo 1977", "ambani story",
             "indian business history", "founder story", "business case study", "india"],
    "localizations": {
        "es": {"title": "Dhirubhai Ambani: de un empleo en Yemen a Reliance",
               "summary": "Dejó la India a los 17 para trabajar en Adén (Yemen) y fundó Reliance, que hoy ingresa unos 124.000 millones de dólares al año. Su historia, con sus luces y sus críticas."},
        "pt": {"title": "Dhirubhai Ambani: de um emprego no Iêmen à Reliance",
               "summary": "Ele deixou a Índia aos 17 para trabalhar em Áden (Iêmen) e fundou a Reliance, que hoje fatura cerca de 124 bilhões de dólares por ano. A história, com méritos e críticas."},
        "hi": {"title": "धीरूभाई अंबानी: यमन की नौकरी से रिलायंस तक",
               "summary": "17 साल की उम्र में वे अदन (यमन) गए और फिर रिलायंस बनाई, जिसकी सालाना आय अब 11 लाख करोड़ रुपये से ज़्यादा है। उनकी कहानी, तारीफ़ और आलोचना दोनों के साथ।"},
        "id": {"title": "Dhirubhai Ambani: Dari Kerja di Yaman ke Reliance",
               "summary": "Ia meninggalkan India pada usia 17 untuk bekerja di Aden (Yaman), lalu mendirikan Reliance yang kini berpendapatan sekitar 124 miliar dolar per tahun. Kisahnya, termasuk kritiknya."},
        "de": {"title": "Dhirubhai Ambani: Vom Job im Jemen zu Reliance",
               "summary": "Mit 17 ging er nach Aden im heutigen Jemen und gründete später Reliance, heute rund 124 Milliarden Dollar Umsatz im Jahr. Seine Geschichte, mit Lob und Kritik."},
        "fr": {"title": "Dhirubhai Ambani : d'un job au Yémen à Reliance",
               "summary": "À 17 ans, il part travailler à Aden, au Yémen, puis fonde Reliance, qui réalise aujourd'hui environ 124 milliards de dollars de revenus par an. Son histoire, éloges et critiques compris."},
    },
    "thumbnail": {"big": f"${RIL_REV_FY26_USD / 1e9:.0f}B", "line": "In sales, every year", "color": "gold",
                  "photo": {"file": "assets/photos/dhirubhai_ambani_nail_art.jpg", "focus": [0.5, 0.45]}},
    "scenes": [
        # hook: the biggest number on frame 0 + open loop (how do you get from Yemen to that?)
        {"say": "Over eleven lakh crore rupees a year. Its founder started in Yemen.",
         "visual": {"type": "equation", "title": "Reliance revenue, FY2025-26",
                    "lines": [{"text": f"₹{lakh_crore:.2f} lakh crore", "color": "gold", "size": 100},
                              {"text": f"≈ ${RIL_REV_FY26_USD / 1e9:.0f} billion a year", "color": "text", "size": 64},
                              {"text": "source: RIL results, Apr 2026", "color": "muted", "size": 40}]}},
        {"say": "At seventeen, Dhirubhai Ambani left India for Aden, in today's Yemen.",
         "visual": {"type": "photo", "file": "assets/photos/dhirubhai_ambani_nail_art.jpg", "title": "Dhirubhai Ambani",
                    "label": f"Age {ADEN_AGE}: leaves India for Aden, today's Yemen", "focus": [0.5, 0.45]}},
        {"say": "Obituaries say he worked at a petrol station, then as a clerk.",
         "visual": {"type": "equation", "title": "First jobs (accounts vary)",
                    "lines": [{"text": "Petrol station", "color": "text", "size": 100},
                              {"text": "then", "color": "muted", "size": 60},
                              {"text": "Clerk", "color": "gold", "size": 110}]}},
        {"say": "Back in Mumbai, he traded yarn and spices. At forty-four, he took Reliance public.",
         "visual": {"type": "photo", "file": "assets/photos/bse_building_mumbai.jpg", "title": "Back in Mumbai",
                    "value": f"Age {ipo_age}", "color": "gold", "label": f"takes Reliance public ({IPO_YEAR}) · BSE today",
                    "focus": [0.45, 0.35]}},
        {"say": "That nineteen seventy-seven I-P-O raised two point eight crore rupees, oversubscribed seven times.",
         "visual": {"type": "compare", "title": f"{IPO_YEAR} IPO: {OVERSUB}x oversubscribed",
                    "left": {"label": "On offer", "value": ipo_raised, "color": "slate"},
                    "right": {"label": "Demand", "value": bids, "color": "green"}}},
        # mid-video re-hook: opens a second loop (what's the other side?)
        {"say": "But here's the catch: there's another side.",
         "visual": {"type": "equation", "title": "The catch",
                    "lines": [{"text": "Big success.", "color": "text", "size": 110},
                              {"text": "Big questions.", "color": "red", "size": 110}]}},
        {"say": "Reuters reported accusations his success owed as much to policy manipulation as business skill.",
         "visual": {"type": "pair", "title": "Two sides",
                    "left": {"label": "Praised", "sub": "for thinking big", "color": "green"},
                    "right": {"label": "Criticised", "sub": "over policy influence", "color": "red"}}},
        {"say": "The lesson: think big and bring investors along. But how you win matters.",
         "visual": {"type": "equation", "title": "The lesson",
                    "lines": [{"text": "Think big.", "color": "gold", "size": 110},
                              {"text": "Bring people with you.", "color": "text", "size": 70},
                              {"text": "How you win matters too.", "color": "muted", "size": 56}]}},
        # loop line: runs back into "Over eleven lakh crore rupees a year..."
        {"say": "From a teenager's job abroad, to...",
         "visual": {"type": "cta", "lines": ["Think big.", "Play fair."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "038_dhirubhai.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
