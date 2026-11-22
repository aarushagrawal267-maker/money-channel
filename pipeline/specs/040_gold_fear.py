"""Video 040 (global/US): why gold tends to rise when the world is scared. Pillar: How Markets Work."""
import json, os

# ---------------------------------------------------------------- sourced facts
# World Gold Council, Gold Demand Trends Q3 2026 (published Nov 3, 2026), supply/demand table, LBMA (PM) gold
# price, quarterly average, US$/oz: Q3'25 3,456.5 · Q4'25 4,135.2 · Q1'26 4,872.9 · Q2'26 4,506.3 · Q3'26 4,262.2.
# Central bank and other institutions, tonnes: Q3'25 226.3 · Q3'26 321.2 ("up 42% year-on-year").
# Press release (Nov 3, 2026): ETFs added 211t in Q3, holdings "rose to a record 4,256t"; Louise Street (WGC):
# "geopolitical risk and concerns around fiscal discipline driving institutional interest" ... "rising interest
# rates and mixed inflation expectations present potential headwinds" ... "the combined shadows of geopolitical
# risk and financial market stress may cause participants to seek stability in gold."
PRICE = {"Q3 2025": 3456.5, "Q4 2025": 4135.2, "Q1 2026": 4872.9, "Q2 2026": 4506.3, "Q3 2026": 4262.2}
CB_Q3_25, CB_Q3_26 = 226.3, 321.2
ETF_INFLOW_Q3_26 = 211

# ---------------------------------------------------------------- checks behind spoken / shown claims
yoy = PRICE["Q3 2026"] / PRICE["Q3 2025"] - 1
assert round(yoy * 100) == 23, yoy                              # "about twenty-three percent higher"
assert round(PRICE["Q3 2026"]) == 4262                          # "four thousand two hundred sixty-two dollars"
drop = 1 - PRICE["Q3 2026"] / PRICE["Q1 2026"]
assert round(drop * 100) == 13, drop                            # "about thirteen percent lower than in Q1"
cb_growth = CB_Q3_26 / CB_Q3_25 - 1
assert round(cb_growth * 100) == 42, cb_growth                  # "forty-two percent more"
assert round(CB_Q3_26) == 321                                   # "three hundred and twenty-one tonnes"
print(f"gold +{yoy:.1%} y/y, -{drop:.1%} vs Q1 2026 avg; central banks +{cb_growth:.0%}")

spec = {
    "id": "040_gold_fear",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "HOW MARKETS WORK",
    "disclaimer": "Past prices don't predict future ones · not financial advice",
    "title": "Why Gold Rises When the World Is Scared (It Pays $0)",
    "description": (
        "Why does gold often rise in a crisis, even though it pays no interest? It is nobody's debt, so it can't "
        "default, and many investors and central banks treat it as a safe haven. Central banks bought a net 321 tonnes "
        f"in Q3 2026, up {cb_growth:.0%} from a year earlier, and gold averaged ${PRICE['Q3 2026']:,.0f} an ounce, about "
        f"{yoy:.0%} higher than a year earlier, but about {drop:.0%} below its Q1 2026 average. Real interest rates "
        "(rates after inflation) matter too: gold pays nothing, so higher real rates make it less attractive.\n\n"
        "Source: World Gold Council, Gold Demand Trends Q3 2026 and press release (Nov 3, 2026); prices are quarterly "
        "averages of the LBMA (PM) gold price. Past prices don't predict future ones. This is education, not a "
        "recommendation to buy or sell gold. Not financial advice.\n\n"
        "#gold #investing #economy #centralbanks #personalfinance"
    ),
    "tags": ["why gold prices rise", "gold safe haven", "gold price explained", "central bank gold buying",
             "real interest rates", "world gold council", "how markets work"],
    "localizations": {
        "es": {"title": "Por qué el oro sube cuando el mundo tiene miedo",
               "summary": "El oro no paga intereses, pero no es deuda de nadie, así que muchos lo ven como refugio. "
                          "Los bancos centrales compraron 321 toneladas en el 3T 2026, un 42% más que un año antes."},
        "pt": {"title": "Por que o ouro sobe quando o mundo tem medo",
               "summary": "O ouro não paga juros, mas não é dívida de ninguém, por isso muitos o veem como porto seguro. "
                          "Bancos centrais compraram 321 toneladas no 3º tri de 2026, 42% a mais que um ano antes."},
        "hi": {"title": "दुनिया डरती है तो सोना क्यों चढ़ता है?",
               "summary": "सोना ब्याज नहीं देता, पर यह किसी का कर्ज़ नहीं, इसलिए लोग इसे सुरक्षित मानते हैं। "
                          "Q3 2026 में केंद्रीय बैंकों ने 321 टन सोना खरीदा, एक साल पहले से 42% ज़्यादा।"},
        "id": {"title": "Kenapa Emas Naik Saat Dunia Ketakutan",
               "summary": "Emas tidak memberi bunga, tetapi bukan utang siapa pun, jadi banyak yang menganggapnya aman. "
                          "Bank sentral membeli 321 ton pada Q3 2026, naik 42% dari setahun sebelumnya."},
        "de": {"title": "Warum Gold steigt, wenn die Welt Angst hat",
               "summary": "Gold bringt keine Zinsen, ist aber niemandes Schuld, deshalb gilt es als sicherer Hafen. "
                          "Zentralbanken kauften im 3. Quartal 2026 netto 321 Tonnen, 42 % mehr als ein Jahr zuvor."},
        "fr": {"title": "Pourquoi l'or monte quand le monde a peur",
               "summary": "L'or ne rapporte pas d'intérêts, mais ce n'est la dette de personne : beaucoup y voient une valeur "
                          "refuge. Les banques centrales en ont acheté 321 tonnes au T3 2026, 42 % de plus qu'un an plus tôt."},
    },
    "scenes": [
        {"say": "When the world gets scared, money often runs to a metal that pays no interest at all. Gold.",
         "visual": {"type": "stat", "value": f"${PRICE['Q3 2026']:,.0f}", "label": "average gold price per ounce",
                    "sub": f"Q3 2026 · up {yoy:.0%} in a year · World Gold Council", "color": "gold"}},
        {"say": "Why gold? It isn't anyone's debt, so it can't default. No government can print more of it. So in wars, crises and crashes, many treat it as a safe haven.",
         "visual": {"type": "equation", "title": "Why gold feels safe",
                    "lines": [{"text": "Nobody's debt", "color": "gold", "size": 96},
                              {"text": "Can't default", "color": "text", "size": 88},
                              {"text": "Can't be printed", "color": "muted", "size": 80}]}},
        {"say": "Central banks buy it too. In the third quarter of twenty twenty-six, they added a net three hundred and twenty-one tonnes, forty-two percent more than a year earlier.",
         "visual": {"type": "bars", "title": "Central bank buying (tonnes)", "format": "num",
                    "items": [{"label": "Q3 2025", "value": round(CB_Q3_25), "color": "slate"},
                              {"label": "Q3 2026", "value": round(CB_Q3_26), "color": "gold"}]}},
        {"say": "Then there are real interest rates: what savings pay after inflation. Gold pays nothing, so when real rates fall, holding it costs less. When they rise, gold often struggles.",
         "visual": {"type": "pair", "title": "Real interest rates",
                    "left": {"label": "Lower", "sub": "gold looks better", "color": "green"},
                    "right": {"label": "Higher", "sub": "gold often lags", "color": "red"}}},
        {"say": "But safe doesn't mean steady. From July to September, gold averaged about thirteen percent less than from January to March.",
         "visual": {"type": "compare", "title": "Average gold price, 2026",
                    "left": {"label": "Q1 2026", "value": PRICE["Q1 2026"], "color": "gold"},
                    "right": {"label": "Q3 2026", "value": PRICE["Q3 2026"], "color": "red"}}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Safe haven.", "Not risk-free."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "040_gold_fear.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
