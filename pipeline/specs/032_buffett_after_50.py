"""Video 032 (global/US): Warren Buffett made 99%+ of his fortune after 52: the compounding math. Pillar: Founder story."""
import json, math, os

# ---------------------------------------------------------------- sourced facts
# Born Aug 30, 1930 (Berkshire Hathaway / Forbes profile).
BORN = 1930
# Forbes 400, first list, 1982: Buffett "with a net worth of $250 million", the "52-year-old chairman" of
# Berkshire Hathaway (Forbes, Kate Vinton, Dec 9, 2016; Forbes "Billionaire Streakers", Sept 28, 2022 and
# Oct 5, 2024; the 2022 piece puts it at "$770 million today" after inflation).
FORBES_1982_YEAR, FORBES_1982_AGE, FORBES_1982_WORTH = 1982, 52, 250e6
# Forbes real-time ranking, top 10 richest people, figures as of midnight ET Nov 1, 2026 (Forbes Argentina,
# Nov 2, 2026): Warren Buffett, net worth US$154 billion (No. 10). Moves daily with Berkshire's share price.
NOW_YEAR, NOW_WORTH = 2026, 154e9
# Berkshire Hathaway 2018 shareholder letter (Feb 23, 2019): first stock purchase on March 11, 1942, aged 11
# ("$114.75 I had begun accumulating at age six").
FIRST_STOCK_YEAR, FIRST_STOCK_AGE = 1942, 11
# Description only: AP (June 30, 2025) - gifts since 2006 total "roughly $60 billion" at value when received.
GIFTS_SINCE_2006 = 60e9

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert FORBES_1982_YEAR - BORN == FORBES_1982_AGE                     # "at fifty-two"
now_age = NOW_YEAR - BORN                                             # birthday Aug 30 has passed by Nov
assert now_age == 96
share_after_52 = (NOW_WORTH - FORBES_1982_WORTH) / NOW_WORTH
assert share_after_52 > 0.99, share_after_52                          # "more than ninety-nine percent"
years = NOW_YEAR - FORBES_1982_YEAR
assert years == 44                                                    # "for forty-four years"
multiple = NOW_WORTH / FORBES_1982_WORTH                              # 616x
cagr = multiple ** (1 / years) - 1
assert 0.155 < cagr < 0.16, cagr                                      # "about sixteen percent a year"
doubling_time = math.log(2) / math.log(1 + cagr)
assert 4.5 < doubling_time < 5.0, doubling_time                       # "roughly every five years"
doublings = math.log2(multiple)
assert 9 < doublings < 9.5, doublings                                 # "after nine doublings" (shown as 9+)
last_doubling_gain = NOW_WORTH / 2
assert last_doubling_gain == 77e9                                     # "the final doubling alone added ~77B"
assert last_doubling_gain > (NOW_WORTH / 2 - FORBES_1982_WORTH)       # ...more than all growth before it
assert FORBES_1982_AGE - FIRST_STOCK_AGE > 40                         # "investing for over forty years"
assert FIRST_STOCK_YEAR - BORN - 1 == FIRST_STOCK_AGE                      # March 1942, before his Aug birthday
print(f"{multiple:.0f}x in {years}y = {cagr:.2%}/yr, doubles every {doubling_time:.2f}y, "
      f"{doublings:.2f} doublings, {share_after_52:.2%} after 52")

# Smoothed illustration (NOT his actual year-by-year path): constant-growth curve between the two Forbes points.
xs = list(range(FORBES_1982_YEAR, NOW_YEAR + 1))
smooth = [FORBES_1982_WORTH * (1 + cagr) ** (y - FORBES_1982_YEAR) for y in xs]
assert abs(smooth[-1] - NOW_WORTH) < 1e6
half_year = FORBES_1982_YEAR + math.ceil(years - doubling_time)       # last doubling starts ~2022

spec = {
    "id": "032_buffett_after_50",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "FOUNDER STORY",
    "disclaimer": "Past returns don't predict future returns · not investment advice",
    "title": "Warren Buffett: 99% of His Fortune Came After 52",
    "description": (
        "Forbes put Warren Buffett's net worth at $250 million in 1982, when he was 52. On Nov 1, 2026, at 96, "
        f"Forbes estimated about $154 billion: {multiple:.0f} times more, so over 99% of today's fortune came "
        f"after 52 (and that is after giving away roughly $60 billion since 2006). That is like growing about "
        f"{cagr:.1%} a year for {years} years, doubling roughly every {doubling_time:.1f} years. The late boom "
        "came from an early start: he bought his first stock at 11. His returns were exceptional; the lesson is "
        "time in compounding, not copying him.\n\n"
        "Sources: Forbes 400 (1982), as reported by Forbes (Dec 9, 2016; Sept 28, 2022; Oct 5, 2024); Forbes "
        "real-time ranking as of Nov 1, 2026 (reported by Forbes Argentina, Nov 2, 2026); Berkshire Hathaway "
        "2018 shareholder letter (Feb 2019); Associated Press (June 30, 2025) on gifts since 2006. The growth "
        "curve shown is a smoothed illustration, not his actual yearly path. Net worth estimates move daily. "
        "Educational content, not investment advice; past returns don't predict future returns.\n\n"
        "#warrenbuffett #compounding #investing #personalfinance #money"
    ),
    "tags": ["warren buffett", "buffett net worth", "compound interest", "compounding", "buffett age 50",
             "berkshire hathaway", "long term investing", "founder story", "money lessons"],
    "localizations": {
        "es": {"title": "Warren Buffett: el 99% de su fortuna llegó tras los 52",
               "summary": "Forbes calculó su patrimonio en 250 millones de dólares en 1982, a los 52 años; en noviembre de 2026 eran unos 154.000 millones. Así funciona el interés compuesto con el tiempo."},
        "pt": {"title": "Warren Buffett: 99% da fortuna veio depois dos 52",
               "summary": "A Forbes estimou sua fortuna em 250 milhões de dólares em 1982, aos 52 anos; em novembro de 2026, cerca de 154 bilhões. É a matemática dos juros compostos ao longo do tempo."},
        "hi": {"title": "वॉरेन बफे: 99% दौलत 52 की उम्र के बाद आई",
               "summary": "1982 में, 52 की उम्र में, फोर्ब्स ने उनकी संपत्ति 25 करोड़ डॉलर आंकी; नवंबर 2026 में करीब 154 अरब डॉलर। समय के साथ चक्रवृद्धि का गणित ऐसे काम करता है।"},
        "id": {"title": "Warren Buffett: 99% Kekayaannya Datang Setelah Usia 52",
               "summary": "Forbes menaksir kekayaannya 250 juta dolar pada 1982, saat ia berusia 52; pada November 2026 sekitar 154 miliar dolar. Inilah matematika bunga majemuk seiring waktu."},
        "de": {"title": "Warren Buffett: 99 % seines Vermögens kamen nach 52",
               "summary": "Forbes schätzte sein Vermögen 1982, mit 52, auf 250 Millionen Dollar; im November 2026 auf rund 154 Milliarden. So wirkt der Zinseszins über lange Zeit."},
        "fr": {"title": "Warren Buffett : 99 % de sa fortune après 52 ans",
               "summary": "Forbes estimait sa fortune à 250 millions de dollars en 1982, à 52 ans ; environ 154 milliards en novembre 2026. Voici les maths des intérêts composés dans la durée."},
    },
    "thumbnail": {"big": f"+${last_doubling_gain / 1e9:.0f}B", "line": "The last doubling", "color": "gold",
                  "photo": {"file": "assets/photos/warren_buffett_student_visit.jpg", "focus": [0.64, 0.3]}},
    "scenes": [
        {"say": "More than ninety-nine percent of Warren Buffett's fortune came after he turned fifty-two.",
         "visual": {"type": "photo", "file": "assets/photos/warren_buffett_student_visit.jpg", "value": "99%+",
                    "label": "of his fortune came after age 52", "color": "gold", "focus": [0.62, 0.35]}},
        {"say": "In nineteen eighty-two, at fifty-two, Forbes put his net worth at two hundred and fifty million dollars. In November twenty twenty-six: about one hundred and fifty-four billion.",
         "visual": {"type": "compare", "title": "Buffett's net worth (Forbes)",
                    "left": {"label": f"Age {FORBES_1982_AGE}", "value": FORBES_1982_WORTH, "color": "slate"},
                    "right": {"label": f"Age {now_age}", "value": NOW_WORTH, "color": "gold"}}},
        {"say": "That's like growing about sixteen percent a year for forty-four years. Smoothed out, the curve looks flat for decades, then shoots up.",
         "visual": {"type": "line", "title": f"Smoothed: {cagr:.1%} a year", "x": xs,
                    "series": [{"label": "", "values": smooth, "color": "gold"}],
                    "x_label": "illustration, not actual yearly values",
                    "highlight": {"from": half_year, "to": NOW_YEAR, "label": "last doubling"}}},
        {"say": "At that pace, money doubles roughly every five years. After nine doublings, the final doubling alone added about seventy-seven billion dollars.",
         "visual": {"type": "equation", "title": "The doubling math",
                    "lines": [{"text": "Doubles every ~5 years", "color": "text", "size": 70},
                              {"text": f"{int(doublings)}+ doublings since {FORBES_1982_YEAR}", "color": "muted", "size": 60},
                              {"text": f"Last one: +${last_doubling_gain / 1e9:.0f}B", "color": "gold", "size": 96}]}},
        {"say": "And that late boom came from an early start: he bought his first stock at eleven.",
         "visual": {"type": "timeline", "title": f"{FORBES_1982_AGE - FIRST_STOCK_AGE} years of investing by {FORBES_1982_AGE}", "start": 10, "end": 70,
                    "rows": [{"label": "Investing", "from": FIRST_STOCK_AGE, "color": "green"},
                             {"label": "Forbes 400", "from": FORBES_1982_AGE, "color": "gold"}]}},
        {"say": "His returns were exceptional, and nobody can count on them. The real lesson is time: start early, and give compounding decades to work.",
         "visual": {"type": "photo", "file": "assets/photos/berkshire_shareholders_sign.jpg", "title": "The lesson",
                    "label": "Not his returns. His time.", "focus": [0.5, 0.55]}},
        {"say": "Follow for tomorrow's money lesson.",
         "visual": {"type": "cta", "lines": ["Start early.", "Let time work."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "032_buffett_after_50.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
