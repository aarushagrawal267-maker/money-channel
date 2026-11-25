"""Video 046 (global/USD): bonds explained as lending to a friend: coupon, maturity, and why prices fall when
rates rise. Pillar: How Markets Work. Illustration only: every number is computed here (no sourced data)."""
import json, os

# ---------------------------------------------------------------- illustration (assumptions)
FACE = 1_000          # amount lent, repaid at maturity
COUPON_RATE = 0.04    # 4% a year -> $40, paid once a year (simplified; many government bonds pay twice a year)
YEARS = 10
NEW_RATE = 0.05       # rates rise: new 10-year bonds now pay 5%
coupon = FACE * COUPON_RATE
new_coupon = FACE * NEW_RATE

def price(market_rate, years=YEARS):
    """Present value of the remaining coupons + repayment, discounted at the rate new bonds pay."""
    return sum(coupon / (1 + market_rate) ** t for t in range(1, years + 1)) + FACE / (1 + market_rate) ** years

def irr(p, lo=0.0, hi=0.5):
    """Yearly return a buyer earns paying p and holding to maturity (bisection)."""
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if price(mid) > p else (lo, mid)
    return (lo + hi) / 2

p_new = price(NEW_RATE)
drop = FACE - p_new
rates_axis = [2, 3, 4, 5, 6, 7]                         # % paid by new bonds
prices_axis = [round(price(x / 100)) for x in rates_axis]

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert coupon == 40 and new_coupon == 50                 # "forty dollars a year" / "new bonds pay fifty"
assert abs(price(COUPON_RATE) - FACE) < 1e-9             # at 4%, the bond is worth exactly its $1,000
assert 922 < p_new < 923.5, p_new                        # "about nine hundred twenty-three"
assert 77 < drop < 78, drop                              # "lost seventy-seven dollars"
assert abs(irr(p_new) - NEW_RATE) < 1e-6                 # "where buyers earn five percent"
assert coupon * YEARS == 400                             # (shown) $400 of interest over ten years
assert all(a > b for a, b in zip(prices_axis, prices_axis[1:]))   # "rates up, prices down; rates down, prices up"
print(f"price at 5%: ${p_new:,.2f} (drop ${drop:,.2f}); curve {dict(zip(rates_axis, prices_axis))}")

spec = {
    "id": "046_bonds_friend",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": "Simplified example · yearly interest · not advice",
    "title": "Bonds Explained: Why Prices Fall When Rates Rise",
    "description": (
        "Bonds explained simply: a bond is a loan. Lend a friend $1,000 for 10 years at 4%, and you get $40 of "
        "interest (the coupon) each year and your $1,000 back at the end (maturity). If rates then rise and new "
        f"bonds pay 5%, nobody will pay $1,000 for your $40 a year, so your bond's price falls to about "
        f"${p_new:,.0f}: the price at which a buyer earns 5% a year, counting the ${drop:,.0f} gain at maturity.\n\n"
        "Our own simplified example, all numbers computed: interest paid once a year (many bonds pay twice a "
        "year), 10 years left when rates move, no fees or taxes. Holding to maturity gets you the $1,000 back only "
        "if the borrower doesn't default; selling early locks in today's price. The longer the time left, the more "
        "a bond's price moves when rates change. Not financial advice.\n\n"
        "#bonds #investing #interestrates #personalfinance #stockmarket"
    ),
    "tags": ["bonds explained", "how bonds work", "why bond prices fall when rates rise", "bond coupon",
             "bond maturity", "interest rates and bonds", "investing for beginners", "fixed income",
             "how the market works"],
    "localizations": {
        "es": {"title": "Bonos explicados: por qué bajan cuando suben las tasas",
               "summary": f"Un bono es un préstamo: prestas $1.000 a 10 años al 4% y cobras $40 al año. Si los bonos nuevos "
                          f"pagan 5%, el precio del tuyo baja a unos ${p_new:,.0f}."},
        "pt": {"title": "Títulos explicados: por que caem quando os juros sobem",
               "summary": f"Um título é um empréstimo: você empresta US$1.000 por 10 anos a 4% e recebe US$40 por ano. Se os "
                          f"novos pagam 5%, o preço do seu cai para cerca de US${p_new:,.0f}."},
        "hi": {"title": "बॉन्ड आसान भाषा में: ब्याज दर बढ़े तो दाम क्यों गिरते हैं",
               "summary": f"बॉन्ड एक कर्ज़ है: $1,000 दस साल के लिए 4% पर दें, हर साल $40 मिलते हैं। नए बॉन्ड 5% दें तो "
                          f"आपके बॉन्ड का दाम लगभग ${p_new:,.0f} रह जाता है।"},
        "id": {"title": "Obligasi Dijelaskan: Kenapa Harga Turun Saat Bunga Naik",
               "summary": f"Obligasi adalah pinjaman: pinjamkan $1.000 selama 10 tahun dengan bunga 4%, dapat $40 per tahun. "
                          f"Jika obligasi baru memberi 5%, harga obligasimu turun ke sekitar ${p_new:,.0f}."},
        "de": {"title": "Anleihen erklärt: Warum Kurse fallen, wenn Zinsen steigen",
               "summary": f"Eine Anleihe ist ein Kredit: 1.000 $ für 10 Jahre zu 4 %, also 40 $ Zinsen im Jahr. Zahlen neue "
                          f"Anleihen 5 %, fällt der Kurs deiner auf rund {p_new:,.0f} $."},
        "fr": {"title": "Les obligations expliquées : pourquoi leur prix baisse",
               "summary": f"Une obligation est un prêt : 1 000 $ sur 10 ans à 4 %, soit 40 $ d'intérêts par an. Si les "
                          f"nouvelles paient 5 %, le prix de la vôtre tombe à environ {p_new:,.0f} $."},
    },
    "thumbnail": {"photo": {"file": "assets/photos/us_treasury_building.jpg", "focus": [0.45, 0.45]}},
    "scenes": [
        # hook: payoff number on frame 0 + contradiction ("nobody missed a payment") + open loop ("why?")
        {"say": "Your bond lost seventy-seven dollars, and nobody missed a payment. Why?",
         "visual": {"type": "stat", "value": f"−${drop:,.0f}", "label": "your bond's price, after rates rose",
                    "sub": "simplified example · $1,000 bond", "color": "red"}},
        {"say": "A bond is a loan: lend a friend a thousand for ten years.",
         "visual": {"type": "pair", "title": "A bond is a loan",
                    "left": {"label": "You", "sub": "lend $1,000", "color": "green"},
                    "right": {"label": "Friend", "sub": "borrows for 10 yrs", "color": "blue"}}},
        {"say": "He pays forty dollars a year: the coupon, four percent.",
         "visual": {"type": "photo", "file": "assets/photos/dollar_bills_100s.jpg",
                    "title": f"The coupon: ${FACE:,} × {COUPON_RATE:.0%}",
                    "value": f"${coupon:.0f}/yr", "color": "gold", "label": "the coupon, every year", "focus": [0.5, 0.4]}},
        {"say": "In year ten, he repays the thousand. That's maturity.",
         "visual": {"type": "compare", "title": "Over 10 years", "format": "usd",
                    "left": {"label": "Coupons", "value": coupon * YEARS, "color": "gold"},
                    "right": {"label": "At maturity", "value": FACE, "color": "green"}}},
        # mid-video re-hook: second loop
        {"say": "The twist: rates rise. New bonds pay five percent.",
         "visual": {"type": "photo", "file": "assets/photos/us_treasury_building.jpg",
                    "title": "The twist: rates rise",
                    "value": f"{NEW_RATE:.0%}", "color": "red", "label": "what new bonds pay",
                    "focus": [0.5, 0.45]}},
        {"say": "Who pays a thousand for your forty, when new bonds pay fifty?",
         "visual": {"type": "bars", "title": "Interest a year, same $1,000", "format": "usd",
                    "items": [{"label": "Your bond", "value": coupon, "color": "slate"},
                              {"label": "New bond", "value": new_coupon, "color": "green"}]}},
        {"say": "So its price drops to about nine hundred twenty-three, where buyers earn five percent.",
         "visual": {"type": "stat", "value": f"${p_new:,.0f}", "label": "your bond's new price",
                    "sub": f"buyer earns {NEW_RATE:.0%}/yr incl. ${drop:,.0f} gain at maturity", "color": "gold"}},
        {"say": "Rates up, prices down. Rates down, prices up.",
         "visual": {"type": "line", "title": "Your 4% bond's price", "x": rates_axis,
                    "x_label": "rate new bonds pay, %", "format": "usd",
                    "hline": {"value": round(p_new), "x": 5, "at": 0.8, "label": f"5% → ${p_new:,.0f}"},
                    "series": [{"label": "", "values": prices_axis, "color": "gold"}]}},
        {"say": "Hold, and if he pays, your thousand returns. Still just four percent.",
         "visual": {"type": "pair", "title": "Your choice",
                    "left": {"label": "Hold", "sub": "$1,000 if repaid", "color": "green"},
                    "right": {"label": "Sell now", "sub": f"≈ ${p_new:,.0f}", "color": "red"}}},
        # loop line: runs back into "Your bond lost seventy-seven dollars..."
        {"say": "Sell early, and that drop is real.",
         "visual": {"type": "cta", "lines": ["Rates up,", "bond prices down."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "046_bonds_friend.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
