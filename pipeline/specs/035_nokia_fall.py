"""Video 035 (global): Nokia, from 4 in 10 phones sold to selling its phone business. Pillar: Case Studies."""
import json, os

# ---------------------------------------------------------------- sourced facts
# Nokia Q4 and full-year 2007 results, Form 6-K (SEC EDGAR, Jan 24, 2008): "Nokia estimated device market
# share of 40%" in Q4 2007 (up from 36% in Q4 2006); full year 2007 "38%"; 437.1 million devices in 2007.
NOKIA_SHARE_Q4_2007 = 40
NOKIA_SHARE_FY_2007 = 38
# Gartner, worldwide mobile phone sales to end users, Q2 2013 (Aug 14, 2013; table as published by
# TelecomLead): Nokia 60,953.7 thousand units, 14.0% share (Q2 2012: 19.9%).
NOKIA_SHARE_Q2_2013 = 14.0
# Stephen Elop "burning platform" memo to Nokia staff, Feb 2011 (published by Engadget, Feb 8, 2011, confirmed
# genuine by multiple sources): "The first iPhone shipped in 2007, and we still don't have a product that is
# close to their experience." / "We fell behind, we missed big trends, and we lost time."
IPHONE_YEAR = 2007
MEMO_YEAR = 2011
# Microsoft press release, Sept 3, 2013: EUR 3.79B for "substantially all of Nokia's Devices & Services
# business" + EUR 1.65B to license Nokia's patents = "total transaction price of EUR 5.44 billion in cash".
# TechCrunch (Sept 2, 2013): "currently worth $7.17 billion in U.S. dollars". Closed Apr 25, 2014 (Nokia release,
# which describes the remaining Nokia as its networks business (NSN), HERE maps and Technologies: "survived as a
# network equipment company").
DEAL_YEAR = 2013
DEAL_DEVICES_EUR, DEAL_PATENTS_EUR, DEAL_TOTAL_EUR = 3.79e9, 1.65e9, 5.44e9
DEAL_TOTAL_USD = 7.17e9
# Microsoft press release, July 8, 2015: "impairment charge of approximately $7.6 billion" related to assets
# from the Nokia Devices and Services acquisition; "reduction of up to 7,800 positions".
WRITEOFF_YEAR, WRITEOFF_USD = 2015, 7.6e9

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert abs(DEAL_DEVICES_EUR + DEAL_PATENTS_EUR - DEAL_TOTAL_EUR) < 1e6
assert NOKIA_SHARE_Q4_2007 / 100 == 4 / 10                 # "four in every ten phones sold"
assert round(DEAL_TOTAL_USD / 1e9, 1) == 7.2               # "about seven point two billion dollars"
assert WRITEOFF_YEAR - DEAL_YEAR == 2                      # "two years later"
assert WRITEOFF_USD > DEAL_TOTAL_USD                       # write-off bigger than the price (in USD terms)
assert MEMO_YEAR - IPHONE_YEAR == 4
print(f"share {NOKIA_SHARE_Q4_2007}% -> {NOKIA_SHARE_Q2_2013}%; deal ${DEAL_TOTAL_USD/1e9:.2f}B, "
      f"write-off ${WRITEOFF_USD/1e9:.1f}B")

spec = {
    "id": "035_nokia_fall",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "CASE STUDY",
    "disclaimer": "Sources: Nokia, Gartner, Microsoft · see description",
    "title": "Nokia: From 40% of Phones to Selling the Business",
    "description": (
        "At the end of 2007, Nokia estimated it sold about 4 in every 10 phones in the world. The first iPhone "
        "shipped that same year. By mid-2013, Gartner put Nokia at 14% of phone sales, and Microsoft agreed to "
        "buy its phone business plus a patent licence for EUR 5.44 billion (about $7.2 billion). In 2015 "
        "Microsoft took a $7.6 billion impairment charge tied to the deal. Nokia itself survived as a network "
        "equipment company. The lesson: success can make you slow to change.\n\n"
        "Sources: Nokia Q4 and full-year 2007 results, Form 6-K (Jan 24, 2008); Gartner mobile phone sales, "
        "Q2 2013 (Aug 14, 2013); Stephen Elop memo to Nokia staff (Feb 2011, published by Engadget, Feb 8, "
        "2011); Microsoft press releases (Sept 3, 2013; July 8, 2015); TechCrunch (Sept 2, 2013) for the "
        "dollar conversion; Nokia release on completing the sale (Apr 25, 2014). Market share figures come from "
        "Nokia's own estimate (2007) and Gartner (2013), which use different methods.\n\n"
        "#nokia #business #casestudy #smartphones #microsoft"
    ),
    "tags": ["nokia", "rise and fall of nokia", "why nokia failed", "nokia microsoft deal", "iphone",
             "business case study", "business lessons", "disruption", "smartphones"],
    "localizations": {
        "es": {"title": "Nokia: del 40% de los móviles a vender el negocio",
               "summary": "En 2007, Nokia vendía unos 4 de cada 10 móviles del mundo. En 2013 vendió su negocio de teléfonos a Microsoft por 5.440 millones de euros. Por qué el éxito puede volverte lento."},
        "pt": {"title": "Nokia: de 40% dos celulares a vender o negócio",
               "summary": "Em 2007, a Nokia vendia cerca de 4 em cada 10 celulares do mundo. Em 2013, vendeu sua divisão de celulares à Microsoft por 5,44 bilhões de euros. Por que o sucesso pode deixar você lento."},
        "hi": {"title": "नोकिया: 40% फ़ोन बाज़ार से बिज़नेस बेचने तक",
               "summary": "2007 में दुनिया के हर 10 में से करीब 4 फ़ोन नोकिया के थे। 2013 में उसने अपना फ़ोन बिज़नेस 5.44 अरब यूरो में माइक्रोसॉफ्ट को बेच दिया। सफलता कैसे बदलाव को धीमा कर देती है।"},
        "id": {"title": "Nokia: Dari 40% Pasar Ponsel hingga Jual Bisnisnya",
               "summary": "Pada 2007, Nokia menjual sekitar 4 dari 10 ponsel di dunia. Pada 2013, bisnis ponselnya dijual ke Microsoft seharga 5,44 miliar euro. Mengapa sukses bisa membuat lambat berubah."},
        "de": {"title": "Nokia: Von 40 % aller Handys zum Verkauf der Sparte",
               "summary": "2007 verkaufte Nokia rund 4 von 10 Handys weltweit. 2013 ging das Handygeschäft für 5,44 Milliarden Euro an Microsoft. Warum Erfolg träge machen kann."},
        "fr": {"title": "Nokia : de 40 % des téléphones à la vente de l'activité",
               "summary": "En 2007, Nokia vendait environ 4 téléphones sur 10 dans le monde. En 2013, son activité mobile a été vendue à Microsoft pour 5,44 milliards d'euros. Pourquoi le succès peut ralentir le changement."},
    },
    "scenes": [
        {"say": "At the end of two thousand seven, about four in every ten phones sold worldwide were Nokias.",
         "visual": {"type": "stat", "value": f"{NOKIA_SHARE_Q4_2007}%", "label": "of phones sold were Nokias",
                    "sub": "Q4 2007 · Nokia's own estimate", "color": "blue"}},
        {"say": "That same year, Apple shipped its very first iPhone.",
         "visual": {"type": "pair", "title": str(IPHONE_YEAR),
                    "left": {"label": "Nokia", "sub": "the giant", "color": "blue"},
                    "right": {"label": "iPhone", "sub": "the newcomer", "color": "slate"}}},
        {"say": "By mid twenty thirteen, research firm Gartner put Nokia at just fourteen percent of phone sales.",
         "visual": {"type": "bars", "title": "Nokia's share of phones sold (%)", "format": "num",
                    "items": [{"label": "End 2007", "value": NOKIA_SHARE_Q4_2007, "color": "blue"},
                              {"label": "Mid 2013", "value": NOKIA_SHARE_Q2_2013, "color": "red"}]}},
        {"say": "In twenty eleven, its own chief executive had written to staff: we fell behind, we missed big trends, and we lost time.",
         "visual": {"type": "equation", "title": f"Nokia CEO memo, {MEMO_YEAR}",
                    "lines": [{"text": "“We fell behind,", "color": "text", "size": 84},
                              {"text": "we missed big trends,", "color": "text", "size": 84},
                              {"text": "and we lost time.”", "color": "gold", "size": 84}]}},
        {"say": "In twenty thirteen, Microsoft agreed to buy Nokia's phone business, plus a patent licence, for about seven point two billion dollars. Two years later, Microsoft wrote off seven point six billion tied to the deal.",
         "visual": {"type": "compare", "title": "Microsoft and Nokia's phones",
                    "left": {"label": "Paid, 2013", "value": DEAL_TOTAL_USD, "color": "slate"},
                    "right": {"label": "Written off, 2015", "value": WRITEOFF_USD, "color": "red"}}},
        {"say": "Nokia itself survived, as a network equipment company. The lesson: success can make you slow to change. When you're winning, ask what could make your best product obsolete.",
         "visual": {"type": "equation", "title": "The lesson",
                    "lines": [{"text": "Success can make", "color": "text", "size": 80},
                              {"text": "you slow to change.", "color": "gold", "size": 80},
                              {"text": "What could replace your best product?", "color": "muted", "size": 42}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Winning today", "isn't enough."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "035_nokia_fall.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
