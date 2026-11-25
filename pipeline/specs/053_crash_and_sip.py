"""Video 053 (global/USD): what a market crash means for someone investing a fixed amount every month.
Pillar: How Markets Work. The 12-month example is an ILLUSTRATION computed here (not real prices, not a forecast);
the 2007-2013 S&P 500 recovery is a sourced historical fact."""
import json, os

# ---------------------------------------------------------------- sourced facts
# AP / NPR, Mar 28, 2013 ("1,569: S&P 500 Closes At All-Time High, Rising Above Oct. 2007 Mark"): the S&P 500
# closed at 1,569.19, passing its Oct 9, 2007 record close of 1,565.15; it had fallen 57% to a closing low of
# 676.53 on Mar 9, 2009. Price index only (dividends not included).
SP_PEAK_2007, SP_LOW_2009, SP_RECORD_2013 = 1565.15, 676.53, 1569.19
PEAK_Y, PEAK_M = 2007, 10        # Oct 9, 2007
BACK_Y, BACK_M = 2013, 3         # Mar 28, 2013

# ---------------------------------------------------------------- illustration (our own numbers)
MONTHLY = 500
PRICES = [100, 90, 80, 70, 60, 50, 50, 60, 70, 80, 90, 100]     # fund price per unit, month 1..12
months = list(range(1, len(PRICES) + 1))
units, value, put_in = 0.0, [], []
for k, p in enumerate(PRICES):
    units += MONTHLY / p
    value.append(units * p)
    put_in.append(MONTHLY * (k + 1))
mid = 5                                                          # month 6, price at the bottom
mid_loss = 1 - value[mid] / put_in[mid]
end_gain = value[-1] / put_in[-1] - 1
units_at_100 = MONTHLY / PRICES[0]
units_at_50 = MONTHLY / min(PRICES)
avg_cost = put_in[-1] / units                                    # average price paid per unit
fall_0809 = 1 - SP_LOW_2009 / SP_PEAK_2007
recovery_years = (BACK_Y + (BACK_M - 1) / 12) - (PEAK_Y + (PEAK_M - 1) / 12)

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert PRICES[0] == PRICES[-1] == 100 and min(PRICES) == 50     # "price falls by half... back to even"
assert units_at_100 == 5 and units_at_50 == 10                   # "five units... ten units"
assert put_in[-1] == 6_000                                       # "six thousand put in"
assert 8_450 < value[-1] < 8_460, value[-1]                      # "about eighty-four hundred fifty"
assert round(end_gain * 100) == 41, end_gain                     # "up forty-one percent"
assert 0.29 < mid_loss < 0.30, mid_loss                          # "down almost thirty percent"
assert 3_000 == put_in[mid] and 2_110 < value[mid] < 2_120       # (shown on chart)
assert 70 < avg_cost < 71, avg_cost                              # (not spoken) average price paid per unit
assert round(fall_0809 * 100) == 57, fall_0809                   # "fell fifty-seven percent"
assert 5.3 <= recovery_years <= 5.6, recovery_years              # "about five and a half years"
print(f"units {units:.2f}; value ${value[-1]:,.0f} on ${put_in[-1]:,} (+{end_gain:.1%}); mid -{mid_loss:.1%}; "
      f"avg cost ${avg_cost:.2f}; 2007-09 fall {fall_0809:.1%}, back in {recovery_years:.1f} yrs")

spec = {
    "id": "053_crash_and_sip",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": "Made-up prices, not a forecast · S&P data: AP · not advice",
    "title": "Stock Market Crash: Why Monthly Investors Get a Sale",
    "description": (
        "What does a stock market crash mean if you invest every month? In our simple illustration, a fund falls "
        "from $100 to $50 and only climbs back to $100. Investing $500 a month buys more units when prices are low, "
        f"so $6,000 put in becomes about ${value[-1]:,.0f}, up {end_gain:.0%}, even though the price ended where it "
        f"started. Halfway through, the same account was down about {mid_loss:.0%}: that is where many people stop.\n\n"
        "This is an illustration with made-up prices, not real data and not a forecast. It only works if prices "
        "recover, which is not guaranteed: a single stock may never recover, and even broad markets can take years. "
        f"Example: the S&P 500 fell {fall_0809:.0%} from its October 2007 record close to its March 2009 low and "
        "only closed above that 2007 record in March 2013 (price index, dividends not included).\n\n"
        "Source: Associated Press / NPR, \"S&P 500 Closes At All-Time High, Rising Above Oct. 2007 Mark\" "
        "(Mar 28, 2013): closes of 1,565.15 (Oct 9, 2007), 676.53 (Mar 9, 2009) and 1,569.19 (Mar 28, 2013).\n\n"
        "Assumptions: $500 invested at the start of each month at that month's price, no fees or taxes. "
        "Past results don't guarantee future returns; prices can fall further and for longer. Not financial advice.\n\n"
        "#stockmarket #investing #marketcrash #personalfinance #dollarcostaveraging"
    ),
    "tags": ["stock market crash", "what to do in a market crash", "investing every month", "dollar cost averaging",
             "SIP in market crash", "monthly investing", "bear market", "how the stock market works",
             "investing for beginners"],
    "localizations": {
        "es": {"title": "Caída de la bolsa: por qué el inversor mensual compra barato",
               "summary": f"Ejemplo ilustrativo: un fondo cae de $100 a $50 y vuelve a $100. Con $500 al mes, $6.000 se "
                          f"convierten en unos ${value[-1]:,.0f} (+{end_gain:.0%}). A mitad de camino, la cuenta iba {mid_loss:.0%} abajo."},
        "pt": {"title": "Queda da bolsa: por que o investidor mensal ganha desconto",
               "summary": f"Exemplo ilustrativo: um fundo cai de US$100 para US$50 e volta a US$100. Com US$500 por mês, "
                          f"US$6.000 viram cerca de US${value[-1]:,.0f} (+{end_gain:.0%}). No meio do caminho, a conta caía {mid_loss:.0%}."},
        "hi": {"title": "शेयर बाज़ार क्रैश: हर महीने निवेश करने वालों के लिए सेल",
               "summary": f"उदाहरण: एक फंड $100 से $50 तक गिरकर फिर $100 पर लौटता है। हर महीने $500 लगाने पर $6,000 बन जाते हैं "
                          f"लगभग ${value[-1]:,.0f} (+{end_gain:.0%})। बीच में खाता {mid_loss:.0%} नीचे था।"},
        "id": {"title": "Pasar Saham Anjlok: Kenapa Investor Bulanan Dapat Diskon",
               "summary": f"Ilustrasi: harga reksa dana turun dari $100 ke $50 lalu kembali ke $100. Dengan $500 per bulan, "
                          f"$6.000 menjadi sekitar ${value[-1]:,.0f} (+{end_gain:.0%}). Di tengah jalan, akun sempat turun {mid_loss:.0%}."},
        "de": {"title": "Börsencrash: Warum Sparplan-Anleger Rabatt bekommen",
               "summary": f"Beispiel: Ein Fonds fällt von 100 $ auf 50 $ und steigt zurück auf 100 $. Mit 500 $ im Monat werden "
                          f"aus 6.000 $ rund {value[-1]:,.0f} $ (+{end_gain:.0%}). Zwischendurch lag das Depot {mid_loss:.0%} im Minus."},
        "fr": {"title": "Krach boursier : l'investisseur mensuel achète en soldes",
               "summary": f"Exemple : un fonds passe de 100 $ à 50 $ puis revient à 100 $. Avec 500 $ par mois, 6 000 $ "
                          f"deviennent environ {value[-1]:,.0f} $ (+{end_gain:.0%}). À mi-parcours, le compte perdait {mid_loss:.0%}."},
    },
    "thumbnail": {"photo": {"file": "assets/photos/stock_screens_tokyo_chart.jpg", "focus": [0.3, 0.45]}},
    "scenes": [
        # hook: payoff number on frame 0 + contradiction ("price back to even, yet up 41%")
        {"say": "Price back to even, yet this monthly investor is up forty-one percent.",
         "visual": {"type": "stat", "value": f"+{end_gain:.0%}", "label": "monthly investor, price back to even",
                    "sub": "illustration · made-up prices", "color": "green"}},
        {"say": "Say a fund drops from one hundred dollars to fifty, then climbs back.",
         "visual": {"type": "line", "title": "Fund price (illustration)", "x": months, "x_label": "month",
                    "format": "usd", "series": [{"label": "Price", "values": PRICES, "color": "gold"}]}},
        {"say": "Invest five hundred a month: five units at one hundred, ten at fifty.",
         "visual": {"type": "bars", "title": f"Units ${MONTHLY} a month buys", "format": "num",
                    "items": [{"label": "At $100", "value": units_at_100, "color": "slate"},
                              {"label": "At $50", "value": units_at_50, "color": "green"}]}},
        {"say": "So a crash is a sale. But here's the catch.",
         "visual": {"type": "photo", "file": "assets/photos/stock_screens_tokyo_chart.jpg",
                    "title": "A crash means",
                    "value": f"{units_at_50 // units_at_100:.0f}× units", "color": "green",
                    "label": "price cut in half: twice as many units", "focus": [0.4, 0.4]}},
        # mid-video re-hook: the painful middle
        {"say": "Halfway, you're down almost thirty percent. Many people quit here.",
         "visual": {"type": "compare", "title": "Month 6, at the bottom", "format": "usd",
                    "left": {"label": "Put in", "value": put_in[mid], "color": "slate"},
                    "right": {"label": "Worth", "value": round(value[mid]), "color": "red"}}},
        {"say": "Keep going, and six thousand becomes about eighty-four hundred fifty.",
         "visual": {"type": "line", "title": "Worth vs money put in", "x": months, "x_label": "month", "format": "usd",
                    "series": [{"label": "Worth", "values": [round(v) for v in value], "color": "green"},
                               {"label": "", "values": put_in, "color": "slate"}]}},
        {"say": "Real crashes run deep: the S and P five hundred once fell fifty-seven percent.",
         "visual": {"type": "photo", "file": "assets/photos/lehman_brothers_hq_2008.jpg",
                    "title": "Real crash: 2007–2009",
                    "value": f"−{fall_0809:.0%}", "color": "red", "label": "S&P 500, Oct 2007 → Mar 2009",
                    "focus": [0.5, 0.4]}},
        {"say": "Its record took about five and a half years to return.",
         "visual": {"type": "equation", "title": "Real history: slow recovery",
                    "lines": [{"text": "Oct 2007 → Mar 2013", "color": "text", "size": 84},
                              {"text": "≈ 5.5 years", "color": "gold", "size": 130}]}},
        # lesson + loop line: runs back into "Price back to even, yet..."
        {"say": "Here, buying through the drop made even a round trip pay.",
         "visual": {"type": "cta", "lines": ["$100 → $50 → $100", f"+{end_gain:.0%}"],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "053_crash_and_sip.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
