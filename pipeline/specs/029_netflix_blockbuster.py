"""Video 029 (global/US): Netflix vs Blockbuster, the $50M deal Blockbuster turned down. Pillar: Case Studies."""
import json, os

# ---------------------------------------------------------------- sourced facts
# The 2000 offer. Both co-founders describe it in their books: Marc Randolph, "That Will Never Work" (2019),
# and Reed Hastings & Erin Meyer, "No Rules Rules" (2020). Newsweek fact check (updated Feb 2, 2022) rates
# "Blockbuster declined to purchase Netflix for $50 million in 2000" as True, and notes that former
# Blockbuster CEO John Antioco "asserted that there were never any serious acquisition talks". DISPUTED
# DETAIL, so the script attributes it ("the founders say") and gives his side.
OFFER_YEAR = 2000
OFFER_PRICE = 50e6
# Netflix Form S-1 (SEC EDGAR, filed Mar 6, 2002), statements of operations, year 2000 (in $ thousands):
# total revenues 35,894; net loss (57,363).
NFLX_REV_2000 = 35.894e6
NFLX_LOSS_2000 = 57.363e6
# Associated Press (Anderson & Liedtke, Sept 23, 2010, via NBC News): Blockbuster filed for bankruptcy on
# Thursday Sept 23, 2010; the chain's store count "peaked at 9,100 in 2004".
BB_PEAK_STORES, BB_PEAK_YEAR = 9100, 2004
BB_BANKRUPT_YEAR = 2010
# Netflix Q4 2025 shareholder letter (Jan 20, 2026): FY2025 revenues $45,183,036 thousand;
# "With over 325M paid memberships" (description only).
NFLX_REV_2025 = 45.183036e9
NFLX_PAID_MEMBERSHIPS = 325e6

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert round(NFLX_REV_2000 / 1e6) == 36          # "about thirty-six million dollars"
assert round(NFLX_LOSS_2000 / 1e6) == 57         # "lost fifty-seven million"
assert BB_BANKRUPT_YEAR - OFFER_YEAR == 10       # "ten years later" (description)
assert int(NFLX_REV_2025 / 1e9) == 45            # "forty-five billion dollars"
ratio = NFLX_REV_2025 / OFFER_PRICE
assert 880 < ratio < 920, ratio                  # "about nine hundred times that asking price"
print(f"Netflix 2025 revenue / asking price = {ratio:.0f}x")

spec = {
    "id": "029_netflix_blockbuster",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "CASE STUDY",
    "disclaimer": "Sources: Netflix filings, AP, Newsweek · see description",
    "title": "Why Blockbuster Didn't Buy Netflix for $50 Million",
    "description": (
        "In 2000, Netflix's co-founders say they offered to sell the company to Blockbuster for $50 million, "
        "and Blockbuster said no (Blockbuster's former CEO later said there were never serious talks). "
        "Blockbuster peaked at about 9,100 stores in 2004 and filed for bankruptcy in September 2010. Netflix "
        f"moved from DVDs by mail to streaming, and in 2025 brought in $45.2 billion, about {ratio:.0f} times "
        "that asking price, with over 325 million paid memberships. The lesson: protect the future, not just "
        "this year's profits.\n\n"
        "Sources: Marc Randolph, 'That Will Never Work' (2019); Reed Hastings & Erin Meyer, 'No Rules Rules' "
        "(2020); Newsweek fact check (updated Feb 2, 2022); Netflix Form S-1 (SEC, Mar 6, 2002), 2000 revenue "
        "$35.9M and net loss $57.4M; Associated Press (Sept 23, 2010) on Blockbuster's bankruptcy and 2004 "
        "store peak; Netflix Q4 2025 shareholder letter (Jan 20, 2026). Educational content, not investment "
        "advice.\n\n"
        "#netflix #blockbuster #business #casestudy #entrepreneurship"
    ),
    "tags": ["netflix", "blockbuster", "netflix vs blockbuster", "netflix blockbuster 50 million",
             "business case study", "business lessons", "disruption", "streaming", "entrepreneurship"],
    "localizations": {
        "es": {"title": "Por qué Blockbuster no compró Netflix por $50 millones",
               "summary": "En 2000, los fundadores de Netflix dicen que ofrecieron venderla a Blockbuster por 50 millones de dólares. Blockbuster dijo que no, quebró en 2010, y Netflix ingresó 45.200 millones de dólares en 2025."},
        "pt": {"title": "Por que a Blockbuster não comprou a Netflix por $50 milhões",
               "summary": "Em 2000, os fundadores da Netflix dizem que ofereceram a empresa à Blockbuster por 50 milhões de dólares. A Blockbuster recusou, faliu em 2010, e a Netflix faturou 45,2 bilhões de dólares em 2025."},
        "hi": {"title": "Blockbuster ने Netflix को $50 मिलियन में क्यों नहीं खरीदा",
               "summary": "Netflix के संस्थापकों के मुताबिक, 2000 में उन्होंने कंपनी Blockbuster को $50 मिलियन में बेचने की पेशकश की। Blockbuster ने मना किया, 2010 में दिवालिया हुई, और 2025 में Netflix की कमाई $45.2 अरब रही।"},
        "id": {"title": "Kenapa Blockbuster Tak Membeli Netflix Seharga $50 Juta",
               "summary": "Pada 2000, pendiri Netflix mengaku menawarkan perusahaannya ke Blockbuster seharga 50 juta dolar. Blockbuster menolak, bangkrut pada 2010, dan pendapatan Netflix mencapai 45,2 miliar dolar pada 2025."},
        "de": {"title": "Warum Blockbuster Netflix nicht für $50 Millionen kaufte",
               "summary": "Laut den Netflix-Gründern boten sie Blockbuster ihre Firma im Jahr 2000 für 50 Millionen Dollar an. Blockbuster lehnte ab, ging 2010 pleite, und Netflix setzte 2025 45,2 Milliarden Dollar um."},
        "fr": {"title": "Pourquoi Blockbuster n'a pas acheté Netflix $50 millions",
               "summary": "En 2000, les fondateurs de Netflix disent avoir proposé leur société à Blockbuster pour 50 millions de dollars. Blockbuster a refusé, a fait faillite en 2010, et Netflix a réalisé 45,2 milliards de dollars de revenus en 2025."},
    },
    "scenes": [
        {"say": "In two thousand, Netflix's founders say they offered to sell their company to Blockbuster for fifty million dollars. Blockbuster said no.",
         "visual": {"type": "stat", "value": "$50M", "label": "Netflix's asking price, 2000",
                    "sub": "as told by both Netflix co-founders", "color": "gold"}},
        {"say": "Back then, Netflix brought in about thirty-six million dollars a year, and lost fifty-seven million.",
         "visual": {"type": "compare", "title": "Netflix in 2000",
                    "left": {"label": "Revenue", "value": NFLX_REV_2000, "color": "green"},
                    "right": {"label": "Net loss", "value": NFLX_LOSS_2000, "color": "red"}}},
        {"say": "Blockbuster's former boss later said there were never serious talks. But both Netflix co-founders describe the offer in their books.",
         "visual": {"type": "pair", "title": "Two sides of the story",
                    "left": {"label": "Netflix", "sub": "“We offered $50M”", "color": "red"},
                    "right": {"label": "Blockbuster", "sub": "“No serious talks”", "color": "blue"}}},
        {"say": "Blockbuster peaked at about nine thousand one hundred stores in two thousand four. In September twenty ten, it filed for bankruptcy.",
         "visual": {"type": "equation", "title": "Blockbuster",
                    "lines": [{"text": f"{BB_PEAK_STORES:,} stores", "color": "blue", "size": 110},
                              {"text": f"at its peak, {BB_PEAK_YEAR}", "color": "muted", "size": 52},
                              {"text": "Bankrupt", "color": "red", "size": 110},
                              {"text": f"September {BB_BANKRUPT_YEAR}", "color": "muted", "size": 52}]}},
        {"say": "Netflix moved from DVDs by mail to streaming. In twenty twenty-five, it brought in forty-five billion dollars, about nine hundred times that asking price, in a single year.",
         "visual": {"type": "bars", "title": "Asking price vs revenue",
                    "items": [{"label": "Price, 2000", "value": OFFER_PRICE, "color": "slate"},
                              {"label": "Revenue, 2025", "value": NFLX_REV_2025, "color": "green"}]}},
        {"say": "The lesson: protecting this year's profits can cost you the future. Keep asking what your customers will want next.",
         "visual": {"type": "equation", "title": "The lesson",
                    "lines": [{"text": "Protect today's profits?", "color": "muted", "size": 64},
                              {"text": "Protect the future.", "color": "gold", "size": 84},
                              {"text": "Ask what customers want next", "color": "text", "size": 50}]}},
        {"say": "Share this with someone who needs it.",
         "visual": {"type": "cta", "lines": ["$50 million.", "Turned down."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "029_netflix_blockbuster.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
