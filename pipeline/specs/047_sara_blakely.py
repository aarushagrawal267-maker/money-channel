"""Video 047 (global/US): Sara Blakely, from $5,000 in savings to Spanx. Pillar: Founder story."""
import json, os

# ---------------------------------------------------------------- sourced facts
# CNN Business (Rob McLean, Jill Disis, Oct 21, 2021, "Spanx is now worth $1.2 billion"): Blakely "started the
# company in 2000 with $5,000 in savings"; Forbes named her "the youngest self-made female billionaire in 2012".
# Fortune (Sept 20, 2025): she started Spanx with "five grand from selling fax machines"; founded 2000, aged 29.
SAVINGS = 5_000
FOUNDED, FOUNDED_AGE = 2000, 29
# CNBC (Apr 3, 2019) and Fortune (Sept 20, 2025): seven years selling fax machines door to door (Fortune: before
# joining office-supply company Danka as a national sales trainer). CNBC: she cut the feet out of pantyhose to
# look better in "fitted white pants".
FAX_YEARS = 7
# Fortune (Sept 20, 2025): found a hosiery mill to make the prototype "after multiple rejections"; Spanx on Oprah's
# Favorite Things in November 2000; sales of $4 million in the first year and $10 million in the second
# (as reported by Fortune; Spanx is private, so these are not audited figures).
SALES_Y1, SALES_Y2 = 4e6, 10e6
# Forbes billionaires list, March 2012 (reported by CNN Business 2021, The Week 2012, Marketplace Mar 14, 2012):
# youngest self-made woman billionaire, aged 41; Spanx "estimated to be worth $1 billion"; Blakely "is the sole
# owner of the company, which has no debt and has never received outside investment" (The Week, citing Forbes).
FORBES_YEAR, FORBES_AGE = 2012, 41
FORBES_VALUE = 1e9
# Reuters via CNBC (Oct 20, 2021): Blackstone to buy a majority stake in Spanx, "valuing the shapewear maker at
# $1.2 billion". CNN Business (Oct 21, 2021): price paid not disclosed; Blakely keeps a "significant" equity stake
# and becomes executive chairwoman.
DEAL_YEAR, DEAL_VALUATION = 2021, 1.2e9
# Fortune (Sept 20, 2025): her net worth fell below $1 billion in 2020 (description only, attributed).

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert SAVINGS == 5000                                        # "five thousand dollars in savings"
assert FORBES_YEAR - FOUNDED == 12                            # "twelve years later"
assert FORBES_AGE - (FORBES_YEAR - FOUNDED) == FOUNDED_AGE      # sources agree: 29 in 2000, 41 in 2012
assert FAX_YEARS == 7                                         # "seven years"
assert (SALES_Y1, SALES_Y2) == (4e6, 10e6)                    # "four million, then ten million"
assert FORBES_VALUE >= 1e9                                    # "a billionaire" (Forbes estimate)
assert round(DEAL_VALUATION / 1e9, 1) == 1.2                  # "one point two billion"
assert DEAL_YEAR - FOUNDED == 21                              # "twenty-one years" self-funded (Fortune) / shown
multiple = DEAL_VALUATION / SAVINGS
assert multiple == 240_000                                    # description: valuation = 240,000x the savings
print(f"$5,000 -> ${DEAL_VALUATION/1e9:.1f}B valuation ({multiple:,.0f}x); founded {FOUNDED}, Forbes {FORBES_YEAR}")

spec = {
    "id": "047_sara_blakely",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "FOUNDER STORY",
    "caption_fix": {"Oh-pruh": "Oprah"},   # Kokoro says "Oprah" as "opera"
    "disclaimer": "Sources: CNN, Reuters, Forbes, Fortune, CNBC · see description",
    "title": "Sara Blakely: $5,000 in Savings to Billion-Dollar Spanx",
    "description": (
        "Sara Blakely started Spanx in 2000 with $5,000 in savings, after seven years selling fax machines door "
        "to door. Hosiery mills turned her down before one agreed to make her footless pantyhose; Oprah featured "
        "Spanx in November 2000. In 2012 Forbes named her the youngest self-made woman billionaire, at 41, while "
        "she still owned 100% of the company with no debt and no outside investors. In 2021 Blackstone bought a "
        "majority stake valuing Spanx at $1.2 billion; Blakely kept a significant stake (the price paid was not "
        "disclosed). Billionaire status depends on estimates: Fortune reports her net worth fell below $1 billion "
        "in 2020. The lesson: test a cheap fix for a problem you actually have before you spend big.\n\n"
        "Sources: CNN Business (Oct 21, 2021); Reuters via CNBC (Oct 20, 2021); Forbes World's Billionaires 2012, "
        "as reported by CNN Business, The Week and Marketplace (Mar 14, 2012); CNBC (Apr 3, 2019); Fortune "
        "(Sept 20, 2025) for the fax-machine years, mill rejections, Oprah and first-year sales ($4M, then $10M; "
        "Spanx is private, so these are company/founder figures). Educational content, not investment advice.\n\n"
        "#spanx #entrepreneur #founderstory #business #startup"
    ),
    "tags": ["sara blakely", "spanx", "spanx story", "sara blakely story", "self made billionaire",
             "bootstrapping", "founder story", "business case study", "blackstone spanx"],
    "localizations": {
        "es": {"title": "Sara Blakely: de 5.000 dólares ahorrados a Spanx",
               "summary": "Sara Blakely fundó Spanx en 2000 con 5.000 dólares de ahorros, tras vender faxes puerta a puerta. En 2021, Blackstone compró la mayoría valorando Spanx en 1.200 millones de dólares. La lección: prueba una solución barata a un problema real."},
        "pt": {"title": "Sara Blakely: de 5 mil dólares de poupança à Spanx",
               "summary": "Sara Blakely fundou a Spanx em 2000 com 5 mil dólares de poupança, depois de vender aparelhos de fax de porta em porta. Em 2021, a Blackstone comprou o controle avaliando a Spanx em 1,2 bilhão de dólares. A lição: teste uma solução barata para um problema real."},
        "hi": {"title": "Sara Blakely: 5,000 डॉलर की बचत से अरब डॉलर की Spanx",
               "summary": "Sara Blakely ने 2000 में 5,000 डॉलर की बचत से Spanx शुरू की, उससे पहले वे घर-घर जाकर फ़ैक्स मशीनें बेचती थीं। 2021 में Blackstone ने बहुमत हिस्सेदारी ली और Spanx का मूल्य 1.2 अरब डॉलर आँका। सीख: अपनी असली समस्या का सस्ता हल पहले आज़माएँ।"},
        "id": {"title": "Sara Blakely: Dari Tabungan $5.000 ke Spanx Bernilai $1 Miliar",
               "summary": "Sara Blakely mendirikan Spanx pada 2000 dengan tabungan 5.000 dolar, setelah menjual mesin faks dari pintu ke pintu. Pada 2021, Blackstone membeli saham mayoritas dengan valuasi 1,2 miliar dolar. Pelajarannya: uji solusi murah untuk masalah nyata."},
        "de": {"title": "Sara Blakely: Mit 5.000 $ Erspartem zur Milliardenfirma",
               "summary": "Sara Blakely gründete Spanx im Jahr 2000 mit 5.000 Dollar Erspartem, nachdem sie Faxgeräte an der Haustür verkauft hatte. 2021 übernahm Blackstone die Mehrheit bei einer Bewertung von 1,2 Milliarden Dollar. Die Lehre: Teste erst eine günstige Lösung für ein echtes Problem."},
        "fr": {"title": "Sara Blakely : de 5 000 $ d'économies à Spanx",
               "summary": "Sara Blakely a fondé Spanx en 2000 avec 5 000 dollars d'économies, après avoir vendu des fax en porte-à-porte. En 2021, Blackstone a pris la majorité en valorisant Spanx à 1,2 milliard de dollars. La leçon : tester une solution bon marché à un vrai problème."},
    },
    "thumbnail": {"big": "100%", "line": "No outside investors", "color": "green",
                  "photo": {"file": "assets/photos/sara_blakely_2012.jpg", "focus": [0.5, 0.3], "cutout": True}},
    "scenes": [
        # hook: the big gap on frame 0 + open loop ("how?")
        {"say": "Five thousand dollars in savings. Twelve years later, Forbes said: billionaire. How?",
         "visual": {"type": "compare", "title": "Sara Blakely",
                    "left": {"label": f"Savings, {FOUNDED}", "value": SAVINGS, "color": "slate"},
                    "right": {"label": f"Forbes est., {FORBES_YEAR}", "value": FORBES_VALUE, "color": "green"}}},
        {"say": "She'd sold fax machines door to door for seven years.",
         "visual": {"type": "photo", "file": "assets/photos/fax_machine_generic.jpg", "focus": [0.5, 0.45],
                    "value": f"{FAX_YEARS} years", "label": "selling fax machines door to door", "color": "gold"}},
        {"say": "Her idea: pantyhose with the feet cut off.",
         "visual": {"type": "equation", "title": "The idea",
                    "lines": [{"text": "Pantyhose", "color": "text", "size": 110},
                              {"text": "− the feet", "color": "muted", "size": 90},
                              {"text": "= Spanx", "color": "gold", "size": 120}]}},
        {"say": "Mills said no. Then one agreed.",
         "visual": {"type": "pair", "title": "Finding a maker",
                    "left": {"label": "Mills", "sub": "several said no", "color": "red"},
                    "right": {"label": "One mill", "sub": "said yes", "color": "green"}}},
        {"say": "Oh-pruh featured it in two thousand. Sales: four million, then ten million.",
         "visual": {"type": "bars", "title": "Spanx sales (per Fortune)", "format": "usd",
                    "items": [{"label": "Year 1", "value": SALES_Y1, "color": "slate"},
                              {"label": "Year 2", "value": SALES_Y2, "color": "green"}]}},
        {"say": "By twenty twelve, Forbes called her a billionaire.",
         "visual": {"type": "photo", "file": "assets/photos/sara_blakely_2012.jpg", "focus": [0.5, 0.3],
                    "title": f"${FORBES_VALUE / 1e9:.0f}B · Forbes, {FORBES_YEAR} · age {FORBES_AGE}",
                    "label": "youngest self-made woman billionaire"}},
        # mid-video re-hook: opens a second loop (no investors... so what happened next?)
        {"say": "Now the twist: she'd never taken a single outside investor.",
         "visual": {"type": "equation", "title": "The twist (Forbes, 2012)",
                    "lines": [{"text": "100% owned", "color": "gold", "size": 100},
                              {"text": "$0 debt", "color": "text", "size": 90},
                              {"text": "0 outside investors", "color": "text", "size": 80}]}},
        {"say": "In twenty twenty-one, Blackstone bought control, valuing Spanx at one point two billion.",
         "visual": {"type": "photo", "file": "assets/photos/spanx_store.jpg", "focus": [0.55, 0.4],
                    "value": f"${DEAL_VALUATION / 1e9:.1f}B", "label": f"Blackstone majority deal, {DEAL_YEAR}", "color": "gold"}},
        {"say": "The lesson: test a cheap fix for a problem you actually have.",
         "visual": {"type": "pair", "title": "The lesson",
                    "left": {"label": "Problem", "sub": "one you really have", "color": "slate"},
                    "right": {"label": "Cheap test", "sub": "before big spending", "color": "green"}}},
        # loop line: runs back into "Five thousand dollars in savings..."
        {"say": "And it all started with...",
         "visual": {"type": "cta", "lines": ["Your problem.", "Your fix."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "047_sara_blakely.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
