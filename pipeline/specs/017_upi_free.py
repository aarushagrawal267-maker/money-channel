"""Video 017 (India story for a global viewer): UPI is free to use, so who pays for it? Pillar: Business Breakdowns."""
import json, os

# ---------------------------------------------------------------- sourced facts
# NPCI monthly UPI statistics for October 2026, released Nov 1, 2026 (npci.org.in blocks automated fetches;
# figures as reported citing NPCI by Free Press Journal, updated Nov 2, 2026, and Entrepreneur India).
UPI_OCT26_TXNS = 25.47e9          # transactions
UPI_OCT26_VALUE = 31.53e12        # ₹31.53 lakh crore
# PIB / Ministry of Finance backgrounder, 24 Mar 2025 (Cabinet approval 19 Mar 2025):
# "Since January 2020 ... MDR has been made zero for RuPay Debit Card and BHIM-UPI transactions";
# "As per RBI, MDR of up to 0.90% ... for debit cards"; incentive scheme outlay ₹1,500 crore for
# FY 2024-25 (1 Apr 2024 - 31 Mar 2025), 0.15% on P2M payments up to ₹2,000 to small merchants,
# "paid by the Government to the Acquiring Bank ... then shared among ... Issuer Bank, PSP Bank, App Providers".
ZERO_MDR_SINCE = 2020
DEBIT_MDR_CAP = 0.0090
GOVT_INCENTIVE_FY25 = 1500e7      # ₹1,500 crore
# NPCI, "FAQs: Merchant Discount Rate (MDR) on Select UPI (P2M) Transactions", 15 Sept 2026:
# Q10 "Industry estimates indicate that maintaining UPI ... costs around ~₹20,000 crore annually."
# Q3 "A MDR of 0.4% ... on P2M UPI transactions above ₹2,000 ... ₹75,000 and above ... capped at ₹300."
# Q2 transactions up to ₹2,000 are "more than 95% of the total volume of UPI (P2M)".
# Q15/Q16: consumers and person-to-person transfers are not charged.
UPI_COST_EST = 20_000e7           # ₹20,000 crore a year (industry estimate cited by NPCI)
NEW_MDR, MDR_FLOOR_AMT, MDR_CAP = 0.004, 2000, 300
SMALL_SHARE = 0.95
# Business Today, 20 Nov 2026: the Oct 15 start was "deferred ... until after Diwali"; no new date announced.
# Apps' other income: PhonePe updated DRHP (reported by DT Next, 6 Mar 2026: merchant lending, Smart Speaker
# device subscriptions); Paytm Q2 FY27 results (Oct 27, 2026): financial services distribution revenue ₹912 crore.

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert UPI_OCT26_TXNS > 25e9                                  # "over twenty-five billion"
avg_ticket = UPI_OCT26_VALUE / UPI_OCT26_TXNS
assert 1200 < avg_ticket < 1300                               # description: "about ₹1,240 per payment"
SALE = 1000
debit_fee, upi_fee = SALE * DEBIT_MDR_CAP, 0
assert abs(debit_fee - 9) < 1e-9                                      # "up to ₹9 on a ₹1,000 sale"
assert abs(DEBIT_MDR_CAP * 100 - 0.9) < 1e-9                          # "zero point nine percent"
assert UPI_COST_EST / GOVT_INCENTIVE_FY25 > 13                # incentive covers a small slice of the estimate
assert abs(NEW_MDR * 75000 - MDR_CAP) < 1e-9                          # cap kicks in at ₹75,000
assert abs(NEW_MDR * MDR_FLOOR_AMT - 8) < 1e-9                        # fee threshold example
print(f"avg UPI payment ₹{avg_ticket:,.0f}; cost/incentive = {UPI_COST_EST / GOVT_INCENTIVE_FY25:.1f}x")

spec = {
    "id": "017_upi_free",
    "currency": "inr", "voice": "af_heart", "speed": 1.05,
    "badge": "INDIA STORY",
    "disclaimer": "Figures: NPCI, Govt of India (PIB) · status as of Nov 2026",
    "title": "25 billion payments a month, and they're free. Who pays for India's UPI? #shorts",
    "description": (
        f"India's UPI handled about 25.5 billion payments worth ₹31.53 lakh crore in October 2026 "
        f"(about ₹{avg_ticket:,.0f} per payment on average), and customers pay nothing. Since 2020 the law has kept the "
        "merchant fee (MDR) at zero, the government has paid banks an incentive on small shop payments, and apps "
        "earn from loans, insurance and shop devices instead. In September 2026, NPCI announced a 0.4% fee on shop "
        "payments above ₹2,000 (capped at ₹300, paid by merchants, not customers); its 15 October start was "
        "deferred and no new date had been announced as of 20 November 2026.\n\n"
        "Sources: NPCI monthly UPI statistics, October 2026 (reported 1-2 Nov 2026); PIB / Ministry of Finance, "
        "'₹1,500 Cr Incentive Scheme for Low-Value BHIM-UPI Transactions' (24 Mar 2025); NPCI FAQs on MDR on select "
        "UPI P2M transactions (15 Sep 2026); Business Today (20 Nov 2026) on the deferral; PhonePe updated DRHP "
        "(Mar 2026); Paytm Q2 FY27 results (27 Oct 2026).\n\n"
        "#upi #india #fintech #digitalpayments #business"
    ),
    "tags": ["upi", "how upi makes money", "upi mdr", "npci", "phonepe", "paytm", "google pay",
             "digital payments india", "fintech", "business breakdown"],
    "scenes": [
        {"say": "In October, Indians made over twenty-five billion UPI payments and paid nothing to send them. So who pays?",
         "visual": {"type": "stat", "value": "25.5B", "label": "UPI payments in October 2026",
                    "sub": "worth ₹31.5 lakh crore · source: NPCI", "color": "gold"}},
        {"say": "UPI is India's instant payment system. Scan a QR code, and money moves bank to bank.",
         "visual": {"type": "pair", "title": "How UPI works",
                    "left": {"label": "You", "sub": "scan a QR code", "color": "green"},
                    "right": {"label": "Shop", "sub": "paid in seconds", "color": "gold"}}},
        {"say": "Shops pay up to zero point nine percent on debit card sales in India. On UPI, they pay zero, by law, since twenty twenty.",
         "visual": {"type": "compare", "title": "Shop's fee on a ₹1,000 sale",
                    "left": {"label": "Debit card", "value": debit_fee, "color": "red"},
                    "right": {"label": "UPI", "value": upi_fee, "color": "green"}}},
        {"say": "But running UPI isn't free. NPCI cites estimates of twenty thousand crore rupees a year. The government's incentive to banks for twenty twenty-four to twenty-five? Fifteen hundred crore.",
         "visual": {"type": "bars", "title": "Who covers the bill?",
                    "items": [{"label": "Cost (est.)", "value": UPI_COST_EST, "color": "red"},
                              {"label": "Govt help", "value": GOVT_INCENTIVE_FY25, "color": "green"}]}},
        {"say": "So apps like PhonePe and PayTM earn elsewhere: loans, insurance, and payment speakers rented to shops.",
         "visual": {"type": "equation", "title": "How the apps earn",
                    "lines": [{"text": "Loans", "color": "gold", "size": 96},
                              {"text": "Insurance", "color": "text", "size": 84},
                              {"text": "Shop speakers", "color": "muted", "size": 72}]}},
        {"say": "And free may not last. India plans a zero point four percent fee on shop payments over two thousand rupees, paid by the shop, not you. The start has been delayed.",
         "visual": {"type": "equation", "title": "Announced, not yet started",
                    "lines": [{"text": "0.4% fee", "color": "red", "size": 130},
                              {"text": "shop payments over ₹2,000", "color": "text", "size": 58},
                              {"text": "paid by the shop · capped at ₹300", "color": "muted", "size": 46}]}},
        {"say": "Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Free for you.", "Not free to run."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "017_upi_free.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
