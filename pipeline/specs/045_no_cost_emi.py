"""Video 045 (India story for a global viewer): "no-cost EMI" and who really pays the interest. Pillar: Financing traps."""
import json, os

# ---------------------------------------------------------------- sourced facts
# SBI Card, "No Cost EMI" terms/calculator page (sbicard.com/.../offers/calculator/cal-tc.html, checked 25 Nov 2026):
# "The Brands or Manufacturer/OEMs ... bear the interest cost for EMI on specific tenures" (called "Interest
# Subvention"); "Manufacturer cashback equivalent to interest levied amount is credited / adjusted upfront".
# Worked example on that page: transaction Rs 35,000, 6-month EMI, "14% rate of interest on monthly reducing
# balance", manufacturer cashback 3.96% = Rs 1,386, loan booked on Rs 33,614, EMI Rs 5,833, total paid Rs 35,000.
# The page also says SBI Card does not use the "No Cost" label in promotions because of RBI guidelines.
PRICE = 35_000
MONTHS = 6
RATE = 0.14
CASHBACK = 1_386
BOOKED = 33_614
EMI_SBI = 5_833
# HDFC Bank, "EasyEMI on Credit Card" (hdfc.bank.in/easyemi/credit-card, checked 25 Nov 2026):
# "Processing Fee - ₹99 to ₹699 + GST (*varies by product and merchant) applicable on EMI transactions";
# "GST of 18% is applicable. GST will be applicable on the Interest Component of EMI."
FEE_MIN, FEE_MAX = 99, 699
GST = 0.18
# Kotak Mahindra Bank, "How to avail Amazon No Cost EMI on credit cards" (10 Dec 2025): "Participating sellers and
# brands fund No Cost EMI"; "Bank will continue to charge interest + GST"; "GST & processing fees may be applicable".
# RBI circular RBI/2013-14/292, "Pernicious practices of select banks deterring customer protection and accounting
# integrity" (17 Sept 2013), para 3: in credit card zero percent EMI schemes "the interest element is often
# camouflaged and passed on to customer in the form of processing fee"; "the very concept of zero percent interest
# is non-existent".
RBI_YEAR = 2013
# FX for the one USD equivalent: rupee closed at 93.44 per US dollar on 18 Nov 2026 (PTI, via Telangana Today).
INR_PER_USD = 93.44

# ---------------------------------------------------------------- checks behind spoken / shown claims
r = RATE / 12
emi = BOOKED * r / (1 - (1 + r) ** -MONTHS)
assert abs(emi - EMI_SBI) < 2, emi                           # SBI Card's EMI reproduces at 14% on reducing balance
assert abs(EMI_SBI * MONTHS - PRICE) < 5                     # "you still repay thirty-five thousand" (rounded EMIs)
assert BOOKED + CASHBACK == PRICE                            # loan = price minus the brand's discount
assert abs(emi * MONTHS - BOOKED - CASHBACK) < 15            # interest at 14% ≈ the discount (Rs 1,386)
assert round(CASHBACK / PRICE * 100, 2) == 3.96              # SBI Card: "3.96%"
assert round(RATE * 100) == 14                               # "fourteen percent"
gst_on_interest = CASHBACK * GST
assert abs(gst_on_interest - 249.48) < 0.01                  # "about two hundred fifty rupees"
assert round(gst_on_interest, -1) == 250
usd = PRICE / INR_PER_USD
assert 370 < usd < 380 and round(usd / 5) * 5 == 375, usd  # "about three hundred seventy-five dollars"
assert (FEE_MIN, FEE_MAX) == (99, 699)                       # "ninety-nine to six hundred ninety-nine rupees"
extra_low = gst_on_interest + FEE_MIN * (1 + GST)
extra_high = gst_on_interest + FEE_MAX * (1 + GST)
assert 365 < extra_low < 370 and 1070 < extra_high < 1075    # description: "roughly ₹366 to ₹1,074 extra"
assert RBI_YEAR == 2013
print(f"EMI ₹{emi:.0f}; interest ₹{CASHBACK}; GST ₹{gst_on_interest:.2f}; ${usd:.0f}; "
      f"extra cost ₹{extra_low:.0f}-₹{extra_high:.0f}")

spec = {
    "id": "045_no_cost_emi",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "MONEY TRAP",
    "disclaimer": "Sources: SBI Card, HDFC Bank, RBI · see description",
    "title": "No-Cost EMI Explained: Who Really Pays the Interest?",
    "description": (
        "Is no-cost EMI really free? The bank still charges interest; the brand or seller pays it for you as an "
        "upfront discount (banks call this interest subvention). In SBI Card's own example, a ₹35,000 purchase "
        "(about $375) over 6 months at 14% carries ₹1,386 of interest, covered by a ₹1,386 discount, so the six "
        "EMIs add up to ₹35,000. But the discount doesn't cover the 18% GST on that interest (about ₹250 here), and "
        f"many banks add a processing fee: HDFC Bank lists ₹{FEE_MIN} to ₹{FEE_MAX} + GST on EMI transactions. In "
        f"this example that is roughly ₹{extra_low:.0f} to ₹{extra_high:,.0f} extra. Compare with the price for "
        "paying in full before you choose EMI.\n\n"
        "In 2013 the Reserve Bank of India told banks that in zero percent EMI schemes the interest is often "
        "camouflaged as a processing fee, and that \"the very concept of zero percent interest is non-existent\".\n\n"
        "Sources: SBI Card No Cost EMI terms and worked example (sbicard.com, checked 25 Nov 2026); HDFC Bank "
        "EasyEMI on Credit Card page (checked 25 Nov 2026); Kotak Mahindra Bank, 'How to avail Amazon No Cost EMI' "
        "(10 Dec 2025); RBI circular RBI/2013-14/292 (17 Sept 2013). Dollar figure at ₹93.44 per $ (PTI, 18 Nov 2026). "
        "Fees and rates vary by bank, card and offer; check your offer's terms. Educational content, not financial "
        "advice.\n\n"
        "#emi #india #creditcard #personalfinance #moneytips"
    ),
    "tags": ["no cost emi", "no cost emi explained", "is no cost emi really free", "zero interest emi",
             "credit card emi", "gst on emi interest", "emi processing fee", "personal finance india"],
    "localizations": {
        "es": {"title": "EMI sin costo: ¿quién paga realmente los intereses?",
               "summary": "En la India, las cuotas \"sin costo\" sí cobran intereses: la marca los paga con un descuento. Pero tú pagas el 18% de GST sobre esos intereses y a veces una comisión."},
        "pt": {"title": "EMI sem custo: quem realmente paga os juros?",
               "summary": "Na Índia, a parcela \"sem custo\" tem juros: a marca os paga com um desconto. Mas você paga 18% de GST sobre os juros e, muitas vezes, uma taxa de processamento."},
        "hi": {"title": "No-Cost EMI: असल में ब्याज कौन चुकाता है?",
               "summary": "No-cost EMI में बैंक ब्याज लेता है, जिसे ब्रांड छूट देकर चुकाता है। लेकिन उस ब्याज पर 18% GST और प्रोसेसिंग फ़ीस आप देते हैं।"},
        "id": {"title": "EMI Tanpa Biaya: Siapa yang Bayar Bunganya?",
               "summary": "Di India, cicilan \"tanpa biaya\" tetap berbunga: merek membayarnya lewat diskon. Tapi kamu tetap bayar GST 18% atas bunga itu dan sering juga biaya proses."},
        "de": {"title": "No-Cost-EMI: Wer zahlt wirklich die Zinsen?",
               "summary": "In Indien kosten \"kostenlose\" Raten trotzdem Zinsen: Die Marke zahlt sie per Rabatt. Die 18 % GST auf die Zinsen und oft eine Gebühr zahlst aber du."},
        "fr": {"title": "EMI sans frais : qui paie vraiment les intérêts ?",
               "summary": "En Inde, les mensualités \"sans frais\" portent des intérêts, payés par la marque via une remise. Mais vous payez 18 % de GST sur ces intérêts et souvent des frais de dossier."},
    },
    "thumbnail": {"big": f"₹{gst_on_interest:.0f}", "line": "Still on your bill", "color": "red",
                  "photo": {"file": "assets/photos/credit_card_tap_terminal_hand.jpg", "focus": [0.6, 0.5]}},
    "scenes": [
        # hook: contradiction + the rate on frame 0 + open loop ("who actually pays it?")
        {"say": "No-cost E-M-I still charges interest. Who actually pays it?",
         "visual": {"type": "stat", "value": f"{RATE:.0%}", "label": "interest on a 'no-cost' EMI",
                    "sub": "SBI Card's own 6-month example", "color": "red"}},
        {"say": "S-B-I Card's example: a thirty-five thousand rupee purchase, about three hundred seventy-five dollars.",
         "visual": {"type": "photo", "file": "assets/photos/credit_card_tap_terminal_hand.jpg", "title": "SBI Card's example",
                    "value": f"₹{PRICE:,}", "color": "gold", "label": f"≈ ${usd:.0f} · {MONTHS} monthly EMIs",
                    "focus": [0.55, 0.45]}},
        {"say": "At fourteen percent over six months, that's thirteen hundred eighty-six rupees interest.",
         "visual": {"type": "compare", "title": f"{RATE:.0%} a year, {MONTHS} months",
                    "left": {"label": "Price", "value": PRICE, "color": "slate"},
                    "right": {"label": "Interest", "value": CASHBACK, "color": "red"}}},
        {"say": "The brand pays it, as an upfront discount. You still repay thirty-five thousand.",
         "visual": {"type": "pair", "title": "Who pays the interest?",
                    "left": {"label": "Brand", "sub": "gives a discount", "color": "gold"},
                    "right": {"label": "You", "sub": f"repay ₹{PRICE:,}", "color": "green"}}},
        # mid-video re-hook: opens a second loop (what isn't covered?)
        {"say": "But here's the catch: the discount doesn't cover the tax.",
         "visual": {"type": "equation", "title": "The catch",
                    "lines": [{"text": "Interest: covered.", "color": "green", "size": 96},
                              {"text": "Tax on it: not.", "color": "red", "size": 96}]}},
        {"say": "You pay eighteen percent G-S-T on that interest: about two hundred fifty rupees.",
         "visual": {"type": "stat", "value": f"₹{gst_on_interest:.0f}", "label": "18% GST on ₹1,386 interest",
                    "sub": "paid by you, not the brand", "color": "red"}},
        {"say": "Often a processing fee: H-D-F-C lists ninety-nine to six hundred ninety-nine rupees.",
         "visual": {"type": "bars", "title": "HDFC EMI processing fee (+GST)",
                    "items": [{"label": "Lowest", "value": FEE_MIN, "color": "gold"},
                              {"label": "Highest", "value": FEE_MAX, "color": "red"}]}},
        {"say": "In twenty thirteen, India's central bank called zero percent interest non-existent.",
         "visual": {"type": "equation", "title": f"Reserve Bank of India, {RBI_YEAR}",
                    "lines": [{"text": "“The very concept of", "color": "text", "size": 76},
                              {"text": "zero percent interest", "color": "gold", "size": 76},
                              {"text": "is non-existent.”", "color": "text", "size": 76}]}},
        {"say": "Compare the full-payment price, and add every fee.",
         "visual": {"type": "photo", "file": "assets/photos/online_shopping_cart_phone.jpg", "title": "Before you click",
                    "label": "Full price vs EMI + GST + fees", "focus": [0.45, 0.5]}},
        # loop line: runs back into "No-cost E-M-I still charges interest..."
        {"say": "So remember, even a...",
         "visual": {"type": "cta", "lines": ["No-cost EMI?", "Read the fees."],
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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "045_no_cost_emi.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
