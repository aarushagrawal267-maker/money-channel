"""Video 054 (India story for a global viewer): Infosys started with ₹10,000 from Sudha Murty. Pillar: Founder story."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Founding. Infosys was incorporated as Infosys Consultants Private Limited in Pune on 2 July 1981 by seven engineers:
# N. R. Narayana Murthy, Nandan Nilekani, Kris Gopalakrishnan, S. D. Shibulal, K. Dinesh, N. S. Raghavan and Ashok
# Arora (Wikipedia "Infosys", citing Moneycontrol company history and Rediff "Major events in the history of Infosys",
# 7 Oct 2017); moved to Bangalore in 1983 (Infosys "About Infosys", archived).
FOUNDED_YEAR, FOUNDERS = 1981, 7
# The seed money. Business Today (15 Mar 2024, Sudha Murty at the India Today Conclave): "Infosys started with a
# loan of Rs 10,000 that Sudha Murty gave her husband Narayana Murthy in 1981"; she "gave Rs 10,000 to her husband
# from the Rs 10,250 she had"; her words: "I took a little bit of risk. I assumed I will write off whether he
# succeeds or not". (She also calls it her "only investment"; the script says "the money came from", not "loan".)
SEED, SHE_HAD = 10_000, 10_250
# 1993 IPO. Business Today, "Year 1993 round-up" (print edition, 9 Jan 2011): "The IPO scraped through after
# investment banker Morgan Stanley picked up 13 per cent of the company's equity". Wikipedia (citing in.com):
# launched February 1993, "initially undersubscribed".
IPO_YEAR, MS_STAKE = 1993, 13
# Nasdaq. Listed its ADRs on Nasdaq on 11 March 1999, "the first Indian company to be listed on Nasdaq"
# (Wikipedia, citing Jairam Ramesh, India Today, 29 Mar 1999).
NASDAQ_YEAR = 1999
# Today. Infosys press release, 23 Apr 2026 (Q4 and FY2025-26 results): FY26 revenue $20,158 million.
# PTI via ThePrint (23 Apr 2026): FY26 revenue "rose 9.6 per cent to Rs 178,650 crore".
REV_FY26_USD = 20_158e6
CRORE = 1e7
REV_FY26_INR = 178_650 * CRORE
# Criticism / balance. Business Today (4 Jan 2024), Murthy to CNBC-TV18 on keeping his wife out of Infosys:
# "I think what I was doing those days was wrong. I was wrongly idealistic."
# CNBC (6 Nov 2023): Murthy said "young people should be working 70 hours a week"; the All India IT and ITeS
# Employees' Union called a 70-hour week "illegal" (description only).

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert SEED == 10_000                                         # "ten thousand rupees"
assert SEED / SHE_HAD > 0.97                                  # "almost everything she had" (97.6%)
assert FOUNDERS - 1 == 6                                      # "Narayana Murthy and six other engineers"
assert REV_FY26_USD > 20e9 and round(REV_FY26_USD / 1e9, 1) == 20.2   # "twenty billion dollars a year" / "$20.2B"
lakh_crore = REV_FY26_INR / (1e5 * CRORE)
assert round(lakh_crore, 2) == 1.79                           # on screen "₹1.79 lakh crore"
assert MS_STAKE == 13                                         # "thirteen percent"
assert IPO_YEAR - FOUNDED_YEAR == 12                          # "twelve years to go public"
assert NASDAQ_YEAR == 1999                                    # "by nineteen ninety-nine"
print(f"seed ₹{SEED:,} of ₹{SHE_HAD:,} ({SEED / SHE_HAD:.1%}); FY26 ${REV_FY26_USD / 1e9:.2f}B = ₹{lakh_crore:.2f} lakh Cr")

spec = {
    "id": "054_narayana_murthy",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "FOUNDER STORY",
    "disclaimer": "Sources: Infosys, Business Today, PTI · see description",
    "title": "Infosys Started With ₹10,000. Its IPO Nearly Flopped",
    "description": (
        "Infosys started in 1981 with ₹10,000 that Sudha Murty gave her husband, Narayana Murthy, out of the ₹10,250 "
        "she had. He and six other engineers founded the company in Pune. In the year to March 2026 Infosys reported "
        f"${REV_FY26_USD / 1e9:.1f} billion in revenue (₹{lakh_crore:.2f} lakh crore). The road wasn't smooth: its 1993 "
        "public share sale only scraped through after Morgan Stanley bought 13% of the company. By 1999 it was the "
        "first Indian company listed on Nasdaq.\n\n"
        "The other side: Murthy later said keeping his wife, an engineer, out of the company was \"wrongly "
        "idealistic\" (CNBC-TV18, Jan 2024), and his 2023 call for young people to work 70 hours a week was "
        "criticised; an IT employees' union called a 70-hour week \"illegal\" (CNBC, Nov 2023). The lesson: you can "
        "start small, but expect years of work and near-misses.\n\n"
        "Sources: Infosys Q4 FY2025-26 press release (23 Apr 2026); PTI via ThePrint (23 Apr 2026); Business Today "
        "(15 Mar 2024, Sudha Murty at the India Today Conclave; 4 Jan 2024, Murthy to CNBC-TV18; 9 Jan 2011, 1993 IPO); "
        "CNBC (6 Nov 2023); India Today (29 Mar 1999) on the Nasdaq listing; Infosys company history. "
        "1 lakh crore = 1 trillion. Educational content, not investment advice.\n\n"
        "#infosys #india #founderstory #business #entrepreneurship"
    ),
    "tags": ["infosys", "narayana murthy", "sudha murty", "infosys story", "infosys 10000 rupees",
             "infosys ipo 1993", "founder story", "indian business history", "startup lessons"],
    "localizations": {
        "es": {"title": "Infosys empezó con ₹10.000. Su salida a bolsa casi falla",
               "summary": "En 1981, Sudha Murty dio 10.000 rupias a su marido, Narayana Murthy, para fundar Infosys con otros seis ingenieros. Hoy factura 20.200 millones de dólares al año. La historia completa, con sus tropiezos."},
        "pt": {"title": "Infosys começou com ₹10.000. O IPO quase fracassou",
               "summary": "Em 1981, Sudha Murty deu 10.000 rúpias ao marido, Narayana Murthy, para fundar a Infosys com outros seis engenheiros. Hoje fatura 20,2 bilhões de dólares por ano. A história, com os tropeços."},
        "hi": {"title": "Infosys ₹10,000 से शुरू हुई, IPO लगभग फ्लॉप हुआ",
               "summary": "1981 में Sudha Murty ने अपने पति Narayana Murthy को ₹10,000 दिए और छह और इंजीनियरों के साथ Infosys बनी। आज सालाना आय $20.2 अरब है। पूरी कहानी, उतार-चढ़ाव के साथ।"},
        "id": {"title": "Infosys Dimulai dengan ₹10.000, IPO-nya Nyaris Gagal",
               "summary": "Pada 1981, Sudha Murty memberi 10.000 rupee kepada suaminya, Narayana Murthy, untuk mendirikan Infosys bersama enam insinyur lain. Kini pendapatannya 20,2 miliar dolar per tahun. Kisahnya, termasuk jatuh bangunnya."},
        "de": {"title": "Infosys begann mit ₹10.000, der Börsengang scheiterte fast",
               "summary": "1981 gab Sudha Murty ihrem Mann Narayana Murthy 10.000 Rupien, um mit sechs weiteren Ingenieuren Infosys zu gründen. Heute 20,2 Milliarden Dollar Umsatz im Jahr. Die Geschichte, mit allen Rückschlägen."},
        "fr": {"title": "Infosys a démarré avec ₹10 000, son IPO a failli échouer",
               "summary": "En 1981, Sudha Murty a donné 10 000 roupies à son mari, Narayana Murthy, pour fonder Infosys avec six autres ingénieurs. Aujourd'hui, 20,2 milliards de dollars de revenus par an. L'histoire, revers compris."},
    },
    "scenes": [
        # hook: the starting number on frame 0 + the end result + open loop ("how?")
        {"say": "Ten thousand rupees, nineteen eighty-one. Now twenty billion dollars a year. How?",
         "visual": {"type": "stat", "value": f"₹{SEED // 1000}K", "label": f"Infosys's starting money, {FOUNDED_YEAR}",
                    "sub": f"revenue FY2025-26: ${REV_FY26_USD / 1e9:.1f}B (₹{lakh_crore:.2f} lakh Cr)", "color": "gold"}},
        {"say": "That's Infosys, founded by Narayana Murthy and six other engineers.",
         "visual": {"type": "pair", "title": f"Pune, {FOUNDED_YEAR}",
                    "left": {"label": "Murthy", "sub": "co-founder", "color": "blue"},
                    "right": {"label": "+6 more", "sub": "engineers", "color": "green"}}},
        {"say": "The money came from his wife, Sudha Murty: almost everything she had.",
         "visual": {"type": "compare", "title": "Sudha Murty's money",
                    "left": {"label": "She had", "value": SHE_HAD, "color": "slate"},
                    "right": {"label": "She gave", "value": SEED, "color": "gold"}}},
        # mid-video re-hook: opens a second loop (how close did it come?)
        {"say": "But here's the catch: going public nearly flopped.",
         "visual": {"type": "equation", "title": "The catch",
                    "lines": [{"text": f"{IPO_YEAR} share sale:", "color": "text", "size": 96},
                              {"text": "nearly flopped.", "color": "red", "size": 110}]}},
        {"say": "In nineteen ninety-three, it scraped through after Morgan Stanley bought thirteen percent.",
         "visual": {"type": "stat", "value": f"{MS_STAKE}%", "label": "of Infosys bought by Morgan Stanley",
                    "sub": f"so the {IPO_YEAR} share sale could scrape through", "color": "red"}},
        {"say": "By nineteen ninety-nine, it was the first Indian company on Nasdaq.",
         "visual": {"type": "timeline", "title": "Slow, then fast", "start": 1980, "end": 2010,
                    "rows": [{"label": "Listed in India", "from": IPO_YEAR, "color": "gold"},
                             {"label": "Listed on Nasdaq", "from": NASDAQ_YEAR, "color": "green"}]}},
        {"say": "Murthy later said keeping his wife out of Infosys was 'wrongly idealistic.'",
         "visual": {"type": "equation", "title": "Narayana Murthy, 2024",
                    "lines": [{"text": "Keeping Sudha out:", "color": "text", "size": 84},
                              {"text": "“I was wrongly", "color": "gold", "size": 100},
                              {"text": "idealistic.”", "color": "gold", "size": 100}]}},
        {"say": "The lesson: you can start small. Infosys took twelve years to go public.",
         "visual": {"type": "pair", "title": "The lesson",
                    "left": {"label": "Start small", "sub": f"₹{SEED:,}", "color": "gold"},
                    "right": {"label": "Stay long", "sub": f"{IPO_YEAR - FOUNDED_YEAR} years to the IPO", "color": "green"}}},
        # loop line: runs back into "Ten thousand rupees, nineteen eighty-one..."
        {"say": "And it all began with...",
         "visual": {"type": "cta", "lines": [f"₹{SEED:,}.", "Twelve years."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "054_narayana_murthy.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
