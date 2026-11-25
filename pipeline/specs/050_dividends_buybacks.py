"""Video 050 (global/USD): dividends vs buybacks, the two ways companies hand cash back. Pillar: How Markets Work.
Real-world totals are sourced (S&P Dow Jones Indices); the $10,000 company is a simplified example computed here."""
import json, os

# ---------------------------------------------------------------- sourced facts
# S&P Dow Jones Indices press release, "S&P 500 Q3 2025 Buybacks Post Modest 6.2% Gain to $249.0 Billion ..."
# (Dec 18, 2025; via PR Newswire, read 2026-11-25): "The 12-month September 2025 expenditure was a record $1.020
# trillion"; "For the 12-month September 2025 period, dividends set a record $664.9 billion payment"; "Total
# shareholder returns for the 12-month September 2025 period increased 9.8% to a record $1.685 trillion".
# (This is the latest S&P DJI buyback release we could confirm; the Q4 2025 / later releases did not surface.)
BUYBACKS_12M = 1_020e9
DIVIDENDS_12M = 664.9e9
TOTAL_RETURN_12M = 1_685e9
# Same release: buybacks are subject to a 1% US excise tax on net buybacks (in force since 2023).

# ---------------------------------------------------------------- simplified example (computed)
# A company worth $10,000 (including $100 of spare cash) with 100 shares. You own 1 share. It returns the $100.
# Assumes the market values the company at exactly its worth (no price noise), no taxes, no fees.
COMPANY_VALUE, SHARES, CASH_OUT = 10_000, 100, 100
price0 = COMPANY_VALUE / SHARES
# Dividend: $1 per share paid out; company now worth $9,900 over 100 shares.
div_per_share = CASH_OUT / SHARES
price_after_div = (COMPANY_VALUE - CASH_OUT) / SHARES
you_div = price_after_div + div_per_share
# Buyback: company buys shares at $100 each with the $100; company worth $9,900 over 99 shares.
bought = CASH_OUT / price0
shares_after = SHARES - bought
price_after_bb = (COMPANY_VALUE - CASH_OUT) / shares_after
you_bb = price_after_bb

assert price0 == 100 and div_per_share == 1 and price_after_div == 99     # "one dollar", "drops to ninety-nine"
assert you_div == 100                                                        # $99 share + $1 cash
assert bought == 1 and shares_after == 99                                    # "buys one share", "ninety-nine shares"
assert COMPANY_VALUE - CASH_OUT == 9_900 and price_after_bb == 100           # "still one hundred each"
assert you_div == you_bb                                                     # "same value either way" (day one)
assert abs(BUYBACKS_12M + DIVIDENDS_12M - TOTAL_RETURN_12M) < 1e9            # release totals add up
assert BUYBACKS_12M > 1e12                                                   # "over a trillion dollars"
assert round(DIVIDENDS_12M / 1e9) == 665                                     # "six hundred sixty-five billion"
print(f"dividend: ${price_after_div:.0f} + ${div_per_share:.0f}; buyback: {shares_after:.0f} shares @ ${price_after_bb:.0f}")

spec = {
    "id": "050_dividends_buybacks",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": "Simplified example · not investment advice",
    "title": "Dividends vs Buybacks: Which Pays You More?",
    "description": (
        "Dividends vs buybacks: how do companies return money to shareholders? A dividend pays you cash; a buyback "
        "uses the cash to buy back shares, so each remaining share owns a bigger slice. In the 12 months to September "
        "2025, S&P 500 companies spent a record $1.02 trillion on buybacks and $664.9 billion on dividends. On day "
        "one both give you the same value; the differences are taxes, timing and the price the company pays.\n\n"
        "Source: S&P Dow Jones Indices, S&P 500 buybacks and dividends, Q3 2025 release (Dec 18, 2025; 12 months to "
        "September 2025, the latest release we could confirm).\n\n"
        "Our simplified example: a company worth $10,000 (including $100 of spare cash) with 100 shares at $100. "
        "Dividend: $1 per share is paid and, in theory, the share price falls to $99 ($99 + $1 = $100). Buyback: the "
        "company buys 1 share for $100; the $9,900 company now has 99 shares, still $100 each. Real prices move for "
        "many other reasons. Tax: in a taxable account, dividends are usually taxed in the year you receive them, "
        "while gains from a higher share price are usually taxed only when you sell; rules vary by country and "
        "account type. US companies also pay a 1% excise tax on net buybacks. A buyback only helps remaining owners "
        "if the company doesn't overpay. Educational only, not investment advice.\n\n"
        "#investing #dividends #stockmarket #buybacks #personalfinance"
    ),
    "tags": ["dividends vs buybacks", "stock buybacks explained", "share buyback", "how dividends work",
             "what is a stock buyback", "S&P 500 buybacks", "how markets work", "investing basics"],
    "localizations": {
        "es": {"title": "Dividendos vs recompras: ¿cuál te paga más?",
               "summary": "En 12 meses hasta septiembre de 2025, las empresas del S&P 500 gastaron 1,02 billones de dólares en "
                          "recompras y 664.900 millones en dividendos. El primer día valen lo mismo; cambian impuestos y precio."},
        "pt": {"title": "Dividendos vs recompras: qual paga mais?",
               "summary": "Em 12 meses até setembro de 2025, as empresas do S&P 500 gastaram US$1,02 trilhão em recompras e "
                          "US$664,9 bilhões em dividendos. No primeiro dia valem o mesmo; mudam impostos e preço."},
        "hi": {"title": "डिविडेंड बनाम बायबैक: किससे ज़्यादा फ़ायदा?",
               "summary": "सितंबर 2025 तक 12 महीनों में S&P 500 कंपनियों ने बायबैक पर $1.02 ट्रिलियन और डिविडेंड पर $664.9 अरब "
                          "खर्च किए। पहले दिन दोनों की कीमत बराबर; फ़र्क टैक्स और कीमत का है।"},
        "id": {"title": "Dividen vs Buyback: Mana yang Lebih Untung?",
               "summary": "Dalam 12 bulan hingga September 2025, perusahaan S&P 500 menghabiskan $1,02 triliun untuk buyback dan "
                          "$664,9 miliar untuk dividen. Di hari pertama nilainya sama; bedanya pajak dan harga."},
        "de": {"title": "Dividende vs. Aktienrückkauf: Was bringt mehr?",
               "summary": "In den 12 Monaten bis September 2025 gaben S&P-500-Firmen 1,02 Billionen Dollar für Rückkäufe und "
                          "664,9 Mrd. Dollar für Dividenden aus. Am ersten Tag gleich viel wert; Steuern und Preis machen den Unterschied."},
        "fr": {"title": "Dividendes ou rachats d'actions : lequel rapporte plus ?",
               "summary": "Sur 12 mois jusqu'à septembre 2025, les sociétés du S&P 500 ont consacré 1 020 milliards de dollars aux "
                          "rachats et 664,9 milliards aux dividendes. Même valeur au départ ; la fiscalité et le prix changent tout."},
    },
    "thumbnail": {"photo": {"file": "assets/photos/nyse_facade_wall_street.jpg", "focus": [0.5, 0.4]},
                  "big": f"${BUYBACKS_12M / 1e12:.2f}T", "color": "gold"},
    "scenes": [
        # hook: the biggest number on frame 0 + open loop ("Why?")
        {"say": "Over a trillion dollars, spent by companies on their own shares. Why?",
         "visual": {"type": "photo", "file": "assets/photos/nyse_facade_wall_street.jpg",
                    "title": "S&P 500 · 12 months to Sept 2025",
                    "value": f"${BUYBACKS_12M / 1e12:.2f}T", "color": "gold", "label": "spent on buybacks in one year",
                    "focus": [0.5, 0.45]}},
        {"say": "They paid six hundred sixty-five billion in dividends too.",
         "visual": {"type": "bars", "title": "S&P 500, 12 months to Sept 2025 ($B)", "format": "num",
                    "items": [{"label": "Buybacks", "value": BUYBACKS_12M / 1e9, "color": "gold"},
                              {"label": "Dividends", "value": DIVIDENDS_12M / 1e9, "color": "green"}]}},
        {"say": "Ten thousand dollar company, one hundred shares, a hundred dollars to give back.",
         "visual": {"type": "equation", "title": "Simple example",
                    "lines": [{"text": f"${COMPANY_VALUE:,} company", "color": "text", "size": 92},
                              {"text": f"{SHARES} shares × ${price0:.0f}", "color": "muted", "size": 76},
                              {"text": f"${CASH_OUT} to give back", "color": "gold", "size": 92}]}},
        {"say": "Dividend: you get one dollar, and in theory your share drops to ninety-nine.",
         "visual": {"type": "compare", "title": "Dividend: your 1 share",
                    "left": {"label": "Share price", "value": price_after_div, "color": "blue"},
                    "right": {"label": "Cash to you", "value": div_per_share, "color": "green"}}},
        {"say": "Buyback: it buys one share back. Ninety-nine shares, still one hundred each.",
         "visual": {"type": "equation", "title": "Buyback: your 1 share",
                    "lines": [{"text": f"${COMPANY_VALUE - CASH_OUT:,} ÷ {shares_after:.0f} shares", "color": "text", "size": 88},
                              {"text": f"= ${price_after_bb:.0f} each", "color": "gold", "size": 110},
                              {"text": "you own a bigger slice", "color": "muted", "size": 56}]}},
        # mid-video re-hook: opens a second loop (if they're equal, what's the catch?)
        {"say": "Same value either way. But here's the catch.",
         "visual": {"type": "pair", "title": f"Day one: both = ${you_div:.0f}",
                    "left": {"label": "Dividend", "sub": "$99 share + $1", "color": "green"},
                    "right": {"label": "Buyback", "sub": "$100 share", "color": "gold"}}},
        {"say": "Dividends are usually taxed when paid. Buyback gains, only when you sell.",
         "visual": {"type": "equation", "title": "Taxes (taxable accounts)",
                    "lines": [{"text": "Dividend:", "color": "green", "size": 80},
                              {"text": "taxed when paid", "color": "text", "size": 80},
                              {"text": "Buyback gain:", "color": "gold", "size": 80},
                              {"text": "taxed when you sell", "color": "text", "size": 80}]}},
        {"say": "And a buyback only helps if the company pays a fair price.",
         "visual": {"type": "photo", "file": "assets/photos/wall_street_sign.jpg",
                    "title": "Price matters",
                    "label": "Fair price: owners gain · overpay: they lose", "focus": [0.4, 0.4]}},
        # loop line: runs back into "Over a trillion dollars, spent by companies on their own shares."
        {"say": "Remember that the next time you hear...",
         "visual": {"type": "cta", "lines": ["Same value.", "Different taxes."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "050_dividends_buybacks.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
