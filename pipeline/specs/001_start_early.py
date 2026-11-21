"""Video 001: Same SIP, start at 25 vs 35. All numbers computed here, not typed by hand."""
import json, os

SIP, ANNUAL = 5000, 0.12
r = ANNUAL / 12

def fv(months):
    """Future value of a monthly SIP (investment at start of each month)."""
    return SIP * (((1 + r) ** months - 1) / r) * (1 + r) if months > 0 else 0

ages = list(range(25, 61))
rahul = [fv((a - 25) * 12) for a in ages]
aman = [fv(max(0, (a - 35) * 12)) for a in ages]
R60, A60 = rahul[-1], aman[-1]
R_inv, A_inv = SIP * 12 * 35, SIP * 12 * 25

# sanity checks behind every spoken claim
assert R60 > 3e7                       # "over three crore"
assert 9.4e6 < A60 < 9.6e6             # "about ninety-five lakh"
assert R_inv == 2.1e6 and A_inv == 1.5e6
assert R60 - A60 > 2e7                 # "over two crore more"
assert abs(rahul[ages.index(50)] - A60) < 1  # Rahul at 50 == Aman at 60
gain_last5 = R60 - rahul[ages.index(55)]
assert 1.4e7 < gain_last5 < 1.5e7      # "almost one and a half crore"

spec = {
    "id": "001_start_early",
    "currency": "inr", "voice": "af_heart", "speed": 1.06,
    "badge": "DAILY MONEY LESSON",
    "disclaimer": "Illustration · assumes ~12% p.a. · returns not guaranteed · not financial advice",
    "title": "Same ₹5,000 SIP. ₹3.2 Crore vs ₹95 Lakh. Why? #shorts",
    "description": (
        "Two friends invest the same ₹5,000 every month. One starts at 25, the other at 35. "
        "At 60, one has over ₹3.2 crore and the other about ₹95 lakh.\n\n"
        "Assumptions: ₹5,000 monthly SIP, ~12% average annual return compounded monthly, "
        "invested at the start of each month until age 60. Illustration only: market returns "
        "vary and are not guaranteed. This is not financial advice.\n\n"
        "#sip #compounding #personalfinance #investing #mutualfunds #moneytips"
    ),
    "tags": ["sip", "compounding", "personal finance india", "mutual funds", "investing",
             "money tips", "financial literacy", "power of compounding", "start investing early"],
    "scenes": [
        {"say": "Two friends invest the same five thousand rupees every month.",
         "visual": {"type": "pair", "title": "Same SIP. Same fund.",
                    "left": {"label": "Rahul", "sub": "₹5,000 / month", "color": "green"},
                    "right": {"label": "Aman", "sub": "₹5,000 / month", "color": "slate"}}},
        {"say": "At sixty, one has over three crore. The other? About ninety-five lakh.",
         "visual": {"type": "compare", "title": "Wealth at age 60",
                    "left": {"label": "Rahul", "value": R60, "color": "green"},
                    "right": {"label": "Aman", "value": A60, "color": "slate"}}},
        {"say": "The only difference: Rahul started at twenty-five. Aman waited until thirty-five.",
         "visual": {"type": "timeline", "title": "The only difference", "start": 25, "end": 60,
                    "rows": [{"label": "Rahul", "from": 25, "color": "green"},
                             {"label": "Aman", "from": 35, "color": "slate"}]}},
        {"say": "Both earn about twelve percent a year, a common long-term assumption for Indian equity funds.",
         "visual": {"type": "stat", "value": "12%", "label": "average yearly return",
                    "sub": "assumed · not guaranteed", "color": "gold"}},
        {"say": "Rahul puts in twenty-one lakh in total. Aman puts in fifteen.",
         "visual": {"type": "bars", "title": "Total money invested",
                    "items": [{"label": "Rahul", "value": R_inv, "color": "green"},
                              {"label": "Aman", "value": A_inv, "color": "slate"}]}},
        {"say": "Just six lakh more, but Rahul ends up with over two crore more.",
         "visual": {"type": "equation",
                    "lines": [{"text": "+₹6 L invested", "color": "muted", "size": 84},
                              {"text": "↓", "color": "dim", "size": 84},
                              {"text": "+₹2.3 Cr wealth", "color": "green", "size": 100}]}},
        {"say": "Here's the crazy part. By fifty, Rahul already has ninety-five lakh. That's Aman's entire final amount, ten years early.",
         "visual": {"type": "line", "title": "Growth by age", "x": ages, "x_label": "age",
                    "series": [{"label": "Rahul", "values": rahul, "color": "green"},
                               {"label": "Aman", "values": aman, "color": "slate"}],
                    "hline": {"value": A60, "label": "Aman at 60 = Rahul at 50", "x": 50, "at": 2.2}}},
        {"say": "And in his last five years alone, his money grows by almost one and a half crore.",
         "visual": {"type": "line", "title": "The last 5 years", "x": ages, "x_label": "age", "reveal": False,
                    "series": [{"label": "Rahul", "values": rahul, "color": "green"},
                               {"label": "Aman", "values": aman, "color": "slate"}],
                    "highlight": {"from": 55, "to": 60, "label": "+₹1.5 Cr"}}},
        {"say": "That's compounding. The biggest gains come at the very end, so every year you wait cuts off the best part.",
         "visual": {"type": "equation", "title": "Compounding rewards",
                    "lines": [{"text": "TIME", "color": "gold", "size": 200},
                              {"text": "more than amount", "color": "muted", "size": 64}]}},
        {"say": "Start today, even with five hundred rupees. Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Start today.", "Even ₹500."],
                    "sub": "Follow for daily money lessons"}},
    ],
}

out = os.path.join(os.path.dirname(__file__), "001_start_early.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, f"R60={R60:,.0f} A60={A60:,.0f} last5={gain_last5:,.0f}")
